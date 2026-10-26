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
<div class="it"><span class="d mono">7 сен</span><span><b>оракул в эмуляторе процессора</b> — уже в первом коммите: ходьба совпала на 8 506 тиках кода оригинала</span></div>
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
  { title: 'Код оригинала в эмуляторе процессора', sub: 'Unicorn исполняет машинный код exe; вызовы Windows подменены заглушками', out: 'байты после вызова + маска записей, вызовы ГСЧ, события ресурсов', color: 'var(--s2)', tag: 'эталон' },
  { title: 'Swift-порт той же функции', sub: 'свои аллокации, свой откат', out: 'байты после вызова, вызовы ГСЧ, события', color: 'var(--s1)', tag: 'порт' },
]" verdict="совпало побайтно" verdict-sub="только там, где байт определён маской" />

<div class="grid grid-cols-3 gap-3 mt-2 orc">
<div class="card-soft"><b>Канарейки.</b> Регистры заполнены <code>0x11223344…</code>, куча — <code>0xA5</code>. Вызов засчитан, только если EIP дошёл до STOP, а стек и канарейки целы.</div>
<div class="card-soft"><b>Падение — тоже поведение.</b> Если оригинал упал, это исход <code>sourceFault</code>, а не «совпало». Порт обязан упасть так же — или объявить границу.</div>
<div class="card-soft"><b>Масштаб.</b> 215 скриптов-оракулов; VM создают 17, остальные наследуют её цепочкой: игра грузится, проходит меню и играет такты в одной VM.</div>
</div>


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

<Kicker>решение · слой 2 · петля на настоящем телефоне · 7–10 октября</Kicker>

# Замер → правка → проверки → решение

<DemoLoop class="mt-1" />

<div class="rule-l mt-3"><span class="pixel hl">правило агента</span><span>коммит — только если стало быстрее или строго меньше работы без усложнения; иначе откат и запись в журнал</span></div>

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

<DemoPhase at="solution" />

<Kicker>решение · где остановиться · 10 октября</Kicker>

# Петля остановилась сама

<div class="grid grid-cols-[1.15fr_1fr] gap-7 mt-2 items-center">
<div>

<div class="wh-h">шесть оставшихся идей — сколько каждая сэкономила бы, мс на тик</div>

<DemoWall />

<div class="wh-c">Все шесть — меньше погрешности замера, и каждая добавила бы второй путь в коде. По правилу коммитить нельзя.</div>

</div>
<div class="wr">

<PhoneChat :messages="[
  { who: 'agent', time: '18:27', text: 'всё, что осталось, — ниже разрешения телефона; дальше нужны ответы автора на четыре вопроса', gloss: 'последний коммит петли, 0034e45c — пересказ' },
  { who: 'human', time: '21:23', text: 'you did good. we reached the wall. performance is now close to optimal', gloss: 'хорошая работа, это стена — производительность близка к оптимальной', hot: true },
]" />

<div class="fc mt-3">
<div><span class="pixel">прогноз · 8 окт</span><b>≈ 11 мс</b><i>написал отдельный агент-планировщик за 44 часа до конца</i></div>
<div><span class="pixel">факт · 10 окт</span><b>11,09 мс</b><i>последний замер петли</i></div>
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
≈ 60 секунд. Ответ на вопрос «где плато и сколько токенов тратить». Здесь его дал не человек: правило коммита запрещает шаги, выигрыш которых меньше разрешения замера (около ±0,25 мс на прогон) или которые добавляют второй путь кода. Слева — шесть идей, которые не требовали решений автора, с оценками самого плана: от 0,04 до 0,15 мс. Все внутри серой полосы шума.

Последний коммит петли (0034e45c), дословно: «Every remaining decision-free item is below the phone's resolution and would add a second code path, so none meets the commit rule; the copies left are the transactional ones. The input needed is the user's answers to Q1-Q4 (TIER3).» Четыре вопроса — о том, что можно менять в поведении игры после внутреннего сбоя; с ответами план обещал ≈ 9–10 мс. Автор на них не ответил и перевёл агента на память и загрузку: «you did good. we reached the wall. performance is now close to optimal. now lets do the loop for optimizing memory footprint and loading times».

Прогноз: план яруса 3 писал отдельный агент только для чтения вечером 8 октября, когда главный поток был на 16,25 мс: «без решений — около 11 мс на главном потоке и около 8 на рендере». Через 44 часа последний замер дал 11,09 и 7,55. Путь был другим, а стена оказалась там, где её нарисовали.
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
