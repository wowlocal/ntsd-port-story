<script setup lang="ts">
import data from '../data/codex_limits.json'

// Percent of the weekly Codex limit burned per local day: port sessions below, the rest of the
// account above. The dashed line is the pace at which one weekly limit lasts exactly seven days.
const burn = (data as any).burn as Record<string, { port?: number, other?: number }>
const WEEK_USD = (200 * 12) / 52.1786
const days: string[] = []
for (let t = Date.parse('2026-09-07T12:00Z'); t <= Date.parse('2026-10-03T12:00Z'); t += 864e5)
  days.push(new Date(t).toISOString().slice(0, 10))

const W = 900
const H = 220
const m = { l: 44, r: 8, t: 14, b: 34 }
const yMax = 160
const plotH = H - m.t - m.b
const band = (W - m.l - m.r) / days.length
const bw = Math.min(20, band * 0.66)
const y = (v: number) => m.t + plotH - (v / yMax) * plotH
const x = (i: number) => m.l + i * band + (band - bw) / 2
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
const NORM = 100 / 7

// A rounded-top bar from v0 up to v1; only the topmost segment gets rounded corners.
function seg(i: number, v0: number, v1: number, top: boolean) {
  const x0 = x(i)
  const x1 = x0 + bw
  const y0 = y(v0) - (v0 > 0 ? 1 : 0)
  const y1 = y(v1)
  const r = top ? Math.min(4, (y0 - y1) / 2) : 0
  return `M${x0},${y0} L${x0},${y1 + r} Q${x0},${y1} ${x0 + r},${y1} L${x1 - r},${y1} Q${x1},${y1} ${x1},${y1 + r} L${x1},${y0} Z`
}
const bars = days.map((d, i) => {
  const port = burn[d]?.port ?? 0
  const other = burn[d]?.other ?? 0
  const dt = new Date(`${d}T12:00:00Z`)
  return { i, d, port, other, total: port + other, day: dt.getUTCDate(), month: dt.getUTCMonth() }
})
const pauseFrom = days.indexOf('2026-09-15')
const pauseTo = days.indexOf('2026-09-21')
const usd = (v: number) => `$${Math.round((v / 100) * WEEK_USD)}`
</script>

<template>
  <div>
    <div class="legend">
      <span><i class="key" style="background: var(--s1)" />сессии порта</span>
      <span><i class="key" style="background: #646b7a" />другие проекты аккаунта</span>
      <span><i class="key dash" />норма: 14 % в день — так недельного лимита хватает на 7 дней</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Сколько недельного лимита Codex сгорало в день">
      <rect :x="m.l + pauseFrom * band + 1" :y="m.t" :width="(pauseTo - pauseFrom + 1) * band - 2" :height="plotH" fill="rgba(255,255,255,0.035)" rx="5" />
      <text :x="m.l + (pauseFrom + (pauseTo - pauseFrom + 1) / 2) * band" :y="y(118)" text-anchor="middle" class="pause">пауза в порте</text>
      <line v-for="v in [0, 50, 100, 150]" :key="v" :x1="m.l" :x2="W - m.r" :y1="y(v)" :y2="y(v)" :stroke="v === 0 ? 'var(--axis)' : 'var(--grid)'" />
      <text v-for="v in [0, 50, 100, 150]" :key="`t${v}`" :x="m.l - 7" :y="y(v) + 3.5" text-anchor="end" class="tick">{{ v }} %</text>
      <g v-for="b in bars" :key="b.d">
        <path v-if="b.port > 0" :d="seg(b.i, 0, b.port, b.other <= 0)" fill="var(--s1)" />
        <path v-if="b.other > 0" :d="seg(b.i, b.port, b.total, true)" fill="#646b7a" />
        <rect :x="x(b.i) - 2" :y="m.t" :width="bw + 4" :height="plotH" fill="transparent">
          <title>{{ b.day }} {{ months[b.month] }}: порт {{ b.port }} %, другие {{ b.other }} % недельного лимита · ≈ {{ usd(b.total) }} по номиналу</title>
        </rect>
        <text v-if="b.total >= 60" :x="x(b.i) + bw / 2" :y="y(b.total) - 5" text-anchor="middle" class="val">{{ Math.round(b.total) }} %</text>
        <text :x="x(b.i) + bw / 2" :y="H - m.b + 14" text-anchor="middle" class="tick">{{ b.day }}</text>
        <text v-if="b.i === 0 || b.day === 1" :x="x(b.i) + bw / 2" :y="H - m.b + 28" text-anchor="middle" class="tick">{{ months[b.month] }}</text>
      </g>
      <line :x1="m.l" :x2="W - m.r" :y1="y(NORM)" :y2="y(NORM)" stroke="var(--ink-2)" stroke-width="1.2" stroke-dasharray="4 3" />
    </svg>
  </div>
</template>

<style scoped>
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem 1.1rem;
  font-size: 0.62rem;
  color: var(--ink-2);
  margin-bottom: 0.1rem;
}
.key {
  display: inline-block;
  width: 12px;
  height: 8px;
  border-radius: 2px;
  margin-right: 0.38rem;
  vertical-align: middle;
}
.key.dash {
  height: 0;
  border-top: 1.5px dashed var(--ink-2);
  border-radius: 0;
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.val {
  font-size: 10.5px;
  font-weight: 600;
  fill: var(--ink);
  font-variant-numeric: tabular-nums;
}
.pause {
  font-size: 10px;
  fill: var(--muted);
}
</style>
