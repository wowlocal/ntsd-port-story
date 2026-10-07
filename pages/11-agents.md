---
layout: chapter
num: 11
total: 15
kicker: Глава одиннадцатая
dates: журналы сессий
image: /img/covers/ch11-context-breath.jpg
imagePixel: false
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

<div class="enter mt-3">
<div class="enter-row">
<div class="who"><span class="pixel hl">Codex · /goal</span><span>20 дней работы</span></div>
<div>
<div class="units"><i v-for="n in 163" :key="`h${n}`" class="sq-human" /><i v-for="n in 383" :key="`g${n}`" class="sq-goal" /></div>
<div class="keys"><span><i class="sq-human" /><b>163</b> сообщения человека</span><span><i class="sq-goal" /><b>383</b> автопродолжения /goal — 8 запусков цели, 129,5 ч автопилота</span></div>
<div class="turns"><b>≈ 2,3</b> автопродолжения на одно сообщение человека · <b>820</b> ходов: медиана <b>9,3 мин</b>, самый длинный <b>8,4 ч</b>, всего <b>241 ч</b> · <b>299</b> компакций контекста, окно 258 тыс. токенов</div>
</div>
</div>
<div class="enter-row">
<div class="who"><span class="pixel hl">Claude Code · /loop</span><span>6 дней работы</span></div>
<div>
<div class="units"><i v-for="n in 25" :key="`h${n}`" class="sq-human" /><i v-for="n in 60" :key="`l${n}`" class="sq-loop" /><i v-for="n in 55" :key="`w${n}`" class="sq-wake" /></div>
<div class="keys"><span><i class="sq-human" /><b>25</b> сообщений человека</span><span><i class="sq-loop" /><b>60</b> итераций /loop</span><span><i class="sq-wake" /><b>55</b> пробуждений по таймеру</span></div>
<div class="turns"><b>≈ 4,6</b> итерации и пробуждения на одно сообщение человека · <b>281</b> ход: медиана <b>0,9 мин</b>, самый длинный <b>4,4 ч</b>, всего <b>43,5 ч</b> · <b>9</b> компакций, каждая с ~967 тыс. до 11–36 тыс. токенов</div>
</div>
</div>
</div>

<div class="card-soft mt-4 small ink2">
Один квадрат — одно сообщение агенту: от человека или от автопилота. Длинные ходы Codex и короткие у Claude — разные режимы: <span class="mono">/goal</span> держит одну задачу часами, <span class="mono">/loop</span> просыпается, делает шаг и засыпает.
</div>

<div class="source">~/.codex/sessions: task_started/complete, compacted, сообщения goal · ~/.claude/projects: turn_duration, compact_boundary, scheduled_task_fire · data/sessions.json</div>

<style>
.enter-row { display: grid; grid-template-columns: 9rem 1fr; column-gap: 1rem; align-items: start; }
.enter-row + .enter-row { margin-top: 1.1rem; }
.enter .who { display: flex; flex-direction: column; gap: 0.15rem; font-size: 0.8rem; }
.enter .who span:last-child { font-size: 0.64rem; color: var(--muted); }
.enter .units { display: grid; grid-template-rows: repeat(7, 7px); grid-auto-flow: column; grid-auto-columns: 7px; gap: 2px; }
.enter .units i { display: block; border-radius: 1.5px; }
.enter .keys { display: flex; flex-wrap: wrap; gap: 0.2rem 1.1rem; margin-top: 0.45rem; font-size: 0.7rem; color: var(--ink-2); }
.enter .keys i { display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: 0.35rem; }
.enter .keys b { color: var(--ink); }
.enter .turns { margin-top: 0.2rem; font-size: 0.66rem; line-height: 1.4; color: var(--muted); }
.enter .turns b { color: var(--ink-2); font-weight: 600; }
.enter .sq-human { background: var(--ink-2); }
.enter .sq-goal { background: var(--s1); }
.enter .sq-loop { background: var(--s2); }
.enter .sq-wake { background: #8f4325; }
</style>

<!--
Было плитками: Codex — 383 автопродолжения /goal (8 запусков цели, 129,5 часа автопилота), 163 сообщения человека за 20 дней работы, 820 ходов (медиана 9,3 мин, самый длинный — 8,4 ч), 299 компакций контекста (окно — 258 тыс. токенов). Claude Code — 60 итераций /loop и 55 пробуждений по таймеру, 25 сообщений человека за 6 дней работы, 281 ход (медиана 0,9 мин, самый длинный — 4,4 ч), 9 компакций контекста (каждая — с ~967 тыс. до 11–36 тыс. токенов).

241 час ходов у Codex и 43,5 часа у Claude. На одно сообщение человека приходилось ~2,3 автопродолжения у Codex и ~4,6 итерации и пробуждения у Claude. Квадраты — те же счётчики: в каждом столбце семь сообщений, человек слева, автопилот справа.
-->

---

<Kicker>память агента</Kicker>

# Как агент «дышит» контекстом

<div class="xsmall ink2 mt-1"><i class="swatch" style="background: var(--s2)" /><b>Claude Opus 5.5</b> · сессия 28 сентября — 3 октября · 5 257 запросов · 9 автосжатий · медиана контекста 492 тыс. токенов</div>
<ContextBreath agent="claude" :height="140" />

<div class="xsmall ink2 mt-1"><i class="swatch" style="background: var(--s1)" /><b>Codex · GPT-6 Astra</b> · первая сессия 7–9 сентября, ночной спринт · 4 057 запросов · 54 сжатия · медиана 146 тыс.</div>
<ContextBreath agent="codex" :height="120" />

<div class="grid grid-cols-3 gap-4 mt-2 small ink2">
<div>Каждая точка — один запрос к модели. Контекст растёт с каждым выводом инструмента, а при сжатии агент сохраняет лишь краткий пересказ.</div>
<div>Claude доходит до ~967 тыс. и падает до 11–36 тыс. — одно сжатие на ~580 запросов. У Codex окно в 258 тыс., и сжатие случается раз в ~75 запросов.</div>
<div>Поэтому всё, что должно пережить сжатие, живёт в файлах: <code>AGENTS.md</code>, <code>CURRENT_WORK.md</code>, карточки и коммиты.</div>
</div>

<div class="source">~/.claude/projects: usage каждого запроса, compact_boundary · ~/.codex/sessions: token_usage_record, compacted · scripts/collect_context.py</div>

---

<Kicker>лимиты · ChatGPT Pro</Kicker>

# Сколько ресетов ушло на Astra

<div class="small ink2 -mt-1">За 27 дней недельное окно Codex досрочно обнулялось 8 раз. Четыре раза это были ваши ресеты, когда лимит был выбран на 93–100 %.</div>

<LimitSaw class="mt-1" :height="190" />

<div class="grid grid-cols-[1.25fr_1fr_1fr] gap-3 mt-1 xsmall ink2">
<div class="card-soft">
<div class="small ink"><i class="dot" style="background: var(--s2)" /><b>4 ваших ресета за 5 дней</b></div>
<b class="ink">10 сен</b>: через пару минут после «You've hit your usage limit… try again at Sep 15th» · <b class="ink">12 сен</b>: при 93 % · <b class="ink">13 сен</b>: через 7 часов после ночного упора («try again at Sep 19th») · <b class="ink">14 сен</b>: через 9 минут после 100 %
</div>
<div class="card-soft">
<div class="small ink"><i class="dot ring" /><b>2 общих сброса OpenAI</b></div>
<b class="ink">8 сен</b>: всем платным после выката GPT-6 Astra, было 36 % · <b class="ink">26 сен</b>: после сбоя Codex 25 сентября, было 72 %
</div>
<div class="card-soft">
<div class="small ink"><i class="dot ring dashed" /><b>2 — не различить</b></div>
<b class="ink">24 сен</b> при 90 % и <b class="ink">2 окт</b> при 86 %: окно началось заново раньше срока, но журнал не говорит, кто его сбросил.
</div>
</div>

<div class="xsmall muted mt-2">Лимит паузу 15–21 сентября не объясняет: 14-го окно обнулили, и до 18-го 87 из 90 % нового окна ушли на другие проекты.</div>

<div class="source">~/.codex/sessions: rate_limits.primary (окно 10 080 мин) в token_count, ошибки usage_limit_exceeded · общие сбросы — объявления OpenAI · scripts/collect_limits.py</div>

---

<Kicker>лимиты · ChatGPT Pro</Kicker>

# Как сгорала подписка за $200

<div class="small ink2 -mt-1">В журнале нет денег, только процент недельного лимита. По номиналу неделя Pro стоит ≈ $46: $200 × 12 месяцев ÷ 52 недели.</div>

<SubscriptionBurn class="mt-1" />

<div class="grid grid-cols-3 gap-3 mt-2">
<StatTile :value="7.9" :decimals="1" label="недельного лимита за 27 дней" sub="весь аккаунт, из них 5,8 на порт; без досрочных сбросов потолок был бы 3,9" size="sm" accent="var(--s1)" />
<StatTile :value="362" prefix="≈ $" label="лимита по номиналу" sub="из них ≈ $266 на порт; подписка за эти 27 дней стоила ≈ $177" size="sm" />
<StatTile :value="152" suffix="%" label="за 12 сентября" sub="полтора недельных лимита за сутки, ≈ $70; с 28 сентября работу ведёт Claude, и Codex тратит до 20 % в день" size="sm" accent="var(--s2)" />
</div>

<div class="source">~/.codex/sessions: рост максимума внутри недельного окна по дням (+03:00, с 28 сентября +02:00) · пересчёт по номиналу $200 в месяц · scripts/collect_limits.py</div>

---

<Kicker>лимиты · Claude Max 20x</Kicker>

# Как сгорала подписка Anthropic

<div class="small ink2 -mt-1">Тоже $200 в месяц, но процент лимита Claude Code локально не пишет. Поэтому считаем, во сколько те же токены обошлись бы по ценам API Opus 5.5.</div>

<ClaudeBurn class="mt-1" />

<div class="grid grid-cols-3 gap-3 mt-2">
<StatTile :value="797" prefix="≈ $" label="по ценам API за 6 дней порта" sub="в 20 раз больше стоимости этих дней подписки ($40) — как 4 месячные подписки" size="sm" accent="var(--s2)" />
<StatTile :value="237" prefix="$" label="за 29 сентября" sub="×36 к дню подписки; агент работал все 24 часа, и 30-го тоже" size="sm" />
<StatTile :value="0" label="сообщений о лимите" sub="Codex трижды упирался в недельный потолок, Claude — ни разу. 99,4 % входных токенов пришло из кэша, чтение кэша — 70 % цены" size="sm" accent="var(--s1)" />
</div>

<div class="source">~/.claude/projects: usage каждого ответа, дедупликация как в collect_tokens.py · цены platform.claude.com/docs/en/about-claude/pricing · scripts/collect_claude_burn.py</div>

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

