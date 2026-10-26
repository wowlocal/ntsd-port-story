<script setup lang="ts">
// Chapter 3: 9 September (git local time, +0300) — every commit of the day on lanes by part of the game tick,
// then the night of 10 September up to 04:30, when lib.dll is found (01:28) and the first library hooks
// are redone. Dot size — lines added under native/Sources. Click 1 rings the five of thirteen lib.dll patch
// sites that ACTIVE_LIB_IMPACT (5a28b0a) found in the pristine active controls, at the commit that ported
// that stage. Print mode shows the rings. Hover a dot for the commit.
// Data: git log fc959db, 9–10 September; native/Sources insertions from git show --numstat.
import { computed, ref } from 'vue'
import { useNav, useSlideContext } from '@slidev/client'

interface C { h: string, t: string, d?: 10, n: number, s: string, lane: number, patch?: string, pos?: 'al' | 'bl', lib?: boolean }
const lanes = [
  'вход в матч, управление',
  'физика, контакты, удары',
  'камера, фон, отрисовка',
  'точность x87',
  'планировщик, post-draw',
  'HUD и уведомления',
  'запись повтора',
  'результат и тело такта',
  'пауза и таймеры',
  'документы и оценки',
]
const commits: C[] = [
  { h: 'eb26182', t: '00:45', n: 469, s: 'reproduce original match settings and start selection', lane: 0 },
  { h: 'fa89845', t: '01:32', n: 296, s: 'join original match launch with first gameplay entry', lane: 0 },
  { h: '6f2ff66', t: '01:59', n: 162, s: 'reproduce generic actor input and DAT frame transfers', lane: 0 },
  { h: '50fcbde', t: '02:26', n: 286, s: 'reproduce complete original actor control', lane: 0, patch: '41408b · управление' },
  { h: 'e2f20ce', t: '02:53', n: 170, s: 'join original world control with native match state', lane: 0 },
  { h: '71b74a2', t: '03:44', n: 447, s: 'port complete actor and world physics from original game', lane: 1 },
  { h: '08cbc6a', t: '04:08', n: 184, s: 'port original depth and held-object world passes', lane: 1 },
  { h: '4030489', t: '04:48', n: 324, s: 'port original contact collection and fusion passes', lane: 1, patch: '4176ac · контакты', pos: 'bl' },
  { h: '0ef2a81', t: '05:51', n: 747, s: 'port original hit resolution and item passes', lane: 1 },
  { h: '445d723', t: '06:24', n: 265, s: 'port original cpoint actions and attachment passes', lane: 1 },
  { h: '30be76e', t: '07:11', n: 299, s: 'port original camera and background drawing', lane: 2 },
  { h: 'ec0d536', t: '07:29', n: 0, s: 'docs: document progress estimator in agent instructions', lane: 9 },
  { h: 'd47d414', t: '08:00', n: 0, s: 'tools: update progress estimates with overnight gameplay work', lane: 9 },
  { h: 'e3c220f', t: '08:15', n: 375, s: 'port original World and Actor drawing', lane: 2 },
  { h: 'a2a853c', t: '08:49', n: 156, s: 'port post-draw impulses and audit FPU precision', lane: 4, patch: '401290 · текст', pos: 'al' },
  { h: '2cf272c', t: '09:13', n: 118, s: 'fix: model original x87 arithmetic precision', lane: 3 },
  { h: '1fcc04b', t: '09:45', n: 73, s: 'test: validate initialized gameplay at original FPU precision', lane: 3 },
  { h: '92aed35', t: '10:08', n: 23, s: 'fix: preserve original arithmetic in actor control', lane: 3 },
  { h: 'adf93da', t: '10:25', n: 0, s: 'test: verify original coordinate conversion and camera precision', lane: 3 },
  { h: '2be325d', t: '10:44', n: 3, s: 'test: verify original DAT scanning at startup precision', lane: 3 },
  { h: 'fcf9cd1', t: '11:04', n: 173, s: 'port the original Actor frame scheduler', lane: 4 },
  { h: '246e7cf', t: '11:30', n: 179, s: 'port post-draw transformations, particles and recovery', lane: 4 },
  { h: 'ecd4b2e', t: '11:48', n: 196, s: 'port generic post-draw opoint and frame lifetime', lane: 4 },
  { h: '279c606', t: '12:17', n: 262, s: 'port complete live-slot post-draw lifecycle', lane: 4, patch: '41f5fc · цикл слотов', pos: 'bl' },
  { h: '7c7c6bc', t: '12:49', n: 101, s: 'test: join initialized matches through post-draw lifecycle', lane: 4 },
  { h: '42b444a', t: '13:40', n: 226, s: 'port post-draw commands and join initialized matches', lane: 4, patch: '4214d7 · команды' },
  { h: '22175e3', t: '14:25', n: 220, s: 'port original HUD and join initialized gameplay', lane: 5 },
  { h: '9e705cd', t: '14:45', n: 223, s: 'reproduce original diagnostic number formatting', lane: 5 },
  { h: '46d93a8', t: '15:14', n: 131, s: 'port original post-HUD notices', lane: 5 },
  { h: '56e9c19', t: '15:43', n: 130, s: 'join initialized matches through post-HUD notices', lane: 5 },
  { h: 'c674066', t: '16:46', n: 5049, s: 'reproduce original replay compression (zlib 1.1.4, 815 вызовов оригинала)', lane: 6 },
  { h: '00aac27', t: '17:14', n: 88, s: 'reproduce original replay stream buffering', lane: 6 },
  { h: '248f7e5', t: '18:22', n: 221, s: 'reproduce whole original replay writer', lane: 6 },
  { h: '9cf01e5', t: '20:12', n: 374, s: 'wip: checkpoint result recording, font helpers, and research scope', lane: 7 },
  { h: '4678f1d', t: '21:04', n: 139, s: 'accept result recording and native tick output helpers', lane: 7 },
  { h: '37b2a14', t: '21:33', n: 168, s: 'reproduce original result layout and replay indicators', lane: 7 },
  { h: '9784426', t: '21:39', n: 33, s: 'compare gameplay output order and controlled original return', lane: 7 },
  { h: '872964f', t: '21:40', n: 0, s: 'docs: record controlled gameplay output acceptance', lane: 9 },
  { h: '582a2de', t: '21:52', n: 73, s: 'join both initialized result layout continuations', lane: 7 },
  { h: 'c558f56', t: '22:07', n: 0, s: 'docs: map loaded tick runtime composition and remaining lifetimes', lane: 9 },
  { h: '696e2a6', t: '22:16', n: 167, s: 'compare initialized gameplay output and both returns', lane: 7 },
  { h: 'f98c5ab', t: '22:35', n: 337, s: 'compose the native unpaused gameplay body atomically', lane: 7 },
  { h: 'c65f9a8', t: '23:07', n: 390, s: 'compare sixteen successive native gameplay calls', lane: 7 },
  { h: '5a0916a', t: '23:14', n: 26, s: 'preserve command flags in the paused HUD callee', lane: 8 },
  { h: 'f09d23e', t: '00:04', d: 10, n: 26, s: 'preserve original application timer decisions', lane: 8 },
  { h: '30ce08e', t: '00:23', d: 10, n: 547, s: 'continue own pause, single-step and resume', lane: 8 },
  { h: 'a11f571', t: '00:50', d: 10, n: 42, s: 'preserve original application service key scan', lane: 8 },
  { h: '4298b7e', t: '01:00', d: 10, n: 23, s: 'preserve full-surface clear and dispatcher prerequisites', lane: 8 },
  { h: '5feeb80', t: '01:33', d: 10, n: 242, s: 'test: verify 48 active-input pristine game calls', lane: 7, lib: true },
  { h: '5a28b0a', t: '01:39', d: 10, n: 0, s: 'docs: audit bundled library impact on active controls', lane: 9, lib: true },
  { h: 'fe20733', t: '01:59', d: 10, n: 119, s: 'connect bundled library preparation to stage commands', lane: 0, lib: true },
  { h: '0a7c7a6', t: '02:13', d: 10, n: 35, s: 'preserve bundled library Actor control', lane: 0, lib: true },
  { h: '834b36a', t: '02:37', d: 10, n: 56, s: 'preserve bundled library contact filters', lane: 1, lib: true },
  { h: 'db588b3', t: '04:08', d: 10, n: 123, s: 'Recover bundled library hit effects and movement order', lane: 1, lib: true },
]

const nav = useNav()
const { $clicks } = useSlideContext()
const showPatches = computed(() => nav.isPrintMode.value || ($clicks?.value ?? 0) >= 1)

const min = (c: { t: string, d?: number }) => {
  const [h, m] = c.t.split(':').map(Number)
  return (c.d === 10 ? 24 * 60 : 0) + h * 60 + m
}
const T0 = 0
const T1 = 28.5 * 60
const W = 884
const L = 150
const top = 18
const row = 17
const H = top + lanes.length * row + 26
const x = (m: number) => L + ((m - T0) / (T1 - T0)) * (W - L - 10)
const y = (lane: number) => top + lane * row + row / 2
const r = (n: number) => 2.6 + Math.min(5.4, Math.sqrt(n) / 5.2)
const ticks = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27]
const libAt = 25 * 60 + 28
const star = commits.find(c => c.h === 'c65f9a8')!

const sel = ref<C>(star)
const nf = new Intl.NumberFormat('ru-RU')
const detail = computed(() => {
  const c = sel.value
  const when = `${c.d === 10 ? '10' : '9'} сен ${c.t}`
  const lines = c.n ? ` · +${nf.format(c.n)} строк в native/Sources` : ''
  const patch = c.patch ? ` · здесь заплатка lib.dll ${c.patch}` : ''
  const lib = c.lib ? ' · уже после lib.dll' : ''
  return `${when} · ${c.h} · ${c.s}${lines}${patch}${lib}`
})
</script>

<template>
  <div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="9 сентября по часам: коммиты по частям игрового такта и находка lib.dll в 01:28 10 сентября">
      <rect :x="x(24 * 60)" :y="top - 6" :width="x(T1) - x(24 * 60)" :height="lanes.length * row + 6" class="night" />
      <g v-for="h in ticks" :key="h">
        <line :x1="x(h * 60)" :x2="x(h * 60)" :y1="top - 6" :y2="top + lanes.length * row" class="gl" />
        <text class="ax" :x="x(h * 60)" :y="H - 10" text-anchor="middle">{{ String(h % 24).padStart(2, '0') }}:00</text>
      </g>
      <text class="axd" :x="x(0)" :y="H - 0.5">9 сентября</text>
      <text class="axd" :x="x(24 * 60) + 3" :y="H - 0.5">10 сентября</text>

      <g v-for="(name, i) in lanes" :key="name">
        <line :x1="L" :x2="W - 10" :y1="y(i)" :y2="y(i)" class="lane" />
        <text class="ln" :class="{ dim: i === 9 }" x="0" :y="y(i) + 3.5">{{ name }}</text>
      </g>

      <!-- lib.dll found -->
      <line :x1="x(libAt)" :x2="x(libAt)" :y1="4" :y2="top + lanes.length * row" class="lib" />
      <text class="libt" :x="x(libAt) - 5" y="10" text-anchor="end">01:28 · 9bb48f6 · lib.dll</text>

      <!-- the 16-call comparison -->
      <text class="st" :x="x(min(star)) - 9" :y="y(star.lane) + 15" text-anchor="end">23:07 · 16 вызовов подряд</text>

      <g v-for="c in commits" :key="c.h" class="hov" tabindex="0" @pointerenter="sel = c" @focus="sel = c">
        <circle :cx="x(min(c))" :cy="y(c.lane)" r="9" class="hit" />
        <circle
          :cx="x(min(c))" :cy="y(c.lane)" :r="r(c.n)"
          :class="[c.lib ? 'dl' : c.lane === 9 ? 'dd' : 'dc', { on: sel === c, star: c === star }]"
        />
      </g>

      <!-- patch rings -->
      <g v-for="c in commits.filter(k => k.patch)" :key="`p${c.h}`" class="pr" :class="{ shown: showPatches }">
        <circle :cx="x(min(c))" :cy="y(c.lane)" :r="r(c.n) + 4.5" class="ring" />
        <text class="pt" :x="c.pos ? x(min(c)) - r(c.n) - 7 : x(min(c)) + r(c.n) + 7" :y="c.pos === 'bl' ? y(c.lane) + 19 : y(c.lane) - 6" :text-anchor="c.pos ? 'end' : 'start'">{{ c.patch }}</text>
      </g>
    </svg>
    <div class="leg">
      <span><i class="k dc" />коммит 9 сентября · размер — строки в <code>native/Sources</code></span>
      <span><i class="k dl" />после lib.dll</span>
      <span class="pk" :class="{ shown: showPatches }"><i class="k ring" />заплатка lib.dll в стадии этого коммита — 5 из 13</span>
    </div>
    <div class="det" aria-live="polite">{{ detail }}</div>
  </div>
</template>

<style scoped>
.night { fill: rgba(57, 135, 229, 0.06); }
.gl { stroke: var(--grid); stroke-width: 1; }
.lane { stroke: rgba(255, 255, 255, 0.05); stroke-width: 1; }
.ax { font-size: 10px; fill: var(--muted); font-family: var(--font-sans); font-variant-numeric: tabular-nums; }
.axd { font-size: 9.5px; fill: var(--ink-2); font-family: var(--font-sans); }
.ln { font-size: 10.5px; fill: var(--ink); font-family: var(--font-sans); }
.ln.dim { fill: var(--muted); }
.lib { stroke: var(--s8); stroke-width: 1.6; stroke-dasharray: 4 3; }
.libt { font-size: 10.5px; fill: var(--s8); font-family: var(--font-sans); font-weight: 700; }
.st { font-size: 10.5px; fill: var(--ink); font-family: var(--font-sans); font-weight: 700; }
.hov { cursor: pointer; outline: none; }
.hit { fill: transparent; }
.dc { fill: var(--s1); stroke: var(--bg); stroke-width: 1.5; }
.dd { fill: var(--muted); stroke: var(--bg); stroke-width: 1.5; }
.dl { fill: var(--s8); stroke: var(--bg); stroke-width: 1.5; }
.star { fill: var(--naruto); }
.on { stroke: var(--ink); stroke-width: 1.8; }
.pr { opacity: 0; transition: opacity 0.4s ease; }
.pr.shown { opacity: 1; }
.ring { fill: none; stroke: var(--s8); stroke-width: 1.6; }
.pt { font-size: 9.5px; fill: var(--s8); font-family: var(--font-mono); }
.leg { display: flex; flex-wrap: wrap; gap: 0.25rem 1.1rem; font-size: 0.6rem; color: var(--ink-2); margin-top: 0.1rem; }
.leg span { display: inline-flex; align-items: center; gap: 0.35rem; }
.leg code { font-size: 0.56rem !important; }
.leg .pk { opacity: 0; transition: opacity 0.4s ease; }
.leg .pk.shown { opacity: 1; }
.k { display: inline-block; width: 9px; height: 9px; border-radius: 50%; }
.k.dc { background: var(--s1); }
.k.dl { background: var(--s8); }
.k.ring { border: 1.6px solid var(--s8); width: 11px; height: 11px; }
.det { font-size: 0.62rem; color: var(--ink-2); line-height: 1.35; min-height: 1.7em; font-family: var(--font-sans); margin-top: 0.15rem; }
</style>
