<script setup lang="ts">
import data from '../data/xplat.json'

// The project passport of chapter 10 (3 Oct 16:18, fc959db) against 7 Oct 08:23 (8840eb3), same definitions
// (scripts/collect_xplat.py). Each tile: the new value, the old one, and a bar where the muted part is
// what was there on 3 October and the accent part is what the four days added (or, for memory, kept).
const a = (data as any).passport.before
const b = (data as any).passport.after
interface Tile { label: string, before: number, after: number, show?: string, was?: string, unit?: string, down?: boolean, note?: string }
const tiles: Tile[] = [
  { label: 'коммитов с 7 сентября', before: a.commits_since_sept, after: b.commits_since_sept },
  { label: 'активных дней', before: a.active_days, after: b.active_days, note: `из ${Math.round((Date.parse(b.last_day) - Date.parse(b.first_day)) / 864e5) + 1} календарных` },
  { label: 'строк Swift в самой игре', before: a.swift_src_lines, after: b.swift_src_lines },
  { label: 'тестовых функций', before: a.test_functions, after: b.test_functions },
  { label: 'evidence-файлов', before: a.evidence_files, after: b.evidence_files },
  { label: 'хостов, равных эталону', before: 1, after: 9, note: 'macOS → Linux, Windows, iPad, Android' },
  { label: 'сценариев, равных эталону', before: 9, after: 90, note: 'на main запись падала и на Mac' },
  { label: 'куча матча, ГБ', before: 3.9, after: 1.5, show: '1,5', was: '3,9', down: true, note: 'та же игра, те же кадры' },
  { label: 'Galaxy A12, тиков в секунду', before: 0, after: 30.25, show: '30,25', was: 'убита на загрузке', note: 'темп оригинала — 30' },
  { label: 'реплик человека за 84 часа', before: 0, after: 23, was: '—', note: '65 запусков /loop, 137 коммитов' },
]
const fmt = (n: number) => n.toLocaleString('ru-RU')
const pct = (t: Tile) => {
  const max = Math.max(t.before, t.after)
  return { base: (Math.min(t.before, t.after) / max) * 100, rest: (Math.abs(t.after - t.before) / max) * 100 }
}
const delta = (t: Tile) => {
  if (t.was || t.down)
    return ''
  const d = t.after - t.before
  return `+${fmt(d)}`
}
</script>

<template>
  <div class="pp">
    <div v-for="t in tiles" :key="t.label" class="tile" :class="{ down: t.down }">
      <div class="lab">{{ t.label }}</div>
      <div class="val">
        <b>{{ t.show ?? fmt(t.after) }}</b>
        <span v-if="delta(t)" class="d">{{ delta(t) }}</span>
      </div>
      <div class="bar">
        <template v-if="t.down">
          <i class="acc" :style="{ width: `${pct(t).base}%` }" /><i class="freed" :style="{ width: `${pct(t).rest}%` }" />
        </template>
        <template v-else>
          <i class="old" :style="{ width: `${pct(t).base}%` }" /><i class="acc" :style="{ width: `${pct(t).rest}%` }" />
        </template>
      </div>
      <div class="was">3 окт: {{ t.was ?? fmt(t.before) }}<template v-if="t.note"> · {{ t.note }}</template></div>
    </div>
  </div>
</template>

<style scoped>
.pp {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.85rem;
}
.tile {
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.85rem 0.85rem 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.lab {
  font-size: 0.66rem;
  color: var(--ink-2);
  line-height: 1.25;
  min-height: 2.5em;
}
.val {
  display: flex;
  align-items: baseline;
  gap: 0.4rem;
}
.val b {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--ink);
  line-height: 1.1;
}
.val .d {
  font-size: 0.68rem;
  font-weight: 650;
  color: var(--ink-2);
}
.bar {
  display: flex;
  gap: 2px;
  height: 6px;
  margin: 0.25rem 0 0.15rem;
}
.bar i {
  display: block;
  height: 6px;
  border-radius: 2px;
}
.bar .old {
  background: var(--surface-3);
}
.bar .acc {
  background: var(--s2);
}
.down .bar .acc {
  background: var(--s3);
}
.bar .freed {
  background: repeating-linear-gradient(135deg, rgba(255, 255, 255, 0.14) 0 2px, transparent 2px 5px);
  border: 1px solid var(--axis);
  height: 6px;
  box-sizing: border-box;
}
.was {
  font-size: 0.6rem;
  color: var(--muted);
  line-height: 1.3;
}
</style>
