<script setup lang="ts">
// What every redesign increment was checked with, read from its own evidence file (fields gates, checks, review,
// phone). Filled — recorded as passed; hollow — recorded as not required or not applicable; dot — not in the
// evidence. Data: data/perf_gates.json (scripts/collect_perf.py).
import data from '../data/perf_gates.json'
import ladder from '../data/perf_ladder.json'

type Cell = 'pass' | 'na' | 'none'
const cols = (data as any).columns as string[]
const rows = (data as any).rows as Record<string, any>[]
const dateOf = Object.fromEntries((ladder as any).steps.map((s: any) => [s.id, s.date]))
const names: Record<string, string> = {
  headless: 'headless vs: 1 832 кадра',
  scenarios: 'все 10 сценариев',
  appkit: 'AppKit: 3 960 кадров',
  emulator: 'эмулятор Android',
  suites: 'наборы тестов',
  tsan: 'ThreadSanitizer',
  phone: 'замер на телефоне',
  review: 'независимое ревью',
}
const W = 884
const L = 196
const cw = (W - L) / rows.length
const top = 40
const rh = 21
const H = top + cols.length * rh + 4
const cx = (i: number) => L + cw * (i + 0.5)
const count = (c: string) => rows.filter(r => r[c] === 'pass').length
const days: { label: string, i0: number, i1: number }[] = []
rows.forEach((r, i) => {
  const d = dateOf[r.id]
  const label = d === '2026-10-06' ? '6 октября' : d === '2026-10-07' ? '7 октября' : d
  if (!days.length || days[days.length - 1].label !== label)
    days.push({ label, i0: i, i1: i })
  else days[days.length - 1].i1 = i
})
const word: Record<Cell, string> = { pass: 'пройдено', na: 'не требовалось', none: 'нет в evidence' }
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Ворота каждой ступени редизайна">
    <g v-for="d in days" :key="d.label">
      <line :x1="L + cw * d.i0 + 3" :x2="L + cw * (d.i1 + 1) - 3" y1="12" y2="12" stroke="var(--axis)" />
      <text :x="L + cw * d.i0 + 3" y="8" class="day">{{ d.label }}</text>
    </g>
    <text v-for="(r, i) in rows" :key="r.id" :x="cx(i)" y="30" text-anchor="middle" class="sid">{{ r.id }}</text>
    <g v-for="(c, j) in cols" :key="c">
      <line :x1="0" :x2="W" :y1="top + j * rh - 2" :y2="top + j * rh - 2" stroke="var(--grid)" />
      <text x="0" :y="top + j * rh + 13" class="rl">{{ names[c] }}</text>
      <text :x="L - 10" :y="top + j * rh + 13" text-anchor="end" class="rc">{{ count(c) }}</text>
      <g v-for="(r, i) in rows" :key="`${c}${r.id}`">
        <title>{{ r.id }} · {{ r.hash }} — {{ names[c] }}: {{ word[r[c] as Cell] }}{{ c === 'review' && r.reviewNote ? ` (${r.reviewNote.slice(0, 120)}…)` : '' }}</title>
        <rect v-if="r[c] === 'pass'" :x="cx(i) - 7" :y="top + j * rh + 2" width="14" height="14" rx="3" fill="var(--good)" />
        <rect v-else-if="r[c] === 'na'" :x="cx(i) - 6.25" :y="top + j * rh + 2.75" width="12.5" height="12.5" rx="3" fill="none" stroke="#535c70" stroke-width="1.5" />
        <circle v-else :cx="cx(i)" :cy="top + j * rh + 9" r="2.2" fill="var(--axis)" />
      </g>
    </g>
  </svg>
</template>

<style scoped>
.day {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.sid {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-mono);
}
.rl {
  font-size: 11px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.rc {
  font-size: 11px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
}
</style>
