<script setup lang="ts">
import { computed } from 'vue'
import cp from '../data/evidence/crossplay-matches.json'

// How many of the equal cross-checked matches each character appeared in (one series, one hue).
const items = computed(() => {
  const a = (cp as any).characterAppearances as Record<string, number>
  const list = Object.entries(a).map(([k, v]) => ({
    name: k.startsWith('Sasori (') ? 'Сасори · скрытый id 51' : k.replace('_', ' '),
    n: v,
    hidden: k.startsWith('Sasori ('),
  }))
  return list.sort((x, y) => y.n - x.n)
})
const max = computed(() => Math.max(...items.value.map(i => i.n)))
</script>

<template>
  <div>
    <div class="head">
      сколько раз персонаж выходил на арену в равных матчах
    </div>
    <div class="grid4">
      <div v-for="it in items" :key="it.name" class="row" :class="{ hidden: it.hidden }">
        <span class="nm">{{ it.name }}</span>
        <span class="tr"><i :style="{ width: `${(it.n / max) * 100}%` }" /></span>
        <span class="v">{{ it.n }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.head {
  font-size: 0.64rem;
  color: var(--muted);
  margin-bottom: 0.3rem;
}
.grid4 {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.1rem 0.9rem;
}
.row {
  display: grid;
  grid-template-columns: 5.6rem 1fr 1.1rem;
  align-items: center;
  gap: 0.35rem;
  height: 15px;
}
.nm {
  font-size: 0.6rem;
  color: var(--ink-2);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.hidden .nm {
  color: var(--naruto);
}
.tr {
  height: 6px;
}
.tr i {
  display: block;
  height: 6px;
  background: var(--s1);
  border-radius: 0 3px 3px 0;
}
.v {
  font-size: 0.6rem;
  color: var(--ink-2);
  text-align: right;
  font-variant-numeric: tabular-nums;
}
</style>
