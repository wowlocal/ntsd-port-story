<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'

// Two pictures of the same scene on top of each other; drag the handle to compare them.
// When the slide opens, the handle sweeps once from the "after" side to `start`; export shows `start`.
const props = withDefaults(defineProps<{
  before: string
  after: string
  beforeLabel?: string
  afterLabel?: string
  height?: string
  start?: number
  fit?: 'cover' | 'contain'
  position?: string
  pixelated?: boolean
}>(), { beforeLabel: 'до', afterLabel: 'после', height: '300px', start: 50, fit: 'cover', position: 'center', pixelated: false })

const nav = useNav()
const active = useIsSlideActive()
const pos = ref(props.start)
const box = ref<HTMLElement | null>(null)
let dragging = false
let raf = 0

function setFrom(e: PointerEvent) {
  const r = box.value?.getBoundingClientRect()
  if (!r || r.width === 0)
    return
  pos.value = Math.min(100, Math.max(0, ((e.clientX - r.left) / r.width) * 100))
}
function down(e: PointerEvent) {
  dragging = true
  ;(e.currentTarget as HTMLElement).setPointerCapture?.(e.pointerId)
  setFrom(e)
}
function move(e: PointerEvent) {
  if (dragging)
    setFrom(e)
}
function up() {
  dragging = false
}
function sweep() {
  if (nav.isPrintMode.value) {
    pos.value = props.start
    return
  }
  cancelAnimationFrame(raf)
  const t0 = performance.now()
  const from = 96
  const tick = (t: number) => {
    const k = Math.min(1, (t - t0) / 1400)
    const e = 1 - (1 - k) ** 3
    pos.value = from + (props.start - from) * e
    if (k < 1)
      raf = requestAnimationFrame(tick)
  }
  raf = requestAnimationFrame(tick)
}
watch(active, (v) => {
  if (v)
    sweep()
}, { immediate: true })
onBeforeUnmount(() => cancelAnimationFrame(raf))
</script>

<template>
  <div
    ref="box" class="ba" :style="{ height }"
    @pointerdown="down" @pointermove="move" @pointerup="up" @pointercancel="up"
  >
    <img :src="after" class="img" :class="{ pixelated }" :style="{ objectFit: fit, objectPosition: position }" alt="">
    <img :src="before" class="img top" :class="{ pixelated }" :style="{ objectFit: fit, objectPosition: position, clipPath: `inset(0 ${100 - pos}% 0 0)` }" alt="">
    <div class="line" :style="{ left: `${pos}%` }">
      <div class="knob">
        <svg viewBox="0 0 16 16" width="14" height="14"><path d="M6 3L1 8l5 5M10 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.8" /></svg>
      </div>
    </div>
    <span class="lab l">{{ beforeLabel }}</span>
    <span class="lab r">{{ afterLabel }}</span>
  </div>
</template>

<style scoped>
.ba {
  position: relative;
  overflow: hidden;
  border-radius: 10px;
  border: 1px solid var(--hair);
  background: #000;
  cursor: ew-resize;
  user-select: none;
  touch-action: none;
}
.img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  pointer-events: none;
}
.line {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  margin-left: -1px;
  background: var(--naruto);
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.35);
  pointer-events: none;
}
.knob {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 26px;
  height: 26px;
  margin: -13px 0 0 -13px;
  border-radius: 50%;
  background: var(--naruto);
  color: #1a0d05;
  display: grid;
  place-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}
.lab {
  position: absolute;
  top: 8px;
  font-size: 0.6rem;
  font-weight: 600;
  color: #fff;
  background: rgba(10, 13, 19, 0.78);
  border-radius: 999px;
  padding: 0.1rem 0.55rem;
  pointer-events: none;
}
.lab.l {
  left: 8px;
}
.lab.r {
  right: 8px;
}
</style>
