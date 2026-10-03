#!/usr/bin/env python3
"""Weekly Codex limit of the ChatGPT Pro plan during the port, from local session logs.

Usage:
    python3 scripts/collect_limits.py [/path/to/ntsd-2.4]

Every Codex response logs the account's rate limits: the weekly window
(10,080 minutes), its used percentage and when it resets. From those readings:
  * windows: one weekly window per distinct resets_at (readings of an older window that
    arrive after a newer one are dropped); a window that starts before the previous one
    was due is an early reset;
  * burn: per local day, increases of the running maximum inside a window, attributed to
    the session whose reading showed them (port sessions vs the rest of the account);
  * gauge: the highest reading per 20 minutes, for the sawtooth chart;
  * limit hits: "You've hit your usage limit" errors that ended a turn in a port session,
    and the first 100 % reading of each window.
Writes data/codex_limits.json. Only numbers and timestamps are kept.
"""
import collections
import datetime as dt
import glob
import json
import os
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "ntsd-2.4"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "codex_limits.json")
SESSIONS = os.path.join(os.path.expanduser("~"), ".codex", "sessions")
UTC = dt.timezone.utc
START = dt.datetime(2026, 9, 6, tzinfo=UTC)
END = dt.datetime(2026, 10, 4, tzinfo=UTC)
FIRST_DAY = "2026-09-07"
SWITCH = dt.datetime(2026, 9, 27, 22, tzinfo=UTC)  # commits move from +03:00 to +02:00
# Resets OpenAI gave every paid account on these UTC dates (public announcements):
# 8 Sep — global reset after the GPT-6 Astra rollout; 26 Sep — after the 25 Sep Codex outage.
GLOBAL_RESET_DAYS = {"2026-09-08": "общий сброс OpenAI после выката GPT-6 Astra",
                     "2026-09-26": "общий сброс OpenAI после сбоя Codex 25 сентября"}


def local_day(t):
    return (t + dt.timedelta(hours=3 if t < SWITCH else 2)).date().isoformat()


def iso(t):
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%MZ")


def is_port(cwd):
    return cwd == REPO or cwd.startswith(REPO + "/") or cwd.startswith(REPO + "-")


readings = []
hits = []
for path in glob.glob(os.path.join(SESSIONS, "**", "*.jsonl"), recursive=True):
    with open(path, encoding="utf-8", errors="replace") as fh:
        try:
            meta = json.loads(fh.readline())
        except json.JSONDecodeError:
            continue
        port = is_port((meta.get("payload") or {}).get("cwd") or "")
        for ln in fh:
            if '"rate_limits"' in ln and '"token_count"' in ln:
                d = json.loads(ln)
                rl = (d.get("payload") or {}).get("rate_limits") or {}
                pr = rl.get("primary") or {}
                if rl.get("limit_id") != "codex" or pr.get("window_minutes") != 10080 or pr.get("used_percent") is None:
                    continue
                t = dt.datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00"))
                if START <= t <= END:
                    readings.append((t, float(pr["used_percent"]), int(pr["resets_at"]), port))
            elif port and "usage_limit_exceeded" in ln and '"task_complete"' in ln:
                d = json.loads(ln)
                err = ((d.get("payload") or {}).get("error") or {}).get("message", "")
                if "hit your usage limit" in err:
                    hits.append(dt.datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00")))
readings.sort()

# Windows: a reading belongs to the newest window seen so far (resets_at within an hour).
windows = []
clean = []
for t, u, r, port in readings:
    if not windows or r > windows[-1]["resets_at"] + 3600:
        windows.append({"resets_at": r, "first": t, "last": t, "max": u, "start_used": u})
    w = windows[-1]
    if abs(r - w["resets_at"]) <= 3600:
        w["last"] = t
        w["max"] = max(w["max"], u)
        clean.append((t, u, len(windows) - 1, port))

out_windows = []
for i, w in enumerate(windows):
    end = dt.datetime.fromtimestamp(w["resets_at"], UTC)
    start = end - dt.timedelta(days=7)
    item = {"start": iso(start), "end": iso(end), "max": w["max"], "first_reading": iso(w["first"])}
    if i:
        prev = windows[i - 1]
        due = dt.datetime.fromtimestamp(prev["resets_at"], UTC)
        if start < due - dt.timedelta(hours=1):
            item["early"] = True
            item["used_before"] = prev["max"]
            item["was_due"] = iso(due)
            item["origin"] = "global" if start.date().isoformat() in GLOBAL_RESET_DAYS else (
                "after_limit" if prev["max"] >= 93 else "unknown")
            if item["origin"] == "global":
                item["note"] = GLOBAL_RESET_DAYS[start.date().isoformat()]
    out_windows.append(item)

# Burn: increases of the running maximum within a window. A new window starts at zero; usage
# already present at its first reading, long after the window began, came from clients that
# leave no local log and counts as "other".
burn = collections.defaultdict(lambda: {"port": 0.0, "other": 0.0})
running = {}
for t, u, wi, port in clean:
    if wi not in running:
        if wi == 0:
            running[wi] = u
            continue
        running[wi] = 0.0
        start = dt.datetime.fromisoformat(out_windows[wi]["start"].replace("Z", "+00:00"))
        if t - start > dt.timedelta(minutes=30):
            port = False
    if u > running[wi]:
        burn[local_day(t)]["port" if port else "other"] += u - running[wi]
        key = "burn_port" if port else "burn_other"
        out_windows[wi][key] = round(out_windows[wi].get(key, 0) + u - running[wi], 1)
        running[wi] = u

days = {d: {k: round(v, 1) for k, v in vals.items()} for d, vals in sorted(burn.items()) if d >= FIRST_DAY}

# Gauge: running maximum of each window, one point per 20 minutes with readings.
CHART_FROM = dt.datetime(2026, 9, 6, 21, tzinfo=UTC)  # 7 Sep, 00:00 MSK
gauge = []
peak = {}
full = list(hits)
for t, u, wi, port in clean:
    if u >= 100 and peak.get(wi, 0) < 100:
        full.append(t)
    peak[wi] = max(peak.get(wi, 0), u)
    if t < CHART_FROM:
        continue
    key = int(t.timestamp()) // 1200
    if gauge and gauge[-1][3] == key and gauge[-1][2] == wi:
        gauge[-1][1] = peak[wi]
    else:
        gauge.append([iso(t), peak[wi], wi, key])
gauge = [g[:3] for g in gauge]

unique_hits = []
for h in sorted(x for x in full if x >= CHART_FROM):
    if not unique_hits or h - unique_hits[-1] > dt.timedelta(minutes=30):
        unique_hits.append(h)

early = [w for w in out_windows if w.get("early") and w["start"] >= FIRST_DAY]
port_total = sum(v["port"] for v in days.values())
all_total = sum(v["port"] + v["other"] for v in days.values())
out = {
    "plan": "pro",
    "price_usd_month": 200,
    "note": "percent of the weekly Codex limit; burn = increases of the running maximum per window",
    "windows": out_windows,
    "burn": days,
    "gauge": gauge,
    "limit_hits": [iso(h) for h in unique_hits],
    "totals": {
        "burn_port_percent": round(port_total),
        "burn_all_percent": round(all_total),
        "early_resets": len(early),
        "early_after_limit": sum(1 for w in early if w["origin"] == "after_limit"),
        "early_global": sum(1 for w in early if w["origin"] == "global"),
        "early_unknown": sum(1 for w in early if w["origin"] == "unknown"),
        "days": 27,
        "nominal_weekly_limits": round(27 / 7, 2),
    },
}
with open(OUT, "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(json.dumps(out["totals"], ensure_ascii=False))
for w in out_windows:
    print(w)
print("hits", out["limit_hits"])
for d, v in days.items():
    print(d, v)
