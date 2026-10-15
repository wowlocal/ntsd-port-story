<script setup lang="ts">
import { ref } from 'vue'
import data from '../data/web_delivery.json'

// What a first visit downloads (W2b-4c's measure of one session: every app file at startup, the menu's music
// track when it plays) by kind, and what each kind weighs as brotli -11 (W3b's pre-compressed forms).
// Grey: bytes as stored; blue: bytes on the wire with brotli. Hover a row for gzip and the file count.
// Data: data/web_delivery.json (tw-w2b4c-browser-static-20261012.json firstLoad.measure).
const d = data as any
const parts = d.parts as any[]
const W = 500
const xl = 150
const xr = W - 96
const MAX = 700
const X = (v: number) => xl + (v / MAX) * (xr - xl)
const RH = 27
const y0 = 8
const H = y0 + parts.length * RH + 46
const f1 = (v: number) => v.toLocaleString('ru-RU', { minimumFractionDigits: 1, maximumFractionDigits: 1 })
const files = (n: number) => `${n.toLocaleString('ru-RU')} ${n % 10 === 1 && n % 100 !== 11 ? 'файл' : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14)) ? 'файла' : 'файлов'}`
const tip = ref<{ y: number, p: any } | null>(null)
function ratio(p: any) {
  const r = p.MB / p.brotliMB
  if (r < 1.15)
    return 'почти не сжимается: уже сжато'
  if (r < 2)
    return `на ${Math.round((1 - 1 / r) * 100)} % меньше`
  const n = Math.round(r)
  const w = n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14) ? 'раза' : 'раз'
  return `в ${n} ${w} меньше`
}
</script>

<template>
  <div class="bytes" @pointerleave="tip = null">
    <div class="legend">
      <span><i class="sw" style="background: #4a5366" />как лежит на диске</span>
      <span><i class="sw" style="background: var(--s1)" />уходит по сети с brotli</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`Первый визит: ${f1(d.total.MB)} МБ, с brotli ${f1(d.total.brotliMB)} МБ`">
      <g v-for="t in [0, 100, 200, 300, 400, 500, 600, 700]" :key="t">
        <line :x1="X(t)" :x2="X(t)" :y1="y0 - 4" :y2="y0 + parts.length * RH" stroke="var(--grid)" />
        <text class="tick" :x="X(t)" :y="y0 + parts.length * RH + 12" text-anchor="middle">{{ t }}</text>
      </g>
      <text class="tick" :x="xr + 22" :y="y0 + parts.length * RH + 12">МБ</text>
      <g
        v-for="(p, i) in parts" :key="p.key" class="row" tabindex="0"
        @pointerenter="tip = { y: y0 + i * RH, p }" @focus="tip = { y: y0 + i * RH, p }" @blur="tip = null"
      >
        <rect x="0" :y="y0 + i * RH" :width="W" :height="RH" fill="transparent" />
        <text class="nm" x="0" :y="y0 + i * RH + 17.5">{{ p.label }}</text>
        <rect :x="xl" :y="y0 + i * RH + 5" :width="Math.max(1.5, X(p.MB) - xl)" height="16" rx="3" fill="#4a5366" />
        <rect :x="xl" :y="y0 + i * RH + 5" :width="Math.max(1.5, X(p.brotliMB) - xl)" height="16" rx="3" fill="var(--s1)" />
        <text class="val" :x="Math.max(X(p.MB), xl + 4) + 6" :y="y0 + i * RH + 17.5">{{ f1(p.MB) }} → <tspan class="b">{{ f1(p.brotliMB) }}</tspan></text>
      </g>
      <line x1="0" :x2="W" :y1="y0 + parts.length * RH + 20" :y2="y0 + parts.length * RH + 20" stroke="var(--axis)" />
      <text class="tot" x="0" :y="y0 + parts.length * RH + 38">весь первый визит</text>
      <text class="totv" :x="xl" :y="y0 + parts.length * RH + 38">{{ f1(d.total.MB) }} МБ → <tspan class="b">{{ f1(d.total.brotliMB) }} МБ</tspan><tspan class="tf"> · {{ files(d.total.files) }}</tspan></text>
    </svg>
    <div v-if="tip" class="tip" :style="{ top: `${((tip.y) / H) * 100}%` }">
      <b>{{ tip.p.label }}</b> · {{ files(tip.p.files) }} · {{ f1(tip.p.MB) }} МБ → gzip {{ f1(tip.p.gzipMB) }}, brotli {{ f1(tip.p.brotliMB) }} МБ
      · {{ ratio(tip.p) }}
    </div>
  </div>
</template>

<style scoped>
.bytes {
  position: relative;
}
.legend {
  display: flex;
  gap: 1rem;
  font-size: 0.64rem;
  color: var(--ink-2);
  margin-bottom: 0.15rem;
}
.legend span {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.sw {
  display: inline-block;
  width: 11px;
  height: 11px;
  border-radius: 3px;
}
.row {
  outline: none;
  cursor: default;
}
.row:hover .nm,
.row:focus .nm {
  fill: var(--naruto);
}
.nm {
  font-family: var(--font-sans);
  font-size: 12px;
  fill: var(--ink);
}
.val {
  font-family: var(--font-sans);
  font-size: 11.5px;
  fill: var(--ink-2);
  font-variant-numeric: tabular-nums;
}
.val .b,
.totv .b {
  font-weight: 700;
  fill: var(--ink);
}
.tick {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
}
.tot {
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 650;
  fill: var(--ink);
}
.totv {
  font-family: var(--font-sans);
  font-size: 12.5px;
  fill: var(--ink-2);
}
.tf {
  font-size: 10.5px;
  fill: var(--muted);
}
.tip {
  position: absolute;
  left: 30%;
  transform: translateY(-100%);
  pointer-events: none;
  background: #0c1017;
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 8px;
  padding: 0.25rem 0.5rem;
  font-size: 0.64rem;
  color: var(--ink-2);
  max-width: 340px;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.5);
  z-index: 5;
}
.tip b {
  color: var(--ink);
}
</style>
