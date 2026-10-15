<script setup lang="ts">
import { computed, ref } from 'vue'
import { useNav, useSlideContext } from '@slidev/client'
import data from '../data/web_hosts.json'

// The four new hosts against the same frozen references: 10 app_e2e scenarios and every frame.
// `stepwise`: click 0 is the state before W4 (the browser drew no GDI text: the text-free `none` group),
// click 1 adds W4 (f0471f13): text in exactly the same 9,565 frames as CoreText. Export shows click 1.
// Hover a cell: that scenario's run. Data: data/web_hosts.json (scripts/collect_web.py).
const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const after = computed(() => !props.stepwise || nav.isPrintMode.value || ($clicks?.value ?? 0) >= 1)

const d = data as any
const scen = d.scenarios as string[]
const head: Record<string, [string, string]> = {
  'vs': ['', 'VS'], 'mission': ['', 'Mission'], 'demo': ['', 'Demo'], 'war': ['', 'War'], 'playback': ['', 'запись'],
  'tournament': ['', 'Tourn.'], 'altenter': ['Alt+', 'Enter'], 'tournament-win': ['до', 'победы'], 'team-tournament': ['Team', 'Tourn.'], 'joystick': ['', 'геймпад'],
}
const hosts = d.hosts as any[]
const scenName: Record<string, string> = {
  'vs': 'VS', 'mission': 'Mission', 'demo': 'Demo', 'war': 'War', 'playback': 'запись', 'tournament': 'Tournament',
  'altenter': 'Alt+Enter', 'tournament-win': 'турнир до победы', 'team-tournament': 'Team Tournament', 'joystick': 'геймпад',
}
const nf = (n: number) => n.toLocaleString('ru-RU')

const W = 884
const xEnv = 92
const xGrid = 262
const CW = 39
const xFr = xGrid + scen.length * CW + 12
const frW = 70
const xGr = xFr + frW + 8
const RH = 26
const y0 = 64
const H = y0 + hosts.length * RH + 12
const cx = (i: number) => xGrid + i * CW + CW / 2
const ry = (i: number) => y0 + i * RH
const group = (h: any) => {
  if (h.key === 'tvos')
    return ['как AppKit', 'текст CoreText']
  if (h.key === 'wasi')
    return ['как Mac headless', 'без текста']
  return after.value ? ['свой текст движка', 'без текста — как headless'] : ['как Mac headless', 'текст не рисуется']
}
const envShort: Record<string, string> = { tvos: 'симулятор tvOS 27, Apple TV 4K', wasi: 'Node 26.7 — тестовый стенд', chromium: 'headless Chromium 153', webkit: 'Playwright, движок Safari' }

// the text split (W4), over the 18,030 frame digests compare_text_frames.py reads
const T = d.text
const bx = 0
const bwid = W
const tx = (n: number) => bx + (n / T.frames) * bwid

const tip = ref<{ x: number, y: number, title: string, lines: string[] } | null>(null)
function cellTip(h: any, s: string, i: number, r: number) {
  const det = h.detail[s]
  const lines: string[] = []
  if (h.key === 'tvos')
    lines.push(`${nf(det.digests)} дайджестов кадров и ${det.frames} PNG — как у AppKit`)
  else if (h.key === 'wasi')
    lines.push(`прогон ${det.seconds.toString().replace('.', ',')} с; кадры — как у Mac headless`)
  else
    lines.push(`страница нарисовала ${nf(det.draws)} из ${nf(det.presents)} кадров`, `прогон ${det.seconds.toString().replace('.', ',')} с`)
  tip.value = { x: cx(i), y: ry(r), title: `${h.name} · ${scenName[s]}: равно эталону`, lines }
}
function rowTip(h: any, r: number) {
  tip.value = { x: xEnv + 60, y: ry(r), title: `${h.name} — ${h.env}`, lines: [h.note, `сравнение: ${h.against} · ${h.commit}`] }
}
</script>

<template>
  <div class="hs">
    <div class="prev">
      <span class="pixel">глава 13</span> девять хостов — Mac, macOS SDL, iPad, Linux ×3, Windows ×2, Android: <b>90 из 90</b> сценариев равны тем же эталонам
    </div>
    <div class="wrap" @pointerleave="tip = null">
      <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Четыре новых хоста: десять сценариев и кадры">
        <text class="hd" x="0" :y="y0 - 12">новый хост</text>
        <text class="hd" :x="xEnv" :y="y0 - 12">где проверено</text>
        <g v-for="(s, i) in scen" :key="s">
          <text v-if="head[s][0]" class="hd sc" :x="cx(i)" :y="y0 - 25" text-anchor="middle">{{ head[s][0] }}</text>
          <text class="hd sc" :x="cx(i)" :y="y0 - 12" text-anchor="middle">{{ head[s][1] }}</text>
        </g>
        <text class="hd" :x="xFr" :y="y0 - 25">кадров</text>
        <text class="hd" :x="xFr" :y="y0 - 12">равны</text>
        <text class="hd" :x="xGr" :y="y0 - 12">эталон и текст</text>
        <line x1="0" :x2="W" :y1="y0 - 5" :y2="y0 - 5" stroke="var(--axis)" />

        <g v-for="(h, r) in hosts" :key="h.key">
          <line x1="0" :x2="W" :y1="ry(r) + RH" :y2="ry(r) + RH" stroke="var(--grid)" />
          <g class="hit" tabindex="0" @pointerenter="rowTip(h, r)" @focus="rowTip(h, r)" @blur="tip = null">
            <rect x="0" :y="ry(r)" :width="xGrid - 8" :height="RH" fill="transparent" />
            <text class="nm" x="0" :y="ry(r) + 17">{{ h.name }}</text>
            <text class="env" :x="xEnv" :y="ry(r) + 17">{{ envShort[h.key] }}</text>
          </g>
          <g v-for="(s, i) in scen" :key="s" class="hit" tabindex="0" @pointerenter="cellTip(h, s, i, r)" @focus="cellTip(h, s, i, r)" @blur="tip = null">
            <rect :x="cx(i) - CW / 2" :y="ry(r)" :width="CW" :height="RH" fill="transparent" />
            <rect :x="cx(i) - 7" :y="ry(r) + 6" width="14" height="14" rx="3.5" fill="var(--good)" />
            <path :d="`M${cx(i) - 3.6},${ry(r) + 13.3} l2.6,2.6 l4.8,-5.2`" fill="none" stroke="#0a0d13" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" />
          </g>
          <text class="fin" :x="xFr" :y="ry(r) + 17.5">{{ nf(h.frames) }}</text>
          <text class="g1" :x="xGr" :y="ry(r) + 12">{{ group(h)[0] }}</text>
          <text class="g2" :x="xGr" :y="ry(r) + 23">{{ group(h)[1] }}</text>
        </g>
      </svg>
      <div v-if="tip" class="tip" :style="{ left: `${(tip.x / W) * 100}%`, top: `${(tip.y / H) * 100}%`, transform: `translate(${tip.x > W * 0.6 ? '-100%' : '-30%'}, -105%)` }">
        <div class="tt">
          {{ tip.title }}
        </div>
        <div v-for="l in tip.lines" :key="l" class="tl">
          {{ l }}
        </div>
      </div>
    </div>

    <div class="txt" :class="{ off: !after }">
      <div class="th">
        <span class="pixel hl">W4 · 13 окт, 06:21</span> текст игры — шрифтом браузера: сравнение по {{ nf(T.frames) }} дайджестам кадров, Chromium и WebKit отдельно
      </div>
      <svg :viewBox="`0 0 ${W} 40`" width="100%" role="img" :aria-label="`${nf(T.textless)} кадров без текста равны, в ${nf(T.text)} текст стоит в тех же кадрах`">
        <defs>
          <pattern id="whsHatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <rect width="7" height="7" fill="#24466f" />
            <line x1="0" y1="0" x2="0" y2="7" stroke="#2f5b91" stroke-width="2" />
          </pattern>
        </defs>
        <rect :x="tx(0)" y="2" :width="tx(T.textless) - 2" height="20" rx="3" fill="var(--s1)" />
        <rect :x="tx(T.textless)" y="2" :width="tx(T.frames) - tx(T.textless)" height="20" rx="3" fill="url(#whsHatch)" />
        <text class="in" :x="tx(0) + 8" y="16.5">{{ nf(T.textless) }} без текста — побайтно как эталон</text>
        <text class="in" :x="tx(T.textless) + 8" y="16.5">{{ nf(T.text) }} с текстом — буквы в тех же кадрах, что у CoreText</text>
        <text class="sub" x="0" y="36">расхождений по кадрам с текстом: {{ T.disagree }} · пиксели букв у движков свои: Chromium и WebKit различаются в {{ T.enginesDiffer }} кадрах — у каждого своя группа</text>
      </svg>
    </div>
  </div>
</template>

<style scoped>
.hs {
  position: relative;
}
.prev {
  font-size: 0.66rem;
  color: var(--muted);
  margin-bottom: 0.1rem;
}
.prev .pixel {
  color: var(--ink-2);
  margin-right: 0.4rem;
}
.prev b {
  color: var(--ink-2);
}
.wrap {
  position: relative;
}
.hd {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
}
.nm {
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 650;
  fill: var(--ink);
}
.env {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--ink-2);
}
.fin {
  font-family: var(--font-sans);
  font-size: 12.5px;
  font-weight: 700;
  fill: var(--ink);
  font-variant-numeric: tabular-nums;
}
.fof {
  font-size: 10.5px;
  font-weight: 400;
  fill: var(--ink-2);
}
.g1 {
  font-family: var(--font-sans);
  font-size: 10.5px;
  font-weight: 600;
  fill: var(--ink);
}
.g2 {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--ink-2);
}
.hit {
  cursor: pointer;
  outline: none;
}
.tip {
  position: absolute;
  pointer-events: none;
  background: #0c1017;
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 8px;
  padding: 0.3rem 0.55rem;
  max-width: 330px;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.5);
  z-index: 5;
}
.tt {
  font-size: 0.68rem;
  font-weight: 650;
  color: var(--ink);
}
.tl {
  font-size: 0.64rem;
  color: var(--ink-2);
  line-height: 1.3;
}
.txt {
  margin-top: 0.5rem;
  transition: opacity 0.4s ease;
}
.txt.off {
  opacity: 0;
}
.th {
  font-size: 0.7rem;
  color: var(--ink-2);
  margin-bottom: 0.25rem;
}
.th .pixel {
  margin-right: 0.4rem;
}
.in {
  font-family: var(--font-sans);
  font-size: 11px;
  font-weight: 650;
  fill: #fff;
}
.sub {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--ink-2);
}
</style>
