---
layout: chapter
num: 8
total: 20
kicker: Глава восьмая
dates: 2–3 октября
image: /img/screens/15-summary-mac-vs-original-side-by-side.jpg
stats: 47 из 47 случайных матчей равны · 156 730 сверенных тиков · /loop
---

# Сверка с оригиналом

Хватит отдельных функций: обе программы играют одни и те же матчи целиком — и сравнивают итоги прямо из памяти.

---

<Kicker>2 октября, 06:59 — 07:02 · офлайн-приёмка и сверка объёма</Kicker>

# Перепроверить на чистом дереве

<div class="grid grid-cols-[0.9fr_1.3fr] gap-5 mt-1">
<div class="trees">

<div class="tr dirty">
<div class="th"><span class="i-pixelarticons-git-branch ti" /><b>рабочее дерево main</b><span class="tag">грязное</span></div>
<div class="tt">Лежат <b>15 незакоммиченных файлов</b> — 14 изменённых и 1 новый: отложенная автором сеть N2 и чужие правки документов. Проверки слова попадания вечером 1 октября (<code>7d592f9</code>) собраны вместе с ними.</div>
</div>

<div class="arr"><span>«Earlier dirty-tree results do not transfer» — прогнать заново, один раз</span></div>

<div class="tr clean">
<div class="th"><span class="i-pixelarticons-git-commit ti" /><b>кандидат <code>2d6a7e5</code></b><span class="tag">отдельный worktree на X5</span></div>
<div class="tt">LFS — <b>3 025 из 3 025</b> объектов из локального хранилища, без сети. <code>build-native.sh</code> — 166,7 с, бинарник <code>ec5afcc1…</code>, ad-hoc подпись цела.</div>
</div>

<div class="grid grid-cols-3 gap-2 mt-2">
<StatTile :value="38" label="тестов" sub="попадания, физика, слот" size="sm" accent="var(--good)" />
<StatTile :value="7845" label="целых пулов" sub="корпус попаданий" size="sm" accent="var(--good)" />
<StatTile value="10 / 10" label="сценариев e2e" sub="на бандле кандидата" size="sm" accent="var(--good)" />
</div>

</div>
<div>

<div class="sh">07:02 · 18 критериев полного объёма из CONTINUE_GOAL — у каждого класс и свежее доказательство</div>

<BScopeStrip />

</div>
</div>

<div class="verdict"><span class="i-pixelarticons-flag vi" /><span><span class="q">«The only implementation gap is network play, which the user has deferred.»</span> Остальные недостающие проверки упираются во внешнее: проснувшийся экран, Windows, устройство, чистый Mac.</span></div>

<div class="source">3d36966 · 0356f06 · docs/evidence/application-offline-acceptance-20261002.json · docs/research/APPLICATION_PACKAGING.md (offline follow-up) · SCOPE_RECONCILIATION_2026-10-02.md</div>

<style>
.trees { display: flex; flex-direction: column; }
.tr { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: 0.42rem 0.65rem 0.48rem; }
.tr.dirty { border-color: rgba(250, 178, 25, 0.5); }
.tr.clean { border-color: rgba(12, 163, 12, 0.5); }
.th { display: flex; align-items: center; gap: 0.4rem; font-size: 0.7rem; color: var(--ink); }
.th code { font-size: 0.64rem !important; }
.th .tag { margin-left: auto; font-size: 0.54rem; }
.ti { width: 1rem; height: 1rem; color: var(--naruto); flex: none; }
.tt { font-size: 0.62rem; line-height: 1.38; color: var(--ink-2); margin-top: 0.2rem; }
.tt b { color: var(--ink); }
.tt code { font-size: 0.56rem !important; }
.arr { display: flex; justify-content: center; margin: 0.1rem 0; }
.arr span { position: relative; font-size: 0.56rem; color: var(--muted); padding: 0.28rem 0 0.28rem 1rem; }
.arr span::before { content: '↓'; position: absolute; left: 0; top: 0.12rem; color: var(--naruto); font-size: 0.85rem; }
.sh { font-size: 0.6rem; color: var(--muted); margin-bottom: 0.3rem; }
.verdict { display: flex; align-items: center; gap: 0.6rem; margin-top: 0.55rem; font-size: 0.66rem; line-height: 1.38; color: var(--ink-2); background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(208, 59, 59, 0.45); border-radius: 12px; padding: 0.4rem 0.75rem; }
.verdict .q { color: var(--ink); font-family: var(--font-mono); font-size: 0.6rem; }
.vi { width: 1.2rem; height: 1.2rem; color: var(--critical); flex: none; }
</style>

<!--
Утро перед сверкой с оригиналом. Ночью 1 октября агент закрыл слово попадания (7d592f9), но в коммите честно записал: прогон шёл на рабочем дереве, где лежат отложенные автором незакоммиченные сетевые правки. Значит, эти результаты относятся к другому бинарнику.

Офлайн-приёмка (3d36966, 06:59). Кандидат — detached worktree коммита 2d6a7e5 (в нём уже есть 7d592f9) на диске X5, на отведённых задаче 40 ГиБ. Объекты LFS — 3 025 из 3 025 — взяты из локального хранилища без сети. Отложенная работа N2 и чужие правки документов в основном дереве не тронуты: 14 изменённых файлов и 1 новый перечислены в evidence с хэшами. Сборка tools/build-native.sh — 166,7 с, бинарник 15,6 МБ, sha256 ec5afcc1…, ad-hoc подпись действительна. Прошли 38 тестов попаданий, физики, игрового тела и слота запросов, корпус попаданий (7 845 целых пулов) и все десять e2e-сценариев на исполняемом файле бандла: vs, mission, demo, war, playback, tournament, altenter, tournament-win, team-tournament, joystick. Длинные soak-прогоны (War 60 000, Demo 100 000, Stage 4-1 100 000 тел) шли на том же грязном бинарнике и не повторялись: гейт их не требовал, они остаются доказательством для своих входов. Оригинал не запускался, сеть не использовалась.

Сверка объёма (0356f06, 07:02). Каждый из 18 критериев полного объёма из CONTINUE_GOAL получил класс: V — проверено сравнением или проверками приложения; M — реализовано, но не хватает конкретной проверки; G — пробел реализации; E — препятствие снаружи, с доказательством. Наведите на плитку — внизу появится, чего не хватает. Единственный G — ONLINE GAME: N1 закоммичен, N2 — незакоммиченный WIP, автор отложил сеть 1 октября, отказ модели на сетевой интеграции открыт. Звук и полный экран macOS — M: звук не с чем сравнить без Windows, а переход AppKit не видел никто — 1 и 2 октября дисплей спал. Единственная разрешённая конкретная проверка, которую нашла сверка, — F1, F2, F3, F5, F6 и F9 в бою VS на офлайн-кандидате; прошла без остановки, игра показала своё «Function Keys Locked». Заодно исправлена устаревшая строка карты: «Default launch is still Practice». Независимый ревьюер в этих сессиях недоступен, ревью всех карточек открыто.

Итог карточки: других разрешённых задач нет, пока автор не снимет отсрочку сети или не станет доступна одна из внешних проверок. Через десять часов автор спросит, какой процент кода реализован, — следующий слайд.
-->

---

<Kicker>2 октября, 17:07 → 23:26 · реплики автора — из журнала сессии Claude</Kicker>

# «чтобы на 100% покрыть всё»

<div class="asks">
<div class="ask"><span class="t mono">17:07</span>«какой процент кода проанализирован и exactly реализован?»</div>
<div class="ask"><span class="t mono">18:15</span>«у нас же есть windows через crossover?»</div>
<div class="ask hot"><span class="t mono">18:18</span>«…составь доку с планом по добивке игры. чтобы на 100% покрыть всё. запиши в docs/GOAL_100.md»</div>
</div>

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-2">
<div>

<div class="sh">18:34 · <code>a8bbb84</code> · docs/GOAL_100.md — восемь измерений и где проект на 2 октября</div>

<div class="dims">
<div class="dm part"><i>1</i><b>Код EXE</b><span>51,4 % инструкций исполнено в записях; 157 из 174 функций с корпусами — 92,4 % инструкций</span></div>
<div class="dm part"><i>2</i><b>Поведение</b><span>10 e2e-сценариев, все режимы; известный пробел — финал Stage <em class="p0">P0</em></span></div>
<div class="dm open"><i>3</i><b>Длинная эквивалентность</b><span>не измерялась: целые матчи потиково не сравнивались. План P1b — повторы через CrossOver, <q>нужно участие пользователя у экрана</q></span></div>
<div class="dm open"><i>4</i><b>Windows</b><span>ответы, которых EXE не фиксирует, объявлены; на Windows ничего не наблюдалось</span></div>
<div class="dm none"><i>5</i><b>Данные</b><span>строки состояния нет; в работах — hit_Fa 11, его не использует ни один DAT дистрибутива</span></div>
<div class="dm part"><i>6</i><b>Приложение и устройство</b><span>хост-проверки пройдены; полный экран macOS, контроллер, чистый Mac — ждут</span></div>
<div class="dm open"><i>7</i><b>Сеть</b><span>N1 в main, N2 у параллельного агента; отказ модели 1 октября открыт</span></div>
<div class="dm open"><i>8</i><b>Приёмка</b><span>независимого ревьюера нет — ревью всех карточек открыто</span></div>
</div>

</div>
<div>

<div class="sh">P0 · 23:26 · <code>996d2c0</code> · экран ENDING, до которого порт не доходил</div>

<BEnding />

<div class="grid grid-cols-3 gap-2 mt-2">
<StatTile :value="581" label="случай Unicorn" sub="все совпали" size="sm" accent="var(--good)" />
<StatTile :value="7171" label="вызов" sub="по порядку" size="sm" accent="var(--s1)" />
<StatTile :value="39186" label="байт записано" sub="ничего лишнего" size="sm" accent="var(--s1)" />
</div>

<div class="lim">Живое приложение до меню 300 ещё не доходило: нужен пройденный Stage 5 или его запись.</div>

</div>
</div>

<div class="source">сессия Claude Code 7ea5b99f, 2 октября (UTC+2) · a8bbb84 · 996d2c0 · docs/GOAL_100.md · docs/research/STAGE_ENDING.md · ресурс ENDING из NTSD 2.4.exe</div>

<style>
.asks { display: flex; gap: 0.5rem; margin-top: -0.2rem; }
.ask { font-size: 0.62rem; line-height: 1.32; color: var(--ink); background: rgba(57, 135, 229, 0.16); border: 1px solid rgba(57, 135, 229, 0.45); border-radius: 12px; border-top-right-radius: 4px; padding: 0.3rem 0.55rem; }
.ask.hot { border-color: rgba(255, 138, 61, 0.65); flex: 1.5; }
.ask .t { display: block; font-size: 0.5rem; color: var(--muted); margin-bottom: 0.05rem; }
.sh { font-size: 0.6rem; color: var(--muted); margin-bottom: 0.3rem; line-height: 1.3; }
.sh code { font-size: 0.54rem !important; }
.dims { display: flex; flex-direction: column; gap: 3px; }
.dm { display: grid; grid-template-columns: 1.1rem 8.4rem 1fr; gap: 0.4rem; align-items: baseline; font-size: 0.6rem; line-height: 1.3; color: var(--ink-2); background: var(--surface); border: 1px solid var(--hair); border-left: 3px solid var(--muted); border-radius: 8px; padding: 0.22rem 0.5rem; }
.dm i { font-style: normal; font-family: var(--font-pixel); color: var(--muted); }
.dm b { color: var(--ink); font-weight: 650; }
.dm.part { border-left-color: var(--warning); }
.dm.open { border-left-color: var(--serious); }
.dm.none { border-left-color: var(--axis); }
.dm q { color: var(--ink); quotes: '«' '»'; }
.p0 { font-style: normal; font-family: var(--font-mono); font-size: 0.52rem; color: #0a0d13; background: var(--naruto); border-radius: 4px; padding: 0 0.3rem; }
.lim { font-size: 0.58rem; color: var(--muted); margin-top: 0.35rem; line-height: 1.35; }
</style>

<!--
Реплики автора — дословно из журнала сессии Claude (время UTC+2); ответы агента здесь не цитируем. Между ними были ещё две: в 17:10 «посчитай глубокую оценку» и в 18:11 «ветку пушни с исследованием; и скажи мне что имеет смысл сделать дальше. нет ли темных мест которые стоило бы дальше поииследовать или потестить на предмет совпадения». Ответ на вопрос о проценте — измерение покрытия EXE на отдельной ветке, слайд «Сколько EXE на самом деле проверено» в конце главы.

GOAL_100.md (a8bbb84, 18:34). Документ определяет, что значит «покрыть игру на 100 %»: восемь измерений, и каждое закрывается отдельно — одно не заменяет другое. Левая колонка — его же таблица «Где мы сейчас», цвет полосы — моя оценка по её словам: жёлтое — частично, оранжевое — не начато или открыто. У «Данных» в таблице состояния строки нет; в работах есть hit_Fa 11 (0x406a20) — его не использует ни один DAT дистрибутива, но «для 100 % совместимости с данными» его тоже надо перенести и сверить на синтетическом DAT.

План P1b — длинная эквивалентность двумя способами: перекрёстное воспроизведение повторов через CrossOver и Unicorn lockstep на тысячи тиков. Про первый в плане прямо сказано: «Нужно участие пользователя у экрана». Поэтому через минуту после этого коммита, в 18:35, агент и попросил человека посидеть у экрана — следующий слайд. В 21:23 — девять целых матчей в обеих программах.

P0 — финал Stage. После последней группы стадий логика пишет меню 300 (это сверено в корпусе Mission), а экран 437220, который диспетчер вызывает для этого значения, не был разобран: порт останавливался на «Other menu dispatcher». В 23:26 (996d2c0) экран перенесён: страницы листа ENDING с открывающей и закрывающей шторкой из 13 полос, страницу закрывает Attack любого места, стрелка в углу мигает, после четвёртой страницы — меню 10 через сброс ввода 431c70. Все 581 случай настоящих 437220/431c70 под Unicorn совпали: 7 171 вызов по порядку и 39 186 записанных байт, и больше ничего не записано.

Анимация справа — по описанию из карточки: кадры листа ENDING из самого EXE, прямоугольники — статические константы, которые 424b45..424c98 пишут при старте; темп анимации наш, не замер. Переключатель сложности: на Easy и Normal (450c30 = 2 и 1) первая страница — «Congratulations on finishing Mission Mode. Now see if you accomplish it at a higher level…», на Difficult и CRAZY! её место занимает «Sorry, but there is no password for the Demo Version». Дальше у всех — «Thanks for playing!», прощальное письмо zxcv («I'll be retiring and focusing more time on my studies») и «special thanks to all our fans — The NTSDII Team».

Граница карточки: живое приложение в прогоне до меню 300 не доходило — для этого нужен пройденный Stage 5 или его запись; подключение идёт через тот же диспетчер и путь отрисовки, что у проверенных экранов.
-->

---

<Kicker>2 октября, 18:35–21:23 · из журнала сессии Claude</Kicker>

# Агент попросил человека посидеть у экрана

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-1">
<ChatLog :messages="[
  { who: 'agent', time: '18:35', text: '<b>Для прогона в CrossOver нужны вы у экрана:</b> окно Wine мне не видно.' },
  { who: 'human', time: '19:02', text: 'зачем я у экрана? что мне нужно будет делать?' },
  { who: 'agent', time: '19:02', text: 'Вариант А — вы проходите сами, около 20–30 минут: открываете повтор, смотрите до экрана итогов и делаете скриншот <code>⌘⇧3</code>. Так для каждого из пяти.' },
  { who: 'human', time: '19:03', text: 'а если ты используешь это <code>github.com/trycua/cua</code>?', hot: true },
  { who: 'agent', time: '19:04', text: 'Да, это может заметно облегчить дело. Скрипт установки я сначала прочитаю и только потом запущу.' },
  { who: 'human', time: '19:08', text: 'да, ставь cua driver и делай пробу' },
  { who: 'event', time: '19:22', text: 'единственное ручное действие: два переключателя для CuaDriver в настройках macOS' },
  { who: 'agent', time: '19:23', text: 'Главное меню оригинала под CrossOver видно. <b>До этого места прошлая попытка не дошла.</b>', hot: true },
  { who: 'event', time: '21:23', text: '3313088 · девять целых матчей сыграны в обеих программах', hot: true },
]" />
<div>

<div class="card">
<div class="pixel hl small">что было до этого</div>
<p class="small ink2 mb-0" style="line-height: 1.45">26 сентября Codex пытался управлять окном оригинала через AppleScript и встроенный Computer Use: macOS отказала в assistive access (<span class="mono">-1728</span>), а инструмент не стал работать с окном терминала. Окно игры агенту так и не открылось.</p>
<div class="xsmall muted mt-1">REFERENCE_ENVIRONMENT_ACCESS.md · 3cea373</div>
</div>

<div class="grid grid-cols-2 gap-3 mt-3">
<StatTile value="21 мин" label="от «а если cua?» до меню оригинала на экране агента" size="sm" />
<StatTile value="2 ч 20 мин" label="до девяти сверенных целых матчей" size="sm" accent="var(--s1)" />
</div>

<div class="card-soft mt-3 small ink2">
Перед установкой агент прочитал обёртку и проверил установщик на <b>1 605 строк</b>: sudo, автозапуск, правки shell rc, телеметрию. Телеметрию выключил.
</div>

</div>
</div>

<div class="source">~/.claude/projects: сессия 7ea5b99f, 2 октября (время местное, UTC+2) · 3313088 · docs/research/REFERENCE_ENVIRONMENT_ACCESS.md</div>

<!--
Поворот роли: агент по привычке предложил сделать человека своими руками и глазами. Человек вместо этого дал агенту руки — драйвер управления компьютером. Дальше вся сверка с оригиналом шла без человека у экрана.
-->

---

<Kicker>руки для агента · Cua Driver 0.32.0</Kicker>

# Чему агент научился, управляя Wine

<IconCards class="mt-3" :cols="3" :items="[
  { icon: 'i-pixelarticons-mouse', title: 'Клик в три приёма', text: 'Фоновые клики по кнопкам Wine игнорирует: окно вперёд → фоновый клик ставит курсор игры → клик foreground в ту же точку.', tag: 'tools/crossover_drive/cua.py' },
  { icon: 'i-pixelarticons-keyboard', title: 'Клавишу надо держать', text: 'Клавиши игра читает раз в кадр — нажатие держится 150 мс через <code>CGEvent.postToPid</code>.', tag: 'tools/crossover_drive/keyhold.swift' },
  { icon: 'i-pixelarticons-music', title: 'ERROR на каждой музыке', text: '«Could not create a filter graph» закрывается кликом по OK: клавиша дошла бы до игры.', tag: 'da5eaaa · 23139fe' },
  { icon: 'i-pixelarticons-coffee', title: 'Экран не должен спать', text: 'Блокировка экрана останавливает снимки и ввод — прогоны идут под <code>caffeinate</code>.', tag: 'docs/CROSSPLAY_LOOP.md' },
  { icon: 'i-pixelarticons-duplicate', title: 'Чужое окно с тем же именем', text: 'Окна параллельного агента тоже «Little Fighter 2» — ввод теперь только в <code>NTSD 2.4.exe</code>.', tag: 'CROSSOVER_REPLAY_CROSSPLAY.md' },
  { icon: 'i-pixelarticons-terminal', title: 'Терминалы не трогать', text: 'После отказа 26 сентября Cua шлёт ввод только в окно оригинала.', tag: 'codex-cua-ghostty-refusal-2026-09-26.json' },
]" />

<div class="grid grid-cols-3 gap-3 mt-4">
<StatTile value="~20–30 мин" label="вариант «вы проходите сами»" sub="человек у экрана — на пять повторов" size="sm" accent="var(--muted)" />
<StatTile :value="47" suffix="матчей" label="на следующий день с Cua и /loop" sub="агент сам сыграл и сверил 156 730 тиков" size="sm" accent="var(--s2)" />
<StatTile :value="8" suffix="сообщений" label="написал человек за эти девять часов" size="sm" accent="var(--chakra)" />
</div>

<div class="source">docs/CROSSPLAY_LOOP.md · docs/research/CROSSOVER_REPLAY_CROSSPLAY.md · da5eaaa · 23139fe · журнал сессии 7ea5b99f</div>

<!--
Клик в три приёма (tools/crossover_drive/cua.py). Wine игнорирует фоновые клики по кнопкам. Работает так: вывести окно вперёд, фоновым кликом поставить игровой курсор, затем клик в режиме foreground в ту же точку.

Клавишу надо держать (tools/crossover_drive/keyhold.swift). Мгновенное нажатие игра теряет: состояние клавиш она читает раз в кадр. Нажатия отправляются через CGEvent.postToPid с удержанием 150 мс.

ERROR на каждой музыке (da5eaaa · 23139fe). Под CrossOver каждый запуск музыки показывает «Could not create a filter graph». Окно закрывается кликом по OK, а не клавишей: клавиша дошла бы до игры. Однажды окно съело отпускание J.

Экран не должен спать (docs/CROSSPLAY_LOOP.md). Заблокированный экран останавливает снимки и ввод. «наверное mac mini уснул?» — после этого прогоны идут под caffeinate. А winedbg читает память оригинала и при заблокированном экране.

Чужое окно с тем же именем (CROSSOVER_REPLAY_CROSSPLAY.md). Окна нативного приложения параллельного агента тоже называются «Little Fighter 2». Два нажатия J и два клика ушли в его сетевой матч. Теперь ввод идёт только в окна NTSD 2.4.exe.

Терминалы не трогать (codex-cua-ghostty-refusal-2026-09-26.json). После отказа 26 сентября правило цикла: Cua не отправляет ввод в терминалы и другие приложения — только в окно оригинала.

Итог: вариант «вы проходите сами» стоил бы человеку ~20–30 минут на пять повторов. С Cua и /loop на следующий день агент сам сыграл и сверил 47 матчей — 156 730 тиков. Человек за эти девять часов написал восемь сообщений.
-->

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

<div class="card text-center" style="padding: 0.7rem 1rem 0.65rem">
<div class="xsmall muted">контрольная сумма порта + веса двойных токенов</div>
<div class="display mt-1" style="font-size: 1rem; line-height: 1.45">31 475 378<br>+ 137 × 5 239 <span class="xsmall muted">(&lt;frame_end&gt;)</span><br>+ 17 × 3 749 <span class="xsmall muted">(layer_end)</span></div>
<div class="mt-1" style="border-top: 1px solid var(--axis); padding-top: .4rem"><span class="display hl" style="font-size: 1.3rem">= 32 256 854</span></div>
<div class="mono small muted">0x1e046b2 → 0x1ec3356</div>
</div>

<div class="xsmall muted mt-2 mb-1">OriginalObjectLoader.swift: на EOF в сумму снова идёт прежний токен</div>

<div class="oracle-code">

```swift
while !input.eof {
    if let next = try input.observedToken() { token = next }
    guard let current = token else { throw Self.error("No initialized outer token") }
    for (index, scalar) in current.unicodeScalars.enumerated() {
        checksum &+= UInt32(bitPattern: Int32(Int8(
            bitPattern: UInt8(scalar.value)))) &* UInt32(index)
    }
```

</div>

</div>
</div>

<div class="source">3313088 · 53bc59e · docs/research/APPLICATION_CATALOG_CHECKSUM.md</div>

<style>
.oracle-code .slidev-code,
.oracle-code pre.shiki { font-size: 10px !important; line-height: 15px !important; }
</style>

---
clicks: 3
---

<Kicker>как играет пара программ</Kicker>

# Одна запись — две программы — одна таблица итогов

<FlowDiagram stepwise class="mt-2" input=".lfr запись" input-sub="Mac → оригинал или оригинал → Mac" :lanes="[
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

<div class="grid grid-cols-[30.5rem_1fr] gap-5 mt-1">
<BeforeAfter before="/img/compare/summary-mac.jpg" after="/img/compare/summary-original.jpg" before-label="Mac" after-label="оригинал под CrossOver" height="21.1rem" :start="50" />
<div class="flex flex-col gap-3">
<div class="card sumcard">
<div class="pixel hl xsmall">Summary · одинаково в обеих программах</div>
<table class="sumt">
<thead><tr><th></th><th>Kill</th><th>Attack</th><th>HP Lost</th><th>MP Usage</th><th>Picking</th><th>Status</th></tr></thead>
<tbody>
<tr><td>P1</td><td>1</td><td>985</td><td>780</td><td>275</td><td>0</td><td>Lose (Dead)</td></tr>
<tr><td>P2</td><td>0</td><td>30</td><td>960</td><td>0</td><td>0</td><td>Lose (Dead)</td></tr>
<tr><td>Com</td><td>1</td><td>1270</td><td>545</td><td>1165</td><td>6</td><td>Win (Alive)</td></tr>
</tbody>
</table>
<div class="sumtime"><span class="i-pixelarticons-clock" /> time <b>00 : 54</b></div>
</div>
<div class="small ink2">Kill, Attack, HP Lost, MP Usage, Picking и время 00:54 совпадают во всех трёх строках.</div>
<div class="small ink2">Внизу слева — <span class="mono xsmall">Recording file '20260101_010000_VS.lfr' saved!</span>: запись сделана на Mac со скриптом и виртуальными часами.</div>
<span class="tag self-start">docs/evidence/crossover-replay-crossplay-20261002</span>
</div>
</div>

<style>
.sumcard { padding: 0.6rem 0.75rem 0.55rem; }
.sumt { margin-top: 0.35rem; font-size: 0.62rem !important; font-variant-numeric: tabular-nums; }
.sumt th { font-size: 0.56rem; font-weight: 600; color: var(--muted); padding: 0.15rem 0.2rem !important; text-align: right; white-space: nowrap; }
.sumt td { padding: 0.2rem 0.2rem !important; color: var(--ink) !important; text-align: right; white-space: nowrap; }
.sumt td:first-child, .sumt th:first-child { text-align: left; color: var(--ink-2) !important; }
.sumt td:last-child { color: var(--ink-2) !important; }
.sumtime { display: flex; align-items: center; justify-content: flex-end; gap: 0.35rem; margin-top: 0.35rem; font-size: 0.62rem; color: var(--muted); }
.sumtime b { color: var(--ink); font-family: var(--font-mono); }
.sumtime span { width: 0.9rem; height: 0.9rem; color: var(--naruto); }
</style>

<!--
Ползунок можно тянуть: слева от ручки — кадр Mac-приложения, справа — тот же матч в оригинале под CrossOver 26.3. Оба кадра вырезаны из одного снимка по игровой области окна (794 × 550), без рамок.

Это два отдельных снимка: Mac — из своего e2e-прогона, оригинал — снимок через Cua. Сцена за таблицей на них разная: игра за Summary идёт дальше, а снимки сняты отдельно. Сравниваются итоги.

Mac-сборка этого кадра — ещё до исправления дыр RLE (55fd92d), отсюда чёрные плашки под подписями вроде «P1» и «Com». Оригинал проигрывал копию записи, в которой изменены только байты контрольной суммы каталога (+0x744…+0x746): тогда суммы у программ ещё расходились.
-->

---

<Kicker>3 октября · итог сверки</Kicker>

# 58 целых матчей — ни одного расхождения порта

<div class="mt-2">
<CrossplayTiles />
</div>

<div class="grid grid-cols-4 gap-3 mt-3">
<StatTile value="25 / 25" label="персонажей сыграли в равных матчах" size="sm" />
<StatTile value="17 / 17" label="фонов" size="sm" accent="var(--s1)" />
<StatTile :value="35272" label="тика — самый длинный War, ГСЧ сверялся каждые 1 000 тиков" size="sm" accent="var(--s3)" />
<StatTile value="1-1 … 5-1" label="первая фаза каждой группы Stage" size="sm" accent="var(--s4)" />
</div>

<CharacterBars class="mt-2" />

<div class="source">docs/evidence/crossplay-*.json · docs/research/CROSSPLAY_MATRIX.md · data/evidence/crossplay-matches.json</div>

---
layout: statement
kicker: 2–3 октября
big: 58 / 58
image: /img/screens/15-summary-mac-vs-original-side-by-side.jpg
shade: 0.9
---

<b>58 целых матчей</b> сверены с оригиналом под CrossOver.<br><b>Ни одного расхождения порта.</b>

<!--
58 = 42 случайных матча Mac → оригинал (VS 32, Stage 6, War 4) + 5 матчей оригинал → Mac + 11 ранних повторов; все равны (data/evidence/crossplay-matches.json, totals.allEqual). Demo остаётся открытым — следующий слайд.
-->

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
clicks: 5
---

<Kicker>/loop · 3 октября, 07:06–16:05</Kicker>

# Цикл, который ищет расхождения сам

<div class="xsmall muted mb-2 mt-2">CROSSPLAY_LOOP.md — задание для самотактируемого <code>/loop</code> Claude Code</div>

<Pipeline stepwise :steps="[
  { name: 'READ', ru: 'прочитать задание', desc: 'CROSSPLAY_LOOP.md и общие правила' },
  { name: 'PICK', ru: 'взять строку', desc: 'верхняя непроверенная в матрице' },
  { name: 'PLAY', ru: 'сыграть', desc: 'запись — в другой программе' },
  { name: 'DIFF', ru: 'локализовать', desc: 'тик → функция → инструкция', accent: true },
  { name: 'FIX', ru: 'исправить и записать', desc: 'тест, матрица, коммит' },
]" />
<CrossLoopBack :steps="5" :at="5" label="следующая итерация — пока в матрице есть непроверенные строки" />

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

<div class="card-soft mt-3 audit">
<div class="flex items-center gap-2"><span class="i-pixelarticons-warning-box audit-ico" /><b>Аудит на следующий день</b> <span class="muted">· другой агент</span></div>
<div class="mt-1">Метрика засчитала 293 адреса из статического файла, не нашла WndProc <code>0x43b3d0</code> и пропустила 2 529 входов в блоки. 47&nbsp;% — ни процент реализованного кода, ни проверенная нижняя граница, интервал <span style="white-space: nowrap">51–92&nbsp;%</span> тоже не обоснован; новый процент готовности не объявлен.</div>
</div>

</div>
</div>

<div class="source">6fcf8b9 · f9ee219 · docs/research/EXE_COVERAGE_2026-10-02.md · EXE_COVERAGE_AUDIT_2026-10-03.md</div>

<style>
.audit { font-size: 0.72rem; line-height: 1.42; color: var(--ink-2); padding: 0.6rem 0.8rem; }
.audit b { color: var(--ink); }
.audit-ico { width: 1.1rem; height: 1.1rem; color: var(--naruto); flex: none; }
</style>

<!--
Аудит на следующий день (другой агент): метрика засчитала 293 адреса из статического файла, не нашла WndProc 0x43b3d0, переданный через push, и пропустила 2 529 входов в блоки. Вывод: 47 % — ни процент реализованного кода, ни проверенная нижняя граница, интервал 51–92 % тоже не обоснован; новый процент готовности не объявлен.
-->
