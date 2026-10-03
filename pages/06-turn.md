---
layout: chapter
num: 6
total: 13
kicker: Глава шестая
dates: 28 сентября
image: /img/screens/16-character-ai-ko.png
stats: 15 коммитов · 13:31 → 23:56 · первый полный матч в приложении
---

# Поворот

Новый агент, новые правила и две недели проверенного кода в изолированном кандидате. За один день всё это превращается в игру.

---

<Kicker>28 сентября · 13:31–13:37</Kicker>

# Передача за шесть минут

<div class="grid grid-cols-[1.15fr_1fr] gap-6 mt-2">
<div>

<Timeline :items="[
  { time: '13:31', title: 'Publish the verified 167-method loading-arena validation', hash: '838cbe7', note: 'очередь из 167 методов, запущенная ещё при Codex, завершилась с кодом 0; первый коммит с трейлером Claude' },
  { time: '13:32', title: 'Connect the progress rules to the standing instructions', hash: 'd1a930e', note: 'патч промптов, подготовленный накануне, применён: защищавшие его jobs завершились' },
  { time: '13:34', title: 'Promote the verified 2291-file Native candidate into native/', hash: '866bf83', note: '1 257 новых файлов (20 Core, 11 платформа, 27 тестов, 1 199 ресурсов каталога) и 51 изменённый, ни одного удалённого', hot: true },
  { time: '13:37', title: 'Record the native root promotion in the current handoff', hash: 'b55e8d9' },
]" />

</div>
<div>

<div class="card">
<div class="pixel hl small">честный контекст</div>
<p class="small ink2">Скорость следующих часов опиралась на код эпохи Codex. В момент переноса в <code>native/Sources</code> было <b>39 300 строк</b> — это <b>81 %</b> нынешних 48 369.</p>
<div class="grid grid-cols-2 gap-2 mt-2">
<StatTile :value="39300" label="строк native/Sources после переноса" size="sm" accent="var(--s1)" />
<StatTile :value="48369" label="строк на 3 октября" size="sm" />
</div>
</div>

<p class="xsmall muted mt-2">В эти же сутки сменились и агент, и правила (PROGRESS_RULES). Их вклад по отдельности не измерен.</p>

</div>
</div>

<div class="source">838cbe7 · d1a930e · 866bf83 · b55e8d9 · git ls-tree 866bf83 native/Sources</div>

---

<Kicker>28 сентября · 13:56–23:56</Kicker>

# День, когда игра ожила

<div class="grid grid-cols-[1fr_1.05fr] gap-5 mt-1">
<div>

<Timeline dense :items="[
  { time: '13:56', title: 'Оригинальный WinMain запущен в приложении на runtime-провайдерах', hash: '743380c' },
  { time: '14:34', title: 'Живое главное меню оригинала', hash: 'a1c5f3c' },
  { time: '15:32', title: 'Загрузка каталога после START', hash: 'c1567cb' },
  { time: '15:50', title: 'Матч Наруто против Саске на District', hash: '4943589' },
  { time: '15:57', title: 'Живой бой — и найден блокер AI', hash: '455afeb' },
  { time: '17:10', title: 'Порт ввода объектов 406ba0', hash: '855e206' },
  { time: '18:15', title: 'Порт AI персонажей 4094b0 — бой до KO', hash: '2c02e5b', hot: true },
  { time: '19:15', title: 'Повтор, Summary, эпилог, возврат в меню', hash: '0a77527', hot: true },
  { time: '19:54', title: 'Все блоки спецприёмов селектора AI 403a40', hash: '5986808' },
  { time: '21:27', title: 'VS с компьютерным игроком', hash: '94762ea' },
  { time: '23:56', title: '30 тиков в секунду с тремя бойцами', hash: '9d33d8d' },
]" />

</div>
<div>

<WindowFrame src="/img/screens/16-character-ai-ko.png" height="245px" position="center 70%" title="NTSD Native — VS, District · 18:15" caption="Теневые клоны Наруто добивают Саске: первый KO в приложении (2c02e5b)" />

<div class="card-soft mt-2">
<div class="mono xsmall hl">"The app now plays the Naruto vs Sasuke District match through KO, Summary and back to the menus."</div>
<div class="xsmall muted">0a77527 — через 5 ч 44 мин после первого коммита Claude</div>
</div>

</div>
</div>

---

<Kicker>что мешало и как нашлось</Kicker>

# Три стопора первого матча

<IconCards class="mt-3 stoppers" :cols="3" :items="[
  { icon: 'i-pixelarticons-bullseye-arrow', title: 'Погоня, которой не было', text: 'Бой встал на непортированном вводе объекта: «догоняющий» снаряд <code>jan_chaseh.dat</code>. Порт AI 4094b0 сверили с оригиналом на двух корпусах — <b>3 770 реальных вызовов</b>.', tag: '406ba0 · 4094b0 · 455afeb → 2c02e5b' },
  { icon: 'i-pixelarticons-snail', title: 'Игра в 8 тиков в секунду', text: 'В фоне macOS App Nap душил цикл тиков. Теперь приложение держит user-initiated activity: Windows не тормозит цикл <code>Sleep</code> фоновой игры. Итог — <b>30,3 тика/с</b>.', tag: '9d33d8d' },
  { icon: 'i-pixelarticons-repeat', title: 'Воспроизводимый Mac', text: '<code>--script</code> — клики, клавиши, снимки. <code>--virtual-clock</code> — время из номера итерации. Снимки кадров побайтно совпадают между прогонами.', tag: '4943589 · 9d33d8d' },
]" />

<TurnTimer class="mt-4" />

<style>
.stoppers :deep(.ic) { padding: 0.85rem 1rem 0.9rem; }
.stoppers :deep(.ico) { width: 1.7rem; height: 1.7rem; }
.stoppers :deep(.head b) { font-size: 0.88rem; }
.stoppers :deep(.txt) { font-size: 0.76rem; line-height: 1.45; margin-top: 0.5rem; }
.stoppers :deep(.txt b) { color: var(--ink); }
.stoppers :deep(.txt code) { white-space: nowrap; }
.stoppers :deep(.tg) { margin-top: 0.6rem; font-size: 0.6rem; }
</style>

<div class="source">455afeb · 855e206 · 2c02e5b · 9d33d8d · docs/ORIGINAL_ENGINE.md</div>

<!--
Погоня: диагностика назвала объект 219 — chars\jan_chaseh.dat, тип 3, кадр 51. Порт AI 4094b0 шёл с помощниками; сверка на двух корпусах по 3 770 реальных вызовов — вызовы ГСЧ, глобалы, World и все Actor.
8 тиков: когда окно теряло фокус, App Nap душил цикл, а приложение ещё и строило никому не нужные снимки состояния на каждой стадии.
Воспроизводимость: --script — тайм-клики, клавиши, снимки и выход; --virtual-clock BASE STEP — timeGetTime из номера итерации, фиксированная дата старта и курсор. На этом потом построится вся сверка с оригиналом.
Таймер: база сдвигается ровно на 33 мс, а не до текущего времени, поэтому в среднем тик раз в 33 мс — 1000 / 33 ≈ 30,3 в секунду.
-->
