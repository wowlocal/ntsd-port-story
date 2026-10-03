<script setup lang="ts">
// The original's frame timer, in instruction order (docs/ORIGINAL_ENGINE.md, "Timer branch"):
// a tick needs strictly more than 33 ms since the baseline, lateness is capped at 100 ms,
// and the baseline advances by 33 ms, not to "now". Hence 1000 / 33 ≈ 30.3 ticks per second.
const steps = [
  { addr: '0x43d160', text: 'прошло <b>строго больше 33&nbsp;мс</b>' },
  { addr: '0x43d169', text: 'отставание режется до 100&nbsp;мс' },
  { addr: '0x43d17f', text: 'база сдвигается на 33&nbsp;мс' },
]
</script>

<template>
  <div class="timer">
    <div class="lead">
      <span class="ico i-pixelarticons-clock" />
      <b>Таймер оригинала</b>
    </div>
    <div class="chain">
      <template v-for="(s, i) in steps" :key="s.addr">
        <div class="st">
          <code>{{ s.addr }}</code>
          <span v-html="s.text" />
        </div>
        <span v-if="i < steps.length - 1" class="arr i-pixelarticons-arrow-right" />
      </template>
    </div>
    <div class="res">
      <span class="eq">1000 / 33 ≈</span>
      <b>30,3</b>
      <span class="u">тика/с, а не ровно 30</span>
    </div>
  </div>
</template>

<style scoped>
.timer {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.8rem 1rem;
}
.lead {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.ico {
  width: 1.6rem;
  height: 1.6rem;
  color: var(--naruto);
}
.lead b {
  font-size: 0.78rem;
  color: var(--ink);
  font-weight: 650;
  line-height: 1.2;
  max-width: 5.5rem;
}
.chain {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}
.st {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 8px;
  padding: 0.45rem 0.6rem;
  font-size: 0.72rem;
  line-height: 1.3;
  color: var(--ink-2);
}
.st code {
  align-self: flex-start;
  font-size: 0.58rem;
}
.st :deep(b) {
  color: var(--ink);
}
.arr {
  flex: none;
  width: 1rem;
  height: 1rem;
  color: var(--naruto);
}
.res {
  display: flex;
  align-items: baseline;
  gap: 0.35rem;
  white-space: nowrap;
}
.eq {
  font-size: 0.7rem;
  color: var(--muted);
}
.res b {
  font-family: var(--font-display);
  font-size: 1.35rem;
  color: var(--naruto);
  font-weight: 700;
}
.u {
  font-size: 0.68rem;
  color: var(--ink-2);
  white-space: normal;
  max-width: 7.5rem;
  line-height: 1.25;
}
</style>
