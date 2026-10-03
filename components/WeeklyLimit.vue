<script setup lang="ts">
import { computed } from 'vue'
import data from '../data/sessions.json'
import daily from '../data/daily.json'

// Highest weekly Codex rate-limit usage seen each day (one series; days at 100 % emphasised).
const lim = (data as any).codex.weekly_limit_by_day as Record<string, { used: number, resets: string }>
const W = 900
const H = 210
const m = { l: 44, r: 8, t: 24, b: 38 }
const plotW = W - m.l - m.r
const plotH = H - m.t - m.b
const n = daily.length
const band = plotW / n
const bw = Math.min(22, band * 0.7)
const y = (v: number) => m.t + plotH - (v / 100) * plotH
const x = (i: number) => m.l + i * band + (band - bw) / 2
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
const bars = computed(() => daily.map((d: any, i: number) => {
  const v = lim[d.date]?.used
  const dt = new Date(`${d.date}T12:00:00`)
  return { i, v, date: d.date, day: dt.getDate(), month: dt.getMonth(), resets: lim[d.date]?.resets }
}))
const resetIdx = daily.findIndex((d: any) => d.date === '2026-09-20')
const pauseFrom = daily.findIndex((d: any) => d.date === '2026-09-15')
const pauseTo = daily.findIndex((d: any) => d.date === '2026-09-21')
</script>

<template>
  <div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Недельный лимит Codex по дням">
      <rect :x="m.l + pauseFrom * band + 2" :y="m.t" :width="(pauseTo - pauseFrom + 1) * band - 4" :height="plotH" fill="rgba(255,255,255,0.03)" rx="6" />
      <text :x="m.l + (pauseFrom + (pauseTo - pauseFrom + 1) / 2) * band" :y="y(50)" text-anchor="middle" class="pause">коммитов нет</text>
      <line v-for="t in [0, 50, 100]" :key="t" :x1="m.l" :x2="W - m.r" :y1="y(t)" :y2="y(t)" :stroke="t === 0 ? 'var(--axis)' : 'var(--grid)'" />
      <text v-for="t in [0, 50, 100]" :key="`t${t}`" :x="m.l - 8" :y="y(t) + 3.5" text-anchor="end" class="tick">{{ t }} %</text>
      <g v-for="b in bars" :key="b.i">
        <path
          v-if="b.v !== undefined"
          :d="`M${x(b.i)},${y(0)} L${x(b.i)},${y(b.v) + 4} Q${x(b.i)},${y(b.v)} ${x(b.i) + 4},${y(b.v)} L${x(b.i) + bw - 4},${y(b.v)} Q${x(b.i) + bw},${y(b.v)} ${x(b.i) + bw},${y(b.v) + 4} L${x(b.i) + bw},${y(0)} Z`"
          :fill="b.v >= 100 ? 'var(--s2)' : 'var(--s1)'"
        >
          <title>{{ b.date }}: до {{ b.v }} % недельного лимита · сброс {{ b.resets?.slice(0, 16) }} UTC</title>
        </path>
        <text v-if="b.v !== undefined && b.v >= 96" :x="x(b.i) + bw / 2" :y="y(b.v) - 6" text-anchor="middle" class="val">{{ b.v }} %</text>
        <text :x="x(b.i) + bw / 2" :y="H - m.b + 15" text-anchor="middle" class="tick">{{ b.day }}</text>
        <text v-if="b.i === 0 || b.day === 1" :x="x(b.i) + bw / 2" :y="H - m.b + 30" text-anchor="middle" class="tick">{{ months[b.month] }}</text>
      </g>
      <line :x1="x(resetIdx) + bw / 2" :x2="x(resetIdx) + bw / 2" :y1="m.t" :y2="y(0)" stroke="var(--s2)" stroke-width="1.5" />
      <text :x="x(resetIdx) + bw / 2 + 5" :y="m.t + 10" class="ann">20 сен, 08:36 МСК — сброс лимита</text>
    </svg>
  </div>
</template>

<style scoped>
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.val {
  font-size: 10.5px;
  font-weight: 600;
  fill: var(--ink);
}
.ann {
  font-size: 10.5px;
  fill: var(--ink);
  font-weight: 600;
}
.pause {
  font-size: 10px;
  fill: var(--muted);
}
</style>
