<script setup lang="ts">
import data from '../data/xplat.json'

// One square = 100 lines of Swift in native/Sources at 2fe64be (5 Oct, nine-host baseline).
// Blocks stand on one baseline like a skyline: the core, the new shared runtime, one adapter per host.
// Orange squares: core lines changed since main (74be317). Dashed box: the Mac layer on main.
const t = (data as any).targets
const nine = t.nine as Record<string, number>
const main = t.main as Record<string, number>
const cd = (data as any).core_diff
const changed = cd.added + cd.deleted

const S = 9
const P = 11
const ROWS = 10
const base = 166
const top = base - ROWS * P

interface Block { key: string, name: string, sub?: string, lines: number, x: number, color: string, wide?: boolean }
const blocks: Block[] = [
  { key: 'core', name: 'ядро игры', sub: 'NTSDCore · правила, ИИ, режимы, записи', lines: nine.core, x: 0, color: 'var(--core)', wide: true },
  { key: 'runtime', name: 'рантайм', sub: 'NTSDRuntime · новый', lines: nine.runtime, x: 376, color: 'var(--s1)', wide: true },
  { key: 'mac', name: 'macOS', sub: 'AppKit', lines: nine.mac, x: 522, color: 'var(--s3)', wide: true },
  { key: 'sdl', name: 'SDL3', sub: 'Linux · Windows', lines: nine.sdl, x: 630, color: 'var(--s3)' },
  { key: 'android', name: 'Android', lines: nine.android, x: 716, color: 'var(--s3)' },
  { key: 'ios', name: 'iPad', lines: nine.ios, x: 784, color: 'var(--s3)' },
  { key: 'headless', name: 'без окна', lines: nine.headless, x: 828, color: 'var(--s3)' },
]

interface Sq { x: number, y: number, w: number }
function squares(b: Block): Sq[] {
  const n = b.lines / 100
  const full = Math.floor(n)
  const frac = n - full
  const count = full + (frac > 0.05 ? 1 : 0)
  const out: Sq[] = []
  for (let i = 0; i < count; i++) {
    const col = Math.floor(i / ROWS)
    const row = i % ROWS
    out.push({ x: b.x + col * P, y: base - (row + 1) * P + (P - S), w: i === full ? Math.max(2, S * frac) : S })
  }
  return out
}
const all = blocks.map(b => ({ b, sq: squares(b) }))
const heightOf = (b: Block) => Math.min(ROWS, Math.ceil(b.lines / 100)) * P
const widthOf = (b: Block) => Math.ceil(b.lines / 100 / ROWS) * P - (P - S)

// the changed lines, drawn over the last full squares of the core block
const coreSq = all[0].sq
const nChanged = changed / 100
const changedSq: Sq[] = []
{
  let left = nChanged
  let i = coreSq.length - 2
  const picked: Sq[] = []
  while (left > 0 && i >= 0) {
    picked.unshift({ ...coreSq[i], w: S * Math.min(1, left) })
    left -= 1
    i--
  }
  changedSq.push(...picked)
}
const hi = changedSq.reduce((a, s) => (s.y < a.y ? s : a), changedSq[0])

const ghostCols = Math.ceil(main.mac / 100 / ROWS)
const ghost = { x: blocks[2].x - 3, y: top - 3, w: ghostCols * P - (P - S) + 6, h: ROWS * P + 1 }
const fmt = (n: number) => n.toLocaleString('ru-RU')
</script>

<template>
  <div class="waffle">
    <svg viewBox="0 0 884 236" width="100%" role="img" aria-label="Строки Swift по модулям: один квадрат — сто строк">
      <!-- the Mac layer on main, as a dashed outline behind today's Mac adapter -->
      <rect :x="ghost.x" :y="ghost.y" :width="ghost.w" :height="ghost.h" rx="3" fill="rgba(255,255,255,0.025)" stroke="var(--muted)" stroke-dasharray="3 3" />
      <text class="ghost" :x="ghost.x" :y="ghost.y - 7">на main было <tspan class="b">{{ fmt(main.mac) }}</tspan></text>

      <g v-for="{ b, sq } in all" :key="b.key">
        <rect v-for="(s, i) in sq" :key="i" :x="s.x" :y="s.y" :width="s.w" :height="S" rx="1.5" :fill="b.color" />
      </g>
      <rect v-for="(s, i) in changedSq" :key="`c${i}`" :x="s.x" :y="s.y" :width="s.w" :height="S" rx="1.5" fill="var(--s2)" />

      <!-- callout -->
      <path :d="`M${hi.x + S / 2},${hi.y - 3} V${top - 9} H0`" fill="none" stroke="var(--s2)" />
      <circle :cx="hi.x + S / 2" :cy="hi.y - 3" r="2" fill="var(--s2)" />
      <text class="call" x="0" :y="top - 30">изменено {{ fmt(changed) }} строк из {{ fmt(nine.core) }}</text>
      <text class="callsub" x="0" :y="top - 15">+{{ cd.added }} / −{{ cd.deleted }} в {{ cd.files.length }} файлах ядра — переносимость, а не поведение</text>

      <!-- values above host blocks -->
      <template v-for="{ b } in all" :key="`v${b.key}`">
        <text v-if="!b.wide" class="val" :x="b.x" :y="base - heightOf(b) - 6">{{ fmt(b.lines) }}</text>
      </template>

      <!-- names below the baseline -->
      <line x1="0" x2="884" :y1="base + 1.5" :y2="base + 1.5" stroke="var(--axis)" />
      <template v-for="{ b } in all" :key="`n${b.key}`">
        <text class="nm" :x="b.x" :y="base + 17">{{ b.name }}<tspan v-if="b.wide" class="nmv" dx="6">{{ fmt(b.lines) }}</tspan></text>
        <text v-if="b.sub" class="sub" :x="b.x" :y="base + 30">{{ b.sub }}</text>
      </template>

      <g class="br">
        <path :d="`M0,${base + 42} v5 H${widthOf(blocks[0])} v-5`" />
        <text :x="widthOf(blocks[0]) / 2" :y="base + 60" text-anchor="middle">одно ядро на все платформы</text>
        <path :d="`M${blocks[1].x},${base + 42} v5 H${blocks[1].x + widthOf(blocks[1])} v-5`" />
        <text :x="blocks[1].x + widthOf(blocks[1]) / 2" :y="base + 60" text-anchor="middle">окно, звук, сеть</text>
        <path :d="`M${blocks[2].x},${base + 42} v5 H880 v-5`" />
        <text :x="(blocks[2].x + 880) / 2" :y="base + 60" text-anchor="middle">хост — сотни строк на платформу</text>
      </g>
    </svg>
    <div class="key">
      <span><i style="background: var(--core)" />ядро без изменений</span>
      <span><i style="background: var(--s2)" />изменённые строки ядра</span>
      <span><i style="background: var(--s1)" />общий рантайм</span>
      <span><i style="background: var(--s3)" />адаптер хоста</span>
      <span><i class="dash" />Mac-слой на main</span>
      <span class="muted">один квадрат — 100 строк Swift · ещё {{ nine.freetype }} строк — текст через FreeType, {{ nine.music }} — декодер музыки ALAC</span>
    </div>
  </div>
</template>

<style scoped>
.waffle {
  --core: #4c5466;
}
.val {
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 650;
  fill: var(--ink);
  font-variant-numeric: tabular-nums;
}
.nm {
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 650;
  fill: var(--ink);
}
.nmv {
  font-weight: 700;
  fill: var(--ink);
}
.sub {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
}
.ghost {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
}
.ghost.b {
  font-weight: 650;
  fill: var(--ink-2);
}
.call {
  font-family: var(--font-sans);
  font-size: 12.5px;
  font-weight: 700;
  fill: var(--ink);
}
.callsub {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--ink-2);
}
.br path {
  fill: none;
  stroke: var(--axis);
}
.br text {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--ink-2);
}
.key {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem 1rem;
  font-size: 0.62rem;
  color: var(--ink-2);
  margin-top: 0.15rem;
}
.key i {
  display: inline-block;
  width: 9px;
  height: 9px;
  border-radius: 2px;
  margin-right: 0.35rem;
  vertical-align: -1px;
}
.key i.dash {
  border: 1px dashed var(--muted);
  background: transparent;
}
</style>
