<script setup lang="ts">
import { computed } from 'vue'
import cov from '../data/evidence/exe-coverage.json'

// Squarified treemap of the 174 game-code functions of NTSD 2.4.exe, area = instructions.
// Three classes (all-pairs form → at most three categorical slots).
const W = 900
const H = 300
const cls = (s: string) => (s === 'recordedOrCompared' ? 'rec' : s === 'portedInsideComparedCallers' ? 'inside' : 'gap')
const color: Record<string, string> = { rec: 'var(--s1)', gap: 'var(--s2)', inside: 'var(--s3)' }

interface Item { entry: string, instructions: number, status: string, label?: string }
interface Rect { x: number, y: number, w: number, h: number, it: Item }

function worst(row: number[], side: number) {
  const s = row.reduce((a, b) => a + b, 0)
  const mx = Math.max(...row)
  const mn = Math.min(...row)
  return Math.max((side * side * mx) / (s * s), (s * s) / (side * side * mn))
}

function squarify(items: Item[], x: number, y: number, w: number, h: number): Rect[] {
  const total = items.reduce((a, b) => a + b.instructions, 0)
  const scale = (w * h) / total
  const areas = items.map(i => i.instructions * scale)
  const out: Rect[] = []
  let i = 0
  let cx = x
  let cy = y
  let cw = w
  let ch = h
  while (i < areas.length) {
    const side = Math.min(cw, ch)
    const row: number[] = [areas[i]]
    let j = i + 1
    while (j < areas.length && worst([...row, areas[j]], side) <= worst(row, side)) {
      row.push(areas[j])
      j++
    }
    const s = row.reduce((a, b) => a + b, 0)
    if (cw >= ch) {
      const rw = s / ch
      let yy = cy
      row.forEach((a, k) => {
        const rh = a / rw
        out.push({ x: cx, y: yy, w: rw, h: rh, it: items[i + k] })
        yy += rh
      })
      cx += rw
      cw -= rw
    }
    else {
      const rh = s / cw
      let xx = cx
      row.forEach((a, k) => {
        const rw = a / rh
        out.push({ x: xx, y: cy, w: rw, h: rh, it: items[i + k] })
        xx += rw
      })
      cy += rh
      ch -= rh
    }
    i = j
  }
  return out
}

const rects = computed(() => {
  const items = [...(cov as any).gameFunctions as Item[]].sort((a, b) => b.instructions - a.instructions)
  return squarify(items, 0, 0, W, H)
})
const fmt = new Intl.NumberFormat('ru-RU')
const short = (s?: string) => (s || '').replace(/\s*\(.*\)\s*/g, '').split(' / ')[0]
const totals = (cov as any).gameFunctionsByStatus
const legend = [
  { k: 'rec', label: `есть записи исполнения или сравнённый корпус — ${totals.functions.recordedOrCompared} функций` },
  { k: 'inside', label: `перенесены, исполняются внутри сравнённых вызывающих — ${totals.functions.portedInsideComparedCallers}` },
  { k: 'gap', label: `режимы разработчика и функции без установленной достижимости — ${totals.functions.developerModes + totals.functions.undocumentedOrUnported}` },
]
</script>

<template>
  <div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Карта 174 функций игрового кода EXE">
      <g v-for="r in rects" :key="r.it.entry">
        <rect
          :x="r.x + 1" :y="r.y + 1" :width="Math.max(0, r.w - 2)" :height="Math.max(0, r.h - 2)" rx="3"
          :fill="color[cls(r.it.status)]" :style="{ opacity: cls(r.it.status) === 'rec' ? 0.88 : 1 }"
        >
          <title>{{ r.it.entry }} · {{ fmt.format(r.it.instructions) }} инструкций · {{ r.it.label || 'без метки' }}</title>
        </rect>
        <template v-if="r.w > 74 && r.h > 30">
          <text :x="r.x + 6" :y="r.y + 15" class="addr">{{ r.it.entry }}</text>
          <text v-if="r.w > 110 && r.h > 44" :x="r.x + 6" :y="r.y + 29" class="lbl">{{ short(r.it.label).slice(0, Math.floor(r.w / 6.2)) }}</text>
        </template>
      </g>
    </svg>
    <div class="legend">
      <span v-for="l in legend" :key="l.k"><i class="swatch" :style="{ background: color[l.k] }" />{{ l.label }}</span>
    </div>
  </div>
</template>

<style scoped>
.addr {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 700;
  fill: #fff;
}
.lbl {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: rgba(255, 255, 255, 0.86);
}
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem 1.2rem;
  font-size: 0.68rem;
  color: var(--ink-2);
  margin-top: 0.35rem;
}
rect:hover {
  opacity: 0.7;
}
</style>
