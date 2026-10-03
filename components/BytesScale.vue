<script setup lang="ts">
import { computed } from 'vue'
import comp from '../data/composition.json'

// one square = 1 MB of tracked files at HEAD
const MB = 1e6
const groups = computed(() => [
  { key: 'native-code', label: 'Swift-код порта (игра + тесты)', color: 'var(--s2)', mb: (comp as any)['native-code'].bytes / MB },
  { key: 'tools', label: 'Python-инструменты и оракулы', color: 'var(--s3)', mb: (comp as any).tools.bytes / MB },
  { key: 'docs', label: 'карточки исследований + evidence', color: 'var(--s4)', mb: ((comp as any).research.bytes + (comp as any).evidence.bytes) / MB },
  { key: 'test-fixtures', label: 'эталонные трассы оригинала (fixtures)', color: 'var(--s1)', mb: (comp as any)['test-fixtures'].bytes / MB },
])
const cols = 168
const size = 3.9
const pitch = 5
const squares = computed(() => {
  const out: { x: number, y: number, c: string, k: string }[] = []
  let i = 0
  for (const g of groups.value) {
    const n = Math.max(1, Math.round(g.mb))
    for (let j = 0; j < n; j++, i++)
      out.push({ x: (i % cols) * pitch, y: Math.floor(i / cols) * pitch, c: g.color, k: g.key })
  }
  return out
})
const rows = computed(() => Math.ceil(squares.value.length / cols))
const W = cols * pitch
const H = computed(() => rows.value * pitch)
const fmt = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 1 })
</script>

<template>
  <div class="wrap">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Объём файлов: 1 квадрат = 1 МБ">
      <rect v-for="(s, i) in squares" :key="i" :x="s.x" :y="s.y" :width="size" :height="size" rx="1" :fill="s.c" />
    </svg>
    <div class="legend">
      <div v-for="g in groups" :key="g.key" class="item">
        <i class="swatch" :style="{ background: g.color }" />
        <span class="v">{{ fmt.format(g.mb) }} МБ</span>
        <span class="l">{{ g.label }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.legend {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.6rem;
  margin-top: 0.55rem;
}
.item {
  font-size: 0.7rem;
  color: var(--ink-2);
  line-height: 1.25;
}
.v {
  font-weight: 700;
  color: var(--ink);
  font-size: 0.95rem;
  margin-right: 0.3rem;
}
.l {
  display: block;
  margin-top: 0.1rem;
}
</style>
