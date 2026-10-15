<script setup lang="ts">
// Where the Galaxy A12's loading time and peak memory went, one strip each (own scale, own units).
// A segment is a step's saving measured in its own gate (previous build's median minus the new one's), drawn only
// when the new build's range lies wholly below the previous one's. Load: 123.9 s (branch start) to 5.24 s at
// L18+19 (10:05, after which the load stopped falling); the in-gate savings add up to 119.0 s against a drop of
// 118.7 s, so widths are scaled by 0.997 to fit. Memory: 1598 MiB to the RAM audit's 565 MiB (sounds on); what the
// measured steps do not explain is hatched. Hover a segment for its A/B. Colour = mechanism family.
// Data: data/loading_steps.json (scripts/collect_loading.py).
import { computed, ref } from 'vue'
import { useNav } from '@slidev/client'
import data from '../data/loading_steps.json'

const nav = useNav()
const d = data as any
const byId: Record<string, any> = Object.fromEntries(d.steps.map((s: any) => [s.id, s]))
const famColor: Record<string, string> = {
  inplace: 'var(--s2)', parallel: 'var(--s1)', search: 'var(--s4)', convert: 'var(--s5)', memory: 'var(--s3)',
}
const famOrder = ['inplace', 'parallel', 'convert', 'search', 'memory']
const W = 884
const BH = 44
const GAP = 2
const f1 = (v: number) => v.toLocaleString('ru-RU', { minimumFractionDigits: 1, maximumFractionDigits: 1 })
const f0 = (v: number) => Math.round(v).toLocaleString('ru-RU')

// ---- load
const start = d.baseline.a12.load[0] as number
const end = d.waterfall.loadEnd.load[0] as number
const parts = d.waterfall.load as { id: string, family: string, seconds: number }[]
const sum = parts.reduce((a, p) => a + p.seconds, 0)
const kL = W / start
const fit = (start - end) / sum
let xl = 0
const loadSegs = parts.map((p) => {
  const w = p.seconds * fit * kL
  const seg = { ...p, x: xl, w }
  xl += w
  return seg
})
const remL = { x: xl, w: W - xl }
const famTotals = famOrder.map(f => ({
  f, total: parts.filter(p => p.family === f).reduce((a, p) => a + p.seconds, 0), ids: parts.filter(p => p.family === f).map(p => p.id),
}))

// ---- memory
const mStart = d.baseline.a12.peak[0] as number
const mEnd = d.final.a12.peakAudit[0] as number
const mparts = d.waterfall.memory as { id: string, family: string, mib: number }[]
const kM = W / mStart
let xm = 0
const memSegs = mparts.map((p) => {
  const w = p.mib * kM
  const seg = { ...p, x: xm, w }
  xm += w
  return seg
})
const resid = mStart - mparts.reduce((a, p) => a + p.mib, 0) - mEnd
const residSeg = { x: xm, w: resid * kM }
const remM = { x: xm + resid * kM, w: W - xm - resid * kM }

const labelL: Record<string, string> = { L1: 'L1', L2: 'L2', L3: 'L3', L5: 'L5', L6: 'L6', L7: 'L7', L8: 'L8', L13: 'L13' }
const labelM: Record<string, boolean> = { M1: true, M2: true, M3: true, M5a: true, M5b: true }
const famShort: Record<string, string> = d.families

// ---- hover
const box = ref<HTMLElement | null>(null)
const hover = ref<{ x: number, y: number, html: string } | null>(null)
function tip(e: PointerEvent, html: string) {
  const r = box.value?.getBoundingClientRect()
  if (!r)
    return
  const scale = r.width / box.value!.offsetWidth || 1
  hover.value = { x: (e.clientX - r.left) / scale, y: (e.clientY - r.top) / scale, html }
}
const rng = (a: number[], f: (v: number) => string) => `${f(a[1])}–${f(a[2])}`
function loadTip(id: string) {
  const s = byId[id]
  const p = s.phone
  return `<b>${s.id}</b> · ${s.time.slice(11)} · ${s.name}<br><span class="v">${f1(p.prev.load[0])} → ${f1(p.new.load[0])} с</span> (${rng(p.new.load, f1)} против ${rng(p.prev.load, f1)}), −${f1(p.prev.load[0] - p.new.load[0])} с`
}
function memTip(id: string) {
  const s = byId[id]
  const p = s.phone
  return `<b>${s.id}</b> · ${s.time.slice(11)} · ${s.name}<br><span class="v">${f0(p.prev.peak[0])} → ${f0(p.new.peak[0])} МиБ</span> (${rng(p.new.peak, f0)} против ${rng(p.prev.peak, f0)})`
}
const showTip = computed(() => hover.value && !nav.isPrintMode.value)
</script>

<template>
  <div ref="box" class="wf" @pointerleave="hover = null">
    <div class="hd">
      <span class="t">Экран загрузки, Galaxy A12</span>
      <span class="v">{{ f1(start) }} с → <b>{{ f1(end) }} с</b> к {{ d.waterfall.loadEnd.time.slice(11) }}</span>
      <span class="n">ступени, давшие измеримый выигрыш в своём A/B: {{ parts.length }}</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${BH + 20}`" width="100%" role="img" :aria-label="`Загрузка ${f1(start)} → ${f1(end)} с по ступеням`">
      <g v-for="s in loadSegs" :key="s.id" @pointermove="tip($event, loadTip(s.id))">
        <rect :x="s.x" y="16" :width="Math.max(s.w - GAP, 1)" :height="BH" :rx="s.w > 8 ? 3 : 1" :fill="famColor[s.family]" />
        <text v-if="labelL[s.id] && s.w > 24" :x="s.x + (s.w - GAP) / 2" :y="16 + BH / 2 + 4" text-anchor="middle" class="in">{{ s.id }}</text>
        <text v-if="s.w > 70" :x="s.x + 2" y="11" class="ab">−{{ f1(s.seconds) }} с</text>
      </g>
      <rect :x="remL.x" y="16" :width="remL.w" :height="BH" rx="3" fill="none" stroke="var(--ink)" stroke-width="1.5" />
      <text :x="W" y="11" text-anchor="end" class="ab">{{ f1(end) }} с</text>
    </svg>
    <div class="fams">
      <div v-for="f in famTotals" :key="f.f" class="fam">
        <div class="fh">
          <i class="sw" :style="{ background: famColor[f.f] }" /><span class="fn">{{ famShort[f.f] }}</span>
        </div>
        <div class="ft">
          −{{ f1(f.total) }} с
        </div>
        <div class="ids mono">
          {{ f.ids.join(' ') }}
        </div>
      </div>
    </div>

    <div class="hd mt">
      <span class="t">Пик памяти, Galaxy A12</span>
      <span class="v">{{ f0(mStart) }} → <b>{{ f0(mEnd) }} МиБ</b></span>
      <span class="n">RSS + swap; итог — RAM-аудит со звуком эффектов, без музыки</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${BH + 20}`" width="100%" role="img" :aria-label="`Пик памяти ${f0(mStart)} → ${f0(mEnd)} МиБ по ступеням`">
      <g v-for="s in memSegs" :key="s.id" @pointermove="tip($event, memTip(s.id))">
        <rect :x="s.x" y="16" :width="Math.max(s.w - GAP, 1)" :height="BH" :rx="s.w > 8 ? 3 : 1" :fill="famColor[s.family]" />
        <text v-if="labelM[s.id] && s.w > 24" :x="s.x + (s.w - GAP) / 2" :y="16 + BH / 2 + 4" text-anchor="middle" class="in">{{ s.id }}</text>
        <text v-if="labelM[s.id] && s.w > 30" :x="s.x + 2" y="11" class="ab">−{{ f0(s.mib) }}</text>
      </g>
      <g @pointermove="tip($event, `<b>${f0(resid)} МиБ</b> не объяснены ступенями с измеримым выигрышем: M6 и M5c (их диапазоны перекрылись с прошлой сборкой), звук эффектов в итоговом замере, разброс телефона`)">
        <rect :x="residSeg.x" y="16" :width="residSeg.w - GAP" :height="BH" rx="2" fill="url(#wf-hatch)" />
      </g>
      <defs>
        <pattern id="wf-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect width="6" height="6" fill="#262d3c" />
          <line x1="0" y1="0" x2="0" y2="6" stroke="#4a5366" stroke-width="2" />
        </pattern>
      </defs>
      <rect :x="remM.x" y="16" :width="remM.w" :height="BH" rx="3" fill="none" stroke="var(--ink)" stroke-width="1.5" />
      <text :x="residSeg.x + residSeg.w / 2" y="11" text-anchor="middle" class="ab muted">{{ f0(resid) }}</text>
      <text :x="W" y="11" text-anchor="end" class="ab">{{ f0(mEnd) }} МиБ осталось</text>
    </svg>
    <div class="mkey">
      <span><i class="sw" :style="{ background: famColor.memory }" />хранить меньше: <b>M1</b> листы в LZ4, <b>M2</b> слова кадров в слотах, <b>M5b</b> копии звука, <b>M3</b> без резерва буфера, M5a, M7a</span>
      <span><i class="sw" :style="{ background: famColor.convert }" /><i class="sw" :style="{ background: famColor.parallel }" /><i class="sw" :style="{ background: famColor.search }" />попутно: L4, L13, L18+19</span>
      <span><i class="sw hatch" />не измерено по отдельности</span>
    </div>

    <div v-if="showTip" class="tip" :style="{ left: `${Math.min(hover!.x + 12, 640)}px`, top: `${hover!.y + 14}px` }" v-html="hover!.html" />
  </div>
</template>

<style scoped>
.wf {
  position: relative;
}
.hd {
  display: flex;
  align-items: baseline;
  gap: 0.8rem;
  font-size: 0.72rem;
  color: var(--ink-2);
  border-bottom: 1px solid var(--axis);
  padding-bottom: 0.15rem;
  margin-bottom: 0.1rem;
}
.hd.mt {
  margin-top: 1.2rem;
}
.hd .t {
  font-weight: 650;
  color: var(--ink);
}
.hd .v b {
  color: var(--ink);
}
.hd .n {
  margin-left: auto;
  font-size: 0.64rem;
  color: var(--muted);
}
svg {
  display: block;
  overflow: visible;
}
.in {
  font-size: 10.5px;
  font-weight: 650;
  fill: #fff;
  font-family: var(--font-mono);
  pointer-events: none;
}
.ab {
  font-size: 10.5px;
  font-weight: 600;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.ab.muted {
  fill: var(--muted);
  font-weight: 500;
}
.fams {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.8rem;
  margin-top: 0.35rem;
}
.fh {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.66rem;
  color: var(--ink-2);
  white-space: nowrap;
}
.ft {
  font-size: 1.05rem;
  font-weight: 650;
  color: var(--ink);
  line-height: 1.2;
  margin-top: 0.05rem;
}
.ids {
  font-size: 0.6rem;
  color: var(--muted);
}
.mkey {
  display: flex;
  flex-wrap: wrap;
  gap: 0.2rem 1.4rem;
  margin-top: 0.35rem;
  font-size: 0.66rem;
  color: var(--ink-2);
}
.mkey span {
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
}
.mkey b {
  color: var(--ink);
  font-family: var(--font-mono);
  font-size: 0.62rem;
}
.sw {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 3px;
  margin-right: 0.15rem;
}
.sw.hatch {
  background: repeating-linear-gradient(45deg, #4a5366 0 2px, #262d3c 2px 5px);
}
.tip {
  position: absolute;
  z-index: 5;
  max-width: 300px;
  font-size: 0.66rem;
  line-height: 1.35;
  color: var(--ink-2);
  background: var(--surface-2);
  border: 1px solid var(--axis);
  border-radius: 8px;
  padding: 0.3rem 0.55rem;
  pointer-events: none;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.45);
}
.tip :deep(b),
.tip :deep(.v) {
  color: var(--ink);
  font-weight: 650;
}
</style>
