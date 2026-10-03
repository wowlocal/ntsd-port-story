---
layout: chapter
num: 9
total: 11
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

<div class="grid grid-cols-4 gap-3 mt-3">
<QuirkCard title="Ключ шифрования DAT" icon="🔑" addr="0x44892c · 0x4148a0">
<code style="word-break: break-all">SiuHungIsAGoodBearBecauseHeIsVeryGood</code>. Из каждого байта вычитается байт ключа; 123 байта мусорного заголовка тоже прокручивают ключ.
</QuirkCard>
<QuirkCard title="«Do not erase this file.»" icon="📝" addr="0x412277">
Каждый DAT расшифровывается посимвольно через <code>fprintf("%c")</code> во временный <code>data\temporary.txt</code>, а после разбора файл затирается этой строкой.
</QuirkCard>
<QuirkCard title="Имя кадра течёт в звук" icon="🔊" commit="0f5ceeb">
Имена кадров читаются через <code>%s</code> без ограничения в 20 байт и затирают соседние поля: отсюда «указатели звука» <code>ast</code>, <code>down</code>, <code>plod</code> — 38 кадров в 7 файлах.
</QuirkCard>
<QuirkCard title="Кэш звуков на 20 байт" icon="📦" addr="0x455638">
Шаг записей — 20 байт, а путь <code>data\SNDDATA_1869.wav</code> с NUL занимает 21. Каждая новая запись затирает хвост предыдущей и меняет результаты поиска.
</QuirkCard>
<QuirkCard title="−6 846 518 779" icon="🔢" commit="fab8104">
<code>%d</code> VC80 считает по модулю 2³²: число из <code>kyubi.dat</code> превращается в 1 743 415 813, <code>4294967296</code> — в 0, а <code>+nope</code> съедает знак.
</QuirkCard>
<QuirkCard title="Шестой хитбокс" icon="💥" addr="malloc(400)">
<code>itr</code> — <code>malloc(400)</code> на 5 записей по 80 байт, <code>bdy</code> — <code>malloc(200)</code> на 5 × 40. Шестой переполнил бы кучу; порт такой DAT отклоняет.
</QuirkCard>
<QuirkCard title="Повторный кадр дописывает" icon="➕" addr="Naruto, кадр 123">
Второй <code>&lt;frame&gt;</code> с тем же номером не заменяет, а дополняет запись: 318 определений дают 317 кадров.
</QuirkCard>
<QuirkCard title="Каталог одним куском" icon="🧱" addr="0x4d823a8">
Весь каталог — один <code>malloc</code> на 81 273 768 байт. Actor — 0x420 байт, конструктор пишет 913 из 1 056; остальное порт хранит как «неизвестное», а не как нули.
</QuirkCard>
</div>

<div class="source">docs/research/CRT_SCANNER.md · docs/FRAME_LOADER.md · OriginalDATDecoder.swift · OriginalFrameLoader.swift · ADDRESS_BOOK.md</div>

---

<Kicker>во время игры</Kicker>

# Странное поведение, сохранённое бережно

<div class="grid grid-cols-4 gap-3 mt-3">
<QuirkCard title="Музыка из мусорного регистра" icon="🎵" addr="0x4025d0 · 0x42d7a1">
Функцию выбора трека Demo зовут без аргументов, и её <code>push ecx</code> берёт ECX, оставшийся от GetDC/ReleaseDC в <code>lib.dll</code>. Если там 0 — лишний вызов ГСЧ меняет весь Demo.
</QuirkCard>
<QuirkCard title="AI сравнивает себя с указателем" icon="🤖" commit="2c02e5b">
AI без цели сравнивает свою z с указателем каталога World+0x7d4 — «Actor 400». После матча он читает ширину фона «Random», которую никто не записывал.
</QuirkCard>
<QuirkCard title="d и u" icon="⌨" addr="0x455378">
Таблица клавиш — 256 байт. WndProc пишет 100 на <code>WM_KEYDOWN</code> и 117 на <code>WM_KEYUP</code> — это ASCII <code>d</code> и <code>u</code>, down и up.
</QuirkCard>
<QuirkCard title="Survival навсегда" icon="♾" commit="211de58">
Пятое нажатие на строке Stage — Survival. Стадии 50 в <code>stage.dat</code> NTSD 2.4 нет: обе программы показывают «Man: 0» и ждут вечно.
</QuirkCard>
<QuirkCard title="War без войск" icon="⚔" commit="4651853">
War с нулём юнитов не заканчивается. Кадр войск режется за краем листа 800×484 — игра полагается на ответ DirectDraw <code>DDERR_INVALIDRECT</code>.
</QuirkCard>
<QuirkCard title="Тишина в фоне" icon="🔇" commit="abf941f">
Эффекты молчат в неактивном окне: у звуковых буферов нет <code>DSBCAPS_GLOBALFOCUS</code>. Порт повторяет и это.
</QuirkCard>
<QuirkCard title="Хук за край Actor" icon="🧨" addr="Actor+0x7b4">
Хук трансформаций из <code>lib.dll</code> пишет за пределы 0x420-байтного Actor — в куче порта это соседний Actor по +0x394.
</QuirkCard>
<QuirkCard title="Режимы разработчика" icon="🛠" addr="0x450bec">
A, B, C поднимают флаг диагностики, F2 открывает редактор <code>data.txt</code>, F3 — режим 2. Единственный код, который не переносили.
</QuirkCard>
</div>

<div class="source">docs/research/APPLICATION_DEMO.md · WINDOW_INPUT.md · LIB_RUNTIME.md · EXE_COVERAGE_AUDIT_2026-10-03.md</div>

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
<div class="card">
<div class="pixel hl small">цвет · 26 сентября</div>
<p class="small ink2">В окне с профилем монитора по умолчанию пиксель <code>#336699</code> хранился как <b>(64, 101, 149)</b>. А <code>NSBitmapImageRep.colorAt</code> отдаёт Generic RGB даже для sRGB-битмапа — проверка цвета обманывала сама себя. Лечение: явный sRGB у окна.</p>
<span class="tag">6ba168e · 1cd74a1 · a75f3a2</span>
</div>
<div class="card">
<div class="pixel hl small">App Nap · 28 сентября</div>
<p class="small ink2">Вне фокуса macOS душил цикл тиков до ~7 % CPU — 8 тиков в секунду вместо 30,3. Windows фоновый <code>Sleep</code>-цикл игры не тормозит, поэтому приложение держит user-initiated activity.</p>
<span class="tag">9d33d8d</span>
</div>
<div class="card">
<div class="pixel hl small">музыка · 29 сентября</div>
<p class="small ink2">8 треков WMA из <code>bgm\</code> конвертированы без потерь в ALAC с побитной проверкой. Конец трека доходит до восстановленного обратного вызова WndProc для графа DirectShow (событие <code>0x400</code>) — музыка зацикливается как в оригинале.</p>
<span class="tag">de16c36 · 798a66e</span>
</div>
</div>

<div class="source">docs/research/APPLICATION_MAC_DISPLAY_COLOR_DIAGNOSIS.md · 9d33d8d · de16c36 · 798a66e</div>

---

<Kicker>архитектура</Kicker>

# Windows-сервисы, на которые отвечает Mac

<div class="grid grid-cols-[1.45fr_1fr] gap-6 mt-1">
<div class="tight">

| Windows в EXE | роль | ответ на macOS |
| --- | --- | --- |
| WinMain `0x43cf40`, WndProc `0x43b3d0` | сообщения, темп | восстановленный WinMain; AppKit → `WM_KEYDOWN/CHAR` |
| `timeGetTime`, `Sleep` | 33 мс на тик | часы хоста или `--virtual-clock` |
| DirectDraw, 794×550×8 | Blt, color key | `NSWindow`, XRGB8888 |
| DirectSound | буферы, 1/100 дБ | AVFoundation, gain 10^(v/2000) |
| DirectShow | `bgm\*.wma` | ALAC, событие EC_COMPLETE |
| GDI `TextOutA` | подписи | системный шрифт macOS |
| WinMM `joyGetPosEx` | 2 джойстика | `GCController`, опрос 25 мс |
| Winsock 1.1 | сеть | BSD sockets, `SO_NOSIGPIPE` |
| `lib.dll` | 12 хуков | Swift, без DLL |

</div>
<div>

<div class="card">
<div class="pixel hl small">модули Swift</div>
<div class="grid grid-cols-[1fr_auto] gap-x-3 gap-y-1 small mt-2">
<span>NTSDCore</span><b>30 540</b>
<span>NTSDReferenceChecks</span><b>11 277</b>
<span>NTSDMacPlatform</span><b>4 523</b>
<span>NTSDApp</span><b>1 515</b>
<span class="muted">тесты, 692 функции</span><b>46 852</b>
</div>
<div class="xsmall muted mt-2">строк кода · zlib 1.1.4 вшит отдельным C-модулем</div>
</div>

<div class="card-soft mt-3 small ink2">
Core выдаёт запросы с аргументами оригинала — вплоть до смещения метода в vtable. Физический ввод-вывод выполняется только после commit транзакции Core; откат такта его не отменяет.
</div>

</div>
</div>

<div class="source">native/Sources/NTSDMacPlatform · docs/research/APPLICATION_MAC_AUDIO.md · NETWORK_PLAY.md · APPLICATION_JOYSTICKS.md</div>
