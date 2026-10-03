<script setup lang="ts">
import data from '../data/claude_burn.json'

// API-equivalent dollars per local day of Claude Code work: the port's sessions, plus the
// session that wrote this deck on top. The dashed line is what one day of the subscription costs.
const d = data as any
const days = Object.entries(d.days as Record<string, { port_usd: number, deck_usd: number, x_subscription: number, active_hours: number }>)
  .map(([date, v]) => ({ date, ...v }))
const DAY = d.plan.price_usd_day as number
const W = 900
const H = 205
const m = { l: 52, r: 10, t: 22, b: 34 }
const yMax = 300
const plotH = H - m.t - m.b
const band = (W - m.l - m.r) / days.length
const bw = Math.min(64, band * 0.52)
const y = (v: number) => m.t + plotH - (v / yMax) * plotH
const x = (i: number) => m.l + i * band + (band - bw) / 2
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
const label = (date: string) => `${Number(date.slice(8, 10))} ${months[Number(date.slice(5, 7)) - 1]}`

function seg(i: number, v0: number, v1: number, top: boolean) {
  const x0 = x(i)
  const x1 = x0 + bw
  const y0 = y(v0) - (v0 > 0 ? 1.5 : 0)
  const y1 = y(v1)
  const r = top ? Math.min(5, (y0 - y1) / 2) : 0
  return `M${x0},${y0} L${x0},${y1 + r} Q${x0},${y1} ${x0 + r},${y1} L${x1 - r},${y1} Q${x1},${y1} ${x1},${y1 + r} L${x1},${y0} Z`
}
</script>

<template>
  <div>
    <div class="legend">
      <span><i class="key" style="background: var(--s2)" />сессии порта</span>
      <span><i class="key" style="background: rgba(217, 89, 38, 0.42)" />сессия, которая делала эту презентацию</span>
      <span><i class="key dash" />день подписки Max 20x: ${{ DAY.toFixed(2).replace('.', ',') }}</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="API-эквивалент Claude Code по дням">
      <line v-for="v in [0, 100, 200, 300]" :key="v" :x1="m.l" :x2="W - m.r" :y1="y(v)" :y2="y(v)" :stroke="v === 0 ? 'var(--axis)' : 'var(--grid)'" />
      <text v-for="v in [0, 100, 200, 300]" :key="`t${v}`" :x="m.l - 8" :y="y(v) + 3.5" text-anchor="end" class="tick">${{ v }}</text>
      <g v-for="(b, i) in days" :key="b.date">
        <path :d="seg(i, 0, b.port_usd, b.deck_usd <= 0)" fill="var(--s2)">
          <title>{{ label(b.date) }}: порт ${{ b.port_usd }} по ценам API · ×{{ b.x_subscription }} к дню подписки · активных часов: {{ b.active_hours }}</title>
        </path>
        <path v-if="b.deck_usd > 0" :d="seg(i, b.port_usd, b.port_usd + b.deck_usd, true)" fill="rgba(217, 89, 38, 0.42)">
          <title>{{ label(b.date) }}: эта презентация ${{ b.deck_usd }}</title>
        </path>
        <text :x="x(i) + bw / 2" :y="y(b.port_usd + b.deck_usd) - 18" text-anchor="middle" class="val">${{ Math.round(b.port_usd) }}</text>
        <text :x="x(i) + bw / 2" :y="y(b.port_usd + b.deck_usd) - 6" text-anchor="middle" class="mult">×{{ String(b.x_subscription).replace('.', ',') }}</text>
        <text v-if="b.deck_usd > 0" :x="x(i) - 10" :y="y(b.port_usd + b.deck_usd / 2) + 3" text-anchor="end" class="note">эта презентация: +${{ Math.round(b.deck_usd) }} →</text>
        <text :x="x(i) + bw / 2" :y="H - m.b + 16" text-anchor="middle" class="tick">{{ label(b.date) }}</text>
      </g>
      <line :x1="m.l" :x2="W - m.r" :y1="y(DAY)" :y2="y(DAY)" stroke="var(--ink-2)" stroke-width="1.2" stroke-dasharray="4 3" />
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
  font-size: 11px;
  font-weight: 650;
  fill: var(--ink);
  font-variant-numeric: tabular-nums;
}
.mult {
  font-size: 9.5px;
  fill: var(--ink-2);
  font-variant-numeric: tabular-nums;
}
.note {
  font-size: 10px;
  fill: var(--ink-2);
}
</style>
