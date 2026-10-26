---
layout: chapter
num: 5
total: 20
kicker: Глава пятая
dates: 22–27 сентября
image: /img/menu-back-green-blue.jpg
stats: 96 коммитов · 0 правок в native/Sources · +20 700 строк инструментов
---

# Фабрика доказательств

Каждый шаг доказан, каждый провал сохранён. Но игра в приложении всё ещё не запускается.

---

<Kicker>где шла работа</Kicker>

# Две недели мимо `native/`

<NativeShare />

<div class="grid grid-cols-3 gap-4 mt-2 small ink2">
<div>С 14 по 27 сентября <b class="hl">1 коммит из 115</b> менял код игры в <code>native/Sources</code>. Работа шла в изолированных кандидатах — APFS-клонах на внешнем диске.</div>
<div>За те же дни Python-инструменты выросли <b class="hl">с 57 692 до 78 392 строк</b>: новые <code>*_validation.py</code>, <code>*_correction2.py</code>, <code>*_candidate.py</code>.</div>
<div>28 сентября проверенный кандидат на <b class="hl">2 291 файл</b> перенесли в <code>native/</code> одним коммитом — и график снова стал оранжевым.</div>
</div>

<div class="source">git log --name-only · data/daily.json · 866bf83</div>

---

<Kicker>docs/CONTINUE_GOAL.md · текст для запуска /goal · три редакции</Kicker>

# Разворот на бумаге — 14 сентября

<p class="lead">Задачу автопилота повернули к матчу в приложении за две недели до поворота. Направление появилось 14 сентября, а правило, которое заставило переносить код, — только 27-го.</p>

<div class="trig"><span class="tm">14 сен · 09:42 · 0656992</span>карта разрывов APPLICATION_EQUIVALENCE_FRONTIER: <span lang="en" class="q">«MeleeScene still uses OriginalMelee»</span> <i>→</i> <span lang="en" class="q">«Connect the recovered engine to the actual app»</span></div>

<div class="drafts">
<div class="dr">
<div class="dh"><span class="pixel">13 сен · 23:38</span><code>a2e0230</code></div>
<div class="dk">задачу выбирать по карте</div>
<p class="old">«Следующая карточка — собственный ввод и ближайшая готовая сохранённая active/paused gameplay-ветвь по CURRENT_WORK и карте».</p>
<p class="old">«…переходить к следующей проверяемой игровой или прикладной границе по готовности доказательств».</p>
</div>
<div class="dr now">
<div class="dh"><span class="pixel">14 сен · 10:36</span><code>2bbff56</code></div>
<div class="dk">задачу выбирать по матчу</div>
<p class="add">«…препятствия ближайшей сквозной вехе: сначала полному матчу Наруто и Саске на District в нативном приложении».</p>
<p class="add">«Наличие удобного сохранённого корпуса само по себе не определяет приоритет».</p>
<p class="add">«…подключение восстановленного движка к приложению вести… не откладывая до переноса всего содержимого».</p>
</div>
<div class="dr">
<div class="dh"><span class="pixel">27 сен · 09:47</span><code>007c007</code></div>
<div class="dk">что делать после каждого «совпало»</div>
<p class="add">«После успешного сравнения кандидата следующая задача — перенос в native/ и подключение готового потребителя».</p>
<p class="add">«После двух этапов только подготовки/упаковки/проверок разобрать отсутствие продвижения…»</p>
</div>
</div>

<div class="track">
<div class="ev"><b>10:43</b><code>62565b8</code><span>пауза, шаг и продолжение — последний коммит в <code>native/Sources</code> до 28-го</span></div>
<div class="ev"><b>12:05</b><code>be3d407</code><span>первый урон; в ту же минуту закончилась сессия /goal</span></div>
<div class="gap"><b>196,5 ч</b><span>ни одного коммита</span></div>
<div class="ev"><b>22–27 сен</b><code>96</code><span>коммитов — кандидаты на внешнем диске, мимо <code>native/</code></span></div>
<div class="ev hot"><b>28 сен 13:34</b><code>866bf83</code><span>перенос 2 291 файла — и первый матч</span></div>
</div>

<div class="source">git show a2e0230 · 2bbff56 · 007c007 -- docs/CONTINUE_GOAL.md · 0656992: docs/research/APPLICATION_EQUIVALENCE_FRONTIER.md · git log fc959db -- native/Sources · data/sessions.json (запуски цели, только время)</div>

<style>
.lead { margin: -0.45rem 0 0.35rem !important; font-size: 0.78rem; line-height: 1.4; color: var(--ink-2); max-width: 56rem; }
.trig { font-size: 0.62rem; line-height: 1.35; color: var(--ink-2); background: rgba(255,255,255,.03); border: 1px dashed var(--axis); border-radius: 10px; padding: 0.3rem 0.6rem; margin-bottom: 0.5rem; }
.trig .tm { font-family: var(--font-mono); font-size: 0.58rem; color: var(--muted); margin-right: 0.5rem; }
.trig .q { color: var(--ink); }
.trig i { font-style: normal; color: var(--naruto); margin: 0 0.25rem; }
.drafts { display: grid; grid-template-columns: 1fr 1.18fr 1fr; gap: 10px; align-items: stretch; }
.dr { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: 0.5rem 0.7rem 0.55rem; }
.dr.now { border-color: rgba(255,138,61,.6); box-shadow: 0 0 0 1px rgba(255,138,61,.15), 0 10px 28px rgba(0,0,0,.35); }
.dh { display: flex; justify-content: space-between; align-items: baseline; gap: 0.4rem; }
.dh .pixel { font-size: 0.72rem; color: var(--ink); }
.dr.now .dh .pixel { color: var(--naruto); }
.dh code { font-size: 0.56rem !important; }
.dk { font-family: var(--font-display); font-weight: 600; font-size: 0.78rem; color: var(--ink); margin: 0.2rem 0 0.3rem; }
.dr p { font-size: 0.62rem; line-height: 1.38; margin: 0.25rem 0 !important; padding-left: 0.55rem; border-left: 2px solid var(--axis); color: var(--ink-2); }
.dr p.old { border-left-color: rgba(141,145,156,.6); }
.dr p.add { border-left-color: var(--good); color: var(--ink); }
.track { display: grid; grid-template-columns: 1.25fr 1fr 0.9fr 1.2fr 1.15fr; gap: 8px; margin-top: 0.55rem; }
.track .ev, .track .gap { font-size: 0.6rem; line-height: 1.32; color: var(--ink-2); padding: 0.3rem 0.5rem; border-radius: 9px; background: rgba(255,255,255,.03); border: 1px solid var(--hair); }
.track b { display: block; font-family: var(--font-pixel); font-weight: 400; font-size: 0.7rem; color: var(--ink); }
.track .ev > code { font-size: 0.54rem !important; margin-right: 0.3rem; }
.track .gap { border-style: dashed; text-align: center; background: transparent; }
.track .gap b { color: var(--muted); }
.track .hot { border-color: rgba(255,138,61,.55); }
.track .hot b { color: var(--naruto); }
</style>

<!--
docs/CONTINUE_GOAL.md появился 12 сентября вместе со сжатием AGENTS.md (ffe16f4) под заголовком «Текст для нового goal»: «Ниже готовое задание… Сам этот документ goal не запускает». Это текст, которым запускали автопилот /goal в Codex.

Слева — редакция 13 сентября (a2e0230): задача выбирается по карте и CURRENT_WORK, «по готовности доказательств». Уже тогда в тексте было: «Рост EXE envelope не является условием её выбора» и «Сначала довести до проверенного полного матча Наруто и Саске на District» — но как промежуточная веха в конце задания.

В 09:42 14 сентября агент составил карту разрывов между проверенным ядром и приложением (0656992, APPLICATION_EQUIVALENCE_FRONTIER): в строке Product integration — «MeleeScene still uses OriginalMelee» и требование «Connect the recovered engine to the actual app». Та же фраза — у аудитора Codex на слайде «Не ускорять видимый прогресс».

В 10:36 — вторая редакция (2bbff56, «Refocus continuation prompt on playable match dependencies»). Задача теперь выбирается по препятствиям сквозной вехе — полному матчу Наруто и Саске на District в нативном приложении; до начала нужно показать связь «задача → недостающий контракт или результат → сквозная веха»; удобный сохранённый корпус приоритет не определяет; подключение движка к приложению не откладывать до переноса всего. Тогда же появилось правило про medium effort: оценивать его «на ограниченной реализации по закреплённому контракту и независимо проверенному компаратору».

Что было дальше. В 10:43 — 62565b8, пауза, шаг и продолжение в собственной сессии приложения: это единственный коммит в native/Sources с 14 по 27 сентября (тот самый «1 коммит из 115» с предыдущего слайда). В 12:05 — диагностика первого урона (be3d407), и в ту же минуту закончилась сессия Codex с автопродолжениями /goal, начатая 12 сентября (по метаданным журнала, без текста). Следующий коммит — через 196,5 часа, 22 сентября в 16:37; следующая сессия с /goal началась в тот же день в 08:59. 22–27 сентября — 96 коммитов, работа в кандидатах на внешнем диске.

Третья редакция — 27 сентября в 09:47 (007c007), вместе с правилами прогресса. Разница с 14-м: не куда идти, а что делать после каждого успешного сравнения — перенести и подключить; и счётчик «два этапа без продвижения». Через сутки, 28 сентября в 13:34, кандидат на 2 291 файл перенесли в native/ (866bf83), и в тот же день матч в приложении дошёл до KO.

Вывод: поворот 27–28 сентября не был первой попыткой. Направление к матчу записали 14-го, но без механизма переноса оно две недели оставалось на бумаге.
-->

---
clicks: 6
---

<Kicker>жизненный цикл карточки</Kicker>

# От плана до переноса — шесть стадий

<Pipeline class="mt-4" stepwise :steps="[
  { name: 'PLAN', ru: 'замороженный план', desc: 'вопрос, входы с SHA, конечный список случаев, лимиты, критерии приёмки' },
  { name: 'PREFLIGHT', ru: 'предполётная', desc: 'только чтение: найти разрывы интеграции до запуска' },
  { name: 'CANDIDATE', ru: 'кандидат', desc: 'изолированная копия; синтаксис — ещё не доказательство' },
  { name: 'VALIDATION', ru: 'валидация', desc: 'свежая сборка, сравнение с эталоном, каждый исход записан', accent: true },
  { name: 'CORRECTION', ru: 'исправление', desc: 'новый run ID; старый провал остаётся провалом' },
  { name: 'COMPLETION', ru: 'завершение', desc: 'регрессии, гейты, перенос в native/' },
]" loop-label="не больше трёх раундов на механизм — переименование не обнуляет счётчик" :loop-from="3" :loop-to="4" />

<div class="grid grid-cols-3 gap-4 mt-2 small ink2">
<div><b>Frozen plan.</b> План коммитится до запуска и больше не правится. Уточнение — отдельный amendment, который «описывает только различие».</div>
<div><b>202 плана, 27 исправлений.</b> В <code>docs/research</code> 568 карточек; 26 VALIDATION и 22 PREFLIGHT.</div>
<div><b>Ничего не стирать.</b> Прежний кандидат, логи и исходы хранятся; новый запуск получает свой ID и запись «что изменили и почему».</div>
</div>

<div class="source">docs/research/WORKFLOW.md · docs/research/PROGRESS_RULES.md · docs/research/TASK_TEMPLATE.md</div>

---

<Kicker>анатомия одной карточки · 22 сентября, 18:11–20:09</Kicker>

# 42 метода, 5 прогонов, 0 изменённых эталонов

<div class="mt-3">
<HostChainStrip />
</div>

<div class="grid grid-cols-[1.4fr_1fr] gap-5 mt-2">
<div class="small ink2">

Вопрос карточки: удержит ли постоянный host вход в загрузку и закоммитит ли итерацию меню целиком — с откатом и повтором. Все три исправления касались **только теста**; Core, expected и маски не менялись.

</div>
<div class="card-soft">
<div class="mono xsmall hl">"This is an incomplete resource-limited run, not a successful comparison or an assertion mismatch."</div>
<div class="xsmall muted mt-1">APPLICATION_HOST_LOADING_CORRECTION1.md</div>
</div>
</div>

<!--
Итог цепочки: 7 коммитов, 14 документов, 25 evidence-файлов за два часа — ради двух исправлений теста. Самое смешное — тест №28 упал не на логике игры, а на XCTAssertNotNil, который рекурсивно печатал огромное значение (пик 13,2 ГБ).
-->

---

<Kicker>7–27 сентября · месяц вслепую</Kicker>

# 3,4 млрд токенов — и никакой новой картинки

<BlindMonth class="mt-1" />

<div class="grid grid-cols-4 gap-3 mt-1">
<StatTile :value="36104" prefix="+" label="строк Swift-тестов за 7–27 сентября" size="sm" accent="var(--s1)" />
<StatTile :value="58621" prefix="+" label="строк в карточках исследований" size="sm" accent="var(--s4)" />
<StatTile value="52,87 %" label="кода .text EXE в описанных диапазонах порта" size="sm" accent="var(--s3)" />
<StatTile value="801 → 801" label="строк в слое приложения: на экране ничего нового" size="sm" accent="var(--s2)" />
</div>

<div class="source">data/tokens.json (журналы сессий) · data/app_lines.json (native/Sources/NTSDApp по дням) · data/growth.json · docs/estimates</div>

<!--
55 % всех токенов проекта ушло до первого матча в приложении. Снаружи это выглядело как сжигание денег: в окне — тренировочная сцена 7 сентября. Внутри росли ядро, оракулы и эталоны, на которых потом всё собралось за один день.
-->

---

<Kicker>что говорили аудиторы — что решали</Kicker>

# Не ускорять видимый прогресс

<div class="blind mt-1">
<div class="hdr"><span class="i-pixelarticons-eye" />аудиторы Codex видели</div>
<div></div>
<div class="hdr"><span class="i-pixelarticons-flag" />решение</div>

<div class="q"><span class="d">8 сен</span>«Но прироста подтверждённых игровых возможностей Practice за эти 12 часов нет».</div>
<div class="arr i-pixelarticons-arrow-right" />
<div class="a"><span class="d">8 сен</span>«<b>Не ускоряем видимый прогресс добавлением персонажей и техник на неполной основе.</b> …тренировочное окно некоторое время может выглядеть прежним».</div>

<div class="q"><span class="d">12 сен</span>«Сейчас основная проблема — разрыв между большим проверенным ядром и ограниченной Practice».</div>
<div class="arr i-pixelarticons-arrow-right" />
<div class="a"><span class="d">12 сен</span>Готовый движок L2DF дал работающее приложение через 16 минут после просьбы — и был остановлен: <i>«ок, остановил. продолжаем на main»</i>.</div>

<div class="q"><span class="d">14 сен</span>«Это полезно, но пользовательского результата пока не добавляет: MeleeScene всё ещё использует OriginalMelee».</div>
<div class="arr i-pixelarticons-arrow-right" />
<div class="a"><span class="d">13 сен</span>«…Погоня за ростом диапазонов сейчас дала бы красивый процент, но не приблизила бы так сильно первый настоящий матч».</div>

<div class="q"><span class="d">27 сен</span>«Ни одного коммита в <code>native/</code> за эти 9 часов. Приложение продолжает запускать Practice».</div>
<div class="arr i-pixelarticons-arrow-right" />
<div class="a"><span class="d">27 сен</span>Правила прогресса: проверенное — сразу переносить в <code>native/</code>. Но ни одна проверка не отменяется и ни один эталон не правится.</div>
</div>

<div class="card thesis mt-3">
<span class="i-pixelarticons-quote-text-inline" />
<div>
<div class="mono small">«Методология валидации — это всё. Это самое важное. Это ровно то, что в самом конце привело нас к полному паритету в интеграционных тестах».</div>
<div class="xsmall muted mt-1">автор проекта · <b class="hl">28 сентября</b> — первый матч в приложении, <b class="hl">3 октября</b> — 58 целых матчей без единого расхождения с оригиналом</div>
</div>
</div>

<div class="source">~/.codex/sessions: сессии-аудиты 8, 12, 13, 14, 26 и 27 сентября · 007c007 · docs/research/PROGRESS_RULES.md</div>

<style>
.blind { display: grid; grid-template-columns: 1fr 1.3rem 1.12fr; column-gap: 0.55rem; row-gap: 0.45rem; align-items: center; }
.blind .hdr { display: flex; align-items: center; gap: 0.4rem; font-family: var(--font-pixel); font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--naruto); }
.blind .hdr span { width: 1.05rem; height: 1.05rem; }
.blind .q, .blind .a { align-self: stretch; font-size: 0.66rem; line-height: 1.36; padding: 0.38rem 0.6rem; border-radius: 10px; }
.blind .q { background: var(--surface); border: 1px solid var(--hair); color: var(--ink-2); }
.blind .a { background: rgba(57,135,229,0.12); border: 1px solid rgba(57,135,229,0.35); color: var(--ink); }
.blind .d { display: inline-block; font-family: var(--font-mono); font-size: 0.58rem; color: var(--muted); margin-right: 0.45rem; }
.blind .arr { width: 1.1rem; height: 1.1rem; color: var(--naruto); justify-self: center; }
.thesis { display: flex; gap: 0.75rem; align-items: flex-start; border-color: rgba(255,138,61,0.55); padding: 0.75rem 1rem; }
.thesis > span { flex: none; width: 1.5rem; height: 1.5rem; color: var(--naruto); }
</style>

<!--
Полностью, 8 сентября: «Не ускоряем видимый прогресс добавлением персонажей и техник на неполной основе. Сейчас основной результат будет появляться в движке и проверках; тренировочное окно некоторое время может выглядеть прежним».
12 сентября пользователь спросил: «кароче не стоит полагаться на движок? лучше делать как в main-е, продолжить как шли?» — ответ: «ок, остановил. продолжаем на main».
13 сентября целиком: «Основную стратегию менять не стоит… Погоня за ростом диапазонов сейчас дала бы красивый процент, но не приблизила бы так сильно первый настоящий матч».
-->

---

<Kicker>26 сентября, 21:21 → 27 сентября, 09:46 · UTM 4.7.5</Kicker>

# Windows дошла до лицензии

<p class="lead">Единственная попытка получить настоящую Windows: виртуальная машина без сети на том же Mac. За ночь она дошла до экрана лицензии, человек лицензию одобрил — а нажать «Принять» оказалось нечем.</p>

<div class="grid grid-cols-[1.38fr_1fr] gap-5">
<div class="win">
<div class="wt"><span class="dots"><i /><i /><i /></span><span>NTSD Windows 11 ARM Reference</span><span class="mono">QEMU · UTM 4.7.5</span></div>
<div class="spec"><span class="tag">ARM64</span><span class="tag">4 vCPU</span><span class="tag">8 ГиБ</span><span class="tag">64 ГиБ NVMe</span><span class="tag">UEFI + TPM 2</span><span class="tag no">без сети</span><span class="tag no">без общих папок</span><span class="tag no">без буфера обмена</span></div>
<div class="steps">
<div class="s ok"><span class="t">21:21</span><span class="m">✓</span><div>ВМ создана и сверена по конфигурации <code>d638ad5</code></div></div>
<div class="s ok"><span class="t">22:39</span><span class="m">✓</span><div>ISO Windows 11 25H2 ARM64 с официальной страницы: первое скачивание встало на 16 МиБ, дальше — <b>6 385 диапазонов</b>, 7 994 415 104 байт, SHA-256 = Microsoft <code>ab504f5</code></div></div>
<div class="s ok"><span class="t">22:40</span><span class="m">✓</span><div>загрузка: UEFI shell → Boot Manager → со второго выбора CD — <b>Windows 11 Setup</b> <code>ab504f5</code></div></div>
<div v-click class="s hum"><span class="t">до 23:18</span><span class="m">✓</span><div><b>человек одобрил лицензию</b> Windows 11 Home и разрешил ставить дальше без повторных вопросов</div></div>
<div v-click class="s bad"><span class="t">23:18</span><span class="m">✕</span><div>экран Mac заблокирован: окна UTM «нет» — <code>cgWindowNotFound</code>, «Принять» не нажато <code>e1567bf</code></div></div>
<div v-click class="s bad"><span class="t">08:09–09:21</span><span class="m">✕</span><div>снять кадр мимо окна: у QEMU только канал SPICE, без QMP; снимки UTM живут лишь в памяти <code>b690e40</code> <code>97b2f65</code></div></div>
<div v-click class="s end"><span class="t">09:46</span><span class="m">■</span><div><b>«give up on UTM»</b>. Перед отменой окно ожило на лицензии: Return — «Please wait», затем процесс QEMU исчез. Windows так и не установлена <code>52d4740</code></div></div>
</div>
</div>
<div>

<div class="card-soft why">
<div class="pixel hl xsmall mb-1">зачем была нужна Windows</div>
<p><b>10 сен.</b> Захват старта CRT упёрся в ответ Windows на <code>GetStringTypeW</code> — его знает только настоящая система <code>4595a0e</code></p>
<p><b>26 сен.</b> Пиксели первого меню: курсор, текст GDI, DirectDraw — в Unicorn это лишь объявленные ответы устройства <code>2255ba5</code></p>
</div>

<div class="card-soft why mt-2">
<div class="pixel xsmall mb-1" style="color: var(--muted)">приготовили — и не запустили</div>
<p>диск переноса: <b>1 595 файлов игры</b>, сверенных побайтно</p>
<p>VC++ 2005 SP1 x86 для MSVCR80 оригинала</p>
<p>наборы наблюдений: курсор <code>4ad8cbb</code>, текст меню DirectDraw <code>d6f2ce8</code></p>
</div>

<div class="card-soft mt-2 cx">В 21:36 того же вечера поставили и пробный <b>CrossOver</b> <code>da9eeb8</code> — эталоном в итоге станет он (глава 8).</div>

</div>
</div>

<div class="source">WINDOWS_UTM_REFERENCE_SETUP.md · WINDOWS_UTM_INSTALLER_START.md · WINDOWS_UTM_HOST_LOCK.md · REFERENCE_PREREQUISITE_PREPARATION.md · WINDOWS_REFERENCE_PLAN.md · docs/evidence/windows-utm-*.json · d638ad5 … 97b2f65 · 52d4740 · время — по git, +0300</div>

<style>
.lead { margin: -0.45rem 0 0.4rem !important; font-size: 0.78rem; line-height: 1.4; color: var(--ink-2); max-width: 56rem; }
.win { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; overflow: hidden; }
.wt { display: flex; align-items: center; gap: 0.6rem; font-size: 0.64rem; color: var(--ink); background: var(--surface-2); padding: 0.3rem 0.6rem; border-bottom: 1px solid var(--hair); }
.wt .mono { margin-left: auto; font-size: 0.56rem; color: var(--muted); }
.wt .dots { display: inline-flex; gap: 4px; }
.wt .dots i { width: 8px; height: 8px; border-radius: 50%; background: var(--axis); }
.spec { display: flex; flex-wrap: wrap; gap: 0.25rem 0.3rem; padding: 0.4rem 0.6rem 0.1rem; }
.spec .tag { font-size: 0.56rem; }
.spec .tag.no { color: var(--good); border-color: rgba(12,163,12,.4); }
.steps { padding: 0.3rem 0.6rem 0.5rem; display: flex; flex-direction: column; gap: 0.22rem; }
.s { display: grid; grid-template-columns: 4.2rem 1rem 1fr; align-items: baseline; font-size: 0.61rem; line-height: 1.34; color: var(--ink-2); padding: 0.18rem 0.35rem; border-radius: 7px; }
.s .t { font-family: var(--font-mono); font-size: 0.56rem; color: var(--muted); }
.s .m { font-weight: 700; }
.s b { color: var(--ink); }
.s code { font-size: 0.52rem !important; }
.s.ok .m { color: var(--good); }
.s.hum { background: rgba(57,135,229,.1); }
.s.hum .m { color: var(--chakra); }
.s.bad .m { color: var(--critical); }
.s.end { background: rgba(208,59,59,.1); border: 1px solid rgba(208,59,59,.35); }
.s.end .m { color: var(--critical); }
.why p { font-size: 0.62rem; line-height: 1.36; color: var(--ink-2); margin: 0.22rem 0 !important; }
.why b { color: var(--ink); }
.why code, .cx code { font-size: 0.52rem !important; }
.cx { font-size: 0.62rem; line-height: 1.36; color: var(--ink-2); }
.cx b { color: var(--ink); }
</style>

<!--
По кликам — как ночь закончилась.

Зачем вообще Windows. Ещё 10 сентября захват старта CRT в Unicorn остановился на GetStringTypeW: ответ этой функции знает только настоящая система, и агент написал план эталонной машины (4595a0e, WINDOWS_REFERENCE_PLAN): гость ARM64 не больше 4 vCPU и 8 ГиБ, тонкий диск 64 ГиБ, без сети — с оговоркой, что Windows ARM исполняет x86-игру через трансляцию и это не физический x86. 26 сентября к этому добавились пиксели первого меню (2255ba5): курсор, текст и DirectDraw.

Ночь 26 сентября, время по git (Москва). Человек разрешил Windows через UTM и сам поставил UTM. 21:21 — ВМ «NTSD Windows 11 ARM Reference»: ARM64, 4 vCPU, 8 192 МиБ, UEFI, TPM 2, тонкий NVMe на 64 ГиБ, без сетевой карты, без общих папок и общего буфера; рядом — отдельный диск переноса только для чтения: 1 595 файлов игры (854 489 099 байт), каждый сверен побайтно. ISO — Windows 11 25H2 English ARM64 с официальной страницы Microsoft; ссылка на IoT-образ, от которой отказался веб-инструмент (строка S в таблице остановок), не повторялась. Первое скачивание curl встало на 16 МиБ; агент перешёл на диапазоны по 8 МиБ с проверкой каждого ответа 206. Итог к 22:39 (коммит в 22:47): 176 сохранённых и 6 209 новых диапазонов покрывают ровно 7 994 415 104 байт без дыр и наложений, SHA-256 совпал с опубликованным Microsoft.

22:40:45 — старт QEMU. Первая автозагрузка попала в UEFI shell; выход в Boot Manager и выбор CD показал «press any key», но подтверждение ушло отдельным вызовом инструмента и вернуло прошивку; со второго раза — Windows 11 Setup. Обходы проверок из руководства UTM не использовали.

До 23:18 человек явно одобрил лицензию Windows 11 Home (апрель 2024) и попросил продолжать установку без повторных вопросов о соглашениях. Но «Принять» не нажато: Computer Use вернул cgWindowNotFound для окна UTM, а IORegistry показал CGSSessionScreenIsLocked=true — экран Mac заблокирован. Разблокировать его агент не пытался. Карточка: «This is an unavailable host UI, not a safety refusal, an installer failure or a request to restart the guest». Тем временем агент подготовил наборы наблюдений для будущей Windows — курсор (4ad8cbb) и текст меню через DirectDraw (d6f2ce8) — и вернулся к нативной работе: той же ночью шли звук и PCM.

Утром 27-го — попытки увидеть экран гостя без окна. 08:09: у QEMU монитор — именованный канал SPICE, отдельного QMP нет, снимка на диске нет. 09:21: по исходникам UTM 4.7.5 периодические снимки SPICE обновляют состояние только в памяти, а сохранённые состояния не поддерживаются для GL-дисплея и NVMe этой ВМ.

09:46 — «give up on UTM» (52d4740), указание человека: работу с UTM не возобновлять, CrossOver остаётся альтернативой. Перед отменой окно гостя снова стало видно на экране лицензии: клик по координатам — ошибка Computer Use -10005, Return — «Please wait», следующий снимок — только библиотека UTM. В 09:42:46 процесса QEMU в ps уже не было; почему — неизвестно, и ни установки Windows, ни ошибки установщика это не доказывает. ВМ, ISO и все записи сохранены. Поэтому на слайде о лестнице доказательств: настоящей Windows-машины в проекте так и не появилось.

А в 21:36 того же вечера (da9eeb8) агент поставил пробный CrossOver и подготовил чистую копию NTSD — с этой стороны эталон и пришёл: глава 8.
-->

---

<Kicker>27 сентября</Kicker>

# Правила прогресса

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-2">
<div>

<div class="xsmall muted">PROGRESS_RULES.md — «указание пользователя от 2026-09-27 после разбора 19 коммитов за девять часов»</div>

<div class="prules mt-2">
<div class="pr"><span class="i-pixelarticons-git-merge" /><div><b>Проверено — переносим.</b> «После успешного сравнения кандидата следующая задача — его перенос в <code>native/</code> и подключение ближайшего готового потребителя».</div></div>
<div class="pr"><span class="i-pixelarticons-repeat" /><div><b>Два шага без продвижения — разбор.</b> «После двух последовательных этапов только подготовки/упаковки/проверок… разобрать причину отсутствия продвижения. Переименование карточки счётчик не обнуляет».</div></div>
<div class="pr"><span class="i-pixelarticons-script" /><div><b>Без новых обёрток.</b> «Не добавлять новый prepare/finalize/publish-скрипт, отличающийся путями, счётчиками или названием задачи».</div></div>
<div class="pr"><span class="i-pixelarticons-pin" /><div><b>Гейт — один раз.</b> «Каждая отдельная gate проверяется и записывается один раз для закреплённых байтов».</div></div>
<div class="pr"><span class="i-pixelarticons-gamepad" /><div><b>Счёт файлов — не результат.</b> «Число файлов, архивов, инструкций и тестов не заменяет игровой или прикладной результат».</div></div>
</div>

</div>
<div>

<div class="card">
<div class="ttl"><span class="i-pixelarticons-computer" /><span class="pixel hl small">в тот же день</span></div>
<p class="small ink2">«Stop UTM work and prioritize native app integration» — виртуальную Windows-машину бросили: <i>«give up on UTM»</i>.</p>
<div class="tag">52d4740</div> <div class="tag">007c007</div>
</div>

<div class="card mt-3">
<div class="ttl"><span class="i-pixelarticons-calendar" /><span class="pixel hl small">прогноз · 27 сен, 09:49 МСК</span></div>
<p class="small ink2">«1–3 недели до первого проверенного Наруто/Саске матча в приложении; 6–12 недель до полного порта».</p>
<div class="xsmall muted">Через 33 часа матч в приложении дошёл до KO, через 5 дней целые матчи сверялись с оригиналом →</div>
</div>

</div>
</div>

<style>
.prules { display: flex; flex-direction: column; gap: 0.4rem; }
.pr { display: flex; gap: 0.6rem; align-items: flex-start; background: rgba(255, 255, 255, 0.03); border: 1px solid var(--hair); border-radius: 10px; padding: 0.42rem 0.65rem; font-size: 0.68rem; line-height: 1.38; color: var(--ink-2); }
.pr > span { flex: none; width: 1.3rem; height: 1.3rem; color: var(--naruto); margin-top: 0.05rem; }
.pr b { color: var(--ink); font-weight: 650; }
.ttl { display: flex; align-items: center; gap: 0.45rem; }
.ttl > span:first-child { flex: none; width: 1.2rem; height: 1.2rem; color: var(--naruto); }
</style>

<div class="source">docs/research/PROGRESS_RULES.md · 52d4740 · 007c007 · d1a930e</div>

<!--
Правила подготовили 27-го, но подключили только 28-го (d1a930e) — когда закрылись jobs, которые закрепили старые версии инструкций как вход. Даже правки правил ждали, пока живые процессы допишут свои результаты.
-->
