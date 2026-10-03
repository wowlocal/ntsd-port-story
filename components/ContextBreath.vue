<script setup lang="ts">
import { computed } from 'vue'
import ctx from '../data/context.json'

// Context size of each model request over one session: grows with every tool result,
// collapses at each automatic compaction. One series per chart (title names it).
const props = withDefaults(defineProps<{ agent: 'claude' | 'codex', height?: number }>(), { height: 150 })
const d = computed(() => (ctx as any)[props.agent])
const color = computed(() => (props.agent === 'claude' ? 'var(--s2)' : 'var(--s1)'))
const W = 900
const H = computed(() => props.height)
const m = { l: 56, r: 12, t: 10, b: 22 }
const plotW = W - m.l - m.r
const plotH = computed(() => H.value - m.t - m.b)
const tMax = computed(() => d.value.points[d.value.points.length - 1][0])
const yMax = computed(() => (props.agent === 'claude' ? 1000 : 260))
const x = (t: number) => m.l + (t / tMax.value) * plotW
const y = (v: number) => m.t + plotH.value - (v / yMax.value) * plotH.value
const line = computed(() => d.value.points.map((p: number[], i: number) => `${i ? 'L' : 'M'}${x(p[0]).toFixed(1)},${y(p[1]).toFixed(1)}`).join(''))
const area = computed(() => `${line.value}L${x(tMax.value).toFixed(1)},${y(0)}L${x(0)},${y(0)}Z`)
const ticks = computed(() => (props.agent === 'claude' ? [0, 250, 500, 750, 1000] : [0, 100, 200]))
const tickLabel = (v: number) => (v === 0 ? '0' : v === 1000 ? '1 млн' : `${v} тыс.`)
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
// local midnights inside the session
const days = computed(() => {
  const start = new Date(d.value.start).getTime()
  const off = d.value.utc_offset_hours * 3600e3
  const out: { t: number, label: string }[] = []
  let day = Math.ceil((start + off) / 864e5) * 864e5 - off
  while ((day - start) / 6e4 <= tMax.value) {
    const local = new Date(day + off)
    out.push({ t: (day - start) / 6e4, label: `${local.getUTCDate()} ${months[local.getUTCMonth()]}` })
    day += 864e5
  }
  return out
})
// a compaction shows up as a request whose context is under a third of the previous one
const comp = computed(() => {
  const pts = d.value.points as number[][]
  const out: { t: number, v: number, post: number }[] = []
  for (let i = 0; i + 1 < pts.length; i++) {
    if (pts[i][1] > 0.5 * d.value.window_k && pts[i + 1][1] < 0.35 * pts[i][1])
      out.push({ t: pts[i][0], v: pts[i][1], post: pts[i + 1][1] })
  }
  return out
})
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`Размер контекста по запросам: ${agent}`">
    <line v-for="v in ticks" :key="v" :x1="m.l" :x2="W - m.r" :y1="y(v)" :y2="y(v)" :stroke="v === 0 ? 'var(--axis)' : 'var(--grid)'" />
    <text v-for="v in ticks" :key="`t${v}`" :x="m.l - 8" :y="y(v) + 3.5" text-anchor="end" class="tick">{{ tickLabel(v) }}</text>
    <line v-if="agent === 'codex'" :x1="m.l" :x2="W - m.r" :y1="y(d.window_k)" :y2="y(d.window_k)" stroke="var(--s1)" stroke-width="1" style="opacity: 0.6" />
    <text v-if="agent === 'codex'" :x="W - m.r" :y="y(d.window_k) - 4" text-anchor="end" class="ann2">окно {{ Math.round(d.window_k) }} тыс.</text>
    <line v-for="dd in days" :key="dd.t" :x1="x(dd.t)" :x2="x(dd.t)" :y1="m.t" :y2="y(0) + 4" stroke="var(--grid)" />
    <text v-for="dd in days" :key="`d${dd.t}`" :x="x(dd.t) + 4" :y="H - 6" class="tick">{{ dd.label }}</text>
    <path :d="area" :fill="color" style="opacity: 0.1" />
    <path :d="line" fill="none" :stroke="color" stroke-width="1.4" stroke-linejoin="round" />
    <circle v-for="(c, i) in comp" :key="i" :cx="x(c.t)" :cy="y(c.v)" r="3" fill="var(--ink)" stroke="var(--bg)" stroke-width="1.5">
      <title>сжатие контекста: {{ Math.round(c.v) }} тыс. → {{ Math.round(c.post) }} тыс. токенов</title>
    </circle>
  </svg>
</template>

<style scoped>
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.ann {
  font-size: 10.5px;
  font-weight: 600;
  fill: var(--ink);
}
.ann2 {
  font-size: 10px;
  fill: var(--ink-2);
}
</style>
