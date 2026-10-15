<script setup lang="ts">
// Chapter 18, MENU_MEMORY result: footprint of the AppKit app during a 60,000-step VS session
// (virtual clock), sampled every 10 s, before (tw-w3e) and after the fix (mm-2). Hover for both values.
// Data: data/rel_memory.json (scripts/collect_release.py).
import { computed, ref } from 'vue'
import mem from '../data/rel_memory.json'

const vs = (mem as any).soaks.find((s: any) => s.id === 'vs')
const B = vs.footprint.before as [number, number][]
const A = vs.footprint.after as [number, number][]
const n = Math.min(B.length, A.length)

const W = 470
const H = 214
const m = { l: 50, r: 108, t: 10, b: 24 }
const X1 = B[n - 1][0]
const Y0 = 650
const Y1 = 900
const x = (s: number) => m.l + (s / X1) * (W - m.l - m.r)
const y = (v: number) => H - m.b - ((v - Y0) / (Y1 - Y0)) * (H - m.t - m.b)
const path = (pts: [number, number][]) => pts.slice(0, n).map((p, i) => `${i ? 'L' : 'M'}${x(p[0]).toFixed(1)},${y(p[1]).toFixed(1)}`).join(' ')
const yTicks = [650, 700, 750, 800, 850, 900]
const xTicks = [0, 60, 120, 180, 240, 300]
const flatFrom = A.findIndex((p, i) => i > 0 && A.slice(i, n).every(q => q[1] === A[n - 1][1]))

const hover = ref<number | null>(null)
function onMove(e: PointerEvent) {
  const svg = (e.currentTarget as SVGRectElement).ownerSVGElement!
  const r = svg.getBoundingClientRect()
  const vx = ((e.clientX - r.left) / r.width) * W
  const s = ((vx - m.l) / (W - m.l - m.r)) * X1
  hover.value = Math.max(0, Math.min(n - 1, Math.round(s / (X1 / (n - 1)))))
}
const tip = computed(() => {
  if (hover.value === null)
    return null
  const i = hover.value
  const tx = x(B[i][0])
  return { x: tx, s: B[i][0], b: B[i][1], a: A[i][1], left: tx > W - m.r - 120 }
})
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`Footprint VS-сессии: до правки ${B[0][1]} → ${B[n - 1][1]} МБ, после ${A[0][1]} → ${A[n - 1][1]} МБ`">
    <g class="gl">
      <line v-for="g in yTicks" :key="g" :x1="m.l" :x2="W - m.r" :y1="y(g)" :y2="y(g)" />
    </g>
    <text v-for="g in yTicks" :key="`y${g}`" class="ax" :x="m.l - 6" :y="y(g) + 3.5" text-anchor="end">{{ g }}{{ g === 900 ? ' МБ' : '' }}</text>
    <text v-for="s in xTicks" :key="`x${s}`" class="ax" :x="x(s)" :y="H - 7" text-anchor="middle">{{ s / 60 }} мин</text>

    <path :d="path(B)" fill="none" stroke="var(--s2)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />
    <path :d="path(A)" fill="none" stroke="var(--s1)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />
    <circle :cx="x(B[n - 1][0])" :cy="y(B[n - 1][1])" r="4" fill="var(--s2)" stroke="var(--surface)" stroke-width="2" />
    <circle :cx="x(A[n - 1][0])" :cy="y(A[n - 1][1])" r="4" fill="var(--s1)" stroke="var(--surface)" stroke-width="2" />
    <text class="end" :x="x(X1) + 9" :y="y(B[n - 1][1]) + 1"><tspan class="v">{{ B[n - 1][1] }} МБ</tspan></text>
    <text class="endn" :x="x(X1) + 9" :y="y(B[n - 1][1]) + 14">до: всё ещё растёт</text>
    <text class="end" :x="x(X1) + 9" :y="y(A[n - 1][1]) + 4"><tspan class="v">{{ A[n - 1][1] }} МБ</tspan></text>
    <text class="endn" :x="x(X1) + 9" :y="y(A[n - 1][1]) + 17">после: ровно</text>
    <text class="endn" :x="x(X1) + 9" :y="y(A[n - 1][1]) + 30">с {{ A[flatFrom][0] / 60 }}-й минуты</text>

    <g v-if="tip">
      <line :x1="tip.x" :x2="tip.x" :y1="m.t" :y2="H - m.b" stroke="var(--ink-2)" stroke-width="1" />
      <circle :cx="tip.x" :cy="y(tip.b)" r="4" fill="var(--s2)" stroke="var(--surface)" stroke-width="2" />
      <circle :cx="tip.x" :cy="y(tip.a)" r="4" fill="var(--s1)" stroke="var(--surface)" stroke-width="2" />
      <g :transform="`translate(${tip.left ? tip.x - 116 : tip.x + 8}, ${m.t + 2})`">
        <rect width="108" height="46" rx="6" fill="var(--surface-2)" stroke="var(--axis)" />
        <text class="tt" x="8" y="14">{{ tip.s }} с</text>
        <line x1="8" x2="18" y1="25" y2="25" stroke="var(--s2)" stroke-width="2" />
        <text class="tv" x="24" y="28">{{ tip.b }} МБ <tspan class="tn">до</tspan></text>
        <line x1="8" x2="18" y1="38" y2="38" stroke="var(--s1)" stroke-width="2" />
        <text class="tv" x="24" y="41">{{ tip.a }} МБ <tspan class="tn">после</tspan></text>
      </g>
    </g>
    <rect class="hit" :x="m.l" :y="m.t" :width="W - m.l - m.r" :height="H - m.t - m.b" @pointermove="onMove" @pointerleave="hover = null" />
  </svg>
</template>

<style scoped>
.gl line { stroke: var(--grid); stroke-width: 1; }
.ax { font-size: 10px; fill: var(--muted); font-family: var(--font-sans); font-variant-numeric: tabular-nums; }
.end { font-size: 11.5px; font-family: var(--font-sans); }
.end .v { fill: var(--ink); font-weight: 700; }
.endn { font-size: 10.5px; fill: var(--ink-2); font-family: var(--font-sans); }
.tt { font-size: 10px; fill: var(--muted); font-family: var(--font-sans); }
.tv { font-size: 11px; fill: var(--ink); font-weight: 650; font-family: var(--font-sans); font-variant-numeric: tabular-nums; }
.tn { fill: var(--ink-2); font-weight: 400; }
.hit { fill: transparent; cursor: crosshair; }
</style>
