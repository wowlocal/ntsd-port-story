<script setup lang="ts">
// Chapter 15: the loop the agent ran 7–10 Oct, as a ring of five stations, with three real iterations to pick from
// (one kept, one parked, one reverted). While the slide is active a token travels the ring and lights the station it
// passes; the tabs switch the iteration. Export shows S2b with every station lit.
// Numbers: data/rt2_steps.json (phone A/B of each step) and the evidence files named on the slide.
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'
import data from '../data/rt2_steps.json'
import loop from '../data/rt2_loop.json'

const nav = useNav()
const active = useIsSlideActive()
const steps = (data as any).steps as any[]
const st = (id: string) => steps.find(s => s.id === id)
const f2 = (v: number) => v.toFixed(2).replace('.', ',')
const ab = (id: string, sc: 'vs' | 'demo') => {
  const v = st(id)[sc]
  return `${f2(v.base.main)} → ${f2(v.after.main)}`
}
const L = loop as any

const stations = ['профиль телефона', 'одна правка', 'ворота и ревью', 'A/B на телефоне', 'решение']
const examples = [
  {
    id: 'S2b', tag: 'быстрее — оставлено', cls: 'good', when: '9 окт, 11:18 → 18:51',
    text: [
      'копирование массивов при записи — 9,40 % главного потока: каждая копия записи дублировала массив байтов и массив Bool',
      'каждая запись — один буфер: байты, затем бит «определён» на каждый байт; запись по-прежнему 40 байт',
      'первый прогон: проверки в тестах стали квадратичными, набор встал на ~2 ч → кэш целых массивов; затем 10 сценариев, 1 832 кадра, AppKit, эмулятор, 755 тестов; ревью — одобрено после исправлений',
      `3 прогона против 2 прежней сборки в одной сессии: vs ${ab('S2b', 'vs')} мс, Demo ${ab('S2b', 'demo')} мс`,
      'быстрее → коммит 10b9c05; в профиле после — 4,96 %',
    ],
  },
  {
    id: 'S3', tag: 'не быстрее — отложено', cls: 'bad', when: '9 окт, 18:52',
    text: [
      'после S2b: массив из 400 актёров копируется целиком в локальном вводе и в управлении миром',
      'таблица актёров — 25 кусков по 16 записей за интерфейсом массива; ~50 сигнатур проходов',
      'поведение равно; ревью одобрило — и заподозрило лишние retain/release при чтении через вложенные куски',
      `vs ${ab('S3', 'vs')} мс, Demo ${ab('S3', 'demo')} (один низкий выброс): копий массива меньше, уничтожений записей больше`,
      'не быстрее, а сложнее → не коммитить: патч отложен, результат записан в реестр (cea9fd0)',
    ],
  },
  {
    id: 'B2 P4a', tag: 'не быстрее — откат', cls: 'bad', when: '8 окт, 00:21',
    text: [
      'подсчёт ссылок ~30 % главного потока, копии записей 5,6 % — от проходов игрового тела',
      'три прохода мира — управление, связи, импульсы — работают на месте, без своей копии',
      'поведение равно; ревью: верно — и заранее предсказало, что выигрыша не будет',
      `${ab('B2 P4a', 'vs')} мс — в пределах разброса прогонов`,
      'откат. Вывод: каждый уровень транзакции копирует массив — убирать надо все уровни разом. Так сделали P4b–P4f: 18,14 → 16,86 мс',
    ],
  },
]
const pick = ref(0)
const ex = computed(() => examples[pick.value])

// ring geometry
const W = 340
const H = 272
const cx = 170
const cy = 146
const R = 100
const ang = (k: number) => -Math.PI / 2 + (k * 2 * Math.PI) / 5
const node = (k: number) => ({ x: cx + R * Math.cos(ang(k)), y: cy + R * Math.sin(ang(k)) })
const nodes = stations.map((name, k) => ({ name, k, ...node(k) }))
// labels above the top three stations, below the bottom two; always centred, so they stay inside the viewBox
const labelPos = (k: number) => {
  const p = node(k)
  return { x: p.x, y: k === 2 || k === 3 ? p.y + 39 : p.y - 30, anchor: 'middle' }
}
const arc = (k: number) => {
  const a0 = ang(k) + 0.3
  const a1 = ang(k + 1) - 0.3
  const p0 = { x: cx + R * Math.cos(a0), y: cy + R * Math.sin(a0) }
  const p1 = { x: cx + R * Math.cos(a1), y: cy + R * Math.sin(a1) }
  return `M${p0.x.toFixed(1)},${p0.y.toFixed(1)} A${R},${R} 0 0 1 ${p1.x.toFixed(1)},${p1.y.toFixed(1)}`
}

const phase = ref(0) // 0..5, the token's position along the ring in stations
const lit = computed(() => (nav.isPrintMode.value ? -1 : Math.floor(phase.value) % 5))
const token = computed(() => {
  const a = -Math.PI / 2 + (phase.value * 2 * Math.PI) / 5
  return { x: cx + R * Math.cos(a), y: cy + R * Math.sin(a) }
})
let raf = 0
let t0 = 0
function run() {
  cancelAnimationFrame(raf)
  if (nav.isPrintMode.value) {
    phase.value = 4.5
    return
  }
  t0 = performance.now()
  const tick = (t: number) => {
    phase.value = ((t - t0) / 1700) % 5
    if (active.value)
      raf = requestAnimationFrame(tick)
  }
  raf = requestAnimationFrame(tick)
}
function choose(i: number) {
  pick.value = i
  t0 = performance.now()
}
onMounted(() => {
  if (active.value || nav.isPrintMode.value)
    run()
})
watch(active, (v) => {
  if (v)
    run()
  else
    cancelAnimationFrame(raf)
})
onBeforeUnmount(() => cancelAnimationFrame(raf))
const perRow = Math.round((loop as any).hours * 60 / (loop as any).rows)
</script>

<template>
  <div class="loop">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Петля: профиль, одна правка, ворота и ревью, A/B на телефоне, решение">
      <defs>
        <marker id="rt2-arrow" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="7" markerHeight="7" orient="auto">
          <path d="M0,0 L8,4 L0,8 z" fill="var(--axis)" />
        </marker>
      </defs>
      <path v-for="k in 5" :key="`a${k}`" :d="arc(k - 1)" fill="none" stroke="var(--axis)" stroke-width="2" marker-end="url(#rt2-arrow)" />
      <g v-for="n in nodes" :key="n.k">
        <circle :cx="n.x" :cy="n.y" r="22" :fill="lit === n.k || lit === -1 ? 'rgba(255,138,61,0.16)' : 'var(--surface-2)'" :stroke="lit === n.k ? 'var(--naruto)' : 'var(--axis)'" stroke-width="2" class="nd" />
        <text :x="n.x" :y="n.y + 6" text-anchor="middle" class="num">{{ n.k + 1 }}</text>
        <text :x="labelPos(n.k).x" :y="labelPos(n.k).y" :text-anchor="labelPos(n.k).anchor" class="nl">{{ n.name }}</text>
      </g>
      <circle v-if="!nav.isPrintMode.value" :cx="token.x" :cy="token.y" r="6" fill="var(--naruto)" stroke="var(--bg)" stroke-width="2" />
      <text :x="cx" :y="cy - 6" text-anchor="middle" class="c1">{{ L.rows }} строк реестра</text>
      <text :x="cx" :y="cy + 10" text-anchor="middle" class="c2">в среднем каждые ≈ {{ perRow }} мин</text>
      <text :x="cx" :y="cy + 25" text-anchor="middle" class="c2">днём и ночью</text>
    </svg>

    <div class="panel">
      <div class="tabs">
        <button v-for="(e, i) in examples" :key="e.id" class="tab" :class="{ on: pick === i }" @click="choose(i)">
          <span class="pixel tid">{{ e.id }}</span> <span class="tt">{{ e.tag }}</span>
        </button>
      </div>
      <div class="when mono">
        {{ ex.when }}
      </div>
      <div v-for="(t, k) in ex.text" :key="`${ex.id}${k}`" class="st" :class="{ on: lit === k, last: k === 4, [ex.cls]: k === 4 }">
        <span class="n pixel">{{ k + 1 }}</span>
        <div><span class="sn">{{ stations[k] }}</span> {{ t }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.loop {
  display: grid;
  grid-template-columns: 340fr 544fr;
  gap: 1rem;
  align-items: start;
}
.nd {
  transition: fill 0.25s ease, stroke 0.25s ease;
}
.num {
  font-family: var(--font-pixel);
  font-size: 17px;
  fill: var(--ink);
}
.nl {
  font-family: var(--font-sans);
  font-size: 11.5px;
  fill: var(--ink-2);
}
.c1 {
  font-family: var(--font-sans);
  font-size: 13px;
  font-weight: 650;
  fill: var(--ink);
}
.c2 {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--muted);
}
.tabs {
  display: flex;
  gap: 0.35rem;
  margin-bottom: 0.25rem;
}
.tab {
  font-family: var(--font-sans);
  font-size: 0.66rem;
  color: var(--ink-2);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--hair);
  border-radius: 999px;
  padding: 0.14rem 0.6rem;
  cursor: pointer;
}
.tab.on {
  color: var(--ink);
  border-color: rgba(255, 138, 61, 0.7);
  background: rgba(255, 138, 61, 0.12);
}
.tid {
  color: var(--naruto);
}
.when {
  font-size: 0.6rem;
  color: var(--muted);
  margin: 0.1rem 0 0.2rem 0.2rem;
}
.st {
  display: grid;
  grid-template-columns: 1.3rem 1fr;
  gap: 0.35rem;
  font-size: 0.66rem;
  line-height: 1.33;
  color: var(--ink-2);
  padding: 0.24rem 0.45rem;
  border-radius: 8px;
  border: 1px solid transparent;
  transition: background 0.25s ease, border-color 0.25s ease;
}
.st.on {
  background: rgba(255, 138, 61, 0.08);
  border-color: rgba(255, 138, 61, 0.35);
}
.st .n {
  font-size: 0.85rem;
  color: var(--naruto);
  line-height: 1.1;
}
.sn {
  color: var(--ink);
  font-weight: 650;
  margin-right: 0.2rem;
}
.st.last.good {
  box-shadow: inset 3px 0 0 var(--good);
}
.st.last.bad {
  box-shadow: inset 3px 0 0 var(--serious);
}
</style>
