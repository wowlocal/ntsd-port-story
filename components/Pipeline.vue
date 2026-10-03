<script setup lang="ts">
import { useNav, useSlideContext } from '@slidev/client'

// `stepwise` reveals one step per click (the slide needs `clicks: <steps>` in its frontmatter);
// export and print always show everything.
interface Step { name: string, ru?: string, desc?: string, icon?: string, accent?: boolean }
const props = withDefaults(defineProps<{ steps: Step[], loopLabel?: string, loopFrom?: number, loopTo?: number, stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const shown = (i: number) => !props.stepwise || nav.isPrintMode.value || ($clicks?.value ?? 0) >= i
</script>

<template>
  <div class="pipe">
    <div class="row" :style="{ gridTemplateColumns: `repeat(${steps.length}, 1fr)` }">
      <div v-for="(s, i) in steps" :key="s.name" class="step" :class="{ accent: s.accent, off: !shown(i) }">
        <div class="idx pixel">
          {{ String(i + 1).padStart(2, '0') }}
        </div>
        <div class="name mono">
          <span v-if="s.icon" class="icon">{{ s.icon }}</span>{{ s.name }}
        </div>
        <div v-if="s.ru" class="ru">
          {{ s.ru }}
        </div>
        <div v-if="s.desc" class="desc">
          {{ s.desc }}
        </div>
        <svg v-if="i < steps.length - 1" class="arrow" :class="{ off: !shown(i + 1) }" viewBox="0 0 16 16" width="16" height="16"><path d="M2 8h10M8 3l5 5-5 5" fill="none" stroke="var(--naruto)" stroke-width="2" stroke-linecap="square" /></svg>
      </div>
    </div>
    <div v-if="loopLabel && loopFrom !== undefined && loopTo !== undefined" class="loop" :class="{ off: !shown(steps.length) }" :style="{ gridTemplateColumns: `repeat(${steps.length}, 1fr)` }">
      <div class="loopwrap" :style="{ gridColumn: `${Math.min(loopFrom, loopTo) + 1} / ${Math.max(loopFrom, loopTo) + 2}` }">
        <svg class="loopsvg" viewBox="0 0 200 28" preserveAspectRatio="none">
          <path d="M150,0 V14 Q150,22 142,22 H58 Q50,22 50,14 V6" fill="none" stroke="var(--naruto)" stroke-width="2" vector-effect="non-scaling-stroke" />
        </svg>
        <svg class="loophead" viewBox="0 0 12 10"><path d="M1 9 L6 2 L11 9" fill="none" stroke="var(--naruto)" stroke-width="2" /></svg>
        <div class="looplabel mono">
          {{ loopLabel }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.step,
.arrow,
.loop {
  transition: opacity 0.35s ease, transform 0.35s ease;
}
.off {
  opacity: 0;
  transform: translateY(6px);
}
.arrow.off {
  transform: translateY(-50%);
}
.row {
  display: grid;
  gap: 1.1rem;
}
.step {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.6rem 0.7rem 0.7rem;
}
.step.accent {
  border-color: rgba(255, 138, 61, 0.55);
  box-shadow: 0 0 0 1px rgba(255, 138, 61, 0.2), 0 10px 24px rgba(217, 89, 38, 0.15);
}
.idx {
  font-size: 0.68rem;
  color: var(--naruto);
}
.name {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--ink);
  margin-top: 0.15rem;
  word-break: break-word;
}
.icon {
  margin-right: 0.3rem;
}
.ru {
  font-size: 0.72rem;
  color: var(--ink);
  margin-top: 0.15rem;
  font-weight: 600;
}
.desc {
  font-size: 0.66rem;
  color: var(--ink-2);
  line-height: 1.35;
  margin-top: 0.3rem;
}
.arrow {
  position: absolute;
  right: -1.05rem;
  top: 50%;
  transform: translateY(-50%);
}
.loop {
  display: grid;
  gap: 1.1rem;
  margin-top: 0.2rem;
}
.loopwrap {
  position: relative;
  height: 2.6rem;
}
.loopsvg {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  width: 100%;
  height: 1.6rem;
}
.loophead {
  position: absolute;
  left: calc(25% - 6px);
  top: -2px;
  width: 12px;
  height: 10px;
}
.looplabel {
  position: absolute;
  left: 0;
  right: 0;
  top: 1.65rem;
  text-align: center;
  font-size: 0.64rem;
  color: var(--naruto);
  white-space: nowrap;
}
</style>
