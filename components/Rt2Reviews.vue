<script setup lang="ts">
// Chapter 15: every ledger row 4m..4ad as a column; the rows are the independent review and the gates its evidence
// records (all 10 scenarios equal with frames identical, AppKit, the Android emulator, ThreadSanitizer). Hover a column
// for its step; the five steps where the review (or a gate) found a defect before the commit carry a numbered mark,
// explained beside the grid. Data: data/rt2_steps.json (scripts/collect_realtime2.py).
import { computed, ref } from 'vue'
import data from '../data/rt2_steps.json'

const steps = (data as any).steps as any[]
const W = 884
const L = 120
const CW = (W - L) / steps.length
const rows = [
  { key: 'review', name: 'независимое ревью' },
  { key: 'scenarios10', name: '10 сценариев, кадры' },
  { key: 'appkit', name: 'AppKit, 3 960 кадров' },
  { key: 'emulator', name: 'эмулятор Android' },
  { key: 'tsan', name: 'ThreadSanitizer' },
]
const RH = 21
const top = 22
const H = top + rows.length * RH + 6
const caught = steps.map((s, i) => ({ s, i })).filter(o => o.s.review === 'caught')
const mark = (i: number) => caught.findIndex(o => o.i === i) + 1
const dayName: Record<string, string> = { '10-07': '7 окт', '10-08': '8 окт', '10-09': '9 окт', '10-10': '10 окт' }
const days = Object.keys(dayName).map((k) => {
  const idx = steps.map((s, i) => ({ s, i })).filter(o => o.s.time?.startsWith(k)).map(o => o.i)
  return { k, name: dayName[k], a: Math.min(...idx) }
})
const fill = (s: any, key: string) => {
  if (key === 'review') {
    if (s.review === 'ok' || s.review === 'nits')
      return 'var(--good)'
    if (s.review === 'caught')
      return 'var(--warning)'
    return null
  }
  return s.gates[key] ? 'var(--good)' : null
}
const outline = (s: any, key: string) => key === 'review' && s.review === 'skipped'
const hover = ref<number | null>(null)
const hs = computed(() => (hover.value == null ? null : steps[hover.value]))
const day = (t: string) => `${Number(t.slice(3, 5))} окт, ${t.slice(6)}`
const reviewText: Record<string, string> = {
  ok: 'ревью: одобрено', nits: 'ревью: одобрено с замечаниями, они учтены', caught: 'ревью или ворота нашли дефект — исправлен до коммита',
  skipped: 'ревью не требовалось — причина записана', none: 'поля ревью нет',
}
const verdictText: Record<string, string> = {
  kept: 'быстрее', less: 'меньше работы', reverted: 'откат', parked: 'отложено', follow: 'доработка', test: 'тесты',
  telemetry: 'телеметрия', procedure: 'процедура', build: 'сборки', decision: 'решение автора',
}
const counts = computed(() => ({
  approved: steps.filter(s => s.review === 'ok' || s.review === 'nits').length,
  caught: caught.length,
  skipped: steps.filter(s => s.review === 'skipped').length,
}))
</script>

<template>
  <div class="rv" @pointerleave="hover = null">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`75 ступеней: ревью и ворота каждой`">
      <g v-for="dd in days" :key="dd.k">
        <line :x1="L + dd.a * CW" :x2="L + dd.a * CW" y1="2" :y2="H - 4" stroke="var(--axis)" />
        <text :x="L + dd.a * CW + 3" y="11" class="dy">{{ dd.name }}</text>
      </g>
      <g v-for="(r, ri) in rows" :key="r.key">
        <text x="0" :y="top + ri * RH + 12.5" class="rn">{{ r.name }}</text>
        <g v-for="(s, i) in steps" :key="s.id + ri">
          <rect v-if="fill(s, r.key)" :x="L + i * CW + 1" :y="top + ri * RH + 1" :width="CW - 2" :height="RH - 6" rx="2" :fill="fill(s, r.key)!" :style="{ opacity: hover == null || hover === i ? 1 : 0.55 }" />
          <rect v-else-if="outline(s, r.key)" :x="L + i * CW + 1.5" :y="top + ri * RH + 1.5" :width="CW - 3" :height="RH - 7" rx="2" fill="none" stroke="#535c70" stroke-width="1.2" />
          <circle v-else :cx="L + i * CW + CW / 2" :cy="top + ri * RH + 8" r="1.6" fill="var(--axis)" />
        </g>
      </g>
      <g v-for="o in caught" :key="`m${o.i}`">
        <text :x="L + o.i * CW + CW / 2" y="20" text-anchor="middle" class="mk">{{ mark(o.i) }}</text>
      </g>
      <rect
        v-for="(s, i) in steps" :key="`h${i}`" :x="L + i * CW" y="12" :width="CW" :height="H - 12"
        :fill="hover === i ? 'rgba(255,255,255,0.07)' : 'transparent'" @pointerenter="hover = i"
      />
    </svg>
    <div class="cap">
      <template v-if="hs">
        <span class="pixel cid">{{ hs.id === 'R2@09' ? 'R2' : hs.id }}</span>
        <span class="mono cw">{{ day(hs.time) }} · {{ hs.hash }}</span>
        <span>{{ hs.label }} · {{ verdictText[hs.verdict] }} · {{ reviewText[hs.review] }}</span>
      </template>
      <template v-else>
        <span><i class="sq good" />одобрено независимым ревью · {{ counts.approved }}</span>
        <span><i class="sq warn" />дефект найден до коммита · {{ counts.caught }}</span>
        <span><i class="sq out" />ревью не требовалось · {{ counts.skipped }}</span>
        <span><i class="sq good" />ворота пройдены</span>
        <span><i class="dt" />нет в записи</span>
      </template>
    </div>
  </div>
</template>

<style scoped>
.dy {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.rn {
  font-size: 11.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.mk {
  font-size: 10px;
  fill: var(--ink);
  font-family: var(--font-pixel);
}
.cap {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  height: 1.1rem;
  font-size: 0.62rem;
  color: var(--ink-2);
  white-space: nowrap;
  overflow: hidden;
  margin-top: 0.1rem;
}
.cap span {
  display: inline-flex;
  align-items: center;
}
.cid {
  color: var(--naruto);
  font-size: 0.75rem;
}
.cw {
  color: var(--muted);
  font-size: 0.6rem;
}
.sq {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 2px;
  margin-right: 0.35rem;
}
.sq.good {
  background: var(--good);
}
.sq.warn {
  background: var(--warning);
}
.sq.out {
  border: 1.3px solid #535c70;
}
.dt {
  display: inline-block;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--axis);
  margin-right: 0.35rem;
}
</style>
