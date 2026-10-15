<script setup lang="ts">
// Chapter 15: phase 4aa (shipping builds without Swift's dynamic exclusivity checks) on the A12 — main-thread compute
// per tick before (4z, same session) and after (three runs of one APK), vs and the Demo, against 16.67 ms (60 fps,
// the author's criterion). Dots, not bars: the axis starts at 15.5 ms to show the last half-millisecond.
// Data: data/rt2_steps.json (row 4aa; evidence rt-4aa-unchecked-exclusivity-60fps-20261008.json).
import data from '../data/rt2_steps.json'

const s = (data as any).steps.find((x: any) => x.id === '4aa')
const f2 = (v: number) => v.toFixed(2).replace('.', ',')
const W = 420
const H = 112
const L = 92
const R = 400
const LO = 15.5
const HI = 17
const x = (v: number) => L + ((v - LO) / (HI - LO)) * (R - L)
const rows = [
  { k: 'vs', name: 'vs', b: s.vs.base.main, a: s.vs.after.main, y: 30 },
  { k: 'demo', name: 'Demo', b: s.demo.base.main, a: s.demo.after.main, y: 78 },
]
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`Главный поток: vs ${f2(rows[0].b)} → ${f2(rows[0].a)}, Demo ${f2(rows[1].b)} → ${f2(rows[1].a)} мс при пороге 16,67`">
    <defs>
      <marker id="rt2-six" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M0,0 L8,4 L0,8 z" fill="var(--ink-2)" />
      </marker>
    </defs>
    <line :x1="x(16.67)" :x2="x(16.67)" y1="14" :y2="H - 16" stroke="var(--ink)" stroke-width="1.5" />
    <text :x="x(16.67) - 4" y="10" text-anchor="end" class="thr">60 fps = 16,67 мс</text>
    <g v-for="t in [15.5, 16, 16.5, 17]" :key="t">
      <line :x1="x(t)" :x2="x(t)" y1="18" :y2="H - 16" stroke="var(--grid)" />
      <text :x="x(t)" :y="H - 4" text-anchor="middle" class="tick">{{ String(t).replace('.', ',') }}</text>
    </g>
    <g v-for="r in rows" :key="r.k">
      <text x="0" :y="r.y + 4" class="lab">{{ r.name }}</text>
      <text x="0" :y="r.y + 17" class="sub">главный поток</text>
      <line :x1="x(r.b) - 6" :x2="x(r.a) + 7" :y1="r.y + 4" :y2="r.y + 4" stroke="var(--ink-2)" stroke-width="1.4" marker-end="url(#rt2-six)" />
      <circle :cx="x(r.b)" :cy="r.y + 4" r="5" fill="#566074" stroke="var(--bg)" stroke-width="2" />
      <circle :cx="x(r.a)" :cy="r.y + 4" r="5.5" fill="var(--s2)" stroke="var(--bg)" stroke-width="2" />
      <text :x="x(r.b) + 6" :y="r.y - 7" text-anchor="end" class="v halo">{{ f2(r.b) }} с проверками</text>
      <text :x="x(r.a) + 6" :y="r.y + 21" text-anchor="end" class="va halo">{{ f2(r.a) }} без них</text>
    </g>
  </svg>
</template>

<style scoped>
.thr {
  font-size: 10.5px;
  fill: var(--ink);
  font-family: var(--font-sans);
  font-weight: 600;
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.lab {
  font-size: 12px;
  fill: var(--ink);
  font-family: var(--font-sans);
  font-weight: 650;
}
.sub {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.v {
  font-size: 10px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.halo {
  paint-order: stroke;
  stroke: var(--bg);
  stroke-width: 4px;
  stroke-linejoin: round;
}
.va {
  font-size: 11px;
  fill: var(--ink);
  font-family: var(--font-sans);
  font-weight: 650;
}
</style>
