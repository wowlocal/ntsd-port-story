<script setup lang="ts">
// Demo-day deck: the phone loop in one picture. Left, the cycle every turn goes through and its two exits;
// right, the main thread's work per tick on the Galaxy A12 after each turn (vs scenario, mean of 2–4 runs),
// from the loop's start (8840eb3, 7 Oct 08:23, 24.55 ms) to its last row (e5, 10 Oct 17:31, 11.09 ms).
// Data: data/rt2_steps.json (scripts/collect_realtime2.py) — one point per registry row with a vs measurement.
import { computed } from 'vue'
import rt from '../data/rt2_steps.json'

const d = rt as any
const t0 = Date.parse('2026-10-07T08:00:00')
const t1 = Date.parse('2026-10-10T19:00:00')
const toT = (s: string) => Date.parse(`2026-${s.replace(' ', 'T')}:00`)

interface P { t: number, ms: number, kind: 'kept' | 'out' | 'other', id: string }
const pts = computed<P[]>(() => {
  const out: P[] = [{ t: toT(d.start.time), ms: d.start.vs.main, kind: 'kept', id: d.start.id }]
  for (const s of d.steps) {
    const a = s.vs?.after
    if (!a?.main)
      continue
    const kind = s.verdict === 'reverted' || s.verdict === 'parked' ? 'out' : (s.verdict === 'kept' || s.verdict === 'less') ? 'kept' : 'other'
    out.push({ t: toT(s.time), ms: a.main, kind, id: s.id })
  }
  return out
})

const W = 560
const H = 250
const L = 40
const R = 14
const T = 18
const B = 30
const x = (t: number) => L + ((t - t0) / (t1 - t0)) * (W - L - R)
const y = (ms: number) => T + ((26 - ms) / (26 - 9)) * (H - T - B)
const line = computed(() => pts.value.filter(p => p.kind !== 'out').map((p, i) => `${i ? 'L' : 'M'}${x(p.t).toFixed(1)},${y(p.ms).toFixed(1)}`).join(' '))
const days = [7, 8, 9, 10].map(n => ({ n, t: Date.parse(`2026-10-${String(n).padStart(2, '0')}T00:00:00`) })).filter(dd => dd.t >= t0)
const sixty = 16.67
</script>

<template>
  <div class="dl">
    <div class="cyc">
      <svg viewBox="0 0 300 300" role="img" aria-label="Цикл: замер на телефоне, одна правка, проверки, решение — коммит или откат">
        <defs>
          <marker id="dl-ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="var(--naruto)" />
          </marker>
        </defs>
        <circle cx="150" cy="150" r="98" fill="none" stroke="var(--axis)" stroke-width="2" stroke-dasharray="4 5" />
        <path d="M 206 70 A 98 98 0 0 1 238 120" fill="none" stroke="var(--naruto)" stroke-width="2.5" marker-end="url(#dl-ar)" />
        <path d="M 232 196 A 98 98 0 0 1 194 236" fill="none" stroke="var(--naruto)" stroke-width="2.5" marker-end="url(#dl-ar)" />
        <path d="M 106 236 A 98 98 0 0 1 68 196" fill="none" stroke="var(--naruto)" stroke-width="2.5" marker-end="url(#dl-ar)" />
        <path d="M 62 120 A 98 98 0 0 1 94 70" fill="none" stroke="var(--naruto)" stroke-width="2.5" marker-end="url(#dl-ar)" />
        <g class="nd">
          <rect x="95" y="28" width="110" height="44" rx="10" />
          <text x="150" y="47">1 · замер</text>
          <text x="150" y="63" class="s">на телефоне</text>
          <rect x="200" y="128" width="96" height="44" rx="10" />
          <text x="248" y="147">2 · правка</text>
          <text x="248" y="163" class="s">одна за оборот</text>
          <rect x="95" y="228" width="110" height="44" rx="10" />
          <text x="150" y="247">3 · проверки</text>
          <text x="150" y="263" class="s">кадры = эталону</text>
          <rect x="4" y="128" width="96" height="44" rx="10" class="dec" />
          <text x="52" y="147">4 · решение</text>
          <text x="52" y="163" class="s">коммит / откат</text>
        </g>
        <text x="150" y="146" class="mid">75</text>
        <text x="150" y="168" class="mids">оборотов</text>
      </svg>
    </div>
    <div class="ch">
      <div class="ch-h">работа главного потока на один тик, мс · Galaxy A12</div>
      <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Время главного потока на тик: с 24,6 до 11,1 миллисекунды за 75 оборотов">
        <g class="gl">
          <line v-for="v in [10, 15, 20, 25]" :key="v" :x1="L" :x2="W - R" :y1="y(v)" :y2="y(v)" />
          <text v-for="v in [10, 15, 20, 25]" :key="`t${v}`" :x="L - 7" :y="y(v) + 4" text-anchor="end">{{ v }}</text>
        </g>
        <g class="xa">
          <text v-for="dd in days" :key="dd.n" :x="x(dd.t)" :y="H - 8" text-anchor="middle">{{ dd.n }} окт</text>
        </g>
        <line class="sixty" :x1="L" :x2="W - R" :y1="y(sixty)" :y2="y(sixty)" />
        <text class="sixty-t" :x="W - R - 4" :y="y(sixty) - 7" text-anchor="end">16,7 мс = 60 кадров в секунду</text>
        <path :d="line" class="ln" />
        <g v-for="p in pts" :key="p.id">
          <circle v-if="p.kind === 'out'" :cx="x(p.t)" :cy="y(p.ms)" r="4" class="out" />
          <circle v-else :cx="x(p.t)" :cy="y(p.ms)" r="2.6" class="kept" />
        </g>
        <g class="ann">
          <text :x="x(pts[0].t) + 8" :y="y(pts[0].ms) - 8">24,6 мс</text>
          <text :x="x(pts[pts.length - 1].t) - 4" :y="y(pts[pts.length - 1].ms) + 20" text-anchor="end" class="end">11,1 мс</text>
        </g>
      </svg>
      <div class="lg"><span><i class="k" />шаг принят</span><span><i class="o" />откат или отложен — замер был, коммита нет</span></div>
    </div>
  </div>
</template>

<style scoped>
.dl { display: grid; grid-template-columns: 0.62fr 1.38fr; gap: 1.6rem; align-items: center; }
.cyc svg { width: 100%; display: block; }
.nd rect { fill: var(--surface); stroke: var(--hair); stroke-width: 1.5; }
.nd rect.dec { stroke: var(--naruto); }
.nd text { font-family: var(--font-sans); font-size: 13px; font-weight: 700; fill: var(--ink); text-anchor: middle; }
.nd text.s { font-size: 10.5px; font-weight: 400; fill: var(--ink-2); }
.mid { font-family: var(--font-display); font-weight: 700; font-size: 38px; fill: var(--naruto); text-anchor: middle; }
.mids { font-family: var(--font-sans); font-size: 12px; fill: var(--ink-2); text-anchor: middle; }
.exits { display: flex; flex-direction: column; gap: .3rem; margin-top: .3rem; font-size: .72rem; }
.exits span { padding: .2rem .6rem; border-radius: 8px; border-left: 4px solid; background: rgba(255, 255, 255, .03); color: var(--ink); }
.exits .ok { border-color: var(--good); }
.exits .no { border-color: var(--critical); }
.ch-h { font-size: .72rem; color: var(--ink-2); margin-bottom: .2rem; }
.gl line { stroke: var(--grid); }
.gl text, .xa text { font-family: var(--font-mono); font-size: 11px; fill: var(--muted); }
.sixty { stroke: var(--good); stroke-width: 1.5; stroke-dasharray: 6 4; }
.sixty-t { font-family: var(--font-sans); font-size: 12px; fill: var(--good); }
.ln { fill: none; stroke: var(--s2); stroke-width: 2.2; stroke-linejoin: round; }
.kept { fill: var(--s2); }
.out { fill: var(--bg); stroke: var(--critical); stroke-width: 1.8; }
.ann text { font-family: var(--font-display); font-weight: 700; font-size: 17px; fill: var(--ink); }
.ann text.end { fill: var(--naruto); }
.lg { display: flex; gap: 1.1rem; font-size: .64rem; color: var(--ink-2); margin-top: .2rem; }
.lg i { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: .35rem; vertical-align: -1px; }
.lg i.k { background: var(--s2); }
.lg i.o { border: 1.8px solid var(--critical); }
</style>
