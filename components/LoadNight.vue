<script setup lang="ts">
// The memory/loading night on one clock (10 Oct 21:00 -> 11 Oct 20:30, local time): every gated step at its
// commit time, the new build's median from that gate's own A/B. Two panels with their own y-axes (small multiples):
// loading time (log scale) and peak memory. A12 <-> Mac switches the host. Drag across the chart (or use the
// arrow keys, or "play") to pick a step; the card below shows that gate's A/B with ranges. Rings: steps that were
// not taken (rejected, held for the human, parked). Lane on top: the human's turns, compactions; hatching: the agent
// had finished and waited for the human. Export shows the A12 with step L3 picked.
// Data: data/loading_steps.json, data/loading_night.json (scripts/collect_loading.py).
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'
import steps from '../data/loading_steps.json'
import night from '../data/loading_night.json'

const nav = useNav()
const active = useIsSlideActive()
const S = (steps as any).steps as any[]
const N = night as any
const T0 = new Date(N.t0).getTime()
const hOf = (iso: string) => (new Date(`${iso}:00+02:00`).getTime() - T0) / 3.6e6
const famColor: Record<string, string> = {
  inplace: 'var(--s2)', parallel: 'var(--s1)', search: 'var(--s4)', convert: 'var(--s5)', memory: 'var(--s3)',
}

// events the scrubber can stop at: every gated step, plus two checks that changed how the loop measured
const checks = [
  { id: 'проверка', hash: 'db3c605', name: 'Прогрев A/B и дрейф телефона', how: 'Запуск → меню вырос на 1,2 с «после M5b». A/B S2 против M5b в одной сессии: 12,71–12,75 против 12,62–12,70 с — одинаково. Замедлился телефон, не код; первая сборка в серии ждёт дольше всех — теперь перед замером прогон-прогрев.' },
  { id: 'аудит', hash: '85fab5b', name: 'Аудит RAM по просьбе человека', how: 'Свежая база A12 со звуком: пик 565 МиБ (555–581). Из 1 597 МиБ, выделенных в куче, реально заняты 405–450: остальное — нетронутые страницы поверхностей. Самый большой держатель в игре — музыка: её не включал ни один прогон.' },
]
interface Ev { kind: 'step' | 'check', h: number, s?: any, c?: any }
const events: Ev[] = [
  ...S.map(s => ({ kind: 'step' as const, h: hOf(s.time), s })),
  ...checks.map(c => ({ kind: 'check' as const, h: N.commits.find((x: any) => x.hash === c.hash).h, c })),
].sort((a, b) => a.h - b.h)

const host = ref<'a12' | 'mac'>('a12')
const defaultSel = events.findIndex(e => e.s?.id === 'L3')
const sel = ref(defaultSel)
const host_ = computed(() => (nav.isPrintMode.value ? 'a12' : host.value))
const selIdx = computed(() => (nav.isPrintMode.value ? defaultSel : sel.value))
const cur = computed(() => events[selIdx.value])

// ---- geometry
const W = 884
const ml = 62
const mr = 14
const span = N.spanHours as number
const X = (h: number) => ml + (h / span) * (W - ml - mr)
const lane = { top: 2, h: 30 }
const A = { top: 56, h: 100 }
const B = { top: 184, h: 70 }
const axisY = B.top + B.h + 6
const H = axisY + 34

const cfg = computed(() => host_.value === 'a12'
  ? { lmin: 4, lmax: 150, lt: [5, 10, 20, 50, 100], mmax: 1700, mt: [0, 500, 1000, 1500], mu: 'МиБ', loadKey: 'phone', name: 'Galaxy A12' }
  : { lmin: 0.25, lmax: 7, lt: [0.3, 0.5, 1, 2, 5], mmax: 2200, mt: [0, 1000, 2000], mu: 'МБ', loadKey: 'mac', name: 'Mac' })
const yL = (v: number) => {
  const c = cfg.value
  const k = (Math.log(v) - Math.log(c.lmin)) / (Math.log(c.lmax) - Math.log(c.lmin))
  return A.top + (1 - k) * A.h
}
const yM = (v: number) => B.top + (1 - v / cfg.value.mmax) * B.h
const side = (s: any) => s[cfg.value.loadKey]
const load = (s: any) => side(s).new.load[0]
const peak = (s: any) => side(s).new.peak[0]

const done = S.filter(s => s.status === 'done')
const notTaken = S.filter(s => s.status !== 'done')
const startH = (N.human as number[])[0]
const stopH = N.commits[N.commits.length - 1].h
// stepped line: the baseline from the human's first turn, then at each gate's commit the drop to its new median
function pathFor(val: (s: any) => number, y: (v: number) => number, base: number) {
  let p = `M${X(startH)},${y(base)}`
  for (const s of done)
    p += ` H${X(hOf(s.time))} V${y(val(s))}`
  return `${p} H${X(stopH)}`
}
const loadPath = computed(() => pathFor(load, yL, side(done[0]).prev.load[0]))
const peakPath = computed(() => pathFor(peak, yM, side(done[0]).prev.peak[0]))
const base = computed(() => ({ load: side(done[0]).prev.load[0], peak: side(done[0]).prev.peak[0] }))
const last = done[done.length - 1]

const fmt = (v: number, d = 1) => v.toLocaleString('ru-RU', { minimumFractionDigits: d, maximumFractionDigits: d })
const fl = (v: number) => (v >= 10 ? fmt(v, 1) : v >= 1 ? fmt(v, 2) : fmt(v, 3))
const f1 = (v: number) => (v >= 1 ? fmt(v, 1) : fmt(v, 2))
const fm = (v: number) => Math.round(v).toLocaleString('ru-RU')
const clock = (h: number) => {
  const m = Math.round((h * 60 + 21 * 60)) % 1440
  return `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`
}
const labelled: Record<string, { dx: number, dy: number, anchor?: string }> = {
  L1: { dx: 4, dy: -6 },
  L2: { dx: 4, dy: -6 },
  L3: { dx: 4, dy: -6 },
  L5: { dx: 4, dy: -6 },
  L13: { dx: 4, dy: -6 },
  'L18+19': { dx: 4, dy: -6 },
}
const memLabelled: Record<string, { dx: number, dy: number }> = { M1: { dx: 4, dy: -5 }, M2: { dx: 4, dy: -5 }, M5b: { dx: 4, dy: -5 } }

// time axis: every two hours, the date at midnight
const hourTicks = Array.from({ length: 12 }, (_, i) => 1 + i * 2).filter(h => h <= span)
const midnight = 3

// human lane: clusters with short labels (descriptions, not quotes)
const humanLabels = [
  { h: 0.39, text: 'старт цикла', anchor: 'start', dx: 6 },
  { h: 17.34, text: 'правило, подозрение', anchor: 'end', dx: 4 },
  { h: 19.21, text: '«ждёшь?»', anchor: 'middle', dx: 0 },
  { h: 20.29, text: 'RAM', anchor: 'start', dx: 5 },
  { h: 22.2, text: 'M8 · стоп', anchor: 'middle', dx: 0 },
]

// ---- interaction
const svgEl = ref<SVGSVGElement | null>(null)
let dragging = false
function pick(e: PointerEvent) {
  const r = svgEl.value?.getBoundingClientRect()
  if (!r || r.width === 0)
    return
  const x = ((e.clientX - r.left) / r.width) * W
  let best = 0
  let bd = Infinity
  events.forEach((ev, i) => {
    const dd = Math.abs(X(ev.h) - x)
    if (dd < bd) {
      bd = dd
      best = i
    }
  })
  sel.value = best
}
function down(e: PointerEvent) {
  stopPlay()
  dragging = true
  ;(e.currentTarget as Element).setPointerCapture?.(e.pointerId)
  pick(e)
}
function move(e: PointerEvent) {
  if (dragging)
    pick(e)
}
function up() {
  dragging = false
}
function key(e: KeyboardEvent) {
  if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
    e.preventDefault()
    e.stopPropagation()
    stopPlay()
    sel.value = Math.max(0, Math.min(events.length - 1, sel.value + (e.key === 'ArrowRight' ? 1 : -1)))
  }
}
// give the keyboard back to the deck after a button press
const blur = (e: Event) => (e.currentTarget as HTMLElement | null)?.blur()
let timer: ReturnType<typeof setInterval> | null = null
const playing = ref(false)
function stopPlay() {
  if (timer)
    clearInterval(timer)
  timer = null
  playing.value = false
}
function play() {
  if (playing.value)
    return stopPlay()
  sel.value = 0
  playing.value = true
  timer = setInterval(() => {
    if (sel.value >= events.length - 1)
      return stopPlay()
    sel.value++
  }, 650)
}
watch(active, (v) => {
  if (!v)
    stopPlay()
})
onBeforeUnmount(stopPlay)

// ---- readout
const gainText: Record<string, string> = { measured: 'измерено', overlap: 'в пределах разброса', worse: 'хуже' }
const statusText: Record<string, string> = { rejected: 'отклонено', held: 'ждёт решения человека', parked: 'отложено' }
const r = computed(() => {
  const ev = cur.value
  if (ev.kind === 'check')
    return null
  const s = ev.s
  const p = s.phone
  const m = s.mac
  const rng = (a: number[], f: (v: number) => string) => `${f(a[1])}–${f(a[2])}`
  return {
    s,
    a12: `загрузка ${fl(p.prev.load[0])} → <b>${fl(p.new.load[0])} с</b> <span class="rg">(${rng(p.new.load, fl)} против ${rng(p.prev.load, fl)})</span> <i class="g">${gainText[p.loadGain] ?? ''}</i> · пик ${fm(p.prev.peak[0])} → <b>${fm(p.new.peak[0])} МиБ</b> <i class="g">${gainText[p.peakGain] ?? ''}</i>`,
    mac: `загрузка ${fl(m.prev.load[0])} → <b>${fl(m.new.load[0])} с</b> · пик ${fm(m.prev.peak[0])} → <b>${fm(m.new.peak[0])} МБ</b>`,
    loadGain: gainText[p.loadGain] ?? '',
    peakGain: gainText[p.peakGain] ?? '',
    macLoadGain: gainText[m.loadGain] ?? '',
    cond: [s.sounds ? 'со звуком' : 'без звука', s.music ? 'с музыкой' : null].filter(Boolean).join(', '),
  }
})
</script>

<template>
  <div class="night">
    <div class="ctl">
      <div class="seg">
        <button :class="{ on: host_ === 'a12' }" @click="blur($event); host = 'a12'">
          Galaxy A12
        </button>
        <button :class="{ on: host_ === 'mac' }" @click="blur($event); host = 'mac'">
          Mac
        </button>
      </div>
      <button v-if="!nav.isPrintMode.value" class="play" @click="blur($event); play()">
        <span :class="playing ? 'i-pixelarticons-pause' : 'i-pixelarticons-play'" />{{ playing ? 'пауза' : 'прогнать ночь' }}
      </button>
      <span class="hint">{{ nav.isPrintMode.value ? 'выбрана ступень L3' : 'тяните по графику, ← →' }}</span>
      <span class="keys">
        <i class="k dot" />реплика человека
        <i class="k tri" />сжатие контекста
        <i class="k hatch" />агент ждал человека
        <i class="k ring" />не принято
        <i class="k dia" />проверка
      </span>
    </div>

    <svg
      ref="svgEl" :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" tabindex="0"
      :aria-label="`Ночь цикла: ${cfg.name}, загрузка и пик памяти после каждой ступени`"
      @pointerdown="down" @pointermove="move" @pointerup="up" @pointercancel="up" @keydown="key"
    >
      <defs>
        <pattern id="ln-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect width="6" height="6" fill="rgba(255,255,255,0.02)" />
          <line x1="0" y1="0" x2="0" y2="6" stroke="rgba(255,255,255,0.09)" stroke-width="2" />
        </pattern>
      </defs>

      <!-- idle stretches -->
      <g v-for="(g, i) in N.idle" :key="`i${i}`">
        <rect :x="X(g[0])" :y="A.top - 4" :width="X(g[1]) - X(g[0])" :height="axisY - A.top + 4" fill="url(#ln-hatch)" />
      </g>
      <text :x="(X(N.idle[0][0]) + X(N.idle[0][1])) / 2" :y="A.top + 12" text-anchor="middle" class="idle">агент ждал</text>

      <!-- human lane -->
      <text x="0" :y="lane.top + 14" class="pl">человек</text>
      <line :x1="ml" :x2="W - mr" :y1="lane.top + 10" :y2="lane.top + 10" stroke="var(--grid)" />
      <circle v-for="(h, i) in N.human" :key="`h${i}`" :cx="X(h)" :cy="lane.top + 10" r="4" fill="var(--chakra)" stroke="var(--bg)" stroke-width="1.5" />
      <path v-for="(c, i) in N.compactions" :key="`c${i}`" :d="`M${X(c)},${lane.top + 5} l4,9 h-8 z`" fill="var(--muted)" />
      <text v-for="l in humanLabels" :key="l.text" :x="X(l.h) + l.dx" :y="lane.top + 27" :text-anchor="l.anchor" class="hl">{{ l.text }}</text>

      <!-- panel A: load, log scale -->
      <text :x="ml" :y="A.top - 8" class="pl">загрузка, с <tspan class="pls">· логарифмическая шкала</tspan></text>
      <g v-for="t in cfg.lt" :key="`a${t}`">
        <line :x1="ml" :x2="W - mr" :y1="yL(t)" :y2="yL(t)" stroke="var(--grid)" />
        <text :x="ml - 6" :y="yL(t) + 3.5" text-anchor="end" class="tick">{{ String(t).replace('.', ',') }}</text>
      </g>
      <path :d="loadPath" fill="none" stroke="var(--ink-2)" stroke-width="2" stroke-linejoin="round" />
      <g v-for="s in done" :key="`p${s.id}`">
        <circle :cx="X(hOf(s.time))" :cy="yL(load(s))" r="4" :fill="famColor[s.family]" stroke="var(--bg)" stroke-width="2" />
        <text v-if="labelled[s.id] && host_ === 'a12'" :x="X(hOf(s.time)) + labelled[s.id].dx" :y="yL(load(s)) + labelled[s.id].dy" class="sid">{{ s.id }}</text>
        <text v-if="s.id === 'L18+19'" :x="X(hOf(s.time)) + 2" :y="yL(load(s)) + 17" class="end">{{ f1(load(s)) }} с</text>
      </g>
      <g v-for="s in notTaken" :key="`n${s.id}`">
        <circle :cx="X(hOf(s.time))" :cy="yL(load(s))" r="4.5" fill="none" stroke="var(--ink-2)" stroke-width="1.6" />
      </g>
      <text :x="X(startH) + 2" :y="yL(base.load) + 16" class="end">{{ f1(base.load) }} с</text>
      <text :x="X(stopH) + 2" :y="yL(load(last)) + 17" text-anchor="end" class="end">{{ f1(load(last)) }} с</text>

      <!-- panel B: peak memory -->
      <text :x="ml" :y="B.top - 8" class="pl">пик памяти, {{ cfg.mu }} <tspan class="pls">· {{ host_ === 'a12' ? 'RSS + swap' : 'phys_footprint_peak' }}</tspan></text>
      <g v-for="t in cfg.mt" :key="`b${t}`">
        <line :x1="ml" :x2="W - mr" :y1="yM(t)" :y2="yM(t)" :stroke="t === 0 ? 'var(--axis)' : 'var(--grid)'" />
        <text :x="ml - 6" :y="yM(t) + 3.5" text-anchor="end" class="tick">{{ t.toLocaleString('ru-RU') }}</text>
      </g>
      <path :d="peakPath" fill="none" stroke="var(--ink-2)" stroke-width="2" stroke-linejoin="round" />
      <g v-for="s in done" :key="`q${s.id}`">
        <circle :cx="X(hOf(s.time))" :cy="yM(peak(s))" r="4" :fill="famColor[s.family]" stroke="var(--bg)" stroke-width="2" />
        <text v-if="memLabelled[s.id] && host_ === 'a12'" :x="X(hOf(s.time)) + memLabelled[s.id].dx" :y="yM(peak(s)) + memLabelled[s.id].dy" class="sid">{{ s.id }}</text>
      </g>
      <g v-for="s in notTaken" :key="`m${s.id}`">
        <circle :cx="X(hOf(s.time))" :cy="yM(peak(s))" r="4.5" fill="none" stroke="var(--ink-2)" stroke-width="1.6" />
      </g>
      <text :x="X(startH) + 2" :y="yM(base.peak) + 16" class="end">{{ fm(base.peak) }}</text>
      <text :x="X(stopH) + 2" :y="yM(peak(last)) - 8" text-anchor="end" class="end">{{ fm(peak(last)) }}</text>

      <!-- time axis -->
      <line :x1="ml" :x2="W - mr" :y1="axisY" :y2="axisY" stroke="var(--axis)" />
      <g v-for="h in hourTicks" :key="`t${h}`">
        <line :x1="X(h)" :x2="X(h)" :y1="axisY" :y2="axisY + 4" stroke="var(--axis)" />
        <text :x="X(h)" :y="axisY + 15" text-anchor="middle" class="tick">{{ clock(h) }}</text>
      </g>
      <!-- checks on the axis -->
      <g v-for="(ev, i) in events" :key="`e${i}`">
        <path v-if="ev.kind === 'check'" :d="`M${X(ev.h)},${axisY - 6} l6,6 l-6,6 l-6,-6 z`" fill="var(--ink-2)" stroke="var(--bg)" stroke-width="1.5" />
      </g>
      <text :x="X(0)" :y="axisY + 29" class="date">10 окт</text>
      <line :x1="X(midnight)" :x2="X(midnight)" :y1="A.top - 2" :y2="A.top + A.h" stroke="var(--axis)" />
      <line :x1="X(midnight)" :x2="X(midnight)" :y1="B.top - 2" :y2="axisY + 22" stroke="var(--axis)" />
      <text :x="X(midnight) + 4" :y="axisY + 29" class="date">11 окт</text>

      <!-- scrubber -->
      <line :x1="X(cur.h)" :x2="X(cur.h)" :y1="lane.top + 18" :y2="axisY" stroke="var(--naruto)" stroke-width="1.5" />
      <template v-if="cur.kind === 'step'">
        <circle :cx="X(cur.h)" :cy="yL(load(cur.s))" r="7" fill="none" stroke="var(--ink)" stroke-width="2" />
        <circle :cx="X(cur.h)" :cy="yM(peak(cur.s))" r="7" fill="none" stroke="var(--ink)" stroke-width="2" />
      </template>
      <rect :x="ml" :y="lane.top" :width="W - ml - mr" :height="axisY - lane.top" fill="transparent" style="cursor: ew-resize" />
    </svg>

    <div class="card-r">
      <template v-if="cur.kind === 'step' && r">
        <div class="r1">
          <span class="t mono">{{ clock(cur.h) }}</span>
          <span class="chip" :style="{ '--c': famColor[r.s.family] }">{{ r.s.id }}</span>
          <span class="nm">{{ r.s.name }}</span>
          <span v-if="r.s.status !== 'done'" class="st">{{ statusText[r.s.status] }}</span>
          <code class="hh">{{ r.s.hash }}</code>
          <span class="cond">{{ r.cond }}</span>
        </div>
        <div class="how">
          {{ r.s.how }}
        </div>
        <div class="nums">
          <span :class="{ dim: host_ !== 'a12' }"><b class="hn">A12</b> <span v-html="r.a12" /></span>
          <span :class="{ dim: host_ !== 'mac' }"><b class="hn">Mac</b> <span v-html="r.mac" /></span>
        </div>
        <div v-if="r.s.reviewFinding" class="rev">
          {{ r.s.reviewFinding }}
        </div>
      </template>
      <template v-else-if="cur.kind === 'check'">
        <div class="r1">
          <span class="t mono">{{ clock(cur.h) }}</span>
          <span class="chip" style="--c: var(--ink-2)">{{ cur.c.id }}</span>
          <span class="nm">{{ cur.c.name }}</span>
          <code class="hh">{{ cur.c.hash }}</code>
        </div>
        <div class="how">
          {{ cur.c.how }}
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.ctl {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  white-space: nowrap;
  font-size: 0.66rem;
  color: var(--ink-2);
  margin-bottom: 0.15rem;
}
.seg {
  display: inline-flex;
}
.seg button,
.play {
  font-family: var(--font-sans);
  font-size: 0.7rem;
  color: var(--ink-2);
  background: var(--surface-2);
  border: 1px solid var(--axis);
  padding: 0.15rem 0.6rem;
  cursor: pointer;
}
.seg button:first-child {
  border-radius: 8px 0 0 8px;
}
.seg button:last-child {
  border-radius: 0 8px 8px 0;
  border-left: none;
}
.seg button.on {
  color: var(--ink);
  background: var(--surface-3);
  box-shadow: inset 0 -2px 0 var(--naruto);
}
.play {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  border-radius: 8px;
  color: var(--ink);
  background: rgba(255, 138, 61, 0.16);
  border-color: rgba(255, 138, 61, 0.6);
}
.hint {
  color: var(--muted);
}
.keys {
  font-size: 0.62rem;
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}
.k {
  display: inline-block;
  width: 9px;
  height: 9px;
  margin-left: 0.5rem;
}
.k.dot {
  border-radius: 50%;
  background: var(--chakra);
  margin-left: 0;
}
.k.tri {
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 9px solid var(--muted);
}
.k.hatch {
  width: 14px;
  background: repeating-linear-gradient(45deg, rgba(255, 255, 255, 0.16) 0 2px, rgba(255, 255, 255, 0.03) 2px 5px);
  border: 1px solid var(--hair);
}
.k.dia {
  width: 8px;
  height: 8px;
  background: var(--ink-2);
  transform: rotate(45deg);
}
.k.ring {
  border-radius: 50%;
  border: 1.5px solid var(--ink-2);
  box-sizing: border-box;
}
svg {
  display: block;
  touch-action: none;
  user-select: none;
  outline: none;
}
.pl {
  font-size: 11px;
  font-weight: 600;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.pls {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
}
.date {
  font-size: 10px;
  fill: var(--ink-2);
  font-family: var(--font-pixel);
}
.sid {
  font-size: 10px;
  fill: var(--ink-2);
  font-family: var(--font-mono);
}
.end {
  font-size: 11.5px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.hl {
  font-size: 10px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.idle {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.card-r {
  margin-top: 0.2rem;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-left: 3px solid var(--naruto);
  border-radius: 10px;
  padding: 0.35rem 0.75rem 0.4rem;
  min-height: 4.6rem;
}
.r1 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.74rem;
}
.r1 .t {
  color: var(--muted);
  font-size: 0.7rem;
}
.chip {
  font-family: var(--font-mono);
  font-size: 0.66rem;
  color: var(--ink);
  border: 1px solid var(--c);
  background: color-mix(in srgb, var(--c) 22%, transparent);
  border-radius: 6px;
  padding: 0 0.35rem;
}
.nm {
  font-weight: 650;
  color: var(--ink);
}
.st {
  font-size: 0.64rem;
  color: var(--warning);
  border: 1px solid rgba(250, 178, 25, 0.5);
  border-radius: 999px;
  padding: 0 0.45rem;
}
.hh {
  font-size: 0.6rem !important;
}
.cond {
  margin-left: auto;
  font-size: 0.62rem;
  color: var(--muted);
}
.how {
  font-size: 0.66rem;
  color: var(--ink-2);
  line-height: 1.32;
  margin-top: 0.12rem;
}
.nums {
  display: flex;
  flex-wrap: wrap;
  gap: 0.1rem 1.2rem;
  font-size: 0.66rem;
  color: var(--ink-2);
  margin-top: 0.15rem;
}
.nums .dim {
  opacity: 0.6;
}
.nums :deep(b) {
  color: var(--ink);
}
.nums :deep(.rg) {
  color: var(--muted);
}
.hn {
  font-family: var(--font-pixel);
  font-weight: 400;
  color: var(--naruto) !important;
  margin-right: 0.15rem;
}
.nums :deep(.g),
.g {
  font-style: normal;
  font-size: 0.6rem;
  color: var(--muted);
}
.rev {
  font-size: 0.64rem;
  color: var(--ink-2);
  margin-top: 0.1rem;
}
</style>
