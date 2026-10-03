<script setup lang="ts">
// Safety stops on three lanes. A diamond marks the stop; the bar after it shows how long the dependent
// task waited before it moved on (never a reversal of the decision); the dotted line is the ISO hunt.
interface Stop { id: string, lane: number, sub: number, t: string, end?: string, hours?: string, style?: 'bar' | 'dots' | 'none', left?: boolean }
const lanes = ['Codex · GPT-6 Astra', 'Codex · инструменты', 'Claude Code · Opus 5.5']
const stops: Stop[] = [
  { id: '1', lane: 0, sub: 0, t: '2026-09-09T15:34Z', end: '2026-09-09T18:05Z', hours: '2,5 ч' },
  { id: '2', lane: 0, sub: 1, t: '2026-09-09T23:10Z', end: '2026-09-12T06:54Z', hours: '55,7 ч*' },
  { id: '3', lane: 0, sub: 0, t: '2026-09-12T00:30Z', end: '2026-09-12T06:12Z', hours: '5,7 ч' },
  { id: 'S', lane: 1, sub: 0, t: '2026-09-10T02:57Z', end: '2026-09-26T19:40Z', hours: 'урывками', style: 'dots' },
  { id: '4', lane: 1, sub: 1, t: '2026-09-26T19:02Z', hours: 'не повторяли', style: 'none' },
  { id: '5', lane: 2, sub: 0, t: '2026-10-01T18:06Z', end: '2026-10-02T16:26Z', hours: '22,3 ч' },
  { id: 'M', lane: 2, sub: 1, t: '2026-10-03T18:57Z', style: 'none', hours: '≈ 0', left: true },
]
const W = 900
const m = { l: 150, r: 14, t: 6 }
const LH = 31
const H = m.t + lanes.length * LH + 22
const T0 = Date.parse('2026-09-07T00:00Z')
const T1 = Date.parse('2026-10-04T00:00Z')
const x = (t: string) => m.l + ((Date.parse(t) - T0) / (T1 - T0)) * (W - m.l - m.r)
const y = (s: Stop) => m.t + s.lane * LH + 10 + s.sub * 12
const ticks = ['2026-09-07', '2026-09-14', '2026-09-21', '2026-09-28'].map(d => ({ d, label: `${Number(d.slice(8, 10))} ${d.slice(5, 7) === '09' ? 'сен' : 'окт'}` }))
</script>

<template>
  <div>
    <div class="legend">
      <span><svg width="12" height="12"><rect x="2.5" y="2.5" width="7" height="7" transform="rotate(45 6 6)" fill="var(--critical)" /></svg>остановка</span>
      <span><i class="bar" />сколько ждала зависимая задача</span>
      <span><i class="dots" />ISO искали урывками</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Остановки по дням">
      <g v-for="(l, i) in lanes" :key="l">
        <rect :x="0" :y="m.t + i * LH" :width="W" :height="LH - 4" rx="6" :fill="i % 2 ? 'rgba(255,255,255,0.02)' : 'rgba(255,255,255,0.04)'" />
        <text :x="10" :y="m.t + i * LH + LH / 2 + 2" class="lane">{{ l }}</text>
      </g>
      <g v-for="tk in ticks" :key="tk.d">
        <line :x1="x(`${tk.d}T00:00Z`)" :x2="x(`${tk.d}T00:00Z`)" :y1="m.t" :y2="H - 18" stroke="var(--grid)" />
        <text :x="x(`${tk.d}T00:00Z`)" :y="H - 6" text-anchor="middle" class="tick">{{ tk.label }}</text>
      </g>
      <g v-for="s in stops" :key="s.id">
        <rect v-if="s.end && (s.style ?? 'bar') === 'bar'" :x="x(s.t)" :y="y(s) - 4" :width="Math.max(2, x(s.end) - x(s.t))" height="8" rx="3" fill="rgba(250, 178, 25, 0.45)" />
        <line v-if="s.end && s.style === 'dots'" :x1="x(s.t)" :x2="x(s.end)" :y1="y(s)" :y2="y(s)" stroke="var(--warning)" stroke-width="1.5" stroke-dasharray="1.5 4" stroke-linecap="round" />
        <rect :x="x(s.t) - 5" :y="y(s) - 5" width="10" height="10" :transform="`rotate(45 ${x(s.t)} ${y(s)})`" fill="var(--critical)" stroke="var(--bg)" stroke-width="1.3">
          <title>№ {{ s.id }} · {{ s.t }}</title>
        </rect>
        <text :x="x(s.t)" :y="y(s) + 3.2" text-anchor="middle" class="num">{{ s.id }}</text>
        <text :x="s.left ? x(s.t) - 9 : (s.end && s.style !== 'none' ? x(s.end) : x(s.t)) + 9" :y="y(s) + 3.5" :text-anchor="s.left ? 'end' : 'start'" class="hrs">{{ s.hours }}</text>
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
  margin-bottom: 0.15rem;
}
.legend span {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.bar {
  display: inline-block;
  width: 16px;
  height: 7px;
  border-radius: 3px;
  background: rgba(250, 178, 25, 0.45);
}
.dots {
  display: inline-block;
  width: 16px;
  border-top: 2px dotted var(--warning);
}
.lane {
  font-size: 10.5px;
  font-weight: 600;
  fill: var(--ink-2);
}
.tick {
  font-size: 9.5px;
  fill: var(--muted);
}
.num {
  font-size: 7.5px;
  font-weight: 700;
  fill: #fff;
}
.hrs {
  font-size: 10px;
  fill: var(--ink);
  font-variant-numeric: tabular-nums;
}
</style>
