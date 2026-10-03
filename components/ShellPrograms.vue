<script setup lang="ts">
import data from '../data/sessions.json'

// What the agents ran in the terminal: first program of every shell command, two panels.
const props = withDefaults(defineProps<{ top?: number }>(), { top: 11 })
const d = data as any
const reading = new Set(['sed', 'cat', 'rg', 'grep', 'tail', 'head', 'nl', 'ls', 'wc', 'awk', 'git diff', 'git status', 'git log', 'git show', 'pwd', 'find', 'stat'])
const panels = [
  { key: 'codex', title: 'Codex', total: d.codex.shell_commands, color: 'var(--s1)' },
  { key: 'claude', title: 'Claude Code', total: d.claude.shell_commands, color: 'var(--s2)' },
]
function rows(key: string) {
  const entries = Object.entries(d[key].shell_programs as Record<string, number>).slice(0, props.top)
  const max = entries[0][1]
  return entries.map(([name, n]) => ({ name, n, pct: n / max, read: reading.has(name) }))
}
function readShare(key: string) {
  const all = d[key].shell_programs as Record<string, number>
  const total = d[key].shell_commands as number
  const r = Object.entries(all).filter(([k]) => reading.has(k)).reduce((s, [, v]) => s + v, 0)
  return Math.round((r / total) * 100)
}
const fmt = new Intl.NumberFormat('ru-RU')
</script>

<template>
  <div class="grid2">
    <div v-for="p in panels" :key="p.key">
      <div class="head">
        <span class="t">{{ p.title }}</span>
        <span class="s">{{ fmt.format(p.total) }} команд · ≥ {{ readShare(p.key) }} % — чтение</span>
      </div>
      <div v-for="r in rows(p.key)" :key="r.name" class="row">
        <span class="nm mono" :class="{ read: r.read }">{{ r.name }}</span>
        <span class="tr"><i :style="{ width: `${Math.max(3, r.pct * 100)}%`, background: p.color, opacity: r.read ? 0.55 : 1 }" /></span>
        <span class="v">{{ fmt.format(r.n) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.grid2 {
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
  margin-bottom: 0.35rem;
}
.t {
  font-weight: 700;
  font-size: 0.82rem;
}
.s {
  font-size: 0.64rem;
  color: var(--muted);
}
.row {
  display: grid;
  grid-template-columns: 11rem 1fr 3rem;
  align-items: center;
  gap: 0.5rem;
  height: 1.12rem;
}
.nm {
  font-size: 0.62rem;
  color: var(--ink);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.nm.read {
  color: var(--ink-2);
}
.tr i {
  display: block;
  height: 8px;
  border-radius: 0 4px 4px 0;
}
.v {
  font-size: 0.64rem;
  color: var(--ink-2);
  text-align: right;
  font-variant-numeric: tabular-nums;
}
</style>
