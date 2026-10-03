<script setup lang="ts">
defineProps<{ color?: string }>()
</script>

<template>
  <div class="kicker pixel" :style="color ? { color } : undefined">
    <span class="sq" />
    <slot />
  </div>
</template>

<style scoped>
.kicker {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--naruto);
  margin-bottom: 0.45rem;
}
.sq {
  width: 8px;
  height: 8px;
  background: currentColor;
  box-shadow: 3px 3px 0 rgba(255, 255, 255, 0.12);
}
</style>
