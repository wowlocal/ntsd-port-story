<script setup lang="ts">
import { computed } from 'vue'
import { useNav, useSlideContext } from '@slidev/client'
import data from '../data/xplat.json'

// 9 hosts x 10 app_e2e scenarios against the frozen AppKit references, grouped by text rasteriser.
// `stepwise`: click 0 shows the baseline run of 4 Oct 23:20 (b9d4b62, recorded in 2fe64be), click 1 the run of 22:39 (870c24a, committed in 7f15b7b).
// Export and print show the final state.
const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const after = computed(() => !props.stepwise || nav.isPrintMode.value || ($clicks?.value ?? 0) >= 1)

const m = (data as any).matrix
const state = computed(() => (after.value ? m.after : m.before))
const scen = m.scenarios as string[]
const scenName: Record<string, string> = {
  'vs': 'VS', 'mission': 'Mission', 'demo': 'Demo', 'war': 'War', 'playback': 'запись',
  'tournament': 'Tourn.', 'altenter': 'Alt+Enter', 'tournament-win': 'турнир до победы', 'team-tournament': 'Team Tourn.', 'joystick': 'геймпад',
}
// two-line column heads
const head2: Record<string, [string, string]> = {
  'vs': ['', 'VS'], 'mission': ['', 'Mission'], 'demo': ['', 'Demo'], 'war': ['', 'War'], 'playback': ['', 'запись'],
  'tournament': ['', 'Tourn.'], 'altenter': ['Alt+', 'Enter'], 'tournament-win': ['до', 'победы'], 'team-tournament': ['Team', 'Tourn.'], 'joystick': ['', 'геймпад'],
}
interface Row { key: string, name: string, env: string, hw?: string, hwNote?: string }
const groups: { key: string, name: string, rows: Row[] }[] = [
  { key: 'coretext', name: 'текст CoreText', rows: [
    { key: 'appkit', name: 'macOS · AppKit', env: 'этот Mac · эталон', hw: 'yes', hwNote: 'выпущенное приложение' },
    { key: 'macos-sdl', name: 'macOS · SDL3', env: 'этот Mac' },
    { key: 'ios', name: 'iPad', env: 'симулятор', hw: 'report', hwNote: 'iPad Pro: отчёт человека, без замеров' },
  ] },
  { key: 'freetype', name: 'FreeType', rows: [
    { key: 'linux-sdl', name: 'Linux · SDL3', env: 'контейнер' },
  ] },
  { key: 'gdi', name: 'GDI', rows: [
    { key: 'windows-sdl', name: 'Windows · SDL3', env: 'CrossOver' },
  ] },
  { key: 'none', name: 'без текста', rows: [
    { key: 'linux-headless', name: 'Linux arm64', env: 'контейнер' },
    { key: 'linux-x86_64', name: 'Linux x86_64', env: 'контейнер · Rosetta' },
    { key: 'windows', name: 'Windows', env: 'CrossOver' },
    { key: 'android', name: 'Android', env: 'эмулятор', hw: 'yes', hwNote: 'Galaxy A12: сценарий VS, 5 октября' },
  ] },
]

const W = 884
const xName = 0
const xEnv = 116
const xHw = 236 // the "real device" mark, between the place of the check and the grid
const xGrid = 256
const CW = 41
const xBr = xGrid + scen.length * CW + 12
const RH = 23
const GAP = 9
const y0 = 50
const layout = computed(() => {
  let y = y0
  return groups.map((g) => {
    const rows = g.rows.map((r) => {
      const row = { ...r, y }
      y += RH
      return row
    })
    const out = { ...g, rows, top: rows[0].y, bot: y }
    y += GAP
    return out
  })
})
const H = computed(() => layout.value[layout.value.length - 1].bot + 30)
const cx = (i: number) => xGrid + i * CW + CW / 2
const cell = (host: string, s: string) => state.value.cells[host]?.[s] ?? 'differs'
const total = computed(() => Object.values(state.value.cells as Record<string, Record<string, string>>).reduce((a, r) => a + Object.values(r).filter(v => v === 'equal').length, 0))
const frames = computed(() => state.value.frames)
const pairFrames = computed(() => frames.value['appkit==macos-sdl'].frames)
const textFrames = computed(() => frames.value['text:appkit~linux-sdl'].text)
const fmt = (n: number) => n.toLocaleString('ru-RU')
const pi = scen.indexOf('playback')
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Матрица: девять хостов, десять сценариев">
    <!-- header -->
    <text class="hd" :x="xName" :y="y0 - 12">хост</text>
    <text class="hd" :x="xEnv" :y="y0 - 12">где проверено</text>
    <g v-for="(s, i) in scen" :key="s">
      <text v-if="head2[s][0]" class="hd sc" :class="{ pb: s === 'playback' }" :x="cx(i)" :y="y0 - 23" text-anchor="middle">{{ head2[s][0] }}</text>
      <text class="hd sc" :class="{ pb: s === 'playback' }" :x="cx(i)" :y="y0 - 12" text-anchor="middle">{{ head2[s][1] }}</text>
    </g>
    <text class="hd" :x="xBr + 12" :y="y0 - 12">группа растеризатора · кадры</text>
    <line :x1="0" :x2="W" :y1="y0 - 5" :y2="y0 - 5" stroke="var(--axis)" />

    <!-- the playback column -->
    <rect :x="xGrid + pi * CW + 2" :y="y0 - 4" :width="CW - 4" :height="layout[layout.length - 1].bot - y0 + 4" rx="5"
          :fill="after ? 'rgba(12,163,12,0.07)' : 'rgba(208,59,59,0.08)'" />

    <g v-for="g in layout" :key="g.key">
      <g v-for="r in g.rows" :key="r.key">
        <line :x1="0" :x2="xBr - 6" :y1="r.y + RH" :y2="r.y + RH" stroke="var(--grid)" />
        <text class="nm" :x="xName" :y="r.y + 15.5">{{ r.name }}</text>
        <text class="env" :x="xEnv" :y="r.y + 15.5">{{ r.env }}</text>
        <g v-for="(s, i) in scen" :key="s">
          <template v-if="cell(r.key, s) === 'equal'">
            <rect :x="cx(i) - 7" :y="r.y + 4.5" width="14" height="14" rx="3.5" fill="var(--good)" />
            <path :d="`M${cx(i) - 3.6},${r.y + 11.8} l2.6,2.6 l4.8,-5.2`" fill="none" stroke="#0a0d13" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" />
          </template>
          <template v-else>
            <rect :x="cx(i) - 6.5" :y="r.y + 5" width="13" height="13" rx="3.5" fill="none" stroke="var(--critical)" stroke-width="1.6" />
            <text class="ne" :x="cx(i)" :y="r.y + 15.4" text-anchor="middle">≠</text>
          </template>
          <title>{{ r.name }} · {{ scenName[s] }}: {{ cell(r.key, s) === 'equal' ? 'равно эталону' : 'отличается от эталона' }}</title>
        </g>
        <g v-if="r.hw">
          <circle v-if="r.hw === 'yes'" :cx="xHw" :cy="r.y + 11.5" r="4.5" fill="var(--chakra)"><title>{{ r.hwNote }}</title></circle>
          <circle v-else :cx="xHw" :cy="r.y + 11.5" r="4" fill="none" stroke="var(--chakra)" stroke-width="1.5" stroke-dasharray="2 1.6"><title>{{ r.hwNote }}</title></circle>
        </g>
      </g>
      <!-- group bracket -->
      <path :d="`M${xBr},${g.top + 3} h5 V${g.bot - 3} h-5`" fill="none" stroke="var(--axis)" />
      <text class="gname" :x="xBr + 12" :y="g.top + 15">{{ g.name }}</text>
      <text v-if="g.key === 'coretext' || g.key === 'none'" class="gsub" :x="xBr + 12" :y="g.top + 30">кадры побайтно равны,</text>
      <text v-if="g.key === 'coretext' || g.key === 'none'" class="gsub" :x="xBr + 12" :y="g.top + 43"><tspan class="b">{{ fmt(pairFrames) }}</tspan> на пару хостов</text>
    </g>
    <!-- text agreement across the three text groups -->
    <path :d="`M${xBr + 74},${layout[1].top + 11} H${xBr + 84} V${layout[2].top + 11} H${xBr + 74}`" fill="none" stroke="var(--axis)" />
    <text class="gsub" :x="xBr + 90" :y="layout[1].top + 12">текст в тех же</text>
    <text class="gsub" :x="xBr + 90" :y="layout[1].top + 25"><tspan class="b">{{ fmt(textFrames) }}</tspan> кадрах,</text>
    <text class="gsub" :x="xBr + 90" :y="layout[1].top + 38">что у CoreText</text>

    <!-- footer -->
    <text class="foot" x="0" :y="H - 10">
      <tspan class="b">{{ total }} из 90</tspan> сценариев равны эталонам · {{ after ? '5 окт, 19:59 · 870c24a → 7f15b7b' : '4 окт, 23:20 · b9d4b62 → 2fe64be' }}
    </text>
    <g class="legend" :transform="`translate(${W - 404}, ${H - 14})`">
      <rect x="0" y="-9" width="11" height="11" rx="3" fill="var(--good)" /><text x="15" y="0">равно эталону</text>
      <rect x="98" y="-9" width="11" height="11" rx="3" fill="none" stroke="var(--critical)" stroke-width="1.5" /><text x="113" y="0">отличается</text>
      <circle cx="187" cy="-3.5" r="4.5" fill="var(--chakra)" /><text x="196" y="0">и на устройстве</text>
      <circle cx="292" cy="-3.5" r="4" fill="none" stroke="var(--chakra)" stroke-width="1.5" stroke-dasharray="2 1.6" /><text x="301" y="0">отчёт без замеров</text>
    </g>
  </svg>
</template>

<style scoped>
.hd {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
}
.hd.sc {
  font-size: 9.5px;
}
.hd.pb {
  fill: var(--ink);
  font-weight: 650;
}
.nm {
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 600;
  fill: var(--ink);
}
.env {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--ink-2);
}
.ne {
  font-family: var(--font-sans);
  font-size: 11px;
  font-weight: 700;
  fill: var(--critical);
}
.dash {
  font-size: 10px;
  fill: var(--axis);
}
.gname {
  font-family: var(--font-sans);
  font-size: 10.5px;
  font-weight: 650;
  fill: var(--ink);
}
.gsub {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--ink-2);
}
.b {
  font-weight: 700;
  fill: var(--ink);
}
.foot {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--ink-2);
}
.legend text {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--ink-2);
}
</style>
