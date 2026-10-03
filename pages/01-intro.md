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

<div class="grid grid-cols-2 gap-5 mt-3">
<div class="card">
<div class="pixel hl small">нужно</div>

- Нативная macOS-игра: поведение, вид, ввод, звук и **ощущение** оригинала.
- Весь объём: контент, режимы, AI, меню, настройки, сохранения, повторы, сеть.
- Даже **оригинальные ошибки**, достижимые в игре.
- Правила — из EXE: общие DAT-обработчики плюс исключения по ID, которые есть в самом EXE.

</div>
<div class="card">
<div class="pixel small" style="color: var(--s8)">нельзя</div>

- В рантайме: браузерный движок, Windows-EXE, CrossOver, Wine, эмуляция.
- Угадывать физику, тайминги комбо, урон, AI и случайность.
- Брать правила из F.LF или другой реимплементации LF2.
- Трогать оригинальные ассеты, чтобы подогнать их под недописанный движок.

</div>
</div>

<div class="card-soft mt-4 flex items-center gap-4">
<div class="pixel hl" style="font-size: 1.6rem">!</div>
<div class="small"><span class="mono">"The user rejected the previous JavaScript implementation. Do not copy its behavior."</span><br><span class="muted xsmall">первый AGENTS.md, 7 сентября 2026, коммит ceead97</span></div>
</div>

<div class="source">AGENTS.md · ceead97</div>

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
Цвет — кто сделал коммит. Серые плашки — дни без коммитов: восемь дней с 15 по 21 сентября и три дня с 23 по 25.
-->

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
