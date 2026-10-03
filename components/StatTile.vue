<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'

const props = withDefaults(defineProps<{
  value: number | string
  label: string
  sub?: string
  suffix?: string
  prefix?: string
  decimals?: number
  accent?: string
  size?: 'md' | 'lg' | 'sm'
}>(), {
  decimals: 0,
  size: 'md',
})

const nav = useNav()
const active = useIsSlideActive()
const shown = ref<number>(typeof props.value === 'number' ? 0 : 0)
const isNumber = computed(() => typeof props.value === 'number')

const fmt = computed(() => new Intl.NumberFormat('ru-RU', {
  minimumFractionDigits: props.decimals,
  maximumFractionDigits: props.decimals,
}))

const text = computed(() => {
  if (!isNumber.value)
    return String(props.value)
  return fmt.value.format(shown.value)
})

let raf = 0
function run() {
  if (!isNumber.value)
    return
  const target = props.value as number
  if (nav.isPrintMode.value) {
    shown.value = target
    return
  }
  cancelAnimationFrame(raf)
  const start = performance.now()
  const dur = 1100
  const tick = (t: number) => {
    const k = Math.min(1, (t - start) / dur)
    const e = 1 - (1 - k) ** 3
    shown.value = target * e
    if (k < 1)
      raf = requestAnimationFrame(tick)
    else
      shown.value = target
  }
  raf = requestAnimationFrame(tick)
}

onMounted(() => {
  if (active.value || nav.isPrintMode.value)
    run()
  else if (isNumber.value)
    shown.value = props.value as number
})
watch(active, (v) => {
  if (v)
    run()
})
</script>

<template>
  <div class="tile" :class="size" :style="accent ? { '--tile-accent': accent } : undefined">
    <div class="label">
      {{ label }}
    </div>
    <div class="value">
      <span v-if="prefix" class="affix">{{ prefix }}</span>{{ text }}<span v-if="suffix" class="affix">{{ suffix }}</span>
    </div>
    <div v-if="sub" class="sub">
      {{ sub }}
    </div>
  </div>
</template>

<style scoped>
.tile {
  --tile-accent: var(--naruto);
  position: relative;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 14px;
  padding: 0.75rem 0.95rem 0.8rem;
  overflow: hidden;
}
.tile::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 3px;
  width: 42px;
  background: var(--tile-accent);
}
.label {
  font-size: 0.72rem;
  color: var(--muted);
  line-height: 1.25;
}
.value {
  font-family: var(--font-sans);
  font-weight: 650;
  font-size: 1.85rem;
  line-height: 1.1;
  margin-top: 0.3rem;
  color: var(--ink);
  letter-spacing: -0.01em;
  white-space: nowrap;
}
.lg .value {
  font-size: 2.6rem;
}
.sm .value {
  font-size: 1.35rem;
}
.affix {
  font-size: 0.6em;
  font-weight: 500;
  color: var(--ink-2);
  margin: 0 0.12em;
}
.sub {
  font-size: 0.7rem;
  color: var(--ink-2);
  margin-top: 0.25rem;
  line-height: 1.3;
}
</style>
