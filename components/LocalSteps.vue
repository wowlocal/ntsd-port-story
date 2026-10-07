<script setup lang="ts">
// Eight local speed steps on the Galaxy A12 (5-6 Oct, before the redesign branch): game ticks per second after
// each step against the original's own rate. The last step is within noise by its own evidence.
// Data: data/perf_local.json (scripts/collect_perf.py).
import data from '../data/perf_local.json'

interface Step { step: string, what: string, ticksPerSecond: number, hash: string, noise?: boolean }
const steps = (data as any).steps as Step[]
const rate = (data as any).gameRate as number

const W = 470
const H = 250
const m = { l: 30, r: 26, t: 22, b: 26 }
const YMAX = 32
const y = (v: number) => m.t + (1 - v / YMAX) * (H - m.t - m.b)
const slot = (W - m.l - m.r) / steps.length
const bw = 22
const cx = (i: number) => m.l + slot * (i + 0.5)
const short: Record<string, string> = { 'start': 'старт', 'steps 1–2': '1–2', 'step 3': '3', 'steps 3–4': '4', 'steps 3–5': '5', 'step 6': '6', 'step 6b': '6b', 'step 7': '7', 'step 8': '8' }
const f = (v: number) => String(v).replace('.', ',')
const best = Math.max(...steps.map(s => s.ticksPerSecond))
const bestI = steps.findIndex(s => s.ticksPerSecond === best)
const gx = W - m.r + 16
const ratio = (rate / best).toFixed(1).replace('.', ',')
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Тики в секунду на Galaxy A12 после каждого локального шага">
    <g v-for="t in [0, 10, 20]" :key="t">
      <line :x1="m.l" :x2="W - m.r" :y1="y(t)" :y2="y(t)" stroke="var(--grid)" />
      <text :x="m.l - 6" :y="y(t) + 3.5" text-anchor="end" class="tick">{{ t }}</text>
    </g>
    <!-- the original's rate -->
    <line :x1="m.l" :x2="W - m.r + 30" :y1="y(rate)" :y2="y(rate)" stroke="var(--ink-2)" stroke-width="1.5" />
    <text :x="m.l + 2" :y="y(rate) - 7" class="ref">темп оригинала ≈ {{ rate }} тиков/с</text>

    <!-- the gap -->
    <path :d="`M${gx - 5},${y(rate) + 2} H${gx} V${y(best) - 2} H${gx - 5}`" fill="none" stroke="var(--naruto)" stroke-width="1.3" />
    <text :x="gx - 10" :y="(y(rate) + y(best)) / 2 - 4" text-anchor="end" class="gap">до темпа оригинала</text>
    <text :x="gx - 10" :y="(y(rate) + y(best)) / 2 + 13" text-anchor="end" class="gapv">не хватает ×{{ ratio }}</text>
    <line :x1="cx(bestI) + bw / 2 + 3" :x2="gx - 6" :y1="y(best)" :y2="y(best)" stroke="var(--naruto)" stroke-width="1" stroke-dasharray="2 3" />

    <g v-for="(s, i) in steps" :key="s.step">
      <title>{{ short[s.step] }} · {{ s.hash }} — {{ s.what }}: {{ f(s.ticksPerSecond) }} тика/с{{ s.noise ? ' (в пределах шума)' : '' }}</title>
      <path v-if="!s.noise" :d="`M${cx(i) - bw / 2},${y(0)} V${y(s.ticksPerSecond) + 4} q0,-4 4,-4 h${bw - 8} q4,0 4,4 V${y(0)} Z`" :fill="i === 0 ? 'var(--axis)' : 'var(--s2)'" />
      <rect v-else :x="cx(i) - bw / 2 + 0.75" :y="y(s.ticksPerSecond) + 0.75" :width="bw - 1.5" :height="y(0) - y(s.ticksPerSecond) - 0.75" rx="3" fill="none" stroke="var(--s2)" stroke-width="1.5" stroke-dasharray="3 2.5" />
      <text :x="cx(i)" :y="y(s.ticksPerSecond) - 6" text-anchor="middle" class="val">{{ f(s.ticksPerSecond) }}</text>
      <text :x="cx(i)" :y="H - m.b + 15" text-anchor="middle" class="step">{{ short[s.step] }}</text>
    </g>
    <text :x="cx(steps.length - 1)" :y="y(steps[steps.length - 1].ticksPerSecond) - 20" text-anchor="middle" class="noise">шум</text>
    <line :x1="m.l" :x2="W - m.r" :y1="y(0)" :y2="y(0)" stroke="var(--axis)" />
  </svg>
</template>

<style scoped>
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
}
.ref {
  font-size: 11px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.gap {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.gapv {
  font-size: 14px;
  font-weight: 700;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.val {
  font-size: 11.5px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.step {
  font-size: 11px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.noise {
  font-size: 10.5px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
</style>
