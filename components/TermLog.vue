<script setup lang="ts">
interface Line { t: string, h: string, s: string, hot?: boolean }
withDefaults(defineProps<{ title?: string, lines: Line[], night?: boolean }>(), { title: 'git log', night: false })
</script>

<template>
  <div class="term">
    <div class="bar">
      <i class="dot r" /><i class="dot y" /><i class="dot g" />
      <span class="title mono">{{ title }}</span>
    </div>
    <div class="body" :class="{ night }">
      <div v-for="(l, i) in lines" :key="i" class="ln mono" :class="{ hot: l.hot }">
        <span class="t">{{ l.t }}</span>
        <span class="h">{{ l.h }}</span>
        <span class="s">{{ l.s }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.term {
  background: #0c1017;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 14px 30px rgba(0, 0, 0, 0.4);
}
.bar {
  height: 22px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 9px;
  background: #161b25;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}
.r { background: #ff5f57; }
.y { background: #febc2e; }
.g { background: #28c840; }
.title {
  flex: 1;
  text-align: center;
  font-size: 0.6rem;
  color: var(--muted);
  margin-right: 34px;
}
.body {
  padding: 0.45rem 0.7rem 0.55rem;
  position: relative;
}
.body.night {
  background: linear-gradient(180deg, rgba(57, 135, 229, 0.08), rgba(57, 135, 229, 0.02) 60%, rgba(255, 138, 61, 0.1));
}
.ln {
  display: grid;
  grid-template-columns: 2.7rem 3.8rem 1fr;
  gap: 0.4rem;
  font-size: 0.64rem;
  line-height: 1.55;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.t {
  color: var(--muted);
}
.h {
  color: #febc2e;
}
.s {
  color: var(--ink-2);
  overflow: hidden;
  text-overflow: ellipsis;
}
.hot .s {
  color: var(--ink);
  font-weight: 700;
}
</style>
