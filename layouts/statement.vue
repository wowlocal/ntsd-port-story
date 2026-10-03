<script setup lang="ts">
// A breathing slide between chapters: one big figure or phrase, a kicker above and the slot as caption.
// `big` is the figure ("58 / 58", or a bare number); leave it out to make the slot itself the statement.
const props = withDefaults(defineProps<{
  big?: string | number
  kicker?: string
  image?: string
  shade?: number
  accent?: string
}>(), { shade: 0.86, accent: 'var(--naruto)' })
// `big: 0` arrives as the number 0, which must still render.
const hasBig = () => props.big !== undefined && props.big !== null && props.big !== ''
</script>

<template>
  <div class="slidev-layout statement">
    <div v-if="image" class="bg" :style="{ backgroundImage: `url(${image})` }" />
    <div class="shade" :style="{ '--shade': shade }" />
    <div class="inner">
      <div v-if="kicker" class="kicker pixel">
        <i />{{ kicker }}
      </div>
      <div v-if="hasBig()" class="big" :style="{ color: accent }">
        {{ big }}
      </div>
      <div class="cap" :class="{ solo: !hasBig() }">
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped>
.statement {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  text-align: center;
}
.bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  image-rendering: pixelated;
}
.shade {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, rgba(10, 13, 19, calc(var(--shade) - 0.12)) 0%, rgba(10, 13, 19, var(--shade)) 70%);
}
.inner {
  position: relative;
  max-width: 44rem;
}
.kicker {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--naruto);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.kicker i {
  width: 10px;
  height: 10px;
  background: var(--naruto);
  box-shadow: 3px 3px 0 rgba(255, 138, 61, 0.35);
}
.big {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 7.2rem;
  line-height: 1;
  letter-spacing: -0.02em;
  margin: 0.6rem 0 0.9rem;
  text-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
  font-variant-numeric: tabular-nums;
}
.cap {
  font-size: 1.15rem;
  line-height: 1.45;
  color: var(--ink-2);
}
.cap :deep(b),
.cap :deep(strong) {
  color: var(--ink);
}
.cap.solo {
  font-family: var(--font-display);
  font-size: 2.6rem;
  line-height: 1.12;
  color: var(--ink);
  margin-top: 0.6rem;
}
.cap :deep(p) {
  margin: 0.3rem 0;
}
</style>
