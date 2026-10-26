<script setup lang="ts">
// Chapter 7: the five questions Claude left when it stopped the loop at 00:53 on 1 October, the author's
// single reply at 05:56 and the commits that carried each answer out by 09:42. The questions are a Russian
// gloss of the agent's "Waiting on you" list (session 7ea5b99f, 2026-09-30T22:53:59Z); the reply is verbatim
// (2026-10-01T03:56:25Z), split into its five sentences. Hover a question, a piece of the reply or a commit
// to light that decision; with nothing hovered (and in export) every row is lit.
import { ref } from 'vue'

interface Decision { n: number, color: string, q: string, reply: string }
const decisions: Decision[] = [
  { n: 1, color: 'var(--s1)', q: 'Запуск: открывать оригинальную игру вместо Practice?', reply: 'При запуске открывать основную игру.' },
  { n: 2, color: 'var(--s2)', q: 'Alt+Enter: как в оригинале, полный экран macOS — или оба?', reply: 'Поведение Alt+Enter воспроизвести как в оригинале; стандартный полноэкранный режим macOS можно добавить отдельно.' },
  { n: 3, color: 'var(--s3)', q: 'Текст GDI: каким шрифтом, если вообще? Цифры Summary и имена пока пусты', reply: 'Шрифт установить по оригиналу, а если есть препятствие, то для GDI-текста используй стандартный системный шрифт macOS. Сохрани положение, размер, цвет и выравнивание текста максимально близко к оригиналу. Различие в шрифте зафиксируй как временное отступление от точного воспроизведения; оно не должно блокировать дальнейшую работу.' },
  { n: 4, color: 'var(--s4)', q: 'Музыка Demo: оставить подставное значение, которое выбирает трек?', reply: 'Подставной выбор музыки считать временным.' },
  { n: 5, color: 'var(--s5)', q: 'F8 на полном пуле: строить полную обработку?', reply: 'Полную обработку F8 оставить обязательной частью совместимости и выполнить в порядке приоритетов проекта.' },
]

interface Done { n: number, time: string, hash?: string, text: string }
const done: Done[] = [
  { n: 1, time: '06:01', hash: '80c83c1', text: '<b>.app без аргументов открывает оригинал</b>; лаборатория Practice — по <code>--practice</code>' },
  { n: 3, time: '06:45', hash: '778a8c4', text: '<b>SYSTEM_FONT поставлять нельзя</b> — системный шрифт Mac, bold 13 px в ячейке 16 px; позиция и цвет — оригинала' },
  { n: 2, time: '07:30', hash: 'cb33304', text: '<b>Alt+Enter как в оригинале</b>: окно уничтожается и создаётся заново, звук пропадает; в записи — падение оригинала' },
  { n: 5, time: '09:08', hash: 'f4cdcbb', text: '<b>слово SP+34 смоделировано</b> через весь цикл 41f550..4214cf — 9 новых тестов' },
  { n: 2, time: '09:42', hash: 'c50a806', text: '<b>и отдельно — полный экран macOS</b>: зелёная кнопка, ⌃⌘F; игра не получает ни одного сообщения' },
  { n: 4, time: 'без кода', text: '<b>записано как временное</b>: трек Demo выбирает остаток регистра ECX — нужен замер на Windows' },
]

const hover = ref<number | null>(null)
const lit = (n: number) => hover.value === null || hover.value === n
const colorOf = (n: number) => decisions[n - 1].color
</script>

<template>
  <div class="dec" @mouseleave="hover = null">
    <div class="left">
      <div class="qbox">
        <div class="hd">
          <span class="t mono">00:53</span><b>Claude</b> останавливает <code>/loop</code>: «Waiting on you» <span class="muted">· пересказ</span>
        </div>
        <div v-for="d in decisions" :key="d.n" class="q" :class="{ dim: !lit(d.n) }" @mouseenter="hover = d.n">
          <i class="chip" :style="{ background: d.color }">{{ d.n }}</i><span>{{ d.q }}</span>
        </div>
      </div>
      <div class="gap">
        <span class="mono">5 ч 03 мин</span> тишины
      </div>
      <div class="human">
        <div class="hd hr"><b>автор</b><span class="t mono">05:56</span></div>
        <div class="bubble">
          <span v-for="d in decisions" :key="d.n" class="seg" :class="{ dim: !lit(d.n) }" :style="{ '--c': d.color }" @mouseenter="hover = d.n"><sup>{{ d.n }}</sup>{{ d.reply }} </span>
        </div>
      </div>
    </div>
    <div class="right">
      <div class="hd">
        <span class="t mono">05:56 → 09:42</span><b>3 ч 46 мин</b> — пять коммитов
      </div>
      <ol class="runs">
        <li v-for="(c, i) in done" :key="i" :class="{ dim: !lit(c.n), nocode: !c.hash }" :style="{ '--c': colorOf(c.n) }" @mouseenter="hover = c.n">
          <span class="tm mono">{{ c.time }}</span>
          <i class="chip" :style="{ background: colorOf(c.n) }">{{ c.n }}</i>
          <span class="tx" v-html="c.text" />
          <code v-if="c.hash" class="hs">{{ c.hash }}</code>
        </li>
      </ol>
    </div>
  </div>
</template>

<style scoped>
.dec { display: grid; grid-template-columns: 1.08fr 1fr; gap: 1.1rem; }
.left, .right { display: flex; flex-direction: column; min-width: 0; }
.hd { font-size: 0.6rem; color: var(--ink-2); margin-bottom: 0.3rem; display: flex; align-items: baseline; gap: 0.35rem; flex-wrap: wrap; }
.hd b { color: var(--ink); }
.hd code { font-size: 0.56rem !important; }
.hd .t { color: var(--muted); }
.hd.hr { justify-content: flex-end; margin: 0 0.3rem 0.12rem; }
.qbox { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; border-top-left-radius: 4px; padding: 0.45rem 0.65rem 0.4rem; }
.q { display: grid; grid-template-columns: 1.05rem 1fr; gap: 0.4rem; align-items: start; font-size: 0.64rem; line-height: 1.3; color: var(--ink); padding: 0.14rem 0; transition: opacity 0.2s; cursor: default; }
.chip { display: inline-flex; align-items: center; justify-content: center; width: 1.05rem; height: 1.05rem; border-radius: 4px; font-style: normal; font-family: var(--font-mono); font-size: 0.6rem; color: #0a0d13; font-weight: 700; }
.gap { align-self: center; font-size: 0.56rem; color: var(--muted); margin: 0.3rem 0 0.15rem; letter-spacing: 0.02em; }
.gap .mono { color: var(--ink-2); }
.human { display: flex; flex-direction: column; align-items: flex-end; }
.bubble { background: rgba(57, 135, 229, 0.16); border: 1px solid rgba(57, 135, 229, 0.45); border-radius: 12px; border-top-right-radius: 4px; padding: 0.42rem 0.6rem; font-size: 0.62rem; line-height: 1.42; color: var(--ink); }
.seg { transition: opacity 0.2s; box-shadow: inset 0 -2px 0 var(--c); cursor: default; }
.seg sup { font-family: var(--font-mono); font-size: 0.5rem; font-weight: 700; color: var(--c); margin-right: 0.12rem; vertical-align: 0.35em; }
.runs { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.32rem; }
.runs li { display: grid; grid-template-columns: 2.6rem 1.05rem 1fr auto; gap: 0.45rem; align-items: center; background: var(--surface); border: 1px solid var(--hair); border-left: 3px solid var(--c); border-radius: 10px; padding: 0.34rem 0.55rem 0.34rem 0.5rem; transition: opacity 0.2s; cursor: default; }
.runs li.nocode { background: transparent; border-style: dashed; border-left-style: solid; }
.tm { font-size: 0.62rem; color: var(--ink); }
.nocode .tm { color: var(--muted); font-size: 0.54rem; }
.tx { font-size: 0.6rem; line-height: 1.32; color: var(--ink-2); }
.tx :deep(b) { color: var(--ink); font-weight: 650; }
.tx :deep(code) { font-size: 0.54rem !important; }
.hs { font-size: 0.54rem !important; color: var(--muted) !important; background: rgba(255, 255, 255, 0.05) !important; border: 0 !important; }
.dim { opacity: 0.28; }
</style>
