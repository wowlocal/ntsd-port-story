<script setup lang="ts">
// Chapter 8: the 2 October scope reconciliation (docs/research/SCOPE_RECONCILIATION_2026-10-02.md, 0356f06b).
// Each of CONTINUE_GOAL's 18 full-scope criteria got a class: V verified, M implemented with a missing check,
// G an implementation gap, E (the corner mark) a missing check blocked outside the project. "V, then M" rows
// are split tiles; a star marks a declared deviation or declared stops. Hover a tile for its missing check;
// with nothing hovered (and in export) the one G row is shown.
import { computed, ref } from 'vue'

interface Row { name: string, cls: 'V' | 'VM' | 'M' | 'G', ext?: boolean, star?: boolean, miss: string }
const rows: Row[] = [
  { name: 'Персонажи, техники, объекты, эффекты', cls: 'VM', ext: true, miss: 'целые матчи на Windows — Windows-машины здесь нет' },
  { name: 'AI', cls: 'V', miss: '3 770 вызовов, soak-прогоны всех режимов' },
  { name: 'Арены', cls: 'V', miss: '17 фонов и Random запускаются и играются' },
  { name: 'Режимы: VS, Stage, Demo, War, турниры, Playback, Quit', cls: 'V', miss: 'все десять e2e-сценариев на бандле кандидата' },
  { name: 'ONLINE GAME', cls: 'G', miss: 'N1 в 7727346, N2 — незакоммиченный WIP; отложено автором 1 октября, отказ модели открыт' },
  { name: 'Меню, настройки, сохранения', cls: 'V', miss: 'CONTROL SETTINGS — 106 случаев, RECORDING INFO — 129' },
  { name: 'Повторы', cls: 'V', miss: 'Playback P1–P4, проигрывание попиксельно' },
  { name: 'Физика, комбо, ГСЧ, x87', cls: 'V', ext: true, miss: 'наблюдение на Windows' },
  { name: 'Тайминги', cls: 'VM', ext: true, miss: 'задержка ввода и ощущение на устройстве — вручную' },
  { name: 'Камера', cls: 'V', miss: 'корпуса игровой камеры и камеры проигрывания (F6)' },
  { name: 'HUD и текст GDI', cls: 'V', star: true, miss: 'шрифт SYSTEM_FONT — временное отличие: его нельзя распространять' },
  { name: 'Звук', cls: 'M', ext: true, miss: 'сравнение звука на Windows; трек Demo — временный объявленный выбор' },
  { name: 'Исключения ID в EXE', cls: 'V', miss: 'ID 50/51, 122, 217/218, 998/999 — внутри сверенных проходов' },
  { name: 'Полный пул', cls: 'V', star: true, ext: true, miss: 'случаи с адресами кучи — объявленные остановки' },
  { name: 'Окно: запуск, ESC, Alt+Enter', cls: 'V', ext: true, miss: 'ответы режима дисплея при Alt+Enter объявлены' },
  { name: 'Полный экран macOS', cls: 'M', miss: '1 и 2 октября дисплей спал — переход AppKit не наблюдался' },
  { name: 'Ввод: клавиши, F-клавиши, джойстик', cls: 'VM', ext: true, miss: 'физический контроллер; F1, F2, F3, F5, F6 и F9 в бою проверены этим утром' },
  { name: 'Упаковка и офлайн-сборка', cls: 'V', ext: true, miss: 'приёмка на чистом Mac' },
]
const hover = ref<number | null>(null)
const shown = computed(() => rows[hover.value ?? rows.findIndex(r => r.cls === 'G')])
const count = (c: Row['cls']) => rows.filter(r => r.cls === c).length
</script>

<template>
  <div class="sc">
    <div class="grid3">
      <div v-for="(r, i) in rows" :key="i" class="tile" :class="[r.cls, { on: hover === i }]" @mouseenter="hover = i" @mouseleave="hover = null">
        <span class="badge">{{ r.cls === 'VM' ? 'V→M' : r.cls }}{{ r.star ? '*' : '' }}</span>
        <span class="nm">{{ r.name }}</span>
        <span v-if="r.ext" class="ext" title="внешнее препятствие">E</span>
      </div>
    </div>
    <div class="detail" :class="shown.cls">
      <span class="badge">{{ shown.cls === 'VM' ? 'V→M' : shown.cls }}</span>
      <span><b>{{ shown.name }}</b> — {{ shown.miss }}</span>
    </div>
    <div class="legend">
      <span><i class="sw V" />V проверено · {{ count('V') }}</span>
      <span><i class="sw VM" />V, затем M · {{ count('VM') }}</span>
      <span><i class="sw M" />M нет проверки · {{ count('M') }}</span>
      <span><i class="sw G" />G пробел · {{ count('G') }}</span>
      <span><b class="e">E</b> упирается во внешнее</span>
      <span>* объявленное отличие</span>
    </div>
  </div>
</template>

<style scoped>
.sc { display: flex; flex-direction: column; gap: 0.35rem; }
.grid3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 4px; }
.tile { position: relative; display: grid; grid-template-columns: 2.1rem 1fr; align-items: center; gap: 0.35rem; min-height: 2.05rem; padding: 0.2rem 0.75rem 0.2rem 0.3rem; background: var(--surface); border: 1px solid var(--hair); border-radius: 8px; transition: border-color 0.2s; cursor: default; }
.tile.on { border-color: var(--ink-2); }
.badge { font-family: var(--font-mono); font-size: 0.56rem; font-weight: 700; text-align: center; border-radius: 5px; padding: 0.12rem 0; color: #0a0d13; }
.V .badge { background: var(--good); }
.VM .badge { background: linear-gradient(90deg, var(--good) 50%, var(--warning) 50%); }
.M .badge { background: var(--warning); }
.G .badge { background: var(--critical); color: var(--ink); }
.G.tile { border-color: rgba(208, 59, 59, 0.6); background: rgba(208, 59, 59, 0.1); }
.nm { font-size: 0.56rem; line-height: 1.2; color: var(--ink-2); }
.ext { position: absolute; top: 2px; right: 4px; font-family: var(--font-mono); font-size: 0.48rem; color: var(--chakra); }
.detail { display: grid; grid-template-columns: 2.1rem 1fr; gap: 0.45rem; align-items: center; font-size: 0.6rem; line-height: 1.3; color: var(--ink-2); background: rgba(255, 255, 255, 0.03); border: 1px dashed var(--axis); border-radius: 8px; padding: 0.28rem 0.5rem 0.28rem 0.3rem; min-height: 1.9rem; }
.detail b { color: var(--ink); }
.legend { display: flex; flex-wrap: wrap; gap: 0.25rem 0.8rem; font-size: 0.54rem; color: var(--muted); }
.legend span { display: inline-flex; align-items: center; gap: 0.3rem; }
.sw { display: inline-block; width: 14px; height: 9px; border-radius: 3px; }
.sw.V { background: var(--good); }
.sw.VM { background: linear-gradient(90deg, var(--good) 50%, var(--warning) 50%); }
.sw.M { background: var(--warning); }
.sw.G { background: var(--critical); }
.e { font-family: var(--font-mono); color: var(--chakra); font-weight: 400; }
</style>
