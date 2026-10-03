<script setup lang="ts">
// Two time scales on purpose: twenty years of hand-made rewrites, then three months of 2026.
interface Ev { t: string, label: string, sub?: string, row: number, end?: boolean, kind: 'old' | 'ai' | 'port' }
const old: Ev[] = [
  { t: '2004-03-06', label: '2004 · OpenTTD', sub: 'Transport Tycoon → C', row: 1, kind: 'old' },
  { t: '2008-06-01', label: '2008 · OpenMW', sub: 'движок Morrowind', row: -1, kind: 'old' },
  { t: '2014-04-02', label: '2014 · OpenRCT2', sub: '≈ 250 участников', row: 1, kind: 'old' },
  { t: '2018-04-01', label: '2018 · Devilution', sub: 'Diablo', row: -1, kind: 'old' },
  { t: '2019-07-01', label: '2019 · SM64', sub: 'побайтовая декомпиляция', row: 2, kind: 'old' },
  { t: '2021-11-01', label: '2021 · Ocarina of Time', sub: '21 месяц до 100 %', row: -2, end: true, kind: 'old' },
  { t: '2024-05-10', label: '2024 · Zelda 64: Recompiled', row: 1, end: true, kind: 'old' },
  { t: '2025-03-01', label: '2025 · Unleashed Recomp', row: -1, end: true, kind: 'old' },
]
const now: Ev[] = [
  { t: '2026-07-24', label: '24 июл · benilla', sub: 'WoW 1.12.1, ≈ 3 месяца с Claude', row: 1, kind: 'ai' },
  { t: '2026-08-13', label: '13 авг · Touhou 8', sub: 'агенты', row: -1, kind: 'ai' },
  { t: '2026-09-07', label: '7 сен · NTSD', sub: 'старт спринта', row: -2, kind: 'port' },
  { t: '2026-09-08', label: '8 сен · Skate 3 Rust Engine', row: 1, end: true, kind: 'ai' },
  { t: '2026-09-09', label: '9 сен · Melee', sub: 'декомпиляция — 100 %', row: 2, kind: 'ai' },
  { t: '2026-09-13', label: '13 сен · IW4L', sub: 'MW2, «written by an LLM»', row: -1, kind: 'ai' },
  { t: '2026-09-27', label: '27 сен · OpenLF2', row: 1, end: true, kind: 'ai' },
  { t: '2026-10-03', label: '3 окт · NTSD v0.4.0', row: 3, end: true, kind: 'port' },
]
const W = 900
const PH = 136
const m = { l: 18, r: 18 }
const panels = [
  { key: 'old', title: 'до ИИ: годы и десятки людей', evs: old, from: Date.parse('2003-01-01'), to: Date.parse('2026-01-01'), y0: 0, axis: 74 },
  { key: 'now', title: '2026: один человек и агенты — месяцы и недели', evs: now, from: Date.parse('2026-07-12'), to: Date.parse('2026-10-08'), y0: PH + 10, axis: 84 },
]
const H = PH * 2 + 10
const px = (p: typeof panels[number], t: number) => m.l + ((t - p.from) / (p.to - p.from)) * (W - m.l - m.r)
const axisY = (p: typeof panels[number]) => p.y0 + p.axis
const labelY = (p: typeof panels[number], row: number) => axisY(p) + (row > 0 ? -12 - (row - 1) * 18 : 20 + (-row - 1) * 18)
const color = { old: '#8d919c', ai: 'var(--s1)', port: 'var(--naruto)' }
</script>

<template>
  <div>
    <div class="legend">
      <span><i class="dot" style="background: #8d919c" />без ИИ</span>
      <span><i class="dot" style="background: var(--s1)" />с ИИ-агентами</span>
      <span><i class="dot" style="background: var(--naruto)" />этот порт</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Переписывания игр: 2004–2025 и 2026">
      <g v-for="p in panels" :key="p.key">
        <rect :x="0" :y="p.y0" :width="W" :height="PH" rx="10" :fill="p.key === 'now' ? 'rgba(57,135,229,0.06)' : 'rgba(255,255,255,0.025)'" />
        <text :x="12" :y="p.y0 + 15" class="ptitle">{{ p.title }}</text>
        <line :x1="m.l" :x2="W - m.r" :y1="axisY(p)" :y2="axisY(p)" stroke="var(--axis)" />
        <g v-for="e in p.evs" :key="e.label">
          <line :x1="px(p, Date.parse(e.t))" :x2="px(p, Date.parse(e.t))" :y1="axisY(p)" :y2="labelY(p, e.row) + (e.row > 0 ? 4 : -10)" :stroke="color[e.kind]" style="opacity: 0.55" />
          <circle :cx="px(p, Date.parse(e.t))" :cy="axisY(p)" r="4.5" :fill="color[e.kind]" stroke="var(--bg)" stroke-width="1.5">
            <title>{{ e.t }} · {{ e.label }} {{ e.sub ?? '' }}</title>
          </circle>
          <text :x="px(p, Date.parse(e.t)) + (e.end ? -4 : 4)" :y="labelY(p, e.row)" :text-anchor="e.end ? 'end' : 'start'" class="nm" :class="e.kind">{{ e.label }}<tspan v-if="e.sub" class="sub" dx="5">{{ e.sub }}</tspan></text>
        </g>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.legend {
  display: flex;
  gap: 1.1rem;
  font-size: 0.62rem;
  color: var(--ink-2);
  margin-bottom: 0.2rem;
}
.dot {
  display: inline-block;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  margin-right: 0.35rem;
  vertical-align: -1px;
}
.ptitle {
  font-size: 10.5px;
  font-weight: 600;
  fill: var(--ink-2);
}
.tick {
  font-size: 9.5px;
  fill: var(--muted);
}
.nm {
  font-size: 10.5px;
  font-weight: 650;
  fill: var(--ink);
}
.nm.port {
  fill: var(--naruto);
}
.sub {
  font-size: 9.5px;
  font-weight: 400;
  fill: var(--ink-2);
}
</style>
