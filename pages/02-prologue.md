---
layout: chapter
num: 1
total: 12
kicker: Пролог
dates: 31 марта 2026
image: /img/menu-back-naruto-vs-sasuke.jpg
imagePixel: false
stats: 5 коммитов · потом 160 дней тишины
---

# Сначала был план

…и он был неправильным. Причём дважды за одну минуту.

---

<Kicker>31 марта, ночь</Kicker>

# Три плана за полгода

<div class="grid grid-cols-[1.1fr_1fr] gap-7 mt-2">
<div>

<Timeline :items="[
  { time: '00:25', title: 'NTSD 2.4 Full Recreation in Godot 4 for macOS', hash: '8940864', note: 'план №1: написать движок заново на Godot' },
  { time: '00:26', title: 'Fork F.LF + Tauri', hash: '20b1b09', note: 'через 13 секунд — план №2: взять готовую JS-реимплементацию LF2 и завернуть в Tauri', hot: true },
  { time: '12:00', title: 'CrossOver: ошибки и решения', hash: 'aa2e149', note: 'оригинал под Wine падает на chars/flash.dat; файлы игры уходят в Git LFS' },
  { time: '7 сен', title: 'Первый AGENTS.md: JS-реализация отвергнута', hash: 'ceead97', note: 'план №3: нативный Swift, эталон — только оригинальный EXE' },
]" />

</div>
<div>

<div class="card-soft">
<div class="xsmall muted">PLAN.md, 20b1b09</div>
<div class="mono small mt-1">"Key fact: NTSD 2.4 uses <b class="hl">unmodified LF2 engine</b> — no custom itr types or engine extensions."</div>
</div>

<div class="card-soft mt-3">
<div class="xsmall muted">там же, таблица рисков</div>
<div class="mono small mt-1">"Accuracy risk — Low (F.LF already matches LF2)"</div>
</div>

<div class="card mt-3" style="border-color: rgba(230,103,103,.5)">
<div class="pixel small" style="color: var(--s8)">спойлер · 10 сентября</div>
<p class="small ink2 mb-0">Настоящая точка входа EXE ещё до старта CRT грузит <code>lib.dll</code>, и та <b>переписывает игру</b>: 12 переходов в игровой код и один двухбайтовый патч — 62 байта в 13 местах. «Немодифицированный LF2» оказался мифом.</p>
<span class="tag">9bb48f6</span>
</div>

</div>
</div>

<div class="source">8940864 · 20b1b09 · aa2e149 · ceead97 · 9bb48f6</div>

---
layout: chapter
num: 2
total: 12
kicker: Глава вторая
dates: 7 сентября, 18:20–21:13
image: /img/district-composite-960x550.png
stats: 4 коммита практики · 1 разворот
---

# Первый вечер

Два часа — и Наруто ходит, Саске бросает Чидори. А потом вопрос: это правильный путь?

---

<Kicker>7 сентября · вечер</Kicker>

# Похоже — ещё не значит «так же»

<div class="grid grid-cols-[1fr_15rem] gap-6 mt-2">
<div>

<Timeline :items="[
  { time: '18:20', title: 'Native macOS Naruto movement milestone', hash: 'ceead97', note: 'AppKit + SpriteKit, ассеты District; ходьба совпала с оригиналом на 8 506 тиках x86-оракула' },
  { time: '19:38', title: 'Naruto and Sasuke melee practice', hash: '40b6ece', note: 'атаки, защита, реакции на удар, падения, голоса, ГСЧ повторов' },
  { time: '20:21', title: 'Sasuke projectiles and chakra technique', hash: 'a9f2cfe', note: 'снаряды и Чидори — но через проверки вида name == &quot;Sasuke&quot;' },
  { time: '20:45', title: 'Map original engine research and porting sequence', hash: 'c9a5263', note: 'RESEARCH_MAP.md, ADDRESS_BOOK.md, шаблон задачи — практика заморожена', hot: true },
  { time: '21:13', title: 'Trace original match tick and identify pipeline gaps', hash: 'ea19082', note: 'первая карточка R01.1: границы и порядок полного игрового такта' },
]" />

</div>
<div class="flex flex-col items-center gap-3 pt-1">
<div class="flex items-end justify-center gap-1" style="width: 100%">
<Sprite src="/img/sprites/naruto-rasengan-4x.png" :scale="0.36" float />
<Sprite src="/img/sprites/sasuke-chidori-4x.png" :scale="0.36" flip float />
</div>
<div class="card-soft text-center">
<div class="mono small hl">"Movement matches 8,506 reference ticks; combat remains the next milestone."</div>
<div class="xsmall muted mt-1">ceead97, первый коммит сентября</div>
</div>
</div>
</div>

---

<Kicker>ДНК проекта · RESEARCH_MAP.md, 7 сентября</Kicker>

# Три вида условий в коде

<p class="ink2">«Поддержка нового персонажа, использующего уже перенесённые правила, не должна требовать изменения Swift-кода. <b>Имена персонажей и названия техник не являются единицами переноса</b>».</p>

| основание | пример | как с ним работать |
| --- | --- | --- |
| **Общее правило EXE** | `state`, `itr.kind`, `effect`, переход по `hit_Fa`, стоимость `mp` | переносить общий обработчик с исходным порядком операций |
| **Исключение EXE** | проверка ID 224 при отрисовке тени | записать адрес, контекст и условия; сохранить правило и добавить проверку |
| **Ограничение прототипа** | `name == "Sasuke" && target == 261`, список из двух снарядов | граница реализации; заменять проверкой поддержанных механизмов |

<div class="grid grid-cols-2 gap-4 mt-4 small ink2">
<div class="card-soft">«Ограничения прототипа нельзя просто удалить: ранее недоступные кадры могут требовать ещё не перенесённых правил».</div>
<div class="card-soft">«Неподдержанный механизм должен иметь явную диагностику; <b>откат всего такта</b> сохраняется. Исходные данные не исправляем ради обхода ошибки».</div>
</div>

<div class="source">docs/RESEARCH_MAP.md @ c9a5263</div>

---

<Kicker>что видит движок · chars/naruto.dat</Kicker>

# Наруто глазами движка

<div class="mt-3">
<FrameInspector :ids="[0, 63, 72, 258]" :scale="2.4" />
</div>

<div class="grid grid-cols-3 gap-4 mt-3 small ink2">
<div>Картинка — ячейка 79×79 из спрайт-листа <code>naruto_0.bmp</code> / <code>naruto_2.bmp</code>. Чёрный цвет — прозрачный, как в игре.</div>
<div>Рамки — не разметка художника: движок читает их из текста DAT для этого же кадра. Урон, отбрасывание и падение — поля самого <code>itr</code>.</div>
<div>У каждого из этих кадров есть <b>второй bdy на y: 80 000</b> — в 80 000 пикселях под персонажем. Такой есть в 127 из 318 определений кадров Наруто.</div>
</div>

<div class="source">scripts/extract_frames.py · data/engine_frames.json · decoder: tools/import_ntsd.py</div>

---

<Kicker>кадр — это текст</Kicker>

# Так выглядит кадр после расшифровки

<div class="grid grid-cols-[1fr_1fr_0.95fr] gap-4 mt-2">
<div>
<div class="xsmall muted mb-1">frame 72 · super_punch — удар с полями урона и падения</div>
<DatText :id="72" :odd="['80000']" />
</div>
<div>
<div class="xsmall muted mb-1">frame 123 · catching — определён в файле дважды</div>
<DatText :id="123" :odd="['-842150451']" />
</div>
<div class="small ink2">

- **Шифр.** Из каждого байта вычитается байт ключа `SiuHungIsAGoodBearBecauseHeIsVeryGood`; 123 байта мусорного заголовка тоже прокручивают ключ.
- **−842150451 = 0xCDCDCDCD** — так отладочная куча MSVC заполняет только что выделенную память. В <code>naruto.dat</code> это число встречается 68 раз, во всех DAT персонажей — 1 573 раза в 62 файлах: похоже, редактор, которым сохраняли файлы, записал мусор из памяти.
- **Кадр 123 определён дважды:** 318 определений дают 317 кадров, а второе определение дописывает поля первого.

</div>
</div>

<div class="source">chars/naruto.dat, расшифровано · scripts/extract_frames.py · docs/FRAME_LOADER.md</div>
