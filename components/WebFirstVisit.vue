<script setup lang="ts">
import { computed, ref } from 'vue'
import { useNav } from '@slidev/client'
import data from '../data/web_delivery.json'

// A first visit's seconds to the menu at any bandwidth, for the four page builds that were measured
// (W3b plain and brotli; W3e + W3f plain and brotli). Each configuration was measured twice — unthrottled and at
// 100 Mbit/s on the local test server (bandwidth only, no round trips) — and the bar is the straight line through
// those two points: startup = the unthrottled time, download = the slope's megabytes over the chosen bandwidth.
// Exactly the measurement at 100 Mbit/s and «∞»; an estimate elsewhere. Export shows 100 Mbit/s.
// Below: where the 5.6 s before the menu went with the data already cached (W3c) and the first frame after W3e.
// Data: data/web_delivery.json (scripts/collect_web.py).
const d = data as any
const nav = useNav()
const configs = d.configs as any[]
const st = d.startup

const MIN = 5
const MAXB = 1000
const pos = ref(Math.log(100 / MIN) / Math.log(MAXB / MIN)) // 0..1 on a log scale
const inf = ref(false)
const bw = computed(() => (nav.isPrintMode.value ? 100 : MIN * (MAXB / MIN) ** pos.value))
const local = computed(() => !nav.isPrintMode.value && inf.value)
function setBw(v: number) {
  inf.value = false
  pos.value = Math.log(v / MIN) / Math.log(MAXB / MIN)
}
const chips = [10, 25, 50, 100, 300, 1000]
const measured = computed(() => local.value || Math.abs(bw.value - 100) < 0.6)
const bwText = computed(() => (local.value ? 'без ограничения' : `${bw.value >= 100 ? Math.round(bw.value) : bw.value.toFixed(bw.value < 20 ? 1 : 0).replace('.', ',')} Мбит/с`))

const rows = computed(() => configs.map((c) => {
  const net = local.value ? 0 : (c.effectiveMB * 8) / bw.value
  return { ...c, net, cpu: c.firstFrameLocal, total: net + c.firstFrameLocal }
}))
const niceMax = computed(() => {
  const m = Math.max(...rows.value.map(r => r.total))
  const steps = [2, 5, 10, 15, 20, 30, 50, 75, 100, 150, 200, 300, 500, 750, 1000, 1500, 2000]
  return steps.find(s => s >= m * 1.02) ?? m
})
const ticks = computed(() => {
  const m = niceMax.value
  const step = m <= 2 ? 0.5 : m <= 10 ? 2 : m <= 20 ? 5 : m <= 50 ? 10 : m <= 100 ? 25 : m <= 300 ? 50 : m <= 1000 ? 200 : 500
  const out: number[] = []
  for (let t = 0; t <= m + 1e-9; t += step) out.push(Math.round(t * 10) / 10)
  return out
})

const W = 884
const xl = 236
const xr = W - 108
const X = (v: number) => xl + (v / niceMax.value) * (xr - xl)
const RH = 36
const y0 = 18
const H = y0 + configs.length * RH + 34
const sec = (v: number) => {
  if (v >= 120)
    return `≈ ${(v / 60).toFixed(1).replace('.', ',')} мин`
  return `${v.toFixed(1).replace('.', ',')} с`
}
const f1 = (v: number) => v.toFixed(1).replace('.', ',')

// attribution bar (W3c) and the first frame after W3e
const parts = [
  { k: 'SHA-256 всех файлов', v: st.sha256, hot: true },
  { k: 'ждёт подкачку', v: st.prefetchWait },
  { k: 'чтение из кэша', v: st.cacheReads },
  { k: 'LZ4', v: st.lz4 },
  { k: 'прочее', v: st.other },
]
const AW = 884
const ax = (v: number) => 236 + (v / 6) * (AW - 108 - 236)
let acc = 0
const segs = parts.map((p) => {
  const s = { ...p, x0: ax(acc), x1: ax(acc + p.v) }
  acc += p.v
  return s
})
const tip = ref<{ x: number, y: number, text: string } | null>(null)
function rowTip(r: any, i: number) {
  tip.value = {
    x: X(r.total),
    y: y0 + i * RH,
    text: `${r.label} (${r.step}, ${r.commit}): замер ${f1(r.firstFrame100)} с при 100 Мбит/с и ${String(r.firstFrameLocal).replace('.', ',')} с без ограничения; по сети ${f1(r.wireMB)} МБ`,
  }
}
</script>

<template>
  <div class="fv" @pointerleave="tip = null">
    <div class="ctl" @keydown.stop>
      <span class="lbl">скорость канала</span>
      <input
        v-model.number="pos" type="range" min="0" max="1" step="0.001" class="rng" aria-label="скорость канала"
        :disabled="nav.isPrintMode.value" @input="inf = false"
      >
      <span class="bw">{{ bwText }}</span>
      <span class="chips">
        <button v-for="c in chips" :key="c" class="chip" :class="{ on: !local && Math.abs(bw - c) < 0.6 }" @click="setBw(c)">{{ c >= 1000 ? '1 Гбит/с' : c }}{{ c === 100 ? ' · замер' : '' }}</button>
        <button class="chip" :class="{ on: local }" @click="inf = true">∞ · замер</button>
      </span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`Секунды до меню при ${bwText}`">
      <g v-for="t in ticks" :key="t">
        <line :x1="X(t)" :x2="X(t)" :y1="y0 - 4" :y2="y0 + configs.length * RH" stroke="var(--grid)" />
        <text class="tick" :x="X(t)" :y="y0 + configs.length * RH + 13" text-anchor="middle">{{ t }}</text>
      </g>
      <text class="tick" :x="xr" :y="y0 + configs.length * RH + 28" text-anchor="end">секунды до первого кадра меню</text>
      <text class="cap" x="0" :y="y0 - 6">сборка страницы</text>
      <g v-for="(r, i) in rows" :key="r.label" class="row" tabindex="0" @pointerenter="rowTip(r, i)" @focus="rowTip(r, i)" @blur="tip = null">
        <rect x="0" :y="y0 + i * RH" :width="W" :height="RH" fill="transparent" />
        <text class="nm" x="0" :y="y0 + i * RH + 16">{{ r.label }}</text>
        <text class="st" x="0" :y="y0 + i * RH + 29">{{ r.step }} · {{ r.commit }} · {{ f1(r.wireMB) }} МБ по сети</text>
        <rect :x="xl" :y="y0 + i * RH + 8" :width="Math.max(0, X(r.net) - xl - (r.net > 0 ? 2 : 0))" height="20" rx="3" fill="var(--s1)" />
        <rect :x="X(r.net)" :y="y0 + i * RH + 8" :width="Math.max(1.5, X(r.total) - X(r.net))" height="20" rx="3" fill="var(--s2)" />
        <text class="val" :x="X(r.total) + 6" :y="y0 + i * RH + 22.5">{{ sec(r.total) }}</text>
      </g>
    </svg>
    <div class="leg">
      <span><i class="sw" style="background: var(--s1)" />скачать нужное до меню</span>
      <span><i class="sw" style="background: var(--s2)" />старт программы в браузере</span>
      <span class="tag" :class="{ est: !measured }">{{ measured ? 'это замер: Chromium, 3 холодных визита' : 'оценка: прямая через два замера' }}</span>
    </div>

    <div class="attr">
      <svg :viewBox="`0 0 ${AW} 84`" width="100%" role="img" :aria-label="`До меню ${f1(st.firstFrame)} с: SHA-256 ${f1(st.sha256)} с; после W3e ${f1(st.after)} с`">
        <text class="nm" x="0" y="15">куда уходили {{ f1(st.firstFrame) }} с до меню</text>
        <text class="st" x="0" y="28">данные уже в кэше · профиль воркера, W3c</text>
        <g v-for="s in segs" :key="s.k">
          <rect :x="s.x0" y="4" :width="s.x1 - s.x0 - 2" height="22" rx="3" :fill="s.hot ? 'var(--s2)' : '#8a3d1e'"><title>{{ s.k }}: ≈ {{ f1(s.v) }} с</title></rect>
          <text class="in" :x="s.x0 + 5" y="19">{{ f1(s.v) }}</text>
          <text class="seg" :x="(s.x0 + s.x1 - 2) / 2" y="38" text-anchor="middle">{{ s.k }}</text>
        </g>
        <text class="val" :x="ax(st.firstFrame) + 6" y="20">{{ f1(st.firstFrame) }} с</text>
        <text class="nm" x="0" y="62">меню раньше пакетов, W3e</text>
        <text class="st" x="0" y="75">первый кадр, 3 холодных визита</text>
        <rect :x="ax(0)" y="50" :width="ax(st.after) - ax(0)" height="22" rx="3" fill="var(--s2)" />
        <text class="val" :x="ax(st.after) + 6" y="66">{{ f1(st.after) }} с <tspan class="st">вместо {{ f1(st.before) }}: меню нужно {{ f1(st.menuNeedsMB) }} МБ, а до него читались и хешировались все {{ f1(st.digestedMB) }} МБ</tspan></text>
      </svg>
    </div>
    <div v-if="tip" class="tip" :style="{ left: `${(Math.min(tip.x, W - 200) / W) * 100}%`, top: `${((tip.y + 26) / (H + 110)) * 100}%` }">
      {{ tip.text }}
    </div>
  </div>
</template>

<style scoped>
.fv {
  position: relative;
}
.ctl {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.25rem;
  flex-wrap: nowrap;
}
.lbl {
  font-size: 0.66rem;
  color: var(--muted);
  white-space: nowrap;
}
.rng {
  width: 190px;
  accent-color: var(--naruto);
}
.bw {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--ink);
  min-width: 8.6rem;
  white-space: nowrap;
}
.chips {
  display: flex;
  gap: 0.3rem;
  flex-wrap: nowrap;
}
.chip {
  font-family: var(--font-sans);
  font-size: 0.64rem;
  color: var(--ink-2);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--hair);
  border-radius: 999px;
  padding: 0.1rem 0.5rem;
  white-space: nowrap;
  cursor: pointer;
}
.chip.on {
  color: #1a0d05;
  background: var(--naruto);
  border-color: var(--naruto);
  font-weight: 650;
}
.cap {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
}
.row {
  outline: none;
}
.nm {
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 650;
  fill: var(--ink);
}
.st {
  font-family: var(--font-sans);
  font-size: 10px;
  font-weight: 400;
  fill: var(--muted);
}
.val {
  font-family: var(--font-sans);
  font-size: 12.5px;
  font-weight: 700;
  fill: var(--ink);
  font-variant-numeric: tabular-nums;
}
.tick {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
  font-variant-numeric: tabular-nums;
}
.seg {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--ink-2);
}
.in {
  font-family: var(--font-sans);
  font-size: 10.5px;
  font-weight: 600;
  fill: #fff;
}
.leg {
  display: flex;
  gap: 1.1rem;
  align-items: center;
  font-size: 0.64rem;
  color: var(--ink-2);
  margin: 0.1rem 0 0.4rem;
}
.leg span {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.sw {
  display: inline-block;
  width: 11px;
  height: 11px;
  border-radius: 3px;
}
.tag {
  margin-left: auto;
  font-size: 0.64rem;
  color: #a6e3a6;
  border: 1px solid rgba(12, 163, 12, 0.6);
  border-radius: 999px;
  padding: 0.05rem 0.55rem;
}
.tag.est {
  color: #ffd27a;
  border-color: rgba(250, 178, 25, 0.6);
}
.attr {
  border-top: 1px solid var(--grid);
  padding-top: 0.35rem;
}
.tip {
  position: absolute;
  pointer-events: none;
  background: #0c1017;
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 8px;
  padding: 0.25rem 0.5rem;
  font-size: 0.64rem;
  color: var(--ink);
  max-width: 360px;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.5);
  z-index: 5;
}
</style>
