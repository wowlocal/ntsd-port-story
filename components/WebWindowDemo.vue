<script setup lang="ts">
import { computed, ref } from 'vue'
import { useNav } from '@slidev/client'
import data from '../data/web_window.json'

// The scalable window (WINDOW_SCALING S1–S6) as a model one can play with. A real 794×550 game frame
// (the AppKit app's Demo, public/img/web/frame-demo-794.png) is fitted into a host's screen or window with its
// aspect kept and nearest pixels; with --original-window it is shown one point per pixel, centred, shrunk only
// when the window is smaller (browser, Android). Presets are the sizes the evidence measured; the panel shows the
// model's box next to the measured one. Drag the window's corner (windowed hosts), hover the picture to see the
// game pixel a click would reach. Export shows Apple TV at 1080p, the chapter's case.
// Data: data/web_window.json (scripts/collect_web.py).
const d = data as any
const nav = useNav()
const presets = d.presets as any[]
const GW = 794
const GH = 550

const key = ref('tv1080')
const orig = ref(false)
const P = computed(() => presets.find(p => p.key === (nav.isPrintMode.value ? 'tv1080' : key.value))!)
const isOrig = computed(() => !nav.isPrintMode.value && orig.value)
const isBrowser = computed(() => P.value.key.startsWith('web'))
const fixedOrig = computed(() => isOrig.value && (P.value.key === 'mac' || P.value.key === 'x11')) // the original fixed window
const aspectLock = computed(() => P.value.key === 'mac') // AppKit keeps contentAspectRatio; Xvfb had no window manager

// the desktop behind a browser window is only a backdrop (Playwright sets the viewport, there is no screen)
const desk = computed<[number, number]>(() => (isBrowser.value ? [1920, 1080] : P.value.screen))
const userWin = ref<Record<string, [number, number]>>({})
const win = computed<[number, number]>(() => {
  if (!P.value.windowed)
    return P.value.screen
  if (fixedOrig.value)
    return [GW, GH]
  return userWin.value[P.value.key] ?? P.value.window
})
const dragged = computed(() => !!userWin.value[P.value.key] && !fixedOrig.value && P.value.windowed)

// stage geometry (CSS px of the slide)
const SW = 512
const SH = 272
const PAD = 10
const chrome = computed(() => (!P.value.windowed ? 0 : isBrowser.value ? 16 : P.value.key === 'mac' ? Math.max(6, 28 * k.value) : 0))
const k = computed(() => Math.min((SW - 2 * PAD) / desk.value[0], (SH - 2 * PAD) / desk.value[1]))
const scr = computed(() => ({ w: desk.value[0] * k.value, h: desk.value[1] * k.value, x: (SW - desk.value[0] * k.value) / 2, y: (SH - desk.value[1] * k.value) / 2 }))
const winBox = computed(() => {
  const [w, h] = win.value
  const ww = w * k.value
  const wh = h * k.value
  if (!P.value.windowed)
    return { x: scr.value.x, y: scr.value.y, w: ww, h: wh }
  const init = P.value.window as [number, number]
  // the window keeps its top-left corner where the preset's window opened (centred)
  const ox = ((desk.value[0] - init[0]) / 2) * k.value
  const oy = Math.max(chrome.value, ((desk.value[1] - init[1]) / 2) * k.value)
  const fx = fixedOrig.value ? ((desk.value[0] - GW) / 2) * k.value : ox
  const fy = fixedOrig.value ? Math.max(chrome.value, ((desk.value[1] - GH) / 2) * k.value) : oy
  return { x: scr.value.x + fx, y: scr.value.y + fy, w: ww, h: wh }
})

// the picture, in host units (pt or px) and in device pixels
const s = computed(() => {
  const [w, h] = win.value
  const fit = Math.min(w / GW, h / GH)
  return isOrig.value ? Math.min(1, fit) : fit
})
const dpr = computed(() => P.value.scale as number)
const r = computed(() => s.value * dpr.value)
const pic = computed(() => ({ w: GW * s.value * k.value, h: GH * s.value * k.value }))
const picDev = computed<[number, number]>(() => [Math.round(GW * r.value + 1e-6), Math.round(GH * r.value + 1e-6)])
const availDev = computed<[number, number]>(() => [Math.round(win.value[0] * dpr.value), Math.round(win.value[1] * dpr.value)])
const bars = computed(() => {
  const bx = availDev.value[0] - picDev.value[0]
  const by = availDev.value[1] - picDev.value[1]
  if (bx <= 1 && by <= 1)
    return 'полей нет'
  const parts: string[] = []
  const half = (v: number) => (v % 2 === 0 ? `по ${v / 2} px` : `${Math.floor(v / 2)} и ${Math.ceil(v / 2)} px`)
  if (bx > 1)
    parts.push(`${half(bx)} слева и справа`)
  if (by > 1)
    parts.push(`${half(by)} сверху и снизу`)
  return `поля ${parts.join(', ')}`
})

// nearest scaling: how many device pixels each game column / row gets
function widths(n: number, m: number) {
  const base = Math.floor(m / n)
  const wide = m - base * n // this many get base+1
  return { base, wide, narrow: n - wide }
}
const cols = computed(() => widths(GW, picDev.value[0]))
const rows = computed(() => widths(GH, picDev.value[1]))
const even = computed(() => cols.value.wide === 0 && rows.value.wide === 0)
const nf = (n: number) => n.toLocaleString('ru-RU')
const evenText = (w: { base: number, wide: number, narrow: number }, what: string) => {
  if (w.wide === 0)
    return `${what}: все по ${w.base} px`
  if (w.base === 0)
    return `${what}: на экран попадают ${nf(w.wide)}, ${nf(w.narrow)} выпадают`
  return `${what}: ${nf(w.narrow)} по ${w.base} px и ${nf(w.wide)} по ${w.base + 1} px`
}

// the magnifier: 20 game columns and 20 game rows around the first odd one, each drawn as wide as the
// device pixels nearest scaling gives it (the minority width in orange)
const ZW = 300
const N = 20
function run(n: number, m: number) {
  const ws: number[] = []
  for (let j = 0; j < n; j++) ws.push(Math.ceil(((j + 1) * m) / n - 1e-9) - Math.ceil((j * m) / n - 1e-9))
  const w = widths(n, m)
  const oddW = w.wide === 0 ? -1 : (w.wide <= w.narrow ? w.base + 1 : w.base)
  const odd = oddW < 0 ? 0 : ws.findIndex(x => x === oddW)
  const start = Math.max(0, Math.min(n - N, odd - Math.floor(N / 2)))
  return { ws: ws.slice(start, start + N), oddW, start }
}
const magC = computed(() => run(GW, picDev.value[0]))
const magR = computed(() => run(GH, picDev.value[1]))
const zoom = computed(() => {
  const tot = Math.max(magC.value.ws.reduce((a, b) => a + b, 0), magR.value.ws.reduce((a, b) => a + b, 0), 1)
  return Math.max(1, Math.min(10, (ZW - 56) / tot))
})
function strip(m: { ws: number[], oddW: number, start: number }) {
  let x = 56
  return m.ws.map((w, i) => {
    const c = { x, w: w * zoom.value, odd: w === m.oddW, dark: (i + m.start) % 2 === 0 }
    x += w * zoom.value
    return c
  })
}
const stripC = computed(() => strip(magC.value))
const stripR = computed(() => strip(magR.value))

// measured, when the window is the preset's own
const measured = computed(() => {
  if (dragged.value)
    return null
  const m = P.value.measured?.[isOrig.value ? 'orig' : 'fit']
  return m ? m as [number, number] : null
})
const agrees = computed(() => !!measured.value && Math.abs(measured.value[0] - picDev.value[0]) <= 2 && Math.abs(measured.value[1] - picDev.value[1]) <= 2)
const fmtBox = (b: [number, number]) => `${nf(Math.round(b[0] * 10) / 10)} × ${nf(Math.round(b[1] * 10) / 10)}`
const sx = computed(() => r.value.toFixed(2).replace('.', ','))

// drag the window's corner
const stage = ref<HTMLElement | null>(null)
let dragging = false
function stagePt(e: PointerEvent) {
  const rc = stage.value!.getBoundingClientRect()
  const f = SW / rc.width
  return [(e.clientX - rc.left) * f, (e.clientY - rc.top) * f]
}
function down(e: PointerEvent) {
  dragging = true
  ;(e.currentTarget as HTMLElement).setPointerCapture?.(e.pointerId)
}
function move(e: PointerEvent) {
  if (!dragging)
    return
  const [x, y] = stagePt(e)
  const b = winBox.value
  let w = (x - b.x) / k.value
  let h = (y - b.y) / k.value
  const maxW = (scr.value.x + scr.value.w - b.x) / k.value
  const maxH = (scr.value.y + scr.value.h - b.y) / k.value
  const minW = isBrowser.value ? 240 : GW / 2
  const minH = isBrowser.value ? 180 : GH / 2
  w = Math.max(minW, Math.min(maxW, w))
  h = Math.max(minH, Math.min(maxH, h))
  if (aspectLock.value) {
    h = (w * GH) / GW
    if (h > maxH) {
      h = maxH
      w = (h * GW) / GH
    }
  }
  userWin.value = { ...userWin.value, [P.value.key]: [Math.round(w), Math.round(h)] }
}
function up() {
  dragging = false
}
function pick(k2: string) {
  key.value = k2
  const u = { ...userWin.value }
  delete u[k2]
  userWin.value = u
}

// hover the picture: which game pixel a click there reaches
const hoverPx = ref<[number, number] | null>(null)
function overPic(e: PointerEvent) {
  const rc = (e.currentTarget as HTMLElement).getBoundingClientRect()
  const gx = Math.min(GW - 1, Math.max(0, Math.floor(((e.clientX - rc.left) / rc.width) * GW)))
  const gy = Math.min(GH - 1, Math.max(0, Math.floor(((e.clientY - rc.top) / rc.height) * GH)))
  hoverPx.value = [gx, gy]
}
const short: Record<string, string> = { tv1080: 'Apple TV 1080p', tv4k: 'Apple TV 4K', mac: 'Mac · окно', macfs: 'Mac · полный экран', x11: 'Linux · X11', a12: 'Galaxy A12', web1600: 'браузер 1600×900', web400: 'браузер 400×600' }
</script>

<template>
  <div class="wd">
    <div class="chips">
      <button v-for="p in presets" :key="p.key" class="chip" :class="{ on: P.key === p.key }" @click="pick(p.key)">
        {{ short[p.key] }}<span v-if="p.windowed" class="rs">⇲</span>
      </button>
    </div>
    <div class="grid2">
      <div class="left">
      <div
        ref="stage" class="stage" :style="{ width: `${SW}px`, height: `${SH}px` }"
        @pointermove="move" @pointerup="up" @pointercancel="up"
      >
        <!-- the screen or desktop -->
        <div class="scr" :class="{ tv: P.key.startsWith('tv'), desk: P.windowed }" :style="{ left: `${scr.x}px`, top: `${scr.y}px`, width: `${scr.w}px`, height: `${scr.h}px` }" />
        <!-- window chrome -->
        <div v-if="P.windowed && chrome > 0" class="bar" :class="{ browser: isBrowser }" :style="{ left: `${winBox.x}px`, top: `${winBox.y - chrome}px`, width: `${winBox.w}px`, height: `${chrome}px` }">
          <i /><i /><i />
        </div>
        <!-- the window's client area / the whole screen -->
        <div class="client" :class="{ windowed: P.windowed }" :style="{ left: `${winBox.x}px`, top: `${winBox.y}px`, width: `${winBox.w}px`, height: `${winBox.h}px` }">
          <img
            src="/img/web/frame-demo-794.png" alt="кадр игры 794×550" class="pic"
            :style="{ width: `${pic.w}px`, height: `${pic.h}px`, left: `${(winBox.w - pic.w) / 2}px`, top: `${(winBox.h - pic.h) / 2}px` }"
            draggable="false" @pointermove="overPic" @pointerleave="hoverPx = null"
          >
        </div>
        <div
          v-if="P.windowed && !fixedOrig" class="handle" :style="{ left: `${winBox.x + winBox.w - 9}px`, top: `${winBox.y + winBox.h - 9}px` }"
          title="потяните, чтобы изменить размер окна" @pointerdown="down"
        />
      </div>
      <div class="cap">
        {{ P.where }}
      </div>
      </div>

      <div class="panel">
        <label class="tog" :class="{ on: isOrig }">
          <input v-model="orig" type="checkbox" :disabled="nav.isPrintMode.value">
          <span class="sw"><i /></span>
          <span class="mono">--original-window</span>
        </label>
        <div class="big">
          <span class="num">{{ sx }}×</span>
          <span class="u">пикселей экрана на пиксель игры</span>
        </div>
        <div class="ln">
          {{ P.windowed ? (isBrowser ? 'окно браузера' : 'окно') : 'экран' }} <b>{{ fmtBox(win) }}</b> {{ P.unit }}<span v-if="dpr > 1"> · ×{{ dpr }} = {{ fmtBox(availDev) }} px</span>
        </div>
        <div class="ln">
          картинка <b>{{ fmtBox(picDev) }} px</b> · {{ bars }}
        </div>
        <div class="ln meas" :class="{ ok: agrees, miss: measured && !agrees, none: !measured }">
          <template v-if="measured">
            замер: <b>{{ fmtBox(measured) }} px</b> · {{ agrees ? 'совпадает с моделью' : (P.key === 'a12' ? 'масштабирует компоновщик Android' : 'расходится с моделью') }}
          </template>
          <template v-else>
            {{ dragged ? 'свой размер — такой не замерялся' : 'в этом режиме не замерялось' }}
          </template>
        </div>
        <div class="ln game">
          игра видит своё окно <b>794 × 550</b> — всегда
        </div>
        <div class="ln click">
          <template v-if="hoverPx">
            клик сюда → пиксель игры <b>({{ hoverPx[0] }}, {{ hoverPx[1] }})</b>
          </template>
          <template v-else>
            клики переводятся в пиксели игры: (0, 0), (350, 230), (793, 549) — точно на каждом проверенном размере
          </template>
        </div>
        <div class="mag">
          <svg :width="ZW" height="44" :viewBox="`0 0 ${ZW} 44`">
            <text x="0" y="14" class="ml">столбцы</text>
            <rect v-for="(c, i) in stripC" :key="`c${i}`" :x="c.x" y="4" :width="Math.max(0.8, c.w - 0.8)" height="14" :fill="c.odd ? (c.dark ? '#b8501f' : 'var(--s2)') : (c.dark ? '#2b3345' : '#4a5366')" />
            <text x="0" y="36" class="ml">строки</text>
            <rect v-for="(c, i) in stripR" :key="`r${i}`" :x="c.x" y="26" :width="Math.max(0.8, c.w - 0.8)" height="14" :fill="c.odd ? (c.dark ? '#b8501f' : 'var(--s2)') : (c.dark ? '#2b3345' : '#4a5366')" />
          </svg>
          <div class="mt">
            <template v-if="even">
              лупа: масштаб целый — каждый пиксель игры шириной {{ cols.base }} px, все одинаковые
            </template>
            <template v-else>
              лупа: ширина пикселей игры на экране, рыжие — другой ширины. {{ evenText(cols, 'Столбцы') }}; {{ evenText(rows, 'строки') }}
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wd {
  position: relative;
}
.chips {
  display: flex;
  gap: 0.3rem;
  flex-wrap: wrap;
  margin-bottom: 0.4rem;
}
.chip {
  font-family: var(--font-sans);
  font-size: 0.64rem;
  color: var(--ink-2);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--hair);
  border-radius: 999px;
  padding: 0.12rem 0.55rem;
  cursor: pointer;
  white-space: nowrap;
}
.chip .rs {
  margin-left: 0.3rem;
  color: var(--muted);
}
.chip.on {
  color: #1a0d05;
  background: var(--naruto);
  border-color: var(--naruto);
  font-weight: 650;
}
.chip.on .rs {
  color: #1a0d05;
}
.grid2 {
  display: grid;
  grid-template-columns: 512px 1fr;
  gap: 1rem;
}
.stage {
  position: relative;
  background: #07090d;
  border: 1px solid var(--hair);
  border-radius: 10px;
  overflow: hidden;
  touch-action: none;
  user-select: none;
}
.scr {
  position: absolute;
  background: #000;
  border-radius: 2px;
}
.scr.tv {
  box-shadow: 0 0 0 4px #1d2230, 0 0 0 5px #3a4252;
}
.scr.desk {
  background: linear-gradient(160deg, #1b2233, #121722);
}
.bar {
  position: absolute;
  background: linear-gradient(180deg, #2a3142, #222838);
  border-radius: 4px 4px 0 0;
  display: flex;
  align-items: center;
  gap: 2px;
  padding-left: 3px;
  overflow: hidden;
}
.bar i {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: #ff5f57;
}
.bar i:nth-child(2) {
  background: #febc2e;
}
.bar i:nth-child(3) {
  background: #28c840;
}
.bar.browser i {
  width: 5px;
  height: 5px;
}
.client {
  position: absolute;
  background: #000;
  overflow: hidden;
}
.client.windowed {
  outline: 1px solid rgba(255, 255, 255, 0.22);
}
.pic {
  position: absolute;
  image-rendering: pixelated;
  max-width: none;
  cursor: crosshair;
}
.handle {
  position: absolute;
  width: 18px;
  height: 18px;
  border-radius: 4px;
  background: var(--naruto);
  box-shadow: 0 0 0 2px rgba(10, 13, 19, 0.8), 0 0 14px rgba(255, 138, 61, 0.6);
  cursor: nwse-resize;
  z-index: 3;
}
.handle::after {
  content: '';
  position: absolute;
  inset: 4px;
  border-right: 2px solid #1a0d05;
  border-bottom: 2px solid #1a0d05;
}
.cap {
  font-size: 0.64rem;
  color: var(--muted);
  line-height: 1.3;
  margin-top: 0.25rem;
}
.panel {
  display: flex;
  flex-direction: column;
  gap: 0.22rem;
  min-width: 0;
}
.tog {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.7rem;
  color: var(--ink-2);
  cursor: pointer;
  user-select: none;
}
.tog input {
  display: none;
}
.tog .sw {
  width: 28px;
  height: 16px;
  border-radius: 999px;
  background: #3a4252;
  position: relative;
  transition: background 0.2s ease;
}
.tog .sw i {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--ink);
  transition: left 0.2s ease;
}
.tog.on .sw {
  background: var(--naruto);
}
.tog.on .sw i {
  left: 14px;
}
.tog.on .mono {
  color: var(--ink);
}
.big {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin: 0.1rem 0 0.05rem;
}
.big .num {
  font-size: 2rem;
  font-weight: 700;
  color: var(--ink);
  line-height: 1;
}
.big .u {
  font-size: 0.64rem;
  color: var(--muted);
  line-height: 1.2;
}
.ln {
  font-size: 0.66rem;
  color: var(--ink-2);
  line-height: 1.35;
}
.ln b {
  color: var(--ink);
}
.meas {
  padding-left: 0.5rem;
  border-left: 2px solid var(--axis);
}
.meas.ok {
  border-left-color: var(--good);
}
.meas.miss {
  border-left-color: var(--warning);
}
.meas.none {
  color: var(--muted);
}
.game {
  color: var(--ink-2);
}
.click {
  min-height: 2.6em;
}
.mag {
  margin-top: 0.15rem;
  border-top: 1px solid var(--grid);
  padding-top: 0.3rem;
}
.ml {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
}
.mt {
  font-size: 0.64rem;
  color: var(--muted);
  line-height: 1.3;
  margin-top: 0.15rem;
}
</style>
