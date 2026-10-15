---
layout: chapter
num: 18
total: 19
kicker: Глава восемнадцатая
dates: 13 октября
image: /img/covers/ch18-menu.svg
imagePixel: false
stats: ≈ 29 МБ в минуту → ровно · Razer Kishi V2, а не Backbone One · 13 файлов, 6 платформ, Latest
---

# Семь часов в меню

Один день. Автор находит в Activity Monitor процесс игры на 11 ГБ, присылает фото джойстика — и получает релиз на шесть платформ. Выпустил его не Claude.

<div class="cover-note">Обложка — рисунок: условное окно монитора памяти и условный контроллер, не снимок экрана и не фото.</div>

<style>
.cover-note { margin-top: 0.7rem; font-size: 0.66rem; color: var(--muted); }
</style>

<!--
Глава об одном дне, 13 октября: с 04:48 (df74758a, масштабируемые окна слиты в main) до 20:14 (5f5a8ee4, коммит C3). Все цифры заморожены на 5f5a8ee4, ветка exp/iphone. Время местное, UTC+2.

Три истории дня: утечка памяти в меню (MENU_MEMORY), контроллер для телефона (PHONE_CONTROLLER C0–C3) и подписанный релиз на шесть платформ, который сделала сессия Codex, пока Claude молчал девять с половиной часов.
-->

---

<Kicker>13 октября, 05:40 · вопрос автора</Kicker>

# 11,22 ГБ за одну ночь в главном меню

<div class="grid grid-cols-[1.42fr_1fr] gap-6 mt-1">
<div>

<RelActivityMonitor />

</div>
<div class="side">

<PhoneChat :messages="[
  { who: 'human', time: '05:40', text: 'по памяти не утекает? нашел такой процесс в activity monitor', gloss: 'со снимком экрана: приложение в симуляторе — 11,22 ГБ', hot: true },
  { who: 'event', time: '08:15', text: '<code>340b1a64</code> · правка · слита в main как <code>1c692c22</code>' },
]" />

<div class="grid grid-cols-2 gap-2 mt-3">
<StatTile value="≈ 29 МБ" label="в минуту — рост в главном меню" sub="footprint раз в 20 с: 165 → 386 МБ за 460 с" size="sm" accent="var(--s2)" />
<StatTile value="≈ 1,7 ГБ" label="в час при том же темпе" sub="симуляторы Apple TV 1080p и iPad Air" size="sm" accent="var(--s2)" />
<StatTile value="+71 МБ" label="куча Mac-приложения за 140 с" sub="heap: 179 → 250 МБ, то же меню" size="sm" accent="var(--s2)" />
<StatTile value="158 МБ" label="после правки, ровно" sub="симулятор Apple TV, 4 мин замера" size="sm" accent="var(--s1)" />
</div>

</div>
</div>

<div class="source">docs/research/MENU_MEMORY.md (Observation, Result) · docs/evidence/menu-memory-20261013.json · 340b1a64 → 1c692c22 · сессия 1f9218ae, 03:40:58Z · data/rel_memory.json</div>

<style>
.side { display: flex; flex-direction: column; }
</style>

<!--
Слайдер — время простоя в меню. При открытии слайда он сам доезжает до точки, где замеренный темп даёт 11,22 ГБ; можно тянуть и наводить на график.

Честно о том, что здесь замер, а что нет. 11,22 ГБ — это снимок экрана автора: экземпляр в симуляторе tvOS/iPad простоял в меню около семи часов после проверок WINDOW_SCALING. Замер агента — footprint каждые 20 секунд в главном меню на настоящих часах, со звуком и музыкой выключенными: 165 → 386 МБ за 460 с, линейно, ≈ 29 МБ в минуту. Сплошной кусочек линии — эти 460 секунд; пунктир — тот же темп, продолженный на семь часов. Он доходит до 11,22 ГБ примерно за шесть с половиной часов — в согласии с «около семи».

На Mac рост мерили кучей (heap): 179 → 250 МБ за 140 с — те же ≈ 30 МБ в минуту. Вопрос автора пришёл в очередь сессии в 05:40:58 (03:40:58Z) и был подхвачен посреди хода.
-->

---

<Kicker>05:40 — 08:15 · причина</Kicker>

# Каждый кадр меню оставлял себе копию

<p class="lead">Итерация цикла сообщений — это курсор: запросы игры и ответы хоста. Ответ дисплея держит поверхности, которые рисовал, и порт хранил курсор <b>целиком</b>, чтобы они не пропали. А поверхности каждый кадр одни и те же.</p>

<div class="grid grid-cols-[1.18fr_1fr] gap-6">
<div>

<RelHistory />

</div>
<div class="code-sm">

```diff
- if let old = self.cursor,old.position > 0,
-    old.retainsResources { earlier.append(old) }
+ if let old = self.cursor,old.position > 0 {
+   var held = false
+   old.forEachResource { resource in
+     held = true
+     if retainedIdentities.insert(
+       ObjectIdentifier(resource)).inserted {
+       retained.append(resource) }
+   }
+   if held { retainedIterationCount += 1 }
+ }
```

<div class="cnote">Mac, 140 с в меню: узлов истории <b>138 → 4 404</b>, ≈ 30 в секунду (на tvOS ≈ 10); квитанции — ≈ 12 КБ на курсор, 54 МБ на 4 406.</div>

</div>
</div>

<div class="rounds">
<span class="rh pixel">третий раз — одна история</span>
<div class="rd"><b>29 сен</b> вся история копировалась каждую итерацию: 16,2 → 24,7 с на 2000 итераций меню → общий неизменяемый список</div>
<div class="rd"><b>30 сен</b> хранились курсоры всех тиков игры: ≈ 9 000 за матч, ≈ 12 МБ → только те, что держат ресурс</div>
<div class="rd now"><b>13 окт</b> итерации меню держат поверхности — ≈ 29 МБ в минуту → каждый ресурс один раз + счётчик</div>
</div>

<div class="source">OriginalApplicationObservedIteration.swift (340b1a64) · docs/research/MENU_MEMORY.md (Cause, Change) · APPLICATION_ITERATION_HISTORY.md · menu-memory-20261013.json · data/rel_memory.json</div>

<style>
.lead { margin: -0.45rem 0 0.4rem !important; font-size: 0.8rem; line-height: 1.4; color: var(--ink-2); max-width: 54rem; }
.lead b { color: var(--ink); }
.code-sm .slidev-code { font-size: 10px !important; line-height: 14.5px !important; margin: 0 !important; }
.cnote { font-size: .64rem; line-height: 1.38; color: var(--ink-2); margin-top: .45rem; }
.cnote b { color: var(--ink); }
.rounds { display: grid; grid-template-columns: auto 1fr 1fr 1fr; gap: 10px; align-items: stretch; margin-top: 0.6rem; }
.rounds .rh { font-size: 0.66rem; color: var(--naruto); align-self: center; width: 6.5rem; line-height: 1.25; }
.rounds .rd { font-size: 0.64rem; line-height: 1.35; color: var(--ink-2); background: rgba(255,255,255,.03); border: 1px solid var(--hair); border-radius: 10px; padding: 0.35rem 0.6rem; }
.rounds .rd b { color: var(--ink); margin-right: 0.3rem; }
.rounds .rd.now { border-color: rgba(217,89,38,.55); }
</style>

<!--
При открытии слайда счётчик курсоров бежит от 138 до 4 404 — столько узлов истории было в куче Mac-приложения в главном меню через 140 секунд (≈ 30 в секунду; на tvOS — 1 748 → 2 431 за ≈ 70 с, ≈ 10 в секунду).

Механика. OriginalApplicationIterationDelivery хранила каждый прежний непустой курсор итерации, если его квитанции держат ресурс: ресурс должен жить, пока его могут видеть скопированные контексты платформы и доставки. Тики игры ресурсов не держат и с 30 сентября не хранились. Но каждая итерация меню рисует через бэкенд дисплея, а его ответы держат поверхности, которых касались (`retained = [s]` в OriginalMacDisplayBackend). Каждый кадр — те же несколько поверхностей, и каждый раз — целый курсор с запросами и ответами. Курсоры никто не читал, кроме их числа.

Правка: доставка держит каждый ресурс один раз — массив в порядке первого появления плюс набор идентичностей — и считает итерации. Те же ресурсы живут столько же, копии независимы, откат забирает свои добавления. Порядок освобождения стал детерминированным (порядок вставки) — это находка ревью. Новый тест: 1 000 итераций с одними и теми же поверхностями держат два ресурса.

Код справа — строки самой правки из диффа 340b1a64, дословно; переносы длинных строк и отступы в два пробела — мои. «Третий раз»: 29 сентября историю перестали копировать целиком (общий неизменяемый список), 30 сентября перестали хранить курсоры тиков игры (≈ 9 000 курсоров и ≈ 12 МБ за матч), 13 октября — курсоры меню.
-->

---

<Kicker>08:15 · гейт mm-2 против tw-w3e · Mac</Kicker>

# После правки — ровная линия

<div class="grid grid-cols-[1.12fr_1fr] gap-6 mt-1">
<div>

<div class="chart-h">footprint Mac-приложения в сессии VS: 60 000 игровых шагов на виртуальных часах, замер раз в 10 с</div>

<RelSoak />

</div>
<div>

<div class="chart-h">прирост живой кучи за прогон · справа — узлы истории в конце прогона</div>

<RelHeapPairs />

<div class="lg2"><span><i class="sw2" style="background: var(--s2)" />до правки (tw-w3e)</span><span><i class="sw2" style="background: var(--s1)" />после (mm-2)</span></div>

</div>
</div>

<div class="grid grid-cols-4 gap-3 mt-3">
<StatTile value="0 из 20" label="запусков приложения упали" sub="гейт mm-2, AppKit" size="sm" accent="var(--good)" />
<StatTile value="15 из 15" label="прогонов сценариев = эталон" sub="кадры идентичны: 1 832 и 3 960" size="sm" accent="var(--good)" />
<StatTile value="1,43 → 1,38 мс" label="тик на Mac, медиана трёх прогонов" sub="процесс: 3,48 → 3,33 мс" size="sm" accent="var(--s1)" />
<StatTile value="10,86 = 10,86 мс" label="главный поток Galaxy A12" sub="второй A/B; в первом +0,07 — дрейф" size="sm" accent="var(--s1)" />
</div>

<div class="source">docs/evidence/menu-memory-20261013.json (soaks, gate, phoneAB2) · docs/research/MENU_MEMORY.md (Result) · 340b1a64 · data/rel_memory.json</div>

<style>
.chart-h { font-size: .66rem; color: var(--muted); margin-bottom: .2rem; line-height: 1.3; }
.lg2 { display: flex; gap: 1rem; font-size: .64rem; color: var(--ink-2); margin-top: .1rem; }
.lg2 span { display: inline-flex; align-items: center; gap: .35rem; }
.sw2 { display: inline-block; width: 10px; height: 10px; border-radius: 3px; }
</style>

<!--
Наведите на график — перекрестие покажет обе линии в одной точке.

Прогоны по одному процессу за раз: старый бинарник (tw-w3e, предыдущий гейт) и новый (mm-2). Главное меню — 4 минуты простоя на настоящих часах: живая куча 170,9 → 287,2 МБ и 7 441 узел истории до; 168,6 → 168,8 МБ и ноль узлов после, footprint после прогрева ровно 298 МБ. Выбор персонажей VS — 3 минуты: +13,8 МБ и 5 619 узлов до, −0,2 МБ после. Сессия VS на 60 000 игровых шагов — виртуальные часы: +121,4 МБ и 35 460 узлов до, footprint всё ещё рос примерно на 1 МБ за 10 с; после — +37,5 МБ за первые матчи и ровные 829 МБ со второй минуты.

Ресурсы по-прежнему живут до конца сессии, как и раньше: перестали храниться только запросы и ответы итераций. Это записано в границах карточки.

Гейт: Core-наборы с новым тестом, 20 запусков AppKit без падений, все сценарии AppKit с идентичными кадрами, unchecked vs и Demo, vs в эмуляторе; A/B на Mac — 1,38 против 1,43 мс на тик; на Galaxy A12 — два A/B, во втором 10,86 против 10,86 мс. Независимое ревью — OK.
-->

---

<Kicker>06:36 — 19:03 · PHONE_CONTROLLER C0–C2</Kicker>

# Джойстик с фотографии

<div class="grid grid-cols-[1fr_1.15fr] gap-6 mt-1">
<div>

<PhoneChat :messages="[
  { who: 'human', time: '06:36', text: 'как закончишь, влей обе ветки в main; и новая задача тебе [фото] вот джойстик для мобильных телефонов (погугли что за девайс). если у нас есть поддержка таких джойстиков то супер. Погугли мануалы и примеры реализаций. Если нет, то добавь. и в ios и в android', hot: true },
  { who: 'human', time: '06:40', text: 'ага, сделай iPhone отдельную сборку значит. как закончишь с этой задачей.', gloss: 'приложение для iOS было только для iPad' },
  { who: 'event', time: '08:45', text: '<code>f340f1e2</code> · C1: отдельное приложение для iPhone' },
  { who: 'event', time: '19:03', text: '<code>d4619cbc</code> · C2: «not the Backbone One C0 guessed from the photo»' },
]" />

<div class="card-soft mt-3 c0">
<div class="pixel hl xsmall mb-1">что нашёл обзор C0</div>
Поддержка уже была: iPad, Apple TV и macOS берут первые два геймпада через GameController (T1b), Android — через InputDevice (T1c). Не хватало только цели: приложение iOS собиралось лишь для iPad.
</div>

</div>
<div>

<div class="ids">
<div class="idc bad">
<div class="ih"><span>C0 · по фото</span><span class="st"><b>✕</b> неверно</span></div>
<div class="nm">Backbone One</div>
<div class="tx"><span lang="en" class="q">«most likely a Backbone One (USB-C)»</span> — тот же облик: крепление на телефон, раздвижной мост, A/B/X/Y как у Xbox, два стика, бамперы, курки, кнопка с логотипом</div>
</div>
<div class="idc good">
<div class="ih"><span>C2 · по USB</span><span class="st"><b>✓</b> назвалось само</span></div>
<div class="nm">Razer Kishi V2</div>
<div class="tx"><span class="mono">«Razer Razer Kishi V2»</span><br>vendor <span class="mono">0x1532</span> · product <span class="mono">0x0712</span> · на Pixel 10, Android 17</div>
</div>
</div>

<div class="card-soft mt-3 ip">
<div class="pixel hl xsmall mb-1">C1 · iPhone — отдельная сборка</div>
<RelIphoneFit />
<div class="xsmall ink2 mt-1" style="line-height: 1.35">Хост iOS теперь сообщает игре экран не меньше 800×600, как Android, и вписывает картинку. Всё — в симуляторе; настоящий iPhone не пробовали.</div>
</div>

</div>
</div>

<div class="source">docs/research/PHONE_CONTROLLER.md (The device, Ledger C0–C2) · phone-controller-c1-20261013.json · phone-controller-c2-20261013.json · f340f1e2 · d4619cbc · сессия 1f9218ae (UTC+2) · data/rel_controller.json</div>

<style>
.ids { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.idc { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: .5rem .7rem .55rem; }
.idc.bad { border-color: rgba(208,59,59,.55); }
.idc.good { border-color: rgba(12,163,12,.55); }
.ih { display: flex; justify-content: space-between; gap: .4rem; font-size: .6rem; color: var(--muted); }
.st { color: var(--ink-2); white-space: nowrap; }
.bad .st b { color: var(--critical); }
.good .st b { color: var(--good); }
.idc .nm { font-family: var(--font-display); font-weight: 700; font-size: 1.05rem; margin: .2rem 0 .25rem; color: var(--ink); }
.bad .nm { text-decoration: line-through; text-decoration-color: var(--critical); text-decoration-thickness: 2px; }
.idc .tx { font-size: .64rem; line-height: 1.38; color: var(--ink-2); }
.idc .q { color: var(--ink); }
.idc .mono { font-size: .6rem; color: var(--ink); }
.ip { padding: .5rem .7rem .55rem; }
.c0 { font-size: .68rem; line-height: 1.4; color: var(--ink-2); }
</style>

<!--
Фото автора в колоде не показываем: в тексте сообщения на его месте — пометка [Image #7], здесь заменённая на «[фото]». Остальное — дословно из журнала сессии 1f9218ae; время местное.

C0 — карточка исследования: устройство по фото, исходники, обзор. Агент опознал его как Backbone One с USB-C: у них действительно одинаковый облик — накладка на телефон с раздвижным мостом, кнопки A/B/X/Y в раскладке Xbox, два стика, бамперы, курки, кнопка с логотипом. Опознание было неверным. Вечером на Pixel 10 устройство само назвалось по USB: «Razer Razer Kishi V2», vendor 0x1532, product 0x0712. Карточка исправлена в коммите C2, а коммит говорит прямо: «not the Backbone One C0 guessed from the photo».

Из обзора C0 же вышло главное: оба хоста уже умели геймпады (iPad, Apple TV и macOS — через GameController; Android — через InputDevice), а вот iPhone не был целью: приложение iOS собиралось только для iPad. Автор в 06:40 попросил отдельную сборку.

C1: свой bundle local.ntsd.native.iphone, только iPhone, только альбомная ориентация. Первый прогон остановил все 10 сценариев на первом blit меню: окну 794×550 не хватало экрана 874×402 точки. После правки — 10 из 10, все 18 088 кадров идентичны эталону CoreText. Ревью нашло одну проблему средней важности (профиль подписи для iPhone) — исправлено. Записано: всплывающее окно Alt+Enter заполняет экран целиком, и Dynamic Island со скруглёнными углами закрывают его края.
-->

---

<Kicker>C2 · Pixel 10, Android 17 · что увидел Android</Kicker>

# Один контроллер — три HID-интерфейса

<div class="grid grid-cols-[1.18fr_1fr] gap-6 mt-1">
<div>

<RelController />

</div>
<div class="ifs">

<div class="if">
<div class="ih2"><b>интерфейс 0 · геймпад</b><span class="mono">event3 → Android id 4</span></div>
<div class="tx2">стики X/Y и Z/RZ, курки GAS/BRAKE: 0–255, покой 0x80, мёртвая зона 15 · крестовина — оси HAT0X/HAT0Y · 15 кнопок</div>
<div class="src2 mono">KEYBOARD | GAMEPAD | JOYSTICK</div>
</div>

<div class="if warn">
<div class="ih2"><b>интерфейс 2 · двойник без осей</b><span class="mono">event6 → id 5</span></div>
<div class="tx2">те же 15 кнопок, осей нет · за всю запись — <b>ни одного события</b>, но для Android это второй геймпад</div>
<div class="src2 mono">KEYBOARD | GAMEPAD</div>
</div>

<div class="if">
<div class="ih2"><b>интерфейс 1 · сенсорная панель</b><span class="mono">event5</span></div>
<div class="tx2">мультитач 2048×4096, 5 касаний</div>
</div>

<div class="xsmall muted" style="line-height: 1.3">ещё два узла: Consumer Control (громкость, питание, «назад», «домой»…) и ABS_MISC</div>

<div class="pipe">
<span>событие Android</span><i>→</i><span>каждые 25 мс: X/Y 0–65535 и кнопки 1–4</span><i>→</i><span class="mono">MM_JOY1MOVE · MM_JOY1BUTTONDOWN</span><i>→</i><span>control.txt: игрок 3 = джойстик 1</span>
</div>

</div>
</div>

<div class="source">phone-controller-c2-20261013.json (hidNodes, androidInputDevices, rawEventsOnController) · NTSDAndroidGamepads.swift · APPLICATION_JOYSTICKS.md · data/control.txt оригинала · OriginalCharacterAI.swift (порядок клавиш) · data/rel_controller.json</div>

<style>
.ifs { display: flex; flex-direction: column; gap: .4rem; }
.if { background: var(--surface); border: 1px solid var(--hair); border-radius: 10px; padding: .32rem .6rem .38rem; }
.if.warn { border-color: rgba(250,178,25,.5); }
.ih2 { display: flex; justify-content: space-between; align-items: baseline; gap: .4rem; font-size: .68rem; color: var(--ink); }
.ih2 .mono { font-size: .58rem; color: var(--muted); white-space: nowrap; }
.tx2 { font-size: .64rem; line-height: 1.35; color: var(--ink-2); margin-top: .1rem; }
.tx2 b { color: var(--ink); }
.src2 { font-size: .58rem; color: var(--muted); margin-top: .1rem; }
.pipe { display: flex; flex-wrap: wrap; align-items: center; gap: .2rem .3rem; font-size: .62rem; color: var(--ink-2); background: rgba(255,255,255,.03); border: 1px dashed var(--axis); border-radius: 10px; padding: .35rem .5rem; line-height: 1.3; }
.pipe span { background: var(--surface-2); border-radius: 6px; padding: .05rem .4rem; }
.pipe span.mono { font-size: .58rem; }
.pipe i { font-style: normal; color: var(--naruto); }
</style>

<!--
Наведите на кнопку или стик — внизу появится его путь: код evdev на HID-интерфейсе 0, клавиша или ось Android, что хост порта отдаёт оригиналу через WinMM и что эта кнопка делает у игрока 3 по умолчанию. Ореол и число — сырые события evdev за всю запись, нажатия и отпускания вместе.

Что видел Android: интерфейс 0 — сам геймпад, одно устройство ввода с источниками KEYBOARD | GAMEPAD | JOYSTICK; интерфейс 2 — те же 15 кнопок без осей, второе устройство KEYBOARD | GAMEPAD; интерфейс 1 — сенсорная поверхность. Плюс узел Consumer Control и узел ABS_MISC.

Как кнопка доходит до игры. Хост Android (NTSDAndroidGamepads, T1c) при запуске берёт первые два устройства с SOURCE_GAMEPAD — оригинал тоже опрашивает джойстики один раз, при старте. Каждые 25 мс, как просит joySetCapture оригинала, он отдаёт оси X/Y в 0–65535 (крестовина поверх левого стика) и кнопки 1–4 из A/B/X/Y. B никогда не превращается в «Назад», иначе игра задала бы вопрос о выходе. Дальше работает портированный код оригинала: MM_JOY1MOVE с порогом 100, MM_JOY1BUTTONDOWN/UP.

Роли кнопок — из data/control.txt оригинала: игрок 3 по умолчанию на джойстике 1, атака — кнопка 1, прыжок — 2, защита — 3. Порядок строк (вверх, вниз, влево, вправо, атака, прыжок, защита) совпадает с порядком байтов клавиш актёра в OriginalCharacterAI. Игрок может переназначить кнопки в CONTROL SETTINGS; направления у джойстика не переназначаются.

Забавное: правый стик и курки за запись дали больше 700 событий — у игры для них нет роли.
-->

---

<Kicker>13 октября, 18:45 — 20:14 · C2 и C3</Kicker>

# «все работает» — и лишний джойстик

<RelPixelRuns />

<RelJoySlots class="mt-2" />

<div class="logl">ожидаемая строка logcat после C3: <code>NTSD: gamepads at launch: [4 1532:712 axes, 5 1532:712 unused]</code> — на телефоне ещё не проверено; эмулятор: vs и joystick = эталон</div>

<div class="source">phone-controller-c2-20261013.json (timeline, findings) · phone-controller-c3-20261013.json · PHONE_CONTROLLER.md (Gaps, Next task) · d4619cbc · 5f5a8ee4 · сессия 1f9218ae (UTC+2) · data/rel_controller.json, rel_day.json</div>

<style>
.logl { font-size: .62rem; color: var(--ink-2); margin-top: .35rem; }
.logl code { font-size: .58rem !important; }
</style>

<!--
Верхняя полоса — вечер на Pixel 10. В 18:45 автор просит убрать кофеин (caffeinate не давал Mac уснуть), в 18:46 — поставить сборку на подключённый Pixel. Телефон работал с adb по Wi-Fi: на USB включили tcpip, потом телефон ушёл в контроллер. Запись шла скриптом наблюдения: dumpsys input и getevent на каждое изменение устройств, getevent -lt, logcat, pidof раз в 2 секунды.

Три запуска. В первом и втором контроллер подключили уже после старта — хост его не берёт: джойстики опрашиваются один раз. Третий — с контроллером с самого старта, 4 минуты 40 секунд игры. В 18:58 — «все работает». На выходе из третьего запуска libc записал SIGSEGV в потоке «Jit thread pool» ART через 94 мс после того, как окно стало невидимым; Zygote сообщил, что процесс «exited cleanly (0)», без tombstone и диалога. onDestroy хоста вызывает exit(0), пока потоки ART ещё работают. Записано, не изучено.

APK был debug-сборкой из гейта MENU_MEMORY (mm-2): исходники Android с main не отличались.

Нижняя часть — C3. Хост брал первые два устройства с SOURCE_GAMEPAD, поэтому немой интерфейс 2 контроллера становился джойстиком 2: он не двигается и не нажимается, а второму игроку с настоящим геймпадом слота бы не досталось. Последнее — вывод карточки из кода и списка устройств: число джойстиков на Android не логируется. Переключатель «второй геймпад» показывает этот вывод, а не проведённый опыт. C3 пропускает устройство без осей джойстика, если у устройства с осями тот же vendor и product. Эмулятор — vs и joystick равны, обычный запуск логирует «gamepads at launch: []», ревью OK. Первый прогон C3 завис на чёрном экране: APK собрали на диске T7 с ExFAT, и в список ассетов попали файлы ._ — ошибка харнесса, повтор на X5.
-->

---

<Kicker>14:24 — 15:28 · релиз native-preview-20261013</Kicker>

# 13 файлов на шесть платформ

<div class="meta">
<span class="tag">тег → f340f1e2 · ветка exp/iphone, не main</span>
<span class="tag">release/native-preview-20261013 → 0b5d4621</span>
<span class="tag">опубликован 15:22 · Latest с 15:26</span>
<span class="tag">одно native-дерево 9db6dd70 на все шесть сборок</span>
</div>

<RelAssets />

<div class="source">docs/evidence/release-refresh-20261013.json · CURRENT_WORK.md · releases-20261013/published-digest-verification.json, latest-release.json · git tag native-preview-20261013 · origin/release/native-preview-20261013 · data/rel_release.json</div>

<style>
.meta { display: flex; flex-wrap: wrap; gap: .3rem .4rem; margin: -0.35rem 0 .5rem; }
.meta .tag { font-size: .6rem; }
</style>

<!--
Наведите на полосу, строку или точку — справа появятся точный размер, SHA-256 и подпись.

Что выпущено: macOS 0.5.0 — DMG для macOS 14+ на Apple silicon; APK для Android 9+ на ARM64; ZIP для Windows x86-64; два tar.gz для Linux ARM64 и x86-64; ZIP с Web-версией для статического хостинга. К каждому пакету — манифест с SHA-256 каждого файла внутри, плюс DMG.sha256 и общий SHA256SUMS.txt. Всего 13 файлов, 1,48 ГБ. iOS исключён по просьбе автора, сборки tvOS — только для симулятора, их не выдают за устройство.

Тег native-preview-20261013 — лёгкий, на f340f1e2: это игровой исходник, ветка exp/iphone, в main не слита. Windows собран из 2c4db98b, Android — из 9c700dae: эти коммиты меняют только инструменты и документацию, native-дерево у всех шести одно — 9db6dd70.

Автор попросил вместо pre-release обычный релиз с меткой Latest: опубликован в 15:22:12, метка и заголовок обновлены к 15:26:11. Проверка публикации: у всех 13 вложений дайджест и размер на GitHub равны локальным; три маленьких манифеста скачаны целиком и сверены, крупные загрузки остановлены, как только совпали все серверные дайджесты.

gh CLI в момент сборки главы не авторизован (401), поэтому размеры и время загрузки — из записи GitHub о релизе, которую агент сохранил после публикации в папку артефактов, указанную в evidence.
-->

---

<Kicker>как проверяли и где споткнулись · 15 записей в failures.json</Kicker>

# Шесть пакетов — шесть разных проверок

<RelChecks />

<div class="source">release-refresh-20261013.json (checks, signing, boundaries) · releases-20261013/failures.json, *.notary.json, *.spctl.txt, web-checks2.log · tools/crossplatform/linux_x11_smoke.sh (2c4db98b) · data/rel_release.json</div>

<!--
Наведите на квадратик в последней колонке — внизу появится запись из failures.json: что упало и что сделали дальше. По умолчанию показан самый характерный сбой дня.

Файлы ._ — призрак этого дня. macOS, записывая на диск с ExFAT, кладёт рядом с каждым файлом двойника «._имя» с атрибутами. Из-за них проверка Linux ARM64 упала на запуске, матч VS отличился ровно четырьмя такими файлами в оверлее (сравнение их честно учло), APK показал чёрный экран — aapt2 выкинул ._-файлы, а список ассетов их ждал. Вечером тот же призрак повесил первый прогон C3. После третьего круга правило: всё, что запускается, и все записываемые оверлеи — только на APFS; на T7 — лишь итоговые архивы и отчёты.

Масштабируемое окно: проверка X11 кликала по координатам игры 350,230, а окно 1088×754 уже масштабируется — правильная точка 480,316. Скрипт исправлен той же формулой, что уже была в linux_sdl_scaling.py (коммит 2c4db98b).

Шесть сбоев — связка ключей. Подпись в сеансе агента упала с errSecInternalComponent, notarytool — keychainLocked; unlock-keychain без пароля запрещён, переход в сеанс пользователя через launchctl asuser — тоже. Обошлось без пароля: подпись и нотаризация ушли в LaunchAgent графического сеанса Aqua, где связка уже открыта; с первого раза задача не стартовала — пути на внешнем диске, со второго прошла. Секрет ключа Android шёл из связки прямо в окружение apksigner, не печатался и не сохранялся; агент после выгружен.

Подпись: только macOS (Developer ID, нотаризация app и DMG — Accepted, staple, Gatekeeper: «Notarized Developer ID») и Android (прежний release-ключ, сертификат совпал). Windows, Linux и Web — без подписи кода: целостность по SHA256SUMS и манифестам. Независимого ревью у релиза не было: «No independent reviewer available».
-->

---

<Kicker>кто что делал 13 октября · метаданные сессий, без текста переписки</Kicker>

# Релиз выпустил другой агент

<RelDayLanes />

<div class="grid grid-cols-3 gap-3 mt-2 who">
<div class="card-soft"><b class="big">152 из 155</b> коммитов с 7 октября (<code>8840eb3..5f5a8ee4</code>) несут трейлер <code>Co-Authored-By: Claude Opus 5.5</code>. Автор в git у всех один — Michael: агенты коммитят под учёткой автора.</div>
<div class="card-soft"><b class="big">Три без трейлера</b> — <code>2c4db98b</code> 14:51, <code>9c700dae</code> 14:59, <code>0b5d4621</code> 15:28: один заголовок, тело пустое. Время — внутри сессии Codex 14:24–15:28; в plan.json релиза — <code>owner: Codex</code>.</div>
<div class="card-soft"><b class="big">Без вопросов.</b> Сессия Codex — <code>approval: never</code>, <code>danger-full-access</code>; 251 вызов инструментов за час, 28,7 млн токенов, 98,7 % входа из кэша. Claude в это время молчал 9,5 часа.</div>
</div>

<div class="source">git log 5f5a8ee4 (трейлеры) · git rev-list 8840eb3..5f5a8ee4 · ~/.codex/sessions/2026/10/13: session_meta, turn_context, token_count · ~/.claude/projects/…/1f9218ae (только время) · releases-20261013/plan.json · data/rel_day.json</div>

<style>
.who .card-soft { font-size: .66rem; line-height: 1.4; color: var(--ink-2); }
.who .big { display: block; font-family: var(--font-display); font-size: .92rem; color: var(--ink); margin-bottom: .15rem; }
.who code { font-size: .58rem !important; }
</style>

<!--
Наведите на коммит или на полосу сессии Codex — под графиком появятся подробности. По умолчанию выбран коммит публикации.

Как установлено авторство. В git автор и коммиттер всех 155 коммитов — Michael: агенты коммитят под учёткой автора, а Claude подписывается трейлером Co-Authored-By. У трёх коммитов релиза трейлера нет, а тело сообщения пустое. Их время — 14:51, 14:59 и 15:28 — лежит внутри единственной сессии агента в репозитории порта в эти часы: Codex CLI (codex-tui 0.156.1-fork.1), модель GPT-6 Astra, effort medium, ветка exp/iphone на f340f1e2. В plan.json релиза, записанном в 14:32, поле owner — Codex. Текст сессии не читался: только метаданные, время, имена инструментов и счётчики токенов.

«Без вопросов» — про режим: approval never значит, что Codex не спрашивал разрешений на команды. Вопросы автору он задавал: в сессии три вызова request_user_input, и в evidence записана просьба автора поставить метку Latest вместо pre-release.

Claude Code (сессия 1f9218ae, Opus 5.5) в это время молчал: последнее сообщение — 09:14, следующее — 18:45, когда автор вернулся с телефоном. В главе 11 Codex вёл порт до 3 октября, потом основную работу взял Claude. Codex в репозитории открывали и позже (5, 6, 7 и 9 октября — короткие сессии без коммитов), но 13 октября его сессия впервые за неделю оставила коммиты.

Ещё одна сессия Codex — в 06:28–06:44, Codex Desktop на ветке exp/menu-memory: 3 хода, 68 вызовов инструментов, коммитов нет. При ней работал ревьюер одобрений (guardian, модель codex-auto-review, effort low, только чтение) — 41 проверка.

Полоса Claude — сообщения агента по часам с 04:00 до 21:00. Вертикальная линия — 20:14, заморозка главы.
-->

---

<Kicker>состояние на 13 октября, 20:14 · 5f5a8ee4</Kicker>

# Что осталось открытым

<div class="grid grid-cols-3 gap-4 mt-2 open">
<div class="card">
<div class="pixel small" style="color: var(--s2)">память в меню</div>

- Простой в меню мерили на симуляторах Apple TV/iPad и на Mac — не на Android, Linux, Windows и Web
- Ресурсы по-прежнему живут до конца сессии: перестали храниться только запросы и ответы
- Сессия VS в прогоне — на виртуальных часах

</div>
<div class="card">
<div class="pixel small" style="color: var(--s3)">контроллер</div>

- C3 на Pixel с Kishi V2 не проверен: сборка стоит на телефоне
- Kishi V2 на Mac и iOS не наблюдался; у Razer для iPhone отдельная модель
- Настоящий iPhone не пробовали — только симулятор
- SIGSEGV потока JIT при выходе — записан, не изучен

</div>
<div class="card">
<div class="pixel small" style="color: var(--s1)">релиз</div>

- Windows — только CrossOver, Linux — только контейнеры
- APK релиза на телефоне не запускали
- Независимого ревью не было
- Пакетные проверки не закрывают приёмку против оригинала: это «preview»

</div>
</div>

<div class="grid grid-cols-4 gap-3 mt-3">
<StatTile value="≈ 29 → 0" label="МБ в минуту простоя в меню" sub="симулятор Apple TV, до и после 340b1a64" size="sm" accent="var(--s2)" />
<StatTile value="4 мин 40 с" label="сыграно на Pixel 10 с Kishi V2" sub="«все работает», 18:58" size="sm" accent="var(--s3)" />
<StatTile value="13 файлов" label="1,48 ГБ на шесть платформ" sub="13 из 13 дайджестов = локальные" size="sm" accent="var(--s1)" />
<StatTile value="3 из 155" label="коммитов с 7 октября без трейлера Claude" sub="все три — релиз, сессия Codex" size="sm" accent="var(--s1)" />
</div>

<div class="card-soft mt-2 xsmall ink2 flex items-center gap-4">
<span class="pixel hl" style="font-size: 1.15rem; white-space: nowrap">1 день</span>
<span>Автор задал вопрос, прислал фото и сыграл 4 минуты 40 секунд. Утечку нашли и закрыли, контроллер опознали со второй попытки — по его собственному USB-отчёту, а релиз на шесть платформ выпустил Codex.</span>
</div>

<div class="source">MENU_MEMORY.md (boundaries) · PHONE_CONTROLLER.md (Gaps, Next task) · phone-controller-c1/c3-20261013.json · release-refresh-20261013.json (boundaries, review, failedRound) · releases-20261013/release-notes.txt</div>

<style>
.open .card { font-size: .72rem; }
.open ul { margin: .3rem 0 0; }
.open li { font-size: .7rem; line-height: 1.35; margin: .28rem 0; }
</style>

<!--
Дословно из карточек и evidence. Память: «Resources are still kept until the session ends (as before); only their iterations' requests and replies are no longer kept», «The soak's VS session is virtual-clock». Контроллер: «the Pixel launch with the controller pending», «Not observed: the Kishi V2 on the Mac and on iOS», «No real iPhone tried». Релиз: «CrossOver harness only, real Windows untested», «Physical-device validation of this package remains open», «No independent reviewer available», и в release notes: «This is a preview. These package checks do not close the remaining original-game, clean-machine or physical-device acceptance gates.»

Codex в репозитории порта открывали и между 5 и 9 октября — короткие сессии по 20–61 вызову инструментов, без коммитов в этой истории. Сессия Codex Desktop утром 13 октября коммитов тоже не оставила.
-->
