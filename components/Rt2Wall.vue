<script setup lang="ts">
// Chapter 15: the wall of 10 Oct. Left: what was left for the main thread, in the plan's own estimates (ms per tick):
// the decision-free items all sit inside the phone's resolution (±0.25 ms per run, shaded); the four items the
// author's answers would unlock (Q1–Q4) are ranges. Right: the tier-3 plan's forecast of 8 Oct for "no decisions"
// against what the loop reached. Hover a row for its full name. Data: data/rt2_wall.json (scripts/collect_realtime2.py).
import { ref } from 'vue'
import data from '../data/rt2_wall.json'

const d = data as any
const f2 = (v: number) => v.toFixed(2).replace('.', ',')
const fx = (v: number) => String(v).replace('.', ',')
const freeName: Record<string, string> = {
  'H3': 'H3 · отдельная дорожка шага тика',
  'H2': 'H2 · одна слитая попытка Host',
  'a polling render thread': 'рендер-поток без пробуждений',
  'boxing the platform\'s rarely written deliveries': 'редкие поставки платформы — в коробку',
  'L6': 'L6 · ленивый холостой батч',
  'lastRequest': 'перезапись lastRequest',
}
const qName: Record<string, string> = {
  Q1: 'B · одна транзакционная копия на тик',
  Q2: 'D · прямой игровой тик (с B и H2)',
  Q3: 'L6b · прежняя платформа в коммите',
  Q4: 'P · проверки дисплея — в поток рендера',
}
const rows = [
  ...d.decisionFree.map((f: any) => ({ key: f.item, name: freeName[f.item] ?? f.item, lo: f.ms, hi: f.ms, q: null })),
  ...['Q1', 'Q2', 'Q3', 'Q4'].map(q => ({ key: q, name: qName[q], lo: d.decisions[q].lo, hi: d.decisions[q].hi, q })),
]
const W = 520
const RH = 20
const top = 24
const H = top + rows.length * RH + 36
const L = 236
const R = W - 46
const MAX = 1.3
const x = (v: number) => L + (v / MAX) * (R - L)
const res = d.resolutionMs
const hover = ref<string | null>(null)

// plan vs fact, one axis 8..17 ms
const PW = 340
const PH = 132
const PL = 14
const PR = PW - 14
const px = (v: number) => PL + ((v - 8) / (17 - 8)) * (PR - PL)
const plan = d.planWithoutDecisions
const fact = d.fact
const proj = d.projectionWithQ2toQ4
const start = d.planStart.vs
// short Russian glosses of TIER3's "Decisions for the user" (the English text is in d.decisions[q].question)
const gloss: Record<string, string> = {
  Q1: 'упавший тик может оставить Host только с входом до тика?',
  Q2: 'любой сбой до хвоста тика оставляет Host на последнем батче?',
  Q3: 'холостой коммит может держать прежний объект платформы?',
  Q4: 'ошибка дисплея может остановить игру на тик позже?',
}
const qs = ['Q1', 'Q2', 'Q3', 'Q4'].map(q => ({ q, text: gloss[q] }))
</script>

<template>
  <div class="wall">
    <div>
      <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Что осталось для главного потока: оценки плана против разрешения телефона" @pointerleave="hover = null">
        <rect :x="x(0)" :y="top - 6" :width="x(res) - x(0)" :height="rows.length * RH + 20" fill="rgba(255,255,255,0.07)" />
        <text :x="x(res) + 4" :y="top - 10" class="res">± {{ fx(res) }} мс — разрешение телефона за прогон</text>
        <g v-for="t in [0, 0.5, 1]" :key="t">
          <line :x1="x(t)" :x2="x(t)" :y1="top - 6" :y2="H - 18" stroke="var(--grid)" />
          <text :x="x(t)" :y="H - 6" text-anchor="middle" class="tick">{{ fx(t) }}{{ t === 1 ? ' мс' : '' }}</text>
        </g>
        <text x="0" :y="top - 10" class="gh">без решений автора</text>
        <line x1="0" :x2="W" :y1="top + 6 * RH - 1" :y2="top + 6 * RH - 1" stroke="var(--axis)" />
        <text x="0" :y="top + 6 * RH + 11" class="gh2">по ответам автора</text>
        <g v-for="(r, i) in rows" :key="r.key" @pointerenter="hover = r.key">
          <rect x="0" :y="top + i * RH + (i >= 6 ? 14 : 0)" :width="W" :height="RH" :fill="hover === r.key ? 'rgba(255,255,255,0.05)' : 'transparent'" />
          <text :x="L - 8" :y="top + i * RH + (i >= 6 ? 14 : 0) + 13" text-anchor="end" class="rn"><tspan v-if="r.q" class="qn">{{ `${r.q}\u00A0·\u00A0` }}</tspan>{{ r.name }}</text>
          <template v-if="!r.q">
            <rect :x="x(0)" :y="top + i * RH + 4" :width="Math.max(2, x(r.lo) - x(0))" height="11" rx="2" fill="#7a8396" />
            <text :x="x(r.lo) + 5" :y="top + i * RH + 13" class="rv">≈ {{ fx(r.lo) }}</text>
          </template>
          <template v-else>
            <rect :x="x(0)" :y="top + i * RH + 18" :width="x(r.lo) - x(0)" height="11" rx="2" fill="var(--s2)" />
            <rect :x="x(r.lo)" :y="top + i * RH + 18" :width="x(r.hi) - x(r.lo)" height="11" rx="2" fill="var(--s2)" style="opacity: 0.4" />
            <text :x="x(r.hi) + 5" :y="top + i * RH + 27" class="rv">{{ fx(r.lo) }}–{{ fx(r.hi) }}</text>
          </template>
        </g>
      </svg>
      <div class="qs">
        <div v-for="q in qs" :key="q.q" class="q">
          <span class="pixel qn2">{{ q.q }}</span> {{ q.text }}
        </div>
      </div>
    </div>

    <div class="pf">
      <div class="ph">
        план яруса 3 · 8 окт 21:12 · <span class="mono">5fe8641</span>
      </div>
      <p class="plan-quote">
        «Without them the plan reaches about 11 ms on the main thread and about 8 on the render thread.»
      </p>
      <svg :viewBox="`0 0 ${PW} ${PH}`" width="100%" role="img" :aria-label="`План: ${plan.main} мс (${plan.lo}–${plan.hi}); факт: vs ${f2(fact.vs)}, Demo ${f2(fact.demo)}`">
        <line :x1="PL" :x2="PR" y1="96" y2="96" stroke="var(--axis)" />
        <g v-for="t in [8, 10, 12, 14, 16]" :key="t">
          <line :x1="px(t)" :x2="px(t)" y1="92" y2="100" stroke="var(--axis)" />
          <text :x="px(t)" y="114" text-anchor="middle" class="tick">{{ t }}{{ t === 16 ? ' мс' : '' }}</text>
        </g>
        <!-- target -->
        <line :x1="px(8)" :x2="px(8)" y1="14" y2="96" stroke="var(--ink)" stroke-width="1.5" />
        <text :x="px(8) + 4" y="22" class="lbl">цель 8</text>
        <!-- where the main thread stood when the plan was written -->
        <circle :cx="px(start)" cy="12" r="4" fill="#566074" />
        <text :x="px(start) - 8" y="16" text-anchor="end" class="lbl2">8 окт, когда писали: {{ fx(start) }}</text>
        <!-- plan band -->
        <rect :x="px(plan.lo)" y="26" :width="px(plan.hi) - px(plan.lo)" height="18" rx="3" fill="rgba(255,255,255,0.08)" stroke="var(--axis)" />
        <line :x1="px(plan.main)" :x2="px(plan.main)" y1="24" y2="46" stroke="var(--ink-2)" stroke-width="2" />
        <text :x="px(plan.hi) + 5" y="39" class="lbl">план: ≈ {{ plan.main }} ({{ fx(plan.lo) }}–{{ fx(plan.hi) }})</text>
        <!-- with decisions -->
        <rect :x="px(proj.lo)" y="52" :width="px(proj.hi) - px(proj.lo)" height="12" rx="3" fill="rgba(255,255,255,0.05)" stroke="var(--axis)" stroke-dasharray="3 2" />
        <text :x="px(proj.hi) + 5" y="62" class="lbl2">с ответами Q2–Q4: ≈ {{ proj.lo }}–{{ proj.hi }}</text>
        <!-- fact -->
        <circle :cx="px(fact.vs)" cy="80" r="5" fill="var(--s2)" stroke="var(--bg)" stroke-width="2" />
        <circle :cx="px(fact.demo)" cy="80" r="5" fill="var(--s2)" style="opacity: 0.55" stroke="var(--bg)" stroke-width="2" />
        <text :x="px(fact.demo) + 9" y="84" class="lbl">факт 10 окт: vs {{ f2(fact.vs) }}, Demo {{ f2(fact.demo) }}</text>
      </svg>
      <div class="pn">
        Рендер: план ≈ {{ plan.render }}, факт — {{ f2(fact.renderVs) }} (vs) и {{ f2(fact.renderDemo) }} (Demo). План шёл своим порядком; сравнимы только концы.
      </div>
      <div class="qq">
        <div class="ph">
          что на кону в Q1–Q4
        </div>
        <p lang="en" class="mono qe">
          «Production stops on any error … so Q1–Q3 change only what tests observe after a failure; Q4 moves when an error surfaces by one tick.»
        </p>
        <p class="qg">
          В выпуске любая ошибка и так останавливает игру: ответы меняют только то, что видят тесты после сбоя, — а Q4 сдвигает остановку на один тик.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wall {
  display: grid;
  grid-template-columns: 520fr 340fr;
  gap: 1.4rem;
  align-items: start;
}
.res {
  font-size: 10px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.gh,
.gh2 {
  font-size: 10.5px;
  fill: var(--ink);
  font-weight: 650;
  font-family: var(--font-sans);
}
.rn {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.qn {
  fill: var(--naruto);
  font-family: var(--font-pixel);
}
.rv {
  font-size: 10.5px;
  fill: var(--ink);
  font-family: var(--font-sans);
  font-weight: 600;
}
.qs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.2rem 0.8rem;
  margin-top: 0.15rem;
}
.q {
  font-size: 0.64rem;
  line-height: 1.3;
  color: var(--ink-2);
}
.qn2 {
  color: var(--naruto);
  font-size: 0.66rem;
}
.pf {
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.45rem 0.7rem 0.5rem;
}
.ph {
  font-size: 0.64rem;
  color: var(--naruto);
  font-family: var(--font-pixel);
}
.ph .mono {
  font-family: var(--font-mono);
  color: var(--muted);
  font-size: 0.6rem;
}
.plan-quote {
  font-size: 0.64rem !important;
  line-height: 1.35;
  color: var(--ink) !important;
  margin: 0.2rem 0 0.1rem !important;
}
.lbl {
  font-size: 10.5px;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.lbl2 {
  font-size: 10px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.qq {
  margin-top: 0.45rem;
  border-top: 1px dashed var(--axis);
  padding-top: 0.35rem;
}
.qe {
  font-size: 0.62rem !important;
  line-height: 1.4;
  color: var(--ink) !important;
  margin: 0.15rem 0 !important;
}
.qg {
  font-size: 0.64rem !important;
  line-height: 1.35;
  color: var(--ink-2) !important;
  margin: 0.1rem 0 0 !important;
}
.pn {
  font-size: 0.6rem;
  line-height: 1.35;
  color: var(--muted);
}
</style>
