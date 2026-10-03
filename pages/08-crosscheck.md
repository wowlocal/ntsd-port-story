---
layout: chapter
num: 8
total: 12
kicker: Глава восьмая
dates: 2–3 октября
image: /img/screens/15-summary-mac-vs-original-side-by-side.jpg
stats: 47 из 47 случайных матчей равны · 156 730 сверенных тиков · /loop
---

# Сверка с оригиналом

Хватит отдельных функций: обе программы играют одни и те же матчи целиком — и сравнивают итоги прямо из памяти.

---

<Kicker>2 октября · детектив</Kicker>

# Оракул разделял нашу ошибку

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-2">
<div class="small ink2">

Девять целых матчей совпали — но **записями обменяться было нельзя**: каждая сторона отвергала чужие файлы: *«Recording file are recorded in a LF2 with some data files … different from yours»*.

- Сумма каталога: у оригинала `0x1ec3356`, у порта `0x1e046b2` — при 1 194 одинаковых файлах данных.
- Точка останова на загрузчике `0x40ef70`: оригинал уходит вперёд ровно на **5239 за объект** и **3749 за фон**.
- Причина: из-за lookahead VC80 цикл `fscanf("%c")`/`feof` не декодирует последний символ файла — и последний токен считается **дважды**.

<div class="card mt-2" style="border-color: rgba(255,138,61,.5)">
<div class="small"><b>Мораль.</b> Unicorn-оракул давал то же неверное значение, что и порт: оба опирались на одну модель CRT. Поймал ошибку только настоящий рантайм.</div>
</div>

</div>
<div>

<div class="card text-center">
<div class="xsmall muted">контрольная сумма порта + веса двойных токенов</div>
<div class="display mt-2" style="font-size: 1.15rem; line-height: 1.6">31 475 378<br>+ 137 × 5 239 <span class="xsmall muted">(&lt;frame_end&gt;)</span><br>+ 17 × 3 749 <span class="xsmall muted">(layer_end)</span></div>
<div class="mt-2" style="border-top: 1px solid var(--axis); padding-top: .5rem"><span class="display hl" style="font-size: 1.5rem">= 32 256 854</span></div>
<div class="mono small muted mt-1">0x1e046b2 → 0x1ec3356</div>
</div>

<div class="xsmall muted mt-2 mb-1">OriginalObjectLoader.swift: если на EOF новый токен не прочитан, в сумму снова идёт прежний</div>

```swift
while !input.eof {
    if let next = try input.observedToken() { token = next }
    guard let current = token else {
        throw Self.error("No initialized outer token")
    }
    for (index, scalar) in current.unicodeScalars.enumerated() {
        checksum &+= UInt32(bitPattern: Int32(Int8(
            bitPattern: UInt8(scalar.value)))) &* UInt32(index)
    }
```

</div>
</div>

<div class="source">3313088 · 53bc59e · docs/research/APPLICATION_CATALOG_CHECKSUM.md</div>

---

<Kicker>как играет пара программ</Kicker>

# Одна запись — две программы — одна таблица итогов

<FlowDiagram class="mt-2" input=".lfr запись" input-sub="Mac → оригинал или оригинал → Mac" :lanes="[
  { title: 'NTSD Native.app', sub: 'release-сборка, --virtual-clock, --playback-file, --summary-json', out: 'Summary в JSON прямо из состояния порта', color: 'var(--s1)', tag: 'macOS' },
  { title: 'NTSD 2.4.exe под CrossOver 26.3', sub: 'APFS-клон проверенной копии; клавиши через Cua Driver, 150 мс удержания', out: 'winedbg: x /x 0x450bbc… поля мест +0x348…+0x35c', color: 'var(--s2)', tag: 'Windows' },
]" verdict="равно" verdict-sub="Kill, Attack, HP Lost, MP Usage, Picking, время, победитель, итоги War" />

<div class="grid grid-cols-3 gap-4 mt-4 small ink2">
<div><b>START без GUI.</b> В меню 10 драйвер пишет в память оригинала <code>0x4546f0 = 350</code>, <code>0x453cdc = 230</code>, <code>0x457580 = 1</code> — и игра стартует сама.</div>
<div><b>Клавиши держат 150 мс</b> через <code>CGEvent.postToPid</code>: мгновенное нажатие игра теряет между кадрами. Окно ERROR музыки под CrossOver закрывается кликом — клавиша дошла бы до игры.</div>
<div><b>HP живого бойца</b> сравнивается как «жив / мёртв»: за экраном Summary HP продолжает восстанавливаться. Один оригинал за раз — под блокировкой.</div>
</div>

<div class="source">tools/crossover_drive/*.py · docs/CROSSPLAY_LOOP.md · 25d32a1 · 200214d · 23139fe</div>

---

<Kicker>доказательство на одном кадре</Kicker>

# Слева Mac пишет матч, справа оригинал его проигрывает

<img src="/img/screens/15-summary-mac-vs-original-side-by-side.jpg" class="rounded-lg border border-white/10 mt-2" style="width: 100%">

<div class="grid grid-cols-[1fr_auto] gap-4 mt-3 items-center">
<div class="small ink2">Kill, Attack, HP Lost, MP Usage, Picking и время 00:54 совпадают во всех трёх строках. Внизу слева — <span class="mono">Recording file '20260101_010000_VS.lfr' saved!</span>: запись сделана на Mac со скриптом и виртуальными часами.</div>
<span class="tag">docs/evidence/crossover-replay-crossplay-20261002</span>
</div>

---

<Kicker>3 октября · итог сверки</Kicker>

# 58 целых матчей — ни одного расхождения порта

<div class="mt-2">
<CrossplayTiles />
</div>

<div class="grid grid-cols-4 gap-3 mt-4">
<StatTile value="25 / 25" label="персонажей сыграли в равных матчах" size="sm" />
<StatTile value="17 / 17" label="фонов" size="sm" accent="var(--s1)" />
<StatTile :value="35272" label="тика — самый длинный War, ГСЧ сверялся каждые 1 000 тиков" size="sm" accent="var(--s3)" />
<StatTile value="1-1 … 5-1" label="первая фаза каждой группы Stage" size="sm" accent="var(--s4)" />
</div>

<CharacterBars class="mt-3" />

<div class="source">docs/evidence/crossplay-*.json · docs/research/CROSSPLAY_MATRIX.md · data/evidence/crossplay-matches.json</div>

---

<Kicker>как снималось Demo</Kicker>

# Тик в тик: таблица случайных чисел из Mac — в живой оригинал

<div class="grid grid-cols-[1fr_1.05fr] gap-6 mt-2">
<div class="small ink2">

Demo не записывается в файл, а его состав зависит от seed ГСЧ и фазы, которая крутится, пока открыто меню. Поэтому:

1. Mac играет Demo с `--virtual-clock 777 8` и пишет трассу.
2. `crt_table(777)` повторяет генератор таблицы `0x422ac0`, и 750 команд `set` переписывают таблицу `0x44ff90` **в живом оригинале**.
3. Фаза `0x450bd0` копируется из трассы Mac на первом тике.
4. Точка останова на конце тела тика `0x421cdc` с условием на номер тика — снимок окна и сверка индекса и счётчика ГСЧ.

</div>
<div>

```python
# tools/crossover_drive/demo_frames.py
run(f"set *(int*)0x450bd0 = {phase}")
try:
    for tick in range(first, last + 1, step):
        run(f"cond 1 *(int*)0x450bbc == {tick}")
        resume()
        index, counter = word(0x450BCC), word(0x450C34)
```

<div class="card-soft mt-3 small ink2">
В Demo с восемью компьютерными бойцами — около <b>55 вызовов ГСЧ за тик</b>: 49 517 за 900 тиков. Одна ошибка порядка — и сцены разойдутся за секунды.
</div>

</div>
</div>

<div class="source">tools/crossover_drive/demo_frames.py · demo_crossplay.py · docs/evidence/readme-demo-frames.json</div>

---

<Kicker>Demo · seed 777</Kicker>

# Две линии сливаются в одну — до тика 879

<DemoSync class="mt-1" />

<div class="grid grid-cols-2 gap-5 mt-3 small ink2">
<div>Каждая точка — индекс таблицы ГСЧ в двух программах на одном и том же тике. Пила сворачивается на 3 000; <b class="hl">244 кадра подряд</b> совпадают полностью — вместе со счётчиком.</div>
<div class="card-soft xsmall">Честно: в этом прогоне оригинал разошёлся с Mac между тиками 879 и 882, причина не найдена. Ролик в README остаётся внутри проверенного диапазона, а Demo в матрице помечено как открытое.</div>
</div>

<div class="source">data/evidence/demo-frames.json · docs/evidence/readme-demo-frames.json · 2e2992b</div>

---

<Kicker>/loop · 3 октября, 07:06–16:05</Kicker>

# Цикл, который ищет расхождения сам

<div class="xsmall muted mb-2 mt-2">CROSSPLAY_LOOP.md — задание для самотактируемого <code>/loop</code> Claude Code</div>

<Pipeline :steps="[
  { name: 'READ', ru: 'прочитать задание', desc: 'CROSSPLAY_LOOP.md и общие правила' },
  { name: 'PICK', ru: 'взять строку', desc: 'верхняя непроверенная в матрице' },
  { name: 'PLAY', ru: 'сыграть', desc: 'запись — в другой программе' },
  { name: 'DIFF', ru: 'локализовать', desc: 'тик → функция → инструкция', accent: true },
  { name: 'FIX', ru: 'исправить и записать', desc: 'тест, матрица, коммит' },
]" />

<div class="grid grid-cols-[1fr_1fr_1.6fr] gap-4 mt-4">
<StatTile :value="18" label="коммитов Claude за 9 часов цикла" size="sm" />
<StatTile value="0" label="расхождений порта в проверенных строках" size="sm" accent="var(--good)" />
<div class="card-soft">
<div class="mono xsmall hl">"No port difference was found in the checked rows. The Demo stays open."</div>
<div class="xsmall muted mt-1">2e2992b — цикл остановлен по решению пользователя</div>
</div>
</div>

<p class="small ink2 mt-3">«Цель — проверить всю игру, а не отдельные функции». Побочные находки — в оригинале и стенде: итоги War копятся между проигрываниями; окно ERROR музыки съедало отпускание клавиши J (<code>23139fe</code>); сиды 17 и 21 падали из-за второго запущенного экземпляра оригинала.</p>

<div class="source">docs/CROSSPLAY_LOOP.md · docs/research/CROSSPLAY_MATRIX.md · 0816dca … 2e2992b</div>

---

<Kicker>покрытие · 2–3 октября</Kicker>

# Сколько EXE на самом деле проверено

<div class="grid grid-cols-[1.55fr_1fr] gap-6 mt-1">
<div>
<ExeTreemap />
</div>
<div>

<Meter :value="0.924" label="инструкций в функциях с записями или корпусом" sub="157 из 174 функций игрового кода (63 694 инструкции)" />
<Meter :value="0.514" label="инструкций реально исполнено в записях" sub="47,0 % — в фикстурах, которые сравнивают тесты" />
<Meter :value="0.978" label="процитировано в карточках или порте" sub="160 функций" />

<div class="card-soft mt-3 small ink2">
<b>Аудит на следующий день</b> (другой агент): метрика засчитала 293 адреса из статического файла, не нашла WndProc <code>0x43b3d0</code>, переданный через <code>push</code>, и пропустила 2 529 входов в блоки. Вердикт: «Новый процент готовности не объявлен».
</div>

</div>
</div>

<div class="source">6fcf8b9 · f9ee219 · docs/research/EXE_COVERAGE_2026-10-02.md · EXE_COVERAGE_AUDIT_2026-10-03.md</div>
