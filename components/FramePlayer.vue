<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useIsSlideActive, useNav } from '@slidev/client'
import data from '../data/engine_sequence.json'

// A frame debugger: plays one real `next` chain from chars/naruto.dat tick by tick.
// A frame with `wait: N` stays for N + 1 ticks (frame.ticks, written by scripts/extract_frames.py
// from docs/research/ACTOR_SCHEDULER.md rules 4 and 7). The timer is slowed to `tps` ticks per second;
// print/export shows `printFrame` at its `printTick`-th tick. The default slot goes under the HUD.
const props = withDefaults(defineProps<{
  scale?: number
  tps?: number
  printFrame?: number
  printTick?: number
}>(), { scale: 3, tps: 5, printFrame: 72, printTick: 2 })

interface Box { kind?: number, x: number, y: number, w: number, h: number, [k: string]: number | undefined }
interface Point { oid?: number, action?: number, file?: string | null, [k: string]: unknown }
interface Frame {
  id: number, name: string, pic: number, state: number, wait: number, next: number, ticks: number
  centerx: number, centery: number, dvx: number, mp: number | null, sound: string | null
  image: string, w: number, h: number, bdy: Box[], itr: Box[], opoint: Point[]
}

const seq = data as unknown as { frames: Frame[], ticks: number, tick_ms: number, end: { next: number, becomes: number } }
const frames = seq.frames
const starts: number[] = []
let acc = 0
for (const fr of frames) {
  starts.push(acc)
  acc += fr.ticks
}
const total = acc
const HOLD = 4 // timer steps that keep the final `next: 999` on screen before the loop restarts

const nav = useNav()
const active = useIsSlideActive()
const isPrint = computed(() => nav.isPrintMode.value)
const printIndex = Math.max(0, frames.findIndex(fr => fr.id === props.printFrame))
const printStep = starts[printIndex] + Math.min(Math.max(props.printTick, 1), frames[printIndex].ticks) - 1

const step = ref(isPrint.value ? printStep : 0)
const paused = ref(false)
const ended = computed(() => step.value >= total)
const t = computed(() => Math.min(step.value, total - 1))
const idx = computed(() => {
  let i = frames.length - 1
  while (i > 0 && starts[i] > t.value) i--
  return i
})
const f = computed(() => frames[idx.value])
const k = computed(() => t.value - starts[idx.value] + 1) // the frame counter after this tick's scheduler call
const leaving = computed(() => k.value > f.value.wait)

let timer: ReturnType<typeof setInterval> | undefined
function stop() {
  if (timer)
    clearInterval(timer)
  timer = undefined
}
function play() {
  stop()
  timer = setInterval(() => {
    step.value = (step.value + 1) % (total + HOLD)
  }, 1000 / props.tps)
}
watch([active, isPrint], ([a, p]) => {
  if (p) {
    stop()
    step.value = printStep
    return
  }
  if (a) {
    step.value = 0
    if (!paused.value)
      play()
  }
  else {
    stop()
  }
}, { immediate: true })
onBeforeUnmount(stop)

function toggle() {
  paused.value = !paused.value
  if (paused.value)
    stop()
  else if (active.value && !isPrint.value)
    play()
}
function jump(i: number) {
  step.value = starts[i]
}

const S = computed(() => props.scale)
const CELL = 79
const pad = 10
const stageW = computed(() => CELL * S.value + pad * 2)
const stageH = computed(() => CELL * S.value + pad + 24)
// The actor's position stays fixed on the stage; each frame's picture is drawn at -centerx/-centery from it.
const anchor = computed(() => ({ x: pad + 39 * S.value, y: pad + CELL * S.value }))
const spriteStyle = computed(() => ({
  left: `${anchor.value.x - f.value.centerx * S.value}px`,
  top: `${anchor.value.y - f.value.centery * S.value}px`,
  width: `${f.value.w * S.value}px`,
  height: `${f.value.h * S.value}px`,
}))

const onSprite = (b: Box, fr: Frame) => b.y > -200 && b.y < fr.h + 200
const offBdy = computed(() => f.value.bdy.filter(b => !onSprite(b, f.value)))
const offItr = computed(() => f.value.itr.filter(b => !onSprite(b, f.value)))
const fmt = new Intl.NumberFormat('ru-RU')
const itrNote = (b: Box) => {
  const parts: string[] = [`kind ${b.kind}`]
  if (b.injury !== undefined)
    parts.push(`урон ${b.injury}`)
  if (b.dvx !== undefined)
    parts.push(`dvx ${b.dvx}`)
  if (b.fall !== undefined)
    parts.push(`fall ${b.fall}`)
  return parts.join(' · ')
}
const bdyNote = computed(() => {
  const on = f.value.bdy.filter(b => onSprite(b, f.value))
  return on.map(b => `${b.x},${b.y} ${b.w}×${b.h}`).join(' · ')
})
const groups = computed(() => {
  const out: { name: string, span: number }[] = []
  for (const fr of frames) {
    const last = out[out.length - 1]
    if (last && last.name === fr.name)
      last.span++
    else out.push({ name: fr.name, span: 1 })
  }
  return out
})
const ms = computed(() => t.value * seq.tick_ms)
const slower = computed(() => Math.round(1000 / seq.tick_ms / props.tps))
</script>

<template>
  <div class="fp">
    <div class="top">
      <div class="left">
        <div class="stage" :style="{ width: `${stageW}px`, height: `${stageH}px` }">
          <div class="ground" :style="{ top: `${anchor.y}px` }" />
          <div class="sprite" :style="spriteStyle">
            <!-- fills sit under the picture so the sprite keeps its colours; outlines go on top -->
            <svg :viewBox="`0 0 ${f.w} ${f.h}`" class="overlay">
              <rect v-for="(b, i) in f.bdy.filter(b => onSprite(b, f))" :key="`bf${f.id}-${i}`" :x="b.x" :y="b.y" :width="b.w" :height="b.h" class="bdy fill" />
              <rect v-for="(b, i) in f.itr.filter(b => onSprite(b, f))" :key="`if${f.id}-${i}`" :x="b.x" :y="b.y" :width="b.w" :height="b.h" class="itr fill" />
            </svg>
            <img :src="f.image" class="pixelated" alt="">
            <svg :viewBox="`0 0 ${f.w} ${f.h}`" class="overlay">
              <rect v-for="(b, i) in f.bdy.filter(b => onSprite(b, f))" :key="`b${f.id}-${i}`" :x="b.x" :y="b.y" :width="b.w" :height="b.h" class="bdy line" />
              <rect v-for="(b, i) in f.itr.filter(b => onSprite(b, f))" :key="`i${f.id}-${i}`" :x="b.x" :y="b.y" :width="b.w" :height="b.h" class="itr line" />
              <g class="center">
                <line :x1="f.centerx - 3" :x2="f.centerx + 3" :y1="f.centery - 0.5" :y2="f.centery - 0.5" />
                <line :x1="f.centerx" :x2="f.centerx" :y1="f.centery - 4" :y2="f.centery" />
              </g>
            </svg>
          </div>
          <div class="speed">
            <span v-if="!isPrint" class="i-pixelarticons-speed-slow" />{{ isPrint ? 'стоп-кадр' : `замедлено ×${slower} · ${tps} тиков/с` }}
          </div>
          <button v-if="!isPrint" class="pp" :title="paused ? 'дальше' : 'пауза'" @click="toggle">
            <span v-if="paused" class="i-pixelarticons-play" />
            <span v-else class="i-pixelarticons-pause" />
          </button>
        </div>
        <div class="chips">
          <span v-for="(b, i) in offBdy" :key="`ob${f.id}-${i}`" class="chip bdyc">↓ bdy y: {{ fmt.format(b.y) }}</span>
          <span v-for="(b, i) in offItr" :key="`oi${f.id}-${i}`" class="chip itrc">↓ itr y: {{ fmt.format(b.y) }}</span>
        </div>
      </div>

      <div class="right">
        <div class="hud">
          <div class="hhead">
            <span class="fid pixel">frame {{ f.id }}</span>
            <span class="fname">{{ f.name }}</span>
            <span class="tick mono">тик <b>{{ t + 1 }}</b> / {{ total }} · {{ fmt.format(ms) }} мс</span>
          </div>
          <div class="rows">
            <div class="row">
              <span class="lab">state</span><span class="val">{{ f.state }}</span>
              <span class="lab">pic</span><span class="val">{{ f.pic }}</span>
              <span class="lab">dvx</span><span class="val">{{ f.dvx }}</span>
              <template v-if="f.mp !== null">
                <span class="lab">mp</span><span class="val">{{ f.mp }}</span>
              </template>
            </div>
            <div class="row">
              <span class="lab">wait</span><span class="val big">{{ f.wait }}</span>
              <span class="pips">
                <i v-for="n in f.ticks" :key="`p${f.id}-${n}`" :class="{ on: n <= k, now: n === k, last: n === f.ticks }" />
              </span>
              <span class="cmp mono" :class="{ go: leaving }">
                счётчик {{ k }} {{ leaving ? '>' : '≤' }} {{ f.wait }}<template v-if="leaving"> → next</template>
              </span>
            </div>
            <div class="row">
              <span class="lab">next</span>
              <span class="val nxt" :class="{ go: leaving }">
                → {{ f.next }}<template v-if="f.next === 999"> → {{ seq.end.becomes }} <span class="muted">(стойка)</span></template>
              </span>
            </div>
            <div class="row box" :class="{ lit: f.bdy.length }">
              <i class="sw bdyc" /><span class="lab">bdy</span>
              <span class="val sm">{{ bdyNote }}<template v-if="offBdy.length"> · ещё {{ offBdy.length }} под картинкой</template></span>
            </div>
            <div class="row box" :class="{ lit: f.itr.length }">
              <i class="sw itrc" /><span class="lab">itr</span>
              <span v-if="f.itr.length" class="val sm itrtxt">{{ f.itr.map(itrNote).join(' | ') }}</span>
              <span v-else class="val sm muted">нет — этим кадром не бьют</span>
            </div>
            <div class="row extra">
              <span class="val sm" :class="{ dim: !f.sound }"><span class="lab">sound</span> {{ f.sound ?? '—' }}</span>
              <span v-for="(o, i) in f.opoint" :key="`o${i}`" class="val sm"><span class="lab">opoint</span> oid {{ o.oid }} → {{ o.file }}</span>
            </div>
          </div>
        </div>
        <slot />
      </div>
    </div>

    <div class="strip">
      <div class="groups">
        <span v-for="(g, i) in groups" :key="i" class="grp mono" :style="{ flex: g.span }">{{ g.name }}</span>
        <span class="grp-end" />
      </div>
      <div class="cells">
        <button
          v-for="(fr, i) in frames" :key="fr.id" class="cell"
          :class="{ cur: i === idx && !ended, hit: fr.itr.length }" @click="jump(i)"
        >
          <img :src="fr.image" class="pixelated" alt="">
          <span class="cinfo">
            <span class="cid mono">{{ fr.id }}</span>
            <span class="cw mono">wait {{ fr.wait }}</span>
            <span class="cpips">
              <i v-for="n in fr.ticks" :key="n" :class="{ on: i < idx || (i === idx && n <= k) || ended }" />
            </span>
          </span>
        </button>
        <div class="endchip" :class="{ cur: ended }">
          <span class="mono">next 999</span>
          <span class="arrow">→ {{ seq.end.becomes }}</span>
          <span class="muted">стойка</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fp {
  --bdy: var(--s1);
  --itr: var(--naruto);
}
.top {
  display: flex;
  gap: 1.2rem;
  align-items: flex-start;
}
.left {
  flex: none;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.stage {
  position: relative;
  background:
    linear-gradient(45deg, rgba(255, 255, 255, 0.035) 25%, transparent 25%, transparent 75%, rgba(255, 255, 255, 0.035) 75%),
    linear-gradient(45deg, rgba(255, 255, 255, 0.035) 25%, transparent 25%, transparent 75%, rgba(255, 255, 255, 0.035) 75%);
  background-size: 12px 12px;
  background-position: 0 0, 6px 6px;
  border: 1px solid var(--hair);
  border-radius: 10px;
  overflow: hidden;
}
.ground {
  position: absolute;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--axis);
}
.sprite {
  position: absolute;
}
.sprite img {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
}
.overlay {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
}
.fill {
  stroke: none;
}
.bdy.fill {
  fill: color-mix(in srgb, var(--bdy) 26%, transparent);
}
.itr.fill {
  fill: color-mix(in srgb, var(--itr) 40%, transparent);
  animation: flash 0.45s ease-out;
}
.line {
  fill: none;
}
.bdy.line {
  stroke: var(--bdy);
  stroke-width: 0.7;
  filter: drop-shadow(0 0 1.5px var(--bdy));
}
.itr.line {
  fill: color-mix(in srgb, var(--itr) 12%, transparent);
  stroke: var(--itr);
  stroke-width: 0.8;
  filter: drop-shadow(0 0 2px var(--itr));
}
@keyframes flash {
  0% { fill: color-mix(in srgb, var(--itr) 90%, transparent); }
  100% { fill: color-mix(in srgb, var(--itr) 40%, transparent); }
}
.center line {
  stroke: var(--ink);
  stroke-width: 0.6;
}
.speed {
  position: absolute;
  left: 8px;
  bottom: 4px;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-family: var(--font-pixel);
  font-size: 0.6rem;
  color: var(--muted);
  letter-spacing: 0.02em;
}
.speed span {
  width: 0.85rem;
  height: 0.85rem;
}
.pp {
  position: absolute;
  right: 6px;
  bottom: 2px;
  width: 22px;
  height: 20px;
  display: grid;
  place-items: center;
  color: var(--ink-2);
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--hair);
  border-radius: 5px;
  cursor: pointer;
  padding: 0;
}
.pp span {
  width: 12px;
  height: 12px;
}
.chips {
  height: 1.15rem;
  margin-top: 0.3rem;
  display: flex;
  gap: 0.4rem;
}
.chip {
  font-family: var(--font-mono);
  font-size: 0.58rem;
  padding: 0.05rem 0.4rem;
  border-radius: 4px;
  white-space: nowrap;
  animation: pop 0.3s ease-out;
}
@keyframes pop {
  0% { opacity: 0; transform: translateY(-3px); }
  100% { opacity: 1; transform: none; }
}
.chip.bdyc {
  color: #9ec5f4;
  background: color-mix(in srgb, var(--bdy) 22%, transparent);
}
.chip.itrc {
  color: #ffc49f;
  background: color-mix(in srgb, var(--itr) 22%, transparent);
}
.right {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.hud {
  background: #0c1017;
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.55rem 0.8rem 0.6rem;
}
.hhead {
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
  padding-bottom: 0.4rem;
  margin-bottom: 0.35rem;
  border-bottom: 1px solid var(--grid);
}
.fid {
  font-size: 1.05rem;
  color: var(--naruto);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.fname {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--ink);
  font-weight: 600;
}
.tick {
  margin-left: auto;
  font-size: 0.66rem;
  color: var(--ink-2);
}
.tick b {
  color: var(--ink);
}
.rows {
  display: flex;
  flex-direction: column;
  gap: 0.28rem;
}
.row {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  min-height: 1.15rem;
}
.lab {
  font-family: var(--font-mono);
  font-size: 0.62rem;
  color: var(--muted);
  min-width: 2.1rem;
}
.val {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--ink);
  margin-right: 0.6rem;
}
.val.big {
  font-size: 0.9rem;
  font-weight: 700;
}
.val.sm {
  font-size: 0.66rem;
  color: var(--ink-2);
  margin-right: 0;
}
.pips {
  display: inline-flex;
  gap: 3px;
}
.pips i {
  width: 11px;
  height: 11px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.16);
}
.pips i.on {
  background: rgba(246, 243, 236, 0.55);
  border-color: transparent;
}
.pips i.now {
  background: var(--ink);
}
.pips i.last {
  outline: 1px dashed var(--naruto);
  outline-offset: 1px;
}
.cmp {
  font-size: 0.66rem;
  color: var(--ink-2);
  margin-left: 0.4rem;
}
.cmp.go,
.nxt.go {
  color: var(--naruto);
}
.box {
  opacity: 0.38;
  transition: opacity 0.2s;
}
.box.lit {
  opacity: 1;
}
.sw {
  display: inline-block;
  width: 12px;
  height: 9px;
  border-radius: 2px;
  flex: none;
}
.sw.bdyc {
  background: color-mix(in srgb, var(--bdy) 40%, transparent);
  outline: 1px solid var(--bdy);
}
.sw.itrc {
  background: color-mix(in srgb, var(--itr) 45%, transparent);
  outline: 1px solid var(--itr);
}
.box .lab {
  min-width: 1.6rem;
}
.itrtxt {
  color: #ffc49f;
}
.extra {
  gap: 1rem;
}
.extra .dim {
  opacity: 0.38;
}
.extra .lab {
  min-width: 0;
  margin-right: 0.25rem;
}
.strip {
  margin-top: 0.45rem;
}
.groups {
  display: flex;
  gap: 6px;
  margin-bottom: 3px;
}
.grp {
  font-size: 0.58rem;
  color: var(--muted);
  border-top: 1px solid var(--axis);
  padding-top: 1px;
  text-align: center;
}
.grp-end {
  flex: none;
  width: 92px;
}
.cells {
  display: flex;
  gap: 6px;
  align-items: stretch;
}
.cell {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 3px;
  padding: 2px 4px 2px 1px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--hair);
  border-radius: 8px;
  cursor: pointer;
  color: inherit;
  font: inherit;
  text-align: left;
  transition: border-color 0.15s, background 0.15s;
}
.cell img {
  flex: none;
  width: 42px;
  height: 42px;
}
.cinfo {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.cell.hit {
  box-shadow: inset 0 -2px 0 color-mix(in srgb, var(--itr) 80%, transparent);
}
.cell.cur {
  background: rgba(255, 138, 61, 0.1);
  border-color: var(--naruto);
  box-shadow: 0 0 12px rgba(255, 138, 61, 0.25);
}
.cell.cur.hit {
  box-shadow: 0 0 12px rgba(255, 138, 61, 0.25), inset 0 -2px 0 color-mix(in srgb, var(--itr) 80%, transparent);
}
.cid {
  font-size: 0.66rem;
  line-height: 1;
  color: var(--ink);
  font-weight: 600;
}
.cw {
  font-size: 0.56rem;
  line-height: 1;
  color: var(--muted);
  white-space: nowrap;
}
.cpips {
  display: flex;
  gap: 2px;
}
.cpips i {
  width: 5px;
  height: 5px;
  border-radius: 1px;
  background: rgba(255, 255, 255, 0.14);
}
.cpips i.on {
  background: var(--ink-2);
}
.cell.cur .cpips i.on {
  background: var(--naruto);
}
.endchip {
  flex: none;
  width: 92px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1px;
  border: 1px dashed var(--axis);
  border-radius: 8px;
  font-size: 0.62rem;
  color: var(--ink-2);
}
.endchip .arrow {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--ink);
}
.endchip.cur {
  border-color: var(--naruto);
  border-style: solid;
  background: rgba(255, 138, 61, 0.1);
}
</style>
