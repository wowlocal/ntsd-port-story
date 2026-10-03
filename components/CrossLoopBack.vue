<script setup lang="ts">
import { computed } from 'vue'
import { useNav, useSlideContext } from '@slidev/client'

// A return arrow under a <Pipeline>: from the last step back up to the first one (the next iteration).
// It mirrors Pipeline's grid (`steps` equal columns, `gap` between them), so the legs sit under the
// centres of the first and last cards. `at` reveals it on that click; export and print always show it.
const props = withDefaults(defineProps<{ steps: number, label?: string, at?: number, gap?: string }>(), { gap: '1.1rem' })
const { $clicks } = useSlideContext()
const nav = useNav()
const shown = computed(() => props.at === undefined || nav.isPrintMode.value || ($clicks?.value ?? 0) >= props.at)
const inset = computed(() => `calc((100% - ${props.steps - 1} * ${props.gap}) / ${2 * props.steps})`)
</script>

<template>
  <div class="back" :class="{ off: !shown }" :style="{ '--inset': inset }">
    <div class="u" />
    <svg class="head" viewBox="0 0 12 10"><path d="M1 9 L6 2 L11 9" fill="none" stroke="var(--naruto)" stroke-width="2" /></svg>
    <div v-if="label" class="lab mono">
      {{ label }}
    </div>
  </div>
</template>

<style scoped>
.back {
  position: relative;
  height: 2.6rem;
  margin-top: 0.2rem;
  transition: opacity 0.35s ease, transform 0.35s ease;
}
.off {
  opacity: 0;
  transform: translateY(6px);
}
.u {
  position: absolute;
  left: var(--inset);
  right: var(--inset);
  top: 0.15rem;
  height: 1.15rem;
  border: 2px solid var(--naruto);
  border-top: 0;
  border-radius: 0 0 10px 10px;
}
.head {
  position: absolute;
  left: calc(var(--inset) - 5px);
  top: -0.2rem;
  width: 12px;
  height: 10px;
}
.lab {
  position: absolute;
  left: 0;
  right: 0;
  top: 1.55rem;
  text-align: center;
  font-size: 0.64rem;
  color: var(--naruto);
  white-space: nowrap;
}
</style>
