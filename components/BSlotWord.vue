<script setup lang="ts">
// Chapter 7: what the port did with F8 on a full object pool between 30 September 15:30 and 1 October 10:45.
// The requested-items pass then takes its slot from the gameplay body's frame word SP+34. The lane shows the
// port's policy for that case over time (boundary → declared skip → boundary again → model) with the events
// that switched it; hover a mark to single it out. The quiet night (01:30–05:30) is cut out of the axis and
// marked by a break. Times are local (UTC+2): git author times, and the Claude Code log 7ea5b99f for the
// question (22:53:59Z) and the author's reply (03:56:25Z).
import { ref } from 'vue'

const at = (mo: number, d: number, h: number, m: number) => Date.UTC(2026, mo - 1, d, h, m)
const t0 = at(9, 30, 15, 30)
const aEnd = at(10, 1, 1, 30)
const bStart = at(10, 1, 5, 30)
const t1 = at(10, 1, 10, 45)
const W = 884
const L = 10
const GAP = 22
const p = (W - 2 * L - GAP) / ((aEnd - t0) + (t1 - bStart))
const x = (t: number) => t <= aEnd ? L + (t - t0) * p : L + (aEnd - t0) * p + GAP + (Math.max(t, bStart) - bStart) * p
const breakX = L + (aEnd - t0) * p

interface Piece { from: number, to: number, kind: 'stop' | 'skip' | 'model', label?: string }
const pieces: Piece[] = [
  { from: t0, to: at(9, 30, 16, 53), kind: 'stop' },
  { from: at(9, 30, 16, 53), to: at(9, 30, 23, 3), kind: 'skip', label: 'пропуск предмета — отход от поведения EXE' },
  { from: at(9, 30, 23, 3), to: aEnd, kind: 'stop', label: 'снова граница' },
  { from: bStart, to: at(10, 1, 9, 8), kind: 'stop', label: 'граница' },
  { from: at(10, 1, 9, 8), to: t1, kind: 'model', label: 'модель' },
]

interface Mark { t: number, time: string, hash?: string, who: 'agent' | 'review' | 'human' | 'run', title: string, up: boolean, end?: boolean }
const marks: Mark[] = [
  { t: at(9, 30, 16, 9), time: '16:09', hash: 'd8481cb', who: 'agent', title: 'War: пропуск предмета', up: true },
  { t: at(9, 30, 16, 53), time: '16:53', hash: 'd26e412', who: 'agent', title: 'F8: тоже пропуск', up: false },
  { t: at(9, 30, 23, 3), time: '23:03', hash: '698f76a', who: 'review', title: 'ревью: «not unknown»', up: true },
  { t: at(10, 1, 0, 53), time: '00:53', who: 'agent', title: 'вопрос автору', up: false },
  { t: at(10, 1, 5, 56), time: '05:56', who: 'human', title: 'автор: обязательно', up: true },
  { t: at(10, 1, 9, 8), time: '09:08', hash: 'f4cdcbb', who: 'agent', title: 'модель слова SP+34', up: false, end: true },
  { t: at(10, 1, 10, 16), time: '10:16', hash: '8d107f1', who: 'run', title: '88 нажатий → слот 0', up: true, end: true },
]
const ticks = [
  ...[16, 18, 20, 22].map(h => ({ t: at(9, 30, h, 0), label: `${h}:00` })),
  { t: at(10, 1, 0, 0), label: '00:00' },
  ...[6, 8, 10].map(h => ({ t: at(10, 1, h, 0), label: `0${h}:00`.slice(-5) })),
]
const midnight = x(at(10, 1, 0, 0))
const laneY = 62
const hover = ref<number | null>(null)
</script>

<template>
  <div class="sw">
    <svg :viewBox="`0 0 ${W} 128`" width="100%" role="img" aria-label="Политика порта для F8 на полном пуле: граница, пропуск с 16:53, снова граница после ревью в 23:03, модель с 09:08 1 октября">
      <line :x1="midnight" :x2="midnight" y1="4" y2="112" class="mid" />
      <text :x="L" y="9" class="day">30 сентября</text>
      <text :x="midnight + 4" y="9" class="day">1 октября</text>
      <g v-for="(s, i) in pieces" :key="i">
        <rect :x="x(s.from)" :y="laneY - 9" :width="Math.max(0, x(s.to) - x(s.from))" height="18" :class="['seg', s.kind]" />
        <text v-if="s.label && x(s.to) - x(s.from) > 60" :x="(x(s.from) + x(s.to)) / 2" :y="laneY + 3.5" text-anchor="middle" :class="['sl', s.kind]">{{ s.label }}</text>
      </g>
      <g class="brk">
        <rect :x="breakX + 2" :y="laneY - 14" :width="GAP - 4" height="28" class="brkbg" />
        <path :d="`M${breakX + 4},${laneY + 13} l6,-26 M${breakX + GAP - 10},${laneY + 13} l6,-26`" />
        <text :x="breakX + GAP / 2" :y="laneY + 26" text-anchor="middle" class="brkt">ночь</text>
      </g>
      <g v-for="(m, i) in marks" :key="`m${i}`" class="mk" :class="{ dim: hover !== null && hover !== i }" @mouseenter="hover = i" @mouseleave="hover = null">
        <line :x1="x(m.t)" :x2="x(m.t)" :y1="m.up ? 28 : laneY + 9" :y2="m.up ? laneY - 9 : 96" :class="['stem', m.who]" />
        <circle :cx="x(m.t)" :cy="m.up ? 28 : 96" r="3.6" :class="['dot', m.who]" />
        <text :x="x(m.t) + (m.end ? -6 : 6)" :y="m.up ? 21 : 100" :text-anchor="m.end ? 'end' : 'start'" class="ml">
          <tspan class="mt">{{ m.time }}</tspan><tspan v-if="m.hash" class="mh" dx="5">{{ m.hash }}</tspan>
        </text>
        <text :x="x(m.t) + (m.end ? -6 : 6)" :y="m.up ? 32 : 111" :text-anchor="m.end ? 'end' : 'start'" class="mtt">{{ m.title }}</text>
      </g>
      <text v-for="(tk, i) in ticks" :key="`t${i}`" :x="x(tk.t)" y="125" text-anchor="middle" class="tk">{{ tk.label }}</text>
    </svg>
  </div>
</template>

<style scoped>
.sw { width: 100%; }
.mid { stroke: var(--axis); stroke-dasharray: 2 3; }
.day { font-size: 9.5px; fill: var(--muted); font-family: var(--font-sans); }
.seg.stop { fill: rgba(141, 145, 156, 0.2); stroke: var(--axis); }
.seg.skip { fill: rgba(250, 178, 25, 0.26); stroke: var(--warning); }
.seg.model { fill: rgba(12, 163, 12, 0.3); stroke: var(--good); }
.sl { font-size: 10px; font-family: var(--font-sans); font-weight: 600; fill: var(--ink-2); }
.sl.skip { fill: #ffd27a; }
.sl.model { fill: #b9f0b9; }
.brkbg { fill: var(--bg); }
.brk path { stroke: var(--muted); stroke-width: 1.3; fill: none; }
.brkt { font-size: 8.5px; fill: var(--muted); font-family: var(--font-sans); }
.stem { stroke-width: 1.2; stroke: var(--axis); }
.stem.review { stroke: var(--chakra); }
.stem.human { stroke: var(--s1); }
.stem.run { stroke: var(--naruto); }
.dot { fill: var(--surface-3); stroke: var(--ink-2); stroke-width: 1.3; }
.dot.review { fill: var(--chakra); stroke: var(--chakra); }
.dot.human { fill: var(--s1); stroke: var(--s1); }
.dot.run { fill: var(--naruto); stroke: var(--naruto); }
.ml { font-size: 10px; font-family: var(--font-mono); }
.mt { fill: var(--ink); }
.mh { fill: var(--muted); font-size: 9px; }
.mtt { font-size: 9.8px; fill: var(--ink-2); font-family: var(--font-sans); }
.tk { font-size: 8.5px; fill: var(--muted); font-family: var(--font-mono); }
.mk { transition: opacity 0.2s; cursor: default; }
.mk.dim { opacity: 0.3; }
</style>
