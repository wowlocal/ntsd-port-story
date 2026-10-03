<script setup lang="ts">
import { computed } from 'vue'
import cp from '../data/evidence/crossplay-matches.json'

interface M { suite: string, direction: string, seed: number, mode: string, background: string, difficulty: string, fighters: number, ticks: number, equal: boolean }
const matches = (cp as any).matches as M[]
const groups = computed(() => {
  const g: { key: string, title: string, items: M[] }[] = [
    { key: 'VS', title: 'VS, Mac → оригинал', items: [] },
    { key: 'Stage', title: 'Stage', items: [] },
    { key: 'War', title: 'War', items: [] },
    { key: 'orig', title: 'оригинал → Mac', items: [] },
  ]
  for (const mt of matches) {
    const key = mt.direction.startsWith('original') ? 'orig' : mt.mode
    ;(g.find(x => x.key === key) || g[0]).items.push(mt)
  }
  return g
})
const fmt = new Intl.NumberFormat('ru-RU')
const totals = (cp as any).totals
</script>

<template>
  <div>
    <div class="groups">
      <div v-for="g in groups" :key="g.key" class="grp">
        <div class="gt">
          {{ g.title }} <span class="muted">· {{ g.items.length }}</span>
        </div>
        <div class="tiles">
          <div v-for="(mt, i) in g.items" :key="i" class="tile" :class="{ bad: !mt.equal }">
            <span class="f">{{ mt.fighters }}</span>
            <span class="ok">{{ mt.equal ? '✓' : '≠' }}</span>
            <div class="tip">
              seed {{ mt.seed }} · {{ mt.mode }} · {{ mt.background }} · {{ mt.difficulty }} · {{ mt.fighters }} бойц. · {{ fmt.format(mt.ticks) }} тиков
            </div>
          </div>
        </div>
      </div>
      <div class="grp">
        <div class="gt">
          ранние повторы <span class="muted">· {{ totals.earlierReplayChecks }}</span>
        </div>
        <div class="tiles">
          <div v-for="i in totals.earlierReplayChecks" :key="i" class="tile early">
            <span class="ok">✓</span>
          </div>
        </div>
      </div>
    </div>
    <div class="cap">
      Число в плитке — сколько бойцов на арене. Все {{ totals.macToOriginalEqual + totals.originalToMacEqual }} случайных матчей равны;
      сверено {{ fmt.format(totals.ticksComparedSum) }} тиков, самый длинный матч — {{ fmt.format(totals.longestMatchTicks) }} тика.
    </div>
  </div>
</template>

<style scoped>
.groups {
  display: grid;
  grid-template-columns: 2.6fr 0.9fr 0.8fr 0.9fr 1.3fr;
  gap: 0.9rem;
}
.gt {
  font-size: 0.68rem;
  color: var(--ink-2);
  margin-bottom: 0.35rem;
  white-space: nowrap;
}
.tiles {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.tile {
  position: relative;
  width: 26px;
  height: 26px;
  border-radius: 6px;
  background: rgba(12, 163, 12, 0.18);
  border: 1px solid rgba(12, 163, 12, 0.55);
  display: grid;
  place-items: center;
}
.tile.early {
  background: rgba(12, 163, 12, 0.08);
  border-style: dashed;
}
.tile .f {
  position: absolute;
  left: 3px;
  top: 1px;
  font-size: 0.5rem;
  color: var(--ink-2);
  font-family: var(--font-mono);
}
.ok {
  color: #7ee07e;
  font-weight: 800;
  font-size: 0.8rem;
}
.tip {
  display: none;
  position: absolute;
  bottom: 120%;
  left: 50%;
  transform: translateX(-50%);
  background: var(--surface-3);
  border: 1px solid var(--hair);
  padding: 0.25rem 0.45rem;
  border-radius: 6px;
  font-size: 0.6rem;
  white-space: nowrap;
  z-index: 5;
  color: var(--ink);
}
.tile:hover .tip {
  display: block;
}
.cap {
  font-size: 0.66rem;
  color: var(--muted);
  margin-top: 0.6rem;
}
</style>
