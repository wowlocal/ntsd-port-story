<script setup lang="ts">
import { computed, ref } from 'vue'
import { useNav } from '@slidev/client'
import data from '../data/epilogue.json'

// The week after the freeze (7 Oct 08:23 → 13 Oct 20:14): every commit as a dot in its topic's lane
// (scripts/collect_epilogue.py), and the human's turns on top. Click a blue dot to read that turn;
// click a topic name to highlight its lane. Export shows the turn of 10 Oct 21:23.
interface C { hash: string, time: string, subject: string, topic: string, claude: boolean }
const week = (data as any).week as C[]
const nav = useNav()

const lanes = [
  { key: 'realtime', name: 'ядро · 16 мс', ch: 15, color: 'var(--s2)' },
  { key: 'memory', name: 'память и загрузка', ch: 16, color: 'var(--s1)' },
  { key: 'web', name: 'ТВ и браузер', ch: 17, color: 'var(--s3)' },
  { key: 'window', name: 'масштаб окна', ch: 17, color: 'var(--s7)' },
  { key: 'menu', name: 'утечка в меню', ch: 18, color: 'var(--s5)' },
  { key: 'controller', name: 'джойстик, iPhone', ch: 18, color: 'var(--s4)' },
  { key: 'release', name: 'релиз', ch: 18, color: 'var(--ink-2)' },
]
// the human's directives, verbatim from the session log 1f9218ae (local time, UTC+2)
const turns = [
  { t: '2026-10-07T14:50', q: 'я чутка попользовался телефоном во время прогона, поднял яркость. можешь вернуть яркость на 0?' },
  { t: '2026-10-08T07:21', q: 'when you get to 60fps on a phone put a tag on a branch pls' },
  { t: '2026-10-08T07:28', q: 'and we should also test DEMO game with a lot of going on, not just two chars figting' },
  { t: '2026-10-09T10:52', q: 'я поставил windows через vmpal. если тебе полезно будет можешь использовать' },
  { t: '2026-10-10T21:23', q: 'you did good. we reached the wall. performance is now close to optimal. now lets do the loop for optimizing  memory footprint and loading times.' },
  { t: '2026-10-11T14:14', q: 'we must not compromise on performance (loading speed and frame time) while we optimize memory footprint btw' },
  { t: '2026-10-11T14:20', q: 'suspicious of b8d1c9b2… commit. i might be wrong but feels like we added cpu overhead' },
  { t: '2026-10-11T19:09', q: '0.5ms на слабом телефоне или это 0.5 на mac mini?' },
  { t: '2026-10-11T20:02', q: 'теперь изучи как ты делал кросскомпиляцию игры… запустил loop с сборкой поддержки apple tv и web (вроде как swift умеет компилироваться в wasm)' },
  { t: '2026-10-12T17:36', q: 'хромиум wasm быстрее чем нативная mac версия?' },
  { t: '2026-10-12T21:50', q: 'отведи отдельную ветку где поработай над тем чтобы мы могли скейлить окно игры… запуск в оригинальном формате оставь под флагом' },
  { t: '2026-10-13T05:37', q: 'ну что задеплоим web версию?' },
  { t: '2026-10-13T06:36', q: 'вот джойстик для мобильных телефонов (погугли что за девайс)… и в ios и в android' },
  { t: '2026-10-13T18:58', q: 'все работает' },
]

const W = 884
const x0 = 132
const x1 = W - 6
const T0 = Date.parse('2026-10-07T08:00:00+02:00')
const T1 = Date.parse('2026-10-13T22:00:00+02:00')
const X = (iso: string) => x0 + ((Date.parse(`${iso}:00+02:00`) - T0) / (T1 - T0)) * (x1 - x0)
const LH = 24
const top = 40
const laneY = (i: number) => top + 30 + i * LH + LH / 2
const bottom = top + 30 + lanes.length * LH
const count = (k: string) => week.filter(c => c.topic === k).length
const days = Array.from({ length: 7 }, (_, i) => ({ iso: `2026-10-${String(8 + i).padStart(2, '0')}T00:00`, label: `${8 + i} окт` }))
  .filter(d => Date.parse(`${d.iso}:00+02:00`) < T1)
const nights = [...Array.from({ length: 7 }, (_, i) => [`2026-10-${String(8 + i).padStart(2, '0')}T00:00`, `2026-10-${String(8 + i).padStart(2, '0')}T06:00`])]
  .filter(n => Date.parse(`${n[0]}:00+02:00`) < T1)

const picked = ref(4)
const focus = ref<string | null>(null)
const shownTurn = computed(() => (nav.isPrintMode.value ? turns[4] : turns[picked.value]))
const dim = (k: string) => focus.value !== null && focus.value !== k
const fmt = (iso: string) => `${Number(iso.slice(8, 10))} окт, ${iso.slice(11, 16)}`
</script>

<template>
  <div class="wl">
    <svg :viewBox="`0 0 ${W} ${bottom + 22}`" width="100%" role="img" aria-label="Неделя после 7 октября: коммиты по темам и реплики человека">
      <rect v-for="(n, i) in nights" :key="`n${i}`" :x="X(n[0])" :y="top" :width="X(n[1]) - X(n[0])" :height="bottom - top" fill="rgba(57,135,229,0.06)" />
      <!-- human lane -->
      <text class="lane hum" :x="x0 - 10" :y="top + 14" text-anchor="end">человек</text>
      <line :x1="x0" :x2="x1" :y1="top + 10" :y2="top + 10" stroke="var(--grid)" />
      <g v-for="(t, i) in turns" :key="t.t" class="turn" :class="{ on: i === picked }" @click="picked = i">
        <circle :cx="X(t.t)" :cy="top + 10" r="9" fill="transparent" />
        <circle :cx="X(t.t)" :cy="top + 10" :r="i === picked ? 6 : 4.5" fill="var(--s1)" stroke="var(--bg)" stroke-width="1.5" />
        <title>{{ fmt(t.t) }} · {{ t.q }}</title>
      </g>
      <line :x1="X(shownTurn.t)" :x2="X(shownTurn.t)" :y1="top + 17" :y2="bottom" stroke="var(--s1)" stroke-dasharray="2 3" style="opacity: 0.7" />

      <!-- topic lanes -->
      <g v-for="(l, i) in lanes" :key="l.key" :style="{ opacity: dim(l.key) ? 0.25 : 1 }">
        <line :x1="x0" :x2="x1" :y1="laneY(i)" :y2="laneY(i)" stroke="var(--grid)" />
        <g class="lname" @click="focus = focus === l.key ? null : l.key">
          <rect :x="0" :y="laneY(i) - 10" :width="x0 - 4" height="20" fill="transparent" />
          <text class="lane" :x="x0 - 10" :y="laneY(i) + 3.5" text-anchor="end">{{ l.name }}<tspan class="cnt" dx="5">{{ count(l.key) }}</tspan></text>
        </g>
        <g v-for="c in week.filter(c => c.topic === l.key)" :key="c.hash">
          <circle :cx="X(c.time)" :cy="laneY(i)" r="3.6" :fill="l.color" stroke="var(--bg)" stroke-width="1.2">
            <title>{{ fmt(c.time) }} · {{ c.hash }} · {{ c.subject }}{{ c.claude ? '' : ' · без трейлера Claude' }}</title>
          </circle>
        </g>
      </g>

      <!-- days -->
      <line :x1="x0" :x2="x1" :y1="bottom" :y2="bottom" stroke="var(--axis)" />
      <g v-for="d in days" :key="d.iso">
        <line :x1="X(d.iso)" :x2="X(d.iso)" :y1="top" :y2="bottom + 4" stroke="var(--axis)" stroke-dasharray="2 3" />
        <text class="day" :x="X(d.iso) + 4" :y="bottom + 16">{{ d.label }}</text>
      </g>
      <text class="day" :x="x0" :y="bottom + 16">7 окт</text>
    </svg>
    <div class="quote">
      <span class="when mono">{{ fmt(shownTurn.t) }}</span>
      <span class="q">«{{ shownTurn.q }}»</span>
    </div>
  </div>
</template>

<style scoped>
.lane {
  font-family: var(--font-sans);
  font-size: 11px;
  font-weight: 600;
  fill: var(--ink);
}
.lane.hum {
  fill: var(--chakra);
}
.cnt {
  font-weight: 400;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.lname,
.turn {
  cursor: pointer;
}
.day {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--ink-2);
}
.quote {
  display: flex;
  gap: 0.7rem;
  align-items: baseline;
  margin-top: 0.3rem;
  padding: 0.45rem 0.75rem;
  border-radius: 10px;
  background: rgba(57, 135, 229, 0.12);
  border: 1px solid rgba(57, 135, 229, 0.4);
  min-height: 2.4rem;
}
.quote .when {
  font-size: 0.66rem;
  color: var(--chakra);
  white-space: nowrap;
}
.quote .q {
  font-size: 0.78rem;
  color: var(--ink);
  line-height: 1.35;
}
</style>
