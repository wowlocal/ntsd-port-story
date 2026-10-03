#!/usr/bin/env python3
"""Token usage of the AI agents that built the port, from local session logs.

Usage:
    python3 scripts/collect_tokens.py [/path/to/ntsd-2.4]

Reads only token counters, model names and timestamps — no message content:
  * Codex: ~/.codex/sessions/**/*.jsonl whose session cwd lies inside the port
    repository; one `token_usage_record` per model response (deduplicated by
    response id, so forked subagent threads are not counted twice).
  * Claude Code: ~/.claude/projects/<port project>/**/*.jsonl; the `usage` of
    every assistant message (deduplicated by message id).

"Processed" tokens = every input token sent to the model (fresh, cache write and
cache read) plus output tokens. The Claude Code session that produced this deck
is reported separately and is not part of the port totals.
"""
import collections
import datetime as dt
import glob
import json
import os
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "ntsd-2.4"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "tokens.json")
HOME = os.path.expanduser("~")
CLAUDE_PROJECT = os.path.join(HOME, ".claude", "projects", REPO.replace("/", "-").replace(".", "-"))
DECK_SESSIONS = {"4f2b8068-785d-4bf1-89e2-9748dfa5a3eb"}  # the session that wrote this deck
SWITCH = dt.datetime(2026, 9, 27, 22, 0, tzinfo=dt.timezone.utc)  # commits moved from +03:00 to +02:00


def parse_ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def local_day(ts):
    off = 3 if ts < SWITCH else 2
    return (ts + dt.timedelta(hours=off)).date().isoformat()


def blank():
    return collections.Counter()


# ------------------------------------------------------------------ Codex
codex = {"responses": {}, "sessions": set(), "subagent_sessions": set()}
for path in glob.glob(os.path.join(HOME, ".codex", "sessions", "**", "*.jsonl"), recursive=True):
    with open(path, encoding="utf-8", errors="replace") as fh:
        first = fh.readline()
        try:
            meta = json.loads(first)
        except json.JSONDecodeError:
            continue
        p = meta.get("payload") or {}
        cwd = p.get("cwd") or ""
        if meta.get("type") != "session_meta" or not (cwd == REPO or cwd.startswith(REPO + "/") or cwd.startswith(REPO + "-")):
            continue
        sid = p.get("id")
        codex["sessions"].add(sid)
        if p.get("thread_source") == "subagent":
            codex["subagent_sessions"].add(sid)
        turn_model = {}
        for ln in fh:
            if '"turn_context"' not in ln and '"token_usage_record"' not in ln:
                continue
            d = json.loads(ln)
            if d.get("type") == "turn_context":
                tp = d["payload"]
                turn_model[tp.get("turn_id")] = (tp.get("model"), tp.get("effort"))
            elif d.get("type") == "token_usage_record":
                tp = d["payload"]
                rid = tp.get("response_id")
                if not rid or rid in codex["responses"]:
                    continue
                u = tp.get("usage") or {}
                model, effort = turn_model.get(tp.get("turn_id"), (None, None))
                codex["responses"][rid] = {
                    "ts": parse_ts(d["timestamp"]),
                    "model": model or "unknown",
                    "effort": effort,
                    "input": u.get("input_tokens", 0),           # includes cached
                    "cached": u.get("cached_input_tokens", 0),
                    "output": u.get("output_tokens", 0),         # includes reasoning
                    "reasoning": u.get("reasoning_output_tokens", 0),
                    "subagent": sid in codex["subagent_sessions"],
                }

# ------------------------------------------------------------------ Claude Code
claude = {"messages": {}, "deck": {}, "sessions": set(), "subagent_files": 0}
for path in glob.glob(os.path.join(CLAUDE_PROJECT, "**", "*.jsonl"), recursive=True):
    rel = os.path.relpath(path, CLAUDE_PROJECT)
    session = rel.split(os.sep)[0].replace(".jsonl", "")
    is_sub = os.sep + "subagents" + os.sep in os.sep + rel
    target = claude["deck"] if session in DECK_SESSIONS else claude["messages"]
    if session not in DECK_SESSIONS:
        claude["sessions"].add(session)
        claude["subagent_files"] += 1 if is_sub else 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            if '"usage"' not in ln:
                continue
            try:
                d = json.loads(ln)
            except json.JSONDecodeError:
                continue
            m = d.get("message") or {}
            u = m.get("usage")
            if d.get("type") != "assistant" or not u or not m.get("id"):
                continue
            mid = m["id"]
            rec = {
                "ts": parse_ts(d["timestamp"]),
                "model": m.get("model") or "unknown",
                "input": u.get("input_tokens", 0) or 0,
                "cache_write": u.get("cache_creation_input_tokens", 0) or 0,
                "cache_read": u.get("cache_read_input_tokens", 0) or 0,
                "output": u.get("output_tokens", 0) or 0,
                "subagent": is_sub,
            }
            old = target.get(mid)
            if old is None or rec["output"] > old["output"]:
                if old is not None:
                    rec["ts"] = min(rec["ts"], old["ts"])
                target[mid] = rec


# ------------------------------------------------------------------ aggregate
def codex_totals(rows):
    t = blank()
    for r in rows:
        t["responses"] += 1
        t["input"] += r["input"]
        t["cached"] += r["cached"]
        t["fresh_input"] += r["input"] - r["cached"]
        t["output"] += r["output"]
        t["reasoning"] += r["reasoning"]
        t["processed"] += r["input"] + r["output"]
        t["max_context"] = max(t["max_context"], r["input"])
    return dict(t)


def claude_totals(rows):
    t = blank()
    for r in rows:
        t["responses"] += 1
        t["fresh_input"] += r["input"]
        t["cache_write"] += r["cache_write"]
        t["cache_read"] += r["cache_read"]
        t["input"] += r["input"] + r["cache_write"] + r["cache_read"]
        t["output"] += r["output"]
        t["processed"] += r["input"] + r["cache_write"] + r["cache_read"] + r["output"]
        t["max_context"] = max(t["max_context"], r["input"] + r["cache_write"] + r["cache_read"])
    return dict(t)


crows = list(codex["responses"].values())
arows = [r for r in claude["messages"].values() if r["model"] != "<synthetic>"]
drows = [r for r in claude["deck"].values() if r["model"] != "<synthetic>"]

by_model = collections.defaultdict(blank)
for r in crows:
    key = f"codex · {r['model']}"
    by_model[key]["responses"] += 1
    by_model[key]["processed"] += r["input"] + r["output"]
    by_model[key]["output"] += r["output"]
for r in arows:
    key = f"claude · {r['model']}"
    by_model[key]["responses"] += 1
    by_model[key]["processed"] += r["input"] + r["cache_write"] + r["cache_read"] + r["output"]
    by_model[key]["output"] += r["output"]

daily = collections.defaultdict(blank)
for r in crows:
    day = local_day(r["ts"])
    daily[day]["codex"] += r["input"] + r["output"]
    daily[day]["codex_output"] += r["output"]
for r in arows:
    day = local_day(r["ts"])
    daily[day]["claude"] += r["input"] + r["cache_write"] + r["cache_read"] + r["output"]
    daily[day]["claude_output"] += r["output"]

days = sorted(daily)
cal = []
if days:
    d0, d1 = dt.date.fromisoformat(days[0]), dt.date.fromisoformat(days[-1])
    while d0 <= d1:
        k = d0.isoformat()
        cal.append({"date": k, **{f: daily[k].get(f, 0) for f in ("codex", "claude", "codex_output", "claude_output")}})
        d0 += dt.timedelta(days=1)

out = {
    "note": "processed = all input tokens sent (fresh + cache write + cache read) + output tokens; Codex input includes cached tokens and output includes reasoning",
    "codex": {
        **codex_totals(crows),
        "sessions": len(codex["sessions"]),
        "subagent_sessions": len(codex["subagent_sessions"]),
        "subagent_processed": sum(r["input"] + r["output"] for r in crows if r["subagent"]),
        "first": min(r["ts"] for r in crows).isoformat() if crows else None,
        "last": max(r["ts"] for r in crows).isoformat() if crows else None,
        "efforts": dict(collections.Counter(r["effort"] for r in crows)),
    },
    "claude": {
        **claude_totals(arows),
        "sessions": len(claude["sessions"]),
        "subagent_files": claude["subagent_files"],
        "subagent_processed": sum(r["input"] + r["cache_write"] + r["cache_read"] + r["output"] for r in arows if r["subagent"]),
        "first": min(r["ts"] for r in arows).isoformat() if arows else None,
        "last": max(r["ts"] for r in arows).isoformat() if arows else None,
    },
    "deck_session": {**claude_totals(drows), "note": "the Claude Code session that analysed the history and wrote this deck (counted until the data was collected)"},
    "by_model": {k: dict(v) for k, v in sorted(by_model.items(), key=lambda kv: -kv[1]["processed"])},
    "daily": cal,
}
with open(OUT, "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(json.dumps({k: v for k, v in out.items() if k != "daily"}, ensure_ascii=False, indent=1))
