<script setup lang="ts">
// Chapter 19, TOUCH_CONTROLS: StormPixels' on-screen controls as the port took them in.
// A schematic, not a capture: the canvas is the A12's drawn buffer (1223×550, the 794×550 frame in the middle),
// the places are drawn by the card's description (d-pad bottom left, attack/jump/defend bottom right, the F button
// with its 5×2 grid of F1–F9 and ESC, the show/hide toggle), not measured.
// What the buttons pressed (docs/research/TOUCH_CONTROLS.md, change 4): the proposal sent the arrows, A, J and D,
// which in the shipped data/control.txt are Player 2's arrows and Player 1's left, attack and right; the port sends
// Player 1's W S A D and J K L. Sizes (change 7): ~13 mm on an iPhone and ~37 mm on a 13-inch iPad before the
// 48 pt/dp cap, ~13 mm and ~16 mm after.
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'

const nav = useNav()
const active = useIsSlideActive()
const mode = ref<'proposal' | 'port'>(nav.isPrintMode.value ? 'port' : 'proposal')
let timer = 0
watch(active, (a) => {
  clearTimeout(timer)
  if (nav.isPrintMode.value)
    return
  if (a) {
    mode.value = 'proposal'
    timer = window.setTimeout(() => { mode.value = 'port' }, 2600)
  }
}, { immediate: true })
onBeforeUnmount(() => clearTimeout(timer))
const pick = (m: 'proposal' | 'port') => {
  clearTimeout(timer)
  mode.value = m
}

const U = 550 / 9
const R = 0.85 * U
const pad = { x: 165, y: 405 }
const dirs = [
  { k: 'up', face: '▲', dx: 0, dy: -1.15, prop: '↑', port: 'W' },
  { k: 'down', face: '▼', dx: 0, dy: 1.15, prop: '↓', port: 'S' },
  { k: 'left', face: '◀', dx: -1.15, dy: 0, prop: '←', port: 'A' },
  { k: 'right', face: '▶', dx: 1.15, dy: 0, prop: '→', port: 'D' },
]
const acts = [
  { k: 'a', face: 'A', x: 1105, y: 455, prop: 'A', port: 'J' },
  { k: 'j', face: 'J', x: 1150, y: 330, prop: 'J', port: 'K' },
  { k: 'd', face: 'D', x: 1010, y: 360, prop: 'D', port: 'L' },
]
const fkeys = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'ESC']
const port = computed(() => mode.value === 'port')

const rows = [
  { btn: '◀▲▼▶', prop: 'стрелки', propDoes: 'ходит игрок 2', port: 'W S A D', portDoes: 'ходит игрок 1' },
  { btn: 'A', prop: 'A', propDoes: 'игрок 1: влево', port: 'J', portDoes: 'игрок 1: атака' },
  { btn: 'J', prop: 'J', propDoes: 'игрок 1: атака', port: 'K', portDoes: 'игрок 1: прыжок' },
  { btn: 'D', prop: 'D', propDoes: 'игрок 1: вправо', port: 'L', portDoes: 'игрок 1: защита' },
]
const sizes = [
  { dev: 'iPhone', prop: 13, port: 13 },
  { dev: 'iPad 13″', prop: 37, port: 16 },
]
</script>

<template>
  <div class="tc">
    <div class="sw">
      <button :class="{ on: !port }" @click="pick('proposal')">предложение StormPixels</button>
      <button :class="{ on: port }" @click="pick('port')">в порте, 743f0558</button>
      <span class="muted">схема, не снимок экрана</span>
    </div>
    <div class="phone">
      <svg viewBox="0 0 1223 550" role="img" :aria-label="`Сенсорные кнопки поверх кадра игры: ${port ? 'клавиши игрока 1' : 'клавиши из предложения'}`">
        <rect width="1223" height="550" fill="#05070b" />
        <image href="/img/screens/16-character-ai-ko.png" x="214.5" y="0" width="794" height="550" preserveAspectRatio="none" />
        <g class="ctl">
          <g v-for="d in dirs" :key="d.k" :transform="`translate(${pad.x + d.dx * U}, ${pad.y + d.dy * U})`">
            <circle :r="R * 0.78" class="btn" />
            <text y="8" class="face sm">{{ d.face }}</text>
            <text :y="R * 0.78 + 22" class="key" :class="{ bad: !port }">{{ port ? d.port : d.prop }}</text>
          </g>
          <g v-for="a in acts" :key="a.k" :transform="`translate(${a.x}, ${a.y})`">
            <circle :r="R" class="btn" />
            <text y="13" class="face">{{ a.face }}</text>
            <text :y="R + 24" class="key" :class="{ bad: !port }">{{ port ? a.port : a.prop }}</text>
          </g>
          <g transform="translate(1160, 52)">
            <rect x="-28" y="-26" width="56" height="52" rx="10" class="btn" />
            <text y="10" class="face sm">F</text>
          </g>
          <g transform="translate(866, 96)">
            <g v-for="(f, i) in fkeys" :key="f" :transform="`translate(${(i % 5) * 64}, ${Math.floor(i / 5) * 48})`">
              <rect width="58" height="42" rx="7" class="fk" />
              <text x="29" y="28" class="ft">{{ f }}</text>
            </g>
          </g>
          <g transform="translate(52, 52)">
            <rect x="-30" y="-24" width="60" height="48" rx="10" class="btn dim" />
            <text y="9" class="face xs">◐</text>
          </g>
        </g>
      </svg>
    </div>
    <div class="below">
      <table class="map">
        <thead>
          <tr><th>кнопка</th><th :class="{ cur: !port }">предложение: клавиша → в игре</th><th :class="{ cur: port }">в порте: клавиша → в игре</th></tr>
        </thead>
        <tbody>
          <tr v-for="r in rows" :key="r.btn">
            <td class="bt">{{ r.btn }}</td>
            <td :class="{ cur: !port }"><code>{{ r.prop }}</code> <span class="bad">{{ r.propDoes }}</span></td>
            <td :class="{ cur: port }"><code>{{ r.port }}</code> {{ r.portDoes }}</td>
          </tr>
        </tbody>
      </table>
      <div class="sz">
        <div class="szh">ширина кнопки, мм</div>
        <div v-for="s in sizes" :key="s.dev" class="szr">
          <span class="dv">{{ s.dev }}</span>
          <div class="bars">
            <div class="b prop" :style="{ width: `${s.prop * 1.9}px` }"><i>{{ s.prop }}</i></div>
            <div class="b port" :style="{ width: `${s.port * 1.9}px` }"><i>{{ s.port }}</i></div>
          </div>
        </div>
        <div class="szl"><span><i class="prop" />предложение</span><span><i class="port" />единица ≤ 48 pt</span></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tc { display: flex; flex-direction: column; gap: 6px; }
.sw { display: flex; align-items: center; gap: 6px; font-size: 0.62rem; }
.sw button { font-size: 0.62rem; color: var(--ink-2); background: transparent; border: 1px solid var(--axis); border-radius: 999px; padding: 1px 9px; cursor: pointer; }
.sw button.on { color: var(--ink); border-color: var(--naruto); background: rgba(255, 138, 61, 0.14); }
.sw .muted { margin-left: auto; font-size: 0.56rem; }
.phone { border: 6px solid #1d2230; border-radius: 22px; overflow: hidden; line-height: 0; box-shadow: 0 8px 26px rgba(0, 0, 0, 0.45); }
.phone svg { width: 100%; display: block; }
.btn { fill: rgba(255, 255, 255, 0.16); stroke: rgba(255, 255, 255, 0.6); stroke-width: 3; }
.btn.dim { fill: rgba(255, 255, 255, 0.08); stroke: rgba(255, 255, 255, 0.35); }
.face { font-family: var(--font-pixel); font-size: 38px; fill: #f6f3ec; text-anchor: middle; }
.face.sm { font-size: 26px; }
.face.xs { font-size: 24px; }
.key { font-family: var(--font-mono); font-size: 25px; font-weight: 700; text-anchor: middle; fill: var(--chakra); paint-order: stroke; stroke: #05070b; stroke-width: 6px; transition: fill 0.3s; }
.key.bad { fill: var(--serious); }
.fk { fill: rgba(10, 13, 19, 0.78); stroke: rgba(255, 255, 255, 0.4); stroke-width: 2; }
.ft { font-family: var(--font-mono); font-size: 18px; fill: #f6f3ec; text-anchor: middle; }
.below { display: grid; grid-template-columns: 1fr 148px; gap: 10px; align-items: start; }
.map { font-size: 0.6rem !important; }
.map th, .map td { padding: 0.14rem 0.35rem !important; }
.map th { font-size: 0.56rem; font-weight: 500; }
.map th.cur { color: var(--ink); }
.map td { color: var(--muted) !important; }
.map td.cur { color: var(--ink) !important; }
.map td.bt { font-family: var(--font-pixel); color: var(--ink-2) !important; white-space: nowrap; }
.map code { font-size: 0.56rem !important; }
.map .bad { color: inherit; }
.map td.cur .bad { color: var(--serious); }
.sz { background: var(--surface); border: 1px solid var(--hair); border-radius: 10px; padding: 4px 8px 5px; }
.szh { font-size: 0.56rem; color: var(--muted); margin-bottom: 2px; }
.szr { display: grid; grid-template-columns: 40px 1fr; gap: 4px; align-items: center; margin: 2px 0; }
.dv { font-size: 0.56rem; color: var(--ink-2); }
.bars { display: flex; flex-direction: column; gap: 2px; }
.b { height: 9px; border-radius: 2px; position: relative; }
.b i { position: absolute; left: 100%; margin-left: 3px; top: -2px; font-style: normal; font-size: 0.52rem; font-family: var(--font-mono); color: var(--ink-2); }
.b.prop, .szl i.prop { background: var(--s2); }
.b.port, .szl i.port { background: var(--s1); }
.szl { display: flex; flex-direction: column; gap: 1px; font-size: 0.5rem; color: var(--muted); margin-top: 3px; }
.szl i { display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: 4px; vertical-align: -1px; }
</style>
