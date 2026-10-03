<script setup lang="ts">
import { computed } from 'vue'
import data from '../data/codex_limits.json'

// Weekly Codex limit as a gauge: each window climbs from zero and drops back when the next one
// starts. A drop before the window was due is an early reset; its marker shows who caused it.
interface Win { start: string, end: string, max: number, early?: boolean, used_before?: number, origin?: string }
const wins = (data as any).windows as Win[]
const gauge = (data as any).gauge as [string, number, number][]
const hits = (data as any).limit_hits as string[]

const props = withDefaults(defineProps<{ height?: number }>(), { height: 200 })
const W = 900
const H = computed(() => props.height)
const m = { l: 40, r: 10, t: 20, b: 30 }
const T0 = Date.parse('2026-09-06T21:00Z')
const T1 = Date.parse('2026-10-03T22:00Z')
const PAUSE = [Date.parse('2026-09-14T09:05Z'), Date.parse('2026-09-22T13:37Z')]
const x = (t: number) => m.l + ((t - T0) / (T1 - T0)) * (W - m.l - m.r)
const y = (v: number) => m.t + (H.value - m.t - m.b) * (1 - v / 100)

const shapes = computed(() => wins.map((w, i) => {
  const start = Date.parse(w.start)
  const next = wins[i + 1]
  const stop = Math.min(Date.parse(w.end), next ? Date.parse(next.start) : T1, T1)
  const pts = gauge.filter(g => g[2] === i).map(g => [Date.parse(g[0]), g[1]] as [number, number])
  if (stop <= T0 || !pts.length) return null
  const s = Math.max(start, T0)
  let line = ''
  let ramp = ''
  let area = `M${x(s)},${y(0)}`
  let last = start < T0 ? pts[0][1] : 0
  if (start < T0) {
    line = `M${x(s)},${y(last)}`
    area += ` V${y(last)}`
  }
  pts.forEach(([t, u], k) => {
    if (k === 0 && start >= T0) {
      // Usage already present at the first local reading came from clients without logs.
      if (t - start > 3 * 3600e3 && u > 2) {
        ramp = `M${x(start)},${y(0)} L${x(t)},${y(u)}`
        line = `M${x(t)},${y(u)}`
        area += ` L${x(t)},${y(u)}`
      }
      else {
        line = `M${x(s)},${y(0)} H${x(t)} V${y(u)}`
        area += ` H${x(t)} V${y(u)}`
      }
    }
    else {
      line += ` H${x(t)} V${y(u)}`
      area += ` H${x(t)} V${y(u)}`
    }
    last = u
  })
  line += ` H${x(stop)} V${y(0)}`
  area += ` H${x(stop)} V${y(0)} Z`
  return { i, line, ramp, area }
}).filter(Boolean) as { i: number, line: string, ramp: string, area: string }[])

const resets = computed(() => wins
  .filter(w => w.early && Date.parse(w.start) >= T0)
  .map(w => ({ t: Date.parse(w.start), v: w.used_before ?? 0, origin: w.origin ?? 'unknown', start: w.start })))
const hitMarks = computed(() => hits.map(h => Date.parse(h)).filter(t => t >= T0))
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
const ticks = ['2026-09-07', '2026-09-10', '2026-09-13', '2026-09-16', '2026-09-19', '2026-09-22', '2026-09-25', '2026-09-28', '2026-10-01'].map((d) => {
  const t = Date.parse(`${d}T09:00Z`)
  const dt = new Date(t)
  return { t, label: dt.getUTCDate() === 1 || d === '2026-09-07' ? `${dt.getUTCDate()} ${months[dt.getUTCMonth()]}` : `${dt.getUTCDate()}` }
})
const msk = (iso: string) => {
  const d = new Date(Date.parse(iso) + 3 * 3600e3)
  return `${d.getUTCDate()} ${months[d.getUTCMonth()]}, ${String(d.getUTCHours()).padStart(2, '0')}:${String(d.getUTCMinutes()).padStart(2, '0')} МСК`
}
const originName: Record<string, string> = { after_limit: 'ресет после упора в лимит', global: 'общий сброс OpenAI', unknown: 'по журналу не различить' }
</script>

<template>
  <div>
    <div class="legend">
      <span><i class="key" />недельный лимит Codex, весь аккаунт</span>
      <span><svg width="12" height="12"><circle cx="6" cy="6" r="4.5" fill="var(--s2)" stroke="var(--bg)" stroke-width="1.5" /></svg>ваш ресет</span>
      <span><svg width="12" height="12"><circle cx="6" cy="6" r="4" fill="var(--bg)" stroke="var(--ink)" stroke-width="1.6" /></svg>общий сброс OpenAI</span>
      <span><svg width="12" height="12"><circle cx="6" cy="6" r="4" fill="var(--bg)" stroke="var(--ink-2)" stroke-width="1.4" stroke-dasharray="2 1.6" /></svg>не различить</span>
      <span><svg width="12" height="12"><rect x="2.5" y="2.5" width="7" height="7" transform="rotate(45 6 6)" fill="var(--critical)" /></svg>упор в 100 %</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Недельный лимит Codex: подъёмы и сбросы">
      <rect :x="x(PAUSE[0])" :y="m.t - 18" :width="x(PAUSE[1]) - x(PAUSE[0])" :height="y(0) - m.t + 18" fill="rgba(255,255,255,0.035)" rx="5" />
      <text :x="(x(PAUSE[0]) + x(PAUSE[1])) / 2" :y="m.t - 5" text-anchor="middle" class="pause">коммитов нет</text>
      <line v-for="v in [0, 50, 100]" :key="v" :x1="m.l" :x2="W - m.r" :y1="y(v)" :y2="y(v)" :stroke="v === 0 ? 'var(--axis)' : 'var(--grid)'" />
      <text v-for="v in [0, 50, 100]" :key="`y${v}`" :x="m.l - 7" :y="y(v) + 3.5" text-anchor="end" class="tick">{{ v }} %</text>
      <text v-for="tk in ticks" :key="tk.t" :x="x(tk.t)" :y="H - 10" text-anchor="middle" class="tick">{{ tk.label }}</text>
      <g v-for="sh in shapes" :key="sh.i">
        <path :d="sh.area" fill="var(--s1)" style="opacity: 0.16" />
        <path v-if="sh.ramp" :d="sh.ramp" fill="none" stroke="var(--s1)" stroke-width="1.5" stroke-dasharray="3 3" />
        <path :d="sh.line" fill="none" stroke="var(--s1)" stroke-width="2" stroke-linejoin="round" />
      </g>
      <g v-for="h in hitMarks" :key="h">
        <rect :x="x(h) - 3.5" :y="y(100) - 13.5" width="7" height="7" :transform="`rotate(45 ${x(h)} ${y(100) - 10})`" fill="var(--critical)" stroke="var(--bg)" stroke-width="1.2" />
      </g>
      <g v-for="r in resets" :key="r.start">
        <circle
          :cx="x(r.t)" :cy="y(r.v)" :r="r.origin === 'after_limit' ? 5.5 : 5"
          :fill="r.origin === 'after_limit' ? 'var(--s2)' : 'var(--bg)'"
          :stroke="r.origin === 'after_limit' ? 'var(--bg)' : r.origin === 'global' ? 'var(--ink)' : 'var(--ink-2)'"
          :stroke-width="r.origin === 'after_limit' ? 1.5 : 1.8"
          :stroke-dasharray="r.origin === 'unknown' ? '2.4 1.8' : undefined"
        >
          <title>{{ msk(r.start) }} · было {{ r.v }} % · {{ originName[r.origin] }}</title>
        </circle>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem 1rem;
  font-size: 0.62rem;
  color: var(--ink-2);
  margin-bottom: 0.1rem;
}
.legend span {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.key {
  display: inline-block;
  width: 14px;
  height: 3px;
  border-radius: 2px;
  background: var(--s1);
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.pause {
  font-size: 10px;
  fill: var(--muted);
}
</style>
