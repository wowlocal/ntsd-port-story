<script setup lang="ts">
// Illustrative stack (widths are not data): from the most holistic check on top to the most granular at the base.
const layers = [
  { n: '58 + 244', what: 'целых матчей против оригинала под CrossOver · кадров Demo тик в тик', note: '42 Mac → оригинал, 5 оригинал → Mac, 11 ранних повторов' },
  { n: '22 + 10', what: 'длинных прогонов до 200 000 тиков · e2e-сценариев приложения', note: 'vs, mission, demo, war, playback, tournament ×2, team, altenter, joystick' },
  { n: '692', what: 'Swift-теста в 317 файлах', note: 'XCTest против неизменяемых фикстур' },
  { n: '408 + 698', what: 'фикстур (4,3 ГиБ) · evidence-записей', note: 'эталоны и квитанции проверок, всё в git' },
  { n: '215', what: 'Unicorn-оракулов отдельных функций EXE', note: '+ 23 092 сырых корпуса, 8,5 ГБ, локально' },
]
</script>

<template>
  <div class="pyr">
    <div v-for="(l, i) in layers" :key="i" class="layer" :style="{ width: `${52 + i * 12}%` }">
      <span class="n">{{ l.n }}</span>
      <span class="what">{{ l.what }}<span class="note">{{ l.note }}</span></span>
    </div>
  </div>
</template>

<style scoped>
.pyr {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}
.layer {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: linear-gradient(90deg, rgba(57, 135, 229, 0.18), rgba(57, 135, 229, 0.06));
  border: 1px solid rgba(57, 135, 229, 0.35);
  border-radius: 10px;
  padding: 0.42rem 0.9rem;
}
.layer:first-child {
  background: linear-gradient(90deg, rgba(217, 89, 38, 0.3), rgba(217, 89, 38, 0.08));
  border-color: rgba(255, 138, 61, 0.55);
}
.n {
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--ink);
  white-space: nowrap;
  min-width: 5.6rem;
}
.what {
  font-size: 0.74rem;
  color: var(--ink);
  line-height: 1.25;
  display: flex;
  flex-direction: column;
}
.note {
  font-size: 0.62rem;
  color: var(--muted);
}
</style>
