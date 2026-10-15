<script setup lang="ts">
// Chapter 18: the 13 files of the GitHub release native-preview-20261013. Bars are the six packages (MB, decimal);
// the strip below is when each file was uploaded, with the three release commits, the publication and the
// switch to Latest. Hover a bar, a row or a dot to see the file's exact size, SHA-256 and what was checked.
// Data: data/rel_release.json (scripts/collect_release.py).
import { computed, ref } from 'vue'
import rel from '../data/rel_release.json'
import day from '../data/rel_day.json'

const r = rel as any
const assets = r.assets as any[]
const platOf = (name: string) => {
  if (name.startsWith('NTSD-Native'))
    return 'macos'
  const m = name.match(/^ntsd-(android|windows|web|linux-aarch64|linux-x86_64)/)
  return m ? m[1] : null
}
const labels = r.matrix.labels as Record<string, string>
const rowOf = (id: string) => (r.matrix.rows as any[]).find(x => x.ids.includes(id))
const order = ['macos', 'android', 'windows', 'linux-aarch64', 'linux-x86_64', 'web']
const pkgs = order.map(id => assets.find(a => a.kind === 'package' && platOf(a.name) === id))
const small = assets.filter(a => a.kind !== 'package')
const sel = ref('NTSD-Native-0.5.0.dmg')
const cur = computed(() => assets.find(a => a.name === sel.value))
const curPlat = computed(() => {
  const id = platOf(cur.value.name)
  return id ? { label: labels[id], signing: rowOf(id)?.signing } : null
})

const mbf = new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 1, maximumFractionDigits: 1 })
const nf = new Intl.NumberFormat('ru-RU')
const size = (b: number) => (b >= 1e6 ? `${mbf.format(b / 1e6)} МБ` : b >= 1e3 ? `${nf.format(Math.round(b / 1e3))} КБ` : `${b} Б`)
const commitOf = (name: string) => name.match(/-([0-9a-f]{7})\./)?.[1] ?? (name.startsWith('NTSD-Native') ? r.tagCommit.slice(0, 7) : '—')
const shaRows = (h: string) => [h.slice(0, 32), h.slice(32)]
const kindRu: Record<string, string> = { package: 'пакет', manifest: 'манифест: SHA-256 каждого файла внутри', sums: 'контрольные суммы' }

// bars
const BW = 470
const rowH = 25
const BH = pkgs.length * rowH + 4
const lx = 118
const maxB = Math.max(...pkgs.map(p => p.bytes))
const bl = (b: number) => (b / maxB) * (BW - lx - 70)
const totalPkg = pkgs.reduce((a, p) => a + p.bytes, 0)

// timeline
const sec = (t: string) => {
  const [h, m, s] = t.split(':').map(Number)
  return h * 3600 + m * 60 + (s || 0)
}
const T0 = sec('14:48')
const T1 = sec('15:31')
const TW = 884
const TH = 74
const tx = (t: string) => 12 + ((sec(t) - T0) / (T1 - T0)) * (TW - 24)
const tTicks = ['14:50', '14:55', '15:00', '15:05', '15:10', '15:15', '15:20', '15:25', '15:30']
const relCommits = (day as any).commits.filter((c: any) => !c.trailer)
const pub = r.publication
const dotColor = (a: any) => (a.kind === 'package' ? 'var(--s1)' : a.kind === 'manifest' ? 'var(--muted)' : 'var(--ink-2)')
</script>

<template>
  <div class="ra">
    <div class="top">
      <div>
        <svg :viewBox="`0 0 ${BW} ${BH}`" width="100%" role="img" :aria-label="`Шесть пакетов релиза, всего ${size(totalPkg)}`">
          <g v-for="(p, i) in pkgs" :key="p.name" class="row" :class="{ sel: sel === p.name }" @pointerenter="sel = p.name" @focus="sel = p.name" tabindex="0">
            <rect x="0" :y="i * rowH" :width="BW" :height="rowH" class="hit" />
            <text class="pl" x="0" :y="i * rowH + 16">{{ labels[platOf(p.name)!] }}</text>
            <path :d="`M${lx},${i * rowH + 5} h${bl(p.bytes) - 4} q4,0 4,4 v8 q0,4 -4,4 h${-(bl(p.bytes) - 4)} Z`" class="bar" />
            <text class="val" :x="lx + bl(p.bytes) + 6" :y="i * rowH + 16">{{ size(p.bytes) }}</text>
          </g>
        </svg>
        <div class="small">
          <span v-for="a in small" :key="a.name" class="sf" :class="{ sel: sel === a.name }" tabindex="0" @pointerenter="sel = a.name" @focus="sel = a.name">
            <i :style="{ background: dotColor(a) }" />{{ a.name.replace(/-[0-9a-f]{7}\.manifest\.json$/, '…manifest').replace('ntsd-', '') }} <b>{{ size(a.bytes) }}</b>
          </span>
        </div>
      </div>
      <div class="det" aria-live="polite">
        <div class="fn">{{ cur.name }}</div>
        <div class="kv"><span>что</span><span>{{ kindRu[cur.kind] }}<template v-if="curPlat"> · {{ curPlat.label }}</template></span></div>
        <div class="kv"><span>размер</span><span><b>{{ nf.format(cur.bytes) }}</b> байт</span></div>
        <div class="kv"><span>SHA-256</span><span class="sha"><span v-for="(s, i) in shaRows(cur.sha256)" :key="i">{{ s }}</span></span></div>
        <div class="kv"><span>загружен</span><span>{{ cur.uploaded }} · исходники {{ commitOf(cur.name) }}</span></div>
        <div class="kv"><span>GitHub</span><span class="ok">✓ дайджест и размер = локальный файл</span></div>
        <div v-if="curPlat && cur.kind === 'package'" class="kv"><span>подпись</span><span>{{ curPlat.signing || 'подписи кода нет — целостность по SHA256SUMS и манифесту' }}</span></div>
      </div>
    </div>

    <svg class="tl" :viewBox="`0 0 ${TW} ${TH}`" width="100%" role="img" aria-label="Время загрузки файлов релиза, коммиты, публикация и метка Latest">
      <line :x1="12" :x2="TW - 12" :y1="44" :y2="44" class="axis" />
      <g v-for="t in tTicks" :key="t">
        <line :x1="tx(t)" :x2="tx(t)" y1="41" y2="47" class="axis" />
        <text class="ax" :x="tx(t)" :y="TH - 12" text-anchor="middle">{{ t }}</text>
      </g>
      <!-- commits without the Claude trailer -->
      <g v-for="(c, i) in relCommits" :key="c.hash">
        <line :x1="tx(c.time)" :x2="tx(c.time)" y1="18" y2="44" class="cm" />
        <text class="cmt" :x="tx(c.time) + (i === 2 ? 4 : 4)" :y="i === 2 ? 26 : 16">{{ c.hash }}</text>
      </g>
      <!-- publication -->
      <g>
        <line :x1="tx(pub.published)" :x2="tx(pub.published)" y1="6" y2="44" class="pub" />
        <text class="pubt" :x="tx(pub.published) - 4" y="12" text-anchor="end">опубликован {{ pub.published.slice(0, 5) }}</text>
        <line :x1="tx(pub.updated)" :x2="tx(pub.updated)" y1="30" y2="44" class="pub" />
        <text class="pubt" :x="tx(pub.updated) - 4" y="36" text-anchor="end">Latest</text>
      </g>
      <g v-for="a in assets" :key="a.name" class="dot" tabindex="0" @pointerenter="sel = a.name" @focus="sel = a.name">
        <circle :cx="tx(a.uploaded)" cy="44" r="12" class="hit" />
        <circle :cx="tx(a.uploaded)" cy="44" :r="sel === a.name ? 6 : 4.5" :fill="dotColor(a)" stroke="var(--bg)" stroke-width="2" />
      </g>
      <text class="ax" x="12" :y="TH - 1">точки — загрузка каждого из {{ assets.length }} файлов; синие — пакеты</text>
    </svg>
  </div>
</template>

<style scoped>
.ra { display: flex; flex-direction: column; gap: 6px; }
.top { display: grid; grid-template-columns: 1.12fr 1fr; gap: 18px; }
.row { cursor: pointer; outline: none; }
.hit { fill: transparent; }
.pl { font-size: 11.5px; fill: var(--ink-2); font-family: var(--font-sans); }
.row.sel .pl { fill: var(--ink); font-weight: 650; }
.bar { fill: var(--s1); }
.row.sel .bar { fill: #5c9eec; }
.val { font-size: 11px; fill: var(--ink); font-weight: 650; font-family: var(--font-sans); font-variant-numeric: tabular-nums; }
.small { display: flex; flex-wrap: wrap; gap: 2px 10px; margin-top: 4px; }
.sf { font-size: 0.6rem; color: var(--ink-2); display: inline-flex; align-items: center; gap: 4px; cursor: pointer; outline: none; font-family: var(--font-mono); }
.sf b { color: var(--ink); font-weight: 600; font-family: var(--font-sans); }
.sf i { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }
.sf.sel { color: var(--ink); text-decoration: underline; text-decoration-color: var(--naruto); }
.det { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: 7px 11px 8px; font-size: 0.66rem; color: var(--ink-2); }
.fn { font-family: var(--font-mono); font-size: 0.7rem; color: var(--ink); margin-bottom: 4px; word-break: break-all; }
.kv { display: grid; grid-template-columns: 4.6rem 1fr; gap: 6px; line-height: 1.38; }
.kv > span:first-child { color: var(--muted); }
.kv b { color: var(--ink); }
.sha { font-family: var(--font-mono); font-size: 0.6rem; display: flex; flex-direction: column; color: var(--ink); }
.ok { color: var(--ink); }
.tl { margin-top: 2px; }
.axis { stroke: var(--axis); stroke-width: 1; }
.ax { font-size: 10px; fill: var(--muted); font-family: var(--font-sans); font-variant-numeric: tabular-nums; }
.cm { stroke: var(--s1); stroke-width: 1; }
.cmt { font-size: 10px; fill: var(--ink-2); font-family: var(--font-mono); }
.pub { stroke: var(--ink); stroke-width: 1.5; }
.pubt { font-size: 10.5px; fill: var(--ink); font-family: var(--font-sans); font-weight: 600; }
.dot { cursor: pointer; outline: none; }
</style>
