<script setup lang="ts">
import { computed } from 'vue'
import tokens from '../data/tokens.json'

// Cumulative processed tokens, stacked by agent, above a strip of what a player could see in the app.
interface Day { date: string, codex: number, claude: number }
const days = (tokens as any).daily as Day[]
const W = 900
const H = 300
const m = { l: 56, r: 12, t: 16, b: 96 }
const plotW = W - m.l - m.r
const plotH = H - m.t - m.b
const n = days.length
const x = (i: number) => m.l + (i / (n - 1)) * plotW
const yMax = 7
const y = (v: number) => m.t + plotH - (v / yMax) * plotH
const ticks = [0, 2, 4, 6]
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']

const series = computed(() => {
  let c = 0
  let a = 0
  return days.map((d, i) => {
    c += d.codex / 1e9
    a += d.claude / 1e9
    return { i, date: d.date, codex: c, total: c + a }
  })
})
const codexArea = computed(() => {
  const top = series.value.map(p => `${x(p.i).toFixed(1)},${y(p.codex).toFixed(1)}`).join(' L')
  return `M${x(0)},${y(0)} L${top} L${x(n - 1)},${y(0)} Z`
})
const claudeArea = computed(() => {
  const top = series.value.map(p => `${x(p.i).toFixed(1)},${y(p.total).toFixed(1)}`).join(' L')
  const bottom = [...series.value].reverse().map(p => `${x(p.i).toFixed(1)},${y(p.codex).toFixed(1)}`).join(' L')
  return `M${top} L${bottom} Z`
})
const totalLine = computed(() => series.value.map((p, k) => `${k ? 'L' : 'M'}${x(p.i).toFixed(1)},${y(p.total).toFixed(1)}`).join(''))
const idx = (d: string) => days.findIndex(v => v.date === d)
const i27 = idx('2026-09-27')
const i28 = idx('2026-09-28')
const at27 = computed(() => series.value[i27])
const atEnd = computed(() => series.value[n - 1])
const label = (d: string) => {
  const dt = new Date(`${d}T12:00:00`)
  return `${dt.getDate()} ${months[dt.getMonth()]}`
}
const xt = ['2026-09-07', '2026-09-14', '2026-09-21', '2026-09-28', '2026-10-03']
const fmt = (v: number) => v.toFixed(2).replace('.', ',')
const stripY = H - m.b + 30
</script>

<template>
  <div>
    <div class="legend">
      <span><i class="swatch" style="background: var(--s1)" />Codex</span>
      <span><i class="swatch" style="background: var(--s2)" />Claude</span>
      <span class="muted">накоплено обработанных токенов, млрд; ниже — что игрок видел в приложении</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Накопленные токены и видимый результат">
      <line v-for="t in ticks" :key="t" :x1="m.l" :x2="W - m.r" :y1="y(t)" :y2="y(t)" :stroke="t === 0 ? 'var(--axis)' : 'var(--grid)'" />
      <text v-for="t in ticks" :key="`t${t}`" :x="m.l - 8" :y="y(t) + 3.5" text-anchor="end" class="tick">{{ t }} млрд</text>
      <path :d="codexArea" fill="var(--s1)" style="opacity: 0.32" />
      <path :d="claudeArea" fill="var(--s2)" style="opacity: 0.38" />
      <path :d="totalLine" fill="none" stroke="var(--ink)" stroke-width="1.6" stroke-linejoin="round" />
      <!-- the blind stretch -->
      <line :x1="x(i27)" :x2="x(i27)" :y1="y(at27.total)" :y2="stripY - 4" stroke="var(--ink-2)" stroke-width="1" style="opacity: 0.6" />
      <circle :cx="x(i27)" :cy="y(at27.total)" r="4.5" fill="var(--ink)" stroke="var(--bg)" stroke-width="2" />
      <text :x="x(i27) - 14" :y="y(at27.total) - 30" text-anchor="end" class="ann">27 сентября: {{ fmt(at27.total) }} млрд токенов</text>
      <text :x="x(i27) - 14" :y="y(at27.total) - 15" text-anchor="end" class="ann2">а в приложении — та же тренировочная сцена, что и 7 сентября</text>
      <circle :cx="x(n - 1)" :cy="y(atEnd.total)" r="4.5" fill="var(--ink)" stroke="var(--bg)" stroke-width="2" />
      <text :x="x(n - 1) - 8" :y="y(atEnd.total) - 10" text-anchor="end" class="ann">{{ fmt(atEnd.total) }} млрд</text>
      <text v-for="d in xt" :key="d" :x="x(idx(d))" :y="H - m.b + 16" text-anchor="middle" class="tick">{{ label(d) }}</text>
      <!-- what a player could see -->
      <rect :x="x(0)" :y="stripY" :width="x(i27) - x(0) + 8" height="44" rx="8" fill="rgba(255,255,255,0.05)" stroke="var(--axis)" />
      <text :x="x(0) + 12" :y="stripY + 18" class="strip">В приложении: тренировка Наруто против Саске на заглушках</text>
      <text :x="x(0) + 12" :y="stripY + 34" class="strip2">код приложения — ровно 801 строка 21 день подряд; вся работа уходила в ядро, оракулы и проверки</text>
      <rect :x="x(i28) - 4" :y="stripY" :width="x(n - 1) - x(i28) + 4" height="44" rx="8" fill="rgba(217,89,38,0.28)" stroke="var(--s2)" />
      <text :x="x(i28) + 6" :y="stripY + 18" class="strip">меню → матч → режимы</text>
      <text :x="x(i28) + 6" :y="stripY + 34" class="strip2">→ 58 матчей = оригинал</text>
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
.ann {
  font-size: 11.5px;
  font-weight: 700;
  fill: var(--ink);
}
.ann2 {
  font-size: 10.5px;
  fill: var(--ink-2);
}
.strip {
  font-size: 11.5px;
  font-weight: 600;
  fill: var(--ink);
}
.strip2 {
  font-size: 10px;
  fill: var(--ink-2);
}
</style>
