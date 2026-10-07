#!/usr/bin/env python3
"""Regenerate the deck's data/perf_*.json (chapter 14, «Телефон 2008 года»)
from the NTSD port repository.

Usage:
    python3 scripts/collect_perf.py ../ntsd-2.4 [REV]

REV defaults to 8840eb3 (branch exp/core-realtime, 7 Oct 2026, 08:23), the
commit the chapter is frozen at. Every number is read with
`git show REV:path`, so later commits do not change the output. The only
exception is `afterFreeze` (and `renderPassesPlan`) in perf_now.json: steps
that were in flight at REV and landed later on exp/core-realtime, read from
the commits that added their evidence; the slide shows them apart from the
frozen numbers.

Nothing in the source repository is modified: only `git show`, `git log`,
`git rev-list`.
"""
import json
import os
import re
import subprocess
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../ntsd-2.4")
REV = sys.argv[2] if len(sys.argv) > 2 else "8840eb3"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
FROZEN = "состояние на 7 октября 2026, 08:23 (8840eb3)"
EV = "docs/evidence/"
RS = "docs/research/"


def git(*args):
    res = subprocess.run(["git", "-C", REPO, *args], check=True, capture_output=True)
    return res.stdout.decode("utf-8", "replace")


def show(path):
    return git("show", f"{REV}:{path}")


def evidence(name):
    return json.loads(show(EV + name))


def added_in(path):
    """Short hash of the commit (up to REV) that added a file."""
    out = git("log", REV, "--diff-filter=A", "--format=%h", "--", path).split()
    return out[-1] if out else None


def dump(name, obj):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def num(s):
    return float(s.replace(",", ""))


def need(pattern, text, what):
    m = re.search(pattern, re.sub(r"\s+", " ", text))  # Markdown wraps lines; match across them
    if not m:
        raise SystemExit(f"collect_perf: cannot find {what!r} ({pattern})")
    return m


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 3) if xs else None


# ------------------------------------------------------------------ memory
phone = evidence("crossplatform-p8-android-phone-20261005.json")
foot = evidence("crossplatform-memory-footprint-20261005.json")
attr = evidence("crossplatform-memory-attribution-20261005.json")
mem1 = evidence("crossplatform-memory-step1-20261005.json")
mem2 = evidence("crossplatform-memory-step2-20261005.json")
mem3 = evidence("crossplatform-memory-step3-20261005.json")

kill = phone["finding 2: memory"]
lmk = need(r"lmkd: '([^']+)'", kill, "lmkd line").group(1)
mem_total_kb = int(need(r"MemTotal (\d+) kB", phone["device"], "MemTotal").group(1))
mac_peak = int(need(r"peak memory footprint ([\d,]+) bytes", phone["macOS comparison"], "mac peak").group(1).replace(",", ""))
live_gib = num(need(r"([\d.]+) GiB", attr["live heap"], "live heap").group(1))

GROUPS = [  # (substring of the allocation site, group id); first match wins
    ("Storage.init :68", "surface"),
    ("Storage.init :69", "known"),
    ("OriginalDIBPixels.init", "decoded"),
    ("Array copy in Bitmap.init", "filebytes"),
    ("OriginalStateRecord.write", "records"),
    ("OriginalFrameLoader.projected", "frames"),
    ("OriginalMacAudioBackend", "sounds"),
    ("StartupInputs.load read", "startup"),
]
NAMES = {
    "surface": ("пиксели 851 поверхности дисплея", True),
    "decoded": ("декодированные цвета битмапов", True),
    "filebytes": ("байты файлов картинок, копия", True),
    "known": ("маска «known», байт на пиксель", True),
    "records": ("записи состояния", False),
    "frames": ("словари загрузчика кадров", False),
    "sounds": ("звуки", False),
    "startup": ("чтение стартовых файлов", False),
    "other": ("прочее", False),
}
mib = {}
for h in attr["top holders (innermost game frames)"]:
    gid = next((g for s, g in GROUPS if s in h["site"]), "other")
    mib[gid] = mib.get(gid, 0) + h["MiB"]
mib["other"] = round(live_gib * 1024) - sum(mib.values())
holders = [{"id": g, "label": NAMES[g][0], "image": NAMES[g][1], "MiB": mib[g]}
           for g in ["surface", "decoded", "filebytes", "known", "records", "frames", "sounds", "startup", "other"]]

steps = [
    {"n": 1, "hash": added_in(EV + "crossplatform-memory-step1-20261005.json"),
     "what": "картинка не хранит декодированную копию",
     "metric": "живая куча", "before": num(need(r"~([\d.]+) GB", mem1["memory"]["before"], "m1 before").group(1)),
     "after": num(need(r"([\d.]+) GB", mem1["memory"]["after"], "m1 after").group(1))},
    {"n": 2, "hash": added_in(EV + "crossplatform-memory-step2-20261005.json"),
     "what": "маска «known» битами, а не байтами",
     "metric": "живая куча", "before": num(need(r"from ([\d.]+) GB", mem2["memory"]["live heap at 40 s"], "m2 before").group(1)),
     "after": num(need(r"^([\d.]+) GB", mem2["memory"]["live heap at 40 s"], "m2 after").group(1))},
]
m3 = mem3["memory (macOS headless, vmmap DefaultMallocZone dirty+swapped)"]
steps.append({"n": 3, "hash": added_in(EV + "crossplatform-memory-step3-20261005.json"),
              "what": "поверхность заполняется при первом обращении",
              "metric": "резидентная куча", "before": num(need(r"~([\d.]+) GB", m3["before"], "m3 before").group(1)),
              "after": num(need(r"^([\d.]+) GB", m3["after"], "m3 after").group(1))})
p3 = mem3["phone (Galaxy A12, 2.8 GB RAM, debug APK with steps 1-3)"]
phone_after = {
    "scriptedSeconds": int(need(r"in (\d+) s", p3["scripted vs"], "scripted s").group(1)),
    "emulatorSeconds": int(need(r"emulator (\d+) s", p3["scripted vs"], "emu s").group(1)),
    "frames": int(need(r"all ([\d,]+) frames identical", p3["scripted vs"], "frames").group(1).replace(",", "")),
    "loadingSeconds": int(need(r"~(\d+) s of loading", p3["interactive"], "loading").group(1)),
    "peakRssGB": num(need(r"peak RSS ([\d.]+) GB", p3["speed"], "peak rss").group(1)),
    "ticksPerSecond": need(r"([\d.]+-[\d.]+) gameplay ticks", p3["speed"], "tps").group(1),
}
dump("perf_memory.json", {
    "title": "Память игры на Galaxy A12 и на macOS: убийство на загрузке, куда уходит куча, три шага хранения",
    "source": "ntsd-2.4 at %s: %scrossplatform-p8-android-phone-20261005.json, crossplatform-memory-footprint-20261005.json, "
              "crossplatform-memory-attribution-20261005.json, crossplatform-memory-step{1,2,3}-20261005.json, %sMEMORY_FOOTPRINT.md" % (REV, EV, RS),
    "caveat": "Holders are malloc_history stacks at a 3.6 GB footprint of the macOS headless run (live heap 3.84 GiB); 'other' is the rest of "
              "that live heap. Steps 1-2 are measured as live heap (heap -s), step 3 as resident heap (vmmap dirty+swapped): two metrics, "
              "not one series. The macOS footprint varied 1.4-3.1 GB between identical runs and is not used to compare steps.",
    "rev": REV,
    "phone": {"device": "Samsung Galaxy A12 (SM-A125F), Android 12", "memTotalKB": mem_total_kb,
              "memTotalMiB": round(mem_total_kb / 1024), "lmkd": lmk,
              "residentGB": num(need(r"rose to ([\d.]+) GB", kill, "resident").group(1)),
              "availableMB": int(need(r"~(\d+) MB", kill, "available").group(1))},
    "macPeakFootprintBytes": mac_peak,
    "liveHeapMiB": round(live_gib * 1024),
    "mappedFilesMB": num(need(r"mapped files ([\d.]+) ?M", foot["footprint"]["vmmap"], "mapped").group(1)),
    "holders": holders,
    "steps": steps,
    "phoneAfter": phone_after,
})

# ------------------------------------------------------------------ local speed steps (5 Oct, dev/crossplatform)
mp = show(RS + "MOBILE_PERFORMANCE.md")
rows = re.findall(r"^\| Galaxy A12(?:, vs script, no frame capture| after ([^|]+?)) \| \**([\d.]+)\** \|", mp, re.M)
step8 = evidence("crossplatform-speed-step8-20261006.json")
s8 = need(r"([\d.]+) -> ([\d.]+) ticks", step8["phone"]["speed (vs script, no frame capture)"], "step 8")
local_hash = {"steps 1–2": "crossplatform-speed-steps12-20261005.json", "step 3": "crossplatform-speed-step3-20261005.json",
              "steps 3–4": "crossplatform-speed-steps45-20261005.json", "steps 3–5": "crossplatform-speed-steps45-20261005.json",
              "step 6": "crossplatform-speed-step6-20261005.json", "step 6b": "crossplatform-speed-step6b-20261005.json",
              "step 7": "crossplatform-speed-step7-20261005.json"}
local_what = {"": "после шагов памяти 1–3", "steps 1–2": "скан экрана на неизвестные пиксели — сразу выход",
              "step 3": "буфер повтора 6,5 МБ страницами по 16 КиБ", "steps 3–4": "копирование спрайтов по строкам",
              "steps 3–5": "биты маски словами по 64", "step 6": "диапазоны адресов в локальном массиве",
              "step 6b": "токены звука без склейки списков", "step 7": "целые строки экрана одним блоком"}
local = []
for after, v in rows:
    key = after.strip()
    local.append({"step": key or "start", "what": local_what[key], "ticksPerSecond": float(v),
                  "hash": added_in(EV + local_hash[key]) if key in local_hash else added_in(EV + "crossplatform-memory-step3-20261005.json")})
local.append({"step": "step 8", "what": "запись меню перезаписывается на месте", "ticksPerSecond": float(s8.group(2)),
              "hash": added_in(EV + "crossplatform-speed-step8-20261006.json"), "noise": True})
cow = evidence("crossplatform-speed-steps12-20261005.json")["copy-on-write probe (temporary, not committed; headless vs run, all records copied by OriginalStateRecord.write)"]
probe = []
for k, label in [("0x630e18 bytes (replay recording buffer)", "буфер записи повтора, 6,5 МБ"), ("0x420 bytes (actors)", "записи актёров, 1 КБ"),
                 ("0x1f50 bytes", "записи ресурсов битмапов, 8 КБ"), ("0xb440 bytes (globals)", "глобальные переменные, 45 КБ")]:
    s = cow[k]
    m = need(r"^([\d,.]+)( million|)? copies.*?~([\d.]+) GB", s, k)
    copies = num(m.group(1)) * (1e6 if m.group(2) else 1)
    probe.append({"what": label, "copies": int(copies), "GB": float(m.group(3))})
dump("perf_local.json", {
    "title": "Восемь локальных ускорений на Galaxy A12, 5 октября: тики в секунду по шагам",
    "source": "ntsd-2.4 at %s: %sMOBILE_PERFORMANCE.md (Measurements), %scrossplatform-speed-*.json; hashes = commits that added each evidence file" % (REV, RS, EV),
    "caveat": "android_speed predecessor: scripted computer-vs match on one phone, bodies 300->1800, no frame capture, virtual clock. "
              "Step 8 (10.2 -> 10.1) is within run-to-run noise by the evidence's own words. The copy probe is a temporary macOS headless "
              "probe before step 3, not committed code.",
    "rev": REV,
    "gameRate": 30,
    "steps": local,
    "copyProbe": probe,
})

# ------------------------------------------------------------------ redesign ledger (6-7 Oct, exp/core-realtime)
card = show(RS + "CORE_REALTIME.md")
ledger = re.findall(r"^\| (2026-10-0\d) \| ([^|]+?) \| (.+?) \| (\[evidence\]\(\.\./evidence/(rt-[\w-]+\.json)\)[^|]*|—) \| ([^|]+?) \|$", card, re.M)
LABEL = {  # short Russian names for the slide; numbers come from the evidence files
    "0": "старт ветки", "1a": "окно Android одним SIMD-проходом", "2a": "кэши на сессию", "2b": "пары записей актёров",
    "1c": "рисование в отдельном потоке", "1d": "заливка строками", "1e": "текст без ожидания рендера",
    "2c": "записи ресурсов на сессию", "2d": "запись без изменений не копирует", "4a": "данные сессии в одном объекте",
    "4b": "графика на месте", "4c": "чтение целых через буфер", "M2a": "запросы очереди внутри попытки",
    "M2b": "очистка буфера внутри попытки", "1f": "очистка буфера в потоке рендера", "R3": "400 актёров в форме модели",
    "1g": "флаг «все пиксели известны»", "4d": "без событий, которые никто не слушает", "4e": "таблица ГСЧ одной копией",
    "4f": "вход презентации без JSON", "4g": "одна валидация на рисунок", "A0": "без лишней копии при коммите",
    "A1": "лёгкое ядро холостой итерации", "1i": "буферы crop переиспользуются", "4h": "маски глифов по строке",
    "3a": "запись из частей (без включения)", "3b": "состояние меню из частей", "4i": "проверки битмапов на сессию",
    "4j": "пары актёров одним проходом", "4k": "cross-module optimization", "4l": "загрузка в одном объекте",
}
AREA = {"1a": "render", "1c": "render", "1d": "render", "1e": "render", "1f": "render", "1g": "render", "1i": "render",
        "4h": "render", "2a": "state", "2b": "state", "2c": "state", "2d": "state", "R3": "state", "4c": "state",
        "4e": "state", "3a": "state", "3b": "state", "4i": "state", "4j": "state", "4a": "copies", "4b": "copies",
        "4l": "copies", "M2a": "host", "M2b": "host", "4d": "host", "4f": "host", "4g": "host", "A0": "host", "A1": "host",
        "4k": "compiler", "0": "start"}


def step_id(name):
    m = re.match(r"(?:Phase |R3 stage |B1 )?([0-9][a-z]?|M2[ab]|A0|A1)\b", name)
    if name.startswith("R3 stage 1"):
        return "R3"
    return m.group(1) if m else None


def runs(ev):
    """(before, after) phone runs of an evidence file, each a list of dicts."""
    ph = ev.get("phone") or {}
    if "speed" in ev and "phone" not in ev:          # the baseline
        return [], [ev["speed"]]
    after = ph.get("after", [])
    after = [after] if isinstance(after, dict) else after
    before = ph.get("before", [])
    before = [before] if isinstance(before, dict) else before
    return before, after


def virtual(rs):
    return [r for r in rs if isinstance(r, dict) and r.get("bodies", 1800) == 1800 and "real" not in r.get("label", "")]


def real(rs):
    return [r for r in rs if isinstance(r, dict) and "real" in r.get("label", "")]


def summarize(rs):
    return {"ticksPerSecond": mean([r.get("ticksPerSecond") for r in rs]),
            "mainMs": mean([r.get("mainMsPerTick") for r in rs]),
            "renderMs": mean([r.get("renderMsPerTick") for r in rs]),
            "menuMsPerStep": mean([r.get("menuMsPerStep") for r in rs]),
            "runs": len(rs)}


ladder, gates = [], []
for date, name, result, evcell, evfile, commit in ledger:
    sid = step_id(name.strip())
    if sid is None:
        continue
    ev = evidence(evfile)
    before, after = runs(ev)
    v = summarize(virtual(after))
    commit = commit.strip()
    if not re.fullmatch(r"[0-9a-f]{7,}", commit):
        commit = added_in(EV + evfile)
    entry = {"id": sid, "date": date, "label": LABEL.get(sid, name), "area": AREA.get(sid, "other"),
             "hash": commit, "evidence": evfile, **v}
    rr = real(after)
    if rr:
        entry["realClock"] = summarize(rr)
    for key, note in (("tried_1h", "1h: копии с ключом по 4 пикселя (SIMD) — без выигрыша, откат"),
                      ("rejected_first_version", "первая версия 3a: лишнее поле, запись 48 байт вместо 40 — переделано")):
        if key in ev:
            entry["rejected"] = {"note": note, **summarize(virtual(ev[key].get("phone", [])))}
    if sid == "1g":  # main thread unchanged; the evidence gives render-thread samples per main-thread sample
        rm = need(r"render/main samples (0\.\d+) \([^)]*\) -> (0\.\d+)", json.dumps(ev), "1g render")
        entry["renderToMain"] = [float(rm.group(1)), float(rm.group(2))]
    ladder.append(entry)
    if sid == "0":
        continue
    # gates: what each increment was checked with (from the evidence's own gates/checks/review fields)
    g = ev.get("gates") or {}
    blob = json.dumps(g)
    rev = ev.get("review")
    rtext = rev if isinstance(rev, str) else json.dumps(rev) if rev else ""
    if not rtext:
        review = "none"
    elif rtext.startswith("not required"):
        review = "na"
    else:
        review = "pass"
    checks = ev.get("checks") or {}
    gates.append({
        "id": sid, "hash": commit, "label": entry["label"],
        "headless": "pass" if "vs equal" in json.dumps(g.get("headless", "")) else ("na" if sid == "1a" else "none"),
        "scenarios": "pass" if ("all 10" in blob) else ("na" if sid == "1a" else "none"),
        "appkit": "pass" if "3,960 frames identical" in json.dumps(g.get("AppKit", "")) else ("na" if sid == "1a" else "none"),
        "emulator": "pass" if ("emulator" in g or "Android" in g or "emulator" in checks) else "none",
        "suites": "pass" if ("Core suites" in g or "tests" in g or "swap equivalence" in checks) else "none",
        "tsan": "pass" if "ThreadSanitizer" in g else "na",
        "phone": "pass" if after else "none",
        "review": review,
        "reviewNote": rtext[:200],
    })

real_points = [{"id": e["id"], **e["realClock"]} for e in ladder if "realClock" in e]
dump("perf_ladder.json", {
    "title": "Редизайн ядра на Galaxy A12, 6–7 октября: каждая ступень реестра CORE_REALTIME с замерами телефона",
    "source": "ntsd-2.4 at %s: %sCORE_REALTIME.md (Ledger) and the evidence file named in each row (%srt-*.json)" % (REV, RS, EV),
    "caveat": "One phone (Galaxy A12 R58R36F7VFD), debuggable build, scripted computer-vs match with music, sounds and network off, no frame "
              "capture. ticksPerSecond = mean of the virtual-clock runs (8 ms per message-loop iteration: every tick sleeps ~16 ms of the "
              "original's own pacing, so it undercounts compute savings). mainMs/renderMs = compute per gameplay tick per thread from "
              "schedstat (bodies 600-1500), measured from phase 4f on. realClock = the same match with --real-clock. Several steps are "
              "within run-to-run noise by their own evidence. " + FROZEN,
    "rev": REV,
    "steps": ladder,
    "realClock": real_points,
})

# ------------------------------------------------------------------ gates
mx = evidence("crossplatform-matrix-20261005-speed.json")
hosts = mx["hosts"]
scen = sorted({s for h in hosts.values() for s in h["equal"]} | {s for h in hosts.values() for s in h["differs"]})
branch_matrix = [p for p in git("log", "--format=", "--name-only", f"36edf83^..{REV}", "--", EV).split() if "matrix" in p]
dump("perf_gates.json", {
    "title": "Чем проверена каждая ступень редизайна: ворота из evidence-файлов",
    "source": "ntsd-2.4 at %s: %srt-*.json (fields gates, checks, review, phone), %sCORE_REALTIME.md (Gates); matrix: %scrossplatform-matrix-20261005-speed.json" % (REV, EV, RS, EV),
    "caveat": "pass = the evidence records the check passing; na = recorded as not required or not applicable (1a is Android-only; "
              "ThreadSanitizer only for threading changes); none = not in the evidence. The nine-host matrix ran on 5 Oct at %s, "
              "before the redesign branch; the card runs it at each phase end and the branch has no matrix evidence yet." % mx["commit"][:7],
    "rev": REV,
    "columns": ["headless", "scenarios", "appkit", "emulator", "suites", "tsan", "phone", "review"],
    "rows": gates,
    "matrix": {"commit": mx["commit"][:7], "date": mx["date"][:10], "hosts": len(hosts), "scenarios": len(scen),
               "equal": sum(len(h["equal"]) for h in hosts.values()),
               "framesPerPair": max(p["frames"] for p in mx["frames"].values()),
               "matrixEvidenceOnBranch": len(branch_matrix)},
})

# ------------------------------------------------------------------ profile before the redesign
base = evidence("rt-baseline-20261006.json")
INCL = [("front-buffer drawing", "рисование в буфер экрана", 0), ("gameplay session", "игровая сессия", 0),
        ("gameplay body", "тело игрового тика", 1), ("loaded cycle", "загруженный цикл", 0),
        ("bindings store", "запись модели обратно в состояние", 0), ("Android window drawing", "окно Android", 0),
        ("loaded menu attempt", "подготовка попытки меню", 0), ("loaded match entry", "вход в матч", 0),
        ("display perform", "сервис дисплея", 0), ("bindings read", "чтение состояния в модель", 0),
        ("menu state replace", "замена записи меню", 0), ("observed iteration", "наблюдаемая итерация", 0)]
selfp = base["profile"]["self"]
dump("perf_profile.json", {
    "title": "Профиль телефона на старте редизайна (simpleperf, 30 с игры): доли фаз и символов",
    "source": "ntsd-2.4 at %s: %srt-baseline-20261006.json (35ec7a3); per-tick data flow: %sCORE_REALTIME_DATAFLOW.md, copy map: %sCORE_REALTIME_COPIES.md" % (REV, EV, RS, RS),
    "caveat": "Inclusive shares overlap (the gameplay body is inside the gameplay session); do not add them. Self shares are disjoint. "
              "Frame-pointer call graphs on one phone; the build is debuggable.",
    "rev": REV,
    "samples": base["profile"]["samples"], "seconds": base["profile"]["seconds"],
    "ticksPerSecond": base["speed"]["ticksPerSecond"], "peakResidentMB": base["speed"]["peakResidentMB"],
    "inclusive": [{"key": k, "label": l, "depth": d, "share": base["profile"]["inclusive"][k]} for k, l, d in INCL],
    "self": {"memcpy": selfp["__memcpy"], "retain": selfp["swift_retain"], "release": selfp["swift_release"],
             "atomics": round(selfp["__aarch64_cas8_rel"] + selfp["__aarch64_cas8_relax"], 1)},
})

# ------------------------------------------------------------------ clocks and budget
meas = evidence("rt-measurement-20261006.json")
off = meas["offcpu"]
budget = show(RS + "CORE_REALTIME_BUDGET.md")
by_label = {r["label"]: r for r in meas["runs"]}
virt, realr = by_label["rt4f-cpu-virtual"], by_label["rt4f-cpu-realclock"]
last = ladder[-1]
dump("perf_budget.json", {
    "title": "Часы харнесса и бюджет кадра: виртуальные и настоящие часы на фазе 4f, ярусы 33/16/8 мс",
    "source": "ntsd-2.4 at %s: %srt-measurement-20261006.json (4c3ea6f), %sCORE_REALTIME_BUDGET.md, the last ledger row (%s)" % (REV, EV, RS, last["evidence"]),
    "caveat": "Wall time per tick = 1000 / ticks per second. Compute per tick = the thread's on-CPU share x wall time per tick. "
              "The render thread runs in parallel with the main thread. Scripted match on one phone; hand play is an open check. " + FROZEN,
    "rev": REV,
    "pacingMs": 33, "sleepStepMs": 5, "virtualIterationMs": 8,
    "offcpu": {"share": int(need(r"\((\d+)%\) off-CPU", off, "off share").group(1)),
               "inLooper": num(need(r"([\d.]+)% of it in __epoll_pwait", off, "looper").group(1)),
               "waits": int(need(r"([\d,]+) waits", off, "waits").group(1).replace(",", "")),
               "waits4to6": int(need(r"([\d,]+) of them 4-6 ms", off, "4-6").group(1).replace(",", "")),
               "medianMs": num(need(r"median ([\d.]+) ms", off, "median").group(1))},
    "virtual": {"ticksPerSecond": virt["ticksPerSecond"], "wallMs": round(1000 / virt["ticksPerSecond"], 1),
                "mainMs": virt["mainMsPerTick"], "renderMs": virt["renderMsPerTick"]},
    "real": {"ticksPerSecond": realr["ticksPerSecond"], "wallMs": round(1000 / realr["ticksPerSecond"], 1),
             "mainMs": realr["mainMsPerTick"], "renderMs": realr["renderMsPerTick"]},
    "tiers": [33, 16, 8],
    "tier1MetAt": need(r"\*\*Where it stands \(4f, (2026-10-06 [\d:]+)\)", budget, "tier1 time").group(1),
    "now": {"id": last["id"], "hash": last["hash"], "mainMs": last["mainMs"], "renderMs": last["renderMs"],
            "menuMsPerStep": last["menuMsPerStep"]},
})

# ------------------------------------------------------------------ now: what is next, what is not proven
nxt = need(r"## Next task(.*)$", card, "next task").group(1)
j = need(r"18\.6 → ([\d.]+) ms.*?\(([\d.]+), ([\d.]+) ms", nxt, "1j bench")
orch = need(r"main ([\d.]+) ms per tick\): orchestration still ~(\d+) ms around a ~([\d.]+) ms gameplay body", nxt, "orchestration")
now = {
    "title": "Что в работе и что не доказано на 7 октября, 08:23",
    "source": "ntsd-2.4 at %s: %sCORE_REALTIME.md (Next task, header), %sCORE_REALTIME_A3.md, %sCORE_REALTIME_TIER2.md; afterFreeze: commits on exp/core-realtime after REV" % (REV, RS, RS, RS),
    "caveat": "Plans and design estimates are not measurements. afterFreeze = steps committed after REV on exp/core-realtime, outside the frozen chapter.",
    "rev": REV,
    "afterB1": {"mainMs": num(orch.group(1)), "orchestrationMs": int(orch.group(2)), "gameplayBodyMs": num(orch.group(3))},
    "bench1j": {"beforeMs": 18.6, "afterMs": num(j.group(1)), "branchlessMs": num(j.group(2)), "simdMs": num(j.group(3)),
                "what": "300 keyed 80x80 blits per frame on the A12 (committed note, change in flight)"},
    "idleIteration": {"nowMs": last["menuMsPerStep"],
                      "targetMs": num(need(r"idle message-loop iterations at ≤([\d.]+) ms", show(RS + "CORE_REALTIME_A3.md"), "A3 target").group(1))},
    "openManualCheck": "playing by hand on the A12" in json.dumps(meas),
    "loadingMinutes": num(need(r"Loading time on the phone \(~([\d.]+) minutes\)", card, "loading").group(1)),
    "merged": "Not merged" not in card,
}
# Work that was in flight at REV (named in the committed Next task: 4m and 1j) and landed later on the same
# branch. Read from the commits that added their evidence, so the numbers have a source; reported apart from
# the frozen chapter. Absent if the branch has no such commits yet.
later = []
for h in git("rev-list", "--reverse", f"{REV}..exp/core-realtime").split():
    added = git("show", "--diff-filter=A", "--name-only", "--format=", h).split()
    for path in added:
        name = os.path.basename(path)
        if path.startswith(EV + "rt-") and name.endswith(".json"):
            ev = json.loads(git("show", f"{h}:{path}"))
            _, after = runs(ev)
            later.append({"hash": h[:7], "time": git("show", "-s", "--format=%ad", "--date=format:%Y-%m-%d %H:%M", h).strip(),
                          "phase": ev.get("phase", "").split(" ")[0], "evidence": name, **summarize(virtual(after))})
        if path == RS + "CORE_REALTIME_RENDER_PASSES.md":
            t = git("show", f"{h}:{path}")
            now["renderPassesPlan"] = {
                "hash": h[:7], "state": "a static plan by a read-only planner, nothing built or run",
                "renderMsAfter1j": num(need(r"Render thread ([\d.]+) ms per tick after 1j", t, "1j render").group(1)),
                "passMs": num(need(r"~([\d.]+) ms for a channel swap", t, "pass ms").group(1)),
                "passes": len(re.findall(r"^\d\. ", t, re.M)),
            }
now["afterFreeze"] = later
dump("perf_now.json", now)
print("collect_perf: wrote perf_memory, perf_local, perf_ladder (%d steps), perf_gates, perf_profile, perf_budget, perf_now at %s"
      % (len(ladder), REV))
