<script setup lang="ts">
import { computed } from 'vue'
import rhythm from '../data/rhythm.json'

const days: string[] = rhythm.days
const cellW = 24
const cellH = 13
const gap = 2
const left = 30
const top = 6
const gridW = days.length * (cellW + gap)
const gridH = 24 * (cellH + gap)
const histX = left + gridW + 26
const histW = 150
const W = histX + histW + 34
const H = top + gridH + 42

// one hue (blue); on the dark surface more commits = lighter step, empty cells recede
const ramp = ['#184f95', '#1c5cab', '#256abf', '#2a78d6', '#3987e5', '#6da7ec']
const color = (n: number) => ramp[Math.min(n, ramp.length) - 1]

const cellMap = computed(() => {
  const mp = new Map<string, number>()
  for (const c of rhythm.cells)
    mp.set(`${c.date}|${c.hour}`, c.n)
  return mp
})
const cells = computed(() => {
  const out: { x: number, y: number, n: number, date: string, hour: number }[] = []
  days.forEach((d, i) => {
    for (let h = 0; h < 24; h++) {
      out.push({ x: left + i * (cellW + gap), y: top + h * (cellH + gap), n: cellMap.value.get(`${d}|${h}`) ?? 0, date: d, hour: h })
    }
  })
  return out
})
const hours: number[] = rhythm.hours
const hmax = Math.max(...hours)
const hmin = Math.min(...hours)
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
const dayLabel = (d: string) => new Date(`${d}T12:00:00`).getDate()
const fmtDate = (d: string) => {
  const dt = new Date(`${d}T12:00:00`)
  return `${dt.getDate()} ${months[dt.getMonth()]}`
}
</script>

<template>
  <div class="wrap">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Коммиты по дням и часам">
      <g>
        <text v-for="h in [0, 3, 6, 9, 12, 15, 18, 21]" :key="h" :x="left - 6" :y="top + h * (cellH + gap) + cellH" text-anchor="end" class="tick">
          {{ String(h).padStart(2, '0') }}
        </text>
      </g>
      <rect
        v-for="c in cells" :key="`${c.date}-${c.hour}`" :x="c.x" :y="c.y" :width="cellW" :height="cellH" rx="2"
        :fill="c.n ? color(c.n) : 'rgba(255,255,255,0.035)'"
      >
        <title>{{ fmtDate(c.date) }}, {{ String(c.hour).padStart(2, '0') }}:00 — {{ c.n }} коммит(ов)</title>
      </rect>
      <g>
        <text
          v-for="(d, i) in days" :key="d" :x="left + i * (cellW + gap) + cellW / 2" :y="top + gridH + 15"
          text-anchor="middle" class="tick"
        >
          {{ dayLabel(d) }}
        </text>
        <text :x="left + cellW / 2" :y="top + gridH + 33" class="month" text-anchor="middle">сен</text>
        <text :x="left + days.indexOf('2026-10-01') * (cellW + gap) + cellW / 2" :y="top + gridH + 33" class="month" text-anchor="middle">окт</text>
      </g>
      <!-- marginal: commits per hour of day -->
      <g>
        <line :x1="histX" :x2="histX" :y1="top - 2" :y2="top + gridH" stroke="var(--axis)" stroke-width="1" />
        <g v-for="(v, h) in hours" :key="`h${h}`">
          <path
            :d="`M${histX},${top + h * (cellH + gap)} h${(v / hmax) * histW - 3} q3,0 3,3 v${cellH - 6} q0,3 -3,3 h${-(v / hmax) * histW + 3} Z`"
            fill="var(--s1)"
          >
            <title>{{ String(h).padStart(2, '0') }}:00–{{ String(h).padStart(2, '0') }}:59 — {{ v }} коммит(ов) за всё время</title>
          </path>
          <text v-if="v === hmax || v === hmin" :x="histX + (v / hmax) * histW + 5" :y="top + h * (cellH + gap) + cellH" class="val">{{ v }}</text>
        </g>
        <text :x="histX" :y="top + gridH + 15" class="tick">всего по часам суток</text>
      </g>
    </svg>
    <div class="legend">
      <span class="muted">коммитов в час:</span>
      <span v-for="(c, i) in ramp" :key="c" class="step"><i :style="{ background: c }" />{{ i + 1 }}{{ i === ramp.length - 1 ? '' : '' }}</span>
      <span class="step"><i style="background: rgba(255,255,255,0.035); outline: 1px solid var(--hair)" />0</span>
    </div>
  </div>
</template>

<style scoped>
.tick {
  /* the chart renders at ~0.7 scale: 13px here is ~9px (0.57rem) on the slide */
  font-size: 13px;
  fill: var(--muted);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
}
.month {
  font-size: 13px;
  fill: var(--muted);
  font-family: var(--font-pixel);
}
.val {
  font-size: 13px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
  font-weight: 600;
}
.legend {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.66rem;
  color: var(--ink-2);
  margin-top: 0.2rem;
}
.step {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}
.step i {
  width: 14px;
  height: 8px;
  border-radius: 2px;
  display: inline-block;
}
rect:hover {
  stroke: var(--ink);
  stroke-width: 1;
}
</style>
