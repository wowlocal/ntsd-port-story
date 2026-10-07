---
layout: chapter
num: 13
total: 15
kicker: Глава тринадцатая
dates: 3 — 5 октября
image: /img/covers/ch13-nine-hosts.jpg
imagePixel: false
stats: 74 коммита за 30 часов · 9 хостов · 90 из 90 сценариев · 1 баг компилятора
---

# Одно ядро, девять хостов

Через три с половиной часа после релиза агент получил новую задачу: та же игра на Linux, Windows, iPad и Android, собранная с одного Mac. Ядро трогать нельзя.

<!--
Обложка — иллюстрация: один и тот же кадр Demo из AppKit-приложения, повторённый девять раз с подписями хостов. Настоящие кадры хостов без текста (Linux, Windows и Android без окна) надписей не содержат; побайтное равенство кадров — на слайде с матрицей.
-->

---

<Kicker>точка отсчёта · 3 октября, 16:46</Kicker>

# v0.4.0: игру можно скачать

<div class="grid grid-cols-3 gap-4 mt-2" style="font-size: 0.74rem">
<div class="card">
<div class="pixel small" style="color: var(--s3)">что внутри</div>

- Все режимы оригинала: VS, Mission, Tournament, Team Tournament, War, Demo и просмотр записей — с его меню, HUD, Summary и концовкой Stage.
- 25 персонажей, 17 фонов, 25 стейджей. Записи `.lfr` совместимы с оригиналом в обе стороны.
- DMG на 245 МБ: подпись Developer ID, нотаризация Apple, тикет вшит. macOS 14+, Apple silicon.

</div>
<div class="card">
<div class="pixel small" style="color: var(--s1)">сверено с оригиналом</div>

- 58 целых матчей с одинаковыми Summary: VS с 1–7 компьютерными игроками, War, первая фаза каждой группы Stage, все три обычные сложности, все 25 персонажей и 17 фонов.
- Записи проверены в обе стороны: Mac → оригинал и оригинал → Mac.

</div>
<div class="card">
<div class="pixel small" style="color: var(--s4)">объявлено честно</div>

- Несколько надписей, которые оригинал рисует через Windows GDI, — системным шрифтом macOS.
- Музыка Demo — объявленная замена.
- Ещё не сверены с оригиналом: турниры целиком, Stage дальше первой фазы, *CRAZY!* и онлайн-игра, которая ещё в работе.

</div>
</div>

<div class="card-soft mt-3 xsmall ink2 flex items-center gap-4">
<span class="pixel hl" style="font-size: 1.2rem; white-space: nowrap">20:08</span>
<span>Человек вставляет внешний обзор архитектуры: «a good candidate for Windows and Linux ports without rewriting the gameplay core». Агент сверяет его с кодом, пишет план и запускает <code>/loop</code>.</span>
</div>

<div class="source">github.com/wowlocal/ntsd-2.4/releases/tag/v0.4.0 · tools/release-macos.sh · docs/research/CROSSPLAY_MATRIX.md · CROSS_PLATFORM.md L8–10 · журнал сессии 1f9218ae</div>

<!--
Обзор, который вставил человек, в плане назван так: «Its claims are leads to verify, not evidence». Подтверждённое по коду записано отдельно, в разделе Verified starting point.
-->

---

<Kicker>план · /loop на ветке dev/crossplatform · 3 октября, 20:11–21:01</Kicker>

# Агент в цикле: план на девять фаз

<div class="grid grid-cols-[1.3fr_1fr] gap-6 mt-1">
<div>

<Timeline dense :items="[
  { time: '20:11', title: 'план: одно ядро на всех платформах, фазы P0–P8', hash: 'c753d7c' },
  { time: '20:20', title: 'Static Linux SDK 6.4.0: проба собрана и запущена в контейнерах; ядро упёрлось в import CryptoKit', hash: 'c649bac' },
  { time: '20:32', title: 'свой SHA-256: на 1 528 файлах игры (874 МБ) дайджесты равны CryptoKit', hash: '4547acc' },
  { time: '20:37', title: 'часы по ОС — NTSDCore собирается под Linux', hash: '65c6916', hot: true },
  { time: '20:54', title: 'zlib вместо Compression: 1 934 фикстуры, 18,3 ГБ — байт в байт; все 9 проверочных программ под Linux', hash: '699f9ec' },
  { time: '21:00', title: 'манифест без Mac-целей: все 696 тестов на месте; в static musl SDK нет XCTest', hash: '48db790' },
  { time: '21:01', title: 'Swift SDK для Windows извлечён из официального установщика; дальше нужна лицензия Microsoft', hash: '6203799' },
]" />

<div class="card-soft mt-2 xsmall ink2">Методика переехала вместе с кодом: <span class="mono">«A difference on a new platform is a recorded mismatch, never a regenerated expected value.»</span> Wine, CrossOver и контейнеры — только стенды, не рантайм.</div>

</div>
<div>

<PhaseRail :phases="[
  { id: 'P0', name: 'тулчейны', state: 'done', note: 'Linux, Windows, iOS и Android — кросс-сборкой с одного Mac' },
  { id: 'P1', name: 'граф пакета', state: 'done', note: 'сборка без Mac-целей, тесты разделены переносом файлов' },
  { id: 'P2', name: 'переносимость ядра', state: 'done', note: 'SHA-256, часы, zlib — ядро и проверки собираются под Linux' },
  { id: 'P3', name: 'детерминизм на Linux', state: 'done', note: '581 переносимый тест прошёл, 0 упало; на x86_64 — 595' },
  { id: 'P4', name: 'Windows без окна', state: 'done', note: 'те же сценарии под Wine; настоящий Windows не наблюдался' },
  { id: 'P5', name: 'общий рантайм', state: 'done', note: 'окно, звук, ввод, сокеты — за протоколами NTSDRuntime' },
  { id: 'P6', name: 'бэкенд SDL3', state: 'done', note: '15 909 кадров SDL побайтно равны AppKit' },
  { id: 'P7', name: 'Linux и Windows', state: 'done', note: 'пакеты, музыка, онлайн; pre-release 4 октября' },
  { id: 'P8', name: 'мобильные', state: 'part', note: 'iPad и Android работают; скорость на телефоне — глава 14' },
]" />

<div class="xsmall muted mt-1">состояние фаз на 5 октября</div>

</div>
</div>

<div class="source">ntsd-2.4 (ветка dev/crossplatform): docs/research/CROSS_PLATFORM.md — план, правила, журнал статуса · c753d7c … 6203799 · состояние фаз — журнал статуса 5 октября</div>

<!--
Слева — первый час цикла, как он шёл. Справа — те же девять фаз через тридцать часов: в стенде пройдены все, кроме скорости на телефоне. «Стенд» здесь честное слово: контейнеры, CrossOver, симулятор и эмулятор на одном Mac.
-->

---

<Kicker>что пришлось поменять · 3 → 5 октября</Kicker>

# Ядро почти не тронуто

<CoreWaffle class="mt-2" />

<div class="grid grid-cols-3 gap-4 mt-3 xsmall ink2">
<div><b class="ink">Переносимость — да, поведение — нет.</b> Свой SHA-256 вместо CryptoKit (96 строк, дайджесты равны на 1 528 файлах), часы по ОС, чтение файлов без Darwin, папку ресурсов называет хост. +24 / −14 — обход бага компилятора.</div>
<div><b class="ink">Mac-слой похудел на 4 504 строки.</b> Окно, звук, ввод, сокеты и цикл приложения теперь в NTSDRuntime за протоколами. На Mac остались 1&nbsp;534 строки адаптеров AppKit.</div>
<div><b class="ink">Новая платформа — это хост.</b> Android — NativeActivity без строчки Java, 572 строки. iPad — 301. Хосту нужно ответить на те же запросы ядра: окно, кадр, звук, сокет, часы.</div>
</div>

<div class="source">git ls-tree 74be317 / 2fe64be native/Sources · git diff --numstat 74be317 2fe64be -- native/Sources/NTSDCore · CROSS_PLATFORM_RUNTIME.md · data/xplat.json</div>

<!--
Квадраты — строки Swift в native/Sources на 2fe64be, вечер 4 октября, перед работой с телефоном. Проверочные программы и NTSDReferenceChecks (11,8 тыс. строк) не показаны: в игру они не входят.
Изменённые строки ядра — по numstat: 223 добавлено, 26 удалено в 11 файлах. Самое большое — PortableSHA256: CryptoKit есть только на Apple, а ядро считает SHA-256 ресурсов при загрузке.
-->

---

<Kicker>3 октября, 20:11 → 5 октября, 02:23</Kicker>

# 30 часов, шесть платформ

<HostDayStrip class="mt-1" />

<div class="grid grid-cols-3 gap-4 mt-1 xsmall ink2">
<div><b class="ink">Ночью — Linux.</b> К 04:00 целый VS-матч без окна идёт в контейнере с тем же состоянием, что на Mac, и его кадры побайтно равны.</div>
<div><b class="ink">Днём — Windows и iPad.</b> Windows под CrossOver с настоящим Winsock, iPad в симуляторе. Экран Mac заблокирован с 12:20: окно AppKit в такой сессии не рисует, и два хоста ждут человека.</div>
<div><b class="ink">Вечером — Android.</b> От первого запуска NativeActivity до текста, звука и музыки — 22 минуты. В 01:59 все девять хостов дают одно состояние.</div>
</div>

<div class="source">git log 74be317..75593f5 (ветка dev/crossplatform) · дорожка — по изменённым файлам коммита · реплики человека — журнал сессии 1f9218ae (только время) · data/xplat.json · data/loop.json</div>

<!--
Наведите на точку — подсказка с временем и заголовком коммита. Синие точки — реплики человека, их 13 за эти 30 часов. Штриховка — экран Mac заблокирован с 12:20 до 19:45: агент прогнал матрицу на шести хостах, которым экран не нужен, нашёл ошибку в собственных прогонах под Wine (CrossOver не передаёт программам переменные SDL_*), записал исправление, а в 19:24 остановил цикл: «everything left needs you».
-->

---

<Kicker>4 октября, 05:14 · ошибка не в игре</Kicker>

# Баг компилятора, который нашла матрица

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-1">
<div class="small ink2">

Тот же сценарий, собранный под Linux x86_64, падает сразу после старта: **SIGSEGV**, код 139. Под QEMU — так же, значит, Rosetta ни при чём. В отладчике падение — внутри `isKnownUniquelyReferenced`, вызванного из `OriginalRetainedHistory`.

<div class="asm mt-2">
<div class="asmc">
<div class="asmh"><span class="dot" style="background: var(--good)" />macOS arm64 · Xcode Swift 6.4</div>
<pre>str  x22, [sp, #0x8]   <i>узел записан в слот</i>
…
bl   isKnownUniquelyReferenced
ldr  x0, [sp, #0x8]</pre>
</div>
<div class="asmc bad">
<div class="asmh"><span class="dot" style="background: var(--critical)" />Linux aarch64 · Static SDK 6.4.0</div>
<pre>add  x0, sp, #0x8      <i>адрес слота</i>
bl   isKnownUniquelyReferenced
<i>x21 в слот так и не записан</i></pre>
</div>
</div>

</div>
<div>

<div class="xsmall muted mb-1">короткая программа из отчёта, по три запуска</div>
<div class="bugtab">
<div class="r"><span>Static Linux SDK, x86_64</span><b class="bad">SIGSEGV 3 из 3</b></div>
<div class="r"><span>Static Linux SDK, aarch64</span><b class="bad">SIGSEGV 3 из 3</b></div>
<div class="r"><span>glibc-SDK, aarch64</span><b class="ok">верно 3 из 3</b></div>
<div class="r"><span>macOS arm64</span><b class="ok">верно</b></div>
</div>

<Timeline class="mt-3" dense :items="[
  { time: '05:14', title: '4 окт · обход в OriginalRetainedHistory: порядок освобождения тот же, x86_64 и aarch64 дают одинаковые кадры', hash: 'a72ae97' },
  { time: '20:52', title: '4 окт · с разрешения человека — отчёт swiftlang/swift#92905; после перепроверки сужен до Static Linux SDK', hash: 'b13b1de' },
  { time: '12:06', title: '6 окт · «This is fixed on 6.4.x by #92771» — отчёт закрыт инженером Swift', hot: true },
]" />

<div class="card-soft mt-2 xsmall ink2">В самой игре aarch64 «выжил случайно», а x86_64 упал. Без замороженных эталонов это выглядело бы как ошибка порта. Урок про оракул повторился: ошибся инструмент, а не оригинал.</div>

</div>
</div>

<div class="source">a72ae97 · b13b1de · docs/evidence/crossplatform-swift640-linux-uniqueness-20261004.json · crossplatform-swift640-report-20261004.json · github.com/swiftlang/swift/issues/92905</div>

<style>
.asm { display: grid; grid-template-columns: 1fr; gap: 0.5rem; }
.asmc { background: var(--surface); border: 1px solid var(--hair); border-radius: 10px; padding: 0.45rem 0.7rem 0.5rem; }
.asmc.bad { border-color: rgba(208, 59, 59, 0.5); }
.asmh { font-size: 0.62rem; color: var(--ink-2); margin-bottom: 0.2rem; }
.asmh .dot { width: 8px; height: 8px; margin-right: 0.35rem; }
.asmc pre { margin: 0; font-family: var(--font-mono); font-size: 0.66rem; line-height: 1.45; color: var(--ink); white-space: pre; }
.asmc pre i { font-style: normal; color: var(--muted); }
.bugtab { display: flex; flex-direction: column; border-top: 1px solid var(--axis); }
.bugtab .r { display: flex; justify-content: space-between; align-items: baseline; padding: 0.28rem 0.1rem; border-bottom: 1px solid var(--grid); font-size: 0.72rem; color: var(--ink-2); }
.bugtab b { font-weight: 650; font-size: 0.72rem; }
.bugtab b.bad { color: #f08a8a; }
.bugtab b.ok { color: #7fd17f; }
</style>

<!--
Механизм по разбору: оптимизатор считает, что неспециализированный обобщённый вызов isKnownUniquelyReferenced не читает свой inout-аргумент, и выбрасывает запись узла в слот. Обход — отдельный необобщённый класс-звено, вызываемый из deinit узла: там вызов специализируется, порядок освобождения прежний.
Первая версия отчёта утверждала, что затронут и glibc-SDK. Перепроверка короткой программы это опровергла, и текст отчёта исправили на месте с пометкой, до первого ответа.
-->

---
clicks: 1
---

<Kicker>девять хостов · десять сценариев · одни эталоны</Kicker>

# 90 из 90

<HostMatrix class="mt-1" stepwise />

<div class="grid grid-cols-[1.4fr_1fr] gap-5 mt-1 xsmall ink2">
<div><b class="ink">Колонка «запись» падала везде — и на main.</b> В рабочем дереве вместо записи лежал 130-байтовый указатель Git LFS, и игра честно отвечала «Recording file may be corrupted!!». Стенд стал читать запись из хранилища LFS с проверкой SHA-256 — и впервые 10 из 10.</div>
<div><b class="ink">Эталон один на всех</b> — замороженные прогоны AppKit-приложения. Расхождение на новой платформе записывается как расхождение, эталон не пересчитывают.</div>
</div>

<div class="source">tools/crossplatform/matrix.py · docs/evidence/crossplatform-matrix-20261005-nine-hosts.json (b9d4b62) · crossplatform-matrix-20261005-speed.json (870c24a, 7f15b7b) · crossplatform-playback-lfs-20261005.json · 16cb07b</div>

<!--
Сначала — базовая линия, снятая 4 октября в 23:20 на b9d4b62 и записанная в 2fe64be: у всех хостов 9 из 10, запись не проходит. По клику — прогон того же дня в 19:59, после работы над памятью и скоростью: 90 из 90. На Windows запись сперва разошлась из-за сравнения пути: имя файла в окне — Windows-путь, его разбирали как POSIX. Сравнение исправлено, сохранённые выходы пересравнены.
Кадры внутри группы растеризатора побайтно равны: 18 088 на пару. Между группами текст стоит в одних и тех же 9 565 кадрах — FreeType и GDI рисуют буквы по-своему, но там же, где CoreText.
-->

---

<Kicker>5 октября, 02:05 · ONLINE GAME между платформами</Kicker>

# Одна сетевая партия — четыре системы

<OnlineGraph class="mt-1" />

<div class="grid grid-cols-2 gap-5 mt-2 xsmall ink2">
<div><b class="ink">Протокол оригинала, без изменений.</b> TCP-порт 12345, таблица случайных чисел на 3 001 байт и 22 байта на тик. Каждая пара проходит сохранённую пробу сетевой игры с тем же хешем таблицы, что в её эталонном прогоне.</div>
<div><b class="ink">Одна загадка — артефакт стенда.</b> Mac-хост с Linux-клиентом молча ждали. strace показал: клиент сам занимает 127.0.0.1:12345, и внутри контейнера звонил сам себе. В сети клиент набирает адрес хоста — там этого не бывает.</div>
</div>

<div class="source">tools/crossplatform/pair_probe.py --cross · docs/evidence/crossplatform-online-cross-20261005.json · crossplatform-online-cross-linux-client-20261005.json · c9803c9 · 0a3707d · e509c32</div>

<!--
Все партии идут на одном Mac: Windows — в бутылке CrossOver с настоящим Winsock, Android — в эмуляторе через adb forward или reverse, Linux — в контейнере OrbStack, который мостит loopback Mac. Сеть между настоящими машинами и партия против оригинального EXE под Windows ещё не наблюдались.
-->

---

<Kicker>человек в цикле · 13 реплик за 30 часов</Kicker>

# Руки, которых у агента нет

<div class="grid grid-cols-[1.3fr_1fr] gap-6 mt-1">
<div>

<ChatLog agent="Claude" human="автор" :messages="[
  { who: 'human', time: '3 окт, 21:28', text: 'где что принять?' },
  { who: 'agent', time: '21:28', text: 'Двух кнопок «принять» нет: оба вопроса — просто ответ в чате, дальше всё делаю я.' },
  { who: 'event', time: '4 окт, 12:20', text: 'экран Mac заблокирован — AppKit-хосты стоят, шесть остальных идут' },
  { who: 'agent', time: '19:24', text: '<b>I’ve stopped the loop because everything left needs you.</b>', hot: true },
  { who: 'human', time: '19:45', text: 'разблокировал, запускай AppKit и macOS SDL и ставь антисон чтобы не пришлось разблокировать' },
  { who: 'human', time: '21:58', text: 'подключил кабелем, разблокировал' },
  { who: 'event', time: '22:04', text: 'sudo killall remoted — пароль вводит человек; шесть попыток установки на iPad не проходят' },
  { who: 'human', time: '22:12', text: 'can you host the app on simple http server so i can downlaod on lan on different mac', hot: true },
  { who: 'human', time: '5 окт, 07:51', text: 'i downloaded ipad ipa, taps on the keyboard worked.' },
]" />

</div>
<div>

<div class="hands">
<div class="hand"><span class="i-pixelarticons-file-alt" /><div><b>лицензии</b><p>Microsoft Build Tools для Windows-SDK, потом лицензии Android SDK</p></div></div>
<div class="hand"><span class="i-pixelarticons-lock-open" /><div><b>разблокировать Mac</b><p>окно AppKit не рисует в заблокированной сессии; дальше — «антисон»</p></div></div>
<div class="hand"><span class="i-pixelarticons-device-tablet" /><div><b>железо</b><p>iPad по кабелю, пароль для <code>sudo</code>, установка с другого Mac; 5 октября — телефон</p></div></div>
<div class="hand"><span class="i-pixelarticons-upload" /><div><b>всё, что уходит наружу</b><p>публикация pre-release и отчёт об ошибке в Swift — только с разрешения</p></div></div>
</div>

<div class="xsmall muted mt-2">Агент дал ссылку на IPA и временный HTTP-сервер в локальной сети, а после загрузки остановил его.</div>

</div>
</div>

<div class="source">журнал сессии 1f9218ae (реплики автора и ответы агента, время местное) · CROSS_PLATFORM.md L30–35 · docs/evidence/crossplatform-p8-ipad-device-20261005.json · 14e495e</div>

<style>
.hands { display: flex; flex-direction: column; gap: 0.5rem; }
.hand { display: grid; grid-template-columns: 1.6rem 1fr; gap: 0.5rem; align-items: start; background: var(--surface); border: 1px solid var(--hair); border-radius: 10px; padding: 0.45rem 0.6rem; }
.hand > span { width: 1.4rem; height: 1.4rem; color: var(--chakra); margin-top: 0.05rem; }
.hand b { font-size: 0.74rem; color: var(--ink); }
.hand p { margin: 0.1rem 0 0; font-size: 0.64rem; line-height: 1.35; color: var(--ink-2); }
</style>

<!--
Цитаты — дословно, с опечатками. Отчёт с iPad — наблюдение человека на настоящем устройстве (iPad Pro 11, M4): клавиатура работает. Он не инструментирован: ни журнала событий, ни кадров. Касания и звук на устройстве отдельно не проверялись.
-->

---

<Kicker>объявлено честно · 5 октября</Kicker>

# Стенд — не железо

<div class="grid grid-cols-3 gap-4 mt-3 small">
<div class="card">
<div class="pixel small" style="color: var(--s3)">проверено на стенде</div>

- Linux — в контейнерах OrbStack, x86_64 под Rosetta.
- Windows — в бутылке CrossOver с настоящим Winsock.
- iPad — в симуляторе, Android — в эмуляторе Android 15.
- Онлайн — на одном Mac: loopback, adb forward, мост OrbStack.

</div>
<div class="card">
<div class="pixel small" style="color: var(--s1)">на настоящем устройстве</div>

- Mac — выпущенное приложение и эталон для всех.
- iPad Pro — «taps on the keyboard worked»: отчёт человека, без замеров.
- Galaxy A12 — сценарий VS с точным эталонным состоянием, но сначала игру убил Android: ей нужно 4 ГБ.

</div>
<div class="card">
<div class="pixel small" style="color: var(--s4)">не наблюдалось</div>

- Настоящий Linux-десктоп и Windows-ПК. Pre-release так и подписан: «tested only in containers and Wine».
- Партия против оригинального EXE под Windows.
- 10 тяжёлых наборов тестов не помещаются в память контейнера.

</div>
</div>

<div class="card-soft mt-4 small ink2 flex items-center gap-4">
<span class="pixel" style="font-size: 1.4rem; color: var(--s1); white-space: nowrap">4 ГБ</span>
<span>Первое же настоящее устройство нашло то, чего не видел ни один стенд: на Mac лишние гигабайты незаметны, а на телефоне с 2,8 ГБ игра не доживает до меню. Об этом — следующая глава.</span>
</div>

<div class="source">CROSS_PLATFORM.md: таблица тулчейнов, журнал статуса · crossplatform-p7-release-20261004.json · crossplatform-p8-ipad-device-20261005.json · crossplatform-p8-android-phone-20261005.json · crossplatform-p3-x86_64-20261005.json</div>

<!--
Pre-release crossplatform-preview-20261004 — Linux aarch64, Linux x86_64 и Windows x86_64, по 217 МБ. На 7 октября у каждого архива по одному скачиванию. Самой свежей (Latest) осталась macOS-версия v0.4.0.
-->
