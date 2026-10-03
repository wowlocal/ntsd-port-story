<script setup lang="ts">
import { computed } from 'vue'
import storage from '../data/storage.json'

// Free space recorded by the agents, one line per volume. Readings are joined in time order;
// a "before/after" pair at the same moment draws a vertical step.
interface Pt { t: string, free: number }
interface Note { t: string, v: number, text: string, dx?: number, dy?: number, anchor?: 'start' | 'end' | 'middle', sub?: string }
const props = withDefaults(defineProps<{
  from: string
  to: string
  yMax: number
  volumes?: ('internal' | 'x5')[]
  notes?: Note[]
  guards?: { v: number, label: string }[]
  markers?: { t: string, label: string }[]
  ticks?: string[]
  hourTicks?: boolean
  height?: number
}>(), { volumes: () => ['internal', 'x5'], notes: () => [], guards: () => [], markers: () => [], ticks: () => [], hourTicks: false, height: 240 })

const W = 900
const H = computed(() => props.height)
const m = { l: 50, r: 14, t: 14, b: 26 }
const t0 = computed(() => Date.parse(props.from))
const t1 = computed(() => Date.parse(props.to))
const x = (t: string | number) => m.l + (((typeof t === 'number' ? t : Date.parse(t)) - t0.value) / (t1.value - t0.value)) * (W - m.l - m.r)
const y = (gb: number) => m.t + (H.value - m.t - m.b) * (1 - gb / props.yMax)
const color: Record<string, string> = { internal: 'var(--s1)', x5: 'var(--s2)' }
const name: Record<string, string> = { internal: 'внутренний SSD Mac mini', x5: 'внешний X5 (APFS, 2 ТБ)' }
const lines = computed(() => props.volumes.map((k) => {
  const pts = ((storage as any)[k] as Pt[]).filter(p => Date.parse(p.t) >= t0.value - 1 && Date.parse(p.t) <= t1.value + 1)
  const d = pts.map((p, i) => `${i ? 'L' : 'M'}${x(p.t).toFixed(1)},${y(p.free / 1e9).toFixed(1)}`).join('')
  return { k, d, pts }
}))
const yTicks = computed(() => {
  const step = props.yMax > 150 ? 50 : props.yMax > 60 ? 20 : 10
  const out: number[] = []
  for (let v = 0; v <= props.yMax; v += step) out.push(v)
  return out
})
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
const tickLabel = (t: string) => {
  const d = new Date(Date.parse(t) + 3 * 3600e3)
  return props.hourTicks
    ? `${d.getUTCDate()} ${months[d.getUTCMonth()]}, ${String(d.getUTCHours()).padStart(2, '0')}:00`
    : `${d.getUTCDate()} ${months[d.getUTCMonth()]}`
}
const fmt = (b: number) => (b / 1e9).toFixed(1).replace('.', ',')
</script>

<template>
  <div>
    <div class="legend">
      <span v-for="k in volumes" :key="k"><i class="key" :style="{ background: color[k] }" />{{ name[k] }}</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Свободное место на дисках">
      <line v-for="v in yTicks" :key="v" :x1="m.l" :x2="W - m.r" :y1="y(v)" :y2="y(v)" :stroke="v === 0 ? 'var(--axis)' : 'var(--grid)'" />
      <text v-for="v in yTicks" :key="`y${v}`" :x="m.l - 8" :y="y(v) + 3.5" text-anchor="end" class="tick">{{ v }} ГБ</text>
      <g v-for="g in guards" :key="g.label">
        <line :x1="m.l" :x2="W - m.r" :y1="y(g.v)" :y2="y(g.v)" stroke="var(--critical)" stroke-width="1" style="opacity: 0.7" />
        <text :x="m.l + 6" :y="y(g.v) + 13" class="guard">{{ g.label }}</text>
      </g>
      <g v-for="mk in markers" :key="mk.t">
        <line :x1="x(mk.t)" :x2="x(mk.t)" :y1="m.t" :y2="y(0)" stroke="var(--s3)" stroke-width="1.5" />
        <text :x="x(mk.t) + 5" :y="m.t + 10" class="marker">{{ mk.label }}</text>
      </g>
      <text v-for="t in ticks" :key="t" :x="x(t)" :y="H - 8" text-anchor="middle" class="tick">{{ tickLabel(t) }}</text>
      <g v-for="l in lines" :key="l.k">
        <path :d="l.d" fill="none" :stroke="color[l.k]" stroke-width="2" stroke-linejoin="round" />
        <circle v-for="(p, i) in l.pts" :key="i" :cx="x(p.t)" :cy="y(p.free / 1e9)" r="3.6" :fill="color[l.k]" stroke="var(--bg)" stroke-width="1.5">
          <title>{{ name[l.k] }}: {{ fmt(p.free) }} ГБ свободно · {{ p.t }}</title>
        </circle>
      </g>
      <g v-for="(n, i) in notes" :key="`n${i}`">
        <text :x="x(n.t) + (n.dx ?? 8)" :y="y(n.v) + (n.dy ?? 4)" :text-anchor="n.anchor ?? 'start'" class="note">{{ n.text }}</text>
        <text v-if="n.sub" :x="x(n.t) + (n.dx ?? 8)" :y="y(n.v) + (n.dy ?? 4) + 13" :text-anchor="n.anchor ?? 'start'" class="note2">{{ n.sub }}</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.legend {
  display: flex;
  gap: 1.1rem;
  font-size: 0.66rem;
  color: var(--ink-2);
  margin-bottom: 0.15rem;
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
  font-variant-numeric: tabular-nums;
}
.guard {
  font-size: 10px;
  fill: #f19393;
}
.marker {
  font-size: 10.5px;
  font-weight: 600;
  fill: var(--ink);
}
.note {
  font-size: 11px;
  font-weight: 600;
  fill: var(--ink);
}
.note2 {
  font-size: 10px;
  fill: var(--ink-2);
}
</style>
