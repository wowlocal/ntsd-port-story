<script setup lang="ts">
defineProps<{ title: string, addr?: string, commit?: string, icon?: string }>()
</script>

<template>
  <div class="quirk">
    <div class="top">
      <span v-if="icon" class="icon">{{ icon }}</span>
      <span class="title">{{ title }}</span>
    </div>
    <div class="text">
      <slot />
    </div>
    <div v-if="addr || commit" class="foot">
      <span v-if="addr" class="tag">{{ addr }}</span>
      <span v-if="commit" class="tag">{{ commit }}</span>
    </div>
  </div>
</template>

<style scoped>
.quirk {
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.7rem 0.85rem 0.65rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  height: 100%;
}
.top {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}
.icon {
  font-size: 1.05rem;
}
.title {
  font-weight: 700;
  font-size: 0.86rem;
  line-height: 1.2;
  color: var(--ink);
}
.text {
  font-size: 0.72rem;
  color: var(--ink-2);
  line-height: 1.38;
  flex: 1;
}
.text :deep(code) {
  font-size: 0.66rem;
}
.foot {
  display: flex;
  gap: 0.3rem;
  flex-wrap: wrap;
}
.tag {
  font-size: 0.58rem;
}
</style>
