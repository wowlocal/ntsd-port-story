<script setup lang="ts">
import { ref } from 'vue'

// The browser host (TVOS_WEB W2a–W2b-4c): the game runs in a worker that never yields, so everything it shares
// with the page goes through shared memory. Five channels, each with the defect a review or a test caught on it.
// Hover a channel or its card to light both. Facts: TVOS_WEB.md ledger, commits b0b6b470 … 21f5caa9.
interface Ch { key: string, name: string, dir: 'left' | 'right', line: string, sub: string, who: string, bug: string, ok: string, hash: string }
const chans: Ch[] = [
  { key: 'frame', name: 'кадр', dir: 'left', line: 'общий буфер кадра под seqlock', sub: 'страница рисует новейший на каждом кадре анимации', who: 'ревью', bug: 'OffscreenCanvas не дошёл бы до страницы: воркер не уступает управление.', ok: 'Через общий буфер страница рисует почти каждый кадр: 3 655 из 3 655.', hash: 'b0b6b470' },
  { key: 'input', name: 'ввод', dir: 'right', line: 'кольцо ввода: клавиши, мышь, Gamepad API', sub: 'хост выбирает его каждые 2 мс', who: 'ревью', bug: 'После Alt+Tab залипали клавиши, терялась вторая кнопка мыши.', ok: 'При потере фокуса страница отпускает всё нажатое.', hash: '6f4cb344' },
  { key: 'audio', name: 'звук', dir: 'left', line: 'кольцо стерео-сэмплов, ≈ 150 мс вперёд', sub: 'AudioWorklet играет на 44,1 кГц', who: 'тест', bug: 'Декодер ALAC отбрасывал каждый пакет: little-endian знал только Linux, Android, Windows.', ok: '+ .wasi в Package.swift: сэмпл в сэмпл с macOS.', hash: 'c1cd3f91' },
  { key: 'saves', name: 'сохранения', dir: 'left', line: 'изменения /save по порядку → IndexedDB', sub: 'второй визит читает сохранения первого', who: 'тест', bug: 'Chromium по умолчанию терял последнее сохранение, если браузер убит.', ok: 'Запись со строгой durability.', hash: 'f829a551' },
  { key: 'files', name: 'файлы', dir: 'right', line: 'файлы по требованию: синхронный XHR', sub: '/app и /music только для чтения', who: 'тест', bug: 'Без пробы кэша WebKit скачал всё дважды: 3 045 запросов, 1 635 МБ.', ok: 'Подкачка — только если кэш отвечает на чтения.', hash: '21f5caa9' },
]
const hot = ref<string | null>(null)

const W = 884
const bw = 196
const L = bw
const R = W - bw
const y0 = 30
const RH = 33
const H = y0 + chans.length * RH + 8
const cy = (i: number) => y0 + i * RH + RH / 2
const pageItems = ['canvas 794×550', 'клавиатура, мышь, геймпад', 'AudioWorklet', 'IndexedDB', 'Full screen и Saves']
const workerItems = ['NTSDWeb.wasm', 'WASI-шим: 34 импорта', 'цикл не отдаёт управление', 'сон — Atomics.wait', 'headless-хост + вывод кадра']
</script>

<template>
  <div class="br">
    <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Страница и воркер браузера: пять каналов через общую память">
      <defs>
        <marker id="wbArrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L8,4 L0,8 z" fill="var(--ink-2)" />
        </marker>
        <marker id="wbArrowHot" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L8,4 L0,8 z" fill="var(--naruto)" />
        </marker>
      </defs>
      <!-- page -->
      <rect x="0.5" y="4" :width="bw - 8" :height="H - 6" rx="10" class="box" />
      <text x="12" y="20" class="bh">страница · главный поток</text>
      <text v-for="(t, i) in pageItems" :key="t" x="12" :y="cy(i) + 8" class="bi">{{ t }}</text>
      <!-- worker -->
      <rect :x="R + 8" y="4" :width="bw - 8.5" :height="H - 6" rx="10" class="box wk" />
      <text :x="R + 20" y="20" class="bh">воркер · игра</text>
      <text v-for="(t, i) in workerItems" :key="t" :x="R + 20" :y="cy(i) + 8" class="bi">{{ t }}</text>
      <!-- channels -->
      <g
        v-for="(c, i) in chans" :key="c.key" class="ch" :class="{ on: hot === c.key, dim: hot && hot !== c.key }" tabindex="0"
        @pointerenter="hot = c.key" @pointerleave="hot = null" @focus="hot = c.key" @blur="hot = null"
      >
        <rect :x="L" :y="cy(i) - RH / 2 + 1" :width="R - L + 8" :height="RH - 2" fill="transparent" />
        <text :x="L + 10" :y="cy(i) - 5" class="cn">{{ c.name }}</text>
        <g :transform="`translate(${L + 16 + c.name.length * 7.3} ${cy(i) - 15})`">
          <rect x="0" y="0" :width="c.who === 'ревью' ? 40 : 30" height="13" rx="6.5" class="badge" />
          <text :x="c.who === 'ревью' ? 20 : 15" y="10" text-anchor="middle" class="bt">{{ c.who }}</text>
        </g>
        <text :x="L + 134" :y="cy(i) - 5" class="cl">{{ c.line }}</text>
        <line
          :x1="c.dir === 'right' ? L + 4 : R + 2" :x2="c.dir === 'right' ? R + 2 : L + 4" :y1="cy(i) + 3" :y2="cy(i) + 3"
          :stroke="hot === c.key ? 'var(--naruto)' : 'var(--ink-2)'" stroke-width="1.5" :marker-end="hot === c.key ? 'url(#wbArrowHot)' : 'url(#wbArrow)'"
        />
        <text :x="L + 134" :y="cy(i) + 15" class="cs">{{ c.sub }}</text>
      </g>
    </svg>
    <div class="cards">
      <div
        v-for="c in chans" :key="c.key" class="cd" :class="{ on: hot === c.key }" tabindex="0"
        @pointerenter="hot = c.key" @pointerleave="hot = null" @focus="hot = c.key" @blur="hot = null"
      >
        <div class="ch2">
          <b>{{ c.name }}</b><span class="mono">{{ c.hash }}</span>
        </div>
        <p class="bug">
          {{ c.bug }}
        </p>
        <p class="ok">
          {{ c.ok }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.box {
  fill: var(--surface);
  stroke: rgba(255, 255, 255, 0.1);
}
.box.wk {
  stroke: rgba(255, 138, 61, 0.35);
}
.bh {
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 700;
  fill: var(--ink);
}
.bi {
  font-family: var(--font-sans);
  font-size: 10.5px;
  fill: var(--ink-2);
}
.ch {
  cursor: pointer;
  outline: none;
  transition: opacity 0.2s ease;
}
.ch.dim {
  opacity: 0.35;
}
.cn {
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 700;
  fill: var(--ink);
}
.cl {
  font-family: var(--font-sans);
  font-size: 11px;
  fill: var(--ink);
}
.cs {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
}
.badge {
  fill: rgba(255, 138, 61, 0.16);
  stroke: rgba(255, 138, 61, 0.7);
  stroke-width: 1;
}
.bt {
  font-family: var(--font-sans);
  font-size: 10px;
  font-weight: 600;
  fill: #ffd5b8;
}
.cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.45rem;
  margin-top: 0.35rem;
}
.cd {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--hair);
  border-radius: 10px;
  padding: 0.35rem 0.5rem 0.4rem;
  outline: none;
  transition: border-color 0.2s ease, background 0.2s ease;
}
.cd.on {
  border-color: rgba(255, 138, 61, 0.7);
  background: rgba(255, 138, 61, 0.06);
}
.ch2 {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-size: 0.68rem;
  color: var(--ink);
}
.ch2 .mono {
  font-size: 0.64rem;
  color: var(--muted);
}
.cd p {
  margin: 0.15rem 0 0 !important;
  font-size: 0.66rem;
  line-height: 1.32;
}
.bug {
  color: #ffc4b0;
}
.ok {
  color: var(--ink-2);
}
</style>
