<script setup lang="ts">
import { computed, ref } from 'vue'
import { useNav, useSlideContext } from '@slidev/client'
import data from '../data/web_frametime.json'

// «хромиум wasm быстрее чем нативная mac версия?» (12 Oct 17:36). Panel A is what the first table compared:
// the Mac's game thread alone and its CPU summed over all threads against Chromium's one thread doing tick and
// drawing. Panel B (click 1) is the like-for-like run measured afterwards: every host draws on its game thread.
// Milliseconds per tick, VS over bodies 600–1500, median of 3 runs. Hover a bar for the Demo's value.
// Data: data/web_frametime.json (tw-w3a-browser-frame-time-20261012.json, ef6e880a).
const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const shownB = computed(() => !props.stepwise || nav.isPrintMode.value || ($clicks?.value ?? 0) >= 1)

const rows = (data as any).rows as any[]
const by = (k: string) => rows.find(r => r.key === k)
const color: Record<string, string> = { 'mac': 'var(--s1)', 'mac-cpu': 'var(--s1)', 'macsync': 'var(--s1)', 'chromium': 'var(--s2)', 'webkit': 'var(--s3)', 'wasi': 'var(--s4)' }
const A = [
  { r: by('mac'), name: 'Mac', what: 'только игровой поток', hatch: true },
  { r: by('chromium'), name: 'Chromium', what: 'всё в одном потоке' },
  { r: by('mac-cpu'), name: 'Mac', what: 'CPU, сложенный по потокам', hatch: true },
]
const B = [
  { r: by('macsync'), name: 'Mac', what: '--synchronous-render' },
  { r: by('chromium'), name: 'Chromium', what: 'headless 153' },
  { r: by('webkit'), name: 'WebKit', what: 'движок Safari' },
  { r: by('wasi'), name: 'Node WASI', what: 'без страницы' },
]
const base = by('macsync').vs as number

const W = 520
const xl = 178
const xr = W - 70
const MAX = 4
const X = (v: number) => xl + (v / MAX) * (xr - xl)
const RH = 28
const hA = 20
const yA = hA
const hB = yA + A.length * RH + 34
const yB = hB
const axisY = yB + B.length * RH + 6
const H = axisY + 20
const f2 = (v: number) => v.toFixed(2).replace('.', ',')

const tip = ref<{ x: number, y: number, text: string } | null>(null)
function show(o: any, y: number) {
  tip.value = { x: X(o.r.vs), y, text: `${o.name} · ${o.what}: VS ${f2(o.r.vs)} мс, Demo ${f2(o.r.demo)} мс на тик` }
}
</script>

<template>
  <div class="ft" @pointerleave="tip = null">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`Мс на тик: Mac ${f2(base)}, Chromium ${f2(by('chromium').vs)}, WebKit ${f2(by('webkit').vs)}, Node ${f2(by('wasi').vs)}`">
      <defs>
        <pattern id="wftHatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect width="6" height="6" fill="rgba(57,135,229,0.22)" />
          <line x1="0" y1="0" x2="0" y2="6" stroke="var(--s1)" stroke-width="2" />
        </pattern>
      </defs>
      <!-- grid -->
      <g v-for="t in [0, 1, 2, 3, 4]" :key="t">
        <line :x1="X(t)" :x2="X(t)" :y1="yA - 6" :y2="axisY" stroke="var(--grid)" />
        <text class="tick" :x="X(t)" :y="axisY + 13" text-anchor="middle">{{ t }}</text>
      </g>
      <text class="tick" :x="xr + 6" :y="axisY + 13">мс на тик</text>

      <!-- panel A -->
      <text class="ph" x="0" :y="yA - 6"><tspan class="pa">А</tspan> что сравнивала первая таблица</text>
      <g v-for="(o, i) in A" :key="`a${i}`" class="row" :class="{ dim: shownB && o.hatch }" @pointerenter="show(o, yA + i * RH + 6)">
        <rect x="0" :y="yA + i * RH" :width="W" :height="RH" fill="transparent" />
        <text class="nm" x="0" :y="yA + i * RH + 18">{{ o.name }}<tspan class="wh"> · {{ o.what }}</tspan></text>
        <rect :x="xl" :y="yA + i * RH + 6" :width="X(o.r.vs) - xl" height="16" rx="3" :fill="o.hatch ? 'url(#wftHatch)' : color[o.r.key]" />
        <text class="val" :x="X(o.r.vs) + 5" :y="yA + i * RH + 18.5">{{ f2(o.r.vs) }}</text>
        <text v-if="shownB && o.hatch" class="no" :x="X(o.r.vs) + 40" :y="yA + i * RH + 18.5">не то же самое</text>
      </g>

      <!-- panel B -->
      <g :class="{ off: !shownB }" class="pb">
        <text class="ph" x="0" :y="yB - 6"><tspan class="pa">Б</tspan> честно: отрисовка в том же потоке, что тик</text>
        <g v-for="(o, i) in B" :key="`b${i}`" class="row" @pointerenter="show(o, yB + i * RH + 6)">
          <rect x="0" :y="yB + i * RH" :width="W" :height="RH" fill="transparent" />
          <text class="nm" x="0" :y="yB + i * RH + 18">{{ o.name }}<tspan class="wh"> · {{ o.what }}</tspan></text>
          <rect :x="xl" :y="yB + i * RH + 6" :width="X(o.r.vs) - xl" height="16" rx="3" :fill="color[o.r.key]" />
          <text class="val" :x="X(o.r.vs) + 5" :y="yB + i * RH + 18.5">{{ f2(o.r.vs) }}</text>
          <text v-if="i > 0" class="rt" :x="X(o.r.vs) + 38" :y="yB + i * RH + 18.5">×{{ (o.r.vs / base).toFixed(2).replace('.', ',') }}</text>
        </g>
      </g>
    </svg>
    <div v-if="tip" class="tip" :style="{ left: `${(tip.x / W) * 100}%`, top: `${(tip.y / H) * 100}%` }">
      {{ tip.text }}
    </div>
  </div>
</template>

<style scoped>
.ft {
  position: relative;
}
.ph {
  font-family: var(--font-sans);
  font-size: 11px;
  fill: var(--ink-2);
}
.pa {
  font-family: var(--font-pixel);
  fill: var(--naruto);
}
.row {
  cursor: default;
  transition: opacity 0.4s ease;
}
.row.dim {
  opacity: 0.45;
}
.nm {
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 650;
  fill: var(--ink);
}
.wh {
  font-weight: 400;
  font-size: 10.5px;
  fill: var(--ink-2);
}
.val {
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 700;
  fill: var(--ink);
  font-variant-numeric: tabular-nums;
}
.rt {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--ink-2);
}
.no {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
}
.tick {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.pb {
  transition: opacity 0.4s ease;
}
.off {
  opacity: 0;
}
.tip {
  position: absolute;
  transform: translate(-50%, -110%);
  pointer-events: none;
  background: #0c1017;
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 8px;
  padding: 0.25rem 0.5rem;
  font-size: 0.64rem;
  color: var(--ink);
  white-space: nowrap;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.5);
  z-index: 5;
}
</style>
