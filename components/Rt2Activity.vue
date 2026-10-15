<script setup lang="ts">
// Chapter 15: the 84 commits of 7–10 Oct on a clock-time axis (local, +0200). Tall ticks are commits named by a ledger
// row, short ticks the ledger/plan/status records and harness fixes. The bracket marks 8 Oct, when the loop stopped
// for the author's answer (question 09:38, answer 18:43, from the session log 1f9218ae). Hover a tick: the legend row
// under the strip shows that commit's time, hash and subject (verbatim); export shows the legend.
// Data: data/rt2_commits.json (scripts/collect_realtime2.py).
import { computed, ref } from 'vue'
import data from '../data/rt2_commits.json'

const d = data as any
const commits = d.commits as { hash: string, time: string, subject: string, kind: string }[]
const t = (s: string) => {
  const [md, hm] = s.split(' ')
  const dd = Number(md.split('-')[1])
  const [h, mi] = hm.split(':').map(Number)
  return (dd - 7) * 24 + h + mi / 60
}
const T0 = 8 // 7 Oct 08:00
const T1 = 3 * 24 + 19 // 10 Oct 19:00
const W = 884
const H = 72
const L = 6
const R = W - 6
const x = (h: number) => L + ((h - T0) / (T1 - T0)) * (R - L)
const base = 51
const kindH: Record<string, number> = { step: 28, record: 14, tool: 14 }
const kindC: Record<string, string> = { step: 'var(--s2)', record: 'var(--s7)', tool: 'var(--s3)' }
const ticks = commits.map(c => ({ ...c, h: t(c.time) }))
const days = [1, 2, 3].map(k => ({ h: k * 24, label: `${7 + k} окт` }))
const ask = t('10-08 09:38')
const ans = t('10-08 18:43')
const tag = t(d.tag.time)
const gapText = (() => {
  const mins = Math.round((ans - ask) * 60)
  return `${Math.floor(mins / 60)} ч ${String(mins % 60).padStart(2, '0')} мин`
})()
const hover = ref<number | null>(null)
const tip = computed(() => (hover.value == null ? null : ticks[hover.value]))
const when = (s: string) => `${Number(s.slice(3, 5))} окт, ${s.slice(6)}`
const counts = ['step', 'record', 'tool'].map(k => commits.filter(c => c.kind === k).length)
</script>

<template>
  <div class="act" @pointerleave="hover = null">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`${commits.length} коммита с 7 по 10 октября; 8 октября пауза ${gapText} в ожидании ответа автора`">
      <line :x1="L" :x2="R" :y1="base" :y2="base" stroke="var(--axis)" />
      <text :x="L" y="11" class="ax">7 окт, 08:00</text>
      <g v-for="dd in days" :key="dd.h">
        <line :x1="x(dd.h)" :x2="x(dd.h)" y1="2" :y2="base + 4" stroke="var(--grid)" />
        <text :x="x(dd.h) + 4" y="11" class="ax">{{ dd.label }}</text>
      </g>
      <!-- the wait -->
      <rect :x="x(ask)" :y="base - 30" :width="x(ans) - x(ask)" height="30" fill="rgba(250,178,25,0.10)" />
      <path :d="`M${x(ask)},${base - 32} V${base - 36} H${x(ans)} V${base - 32}`" fill="none" stroke="var(--warning)" stroke-width="1.2" />
      <text :x="(x(ask) + x(ans)) / 2" y="11" text-anchor="middle" class="gap">вопрос ждал ответа {{ gapText }}</text>
      <!-- tag -->
      <path :d="`M${x(tag)},${base + 3} l-4,7 h8 z`" fill="var(--ink)" />
      <text :x="x(tag) + 7" :y="base + 18" class="tg">тег rt-60fps-a12 · 19:49</text>
      <!-- ticks -->
      <g v-for="(c, i) in ticks" :key="c.hash" class="tk" @pointerenter="hover = i">
        <rect :x="x(c.h) - 4" :y="base - 32" width="8" height="34" fill="transparent" />
        <line :x1="x(c.h)" :x2="x(c.h)" :y1="base" :y2="base - kindH[c.kind]" :stroke="kindC[c.kind]" :stroke-width="hover === i ? 3.2 : 1.8" stroke-linecap="round" />
      </g>
    </svg>
    <div class="leg">
      <template v-if="tip">
        <span class="mono tt">{{ when(tip.time) }} · {{ tip.hash }}</span><span class="mono ts" lang="en">{{ tip.subject }}</span>
      </template>
      <template v-else>
        <span><i class="k" style="background: var(--s2)" />шаг реестра · {{ counts[0] }}</span>
        <span><i class="k short" style="background: var(--s7)" />запись реестра, плана, статуса · {{ counts[1] }}</span>
        <span><i class="k short" style="background: var(--s3)" />харнесс и установка на телефон · {{ counts[2] }}</span>
        <span class="hint">наведите на штрих — тема коммита</span>
      </template>
    </div>
  </div>
</template>

<style scoped>
.ax {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.gap {
  font-size: 10.5px;
  fill: var(--ink);
  font-family: var(--font-sans);
  font-weight: 600;
}
.tg {
  font-size: 10px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.tk {
  cursor: default;
}
.leg {
  display: flex;
  align-items: center;
  gap: 1rem;
  height: 1.05rem;
  font-size: 0.62rem;
  color: var(--ink-2);
  white-space: nowrap;
  overflow: hidden;
}
.leg span {
  display: inline-flex;
  align-items: center;
}
.k {
  display: inline-block;
  width: 2.5px;
  height: 12px;
  border-radius: 1px;
  margin-right: 0.35rem;
}
.k.short {
  height: 7px;
}
.hint {
  margin-left: auto;
  color: var(--muted);
}
.tt {
  color: var(--naruto);
  font-size: 0.62rem;
}
.ts {
  color: var(--ink);
  font-size: 0.62rem;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
