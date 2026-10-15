---
layout: chapter
num: 19
total: 19
kicker: Эпилог
dates: 3 — 13 октября
image: /img/stage-1-1-background.jpg
stats: 241 час одной сессии · 155 коммитов за неделю · паспорт 3 → 13 октября · десять уроков
---

# Уроки

Релиз 3 октября не стал концом. За десять дней одна сессия агента довела ту же игру до девяти хостов, телефона, телевизора и браузера, а человек управлял ею парой строк в день.

---

<Kicker>агент в цикле · 3 октября, 20:08 → 13 октября, 21:15</Kicker>

# 241 час одной сессии

<SessionSpan class="mt-1" />

<div class="grid grid-cols-6 gap-3 mt-2">
<StatTile :value="9073" label="запроса основного потока" sub="ещё 4 346 — у 160 субагентов" size="sm" />
<StatTile value="4,57 млрд" label="токенов прочитано" sub="контекст до 967 тыс. в запросе" size="sm" accent="var(--s2)" />
<StatTile :value="18" label="сжатий контекста" sub="агент «выдыхал» и продолжал" size="sm" accent="var(--ink-2)" />
<StatTile :value="164" label="запуска /loop" sub="587 запланированных пробуждений" size="sm" accent="var(--s3)" />
<StatTile :value="56" label="реплик человека" sub="за десять дней" size="sm" accent="var(--s1)" />
<StatTile :value="0" label="отказов модели" sub="и 3 обрыва сети в ночь на 12 октября" size="sm" accent="var(--good)" />
</div>

<div class="source">журнал сессии Claude Code 1f9218ae: только время, счётчики токенов и типы сообщений · scripts/collect_epilogue.py · data/epilogue.json · data/loop.json · коммиты — git log 74be317..5f5a8ee4</div>

<!--
Один и тот же разговор с агентом шёл 241 час: от вставленного человеком обзора архитектуры 3 октября до релиза и джойстика 13-го. Линия — размер контекста каждого третьего запроса и пики перед сжатием; белые точки — 18 автоматических сжатий. Ниже три дорожки: коммиты, запуски /loop (цикл сам будил агента) и реплики человека. Наведите на полосу главы сверху — останутся только её события.
7 октября компьютер перезагрузился сам: «resume. computer crashed and restarted for some reason» — и сессия продолжилась с того же места. В ночь на 12 октября трижды пропадал интернет.
-->

---

<Kicker>неделя после 7 октября · 154 коммита и одно слияние · 14 реплик, которые всё повернули</Kicker>

# Строка человека — ветка агента

<WeekLanes class="mt-1" />

<div class="source">git log 8840eb3..5f5a8ee4 (без слияний) · тема — по тегу в заголовке коммита · реплики — журнал сессии 1f9218ae, дословно · scripts/collect_epilogue.py · data/epilogue.json</div>

<!--
Нажмите на синюю точку — внизу появится реплика человека; нажмите на название темы — останется только её дорожка; наведите на точку коммита — его заголовок.
Ритм недели: одна строка человека — и следующие сутки агент сам ведёт ветку, меряет, откатывает и коммитит. 151 из 154 коммитов — с трейлером Claude, у слияния он тоже есть; три коммита релиза 13 октября сделаны без него, внутри сессии Codex (глава 18).
-->

---

<Kicker>паспорт проекта · 3 октября 16:18 → 13 октября 20:14</Kicker>

# Десять дней в цифрах

<PassportDelta class="mt-4" />

<div class="grid grid-cols-2 gap-6 mt-6 small ink2">
<div><b class="ink">Те же определения, что в главе 10.</b> Строки, тесты и файлы считаются тем же способом на двух коммитах: fc959db — на нём посчитана первая часть деки, и 5f5a8ee4 — голова ветки exp/iphone, в которой main, релиз и джойстик.</div>
<div><b class="ink">Новые хосты — стенды.</b> Apple TV и iPhone проверены в симуляторах, браузеры — в headless Chromium и WebKit, WASI — в Node. Телефонные цифры — один Galaxy A12, расписанный матч, отладочная сборка.</div>
</div>

<div class="source">scripts/collect_epilogue.py (паспорт fc959db и 5f5a8ee4) · data/web_hosts.json · data/rt2_steps.json · data/loading_race.json · data/loading_steps.json · data/epilogue.json</div>

<!--
Полосы: тёмная часть — что было 3 октября, оранжевая — что добавили десять дней. У телефонных плиток наоборот: зелёная часть — сколько осталось, штриховка — сколько ушло; «было» для них — первый замер на телефоне, 7 и 10 октября: 3 октября игра на нём ещё не запускалась.
Строк Swift в игре прибавилось 9 777: общий рантайм, хосты, перестройка ядра, веб-хост. Тестов — 141. Evidence-файлов — 262.
-->

---

<Kicker>методология в десяти строках</Kicker>

# Что стоит унести с собой

<div class="lessons grid grid-cols-5 gap-3 mt-3">
<div class="ls"><div class="top"><span class="i-pixelarticons-lock" /><i class="pixel">01</i></div><b>Один эталон, неизменяемые ожидания</b><p>ни одно expected не переписывали под код</p><em>девять хостов сверены с теми же замороженными прогонами</em></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-checklist" /><i class="pixel">02</i></div><b>У каждого утверждения — класс доказательства</b><p>статика, вывод, сравнение, настоящий рантайм</p><em>контейнер, CrossOver и симулятор названы стендом, а не платформой</em></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-robot" /><i class="pixel">03</i></div><b>Оракул может разделять вашу ошибку</b><p>контрольная сумма совпадала с Unicorn — и была неверной</p><em>ошибся и компилятор: Static Linux SDK терял запись в слот</em></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-git-merge" /><i class="pixel">04</i></div><b>Проверка без интеграции — тоже долг</b><p>после успешного сравнения — перенос в <code>native/</code></p><em>каждая ступень ускорения — коммит с замером на телефоне или откат</em></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-archive" /><i class="pixel">05</i></div><b>Провал — это артефакт</b><p>assertion, гарды памяти и таймауты сохраняются</p><em>падение записи, отмеченное на main, оказалось указателем Git LFS</em></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-shield" /><i class="pixel">06</i></div><b>Отказ модели не обходят — и не раздувают</b><p>остановиться, записать, продолжать независимую работу</p><em>за 241 час сессии — ни одного отказа</em></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-tournament" /><i class="pixel">07</i></div><b>Целое — не сумма частей</b><p>692 теста и 215 оракулов не заменили 58 целых матчей</p><em>581 тест на Linux прошёл, а запись падала только в целом прогоне</em></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-book-open" /><i class="pixel">08</i></div><b>Правила — не журнал</b><p>инструкции отдельно, статус отдельно</p><em>«у тестового телефона нет PIN» — правило в AGENTS.md, а не строка в журнале</em></div>
<div class="ls new"><div class="top"><span class="i-pixelarticons-device-phone" /><i class="pixel">09</i></div><b>Стенд — не железо</b><p>девять стендов не заметили лишние 2,5 ГБ памяти</p><em>первый же телефон убил игру на загрузке</em></div>
<div class="ls new"><div class="top"><span class="i-pixelarticons-human-handsup" /><i class="pixel">10</i></div><b>Когда выигрыш тонет в шуме — спросить</b><p>шаг 8 корректен, но не быстрее: агент поставил паузу</p><em>человек выбрал перестройку ядра на отдельной ветке</em></div>
</div>

<div class="xsmall muted mt-2"><span class="em-key" />после релиза, 3–7 октября · <span class="new-key" />новые уроки</div>

<style>
.lessons { row-gap: 0.7rem; }
.lessons .ls { position: relative; background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: 0.7rem 0.7rem 0.75rem; overflow: hidden; display: flex; flex-direction: column; }
.lessons .ls::before { content: ''; position: absolute; left: 0; top: 0; height: 3px; width: 42px; background: var(--naruto); }
.lessons .ls.new { border-color: rgba(108, 182, 255, 0.4); }
.lessons .ls.new::before { background: var(--chakra); width: 100%; }
.lessons .top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.45rem; }
.lessons .top span { width: 1.45rem; height: 1.45rem; color: var(--naruto); }
.lessons .ls.new .top span { color: var(--chakra); }
.lessons .top i { font-style: normal; font-size: 0.7rem; color: var(--muted); }
.lessons b { display: block; font-size: 0.76rem; line-height: 1.22; color: var(--ink); font-weight: 700; }
.lessons p { font-size: 0.62rem; line-height: 1.35; color: var(--ink-2); margin: 0.35rem 0 0; flex: 1; }
.lessons em { display: block; font-style: normal; font-size: 0.6rem; line-height: 1.32; color: var(--ink); margin-top: 0.45rem; padding-top: 0.4rem; border-top: 1px dashed var(--axis); }
.lessons em::before { content: '→ '; color: var(--naruto); }
.lessons .ls.new em::before { color: var(--chakra); }
.em-key, .new-key { display: inline-block; width: 18px; height: 3px; vertical-align: middle; margin: 0 0.35rem 0 0.2rem; background: var(--naruto); }
.new-key { background: var(--chakra); margin-left: 0.6rem; }
</style>

<!--
Десять уроков полностью. Строка под чертой — чем их подтвердили или дополнили четыре дня после релиза.
1. Один эталон, неизменяемые ожидания. Ни одно expected не переписывали под код. На новых платформах правило звучало так: «A difference on a new platform is a recorded mismatch, never a regenerated expected value».
2. У каждого утверждения — класс доказательства. Контейнеры, CrossOver, симулятор и эмулятор названы стендами; отчёт с iPad записан как наблюдение человека без замеров.
3. Оракул может разделять вашу ошибку. В первой части — Unicorn, теперь — компилятор: Static Linux SDK Swift 6.4.0 выбрасывал запись узла в слот перед isKnownUniquelyReferenced. Отчёт swiftlang/swift#92905 закрыт исправлением.
4. Проверка без интеграции — тоже долг. Правило ветки ускорения: коммит, только если на телефоне измеримо быстрее или строго меньше работы без лишней сложности; иначе записать и откатить.
5. Провал — это артефакт. Падение сценария playback записали ещё на main 3 октября; через два дня причина нашлась: в рабочем дереве лежал 130-байтовый указатель Git LFS.
6. Отказ модели не обходят — и не раздувают. В журнале десятидневной сессии нет ни одного ответа, остановленного отказом; три сбоя за 241 час — это обрывы сети.
7. Целое — не сумма частей. Переносимые тесты прошли на Linux, а матрица целых сценариев нашла и запись, и баг компилятора.
8. Правила — не журнал. Агент неверно считал телефон занятым; человек попросил записать в AGENTS.md, что у тестового телефона только блокировка свайпом.
9. Стенд — не железо. На Mac лишние гигабайты незаметны. Galaxy A12 с 2,8 ГБ убил игру на загрузке, и только это запустило работу над памятью: 3,9 → 1,5 ГБ без изменения игры.
10. Когда выигрыш тонет в шуме — спросить. Восемь локальных шагов ускорения дали 5,4 → 10,2 тика в секунду; восьмой — в пределах шума. Агент остановил цикл и попросил решение. Человек: «make an experimental branch and do core redesign for real time play on slow phones like A12».
-->

---

<Kicker>весь маршрут · 31 марта — 13 октября</Kicker>

# Маршрут пройден

<MetroMap class="mt-2" :visited="19" :current="19" />

<div class="source">даты и цифры — с обложек глав · цвет линии — автор коммитов: git log, трейлер Co-Authored-By</div>

<!--
Та же карта, что в начале: все девятнадцать станций пройдены. Пунктир дальше — то, что ждёт решения автора: ветка exp/iphone и публикация веб-версии.
-->

---
layout: hero
image: /img/covers/end-valley-of-the-end.jpg
align: center
shade: 0.7
---

<div class="flex flex-col items-center">
<div class="flex items-end gap-6 mb-3">
<Sprite src="/img/sprites/naruto-rasengan-4x.png" :scale="0.6" float />
<Sprite src="/img/sprites/sasuke-chidori-4x.png" :scale="0.6" flip float />
</div>
<Kicker>конец · спасибо</Kicker>
<h1 class="cover-title">Один EXE.<br><span class="hl">Одна и та же игра.</span></h1>
<p class="small ink" style="max-width: 40rem; margin-top: -0.3rem">На Mac, Linux, Windows, iPad и Android — с одними эталонами.</p>
<p class="small ink2" style="max-width: 40rem">Порт и релиз v0.4.0: <span class="mono">github.com/wowlocal/ntsd-2.4</span> · эта презентация: <span class="mono">github.com/wowlocal/ntsd-port-story</span></p>
<p class="xsmall muted" style="max-width: 38rem"><i>Naruto: The Setting Dawn</i> — фанатская игра её авторов на движке <i>Little Fighter 2</i> Марти Вонга и Старски Вонга. Права на контент принадлежат авторам; изображения использованы для рассказа о проекте сохранения игры. Оригинал в эталонных проверках — под CrossOver; отдельные функции — в Unicorn Engine.</p>
</div>

<style>
.cover-title { font-size: 2.8rem !important; line-height: 1.08 !important; margin: 0.3rem 0 0.8rem !important; text-align: center; }
</style>

<!--
Фон — сцена Valley_of_the_End из оригинального дистрибутива (bg/sys/Valley): слои собраны по её bg.dat, кадр водопада — первый из анимации.
-->
