<script setup lang="ts">
// One time axis with hand-placed labels: row > 0 above the axis, row < 0 below; `end` anchors the label left of the dot.
// `gap` is the distance between label rows.
interface Ev { t: string, label: string, sub?: string, row: number, end?: boolean, kind: string }
const props = withDefaults(defineProps<{
  events: Ev[]
  from: string
  to: string
  ticks?: string[]
  kinds: Record<string, { color: string, name: string }>
  height?: number
  axis?: number
  gap?: number
}>(), { ticks: () => [], height: 132, axis: 76, gap: 18 })
const W = 900
const m = { l: 14, r: 14 }
const x = (t: string) => m.l + ((Date.parse(t) - Date.parse(props.from)) / (Date.parse(props.to) - Date.parse(props.from))) * (W - m.l - m.r)
const labelY = (row: number) => props.axis + (row > 0 ? -12 - (row - 1) * props.gap : 20 + (-row - 1) * props.gap)
</script>

<template>
  <div>
    <div class="legend">
      <span v-for="(k, key) in kinds" :key="key"><i class="dot" :style="{ background: k.color }" />{{ k.name }}</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${height}`" width="100%" role="img" aria-label="Хронология">
      <rect x="0" y="0" :width="W" :height="height" rx="10" fill="rgba(255,255,255,0.025)" />
      <line :x1="m.l" :x2="W - m.r" :y1="axis" :y2="axis" stroke="var(--axis)" />
      <g v-for="t in ticks" :key="t">
        <line :x1="x(t)" :x2="x(t)" :y1="axis - 3" :y2="axis + 3" stroke="var(--axis)" />
        <text :x="x(t)" :y="height - 6" text-anchor="middle" class="tick">{{ t.slice(0, 4) }}</text>
      </g>
      <g v-for="e in events" :key="e.label">
        <line :x1="x(e.t)" :x2="x(e.t)" :y1="axis" :y2="labelY(e.row) + (e.row > 0 ? 4 : -10)" :stroke="kinds[e.kind].color" style="opacity: 0.55" />
        <circle :cx="x(e.t)" :cy="axis" r="4.5" :fill="kinds[e.kind].color" stroke="var(--bg)" stroke-width="1.5">
          <title>{{ e.t }} · {{ e.label }} {{ e.sub ?? '' }}</title>
        </circle>
        <text :x="x(e.t) + (e.end ? -4 : 4)" :y="labelY(e.row)" :text-anchor="e.end ? 'end' : 'start'" class="nm" :style="e.kind === 'port' ? { fill: 'var(--naruto)' } : undefined">{{ e.label }}<tspan v-if="e.sub" class="sub" dx="5">{{ e.sub }}</tspan></text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.2rem 1.1rem;
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
.tick {
  font-size: 9.5px;
  fill: var(--muted);
}
.nm {
  font-size: 10.5px;
  font-weight: 650;
  fill: var(--ink);
}
.sub {
  font-size: 9.5px;
  font-weight: 400;
  fill: var(--ink-2);
}
</style>
