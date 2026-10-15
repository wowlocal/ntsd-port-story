<script setup lang="ts">
// Chapter 18, PHONE_CONTROLLER C1: why the first iPhone run stopped at the menu's first blit. The iPhone
// told the game its 874x402-point screen, lower than the original's 794x550 window; the host now tells a
// screen scaled up to at least 800x600 (as Android does) and fits the picture: on the iPhone 17 Pro
// screenshot (2622x1206 px) the picture is 1742x1206 px, centred. Data: data/rel_controller.json.
import ctl from '../data/rel_controller.json'

const ip = (ctl as any).iphone
const [sw, sh] = ip.screenPt as [number, number]
const [ww, wh] = ip.window as [number, number]
const shot = ip.screenshots[0]
const W = 440
const k = 0.17
const top = 22
const scr = { w: sw * k, h: sh * k }
const win = { w: ww * k, h: wh * k }
const H = top + win.h + 36
const p1 = 4
const p2 = 236
const k2 = scr.w / shot.screen[0]
const s2 = { w: shot.screen[0] * k2, h: shot.screen[1] * k2 }
const b2 = { x: shot.box[0] * k2, w: shot.boxSize[0] * k2, h: shot.boxSize[1] * k2 }
const midY = top + win.h / 2
const nf = new Intl.NumberFormat('ru-RU')
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`Экран iPhone ${sw}×${sh} точек ниже окна игры ${ww}×${wh}; после правки картинка вписана: ${shot.boxSize[0]}×${shot.boxSize[1]} пикселей`">
    <text class="h" :x="p1" y="11">первый прогон</text>
    <rect :x="p1" :y="midY - scr.h / 2" :width="scr.w" :height="scr.h" rx="9" fill="var(--surface-3)" stroke="var(--axis)" />
    <rect :x="p1 + (scr.w - win.w) / 2" :y="top" :width="win.w" :height="win.h" fill="none" stroke="var(--critical)" stroke-width="1.5" />
    <text class="t" :x="p1 + scr.w / 2" :y="midY - 3" text-anchor="middle">окно {{ ww }}×{{ wh }}</text>
    <text class="t" :x="p1 + scr.w / 2" :y="midY + 10" text-anchor="middle">экран {{ sw }}×{{ sh }} pt</text>
    <text class="c" :x="p1" :y="top + win.h + 15"><tspan class="x">✕</tspan> {{ ip.firstRunStopped }} из {{ ip.scenarios }} сценариев встали</text>
    <text class="c" :x="p1" :y="top + win.h + 28">на первом blit меню</text>

    <text class="h" :x="p2" y="11">после правки · iPhone 17 Pro</text>
    <rect :x="p2" :y="midY - s2.h / 2" :width="s2.w" :height="s2.h" rx="9" fill="#05070b" stroke="var(--axis)" />
    <rect :x="p2 + b2.x" :y="midY - s2.h / 2" :width="b2.w" :height="b2.h" fill="var(--s1)" style="opacity: 0.55" />
    <text class="t" :x="p2 + s2.w / 2" :y="midY + 4" text-anchor="middle">{{ shot.boxSize[0] }}×{{ shot.boxSize[1] }} px</text>
    <text class="c" :x="p2" :y="top + win.h + 15"><tspan class="ok">✓</tspan> {{ ip.scenarios }} из {{ ip.scenarios }} сценариев,</text>
    <text class="c" :x="p2" :y="top + win.h + 28">{{ nf.format(ip.frames) }} кадров = Mac</text>
  </svg>
</template>

<style scoped>
.h { font-size: 10.5px; fill: var(--muted); font-family: var(--font-sans); }
.t { font-size: 10px; fill: var(--ink); font-family: var(--font-sans); }
.c { font-size: 10.5px; fill: var(--ink-2); font-family: var(--font-sans); }
.x { fill: var(--critical); font-weight: 700; }
.ok { fill: var(--good); font-weight: 700; }
</style>
