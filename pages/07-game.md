---
layout: chapter
num: 7
total: 20
kicker: Глава седьмая
dates: 29 сентября — 2 октября
image: /img/screens/12-all-17-backgrounds-grid.jpg
stats: все режимы за день · 200 000 тиков без остановки · сетевой матч двух приложений
---

# Вся игра

Когда ядро стоит на месте, режимы подключаются один за другим. Дальше — износ, причуды оригинала и сеть.

---

<Kicker>29 сентября · 34 коммита</Kicker>

# Все режимы за один день

<div class="grid grid-cols-3 gap-3 mt-2">
<WindowFrame src="/img/screens/07-mission-stage-1-1-storyboard.png" height="122px" title="Stage 1-1 · efcdedc" caption="Mission: логика стейджей 437860 — диалог Какаши, бой, Summary" />
<WindowFrame src="/img/screens/09-war-battle-cave.png" height="122px" title="War · 4651853" caption="War: логика битвы 43a860, десятки войск на арене" />
<WindowFrame src="/img/screens/10-team-tournament-bracket-winner.png" height="122px" title="Team Tournament · 16f36a0" caption="Tournament и Team Tournament: сетка и победитель" />
<WindowFrame src="/img/screens/06-demo-arena-ai.png" height="122px" title="Demo · 6c384fc" caption="Demo: компьютерные бойцы на арене" />
<WindowFrame src="/img/screens/11-summary-table-values.png" height="122px" title="Playback · d86c783" caption="Просмотр записей: zlib 1.1.4, пролог проигрывания 41bd24" />
<WindowFrame src="/img/screens/17-gdi-text-controls.png" height="122px" title="CONTROL SETTINGS · 69ffa8e" caption="Настройки управления: клавиши игрока сохраняются" />
</div>

<div class="source">efcdedc · 4651853 · 6c384fc · d86c783 · 16f36a0 · abf941f · 69ffa8e · 553d100</div>

---

<Kicker>записи матчей</Kicker>

# Анатомия `.lfr`

<LfrAnatomy class="mt-3" />

<div class="grid grid-cols-3 gap-4 mt-4 small ink2">
<div><b>Вшитый zlib 1.1.4.</b> Современный zlib 1.2.12 расходится с ним в 53 случаях корпуса — порт вендорит именно 1.1.4. Реализацию <code>longest_match</code> оригинал выбирает по CPUID; порт объявляет сигнатуру <code>0x600</code> и совпадает на всех 4 353 858 вызовах.</div>
<div><b>Баг в загрузчике.</b> 0x43e620 выделяет 0x630e18 байт, а распаковывает с ёмкостью 0x631200 — на 1 000 больше. На повреждённом файле это переполнение кучи; порт его документирует и отклоняет.</div>
<div><b>Попиксельно.</b> «A recorded VS match plays back pixel-identical to the recording outside the playback bar» — запись, сделанная на Mac, проигрывается кадр в кадр вместе с полным Summary.</div>
</div>

<div class="source">tools/original_replay.py · docs/research/REPLAY_TICK.md · REPLAY_WRITER.md · REPLAY_COMPRESSION.md · d786b52 · d86c783</div>

---

<Kicker>30 сентября · на износ</Kicker>

# 200 000 тиков и утечка памяти

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-2">
<div>

<div class="xsmall muted mb-1">рост RSS во время длинных VS-сессий, МБ в минуту</div>

<div class="bars">
<div class="bar-row"><span class="bl">до исправления, 20 матчей</span><span class="bt"><i style="width: 100%" /></span><span class="bv">72</span></div>
<div class="bar-row"><span class="bl">экран хранит счётчики, а не журнал отрисовки</span><span class="bt"><i style="width: 16.7%" /></span><span class="bv">12</span></div>
<div class="bar-row"><span class="bl">курсоры итераций только с ресурсами</span><span class="bt"><i style="width: 7.6%" /></span><span class="bv">4–7</span></div>
<div class="bar-row"><span class="bl">Demo, 27 минут после обоих исправлений</span><span class="bt"><i style="width: 5.6%" /></span><span class="bv">4</span></div>
</div>

<p class="small ink2 mt-3">Footprint за 20 матчей рос с 2,0 до 3,2 ГБ; после исправлений — ровно 2,0 ГБ на каждом замере. Причины: ~130 записей отрисовки на тик (714 587 за три матча) и ~9 000 сохранённых курсоров итераций на матч.</p>

</div>
<div>

<div class="grid grid-cols-2 gap-3">
<StatTile :value="22" label="длинных прогона Demo, War и Stage" size="sm" />
<StatTile :value="200000" label="тиков в самом длинном прогоне без остановки" size="sm" accent="var(--s1)" />
<StatTile :value="1282772" label="вызова AI за 95 матчей Demo" size="sm" accent="var(--s3)" />
<StatTile value="15,1 с" label="на 2 000 итераций меню вместо растущих 16 → 25 с" size="sm" accent="var(--s4)" />
</div>

<p class="small ink2 mt-3">Каждая неподдержанная ветвь в прогоне останавливает игру событием <code>boundary</code>. Так находились причуды оригинала: кадр 1000 у <code>ironsand.dat</code>, незаписанные слова прыжка у <code>wind.dat</code>…</p>

</div>
</div>

<div class="source">e0d1b64 · 873e039 · 83f65a6 · 2278c4d · 36528c9 · docs/research/APPLICATION_SOAKS.md · data/evidence/memory-soak.json</div>

<style>
.bars { display: flex; flex-direction: column; gap: 0.45rem; }
.bar-row { display: grid; grid-template-columns: 12.5rem 1fr 2.2rem; align-items: center; gap: 0.6rem; }
.bl { font-size: 0.66rem; color: var(--ink-2); line-height: 1.2; }
.bt { height: 12px; }
.bt i { display: block; height: 12px; background: var(--s1); border-radius: 0 4px 4px 0; }
.bv { font-size: 0.8rem; font-weight: 650; color: var(--ink); }
</style>

---

<Kicker>необычные состояния</Kicker>

# Когда оригинал читает за краем памяти

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2">
<div>

<WindowFrame src="/img/screens/05-f8-full-pool-chaos.png" title="NTSD Native — F8 × 88" caption="F8 сыплет предметы, пока пул из 400 слотов не заполнится" />

</div>
<div class="small ink2">

**F8 на полном пуле.** Номер слота оригинал берёт из слова кадра стека `SP+34`: каждый вызов 41f2c7 пишет туда −4 − World, а цикл жизненного цикла может его перезаписать. Если там 0 — предметом становится Наруто игрока 1. Обычно же там −4 − World, и чтение таблицы Actor по `0xff2f6084` падает с access violation. Порт воспроизводит обе ветки: вторая — объявленный *Source fault*.

**Кадр 1000.** Лечащий удар kind 8 ставит атакующему кадр 1000, и оригинал читает Frame по `Object+0x5c464` — далеко за концом аллокации. Ещё 41 <code>wpoint</code> использует <code>weaponact</code> 1000, 9998 или −888.

<div class="card-soft mt-2">
<div class="mono xsmall hl">"The review found three errors, all confirmed."</div>
<div class="xsmall muted mt-1">независимое ревью политики «кадры за пределами Object читаются как отсутствующие», 7bf3624</div>
</div>

</div>
</div>

<div class="source">8d107f1 · f4cdcbb · 457cc7d · 7bf3624 · b729b3f · docs/research/APPLICATION_OUT_OF_OBJECT_FRAMES.md</div>

---

<Kicker>30 сентября, 16:09 → 1 октября, 10:16 · F8 на полном пуле</Kicker>

# Пропуск, который откатило ревью

<p class="lead">Когда свободного слота нет, проход запрошенных предметов берёт номер из слова <code>SP+34</code>. В 16:53 агент записал, что его значение «не смоделировано», и стал пропускать предмет — как за 44 минуты до этого со случайным выпадом в War. Независимое ревью нашло, кто пишет это слово: <span class="q">«its slot word is not unknown»</span>.</p>

<BSlotWord />

<div class="words">
<div class="wd hot">
<div class="wh"><code>−4 − World</code><span>обычный случай</span></div>
41f2c7 пишет его при каждом вызове. Чтение таблицы Actor по <code>0xff2f6084</code>: World статичен (<code>0x458b00</code>), EXE с фиксированной базой и без LAA — оригинал падает. В порту — <b>Source fault</b>.
</div>
<div class="wd">
<div class="wh"><code>0</code><span>обратный отсчёт дошёл до нуля</span></div>
Слот 0 пересобирается — <b>Наруто игрока 1 становится предметом</b>. В 10:16 так и вышло на 89-м нажатии F8. Дальше HUD читает у предмета картинку <code>small:</code> без проверки на null — именованная остановка.
</div>
<div class="wd">
<div class="wh"><code>400 · адреса</code><span>решает куча Windows</span></div>
Счётчик 400, курсоры каталога и адреса Actor зависят от раскладки кучи Windows, а не от EXE. Это <b>объявленная остановка</b>.
</div>
</div>

<div class="source">d8481cb · d26e412 · 698f76a · f4cdcbb · 8d107f1 · docs/research/APPLICATION_FULL_POOL_ITEM.md · APPLICATION_REQUESTED_ITEMS_SLOT_PLAN.md · сессия Claude 7ea5b99f (UTC+2)</div>

<style>
.lead { margin: -0.45rem 0 0.35rem !important; font-size: 0.78rem; line-height: 1.42; color: var(--ink-2); max-width: 56rem; }
.lead code { font-size: 0.72rem !important; }
.lead .q { color: var(--ink); font-family: var(--font-mono); font-size: 0.7rem; }
.words { display: grid; grid-template-columns: 1.05fr 1fr 1fr; gap: 10px; margin-top: 0.45rem; }
.wd { font-size: 0.64rem; line-height: 1.4; color: var(--ink-2); background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: 0.45rem 0.7rem 0.5rem; }
.wd.hot { border-color: rgba(217, 89, 38, 0.55); }
.wd b { color: var(--ink); }
.wd code { font-size: 0.58rem !important; }
.wh { display: flex; justify-content: space-between; align-items: baseline; gap: 0.4rem; margin-bottom: 0.25rem; }
.wh code { font-size: 0.72rem !important; color: var(--ink) !important; }
.wh span { font-size: 0.56rem; color: var(--muted); white-space: nowrap; }
</style>

<!--
Наведите на отметку — останется только она. Полоса — что порт делал с F8 на полном пуле: серое — граница (игра останавливается событием boundary), жёлтое — объявленный пропуск, зелёное — модель. Ночь с 01:30 до 05:30 вырезана из оси: в это время ничего не происходило.

16:09 (d8481cb). Прогон War дошёл до случайного выпада предмета, когда слоты 50..399 все заняты. Оригинал тогда читает слово кадра [esp+4c], которое неудачный поиск не записал; его прежние писатели кладут указатель на Object или адрес, так что значение под Windows действительно неизвестно. Объявленная политика: без слота выпад пропускается после своих бросков ГСЧ. Этот пропуск остался.

16:53 (d26e412). Агент перенёс ту же политику на проход запрошенных предметов — F8 и запросы стадий библиотеки. Коммит: входящее значение SP+34 — последняя запись цикла жизненного цикла («a countdown's 0, a counter's 400, an Object-table pointer»), «not modelled». Значит, пропуск после четырёх бросков координат.

23:03 (698f76a). Независимое ревью: «the requested-items slot word is not unknown: 41f2c7 writes −4−World into it on every call, then the lifecycle loop overwrites it (a countdown's 0 makes the original rebuild slot 0). The skip from d26e412 departed from known EXE behaviour, so the explicit boundary is back». То есть агент заменил известное поведение оригинала удобным пропуском — ревью это вернуло.

00:53. Агент остановил цикл и среди пяти вопросов автору спросил, стоит ли строить полную обработку F8. В 05:56 автор ответил: «Полную обработку F8 оставить обязательной частью совместимости и выполнить в порядке приоритетов проекта» — следующий слайд.

09:08 (f4cdcbb). Ядро несёт слово от 41f2c7 через всех писателей цикла 41f550..4214cf — частицы, поиск opoint, оружие, команды, смерть и огненные частицы, как их перечисляет статическая трасса слова кадра. На полном пуле слот 0..399 пересобирается как в оригинале. 9 новых тестов; слово, которое видел оракул команд (0xddffffdc для его World 0x22000020), теперь обязано совпасть с моделью.

10:16 (8d107f1). Бой VS: F8 каждые 12 тиков, F7 восстанавливает HP. После 88 нажатий пул заполнился, следующее F8 пересобрало слот 0 — Наруто игрока 1 — в предмет, как оригинал при SP+34 = 0. Дальше HUD передаёт указатель картинки small: (заголовок +728) в 43f010, а та разыменовывает его без проверки. У предметов small: нет, загрузчик +728 не пишет, а содержимое каждой ~150 КБ аллокации Object ничем не определено. HUD и Summary теперь останавливаются там с именованной объявленной остановкой.

Вечером того же дня (7d592f9, 22:05) та же логика дошла до случайного выпада: если перед ним в том же вызове был респаун из резерва, слово равно −3 − World, и оригинал читает 0xff2f6088 — теперь это Source fault, а без респауна пропуск остаётся.
-->

---

<Kicker>1 октября, 00:53 → 09:42 · вопросы и реплика — из журнала сессии Claude</Kicker>

# Пять вопросов — одна реплика

<p class="lead">Ещё 30 сентября в 02:36 план полного экрана встал: <span class="q">«The plan now waits for the user's choice»</span>. К ночи таких развилок набралось пять, и агент остановил цикл. Наведите на вопрос, кусок реплики или коммит — подсветится одно решение.</p>

<BDecisions />

<div class="source">сессия Claude Code 7ea5b99f: список «Waiting on you» в 00:53 (пересказ), реплика автора в 05:56 (дословно), время UTC+2 · 69055ca · 80c83c1 · 778a8c4 · cb33304 · f4cdcbb · c50a806 · docs/research/CURRENT_WORK.md · SCOPE_RECONCILIATION_2026-10-02.md</div>

<style>
.lead { margin: -0.45rem 0 0.45rem !important; font-size: 0.78rem; line-height: 1.42; color: var(--ink-2); max-width: 56rem; }
.lead .q { color: var(--ink); font-family: var(--font-mono); font-size: 0.7rem; }
</style>

<!--
Левая колонка — сообщение агента в 00:53, когда он остановил /loop: что сделано за сессию, что откатано (пропуск F8, предыдущий слайд) и пять пунктов «Waiting on you». Здесь они пересказаны по-русски, в порядке ответа автора. Реплика автора — дословно, одним сообщением в 05:56; цифры над ней — какой кусок отвечает на какой вопрос.

Правая колонка — что сделано по каждому ответу, по времени коммитов. От реплики до последнего коммита — 3 часа 46 минут.

1. Запуск (80c83c1, 06:01). Приложение без аргументов открывает восстановленную оригинальную игру; лаборатория Practice — только с --practice или своими ключами; --original по-прежнему принимается. В этом же коммите все пять решений записаны в CURRENT_WORK.

2. Alt+Enter (cb33304, 07:30, и c50a806, 09:42). Как в оригинале: WM_SYSKEYUP(VK_RETURN) доходит до восстановленной 43b83f — она освобождает дисплей, уничтожает окно (синхронный WM_DESTROY освобождает звуковое устройство, граф музыки и буферы записи) и создаёт заново полноэкранное окно или обычное. Переключение во время записи матча — собственное падение оригинала по нулевому указателю, в порту это Source fault. Отдельно, по тому же решению, — стандартный полный экран macOS: зелёная кнопка, View → Enter Full Screen (⌃⌘F) и команда сценария fullscreen; игре он не посылает ни одного сообщения. Настоящий переход AppKit тогда не наблюдали — дисплей спал.

3. Шрифт (778a8c4, 06:45). Ни EXE, ни lib.dll не создают шрифт — оригинал рисует TextOut шрифтом DC по умолчанию, SYSTEM_FONT, растровым шрифтом Windows, который нельзя поставлять. Поэтому — системный шрифт macOS, bold 13 px в ячейке 16 px, базовая линия +13, без сглаживания; позиция, точный цвет и фон — как у оригинала. Цифры Summary, HUD Stage, значения меню и CONTROL SETTINGS получили текст.

4. Музыка Demo. Трек Demo выбирается по остатку регистра ECX от предыдущего вызова текста (6c384fc) — объявленная политика порта. Кода по этому ответу не было: выбор записан как временный, а 2 октября сверка объёма отнесла его к внешнему: нужен замер регистра на Windows.

5. F8 (f4cdcbb, 09:08) — модель слова SP+34, предыдущий слайд.

Деталь: агент задал вопросы в 00:53, автор ответил в 05:56 — пять часов цикл стоял. Потом пять развилок закрылись за одно утро.
-->

---

<Kicker>1–2 октября · как в оригинале</Kicker>

# Мелочи, которые делают игру той самой

<div class="grid grid-cols-[30rem_1fr] gap-5 mt-1">
<div>
<BeforeAfter before="/img/screens/13a-rle-holes-before.png" after="/img/screens/13b-rle-holes-after.png" before-label="до исправления" after-label="после" height="18rem" :start="47" fit="cover" position="20% 50%" pixelated />
<div class="rle-cap">
<span class="i-pixelarticons-image-broken rle-ico" />
<div>
<div class="flex items-center gap-2"><b>Дыры RLE</b><code class="mini-tag">55fd92d</code></div>
<div class="rle-txt">«Com» и «P1» — bitmap-шрифты RLE8 с 20 800+ незаписанными пикселями. Windows заливает их индексом палитры 0, и color key их вырезает.</div>
</div>
</div>
</div>
<div class="flex flex-col gap-2">
<IconCards :cols="1" :items="[
  { icon: 'i-pixelarticons-expand', title: 'Alt+Enter', text: 'Полный экран как в оригинале — вместе с его багом: эффекты глохнут, а при записи повтора игра падает через обнулённый указатель <code>0x4588a8</code>.', tag: 'cb33304' },
  { icon: 'i-pixelarticons-text-start-t', title: 'GDI-текст', text: 'Подписи <code>SYSTEM_FONT</code> рисует системный шрифт Mac: позиция, размер и цвет те же. Одно из двух объявленных отличий.', tag: '778a8c4' },
]" />
<div class="also">
<div class="pixel hl also-h">и ещё</div>
<div class="also-row"><span class="i-pixelarticons-play also-ico" /><span>Приложение сразу открывает оригинальную игру</span><code class="mini-tag">80c83c1</code></div>
<div class="also-row"><span class="i-pixelarticons-gamepad also-ico" /><span>Геймпады — как джойстики оригинала, через GameController</span><code class="mini-tag">f265f11</code></div>
<div class="also-row"><span class="i-pixelarticons-image also-ico" /><span>У бандла — иконка из самого EXE</span><code class="mini-tag">60cd161</code></div>
</div>
</div>
</div>

<style>
.rle-cap { display: flex; gap: 0.6rem; align-items: flex-start; margin-top: 0.65rem; }
.rle-ico { flex: none; width: 1.45rem; height: 1.45rem; color: var(--naruto); }
.rle-cap b { font-size: 0.78rem; font-weight: 650; color: var(--ink); }
.rle-txt { font-size: 0.66rem; line-height: 1.38; color: var(--ink-2); margin-top: 0.2rem; }
.mini-tag { font-size: 0.56rem !important; color: var(--muted) !important; background: rgba(255, 255, 255, 0.05) !important; border: 0 !important; border-radius: 4px !important; padding: 0.05rem 0.35rem !important; }
.also { background: rgba(255, 255, 255, 0.03); border: 1px solid var(--hair); border-radius: 12px; padding: 0.5rem 0.8rem 0.55rem; }
.also-h { font-size: 0.66rem; margin-bottom: 0.2rem; }
.also-row { display: grid; grid-template-columns: 1.1rem 1fr auto; align-items: center; gap: 0.5rem; font-size: 0.66rem; line-height: 1.3; color: var(--ink-2); padding: 0.2rem 0; }
.also-row + .also-row { border-top: 1px solid var(--hair); }
.also-ico { width: 1.05rem; height: 1.05rem; color: var(--naruto); }
</style>

<!--
Слайдер: «до исправления» — чёрные плашки под буквами, «после» — сквозь буквы видна кладка. Ползунок можно тянуть.

Alt+Enter (cb33304). Полноэкранный режим как в оригинале — вместе с его багом: звуковые эффекты глохнут до конца сессии, а во время записи повтора игра падает через обнулённый указатель 0x4588a8. В порту это остановка «Source fault»; обычный полноэкранный режим macOS добавлен отдельно.

GDI-текст (778a8c4). Часть подписей оригинал рисует через Windows GDI шрифтом SYSTEM_FONT. На Mac — системный шрифт, bold 13 px в ячейке 16 px: позиция, размер и цвет сохранены. Это одно из двух объявленных отличий.

Дыры RLE (55fd92d). «Com» и «P1» — bitmap-шрифты в RLE8 с 20 800+ незаписанными пикселями. Windows заполняет дыры индексом палитры 0, и color key их вырезает. Без этого под надписью — чёрная плашка.

И ещё: приложение сразу открывает оригинальную игру (80c83c1), геймпады работают как джойстики оригинала через GameController (f265f11), у бандла — иконка из самого EXE (60cd161).
-->

---

<Kicker>1–2 октября · сеть</Kicker>

# Отказ, перестраховка и матч двух приложений

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-2">
<div>

<Timeline dense :items="[
  { time: '01.10', title: 'Mac-сервис Winsock для сетевой игры (Claude)', hash: '7727346' },
  { time: '01.10', title: 'Отказ модели на сетевой интеграции — сеть отложена', hash: '0efae95' },
  { time: '02.10', title: 'Correct overstated networking hold — запрет был не на всю сеть', hash: 'a4fb48c', hot: true },
  { time: '02.10', title: 'Нативный клиент и переход меню в подключённое состояние', hash: 'c573f10' },
  { time: '02.10', title: 'Два приложения доигрывают матч до Summary', hash: '73f8d22', hot: true },
  { time: '02.10', title: 'Выход хоста и закрытие клиента', hash: '4f65fa4' },
]" />

<p class="xsmall muted mt-2">Сеть N1–N5 довёл параллельный агент (Codex, без трейлера). Независимое ревью нашло одно замечание P2 — исправлено.</p>

</div>
<div>

<div class="grid grid-cols-2 gap-3">
<StatTile :value="1070" label="игровых тиков сетевого матча" size="sm" />
<StatTile :value="836" label="пакетов в каждую сторону, каждый совпал с приёмом" size="sm" accent="var(--s1)" />
</div>

<div class="card mt-3">
<div class="pixel hl small">протокол оригинала</div>
<p class="small ink2 mb-0">Хост шлёт <code>u can connect\0</code> (14 байт) и спит <code>Sleep(3000)</code>. Клиент делает <code>recv</code> 3001 байта <b>прямо в таблицу ГСЧ</b> <code>0x44ff90</code>, не проверяя код возврата. Сообщение об ошибке так и написано: <code>Accpet() Error</code>.</p>
</div>

<p class="xsmall muted mt-2">Состояние двух приложений различалось только CRT-случайными смещениями искр (≤ 8 px): стартовые seed разные намеренно.</p>

</div>
</div>

<div class="source">docs/research/NETWORK_PLAY.md · NETWORK_CLIENT.md · NETWORK_NOTIFICATION.md · docs/evidence/network-review-20261002.json</div>
