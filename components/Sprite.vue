<script setup lang="ts">
withDefaults(defineProps<{ src: string; scale?: number; float?: boolean; flip?: boolean; alt?: string }>(), {
  scale: 2,
  float: false,
  flip: false,
  alt: '',
})
</script>

<template>
  <img
    :src="src"
    :alt="alt"
    class="sprite"
    :class="{ float }"
    :style="{ zoom: scale, transform: flip ? 'scaleX(-1)' : undefined }"
  >
</template>

<style scoped>
.sprite {
  image-rendering: pixelated;
  display: inline-block;
  filter: drop-shadow(0 6px 10px rgba(0, 0, 0, 0.45));
}
.float {
  animation: float 3.2s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { translate: 0 0; }
  50% { translate: 0 -5px; }
}
</style>
