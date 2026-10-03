<script setup lang="ts">
// A one-line chain of stages (mono name over a short note) joined by arrows; used for the path a DAT
// file takes through the EXE. `steps[i].t` may contain inline HTML such as <code>.
interface Step { t: string, s?: string, accent?: boolean }
defineProps<{ steps: Step[], label?: string }>()
</script>

<template>
  <div class="dpath">
    <div v-if="label" class="lab pixel">
      {{ label }}
    </div>
    <div class="row">
      <template v-for="(st, i) in steps" :key="i">
        <div class="st" :class="{ accent: st.accent }">
          <div class="t mono" v-html="st.t" />
          <div v-if="st.s" class="s">
            {{ st.s }}
          </div>
        </div>
        <svg v-if="i < steps.length - 1" class="arr" viewBox="0 0 16 16" width="14" height="14"><path d="M2 8h10M8 3l5 5-5 5" fill="none" stroke="var(--naruto)" stroke-width="2" stroke-linecap="square" /></svg>
      </template>
    </div>
  </div>
</template>

<style scoped>
.lab {
  font-size: 0.62rem;
  color: var(--naruto);
  letter-spacing: 0.04em;
  margin-bottom: 0.3rem;
}
.row {
  display: flex;
  align-items: stretch;
  gap: 0.45rem;
}
.st {
  flex: 1 1 auto;
  min-width: 0;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--hair);
  border-radius: 10px;
  padding: 0.35rem 0.6rem 0.4rem;
}
.st.accent {
  border-color: rgba(255, 138, 61, 0.45);
}
.t {
  font-size: 0.66rem;
  color: var(--ink);
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.s {
  font-size: 0.6rem;
  color: var(--muted);
  line-height: 1.3;
  margin-top: 0.1rem;
}
.arr {
  flex: none;
  align-self: center;
}
</style>
