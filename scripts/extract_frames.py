#!/usr/bin/env python3
"""Cut Naruto's frames out of the original sprite sheets and read their hitboxes from the DAT.

Usage:
    python3 scripts/extract_frames.py [../ntsd-2.4]

Writes public/img/frames/naruto-<id>.png (black keyed to transparent, as the
game draws it) and data/engine_frames.json with each frame's raw DAT text and
its body (bdy), attack (itr), weapon (wpoint) and catch (cpoint) points.
Needs ffmpeg for the crops. Decoding follows tools/import_ntsd.py of the port.
"""
import json
import os
import re
import subprocess
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "ntsd-2.4"))
GAME = os.path.join(REPO, "downloads", "NTSD_2.4_2.0a_clean", "NTSD 2.4_2.0a")
DECK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT_IMG = os.path.join(DECK, "public", "img", "frames")
KEY = b"SiuHungIsAGoodBearBecauseHeIsVeryGood"
KEY = KEY[123 % len(KEY):] + KEY[:123 % len(KEY)]  # the 123-byte header also advances the key
SELECTED = [0, 63, 72, 258, 123]


def decode(path):
    data = open(path, "rb").read()
    return bytes((b - KEY[i % len(KEY)]) & 255 for i, b in enumerate(data[123:])).decode("latin-1")


def ints(text):
    return {k: int(v) for k, v in re.findall(r"([A-Za-z_]+):\s*(-?\d+)", text)}


text = decode(os.path.join(GAME, "chars", "naruto.dat"))
sheets = []
for a, b, f, w, h, row, col in re.findall(r"file\((\d+)-(\d+)\):\s*(\S+)\s+w:\s*(\d+)\s+h:\s*(\d+)\s+row:\s*(\d+)\s+col:\s*(\d+)", text):
    sheets.append({"first": int(a), "last": int(b), "file": f.replace("\\", "/"), "w": int(w), "h": int(h), "row": int(row), "col": int(col)})

definitions = {}
for m in re.finditer(r"<frame>\s+(\d+)\s+(\S+)(.*?)<frame_end>", text, re.S):
    definitions.setdefault(int(m.group(1)), []).append((m.group(2), m.group(3), m.group(0)))


def blocks(body, name):
    return [ints(b) for b in re.findall(name + r":(.*?)" + name + r"_end:", body, re.S)]


os.makedirs(OUT_IMG, exist_ok=True)
frames = []
for fid in SELECTED:
    name, body, raw = definitions[fid][0]
    head = ints(body.split("\n", 2)[1] if "\n" in body else body)
    pic = head["pic"]
    sheet = next(s for s in sheets if s["first"] <= pic <= s["last"])
    i = pic - sheet["first"]
    x = (i % sheet["row"]) * (sheet["w"] + 1)
    y = (i // sheet["row"]) * (sheet["h"] + 1)
    png = f"naruto-{fid}.png"
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-i", os.path.join(GAME, sheet["file"]),
        "-vf", f"crop={sheet['w']}:{sheet['h']}:{x}:{y},format=rgba,colorkey=0x000000:0.01:0",
        "-frames:v", "1", os.path.join(OUT_IMG, png),
    ], check=True)
    frames.append({
        "id": fid, "name": name, "pic": pic, "state": head.get("state"), "wait": head.get("wait"), "next": head.get("next"),
        "centerx": head.get("centerx"), "centery": head.get("centery"),
        "image": f"/img/frames/{png}", "w": sheet["w"], "h": sheet["h"],
        "sheet": sheet["file"], "cell": {"x": x, "y": y},
        "bdy": blocks(body, "bdy"), "itr": blocks(body, "itr"),
        "wpoint": blocks(body, "wpoint"), "cpoint": blocks(body, "cpoint"),
        "raw": re.sub(r"[ \t]+\n", "\n", raw.replace("\r", "")).strip(),
        "definitions": len(definitions[fid]),
    })

stats = {
    "frame_definitions": sum(len(v) for v in definitions.values()),
    "frames": len(definitions),
    "repeated": sorted(k for k, v in definitions.items() if len(v) > 1),
    "with_phantom_bdy": sum(1 for v in definitions.values() for (_, b, _) in v if any(d.get("y") == 80000 for d in blocks(b, "bdy"))),
    "debug_fill_values": text.count("-842150451"),
}
with open(os.path.join(DECK, "data", "engine_frames.json"), "w") as f:
    json.dump({"object": "chars/naruto.dat", "sheets": sheets, "frames": frames, "stats": stats}, f, ensure_ascii=False, indent=1)
    f.write("\n")
print(json.dumps(stats), [(fr["id"], fr["name"], fr["pic"], fr["cell"]) for fr in frames])
