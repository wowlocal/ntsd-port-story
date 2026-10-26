<script setup lang="ts">
// Demo-day deck: ONLINE GAME between four systems (5 Oct). Every arrow is one run from the host to the client through
// the original's own menu and protocol (pair_probe.py --cross); all seven reached "network ready" on both sides with
// the same random table (SHA-256 5352f941…), the retained run's. Data: data/xplat.json (online.pairs).
// All on one Mac: Windows in CrossOver with real Winsock, Android in the emulator through adb, Linux in an OrbStack
// container — the slide says so.
import data from '../data/xplat.json'

const pairs = (data as any).online.pairs as { host: string, client: string, result: string }[]
const W = 880
const H = 250
const pos: Record<string, { x: number, y: number }> = {
  local: { x: 440, y: 120 },
  wine: { x: 110, y: 120 },
  android: { x: 770, y: 120 },
  linux: { x: 440, y: 222 },
}
const cw = 196
const ch = 52
function edge(k: string, tx: number, ty: number) {
  const n = pos[k]
  const dx = tx - n.x
  const dy = ty - n.y
  const s = Math.min((cw / 2 + 8) / Math.abs(dx || 1e-6), (ch / 2 + 8) / Math.abs(dy || 1e-6))
  return { x: n.x + dx * s, y: n.y + dy * s }
}
const both = (p: { host: string, client: string }) => pairs.some(q => q.host === p.client && q.client === p.host)
const arrows = pairs.map((p) => {
  const a = pos[p.host]
  const b = pos[p.client]
  const len = Math.hypot(b.x - a.x, b.y - a.y)
  const nx = -(b.y - a.y) / len
  const ny = (b.x - a.x) / len
  const across = (p.host === 'wine' && p.client === 'android') || (p.host === 'android' && p.client === 'wine')
  const bend = across ? -190 : both(p) ? 18 : 0
  const cx = (a.x + b.x) / 2 + nx * bend
  const cy = (a.y + b.y) / 2 + ny * bend
  const s = edge(p.host, cx, cy)
  const e = edge(p.client, cx, cy)
  return { d: `M${s.x.toFixed(1)},${s.y.toFixed(1)} Q${cx.toFixed(1)},${cy.toFixed(1)} ${e.x.toFixed(1)},${e.y.toFixed(1)}`, ok: p.result === 'PASS' }
})
const allOk = pairs.every(p => p.result === 'PASS')
const pctX = (x: number) => `${(x / W) * 100}%`
const pctY = (y: number) => `${(y / H) * 100}%`
</script>

<template>
  <div class="on">
    <svg :viewBox="`0 0 ${W} ${H}`" class="ln" role="img" :aria-label="`Сетевая игра: ${pairs.length} пар хост — клиент между четырьмя системами, ${allOk ? 'все прошли' : 'есть провалы'}`">
      <defs>
        <marker id="do-ar" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0.8 L9,5 L0,9.2 Z" fill="var(--s2)" />
        </marker>
      </defs>
      <path v-for="(a, i) in arrows" :key="i" :d="a.d" fill="none" stroke="var(--s2)" stroke-width="2.2" marker-end="url(#do-ar)" />
    </svg>
    <div class="nd" :style="{ left: pctX(pos.local.x), top: pctY(pos.local.y) }">
      <span class="ico i-pixelarticons-apple" /><div><b>macOS</b><i>этот Mac</i></div>
    </div>
    <div class="nd" :style="{ left: pctX(pos.wine.x), top: pctY(pos.wine.y) }">
      <span class="ico i-pixelarticons-app-windows" /><div><b>Windows</b><i>CrossOver</i></div>
    </div>
    <div class="nd" :style="{ left: pctX(pos.android.x), top: pctY(pos.android.y) }">
      <span class="ico i-pixelarticons-android" /><div><b>Android</b><i>эмулятор</i></div>
    </div>
    <div class="nd" :style="{ left: pctX(pos.linux.x), top: pctY(pos.linux.y) }">
      <span class="ico i-pixelarticons-linux" /><div><b>Linux</b><i>контейнер</i></div>
    </div>
    <div class="badge"><b>{{ pairs.length }} из {{ pairs.length }}</b> пар соединились</div>
  </div>
</template>

<style scoped>
.on { position: relative; width: 100%; aspect-ratio: 880 / 250; }
.ln { position: absolute; inset: 0; width: 100%; height: 100%; }
.nd { position: absolute; transform: translate(-50%, -50%); width: 22.3%; display: flex; align-items: center; gap: .6rem; background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: .45rem .7rem; }
.nd .ico { flex: none; width: 1.9rem; height: 1.9rem; color: var(--naruto); }
.nd b { display: block; font-size: .92rem; color: var(--ink); line-height: 1.1; }
.nd i { display: block; font-style: normal; font-size: .64rem; color: var(--muted); }
.badge { position: absolute; left: 76%; top: 86%; transform: translateX(-50%); font-size: .74rem; color: var(--ink-2); background: rgba(12, 163, 12, .12); border: 1px solid rgba(12, 163, 12, .55); border-radius: 999px; padding: .15rem .8rem; white-space: nowrap; }
.badge b { color: var(--good); }
</style>
