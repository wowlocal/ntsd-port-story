#!/usr/bin/env python3
"""Data for the chapter on the cross-platform port (3–5 October) and the 7 October passport.

Usage:
    python3 scripts/collect_xplat.py [/path/to/ntsd-2.4]

Writes data/xplat.json. Everything is read with plain `git` commands and from
committed evidence files at pinned commits, so a later checkout of the port
repository does not change the result; nothing in the source repository is
modified. Times are the commit's own local time as recorded by git (+02:00).

Pinned commits:
  PART1  fc959db  3 Oct 16:18  the commit the first part of the deck was counted at
  MAIN   74be317  3 Oct 16:44  main: the signed v0.4.0 release script
  NINE   2fe64be  5 Oct 01:59  nine-host matrix baseline, before the phone work
  TEN    7f15b7b  5 Oct 22:39  all ten scenarios equal on all nine hosts
  NOW    8840eb3  7 Oct 08:23  head of exp/core-realtime when this chapter was written
"""
import collections
import json
import os
import re
import subprocess
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "ntsd-2.4"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "xplat.json")
PART1, MAIN, NINE, TEN, NOW = "fc959db", "74be317", "2fe64be", "7f15b7b", "8840eb3"
SINCE = "2026-09-01"


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], check=True, capture_output=True).stdout.decode("utf-8", "replace")


def show_json(ref, path):
    return json.loads(git("show", f"{ref}:{path}"))


cat = subprocess.Popen(["git", "-C", REPO, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
_lines = {}


def blob(sha):
    cat.stdin.write((sha + "\n").encode())
    cat.stdin.flush()
    _, _, size = cat.stdout.readline().decode().split()
    data = cat.stdout.read(int(size))
    cat.stdout.read(1)
    return data


def lines_of(sha):
    if sha not in _lines:
        _lines[sha] = blob(sha).count(b"\n")
    return _lines[sha]


def tree(ref):
    for t in git("ls-tree", "-r", "-l", ref).split("\n"):
        if t.strip():
            meta, path = t.split("\t", 1)
            _, _, sha, size = meta.split()
            yield path, sha, size


# ------------------------------------------------------------------ passport: the same definitions as collect_stats.py
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
    for path, sha, size in tree(ref):
        if path.startswith("docs/evidence/"):
            evidence += 1
        k = kind(path)
        if k is None or size == "-" or int(size) > 5_000_000:
            continue
        files[k] += 1
        lines[k] += lines_of(sha)
        if k == "swift-tests":
            tests += len(re.findall(rb"\bfunc test\w*", blob(sha)))
    log = git("log", ref, f"--since={SINCE}", "--format=%ad", "--date=format:%Y-%m-%d").split()
    stat = git("log", ref, f"--since={SINCE}", "--numstat", "--format=")
    ins = sum(int(m.group(1)) for m in re.finditer(r"^(\d+)\t\d+\t", stat, re.M))
    return {
        "ref": ref, "date": git("log", "-1", "--format=%ad", "--date=format:%Y-%m-%dT%H:%M:%S%z", ref).strip(),
        "commits_since_sept": len(log), "active_days": len(set(log)), "first_day": min(log), "last_day": max(log),
        "swift_src_lines": lines["swift-src"], "swift_src_files": files["swift-src"],
        "swift_test_lines": lines["swift-tests"], "test_functions": tests,
        "python_lines": lines["python"], "research_cards": files["research-md"], "evidence_files": evidence,
        "insertions": ins,
    }


# ------------------------------------------------------------------ architecture: Swift lines per target
GROUPS = {
    "NTSDCore": "core", "NTSDRuntime": "runtime",
    "NTSDMacPlatform": "mac", "NTSDApp": "mac", "NTSDSDL": "sdl", "NTSDHeadless": "headless",
    "NTSDiOS": "ios", "NTSDAndroid": "android", "NTSDFreeTypeText": "freetype", "NTSDMusicDecoder": "music",
}


def targets(ref):
    out = collections.Counter()
    for path, sha, size in tree(ref):
        if not (path.startswith("native/Sources/") and path.endswith(".swift")):
            continue
        t = path.split("/")[2]
        out[GROUPS.get(t, "checks")] += lines_of(sha)
    return dict(out)


core_diff = []
for ln in git("diff", "--numstat", MAIN, NINE, "--", "native/Sources/NTSDCore").strip().split("\n"):
    a, d, p = ln.split("\t")
    core_diff.append({"file": p.split("/")[-1], "added": int(a), "deleted": int(d)})

# ------------------------------------------------------------------ the 30 hours: every commit from the plan to the cross-platform ONLINE GAME
# lane of each commit, by what it changed (reviewed by hand against `git show --stat`)
LANE = {
    "core": "c753d7c 4547acc 65c6916 699f9ec 48db790 503af05 3f43f53 fb61a77 56ac79e 1c2db2a 882adc6 92985dd c5f5e0b 08e6f4f "
            "1dcf183 d855299 60b463b fb2e1c0 6e68178 5ffe2dc 706dc65 2f5e707 da2414f b5d00e4 af1f808",
    "linux": "c649bac ebb9adc 6cdb5c2 414a2aa 5dd1933 f7de972 a72ae97 4bbf311 3e3c712 de3ad55 7c504a6 927f319 0f91b25 ee2c6b8 e1eb5b8 db3e341 b13b1de",
    "macsdl": "6b6ed02 50c19ea",
    "windows": "6203799 c8f475b d02c20b 6dfc200 e300149 a8ed861 c50e514",
    "ipad": "8f6d1eb 3045f07 14e495e 9d63735 edccfde",
    "android": "38fc1a8 0fc5bb9 07bc662 1fc52f2 b9d4b62 f1acc80",
    "matrix": "b154778 a4c48a6 87edc32 e752f9c 59cb328 e240ca2 71dd3cb 2fe64be c9803c9 0a3707d e509c32 75593f5",
}
lane_of = {h: lane for lane, hs in LANE.items() for h in hs.split()}
MILESTONE = {
    "65c6916": "ядро собралось под Linux",
    "5dd1933": "VS-матч: Linux = macOS",
    "a72ae97": "баг компилятора Swift",
    "50c19ea": "15 909 кадров SDL = AppKit",
    "0f91b25": "пакет на чистом Ubuntu",
    "a8ed861": "онлайн через Winsock",
    "8f6d1eb": "iPad в симуляторе",
    "71dd3cb": "pre-release Linux и Windows",
    "07bc662": "Android-приложение",
    "2fe64be": "9 хостов, одно состояние",
    "c9803c9": "онлайн между платформами",
}
raw = git("log", "--reverse", "--format=%h\x1f%ad\x1f%s", "--date=format:%Y-%m-%dT%H:%M", f"{MAIN}..75593f5")
commits = []
for ln in raw.strip().split("\n"):
    h, d, s = ln.split("\x1f")
    commits.append({"hash": h, "time": d, "subject": s, "lane": lane_of.get(h, "other"), **({"milestone": MILESTONE[h]} if h in MILESTONE else {})})
unlabelled = [c["hash"] for c in commits if c["lane"] == "other"]
assert not unlabelled, unlabelled

# ------------------------------------------------------------------ the matrix: 9 hosts x 10 scenarios, before and after the playback fix
EV = "docs/evidence/"
nine = show_json(NINE, EV + "crossplatform-matrix-20261005-nine-hosts.json")
speed = show_json(TEN, EV + "crossplatform-matrix-20261005-speed.json")
SCEN = ["vs", "mission", "demo", "war", "playback", "tournament", "altenter", "tournament-win", "team-tournament", "joystick"]


def grid(m, recompare=None):
    out = {}
    for host, v in m["hosts"].items():
        row = {}
        for s in SCEN:
            row[s] = "equal" if s in v.get("equal", []) else "differs"
        if recompare:
            for k, r in recompare.items():
                if k.startswith(host + "/") and r.get("result") == "equal":
                    row[k.split("/")[1].split()[0]] = "equal"
        out[host] = row
    return out


matrix = {
    "scenarios": SCEN,
    "groups": {h: v["group"] for h, v in speed["hosts"].items()},
    "before": {"commit": nine["commit"][:7], "date": nine["date"], "cells": grid(nine), "frames": nine["frames"]},
    "after": {"commit": speed["commit"][:7], "recorded_in": TEN, "date": speed["date"], "cells": grid(speed, speed.get("recompare")),
              "frames": speed["frames"], "note": speed["note"]},
    "playback_cause": "the working tree held the recording's 130-byte Git LFS pointer, which the game rejects; app_e2e.py now reads the committed recording from the local LFS store (16cb07b)",
    "source": [f"{NINE}:{EV}crossplatform-matrix-20261005-nine-hosts.json", f"{TEN}:{EV}crossplatform-matrix-20261005-speed.json"],
}

# ------------------------------------------------------------------ ONLINE GAME across platforms
on = show_json("e509c32", EV + "crossplatform-online-cross-20261005.json")
onl = show_json("e509c32", EV + "crossplatform-online-cross-linux-client-20261005.json")
pairs = []
for k, r in on["results"].items():
    pairs.append({"host": r["roles"]["host"], "client": r["roles"]["client"], "result": r["result"], "rng": r["rngSHA256"]})
for k, r in (on.get("linux (added later the same day)") or {}).items() if isinstance(on.get("linux (added later the same day)"), dict) else []:
    if isinstance(r, dict) and r.get("roles"):
        pairs.append({"host": r["roles"]["host"], "client": r["roles"]["client"], "result": r["result"], "rng": r.get("rngSHA256")})
for k, r in onl["results"].items():
    if isinstance(r, dict) and r.get("roles"):
        pairs.append({"host": r["roles"]["host"], "client": r["roles"]["client"], "result": r["result"], "rng": r.get("rngSHA256")})
online = {"pairs": pairs, "cause_linux_client": onl["cause (strace of the Linux client, NTSD_PAIR_STRACE=1)"],
          "binaries": on["binaries"], "source": [f"e509c32:{EV}crossplatform-online-cross-20261005.json", f"e509c32:{EV}crossplatform-online-cross-linux-client-20261005.json"]}

# ------------------------------------------------------------------ the compiler bug
rep = show_json("b13b1de", EV + "crossplatform-swift640-report-20261004.json")
uni = show_json("a72ae97", EV + "crossplatform-swift640-linux-uniqueness-20261004.json")
swift = {
    "issue": rep["issue"]["url"], "title": rep["issue"]["title"],
    "results": rep["results"], "codegen": uni["codegen"], "symptom": uni["symptom"]["x86_64"],
    "closed": {"at": "2026-10-06T10:06:53Z", "by_comment": "This is fixed on 6.4.x by https://github.com/swiftlang/swift/pull/92771",
               "source": "gh issue view 92905 -R swiftlang/swift, read 7 Oct 2026"},
    "source": [f"a72ae97:{EV}crossplatform-swift640-linux-uniqueness-20261004.json", f"b13b1de:{EV}crossplatform-swift640-report-20261004.json"],
}

data = {
    "note": "cross-platform chapter data; pinned commits in scripts/collect_xplat.py",
    "passport": {"before": passport(PART1), "after": passport(NOW)},
    "targets": {"main": targets(MAIN), "nine": targets(NINE), "now": targets(NOW)},
    "core_diff": {"from": MAIN, "to": NINE, "files": core_diff,
                  "added": sum(f["added"] for f in core_diff), "deleted": sum(f["deleted"] for f in core_diff)},
    "commits": commits,
    "matrix": matrix,
    "online": online,
    "swift": swift,
}
with open(OUT, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(json.dumps({"passport": data["passport"], "targets": data["targets"], "core_diff": {k: v for k, v in data["core_diff"].items() if k != "files"},
                  "commits": len(commits), "lanes": collections.Counter(c["lane"] for c in commits), "pairs": len(pairs)}, ensure_ascii=False, indent=1))
