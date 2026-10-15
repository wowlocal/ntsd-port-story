<script setup lang="ts">
// The load steps grouped by mechanism family, each family's total saving on the Galaxy A12 (sum of its steps'
// in-gate savings, only steps with a measured gain), with one worked example per family. The copy-on-write card
// carries a schematic (not to scale) of L2: a write into one loaded bitmap copied the whole array of them.
// Data: data/loading_steps.json (scripts/collect_loading.py); the explanations paraphrase MEMORY_LOADING.md.
import data from '../data/loading_steps.json'

const d = data as any
const byId: Record<string, any> = Object.fromEntries(d.steps.map((s: any) => [s.id, s]))
const parts = d.waterfall.load as { id: string, family: string, seconds: number }[]
const total = (f: string) => parts.filter(p => p.family === f).reduce((a, p) => a + p.seconds, 0)
const ids = (f: string) => parts.filter(p => p.family === f).map(p => p.id)
const f1 = (v: number) => v.toLocaleString('ru-RU', { minimumFractionDigits: 1, maximumFractionDigits: 1 })
const ab = (id: string) => {
  const p = byId[id].phone
  return `${f1(p.prev.load[0])} → ${f1(p.new.load[0])} с`
}
const color: Record<string, string> = { inplace: 'var(--s2)', parallel: 'var(--s1)', search: 'var(--s4)', convert: 'var(--s5)' }
const cards = [
  {
    f: 'parallel', title: 'Все ядра и железо',
    ex: [
      { id: 'L3', text: 'пакеты читаются, хешируются и декодируются параллельно, принимаются в порядке манифеста' },
      { id: 'L12', text: 'воркеры Dispatch жили на ядрах 0–3: унаследовали привязку главного потока. Свои потоки — на всех 8' },
      { id: 'L11', text: 'SHA-256 ~700 МБ на каждом запуске — инструкциями ARMv8, если на 12 входах ответ равен Swift' },
    ],
  },
  {
    f: 'convert', title: 'Меньше превращений',
    ex: [
      { id: 'L7', text: 'текст Latin-1 переводился в String скаляр за скаляром' },
      { id: 'L10', text: 'flatMap строил массив на каждый байт текстового режима' },
    ],
  },
  {
    f: 'search', title: 'Поиск вместо перебора',
    ex: [
      { id: 'L6', text: 'каждое выделение, запись и поиск перебирали все ~15 000 выделений; теперь двоичный поиск по адресам' },
    ],
  },
]
const cells = Array.from({ length: 12 }, (_, i) => i)
</script>

<template>
  <div class="fam">
    <div class="big card-f" :style="{ '--c': color.inplace }">
      <div class="h">
        <span class="nm">На месте, без копий</span>
        <span class="tot">−{{ f1(total('inplace')) }} с</span>
      </div>
      <div class="ids mono">
        {{ ids('inplace').join(' · ') }}
      </div>
      <p class="lead">
        Swift копирует массив или словарь при записи, если на него есть вторая ссылка. В загрузчике их оставляли вычисляемые свойства и копии «для отката», который и так делает внешний слой, — и каждая запись копировала всю структуру.
      </p>
      <svg viewBox="0 0 330 124" width="100%" role="img" aria-label="Схема L2: запись в одну картинку копировала весь массив">
        <text x="0" y="11" class="lb">L2, было: запись в одну картинку из ~1 800 загруженных</text>
        <g v-for="i in cells" :key="`a${i}`">
          <rect :x="i * 22" y="20" width="18" height="18" rx="3" :fill="i === 4 ? 'var(--s2)' : '#3a4252'" />
        </g>
        <text x="268" y="33" class="lb">…</text>
        <path d="M 97,42 V 62" stroke="var(--ink-2)" stroke-width="1.4" fill="none" marker-end="url(#lf-ah)" />
        <text x="108" y="56" class="lb">копируется весь массив</text>
        <g v-for="i in cells" :key="`b${i}`">
          <rect :x="i * 22" y="68" width="18" height="18" rx="3" :fill="i === 4 ? 'var(--s2)' : '#5d6679'" />
        </g>
        <text x="268" y="81" class="lb">…</text>
        <text x="0" y="112" class="lb">стало: <tspan class="b">_modify</tspan> — запись прямо в элемент, без копии</text>
        <defs>
          <marker id="lf-ah" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M0,0 L8,4 L0,8 z" fill="var(--ink-2)" />
          </marker>
        </defs>
      </svg>
      <div class="ex">
        <div><code>L1</code> символ DAT-файла копировал весь Stream туда и обратно · <b>{{ ab('L1') }}</b></div>
        <div><code>L2</code> массивы загрузчика · <b>{{ ab('L2') }}</b></div>
        <div><code>L5</code> эффекты картинок · <b>{{ ab('L5') }}</b></div>
      </div>
    </div>

    <div v-for="c in cards" :key="c.f" class="card-f" :style="{ '--c': color[c.f] }">
      <div class="h">
        <span class="nm">{{ c.title }}</span>
        <span class="tot">−{{ f1(total(c.f)) }} с</span>
      </div>
      <div class="ids mono">
        {{ ids(c.f).join(' · ') }}
      </div>
      <div v-for="e in c.ex" :key="e.id" class="exi">
        <code>{{ e.id }}</code> {{ e.text }} · <b>{{ ab(e.id) }}</b>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fam {
  display: grid;
  grid-template-columns: 1.08fr 1fr;
  grid-template-rows: auto auto auto;
  gap: 0.55rem 0.8rem;
}
.big {
  grid-row: 1 / span 3;
}
.card-f {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.45rem 0.75rem 0.5rem;
  overflow: hidden;
}
.card-f::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: var(--c);
}
.h {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}
.nm {
  font-size: 0.86rem;
  font-weight: 650;
  color: var(--ink);
}
.tot {
  font-size: 1.15rem;
  font-weight: 650;
  color: var(--ink);
}
.ids {
  font-size: 0.6rem;
  color: var(--muted);
  margin-bottom: 0.15rem;
}
.lead {
  font-size: 0.68rem !important;
  line-height: 1.35;
  color: var(--ink-2);
  margin: 0.15rem 0 0.35rem !important;
}
.lb {
  font-size: 10.5px;
  fill: var(--ink-2);
  font-family: var(--font-sans);
}
.lb .b {
  fill: var(--ink);
  font-family: var(--font-mono);
}
.ex {
  margin-top: 0.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  font-size: 0.65rem;
  color: var(--ink-2);
}
.exi {
  font-size: 0.65rem;
  line-height: 1.32;
  color: var(--ink-2);
  margin-top: 0.15rem;
}
b {
  color: var(--ink);
  white-space: nowrap;
}
code {
  font-size: 0.6rem !important;
}
</style>
