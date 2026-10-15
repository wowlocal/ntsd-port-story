<script setup lang="ts">
// Chapter 18: an Activity Monitor-like window over seven hours of idling in the main menu.
// The memory grows at the rate the agent measured on the Apple TV / iPad simulators (footprint every 20 s,
// 165 -> 386 MB over 460 s); everything past 460 s is that rate carried on, drawn dashed. After the fix
// (340b1a64) the tvOS menu stayed at 158 MB for the 4 measured minutes. The user's own reading — 11.22 GB —
// is a reference line. Drag the slider or hover the chart; it plays once when the slide opens.
// Data: data/rel_memory.json (scripts/collect_release.py).
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'
import mem from '../data/rel_memory.json'

const d = mem as any
const nav = useNav()
const active = useIsSlideActive()
const isPrint = computed(() => nav.isPrintMode.value)

const from = d.sims.fromMB as number
const rate = d.sims.mbPerMin as number
const measuredMin = d.sims.seconds / 60
const flat = d.after.tvosFlatMB as number
const flatMin = d.after.tvosMinutes as number
const reportMB = d.report.gb * 1024
const cross = (reportMB - from) / rate // minutes until the measured rate reaches the user's reading
const TMAX = 420

const t = ref(isPrint.value ? cross : 0)
const before = (m: number) => from + rate * m
const nf2 = new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const nf0 = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 0 })
const mb = (v: number) => (v < 1000 ? `${nf0.format(v)} МБ` : `${nf2.format(v / 1024)} ГБ`)
const clock = (m: number) => {
  const h = Math.floor(m / 60)
  const mm = Math.round(m - h * 60)
  return h ? `${h} ч ${String(mm).padStart(2, '0')} мин` : `${mm} мин`
}

// chart geometry (viewBox units = px at the slide's size)
const W = 490
const H = 214
const m = { l: 40, r: 14, t: 12, b: 22 }
const YMAX = 13 * 1024
const x = (min: number) => m.l + (min / TMAX) * (W - m.l - m.r)
const y = (v: number) => H - m.b - (v / YMAX) * (H - m.t - m.b)
const yTicks = [0, 5, 10]
const xTicks = [0, 1, 2, 3, 4, 5, 6, 7]

const playX = computed(() => x(t.value))

// play once when the slide becomes active
let raf = 0
const playing = ref(false)
function play() {
  cancelAnimationFrame(raf)
  if (isPrint.value) {
    t.value = cross
    return
  }
  playing.value = true
  const start = performance.now()
  const t0 = t.value >= cross - 0.5 ? 0 : t.value
  const dur = 6000 * (1 - t0 / cross)
  const step = (now: number) => {
    const k = Math.min(1, (now - start) / dur)
    t.value = t0 + (cross - t0) * k
    if (k < 1 && playing.value)
      raf = requestAnimationFrame(step)
    else playing.value = false
  }
  raf = requestAnimationFrame(step)
}
function stop() {
  playing.value = false
  cancelAnimationFrame(raf)
}
function onSlider(e: Event) {
  stop()
  t.value = Number((e.target as HTMLInputElement).value)
}
function onHover(e: PointerEvent) {
  const svg = (e.currentTarget as SVGRectElement).ownerSVGElement!
  const r = svg.getBoundingClientRect()
  const vx = ((e.clientX - r.left) / r.width) * W
  stop()
  t.value = Math.max(0, Math.min(TMAX, ((vx - m.l) / (W - m.l - m.r)) * TMAX))
}
onMounted(() => {
  if (isPrint.value)
    t.value = cross
  else if (active.value)
    play()
})
watch(active, (v) => {
  if (v) {
    t.value = 0
    play()
  }
  else { stop() }
})
watch(isPrint, (p) => {
  if (p) {
    stop()
    t.value = cross
  }
})
onBeforeUnmount(stop)
</script>

<template>
  <figure class="am">
    <div class="bar">
      <i class="dot r" /><i class="dot y" /><i class="dot g" />
      <span class="ttl">Activity Monitor</span>
      <span class="tabs"><span>ЦП</span><span class="on">Память</span><span>Энергия</span><span>Диск</span><span>Сеть</span></span>
    </div>
    <div class="tbl">
      <div class="th">
        <span>Имя процесса</span><span class="num">Память</span><span class="num">В меню</span>
      </div>
      <div class="tr sel">
        <span><i class="sw" style="background: var(--s2)" />NTSD · симулятор Apple TV / iPad — до правки</span>
        <span class="num v">{{ mb(before(t)) }}</span>
        <span class="num">{{ clock(t) }}</span>
      </div>
      <div class="tr">
        <span><i class="sw" style="background: var(--s1)" />NTSD · симулятор Apple TV — после <code>340b1a64</code></span>
        <span class="num v">{{ mb(flat) }}</span>
        <span class="num">{{ clock(t) }}</span>
      </div>
    </div>
    <div class="plot">
      <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`Память в главном меню: ${from} МБ плюс ${rate} МБ в минуту до правки; ${flat} МБ после`">
        <g class="gl">
          <line v-for="g in yTicks" :key="g" :x1="m.l" :x2="W - m.r" :y1="y(g * 1024)" :y2="y(g * 1024)" />
        </g>
        <text v-for="g in yTicks" :key="`yl${g}`" class="ax" :x="m.l - 6" :y="y(g * 1024) + 3.5" text-anchor="end">{{ g }} ГБ</text>
        <text v-for="h in xTicks" :key="`xl${h}`" class="ax" :x="x(h * 60)" :y="H - 6" text-anchor="middle">{{ h }} ч</text>

        <!-- the user's reading -->
        <line class="ref" :x1="m.l" :x2="W - m.r" :y1="y(reportMB)" :y2="y(reportMB)" />
        <text class="reft" :x="m.l + 6" :y="y(reportMB) - 5">11,22 ГБ — увидел автор («около семи часов»)</text>

        <!-- before: measured nub solid, the rate carried on dashed -->
        <line :x1="x(measuredMin)" :x2="x(TMAX)" :y1="y(before(measuredMin))" :y2="y(before(TMAX))" stroke="var(--s2)" stroke-width="2" stroke-dasharray="5 4" stroke-linecap="round" />
        <line :x1="x(0)" :x2="x(measuredMin)" :y1="y(before(0))" :y2="y(before(measuredMin))" stroke="var(--s2)" stroke-width="3" stroke-linecap="round" />
        <!-- after: 4 measured minutes, then the line carried on -->
        <line :x1="x(flatMin)" :x2="x(TMAX)" :y1="y(flat)" :y2="y(flat)" stroke="var(--s1)" stroke-width="2" stroke-dasharray="5 4" stroke-linecap="round" />
        <line :x1="x(0)" :x2="x(flatMin)" :y1="y(flat)" :y2="y(flat)" stroke="var(--s1)" stroke-width="3" stroke-linecap="round" />

        <!-- where the measured rate meets the reading -->
        <circle :cx="x(cross)" :cy="y(reportMB)" r="4" fill="var(--ink)" stroke="var(--surface)" stroke-width="2" />
        <text class="ann" :x="m.l + 6" :y="y(reportMB) + 14">замеренный темп доходит сюда за {{ clock(cross) }} →</text>

        <!-- playhead -->
        <line :x1="playX" :x2="playX" :y1="m.t" :y2="H - m.b" stroke="var(--ink-2)" stroke-width="1" />
        <circle :cx="playX" :cy="y(before(t))" r="4.5" fill="var(--s2)" stroke="var(--surface)" stroke-width="2" />
        <circle :cx="playX" :cy="y(flat)" r="4.5" fill="var(--s1)" stroke="var(--surface)" stroke-width="2" />

        <rect class="hit" :x="m.l" :y="m.t" :width="W - m.l - m.r" :height="H - m.t - m.b" @pointermove="onHover" @pointerdown="onHover" />
      </svg>
      <div class="ctl">
        <button class="btn" :aria-label="playing ? 'пауза' : 'проиграть'" @click="playing ? stop() : play()">
          <span v-if="playing" class="i-pixelarticons-pause" /><span v-else class="i-pixelarticons-play" />
        </button>
        <input type="range" min="0" :max="TMAX" step="1" :value="Math.round(t)" aria-label="время простоя в меню" @input="onSlider">
        <span class="lg"><i class="ln" style="background: var(--s2)" />до</span>
        <span class="lg"><i class="ln" style="background: var(--s1)" />после</span>
        <span class="lg"><i class="ln dash" />продолжение темпа, не замер</span>
      </div>
    </div>
  </figure>
</template>

<style scoped>
.am {
  margin: 0;
  background: #1d2230;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.45);
}
.bar {
  height: 26px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 10px;
  background: linear-gradient(180deg, #2a3142, #222838);
  border-bottom: 1px solid rgba(0, 0, 0, 0.35);
}
.dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
.r { background: #ff5f57; }
.y { background: #febc2e; }
.g { background: #28c840; }
.ttl { font-size: 0.66rem; color: rgba(255, 255, 255, 0.78); font-weight: 600; margin-left: 6px; }
.tabs { margin-left: auto; display: flex; gap: 2px; background: rgba(0, 0, 0, 0.25); border-radius: 6px; padding: 2px; }
.tabs span { font-size: 0.6rem; color: var(--ink-2); padding: 1px 7px; border-radius: 4px; }
.tabs .on { background: rgba(255, 255, 255, 0.16); color: var(--ink); }
.tbl { background: var(--surface); font-size: 0.66rem; }
.th, .tr { display: grid; grid-template-columns: 1fr 74px 92px; gap: 8px; padding: 3px 10px; align-items: center; }
.th { color: var(--muted); border-bottom: 1px solid var(--axis); font-size: 0.62rem; }
.tr { color: var(--ink-2); border-bottom: 1px solid var(--grid); }
.tr.sel { background: rgba(217, 89, 38, 0.14); }
.tr code { font-size: 0.58rem !important; }
.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.v { color: var(--ink); font-weight: 650; font-size: 0.72rem; }
.sw { display: inline-block; width: 9px; height: 9px; border-radius: 2px; margin-right: 6px; vertical-align: -1px; }
.plot { background: var(--bg-2); padding: 6px 8px 6px; }
.gl line { stroke: var(--grid); stroke-width: 1; }
.ax { font-size: 10px; fill: var(--muted); font-family: var(--font-sans); font-variant-numeric: tabular-nums; }
.ref { stroke: var(--ink-2); stroke-width: 1; }
.reft { font-size: 10.5px; fill: var(--ink-2); font-family: var(--font-sans); }
.ann { font-size: 10.5px; fill: var(--ink); font-family: var(--font-sans); }
.hit { fill: transparent; cursor: ew-resize; }
.ctl { display: flex; align-items: center; gap: 8px; margin-top: 2px; }
.btn { width: 24px; height: 22px; border-radius: 6px; border: 1px solid var(--axis); background: var(--surface-2); color: var(--ink); display: grid; place-items: center; cursor: pointer; flex: none; }
.btn span { width: 14px; height: 14px; }
input[type='range'] { flex: 1; accent-color: var(--naruto); height: 14px; min-width: 60px; }
.lg { display: inline-flex; align-items: center; gap: 4px; font-size: 0.6rem; color: var(--ink-2); white-space: nowrap; }
.ln { display: inline-block; width: 14px; height: 2px; border-radius: 1px; }
.ln.dash { background: repeating-linear-gradient(90deg, var(--ink-2) 0 4px, transparent 4px 7px); }
</style>
