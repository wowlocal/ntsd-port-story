<script setup lang="ts">
// Chapter 8: the Stage ENDING screen (menu 300, 437220; STAGE_ENDING.md, 996d2c0e), drawn from the EXE's own
// ENDING bitmap resource (public/img/screens/ending-sheet.png, cut from NTSD 2.4.exe unchanged). Frames are the
// static rectangles 424b45..424c98 write at startup. Each page opens over 13 frames: thirteen black bands
// 13 px apart, each 13 − n high; while it is open the arrow (frame 5) blinks at the page's lower-right corner;
// Attack closes it the same way. Easy and Normal (450c30 = 2, 1) show frame 0 and skip frame 1; Difficult and
// CRAZY! show frame 1 instead. After the fourth page the menu is 10. The animation's pace is ours, not a
// measurement; export shows the first page open.
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'

const frames = [
  [0, 0, 402, 66],
  [0, 67, 402, 91],
  [0, 159, 402, 156],
  [0, 316, 419, 169],
  [0, 486, 419, 65],
]
const arrow = [403, 53, 15, 13]
const S = 0.74
const BW = 346
const BH = 150

const nav = useNav()
const active = useIsSlideActive()
const hard = ref(false)
const order = computed(() => hard.value ? [1, 2, 3, 4] : [0, 2, 3, 4])
const page = ref(0)
const band = ref(0) // 0 = fully open, 13 = fully closed
const tick = ref(0)
const atMenu = ref(false)

const f = computed(() => frames[order.value[page.value]])
const px = computed(() => Math.round((BW - f.value[2] * S) / 2))
const py = computed(() => Math.round((BH - 12 - f.value[3] * S) / 2))
const pageStyle = computed(() => ({
  left: `${px.value}px`,
  top: `${py.value}px`,
  width: `${f.value[2] * S}px`,
  height: `${f.value[3] * S}px`,
  backgroundSize: `${419 * S}px ${552 * S}px`,
  backgroundPosition: `-${f.value[0] * S}px -${f.value[1] * S}px`,
}))
const arrowStyle = computed(() => ({
  left: `${px.value + f.value[2] * S}px`,
  top: `${py.value + f.value[3] * S}px`,
  width: `${arrow[2] * S}px`,
  height: `${arrow[3] * S}px`,
  backgroundSize: `${419 * S}px ${552 * S}px`,
  backgroundPosition: `-${arrow[0] * S}px -${arrow[1] * S}px`,
}))
const bands = computed(() => Array.from({ length: 13 }, (_, i) => ({ top: py.value + i * 13 * S, h: band.value * S })))
const arrowOn = computed(() => band.value === 0 && tick.value % 10 < 5)

let timer = 0
let phase: 'open' | 'hold' | 'close' | 'menu' = 'open'
let held = 0
function step() {
  tick.value++
  if (phase === 'open') {
    band.value = Math.max(0, band.value - 1)
    if (band.value === 0) { phase = 'hold'; held = 0 }
  }
  else if (phase === 'hold') {
    if (++held > 52) phase = 'close'
  }
  else if (phase === 'close') {
    band.value = Math.min(13, band.value + 1)
    if (band.value === 13) {
      if (page.value === 3) { phase = 'menu'; held = 0; atMenu.value = true }
      else { page.value++; phase = 'open' }
    }
  }
  else if (++held > 30) {
    atMenu.value = false
    page.value = 0
    phase = 'open'
  }
}
function stop() {
  clearInterval(timer)
  timer = 0
}
function reset() {
  stop()
  page.value = 0
  atMenu.value = false
  if (nav.isPrintMode.value || !active.value) {
    band.value = 0
    return
  }
  band.value = 13
  phase = 'open'
  timer = window.setInterval(step, 40)
}
watch([active, hard], reset, { immediate: true })
onBeforeUnmount(stop)
</script>

<template>
  <div class="en">
    <div class="scr" :style="{ width: `${BW}px`, height: `${BH}px` }">
      <template v-if="!atMenu">
        <div class="pg" :style="pageStyle" />
        <div v-if="arrowOn" class="pg" :style="arrowStyle" />
        <div v-for="(b, i) in bands" :key="i" class="band" :style="{ top: `${b.top}px`, height: `${b.h}px` }" />
      </template>
      <div v-else class="menu pixel">
        menu = 10 · главное меню
      </div>
      <div class="cap mono">
        стр. {{ page + 1 }} из 4 · кадр {{ order[page] }}
      </div>
    </div>
    <div class="tog">
      <span class="muted">сложность:</span>
      <button :class="{ on: !hard }" @click="hard = false">
        Easy · Normal
      </button>
      <button :class="{ on: hard }" @click="hard = true">
        Difficult · CRAZY!
      </button>
    </div>
  </div>
</template>

<style scoped>
.en { display: flex; flex-direction: column; align-items: center; gap: 0.3rem; }
.scr { position: relative; background: #000; border: 1px solid var(--hair); border-radius: 8px; overflow: hidden; box-shadow: 0 8px 26px rgba(0, 0, 0, 0.45); }
.pg { position: absolute; background-image: url('/img/screens/ending-sheet.png'); background-repeat: no-repeat; }
.band { position: absolute; left: 0; right: 0; background: #000; }
.menu { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 0.72rem; color: var(--naruto); }
.cap { position: absolute; left: 0; right: 0; bottom: 3px; text-align: center; font-size: 0.5rem; color: var(--muted); }
.tog { display: flex; align-items: center; gap: 0.35rem; font-size: 0.56rem; }
.tog button { font-family: var(--font-mono); font-size: 0.54rem; color: var(--ink-2); background: var(--surface); border: 1px solid var(--hair); border-radius: 999px; padding: 0.06rem 0.5rem; cursor: pointer; }
.tog button.on { color: var(--ink); border-color: var(--naruto); }
</style>
