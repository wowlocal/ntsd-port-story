---
layout: chapter
num: 9
total: 13
kicker: Кунсткамера
dates: что нашлось внутри EXE
image: /img/screens/05-f8-full-pool-chaos.png
stats: баги оригинала, которые порт обязан повторить
---

# Кунсткамера

Порт не исправляет оригинал. Он воспроизводит его — вместе со странностями, опечатками и чтением за краем памяти.

---

<Kicker>данные и загрузка</Kicker>

# Как NTSD читает свои файлы

<QuirkDatPath class="mt-1" label="путь каждого DAT" :steps="[
  { t: '*.dat', s: 'зашифрован' },
  { t: '4148a0', s: 'минус байт ключа' },
  { t: 'data\\temporary.txt', s: 'открытый текст' },
  { t: 'fscanf: %s, %d', s: 'разбор по токенам', accent: true },
  { t: 'Do not erase this file.', s: 'этой строкой файл затирается' },
]" />

<div class="roomy">
<IconCards class="mt-3" :cols="4" :items="[
  { icon: 'i-pixelarticons-key', title: 'Ключ шифрования DAT', text: 'Из байта файла вычитается байт ключа <code>SiuHungIsAGoodBear<wbr>BecauseHeIsVeryGood</code>', tag: '0x44892c · 0x4148a0' },
  { icon: 'i-pixelarticons-eraser', title: '«Do not erase this file.»', text: 'После разбора временный <code>data\\temporary.txt</code> затирается этой строкой', tag: '0x412277' },
  { icon: 'i-pixelarticons-volume-2', title: 'Имя кадра течёт в звук', text: 'Имя через <code>%s</code> без предела в 20 байт даёт «указатели звука» <code>ast</code>, <code>down</code>, <code>plod</code> — 38 кадров в 7 файлах', tag: '0f5ceeb' },
  { icon: 'i-pixelarticons-archive', title: 'Кэш звуков на 20 байт', text: 'Путь <code>data\\SNDDATA_1869.wav</code> с NUL — 21 байт: запись затирает хвост предыдущей', tag: '0x455638' },
  { icon: 'i-pixelarticons-binary', title: '−6 846 518 779', text: '<code>%d</code> VC80 считает по модулю 2³²: из <code>kyubi.dat</code> выходит 1 743 415 813', tag: 'fab8104' },
  { icon: 'i-pixelarticons-zap', title: 'Шестой хитбокс', text: '<code>itr</code> — <code>malloc(400)</code> на 5 записей: шестой переполнил бы кучу, порт отклоняет DAT', tag: 'malloc(400)' },
  { icon: 'i-pixelarticons-add-box', title: 'Повторный кадр дописывает', text: 'Второй <code>\u0026lt;frame\u0026gt;</code> с тем же номером дополняет запись: 318 определений → 317 кадров', tag: 'Naruto, кадр 123' },
  { icon: 'i-pixelarticons-memory-stick', title: 'Каталог одним куском', text: 'Один <code>malloc</code> на 81 273 768 байт; из 1 056 байт Actor конструктор пишет 913', tag: '0x4d823a8' },
]" />
</div>

<style>
.roomy :deep(.ic) { padding: 0.8rem 0.9rem 0.85rem; }
.roomy :deep(.ico) { width: 1.6rem; height: 1.6rem; }
.roomy :deep(.head b) { font-size: 0.8rem; }
.roomy :deep(.txt) { font-size: 0.72rem; margin-top: 0.45rem; }
.roomy :deep(.tg) { font-size: 0.6rem; margin-top: 0.5rem; }
</style>

<div class="source">docs/research/CRT_SCANNER.md · docs/FRAME_LOADER.md · OriginalDATDecoder.swift · OriginalFrameLoader.swift · ADDRESS_BOOK.md</div>

<!--
Ключ шифрования DAT (0x44892c · 0x4148a0). SiuHungIsAGoodBearBecauseHeIsVeryGood. Из каждого байта вычитается байт ключа; 123 байта мусорного заголовка тоже прокручивают ключ.

«Do not erase this file.» (0x412277). Каждый DAT расшифровывается посимвольно через fprintf("%c") во временный data\temporary.txt, а после разбора файл затирается этой строкой.

Имя кадра течёт в звук (0f5ceeb). Имена кадров читаются через %s без ограничения в 20 байт и затирают соседние поля: отсюда «указатели звука» ast, down, plod — 38 кадров в 7 файлах.

Кэш звуков на 20 байт (0x455638). Шаг записей — 20 байт, а путь data\SNDDATA_1869.wav с NUL занимает 21. Каждая новая запись затирает хвост предыдущей и меняет результаты поиска.

−6 846 518 779 (fab8104). %d VC80 считает по модулю 2³²: число из kyubi.dat превращается в 1 743 415 813, 4294967296 — в 0, а +nope съедает знак.

Шестой хитбокс (malloc(400)). itr — malloc(400) на 5 записей по 80 байт, bdy — malloc(200) на 5 × 40. Шестой переполнил бы кучу; порт такой DAT отклоняет.

Повторный кадр дописывает (Naruto, кадр 123). Второй `<frame>` с тем же номером не заменяет, а дополняет запись: 318 определений дают 317 кадров.

Каталог одним куском (0x4d823a8). Весь каталог — один malloc на 81 273 768 байт. Actor — 0x420 байт, конструктор пишет 913 из 1 056; остальное порт хранит как «неизвестное», а не как нули.
-->

---

<Kicker>во время игры</Kicker>

# Странное поведение, сохранённое бережно

<div class="roomy">
<IconCards class="mt-3" :cols="4" :items="[
  { icon: 'i-pixelarticons-music', title: 'Музыка из мусорного регистра', text: 'Функция трека Demo берёт мусорный ECX от GetDC/ReleaseDC: при 0 лишний вызов ГСЧ меняет весь Demo', tag: '0x4025d0 · 0x42d7a1' },
  { icon: 'i-pixelarticons-robot', title: 'AI сравнивает себя с указателем', text: 'Без цели AI сравнивает свою z с указателем каталога World+0x7d4 — «Actor 400»', tag: '2c02e5b' },
  { icon: 'i-pixelarticons-keyboard', title: 'd и u', text: 'WndProc пишет в таблицу клавиш 100 и 117 — ASCII <code>d</code> и <code>u</code>, down и up', tag: '0x455378' },
  { icon: 'i-pixelarticons-infinity', title: 'Survival навсегда', text: 'Стадии 50 в <code>stage.dat</code> NTSD 2.4 нет: обе программы показывают «Man: 0» и ждут вечно', tag: '211de58' },
  { icon: 'i-pixelarticons-sword', title: 'War без войск', text: 'С нулём юнитов War не кончается; за краем листа игра полагается на <code>DDERR_INVALIDRECT</code>', tag: '4651853' },
  { icon: 'i-pixelarticons-volume-x', title: 'Тишина в фоне', text: 'Без <code>DSBCAPS_GLOBALFOCUS</code> эффекты молчат в неактивном окне — порт повторяет', tag: 'abf941f' },
  { icon: 'i-pixelarticons-bomb', title: 'Хук за край Actor', text: 'Хук из <code>lib.dll</code> пишет за 0x420-байтный Actor — в куче порта это соседний', tag: 'Actor+0x7b4' },
  { icon: 'i-pixelarticons-debug', title: 'Режимы разработчика', text: 'A, B, C — флаг диагностики, F2 — редактор <code>data.txt</code>, F3 — режим 2. Единственное, что не переносили', tag: '0x450bec' },
]" />
</div>

<style>
.roomy :deep(.ic) { padding: 0.8rem 0.9rem 0.85rem; }
.roomy :deep(.ico) { width: 1.6rem; height: 1.6rem; }
.roomy :deep(.head b) { font-size: 0.8rem; }
.roomy :deep(.txt) { font-size: 0.72rem; margin-top: 0.45rem; }
.roomy :deep(.tg) { font-size: 0.6rem; margin-top: 0.5rem; }
</style>

<div class="source">docs/research/APPLICATION_DEMO.md · WINDOW_INPUT.md · LIB_RUNTIME.md · EXE_COVERAGE_AUDIT_2026-10-03.md</div>

<!--
Музыка из мусорного регистра (0x4025d0 · 0x42d7a1). Функцию выбора трека Demo зовут без аргументов, и её push ecx берёт ECX, оставшийся от GetDC/ReleaseDC в lib.dll. Если там 0 — лишний вызов ГСЧ меняет весь Demo.

AI сравнивает себя с указателем (2c02e5b). AI без цели сравнивает свою z с указателем каталога World+0x7d4 — «Actor 400». После матча он читает ширину фона «Random», которую никто не записывал.

d и u (0x455378). Таблица клавиш — 256 байт. WndProc пишет 100 на WM_KEYDOWN и 117 на WM_KEYUP — это ASCII d и u, down и up.

Survival навсегда (211de58). Пятое нажатие на строке Stage — Survival. Стадии 50 в stage.dat NTSD 2.4 нет: обе программы показывают «Man: 0» и ждут вечно.

War без войск (4651853). War с нулём юнитов не заканчивается. Кадр войск режется за краем листа 800×484 — игра полагается на ответ DirectDraw DDERR_INVALIDRECT.

Тишина в фоне (abf941f). Эффекты молчат в неактивном окне: у звуковых буферов нет DSBCAPS_GLOBALFOCUS. Порт повторяет и это.

Хук за край Actor (Actor+0x7b4). Хук трансформаций из lib.dll пишет за пределы 0x420-байтного Actor — в куче порта это соседний Actor по +0x394.

Режимы разработчика (0x450bec). A, B, C поднимают флаг диагностики, F2 открывает редактор data.txt, F3 — режим 2. Единственный код, который не переносили.
-->

---
clicks: 4
---

<Kicker>случайная находка · из дизассемблера</Kicker>

# Код LF2.NET и скрытый режим

<div class="grid grid-cols-[0.9fr_1.4fr] gap-5 mt-1">
<div>
<ChatLog agent="Claude" human="автор" :messages="[
  { who: 'human', time: '3 окт, 15:58', text: 'что такое «CRAZY!»?' },
  { who: 'agent', time: '3 окт', text: 'Нашёл скрытую пятую сложность «CRAZY!» (-1): включается через фл… …поэтому помечаю как непроверенную.', hot: true },
]" />
<div class="small ink2 mt-3">

В файлах дистрибутива об этом ни слова — режим нашёлся при разборе экрана выбора и обработчика клавиатуры EXE. Коды — домены Little Fighter 2: механизм достался NTSD от движка.

- Второй код **HEROFIGHTER.COM** переключает ещё один флаг, `0x45842c`.
- Оба флага пишутся в запись матча и восстанавливаются при просмотре.
- CRAZY! ещё не сверен с оригиналом под CrossOver.

</div>
</div>
<div>

<Pipeline stepwise :steps="[
  { name: 'LF2.NET', ru: 'набрать в меню режимов', desc: 'автомат в WndProc ведёт состояние 0x45857c' },
  { name: '0x455471 = 100', ru: 'защёлка-клавиша', desc: 'индекс 249 в таблице клавиш' },
  { name: '0x416c70', ru: 'флаг 0x458428', desc: 'флаг = 1 − флаг, звук подтверждения' },
  { name: 'UNLOCK', ru: 'скрытый режим', desc: 'CRAZY! (−1), бойцы с ID 30–39 и 50–59, трансформации без порога HP < 177', accent: true },
]" />

<div v-click="4">
<div class="xsmall muted mt-3 mb-1">17 скрытых бойцов, которых экран выбора пропускает без флага (имена из их DAT-файлов)</div>
<HiddenRoster />
</div>

</div>
</div>

<div class="source">OriginalWindowInput.swift · INPUT_CONTROL.md · CHARACTER_SCREEN.md · MATCH_SELECTION.md · CROSSPLAY_MATRIX.md · скриншот 3 октября</div>

---

<Kicker>археология</Kicker>

# Внутри NTSD всё ещё живёт Little Fighter 2

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-2">
<div>
<img src="/img/lf2-slogans.png" class="pixelated rounded-lg border border-white/10" style="width: 100%" alt="Слоганы Little Fighter 2 внутри EXE">
<div class="xsmall muted mt-1">Битмапы-слоганы LF2 (Davis, «Avoid taking drugs», «Protect your environment»), оставшиеся внутри EXE NTSD</div>
</div>
<div class="small ink2">

- Отладочная строка <code>u%d d%d l%d r%d a%d d%d </code> — с повтором <code>d</code> и пробелом в конце — сохранена как есть.
- Если набрать в меню «LF2.NET», игра проигрывает звук — пасхалка тоже перенесена.
- Опечатки оригинала: сообщение <code>Accpet() Error</code> и суффикс записей турнира <code>_1on1_Prelminar.lfr</code>.
- Детур <code>0x4464c4</code> спрятан в файловом хвосте <code>.text</code> за объявленным размером секции — <code>llvm-objdump</code> его не видит.
- <code>NTSD 2.4.exe</code> весит 31,7 МБ, а код в нём — 283 КБ: титульный экран и меню хранятся как битмапы прямо в исполняемом файле. Рядом лежит <code>lib.dll</code> на 6 144 байта.

</div>
</div>

<div class="source">docs/research/LIB_RUNTIME.md · NETWORK_NOTIFICATION.md · a2a853c · abf941f · ассеты из EXE</div>

---

<Kicker>macOS тоже удивляет</Kicker>

# Пиксель #336699 и другие ловушки Mac

<div class="grid grid-cols-3 gap-4 mt-3">
<div class="card trap">
<div class="trap-h"><span class="i-pixelarticons-colors-swatch trap-ico" /><span class="pixel hl small">цвет · 26 сентября</span></div>
<div class="trap-vis sw">
<div class="swi"><i style="background: #336699" title="#336699 = (51, 102, 153)" /><code>#336699</code><span>задан</span></div>
<span class="swa">→</span>
<div class="swi"><i style="background: rgb(64, 101, 149)" title="(64, 101, 149)" /><code>(64, 101, 149)</code><span>хранился в окне</span></div>
</div>
<p class="trap-t">Проверка цвета обманывала сама себя: <code>NSBitmapImageRep.colorAt</code> отдаёт Generic RGB даже для sRGB. Лечение — явный sRGB у окна.</p>
<span class="tag self-start">6ba168e · 1cd74a1 · a75f3a2</span>
</div>
<div class="card trap">
<div class="trap-h"><span class="i-pixelarticons-moon trap-ico" /><span class="pixel hl small">App Nap · 28 сентября</span></div>
<div class="trap-vis tps">
<div class="tr"><span class="tl">как в оригинале</span><span class="tb"><i style="width: 100%" title="30,3 тика в секунду" /></span><b>30,3</b></div>
<div class="tr"><span class="tl">вне фокуса</span><span class="tb"><i style="width: 26.4%" title="8 тиков в секунду при ~7 % CPU" /></span><b>8</b></div>
<div class="tcap">тиков в секунду; вне фокуса — ~7 % CPU</div>
</div>
<p class="trap-t">Windows фоновый <code>Sleep</code>-цикл игры не тормозит — поэтому приложение держит user-initiated activity.</p>
<span class="tag self-start">9d33d8d</span>
</div>
<div class="card trap">
<div class="trap-h"><span class="i-pixelarticons-music trap-ico" /><span class="pixel hl small">музыка · 29 сентября</span></div>
<div class="trap-vis fmt">
<div class="fmt-row"><span class="chip mono">bgm\ · 8 × WMA</span><span class="swa">→</span><span class="chip mono">ALAC</span></div>
<div class="tcap">без потерь, с побитной проверкой</div>
</div>
<p class="trap-t">Конец трека идёт в восстановленный обратный вызов WndProc (событие <code>0x400</code>) — музыка зацикливается как в оригинале.</p>
<span class="tag self-start">de16c36 · 798a66e</span>
</div>
</div>

<style>
.trap { display: flex; flex-direction: column; gap: 0.55rem; }
.trap-h { display: flex; align-items: center; gap: 0.5rem; }
.trap-ico { width: 1.4rem; height: 1.4rem; color: var(--naruto); flex: none; }
.trap-vis { height: 8.6rem; border-radius: 10px; background: rgba(255, 255, 255, 0.03); border: 1px solid var(--hair); padding: 0.55rem 0.7rem; display: flex; flex-direction: column; justify-content: center; }
.trap-t { font-size: 0.82rem; line-height: 1.42; color: var(--ink-2); margin: 0 !important; flex: 1; }
.sw { flex-direction: row; align-items: center; justify-content: space-between; gap: 0.4rem; }
.swi { display: flex; flex-direction: column; align-items: center; gap: 0.2rem; }
.swi i { width: 5rem; height: 3.5rem; border-radius: 6px; border: 1px solid rgba(255, 255, 255, 0.15); }
.swi code { font-size: 0.66rem !important; }
.swi span { font-size: 0.62rem; color: var(--muted); }
.swa { color: var(--naruto); font-weight: 700; }
.tr { display: grid; grid-template-columns: 6.6rem 1fr 2rem; align-items: center; gap: 0.45rem; height: 2rem; }
.tl { font-size: 0.66rem; color: var(--ink-2); }
.tb { height: 12px; }
.tb i { display: block; height: 12px; background: var(--s1); border-radius: 0 4px 4px 0; }
.tr b { font-size: 0.8rem; color: var(--ink); text-align: right; font-variant-numeric: tabular-nums; }
.tcap { font-size: 0.62rem; color: var(--muted); margin-top: 0.3rem; text-align: center; }
.fmt-row { display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
.chip { font-size: 0.8rem; color: var(--ink); background: rgba(255, 255, 255, 0.06); border: 1px solid var(--hair); border-radius: 6px; padding: 0.2rem 0.5rem; }
</style>

<div class="source">docs/research/APPLICATION_MAC_DISPLAY_COLOR_DIAGNOSIS.md · 9d33d8d · de16c36 · 798a66e</div>

<!--
Цвет (26 сентября; 6ba168e · 1cd74a1 · a75f3a2). В окне с профилем монитора по умолчанию пиксель #336699 хранился как (64, 101, 149). А NSBitmapImageRep.colorAt отдаёт Generic RGB даже для sRGB-битмапа — проверка цвета обманывала сама себя. Лечение: явный sRGB у окна.

App Nap (28 сентября; 9d33d8d). Вне фокуса macOS душил цикл тиков до ~7 % CPU — 8 тиков в секунду вместо 30,3. Windows фоновый Sleep-цикл игры не тормозит, поэтому приложение держит user-initiated activity.

Музыка (29 сентября; de16c36 · 798a66e). 8 треков WMA из bgm\ конвертированы без потерь в ALAC с побитной проверкой. Конец трека доходит до восстановленного обратного вызова WndProc для графа DirectShow (событие 0x400) — музыка зацикливается как в оригинале.
-->

---

<Kicker>архитектура</Kicker>

# Windows-сервисы, на которые отвечает Mac

<div class="grid grid-cols-[1.45fr_1fr] gap-6 mt-1">
<div class="tight">

| | Windows в EXE | роль | ответ на macOS |
| --- | --- | --- | --- |
| <span class="i-pixelarticons-app-windows svc" /> | WinMain `0x43cf40`, WndProc `0x43b3d0` | сообщения, темп | восстановленный WinMain; AppKit → `WM_KEYDOWN/CHAR` |
| <span class="i-pixelarticons-clock svc" /> | `timeGetTime`, `Sleep` | 33 мс на тик | часы хоста или `--virtual-clock` |
| <span class="i-pixelarticons-monitor svc" /> | DirectDraw, 794×550×8 | Blt, color key | `NSWindow`, XRGB8888 |
| <span class="i-pixelarticons-volume-2 svc" /> | DirectSound | буферы, 1/100 дБ | AVFoundation, gain 10^(v/2000) |
| <span class="i-pixelarticons-music svc" /> | DirectShow | `bgm\*.wma` | ALAC, событие EC_COMPLETE |
| <span class="i-pixelarticons-text-start-t svc" /> | GDI `TextOutA` | подписи | системный шрифт macOS |
| <span class="i-pixelarticons-gamepad svc" /> | WinMM `joyGetPosEx` | 2 джойстика | `GCController`, опрос 25 мс |
| <span class="i-pixelarticons-globe svc" /> | Winsock 1.1 | сеть | BSD sockets, `SO_NOSIGPIPE` |
| <span class="i-pixelarticons-plug svc" /> | `lib.dll` | 12 хуков | Swift, без DLL |

</div>
<div>

<div class="card">
<div class="pixel hl small">модули Swift · строк кода</div>
<div class="lmods mt-2">
<div class="lmod"><span class="lmod-n">NTSDCore</span><span class="lmod-b"><i style="width: 65.2%" title="NTSDCore: 30 540 строк" /></span><b>30 540</b></div>
<div class="lmod"><span class="lmod-n">NTSDReferenceChecks</span><span class="lmod-b"><i style="width: 24.1%" title="NTSDReferenceChecks: 11 277 строк" /></span><b>11 277</b></div>
<div class="lmod"><span class="lmod-n">NTSDMacPlatform</span><span class="lmod-b"><i style="width: 9.65%" title="NTSDMacPlatform: 4 523 строки" /></span><b>4 523</b></div>
<div class="lmod"><span class="lmod-n">NTSDApp</span><span class="lmod-b"><i style="width: 3.23%" title="NTSDApp: 1 515 строк" /></span><b>1 515</b></div>
<div class="lmod tests"><span class="lmod-n">тесты, 692 функции</span><span class="lmod-b"><i style="width: 100%" title="тесты: 46 852 строки" /></span><b>46 852</b></div>
</div>
<div class="xsmall muted mt-2">zlib 1.1.4 вшит отдельным C-модулем</div>
</div>

<div class="card-soft mt-3 small ink2">
Core выдаёт запросы с аргументами оригинала — вплоть до смещения метода в vtable. Физический ввод-вывод выполняется только после commit транзакции Core; откат такта его не отменяет.
</div>

</div>
</div>

<div class="source">native/Sources/NTSDMacPlatform · docs/research/APPLICATION_MAC_AUDIO.md · NETWORK_PLAY.md · APPLICATION_JOYSTICKS.md</div>

<style>
.svc { display: inline-block; width: 1.05rem; height: 1.05rem; color: var(--naruto); vertical-align: -0.2rem; }
.tight td:first-child, .tight th:first-child { width: 1.6rem; padding-right: 0 !important; }
.lmods { display: flex; flex-direction: column; gap: 0.32rem; }
.lmod { display: grid; grid-template-columns: 8.4rem 1fr 2.6rem; align-items: center; gap: 0.5rem; }
.lmod-n { font-size: 0.7rem; color: var(--ink); white-space: nowrap; }
.lmod-b { height: 8px; }
.lmod-b i { display: block; height: 8px; background: var(--s1); border-radius: 0 4px 4px 0; }
.lmod b { font-size: 0.72rem; color: var(--ink); text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.lmod.tests .lmod-n { color: var(--muted); }
.lmod.tests .lmod-b i { background: var(--s1); opacity: 0.45; }
</style>
