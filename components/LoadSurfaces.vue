<script setup lang="ts">
// Memory the game asked for against memory it used. Left: the 891 display surfaces of a vs run (1.14 GB allocated),
// one cell each; filled: the 65-77 a whole match touches (attribution probe, 10 Oct). Cell order is not the game's.
// Right: the sprite sheets' file bytes before M1, after M1 (compressed, the compressor's spare capacity still held)
// and after M3; and the A12's native heap at the RAM audit: allocated vs private dirty (actually in RAM).
// Data: data/loading_method.json (scripts/collect_loading.py).
import data from '../data/loading_method.json'

const d = data as any
const s = d.surfaces
const a = d.ramAudit
const COLS = 54
const C = 7
const G = 2
const total = s.total as number
const lo = s.touched[0] as number
const hi = s.touched[1] as number
const cells = Array.from({ length: total }, (_, i) => ({ i, x: (i % COLS) * (C + G), y: Math.floor(i / COLS) * (C + G) }))
const WW = COLS * (C + G)
const HH = Math.ceil(total / COLS) * (C + G)

const W = 400
const L = 132
const bar = (v: number, max: number) => ((W - L - 70) * v) / max
const f0 = (v: number) => Math.round(v).toLocaleString('ru-RU')
const sheets = [
  { k: 'до M1', v: s.sheetBytesMB, fill: '#5d6679', note: 'байты файлов' },
  { k: 'M1', v: s.compressedHeldMB, fill: 'var(--s3)', note: 'LZ4 + резерв буфера' },
  { k: 'M3', v: s.compressedMB, fill: 'var(--s3)', note: 'по своему размеру' },
]
</script>

<template>
  <div class="sf">
    <div class="left">
      <div class="cap">
        <b>{{ total }}</b> поверхностей спрайтов · {{ String(s.allocatedGB).replace('.', ',') }} ГБ выделено
      </div>
      <svg :viewBox="`0 0 ${WW} ${HH}`" width="100%" role="img" :aria-label="`${total} поверхностей, за матч тронуты ${lo}–${hi}`">
        <rect v-for="c in cells" :key="c.i" :x="c.x" :y="c.y" :width="C" :height="C" rx="1.5"
              :fill="c.i < lo ? 'var(--s2)' : c.i < hi ? 'rgba(217,89,38,0.45)' : '#2a3142'" />
      </svg>
      <div class="key">
        <span><i class="sw" style="background: var(--s2)" />тронуты за целый матч VS: {{ lo }}–{{ hi }} ({{ s.touchedMB[0] }}–{{ s.touchedMB[1] }} МБ)</span>
        <span><i class="sw" style="background: #2a3142" />выделены и не тронуты ни разу</span>
      </div>
      <div class="note">
        Декодированные пиксели картинок за матч читаются {{ s.pixelReads }} раз. Порядок клеток условный.
      </div>
    </div>

    <div class="right">
      <div class="ph">
        Байты спрайт-листов в памяти, МБ
      </div>
      <svg :viewBox="`0 0 ${W} 96`" width="100%" role="img" aria-label="Байты спрайт-листов: до M1, после M1, после M3">
        <g v-for="(r, i) in sheets" :key="r.k" :transform="`translate(0, ${6 + i * 30})`">
          <text x="0" y="13" class="k">{{ r.k }}</text>
          <text x="0" y="25" class="kn">{{ r.note }}</text>
          <rect :x="L" y="2" :width="bar(r.v, s.sheetBytesMB)" height="18" rx="3" :fill="r.fill" />
          <text :x="L + bar(r.v, s.sheetBytesMB) + 6" y="15.5" class="v">{{ f0(r.v) }}</text>
        </g>
      </svg>
      <div class="ph mt">
        Куча A12 при RAM-аудите, МиБ
      </div>
      <svg :viewBox="`0 0 ${W} 70`" width="100%" role="img" aria-label="Куча A12: выделено и реально в RAM">
        <g transform="translate(0, 6)">
          <text x="0" y="13" class="k">выделено</text>
          <rect :x="L" y="2" :width="bar(a.nativeAllocated, a.nativeAllocated)" height="18" rx="3" fill="none" stroke="var(--ink-2)" stroke-width="1.4" />
          <text :x="L + bar(a.nativeAllocated, a.nativeAllocated) + 6" y="15.5" class="v">{{ f0(a.nativeAllocated) }}</text>
        </g>
        <g transform="translate(0, 36)">
          <text x="0" y="13" class="k">реально в RAM</text>
          <text x="0" y="25" class="kn">private dirty</text>
          <rect :x="L" y="2" :width="bar(a.nativeDirty[1], a.nativeAllocated)" height="18" rx="3" fill="var(--s1)" />
          <text :x="L + bar(a.nativeDirty[1], a.nativeAllocated) + 6" y="15.5" class="v">{{ a.nativeDirty[0] }}–{{ a.nativeDirty[1] }}</text>
        </g>
      </svg>
      <div class="note">
        Остальное — страницы поверхностей, которые никто не трогал: ядро не даёт им физической памяти. Человек так и написал в задании на аудит: «Большой размер allocation сам по себе не доказывает расход RAM».
      </div>
    </div>
  </div>
</template>

<style scoped>
.sf {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.6rem;
}
.cap {
  font-size: 0.74rem;
  color: var(--ink-2);
  margin-bottom: 0.3rem;
}
.cap b {
  color: var(--ink);
  font-size: 1rem;
}
.key {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  font-size: 0.66rem;
  color: var(--ink-2);
  margin-top: 0.35rem;
}
.key span {
  display: inline-flex;
  align-items: center;
}
.sw {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 2px;
  margin-right: 0.4rem;
}
.note {
  font-size: 0.64rem;
  line-height: 1.35;
  color: var(--muted);
  margin-top: 0.3rem;
}
.ph {
  font-size: 0.72rem;
  color: var(--ink-2);
  border-bottom: 1px solid var(--axis);
  padding-bottom: 0.15rem;
  margin-bottom: 0.1rem;
}
.ph.mt {
  margin-top: 0.4rem;
}
.k {
  font-size: 11px;
  font-weight: 600;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.kn {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.v {
  font-size: 11.5px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
</style>
