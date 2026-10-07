<script setup lang="ts">
// Render pipelining (phases 1c, 1e, 1f; design: CORE_REALTIME_RENDER.md) as a schematic swimlane: before, the
// main thread computed a tick and then drew it; after, it validates the draws (phase A) and a serial render
// thread applies the pixels, crop and present (phase B) while the main thread computes the next tick.
// Not to scale. The four result cards read data/perf_ladder.json (scripts/collect_perf.py).
import { useNav, useSlideContext } from '@slidev/client'
import data from '../data/perf_ladder.json'

const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const shown = (k: number) => !props.stepwise || nav.isPrintMode.value || ($clicks?.value ?? 0) >= k

const W = 884
const H = 150
const L = 132
const U = 205 // px per schematic "before" tick
const A = 0.7 // core work share of a tick
const D = 0.3 // drawing share of a tick
const V = 0.07 // phase A: validation on the main thread
const R = W - 6
const before: { x: number, w: number, kind: 'core' | 'draw', n: number }[] = []
for (let n = 0, t = L; t < R; n++) {
  before.push({ x: t, w: U * A, kind: 'core', n })
  before.push({ x: t + U * A, w: U * D, kind: 'draw', n })
  t += U
}
const main: { x: number, w: number, kind: 'core' | 'check', n: number }[] = []
const render: { x: number, w: number, n: number }[] = []
for (let n = 0, t = L; t < R; n++) {
  main.push({ x: t, w: U * A, kind: 'core', n })
  main.push({ x: t + U * A, w: U * V, kind: 'check', n })
  render.push({ x: t + U * (A + V), w: U * D, n })
  t += U * (A + V)
}
const clip = (x: number, w: number) => Math.max(0, Math.min(w, R - x) - 2)
const yB = 30
const yM = 84
const yR = 116
const h = 22

const steps = Object.fromEntries((data as any).steps.map((s: any) => [s.id, s]))
const pct = (a: number, b: number) => `${b > a ? '+' : '−'}${Math.abs((b / a - 1) * 100).toFixed(1).replace('.', ',').replace(/,0$/, '')} %`
const f = (v: number) => v.toFixed(1).replace('.', ',')
const g = steps['1g'].renderToMain as [number, number]
const cards = [
  { id: '1c', hash: steps['1c'].hash, title: 'Пиксели батча — в поток рендера', from: `${f(steps['2b'].ticksPerSecond)} → ${f(steps['1c'].ticksPerSecond)} тика/с`, d: pct(steps['2b'].ticksPerSecond, steps['1c'].ticksPerSecond) },
  { id: '1e', hash: steps['1e'].hash, title: 'Текст больше не ждёт рендер', from: `${f(steps['1d'].ticksPerSecond)} → ${f(steps['1e'].ticksPerSecond)} тика/с`, d: pct(steps['1d'].ticksPerSecond, steps['1e'].ticksPerSecond) },
  { id: '1g', hash: steps['1g'].hash, title: 'Флаг «все пиксели известны»', from: `рендер/главный ${String(g[0]).replace('.', ',')} → ${String(g[1]).replace('.', ',')}`, d: pct(g[0], g[1]) },
  { id: '1i', hash: steps['1i'].hash, title: 'Три буфера crop вместо нового на кадр', from: `рендер ${f(steps.A1.renderMs)} → ${f(steps['1i'].renderMs)} мс на тик`, d: pct(steps.A1.renderMs, steps['1i'].renderMs) },
]
</script>

<template>
  <div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Схема: до — главный поток считает и рисует; после — рисование идёт в отдельном потоке параллельно со следующим тиком">
      <text x="0" :y="yB + 15" class="lane">до · главный поток</text>
      <g v-for="(s, i) in before" :key="`b${i}`">
        <rect v-if="clip(s.x, s.w) > 0" :x="s.x" :y="yB" :width="clip(s.x, s.w)" :height="h" rx="3" :fill="s.kind === 'core' ? 'var(--s2)' : 'var(--s1)'" />
        <text v-if="s.kind === 'core' && clip(s.x, s.w) > 70" :x="s.x + 8" :y="yB + 15" class="in">ядро: тик {{ s.n === 0 ? 'N' : `N+${s.n}` }}</text>
        <text v-if="s.kind === 'draw' && clip(s.x, s.w) > 50" :x="s.x + 6" :y="yB + 15" class="in">пиксели</text>
      </g>

      <g :class="{ off: !shown(1) }" class="after">
        <line :x1="0" :x2="W" :y1="yM - 16" :y2="yM - 16" stroke="var(--grid)" />
        <text x="0" :y="yM + 15" class="lane">после · главный</text>
        <text x="0" :y="yR + 15" class="lane">после · рендер</text>
        <g v-for="(s, i) in main" :key="`m${i}`">
          <rect v-if="clip(s.x, s.w) > 0" :x="s.x" :y="yM" :width="clip(s.x, s.w)" :height="h" rx="3" :fill="s.kind === 'core' ? 'var(--s2)' : 'var(--ink-2)'" />
          <text v-if="s.kind === 'core' && clip(s.x, s.w) > 70" :x="s.x + 8" :y="yM + 15" class="in">ядро: тик {{ s.n === 0 ? 'N' : `N+${s.n}` }}</text>
        </g>
        <g v-for="(s, i) in render" :key="`r${i}`">
          <rect v-if="clip(s.x, s.w) > 0" :x="s.x" :y="yR" :width="clip(s.x, s.w)" :height="h" rx="3" fill="var(--s1)" />
          <text v-if="clip(s.x, s.w) > 50" :x="s.x + 6" :y="yR + 15" class="in">кадр {{ s.n === 0 ? 'N' : `N+${s.n}` }}</text>
          <path v-if="s.x < R - 10" :d="`M${s.x - 4},${yM + h + 1} L${s.x + 2},${yR - 1}`" stroke="var(--muted)" stroke-width="1" fill="none" />
        </g>
      </g>
    </svg>
    <div class="legend">
      <span><i class="sw" style="background: var(--s2)" />ядро игры</span>
      <span><i class="sw" style="background: var(--s1)" />пиксели, crop, окно</span>
      <span :class="{ off: !shown(1) }" class="after"><i class="sw" style="background: var(--ink-2)" />проверки рисования — на главном, в том же порядке</span>
      <span class="muted">схема, не в масштабе</span>
    </div>
    <div class="cards">
      <div v-for="c in cards" :key="c.id" class="card">
        <div class="top">
          <span class="pixel id">{{ c.id }}</span><code>{{ c.hash }}</code>
        </div>
        <div class="t">
          {{ c.title }}
        </div>
        <div class="d">
          {{ c.d }}
        </div>
        <div class="from">
          {{ c.from }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.lane {
  font-size: 11px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.in {
  font-size: 10.5px;
  font-weight: 600;
  fill: #fff;
  font-family: var(--font-sans);
}
.after {
  transition: opacity 0.4s ease;
}
.off {
  opacity: 0;
}
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem 1.1rem;
  font-size: 0.66rem;
  color: var(--ink-2);
  margin: 0.15rem 0 0.7rem;
}
.legend span {
  display: inline-flex;
  align-items: center;
}
.sw {
  display: inline-block;
  width: 12px;
  height: 10px;
  border-radius: 2px;
  margin-right: 0.4rem;
}
.cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.7rem;
}
.card {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.55rem 0.75rem 0.6rem;
  overflow: hidden;
}
.card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 3px;
  width: 36px;
  background: var(--s1);
}
.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.top code {
  font-size: 0.62rem !important;
}
.id {
  font-size: 0.8rem;
  color: var(--naruto);
}
.t {
  font-size: 0.72rem;
  line-height: 1.25;
  color: var(--ink);
  font-weight: 600;
  margin-top: 0.25rem;
  min-height: 1.8rem;
}
.d {
  font-size: 1.35rem;
  font-weight: 650;
  color: var(--ink);
  line-height: 1.1;
  margin-top: 0.15rem;
}
.from {
  font-size: 0.64rem;
  color: var(--muted);
  margin-top: 0.15rem;
}
</style>
