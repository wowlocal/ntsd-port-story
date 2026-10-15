<script setup lang="ts">
// The TVOS_WEB harness (docs/research/TVOS_WEB.md, «Harness» and «Gates»): four runners, one output layout,
// the comparators every earlier host already passed, frozen references. Hover a runner: what it reproduced first.
import { ref } from 'vue'

const runners = [
  { cmd: 'ios_app.py --platform tvos', host: 'симулятор Apple TV', first: 'тот же бегун сначала повторил iPad: vs равен, кадры те же' },
  { cmd: 'run_headless_scenarios.py --wasi', host: 'WASI в Node', first: 'тот же набор сценариев, что у Mac headless, тем же путём' },
  { cmd: 'run_headless_scenarios.py --browser / --web', host: 'headless Chromium и WebKit', first: 'мост страницы сначала вернул кадр байт в байт' },
  { cmd: 'web_app.py build / serve', host: 'статическая папка, без бегуна', first: 'сценарии из файлов этой папки равны, 18 088 кадров те же' },
]
const out = ['events.jsonl', 'frames/f*.png', 'дайджесты кадров', 'код выхода']
const cmp = ['compare_headless.py', 'compare_frames.py', 'compare_text_frames.py', 'matrix.py']
const hot = ref(-1)
</script>

<template>
  <div class="hn">
    <div class="col">
      <div class="h pixel">
        4 бегуна
      </div>
      <div
        v-for="(r, i) in runners" :key="r.cmd" class="run" :class="{ on: hot === i }" tabindex="0"
        @pointerenter="hot = i" @pointerleave="hot = -1" @focus="hot = i" @blur="hot = -1"
      >
        <code>{{ r.cmd }}</code>
        <span>{{ r.host }}</span>
      </div>
    </div>
    <div class="arrow">
      →
    </div>
    <div class="col mid">
      <div class="h pixel">
        один формат
      </div>
      <div class="box">
        <div class="mono path">
          OUT/&lt;сценарий&gt;/
        </div>
        <div v-for="o in out" :key="o" class="li">
          {{ o }}
        </div>
      </div>
    </div>
    <div class="arrow">
      →
    </div>
    <div class="col">
      <div class="h pixel">
        те же сравнения
      </div>
      <div class="box">
        <div v-for="c in cmp" :key="c" class="li mono">
          {{ c }}
        </div>
        <div class="ref">
          эталоны заморожены: 10 сценариев app_e2e, кадры по группам текста
        </div>
      </div>
    </div>
    <div class="foot">
      <span class="pixel hl">приёмка бегуна</span>
      <span v-if="hot < 0">прежде чем судить новый хост, бегун повторяет результат уже известного</span>
      <span v-else class="ink">{{ runners[hot].first }}</span>
    </div>
  </div>
</template>

<style scoped>
.hn {
  display: grid;
  grid-template-columns: 1.18fr 14px 0.7fr 14px 1.12fr;
  gap: 0.35rem 0.3rem;
  align-items: stretch;
}
.h {
  font-size: 0.66rem;
  color: var(--naruto);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 0.25rem;
}
.col {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}
.run {
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 8px;
  padding: 0.2rem 0.45rem 0.25rem;
  display: flex;
  flex-direction: column;
  line-height: 1.25;
  outline: none;
  transition: border-color 0.2s ease;
}
.run.on {
  border-color: rgba(255, 138, 61, 0.7);
}
.run code {
  font-size: 0.64rem !important;
  background: none !important;
  border: none !important;
  padding: 0 !important;
  color: #ffd5b8;
  white-space: normal;
  overflow-wrap: anywhere;
  line-height: 1.3;
  display: block;
}
.run span {
  font-size: 0.64rem;
  color: var(--ink-2);
}
.arrow {
  align-self: center;
  color: var(--muted);
  font-size: 0.9rem;
  text-align: center;
  padding-top: 1rem;
}
.box {
  flex: 1;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 8px;
  padding: 0.35rem 0.5rem;
}
.path {
  font-size: 0.66rem;
  color: var(--ink);
  margin-bottom: 0.15rem;
}
.li {
  font-size: 0.64rem;
  color: var(--ink-2);
  line-height: 1.5;
}
.li.mono {
  font-size: 0.64rem;
}
.mid .li::before {
  content: '└ ';
  color: var(--muted);
}
.ref {
  margin-top: 0.3rem;
  padding-top: 0.25rem;
  border-top: 1px solid var(--grid);
  font-size: 0.64rem;
  color: var(--muted);
  line-height: 1.3;
}
.foot {
  grid-column: 1 / -1;
  display: flex;
  gap: 0.6rem;
  align-items: baseline;
  font-size: 0.66rem;
  color: var(--ink-2);
  border-top: 1px solid var(--grid);
  padding-top: 0.3rem;
  min-height: 1.4rem;
}
.foot .pixel {
  font-size: 0.64rem;
  white-space: nowrap;
}
</style>
