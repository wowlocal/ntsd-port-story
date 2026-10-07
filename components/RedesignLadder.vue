<script setup lang="ts">
// The redesign ladder on the Galaxy A12, every ledger row of CORE_REALTIME.md in order, in two panels because the
// metric changed at phase 4f: (A) game ticks per second on the harness's virtual clock, branch start to 4f;
// (B) compute per tick per thread (schedstat), 4f to 4l. Hollow rings are tried versions that were reverted.
// Data: data/perf_ladder.json (scripts/collect_perf.py; each value is the mean of that step's phone runs).
import { useNav, useSlideContext } from '@slidev/client'
import data from '../data/perf_ladder.json'

const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const shown = (k: number) => !props.stepwise || nav.isPrintMode.value || ($clicks?.value ?? 0) >= k

interface Step { id: string, label: string, hash: string, ticksPerSecond: number, mainMs: number | null, renderMs: number | null, rejected?: any }
const all = (data as any).steps as Step[]
const cut = all.findIndex(s => s.id === '4f')
const A = all.slice(0, cut + 1)
const B = all.slice(cut)
const f1 = (v: number) => v.toFixed(1).replace('.', ',')
const pctUp = (a: number, b: number) => `+${Math.round((b / a - 1) * 100)} %`

// ---- panel A
const WA = 492
const HA = 252
const ma = { l: 26, r: 10, t: 64, b: 30 }
const YA = 24
const xa = (i: number) => ma.l + 8 + i * ((WA - ma.l - ma.r - 16) / (A.length - 1))
const ya = (v: number) => ma.t + (1 - v / YA) * (HA - ma.t - ma.b)
const stepPath = A.map((s, i) => i === 0 ? `M${xa(0)},${ya(s.ticksPerSecond)}` : `H${xa(i)} V${ya(s.ticksPerSecond)}`).join(' ')
const callIds = ['2b', '1c', '1e', '4a', 'R3']
const callText: Record<string, [string, string]> = {
  '2b': ['пары записей', 'актёров'],
  '1c': ['пиксели —', 'в свой поток'],
  '1e': ['текст не ждёт', 'рендер'],
  '4a': ['данные сессии', 'в одном объекте'],
  'R3': ['400 актёров', 'в форме модели'],
}
const callX = [44, 136, 228, 320, 418]
const calls = callIds.map((id, k) => {
  const i = A.findIndex(s => s.id === id)
  return { id, i, cx: callX[k], lines: callText[id], gain: pctUp(A[i - 1].ticksPerSecond, A[i].ticksPerSecond), px: xa(i), py: ya((A[i - 1].ticksPerSecond + A[i].ticksPerSecond) / 2) }
})
const first = A[0]
const lastA = A[A.length - 1]

// ---- panel B
const WB = 372
const HB = 252
const mb = { l: 26, r: 92, t: 30, b: 30 }
const YB = 36
const xb = (i: number) => mb.l + 8 + i * ((WB - mb.l - mb.r - 16) / (B.length - 1))
const yb = (v: number) => mb.t + (1 - v / YB) * (HB - mb.t - mb.b)
const line = (key: 'mainMs' | 'renderMs') => B.map((s, i) => `${i ? 'L' : 'M'}${xb(i)},${yb(s[key] as number)}`).join(' ')
const lastB = B[B.length - 1]
const firstB = B[0]
const rej = B.map((s, i) => ({ s, i })).filter(o => o.s.rejected)
</script>

<template>
  <div class="ladder">
    <div class="panel">
      <div class="ph">
        <span class="pixel">А</span> тики в секунду · часы харнесса · 6 октября
      </div>
      <svg :viewBox="`0 0 ${WA} ${HA}`" width="100%" role="img" :aria-label="`Тики в секунду: от ${f1(first.ticksPerSecond)} до ${f1(lastA.ticksPerSecond)}`">
        <g v-for="t in [0, 10, 20]" :key="t">
          <line :x1="ma.l" :x2="WA - ma.r" :y1="ya(t)" :y2="ya(t)" stroke="var(--grid)" />
          <text :x="ma.l - 5" :y="ya(t) + 3.5" text-anchor="end" class="tick">{{ t }}</text>
        </g>
        <!-- callouts for the biggest steps -->
        <g v-for="c in calls" :key="c.id">
          <path :d="`M${c.cx},${46} L${c.cx},${50} L${c.px - 4},${c.py}`" fill="none" stroke="var(--muted)" stroke-width="1" />
          <text :x="c.cx" y="14" text-anchor="middle" class="cg"><tspan class="cid">{{ c.id }}</tspan> {{ c.gain }}</text>
          <text :x="c.cx" y="28" text-anchor="middle" class="cl">{{ c.lines[0] }}</text>
          <text :x="c.cx" y="40" text-anchor="middle" class="cl">{{ c.lines[1] }}</text>
        </g>
        <path :d="stepPath" fill="none" stroke="var(--s2)" stroke-width="2" stroke-linejoin="round" />
        <g v-for="(s, i) in A" :key="s.id">
          <title>{{ s.id }} · {{ s.hash }} — {{ s.label }}: {{ f1(s.ticksPerSecond) }} тика/с</title>
          <circle :cx="xa(i)" :cy="ya(s.ticksPerSecond)" r="3.5" fill="var(--s2)" stroke="var(--bg)" stroke-width="2" />
          <text :x="xa(i)" :y="HA - ma.b + 16" text-anchor="middle" class="sid">{{ s.id }}</text>
        </g>
        <text :x="xa(0) + 6" :y="ya(first.ticksPerSecond) + 18" class="end">{{ f1(first.ticksPerSecond) }}</text>
        <text :x="xa(A.length - 1)" :y="ya(lastA.ticksPerSecond) - 9" text-anchor="end" class="end">{{ f1(lastA.ticksPerSecond) }}</text>
      </svg>
      <div class="cav">
        <span class="i-pixelarticons-alarm-clock ico" />На часах харнесса в каждом тике ≈ 16 мс сна самой игры: тики/с показывают экономию лишь частично. Отсюда переход к панели Б.
      </div>
    </div>

    <div class="panel" :class="{ off: !shown(1) }">
      <div class="ph">
        <span class="pixel">Б</span> мс работы на тик · 6–7 октября
      </div>
      <svg :viewBox="`0 0 ${WB} ${HB}`" width="100%" role="img" :aria-label="`Мс на тик: главный ${f1(firstB.mainMs!)} → ${f1(lastB.mainMs!)}, рендер ${f1(firstB.renderMs!)} → ${f1(lastB.renderMs!)}`">
        <g v-for="t in [0, 10, 20, 30]" :key="t">
          <line :x1="mb.l" :x2="xb(B.length - 1) + 4" :y1="yb(t)" :y2="yb(t)" stroke="var(--grid)" />
          <text :x="mb.l - 5" :y="yb(t) + 3.5" text-anchor="end" class="tick">{{ t }}</text>
        </g>
        <line :x1="mb.l" :x2="xb(B.length - 1) + 4" :y1="yb(33)" :y2="yb(33)" stroke="var(--good)" stroke-width="1.5" />
        <text :x="mb.l + 2" :y="yb(33) - 6" class="tier">ярус 1 · 33 мс — выполнен</text>
        <line :x1="mb.l" :x2="xb(B.length - 1) + 4" :y1="yb(16)" :y2="yb(16)" stroke="var(--ink-2)" stroke-width="1.5" />
        <text :x="mb.l + 2" :y="yb(16) + 14" class="tier">ярус 2 · 16 мс — следующий</text>

        <path :d="line('renderMs')" fill="none" stroke="var(--s1)" stroke-width="2" stroke-linejoin="round" />
        <path :d="line('mainMs')" fill="none" stroke="var(--s2)" stroke-width="2" stroke-linejoin="round" />
        <g v-for="(s, i) in B" :key="s.id">
          <title>{{ s.id }} · {{ s.hash }} — {{ s.label }}: главный {{ f1(s.mainMs!) }} мс, рендер {{ f1(s.renderMs!) }} мс</title>
          <circle :cx="xb(i)" :cy="yb(s.renderMs!)" r="3.5" fill="var(--s1)" stroke="var(--bg)" stroke-width="2" />
          <circle :cx="xb(i)" :cy="yb(s.mainMs!)" r="3.5" fill="var(--s2)" stroke="var(--bg)" stroke-width="2" />
          <text :x="xb(i)" :y="HB - mb.b + 16" text-anchor="middle" class="sid">{{ s.id }}</text>
        </g>
        <g v-for="o in rej" :key="`r${o.s.id}`">
          <title>{{ o.s.rejected.note }}</title>
          <circle v-if="o.s.id === '1i'" :cx="xb(o.i) - 7" :cy="yb(o.s.rejected.renderMs)" r="4" fill="none" stroke="var(--s1)" stroke-width="1.5" />
          <circle v-else :cx="xb(o.i) - 7" :cy="yb(o.s.rejected.mainMs)" r="4" fill="none" stroke="var(--s2)" stroke-width="1.5" />
        </g>
        <text :x="xb(B.length - 1) + 9" :y="yb(lastB.mainMs!) + 4" class="lbl">главный</text>
        <text :x="xb(B.length - 1) + 9" :y="yb(lastB.mainMs!) + 17" class="lv">{{ f1(lastB.mainMs!) }} мс</text>
        <text :x="xb(B.length - 1) + 9" :y="yb(lastB.renderMs!) + 4" class="lbl">рендер</text>
        <text :x="xb(B.length - 1) + 9" :y="yb(lastB.renderMs!) + 17" class="lv">{{ f1(lastB.renderMs!) }} мс</text>
      </svg>
      <div class="legend">
        <span><i class="ln" style="background: var(--s2)" />главный поток</span>
        <span><i class="ln" style="background: var(--s1)" />поток рендера</span>
        <span><i class="ring" />попытка, откат: 1h, первая 3a</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ladder {
  display: grid;
  grid-template-columns: 492fr 372fr;
  gap: 1.2rem;
}
.panel {
  transition: opacity 0.4s ease;
}
.off {
  opacity: 0;
}
.ph {
  font-size: 0.7rem;
  color: var(--ink-2);
  border-bottom: 1px solid var(--axis);
  padding-bottom: 0.2rem;
  margin-bottom: 0.2rem;
}
.ph .pixel {
  color: var(--naruto);
  margin-right: 0.3rem;
}
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
}
.sid {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-mono);
}
.cg {
  font-size: 12px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.cid {
  fill: var(--naruto);
  font-family: var(--font-pixel);
}
.cl {
  font-size: 10px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.end {
  font-size: 12px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.tier {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.lbl {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.lv {
  font-size: 12px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.cav {
  display: flex;
  gap: 0.45rem;
  align-items: flex-start;
  font-size: 0.66rem;
  line-height: 1.35;
  color: var(--ink-2);
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--hair);
  border-radius: 10px;
  padding: 0.35rem 0.6rem;
  margin-top: 0.15rem;
}
.ico {
  flex: none;
  width: 1rem;
  height: 1rem;
  color: var(--naruto);
  margin-top: 0.05rem;
}
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem 0.9rem;
  font-size: 0.64rem;
  color: var(--ink-2);
  margin-top: 0.15rem;
}
.legend span {
  display: inline-flex;
  align-items: center;
}
.ln {
  display: inline-block;
  width: 14px;
  height: 2.5px;
  border-radius: 2px;
  margin-right: 0.35rem;
}
.ring {
  display: inline-block;
  box-sizing: border-box;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: transparent;
  border: 1.5px solid var(--ink-2);
  margin-right: 0.35rem;
}
</style>
