---
clicks: 0
---

<DemoPhase at="problem" />

<Kicker>проблема</Kicker>

# Глазами не проверить, кодом не прочитать

<div class="grid grid-cols-[0.8fr_1.2fr] gap-7 mt-2 items-center">
<div class="beats">

<div class="bt"><span class="big">0</span><div><b>строк исходников</b><span>ни у игры 2008 года, ни у её движка — только бинарники</span></div></div>

<div class="bt"><span class="big">=</span><div><b>так же, а не похоже</b><span>та самая игра, какой я её помню; совместимость с оригиналом — бонус</span></div></div>

</div>
<div>

<BeforeAfter before="/img/compare/summary-mac.jpg" after="/img/compare/summary-original.jpg" before-label="порт" after-label="оригинал" height="17.5rem" :start="50" />

</div>
</div>

<div class="ask mt-5"><span class="pixel">вопрос доклада</span>Чему доверять агенту, если разницу не видно глазами, а код не прочитать?</div>

<style>
.beats { display: flex; flex-direction: column; gap: 1.4rem; }
.bt { display: grid; grid-template-columns: 4.2rem 1fr; gap: .9rem; align-items: center; }
.bt .big { font-family: var(--font-display); font-weight: 700; font-size: 3.6rem; line-height: 1; color: var(--naruto); text-align: center; }
.bt b { display: block; font-family: var(--font-display); font-size: 1.05rem; color: var(--ink); margin-bottom: .2rem; }
.bt span:not(.big) { display: block; font-size: .8rem; line-height: 1.38; color: var(--ink-2); }
.ask { font-size: 1.05rem; line-height: 1.38; color: var(--ink); background: rgba(255,138,61,.1); border: 1px solid rgba(255,138,61,.5); border-radius: 12px; padding: .6rem 1rem; }
.ask .pixel { display: block; font-size: .6rem; color: var(--naruto); text-transform: uppercase; letter-spacing: .08em; margin-bottom: .2rem; }
</style>

<!--
≈ 60 секунд.

Главное на слайде — последний блок: вопрос доклада. Всё остальное — почему обычные способы доверять агенту здесь не работают.

Мотив — личный: вернуть игру ровно такой, какой я её помню. «Похоже» начинается с первого вечера — агент собрал тренировочную сцену за три часа, — но в ней был придуманный HUD и «примерная» физика. Цель — полностью идентичный опыт.

Почему совместимость с оригиналом — следствие, а не отдельная задача. Файл повтора .lfr — это заголовок, таблица случайных чисел на 3 000 байт и по 10 байт ввода всех игроков на каждый тик; картинки в нём нет. Сетевой матч идёт lockstep: стороны обмениваются только вводом. Каждая программа пересчитывает матч сама, поэтому совпадает всё — или ничего: один тик другой физики, и в повторе Наруто промахивается там, где в оригинале попал. Раз порт совпадает тик в тик, повторы ходят в обе стороны: 58 из 58 матчей, Mac → оригинал и обратно.

Честная оговорка про сеть: порт говорит протоколом оригинала без изменений (TCP 12345, таблица на 3 001 байт, 22 байта на тик), и сетевые партии между хостами порта — Mac, Linux, Windows под CrossOver, Android — проверены. А партию порта против самого оригинального exe по сети ещё никто не сыграл — поэтому на слайде «можно сыграть», а не «сыграли». Если спросят — так и сказать.

Справа — один и тот же матч: слева таблица итогов в порте на Mac, справа оригинал под CrossOver проигрывает запись, сделанную на Mac. Совпадают все числа.
-->

---

<DemoPhase at="solution" />

<Kicker>решение · кто что построил</Kicker>

# Человек — рамку, агент — механизмы

<div class="who2 mt-2">
<div class="col">
<div class="ch"><span class="pixel">человек</span></div>
<div class="it"><span class="d mono">7 сен</span><span>только исходная игра <i>— единственный эталон</i></span></div>
<div class="it"><span class="d mono">12 сен</span><span>методология ReAgent <i>— отдельный ревьюер</i></span></div>
<div class="it"><span class="d mono">27 сен</span><span>правила прогресса <i>— проверенное сразу в игру</i></span></div>
<div class="it"><span class="d mono">2 окт</span><span>сверка через CrossOver <i>— целыми матчами</i></span></div>
<div class="it"><span class="d mono">6 окт</span><span>петля на телефоне <i>— цели 33 / 16 / 8 мс</i></span></div>
</div>
<div class="col ag">
<div class="ch"><span class="pixel">агент</span></div>
<div class="it"><span class="d mono">7 сен</span><span>оракул на коде оригинала <i>— в первом же коммите</i></span></div>
<div class="it"><span class="d mono">9 сен</span><span>исходы вместо «прошло / упало» <i>— падение тоже результат</i></span></div>
<div class="it"><span class="d mono">сен</span><span>защита от ложных совпадений <i>— канарейки, маски</i></span></div>
<div class="it"><span class="d mono">6 окт</span><span>правило коммита <i>— через 2 минуты после запуска петли</i></span></div>
<div class="it"><span class="d mono">10 окт</span><span>остановка у «стены» <i>— и четыре вопроса мне</i></span></div>
</div>
</div>

<DemoVolume class="mt-3" />

<div class="moral mt-2"><b>Делегировали:</b> как проверять и когда остановиться. <b>Оставили себе:</b> цель, рамку и развилки.</div>

<style>
.who2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.who2 .col { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: .6rem .9rem .7rem; display: flex; flex-direction: column; gap: .45rem; }
.who2 .col.ag { border-color: rgba(255,138,61,.5); }
.who2 .ch { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: .1rem; }
.who2 .ch .pixel { font-size: .72rem; color: var(--chakra); text-transform: uppercase; letter-spacing: .06em; }
.who2 .ag .ch .pixel { color: var(--naruto); }
.who2 .ch .muted { font-size: .62rem; }
.who2 .it { display: grid; grid-template-columns: 3.6rem 1fr; gap: .4rem; font-size: .8rem; line-height: 1.3; color: var(--ink); }
.who2 .it i { font-style: normal; color: var(--ink-2); }
.who2 .it .d { font-size: .62rem; color: var(--muted); padding-top: .25rem; }
.who2 b { color: var(--ink); }
.who2 code { font-size: .56rem !important; }
.hx .card-soft { display: flex; align-items: baseline; gap: .6rem; font-size: .66rem; line-height: 1.38; color: var(--ink-2); }
.hx .pixel { font-size: 1.5rem; line-height: 1; }
.moral { font-size: .76rem; line-height: 1.4; color: var(--ink-2); background: rgba(255,138,61,.08); border: 1px solid rgba(255,138,61,.4); border-radius: 12px; padding: .45rem .8rem; }
.moral b { color: var(--ink); }
</style>

<!--
Что было на слайде раньше — говорить словами.
Человек: 7 сен — «ориентируйся исключительно на исходную игру под windows»; 12 сен — принёс методологию ReAgent (ограниченные задачи, отдельный ревьюер, промежуточные результаты на диск) → AGENTS.md 4 954 → 153 строки; 27 сен — правила прогресса: проверенное сразу переносить в приложение; 2 окт — «у нас же есть windows через crossover?» → сверка целыми матчами; 6 окт — «start the core redesign loop», цели 33 / 16 / 8 мс на телефоне.
Агент: 7 сен — оракул в эмуляторе процессора уже в первом коммите (ходьба совпала на 8 506 тиках кода оригинала); 9–10 сен — исходы вместо «прошло / упало» (падение оригинала — sourceFault, сломанный стенд — harness error); защита оракула от ложных совпадений — канарейки, куча 0xA5, маски записей из самих инструкций копирования; 6 окт — правило коммита через 2 минуты после запуска петли и харнесс телефона (schedstat, A/B вперемешку, прогрев); 10 окт — остановка у «стены» по своему правилу и четыре вопроса автору.
Итог: делегировали «как проверять и когда остановиться», себе оставили цель, рамку и развилки.

≈ 75 секунд. Центральный слайд доклада — и честная поправка к его заголовку. «Агент сам выстроил методологию» верно наполовину: механизмы проверки, харнесс замеров и правило остановки — его. Рамку задавал человек короткими репликами: исходная игра как единственный эталон, чужая методология ReAgent (разделение исполнителя и ревьюера), правила прогресса после 19 коммитов мимо приложения, вопрос про CrossOver, запуск петель и цели по миллисекундам.

Правило коммита петли: «Commit an increment only when every gate passes and it is either measurably faster or strictly less work without added complexity; otherwise record the result here and revert.» Его агент записал в карточку 6 октября в 03:48 — через две минуты после реплики автора «make an experimental branch and do core redesign for real time play on slow phones like A12… start the core redesign loop». В реплике автора правила нет.

Оракул: в первом коммите 7 сентября «Movement matches 8,506 reference ticks» — про Unicorn в репликах человека не было ни слова.

Объём внизу — на origin/main 19 октября, одна строка = перевод строки в файле (пустые и комментарии тоже, как в паспорте полной деки). Игра: Swift модулей, которые уходят игроку, — 47 471 строка, плюс браузерный хост (JS/HTML) — 1 549; всего ≈ 49 тыс. Харнесс ≈ 154 тыс.: тесты Swift 52 958, оракулы на коде оригинала (215 скриптов tools/oracle_*.py) 37 088, сверочные программы Swift 12 171, прочие инструменты — остальной Python, shell и JS — 52 231. В 3,2 раза больше кода, чем сама игра. Не считались вендорные C-библиотеки (zlib 1.1.4, ALAC, обвязки — 9 632 строки). Рядом с кодом — 598 карточек исследований (≈ 610 тыс. слов) и 1 055 файлов доказательств (39,4 МБ JSON). Всё это написали агенты.
-->

---

<DemoPhase at="solution" />

<Kicker>решение · 12 сентября · после ложных срабатываний фильтра безопасности</Kicker>

# Методология из чужого репозитория

<div class="ra mt-4">
<div class="src">
<div class="nm2"><span class="i-pixelarticons-github" />ReAgent</div>
<div class="sub2">агент для реверс-инжиниринга: Ghidra + LLM</div>
<div class="cyc"><span>реверсер</span><i>→</i><span>проверяющий</span><i>→</i><span>правка</span></div>
</div>
<span class="ar2">→</span>
<div class="took">
<div><span class="i-pixelarticons-crop" />задача с границами</div>
<div><span class="i-pixelarticons-users" />исполнитель и ревьюер — разные агенты</div>
<div><span class="i-pixelarticons-save" />всё промежуточное — на диск</div>
</div>
</div>

<div class="shrink mt-6">
<div><span class="lb2">AGENTS.md</span><b>4 954</b><i>→</i><b class="hl">153</b><span class="lb2">строки</span></div>
</div>

<style>
.ra { display: grid; grid-template-columns: 1fr auto 1.1fr; gap: 1.4rem; align-items: center; }
.ra .src { background: var(--surface); border: 1px solid var(--hair); border-radius: 14px; padding: 1rem 1.1rem; }
.ra .nm2 { display: flex; align-items: center; gap: .55rem; font-family: var(--font-display); font-weight: 700; font-size: 1.6rem; color: var(--ink); }
.ra .nm2 span { width: 1.6rem; height: 1.6rem; color: var(--ink-2); }
.ra .sub2 { font-size: .82rem; color: var(--ink-2); margin: .3rem 0 .8rem; }
.ra .cyc { display: flex; align-items: center; gap: .45rem; font-size: .8rem; }
.ra .cyc span { background: var(--surface-2); border-radius: 8px; padding: .2rem .55rem; color: var(--ink); }
.ra .cyc i { font-style: normal; color: var(--naruto); }
.ra .ar2 { font-family: var(--font-display); font-size: 2rem; color: var(--naruto); }
.ra .took { display: flex; flex-direction: column; gap: .7rem; }
.ra .took div { display: flex; align-items: center; gap: .7rem; font-size: 1rem; color: var(--ink); background: rgba(255,138,61,.07); border: 1px solid rgba(255,138,61,.4); border-radius: 12px; padding: .55rem .8rem; }
.ra .took span { flex: none; width: 1.4rem; height: 1.4rem; color: var(--naruto); }
.shrink { display: flex; align-items: baseline; justify-content: center; gap: 1.6rem; }
.shrink > div:first-child { display: flex; align-items: baseline; gap: .8rem; }
.shrink b { font-family: var(--font-display); font-size: 2.6rem; line-height: 1; color: var(--ink); }
.shrink i { font-style: normal; font-size: 1.6rem; color: var(--naruto); }
.shrink .lb2 { font-family: var(--font-mono); font-size: .85rem; color: var(--ink-2); }
.shrink .when { font-size: .85rem; color: var(--muted); }
</style>

<!--
≈ 60 секунд. Деталь к пункту «методология ReAgent» с прошлого слайда.

Что случилось. К 12 сентября агент Codex раз за разом упирался в ложные срабатывания фильтра кибербезопасности (cyber_policy): работа с бинарником и эмулятором похожа на взлом. Автор нашёл открытый проект ReAgent (github.com/Dryxio/reagent) и в 08:31 по местному времени спросил: «как думаешь использование методологии отсюда … и переключение на более слабую модель даст нам то же качество и меньше срабатываний конкретно в нашем проекте?». В 08:35: «давай докрутим нашу методологию позаимствовав хорошие идеи из проекта который я тебе скинул и уменьшив риск ложного срабатывания сайбер полиси. я смогу запустить новый goal с обновленной методологией». В 08:49 — коммит ffe16f4.

Что такое ReAgent: открытый агент для реверс-инжиниринга — Ghidra и LLM (Claude, Codex) восстанавливают функции C/C++ из скомпилированного бинарника. Внутри — цикл реверсер → проверяющий → правка с ограниченным числом раундов, независимые модели-реверсер и модель-проверяющий, ворота сборки и тестов, журналы и чекпойнты каждого раунда.

Что взяли (дословно из WORKFLOW.md, раздел «Основания изменений»): «ограниченные задачи, разделение исполнителя и reviewer и сохранение промежуточных результатов». Чего не взяли: ReAgent не устанавливали и модель не меняли; его сравнение сопоставляет JSON-наблюдения, подготовленные самим проектом, — свои компараторы порта остались.

Что получилось в том же коммите: AGENTS.md сжат с 4 954 до 153 строк — до этого 167 из 175 коммитов дописывали туда журнал «что сделано», правил было ~90 строк. Старый файл сохранён как неизменяемый архив AGENTS_HISTORY_2026-09-12.md, рядом — WORKFLOW.md (методология v1: пакет доказательств до запуска, протокол отказов модели) и шаблон задачи. Отсюда же выросли карточки исследований с замороженным планом и не больше трёх раундов на механизм, и отдельные ревьюеры только для чтения — потом их было 47 только в петле на телефоне.

Помогло ли с ложными срабатываниями — в самом документе честно: «снижение числа ложных срабатываний этой методологией пока не измерено и не гарантируется».
-->

---
clicks: 3
---

<DemoPhase at="solution" />

<Kicker>решение · слой 1 · дифференциальный оракул</Kicker>

# Код оригинала исполняется рядом с портом

<FlowDiagram stepwise class="mt-4" input="одни и те же входы" :lanes="[
  { title: 'оригинал в эмуляторе процессора', out: 'байты после вызова', color: 'var(--s2)', tag: 'эталон' },
  { title: 'та же функция на Swift', out: 'байты после вызова', color: 'var(--s1)', tag: 'порт' },
]" verdict="совпало побайтно" />

<div class="grid grid-cols-3 gap-3 mt-4 orc">
<div class="card-soft"><b>Канарейки.</b> Вызов засчитан, только если стек и регистры-ловушки целы.</div>
<div class="card-soft"><b>Падение — тоже поведение.</b> Упал оригинал — порт обязан упасть так же.</div>
<div class="card-soft"><b>215 оракулов.</b> Игра грузится, проходит меню и играет такты прямо в эмуляторе.</div>
</div>

<style>
.orc .card-soft { font-size: .8rem; line-height: 1.4; color: var(--ink-2); }
.orc b { color: var(--ink); }
.orc code { font-size: .58rem !important; }
</style>

<!--
Что было на слайде раньше: эталон — Unicorn исполняет машинный код exe, вызовы Windows подменены заглушками; на выходе байты после вызова плюс маска записей, вызовы ГСЧ, события ресурсов. Порт — та же функция на Swift со своими аллокациями и откатом. «Совпало» — только там, где байт определён маской. Канарейки: регистры 0x11223344…, куча 0xA5; вызов засчитан, только если EIP дошёл до STOP, а стек и канарейки целы. Падение оригинала — исход sourceFault, а не «совпало»: порт обязан упасть так же или объявить границу. 215 скриптов-оракулов; VM создают 17, остальные наследуют её цепочкой.

≈ 60 секунд. Это механизм, на котором держится всё доверие первых трёх недель.

Unicorn — эмулятор процессора (ядро QEMU как библиотека). Агент грузит в него секции настоящего EXE по их адресам, импорты Windows подменяет страницей-заглушкой: Python-обработчик снимает аргументы со стека и отвечает. Одни и те же входы подаются в функцию оригинала и в её Swift-порт, байты после вызова сравниваются по маске — только те, что функция реально записала.

Подвох, который агент нашёл сам: memory-хуки Unicorn увидели 259 526 из 524 454 байт, записанных инструкцией REP MOVSD, — маски теперь берутся из самих инструкций копирования.

Клики: входы → две программы → выходы → вердикт.
-->

---

<DemoPhase at="solution" />

<Kicker>решение · разметка exe · 2–3 октября</Kicker>

# Сколько exe на самом деле проверено

<div class="grid grid-cols-[1.55fr_1fr] gap-7 mt-2 items-center">
<div>
<ExeTreemap />
</div>
<div>

<Meter :value="0.924" label="сверено с оригиналом" sub="157 из 174 функций игрового кода" />
<Meter :value="0.514" label="выполнено в прогонах эмулятора" sub="остальное в прогоны не попало" />

<div class="aud mt-4"><span class="i-pixelarticons-warning-box" />на следующий день другой агент проверил метрику: засчитала лишнее, за готовность её не выдавать</div>

</div>
</div>

<style>
.aud { display: flex; align-items: center; gap: .5rem; font-size: .8rem; line-height: 1.35; color: var(--ink); }
.aud span { flex: none; width: 1.3rem; height: 1.3rem; color: var(--naruto); }
.audit { font-size: 0.72rem; line-height: 1.42; color: var(--ink-2); padding: 0.6rem 0.8rem; }
.audit b { color: var(--ink); }
.audit-ico { width: 1.1rem; height: 1.1rem; color: var(--naruto); flex: none; }
</style>

<!--
Что было на слайде раньше: подпись к карте — каждый прямоугольник — функция игрового кода, площадь — число инструкций. 92,4 % кода — в функциях, сверенных с оригиналом (157 из 174: есть прогон оригинала или набор сравнённых входов); 51,4 % кода оригинала выполнилось в сохранённых прогонах эмулятора; 97,8 % описано в исследованиях или перенесено (160 функций). Аудит на следующий день, другой агент: метрика засчитала лишнее и пропустила часть кода (например, обработчик окна) — процент готовности по ней объявлять нельзя; новый так и не объявили.

≈ 45 секунд. Слайд из полной деки (глава 8), формулировки упрощены.

Карта — 174 функции игрового кода оригинального exe, площадь прямоугольника — число инструкций. Синие — есть записи исполнения или сравнённый корпус входов (157 функций), зелёные — перенесены и исполняются внутри уже сравнённых вызывающих (6), оранжевые — режимы разработчика и функции без установленной достижимости (11).

Справа три меры: 92,4 % инструкций — в функциях с записями или корпусом (157 из 174, 63 694 инструкции); 51,4 % инструкций реально исполнено в записях, 47,0 % — в фикстурах, которые сравнивают тесты; 97,8 % процитировано в карточках или в порте (160 функций).

Аудит на следующий день — другой агент: метрика засчитала 293 адреса из статического файла, не нашла WndProc 0x43b3d0, переданный через push, и пропустила 2 529 входов в блоки. Вывод: 47 % — ни процент реализованного кода, ни проверенная нижняя граница, интервал 51–92 % тоже не обоснован; новый процент готовности не объявлен. Это ещё один пример из темы доверия: метрику агента проверил другой агент и не дал выдать её за готовность.

Источники: 6fcf8b9 · f9ee219 · docs/research/EXE_COVERAGE_2026-10-02.md · EXE_COVERAGE_AUDIT_2026-10-03.md.
-->

---

<DemoPhase at="solution" />

<Kicker>решение · 7–27 сентября вслепую — 28 сентября вся игра</Kicker>

# Три недели без картинки — и игра за день

<BlindMonth class="mt-1" />

<div class="grid grid-cols-[1fr_1.4fr] gap-4 mt-1">
<div class="grid grid-cols-2 gap-2">
<StatTile value="801 → 801" label="строк в приложении" sub="21 день подряд" size="sm" accent="var(--s2)" />
<StatTile value="5 ч 44 мин" label="28 сен: до матча с KO" sub="от первого коммита Claude" size="sm" accent="var(--good)" />
</div>
<div class="card-soft bm"><b>Агент, 8 сентября:</b> «Не ускоряем видимый прогресс… тренировочное окно некоторое время может выглядеть прежним».</div>
</div>

<style>
.bm { font-size: .7rem; line-height: 1.42; color: var(--ink-2); }
.bm b { color: var(--ink); }
</style>

<!--
Что было на слайде раньше: 801 → 801 строк в слое приложения 21 день подряд; 28 сентября от первого коммита Claude до матча с KO — 5 ч 44 мин. Решение агента 8 сентября: «Не ускоряем видимый прогресс добавлением персонажей и техник на неполной основе… тренировочное окно некоторое время может выглядеть прежним».

≈ 50 секунд. Здесь — суть доверия: 55 % всех токенов проекта ушло до первого матча в приложении. Снаружи это выглядело как сжигание денег: в окне — тренировочная сцена 7 сентября. Внутри росли ядро, оракулы и эталоны.

28 сентября Claude получил проект в 13:31: в 15:50 — матч Наруто против Саске в приложении, в 18:15 — первый KO, в 19:15 — повтор и Summary, к полуночи — 30 тиков в секунду. Это не скорость Claude: 39 300 строк, 81 % итогового кода, уже были написаны и сверены; в тот же день сменились и агент, и правила прогресса, их вклад по отдельности не измерен.

Автор после релиза: «Методология валидации — это всё. Это самое важное. Это ровно то, что в самом конце привело нас к полному паритету в интеграционных тестах».

Аудиторы Codex несколько раз писали: «прироста подтверждённых игровых возможностей нет». 12 сентября готовый чужой движок L2DF дал работающее приложение за 16 минут — и автор его остановил: «ок, остановил. продолжаем на main».
-->

---

<DemoPhase at="solution" />

<Kicker>решение · перенос на другие платформы · 3–19 октября</Kicker>

# Платформы — за часы, телефон — за неделю

<DemoPorting class="mt-1" />

<div class="wz mt-2">
<span class="wh">WebAssembly против натива<i>мс на тик</i></span>
<div class="wb"><span class="n">Mac</span><b style="width: 38%" class="mac" /><span class="v">1,91</span></div>
<div class="wb"><span class="n">Chromium</span><b style="width: 44.8%" /><span class="v">2,24 · ×1,17</span></div>
<div class="wb"><span class="n">WebKit — движок Safari</span><b style="width: 65.4%" /><span class="v">3,27 · ×1,71</span></div>
<span class="wn">даже WebKit в 5 раз быстрее кадра на 60 fps</span>
</div>

<style>
.wz { display: grid; grid-template-columns: 11.5rem repeat(3, 1fr) 12rem; gap: .9rem; align-items: center; background: rgba(255,255,255,.03); border: 1px solid var(--hair); border-radius: 12px; padding: .35rem .8rem; }
.wz .wh { font-family: var(--font-pixel); font-size: .64rem; color: var(--naruto); text-transform: uppercase; letter-spacing: .05em; line-height: 1.3; }
.wz .wh i { display: block; font-family: var(--font-sans); font-style: normal; text-transform: none; letter-spacing: 0; font-size: .6rem; color: var(--muted); margin-top: .1rem; }
.wb { display: flex; flex-direction: column; gap: .15rem; }
.wb .n { font-size: .66rem; color: var(--ink-2); }
.wb b { display: block; height: .55rem; border-radius: 3px; background: var(--s1); }
.wb b.mac { background: var(--ink-2); }
.wb .v { font-family: var(--font-mono); font-size: .64rem; color: var(--ink); }
.wz .wn { font-size: .66rem; line-height: 1.35; color: var(--ink-2); }
</style>

<!--
≈ 60 секунд. После релиза для Mac 3 октября агент переносил игру на другие платформы. Полосы — от первого до последнего коммита каждой работы, время местное.

Простая часть — сами платформы: Linux, Windows, iPad и Android встали за 30 часов (3 октября 20:11 → 5 октября 02:01), девять «хостов» дали одно состояние, 90 из 90 сценариев. Подводные камни здесь — мелкие: компилятор Swift для Linux выбрасывал запись в слот перед проверкой уникальности ссылки (поймал прогон всей матрицы; отчёт swiftlang/swift#92905 закрыт исправлением); на iPad тап приходил как нажатие и отпускание в один момент, а оригинал смотрит на кнопку несколько тиков; Android от первого запуска до текста, звука и музыки — 22 минуты.

Сложная часть — настоящее железо. Galaxy A12 убил игру на загрузке: ей нужно было 4 ГБ, у телефона 2,8. Дальше шесть с половиной дней: память матча 4 → 1,5 ГБ, скорость 5,4 тика в секунду → 60 кадров в секунду, от иконки до меню 131,9 → 12,7 с.

Скорость WebAssembly против натива (внизу слайда): автор спросил «хромиум wasm быстрее чем нативная mac версия?», агент ответил «Нет, нативная Mac-версия быстрее» и признал, что его первая таблица сравнивала разное. Честное сравнение — тот же бинарник Mac с отрисовкой в игровом потоке (--synchronous-render), как в браузере: 1,91 мс на тик против 2,24 в Chromium (×1,17) и 3,27 в WebKit (×1,71); Node WASI — 3,67 (×1,92). Медианы трёх прогонов, сценарий VS, один хост за раз на этом Mac, 12 октября. Дорого не исполнение, а старт: от запуска до загрузки 5,6 с в Chromium против 0,63 с на Mac; линейная память модуля — 1 617 МиБ.

Браузер — свои особенности. Игра — это Swift, собранный в WebAssembly; данные игры — 1 521 файл. Сначала первый визит качал 881,5 МБ — сжатие довело до 99,5 МБ. Но на живом сайте каждый файл — отдельный запрос к CDN с задержкой 0,2–0,35 с, и данные шли 46,5 с при любом интернете. Решение 17 октября: файлы упакованы в 12 сжатых пачек в порядке, в котором игра их читает, и сохраняются в приватном хранилище браузера (OPFS) — 46,5 → 4,6 с, повторный визит не качает ничего.

Кнопки на экране — 19 октября, по предложению игрока StormPixels из Discord: у оригинала всегда была клавиатура, поэтому экранные кнопки просто жмут её клавиши; в его версии кнопки жали клавиши второго игрока — агент заметил это в симуляторе, когда меню не реагировало на «атаку». Показываются только без клавиатуры и геймпада. Начало этой работы шло на другом Mac, поэтому на графике — точка по времени коммита, без длительности.

iPhone — экран 874×402 точки меньше окна игры 794×550: хост сообщает игре экран не меньше 800×600 и вписывает картинку. Steam Deck — Linux-сборка как есть, но меню оригинала понимает только мышь: геймпад ведёт мышь игры к ближайшей кнопке.
-->

---

<DemoPhase at="demo" />

<Kicker>демо · режим Demo, одна и та же партия</Kicker>

<DemoHandoff class="mt-1" />

<style>
.hand { text-align: center; font-size: .82rem; color: var(--ink-2); }
</style>

<!--
≈ 40 секунд. Ролик сам играет по кругу, 24 секунды.

Что на экране. Встроенный режим Demo игры: восемь бойцов под управлением компьютера на арене District. Первые 12 секунд — оригинальный NTSD 2.4.exe, Windows-программа 2008 года, запущенная на Mac через CrossOver. На 12-й секунде, прямо посреди боя, картинка переключается на нативное Swift-приложение — и партия продолжается: те же бойцы, те же удары, те же полоски здоровья. Склейки не видно, потому что кадры обеих программ на одном и том же тике совпадают.

Откуда кадры. Это не запись экрана, а кадры из сверки 3 октября (то же, что видео на README порта): оригинал под CrossOver снимал кадр каждые 3 тика с 150-го, приложение на Mac — тоже. Обе программы шли с одной таблицей случайных чисел: в оригинал подставили таблицу Mac (srand(777)), чтобы бои были одинаковыми. Оригинал — тики 150–510, порт — 513–879, 10 кадров в секунду — это собственная скорость игры (30 тиков в секунду, кадр на каждый третий).

Честная деталь: в этом прогоне оригинал разошёлся с Mac между тиками 879 и 882, причина не найдена, поэтому ролик заканчивается на 879-м.

Живая демка после ролика: открыть ntsd-web-ashy.vercel.app — та же игра в браузере.
-->

---

<DemoPhase at="demo" />

<Kicker>демо · одна игра на Swift — на всех платформах</Kicker>

# Ядро почти не тронуто

<CoreWaffle lite class="mt-2" />

<div class="lgc mt-1"><span><i style="background: #4c5466" />ядро без изменений</span><span><i style="background: var(--s2)" />изменено при переезде</span><span><i style="background: var(--s1)" />общий рантайм</span><span><i style="background: var(--s3)" />хост платформы</span><span class="muted">один квадрат — 100 строк</span></div>

<div class="pf mt-3">
<span class="on">macOS</span><span class="on">Linux</span><span class="on">Steam Deck</span><span class="on">Android</span><span class="on">браузер</span><span>Windows</span><span>iPad</span><span>iPhone</span><span>Apple TV</span>
<i class="lg"><b class="on" />на устройстве <b />в симуляторе или эмуляции</i>
</div>

<div class="live mt-3"><span class="pixel hl">живьём</span><code>ntsd-web-ashy.vercel.app</code><span>меню через ≈ 2 с</span></div>

<style>
.lgc { display: flex; flex-wrap: wrap; gap: .2rem 1.1rem; font-size: .66rem; color: var(--ink-2); }
.lgc i { display: inline-block; width: 9px; height: 9px; border-radius: 2px; margin-right: .35rem; vertical-align: -1px; }
.pf { display: flex; flex-wrap: wrap; align-items: center; gap: .4rem; }
.pf span { font-size: .78rem; color: var(--ink-2); border: 1px dashed var(--axis); border-radius: 999px; padding: .12rem .7rem; }
.pf span.on { color: var(--ink); border: 1px solid var(--naruto); background: rgba(255,138,61,.1); }
.pf .lg { font-style: normal; font-size: .62rem; color: var(--muted); margin-left: .6rem; display: inline-flex; align-items: center; gap: .35rem; }
.pf .lg b { display: inline-block; width: 10px; height: 10px; border-radius: 50%; border: 1px dashed var(--axis); margin-left: .4rem; }
.pf .lg b.on { border: 1px solid var(--naruto); background: rgba(255,138,61,.35); }
.pt .card-soft { display: flex; flex-direction: column; gap: .2rem; padding: .55rem .8rem; }
.pt .big { font-family: var(--font-display); font-weight: 700; font-size: 1.15rem; color: var(--naruto); }
.pt .cap { font-size: .74rem; line-height: 1.38; color: var(--ink-2); }
.live { display: flex; align-items: baseline; gap: .8rem; font-size: .8rem; color: var(--ink-2); }
.live .pixel { font-size: .66rem; text-transform: uppercase; letter-spacing: .06em; }
.live code { font-size: .74rem !important; }
</style>

<!--
Что было на слайде раньше: легенда квадратов (ядро без изменений, изменённые строки ядра, общий рантайм, адаптер хоста, Mac-слой на main; один квадрат — 100 строк Swift); подписи модулей NTSDCore и NTSDRuntime; «+223 / −26 в 11 файлах ядра — переносимость, а не поведение». Плашки платформ: залитые — на настоящем устройстве (macOS, Linux, Steam Deck, Android, браузер), контурные — пока в симуляторе или под эмуляцией (Windows через CrossOver, iPad, iPhone, Apple TV). Живая демка: ntsd-web-ashy.vercel.app — меню через ≈ 2 с.

≈ 2–3 минуты вместе с живой демкой.

Квадраты — строки Swift в коде игры на 5 октября, вечер, когда игра шла на девяти «хостах» (один квадрат — 100 строк): ядро — правила, ИИ, режимы, записи; общий рантайм; по тонкому адаптеру на платформу. Оранжевые квадраты в ядре — изменённые при переезде строки: 223 добавлено, 26 удалено в 11 файлах. Самое большое — свой SHA-256 вместо системной библиотеки Apple. Поведение игры не менялось. Пунктирный контур — сколько занимал Mac-слой до переезда: он похудел на 4 504 строки, окно, звук, ввод и сеть ушли в общий рантайм.

Проверка: на девяти хостах — 90 из 90 сценариев с кадрами, равными эталонам Mac. Потом добавились Apple TV, браузер (Swift в WebAssembly, Chromium и WebKit), iPhone — те же 18 088 кадров эталона. Steam Deck запускает Linux-сборку из Game Mode.

Честно о «настоящем железе»: macOS, Android (Galaxy A12, Pixel 10), Steam Deck и браузер — настоящие устройства. Linux, кроме Deck, проверялся в контейнерах; Windows — только под CrossOver, настоящую Windows не пробовали; iPad, iPhone и Apple TV — в симуляторах.

Живая демка: открыть ntsd-web-ashy.vercel.app в браузере с чистым профилем — меню через ~2 секунды. Выбрать VS, Наруто против Саске, сыграть несколько секунд. Если сеть подведёт — показать видео из полной деки: Mac и оригинал рядом в режиме Demo, кадры совпадают тик в тик.
-->

---

<DemoPhase at="demo" />

<Kicker>демо · сетевая игра · 2 и 5 октября</Kicker>

# Одна сетевая партия — четыре системы

<DemoOnline class="mt-1" />

<div class="nf grid grid-cols-3 gap-5 mt-2">
<div class="it"><span class="pixel hl">как это работает</span>по сети ходят только нажатия — все копии обязаны совпадать бит в бит</div>
<div class="it"><span class="pixel hl">целый матч</span>два приложения на Mac: <b>1 070 тиков</b>, мир совпадал на каждом</div>
<div class="it"><span class="pixel hl">между системами</span>все пары получили <b>одну и ту же</b> таблицу случайных чисел</div>
</div>

<div class="hon2 mt-3">пока всё — на одном Mac: CrossOver, эмулятор, контейнер</div>

<style>
.nf .it { font-size: .72rem; line-height: 1.42; color: var(--ink-2); }
.nf .it .pixel { display: block; font-size: .62rem; text-transform: uppercase; letter-spacing: .06em; margin-bottom: .15rem; }
.nf b { color: var(--ink); }
.hon2 { font-size: .8rem; color: var(--muted); text-align: center; }
.hon { font-size: .74rem; line-height: 1.4; color: var(--ink-2); border-left: 3px solid var(--warning); padding: .3rem .8rem; background: rgba(250,178,25,.06); border-radius: 0 10px 10px 0; }
</style>

<!--
Что было на слайде раньше. Как это работает: по сети ходят только нажатия кнопок, остальное каждая копия игры считает сама — поэтому все копии обязаны совпадать бит в бит. Целый матч: два приложения на Mac сыграли бой Наруто против Саске — 1 070 тиков, 836 пакетов в каждую сторону, мир игры у обеих сторон совпадал на каждом тике. Между системами: каждая пара прошла меню сетевой игры оригинала и получила одну и ту же таблицу случайных чисел. Оговорка: всё на одном Mac — Windows через CrossOver, Android в эмуляторе, Linux в контейнере; двух устройств в настоящей сети и партии с оригинальной игрой ещё не было.

≈ 45 секунд. Продолжение истории про платформы и тот самый «бонус» со второго слайда.

Как работает сеть оригинала: протокол без изменений — TCP-порт 12345, хост отдаёт клиенту таблицу случайных чисел на 3 001 байт, дальше 22 байта на тик — только ввод. Каждая сторона пересчитывает матч сама (lockstep), поэтому любое расхождение в физике или случайных числах разваливает партию.

Целый матч (2 октября, network-app-match-20261002): два процесса нативного приложения на Mac, 1 672 итерации цикла, 1 070 игровых тиков, 836 пакетов в каждую сторону; все байты мира и маски совпадали на каждой итерации, записи повторов у обеих сторон восстановлены из реальных байтов в сети. Различались только координаты искр — косметика, которую оригинал считает по-своему в каждом процессе. Итог: Наруто победил, 00:34.

Между системами (5 октября, crossplatform-online-cross-20261005): 7 запусков «хост → клиент» — стрелки на схеме, — Mac↔Android, Mac↔Windows, Windows→Android, Mac↔Linux. Каждый: оба процесса прошли меню ONLINE GAME, оба дошли до состояния «сеть готова», роли, места и имена — как в эталонном прогоне, и таблица случайных чисел одинакова во всех семи (SHA-256 5352f941…). До конца матча эти пары не играли — проба останавливается, когда сеть готова.

Честно: всё на одном Mac. Windows — бутылка CrossOver с настоящим Winsock, Android — эмулятор, связь через adb, Linux — контейнер OrbStack. Одна загадка оказалась артефактом стенда: Linux-клиент в контейнере звонил сам себе на 127.0.0.1. Двух настоящих устройств в сети и партии против оригинального exe ещё не было.
-->

---

<DemoPhase at="results" />

<Kicker>результаты</Kicker>

# Что получилось

<DemoResults class="mt-2" />

<div class="cost mt-4"><span><b>37</b> дней</span><span><b>756</b> коммитов</span><span><b>2</b> подписки по $200</span></div>

<style>
.cost { display: flex; gap: 2rem; align-items: baseline; font-size: .8rem; color: var(--ink-2); border-top: 1px solid var(--axis); padding-top: .55rem; }
.cost b { font-family: var(--font-display); font-size: 1.25rem; color: var(--ink); margin-right: .3rem; }
</style>

<!--
≈ 60 секунд.

Слева — один и тот же матч в двух программах: таблицу итогов записал порт на Mac, справа эту запись проигрывает оригинальная игра. 58 из 58 = 42 случайных матча Mac → оригинал (VS 32, Stage 6, War 4) + 5 матчей оригинал → Mac + 11 ранних повторов; все равны. 18 088 кадров — эталонные прогоны десяти сценариев; на каждой новой платформе кадры сравнивались с теми же замороженными эталонами Mac — равны.

Справа — Galaxy A12, «было» и «стало»:
- Скорость: первый доигранный матч 5 октября шёл 5,4 тика в секунду при нужных 30 — игра в замедленной съёмке. После перестройки ядра игра идёт в темпе оригинала (30,25 тика/с с настоящими часами), а главный поток тратит 11,1 мс на тик — это запас на 60 кадров в секунду.
- Память: сначала игре требовалось около 4 ГБ — больше, чем 2,8 ГБ в телефоне, и игра падала на загрузке. Пик после ночи загрузки — 565 МиБ.
- Загрузка: от иконки до меню 131,9 → 12,7 с в типичном прогоне.

Внизу — цена: 37 дней с 7 сентября по 13 октября, 756 коммитов, подписки ChatGPT Pro и Claude Max по $200 в месяц. По номиналу Codex съел ≈ $266 на порт; работа Claude за первые 6 дней по ценам API стоила бы ≈ $797.
-->

---

<DemoPhase at="results" />

<Kicker>результаты · петля на настоящем телефоне · 7–10 октября</Kicker>

# Замер → правка → проверки → решение

<DemoLoop class="mt-1" />

<div class="rule-l mt-3"><span class="pixel hl">правило агента</span><span>быстрее — коммит, иначе откат</span></div>

<style>
.rule-l { display: flex; align-items: baseline; gap: 1rem; font-size: .86rem; line-height: 1.4; color: var(--ink); background: rgba(255,138,61,.08); border: 1px solid rgba(255,138,61,.45); border-radius: 12px; padding: .5rem .9rem; }
.rule-l .pixel { font-size: .66rem; text-transform: uppercase; letter-spacing: .06em; white-space: nowrap; }
</style>

<!--
≈ 75 секунд.

Слева — что происходит за один оборот. Автор запустил /loop одной фразой («start the core redesign loop») и задал цели 33 / 16 / 8 мс; дальше агент сам: замер на настоящем Galaxy A12 (бюджетный телефон 2020 года, 2,8 ГБ памяти), одна правка, проверки — 10 сценариев с кадрами, равными эталону, приложение на Mac, эмулятор, отдельный ревьюер только для чтения, — и решение. За 3 дня — 75 оборотов: 37 быстрее, 19 «строго меньше работы», 2 отката, 6 отложено, остальное — доработки после ревью, тесты и сборки. 480 прогонов на телефоне, ≈ 31 час матчей, 47 независимых ревью.

Справа — работа главного потока на один тик после каждого оборота (сценарий vs, среднее 2–4 прогонов): 24,6 мс в начале петли 7 октября → 11,1 мс 10 октября. Зелёная пунктирная линия — 16,7 мс, бюджет кадра при 60 кадрах в секунду; её пересекли 8 октября (тег rt-60fps-a12). Красные кольца — замер был, но шаг откатили или отложили. Телефон «плывёт» между сессиями, поэтому прежнюю сборку гоняли вперемешку с новой в той же сессии; разрешение — около ±0,25 мс на прогон.

Правило коммита — дословно: «Commit an increment only when every gate passes and it is either measurably faster or strictly less work without added complexity; otherwise record the result here and revert». Агент записал его 6 октября в 03:48 — через две минуты после реплики автора, где этого правила нет.

Если спросят про хитрости:
1. Запись состояния тика — одним буфером (S2b): копирование массивов в профиле главного потока 9,40 → 4,96 %. По дороге прогон тестов встал на два часа: проверки, читавшие целые массивы в цикле, стали квадратичными.
2. Пиксели — в свой поток: рендер отделён от логики тика, вывод на экран Android — ещё в отдельный поток.
3. Динамические проверки эксклюзивности Swift стоили 3,5–4 % главного потока; снять их в релизе решил автор — агент спросил и девять часов ждал ответа.

До петли, 5 октября, первый доигранный матч на телефоне шёл 5,4 тика в секунду (≈ 185 мс на тик на часах харнесса, включая сон самой игры) — это другая мера, на график её не ставим.
-->

---

<DemoPhase at="results" />

<Kicker>результаты · где остановиться · 10 октября</Kicker>

# Петля остановилась сама

<div class="grid grid-cols-[1.25fr_1fr] gap-8 mt-3 items-center">
<div>
<div class="wh-h">шесть оставшихся идей — сколько сэкономила бы каждая, мс на тик</div>
<DemoWall />
<div class="wh-c">все шесть — внутри шума замера, по правилу коммитить нельзя</div>
</div>
<div>
<PhoneChat :messages="[
  { who: 'agent', time: '18:27', text: 'всё, что осталось, — ниже разрешения телефона' },
  { who: 'human', time: '21:23', text: 'you did good. we reached the wall', hot: true },
]" />
<div class="fc mt-3">
<div><span class="pixel">прогноз · 8 окт</span><b>≈ 11 мс</b></div>
<div><span class="pixel">факт · 10 окт</span><b>11,09 мс</b></div>
</div>
</div>
</div>

<style>
.wh-h { font-size: .74rem; color: var(--ink-2); margin-bottom: .3rem; }
.wh-c { font-size: .86rem; line-height: 1.42; color: var(--ink); margin-top: .5rem; }
.fc { display: grid; grid-template-columns: 1fr 1fr; gap: .6rem; }
.fc div { display: flex; flex-direction: column; gap: .15rem; background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: .55rem .7rem; }
.fc .pixel { font-size: .6rem; color: var(--naruto); text-transform: uppercase; letter-spacing: .06em; }
.fc b { font-family: var(--font-display); font-size: 1.5rem; color: var(--ink); }
.fc i { font-style: normal; font-size: .64rem; line-height: 1.35; color: var(--ink-2); }
</style>

<!--
Что было на слайде раньше: шесть оставшихся идей и сколько каждая сэкономила бы (мс на тик); все шесть меньше погрешности замера и добавили бы второй путь в коде — по правилу коммитить нельзя. Диалог: агент в 18:27 (последний коммит петли 0034e45c, пересказ) — «всё, что осталось, ниже разрешения телефона; дальше нужны ответы автора на четыре вопроса»; автор в 21:23 — «you did good. we reached the wall. performance is now close to optimal». Прогноз ≈ 11 мс написал отдельный агент-планировщик за 44 часа до конца; факт — 11,09 мс.

≈ 60 секунд. Ответ на вопрос «где плато и сколько токенов тратить». Здесь его дал не человек: правило коммита запрещает шаги, выигрыш которых меньше разрешения замера (около ±0,25 мс на прогон) или которые добавляют второй путь кода. Слева — шесть идей, которые не требовали решений автора, с оценками самого плана: от 0,04 до 0,15 мс. Все внутри серой полосы шума.

Последний коммит петли (0034e45c), дословно: «Every remaining decision-free item is below the phone's resolution and would add a second code path, so none meets the commit rule; the copies left are the transactional ones. The input needed is the user's answers to Q1-Q4 (TIER3).» Четыре вопроса — о том, что можно менять в поведении игры после внутреннего сбоя; с ответами план обещал ≈ 9–10 мс. Автор на них не ответил и перевёл агента на память и загрузку: «you did good. we reached the wall. performance is now close to optimal. now lets do the loop for optimizing memory footprint and loading times».

Прогноз: план яруса 3 писал отдельный агент только для чтения вечером 8 октября, когда главный поток был на 16,25 мс: «без решений — около 11 мс на главном потоке и около 8 на рендере». Через 44 часа последний замер дал 11,09 и 7,55. Путь был другим, а стена оказалась там, где её нарисовали.
-->

---

<DemoPhase at="lessons" />

<Kicker>вывод · моя позиция</Kicker>

# LLM — компилятор намерений в машинный код

<div class="cmp mt-4">
<div class="st in">
<span class="pixel">исходник</span>
<b>намерение</b>
<i>«та самая игра, как я её помню» — и чем это проверить</i>
<em>≈ 240 моих сообщений</em>
</div>
<span class="ar">→</span>
<div class="st cc">
<span class="pixel">компилятор</span>
<b>LLM + харнесс</b>
<i>оракул, петлю и правило остановки агент собрал сам</i>
<em>больше 10 млрд токенов</em>
</div>
<span class="ar">→</span>
<div class="st out">
<span class="pixel">машинный код</span>
<b>игра на 9 платформах</b>
<i>код, который никто не обязан читать</i>
<em>58 тыс. строк Swift</em>
</div>
</div>

<div class="tests mt-3"><span class="pixel">тесты</span><span>сам оригинал: <b>58 из 58</b> матчей, <b>18 088</b> одинаковых кадров</span></div>

<div class="mine mt-4">
<div class="mh pixel">что остаётся человеку</div>
<div class="mr">
<div><span class="n">1</span>сформулировать задачу и чем её проверить</div>
<div><span class="n">2</span>дать достаточно токенов</div>
<div><span class="n">3</span>решать на развилках</div>
</div>
</div>

<style>
.cmp { display: grid; grid-template-columns: 1fr auto 1.15fr auto 1fr; gap: .7rem; align-items: stretch; }
.cmp .st { display: flex; flex-direction: column; gap: .25rem; background: var(--surface); border: 1px solid var(--hair); border-radius: 14px; padding: .75rem .9rem; }
.cmp .st.cc { border-color: rgba(255,138,61,.6); background: rgba(255,138,61,.07); }
.cmp .pixel { font-size: .62rem; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; }
.cmp .cc .pixel { color: var(--naruto); }
.cmp b { font-family: var(--font-display); font-size: 1.15rem; color: var(--ink); line-height: 1.15; }
.cmp i { font-style: normal; font-size: .74rem; line-height: 1.38; color: var(--ink-2); flex: 1; }
.cmp em { font-style: normal; font-family: var(--font-mono); font-size: .62rem; color: var(--muted); }
.cmp .ar { align-self: center; font-family: var(--font-display); font-size: 1.6rem; color: var(--naruto); }
.tests { display: flex; align-items: baseline; gap: 1rem; font-size: .8rem; color: var(--ink-2); border: 1px dashed var(--axis); border-radius: 12px; padding: .45rem .9rem; }
.tests .pixel { font-size: .62rem; color: var(--good); text-transform: uppercase; letter-spacing: .06em; white-space: nowrap; }
.tests b { color: var(--ink); }
.mine .mh { font-size: .66rem; color: var(--chakra); text-transform: uppercase; letter-spacing: .06em; margin-bottom: .45rem; }
.mine .mr { display: grid; grid-template-columns: repeat(3, 1fr); gap: .8rem; }
.mine .mr div { display: flex; gap: .6rem; align-items: baseline; font-size: .86rem; line-height: 1.38; color: var(--ink); }
.mine .n { font-family: var(--font-display); font-weight: 700; font-size: 1.5rem; color: var(--chakra); line-height: 1; }
</style>

<!--
Что было на слайде раньше: исходник — «та самая игра, как я её помню» и чем проверить, что это она; компилятор — Codex и Claude, оракул, петлю и правило остановки агент собрал сам, 756 коммитов; выход — 58 тыс. строк Swift, читать которые никто не обязан, macOS · Linux · Windows · Android · iOS · браузер; тесты компилятора — 58 из 58 матчей, 18 088 кадров одинаковы на всех платформах. Что остаётся человеку: 1) сформулировать задачу — что значит «правильно» и чем это проверить; 2) дать достаточно токенов; 3) решать на развилках, куда агенту не положено.

≈ 75 секунд. Это вывод автора — позиция, а не замер; на слайде так и подписано.

Аналогия. Компилятор берёт исходник и выдаёт машинный код; его вывод никто не читает построчно — ему доверяют, потому что есть тесты. Здесь исходник — намерение: «та самая игра, как я её помню» плюс то, чем это проверить. Компилятор — LLM вместе с харнессом, который агент построил сам: оракул на коде оригинала, петля замеров на телефоне, правило коммита и остановки. Выход — 58 146 строк Swift (на 13 октября) и нативная игра на девяти платформах. Тесты компилятора — сам оригинал: 58 из 58 целых матчей совпали, 18 088 кадров одинаковы на всех платформах.

Цифры. ≈ 240 сообщений человека — сумма по основным сессиям: 163 у Codex (7–27 сентября), 25 и 56 у Claude (28 сентября — 3 октября и 3–13 октября). Токены: 6,3 млрд до релиза 3 октября плюс 4,6 млрд, прочитанных одной сессией Claude 3–13 октября, — больше 10 млрд. 756 коммитов с 7 сентября по 13 октября.

Что остаётся человеку — три пункта, и все три видны в истории:
1. Сформулировать задачу. Тут больше работы, чем кажется: «так же, а не похоже», исходная игра как единственный эталон, правила прогресса после 19 коммитов мимо приложения, методология ReAgent с отдельным ревьюером, вопрос «у нас же есть windows через crossover?».
2. Дать токенов. Три недели без видимой картинки — 3,4 млрд токенов; без этого не было бы дня, когда игра собралась целиком.
3. Решать на развилках: снять проверки эксклюзивности Swift (агент ждал ответа девять часов), остановить чужой движок L2DF, остановиться у «стены» и переключить петлю на память и загрузку.

Если спросят про слабые места аналогии: компилятор детерминирован, а LLM — нет; поэтому и нужен харнесс — он превращает недетерминированную генерацию в проверенный результат. И «тесты» здесь были роскошью: эталон — сам оригинал, бит в бит. Для задач без такого эталона формулировка «чем проверить» — самая трудная часть.
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
<p class="small ink" style="max-width: 40rem; margin-top: -0.3rem">Механизмы агент строит сам. Цель, рамка и развилки — ваши.</p>
<p class="small ink2" style="max-width: 40rem">порт: <span class="mono">github.com/wowlocal/ntsd-2.4</span></p>
</div>

<style>
.cover-title { font-size: 2.6rem !important; line-height: 1.1 !important; margin: 0.3rem 0 0.8rem !important; text-align: center; }
</style>

<!--
Финальная мысль — одной фразой: доверять агенту можно настолько, насколько независимы слои, которые проверяют его работу. Механизмы он строит сам; цель и развилки — ваши.
-->

---

<Kicker>лента X и YouTube · 30 сентября — 3 октября 2026</Kicker>

# Не я один

<div class="trend grid grid-cols-3 gap-3 mt-2">
<figure><img src="/img/trend/cydonix-skyrim-tarkov-spiderman.jpg" alt=""><figcaption><b>Skyrim × Tarkov × Spider-Man</b> · «за несколько часов»</figcaption></figure>
<figure><img src="/img/trend/tobynjacobs-elden-ring-mac.jpg" alt=""><figcaption><b>Minecraft в Elden Ring на Mac</b> · 20,7 млн просмотров</figcaption></figure>
<figure><img src="/img/trend/chasm-wow-bevy.jpg" alt=""><figcaption><b>WoW 1.12.1 на Rust</b> · benilla, 3 месяца с Claude</figcaption></figure>
<figure><img src="/img/trend/smallzero-cs16.jpg" alt=""><figcaption><b>CS 1.6 в браузере</b> · 16 игроков</figcaption></figure>
<figure class="col-span-2 wide"><img src="/img/trend/chasm-videos.jpg" alt=""><figcaption><b>MW2 × Skate 3 × Minecraft</b> · «basically 100% vibe coded»</figcaption></figure>
</div>

<style>
.trend figure { margin: 0; background: var(--surface); border: 1px solid var(--hair); border-radius: 10px; overflow: hidden; }
.trend img { display: block; width: 100%; height: 136px; object-fit: cover; object-position: top; }
.trend .wide img { height: 136px; object-fit: contain; background: #0f0f0f; }
.trend figcaption { font-size: 0.6rem; color: var(--ink-2); padding: 0.3rem 0.55rem 0.35rem; line-height: 1.3; }
.trend figcaption b { color: var(--ink); font-weight: 600; }
</style>

<!--
Последний слайд, после «спасибо» — можно оставить на экране на время вопросов. Слайд из полной деки (глава 12), без изменений.

Пока шёл порт, лента автора 30 сентября — 3 октября заполнилась такими же историями: старые игры, переписанные или смешанные с помощью ИИ. Skyrim × Tarkov × Spider-Man (по Kotaku — «за несколько часов»), Minecraft в Elden Ring на Mac (20,7 млн просмотров, открытый клон через два дня), World of Warcraft 1.12.1 на Bevy/Rust — проект benilla, 553 из 559 коммитов с Claude, три месяца; CS 1.6 в браузере на 16 игроков; мэшапы chasm поверх трёх Rust-переписок.

Мысль для финала: переписывание старых игр с ИИ — уже тренд. Разница в том, чем проверяют результат: у benilla в методе те же правила — «The reference client is the spec», «Measure, never eyeball».

Источники: скриншоты ленты автора 3 октября 2026; Kotaku, MakeUseOf, heldgames.com, Community Note; data/evidence/ai-game-rewrites-2026.json.
-->
