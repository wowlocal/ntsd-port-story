<script setup lang="ts">
// One gameplay tick at phase 4f on two clocks, in milliseconds. The original paces itself with a 33 ms timer and
// sleeps at most 5 ms at a time while ahead; the harness's virtual clock (8 ms per message-loop iteration) makes
// every tick sleep about three such steps whatever the compute. Wall time = 1000 / ticks per second; compute =
// the thread's on-CPU share x wall time (schedstat). The render thread runs in parallel with the main thread.
// Data: data/perf_budget.json (scripts/collect_perf.py, from rt-measurement-20261006.json).
import { useNav, useSlideContext } from '@slidev/client'
import data from '../data/perf_budget.json'

const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const shown = (k: number) => !props.stepwise || nav.isPrintMode.value || ($clicks?.value ?? 0) >= k

const d = data as any
const W = 884
const H = 196
const L = 168
const R = 774
const MAX = 50
const x = (ms: number) => L + (ms / MAX) * (R - L)
const f = (v: number) => v.toFixed(1).replace('.', ',')
const f2 = (v: number) => String(v).replace('.', ',')
const h = 20
const rows = [
  { key: 'virtual', y: 30, title: 'часы харнесса', sub: `8 мс на итерацию · ${f(d.virtual.ticksPerSecond)} тика/с`, k: 0, sleeps: 3 },
  { key: 'real', y: 112, title: 'настоящие часы', sub: `${f2(d.real.ticksPerSecond)} тика/с — темп оригинала`, k: 1, sleeps: 0 },
].map((r) => {
  const v = d[r.key]
  return { ...r, wall: v.wallMs, main: v.mainMs, render: v.renderMs, wait: v.wallMs - v.mainMs }
})
const tiers = [{ ms: 8, label: '8 мс' }, { ms: 16, label: '16 мс' }, { ms: 33, label: '33 мс — таймер оригинала, ярус 1' }]
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Один тик на фазе 4f: на часах харнесса и на настоящих часах">
    <defs>
      <pattern id="tc-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
        <rect width="6" height="6" fill="#262d3c" />
        <line x1="0" y1="0" x2="0" y2="6" stroke="#4a5366" stroke-width="2.2" />
      </pattern>
    </defs>
    <!-- tiers -->
    <g v-for="t in tiers" :key="t.ms">
      <line :x1="x(t.ms)" :x2="x(t.ms)" y1="14" :y2="H - 20" :stroke="t.ms === 33 ? 'var(--ink-2)' : 'var(--axis)'" :stroke-width="t.ms === 33 ? 1.5 : 1" />
      <text :x="x(t.ms) + 5" y="10" class="tier" :class="{ main33: t.ms === 33 }">{{ t.label }}</text>
    </g>
    <!-- axis -->
    <line :x1="L" :x2="R" :y1="H - 20" :y2="H - 20" stroke="var(--axis)" />
    <text v-for="t in [0, 10, 20, 30, 40, 50]" :key="t" :x="x(t)" :y="H - 6" text-anchor="middle" class="tick">{{ t }}{{ t === 50 ? ' мс' : '' }}</text>

    <g v-for="r in rows" :key="r.key" :class="{ off: !shown(r.k) }" class="row">
      <text x="0" :y="r.y + 14" class="rt">{{ r.title }}</text>
      <text x="0" :y="r.y + 30" class="rs">{{ r.sub }}</text>
      <!-- main thread -->
      <rect :x="x(0)" :y="r.y" :width="x(r.main) - x(0) - 2" :height="h" rx="3" fill="var(--s2)" />
      <text :x="x(0) + 8" :y="r.y + 14" class="in">главный поток: {{ f(r.main) }} мс работы</text>
      <template v-if="r.sleeps">
        <rect v-for="i in r.sleeps" :key="i" :x="x(r.main + (i - 1) * 5)" :y="r.y" :width="x(5) - x(0) - 2" :height="h" rx="3" fill="url(#tc-hatch)" />
        <rect :x="x(r.main + r.sleeps * 5)" :y="r.y" :width="x(r.wall) - x(r.main + r.sleeps * 5)" :height="h" rx="3" fill="#262d3c" />
        <text :x="x(r.main + r.sleeps * 2.5)" :y="r.y - 5" text-anchor="middle" class="sl">сон 3 × 5 мс</text>
      </template>
      <rect v-else :x="x(r.main)" :y="r.y" :width="x(r.wall) - x(r.main)" :height="h" rx="3" fill="url(#tc-hatch)" />
      <text :x="x(r.wall) + 6" :y="r.y + 14" class="wall">{{ f(r.wall) }} мс на тик</text>
      <!-- render thread, in parallel -->
      <rect :x="x(0)" :y="r.y + h + 5" :width="x(r.render) - x(0)" height="17" rx="3" fill="var(--s1)" />
      <text :x="x(0) + 8" :y="r.y + h + 17.5" class="in">рендер, параллельно: {{ f(r.render) }} мс</text>
    </g>
  </svg>
</template>

<style scoped>
.tier {
  font-size: 10.5px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.tier.main33 {
  fill: var(--ink-2);
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
}
.rt {
  font-size: 12.5px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.rs {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.in {
  font-size: 11px;
  font-weight: 600;
  fill: #fff;
  font-family: var(--font-sans);
}
.sl {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.wall {
  font-size: 12px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.row {
  transition: opacity 0.4s ease;
}
.off {
  opacity: 0;
}
</style>
