<script setup lang="ts">
// Chapter 18, MENU_MEMORY result: how much the AppKit app's live heap grew during each soak, before
// (tw-w3e) and after the fix (mm-2), with the iteration-history nodes left at the end. Hover a bar.
// Data: data/rel_memory.json (scripts/collect_release.py).
import mem from '../data/rel_memory.json'

const soaks = (mem as any).soaks as any[]
const nf = new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 1, maximumFractionDigits: 1 })
const ni = new Intl.NumberFormat('ru-RU')
const sign = (v: number) => (v > 0 ? '+' : v < 0 ? '−' : '') + nf.format(Math.abs(v))

const W = 400
const rowH = 66
const H = soaks.length * rowH + 4
const lx = 0
const bx = 0
const bw = 268
const MAX = 130
const len = (v: number) => Math.max(0, (v / MAX) * bw)
const BAR = 13
const when = (s: any) => (s.minutes ? `${s.minutes} мин простоя` : '60 000 игровых шагов, виртуальные часы')
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Прирост живой кучи за прогон до и после правки">
    <g v-for="(s, i) in soaks" :key="s.id" :transform="`translate(0, ${i * rowH})`">
      <text class="nm" :x="lx" y="11">{{ s.label }} <tspan class="sub">· {{ when(s) }}</tspan></text>
      <g>
        <title>до правки: {{ ni.format(s.before.startMB) }} → {{ ni.format(s.before.endMB) }} МБ живой кучи, узлов истории {{ ni.format(s.before.nodesStart) }} → {{ ni.format(s.before.nodesEnd) }}</title>
        <path :d="`M${bx},18 h${len(s.before.growthMB) - 4} q4,0 4,4 v${BAR - 8} q0,4 -4,4 h${-(len(s.before.growthMB) - 4)} Z`" fill="var(--s2)" />
        <text class="val" :x="bx + len(s.before.growthMB) + 6" :y="18 + BAR - 3">{{ sign(s.before.growthMB) }} МБ</text>
      </g>
      <g>
        <title>после: {{ ni.format(s.after.startMB) }} → {{ ni.format(s.after.endMB) }} МБ живой кучи, узлов истории {{ s.after.nodesEnd }}</title>
        <path v-if="len(s.after.growthMB) > 5" :d="`M${bx},${20 + BAR} h${len(s.after.growthMB) - 4} q4,0 4,4 v${BAR - 8} q0,4 -4,4 h${-(len(s.after.growthMB) - 4)} Z`" fill="var(--s1)" />
        <rect v-else :x="bx" :y="20 + BAR" width="3" :height="BAR" rx="1.5" fill="var(--s1)" />
        <text class="val" :x="bx + Math.max(3, len(s.after.growthMB)) + 6" :y="20 + BAR * 2 - 3">{{ sign(s.after.growthMB) }} МБ</text>
      </g>
      <text class="nodes" :x="W" :y="18 + BAR - 3" text-anchor="end">{{ ni.format(s.before.nodesEnd) }} узл.</text>
      <text class="nodes" :x="W" :y="20 + BAR * 2 - 3" text-anchor="end">{{ s.after.nodesEnd }} узл.</text>
    </g>
  </svg>
</template>

<style scoped>
.nm { font-size: 11.5px; fill: var(--ink); font-weight: 600; font-family: var(--font-sans); }
.sub { fill: var(--muted); font-weight: 400; font-size: 10.5px; }
.val { font-size: 11px; fill: var(--ink); font-weight: 650; font-family: var(--font-sans); font-variant-numeric: tabular-nums; }
.nodes { font-size: 10.5px; fill: var(--ink-2); font-family: var(--font-sans); font-variant-numeric: tabular-nums; }
</style>
