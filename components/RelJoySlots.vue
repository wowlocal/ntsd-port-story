<script setup lang="ts">
// Chapter 18, PHONE_CONTROLLER C3: which Android input devices become the original's two joysticks.
// Before C3 the probe took the first two SOURCE_GAMEPAD devices, so the Kishi V2's button-only interface 2
// took joystick 2; after C3 a gamepad without joystick axes is skipped when a device with axes has the same
// vendor and product. The "second gamepad" switch is the card's inference from the probe code, not a test.
// Data: data/rel_controller.json (scripts/collect_release.py).
import { computed, ref } from 'vue'
import { useNav } from '@slidev/client'
import ctl from '../data/rel_controller.json'

const c = ctl as any
const nav = useNav()
const userSecond = ref<boolean | null>(null)
const second = computed(() => userSecond.value ?? nav.isPrintMode.value)
const vid = `${c.device.vendor.replace('0x', '')}:${c.device.product.replace('0x', '')}`

interface Dev { key: string, name: string, sub: string, axes: boolean, ghost?: boolean }
const devs = computed<Dev[]>(() => [
  { key: 'k0', name: `id 4 · Kishi V2, интерфейс 0`, sub: `${vid} · GAMEPAD | JOYSTICK · оси`, axes: true },
  { key: 'k2', name: `id 5 · Kishi V2, интерфейс 2`, sub: `${vid} · GAMEPAD · без осей`, axes: false },
  ...(second.value ? [{ key: 'g2', name: 'второй геймпад', sub: 'подключён позже', axes: true, ghost: true }] : []),
])
function slots(after: boolean) {
  const usable = devs.value.filter(d => !after || d.axes || d.key !== 'k2')
  return [usable[0]?.key ?? null, usable[1]?.key ?? null]
}
const panels = computed(() => [
  { id: 'before', title: 'до C3', hash: 'd4619cbc', s: slots(false) },
  { id: 'after', title: 'после C3', hash: '5f5a8ee4', s: slots(true) },
])
const W = 430
const H = 128
const dy = (i: number) => 22 + i * 36
const sy = (i: number) => 34 + i * 44
const label = (k: string | null) => devs.value.find(d => d.key === k)
</script>

<template>
  <div class="js">
    <label class="sw">
      <input type="checkbox" :checked="second" @change="userSecond = ($event.target as HTMLInputElement).checked">
      <span>подключить второй геймпад <i class="muted">(вывод карточки из кода, не проверялось)</i></span>
    </label>
    <div class="row">
      <div v-for="p in panels" :key="p.id" class="pan">
        <div class="ph"><b>{{ p.title }}</b> <code>{{ p.hash }}</code></div>
        <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" :aria-label="`${p.title}: джойстик 1 — ${label(p.s[0])?.name ?? 'пусто'}, джойстик 2 — ${label(p.s[1])?.name ?? 'пусто'}`">
          <g v-for="(d, i) in devs" :key="d.key">
            <rect x="0" :y="dy(i) - 14" width="222" height="30" rx="7" :class="['dev', { ghost: d.ghost, skip: p.id === 'after' && d.key === 'k2', lost: !p.s.includes(d.key) && p.id === 'before' }]" />
            <text class="dn" x="9" :y="dy(i) - 1">{{ d.name }}</text>
            <text class="ds" x="9" :y="dy(i) + 11">{{ d.sub }}</text>
            <text v-if="p.id === 'after' && d.key === 'k2'" class="tag" x="214" :y="dy(i) + 11" text-anchor="end">пропущен</text>
            <text v-if="p.id === 'before' && d.ghost" class="tag warn" x="214" :y="dy(i) + 11" text-anchor="end">слота нет</text>
          </g>
          <g v-for="(k, j) in p.s" :key="`s${j}`">
            <rect x="290" :y="sy(j) - 15" width="140" height="30" rx="7" class="slot" :class="{ empty: !k, bad: k === 'k2' }" />
            <text class="dn" x="299" :y="sy(j) - 1">джойстик {{ j + 1 }}</text>
            <text class="ds" x="299" :y="sy(j) + 11">{{ k === 'k2' ? 'не двигается, не жмётся' : k ? (k === 'k0' ? 'игрок 3 по умолчанию' : 'игрок 4 по умолчанию') : 'свободен' }}</text>
            <path v-if="k" :d="`M222,${dy(devs.findIndex(d => d.key === k))} C256,${dy(devs.findIndex(d => d.key === k))} 256,${sy(j)} 290,${sy(j)}`" class="lnk" :class="{ bad: k === 'k2' }" />
          </g>
        </svg>
      </div>
    </div>
  </div>
</template>

<style scoped>
.js { display: flex; flex-direction: column; gap: 3px; }
.sw { display: inline-flex; align-items: center; gap: 6px; font-size: 0.66rem; color: var(--ink-2); cursor: pointer; }
.sw input { accent-color: var(--naruto); }
.sw i { font-style: normal; }
.row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.pan { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: 5px 9px 4px; }
.ph { font-size: 0.7rem; color: var(--ink-2); margin-bottom: 1px; }
.ph b { color: var(--ink); }
.ph code { font-size: 0.6rem !important; }
.dev { fill: var(--surface-2); stroke: var(--axis); }
.dev.ghost { fill: rgba(57, 135, 229, 0.12); stroke: var(--s1); stroke-dasharray: 4 3; }
.dev.skip { fill: transparent; stroke: var(--axis); stroke-dasharray: 3 3; }
.dev.lost { stroke: var(--warning); }
.slot { fill: var(--surface-3); stroke: var(--s2); }
.slot.empty { fill: transparent; stroke: var(--axis); stroke-dasharray: 3 3; }
.slot.bad { stroke: var(--warning); }
.dn { font-size: 10.5px; fill: var(--ink); font-family: var(--font-sans); font-weight: 600; }
.ds { font-size: 10px; fill: var(--ink-2); font-family: var(--font-sans); }
.tag { font-size: 10px; fill: var(--muted); font-family: var(--font-sans); }
.tag.warn { fill: var(--warning); }
.lnk { fill: none; stroke: var(--s2); stroke-width: 2; }
.lnk.bad { stroke: var(--warning); }
</style>
