<script setup lang="ts">
// The four separate acceptance gates (AGENTS.md: "Treat source/audit publication, Native tests,
// package byte verification and archive verification as separate gates. Process exit 0 alone is
// not acceptance."). Separate cells, no arrows: the gates are independent, not a sequence.
const gates = [
  { ru: 'эталон и аудит опубликованы', en: 'source / audit publication', icon: 'i-pixelarticons-upload' },
  { ru: 'тесты Native', en: 'сравнение с expected и масками', icon: 'i-pixelarticons-test-tube' },
  { ru: 'байты пакета', en: 'package byte verification', icon: 'i-pixelarticons-package' },
  { ru: 'архив проверен', en: 'archive verification', icon: 'i-pixelarticons-archive' },
]
</script>

<template>
  <div>
    <div class="caprow">
      <span class="cap">четыре отдельных гейта приёмки — каждый записывается один раз для закреплённых байтов</span>
      <span class="not"><span class="i-pixelarticons-terminal" /><s class="mono">exit 0</s> — не приёмка</span>
    </div>
    <div class="strip">
      <div v-for="(g, i) in gates" :key="g.ru" class="gate">
        <span class="badge">
          <span class="ico" :class="g.icon" />
          <span class="num pixel">{{ i + 1 }}</span>
        </span>
        <div class="txt">
          <b>{{ g.ru }}</b>
          <span class="en">{{ g.en }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.caprow {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.45rem;
}
.cap {
  font-size: 0.68rem;
  color: var(--muted);
}
.not {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  flex: none;
  font-size: 0.66rem;
  color: var(--ink-2);
  border: 1px dashed var(--axis);
  border-radius: 999px;
  padding: 0.12rem 0.6rem 0.12rem 0.45rem;
}
.not > span {
  width: 1rem;
  height: 1rem;
  color: var(--muted);
}
.not s {
  color: var(--ink);
  text-decoration-color: var(--muted);
}
.strip {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.6rem;
}
.gate {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--hair);
  border-radius: 10px;
  padding: 0.6rem 0.75rem;
}
.badge {
  position: relative;
  flex: none;
  width: 2.1rem;
  height: 2.1rem;
  display: grid;
  place-items: center;
  background: rgba(255, 138, 61, 0.1);
  border-radius: 8px;
}
.ico {
  width: 1.4rem;
  height: 1.4rem;
  color: var(--naruto);
}
.num {
  position: absolute;
  left: -0.35rem;
  top: -0.35rem;
  width: 0.95rem;
  height: 0.95rem;
  display: grid;
  place-items: center;
  font-size: 0.6rem;
  line-height: 1;
  color: var(--bg);
  background: var(--naruto);
  border-radius: 3px;
}
.txt {
  display: flex;
  flex-direction: column;
  min-width: 0;
  line-height: 1.25;
}
.txt b {
  font-size: 0.72rem;
  font-weight: 650;
  color: var(--ink);
}
.en {
  font-size: 0.6rem;
  color: var(--muted);
  margin-top: 0.1rem;
}
</style>
