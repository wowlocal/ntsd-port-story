#!/usr/bin/env python3
"""Capability matrix of open-source LF2 engines for the deck.

Usage:
    python3 scripts/build_oss_matrix.py

Reads data/evidence/lf2-oss-engines.json (GitHub API data, shallow clones and source
reading on 2026-10-03; every cell carries its evidence and source lines) and writes
data/oss_matrix.json: one row per repository with short name, language, own code lines,
stars, last commit and the capability cells, plus a row for this port.
"""
import json
import os

DECK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(DECK, "data", "evidence", "lf2-oss-engines.json")
OUT = os.path.join(DECK, "data", "oss_matrix.json")
COLS = ["readsOriginalDat", "frameStateMachine", "combatBoxes", "physics", "computerAI", "modesBeyondVS",
        "replays", "network", "automatedTests", "comparesWithOriginal", "nativeMacOS"]
SHORT = {
    "atom-tm/l2df-engine": "L2DF", "gimhol/Little-Fighter-Wemake": "Wemake", "Project-F/F.LF": "F.LF",
    "Mesujin/LF2-Enchanted-4th": "Enchanted 4th", "xsoameix/openlf2": "openlf2", "Archer-Dante/Neora": "Neora",
    "s911415/html5-lf2": "html5-lf2", "Razenpok-Graveyard/lf2net": "lf2net", "Tomius/LittleFighter": "Tomius/LF",
    "shivamshekhar/LittleFighter": "shivamshekhar/LF", "GDur/jLF2": "jLF2", "fishfolk/punchy": "Punchy",
    "Mesujin/LF2-AI-ScriptEngine": "AI-ScriptEngine",
}
CODE = {"yes": "y", "partial": "p", "no": "n", "unknown": "u"}

d = json.load(open(SRC))
rows = []
for r in d["repositories"]:
    name = r["repository"]
    cells = {c: CODE.get(d["matrix"][name][c]["value"], "u") for c in COLS}
    dates = [(r.get("pinned") or {}).get("commitDateUTC") or "", (r.get("defaultBranch") or {}).get("lastCommitDateUTC") or ""]
    score = sum(1 if v == "y" else 0.5 if v == "p" else 0 for v in cells.values())
    rows.append({"name": SHORT.get(name, name), "repo": name, "lang": r["github"]["primaryLanguage"],
                 "loc": r["loc"].get("ownNonTestCode"), "stars": r["github"]["stars"], "last": max(dates)[:7],
                 "cells": cells, "score": score})
rows.sort(key=lambda x: (-x["score"], -x["stars"]))
port = d["contextProjectPort"]
out = {
    "as_of": d.get("asOfDate", "2026-10-03"),
    "columns": COLS,
    "rows": rows,
    "port": {"name": "этот порт", "lang": "Swift", "loc": port["runtimeSwift"]["total"], "stars": None, "last": "2026-10",
             "cells": {c: "y" for c in COLS}},
}
with open(OUT, "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
    f.write("\n")
print([(r["name"], r["score"]) for r in rows])
