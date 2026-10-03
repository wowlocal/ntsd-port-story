<script setup lang="ts">
import { computed } from 'vue'
import rulebook from '../data/rulebook.json'

const series = [
  { key: 'AGENTS.md', short: 'AGENTS', label: 'AGENTS.md — свод правил', color: 'var(--s1)' },
  { key: 'CURRENT_WORK.md', short: 'CURRENT', label: 'CURRENT_WORK.md — «короткая передача»', color: 'var(--s2)' },
  { key: 'RESEARCH_MAP.md', short: 'MAP', label: 'RESEARCH_MAP.md — карта исследований', color: 'var(--s3)' },
]
const W = 900
const H = 300
const m = { l: 50, r: 120, t: 18, b: 28 }
const plotW = W - m.l - m.r
const plotH = H - m.t - m.b
const t0 = new Date('2026-09-07T12:00:00+0300').getTime()
const t1 = new Date('2026-10-03T23:00:00+0200').getTime()
const parse = (d: string) => new Date(d.replace(/([+-]\d\d)(\d\d)$/, '$1:$2')).getTime()
const x = (t: number) => m.l + ((t - t0) / (t1 - t0)) * plotW
const maxV = 5000
const y = (v: number) => m.t + plotH - (v / maxV) * plotH
const ticks = [0, 1000, 2000, 3000, 4000, 5000]
const fmt = new Intl.NumberFormat('ru-RU')

const paths = computed(() => series.map((s) => {
  const pts = (rulebook as any)[s.key] as { date: string, lines: number }[]
  let d = ''
  pts.forEach((p, i) => {
    const px = x(parse(p.date))
    const py = y(p.lines)
    if (i === 0) {
      d += `M${px.toFixed(1)},${py.toFixed(1)}`
    }
    else {
      const prev = pts[i - 1]
      d += ` L${px.toFixed(1)},${y(prev.lines).toFixed(1)} L${px.toFixed(1)},${py.toFixed(1)}`
    }
  })
  const last = pts[pts.length - 1]
  d += ` L${x(t1).toFixed(1)},${y(last.lines).toFixed(1)}`
  return { ...s, d, endY: y(last.lines), endV: last.lines }
}))

const agents = (rulebook as any)['AGENTS.md'] as { date: string, lines: number, hash: string }[]
const peak = agents.reduce((a, b) => (b.lines > a.lines ? b : a))
const peakIdx = agents.indexOf(peak)
const after = agents[peakIdx + 1]
const days = ['2026-09-07', '2026-09-14', '2026-09-21', '2026-09-28', '2026-10-03']
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
const dl = (d: string) => {
  const dt = new Date(`${d}T12:00:00`)
  return `${dt.getDate()} ${months[dt.getMonth()]}`
}
</script>

<template>
  <div>
    <div class="legend">
      <span v-for="s in series" :key="s.key"><i class="key" :style="{ background: s.color }" />{{ s.label }}</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Длина файлов с правилами по коммитам">
      <line v-for="t in ticks" :key="t" :x1="m.l" :x2="x(t1)" :y1="y(t)" :y2="y(t)" :stroke="t === 0 ? 'var(--axis)' : 'var(--grid)'" />
      <text v-for="t in ticks" :key="`y${t}`" :x="m.l - 8" :y="y(t) + 3.5" text-anchor="end" class="tick">{{ fmt.format(t) }}</text>
      <text v-for="d in days" :key="d" :x="x(new Date(`${d}T12:00:00+0300`).getTime())" :y="H - 8" text-anchor="middle" class="tick">{{ dl(d) }}</text>
      <path v-for="p in paths" :key="p.key" :d="p.d" fill="none" :stroke="p.color" stroke-width="2" stroke-linejoin="round" />
      <g v-for="p in paths" :key="`e${p.key}`">
        <circle :cx="x(t1)" :cy="p.endY" r="4.5" :fill="p.color" stroke="var(--bg)" stroke-width="2" />
        <text :x="x(t1) + 9" :y="p.endY + 4" class="end">{{ fmt.format(p.endV) }} <tspan class="endname">{{ p.short }}</tspan></text>
      </g>
      <!-- peak and compaction -->
      <g>
        <circle :cx="x(parse(peak.date))" :cy="y(peak.lines)" r="4.5" fill="var(--s1)" stroke="var(--bg)" stroke-width="2" />
        <text :x="x(parse(peak.date)) - 8" :y="y(peak.lines) + 4" text-anchor="end" class="ann">4 954 строки · 364 КБ</text>
        <text :x="x(parse(after.date)) + 8" :y="y(after.lines) - 30" class="ann">12 сен · сжатие до {{ after.lines }} строк,</text>
        <text :x="x(parse(after.date)) + 8" :y="y(after.lines) - 16" class="ann2">старый файл → неизменяемый архив</text>
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
.end {
  font-size: 11.5px;
  font-weight: 600;
  fill: var(--ink);
}
.endname {
  font-weight: 400;
  fill: var(--ink-2);
}
.ann {
  font-size: 11px;
  font-weight: 600;
  fill: var(--ink);
}
.ann2 {
  font-size: 10.5px;
  fill: var(--ink-2);
}
</style>
