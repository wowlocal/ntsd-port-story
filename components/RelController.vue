<script setup lang="ts">
// Chapter 18, PHONE_CONTROLLER: the user's clip-on controller (it reported itself as "Razer Razer Kishi V2",
// USB 1532:0712) drawn as a schematic. Hover or focus a control to see its evdev code (HID interface 0),
// the Android key or axis, what the port's Android host sends to the original's WinMM joystick, the action
// player 3 has on that button by default (control.txt) and how many raw events it produced in the recording
// while the user played (18:51–18:58). Halo area is proportional to the event count.
// Data: data/rel_controller.json (scripts/collect_release.py).
import { computed, ref } from 'vue'
import ctl from '../data/rel_controller.json'

const d = ctl as any
const byId: Record<string, any> = Object.fromEntries(d.controls.map((c: any) => [c.id, c]))
const sel = ref('a')
const cur = computed(() => byId[sel.value])
const mapped = (id: string) => byId[id].kind !== 'unused'
const nf = new Intl.NumberFormat('ru-RU')
const events = (n: number) => {
  const a = n % 10
  const b = n % 100
  return a === 1 && b !== 11 ? 'событие' : a >= 2 && a <= 4 && (b < 12 || b > 14) ? 'события' : 'событий'
}
const maxEv = Math.max(...d.controls.map((c: any) => c.events))
const halo = (id: string) => 16 * Math.sqrt(byId[id].events / maxEv)

const W = 480
const H = 256
interface Shape { id: string, kind: 'circle' | 'rect' | 'dpad', x: number, y: number, r?: number, w?: number, h?: number, label?: string, badge?: [number, number] }
const shapes: Shape[] = [
  { id: 'lt', kind: 'rect', x: 26, y: 12, w: 78, h: 15, label: 'LT' },
  { id: 'lb', kind: 'rect', x: 26, y: 31, w: 78, h: 12, label: 'LB' },
  { id: 'rt', kind: 'rect', x: 376, y: 12, w: 78, h: 15, label: 'RT' },
  { id: 'rb', kind: 'rect', x: 376, y: 31, w: 78, h: 12, label: 'RB' },
  { id: 'ls', kind: 'circle', x: 62, y: 102, r: 22, badge: [30, 66] },
  { id: 'dp', kind: 'dpad', x: 84, y: 172, r: 22, badge: [118, 206] },
  { id: 'sel', kind: 'rect', x: 100, y: 64, w: 18, h: 10 },
  { id: 'start', kind: 'rect', x: 362, y: 64, w: 18, h: 10 },
  { id: 'y', kind: 'circle', x: 418, y: 78, r: 10, label: 'Y', badge: [418, 60] },
  { id: 'x', kind: 'circle', x: 395, y: 101, r: 10, label: 'X', badge: [372, 101] },
  { id: 'b', kind: 'circle', x: 441, y: 101, r: 10, label: 'B', badge: [464, 101] },
  { id: 'a', kind: 'circle', x: 418, y: 124, r: 10, label: 'A', badge: [418, 146] },
  { id: 'rs', kind: 'circle', x: 398, y: 176, r: 22 },
  { id: 'mode', kind: 'circle', x: 446, y: 214, r: 7 },
]
const cx = (s: Shape) => (s.kind === 'rect' ? s.x + (s.w || 0) / 2 : s.x)
const cy = (s: Shape) => (s.kind === 'rect' ? s.y + (s.h || 0) / 2 : s.y)
const fill = (id: string) => (mapped(id) ? 'rgba(217, 89, 38, 0.85)' : '#3a4252')
const grip = (side: 1 | -1) => {
  const o = side === 1 ? 0 : W
  const s = side
  const X = (v: number) => o + s * v
  return `M${X(120)},50 C${X(80)},44 ${X(30)},44 ${X(16)},74 C${X(2)},110 ${X(4)},180 ${X(18)},222 C${X(28)},250 ${X(70)},254 ${X(96)},236 C${X(110)},226 ${X(118)},214 ${X(126)},206 Z`
}
</script>

<template>
  <div class="ctl">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Схема контроллера: наведите на кнопку, чтобы увидеть её путь до игры">
      <!-- body -->
      <path :d="grip(1)" class="body" />
      <path :d="grip(-1)" class="body" />
      <rect x="118" y="52" width="244" height="156" rx="20" fill="#07090e" stroke="var(--axis)" stroke-width="2" />
      <rect x="128" y="62" width="224" height="136" rx="12" fill="#0e1a2c" />
      <text class="scr" x="240" y="118" text-anchor="middle">Pixel 10 · NTSD</text>
      <text class="scr2" x="240" y="136" text-anchor="middle">контроллер = джойстик 1 = игрок 3</text>

      <!-- halos: event counts -->
      <template v-for="s in shapes.filter(s => byId[s.id].events > 0)" :key="`h${s.id}`">
        <rect v-if="s.kind === 'rect'" :x="s.x - halo(s.id)" :y="s.y - halo(s.id)" :width="(s.w || 0) + 2 * halo(s.id)" :height="(s.h || 0) + 2 * halo(s.id)" :rx="5 + halo(s.id)" class="halo" :class="{ on: mapped(s.id) }" />
        <circle v-else :cx="cx(s)" :cy="cy(s)" :r="(s.r || 10) + halo(s.id)" class="halo" :class="{ on: mapped(s.id) }" />
      </template>

      <!-- controls -->
      <g v-for="s in shapes" :key="s.id" class="c" :class="{ sel: sel === s.id }" tabindex="0" role="button"
         :aria-label="byId[s.id].label" @pointerenter="sel = s.id" @focus="sel = s.id" @click="sel = s.id">
        <circle :cx="cx(s)" :cy="cy(s)" :r="Math.max(14, (s.r || 8) + 4)" class="hit" />
        <template v-if="s.kind === 'circle' && (s.r || 0) > 15">
          <circle :cx="s.x" :cy="s.y" :r="s.r" fill="#11151d" :stroke="mapped(s.id) ? 'var(--s2)' : '#4a5366'" stroke-width="2.5" class="m" />
          <circle :cx="s.x" :cy="s.y" :r="(s.r || 0) * 0.55" :fill="mapped(s.id) ? 'rgba(217, 89, 38, 0.55)' : '#2a3142'" />
        </template>
        <template v-else-if="s.kind === 'circle'">
          <circle :cx="s.x" :cy="s.y" :r="s.r" :fill="fill(s.id)" class="m" />
          <text v-if="s.label" class="bl" :x="s.x" :y="s.y + 3.8" text-anchor="middle">{{ s.label }}</text>
        </template>
        <template v-else-if="s.kind === 'dpad'">
          <path :d="`M${s.x - 7},${s.y - 21} h14 v14 h14 v14 h-14 v14 h-14 v-14 h-14 v-14 h14 Z`" :fill="fill(s.id)" class="m" />
        </template>
        <template v-else>
          <rect :x="s.x" :y="s.y" :width="s.w" :height="s.h" rx="5" :fill="fill(s.id)" class="m" />
          <text v-if="s.label" class="bl sm" :x="cx(s)" :y="cy(s) + 3.4" text-anchor="middle">{{ s.label }}</text>
        </template>
      </g>

      <!-- counts on the controls that reach the game -->
      <g v-for="s in shapes.filter(s => s.badge)" :key="`b${s.id}`">
        <text class="badge" :x="s.badge![0]" :y="s.badge![1] + 3.5" text-anchor="middle">{{ byId[s.id].events }}</text>
      </g>
    </svg>

    <div class="legend">
      <span><i class="k on" />доходит до игры</span>
      <span><i class="k" />у игры нет роли</span>
      <span><i class="k halo-k" />ореол и число — события evdev за запись 18:51–18:58 · схема, не чертёж</span>
    </div>

    <div class="panel" aria-live="polite">
      <div class="ph">
        <span class="nm">{{ cur.label }}</span>
        <span class="chip" :class="{ on: mapped(sel) }">{{ mapped(sel) ? 'доходит до игры' : 'без роли в игре' }}</span>
        <span class="ev"><b>{{ nf.format(cur.events) }}</b> {{ events(cur.events) }}</span>
      </div>
      <div class="rows">
        <span class="k2">HID-интерфейс 0 · evdev</span><span class="mono">{{ cur.evdev }}</span>
        <span class="k2">Android</span><span class="mono">{{ cur.android }}</span>
        <span class="k2">порт → WinMM</span><span>{{ cur.port }}</span>
        <span class="k2">игрок 3 по умолчанию</span><span>{{ cur.game }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ctl { display: flex; flex-direction: column; gap: 4px; }
.body { fill: #1b2130; stroke: #4a5366; stroke-width: 2; }
.scr { font-family: var(--font-pixel); font-size: 15px; fill: var(--chakra); }
.scr2 { font-family: var(--font-sans); font-size: 10.5px; fill: var(--ink-2); }
.halo { fill: rgba(141, 145, 156, 0.18); pointer-events: none; }
.halo.on { fill: rgba(217, 89, 38, 0.22); }
.c { cursor: pointer; outline: none; }
.hit { fill: transparent; }
.c .m { transition: stroke 0.15s ease; }
.c.sel .m { stroke: var(--ink); stroke-width: 2.5; }
.bl { font-family: var(--font-sans); font-size: 10.5px; font-weight: 700; fill: #fff; pointer-events: none; }
.bl.sm { font-size: 10px; }
.badge { font-family: var(--font-sans); font-size: 10.5px; font-weight: 650; fill: var(--ink); pointer-events: none; }
.legend { display: flex; flex-wrap: wrap; gap: 2px 12px; font-size: 0.6rem; color: var(--ink-2); }
.legend span { display: inline-flex; align-items: center; gap: 5px; }
.k { width: 10px; height: 10px; border-radius: 3px; background: #3a4252; display: inline-block; }
.k.on { background: rgba(217, 89, 38, 0.85); }
.k.halo-k { border-radius: 50%; background: rgba(217, 89, 38, 0.3); }
.panel { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: 4px 10px 5px; margin-top: 1px; }
.ph { display: flex; align-items: baseline; gap: 8px; }
.nm { font-family: var(--font-display); font-weight: 700; font-size: 0.95rem; color: var(--ink); }
.chip { font-size: 0.6rem; border-radius: 999px; padding: 0 7px; border: 1px solid var(--axis); color: var(--ink-2); }
.chip.on { border-color: rgba(217, 89, 38, 0.7); color: var(--ink); }
.ev { margin-left: auto; font-size: 0.66rem; color: var(--ink-2); }
.ev b { color: var(--ink); font-size: 0.8rem; }
.rows { display: grid; grid-template-columns: 9.6rem 1fr; gap: 0 8px; font-size: 0.64rem; line-height: 1.32; margin-top: 2px; color: var(--ink); }
.k2 { color: var(--muted); }
.mono { font-family: var(--font-mono); font-size: 0.62rem; }
</style>
