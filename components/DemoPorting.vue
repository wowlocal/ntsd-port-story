<script setup lang="ts">
// Demo-day deck: how long each platform took after the macOS release, and what got in the way.
// Bars span the first and last commit of each piece of work (local time, UTC+2), 3–19 October:
// Linux/Windows/iPad/Android from data/xplat.json lanes (3 Oct 20:11 → 5 Oct 02:01); the Galaxy A12 from its first
// connection (5 Oct 07:42, chapter 14) to the end of the loading night (11 Oct 19:43, chapter 16); Apple TV and the
// browser from TVOS_WEB's start to W4 (11 Oct 20:12 → 13 Oct 06:21, data/web_steps.json); the iPhone build (13 Oct
// 06:40 request → 08:45 f340f1e2); the Steam Deck (16 Oct 19:31 → 17 Oct 05:27, MENU_GAMEPAD); the live site (W5,
// 17 Oct 13:50 → 16:21); the on-screen buttons as a point at their commit (743f0558, 19 Oct 14:06 UTC+2 — the start of
// that work is not on this Mac, so no duration). Releases: v0.4.0 3 Oct 16:45, native-preview 13 Oct 15:22, 0.6.0 19 Oct 15:11.
interface Row { name: string, from: string, to: string, hard: string, hot?: boolean, span: string, point?: boolean }
const rows: Row[] = [
  { name: 'Linux, Windows', from: '10-03T20:11', to: '10-04T20:54', span: '≈ 1 сутки', hard: 'компилятор Swift для Linux терял запись в память — поймал прогон всей матрицы, ушёл отчёт в Swift' },
  { name: 'iPad', from: '10-04T13:20', to: '10-04T22:43', span: '9 ч', hard: 'тап приходит мгновенно, а игра ждёт, что кнопку держат несколько тиков' },
  { name: 'Android', from: '10-04T21:12', to: '10-05T02:01', span: '5 ч', hard: '22 минуты от первого запуска до звука и музыки' },
  { name: 'телефон Galaxy A12', from: '10-05T07:42', to: '10-11T19:43', span: '6,5 дня', hot: true, hard: 'игре нужно 4 ГБ, у телефона 2,8 · 5,4 тика/с → 60 кадров/с · меню 131,9 → 12,7 с' },
  { name: 'Apple TV, браузер', from: '10-11T20:12', to: '10-13T06:21', span: '34 ч', hard: 'Swift в WebAssembly; первый визит — 881,5 МБ данных, сжатие → 99,5 МБ' },
  { name: 'iPhone', from: '10-13T06:40', to: '10-13T08:45', span: '2 ч', hard: 'экран телефона меньше окна игры' },
  { name: 'Steam Deck', from: '10-16T19:31', to: '10-17T05:27', span: '10 ч', hard: 'меню оригинала понимает только мышь' },
  { name: 'браузер, живой сайт', from: '10-17T13:50', to: '10-17T16:21', span: '2,5 ч', hard: '1 521 файл игры — 1 521 запрос; упаковали в 12 пачек в памяти браузера: 46,5 → 4,6 с' },
  { name: 'кнопки на экране', from: '10-19T14:06', to: '10-19T14:11', span: '19 окт', point: true, hard: 'у оригинала всегда была клавиатура: кнопки жмут её клавиши — и водили не того игрока' },
]
const t0 = Date.parse('2026-10-03T12:00:00')
const t1 = Date.parse('2026-10-20T00:00:00')
const pct = (s: string) => ((Date.parse(`2026-${s}:00`) - t0) / (t1 - t0)) * 100
const bar = (r: Row) => ({ left: `${pct(r.from)}%`, width: `max(5px, ${pct(r.to) - pct(r.from)}%)` })
const ticks = [4, 6, 8, 10, 12, 14, 16, 18].map(d => ({ d, left: `${pct(`10-${String(d).padStart(2, '0')}T00:00`)}%` }))
const rel = [
  { at: '10-03T16:45', label: 'v0.4.0' },
  { at: '10-13T15:22', label: 'релиз' },
  { at: '10-19T15:11', label: '0.6.0' },
].map(r => ({ ...r, left: `${pct(r.at)}%` }))
</script>

<template>
  <div class="dp">
    <div class="hd">
      <span />
      <div class="axis">
        <span v-for="t in ticks" :key="t.d" class="tk" :style="{ left: t.left }">{{ t.d }} окт</span>
      </div>
      <span class="hh">что мешало</span>
    </div>
    <div v-for="r in rows" :key="r.name" class="row" :class="{ hot: r.hot }">
      <span class="nm">{{ r.name }}</span>
      <div class="track">
        <span v-for="x in rel" :key="x.label" class="rl" :style="{ left: x.left }" />
        <span v-if="r.point" class="pt" :style="{ left: `${pct(r.from)}%` }" />
        <span v-else class="bar" :style="bar(r)" />
        <span v-if="!r.point" class="sp" :style="{ left: `calc(${pct(r.to)}% + 8px)` }">{{ r.span }}</span>
      </div>
      <span class="hard">{{ r.hard }}</span>
    </div>
    <div class="ft">
      <span />
      <div class="axis rels">
        <span v-for="x in rel" :key="x.label" class="rt" :style="{ left: x.left }">{{ x.label }}</span>
      </div>
      <span />
    </div>
  </div>
</template>

<style scoped>
.dp { display: flex; flex-direction: column; gap: 4px; }
.hd, .row, .ft { display: grid; grid-template-columns: 8.6rem 1fr 22rem; gap: .9rem; align-items: center; }
.axis { position: relative; height: 1.1rem; }
.tk { position: absolute; transform: translateX(-50%); font-family: var(--font-mono); font-size: .58rem; color: var(--muted); white-space: nowrap; }
.hh { font-family: var(--font-pixel); font-size: .6rem; color: var(--naruto); text-transform: uppercase; letter-spacing: .06em; }
.row { min-height: 2.15rem; border-top: 1px solid var(--grid); padding-top: 3px; }
.nm { font-size: .78rem; color: var(--ink); font-weight: 600; }
.track { position: relative; height: 1.5rem; }
.rl { position: absolute; top: -4px; bottom: -4px; width: 0; border-left: 1px dashed var(--axis); }
.bar { position: absolute; top: .3rem; height: .9rem; border-radius: 4px; background: var(--s1); }
.sp { position: absolute; top: .22rem; font-family: var(--font-mono); font-size: .62rem; color: var(--ink-2); white-space: nowrap; }
.hard { font-size: .7rem; line-height: 1.32; color: var(--ink-2); }
.pt { position: absolute; top: .38rem; width: .75rem; height: .75rem; margin-left: -.375rem; border-radius: 50%; background: var(--s1); }
.row.hot .bar { background: var(--naruto); box-shadow: 0 0 12px rgba(255, 138, 61, .45); }
.row.hot .nm, .row.hot .hard { color: var(--ink); }
.row.hot .sp { color: var(--naruto); font-weight: 700; }
.rels { height: 1rem; }
.rt { position: absolute; transform: translateX(-50%); font-family: var(--font-pixel); font-size: .58rem; color: var(--muted); white-space: nowrap; }
</style>
