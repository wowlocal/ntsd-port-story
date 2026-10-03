<script setup lang="ts">
// Forecasts of the remaining work against what actually happened, on one calendar axis.
// A forecast starts at the moment it was written (dot), runs dashed until the earliest named date
// and turns into a solid bar over the named range. Both estimate documents count their ranges from
// their own snapshot, so the end dates are derived: snapshot + the named number of weeks.
//   docs/estimates/2026-09-08-code-progress.md — snapshot c2c2c91, 8 Sep 22:39:01 (UTC+3)
//   docs/estimates/2026-09-27-code-progress.md — snapshot 166ddf7, 27 Sep 09:49:38 MSK
// Facts: 0a77527 (pages/06-turn.md), all modes on 29 Sep (07-game.md), 58 whole matches on 2–3 Oct
// (08-crosscheck.md), release v0.4.0 on 3 Oct, 16:46 (13-lessons.md). Pauses: data/summary.json.
import summary from '../data/summary.json'

const W = 900
const H = 266
const m = { l: 132, r: 12 }
const DAY = 864e5
const T0 = Date.parse('2026-09-01T00:00:00+03:00')
const T1 = Date.parse('2026-12-23T00:00:00+03:00')
const x = (t: number) => m.l + ((t - T0) / (T1 - T0)) * (W - m.l - m.r)
const at = (iso: string) => Date.parse(iso)

const rows = { a: 30, b1: 88, b2: 152 }
const factY0 = 184
const factStep = 17
const axisY = 248

const forecasts = [
  {
    y: rows.a, made: at('2026-09-08T22:39:01+03:00'), lo: 14, hi: 21,
    range: '≈ 2–3 недели → 22–29 сен', what: 'до конечного результата · ≈ 250 ч работы, осторожно ≈ 500 ч',
    title: 'Оценка 8 сентября, 22:39: «около 250 часов… осторожный сценарий — около 500»; в календаре «около двух недель, с резервным сценарием около трёх недель». Даты 22–29 сен посчитаны от дня оценки.',
    labelSide: 'right',
  },
  {
    y: rows.b1, made: at('2026-09-27T09:49:38+03:00'), lo: 7, hi: 21,
    range: '1–3 недели → 4–18 окт', what: 'до первого проверенного Наруто/Саске матча в приложении',
    title: 'Оценка 27 сентября, 09:49: «1–3 недели до первого проверенного Наруто/Саске матча в приложении». Даты 4–18 окт посчитаны от дня оценки.',
    labelSide: 'right',
  },
  {
    y: rows.b2, made: at('2026-09-27T09:49:38+03:00'), lo: 42, hi: 84,
    range: '6–12 недель → 8 ноя – 20 дек', what: 'до полного порта · срок ещё не наступил',
    title: 'Оценка 27 сентября, 09:49: «6–12 недель до полного порта». Даты 8 ноя – 20 дек посчитаны от дня оценки.',
    labelSide: 'above',
  },
].map(f => ({ ...f, x0: x(f.made), xLo: x(f.made + f.lo * DAY), xHi: x(f.made + f.hi * DAY) }))

const facts = [
  { t: at('2026-09-28T19:15:00+02:00'), date: '28 сен', text: 'матч Наруто/Саске в приложении до KO и Summary', note: '' },
  { t: at('2026-09-29T12:00:00+02:00'), date: '29 сен', text: 'все режимы', note: '' },
  { t: at('2026-10-02T00:00:00+02:00'), t2: at('2026-10-04T00:00:00+02:00'), date: '2–3 окт', text: '58 целых матчей сверены с оригиналом', note: '' },
  { t: at('2026-10-03T16:46:00+02:00'), date: '3 окт', text: 'релиз v0.4.0', note: ' · ещё не всё сверено с оригиналом' },
].map((f, i) => ({ ...f, y: factY0 + i * factStep, x: x(f.t), x2: f.t2 ? x(f.t2) : 0 }))
const factLabelX = x(at('2026-10-04T00:00:00+02:00')) + 12
const band = { x0: x(at('2026-09-28T00:00:00+02:00')), x1: x(at('2026-10-04T00:00:00+02:00')) }

// working pauses longer than two days (no commits at all)
const pauses = (summary as any).longest_pauses_h
  .filter((p: any) => p.hours > 48)
  .map((p: any) => ({ x0: x(at(p.from)), x1: x(at(p.to)), hours: p.hours, from: p.from.slice(0, 16), to: p.to.slice(0, 16) }))
const pauseLabelX = pauses.length ? (Math.min(...pauses.map((p: any) => p.x0)) + Math.max(...pauses.map((p: any) => p.x1))) / 2 : 0

const months = [
  { t: at('2026-09-01T00:00:00+03:00'), label: 'сентябрь' },
  { t: at('2026-10-01T00:00:00+03:00'), label: 'октябрь' },
  { t: at('2026-11-01T00:00:00+03:00'), label: 'ноябрь' },
  { t: at('2026-12-01T00:00:00+03:00'), label: 'декабрь' },
].map(mo => ({ ...mo, x: x(mo.t) }))
const diamond = (cx: number, cy: number, r: number) => `M${cx},${cy - r} L${cx + r},${cy} L${cx},${cy + r} L${cx - r},${cy} Z`
</script>

<template>
  <div>
    <div class="legend">
      <span>
        <svg width="40" height="10" aria-hidden="true">
          <circle cx="4.5" cy="5" r="3.5" fill="var(--s1)" />
          <line x1="9" x2="22" y1="5" y2="5" stroke="var(--s1)" stroke-width="1.5" stroke-dasharray="3 2.5" />
          <rect x="23" y="1" width="17" height="8" rx="2" fill="var(--s1)" />
        </svg>прогноз: день оценки → названный срок
      </span>
      <span><svg width="11" height="11" aria-hidden="true"><path :d="diamond(5.5, 5.5, 5)" fill="var(--s2)" /></svg>факт</span>
      <span><i class="pz" />пауза без коммитов</span>
      <span class="muted">концы диапазонов посчитаны: день оценки + срок</span>
    </div>
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Прогнозы срока и фактические даты на одной оси">
      <!-- calendar grid -->
      <line v-for="mo in months" :key="mo.t" :x1="mo.x" :x2="mo.x" y1="6" :y2="axisY" stroke="var(--grid)" />
      <text v-for="mo in months" :key="`l${mo.t}`" :x="mo.x + 5" :y="axisY + 14" class="tick">{{ mo.label }}</text>
      <line :x1="m.l" :x2="W - m.r" :y1="axisY" :y2="axisY" stroke="var(--axis)" />

      <!-- pauses and the fact window -->
      <rect v-for="p in pauses" :key="p.from" :x="p.x0" y="6" :width="p.x1 - p.x0" :height="axisY - 6" fill="rgba(255,255,255,0.035)">
        <title>пауза без коммитов: {{ p.from }} → {{ p.to }}, {{ String(p.hours).replace('.', ',') }} ч</title>
      </rect>
      <text v-if="pauses.length" :x="pauseLabelX" y="17" text-anchor="middle" class="pause">паузы</text>
      <rect :x="band.x0" y="6" :width="band.x1 - band.x0" :height="axisY - 6" fill="var(--s2)" style="opacity: 0.09" />

      <!-- row labels -->
      <text x="0" :y="rows.a - 2" class="when">8 сен, 22:39</text>
      <text x="0" :y="rows.a + 12" class="whensub">прогноз</text>
      <text x="0" :y="rows.b1 - 2" class="when">27 сен, 09:49</text>
      <text x="0" :y="rows.b1 + 12" class="whensub">прогноз</text>
      <text x="0" :y="rows.b1 + 30" class="whennote">метрика .text к этому</text>
      <text x="0" :y="rows.b1 + 41" class="whennote">дню две недели стояла</text>
      <text x="0" :y="rows.b1 + 52" class="whennote">на 52,87 %</text>
      <text x="0" :y="factY0 + 4" class="when">факт</text>

      <!-- forecasts -->
      <g v-for="f in forecasts" :key="f.y">
        <title>{{ f.title }}</title>
        <line :x1="f.x0" :x2="f.xLo" :y1="f.y" :y2="f.y" stroke="var(--s1)" stroke-width="1.5" stroke-dasharray="4 3" />
        <rect :x="f.xLo" :y="f.y - 5" :width="f.xHi - f.xLo" height="10" rx="3" fill="var(--s1)" />
        <circle :cx="f.x0" :cy="f.y" r="4.5" fill="var(--s1)" stroke="var(--bg)" stroke-width="2" />
        <template v-if="f.labelSide === 'right'">
          <text :x="f.xHi + 9" :y="f.y - 1" class="range">{{ f.range }}</text>
          <text :x="f.xHi + 9" :y="f.y + 12" class="what">{{ f.what }}</text>
        </template>
        <template v-else>
          <text :x="f.xHi" :y="f.y - 24" text-anchor="end" class="range">{{ f.range }}</text>
          <text :x="f.xHi" :y="f.y - 11" text-anchor="end" class="what">{{ f.what }}</text>
        </template>
      </g>

      <!-- facts -->
      <g v-for="f in facts" :key="f.date">
        <title>{{ f.date }} — {{ f.text }}{{ f.note }}</title>
        <line :x1="(f.x2 || f.x) + 7" :x2="factLabelX - 5" :y1="f.y" :y2="f.y" stroke="var(--muted)" stroke-width="1" stroke-dasharray="1 2.5" />
        <rect v-if="f.x2" :x="f.x" :y="f.y - 4" :width="f.x2 - f.x" height="8" rx="2.5" fill="var(--s2)" stroke="var(--bg)" stroke-width="1.5" />
        <path v-else :d="diamond(f.x, f.y, 5.5)" fill="var(--s2)" stroke="var(--bg)" stroke-width="1.5" />
        <text :x="factLabelX" :y="f.y + 4" class="fact"><tspan class="factdate">{{ f.date }}</tspan> — {{ f.text }}<tspan class="factnote">{{ f.note }}</tspan></text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.legend {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.3rem 1.1rem;
  font-size: 0.66rem;
  color: var(--ink-2);
  margin-bottom: 0.15rem;
}
.legend span {
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
}
.legend svg {
  flex: none;
  margin-right: 0.4rem;
}
.pz {
  display: inline-block;
  width: 14px;
  height: 10px;
  margin-right: 0.4rem;
  vertical-align: -1px;
  background: rgba(255, 255, 255, 0.09);
  border-radius: 2px;
}
.tick {
  font-size: 10.5px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.pause {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.when {
  font-family: var(--font-pixel);
  font-size: 12px;
  fill: var(--naruto);
  letter-spacing: 0.02em;
}
.whensub {
  font-size: 10.5px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.whennote {
  font-size: 9.5px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
.range {
  font-size: 12px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
}
.what {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.fact {
  font-size: 11px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.factdate {
  font-weight: 650;
  fill: var(--ink);
}
.factnote {
  fill: var(--muted);
}
</style>
