<script setup lang="ts">
import { computed, ref } from 'vue'
import { useNav } from '@slidev/client'

// Chapter 13: five places where a new host answered the core differently from Windows,
// on the 30-hour strip of the loop (3 Oct 20:11 → 5 Oct 02:23). Hover a card or a marker to pair them.
// Facts are from the commit bodies, OriginalRuntimeTouchMouse.swift (edccfde) and crossplatform-p7-music-20261004.json.
interface Quirk { id: string, at: string, label: string, host: string, tone: string, symptom: string, cause: string, fix: string }

const quirks: Quirk[] = [
  {
    id: '503af05', at: '2026-10-03T21:42', label: '3 окт 21:42', host: 'Linux · тесты', tone: 's7',
    symptom: 'Четыре теста не находят родительский случай — только на Linux.',
    cause: '<code>NSDictionary.isEqual</code> на Darwin считает JSON <code>true</code> равным <code>1</code>, swift-corelibs-foundation — нет.',
    fix: '<code>sameJSONObject</code> даёт ответ Darwin везде — на 18 случаях JSON.',
  },
  {
    id: '7c504a6', at: '2026-10-04T09:46', label: '4 окт 09:46', host: 'Linux aarch64 · музыка', tone: 's4',
    symptom: 'Первый же прогон: <code>corrupt("packet at 8192")</code>, музыки нет.',
    cause: 'Декодер ALAC от Apple взят без изменений и узнаёт порядок байт из заголовков Apple или макросов x86.',
    fix: '<code>TARGET_RT_LITTLE_ENDIAN=1</code> для не-Apple целей. Каждый трек — ровно PCM из манифеста.',
  },
  {
    id: 'db3e341', at: '2026-10-04T20:51', label: '4 окт 20:51', host: 'Linux · Wayland', tone: 's3',
    symptom: 'Под Weston вся сцена сдвинута на отступ окна.',
    cause: 'Wayland не сообщает программам позицию их окна.',
    fix: 'Хост SDL сам говорит игре, куда поставил окно; VS равен остальным Linux.',
  },
  {
    id: '9d63735', at: '2026-10-04T22:15', label: '4 окт 22:15', host: 'iPad · клавиши', tone: 's1',
    symptom: 'После переключателя приложений игра видит клавишу зажатой.',
    cause: 'iPadOS отменяет нажатия, которые забирает себе, — отпускания не приходит.',
    fix: 'Отмена нажатия — это отпускание.',
  },
]

const t0 = Date.parse('2026-10-03T20:11')
const t1 = Date.parse('2026-10-05T02:23')
const x = (iso: string) => ((Date.parse(iso) - t0) / (t1 - t0)) * 100
const marks = [...quirks.map(q => ({ id: q.id, at: q.at, tone: q.tone })), { id: 'edccfde', at: '2026-10-04T22:43', tone: 's1' }]
const ticks = [
  { at: '2026-10-04T00:00', label: '4 окт' },
  { at: '2026-10-04T12:00', label: '12:00' },
  { at: '2026-10-05T00:00', label: '5 окт' },
]

const nav = useNav()
const hot = ref<string | null>(null)
const isHot = (id: string) => !nav.isPrintMode.value && hot.value === id
const dim = computed(() => !nav.isPrintMode.value && hot.value !== null)
</script>

<template>
  <div class="hq">
    <div class="strip">
      <span class="end l mono">3 окт 20:11</span>
      <div class="axis">
        <i class="line" />
        <span v-for="t in ticks" :key="t.at" class="tick" :style="{ left: `${x(t.at)}%` }"><b class="mono">{{ t.label }}</b></span>
        <span
          v-for="m in marks" :key="m.id" class="mk" :class="{ on: isHot(m.id), off: dim && !isHot(m.id) }"
          :style="{ left: `${x(m.at)}%`, '--tone': `var(--${m.tone})` }"
          @mouseenter="hot = m.id" @mouseleave="hot = null"
        />
      </div>
      <span class="end r mono">5 окт 02:23 · 30 часов</span>
    </div>

    <div class="body">
      <div class="feat" :class="{ on: isHot('edccfde'), off: dim && !isHot('edccfde') }" style="--tone: var(--s1)" @mouseenter="hot = 'edccfde'" @mouseleave="hot = null">
        <div class="hd"><span class="host">iPad · касания</span><span class="mono when">4 окт 22:43 · edccfde</span></div>
        <div class="row"><b>симптом</b><span>Тап по пункту меню ничего не выбирает.</span></div>
        <div class="row"><b>причина</b><span>Хост отдавал курсор в 0,0 и присылал нажатие с отпусканием разом. А оригинал берёт пункт <i>под курсором</i> и читает кнопку на протяжении нескольких тиков: его же скриптовые клики держат её 10–15 итераций цикла.</span></div>

        <svg class="tap" viewBox="0 0 400 104" role="img" aria-label="Тап до и после правки: курсор, нажатие через 80 мс, отпускание не раньше чем через 150 мс после нажатия">
          <text x="0" y="20" class="ln">было</text>
          <line x1="52" y1="16" x2="392" y2="16" class="rail" />
          <rect x="52" y="9" width="3" height="14" class="hit bad" />
          <text x="60" y="13" class="ev">0x201 + 0x202 разом</text>
          <text x="60" y="25" class="ev dim">курсор 0,0</text>

          <text x="0" y="62" class="ln">стало</text>
          <line x1="52" y1="58" x2="392" y2="58" class="rail" />
          <circle cx="54" cy="58" r="3.5" class="mv" />
          <rect x="122" y="51" width="128" height="14" rx="3" class="held" />
          <text x="186" y="61.5" class="ev in">кнопка держится</text>
          <text x="54" y="45" class="ev">0x200 · курсор под пальцем</text>
          <text x="122" y="79" class="ev">0x201</text>
          <text x="250" y="79" class="ev">0x202</text>
          <line x1="54" y1="86" x2="250" y2="86" class="dim-axis" />
          <line x1="54" y1="83" x2="54" y2="89" class="dim-axis" />
          <line x1="122" y1="83" x2="122" y2="89" class="dim-axis" />
          <line x1="250" y1="83" x2="250" y2="89" class="dim-axis" />
          <text x="88" y="99" class="ms">80 мс</text>
          <text x="186" y="99" class="ms">≥ 150 мс</text>
        </svg>

        <div class="row"><b>правка</b><span>Общий помощник <code>OriginalRuntimeTouchMouse</code> для хостов без мыши ведёт касание как клик игрока.</span></div>
      </div>

      <div class="grid4">
        <div
          v-for="q in quirks" :key="q.id" class="qc" :class="{ on: isHot(q.id), off: dim && !isHot(q.id) }"
          :style="{ '--tone': `var(--${q.tone})` }" @mouseenter="hot = q.id" @mouseleave="hot = null"
        >
          <div class="hd"><span class="host">{{ q.host }}</span><span class="mono when">{{ q.label }} · {{ q.id }}</span></div>
          <div class="row"><b>симптом</b><span v-html="q.symptom" /></div>
          <div class="row"><b>причина</b><span v-html="q.cause" /></div>
          <div class="row fx"><b>правка</b><span v-html="q.fix" /></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.strip { display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: .6rem; margin-bottom: .45rem; }
.end { font-size: .56rem; color: var(--muted); white-space: nowrap; }
.axis { position: relative; height: 22px; }
.line { position: absolute; left: 0; right: 0; top: 10px; height: 2px; background: var(--axis); }
.tick { position: absolute; top: 4px; width: 1px; height: 14px; background: var(--grid); }
.tick b { position: absolute; top: -9px; left: 3px; font-size: .5rem; font-weight: 400; color: var(--muted); white-space: nowrap; }
.mk { position: absolute; top: 4px; width: 14px; height: 14px; margin-left: -7px; border-radius: 3px; background: var(--tone); box-shadow: 2px 2px 0 rgba(0,0,0,.45); cursor: default; transition: transform .2s, opacity .2s; }
.mk.on { transform: scale(1.35); }
.mk.off { opacity: .3; }

.body { display: grid; grid-template-columns: 1.02fr 1.45fr; gap: .6rem; }
.feat, .qc { background: var(--surface); border: 1px solid var(--hair); border-left: 3px solid var(--tone); border-radius: 10px; transition: opacity .2s, border-color .2s; }
.feat { padding: .45rem .7rem .5rem; display: flex; flex-direction: column; gap: .2rem; }
.qc { padding: .35rem .6rem .4rem; display: flex; flex-direction: column; gap: .12rem; }
.on { border-color: var(--tone); }
.off { opacity: .45; }
.grid4 { display: grid; grid-template-columns: 1fr 1fr; gap: .4rem; }
.hd { display: flex; justify-content: space-between; align-items: baseline; gap: .4rem; margin-bottom: .05rem; }
.host { font-family: var(--font-pixel); font-size: .74rem; color: var(--tone); white-space: nowrap; }
.when { font-size: .52rem; color: var(--muted); white-space: nowrap; }
.row { display: grid; grid-template-columns: 3.1rem 1fr; gap: .3rem; font-size: .6rem; line-height: 1.32; color: var(--ink-2); }
.row b { font-family: var(--font-pixel); font-weight: 400; font-size: .56rem; color: var(--muted); padding-top: .05rem; }
.row.fx span { color: var(--ink); }
.feat .row { font-size: .64rem; }
.feat .row:last-child span { color: var(--ink); }
.row :deep(code), .row code { font-size: .56rem !important; padding: 0 .25em; }
.row i { font-style: normal; color: var(--ink); }

.tap { width: 100%; height: auto; margin: .15rem 0 .1rem; }
.tap .ln { font-family: var(--font-pixel); font-size: 10px; fill: var(--muted); }
.tap .rail { stroke: var(--axis); stroke-width: 1.5; }
.tap .hit.bad { fill: var(--critical); }
.tap .ev { font-family: var(--font-mono); font-size: 8.5px; fill: var(--ink-2); }
.tap .ev.dim { fill: var(--muted); }
.tap .ev.in { fill: var(--bg); text-anchor: middle; font-family: var(--font-sans); font-weight: 600; }
.tap .mv { fill: var(--s1); }
.tap .held { fill: var(--s1); }
.tap .dim-axis { stroke: var(--muted); stroke-width: 1; }
.tap .ms { font-family: var(--font-mono); font-size: 8.5px; fill: var(--ink); text-anchor: middle; }
</style>
