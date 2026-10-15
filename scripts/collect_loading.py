#!/usr/bin/env python3
"""Regenerate the deck's data/loading_*.json (chapter 16, «Две минуты за одну ночь»)
from the NTSD port repository and the Claude Code session log.

Usage:
    python3 scripts/collect_loading.py [../ntsd-2.4] [REV]

REV defaults to 5f5a8ee4 (13 Oct 2026, 20:14), the commit the chapter is frozen
at. The MEMORY_LOADING study is the span 0034e45c..6b4bffd5 (branch
exp/memory-loading, 10 Oct 18:27 -> 11 Oct 19:43). Every number is read with
`git show REV:path` from docs/research/MEMORY_LOADING.md and the evidence files
docs/evidence/ml-*.json that span added; commit times come from `git log`.

data/loading_night.json also reads the session log
~/.claude/projects/-Users-michael-Developer-ntsd-2-4/1f9218ae-....jsonl, but only
timestamps and counts: when the human typed or queued a turn, compactions,
tool-call counts, long stretches without an agent message. No message text is
stored; the quotes on the slides are in pages/16-loading.md.

Writes:
    data/loading_steps.json   every gated increment: A/B medians and ranges on the
                              Galaxy A12 and the Mac, mechanism family, review
    data/loading_race.json    one typical run before and after (the race slide)
    data/loading_method.json  noise floor, warm-up, the menu-phase drift check,
                              frame-time audit, mixer benchmark, RAM audit, M8, M9
    data/loading_night.json   the night on one time axis: commits, human turns,
                              compactions, idle stretches, counters

Nothing in the source repository is modified: only `git show` and `git log`.
"""
import datetime as dt
import json
import os
import re
import statistics
import subprocess
import sys

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "ntsd-2.4"))
REV = sys.argv[2] if len(sys.argv) > 2 else "5f5a8ee4"
BASE, LAST = "0034e45c", "6b4bffd5"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
SESSION = os.path.join(os.path.expanduser("~"), ".claude", "projects", "-Users-michael-Developer-ntsd-2-4",
                       "1f9218ae-9d5d-4c4e-a8dd-d5254994839c.jsonl")
TZ = dt.timezone(dt.timedelta(hours=2))
EV = "docs/evidence/"
CARD = "docs/research/MEMORY_LOADING.md"
FROZEN = "ntsd-2.4 на 5f5a8ee4 (13 окт 2026, 20:14); исследование MEMORY_LOADING — 0034e45..6b4bffd, ветка exp/memory-loading"


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], check=True, capture_output=True).stdout.decode("utf-8", "replace")


def evidence(name):
    return json.loads(git("show", f"{REV}:{EV}{name}"))


def dump(name, obj):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def r3(v):
    return None if v is None else round(v, 3)


def stat(s):
    """{median,min,max} -> [median, min, max]"""
    return None if not isinstance(s, dict) else [r3(s["median"]), r3(s["min"]), r3(s["max"])]


def runs_stat(runs, key):
    xs = [r[key] for r in runs if r.get(key) is not None]
    return [r3(statistics.median(xs)), r3(min(xs)), r3(max(xs))] if xs else None


def need(cond, what):
    if not cond:
        raise SystemExit(f"collect_loading: {what}")


# ------------------------------------------------------------------ commits of the span
log = git("log", "--reverse", "--format=%h|%H|%cI|%s", f"{BASE}..{LAST}").strip().split("\n")
commits = []
for ln in log:
    h, full, iso, subj = ln.split("|", 3)
    commits.append({"hash": full[:7], "time": iso[:16], "subject": subj})
by_hash = {c["hash"]: c for c in commits}
need(len(commits) >= 30 and commits[-1]["hash"] == LAST[:7], "unexpected commit span")
tagged = sum(1 for c in commits if "MEMORY_LOADING" in c["subject"])

card = re.sub(r"\s+", " ", git("show", f"{REV}:{CARD}"))  # Markdown wraps lines
need("останавливаемся на" in card and "we must not compromise on performance" in card, "card quotes moved")

# ------------------------------------------------------------------ gated increments
# family: how the step saves time (load) or memory; the slide groups load steps by family
FAM = {
    "inplace": "на месте, без копий",
    "parallel": "все ядра и железо",
    "search": "поиск вместо перебора",
    "convert": "меньше превращений",
    "memory": "хранить меньше",
}
# id, evidence file, commit, family, name (ru), how (ru), review finding (ru, only where the review changed something)
STEPS = [
    ("L1", "ml-l1-file-streams-in-place-20261010.json", "17416cd", "inplace",
     "Потоки файлов меняются на месте",
     "каждый прочитанный символ DAT-файла копировал весь Stream — четыре массива байтов — туда и обратно; ещё массив на каждый байт",
     None),
    ("L2", "ml-l2-loader-arrays-in-place-20261010.json", "5e1ec59", "inplace",
     "Массивы загрузчика — на месте",
     "запись в одну картинку копировала весь массив из ~1 800 загруженных: свойство было вычисляемым get/set, теперь _modify",
     None),
    ("L3", "ml-l3-packages-on-all-cores-20261010.json", "2e4d4dd", "parallel",
     "Пакеты — на всех ядрах",
     "записи пакетов читаются, проверяются SHA-256 и декодируются параллельно, а принимаются в порядке манифеста: первая ошибка та же",
     "ревью: подменённый огромный файл читался бы на всех ядрах до первой ошибки — размер теперь проверяется до чтения (в L4)"),
    ("L4", "ml-l4-bitmap-validation-20261011.json", "5c3a5a4", "convert",
     "Картинки проверяются без декодирования",
     "те же проверки декодера в том же порядке, но без раскодированных массивов; заголовки — прямо из байтов",
     "ревью: первая версия проверки размера меняла ошибку для нечитаемого файла — исправлено до гейта"),
    ("M1", "ml-m1-bitmap-bytes-compressed-20261011.json", "8aceb53", "memory",
     "Спрайт-листы хранятся сжатыми",
     "байты листов от 64 КиБ — в LZ4 (~13×); распаковка, когда поверхности впервые нужны пиксели: 77 чтений за матч",
     None),
    ("M2", "ml-m2-compact-frame-words-20261011.json", "c4223e5", "memory",
     "Слова кадров — в 94 слотах",
     "вместо словаря [String: Int32] на каждую из 54 800 записей кадров — слоты с маской присутствия; то же равенство и JSON",
     None),
    ("L5", "ml-l5-bitmap-effects-in-place-20261011.json", "1016ca7", "inplace",
     "Эффекты картинок — на месте",
     "каждый эффект копировал таблицы картинок, поверхностей и DC; теперь он бросает ошибку только до первого изменения",
     None),
    ("L6", "ml-l6-frame-heap-index-20261011.json", "e12472a", "search",
     "Куча кадров — двоичным поиском",
     "каждое выделение, запись и поиск перебирали все ~15 000 выделений; теперь поиск по порядку адресов",
     None),
    ("L7", "ml-l7-latin1-text-20261011.json", "961cd99", "convert",
     "Текст Latin-1 без String по символу",
     "разобранные файлы и токены переводятся в строки сразу, а не скаляр за скаляром; строки и байты те же",
     None),
    ("L8", "ml-l8-sound-bytes-once-20261011.json", "e68da21", "inplace",
     "Байты звука читаются один раз",
     "перевод WAV во float копировал запись звука на каждый прочитанный байт",
     None),
    ("M3", "ml-m3-compressed-sheets-trimmed-20261011.json", "1e8006d", "memory",
     "Сжатые листы — по своему размеру",
     "буфер компрессора сохранял резерв: 130 МБ выделено под 52 МБ сжатых данных",
     None),
    ("L9", "ml-l9-implicit-unknown-surfaces-20261011.json", "58d17b6", "convert",
     "Новые поверхности — без массивов",
     "пока пиксели не прочитаны и не записаны, поверхность — «всё неизвестно на нулях», без двух выделенных и обнулённых массивов",
     None),
    ("L10", "ml-l10-text-translation-20261011.json", "0cdf24c", "convert",
     "Текстовый режим — в один массив",
     "flatMap строил массив на каждый байт; теперь CR LF дописываются в один заранее выделенный массив",
     None),
    ("L11", "ml-l11-hardware-sha256-20261011.json", "643ae9f", "parallel",
     "SHA-256 инструкциями процессора",
     "на Android нет CryptoKit: ~700 МБ хешировал переносимый Swift-код. Теперь блок считают инструкции ARMv8 SHA-2 — и только если на 12 входах дайджесты равны Swift",
     None),
    ("L12", "ml-l12-package-loads-every-core-20261011.json", "72e9fcc", "parallel",
     "Восемь ядер вместо четырёх",
     "воркеры Dispatch наследовали привязку главного потока к ядрам 0–3; у загрузчика теперь свои потоки на всех ядрах",
     "ревью: если поток не стартует, done.wait() повиснет навсегда — переписано до гейта"),
    ("L13", "ml-l13-read-ahead-20261011.json", "4615465", "parallel",
     "Пакеты читаются заранее, во время меню",
     "главный поток ~4 с ждал пакеты после повторного чтения стартового; теперь пять пакетов читаются в фоне с конца старта",
     None),
    ("M5a", "ml-m5a-sound-records-20261011.json", "cb426f7", "memory",
     "Одна запись PCM на звук",
     "временная копия звука, занимающая весь буфер, — это и есть запись: два равных набора по 17 МБ стали одним",
     None),
    ("M6", "ml-m6-paged-stage-slots-20261011.json", "5b35a9a", "memory",
     "60 слотов Stage — страницами",
     "запись-сторож делала 60 плоских копий (87 МБ); теперь слоты делят страницы, а заполненный становится плоским",
     "ревью: маленькая страничная запись, перезаписанная в составную, — риск устранён до гейта"),
    ("L14+15", "ml-l14-l15-sounds-in-place-defined-bits-20261011.json", "fa06d04", "inplace",
     "Звуки на месте, маска по 8 байт",
     "регистрация звука копировала оба словаря всех прежних звуков ради отката, который уже есть снаружи; маска определённости — по 8 байт за шаг",
     None),
    ("L16", "ml-l16-objects-in-place-20261011.json", "5aa5250", "inplace",
     "Объекты без копий для отката",
     "первое выделение каждого объекта копировало все прежние (~15 000), хотя любая ошибка всё равно обрывает загрузку каталога",
     None),
    ("L17", "ml-l17-posix-file-facts-20261011.json", "d5fee4d", "convert",
     "lstat вместо resourceValues",
     "проверка каждого файла строила словарь атрибутов — ~1,8 мс на файл на Android",
     "ревью: lstat и старый API по-разному переводят ENAMETOOLONG — ошибки отданы старому API"),
    ("L18+19", "ml-l18-l19-ranges-shared-frame-slots-20261011.json", "97423ae", "search",
     "Пересечения — двоичным поиском",
     "проверка пересечения выделений перебирала все прежние диапазоны; пустые слоты кадров делят одну запись",
     None),
    ("S2", "ml-s2-parallel-asset-extraction-20261011.json", "1e0b93e", "parallel",
     "Распаковка APK на всех ядрах",
     "первый запуск после установки копировал 726 МБ ресурсов по одному файлу кусками по 64 КБ",
     "ревью: при ошибке распаковки может быть назван другой файл — записано как риск"),
    ("M5b", "ml-m5b-sound-copies-20261011.json", "ec84abd", "memory",
     "Остальные копии звука",
     "копии без кэша целых массивов, журналы запросов звука (их читают только тесты) выключены в игре",
     None),
    ("M7a", "ml-m7a-closed-stream-contents-20261011.json", "49bf0bf", "memory",
     "Закрытые потоки без содержимого",
     "загруженное меню держало массивы всех закрытых файлов весь матч, хотя их никто не читает",
     None),
    ("M5c", "ml-m5c-pcm-samples-20261011.json", "b8d1c9b", "memory",
     "PCM вместо float — перевод в микшере",
     "буферы хранят 8/16-битный PCM (16 МБ вместо 32), микшер переводит сэмпл при чтении",
     None),
    ("M5d", "ml-m5d-mixer-raw-mono-20261011.json", "ef7a6b7", "inplace",
     "Микшер через адрес буфера",
     "PCM читается по указателю там, где индексы доказуемо в буфере; моно-голос читает кадр один раз на оба канала",
     "ревью: отрицательный шаг (хосты его не дают) пошёл бы по быстрому пути — исправлено до гейта"),
    ("L20", "ml-l20-menu-bitmap-inputs-in-place-20261011.json", "e184b10", "inplace",
     "Битмапы меню — на месте",
     "каждый запрос битмапа в меню копировал таблицы картинок, поверхностей и DC до двух раз",
     None),
    ("L21", "ml-l21-posix-file-bytes-rejected-20261011.json", "9ed8f6c", "convert",
     "Файлы пакетов сразу в массив — отклонено",
     "поведение равно, выигрыша нет ни на A12, ни на Mac, а кода больше — откат, дифф сохранён",
     None),
    ("M8", "ml-m8-streaming-music-20261011.json", "d90472a", "memory",
     "Музыка потоком — ждёт решения",
     "трек декодируется по мере игры, а не целиком: −50 МиБ на пике, но поток музыки +0,5 мс на тик",
     None),
    ("M9", "ml-m9-shared-uniform-pages-parked-20261011.json", "6b4bffd", "memory",
     "Общие однородные страницы — отложено",
     "A12 −36–40 МиБ PSS, но на Mac footprint вырос на 65–90 МиБ: malloc держал освобождённое грязным",
     None),
]
STATUS = {"L21": "rejected", "M8": "held", "M9": "parked"}
NOTE_UNITS = "A12: VmRSS + VmSwap, кБ /proc ÷ 1024 (МиБ); Mac: phys_footprint_peak утилиты footprint (МБ)"


def phone_side(d, build):
    """Medians/ranges of one build in a gate's phone A/B (M7a's rerun has no summary)."""
    s = (d.get("phone") or {}).get("summary") or {}
    if build in s:
        v = s[build]
        return {"build": build, "runs": v.get("runs"), "load": stat(v.get("loadSeconds")),
                "startToLoaded": stat(v.get("startToLoadedSeconds")), "peak": stat(v.get("peakFootprintMB")),
                "main": stat(v.get("mainMsPerTick")), "render": stat(v.get("renderMsPerTick"))}
    runs = [r for r in d.get("phoneRerun", []) if r["label"].endswith("-" + build)]
    need(runs, f"no phone runs for {build}")
    return {"build": build, "runs": len(runs), "load": runs_stat(runs, "loadSeconds"),
            "startToLoaded": runs_stat(runs, "startToLoadedSeconds"), "peak": runs_stat(runs, "peakFootprintMB"),
            "main": None, "render": None}


def mac_side(d, build):
    v = d["mac"]["summary"][f"frozen-unchecked-{build}"]
    return {"build": build, "runs": v.get("runs"), "load": stat(v.get("loadSeconds")), "peak": stat(v.get("peakResidentMB"))}


def gain(prev, new):
    """'measured' when the new range lies wholly below the previous one, 'worse' wholly above, else 'overlap'."""
    if not prev or not new:
        return None
    if new[2] < prev[1]:
        return "measured"
    if new[1] > prev[2]:
        return "worse"
    return "overlap"


steps = []
for sid, fname, h, fam, name, how, finding in STEPS:
    d = evidence(fname)
    inc, prv = d["increment"], d["previous"]
    runs = (d.get("phone") or {}).get("runs") or d.get("phoneRerun") or []
    sounds = any(r.get("sounds") for r in runs)
    music = any(r.get("music") for r in runs)
    review = d.get("review") or ""
    p_new, p_prev = phone_side(d, inc), phone_side(d, prv)
    m_new, m_prev = mac_side(d, inc), mac_side(d, prv)
    c = by_hash.get(h)
    need(c, f"commit {h} not in span")
    steps.append({
        "id": sid, "hash": h, "time": c["time"], "subject": c["subject"], "status": STATUS.get(sid, "done"),
        "family": fam, "name": name, "how": how, "evidence": fname,
        "review": "independent" if re.match(r"(?i)independent", review) else ("not delegated" if review.startswith("not delegated") else None),
        "reviewFinding": finding,
        "sounds": sounds, "music": music,
        "phone": {"prev": p_prev, "new": p_new,
                  "loadGain": gain(p_prev["load"], p_new["load"]), "peakGain": gain(p_prev["peak"], p_new["peak"])},
        "mac": {"prev": m_prev, "new": m_new,
                "loadGain": gain(m_prev["load"], m_new["load"]), "peakGain": gain(m_prev["peak"], m_new["peak"])},
    })

# M7a: the ledger's phone numbers come from its rerun (ml-m7a-ab2); keep the card's statement for the peak
# L14+15 / L18+19: one gate for two changes (each alone below the phone's noise floor)

# ------------------------------------------------------------------ baseline
base = evidence("ml-baseline-20261010.json")
noise = [r for r in base["phoneRuns"] if "noise" in r["label"]]
l1 = evidence("ml-l1-file-streams-in-place-20261010.json")
p0_gate = [r for r in l1["phone"]["runs"] if r.get("build") == "ml-p0"]
baseline = {
    "a12": {"load": stat(l1["phone"]["summary"]["ml-p0"]["loadSeconds"]),
            "loadNoiseRuns": [r["loadSeconds"] for r in noise],
            "startup": stat(l1["phone"]["summary"]["ml-p0"]["startupSeconds"]),
            "startToLoaded": stat(l1["phone"]["summary"]["ml-p0"]["startToLoadedSeconds"]),
            "peak": stat(l1["phone"]["summary"]["ml-p0"]["peakFootprintMB"]),
            "mainCpuToLoaded": base["phoneRuns"][0]["mainCpuToLoadedSeconds"],
            "startToLoadedProfiled": base["phoneRuns"][0]["startToLoadedSeconds"]},
    "mac": {"load": stat(l1["mac"]["summary"]["frozen-unchecked-ml-p0"]["loadSeconds"]),
            "peak": stat(l1["mac"]["summary"]["frozen-unchecked-ml-p0"]["peakResidentMB"])},
    "profileA12": base["phoneLoadProfile"]["inclusiveMainThread"],
    "profileSamples": base["phoneLoadProfile"]["samples"],
    "data": base["data"],
}
need(abs(baseline["a12"]["load"][0] - 123.915) < 0.01, "baseline load moved")

# ------------------------------------------------------------------ waterfalls (in-gate deltas of committed steps)
done = [s for s in steps if s["status"] == "done"]


def delta(s, side, key):
    a, b = s[side]["prev"][key], s[side]["new"][key]
    return None if not a or not b else r3(a[0] - b[0])


load_parts = [{"id": s["id"], "family": s["family"], "seconds": delta(s, "phone", "load"), "gain": s["phone"]["loadGain"]}
              for s in done if s["phone"]["loadGain"] == "measured"]
mem_parts = [{"id": s["id"], "family": s["family"], "mib": delta(s, "phone", "peak"), "gain": s["phone"]["peakGain"]}
             for s in done if s["phone"]["peakGain"] == "measured" and delta(s, "phone", "peak") > 0]
# the load stopped falling after L18+19 (10:05): later gates measure 5.2-6.3 s, the loading step waiting for the read-ahead
morning = next(s for s in steps if s["id"] == "L18+19")

# the final committed build is L20 (e184b10); its gate and the 4+4 A/B ml-l20-ab4 (sounds on, warm-up first)
l20 = evidence("ml-l20-menu-bitmap-inputs-in-place-20261011.json")
l20_runs = [r for r in l20["phone"]["runs"] + l20["extraPhoneAB"]["ml-l20-ab4"] if r["build"] == "ml-l20"]
audit = evidence("ml-ram-audit-20261011.json")
need("565 (555-581)" in audit["reading"], "RAM audit reading moved")
final = {
    "a12": {"build": "ml-l20", "commit": "e184b10", "runs": len(l20_runs),
            "load": runs_stat(l20_runs, "loadSeconds"), "startToLoaded": runs_stat(l20_runs, "startToLoadedSeconds"),
            "startup": runs_stat(l20_runs, "startupSeconds"),
            "peakAudit": [565, 555, 581], "peakAuditNote": "RAM-аудит 11 окт, HEAD = L20, vs, звук эффектов включён, музыка выключена (MiB)"},
    "mac": {"build": "ml-l20", "load": stat(l20["mac"]["summary"]["frozen-unchecked-ml-l20"]["loadSeconds"]),
            "peak": stat(l20["mac"]["summary"]["frozen-unchecked-ml-l20"]["peakResidentMB"])},
    "cardSummary": "A12 load ~124 s → ~5.5 s, peak footprint ~1.6 GB → ~565 MiB (sounds on, music off), launch to loaded ~12.6 s on the day's phone; Mac load 5.4 → 0.32 s, peak 2.0 GB → ~675 MB; frame time unchanged",
}
need("A12 load ~124 s → ~5.5 s" in card, "card summary moved")
s2 = evidence("ml-s2-parallel-asset-extraction-20261011.json")
fresh = s2["freshRuns"]
final["a12"]["firstLaunch"] = {"before": runs_stat([r for r in fresh if r["label"].endswith("ml-l19")], "startupSeconds"),
                               "after": runs_stat([r for r in fresh if r["label"].endswith("ml-s2")], "startupSeconds")}

dump("loading_steps.json", {
    "title": "MEMORY_LOADING: каждая ступень — A/B прошлой и новой сборки в одной сессии",
    "source": f"{CARD} (Ledger) · docs/evidence/ml-*.json (поля phone, mac, review) · git log {BASE[:7]}..{LAST[:7]}",
    "caveat": ("Galaxy A12 (SM-A125F), debuggable APK, сценарий vs по скрипту app_e2e на виртуальных часах, сеть выключена; "
               "до M5d звук выключен, с M5d эффекты микшируются, M8 и M9 — с музыкой. На телефоне 3 прогона новой сборки против 2 прошлой, "
               "вперемешку; на Mac — 3 на 3, headless-бинарник без проверок эксклюзивности. Медиана [мин, макс]. "
               "Сравнивать можно только пару внутри одного гейта: телефон дрейфует между сессиями."),
    "units": NOTE_UNITS,
    "frozen": FROZEN,
    "families": FAM,
    "commits": len(commits), "tagged": tagged,
    "baseline": baseline,
    "steps": steps,
    "waterfall": {"load": load_parts, "memory": mem_parts,
                  "loadEnd": {"id": morning["id"], "time": morning["time"], "load": morning["phone"]["new"]["load"]},
                  "note": "только ступени, у которых диапазон новой сборки целиком ниже прошлой; остальное — шум и дрейф между сессиями"},
    "final": final,
})

# ------------------------------------------------------------------ race: one typical run each side
p0_runs = noise + p0_gate
pick = lambda rs: sorted(rs, key=lambda r: r["startToLoadedSeconds"])[len(rs) // 2]
b, a = pick(p0_runs), pick(l20_runs)


def phases(r):
    return {"label": r["label"], "startup": r["startupSeconds"], "load": r["loadSeconds"], "total": r["startToLoadedSeconds"],
            "menu": r3(r["startToLoadedSeconds"] - r["startupSeconds"] - r["loadSeconds"]),
            "sounds": bool(r.get("sounds"))}


dump("loading_race.json", {
    "title": "От запуска до загруженного меню на Galaxy A12: один типичный прогон до и после",
    "source": "ml-baseline-20261010.json (phoneRuns), ml-l1-…json (ml-p0), ml-l20-…json (phone.runs, extraPhoneAB.ml-l20-ab4)",
    "caveat": ("Медианный по «запуск → загружено» прогон из всех прогонов сборки: до — ml-p0 (0034e45), 5 прогонов без звука; "
               "после — ml-l20 (e184b10), 7 прогонов со звуком эффектов. Фаза «меню» = всего − старт − загрузка."),
    "frozen": FROZEN,
    "before": phases(b) | {"build": "ml-p0", "commit": "0034e45", "runs": len(p0_runs)},
    "after": phases(a) | {"build": "ml-l20", "commit": "e184b10", "runs": len(l20_runs)},
})

# ------------------------------------------------------------------ method
menu = evidence("ml-menu-phase-check-20261011.json")
ft = evidence("ml-frame-time-audit-20261011.json")
m5d = evidence("ml-m5d-mixer-raw-mono-20261011.json")
m8 = evidence("ml-m8-streaming-music-20261011.json")
m9 = evidence("ml-m9-shared-uniform-pages-parked-20261011.json")
m5c = evidence("ml-m5c-pcm-samples-20261011.json")
m5b = evidence("ml-m5b-sound-copies-20261011.json")


def bench(lines, key):
    for ln in lines:
        m = re.match(rf"{key} ns per voice-frame: median ([\d.]+)\s+range ([\d.]+)-([\d.]+)", ln)
        if m:
            return [float(m.group(1)), float(m.group(2)), float(m.group(3))]
    raise SystemExit(f"collect_loading: no {key} in the mixer benchmark")


a12bench = ft["mixer"]["a12"]
mixer = {"beforeM5c": bench(a12bench, "floatsBefore"), "m5c": bench(a12bench, "m5c"),
         "raw": bench(a12bench, "raw"), "m5d": bench(a12bench, "rawMono"),
         "setup": "A12, обратный вызов 192 кадра, 8 голосов, выход 48 кГц; выходы побитно равны",
         "extraMsPerSecond": 4.423}
need(mixer["m5c"][0] == 48.72 and mixer["m5d"][0] == 36.2, "mixer benchmark moved")

drift_rows = []
for r in menu["earlierGates"]:
    if r["build"] == "ml-s2" and r["startupSeconds"] < 5:   # runs that re-extracted assets are not comparable
        drift_rows.append({"view": "ledger", "when": "10:41", "gate": "S2", "build": "S2", "s": r["startToLoadedSeconds"]})
for r in m5c["phone"]["runs"]:
    if r["build"] == "ml-m5c" and r["startupSeconds"] < 5:
        drift_rows.append({"view": "ledger", "when": "12:30", "gate": "M5c", "build": "M5c", "s": r["startToLoadedSeconds"]})
for r in menu["runs"]:
    drift_rows.append({"view": "session", "when": "15:30", "gate": "check", "build": r["build"][3:].upper(), "s": r["startToLoadedSeconds"]})

# the attribution probe of 10 Oct (a ledger row of the card, not committed as evidence)
m = re.search(r"of (\d+) surfaces \(([\d.]+) GB allocated\) only (\d+)–(\d+) \((\d+)–(\d+) MB\) are touched in a whole vs run, "
              r"and `Bitmap.pixels` is read (\d+) times", card)
need(m, "attribution probe moved")
sheets = re.search(r"sprite-sheet file bytes (\d+) MB \(catalog\) \+ (\d+) MB \(arenas\)", card)
held = re.search(r"130 MB allocated for 52 MB", card)
need(sheets and held, "sprite-sheet sizes moved")
surfaces = {"total": int(m.group(1)), "allocatedGB": float(m.group(2)), "touched": [int(m.group(3)), int(m.group(4))],
            "touchedMB": [int(m.group(5)), int(m.group(6))], "pixelReads": int(m.group(7)),
            "sheetBytesMB": int(sheets.group(1)) + int(sheets.group(2)), "compressedHeldMB": 130, "compressedMB": 52,
            "source": "MEMORY_LOADING.md, Ledger: Attribution probe (not committed), M1, M3"}

ftsum = ft["a12"]["summary"]
m8s, m9s = m8["phone"]["summary"], m9["phone"]["summary"]
dump("loading_method.json", {
    "title": "Как цикл мерил: шум, прогрев, дрейф телефона, время кадра, звук",
    "source": f"{CARD} (Metrics, Comparison protocol, Gates, Method notes, Ledger) · ml-baseline, ml-menu-phase-check, "
              "ml-frame-time-audit, ml-m5d, ml-ram-audit, ml-m8, ml-m9 (docs/evidence)",
    "caveat": "Один телефон (Galaxy A12), debuggable APK; времена в МиБ и секундах как в evidence; запуск → загружено зависит от памяти телефона в этот час.",
    "frozen": FROZEN,
    "noiseFloor": {"a12Load": 0.6, "a12Startup": 0.03, "a12Footprint": 10, "macLoad": 0.2, "macFootprint": 30,
                   "a12PeakRunToRun": 25},
    "warmupFirstRunWaits": [3.13, 1.44, 1.40],
    "drift": {"rows": drift_rows,
              "phone": menu["phoneState"],
              "reading": "S2 12,71–12,75 с против M5b 12,62–12,70 с в одной сессии: те же; +1,2 с — это телефон после полудня"},
    "surfaces": surfaces,
    "frameAudit": {
        "what": "A12, android_speed.py, начало ветки (ml-p0) против HEAD (ml-m5c), vs и Demo, 3 раунда вперемешку, звук выключен",
        "vsMain": [stat(ftsum["ml-p0 vs"]["mainMsPerTick"]), stat(ftsum["ml-m5c vs"]["mainMsPerTick"])],
        "vsRender": [stat(ftsum["ml-p0 vs"]["renderMsPerTick"]), stat(ftsum["ml-m5c vs"]["renderMsPerTick"])],
        "demoMain": [stat(ftsum["ml-p0 demo"]["mainMsPerTick"]), stat(ftsum["ml-m5c demo"]["mainMsPerTick"])],
        "demoRender": [stat(ftsum["ml-p0 demo"]["renderMsPerTick"]), stat(ftsum["ml-m5c demo"]["renderMsPerTick"])],
    },
    "mixer": mixer,
    "m5dInPlay": {"note": m5d["notes"][:400]},
    "ramAudit": {"build": audit["build"], "peakVs": [565, 555, 581], "peakDemo": [566, 551, 579],
                 "nativeAllocated": 1597, "nativeDirty": [405, 450], "allocatorFree": [19, 46],
                 "musicOnPeak": [607, 630], "musicOffPeak": [536, 567], "matchGrowth": [24, 38],
                 "candidates": audit["candidates"], "decision": audit["decision"]},
    "m8": {"peakWith": stat(m8s["ml-m8b"]["peakFootprintMB"]), "peakWithout": stat(m8s["ml-l20"]["peakFootprintMB"]),
           "main": [stat(m8s["ml-l20"]["mainMsPerTick"]), stat(m8s["ml-m8b"]["mainMsPerTick"])],
           "musicThreadMs": {"without": [1.16, 1.22], "with": [1.69, 1.72]}},
    "m9": {"a12EndPss": {"with": [504, 510], "without": [545, 592]},
           "macLoaded": {"with": [670, 682], "without": [556, 598]}},
    "reviewsFound": [s["id"] for s in steps if s["reviewFinding"]],
    "reviews": sum(1 for s in steps if s["review"] == "independent"),
    "notDelegated": [s["id"] for s in steps if s["review"] == "not delegated"],
    "testOnlyFailures": ["M6", "L17", "M5b", "L6"],
})

# ------------------------------------------------------------------ the night: session log (times and counts only)
t0 = dt.datetime(2026, 10, 10, 21, 0, tzinfo=TZ)
t1 = dt.datetime(2026, 10, 11, 20, 1, tzinfo=TZ)   # the human's last turn of this work: the push at 20:00
AXIS_END = dt.datetime(2026, 10, 11, 20, 30, tzinfo=TZ)


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(TZ)


def hours(t):
    return round((t - t0).total_seconds() / 3600, 3)


human, seen = [], []
comps, tools, agent_times = [], {}, []
with open(SESSION, encoding="utf-8", errors="replace") as fh:
    for ln in fh:
        d = json.loads(ln)
        if "timestamp" not in d:
            continue
        t = ts(d["timestamp"])
        if not (t0 <= t <= t1):
            continue
        typ = d.get("type")
        text = None
        if typ == "queue-operation" and d.get("operation") == "enqueue":
            text = str(d.get("content") or "")
        elif typ == "user" and not d.get("isMeta"):
            c = (d.get("message") or {}).get("content")
            parts = c if isinstance(c, list) else [{"type": "text", "text": c}] if isinstance(c, str) else []
            if not any(isinstance(p, dict) and p.get("type") == "tool_result" for p in parts):
                text = " ".join(p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text").strip()
        elif typ == "system" and d.get("subtype") == "compact_boundary":
            comps.append(hours(t))
        elif typ == "assistant":
            agent_times.append(t)
            for p in (d.get("message") or {}).get("content") or []:
                if isinstance(p, dict) and p.get("type") == "tool_use":
                    tools[p["name"]] = tools.get(p["name"], 0) + 1
        if text and (text.startswith("<pasted_content") or not (text.startswith("<") or text.startswith("[")
                     or text.startswith("This session is being continued") or text.startswith("# /loop"))):
            key = hash(text[:200])
            if any(k == key and abs((t - tt).total_seconds()) < 180 for k, tt in seen):
                continue  # a queued turn shows up again when it is delivered (or is pasted twice)
            seen.append((key, t))
            human.append(hours(t))

agent_times.sort()
idle = []
for a_, b_ in zip(agent_times, agent_times[1:]):
    if (b_ - a_).total_seconds() > 30 * 60:
        idle.append([hours(a_), hours(b_)])

dump("loading_night.json", {
    "title": "Ночь цикла памяти и загрузки на одной оси времени",
    "source": "git log 0034e45..6b4bffd (время коммитов) · журнал сессии Claude Code 1f9218ae: только время реплик человека, компакций и сообщений агента, счётчики вызовов",
    "caveat": "Время местное (UTC+2). Реплики человека — время ввода или постановки в очередь; дубли очереди сняты. Тексты реплик в данные не попадают.",
    "frozen": FROZEN,
    "t0": t0.isoformat(), "spanHours": hours(AXIS_END),
    "commits": [{"h": hours(dt.datetime.fromisoformat(c["time"] + ":00+02:00")), "hash": c["hash"]} for c in commits],
    "human": human,
    "compactions": comps,
    "idle": idle,
    "counts": {"bash": tools.get("Bash", 0), "agents": tools.get("Agent", 0), "compactions": len(comps),
               "humanTurns": len(human), "commits": len(commits), "tagged": tagged},
})
print(f"collect_loading: {len(steps)} steps, {len(commits)} commits, {len(human)} human turns, idle {idle}")
