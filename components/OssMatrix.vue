<script setup lang="ts">
import data from '../data/oss_matrix.json'

// What each open-source LF2 engine implements, by reading its code (data/evidence/lf2-oss-engines.json).
// Shape carries the value: filled — yes, half — partial, dot — no, "?" — unknown.
interface Row { name: string, repo?: string, lang: string, loc: number, stars: number | null, last: string, since?: string, cells: Record<string, string> }
const rows = (data as any).rows as Row[]
const newcomers = ((data as any).newcomers ?? []) as Row[]
const port = (data as any).port as Row
const cols = (data as any).columns as string[]
const head: Record<string, [string, string?]> = {
  readsOriginalDat: ['DAT', 'оригинала'],
  frameStateMachine: ['кадры', 'wait/next'],
  combatBoxes: ['бой', 'itr/bdy'],
  physics: ['физика'],
  computerAI: ['ИИ'],
  modesBeyondVS: ['режимы', 'кроме VS'],
  replays: ['записи'],
  network: ['сеть'],
  automatedTests: ['авто-', 'тесты'],
  comparesWithOriginal: ['сверка', 'с EXE'],
  nativeMacOS: ['macOS', 'нативно'],
}
const word: Record<string, string> = { y: 'есть', p: 'частично', n: 'нет', u: 'неизвестно' }
const months = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
const when = (ym: string) => `${months[Number(ym.slice(5, 7)) - 1]} ${ym.slice(0, 4)}`
const day = (ymd: string) => `${Number(ymd.slice(8, 10))} ${months[Number(ymd.slice(5, 7)) - 1]}`
const kloc = (n: number) => n >= 1000 ? `${(n / 1000).toFixed(1).replace('.', ',')} тыс.` : `${n}`
</script>

<template>
  <div class="matrix" :style="{ '--cols': cols.length }">
    <div class="row head">
      <div class="nm">проект</div>
      <div class="meta">★</div>
      <div class="meta">последний коммит</div>
      <div v-for="c in cols" :key="c" class="h">
        {{ head[c][0] }}<br v-if="head[c][1]"><span v-if="head[c][1]">{{ head[c][1] }}</span>
      </div>
    </div>
    <div v-for="r in [...rows, ...newcomers, port]" :key="r.name" class="row" :class="{ port: r === port, fresh: newcomers.includes(r) }">
      <div class="nm">
        <b>{{ r.name }}</b><span v-if="r.since" class="tag">с {{ day(r.since) }}</span><span class="sub">{{ r.lang }} · {{ kloc(r.loc) }} строк</span>
      </div>
      <div class="meta num">{{ r.stars ?? '—' }}</div>
      <div class="meta">{{ when(r.last) }}</div>
      <div v-for="c in cols" :key="c" class="cell" :title="`${r.name}: ${head[c][0]} ${head[c][1] ?? ''} — ${word[r.cells[c]]}`">
        <i v-if="r.cells[c] === 'y'" class="g y" />
        <i v-else-if="r.cells[c] === 'p'" class="g p" />
        <span v-else-if="r.cells[c] === 'u'" class="q">?</span>
        <i v-else class="g n" />
      </div>
    </div>
    <div class="legend">
      <span><i class="g y" />есть</span>
      <span><i class="g p" />частично</span>
      <span><i class="g n" />нет</span>
      <span><span class="q">?</span>не установлено</span>
      <span class="muted">· «строк» — собственный код без тестов и сторонних библиотек</span>
    </div>
  </div>
</template>

<style scoped>
.matrix {
  font-size: 0.6rem;
  color: var(--ink-2);
}
.row {
  display: grid;
  grid-template-columns: 12.4rem 2.2rem 5.4rem repeat(var(--cols), 1fr);
  align-items: center;
  min-height: 1.13rem;
  border-bottom: 1px solid var(--grid);
}
.row:not(.head):not(.port):nth-child(odd) {
  background: rgba(255, 255, 255, 0.018);
}
.head {
  border-bottom: 1px solid var(--axis);
  color: var(--muted);
  line-height: 1.15;
  padding-bottom: 0.2rem;
}
.head .h {
  text-align: center;
  font-size: 0.56rem;
}
.head .h span {
  color: var(--muted);
  opacity: 0.8;
}
.nm {
  padding-left: 0.35rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.nm b {
  color: var(--ink);
  font-weight: 600;
  margin-right: 0.45rem;
}
.nm .sub {
  color: var(--muted);
  font-size: 0.56rem;
}
.meta {
  text-align: right;
  padding-right: 0.6rem;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
.head .meta {
  font-size: 0.56rem;
}
.cell {
  display: flex;
  justify-content: center;
}
.g {
  display: inline-block;
  width: 9px;
  height: 9px;
  border-radius: 50%;
}
.g.y {
  background: var(--ink-2);
}
.g.p {
  border: 1.5px solid var(--ink-2);
  background: linear-gradient(90deg, var(--ink-2) 50%, transparent 50%);
}
.g.n {
  width: 4px;
  height: 4px;
  background: var(--axis);
}
.q {
  color: var(--muted);
  font-weight: 600;
}
.fresh {
  border-top: 1px dashed var(--muted);
  background: rgba(108, 182, 255, 0.06);
}
.tag {
  font-size: 0.5rem;
  color: var(--chakra);
  border: 1px solid rgba(108, 182, 255, 0.45);
  border-radius: 999px;
  padding: 0 0.35rem;
  margin-right: 0.4rem;
}
.port {
  border-top: 1.5px solid var(--naruto);
  border-bottom: none;
  background: rgba(255, 138, 61, 0.08);
  margin-top: 0.2rem;
  min-height: 1.4rem;
}
.port .nm b {
  color: var(--naruto);
}
.port .g.y {
  background: var(--naruto);
}
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.2rem 1rem;
  margin-top: 0.35rem;
  font-size: 0.58rem;
}
.legend span {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
</style>
