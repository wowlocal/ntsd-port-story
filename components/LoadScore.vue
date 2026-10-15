<script setup lang="ts">
// Before the loop (branch start 0034e45) and after it (L20, e184b10), one row per metric with its own scale:
// the grey track is the "before" value, the coloured bar the "after" value as a share of it.
// Data: data/loading_steps.json (baseline, final), data/loading_method.json (frame-time audit)
// (scripts/collect_loading.py).
import steps from '../data/loading_steps.json'
import method from '../data/loading_method.json'

const b = (steps as any).baseline
const f = (steps as any).final
const ft = (method as any).frameAudit
const best = (steps as any).waterfall.loadEnd.load[0] as number
const f1 = (v: number) => v.toLocaleString('ru-RU', { minimumFractionDigits: 1, maximumFractionDigits: 1 })
const f2 = (v: number) => v.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const f0 = (v: number) => Math.round(v).toLocaleString('ru-RU')
const times = (a: number, c: number) => `×${(a / c).toLocaleString('ru-RU', { maximumFractionDigits: a / c >= 10 ? 0 : 1 })}`
interface Row { host: string, k: string, sub: string, a: number, c: number, fa: string, fc: string, ratio: string, color: string }
const rows: Row[] = [
  { host: 'A12', k: 'экран загрузки', sub: `L20: ${f.a12.runs} прогонов, ${f1(f.a12.load[1])}–${f1(f.a12.load[2])} с; лучший гейт — ${f1(best)} с`, a: b.a12.load[0], c: f.a12.load[0], fa: `${f1(b.a12.load[0])} с`, fc: `${f1(f.a12.load[0])} с`, ratio: times(b.a12.load[0], f.a12.load[0]), color: 'var(--s2)' },
  { host: 'A12', k: 'запуск → меню', sub: `${f1(f.a12.startToLoaded[1])}–${f1(f.a12.startToLoaded[2])} с; больше половины — старт и меню`, a: b.a12.startToLoaded[0], c: f.a12.startToLoaded[0], fa: `${f1(b.a12.startToLoaded[0])} с`, fc: `${f1(f.a12.startToLoaded[0])} с`, ratio: times(b.a12.startToLoaded[0], f.a12.startToLoaded[0]), color: 'var(--s2)' },
  { host: 'A12', k: 'первый запуск после установки', sub: 'распаковка 726 МБ ресурсов APK (S2)', a: f.a12.firstLaunch.before[0], c: f.a12.firstLaunch.after[0], fa: `${f1(f.a12.firstLaunch.before[0])} с`, fc: `${f1(f.a12.firstLaunch.after[0])} с`, ratio: `−${f1(f.a12.firstLaunch.before[0] - f.a12.firstLaunch.after[0])} с`, color: 'var(--s2)' },
  { host: 'A12', k: 'пик памяти', sub: 'RSS + swap; после — RAM-аудит со звуком, без музыки', a: b.a12.peak[0], c: f.a12.peakAudit[0], fa: `${f0(b.a12.peak[0])} МиБ`, fc: `${f0(f.a12.peakAudit[0])} МиБ`, ratio: `−${f0(b.a12.peak[0] - f.a12.peakAudit[0])} МиБ`, color: 'var(--s3)' },
  { host: 'A12', k: 'время кадра, главный поток', sub: `vs, 3 раунда: ${f2(ft.vsMain[0][1])}–${f2(ft.vsMain[0][2])} против ${f2(ft.vsMain[1][1])}–${f2(ft.vsMain[1][2])}`, a: ft.vsMain[0][0], c: ft.vsMain[1][0], fa: `${f2(ft.vsMain[0][0])} мс`, fc: `${f2(ft.vsMain[1][0])} мс`, ratio: 'в шуме', color: 'var(--s1)' },
  { host: 'Mac', k: 'экран загрузки', sub: 'headless-сборка без проверок эксклюзивности, 3 + 3', a: b.mac.load[0], c: f.mac.load[0], fa: `${f2(b.mac.load[0])} с`, fc: `${f2(f.mac.load[0])} с`, ratio: times(b.mac.load[0], f.mac.load[0]), color: 'var(--s2)' },
  { host: 'Mac', k: 'пик памяти', sub: 'phys_footprint_peak', a: b.mac.peak[0], c: f.mac.peak[0], fa: `${f0(b.mac.peak[0])} МБ`, fc: `${f0(f.mac.peak[0])} МБ`, ratio: `−${f0(b.mac.peak[0] - f.mac.peak[0])} МБ`, color: 'var(--s3)' },
]
</script>

<template>
  <div class="score">
    <div class="head">
      <span />
      <span>до · 10 окт</span>
      <span>после · 11 окт</span>
      <span />
      <span />
    </div>
    <div v-for="(r, i) in rows" :key="i" class="row" :class="{ first: i === 0 || rows[i - 1].host !== r.host }">
      <div class="lab">
        <span class="host pixel">{{ r.host }}</span>
        <span class="k">{{ r.k }}</span>
        <div class="sub">
          {{ r.sub }}
        </div>
      </div>
      <div class="va">
        {{ r.fa }}
      </div>
      <div class="vc">
        {{ r.fc }}
      </div>
      <div class="track">
        <div class="fill" :style="{ width: `${Math.min(100, (r.c / r.a) * 100)}%`, background: r.color }" />
      </div>
      <div class="ratio">
        {{ r.ratio }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.score {
  display: flex;
  flex-direction: column;
}
.head,
.row {
  display: grid;
  grid-template-columns: 330px 78px 82px 1fr 84px;
  gap: 0.7rem;
  align-items: center;
}
.head {
  font-size: 0.62rem;
  color: var(--muted);
  border-bottom: 1px solid var(--axis);
  padding-bottom: 0.15rem;
}
.head span:nth-child(2),
.head span:nth-child(3) {
  text-align: right;
}
.row {
  padding: 0.16rem 0;
  border-bottom: 1px solid var(--grid);
}
.row.first:not(:nth-child(2)) {
  border-top: 1px solid var(--axis);
}
.host {
  display: inline-block;
  width: 2.3rem;
  font-size: 0.66rem;
  color: var(--naruto);
}
.k {
  font-size: 0.78rem;
  font-weight: 650;
  color: var(--ink);
}
.sub {
  font-size: 0.6rem;
  color: var(--muted);
  margin-left: 2.3rem;
  line-height: 1.25;
}
.va {
  text-align: right;
  font-size: 0.78rem;
  color: var(--ink-2);
}
.vc {
  text-align: right;
  font-size: 0.92rem;
  font-weight: 650;
  color: var(--ink);
  white-space: nowrap;
}
.track {
  position: relative;
  height: 14px;
  background: #2a3142;
  border-radius: 3px;
}
.fill {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  border-radius: 3px;
  min-width: 3px;
}
.ratio {
  font-size: 0.8rem;
  font-weight: 650;
  color: var(--ink);
  white-space: nowrap;
}
</style>
