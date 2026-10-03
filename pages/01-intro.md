<Kicker>холодный старт</Kicker>

# Одна и та же Demo — тик в тик

<WindowFrame class="mt-1 mx-auto" style="width: 90%" video="/media/demo-side-by-side.mp4" poster="/media/demo-poster.jpg" title="слева — нативное Swift-приложение · справа — оригинальный NTSD 2.4.exe под CrossOver" />

<div class="grid grid-cols-3 gap-4 mt-2 small ink2">
<div>Обе программы стартуют с одной таблицы случайных чисел и играют одну Demo-сцену с восемью компьютерными бойцами.</div>
<div>На каждом кадре — каждый третий тик с 603 по 837 — <b class="hl">индекс и счётчик ГСЧ совпадают</b>.</div>
<div>Справа — настоящий оригинал: его останавливали на нужном тике условной точкой останова в <code>winedbg</code>.</div>
</div>

<div class="source">docs/media/demo-side-by-side.mp4 · docs/evidence/readme-demo-frames.json · tools/crossover_drive/demo_frames.py</div>

---
layout: statement
kicker: с чего начинали
big: "0"
---

строк исходного кода — у нас был только <b>один EXE</b>

<!--
Ноль строк исходного кода. Был только дистрибутив игры: NTSD 2.4.exe, DAT-файлы с кадрами, BMP-спрайты, WAV и WMA — о нём следующий слайд.
-->

---

<Kicker>что портируем</Kicker>

# Naruto: The Setting Dawn 2.4

<div class="grid grid-cols-[17rem_1fr] gap-7 mt-2 items-start">
<div>
<img src="/img/roster-25-faces-2x.png" class="rounded-lg border border-white/10" style="width: 17rem" alt="25 портретов персонажей">
<div class="xsmall muted mt-1">25 играбельных персонажей, портреты из оригинального дистрибутива</div>
</div>
<div>

Фанатская игра на движке **Little Fighter 2** (Marti Wong, Starsky Wong, 1999–2008). Один Windows-файл `NTSD 2.4.exe`, DAT-файлы с кадрами, BMP-спрайты, WAV и WMA.

<div class="grid grid-cols-3 gap-3 mt-3">
<StatTile :value="137" label="объектов в каталоге" sub="персонажи, снаряды, предметы" size="sm" />
<StatTile :value="17" label="фонов-арен" size="sm" accent="var(--s1)" />
<StatTile value="25 / 138" label="стейджей / фаз" size="sm" accent="var(--s3)" />
</div>

- Режимы: VS, Stage, Tournament, Team Tournament, War, Demo, просмотр записей, игра по сети.
- **30 тиков в секунду**, 2.5D-физика, хитбоксы, AI компьютерных бойцов.
- На Mac — только через CrossOver, и в части конфигураций игра падала на загрузке `chars/flash.dat`: разыменование нуля по адресу `0x0043f04b`.

<div class="xsmall muted">SHA-256 эталонного EXE: <span class="mono">3f7ac67c5890ef97…ff71c</span></div>

</div>
</div>

<div class="source">AGENTS.md · NTSD24_CROSSOVER_ERRORS_AND_SOLUTIONS.md · docs/research/LOADED_CATALOG.md</div>

---

<Kicker>правила игры</Kicker>

# Задача, сформулированная запретами

<div class="rules grid grid-cols-2 gap-5 mt-3">
<div class="card">
<div class="rh pixel hl"><span class="i-pixelarticons-check" />нужно</div>
<div class="rr"><span class="ri i-pixelarticons-app-mac" /><div><b>Нативная macOS-игра</b><span>поведение, вид, ввод, звук и ощущение оригинала</span></div></div>
<div class="rr"><span class="ri i-pixelarticons-gamepad" /><div><b>Весь объём игры</b><span>режимы, AI, меню, сохранения, повторы, сеть</span></div></div>
<div class="rr"><span class="ri i-pixelarticons-bug" /><div><b>Даже ошибки оригинала</b><span>если они достижимы в игре</span></div></div>
<div class="rr"><span class="ri i-pixelarticons-binary" /><div><b>Правила — из EXE</b><span>общие DAT-обработчики + исключения по ID из самого EXE</span></div></div>
</div>
<div class="card no">
<div class="rh pixel"><span class="i-pixelarticons-close" />нельзя</div>
<div class="rr"><span class="ri i-pixelarticons-app-windows" /><div><b>В рантайме</b><span>браузерный движок, Windows-EXE, CrossOver, Wine, эмуляция</span></div></div>
<div class="rr"><span class="ri i-pixelarticons-dice" /><div><b>Угадывать</b><span>физику, тайминги комбо, урон, AI и случайность</span></div></div>
<div class="rr"><span class="ri i-pixelarticons-copy-x" /><div><b>Брать правила</b><span>из F.LF или другой реимплементации LF2</span></div></div>
<div class="rr"><span class="ri i-pixelarticons-image-broken" /><div><b>Трогать оригинальные ассеты</b><span>чтобы подогнать их под недописанный движок</span></div></div>
</div>
</div>

<div class="card-soft mt-5 flex items-center gap-4">
<div class="pixel hl" style="font-size: 1.6rem">!</div>
<div class="small"><span class="mono">"The user rejected the previous JavaScript implementation. Do not copy its behavior."</span><br><span class="muted xsmall">первый AGENTS.md, 7 сентября 2026, коммит ceead97</span></div>
</div>

<style>
.rules .card { padding: 0.85rem 1rem 0.9rem; }
.rules .rh { display: flex; align-items: center; gap: 0.45rem; font-size: 0.8rem; margin-bottom: 0.55rem; }
.rules .rh span { width: 1.05rem; height: 1.05rem; }
.rules .no .rh { color: var(--s8); }
.rules .rr { display: grid; grid-template-columns: 1.6rem 1fr; gap: 0.65rem; align-items: start; margin-top: 0.85rem; }
.rules .ri { width: 1.5rem; height: 1.5rem; color: var(--naruto); margin-top: 0.1rem; }
.rules .no .ri { color: var(--s8); }
.rules .rr b { display: block; font-size: 0.92rem; line-height: 1.25; color: var(--ink); font-weight: 650; }
.rules .rr div > span { display: block; font-size: 0.76rem; line-height: 1.35; color: var(--ink-2); margin-top: 0.12rem; }
</style>

<div class="source">AGENTS.md · ceead97</div>

<!--
Полные формулировки из AGENTS.md.
Нужно: нативная macOS-игра — поведение, вид, ввод, звук и ощущение оригинала. Весь объём: контент, режимы, AI, меню, настройки, сохранения, повторы, сеть. Даже оригинальные ошибки, достижимые в игре. Правила — из EXE: общие DAT-обработчики плюс исключения по ID, которые есть в самом EXE.
Нельзя: в рантайме — браузерный движок, Windows-EXE, CrossOver, Wine, эмуляция. Угадывать физику, тайминги комбо, урон, AI и случайность. Брать правила из F.LF или другой реимплементации LF2. Трогать оригинальные ассеты, чтобы подогнать их под недописанный движок.
-->

---

<Kicker>оглавление · 13 глав</Kicker>

# Маршрут на 27 дней

<MetroMap class="mt-2" />

<div class="source">даты и цифры — с обложек глав · цвет линии — автор коммитов: git log, трейлер Co-Authored-By</div>

<!--
Тринадцать глав — станции одной линии. Синий участок — Codex (GPT-6 Astra), 7–27 сентября; оранжевый — Claude Opus 5.5 с 28 сентября, пересадка — глава «Поворот». Главы 9–11 — обо всём проекте сразу, поэтому там идут обе линии. Пролог — 31 марта, за 160 дней тишины до старта. Пунктир в конце — что дальше: Linux, Windows, iPad.
-->

---

<Kicker>карта пути · 7 сентября — 3 октября</Kicker>

# 463 коммита за 27 дней

<CommitDays class="mt-1" :labels="{ pre: 'Codex · GPT-6 Astra', claude: 'Claude Opus 5.5', parallel: 'Codex параллельно: сеть' }" :marks="[
  { date: '2026-09-07', label: 'старт', row: 1 },
  { date: '2026-09-10', label: 'lib.dll патчит EXE', row: 0 },
  { date: '2026-09-12', label: 'свод правил', row: 1 },
  { date: '2026-09-26', label: 'рекорд: 52', row: 0 },
  { date: '2026-09-28', label: 'первый матч', row: 1 },
  { date: '2026-10-03', label: 'сверка', row: 0 },
]" />

<div class="grid grid-cols-3 gap-4 small ink2">
<div><b class="hl">327</b> коммитов Codex (7–27 сентября): модель в реестре инцидентов — <span class="mono">gpt-6-astra</span>, режим <span class="mono">xhigh</span>.</div>
<div><b class="hl">120</b> коммитов с трейлером <span class="mono">Co-Authored-By: Claude Opus 5.5</span> (28 сентября — 3 октября).</div>
<div><b class="hl">16</b> коммитов без трейлера 1–3 октября: сеть и аудит покрытия, параллельный агент.</div>
</div>

<div class="source">git log · data/daily.json · docs/evidence/codex-safety-incidents-2026-09-12.json · docs/GOAL_100.md</div>

<!--
Цвет — кто сделал коммит. Серые плашки — дни без коммитов: семь дней с 15 по 21 сентября и три дня с 23 по 25.
-->

---

<Kicker>те же 27 дней · Gource</Kicker>

# Репозиторий растёт как дерево

<div class="grid grid-cols-[1fr_14rem] gap-5 mt-1 items-start">
<WindowFrame video="/media/gource.mp4" poster="/media/gource-poster.jpg" :pixel="false" title="gource · 7 сентября → 3 октября 2026 · 7 256 изменений файлов" />
<div class="small ink2">

<div class="flex flex-col gap-1 mb-3">
<span><i class="swatch" style="background: var(--s1)" />Codex</span>
<span><i class="swatch" style="background: var(--s2)" />Claude</span>
<span><i class="swatch" style="background: var(--s3)" />Codex параллельно: сеть</span>
</div>

Каждая точка — файл, ветки — папки. Файл окрашивается в цвет агента, который трогал его последним; паузы без коммитов пропущены.

<div class="card-soft mt-3 xsmall">28 сентября — вспышка у <code>native/</code>: проверенный кандидат на 2 291 файл переезжает в корень, а с ним 1 199 ресурсов оригинального каталога.</div>

</div>
</div>

<div class="source">scripts/make_gource.sh · git log --name-status · gource 0.56</div>

---

<Kicker>ритм</Kicker>

# Агенты не спят

<div class="grid grid-cols-[1fr_13rem] gap-5 mt-1 items-start">
<RhythmHeatmap />
<div class="flex flex-col gap-3">
<StatTile :value="92" label="коммита между 00:00 и 06:00" sub="20 % у Codex, 22 % у Claude" size="sm" />
<StatTile :value="28" suffix="мин" label="медианный интервал между коммитами внутри сессии" sub="Codex 27,7 · Claude 30,0" size="sm" accent="var(--s1)" />
<StatTile :value="52" label="коммита за 26 сентября — рекорд" size="sm" accent="var(--s3)" />
</div>
</div>

<div class="source">локальное время коммита · data/rhythm.json · data/summary.json</div>

<!--
Каждый столбец — день, каждая клетка — час. В каждом часе суток за проект набралось минимум 8 коммитов. Ночь 8–9 сентября — сплошная полоса: агент в автономном режиме коммитил каждые полчаса.
-->
