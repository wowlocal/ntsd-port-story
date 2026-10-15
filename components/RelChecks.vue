<script setup lang="ts">
// Chapter 18: how each package of the 13 Oct release was checked (release-refresh-20261013.json), and the
// 15 failures the release run recorded on its way (failures.json in the artifacts folder), as dots by cause.
// Hover a dot for what failed and what was done about it.
// Data: data/rel_release.json (scripts/collect_release.py).
import { computed, ref } from 'vue'
import rel from '../data/rel_release.json'

const r = rel as any
const rows = r.matrix.rows as any[]
const failures = r.failures as any[]
const byPlat = (id: string) => failures.filter(f => f.platform === id)
const causes = [
  { id: 'keychain', label: 'связка ключей и сеанс входа', color: 'var(--s5)' },
  { id: 'appledouble', label: 'файлы ._ от macOS на диске ExFAT', color: 'var(--s4)' },
  { id: 'scaling', label: 'масштабированное окно', color: 'var(--s7)' },
  { id: 'harness', label: 'харнесс и инструменты', color: '#7d8494' },
]
const colorOf = (c: string) => causes.find(x => x.id === c)!.color
const count = (c: string) => failures.filter(f => f.cause === c).length
const sel = ref(failures.find(f => f.cause === 'appledouble' && f.platform === 'android')!.n)
const cur = computed(() => failures.find(f => f.n === sel.value))
const cols = [
  { k: 'integrity', t: 'целостность' },
  { k: 'launch', t: 'запуск' },
  { k: 'vs', t: 'матч VS' },
  { k: 'signing', t: 'подпись' },
  { k: 'where', t: 'где' },
]
</script>

<template>
  <div class="rc">
    <div class="tbl">
      <div class="tr th">
        <span>пакет</span><span v-for="c in cols" :key="c.k">{{ c.t }}</span><span>сбои по дороге</span>
      </div>
      <div v-for="row in rows" :key="row.id" class="tr">
        <span class="pk"><b>{{ row.label }}</b><i>{{ row.pkg }}</i></span>
        <span v-for="c in cols" :key="c.k" class="cell" :class="{ none: !row[c.k] }">
          <template v-if="row[c.k]"><i v-if="c.k !== 'where'" class="ok">✓</i>{{ row[c.k] }}<span v-if="c.k === 'where' && row.boundary" class="bd">⚠ {{ row.boundary }}</span></template>
          <template v-else>—</template>
        </span>
        <span class="dots">
          <i v-for="f in byPlat(row.id)" :key="f.n" class="fd" :class="{ sel: sel === f.n }" :style="{ background: colorOf(f.cause) }" tabindex="0" :aria-label="f.operation" @pointerenter="sel = f.n" @focus="sel = f.n" />
          <span v-if="!byPlat(row.id).length" class="muted">0</span>
        </span>
      </div>
    </div>
    <div class="pubrow">
      <span class="pk"><b>публикация</b><i>GitHub</i></span>
      <span><i class="ok">✓</i>{{ r.assets.length }} из {{ r.assets.length }} дайджестов и размеров на GitHub = локальные файлы; три манифеста скачаны целиком и сверены, крупные файлы не перекачивали</span>
      <span class="dots"><i v-for="f in byPlat('publish')" :key="f.n" class="fd" :class="{ sel: sel === f.n }" :style="{ background: colorOf(f.cause) }" tabindex="0" :aria-label="f.operation" @pointerenter="sel = f.n" @focus="sel = f.n" /></span>
    </div>
    <div class="bottom">
      <div class="legend">
        <div v-for="c in causes" :key="c.id"><i class="fd" :style="{ background: c.color }" />{{ c.label }} <b>{{ count(c.id) }}</b></div>
      </div>
      <div class="fail" aria-live="polite">
        <div class="fh"><i class="fd" :style="{ background: colorOf(cur.cause) }" /><b>#{{ cur.n }} · {{ cur.ru }}</b><span class="mono op" lang="en">{{ cur.operation }}</span></div>
        <div class="fr" lang="en"><span class="k">result</span>{{ cur.result }}</div>
        <div class="fr" lang="en"><span class="k">then</span>{{ cur.next }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rc { display: flex; flex-direction: column; gap: 8px; }
.tbl { font-size: 0.6rem; }
.tr { display: grid; grid-template-columns: 7.4rem 1.15fr 1.2fr 1.15fr 1.25fr 1fr 5.4rem; gap: 8px; padding: 3px 4px; border-bottom: 1px solid var(--grid); align-items: start; line-height: 1.3; color: var(--ink-2); }
.th { color: var(--muted); border-bottom: 1px solid var(--axis); font-size: 0.6rem; }
.pk { display: flex; flex-direction: column; }
.pk b { color: var(--ink); font-size: 0.66rem; }
.pk i { font-style: normal; color: var(--muted); font-family: var(--font-mono); font-size: 0.58rem; }
.cell.none { color: var(--muted); }
.ok { color: var(--good); font-style: normal; font-weight: 700; margin-right: 3px; }
.bd { display: block; color: var(--warning); }
.dots { display: flex; flex-wrap: wrap; gap: 4px; padding-top: 2px; }
.fd { display: inline-block; width: 11px; height: 11px; border-radius: 3px; cursor: pointer; outline: none; flex: none; }
.fd.sel { box-shadow: 0 0 0 2px var(--bg), 0 0 0 3.5px var(--ink); }
.pubrow { display: grid; grid-template-columns: 7.4rem 1fr 5.4rem; gap: 8px; padding: 0 4px; font-size: 0.6rem; color: var(--ink-2); align-items: start; line-height: 1.3; margin-top: -4px; }
.bottom { display: grid; grid-template-columns: 15rem 1fr; gap: 14px; align-items: start; }
.legend { display: flex; flex-direction: column; gap: 3px; font-size: 0.64rem; color: var(--ink-2); }
.legend div { display: flex; align-items: center; gap: 6px; }
.legend b { color: var(--ink); margin-left: auto; }
.legend .fd { cursor: default; }
.fail { background: var(--surface); border: 1px solid var(--hair); border-radius: 12px; padding: 6px 10px; font-size: 0.62rem; color: var(--ink-2); line-height: 1.35; }
.fh { display: flex; align-items: center; gap: 6px; color: var(--ink); margin-bottom: 2px; }
.fh b { font-size: 0.68rem; }
.fh .op { margin-left: auto; font-family: var(--font-mono); font-size: 0.58rem; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 40%; }
.fr .k { display: inline-block; width: 3.4rem; color: var(--muted); font-family: var(--font-mono); }
</style>
