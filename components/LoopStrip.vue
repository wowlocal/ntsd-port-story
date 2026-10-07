<script setup lang="ts">
import loop from '../data/loop.json'

// The four-day Claude Code session after the release, on one time axis (data/loop.json, counters only):
// context size of every main-thread request, the automatic compactions, and three rugs underneath —
// commits, /loop firings and the human's turns. Background bands mark the two chapters and the nights.
const d = loop as any
const W = 884
const x0 = 92
const x1 = W - 8
const tMax = d.points[d.points.length - 1][0] as number // minutes
const X = (t: number) => x0 + (t / tMax) * (x1 - x0)
const top = 26
const cH = 118
const Y = (k: number) => top + cH - (k / 1000) * cH
const line = (d.points as number[][]).map((p, i) => `${i ? 'L' : 'M'}${X(p[0]).toFixed(1)},${Y(p[1]).toFixed(1)}`).join('')
const area = `${line}L${X(tMax).toFixed(1)},${Y(0)}L${X(0)},${Y(0)}Z`

const rug = { commits: top + cH + 24, loop: top + cH + 44, human: top + cH + 64 }
const bottom = rug.human + 14

// local time: the session starts 3 Oct 20:08:25 (+02:00)
const startMin = 20 * 60 + 8 + 25 / 60
const atLocal = (day: number, hh: number, mm = 0) => (day - 3) * 1440 + hh * 60 + mm - startMin
const midnights = [4, 5, 6, 7].map(day => ({ t: atLocal(day, 0), label: `${day} октября` }))
const nights = [4, 5, 6, 7].map(day => [atLocal(day, 0), Math.min(atLocal(day, 6), tMax)])
// chapter 13: until the phone is plugged in (5 Oct 07:26); chapter 14: the phone and the core redesign
const ch = [
  { from: 0, to: atLocal(5, 7, 26), name: 'глава 13 · девять хостов' },
  { from: atLocal(5, 7, 26), to: tMax, name: 'глава 14 · телефон 2008 года' },
]
const ticks = [0, 250, 500, 750, 1000]
const tickLabel = (v: number) => (v === 0 ? '0' : v === 1000 ? '1 млн' : `${v} тыс.`)
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${bottom + 20}`" width="100%" role="img" aria-label="Четыре дня одной сессии агента">
    <!-- chapters and nights -->
    <g v-for="(c, i) in ch" :key="`c${i}`">
      <rect :x="X(c.from)" :y="2" :width="X(c.to) - X(c.from)" height="14" :fill="i ? 'rgba(217,89,38,0.16)' : 'rgba(57,135,229,0.16)'" rx="3" />
      <text class="chn" :x="X(c.from) + 6" y="12.5">{{ c.name }}</text>
    </g>
    <rect v-for="(n, i) in nights" :key="`n${i}`" :x="X(n[0])" :y="top" :width="X(n[1]) - X(n[0])" :height="bottom - top" fill="rgba(57,135,229,0.05)" />

    <!-- context -->
    <line v-for="v in ticks" :key="v" :x1="x0" :x2="x1" :y1="Y(v)" :y2="Y(v)" :stroke="v === 0 ? 'var(--axis)' : 'var(--grid)'" />
    <text v-for="v in ticks" :key="`t${v}`" class="tick" :x="x0 - 8" :y="Y(v) + 3.5" text-anchor="end">{{ tickLabel(v) }}</text>
    <path :d="area" fill="var(--s2)" style="opacity: 0.1" />
    <path :d="line" fill="none" stroke="var(--s2)" stroke-width="1.2" stroke-linejoin="round" />
    <g v-for="(c, i) in d.compactions" :key="`k${i}`">
      <circle :cx="X(c.t)" :cy="Y(c.pre_k)" r="3.5" fill="var(--ink)" stroke="var(--bg)" stroke-width="1.5">
        <title>сжатие контекста: {{ Math.round(c.pre_k) }} тыс. → {{ Math.round(c.post_k) }} тыс. токенов</title>
      </circle>
    </g>
    <text class="lbl" :x="x0 - 8" :y="top - 6" text-anchor="end">контекст</text>

    <!-- rugs -->
    <g>
      <text class="lbl" :x="x0 - 8" :y="rug.commits + 3.5" text-anchor="end">коммиты</text>
      <line v-for="(c, i) in d.commits" :key="`cm${i}`" :x1="X(c.t)" :x2="X(c.t)" :y1="rug.commits - 6" :y2="rug.commits + 6" stroke="var(--s2)" stroke-width="1.4"><title>{{ c.hash }}</title></line>
      <text class="lbl" :x="x0 - 8" :y="rug.loop + 3.5" text-anchor="end">/loop</text>
      <line v-for="(t, i) in d.wakeups" :key="`w${i}`" :x1="X(t)" :x2="X(t)" :y1="rug.loop - 5" :y2="rug.loop + 5" stroke="var(--ink-2)" stroke-width="1.2" />
      <text class="lbl hum" :x="x0 - 8" :y="rug.human + 3.5" text-anchor="end">человек</text>
      <circle v-for="(t, i) in d.human" :key="`h${i}`" :cx="X(Math.max(0, t))" :cy="rug.human" r="3.6" fill="var(--s1)" stroke="var(--bg)" stroke-width="1.2" />
    </g>

    <!-- day axis -->
    <g v-for="m in midnights" :key="m.label">
      <line :x1="X(m.t)" :x2="X(m.t)" :y1="top" :y2="bottom" stroke="var(--axis)" stroke-dasharray="2 3" />
      <text class="day" :x="X(m.t) + 4" :y="bottom + 13">{{ m.label }}</text>
    </g>
    <text class="day" :x="x0" :y="bottom + 13">20:08</text>
  </svg>
</template>

<style scoped>
.tick {
  font-family: var(--font-sans);
  font-size: 9.5px;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.lbl {
  font-family: var(--font-sans);
  font-size: 10.5px;
  font-weight: 600;
  fill: var(--ink-2);
}
.lbl.hum {
  fill: var(--chakra);
}
.chn {
  font-family: var(--font-sans);
  font-size: 9.5px;
  font-weight: 600;
  fill: var(--ink);
}
.day {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--ink-2);
}
</style>
