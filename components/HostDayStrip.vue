<script setup lang="ts">
import data from '../data/xplat.json'
import loop from '../data/loop.json'

// 74 commits from the plan (3 Oct 20:11) to ONLINE GAME across platforms (5 Oct 02:23), one lane per platform.
// Lanes come from scripts/collect_xplat.py (by what each commit changed); human turns from data/loop.json.
interface C { hash: string, time: string, subject: string, lane: string, milestone?: string }
const commits = (data as any).commits as C[]

const W = 884
const x0 = 120
const x1 = W - 6
const H0 = 20 * 60 // 3 Oct 20:00 in minutes of that day
const HOURS = 31
const px = (x1 - x0) / HOURS
const hourOf = (iso: string) => {
  const d = Number(iso.slice(8, 10)) - 3
  const h = Number(iso.slice(11, 13))
  const m = Number(iso.slice(14, 16))
  return (d * 1440 + h * 60 + m - H0) / 60
}
const X = (h: number) => x0 + h * px

const lanes = [
  { key: 'human', name: 'человек' },
  { key: 'core', name: 'ядро, рантайм' },
  { key: 'linux', name: 'Linux' },
  { key: 'macsdl', name: 'macOS SDL' },
  { key: 'windows', name: 'Windows' },
  { key: 'ipad', name: 'iPad' },
  { key: 'android', name: 'Android' },
  { key: 'matrix', name: 'стенд и релиз' },
]
const LH = 22
const head = 70
const laneY = (k: string) => head + lanes.findIndex(l => l.key === k) * LH + LH / 2
const bottom = head + lanes.length * LH
const count = (k: string) => commits.filter(c => c.lane === k).length

// human turns typed in this window (session start 20:08:25 local)
const start = 8 / 60 + 25 / 3600
const human = ((loop as any).human as number[]).map(t => start + t / 60).filter(h => h >= 0 && h <= HOURS)

// milestones on the strip, placed by hand in two tiers (end: label to the left of its leader)
// a label in tier 1 never covers the leader of a tier-0 milestone
const SHOW: Record<string, { tier: number, end?: boolean }> = {
  '65c6916': { tier: 0 },
  '5dd1933': { tier: 0 },
  'a72ae97': { tier: 1 },
  'a8ed861': { tier: 0 },
  '8f6d1eb': { tier: 1 },
  '07bc662': { tier: 1, end: true },
  '2fe64be': { tier: 0, end: true },
}
const placed = commits.filter(c => SHOW[c.hash]).map(c => ({ ...c, x: X(hourOf(c.time)), tier: SHOW[c.hash].tier, anchorEnd: !!SHOW[c.hash].end }))
const tierY = (t: number) => 22 + t * 25

const ticks = Array.from({ length: HOURS / 2 + 1 }, (_, i) => i * 2).filter(h => h <= HOURS)
const clock = (h: number) => String((20 + h) % 24).padStart(2, '0')
const midnights = [4, 28]
const nights = [[4, 10], [28, 31]]
const lock = [16 + 20 / 60, 23 + 45 / 60] // 4 Oct 12:20 → 19:45
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${bottom + 30}`" width="100%" role="img" aria-label="30 часов: коммиты по платформам">
    <defs>
      <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
        <line x1="0" y1="0" x2="0" y2="6" stroke="rgba(255,255,255,0.09)" stroke-width="2" />
      </pattern>
    </defs>

    <!-- night and the locked screen -->
    <rect v-for="(n, i) in nights" :key="`n${i}`" :x="X(n[0])" :y="head" :width="(n[1] - n[0]) * px" :height="bottom - head" fill="rgba(57,135,229,0.06)" />
    <text v-for="(n, i) in nights" :key="`nt${i}`" class="band" :x="X(n[0]) + 4" :y="bottom - 4">ночь</text>
    <rect :x="X(lock[0])" :y="head" :width="(lock[1] - lock[0]) * px" :height="bottom - head" fill="url(#hatch)" />
    <text class="band" :x="X(lock[0] + 1.6)" :y="laneY('macsdl') + LH / 2 + 3.5">экран Mac заблокирован</text>

    <!-- lanes -->
    <g v-for="l in lanes" :key="l.key">
      <line :x1="x0" :x2="x1" :y1="laneY(l.key)" :y2="laneY(l.key)" stroke="var(--grid)" />
      <text class="lane" :class="{ hum: l.key === 'human' }" :x="x0 - 10" :y="laneY(l.key) + 3.5" text-anchor="end">{{ l.name }}<tspan v-if="l.key !== 'human'" class="cnt" dx="5">{{ count(l.key) }}</tspan></text>
    </g>

    <!-- hour axis -->
    <line :x1="x0" :x2="x1" :y1="bottom" :y2="bottom" stroke="var(--axis)" />
    <g v-for="h in ticks" :key="`t${h}`">
      <line :x1="X(h)" :x2="X(h)" :y1="bottom" :y2="bottom + 4" stroke="var(--axis)" />
      <text class="tick" :x="X(h)" :y="bottom + 15" text-anchor="middle">{{ clock(h) }}</text>
    </g>
    <g v-for="h in midnights" :key="`m${h}`">
      <line :x1="X(h)" :x2="X(h)" :y1="head - 4" :y2="bottom" stroke="var(--axis)" stroke-dasharray="2 3" />
      <text class="day" :x="X(h) + 4" :y="bottom + 27">{{ h === 4 ? '4 октября' : '5 октября' }}</text>
    </g>
    <text class="day" :x="x0" :y="bottom + 27">3 октября</text>

    <!-- human turns -->
    <circle v-for="(h, i) in human" :key="`h${i}`" :cx="X(h)" :cy="laneY('human')" r="4" fill="var(--s1)" stroke="var(--bg)" stroke-width="1.5" />

    <!-- milestone leaders and labels -->
    <g v-for="m in placed" :key="`ml${m.hash}`">
      <line :x1="m.x" :x2="m.x" :y1="tierY(m.tier) + 5" :y2="laneY(m.lane) - 6" stroke="var(--axis)" />
      <text class="ms" :x="m.x" :y="tierY(m.tier)" :text-anchor="m.anchorEnd ? 'end' : 'start'" :dx="m.anchorEnd ? -3 : 3">{{ m.milestone }}</text>
      <text class="mst" :x="m.x" :y="tierY(m.tier) - 11" :text-anchor="m.anchorEnd ? 'end' : 'start'" :dx="m.anchorEnd ? -3 : 3">{{ m.time.slice(11, 16) }} · {{ m.hash }}</text>
    </g>

    <!-- commits -->
    <g v-for="c in commits" :key="c.hash">
      <circle :cx="X(hourOf(c.time))" :cy="laneY(c.lane)" :r="SHOW[c.hash] ? 5.5 : 3.6" :fill="SHOW[c.hash] ? 'var(--naruto)' : 'var(--s2)'" stroke="var(--bg)" stroke-width="1.5">
        <title>{{ c.time.slice(8, 10) }}.10 {{ c.time.slice(11, 16) }} · {{ c.hash }} · {{ c.subject }}</title>
      </circle>
    </g>
  </svg>
</template>

<style scoped>
.lane {
  font-family: var(--font-sans);
  font-size: 11px;
  font-weight: 600;
  fill: var(--ink);
}
.lane.hum {
  fill: var(--chakra);
}
.cnt {
  font-weight: 400;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.tick {
  font-family: var(--font-mono);
  font-size: 9.5px;
  fill: var(--muted);
}
.day {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--ink-2);
}
.band {
  font-family: var(--font-sans);
  font-size: 9.5px;
  fill: var(--muted);
  font-style: italic;
}
.ms {
  font-family: var(--font-sans);
  font-size: 10.5px;
  font-weight: 600;
  fill: var(--ink);
}
.mst {
  font-family: var(--font-mono);
  font-size: 8.5px;
  fill: var(--muted);
}
</style>
