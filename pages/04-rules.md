---
layout: chapter
num: 4
total: 12
kicker: Глава четвёртая
dates: 12–14 сентября
image: /img/menu-back-red-purple.jpg
stats: AGENTS.md 4 954 → 153 строки · WORKFLOW.md · реестр отказов
---

# Свод правил

Пять дней правила копились в одном файле вместе с отчётами о статусе. Утром 12 сентября их отделили от журнала — так появилась методология.

<!--
Переход: агент работает быстро, но правила превратились в ленту новостей. Здесь рождается методология, которая дальше станет главным героем.
-->

---

<Kicker>эволюция свода правил</Kicker>

# Правила, которые выросли в журнал

<RulebookChart />

<div class="grid grid-cols-3 gap-4 mt-1 small ink2">
<div><b class="hl">167 из 175</b> коммитов до 12 сентября правили <code>AGENTS.md</code>: правил там было ~90 строк, остальное — датированные абзацы «что сделано».</div>
<div><b class="hl">ffe16f4</b>, 12 сен: файл сжат в 32 раза, а старый сохранён как неизменяемый архив с закреплённым SHA-256. Рядом появились <code>WORKFLOW.md</code> и шаблон задачи.</div>
<div><b class="hl">Эффект водяной кровати:</b> журнал переехал в соседние файлы — <code>CURRENT_WORK</code> вырос с 101 до 2 422 строк, <code>RESEARCH_MAP</code> — до 3 596.</div>
</div>

<div class="source">git log -- AGENTS.md docs/research/CURRENT_WORK.md docs/RESEARCH_MAP.md · data/rulebook.json</div>

<!--
Шкала — строки файла после каждого коммита, который его трогал. Пик 4 954 строки (364 КБ) — 12 сентября в 02:55. Через шесть часов — 153 строки.
-->

---

<Kicker>принципы</Kicker>

# Семь фраз, на которых держится порт

<div class="grid grid-cols-2 gap-3 mt-3">

<div class="card-soft">
<div class="mono small hl">Do not guess physics, combo timing, damage, AI, randomness or standard engine behavior.</div>
<div class="xsmall muted mt-1">Не угадывать: числа, порядок операций, знаковость и переполнения — как в EXE. · AGENTS.md</div>
</div>

<div class="card-soft">
<div class="mono small hl">No unobserved storage becomes known zero.</div>
<div class="xsmall muted mt-1">Неизвестный байт остаётся неизвестным, пока не доказано его происхождение. · AGENTS.md</div>
</div>

<div class="card-soft">
<div class="mono small hl">Never change an old expected value or exclude a mismatch to accept a candidate.</div>
<div class="xsmall muted mt-1">Эталоны неизменны; исправление получает собственное доказательство. · AGENTS.md</div>
</div>

<div class="card-soft">
<div class="mono small hl">Native rejection with rollback is not a successful match to a source fault.</div>
<div class="xsmall muted mt-1">Откат порта там, где оригинал падает, — это не совпадение. · AGENTS.md</div>
</div>

<div class="card-soft">
<div class="small"><b>«Код выхода процесса 0 означает только завершение процесса».</b></div>
<div class="xsmall muted mt-1">Зелёный exit code — не приёмка. · WORKFLOW.md</div>
</div>

<div class="card-soft">
<div class="small"><b>«Мнение LLM и структурное сходство кода не заменяют сравнение поведения».</b></div>
<div class="xsmall muted mt-1">Модель — не компаратор. · WORKFLOW.md</div>
</div>

</div>

<div class="card mt-3 text-center">
<span class="small"><b>«Нельзя выводить полную корректность матча из суммы успешно проверенных функций».</b></span> <span class="xsmall muted">· WORKFLOW.md</span>
</div>

---

<Kicker>классы доказательств</Kicker>

# Лестница доказательств

<div class="grid grid-cols-[1.35fr_1fr] gap-6 mt-2">
<EvidenceLadder />
<div class="small ink2">

У каждого утверждения в карточке есть класс. В карте исследований это сокращено до шкалы **S / D / W**:

- **S** — статическое наблюдение в дизассемблере;
- **D** — сравнение с выполнением оригинальных инструкций;
- **W** — воспроизводимая проверка целой игры в Windows.

<div class="card-soft mt-3">
<div class="xsmall muted">из RESEARCH_MAP.md</div>
<div class="small">«W пока отсутствует».</div>
</div>

Настоящей Windows-машины в проекте так и не появилось: роль «реального мира» в конце сыграл оригинал под CrossOver — и он нашёл то, чего не видел ни один оракул.

</div>
</div>

<!--
Это важно для финала: история с контрольной суммой каталога (глава 8) — пример, когда D-уровень дал ложное совпадение, потому что оракул и порт разделяли одну модель CRT.
-->

---

<Kicker>исходы и гейты</Kicker>

# Семь исходов вместо «прошло / упало»

<Outcomes />

<div class="mt-5">
<div class="xsmall muted mb-2">четыре отдельных гейта приёмки — каждый записывается один раз для закреплённых байтов</div>
<div class="grid grid-cols-4 gap-3">
<div class="card-soft"><span class="pixel hl">1</span> <b class="small">эталон и аудит опубликованы</b><div class="xsmall muted">source / audit publication</div></div>
<div class="card-soft"><span class="pixel hl">2</span> <b class="small">тесты Native</b><div class="xsmall muted">сравнение с expected и масками</div></div>
<div class="card-soft"><span class="pixel hl">3</span> <b class="small">байты пакета</b><div class="xsmall muted">package byte verification</div></div>
<div class="card-soft"><span class="pixel hl">4</span> <b class="small">архив проверен</b><div class="xsmall muted">archive verification</div></div>
</div>
</div>

<div class="source">AGENTS.md · docs/research/WORKFLOW.md · docs/research/PROGRESS_RULES.md</div>

---

<Kicker>роли</Kicker>

# Кто имеет право сказать «готово»

<div class="grid grid-cols-3 gap-4 mt-3">
<div class="card">
<div class="pixel hl">исполнитель</div>
<p class="small ink2">Пишет кандидат и запускает проверки. Не правит expected «под свой код» и не называет своё ревью независимым.</p>
<div class="mono xsmall muted">"do not label author self-review independent"</div>
</div>
<div class="card">
<div class="pixel hl">независимый ревьюер</div>
<p class="small ink2">Read-only. Смотрит исходные доказательства, «не только объяснение автора». Если ревьюера нет — это записывается как открытый гейт.</p>
<div class="mono xsmall muted">449 упоминаний «independent review» в 226 карточках</div>
</div>
<div class="card">
<div class="pixel hl">компаратор</div>
<p class="small ink2">Детерминированная программа: неизменяемые ожидаемые результаты и маски определённости. Последнее слово — за ним.</p>
<div class="mono xsmall muted">байты + маски, а не мнение модели</div>
</div>
</div>

<div class="grid grid-cols-2 gap-4 mt-4 small ink2">
<div>

**Политика моделей.** Сильная модель — для неизвестных контрактов. Меньшая может исполнять уже определённые задачи, но «не вправе ослаблять маски, изменять expected или расширять область принятия».

</div>
<div>

**Реальные ревью.** 30 сентября три независимые проверки: кадры за пределами Object (*"three errors, all confirmed"*), CONTROL SETTINGS и джойстики (4 проблемы), Tournament (дефектов нет). 2 октября — ревью сети: одно замечание P2, исправлено.

</div>
</div>

<div class="source">docs/research/WORKFLOW.md · 7bf3624 · 9a45779 · cf50bf4 · docs/evidence/network-review-20261002.json</div>

---

<Kicker>отказы модели</Kicker>

# Когда модель говорит «нет»

<div class="grid grid-cols-[0.95fr_1.5fr] gap-6 mt-1">
<div class="small">

<div class="xsmall muted mb-1">протокол из WORKFLOW.md</div>

1. **Записать** точный ответ, время, модель, операцию и логи. Нет вывода — так и написать.
2. **Остановить** автоповторы: никакой смены модели, новой сессии, дробления или переименования команды.
3. **Проверить** живые процессы, не останавливая исследование целиком.
4. **Оставить** зависимость открытой и продолжать независимую работу.
5. **Подготовить** пакет для поддержки — без отправки без человека.

</div>
<div>

| дата | агент | что делалось | реакция |
| --- | --- | --- | --- |
| 9 сен | Codex | оракул записи результата раунда | раздел о целях проверок и протокол |
| 9 сен | Codex | запись Actor за пределы 0x420 | инцидент открыт, повторы запрещены |
| 12 сен | Codex | ошибки ресурсов War, NULL в Unicorn | доделано по уже сохранённым данным |
| 26 сен | Codex, Computer Use | доступ к окну терминала | не повторять через другой инструмент |
| 1 окт | Claude Code | сетевая интеграция | сеть отложена; 2 окт — запрет сужен |

<div class="xsmall muted mt-1">Во всех пяти записях <span class="mono">exactTriggerKnown: false</span>: связь с конкретным действием не установлена. «Сохранённые ошибки не доказывают ни нарушение пользователя, ни ложность решения».</div>

</div>
</div>

<div class="source">docs/evidence/codex-safety-incidents-2026-09-12.json · codex-cua-ghostty-refusal-2026-09-26.json · claude-code-network-safety-2026-10-01.json · a4fb48c</div>

<!--
Урок 2 октября: агент распространил отказ на всю сеть, хотя предмет отказа неизвестен. Коммит a4fb48c «Correct overstated networking hold» вернул сеть в работу — и в тот же день два приложения сыграли сетевой матч.
-->

---

<Kicker>процессы и диски</Kicker>

# Не трогай живой процесс

<div class="grid grid-cols-3 gap-4 mt-3">
<StatTile :value="13.6" :decimals="1" suffix="ч" label="непрерывный Unicorn-захват каталога (PID 59727)" sub="упомянут в 115 карточках, ни разу не перезапущен и не получил ни одного сигнала" accent="var(--s1)" />
<StatTile :value="7.046" :decimals="3" suffix="с" label="перенос живого продюсера на другой диск" sub="SIGSTOP → копия → проверка → symlink → SIGCONT" accent="var(--s2)" />
<StatTile :value="40" suffix="ГиБ" label="неприкосновенный резерв на каждом томе" sub="X5 (APFS, клоны кандидатов) и T7 (ExFAT, архивы)" accent="var(--s3)" />
</div>

<div class="grid grid-cols-2 gap-4 mt-5">
<div class="card-soft">
<div class="mono small hl">Revalidate PID, process start time, command, cwd and job record before acting.</div>
<div class="xsmall muted mt-1">Перед любым действием — убедиться, что это тот самый процесс.</div>
</div>
<div class="card-soft">
<div class="mono small hl">Never restart a completed capture or a live job for silence.</div>
<div class="xsmall muted mt-1">Тихий лог, компакция контекста или отказ модели не значат, что процесс умер.</div>
</div>
</div>

<div class="grid grid-cols-3 gap-4 mt-3 small ink2">
<div><b>Один оригинал за раз.</b> Драйвер держит блокировку и закрывает чужие экземпляры клона; процесс драйвера не убивают сигналом в обход.</div>
<div><b>Только свои процессы.</b> SIGTERM — после перепроверки PID и времени старта; «reaped −15» записывается отдельным исходом.</div>
<div><b>Случай 2 октября.</b> Хелпер отправил два нажатия J и два клика в сетевой матч параллельного агента. Записано в инцидент, фильтр окон ужесточён.</div>
</div>

<div class="source">AGENTS.md · docs/research/WORKFLOW.md · docs/CROSSPLAY_LOOP.md · 90f6b7b</div>

---

<Kicker>диск · из карточек и журналов агентов</Kicker>

# Когда закончился диск

<div class="xsmall ink2 mt-1"><b>Ночь на 11 сентября</b> · свободное место на внутреннем SSD Mac mini (время московское)</div>
<DiskTimeline from="2026-09-10T18:00Z" to="2026-09-11T12:30Z" :y-max="70" :volumes="['internal']" :height="165" hour-ticks
  :ticks="['2026-09-10T21:00Z', '2026-09-11T00:00Z', '2026-09-11T03:00Z', '2026-09-11T06:00Z', '2026-09-11T09:00Z', '2026-09-11T12:00Z']"
  :guards="[{ v: 6.44, label: 'гард 6 GiB: здесь захват останавливается' }]"
  :notes="[
    { t: '2026-09-10T21:21Z', v: 67.6, text: '67,6 ГБ свободно', dx: 8, dy: -6 },
    { t: '2026-09-11T02:30Z', v: 44, text: '−62 ГБ: трасса каталога за ночь', dx: 8, dy: 0 },
    { t: '2026-09-11T08:59Z', v: 33, text: '+16 ГБ: дубли → APFS-клоны', dx: -10, dy: 0, anchor: 'end' },
    { t: '2026-09-11T10:46Z', v: 9.5, text: '→ X5', dx: 8, dy: -6 },
  ]" />

<div class="xsmall ink2 mt-1"><b>Дальше</b> · внутренний SSD и внешний X5 до 3 октября</div>
<DiskTimeline from="2026-09-11T00:00Z" to="2026-10-04T00:00Z" :y-max="260" :height="165"
  :ticks="['2026-09-14T09:00Z', '2026-09-21T09:00Z', '2026-09-28T09:00Z', '2026-10-03T09:00Z']"
  :markers="[{ t: '2026-09-26T07:21Z', label: '+ T7: 2 ТБ ExFAT для трасс и архивов' }]"
  :notes="[
    { t: '2026-09-11T10:46Z', v: 244.8, text: 'X5: 244,8 ГБ свободно', dx: 8, dy: 4 },
    { t: '2026-09-22T17:48Z', v: 66.6, text: 'удалены старые сборки Codex', dx: -8, dy: -8, anchor: 'end' },
    { t: '2026-10-03T16:00Z', v: 48.6, text: 'X5: 48,6 ГБ — занято 98 %', dx: -10, dy: -20, anchor: 'end' },
  ]" />

<div class="source">APPLICATION_CATALOG_PLAN.md · APPLICATION_CATALOG_TRACE_STORAGE.md · LIB_SELECTION_COMMANDS.md · карточки валидаций 22–27 сентября · df/diskutil 3 октября · data/storage.json</div>

<!--
11 сентября утром Unicorn-захват каталога остановился на гарде 6 GiB: за ночь трассы съели ~62 ГБ. Агент не стал ничего удалять — нашёл 15,8 ГБ побайтно одинаковых трасс и заменил копии APFS-клонами. Через полтора часа новый захват снова съел 15 ГБ, и его на ходу перенесли на внешний диск за 7 секунд.
-->

---

<Kicker>куда ушли терабайты</Kicker>

# Клоны, которых не видно в du

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2">
<div>

<div class="xsmall muted mb-2">занято на 3 октября, ГиБ (по du)</div>
<div class="sizes">
<div class="srow"><span class="sl">X5: исследовательские папки агентов</span><span class="st"><i style="width: 100%" /></span><span class="sv">2 032</span></div>
<div class="srow"><span class="sl">папка <code>build/</code> в репозитории</span><span class="st"><i style="width: 9.85%" /></span><span class="sv">200</span></div>
<div class="srow sub"><span class="sl">— из них трассы и отчёты задач</span><span class="st"><i style="width: 6.07%" /></span><span class="sv">123</span></div>
<div class="srow sub"><span class="sl">— 23 отдельные Swift-сборки задач</span><span class="st"><i style="width: 1.68%" /></span><span class="sv">34</span></div>
<div class="srow"><span class="sl">T7: архивы и трассы</span><span class="st"><i style="width: 0.78%" /></span><span class="sv">16</span></div>
<div class="srow"><span class="sl"><code>native/.build</code></span><span class="st"><i style="width: 0.47%" /></span><span class="sv">9,6</span></div>
<div class="srow"><span class="sl">весь <code>.git</code> (включая 4,3 ГиБ фикстур)</span><span class="st"><i style="width: 0.22%" /></span><span class="sv">4,5</span></div>
<div class="srow"><span class="sl">журналы сессий Codex</span><span class="st"><i style="width: 0.19%" /></span><span class="sv">3,8</span></div>
</div>

<div class="card-soft mt-3 small ink2">du насчитывает <b>≈2 ТиБ</b> исследовательских данных на X5 — больше, чем весь диск (1,82 ТиБ). Так du считает клоны: каждый — как отдельный файл, хотя блоки у них общие.</div>

<div class="card-soft mt-2 xsmall ink2">Вечером 11 сентября X5 отвалился, и два WIP-коммита ждали диск: <span class="mono">"Never recapture the completed original corpus to replace unavailable storage."</span></div>

</div>
<div class="small ink2">

<div class="card">
<div class="pixel hl small">ход агента</div>
<p class="mb-0">APFS-клон — копия файла, которая делит блоки с оригиналом, пока её не изменят. Утром 11 сентября агент сверил трассы побайтно и заменил <b>125 292 одинаковые копии</b> клонами <b>42 174</b> канонических файлов: +16 ГБ, а все байты, SHA, пути, права и время изменения остались. «Нет ни перекодирования, ни логического удаления».</p>
</div>

- Кандидаты кода тоже клонировались: неизменённые файлы — без копирования, с проверкой байтов.
- T7 — ExFAT, клонов там нет: туда трассы, отчёты и архивы, а сборки остаются на X5.
- Резервы 6 GiB на SSD и 40 GiB на X5 и T7 не снижаются; доказательства ради места не удаляются.

</div>
</div>

<div class="source">APPLICATION_CATALOG_PLAN.md · APPLICATION_CATALOG_TRACE_STORAGE.md · 13f48b1 · 3ab0ada · du/df 3 октября</div>

<style>
.sizes { display: flex; flex-direction: column; gap: 0.35rem; }
.srow { display: grid; grid-template-columns: 13.5rem 1fr 2.6rem; align-items: center; gap: 0.5rem; }
.srow .sl { font-size: 0.66rem; color: var(--ink); line-height: 1.2; }
.srow.sub .sl { color: var(--ink-2); padding-left: 0.6rem; }
.srow .st i { display: block; height: 10px; min-width: 3px; background: var(--s2); border-radius: 0 4px 4px 0; }
.srow.sub .st i { background: rgba(217,89,38,0.55); }
.srow .sv { font-size: 0.7rem; font-weight: 650; color: var(--ink); text-align: right; font-variant-numeric: tabular-nums; }
</style>

---

<Kicker>12 сентября, 10:13–14:23 · побочная линия</Kicker>

# Соблазн готового движка

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2">
<div>

Обзор 13 открытых движков LF2 (`fbfc3c0`) рекомендовал попробовать **L2DF** на LÖVE: бюджет «1–2 инженерных дня». Прототип подняли в отдельном worktree.

<Timeline dense :items="[
  { time: '10:13', title: 'Isolated native L2DF prototype with verified macOS package', hash: 'a642bfa' },
  { time: '10:28', title: 'Port DAT input combos and resource transfers', hash: 'cb8f723' },
  { time: '12:00', title: 'Verified five-needle combat into native L2DF Practice', hash: '4778284' },
  { time: '12:48', title: 'Verified native Swift bridge with owned Actor storage', hash: '284d69d', hot: true },
  { time: '14:23', title: 'Retain native first front menu return — последний коммит ветки', hash: '5244666' },
]" />

<p class="small ink2 mt-2">12 коммитов, 58 файлов, +9 636 строк. Физику и бой L2DF пришлось заменить своими, а к обеду ветка стала просто оболочкой вокруг Swift-ядра — и её оставили.</p>

</div>
<div>

<div class="card">
<div class="pixel hl small">почему чужие импортёры не годятся</div>
<p class="small ink2">Повторный <code>&lt;frame&gt;</code> в DAT у оригинала <b>дописывает</b> поля. У Наруто кадр 123 определён дважды: 318 определений дают 317 кадров. Конвертер F.LF после повторного определения оставляет только <code>name: second, pic: 2</code> — <code>wait</code> и <code>next</code> теряются.</p>
</div>

<div class="card mt-3">
<p class="small ink2 mb-0">Незакрытый <code>itr:</code> в кадре 48 куная съедает кадр 49. Оригинал загружает 58 определений; L2DF вкладывает кадры 49–55, 60–64, 70–72 и 399 внутрь 48 — <b>43 записи верхнего уровня вместо 58</b>.</p>
</div>

</div>
</div>

<div class="source">fbfc3c0 · docs/research/LF2_OPEN_SOURCE_ENGINES.md · ветка codex/l2df-native-prototype</div>

---

<Kicker>13–14 сентября</Kicker>

# Первый урон — и восемь дней тишины

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-2">
<div class="small ink2">

13–14 сентября — 39 коммитов: собственная загрузка каталога, цикл приложения, выбор персонажей, Start, затем «активный» бой по стадиям — ввод, физика, контакты, HUD, запись, вывод.

Но в 48 активных вызовах **никто не получал урона**: стартовая защита падала с 58 до 10, а HP оставался 500 (`3de9cc9`). Понадобилась отдельная диагностика.

<div class="card-soft mt-3">
<div class="mono xsmall hl">"Это проверенная Native-диагностика; новые damaging calls ещё не сравнены с оригиналом."</div>
<div class="xsmall muted mt-1">FIRST_DAMAGE_DIAGNOSTIC.md · be3d407 · 14 сентября, 12:05</div>
</div>

</div>
<div>

| атакующий | вызовов | защита ушла на | HP защитника |
| --- | ---: | ---: | --- |
| Наруто | 91 | 58 | 500 → **480** → 481 |
| Саске | 93 | 58 | 500 → **485** → 485 |

<p class="xsmall muted">У Наруто удар — кадр 63, ITR 0, kind 0: −20 HP, а на шаге жизненного цикла HP восстанавливается на единицу.</p>

<div class="card mt-3" style="border-style: dashed">
<div class="pixel small muted">14 → 22 сентября</div>
<p class="small ink2 mb-0">Следующий коммит появится через <b>196,5 часа</b>. 22 сентября первым делом появится правило: делать коммит после каждого проверенного шага.</p>
</div>

</div>
</div>

<div class="source">3de9cc9 · be3d407 · docs/research/FIRST_DAMAGE_DIAGNOSTIC.md · 5b7e63d</div>
