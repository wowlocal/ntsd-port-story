<script setup lang="ts">
// The seven outcome types a run may record (AGENTS.md, WORKFLOW.md) plus the rollback rule.
// One pixel icon and one line per tile; the longer wording lives in the slide notes.
// Icon classes are written literally so the UnoCSS extractor generates them.
const items = [
  { en: 'returned source case', ru: 'оригинал вернул результат', icon: 'i-pixelarticons-check', tone: 'good' },
  { en: 'source memory fault', ru: 'оригинал упал — это тоже поведение', icon: 'i-pixelarticons-zap', tone: 'serious' },
  { en: 'unsupported boundary', ru: 'сюда стенд не ходит', icon: 'i-pixelarticons-wall', tone: 'neutral' },
  { en: 'harness error', ru: 'сломался стенд, а не игра', icon: 'i-pixelarticons-tools', tone: 'warning' },
  { en: 'Native mismatch', ru: 'Swift разошёлся с оригиналом', icon: 'i-pixelarticons-copy-x', tone: 'critical' },
  { en: 'missing evidence', ru: 'улик нет — значит, неизвестно', icon: 'i-pixelarticons-circle-question', tone: 'neutral' },
  { en: 'safety refusal', ru: 'отказ модели — отдельный исход', icon: 'i-pixelarticons-shield', tone: 'neutral' },
  { en: 'rollback ≠ match', ru: 'откат при падении оригинала — <b>не</b> совпадение', icon: 'i-pixelarticons-undo', tone: 'rule' },
]
</script>

<template>
  <div class="outcomes">
    <div v-for="it in items" :key="it.en" class="tile" :class="it.tone">
      <div class="head">
        <span class="ico" :class="it.icon" />
        <span class="en mono">{{ it.en }}</span>
      </div>
      <div class="ru" v-html="it.ru" />
    </div>
  </div>
</template>

<style scoped>
.outcomes {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.6rem;
}
.tile {
  --tone: var(--ink-2);
  position: relative;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.85rem 0.9rem 0.9rem;
  overflow: hidden;
}
.tile::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--tone);
  opacity: 0.85;
}
.good { --tone: var(--good); }
.serious { --tone: var(--serious); }
.warning { --tone: var(--warning); }
.critical { --tone: var(--critical); }
.neutral { --tone: var(--muted); }
.rule {
  --tone: var(--naruto);
  border-color: rgba(255, 138, 61, 0.5);
  background: rgba(255, 138, 61, 0.06);
}
.head {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}
.ico {
  flex: none;
  width: 2rem;
  height: 2rem;
  color: var(--tone);
}
.neutral .ico {
  color: var(--ink-2);
}
.en {
  font-size: 0.74rem;
  font-weight: 700;
  line-height: 1.2;
  color: var(--ink);
}
.ru {
  font-size: 0.68rem;
  line-height: 1.35;
  color: var(--ink-2);
  margin-top: 0.5rem;
}
.ru :deep(b) {
  color: var(--ink);
}
</style>
