<script setup lang="ts">
import { computed } from 'vue'
import tokens from '../data/tokens.json'

// Processed tokens per local day, stacked by agent (millions).
const days = (tokens as any).daily as { date: string, codex: number, claude: number }[]
const W = 900
const H = 180
const m = { l: 60, r: 8, t: 22, b: 38 }
const plotW = W - m.l - m.r
const plotH = H - m.t - m.b
const n = days.length
const band = plotW / n
const bw = Math.min(22, band * 0.7)
const maxV = 1000
const y = (v: number) => m.t + plotH - (v / maxV) * plotH
const x = (i: number) => m.l + i * band + (band - bw) / 2
const ticks = [0, 250, 500, 750, 1000]
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
const fmt = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 0 })

function top(x0: number, y0: number, w: number, h: number, r: number) {
  const rr = Math.min(r, h, w / 2)
  return `M${x0},${y0 + h} L${x0},${y0 + rr} Q${x0},${y0} ${x0 + rr},${y0} L${x0 + w - rr},${y0} Q${x0 + w},${y0} ${x0 + w},${y0 + rr} L${x0 + w},${y0 + h} Z`
}

const bars = computed(() => days.map((d, i) => {
  const c = d.codex / 1e6
  const a = d.claude / 1e6
  const segs: { path: string, fill: string, title: string }[] = []
  const dt = new Date(`${d.date}T12:00:00`)
  const label = `${dt.getDate()} ${months[dt.getMonth()]}`
  const present = [{ v: c, fill: 'var(--s1)', who: 'Codex' }, { v: a, fill: 'var(--s2)', who: 'Claude' }].filter(s => s.v >= 0.5)
  let acc = 0
  present.forEach((s, k) => {
    const yTop = y(acc + s.v)
    const yBot = y(acc) - (k > 0 ? 2 : 0)
    const h = Math.max(0.5, yBot - yTop)
    segs.push({
      path: k === present.length - 1 ? top(x(i), yTop, bw, h, 4) : `M${x(i)},${yTop} h${bw} v${h} h${-bw} Z`,
      fill: s.fill,
      title: `${label}: ${s.who} — ${fmt.format(s.v)} млн токенов`,
    })
    acc += s.v
  })
  return { i, total: c + a, segs, day: dt.getDate(), month: dt.getMonth() }
}))
const peak = computed(() => bars.value.reduce((p, b) => (b.total > p.total ? b : p)))
</script>

<template>
  <div>
    <div class="legend">
      <span><i class="swatch" style="background: var(--s1)" />Codex · GPT-6 Astra и помощники</span>
      <span><i class="swatch" style="background: var(--s2)" />Claude Opus 5.5 и субагенты</span>
      <span class="muted">обработано токенов за день, млн: весь ввод (включая кэш) + ответ</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Токены по дням">
      <line v-for="t in ticks" :key="t" :x1="m.l" :x2="W - m.r" :y1="y(t)" :y2="y(t)" :stroke="t === 0 ? 'var(--axis)' : 'var(--grid)'" />
      <text v-for="t in ticks" :key="`t${t}`" :x="m.l - 8" :y="y(t) + 3.5" text-anchor="end" class="tick">{{ t === 0 ? '0' : t === 1000 ? '1 млрд' : `${t} млн` }}</text>
      <g v-for="b in bars" :key="b.i">
        <path v-for="(s, k) in b.segs" :key="k" :d="s.path" :fill="s.fill"><title>{{ s.title }}</title></path>
        <text :x="x(b.i) + bw / 2" :y="H - m.b + 15" text-anchor="middle" class="tick" :class="{ strong: b.total > 0 }">{{ b.day }}</text>
        <text v-if="b.i === 0 || b.day === 1" :x="x(b.i) + bw / 2" :y="H - m.b + 30" text-anchor="middle" class="tick">{{ months[b.month] }}</text>
      </g>
      <text :x="x(peak.i) + bw / 2" :y="y(peak.total) - 8" text-anchor="middle" class="peak">{{ fmt.format(peak.total) }} млн</text>
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
  margin-bottom: 0.15rem;
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.tick.strong {
  fill: var(--ink-2);
}
.peak {
  font-size: 11px;
  font-weight: 600;
  fill: var(--ink);
}
</style>
