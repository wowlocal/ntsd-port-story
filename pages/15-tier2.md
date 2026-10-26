---
layout: chapter
num: 15
total: 20
kicker: Глава пятнадцатая
dates: 7 — 10 октября
image: /img/covers/ch15-ticks.svg
imagePixel: false
stats: 84 коммита · главный поток 24,6 → 11,1 мс · рендер 18,1 → 7,6 мс
---

# 16 миллисекунд

Цель автора — 8 мс работы на тик на Galaxy A12: сначала 33, потом 16, потом 8. Глава 14 закончилась на 24,6 мс. Агент крутил петлю «замер на телефоне → одна правка → ворота → оставить или откатить» трое с половиной суток — пока не упёрся в стену.

<div class="cover-note">Обложка нарисована из данных главы: каждая пара столбиков — закоммиченная ступень, оранжевый — главный поток, синий — рендер (vs).</div>

<style>
.cover-note { margin-top: 0.7rem; font-size: 0.66rem; color: var(--muted); }
</style>

<!--
Глава о 7–10 октября, ветка exp/core-realtime: от коммита bf5628e (7 октября, 08:51) до 0034e45c (10 октября, 18:27) — 84 коммита. Все числа — из реестра docs/research/CORE_REALTIME.md и его evidence-файлов; данные собраны scripts/collect_realtime2.py на коммите 5f5a8ee4.

Метрика та же, что в конце главы 14: время работы потока на один игровой тик (schedstat), а не время кадра на стене. Телефон один — Galaxy A12, debuggable-сборка, матч по сценарию без звука, музыки и сети, часы харнесса виртуальные.
-->

---

<Kicker>петля агента · одна строка реестра = один оборот</Kicker>

# Петля: замер → правка → ворота → решение

<Rt2Loop class="mt-1" />

<div class="grid grid-cols-5 gap-2 mt-2">
<StatTile :value="84" label="коммита за 81,6 часа" sub="7 окт 08:51 — 10 окт 18:27" size="sm" />
<StatTile :value="37" label="ступеней быстрее" sub="и 19 — «меньше работы»" size="sm" accent="var(--good)" />
<StatTile :value="8" label="не закоммичено" sub="2 отката, 6 отложено" size="sm" accent="var(--serious)" />
<StatTile :value="47" label="независимых ревью" sub="агент только для чтения" size="sm" accent="var(--s7)" />
<StatTile :value="480" label="прогонов на телефоне" sub="≈ 31 час матчей" size="sm" accent="var(--s1)" />
</div>

<div class="source">docs/research/CORE_REALTIME.md (Gates, Ledger) · rt-s2b-record-storage-20261009.json · rt-s3-actor-table-parked-20261009.json · rt-b2p4a-world-passes-reverted-20261008.json · data/rt2_loop.json, rt2_steps.json</div>

<!--
Петлю запускал автор: «/loop» с одним и тем же текстом, агент сам будил себя по расписанию. Каждый оборот — одна механика, одна строка реестра CORE_REALTIME.md и один evidence-файл.

Правило коммита из карточки, дословно: «Commit an increment only when every gate passes and it is either measurably faster or strictly less work without added complexity; otherwise record the result here and revert.»

Три примера. S2b — самый большой шаг главного потока 9 октября: запись состояния стала одним буфером, и копирование массивов в профиле упало с 9,40 до 4,96 %. По дороге первый прогон тестов встал на два часа: проверки, которые в цикле читали целые массивы, стали квадратичными. S3 — следующая правка, «таблица кусками»: копий массива меньше, но чтения через вложенные куски платят подсчётом ссылок, итог — ноль. B2 P4a — попытка из ночи на 8 октября: ревьюер ещё до замера написал, что выигрыша не будет, — и телефон это подтвердил. Вывод «убирать все уровни копий разом» превратился в P4b–P4f: главный поток 18,14 → 16,86 мс.

Счётчики: 75 строк реестра — 37 быстрее, 19 «меньше работы», 2 отката, 6 отложено, остальные 11 — доработки после ревью, тесты, телеметрия, правило процедуры, решение автора и сборки пакетов. 480 — различные прогоны телефона в evidence-файлах (по меткам), вместе ≈ 31 час матчей; одна сборка — 2–4 прогона, прежняя сборка — вперемешку в той же сессии.
-->

---

<Kicker>7 окт 08:51 — 10 окт 17:31 · 75 строк реестра · Galaxy A12</Kicker>

# 75 ступеней: 24,6 → 11,1 мс

<Rt2Scrubber />

<div class="legend-15">
<span><i class="ln" style="background: var(--s2)" />главный поток</span>
<span><i class="ln" style="background: var(--s1)" />поток рендера</span>
<span><i class="ln thin" />тонкая линия — Demo, восемь бойцов</span>
<span><i class="ring" />замерено, но не закоммичено</span>
<span class="hint"><span class="i-pixelarticons-drag-and-drop ico" />тяните по графику</span>
</div>

<div class="source">docs/research/CORE_REALTIME.md (реестр, 4m … 4ad) · docs/evidence/rt-*.json · среднее прогонов; Δ — против прежней сборки (с 8 окт — вперемешку в той же сессии) · data/rt2_steps.json</div>

<style>
.legend-15 { display: flex; flex-wrap: wrap; gap: .2rem 1rem; font-size: .64rem; color: var(--ink-2); margin-top: .35rem; align-items: center; }
.legend-15 span { display: inline-flex; align-items: center; }
.legend-15 .ln { display: inline-block; width: 14px; height: 2.5px; border-radius: 2px; margin-right: .35rem; }
.legend-15 .ln.thin { height: 1.3px; background: var(--ink-2); opacity: .7; }
.legend-15 .ring { display: inline-block; box-sizing: border-box; width: 9px; height: 9px; border-radius: 50%; border: 1.5px solid var(--ink-2); margin-right: .35rem; }
.legend-15 .hint { margin-left: auto; color: var(--muted); }
.legend-15 .ico { width: .85rem; height: .85rem; margin-right: .3rem; color: var(--naruto); }
</style>

<!--
Каждая точка — строка реестра и её evidence-файл: среднее 2–4 прогонов телефона. Под курсором — что это за ступень, во сколько закоммичена, и её собственное A/B: с 8 октября прошлую сборку гоняли вперемешку с новой в той же сессии, потому что телефон «плывёт» между сессиями; 7 октября новую ступень сравнивали с прогонами предыдущей. Короткие вертикальные чёрточки у курсора — разброс прогонов: видно, где шаг меньше шума.

Разрешение телефона — около ±0,25 мс на прогон. Поэтому на лестнице много ступеней «меньше работы, в пределах шума»: их коммитили по правилу карточки — строго меньше работы без лишней сложности, — а пользу проверяли профилем.

Две оговорки к линиям. С R2 (10 октября, 08:30) вывод кадра на экран Android ушёл в отдельный поток presenter (≈ 5,8 мс на тик, на медленных ядрах) — синяя линия его больше не включает. С R3 освобождение памяти ушло в поток release (≈ 2 мс) — его нет в оранжевой. Это честный перенос работы на другие ядра; об этом — слайд «Работа переехала».
-->

---

<Kicker>8 октября · 07:21 — 19:49</Kicker>

# 60 кадров в секунду ждали девять часов

<div class="grid grid-cols-[0.9fr_1.1fr] gap-5 mt-1">
<div>

<PhoneChat :messages="[
  { who: 'human', time: '07:21', text: 'when you get to 60fps on a phone put a tag on a branch pls', gloss: 'дойдёшь до 60 fps на телефоне — поставь тег', hot: true },
  { who: 'human', time: '07:28', text: '16.67 ms counts as 60fps', gloss: '16,67 мс — это уже 60 fps' },
  { who: 'human', time: '07:28', text: 'and we should also test DEMO game with a lot of going on, not just two chars figting', gloss: 'и мерить Demo, где много всего, а не только двух бойцов' },
  { who: 'event', time: '08:07', text: '<code>75c59ec</code> · Demo в замерах' },
]" />

</div>
<div>

<div class="ask">
<div class="ah"><span class="i-pixelarticons-robot ai" />Claude спрашивает · 09:38 <span class="aa">ответ — в 18:43</span></div>
<div class="aq" lang="en">Swift's dynamic exclusivity checks cost ~3.5–4% of the A12 main thread (~0.6 ms/tick) — enough for 60 fps in both vs and the Demo. Turning them off (<code>-enforce-exclusivity=unchecked</code>) changes nothing for correct code, but an overlapping-access bug would become silent undefined behaviour instead of a crash. How should I handle it?</div>
<div class="ao chosen" lang="en"><span class="i-pixelarticons-check oi" />Unchecked in shipping builds (Recommended)</div>
<div class="ao" lang="en">Keep the checks</div>
<div class="ao" lang="en">Unchecked everywhere</div>
</div>

<Rt2Sixty class="mt-1" />

</div>
</div>

<Rt2Activity class="mt-1" />

<div class="source">сессия 1f9218ae (вопрос AskUserQuestion; время местное, UTC+2) · 3d8935d, 7c02b7f, тег rt-60fps-a12 · rt-4aa-unchecked-exclusivity-60fps-20261008.json · data/rt2_commits.json, rt2_steps.json</div>

<style>
.ask { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: .45rem .7rem .5rem; }
.ah { display: flex; align-items: center; gap: .35rem; font-size: .64rem; color: var(--ink-2); margin-bottom: .2rem; }
.ah .ai { width: .9rem; height: .9rem; color: var(--naruto); }
.ah .aa { margin-left: auto; color: var(--warning); }
.aq { font-size: .64rem; line-height: 1.38; color: var(--ink); margin-bottom: .25rem; font-family: var(--font-sans); }
.aq code { font-size: .58rem !important; }
.ao { font-size: .64rem; color: var(--muted); border: 1px solid var(--hair); border-radius: 8px; padding: .1rem .5rem; margin-top: .18rem; display: flex; align-items: center; gap: .3rem; }
.ao.chosen { color: var(--ink); border-color: rgba(12,163,12,.65); background: rgba(12,163,12,.1); }
.ao .oi { width: .8rem; height: .8rem; color: var(--good); }
</style>

<!--
Утром 8 октября главный поток стоял на 16,9 мс — в шаге от 60 кадров в секунду. Автор попросил поставить тег, когда цель будет взята, уточнил порог — 16,67 мс — и попросил мерить не только vs, но и Demo, «где много всего». Через 40 минут Demo вошло в замеры (75c59ec).

В 09:38 агент спросил про проверки эксклюзивности Swift: в профиле телефона они занимали 3,5–4 % главного потока (swift_beginAccess, swift_endAccess и их thread-local состояние). Это не оптимизация, а снятие страховки во время выполнения: правильный код работает так же, но ошибка одновременного доступа стала бы тихим неопределённым поведением вместо падения. Сам агент такие решения не принимает: в разделе карточки «Out of scope» записано «dropping runtime safety checks without the user».

Петля встала. С 09:26 (4z) до 19:48 на ветке не было ни одного коммита: следующий шаг зависел от ответа. Ответ пришёл в 18:43 — вариант, который рекомендовал агент: релизные сборки без динамических проверок, тестовые — с ними, плюс тест-сторож, который падает, если тестовый бандл собран без проверок.

Результат — среднее трёх прогонов одного APK: Demo 16,13 мс главного потока и 11,99 рендера, vs 16,25 и 13,82. Оба потока в обоих сценариях не больше 16,67 мс — тег rt-60fps-a12 стоит на 7c02b7f (19:49). Первый коммит 4aa забыл половину правки: из-за опечатки в команде оболочки («$TT:crossplatform» zsh прочитал как модификатор) файл сборщика APK не попал в индекс; второй коммит через полминуты это исправил.

Наведите на штрихи внизу — тема каждого коммита. Высокие штрихи — шаги реестра, короткие — записи реестра и плана и правки инструментов.
-->

---
clicks: 4
---

<Kicker>8 — 13 октября · от ответа автора до релиза</Kicker>

# Страховку сняли — и в релизе

<p class="lead">Ответ автора — «Unchecked in shipping builds». За пять дней он дошёл от APK до всех пакетов релиза; тесты и ворота проверки сохранили.</p>

<CExclusivityMatrix stepwise />

<div class="xfacts">
<div><b style="color: var(--naruto)">3,5–4 %</b><span>главного потока A12 стоили проверки, ≈ 0,6 мс на тик</span></div>
<div><b style="color: var(--naruto)">3 306 → 0</b><span>точек проверок: бинарник ворот → релизное приложение macOS</span></div>
<div><b>2 164</b><span>остались в статически слинкованном Foundation (Linux arm64 — 2 170)</span></div>
<div><b style="color: var(--good)">60 fps</b><span>на A12 и после 4ab, в обоих сценариях</span></div>
</div>

<div class="source">тела коммитов 3d8935d · 7c02b7f · 0dd7740 · 1035e40d · 5b8e5d02 · rt-4aa-unchecked-exclusivity-60fps-20261008.json · release-refresh-20261013.json на 0b5d4621</div>

<style>
.lead { margin: -0.45rem 0 0.5rem !important; font-size: 0.8rem; line-height: 1.4; color: var(--ink-2); max-width: 54rem; }
.xfacts { display: grid; grid-template-columns: repeat(4, 1fr); gap: .5rem; margin-top: .5rem; }
.xfacts > div { background: var(--surface); border: 1px solid var(--hair); border-radius: 10px; padding: .28rem .55rem .32rem; display: flex; align-items: baseline; gap: .45rem; }
.xfacts b { font-family: var(--font-display); font-size: .88rem; color: var(--ink); white-space: nowrap; font-weight: 700; }
.xfacts span { font-size: .58rem; line-height: 1.3; color: var(--ink-2); }
</style>

<!--
Клики открывают по одному шагу; в экспорте видны все пять столбцов. Оранжевая рамка — клетка, которая изменилась на этом шаге.

Вопрос был узким: проверки эксклюзивности Swift — swift_beginAccess, swift_endAccess и их thread-local состояние — стоили 3,5–4 % главного потока телефона, около 0,6 мс на тик. Ответ — «Unchecked in shipping builds»: релизные сборки без динамических проверок, тестовые бандлы с ними. Статические диагностики компилятора остаются, правильный код работает так же; меняется только то, что ошибка одновременного доступа стала бы тихим неопределённым поведением, а не падением.

4aa (8 октября, 19:48): Package.swift добавляет -enforce-exclusivity=unchecked только в release и только при NTSD_UNCHECKED_EXCLUSIVITY=1; переменную ставит сборщик APK. Тест-сторож падает, если тестовый бандл собран без проверок. Это и есть 60 fps и тег rt-60fps-a12.

4ab (20:46 того же дня): ревью 4aa нашло, что модуль NTSDFreeTypeText — часть APK — сохранил проверки, а хосты SDL и iOS вообще не могли включить флаг. После правки в библиотеке APK в наших модулях нет ни одной точки проверки; 2 164 оставшиеся принадлежат статически слинкованному Foundation тулчейна. Телефон по-прежнему на 60 fps в обоих сценариях. То же ревью предложило: бинарники ворот оставить с проверками, чтобы динамические проверки ловили ошибку на каждом проверяемом пути, плюс один прогон без проверок — для конфигурации, которая уходит игрокам.

4ac (10 октября, 18:02): build-native.sh экспортирует флаг для релизной сборки приложения macOS. В релизном NTSDNative точек проверки нет, в бинарнике ворот — 3 306; сценарии vs и playback равны, кадры идентичны, 20 из 20 запусков чистые.

4ad (18:26): package_linux.py, package_windows.py и ios_app.py передают флаг своим релизным сборкам. Linux arm64 — проверка пакета проходит, в наших модулях вызовов нет (2 170 — в Foundation); симулятор iOS — vs равен; Windows x86_64 — проверка пакета в свежей бутылке CrossOver. Коммит сам называет это проверками упаковщиков, а не приёмкой на устройствах.

Релиз 13 октября (глава 18): macOS 0.5.0 записан как «fresh release NTSDNative, unchecked exclusivity as existing shipping policy»; APK, Windows и Linux собраны теми же упаковщиками с флагом. iOS в релиз не вошёл по просьбе автора. Веб-сборку в этой цепочке не трогали: в web_app.py на 0b5d4621 переменной нет.

Вывод для зрителя: решение «снять страховку» не осталось экспериментом ветки — оно стало политикой поставки, и это записано в evidence релиза.
-->

---

<Kicker>что двигало стрелку · vs, против прежней сборки</Kicker>

# Большие шаги — и шум под ними

<Rt2Biggest class="mt-1" />

<div class="source">docs/evidence/rt-*.json (phone: after против base) · B2 P4b–f — одна группа: все четыре мерили против одних и тех же прогонов 4w · разрешение ±0,25 мс — CORE_REALTIME.md (Next task) · data/rt2_steps.json → biggest</div>

<!--
Три самых больших шага — на потоке рендера. R2 — не экономия, а переезд: вывод кадра на экран Android ушёл в отдельный поток presenter, который сам стоит ≈ 5,8 мс на медленных ядрах; поэтому полоса заштрихована. R1 — копия заднего буфера и обрезка кадра слились в одну операцию. A3 P5a — таймер итераций через timerfd в главном цикле Android: каждый asyncAfter будил служебный поток libdispatch системным вызовом (1,55 % главного потока); после правки быстрее стали оба потока.

На главном потоке крупнее всех 4p: кадровые блоки (≈ 14 600) сортировались по адресу при каждом построении, дважды за тик; теперь порядок считается раз на загруженный каталог. Первая версия — «не сортировать, если уже по порядку» — не дала ничего: блоки не лежат по адресам. B2 P4b–f — серия из четырёх коммитов ночью 8 октября: все проходы игрового тела работают на месте под единственной копией. P0 тоже заштрихован: та же работа, просто на быстрых ядрах.

Чёрточка на полосе — разброс прогонов шага. У e (команды Blt и заливки одной записью) он большой: третий прогон оказался низким на обоих потоках, в реестре шаг записан скромнее — 13,96 → 13,61 по двум прогонам.

Нижняя полоса — честный фон: из 57 закоммиченных шагов 35 меняют главный поток меньше чем на ±0,25 мс. Их коммитили по второй половине правила — «строго меньше работы без лишней сложности», — подтверждая пользу профилем, а не секундомером. Точки правее нуля — тоже шум: R2 и g, по записям реестра, сравнивались с базой, где один прогон прочитался низко.
-->

---
clicks: 4
---

<Kicker>9 окт 06:09 — 10 окт 12:18 · R2 → P0 → R2 → R3</Kicker>

# Отложенная правка нашла медленные ядра

<Rt2Cores stepwise class="mt-1" />

<div class="source">rt-r2-presenter-thread-parked-20261009.json · rt-r2b-presenter-remeasured-20261010.json · rt-p0-main-on-fast-cores-20261010.json (finding) · rt-r2-presenter-thread-20261010.json · rt-r3-release-thread-20261010.json · data/rt2_threads.json</div>

<!--
Клики проходят пять моментов.

9 октября R2 вынес вывод на экран Android (полосы, перестановка каналов, post) в отдельный поток: рендер −4 мс, но главный поток стал медленнее на 0,2–0,4 мс — а кадр упирается именно в главный. Правку отложили с пометкой «вернуться, когда главный станет быстрее рендера».

Утром 10 октября агент перемерил R2 на новой сборке — и снова +0,57 мс главного в Demo. Тогда он стал раз в секунду читать, на каком процессоре выполняется каждый поток (/proc/<pid>/task/*/stat, поле 39). Ответ: пока поток рендера занят, планировщик Android держал главный поток в основном на медленном кластере — 1,8 ГГц против 2,3.

P0 — главный поток закрепляется за ядрами быстрее самого медленного яруса; кластер находится по максимальной частоте каждого ядра, на возобновлении закрепление повторяется. Результат игры от ядра не зависит — меняется только скорость. Ревью настояло, чтобы закреплять за всеми быстрыми ядрами, а не за одним.

После этого R2 вернулся — с presenter, закреплённым на медленных ядрах: рендер Demo 10,59 → 5,90 мс. И той же дорогой пошёл R3: освобождение мёртвых значений (≈ 10 % работы главного потока — целые копии State, освобождаемые поэлементно) ушло в поток release, тоже на медленные ядра.

Урок для петли: «отложено» — не «выброшено». Запарковка с записанной причиной и патчем позволила вернуться, когда условие изменилось.
-->

---

<Kicker>10 октября, 10:12 и 12:18 · шаги L4b и R3</Kicker>

# Компилятор ошибся ещё дважды

<p class="lead">Через шесть дней после <code>#92905</code> — снова Swift, и снова на одной ветке: два случая за два часа. Оба поймали сборка и тесты, игроку не досталось ни одного.</p>

<div class="cc">
<div class="ccard">
<div class="ch"><span class="pixel">упал сам оптимизатор</span><span class="mono">10:12 · 7091da10 · L4b</span></div>
<pre class="err">signal 6 · PerfInliner
Assertion isLoadableOrOpaque
  in SILBuilder createLoad</pre>
<p>Релизная сборка тестов, rtl4b и rtl4bt. Новый тест передавал постоянное замыкание в ещё обобщённый <code>standaloneCursor</code>, и оптимизатор, специализируя его, падал.</p>
<pre class="sw"><i>/// Hides a constant closure from the release optimizer</i>
@inline(never) private func opaque&lt;T&gt;(_ value: T) -> T { value }</pre>
<div class="out">сборки игры — headless, AppKit, APK — не затронуты</div>
</div>

<div class="ccard">
<div class="ch"><span class="pixel">массив освобождён дважды</span><span class="mono">12:18 · d342f740 · R3</span></div>
<pre class="err">NTSD.release · _swift_release_dealloc
debug-сборка теста загрузки · 2 падения
журнал типов: Array&lt;Batch&gt;</pre>
<p>Уже после правок ревью: <code>retire(consume drained)</code> внутри <code>defer</code>. По записи evidence, компилятор всё равно освобождал переменную в конце области — второй раз.</p>
<pre class="sw"><i>// после цикла, не в defer</i>
if !drained.isEmpty { …retire(consume drained) }
<i>/// Never `consume` a variable declared outside a `defer`</i>
<i>/// from inside it … A binding made inside the `defer` is fine.</i></pre>
<div class="out">7 тестов загрузки в debug прошли; запрет записан в комментарии к <code>retire</code></div>
</div>
</div>

<div class="three">
<span class="th pixel">три раза Swift</span>
<div class="tc"><b>4 окт · a72ae97</b>Static Linux SDK выбрасывал запись в слот перед <code>isKnownUniquelyReferenced</code> → отчёт #92905, исправлен в 6.4.x</div>
<div class="tc now"><b>10 окт · 7091da10</b>оптимизатор падает на тесте → замыкание через <code>@inline(never)</code></div>
<div class="tc now"><b>10 окт · d342f740</b><code>consume</code> из <code>defer</code> → двойное освобождение → передача после цикла</div>
</div>

<div class="source">тела коммитов 7091da10 · d342f740 · rt-a3-l4b-driverless-idle-20261010.json (compiler) · rt-r3-release-thread-20261010.json (crash_found_and_fixed) · swiftlang/swift#92905</div>

<style>
.lead { margin: -0.45rem 0 0.6rem !important; font-size: 0.8rem; line-height: 1.4; color: var(--ink-2); max-width: 54rem; }
.lead code { font-size: .7rem !important; }
.cc { display: grid; grid-template-columns: 1fr 1fr; gap: .7rem; }
.ccard { background: var(--surface); border: 1px solid rgba(208,59,59,.45); border-radius: 12px; padding: .45rem .7rem .5rem; display: flex; flex-direction: column; gap: .3rem; }
.ch { display: flex; justify-content: space-between; align-items: baseline; gap: .5rem; }
.ch .pixel { color: #f08a8a; font-size: .86rem; }
.ch .mono { font-size: .54rem; color: var(--muted); white-space: nowrap; }
.ccard pre { margin: 0; font-family: var(--font-mono); white-space: pre-wrap; border-radius: 7px; padding: .3rem .5rem; }
.ccard pre.err { font-size: .58rem; line-height: 1.45; color: #f6c0c0; background: rgba(208,59,59,.12); }
.ccard pre.sw { font-size: .55rem; line-height: 1.45; color: var(--ink); background: #0c1017; border: 1px solid var(--hair); }
.ccard pre i { font-style: normal; color: var(--muted); }
.ccard p { font-size: .64rem; line-height: 1.38; color: var(--ink-2); margin: 0 !important; }
.ccard p code, .out code, .tc code { font-size: .56rem !important; }
.out { font-size: .6rem; color: var(--ink); border-top: 1px dashed var(--axis); padding-top: .22rem; margin-top: auto; }
.out::before { content: '→ '; color: var(--good); }
.three { display: grid; grid-template-columns: auto 1fr 1fr 1fr; gap: 10px; align-items: stretch; margin-top: .6rem; }
.three .th { font-size: .66rem; color: var(--naruto); align-self: center; width: 5.6rem; line-height: 1.25; }
.three .tc { font-size: .6rem; line-height: 1.35; color: var(--ink-2); background: rgba(255,255,255,.03); border: 1px solid var(--hair); border-radius: 10px; padding: .32rem .55rem; }
.three .tc b { display: block; color: var(--ink); font-weight: 600; font-size: .58rem; margin-bottom: .05rem; }
.three .tc.now { border-color: rgba(217,89,38,.55); }
</style>

<!--
Оба случая — в тот же день, что медленные ядра и поток release, на ветке exp/core-realtime.

L4b (7091da10, 10:12) — первый холостой проход шага без драйвера и обмена: главный поток vs 12,07 → 11,82 мс на тик. Для него написан юнит-тест, который передаёт постоянное замыкание в ещё обобщённый standaloneCursor. Первые две релизные сборки тестов (rtl4b и rtl4bt) уронили оптимизатор Swift: signal 6, PerfInliner, «Assertion isLoadableOrOpaque in SILBuilder createLoad». Это падение самого компилятора при специализации замыкания. Обход — пропустить замыкание через тождественную функцию с @inline(never); комментарий в тесте называет логи сборок. Сборки игры — headless, AppKit, APK — не затронуты.

R3 (d342f740, 12:18) — освобождение мёртвых значений на отдельном потоке NTSD.release. Ревью одобрило с мелкими замечаниями; при их применении функция retire стала брать значение как consuming, и вызов retire(consume drained) оказался внутри defer. В debug-сборке тест загрузки дважды упал в _swift_release_dealloc на потоке NTSD.release, журнал типов показал Array<Batch>. Запись в evidence: «the compiler still released the consumed variable at the scope's end». Передачу перенесли после цикла выборки; 7 тестов загрузки прошли в debug; в комментарии к retire теперь запрет: не делать consume переменной, объявленной снаружи defer, изнутри него — а привязка, сделанная внутри defer, допустима. Прогон ThreadSanitizer тестов потока release и загрузки — чистый.

Сравнение с #92905 (глава 13): там ошибку нашла матрица целых сценариев, и отчёт ушёл в Swift с разрешения автора. Здесь обе ошибки поймали собственные тесты шага, до коммита: в первом случае страдала только сборка теста, во втором — debug-сборка. В evidence записаны обходы и правило; отдельных отчётов в Swift по ним в репозитории нет.
-->

---

<Kicker>8 строк реестра «не закоммичено» и 2 первые версии</Kicker>

# Что не взяли — и что из этого выросло

<div class="rej">
<div class="rc"><div class="rh"><span class="pixel">B2 P4a</span><span class="rt bad">откат</span><span class="mono rd">8 окт 00:21</span></div><div class="rw">три прохода мира — на месте</div><div class="rn">главный 18,1/17,9 → 17,7/18,0 мс — в пределах разброса; ревью предсказало это до замера</div><div class="rg">→ убрать все уровни копий разом: P4b–f, 18,14 → 16,86</div></div>
<div class="rc"><div class="rh"><span class="pixel">B3a</span><span class="rt bad">откат</span><span class="mono rd">8 окт 06:13</span></div><div class="rw">загруженный цикл — один уровень транзакции</div><div class="rn">телефон 16,93 → 16,95 мс, Mac на ~1 % медленнее (0,879 → 0,889 мс в трёх парах)</div><div class="rg">причина не установлена — не коммитить</div></div>
<div class="rc"><div class="rh"><span class="pixel">R2</span><span class="rt park">отложено</span><span class="mono rd">9 окт 06:09</span></div><div class="rw">вывод Android — в свой поток</div><div class="rn">рендер −4 мс, но главный +0,19 (vs) и +0,36 (Demo)</div><div class="rg">→ через сутки: медленные ядра, P0, R2 закоммичен</div></div>
<div class="rc"><div class="rh"><span class="pixel">S3</span><span class="rt park">отложено</span><span class="mono rd">9 окт 18:52</span></div><div class="rw">таблица актёров кусками по 16</div><div class="rn">vs 14,18 → 14,26 мс: копий массива меньше, уничтожений записей больше</div><div class="rg">патч на диске; нужен доступ без копий или решение Q1</div></div>
<div class="rc"><div class="rh"><span class="pixel">G4b</span><span class="rt park">отложено</span><span class="mono rd">10 окт 03:40</span></div><div class="rw">кэш поверхностей на время повтора</div><div class="rn">все ворота прошли, но выигрыш ≈ 0,02 мс (frontSurface 0,87 → 0,74 %)</div><div class="rg">не стоит кэша с правилами инвалидации</div></div>
<div class="rc"><div class="rh"><span class="pixel">R4a</span><span class="rt park">отложено</span><span class="mono rd">10 окт 15:39</span></div><div class="rw">SIMD-копии по 4 пикселя</div><div class="rn">кадры те же, но рендер медленнее: Demo 6,05 → 6,42, vs 8,26 → 8,72 мс</div><div class="rg">→ R4b: тесные циклы без лишних ветвлений, vs 8,16 → 7,59</div></div>
<div class="rc"><div class="rh"><span class="pixel">F1</span><span class="rt park">отложено</span><span class="mono rd">10 окт 17:50</span></div><div class="rw">поля кадров физики — на месте</div><div class="rn">уничтожения Flat? 2,71 → 2,68 %: этой доли у физики не было</div><div class="rg">→ исправлен сам инструмент: листинг копий печатает долю каждого вызывающего</div></div>
<div class="rc"><div class="rh"><span class="pixel">4p v1</span><span class="rt bad">не закоммичено</span><span class="mono rd">7 окт</span></div><div class="rw">не сортировать уже упорядоченное</div><div class="rn">ничего: 14 600 блоков кадров не лежат по адресам</div><div class="rg">→ v2: порядок раз на каталог, −1,6 мс — крупнейший шаг главного</div></div>
<div class="rc"><div class="rh"><span class="pixel">M1 v1</span><span class="rt bad">не закоммичено</span><span class="mono rd">9 окт</span></div><div class="rw">таблица актёров только для токенов до 4096</div><div class="rn">всё равно хешировала каждое из 400 мест</div><div class="rg">→ v2: таблица по общему шагу токенов, привязки 4,61 → 3,09 %</div></div>
</div>

<div class="source">rt-b2p4a-world-passes-reverted · rt-b3a-loaded-cycle-in-place · rt-r2-presenter-thread-parked · rt-s3-actor-table-parked · rt-g4b-surface-cache-parked · rt-r4a-simd-copies-parked · rt-f1-frame-words-parked · rt-4p-frame-order (rejected_first_version) · rt-m1-actor-table-one-pass (first_version) · data/rt2_steps.json</div>

<style>
.rej { display: grid; grid-template-columns: repeat(3, 1fr); gap: .45rem; margin-top: .2rem; }
.rc { background: var(--surface); border: 1px solid var(--hair); border-radius: 10px; padding: .32rem .6rem .38rem; }
.rh { display: flex; align-items: baseline; gap: .45rem; }
.rh .pixel { color: var(--naruto); font-size: .82rem; }
.rt { font-size: .6rem; padding: 0 .4rem; border-radius: 999px; border: 1px solid var(--hair); color: var(--ink-2); }
.rt.bad { border-color: rgba(236,131,90,.7); }
.rt.park { border-color: rgba(250,178,25,.6); }
.rd { margin-left: auto; font-size: .58rem; color: var(--muted); }
.rw { font-size: .72rem; color: var(--ink); line-height: 1.25; margin-top: .1rem; }
.rn { font-size: .63rem; color: var(--ink-2); line-height: 1.3; margin-top: .12rem; }
.rg { font-size: .63rem; color: var(--ink); line-height: 1.3; margin-top: .15rem; border-top: 1px dashed var(--axis); padding-top: .12rem; }
</style>

<!--
Правило карточки работает в обе стороны: правка, которая не стала быстрее на телефоне или добавила сложности без выигрыша, не коммитится — но и не пропадает. Результат пишется в реестр отдельным коммитом, evidence-файл объясняет почему, патч кладётся на внешний диск.

Половина «нет» дала следующий шаг. B2 P4a показал, что убирать копии нужно сразу на всех уровнях, — и серия P4b–f сняла 1,3 мс. R2 через сутки привёл к находке про медленные ядра. R4a — к R4b, первому шагу, который опустил рендер vs ниже 8 мс. F1 исправил не игру, а инструмент: листинг копий начал печатать собственную долю каждого вызывающего, потому что посылка F1 из него и была ошибочной.

B3a — честный случай без объяснения: на телефоне без изменений, на Mac на процент медленнее, причина не найдена. По правилу — откат.

Отдельно — R2 (9 окт) в реестре записан как «not committed», а не «reverted»: ворота прошли, ревью нашло ошибку порядка (синхронный вывод мог обогнать кадры в очереди presenter при переходе из игры в меню) и её исправили до замера.
-->

---

<Kicker>каждая строка реестра · ревью и ворота из её evidence-файла</Kicker>

# Ворота — каждый раз, ревью — по делу

<Rt2Reviews class="mt-1" />

<div class="grid grid-cols-[1.35fr_1fr] gap-4 mt-2">
<div class="caught">
<div class="ch2 pixel">что нашли до коммита</div>
<div class="ci"><b class="pixel">1</b> <span><b>R1</b> · отложенная копия кадра могла расти без предела, если окно двигают каждый кадр</span></div>
<div class="ci"><b class="pixel">2</b> <span><b>S1</b> · первая версия раздувала каждую запись с 40 до 48 байт — блокирующая находка; прогон ворот остановлен</span></div>
<div class="ci"><b class="pixel">3</b> <span><b>G1</b> · порог в тесте-близнеце был недостижим (1 500 при реальных 922)</span></div>
<div class="ci"><b class="pixel">4</b> <span><b>R2</b> · синхронный вывод мог обогнать кадры в очереди presenter при выходе в меню</span></div>
<div class="ci"><b class="pixel">5</b> <span><b>S2b</b> · пять находок — от широких целых до маски по битам — исправлены до ворот</span></div>
</div>
<div class="inc">
<div class="ch2 pixel">4u · 7 окт, 21:22</div>
<p>Приложение AppKit из инкрементальной сборки падало на старте в 10 запусках из 20: модуль, который не пересобрался, держал встроенный размер объекта сессии — <b>448 байт вместо 472</b> — и писал за его конец.</p>
<p class="rule">Правило с тех пор: бинарники для ворот — только из чистых сборок, ≈ 2 мин на бинарник и ≈ 6 на тесты.</p>
</div>
</div>

<div class="source">docs/evidence/rt-*.json: поля review, gates · rt-r1-present-crop · rt-s1-two-level-pages · rt-g1-unobserved-draw · rt-r2-presenter-thread-parked · rt-s2b-record-storage · rt-4u-clean-gate-builds · data/rt2_steps.json</div>

<style>
.caught, .inc { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: .4rem .7rem .45rem; }
.ch2 { font-size: .66rem; color: var(--naruto); margin-bottom: .15rem; }
.ci { display: flex; gap: .45rem; font-size: .7rem; line-height: 1.34; color: var(--ink-2); margin: .2rem 0; }
.ci > b.pixel { color: var(--ink); background: rgba(250,178,25,.22); border: 1px solid rgba(250,178,25,.6); border-radius: 4px; min-width: 1.05rem; height: 1.05rem; display: inline-flex; align-items: center; justify-content: center; font-size: .62rem; flex: none; }
.ci span b { color: var(--ink); }
.inc p { font-size: .7rem !important; line-height: 1.4; color: var(--ink-2); margin: .2rem 0 !important; }
.inc p b { color: var(--ink); }
.inc .rule { color: var(--ink); border-top: 1px dashed var(--axis); padding-top: .2rem; }
</style>

<!--
Сетка собрана из evidence-файлов: если проверка в файле не записана — точка. Ворота для каждой ступени, по карточке: 10 сценариев app_e2e равны эталонам и 1 832 кадра матча VS совпадают с замороженной записью m1-frames-ref; AppKit — VS и запись, 3 960 кадров; эмулятор Android — VS, 1 832 кадра; затронутые наборы тестов; ThreadSanitizer — там, где меняются потоки (P2, R3). Пустые столбцы — строки без кода: тесты, записи отката, сборки пакетов.

Независимое ревью — отдельный агент только для чтения — обязательно для изменений модели хранения и архитектуры: 47 раз из 75. Ещё 23 строки записали, почему ревью не нужно («одна локальная эквивалентность», «итерация в том же порядке»), у пяти поля ревью нет вовсе — это записи отката и сборки.

Ревью шло параллельно с воротами. В S1, G1 и R2 находка пришла, когда прогон ворот уже шёл, — прогон останавливали, исправляли и запускали заново. Находка S1 — та самая ошибка, что в главе 14 стоила около 1 мс на тик: лишнее поле раздувало запись до 48 байт; на этот раз её поймал тест на размер записи и ревьюер до замера.

4u — правило процедуры, а не оптимизация. Релизные сборки компилируют модуль целиком, а с межмодульной оптимизацией (4k) неизменённый клиентский модуль сохраняет встроенный код старой зависимости. Guard Malloc нашёл запись на байт за концом объекта в OriginalRuntimeSession.init. Флаг -disable-incremental-imports не помог. С тех пор ворота — только из чистых сборок.
-->

---

<Kicker>состояние на 10 октября, 17:31 · e5 · Galaxy A12</Kicker>

# Ярусы: рендер взял 8 мс, главный — 16

<Rt2Tiers class="mt-1" />

<div class="source">docs/research/CORE_REALTIME.md (Status, R4b; tiers) · rt-e5-emit-consumes-20261010.json · rt-4l-pending-loading-20261007.json · rt-4z-font-bitmap-once-20261008.json (первые прогоны Demo) · data/rt2_steps.json → tiers, rt2_threads.json</div>

<!--
Переключатель над графиком двигает бюджет: 33 мс (ярус 1, взят ещё 6 октября), 16,67 (60 кадров в секунду — порог автора), 16 (ярус 2) и 8 (ярус 3, цель). В выгрузке — 16 мс.

Когда пройден ярус 2 (16 мс): поток рендера vs — R1, 7 октября в 10:52; главный vs — S1, 8 октября в 22:22 (15,73); главный Demo — G1 через час (15,46); рендер Demo был ниже 16 мс уже при первом замере Demo. 60 кадров в секунду (≤ 16,67 на обоих потоках в обоих сценариях) — 4aa, 8 октября в 19:48.

Ярус 3 (8 мс): рендер Demo — R2, 10 октября в 08:30 (5,90); рендер vs — R4b в 15:39 (7,59). Главный поток так и не дошёл: 11,09 мс в vs и 11,62 в Demo.

Внизу — неудобная правда метрики «на поток». В начале главы главный и рендер вместе делали 42,7 мс работы на тик; в конце четыре потока делают 26,3 мс. Работы стало почти на 40 % меньше, а самый медленный поток похудел больше чем вдвое — потому что часть работы переехала в presenter и release на медленные ядра. Все числа — время работы потока на тик по schedstat под виртуальными часами харнесса, а не время кадра на экране.
-->

---

<Kicker>10 октября, 18:27 · 0034e45c</Kicker>

# Стена: дальше — только по решениям автора

<Rt2Wall class="mt-1" />

<div class="source">docs/research/CORE_REALTIME.md (Next task, 2026-10-10) · docs/research/CORE_REALTIME_TIER3.md (Candidates, Order, Decisions for the user; 5fe8641) · 0034e45c · оценки плана, не замеры · data/rt2_wall.json</div>

<!--
Что осталось без решений автора, по оценкам самого агента: H3, H2, рендер-поток без пробуждений, коробка для редких поставок платформы, L6, lastRequest — от 0,04 до 0,15 мс каждое. Всё это внутри разрешения телефона (±0,25 мс за прогон) и каждое добавило бы второй путь кода. Правило коммита — «измеримо быстрее или строго меньше работы без лишней сложности» — ни одно не проходит. Оставшиеся копии в профиле — транзакционные: они хранят состояние упавшего шага.

Чтобы идти дальше, нужно менять то, что видно после сбоя. Четыре вопроса автору из карточки яруса 3 (дословно — в карточке): Q1 — может ли упавший загруженный тик оставить Host только с ожидающим вводом до тика; Q2 — может ли любой сбой от итерации до хвоста оставлять Host на последнем закоммиченном батче (покрывает Q1); Q3 — могут ли холостые коммиты держать прежний объект платформы; Q4 — может ли ошибка дисплея на закоммиченных отрисовках остановить игру на тик позже. В выпуске любая ошибка всё равно останавливает игру, так что Q1–Q3 меняют только то, что видят тесты после сбоя, а Q4 сдвигает момент ошибки на один тик. С Q2–Q4 план обещал ≈ 9–10 мс.

Справа — самое неожиданное. План яруса 3 писал отдельный агент только для чтения вечером 8 октября, когда главный поток был на 16,25 мс: «без решений — около 11 мс на главном потоке и около 8 на рендере». Через 44 часа последний замер петли дал 11,09 (vs) и 11,62 (Demo), рендер — 7,55 и 6,14. Путь был другим — P0, R2 и R3 в плане не было, — а стена оказалась там, где её нарисовали.
-->

---

<Kicker>10 октября, 21:23 · конец петли</Kicker>

# «We reached the wall»

<div class="grid grid-cols-[1.05fr_1fr] gap-6 mt-2">
<div>

<div class="cm">
<div class="cmh"><span class="i-pixelarticons-git-commit ci2" />последний коммит петли · 18:27 · <span class="mono">0034e45c</span></div>
<div class="cmb mono" lang="en">Every remaining decision-free item is below the phone's resolution and would add a second code path, so none meets the commit rule; the copies left are the transactional ones. The input needed is the user's answers to Q1-Q4 (TIER3).</div>
<div class="cmg">всё, что осталось без решений, — ниже разрешения телефона и добавило бы второй путь кода; нужны ответы на Q1–Q4</div>
</div>

<PhoneChat class="mt-3" :messages="[
  { who: 'human', time: '21:23', text: 'you did good. we reached the wall. performance is now close to optimal. now lets do the loop for optimizing  memory footprint and loading times. …', gloss: 'хорошая работа; это стена, производительность близка к оптимальной. Теперь — петля по памяти и времени загрузки', hot: true },
]" />

<div class="grid grid-cols-3 gap-2 mt-3">
<StatTile value="11,1 мс" label="главный поток, vs" sub="с 24,6 · Demo 11,6" size="sm" accent="var(--s2)" />
<StatTile value="7,6 мс" label="поток рендера, vs" sub="с 18,1 · Demo 6,1" size="sm" accent="var(--s1)" />
<StatTile value="60 fps" label="с 8 окт, 19:48" sub="тег rt-60fps-a12" size="sm" accent="var(--good)" />
</div>

</div>
<div>

<div class="np">
<div class="nph pixel">что числа не доказали</div>

- **Один телефон** — Galaxy A12; debuggable-сборка (релизная оптимизация, без проверок эксклюзивности); матч по сценарию, без музыки, звуков и сети
- **Работа на поток, не кадр на экране**: schedstat под виртуальными часами харнесса. С настоящими часами матч идёт в темпе оригинала, 30,3 тика/с, а холостых итераций на тик 4,1 вместо 3,12 — экономия на итерацию весит в ≈ 1,3 раза больше
- **Руками на A12** плавность игры в реестре этих дней не записана — это критерий карточки
- **Q1–Q4 остались без ответа**: автор перевёл петлю на память и загрузку

</div>

</div>
</div>

<div class="source">0034e45c · 49f44e09 (per-tick split, real-clock idle steps) · docs/research/CORE_REALTIME.md (критерий, Gates) · tools/crossplatform/android_speed.py · сессия 1f9218ae (время местное, UTC+2)</div>

<style>
.cm { background: #0c1017; border: 1px solid rgba(255,255,255,.1); border-radius: 10px; overflow: hidden; }
.cmh { display: flex; align-items: center; gap: .4rem; font-size: .64rem; color: var(--muted); background: #161b25; border-bottom: 1px solid rgba(255,255,255,.06); padding: .22rem .6rem; }
.cmh .ci2 { width: .9rem; height: .9rem; color: var(--naruto); }
.cmb { font-size: .66rem; line-height: 1.45; color: var(--ink); padding: .45rem .7rem .2rem; }
.cmg { font-size: .64rem; color: var(--muted); padding: .1rem .7rem .5rem; }
.np { background: var(--surface); border: 1px solid rgba(250,178,25,.45); border-radius: 12px; padding: .45rem .8rem .5rem; }
.nph { font-size: .72rem; color: var(--warning); margin-bottom: .2rem; }
.np ul { margin: 0; }
.np ul > li { font-size: .76rem; line-height: 1.42; margin: .42rem 0; }
</style>

<!--
В 18:27 агент записал в карточку, что петля упёрлась в стену, и остановился. В 21:23 автор ответил — и не стал отвечать на Q1–Q4: «you did good. we reached the wall. performance is now close to optimal. now lets do the loop for optimizing memory footprint and loading times. . you can create a new branch and start developing. build strong methodology as you progress.» Опечатки и двойной пробел — авторские. Об этой петле — следующая глава.

Итог главы на телефоне 2008 года: главный поток 24,6 → 11,1 мс работы на тик (vs) и 11,6 в Demo с восемью бойцами; рендер 18,1 → 7,6 и 6,1. 60 кадров в секунду с 8 октября, тег rt-60fps-a12. Игра та же: на каждой ступени 10 сценариев равны эталонам, кадры совпадают.

Оговорки — дословно из карточки и инструмента: телефон один, сборка debuggable (выпускная не скриптуется), музыка, звуки и сеть в замерах выключены. Время на тик — работа потока, а не время кадра: с настоящими часами игра идёт в своём темпе, 30,3 тика в секунду, и спит остаток таймера в 33 мс.
-->
