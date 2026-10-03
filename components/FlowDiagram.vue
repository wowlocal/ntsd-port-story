<script setup lang="ts">
// Two-lane flow: one shared input fans out to two programs whose outputs meet in a comparator.
interface Lane { title: string, sub?: string, out: string, color?: string, tag?: string }
withDefaults(defineProps<{
  input: string
  inputSub?: string
  lanes: Lane[]
  verdict: string
  verdictSub?: string
}>(), {})
</script>

<template>
  <div class="flow">
    <div class="node input">
      <div class="t">
        {{ input }}
      </div>
      <div v-if="inputSub" class="s">
        {{ inputSub }}
      </div>
    </div>
    <svg class="fan" viewBox="0 0 60 200" preserveAspectRatio="none">
      <path d="M0,100 C30,100 30,40 60,40" fill="none" stroke="var(--axis)" stroke-width="2" vector-effect="non-scaling-stroke" />
      <path d="M0,100 C30,100 30,160 60,160" fill="none" stroke="var(--axis)" stroke-width="2" vector-effect="non-scaling-stroke" />
    </svg>
    <div class="lanes">
      <div v-for="l in lanes" :key="l.title" class="lane">
        <div class="node prog" :style="{ borderColor: l.color }">
          <div v-if="l.tag" class="tag">
            {{ l.tag }}
          </div>
          <div class="t">
            {{ l.title }}
          </div>
          <div v-if="l.sub" class="s">
            {{ l.sub }}
          </div>
        </div>
        <svg class="arrow" viewBox="0 0 40 12"><path d="M0 6h32M28 1l6 5-6 5" fill="none" stroke="var(--axis)" stroke-width="2" /></svg>
        <div class="node out">
          <div class="s">
            {{ l.out }}
          </div>
        </div>
      </div>
    </div>
    <svg class="fan" viewBox="0 0 60 200" preserveAspectRatio="none">
      <path d="M0,40 C30,40 30,100 60,100" fill="none" stroke="var(--axis)" stroke-width="2" vector-effect="non-scaling-stroke" />
      <path d="M0,160 C30,160 30,100 60,100" fill="none" stroke="var(--axis)" stroke-width="2" vector-effect="non-scaling-stroke" />
    </svg>
    <div class="node verdict">
      <div class="eq pixel">
        ==
      </div>
      <div class="t">
        {{ verdict }}
      </div>
      <div v-if="verdictSub" class="s">
        {{ verdictSub }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.flow {
  display: grid;
  grid-template-columns: 9.5rem 2.6rem 1fr 2.6rem 9rem;
  align-items: center;
}
.fan {
  width: 100%;
  height: 11rem;
}
.lanes {
  display: flex;
  flex-direction: column;
  gap: 1.6rem;
}
.lane {
  display: grid;
  grid-template-columns: 1.25fr 2rem 1fr;
  align-items: center;
}
.arrow {
  width: 100%;
  height: 12px;
}
.node {
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.55rem 0.7rem;
  position: relative;
}
.prog {
  border-width: 1.5px;
}
.input {
  border-color: rgba(255, 255, 255, 0.18);
}
.verdict {
  text-align: center;
  border-color: rgba(255, 138, 61, 0.55);
  box-shadow: 0 0 24px rgba(217, 89, 38, 0.18);
}
.eq {
  font-size: 1.6rem;
  color: var(--naruto);
  line-height: 1;
}
.t {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--ink);
  line-height: 1.25;
}
.s {
  font-size: 0.66rem;
  color: var(--ink-2);
  line-height: 1.3;
  margin-top: 0.15rem;
}
.out .s {
  margin-top: 0;
}
.tag {
  position: absolute;
  top: -0.6rem;
  left: 0.6rem;
  font-size: 0.58rem;
}
</style>
