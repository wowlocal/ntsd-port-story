<script setup lang="ts">
import { computed, ref } from 'vue'
import { useNav } from '@slidev/client'
import ep from '../data/epilogue.json'
import loop from '../data/loop.json'

// One Claude Code session (1f9218ae), 3 Oct 20:08 → 13 Oct 21:15, on one axis: the context of the
// main-thread requests (every 3rd request plus the peaks), the automatic compactions, and three rugs —
// commits (coloured by chapter), /loop firings and the human's turns. Hover a chapter band to see it alone.
const s = (ep as any).session
const nav = useNav()
const W = 884
const x0 = 96
const x1 = W - 6
const H = s.totals.hours as number
const X = (h: number) => x0 + (h / H) * (x1 - x0)
const top = 26
const cH = 112
const Y = (k: number) => top + cH - (k / 1000) * cH
const pts = s.points as number[][]
// a step line: the context holds until the next request, so idle gaps stay flat and compactions drop straight down
const line = pts.map((p, i) => (i ? `H${X(p[0]).toFixed(1)}V${Y(p[1]).toFixed(1)}` : `M${X(p[0]).toFixed(1)},${Y(p[1]).toFixed(1)}`)).join('')
const area = `${line}L${X(pts[pts.length - 1][0]).toFixed(1)},${Y(0)}L${X(0)},${Y(0)}Z`
const rug = { commits: top + cH + 22, loop: top + cH + 40, human: top + cH + 58 }
const bottom = rug.human + 12

// local hours since the session start (3 Oct 20:08:25)
const startMs = Date.parse(s.start)
const at = (iso: string) => (Date.parse(`${iso}:00+02:00`) - startMs) / 36e5
const chapters = [
  { n: 13, name: 'девять хостов', from: 0, to: at('2026-10-05T07:26') },
  { n: 14, name: 'телефон', from: at('2026-10-05T07:26'), to: at('2026-10-07T08:23') },
  { n: 15, name: '16 мс', from: at('2026-10-07T08:23'), to: at('2026-10-10T21:23') },
  { n: 16, name: 'загрузка', from: at('2026-10-10T21:23'), to: at('2026-10-11T20:02') },
  { n: 17, name: 'ТВ и браузер', from: at('2026-10-11T20:02'), to: at('2026-10-13T06:36') },
  { n: 18, name: 'релиз', from: at('2026-10-13T06:36'), to: H },
]
const chColor = ['rgba(57,135,229,0.16)', 'rgba(217,89,38,0.16)']
// commits: 3–7 Oct from data/loop.json (minutes), 7–13 Oct from data/epilogue.json (hours)
const early = ((loop as any).commits as { t: number }[]).map(c => c.t / 60)
const late = (s.commits as { h: number }[]).map(c => c.h)
const commits = [...early, ...late]
const chapterOf = (h: number) => chapters.find(c => h >= c.from && h < c.to)?.n ?? 18
const hover = ref<number | null>(null)
const lit = (h: number) => hover.value === null || nav.isPrintMode.value || chapterOf(h) === hover.value
const days = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13].map(d => ({ h: at(`2026-10-${String(d).padStart(2, '0')}T00:00`), label: d === 4 ? '4 окт' : `${d}` }))
const ticks = [0, 500, 1000]
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${bottom + 20}`" width="100%" role="img" aria-label="Десять дней одной сессии агента">
    <g v-for="(c, i) in chapters" :key="c.n" class="band" @mouseenter="hover = c.n" @mouseleave="hover = null">
      <rect :x="X(c.from)" y="2" :width="X(c.to) - X(c.from) - 1.5" height="16" rx="3" :fill="chColor[i % 2]" :style="{ opacity: hover === null || hover === c.n ? 1 : 0.35 }" />
      <text class="chn" :x="X(c.from) + 5" y="13.5">{{ c.n }} · {{ c.name }}</text>
      <rect :x="X(c.from)" :y="top" :width="X(c.to) - X(c.from)" :height="bottom - top" fill="transparent" />
    </g>
    <line v-for="v in ticks" :key="v" :x1="x0" :x2="x1" :y1="Y(v)" :y2="Y(v)" :stroke="v === 0 ? 'var(--axis)' : 'var(--grid)'" />
    <text v-for="v in ticks" :key="`t${v}`" class="tick" :x="x0 - 8" :y="Y(v) + 3.5" text-anchor="end">{{ v === 0 ? '0' : v === 1000 ? '1 млн' : '500 тыс.' }}</text>
    <text class="lbl" :x="x0 - 8" :y="top - 4" text-anchor="end">контекст</text>
    <path :d="area" fill="var(--s2)" style="opacity: 0.1; pointer-events: none" />
    <path :d="line" fill="none" stroke="var(--s2)" stroke-width="1" stroke-linejoin="round" style="pointer-events: none" />
    <circle v-for="(c, i) in s.compactions" :key="`k${i}`" :cx="X(c.h)" :cy="Y(c.pre_k)" r="3" fill="var(--ink)" stroke="var(--bg)" stroke-width="1.2">
      <title>сжатие контекста: {{ c.pre_k }} тыс. → {{ c.post_k }} тыс. токенов</title>
    </circle>

    <text class="lbl" :x="x0 - 8" :y="rug.commits + 3.5" text-anchor="end">коммиты</text>
    <line v-for="(h, i) in commits" :key="`c${i}`" :x1="X(h)" :x2="X(h)" :y1="rug.commits - 6" :y2="rug.commits + 6" stroke="var(--s2)" stroke-width="1.1" :style="{ opacity: lit(h) ? 1 : 0.15 }" />
    <text class="lbl" :x="x0 - 8" :y="rug.loop + 3.5" text-anchor="end">/loop</text>
    <line v-for="(h, i) in s.wakeups" :key="`w${i}`" :x1="X(h)" :x2="X(h)" :y1="rug.loop - 5" :y2="rug.loop + 5" stroke="var(--ink-2)" stroke-width="1" :style="{ opacity: lit(h) ? 1 : 0.15 }" />
    <text class="lbl hum" :x="x0 - 8" :y="rug.human + 3.5" text-anchor="end">человек</text>
    <circle v-for="(h, i) in s.human" :key="`h${i}`" :cx="X(Math.max(0, h))" :cy="rug.human" r="3.2" fill="var(--s1)" stroke="var(--bg)" stroke-width="1" :style="{ opacity: lit(h) ? 1 : 0.15 }" />

    <g v-for="d in days" :key="d.label">
      <line :x1="X(d.h)" :x2="X(d.h)" :y1="top" :y2="bottom" stroke="var(--axis)" stroke-dasharray="2 3" style="opacity: 0.6" />
      <text class="day" :x="X(d.h) + 3" :y="bottom + 13">{{ d.label }}</text>
    </g>

  </svg>
</template>

<style scoped>
.tick {
  font-family: var(--font-sans);
  font-size: 9.5px;
  fill: var(--muted);
}
.lbl {
  font-family: var(--font-sans);
  font-size: 10.5px;
  font-weight: 600;
  fill: var(--ink-2);
}
.lbl.hum {
  fill: var(--chakra);
}
.chn {
  font-family: var(--font-sans);
  font-size: 9.5px;
  font-weight: 600;
  fill: var(--ink);
  pointer-events: none;
}
.band {
  cursor: default;
}
.day {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--ink-2);
}
</style>
