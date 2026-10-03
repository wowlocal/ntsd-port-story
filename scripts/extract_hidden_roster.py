#!/usr/bin/env python3
"""Portraits of the characters the original hides behind the LF2.NET cheat.

Usage:
    python3 scripts/extract_hidden_roster.py [../ntsd-2.4]

The character screen of NTSD 2.4 (EXE 42a651..42a899, docs/research/CHARACTER_SCREEN.md)
skips type-0 objects whose ID/10 is 3 or 5 unless the global 458428 is 1; typing
LF2.NET on the mode menu toggles that global. This script lists those objects from
data/data.txt, reads each DAT header (name, head bitmap) and converts the portrait
to public/img/hidden/<file>.png with ffmpeg. Writes data/hidden_roster.json.
"""
import json
import os
import re
import subprocess
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "ntsd-2.4"))
GAME = os.path.join(REPO, "downloads", "NTSD_2.4_2.0a_clean", "NTSD 2.4_2.0a")
DECK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(DECK, "public", "img", "hidden")
KEY = b"SiuHungIsAGoodBearBecauseHeIsVeryGood"
KEY = KEY[123 % len(KEY):] + KEY[:123 % len(KEY)]


def decode(path):
    data = open(path, "rb").read()
    return bytes((b - KEY[i % len(KEY)]) & 255 for i, b in enumerate(data[123:])).decode("latin-1")


os.makedirs(OUT, exist_ok=True)
roster = []
listing = open(os.path.join(GAME, "data", "data.txt"), encoding="latin-1").read()
for oid, typ, f in re.findall(r"id:\s*(\d+)\s+type:\s*(\d+)\s+file:\s*(\S+)", listing):
    oid, typ = int(oid), int(typ)
    if typ != 0 or oid // 10 not in (3, 5):
        continue
    f = f.replace("\\", "/")
    dat = os.path.join(GAME, f)
    head = decode(dat).split("<bmp_end>")[0]
    name = re.search(r"name:\s*(.+)", head)
    face = re.search(r"head:\s*(\S+)", head)
    item = {"id": oid, "file": os.path.basename(f), "name": name.group(1).strip() if name else None}
    if face:
        src = os.path.join(GAME, face.group(1).replace("\\", "/"))
        png = os.path.splitext(os.path.basename(f))[0] + ".png"
        if os.path.exists(src):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-frames:v", "1", os.path.join(OUT, png)], check=True)
            item["image"] = f"/img/hidden/{png}"
    roster.append(item)
roster.sort(key=lambda r: r["id"])
with open(os.path.join(DECK, "data", "hidden_roster.json"), "w") as fh:
    json.dump({"rule": "type-0 objects with ID/10 in {3, 5} are selectable only while 458428 == 1 (LF2.NET)", "characters": roster}, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print(len(roster), [(r["id"], r["name"], bool(r.get("image"))) for r in roster])
