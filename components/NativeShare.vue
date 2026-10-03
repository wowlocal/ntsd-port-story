<script setup lang="ts">
import { computed } from 'vue'
import daily from '../data/daily.json'

// Emphasis form: commits that touched native/Sources in the accent hue, the rest in gray.
const W = 900
const H = 230
const m = { l: 34, r: 8, t: 14, b: 38 }
const plotW = W - m.l - m.r
const plotH = H - m.t - m.b
const n = daily.length
const band = plotW / n
const bw = Math.min(22, band * 0.7)
const maxV = 60
const y = (v: number) => m.t + plotH - (v / maxV) * plotH
const x = (i: number) => m.l + i * band + (band - bw) / 2
const ticks = [0, 20, 40, 60]
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']

function top(x0: number, y0: number, w: number, h: number, r: number) {
  const rr = Math.min(r, h, w / 2)
  return `M${x0},${y0 + h} L${x0},${y0 + rr} Q${x0},${y0} ${x0 + rr},${y0} L${x0 + w - rr},${y0} Q${x0 + w},${y0} ${x0 + w},${y0 + rr} L${x0 + w},${y0 + h} Z`
}

const bars = computed(() => daily.map((d: any, i: number) => {
  const dt = new Date(`${d.date}T12:00:00`)
  const nat = d.native
  const rest = d.commits - d.native
  const yN = y(nat)
  const out: { path: string, fill: string, title: string }[] = []
  if (nat > 0) {
    out.push({
      path: rest > 0 ? `M${x(i)},${yN} h${bw} v${y(0) - yN} h${-bw} Z` : top(x(i), yN, bw, y(0) - yN, 4),
      fill: 'var(--s2)',
      title: `${dt.getDate()} ${months[dt.getMonth()]}: ${nat} из ${d.commits} коммитов трогали native/Sources`,
    })
  }
  if (rest > 0) {
    const yT = y(d.commits)
    const h = (nat > 0 ? yN - 2 : y(0)) - yT
    out.push({
      path: top(x(i), yT, bw, Math.max(0, h), 4),
      fill: '#4a5163',
      title: `${dt.getDate()} ${months[dt.getMonth()]}: ${rest} из ${d.commits} — только инструменты, карточки, evidence`,
    })
  }
  return { i, d, out, day: dt.getDate(), month: dt.getMonth() }
}))
</script>

<template>
  <div>
    <div class="legend">
      <span><i class="swatch" style="background: var(--s2)" />коммит менял код игры в <code>native/Sources</code></span>
      <span><i class="swatch" style="background: #4a5163" />только инструменты, карточки, evidence, кандидаты вне <code>native/</code></span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Доля коммитов, менявших native/Sources">
      <line v-for="t in ticks" :key="t" :x1="m.l" :x2="W - m.r" :y1="y(t)" :y2="y(t)" :stroke="t === 0 ? 'var(--axis)' : 'var(--grid)'" />
      <text v-for="t in ticks" :key="`t${t}`" :x="m.l - 8" :y="y(t) + 3.5" text-anchor="end" class="tick">{{ t }}</text>
      <g v-for="b in bars" :key="b.i">
        <path v-for="(s, k) in b.out" :key="k" :d="s.path" :fill="s.fill"><title>{{ s.title }}</title></path>
        <text :x="x(b.i) + bw / 2" :y="H - m.b + 15" text-anchor="middle" class="tick" :class="{ strong: b.d.commits > 0 }">{{ b.day }}</text>
        <text v-if="b.i === 0 || b.day === 1" :x="x(b.i) + bw / 2" :y="H - m.b + 30" text-anchor="middle" class="month">{{ months[b.month] }}</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.legend {
  display: flex;
  gap: 1.2rem;
  font-size: 0.7rem;
  color: var(--ink-2);
  margin-bottom: 0.2rem;
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
}
.tick.strong {
  fill: var(--ink-2);
}
.month {
  font-size: 10px;
  fill: var(--muted);
}
</style>
