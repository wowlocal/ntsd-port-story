<script setup lang="ts">
import { computed } from 'vue'
import { useNav, useSlideContext } from '@slidev/client'

// Chapter 15: how "unchecked in shipping builds" (the user's answer of 8 Oct, 18:43) spread from the APK
// to every package of the 13 October release, step by step (4aa → 4ab → 4ac → 4ad → release).
// `stepwise` reveals one column per click (frontmatter `clicks: 4`); export and print show all five.
// States come from the commit bodies of 3d8935d, 7c02b7f, 0dd7740, 1035e40d, 5b8e5d02 and from
// release-refresh-20261013.json on 0b5d4621; the iOS app was left out of that release at the user's request.
type S = 'on' | 'opt' | 'off' | 'guard' | 'rel' | 'na'
const props = withDefaults(defineProps<{ stepwise?: boolean }>(), { stepwise: false })
const { $clicks } = useSlideContext()
const nav = useNav()
const shownCols = computed(() => (!props.stepwise || nav.isPrintMode.value) ? 5 : Math.min(5, ($clicks?.value ?? 0) + 1))

const cols = [
  { step: '4aa', when: '8 окт 19:48', hash: '3d8935d · 7c02b7f', note: 'флаг в Package.swift — только release и только с <code>NTSD_UNCHECKED_EXCLUSIVITY=1</code>; его ставит сборщик APK' },
  { step: '4ab', when: '8 окт 20:46', hash: '0dd7740', note: 'ревью 4aa: FreeType-текст в APK остался с проверками, хосты SDL и iOS не могли включить флаг' },
  { step: '4ac', when: '10 окт 18:02', hash: '1035e40d', note: '<code>build-native.sh</code> экспортирует флаг; 20 из 20 запусков чистые' },
  { step: '4ad', when: '10 окт 18:26', hash: '5b8e5d02', note: 'упаковщики Linux, Windows и iOS; их проверки — стенды, не приёмка на устройствах' },
  { step: 'релиз', when: '13 окт 15:22', hash: '0b5d4621', note: '«unchecked exclusivity as existing shipping policy»' },
]
const rows: { name: string, sub?: string, s: S[] }[] = [
  { name: 'APK Android', sub: 'наши модули', s: ['off', 'off', 'off', 'off', 'rel'] },
  { name: 'FreeType-текст', sub: 'модуль внутри APK', s: ['on', 'off', 'off', 'off', 'rel'] },
  { name: 'приложение macOS', s: ['on', 'on', 'off', 'off', 'rel'] },
  { name: 'пакет Linux', sub: 'хост SDL', s: ['on', 'opt', 'opt', 'off', 'rel'] },
  { name: 'пакет Windows', sub: 'хост SDL', s: ['on', 'opt', 'opt', 'off', 'rel'] },
  { name: 'приложение iOS', s: ['on', 'opt', 'opt', 'off', 'na'] },
  { name: 'тесты и ворота', sub: 'бинарники проверок', s: ['guard', 'guard', 'guard', 'guard', 'guard'] },
]
const label: Record<S, string> = { on: 'с проверками', opt: 'флаг доступен', off: 'без проверок', guard: 'с проверками + сторож', rel: 'без проверок', na: 'не в релизе' }
const changed = (r: S[], i: number) => i > 0 && r[i] !== r[i - 1] && r[i] !== 'rel' && r[i] !== 'na'
</script>

<template>
  <div class="xm">
    <div class="hdr" />
    <div v-for="(c, i) in cols" :key="c.step" class="hdr col" :class="{ hidden: i >= shownCols, last: i === 4 }">
      <span class="pixel st">{{ c.step }}</span>
      <span class="mono wh">{{ c.when }}</span>
      <span class="mono hs">{{ c.hash }}</span>
    </div>

    <template v-for="r in rows" :key="r.name">
      <div class="rn">
        <b>{{ r.name }}</b><span v-if="r.sub">{{ r.sub }}</span>
      </div>
      <div v-for="(st, i) in r.s" :key="i" class="cell" :class="[st, { hidden: i >= shownCols, nw: changed(r.s, i) }]">
        <span v-if="st === 'off' || st === 'rel'" class="i-pixelarticons-shield-off ic" />
        <span v-else-if="st === 'on' || st === 'guard'" class="i-pixelarticons-shield ic" />
        <span>{{ label[st] }}</span>
      </div>
    </template>

    <div class="rn notes">что сделано</div>
    <div v-for="(c, i) in cols" :key="`n${c.step}`" class="note" :class="{ hidden: i >= shownCols }" v-html="c.note" />
  </div>
</template>

<style scoped>
.xm { display: grid; grid-template-columns: 7.6rem repeat(5, minmax(0, 1fr)); gap: 3px 6px; align-items: stretch; }
.hdr { display: flex; flex-direction: column; gap: 0; padding: 0 .1rem .15rem; border-bottom: 1px solid var(--axis); }
.hdr .st { font-size: .86rem; color: var(--naruto); line-height: 1.1; }
.hdr.last .st { color: var(--ink); }
.hdr .wh { font-size: .56rem; color: var(--ink-2); }
.hdr .hs { font-size: .5rem; color: var(--muted); }
.rn { display: flex; flex-direction: column; justify-content: center; line-height: 1.15; }
.rn b { font-size: .64rem; color: var(--ink); font-weight: 600; }
.rn span { font-size: .5rem; color: var(--muted); }
.cell { display: flex; align-items: center; gap: .3rem; font-size: .58rem; line-height: 1.15; border-radius: 6px; padding: .13rem .4rem; border: 1px solid var(--hair); color: var(--ink-2); background: rgba(255,255,255,.02); transition: opacity .35s ease, transform .35s ease; }
.cell .ic { width: .78rem; height: .78rem; flex: none; }
.cell.on { color: var(--ink-2); }
.cell.on .ic { color: var(--muted); }
.cell.opt { border-style: dashed; border-color: rgba(250,178,25,.55); color: var(--ink-2); }
.cell.off { background: rgba(217,89,38,.22); border-color: rgba(217,89,38,.55); color: var(--ink); }
.cell.off .ic { color: var(--naruto); }
.cell.rel { background: var(--s2); border-color: var(--s2); color: #fff; font-weight: 600; }
.cell.rel .ic { color: #fff; }
.cell.guard { border-color: rgba(12,163,12,.55); background: rgba(12,163,12,.08); color: var(--ink); }
.cell.guard .ic { color: var(--good); }
.cell.na { color: var(--muted); border-style: dotted; }
.cell.nw { box-shadow: 0 0 0 1.5px var(--naruto), 0 0 14px rgba(255,138,61,.35); }
.notes { font-size: .52rem; color: var(--muted); font-family: var(--font-pixel); justify-content: flex-start; padding-top: .2rem; }
.note { font-size: .54rem; line-height: 1.3; color: var(--ink-2); padding: .2rem .1rem 0; border-top: 1px dashed var(--axis); transition: opacity .35s ease; }
.note :deep(code) { font-size: .5rem !important; padding: 0 .2em; }
.hidden { opacity: 0; transform: translateY(6px); }
</style>
