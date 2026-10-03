#!/usr/bin/env python3
"""Cut Naruto's frames out of the original sprite sheets and read their hitboxes from the DAT.

Usage:
    python3 scripts/extract_frames.py [../ntsd-2.4] [--sequence-only] [--force]

Writes public/img/frames/naruto-<id>.png (black keyed to transparent, as the
game draws it) and data/engine_frames.json with each frame's raw DAT text and
its body (bdy), attack (itr), weapon (wpoint) and catch (cpoint) points.

It also follows one real `next` chain, the clone_spin special that standing
frames reach through `hit_Da: 285`, until `next: 999`, and writes
data/engine_sequence.json plus one PNG per picture under public/img/frames/seq/.

Existing PNGs are kept unless --force is given; --sequence-only skips
engine_frames.json. Needs ffmpeg for the crops. Decoding follows
tools/import_ntsd.py of the port.
"""
import argparse
import json
import os
import re
import subprocess

DECK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
parser = argparse.ArgumentParser()
parser.add_argument("repo", nargs="?", default=os.path.join(DECK, "..", "ntsd-2.4"))
parser.add_argument("--sequence-only", action="store_true", help="write only engine_sequence.json and its PNGs")
parser.add_argument("--force", action="store_true", help="re-crop PNGs that already exist")
args = parser.parse_args()

REPO = os.path.abspath(args.repo)
GAME = os.path.join(REPO, "downloads", "NTSD_2.4_2.0a_clean", "NTSD 2.4_2.0a")
OUT_IMG = os.path.join(DECK, "public", "img", "frames")
KEY = b"SiuHungIsAGoodBearBecauseHeIsVeryGood"
KEY = KEY[123 % len(KEY):] + KEY[:123 % len(KEY)]  # the 123-byte header also advances the key
SELECTED = [0, 63, 72, 258, 123]
SEQUENCE_START = 285  # clone_spin; frames 0-8 carry hit_Da: 285
TICK_MS = 33  # docs/ORIGINAL_ENGINE.md:75-79: one 0x43e9a0 call per 33 ms of baseline


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


def head_of(body):
    return ints(body.split("\n", 2)[1] if "\n" in body else body)


def crop(pic, png):
    """Cut picture `pic` out of its sheet into OUT_IMG/png; returns the sheet and cell."""
    sheet = next(s for s in sheets if s["first"] <= pic <= s["last"])
    i = pic - sheet["first"]
    x = (i % sheet["row"]) * (sheet["w"] + 1)
    y = (i // sheet["row"]) * (sheet["h"] + 1)
    out = os.path.join(OUT_IMG, png)
    if args.force or not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run([
            "ffmpeg", "-v", "error", "-y", "-i", os.path.join(GAME, sheet["file"]),
            "-vf", f"crop={sheet['w']}:{sheet['h']}:{x}:{y},format=rgba,colorkey=0x000000:0.01:0",
            "-frames:v", "1", out,
        ], check=True)
    return sheet, {"x": x, "y": y}


if not args.sequence_only:
    frames = []
    for fid in SELECTED:
        name, body, raw = definitions[fid][0]
        head = head_of(body)
        pic = head["pic"]
        png = f"naruto-{fid}.png"
        sheet, cell = crop(pic, png)
        frames.append({
            "id": fid, "name": name, "pic": pic, "state": head.get("state"), "wait": head.get("wait"), "next": head.get("next"),
            "centerx": head.get("centerx"), "centery": head.get("centery"),
            "image": f"/img/frames/{png}", "w": sheet["w"], "h": sheet["h"],
            "sheet": sheet["file"], "cell": cell,
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

# ---- one real `next` chain, frame by frame -------------------------------------------------
objects = {}
for oid, path in re.findall(r"id:\s*(\d+)\s+type:\s*\d+\s+file:\s*(\S+)", open(os.path.join(GAME, "data", "data.txt"), encoding="latin-1").read()):
    objects.setdefault(int(oid), path.replace("\\", "/"))

entry = [fid for fid in sorted(definitions) if head_of(definitions[fid][0][1]).get("hit_Da") == SEQUENCE_START]
chain, seen, fid = [], set(), SEQUENCE_START
while 0 < fid < 400 and fid != 999 and fid not in seen:
    assert len(definitions[fid]) == 1, f"frame {fid} is defined more than once"
    seen.add(fid)
    name, body, raw = definitions[fid][0]
    head = head_of(body)
    pic = head["pic"]
    png = f"seq/naruto-p{pic}.png"
    sheet, cell = crop(pic, png)
    sound = re.search(r"sound:\s*(\S+)", body)
    opoints = blocks(body, "opoint")
    for o in opoints:
        o["file"] = objects.get(o.get("oid"))
    chain.append({
        "id": fid, "name": name, "pic": pic, "state": head.get("state"), "wait": head.get("wait"), "next": head.get("next"),
        "ticks": head.get("wait") + 1,
        "centerx": head.get("centerx"), "centery": head.get("centery"),
        "dvx": head.get("dvx", 0), "dvy": head.get("dvy", 0), "mp": head.get("mp"),
        "sound": sound.group(1).replace("\\", "/") if sound else None,
        "image": f"/img/frames/{png}", "w": sheet["w"], "h": sheet["h"], "sheet": sheet["file"], "cell": cell,
        "bdy": blocks(body, "bdy"), "itr": blocks(body, "itr"), "wpoint": blocks(body, "wpoint"), "opoint": opoints,
    })
    fid = head.get("next")

sequence = {
    "object": "chars/naruto.dat",
    "start": SEQUENCE_START,
    "entry": {"frames": entry, "field": "hit_Da"},
    "end": {"next": fid, "becomes": 0 if fid == 999 else fid,
            "rule": "next 999 becomes 212 only for type 0 with integerY != 0, otherwise 0: docs/research/ACTOR_SCHEDULER.md:53-54"},
    "tick_rule": "wait counter resets on a frame change and then increments every scheduler call; when it exceeds the "
                 "frame's wait it resets and next is written, so a frame lasts wait + 1 calls: docs/research/ACTOR_SCHEDULER.md:43-44, 51-52",
    "tick_ms": TICK_MS,
    "ticks": sum(f["ticks"] for f in chain),
    "frames": chain,
}
with open(os.path.join(DECK, "data", "engine_sequence.json"), "w") as f:
    json.dump(sequence, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("sequence", [(f["id"], f["name"], f["wait"], f["next"], len(f["itr"])) for f in chain], "->", fid, "ticks", sequence["ticks"], "entry", entry)
