<script setup lang="ts">
import data from '../data/hidden_roster.json'

// Portraits of the type-0 objects the character screen skips until LF2.NET sets 458428.
const chars = (data as any).characters as { id: number, file: string, name: string, image?: string }[]
</script>

<template>
  <div class="roster">
    <div v-for="c in chars" :key="c.id" class="cell" :title="`ID ${c.id} · ${c.file}`">
      <img v-if="c.image" :src="c.image" class="pixelated" alt="">
      <div class="nm">
        {{ c.name.replace('_', ' ') }}
      </div>
      <div class="id mono">
        {{ c.id }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.roster {
  display: grid;
  grid-template-columns: repeat(9, 1fr);
  gap: 0.45rem;
}
.cell {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--hair);
  border-radius: 8px;
  overflow: hidden;
  text-align: center;
}
.cell img {
  display: block;
  width: 100%;
  aspect-ratio: 1;
}
.nm {
  font-size: 0.55rem;
  color: var(--ink);
  padding: 0.12rem 0.2rem 0.18rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.id {
  position: absolute;
  top: 3px;
  left: 4px;
  font-size: 0.56rem;
  color: #fff;
  background: rgba(10, 13, 19, 0.75);
  border-radius: 3px;
  padding: 0 0.2rem;
}
</style>
