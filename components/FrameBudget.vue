<script setup lang="ts">
// Where the frame budget stands at the frozen commit: compute per tick on each thread against the three tiers
// the author set (33, 16, 8 ms), with the value at phase 4f (when the metric started) as a faint bar, and the
// main thread's split after B1 3b (orchestration around the gameplay body) on the same millisecond scale.
// Data: data/perf_budget.json, data/perf_ladder.json, data/perf_now.json (scripts/collect_perf.py).
import budget from '../data/perf_budget.json'
import ladder from '../data/perf_ladder.json'
import now from '../data/perf_now.json'

const b = budget as any
const at4f = (ladder as any).steps.find((s: any) => s.id === '4f')
const split = (now as any).afterB1
const W = 480
const H = 240
const L = 82
const R = 470
const MAX = 36
const x = (ms: number) => L + (ms / MAX) * (R - L)
const f = (v: number) => v.toFixed(1).replace('.', ',')
const bars = [
  { key: 'main', label: 'главный', y: 34, now: b.now.mainMs, was: at4f.mainMs, color: 'var(--s2)' },
  { key: 'render', label: 'рендер', y: 92, now: b.now.renderMs, was: at4f.renderMs, color: 'var(--s1)' },
]
const tiers = [{ ms: 8, label: '8 мс · ярус 3' }, { ms: 16, label: '16 мс · ярус 2' }, { ms: 33, label: 'ярус 1 · 33 мс ✓' }]
const sy = 196
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`Главный поток ${f(b.now.mainMs)} мс, рендер ${f(b.now.renderMs)} мс на тик; ярусы 33, 16, 8 мс`">
    <g v-for="t in tiers" :key="t.ms">
      <line :x1="x(t.ms)" :x2="x(t.ms)" y1="16" :y2="sy - 34" :stroke="t.ms === 33 ? 'var(--good)' : t.ms === 16 ? 'var(--ink-2)' : 'var(--axis)'" stroke-width="1.5" />
      <line :x1="x(t.ms)" :x2="x(t.ms)" :y1="sy - 4" :y2="sy + 30" :stroke="t.ms === 33 ? 'var(--good)' : t.ms === 16 ? 'var(--ink-2)' : 'var(--axis)'" stroke-width="1.5" />
      <text :x="x(t.ms) + (t.ms === 33 ? -4 : 4)" y="11" :text-anchor="t.ms === 33 ? 'end' : 'start'" class="tier">{{ t.label }}</text>
    </g>
    <g v-for="r in bars" :key="r.key">
      <text x="0" :y="r.y + 18.5" class="lab">{{ r.label }}</text>
      <rect :x="x(0)" :y="r.y" :width="x(r.was) - x(0)" height="28" rx="3" :fill="r.color" opacity="0.22" />
      <rect :x="x(0)" :y="r.y" :width="x(r.now) - x(0)" height="28" rx="3" :fill="r.color" />
      <text :x="x(0) + 8" :y="r.y + 18.5" class="in">{{ f(r.now) }} мс</text>
      <text v-if="x(r.was) + 62 < x(33)" :x="x(r.was) + 5" :y="r.y + 18.5" class="was">4f: {{ f(r.was) }}</text>
      <text v-else :x="x(r.was) - 5" :y="r.y + 18.5" text-anchor="end" class="was">4f: {{ f(r.was) }}</text>
      <text :x="x(16) - 5" :y="r.y + 44" text-anchor="end" class="gap">до 16 мс: −{{ f(r.now - 16) }}</text>
      <path :d="`M${x(16) + 1},${r.y + 31} V${r.y + 34} H${x(r.now) - 1} V${r.y + 31}`" fill="none" stroke="var(--naruto)" stroke-width="1.2" />
    </g>

    <!-- the main thread after B1 3b, split -->
    <line x1="0" :x2="W" :y1="sy - 30" :y2="sy - 30" stroke="var(--grid)" />
    <text x="0" :y="sy - 12" class="cap">главный поток после B1 3b — {{ f(split.mainMs) }} мс:</text>
    <text x="0" :y="sy + 16" class="lab">из чего</text>
    <rect :x="x(0)" :y="sy" :width="x(split.orchestrationMs) - x(0) - 2" height="24" rx="3" fill="#566074" />
    <text :x="x(0) + 8" :y="sy + 16" class="in">обвязка ≈ {{ split.orchestrationMs }} мс</text>
    <rect :x="x(split.orchestrationMs)" :y="sy" :width="x(split.orchestrationMs + split.gameplayBodyMs) - x(split.orchestrationMs)" height="24" rx="3" fill="var(--s2)" />
    <text :x="x(split.orchestrationMs) + 6" :y="sy + 16" class="in">игра ≈ {{ f(split.gameplayBodyMs) }}</text>
  </svg>
</template>

<style scoped>
.tier {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.lab {
  font-size: 11.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.in {
  font-size: 11.5px;
  font-weight: 650;
  fill: #fff;
  font-family: var(--font-sans);
}
.was {
  font-size: 10.5px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.gap {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.cap {
  font-size: 11px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
</style>
