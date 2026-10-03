<script setup lang="ts">
// Cards for dense slides: a pixel icon, a short title and one line. `icon` is a full UnoCSS icon class
// written literally in the slide (e.g. 'i-pixelarticons-bug') so the extractor generates it.
// `tag` is a small mono label (an address, a commit); `tone` picks the accent token for icon and edge.
interface Item { icon?: string, title: string, text?: string, tag?: string, tone?: string }
withDefaults(defineProps<{ items: Item[], cols?: number, compact?: boolean }>(), { cols: 3, compact: false })
const toneColor = (t?: string) => t ? `var(--${t})` : 'var(--naruto)'
</script>

<template>
  <div class="icards" :class="{ compact }" :style="{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }">
    <div v-for="it in items" :key="it.title" class="ic" :style="{ '--tone': toneColor(it.tone) }">
      <div class="head">
        <span v-if="it.icon" class="ico" :class="it.icon" />
        <b>{{ it.title }}</b>
      </div>
      <div v-if="it.text" class="txt" v-html="it.text" />
      <code v-if="it.tag" class="tg">{{ it.tag }}</code>
    </div>
  </div>
</template>

<style scoped>
.icards {
  display: grid;
  gap: 0.6rem;
}
.ic {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.65rem 0.8rem 0.7rem;
  overflow: hidden;
}
.ic::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--tone);
  opacity: 0.85;
}
.head {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.ico {
  flex: none;
  width: 1.45rem;
  height: 1.45rem;
  color: var(--tone);
}
.head b {
  font-size: 0.78rem;
  line-height: 1.2;
  color: var(--ink);
  font-weight: 650;
}
.txt {
  font-size: 0.66rem;
  line-height: 1.38;
  color: var(--ink-2);
  margin-top: 0.35rem;
}
.txt :deep(code) {
  font-size: 0.92em;
}
.tg {
  display: inline-block;
  margin-top: 0.4rem;
  font-size: 0.56rem;
  color: var(--muted);
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  padding: 0.05rem 0.35rem;
}
.compact .ic {
  padding: 0.5rem 0.7rem 0.55rem;
}
.compact .ico {
  width: 1.2rem;
  height: 1.2rem;
}
.compact .head b {
  font-size: 0.72rem;
}
.compact .txt {
  font-size: 0.62rem;
  margin-top: 0.25rem;
}
</style>
