#!/usr/bin/env python3
"""Regenerate the deck's data/web_*.json (chapter 17, «В браузере и на телевизоре»)
from the NTSD port repository.

Usage:
    python3 scripts/collect_web.py ../ntsd-2.4 [REV]

REV defaults to 5f5a8ee4 (main, 13 Oct 2026, 20:14), the commit the chapter
is frozen at. Its subject is the Apple TV and Web loop (TVOS_WEB T0–T1c,
W0–W4: branches exp/tvos-web and exp/web-text) and the scalable window
(WINDOW_SCALING S0–S6: exp/window-scaling), 11 Oct 20:12 → 13 Oct 06:21,
a16fe0d2 … f0471f13, all on main by fast-forward.

Every number is read with `git show REV:path` (research cards
docs/research/TVOS_WEB.md and WINDOW_SCALING.md, evidence
docs/evidence/tw-*.json, ws-*.json, web-text-20261013.json,
release-refresh-20261013.json) or `git log`, so later commits do not change
the output. Values that are derived here (a two-point model of a first visit,
the uneven-pixel counts of nearest scaling) say so in their `derived` field.

Nothing in the source repository is modified: only `git show` and `git log`.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../ntsd-2.4")
REV = sys.argv[2] if len(sys.argv) > 2 else "5f5a8ee4"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
FIRST, LAST = "a16fe0d2", "f0471f13"
FROZEN = "состояние на 13 октября 2026, 20:14 (5f5a8ee4)"
EV = "docs/evidence/"
RS = "docs/research/"


def git(*args):
    res = subprocess.run(["git", "-C", REPO, *args], check=True, capture_output=True)
    return res.stdout.decode("utf-8", "replace")


def show(path):
    return git("show", f"{REV}:{path}")


def evidence(name):
    return json.loads(show(EV + name))


def dump(name, obj):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def need(pattern, text, what):
    m = re.search(pattern, re.sub(r"\s+", " ", text))  # Markdown wraps lines; match across them
    if not m:
        raise SystemExit(f"collect_web: cannot find {what!r} ({pattern})")
    return m


def mb(n):
    return round(n / 1e6, 1)


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else round((xs[n // 2 - 1] + xs[n // 2]) / 2, 4)


tvos_web = show(RS + "TVOS_WEB.md")
scaling = show(RS + "WINDOW_SCALING.md")

# ------------------------------------------------------------------ steps
log = git("log", "--reverse", "--format=%h%x09%H%x09%cI%x09%s", f"{FIRST}^..{LAST}")
steps = []
for line in log.strip().splitlines():
    short, full, iso, subject = line.split("\t", 3)
    m = re.search(r"\((TVOS_WEB|WINDOW_SCALING)(?: ([A-Z0-9a-z, -]+))?\)$", subject)
    if not m:
        raise SystemExit(f"collect_web: untagged commit {short} {subject}")
    card, step = m.group(1), (m.group(2) or "").strip()
    if card == "WINDOW_SCALING":
        lane = "window"
    elif step.startswith("T"):
        lane = "tvos"
    elif step.startswith("W"):
        lane = "web"
    else:
        lane = "card"
    if step in ("S0",):
        lane = "card"
    steps.append({"hash": full[:8], "time": iso[:16], "subject": subject[: m.start()].strip(),
                  "card": card, "step": step or None, "lane": lane})
t0 = datetime.fromisoformat(steps[0]["time"])
t1 = datetime.fromisoformat(steps[-1]["time"])
dump("web_steps.json", {
    "title": "Apple TV, Web и масштабируемое окно: коммиты a16fe0d2 … f0471f13",
    "source": f"git log --reverse {FIRST}^..{LAST} (ntsd-2.4); дорожка — по метке карточки в заголовке коммита",
    "caveat": "время коммита, UTC+2; все коммиты попали в main перемоткой (fast-forward), без merge-коммитов",
    "frozen": FROZEN,
    "count": len(steps),
    "hours": round((t1 - t0).total_seconds() / 3600, 1),
    "first": steps[0]["time"], "last": steps[-1]["time"],
    "tag": "web-f0471f13-20261013 (на f0471f13, W4)",
    "steps": steps,
})

# ------------------------------------------------------------------ hosts: the same frames
t0e = evidence("tw-t0-tvos-simulator-20261011.json")
t1a = evidence("tw-t1a-tvos-all-scenarios-20261011.json")
w0 = evidence("tw-w0-w1-wasi-headless-20261011.json")
w2a = evidence("tw-w2a-browser-runner-20261012.json")
w3e = evidence("tw-w3e-wasi-lazy-packages-20261012.json")
text = evidence("web-text-20261013.json")
s1 = evidence("ws-s1-tvos-full-screen-20261013.json")

t1a_frames = t1a["framesTvosAgainstAppKit"][-1]
assert t1a_frames["result"] == "identical"
tvos_rows = t1a["tvos"]
scenarios = [r["scenario"] for r in tvos_rows]


def rows_equal(rows):
    out = {}
    for r in rows:
        res = r.get("result") or r.get("compare", {}).get("result")
        out[r["scenario"]] = res
    return out


wasi = w3e["scenarios"]["wasi"]
chrom = w3e["scenarios"]["chromium"]
webk = w3e["scenarios"]["webkit"]
draws = {r["scenario"]: [r["page"]["draws"], r["page"]["presents"]] for r in chrom["rows"]}
node_note = need(r"Node 20\.19\.5's V8 crashed compiling it \(GC fatal error\), Node 26\.7\.0 runs it", w0["notes"], "node")
w2a_load = need(r"Load ([0-9.–]+) s in Chromium, ([0-9.–]+) s in WebKit \(0\.33 s natively, ~0\.9 s under Node WASI\)", tvos_web, "w2a load")
hosts = [
    {"key": "tvos", "name": "Apple TV", "env": "симулятор Apple TV 4K, tvOS 27.0", "group": "coretext",
     "against": "приложение AppKit", "commit": "76c40436", "evidence": "tw-t1a-tvos-all-scenarios-20261011.json",
     "cells": rows_equal(tvos_rows), "frames": t1a_frames["frames"], "mismatched": t1a_frames["mismatched"],
     "note": "iOS-хост, собранный под tvOS; Core и Runtime не тронуты (T0)"},
    {"key": "wasi", "name": "WASI", "env": "Node " + wasi["rows"][0]["node"].lstrip("v") + " (тестовый стенд)", "group": "none",
     "against": "Mac headless", "commit": "6a17823c", "evidence": "tw-w0-w1-wasi-headless-20261011.json; повтор tw-w3e-wasi-lazy-packages-20261012.json",
     "cells": rows_equal(wasi["rows"]), "frames": wasi["frames"]["frames"], "mismatched": wasi["frames"]["mismatched"],
     "note": "NTSDHeadless.wasm, 96 МБ с отладочной информацией; Node 20 падал на компиляции модуля, Node 26 запускает"},
    {"key": "chromium", "name": "Chromium", "env": "headless Chromium 153 (Playwright)", "group": "none → свой текст",
     "against": "Mac headless (без текста)", "commit": "ce9b3c5f", "evidence": "tw-w2a … tw-w3f, web-text-20261013.json",
     "cells": rows_equal(chrom["rows"]), "frames": chrom["frames"]["frames"], "mismatched": chrom["frames"]["mismatched"],
     "note": "страница с canvas: нарисованы почти все кадры игры (" + "; ".join(f"{k} {v[0]} из {v[1]}" for k, v in draws.items() if k in ("vs", "tournament-win")) + ")"},
    {"key": "webkit", "name": "WebKit", "env": "WebKit из Playwright (движок Safari)", "group": "none → свой текст",
     "against": "Mac headless (без текста)", "commit": "ce9b3c5f", "evidence": "tw-w2a … tw-w3f, web-text-20261013.json",
     "cells": rows_equal(webk["rows"]), "frames": webk["frames"]["frames"], "mismatched": webk["frames"]["mismatched"],
     "note": "настоящий Safari и Firefox руками не проверялись"},
]
for h in hosts:
    assert all(v == "equal" for v in h["cells"].values()) and len(h["cells"]) == 10, h["key"]
# per-scenario details for the tooltips
per = {f["scenario"]: f for f in t1a["framesTvosAgainstAppKit"] if "scenario" in f}
hosts[0]["detail"] = {s: {"frames": per[s]["frames"], "digests": per[s]["digests"]["a"]} for s in scenarios}
hosts[1]["detail"] = {r["scenario"]: {"seconds": r["seconds"]} for r in wasi["rows"]}
for h, src in ((hosts[2], chrom), (hosts[3], webk)):
    h["detail"] = {r["scenario"]: {"seconds": r["seconds"], "presents": r["page"]["presents"], "draws": r["page"]["draws"]} for r in src["rows"]}
tf = text["checks"]["chromium"]["textFrames"]
dump("web_hosts.json", {
    "title": "Новые хосты против замороженных эталонов: 10 сценариев app_e2e и кадры",
    "source": "docs/evidence/tw-t1a-tvos-all-scenarios-20261011.json, tw-w0-w1-wasi-headless-20261011.json, tw-w3e-wasi-lazy-packages-20261012.json (повтор всех трёх веб-хостов), web-text-20261013.json, ws-s1-tvos-full-screen-20261013.json",
    "caveat": "симулятор — не Apple TV у телевизора; headless Chromium и WebKit из Playwright — не браузер игрока; WASI в Node — тестовый стенд",
    "frozen": FROZEN,
    "scenarios": scenarios,
    "hosts": hosts,
    "earlier": {"hosts": 9, "equal": 90, "of": 90, "source": "глава 13: crossplatform-matrix-20261005-speed.json"},
    "loadSeconds": {"chromium": w2a_load.group(1), "webkit": w2a_load.group(2), "native": 0.33, "wasi": 0.9,
                    "source": "TVOS_WEB.md, строка W2a"},
    "text": {"commit": "f0471f13", "frames": tf["frames"], "text": tf["text"], "textless": tf["textless"],
             "disagree": tf["disagree"], "enginesDiffer": text["engines"]["chromiumVsWebkit"]["mismatched"],
             "font": "bold 13px, системный UI-шрифт платформы (SF, Segoe UI, Roboto …)",
             "how": text["textFramesHow"]},
    "tvosRerun": {"commit": "f075d765", "frames": s1["scenarios"]["framesAgainstAppKit"]["frames"],
                  "mismatched": s1["scenarios"]["framesAgainstAppKit"]["mismatched"]},
    "minutes": {
        "tvosFirst": round((datetime.fromisoformat(next(s["time"] for s in steps if s["step"] == "T0")) - t0).total_seconds() / 60),
        "tvosAll": round((datetime.fromisoformat(next(s["time"] for s in steps if s["step"] == "T1a")) - t0).total_seconds() / 60),
        "wasiAll": round((datetime.fromisoformat(next(s["time"] for s in steps if s["step"] == "W0, W1")) - t0).total_seconds() / 60),
        "from": steps[0]["time"],
    },
})

# ------------------------------------------------------------------ frame time (W3a)
w3a = evidence("tw-w3a-browser-frame-time-20261012.json")
med = w3a["medians"]
rows = []
for key, label, like, note in [
    ("mac", "Mac · игровой поток", False, "отрисовка идёт рядом, в потоке рендера"),
    ("mac-cpu", "Mac · CPU всех потоков", False, "сумма по потокам, с очередями и пересылками"),
    ("chromium", "Chromium", True, "один поток: тик и отрисовка подряд"),
    ("macsync", "Mac · --synchronous-render", True, "отрисовка в том же потоке, как в wasm"),
    ("webkit", "WebKit", True, "один поток"),
    ("wasi", "Node WASI", True, "один поток, без страницы"),
]:
    src = "mac" if key == "mac-cpu" else key
    field = "processMsPerTick" if key == "mac-cpu" else "completeMsPerTick"
    rows.append({"key": key, "label": label, "likeForLike": like, "note": note,
                 "vs": round(med["vs"][src][field], 2), "demo": round(med["demo"][src][field], 2),
                 "startedToLoaded": med["vs"][src]["startedToLoadedSeconds"]})
dump("web_frametime.json", {
    "title": "Время на тик: браузер, WASI и Mac (медианы трёх прогонов)",
    "source": "docs/evidence/tw-w3a-browser-frame-time-20261012.json (medians), коммит ef6e880a; вопрос автора и ответ агента — журнал сессии 1f9218ae, 12 октября 17:36–17:37",
    "caveat": w3a["comparison"],
    "how": w3a["how"],
    "frozen": FROZEN,
    "rows": rows,
    "budgetMs": {"fps60": 16.67, "originalTick": 33},
    "linearMemoryMiB": w3a["linearMemoryMiB"]["values"],
})

# ------------------------------------------------------------------ delivery (W2b-4c, W3b, W3c, W3e, W3f)
w2b4c = evidence("tw-w2b4c-browser-static-20261012.json")
w3b = evidence("tw-w3b-browser-compressed-20261012.json")
w3c = evidence("tw-w3c-browser-startup-20261012.json")
w3f = evidence("tw-w3f-browser-prefetch-overlap-20261012.json")
rel = evidence("release-refresh-20261013.json")

meas = w2b4c["firstLoad"]["measure"]
kinds = meas["byKind"]
names = {".bmp": "картинки BMP", "program": "программа .wasm", ".dib": "картинки DIB", ".caf": "музыка меню (ALAC)",
         ".wav": "звуки WAV", ".wma": "WMA", ".dat": "данные .dat"}
parts = []
rest = {"files": 0, "bytes": 0, "brotli11": 0, "gzip6": 0}
for k, v in sorted(kinds.items(), key=lambda kv: -kv[1]["bytes"]):
    if k in names:
        parts.append({"key": k, "label": names[k], "files": v["files"], "MB": mb(v["bytes"]),
                      "brotliMB": mb(v["brotli11"]), "gzipMB": mb(v["gzip6"])})
    else:
        for f in rest:
            rest[f] += v[f]
parts.append({"key": "other", "label": "остальное", "files": rest["files"], "MB": mb(rest["bytes"]),
              "brotliMB": mb(rest["brotli11"]), "gzipMB": mb(rest["gzip6"])})

runs_b = w3b["firstVisits"]["runs"]
unthr_b = w3b["unthrottledFirstFrames"]["ms"]
runs_f = w3f["firstVisits"]["runs"]
e_ff = w3e["startup"]["staticFirstFrameMs"]


def model(label, short, step, commit, t100, tinf, wire, note):
    eff = round((t100 - tinf) * 100 / 8, 1)  # MB that must arrive before the first frame, from the slope
    return {"label": label, "short": short, "step": step, "commit": commit, "firstFrame100": t100,
            "firstFrameLocal": tinf, "wireMB": wire, "effectiveMB": eff, "note": note}


configs = [
    model("как было: файлы без сжатия", "без сжатия", "W3b", "5d24e399",
          runs_b["plain-100-chromium"]["firstFrameSeconds"],
          round(median([unthr_b[f"plain-{i}"] for i in (1, 2, 3)]) / 1000, 2), runs_b["plain-100-chromium"]["wireMB"],
          "программа ждёт все файлы, читает и хеширует их до меню"),
    model("сжатие brotli", "brotli", "W3b", "5d24e399",
          runs_b["packed-100-chromium"]["firstFrameSeconds"],
          round(median([unthr_b[f"packed-{i}"] for i in (1, 2, 3)]) / 1000, 2), runs_b["packed-100-chromium"]["wireMB"],
          "байты те же после распаковки; распаковка стоит ≈ 0,7 с"),
    model("меню раньше + подкачка", "меню раньше", "W3e + W3f", "9d7beb8a",
          median(runs_f["plain-100-chromium"]["firstFrameSeconds"]),
          median(runs_f["plain-none-chromium"]["firstFrameSeconds"]), runs_f["plain-100-chromium"]["wireMB"],
          "пакеты считаются при первой загрузке, страница качает файлы, пока программа стартует"),
    model("brotli + меню раньше + подкачка", "всё вместе", "W3b + W3e + W3f", "9d7beb8a",
          median(runs_f["packed-100-chromium"]["firstFrameSeconds"]),
          median(runs_f["packed-none-chromium"]["firstFrameSeconds"]), runs_f["packed-100-chromium"]["wireMB"],
          "все данные на месте к 8,5 с; первый кадр — 5,6 с"),
]
attr = w3c["attribution"]
sha = float(need(r"~([0-9.]+) s on SHA-256", attr, "sha").group(1))
wait = float(need(r"~([0-9.]+) s waiting for the prefetch", attr, "wait").group(1))
reads = float(need(r"~([0-9.]+) s in its synchronous reads from the cache", attr, "reads").group(1))
lz4 = float(need(r"~([0-9.]+) s in LZ4", attr, "lz4").group(1))
digested = float(need(r"every packaged file, ([0-9.]+) MB, digested", attr, "digested").group(1))
ff_static = float(need(r"first frame ([0-9.]+) s", w3c["profiles"]["chromiumStatic"]["how"], "static first frame").group(1))
menu_needs = float(need(r"the menu needs the ([0-9.]+) MB startup package", " ".join(w3c["levers"]), "menu").group(1))
host_line = need(r"\*\*Hosting \(user, 2026-10-11\):\*\*(.*?)\*\*Game result", tvos_web, "hosting").group(1).strip()
tiers = need(r"checked 2026-10-11: (Vercel Hobby [^;]+); (Cloudflare R2 [^;]+); (Cloudflare Pages [^)]+)\)", host_line, "tiers")
dump("web_delivery.json", {
    "title": "Первый визит в браузере: что скачивается и когда появляется меню",
    "source": "docs/evidence/tw-w2b4c-browser-static-20261012.json (firstLoad.measure), tw-w3b-browser-compressed-20261012.json, tw-w3c-browser-startup-20261012.json, tw-w3e-wasi-lazy-packages-20261012.json, tw-w3f-browser-prefetch-overlap-20261012.json; TVOS_WEB.md (Hosting); release-refresh-20261013.json (web)",
    "caveat": "локальный тестовый сервер web_app.py serve с --rate 100 (только полоса, без задержек сети): времена — нижние границы; Chromium 153 headless на этом Mac, три холодных визита на точку; WebKit по HTTP не берёт brotli (gzip, 120,9 МБ)",
    "frozen": FROZEN,
    "total": {"files": meas["total"]["files"], "MB": mb(meas["total"]["bytes"]), "brotliMB": mb(meas["total"]["brotli11"]),
              "gzipMB": mb(meas["total"]["gzip6"]), "requests": meas["requests"]},
    "programMB": mb(w2b4c["build"]["programBytes"]),
    "parts": parts,
    "wire": {"plain": runs_b["plain-100-chromium"]["wireMB"], "brotliChromium": runs_b["packed-100-chromium"]["wireMB"],
             "gzipWebkit": runs_b["packed-100-webkit"]["wireMB"]},
    "configs": configs,
    "model": {"derived": "t(полоса) = t(локально) + effectiveMB × 8 / полоса — прямая через два замера каждой конфигурации (без ограничения и 100 Мбит/с); между ними и ниже 100 Мбит/с — оценка, не замер",
              "measuredMbit": 100},
    "startup": {"firstFrame": ff_static, "sha256": sha, "prefetchWait": wait, "cacheReads": reads, "lz4": lz4,
                "other": round(ff_static - sha - wait - reads - lz4, 1), "digestedMB": digested, "menuNeedsMB": menu_needs,
                "after": round(median([e_ff[f"after-{i}"] for i in (1, 2, 3)]) / 1000, 2),
                "before": round(median([e_ff[f"before-{i}"] for i in (1, 2, 3)]) / 1000, 2),
                "source": "tw-w3c (профиль воркера, статическая страница, данные в кэше) · tw-w3e (первый кадр, 3 холодных визита)"},
    "hosting": {"checked": "2026-10-11", "tiers": [tiers.group(1), tiers.group(2), tiers.group(3)],
                "plan": "автор: тестировать локально; публиковать позже на Vercel, бесплатно или с минимальным счётом",
                "rights": "данные — файлы оригинальной игры: публиковать их — решение автора; страница, открывающая копию игрока, их не распространяет"},
    "release": {"tag": rel["tag"], "archive": rel["web"]["archive"], "hosting": rel["web"]["hosting"],
                "commit": "0b5d4621", "date": "2026-10-13 15:28"},
})

# ------------------------------------------------------------------ window (S1–S6)
s2 = evidence("ws-s2-browser-original-window-20261013.json")
s3 = evidence("ws-s3-macos-scalable-window-20261013.json")
s4 = evidence("ws-s4-sdl-scalable-window-20261013.json")
s5 = evidence("ws-s5-ipad-android-20261013.json")
w2b4b = evidence("tw-w2b4b-browser-page-20261012.json")
fit_sizes = w2b4b["fitting"]["sizes"]
r1 = s1["screenshots"]["results"]


def box(name):
    return r1[name]["boxSize"]


canv = [json.loads(x.rsplit(" = ", 1)[1]) for x in s2["checks"]["runner"]["logs"] if x.startswith("(() =>")]
fs = [json.loads(x.rsplit(" = ", 1)[1]) for x in s2["checks"]["runner"]["logs"] if x.startswith("[!!document.fullscreenElement")]
a12 = {}
for line in s5["checks"]["devices"]["lines"]:
    m = re.match(r"(\S+) (fit|orig) screen (\d+)x(\d+) .*box=(\{.*\})", line)
    if m:
        a12[(m.group(1), m.group(2))] = json.loads(m.group(5))["boxSize"]
static_fit = s2["checks"]["staticPage"]["results"]["?"]
x11 = s4["checks"]["linuxScaling"]["summary"]["x11"]
mac_live = s3["checks"]["live"]
fs_lines = [json.loads(x) for x in mac_live["lines"] if x.startswith("{")]
presets = [
    {"key": "tv1080", "name": "Apple TV · 1080p", "unit": "pt", "screen": [1920, 1080], "scale": 1, "windowed": False,
     "measured": {"fit": box("fit-1080"), "orig": box("orig-1080")}, "evidence": "ws-s1-tvos-full-screen-20261013.json", "commit": "f075d765",
     "where": "симулятор Apple TV 4K (3-е поколение) в режиме 1080p"},
    {"key": "tv4k", "name": "Apple TV · 4K", "unit": "pt", "screen": [1920, 1080], "scale": 2, "windowed": False,
     "measured": {"fit": box("fit-4k"), "orig": box("orig-4k")}, "evidence": "ws-s1-tvos-full-screen-20261013.json", "commit": "f075d765",
     "where": "симулятор Apple TV 4K, 3840×2160 px"},
    {"key": "mac", "name": "Mac · окно", "unit": "pt", "screen": [3008, 1692], "scale": 2, "windowed": True, "window": [1588, 1100],
     "measured": {"fit": [1588 * 2, 1100 * 2], "orig": [794 * 2, 550 * 2]}, "evidence": "ws-s3-macos-scalable-window-20261013.json", "commit": "b7cd16c6",
     "where": "дисплей Apple 6K, 3008×1692 pt: окно открывается в 2× — 1588×1100 pt; с флагом — 794×550"},
    {"key": "macfs", "name": "Mac · полный экран", "unit": "pt", "screen": [3008, 1692], "scale": 2, "windowed": False,
     "measured": {"fit": [4886, 3384]}, "evidence": "ws-s3-macos-scalable-window-20261013.json", "commit": "b7cd16c6",
     "where": "зелёная кнопка: клиент " + "×".join(map(str, fs_lines[0]["client"])) + " pt, картинка 4886×3384 px по центру"},
    {"key": "x11", "name": "Linux · окно X11", "unit": "px", "screen": [1920, 1080], "scale": 1, "windowed": True, "window": [1325, 918],
     "measured": {"fit": [1325, 918], "orig": [794, 550]}, "evidence": "ws-s4-sdl-scalable-window-20261013.json", "commit": "d45fd928",
     "where": "Xvfb 1920×1080 без оконного менеджера: окно " + x11["window"][0].replace("first ", "").replace(" ", "×") + ", потом " + x11["window"][1].replace("resized ", "").replace(" ", "×") + "; клики xdotool"},
    {"key": "a12", "name": "Galaxy A12", "unit": "px", "screen": [1600, 720], "scale": 1, "windowed": False,
     "measured": {"fit": a12[("R58R36F7VFD", "fit")], "orig": a12[("R58R36F7VFD", "orig")]}, "evidence": "ws-s5-ipad-android-20261013.json", "commit": "f7aeada1",
     "where": "настоящий телефон, 1600×720 px; по умолчанию масштабирует компоновщик Android (с фильтрацией); флаг — пиксель в пиксель устройства"},
    {"key": "web1600", "name": "Браузер · 1600×900", "unit": "px", "screen": [1600, 900], "scale": 1, "windowed": True, "window": [1600, 900],
     "measured": {"fit": [round(v, 1) for v in fit_sizes["1600x900"]["canvasBox"][:2]], "orig": canv[0][:2]},
     "evidence": "tw-w2b4b-browser-page-20261012.json (fit), ws-s2-browser-original-window-20261013.json (флаг)", "commit": "4f678fa7, 71e5243a",
     "where": "headless Chromium, окно 1600×900: canvas 1299×900; с флагом — 794×550 по центру (403, 175); полный экран с флагом — снова 1299×900"},
    {"key": "web400", "name": "Браузер · 400×600", "unit": "px", "screen": [400, 600], "scale": 1, "windowed": True, "window": [400, 600],
     "measured": {"fit": [round(v, 1) for v in fit_sizes["400x600"]["canvasBox"][:2]], "orig": canv[3][:2]},
     "evidence": "tw-w2b4b-browser-page-20261012.json (fit), ws-s2-browser-original-window-20261013.json (флаг)", "commit": "4f678fa7, 71e5243a",
     "where": "с флагом окно меньше кадра: картинка уменьшается до 400×277, не обрезается"},
]
# the browser's fit in an 800x600 viewport, from the static page check
browser800 = {"viewport": static_fit[3:5], "fit": static_fit[1:3]}
pointer_sizes = re.findall(r"(\d+x\d+)", w2b4b["pointerMapping"]["how"])
flags = []
tab = need(r"\| Host \| Default \| Original window \| Full screen \|(.*?)Common rules", scaling, "flags table").group(1)
for row in re.findall(r"\| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|", tab):
    if row[0].strip().startswith("---"):
        continue
    flags.append({"host": row[0].strip(), "default": row[1].strip(), "original": row[2].strip(), "fullScreen": row[3].strip()})
uneven = need(r"\(1\.96× at 1080p, 3\.93× at 4K\) gives uneven pixels \(at 1080p (\d+) rows and (\d+) columns 1 px narrower\)", s1["scaling"], "uneven")
mac_perf = s3["checks"]["performance"]
dump("web_window.json", {
    "title": "Масштабируемое окно: замеренные размеры картинки на хостах",
    "source": "docs/research/WINDOW_SCALING.md (Flags and controls), docs/evidence/ws-s1 … ws-s6 (13 октября)",
    "caveat": "Apple TV и iPad — симуляторы; браузер — headless Chromium; Linux — Xvfb и Weston в контейнере; Mac и Galaxy A12 — настоящие; Windows SDL не собиралась",
    "frozen": FROZEN,
    "game": [794, 550],
    "presets": presets,
    "browser800": browser800,
    "pointer": {"sizes": pointer_sizes, "exact": w2b4b["pointerMapping"]["exact"],
                "pixels": [[0, 0], [350, 230], [793, 549], [400, 275]], "source": "tw-w2b4b-browser-page-20261012.json (pointerMapping)"},
    "uneven1080": {"rows": int(uneven.group(1)), "columns": int(uneven.group(2)),
                   "derived": "в компоненте: при масштабе между k и k+1 исходных пикселей шириной k ровно (k+1)·n − m; для 1080p это совпадает с замером"},
    "flags": flags,
    "macAB": {"msPerTick": "2.02 vs 1.74", "peakMB": "799 vs 692 (vs)", "source": "WINDOW_SCALING.md, строка S3"},
    "linuxResized": x11["window"][1],
    "wayland": s4["checks"]["linuxScaling"]["summary"]["wayland"]["fullScreen"],
    "openQuestions": [
        "растянуть или обрезать картинку на 16:9 — исказит или срежет оригинал: решать автору",
        "сглаживание при нецелом масштабе размоет пиксели: тоже выбор автора",
    ],
})
print("collect_web: wrote web_steps, web_hosts, web_frametime, web_delivery, web_window "
      f"({len(steps)} commits, {round((t1 - t0).total_seconds() / 3600, 1)} h)")
