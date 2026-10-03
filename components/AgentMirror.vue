<script setup lang="ts">
// Commit habits of the two agents as a butterfly chart: Codex grows to the left, Claude to the right.
// Units differ from row to row, so every row is scaled to the larger of the Codex and Claude values.
// The parallel Codex agent (1–3 October) is a thin bar under the Codex one and a number under the label.
// Values: data/summary.json → eras.pre / eras.claude / eras.parallel (commits, median_gap_min,
// night_share, with_body, conventional_prefix); «remain open»: commit bodies in git log, same eras.
interface Row { label: string, a: number, b: number, p: number, fa: string, fb: string, fp: string }
const rows: Row[] = [
  { label: 'коммитов', a: 327, b: 120, p: 16, fa: '327', fb: '120', fp: '16' },
  { label: 'медианный интервал', a: 27.7, b: 30.0, p: 19.3, fa: '27,7 мин', fb: '30,0 мин', fp: '19,3 мин' },
  { label: 'коммитов ночью, 00–06', a: 20, b: 22, p: 0, fa: '20 %', fb: '22 %', fp: '0 %' },
  { label: 'с телом сообщения', a: 34, b: 100, p: 69, fa: '34 %', fb: '100 %', fp: '69 %' },
  { label: 'префикс <span class="mono">feat:</span> и т. п.', a: 116, b: 0, p: 3, fa: '116', fb: '0', fp: '3' },
  { label: '«remain open» в теле', a: 72, b: 0, p: 6, fa: '72 из 327', fb: '0 из 120', fp: '6 из 16' },
]
const scaled = rows.map((r) => {
  const max = Math.max(r.a, r.b)
  return { ...r, ka: r.a / max, kb: r.b / max, kp: Math.min(1, r.p / max) }
})
// bar length = share of the track that is left after the room reserved for the value label
const len = (k: number) => `calc((100% - 4.2rem) * ${k.toFixed(4)})`
const plain = (s: string) => s.replace(/<[^>]+>/g, '')
</script>

<template>
  <div class="mirror">
    <div class="head">
      <div class="side left">
        <div><b>Codex · GPT-6 Astra</b><span>7–27 сентября</span></div><i class="sw" style="background: var(--s1)" />
      </div>
      <div />
      <div class="side right">
        <i class="sw" style="background: var(--s2)" /><div><b>Claude Opus 5.5</b><span>28 сентября — 3 октября</span></div>
      </div>
    </div>
    <div v-for="r in scaled" :key="r.label" class="row">
      <div class="track left">
        <div class="bar" :style="{ width: len(r.ka) }" :title="`Codex: ${plain(r.label)} — ${r.fa}`" />
        <span class="val" :style="{ right: `calc(${len(r.ka)} + 0.4rem)` }">{{ r.fa }}</span>
        <div v-if="r.p > 0" class="par" :style="{ width: len(r.kp) }" :title="`Codex параллельно: ${plain(r.label)} — ${r.fp}`" />
      </div>
      <div class="label">
        <span v-html="r.label" />
        <span class="pnote"><i class="pd" />{{ r.fp }}</span>
      </div>
      <div class="track right">
        <div class="bar" :style="{ width: len(r.kb) }" :title="`Claude: ${plain(r.label)} — ${r.fb}`" />
        <span class="val" :style="{ left: `calc(${len(r.kb)} + 0.4rem)` }">{{ r.fb }}</span>
      </div>
    </div>
    <div class="note">
      <span><i class="pd" />Codex параллельно, 1–3 октября: тонкая полоса и число под названием строки</span>
      <span>Единицы в строках разные, поэтому каждая строка нормирована к большему из значений Codex и Claude</span>
    </div>
  </div>
</template>

<style scoped>
.mirror {
  --track-gap: 0.55rem;
}
.head,
.row {
  display: grid;
  grid-template-columns: 1fr 9.6rem 1fr;
  column-gap: var(--track-gap);
}
.head {
  align-items: end;
  border-bottom: 1px solid var(--axis);
  padding-bottom: 0.3rem;
  margin-bottom: 0.35rem;
}
.side {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  line-height: 1.2;
  white-space: nowrap;
}
.side b,
.side span {
  display: block;
}
.side span {
  font-size: 0.64rem;
  color: var(--muted);
}
.side.left {
  justify-content: flex-end;
  text-align: right;
}
.sw {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 3px;
  align-self: center;
}
.row {
  height: 2.3rem;
  align-items: center;
}
.track {
  position: relative;
  height: 100%;
}
.track.left {
  border-right: 1px solid var(--axis);
}
.track.right {
  border-left: 1px solid var(--axis);
}
.bar {
  position: absolute;
  top: calc(50% - 5px);
  height: 10px;
}
.left .bar {
  right: 0;
  background: var(--s1);
  border-radius: 4px 0 0 4px;
}
.right .bar {
  left: 0;
  background: var(--s2);
  border-radius: 0 4px 4px 0;
}
.par {
  position: absolute;
  right: 0;
  top: calc(50% + 8px);
  height: 3px;
  background: var(--s3);
  border-radius: 2px 0 0 2px;
}
.val {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.76rem;
  font-weight: 600;
  color: var(--ink);
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}
.label {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  line-height: 1.15;
  font-size: 0.7rem;
  color: var(--ink-2);
}
.label :deep(.mono) {
  font-size: 0.92em;
  color: #ffd5b8;
}
.pnote {
  margin-top: 0.12rem;
  font-size: 0.58rem;
  color: var(--muted);
  white-space: nowrap;
}
.pd {
  display: inline-block;
  width: 12px;
  height: 3px;
  border-radius: 2px;
  background: var(--s3);
  margin-right: 0.3rem;
  vertical-align: 0.18em;
}
.note {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  margin-top: 0.45rem;
  font-size: 0.6rem;
  color: var(--muted);
}
</style>
