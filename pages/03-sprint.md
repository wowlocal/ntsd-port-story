---
layout: chapter
num: 3
total: 20
kicker: Глава третья
dates: 7–12 сентября
image: /img/loading-screen-tobi.jpg
imagePixel: false
stats: 171 коммит за 102 часа · коммит каждые ~30 минут, днём и ночью
---

# Ночной спринт

Агент в автономном режиме идёт по оригиналу функция за функцией: загрузка, меню, повторы, физика, отрисовка, окно, сеть.

---

<Kicker>ночь с 7 на 8 сентября</Kicker>

# Пока все спят

<div class="grid grid-cols-[1.35fr_1fr] gap-6 mt-2">
<TermLog title="git log --since '2026-09-07 21:00' --until '2026-09-08 07:30'" night :lines="[
  { t: '21:13', h: 'ea19082', s: 'trace original match tick and identify pipeline gaps' },
  { t: '21:45', h: '76c50b7', s: 'preserve original constructor state and capture raw tick storage' },
  { t: '22:17', h: '40137c3', s: 'reproduce the original loading-time actor pool' },
  { t: '22:41', h: '40583ba', s: 'reproduce the original catalog parent and registry' },
  { t: '23:27', h: 'ed40eeb', s: 'load complete original object files natively' },
  { t: '23:50', h: 'cdd0f4c', s: 'reproduce original background loading and resource lifecycle' },
  { t: '00:19', h: 'e8f6298', s: 'reproduce the complete original stage data loader' },
  { t: '00:53', h: 'fab8104', s: 'match VC80 integer parsing and trace all original objects', hot: true },
  { t: '01:21', h: '0f5ceeb', s: 'preserve raw frames and load all original objects natively' },
  { t: '01:57', h: '29acb39', s: 'load the complete original catalog with shared native resources', hot: true },
  { t: '02:33', h: '28943b6', s: 'reproduce common match preparation from the full catalog' },
  { t: '03:04', h: 'c18a0f4', s: 'reproduce original recording initialization and RNG reset' },
  { t: '03:43', h: '586b193', s: 'reproduce original confirmed-match prelude' },
  { t: '04:22', h: 'be6f0f9', s: 'reproduce remaining menu state and random roster selection' },
  { t: '04:48', h: 'b9ff994', s: 'reproduce original CRT RNG initialization through match recording' },
  { t: '05:26', h: 'b54e5ca', s: 'reproduce original mouse input and main menu state transitions' },
  { t: '05:58', h: '6a379d4', s: 'reproduce original menu presentation and world transition' },
  { t: '06:43', h: '65ea14b', s: 'reproduce original WAV loading and startup sound resources' },
  { t: '07:00', h: '187b252', s: 'reproduce initial interface loading and bitmap error lifecycle' },
]" />
<div class="small ink2">

**19 коммитов за 10 часов ночи** — каждый с оракулом, фикстурами и карточкой исследования.

К утру нативный Swift загружал **весь каталог** оригинала и совпадал с EXE на всех объектах:

- 137 объектов, 17 фонов, 25 стейджей / 138 фаз;
- 400 слотов пула Actor и 829 обёрток битмапов;
- целые байты Object/Frame вместе с масками неизвестного.

<div class="card-soft mt-3">
<div class="xsmall muted">из карточки LOADED_CATALOG</div>
<div class="small">Сравнение удерживает все 101 слот BG и 60 слотов Stage после <b>каждого</b> вызова дочернего загрузчика.</div>
</div>

</div>
</div>

<div class="source">git log · README.md @ 2026-09-12 · docs/research/LOADED_CATALOG.md</div>

---
clicks: 3
---

<Kicker>как доказывали · дифференциальный оракул</Kicker>

# Оригинал исполняется рядом — в Unicorn

<FlowDiagram stepwise class="mt-1" input="одни и те же входы" input-sub="состояние, аргументы, байты DAT" :lanes="[
  { title: 'NTSD 2.4.exe в Unicorn', sub: 'x86-код оригинала по 0x400000; импорты → страница-заглушка; настоящий MSVCR80', out: 'байты после вызова + маска записей, вызовы ГСЧ, события ресурсов', color: 'var(--s2)', tag: 'эталон' },
  { title: 'Swift NTSDCore', sub: 'порт той же функции, свои аллокации и откат', out: 'байты после вызова, вызовы ГСЧ, события', color: 'var(--s1)', tag: 'порт' },
]" verdict="совпало побайтно" verdict-sub="только там, где байт определён маской" />

<div class="grid grid-cols-[1fr_1.05fr] gap-5 mt-2">
<div class="small ink2">

- Канарейки `0x11223344…` в регистрах, куча залита `0xA5`: возврат засчитан, только если EIP дошёл до STOP, а стек и канарейки целы.
- Падение оригинала — исход `sourceFault`, а не совпадение.
- 215 скриптов `oracle_*.py`, но VM создают лишь 17: остальные наследуют её цепочкой до 31 класса — игра грузится, проходит меню и играет такты в одной VM.

</div>
<div>

```python
# tools/oracle_crt.py: импорт EXE ведёт на «стоп-страницу»,
# там Python-заглушка снимает аргументы с ESP и делает ret
for item in pe.imports():
    address = STOP + 0x100 + len(self.boundaries) * 16
    self.put(int(item['iatVA'], 16), address)
    self.boundaries[address] = item['name']
self.uc.hook_add(UC_HOOK_CODE, self.boundary,
                 begin=STOP + 0x100, end=STOP + 0xFFFF)
```

<div class="xsmall muted">Подвох: memory-хуки Unicorn увидели 259 526 из 524 454 байт, записанных <code>REP&nbsp;MOVSD</code> — маски теперь берутся из самих инструкций копирования.</div>

</div>
</div>

<div class="source">tools/oracle_crt.py · tools/oracle_*.py · tools/verify_*.py · tools/accept_*.py</div>

---

<Kicker>9 сентября · точность до бита</Kicker>

# Игра считает с 53 битами, а не с 64

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-2">
<div>

Ещё до `WinMain` инициализатор CRT `0x44547e` вызывает `_controlfp_s(NULL, 0x10000, 0x30000)` — x87 переключается на 53-битную мантиссу (CW `037f` → `023f`). Первые «зелёные» сравнения шли при 64 битах.

<div class="grid grid-cols-2 gap-3 mt-3">
<StatTile :value="54201" label="последовательность сверена с настоящими fld / fadd / fmul / fdiv" size="sm" />
<StatTile value="168 / 9 344" label="исходов физики меняет 53-битный режим" size="sm" accent="var(--s1)" />
</div>

<div class="card-soft mt-3 small">
Одна и та же скорость: <span class="mono hl">3e3315113574ea8d</span> при 53 битах и <span class="mono">…ea8c</span> при 64. Разница — <b>один ULP</b>, но порт обязан повторить именно его.
</div>

</div>
<div>

```swift
// native/Sources/NTSDCore/OriginalExtended.swift
// x87 с явной точностью 24/53/64 бит:
// полное 128-битное произведение, затем округление
static func *(lhs: Self,rhs: Self) -> Self {
    precondition(lhs.precision == rhs.precision,
                 "Arithmetic operands need the same x87 context")
    let product = lhs.significand.multipliedFullWidth(by: rhs.significand)
    return rounded(.init(high: product.high,low: product.low),
                   negative: lhs.negative != rhs.negative,
                   exponent: lhs.exponent+rhs.exponent,
                   precision: lhs.precision)
}
```

<div class="xsmall muted">Перейти на <code>Double</code> нельзя: у x87 расширенный диапазон экспоненты. Порог анимации падения равен 1, а не 0, — он берётся со стека x87.</div>

</div>
</div>

<div class="source">a2a853c · 2cf272c · docs/research/FPU_PRECISION.md · docs/research/ARITHMETIC_PRECISION.md</div>

---

<Kicker>компилятор — часть игры</Kicker>

# VC80 тоже надо портировать

<div class="grid grid-cols-[1.05fr_1fr] gap-6 mt-2">
<div>

```swift
// OriginalFrameLoader.swift — целое из DAT, как его читает
// fscanf("%d") из MSVCR80: знак съедается до проверки цифр,
// значение считается по модулю 2³²
var negative = false
if bytes[position] == 43 || bytes[position] == 45 {
    negative = bytes[position] == 45; position += 1
}
let start = position
var value: UInt32 = 0
while position < bytes.count && (48...57).contains(bytes[position]) {
    value = value &* 10 &+ UInt32(bytes[position]-48)
    position += 1
}
guard position > start else { return nil }
return Int32(bitPattern: negative ? 0 &- value : value)
```

</div>
<div>

<IconCards class="vc80" :cols="1" compact :items="[
  { icon: 'i-pixelarticons-hash', title: 'Целые — по модулю 2³²', tone: 'naruto', text: '<code>-6846518779</code> из <code>kyubi.dat</code> превращается в <strong>1743415813</strong>, <code>4294967296</code> — в <strong>0</strong>. Из 867 уникальных целых в DAT 39 не помещаются в Int32.' },
  { icon: 'i-pixelarticons-package', title: 'Настоящий MSVCR80 8.0.50727.6195', tone: 's1', text: 'Достали из <code>vcredist_x86_2005sp1.exe</code> без запуска установщика (bsdtar → olefile → bsdtar) и исполняли в Unicorn: 919 912 сканов каталога.' },
  { icon: 'i-pixelarticons-printer', title: 'printf VC80 округляет дважды', tone: 's3', text: '<code>%2.4f</code> от 0.03125 даёт <code>0.0313</code> (macOS — <code>0.0312</code>), а <code>1#INF</code> становится <code>1.#IO</code>.' },
  { icon: 'i-pixelarticons-git-branch', title: 'float → int идёт двумя путями', tone: 's7', text: 'Для 4294967295 x87 даёт <code>0xffffffff</code>, SSE2 — <code>0x80000000</code>.' },
]" />

</div>
</div>

<div class="source">fab8104 · docs/research/CRT_SCANNER.md · docs/research/DIAGNOSTIC_NUMBERS.md · adf93da</div>

<style>
.vc80 :deep(.head b) { font-size: 0.8rem; }
.vc80 :deep(.txt) { font-size: 0.7rem; line-height: 1.42; }
</style>

---

<Kicker>поворот сюжета · 10 сентября, 01:28</Kicker>

# Игра, которая патчит сама себя

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-3">
<div>

Настоящая точка входа `NTSD 2.4.exe` ещё **до** таблиц инициализации CRT загружает `lib.dll` из дистрибутива. Код подключения DLL:

<div class="grid grid-cols-3 gap-3 mt-3">
<StatTile :value="12" label="переходов в игровой код" size="sm" />
<StatTile :value="1" label="двухбайтовый патч" size="sm" accent="var(--s1)" />
<StatTile :value="62" suffix="байта" label="13 вызовов RtlMoveMemory" size="sm" accent="var(--s3)" />
</div>

<p class="small ink2 mt-3">Порт обязан воспроизвести это поведение <b>без</b> загрузки DLL и без патча исполняемой памяти. DLL добавляет даже состояния 85/86, которых нет в DAT-таблицах.</p>

</div>
<div>

<div class="card" style="border-color: rgba(230,103,103,.45)">
<div class="pixel small" style="color: var(--s8)">последствие</div>
<div class="mono small mt-1">"This is a correction to the scope of the preceding gameplay comparisons."</div>
<p class="small ink2 mt-2 mb-0">Все прежние сравнения шли на «чистом» EXE ниже загрузки библиотеки. Они остаются неизменяемыми контролями — но <b>не доказывают</b> поведение настоящего приложения. Работа пошла заново поверх: <code>LIB_RUNTIME</code>, <code>LIB_ACTOR_CONTROL</code>, <code>LIB_WORLD_CONTACTS</code>…</p>
</div>

<div class="card-soft mt-3">
<div class="xsmall muted">а в мартовском плане было</div>
<div class="mono small">"NTSD 2.4 uses unmodified LF2 engine"</div>
</div>

</div>
</div>

<div class="source">9bb48f6 · docs/research/LIB_RUNTIME.md</div>

---
clicks: 1
---

<Kicker>9 сентября · что задела lib.dll</Kicker>

# Такт за сутки — и пять заплаток в нём

<p class="lead">9 сентября агент перенёс такт по частям и в 23:07 сверил с оригиналом 16 вызовов подряд. Через 2 ч 21 мин нашлась <code>lib.dll</code>; по клику — куда легли её заплатки.</p>

<ATickDay />

<div class="kpis">
<div><b>44</b><span>коммита за 9 сентября</span></div>
<div><b class="o">16</b><span>вызовов такта подряд = оригинал · <code>c65f9a8</code>, без нажатий</span></div>
<div><b class="g">zlib 1.1.4</b><span>внутри записи повтора: 815 из 815 вызовов</span></div>
<div><b class="r">5 из 13</b><span>заплаток lib.dll — в стадиях этого дня · <code>5a28b0a</code></span></div>
</div>

<div class="source">git log fc959db, 9–10 сентября · git show --numstat -- native/Sources · CONTINUOUS_GAMEPLAY_CAPTURE.md · REPLAY_COMPRESSION.md · ACTIVE_LIB_IMPACT.md · docs/evidence/active-lib-impact.json · LIB_RUNTIME.md</div>

<style>
.lead { margin: -0.45rem 0 0.2rem !important; font-size: 0.78rem; line-height: 1.4; color: var(--ink-2); max-width: 58rem; }
.lead code { font-size: 0.72rem !important; }
.kpis { display: grid; grid-template-columns: 0.8fr 1.25fr 1.15fr 1.2fr; gap: 8px; margin-top: 0.25rem; }
.kpis > div { display: flex; align-items: center; gap: 0.55rem; background: var(--surface); border: 1px solid var(--hair); border-radius: 10px; padding: 0.3rem 0.6rem; }
.kpis b { font-family: var(--font-display); font-size: 1.05rem; line-height: 1; color: var(--ink); white-space: nowrap; }
.kpis b.o { color: var(--naruto); }
.kpis b.g { color: var(--s3); font-size: 0.9rem; }
.kpis b.r { color: var(--s8); }
.kpis span { font-size: 0.58rem; line-height: 1.3; color: var(--ink-2); }
.kpis code { font-size: 0.52rem !important; }
</style>

<!--
Наведите на точку — внизу появится коммит: время, хэш, заголовок и сколько строк он добавил в native/Sources. По клику появляются красные кольца — пять заплаток lib.dll.

День по часам git (+0300). Ночью — вход в матч и управление (eb26182 … e2f20ce), в 03:44 — вся физика Actor и мира (71b74a2), к 06:24 — контакты, удары, предметы, cpoint. Утром камера, фон и вся отрисовка World и Actor (30be76e, e3c220f), потом точность x87 — это предыдущий слайд про 53 бита. Днём — планировщик кадров Actor (fcf9cd1) и весь post-draw, HUD (22175e3) и уведомления. Вечером — запись повтора: сжатие — это настоящий zlib 1.1.4 2002 года из официального архива: 8 из 10 вендорённых файлов побайтно совпадают с ним по SHA-256, правлены только zutil.h и zconf.h (c674066; поэтому точка такая большая — 5 049 строк, в основном исходники zlib), затем буфер потока и весь писатель файла записи (248f7e5). К ночи — запись результата и вывод, тело такта собрано атомарно (f98c5ab), и в 23:07 — c65f9a8: «Both initialized variants now match sixteen successive native loaded calls».

Что это значило и чего ещё нет — по самой карточке CONTINUOUS_GAMEPLAY_CAPTURE: шестнадцать вызовов такта на собственном сохранённом состоянии, без единого нажатия (клавиатура нейтральна), фазы чередуются 0/1, счётчик повтора идёт 2..17. Дословно: «The real outer 43e9a0 loop and its clock pacing remain a necessary separate join. Neutral keyboard memory does not prove keyboard-device acquisition, input latency, wall-clock animation cadence, audio timing or a complete match.»

Через 2 ч 21 мин, в 01:28, — 9bb48f6: настоящая точка входа грузит lib.dll (предыдущий слайд). В 01:39 агент сделал аудит только для чтения (5a28b0a, ACTIVE_LIB_IMPACT): из тринадцати мест, куда пишет установщик DLL, пять пересекаются с инструкциями двух принятых контролей по 48 вызовов — управление 41408b, контакты 4176ac (в 11 вызовах из 48), жизненный цикл post-draw 41f5fc, команды post-draw 4214d7 и текст 401290 (импульсы post-draw и итоговый вывод). Кольца стоят на коммитах, которые перенесли эти стадии; это пересечение байтов кода, а не число исполнений и не исход: «It does not establish which DLL branches will run or how the resulting game state will differ».

Ничего не стёрли: прежние сравнения остались «immutable, useful controls», но перестали доказывать поведение приложения с библиотекой. Красные точки справа — та же ночь: в 02:13 управление Actor с установленным переходом 41408b → 10001125 (0a7c7a6, 7 168 вызовов), в 02:37 фильтры контактов, в 04:08 эффекты ударов — уже поверх библиотеки.
-->

---

<Kicker>10–12 сентября</Kicker>

# Всё приложение — от WinMain до War

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-2">
<div>

<Timeline dense :items="[
  { time: '10.09', title: 'Таймеры, пауза, пошаговый режим', hash: '30ce08e' },
  { time: '10.09', title: 'Окно, дисплей, пересоздание поверхностей', hash: 'b2d116e' },
  { time: '10.09', title: 'DirectShow: события музыкального графа', hash: '97b91a6' },
  { time: '10.09', title: 'Сеть: рукопожатие сервера и клиента', hash: '77cbfb6' },
  { time: '10.09', title: 'Непрерывный WinMain и цикл сообщений', hash: '6b69cc3' },
  { time: '11.09', title: 'Tournament: сетка, места, победители', hash: '60c99c3' },
  { time: '11.09', title: 'Team Tournament: пары и перемешивание', hash: 'ea7bb8e' },
  { time: '12.09', title: 'War: 806 оригинальных вызовов', hash: 'b6fe14e', hot: true },
]" />

</div>
<div>

<div class="card">
<div class="pixel hl small">b6fe14e · 12 сентября, 00:38</div>
<p class="small ink2">805 внешних возвратов, 801 возврат War, 574/192/40 случаев транспорта, все 44 ячейки войск, 14 комбинаций действий нескольких людей и 18 поздних откатов.</p>
<div class="mono xsmall">"Preserve the original seven-cell coverage gap and all source/tool failures; no game or expected byte changed during acceptance."</div>
</div>

<div class="card-soft mt-3 small ink2">
Пик режима «точность любой ценой»: семь тестов в пакете — 473 секунды, плюс проверка 21 новой и 295 старых фикстур и 745 файлов пакета и архива.
</div>

</div>
</div>

<div class="source">git log · b6fe14e</div>
