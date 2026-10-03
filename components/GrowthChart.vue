<script setup lang="ts">
import { computed } from 'vue'
import growth from '../data/growth.json'
import daily from '../data/daily.json'

const series = [
  { key: 'swift-src', label: 'Swift — сама игра', short: 'игра', color: 'var(--s1)' },
  { key: 'swift-tests', label: 'Swift — тесты', short: 'тесты', color: 'var(--s2)' },
  { key: 'python', label: 'Python — инструменты и оракулы', short: 'Python', color: 'var(--s3)' },
  { key: 'research-md', label: 'Markdown — карточки исследований', short: 'карточки', color: 'var(--s4)' },
]

const W = 900
const H = 300
const m = { l: 46, r: 150, t: 14, b: 30 }
const plotW = W - m.l - m.r
const plotH = H - m.t - m.b
const start = new Date(`${daily[0].date}T12:00:00`).getTime()
const end = new Date(`${daily[daily.length - 1].date}T12:00:00`).getTime()
const x = (d: string) => m.l + ((new Date(`${d}T12:00:00`).getTime() - start) / (end - start)) * plotW
const maxV = 90000
const y = (v: number) => m.t + plotH - (v / maxV) * plotH
const ticks = [0, 30000, 60000, 90000]
const fmtK = (v: number) => v === 0 ? '0' : `${Math.round(v / 1000)} тыс.`
const fmt = new Intl.NumberFormat('ru-RU')

const paths = computed(() => series.map((s) => {
  // values are end-of-day totals: across a pause hold the last value and rise only on the next active day
  const pts: [number, number][] = []
  growth.forEach((g: any, i: number) => {
    if (i > 0) {
      const prev: any = growth[i - 1]
      const gapDays = (new Date(`${g.date}T12:00:00`).getTime() - new Date(`${prev.date}T12:00:00`).getTime()) / 864e5
      if (gapDays > 1) {
        const hold = new Date(new Date(`${g.date}T12:00:00`).getTime() - 864e5).toISOString().slice(0, 10)
        pts.push([x(hold), y(prev.lines[s.key] ?? 0)])
      }
    }
    pts.push([x(g.date), y(g.lines[s.key] ?? 0)])
  })
  const d = pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ')
  const last = growth[growth.length - 1] as any
  return { ...s, d, end: pts[pts.length - 1], value: last.lines[s.key], ly: pts[pts.length - 1][1] }
}))

// end labels: keep at least 15px apart, connect moved labels with a short leader
const labels = computed(() => {
  const items = paths.value.map(p => ({ key: p.key, y: p.end[1], ly: p.end[1] })).sort((a, b) => a.y - b.y)
  for (let i = 1; i < items.length; i++) {
    if (items[i].ly - items[i - 1].ly < 15)
      items[i].ly = items[i - 1].ly + 15
  }
  return Object.fromEntries(items.map(i => [i.key, i.ly]))
})

const pauses = computed(() => {
  const runs: { a: string, b: string }[] = []
  let s: string | null = null
  daily.forEach((d: any, i: number) => {
    if (d.commits === 0 && !s)
      s = daily[i - 1].date
    if (d.commits > 0 && s) {
      runs.push({ a: s, b: d.date })
      s = null
    }
  })
  return runs
})
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
const xt = ['2026-09-07', '2026-09-14', '2026-09-21', '2026-09-28', '2026-10-03']
const label = (d: string) => {
  const dt = new Date(`${d}T12:00:00`)
  return `${dt.getDate()} ${months[dt.getMonth()]}`
}
</script>

<template>
  <div>
    <div class="legend">
      <span v-for="s in series" :key="s.key"><i class="key" :style="{ background: s.color }" />{{ s.label }}</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Рост кода по дням">
      <rect
        v-for="p in pauses" :key="p.a" :x="x(p.a) + 4" :y="m.t" :width="x(p.b) - x(p.a) - 8" :height="plotH"
        fill="rgba(255,255,255,0.025)" rx="6"
      />
      <text v-for="p in pauses" :key="`t${p.a}`" :x="(x(p.a) + x(p.b)) / 2" :y="m.t + 14" text-anchor="middle" class="pause">пауза</text>
      <line
        v-for="t in ticks" :key="t" :x1="m.l" :x2="W - m.r + 10" :y1="y(t)" :y2="y(t)"
        :stroke="t === 0 ? 'var(--axis)' : 'var(--grid)'"
      />
      <text v-for="t in ticks" :key="`y${t}`" :x="m.l - 8" :y="y(t) + 3.5" text-anchor="end" class="tick">{{ fmtK(t) }}</text>
      <text v-for="d in xt" :key="d" :x="x(d)" :y="H - 10" text-anchor="middle" class="tick">{{ label(d) }}</text>
      <path v-for="p in paths" :key="p.key" :d="p.d" fill="none" :stroke="p.color" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />
      <g v-for="p in paths" :key="`e${p.key}`">
        <circle :cx="p.end[0]" :cy="p.end[1]" r="4.5" :fill="p.color" stroke="var(--bg)" stroke-width="2" />
        <line v-if="Math.abs(labels[p.key] - p.end[1]) > 1" :x1="p.end[0] + 6" :y1="p.end[1]" :x2="p.end[0] + 14" :y2="labels[p.key]" stroke="var(--muted)" stroke-width="1" />
        <text :x="p.end[0] + 17" :y="labels[p.key] + 4" class="end">{{ fmt.format(p.value) }} <tspan class="endname">{{ p.short }}</tspan></text>
        <title>{{ p.label }}: {{ fmt.format(p.value) }} строк на 3 октября</title>
      </g>
      <g v-for="g in growth" :key="g.date">
        <rect :x="x(g.date) - 8" :y="m.t" width="16" :height="plotH" fill="transparent">
          <title>{{ label(g.date) }} · игра {{ fmt.format(g.lines['swift-src'] || 0) }} · тесты {{ fmt.format(g.lines['swift-tests'] || 0) }} · Python {{ fmt.format(g.lines.python || 0) }} · карточки {{ fmt.format(g.lines['research-md'] || 0) }}</title>
        </rect>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem 1.1rem;
  font-size: 0.7rem;
  color: var(--ink-2);
  margin-bottom: 0.2rem;
}
.key {
  display: inline-block;
  width: 14px;
  height: 3px;
  border-radius: 2px;
  margin-right: 0.4rem;
  vertical-align: middle;
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
}
.pause {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.endname {
  font-weight: 400;
  fill: var(--ink-2);
}
.end {
  font-size: 11.5px;
  font-weight: 600;
  fill: var(--ink);
  font-family: var(--font-sans);
}
</style>
