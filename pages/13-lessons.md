---
layout: chapter
num: 13
total: 13
kicker: Эпилог
dates: 3 октября 2026
image: /img/stage-1-1-background.jpg
stats: релиз v0.4.0 · что дальше · чему научились
---

# Уроки

Порт выпущен: 3 октября на GitHub вышла подписанная и нотаризованная сборка v0.4.0 — всю игру можно скачать и играть. А методика доказала главное: агенты могут восстанавливать сложное поведение, не угадывая.

---

<Kicker>релиз · 3 октября, 16:46</Kicker>

# v0.4.0: игру можно скачать

<div class="grid grid-cols-3 gap-4 mt-3 small">
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

<div class="source">github.com/wowlocal/ntsd-2.4/releases/tag/v0.4.0 · tools/release-macos.sh · docs/research/CROSSPLAY_MATRIX.md</div>

---

<Kicker>что дальше · /loop на ветке dev/crossplatform · 3 октября, 20:11–21:01</Kicker>

# Агент в цикле: Linux, Windows, iPad

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
  { id: 'P0', name: 'тулчейны', state: 'part', note: 'Linux готов; для Windows ждём согласия с лицензией Microsoft' },
  { id: 'P1', name: 'граф пакета', state: 'done', note: 'сборка без Mac-целей, тесты разделены переносом файлов' },
  { id: 'P2', name: 'переносимость ядра', state: 'done', note: 'SHA-256, часы, zlib — ядро и проверки собираются под Linux' },
  { id: 'P3', name: 'детерминизм на Linux', state: 'next', note: 'байты состояния, ГСЧ и записи — как на macOS' },
  { id: 'P4', name: 'Windows без окна', state: 'ahead', note: 'то же под Wine; настоящий Windows отдельно' },
  { id: 'P5', name: 'общий рантайм', state: 'ahead', note: 'окно, звук, ввод, сокеты — за протоколами' },
  { id: 'P6', name: 'бэкенд SDL3', state: 'ahead', note: 'кадры и состояние совпадают с Mac-бэкендом' },
  { id: 'P7', name: 'приложения Linux и Windows', state: 'ahead', note: 'матч Наруто/Саске по записи на каждой платформе' },
  { id: 'P8', name: 'мобильные', state: 'ahead', note: 'iPad с контроллером, затем тач и Android' },
]" />

</div>
</div>

<div class="source">ntsd-2.4 (локальная ветка dev/crossplatform): docs/research/CROSS_PLATFORM.md — план, правила, журнал статуса · c753d7c … 6203799 · состояние на 21:01</div>

---

<Kicker>методология в восьми строках</Kicker>

# Что стоит унести с собой

<div class="lessons grid grid-cols-4 gap-3 mt-4">
<div class="ls"><div class="top"><span class="i-pixelarticons-lock" /><i class="pixel">01</i></div><b>Один эталон, неизменяемые ожидания</b><p>ни одно expected не переписывали под код</p></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-checklist" /><i class="pixel">02</i></div><b>У каждого утверждения — класс доказательства</b><p>статика, вывод, дифференциальное сравнение, настоящий рантайм</p></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-robot" /><i class="pixel">03</i></div><b>Оракул может разделять вашу ошибку</b><p>контрольная сумма совпадала с Unicorn — и была неверной</p></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-git-merge" /><i class="pixel">04</i></div><b>Проверка без интеграции — тоже долг</b><p>после успешного сравнения — перенос в <code>native/</code></p></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-archive" /><i class="pixel">05</i></div><b>Провал — это артефакт</b><p>assertion, гарды памяти и таймауты сохраняются</p></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-shield" /><i class="pixel">06</i></div><b>Отказ модели не обходят — и не раздувают</b><p>остановиться, записать, продолжать независимую работу</p></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-tournament" /><i class="pixel">07</i></div><b>Целое — не сумма частей</b><p>692 теста и 215 оракулов не заменили 58 целых матчей</p></div>
<div class="ls"><div class="top"><span class="i-pixelarticons-book-open" /><i class="pixel">08</i></div><b>Правила — не журнал</b><p>инструкции отдельно, статус отдельно</p></div>
</div>

<style>
.lessons { row-gap: 0.85rem; }
.lessons .ls { position: relative; background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: 0.95rem 0.9rem 1rem; overflow: hidden; }
.lessons .ls::before { content: ''; position: absolute; left: 0; top: 0; height: 3px; width: 42px; background: var(--naruto); }
.lessons .top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.65rem; }
.lessons .top span { width: 1.75rem; height: 1.75rem; color: var(--naruto); }
.lessons .top i { font-style: normal; font-size: 0.75rem; color: var(--muted); }
.lessons b { display: block; font-size: 0.9rem; line-height: 1.24; color: var(--ink); font-weight: 700; }
.lessons p { font-size: 0.72rem; line-height: 1.4; color: var(--ink-2); margin: 0.45rem 0 0; }
</style>

<!--
Восемь уроков полностью.
1. Один эталон, неизменяемые ожидания. Ни одно expected не переписывали под код: исправление получает своё доказательство и свой run ID.
2. У каждого утверждения — класс доказательства. Статика, вывод, дифференциальное сравнение, настоящий рантайм. Неизвестное не становится нулём.
3. Оракул может разделять вашу ошибку. Контрольная сумма совпадала с Unicorn байт в байт — и была неверной. Нужен настоящий оригинал.
4. Проверка без интеграции — тоже долг. Две недели доказательств без единой правки в native/ закончились правилом: после успешного сравнения — перенос.
5. Провал — это артефакт. Сохранённые assertion, гарды памяти и таймауты превращают историю проекта в воспроизводимое расследование.
6. Отказ модели не обходят — и не раздувают. Остановиться, записать, продолжать независимую работу; но неизвестный предмет отказа — не запрет на всю сеть.
7. Целое — не сумма частей. 692 теста и 215 оракулов не заменили 58 целых матчей против настоящего оригинала.
8. Правила — не журнал. Свод из 4 954 строк перестал работать как свод. Инструкции отдельно, статус отдельно — и следить, куда утечёт журнал.
-->

---

<Kicker>весь маршрут · 31 марта — 3 октября</Kicker>

# Маршрут пройден

<MetroMap class="mt-2" :visited="13" :current="13" />

<div class="source">даты и цифры — с обложек глав · цвет линии — автор коммитов: git log, трейлер Co-Authored-By</div>

<!--
Та же карта, что в начале: все тринадцать станций пройдены. Пунктир дальше — ветка dev/crossplatform: Linux, Windows, iPad.
-->

---
layout: hero
image: /img/covers/end-valley-of-the-end.jpg
align: center
shade: 0.7
---

<div class="flex flex-col items-center">
<div class="flex items-end gap-6 mb-3">
<Sprite src="/img/sprites/naruto-rasengan-4x.png" :scale="0.75" float />
<Sprite src="/img/sprites/sasuke-chidori-4x.png" :scale="0.75" flip float />
</div>
<Kicker>конец · спасибо</Kicker>
<h1 class="cover-title">Один EXE.<br><span class="hl">Одна и та же игра.</span></h1>
<p class="small ink2" style="max-width: 40rem">Порт и релиз v0.4.0: <span class="mono">github.com/wowlocal/ntsd-2.4</span> · эта презентация: <span class="mono">github.com/wowlocal/ntsd-port-story</span></p>
<p class="xsmall muted" style="max-width: 38rem"><i>Naruto: The Setting Dawn</i> — фанатская игра её авторов на движке <i>Little Fighter 2</i> Марти Вонга и Старски Вонга. Права на контент принадлежат авторам; изображения использованы для рассказа о проекте сохранения игры. Оригинал в эталонных проверках — под CrossOver; отдельные функции — в Unicorn Engine.</p>
</div>

<style>
.cover-title { font-size: 2.8rem !important; line-height: 1.08 !important; margin: 0.3rem 0 0.8rem !important; text-align: center; }
</style>

<!--
Фон — сцена Valley_of_the_End из оригинального дистрибутива (bg/sys/Valley): слои собраны по её bg.dat, кадр водопада — первый из анимации.
-->
