<script setup lang="ts">
import { computed } from 'vue'
import daily from '../data/daily.json'

interface Mark { date: string, label: string, row?: number }

const props = withDefaults(defineProps<{
  marks?: Mark[]
  height?: number
  labels?: { pre: string, claude: string, parallel: string }
  pauses?: boolean
}>(), {
  marks: () => [],
  height: 270,
  labels: () => ({ pre: 'до 28.09 — без ИИ-трейлера', claude: 'Co-Authored-By: Claude', parallel: 'параллельный агент' }),
  pauses: true,
})

const W = 900
const H = computed(() => props.height)
const m = { l: 34, r: 8, t: 54, b: 40 }
const plotW = W - m.l - m.r
const plotH = computed(() => H.value - m.t - m.b)
const n = daily.length
const band = plotW / n
const bw = Math.min(22, band * 0.7)
const maxV = 60
const y = (v: number) => m.t + plotH.value - (v / maxV) * plotH.value
const x = (i: number) => m.l + i * band + (band - bw) / 2
const ticks = [0, 20, 40, 60]
const eras = ['pre', 'claude', 'parallel'] as const
const colors: Record<string, string> = { pre: 'var(--s1)', claude: 'var(--s2)', parallel: 'var(--s3)' }
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']

function roundedTop(x0: number, y0: number, w: number, h: number, r: number) {
  const rr = Math.min(r, h, w / 2)
  return `M${x0},${y0 + h} L${x0},${y0 + rr} Q${x0},${y0} ${x0 + rr},${y0} L${x0 + w - rr},${y0} Q${x0 + w},${y0} ${x0 + w},${y0 + rr} L${x0 + w},${y0 + h} Z`
}

const bars = computed(() => daily.map((d: any, i: number) => {
  const segs: { era: string, path: string, v: number }[] = []
  let acc = 0
  const present = eras.filter(e => d[e] > 0)
  present.forEach((e, k) => {
    const v = d[e]
    const yTop = y(acc + v)
    const yBot = y(acc)
    const gap = k > 0 ? 2 : 0
    const h = Math.max(0, yBot - yTop - gap)
    const isTop = k === present.length - 1
    const path = isTop
      ? roundedTop(x(i), yTop, bw, h, 4)
      : `M${x(i)},${yTop} h${bw} v${h} h${-bw} Z`
    segs.push({ era: e, path, v })
    acc += v
  })
  const dt = new Date(`${d.date}T12:00:00`)
  return { i, d, segs, day: dt.getDate(), month: dt.getMonth(), total: d.commits }
}))

const pauseRuns = computed(() => {
  const runs: { from: number, to: number }[] = []
  let s = -1
  daily.forEach((d: any, i: number) => {
    if (d.commits === 0 && s < 0)
      s = i
    if ((d.commits > 0 || i === n - 1) && s >= 0) {
      runs.push({ from: s, to: d.commits > 0 ? i - 1 : i })
      s = -1
    }
  })
  return runs
})

const markItems = computed(() => props.marks.map((mk) => {
  const i = daily.findIndex((d: any) => d.date === mk.date)
  const d: any = daily[i]
  const cx = x(i) + bw / 2
  return { ...mk, cx, top: y(d ? d.commits : 0) - 6, ly: 12 + (mk.row ?? 0) * 15 }
}))

const fmtDay = (d: any) => {
  const dt = new Date(`${d.date}T12:00:00`)
  return `${dt.getDate()} ${months[dt.getMonth()]}`
}
</script>

<template>
  <div class="chart">
    <div class="legend">
      <span v-for="e in eras" :key="e"><i class="swatch" :style="{ background: colors[e] }" />{{ labels[e] }}</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Коммиты по дням">
      <g>
        <line
          v-for="t in ticks" :key="t" :x1="m.l" :x2="W - m.r" :y1="y(t)" :y2="y(t)"
          :stroke="t === 0 ? 'var(--axis)' : 'var(--grid)'" stroke-width="1"
        />
        <text v-for="t in ticks" :key="`t${t}`" :x="m.l - 8" :y="y(t) + 3.5" text-anchor="end" class="tick">{{ t }}</text>
      </g>
      <g v-if="pauses">
        <g v-for="(p, k) in pauseRuns" :key="k">
          <rect
            :x="m.l + p.from * band + 2" :y="m.t" :width="(p.to - p.from + 1) * band - 4" :height="plotH"
            fill="rgba(255,255,255,0.025)" rx="6"
          />
          <text
            :x="m.l + (p.from + (p.to - p.from + 1) / 2) * band" :y="y(0) - 10" text-anchor="middle"
            class="pause"
          >
            {{ p.to - p.from + 1 >= 3 ? `пауза · ${p.to - p.from + 1} дн.` : '' }}
          </text>
        </g>
      </g>
      <g v-for="b in bars" :key="b.i">
        <path v-for="s in b.segs" :key="s.era" :d="s.path" :fill="colors[s.era]">
          <title>{{ fmtDay(b.d) }}: {{ b.total }} коммит(ов) · {{ labels[s.era] }}: {{ s.v }}</title>
        </path>
        <text :x="x(b.i) + bw / 2" :y="H - m.b + 15" text-anchor="middle" class="tick" :class="{ strong: b.total > 0 }">{{ b.day }}</text>
        <text v-if="b.i === 0 || b.day === 1" :x="x(b.i) + bw / 2" :y="H - m.b + 30" text-anchor="middle" class="month">{{ months[b.month] }}</text>
      </g>
      <g v-for="mk in markItems" :key="mk.date + mk.label">
        <line :x1="mk.cx" :x2="mk.cx" :y1="mk.ly + 6" :y2="mk.top" stroke="var(--ink-2)" stroke-width="1" style="opacity: 0.55" />
        <circle :cx="mk.cx" :cy="mk.top" r="2.5" fill="var(--ink)" />
        <text :x="mk.cx" :y="mk.ly" text-anchor="middle" class="mark">{{ mk.label }}</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.chart {
  width: 100%;
}
.legend {
  display: flex;
  gap: 1.1rem;
  font-size: 0.7rem;
  color: var(--ink-2);
  margin-bottom: 0.15rem;
}
.tick {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.tick.strong {
  fill: var(--ink-2);
}
.month {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-pixel);
}
.pause {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.mark {
  font-size: 11px;
  fill: var(--ink);
  font-family: var(--font-sans);
  font-weight: 600;
}
path {
  transition: opacity 0.2s;
}
path:hover {
  opacity: 0.8;
}
</style>
