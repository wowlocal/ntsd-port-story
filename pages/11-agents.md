---
layout: chapter
num: 11
total: 12
kicker: Глава одиннадцатая
dates: журналы сессий
image: /img/screens/12-all-17-backgrounds-grid.jpg
stats: 34 сессии · 31 095 ответов моделей · 1 101 ход · 6,3 млрд токенов
---

# Под капотом агентов

Что записали сами агенты: модели и effort, автопилот против человека, терминал, лимиты и токены.

<!--
Источник главы — локальные журналы сессий Codex (~/.codex/sessions) и Claude Code (~/.claude/projects). Скрипты берут только счётчики, модели, время и тип сообщения; текст переписки не сохраняется.
-->

---

<Kicker>модели и усилие</Kicker>

# На чём это делалось

<div class="grid grid-cols-2 gap-5 mt-2">
<div class="card">
<div class="flex justify-between items-baseline"><span class="pixel hl">Codex</span><span class="xsmall muted">7 сентября — 3 октября · 25 141 ответ</span></div>
<div class="display mt-1" style="font-size: 1.3rem">GPT-6 Astra <span class="small muted" style="font-family: var(--font-sans)">· 99,4 % ответов</span></div>
<EffortBar class="mt-2" :parts="[
  { label: 'xhigh', n: 20243, color: 'var(--s1)' },
  { label: 'high', n: 4667, color: 'var(--s3)' },
  { label: 'medium + low', n: 74, color: 'var(--s4)' },
]" />
<p class="xsmall ink2 mt-2 mb-1">12 сентября в 19:07 UTC основная сессия перешла с <b>xhigh</b> на <b>high</b> — через 17 минут после того, как короткая сессия-советник разобрала 48 часов работы и предложила снизить effort. С 22 сентября — снова xhigh.</p>
<p class="xsmall muted mb-0">Помощники для оценок и правки промптов: GPT-6 Sol (86 ответов), GPT-5.6 Sol (54), GPT-5.6 Terra (13).</p>
</div>
<div class="card">
<div class="flex justify-between items-baseline"><span class="pixel hl">Claude Code</span><span class="xsmall muted">28 сентября — 3 октября · 5 954 ответа</span></div>
<div class="display mt-1" style="font-size: 1.3rem">Claude Opus 5.5 <span class="small muted" style="font-family: var(--font-sans)">· 100 % ответов</span></div>
<EffortBar class="mt-2" :parts="[{ label: 'xhigh', n: 5954, color: 'var(--s2)' }]" />
<p class="xsmall ink2 mt-2 mb-1">Effort задан одной командой <span class="mono">/effort xhigh</span> 28 сентября в 11:25 UTC — за шесть минут до первого коммита — и больше не менялся. Окно контекста — до 967 тыс. токенов.</p>
<p class="xsmall muted mb-0">Эта презентация — тоже Opus 5.5, но с effort <b>max</b>.</p>
</div>
</div>

<div class="card-soft mt-4 small ink2">
<b>Режим работы.</b> Codex в 1 104 из 1 128 контекстов хода работал с <span class="mono">approval: never</span> и <span class="mono">sandbox: danger-full-access</span>; Claude Code — в режиме <span class="mono">bypassPermissions</span>. Агенты не спрашивали разрешений: всё, что их сдерживало, — правила в репозитории.
</div>

<div class="source">~/.codex/sessions: turn_context (model, effort, approval, sandbox) · ~/.claude/projects: /effort, permissionMode · data/sessions.json</div>

---

<Kicker>34 сессии на одной оси</Kicker>

# Кто и когда работал

<SessionGantt class="mt-1" />

<div class="grid grid-cols-3 gap-4 mt-2 small ink2">
<div><b>12 сентября</b> — день субагентов: семь сессий-помощников Codex, в том числе прототип L2DF в отдельном worktree.</div>
<div><b>Claude работал одной сессией</b> шесть дней подряд: 5 954 ответа, 9 компакций контекста и 10 субагентов для ревью.</div>
<div><b>1–3 октября</b> — два агента одновременно: Claude сверял игру с оригиналом, Codex доводил сеть.</div>
</div>

<div class="source">data/sessions.json · scripts/collect_sessions.py</div>

---

<Kicker>автопилот и человек</Kicker>

# Кто нажимал Enter

<div class="grid grid-cols-2 gap-5 mt-2">
<div>
<div class="pixel hl small mb-2">Codex · /goal</div>
<div class="grid grid-cols-2 gap-3">
<StatTile :value="383" label="автопродолжения /goal" sub="8 запусков цели, 129,5 часа автопилота" size="sm" accent="var(--s1)" />
<StatTile :value="163" label="сообщения человека" sub="за 20 дней работы" size="sm" accent="var(--s1)" />
<StatTile :value="820" label="ходов" sub="медиана 9,3 мин, самый длинный — 8,4 ч" size="sm" accent="var(--s1)" />
<StatTile :value="299" label="компакций контекста" sub="окно — 258 тыс. токенов" size="sm" accent="var(--s1)" />
</div>
</div>
<div>
<div class="pixel hl small mb-2">Claude Code · /loop</div>
<div class="grid grid-cols-2 gap-3">
<StatTile :value="60" label="итераций /loop" sub="и 55 пробуждений по таймеру" size="sm" accent="var(--s2)" />
<StatTile :value="25" label="сообщений человека" sub="за 6 дней работы" size="sm" accent="var(--s2)" />
<StatTile :value="281" label="ход" sub="медиана 0,9 мин, самый длинный — 4,4 ч" size="sm" accent="var(--s2)" />
<StatTile :value="9" label="компакций контекста" sub="каждая — с ~967 тыс. до 11–36 тыс. токенов" size="sm" accent="var(--s2)" />
</div>
</div>
</div>

<div class="card-soft mt-4 small ink2">
<b>241 час</b> ходов у Codex и <b>43,5 часа</b> у Claude. На одно сообщение человека приходилось ~2,3 автопродолжения у Codex и ~4,6 итерации и пробуждения у Claude. Длинные ходы Codex и короткие у Claude — разные режимы: <span class="mono">/goal</span> держит одну задачу часами, <span class="mono">/loop</span> просыпается, делает шаг и засыпает.
</div>

<div class="source">~/.codex/sessions: task_started/complete, compacted, сообщения goal · ~/.claude/projects: turn_duration, compact_boundary, scheduled_task_fire · data/sessions.json</div>

---

<Kicker>память агента</Kicker>

# Как агент «дышит» контекстом

<div class="xsmall ink2 mt-1"><i class="swatch" style="background: var(--s2)" /><b>Claude Opus 5.5</b> · сессия 28 сентября — 3 октября · 5 257 запросов · 9 автосжатий · медиана контекста 492 тыс. токенов</div>
<ContextBreath agent="claude" :height="150" />

<div class="xsmall ink2 mt-1"><i class="swatch" style="background: var(--s1)" /><b>Codex · GPT-6 Astra</b> · первая сессия 7–9 сентября, ночной спринт · 4 057 запросов · 54 сжатия · медиана 146 тыс.</div>
<ContextBreath agent="codex" :height="130" />

<div class="grid grid-cols-3 gap-4 mt-2 small ink2">
<div>Каждая точка — один запрос к модели. Контекст растёт с каждым выводом инструмента, а при сжатии агент сохраняет лишь краткий пересказ.</div>
<div>Claude доходит до ~967 тыс. и падает до 11–36 тыс. — одно сжатие на ~580 запросов. У Codex окно в 258 тыс., и сжатие случается раз в ~75 запросов.</div>
<div>Поэтому всё, что должно пережить сжатие, живёт в файлах: <code>AGENTS.md</code>, <code>CURRENT_WORK.md</code>, карточки и коммиты.</div>
</div>

<div class="source">~/.claude/projects: usage каждого запроса, compact_boundary · ~/.codex/sessions: token_usage_record, compacted · scripts/collect_context.py</div>

---

<Kicker>почему была пауза</Kicker>

# Восемь дней тишины совпали с лимитом

<WeeklyLimit class="mt-2" />

<div class="grid grid-cols-3 gap-4 mt-1 small ink2">
<div>Каждый столбец — максимум недельного лимита Codex за день (по московскому времени) по счётчику в журнале. <b class="hl">13 и 14 сентября — 100 %.</b></div>
<div>14 сентября в 12:05 МСК — последний коммит перед паузой; лимит сбрасывался только 20 сентября в 08:36 МСК.</div>
<div>Это совпадение по времени, а не доказанная причина: 22 сентября работа возобновилась уже при новом лимите.</div>
</div>

<div class="source">~/.codex/sessions: rate_limits.primary (окно 10 080 минут) в событиях token_count · data/sessions.json</div>

---

<Kicker>терминал</Kicker>

# Что агенты набирали в shell

<ShellPrograms class="mt-2" />

<div class="grid grid-cols-3 gap-4 mt-3 small ink2">
<div><b>Агенты в основном читают:</b> <span class="mono">sed</span>, <span class="mono">cat</span>, <span class="mono">rg</span>, <span class="mono">grep</span>, <span class="mono">tail</span>, <span class="mono">git diff</span> — это как минимум половина команд.</div>
<div>Codex сделал <b>20 899</b> вызовов <span class="mono">exec</span>, упаковав в них 29 410 команд — часто по несколько параллельно, плюс 1 603 сообщения своим субагентам.</div>
<div>Claude правил файлы в основном через Bash и Write: инструмент Edit за шесть дней — всего <b>12 раз</b>, Write — 151, Read — 337.</div>
</div>

<div class="source">первая программа каждой shell-команды · data/sessions.json · scripts/collect_sessions.py</div>

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

