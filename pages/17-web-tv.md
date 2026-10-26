---
layout: chapter
num: 17
total: 20
kicker: Глава семнадцатая
dates: 11 — 13 октября
image: /img/covers/ch17-tv-browser.svg
imagePixel: false
stats: 29 коммитов за 34 часа · Apple TV и браузер · 18 088 кадров — те же · 881,5 → 99,5 МБ на первый визит
---

# В браузере и на телевизоре

Swift умеет собираться в WebAssembly — значит, игра 2008 года может открыться во вкладке. iOS-хост почти без правок встаёт на Apple TV. Осталось доказать, что это та же игра, и научить её окно расти.

<div class="cover-note">Обложка — рисунок: один и тот же кадр Demo на телевизоре 16:9 и в окне браузера, не фотография.</div>

<style>
.cover-note { margin-top: 0.7rem; font-size: 0.66rem; color: var(--muted); }
</style>

<!--
Глава о 34 часах, с 11 октября 20:12 до 13 октября 06:21: ветки exp/tvos-web и exp/web-text (карточка TVOS_WEB, шаги T0–T1c и W0–W4) и exp/window-scaling (карточка WINDOW_SCALING, S0–S6). Всё влито в main перемоткой, без merge-коммитов. Цифры главы заморожены на 5f5a8ee4 (13 октября, 20:14); скрипт scripts/collect_web.py.

Обложка: рисунок. Картинка на телевизоре стоит по высоте с полями по бокам — ровно в той пропорции, которую симулятор Apple TV показал в 1080p: 1560 из 1920 пикселей ширины. Кадр — настоящий кадр Demo из приложения AppKit.
-->

---

<Kicker>11 октября, 20:02 · новая задача</Kicker>

# Сначала харнесс, потом хосты

<div class="grid grid-cols-[0.88fr_1.12fr] gap-5">
<div>

<PhoneChat :messages="[
  { who: 'human', time: '20:02', text: 'теперь изучи как ты делал кросскомпиляцию игры и поддержку android/linux/windows/ios/ipad<br>хочу чтобы ты сделал хороший качественный харнес и запустил loop с сборкой поддержки apple tv и web (вроде как swift умеет компилироваться в wasm)', hot: true },
  { who: 'agent', time: '20:10', text: 'Существующие сравнения (<code>compare_headless</code>, <code>compare_frames</code>, группы <code>matrix.py</code>) переиспользую целиком.' },
  { who: 'event', time: '20:12', text: '<code>a16fe0d2</code> · карточка TVOS_WEB, ветка exp/tvos-web, /loop' },
]" />

</div>
<div>

<WebHarness />

</div>
</div>

<WebStepStrip class="mt-2" />

<div class="source">docs/research/TVOS_WEB.md (Harness, Gates) · a16fe0d2 … f0471f13 · журнал сессии 1f9218ae (реплики, время местное, UTC+2) · data/web_steps.json</div>

<!--
Правило карточки, перенесённое с прошлых хостов: «A difference on a new host is a recorded mismatch, never a new expected value». Эталоны — замороженные прогоны: 10 сценариев app_e2e и кадры по группе растеризатора текста: coretext (AppKit, iOS), none (headless, без текста), freetype, gdi.

Лента внизу: 29 коммитов за 34 часа. Наведите на точку — шаг, время, хеш и заголовок коммита. Синие штрихи — реплики автора (только время). Квадраты на оси — коммиты самой карточки. Ночь на 12 октября — перерыв: с 22:18 до 08:06 коммитов нет, в 07:03 автор просит освободить место на диске.
-->

---

<Kicker>11 октября, 20:12 → 22:18 · шаги T0–T1c</Kicker>

# Apple TV — это iOS-хост

<div class="grid grid-cols-[1fr_1fr] gap-6">
<div>

<div class="grid grid-cols-3 gap-2">
<StatTile value="14 мин" label="от карточки до первого сценария на tvOS" sub="vs равен, кадры как у AppKit" size="sm" accent="var(--s1)" />
<StatTile value="30 мин" label="до всех 10 сценариев" sub="a1f3ac0f → 76c40436" size="sm" accent="var(--s1)" />
<StatTile :value="18088" label="кадров — как у AppKit" sub="симулятор Apple TV 4K" size="sm" accent="var(--good)" />
</div>

<div class="card-soft mt-3 small ink2" style="line-height: 1.4">
<div class="pixel hl xsmall mb-1">что пришлось поменять</div>
Три свойства UIKit, которых на tvOS нет: <code>prefersStatusBarHidden</code>, <code>prefersHomeIndicatorAutoHidden</code>, <code>isMultipleTouchEnabled</code>. Папки Documents нет — оверлей в Caches. Касания пульта не должны стать кликами. <b>Для первого запуска Core, Runtime и Package.swift не тронуты.</b>
</div>

<PhoneChat class="mt-3" :messages="[
  { who: 'human', time: '20:53', text: 'надеюсь мы на apple tv сделаем поддержку джойстиков. tv вроде нативно поддерживает подключение геймпадов по блютуз', hot: true },
]" />

</div>
<div>

<WebRemote />

<div class="card-soft mt-1 xsmall ink2" style="line-height: 1.4">
<b class="ink">Ревью, раунд 1:</b> Menu → Esc закрывал бы игру — Esc всегда спрашивает «выйти?», а окно iOS-хоста отвечает Yes; и tvOS присылает кнопку B геймпада как Menu. Переделано: <code>GCEventViewController</code>, Menu не назначена. На Android до T1c кнопка B геймпада <b class="ink">завершала игру</b> тем же путём.
</div>

</div>
</div>

<div class="source">tw-t0-tvos-simulator-20261011.json · tw-t1a-tvos-all-scenarios-20261011.json · tw-t1b-gamepads-tvos-ipad-20261011.json · tw-t1c-gamepads-android-20261011.json · a1f3ac0f · 76c40436 · 64b6e7ef · 3566265f · сессия 1f9218ae</div>

<!--
Время отсчитано от первого коммита карточки (20:12): T0 — 20:26, все 10 сценариев — 20:42. До этого агент 10 минут изучал прошлую кроссплатформенную работу и поставил с сайта Apple среду симулятора tvOS 27.0 (3,76 ГБ).

18 088 «кадров» — это 18 030 дайджестов кадров в событиях и 58 сохранённых PNG, все равны прогону AppKit.

Геймпады: код опроса GameController переехал из AppKit-хоста без изменений в общий класс OriginalGameControllerJoysticks — теперь им пользуются Mac, iPad и Apple TV. Пульт опрашивается каждые 25 мс как клавиши меню. Сценарии от этого измениться не могли: в записанных прогонах джойстики не опрашиваются.

Не проверено: живой контроллер (ни через симулятор, ни на устройстве), Apple TV у настоящего телевизора, Menu во время запуска. Вопрос автора в 21:29 — «ну и геймпад также будет поддерживаться для ios/android сборок?» — превратился в шаг T1c.
-->

---

<Kicker>11 октября, 20:26 → 21:16 · W0–W1, 12 октября 08:06 · W1b</Kicker>

# Swift → wasm32: сначала в терминале

<div class="grid grid-cols-[1.05fr_1fr] gap-6">
<div>

<div class="term">
<div class="tbar"><i class="d r" /><i class="d y" /><i class="d g" /><span class="mono">первая проба · wasm32-unknown-wasip1 · записана в T0, 20:26</span></div>
<div class="tbody mono">
<div class="ln bad">NTSDCore/OriginalMacStartupClock.swift: clock_gettime, timespec, clockid_t, CLOCK_MONOTONIC_RAW, CLOCK_REALTIME, errno not in WASILibc's Swift import</div>
<div class="ln bad">NTSDCore/OriginalConcurrentInputs.swift:60: DispatchQueue (no Dispatch on wasip1)</div>
<div class="ln dim">the build stops in NTSDCore; Runtime and the host are not reached yet</div>
<div class="ln ok">21:16 · 6a17823c · все 10 сценариев под WASI равны эталонам, 18 088 кадров — как у Mac headless</div>
</div>
</div>

<div class="grid grid-cols-3 gap-2 mt-3">
<StatTile value="96 МБ" label="модуль NTSDHeadless.wasm" sub="с отладочной информацией" size="sm" accent="var(--s2)" />
<StatTile value="Node 26" label="Node 20 падал на компиляции" sub="V8: GC fatal error" size="sm" accent="var(--s2)" />
<StatTile value="0,9 с" label="загрузка под WASI" sub="нативно — 0,33 с" size="sm" accent="var(--s2)" />
</div>

</div>
<div class="wasi">

<div class="blk">
<div class="bh pixel">чего нет в wasm32-wasip1 — и чем заменили</div>

- **Dispatch** — главная очередь на WASI стала списком таймеров: по сроку, потом по порядку создания
- **потоки** — упреждающее чтение, параллельные загрузки, рендер и отложенное освобождение идут по очереди, в том же порядке
- **часы** — вызов WASI вместо `clock_gettime`; **сокеты** — заглушка: ONLINE GAME в браузере нет

</div>

<div class="blk warn">
<div class="bh pixel">Int — 32 бита</div>
Бюджет памяти дисплея <code>3&lt;&lt;30</code> стал отрицательным. Значения ≥ 2³¹ из файлов на 64-битных хостах дают ошибку, а на wasm32 — аварийную остановку. W1b нашёл 9 таких категорий, 47 проверочных случаев. Среди них — находка ревью: <b>имя игрока в GBK</b> (байт 0x80–0xFB) роняло игру на первом кадре матча.
</div>

<div class="blk">
<div class="bh pixel">почему только под #if arch(wasm32)</div>
64-битное сравнение везде подняло память Mac после загрузки на ≈ 80 МБ. Остальные хосты компилируют прежние строки: код и данные бинарника Mac — те же, что до шага.
</div>

</div>
</div>

<div class="source">tw-t0-tvos-simulator-20261011.json (wasiProbe) · tw-w0-w1-wasi-headless-20261011.json · tw-w1b-wasm32-boundaries-20261012.json · TVOS_WEB.md (Verified starting point, W0, W1b) · 6a17823c · d5cf2f0a</div>

<style>
.term { background: #0c1017; border: 1px solid rgba(255,255,255,.1); border-radius: 10px; overflow: hidden; }
.tbar { display: flex; align-items: center; gap: 6px; height: 22px; padding: 0 9px; background: #161b25; border-bottom: 1px solid rgba(255,255,255,.06); }
.tbar .mono { font-size: .64rem; color: var(--muted); margin-left: .5rem; }
.d { width: 9px; height: 9px; border-radius: 50%; }
.d.r { background: #ff5f57; } .d.y { background: #febc2e; } .d.g { background: #28c840; }
.tbody { padding: .45rem .7rem .55rem; font-size: .64rem; line-height: 1.45; }
.tbody .ln { margin: .1rem 0; }
.tbody .bad { color: #ffb4a8; }
.tbody .dim { color: var(--muted); }
.tbody .ok { color: #a6e3a6; margin-top: .35rem; padding-top: .3rem; border-top: 1px dashed rgba(255,255,255,.12); }
.wasi { display: flex; flex-direction: column; gap: .45rem; }
.wasi .blk { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: .4rem .7rem .45rem; font-size: .68rem; line-height: 1.38; color: var(--ink-2); }
.wasi .blk.warn { border-color: rgba(250,178,25,.45); }
.wasi .bh { font-size: .66rem; color: var(--naruto); margin-bottom: .15rem; }
.wasi .blk.warn .bh { color: var(--warning); }
.wasi ul { margin: 0; }
.wasi ul > li { margin: .12rem 0; padding-left: .95rem; font-size: .68rem; line-height: 1.34; }
.wasi ul > li::before { top: .5em; width: 5px; height: 5px; }
</style>

<!--
Строки терминала — дословно из evidence первой пробы (wasiProbe.blockers, 11 октября, 20:26); итог — из коммита 6a17823c в 21:16. От старта карточки до «все 10 сценариев под WASI» прошло 64 минуты.

WASI здесь — тестовый стенд, как Rosetta и Wine для других хостов: настоящая платформа веб-версии — браузер. SDK — официальный swift-6.4.0-RELEASE_wasm со swift.org, контрольная сумма архива проверена при установке.

W1b (12 октября, 08:06): проба wasm32 на входах тестов дала исходы macOS во всех 47 случаях и аварийные остановки во всех 9 категориях на старых исходниках. Находка для ядра: такие имена — граница outOfBounds и на 64-битных хостах: оригинал читает служебные слова аллокатора перед записью глифа.
-->

---

<Kicker>12 октября, 09:09 → 16:51 · W2a–W2b-4c</Kicker>

# Воркер, который не отдаёт управление

<p class="small ink2 lead">Цикл игры не возвращает управление браузеру, поэтому со страницей он говорит только через общую память. На каждом канале нашлась ошибка.</p>

<WebBridge />

<div class="source">TVOS_WEB.md (ledger W2a–W2b-4c) · tw-w2b1 … tw-w2b4c evidence · ce9b3c5f · b0b6b470 · 6f4cb344 · c1cd3f91 · f829a551 · 4f678fa7 · 21f5caa9 · native/Sources/NTSDWeb · tools/crossplatform/web/run.html, wasi-worker.js, audio.js</div>

<style>
.lead { margin: -0.45rem 0 0.35rem !important; max-width: 54rem; line-height: 1.4; }
</style>

<!--
Наведите на канал или на карточку — подсветятся оба. «Ревью» — независимое ревью только для чтения, которое карточка требует для каждого слоя хоста; «тест» — нашлось при прогонах.

Хост NTSDWeb — это сервисы headless-хоста плюс вывод кадра как импорт wasm; он собирается только под wasm32 с NTSD_WEB=1. Звук: headless Chromium по умолчанию открыл аудиоконтекст на 192 кГц и переполнил первое кольцо — поэтому контекст фиксирован на 44,1 кГц, частоте треков игры. Ещё одна находка W2b-4b: без папки /save хост падал при старте — его временный оверлей лежал вне смонтированных папок, и Foundation на WASI в таком случае не бросает ошибку, а останавливается.

12:12 автор спросил: «можно потестить в браузере самому?» — через минуту получил локальный сервер на 127.0.0.1:8123 со своей папкой сохранений.
-->

---
clicks: 1
---

<Kicker>11 → 13 октября · те же эталоны</Kicker>

# 18 088 кадров — те же

<WebHostStrip stepwise />

<div class="grid grid-cols-[1.1fr_1fr] gap-5 mt-2 xsmall ink2">
<div class="card-soft"><b class="ink">13 октября, 05:37 — «где шрифты?»</b> Автор открыл веб-версию и не нашёл имён, счётчиков и цифр итогов: в браузере не было растеризатора текста GDI. Выбрал шрифты браузера — через 44 минуты, в 06:21, текст стоял ровно в тех же кадрах, что у CoreText.</div>
<div class="card-soft"><b class="ink">Почему «как Mac headless».</b> До W4 браузер текста не рисовал, и его эталон — группа без текста. Теперь у каждого движка своя группа: буквы — это шрифт и сглаживание движка, а не игра.</div>
</div>

<div class="source">tw-t1a-tvos-all-scenarios-20261011.json · tw-w0-w1-wasi-headless-20261011.json · tw-w3e-wasi-lazy-packages-20261012.json · web-text-20261013.json (f0471f13, тег web-f0471f13-20261013) · ws-s1-tvos-full-screen-20261013.json · data/web_hosts.json</div>

<!--
Сначала — состояние до W4: все четыре хоста равны эталонам, браузер рисует кадр без текста. По клику — W4: текст шрифтом браузера, полужирный 13 px системного шрифта платформы, с той же геометрией ячейки, что у CoreText и FreeType.

Наведите на клетку — что было в этом прогоне: у Apple TV — число дайджестов кадров и PNG, у браузеров — сколько кадров страница действительно нарисовала (vs: 2 339 из 2 341; война: 3 611 из 3 611).

18 088 — это 18 030 дайджестов кадров и 58 сохранённых PNG; сравнение текста идёт по 18 030 дайджестам. Строки браузеров — повторный прогон W3e (12 октября), Apple TV — T1a, повторено в S1 после масштабируемого окна. Chromium в повторном прогоне дал те же кадры и все 1 826 дайджестов vs.
-->

---
clicks: 1
---

<Kicker>12 октября, 17:36 · вопрос автора</Kicker>

# «хромиум wasm быстрее чем нативная mac версия?»

<div class="grid grid-cols-[0.9fr_1.1fr] gap-6">
<div>

<PhoneChat :messages="[
  { who: 'human', time: '17:36', text: 'хромиум wasm быстрее чем нативная mac версия?', hot: true },
  { who: 'agent', time: '17:37', text: '<b>Нет, нативная Mac-версия быстрее.</b> Таблица выше сравнивала разные вещи, и моя фраза «браузер экономнее всего Mac-процесса» в предыдущем сообщении вводила в заблуждение. … Честное сравнение — Mac с отрисовкой в том же потоке. У headless-хоста для этого есть ключ <code style=\'white-space: nowrap\'>--synchronous-render</code>.' },
  { who: 'human', time: '17:38', text: 'понятненько' },
]" />

<div class="card-soft mt-3 xsmall ink2" style="line-height: 1.4">Всё — далеко под бюджетом: <b class="ink">16,7 мс</b> на кадр при 60 fps и <b class="ink">33 мс</b> на тик оригинала. Дорого другое: от старта до загрузки — <b class="ink">5,6 с</b> в Chromium против 0,63 с на Mac. Линейная память модуля — <b class="ink">1 617 МиБ</b>.</div>

</div>
<div>

<WebFrameTime stepwise />

</div>
</div>

<div class="source">tw-w3a-browser-frame-time-20261012.json (medians, comparison) · ef6e880a · сессия 1f9218ae, 12 октября 17:36–17:38 · data/web_frametime.json</div>

<!--
Сначала — что сравнивала первая таблица: Mac 1,33 мс — только игровой поток, рисование идёт рядом в потоке рендера; Mac 3,23 мс — CPU, сложенный по всем потокам, с очередями и пересылками; Chromium 2,24 мс — один поток делает и тик, и отрисовку. Ни одно из чисел Mac с Chromium не сравнимо.

По клику — замер, сделанный после вопроса и до коммита W3a: тот же бинарник Mac с --synchronous-render рисует в игровом потоке, как wasm. Тогда Chromium медленнее Mac в 1,17 раза, WebKit — в 1,71, Node WASI — в 1,92. Наведите на полосу — значение для Demo.

Метод: по три прогона, VS по телам 600–1500 и Demo по 300–900, один хост за раз на этом Mac; Chromium 153 headless и WebKit из Playwright. Фразу «меньше, чем у Mac» в журнале и evidence агент обещал заменить до коммита — в evidence W3a стоит раздел comparison о том, что сравнимо, а что нет.
-->

---

<Kicker>12 октября, 16:51 → 19:27 · W2b-4c, W3b</Kicker>

# 881,5 МБ на первый визит

<div class="grid grid-cols-[1.08fr_1fr] gap-6">
<div>

<WebBytes />

<p class="xsmall ink2 mt-1 mb-0" style="line-height: 1.4">Игра, как и оригинал, загружает все данные при старте. Картинки BMP сжимаются в 36 раз; музыку меню (ALAC) и WMA сжать уже нельзя. WebKit по HTTP не берёт brotli — у него 120,9 МБ в gzip.</p>

</div>
<div>

<PhoneChat :messages="[
  { who: 'human', time: '11 окт, 20:48', text: '2. тестируй локально, по публикации на сервер я планировал vercel использовать. хз как дешевле всего раздавать. я на этом нисколько не буду зарабатывать и хотелось бы бесплатно где-то захостить или с минимальным биллингом', hot: true },
]" />

<div class="tiers mt-2">
<div class="tr"><b>Vercel Hobby</b><span>100 ГБ трафика в месяц, файл до 100 МБ</span></div>
<div class="tr"><b>Cloudflare R2</b><span>10 ГБ хранения, исходящий трафик бесплатный</span></div>
<div class="tr"><b>Cloudflare Pages</b><span>файл до 25 МиБ — программа 96 МБ и трек 27,5 МБ не влезут</span></div>
</div>

<p class="xsmall muted mt-1 mb-0" style="line-height: 1.4">Арифметика, не замер: 100 ГБ в месяц — это ≈ 1 000 первых визитов по 99,5 МБ или ≈ 113 по 881,5 МБ.</p>

<div class="card-soft mt-2 xsmall ink2" style="line-height: 1.4"><b class="ink">Совет агента:</b> страница — на Vercel, данные — в R2. <b class="ink">Оговорка:</b> это файлы оригинальной игры, выкладывать их — решение автора. Страница, которая открывает копию игрока, ничего не распространяет.</div>

</div>
</div>

<div class="source">tw-w2b4c-browser-static-20261012.json (firstLoad.measure: brotli 11, gzip 6) · tw-w3b-browser-compressed-20261012.json · TVOS_WEB.md (Hosting, лимиты проверены 11 октября) · 21f5caa9 · 5d24e399 · сессия 1f9218ae · data/web_delivery.json</div>

<style>
.tiers { display: flex; flex-direction: column; border-top: 1px solid var(--axis); }
.tiers .tr { display: grid; grid-template-columns: 7.6rem 1fr; gap: .5rem; padding: .26rem .1rem; border-bottom: 1px solid var(--grid); font-size: .68rem; color: var(--ink-2); }
.tiers b { color: var(--ink); font-weight: 650; }
</style>

<!--
Полосы — одна сессия первого визита по видам файлов (web_app.py measure): серым — как лежит, синим — что уйдёт по сети с brotli 11. Наведите на строку — gzip и число файлов. 691 МБ BMP превращаются в 19 МБ: старые картинки с палитрой и большими заливками.

Сжатые формы лежат рядом с файлами (NAME.br, NAME.gz) и отдаются хостом с Content-Encoding — программа читает те же байты; воркер проверяет размер каждого файла по списку, так что хост, который снял или удвоил сжатие, ломает запуск громко: «2815 bytes, listed 5326 (the host altered it)».

Тарифы — как их проверил агент 11 октября по документации; Vercel по документации сжимает image/bmp на лету — не проверено.
-->

---

<Kicker>12 октября, 19:27 → 22:47 · W3b, W3c, W3e, W3f · канал 100 Мбит/с</Kicker>

# Меню через 5,6 секунды, а не через 75

<WebFirstVisit />

<div class="source">tw-w3b-browser-compressed-20261012.json · tw-w3c-browser-startup-20261012.json · tw-w3e-wasi-lazy-packages-20261012.json · tw-w3f-browser-prefetch-overlap-20261012.json · 5d24e399 · b90394c0 · 05e9c595 · 9d7beb8a · data/web_delivery.json</div>

<!--
Двигайте ползунок скорости. Каждая строка — сборка страницы, измеренная дважды: без ограничения и при 100 Мбит/с, по три холодных визита в Chromium. Полоса — прямая через эти две точки: синяя часть — сколько мегабайт должно прийти до меню, делённое на скорость; рыжая — старт программы. На 100 Мбит/с и «∞» это сам замер, в остальных точках — оценка. Сервер локальный, ограничена только полоса, задержек сети нет: настоящий визит будет дольше.

Порядок событий. W3b: сжатие — 881,5 → 99,5 МБ, меню через 12,8 с вместо 75,5. Остаток — старт программы, и профиль W3c показал, куда он уходит: 2,2 с SHA-256 всех упакованных файлов, ожидание подкачки, чтение из кэша, LZ4. Первый вывод — «помогут только потоки» — ревью опровергло: на WASI пакеты загрузки считались при создании, до первого кадра меню, хотя меню нужен один стартовый пакет на 29,7 МБ. W3e перенёс их на первую загрузку — 5,4 → 1,8 с. W3f: страница качает файлы, пока программа стартует, уступая её собственным чтениям до первого кадра.

Две промежуточные версии W3f тоже замерены: восемь потоков без шлюза — 55,8 с (музыка меню, 27,5 МБ, ждала за всей загрузкой), список файлов до компиляции модуля — 38 с (ждал модуль на 96 МБ).
-->

---

<Kicker>12 октября, 21:50 → 13 октября, 04:48 · S0–S6</Kicker>

# Окно, которое растёт

<WebWindowDemo />

<div class="quote xsmall ink2 mt-2"><span class="mono muted">21:50</span> «…запуск в оригинальном формате оставь под флагом. на всех платформах должно работать особенно на apple tv где запуск должен быть на весь экран телевизора.» <span class="muted">Следом:</span> «ну и браузер тоже важен»</div>

<div class="source">docs/research/WINDOW_SCALING.md · ws-s1 … ws-s6 evidence · tw-w2b4b-browser-page-20261012.json · f075d765 · 71e5243a · b7cd16c6 · d45fd928 · f7aeada1 · df74758a · data/web_window.json</div>

<style>
.quote { border-left: 3px solid var(--naruto); padding: .25rem .7rem; background: rgba(255,255,255,.03); border-radius: 0 8px 8px 0; line-height: 1.4; }
</style>

<!--
Просьба автора целиком (12 октября, 21:50): «как закончишь с web-ом влей в main и отведи отдельную ветку где поработай над тем чтобы мы могли скейлить окно игры и использовать нативные кнопки fullscreen для запуска игры на полный экран. запуск в оригинальном формате оставь под флагом. на всех платформах должно работать особенно на apple tv где запуск должен быть на весь экран телевизора.»

Это модель, а не запись экрана: настоящий кадр 794×550 вписывается в экран или окно хоста по той же формуле, что у хостов, — пропорция сохраняется, пиксели ближайшие. Кнопки — размеры, которые замерили в evidence; справа рядом с моделью стоит замер. Потяните угол окна (у Mac, Linux и браузера), включите --original-window, наведите на картинку — увидите, в какой пиксель игры попадёт клик.

Главное: игра всё время видит своё окно 794×550, масштаб — только в показе и в пересчёте ввода. Apple TV уже занимал весь телевизор по высоте; S1 это проверил на 1080p и 4K и добавил оригинальный формат по центру. Масштаб 1,96× нецелый: 20 строк и 29 столбцов игры получают по 1 пикселю вместо 2 — ровно это и записано в evidence S1. Растянуть картинку на 16:9 или сгладить её — вопрос автору: это исказит или размоет оригинал.

Mac: окно открывается в 2× на дисплее 6K. A/B фиксированного окна против 2×: 2,02 против 1,74 мс на тик, пик памяти 799 против 692 МБ — дешевле, потому что масштабирует компоновщик, а первая сборка с буфером размера окна стоила +73–78 МБ и была заменена. Linux: Xvfb без оконного менеджера, клики настоящим xdotool; Wayland — полный экран и обратно с побайтно равными кадрами. Android: по умолчанию масштабирует компоновщик — отсюда 1041 вместо 1039 пикселей.
-->

---

<Kicker>состояние на 13 октября, 06:21 · всё влито в main</Kicker>

# Флаг на каждом хосте — и что не проверено

<div class="grid grid-cols-[1.2fr_1fr] gap-5">
<div>

<table class="flags">
<colgroup><col style="width: 15%"><col style="width: 27%"><col style="width: 35%"><col style="width: 23%"></colgroup>
<thead><tr><th>хост</th><th>по умолчанию</th><th>оригинальное окно</th><th>полный экран</th></tr></thead>
<tbody>
<tr><td><b>macOS</b></td><td>окно растёт; на 6K — 2×</td><td><code>--original-window</code><br><code>-NTSDOriginalWindow YES</code></td><td>зелёная кнопка, ⌃⌘F</td></tr>
<tr><td><b>SDL</b></td><td>окно растёт, Linux и macOS</td><td><code>--original-window</code><br><code>NTSD_ORIGINAL_WINDOW=1</code></td><td>кнопки окна</td></tr>
<tr><td><b>Apple TV</b></td><td>весь телевизор</td><td><code>--original-window</code> или настройка</td><td>всегда</td></tr>
<tr><td><b>iPad</b></td><td>весь экран</td><td>как у Apple TV</td><td>всегда</td></tr>
<tr><td><b>Android</b></td><td>весь экран, масштабирует система</td><td>строка в <code>files/args.txt</code> через adb</td><td>всегда</td></tr>
<tr><td><b>браузер</b></td><td>холст под окно</td><td><code>?original-window</code> или <code>config.json</code></td><td>кнопка Full screen</td></tr>
</tbody>
</table>

<p class="xsmall muted mt-2 mb-0" style="line-height: 1.4">Alt+Enter везде остаётся игровым, как в оригинале: его всплывающее окно заполняет экран в обоих режимах. Сценарии идут в оригинальном окне — их кадры не зависят от дисплея.</p>

</div>
<div class="honest">

<div class="blk">
<div class="bh pixel">стенд, а не устройство</div>
Apple TV и iPad — симуляторы, настоящий телевизор и его overscan не видели. Браузеры — headless Chromium 153 и WebKit из Playwright; Safari, Firefox и браузер телефона (модулю нужно 1,6 ГБ) — открыты. Windows SDL не собиралась. Живой геймпад на Apple TV и в браузере не пробовали.
</div>

<div class="blk">
<div class="bh pixel">не опубликовано</div>
В 05:37 автор спросил: «ну что задеплоим web версию?» — и через 21 секунду прислал «где шрифты?». Ответа про деплой в журнале нет. В 15:28 веб-архив лёг в релиз native-preview-20261013: <span class="ink">«Static archive, not a new deployed website»</span>.
</div>

<div class="blk warn">
<div class="bh pixel">ждёт автора</div>
Где лежат данные и можно ли их выкладывать; растянуть ли картинку на 16:9; сглаживать ли нецелый масштаб.
</div>

</div>
</div>

<div class="source">WINDOW_SCALING.md (Flags and controls, Next task) · TVOS_WEB.md (Next task) · release-refresh-20261013.json (web) · 0b5d4621 · df74758a · f0471f13 · сессия 1f9218ae (05:35–05:40)</div>

<style>
table.flags { font-size: .68rem; table-layout: fixed; }
table.flags td, table.flags th { padding: .3rem .45rem; }
table.flags td code { font-size: .62rem; white-space: nowrap; }
.honest { display: flex; flex-direction: column; gap: .45rem; }
.honest .blk { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: .4rem .7rem .45rem; font-size: .66rem; line-height: 1.38; color: var(--ink-2); }
.honest .blk.warn { border-color: rgba(250,178,25,.45); }
.honest .bh { font-size: .66rem; color: var(--naruto); margin-bottom: .15rem; }
.honest .blk.warn .bh { color: var(--warning); }
</style>

<!--
Таблица — сжатый пересказ раздела «Flags and controls» карточки WINDOW_SCALING; ревьюер сверил её с кодом каждого хоста и исправил четыре утверждения. SDL для Windows использует тот же код, но не собиралась; полный экран у macOS SDL — зелёная кнопка, руками не пробовали. Флаг Apple TV можно положить в настройку NTSDOriginalWindow, которую приставка носит без аргументов запуска.

Что было после 06:21. В 05:40 автор нашёл в мониторе активности процесс на 11 ГБ — экземпляр игры в симуляторе после проверок: память меню росла примерно на 30 МБ в минуту на всех хостах. Это следующая ветка, exp/menu-memory, влита в 08:15. В 15:28 опубликован релиз native-preview-20261013 с веб-архивом: «requires configured COOP/COEP and Content-Encoding for precompressed forms». Сайт так и не развёрнут.

Оставлено в карточке TVOS_WEB: SIMD-вариант SHA-256 (W3g), браузер телефона (W3d), ручные проверки и хранение, звук и жизненный цикл на tvOS (T2).
-->
