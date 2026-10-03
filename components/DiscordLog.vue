<script setup lang="ts">
// Messages from the NTSD Discord, retyped from screenshots: handle, time, optional reply line,
// text, link embed and reactions. Avatars are left out on purpose.
interface Embed { site: string, title: string, text?: string }
interface Msg {
  who?: string
  color?: string
  time?: string
  text?: string
  reply?: { who: string, text: string }
  embed?: Embed
  reactions?: string[]
  day?: string
  me?: boolean
}
defineProps<{ messages: Msg[] }>()
</script>

<template>
  <div class="dc">
    <template v-for="(m, i) in messages" :key="i">
      <div v-if="m.day" class="day"><span>{{ m.day }}</span></div>
      <div v-else class="msg" :class="{ me: m.me }">
        <div v-if="m.reply" class="reply">
          <span class="rw">@{{ m.reply.who }}</span> {{ m.reply.text }}
        </div>
        <div v-if="m.who" class="meta">
          <b :style="{ color: m.color ?? 'var(--ink)' }">{{ m.who }}</b>
          <span class="t">{{ m.time }}</span>
        </div>
        <div v-if="m.text" class="text" v-html="m.text" />
        <div v-if="m.embed" class="embed">
          <div class="site">{{ m.embed.site }}</div>
          <div class="et">{{ m.embed.title }}</div>
          <div v-if="m.embed.text" class="ex">{{ m.embed.text }}</div>
        </div>
        <div v-if="m.reactions" class="re">
          <span v-for="r in m.reactions" :key="r">{{ r }}</span>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.dc {
  background: #1e1f24;
  border: 1px solid var(--hair);
  border-radius: 12px;
  padding: 0.55rem 0.8rem 0.6rem;
  display: flex;
  flex-direction: column;
  gap: 0.36rem;
  font-family: var(--font-sans);
}
.day {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.56rem;
  color: var(--muted);
  font-weight: 600;
}
.day::before,
.day::after {
  content: '';
  flex: 1;
  border-top: 1px solid rgba(255, 255, 255, 0.09);
}
.msg.me {
  border-left: 2px solid var(--naruto);
  padding-left: 0.5rem;
  margin-left: -0.55rem;
}
.reply {
  font-size: 0.56rem;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-left: 0.9rem;
  position: relative;
}
.reply::before {
  content: '';
  position: absolute;
  left: 0.2rem;
  top: 0.45em;
  width: 0.5rem;
  height: 0.6em;
  border-left: 1.5px solid rgba(255, 255, 255, 0.22);
  border-top: 1.5px solid rgba(255, 255, 255, 0.22);
  border-top-left-radius: 4px;
}
.rw {
  color: var(--ink-2);
  font-weight: 600;
}
.meta {
  display: flex;
  align-items: baseline;
  gap: 0.45rem;
  font-size: 0.66rem;
}
.meta b {
  font-weight: 600;
}
.t {
  font-size: 0.56rem;
  color: var(--muted);
}
.text {
  font-size: 0.66rem;
  line-height: 1.35;
  color: #dbdee1;
}
.text :deep(a),
.text :deep(.link) {
  color: #00a8fc;
}
.embed {
  margin-top: 0.25rem;
  border-left: 3px solid #4e5058;
  background: #2b2d31;
  border-radius: 4px;
  padding: 0.3rem 0.55rem;
  max-width: 26rem;
}
.site {
  font-size: 0.56rem;
  color: var(--muted);
}
.et {
  font-size: 0.62rem;
  color: #00a8fc;
  font-weight: 600;
}
.ex {
  font-size: 0.56rem;
  color: #dbdee1;
  line-height: 1.3;
}
.re {
  display: flex;
  gap: 0.3rem;
  margin-top: 0.2rem;
}
.re span {
  font-size: 0.56rem;
  background: #2b2d31;
  border-radius: 6px;
  padding: 0.02rem 0.4rem;
  color: var(--ink-2);
}
</style>
