<script setup lang="ts">
interface Item { time: string, title: string, hash?: string, note?: string, hot?: boolean }
withDefaults(defineProps<{ items: Item[], dense?: boolean }>(), { dense: false })
</script>

<template>
  <ol class="tl" :class="{ dense }">
    <li v-for="(it, i) in items" :key="i" :class="{ hot: it.hot }">
      <span class="time mono">{{ it.time }}</span>
      <span class="node" />
      <div class="body">
        <div class="title">
          {{ it.title }}
          <span v-if="it.hash" class="tag">{{ it.hash }}</span>
        </div>
        <div v-if="it.note" class="note">
          {{ it.note }}
        </div>
      </div>
    </li>
  </ol>
</template>

<style scoped>
.tl {
  list-style: none;
  margin: 0;
  padding: 0;
  position: relative;
}
.tl::before {
  content: '';
  position: absolute;
  left: 4.35rem;
  top: 0.5rem;
  bottom: 0.5rem;
  width: 2px;
  background: linear-gradient(180deg, var(--axis), rgba(255, 138, 61, 0.6));
}
li {
  display: grid;
  grid-template-columns: 3.6rem 1.5rem 1fr;
  align-items: start;
  margin: 0 0 0.55rem;
}
.dense li {
  margin-bottom: 0.28rem;
}
.time {
  font-size: 0.72rem;
  color: var(--muted);
  text-align: right;
  padding-top: 0.12rem;
}
.node {
  width: 10px;
  height: 10px;
  margin: 0.32rem 0 0 0.52rem;
  background: var(--surface-3);
  border: 2px solid var(--axis);
}
.hot .node {
  background: var(--naruto);
  border-color: var(--naruto);
  box-shadow: 0 0 10px rgba(255, 138, 61, 0.6);
}
.title {
  font-size: 0.82rem;
  color: var(--ink);
  line-height: 1.3;
}
.dense .title {
  font-size: 0.76rem;
}
.hot .title {
  font-weight: 700;
}
.note {
  font-size: 0.68rem;
  color: var(--ink-2);
  line-height: 1.3;
  margin-top: 0.1rem;
}
.tag {
  margin-left: 0.3rem;
  font-size: 0.6rem;
}
</style>
