<script setup lang="ts">
import { computed, ref } from 'vue'
import data from '../data/web_steps.json'

// The chapter's 29 commits (a16fe0d2 … f0471f13, 11 Oct 20:12 → 13 Oct 06:21), one lane per study:
// Apple TV (TVOS_WEB T*), the browser (TVOS_WEB W*) and the scalable window (WINDOW_SCALING S*).
// Card-only commits sit on the axis. The author's turns are times only (session 1f9218ae, UTC+2).
// Hover a dot: the commit's time, hash and subject. Data: data/web_steps.json (scripts/collect_web.py).
interface Step { hash: string, time: string, subject: string, step: string | null, lane: string }
const steps = (data as any).steps as Step[]

const W = 884
const x0 = 92
const x1 = W - 8
const HOURS = 35 // 11 Oct 20:00 → 13 Oct 07:00
const px = (x1 - x0) / HOURS
const hourOf = (iso: string) => {
  const d = Number(iso.slice(8, 10)) - 11
  return (d * 1440 + Number(iso.slice(11, 13)) * 60 + Number(iso.slice(14, 16)) - 20 * 60) / 60
}
const X = (h: number) => x0 + h * px

const lanes = [
  { key: 'human', name: 'автор' },
  { key: 'tvos', name: 'Apple TV', color: 'var(--s1)' },
  { key: 'web', name: 'браузер', color: 'var(--s2)' },
  { key: 'window', name: 'окно', color: 'var(--s3)' },
]
const LH = 22
const top = 26
const laneY = (k: string) => top + lanes.findIndex(l => l.key === k) * LH + LH / 2
const axisY = top + lanes.length * LH + 4
const H = axisY + 24

// the author's typed turns, local time (session log; /loop re-invocations and pasted images excluded)
const human = ['11T20:00', '11T20:02', '11T20:46', '11T20:48', '11T20:53', '11T21:29', '12T07:03', '12T07:15', '12T12:12', '12T17:36', '12T17:38', '12T21:50', '12T21:50', '13T04:07', '13T05:35', '13T05:37', '13T05:37', '13T05:40']
  .map(s => hourOf(`2026-10-${s.slice(0, 2)}T${s.slice(3)}`))
const notes = [
  { h: hourOf('2026-10-11T20:02'), text: 'задача', anchor: 'start' },
  { h: hourOf('2026-10-12T12:12'), text: '«можно потестить в браузере самому?»', anchor: 'middle' },
  { h: hourOf('2026-10-12T21:50'), text: 'окно и полный экран', anchor: 'middle' },
  { h: hourOf('2026-10-13T05:37'), text: '«где шрифты?»', anchor: 'end' },
]
const nights = [[4, 11], [28, 35]]
const ticks = Array.from({ length: 12 }, (_, i) => i * 3 + 1).filter(h => h <= HOURS)
const clock = (h: number) => (h === 4 ? '12 окт' : h === 28 ? '13 окт' : String((20 + h) % 24).padStart(2, '0'))

const dots = computed(() => steps.map(s => ({ ...s, x: X(hourOf(s.time)), y: s.lane === 'card' ? axisY : laneY(s.lane) })))
const count = (k: string) => steps.filter(s => s.lane === k).length

const tip = ref<{ x: number, y: number, s: Step } | null>(null)
const wrap = ref<HTMLElement | null>(null)
function show(e: PointerEvent | FocusEvent, s: Step & { x: number, y: number }) {
  tip.value = { x: s.x, y: s.y, s }
}
const fmtTime = (iso: string) => `${Number(iso.slice(8, 10))} окт, ${iso.slice(11, 16)}`
</script>

<template>
  <div ref="wrap" class="strip">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`${steps.length} коммитов за 34 часа по трём дорожкам`" @pointerleave="tip = null">
      <rect v-for="(n, i) in nights" :key="`n${i}`" :x="X(n[0])" :y="top" :width="(n[1] - n[0]) * px" :height="axisY - top" fill="rgba(57,135,229,0.06)" />
      <text v-for="(n, i) in nights" :key="`nt${i}`" class="band" :x="X(n[0]) + 4" :y="top + 10">ночь</text>

      <g v-for="l in lanes" :key="l.key">
        <line :x1="x0" :x2="x1" :y1="laneY(l.key)" :y2="laneY(l.key)" stroke="var(--grid)" />
        <circle v-if="l.color" :cx="8" :cy="laneY(l.key)" r="4" :fill="l.color" />
        <text class="lane" :x="l.color ? 17 : 0" :y="laneY(l.key) + 3.5">{{ l.name }}<tspan v-if="l.color" class="cnt"> · {{ count(l.key) }}</tspan></text>
      </g>

      <!-- the author's turns -->
      <rect v-for="(h, i) in human" :key="`h${i}`" :x="X(h) - 1.5" :y="laneY('human') - 5" width="3" height="10" rx="1" fill="var(--chakra)" style="opacity: 0.85" />
      <g v-for="n in notes" :key="n.text">
        <text class="note" :x="X(n.h) + (n.anchor === 'start' ? -2 : 0)" :y="top - 9" :text-anchor="n.anchor">{{ n.text }}</text>
        <line :x1="X(n.h)" :x2="X(n.h)" :y1="top - 6" :y2="laneY('human') - 6" stroke="var(--axis)" />
      </g>

      <!-- axis -->
      <line :x1="x0" :x2="x1" :y1="axisY" :y2="axisY" stroke="var(--axis)" />
      <g v-for="t in ticks" :key="t">
        <line :x1="X(t)" :x2="X(t)" :y1="axisY" :y2="axisY + 4" stroke="var(--axis)" />
        <text class="tick" :class="{ day: t === 4 || t === 28 }" :x="X(t)" :y="axisY + 15" text-anchor="middle">{{ clock(t) }}</text>
      </g>
      <text class="day" :x="x0 - 6" :y="axisY + 15" text-anchor="end">11 окт</text>

      <!-- commits -->
      <g v-for="d in dots" :key="d.hash" tabindex="0" class="hit" @pointerenter="show($event, d)" @focus="show($event, d)" @blur="tip = null">
        <circle :cx="d.x" :cy="d.y" r="9" fill="transparent" />
        <rect v-if="d.lane === 'card'" :x="d.x - 3.5" :y="d.y - 3.5" width="7" height="7" fill="var(--bg)" stroke="var(--ink-2)" stroke-width="1.4" />
        <circle v-else :cx="d.x" :cy="d.y" r="4" :fill="lanes.find(l => l.key === d.lane)!.color" stroke="var(--bg)" stroke-width="1.5" />
      </g>
      <circle v-if="tip" :cx="tip.x" :cy="tip.y" r="7" fill="none" stroke="var(--ink)" stroke-width="1.5" pointer-events="none" />
    </svg>
    <div v-if="tip" class="tip" :style="{ left: `${(tip.x / W) * 100}%`, top: `${(tip.y / H) * 100}%`, transform: `translate(${tip.x > W * 0.7 ? '-100%' : tip.x < W * 0.25 ? '0' : '-50%'}, -115%)` }">
      <div class="tv">
        <b>{{ tip.s.step ?? 'карточка' }}</b> · {{ fmtTime(tip.s.time) }} · <span class="mono">{{ tip.s.hash }}</span>
      </div>
      <div class="ts" lang="en">
        {{ tip.s.subject }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.strip {
  position: relative;
}
.lane {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--ink-2);
}
.cnt {
  fill: var(--muted);
}
.band {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
}
.note {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--ink-2);
}
.tick,
.day {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.day {
  fill: var(--ink-2);
  font-weight: 600;
}
.hit {
  cursor: pointer;
  outline: none;
}
.tip {
  position: absolute;
  pointer-events: none;
  background: #0c1017;
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 8px;
  padding: 0.3rem 0.55rem;
  max-width: 300px;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.5);
  z-index: 5;
}
.tv {
  font-size: 0.66rem;
  color: var(--ink-2);
  white-space: nowrap;
}
.tv b {
  color: var(--ink);
}
.ts {
  font-size: 0.66rem;
  color: var(--ink);
  line-height: 1.3;
  margin-top: 0.1rem;
}
</style>
