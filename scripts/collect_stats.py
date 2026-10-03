#!/usr/bin/env python3
"""Regenerate the deck's data/*.json from the NTSD port repository.

Usage:
    python3 scripts/collect_stats.py ../ntsd-2.4

Everything is read with plain `git` commands; nothing in the source repository
is modified. Times are the commit's own local time as recorded by git.
"""
import collections
import datetime as dt
import json
import os
import re
import subprocess
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../ntsd-2.4")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
SINCE = "2026-09-01"
# First commit carrying "Co-Authored-By: Claude"; before it every commit has no AI trailer.
TURN_DAY = "2026-09-28"


def git(*args):
    res = subprocess.run(["git", "-C", REPO, *args], check=True, capture_output=True)
    return res.stdout.decode("utf-8", "replace")


def dump(name, obj):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def area_of(path):
    for prefix, name in (("native/Tests/", "native-tests"), ("native/", "native-src"),
                         ("tools/", "tools"), ("docs/research/", "research"),
                         ("docs/evidence/", "evidence"), ("docs/", "docs"),
                         ("downloads/", "downloads"), ("build/", "build")):
        if path.startswith(prefix):
            return name
    return "root"


# ------------------------------------------------------------------ commits
RS, US = "\x1e", "\x1f"
raw = git("log", "--reverse", "--numstat", "--date=format:%Y-%m-%dT%H:%M:%S%z",
          f"--format={RS}%h{US}%ad{US}%s{US}%b{US}")
commits = []
for chunk in raw.split(RS)[1:]:
    short, date, subject, body, stats = chunk.split(US)
    ins = dele = files = 0
    native_src = False
    areas = collections.Counter()
    for ln in stats.strip().split("\n"):
        m = re.match(r"^(\d+|-)\t(\d+|-)\t(.*)$", ln)
        if not m:
            continue
        files += 1
        if m.group(1) == "-":
            continue
        a, d = int(m.group(1)), int(m.group(2))
        path = re.sub(r"\{[^}]*=> ([^}]*)\}", r"\1", m.group(3))
        native_src = native_src or path.startswith("native/Sources/")
        ins += a
        dele += d
        areas[area_of(path)] += a
    claude = "Co-Authored-By: Claude" in body
    commits.append({"hash": short, "date": date, "subject": subject, "body": body.strip(),
                    "claude": claude, "ins": ins, "del": dele, "files": files, "areas": areas,
                    "native_src": native_src})

recent = [c for c in commits if c["date"][:10] >= SINCE]
prologue = [c for c in commits if c["date"][:10] < SINCE]
for c in recent:
    if c["claude"]:
        c["era"] = "claude"
    elif c["date"][:10] < TURN_DAY:
        c["era"] = "pre"
    else:
        c["era"] = "parallel"


def parse(c):
    return dt.datetime.strptime(c["date"], "%Y-%m-%dT%H:%M:%S%z")


# ------------------------------------------------------------------ daily calendar (gaps included)
by_day = collections.OrderedDict()
for c in recent:
    e = by_day.setdefault(c["date"][:10], {"pre": 0, "claude": 0, "parallel": 0, "ins": 0, "native": 0})
    e[c["era"]] += 1
    e["ins"] += c["ins"]
    e["native"] += 1 if c["native_src"] else 0
day = dt.date.fromisoformat(min(by_day))
end = dt.date.fromisoformat(max(by_day))
daily = []
while day <= end:
    e = by_day.get(day.isoformat(), {"pre": 0, "claude": 0, "parallel": 0, "ins": 0, "native": 0})
    daily.append({"date": day.isoformat(), **e, "commits": e["pre"] + e["claude"] + e["parallel"]})
    day += dt.timedelta(days=1)
dump("daily.json", daily)

# ------------------------------------------------------------------ rhythm: day x hour
cells = collections.Counter((c["date"][:10], int(c["date"][11:13])) for c in recent)
hours = collections.Counter(int(c["date"][11:13]) for c in recent)
dump("rhythm.json", {
    "days": [d["date"] for d in daily],
    "cells": [{"date": d, "hour": h, "n": n} for (d, h), n in sorted(cells.items())],
    "hours": [hours.get(h, 0) for h in range(24)],
})


# ------------------------------------------------------------------ verbs per era
def verb(subject):
    s = re.sub(r"^(feat|fix|docs|test|tools|chore|research|wip)(\([^)]*\))?:\s*", "", subject, flags=re.I)
    words = s.split()
    return words[0].lower().strip(":,") if words else ""


verbs = {era: collections.Counter() for era in ("pre", "claude", "parallel")}
for c in recent:
    verbs[c["era"]][verb(c["subject"])] += 1
dump("verbs.json", {era: v.most_common(12) for era, v in verbs.items()})


# ------------------------------------------------------------------ code growth (last commit of each day)
def kind(path):
    # only the port itself: candidates staged under tools/ are not counted as game code
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


last_of_day = collections.OrderedDict()
for c in recent:
    last_of_day[c["date"][:10]] = c["hash"]
cat = subprocess.Popen(["git", "-C", REPO, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
blob_lines = {}


def lines_of(sha):
    if sha not in blob_lines:
        cat.stdin.write((sha + "\n").encode())
        cat.stdin.flush()
        _, _, size = cat.stdout.readline().decode().split()
        data = cat.stdout.read(int(size))
        cat.stdout.read(1)
        blob_lines[sha] = data.count(b"\n")
    return blob_lines[sha]


growth = []
for d, h in last_of_day.items():
    lines, files = collections.Counter(), collections.Counter()
    for t in git("ls-tree", "-r", "-l", h).split("\n"):
        if not t.strip():
            continue
        meta, path = t.split("\t", 1)
        _, _, sha, size = meta.split()
        k = kind(path)
        if k is None or size == "-" or int(size) > 5_000_000:
            continue
        files[k] += 1
        lines[k] += lines_of(sha)
    growth.append({"date": d, "commit": h, "lines": dict(lines), "files": dict(files)})
dump("growth.json", growth)

# ------------------------------------------------------------------ composition at HEAD (bytes by area)
comp = collections.defaultdict(lambda: {"files": 0, "bytes": 0})
for t in git("ls-tree", "-r", "-l", "HEAD").split("\n"):
    if not t.strip():
        continue
    meta, path = t.split("\t", 1)
    size = meta.split()[3]
    if "/Fixtures/" in path and path.startswith("native/Tests/"):
        k = "test-fixtures"
    elif path.startswith("native/") and "/Resources/" in path:
        k = "native-resources"
    elif path.startswith("native/"):
        k = "native-code"
    elif path.startswith("docs/evidence/"):
        k = "evidence"
    elif path.startswith("docs/research/"):
        k = "research"
    elif path.startswith("tools/"):
        k = "tools"
    elif path.startswith("downloads/"):
        k = "downloads-lfs-pointers"
    else:
        k = "other"
    comp[k]["files"] += 1
    comp[k]["bytes"] += int(size) if size != "-" else 0
dump("composition.json", dict(comp))

# ------------------------------------------------------------------ the turn: every commit of 2026-09-28
dump("turn_day.json", [{"time": c["date"][11:16], "hash": c["hash"], "subject": c["subject"]}
                        for c in recent if c["date"][:10] == TURN_DAY])


# ------------------------------------------------------------------ rulebook: line counts of instruction files per commit
def line_history(path):
    out = []
    for ln in git("log", "--reverse", "--format=%h %ad", "--date=format:%Y-%m-%dT%H:%M:%S%z", "--", path).split("\n"):
        if not ln.strip():
            continue
        h, d = ln.split()
        try:
            n = git("show", f"{h}:{path}").count("\n")
        except subprocess.CalledProcessError:
            n = 0  # file deleted in this commit
        out.append({"hash": h, "date": d, "lines": n})
    return out


dump("rulebook.json", {
    "AGENTS.md": line_history("AGENTS.md"),
    "CURRENT_WORK.md": line_history("docs/research/CURRENT_WORK.md"),
    "RESEARCH_MAP.md": line_history("docs/RESEARCH_MAP.md"),
})


# ------------------------------------------------------------------ summary numbers
def median(xs):
    xs = sorted(xs)
    n = len(xs)
    if not n:
        return None
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


eras = {}
for era in ("pre", "claude", "parallel"):
    cs = [c for c in recent if c["era"] == era]
    gaps = [(parse(b) - parse(a)).total_seconds() / 60 for a, b in zip(cs, cs[1:])]
    eras[era] = {
        "commits": len(cs),
        "first": cs[0]["date"], "last": cs[-1]["date"],
        "median_gap_min": round(median([g for g in gaps if g < 360]), 1),
        "night_share": round(sum(1 for c in cs if int(c["date"][11:13]) < 6) / len(cs), 3),
        "median_body_chars": median([len(c["body"]) for c in cs]),
        "with_body": sum(1 for c in cs if c["body"]),
        "conventional_prefix": sum(1 for c in cs if re.match(r"^(feat|fix|docs|test|tools|chore|research|wip)(\(|:)", c["subject"], re.I)),
    }

gaps = sorted((((parse(b) - parse(a)).total_seconds() / 3600), a["hash"], b["hash"], a["date"], b["date"])
              for a, b in zip(recent, recent[1:]))[::-1][:4]
word = lambda w: sum(1 for c in recent if re.search(rf"\b{w}\b", c["subject"], re.I))
summary = {
    "commits_all": len(commits),
    "commits_since_sept": len(recent),
    "prologue": [{"hash": c["hash"], "date": c["date"], "subject": c["subject"]} for c in prologue],
    "first": recent[0]["date"], "last": recent[-1]["date"],
    "calendar_days": len(daily),
    "active_days": sum(1 for d in daily if d["commits"]),
    "busiest_day": max(daily, key=lambda d: d["commits"]),
    "insertions": sum(c["ins"] for c in recent),
    "deletions": sum(c["del"] for c in recent),
    "night_commits": sum(1 for c in recent if int(c["date"][11:13]) < 6),
    "eras": eras,
    "longest_pauses_h": [{"hours": round(g, 1), "after": a, "before": b, "from": fa, "to": tb} for g, a, b, fa, tb in gaps],
    "subject_words": {w: word(w) for w in ("preserve", "verify", "validate", "recover", "reproduce", "port",
                                            "play", "cross-check", "failure", "correct", "fix", "original")},
    "research_cards": int(git("ls-tree", "-r", "--name-only", "HEAD", "docs/research").count(".md")),
    "plan_cards": sum(1 for p in git("ls-tree", "-r", "--name-only", "HEAD", "docs/research").split("\n") if p.endswith("_PLAN.md")),
    "evidence_files": len([p for p in git("ls-tree", "-r", "--name-only", "HEAD", "docs/evidence").split("\n") if p]),
    "oracle_scripts": len([p for p in git("ls-tree", "--name-only", "HEAD", "tools/").split("\n") if os.path.basename(p).startswith("oracle")]),
}
tests = 0
for p in git("ls-tree", "-r", "--name-only", "HEAD", "native/Tests").split("\n"):
    if p.endswith(".swift"):
        tests += len(re.findall(r"\bfunc test\w*", git("show", f"HEAD:{p}")))
summary["test_functions"] = tests
dump("summary.json", summary)
print(json.dumps({k: v for k, v in summary.items() if k != "prologue"}, ensure_ascii=False, indent=1))


# ------------------------------------------------------------------ the app layer: what a player could see
app_lines = {}
for d, h in last_of_day.items():
    n = 0
    for p in git("ls-tree", "-r", "--name-only", h, "native/Sources/NTSDApp").split("\n"):
        if p.endswith(".swift"):
            n += git("show", f"{h}:{p}").count("\n")
    app_lines[d] = n
dump("app_lines.json", {"note": "lines of native/Sources/NTSDApp/*.swift at the last commit of each day with commits", "app_lines": app_lines})
