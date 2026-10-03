<script setup lang="ts">
// Byte layout of an original .lfr recording (tools/original_replay.py, REPLAY_TICK.md). Widths are schematic.
</script>

<template>
  <div class="anat">
    <div class="lbl">файл <span class="mono">.lfr</span> на диске</div>
    <div class="row">
      <div class="seg a" style="flex: 0 0 9%">
        <b>4 Б</b><span>длина</span>
      </div>
      <div class="seg b" style="flex: 0 0 25%">
        <b>1 345 Б</b><span>сдвинуты строкой из 1 345 цифр</span>
      </div>
      <div class="seg c" style="flex: 1">
        <b>zlib 1.1.4</b><span>поток сжатия (вшитая библиотека, не системная)</span>
      </div>
    </div>
    <div class="arrow">
      ↓ распаковка — всегда ровно <b>0x630e18 = 6 491 672 байта</b>
    </div>
    <div class="row">
      <div class="seg d" style="flex: 0 0 18%">
        <b>заголовок</b><span>настройки, игроки, контрольная сумма каталога @ +0x744</span>
      </div>
      <div class="seg e" style="flex: 0 0 15%">
        <b>+0x8c8</b><span>таблица ГСЧ 3000 Б</span>
      </div>
      <div class="seg f" style="flex: 1">
        <b>с 0x2b38: 10 байт на тик</b><span>ввод всех игроков · лимит 647 999 тиков ≈ 6 часов · каждые 150 тиков — сумма HP 20 мест</span>
      </div>
    </div>
    <div class="notes">
      <span>ключ сдвига: <span class="mono">(c − key[i] + 48) &amp; 255</span>, <span class="mono">strlen(key)</span> на каждой итерации</span>
      <span>на тике 216 000 (2 ч) слот суммы HP налезает на первый пакет</span>
    </div>
  </div>
</template>

<style scoped>
.lbl {
  font-size: 0.66rem;
  color: var(--muted);
  margin-bottom: 0.25rem;
}
.row {
  display: flex;
  gap: 3px;
}
.seg {
  border-radius: 6px;
  padding: 0.4rem 0.55rem;
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.seg b {
  font-size: 0.74rem;
  color: var(--ink);
}
.seg span {
  font-size: 0.6rem;
  color: var(--ink-2);
  line-height: 1.25;
}
.a { background: rgba(255, 255, 255, 0.08); }
.b { background: rgba(217, 89, 38, 0.32); }
.c { background: rgba(57, 135, 229, 0.25); }
.d { background: rgba(255, 255, 255, 0.08); }
.e { background: rgba(201, 133, 0, 0.32); }
.f { background: rgba(25, 158, 112, 0.28); }
.arrow {
  font-size: 0.68rem;
  color: var(--ink-2);
  padding: 0.35rem 0 0.35rem 0.4rem;
}
.notes {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  font-size: 0.6rem;
  color: var(--muted);
  margin-top: 0.35rem;
}
</style>
