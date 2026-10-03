---
layout: chapter
num: 5
total: 11
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

<Kicker>жизненный цикл карточки</Kicker>

# От плана до переноса — шесть стадий

<Pipeline class="mt-4" :steps="[
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

<Kicker>27 сентября</Kicker>

# Правила прогресса

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-2">
<div>

<div class="xsmall muted">PROGRESS_RULES.md — «указание пользователя от 2026-09-27 после разбора 19 коммитов за девять часов»</div>

<div class="small">

- «После успешного сравнения кандидата следующая задача — **его перенос в `native/`** и подключение ближайшего готового потребителя».
- «После двух последовательных этапов только подготовки/упаковки/проверок… разобрать причину отсутствия продвижения. **Переименование карточки счётчик не обнуляет**».
- «Не добавлять новый prepare/finalize/publish-скрипт, отличающийся путями, счётчиками или названием задачи».
- «Каждая отдельная gate проверяется и записывается **один раз** для закреплённых байтов».
- «Число файлов, архивов, инструкций и тестов **не заменяет игровой или прикладной результат**».

</div>

</div>
<div>

<div class="card">
<div class="pixel hl small">в тот же день</div>
<p class="small ink2">«Stop UTM work and prioritize native app integration» — виртуальную Windows-машину бросили: <i>«give up on UTM»</i>.</p>
<div class="tag">52d4740</div> <div class="tag">007c007</div>
</div>

<div class="card mt-3">
<div class="pixel hl small">прогноз · 27 сен, 09:49 МСК</div>
<p class="small ink2">«1–3 недели до первого проверенного Наруто/Саске матча в приложении; 6–12 недель до полного порта».</p>
<div class="xsmall muted">Через 33 часа матч в приложении дошёл до KO, через 5 дней целые матчи сверялись с оригиналом →</div>
</div>

</div>
</div>

<div class="source">docs/research/PROGRESS_RULES.md · 52d4740 · 007c007 · d1a930e</div>

<!--
Правила подготовили 27-го, но подключили только 28-го (d1a930e) — когда закрылись jobs, которые закрепили старые версии инструкций как вход. Даже правки правил ждали, пока живые процессы допишут свои результаты.
-->
