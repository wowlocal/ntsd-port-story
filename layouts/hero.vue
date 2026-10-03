<script setup lang="ts">
withDefaults(defineProps<{ image?: string, align?: 'left' | 'center', shade?: number }>(), {
  align: 'left',
  shade: 0.92,
})
</script>

<template>
  <div class="slidev-layout hero" :class="align">
    <div v-if="image" class="bg" :style="{ backgroundImage: `url(${image})` }" />
    <div class="shade" :style="{ '--shade': shade }" />
    <div class="inner">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.hero {
  display: flex;
  align-items: center;
  overflow: hidden;
}
.bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center right;
  image-rendering: pixelated;
}
.shade {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(10, 13, 19, var(--shade)) 0%, rgba(10, 13, 19, calc(var(--shade) - 0.1)) 42%, rgba(10, 13, 19, 0.35) 75%, rgba(10, 13, 19, 0.15) 100%),
    linear-gradient(0deg, rgba(10, 13, 19, 0.9) 0%, transparent 35%);
}
.center .shade {
  background: rgba(10, 13, 19, var(--shade));
}
.inner {
  position: relative;
  width: 100%;
}
.center .inner {
  text-align: center;
}
</style>
