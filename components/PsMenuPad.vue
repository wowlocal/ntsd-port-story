<script setup lang="ts">
// Chapter 19, MENU_GAMEPAD: a controller works CONTROL SETTINGS, a screen the original reads only with the mouse.
// Targets are the card's rectangles in the game's 794×550 client (docs/research/MENU_GAMEPAD.md, "Screens and
// targets"): per player x 194+139·p, 105 wide — the name field y 156…173, the device box 182…272, the key cells
// 280+22·r…298+22·r (a joystick's four direction rows left out); OK 405…560 and Cancel 582…737 at y 441…465.
// A move follows the card's rule: among the targets that way, the nearest in the same row or column band, else within
// 45°, else at least 16 px that way, by the distance along plus twice the distance across; with none, it wraps to the
// farthest the other way (band, then 45°). The autoplay is the e2e route of the card: the first A only shows the
// start (player 1's device box), A switches it keyboard → joystick 1, down ×4 reaches OK, A saves control.txt.
// Screenshot: public/img/screens/17-gdi-text-controls.png (the native app, 2× the client).
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'

type Dir = 'up' | 'down' | 'left' | 'right'
interface T { id: string, kind: 'name' | 'dev' | 'cell' | 'ok' | 'cancel', p: number, r?: number, x0: number, x1: number, y0: number, y1: number }
interface Log { btn: string, text: string, tier?: string }

const rowName = ['up', 'down', 'left', 'right', 'attack', 'jump', 'defend']
const devName = ['клавиатура', 'джойстик 1', 'джойстик 2']
const initialDev = [0, 0, 1, 2] // the packaged control.txt: players 3 and 4 on joysticks 1 and 2

const nav = useNav()
const active = useIsSlideActive()
const dev = ref([...initialDev])
const cur = ref<string | null>(null)
const trail = ref<string[]>([])
const log = ref<Log[]>([])
const closed = ref(false)

const targets = computed<T[]>(() => {
  const t: T[] = []
  for (let p = 0; p < 4; p++) {
    const x0 = 194 + 139 * p
    const x1 = x0 + 105
    t.push({ id: `n${p}`, kind: 'name', p, x0, x1, y0: 156, y1: 173 })
    t.push({ id: `d${p}`, kind: 'dev', p, x0, x1, y0: 182, y1: 272 })
    const rows = dev.value[p] === 0 ? [0, 1, 2, 3, 4, 5, 6] : [4, 5, 6]
    for (const r of rows)
      t.push({ id: `c${p}${r}`, kind: 'cell', p, r, x0, x1, y0: 280 + 22 * r, y1: 298 + 22 * r })
  }
  t.push({ id: 'ok', kind: 'ok', p: -1, x0: 405, x1: 560, y0: 441, y1: 465 })
  t.push({ id: 'cancel', kind: 'cancel', p: -1, x0: 582, x1: 737, y0: 441, y1: 465 })
  return t
})
const byId = (id: string | null) => targets.value.find(t => t.id === id)
const ctr = (t: T) => ({ x: (t.x0 + t.x1) / 2, y: (t.y0 + t.y1) / 2 })
const nameOf = (t?: T) => {
  if (!t)
    return '—'
  if (t.kind === 'ok')
    return 'OK'
  if (t.kind === 'cancel')
    return 'Cancel'
  if (t.kind === 'name')
    return `имя игрока ${t.p + 1}`
  if (t.kind === 'dev')
    return `устройство игрока ${t.p + 1}`
  return `${rowName[t.r!]} игрока ${t.p + 1}`
}

function next(from: T, dir: Dir): { t: T, tier: string } | null {
  const c = ctr(from)
  const horiz = dir === 'left' || dir === 'right'
  const s = dir === 'right' || dir === 'down' ? 1 : -1
  const list = targets.value.filter(t => t.id !== from.id).map((t) => {
    const tc = ctr(t)
    const along = (horiz ? tc.x - c.x : tc.y - c.y) * s
    const across = Math.abs(horiz ? tc.y - c.y : tc.x - c.x)
    const band = horiz ? (t.y0 < from.y1 && t.y1 > from.y0) : (t.x0 < from.x1 && t.x1 > from.x0)
    return { t, along, across, band }
  })
  const tiers: [string, (e: typeof list[number]) => boolean][] = [
    ['в той же полосе', e => e.along > 0 && e.band],
    ['в пределах 45°', e => e.along > 0 && e.across <= e.along],
    ['не меньше 16 px в ту сторону', e => e.along >= 16],
  ]
  for (const [tier, f] of tiers) {
    const cand = list.filter(f)
    if (cand.length)
      return { t: cand.reduce((a, b) => (b.along + 2 * b.across < a.along + 2 * a.across ? b : a)).t, tier }
  }
  for (const [tier, f] of [['по кругу, в полосе', (e: typeof list[number]) => e.along < 0 && e.band], ['по кругу, в пределах 45°', (e: typeof list[number]) => e.along < 0 && e.across <= -e.along]] as const) {
    const cand = list.filter(f)
    if (cand.length)
      return { t: cand.reduce((a, b) => (b.along < a.along || (b.along === a.along && b.across < a.across) ? b : a)).t, tier }
  }
  return null
}

const arrow: Record<Dir, string> = { up: '↑', down: '↓', left: '←', right: '→' }
function push(l: Log) {
  log.value = [...log.value, l].slice(-7)
}
function move(dir: Dir) {
  if (closed.value)
    return
  const from = byId(cur.value)
  if (!from) {
    cur.value = 'd0'
    trail.value = ['d0']
    push({ btn: arrow[dir], text: 'курсор на старте: устройство игрока 1' })
    return
  }
  const n = next(from, dir)
  if (!n)
    return
  cur.value = n.t.id
  trail.value = [...trail.value, n.t.id]
  push({ btn: arrow[dir], text: nameOf(n.t), tier: n.tier })
}
function press() {
  if (closed.value)
    return
  const t = byId(cur.value)
  if (!t) {
    cur.value = 'd0'
    trail.value = ['d0']
    push({ btn: 'A', text: 'ничего не выбрано — A только показывает старт' })
    return
  }
  if (t.kind === 'dev') {
    const d = [...dev.value]
    d[t.p] = (d[t.p] + 1) % 3
    dev.value = d
    push({ btn: 'A', text: `клик: игрок ${t.p + 1} — ${devName[d[t.p]]}` })
  }
  else if (t.kind === 'ok') {
    closed.value = true
    const changed = dev.value.map((d, i) => d !== initialDev[i] ? `игрок ${i + 1}: ${initialDev[i]} → ${d}` : '').filter(Boolean)
    push({ btn: 'A', text: `OK: control.txt записан${changed.length ? ` (${changed.join(', ')})` : ''}` })
  }
  else if (t.kind === 'cancel') {
    closed.value = true
    push({ btn: 'A', text: 'Cancel: экран закрыт без записи' })
  }
  else if (t.kind === 'name') {
    push({ btn: 'A', text: 'поле имени: текст — с клавиатуры (на Deck — экранная клавиатура Steam)' })
  }
  else {
    push({ btn: 'A', text: dev.value[t.p] === 0 ? 'клетка ждёт клавишу' : `клетка ждёт кнопку джойстика ${dev.value[t.p]}` })
  }
}
function reset() {
  dev.value = [...initialDev]
  cur.value = null
  trail.value = []
  log.value = []
  closed.value = false
}

const route: (() => void)[] = [press, press, () => move('down'), () => move('down'), () => move('down'), () => move('down'), press]
let timer = 0
function stop() {
  clearTimeout(timer)
  timer = 0
}
function play(i = 0) {
  if (i === 0)
    reset()
  if (i >= route.length)
    return
  route[i]()
  timer = window.setTimeout(() => play(i + 1), i === 0 ? 900 : 750)
}
if (nav.isPrintMode.value) {
  for (const f of route) f()
}
watch(active, (a) => {
  stop()
  if (a && !nav.isPrintMode.value)
    timer = window.setTimeout(() => play(0), 600)
}, { immediate: true })
onBeforeUnmount(stop)
const user = (f: () => void) => () => {
  stop()
  f()
}

const W = 794
const H = 550
const curT = computed(() => byId(cur.value))
const pts = computed(() => trail.value.map(id => byId(id)).filter(Boolean).map(t => ctr(t!)))
const hiddenRows = computed(() => dev.value.flatMap((d, p) => d === 0 ? [] : [0, 1, 2, 3].map(r => ({ p, r }))))
</script>

<template>
  <div class="mp">
    <div class="scr">
      <img src="/img/screens/17-gdi-text-controls.png" alt="CONTROL SETTINGS в нативном приложении">
      <svg :viewBox="`0 0 ${W} ${H}`" class="ov" role="img" :aria-label="`Цели геймпада на CONTROL SETTINGS: ${targets.length}; курсор — ${nameOf(curT)}`">
        <rect v-for="h in hiddenRows" :key="`h${h.p}${h.r}`" :x="194 + 139 * h.p" :y="280 + 22 * h.r" width="105" height="18" class="gone" />
        <rect v-for="t in targets" :key="t.id" :x="t.x0" :y="t.y0" :width="t.x1 - t.x0" :height="t.y1 - t.y0" rx="2" class="tg" :class="{ on: t.id === cur }" />
        <g v-for="(d, p) in dev" :key="`dv${p}`">
          <text v-if="d !== initialDev[p]" :x="246.5 + 139 * p" y="266" text-anchor="middle" class="dvl">{{ devName[d] }}</text>
        </g>
        <polyline v-if="pts.length > 1" :points="pts.map(q => `${q.x},${q.y}`).join(' ')" class="trail" />
        <g v-if="curT" class="cursor" :style="{ transform: `translate(${ctr(curT).x}px, ${ctr(curT).y}px)` }">
          <path d="M0,0 l0,17 l4.5,-4.5 l4,9 l3.4,-1.5 l-4,-8.6 l6.4,0 z" />
        </g>
        <text v-if="closed" x="397" y="512" text-anchor="middle" class="done">экран закрыт</text>
      </svg>
    </div>
    <div class="side">
      <div class="pad">
        <div class="dp">
          <button class="b u" aria-label="вверх" @click="user(() => move('up'))()">▲</button>
          <button class="b l" aria-label="влево" @click="user(() => move('left'))()">◀</button>
          <button class="b r" aria-label="вправо" @click="user(() => move('right'))()">▶</button>
          <button class="b d" aria-label="вниз" @click="user(() => move('down'))()">▼</button>
        </div>
        <button class="a" aria-label="кнопка A" @click="user(press)()">A</button>
        <div class="meta">
          <div><b>{{ targets.length }}</b> целей на экране</div>
          <button class="again" @click="user(() => play(0))()">↻ маршрут из e2e</button>
          <button class="again" @click="user(reset)()">сброс</button>
        </div>
      </div>
      <ol class="log">
        <li v-for="(l, i) in log" :key="i">
          <span class="k">{{ l.btn }}</span>
          <span class="t">{{ l.text }}<i v-if="l.tier"> · {{ l.tier }}</i></span>
        </li>
        <li v-if="!log.length" class="muted">
          <span class="k">·</span><span class="t">жмите крестовину и A</span>
        </li>
      </ol>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.mp { display: grid; grid-template-columns: 440px 1fr; gap: 14px; align-items: start; }
.scr { position: relative; border: 1px solid var(--hair); border-radius: 10px; overflow: hidden; line-height: 0; }
.scr img { width: 100%; display: block; }
.ov { position: absolute; inset: 0; width: 100%; height: 100%; }
.tg { fill: none; stroke: rgba(108, 182, 255, 0.55); stroke-width: 1.2; stroke-dasharray: 3 2; transition: fill 0.2s, stroke 0.2s; }
.tg.on { fill: rgba(255, 138, 61, 0.22); stroke: var(--naruto); stroke-width: 2.6; stroke-dasharray: none; }
.gone { fill: rgba(10, 13, 19, 0.72); }
.dvl { font-family: var(--font-pixel); font-size: 15px; fill: var(--naruto); paint-order: stroke; stroke: #0a0d13; stroke-width: 4px; }
.trail { fill: none; stroke: var(--naruto); stroke-width: 2; stroke-dasharray: 5 4; opacity: 0.7; }
.cursor { transition: transform 0.28s ease; }
.cursor path { fill: #fff; stroke: #000; stroke-width: 1.2; }
.done { font-family: var(--font-pixel); font-size: 22px; fill: var(--good); paint-order: stroke; stroke: #0a0d13; stroke-width: 5px; }
.side { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.pad { display: grid; grid-template-columns: 84px 44px 1fr; gap: 10px; align-items: center; background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: 8px 10px; }
.dp { position: relative; width: 84px; height: 84px; }
.b { position: absolute; width: 28px; height: 28px; border-radius: 6px; border: 1px solid var(--axis); background: var(--surface-3); color: var(--ink); font-size: 10px; cursor: pointer; line-height: 1; padding: 0; }
.b:hover { border-color: var(--naruto); color: var(--naruto); }
.b.u { left: 28px; top: 0; }
.b.d { left: 28px; top: 56px; }
.b.l { left: 0; top: 28px; }
.b.r { left: 56px; top: 28px; }
.a { width: 40px; height: 40px; border-radius: 50%; border: 1px solid rgba(255, 138, 61, 0.7); background: rgba(255, 138, 61, 0.18); color: var(--naruto); font-family: var(--font-pixel); font-size: 1rem; cursor: pointer; }
.a:hover { background: rgba(255, 138, 61, 0.32); }
.meta { display: flex; flex-direction: column; gap: 4px; font-size: 0.62rem; color: var(--ink-2); }
.meta b { color: var(--ink); font-family: var(--font-display); font-size: 0.85rem; }
.again { align-self: flex-start; font-size: 0.6rem; color: var(--ink-2); background: transparent; border: 1px solid var(--axis); border-radius: 999px; padding: 1px 8px; cursor: pointer; }
.again:hover { color: var(--naruto); border-color: var(--naruto); }
.log { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 2px; min-height: 7.4rem; }
.log li { display: grid; grid-template-columns: 20px 1fr; gap: 6px; align-items: baseline; padding: 0 !important; margin: 0 !important; font-size: 0.62rem; line-height: 1.3; color: var(--ink-2); }
.log li::before { display: none; }
.log .k { font-family: var(--font-pixel); color: var(--naruto); text-align: center; }
.log .t i { font-style: normal; color: var(--muted); }
</style>
