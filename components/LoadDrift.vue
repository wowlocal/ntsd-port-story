<script setup lang="ts">
// Launch -> loaded on the Galaxy A12, every run a dot. Top row: two gates read from the ledger hours apart
// (S2 at 10:41, M5c at 12:30, which contains M5b): +1.2 s, a regression? Bottom row (click 1): S2 against M5b
// interleaved in one session at 15:30 after a warm-up run: the same. The phone slowed down, not the code.
// Runs that re-extracted the APK's assets after their install are left out (not comparable).
// Data: data/loading_method.json (drift.rows; scripts/collect_loading.py, from ml-menu-phase-check and ml-m5c).
import { computed } from 'vue'
import { useNav, useSlideContext } from '@slidev/client'
import data from '../data/loading_method.json'

const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const second = computed(() => !props.stepwise || nav.isPrintMode.value || ($clicks?.value ?? 0) >= 1)

const rows = (data as any).drift.rows as { view: string, when: string, gate: string, build: string, s: number }[]
const W = 430
const L = 118
const R = 16
const lo = 10.9
const hi = 13.1
const x = (v: number) => L + ((v - lo) / (hi - lo)) * (W - L - R)
const color = (b: string) => (b === 'S2' ? 'var(--s1)' : 'var(--s2)')
const top = rows.filter(r => r.view === 'ledger')
const bot = rows.filter(r => r.view === 'session')
const med = (rs: { s: number }[]) => {
  const v = rs.map(r => r.s).sort((a, b) => a - b)
  return v[Math.floor(v.length / 2)]
}
const f2 = (v: number) => v.toFixed(2).replace('.', ',')
const topS2 = med(top.filter(r => r.build === 'S2'))
const topM = med(top.filter(r => r.build !== 'S2'))
const botS2 = med(bot.filter(r => r.build === 'S2'))
const botM = med(bot.filter(r => r.build !== 'S2'))
const Y1 = 44
const Y2 = 118
</script>

<template>
  <svg :viewBox="`0 0 ${W} 178`" width="100%" role="img" aria-label="Запуск → загружено: по журналу гейтов и в одной сессии">
    <g v-for="t in [11, 11.5, 12, 12.5, 13]" :key="t">
      <line :x1="x(t)" :x2="x(t)" y1="20" y2="146" stroke="var(--grid)" />
      <text :x="x(t)" y="160" text-anchor="middle" class="tick">{{ String(t).replace('.', ',') }}{{ t === 13 ? ' с' : '' }}</text>
    </g>

    <text x="0" :y="Y1 - 2" class="k">по журналу</text>
    <text x="0" :y="Y1 + 10" class="kn">гейты 10:41 и 12:30</text>
    <circle v-for="(r, i) in top" :key="`t${i}`" :cx="x(r.s)" :cy="Y1" r="5" :fill="color(r.build)" stroke="var(--bg)" stroke-width="1.5" />
    <path :d="`M${x(topS2)},${Y1 - 12} V${Y1 - 16} H${x(topM)} V${Y1 - 12}`" fill="none" stroke="var(--ink-2)" />
    <text :x="(x(topS2) + x(topM)) / 2" :y="Y1 - 19" text-anchor="middle" class="d">+{{ f2(topM - topS2) }} с — регресс?</text>

    <g :style="{ opacity: second ? 1 : 0, transition: 'opacity .4s' }">
      <text x="0" :y="Y2 - 2" class="k">в одной сессии</text>
      <text x="0" :y="Y2 + 10" class="kn">15:30, прогрев, A B A B</text>
      <circle v-for="(r, i) in bot" :key="`b${i}`" :cx="x(r.s)" :cy="Y2 + (r.build === 'S2' ? -5 : 5)" r="5" :fill="color(r.build)" stroke="var(--bg)" stroke-width="1.5" />
      <text :x="x(Math.min(botS2, botM)) - 12" :y="Y2 + 4" text-anchor="end" class="d">разница {{ f2(Math.abs(botS2 - botM)) }} с — та же скорость</text>
    </g>

    <g>
      <circle :cx="L + 4" cy="174" r="4.5" fill="var(--s1)" /><text :x="L + 12" y="177.5" class="kn">S2</text>
      <circle :cx="L + 44" cy="174" r="4.5" fill="var(--s2)" /><text :x="L + 52" y="177.5" class="kn">M5b; в гейте M5c он уже внутри</text>
    </g>
  </svg>
</template>

<style scoped>
.tick {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
}
.k {
  font-size: 11.5px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.kn {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.d {
  font-size: 11px;
  font-weight: 600;
  fill: var(--ink);
  font-family: var(--font-sans);
}
</style>
