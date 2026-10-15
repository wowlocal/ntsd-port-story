<script setup lang="ts">
// Chapter 18, PHONE_CONTROLLER C2: the evening test on the user's Pixel 10 (adb over Wi-Fi), 18:44–19:05.
// The user's three messages, the three runs of the game (pid), when the controller was attached, the JIT-thread
// SIGSEGV logged while run 3 closed and the commit. Hover a run for its details.
// Data: data/rel_controller.json, data/rel_day.json (scripts/collect_release.py).
import { computed, ref } from 'vue'
import ctl from '../data/rel_controller.json'
import day from '../data/rel_day.json'

const c = ctl as any
const dy = day as any
const sec = (t: string) => {
  const [h, m, s] = t.split(':').map(Number)
  return h * 3600 + m * 60 + (s || 0)
}
const T0 = sec('18:44')
const T1 = sec('19:05')
const W = 884
const H = 132
const m = { l: 116, r: 10 }
const x = (t: string | number) => m.l + (((typeof t === 'string' ? sec(t) : t) - T0) / (T1 - T0)) * (W - m.l - m.r)
const ticks = ['18:44', '18:46', '18:48', '18:50', '18:52', '18:54', '18:56', '18:58', '19:00', '19:02', '19:04']

const msgs = [
  { t: dy.user.caffeine, text: '«убирай кофеин»', row: 0 },
  { t: dy.user.pixel, text: '«поставь сборку на подключенный pixel, я протестирую геймпад»', row: 1 },
  { t: dy.user.works, text: '«все работает»', row: 0 },
]
const commit = dy.commits.find((k: any) => k.hash === 'd4619cbc')
const runs = (c.runs as any[]).map((r, i) => ({ ...r, n: i + 1 }))
const spans = c.attachedSpans as any[]
const sel = ref(3)
const cur = computed(() => runs.find(r => r.n === sel.value)!)
const dur = (r: any) => {
  const s = sec(r.to) - sec(r.from)
  return s < 60 ? `${s} с` : `${Math.floor(s / 60)} мин ${String(s % 60).padStart(2, '0')} с`
}
const attachedAt = (r: any) => {
  const s = spans.find(sp => sec(sp.from) >= sec(r.from) && sec(sp.from) <= sec(r.to))
  return s ? (s.earliest ? `между ${s.earliest} и ${s.from}` : s.from) : '—'
}
const yMsg = 14
const yRun = 66
const yAtt = 96
</script>

<template>
  <div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Вечерняя проверка на Pixel 10: сообщения автора, три запуска игры, подключение контроллера">
      <text class="lane" x="0" :y="yMsg + 14">автор</text>
      <text class="lane" x="0" :y="yRun + 4">запуски игры</text>
      <text class="lane" x="0" :y="yAtt + 4">контроллер</text>
      <line v-for="t in ticks" :key="t" :x1="x(t)" :x2="x(t)" :y1="yRun - 18" :y2="H - 18" class="gl" />
      <text v-for="t in ticks" :key="`l${t}`" class="ax" :x="x(t)" :y="H - 5" text-anchor="middle">{{ t }}</text>

      <!-- the user's messages -->
      <g v-for="(mm, i) in msgs" :key="i">
        <line :x1="x(mm.t)" :x2="x(mm.t)" :y1="yMsg + mm.row * 16 + 4" :y2="yRun - 12" stroke="var(--s1)" stroke-width="1" />
        <circle :cx="x(mm.t)" :cy="yMsg + mm.row * 16 + 4" r="3.5" fill="var(--s1)" />
        <text class="msg" :x="x(mm.t) + 7" :y="yMsg + mm.row * 16 + 8"><tspan class="tm">{{ mm.t }}</tspan> {{ mm.text }}</text>
      </g>

      <!-- runs -->
      <g v-for="r in runs" :key="r.pid" class="run" :class="{ sel: sel === r.n }" tabindex="0" @pointerenter="sel = r.n" @focus="sel = r.n">
        <rect :x="x(r.from)" :y="yRun - 8" :width="Math.max(4, x(r.to) - x(r.from) - 2)" height="16" rx="4" :fill="r.controllerAtLaunch ? 'var(--s2)' : 'var(--axis)'" />
        <text v-if="x(r.to) - x(r.from) > 60" class="in" :x="(x(r.from) + x(r.to)) / 2" :y="yRun + 4" text-anchor="middle">запуск {{ r.n }} · {{ dur(r) }}</text>
        <text v-else class="out" :x="(x(r.from) + x(r.to)) / 2" :y="yRun - 12" text-anchor="middle">{{ r.n }}</text>
        <rect :x="x(r.from)" :y="yRun - 12" :width="Math.max(14, x(r.to) - x(r.from))" height="24" class="hit" />
      </g>
      <!-- SIGSEGV at run 3's exit -->
      <g :transform="`translate(${x(runs[2].to)}, ${yRun})`">
        <path d="M0,-7 L7,0 L0,7 L-7,0 Z" fill="var(--critical)" stroke="var(--bg)" stroke-width="1.5" />
        <text class="bang" x="0" y="3.5" text-anchor="middle">!</text>
      </g>
      <text class="note" :x="x(runs[2].to) + 10" :y="yRun + 4">SIGSEGV при выходе</text>

      <!-- controller attached -->
      <rect :x="x(spans[0].earliest)" :y="yAtt - 6" :width="x(spans[0].from) - x(spans[0].earliest)" height="12" rx="3" class="fuzzy" />
      <rect v-for="(s, i) in spans" :key="`s${i}`" :x="x(s.from)" :y="yAtt - 6" :width="x(s.to) - x(s.from)" height="12" rx="3" fill="var(--s3)" style="opacity: 0.85">
        <title>{{ s.note }}</title>
      </rect>
      <text class="note" :x="x(spans[1].to) + 6" :y="yAtt + 4">отключён {{ spans[1].to }}</text>

      <!-- commit -->
      <line :x1="x(commit.time)" :x2="x(commit.time)" :y1="yRun - 18" :y2="yAtt + 8" stroke="var(--ink-2)" stroke-width="1" />
      <text class="cm" :x="x(commit.time) + 5" :y="yRun + 4">{{ commit.hash }}</text>
    </svg>
    <div class="det">
      <b>Запуск {{ cur.n }}</b> · pid {{ cur.pid }} · {{ cur.from }}–{{ cur.to }} ({{ dur(cur) }}) ·
      <span v-if="cur.controllerAtLaunch">контроллер подключён до старта — игра нашла его при запуске; это и есть сыгранный тест</span>
      <span v-else>контроллер подключили уже после старта ({{ attachedAt(cur) }}) — хост его не берёт: джойстики опрашиваются один раз, при запуске, как в оригинале</span>
    </div>
  </div>
</template>

<style scoped>
.lane { font-size: 10.5px; fill: var(--muted); font-family: var(--font-sans); }
.gl { stroke: var(--grid); stroke-width: 1; }
.ax { font-size: 10px; fill: var(--muted); font-family: var(--font-sans); font-variant-numeric: tabular-nums; }
.msg { font-size: 11px; fill: var(--ink); font-family: var(--font-sans); }
.tm { fill: var(--muted); font-family: var(--font-mono); font-size: 10px; }
.run { cursor: pointer; outline: none; }
.run.sel rect:first-child { stroke: var(--ink); stroke-width: 1.5; }
.in { font-size: 10.5px; fill: #fff; font-weight: 650; font-family: var(--font-sans); pointer-events: none; }
.out { font-size: 10.5px; fill: var(--ink-2); font-family: var(--font-sans); }
.hit { fill: transparent; }
.bang { font-size: 10px; font-weight: 800; fill: #fff; font-family: var(--font-sans); pointer-events: none; }
.note { font-size: 10.5px; fill: var(--ink-2); font-family: var(--font-sans); }
.cm { font-size: 10px; fill: var(--ink-2); font-family: var(--font-mono); }
.fuzzy { fill: rgba(25, 158, 112, 0.25); }
.det { font-size: 0.66rem; color: var(--ink-2); line-height: 1.35; margin-top: 1px; }
.det b { color: var(--ink); }
</style>
