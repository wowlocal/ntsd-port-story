#!/usr/bin/env python3
"""What the Claude Code work would have cost at API prices, per day, against the subscription.

Usage:
    python3 scripts/collect_claude_burn.py [/path/to/ntsd-2.4]

Claude Code keeps no rate-limit utilisation locally (unlike Codex, see collect_limits.py),
so the subscription burn is shown as an API equivalent: the `usage` of every assistant
message in the port's Claude Code transcripts, deduplicated by message id exactly as
collect_tokens.py does, priced at Anthropic's published per-token list prices. Cache
writes are split by TTL (5-minute and 1-hour) as the transcripts record them. Synthetic
messages whose text mentions a usage or rate limit are counted as limit notices.
The session that wrote this deck is reported separately. Writes data/claude_burn.json;
only numbers and timestamps are kept.
"""
import collections
import datetime as dt
import glob
import json
import os
import re
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "ntsd-2.4"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "claude_burn.json")
PROJECT = os.path.join(os.path.expanduser("~"), ".claude", "projects", REPO.replace("/", "-").replace(".", "-"))
DECK_SESSIONS = {"4f2b8068-785d-4bf1-89e2-9748dfa5a3eb"}  # the session that wrote this deck
SWITCH = dt.datetime(2026, 9, 27, 22, 0, tzinfo=dt.timezone.utc)  # commits moved from +03:00 to +02:00

# The account ran on Claude Max 20x: $200 a month for web subscriptions
# (support.claude.com/en/articles/11049741-what-is-the-max-plan). One subscription week and
# day follow collect_limits.py: $/month × 12 / 52, then / 7.
PLAN = {"name": "Claude Max 20x", "price_usd_month": 200,
        "source": "https://support.claude.com/en/articles/11049741-what-is-the-max-plan"}
WEEK_USD = PLAN["price_usd_month"] * 12 / 52
DAY_USD = WEEK_USD / 7
# USD per million tokens: input, 5-minute cache write, 1-hour cache write, cache read, output
# (platform.claude.com/docs/en/about-claude/pricing, checked 2026-10-03; thinking is billed as output).
PRICES = {"claude-opus-5-5": (4.00, 5.00, 8.00, 0.20, 20.00), "claude-haiku-4-5": (1.00, 1.25, 2.00, 0.10, 5.00)}
PRICE_SOURCE = "https://platform.claude.com/docs/en/about-claude/pricing"
LIMIT_TEXT = re.compile(r"usage limit|limit reached|rate.?limit|weekly limit|\b429\b", re.I)


def parse_ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def local(ts):
    return ts + dt.timedelta(hours=3 if ts < SWITCH else 2)


messages = {"port": {}, "deck": {}}
notices = []
for path in glob.glob(os.path.join(PROJECT, "**", "*.jsonl"), recursive=True):
    session = os.path.relpath(path, PROJECT).split(os.sep)[0].replace(".jsonl", "")
    target = messages["deck"] if session in DECK_SESSIONS else messages["port"]
    with open(path, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            if '"usage"' not in ln and '"<synthetic>"' not in ln:
                continue
            try:
                d = json.loads(ln)
            except json.JSONDecodeError:
                continue
            m = d.get("message") or {}
            if d.get("type") != "assistant":
                continue
            if m.get("model") == "<synthetic>":
                text = " ".join(c.get("text", "") for c in m.get("content") or [] if isinstance(c, dict))
                if LIMIT_TEXT.search(text):
                    notices.append(d.get("timestamp"))
                continue
            u = m.get("usage")
            if not u or not m.get("id"):
                continue
            cw = u.get("cache_creation_input_tokens", 0) or 0
            cw1 = (u.get("cache_creation") or {}).get("ephemeral_1h_input_tokens", 0) or 0
            rec = {"ts": parse_ts(d["timestamp"]), "model": re.sub(r"-\d{8}$", "", m.get("model") or ""),
                   "input": u.get("input_tokens", 0) or 0, "cw5": cw - cw1, "cw1": cw1,
                   "cache_read": u.get("cache_read_input_tokens", 0) or 0, "output": u.get("output_tokens", 0) or 0,
                   "speed": u.get("speed") or "standard"}
            old = target.get(m["id"])
            if old is None or rec["output"] > old["output"]:
                if old is not None:
                    rec["ts"] = min(rec["ts"], old["ts"])
                target[m["id"]] = rec


def cost(r):
    p = PRICES.get(r["model"])
    if p is None:
        return None
    return {"input": r["input"] * p[0] / 1e6, "cache_write": (r["cw5"] * p[1] + r["cw1"] * p[2]) / 1e6,
            "cache_read": r["cache_read"] * p[3] / 1e6, "output": r["output"] * p[4] / 1e6}


days = collections.defaultdict(lambda: {"port": 0.0, "deck": 0.0, "port_responses": 0, "hours": set()})
parts = collections.Counter()
tokens = collections.Counter()
unpriced = collections.Counter()
speeds = collections.Counter()
for scope, rows in messages.items():
    for r in rows.values():
        c = cost(r)
        if c is None:
            unpriced[r["model"]] += 1
            continue
        speeds[r["speed"]] += 1
        day = local(r["ts"]).date().isoformat()
        days[day][scope] += sum(c.values())
        if scope == "port":
            days[day]["port_responses"] += 1
            days[day]["hours"].add(local(r["ts"]).hour)
            parts.update(c)
            tokens.update({k: r[k] for k in ("input", "cw5", "cw1", "cache_read", "output")})

port_total = sum(v["port"] for v in days.values())
deck_total = sum(v["deck"] for v in days.values())
port_days = [d for d, v in days.items() if v["port_responses"]]
span = (dt.date.fromisoformat(max(port_days)) - dt.date.fromisoformat(min(port_days))).days + 1
inputs = tokens["input"] + tokens["cw5"] + tokens["cw1"] + tokens["cache_read"]
out = {
    "collected_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
    "plan": {**PLAN, "price_usd_week": round(WEEK_USD, 2), "price_usd_day": round(DAY_USD, 2)},
    "prices_usd_per_mtok": {m: dict(zip(("input", "cache_write_5m", "cache_write_1h", "cache_read", "output"), p))
                            for m, p in PRICES.items()},
    "price_source": PRICE_SOURCE,
    "days": {d: {"port_usd": round(v["port"], 2), "deck_usd": round(v["deck"], 2), "port_responses": v["port_responses"],
                 "active_hours": len(v["hours"]), "x_subscription": round(v["port"] / DAY_USD, 1)}
             for d, v in sorted(days.items())},
    "totals": {
        "port_usd": round(port_total, 2), "deck_usd": round(deck_total, 2), "days": span,
        "subscription_usd": round(DAY_USD * span, 2), "x_subscription": round(port_total / (DAY_USD * span), 1),
        "weeks_of_subscription": round(port_total / WEEK_USD, 1),
        "months_of_subscription": round(port_total / PLAN["price_usd_month"], 1),
        "port_responses": sum(v["port_responses"] for v in days.values()),
        "cost_share": {k: round(v / port_total, 3) for k, v in parts.items()},
        "input_from_cache": round(tokens["cache_read"] / inputs, 3) if inputs else None,
        "output_tokens": tokens["output"],
    },
    "limit_notices": sorted(n for n in notices if n),
    "checks": {"unpriced_models": dict(unpriced), "speed": dict(speeds)},
}
with open(OUT, "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(json.dumps(out["totals"], ensure_ascii=False))
for d, v in out["days"].items():
    print(d, v)
print("limit notices:", len(out["limit_notices"]), out["checks"])
