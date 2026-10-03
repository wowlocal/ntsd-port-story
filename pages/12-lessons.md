---
layout: chapter
num: 12
total: 12
kicker: Эпилог
dates: 3 октября и дальше
image: /img/stage-1-1-background.jpg
stats: что осталось · чему научились
---

# Уроки

Порт ещё не закончен. Но методика уже доказала главное: агенты могут восстанавливать сложное поведение, не угадывая.

---

<Kicker>честный статус</Kicker>

# Что осталось

<div class="grid grid-cols-3 gap-4 mt-3 small">
<div class="card">
<div class="pixel small" style="color: var(--s4)">объявленные отличия</div>

- Текст, который оригинал рисует через Windows GDI, — системным шрифтом macOS вместо `SYSTEM_FONT`; позиция, размер и цвет те же.
- Музыка Demo — объявленная замена треку, который оригинал выбирает по «мусорному» регистру.

</div>
<div class="card">
<div class="pixel small" style="color: var(--s8)">ещё не сверено с оригиналом</div>

- Турниры целиком.
- Stage дальше первой фазы каждой группы.
- Скрытая сложность *CRAZY!*.
- Игра по сети с настоящей Windows.
- Demo после тика 879: расхождение в перепроверке не локализовано.

</div>
<div class="card">
<div class="pixel hl small">следующий шаг</div>

- Подписанный и нотаризованный релиз: скрипт уже есть в ветке `work/goal-100` (`74be317`, 3 октября, 16:44), в `main` не влит.
- Режимы разработчика 1 и 2 (`F2`, `F3`) — единственный код игры, который сознательно не переносили.
- Чистый Mac: приёмка на машине без инструментов разработки.

</div>
</div>

<div class="source">README.md · docs/GOAL_100.md · docs/research/CROSSPLAY_MATRIX.md · 74be317</div>

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
<p class="small ink2" style="max-width: 34rem">Порт: <span class="mono">ntsd-2.4</span> · эта презентация: <span class="mono">github.com/wowlocal/ntsd-port-story</span></p>
<p class="xsmall muted" style="max-width: 38rem"><i>Naruto: The Setting Dawn</i> — фанатская игра её авторов на движке <i>Little Fighter 2</i> Марти Вонга и Старски Вонга. Права на контент принадлежат авторам; изображения использованы для рассказа о проекте сохранения игры. Оригинал в эталонных проверках — под CrossOver; отдельные функции — в Unicorn Engine.</p>
</div>

<style>
.cover-title { font-size: 2.8rem !important; line-height: 1.08 !important; margin: 0.3rem 0 0.8rem !important; text-align: center; }
</style>
