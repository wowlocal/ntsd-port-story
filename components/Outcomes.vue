<script setup lang="ts">
const items = [
  { en: 'returned source case', ru: 'оригинал отработал и вернул результат', icon: '✓', tone: 'good' },
  { en: 'source memory fault', ru: 'оригинал упал по памяти — это тоже поведение', icon: '⚡', tone: 'serious' },
  { en: 'unsupported boundary', ru: 'граница, за которую стенд не ходит', icon: '⊘', tone: 'neutral' },
  { en: 'harness error', ru: 'сломался сам стенд, а не игра', icon: '⚙', tone: 'warning' },
  { en: 'Native mismatch', ru: 'Swift разошёлся с оригиналом', icon: '≠', tone: 'critical' },
  { en: 'missing evidence', ru: 'улик нет — значит, не известно', icon: '?', tone: 'neutral' },
  { en: 'safety refusal', ru: 'отказ модели — фиксируется отдельно', icon: '■', tone: 'neutral' },
]
</script>

<template>
  <div class="grid">
    <div v-for="it in items" :key="it.en" class="cell" :class="it.tone">
      <span class="icon">{{ it.icon }}</span>
      <div>
        <div class="en mono">
          {{ it.en }}
        </div>
        <div class="ru">
          {{ it.ru }}
        </div>
      </div>
    </div>
    <div class="cell rule">
      <span class="icon">↺</span>
      <div>
        <div class="en mono">
          rollback ≠ match
        </div>
        <div class="ru">
          откат Native при падении оригинала — <b>не</b> совпадение
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.55rem;
}
.cell {
  display: flex;
  gap: 0.55rem;
  align-items: flex-start;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.6rem 0.65rem;
}
.icon {
  flex: none;
  width: 1.7rem;
  height: 1.7rem;
  display: grid;
  place-items: center;
  border-radius: 7px;
  font-weight: 800;
  font-size: 0.9rem;
  background: rgba(255, 255, 255, 0.07);
  color: var(--ink);
}
.good .icon { background: rgba(12, 163, 12, 0.22); color: #7ee07e; }
.serious .icon { background: rgba(236, 131, 90, 0.2); color: #f4a585; }
.warning .icon { background: rgba(250, 178, 25, 0.18); color: #fcd06f; }
.critical .icon { background: rgba(208, 59, 59, 0.24); color: #f19393; }
.rule {
  border-color: rgba(255, 138, 61, 0.5);
}
.rule .icon {
  background: rgba(255, 138, 61, 0.18);
  color: var(--naruto);
}
.en {
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--ink);
}
.ru {
  font-size: 0.66rem;
  color: var(--ink-2);
  line-height: 1.3;
  margin-top: 0.1rem;
}
</style>
