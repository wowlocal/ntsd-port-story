<script setup lang="ts">
// docs/research/APPLICATION_HOST_LOADING_{VALIDATION,CORRECTION1,COMPLETION,CORRECTION3,REGRESSIONS}.md
// One row per run of the same frozen 42-method selection, 2026-09-22.
type S = 'pass' | 'fail' | 'guard' | 'timeout' | 'carried' | 'idle'
const N = 42
function row(spec: [number, number, S][]): S[] {
  const r: S[] = Array.from({ length: N }, () => 'idle')
  for (const [a, b, s] of spec) {
    for (let i = a; i <= b; i++)
      r[i - 1] = s
  }
  return r
}
const runs = [
  { time: '18:57', name: 'VALIDATION', hash: '03afa4e', note: '25 ✓ · №26: две assertion · 16 не запускались', cells: row([[1, 25, 'pass'], [26, 26, 'fail']]) },
  { time: '19:18', name: 'CORRECTION 1', hash: '90fd80c', note: 'исправлен только тест · №28 упёрся в гард 8 GiB RSS', cells: row([[1, 27, 'pass'], [28, 28, 'guard']]) },
  { time: '19:35', name: 'COMPLETION', hash: '69f7a82', note: '№28 с лимитом 12 GiB — таймаут 600 с; сэмпл стека: рекурсивная печать в XCTAssertNotNil', cells: row([[1, 27, 'carried'], [28, 28, 'timeout']]) },
  { time: '20:00', name: 'CORRECTION 3', hash: '93df1dd', note: 'XCTAssertNotNil(x) → XCTAssertTrue(x != nil) · 34 ✓ · №35 — гард', cells: row([[1, 34, 'pass'], [35, 35, 'guard']]) },
  { time: '20:09', name: 'REGRESSIONS', hash: 'c656621', note: 'тот же бинарник: 34 сохранённых + 8 новых = 42 из 42', cells: row([[1, 34, 'carried'], [35, 42, 'pass']]) },
]
const legend: { s: S, label: string }[] = [
  { s: 'pass', label: 'прошёл в этом прогоне' },
  { s: 'carried', label: 'зачтён из прошлого прогона' },
  { s: 'fail', label: 'assertion' },
  { s: 'guard', label: 'гард памяти' },
  { s: 'timeout', label: 'таймаут' },
  { s: 'idle', label: 'не запускался' },
]
</script>

<template>
  <div class="strip">
    <div v-for="r in runs" :key="r.name" class="run">
      <div class="meta">
        <span class="time mono">{{ r.time }}</span>
        <span class="name mono">{{ r.name }}</span>
      </div>
      <div class="cells">
        <i v-for="(c, i) in r.cells" :key="i" :class="c" :title="`метод ${i + 1}: ${c}`" />
      </div>
      <div class="note">
        {{ r.note }} <span class="tag">{{ r.hash }}</span>
      </div>
    </div>
    <div class="legend">
      <span v-for="l in legend" :key="l.s"><i :class="l.s" />{{ l.label }}</span>
    </div>
  </div>
</template>

<style scoped>
.run {
  display: grid;
  grid-template-columns: 8.4rem 1fr;
  grid-template-rows: auto auto;
  column-gap: 0.8rem;
  margin-bottom: 0.5rem;
}
.meta {
  grid-row: 1 / 3;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.time {
  font-size: 0.66rem;
  color: var(--muted);
}
.name {
  font-size: 0.74rem;
  font-weight: 700;
  color: var(--ink);
}
.cells {
  display: grid;
  grid-template-columns: repeat(42, 1fr);
  gap: 2px;
}
.cells i,
.legend i {
  display: block;
  height: 14px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.05);
}
i.pass { background: var(--good); }
i.carried { background: rgba(12, 163, 12, 0.35); }
i.fail { background: var(--critical); }
i.guard { background: var(--warning); }
i.timeout { background: var(--serious); }
i.idle { background: rgba(255, 255, 255, 0.05); outline: 1px solid rgba(255, 255, 255, 0.06); outline-offset: -1px; }
.note {
  font-size: 0.64rem;
  color: var(--ink-2);
  margin-top: 0.18rem;
}
.note .tag {
  font-size: 0.56rem;
  margin-left: 0.3rem;
}
.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 1rem;
  font-size: 0.64rem;
  color: var(--ink-2);
  margin-top: 0.4rem;
  padding-left: 9.2rem;
}
.legend span {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.legend i {
  width: 14px;
  height: 10px;
}
</style>
