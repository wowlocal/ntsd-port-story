<script setup lang="ts">
// One increment of the MEMORY_LOADING loop as the card defines it (docs/research/MEMORY_LOADING.md: Plan, Gates,
// Method notes), drawn as a cycle of six stages, with the night's own counts on each stage.
// `stepwise`: stages appear with the slide's clicks 1..6 (export shows all).
// Data: data/loading_steps.json, data/loading_method.json, data/loading_night.json (scripts/collect_loading.py).
import { computed } from 'vue'
import { useNav, useSlideContext } from '@slidev/client'
import steps from '../data/loading_steps.json'
import method from '../data/loading_method.json'
import night from '../data/loading_night.json'

const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const shown = (k: number) => !props.stepwise || nav.isPrintMode.value || ($clicks?.value ?? 0) >= k

const S = (steps as any).steps as any[]
const M = method as any
const N = night as any
const count = (st: string) => S.filter(s => s.status === st).length
const stages = computed(() => [
  { n: 1, icon: 'i-pixelarticons-search', name: 'профиль', rule: 'сначала замер: simpleperf на A12, sample на Mac', fact: 'загрузка — 131 из 135 с на CPU' },
  { n: 2, icon: 'i-pixelarticons-zap', name: 'механизм', rule: 'одно изменение на ступень; данные игры не трогать', fact: `${S.length} ступеней за ночь` },
  { n: 3, icon: 'i-pixelarticons-eye', name: 'ревью', rule: 'отдельный агент, только чтение, до гейта', fact: `${M.reviews} ревью · ${M.reviewsFound.length} замечаний по сути` },
  { n: 4, icon: 'i-pixelarticons-checkbox', name: 'гейт', rule: '10 сценариев = эталонам, кадры побайтно, AppKit, эмулятор, сьюты', fact: 'A/B: A12 3 + 2, Mac 3 + 3 прогона' },
  { n: 5, icon: 'i-pixelarticons-git-commit', name: 'решение', rule: 'коммит, только если быстрее или меньше и ничего не хуже', fact: `${count('done')} принято · ${count('rejected')} откат · ${count('held')} ждёт · ${count('parked')} отложено` },
  { n: 6, icon: 'i-pixelarticons-list', name: 'журнал', rule: 'строка в карточке и evidence-файл — и даже для отката', fact: `${N.counts.commits} коммитов, ${N.counts.tagged} с меткой` },
])
// cycle layout: 1 2 3 on top (left to right), 4 5 6 below (right to left)
const dir = (n: number) => ({ 1: 'r', 2: 'r', 3: 'd', 4: 'l', 5: 'l', 6: 'u' } as Record<number, string>)[n]
const pos = (n: number) => (n <= 3 ? { col: n, row: 1 } : { col: 7 - n, row: 2 })
</script>

<template>
  <div class="loop">
    <div v-for="s in stages" :key="s.n" class="st" :class="{ off: !shown(s.n) }" :style="{ gridColumn: pos(s.n).col, gridRow: pos(s.n).row }">
      <div class="top">
        <span class="n pixel">{{ s.n }}</span>
        <span :class="s.icon" class="ic" />
        <span class="nm">{{ s.name }}</span>
      </div>
      <div class="rule">
        {{ s.rule }}
      </div>
      <div class="fact">
        {{ s.fact }}
      </div>
      <svg class="arr" :class="dir(s.n)" viewBox="0 0 20 12" aria-hidden="true">
        <path d="M0,6 H14" stroke="var(--naruto)" stroke-width="2" />
        <path d="M12,1 L19,6 L12,11 z" fill="var(--naruto)" />
      </svg>
    </div>
  </div>
</template>

<style scoped>
.loop {
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 1fr 1fr;
  column-gap: 22px;
  row-gap: 22px;
  height: 300px;
}
.arr {
  position: absolute;
  width: 18px;
  height: 11px;
}
.arr.r {
  right: -20px;
  top: 50%;
  margin-top: -5px;
}
.arr.l {
  left: -20px;
  top: 50%;
  margin-top: -5px;
  transform: rotate(180deg);
}
.arr.d {
  bottom: -17px;
  left: 50%;
  margin-left: -9px;
  transform: rotate(90deg);
}
.arr.u {
  top: -17px;
  left: 50%;
  margin-left: -9px;
  transform: rotate(-90deg);
}
.st {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.5rem 0.7rem 0.55rem;
  display: flex;
  flex-direction: column;
  transition: opacity 0.35s ease, transform 0.35s ease;
}
.st.off {
  opacity: 0;
  transform: translateY(6px);
}
.top {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}
.n {
  font-size: 0.85rem;
  color: var(--naruto);
}
.ic {
  width: 0.95rem;
  height: 0.95rem;
  color: var(--ink-2);
}
.nm {
  font-size: 0.9rem;
  font-weight: 650;
  color: var(--ink);
}
.rule {
  font-size: 0.7rem;
  line-height: 1.3;
  color: var(--ink-2);
  margin-top: 0.2rem;
  flex: 1;
}
.fact {
  font-size: 0.7rem;
  line-height: 1.25;
  color: var(--ink);
  font-weight: 600;
  border-top: 1px solid var(--grid);
  padding-top: 0.2rem;
  margin-top: 0.2rem;
}
</style>
