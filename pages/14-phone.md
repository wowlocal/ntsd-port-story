---
layout: chapter
num: 14
total: 15
kicker: Глава четырнадцатая
dates: 5 — 7 октября
image: /img/covers/ch14-phone.svg
imagePixel: false
stats: 4 → 1,5 ГБ · 30,25 тика/с с настоящими часами · 30 ступеней с квитанциями
---

# Телефон 2008 года

Игре нужно 4 ГБ, у Galaxy A12 — 2,8. Автор решил: по мощности A12 — как средний компьютер 2008 года, значит, игра обязана на нём идти. И идти точно так же.

<div class="cover-note">Обложка — рисунок: кадр Demo из приложения в контуре телефона, не фотография.</div>

<style>
.cover-note { margin-top: 0.7rem; font-size: 0.66rem; color: var(--muted); }
</style>

<!--
Глава о трёх днях, 5–7 октября. Пользователь подключил к Mac свой тестовый телефон — Samsung Galaxy A12 (SM-A125F, Helio P35, Cortex-A53, Android 12, 720×1600, MemTotal 2 809 044 кБ). Ветка exp/core-realtime; все цифры главы заморожены на коммите 8840eb3, 7 октября, 08:23.

Обложка: рисунок, а не фото. Экран 20:9, окно игры 794×550 стоит по центру с чёрными полями — так его показывает хост Android: он сообщает игре «рабочий стол» не меньше 800×600 в пропорциях устройства (36e7e8e).
-->

---
clicks: 1
---

<Kicker>5 октября, 07:42 · Galaxy A12 подключён по USB</Kicker>

# Игре нужно 4 ГБ, у телефона — 2,8

<div class="chart-h">живая куча macOS-сборки на пике прогона VS — 3 932 МиБ, по стекам выделения памяти</div>

<PhoneHeapBar stepwise />

<div class="grid grid-cols-[1fr_1.08fr] gap-6 mt-2">
<div>

<div class="kill">
<div class="kbar"><span class="i-pixelarticons-android kico" />adb logcat · lmkd</div>
<div class="kbody mono">Reclaim local.ntsd.port ... to free 1311324kB rss, 2493324kB swap; reason: device is low on swap (0kB &lt; 786428kB) and thrashing (272%)</div>
<div class="kfoot">затем <b>signal 9</b> — ещё на загрузке. Резидентно 1,3 ГБ, свободно ≈ 50 МБ.</div>
</div>

<p class="small ink2 mt-3 mb-0" style="line-height: 1.4">На macOS тот же сценарий доходил до 4,17 ГБ — почти всё обычная куча: из файлов отображено лишь 35 МБ. Данные игры копировались в память.</p>

</div>
<div>

<PhoneChat :messages="[
  { who: 'agent', time: '07:42', text: 'I tried the game on your phone: it installs and starts, but with its current memory use <b>it can’t finish loading on this phone.</b>', gloss: 'ставится и запускается, но догрузиться не может' },
  { who: 'event', time: '07:45', text: '<code>1dbaacb</code> · только замер: куда уходит память' },
  { who: 'agent', time: '07:50', text: '<b>Main question: should I make the game fit in less memory?</b>' },
  { who: 'human', time: '07:51', text: '1. yes you should make th egame fit in less memory.', gloss: 'да, уложи игру в меньший объём', hot: true },
]" />

</div>
</div>

<div class="source">crossplatform-p8-android-phone-20261005.json · crossplatform-memory-attribution-20261005.json · footprint-20261005.json · 36e7e8e · 1dbaacb · сессия 1f9218ae (время местное, UTC+2) · data/perf_memory.json</div>

<style>
.chart-h { font-size: .68rem; color: var(--muted); margin-bottom: .1rem; }
.kill { background: #0c1017; border: 1px solid rgba(255,255,255,.1); border-radius: 10px; overflow: hidden; }
.kbar { display: flex; align-items: center; gap: .4rem; font-size: .64rem; color: var(--muted); background: #161b25; border-bottom: 1px solid rgba(255,255,255,.06); padding: .22rem .6rem; font-family: var(--font-mono); }
.kico { width: .9rem; height: .9rem; color: var(--s3); }
.kbody { font-size: .66rem; line-height: 1.45; color: #ffb4a8; padding: .45rem .7rem .2rem; }
.kfoot { font-size: .68rem; color: var(--ink-2); padding: .1rem .7rem .5rem; }
.kfoot b { color: var(--ink); }
</style>

<!--
Клик показывает белую линию: вся оперативная память телефона, 2 743 МиБ по MemTotal. Одни только копии картинок больше неё.

Полоса — живая куча macOS-сборки на пике прогона VS: 3 932 МиБ (3,84 ГиБ), разложенные malloc_history по стекам выделения. Каждую картинку порт держал трижды: байтами файла (666 МиБ), декодированными цветами с байтом определённости на пиксель (1 041 МиБ) и 32-битными пикселями поверхности дисплея (1 113 МиБ), плюс маска «known» — по байту на пиксель (283 МиБ). Вместе 3 103 МиБ, 79 % кучи.

Первой находкой на телефоне был экран: хост сообщил игре 853×384 dp, окно 794×550 встало на y = −83, и первый blit был отвергнут. Хост теперь сообщает не меньше 800×600 — «рабочий стол», под который делали оригинал (36e7e8e). Батарея телефона в тот момент была на 8 %.

Переписка — из журнала сессии Claude Code 1f9218ae; время местное. Опечатка «th egame» — авторская.
-->

---

<Kicker>5 октября, 08:57–11:24 · три правки хранения</Kicker>

# Три правки — и матч доигран

<MemorySteps class="mt-1" />

<div class="grid grid-cols-4 gap-3 mt-4">
<StatTile value="668 с" label="расписанный матч VS на телефоне — до конца" sub="состояние равно эталону; в эмуляторе — 95 с" size="sm" accent="var(--good)" />
<StatTile :value="1832" label="кадра матча — те же, что в эмуляторе" sub="текст включительно" size="sm" accent="var(--good)" />
<StatTile value="1,26 ГБ" label="пик резидентной памяти телефона" sub="lmkd больше не приходит" size="sm" accent="var(--s1)" />
<StatTile value="5,4" label="тика в секунду" sub="у оригинала ≈ 30: играть ещё нельзя" size="sm" accent="var(--warning)" />
</div>

<div class="source">crossplatform-memory-step1/2/3-20261005.json · docs/research/MEMORY_FOOTPRINT.md · 2289ad0 · 58bb8cc · 109304a · data/perf_memory.json</div>

<!--
Правило карточки M1: «Game result: unchanged by definition: only how the native port holds data changes, never what the game computes or shows». Каждая правка: релизная сборка, тесты, сравнение кадров headless и AppKit, новый замер памяти, независимое ревью — и только потом коммит.

Метрики разные, поэтому карточки не соединены в одну линию. Шаги 1–2 мерили живую кучу (heap -s на 40-й секунде), шаг 3 — резидентную (vmmap, dirty + swapped). Footprint macOS для сравнения не годился: на одинаковых прогонах он плавал от 1,4 до 3,1 ГБ.

На телефоне: главное меню через 13 с, загрузка после START — около 165 с. Шаг 3b (лишняя копия байтов файла, до ~0,6 ГБ) оставлен в очереди: память перестала быть пределом, пределом стала скорость.
-->

---

<Kicker>5 октября, 12:33 — 6 октября, 05:48</Kicker>

# Восемь правок — и стена

<div class="grid grid-cols-[1.02fr_1fr] gap-6 mt-1">
<div>

<div class="chart-h">тики в секунду на Galaxy A12 после каждой правки</div>

<LocalSteps />

<p class="xsmall ink2 mt-2 mb-0" style="line-height: 1.4">Самый большой шаг — <b>3</b>: каждый тик работает на копии состояния, чтобы откатить неудачный, и запись пакета повтора дублировала весь буфер записи в 6,5 МБ. Теперь копируется одна страница из 16 КиБ.</p>

</div>
<div>

<PhoneChat :messages="[
  { who: 'agent', time: '6 окт, 01:19', text: '<b>Why I stopped:</b> the last speed fix made no measurable difference. To get from 10 to about 30 ticks per second on the A12, the game would need a redesign of how it copies its state every tick. That’s a large change to the core code, so it’s your call.', gloss: 'последняя правка ничего не дала; до 30 тиков нужен редизайн копирования состояния — решать вам' },
  { who: 'human', time: '05:46', text: 'make an experimental branch and do core redesign for real time play on slow phones like A12. Original game was published at 2008 and Samsung A12 has comparable performance GPU/CPU to the average computers at that time. start the core redesign loop', gloss: 'игра вышла в 2008-м, а A12 по CPU и GPU — как средний компьютер того времени', hot: true },
  { who: 'event', time: '05:48', text: '<code>36edf83</code> · ветка exp/core-realtime и карточка исследования' },
]" />

</div>
</div>

<div class="source">docs/research/MOBILE_PERFORMANCE.md · crossplatform-speed-*.json · accefc6 · f378a0d · 791ad85 · 0667838 · 0b5e9f7 · 870c24a · c8177d7 · 9df1054 · сессия 1f9218ae (UTC+2) · data/perf_local.json</div>

<style>
.chart-h { font-size: .68rem; color: var(--muted); margin-bottom: .1rem; }
</style>

<!--
Шаги по порядку: 1–2 — экран больше не сканируется на «неизвестные» пиксели дважды на каждый blit (проверка, которую любой хост выключает), 5,4 → 7,6. Шаг 3 — буфер повтора страницами, 7,6 → 8,8. 4–5 — копирование спрайтов по строкам и биты маски словами по 64, 9,3. 6 — диапазоны адресов в локальном массиве: проверки эксклюзивности (медленный TLS на Android) с 5,4 до 1,6 % сэмплов, 9,4. 6b — токены звука без склейки трёх списков, 9,9. 7 — целые строки экрана одним блоком, 10,2. 8 — запись меню на месте: 10,2 → 10,1, «в пределах шума».

Временная проба copy-on-write на macOS до шага 3 показала масштаб: за один матч буфер записи повтора (6,5 МБ) копировался 1 659 раз — ≈ 21,5 ГБ; записи актёров — 2,9 млн копий, ≈ 6,2 ГБ; записи ресурсов битмапов — 363 000 копий, ≈ 5,8 ГБ; глобальные переменные — 28 000 копий, ≈ 2,6 ГБ.

Чего агент не сделал без автора: собрать Android с -enforce-exclusivity=unchecked. Это сняло бы последние проценты, но убрало бы проверку безопасности во время выполнения — «the user’s call».

В том же сообщении в 01:19 агент перечислил решения, которые ждут автора, второе из них: «Redesign the core for real-time play on slow phones like the A12, or treat the A12 as below the minimum?»
-->

---

<Kicker>6 октября, 05:58 · старт ветки: 10,07 тика/с</Kicker>

# До редизайна тик тонул в копиях

<div class="grid grid-cols-[1.08fr_1fr] gap-7 mt-1">
<div>

<div class="chart-h">профиль телефона: доля сэмплов, включительно · simpleperf, 30 с, 24 318 сэмплов</div>

<ProfileBars />

</div>
<div>

<div class="chart-h">один тик, как он был устроен</div>

<TickFlow />

</div>
</div>

<div class="source">rt-baseline-20261006.json (35ec7a3) · docs/research/CORE_REALTIME_DATAFLOW.md · CORE_REALTIME_M2.md · CORE_REALTIME_COPIES.md · data/perf_profile.json</div>

<style>
.chart-h { font-size: .68rem; color: var(--muted); margin-bottom: .25rem; }
</style>

<!--
Доли включительные, поэтому они перекрываются: тело игрового тика (11,4 %) входит в игровую сессию (17,3 %). Складывать их нельзя. Доли «на вершине стека» не пересекаются: memcpy 16,1 %, retain 7,6 %, release 7,0 %, атомики 3,9 % — вместе 34,6 %.

Сама логика оригинала — тело тика — занимала около девятой части времени. Остальное — обвязка порта: попытки Host, перевод 400 актёров между состоянием сессии и моделью матча дважды за тик, копии для отката и всё рисование на главном потоке.

Карта потока данных сделана отдельным агентом только для чтения (CORE_REALTIME_DATAFLOW.md). Числа на плашках — из заметок M2 и COPIES; «≈ 600 КБ копий» и «~40 копий данных сессии за тик, ~10 000 пар retain/release» — оценки по полям, не замеры.
-->

---
clicks: 1
---

<Kicker>6 октября, 10:37 — 7 октября, 02:27 · фазы 1c–1i</Kicker>

# Пиксели — в свой поток

<p class="small ink2 lead" style="line-height: 1.4">Ядро только записывает, что нарисовать, и никогда не читает пиксели обратно. Значит, их можно отдать второму ядру процессора: у A12 их восемь, работало одно.</p>

<RenderLanes stepwise />

<div class="source">docs/research/CORE_REALTIME_RENDER.md · rt-1c-render-pipelining · rt-1e-pipelined-text · rt-1g-known-flag · rt-1i-crop-buffers · data/perf_ladder.json</div>

<style>
.lead { margin: -0.4rem 0 0.35rem !important; max-width: 52rem; }
</style>

<!--
Клик показывает схему «после». Не в масштабе.

Фаза A на главном потоке ровно там же, где раньше: проверки, метаданные, ошибки — в том же тике и в том же порядке. Фаза B на одном последовательном потоке рендера: пиксели, crop, вывод в окно. Не больше одного батча в полёте; перед любым чтением пикселей, снимком, выходом — flush. AppKit, iOS и SDL остаются синхронными, флаг --synchronous-render выключает конвейер.

Проверки: все 10 сценариев с дайджестами кадров и с полным перекрытием, ThreadSanitizer — 0 предупреждений, независимое ревью — «OK после четырёх исправлений».

1e — самый большой шаг всей ветки: каждый шаг вывода текста делал flush очереди рендера, и на Mac 20 % занятости главного потока было ожиданием. 1g — флаг «все пиксели известны»: работа с маской занимала 13,9 % сэмплов потока рендера. 1i — каждый кадр выделял и обнулял новый буфер crop на 1,75 МБ; теперь три буфера по кругу. Попытка 1h — копии с ключом по 4 пикселя (SIMD) — выигрыша не дала: поток рендера упирается в пропускную способность памяти. Откатили.
-->

---
clicks: 1
---

<Kicker>6 октября, 20:15 — 22:42 · 4c3ea6f</Kicker>

# Часы, которые спали за игру

<TickClock stepwise />

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-1">
<div>

<div class="hatch-key"><i class="hk" />сон таймера оригинала: Sleep ≤ 5 мс, пока игра впереди графика</div>

<div class="grid grid-cols-3 gap-2 mt-2">
<StatTile value="37 %" label="времени главный поток вне CPU" sub="сборка 4f, 20 с записи" size="sm" />
<StatTile value="99,8 %" label="из них — ожидание в Looper::pollOnce" sub="главный цикл Android" size="sm" accent="var(--s1)" />
<StatTile value="5,14 мс" label="медиана одного ожидания" sub="1 316 из 1 785 — по 4–6 мс" size="sm" accent="var(--s1)" />
</div>

</div>
<div>

<PhoneChat :messages="[
  { who: 'human', time: '20:15', text: 'keep going. I want 8ms per frame on the A12. starting from 33ms per frame, them we should strive to 16ms, then to 8ms', gloss: 'цель — 8 мс на кадр: сначала 33, потом 16, потом 8', hot: true },
  { who: 'event', time: '22:42', text: 'метрика — время работы потока на тик · ярус 33 мс выполнен' },
]" />

</div>
</div>

<div class="source">rt-measurement-20261006.json · docs/research/CORE_REALTIME_BUDGET.md · OriginalApplicationTimer (EXE 43d157..43d1ef) · сессия 1f9218ae (UTC+2) · data/perf_budget.json</div>

<style>
.hatch-key { display: flex; align-items: center; gap: .45rem; font-size: .66rem; color: var(--ink-2); }
.hk { width: 16px; height: 11px; border-radius: 2px; flex: none; background: repeating-linear-gradient(45deg, #4a5366 0 2px, #262d3c 2px 5px); }
</style>

<!--
Клик добавляет вторую строку — тот же матч с настоящими часами.

Шаг 4e убрал 3,6 пункта сэмплов главного потока, а тиков в секунду прибавилось на 1 %. Профиль вне CPU объяснил: 37 % времени главный поток ждал, 99,8 % этого ожидания — в главном цикле Android по ~5 мс. Это собственный темп оригинала: таймер на 33 мс, и пока игра впереди, она спит кусками не длиннее 5 мс. Харнесс шёл на виртуальных часах — 8 мс на итерацию цикла сообщений, — поэтому в каждом тике было ~4 итерации, три из них холостые с настоящим сном по 5 мс: ~16 мс сна при любой скорости вычислений.

Харнесс научился мерить время работы каждого потока на тик (schedstat) и запускаться с настоящими часами. На сборке 4f: главный 30,4 мс и рендер 22,2 мс на тик; с настоящими часами матч идёт 30,25 тика в секунду — темп самого оригинала (не больше 30,3).

Сама карточка бюджета тоже была исправлена в тот же вечер: «The first version of this note counted wall time per tick … That includes ~16 ms of the game’s own sleeping and could never reach 8 ms; superseded the same evening».

Цели автора — из сообщения в очереди сессии в 20:15; опечатка «them» — авторская.
-->

---
clicks: 1
---

<Kicker>6 октября, 05:58 — 7 октября, 08:23 · 30 ступеней</Kicker>

# Лестница редизайна

<RedesignLadder stepwise class="mt-1" />

<div class="source">docs/research/CORE_REALTIME.md (реестр) · docs/evidence/rt-*.json · 35ec7a3 … 8840eb3 · среднее прогонов каждой ступени · состояние на 7 октября, 08:23 · data/perf_ladder.json</div>

<!--
Клик показывает панель Б.

Каждая точка — строка реестра CORE_REALTIME.md и её evidence-файл; значение — среднее прогонов телефона на этой ступени. Правило коммита: быстрее на телефоне или строго меньше работы без лишней сложности; иначе записать результат и откатить. Поэтому на лестнице есть ступени «в пределах шума»: 4b, 4c, M2b, 4g, первая часть B1.

Панель А — тики в секунду на часах харнесса от старта ветки до 4f: 10,07 → 20,4. Крупнейшие ступени: 1e +17 % (текст не ждёт рендер), R3 +14 % (400 актёров держатся в форме модели матча между тиками, а не переводятся дважды за тик), 4a +8 % (данные загруженной сессии — один общий объект вместо ~250 ссылок на копию), 2b +7 %, 1c +6 %.

Панель Б — миллисекунды работы на тик с 4f: главный поток 30,4 → 24,6 мс, рендер 22,2 → 18,1 мс. Оценки дизайна и факт расходились: A1 обещал ~3 мс, дал ~1; B1 3b — 1,2–2,2 мс, дал ~0,8; 4j дал вдвое больше оценки. Кольца — откаченные попытки: 1h (SIMD-копии, рендер без выигрыша) и первая версия 3a (лишнее поле сделало каждую запись 48 байт вместо 40 и стоило около 1 мс на тик).

Последняя ступень, 4k, — флаг компилятора cross-module optimization: обобщённый код Host и сессий стал специализированным, −1 мс на тик, бинарник +5,5 %.
-->

---

<Kicker>каждая ступень · из её собственного evidence-файла</Kicker>

# Та же игра после каждой ступени

<GateGrid class="mt-1" />

<div class="gate-legend">
<span><i class="g pass" />записано как пройденное</span>
<span><i class="g na" />не требовалось: изменение только для Android, не про потоки, или по правилу карточки</span>
<span><i class="g none" />нет в evidence</span>
</div>

<div class="grid grid-cols-[1.25fr_1fr] gap-4 mt-3">
<div class="card-soft small ink2">
<div class="pixel hl xsmall mb-1">правило коммита</div>
<span class="mono xsmall ink" lang="en">«Commit an increment only when every gate passes and it is either measurably faster or strictly less work without added complexity; otherwise record the result here and revert.»</span>
</div>
<div class="card-soft small ink2">
<div class="pixel hl xsmall mb-1">чего здесь нет</div>
Полную матрицу «9 хостов × 10 сценариев» прогнали 5 октября на <code>870c24a</code>, до ветки. На ветке она положена в конце фазы — и ещё не запускалась.
</div>
</div>

<div class="source">docs/evidence/rt-*.json: поля gates, checks, review, phone · docs/research/CORE_REALTIME.md (Gates) · crossplatform-matrix-20261005-speed.json · data/perf_gates.json</div>

<style>
.gate-legend { display: flex; flex-wrap: wrap; gap: .3rem 1.2rem; font-size: .66rem; color: var(--ink-2); margin-top: .2rem; }
.gate-legend span { display: inline-flex; align-items: center; gap: .4rem; }
.gate-legend .g { display: inline-block; width: 11px; height: 11px; border-radius: 3px; }
.gate-legend .g.pass { background: var(--good); }
.gate-legend .g.na { border: 1.5px solid #535c70; }
.gate-legend .g.none { width: 5px; height: 5px; border-radius: 50%; background: var(--axis); }
</style>

<!--
Каждая колонка — ступень редизайна, каждая строка — проверка. Сетка собрана из evidence-файлов ступеней, а не из пересказа: если проверка там не записана, клетка пустая.

Что видно: headless-матч с 1 832 кадрами, 10 сценариев и AppKit с 3 960 кадрами — на каждой ступени, кроме 1a (правка только в хосте Android, проверена эмулятором и попиксельным сравнением формулы). Эмулятор Android вошёл в обязательный набор с 1g; до этого его гоняли для 1a и 1c. ThreadSanitizer — для трёх ступеней, которые трогали потоки: 1c, 1e, 1f. Независимое ревью — у 23 ступеней; шести оно не требовалось по правилу карточки (ревью обязательно для изменений модели хранения и архитектуры), у 1a его нет.

По правилу карточки фикстуры, эталоны и ожидаемые значения не меняются: сравнение всегда с замороженными записями — m1-frames-ref, прогонами AppKit, эталонами app_e2e.
-->

---

<Kicker>состояние на 7 октября, 08:23 · 8840eb3</Kicker>

# Ярус 33 мс взят. Дальше — 16 и 8

<div class="grid grid-cols-[1.12fr_1fr] gap-6 mt-1">
<div>

<div class="chart-h">мс работы на тик, Galaxy A12 · бледная часть — где было на 4f</div>

<FrameBudget />

<div class="card-soft small ink2 mt-3" style="line-height: 1.4">Сама логика оригинала укладывается в <b class="ink">≈ 8,5 мс</b>. Путь к ярусу 2 лежит через обвязку порта: карточка яруса предлагает «прямой игровой тик» — тело игры прямо на модели матча, без пересборки попыток вокруг него.</div>

</div>
<div class="now">

<div class="blk">
<div class="bh pixel">в работе на 08:23</div>

- **4m** — продолжение загруженного цикла в одном объекте: ~380–460 ссылок на каждую копию
- **1j** — копии с ключом без битов маски: на A12 300 блитов 80×80 с ключом — 18,6 → 11,3 мс
- **A3** — холостая итерация цикла: 0,94 → ≤ 0,2 мс, план из пяти частей
- **ярус 3** — рисование на GPU, colour key в шейдере, те же пиксели, что у CPU — план

</div>

<div class="blk late">
<div class="bh pixel">закоммичено после заморозки, 08:51–08:52</div>
<code>bf5628e</code> 4m: главный 23,9 мс · <code>e3dcd6a</code> 1j: рендер 17,5 мс · там же — план убрать целые проходы по кадру, каждый стоит ≈ 1,7 мс; ничего не собрано
</div>

<div class="blk warn">
<div class="bh pixel">не доказано</div>

- игра руками на A12 — открытая ручная проверка
- один телефон, debuggable-сборка, матч по сценарию без звука и сети
- загрузка на телефоне ≈ 4,5 минуты
- ветка не слита, CI не включён, полной матрицы на ней не было

</div>

</div>
</div>

<div class="source">docs/research/CORE_REALTIME.md (Next task) · CORE_REALTIME_BUDGET.md · CORE_REALTIME_A3.md · rt-4l-pending-loading-20261007.json · после заморозки: bf5628e, e3dcd6a · data/perf_budget.json, perf_now.json</div>

<style>
.chart-h { font-size: .68rem; color: var(--muted); margin-bottom: .2rem; }
.now { display: flex; flex-direction: column; gap: .45rem; }
.now .blk { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: .4rem .7rem .45rem; font-size: .66rem; line-height: 1.35; color: var(--ink-2); }
.now .blk.late { background: rgba(255,255,255,.025); border-style: dashed; }
.now .blk.warn { border-color: rgba(250,178,25,.45); }
.now .bh { font-size: .66rem; color: var(--naruto); margin-bottom: .15rem; }
.now .blk.warn .bh { color: var(--warning); }
.now ul { margin: 0; }
.now ul > li { margin: .1rem 0; padding-left: .95rem; font-size: .66rem; line-height: 1.32; }
.now ul > li::before { top: .5em; width: 5px; height: 5px; }
.now code { font-size: .6rem !important; }
</style>

<!--
Бледные части полос — где были потоки на 4f, когда появилась метрика «работа на тик»: главный 30,4 мс, рендер 22,2 мс. Сейчас: 24,6 и 18,1. До яруса 2 главному потоку не хватает 8,6 мс, рендеру — 2,1 мс.

Нижняя полоса — профиль после B1 3b (главный 27,6 мс): обвязка ~19 мс вокруг ~8,5 мс тела игрового тика. Карточка яруса 2 предлагает «прямой игровой тик»: когда тику не нужна поездка к хосту, тело игры работает прямо на модели матча, без пересборки попыток меню и Host вокруг него — с теми же ошибками и границами при сбое.

Ярус 3 по карточке бюджета: рендер на GPU — спрайты и фоны становятся текстурами один раз, блиты — целочисленные прямоугольники с выборкой по ближайшему пикселю и проверкой colour key в шейдере, «so they can produce exactly the CPU’s pixels»; кадры для сравнения читаются обратно. Главный поток: типизированное горячее состояние, ноль выделений памяти в устойчивом тике.

После заморозки главы в 08:51 и 08:52 на ветку легли 4m (главный 24,6 → 23,9 мс) и 1j (рендер 18,1 → 17,5 мс, четверть прогноза стенда: спрайты с ключом — меньшая доля работы рендера, чем 300 спрайтов стенда). Вместе с 1j закоммичен план RENDER_PASSES — статический, «nothing built or run».

Что не доказано, дословно из карточек: «playing it by hand is the open manual check»; ветка «Not merged into dev/crossplatform/main, CI not enabled, nothing published without the user».
-->
