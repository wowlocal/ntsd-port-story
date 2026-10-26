<script setup lang="ts">
// Demo-day deck: the five-part arc the organisers ask for, with the current part lit.
// Sits in the top right corner of a slide; `at` is the part's key.
const props = defineProps<{ at: 'problem' | 'solution' | 'demo' | 'results' | 'lessons' }>()
const parts = [
  { key: 'problem', label: 'проблема и контекст' },
  { key: 'solution', label: 'решение' },
  { key: 'demo', label: 'демо' },
  { key: 'results', label: 'результаты' },
  { key: 'lessons', label: 'уроки' },
]
const idx = parts.findIndex(p => p.key === props.at)
</script>

<template>
  <div class="phase" role="img" :aria-label="`часть доклада: ${parts[idx]?.label}`">
    <span v-for="(p, i) in parts" :key="p.key" class="ph" :class="{ done: i < idx, now: i === idx }">
      <i />{{ p.label }}
    </span>
  </div>
</template>

<style scoped>
.phase { position: absolute; top: 1.15rem; right: 3rem; display: flex; gap: 0.7rem; font-family: var(--font-pixel); font-size: 0.6rem; letter-spacing: 0.04em; color: var(--muted); z-index: 2; }
.ph { display: inline-flex; align-items: center; gap: 0.3rem; }
.ph i { display: inline-block; width: 14px; height: 4px; background: rgba(255, 255, 255, 0.12); }
.ph.done i { background: rgba(255, 138, 61, 0.45); }
.ph.now { color: var(--naruto); }
.ph.now i { background: var(--naruto); box-shadow: 0 0 8px rgba(255, 138, 61, 0.6); }
</style>
