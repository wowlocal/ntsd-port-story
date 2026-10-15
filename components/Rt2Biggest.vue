<script setup lang="ts">
// Chapter 15: the twelve biggest single steps of 7–10 Oct on either thread (vs; each step against the previous build's
// runs), with the spread of the step's own runs as a whisker; hatched bars moved work rather than removing it. Below,
// every committed step's main-thread change on one axis, with the phone's resolution (±0.25 ms per run) shaded.
// Hover a bar or a dot: the caption line shows the step. B2 P4b+c..P4f were measured against the same 4w runs, so the
// list shows them as one group and the strip gives each its change from the one before.
// Data: data/rt2_steps.json → biggest (scripts/collect_realtime2.py).
import { computed, ref } from 'vue'
import data from '../data/rt2_steps.json'

const b = (data as any).biggest
const top = b.top as any[]
const strip = b.strip as any[]
const f2 = (v: number) => v.toFixed(2).replace('.', ',')
const sign = (v: number) => (v <= 0 ? `−${f2(Math.abs(v))}` : `+${f2(v)}`)

const W = 884
const RH = 20
const H = top.length * RH + 22
const LX = 330
const BX = 352
const BMAX = 4
const BW = 360
const bx = (ms: number) => BX + (ms / BMAX) * BW
const rows = top.map((e, i) => ({ ...e, y: 18 + i * RH }))

// strip
const SW = 884
const SH = 64
const SL = 40
const SR = SW - 260
const LO = -1.8
const HI = 0.6
const sx = (v: number) => SL + ((v - LO) / (HI - LO)) * (SR - SL)
const sy = 30
// stack dots that would overlap
const dots = (() => {
  const placed: { x: number, lvl: number }[] = []
  return strip.map((e) => {
    const x = sx(e.delta)
    let lvl = 0
    while (placed.some(p => p.lvl === lvl && Math.abs(p.x - x) < 7.5))
      lvl++
    placed.push({ x, lvl })
    return { ...e, x, y: sy - (lvl % 2 ? 1 : -1) * Math.ceil(lvl / 2) * 7.5 }
  })
})()

const hover = ref<any>(null)
const day = (t: string) => `${Number(t.slice(3, 5))} окт, ${t.slice(6)}`
const thread = (k: string) => (k === 'main' ? 'главный поток' : 'поток рендера')
const caption = computed(() => {
  const e = hover.value
  if (!e)
    return null
  return { head: `${e.id} · ${day(e.time)} · ${e.hash}`, body: `${e.label} — ${thread(e.thread)}: ${f2(e.from)} → ${f2(e.to)} мс (${sign(e.delta)})${e.moved ? `; ${e.moved}` : ''}` }
})
</script>

<template>
  <div class="big" @pointerleave="hover = null">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Двенадцать самых больших шагов, мс на тик">
      <defs>
        <pattern id="rt2-hatch-r" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect width="6" height="6" fill="rgba(57,135,229,0.25)" />
          <line x1="0" y1="0" x2="0" y2="6" stroke="var(--s1)" stroke-width="2.4" />
        </pattern>
        <pattern id="rt2-hatch-m" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect width="6" height="6" fill="rgba(217,89,38,0.25)" />
          <line x1="0" y1="0" x2="0" y2="6" stroke="var(--s2)" stroke-width="2.4" />
        </pattern>
      </defs>
      <g v-for="t in [0, 1, 2, 3, 4]" :key="t">
        <line :x1="bx(t)" :x2="bx(t)" y1="10" :y2="H - 6" stroke="var(--grid)" />
        <text :x="bx(t)" y="8" text-anchor="middle" class="tick">{{ t === 0 ? '0' : `−${t}` }}{{ t === 4 ? ' мс' : '' }}</text>
      </g>
      <g v-for="r in rows" :key="r.id + r.thread" class="row" :class="{ on: hover === r }" @pointerenter="hover = r">
        <rect x="0" :y="r.y - 2" :width="W" :height="RH" fill="transparent" />
        <text x="0" :y="r.y + 12" class="rid">{{ r.id }}</text>
        <text x="78" :y="r.y + 12" class="rl">{{ r.label.length > 44 ? `${r.label.slice(0, 43)}…` : r.label }}</text>
        <rect
          :x="bx(0)" :y="r.y + 2" :width="bx(-r.delta) - bx(0)" height="12" rx="2"
          :fill="r.moved ? (r.thread === 'main' ? 'url(#rt2-hatch-m)' : 'url(#rt2-hatch-r)') : (r.thread === 'main' ? 'var(--s2)' : 'var(--s1)')"
        />
        <line :x1="bx(r.from - r.toMax)" :x2="bx(r.from - r.toMin)" :y1="r.y + 8" :y2="r.y + 8" stroke="var(--ink)" stroke-width="1.2" style="opacity: 0.75" />
        <text :x="Math.max(bx(-r.delta), bx(r.from - r.toMin)) + 6" :y="r.y + 12" class="rv">{{ sign(r.delta) }} <tspan class="rf">{{ f2(r.from) }} → {{ f2(r.to) }}</tspan></text>
      </g>
    </svg>

    <div class="cap">
      <template v-if="caption">
        <span class="pixel ch">{{ caption.head }}</span> <span>{{ caption.body }}</span>
      </template>
      <template v-else>
        <span><i class="sw" style="background: var(--s2)" />главный поток</span>
        <span><i class="sw" style="background: var(--s1)" />поток рендера</span>
        <span><i class="sw hatch" />работа переехала, а не исчезла</span>
        <span><i class="wk" />разброс прогонов шага</span>
      </template>
    </div>

    <svg :viewBox="`0 0 ${SW} ${SH}`" width="100%" role="img" :aria-label="`${b.withinNoise} из ${strip.length} шагов внутри ±0,25 мс`" class="strip">
      <rect :x="sx(-b.noiseMs)" y="6" :width="sx(b.noiseMs) - sx(-b.noiseMs)" :height="SH - 22" fill="rgba(255,255,255,0.06)" />
      <line :x1="sx(0)" :x2="sx(0)" y1="6" :y2="SH - 16" stroke="var(--axis)" />
      <g v-for="t in [-1.5, -1, -0.5, 0, 0.5]" :key="t">
        <text :x="sx(t)" :y="SH - 3" text-anchor="middle" class="tick">{{ t === 0 ? '0' : (t < 0 ? '−' : '+') + String(Math.abs(t)).replace('.', ',') }}{{ t === 0.5 ? ' мс' : '' }}</text>
      </g>

      <circle v-for="p in dots" :key="p.id" :cx="p.x" :cy="p.y" r="3.6" fill="var(--s2)" stroke="var(--bg)" stroke-width="1.5" :class="{ on: hover === p }" @pointerenter="hover = p" />
      <text :x="SR + 18" y="22" class="sx"><tspan class="sxv">{{ b.withinNoise }} из {{ strip.length }}</tspan> закоммиченных шагов</text>
      <text :x="SR + 18" y="38" class="sxs">меняют главный поток меньше чем на ±0,25 мс —</text>
      <text :x="SR + 18" y="52" class="sxs">разрешение телефона (серая полоса)</text>
    </svg>
  </div>
</template>

<style scoped>
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.rid {
  font-size: 11px;
  fill: var(--naruto);
  font-family: var(--font-pixel);
}
.rl {
  font-size: 11px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.rv {
  font-size: 11px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.rf {
  font-weight: 400;
  fill: var(--muted);
  font-size: 10px;
}
.row.on .rl {
  fill: var(--ink);
}
.row.on rect:first-child {
  fill: rgba(255, 255, 255, 0.04);
}
.cap {
  display: flex;
  align-items: center;
  gap: 1rem;
  height: 1.1rem;
  font-size: 0.64rem;
  color: var(--ink-2);
  white-space: nowrap;
  overflow: hidden;
  margin: 0.1rem 0 0.2rem;
}
.cap span {
  display: inline-flex;
  align-items: center;
}
.ch {
  color: var(--naruto);
  margin-right: -0.5rem;
}
.sw {
  display: inline-block;
  width: 12px;
  height: 10px;
  border-radius: 2px;
  margin-right: 0.35rem;
}
.sw.hatch {
  background: repeating-linear-gradient(45deg, var(--ink-2) 0 2px, transparent 2px 5px);
  border: 1px solid var(--ink-2);
}
.wk {
  display: inline-block;
  width: 14px;
  height: 1.5px;
  background: var(--ink);
  margin-right: 0.35rem;
}
.strip circle.on {
  stroke: var(--ink);
}
.sx {
  font-size: 11px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.sxv {
  font-size: 13px;
  font-weight: 650;
  fill: var(--ink);
}
.sxs {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
</style>
