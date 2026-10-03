---
layout: chapter
num: 10
total: 11
kicker: В цифрах
dates: 7 сентября — 3 октября
image: /img/roster-25-faces-2x.png
imagePixel: false
stats: всё посчитано из git и evidence-файлов порта
---

# В цифрах

Сколько стоит доказанная точность — в строках, мегабайтах и словах.

---

<Kicker>паспорт проекта на 3 октября</Kicker>

# Двенадцать чисел

<div class="grid grid-cols-4 gap-3 mt-3">
<StatTile :value="463" label="коммита с 7 сентября" sub="17 активных дней из 27" />
<StatTile :value="48369" label="строк Swift в самой игре" sub="native/Sources, 329 файлов" accent="var(--s1)" />
<StatTile :value="46852" label="строки Swift-тестов" sub="692 тестовые функции" accent="var(--s1)" />
<StatTile :value="84428" label="строк Python-инструментов" sub="629 файлов, из них 215 оракулов" accent="var(--s3)" />
<StatTile :value="567" label="карточек исследований" sub="539 195 слов — почти «Война и мир» в английском переводе" accent="var(--s4)" />
<StatTile :value="789" label="evidence-файлов" sub="квитанции проверок, отказы, прогоны" accent="var(--s4)" />
<StatTile value="4,6 ГБ" label="эталонных фикстур прямо в git" sub="408 файлов, снятых с оригинала" accent="var(--s1)" />
<StatTile :value="2202" label="строки Swift ссылаются на адреса EXE" sub="код читается как карта оригинала" accent="var(--s2)" />
<StatTile :value="1432985" label="строк добавлено" sub="и лишь 13 550 удалено" />
<StatTile value="202 / 27" label="замороженных плана / исправления" sub="ни один эталон не переписан" accent="var(--s2)" />
<StatTile :value="58" label="целых матчей сверено с оригиналом" sub="и 244 кадра Demo тик в тик" accent="var(--good)" />
<StatTile :value="5" label="отказов моделей в реестрах" sub="у обоих агентов; протокол запрещает обход" accent="var(--s8)" />
</div>

<div class="source">data/summary.json · data/composition.json · data/evidence/*.json · docs/evidence/*safety*.json, *refusal*.json</div>

---

<Kicker>рост кода по дням</Kicker>

# Инструменты и исследования обогнали игру

<GrowthChart class="mt-1" />

<div class="grid grid-cols-3 gap-4 mt-1 small ink2">
<div>На каждую строку игры приходится <b class="hl">1,7 строки</b> Python-инструментов и <b class="hl">1,4 строки</b> карточек исследований.</div>
<div>С 14 по 27 сентября код игры стоял на <b>35 435</b> строках — работа шла в изолированных кандидатах. 28-го — скачок после переноса.</div>
<div>Тесты почти сравнялись с самой игрой: 46 852 строки против 48 369, а их фикстуры весят в 670 раз больше всего кода.</div>
</div>

<div class="source">git ls-tree на последнем коммите каждого дня · data/growth.json</div>

---

<Kicker>объём файлов на HEAD</Kicker>

# Один квадрат — один мегабайт

<BytesScale class="mt-3" />

<p class="small ink2 mt-3">Оранжевые семь квадратиков в левом верхнем углу — весь Swift-код порта вместе с тестами. Синее море — то, против чего этот код проверяется: побайтные записи исполнения оригинального EXE в Unicorn, сжатые и закоммиченные как фикстуры XCTest.</p>

<div class="source">git ls-tree -r -l HEAD · data/composition.json · LFS-файлы дистрибутива не учтены</div>

---

<Kicker>язык коммитов</Kicker>

# От «воспроизвести» к «сыграть»

<VerbShift class="mt-3" />

<p class="small ink2 mt-4">Первый глагол заголовка — хороший индикатор фокуса. До 28 сентября агент <b>воспроизводил, проверял и сохранял</b> провалы; после — <b>записывал, портировал, сверял и играл</b>. В 49 заголовках есть слово Preserve, из них 13 — вместе с failure: все из первой эпохи.</p>

<div class="source">git log --format=%s · data/verbs.json</div>

---

<Kicker>два агента — два почерка</Kicker>

# Codex и Claude в одном репозитории

<div class="grid grid-cols-[1.35fr_1fr] gap-6 mt-2">
<div class="tight">

| | Codex · GPT-6 Astra | Claude Opus 5.5 | Codex параллельно |
| --- | ---: | ---: | ---: |
| период | 7–27 сентября | 28 сен — 3 окт | 1–3 октября |
| коммитов | **327** | **120** | **16** |
| медианный интервал | 27,7 мин | 30,0 мин | 19,3 мин |
| коммитов ночью (00–06) | 20 % | 22 % | 0 % |
| с телом сообщения | 34 % | **100 %** | 69 % |
| префикс `feat:` и т. п. | 116 | 0 | 3 |
| «remain open» в теле | 72 из 327 | 0 из 120 | 6 из 16 |

</div>
<div class="small ink2">

**Codex** начинал с Conventional Commits (`feat: reproduce original …`), потом перешёл на «Recover / Verify / Preserve …». Стилистический отпечаток — числа, приклеенные к словам: *first25 methods passed, method26 failed*.

**Claude** формулирует через результат для игрока: *Play War in the app*, *Demo mode plays in the app*; в теле — «Checks:» и обязательная строка про пересчёт метрики.

<div class="card-soft mt-2">Кризисы были у обоих. 27 сентября у Codex затянулись проверки без интеграции — их ограничили правилами прогресса. 2 октября Claude оставил передачу «заблокированы все направления» — параллельный агент заменил её конкретной задачей: <span class="mono xsmall">"Replace the unsupported all-directions-blocked handoff"</span> (<code>2d6a7e5</code>).</div>

</div>
</div>

<div class="source">git log · data/summary.json · d2c6eef · 2d6a7e5 · 007c007</div>

---

<Kicker>токены · из журналов сессий Codex и Claude Code</Kicker>

# 6,3 миллиарда токенов

<div class="grid grid-cols-4 gap-3 mt-2">
<StatTile value="6,28 млрд" label="токенов обработали модели за порт" sub="Codex 3,52 млрд · Claude 2,76 млрд" size="sm" />
<StatTile value="25,7 млн" label="токенов модели написали сами" sub="код, карточки, вызовы инструментов, рассуждения" accent="var(--s2)" size="sm" />
<StatTile :value="31095" label="ответ модели" sub="25 141 у Codex · 5 954 у Claude" accent="var(--s1)" size="sm" />
<StatTile value="967 тыс." label="самый большой контекст одного запроса" sub="у Claude; у Codex — 256 тыс. из окна 258 тыс." accent="var(--s3)" size="sm" />
</div>

<TokenDays class="mt-2" />

<div class="grid grid-cols-3 gap-4 mt-1 small ink2">
<div>Пик — <b class="hl">29 сентября</b>, день «все режимы за один день»: Claude обработал 903 млн токенов.</div>
<div>На коммит: <b>10,3 млн</b> токенов у Codex и <b>23 млн</b> у Claude — у второго окно контекста почти вчетверо больше.</div>
<div>Эта презентация — ещё <b>260 млн</b> токенов: 4 % от всего порта.</div>
</div>

<div class="source">журналы ~/.codex/sessions (33 сессии) и ~/.claude/projects · scripts/collect_tokens.py · data/tokens.json</div>

---

<Kicker>структура токенов</Kicker>

# Из 1 000 токенов модель пишет шесть

<TokenUnits class="mt-3" />

<div class="grid grid-cols-3 gap-4 mt-4 small ink2">
<div><b>97–99 % ввода — кэш.</b> Агент снова и снова перечитывает один и тот же длинный контекст: правила, карточки, вывод инструментов.</div>
<div><b>Рассуждения Codex</b> — 7,25 млн токенов, треть всего его вывода. Почти все ответы — на усилии <span class="mono">xhigh</span> (20 374 из 25 141).</div>
<div><b>На строку Swift-кода игры</b> приходится ~130 тыс. обработанных токенов — и ~530 написанных моделью.</div>
</div>

<div class="source">data/tokens.json · scripts/collect_tokens.py</div>

---

<Kicker>прогнозы против факта</Kicker>

# Сколько ещё осталось?

<div class="grid grid-cols-3 gap-4 mt-3">
<div class="card">
<div class="pixel hl small">8 сентября, 22:39</div>
<p class="small ink2">«Около <b>250 часов</b> продолжения работы; осторожный сценарий — около 500». В календаре — «около двух недель, с резервным сценарием около трёх».</p>
<div class="xsmall muted">прежние устные «1–3 месяца» прямо названы «не расчётом»</div>
</div>
<div class="card">
<div class="pixel hl small">27 сентября, 09:49</div>
<p class="small ink2">«<b>1–3 недели</b> до первого проверенного Наруто/Саске матча в приложении; 6–12 недель до полного порта».</p>
<div class="xsmall muted">метрика «доли .text» к тому дню две недели стояла на 52,87 %</div>
</div>
<div class="card" style="border-color: rgba(255,138,61,.5)">
<div class="pixel hl small">факт</div>
<p class="small ink2"><b>28 сентября</b> — матч в приложении до KO и Summary. <b>29-го</b> — все режимы. <b>2–3 октября</b> — 58 целых матчей сверены с оригиналом.</p>
<div class="xsmall muted">полный порт не закончен: сеть, турниры целиком, CRAZY! и дальние фазы Stage открыты</div>
</div>
</div>

<div class="card-soft mt-4 small ink2">
Метрику тоже проверяли. Оценку до исправления парсера сохранили рядом с исправленной (41,41 % → 48,79 %, тот же коммит), а аудит 3 октября заключил: процент «не измеряет готовность порта» — и новый процент готовности объявлять не стал.
</div>

<div class="source">docs/estimates/2026-09-08-code-progress.md · 2026-09-10-code-progress-before-parser-fix.json · 2026-09-27-code-progress.md · f9ee219</div>

---

<Kicker>как проверяется порт</Kicker>

# Пирамида проверок

<div class="mt-4">
<ValidationPyramid />
</div>

<p class="small ink2 mt-4 text-center">Чем выше слой, тем меньше в нём случаев — и тем ближе он к тому, что видит игрок. Ни один слой не заменяет другой: «целое — не сумма частей».</p>

<div class="source">data/evidence/validation-layers.json · tools/app_e2e.py · docs/research/APPLICATION_SOAKS.md · docs/research/CROSSPLAY_MATRIX.md</div>
