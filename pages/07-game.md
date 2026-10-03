---
layout: chapter
num: 7
total: 12
kicker: Глава седьмая
dates: 29 сентября — 2 октября
image: /img/screens/12-all-17-backgrounds-grid.jpg
stats: все режимы за день · 200 000 тиков без остановки · сетевой матч двух приложений
---

# Вся игра

Когда ядро стоит на месте, режимы подключаются один за другим. Дальше — износ, причуды оригинала и сеть.

---

<Kicker>29 сентября · 34 коммита</Kicker>

# Все режимы за один день

<div class="grid grid-cols-3 gap-3 mt-2">
<WindowFrame src="/img/screens/07-mission-stage-1-1-storyboard.png" height="128px" title="Stage 1-1 · efcdedc" caption="Mission: логика стейджей 437860 — диалог Какаши, бой, Summary" />
<WindowFrame src="/img/screens/09-war-battle-cave.png" height="128px" title="War · 4651853" caption="War: логика битвы 43a860, десятки войск на арене" />
<WindowFrame src="/img/screens/10-team-tournament-bracket-winner.png" height="128px" title="Team Tournament · 16f36a0" caption="Tournament и Team Tournament: сетка и победитель" />
<WindowFrame src="/img/screens/06-demo-arena-ai.png" height="128px" title="Demo · 6c384fc" caption="Demo: компьютерные бойцы на арене" />
<WindowFrame src="/img/screens/11-summary-table-values.png" height="128px" title="Playback · d86c783" caption="Просмотр записей: zlib 1.1.4, пролог проигрывания 41bd24" />
<WindowFrame src="/img/screens/17-gdi-text-controls.png" height="128px" title="CONTROL SETTINGS · 69ffa8e" caption="Настройки управления: клавиши игрока сохраняются" />
</div>

<div class="source">efcdedc · 4651853 · 6c384fc · d86c783 · 16f36a0 · abf941f · 69ffa8e · 553d100</div>

---

<Kicker>записи матчей</Kicker>

# Анатомия `.lfr`

<LfrAnatomy class="mt-3" />

<div class="grid grid-cols-3 gap-4 mt-4 small ink2">
<div><b>Вшитый zlib 1.1.4.</b> Современный zlib 1.2.12 расходится с ним в 53 случаях корпуса — порт вендорит именно 1.1.4. Реализацию <code>longest_match</code> оригинал выбирает по CPUID; порт объявляет сигнатуру <code>0x600</code> и совпадает на всех 4 353 858 вызовах.</div>
<div><b>Баг в загрузчике.</b> 0x43e620 выделяет 0x630e18 байт, а распаковывает с ёмкостью 0x631200 — на 1 000 больше. На повреждённом файле это переполнение кучи; порт его документирует и отклоняет.</div>
<div><b>Попиксельно.</b> «A recorded VS match plays back pixel-identical to the recording outside the playback bar» — запись, сделанная на Mac, проигрывается кадр в кадр вместе с полным Summary.</div>
</div>

<div class="source">tools/original_replay.py · docs/research/REPLAY_TICK.md · REPLAY_WRITER.md · REPLAY_COMPRESSION.md · d786b52 · d86c783</div>

---

<Kicker>30 сентября · на износ</Kicker>

# 200 000 тиков и утечка памяти

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-2">
<div>

<div class="xsmall muted mb-1">рост RSS во время длинных VS-сессий, МБ в минуту</div>

<div class="bars">
<div class="bar-row"><span class="bl">до исправления, 20 матчей</span><span class="bt"><i style="width: 100%" /></span><span class="bv">72</span></div>
<div class="bar-row"><span class="bl">экран хранит счётчики, а не журнал отрисовки</span><span class="bt"><i style="width: 16.7%" /></span><span class="bv">12</span></div>
<div class="bar-row"><span class="bl">курсоры итераций только с ресурсами</span><span class="bt"><i style="width: 7.6%" /></span><span class="bv">4–7</span></div>
<div class="bar-row"><span class="bl">Demo, 27 минут после обоих исправлений</span><span class="bt"><i style="width: 5.6%" /></span><span class="bv">4</span></div>
</div>

<p class="small ink2 mt-3">Footprint за 20 матчей рос с 2,0 до 3,2 ГБ; после исправлений — ровно 2,0 ГБ на каждом замере. Причины: ~130 записей отрисовки на тик (714 587 за три матча) и ~9 000 сохранённых курсоров итераций на матч.</p>

</div>
<div>

<div class="grid grid-cols-2 gap-3">
<StatTile :value="22" label="длинных прогона Demo, War и Stage" size="sm" />
<StatTile :value="200000" label="тиков в самом длинном прогоне без остановки" size="sm" accent="var(--s1)" />
<StatTile :value="1282772" label="вызова AI за 95 матчей Demo" size="sm" accent="var(--s3)" />
<StatTile value="15,1 с" label="на 2 000 итераций меню вместо растущих 16 → 25 с" size="sm" accent="var(--s4)" />
</div>

<p class="small ink2 mt-3">Каждая неподдержанная ветвь в прогоне останавливает игру событием <code>boundary</code>. Так находились причуды оригинала: кадр 1000 у <code>ironsand.dat</code>, незаписанные слова прыжка у <code>wind.dat</code>…</p>

</div>
</div>

<div class="source">e0d1b64 · 873e039 · 83f65a6 · 2278c4d · 36528c9 · docs/research/APPLICATION_SOAKS.md · data/evidence/memory-soak.json</div>

<style>
.bars { display: flex; flex-direction: column; gap: 0.45rem; }
.bar-row { display: grid; grid-template-columns: 12.5rem 1fr 2.2rem; align-items: center; gap: 0.6rem; }
.bl { font-size: 0.66rem; color: var(--ink-2); line-height: 1.2; }
.bt { height: 12px; }
.bt i { display: block; height: 12px; background: var(--s1); border-radius: 0 4px 4px 0; }
.bv { font-size: 0.8rem; font-weight: 650; color: var(--ink); }
</style>

---

<Kicker>необычные состояния</Kicker>

# Когда оригинал читает за краем памяти

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2">
<div>

<WindowFrame src="/img/screens/05-f8-full-pool-chaos.png" title="NTSD Native — F8 × 88" caption="F8 сыплет предметы, пока пул из 400 слотов не заполнится" />

</div>
<div class="small ink2">

**F8 на полном пуле.** Номер слота оригинал берёт из неинициализированного слова стека `SP+34`. Если там 0 — предметом становится Наруто игрока 1. Обычно же там мусор, и чтение по `0xff2f6084` падает с access violation. Порт воспроизводит обе ветки: вторая — объявленный *Source fault*.

**Кадр 1000.** Лечащий удар kind 8 ставит атакующему кадр 1000, и оригинал читает Frame по `Object+0x5c464` — далеко за концом аллокации. Ещё 41 <code>wpoint</code> использует <code>weaponact</code> 1000, 9998 или −888.

<div class="card-soft mt-2">
<div class="mono xsmall hl">"The review found three errors, all confirmed."</div>
<div class="xsmall muted mt-1">независимое ревью политики «кадры за пределами Object читаются как отсутствующие», 7bf3624</div>
</div>

</div>
</div>

<div class="source">8d107f1 · f4cdcbb · 457cc7d · 7bf3624 · b729b3f · docs/research/APPLICATION_OUT_OF_OBJECT_FRAMES.md</div>

---

<Kicker>1–2 октября · как в оригинале</Kicker>

# Мелочи, которые делают игру той самой

<div class="grid grid-cols-3 gap-4 mt-2">
<div class="card">
<div class="pixel hl small">Alt+Enter · cb33304</div>
<p class="small ink2 mb-0">Полноэкранный режим как в оригинале — вместе с его багом: звуковые эффекты глохнут до конца сессии, а во время записи повтора игра падает через обнулённый указатель <code>0x4588a8</code>. В порту это остановка «Source fault»; обычный полноэкранный режим macOS добавлен отдельно.</p>
</div>
<div class="card">
<div class="pixel hl small">GDI-текст · 778a8c4</div>
<p class="small ink2 mb-0">Часть подписей оригинал рисует через Windows GDI шрифтом <code>SYSTEM_FONT</code>. На Mac — системный шрифт, bold 13 px в ячейке 16 px: позиция, размер и цвет сохранены. Это одно из двух объявленных отличий.</p>
</div>
<div class="card">
<div class="pixel hl small">дыры RLE · 55fd92d</div>
<div class="flex gap-2 mt-1">
<img src="/img/screens/13a-rle-holes-before.png" class="pixelated rounded" style="width: 48%">
<img src="/img/screens/13b-rle-holes-after.png" class="pixelated rounded" style="width: 48%">
</div>
<p class="xsmall ink2 mb-0 mt-1">«Com» и «P1» — bitmap-шрифты в RLE8 с 20 800+ незаписанными пикселями. Windows заполняет дыры индексом палитры 0, и color key их вырезает. Без этого под надписью — чёрная плашка.</p>
</div>
</div>

<div class="card-soft mt-4 small ink2">
И ещё: приложение сразу открывает оригинальную игру (80c83c1), геймпады работают как джойстики оригинала через GameController (f265f11), у бандла — иконка из самого EXE (60cd161).
</div>

---

<Kicker>1–2 октября · сеть</Kicker>

# Отказ, перестраховка и матч двух приложений

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-2">
<div>

<Timeline dense :items="[
  { time: '01.10', title: 'Mac-сервис Winsock для сетевой игры (Claude)', hash: '7727346' },
  { time: '01.10', title: 'Отказ модели на сетевой интеграции — сеть отложена', hash: '0efae95' },
  { time: '02.10', title: 'Correct overstated networking hold — запрет был не на всю сеть', hash: 'a4fb48c', hot: true },
  { time: '02.10', title: 'Нативный клиент и переход меню в подключённое состояние', hash: 'c573f10' },
  { time: '02.10', title: 'Два приложения доигрывают матч до Summary', hash: '73f8d22', hot: true },
  { time: '02.10', title: 'Выход хоста и закрытие клиента', hash: '4f65fa4' },
]" />

<p class="xsmall muted mt-2">Сеть N1–N5 довёл параллельный агент (Codex, без трейлера). Независимое ревью нашло одно замечание P2 — исправлено.</p>

</div>
<div>

<div class="grid grid-cols-2 gap-3">
<StatTile :value="1070" label="игровых тиков сетевого матча" size="sm" />
<StatTile :value="836" label="пакетов в каждую сторону, каждый совпал с приёмом" size="sm" accent="var(--s1)" />
</div>

<div class="card mt-3">
<div class="pixel hl small">протокол оригинала</div>
<p class="small ink2 mb-0">Хост шлёт <code>u can connect\0</code> (14 байт) и спит <code>Sleep(3000)</code>. Клиент делает <code>recv</code> 3001 байта <b>прямо в таблицу ГСЧ</b> <code>0x44ff90</code>, не проверяя код возврата. Сообщение об ошибке так и написано: <code>Accpet() Error</code>.</p>
</div>

<p class="xsmall muted mt-2">Состояние двух приложений различалось только CRT-случайными смещениями искр (≤ 8 px): стартовые seed разные намеренно.</p>

</div>
</div>

<div class="source">docs/research/NETWORK_PLAY.md · NETWORK_CLIENT.md · NETWORK_NOTIFICATION.md · docs/evidence/network-review-20261002.json</div>
