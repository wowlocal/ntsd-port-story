<script setup lang="ts">
// Launch -> loaded menu on the Galaxy A12, one typical run before the loop (ml-p0, 0034e45) and one after it
// (ml-l20, e184b10), raced on one time scale in real time (or x10). The run is the median by launch-to-loaded
// among that build's runs; phases: startup, the menu before the load, the loading screen.
// Starts with the button or on the slide's first click. Export shows the moment the new build reaches its menu.
// Data: data/loading_race.json (scripts/collect_loading.py).
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useIsSlideActive, useNav, useSlideContext } from '@slidev/client'
import data from '../data/loading_race.json'

const { $clicks } = useSlideContext()
const nav = useNav()
const active = useIsSlideActive()
const d = data as any
const lanes = [
  { key: 'before', date: '10 октября', name: 'до цикла', build: `сборка ${d.before.commit}`, r: d.before },
  { key: 'after', date: '11 октября', name: 'после цикла', build: `сборка ${d.after.commit}`, r: d.after },
]
const END = d.before.total as number
const t = ref(0)
const running = ref(false)
const speed = ref(1)
let raf = 0
let last = 0

const shownT = computed(() => (nav.isPrintMode.value ? d.after.total : t.value))
const f1 = (v: number) => v.toFixed(1).replace('.', ',')
const pct = (s: number) => `${(s / END) * 100}%`

function phaseOf(r: any, s: number) {
  if (s < r.startup)
    return 'start'
  if (s < r.startup + r.menu)
    return 'menu'
  if (s < r.total)
    return 'load'
  return 'done'
}
function segs(r: any, s: number) {
  const a = Math.min(s, r.startup)
  const b = Math.min(Math.max(s - r.startup, 0), r.menu)
  const c = Math.min(Math.max(s - r.startup - r.menu, 0), r.load)
  return [
    { k: 'start', x: 0, w: a },
    { k: 'menu', x: r.startup, w: b },
    { k: 'load', x: r.startup + r.menu, w: c },
  ]
}

function tick(now: number) {
  const dt = (now - last) / 1000
  last = now
  t.value = Math.min(END, t.value + dt * speed.value)
  if (t.value < END)
    raf = requestAnimationFrame(tick)
  else
    running.value = false
}
function start() {
  cancelAnimationFrame(raf)
  t.value = 0
  running.value = true
  last = performance.now()
  raf = requestAnimationFrame(tick)
}
// give the keyboard back to the deck, so the next arrow key still navigates
const blur = (e: Event) => (e.currentTarget as HTMLElement | null)?.blur()
function reset() {
  cancelAnimationFrame(raf)
  running.value = false
  t.value = 0
}
watch(() => $clicks?.value ?? 0, (c, old) => {
  if (!active.value || nav.isPrintMode.value)
    return
  if (c >= 1 && (old ?? 0) < 1 && !running.value)
    start()
  if (c < 1)
    reset()
})
watch(active, (v) => {
  if (!v)
    reset()
})
onBeforeUnmount(() => cancelAnimationFrame(raf))

const lead = computed(() => {
  const s = shownT.value
  if (s < d.after.total)
    return null
  if (s >= d.before.total)
    return `разница — ${f1(d.before.total - d.after.total)} с`
  return `старой сборке ещё ${f1(d.before.total - s)} с, она на экране загрузки`
})
const ticks = [0, 30, 60, 90, 120]
</script>

<template>
  <div class="race">
    <div v-for="l in lanes" :key="l.key" class="lane" :class="l.key">
      <div class="who">
        <div class="date pixel">
          {{ l.date }}
        </div>
        <div class="name">
          {{ l.name }}
        </div>
        <div class="build mono">
          {{ l.build }}
        </div>
      </div>
      <div class="screen" :class="phaseOf(l.r, shownT)">
        <img v-if="phaseOf(l.r, shownT) === 'load'" src="/img/loading-screen-tobi.jpg" alt="экран загрузки игры">
        <img v-else-if="phaseOf(l.r, shownT) === 'done'" src="/img/menu-back-naruto-vs-sasuke.jpg" alt="фон меню игры">
        <span class="cap">{{ { start: 'запуск', menu: 'меню до загрузки', load: 'экран загрузки', done: 'меню загружено' }[phaseOf(l.r, shownT)] }}</span>
      </div>
      <div class="track-wrap">
        <div class="clock">
          <span class="sec">{{ f1(Math.min(shownT, l.r.total)) }}</span><span class="u">с</span>
          <span v-if="shownT >= l.r.total" class="ok"><span class="i-pixelarticons-check" /> в меню</span>
        </div>
        <div class="track">
          <div v-for="s in segs(l.r, shownT)" :key="s.k" class="seg" :class="s.k" :style="{ left: pct(s.x), width: pct(s.w) }" />
          <div v-if="shownT < l.r.total && (running || shownT > 0)" class="head" :style="{ left: pct(Math.min(shownT, l.r.total)) }" />
        </div>
        <div class="final">
          до меню <b>{{ f1(l.r.total) }} с</b>: запуск {{ f1(l.r.startup) }} · меню {{ f1(l.r.menu) }} · экран загрузки <b>{{ f1(l.r.load) }}</b>
        </div>
      </div>
    </div>

    <div class="axis">
      <span v-for="s in ticks" :key="s" class="tk" :style="{ left: pct(s) }">{{ s }}{{ s === 120 ? ' с' : '' }}</span>
    </div>

    <div class="bar">
      <button v-if="!nav.isPrintMode.value" class="btn go" @click="blur($event); running ? reset() : start()">
        <span :class="running ? 'i-pixelarticons-reload' : 'i-pixelarticons-play'" />{{ running ? 'заново' : (t > 0 ? 'ещё раз' : 'старт') }}
      </button>
      <div v-if="!nav.isPrintMode.value" class="speed">
        <button :class="{ on: speed === 1 }" @click="blur($event); speed = 1">
          1:1
        </button>
        <button :class="{ on: speed === 10 }" @click="blur($event); speed = 10">
          ×10
        </button>
      </div>
      <span v-if="!nav.isPrintMode.value && !running && t === 0" class="hint">или клик по слайду</span>
      <span class="legend"><i class="sw start" />запуск <i class="sw menu" />меню до загрузки <i class="sw load" />экран загрузки</span>
      <span v-if="lead" class="lead">{{ lead }}</span>
    </div>
  </div>
</template>

<style scoped>
.race {
  --lane-h: 100px;
  position: relative;
}
.lane {
  display: grid;
  grid-template-columns: 118px 144px 1fr;
  gap: 14px;
  align-items: center;
  height: var(--lane-h);
  margin-bottom: 10px;
}
.who .date {
  font-size: 0.7rem;
  color: var(--naruto);
}
.after .who .date {
  color: var(--chakra);
}
.who .name {
  font-size: 0.95rem;
  font-weight: 650;
  color: var(--ink);
  line-height: 1.2;
}
.who .build {
  font-size: 0.62rem;
  color: var(--muted);
}
.screen {
  position: relative;
  width: 144px;
  height: 100px;
  border-radius: 8px;
  border: 1px solid var(--axis);
  background: #000;
  overflow: hidden;
}
.screen.menu {
  background: linear-gradient(180deg, #1a2234, #0e131c);
}
.screen img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.screen .cap {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  font-size: 0.6rem;
  color: var(--ink);
  background: rgba(10, 13, 19, 0.78);
  padding: 0.1rem 0.4rem;
  text-align: center;
}
.screen.start .cap,
.screen.menu .cap {
  top: 50%;
  bottom: auto;
  transform: translateY(-50%);
  background: none;
  color: var(--ink-2);
}
.screen.done {
  border-color: rgba(12, 163, 12, 0.7);
}
.track-wrap {
  position: relative;
}
.clock {
  display: flex;
  align-items: baseline;
  gap: 0.2rem;
  height: 30px;
}
.clock .sec {
  font-size: 1.6rem;
  font-weight: 650;
  color: var(--ink);
  font-variant-numeric: tabular-nums;
  line-height: 1;
}
.clock .u {
  font-size: 0.8rem;
  color: var(--ink-2);
}
.clock .ok {
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  margin-left: 0.6rem;
  font-size: 0.72rem;
  color: var(--ink);
  background: rgba(12, 163, 12, 0.18);
  border: 1px solid rgba(12, 163, 12, 0.55);
  border-radius: 999px;
  padding: 0 0.5rem;
}
.track {
  position: relative;
  height: 20px;
  margin-top: 4px;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 4px;
}
.seg {
  position: absolute;
  top: 2px;
  bottom: 2px;
  border-radius: 3px;
}
.seg.start {
  background: #5d6679;
}
.seg.menu {
  background: var(--s1);
}
.seg.load {
  background: var(--s2);
}
.head {
  position: absolute;
  top: -4px;
  bottom: -4px;
  width: 2px;
  margin-left: -1px;
  background: var(--ink);
}
.final {
  margin-top: 5px;
  font-size: 0.66rem;
  color: var(--ink-2);
}
.final b {
  color: var(--ink);
}
.axis {
  position: relative;
  height: 14px;
  margin-left: calc(118px + 144px + 28px);
  border-top: 1px solid var(--axis);
}
.tk {
  position: absolute;
  top: 1px;
  transform: translateX(-50%);
  font-size: 0.62rem;
  color: var(--muted);
}
.bar {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  margin-top: 0.55rem;
  font-size: 0.68rem;
  color: var(--ink-2);
}
.btn,
.speed button {
  font-family: var(--font-sans);
  font-size: 0.72rem;
  color: var(--ink);
  background: var(--surface-2);
  border: 1px solid var(--axis);
  border-radius: 8px;
  padding: 0.2rem 0.7rem;
  cursor: pointer;
}
.btn.go {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(255, 138, 61, 0.18);
  border-color: rgba(255, 138, 61, 0.7);
}
.speed {
  display: inline-flex;
}
.speed button {
  border-radius: 0;
  padding: 0.2rem 0.55rem;
  color: var(--ink-2);
}
.speed button:first-child {
  border-radius: 8px 0 0 8px;
}
.speed button:last-child {
  border-radius: 0 8px 8px 0;
  border-left: none;
}
.speed button.on {
  color: var(--ink);
  background: var(--surface-3);
  box-shadow: inset 0 -2px 0 var(--naruto);
}
.legend {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.sw {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 3px;
  margin-left: 0.4rem;
}
.sw.start {
  background: #5d6679;
  margin-left: 0;
}
.sw.menu {
  background: var(--s1);
}
.sw.load {
  background: var(--s2);
}
.hint {
  color: var(--muted);
}
.lead {
  margin-left: auto;
  color: var(--ink);
  font-weight: 600;
}
</style>
