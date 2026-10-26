---
layout: chapter
num: 16
total: 20
kicker: Глава шестнадцатая
dates: 10 — 11 октября
image: /img/covers/ch16-loading.svg
imagePixel: false
stats: A12 124 → 5,2 с · 1,6 ГБ → 565 МиБ · 31 гейт · кадр не медленнее
---

# Две минуты за одну ночь

Реальное время упёрлось в стену, и автор дал агенту новый цикл: память и загрузка. Телефон грузил игру две минуты. К десяти утра — пять секунд.

<div class="cover-note">Обложка — рисунок: экран загрузки игры в контуре телефона, не фотография.</div>

<style>
.cover-note { margin-top: 0.7rem; font-size: 0.66rem; color: var(--muted); }
</style>

<!--
Глава о 22 часах: от реплики автора 10 октября в 21:23 до остановки цикла 11 октября в 19:43. Ветка exp/memory-loading от exp/core-realtime 0034e45; карточка исследования docs/research/MEMORY_LOADING.md; все цифры — из её журнала и evidence-файлов ml-*.json, состояние репозитория на 5f5a8ee4.

Устройство то же, что в главе 14: Samsung Galaxy A12, Helio P35, восемь ядер Cortex-A53, 2,8 ГБ памяти, флеш eMMC, свободно ~1,3 ГБ. Сборка — debuggable APK, сценарий vs по скрипту app_e2e на виртуальных часах, сеть выключена.

«Пять секунд к десяти утра» — гейт L18+19 в 10:05: 5,24 с (5,20–5,28). Финальная сборка вечером — 5,9 с (5,4–6,3): экран загрузки ждёт пакеты, которые читаются в фоне, а телефон к вечеру был под давлением памяти.
-->

---

<Kicker>10 октября, 21:23 · ветка exp/memory-loading</Kicker>

# Одна фраза — и цикл на всю ночь

<div class="grid grid-cols-[0.9fr_1.22fr] gap-6 mt-1">
<div>

<PhoneChat :messages="[
  { who: 'human', time: '21:23', text: '… now lets do the loop for optimizing  memory footprint and loading times. . you can create a new branch and start developing. build strong methodology as you progress.', gloss: 'теперь цикл на память и время загрузки — новая ветка и сильная методология по ходу', hot: true },
  { who: 'event', time: '22:23', text: '<code>17416cd</code> · L1 вместе с карточкой и харнессом' },
]" />

<div class="quiet">
<div class="qn">16 ч 51 мин</div>
<div class="qt">до следующей реплики человека. За это время — <b>27 коммитов</b>, два сжатия контекста и ни одного вопроса.</div>
</div>

<div class="rule-card mt-3">
<span class="pixel hl xsmall">правило коммита</span>
<span class="mono xsmall ink" lang="en">«Commit an increment only when every gate passes, it is measurably faster or smaller … and neither load time nor frame time is measurably worse; otherwise record it here and revert.»</span>
</div>

</div>
<div>

<div class="chart-h">одна ступень цикла — как её определяет карточка, и сколько их было за ночь</div>

<LoadLoop />

</div>
</div>

<div class="source">сессия 1f9218ae (UTC+2) · docs/research/MEMORY_LOADING.md (Plan, Gates) · 17416cd · data/loading_night.json, loading_steps.json, loading_method.json</div>

<style>
.chart-h { font-size: .68rem; color: var(--muted); margin-bottom: .3rem; }
.quiet { display: flex; gap: .7rem; align-items: center; margin-top: .7rem; background: rgba(255,255,255,.03); border: 1px solid var(--hair); border-radius: 12px; padding: .45rem .7rem; }
.quiet .qn { font-family: var(--font-pixel); font-size: 1.35rem; color: var(--naruto); white-space: nowrap; }
.quiet .qt { font-size: .68rem; line-height: 1.35; color: var(--ink-2); }
.quiet b { color: var(--ink); }
.rule-card { display: flex; flex-direction: column; gap: .15rem; background: rgba(255,255,255,.03); border: 1px solid var(--hair); border-radius: 10px; padding: .35rem .7rem; }
</style>

<!--
Реплика — дословно, с двойным пробелом и лишней точкой автора. Через час первый коммит L1 принёс ветку exp/memory-loading, карточку исследования и харнесс tools/crossplatform/load_memory.py: загрузка и память на Mac и на A12, A/B вперемешку, медианы и диапазоны. Базовая линия снята в этот час: загрузка на A12 122,1–124,6 с, на Mac 5,05–5,43 с; шум — ±0,6 с и ±10 МиБ на телефоне.

Шесть шагов ступени — из карточки. Ревью — отдельный агент только для чтения: 27 ступеней прошли его до гейта, четырём (L2, L8, M3, L10) оно не требовалось — значения равны по построению. Гейт — те же проверки, что в главе 14: 10 сценариев равны замороженным эталонам, 1 832 кадра headless побайтно, AppKit и эмулятор Android, тесты затронутых модулей; плюс A/B загрузки и памяти на Mac и на A12 против прошлой сборки.

Следующая реплика человека — 11 октября в 14:14. До неё агент сам довёл 27 коммитов, пережил два автоматических сжатия контекста (06:20 и 13:26) и в 12:31 сам остановился с отчётом.
-->

---
clicks: 1
---

<Kicker>Galaxy A12 · от иконки до меню · один типичный прогон</Kicker>

# Две минуты на экране загрузки

<p class="lead">Загрузка была занята делом: 131 с из 135 главный поток провёл на процессоре. Обе полосы — в одном масштабе и в настоящем времени.</p>

<LoadRace />

<LoadProfile class="mt-4" />

<div class="source">ml-baseline-20261010.json (0034e45) · ml-l20-…-20261011.json (e184b10, gate + ab4) · MEMORY_LOADING.md (Baseline) · data/loading_race.json</div>

<style>
.lead { font-size: .8rem; color: var(--ink-2); margin: -.4rem 0 .55rem !important; }
</style>

<!--
Клик (или кнопка) запускает гонку: обе полосы идут в одном масштабе и в настоящем времени; переключатель ×10 ускоряет. В PDF — момент, когда новая сборка уже в меню, а старая только четвёртую секунду на экране загрузки.

Прогоны — не медианы по фазам, а один настоящий прогон каждой сборки: медианный по времени «запуск → загружено». До — ml-p0-noise-2 из базовой линии (0034e45, без звука): старт 2,93 с, меню 5,74 с, загрузка 123,25 с, всего 131,92 с. После — ml-l20-ab4-05 (e184b10, финальная сборка, звук эффектов включён): старт 1,58, меню 5,30, загрузка 5,83, всего 12,71 с.

«Меню до загрузки» — фаза, которую сценарий проходит перед загрузкой данных: главный поток строит битмапы переднего меню. Сейчас старт и эта фаза — больше половины пути до меню; именно туда цикл пошёл днём (L20).

Профиль до цикла: simpleperf с DWARF-стеками, 12 308 сэмплов главного потока за загрузку, доли включительные. Разбор каталога 49 % (объекты 32 %, расшифровка DAT 16 %, тела кадров 9,5 %), чтение и проверка пакета каталога 25 % (переносимый SHA-256 15 %, Bitmap.init 8,8 %). На Mac — 99 % разбор DAT, из них три четверти на копирование структуры Stream за каждый символ.
-->

---

<Kicker>10 октября 22:23 → 11 октября 19:43 · 34 коммита</Kicker>

# Ночь по часам

<LoadNight />

<div class="source">git log 0034e45..6b4bffd · docs/evidence/ml-*.json (медианы гейтов) · сессия 1f9218ae (время) · data/loading_steps.json, loading_night.json</div>

<!--
Каждая точка — гейт ступени в момент её коммита; значение — медиана новой сборки в её собственном A/B (на телефоне 3 прогона, на Mac 3). Цвет точки — семейство приёма, как на следующем слайде. Кольца — ступени, которые не вошли: L21 (отклонена), M8 (ждала решения человека), M9 (отложена). Ромбы на оси — две проверки, которые поменяли методику: 15:32 — прогрев и дрейф телефона, 17:56 — аудит RAM.

Тяните по графику или нажмите «прогнать ночь»: карточка внизу показывает A/B этой ступени с диапазонами, и что нашло ревью. Переключатель — Galaxy A12 или Mac (на Mac — headless-сборка без проверок эксклюзивности; память — phys_footprint_peak).

Что видно. До следующей реплики человека (16 ч 51 мин) загрузка на телефоне упала со 123,9 до 5,2–5,4 с. Самые большие ступени — L1, L2, L3, L5: копии и параллельность. Память падает двумя уступами: M1 (сжатые спрайт-листы, 01:10) и звук с копиями днём. После 10:05 загрузка не падает: её ограничивает фоновое чтение пакетов, а телефон к вечеру медленнее.

Штриховка — агент закончил и ждал человека: 12:31–14:15 (отчёт после M5c) и 15:33–16:12 (отчёт после M5d; в 16:12 человек спросил «what are u waiting for?», агент ответил «Nothing.» и взял L20). Синие точки — реплики человека, их 13; треугольники — автоматические сжатия контекста.

С 15:22 гейты меряют со звуком эффектов, M8 и M9 — ещё и с музыкой: пик памяти на этих точках сравним только внутри своего гейта.
-->

---

<Kicker>что дала каждая ступень · только измеримые A/B</Kicker>

# Куда делись две минуты и гигабайт

<LoadWaterfall class="mt-1" />

<div class="after">
<span class="i-pixelarticons-alert ai" />
<div>После 10:05 загрузка больше не падала: экран загрузки ждёт пакеты, которые читаются в фоне (L13), а телефон к вечеру был под давлением памяти. Финальная сборка — <b>5,4–6,3 с</b>, это видно на прошлом слайде.</div>
</div>

<div class="source">docs/evidence/ml-*.json (phone.summary: прошлая и новая сборка в одном гейте) · MEMORY_LOADING.md (Ledger) · data/loading_steps.json</div>

<style>
.after { display: flex; gap: .5rem; align-items: flex-start; margin-top: 1.3rem; font-size: .68rem; line-height: 1.38; color: var(--ink-2); background: rgba(255,255,255,.03); border: 1px solid var(--hair); border-radius: 10px; padding: .4rem .7rem; }
.after b { color: var(--ink); }
.ai { flex: none; width: 1rem; height: 1rem; color: var(--warning); margin-top: .05rem; }
</style>

<!--
Ширина отрезка — выигрыш ступени в её собственном гейте: медиана прошлой сборки минус медиана новой, только если диапазоны не пересекаются (по протоколу карточки это и есть «измерено»). Наведите на отрезок — подсказка с A/B и диапазонами.

Загрузка: сумма девятнадцати измеренных выигрышей — 119,0 с, а разница медиан 123,9 → 5,24 с — 118,7 с. Разница в 0,3 с — шум между сессиями: гейты мерили в разные часы. Ширины чуть ужаты под 118,7 с.

Самое большое семейство — «на месте, без копий»: 64 с из 119. Второе — параллельность и железо: 37 с, из них 30,6 с — одна ступень L3, пакеты на всех ядрах.

Память: измеримые шаги объясняют 991 МиБ из 1 033. Штриховка — 42 МиБ, которые отдельно не измерены: M6 и M5c сэкономили по куче Mac (−46 и −16 МБ), но их диапазоны на телефоне перекрылись с прошлой сборкой; итоговый замер к тому же шёл со звуком эффектов. Три ступени загрузки попутно сняли и память: L4 (−20), L13 (−17,5: стартовый пакет больше не читается дважды), L18+19 (−27: общие пустые слоты кадров).
-->

---

<Kicker>четыре семейства приёмов загрузки</Kicker>

# Копии, ядра, перебор

<LoadFamilies class="mt-1" />

<div class="source">MEMORY_LOADING.md (Plan, Ledger, Method notes) · docs/evidence/ml-l1 … ml-l12 · data/loading_steps.json</div>

<!--
Сумма по семейству — только ступени с измеримым выигрышем; L13 (чтение пакетов заранее, пока идёт меню) отнесено к параллельности.

Ловушка копий. Значения в Swift копируются при записи, если на них есть вторая ссылка. В загрузчике порта вторая ссылка была почти всегда — ради отката: «A copy-on-write value taken for a rollback that an outer layer already provides makes every mutation copy the whole structure». Правило из карточки: прежде чем работать на месте, доказать по коду, что внешний слой и так выбрасывает всё при ошибке, и оставить откат по умолчанию в публичном API.

L1 — модель DAT-файла копировала всю структуру Stream (четыре массива байтов) на каждый прочитанный символ; L2 — свойства bitmaps, sounds, frameHeap были вычисляемыми get/set, и запись в одну картинку копировала массив из ~1 800; L5 — эффект картинки копировал таблицы картинок, поверхностей и DC; L16 — первое выделение каждого объекта копировало все прежние (~15 000).

Железо. L12 нашёл на телефоне неожиданное: воркеры Dispatch работали только на ядрах 0–3 — они унаследовали привязку главного потока к быстрому кластеру. L11: на Android нет CryptoKit; блочная функция на инструкциях ARMv8 SHA-2 включается, только если на двенадцати входах через границы блоков даёт те же дайджесты, что Swift.

Перебор: «Quadratic scans show up as a few percent that grow with the content» — замена на отсортированную структуру и тест против старого перебора на сгенерированных входах.
-->

---

<Kicker>M1 · 11 октября, 01:10 · пик на A12 1 570 → 975 МиБ</Kicker>

# Матч трогает 77 картинок из 891

<LoadSurfaces class="mt-1" />

<div class="grid grid-cols-4 gap-3 mt-2">
<StatTile value="1 570 → 975" suffix="МиБ" label="пик памяти A12, гейт M1" sub="Mac: 2 049 → 1 466 МБ" size="sm" accent="var(--s3)" />
<StatTile value="46,3 → 46,4" suffix="с" label="загрузка A12 в том же гейте" sub="в пределах шума" size="sm" accent="var(--s1)" />
<StatTile value="+1,1 с" label="первая версия M1: загрузка" sub="исправлено до коммита" size="sm" accent="var(--warning)" />
<StatTile value="~13×" label="сжатие: свой кодек LZ4 block" sub="распаковка при первом чтении" size="sm" accent="var(--s3)" />
</div>

<div class="source">MEMORY_LOADING.md (Ledger: Attribution probe, M1, M3, RAM audit) · ml-m1, ml-m3, ml-ram-audit · 8aceb53 · data/loading_method.json</div>

<!--
Слева — замер 10 октября (сборка с подсчётом, не закоммичена): из 891 поверхности (1,14 ГБ выделено) за целый матч VS трогаются 65–77 (55–61 МБ), а декодированные пиксели читаются 77 раз. Самым большим держателем резидентной памяти были байты файлов спрайт-листов: 613 МБ каталога и 65 МБ арен.

M1: листы от 64 КиБ хранят байты сжатыми — свой Swift-кодек формата LZ4 block, ~13× на этих листах — и распаковываются, когда поверхности впервые нужны пиксели. Первый гейт M1 намерил +0,9 с старта и +1,1 с загрузки; сжатие стартового пакета перенесли на все ядра, и время вернулось. Итог: пик A12 1 570 → 975 МиБ, загрузка 46,3 → 46,4 с — без изменений. M3 через три часа: буфер компрессора сохранял резерв — 130 МБ выделено под 52 МБ данных.

Справа внизу — куча A12 при RAM-аудите 11 октября (финальная сборка L20): выделено 1 597 МиБ, а грязных страниц 405–450 МиБ, свободно внутри аллокатора 19–46 МиБ. Разница — около 1,15 ГиБ нетронутых страниц поверхностей: память выделена calloc и ни разу не записана.
-->

---
clicks: 1
---

<Kicker>11 октября, 14:14 — 15:22 · M5c → M5d</Kicker>

# Человек почуял — агент измерил

<div class="grid grid-cols-[1fr_1.05fr] gap-6 mt-1">
<div>

<PhoneChat :messages="[
  { who: 'human', time: '14:14', text: 'we must not compromise on performance (loading speed and frame time) while we optimize memory footprint btw', gloss: 'не жертвуем скоростью загрузки и временем кадра ради памяти', hot: true },
  { who: 'human', time: '14:17', text: 'if you will add full blown frame time gate will it hurt cycle time and development speed?' },
  { who: 'human', time: '14:18', text: 'we shoudl balance' },
  { who: 'human', time: '14:20', text: 'suspicious of b8d1c9b2437ffb161cb1d6e6316fb9ae89132c7f commit. i might be wrong but feels like we added cpu overhead', gloss: 'подозреваю коммит M5c: кажется, добавили нагрузку на CPU', hot: true },
  { who: 'agent', time: '14:20', text: 'You’re likely right to suspect it.' },
  { who: 'event', time: '15:22', text: '<code>ef7a6b7</code> · M5d: исправление и аудит времени кадра' },
]" />

</div>
<div>

<div class="chart-h">микшер звука на A12 · нс на голос-кадр · 8 голосов, 48 кГц, выход побитно тот же</div>

<LoadMixer stepwise />

<div v-click="1" class="inplay">
<span class="ih">в игре со звуком, гейт M5d, мс на тик</span>
<span>поток звука <b>1,12 → 1,03–1,07</b></span>
<span>главный <b>10,39 → 10,29</b></span>
<span>рендер <b>7,38 → 7,03</b></span>
</div>

<div class="why">
<div><b>Почему гейты не видели.</b> Все прогоны шли без звука, а без звука хост Android не вызывает микшер; headless не микширует вовсе. M5c перенёс перевод сэмплов из загрузки в поток звука — туда, где ничего не мерили.</div>
<div><b>Что стало с гейтом.</b> Баланс, как просил человек, — три яруса: время кадра в каждом A/B со звуком, почти даром; полный A/B на 40 минут — только для горячих путей; на вехах — против старта ветки.</div>
</div>

</div>
</div>

<div class="source">сессия 1f9218ae (UTC+2) · b8d1c9b · ef7a6b7 · ml-frame-time-audit (mixer) · ml-m5d (phone) · MEMORY_LOADING.md · data/loading_method.json</div>

<style>
.chart-h { font-size: .68rem; color: var(--muted); margin-bottom: .25rem; }
.inplay { display: flex; flex-wrap: wrap; gap: .15rem 1rem; align-items: baseline; margin-top: .3rem; font-size: .68rem; color: var(--ink-2); background: rgba(255,255,255,.03); border: 1px solid var(--hair); border-radius: 10px; padding: .3rem .65rem; }
.inplay .ih { width: 100%; font-size: .64rem; color: var(--muted); }
.inplay b { color: var(--ink); }
.why { display: flex; flex-direction: column; gap: .35rem; margin-top: .6rem; font-size: .68rem; line-height: 1.36; color: var(--ink-2); }
.why b { color: var(--ink); }
</style>

<!--
Клик показывает M5d.

Реплики — дословно, время местное; опечатка «shoudl» — авторская. M5c (12:30) хранил звук 8/16-битным PCM вместо float — 16 МБ вместо 32 на куче Mac — и переводил сэмпл в микшере при чтении. Гейт его пропустил: на телефоне пик памяти не разделил сборки, загрузка не изменилась, а время звукового потока не мерили.

Аудит: начало ветки против HEAD на A12, vs и Demo, три раунда вперемешку — главный поток 11,05 против 11,27 мс (vs), 11,71 против 11,72 (Demo), рендер 7,51/7,60 и 6,08/6,15: все пары перекрываются. Но эти прогоны микшер не вызывали. Бенчмарк цикла микшера нашёл цену M5c: +31 % на голос-кадр — ≈ 4,4 мс процессора звукового потока на секунду звука при 8 голосах.

M5d: PCM читается по указателю там, где индексы доказуемо внутри буфера (шаг ≥ 0 и, при зацикливании, короче буфера), иначе — прежние проверяемые чтения; моно-голос читает кадр один раз на оба канала. 36,2 нс — быстрее float-цикла до M5c, а 16 МБ экономии остались. Ревью нашло одно: отрицательный шаг (хосты его не дают) пошёл бы по быстрому пути — исправлено до гейта.

В 15:33 агент написал: «You were right about b8d1c9b: it added CPU overhead.»
-->

---
clicks: 1
---

<Kicker>правила, которые карточка дописала за ночь</Kicker>

# Мерить честно — тоже работа цикла

<div class="grid grid-cols-[1fr_1.02fr] gap-6 mt-1">
<div>

<div class="rules">
<div class="r"><span class="rn pixel">1</span><div><b>A B A B A в одной сессии.</b> Новая сборка — 3 прогона, прошлая — 2, вперемешку; медианы и диапазоны. Ступень засчитана, если диапазоны не пересекаются. Шум базы: ±0,6 с и ±10 МиБ на A12.</div></div>
<div class="r"><span class="rn pixel">2</span><div><b>Прогрев.</b> Первая сборка в серии всегда ждала фоновое чтение дольше всех — 3,1, 1,4 и 1,4 с, даже без звука, где изменение не работало. Теперь перед замером — прогон, который не считается.</div></div>
<div class="r"><span class="rn pixel">3</span><div><b>Не сравнивать по журналу.</b> Телефон дрейфует за день: подозрение на регресс проверяется A/B двух сборок в одной сессии.</div></div>
<div class="r"><span class="rn pixel">4</span><div><b>Мерить как в игре.</b> Все прогоны глушили музыку — а музыка оказалась самым большим держателем памяти в матче.</div></div>
<div class="r"><span class="rn pixel">5</span><div><b>Упал тест — ещё не упал код.</b> В гейтах L6, M6, L17 и M5b ошибался новый тест самого агента: тест исправлен, сьюты перезапущены на тех же исходниках, упавший лог оставлен в evidence.</div></div>
</div>

</div>
<div>

<div class="chart-h">запуск → меню на A12, каждый прогон — точка</div>

<LoadDrift stepwise />

<div class="rev">
<div class="rh pixel">что нашло ревью до гейта</div>
<div><code>L12</code> поток не стартовал бы — <code>done.wait()</code> висел бы вечно</div>
<div><code>L4</code> новая проверка размера меняла ошибку для битого файла</div>
<div><code>L17</code> <code>lstat</code> иначе переводит ENAMETOOLONG</div>
<div><code>M6</code> <code>M5d</code> редкие пути, которых хосты не дают</div>
</div>

</div>
</div>

<div class="source">MEMORY_LOADING.md (Comparison protocol, Method notes) · ml-menu-phase-check (db3c605) · ml-m5c · ml-*.json (review) · data/loading_method.json</div>

<style>
.chart-h { font-size: .68rem; color: var(--muted); margin-bottom: .2rem; }
.rules { display: flex; flex-direction: column; gap: .4rem; }
.rules .r { display: flex; gap: .6rem; font-size: .7rem; line-height: 1.36; color: var(--ink-2); background: var(--surface); border: 1px solid var(--hair); border-radius: 10px; padding: .4rem .65rem; }
.rules .rn { color: var(--naruto); font-size: .95rem; line-height: 1.1; }
.rules b { color: var(--ink); }
.rev { margin-top: .45rem; font-size: .66rem; line-height: 1.45; color: var(--ink-2); border-top: 1px solid var(--grid); padding-top: .3rem; }
.rev .rh { font-size: .66rem; color: var(--naruto); margin-bottom: .1rem; }
.rev code { font-size: .6rem !important; }
</style>

<!--
Клик показывает нижний ряд.

Сверху — как выглядел бы «регресс», если сравнивать по журналу: гейт S2 в 10:41 — 11,19–11,24 с от запуска до меню, гейт M5c в 12:30 (в нём уже M5b) — 12,34–12,59 с. Снизу — A/B S2 против M5b в одной сессии в 15:30, с прогоном-прогревом: 12,71–12,75 против 12,62–12,70 с. Одинаково. Медленнее стал телефон: простаивал, но держал 1,34 ГБ в zram и 630 МБ свободно. Прогоны, которые после установки заново распаковывали ресурсы APK, на графике не показаны — с ними сравнивать нельзя.

Ещё два правила из Method notes: «One gate for two changes only when one alone is below the noise floor» (L14 с L15, L18 с L19) и «A test-only failure … gets its suites rerun from a scratch worktree»: в гейтах M6, L17, M5b и L6 падал собственный новый тест агента, не код игры; упавший лог остаётся в evidence.

Ревью: 27 независимых, только для чтения, до гейта. Ещё два случая: в L3 ревью заметило, что подменённый огромный файл читался бы на всех ядрах до первой ошибки, — размер проверяется до чтения с L4; в S2 при сбое распаковки может быть назван другой файл — записано как риск.
-->

---

<Kicker>11 октября, 17:17 — 20:00</Kicker>

# Цикл остановил человек

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-1">
<div>

<div class="dec">
<div class="d"><span class="t mono">17:17</span><span class="tag2 info">новое задание</span><div>Аудит RAM не дольше двух часов. Продолжать, только если найдётся <b>30–50 МиБ</b> при разумной сложности.</div></div>
<div class="d"><span class="t mono">17:38</span><span class="tag2 bad">L21 отклонена</span><div>Поведение равно, выигрыша нет ни на A12, ни на Mac, а кода больше — откат, дифф сохранён.</div></div>
<div class="d"><span class="t mono">17:56</span><span class="tag2 info">аудит</span><div>Пик 565 МиБ со звуком. Кандидаты на <b>55–90 МиБ</b> — цикл идёт дальше. Первая — музыка: её не включал ни один прогон.</div></div>
<div class="d"><span class="t mono">19:05</span><span class="tag2 warn">M8 ждёт решения</span><div>Музыка потоком: пик <b>618 → 568 МиБ</b>, но поток музыки +0,5 мс на тик. По правилу 14:14 — решать человеку.</div></div>
<div class="d"><span class="t mono">19:43</span><span class="tag2 warn">M9 отложена</span><div>A12 −36–40 МиБ PSS, но на Mac footprint вырос на 65–90 МиБ. Не влита.</div></div>
</div>

</div>
<div>

<PhoneChat :messages="[
  { who: 'human', time: '17:17', text: 'Не продолжай его ради количества коммитов.', gloss: 'из задания на аудит RAM' },
  { who: 'agent', time: '19:08', text: '<b>Влить M8 (Recommended)</b> · Отказаться от M8 · Влить, но декодировать заранее' },
  { who: 'human', time: '19:09', text: '0.5ms на слабом телефоне или это 0.5 на mac mini?' },
  { who: 'agent', time: '19:09', text: 'Это 0,5 мс на слабом телефоне, Galaxy A12.' },
  { who: 'human', time: '19:25', text: 'останавливаемся на достигнутом. эксперимент с стримингом звуков с диска я вижу рискованным из-за потенциальных хардверных ошибок и скорости чтения. пора вливаться в main всеми нашими доработками', hot: true },
  { who: 'event', time: '19:43', text: '<code>6b4bffd</code> · стоп: M8 отклонена, M9 отложена' },
  { who: 'human', time: '20:00', text: 'да, пушь main и dev/crossplatform тоже' },
]" />

</div>
</div>

<div class="source">сессия 1f9218ae (UTC+2) · MEMORY_LOADING.md (Ledger) · ml-l21, ml-ram-audit, ml-m8, ml-m9 · 9ed8f6c · 85fab5b · d90472a · 6b4bffd</div>

<style>
.dec { display: flex; flex-direction: column; gap: .38rem; }
.dec .d { display: grid; grid-template-columns: 2.6rem auto; column-gap: .55rem; row-gap: .1rem; align-items: baseline; font-size: .68rem; line-height: 1.35; color: var(--ink-2); background: var(--surface); border: 1px solid var(--hair); border-radius: 10px; padding: .35rem .6rem; }
.dec .d > div { grid-column: 1 / -1; }
.dec .t { font-size: .66rem; color: var(--muted); }
.dec b { color: var(--ink); }
.tag2 { justify-self: start; font-size: .62rem; border-radius: 999px; padding: 0 .5rem; border: 1px solid; color: var(--ink); }
.tag2.info { border-color: rgba(57,135,229,.6); background: rgba(57,135,229,.14); }
.tag2.bad { border-color: rgba(208,59,59,.6); background: rgba(208,59,59,.14); }
.tag2.warn { border-color: rgba(250,178,25,.55); background: rgba(250,178,25,.12); }
</style>

<!--
В 17:17 человек вставил задание на аудит RAM по-русски. Ключевые строки, дословно: «Продолжай реализацию, если аудит покажет обоснованный суммарный резерв хотя бы 30–50 МиБ с разумной сложностью», «Если аудит не найдёт такого резерва … — заверши текущие проверки и останови луп. Не продолжай его ради количества коммитов» и «Достижение конкретной цифры памяти не важнее сохранения поведения и скорости».

Аудит нашёл кандидатов на 55–90 МиБ: музыка потоком (24–34 МиБ PSS в матче, 40–94 на пике), общие однородные страницы (~15), PCM микшера из записей звука (~16), копии журналов (20–40, сложно). Музыка: плеер Android читал весь ALAC-файл и декодировал трек целиком; с музыкой пик 607–630 МиБ против 536–567 без неё.

M8 прошла все проверки поведения; загрузка, главный поток и рендер перекрываются, срывов звука ноль, процессора от запуска до конца матча даже на ~3 с меньше. Но декодирование переехало из всплеска в начале трека в обратный вызов музыки: +0,5 мс на тик (1,69–1,72 против 1,16–1,22 мс). Агент спросил человека через вопрос с вариантами и рекомендовал влить. Человек отказался — по своей причине: чтение с флеш-памяти во время игры. Коммит M8 остался только в локальной ветке exp/memory-loading-m8 (f22270b), как запись.

M9: пока цикл ждал, агент прогнал следующую ступень. На A12 конец матча 504–510 МиБ PSS против 545–592, но macOS malloc держал около 48 МБ освобождённой после загрузки памяти грязной — footprint Mac вырос. Правило карточки: изменение памяти, поднимающее footprint одного хоста, сначала должно это устранить. Отложена с диффом и evidence.

В 19:47 агент слил обе ветки в локальный main fast-forward'ом и спросил разрешения на push — внешнее действие. В 20:00 человек разрешил.
-->

---

<Kicker>итог · сборка e184b10 против 0034e45</Kicker>

# Что изменилось — и что нет

<LoadScore class="mt-1" />

<div class="cav">
<span class="i-pixelarticons-alert ai" />
<div>Один телефон, debuggable APK, сценарий vs по скрипту, сеть выключена; медианы прогонов вперемешку, «до» без звука, «после» со звуком эффектов. Игра та же: на каждой ступени 10 сценариев равны эталонам, кадры побайтно.</div>
</div>

<div class="source">ml-l1 (ml-p0) · ml-l20 (+ab4) · ml-s2 (fresh) · ml-ram-audit · ml-frame-time-audit · MEMORY_LOADING.md (Status) · data/loading_*.json</div>

<style>
.cav { display: flex; gap: .55rem; align-items: flex-start; margin-top: .7rem; font-size: .68rem; line-height: 1.38; color: var(--ink-2); background: rgba(255,255,255,.03); border: 1px solid rgba(250,178,25,.35); border-radius: 10px; padding: .4rem .7rem; }
.ai { flex: none; width: 1rem; height: 1rem; color: var(--warning); margin-top: .05rem; }
</style>

<!--
Полоса — значение «после» как доля «до» в своей строке; у каждой строки свой масштаб.

Экран загрузки: база ml-p0 — медиана двух прогонов в гейте L1, 123,9 с (шумовые прогоны базы — 122,1–124,6). Финальная сборка L20 — 7 прогонов гейта и A/B 4 + 4: 5,9 с (5,4–6,3). Лучший гейт — L18+19 в 10:05, 5,24 с. Карточка пишет «~5,5 с».

Запуск → меню: 132,7 → 12,7 с. Первый запуск после установки (распаковка ресурсов APK) — отдельный A/B с удалением маркера распаковки: 24,7 → 16,8 с; дальше ограничивает запись 726 МБ на флеш.

Время кадра: аудит начала ветки против HEAD на A12 без звука — все пары перекрываются; в игре со звуком гейт M5d: главный 10,29 против 10,39 мс, рендер 7,03 против 7,38, поток звука 1,12 → 1,03–1,07 мс на тик.

Mac: headless-сборка без проверок эксклюзивности, 3 + 3 прогона; 5,41 → 0,33 с, пик 2 004 → 681 МБ.

Чего нет: игра руками на телефоне после цикла здесь не замерялась; ветку влили в main вместе с exp/core-realtime по слову человека; M8 и M9 не влиты; кандидаты на ещё 14–40 МиБ записаны в карточке.
-->
