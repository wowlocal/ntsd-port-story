<script setup lang="ts">
// Where the macOS build's live heap went on 5 Oct (malloc_history at the peak of a VS run), as one bar in MiB,
// against the phone's whole RAM. The three copies of each image (file bytes, decoded colours, surface pixels)
// and the per-pixel "known" mask carry the one accent; everything else is neutral.
// Data: data/perf_memory.json (scripts/collect_perf.py).
import { useNav, useSlideContext } from '@slidev/client'
import data from '../data/perf_memory.json'

const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const shown = (k: number) => !props.stepwise || nav.isPrintMode.value || ($clicks?.value ?? 0) >= k

const W = 884
const H = 132
const barY = 30
const barH = 36
const total = (data as any).liveHeapMiB as number
const ram = (data as any).phone.memTotalMiB as number
const x = (v: number) => (v / total) * W
const nf = new Intl.NumberFormat('ru-RU')
const GAP = 2

const order = ['filebytes', 'decoded', 'surface', 'known', 'records', 'frames', 'sounds', 'startup', 'other']
const inside: Record<string, string> = { filebytes: '1-я копия', decoded: '2-я копия', surface: '3-я копия', known: 'маска' }
const under: Record<string, string> = { filebytes: 'байты файлов картинок', decoded: 'декодированные цвета', surface: 'пиксели 851 поверхности', known: 'байт на пиксель' }
const byId = Object.fromEntries((data as any).holders.map((h: any) => [h.id, h]))
let acc = 0
const segs = order.map((id) => {
  const h = byId[id]
  const s = { ...h, x0: x(acc), x1: x(acc + h.MiB) }
  acc += h.MiB
  return s
})
const img = segs.filter(s => s.image)
const rest = segs.filter(s => !s.image)
const imgMiB = img.reduce((a, s) => a + s.MiB, 0)
const restMiB = rest.reduce((a, s) => a + s.MiB, 0)
const imgEnd = img[img.length - 1].x1
const restMid = (rest[0].x0 + W) / 2
const pct = Math.round((imgMiB / total) * 100)
const ramX = x(ram)
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`Живая куча ${nf.format(total)} МиБ: копии картинок ${nf.format(imgMiB)} МиБ; вся память телефона ${nf.format(ram)} МиБ`">
    <!-- bracket over the image copies -->
    <path :d="`M1,${barY - 6} V${barY - 12} H${imgEnd - 1} V${barY - 6}`" fill="none" stroke="var(--naruto)" stroke-width="1.2" />
    <text :x="imgEnd / 2" :y="barY - 17" text-anchor="middle" class="brk">одна и та же картинка — три копии и маска: <tspan class="v">{{ nf.format(imgMiB) }} МиБ, {{ pct }} % кучи</tspan></text>

    <!-- the bar -->
    <g v-for="s in segs" :key="s.id">
      <title>{{ s.label }}: {{ nf.format(s.MiB) }} МиБ</title>
      <rect :x="s.x0" :y="barY" :width="Math.max(1, s.x1 - s.x0 - GAP)" :height="barH" :rx="3" :fill="s.image ? 'var(--s2)' : 'var(--axis)'" />
      <text v-if="inside[s.id]" :x="(s.x0 + s.x1 - GAP) / 2" :y="barY + barH / 2 + 4" text-anchor="middle" class="in">{{ inside[s.id] }}</text>
    </g>

    <!-- labels under the image copies -->
    <g v-for="s in img" :key="`l${s.id}`">
      <text :x="(s.x0 + s.x1 - GAP) / 2" :y="barY + barH + 17" text-anchor="middle" class="val">{{ nf.format(s.MiB) }} МиБ</text>
      <text :x="(s.x0 + s.x1 - GAP) / 2" :y="barY + barH + 31" text-anchor="middle" class="nm">{{ under[s.id] }}</text>
    </g>
    <text :x="restMid" :y="barY + barH + 17" text-anchor="middle" class="val">{{ nf.format(restMiB) }} МиБ</text>
    <text :x="restMid" :y="barY + barH + 31" text-anchor="middle" class="nm">остальное</text>

    <!-- the phone's whole RAM -->
    <g :class="{ off: !shown(1) }" class="ram">
      <line :x1="ramX" :x2="ramX" :y1="barY - 4" :y2="H - 4" stroke="var(--ink)" stroke-width="1.6" />
      <circle :cx="ramX" :cy="barY - 4" r="3" fill="var(--ink)" />
      <text :x="ramX - 7" :y="H - 7" text-anchor="end" class="ramt">вся память телефона, MemTotal: <tspan class="v">{{ nf.format(ram) }} МиБ</tspan></text>
    </g>
  </svg>
</template>

<style scoped>
.brk {
  font-size: 11.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.brk .v,
.ramt .v {
  fill: var(--ink);
  font-weight: 650;
}
.in {
  font-size: 11px;
  font-weight: 650;
  fill: #fff;
  font-family: var(--font-sans);
}
.val {
  font-size: 12px;
  font-weight: 650;
  fill: var(--ink);
  font-family: var(--font-sans);
  font-variant-numeric: tabular-nums;
}
.nm {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.ramt {
  font-size: 11px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.ram {
  transition: opacity 0.4s ease;
}
.off {
  opacity: 0;
}
</style>
