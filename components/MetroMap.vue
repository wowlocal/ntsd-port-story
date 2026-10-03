<script setup lang="ts">
// The whole deck as one metro route: 13 chapters are stations. Line colour = who worked in that period:
// blue — Codex (7–27 Sep), orange — Claude (from 28 Sep). Chapters 9–11 cover the whole project, so the blue
// line runs alongside the orange there. The prologue (31 Mar) sits before the start, on a dotted pause.
// `visited` fills the stations up to that chapter; `current` puts a glow and a "вы здесь" pin on one station.
import { computed } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'

const props = withDefaults(defineProps<{ visited?: number, current?: number, here?: string, future?: boolean }>(), {
  visited: 0,
  current: 0,
  here: 'вы здесь',
  future: true,
})

type Kind = 'pre' | 'codex' | 'transfer' | 'claude' | 'both'
type Place = 'below' | 'below-start' | 'left' | 'right'
interface Station { n: number, title: string, sub: string, tip: string, kind: Kind, x: number, y: number, place: Place, cap?: { dx: number, dy: number } }

const W = 900
const H = 366
const yA = 52
const yB = 182
const yC = 312
const r = (yB - yA) / 2 // bend radius
const xR = 815 // right bend centre x
const xL = 95 // left bend centre x
const off = 8 // offset of the parallel blue line in the shared corridor (outer side of the left bend)

// facts: chapter covers (num, kicker, dates, stats) of pages/02-prologue.md … pages/13-lessons.md
const stations: Station[] = [
  { n: 1, title: 'Сначала был план', sub: '31 марта', tip: 'Пролог · 31 марта 2026 · 5 коммитов · потом 160 дней тишины', kind: 'pre', x: 44, y: yA, place: 'below-start' },
  { n: 2, title: 'Первый вечер', sub: '7 сентября', tip: 'Глава 2 · 7 сентября, 18:20–21:13 · 4 коммита практики · 1 разворот', kind: 'codex', x: 250, y: yA, place: 'below' },
  { n: 3, title: 'Ночной спринт', sub: '7–12 сентября', tip: 'Глава 3 · 171 коммит за 102 часа', kind: 'codex', x: 410, y: yA, place: 'below' },
  { n: 4, title: 'Свод правил', sub: '12–14 сентября', tip: 'Глава 4 · AGENTS.md 4 954 → 153 строки · WORKFLOW.md · реестр отказов', kind: 'codex', x: 570, y: yA, place: 'below' },
  { n: 5, title: 'Фабрика доказательств', sub: '22–27 сентября', tip: 'Глава 5 · 96 коммитов · 0 правок в native/Sources', kind: 'codex', x: 730, y: yA, place: 'below' },
  { n: 6, title: 'Поворот', sub: '28 сентября · пересадка', tip: 'Глава 6 · 15 коммитов · 13:31 → 23:56 · первый полный матч в приложении', kind: 'transfer', x: xR + r, y: yA + r, place: 'left' },
  { n: 7, title: 'Вся игра', sub: '29 сен — 2 окт', tip: 'Глава 7 · все режимы за день · 200 000 тиков без остановки · сетевой матч двух приложений', kind: 'claude', x: 690, y: yB, place: 'below' },
  { n: 8, title: 'Сверка с оригиналом', sub: '2–3 октября', tip: 'Глава 8 · 47 из 47 случайных матчей равны · 156 730 сверенных тиков', kind: 'claude', x: 500, y: yB, place: 'below' },
  { n: 9, title: 'Кунсткамера', sub: 'баги оригинала', tip: 'Глава 9 · что нашлось внутри EXE: баги оригинала, которые порт обязан повторить', kind: 'both', x: 310, y: yB, place: 'below', cap: { dx: 0, dy: -off } },
  { n: 10, title: 'В цифрах', sub: '463 коммита', tip: 'Глава 10 · 7 сентября — 3 октября · всё посчитано из git и evidence-файлов порта', kind: 'both', x: xL - r, y: yB + r, place: 'right', cap: { dx: -off, dy: 0 } },
  { n: 11, title: 'Под капотом агентов', sub: '6,3 млрд токенов', tip: 'Глава 11 · 34 сессии · 31 095 ответов моделей · 1 101 ход · 6,3 млрд токенов', kind: 'both', x: 205, y: yC, place: 'below', cap: { dx: 0, dy: off } },
  { n: 12, title: 'Сообщество', sub: '2007 → 2026', tip: 'Глава 12 · 2007 → 3 октября 2026 · Discord · лента · что дальше', kind: 'claude', x: 375, y: yC, place: 'below' },
  { n: 13, title: 'Уроки', sub: '3 октября · v0.4.0', tip: 'Глава 13 · Эпилог · релиз v0.4.0 · что дальше · чему научились', kind: 'claude', x: 545, y: yC, place: 'below' },
]
const planned = [
  { name: 'Linux', x: 668 },
  { name: 'Windows', x: 768 },
  { name: 'iPad', x: 862 },
]

const color: Record<Kind, string> = { pre: 'var(--muted)', codex: 'var(--s1)', transfer: 'var(--ink)', claude: 'var(--s2)', both: 'var(--ink-2)' }
const pad = (n: number) => String(n).padStart(2, '0')

// route pieces, in travel order; `d` is the reveal delay index
const st = (n: number) => stations[n - 1]
const routeDotted = `M${st(1).x},${yA} H${st(2).x}`
const routeBlue = `M${st(2).x},${yA} H${xR} A${r},${r} 0 0 1 ${xR + r},${yA + r}`
const routeOrange = `M${xR + r},${yA + r} A${r},${r} 0 0 1 ${xR},${yB} H${xL} A${r},${r} 0 0 0 ${xL - r},${yB + r} A${r},${r} 0 0 0 ${xL},${yC} H${st(13).x}`
const corridor = `M${st(9).x},${yB - off} H${xL} A${r + off},${r + off} 0 0 0 ${xL - r - off},${yB + r} A${r + off},${r + off} 0 0 0 ${xL},${yC + off} H${st(11).x}`
const routeFuture = `M${st(13).x},${yC} H${planned[planned.length - 1].x}`

const nav = useNav()
const active = useIsSlideActive()
const play = computed(() => active.value && !nav.isPrintMode.value)

const isVisited = (s: Station) => s.n <= props.visited
const labelPos = (s: Station) => {
  const capY = s.cap && s.cap.dy > 0 ? s.cap.dy : 0
  if (s.place === 'left')
    return { x: s.x - 24, y: s.y - 2, anchor: 'end' }
  if (s.place === 'right')
    return { x: s.x + 22, y: s.y - 2, anchor: 'start' }
  if (s.place === 'below-start')
    return { x: s.x - 11, y: s.y + 29 + capY, anchor: 'start' }
  return { x: s.x, y: s.y + 29 + capY, anchor: 'middle' }
}
const cur = computed(() => stations.find(s => s.n === props.current))
</script>

<template>
  <div class="metro" :class="{ play }">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Карта глав: маршрут истории порта">
      <!-- legend, in the free space between the first two rows -->
      <g class="legend" :transform="`translate(48, ${yA + 60})`">
        <line x1="0" x2="26" y1="0" y2="0" stroke="var(--s1)" stroke-width="6" stroke-linecap="round" />
        <text x="36" y="3.6">Codex · GPT-6 Astra · 7–27 сентября</text>
        <line x1="0" x2="26" y1="19" y2="19" stroke="var(--s2)" stroke-width="6" stroke-linecap="round" />
        <text x="36" y="22.6">Claude Opus 5.5 · с 28 сентября</text>
        <line x1="0" x2="26" y1="35.5" y2="35.5" stroke="var(--s1)" stroke-width="4" stroke-linecap="round" />
        <line x1="0" x2="26" y1="42.5" y2="42.5" stroke="var(--s2)" stroke-width="5" stroke-linecap="round" />
        <text x="36" y="42.6">обе линии — главы обо всём проекте</text>
      </g>

      <!-- route -->
      <path class="seg" style="--d: 0" :d="routeDotted" fill="none" stroke="var(--muted)" stroke-width="4.5" stroke-linecap="round" stroke-dasharray="0.1 9" />
      <text class="pause" :x="(st(1).x + st(2).x) / 2" :y="yA - 12" text-anchor="middle">160 дней тишины</text>
      <path class="seg" style="--d: 1" :d="routeBlue" fill="none" stroke="var(--s1)" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" />
      <path class="seg" style="--d: 6" :d="routeOrange" fill="none" stroke="var(--s2)" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" />
      <path class="seg" style="--d: 9" :d="corridor" fill="none" stroke="var(--s1)" stroke-width="4.5" stroke-linecap="round" />
      <g v-if="future" class="seg" style="--d: 13">
        <path :d="routeFuture" fill="none" stroke="var(--s2)" stroke-width="5" stroke-dasharray="9 7" style="opacity: 0.75" />
        <text class="pause" :x="(st(13).x + planned[planned.length - 1].x) / 2 + 20" :y="yC - 14" text-anchor="middle">что дальше</text>
        <g v-for="p in planned" :key="p.name">
          <circle :cx="p.x" :cy="yC" r="6.5" fill="var(--bg)" stroke="var(--s2)" stroke-width="2.5">
            <title>что дальше · ветка dev/crossplatform · {{ p.name }}</title>
          </circle>
          <text class="plan" :x="p.x" :y="yC + 26" text-anchor="middle">{{ p.name }}</text>
        </g>
      </g>

      <!-- highlight of the current station -->
      <g v-if="cur" class="here">
        <circle class="glow" :cx="cur.x" :cy="cur.y" r="21" fill="var(--naruto)" style="opacity: 0.22" />
        <g :transform="`translate(${cur.x}, ${cur.y - 33})`">
          <rect x="-34" y="-10" width="68" height="17" rx="3" fill="var(--naruto)" />
          <path d="M-5,7 L0,12 L5,7 Z" fill="var(--naruto)" />
          <text class="pin" x="0" y="3.2" text-anchor="middle">{{ here.toUpperCase() }}</text>
        </g>
      </g>

      <!-- stations -->
      <g v-for="s in stations" :key="s.n" class="st" :class="[s.kind, { visited: isVisited(s), current: s.n === current }]" :style="{ '--d': s.n }">
        <title>{{ s.tip }}</title>
        <template v-if="s.kind === 'transfer'">
          <circle :cx="s.x" :cy="s.y" r="15.5" :fill="isVisited(s) ? 'var(--ink)' : 'var(--bg)'" stroke="var(--ink)" stroke-width="3.5" />
          <text class="num big" :x="s.x" :y="s.y + 4" text-anchor="middle" :style="isVisited(s) ? { fill: 'var(--bg)' } : undefined">{{ pad(s.n) }}</text>
        </template>
        <template v-else-if="s.cap">
          <rect
            :x="s.x + Math.min(0, s.cap.dx) - 11" :y="s.y + Math.min(0, s.cap.dy) - 11"
            :width="22 + Math.abs(s.cap.dx)" :height="22 + Math.abs(s.cap.dy)" rx="11"
            :fill="isVisited(s) ? color[s.kind] : 'var(--bg)'" :stroke="color[s.kind]" stroke-width="3"
          />
          <text class="num" :x="s.x + s.cap.dx / 2" :y="s.y + s.cap.dy / 2 + 3.6" text-anchor="middle" :style="isVisited(s) ? { fill: 'var(--bg)' } : undefined">{{ pad(s.n) }}</text>
        </template>
        <template v-else>
          <circle :cx="s.x" :cy="s.y" r="11" :fill="isVisited(s) ? color[s.kind] : 'var(--bg)'" :stroke="color[s.kind]" stroke-width="3.5" />
          <text class="num" :x="s.x" :y="s.y + 3.6" text-anchor="middle" :style="isVisited(s) ? { fill: 'var(--bg)' } : undefined">{{ pad(s.n) }}</text>
        </template>
        <text class="ttl" :x="labelPos(s).x" :y="labelPos(s).y" :text-anchor="labelPos(s).anchor">{{ s.title }}</text>
        <text class="sub" :x="labelPos(s).x" :y="labelPos(s).y + 14.5" :text-anchor="labelPos(s).anchor">{{ s.sub }}</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.metro {
  width: 100%;
}
.legend text {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--ink-2);
}
.pause {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--muted);
  font-style: italic;
}
.plan {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--ink-2);
}
.num {
  font-family: var(--font-pixel);
  font-size: 10.5px;
  fill: var(--ink);
}
.num.big {
  font-size: 12.5px;
}
.ttl {
  font-family: var(--font-sans);
  font-size: 12.5px;
  font-weight: 650;
  fill: var(--ink);
}
.sub {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--ink-2);
  font-variant-numeric: tabular-nums;
}
.st.pre .sub,
.st.both .sub {
  fill: var(--muted);
}
.st.current .ttl {
  fill: var(--naruto);
}
.pin {
  font-family: var(--font-pixel);
  font-size: 10px;
  fill: var(--bg);
  letter-spacing: 0.06em;
}
.st {
  cursor: default;
}

/* reveal when the slide opens (never in export / print) */
.play .seg,
.play .st {
  animation: metro-in 0.45s ease both;
  animation-delay: calc(var(--d) * 70ms);
}
.play .here {
  animation: metro-in 0.4s ease both;
  animation-delay: 1.05s;
}
.play .glow {
  transform-box: fill-box;
  transform-origin: center;
  animation: metro-pulse 1.8s ease-in-out 1.4s infinite;
}
@keyframes metro-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@keyframes metro-pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.25);
  }
}
</style>
