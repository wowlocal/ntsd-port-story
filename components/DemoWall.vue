<script setup lang="ts">
// Demo-day deck: why the loop stopped. Each bar is one idea left that needed no decision from the author, with the
// plan's own estimate of what it would save (ms per tick); the shaded band is the phone's resolution per run
// (±0.25 ms). Every idea falls inside the noise, so by the commit rule none can be committed.
// Data: data/rt2_wall.json (CORE_REALTIME.md, Next task, 10 Oct; CORE_REALTIME_TIER3.md, Candidates). Estimates, not measurements.
import wall from '../data/rt2_wall.json'

const w = wall as any
const items: { ms: number }[] = w.decisionFree
const res: number = w.resolutionMs
const max = 0.5
const W = 520
const L = 8
const R = 14
const BH = 22
const GAP = 9
const T = 30
const H = T + items.length * (BH + GAP) + 26
const x = (ms: number) => L + (ms / max) * (W - L - R)
const fmt = (v: number) => v.toLocaleString('ru-RU', { maximumFractionDigits: 2 })
</script>

<template>
  <div class="dw">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Шесть оставшихся идей, каждая меньше погрешности замера">
      <rect :x="x(0)" :y="T - 22" :width="x(res) - x(0)" :height="H - T - 4" class="band" />
      <text :x="x(res) - 6" :y="T - 8" text-anchor="end" class="band-t">погрешность замера ±0,25 мс</text>
      <line :x1="x(res)" :x2="x(res)" :y1="T - 22" :y2="H - 26" class="band-edge" />
      <g v-for="(it, i) in items" :key="i" :transform="`translate(0, ${T + i * (BH + GAP)})`">
        <rect :x="x(0)" y="0" :width="x(it.ms) - x(0)" :height="BH" rx="4" class="bar" />
        <text :x="x(it.ms) + 7" :y="BH / 2 + 5" class="val">≈ {{ fmt(it.ms) }} мс</text>
      </g>
      <g class="ax">
        <line :x1="x(0)" :x2="W - R" :y1="H - 22" :y2="H - 22" />
        <text v-for="v in [0, 0.25, 0.5]" :key="v" :x="x(v)" :y="H - 6" text-anchor="middle">{{ fmt(v) }}</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.band { fill: rgba(255, 255, 255, 0.06); }
.band-edge { stroke: var(--muted); stroke-width: 1.2; stroke-dasharray: 4 4; }
.band-t { font-family: var(--font-sans); font-size: 12.5px; fill: var(--ink-2); }
.bar { fill: var(--s1); }
.val { font-family: var(--font-mono); font-size: 12.5px; fill: var(--ink); }
.ax line { stroke: var(--axis); }
.ax text { font-family: var(--font-mono); font-size: 11px; fill: var(--muted); }
</style>
