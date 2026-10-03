<script setup lang="ts">
import { computed } from 'vue'
import demo from '../data/evidence/demo-frames.json'

// RNG index (0..2999) of the original and of the Mac at every third tick of the Demo, seed 777.
const W = 900
const H = 230
const m = { l: 46, r: 12, t: 14, b: 30 }
const plotW = W - m.l - m.r
const plotH = H - m.t - m.b
const rows = (demo as any).rows as number[][]
const t0 = rows[0][0]
const t1 = rows[rows.length - 1][0]
const x = (t: number) => m.l + ((t - t0) / (t1 - t0)) * plotW
const y = (v: number) => m.t + plotH - (v / 3000) * plotH

function path(col: number) {
  let d = ''
  rows.forEach((r, i) => {
    const prev = rows[i - 1]
    const jump = prev && r[col] < prev[col]
    d += `${i === 0 || jump ? 'M' : 'L'}${x(r[0]).toFixed(1)},${y(r[col]).toFixed(1)} `
  })
  return d
}
const orig = computed(() => path(1))
const mac = computed(() => path(3))
const firstDiff = (demo as any).firstDifferentTick as number
const equalTo = (demo as any).equalTo as number
const ticks = [150, 300, 450, 600, 750, 900, 1050]
</script>

<template>
  <div>
    <div class="legend">
      <span><i class="key wide" />оригинал под CrossOver (широкая полоса)</span>
      <span><i class="key" />Mac (линия поверх)</span>
      <span class="muted">индекс таблицы ГСЧ 0x450bcc, каждый третий тик, seed 777</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Индекс генератора случайных чисел в двух программах">
      <rect :x="x(firstDiff)" :y="m.t" :width="x(t1) - x(firstDiff)" :height="plotH" fill="rgba(208,59,59,0.10)" />
      <line v-for="v in [0, 1000, 2000, 3000]" :key="v" :x1="m.l" :x2="W - m.r" :y1="y(v)" :y2="y(v)" :stroke="v === 0 ? 'var(--axis)' : 'var(--grid)'" />
      <text v-for="v in [0, 1000, 2000, 3000]" :key="`y${v}`" :x="m.l - 8" :y="y(v) + 3.5" text-anchor="end" class="tick">{{ v }}</text>
      <text v-for="t in ticks" :key="t" :x="x(t)" :y="H - 10" text-anchor="middle" class="tick">{{ t }}</text>
      <path :d="orig" fill="none" stroke="var(--s2)" stroke-width="6" stroke-linejoin="round" style="stroke-opacity: 0.45" />
      <path :d="mac" fill="none" stroke="var(--s1)" stroke-width="2" stroke-linejoin="round" />
      <line :x1="x(firstDiff)" :x2="x(firstDiff)" :y1="m.t" :y2="m.t + plotH" stroke="var(--critical)" stroke-width="1.5" />
      <text :x="x(firstDiff) + 6" :y="m.t + 12" class="ann">тик {{ firstDiff }}: первое расхождение</text>
      <text :x="x(equalTo) - 6" :y="m.t + 12" text-anchor="end" class="ann2">совпадают с 150 по {{ equalTo }}</text>
    </svg>
  </div>
</template>

<style scoped>
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem 1.2rem;
  font-size: 0.68rem;
  color: var(--ink-2);
  margin-bottom: 0.2rem;
  align-items: center;
}
.key {
  display: inline-block;
  width: 16px;
  height: 2px;
  background: var(--s1);
  margin-right: 0.4rem;
  vertical-align: middle;
}
.key.wide {
  height: 6px;
  background: var(--s2);
  opacity: 0.6;
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.ann {
  font-size: 11px;
  font-weight: 600;
  fill: var(--ink);
  paint-order: stroke;
  stroke: var(--bg);
  stroke-width: 4px;
  stroke-linejoin: round;
}
.ann2 {
  font-size: 11px;
  fill: var(--ink-2);
  paint-order: stroke;
  stroke: var(--bg);
  stroke-width: 4px;
  stroke-linejoin: round;
}
</style>
