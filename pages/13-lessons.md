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

<div class="grid grid-cols-2 gap-x-6 gap-y-3 mt-3">
<div class="lesson"><span class="n pixel">1</span><div><b>Один эталон, неизменяемые ожидания.</b> Ни одно expected не переписывали под код: исправление получает своё доказательство и свой run ID.</div></div>
<div class="lesson"><span class="n pixel">2</span><div><b>У каждого утверждения — класс доказательства.</b> Статика, вывод, дифференциальное сравнение, настоящий рантайм. Неизвестное не становится нулём.</div></div>
<div class="lesson"><span class="n pixel">3</span><div><b>Оракул может разделять вашу ошибку.</b> Контрольная сумма совпадала с Unicorn байт в байт — и была неверной. Нужен настоящий оригинал.</div></div>
<div class="lesson"><span class="n pixel">4</span><div><b>Проверка без интеграции — тоже долг.</b> Две недели доказательств без единой правки в <code>native/</code> закончились правилом: после успешного сравнения — перенос.</div></div>
<div class="lesson"><span class="n pixel">5</span><div><b>Провал — это артефакт.</b> Сохранённые assertion, гарды памяти и таймауты превращают историю проекта в воспроизводимое расследование.</div></div>
<div class="lesson"><span class="n pixel">6</span><div><b>Отказ модели не обходят — и не раздувают.</b> Остановиться, записать, продолжать независимую работу; но неизвестный предмет отказа — не запрет на всю сеть.</div></div>
<div class="lesson"><span class="n pixel">7</span><div><b>Целое — не сумма частей.</b> 692 теста и 215 оракулов не заменили 58 целых матчей против настоящего оригинала.</div></div>
<div class="lesson"><span class="n pixel">8</span><div><b>Правила — не журнал.</b> Свод из 4 954 строк перестал работать как свод. Инструкции отдельно, статус отдельно — и следить, куда утечёт журнал.</div></div>
</div>

<style>
.lesson { display: grid; grid-template-columns: 2rem 1fr; gap: 0.6rem; align-items: start; font-size: 0.8rem; color: var(--ink-2); line-height: 1.4; }
.lesson b { color: var(--ink); }
.lesson .n { width: 2rem; height: 2rem; display: grid; place-items: center; background: rgba(255,138,61,.14); color: var(--naruto); border-radius: 8px; font-size: 1rem; }
</style>

---
layout: hero
image: /img/menu-back-red-purple.jpg
align: center
shade: 0.72
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
