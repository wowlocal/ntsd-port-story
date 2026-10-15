#!/usr/bin/env python3
"""Regenerate the deck's data/rt2_*.json (chapter 15, «16 миллисекунд»)
from the NTSD port repository, and the chapter's cover drawing.

Usage:
    python3 scripts/collect_realtime2.py ../ntsd-2.4 [REV]

REV defaults to 5f5a8ee4 (13 Oct 2026, 20:14), a commit that contains the
whole real-time study. The chapter covers the ledger rows of
docs/research/CORE_REALTIME.md from phase 4m (bf5628e, 7 Oct 08:51) to 4ad
and the status commit 0034e45c (10 Oct 18:27); chapter 14 ends at 8840eb3.
Every number is read with `git show REV:path` or `git log`, so later commits
do not change the output. Nothing in the source repository is modified.

Writes:
    data/rt2_steps.json    every ledger row 4m..4ad: phone runs (vs and the
                           Demo), verdict, review, gates, probe
    data/rt2_commits.json  the 84 commits 8840eb3..0034e45c with their times
    data/rt2_threads.json  compute per tick per thread at the start and end
    data/rt2_wall.json     what was left at the wall, the tier-3 plan vs fact
    data/rt2_loop.json     counts for the loop slide
    public/img/covers/ch15-ticks.svg  the cover: every kept step's main-thread
                           value as a bar (a drawing made from the data)
"""
import json
import os
import re
from datetime import datetime
import subprocess
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../ntsd-2.4")
REV = sys.argv[2] if len(sys.argv) > 2 else "5f5a8ee4"
START = "8840eb3"   # chapter 14's frozen commit
END = "0034e45c"    # "Record that the main thread's next steps need the user's decisions"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data")
COVER = os.path.join(HERE, "..", "public", "img", "covers", "ch15-ticks.svg")
CARD = "docs/research/CORE_REALTIME.md"
TIER3 = "docs/research/CORE_REALTIME_TIER3.md"
EV = "docs/evidence/"
PHONE = ("One phone (Galaxy A12, Helio P35: CPUs 0-3 at 2.3 GHz, 4-7 at 1.8 GHz), debuggable build "
         "(local.ntsd.port), shipping flags from 4aa on (no dynamic exclusivity checks); scripted match (vs: "
         "computer vs computer, bodies 300->1800; Demo: eight computer fighters) with music, sounds and network off, "
         "no frame capture, the harness's virtual clock (8 ms per message-loop iteration). Compute per tick per thread "
         "from schedstat between bodies 600 and 1500 (tools/crossplatform/android_speed.py); not wall time.")


def git(*args):
    res = subprocess.run(["git", "-C", REPO, *args], check=True, capture_output=True)
    return res.stdout.decode("utf-8", "replace")


def show(path):
    return git("show", f"{REV}:{path}")


def dump(name, obj, path=None):
    with open(path or os.path.join(OUT, name), "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def mean(xs):
    return round(sum(xs) / len(xs), 2) if xs else None


def when(h):
    """Local commit time 'MM-DD HH:MM' (+0200) of a commit."""
    return git("show", "-s", "--format=%ad", "--date=format:%m-%d %H:%M", h).strip()


def added_in(path):
    out = git("log", REV, "--diff-filter=A", "--format=%h", "--", path).split()
    return out[-1] if out else None


# ---------------------------------------------------------------- ledger rows
card = show(CARD)
rows = [l for l in card.split("\n## Next task")[0].splitlines() if l.startswith("| 2026-10-")]
first = next(i for i, l in enumerate(rows) if "| Phase 4m:" in l)
rows = rows[first:]


def cells(line):
    parts = [c.strip() for c in line.strip().strip("|").split("|")]
    return {"date": parts[0], "title": parts[1], "result": parts[2], "evidence": parts[3], "commit": parts[4]}


def sid(title):
    t = re.sub(r"\*\*", "", title)
    t = re.sub(r"^Phase ", "", t)
    m = re.match(r"([^:]+):", t)
    head = m.group(1) if m else t
    head = re.sub(r" \((tier 3[^)]*|render thread|main thread|Android)\)", "", head).strip()
    return head


# Short Russian labels, written for the slides from each ledger row (the row stays the source).
RU = {
    "4m": "продолжение цикла и возвраты — в общих объектах",
    "1j": "копии с ключом без битов маски над полным кадром",
    "4n": "владельцы и контекст доставки — в общих объектах",
    "4o": "Host читает сессию на месте, без копий",
    "R1": "вывод кадра: копия и обрезка слиты",
    "4p": "порядок 14 600 блоков кадров — раз на каталог",
    "4q": "адаптер событий слотов — один на проход",
    "B2 P1": "проходы слотов и планировщик — на месте",
    "B2 P1b": "одно тело на проход; корпуса через обе формы",
    "4r": "неактивные слоты выходят до прохода",
    "B2 P2": "подшаги входа в матч — на месте",
    "B2 P2b": "одно ядро приёма ввода",
    "B2 P2c": "локальный ввод — на месте",
    "B2 P2d": "тест отката входа в матч",
    "B2 P3": "ИИ и ввод объектов — на месте",
    "B2 P3b": "проверки отката ИИ через обе формы",
    "A3 P0": "холостые итерации измерены отдельно",
    "A3 L3": "холостой цикл — на пустом контексте",
    "A3 P5a": "таймер итераций Android — timerfd",
    "A3 P5b": "таймер итераций укреплён после ревью",
    "4u": "ворота — только из чистых сборок",
    "4s": "слова битмапов читаются на месте",
    "4t": "завершение цикла без копий",
    "A3 L4a": "холостые запросы без разрешений",
    "1k": "одна отправка рендеру на батч",
    "B2 P4a": "три прохода мира на месте",
    "4w": "быстрые пути плоских записей",
    "B2 P4b+c": "управление, физика, жизненный цикл — на месте",
    "B2 P4d": "связи, контакты, камера, рисование — на месте",
    "B2 P4e": "удары, cpoints и запись — на месте",
    "B2 P4f": "команды после отрисовки — на месте",
    "4x": "попытка загрузки без случайного UUID",
    "B3a": "загруженный цикл — один уровень транзакции",
    "B2 P4g": "вывод и метка режима — на месте",
    "4z": "шрифт ищет битмап глифа один раз",
    "4aa": "релиз без динамических проверок эксклюзивности",
    "4ab": "тот же выключатель для FreeType, SDL и iOS",
    "S1": "двухуровневые таблицы страниц повтора",
    "G1": "невидимые спрайты и глифы — на стеке",
    "G3a": "прямые команды Blt и заливки",
    "G3b": "без наблюдений, которые никто не получает",
    "G3c": "событие Blt строится на месте",
    "d1": "списки команд резервируются заранее",
    "R2@09": "вывод Android — в свой поток",
    "S2a": "узкие чтения записей: 169 правок в 79 файлах",
    "S2b": "запись — один буфер с битовой маской",
    "S3": "таблица актёров кусками по 16",
    "d2": "хвост коммита Host — отдельно",
    "g": "повтор без массивов владельцев",
    "M1": "таблица актёров мира — за один проход",
    "e": "Blt и заливка — одна запись",
    "A3 L5a": "контекст доставки делит платформу",
    "e2": "повтор читает команды на месте",
    "P2": "задний буфер одалживается кадру",
    "L1": "чтение записи — встроено",
    "R0": "memchr для таблицы случайных; трек — один раз",
    "L2": "запись в запись — встроена",
    "L3": "пул ожидания — раз на сессию",
    "e3": "хвост коммита — по индексу",
    "G4a": "копии и заливки рендеру — значениями",
    "G4b": "кэш поверхностей на повтор",
    "L4": "физика без копии актёра для наблюдателя",
    "R2b": "R2 перемерен на новой сборке",
    "P0": "главный поток — на быстрые ядра",
    "R2": "вывод Android — в свой поток, на медленные ядра",
    "A3 L4b": "первая холостая попытка без драйвера",
    "R3": "мёртвые значения освобождает свой поток",
    "e4": "две копии убраны с пути тика",
    "R4a": "SIMD-копии по 4 пикселя",
    "R4b": "копии по 4 пикселя в тесных циклах",
    "R3b": "поток освобождения просыпается сам",
    "e5": "emit забирает эффект, а не копирует",
    "F1": "поля кадров физики — на месте",
    "4ac": "macOS-приложение без проверок",
    "4ad": "пакеты Linux, Windows, iOS без проверок",
}

# Verdicts the ledger states in words; everything else is read from the row (see verdict()).
FORCED = {
    "B2 P1b": "follow", "B2 P2b": "follow", "A3 P5b": "follow", "4ab": "follow",
    "B2 P2d": "test", "B2 P3b": "test", "A3 P0": "telemetry", "4u": "procedure",
    "4aa": "decision", "4ac": "build", "4ad": "build",
    "B2 P4a": "reverted", "B3a": "reverted",
    "R2@09": "parked", "S3": "parked", "G4b": "parked", "R2b": "parked", "R4a": "parked", "F1": "parked",
    "A3 L3": "less",   # idle step 0.66 -> 0.63 ms, main unchanged
    "A3 L4a": "less",  # idle step 0.62 -> 0.60 ms
    "R3": "kept", "R4b": "kept",  # the row's "within noise" is about the other thread
}
LESS = re.compile(r"committed as|no measurable change|within (run )?variation|within noise|below (run )?resolution|"
                  r"Phone within resolution|\(unchanged|within resolution", re.I)

# Where the work landed: main thread, render thread, or the Android host/build.
FOCUS = {"1j": "render", "R1": "render", "1k": "both", "P2": "render", "R2@09": "render", "R2": "render",
         "R2b": "render", "R4a": "render", "R4b": "render", "G4a": "both", "4w": "both", "A3 P5a": "both",
         "4aa": "both", "4ab": "both", "4ac": "build", "4ad": "build", "4u": "build", "B2 P2d": "test",
         "B2 P3b": "test"}

# The probe each row names (profile share of the main or render thread before -> after), in Russian.
PROBE_RU = {
    "G3a": "emit", "G3b": "Attempt.front", "G3c": "emit", "d1": "emit", "S2b": "копирование массивов при записи",
    "d2": "finishLoadedMenu среди копирующих", "g": "бэкенд дисплея", "M1": "привязки (bindings)",
    "e": "сборщик Blt", "A3 L5a": "холостой шаг", "e2": "повтор батча", "P2": "memcpy (поток рендера)",
    "L1": "тело игрового тика", "R0": "проверка таблицы случайных", "L2": "тело игрового тика",
    "e3": "finish", "G4a": "serveFront", "G4b": "frontSurface", "L4": "WorldPhysics.apply",
    "e4": "stagedCopy", "R3b": "retire", "e5": "emit", "R3": "освобождение массивов",
}


def verdict(i, r):
    if i in FORCED:
        return FORCED[i]
    if LESS.search(r["result"]):
        return "less"
    return "kept"


def find_runs(o, path=()):
    """Every run dict under o with its key path."""
    out = []
    if isinstance(o, dict):
        if "mainMsPerTick" in o and isinstance(o["mainMsPerTick"], (int, float)):
            return [(path, o)]
        for k, v in o.items():
            out += find_runs(v, path + (k,))
    elif isinstance(o, list):
        for v in o:
            out += find_runs(v, path)
    return out


def phone_of(ev):
    for root in (ev.get("phone"), (ev.get("result") or {}).get("phone") if isinstance(ev.get("result"), dict) else None,
                 (ev.get("regate") or {}).get("phone") if isinstance(ev.get("regate"), dict) else None):
        if root:
            return root
    return None


def side(lst):
    runs = [r for r in lst if isinstance(r, dict) and isinstance(r.get("mainMsPerTick"), (int, float))]
    if not runs:
        return None
    main = [r["mainMsPerTick"] for r in runs]
    rend = [r["renderMsPerTick"] for r in runs]
    s = {"n": len(runs), "main": mean(main), "render": mean(rend), "mainMin": min(main), "mainMax": max(main),
         "renderMin": min(rend), "renderMax": max(rend)}
    pres = [r["presentMsPerTick"] for r in runs if isinstance(r.get("presentMsPerTick"), (int, float))]
    rel = [r["releaseMsPerTick"] for r in runs if isinstance(r.get("releaseMsPerTick"), (int, float))]
    if pres:
        s["present"] = mean(pres)
    if rel:
        s["release"] = mean(rel)
    return s


def scenario(d):
    """{'after': side, 'base': side, 'baseKey': key} from one scenario's dict of run lists."""
    if isinstance(d, list):
        return {"after": side(d), "base": None, "baseKey": None}
    after = d.get("after") if isinstance(d.get("after"), list) else d.get("runs") if isinstance(d.get("runs"), list) else None
    base_key = next((k for k, v in d.items() if isinstance(v, list) and k not in ("after", "runs")
                     and "review_fix" not in k and k != "summary"), None)
    base = side(d[base_key]) if base_key else None
    if base:
        # 8 Oct on, the previous build was run interleaved in the same session; before that "before" is the previous
        # step's own runs
        base["interleaved"] = "same" in base_key
    return {"after": side(after or []), "base": base, "baseKey": base_key}


all_runs = {}
steps = []
seen_r2 = False
for line in rows:
    r = cells(line)
    i = sid(r["title"])
    if i == "R2" and not seen_r2 and "not committed" in r["title"]:
        i = "R2@09"
    if i == "R2" or i == "R2@09":
        seen_r2 = True
    evm = re.search(r"\(\.\./evidence/([^)]+\.json)\)", r["evidence"])
    evname = evm.group(1) if evm else None
    ev = json.loads(show(EV + evname)) if evname else {}
    commit = re.match(r"([0-9a-f]{7})", r["commit"])
    h = commit.group(1) if commit else added_in(EV + evname)
    if r["commit"].startswith("this commit"):
        h = added_in(EV + evname)
    ph = phone_of(ev)
    vs = demo = None
    if ph:
        if "vs" in ph or "demo" in ph:
            vs = scenario(ph["vs"]) if "vs" in ph else None
            demo = scenario(ph["demo"]) if "demo" in ph else None
        else:
            vs = scenario(ph)
        for p, run in find_runs(ph):
            lab = run.get("label") or json.dumps(run, sort_keys=True)
            all_runs[lab] = run
    for k in ("rejected_first_version", "first_version"):
        if k in ev:
            for p, run in find_runs(ev[k]):
                all_runs[run.get("label") or json.dumps(run, sort_keys=True)] = run
    rv = ev.get("review")
    rvt = rv if isinstance(rv, str) else json.dumps(rv, ensure_ascii=False) if rv else ""
    if not rvt:
        review = "none"
    elif re.search(r"changes needed|blocking finding|review OK after a fix|after a test fix|after its findings", rvt + r["result"], re.I):
        review = "caught"
    elif re.search(r"^(independent|P4b: independent|R2's independent)", rvt) or "independent read-only review" in rvt:
        review = "nits" if re.search(r"nits|findings|finding", rvt) else "ok"
    else:
        review = "skipped"
    gates = json.dumps(ev.get("gates") or ev.get("gates_run") or ev.get("regate") or ev.get("checks") or "", ensure_ascii=False)
    blob = r["result"] + " " + gates
    probe = None
    pm = re.search(r"(?:Profile|Probe): (?:the )?([^.;:]*?) ([\d.]+) → ([\d.]+)%", r["result"])
    if pm:
        probe = {"what": PROBE_RU.get(i, pm.group(1)), "before": float(pm.group(2)), "after": float(pm.group(3))}
    steps.append({
        "id": i, "label": RU[i], "title": re.sub(r"\*\*", "", r["title"]), "date": r["date"],
        "hash": h[:7] if h else None, "time": when(h) if h else None,
        "verdict": verdict(i, r), "focus": FOCUS.get(i, "main"), "review": review,
        "gates": {
            "scenarios10": bool(re.search(r"all 10 scenarios|tournament-win|full suite list|behaviour equal", blob, re.I)),
            "appkit": bool(re.search(r"AppKit|3,960|3960", blob)),
            "emulator": bool(re.search(r"emulator", blob)),
            "tsan": bool(re.search(r"ThreadSanitizer|TSan", blob)),
        },
        "vs": vs, "demo": demo, "probe": probe, "evidence": evname,
    })

assert len(steps) == len(RU), (len(steps), len(RU))

# ------------------------------------------------------------- start / end
ev4l = json.loads(show(EV + "rt-4l-pending-loading-20261007.json"))
start = side(ev4l["phone"]["after"])
kept = [s for s in steps if s["verdict"] in ("kept", "less", "decision", "follow") and s["vs"] and s["vs"]["after"]]
last = next(s for s in reversed(steps) if s["id"] == "e5")
first_demo = next(s for s in steps if s["demo"] and s["demo"]["after"])


def crossing(scen, key, limit):
    for s in steps:
        if s["verdict"] in ("reverted", "parked"):
            continue
        a = (s.get(scen) or {}).get("after")
        if a and a[key] is not None and a[key] <= limit:
            return {"id": s["id"], "hash": s["hash"], "time": s["time"], "value": a[key]}
    return None


tiers = {}
for lim, name in ((16.67, "60fps"), (16.0, "16"), (8.0, "8")):
    tiers[name] = {f"{sc}_{k}": crossing(sc, k, lim) for sc in ("vs", "demo") for k in ("main", "render")}

# biggest in-session steps (baseline mean - after mean), kept steps only
deltas = []
for s in steps:
    if s["verdict"] not in ("kept", "less", "decision"):
        continue
    for sc in ("vs", "demo"):
        d = s.get(sc)
        if d and d["after"] and d["base"]:
            for k in ("main", "render"):
                deltas.append({"id": s["id"], "scenario": sc, "thread": k, "hash": s["hash"],
                               "from": d["base"][k], "to": d["after"][k], "delta": round(d["after"][k] - d["base"][k], 2)})

# The biggest single steps. B2 P4b+c..P4f were each measured against the same 4w runs of that night, so their own
# deltas are cumulative: they are shown as one group, and in the strip each gets the step from the one before it.
GROUP = ["B2 P4b+c", "B2 P4d", "B2 P4e", "B2 P4f"]
MOVED = {"P0": "те же вычисления на быстрых ядрах", "R2": "вывод на экран — в поток presenter (≈ 5,8 мс на медленных ядрах)"}
byid = {s["id"]: s for s in steps}


def entry(s, key, base, after):
    a = s["vs"]["after"]
    return {"id": s["id"], "label": s["label"], "hash": s["hash"], "time": s["time"], "thread": key, "from": base,
            "to": after, "delta": round(after - base, 2), "runs": a["n"], "toMin": a[key + "Min"], "toMax": a[key + "Max"],
            "moved": MOVED.get(s["id"])}


committed = [s for s in steps if s["verdict"] in ("kept", "less", "decision") and s["vs"] and s["vs"]["after"] and s["vs"]["base"]]
main_c, rend_c, strip = [], [], []
for s in committed:
    if s["id"] in GROUP:
        k = GROUP.index(s["id"])
        prev = byid[GROUP[k - 1]]["vs"]["after"]["main"] if k else s["vs"]["base"]["main"]
        strip.append(entry(s, "main", prev, s["vs"]["after"]["main"]))
        continue
    e = entry(s, "main", s["vs"]["base"]["main"], s["vs"]["after"]["main"])
    main_c.append(e)
    strip.append(e)
    if s["focus"] in ("render", "both"):
        rend_c.append(entry(s, "render", s["vs"]["base"]["render"], s["vs"]["after"]["render"]))
g0, g1 = byid[GROUP[0]], byid[GROUP[-1]]
main_c.append({"id": "B2 P4b–f", "label": "все проходы игрового тела — на месте, разом", "hash": f'{g0["hash"]}…{g1["hash"]}',
               "time": g1["time"], "from": g0["vs"]["base"]["main"], "to": g1["vs"]["after"]["main"],
               "delta": round(g1["vs"]["after"]["main"] - g0["vs"]["base"]["main"], 2), "moved": None, "group": GROUP,
               "thread": "main", "runs": g1["vs"]["after"]["n"], "toMin": g1["vs"]["after"]["mainMin"],
               "toMax": g1["vs"]["after"]["mainMax"]})
biggest = {
    "top": sorted(main_c + rend_c, key=lambda e: e["delta"])[:12],
    "strip": sorted(strip, key=lambda e: e["delta"]),
    "noiseMs": 0.25,
    "withinNoise": sum(1 for e in strip if abs(e["delta"]) <= 0.25),
}

runs = list(all_runs.values())
run_seconds = sum(r.get("runSeconds", 0) for r in runs)

dump("rt2_steps.json", {
    "title": "Ярусы 16 и 8 мс на Galaxy A12, 7–10 октября: каждая строка реестра CORE_REALTIME от 4m до 4ad",
    "source": f"ntsd-2.4 at {REV}: {CARD} (Ledger) and the evidence file named in each row (docs/evidence/rt-*.json); "
              "commit times from git (+0200)",
    "caveat": PHONE + " after = mean of the step's runs; base = mean of the previous build's runs interleaved in the same "
              "session (the phone drifts between sessions, so compare after with base, not with the previous step's after). "
              "The phone resolves about ±0.25 ms per run (CORE_REALTIME.md). From R2 (10 Oct) the Android present runs on "
              "its own presenter thread and is not in 'render'; from R3 freeing runs on a release thread and is not in "
              "'main'. verdict: kept = measurably faster; less = committed as strictly less work within noise; reverted/"
              "parked = measured and not committed; follow/test/telemetry/procedure/build/decision as named. "
              "review: ok/nits = independent read-only review approved (with nits); caught = the review or a gate found a "
              "defect that was fixed before the commit; skipped = recorded as not required; none = no review field.",
    "start": {"id": "4l", "hash": "8840eb3", "time": when("8840eb3"), "vs": start},
    "end": {"id": last["id"], "hash": last["hash"], "time": last["time"], "vs": last["vs"]["after"], "demo": last["demo"]["after"]},
    "firstDemo": {"id": first_demo["id"], "hash": first_demo["hash"], "time": first_demo["time"]},
    "tiers": tiers,
    "deltas": sorted(deltas, key=lambda x: x["delta"]),
    "biggest": biggest,
    "phoneRuns": {"runs": len(runs), "hours": round(run_seconds / 3600, 1),
                  "note": "distinct phone runs (by label) recorded in the chapter's evidence, incl. baselines and reverted builds; runSeconds summed"},
    "steps": steps,
})

# ------------------------------------------------------------------ commits
log = git("log", "--reverse", f"{START}..{END}", "--format=%h\t%ad\t%s", "--date=format:%m-%d %H:%M").strip().splitlines()
ledger_hashes = {s["hash"] for s in steps if s["hash"]} | {"7c02b7f"}  # 7c02b7f: 4aa's second half (its tools change)
commits = []
for l in log:
    h, t, subj = l.split("\t")
    h = h[:7]
    if h in ledger_hashes:
        kind = "step"
    elif re.match(r"(Record|Update|Plan)", subj):
        kind = "record"
    else:
        kind = "tool"
    commits.append({"hash": h, "time": t, "subject": subj, "kind": kind})
tag = git("for-each-ref", "refs/tags/rt-60fps-a12", "--format=%(*objectname:short)\t%(taggerdate:format:%m-%d %H:%M)\t%(contents:subject)").strip().split("\t")
dump("rt2_commits.json", {
    "title": "84 коммита 8840eb3..0034e45c (7 окт 08:51 — 10 окт 18:27), время местное (+0200)",
    "source": f"git log --reverse {START}..{END} in ntsd-2.4; tag rt-60fps-a12",
    "caveat": "kind: step = the commit named by a ledger row (or adding its evidence); record = a ledger/plan/status "
              "commit (Record, Update, Plan); tool = harness and install fixes. Subjects verbatim.",
    "count": len(commits),
    "tag": {"name": "rt-60fps-a12", "commit": tag[0][:7], "time": tag[1], "subject": tag[2]},
    "commits": commits,
})

# ------------------------------------------------------------------ threads
e5 = json.loads(show(EV + "rt-e5-emit-consumes-20261010.json"))
fin_vs = side(e5["phone"]["vs"]["after"])
fin_demo = side(e5["phone"]["demo"]["after"])
p0 = json.loads(show(EV + "rt-p0-main-on-fast-cores-20261010.json"))
r2 = json.loads(show(EV + "rt-r2-presenter-thread-20261010.json"))
r3 = json.loads(show(EV + "rt-r3-release-thread-20261010.json"))
r2p = json.loads(show(EV + "rt-r2-presenter-thread-parked-20261009.json"))
r2b = json.loads(show(EV + "rt-r2b-presenter-remeasured-20261010.json"))


def pair(ev, sc):
    d = scenario(ev["phone"][sc])
    return {"base": d["base"], "after": d["after"]}


dump("rt2_threads.json", {
    "title": "Работа на тик по потокам: начало главы (4l) и конец (e5); R2 → P0 → R2 → R3",
    "source": f"ntsd-2.4 at {REV}: rt-4l-pending-loading-20261007.json, rt-e5-emit-consumes-20261010.json, "
              "rt-r2-presenter-thread-parked-20261009.json, rt-r2b-presenter-remeasured-20261010.json, "
              "rt-p0-main-on-fast-cores-20261010.json, rt-r2-presenter-thread-20261010.json, rt-r3-release-thread-20261010.json",
    "caveat": PHONE + " The sum over threads is CPU work per tick, not a frame time: the threads run at the same time "
              "on different cores. 4l had no Demo measurement (the Demo was first measured on 8 Oct).",
    "start": {"main": start["main"], "render": start["render"]},
    "end": {"vs": fin_vs, "demo": fin_demo},
    "cores": {"fast": [0, 1, 2, 3], "fastGHz": 2.3, "slow": [4, 5, 6, 7], "slowGHz": 1.8,
              "finding": p0["finding"]},
    "r2parked": {"vs": pair(r2p, "vs"), "demo": pair(r2p, "demo")},
    "r2b": {"vs": pair(r2b, "vs"), "demo": pair(r2b, "demo"), "result": r2b["result"]},
    "p0": {"vs": pair(p0, "vs"), "demo": pair(p0, "demo")},
    "r2": {"vs": pair(r2, "vs"), "demo": pair(r2, "demo")},
    "r3": {"vs": pair(r3, "vs"), "demo": pair(r3, "demo")},
})

# --------------------------------------------------------------------- wall
t3 = show(TIER3)
cand = {}
for l in t3.splitlines():
    m = re.match(r"\| (B|D|L6b|P) \| (.+?) \| ([\d.–]+)[^|]*\| [^|]+\| \*\*yes \((Q\d)\)\*\*", l)
    if m:
        lo, hi = m.group(3).split("–")
        cand[m.group(4)] = {"id": m.group(1), "mechanism": m.group(2), "lo": float(lo), "hi": float(hi)}
for q in ("Q1", "Q2", "Q3", "Q4"):
    qm = re.search(r"- \*\*" + q + r"\.\*\* (.+?)(?=\n- \*\*Q|\n\n|\Z)", t3, re.S)
    cand[q]["question"] = " ".join(qm.group(1).split())
nt = " ".join(card.split("## Next task")[1].split())
free = []
for name, ms in re.findall(r"(H3|H2|a polling render thread|boxing the platform's rarely written deliveries|L6|`lastRequest`) \(~([\d.]+) ms", nt):
    free.append({"item": name.strip("`"), "ms": float(ms)})
assert len(free) == 6, free
order = re.findall(r"\d\. ([^\n]+?) → ~(\d+(?:\.\d+)?) / (\d+(?:\.\d+)?)", t3)
plan = [{"steps": s, "vs": float(a), "demo": float(b)} for s, a, b in order]
ps = re.search(r"main thread ([\d.]+) ms \(vs\) and\s+([\d.]+) ms \(Demo\) per tick", t3)
plan_start = {"vs": float(ps.group(1)), "demo": float(ps.group(2))}
dump("rt2_wall.json", {
    "title": "Стена 10 октября: что осталось без решений автора и что откроют Q1–Q4",
    "source": f"ntsd-2.4 at {REV}: {CARD} (Next task, 2026-10-10) and {TIER3} (Candidates, Order, Decisions for the user; "
              "written 2026-10-08, 5fe8641d)",
    "caveat": "Savings are the plan's conservative estimates (ms per tick), not measurements. The phone resolves about "
              "±0.25 ms per run. The plan's trajectory was written for its own order of steps; the loop took a different "
              "order (P0, R2, R3 were not in it), so only the endpoints compare.",
    "resolutionMs": 0.25,
    "decisionFree": free,
    "decisions": cand,
    "projectionWithQ2toQ4": {"lo": 9, "hi": 10},
    "planWithoutDecisions": {"main": 11, "lo": 9, "hi": 12.5, "render": 8},
    "planOrder": plan,
    "planStart": plan_start,
    "fact": {"vs": fin_vs["main"], "demo": fin_demo["main"], "renderVs": fin_vs["render"], "renderDemo": fin_demo["render"]},
})

# --------------------------------------------------------------------- loop
vc = {}
for s in steps:
    vc[s["verdict"]] = vc.get(s["verdict"], 0) + 1
rc = {}
for s in steps:
    rc[s["review"]] = rc.get(s["review"], 0) + 1
dump("rt2_loop.json", {
    "title": "Петля 7–10 октября в числах",
    "source": f"data/rt2_steps.json and data/rt2_commits.json (ntsd-2.4 {START}..{END}, rows 4m..4ad of {CARD})",
    "caveat": "Counts of ledger rows by the verdict and review classes defined in rt2_steps.json; phone runs are distinct "
              "labelled runs in the evidence files.",
    "rows": len(steps), "commits": len(commits), "verdicts": vc, "reviews": rc,
    "phoneRuns": len(runs), "phoneHours": round(run_seconds / 3600, 1),
    "firstTime": commits[0]["time"], "lastTime": commits[-1]["time"],
    "hours": round((datetime.strptime("2026-" + commits[-1]["time"], "%Y-%m-%d %H:%M")
                    - datetime.strptime("2026-" + commits[0]["time"], "%Y-%m-%d %H:%M")).total_seconds() / 3600, 1),
    "independentReviews": rc.get("ok", 0) + rc.get("nits", 0) + rc.get("caught", 0),
})

# -------------------------------------------------------------------- cover
bars = [s for s in steps if s["verdict"] in ("kept", "less", "decision") and s["vs"] and s["vs"]["after"]]
# the chapter layout shows the image in a box of about 608 x 551 px (cover-fit), so the drawing has that aspect and
# keeps its left third empty for the title
W, H = 620, 560
x0, x1, base = 210, 604, 480
sc = (base - 80) / 26.0
bw = (x1 - x0) / len(bars)
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
       '<rect width="100%" height="100%" fill="#0a0d13"/>']
for k, s in enumerate(bars):
    v = s["vs"]["after"]
    hm = v["main"] * sc
    hr = v["render"] * sc
    x = x0 + k * bw
    out.append(f'<rect x="{x + 1:.1f}" y="{base - hm:.1f}" width="{bw * 0.5:.1f}" height="{hm:.1f}" fill="#d95926"/>')
    out.append(f'<rect x="{x + 1 + bw * 0.5:.1f}" y="{base - hr:.1f}" width="{bw * 0.35:.1f}" height="{hr:.1f}" fill="#3987e5" opacity="0.8"/>')
out.append(f'<line x1="{x0 - 10}" x2="{x1}" y1="{base}" y2="{base}" stroke="#3a4252" stroke-width="2"/>')
for ms, col, lab in ((16.67, "#f6f3ec", "16,67"), (8, "#c3c2b7", "8")):
    y = base - ms * sc
    out.append(f'<line x1="{x0 - 10}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="1.5" stroke-dasharray="6 4"/>')
    out.append(f'<text x="{x1}" y="{y - 8:.1f}" text-anchor="end" font-family="monospace" font-size="17" fill="{col}" '
               f'stroke="#0a0d13" stroke-width="5" paint-order="stroke">{lab} мс</text>')
out.append("</svg>")
with open(COVER, "w") as f:
    f.write("\n".join(out) + "\n")

print(f"{len(steps)} rows, {len(commits)} commits, {len(runs)} runs ({run_seconds / 3600:.1f} h), verdicts {vc}, reviews {rc}")
print("start", start, "\nend vs", fin_vs, "\nend demo", fin_demo)
print("tiers", json.dumps(tiers, ensure_ascii=False))
