---
layout: chapter
num: 19
total: 20
kicker: Глава девятнадцатая
dates: 16 — 19 октября · main
image: /img/covers/ch19-deck.svg
imagePixel: false
stats: 31 коммит в main · Steam Deck из Game Mode · 46,5 → 4,6 с в браузере · кнопки от игрока из Discord · релиз 0.6.0
---

# Игра у игроков

Через три дня после заморозки деки автор берёт в руки Steam Deck, открывает живой сайт и пересылает код из Discord. Каждая жалоба становится веткой агента, а через три дня выходит второй релиз на шесть платформ.

<div class="cover-note">Обложка — рисунок: условная портативная консоль с титульным экраном игры. Кадр — из обложки, которую агент нарезал для библиотеки Steam; это не фото устройства.</div>

<style>
.cover-note { margin-top: 0.7rem; font-size: 0.66rem; color: var(--muted); }
</style>

<!--
Глава — о том, что попало в main после заморозки деки: 31 коммит от 16 октября, 20:27 (94581233) до 19 октября (d7330e96, тег native-preview-20261019). Все цифры — с origin/main на d7330e96. Время — UTC+2, как у автора; три коммита сенсорного управления записаны на втором Mac с поясом +03:00 — здесь они переведены в UTC+2.

Что сюда не вошло: работа в ветках, которые в main не слиты. Глава — только о main.

Четыре истории: Steam Deck и геймпад в меню (16 октября), загрузка в браузере пачками (17 октября), сенсорные кнопки от игрока из Discord (19 октября) и второй релиз. И один взгляд вперёд — оценка следующей версии игры, NTSD 2.8.3.3.
-->

---

<Kicker>16 октября, 19:31 — 20:27 · Steam Deck</Kicker>

# Из Game Mode, как любая игра Steam

<div class="grid grid-cols-[0.92fr_1.2fr] gap-6 mt-1">
<div>

<PhoneChat :messages="[
  { who: 'human', time: '19:31', text: 'хочу собрать игру на steam deck. что для этого нужно? он подключен по проводу', hot: true },
  { who: 'human', time: '19:47', text: 'он ушел в автоапдейт' },
  { who: 'human', time: '20:13', text: 'I want the game to be launchable from steam deck interface, not from desktop mode', gloss: 'запуск из интерфейса Steam, а не с рабочего стола' },
  { who: 'human', time: '20:21', text: 'добавь в репу инструкцию по установке на steam deck и скрипты' },
  { who: 'event', time: '20:27', text: '<code>94581233</code> · docs/STEAM_DECK.md, установщик, ярлык Steam' },
]" />

</div>
<div>

<div class="lib">
<img src="/img/deck/hero.png" alt="Обложка NTSD 2.4 для библиотеки Steam">
</div>
<div class="libcap"><b>NTSD 2.4</b> в библиотеке Steam · обложки агент вырезал через <code>sips</code> из снимка титульного экрана на самом Deck</div>

<div class="flow">
<span>Mac</span><i>→ ssh →</i><span><code>steamdeck_install.py</code>: 208 МиБ, 9,5 с</span><i>→</i><span><code>shortcuts.vdf</code> байт в байт как пишет Steam</span><i>→</i><span>Game Mode: gamescope, X11, PipeWire</span>
</div>

<div class="grid grid-cols-3 gap-2 mt-2">
<StatTile value="0 строк" label="собрано на Deck" sub="Linux x86_64 пакет как есть" size="sm" accent="var(--s1)" />
<StatTile value="glibc 2.41" label="SteamOS 3.8.28" sub="пакету нужна 2.39+" size="sm" accent="var(--s1)" />
<StatTile value="12 000" label="циклов матча в Game Mode" sub="и игра всё ещё шла" size="sm" accent="var(--s2)" />
</div>

<div class="usb xsmall ink2"><b class="ink">«подключен по проводу»</b> — не поможет: USB-C между Deck и Mac их не соединяет, оба — USB-хосты. Пакет идёт по Wi-Fi через SSH.</div>

</div>
</div>

<div class="source">docs/STEAM_DECK.md (What you need, Checked 2026-10-16, Library art) · 94581233 · tools/crossplatform/steamdeck_install.py, steamdeck/add_shortcut.py · сессия Claude Code cc2986ef (только время и реплики автора, UTC+2)</div>

<style>
.lib { position: relative; border: 1px solid var(--hair); border-radius: 12px; overflow: hidden; line-height: 0; }
.lib img { width: 100%; height: 124px; object-fit: cover; object-position: center 22%; display: block; }
.libcap { line-height: 1.35; margin-top: .3rem; font-size: .6rem; color: var(--ink-2); }
.libcap b { color: var(--ink); font-family: var(--font-display); }
.libcap code { font-size: .56rem !important; }
.flow { display: flex; flex-wrap: wrap; align-items: center; gap: .25rem .3rem; margin-top: .5rem; font-size: .62rem; color: var(--ink-2); background: rgba(255,255,255,.03); border: 1px dashed var(--axis); border-radius: 10px; padding: .35rem .5rem; line-height: 1.3; }
.flow span { background: var(--surface-2); border-radius: 6px; padding: .05rem .4rem; }
.flow i { font-style: normal; color: var(--naruto); }
.flow code { font-size: .56rem !important; }
.usb { margin-top: .5rem; line-height: 1.4; }
</style>

<!--
Реплики — дословно из журнала сессии Claude Code cc2986ef, время местное (UTC+2). Между ними — «чет steam deck не включается», «включается...», «найди девайс в сети»: Deck сначала ушёл в автообновление SteamOS.

Как это устроено. SteamOS — x86_64 Linux, поэтому Deck запускает тот же пакет SDL, что и релиз 13 октября; на самом Deck ничего не собирается. Mac загружает пакет по SSH, распаковывает его и добавляет игру в библиотеку Steam как «не-Steam игру». Steam переписывает свой список таких игр при выходе, поэтому установщик закрывает Steam, пишет shortcuts.vdf и возвращает Deck в Game Mode. Читатель и писатель shortcuts.vdf воспроизводят файл, записанный самим Steam, байт в байт; id ярлыка — собственное правило Steam: crc32(exe + name) | 0x80000000, сверено с ярлыком, который сделал Steam.

Что проверено 16 октября: Desktop Mode — Wayland и PipeWire, автор сыграл матч VS. Game Mode — ярлык запущен через steam-launch-wrapper и reaper, игра выбрала X11 под gamescope, открыла виртуальный геймпад Steam («Microsoft X-Box 360 pad 0»), снимок gamescope показал титул на весь экран; автор начал матч, и через 12 000 циклов он всё ещё шёл. Обновление пакета из main 94581233 в Game Mode — 9,5 с: 208 МиБ загружено, все библиотеки найдены, ярлык и обложки уже на месте.

Не проверено: оверлей Steam, сон и пробуждение, чем автор управлял на титуле — сенсорным экраном или трекпадом.

Обложка на слайде — hero.png 1920×620 из tools/crossplatform/steamdeck/art: агент вырезал её через sips из снимка титульного экрана в Desktop Mode.
-->

---

<Kicker>16 октября, 20:21 — 22:18 · MENU_GAMEPAD</Kicker>

# Мышь, которой у Deck нет

<p class="lead">Титул, CONTROL SETTINGS, ONLINE GAME и RECORDING INFO оригинал читает <b>только мышью</b>. Автор: <span class="q">«да понимаю что это отхождение от оригинала»</span>. Порт ведёт мышь игры к ближайшей цели, A — щелчок; флаг <code>--original-menu-input</code> возвращает оригинал.</p>

<PsMenuPad>
<div class="mg">
<div class="card-soft"><b>21:41 «good. push to master»</b> — и через минуту стоп: <span class="q">«buttons in control settings and online game are not working»</span>. Титул заработал, остальные экраны — нет.</div>
<div class="card-soft"><b>Ревью нашло:</b> после Back на ONLINE GAME курсор оставался на OFFICAL WEBSITE, и следующее A открывало браузер.</div>
<div class="card-soft"><b>Текст:</b> пока поле ждёт имя или адрес, сама открывается экранная клавиатура Steam — <code>steam://open/keyboard</code>.</div>
</div>
</PsMenuPad>

<div class="source">docs/research/MENU_GAMEPAD.md (The original, The departure, Review of the general version, Text on the Steam Deck) · 52042b56 · 8075e582 · 9976246d · 14456457 · e334323b · снимок: public/img/screens/17-gdi-text-controls.png</div>

<style>
.lead { margin: -0.5rem 0 0.45rem !important; font-size: 0.74rem; line-height: 1.4; color: var(--ink-2); }
.lead b { color: var(--ink); }
.lead .q, .mg .q { color: var(--ink); }
.lead code { font-size: .64rem !important; }
.mg { display: flex; flex-direction: column; gap: 5px; }
.mg .card-soft { font-size: .58rem; line-height: 1.34; color: var(--ink-2); padding: .3rem .55rem; }
.mg b { color: var(--ink); }
.mg code { font-size: .54rem !important; }
</style>

<!--
Нажимайте крестовину и A справа: курсор ходит по тем же целям, что и в порте. Контуры — 30 целей CONTROL SETTINGS при раскладке по умолчанию (игроки 1 и 2 — клавиатура, 3 и 4 — джойстики): поле имени, коробка устройства и клетки клавиш каждого игрока, OK и Cancel. При открытии слайда проигрывается маршрут из проверки e2e: первое A только показывает старт (коробку устройства игрока 1), второе переключает клавиатуру на джойстик 1 — четыре строки направлений у джойстика назначить нельзя, они пропадают, целей становится 26, — четыре раза вниз до OK, и A записывает control.txt, где у игрока 1 устройство 0 → 1.

Правило шага — из карточки: среди целей в эту сторону ближайшая в той же строке или колонке, иначе в пределах 45°, иначе хотя бы на 16 пикселей в эту сторону; мера — расстояние вдоль плюс удвоенное поперёк; если нет ничего — по кругу к самой дальней с другой стороны. Последний шаг вниз с клетки defend на OK идёт по третьему ярусу: OK не в той же колонке и не в пределах 45°.

Почему это отступление. В оригинале эти экраны слушают только мышь: WM_MOUSEMOVE и левую кнопку. Ни клавиш игроков, ни байтов джойстика там не читают — геймпад оригинала на них ничего не делает. На Deck выручал сенсорный экран или трекпад, на Apple TV не выручало ничего. Автор попросил явно и сам назвал это отступлением. Порт делает его одним модулем OriginalRuntimeMenuGamepad для всех хостов сразу, а без ввода с джойстика на этих экранах ничего не меняется; флаг --original-menu-input убирает отступление целиком.

История вечера. Сначала заработал только титул (52042b56), автор ответил «good. push to master» и через минуту остановил пуш: CONTROL SETTINGS и ONLINE GAME по-прежнему не слушались. Коммит 965cbd8b успел записать слияние в main, которого не было, — карточка потом это исправила. Общая версия (8075e582) прошла ревью с двумя находками средней важности: курсор, оставленный на чужом экране, и экран адреса, который стартовал на OK (OK без адреса пытается соединиться). Автор попросил не гонять полный e2e ради изменения только меню: «не нужно полный e2e для изменения исключительно меню».

Клавиатура Steam: хост SDL раз в 200 мс спрашивает у ядра, ждёт ли поле текст, и включает текстовый ввод SDL — в Game Mode SDL 3.4.16 превращает это в steam://open/keyboard и steam://close/keyboard. Проверено в контейнере под Xvfb с переменной Steam; на самом Deck клавиатуру руками ещё не проверяли.
-->

---

<Kicker>17 октября, 13:50 — 16:21 · TVOS_WEB W5</Kicker>

# 1 521 запрос — и неважно, какой интернет

<div class="ask">
<span class="who pixel">автор · 13:50</span>
<span class="txt">«https://ntsd-web-ashy.vercel.app check out our web version. ita loading times are kinda bad. super bad. no matter the internet speed. we must heavily optimize it. we launch the game in 5s on samsung a12 and web is so slow that nobody is playing»</span>
</div>

<PsWebPacks class="mt-2" />

<div class="why xsmall ink2"><b class="ink">Почему глава 17 этого не видела:</b> стенд ограничивал полосу, но отвечал мгновенно. У CDN каждый из 1 521 файлов ждёт 0,2–0,35 с до первого байта — загрузка упиралась в задержку, а не в скорость линии. Снова «стенд — не железо».</div>

<div class="source">docs/evidence/tw-w5-web-packed-loading-20261017.json (request, liveSiteBefore, compression, build, visits, published) · docs/research/TVOS_WEB.md (W5) · 1deaa396 · 72fe9a48 · ab4e65b4 · сессия Claude Code 9d2efd96 (время реплики, UTC+2)</div>

<style>
.ask { display: grid; grid-template-columns: auto 1fr; gap: .6rem; align-items: baseline; margin-top: -.4rem; background: rgba(57,135,229,.08); border: 1px solid rgba(57,135,229,.35); border-radius: 12px; padding: .35rem .7rem; }
.ask .who { font-size: .64rem; color: var(--chakra); white-space: nowrap; }
.ask .txt { font-size: .64rem; line-height: 1.38; color: var(--ink); }
.why { margin-top: .45rem; line-height: 1.4; }
</style>

<!--
Реплика — дословно, с опечаткой «ita», из журнала сессии Claude Code 9d2efd96; время местное.

Сверху — гонка в десять раз быстрее жизни. Слева — 1 521 квадрат: столько файлов программа читает за запуск (read-order.json), и до W5 каждый был отдельным запросом к CDN. Справа — 12 пачек: первая — 48 файлов старта (2,4 МБ по сети), остальные — по 64 МиБ и больше, в порядке чтения программы. Часы — холодный визит на живой сайт: все данные на месте за 46,45 с до и за 4,61 с после.

Снизу — медианы замеров карточки: оранжевая точка — было, синяя — стало. «Живой сайт» — Vercel, Chromium на этом Mac: до W5 — развёртывание 13 октября; после — второй и третий холодные визиты 17 октября (первый попал на край CDN, где новых файлов ещё не было: 5,3 с и 15,3 с). «Стенд» — локальный сервер web_app.py, который держит каждый ответ 100 мс, как CDN, — то, чего не было в замерах W3b–W3f главы 17; три прогона на точку, по два при 20 Мбит/с. Повторный визит после W5 не качает ничего: данные готовы за 0,4 с, ещё до щелчка.

Что сделали. Данные — 12 пачек brotli 11 в порядке чтения: 757,7 МБ → 43,8 МБ по сети. Программа — без отладочных секций: 96 → 63,7 МБ, по сети 14,1 МБ вместо 29,3 МБ, которые Vercel сжимал на лету. Воркер-загрузчик кладёт пачки в OPFS — приватное хранилище браузера — и отдаёт игре синхронные чтения; модуль компилируется ещё до щелчка START; музыка, которая не успела прийти, идёт молча по часам и вступает, когда доедет. Все 11 сценариев через новый путь в Chromium и WebKit — кадры идентичны HEAD: 18 384 из 18 384. Два раунда ревью: первый нашёл, что имя папки данных не покрывало раскладку пачек, и переупорядоченная пачка могла взять старые байты из кэша.

Опубликовала сайт сессия Codex автора; заголовки на продакшене Claude проверил curl: пачки и модуль приходят с content-encoding: br.
-->

---

<Kicker>18 — 19 октября · TOUCH_CONTROLS</Kicker>

# Кнопки из Discord

<div class="grid grid-cols-[0.82fr_1.3fr] gap-5 mt-1">
<div>

<PhoneChat agent="StormPixels · Discord" :messages="[
  { who: 'agent', time: '18 окт', text: 'use it however you like … No credit needed', gloss: 'архив 12,71 КБ: модуль Swift для Android, патч хоста, README; видео с телефона на Android 9' },
  { who: 'human', time: '19 окт', text: 'думаю имеет смысл on screen контролы показывать на айфонах тоже, если не подключена клава/геймпад', hot: true },
  { who: 'human', time: '19 окт', text: 'и на айпаде тоже если клавиатуры/геймпада нет' },
  { who: 'human', time: '19 окт', text: 'не слишком большие контролы для айпада? … пальцам будет неудобно' },
  { who: 'event', time: '19 окт, 14:11', text: '<code>96d78b63</code> · слито в main' },
]" />

<div class="card-soft mt-2 tw">Это <b>объявленное дополнение хоста</b>: у оригинала всегда была клавиатура. Кнопки жмут те же клавиши, что и клавиатура, — ядро, сессия и кадр игры не меняются. Пока подключены клавиатура или геймпад, кнопок нет.</div>

</div>
<div>

<PsTouch />

</div>
</div>

<div class="source">docs/research/TOUCH_CONTROLS.md (The proposal, Changed in integration 1–8, Ledger) · docs/evidence/touch-controls-t0-t2-20261019.json · data/control.txt оригинала · 743f0558 · 96d78b63 · 86feac76 (записаны на втором Mac, UTC+3)</div>

<style>
.tw { font-size: .62rem; line-height: 1.4; color: var(--ink-2); }
.tw b { color: var(--ink); }
</style>

<!--
Слева — реплики из карточки TOUCH_CONTROLS, дословно; сессия шла на втором Mac, его журнала здесь нет, поэтому время — только дата. StormPixels — игрок из Discord сообщества; предложение пришло 18 октября в личные сообщения: «use it however you like … No credit needed». Агент прочитал архив целиком до использования: ни сети, ни файлов, ни процессов, кроме своего files/controls.txt.

Справа — схема, не снимок: места кнопок нарисованы по описанию карточки. При открытии слайда сначала видны клавиши предложения, через пару секунд — порта; можно переключать руками.

Главная находка встраивания — клавиши. Предложение жало стрелки, A, J и D. Но в data/control.txt оригинала первая строка — игрок 1: W, S, A, D и J атака, K прыжок, L защита; стрелки — игрок 2. С клавишами предложения крестовина водила игрока 2, «атака» (A) была шагом игрока 1 влево, «прыжок» (J) — его атакой, а «защита» (D) — шагом вправо. Нашлось в симуляторе: меню режимов не реагировало на кнопку «A». Теперь кнопки подписаны ролью (A, J, D — как в списках приёмов: D>A), а клавишу показывают настройки.

Остальные изменения:
1. Общий модуль OriginalTouchControls в NTSDRuntime для Android и iOS; в хостах — только связка с платформой.
2. Прячутся, пока подключены клавиатура или геймпад — правило автора. Android спрашивает InputDevice через JNI, iOS — GameController.
3. Рисуются не в игровом потоке: предложение перерисовывало весь кадр на главном потоке при каждом нажатии. Теперь картинка неизменяемая; на Android её растеризует поток презентера и смешивает только тайлы 32×32, где есть пиксели.
4. Клавиши игрока 1 оригинала — см. выше.
5. ESC — в сетке F1–F9: на iOS нет кнопки «Назад».
6. На iPhone — безопасная зона: ни одна кнопка не заходит под Dynamic Island (автор увидел это на левой кнопке).
7. Размер — по физическому экрану: у предложения единица была девятой частью высоты экрана в любых единицах, и кнопка на 13-дюймовом iPad выходила ≈ 37 мм. Единица ограничена 48 pt/dp: ≈ 13 мм на телефоне и ≈ 16 мм на iPad. Места — фиксированные расстояния от нижних углов.
8. Мелочи: несколько пальцев, перетаскивание кнопки без прыжка под палец, сохранение показа и скрытия.

Проверки: инструмент touch_controls_check.swift — ALL PASS, баланс 0 из 3 000 случайных перемешиваний; vs равен эталону в симуляторах iPhone и iPad и в эмуляторе Android; матч VS сыгран касаниями в симуляторе iPhone. Два независимых ревью: 13 находок, потом 6 мелких. Открыто: Galaxy A12 и настоящие iPhone/iPad, несколько пальцев на устройстве.

Время коммитов — с поясом +03:00, второй Mac; в UTC+2 это 14:06–14:11. Автор в git там — «Misha Kh», а не «Michael»: тот же человек, другая машина.
-->

---

<Kicker>19 октября, 15:11 · native-preview-20261019 · Latest</Kicker>

# Второй релиз — и что в него не попало

<div class="grid grid-cols-[1fr_1.12fr] gap-6 mt-1">
<div>

<div class="rel">
<div class="rh"><span class="pixel hl">0.6.0</span><span class="tag">13 файлов · 1,30 ГБ · шесть платформ</span></div>
<div class="ri"><b>Сенсорные кнопки</b> — только в APK: сборки iPhone и iPad не раздаются</div>
<div class="ri"><b>Геймпад во всех экранах меню</b> и клавиатура Steam на Deck</div>
<div class="ri"><b>macOS:</b> окно оригинального размера сообщает игре о переносе — WM_MOVE, как на Windows</div>
<div class="ri"><b>Web:</b> 12 пачек brotli в OPFS — повторный визит ничего не качает</div>
<div class="rf">macOS — Developer ID, нотаризация, staple; Android — прежний ключ. <span class="muted">Не проверено: APK на телефоне, кнопки на устройствах, настоящий Windows; веб-пакет не развёрнут.</span></div>
</div>

<div class="tight two mt-2">

| | 13 октября | 19 октября |
| --- | --- | --- |
| собран из | `exp/iphone`, не main | **main**, `d7330e96` |
| macOS | 0.5.0, build 5 | **0.6.0, build 6** |
| веб-пакет | 354,8 МБ | **174,7 МБ** — пачки |
| всего | 1,48 ГБ | **1,30 ГБ** |
| выпустил | Codex, без трейлера | **Claude**, трейлер в `d7330e96` |

</div>

</div>
<div>

<div class="fate-h">шесть коммитов <code>exp/iphone</code> из главы 18 — где они теперь</div>
<div class="fate">
<div class="fr ok"><code>f340f1e2</code><span>C1 · сборка для iPhone</span><em>cherry-pick <code>39238e3d</code>, 19 окт</em></div>
<div class="fr ok"><code>2c4db98b</code><span>инструменты релиза 13 окт</span><em>перенесены в <code>d7330e96</code></em></div>
<div class="fr ok"><code>9c700dae</code><span>проверки пакетов Linux и Windows</span><em>перенесены в <code>d7330e96</code></em></div>
<div class="fr side"><code>0b5d4621</code><span>запись о релизе 13 окт</span><em>только в release/native-preview-20261013</em></div>
<div class="fr no"><code>d4619cbc</code><span>C2 · Kishi V2 на Pixel 10</span><em>нет в main</em></div>
<div class="fr no"><code>5f5a8ee4</code><span>C3 · один джойстик на контроллер</span><em>нет в main — и нет в 0.6.0</em></div>
</div>
<div class="c3 xsmall ink2">В main и в APK 0.6.0 хост Android по-прежнему берёт <b class="ink">первые два</b> устройства с SOURCE_GAMEPAD: немой интерфейс 2 у Kishi V2 снова займёт джойстик 2.</div>

</div>
</div>

<div class="source">gh release view (13 и 19 окт) · data/rel_release.json · сессия fa971abb (время) · тег → d7330e96 · git cherry origin/main 5f5a8ee4 · NTSDAndroidGamepads.swift на origin/main · dea77af0</div>

<style>
.rel { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: .55rem .8rem .6rem; }
.rh { display: flex; align-items: baseline; justify-content: space-between; gap: .5rem; margin-bottom: .35rem; }
.rh .pixel { font-size: 1.9rem; line-height: 1; }
.ri { font-size: .66rem; line-height: 1.38; color: var(--ink-2); padding: .26rem 0 .26rem .9rem; position: relative; border-top: 1px dashed var(--grid); }
.ri::before { content: ''; position: absolute; left: 0; top: .62rem; width: 6px; height: 6px; background: var(--naruto); }
.ri b { color: var(--ink); }
.rf { font-size: .6rem; line-height: 1.38; color: var(--ink-2); margin-top: .35rem; padding-top: .4rem; border-top: 1px solid var(--axis); }
.fate-h { font-size: .64rem; color: var(--muted); margin-bottom: .3rem; }
.fate-h code { font-size: .56rem !important; }
.fate { display: flex; flex-direction: column; gap: .28rem; }
.fr { display: grid; grid-template-columns: 4.6rem 1fr auto; gap: .5rem; align-items: center; background: var(--surface); border: 1px solid var(--hair); border-left-width: 3px; border-radius: 8px; padding: .22rem .55rem; font-size: .62rem; color: var(--ink-2); }
.fr code { font-size: .56rem !important; }
.fr em { font-style: normal; font-size: .58rem; color: var(--ink); text-align: right; }
.fr.ok { border-left-color: var(--good); }
.fr.side { border-left-color: var(--axis); }
.fr.side em { color: var(--muted); }
.fr.no { border-left-color: var(--critical); }
.fr.no em { color: var(--serious); }
.c3 { margin-top: .5rem; line-height: 1.4; }
.two td, .two th { padding: .18rem .45rem !important; font-size: .64rem; }
.two code { font-size: .56rem !important; }
</style>

<!--
Релиз 19 октября — «NTSD Native — platform release (2026-10-19)», метка Latest, опубликован в 15:11 по UTC+2. Тег native-preview-20261019 стоит на d7330e96 — это main; в отличие от 13 октября, все шесть сборок собраны из одного коммита main (native-дерево f56cc891). 13 файлов: DMG macOS 0.6.0 (build 6) и его SHA-256, APK для Android ARM64, ZIP для Windows x86-64, два tar.gz для Linux, ZIP веб-версии, манифесты к каждому и общий SHA256SUMS.txt — 1,30 ГБ.

Проверки из текста релиза: приложение macOS — все 11 сценариев, vs — ещё и из подписанного приложения в смонтированном DMG; оба пакета Linux — в чистых контейнерах Ubuntu 24.04; Windows — запуск и vs в изолированной бутылке CrossOver; веб — verify и vs через пачки в Chromium и WebKit; Android — подпись, список ассетов и содержимое. Не проверено: APK не запускали ни на телефоне, ни в эмуляторе, кнопки — не на устройствах, Windows — не настоящий, веб-пакет не развёрнут. iOS и iPadOS исключены: в main есть только сборка с подписью разработчика.

WM_MOVE: автор прислал снимок — после переноса окна на macOS картинка оставалась на старом месте, сдвинутая на величину переноса, с чёрным справа и снизу. Окно оригинального размера обрезает экранную поверхность по клиентской области, а игра рисует туда, куда запомнил её обработчик WM_MOVE, — а хост присылал WM_MOVE один раз, при старте. Теперь присылает при каждом переносе (dea77af0).

Кто выпустил. 13 октября релиз сделала сессия Codex, без трейлера в коммитах (глава 18). 19 октября коммит версии d7330e96 несёт трейлер Claude, а публикация в 15:11 лежит внутри сессии Claude Code fa971abb на этом Mac (метаданные, только время). Веб-пакет вдвое меньше — 354,8 → 174,7 МБ: те же данные, но пачками brotli.

Справа — судьба шести коммитов ветки exp/iphone, на которой заморожена глава 18. Сборку для iPhone перенесли в main cherry-pick'ом 19 октября; инструменты релиза 13 октября — коммит версии 0.6.0 прямо говорит, что несёт их изменения, «which never reached main». Запись о релизе 13 октября осталась на ветке релиза. А C2 и C3 — запись о Kishi V2 на телефоне и правка, которая не отдаёт немому HID-интерфейсу контроллера слот второго джойстика, — в main не попали. Проверено по коду: NTSDAndroidGamepads.swift на origin/main берёт первые два устройства с SOURCE_GAMEPAD без пропуска. Значит, в 0.6.0 с Kishi V2 второй игрок с настоящим геймпадом слота не получит — это тот же вывод из кода, что и в главе 18, не опыт.
-->

---

<Kicker>17 октября · следующая версия · без запуска оригинального кода</Kicker>

# На столе — NTSD 2.8.3.3

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-1">
<div class="tight">

| | 2.4 | 2.8.3.3 |
| --- | ---: | ---: |
| файлов в дистрибутиве / во внешнем ZIP | 1 595 | 112 |
| объектов в реестре `data.txt` | 137 | **330** |
| из них лежат отдельными файлами | 137 | **7** |
| фонов в реестре / отдельными файлами | 17 / 17 | 24 / **0** |
| главный EXE | 31,7 МБ | **87,3 МБ** |
| кадров на объект | 0…399 | до 998 по справке |

<div class="xsmall ink2 mt-2" style="line-height: 1.4">323 объекта и все 24 фона в ZIP не лежат: EXE втрое больше и, видимо, несёт их в себе — как именно, не восстановлено. Общих путей у двух дистрибутивов два: <code>data/control.txt</code> и <code>data/data.txt</code>, и оба изменены. Наруто был <code>chars/naruto.dat</code>, стал <code>c/nar/nar.dat</code>.</div>

</div>
<div>

<div class="grid grid-cols-2 gap-2">
<StatTile value="200–520 ч" label="вся версия поверх движка" sub="≈ 25–65 рабочих дней" size="sm" accent="var(--s2)" />
<StatTile value="40–100 ч" label="первый сверенный матч Наруто — Саске" sub="после доступа к читаемому контенту" size="sm" accent="var(--s1)" />
</div>

<div class="card-soft mt-2 cx"><b>Вывод карточки:</b> <span class="q">«feasible, but a substantial version port»</span> — новые загрузчики, хранилище и правила боя; подмена ассетов отвергла бы настоящие файлы и молча потеряла бы новые поля.</div>

<div class="card-soft mt-2 cx"><b>В тот же вечер</b> — оригинал 2.4 под лицензионным CrossOver 25.1.1: через Cua Driver агент закрыл ошибку музыки <span class="q">«Could not create a filter graph for this file!»</span>, нажал START и дошёл до меню режимов.</div>

<div class="grid grid-cols-2 gap-2 mt-2">
<StatTile value="28 из 31" label="коммитов с трейлером Claude" sub="16–19 октября, main" size="sm" accent="var(--s2)" />
<StatTile value="3" label="коммита сессий Codex" sub="модель gpt-6.1-sol — новая" size="sm" accent="var(--s3)" />
</div>

</div>
</div>

<div class="source">docs/research/NTSD_2_8_3_3_ASSESSMENT.md (Measured differences, Preliminary effort estimate) · ntsd-2.4-to-2.8.3.3-static-20261017-run1/validation1.json · 2c5cb633 · CROSSOVER_REFERENCE_LAUNCH.md · crossover-25.1.1-smoke(-ui)-20261017.json · ec86e1f2 · c046f780 · ~/.codex/sessions/2026/10/17 (session_meta, turn_context)</div>

<style>
.cx { font-size: .62rem; line-height: 1.4; color: var(--ink-2); }
.cx b, .cx .q { color: var(--ink); }
</style>

<!--
Автор принёс архив следующей версии игры, NTSD 2.8.3.3, и попросил оценить, что в ней поменялось и сколько работы будет поверх нашего движка. Это ограниченный статический анализ: оригинальные EXE, установщики и DLL не запускали, не патчили и не распаковывали исполнением. Разбор PE на импорте упал — «RVA outside file-backed sections», — и это записано как граница парсера, а не подменено поиском строк.

Таблица — из карточки. Объекты типа 0 — это не число выбираемых персонажей: туда входят превращения, клоны и вспомогательные объекты. 323 объекта и 24 фона, которых нет во внешнем ZIP, нельзя считать удалёнными: EXE вырос с 31,7 до 87,3 МБ, и, похоже, контент вшит в него; способ упаковки не восстановлен. Справка движка описывает до 998 кадров, до 20 opoint и 100 itr в кадре; в настоящих файлах Генмы — кадры до 701. Наш загрузчик держит 0…399 и 400 записей по 0x178 байт — это работа по версии, а не замена числа.

Оценка — допущения для планирования одним владельцем с существующими инструментами, а не замер: 8–24 часа на получение читаемого контента и инвентаризацию, 24–64 — загрузчики и ресурсы, 64–160 — ввод, бой, порождения и AI со сверкой, 40–96 — меню, HUD, режимы, 24–64 — повторы и сеть, 40–112 — интеграция и приёмка. Итого 200–520 часов, ≈ 25–65 рабочих дней. Первый сверенный матч — 40–100 часов после доступа к контенту, внутри общей оценки.

CrossOver: лицензия автора не покрывала обновления после 2 декабря 2025 года, поэтому 26.3 сохранили и поставили подписанный 25.1.1. Все 1 595 файлов чистого дистрибутива совпали с манифестом. Сначала Cua не увидел окно Wine; после явного разрешения автора драйвер нашёл окно, ошибка музыки закрыта кнопкой OK, START удержан 400 мс — игра загрузилась до меню режимов. Короткие нажатия S и стрелки выбор не сдвинули; звук эффектов и матч не проверялись. Это свидетельство Wine и Rosetta, не настоящей Windows.

Кто. Из 31 коммита в main 28 несут трейлер Claude. Три — оценка 2.8.3.3 и две записи CrossOver — без трейлера; их время лежит внутри сессий Codex CLI на ветке main, модель — gpt-6.1-sol: в главе 11 работал GPT-6 Astra. Метаданные сессий, текст не читался.
-->
