<script setup lang="ts">
import { computed } from 'vue'
import data from '../data/engine_frames.json'

// The decoded DAT text of one frame, lightly highlighted: block names, keys, numbers, odd values.
const props = defineProps<{ id: number, odd?: string[] }>()
const raw = computed(() => ((data as any).frames.find((f: any) => f.id === props.id)?.raw ?? '') as string)
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
const html = computed(() => {
  const oddSet = new Set(props.odd ?? [])
  return raw.value.split('\n').map((line) => {
    let s = esc(line)
    s = s.replace(/(&lt;frame&gt;|&lt;frame_end&gt;)/g, '<span class="tag">$1</span>')
    s = s.replace(/\b(bdy|itr|wpoint|cpoint|opoint)(_end)?:/g, '<span class="blk">$1$2:</span>')
    s = s.replace(/\b([a-zA-Z_]+):(\s*)(-?\d+)/g, (_m, k, sp, v) => {
      const cls = oddSet.has(v) ? 'odd' : 'num'
      return `<span class="key">${k}:</span>${sp}<span class="${cls}">${v}</span>`
    })
    return s
  }).join('\n')
})
</script>

<template>
  <pre class="dat" v-html="html" />
</template>

<style scoped>
.dat {
  margin: 0;
  font-family: var(--font-mono);
  font-size: 0.6rem;
  line-height: 1.5;
  background: #0c1017;
  border: 1px solid var(--hair);
  border-radius: 10px;
  padding: 0.6rem 0.75rem;
  color: var(--ink-2);
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
.dat :deep(.tag) {
  color: #febc2e;
}
.dat :deep(.blk) {
  color: #ff8a3d;
  font-weight: 700;
}
.dat :deep(.key) {
  color: var(--muted);
}
.dat :deep(.num) {
  color: var(--ink);
}
.dat :deep(.odd) {
  color: #0a0d13;
  background: #ff8a3d;
  border-radius: 3px;
  padding: 0 0.15rem;
  font-weight: 700;
}
</style>
