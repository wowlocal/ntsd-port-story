---
layout: chapter
num: 15
total: 15
kicker: Эпилог
dates: 3 — 7 октября
image: /img/stage-1-1-background.jpg
stats: 84 часа одной сессии · паспорт 3 → 7 октября · десять уроков
---

# Уроки

Релиз 3 октября не стал концом. За четыре дня та же игра заработала на девяти хостах и на бюджетном телефоне с 2,8 ГБ памяти, а методика выдержала новые платформы и добавила два урока.

---

<Kicker>агент в цикле · 3 октября, 20:08 → 7 октября, 08:23</Kicker>

# 84 часа одной сессии

<LoopStrip class="mt-1" />

<div class="grid grid-cols-6 gap-3 mt-2">
<StatTile :value="3673" label="запроса основного потока" sub="ещё 1 376 — у 50 субагентов" size="sm" />
<StatTile value="1,86 млрд" label="токенов прочитано" sub="контекст до 966 тыс. в запросе" size="sm" accent="var(--s2)" />
<StatTile :value="6" label="сжатий контекста" sub="агент «выдыхал» и продолжал" size="sm" accent="var(--ink-2)" />
<StatTile :value="65" label="запусков /loop" sub="217 запланированных пробуждений" size="sm" accent="var(--s3)" />
<StatTile :value="23" label="реплики человека" sub="за 84 часа" size="sm" accent="var(--s1)" />
<StatTile :value="0" label="отказов модели" sub="ни одного stop_reason refusal" size="sm" accent="var(--good)" />
</div>

<div class="source">журнал сессии Claude Code 1f9218ae: только время, счётчики токенов и типы сообщений · scripts/collect_loop.py · data/loop.json · коммиты — git log 74be317..8840eb3</div>

<!--
Один и тот же разговор с агентом шёл 84 часа: от вставленного человеком обзора архитектуры до перестройки ядра под телефон. Линия — размер контекста каждого запроса; белые точки — шесть автоматических сжатий. Ниже три дорожки: коммиты, запуски /loop (цикл сам будил агента) и реплики человека.
Две плотные пачки синих точек — iPad вечером 4 октября и решения утром 5-го. Утром 6 октября человек вернулся с вопросом «the phone is available? agent is not blocked?» — агент неверно считал телефон занятым: на нём была только блокировка свайпом. Человек попросил записать это в AGENTS.md — так появился раздел Test devices.
-->

---

<Kicker>паспорт проекта · 3 октября 16:18 → 7 октября 08:23</Kicker>

# Четыре дня в цифрах

<PassportDelta class="mt-4" />

<div class="grid grid-cols-2 gap-6 mt-6 small ink2">
<div><b class="ink">Те же определения, что в главе 10.</b> Строки, тесты и файлы считаются тем же скриптом на двух коммитах: fc959db — на нём посчитана первая часть деки, и 8840eb3 — голова ветки exp/core-realtime.</div>
<div><b class="ink">Ветка не слита.</b> 137 коммитов после main живут на dev/crossplatform и exp/core-realtime: CI не включён, release-APK не опубликован, ручной игры на телефоне ещё не было.</div>
</div>

<div class="source">scripts/collect_xplat.py (паспорт fc959db и 8840eb3) · crossplatform-matrix-20261005-speed.json · CURRENT_WORK.md (память) · rt-measurement-20261006.json (Galaxy A12) · data/loop.json</div>

<!--
Полосы: тёмная часть — что было 3 октября, оранжевая — что добавили четыре дня. У памяти наоборот: зелёная часть — сколько осталось, штриховка — сколько ушло.
Строк Swift в игре прибавилось 5 078: общий рантайм, хосты и перестройка ядра под телефон. Тестов — 42. Evidence-файлов — 122, из них 32 квитанции ступеней ускорения.
Скорость на телефоне — расписанный матч с настоящими часами, без звука и сети; это вычисления, а не ощущение от игры руками.
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
<div class="ls"><div class="top"><span class="i-pixelarticons-shield" /><i class="pixel">06</i></div><b>Отказ модели не обходят — и не раздувают</b><p>остановиться, записать, продолжать независимую работу</p><em>за 84 часа сессии — ни одного отказа</em></div>
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
6. Отказ модели не обходят — и не раздувают. В журнале четырёхдневной сессии нет ни одного ответа, остановленного отказом.
7. Целое — не сумма частей. Переносимые тесты прошли на Linux, а матрица целых сценариев нашла и запись, и баг компилятора.
8. Правила — не журнал. Агент неверно считал телефон занятым; человек попросил записать в AGENTS.md, что у тестового телефона только блокировка свайпом.
9. Стенд — не железо. На Mac лишние гигабайты незаметны. Galaxy A12 с 2,8 ГБ убил игру на загрузке, и только это запустило работу над памятью: 3,9 → 1,5 ГБ без изменения игры.
10. Когда выигрыш тонет в шуме — спросить. Восемь локальных шагов ускорения дали 5,4 → 10,2 тика в секунду; восьмой — в пределах шума. Агент остановил цикл и попросил решение. Человек: «make an experimental branch and do core redesign for real time play on slow phones like A12».
-->

---

<Kicker>весь маршрут · 31 марта — 7 октября</Kicker>

# Маршрут пройден

<MetroMap class="mt-2" :visited="15" :current="15" />

<div class="source">даты и цифры — с обложек глав · цвет линии — автор коммитов: git log, трейлер Co-Authored-By</div>

<!--
Та же карта, что в начале: все пятнадцать станций пройдены. Пунктир дальше — ветка exp/core-realtime: ярус 16 мс на тик, игра руками на телефоне и слияние.
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
