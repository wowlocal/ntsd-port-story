<script setup lang="ts">
const rungs = [
  {
    name: 'actual Windows / device observation',
    ru: 'наблюдение на настоящей Windows или устройстве',
    note: 'оригинал под CrossOver, окно, звук, геймпад; синтетические ответы API так не называются',
    level: 4,
  },
  {
    name: 'controlled differential comparison',
    ru: 'контролируемое дифференциальное сравнение',
    note: 'одни и те же входы → оригинальный код (Unicorn) и Swift → побайтное сравнение',
    level: 3,
  },
  {
    name: 'inference',
    ru: 'вывод',
    note: 'логическое следствие из улик; помечается как вывод, а не факт',
    level: 2,
  },
  {
    name: 'static evidence',
    ru: 'статическая улика',
    note: 'дизассемблер: адрес инструкции, хэш EXE, константа в .rdata',
    level: 1,
  },
]
</script>

<template>
  <div class="ladder">
    <div v-for="r in rungs" :key="r.name" class="rung" :style="{ marginLeft: `${(4 - r.level) * 2.2}rem` }">
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
  grid-template-columns: 2.2rem 1fr;
  align-items: center;
  gap: 0.7rem;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.5rem 0.8rem;
}
.rung:first-child {
  border-color: rgba(255, 138, 61, 0.5);
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
</style>
