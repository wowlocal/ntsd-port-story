<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{ value: number, label: string, sub?: string, display?: string }>(), {})
const pct = computed(() => Math.max(0, Math.min(1, props.value)) * 100)
</script>

<template>
  <div class="meter">
    <div class="row">
      <span class="label">{{ label }}</span>
      <span class="val">{{ display ?? `${pct.toFixed(1).replace('.', ',')} %` }}</span>
    </div>
    <div class="track">
      <div class="fill" :style="{ width: `${pct}%` }" />
    </div>
    <div v-if="sub" class="sub">
      {{ sub }}
    </div>
  </div>
</template>

<style scoped>
.meter {
  margin: 0.55rem 0;
}
.row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 1rem;
}
.label {
  font-size: 0.8rem;
  color: var(--ink);
  flex: 1;
  line-height: 1.25;
}
.val {
  font-weight: 650;
  font-size: 1.15rem;
  color: var(--ink);
  white-space: nowrap;
}
.track {
  height: 10px;
  border-radius: 5px;
  background: #184f95;
  margin-top: 0.3rem;
  overflow: hidden;
}
.fill {
  height: 100%;
  background: #6da7ec;
  border-radius: 5px 4px 4px 5px;
}
.sub {
  font-size: 0.66rem;
  color: var(--muted);
  margin-top: 0.25rem;
  line-height: 1.3;
}
</style>
