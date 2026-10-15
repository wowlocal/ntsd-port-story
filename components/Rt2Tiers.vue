<script setup lang="ts">
// Chapter 15: the author's tiers against each thread's compute per tick at the end of the chapter (e5, 10 Oct), with
// the start as a faint bar (vs: 4l, where chapter 14 stopped; the Demo: its first runs, P4g's build on 8 Oct). Pick a
// tier: the budget line moves, each bar says whether it fits, and the row below says on which step it was first met.
// Presenter and release are threads that did not exist at the start: their work was inside the render and main
// threads then. Export shows the 16 ms tier.
// Data: data/rt2_steps.json (tiers, steps 4z and e5), data/rt2_threads.json (start, end).
import { computed, onMounted, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'
import steps from '../data/rt2_steps.json'
import threads from '../data/rt2_threads.json'

const nav = useNav()
const active = useIsSlideActive()
const S = steps as any
const T = threads as any
const z = S.steps.find((s: any) => s.id === '4z')
const tiers = [
  { ms: 33, key: '33', name: '33 мс', sub: 'ярус 1' },
  { ms: 16.67, key: '60fps', name: '16,67', sub: '60 fps' },
  { ms: 16, key: '16', name: '16 мс', sub: 'ярус 2' },
  { ms: 8, key: '8', name: '8 мс', sub: 'ярус 3 · цель' },
]
const sel = ref(2)
const tier = computed(() => tiers[sel.value])
const f2 = (v: number) => v.toFixed(2).replace('.', ',')
const f1 = (v: number) => v.toFixed(1).replace('.', ',')
const day = (t: string) => `${Number(t.slice(3, 5))} окт ${t.slice(6)}`

const blocks = [
  {
    key: 'vs', name: 'vs · два бойца', startName: 'старт главы, 4l',
    rows: [
      { k: 'main', name: 'главный', color: 'var(--s2)', now: T.end.vs.main, was: T.start.main },
      { k: 'render', name: 'рендер', color: 'var(--s1)', now: T.end.vs.render, was: T.start.render },
      { k: 'present', name: 'presenter', color: 'var(--s3)', now: T.end.vs.present, was: null },
      { k: 'release', name: 'release', color: 'var(--s4)', now: T.end.vs.release, was: null },
    ],
  },
  {
    key: 'demo', name: 'Demo · восемь бойцов', startName: 'первый замер Demo, 8 окт',
    rows: [
      { k: 'main', name: 'главный', color: 'var(--s2)', now: T.end.demo.main, was: z.demo.base.main },
      { k: 'render', name: 'рендер', color: 'var(--s1)', now: T.end.demo.render, was: z.demo.base.render },
      { k: 'present', name: 'presenter', color: 'var(--s3)', now: T.end.demo.present, was: null },
      { k: 'release', name: 'release', color: 'var(--s4)', now: T.end.demo.release, was: null },
    ],
  },
]
const W = 432
const RH = 48
const H = 4 * RH + 26
const L = 66
const R = W - 70
const MAX = 34
const x = (ms: number) => L + (ms / MAX) * (R - L)

const grow = ref(1)
function play() {
  if (nav.isPrintMode.value) {
    grow.value = 1
    return
  }
  grow.value = 0
  setTimeout(() => {
    grow.value = 1
  }, 60)
}
onMounted(() => {
  if (active.value)
    play()
})
watch(active, (v) => {
  if (v)
    play()
})

function crossing(block: string, k: string) {
  if (tier.value.key === '33')
    return { ok: true, text: 'ещё 6 окт, 4f (глава 14)' }
  const c = S.tiers[tier.value.key]?.[`${block}_${k}`]
  if (!c)
    return { ok: false, text: 'не пройден' }
  if (block === 'demo' && c.id === '4z')
    return { ok: true, text: 'с первого замера' }
  return { ok: true, text: `${c.id}, ${day(c.time)} · ${f2(c.value)}` }
}
const sumStart = T.start.main + T.start.render
const sumEnd = T.end.vs.main + T.end.vs.render + T.end.vs.present + T.end.vs.release
</script>

<template>
  <div class="tiers">
    <div class="pick">
      <span class="pick-label">бюджет на тик:</span>
      <button v-for="(t, i) in tiers" :key="t.key" class="tb" :class="{ on: sel === i }" @click="sel = i">
        <b>{{ t.name }}</b> <span>{{ t.sub }}</span>
      </button>
    </div>
    <div class="blocks">
      <div v-for="b in blocks" :key="b.key" class="blk">
        <div class="bh">
          {{ b.name }} <span class="bs">· бледная полоса — {{ b.startName }}</span>
        </div>
        <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`${b.name}: работа на тик по потокам против бюджета ${tier.name}`">
          <g v-for="t in [0, 10, 20, 30]" :key="t">
            <line :x1="x(t)" :x2="x(t)" y1="4" :y2="H - 16" stroke="var(--grid)" />
            <text :x="x(t)" :y="H - 4" text-anchor="middle" class="tick">{{ t }}{{ t === 30 ? ' мс' : '' }}</text>
          </g>
          <g v-for="(r, i) in b.rows" :key="r.k">
            <rect v-if="r.was" :x="x(0)" :y="i * RH + 6" :style="{ width: `${(x(r.was) - x(0)) * grow}px` }" height="32" rx="3" :fill="r.color" style="opacity: 0.2" class="bar" />
            <rect :x="x(0)" :y="i * RH + 6" :style="{ width: `${(x(r.now) - x(0)) * grow}px` }" height="32" rx="3" :fill="r.color" class="bar" />
          </g>
          <!-- the budget line sits over the bars and under the labels -->
          <line x1="0" x2="0" y1="0" :y2="H - 14" stroke="var(--ink)" stroke-width="1.6" class="tl" :style="{ transform: `translateX(${x(tier.ms)}px)` }" />
          <g v-for="(r, i) in b.rows" :key="`t${r.k}`">
            <text x="0" :y="i * RH + 27" class="lab">{{ r.name }}</text>
            <text :x="x(r.now) + 5" :y="i * RH + 27" class="val halo">{{ f2(r.now) }}</text>
            <text v-if="r.was" :x="x(r.was) + 5" :y="i * RH + 27" class="was halo">{{ f1(r.was) }}</text>
            <text :x="W" :y="i * RH + 27" text-anchor="end" class="fit" :class="{ over: r.now > tier.ms }">{{ r.now <= tier.ms ? '✓ в бюджете' : `+${f2(r.now - tier.ms)} мс` }}</text>
          </g>
        </svg>
        <div class="cr">
          <span v-for="k in ['main', 'render']" :key="k" :class="{ no: !crossing(b.key, k).ok }">
            <i class="key" :style="{ background: k === 'main' ? 'var(--s2)' : 'var(--s1)' }" />{{ crossing(b.key, k).text }}
          </span>
        </div>
      </div>
    </div>
    <div class="sum">
      Все потоки вместе, vs: <b>{{ f1(sumStart) }} → {{ f1(sumEnd) }} мс</b> работы процессора на тик. Это не время кадра — потоки идут параллельно на разных ядрах; но и не ноль: presenter и release сняли нагрузку с главного и рендера, а не уничтожили её.
    </div>
  </div>
</template>

<style scoped>
.pick {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin-bottom: 0.35rem;
}
.pick-label {
  font-size: 0.66rem;
  color: var(--muted);
  margin-right: 0.2rem;
}
.tb {
  font-family: var(--font-sans);
  font-size: 0.66rem;
  color: var(--ink-2);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--hair);
  border-radius: 999px;
  padding: 0.14rem 0.65rem;
  cursor: pointer;
}
.tb b {
  color: var(--ink);
  font-weight: 650;
}
.tb.on {
  border-color: var(--ink-2);
  background: rgba(255, 255, 255, 0.1);
}
.blocks {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.2rem;
}
.bh {
  font-size: 0.72rem;
  color: var(--ink);
  font-weight: 600;
  border-bottom: 1px solid var(--axis);
  padding-bottom: 0.15rem;
  margin-bottom: 0.15rem;
}
.bs {
  font-weight: 400;
  color: var(--muted);
  font-size: 0.62rem;
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.lab {
  font-size: 13px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.val {
  font-size: 14px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.was {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.halo {
  paint-order: stroke;
  stroke: var(--bg);
  stroke-width: 4px;
  stroke-linejoin: round;
}
.fit {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.fit.over {
  fill: var(--ink);
  font-weight: 650;
}
.bar {
  transition: width 1s cubic-bezier(0.3, 0.1, 0.2, 1);
}
.tl {
  transition: transform 0.5s ease;
}
.cr {
  display: flex;
  flex-wrap: wrap;
  gap: 0.15rem 0.9rem;
  font-size: 0.62rem;
  color: var(--ink-2);
  margin-top: 0.1rem;
}
.cr span {
  display: inline-flex;
  align-items: center;
}
.cr .no {
  color: var(--ink);
  font-weight: 600;
}
.key {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 2px;
  margin-right: 0.3rem;
}
.sum {
  margin-top: 0.45rem;
  font-size: 0.66rem;
  line-height: 1.4;
  color: var(--ink-2);
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--hair);
  border-radius: 10px;
  padding: 0.35rem 0.7rem;
}
.sum b {
  color: var(--ink);
}
</style>
