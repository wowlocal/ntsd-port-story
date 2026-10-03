#!/bin/sh
# Render the port's git history (7 Sep – 3 Oct 2026) as a Gource video for the deck.
#
#   sh scripts/make_gource.sh [../ntsd-2.4]
#
# Needs gource and ffmpeg (brew install gource ffmpeg) and a logged-in GUI session:
# gource draws into an OpenGL window and streams the frames to ffmpeg.
# Users are the agents: commits with "Co-Authored-By: Claude" are Claude, commits
# without the trailer before 28 September are Codex, later ones the parallel Codex.
# A file takes the colour of the agent that touched it last.
set -eu
REPO=$(cd "${1:-../ntsd-2.4}" && pwd)
DECK=$(cd "$(dirname "$0")/.." && pwd)
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

python3 - "$REPO" "$WORK/history.log" <<'EOF'
import subprocess, sys, datetime as dt
repo, out = sys.argv[1], sys.argv[2]
RS, US = "\x1e", "\x1f"
raw = subprocess.run(["git", "-C", repo, "log", "--reverse", "--since=2026-09-01", "--name-status", "--no-renames",
                      f"--format={RS}%ct{US}%ad{US}%B{US}", "--date=format:%Y-%m-%d"],
                     check=True, capture_output=True, text=True).stdout
colour = {"Codex": "3987E5", "Claude": "D95926", "Codex · сеть": "199E70"}
lines = []
for chunk in raw.split(RS)[1:]:
    ct, day, body, files = chunk.split(US)
    who = "Claude" if "Co-Authored-By: Claude" in body else ("Codex" if day < "2026-09-28" else "Codex · сеть")
    for ln in files.strip().splitlines():
        parts = ln.split("\t")
        if len(parts) < 2:
            continue
        kind = {"A": "A", "D": "D"}.get(parts[0][0], "M")
        path = parts[-1]
        if path.startswith("downloads/"):
            continue
        lines.append(f"{ct}|{who}|{kind}|/{path}|{colour[who]}")
open(out, "w").write("\n".join(lines) + "\n")
print(len(lines), "file events")
EOF

# round avatars in the deck's series colours
mkdir -p "$WORK/avatars"
for pair in "Codex:0x3987E5" "Claude:0xD95926" "Codex · сеть:0x199E70"; do
  name=${pair%%:*}; col=${pair#*:}
  ffmpeg -v error -y -f lavfi -i "color=c=${col}:s=96x96,format=rgba" \
    -vf "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lte(hypot(X-47.5,Y-47.5),46),255,0)'" \
    -frames:v 1 "$WORK/avatars/$name.png"
done

FONT=/System/Library/Fonts/Supplemental/Arial\ Unicode.ttf
[ -f "$FONT" ] || FONT=/System/Library/Fonts/Helvetica.ttc

gource "$WORK/history.log" \
  --viewport 1280x720 --output-framerate 30 --multi-sampling \
  --seconds-per-day 2.2 --auto-skip-seconds 0.4 --file-idle-time 0 --max-file-lag 0.2 \
  --background-colour 0A0D13 --font-file "$FONT" --font-size 20 --font-colour F6F3EC \
  --title "NTSD 2.4 → macOS · история репозитория" --date-format "%d.%m.%Y" \
  --user-image-dir "$WORK/avatars" --user-scale 1.4 --highlight-users \
  --hide mouse,progress,filenames --dir-font-size 11 --user-font-size 15 \
  --bloom-multiplier 0.7 --bloom-intensity 0.5 --elasticity 0.02 --camera-mode overview --padding 1.25 \
  --stop-at-end --disable-input \
  --output-ppm-stream - \
| ffmpeg -v error -y -r 30 -f image2pipe -vcodec ppm -i - \
  -vf "scale=1280:720:flags=lanczos,format=yuv420p" -c:v libx264 -preset slow -crf 27 \
  -movflags +faststart "$DECK/public/media/gource.mp4"

ffmpeg -v error -y -sseof -4 -i "$DECK/public/media/gource.mp4" -frames:v 1 -q:v 4 "$DECK/public/media/gource-poster.jpg"
ffprobe -v error -show_entries format=duration,size -of compact "$DECK/public/media/gource.mp4"
