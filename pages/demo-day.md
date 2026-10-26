---
clicks: 0
---

<DemoPhase at="problem" />

<Kicker>проблема</Kicker>

# Глазами не проверить, кодом не прочитать

<div class="grid grid-cols-[1fr_1.05fr] gap-6 mt-1">
<div class="pb">

<div class="card-soft"><b>Задача.</b> Windows-игра 2008 года — <i>Naruto: The Setting Dawn 2.4</i> на движке Little Fighter 2. Исходников нет — только скомпилированный exe. Нужна нативная игра для macOS, а потом и для остальных платформ.</div>

<div class="card-soft"><b>«Так же», а не «похоже».</b> Повтор матча в игре хранит не видео, а только нажатия кнопок; по сети игроки тоже обмениваются только нажатиями. Остальное каждая копия игры досчитывает сама. Если случайные числа или физика порта хоть раз разойдутся с оригиналом, повтор покажет другой бой, а сетевая партия развалится.</div>

<div class="card-soft"><b>Почему это вопрос доверия.</b> «Похоже» и «так же» выглядят одинаково — справа Mac и оригинал. Десятки тысяч строк человек не прочитает. А видимого прогресса может не быть неделями.</div>

<div class="ask"><span class="pixel">вопрос доклада</span>Можно ли дать агенту свободу и безлимит токенов — и чему тогда доверять, если не глазам и не ревью кода?</div>

</div>
<div>

<BeforeAfter before="/img/compare/summary-mac.jpg" after="/img/compare/summary-original.jpg" before-label="порт на Mac" after-label="оригинал для Windows" height="19.5rem" :start="50" />
<div class="xsmall muted mt-1">Таблица итогов одного и того же матча. Тяните ползунок — различий нет: их и не должно быть.</div>

</div>
</div>

<style>
.pb { display: flex; flex-direction: column; gap: .5rem; }
.pb .card-soft { font-size: .72rem; line-height: 1.42; color: var(--ink-2); padding: .5rem .75rem; }
.pb b { color: var(--ink); }
.pb code { font-size: .64rem !important; }
.ask { font-size: .82rem; line-height: 1.38; color: var(--ink); background: rgba(255,138,61,.1); border: 1px solid rgba(255,138,61,.5); border-radius: 12px; padding: .55rem .8rem; }
.ask .pixel { display: block; font-size: .6rem; color: var(--naruto); text-transform: uppercase; letter-spacing: .08em; margin-bottom: .2rem; }
</style>

<!--
≈ 60 секунд.

Главное на слайде — последний блок: вопрос доклада. Всё остальное — почему обычные способы доверять агенту здесь не работают.

Глазами: в LF2 «похоже» начинается с первого вечера — агент собрал тренировочную сцену за три часа. Но файл записи .lfr — это заголовок, таблица ГСЧ на 3 000 байт и по 10 байт ввода всех игроков на каждый тик; картинки в нём нет. Сетевой матч идёт lockstep: стороны обмениваются только вводом. Каждая программа пересчитывает матч сама, поэтому если физика или ГСЧ порта расходятся с оригиналом хоть на один тик, дальше матч идёт по-другому: в записи Наруто промахивается там, где в оригинале попал, а в сети у двух игроков на экранах разные матчи. Поэтому критерий — «так же».

Справа — один и тот же матч: слева таблица итогов в порте на Mac, справа оригинал под CrossOver проигрывает запись, сделанную на Mac. Совпадают все числа.
-->

---

<DemoPhase at="context" />

<Kicker>контекст · ограничения и термины</Kicker>

# Что было на руках

<div class="grid grid-cols-3 gap-3 mt-1 ctx">
<div class="card"><div class="h pixel">один exe — и годы доработок</div>Внутри — движок Little Fighter 2. Сообщество <b>годами дорабатывало игру без исходников</b>: правило байты прямо в exe — по словам моддеров, больше тысячи правок — и добавило маленькую библиотеку, которая при запуске <b>переписывает код игры в памяти</b>. Порт обязан повторить и движок, и все эти доработки.</div>
<div class="card"><div class="h pixel">без Windows</div>Настоящей Windows-машины в проекте так и не появилось. Эталон — <b>оригинал под CrossOver</b> (Wine) на Mac и <b>отдельные функции в Unicorn</b>.</div>
<div class="card"><div class="h pixel">человек — пара строк в день</div>У Codex — <b>163 сообщения человека против 383 автопродолжений</b> /goal за 20 дней. У Claude — <b>56 реплик за 241 час</b> одной сессии.</div>
</div>

<div class="grid grid-cols-[1fr_1fr] gap-4 mt-3">
<div class="card-soft terms">
<div class="pixel hl xsmall mb-1">термины</div>
<p><b>Харнесс</b> — всё вокруг модели, что превращает её вывод в проверенный результат: оракулы, тесты, ворота, журналы, ревьюеры.</p>
<p><b>Оракул</b> — эталон, который исполняют рядом с портом на тех же входах и сравнивают выходы. Здесь — сам код оригинала.</p>
<p><b>Ворота</b> — проверки, без которых шаг не коммитится; «exit 0» воротами не считается.</p>
</div>
<div class="card-soft terms">
<div class="pixel hl xsmall mb-1">агенты и бюджет</div>
<p><b>7–27 сентября</b> — Codex, GPT-6 Astra, режим <code>/goal</code>: одна цель, автопродолжения часами.</p>
<p><b>С 28 сентября</b> — Claude Code, Opus 5.5, режим <code>/loop</code>: агент сам будит себя по расписанию.</p>
<p><b>Подписки</b> ChatGPT Pro и Claude Max: <b>6,3 млрд токенов</b> до релиза 3 октября, ещё <b>4,6 млрд</b> прочитала одна сессия Claude 3–13 октября.</p>
</div>
</div>

<div class="ent mt-3">
<span class="lb">Codex, 7–27 сен</span>
<div class="sq"><i v-for="n in 163" :key="`h${n}`" class="h" /><i v-for="n in 383" :key="`g${n}`" class="g" /></div>
<span class="lg"><i class="h" />163 сообщения человека <i class="g" />383 автопродолжения /goal</span>
</div>

<div class="source">полная дека: главы 3, 4, 11 · data/sessions.json · data/tokens.json · data/epilogue.json</div>

<style>
.ctx .card { font-size: .7rem; line-height: 1.42; color: var(--ink-2); padding: .65rem .8rem; }
.ctx .h { font-size: .66rem; color: var(--naruto); text-transform: uppercase; letter-spacing: .06em; margin-bottom: .3rem; }
.ctx b, .terms b { color: var(--ink); }
.ctx code, .terms code { font-size: .62rem !important; }
.ent { display: grid; grid-template-columns: 7.2rem 1fr; column-gap: .8rem; row-gap: .3rem; align-items: center; }
.ent .lb { font-size: .64rem; color: var(--ink-2); }
.ent .sq { display: grid; grid-template-rows: repeat(6, 6px); grid-auto-flow: column; grid-auto-columns: 6px; gap: 2px; }
.ent .sq i, .ent .lg i { display: block; border-radius: 1.5px; }
.ent .h { background: var(--ink-2); }
.ent .g { background: var(--s1); }
.ent .lg { grid-column: 2; display: flex; align-items: center; gap: .35rem; font-size: .6rem; color: var(--muted); }
.ent .lg i { display: inline-block; width: 8px; height: 8px; margin-left: .5rem; }
.terms p { font-size: .68rem; line-height: 1.4; color: var(--ink-2); margin: .25rem 0 !important; }
</style>

<!--
≈ 60 секунд. Термины — коротко, они нужны для следующих слайдов.

Что за доработки. Exe — это движок Little Fighter 2 (Марти и Старски Вонги), поверх которого сообщество NTSD строило игру без исходников. Первый слой — правки байтов прямо в exe; в 2009 году моддеры писали: «the mods for LF2 include more than 1000 hex edits». Второй — lib.dll, 6 КБ, собрана в 2011 году, автор не установлен: точка входа exe уводится в пустое место кода и грузит DLL, а та переписывает 62 байта в 13 местах — 12 переходов и одна двухбайтовая правка (превращения, попадания, экран загрузки). Сама библиотека — не доработанный exe, а заплатка к нему. Без неё порт был бы портом другой игры: агент нашёл её 10 сентября и проверил, какие уже сверенные куски она задевает.

Человек: у Codex на одно сообщение человека приходилось около 2,3 автопродолжения /goal; у Claude 241-часовая сессия, 56 реплик человека за десять дней. Остальное агент делал сам.
-->

---

<DemoPhase at="solution" />

<Kicker>решение · кто что построил</Kicker>

# Человек — рамку, агент — механизмы

<div class="who2 mt-1">
<div class="col">
<div class="ch"><span class="pixel">человек · пара строк</span><span class="muted">что и зачем</span></div>
<div class="it"><span class="d mono">7 сен</span><span>«ориентируйся исключительно на исходную игру под windows»</span></div>
<div class="it"><span class="d mono">12 сен</span><span>принёс методологию ReAgent: ограниченные задачи, отдельный ревьюер, промежуточные результаты на диск → <code>AGENTS.md</code> 4 954 → 153 строки</span></div>
<div class="it"><span class="d mono">27 сен</span><span>правила прогресса: проверенное сразу переносить в приложение</span></div>
<div class="it"><span class="d mono">2 окт</span><span>«у нас же есть windows через crossover?» → сверка целыми матчами</span></div>
<div class="it"><span class="d mono">6 окт</span><span>«start the core redesign loop» — цели 33 / 16 / 8 мс на телефоне</span></div>
</div>
<div class="col ag">
<div class="ch"><span class="pixel">агент · сам</span><span class="muted">как и когда остановиться</span></div>
<div class="it"><span class="d mono">7 сен</span><span><b>оракул в Unicorn</b> — уже в первом коммите: ходьба совпала на 8 506 тиках кода оригинала</span></div>
<div class="it"><span class="d mono">9–10 сен</span><span><b>исходы вместо «прошло / упало»</b>: падение оригинала — <code>sourceFault</code>, сломанный стенд — <code>harness error</code></span></div>
<div class="it"><span class="d mono">сен</span><span><b>защиту оракула от ложных совпадений</b>: канарейки, куча <code>0xA5</code>, маски записей из самих инструкций копирования</span></div>
<div class="it"><span class="d mono">6 окт</span><span><b>правило коммита</b> — через 2 минуты после запуска петли; <b>харнесс телефона</b>: schedstat, A/B вперемешку, прогрев</span></div>
<div class="it"><span class="d mono">10 окт</span><span><b>остановка у «стены»</b> по своему правилу и четыре вопроса автору</span></div>
</div>
</div>

<div class="grid grid-cols-3 gap-3 mt-3 hx">
<div class="card-soft"><span class="pixel hl">215</span>скриптов-оракулов, 17 из них поднимают свою VM с кодом оригинала</div>
<div class="card-soft"><span class="pixel hl">567</span>карточек исследований: план замораживается до запуска, не больше 3 раундов на механизм</div>
<div class="card-soft"><span class="pixel hl">75</span>строк реестра петли на телефоне: у каждой свой evidence-файл, замер A/B и ревью</div>
</div>

<div class="moral mt-2"><b>Что делегировали:</b> как проверять и когда остановиться. <b>Что оставили себе:</b> цель, рамку и развилки, где нужен вкус или риск.</div>

<div class="source">журналы сессий Codex (7, 12 сен) и Claude Code (2, 6 окт) — только реплики автора и время · ffe16f4 · 007c007 · 0034e45c · docs/research/WORKFLOW.md · полная дека, главы 2–5, 8, 14–15</div>

<style>
.who2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.who2 .col { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: .5rem .7rem .55rem; display: flex; flex-direction: column; gap: .32rem; }
.who2 .col.ag { border-color: rgba(255,138,61,.5); }
.who2 .ch { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: .1rem; }
.who2 .ch .pixel { font-size: .72rem; color: var(--chakra); text-transform: uppercase; letter-spacing: .06em; }
.who2 .ag .ch .pixel { color: var(--naruto); }
.who2 .ch .muted { font-size: .62rem; }
.who2 .it { display: grid; grid-template-columns: 3.6rem 1fr; gap: .4rem; font-size: .66rem; line-height: 1.36; color: var(--ink-2); }
.who2 .it .d { font-size: .58rem; color: var(--muted); padding-top: .1rem; }
.who2 b { color: var(--ink); }
.who2 code { font-size: .56rem !important; }
.hx .card-soft { display: flex; align-items: baseline; gap: .6rem; font-size: .66rem; line-height: 1.38; color: var(--ink-2); }
.hx .pixel { font-size: 1.5rem; line-height: 1; }
.moral { font-size: .76rem; line-height: 1.4; color: var(--ink-2); background: rgba(255,138,61,.08); border: 1px solid rgba(255,138,61,.4); border-radius: 12px; padding: .45rem .8rem; }
.moral b { color: var(--ink); }
</style>

<!--
≈ 75 секунд. Центральный слайд доклада — и честная поправка к его заголовку. «Агент сам выстроил методологию» верно наполовину: механизмы проверки, харнесс замеров и правило остановки — его. Рамку задавал человек короткими репликами: исходная игра как единственный эталон, чужая методология ReAgent (разделение исполнителя и ревьюера), правила прогресса после 19 коммитов мимо приложения, вопрос про CrossOver, запуск петель и цели по миллисекундам.

Правило коммита петли: «Commit an increment only when every gate passes and it is either measurably faster or strictly less work without added complexity; otherwise record the result here and revert.» Его агент записал в карточку 6 октября в 03:48 — через две минуты после реплики автора «make an experimental branch and do core redesign for real time play on slow phones like A12… start the core redesign loop». В реплике автора правила нет.

Оракул: в первом коммите 7 сентября «Movement matches 8,506 reference ticks» — про Unicorn в репликах человека не было ни слова.
-->

---
clicks: 3
---

<DemoPhase at="solution" />

<Kicker>решение · слой 1 · дифференциальный оракул</Kicker>

# Код оригинала исполняется рядом с портом

<FlowDiagram stepwise class="mt-1" input="одни и те же входы" input-sub="состояние, аргументы, байты DAT" :lanes="[
  { title: 'NTSD 2.4.exe в Unicorn', sub: 'x86-код оригинала по 0x400000; импорты → страница-заглушка; настоящий MSVCR80', out: 'байты после вызова + маска записей, вызовы ГСЧ, события ресурсов', color: 'var(--s2)', tag: 'эталон' },
  { title: 'Swift-порт той же функции', sub: 'свои аллокации, свой откат', out: 'байты после вызова, вызовы ГСЧ, события', color: 'var(--s1)', tag: 'порт' },
]" verdict="совпало побайтно" verdict-sub="только там, где байт определён маской" />

<div class="grid grid-cols-3 gap-3 mt-2 orc">
<div class="card-soft"><b>Канарейки.</b> Регистры заполнены <code>0x11223344…</code>, куча — <code>0xA5</code>. Вызов засчитан, только если EIP дошёл до STOP, а стек и канарейки целы.</div>
<div class="card-soft"><b>Падение — тоже поведение.</b> Если оригинал упал, это исход <code>sourceFault</code>, а не «совпало». Порт обязан упасть так же — или объявить границу.</div>
<div class="card-soft"><b>Масштаб.</b> 215 скриптов-оракулов; VM создают 17, остальные наследуют её цепочкой: игра грузится, проходит меню и играет такты в одной VM.</div>
</div>

<div class="source">tools/oracle_*.py · полная дека, глава 3 «Оригинал исполняется рядом — в Unicorn»</div>

<style>
.orc .card-soft { font-size: .66rem; line-height: 1.4; color: var(--ink-2); }
.orc b { color: var(--ink); }
.orc code { font-size: .58rem !important; }
</style>

<!--
≈ 60 секунд. Это механизм, на котором держится всё доверие первых трёх недель.

Unicorn — эмулятор процессора (ядро QEMU как библиотека). Агент грузит в него секции настоящего EXE по их адресам, импорты Windows подменяет страницей-заглушкой: Python-обработчик снимает аргументы со стека и отвечает. Одни и те же входы подаются в функцию оригинала и в её Swift-порт, байты после вызова сравниваются по маске — только те, что функция реально записала.

Подвох, который агент нашёл сам: memory-хуки Unicorn увидели 259 526 из 524 454 байт, записанных инструкцией REP MOVSD, — маски теперь берутся из самих инструкций копирования.

Клики: входы → две программы → выходы → вердикт.
-->

---

<DemoPhase at="solution" />

<Kicker>решение · 7–27 сентября вслепую — 28 сентября вся игра</Kicker>

# Три недели без картинки — и игра за день

<BlindMonth class="mt-1" />

<div class="grid grid-cols-[1fr_1.2fr] gap-4 mt-1">
<div class="grid grid-cols-2 gap-2">
<StatTile value="801 → 801" label="строк в приложении" sub="21 день подряд" size="sm" accent="var(--s2)" />
<StatTile value="5 ч 44 мин" label="28 сен: до матча с KO" sub="от первого коммита Claude" size="sm" accent="var(--good)" />
</div>
<div class="card-soft bm"><b>Решение агента, 8 сентября:</b> «Не ускоряем видимый прогресс добавлением персонажей и техник на неполной основе… тренировочное окно некоторое время может выглядеть прежним».</div>
</div>

<div class="source">data/tokens.json (журналы сессий) · data/app_lines.json · ~/.codex/sessions: сессия-аудит 8 сентября · полная дека, глава 5</div>

<style>
.bm { font-size: .7rem; line-height: 1.42; color: var(--ink-2); }
.bm b { color: var(--ink); }
</style>

<!--
≈ 50 секунд. Здесь — суть доверия: 55 % всех токенов проекта ушло до первого матча в приложении. Снаружи это выглядело как сжигание денег: в окне — тренировочная сцена 7 сентября. Внутри росли ядро, оракулы и эталоны.

28 сентября Claude получил проект в 13:31: в 15:50 — матч Наруто против Саске в приложении, в 18:15 — первый KO, в 19:15 — повтор и Summary, к полуночи — 30 тиков в секунду. Это не скорость Claude: 39 300 строк, 81 % итогового кода, уже были написаны и сверены; в тот же день сменились и агент, и правила прогресса, их вклад по отдельности не измерен.

Автор после релиза: «Методология валидации — это всё. Это самое важное. Это ровно то, что в самом конце привело нас к полному паритету в интеграционных тестах».

Аудиторы Codex несколько раз писали: «прироста подтверждённых игровых возможностей нет». 12 сентября готовый чужой движок L2DF дал работающее приложение за 16 минут — и автор его остановил: «ок, остановил. продолжаем на main».
-->

---

<DemoPhase at="solution" />

<Kicker>решение · слой 2 · целое против частей</Kicker>

# Оракул ошибся вместе с портом

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-1">
<div class="small ink2 wh">

Десятки функций совпадали с Unicorn побайтно. Но записями матчей с оригиналом **обменяться было нельзя**: каждая сторона отвергала чужие файлы.

- Контрольная сумма каталога: у оригинала <code>0x1ec3356</code>, у порта <code>0x1e046b2</code>.
- Причина: из-за lookahead в CRT VC80 цикл <code>fscanf("%c")</code> / <code>feof</code> считает последний токен файла <b>дважды</b>.
- Unicorn давал то же неверное значение, что и порт: оба опирались на одну модель CRT.

<div class="card mt-2" style="border-color: rgba(255,138,61,.5)"><b class="ink">Механизм доверия:</b> части сверяет оракул, целое — настоящий рантайм. Запись матча с Mac проигрывается в оригинале под CrossOver, и обе программы должны выдать одну и ту же таблицу итогов.</div>

</div>
<div>

<div class="pixel hl xsmall mb-1">после правки · 58 из 58 целых матчей равны оригиналу</div>

<CrossplayTiles />

</div>
</div>

<div class="source">3313088 · 53bc59e · docs/research/APPLICATION_CATALOG_CHECKSUM.md · docs/evidence/crossplay-*.json · полная дека, глава 8</div>

<style>
.wh ul { margin-top: .35rem; }
.wh li { font-size: .7rem; line-height: 1.38; }
.wh code { font-size: .6rem !important; }
.wh .card { font-size: .7rem; line-height: 1.4; }
</style>

<!--
≈ 60 секунд. Самый важный механизм для доверия: оракул проверяет функцию против модели мира, которую мы сами в него заложили. Если модель CRT неверна, оракул и порт ошибаются одинаково, и «совпало» ничего не значит.

58 = 42 случайных матча Mac → оригинал (VS 32, Stage 6, War 4) + 5 матчей оригинал → Mac + 11 ранних повторов; все равны. Порт ни разу не разошёлся с оригиналом в целом матче — после правки контрольной суммы.

Отсюда урок «целое — не сумма частей»: 692 теста и 215 оракулов не заменили 58 целых матчей.
-->

---

<DemoPhase at="solution" />

<Kicker>решение · слой 3 · петля на настоящем телефоне</Kicker>

# Замер → правка → ворота → решение

<div class="grid grid-cols-[1.25fr_1fr] gap-5 mt-1">
<div>

<div class="stairs">
<div class="st"><span class="d mono">5 окт</span><div class="bar" style="width: 100%"><b>≈ 185 мс</b> на тик · 5,4 тика/с, первый доигранный матч</div></div>
<div class="st"><span class="d mono">6 окт</span><div class="bar" style="width: 53.5%"><b>≈ 99 мс</b> · 10,07 тика/с после 8 правок</div></div>
<div class="st"><span class="d mono">7 окт</span><div class="bar" style="width: 16.4%"><b>30,4 мс</b></div><span class="nt">главный поток · ярус 33 мс: темп оригинала</span></div>
<div class="st"><span class="d mono">8 окт</span><div class="bar" style="width: 9%"><b>16,7</b></div><span class="nt">60 fps · тег <code>rt-60fps-a12</code></span></div>
<div class="st"><span class="d mono">10 окт</span><div class="bar good" style="width: 6%"><b>11,1</b></div><span class="nt">главный поток · рендер 7,6 мс в своём потоке</span></div>
</div>
<div class="xsmall muted mt-1">Samsung Galaxy A12 — бюджетный телефон 2020 года, 2,8 ГБ памяти. До 6 октября — тики в секунду на часах харнесса, дальше — время работы потока на тик.</div>

<div class="grid grid-cols-3 gap-2 mt-3 mech">
<div class="card-soft"><b>Пиксели — в свой поток.</b> Тик игры больше не ждёт отрисовку: шаг 1e дал +17 % тиков в секунду.</div>
<div class="card-soft"><b>Один буфер вместо копий.</b> Запись состояния тика стала одним буфером: копирование массивов 9,40 → 4,96 % главного потока.</div>
<div class="card-soft"><b>Без проверок эксклюзивности.</b> Динамические проверки Swift стоили 3,5–4 % — сняли в релизе по решению автора.</div>
</div>

</div>
<div class="loop-r">

<div class="card-soft rule"><span class="pixel hl xsmall">правило коммита — агент записал сам, 6 окт 03:48</span><span class="mono">«Commit an increment only when every gate passes and it is either measurably faster or strictly less work without added complexity; otherwise record the result here and revert.»</span></div>

<div class="grid grid-cols-2 gap-2 mt-2">
<StatTile :value="480" label="прогонов на телефоне" sub="≈ 31 час матчей" size="sm" accent="var(--s1)" />
<StatTile :value="47" label="независимых ревью" sub="агент только для чтения" size="sm" accent="var(--s7)" />
<StatTile :value="37" label="ступеней быстрее" sub="из 75 строк реестра" size="sm" accent="var(--good)" />
<StatTile :value="8" label="не закоммичено" sub="2 отката, 6 отложено" size="sm" accent="var(--serious)" />
</div>

</div>
</div>

<div class="source">полная дека, главы 14–15 · docs/research/CORE_REALTIME.md (Gates, Ledger) · data/rt2_loop.json · data/perf_*.json</div>

<style>
.stairs { display: flex; flex-direction: column; gap: .4rem; }
.st { display: grid; grid-template-columns: 3.4rem 1fr; align-items: center; gap: .5rem; position: relative; }
.st .d { font-size: .62rem; color: var(--muted); }
.st .bar { height: 1.55rem; background: linear-gradient(90deg, rgba(217,89,38,.85), rgba(217,89,38,.55)); border-radius: 5px; display: flex; align-items: center; padding: 0 .5rem; font-size: .64rem; color: var(--ink); white-space: nowrap; overflow: visible; min-width: 2.6rem; }
.st .bar.good { background: var(--good); }
.st .bar b { margin-right: .35rem; }
.st .nt { position: absolute; left: calc(3.4rem + .5rem + 18%); font-size: .62rem; color: var(--ink-2); }
.st .nt code { font-size: .56rem !important; }
.mech .card-soft { font-size: .62rem; line-height: 1.38; color: var(--ink-2); padding: .4rem .55rem; }
.mech b { color: var(--ink); }
.rule { display: flex; flex-direction: column; gap: .3rem; font-size: .66rem; line-height: 1.4; color: var(--ink); }
</style>

<!--
≈ 75 секунд. Тут можно копнуть в механизмы — аудитории это нравится. Три хитрости, которые агент нашёл сам:
1. Запись состояния одним буфером (S2b): копирование массивов в профиле главного потока упало с 9,40 до 4,96 %. По дороге первый прогон тестов встал на два часа: проверки, читавшие целые массивы в цикле, стали квадратичными.
2. Пиксели — в свой поток: рендер отделён от логики тика, вывод кадра на экран Android — ещё в отдельный поток presenter.
3. Проверки эксклюзивности Swift (exclusivity checks) стоили 3,5–4 % главного потока; снять их в релизных сборках решил автор, агент только спросил — и девять часов ждал ответа.

Как устроена петля: автор запустил /loop с одним текстом; каждый оборот — одна механика, одна строка реестра и один evidence-файл. Телефон «плывёт» между сессиями, поэтому прежнюю сборку гоняли вперемешку с новой в той же сессии; разрешение — около ±0,25 мс на прогон.

Оговорка о метрике: 185 мс — это 1 / 5,4 тика в секунду на часах харнесса, когда весь тик шёл в одном потоке. 11,1 мс — работа главного потока на тик, рендер к этому времени уже в своём потоке. Сравнивать как «во сколько раз» нечестно, как путь — честно.
-->

---

<DemoPhase at="solution" />

<Kicker>решение · где остановиться · 10 октября, 18:27</Kicker>

# Плато нашёл агент — по своему же правилу

<Rt2Wall class="mt-1" />

<div class="wl mt-1"><b class="hl mono">0034e45c:</b> «…none meets the commit rule» <span class="muted">→</span> <b class="hl">автор, 21:23:</b> «you did good. we reached the wall… now lets do the loop for optimizing memory footprint and loading times»</div>

<div class="source">0034e45c · docs/research/CORE_REALTIME_TIER3.md · data/rt2_wall.json · сессия Claude Code 1f9218ae · полная дека, глава 15 «Стена»</div>

<style>
.wl { font-size: .62rem; line-height: 1.35; color: var(--ink); }
</style>

<!--
≈ 60 секунд. Ответ на вопрос «где плато и сколько токенов тратить». В этом проекте его дал не человек: правило коммита запрещает шаги ниже разрешения замера и шаги, которые добавляют второй путь кода. Когда таких шагов не осталось, петля остановилась и задала автору четыре вопроса — что можно менять в поведении после сбоя.

Самое неожиданное: план яруса 3 писал отдельный агент только для чтения вечером 8 октября, когда главный поток был на 16,25 мс: «без решений — около 11 мс на главном потоке и около 8 на рендере». Через 44 часа последний замер дал 11,09 и 7,55. Путь был другим, а стена оказалась там, где её нарисовали.
-->

---

<DemoPhase at="demo" />

<Kicker>демо · 2–3 минуты</Kicker>

# Живьём: та же игра — против оригинала

<div class="grid grid-cols-[1.25fr_1fr] gap-5 mt-1">
<div>

<WindowFrame video="/media/demo-side-by-side.mp4" poster="/media/demo-poster.jpg" title="слева — нативное Swift-приложение · справа — оригинальный NTSD 2.4.exe под CrossOver" />
<div class="xsmall muted mt-1">Режим Demo, восемь бойцов, один и тот же сид: кадры совпадают тик в тик. Запасной вариант, если живая демка не поедет.</div>

</div>
<div class="steps">

<div class="sp"><span class="n pixel">1</span><div><b>Браузер, холодный визит</b><code>ntsd-web-ashy.vercel.app</code><span>меню через ≈ 2 с, сыграть VS 20 секунд: Swift в WebAssembly, те же 18 088 кадров эталона</span></div></div>

<div class="sp"><span class="n pixel">2</span><div><b>Харнесс за работой</b><code>python3 tools/app_e2e.py --scenario vs</code><span>целый матч на виртуальных часах; вехи, кадры и повтор сравниваются с замороженным эталоном</span></div></div>

<div class="sp"><span class="n pixel">3</span><div><b>Если сеть подведёт</b><code>видео слева</code><span>режим Demo: Mac и оригинал рядом, один сид, кадры тик в тик</span></div></div>

</div>
</div>

<div class="source">docs/media/demo-side-by-side.mp4 · tools/crossover_drive/demo_frames.py · tools/app_e2e.py · ntsd-web-ashy.vercel.app (W5, 17 октября)</div>

<style>
.steps { display: flex; flex-direction: column; gap: .5rem; }
.sp { display: grid; grid-template-columns: 1.7rem 1fr; gap: .5rem; background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: .45rem .6rem; }
.sp .n { display: flex; align-items: center; justify-content: center; width: 1.5rem; height: 1.5rem; border-radius: 50%; background: rgba(255,138,61,.18); color: var(--naruto); font-size: .8rem; }
.sp b { display: block; font-size: .74rem; color: var(--ink); }
.sp code { display: inline-block; font-size: .6rem !important; margin: .15rem 0; }
.sp span:last-child { display: block; font-size: .62rem; line-height: 1.38; color: var(--ink-2); }
</style>

<!--
Демо — после цикла «проблема → контекст → решение», до результатов, как просят организаторы.

1. Открыть в браузере с чистым профилем: меню через ~2 секунды (до 17 октября — 9,3 с и 46,5 с до всех данных). Выбрать VS, Наруто против Саске, сыграть несколько секунд.
2. Если есть время и собрано приложение: запустить e2e-сценарий vs — он сам выбирает режим и бойцов, доигрывает матч и сверяет вехи с эталоном. Занимает около минуты; показать вывод «equal».
3. Если сеть подведёт — видео слева: режим Demo, Mac и оригинал рядом, кадры совпадают.
-->

---

<DemoPhase at="results" />

<Kicker>результаты · как мы поняли, что это работает</Kicker>

# Доказательства, а не впечатления

<div class="grid grid-cols-4 gap-3 mt-1">
<StatTile value="58 / 58" label="целых матчей равны оригиналу" sub="запись Mac → оригинал и обратно" size="sm" accent="var(--good)" />
<StatTile value="18 088" label="кадров — одинаково на всех хостах" sub="90 из 90 сценариев на 9 хостах" size="sm" accent="var(--good)" />
<StatTile value="30,4 → 11,1 мс" label="главный поток на тик, Galaxy A12" sub="60 fps; первый матч шёл 5,4 тика/с" size="sm" accent="var(--s2)" />
<StatTile value="131,9 → 12,7 с" label="от иконки до меню на A12" sub="пик памяти 1,6 ГБ → 565 МиБ" size="sm" accent="var(--s1)" />
</div>

<div class="grid grid-cols-3 gap-3 mt-3 res">
<div class="card"><div class="h pixel">чем мерили</div>Не «выглядит так же», а: побайтные сравнения с кодом оригинала, целые матчи против оригинала под CrossOver, замороженные эталоны кадров, A/B-прогоны на телефоне. <b>Ни один эталон не переписан под код.</b></div>
<div class="card"><div class="h pixel">что получилось</div>Нативная игра на macOS, Linux, Windows, iPad, Android и в браузере, на Steam Deck — из Game Mode; Apple TV и iPhone — пока в симуляторе. Два релиза на шесть платформ, macOS — с нотаризацией Apple.</div>
<div class="card"><div class="h pixel">сколько стоило</div>Две подписки по $200 в месяц. По номиналу Codex съел ≈ $266 на порт; работа Claude за первые 6 дней по ценам API стоила бы ≈ $797. 756 коммитов за 37 дней; человек — пара строк в день.</div>
</div>

<div class="source">полная дека: главы 8, 13–17, 19 · data/evidence/crossplay-matches.json · data/xplat.json · data/rt2_steps.json · data/loading_race.json · data/tokens.json</div>

<style>
.res .card { font-size: .68rem; line-height: 1.42; color: var(--ink-2); padding: .65rem .8rem; }
.res .h { font-size: .64rem; color: var(--naruto); text-transform: uppercase; letter-spacing: .06em; margin-bottom: .3rem; }
.res b { color: var(--ink); }
</style>

<!--
≈ 60 секунд. Каждая цифра — из evidence-файла порта. 18 088 кадров — эталонные прогоны десяти сценариев; на каждом новом хосте (Linux, Windows под CrossOver, iPad, Android, Apple TV, WASI, Chromium, WebKit, iPhone) кадры сравнивались с теми же замороженными эталонами — равны.

Метрика: 30,4 → 11,1 мс — одна и та же мера (работа главного потока на тик, schedstat), в 2,7 раза. Первый доигранный матч на телефоне шёл 5,4 тика в секунду (≈ 185 мс на тик на часах харнесса, включая сон самой игры) — эти числа нельзя делить друг на друга.
-->

---

<DemoPhase at="results" />

<Kicker>результаты · где доверие ломалось — и что это поймало</Kicker>

# Агент ошибался. Важно, кто это замечал

<div class="brk mt-1">
<div class="hd">ошибка</div><div class="hd">кто поймал</div>
<div class="e"><b>Контрольная сумма каталога</b> совпадала с оракулом — и была неверной: оба разделяли одну модель CRT</div><div class="c w">целый матч против оригинала под CrossOver</div>
<div class="e"><b>Пропуск F8</b>: агент заменил известное поведение EXE «объявленным пропуском»</div><div class="c r">независимое ревью — «its slot word is not unknown»</div>
<div class="e"><b>Девять стендов</b> не заметили лишних 2,5 ГБ памяти</div><div class="c h">настоящий телефон: Galaxy A12 убил игру на загрузке</div>
<div class="e"><b>Браузерная версия</b> на стенде грузилась за 5,6 с, на живом сайте — 46,5 с: стенд не моделировал задержку CDN</div><div class="c h">автор открыл живой сайт</div>
<div class="e"><b>Контроллер по фото</b> агент опознал как Backbone One</div><div class="c h">USB-отчёт самого устройства: Razer Kishi V2</div>
<div class="e"><b>Коммит «только документация»</b> захватил чужие <code>git mv</code> — дерево не собиралось 22 минуты</div><div class="c a">сам агент, следующим коммитом</div>
</div>

<div class="leg"><span><i class="w" />рантайм оригинала</span><span><i class="r" />ревьюер только для чтения</span><span><i class="h" />железо и человек</span><span><i class="a" />сам агент</span></div>

<div class="card punch mt-3"><span class="pixel hl">1 из 6</span><span>Сам агент заметил только одну ошибку — и то после того, как хук уже отправил её на GitHub. Остальные пять поймали слои, которые от агента не зависят. Доверие здесь — не вера в безошибочность, а уверенность, что ошибку заметит кто-то другой.</span></div>

<div class="source">полная дека: главы 7, 8, 13, 14, 18, 19 · 698f76a · 3313088 · 2f5e707 · d4619cbc · tw-w5-web-packed-loading-20261017.json</div>

<style>
.brk { display: grid; grid-template-columns: 1.35fr 1fr; gap: .32rem .8rem; }
.brk .hd { font-family: var(--font-pixel); font-size: .6rem; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; }
.brk .e { font-size: .68rem; line-height: 1.38; color: var(--ink-2); background: var(--surface); border: 1px solid var(--hair); border-radius: 8px; padding: .32rem .6rem; }
.brk .e b { color: var(--ink); }
.brk .e code { font-size: .58rem !important; }
.brk .c { font-size: .66rem; line-height: 1.35; color: var(--ink); border-radius: 8px; padding: .32rem .6rem; display: flex; align-items: center; border-left: 4px solid; background: rgba(255,255,255,.03); }
.brk .c.w, .leg i.w { border-color: var(--s2); }
.brk .c.r, .leg i.r { border-color: var(--s7); }
.brk .c.h, .leg i.h { border-color: var(--s1); }
.brk .c.a, .leg i.a { border-color: var(--s3); }
.leg { display: flex; gap: 1.1rem; margin-top: .5rem; font-size: .62rem; color: var(--ink-2); }
.punch { display: flex; align-items: center; gap: 1rem; font-size: .74rem; line-height: 1.42; color: var(--ink); border-color: rgba(255,138,61,.5); }
.punch .pixel { font-size: 1.5rem; white-space: nowrap; }
.leg i { display: inline-block; width: 12px; height: 12px; border-left: 4px solid; margin-right: .35rem; vertical-align: -2px; }
</style>

<!--
≈ 60 секунд. Доверие здесь — не вера в то, что агент не ошибается. Он ошибался регулярно. Доверие — это уверенность, что ошибку поймает слой, который от агента не зависит: рантайм оригинала, отдельный ревьюер только для чтения, железо, человек.

Обратите внимание на правую колонку: сам агент поймал только git-ошибку — и то после того, как хук post-commit уже отправил её на GitHub. Всё остальное поймали независимые слои. Поэтому их и нужно строить с первого дня.
-->

---

<DemoPhase at="lessons" />

<Kicker>уроки · что из этого факт, а что — ощущение</Kicker>

# Что я унёс

<div class="les mt-1">
<div class="l f"><span class="tg">факт</span><div><b>Доверие строится на независимых слоях, а не на вере в агента.</b> Пять из шести ошибок поймали оригинал, ревьюер, железо и человек, и только одну — сам агент.</div></div>
<div class="l f"><span class="tg">факт</span><div><b>Целое — не сумма частей.</b> 692 теста и 215 оракулов не заметили ошибки, которую поймал первый же обмен записями целого матча.</div></div>
<div class="l f"><span class="tg">факт</span><div><b>Механизмы проверки агент строит сам — и сам находит, где остановиться.</b> Правило коммита он записал через 2 минуты после запуска петли и по нему же остановился на 11,1 мс.</div></div>
<div class="l f"><span class="tg">факт</span><div><b>Рамку задаёт человек.</b> Без правила «проверенное — сразу в приложение» с 14 по 27 сентября только 1 коммит из 115 дошёл до кода игры.</div></div>
<div class="l f"><span class="tg">факт</span><div><b>Стенд — не железо.</b> Девять стендов не заметили лишних 2,5 ГБ памяти, локальный сервер — задержки CDN.</div></div>
<div class="l v"><span class="tg">вайб</span><div><b>«Правильно обученная модель и есть харнесс».</b> Здесь модель написала харнесс сама, но методологию разделения ролей принёс человек. Где граница — моё ощущение, не замер.</div></div>
<div class="l v"><span class="tg">вайб</span><div><b>Сколько токенов «достаточно» — открытый вопрос.</b> От v0.4.0 до стены — 221 коммит и +43,7 тыс. строк; на сам путь 30,4 → 11,1 мс — 140 коммитов и +4,8 тыс. строк Swift. Стоит ли — зависит от цели.</div></div>
</div>

<div class="source">полная дека: главы 5, 8, 13–15, 20 · git v0.4.0..0034e45c и 109304a..0034e45c (--shortstat; native/Sources отдельно) · журнал сессии 1f9218ae (6 окт, 03:46 и 03:48)</div>

<style>
.les { display: flex; flex-direction: column; gap: .32rem; }
.les .l { display: grid; grid-template-columns: 3.4rem 1fr; gap: .6rem; align-items: start; background: var(--surface); border: 1px solid var(--hair); border-radius: 10px; padding: .36rem .65rem; font-size: .68rem; line-height: 1.36; color: var(--ink-2); }
.les b { color: var(--ink); }
.les .tg { font-family: var(--font-pixel); font-size: .6rem; text-align: center; border-radius: 999px; padding: .08rem 0; margin-top: .1rem; }
.les .f .tg { color: var(--good); border: 1px solid rgba(12,163,12,.6); }
.les .v .tg { color: var(--warning); border: 1px solid rgba(250,178,25,.6); }
.les .v { border-color: rgba(250,178,25,.3); }
</style>

<!--
≈ 75 секунд. Организаторы просят явно отделять факты от вайба — поэтому метки слева.

1. Пять из шести — таблица с предыдущего слайда: контрольная сумма (рантайм оригинала), пропуск F8 (ревьюер), память (телефон), загрузка в браузере (человек на живом сайте), контроллер (USB-отчёт); сам агент — только коммит, захвативший чужие git mv.
2. Контрольная сумма каталога: оракул и порт опирались на одну модель CRT.
3. Правило коммита — 6 октября в 03:48, реплика автора «start the core redesign loop» — в 03:46, правила в ней нет. Стена — 0034e45c, 10 октября.
4. 1 коммит из 115 менял native/Sources с 14 по 27 сентября; правила прогресса записаны 27 сентября по указанию автора, и на следующий день игра собралась.
5. Девять стендов — глава 13; Galaxy A12 убил игру на загрузке (глава 14); живой сайт — 46,5 с до всех данных против 5,6 с на стенде без задержки.
6. Моя гипотеза «модель и есть харнесс» — вайб. Наблюдение в её пользу: оракул, исходы, харнесс замеров и правило остановки агент придумал сам. Против: разделение исполнителя и ревьюера пришло из чужой методологии (ReAgent), которую принёс человек.
7. Цифры «221 коммит и +43 тыс. строк» — это весь диапазон v0.4.0..0034e45c: в него входят девять хостов, память и ~20,6 тыс. строк JSON с доказательствами. Сам путь скорости, 109304a..0034e45c: 140 коммитов, native/Sources +4 824 / −816.
-->

---
layout: hero
image: /img/covers/end-valley-of-the-end.jpg
align: center
shade: 0.7
---

<div class="flex flex-col items-center">
<Kicker>спасибо · вопросы</Kicker>
<h1 class="cover-title">Делегируйте «как».<br><span class="hl">Оставьте себе «зачем».</span></h1>
<p class="small ink" style="max-width: 40rem; margin-top: -0.3rem">Агент построил оракул, харнесс и правило остановки сам. Человек задал рамку и принимал решения на развилках. Остальное проверяли слои, которые от агента не зависят.</p>
<p class="small ink2" style="max-width: 40rem">Игра в браузере: <span class="mono">ntsd-web-ashy.vercel.app</span> · порт: <span class="mono">github.com/wowlocal/ntsd-2.4</span> · полная версия доклада — 195 слайдов: <span class="mono">github.com/wowlocal/ntsd-port-story</span></p>
</div>

<style>
.cover-title { font-size: 2.6rem !important; line-height: 1.1 !important; margin: 0.3rem 0 0.8rem !important; text-align: center; }
</style>

<!--
Финальная мысль — одной фразой: доверять агенту можно настолько, насколько независимы слои, которые проверяют его работу. Механизмы он строит сам; цель и развилки — ваши.
-->
