<script setup lang="ts">
// Seven principles, each quoted verbatim from AGENTS.md (English, primary). The Russian line is a
// short gloss; in cards 5–7 it is the matching sentence of docs/research/WORKFLOW.md, in «».
const items = [
  {
    en: 'Do not guess physics, combo timing, damage, AI, randomness or standard engine behavior.',
    ru: 'Не угадывать: числа, порядок операций, знаковость и переполнения — как в EXE.',
    icon: 'i-pixelarticons-dice',
  },
  {
    en: 'No unobserved storage becomes known zero.',
    ru: 'Неизвестный байт остаётся неизвестным, пока не доказано его происхождение.',
    icon: 'i-pixelarticons-eye-off',
  },
  {
    en: 'Never change an old expected value or exclude a mismatch to accept a candidate.',
    ru: 'Эталоны неизменны; исправление получает собственное доказательство.',
    icon: 'i-pixelarticons-lock',
  },
  {
    en: 'Native rejection with rollback is not a successful match to a source fault.',
    ru: 'Откат порта там, где оригинал падает, — это не совпадение.',
    icon: 'i-pixelarticons-undo',
  },
  {
    en: 'Process exit 0 alone is not acceptance.',
    ru: '«Код выхода процесса 0 означает только завершение процесса».',
    icon: 'i-pixelarticons-terminal',
  },
  {
    en: 'Models do not replace the comparator.',
    ru: '«Мнение LLM и структурное сходство кода не заменяют сравнение поведения».',
    icon: 'i-pixelarticons-robot',
  },
  {
    en: 'Isolated function tests and instruction counts do not establish a whole tick, match or game.',
    ru: '«Нельзя выводить полную корректность матча из суммы успешно проверенных функций».',
    icon: 'i-pixelarticons-blocks',
  },
]
const rows = [items.slice(0, 4), items.slice(4)]
</script>

<template>
  <div class="principles">
    <div v-for="(row, r) in rows" :key="r" class="row" :style="{ gridTemplateColumns: `repeat(${row.length}, minmax(0, 1fr))` }">
      <div v-for="(it, k) in row" :key="it.en" class="card-q">
        <div class="top">
          <span class="ico" :class="it.icon" />
          <span class="num pixel">{{ String(r * 4 + k + 1).padStart(2, '0') }}</span>
        </div>
        <div class="en mono">
          {{ it.en }}
        </div>
        <div class="ru">
          {{ it.ru }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.principles {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.row {
  display: grid;
  gap: 0.6rem;
}
.card-q {
  position: relative;
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.65rem 0.8rem 0.7rem;
  overflow: hidden;
}
.card-q::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--naruto);
  opacity: 0.85;
}
.top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.ico {
  width: 1.75rem;
  height: 1.75rem;
  color: var(--naruto);
}
.num {
  font-size: 0.7rem;
  color: var(--muted);
}
.en {
  font-size: 0.8rem;
  font-weight: 600;
  line-height: 1.38;
  color: var(--ink);
  margin-top: 0.4rem;
}
.ru {
  font-size: 0.65rem;
  line-height: 1.38;
  color: var(--ink-2);
  margin-top: auto;
  padding-top: 0.45rem;
}
</style>
