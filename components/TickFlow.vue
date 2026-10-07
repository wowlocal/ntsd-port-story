<script setup lang="ts">
// One gameplay tick on the runtime before the redesign, from the read-only data-flow map (CORE_REALTIME_DATAFLOW.md),
// the message-loop design note (CORE_REALTIME_M2.md) and the copy map (CORE_REALTIME_COPIES.md).
// The chips are counts from those notes; the copy totals are estimates from stored fields, not measurements.
const stages = [
  {
    name: 'Цикл сообщений',
    chip: '×5–6 прогонов',
    text: 'Каждый новый запрос к платформе — PeekMessage, timeGetTime, Blt — обрывает попытку Host, и её прогоняют заново с записанными ответами.',
  },
  {
    name: 'Загруженный цикл',
    chip: '400 актёров',
    text: 'bindings.read переводит мир, глобалы и 400 записей актёров из состояния сессии в модель матча; внутри — вложенные копии-кандидаты.',
  },
  {
    name: 'Игровой тик',
    chip: '≈ 600 КБ копий',
    text: 'Новая попытка копирует состояние, модель, звук и ресурсы; второй bindings.store пишет 400 актёров обратно.',
  },
  {
    name: 'Завершение',
    chip: 'всё в одном потоке',
    text: 'Коммит, затем весь батч рисования — пиксели, crop, окно Android — на том же главном потоке.',
  },
]
</script>

<template>
  <div class="flow">
    <div v-for="(s, i) in stages" :key="s.name" class="st">
      <div class="rail">
        <span class="no pixel">{{ i + 1 }}</span>
        <i v-if="i < stages.length - 1" class="ln" />
      </div>
      <div class="body">
        <div class="head">
          <b>{{ s.name }}</b><span class="chip mono">{{ s.chip }}</span>
        </div>
        <div class="txt">
          {{ s.text }}
        </div>
      </div>
    </div>
    <div class="loop">
      <span class="i-pixelarticons-reload ico" />и так каждый тик — ~30 раз в секунду, если успевать
    </div>
  </div>
</template>

<style scoped>
.flow {
  display: flex;
  flex-direction: column;
}
.st {
  display: grid;
  grid-template-columns: 1.5rem 1fr;
  gap: 0.55rem;
}
.rail {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.no {
  display: grid;
  place-items: center;
  width: 1.4rem;
  height: 1.4rem;
  border-radius: 6px;
  background: var(--surface-2);
  border: 1px solid var(--axis);
  color: var(--naruto);
  font-size: 0.78rem;
}
.ln {
  flex: 1;
  width: 2px;
  margin: 2px 0;
  background: var(--axis);
}
.body {
  padding-bottom: 0.5rem;
}
.head {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-height: 1.4rem;
}
.head b {
  font-size: 0.8rem;
  color: var(--ink);
}
.chip {
  font-size: 0.64rem;
  color: var(--ink);
  background: rgba(217, 89, 38, 0.18);
  border: 1px solid rgba(217, 89, 38, 0.55);
  border-radius: 999px;
  padding: 0.02rem 0.45rem;
  white-space: nowrap;
}
.txt {
  font-size: 0.68rem;
  line-height: 1.35;
  color: var(--ink-2);
}
.loop {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-left: 2.05rem;
  font-size: 0.66rem;
  color: var(--muted);
}
.ico {
  width: 0.95rem;
  height: 0.95rem;
  color: var(--naruto);
}
</style>
