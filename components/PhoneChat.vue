<script setup lang="ts">
// Chat bubbles for chapter 14, a larger-type variant of ChatLog: agent on the left, human on the right,
// events centered. Text is verbatim from the session log; `gloss` adds a short Russian gloss under a bubble.
interface Msg { who: 'agent' | 'human' | 'event', time: string, text: string, gloss?: string, hot?: boolean }
withDefaults(defineProps<{ messages: Msg[], agent?: string, human?: string }>(), { agent: 'Claude', human: 'автор' })
</script>

<template>
  <div class="chat">
    <div v-for="(m, i) in messages" :key="i" class="msg" :class="[m.who, { hot: m.hot }]">
      <template v-if="m.who === 'event'">
        <span class="ev"><span class="t mono">{{ m.time }}</span> <span v-html="m.text" /></span>
      </template>
      <template v-else>
        <div class="meta">
          <span class="who">{{ m.who === 'agent' ? agent : human }}</span>
          <span class="t mono">{{ m.time }}</span>
        </div>
        <div class="bubble" lang="en" v-html="m.text" />
        <div v-if="m.gloss" class="gloss">
          {{ m.gloss }}
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  gap: 0.32rem;
}
.msg {
  display: flex;
  flex-direction: column;
  max-width: 90%;
}
.msg.agent {
  align-self: flex-start;
}
.msg.human {
  align-self: flex-end;
  align-items: flex-end;
}
.msg.event {
  align-self: center;
  max-width: 100%;
}
.meta {
  display: flex;
  gap: 0.45rem;
  align-items: baseline;
  font-size: 0.64rem;
  color: var(--muted);
  margin: 0 0.45rem 0.1rem;
}
.who {
  font-weight: 700;
  color: var(--ink-2);
}
.bubble {
  font-size: 0.7rem;
  line-height: 1.36;
  padding: 0.32rem 0.6rem;
  border-radius: 12px;
  color: var(--ink);
}
.agent .bubble {
  background: var(--surface-2);
  border: 1px solid var(--hair);
  border-top-left-radius: 4px;
}
.human .bubble {
  background: rgba(57, 135, 229, 0.2);
  border: 1px solid rgba(57, 135, 229, 0.5);
  border-top-right-radius: 4px;
}
.hot .bubble {
  border-color: rgba(255, 138, 61, 0.7);
  box-shadow: 0 0 0 1px rgba(255, 138, 61, 0.2);
}
.bubble :deep(b) {
  color: var(--ink);
}
.gloss {
  font-size: 0.64rem;
  line-height: 1.3;
  color: var(--muted);
  margin: 0.12rem 0.5rem 0;
}
.human .gloss {
  text-align: right;
}
.ev {
  font-size: 0.66rem;
  color: var(--ink-2);
  background: rgba(255, 255, 255, 0.04);
  border: 1px dashed var(--axis);
  border-radius: 999px;
  padding: 0.14rem 0.7rem;
}
.ev .t {
  color: var(--muted);
  margin-right: 0.25rem;
}
.hot .ev {
  border-color: rgba(255, 138, 61, 0.6);
  color: var(--ink);
}
.ev :deep(code) {
  font-size: 0.62rem;
}
</style>
