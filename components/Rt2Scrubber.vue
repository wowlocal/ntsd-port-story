<script setup lang="ts">
// Chapter 15: every ledger row of CORE_REALTIME.md from 4m to 4ad on one axis (step order), compute per tick on the
// A12's main and render threads, vs (thick) and the Demo (thin, measured from 4z on). Hollow rings are measured builds
// that were not committed. Drag or hover the chart to move the cursor; the readout shows the step's own same-session
// A/B (the previous build run interleaved with it), its verdict, review and probe. On slide entry the lines draw and
// the cursor sweeps to the last step; export shows the last measured step (e5).
// Data: data/rt2_steps.json (scripts/collect_realtime2.py).
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'
import data from '../data/rt2_steps.json'

const nav = useNav()
const active = useIsSlideActive()
const d = data as any
const start = { id: '4l', label: 'глава 14 остановилась здесь', hash: d.start.hash, time: d.start.time, verdict: 'start', review: 'none', focus: 'main', vs: { after: d.start.vs, base: null }, demo: null, probe: null }
const steps = [start, ...d.steps] as any[]
const N = steps.length
const lastMeasured = steps.map((s, i) => ({ s, i })).filter(o => o.s.id === 'e5')[0].i

const W = 884
const H = 238
const m = { l: 30, r: 104, t: 22, b: 30 }
const YMAX = 26
const x = (i: number) => m.l + 6 + i * ((W - m.l - m.r - 12) / (N - 1))
const y = (v: number) => m.t + (1 - v / YMAX) * (H - m.t - m.b)
const f2 = (v: number | null | undefined) => v == null ? '—' : v.toFixed(2).replace('.', ',')
const f1 = (v: number) => v.toFixed(1).replace('.', ',')
const sgn = (v: number) => (v > 0 ? '+' : v < 0 ? '−' : '±') + Math.abs(v).toFixed(2).replace('.', ',')

const onLine = (s: any) => !['reverted', 'parked'].includes(s.verdict)
function path(scen: 'vs' | 'demo', key: 'main' | 'render') {
  let p = ''
  steps.forEach((s, i) => {
    const a = s[scen]?.after
    if (!onLine(s) || !a || a[key] == null)
      return
    p += `${p ? 'L' : 'M'}${x(i).toFixed(1)},${y(a[key]).toFixed(1)}`
  })
  return p
}
const lines = [
  { key: 'vsMain', d: path('vs', 'main'), color: 'var(--s2)', w: 2.2, op: 1 },
  { key: 'vsRender', d: path('vs', 'render'), color: 'var(--s1)', w: 2.2, op: 1 },
  { key: 'demoMain', d: path('demo', 'main'), color: 'var(--s2)', w: 1.3, op: 0.6 },
  { key: 'demoRender', d: path('demo', 'render'), color: 'var(--s1)', w: 1.3, op: 0.6 },
]
const rings = steps.map((s, i) => ({ s, i })).filter(o => !onLine(o.s) && o.s.vs?.after)

// day bands from the commit times ('MM-DD HH:MM')
const dayName: Record<string, string> = { '10-07': '7 октября', '10-08': '8 октября', '10-09': '9 октября', '10-10': '10 октября' }
const days = Object.keys(dayName).map((k) => {
  const idx = steps.map((s, i) => ({ s, i })).filter(o => o.s.time?.startsWith(k)).map(o => o.i)
  return { k, name: dayName[k], a: Math.min(...idx), b: Math.max(...idx) }
})

const marks = [
  { id: '4aa', text: '60 fps', anchor: 'end' },
  { id: 'S1', text: 'vs ≤ 16 мс', anchor: 'start' },
  { id: 'P0', text: 'быстрые ядра', anchor: 'end' },
  { id: 'R2', text: 'presenter', anchor: 'start' },
].map(o => ({ ...o, i: steps.findIndex(s => s.id === o.id) }))

const cur = ref(lastMeasured)
const s = computed(() => steps[cur.value])
const drawn = ref(true)

// pointer: hover and drag both move the cursor
const svg = ref<SVGSVGElement | null>(null)
function pick(e: PointerEvent) {
  const r = svg.value?.getBoundingClientRect()
  if (!r || r.width === 0)
    return
  const px = ((e.clientX - r.left) / r.width) * W
  let best = 0
  let bd = Infinity
  for (let i = 0; i < N; i++) {
    const dd = Math.abs(x(i) - px)
    if (dd < bd) {
      bd = dd
      best = i
    }
  }
  cur.value = best
}
let dragging = false
function down(e: PointerEvent) {
  dragging = true
  stopSweep()
  ;(e.currentTarget as Element).setPointerCapture?.(e.pointerId)
  pick(e)
}
function move(e: PointerEvent) {
  stopSweep()
  pick(e)
}
function up() {
  dragging = false
}

let raf = 0
function stopSweep() {
  cancelAnimationFrame(raf)
}
function play() {
  if (nav.isPrintMode.value) {
    cur.value = lastMeasured
    drawn.value = true
    return
  }
  drawn.value = false
  requestAnimationFrame(() => {
    drawn.value = true
  })
  cancelAnimationFrame(raf)
  const t0 = performance.now()
  const dur = 2600
  const tick = (t: number) => {
    const k = Math.min(1, (t - t0) / dur)
    cur.value = Math.round(k * lastMeasured)
    if (k < 1 && !dragging)
      raf = requestAnimationFrame(tick)
  }
  raf = requestAnimationFrame(tick)
}
onMounted(() => {
  if (active.value && !nav.isPrintMode.value)
    play()
})
watch(active, (v) => {
  if (v)
    play()
})
onBeforeUnmount(() => cancelAnimationFrame(raf))

const verdictName: Record<string, string> = {
  start: 'старт главы', kept: 'быстрее — закоммичено', less: 'меньше работы, в пределах шума — закоммичено',
  reverted: 'не быстрее — откат', parked: 'замерено — отложено', follow: 'доработка после ревью', test: 'только тесты',
  telemetry: 'только телеметрия', procedure: 'правило процедуры', build: 'сборка пакетов', decision: 'решение автора',
}
const verdictClass = (v: string) => ['kept', 'decision'].includes(v) ? 'good' : v === 'less' ? 'less' : ['reverted', 'parked'].includes(v) ? 'bad' : 'plain'
const reviewName: Record<string, string> = {
  ok: 'независимое ревью: одобрено', nits: 'независимое ревью: одобрено с замечаниями', caught: 'ревью или ворота нашли дефект — исправлен до коммита',
  skipped: 'ревью не требовалось', none: '',
}
const day = (t: string | null) => {
  if (!t)
    return ''
  const [md, hm] = t.split(' ')
  return `${Number(md.split('-')[1])} окт, ${hm}`
}
function ab(scen: 'vs' | 'demo') {
  const v = s.value[scen]
  if (!v?.after)
    return null
  return {
    n: v.after.n, base: v.base,
    main: v.after.main, render: v.after.render,
    dMain: v.base ? v.after.main - v.base.main : null,
    dRender: v.base ? v.after.render - v.base.render : null,
    present: v.after.present, release: v.after.release,
  }
}
const vsAB = computed(() => ab('vs'))
const demoAB = computed(() => ab('demo'))
const cx = computed(() => x(cur.value))
const dots = computed(() => {
  const out: { cx: number, cy: number, color: string, op: number }[] = []
  const add = (scen: 'vs' | 'demo', key: 'main' | 'render', color: string, op: number) => {
    const a = s.value[scen]?.after
    if (a && a[key] != null)
      out.push({ cx: cx.value, cy: y(a[key]), color, op })
  }
  add('demo', 'render', 'var(--s1)', 0.7)
  add('demo', 'main', 'var(--s2)', 0.7)
  add('vs', 'render', 'var(--s1)', 1)
  add('vs', 'main', 'var(--s2)', 1)
  return out
})
const whisk = computed(() => {
  const a = s.value.vs?.after
  if (!a || a.mainMin == null)
    return []
  return [
    { y1: y(a.mainMax), y2: y(a.mainMin), color: 'var(--s2)' },
    { y1: y(a.renderMax), y2: y(a.renderMin), color: 'var(--s1)' },
  ]
})
// probe bars: the larger share fills the track
const barW = (v: number) => {
  const p = s.value.probe
  return p ? (62 * v) / Math.max(p.before, p.after) : 0
}
const runs = (n: number) => `${n} ${n % 10 === 1 && n % 100 !== 11 ? 'прогон' : [2, 3, 4].includes(n % 10) && ![12, 13, 14].includes(n % 100) ? 'прогона' : 'прогонов'}`
const demoFrom = steps.findIndex(st => st.id === d.firstDemo.id)
const endVs = d.end.vs
const endDemo = d.end.demo
const lx = x(lastMeasured)
</script>

<template>
  <div class="scrub">
    <svg
      ref="svg" :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" class="plot"
      :aria-label="`Мс работы на тик по ступеням: главный поток vs ${f2(d.start.vs.main)} → ${f2(endVs.main)}, рендер ${f2(d.start.vs.render)} → ${f2(endVs.render)}`"
      @pointerdown="down" @pointermove="move" @pointerup="up" @pointercancel="up"
    >
      <!-- day bands -->
      <g v-for="(dd, k) in days" :key="dd.k">
        <rect v-if="k % 2 === 1" :x="x(dd.a) - 4" :y="m.t - 8" :width="x(dd.b) - x(dd.a) + 8" :height="H - m.t - m.b + 8" fill="rgba(255,255,255,0.025)" />
        <text :x="(x(dd.a) + x(dd.b)) / 2" :y="H - 8" text-anchor="middle" class="day">{{ dd.name }}</text>
      </g>
      <!-- grid -->
      <g v-for="t in [0, 10, 20]" :key="t">
        <line :x1="m.l" :x2="lx + 6" :y1="y(t)" :y2="y(t)" stroke="var(--grid)" />
        <text :x="m.l - 6" :y="y(t) + 3.5" text-anchor="end" class="tick">{{ t }}</text>
      </g>
      <text :x="m.l - 6" :y="m.t - 10" text-anchor="end" class="tick">мс</text>
      <!-- tiers -->
      <line :x1="m.l" :x2="lx + 6" :y1="y(16.67)" :y2="y(16.67)" stroke="var(--ink-2)" stroke-width="1" stroke-dasharray="4 3" />
      <text :x="lx - 4" :y="y(16.67) - 5" text-anchor="end" class="tier">16,67 мс — 60 кадров/с</text>
      <line :x1="m.l" :x2="lx + 6" :y1="y(16)" :y2="y(16)" stroke="var(--ink-2)" stroke-width="1.4" />
      <line :x1="m.l" :x2="lx + 6" :y1="y(8)" :y2="y(8)" stroke="var(--ink-2)" stroke-width="1.4" />
      <text :x="m.l + 4" :y="y(8) - 5" class="tier">8 мс — ярус 3</text>
      <text :x="lx - 4" :y="y(16) + 13" text-anchor="end" class="tier">16 мс — ярус 2</text>

      <!-- event marks -->
      <g v-for="mk in marks" :key="mk.id">
        <line :x1="x(mk.i)" :x2="x(mk.i)" :y1="m.t - 6" :y2="m.t + 2" stroke="var(--muted)" />
        <text :x="x(mk.i) + (mk.anchor === 'end' ? 3 : -3)" :y="m.t - 10" :text-anchor="mk.anchor" class="mk"><tspan class="mkid">{{ mk.id }}</tspan> {{ mk.text }}</text>
      </g>

      <!-- lines -->
      <path
        v-for="l in lines" :key="l.key" :d="l.d" fill="none" :stroke="l.color" :stroke-width="l.w" :style="{ opacity: l.op }"
        stroke-linejoin="round" stroke-linecap="round" pathLength="1" class="ln" :class="{ drawn }"
      />
      <!-- not committed -->
      <g v-for="o in rings" :key="`r${o.i}`">
        <circle :cx="x(o.i)" :cy="y(o.s.vs.after.main)" r="3.6" fill="none" stroke="var(--s2)" stroke-width="1.4" />
        <circle v-if="o.s.focus === 'render'" :cx="x(o.i)" :cy="y(o.s.vs.after.render)" r="3.6" fill="none" stroke="var(--s1)" stroke-width="1.4" />
      </g>

      <!-- start / end labels -->
      <text :x="x(0) + 6" :y="y(d.start.vs.main) - 7" class="end">{{ f1(d.start.vs.main) }}</text>
      <text :x="x(0) + 6" :y="y(d.start.vs.render) - 7" class="end">{{ f1(d.start.vs.render) }}</text>
      <text :x="lx + 12" :y="y(endVs.main) - 9" class="lbs">Demo {{ f2(endDemo.main) }}</text>
      <text :x="lx + 12" :y="y(endVs.main) + 5"><tspan class="lbl">главный </tspan><tspan class="lv">{{ f2(endVs.main) }}</tspan></text>
      <text :x="lx + 12" :y="y(endVs.render) + 5"><tspan class="lbl">рендер </tspan><tspan class="lv">{{ f2(endVs.render) }}</tspan></text>
      <text :x="lx + 12" :y="y(endVs.render) + 19" class="lbs">Demo {{ f2(endDemo.render) }}</text>

      <!-- cursor -->
      <line :x1="cx" :x2="cx" :y1="m.t - 2" :y2="H - m.b" stroke="var(--ink)" stroke-width="1" style="opacity: 0.55" />
      <line v-for="(w, k) in whisk" :key="`w${k}`" :x1="cx + 6 + k * 4" :x2="cx + 6 + k * 4" :y1="w.y1 - 0.5" :y2="w.y2 + 0.5" :stroke="w.color" stroke-width="2" stroke-linecap="round" />
      <circle v-for="(p, k) in dots" :key="`d${k}`" :cx="p.cx" :cy="p.cy" r="4.2" :fill="p.color" :style="{ opacity: p.op }" stroke="var(--bg)" stroke-width="2" />
      <rect :x="m.l" :y="m.t - 30" :width="lx - m.l + 10" :height="H - m.t - m.b + 30" fill="transparent" class="hit" />
    </svg>

    <div class="read">
      <div class="c1">
        <div class="hd">
          <span class="sid pixel">{{ s.id === 'R2@09' ? 'R2' : s.id }}</span>
          <span class="mono xs">{{ day(s.time) }} · {{ s.hash }}</span>
        </div>
        <div class="lab">
          {{ s.label }}
        </div>
        <div class="chips">
          <span class="chip" :class="verdictClass(s.verdict)">{{ verdictName[s.verdict] }}</span>
          <span v-if="reviewName[s.review]" class="chip plain" :class="{ warn: s.review === 'caught' }">{{ reviewName[s.review] }}</span>
        </div>
      </div>
      <div v-for="sc in [{ k: 'vs', name: 'vs · два бойца', v: vsAB }, { k: 'demo', name: 'Demo · восемь бойцов', v: demoAB }]" :key="sc.k" class="c2">
        <div class="sh">
          {{ sc.name }}
        </div>
        <template v-if="sc.v">
          <div class="row">
            <i class="key" style="background: var(--s2)" /><b>{{ f2(sc.v.main) }}</b> мс
            <span v-if="sc.v.dMain != null" class="dl">{{ sgn(sc.v.dMain) }}</span>
          </div>
          <div class="row">
            <i class="key" style="background: var(--s1)" /><b>{{ f2(sc.v.render) }}</b> мс
            <span v-if="sc.v.dRender != null" class="dl">{{ sgn(sc.v.dRender) }}</span>
          </div>
          <div class="nt">
            {{ runs(sc.v.n) }}{{ sc.v.base ? ` · база ${sc.v.base.n}${sc.v.base.interleaved ? ', вперемешку' : ''}` : '' }}<template v-if="sc.v.present">
              · presenter {{ f1(sc.v.present) }}
            </template><template v-if="sc.v.release">
              · release {{ f1(sc.v.release) }}
            </template>
          </div>
        </template>
        <div v-else class="nt">
          {{ sc.k === 'demo' && cur < demoFrom ? 'Demo ещё не мерили (с 4z, 8 окт)' : 'без замера на телефоне' }}
        </div>
      </div>
      <div class="c3">
        <div class="sh">
          профиль, доля потока
        </div>
        <template v-if="s.probe">
          <div class="pw mono">
            {{ s.probe.what }}
          </div>
          <div class="probe-row">
            <i class="bar was" :style="{ width: `${barW(s.probe.before)}%` }" /><span>{{ String(s.probe.before).replace('.', ',') }} %</span>
          </div>
          <div class="probe-row">
            <i class="bar now" :style="{ width: `${barW(s.probe.after)}%` }" /><span>{{ String(s.probe.after).replace('.', ',') }} %</span>
          </div>
        </template>
        <div v-else class="nt">
          в строке реестра нет пробы «до → после»
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.plot {
  display: block;
  touch-action: none;
  cursor: ew-resize;
  user-select: none;
}
.hit {
  cursor: ew-resize;
}
.day {
  font-size: 10.5px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
}
.tier {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.mk {
  font-size: 10px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.mkid {
  fill: var(--naruto);
  font-family: var(--font-pixel);
}
.end {
  font-size: 12px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.lbl {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.lv {
  font-size: 12.5px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.lbs {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.ln {
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
}
.ln.drawn {
  stroke-dashoffset: 0;
  transition: stroke-dashoffset 2.6s cubic-bezier(0.3, 0.1, 0.3, 1);
}
.slidev-print .ln,
.print .ln {
  stroke-dashoffset: 0;
}
.read {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1.05fr;
  gap: 0.7rem;
  margin-top: 0.3rem;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.5rem 0.75rem 0.55rem;
  min-height: 6.5rem;
}
.hd {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}
.sid {
  font-size: 1.15rem;
  color: var(--naruto);
}
.xs {
  font-size: 0.64rem;
  color: var(--muted);
}
.lab {
  font-size: 0.8rem;
  line-height: 1.3;
  color: var(--ink);
  margin: 0.1rem 0 0.3rem;
  min-height: 2.1em;
}
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}
.chip {
  font-size: 0.62rem;
  line-height: 1.25;
  padding: 0.08rem 0.45rem;
  border-radius: 999px;
  border: 1px solid var(--hair);
  color: var(--ink-2);
  background: rgba(255, 255, 255, 0.04);
}
.chip.good {
  border-color: rgba(12, 163, 12, 0.6);
  color: var(--ink);
}
.chip.less {
  border-color: rgba(195, 194, 183, 0.4);
}
.chip.bad {
  border-color: rgba(236, 131, 90, 0.7);
  color: var(--ink);
}
.chip.warn {
  border-color: rgba(250, 178, 25, 0.6);
}
.sh {
  font-size: 0.64rem;
  color: var(--muted);
  border-bottom: 1px solid var(--grid);
  padding-bottom: 0.12rem;
  margin-bottom: 0.2rem;
}
.row {
  display: flex;
  align-items: baseline;
  gap: 0.3rem;
  font-size: 0.72rem;
  color: var(--ink-2);
  line-height: 1.45;
}
.row b {
  font-size: 0.95rem;
  color: var(--ink);
  font-weight: 650;
  font-variant-numeric: tabular-nums;
}
.key {
  display: inline-block;
  width: 12px;
  height: 2.5px;
  border-radius: 2px;
  transform: translateY(-3px);
}
.dl {
  margin-left: auto;
  font-size: 0.7rem;
  color: var(--ink-2);
  font-variant-numeric: tabular-nums;
}
.nt {
  font-size: 0.62rem;
  color: var(--muted);
  line-height: 1.3;
  margin-top: 0.1rem;
}
.pw {
  font-size: 0.66rem;
  color: var(--ink);
  margin-bottom: 0.2rem;
  line-height: 1.25;
}
.probe-row {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.66rem;
  color: var(--ink-2);
  margin: 0.15rem 0;
}
.bar {
  display: inline-block;
  height: 9px;
  border-radius: 0 3px 3px 0;
}
.bar.was {
  background: #566074;
}
.bar.now {
  background: var(--naruto);
}
</style>
