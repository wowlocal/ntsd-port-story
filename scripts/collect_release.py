#!/usr/bin/env python3
"""Regenerate the deck's data/rel_*.json (chapter 18, «Семь часов в меню»):
the menu memory leak, the phone controller and the signed platform release
of 13 Oct 2026.

Usage:
    python3 scripts/collect_release.py ../ntsd-2.4 [REV] [--no-artifacts]

REV defaults to 5f5a8ee4 (branch exp/iphone, 13 Oct 2026, 20:14 CEST), the
commit the chapter is frozen at. Port-repository files are read with
`git show REV:path`, commits with `git log`; nothing in the repository is
modified and no branch is checked out.

Three read-only sources outside the repository fill what git does not hold:

* the release artifacts folder the repo's own evidence names as
  `artifactsRoot` (docs/evidence/release-refresh-20261013.json): GitHub's
  release record as downloaded after publication (asset sizes, upload times,
  digests), the digest check, the packaging failure ledger and the plan.
  Pass --no-artifacts when the drive is not mounted: sizes and upload times
  are then left out (null) and the script says so.
* ~/.codex/sessions/2026/10/13/*.jsonl: only session metadata, models,
  efforts, timestamps, tool-call names and token counters. No message text is
  read into the output.
* the Claude Code session log 1f9218ae: only assistant-message timestamps and
  the timestamps of six user messages (located by a substring match; the text
  itself is not written anywhere).

Times are local (CEST, UTC+2), as in the commits.
"""
import collections
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
FLAGS = {a for a in sys.argv[1:] if a.startswith("--")}
REPO = os.path.abspath(ARGS[0] if ARGS else "../ntsd-2.4")
REV = ARGS[1] if len(ARGS) > 1 else "5f5a8ee4"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
EV = "docs/evidence/"
RS = "docs/research/"
TZ = dt.timezone(dt.timedelta(hours=2))
FROZEN = "состояние на 13 октября 2026, 20:14 (5f5a8ee4)"
CLAUDE_LOG = os.path.expanduser(
    "~/.claude/projects/-Users-michael-Developer-ntsd-2-4/1f9218ae-9d5d-4c4e-a8dd-d5254994839c.jsonl")
CODEX_DAY = os.path.expanduser("~/.codex/sessions/2026/10/13")


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


def must(pattern, text, what, flags=0):
    m = re.search(pattern, text, flags)
    if not m:
        sys.exit(f"collect_release: {what} not found ({pattern!r})")
    return m


def local(ts):
    """ISO timestamp (UTC 'Z' or with offset) -> datetime in CEST."""
    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(TZ)


def hm(ts, seconds=False):
    return local(ts).strftime("%H:%M:%S" if seconds else "%H:%M")


def series(line):
    """'vs-tw-w3e: 0s=676MB 10s=719MB …' -> [[0, 676], [10, 719], …] (a truncated tail is dropped)."""
    return [[int(s), int(v)] for s, v in re.findall(r"(\d+)s=(\d+)MB", line)]


# ---------------------------------------------------------------- memory
def memory():
    card = show(RS + "MENU_MEMORY.md")
    hist = show(RS + "APPLICATION_ITERATION_HISTORY.md")
    ev = evidence("menu-memory-20261013.json")
    obs = ev["observation"]

    gb = float(must(r"at ([\d.]+) GB in Activity Monitor", card, "11.22 GB").group(1))
    hours = must(r"for about (\w+)\s+hours", card, "about seven hours").group(1)
    m = must(r"(\d+) -> (\d+) MB over (\d+) s, linear \(~(\d+) MB per minute, ~([\d.]+) GB per hour\)",
             obs["tvosIpadSimulators"], "simulator growth")
    sim = {"fromMB": int(m[1]), "toMB": int(m[2]), "seconds": int(m[3]),
           "statedMBPerMin": int(m[4]), "statedGBPerHour": float(m[5])}
    sim["mbPerMin"] = round((sim["toMB"] - sim["fromMB"]) / sim["seconds"] * 60, 2)
    m = must(r"live heap (\d+) -> (\d+) MB in (\d+) s, iteration history nodes (\d+) -> (\d+) \(~(\d+) per second\)",
             obs["heapMac"], "mac heap")
    mac = {"heapFromMB": int(m[1]), "heapToMB": int(m[2]), "seconds": int(m[3]),
           "nodesFrom": int(m[4]), "nodesTo": int(m[5]), "nodesPerSecond": int(m[6])}
    m = must(r"nodes (\d+) -> (\d+) in ~(\d+) s \(~(\d+) per second\), receipt arrays ([\d.]+) -> ([\d.]+) MB",
             obs["heapTvos"], "tvOS heap")
    tvos = {"nodesFrom": int(m[1]), "nodesTo": int(m[2]), "seconds": int(m[3]), "nodesPerSecond": int(m[4]),
            "receiptFromMB": float(m[5]), "receiptToMB": float(m[6])}
    m = must(r"receipt arrays ≈(\d+) KB each \((\d+) MB for (\d+) on macOS\)", card, "receipt arrays")
    receipt = {"kbEach": int(m[1]), "mb": int(m[2]), "count": int(m[3])}

    lines = {ln.split(":")[0]: ln for ln in ev["soaks"]["lines"] if re.match(r"^[\w-]+: 0s=", ln)}
    tvos_after = series(lines["tvos-mm-2"])
    heap = ev["soaks"]["heap"]

    def soak(key, label, minutes, clock):
        b, a = heap[f"{key}-tw-w3e"], heap[f"{key}-mm-2"]
        return {"id": key, "label": label, "minutes": minutes, "clock": clock,
                "before": {"startMB": b["start"]["liveMB"], "endMB": b["end"]["liveMB"],
                           "nodesStart": b["start"]["iterationHistoryNodes"], "nodesEnd": b["end"]["iterationHistoryNodes"],
                           "receiptEndMB": b["end"]["receiptArrayMB"],
                           "growthMB": round(b["end"]["liveMB"] - b["start"]["liveMB"], 1)},
                "after": {"startMB": a["start"]["liveMB"], "endMB": a["end"]["liveMB"],
                          "nodesEnd": a["end"]["iterationHistoryNodes"],
                          "growthMB": round(a["end"]["liveMB"] - a["start"]["liveMB"], 1)},
                "footprint": {"before": series(lines[f"{key}-tw-w3e"]), "after": series(lines[f"{key}-mm-2"])}}

    m = must(r"flat at (\d+) MB after warm-up", card, "menu footprint after")
    soaks = [soak("menu", "главное меню", 4, "real"),
             soak("select", "выбор персонажей VS", 3, "real"),
             soak("vs", "сессия VS", None, "virtual")]
    soaks[0]["after"]["footprintFlatMB"] = int(m[1])
    m = must(r"footprint flat at (\d+) MB from 2 minutes on", card, "vs footprint after")
    soaks[2]["after"]["footprintFlatMB"] = int(m[1])

    gate = ev["gate"]
    launches = must(r"crashes (\d+) of (\d+)", " ".join(gate["lines"]), "launches")
    frames = [json.loads(ln)["frames"] for ln in gate["lines"] if ln.startswith('{"frames"')]
    scen = [json.loads(ln) for ln in gate["lines"] if ln.startswith('{"scenario"')]
    mac_ab = gate["macAB"]
    p2 = ev["phoneAB2"]["summary"]

    # the two earlier rounds of the same history (APPLICATION_ITERATION_HISTORY.md)
    r1 = must(r"went ([\d.]+) → ([\d.]+) s\s+per\s+2000\s+by\s+iteration\s+(\d+)", hist, "29 Sep round")
    r2 = must(r"≈([\d,]+) cursors\s+per match", hist, "30 Sep cursors")
    per_match = must(r"\(≈(\d+) MB per match before 2026-09-30\)",
                     show("native/Sources/NTSDCore/OriginalApplicationObservedIteration.swift"), "12 MB per match")
    rounds = [
        {"date": "29 сен", "what": "вся история копировалась на каждой итерации",
         "number": f"{r1[1]} → {r1[2]} с на 2000 итераций меню к итерации {int(r1[3]):,}".replace(",", " ").replace(".", ","),
         "fix": "общий неизменяемый список вместо массива", "source": RS + "APPLICATION_ITERATION_HISTORY.md (Result)"},
        {"date": "30 сен", "what": "хранились курсоры всех тиков игры",
         "number": f"≈{r2[1].replace(',', ' ')} курсоров за матч, ≈{per_match[1]} МБ",
         "fix": "курсор хранится, только если держит ресурс", "source": RS + "APPLICATION_ITERATION_HISTORY.md (Resource-free iterations)"},
        {"date": "13 окт", "what": "итерации меню держат поверхности — хранились целиком",
         "number": f"≈{sim['statedMBPerMin']} МБ в минуту простоя",
         "fix": "каждый ресурс один раз + счётчик итераций", "source": RS + "MENU_MEMORY.md, 340b1a64"},
    ]

    obj = {
        "title": "Рост памяти в меню (MENU_MEMORY), 13 октября",
        "source": f"{RS}MENU_MEMORY.md · {EV}menu-memory-20261013.json · {RS}APPLICATION_ITERATION_HISTORY.md · "
                  f"340b1a64, слит в main как 1c692c22 · git show {REV}",
        "caveat": "11,22 ГБ — то, что автор увидел в Activity Monitor, а не замер агента. Замер — footprint каждые 20 с "
                  "в течение 460 с на симуляторах Apple TV 1080p и iPad Air; всё дальше 460 с на графике — продолжение "
                  "замеренного темпа, не измерение. «После» на tvOS замерено 4 минуты. VS-сессия прогона — на виртуальных часах.",
        "frozenAt": FROZEN,
        "report": {"gb": gb, "hoursApprox": hours, "metric": "Activity Monitor, приложение в симуляторе tvOS/iPad"},
        "sims": sim, "mac": mac, "tvos": tvos, "receipt": receipt,
        "after": {"tvosFlatMB": tvos_after[-1][1], "tvosMinutes": 4, "tvosSeries": tvos_after},
        "soaks": soaks,
        "gate": {"label": gate["label"], "prev": gate["prev"],
                 "launches": int(launches[2]), "crashes": int(launches[1]),
                 "scenarioRuns": len(scen), "scenariosEqual": sum(1 for s in scen if s.get("result") == "equal"),
                 "frameChecks": frames,
                 "macMsPerTick": {"before": mac_ab["frozen-unchecked-tw-w3e"]["completeMsPerTick"]["median"],
                                  "after": mac_ab["frozen-unchecked-mm-2"]["completeMsPerTick"]["median"]},
                 "a12MainMsPerTick": {"before": p2["tw-w3e"]["mainMsPerTick"]["median"],
                                      "after": p2["mm-2"]["mainMsPerTick"]["median"]},
                 "review": "независимое ревью только для чтения: OK"},
        "rounds": rounds,
        "commits": {"base": "df74758a", "fix": "340b1a64", "merge": "1c692c22",
                    "mergeTime": git("log", "-1", "--format=%cd", "--date=format:%H:%M", "1c692c22").strip()},
    }
    dump("rel_memory.json", obj)
    return obj


# ---------------------------------------------------------------- controller
def controller():
    card = show(RS + "PHONE_CONTROLLER.md")
    c1 = evidence("phone-controller-c1-20261013.json")
    c2 = evidence("phone-controller-c2-20261013.json")
    c3 = evidence("phone-controller-c3-20261013.json")
    code = show("native/Sources/NTSDAndroid/NTSDAndroidGamepads.swift")
    control = show("native/Sources/NTSDCore/Resources/OriginalStartup/data/control.txt")
    ai = show("native/Sources/NTSDCore/OriginalCharacterAI.swift")

    guess = must(r"\| C0 \| The device is most likely a ([^|;]+?);", card, "C0 guess").group(1).strip()
    dev = c2["controller"]
    raw = c2["rawEventsOnController"]["event3"]

    # the port's button bits (Android key -> WinMM button) straight from the code
    bits = dict(re.findall(r"case Int32\(AKEYCODE_BUTTON_([ABXY])\),Int32\(AKEYCODE_BUTTON_\d\): bit = (\d)", code))
    if sorted(bits) != ["A", "B", "X", "Y"]:
        sys.exit("collect_release: button bits not found in NTSDAndroidGamepads.swift")
    winmm = {k: {"1": 1, "2": 2, "4": 3, "8": 4}[v] for k, v in bits.items()}
    must(r"schedule\(deadline:\.now\(\) \+ \.milliseconds\((\d+)\),repeating:\.milliseconds\(\1\)\)", code, "25 ms period")
    period = int(re.search(r"repeating:\.milliseconds\((\d+)\)", code)[1])

    # control.txt: 4 players x 11 fields: device (0 keyboard, 1/2 joystick 1/2), 7 key rows, 3 joystick buttons
    rows = must(r"enum Key: Int \{ case up = 0xcd, ([a-z, ]+) \}", ai, "key order").group(1)
    order = ["up"] + [s.strip() for s in rows.split(",")]
    players = []
    for i, ln in enumerate(control.replace("\r", "").split("\n")[:4]):
        f = [int(x) for x in ln.split()]
        players.append({"player": i + 1, "device": f[0], "keys": f[1:8],
                        "buttons": {order[4 + j]: f[8 + j] + 1 for j in range(3)}})
    p3 = players[2]
    if p3["device"] != 1:
        sys.exit("collect_release: player 3 is not on joystick 1 in control.txt")
    action_ru = {"attack": "атака", "jump": "прыжок", "defend": "защита"}
    game_of_button = {b: action_ru[a] for a, b in p3["buttons"].items()}

    def ctl(id_, label, evdev, android, port, game, events, kind):
        return {"id": id_, "label": label, "evdev": evdev, "android": android, "port": port,
                "game": game, "events": events, "kind": kind}

    hat = raw.get("ABS_HAT0X", 0) + raw.get("ABS_HAT0Y", 0)
    controls = [
        ctl("ls", "левый стик", "ABS_X · ABS_Y (0–255, покой 0x80)", "AXIS_X · AXIS_Y (−1…1)",
            "оси X/Y WinMM, 0–65535; уступает крестовине", "движение ← → ↑ ↓ (игрок 3)",
            raw["ABS_X"] + raw["ABS_Y"], "axis"),
        ctl("dp", "крестовина", "ABS_HAT0X · ABS_HAT0Y (−1…1)", "AXIS_HAT_X · AXIS_HAT_Y",
            "оси X/Y WinMM — поверх стика", "движение ← → ↑ ↓ (игрок 3)", hat, "axis"),
        ctl("a", "A", "BTN_SOUTH", "KEYCODE_BUTTON_A", f"кнопка {winmm['A']}", game_of_button.get(winmm["A"], "—"),
            raw.get("BTN_SOUTH", 0), "button"),
        ctl("b", "B", "BTN_EAST", "KEYCODE_BUTTON_B", f"кнопка {winmm['B']} (не «Назад»)",
            game_of_button.get(winmm["B"], "—"), raw.get("BTN_EAST", 0), "button"),
        ctl("x", "X", "BTN_NORTH (= BTN_X)", "KEYCODE_BUTTON_X", f"кнопка {winmm['X']}",
            game_of_button.get(winmm["X"], "—"), raw.get("BTN_NORTH", 0), "button"),
        ctl("y", "Y", "BTN_WEST (= BTN_Y)", "KEYCODE_BUTTON_Y", f"кнопка {winmm['Y']}",
            game_of_button.get(winmm["Y"], "не назначена у игрока 3"), raw.get("BTN_WEST", 0), "button"),
        ctl("rs", "правый стик", "ABS_Z · ABS_RZ", "AXIS_Z · AXIS_RZ", "не читается", "—",
            raw["ABS_Z"] + raw["ABS_RZ"], "unused"),
        ctl("lb", "LB", "BTN_TL", "KEYCODE_BUTTON_L1", "поглощается, без роли", "—", raw.get("BTN_TL", 0), "unused"),
        ctl("rb", "RB", "BTN_TR", "KEYCODE_BUTTON_R1", "поглощается, без роли", "—", raw.get("BTN_TR", 0), "unused"),
        ctl("lt", "LT", "BTN_TL2 + ABS_BRAKE", "KEYCODE_BUTTON_L2 · AXIS_BRAKE", "без роли", "—",
            raw.get("BTN_TL2", 0) + raw.get("ABS_BRAKE", 0), "unused"),
        ctl("rt", "RT", "BTN_TR2 + ABS_GAS", "KEYCODE_BUTTON_R2 · AXIS_GAS", "без роли", "—",
            raw.get("BTN_TR2", 0) + raw.get("ABS_GAS", 0), "unused"),
        ctl("sel", "Select", "BTN_SELECT", "KEYCODE_BUTTON_SELECT", "без роли", "—", raw.get("BTN_SELECT", 0), "unused"),
        ctl("start", "Start", "BTN_START", "KEYCODE_BUTTON_START", "без роли", "—", raw.get("BTN_START", 0), "unused"),
        ctl("mode", "кнопка Razer", "BTN_MODE", "KEYCODE_BUTTON_MODE", "без роли", "—", raw.get("BTN_MODE", 0), "unused"),
    ]

    runs = c2["timeline"]["runs"]
    att = c2["timeline"]["controllerAttached"]
    m1 = must(r"between the ([\d:]+) and ([\d:]+) samples, removed by ([\d:]+)", att[0], "first attach")
    m2 = must(r"^([\d:]+) to ([\d:]+)$", att[1], "second attach")
    spans = [{"earliest": m1[1], "from": m1[2], "to": m1[3], "note": f"подключён между опросами в {m1[1]} и {m1[2]}, отключён к {m1[3]}"},
             {"from": m2[1], "to": m2[2], "note": "подключён всю игру"}]
    played = next(r for r in runs if r.get("controllerAtLaunch"))
    sig = must(r"(\d+) ms after the window became invisible", " ".join(c2["findings"]), "SIGSEGV delay")
    first_fail = sum(1 for ln in c1["firstRun"] if '"differs"' in ln)
    iframes = next(json.loads(ln)["frames"] for ln in c1["checks"]["lines"] if ln.startswith('{"frames"'))
    screen_pt = must(r"iPhone's (\d+)x(\d+) points", c1["change"], "iPhone points")
    fit = [json.loads(re.search(r"\{.*\}", ln)[0]) for ln in c1["checks"]["lines"] if ln.startswith("fit ")]

    obj = {
        "title": "Контроллер для телефона (PHONE_CONTROLLER C0–C3), 13 октября",
        "source": f"{RS}PHONE_CONTROLLER.md · {EV}phone-controller-c1/c2/c3-20261013.json · "
                  "native/Sources/NTSDAndroid/NTSDAndroidGamepads.swift · data/control.txt оригинала (ресурс порта) · "
                  f"f340f1e2 · d4619cbc · 5f5a8ee4 · git show {REV}",
        "caveat": "Модель с фото C0 определил неверно; имя устройства — из его собственного USB-отчёта на Pixel 10. "
                  "Счётчики событий — сырые события evdev за всю запись (нажатия и отпускания), не только за матч. "
                  "Что игра получала второй джойстик от пустого интерфейса — вывод из кода и списка устройств: число джойстиков "
                  "на Android не логируется. Проверка C3 на телефоне не проведена. Kishi V2 на Mac и iOS не наблюдался. "
                  "Роли кнопок — значения control.txt по умолчанию для игрока 3 (джойстик 1); игрок может переназначить.",
        "frozenAt": FROZEN,
        "guess": guess,
        "device": {"name": dev["name"], "vendor": dev["usb"]["vendor"], "product": dev["usb"]["product"],
                   "phone": c2["phone"]["model"].split(" (")[0], "android": c2["phone"]["android"]},
        "interfaces": dev["hidNodes"], "androidDevices": dev["androidInputDevices"],
        "rawEvents": raw, "consumerEvents": c2["rawEventsOnController"]["event4"],
        "samplingMs": period, "winmmButtons": winmm, "player3": p3, "players": players, "keyOrder": order,
        "controls": controls,
        "runs": runs, "attached": c2["timeline"]["controllerAttached"], "attachedSpans": spans,
        "played": {"from": played["from"], "to": played["to"], "pid": played["pid"]},
        "sigsegvMs": int(sig[1]),
        "iphone": {"bundle": "local.ntsd.native.iphone", "simulator": "iPhone 17 Pro",
                   "screenPt": [int(screen_pt[1]), int(screen_pt[2])], "window": [794, 550], "toldMin": [800, 600],
                   "firstRunStopped": first_fail, "scenarios": len(c1["firstRun"]), "frames": iframes,
                   "screenshots": fit},
        "c3": {"change": c3["change"], "emulator": c3["gates"]["emulator"], "pixel": c3["gates"]["pixel"],
               "harnessError": c3["gates"]["harnessError"]},
    }
    dump("rel_controller.json", obj)
    return obj


# ---------------------------------------------------------------- release
FAILURE_CLASS = [  # (prefix of failures.json "operation", platform, cause, short Russian gloss)
    ("macOS signing round 1", "macos", "keychain", "подпись macOS: связка ключей заперта"),
    ("Android release round 1", "android", "keychain", "подпись APK: секрет в связке ключей недоступен"),
    ("Linux ARM64 package check round 1", "linux", "appledouble", "Linux: файлы ._ с диска ExFAT сломали запуск"),
    ("Linux ARM64 package check round 2", "linux", "scaling", "Linux: клик по координатам игры, а окно уже масштабируется"),
    ("Linux package mechanism round 3", "linux", "appledouble", "Linux: матч VS отличился только файлами ._ в оверлее"),
    ("task-owned archived-cache cleanup preflight", "linux", "harness", "очистка кэшей: проверка процессов дважды ошиблась — остановилась до удаления"),
    ("Web scenario invocation round 1", "web", "harness", "Web: сценарий «VS» вместо «vs»"),
    ("security unlock-keychain", "macos", "keychain", "открыть связку без пароля нельзя"),
    ("launchctl asuser", "macos", "keychain", "перейти в сеанс пользователя не дали"),
    ("Android release package smoke", "android", "appledouble", "APK: чёрный экран — файлы ._ в списке ассетов"),
    ("Android Aqua signer initial run", "android", "keychain", "подписчик в сеансе Aqua не нашёл Java"),
    ("APK payload verification", "android", "harness", "проверка APK ждала точный список ZIP, а подпись добавляет файлы"),
    ("Android adb invocation", "android", "harness", "adb нет в PATH"),
    ("macOS Aqua job round 1", "macos", "keychain", "задача в сеансе Aqua не стартовала с путями на внешнем диске"),
    ("Public GitHub API download verifier", "publish", "harness", "Python urllib: соединение закрыто — дальше через curl"),
]


def matrix(ev, notary, art):
    """Per-platform check cells in Russian; every number is pulled out of the evidence strings."""
    def sec(text):
        return must(r"VS (?:round 4 )?equal \(([\d.]+) s\)", text, "VS seconds")[1].replace(".", ",")
    mac, la, lx, win, web, an = (ev[k] for k in ("macOS", "linux-aarch64", "linux-x86_64", "windows", "web", "android"))
    passed = sum(1 for x in mac["scenarios"] if x["result"] == "pass")
    nhash = must(r"(\d+) file hashes", win["checks"], "windows hashes")[1]
    gz = must(r"gzip (\d+) \+ brotli (\d+)", web["checks"], "web gzip/brotli")
    wsec = must(r"VS each equal at ([\d.]+)s", web["checks"], "web VS")[1].replace(".", ",")
    pixels = None
    if art:
        for ln in open(os.path.join(art, "web-checks2.log")):
            if ln.startswith("{"):
                pixels = json.loads(ln)["page"]["check"]
                break
    px = f"0 из {pixels['pixels']:,} пикселей".replace(",", " ") if pixels and pixels["mismatchedPixels"] == 0 else "0 отличий"
    gk = (notary.get("dmg") or {}).get("source", "Notarized Developer ID")
    labels = {"macos": "macOS 0.5.0", "android": "Android ARM64", "windows": "Windows x86-64",
              "linux-aarch64": "Linux ARM64", "linux-x86_64": "Linux x86-64", "web": "Web"}
    rows = [
        {"id": "macos", "ids": ["macos"], "label": labels["macos"], "pkg": "DMG",
         "integrity": "hdiutil: образ цел",
         "launch": f"{passed} из {len(mac['scenarios'])} сценариев приложения из пакета",
         "vs": "= эталон, в составе сценариев",
         "signing": f"Developer ID; нотаризация app и DMG: Accepted; staple; Gatekeeper: {gk}",
         "where": "этот Mac", "boundary": None},
        {"id": "android", "ids": ["android"], "label": labels["android"], "pkg": "APK",
         "integrity": "ассеты — точный размер, содержимое не изменилось",
         "launch": "эмулятор: установка, холодный старт, главное меню",
         "vs": None,
         "signing": "прежний release-ключ, сертификат тот же",
         "where": "эмулятор", "boundary": "на телефоне не запускали"},
        {"id": "windows", "ids": ["windows"], "label": labels["windows"], "pkg": "ZIP",
         "integrity": f"хэши {int(nhash):,} файлов + набор каталогов".replace(",", " "),
         "launch": "шрифт GDI SYSTEM_FONT, музыка из пакета",
         "vs": f"= эталон, {sec(win['checks'])} с",
         "signing": None,
         "where": "CrossOver", "boundary": "настоящий Windows — нет"},
        {"id": "linux", "ids": ["linux-aarch64", "linux-x86_64"], "label": "Linux ARM64 и x86-64", "pkg": "2 × tar.gz",
         "integrity": "члены архива = манифест",
         "launch": "ldd, музыка, шрифт; ввод X11 доходит до матча",
         "vs": f"= эталон, {sec(la['checks'])} и {sec(lx['checks'])} с",
         "signing": None,
         "where": "контейнеры Ubuntu; x86-64 — через Rosetta", "boundary": "железо — нет"},
        {"id": "web", "ids": ["web"], "label": labels["web"], "pkg": "ZIP",
         "integrity": f"хэши файлов; gzip {int(gz[1]):,} + brotli {int(gz[2]):,} форм".replace(",", " "),
         "launch": "свежий wasm в Chromium и WebKit",
         "vs": f"= эталон, {wsec} с; контрольный кадр — {px}",
         "signing": None,
         "where": "Chromium + WebKit", "boundary": "архив, не сайт"},
    ]
    return {"labels": labels, "rows": rows}


def release(art):
    ev = evidence("release-refresh-20261013.json")
    tag_commit = git("rev-list", "-n", "1", ev["tag"]).strip()[:8]
    branch = "origin/release/" + ev["tag"]
    branch_head = git("rev-parse", "--short=8", branch).strip()
    in_main = subprocess.run(["git", "-C", REPO, "merge-base", "--is-ancestor", tag_commit, "origin/main"]).returncode == 0

    pkgs = [
        ("macos", "macOS 14+ · Apple silicon", ev["macOS"]),
        ("android", "Android 9+ · ARM64", ev["android"]),
        ("windows", "Windows x86-64", ev["windows"]),
        ("linux-aarch64", "Linux ARM64", ev["linux-aarch64"]),
        ("linux-x86_64", "Linux x86-64", ev["linux-x86_64"]),
        ("web", "Web · статический хостинг", ev["web"]),
    ]
    platforms = []
    for pid, label, p in pkgs:
        platforms.append({"id": pid, "label": label, "archive": p["archive"], "sha256": p["sha256"],
                          "checks": p.get("checks"), "signing": p.get("signing"), "boundaries": p.get("boundaries"),
                          "commit": re.search(r"-([0-9a-f]{7})\.", p["archive"])[1] if pid != "macos" else ev["sourceCommit"][:7]})
    mac = ev["macOS"]
    scen = mac["scenarios"]

    assets, published, pub_meta, failures, plan, notary = None, None, {}, [], {}, {}
    if art:
        dig = json.load(open(os.path.join(art, "published-digest-verification.json")))
        rel = json.load(open(os.path.join(art, "latest-release.json")))
        up = {a["name"]: a for a in rel["assets"]}
        assets = []
        for a in dig["assets"]:
            g = up[a["name"]]
            if g["digest"] != "sha256:" + a["sha256"] or g["size"] != a["bytes"]:
                sys.exit(f"collect_release: GitHub record and digest check disagree on {a['name']}")
            kind = "sums" if a["name"].endswith((".sha256", "SHA256SUMS.txt")) else (
                "manifest" if a["name"].endswith(".manifest.json") else "package")
            assets.append({"name": a["name"], "bytes": a["bytes"], "sha256": a["sha256"], "kind": kind,
                           "uploaded": hm(g["created_at"], True), "result": a["result"]})
        assets.sort(key=lambda a: a["uploaded"])
        pub_meta = {"name": rel["name"], "id": rel["id"], "published": hm(rel["published_at"], True),
                    "updated": hm(rel["updated_at"], True), "prerelease": rel["prerelease"], "draft": rel["draft"],
                    "latest": dig["latest"], "digestResult": dig["result"]}
        raw = json.load(open(os.path.join(art, "failures.json")))
        if len(raw) != len(FAILURE_CLASS):
            sys.exit("collect_release: failures.json changed; update FAILURE_CLASS")
        for i, f in enumerate(raw):
            pre, plat, cause, ru = FAILURE_CLASS[i]
            if not f["operation"].startswith(pre):
                sys.exit(f"collect_release: unexpected failure #{i}: {f['operation']}")
            failures.append({"n": i + 1, "operation": f["operation"], "platform": plat, "cause": cause, "ru": ru,
                             "result": f.get("result"),
                             "next": f.get("correction") or f.get("status") or f.get("boundary") or f.get("cause")
                             or f.get("action") or f.get("planAfterThreeRounds") or f.get("storage")})
        pl = json.load(open(os.path.join(art, "plan.json")))
        plan = {"time": hm(pl["date"], True), "owner": pl["owner"], "scope": pl["scope"],
                "excluded": pl["excluded"], "bounds": pl["bounds"], "review": pl["review"]}
        for what in ("app", "dmg"):
            n = json.load(open(os.path.join(art, f"NTSD-Native-0.5.0.{what}.notary.json")))
            s = open(os.path.join(art, f"NTSD-Native-0.5.0.{what}.spctl.txt")).read()
            notary[what] = {"status": n["status"], "gatekeeper": "accepted" if ": accepted" in s else "?",
                            "source": must(r"source=(.+)", s, "spctl source")[1].strip()}
    else:
        print("collect_release: --no-artifacts: asset sizes, upload times and the failure ledger are left out")

    obj = {
        "title": "Подписанный релиз на шесть платформ, 13 октября",
        "source": f"{EV}release-refresh-20261013.json · {RS}CURRENT_WORK.md · 2c4db98b · 9c700dae · 0b5d4621 · "
                  f"{branch} · тег {ev['tag']} · папка артефактов из evidence: {ev['artifactsRoot']} "
                  "(published-digest-verification.json, latest-release.json, failures.json, plan.json, *.notary.json, *.spctl.txt)",
        "caveat": "Размеры и время загрузки — из записи GitHub о релизе, сохранённой агентом после публикации (gh CLI сейчас "
                  "не авторизован, перепроверить вживую нельзя). Пакетные проверки — в контейнерах, CrossOver, эмуляторе и браузерах; "
                  "настоящие Windows, Linux-железо и телефон с этим APK не проверялись. Независимого ревью у релиза не было.",
        "frozenAt": FROZEN,
        "tag": ev["tag"], "tagCommit": tag_commit, "tagInMain": in_main,
        "releaseBranch": branch.replace("origin/", ""), "releaseBranchHead": branch_head,
        "nativeTree": ev["sourceNativeTree"][:12], "macVersion": mac["version"],
        "url": ev["publication"]["url"], "status": ev["status"],
        "labelChange": ev["publication"]["labelChange"],
        "publication": pub_meta,
        "macScenarios": [{"scenario": s["scenario"], "result": s["result"]} for s in scen],
        "signing": {"macos": mac["signing"], "android": ev["android"]["signing"],
                    "androidCertSha256": ev["android"]["certificateSHA256"]},
        "notary": notary,
        "platforms": platforms, "assets": assets, "failures": failures, "plan": plan,
        "excluded": ev["excluded"], "review": ev["review"],
        "downloadBoundary": ev["publication"]["downloadBoundary"],
        "androidFailedRound": ev["android"]["failedRound"],
    }
    if assets:
        obj["totalBytes"] = sum(a["bytes"] for a in assets)
    obj["matrix"] = matrix(ev, notary, art)
    dump("rel_release.json", obj)
    return obj


# ---------------------------------------------------------------- day: who did what, when
def codex_sessions():
    out = []
    for path in sorted(glob.glob(os.path.join(CODEX_DAY, "*.jsonl"))):
        meta, first, last, models, efforts, approval, sandbox = None, None, None, set(), set(), set(), set()
        tools, turns, tokens = collections.Counter(), 0, None
        for line in open(path):
            try:
                o = json.loads(line)
            except ValueError:
                continue
            t, p = o.get("type"), o.get("payload") or {}
            ts = o.get("timestamp")
            if ts:
                first = first or ts
                last = ts
            if t == "session_meta":
                first = p.get("timestamp") or first
                src = p.get("source")
                meta = {"id": p["id"][:8], "originator": p.get("originator"), "cli": p.get("cli_version"),
                        "role": "guardian" if isinstance(src, dict) else "main",
                        "branch": (p.get("git") or {}).get("branch"),
                        "commit": ((p.get("git") or {}).get("commit_hash") or "")[:8],
                        "cwd": os.path.basename(p.get("cwd") or "")}
            elif t == "turn_context":
                models.add(p.get("model"))
                efforts.add(p.get("effort"))
                approval.add(p.get("approval_policy"))
                sb = p.get("sandbox_policy")
                sandbox.add(sb.get("type") if isinstance(sb, dict) else sb)
            elif t == "response_item" and p.get("type") in ("function_call", "custom_tool_call"):
                tools[p.get("name")] += 1
            elif t == "event_msg" and p.get("type") == "task_started":
                turns += 1
            elif t == "event_msg" and p.get("type") == "token_count" and p.get("info"):
                tokens = p["info"]["total_token_usage"]
        out.append({**(meta or {}), "file": os.path.basename(path)[:27],
                    "start": hm(first, True), "end": hm(last, True),
                    "model": sorted(m for m in models if m), "effort": sorted(e for e in efforts if e),
                    "approval": sorted(a for a in approval if a), "sandbox": sorted(s for s in sandbox if s),
                    "turns": turns, "toolCalls": sum(tools.values()), "tools": dict(tools),
                    "tokens": {"total": tokens["total_tokens"], "input": tokens["input_tokens"],
                               "cached": tokens["cached_input_tokens"], "output": tokens["output_tokens"]} if tokens else None})
    return out


USER_MARKS = [  # (key, substring in the user's message) — only the timestamp is kept
    ("memory", "по памяти не утекает"),
    ("photo", "джойстик для мобильных"),
    ("iphone", "iPhone отдельную сборку"),
    ("caffeine", "убирай кофеин"),
    ("pixel", "поставь сборку на подключенный pixel"),
    ("works", "все работает"),
]


def claude_session():
    hours, msgs, model = collections.Counter(), [], collections.Counter()
    marks = {}
    for line in open(CLAUDE_LOG):
        try:
            o = json.loads(line)
        except ValueError:
            continue
        ts = o.get("timestamp", "")
        if not ts.startswith("2026-10-13"):
            continue
        if o.get("type") == "assistant":
            t = local(ts)
            hours[t.hour] += 1
            msgs.append(t)
            model[(o.get("message") or {}).get("model")] += 1
            continue
        text = o.get("content") if o.get("type") == "queue-operation" else None
        if o.get("type") == "user":
            c = (o.get("message") or {}).get("content")
            if isinstance(c, str):
                text = c
            elif isinstance(c, list):
                text = " ".join(x.get("text", "") for x in c if x.get("type") == "text")
        if not text or text.startswith("This session is being continued"):
            continue
        for key, needle in USER_MARKS:
            if needle in text and key not in marks:
                marks[key] = hm(ts)
    msgs.sort()
    gaps = sorted(((b - a, a, b) for a, b in zip(msgs, msgs[1:])), reverse=True)[:1]
    return {"id": "1f9218ae", "model": model.most_common(1)[0][0], "assistantMessages": len(msgs),
            "first": msgs[0].strftime("%H:%M"), "last": msgs[-1].strftime("%H:%M"),
            "byHour": [{"hour": h, "messages": hours[h]} for h in sorted(hours)],
            "longestGap": {"from": gaps[0][1].strftime("%H:%M"), "to": gaps[0][2].strftime("%H:%M"),
                           "minutes": round(gaps[0][0].total_seconds() / 60)}}, marks


def day():
    log = git("log", REV, "--since=2026-10-13T00:00:00+02:00",
              "--format=%h%x09%cd%x09%s%x09%(trailers:key=Co-Authored-By,valueonly,separator=%x3B)%x1e", "--date=format:%H:%M")
    commits = []
    for ln in [r.strip() for r in log.split("\x1e") if r.strip()]:
        h, t, s, tr = (ln.split("\t") + [""])[:4]
        commits.append({"hash": h, "time": t, "subject": s, "trailer": "Claude" in tr})
    commits.reverse()
    span = f"8840eb3..{REV}"
    total = int(git("rev-list", "--count", span).strip())
    merges = int(git("rev-list", "--count", "--merges", span).strip())
    authors = collections.Counter(git("log", span, "--format=%an").split("\n")[:-1])
    without = []
    for ln in [r.strip() for r in git("log", span, "--format=%h%x09%cd%x09%s%x09%(trailers:key=Co-Authored-By,valueonly,separator=%x3B)%x1e",
                                      "--date=format:%d.%m %H:%M").split("\x1e") if r.strip()]:
        h, t, s, tr = (ln.split("\t") + [""])[:4]
        if "Claude" not in tr:
            body = git("show", "-s", "--format=%b", h).strip()
            without.append({"hash": h, "time": t, "subject": s, "body": "пустое" if not body else "есть"})
    claude, marks = claude_session()
    obj = {
        "title": "Кто что делал 13 октября: сессии агентов и коммиты",
        "source": f"git log {REV} (коммиты 13 октября, трейлер Co-Authored-By) · git rev-list {span} · "
                  "~/.codex/sessions/2026/10/13/*.jsonl (только session_meta, turn_context, отметки времени, имена "
                  "инструментов, счётчики токенов) · ~/.claude/projects/…/1f9218ae….jsonl (только время сообщений)",
        "caveat": "Автор в git у всех коммитов один — Michael: агенты коммитят под учёткой автора, отличает их только трейлер. "
                  "То, что три коммита без трейлера сделал Codex, следует из совпадения времени с его сессией (14:24–15:28), "
                  "из ветки и коммита в её метаданных и из plan.json релиза (owner: Codex); текст сессии не читался. "
                  "Сессия Codex Desktop в 06:28 коммитов не оставила.",
        "frozenAt": FROZEN,
        "commits": commits,
        "since": {"span": span, "total": total, "merges": merges, "withTrailer": total - len(without),
                  "without": without, "authors": dict(authors)},
        "claude": claude, "codex": codex_sessions(), "user": marks,
    }
    dump("rel_day.json", obj)
    return obj


if __name__ == "__main__":
    ev = evidence("release-refresh-20261013.json")
    art = None if "--no-artifacts" in FLAGS else ev["artifactsRoot"]
    if art and not os.path.isdir(art):
        sys.exit(f"collect_release: {art} is not mounted; pass --no-artifacts to skip it")
    m = memory()
    c = controller()
    r = release(art)
    d = day()
    print(f"rel_memory: {m['sims']['mbPerMin']} MB/min, report {m['report']['gb']} GB")
    print(f"rel_controller: {c['device']['name']} {c['device']['vendor']}:{c['device']['product']}, {len(c['controls'])} controls")
    print(f"rel_release: {len(r['assets'] or [])} assets, {len(r['failures'])} failures, tag {r['tag']} -> {r['tagCommit']}")
    print(f"rel_day: {d['since']['total']} commits since 8840eb3, {d['since']['withTrailer']} with the trailer, "
          f"{len(d['codex'])} Codex sessions, user marks {d['user']}")
