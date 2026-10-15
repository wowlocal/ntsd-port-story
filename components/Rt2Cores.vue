<script setup lang="ts">
// Chapter 15: how a parked experiment found the slow cores. The A12's two CPU clusters, and where each thread ran at
// five moments of 9–10 Oct: R2 parked (presenter thread: render −4 ms, main +0.2–0.4 ms), R2 re-measured and the
// threads sampled (main mostly on the 1.8 GHz cluster), P0 (main pinned to the faster cores), R2 committed with the
// presenter pinned to the slower ones, R3 (a release thread there too). One click per moment; export shows the last
// with every moment listed. Data: data/rt2_threads.json (scripts/collect_realtime2.py).
import { computed } from 'vue'
import { useNav, useSlideContext } from '@slidev/client'
import data from '../data/rt2_threads.json'

const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const k = computed(() => (!props.stepwise || nav.isPrintMode.value ? 4 : Math.min(4, $clicks?.value ?? 0)))

const d = data as any
const f2 = (v: number) => v.toFixed(2).replace('.', ',')
const f1 = (v: number) => v.toFixed(1).replace('.', ',')
const ab = (o: any, key: string) => `${f2(o.base[key])} → ${f2(o.after[key])}`

const moments = [
  {
    id: 'R2', when: '9 окт, 06:09', hash: '2459bdb', head: 'вывод Android — в свой поток',
    lines: [`рендер vs ${ab(d.r2parked.vs, 'render')}, Demo ${ab(d.r2parked.demo, 'render')}`, `но главный vs ${ab(d.r2parked.vs, 'main')}, Demo ${ab(d.r2parked.demo, 'main')}`],
    verdict: 'отложено: кадр упирается в главный поток', bad: true,
  },
  {
    id: 'R2b', when: '10 окт, утро', hash: '7fe4d0e', head: 'перемер на новой сборке и выборка потоков раз в секунду',
    lines: [`Demo: главный снова ${ab(d.r2b.demo, 'main')} мс`, 'главный поток — в основном на медленном кластере'],
    verdict: 'находка, которой не было в плане', bad: false,
  },
  {
    id: 'P0', when: '10 окт, 07:46', hash: '7fe4d0e', head: 'главный поток — на быстрые ядра',
    lines: [`главный vs ${ab(d.p0.vs, 'main')}, Demo ${ab(d.p0.demo, 'main')}`, 'те же вычисления, другое место'],
    verdict: 'закоммичено', bad: false,
  },
  {
    id: 'R2', when: '10 окт, 08:30', hash: '60a16db', head: 'presenter — на медленные ядра',
    lines: [`рендер vs ${ab(d.r2.vs, 'render')}, Demo ${ab(d.r2.demo, 'render')}`, `presenter ≈ ${f1(d.r2.demo.after.present)} мс; главный — в пределах шума`],
    verdict: 'закоммичено', bad: false,
  },
  {
    id: 'R3', when: '10 окт, 12:18', hash: 'd342f74', head: 'освобождение памяти — свой поток, туда же',
    lines: [`главный vs ${ab(d.r3.vs, 'main')}, Demo ${ab(d.r3.demo, 'main')}`, `release ≈ ${f1(d.r3.vs.after.release)} мс на тик`],
    verdict: 'закоммичено', bad: false,
  },
]

// placement per moment: 'fast' / 'slow' cluster, 'any' = left to the scheduler
interface Chip { key: string, name: string, color: string, where: 'fast' | 'slow' | 'any', pinned?: boolean, note?: string }
const placement = computed<Chip[]>(() => {
  const s = k.value
  const out: Chip[] = []
  out.push({ key: 'main', name: 'главный', color: 'var(--s2)', where: s === 0 ? 'any' : s === 1 ? 'slow' : 'fast', pinned: s >= 2, note: s === 1 ? 'в основном здесь' : undefined })
  out.push({ key: 'render', name: 'рендер', color: 'var(--s1)', where: 'any' })
  if (s === 0 || s === 1 || s >= 3)
    out.push({ key: 'present', name: 'presenter', color: 'var(--s3)', where: s >= 3 ? 'slow' : 'any', pinned: s >= 3 })
  if (s >= 4)
    out.push({ key: 'release', name: 'release', color: 'var(--s4)', where: 'slow', pinned: true })
  return out
})
const W = 392
const H = 300
const box = { fast: { x: 0, y: 24 }, slow: { x: 202, y: 24 } }
const BW = 190
const BH = 150
const pos = computed(() => {
  const counts: Record<string, number> = { fast: 0, slow: 0, any: 0 }
  return placement.value.map((c) => {
    const i = counts[c.where]++
    if (c.where === 'any')
      return { ...c, x: 8 + i * 128, y: 220 }
    const b = box[c.where]
    return { ...c, x: b.x + 10, y: b.y + 66 + i * 28 }
  })
})
</script>

<template>
  <div class="cores">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Кластеры процессора Galaxy A12 и потоки игры">
      <g v-for="(b, key) in box" :key="key">
        <rect :x="b.x" :y="b.y" :width="BW" :height="BH" rx="10" fill="var(--surface)" stroke="var(--hair)" />
        <text :x="b.x + 10" :y="b.y - 8" class="ct">{{ key === 'fast' ? `CPU 0–3 · ${String(d.cores.fastGHz).replace('.', ',')} ГГц` : `CPU 4–7 · ${String(d.cores.slowGHz).replace('.', ',')} ГГц` }}</text>
        <g v-for="c in 4" :key="c">
          <rect :x="b.x + 10 + (c - 1) * 44" :y="b.y + 12" width="38" height="38" rx="4" fill="var(--surface-3)" stroke="var(--axis)" />
          <text :x="b.x + 29 + (c - 1) * 44" :y="b.y + 35" text-anchor="middle" class="cn">{{ (key === 'fast' ? 0 : 4) + c - 1 }}</text>
        </g>
      </g>
      <line x1="0" :x2="W" y1="198" y2="198" stroke="var(--grid)" />
      <text x="0" y="212" class="ct2">без привязки — куда поставит планировщик</text>
      <text x="0" y="270" class="nt1">Galaxy A12 · Helio P35: восемь ядер Cortex-A53 в двух кластерах.</text>
      <text x="0" y="286" class="nt1">«Закреплён» — sched_setaffinity на ядра своего кластера.</text>
      <g v-for="c in pos" :key="c.key" class="chip" :style="{ transform: `translate(${c.x}px, ${c.y}px)` }">
        <rect x="0" y="0" :width="c.where === 'any' ? 120 : 170" height="22" rx="6" fill="var(--surface-2)" stroke="var(--hair)" />
        <rect x="0" y="0" width="5" height="22" rx="2" :fill="c.color" />
        <text x="12" y="15" class="cl">{{ c.name }}<tspan v-if="c.pinned" class="pin"> · закреплён</tspan><tspan v-if="c.note" class="pin"> · {{ c.note }}</tspan></text>
      </g>
    </svg>

    <div class="tl">
      <div v-for="(m, i) in moments" :key="i" class="mo" :class="{ off: i > k, now: i === k, bad: m.bad }">
        <div class="mo-top">
          <span class="pixel mo-id">{{ m.id }}</span>
          <span class="mono mo-when">{{ m.when }} · {{ m.hash }}</span>
          <span class="mo-verdict">{{ m.verdict }}</span>
        </div>
        <div class="mo-head">
          {{ m.head }}
        </div>
        <div class="mo-line">
          {{ m.lines[0] }}; {{ m.lines[1] }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cores {
  display: grid;
  grid-template-columns: 392fr 492fr;
  gap: 1.1rem;
  align-items: start;
}
.ct {
  font-size: 11px;
  fill: var(--ink);
  font-family: var(--font-sans);
  font-weight: 600;
}
.ct2 {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.nt1 {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.cn {
  font-size: 12px;
  fill: var(--muted);
  font-family: var(--font-pixel);
}
.chip {
  transition: transform 0.6s cubic-bezier(0.3, 0.1, 0.2, 1);
}
.cl {
  font-size: 11px;
  fill: var(--ink);
  font-family: var(--font-sans);
  font-weight: 600;
}
.pin {
  font-weight: 400;
  fill: var(--ink-2);
  font-size: 10px;
}
.tl {
  display: flex;
  flex-direction: column;
  gap: 0.22rem;
}
.mo {
  border: 1px solid var(--hair);
  border-radius: 10px;
  padding: 0.22rem 0.6rem 0.28rem;
  background: rgba(255, 255, 255, 0.02);
  transition: opacity 0.35s ease, border-color 0.35s ease;
}
.mo.off {
  opacity: 0.18;
}
.mo.now {
  border-color: rgba(255, 138, 61, 0.65);
  background: rgba(255, 138, 61, 0.06);
}
.mo-top {
  display: flex;
  align-items: baseline;
  gap: 0.45rem;
}
.mo-id {
  color: var(--naruto);
  font-size: 0.8rem;
}
.mo-when {
  font-size: 0.58rem;
  color: var(--muted);
}
.mo-verdict {
  margin-left: auto;
  font-size: 0.6rem;
  color: var(--ink-2);
}
.mo.bad {
  box-shadow: inset 3px 0 0 var(--serious);
}
.mo-head {
  font-size: 0.7rem;
  color: var(--ink);
  line-height: 1.3;
}
.mo-line {
  font-size: 0.62rem;
  color: var(--ink-2);
  line-height: 1.3;
}
</style>
