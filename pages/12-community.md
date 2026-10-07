---
layout: chapter
num: 12
total: 15
kicker: Сообщество
dates: 2007 → 3 октября 2026
image: /img/covers/ch12-collage.jpg
imagePixel: false
stats: Discord · лента · что дальше
---

# Игру не бросали

В самом конце нашлось сообщество, которое с 2007 года развивает NTSD без единой строчки исходников. Ему и отдали переписанную игру.

---

<Kicker>история · 2007–2026</Kicker>

# Девятнадцать лет без исходников

<HistoryTimeline class="mt-1" from="2007-07-01" to="2026-12-31" :ticks="['2008-01-01', '2010-01-01', '2012-01-01', '2014-01-01', '2016-01-01', '2018-01-01', '2020-01-01', '2022-01-01', '2024-01-01', '2026-01-01']" :height="196" :axis="100" :gap="22"
  :kinds="{ ntsd: { color: '#c3c2b7', name: 'версии NTSD' }, base: { color: 'var(--s1)', name: 'основа порта' }, community: { color: 'var(--s3)', name: 'сообщество' }, port: { color: 'var(--naruto)', name: 'этот порт' } }"
  :events="[
    { t: '2007-11-15', label: '2007 · тема на форуме LF-Empire', row: 3, kind: 'community' },
    { t: '2008-01-23', label: 'Beta 1.8', row: -1, kind: 'ntsd' },
    { t: '2008-09-01', label: '2.1–2.3', row: 2, kind: 'ntsd' },
    { t: '2009-06-14', label: '14.06.2009 · NTSD 2.4', row: 1, kind: 'ntsd' },
    { t: '2010-11-01', label: '2010–2011 · 2.4_2.0a + lib.dll', sub: 'основа порта', row: -2, kind: 'base' },
    { t: '2014-12-26', label: 'Neora · 2014', row: 1, end: true, kind: 'ntsd' },
    { t: '2015-07-01', label: 'турнир 2015 · .lfr', row: -1, end: true, kind: 'community' },
    { t: '2016-12-01', label: 'Discord · 2016', row: 1, kind: 'community' },
    { t: '2018-07-07', label: 'Community Edition · 2018', row: -3, end: true, kind: 'ntsd' },
    { t: '2019-02-19', label: 'NTSD 2.5 · 2019', sub: '«after 10 years of inactivity»', row: 2, kind: 'ntsd' },
    { t: '2019-09-19', label: 'NTSD 2.6', sub: 'Конан, высокое разрешение', row: -2, kind: 'ntsd' },
    { t: '2021-06-07', label: '2021 · «…I would have to move to a new engine»', row: 1, kind: 'community' },
    { t: '2026-10-02', label: '2 окт 2026 · «Not anymore 🙂»', row: -1, end: true, kind: 'port' },
  ]" />

<div class="grid grid-cols-3 gap-4 mt-4 xsmall ink2">
<div><b class="ink">«2.4_2.0a» — не новая версия, а пересадка.</b> Кредиты и <code>data.txt</code> совпадают побайтно; EXE заменён на LF2 2.0a ради фикса зеркальных спрайтов — 326 файлов <code>*_mirror.bmp</code>.</div>
<div><b class="ink">Сообщество живо.</b> В Discord около 3 842 участников, на форуме с 2008 года — 6 390 пользователей и 273 666 сообщений; NTSD 2.6 на ModDB скачали около 49,8 тыс. раз.</div>
<div><b class="ink">Исходники закрыты официально.</b> FAQ LF2: «Will LF2 be open source? No, we are not planning to do that.» Новые сборки после 2.6 раздают только через Discord.</div>
</div>

<div class="source">форумы LF-Empire и NTSD (снимки Wayback) · ModDB · lf2.net FAQ · локальный дистрибутив 2.4_2.0a · data/evidence/ntsd-history.json</div>

---

<Kicker>авторы и моддеры</Kicker>

# Тысяча hex-правок и одна DLL

<div class="grid grid-cols-[1fr_1.25fr] gap-5 mt-2">
<div>
<div class="card-soft">
<div class="pixel hl small">Little Fighter 2</div>
<p class="xsmall ink2 mb-0" style="line-height: 1.45">Марти Вонг и Старски Вонг, 1999. «Are Marti and Starsky brothers? — No, but we are very good friends». Visual C++ и DirectX; исходники не открывали. Старски — PhD в UCLA, IBM Research, теперь Tech Lead в Meta. Марти 18 июля 2025 года выпустил Little Fighter 2 Remastered в Steam — для Windows и macOS.</p>
</div>
<div class="card-soft mt-3">
<div class="pixel hl small">NTSD</div>
<p class="xsmall ink2 mb-0" style="line-height: 1.45">Основатель — zxcv11791: «leader, coder, sprites, stages», команда около десяти человек. В 2018 году он вернулся с NTSD Z. Высказываний авторов об исходниках, разрешениях или порте не нашлось.</p>
</div>
</div>
<div class="small ink2">

- **2009:** «the mods for LF2 include more than 1000 hex edits, thus the creators are not willing to redo their whole work».
- **`lib.dll`** повторяет туториал 2009 года «Patching exe to load DLL»: точка входа уводится в пустое место кода и вызывает `LoadLibraryA`. DLL переписывает 62 байта в 13 местах EXE — ровно это нашёл порт.
- **2016:** форумчанин угадал «a new 4xxx transformation state». Порт нашёл хук трансформаций с ветвью 4000-диапазона.
- **Neora** собрали три сообщества: EXE от Alkarter (китайское), DLL-каркас Silva (LF-Empire), сборка Archer-Dante с русского lfforever.ru, 2014. Имя — «Neo» + «Ra» от `rarara.dll`.
- **Предел:** «DC has a set, defined limit of impossibility, whereas Hex really does not» (2009) — и «no way to fix it… I would have to move to a new engine» (Tyci, 2021).

</div>
</div>

<div class="source">lf2.net FAQ и страница Starsky Wong · Steam · LF-Empire: «Patching exe to load DLL», LF2 DLL Framework, Neora · форум NTSD · ntsd-2.4: LIB_RUNTIME.md</div>

---

<Kicker>Discord NTSD · 10 февраля 2024</Kicker>

# «Движок всегда был закрыт»

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-3">
<DiscordLog :messages="[
  { day: '10 февраля 2024' },
  { who: 'Nydek', color: '#e8e8e8', time: '18:09', text: 'is there an open-source code for NTSD somewhere?' },
  { who: 'Remie', color: '#e9a25f', time: '18:19', text: 'If curious enough, mess around with Genma in custom folder or alternatively any 2.4 version or lower from the Remiemastered bundle.<br><br>The engine itself has always been closed for everyone though. Just characters and object files can be edited.' },
  { who: 'The Scar', color: '#4fd466', time: '18:20', reply: { who: 'Remie', text: 'The engine itself has always been closed for everyone though…' }, text: 'all exe changes are made in exe or through dll on assembler<br>that’s how it works here' },
]" />
<div class="small ink2">

Так NTSD живёт с 2007 года. Персонажей, объекты и фоны меняют в DAT-файлах и картинках. Всё, что касается самого движка, правят патчами EXE и DLL на ассемблере.

В нашем baseline тоже лежит такая библиотека: `lib.dll` на старте патчит код игры (глава 3).

<div class="card-soft mt-4">
<div class="pixel hl small">чего нельзя без исходников</div>
<p class="xsmall ink2 mb-0">Перенести игру на другую платформу, переписать сетевой код, добавить механику, которой нет в движке, — всё это требует менять скомпилированный код вслепую.</p>
</div>

</div>
</div>

<div class="source">скриншоты Discord-сервера NTSD, 10 февраля 2024 · ники как на сервере, аватары не показаны</div>

---
layout: statement
kicker: Discord NTSD · 2 октября 2026
---

Not anymore 🙂

<!--
Ответ автора порта на то самое сообщение Remie 2024 года — «The engine itself has always been closed for everyone though…». 2 октября 2026, 09:19.
-->

---

<Kicker>Discord NTSD · 2–3 октября 2026</Kicker>

# От ссылки до релиза

<div class="grid grid-cols-2 gap-4 mt-1">
<DiscordLog :messages="[
  { day: '2 октября 2026' },
  { me: true, who: 'resultBuilder', color: '#b5c4a8', time: '09:01', text: 'Hello everybody! Huge fan of the game. Played with my pals when we were kids… We tried to do original game exe analysis with most powerful AI at the time (GPT Astra xhigh and Opus 5.5 xhigh). Take a look what we’ve got <span class=link>github.com/wowlocal/ntsd-2.4</span><br><br>The game is playable, bot AI is working, sounds, everything except remote coop (LLMs refuse to write low level networking code)' },
  { me: true, who: 'resultBuilder', color: '#b5c4a8', time: '09:19', reply: { who: 'Remie', text: 'The engine itself has always been closed for everyone though…' }, text: 'Not anymore 🙂' },
  { who: 'The Scar', color: '#4fd466', time: '10:07', text: 'it is cool for someone who would like to play avoiding Crossover (but it works +- normally there)' },
  { who: 'The Scar', color: '#4fd466', time: '10:32', text: '<span class=link>openlf2.github.io/OpenLF2</span> Also take a look for this project. As author says it is pure 100% reverse-engineered version of original LF2…' },
]" />
<DiscordLog :messages="[
  { me: true, who: 'resultBuilder', color: '#b5c4a8', time: '11:42', reply: { who: 'The Scar', text: 'Can you also provide video with port working on Mac?' }, text: 'Can’t attach videos here for some reason. Uploaded it to youtube', embed: { site: 'YouTube', title: 'Misha Nya · 2 October 2026' }, reactions: ['🔥 1'] },
  { who: 'The Scar', color: '#4fd466', time: '13:14', text: 'i still notice some artefacts but progress is impressive' },
  { day: '3 октября' },
  { me: true, who: 'resultBuilder', color: '#b5c4a8', time: '14:14', reply: { who: 'The Scar', text: 'i still notice some artefacts but progress is impressive' }, text: 'Fixed artifacts, added networking. Game is verified against original, its identical.<br><br>Notarized and signed version will be available soon on github releases', reactions: ['❤️ 1'] },
  { me: true, who: 'resultBuilder', color: '#b5c4a8', time: '17:49', text: 'The release is available here', embed: { site: 'GitHub', title: 'Release NTSD Native 0.4.0 for macOS · wowlocal/ntsd-2.4', text: 'A native macOS port of Naruto: The Setting Dawn 2.4… written in Swift and has no emulator or Wine inside.' } },
]" />
</div>

<div class="source">скриншоты Discord-сервера NTSD · время по часам автора · resultBuilder — автор порта</div>

---

<Kicker>ссылка из Discord · проверено 3 октября</Kicker>

# OpenLF2: «100% reverse-engineered»?

<div class="grid grid-cols-[0.95fr_1.05fr] gap-6 mt-2">
<div>

<Timeline dense :items="[
  { time: '25 сен', title: 'на GitHub появляется организация OpenLF2' },
  { time: '27 сен', title: 'создан репозиторий' },
  { time: '28 сен', title: 'initial commit: 27 268 строк в 175 файлах', hot: true },
  { time: '+18 мин', title: 'релиз v0.9.0' },
  { time: '2 окт', title: 'v0.9.1: 20 сборок, от Windows и macOS до iOS, Switch и Vita' },
]" />

<p class="xsmall muted mt-2" style="line-height: 1.4">22 коммита, один автор, лицензия MIT. История разработки до initial commit не опубликована.</p>

<div class="card mt-2">
<div class="pixel hl small">вердикт</div>
<p class="xsmall ink2 mb-0" style="line-height: 1.45">Серьёзная реимплементация LF2, а не декомпиляция. «100%» ничем публично не подкреплено: функции видны сразу, а совпадение с оригиналом всё ещё нужно доказывать.</p>
</div>

</div>
<div class="small ink2">

- **C++23, SDL3 и LuaJIT**: 19,7 тыс. строк своего кода — больше, чем у L2DF или F.LF.
- **Все шесть режимов** LF2 подключены. Записи пишутся в формате оригинала, ключ берётся из его EXE.
- **Сеть** — свой протокол на TCP, с оригиналом несовместим.
- **Тестов нет**, сверки с оригиналом не опубликовано. README сам предупреждает: <span class="mono xsmall">«Some behavior and platform builds have not yet been verified against the original game»</span>.
- **Принимает только установщик LF2 v2.0a**, сверяя SHA-256, поэтому NTSD 2.4 не загрузит.

</div>
</div>

<div class="source">github.com/OpenLF2/OpenLF2 @ 56e4a47: README L5–16, L84–85 · installer.hpp L15–18 · scripts/base/ui/flow.lua L164–187 · GitHub API · data/evidence/lf2-oss-engines.json → followups</div>

---

<Kicker>лента X и YouTube · 30 сентября — 3 октября 2026</Kicker>

# Не я один

<div class="trend grid grid-cols-3 gap-3 mt-2">
<figure><img src="/img/trend/cydonix-skyrim-tarkov-spiderman.jpg" alt=""><figcaption><b>Skyrim × Tarkov × Spider-Man</b> · 1 окт · 2,5 млн просмотров. Tarkov-в-Skyrim, по Kotaku, сделали «за несколько часов»</figcaption></figure>
<figure><img src="/img/trend/tobynjacobs-elden-ring-mac.jpg" alt=""><figcaption><b>Minecraft в Elden Ring на Mac</b>: исходный пост — 20,7 млн просмотров, открытый клон появился через два дня</figcaption></figure>
<figure><img src="/img/trend/chasm-wow-bevy.jpg" alt=""><figcaption><b>«WoW 1.12.1 переписан на Bevy/Rust»</b> — это benilla. Community Note: «does not make private servers legal»</figcaption></figure>
<figure><img src="/img/trend/smallzero-cs16.jpg" alt=""><figcaption><b>CS 1.6 в браузере, 16 игроков</b> · «all vibe coded by AI» · 51 тыс.</figcaption></figure>
<figure class="col-span-2 wide"><img src="/img/trend/chasm-videos.jpg" alt=""><figcaption><b>chasm</b>: MW2 × Skate 3 × Minecraft поверх трёх Rust-переписок, «basically 100% vibe coded». «Modding has Change FOREVER…» — 1,5 млн просмотров за два дня</figcaption></figure>
</div>

<style>
.trend figure { margin: 0; background: var(--surface); border: 1px solid var(--hair); border-radius: 10px; overflow: hidden; }
.trend img { display: block; width: 100%; height: 136px; object-fit: cover; object-position: top; }
.trend .wide img { height: 136px; object-fit: contain; background: #0f0f0f; }
.trend figcaption { font-size: 0.6rem; color: var(--ink-2); padding: 0.3rem 0.55rem 0.35rem; line-height: 1.3; }
.trend figcaption b { color: var(--ink); font-weight: 600; }
</style>

<div class="source">скриншоты ленты автора 3 октября 2026 · Kotaku, MakeUseOf, heldgames.com, Community Note · data/evidence/ai-game-rewrites-2026.json</div>

---

<Kicker>samwhosung/benilla · 3 октября</Kicker>

# Не поверил — собрал сам

<div class="grid grid-cols-[1.15fr_1fr] gap-5 mt-2">
<div>
<img src="/img/trend/benilla-run.jpg" class="shot" alt="benilla на ноутбуке автора">
<div class="xsmall muted mt-1">Собрал на ноутбуке, поднял сервер — работает: персонаж в Westfall, рядом график загрузки ядер.</div>
</div>
<div class="small ink2">

- **Полный клиент WoW 1.12.1** на Rust и Bevy, написанный с нуля: «no original client code… no bundled game assets».
- **553 из 559 коммитов — с Claude** (Fable 5, Opus 5.5, Fable 5.1). Автор: «Took 3 months. Multiple Claude Code sessions and accounts running non-stop against the original binary».
- **Метод тот же, что у порта.** <span class="mono xsmall">«The reference client is the spec»</span>, <span class="mono xsmall">«Measure, never eyeball»</span>, <span class="mono xsmall">«Prove the run before reading the result»</span>; около 169 коммитов ссылаются на адреса в оригинальном клиенте.
- **Нужна своя копия**: клиент 1.12.1 (build 5875) и сервер без Warden — vmangos или cMaNGOS.
- **525★ и 107 форков**, 50 из них — за 1–3 октября, после поста chasm.

</div>
</div>

<style>
.shot { width: 100%; max-height: 292px; object-fit: cover; object-position: top; border-radius: 10px; border: 1px solid var(--hair); display: block; }
</style>

<div class="source">github.com/samwhosung/benilla: README, AGENTS.md, docs/METHOD.md, git log · пост автора 24 июля 2026 · data/evidence/ai-game-rewrites-2026.json</div>

---

<Kicker>контекст · 2004–2026</Kicker>

# Раньше — годы, теперь — недели

<RewriteTimeline class="mt-1" />

<div class="grid grid-cols-3 gap-4 mt-2 xsmall ink2">
<div><b class="ink">Общее у всех — копия оригинала.</b> От OpenMW («A copy of the original game… is required») до benilla и этого порта: код новый, данные — ваши.</div>
<div><b class="ink">Раньше</b> декомпиляция Ocarina of Time заняла 21 месяц, OpenRCT2 собрал около 250 участников. <b class="ink">Теперь</b> — 3 месяца на benilla и 27 дней на этот порт.</div>
<div><b class="ink">Но не из пустоты.</b> README Skate 3 Rust Engine: «Describing the project as simply "AI rewriting Skate 3" leaves out the work that made it possible».</div>
</div>

<div class="source">Wikipedia и README проектов · github.com/samwhosung/benilla · vladtrc/iw4L · SK8-ENGINE/skate-3-rust-engine · OpenLF2/OpenLF2 · data/evidence/ai-game-rewrites-2026.json</div>

---

<Kicker>что дальше · на вечер 3 октября</Kicker>

# Что открывает исходный код

<div class="grid grid-cols-[1fr_auto_1fr] gap-3 items-center mt-1 small">
<div class="card-soft"><div class="pixel small muted">2008–2026 · моддинг без исходников</div><div class="xsmall ink2 mt-1">Персонажи и объекты меняют в DAT, движок — бинарными патчами: <code>lib.dll</code> NTSD ставит 12 переходов и одну двухбайтовую правку.</div></div>
<div class="hl display" style="font-size: 1.4rem">→</div>
<div class="card-soft" style="border-color: rgba(255,138,61,0.45)"><div class="pixel small hl">октябрь 2026 · логика игры как код</div><div class="xsmall ink2 mt-1">NTSDCore — 30,7 тыс. строк Swift, 84 % приложения. Каждый сервис Windows — запрос к слою платформы. 46,9 тыс. строк тестов.</div></div>
</div>

<div class="persp grid grid-cols-3 gap-3 mt-3">
<div class="card">
<div class="ph pixel" style="color: var(--s3)"><span class="i-pixelarticons-check" />работает</div>
<ul>
<li><b>Сеть по протоколу оригинала</b>: два Mac-приложения сыграли матч до итогов, общее состояние совпало</li>
<li><b>v0.4.0</b> подписан и нотаризован, сеть включена; онлайн в README — «in progress»</li>
</ul>
</div>
<div class="card">
<div class="ph pixel" style="color: var(--s1)"><span class="i-pixelarticons-loader" />в работе</div>
<ul>
<li><b>Одно ядро на всех платформах</b> — без веток геймплея и второго движка <span class="fwd">→ глава 13</span></li>
<li><b>Linux</b>: ядро впервые собралось 3 октября; дальше Windows, iPad и Android <span class="fwd">→ за 30 часов</span></li>
<li><b>Кроссплей с оригиналом</b> под Windows — цель, пока не наблюдался</li>
</ul>
</div>
<div class="card">
<div class="ph pixel hl"><span class="i-pixelarticons-lightbulb" />становится возможным</div>
<ul>
<li>новые механики и режимы — кодом, а не переходами в DLL</li>
<li>инструменты моддинга поверх загрузчика данных ядра</li>
<li>Metal и SDL3 вместо программной отрисовки, консоли</li>
<li>игра через интернет без проброса портов</li>
</ul>
</div>
</div>

<div class="xsmall muted mt-3">Сейчас правила требуют точной верности оригиналу, поэтому третья колонка — идеи. Но эталон остаётся: оригинальное поведение можно держать за переключателем и сверять, что оно не сломалось.</div>

<style>
.persp .ph { display: flex; align-items: center; gap: 0.4rem; font-size: 0.8rem; }
.persp .ph span { width: 1.1rem; height: 1.1rem; }
.persp ul { margin: 0.4rem 0 0; padding-left: 1rem; }
.persp li { font-size: 0.72rem; line-height: 1.38; color: var(--ink-2); margin: 0.3rem 0; }
.persp li b { color: var(--ink); }
.persp .fwd { color: var(--naruto); font-weight: 600; white-space: nowrap; }
</style>

<div class="source">ntsd-2.4: CROSS_PLATFORM.md L3–21, L86–124 · NETWORK_PLAY.md L21–23, L233–250 · NETWORK_PLAY_PLAN.md L13–45, L93–94 · LIB_RUNTIME.md L3–6, L63–66 · PLAN.md L28–30 · 65c6916 (локальная ветка)</div>

<!--
Подробности, убранные со слайда. Сеть по протоколу оригинала: TCP 12345, таблица случайных чисел 3 001 байт, 22 байта на тик; два Mac-приложения сыграли матч до итогов — 836 пакетов в каждую сторону. iPad — сначала контроллер и клавиатура, потом тач; все платформы — кросс-компиляцией с Mac. Сейчас отрисовка программная, 794×550.
-->
