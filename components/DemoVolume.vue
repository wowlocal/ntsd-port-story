<script setup lang="ts">
// Demo-day deck: how much code is the game and how much is the harness the agents wrote around it.
// One square = 1,000 lines (newlines in each file, blanks and comments included — the full deck's passport rule),
// counted at origin/main d7330e96 (19 Oct 2026) with git ls-tree + cat-file:
//   game — Swift in the shipped modules of native/Sources (NTSDCore, NTSDRuntime, NTSDApp, NTSDMacPlatform, NTSDSDL,
//   NTSDAndroid, NTSDiOS, NTSDWeb, NTSDFreeTypeText, NTSDMusicDecoder, NTSDReplayCodec) 47,471 + the browser host's
//   JS/HTML/CSS (tools/crossplatform/web) 1,549;
//   harness — Swift tests (native/Tests) 52,958; oracles (tools/oracle_*.py, 215 files) 37,088; check programs
//   (the *Check modules, NTSDReferenceChecks, NTSDHeadless) 12,171; other tools (the rest of the Python 51,315, shell 439,
//   JS 477) 52,231.
//   Not counted: vendored C (zlib 1.1.4, ALAC and the C shims, 9,632 lines).
//   Beside the code: docs/research 598 cards, 609,923 words; docs/evidence 1,055 files, 39.4 MB.
const game = [{ k: 'game', label: 'игра', lines: 49020, color: 'var(--naruto)' }]
const harness = [
  { k: 'tests', label: 'тесты', lines: 52958, color: 'var(--s1)' },
  { k: 'oracles', label: 'оракулы на коде оригинала', lines: 37088, color: 'var(--s7)' },
  { k: 'checks', label: 'сверочные программы', lines: 12171, color: 'var(--s3)' },
  { k: 'tools', label: 'прочие инструменты', lines: 52231, color: 'var(--axis)' },
]
const sum = (a: { lines: number }[]) => a.reduce((s, x) => s + x.lines, 0)
const squares = (a: { lines: number, color: string }[]) => a.flatMap(x => Array.from({ length: Math.round(x.lines / 1000) }, () => x.color))
const fmt = (n: number) => `${Math.round(n / 1000)} тыс.`
const ratio = (sum(harness) / sum(game)).toLocaleString('ru-RU', { maximumFractionDigits: 1 })
</script>

<template>
  <div class="vol">
    <div class="row">
      <div class="lb"><b>игра</b><span>{{ fmt(sum(game)) }} строк</span></div>
      <div class="sq"><i v-for="(c, i) in squares(game)" :key="i" :style="{ background: c }" /></div>
    </div>
    <div class="row">
      <div class="lb"><b>харнесс</b><span>{{ fmt(sum(harness)) }} строк · ×{{ ratio }}</span></div>
      <div class="sq"><i v-for="(c, i) in squares(harness)" :key="i" :style="{ background: c }" /></div>
    </div>
    <div class="lg">
      <span class="u">один квадрат — 1 000 строк</span>
      <span v-for="h in harness" :key="h.k"><i :style="{ background: h.color }" />{{ h.label }} {{ fmt(h.lines) }}</span>
      <span class="plus">и рядом — 598 карточек исследований (610 тыс. слов) и 1 055 файлов доказательств</span>
    </div>
  </div>
</template>

<style scoped>
.vol { display: flex; flex-direction: column; gap: .35rem; }
.row { display: grid; grid-template-columns: 7.6rem 1fr; gap: .7rem; align-items: center; }
.lb b { display: block; font-family: var(--font-display); font-size: .9rem; color: var(--ink); line-height: 1.1; }
.lb span { font-size: .62rem; color: var(--ink-2); }
.sq { display: grid; grid-template-rows: repeat(3, 9px); grid-auto-flow: column; grid-auto-columns: 9px; gap: 2px; }
.sq i { display: block; border-radius: 2px; }
.lg { display: flex; flex-wrap: wrap; gap: .15rem 1rem; margin-left: 8.3rem; font-size: .6rem; color: var(--ink-2); }
.lg i { display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: .3rem; vertical-align: -1px; }
.lg .u { color: var(--muted); }
.lg .plus { flex-basis: 100%; color: var(--muted); }
</style>
