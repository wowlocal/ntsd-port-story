<script setup lang="ts">
import { computed } from 'vue'
import data from '../data/engine_frames.json'

// Original sprite cells with the boxes the engine reads from the same DAT frame.
const props = withDefaults(defineProps<{ ids?: number[], scale?: number }>(), { ids: () => [0, 63, 72, 258], scale: 2.5 })
interface Box { kind?: number, x: number, y: number, w: number, h: number, [k: string]: number | undefined }
interface Frame { id: number, name: string, pic: number, state: number, centerx: number, centery: number, image: string, w: number, h: number, bdy: Box[], itr: Box[], wpoint: Box[], cpoint: Box[] }
const frames = computed(() => (data as any).frames.filter((f: Frame) => props.ids.includes(f.id)) as Frame[])
const onSprite = (b: Box, f: Frame) => b.y > -200 && b.y < f.h + 200
const off = (list: Box[], f: Frame) => list.filter(b => !onSprite(b, f))
const fmt = new Intl.NumberFormat('ru-RU')
const itrNote = (b: Box) => {
  const parts: string[] = [`kind ${b.kind}`]
  if (b.injury !== undefined) parts.push(`урон ${b.injury}`)
  if (b.dvx !== undefined) parts.push(`dvx ${b.dvx}`)
  if (b.fall !== undefined) parts.push(`fall ${b.fall}`)
  return parts.join(' · ')
}
</script>

<template>
  <div class="row" :style="{ gridTemplateColumns: `repeat(${frames.length}, 1fr)` }">
    <div v-for="f in frames" :key="f.id" class="cell">
      <div class="stage" :style="{ width: `${f.w * scale}px`, height: `${f.h * scale}px` }">
        <img :src="f.image" class="pixelated" :style="{ width: `${f.w * scale}px`, height: `${f.h * scale}px` }" alt="">
        <svg :viewBox="`0 0 ${f.w} ${f.h}`" class="overlay">
          <rect v-for="(b, i) in f.bdy.filter(b => onSprite(b, f))" :key="`b${i}`" :x="b.x" :y="b.y" :width="b.w" :height="b.h" class="bdy" />
          <rect v-for="(b, i) in f.itr.filter(b => onSprite(b, f))" :key="`i${i}`" :x="b.x" :y="b.y" :width="b.w" :height="b.h" class="itr" />
          <g v-for="(p, i) in f.wpoint.filter(p => onSprite(p, f))" :key="`w${i}`">
            <circle :cx="p.x" :cy="p.y" r="1.6" class="wpt" />
          </g>
          <g class="center">
            <line :x1="f.centerx - 3" :x2="f.centerx + 3" :y1="f.centery - 0.5" :y2="f.centery - 0.5" />
            <line :x1="f.centerx" :x2="f.centerx" :y1="f.centery - 4" :y2="f.centery" />
          </g>
        </svg>
        <div v-if="off(f.bdy, f).length || off(f.itr, f).length" class="below">
          <span v-for="(b, i) in off(f.bdy, f)" :key="`ob${i}`" class="ghost bdyc">↓ bdy y: {{ fmt.format(b.y) }}</span>
          <span v-for="(b, i) in off(f.itr, f)" :key="`oi${i}`" class="ghost itrc">↓ itr y: {{ fmt.format(b.y) }}</span>
        </div>
      </div>
      <div class="cap">
        <div class="ttl">
          <span class="mono">frame {{ f.id }}</span> · {{ f.name }}
        </div>
        <div class="sub mono">
          pic {{ f.pic }} · state {{ f.state }}
        </div>
        <div v-for="(b, i) in f.itr.filter(b => onSprite(b, f))" :key="`n${i}`" class="sub itrtxt">
          itr {{ itrNote(b) }}
        </div>
      </div>
    </div>
  </div>
  <div class="legend">
    <span><i class="sw bdyc" />bdy — тело: сюда можно попасть</span>
    <span><i class="sw itrc" />itr — удар или захват: этим бьют</span>
    <span><i class="sw wptc" />wpoint — где держится оружие</span>
    <span><i class="cross">┴</i>centerx / centery — точка опоры</span>
  </div>
</template>

<style scoped>
.row {
  display: grid;
  gap: 1rem;
  align-items: end;
}
.cell {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.stage {
  position: relative;
  background:
    linear-gradient(45deg, rgba(255, 255, 255, 0.04) 25%, transparent 25%, transparent 75%, rgba(255, 255, 255, 0.04) 75%),
    linear-gradient(45deg, rgba(255, 255, 255, 0.04) 25%, transparent 25%, transparent 75%, rgba(255, 255, 255, 0.04) 75%);
  background-size: 10px 10px;
  background-position: 0 0, 5px 5px;
  border: 1px solid var(--hair);
  border-radius: 6px;
}
.stage img {
  display: block;
}
.overlay {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
}
.bdy {
  fill: rgba(57, 135, 229, 0.18);
  stroke: #6da7ec;
  stroke-width: 0.6;
}
.itr {
  fill: rgba(217, 89, 38, 0.3);
  stroke: #ff8a3d;
  stroke-width: 0.6;
}
.wpt {
  fill: #199e70;
  stroke: #0a0d13;
  stroke-width: 0.5;
}
.center line {
  stroke: #f6f3ec;
  stroke-width: 0.6;
}
.below {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -1.3rem;
  display: flex;
  justify-content: center;
  gap: 0.4rem;
}
.ghost {
  font-family: var(--font-mono);
  font-size: 0.55rem;
  padding: 0 0.3rem;
  border-radius: 4px;
  white-space: nowrap;
}
.ghost.bdyc {
  color: #9ec5f4;
  background: rgba(57, 135, 229, 0.18);
}
.ghost.itrc {
  color: #ffc49f;
  background: rgba(217, 89, 38, 0.22);
}
.cap {
  margin-top: 1.55rem;
  text-align: center;
}
.ttl {
  font-size: 0.74rem;
  color: var(--ink);
  font-weight: 600;
}
.sub {
  font-size: 0.6rem;
  color: var(--muted);
}
.itrtxt {
  color: #ffc49f;
}
.legend {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.3rem 1.3rem;
  font-size: 0.66rem;
  color: var(--ink-2);
  margin-top: 0.6rem;
}
.sw {
  display: inline-block;
  width: 12px;
  height: 9px;
  border-radius: 2px;
  margin-right: 0.35rem;
  vertical-align: -1px;
}
.sw.bdyc {
  background: rgba(57, 135, 229, 0.35);
  outline: 1px solid #6da7ec;
}
.sw.itrc {
  background: rgba(217, 89, 38, 0.45);
  outline: 1px solid #ff8a3d;
}
.sw.wptc {
  background: #199e70;
  border-radius: 50%;
  width: 9px;
}
.cross {
  font-style: normal;
  margin-right: 0.35rem;
  color: var(--ink);
}
</style>
