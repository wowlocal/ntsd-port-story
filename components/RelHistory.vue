<script setup lang="ts">
// Chapter 18, MENU_MEMORY cause: every menu iteration's whole cursor (its requests and replies, a receipt
// array of ≈12 KB) was kept because the display replies retain the surfaces they drew — the same few
// surfaces every frame. After 340b1a64 each resource is kept once and the iterations are only counted.
// The counter runs 138 -> 4404 (the macOS heap snapshots 140 s apart) when the slide opens.
// Data: data/rel_memory.json (scripts/collect_release.py).
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'
import mem from '../data/rel_memory.json'

const d = mem as any
const nav = useNav()
const active = useIsSlideActive()
const isPrint = computed(() => nav.isPrintMode.value)
const n0 = d.mac.nodesFrom as number
const n1 = d.mac.nodesTo as number
const kb = d.receipt.kbEach as number
const n = ref(isPrint.value ? n1 : n0)
const nf = new Intl.NumberFormat('ru-RU')

let raf = 0
function run() {
  cancelAnimationFrame(raf)
  if (isPrint.value) {
    n.value = n1
    return
  }
  const start = performance.now()
  const dur = 4200
  const tick = (now: number) => {
    const k = Math.min(1, (now - start) / dur)
    n.value = Math.round(n0 + (n1 - n0) * k)
    if (k < 1)
      raf = requestAnimationFrame(tick)
  }
  raf = requestAnimationFrame(tick)
}
onMounted(() => (active.value || isPrint.value) && run())
watch(active, v => v && run())
watch(isPrint, p => p && run())
onBeforeUnmount(() => cancelAnimationFrame(raf))

const W = 520
const H = 250
const cards = 5
const cw = 46
const ch = 40
const gap = 8
const x0 = 6
const cardX = (i: number) => x0 + i * (cw + gap)
const yB = 34 // before row
const yA = 168 // after row
const sx = 420 // surfaces column
const surf = [{ y: 70, l: 'поверхность' }, { y: 104, l: 'поверхность' }, { y: 138, l: 'поверхность' }]
const sw = 92
const sh = 26
const mbPer = d.receipt.mb / d.receipt.count // 54 MB for 4406 cursors on macOS
const mb = computed(() => n.value * mbPer)
const labels = computed(() => Array.from({ length: cards }, (_, i) => n.value - (cards - 1 - i)))
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`До правки: ${n1} курсоров по ≈${kb} КБ держат одни и те же поверхности; после: каждая поверхность один раз и счётчик итераций`">
    <!-- the surfaces both rows keep alive -->
    <g v-for="(s, i) in surf" :key="i">
      <rect :x="sx" :y="s.y" :width="sw" :height="sh" rx="6" fill="var(--surface-3)" stroke="var(--axis)" />
      <text class="sl" :x="sx + sw / 2" :y="s.y + 17" text-anchor="middle">{{ s.l }} {{ i + 1 }}</text>
    </g>
    <text class="cap" :x="sx + sw / 2" :y="surf[0].y - 20" text-anchor="middle">одни и те же</text>
    <text class="cap" :x="sx + sw / 2" :y="surf[0].y - 8" text-anchor="middle">каждый кадр</text>

    <!-- before: a growing chain of whole cursors -->
    <text class="rowt" :x="x0" y="14">до правки — каждая итерация меню хранится целиком</text>
    <g v-for="(lab, i) in labels" :key="`c${i}`">
      <path v-for="(s, j) in surf" :key="j" :d="`M${cardX(i) + cw / 2},${yB + ch} C${cardX(i) + cw / 2},${yB + ch + 34} ${sx - 40},${s.y + sh / 2} ${sx},${s.y + sh / 2}`" class="lnk b" />
      <rect :x="cardX(i)" :y="yB" :width="cw" :height="ch" rx="5" fill="var(--s2)" :style="{ opacity: 0.55 + 0.45 * (i / (cards - 1)) }" />
      <text class="cn" :x="cardX(i) + cw / 2" :y="yB + 17" text-anchor="middle">#{{ nf.format(lab) }}</text>
      <text class="ck" :x="cardX(i) + cw / 2" :y="yB + 31" text-anchor="middle">≈{{ kb }} КБ</text>
    </g>
    <text class="tot" :x="cardX(cards) - 2" :y="yB + 17">курсоров: <tspan class="v">{{ nf.format(n) }}</tspan></text>
    <text class="tot" :x="cardX(cards) - 2" :y="yB + 32">≈ <tspan class="v">{{ Math.round(mb) }} МБ</tspan> квитанций</text>

    <!-- after: each resource once, plus a count -->
    <line :x1="x0" :x2="W - 4" :y1="yA - 26" :y2="yA - 26" stroke="var(--grid)" />
    <text class="rowt" :x="x0" :y="yA - 10">после 340b1a64 — каждый ресурс один раз</text>
    <rect :x="x0" :y="yA" width="214" :height="ch" rx="6" fill="var(--s1)" style="opacity: 0.9" />
    <text class="cn" :x="x0 + 10" :y="yA + 17">retained: [поверхность 1, 2, 3]</text>
    <text class="ck" :x="x0 + 10" :y="yA + 31">массив и набор идентичностей</text>
    <path v-for="(s, j) in surf" :key="`a${j}`" :d="`M${x0 + 214},${yA + ch / 2} C${x0 + 300},${yA + ch / 2} ${sx - 50},${s.y + sh / 2} ${sx},${s.y + sh / 2}`" class="lnk a" />
    <text class="tot" :x="x0" :y="yA + 58">итерации только считаются: retainedIterationCount = <tspan class="v">{{ nf.format(n) }}</tspan></text>
  </svg>
</template>

<style scoped>
.rowt { font-size: 11px; fill: var(--ink-2); font-family: var(--font-sans); }
.cap { font-size: 10px; fill: var(--muted); font-family: var(--font-sans); }
.sl { font-size: 10.5px; fill: var(--ink); font-family: var(--font-sans); }
.cn { font-size: 10.5px; font-weight: 650; fill: #fff; font-family: var(--font-mono); }
.ck { font-size: 10px; fill: rgba(255, 255, 255, 0.85); font-family: var(--font-sans); }
.tot { font-size: 11px; fill: var(--ink-2); font-family: var(--font-sans); }
.tot .v { fill: var(--ink); font-weight: 700; font-variant-numeric: tabular-nums; }
.lnk { fill: none; stroke-width: 1; }
.lnk.b { stroke: rgba(217, 89, 38, 0.45); }
.lnk.a { stroke: rgba(57, 135, 229, 0.8); stroke-width: 1.5; }
</style>
