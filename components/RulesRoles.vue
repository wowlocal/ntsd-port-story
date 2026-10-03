<script setup lang="ts">
// Who may say "done" (docs/research/WORKFLOW.md, table "Исполнитель, проверяющий и сравнение"):
// executor → candidate → independent reviewer and deterministic comparator → done.
// One line per node; quotes and counts sit in a small mono tag.
interface Node { title: string, line: string, tag?: string, icon: string }
const exec: Node = { title: 'исполнитель', line: 'пишет кандидат и запускает проверки', tag: '"do not label author self-review independent"', icon: 'i-pixelarticons-code' }
const cand: Node = { title: 'кандидат', line: 'артефакты и объявленные входы', icon: 'i-pixelarticons-git-branch' }
const review: Node = { title: 'независимый ревьюер', line: 'read-only: исходные доказательства, «не только объяснение автора»', tag: '449 упоминаний «independent review» в 226 карточках', icon: 'i-pixelarticons-eye' }
const comp: Node = { title: 'компаратор', line: 'неизменяемые expected и маски — последнее слово за ним', tag: 'байты + маски, а не мнение модели', icon: 'i-pixelarticons-binary' }
const done: Node = { title: 'готово', line: 'всё совпало, замечания ревьюера закрыты', icon: 'i-pixelarticons-checkbox-on' }
// connector columns: SVG path in a 0..40 × 0..100 box stretched to the cell, arrowheads at `heads` (% from top)
const links = [
  { col: 2, d: 'M0,50 H40', heads: [50] },
  { col: 4, d: 'M0,50 H18 M18,25 V75 M18,25 H40 M18,75 H40', heads: [25, 75] },
  { col: 6, d: 'M0,25 H22 M0,75 H22 M22,25 V75 M22,50 H40', heads: [50] },
]
</script>

<template>
  <div class="roles">
    <div v-for="(n, k) in [exec, cand]" :key="n.title" class="node" :style="{ gridColumn: k === 0 ? 1 : 3 }">
      <div class="head">
        <span class="ico" :class="n.icon" /><b class="pixel">{{ n.title }}</b>
      </div>
      <div class="line">
        {{ n.line }}
      </div>
      <div v-if="n.tag" class="tag-m mono">
        {{ n.tag }}
      </div>
    </div>

    <div v-for="l in links" :key="l.col" class="link" :style="{ gridColumn: l.col }">
      <svg viewBox="0 0 40 100" preserveAspectRatio="none">
        <path :d="l.d" stroke="var(--naruto)" stroke-width="2" fill="none" vector-effect="non-scaling-stroke" />
      </svg>
      <svg v-for="h in l.heads" :key="h" class="arrowhead" :style="{ top: `${h}%` }" viewBox="0 0 10 12">
        <path d="M1 1 L8 6 L1 11" fill="none" stroke="var(--naruto)" stroke-width="2" />
      </svg>
    </div>

    <div v-for="(n, k) in [review, comp]" :key="n.title" class="node stack" :style="{ gridRow: k + 1 }">
      <div class="head">
        <span class="ico" :class="n.icon" /><b class="pixel">{{ n.title }}</b>
      </div>
      <div class="line">
        {{ n.line }}
      </div>
      <div v-if="n.tag" class="tag-m mono">
        {{ n.tag }}
      </div>
    </div>

    <div class="node done" style="grid-column: 7">
      <div class="head">
        <span class="ico" :class="done.icon" /><b class="pixel">{{ done.title }}</b>
      </div>
      <div class="line">
        {{ done.line }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.roles {
  display: grid;
  grid-template-columns: 1fr 1.5rem 0.9fr 2.2rem 1.45fr 2.2rem 0.85fr;
  grid-template-rows: 1fr 1fr;
  align-items: center;
}
.node {
  grid-row: 1 / 3;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.6rem 0.75rem 0.65rem;
}
.node.stack {
  grid-column: 5;
  margin: 0.25rem 0;
}
.node.done {
  border-color: rgba(255, 138, 61, 0.55);
  background: rgba(255, 138, 61, 0.07);
  box-shadow: 0 0 0 1px rgba(255, 138, 61, 0.18), 0 10px 24px rgba(217, 89, 38, 0.14);
}
.head {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}
.ico {
  flex: none;
  width: 1.4rem;
  height: 1.4rem;
  color: var(--naruto);
}
.head b {
  font-size: 0.78rem;
  font-weight: 400;
  color: var(--naruto);
  line-height: 1.15;
}
.done .head b {
  color: var(--ink);
}
.line {
  font-size: 0.66rem;
  line-height: 1.35;
  color: var(--ink-2);
  margin-top: 0.35rem;
}
.done .line {
  color: var(--ink);
}
.tag-m {
  font-size: 0.56rem;
  line-height: 1.3;
  color: var(--muted);
  margin-top: 0.35rem;
}
.link {
  grid-row: 1 / 3;
  align-self: stretch;
  position: relative;
}
.link svg:first-child {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
.arrowhead {
  position: absolute;
  right: -1px;
  width: 9px;
  height: 11px;
  transform: translateY(-50%);
}
</style>
