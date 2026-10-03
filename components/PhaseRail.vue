<script setup lang="ts">
// Phases of the cross-platform plan (docs/research/CROSS_PLATFORM.md) with their state at the time of the slide.
interface Phase { id: string, name: string, state: 'done' | 'part' | 'next' | 'ahead', note: string }
defineProps<{ phases: Phase[] }>()
const word = { done: 'готово', part: 'частично', next: 'следующее', ahead: 'впереди' }
</script>

<template>
  <div class="rail">
    <div v-for="p in phases" :key="p.id" class="ph" :class="p.state">
      <span class="id mono">{{ p.id }}</span>
      <i class="mark" :title="word[p.state]" />
      <div class="txt">
        <b>{{ p.name }}</b><span class="st">{{ word[p.state] }}</span>
        <div class="note">{{ p.note }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rail {
  display: flex;
  flex-direction: column;
  gap: 0.28rem;
}
.ph {
  display: grid;
  grid-template-columns: 1.7rem 0.9rem 1fr;
  align-items: start;
  gap: 0.35rem;
}
.id {
  font-size: 0.6rem;
  color: var(--muted);
  padding-top: 0.08rem;
}
.mark {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 0.22rem;
  border: 1.5px solid var(--axis);
}
.done .mark {
  background: var(--s3);
  border-color: var(--s3);
}
.part .mark {
  background: linear-gradient(90deg, var(--s4) 50%, transparent 50%);
  border-color: var(--s4);
}
.next .mark {
  border-color: var(--s1);
  box-shadow: 0 0 0 3px rgba(57, 135, 229, 0.25);
}
.txt b {
  font-size: 0.66rem;
  color: var(--ink);
  font-weight: 600;
}
.ahead .txt b {
  color: var(--ink-2);
  font-weight: 500;
}
.st {
  font-size: 0.56rem;
  color: var(--muted);
  margin-left: 0.4rem;
}
.note {
  font-size: 0.58rem;
  color: var(--ink-2);
  line-height: 1.3;
}
.ahead .note {
  color: var(--muted);
}
</style>
