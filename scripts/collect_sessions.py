#!/usr/bin/env python3
"""Session statistics of the agents that built the port, from local session logs.

Usage:
    python3 scripts/collect_sessions.py [/path/to/ntsd-2.4]

Writes data/sessions.json with aggregate numbers only: models and reasoning
effort, turns and their duration, autopilot continuations (/goal, /loop) versus
human messages, context compactions, tool calls by kind, shell commands by
program, weekly rate-limit usage and a per-session timeline. Message text is
read only to classify it (autopilot / injected / human) and is never written.
"""
import collections
import datetime as dt
import glob
import hashlib
import json
import os
import re
import shlex
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "ntsd-2.4"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "sessions.json")
HOME = os.path.expanduser("~")
CLAUDE_PROJECT = os.path.join(HOME, ".claude", "projects", REPO.replace("/", "-").replace(".", "-"))
DECK_SESSIONS = {"4f2b8068-785d-4bf1-89e2-9748dfa5a3eb"}


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def iso(t):
    return t.isoformat().replace("+00:00", "Z") if t else None


CMD_RE = re.compile(r'cmd\s*:\s*"((?:[^"\\]|\\.)*)"')
ENV_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def program(cmd):
    """First real program of a shell command line: skips cd/env/timeout prefixes."""
    cmd = cmd.strip()
    for part in re.split(r"\s*(?:&&|\|\||;|\n)\s*", cmd):
        part = part.strip()
        if not part or part.startswith("#"):
            continue
        try:
            words = shlex.split(part, posix=True)
        except ValueError:
            words = part.split()
        while words and (ENV_RE.match(words[0]) or words[0] in ("env", "time", "timeout", "nice", "caffeinate", "command", "exec", "sudo")):
            words = words[1:]
            if words and re.fullmatch(r"-?\d+[smh]?", words[0] or ""):
                words = words[1:]
        if not words:
            continue
        w = os.path.basename(words[0])
        if w in ("cd", "pushd", "set", "export", "source", ".", "true", "echo", "printf", "sleep"):
            if w == "sleep":
                return "sleep"
            continue
        if w in ("python", "python3", "uv") and len(words) > 1:
            tgt = next((x for x in words[1:] if x.endswith(".py")), None)
            if tgt:
                base = os.path.basename(tgt)
                if base.startswith("oracle_"):
                    return "python3 tools/oracle_*"
                if base.startswith(("verify_", "accept_", "finalize_", "prepare_", "run_")):
                    return "python3 tools/" + base.split("_")[0] + "_*"
                return "python3 (other script)"
            return "python3 -c / modules"
        if w == "swift" and len(words) > 1:
            return "swift " + words[1]
        if w == "git" and len(words) > 1:
            sub = next((x for x in words[1:] if not x.startswith("-") and "=" not in x), "")
            return "git " + sub if sub in ("commit", "push", "status", "diff", "log", "show", "add", "rev-parse", "worktree", "lfs", "apply", "stash", "fetch", "rebase") else "git (other)"
        return w
    return "(shell builtins only)"


# ================================================================== Codex
cx = {
    "sessions": {}, "turns": {}, "responses": {}, "tool_calls": {}, "commands": collections.Counter(),
    "user_msgs": {}, "compactions": set(), "goals": {}, "aborted": set(), "rate": {},
    "policies": collections.Counter(),
}
for path in glob.glob(os.path.join(HOME, ".codex", "sessions", "**", "*.jsonl"), recursive=True):
    with open(path, encoding="utf-8", errors="replace") as fh:
        try:
            meta = json.loads(fh.readline())
        except json.JSONDecodeError:
            continue
        p = meta.get("payload") or {}
        cwd = p.get("cwd") or ""
        if meta.get("type") != "session_meta" or not (cwd == REPO or cwd.startswith(REPO + "/") or cwd.startswith(REPO + "-")):
            continue
        sid = p.get("id")
        sess = cx["sessions"].setdefault(sid, {
            "id": sid[:8], "start": ts(p["timestamp"]), "end": ts(p["timestamp"]),
            "subagent": p.get("thread_source") == "subagent", "models": collections.Counter(),
            "efforts": collections.Counter(), "responses": 0, "turns": 0, "goal_msgs": 0, "human_msgs": 0, "compactions": 0,
        })
        turn_model = {}
        for ln in fh:
            try:
                d = json.loads(ln)
            except json.JSONDecodeError:
                continue
            t = d.get("type")
            q = d.get("payload") or {}
            qt = q.get("type") if isinstance(q, dict) else None
            when = ts(d["timestamp"]) if d.get("timestamp") else None
            if when and when > sess["end"]:
                sess["end"] = when
            if t == "turn_context":
                turn_model[q.get("turn_id")] = (q.get("model") or "unknown", q.get("effort") or "default")
                sb = q.get("sandbox_policy")
                sb = sb.get("type") if isinstance(sb, dict) else sb
                cx["policies"][(q.get("approval_policy"), sb)] += 1
            elif t == "token_usage_record":
                rid = q.get("response_id")
                if rid and rid not in cx["responses"]:
                    model, effort = turn_model.get(q.get("turn_id"), ("unknown", "default"))
                    cx["responses"][rid] = (model, effort, when)
                    sess["responses"] += 1
                    sess["models"][model] += 1
                    sess["efforts"][effort] += 1
            elif t == "event_msg" and qt == "task_started":
                tid = q.get("turn_id")
                if tid not in cx["turns"]:
                    cx["turns"][tid] = {"start": when, "end": None, "session": sid}
                    sess["turns"] += 1
            elif t == "event_msg" and qt in ("task_complete", "turn_aborted"):
                tid = q.get("turn_id")
                if tid in cx["turns"] and cx["turns"][tid]["end"] is None:
                    cx["turns"][tid]["end"] = when
                if qt == "turn_aborted":
                    cx["aborted"].add(tid)
            elif t == "event_msg" and qt == "thread_goal_updated":
                g = q.get("goal") or {}
                key = (g.get("threadId"), g.get("createdAt"))
                old = cx["goals"].get(key)
                if old is None or (g.get("timeUsedSeconds") or 0) >= (old.get("timeUsedSeconds") or 0):
                    cx["goals"][key] = {"timeUsedSeconds": g.get("timeUsedSeconds") or 0, "tokensUsed": g.get("tokensUsed") or 0, "status": g.get("status")}
            elif t == "compacted":
                key = d.get("timestamp")
                if key not in cx["compactions"]:
                    cx["compactions"].add(key)
                    sess["compactions"] += 1
            elif t == "response_item" and qt in ("function_call", "custom_tool_call"):
                cid = q.get("call_id") or q.get("id")
                if cid in cx["tool_calls"]:
                    continue
                cx["tool_calls"][cid] = q.get("name")
                if q.get("name") == "exec":
                    body = q.get("input") or q.get("arguments") or ""
                    for m in CMD_RE.finditer(body):
                        try:
                            cmd = json.loads('"' + m.group(1) + '"')
                        except json.JSONDecodeError:
                            cmd = m.group(1)
                        cx["commands"][program(cmd)] += 1
            elif t == "response_item" and qt == "message" and q.get("role") == "user":
                text = "".join(c.get("text", "") for c in q.get("content") or [] if isinstance(c, dict)).strip()
                key = (d.get("timestamp"), hashlib.sha1(text.encode()).hexdigest())
                if key in cx["user_msgs"]:
                    continue
                if text.startswith('<codex_internal_context source="goal">'):
                    kind = "goal"
                elif text.startswith(("# AGENTS.md instructions", "<environment_context>", "<recommended_plugins>", "<send_user_message_question_reply>", "<codex_internal_context")):
                    kind = "injected"
                else:
                    kind = "human"
                cx["user_msgs"][key] = kind
                if kind == "goal":
                    sess["goal_msgs"] += 1
                elif kind == "human":
                    sess["human_msgs"] += 1
            elif t == "event_msg" and qt == "token_count":
                pr = ((q.get("rate_limits") or {}).get("primary")) or {}
                if pr.get("used_percent") is not None and when:
                    day = (when + dt.timedelta(hours=3)).date().isoformat()
                    cur = cx["rate"].get(day)
                    if cur is None or pr["used_percent"] > cur["used"]:
                        cx["rate"][day] = {"used": pr["used_percent"], "resets": iso(dt.datetime.fromtimestamp(pr.get("resets_at") or 0, dt.timezone.utc))}

# ================================================================== Claude Code
cl = {
    "messages": {}, "tools": {}, "commands": collections.Counter(), "turn_ms": [], "compactions": [],
    "loop_iterations": 0, "wakeups": 0, "human": set(), "refusals": 0, "sessions": {}, "subagent_files": 0,
    "effort_cmds": [], "model_cmds": 0,
}
for path in glob.glob(os.path.join(CLAUDE_PROJECT, "**", "*.jsonl"), recursive=True):
    rel = os.path.relpath(path, CLAUDE_PROJECT)
    session = rel.split(os.sep)[0].replace(".jsonl", "")
    if session in DECK_SESSIONS:
        continue
    is_sub = os.sep + "subagents" + os.sep in os.sep + rel
    cl["subagent_files"] += 1 if is_sub else 0
    s = cl["sessions"].setdefault(session, {"id": session[:8], "start": None, "end": None, "responses": 0, "subagent_files": 0})
    s["subagent_files"] += 1 if is_sub else 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            try:
                d = json.loads(ln)
            except json.JSONDecodeError:
                continue
            t = d.get("type")
            when = ts(d["timestamp"]) if d.get("timestamp") else None
            if when and not is_sub:
                s["start"] = min(s["start"], when) if s["start"] else when
                s["end"] = max(s["end"], when) if s["end"] else when
            if t == "assistant":
                m = d.get("message") or {}
                mid = m.get("id")
                if mid and mid not in cl["messages"]:
                    cl["messages"][mid] = (m.get("model"), is_sub)
                    if m.get("model") != "<synthetic>":
                        s["responses"] += 1
                if m.get("stop_reason") == "refusal" and mid:
                    cl["refusals"] += 1
                for c in m.get("content") or []:
                    if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("id") not in cl["tools"]:
                        cl["tools"][c.get("id")] = c.get("name")
                        if c.get("name") == "Bash":
                            cl["commands"][program((c.get("input") or {}).get("command") or "")] += 1
            elif t == "system":
                st = d.get("subtype")
                if st == "turn_duration" and not is_sub:
                    cl["turn_ms"].append(d.get("durationMs") or 0)
                elif st == "compact_boundary":
                    md = d.get("compactMetadata") or {}
                    cl["compactions"].append({"pre": md.get("preTokens"), "post": md.get("postTokens"), "trigger": md.get("trigger")})
                elif st == "scheduled_task_fire":
                    cl["wakeups"] += 1
            elif t == "user" and not is_sub and not d.get("isMeta"):
                c = (d.get("message") or {}).get("content")
                text = c if isinstance(c, str) else " ".join(x.get("text", "") for x in c or [] if isinstance(x, dict) and x.get("type") == "text")
                text = text.strip()
                if not text:
                    continue
                if text.startswith("<command-message>loop</command-message>"):
                    cl["loop_iterations"] += 1
                elif text.startswith("<command-name>/effort</command-name>"):
                    cl["effort_cmds"].append(iso(when))
                elif text.startswith("<command-name>/model</command-name>"):
                    cl["model_cmds"] += 1
                elif text.startswith("<local-command-stdout>Set effort level to"):
                    cl["effort_cmds"].append(re.sub(r"\x1b\[[0-9;]*m", "", text)[len("<local-command-stdout>"):].split("<")[0].strip())
                elif text.startswith(("<", "This session is being continued", "Base directory for this skill", "# /loop", "[Image", "[Request interrupted", "Your response above was stopped", "You are an independent")):
                    continue
                else:
                    cl["human"].add((d.get("timestamp"), hashlib.sha1(text.encode()).hexdigest()))


# ================================================================== aggregate
def hours(seconds):
    return round(seconds / 3600, 1)


cx_turn_secs = [(v["end"] - v["start"]).total_seconds() for v in cx["turns"].values() if v["start"] and v["end"]]
models = collections.Counter()
efforts = collections.defaultdict(collections.Counter)
for model, effort, _ in cx["responses"].values():
    models[model] += 1
    efforts[model][effort] += 1
kinds = collections.Counter(cx["user_msgs"].values())
tool_kinds = collections.Counter(cx["tool_calls"].values())
goal_secs = sum(g["timeUsedSeconds"] for g in cx["goals"].values())

cl_models = collections.Counter(m for m, _ in cl["messages"].values() if m != "<synthetic>")
cl_tools = collections.Counter(cl["tools"].values())


def session_rows():
    rows = []
    for v in cx["sessions"].values():
        if v["responses"] == 0:
            continue
        top_model = v["models"].most_common(1)[0][0]
        top_effort = v["efforts"].most_common(1)[0][0]
        rows.append({"agent": "codex", "id": v["id"], "start": iso(v["start"]), "end": iso(v["end"]),
                     "subagent": v["subagent"], "model": top_model, "effort": top_effort,
                     "responses": v["responses"], "turns": v["turns"], "goal_msgs": v["goal_msgs"],
                     "human_msgs": v["human_msgs"], "compactions": v["compactions"]})
    for v in cl["sessions"].values():
        if not v["start"] or v["responses"] == 0:
            continue
        rows.append({"agent": "claude", "id": v["id"], "start": iso(v["start"]), "end": iso(v["end"]),
                     "subagent": False, "model": "claude-opus-5-5", "effort": "xhigh",
                     "responses": v["responses"], "subagent_files": v["subagent_files"]})
    return sorted(rows, key=lambda r: r["start"])


out = {
    "note": "aggregates from local session logs; message text was only classified, never stored",
    "codex": {
        "sessions": sum(1 for v in cx["sessions"].values() if v["responses"]),
        "subagent_sessions": sum(1 for v in cx["sessions"].values() if v["responses"] and v["subagent"]),
        "responses": len(cx["responses"]),
        "models": dict(models.most_common()),
        "efforts_by_model": {m: dict(e.most_common()) for m, e in efforts.items()},
        "policies": [{"approval": a, "sandbox": b, "turn_contexts": n} for (a, b), n in cx["policies"].most_common()],
        "turns": len(cx["turns"]),
        "turns_aborted": len(cx["aborted"]),
        "turn_hours_total": hours(sum(cx_turn_secs)),
        "turn_minutes_median": round(sorted(cx_turn_secs)[len(cx_turn_secs) // 2] / 60, 1) if cx_turn_secs else None,
        "turn_hours_longest": hours(max(cx_turn_secs)) if cx_turn_secs else None,
        "goal_runs": len(cx["goals"]),
        "goal_hours": hours(goal_secs),
        "user_messages": dict(kinds),
        "compactions": len(cx["compactions"]),
        "tool_calls": dict(tool_kinds.most_common()),
        "shell_commands": sum(cx["commands"].values()),
        "shell_programs": dict(cx["commands"].most_common(25)),
        "weekly_limit_by_day": dict(sorted(cx["rate"].items())),
    },
    "claude": {
        "sessions": sum(1 for v in cl["sessions"].values() if v["responses"]),
        "subagent_files": cl["subagent_files"],
        "responses": sum(cl_models.values()),
        "models": dict(cl_models.most_common()),
        "effort_commands": cl["effort_cmds"],
        "turns": len(cl["turn_ms"]),
        "turn_hours_total": hours(sum(cl["turn_ms"]) / 1000),
        "turn_minutes_median": round(sorted(cl["turn_ms"])[len(cl["turn_ms"]) // 2] / 60000, 1) if cl["turn_ms"] else None,
        "turn_hours_longest": hours(max(cl["turn_ms"]) / 1000) if cl["turn_ms"] else None,
        "loop_iterations": cl["loop_iterations"],
        "scheduled_wakeups": cl["wakeups"],
        "human_messages": len(cl["human"]),
        "compactions": len(cl["compactions"]),
        "compaction_detail": cl["compactions"],
        "refusals": cl["refusals"],
        "tool_calls": dict(cl_tools.most_common()),
        "shell_commands": sum(cl["commands"].values()),
        "shell_programs": dict(cl["commands"].most_common(25)),
    },
    "sessions": session_rows(),
}
with open(OUT, "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(json.dumps({k: v for k, v in out.items() if k != "sessions"}, ensure_ascii=False, indent=1)[:9000])
print("sessions rows:", len(out["sessions"]))
