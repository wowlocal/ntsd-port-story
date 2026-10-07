#!/usr/bin/env python3
"""The four-day Claude Code session after the release (3 Oct 20:08 – 7 Oct 08:24), as counters on one time axis.

Usage:
    python3 scripts/collect_loop.py [/path/to/ntsd-2.4]

Writes data/loop.json. Reads only timestamps, token counts and message types —
no message text is stored:
  * context size of every main-thread model request (input + cache write + cache read);
  * every automatic compaction (compact_boundary);
  * turns typed or pasted by the human, /loop firings and ScheduleWakeup calls, as times only;
  * subagent files of the session (count and output tokens);
  * commits of the port repository in the same window (time and lane only),
    taken from git at the pinned head 8840eb3.
"""
import datetime as dt
import glob
import json
import os
import subprocess
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "ntsd-2.4"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "loop.json")
HOME = os.path.expanduser("~")
PROJECT = os.path.join(HOME, ".claude", "projects", REPO.replace("/", "-").replace(".", "-"))
SESSION = "1f9218ae-9d5d-4c4e-a8dd-d5254994839c"
HEAD = "8840eb3"
TZ = dt.timezone(dt.timedelta(hours=2))
END = dt.datetime(2026, 10, 7, 8, 24, tzinfo=TZ)  # the session kept running; the chapter is frozen at 8840eb3 (08:23)


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


msgs, comps, human, wakeups, scheduled = {}, [], [], [], {}
with open(os.path.join(PROJECT, SESSION + ".jsonl"), encoding="utf-8", errors="replace") as fh:
    for ln in fh:
        d = json.loads(ln)
        t = d.get("type")
        if "timestamp" not in d or ts(d["timestamp"]) > END:
            continue
        if t == "system" and d.get("subtype") == "compact_boundary":
            md = d.get("compactMetadata") or {}
            comps.append((ts(d["timestamp"]), md.get("preTokens") or 0, md.get("postTokens") or 0))
        elif t == "assistant":
            m = d.get("message") or {}
            u = m.get("usage")
            for p in m.get("content") or []:
                if isinstance(p, dict) and p.get("type") == "tool_use" and p.get("name") == "ScheduleWakeup":
                    scheduled[p.get("id")] = ts(d["timestamp"])
            if not u or m.get("model") == "<synthetic>" or not m.get("id"):
                continue
            ctx = (u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0)
            tt = ts(d["timestamp"])
            old = msgs.get(m["id"])
            if old is None or old[0] > tt:
                msgs[m["id"]] = (tt, ctx, max(u.get("output_tokens") or 0, old[2] if old else 0))
        elif t == "user":
            c = (d.get("message") or {}).get("content")
            parts = c if isinstance(c, list) else [{"type": "text", "text": c}] if isinstance(c, str) else []
            if any(isinstance(p, dict) and p.get("type") == "tool_result" for p in parts):
                continue
            text = " ".join(p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text").strip()
            tt = ts(d["timestamp"])
            if d.get("isMeta"):
                if text.startswith("# /loop"):
                    wakeups.append(tt)
            elif text.startswith("<pasted_content") or (text and not text.startswith("<") and not text.startswith("[")
                                                        and not text.startswith("This session is being continued") and not text.startswith("Skill /loop")):
                human.append(tt)

sub_files, sub_out, sub_requests = 0, 0, 0
for p in glob.glob(os.path.join(PROJECT, SESSION, "subagents", "*.jsonl")):
    seen = {}
    with open(p, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            if '"usage"' not in ln:
                continue
            d = json.loads(ln)
            m = d.get("message") or {}
            if d.get("type") == "assistant" and m.get("id") and m.get("usage") and ts(d["timestamp"]) <= END:
                seen[m["id"]] = max(seen.get(m["id"], 0), m["usage"].get("output_tokens") or 0)
    if seen:
        sub_files += 1
        sub_requests += len(seen)
        sub_out += sum(seen.values())

points = sorted(msgs.values())
start, end = points[0][0], points[-1][0]
mins = lambda t: round((t - start).total_seconds() / 60, 1)

raw = subprocess.run(["git", "-C", REPO, "log", "--reverse", "--format=%h %aI", f"74be317..{HEAD}"], check=True, capture_output=True).stdout.decode()
commits = []
for ln in raw.strip().split("\n"):
    h, d = ln.split()
    commits.append({"t": mins(dt.datetime.fromisoformat(d)), "hash": h})

data = {
    "session": SESSION[:8],
    "start": start.astimezone(TZ).isoformat(), "end": end.astimezone(TZ).isoformat(), "utc_offset_hours": 2,
    "window_k": 1000,
    "points": [[mins(t), round(v / 1000, 1)] for t, v, _ in points],
    "compactions": [{"t": mins(t), "pre_k": round(a / 1000, 1), "post_k": round(b / 1000, 1)} for t, a, b in sorted(comps)],
    "human": [mins(t) for t in human],
    "wakeups": [mins(t) for t in wakeups],
    "scheduled": sorted(mins(t) for t in scheduled.values()),
    "commits": commits,
    "totals": {
        "requests": len(points), "output_tokens": sum(o for _, _, o in points),
        "processed_tokens": sum(v for _, v, _ in points) + sum(o for _, _, o in points),
        "compactions": len(comps), "human_turns": len(human), "loop_firings": len(wakeups), "schedule_wakeup_calls": len(scheduled),
        "subagents": sub_files, "subagent_requests": sub_requests, "subagent_output_tokens": sub_out, "commits": len(commits),
        "hours": round((end - start).total_seconds() / 3600, 1),
        "max_context_k": round(max(v for _, v, _ in points) / 1000, 1),
    },
}
with open(OUT, "w") as f:
    json.dump(data, f, separators=(",", ":"))
    f.write("\n")
print(json.dumps(data["totals"], indent=1), data["start"], data["end"])
print("human turns at (h):", [round(x / 60, 1) for x in data["human"]])
