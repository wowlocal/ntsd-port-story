<script setup lang="ts">
const props = withDefaults(defineProps<{
  num?: number
  total?: number
  kicker?: string
  dates?: string
  image?: string
  imagePixel?: boolean
  stats?: string
}>(), {
  num: 1,
  total: 8,
  imagePixel: true,
})
const pad = (n: number) => String(n).padStart(2, '0')
</script>

<template>
  <div class="slidev-layout chapter">
    <div v-if="image" class="bgimg" :class="{ pixelated: imagePixel }" :style="{ backgroundImage: `url(${image})` }" />
    <div class="content">
      <div class="num pixel">
        {{ pad(props.num) }}
      </div>
      <div class="kicker pixel">
        {{ kicker || `Глава ${props.num}` }}<span v-if="dates" class="dates"> · {{ dates }}</span>
      </div>
      <div class="title">
        <slot />
      </div>
      <div v-if="stats" class="stats">
        {{ stats }}
      </div>
    </div>
    <div class="progress">
      <span v-for="i in props.total" :key="i" class="cell" :class="{ done: i < props.num, now: i === props.num }" />
    </div>
  </div>
</template>

<style scoped>
.chapter {
  display: flex;
  align-items: center;
  overflow: hidden;
}
.bgimg {
  position: absolute;
  inset: 0 0 0 38%;
  background-size: cover;
  background-position: center;
  opacity: 0.55;
  mask-image: linear-gradient(90deg, transparent 0%, rgba(0, 0, 0, 0.85) 35%, #000 100%);
}
.content {
  position: relative;
  max-width: 62%;
}
.num {
  font-size: 5.6rem;
  line-height: 0.9;
  color: transparent;
  -webkit-text-stroke: 2px var(--naruto);
  text-shadow: 6px 6px 0 rgba(255, 138, 61, 0.14);
  margin-bottom: 0.6rem;
}
.kicker {
  color: var(--naruto);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 0.85rem;
}
.dates {
  color: var(--ink-2);
}
.title :deep(h1) {
  font-size: 2.5rem;
  line-height: 1.12;
  margin: 0.45rem 0 0.6rem;
}
.title :deep(p) {
  color: var(--ink-2);
  font-size: 1.02rem;
  max-width: 34rem;
}
.stats {
  margin-top: 1rem;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--muted);
}
.progress {
  position: absolute;
  left: 3rem;
  bottom: 1.6rem;
  display: flex;
  gap: 6px;
}
.cell {
  width: 22px;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
}
.cell.done {
  background: rgba(255, 138, 61, 0.45);
}
.cell.now {
  background: var(--naruto);
  box-shadow: 0 0 12px rgba(255, 138, 61, 0.6);
}
</style>
