<script setup lang="ts">
// Chapter 19, TVOS_WEB W5: the browser host's data as 12 brotli packs kept in OPFS instead of 1,521 files.
// Top: one square — one data file the program reads (read-order.json: 1,521 reads), against the 12 packs
// (pack 0 = the 48 startup reads). On the slide both fill at ×10 speed: the live site's cold visit had its data at
// 46.45 s before and 4.61 s after. Bottom: medians of the card's visits, old → new.
// Data: docs/evidence/tw-w5-web-packed-loading-20261017.json (liveSiteBefore, visits.cases, published.visitsHere),
// pinned at origin/main d7330e96. The live site's "after" is the 2nd and 3rd cold visit (the 1st met a cold CDN edge).
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'

const FILES = 1521
const COLS = 117 // 117 × 13 = 1,521
const PACKS = 12
const before = 46.45
const after = 4.61
const speed = 10

const nav = useNav()
const active = useIsSlideActive()
const t = ref(nav.isPrintMode.value ? 1e9 : 0)
let raf = 0
let t0 = 0
function tick(now: number) {
  t.value = ((now - t0) / 1000) * speed
  if (t.value < before)
    raf = requestAnimationFrame(tick)
}
function start() {
  cancelAnimationFrame(raf)
  t.value = 0
  t0 = performance.now()
  raf = requestAnimationFrame(tick)
}
watch(active, (a) => {
  if (nav.isPrintMode.value) {
    t.value = 1e9
    return
  }
  if (a)
    setTimeout(start, 400)
  else
    cancelAnimationFrame(raf)
}, { immediate: true })
onBeforeUnmount(() => cancelAnimationFrame(raf))

const filesIn = computed(() => Math.min(FILES, Math.floor((t.value / before) * FILES)))
const packsIn = computed(() => Math.min(PACKS, Math.floor((t.value / after) * PACKS)))
const fmt = (s: number) => s.toLocaleString('ru-RU', { minimumFractionDigits: 1, maximumFractionDigits: 1 })
const clockOld = computed(() => fmt(Math.min(t.value, before)))
const clockNew = computed(() => fmt(Math.min(t.value, after)))

interface Row { label: string, sub: string, menu: [number, number], data: [number, number], live?: boolean }
const rows: Row[] = [
  { label: 'живой сайт, первый визит', sub: 'Vercel, Chromium', menu: [9.26, 2.04], data: [46.45, 4.61], live: true },
  { label: 'стенд: 100 мс на ответ', sub: 'полоса не ограничена', menu: [5.51, 1.36], data: [44.19, 1.89] },
  { label: '+ 50 Мбит/с', sub: '100 мс на ответ', menu: [12.97, 3.75], data: [53.69, 14.14] },
  { label: '+ 20 Мбит/с', sub: '100 мс на ответ', menu: [25.98, 7.76], data: [71.51, 34.22] },
  { label: 'повторный визит', sub: 'живой сайт', menu: [1.64, 1.33], data: [1.92, 0.42], live: true },
]
const panels = [
  { key: 'menu' as const, title: 'до меню', max: 30 },
  { key: 'data' as const, title: 'до всех данных', max: 80 },
]
const PW = 300
const x = (v: number, max: number) => 6 + (Math.min(v, max) / max) * (PW - 12)
const RH = 25
</script>

<template>
  <div class="wp">
    <div class="race">
      <div class="lane">
        <div class="lh">
          <b>было: 1 521 файл — 1 521 запрос</b>
          <span class="x10">часы ×{{ speed }}</span>
          <span class="clk mono">{{ clockOld }} с</span>
        </div>
        <svg :viewBox="`0 0 ${COLS * 4} ${13 * 4}`" class="grid" role="img" aria-label="1 521 квадрат — по одному на файл данных">
          <rect v-for="i in FILES" :key="i" :x="((i - 1) % COLS) * 4" :y="Math.floor((i - 1) / COLS) * 4" width="3" height="3" :class="{ in: i <= filesIn }" />
        </svg>
        <div class="ls">каждый запрос к CDN — 0,2–0,35 с до первого байта; четыре дорожки страницы</div>
      </div>
      <div class="lane">
        <div class="lh">
          <b>стало: 12 пачек</b>
          <span class="clk mono new">{{ clockNew }} с</span>
        </div>
        <div class="packs">
          <div v-for="i in PACKS" :key="i" class="pk" :class="{ in: i <= packsIn, first: i === 1 }">
            <span v-if="i === 1">48 файлов старта · 2,4 МБ</span>
          </div>
        </div>
        <div class="ls">в порядке чтения программы · brotli 11 · хранятся в OPFS · повторный визит не качает ничего</div>
      </div>
    </div>

    <div class="dumb">
      <div v-for="p in panels" :key="p.key" class="dp">
        <div class="dh">{{ p.title }}, с <span class="lg"><i class="o" /> было <i class="n" /> стало</span></div>
        <svg :viewBox="`0 0 ${PW + 150} ${rows.length * RH + 14}`" width="100%" role="img" :aria-label="`${p.title}: было и стало по пяти условиям`">
          <g v-for="(r, i) in rows" :key="r.label" :transform="`translate(0, ${i * RH + 4})`">
            <text x="0" y="11" class="rl" :class="{ live: r.live }">{{ r.label }}</text>
            <text x="0" y="21" class="rs">{{ r.sub }}</text>
            <g transform="translate(150, 0)">
              <line :x1="x(r[p.key][1], p.max)" :x2="x(r[p.key][0], p.max)" y1="12" y2="12" class="bar" />
              <circle :cx="x(r[p.key][0], p.max)" cy="12" r="4.2" class="o" />
              <circle :cx="x(r[p.key][1], p.max)" cy="12" r="4.2" class="n" />
              <text :x="x(r[p.key][0], p.max) + 7" y="15.5" class="vo">{{ fmt(r[p.key][0]) }}{{ r[p.key][0] > p.max ? ' →' : '' }}</text>
              <text :x="x(r[p.key][1], p.max) - 7" y="15.5" text-anchor="end" class="vn">{{ fmt(r[p.key][1]) }}</text>
            </g>
          </g>
        </svg>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wp { display: flex; flex-direction: column; gap: 8px; }
.race { position: relative; display: grid; grid-template-columns: 1.35fr 1fr; gap: 12px; }
.lane { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: 6px 10px 6px; }
.lh { display: flex; justify-content: space-between; align-items: baseline; font-size: 0.68rem; color: var(--ink); margin-bottom: 4px; }
.clk { font-size: 0.8rem; color: var(--s2); }
.clk.new { color: var(--s1); }
.grid { width: 100%; display: block; }
.grid rect { fill: rgba(255, 255, 255, 0.08); }
.grid rect.in { fill: var(--s2); }
.packs { display: grid; grid-template-columns: 0.55fr repeat(11, 1fr); gap: 4px; height: 52px; }
.pk { position: relative; border-radius: 4px; background: rgba(255, 255, 255, 0.08); transition: background 0.15s; }
.pk.in { background: var(--s1); }
.pk.first.in { background: var(--naruto); }
.pk span { position: absolute; left: 0; top: 100%; margin-top: 2px; white-space: nowrap; font-size: 0.54rem; color: var(--ink-2); }
.ls { font-size: 0.58rem; color: var(--muted); margin-top: 4px; line-height: 1.3; }
.packs + .ls { margin-top: 15px; }
.x10 { margin-left: auto; margin-right: 10px; font-size: 0.56rem; color: var(--muted); }
.dumb { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.dp { background: rgba(255, 255, 255, 0.025); border: 1px solid var(--hair); border-radius: 12px; padding: 5px 10px 2px; }
.dh { display: flex; justify-content: space-between; font-size: 0.66rem; color: var(--ink-2); }
.lg { display: inline-flex; align-items: center; gap: 5px; font-size: 0.58rem; color: var(--muted); }
.lg i { display: inline-block; width: 8px; height: 8px; border-radius: 50%; }
.lg i.o, circle.o { background: var(--s2); fill: var(--s2); }
.lg i.n, circle.n { background: var(--s1); fill: var(--s1); }
.bar { stroke: var(--axis); stroke-width: 3; }
.rl { font-size: 10.5px; fill: var(--ink); font-family: var(--font-sans); font-weight: 600; }
.rl.live { fill: var(--naruto); }
.rs { font-size: 9px; fill: var(--muted); font-family: var(--font-sans); }
.vo { font-size: 9.5px; fill: var(--s2); font-family: var(--font-mono); }
.vn { font-size: 9.5px; fill: var(--chakra); font-family: var(--font-mono); }
</style>
