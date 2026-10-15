<script setup lang="ts">
// Where the Galaxy A12's game thread spent the load before the loop: simpleperf with DWARF stacks, 12,308 game-thread
// samples over the load, inclusive shares (MEMORY_LOADING.md, Baseline). The darker part of the package segment is
// the portable SHA-256 inside it. One 100 % bar.
// Data: data/loading_steps.json (baseline.profileA12; scripts/collect_loading.py, from ml-baseline-20261010.json).
import data from '../data/loading_steps.json'

const p = (data as any).baseline.profileA12
const cat = p['catalog session load'] as number
const pkg = p['catalog package load'] as number
const sha = p.PortableSHA256 as number
const arena = p['arena package'] as number
const rest = 100 - cat - pkg - arena
const W = 884
const x = (v: number) => (v / 100) * W
const f = (v: number) => `${Math.round(v)} %`
</script>

<template>
  <svg :viewBox="`0 0 ${W} 46`" width="100%" role="img" :aria-label="`Профиль загрузки до цикла: каталог ${f(cat)}, пакет ${f(pkg)}, из них SHA-256 ${f(sha)}`">
    <rect x="0" y="4" :width="x(cat) - 2" height="24" rx="3" fill="var(--s2)" />
    <text x="8" y="20.5" class="in">разбор каталога: объекты, DAT, тела кадров — {{ f(cat) }}</text>
    <rect :x="x(cat)" y="4" :width="x(pkg) - 2" height="24" rx="3" fill="var(--s1)" />
    <rect :x="x(cat)" y="4" :width="x(sha)" height="24" rx="3" fill="#1f5aa6" />
    <text :x="x(cat) + 6" y="20.5" class="in">SHA-256 {{ f(sha) }}</text>
    <text :x="x(cat + pkg) - 6" y="20.5" text-anchor="end" class="in">пакет {{ f(pkg) }}</text>
    <rect :x="x(cat + pkg)" y="4" :width="x(arena) - 2" height="24" rx="2" fill="#5d6679" />
    <rect :x="x(cat + pkg + arena)" y="4" :width="x(rest)" height="24" rx="3" fill="#2a3142" />
    <text :x="W - 8" y="20.5" text-anchor="end" class="in dim">прочее {{ f(rest) }}</text>
    <text x="0" y="43" class="cap">главный поток A12 во время загрузки до цикла, доли сэмплов simpleperf (12 308), включительно · серый узкий — пакет арен {{ String(arena).replace('.', ',') }} %</text>
  </svg>
</template>

<style scoped>
.in {
  font-size: 11px;
  font-weight: 600;
  fill: #fff;
  font-family: var(--font-sans);
}
.in.dim {
  fill: var(--ink-2);
  font-weight: 500;
}
.cap {
  font-size: 10px;
  fill: var(--muted);
  font-family: var(--font-sans);
}
</style>
