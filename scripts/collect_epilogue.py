#!/usr/bin/env python3
"""Data for the epilogue: the week after 7 October by topic, the passport on 13 October, the whole session.

Usage:
    python3 scripts/collect_epilogue.py [/path/to/ntsd-2.4]

Writes data/epilogue.json. Reads the port repository through git at pinned
commits only (nothing in it is modified) and, for the session, only times,
token counts and message types from the Claude Code log — no message text.

Pinned commits:
  PART1  fc959db   3 Oct 16:18  first part of the deck (same as collect_stats.py)
  FROZE  8840eb3   7 Oct 08:23  chapters 13-14
  NOW    5f5a8ee4 13 Oct 20:14  head of exp/iphone: main + the release + the phone controller
"""
import collections
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "ntsd-2.4"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "epilogue.json")
PART1, FROZE, NOW = "fc959db", "8840eb3", "5f5a8ee4"
SINCE = "2026-09-01"
HOME = os.path.expanduser("~")
SESSION = os.path.join(HOME, ".claude", "projects", REPO.replace("/", "-").replace(".", "-"), "1f9218ae-9d5d-4c4e-a8dd-d5254994839c")
TZ = dt.timezone(dt.timedelta(hours=2))


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], check=True, capture_output=True).stdout.decode("utf-8", "replace")


cat = subprocess.Popen(["git", "-C", REPO, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def blob(sha):
    cat.stdin.write((sha + "\n").encode())
    cat.stdin.flush()
    _, _, size = cat.stdout.readline().decode().split()
    data = cat.stdout.read(int(size))
    cat.stdout.read(1)
    return data


# ------------------------------------------------------------------ passport (definitions of collect_stats.py)
def kind(path):
    if path.endswith(".swift"):
        if path.startswith("native/Sources/"):
            return "swift-src"
        if path.startswith("native/Tests/"):
            return "swift-tests"
        return None
    if path.endswith(".py"):
        return "python"
    if path.startswith("docs/research/") and path.endswith(".md"):
        return "research-md"
    return None


def passport(ref):
    lines, files = collections.Counter(), collections.Counter()
    tests = evidence = 0
    for t in git("ls-tree", "-r", "-l", ref).split("\n"):
        if not t.strip():
            continue
        meta, path = t.split("\t", 1)
        _, _, sha, size = meta.split()
        if path.startswith("docs/evidence/"):
            evidence += 1
        k = kind(path)
        if k is None or size == "-" or int(size) > 5_000_000:
            continue
        data = blob(sha)
        files[k] += 1
        lines[k] += data.count(b"\n")
        if k == "swift-tests":
            tests += len(re.findall(rb"\bfunc test\w*", data))
    log = git("log", ref, f"--since={SINCE}", "--format=%ad", "--date=format:%Y-%m-%d").split()
    return {
        "ref": ref, "date": git("log", "-1", "--format=%ad", "--date=format:%Y-%m-%dT%H:%M:%S%z", ref).strip(),
        "commits_since_sept": len(log), "active_days": len(set(log)), "first_day": min(log), "last_day": max(log),
        "swift_src_lines": lines["swift-src"], "swift_src_files": files["swift-src"],
        "swift_test_lines": lines["swift-tests"], "test_functions": tests,
        "python_lines": lines["python"], "research_cards": files["research-md"], "evidence_files": evidence,
    }


# ------------------------------------------------------------------ the week by topic
TAGS = {"MEMORY_LOADING": "memory", "TVOS_WEB": "web", "WINDOW_SCALING": "window",
        "MENU_MEMORY": "menu", "PHONE_CONTROLLER": "controller"}
RELEASE = {"2c4db98b", "9c700dae", "0b5d4621"}
ML_START = "2026-10-10T22:00"


def topic(h, when, subject):
    m = re.search(r"\(([A-Z_]+)[ ,)]", subject)
    if m and m.group(1) in TAGS:
        return TAGS[m.group(1)]
    if h in RELEASE:
        return "release"
    if "memory and loading card" in subject:
        return "memory"
    return "realtime" if when < ML_START else "other"


week = []
for ln in git("log", "--reverse", "--no-merges", "--format=%h\x1f%aI\x1f%s\x1f%b\x1e", f"{FROZE}..{NOW}").split("\x1e"):
    if not ln.strip():
        continue
    h, when, subject, body = ln.strip("\n").split("\x1f")
    local = dt.datetime.fromisoformat(when).astimezone(TZ)
    week.append({"hash": h[:8], "time": local.strftime("%Y-%m-%dT%H:%M"), "subject": subject,
                 "topic": topic(h[:8], local.strftime("%Y-%m-%dT%H:%M"), subject),
                 "claude": "Co-Authored-By: Claude" in body})
assert not [c for c in week if c["topic"] == "other"], [c for c in week if c["topic"] == "other"]

# ------------------------------------------------------------------ the whole session (times and counters only)
msgs, comps, human, wakeups, scheduled = {}, [], [], [], {}
with open(SESSION + ".jsonl", encoding="utf-8", errors="replace") as fh:
    for ln in fh:
        d = json.loads(ln)
        t = d.get("type")
        if "timestamp" not in d:
            continue
        ts = dt.datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00"))
        if t == "system" and d.get("subtype") == "compact_boundary":
            md = d.get("compactMetadata") or {}
            comps.append((ts, md.get("preTokens") or 0, md.get("postTokens") or 0))
        elif t == "assistant":
            m = d.get("message") or {}
            for p in m.get("content") or []:
                if isinstance(p, dict) and p.get("type") == "tool_use" and p.get("name") == "ScheduleWakeup":
                    scheduled[p.get("id")] = ts
            u = m.get("usage")
            if not u or m.get("model") == "<synthetic>" or not m.get("id"):
                continue
            ctx = (u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0)
            old = msgs.get(m["id"])
            if old is None or old[0] > ts:
                msgs[m["id"]] = (ts, ctx, max(u.get("output_tokens") or 0, old[2] if old else 0))
        elif t == "user":
            c = (d.get("message") or {}).get("content")
            parts = c if isinstance(c, list) else [{"type": "text", "text": c}] if isinstance(c, str) else []
            if any(isinstance(p, dict) and p.get("type") == "tool_result" for p in parts):
                continue
            text = " ".join(p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text").strip()
            if d.get("isMeta"):
                if text.startswith("# /loop"):
                    wakeups.append(ts)
            elif text.startswith("<pasted_content") or (text and not text.startswith("<") and not text.startswith("[")
                                                        and not text.startswith("This session is being continued") and not text.startswith("Skill /loop")):
                human.append(ts)

sub_requests = sub_out = sub_files = 0
for p in glob.glob(os.path.join(SESSION, "subagents", "*.jsonl")):
    seen = {}
    with open(p, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            if '"usage"' not in ln:
                continue
            d = json.loads(ln)
            m = d.get("message") or {}
            if d.get("type") == "assistant" and m.get("id") and m.get("usage"):
                seen[m["id"]] = max(seen.get(m["id"], 0), m["usage"].get("output_tokens") or 0)
    if seen:
        sub_files += 1
        sub_requests += len(seen)
        sub_out += sum(seen.values())

points = sorted(msgs.values())
start, end = points[0][0], points[-1][0]
hours = lambda ts: round((ts - start).total_seconds() / 3600, 3)
# keep the strip light: the context of every 3rd request plus every local maximum before a drop
pts = [[hours(t), round(v / 1000)] for t, v, _ in points]
thin = [p for i, p in enumerate(pts) if i % 3 == 0 or (i + 1 < len(pts) and pts[i + 1][1] < 0.5 * p[1])]
session = {
    "id": "1f9218ae", "start": start.astimezone(TZ).isoformat(), "end": end.astimezone(TZ).isoformat(),
    "points": thin,
    "compactions": [{"h": hours(t), "pre_k": round(a / 1000), "post_k": round(b / 1000)} for t, a, b in sorted(comps)],
    "human": [hours(t) for t in human],
    "wakeups": [hours(t) for t in wakeups],
    "commits": [{"h": hours(dt.datetime.fromisoformat(c["time"]).replace(tzinfo=TZ)), "topic": c["topic"]} for c in week],
    "totals": {
        "hours": round((end - start).total_seconds() / 3600, 1), "requests": len(points),
        "processed_tokens": sum(v for _, v, _ in points) + sum(o for _, _, o in points),
        "output_tokens": sum(o for _, _, o in points), "compactions": len(comps),
        "human_turns": len(human), "loop_firings": len(wakeups), "schedule_wakeup_calls": len(scheduled),
        "subagents": sub_files, "subagent_requests": sub_requests, "subagent_output_tokens": sub_out,
        "max_context_k": round(max(v for _, v, _ in points) / 1000),
    },
}

data = {
    "note": "epilogue data; pinned commits in scripts/collect_epilogue.py; the session section holds only times and counters",
    "passport": {"before": passport(PART1), "after": passport(NOW)},
    "week": week,
    "week_totals": dict(collections.Counter(c["topic"] for c in week)),
    "week_claude": sum(1 for c in week if c["claude"]),
    "session": session,
}
with open(OUT, "w") as f:
    json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    f.write("\n")
print(json.dumps({"passport": data["passport"], "week": len(week), "week_totals": data["week_totals"], "week_claude": data["week_claude"],
                  "session": session["totals"], "start": session["start"], "end": session["end"]}, ensure_ascii=False, indent=1))
