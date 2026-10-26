<script setup lang="ts">
// Demo-day deck: the same Demo match first in the original, then in the port, cut mid-fight.
// public/media/original-then-port.mp4 is built from the 3 October crosscheck frames
// (X5 goal-100-20261002/crossplay-loop/demo-gif): the original under CrossOver for ticks 150–510, then the Mac app for
// ticks 513–879, 10 frames per second (every 3rd tick, the game's own speed). Frames of both programs at the same tick
// look the same, so the cut is invisible except for the caption. Under the video a strip shows which program is playing.
// Export shows a still with both programs side by side at tick 513 (the cut) instead of the video.
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'

const nav = useNav()
const active = useIsSlideActive()
const video = ref<HTMLVideoElement | null>(null)
const t = ref(0)
const cut = 12.1
const total = 24.4
let raf = 0
function tick() {
  t.value = video.value?.currentTime ?? 0
  raf = requestAnimationFrame(tick)
}
watch(active, (a) => {
  if (!video.value)
    return
  if (a) {
    video.value.currentTime = 0
    video.value.play().catch(() => {})
  }
  else {
    video.value.pause()
  }
})
onMounted(() => { raf = requestAnimationFrame(tick) })
onBeforeUnmount(() => cancelAnimationFrame(raf))
</script>

<template>
  <div class="ho">
    <img v-if="nav.isPrintMode.value" src="/media/original-then-port-pair.jpg" class="still" alt="Слева оригинал, справа порт — тик 513">
    <video v-else ref="video" src="/media/original-then-port.mp4" poster="/media/original-then-port-poster.jpg" muted loop playsinline autoplay class="vid" />
    <div v-if="!nav.isPrintMode.value" class="strip">
      <div class="seg o" :class="{ on: t < cut }" :style="{ width: `${(cut / total) * 100}%` }">оригинал · Windows</div>
      <div class="seg p" :class="{ on: t >= cut }">порт · Swift на macOS</div>
      <span class="head" :style="{ left: `${(t / total) * 100}%` }" />
    </div>
  </div>
</template>

<style scoped>
.ho { display: flex; flex-direction: column; gap: .4rem; align-items: center; }
.vid, .still { display: block; max-height: 22.5rem; max-width: 100%; border-radius: 10px; border: 1px solid var(--hair); image-rendering: pixelated; }
.strip { position: relative; display: flex; width: 100%; max-width: 32.6rem; height: 1.5rem; border-radius: 8px; overflow: hidden; font-size: .66rem; }
.seg { display: flex; align-items: center; justify-content: center; color: var(--ink-2); background: rgba(255, 255, 255, .05); transition: background .2s, color .2s; }
.seg.p { flex: 1; }
.seg.o.on { background: rgba(57, 135, 229, .35); color: var(--ink); }
.seg.p.on { background: rgba(255, 138, 61, .35); color: var(--ink); }
.head { position: absolute; top: 0; bottom: 0; width: 2px; background: var(--ink); }
</style>
