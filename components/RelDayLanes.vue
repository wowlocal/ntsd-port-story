<script setup lang="ts">
// Chapter 18: 13 October from 04:00 to 21:00 (CEST) in four lanes — the user's messages, the Claude Code
// session (assistant messages per hour), the two Codex sessions and the commits, with or without the
// "Co-Authored-By: Claude" trailer. Hover a commit or a session for details.
// Only timestamps, models and counters are used; no conversation text.
// Data: data/rel_day.json (scripts/collect_release.py).
import { computed, ref } from 'vue'
import day from '../data/rel_day.json'

const d = day as any
const min = (t: string) => {
  const [h, m, s] = t.split(':').map(Number)
  return h * 60 + m + (s || 0) / 60
}
const T0 = 4 * 60
const T1 = 21 * 60
const W = 884
const H = 214
const L = 128
const x = (t: string | number) => L + (((typeof t === 'string' ? min(t) : t) - T0) / (T1 - T0)) * (W - L - 8)
const ticks = [4, 6, 8, 10, 12, 14, 16, 18, 20]
const lane = { user: 20, claude: 70, codex: 120, commits: 164 }

const u = d.user
const userDots = [[u.memory, 0], [u.photo, 1], [u.iphone, 1], [u.caffeine, 0], [u.pixel, 0], [u.works, 0]] as [string, number][]
const userLabels = [
  { t: u.memory, row: 0, text: '«по памяти не утекает?»' },
  { t: u.photo, row: 1, text: 'фото джойстика · «сделай iPhone отдельную сборку»', dx: (min(u.iphone) - min(u.photo)) },
  { t: u.caffeine, row: 0, text: 'Pixel: «поставь сборку…», «все работает»', end: true },
]
const hours = (d.claude.byHour as { hour: number, messages: number }[]).filter(h => h.hour * 60 >= T0 && h.hour * 60 < T1)
const maxMsg = Math.max(...hours.map(h => h.messages))
const gap = d.claude.longestGap
const codex = (d.codex as any[]).filter(c => c.role === 'main')
const guardian = (d.codex as any[]).find(c => c.role === 'guardian')
const commits = (d.commits as any[]).filter(c => min(c.time) >= T0)
const nf = new Intl.NumberFormat('ru-RU')
const mln = (v: number) => `${new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 1 }).format(v / 1e6)} млн`

type Sel = { kind: 'commit', c: any } | { kind: 'codex', c: any }
const sel = ref<Sel>({ kind: 'commit', c: commits.find(c => c.hash === '0b5d4621') })
const detail = computed(() => {
  const s = sel.value
  if (s.kind === 'commit') {
    return `${s.c.time} · ${s.c.hash} · «${s.c.subject}» · ${s.c.trailer ? 'трейлер Co-Authored-By: Claude Opus 5.5' : 'без трейлера, пустое тело сообщения'}`
  }
  const c = s.c
  const cached = Math.round((c.tokens.cached / c.tokens.input) * 1000) / 10
  return `${c.start.slice(0, 5)}–${c.end.slice(0, 5)} · ${c.originator} ${c.cli} · ${c.model.join(', ')}, effort ${c.effort.join(', ')} · ${c.approval.join(', ')} / ${c.sandbox.join(', ')} · ходов ${c.turns}, вызовов инструментов ${c.toolCalls} · ${mln(c.tokens.total)} токенов, ${String(cached).replace('.', ',')} % входа из кэша · ветка ${c.branch} @ ${c.commit}`
})
</script>

<template>
  <div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="13 октября по часам: сообщения автора, сессия Claude, сессии Codex и коммиты">
      <g v-for="h in ticks" :key="h">
        <line :x1="x(h * 60)" :x2="x(h * 60)" :y1="6" :y2="H - 20" class="gl" />
        <text class="ax" :x="x(h * 60)" :y="H - 6" text-anchor="middle">{{ String(h).padStart(2, '0') }}:00</text>
      </g>

      <!-- lane labels -->
      <text class="ln" x="0" :y="lane.user + 8">автор</text>
      <text class="ln" x="0" :y="lane.claude + 4">Claude · Opus 5.5</text>
      <text class="lns" x="0" :y="lane.claude + 17">сообщений в час</text>
      <text class="ln" x="0" :y="lane.codex + 4">Codex · GPT-6 Astra</text>
      <text class="ln" x="0" :y="lane.commits + 4">коммиты</text>

      <!-- user -->
      <circle v-for="(t, i) in userDots" :key="`u${i}`" :cx="x(t[0])" :cy="lane.user + 4 + t[1] * 13" r="3.5" fill="var(--ink)" />
      <text v-for="(lb, i) in userLabels" :key="`ul${i}`" class="ut" :x="x(lb.t) + (lb.end ? -8 : 8 + (lb.dx ? x(T0 + lb.dx) - x(T0) : 0))" :y="lane.user + 8 + lb.row * 13" :text-anchor="lb.end ? 'end' : 'start'"><tspan class="tm">{{ lb.t }}</tspan> {{ lb.text }}</text>

      <!-- Claude: messages per hour -->
      <g v-for="h in hours" :key="`h${h.hour}`">
        <rect :x="x(h.hour * 60) + 1" :y="lane.claude + 12 - (h.messages / maxMsg) * 30" :width="x(60 + T0) - x(T0) - 2" :height="Math.max(1.5, (h.messages / maxMsg) * 30)" rx="2" fill="var(--s2)">
          <title>{{ String(h.hour).padStart(2, '0') }}:00–{{ String(h.hour + 1).padStart(2, '0') }}:00 · {{ h.messages }} сообщений агента</title>
        </rect>
      </g>
      <path :d="`M${x(gap.from)},${lane.claude + 6} V${lane.claude + 12} H${x(gap.to)} V${lane.claude + 6}`" class="gapl" />
      <text class="gapt" :x="(x(gap.from) + x(gap.to)) / 2" :y="lane.claude + 6" text-anchor="middle">{{ gap.from }} → {{ gap.to }}: ни одного сообщения, {{ Math.floor(gap.minutes / 60) }} ч {{ gap.minutes % 60 }} мин</text>

      <!-- Codex sessions -->
      <g v-for="c in codex" :key="c.id + c.start" class="hov" tabindex="0" @pointerenter="sel = { kind: 'codex', c }" @focus="sel = { kind: 'codex', c }">
        <rect :x="x(c.start) - 3" :y="lane.codex - 14" :width="Math.max(6, x(c.end) - x(c.start)) + 6" height="28" class="hit" />
        <rect :x="x(c.start)" :y="lane.codex - 7" :width="Math.max(3, x(c.end) - x(c.start))" height="14" rx="3" fill="var(--s1)" :class="{ selr: sel.kind === 'codex' && sel.c === c }" />
      </g>
      <rect :x="x(guardian.start)" :y="lane.codex + 9" :width="Math.max(3, x(guardian.end) - x(guardian.start))" height="5" rx="2" fill="var(--s3)">
        <title>ревьюер одобрений {{ guardian.model.join(', ') }}: {{ guardian.turns }} проверок</title>
      </rect>
      <text class="ct" :x="x(codex[0].end) + 6" :y="lane.codex + 4">Desktop и ревьюер одобрений: {{ codex[0].toolCalls }} вызовов, коммитов нет</text>
      <text class="ct" :x="x(codex[1].end) + 6" :y="lane.codex + 4"><tspan class="v">релиз</tspan> · {{ codex[1].toolCalls }} вызовов · {{ mln(codex[1].tokens.total) }} токенов</text>

      <!-- commits -->
      <g v-for="c in commits" :key="c.hash" class="hov" tabindex="0" @pointerenter="sel = { kind: 'commit', c }" @focus="sel = { kind: 'commit', c }">
        <circle :cx="x(c.time)" :cy="lane.commits" r="11" class="hit" />
        <circle :cx="x(c.time)" :cy="lane.commits" :r="sel.kind === 'commit' && sel.c === c ? 6.5 : 5" :fill="c.trailer ? 'var(--s2)' : 'var(--s1)'" stroke="var(--bg)" stroke-width="2" />
      </g>
      <text class="ct" :x="x('14:51') - 10" :y="lane.commits + 4" text-anchor="end">три коммита без трейлера Claude →</text>

      <!-- freeze -->
      <line :x1="x('20:14')" :x2="x('20:14')" :y1="lane.claude - 22" :y2="lane.commits + 12" class="frz" />
      <text class="ax" :x="x('20:14') + 4" :y="lane.commits + 18">20:14</text>
    </svg>
    <div class="det" aria-live="polite">{{ detail }}</div>
  </div>
</template>

<style scoped>
.gl { stroke: var(--grid); stroke-width: 1; }
.ax { font-size: 10px; fill: var(--muted); font-family: var(--font-sans); font-variant-numeric: tabular-nums; }
.ln { font-size: 11px; fill: var(--ink); font-weight: 600; font-family: var(--font-sans); }
.lns { font-size: 10px; fill: var(--muted); font-family: var(--font-sans); }
.ut { font-size: 10.5px; fill: var(--ink-2); font-family: var(--font-sans); }
.tm { fill: var(--muted); font-family: var(--font-mono); font-size: 10px; }
.gapl { stroke: var(--ink-2); stroke-width: 1; fill: none; }
.gapt { font-size: 10.5px; fill: var(--ink-2); font-family: var(--font-sans); }
.ct { font-size: 10.5px; fill: var(--ink-2); font-family: var(--font-sans); }
.ct .v { fill: var(--ink); font-weight: 700; }
.hov { cursor: pointer; outline: none; }
.hit { fill: transparent; }
.selr { stroke: var(--ink); stroke-width: 1.5; }
.frz { stroke: var(--ink-2); stroke-width: 1; }
.det { font-size: 0.62rem; color: var(--ink-2); line-height: 1.35; min-height: 1.7em; font-family: var(--font-sans); }
</style>
