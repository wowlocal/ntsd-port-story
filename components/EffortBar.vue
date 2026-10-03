<script setup lang="ts">
import { computed } from 'vue'

// One stacked bar: share of model responses per reasoning effort, with counts under it.
const props = defineProps<{ parts: { label: string, n: number, color: string }[] }>()
const total = computed(() => props.parts.reduce((s, p) => s + p.n, 0))
const fmt = new Intl.NumberFormat('ru-RU')
const pct = (n: number) => {
  const v = (n / total.value) * 100
  return v >= 10 ? `${Math.round(v)} %` : `${v.toFixed(1).replace('.', ',')} %`
}
</script>

<template>
  <div>
    <div class="bar">
      <i v-for="p in parts" :key="p.label" :style="{ flexGrow: Math.max(p.n, total * 0.012), background: p.color }" :title="`${p.label}: ${fmt.format(p.n)}`" />
    </div>
    <div class="keys">
      <span v-for="p in parts" :key="p.label"><i class="sw" :style="{ background: p.color }" /><b class="mono">{{ p.label }}</b> {{ fmt.format(p.n) }} · {{ pct(p.n) }}</span>
    </div>
  </div>
</template>

<style scoped>
.bar {
  display: flex;
  gap: 2px;
  height: 12px;
}
.bar i {
  display: block;
  height: 12px;
  flex-basis: 0;
}
.bar i:first-child {
  border-radius: 4px 0 0 4px;
}
.bar i:last-child {
  border-radius: 0 4px 4px 0;
}
.bar i:only-child {
  border-radius: 4px;
}
.keys {
  display: flex;
  flex-wrap: wrap;
  gap: 0.2rem 1rem;
  margin-top: 0.35rem;
  font-size: 0.64rem;
  color: var(--ink-2);
}
.keys b {
  color: var(--ink);
  margin-right: 0.2rem;
}
.sw {
  display: inline-block;
  width: 9px;
  height: 9px;
  border-radius: 2px;
  margin-right: 0.35rem;
  vertical-align: -1px;
}
</style>
