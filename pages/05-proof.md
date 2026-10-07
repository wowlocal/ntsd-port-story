---
layout: chapter
num: 5
total: 15
kicker: Глава пятая
dates: 22–27 сентября
image: /img/menu-back-green-blue.jpg
stats: 96 коммитов · 0 правок в native/Sources · +20 700 строк инструментов
---

# Фабрика доказательств

Каждый шаг доказан, каждый провал сохранён. Но игра в приложении всё ещё не запускается.

---

<Kicker>где шла работа</Kicker>

# Две недели мимо `native/`

<NativeShare />

<div class="grid grid-cols-3 gap-4 mt-2 small ink2">
<div>С 14 по 27 сентября <b class="hl">1 коммит из 115</b> менял код игры в <code>native/Sources</code>. Работа шла в изолированных кандидатах — APFS-клонах на внешнем диске.</div>
<div>За те же дни Python-инструменты выросли <b class="hl">с 57 692 до 78 392 строк</b>: новые <code>*_validation.py</code>, <code>*_correction2.py</code>, <code>*_candidate.py</code>.</div>
<div>28 сентября проверенный кандидат на <b class="hl">2 291 файл</b> перенесли в <code>native/</code> одним коммитом — и график снова стал оранжевым.</div>
</div>

<div class="source">git log --name-only · data/daily.json · 866bf83</div>

---
clicks: 6
---

<Kicker>жизненный цикл карточки</Kicker>

# От плана до переноса — шесть стадий

<Pipeline class="mt-4" stepwise :steps="[
  { name: 'PLAN', ru: 'замороженный план', desc: 'вопрос, входы с SHA, конечный список случаев, лимиты, критерии приёмки' },
  { name: 'PREFLIGHT', ru: 'предполётная', desc: 'только чтение: найти разрывы интеграции до запуска' },
  { name: 'CANDIDATE', ru: 'кандидат', desc: 'изолированная копия; синтаксис — ещё не доказательство' },
  { name: 'VALIDATION', ru: 'валидация', desc: 'свежая сборка, сравнение с эталоном, каждый исход записан', accent: true },
  { name: 'CORRECTION', ru: 'исправление', desc: 'новый run ID; старый провал остаётся провалом' },
  { name: 'COMPLETION', ru: 'завершение', desc: 'регрессии, гейты, перенос в native/' },
]" loop-label="не больше трёх раундов на механизм — переименование не обнуляет счётчик" :loop-from="3" :loop-to="4" />

<div class="grid grid-cols-3 gap-4 mt-2 small ink2">
<div><b>Frozen plan.</b> План коммитится до запуска и больше не правится. Уточнение — отдельный amendment, который «описывает только различие».</div>
<div><b>202 плана, 27 исправлений.</b> В <code>docs/research</code> 568 карточек; 26 VALIDATION и 22 PREFLIGHT.</div>
<div><b>Ничего не стирать.</b> Прежний кандидат, логи и исходы хранятся; новый запуск получает свой ID и запись «что изменили и почему».</div>
</div>

<div class="source">docs/research/WORKFLOW.md · docs/research/PROGRESS_RULES.md · docs/research/TASK_TEMPLATE.md</div>

---

<Kicker>анатомия одной карточки · 22 сентября, 18:11–20:09</Kicker>

# 42 метода, 5 прогонов, 0 изменённых эталонов

<div class="mt-3">
<HostChainStrip />
</div>

<div class="grid grid-cols-[1.4fr_1fr] gap-5 mt-2">
<div class="small ink2">

Вопрос карточки: удержит ли постоянный host вход в загрузку и закоммитит ли итерацию меню целиком — с откатом и повтором. Все три исправления касались **только теста**; Core, expected и маски не менялись.

</div>
<div class="card-soft">
<div class="mono xsmall hl">"This is an incomplete resource-limited run, not a successful comparison or an assertion mismatch."</div>
<div class="xsmall muted mt-1">APPLICATION_HOST_LOADING_CORRECTION1.md</div>
</div>
</div>

<!--
Итог цепочки: 7 коммитов, 14 документов, 25 evidence-файлов за два часа — ради двух исправлений теста. Самое смешное — тест №28 упал не на логике игры, а на XCTAssertNotNil, который рекурсивно печатал огромное значение (пик 13,2 ГБ).
-->

---

<Kicker>7–27 сентября · месяц вслепую</Kicker>

# 3,4 млрд токенов — и никакой новой картинки

<BlindMonth class="mt-1" />

<div class="grid grid-cols-4 gap-3 mt-1">
<StatTile :value="36104" prefix="+" label="строк Swift-тестов за 7–27 сентября" size="sm" accent="var(--s1)" />
<StatTile :value="58621" prefix="+" label="строк в карточках исследований" size="sm" accent="var(--s4)" />
<StatTile value="52,87 %" label="кода .text EXE в описанных диапазонах порта" size="sm" accent="var(--s3)" />
<StatTile value="801 → 801" label="строк в слое приложения: на экране ничего нового" size="sm" accent="var(--s2)" />
</div>

<div class="source">data/tokens.json (журналы сессий) · data/app_lines.json (native/Sources/NTSDApp по дням) · data/growth.json · docs/estimates</div>

<!--
55 % всех токенов проекта ушло до первого матча в приложении. Снаружи это выглядело как сжигание денег: в окне — тренировочная сцена 7 сентября. Внутри росли ядро, оракулы и эталоны, на которых потом всё собралось за один день.
-->

---

<Kicker>что говорили аудиторы — что решали</Kicker>

# Не ускорять видимый прогресс

<div class="blind mt-1">
<div class="hdr"><span class="i-pixelarticons-eye" />аудиторы Codex видели</div>
<div></div>
<div class="hdr"><span class="i-pixelarticons-flag" />решение</div>

<div class="q"><span class="d">8 сен</span>«Но прироста подтверждённых игровых возможностей Practice за эти 12 часов нет».</div>
<div class="arr i-pixelarticons-arrow-right" />
<div class="a"><span class="d">8 сен</span>«<b>Не ускоряем видимый прогресс добавлением персонажей и техник на неполной основе.</b> …тренировочное окно некоторое время может выглядеть прежним».</div>

<div class="q"><span class="d">12 сен</span>«Сейчас основная проблема — разрыв между большим проверенным ядром и ограниченной Practice».</div>
<div class="arr i-pixelarticons-arrow-right" />
<div class="a"><span class="d">12 сен</span>Готовый движок L2DF дал работающее приложение через 16 минут после просьбы — и был остановлен: <i>«ок, остановил. продолжаем на main»</i>.</div>

<div class="q"><span class="d">14 сен</span>«Это полезно, но пользовательского результата пока не добавляет: MeleeScene всё ещё использует OriginalMelee».</div>
<div class="arr i-pixelarticons-arrow-right" />
<div class="a"><span class="d">13 сен</span>«…Погоня за ростом диапазонов сейчас дала бы красивый процент, но не приблизила бы так сильно первый настоящий матч».</div>

<div class="q"><span class="d">27 сен</span>«Ни одного коммита в <code>native/</code> за эти 9 часов. Приложение продолжает запускать Practice».</div>
<div class="arr i-pixelarticons-arrow-right" />
<div class="a"><span class="d">27 сен</span>Правила прогресса: проверенное — сразу переносить в <code>native/</code>. Но ни одна проверка не отменяется и ни один эталон не правится.</div>
</div>

<div class="card thesis mt-3">
<span class="i-pixelarticons-quote-text-inline" />
<div>
<div class="mono small">«Методология валидации — это всё. Это самое важное. Это ровно то, что в самом конце привело нас к полному паритету в интеграционных тестах».</div>
<div class="xsmall muted mt-1">автор проекта · <b class="hl">28 сентября</b> — первый матч в приложении, <b class="hl">3 октября</b> — 58 целых матчей без единого расхождения с оригиналом</div>
</div>
</div>

<div class="source">~/.codex/sessions: сессии-аудиты 8, 12, 13, 14, 26 и 27 сентября · 007c007 · docs/research/PROGRESS_RULES.md</div>

<style>
.blind { display: grid; grid-template-columns: 1fr 1.3rem 1.12fr; column-gap: 0.55rem; row-gap: 0.45rem; align-items: center; }
.blind .hdr { display: flex; align-items: center; gap: 0.4rem; font-family: var(--font-pixel); font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--naruto); }
.blind .hdr span { width: 1.05rem; height: 1.05rem; }
.blind .q, .blind .a { align-self: stretch; font-size: 0.66rem; line-height: 1.36; padding: 0.38rem 0.6rem; border-radius: 10px; }
.blind .q { background: var(--surface); border: 1px solid var(--hair); color: var(--ink-2); }
.blind .a { background: rgba(57,135,229,0.12); border: 1px solid rgba(57,135,229,0.35); color: var(--ink); }
.blind .d { display: inline-block; font-family: var(--font-mono); font-size: 0.58rem; color: var(--muted); margin-right: 0.45rem; }
.blind .arr { width: 1.1rem; height: 1.1rem; color: var(--naruto); justify-self: center; }
.thesis { display: flex; gap: 0.75rem; align-items: flex-start; border-color: rgba(255,138,61,0.55); padding: 0.75rem 1rem; }
.thesis > span { flex: none; width: 1.5rem; height: 1.5rem; color: var(--naruto); }
</style>

<!--
Полностью, 8 сентября: «Не ускоряем видимый прогресс добавлением персонажей и техник на неполной основе. Сейчас основной результат будет появляться в движке и проверках; тренировочное окно некоторое время может выглядеть прежним».
12 сентября пользователь спросил: «кароче не стоит полагаться на движок? лучше делать как в main-е, продолжить как шли?» — ответ: «ок, остановил. продолжаем на main».
13 сентября целиком: «Основную стратегию менять не стоит… Погоня за ростом диапазонов сейчас дала бы красивый процент, но не приблизила бы так сильно первый настоящий матч».
-->

---

<Kicker>27 сентября</Kicker>

# Правила прогресса

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-2">
<div>

<div class="xsmall muted">PROGRESS_RULES.md — «указание пользователя от 2026-09-27 после разбора 19 коммитов за девять часов»</div>

<div class="prules mt-2">
<div class="pr"><span class="i-pixelarticons-git-merge" /><div><b>Проверено — переносим.</b> «После успешного сравнения кандидата следующая задача — его перенос в <code>native/</code> и подключение ближайшего готового потребителя».</div></div>
<div class="pr"><span class="i-pixelarticons-repeat" /><div><b>Два шага без продвижения — разбор.</b> «После двух последовательных этапов только подготовки/упаковки/проверок… разобрать причину отсутствия продвижения. Переименование карточки счётчик не обнуляет».</div></div>
<div class="pr"><span class="i-pixelarticons-script" /><div><b>Без новых обёрток.</b> «Не добавлять новый prepare/finalize/publish-скрипт, отличающийся путями, счётчиками или названием задачи».</div></div>
<div class="pr"><span class="i-pixelarticons-pin" /><div><b>Гейт — один раз.</b> «Каждая отдельная gate проверяется и записывается один раз для закреплённых байтов».</div></div>
<div class="pr"><span class="i-pixelarticons-gamepad" /><div><b>Счёт файлов — не результат.</b> «Число файлов, архивов, инструкций и тестов не заменяет игровой или прикладной результат».</div></div>
</div>

</div>
<div>

<div class="card">
<div class="ttl"><span class="i-pixelarticons-computer" /><span class="pixel hl small">в тот же день</span></div>
<p class="small ink2">«Stop UTM work and prioritize native app integration» — виртуальную Windows-машину бросили: <i>«give up on UTM»</i>.</p>
<div class="tag">52d4740</div> <div class="tag">007c007</div>
</div>

<div class="card mt-3">
<div class="ttl"><span class="i-pixelarticons-calendar" /><span class="pixel hl small">прогноз · 27 сен, 09:49 МСК</span></div>
<p class="small ink2">«1–3 недели до первого проверенного Наруто/Саске матча в приложении; 6–12 недель до полного порта».</p>
<div class="xsmall muted">Через 33 часа матч в приложении дошёл до KO, через 5 дней целые матчи сверялись с оригиналом →</div>
</div>

</div>
</div>

<style>
.prules { display: flex; flex-direction: column; gap: 0.4rem; }
.pr { display: flex; gap: 0.6rem; align-items: flex-start; background: rgba(255, 255, 255, 0.03); border: 1px solid var(--hair); border-radius: 10px; padding: 0.42rem 0.65rem; font-size: 0.68rem; line-height: 1.38; color: var(--ink-2); }
.pr > span { flex: none; width: 1.3rem; height: 1.3rem; color: var(--naruto); margin-top: 0.05rem; }
.pr b { color: var(--ink); font-weight: 650; }
.ttl { display: flex; align-items: center; gap: 0.45rem; }
.ttl > span:first-child { flex: none; width: 1.2rem; height: 1.2rem; color: var(--naruto); }
</style>

<div class="source">docs/research/PROGRESS_RULES.md · 52d4740 · 007c007 · d1a930e</div>

<!--
Правила подготовили 27-го, но подключили только 28-го (d1a930e) — когда закрылись jobs, которые закрепили старые версии инструкций как вход. Даже правки правил ждали, пока живые процессы допишут свои результаты.
-->
