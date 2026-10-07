<script setup lang="ts">
// The three storage steps of 5 Oct, each as its own before/after pair on one GB scale. Steps 1-2 are measured as
// live heap (heap -s), step 3 as resident heap (vmmap): two metrics, so the cards are not joined into one series.
// Data: data/perf_memory.json (scripts/collect_perf.py).
import data from '../data/perf_memory.json'

const steps = (data as any).steps as { n: number, hash: string, what: string, metric: string, before: number, after: number }[]
const text: Record<number, [string, string]> = {
  1: ['Картинка не держит декодированную копию', 'цвета считаются при чтении, файл всё так же проверяется при загрузке'],
  2: ['Маска «known» — бит на пиксель, а не байт', 'учёт бюджета памяти по-прежнему считает пять байт на пиксель'],
  3: ['Поверхность заполняется при первом обращении', 'большинство из 851 спрайтовой поверхности матч не читает никогда'],
}
const metric: Record<string, string> = { 'живая куча': 'живая куча · heap -s', 'резидентная куча': 'резидентная куча · vmmap' }
const W = 252
const H = 58
const l = 42
const MAX = 4.5
const x = (v: number) => l + (v / MAX) * (W - l - 54)
const f = (v: number) => v.toFixed(2).replace(/0$/, '').replace('.', ',')
</script>

<template>
  <div class="steps">
    <div v-for="s in steps" :key="s.n" class="card">
      <div class="top">
        <span class="pixel n">шаг {{ s.n }}</span>
        <code class="h">{{ s.hash }}</code>
      </div>
      <div class="what">
        {{ text[s.n][0] }}
      </div>
      <div class="why">
        {{ text[s.n][1] }}
      </div>
      <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`${s.metric}: ${f(s.before)} ГБ → ${f(s.after)} ГБ`">
        <line :x1="l" :x2="l" y1="4" :y2="H - 6" stroke="var(--axis)" />
        <text x="0" y="20" class="lab">до</text>
        <rect :x="l" y="10" :width="x(s.before) - l" height="14" rx="3" fill="var(--axis)" />
        <text :x="x(s.before) + 6" y="21.5" class="num muted">{{ f(s.before) }} ГБ</text>
        <text x="0" y="43" class="lab">после</text>
        <rect :x="l" y="33" :width="x(s.after) - l" height="14" rx="3" fill="var(--s2)" />
        <text :x="x(s.after) + 6" y="44.5" class="num">{{ f(s.after) }} ГБ</text>
      </svg>
      <div class="foot">
        <span class="delta">−{{ f(s.before - s.after) }} ГБ</span>
        <span class="metric">{{ metric[s.metric] }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.8rem;
}
.card {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 14px;
  padding: 0.65rem 0.85rem 0.6rem;
  overflow: hidden;
}
.card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 3px;
  width: 42px;
  background: var(--s2);
}
.top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.n {
  font-size: 0.78rem;
  color: var(--naruto);
}
.h {
  font-size: 0.64rem !important;
}
.what {
  margin-top: 0.3rem;
  font-size: 0.82rem;
  font-weight: 650;
  line-height: 1.25;
  color: var(--ink);
}
.why {
  margin: 0.2rem 0 0.35rem;
  font-size: 0.66rem;
  line-height: 1.3;
  color: var(--ink-2);
  min-height: 1.7rem;
}
.lab {
  font-size: 10.5px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.num {
  font-size: 11.5px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.num.muted {
  fill: var(--ink-2);
  font-weight: 500;
}
.foot {
  display: flex;
  align-items: baseline;
  gap: 0.55rem;
  margin-top: 0.15rem;
}
.delta {
  white-space: nowrap;
  font-size: 1.05rem;
  font-weight: 650;
  color: var(--ink);
}
.metric {
  font-size: 0.64rem;
  color: var(--muted);
  line-height: 1.2;
}
</style>
