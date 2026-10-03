<script setup lang="ts">
import { useNav, useSlideContext } from '@slidev/client'

// The four evidence classes of AGENTS.md, strongest on top. `scale` is the letter of the short
// S / D / W scale in RESEARCH_MAP.md that covers the rung (inference has none).
// `stepwise` reveals the rungs bottom-up, one per click: rung `level` appears at click `level`,
// so the slide needs `clicks: 4`. Hidden rungs keep a dashed outline; export and print show all.
const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const shown = (level: number) => !props.stepwise || nav.isPrintMode.value || ($clicks?.value ?? 0) >= level

const rungs = [
  {
    name: 'actual Windows / device observation',
    ru: 'наблюдение на настоящей Windows или устройстве',
    note: 'оригинал под CrossOver, окно, звук, геймпад; синтетические ответы API так не называются',
    level: 4,
    scale: 'W',
  },
  {
    name: 'controlled differential comparison',
    ru: 'контролируемое дифференциальное сравнение',
    note: 'одни и те же входы → оригинальный код (Unicorn) и Swift → побайтное сравнение',
    level: 3,
    scale: 'D',
  },
  {
    name: 'inference',
    ru: 'вывод',
    note: 'логическое следствие из улик; помечается как вывод, а не факт',
    level: 2,
    scale: '',
  },
  {
    name: 'static evidence',
    ru: 'статическая улика',
    note: 'дизассемблер: адрес инструкции, хэш EXE, константа в .rdata',
    level: 1,
    scale: 'S',
  },
]
</script>

<template>
  <div class="ladder">
    <div
      v-for="r in rungs"
      :key="r.name"
      class="rung"
      :class="{ off: !shown(r.level), top: r.level === 4 }"
      :style="{ marginLeft: `${(4 - r.level) * 2.2}rem` }"
    >
      <div class="lvl pixel">
        {{ r.level }}
      </div>
      <div class="txt">
        <div class="name mono">
          {{ r.name }}
        </div>
        <div class="ru">
          {{ r.ru }}
        </div>
        <div class="note">
          {{ r.note }}
        </div>
      </div>
      <div class="scale mono" :class="{ none: !r.scale }">
        {{ r.scale || '—' }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.ladder {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}
.rung {
  display: grid;
  grid-template-columns: 2.2rem 1fr auto;
  align-items: center;
  gap: 0.7rem;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.5rem 0.8rem;
  transition: background-color 0.35s ease, border-color 0.35s ease;
}
.rung > * {
  transition: opacity 0.35s ease, transform 0.35s ease;
}
.rung.top {
  border-color: rgba(255, 138, 61, 0.5);
}
.rung.off {
  background: transparent;
  border: 1px dashed var(--axis);
}
.rung.off > * {
  opacity: 0;
  transform: translateY(6px);
}
.lvl {
  width: 2.2rem;
  height: 2.2rem;
  display: grid;
  place-items: center;
  background: rgba(255, 138, 61, 0.12);
  color: var(--naruto);
  font-size: 1.1rem;
  border-radius: 8px;
}
.name {
  font-size: 0.74rem;
  color: var(--ink);
  font-weight: 700;
}
.ru {
  font-size: 0.74rem;
  color: var(--ink);
}
.note {
  font-size: 0.64rem;
  color: var(--muted);
  line-height: 1.3;
  margin-top: 0.1rem;
}
.scale {
  width: 1.55rem;
  height: 1.55rem;
  display: grid;
  place-items: center;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--chakra);
  border: 1px solid rgba(108, 182, 255, 0.45);
  border-radius: 6px;
}
.scale.none {
  color: var(--muted);
  border-color: var(--hair);
  font-weight: 400;
}
</style>
