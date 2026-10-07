---
layout: chapter
num: 1
total: 15
kicker: Пролог
dates: 31 марта 2026
image: /img/covers/ch01-academy-konoha.jpg
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
total: 15
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

<div class="grid grid-cols-[1fr_24.5rem] gap-5 mt-1">
<div>

<Timeline dense :items="[
  { time: '18:20', title: 'Native macOS Naruto movement milestone', hash: 'ceead97', note: 'AppKit + SpriteKit, ассеты District; ходьба совпала с оригиналом на 8 506 тиках x86-оракула' },
  { time: '19:38', title: 'Naruto and Sasuke melee practice', hash: '40b6ece', note: 'атаки, защита, реакции на удар, падения, голоса, ГСЧ повторов' },
  { time: '20:21', title: 'Sasuke projectiles and chakra technique', hash: 'a9f2cfe', note: 'снаряды и Чидори — но через проверки вида name == &quot;Sasuke&quot;' },
  { time: '20:45', title: 'Map original engine research and porting sequence', hash: 'c9a5263', note: 'RESEARCH_MAP.md, ADDRESS_BOOK.md, шаблон задачи — практика заморожена', hot: true },
  { time: '21:13', title: 'Trace original match tick and identify pipeline gaps', hash: 'ea19082', note: 'первая карточка R01.1: границы и порядок полного игрового такта' },
]" />

<div class="card-soft text-center mt-3">
<div class="mono small hl">"Movement matches 8,506 reference ticks; combat remains the next milestone."</div>
<div class="xsmall muted mt-1">ceead97, первый коммит сентября</div>
</div>

</div>
<div>

<BeforeAfter before="/img/frames/evening/practice-0907.png" after="/img/frames/evening/app-0928.png" before-label="практика · 7 сентября" after-label="приложение · 28 сентября" height="18.1rem" :start="52" fit="cover" position="top" pixelated />

<div class="xsmall ink2 mt-2" style="line-height: 1.45">Тот же District, те же спрайты. Но HUD с надписью «Чакра 500/500» практика придумала сама; справа — восемь панелей HUD оригинала, уже в приложении.</div>

</div>
</div>

<div class="source">ceead97 · 40b6ece · a9f2cfe · c9a5263 · ea19082 · снимки: build/snake.png, 7 сен 19:11 · application-runtime-match-capture.png @ 4943589</div>

<!--
Слева — снимок окна практики первого вечера: build/snake.png в репозитории порта, файл создан 7 сентября в 19:08, изменён в 19:11. Саске попадает в Наруто змеями, у Наруто 445/500. Справа — docs/evidence/application-runtime-match-capture.png из коммита 4943589 (28 сентября): начало матча Наруто против Саске на District уже в нативном приложении.

Оба снимка обрезаны до общей области: камеры отличаются на 10 пикселей игры, после сдвига фон совпадает. Сверху добавлена тёмная полоса под подписи.
-->

---

<Kicker>ДНК проекта · RESEARCH_MAP.md, 7 сентября</Kicker>

# Три вида условий в коде

<p class="ink2">«Поддержка нового персонажа, использующего уже перенесённые правила, не должна требовать изменения Swift-кода. <b>Имена персонажей и названия техник не являются единицами переноса</b>».</p>

<IconCards class="dna mt-4" :cols="3" :items="[
  { icon: 'i-pixelarticons-settings-cog', title: 'Общее правило EXE', tone: 's1', text: '<span class=&quot;lbl&quot;>пример</span><code>state</code>, <code>itr.kind</code>, <code>effect</code>, переход по <code>hit_Fa</code>, стоимость <code>mp</code><span class=&quot;lbl&quot;>как с ним работать</span>переносить общий обработчик с исходным порядком операций' },
  { icon: 'i-pixelarticons-target', title: 'Исключение EXE', tone: 's4', text: '<span class=&quot;lbl&quot;>пример</span>проверка ID 224 при отрисовке тени<span class=&quot;lbl&quot;>как с ним работать</span>записать адрес, контекст и условия; сохранить правило и добавить проверку' },
  { icon: 'i-pixelarticons-warning-box', title: 'Ограничение прототипа', tone: 's8', text: '<span class=&quot;lbl&quot;>пример</span><code>name == &quot;Sasuke&quot; &amp;&amp; target == 261</code>, список из двух снарядов<span class=&quot;lbl&quot;>как с ним работать</span>граница реализации; заменять проверкой поддержанных механизмов' },
]" />

<div class="grid grid-cols-2 gap-4 mt-4 small ink2">
<div class="card-soft">«Ограничения прототипа нельзя просто удалить: ранее недоступные кадры могут требовать ещё не перенесённых правил».</div>
<div class="card-soft">«Неподдержанный механизм должен иметь явную диагностику; <b>откат всего такта</b> сохраняется. Исходные данные не исправляем ради обхода ошибки».</div>
</div>

<div class="source">docs/RESEARCH_MAP.md @ c9a5263</div>

<style>
.dna :deep(.ic) { padding: 0.8rem 0.95rem 0.85rem; }
.dna :deep(.head b) { font-size: 0.9rem; }
.dna :deep(.ico) { width: 1.6rem; height: 1.6rem; }
.dna :deep(.txt) { font-size: 0.74rem; line-height: 1.45; margin-top: 0.15rem; }
.dna :deep(.txt .lbl) { display: block; margin: 0.5rem 0 0.1rem; font-family: var(--font-pixel); font-size: 0.6rem; letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted); }
</style>

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

<Kicker>отладчик кадров · chars/naruto.dat</Kicker>

# Приём — это цепочка next

<FramePlayer>
<div class="fp-rule card-soft">
<p>Каждый тик планировщик кадров <code>0x40d960</code> прибавляет 1 к счётчику кадра. Когда счётчик <b>больше</b> <code>wait</code>, он обнуляется, и движок переходит на <code>next</code>. Кадр с <code>wait: N</code> держится <b class="hl">N + 1 тик</b>, тик — 33 мс. По цепочке весь приём — 24 тика, 0,8 с.</p>
<p>Имя кадра — только подпись: <code>clone_spin</code> переходит в <code>super_punch</code> обычным <code>next: 70</code>.</p>
</div>
</FramePlayer>

<div class="source">chars/naruto.dat, кадры 285–287 и 70–74 · data/engine_sequence.json · docs/research/ACTOR_SCHEDULER.md:43–44, 51–54 · docs/ORIGINAL_ENGINE.md:75–79</div>

<style>
.fp-rule { padding: 0.55rem 0.8rem; }
.fp-rule p { font-size: 0.72rem; line-height: 1.45; color: var(--ink-2); margin: 0; }
.fp-rule p + p { margin-top: 0.35rem; }
</style>

<!--
Цепочка — настоящая: в кадрах стойки и ходьбы (0–3, 5–8) стоит hit_Da: 285. Дальше только поля next: 285 → 286 → 287 → 70 → 71 → 72 → 73 → 74 → 999. В movelist дистрибутива этот приём Наруто называется Clone Toss: Defend, Down, Attack. На кадре 286 opoint порождает объект 33 — chars/naruto_clone.dat по data.txt. На кадре 285 — mp: 100.

Правило счётчика — из docs/research/ACTOR_SCHEDULER.md, правила 4 и 7. При смене кадра счётчик обнуляется и сразу растёт на 1. Когда он превышает wait, он снова обнуляется и записывается next. Значит, кадр живёт wait + 1 вызов планировщика — если ранние выходы планировщика (правило 1) или другие правила не задержат и не сменят кадр. next: 999 у объекта типа 0 на земле становится кадром 0 (правило 7). Тик — 33 мс: ORIGINAL_ENGINE.md, таймер 0x43d157; это 30,3 тика в секунду (APPLICATION_TICK_SPEED.md).

Плеер замедлен в 6 раз: 5 тиков в секунду. Сдвиг по dvx не показан, персонаж стоит на месте. Повтор в конце — наш: в игре после 999 Наруто просто встаёт в стойку. В экспорте — стоп-кадр 72, второй тик из трёх.
-->

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
