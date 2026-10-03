<script setup lang="ts">
import { computed } from 'vue'
import tokens from '../data/tokens.json'

// Of every 1,000 processed tokens: re-read from cache, fresh input (incl. cache writes), written by the model.
const t = tokens as any
const agents = computed(() => {
  const c = t.codex
  const a = t.claude
  const mk = (name: string, sub: string, cache: number, fresh: number, out: number, total: number) => {
    const per = (v: number) => (v / total) * 1000
    const o = Math.round(per(out))
    const f = Math.round(per(fresh))
    return { name, sub, cache: 1000 - o - f, fresh: f, out: o, exact: { cache: per(cache), fresh: per(fresh), out: per(out) } }
  }
  return [
    mk('Codex · GPT-6 Astra', `${(c.processed / 1e9).toFixed(2).replace('.', ',')} млрд токенов, ${c.responses.toLocaleString('ru-RU')} ответов`, c.cached, c.fresh_input, c.output, c.processed),
    mk('Claude Opus 5.5', `${(a.processed / 1e9).toFixed(2).replace('.', ',')} млрд токенов, ${a.responses.toLocaleString('ru-RU')} ответов`, a.cache_read, a.fresh_input + a.cache_write, a.output, a.processed),
  ]
})
const cols = 50
function cells(ag: { cache: number, fresh: number, out: number }) {
  const out: string[] = []
  for (let i = 0; i < ag.out; i++) out.push('out')
  for (let i = 0; i < ag.fresh; i++) out.push('fresh')
  for (let i = 0; i < ag.cache; i++) out.push('cache')
  return out
}
const fmt1 = (v: number) => v.toFixed(1).replace('.', ',')
</script>

<template>
  <div class="wrap">
    <div v-for="ag in agents" :key="ag.name" class="agent">
      <div class="head">
        <span class="nm">{{ ag.name }}</span>
        <span class="sub">{{ ag.sub }}</span>
      </div>
      <svg :viewBox="`0 0 ${cols * 9} ${(1000 / cols) * 9}`" width="100%" role="img" :aria-label="`${ag.name}: структура 1000 токенов`">
        <rect
          v-for="(c, i) in cells(ag)" :key="i" :x="(i % cols) * 9" :y="Math.floor(i / cols) * 9" width="7" height="7" rx="1.5"
          :class="c"
        />
      </svg>
      <div class="nums">
        <span><i class="sw out" /><b>{{ fmt1(ag.exact.out) }}</b> пишет модель</span>
        <span><i class="sw fresh" /><b>{{ fmt1(ag.exact.fresh) }}</b> новый ввод{{ ag.name.startsWith('Claude') ? ' и запись в кэш' : '' }}</span>
        <span><i class="sw cache" /><b>{{ fmt1(ag.exact.cache) }}</b> перечитано из кэша</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wrap {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.6rem;
}
.head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1px solid var(--axis);
  padding-bottom: 0.25rem;
  margin-bottom: 0.4rem;
}
.nm {
  font-weight: 700;
  font-size: 0.82rem;
}
.sub {
  font-size: 0.64rem;
  color: var(--muted);
}
rect.cache { fill: #23406a; }
rect.fresh { fill: var(--s3); }
rect.out { fill: var(--s2); }
.nums {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  margin-top: 0.35rem;
  font-size: 0.68rem;
  color: var(--ink-2);
}
.nums b {
  color: var(--ink);
  margin-right: 0.25rem;
}
.sw {
  display: inline-block;
  width: 9px;
  height: 9px;
  border-radius: 2px;
  margin-right: 0.4rem;
  vertical-align: -1px;
}
.sw.cache { background: #23406a; }
.sw.fresh { background: var(--s3); }
.sw.out { background: var(--s2); }
</style>
