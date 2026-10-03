#!/usr/bin/env python3
"""Context size of every model request in two agent sessions, for the "breathing" chart.

Usage:
    python3 scripts/collect_context.py [/path/to/ntsd-2.4]

Writes data/context.json with only times and token counts:
  * Claude Code, the port session 7ea5b99f (28 Sep – 3 Oct): input + cache
    write + cache read of each main-thread request, and every compaction.
  * Codex, the first port session 01a07b63 (7 – 9 Sep, the overnight sprint):
    input tokens of each response (cached included) and every compaction.
"""
import datetime as dt
import glob
import json
import os
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "ntsd-2.4"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "context.json")
HOME = os.path.expanduser("~")
CLAUDE_FILE = os.path.join(HOME, ".claude", "projects", REPO.replace("/", "-").replace(".", "-"), "7ea5b99f-68d1-4a00-8aa2-0da4bd065e97.jsonl")
CODEX_SESSION = "01a07b63"


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def pack(points, compactions, start, window, tz):
    pts = sorted(points)
    return {
        "start": start.isoformat(), "utc_offset_hours": tz, "window_k": window,
        "points": [[round((t - start).total_seconds() / 60, 1), round(v / 1000, 1)] for t, v in pts],
        "compactions": [{"t": round((t - start).total_seconds() / 60, 1), **({"pre_k": round(a / 1000, 1), "post_k": round(b / 1000, 1)} if a else {})}
                        for t, a, b in sorted(compactions)],
        "requests": len(pts),
        "max_k": round(max(v for _, v in pts) / 1000, 1),
        "median_k": round(sorted(v for _, v in pts)[len(pts) // 2] / 1000, 1),
    }


# ---------------------------------------------------------------- Claude
msgs, comps = {}, []
with open(CLAUDE_FILE, encoding="utf-8", errors="replace") as fh:
    for ln in fh:
        if '"usage"' not in ln and '"compact_boundary"' not in ln:
            continue
        d = json.loads(ln)
        if d.get("type") == "system" and d.get("subtype") == "compact_boundary":
            md = d.get("compactMetadata") or {}
            comps.append((ts(d["timestamp"]), md.get("preTokens") or 0, md.get("postTokens") or 0))
        elif d.get("type") == "assistant":
            m = d.get("message") or {}
            u = m.get("usage")
            if not u or m.get("model") == "<synthetic>" or not m.get("id"):
                continue
            ctx = (u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0)
            t = ts(d["timestamp"])
            if m["id"] not in msgs or msgs[m["id"]][0] > t:
                msgs[m["id"]] = (t, ctx)
cpoints = list(msgs.values())
claude = pack(cpoints, comps, min(t for t, _ in cpoints), 1000, 2)

# ---------------------------------------------------------------- Codex
path = next(p for p in glob.glob(os.path.join(HOME, ".codex", "sessions", "**", f"*{CODEX_SESSION}*.jsonl"), recursive=True))
seen, xpoints, xcomps, window = set(), [], [], None
with open(path, encoding="utf-8", errors="replace") as fh:
    for ln in fh:
        if '"token_usage_record"' not in ln and '"compacted"' not in ln and '"model_context_window"' not in ln:
            continue
        d = json.loads(ln)
        p = d.get("payload") or {}
        if d.get("type") == "token_usage_record":
            rid = p.get("response_id")
            if rid and rid not in seen:
                seen.add(rid)
                xpoints.append((ts(d["timestamp"]), (p.get("usage") or {}).get("input_tokens") or 0))
        elif d.get("type") == "compacted":
            xcomps.append((ts(d["timestamp"]), 0, 0))
        elif isinstance(p, dict) and p.get("type") == "task_started" and p.get("model_context_window"):
            window = p["model_context_window"]
codex = pack(xpoints, xcomps, min(t for t, _ in xpoints), round((window or 258400) / 1000, 1), 3)

with open(OUT, "w") as f:
    json.dump({"claude": claude, "codex": codex}, f, separators=(",", ":"))
    f.write("\n")
for k, v in (("claude", claude), ("codex", codex)):
    print(k, v["start"], v["requests"], "requests", len(v["compactions"]), "compactions", "max", v["max_k"], "median", v["median_k"], "window", v["window_k"])
