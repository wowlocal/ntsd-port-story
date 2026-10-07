<script setup lang="ts">
import data from '../data/xplat.json'

// ONLINE GAME across platforms (pair_probe.py --cross): every arrow is one run, from the host to the client.
// All seven runs pass with the retained run's random-table hash.
const on = (data as any).online
const pairs = on.pairs as { host: string, client: string, result: string, rng: string }[]
const rng = pairs[0].rng as string
const same = pairs.every(p => p.rng === rng && p.result === 'PASS')

const W = 884
const H = 262
interface N { key: string, name: string, env: string, x: number, y: number }
const nodes: N[] = [
  { key: 'local', name: 'macOS', env: 'этот Mac · сокеты Darwin', x: 442, y: 128 },
  { key: 'wine', name: 'Windows', env: 'CrossOver · настоящий Winsock', x: 140, y: 52 },
  { key: 'android', name: 'Android', env: 'эмулятор · сокеты Bionic', x: 744, y: 52 },
  { key: 'linux', name: 'Linux', env: 'контейнер OrbStack', x: 442, y: 226 },
]
const nw = 176
const nh = 40
const node = (k: string) => nodes.find(n => n.key === k) as N

// point on the node's border towards (tx, ty)
function edgePoint(n: N, tx: number, ty: number) {
  const dx = tx - n.x
  const dy = ty - n.y
  const sx = (nw / 2 + 6) / Math.abs(dx || 1e-6)
  const sy = (nh / 2 + 6) / Math.abs(dy || 1e-6)
  const s = Math.min(sx, sy)
  return { x: n.x + dx * s, y: n.y + dy * s }
}
const twoWay = (p: { host: string, client: string }) => pairs.some(q => q.host === p.client && q.client === p.host)
const arrows = pairs.map((p) => {
  const a = node(p.host)
  const b = node(p.client)
  const bend = twoWay(p) ? 16 : 0
  const mx = (a.x + b.x) / 2
  const my = (a.y + b.y) / 2
  const len = Math.hypot(b.x - a.x, b.y - a.y)
  // normal to the segment, so the two directions of a pair bow to opposite sides
  const nx = -(b.y - a.y) / len
  const ny = (b.x - a.x) / len
  const cxp = mx + nx * bend * 2
  const cyp = my + ny * bend * 2
  const s = edgePoint(a, cxp, cyp)
  const e = edgePoint(b, cxp, cyp)
  return { ...p, d: `M${s.x.toFixed(1)},${s.y.toFixed(1)} Q${cxp.toFixed(1)},${cyp.toFixed(1)} ${e.x.toFixed(1)},${e.y.toFixed(1)}` }
})
const label: Record<string, string> = { local: 'macOS', wine: 'Windows', android: 'Android', linux: 'Linux' }
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Онлайн-игра между платформами: семь пар хост-клиент">
    <defs>
      <marker id="og-arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0,0.8 L9,5 L0,9.2 Z" fill="var(--s2)" />
      </marker>
    </defs>
    <path v-for="(a, i) in arrows" :key="i" :d="a.d" fill="none" stroke="var(--s2)" stroke-width="2" marker-end="url(#og-arrow)">
      <title>хост {{ label[a.host] }} → клиент {{ label[a.client] }}: {{ a.result }}, таблица случайных чисел {{ a.rng.slice(0, 8) }}…</title>
    </path>
    <g v-for="n in nodes" :key="n.key">
      <rect :x="n.x - nw / 2" :y="n.y - nh / 2" :width="nw" :height="nh" rx="10" fill="var(--surface-2)" stroke="var(--axis)" />
      <text class="nn" :x="n.x" :y="n.y - 2" text-anchor="middle">{{ n.name }}</text>
      <text class="ne" :x="n.x" :y="n.y + 12" text-anchor="middle">{{ n.env }}</text>
    </g>
    <!-- the shared hash -->
    <g :transform="`translate(${W - 150}, 196)`">
      <text class="hk" x="0" y="0" text-anchor="middle">у всех семи пар одна таблица случайных чисел</text>
      <text class="hv" x="0" y="15" text-anchor="middle">SHA-256 {{ rng.slice(0, 16) }}…</text>
    </g>
    <g class="lg" :transform="`translate(0, ${H - 8})`">
      <line x1="0" x2="26" y1="-4" y2="-4" stroke="var(--s2)" stroke-width="2" marker-end="url(#og-arrow)" />
      <text x="34" y="0">одна партия: от хоста к клиенту · {{ pairs.length }} из {{ pairs.length }} {{ same ? 'прошли' : '' }}</text>
    </g>
  </svg>
</template>

<style scoped>
.nn {
  font-family: var(--font-sans);
  font-size: 13px;
  font-weight: 700;
  fill: var(--ink);
}
.ne {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--ink-2);
}
.hk {
  font-family: var(--font-sans);
  font-size: 11px;
  fill: var(--ink-2);
}
.hv {
  font-family: var(--font-mono);
  font-size: 11px;
  fill: var(--ink);
}
.lg text {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--ink-2);
}
</style>
