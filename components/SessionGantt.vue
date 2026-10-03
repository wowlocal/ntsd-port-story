<script setup lang="ts">
import { computed } from 'vue'
import data from '../data/sessions.json'

// Every agent session that touched the port, one lane each, on a calendar axis (UTC+3 → UTC+2 like the commits).
interface Row { agent: string, id: string, start: string, end: string, subagent: boolean, model: string, effort: string, responses: number }
const rows = (data as any).sessions as Row[]
const W = 900
const lane = 8
const m = { l: 8, r: 8, t: 8, b: 26 }
const H = m.t + rows.length * lane + m.b
const t0 = new Date('2026-09-07T00:00:00+03:00').getTime()
const t1 = new Date('2026-10-04T00:00:00+02:00').getTime()
const x = (s: string) => m.l + ((new Date(s).getTime() - t0) / (t1 - t0)) * (W - m.l - m.r)
const color = (r: Row) => (r.agent === 'claude' ? 'var(--s2)' : r.subagent ? 'var(--s3)' : 'var(--s1)')
const items = computed(() => rows.map((r, i) => {
  const x0 = x(r.start)
  const x1 = Math.max(x0 + 3, x(r.end))
  return { ...r, x0, w: x1 - x0, y: m.t + i * lane }
}))
// Label the bigger sessions (model · effort · responses), largest first, never on two neighbouring lanes,
// so that a readable label size fits the 8-unit lanes.
const labeled = computed(() => {
  const order = items.value.map((it, i) => ({ i, n: it.responses })).filter(o => o.n > 400).sort((a, b) => b.n - a.n)
  const taken = new Set<number>()
  for (const o of order) {
    if (!taken.has(o.i - 1) && !taken.has(o.i + 1))
      taken.add(o.i)
  }
  return taken
})
const days = ['2026-09-07', '2026-09-14', '2026-09-21', '2026-09-28', '2026-10-03']
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
const dl = (d: string) => {
  const dt = new Date(`${d}T12:00:00`)
  return `${dt.getDate()} ${months[dt.getMonth()]}`
}
const fmt = new Intl.NumberFormat('ru-RU')
</script>

<template>
  <div>
    <div class="legend">
      <span><i class="swatch" style="background: var(--s1)" />Codex — основная сессия</span>
      <span><i class="swatch" style="background: var(--s3)" />Codex — субагент</span>
      <span><i class="swatch" style="background: var(--s2)" />Claude Code</span>
      <span class="muted">одна строка — одна сессия; у крупных сессий подписаны модель, effort и число ответов</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Сессии агентов во времени">
      <line v-for="d in days" :key="d" :x1="x(`${d}T00:00:00+03:00`)" :x2="x(`${d}T00:00:00+03:00`)" :y1="m.t - 4" :y2="H - m.b + 4" stroke="var(--grid)" />
      <text v-for="d in days" :key="`l${d}`" :x="x(`${d}T00:00:00+03:00`) + 3" :y="H - 10" class="tick">{{ dl(d) }}</text>
      <g v-for="(it, i) in items" :key="it.id">
        <rect :x="it.x0" :y="it.y" :width="it.w" :height="lane - 2.4" rx="2" :fill="color(it)">
          <title>{{ it.agent }} {{ it.id }} · {{ it.model }} · effort {{ it.effort }} · {{ fmt.format(it.responses) }} ответов · {{ it.start.slice(0, 16) }} → {{ it.end.slice(0, 16) }} UTC</title>
        </rect>
        <text v-if="labeled.has(i)" :x="it.x0 + it.w > W - 170 ? it.x0 - 5 : it.x0 + it.w + 5" :text-anchor="it.x0 + it.w > W - 170 ? 'end' : 'start'" :y="it.y + lane - 2" class="lbl">{{ it.model.replace('claude-opus-5-5', 'Opus 5.5').replace('gpt-6-astra', 'GPT-6 Astra') }} · {{ it.effort }} · {{ fmt.format(it.responses) }}</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem 1.1rem;
  font-size: 0.66rem;
  color: var(--ink-2);
  margin-bottom: 0.2rem;
}
.tick {
  font-size: 10px;
  fill: var(--muted);
}
.lbl {
  font-size: 9.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
</style>
