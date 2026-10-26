<script setup lang="ts">
// Demo-day deck, results: three plain pictures instead of a row of figures.
// 1. The same match in two programs: the Summary the Mac app wrote, played back by the original under CrossOver
//    (public/img/screens/15-summary-mac-vs-original-side-by-side.jpg); 58 of 58 whole matches equal
//    (data/evidence/crossplay-matches.json), 18,088 frames equal on every host (chapter 17).
// 2. The Galaxy A12 before and after, as fractions of what the game needs:
//    speed — 5.4 ticks/s at the first finished match (5 Oct, chapter 14) against the original's 30; 30.25 with the real
//    clock after the redesign, with the main thread at 11.1 ms per tick (room for 60 fps);
//    memory — the game first needed ≈ 4 GB against the phone's 2.8 GB (chapter 14); the loading-night peak ended at
//    565 MiB (chapter 16);
//    menu — 131.9 → 12.7 s from the icon (chapter 16, typical run).
const ram = 2.8
const rows = [
  { k: 'speed', title: 'скорость игры', unit: 'тиков в секунду', cap: 30, capLabel: 'нужно 30 — темп оригинала', before: 5.4, after: 30.25, bLabel: '5,4 — замедленная съёмка', aLabel: '30 — как в оригинале, с запасом на 60 кадров/с', max: 30 },
  { k: 'mem', title: 'память', unit: 'ГБ', cap: ram, capLabel: 'в телефоне 2,8 ГБ', before: 4, after: 0.565, bLabel: '4 ГБ — не влезает, игра падает', aLabel: '0,57 ГБ в пике', max: 4.2 },
  { k: 'load', title: 'от иконки до меню', unit: 'секунд', cap: 0, capLabel: '', before: 131.9, after: 12.7, bLabel: '2 мин 12 с', aLabel: '13 с', max: 132 },
]
const pct = (v: number, max: number) => `${Math.min(100, (v / max) * 100)}%`
</script>

<template>
  <div class="rs">
    <div class="col">
      <div class="h pixel">совпадает с оригиналом</div>
      <div class="img">
        <img src="/img/screens/15-summary-mac-vs-original-side-by-side.jpg" alt="Таблица итогов одного матча: слева Mac, справа оригинал">
        <span class="l">Mac</span><span class="r">оригинал</span>
      </div>
      <div class="big"><b>58 из 58</b> матчей</div>
      <div class="cap">запись матча с Mac проигрывается в оригинальной игре — таблица итогов та же до последней цифры</div>
      <div class="cap2"><b>18 088</b> кадров одинаковы на всех платформах</div>
    </div>
    <div class="col">
      <div class="h pixel">Galaxy A12 — телефон 2020 года</div>
      <div v-for="r in rows" :key="r.k" class="m">
        <div class="mt"><b>{{ r.title }}</b><i>{{ r.unit }}</i></div>
        <div class="tr">
          <span v-if="r.cap" class="capl" :style="{ left: pct(r.cap, r.max) }"><em>{{ r.capLabel }}</em></span>
          <div class="bar before" :class="{ over: r.k === 'mem' }" :style="{ width: pct(r.before, r.max) }" />
          <span class="bl">было · {{ r.bLabel }}</span>
          <div class="bar after" :style="{ width: pct(r.after, r.max) }" />
          <span class="al">стало · {{ r.aLabel }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rs { display: grid; grid-template-columns: 0.95fr 1.05fr; gap: 1.6rem; align-items: start; }
.col { display: flex; flex-direction: column; gap: .45rem; }
.h { font-size: .7rem; color: var(--naruto); text-transform: uppercase; letter-spacing: .06em; }
.img { position: relative; border: 1px solid var(--hair); border-radius: 10px; overflow: hidden; line-height: 0; }
.img img { width: 100%; height: 11.2rem; object-fit: cover; object-position: center 45%; display: block; }
.img span { position: absolute; top: .4rem; font-size: .62rem; line-height: 1; color: var(--ink); background: rgba(10, 13, 19, .8); border-radius: 999px; padding: .2rem .5rem; }
.img .l { left: .4rem; }
.img .r { right: .4rem; }
.big { font-family: var(--font-display); font-size: 1.05rem; color: var(--ink-2); }
.big b { font-size: 1.9rem; color: var(--good); margin-right: .3rem; }
.cap { font-size: .8rem; line-height: 1.4; color: var(--ink); }
.cap2 { font-size: .78rem; color: var(--ink-2); }
.cap2 b { color: var(--ink); }
.m { margin-top: .35rem; }
.mt { display: flex; align-items: baseline; gap: .5rem; margin-bottom: .25rem; }
.mt b { font-size: .86rem; color: var(--ink); }
.mt i { font-style: normal; font-size: .64rem; color: var(--muted); }
.tr { position: relative; display: grid; grid-template-columns: 1fr; row-gap: .1rem; }
.bar { height: .85rem; border-radius: 4px; }
.bar.before { background: rgba(255, 255, 255, .22); }
.bar.before.over { background: var(--critical); }
.bar.after { background: var(--naruto); margin-top: .25rem; }
.bl, .al { font-size: .68rem; line-height: 1.25; color: var(--ink-2); }
.al { color: var(--ink); }
.capl { position: absolute; top: -.35rem; bottom: 1.1rem; border-left: 2px dashed var(--chakra); z-index: 1; }
.capl em { position: absolute; right: .35rem; top: -1rem; white-space: nowrap; font-style: normal; font-size: .6rem; color: var(--chakra); }
</style>
