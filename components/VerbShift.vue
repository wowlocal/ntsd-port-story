<script setup lang="ts">
import verbs from '../data/verbs.json'

const props = withDefaults(defineProps<{ top?: number }>(), { top: 9 })

const panels = [
  { key: 'pre', title: '7–27 сентября', sub: '327 коммитов', color: 'var(--s1)' },
  { key: 'claude', title: '28 сентября — 3 октября', sub: '120 коммитов с Claude', color: 'var(--s2)' },
] as const

const ru: Record<string, string> = {
  verify: 'проверить',
  reproduce: 'воспроизвести',
  preserve: 'сохранить',
  recover: 'восстановить',
  add: 'добавить',
  port: 'портировать',
  continue: 'продолжить',
  compose: 'скомпоновать',
  validate: 'валидировать',
  record: 'записать',
  join: 'соединить',
  retain: 'удержать',
  'cross-check': 'сверить',
  play: 'сыграть',
  keep: 'сохранять',
  open: 'открыть',
  plan: 'спланировать',
  read: 'прочитать',
  run: 'запустить',
  drive: 'провести',
  stop: 'остановить',
}

function rows(key: 'pre' | 'claude') {
  const list = (verbs as any)[key].slice(0, props.top) as [string, number][]
  const max = list[0][1]
  return list.map(([w, n]) => ({ w, n, pct: n / max }))
}
</script>

<template>
  <div class="grid">
    <div v-for="p in panels" :key="p.key" class="panel">
      <div class="head">
        <span class="title">{{ p.title }}</span>
        <span class="sub">{{ p.sub }}</span>
      </div>
      <div v-for="r in rows(p.key)" :key="r.w" class="row">
        <div class="word">
          <span class="en mono">{{ r.w }}</span>
          <span class="ru">{{ ru[r.w] || '' }}</span>
        </div>
        <div class="track">
          <div class="bar" :style="{ width: `${Math.max(4, r.pct * 100)}%`, background: p.color }" />
          <span class="n">{{ r.n }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.6rem;
}
.head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  border-bottom: 1px solid var(--axis);
  padding-bottom: 0.3rem;
  margin-bottom: 0.4rem;
}
.title {
  font-weight: 700;
  font-size: 0.86rem;
}
.sub {
  font-size: 0.7rem;
  color: var(--muted);
}
.row {
  display: grid;
  grid-template-columns: 9.2rem 1fr;
  align-items: center;
  gap: 0.6rem;
  height: 1.62rem;
}
.word {
  display: flex;
  flex-direction: column;
  line-height: 1.05;
}
.en {
  font-size: 0.74rem;
  color: var(--ink);
}
.ru {
  font-size: 0.6rem;
  color: var(--muted);
}
.track {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.bar {
  height: 10px;
  border-radius: 0 4px 4px 0;
}
.n {
  font-size: 0.7rem;
  color: var(--ink-2);
  font-variant-numeric: tabular-nums;
}
</style>
