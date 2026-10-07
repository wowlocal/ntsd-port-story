<script setup lang="ts">
// The phone profile at the start of the redesign (simpleperf, 30 s of the scripted match): inclusive shares of
// the per-tick phases (they overlap, so they are bars, not a stack), and the disjoint self-time of copying and
// reference counting. Data: data/perf_profile.json (scripts/collect_perf.py, from rt-baseline-20261006.json).
import data from '../data/perf_profile.json'

const rows = (data as any).inclusive as { key: string, label: string, depth: number, share: number }[]
const self = (data as any).self as { memcpy: number, retain: number, release: number, atomics: number }
const W = 440
const rowH = 18.5
const top = 4
const lw = 196
const bx = lw + 4
const MAX = 20
const bw = (v: number) => (v / MAX) * (W - bx - 40)
const H1 = top + rows.length * rowH + 4
const f = (v: number) => v.toFixed(1).replace('.', ',')

const segs = [
  { label: 'memcpy', v: self.memcpy },
  { label: 'retain / release', v: Math.round((self.retain + self.release) * 10) / 10 },
  { label: 'атомики', v: self.atomics },
]
const selfTotal = segs.reduce((a, s) => a + s.v, 0)
const SW = W
const sx = (v: number) => bw(v) // the same px per percent as the phase bars above
let acc = 0
const placed = segs.map((s) => {
  const o = { ...s, x0: sx(acc), x1: sx(acc + s.v) }
  acc += s.v
  return o
})
</script>

<template>
  <div>
    <svg :viewBox="`0 0 ${W} ${H1}`" width="100%" role="img" aria-label="Доли фаз тика в профиле телефона, включительно">
      <line :x1="bx" :x2="bx" :y1="0" :y2="H1" stroke="var(--axis)" />
      <g v-for="(r, i) in rows" :key="r.key">
        <title>{{ r.label }} ({{ r.key }}): {{ f(r.share) }} % сэмплов, включительно</title>
        <text :x="r.depth ? 14 : 0" :y="top + i * rowH + 12.5" class="lab" :class="{ sub: r.depth, hot: r.key === 'gameplay body' }">{{ r.depth ? '└ из неё — ' : '' }}{{ r.label }}</text>
        <rect :x="bx" :y="top + i * rowH + 3" :width="bw(r.share)" height="11" rx="2.5" :fill="r.key === 'gameplay body' ? 'var(--s2)' : '#566074'" />
        <text :x="bx + bw(r.share) + 5" :y="top + i * rowH + 12.5" class="val" :class="{ hot: r.key === 'gameplay body' }">{{ f(r.share) }} %</text>
      </g>
    </svg>
    <div class="selfh">
      на вершине стека: <b>{{ f(selfTotal) }} % сэмплов</b> — копирование памяти и счётчики ссылок
    </div>
    <svg :viewBox="`0 0 ${SW} 40`" width="100%" role="img" :aria-label="`memcpy ${f(self.memcpy)} %, retain/release, атомики: всего ${f(selfTotal)} %`">
      <g v-for="s in placed" :key="s.label">
        <title>{{ s.label }}: {{ f(s.v) }} % сэмплов</title>
        <rect :x="s.x0" y="2" :width="s.x1 - s.x0 - 2" height="14" rx="3" fill="var(--s1)" />
        <text :x="s.x0" y="31" class="slab"><tspan class="sv">{{ f(s.v) }} %</tspan> {{ s.label }}</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.lab {
  font-size: 11px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.lab.sub {
  fill: var(--muted);
}
.lab.hot {
  fill: var(--ink);
  font-weight: 650;
}
.val {
  font-size: 11px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
}
.val.hot {
  fill: var(--ink);
  font-weight: 650;
}
.selfh {
  font-size: 0.7rem;
  color: var(--ink-2);
  margin: 0.45rem 0 0.2rem;
}
.selfh b {
  color: var(--ink);
}
.slab {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.sv {
  fill: var(--ink);
  font-weight: 650;
}
</style>
