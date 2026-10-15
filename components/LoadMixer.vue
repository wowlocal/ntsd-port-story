<script setup lang="ts">
// The sound mixer's inner loop on the Galaxy A12, nanoseconds per voice-frame (median, range as a whisker):
// the float loop before M5c, M5c (PCM kept, converted while mixing) and M5d (PCM read through the buffer's address,
// a mono voice read once). Benchmark: 192-frame callback, 8 voices, 48 kHz output, outputs equal bit for bit.
// `stepwise`: M5d appears on the slide's click 1 (export shows it).
// Data: data/loading_method.json (scripts/collect_loading.py, from ml-frame-time-audit-20261011.json).
import { useNav, useSlideContext } from '@slidev/client'
import data from '../data/loading_method.json'

const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const shown = (k: number) => !props.stepwise || nav.isPrintMode.value || ($clicks?.value ?? 0) >= k

const m = (data as any).mixer
const rows = [
  { k: 'до M5c', sub: 'float, перевод при загрузке', v: m.beforeM5c, fill: '#5d6679', step: 0 },
  { k: 'M5c', sub: 'PCM, перевод в микшере', v: m.m5c, fill: 'var(--critical)', step: 0, tag: `+${Math.round((m.m5c[0] / m.beforeM5c[0] - 1) * 100)} %` },
  { k: 'M5d', sub: 'по адресу, моно — один раз', v: m.m5d, fill: 'var(--good)', step: 1, tag: 'быстрее, чем до M5c' },
]
const W = 430
const L = 172
const MAX = 55
const x = (v: number) => L + ((W - L - 96) * v) / MAX
const f1 = (v: number) => v.toFixed(1).replace('.', ',')
</script>

<template>
  <svg :viewBox="`0 0 ${W} 124`" width="100%" role="img" aria-label="Микшер на A12, нс на голос-кадр: до M5c, M5c, M5d">
    <g v-for="t in [0, 10, 20, 30, 40, 50]" :key="t">
      <line :x1="x(t)" :x2="x(t)" y1="0" y2="102" stroke="var(--grid)" />
      <text :x="x(t)" y="116" text-anchor="middle" class="tick">{{ t }}{{ t === 50 ? ' нс' : '' }}</text>
    </g>
    <g v-for="(r, i) in rows" :key="r.k" :transform="`translate(0, ${4 + i * 33})`" :style="{ opacity: shown(r.step) ? 1 : 0, transition: 'opacity .4s' }">
      <text x="0" y="12" class="k">{{ r.k }}</text>
      <text x="0" y="24" class="kn">{{ r.sub }}</text>
      <rect :x="x(0)" y="3" :width="x(r.v[0]) - x(0)" height="18" rx="3" :fill="r.fill" />
      <line :x1="x(r.v[1])" :x2="x(r.v[2])" y1="12" y2="12" stroke="var(--ink)" stroke-width="1.5" />
      <text :x="x(r.v[0]) + 7" y="16.5" class="v">{{ f1(r.v[0]) }}</text>
      <text v-if="r.tag" :x="x(r.v[0]) + 40" y="16.5" class="tg">{{ r.tag }}</text>
    </g>
  </svg>
</template>

<style scoped>
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.k {
  font-size: 11.5px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-mono);
}
.kn {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.v {
  font-size: 12px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.tg {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
</style>
