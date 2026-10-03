<script setup lang="ts">
// A short exchange rendered as chat bubbles: agent on the left, human on the right, events centered.
interface Msg { who: 'agent' | 'human' | 'event', time: string, text: string, hot?: boolean }
withDefaults(defineProps<{ messages: Msg[], agent?: string, human?: string }>(), { agent: 'Claude', human: 'человек' })
</script>

<template>
  <div class="chat">
    <div v-for="(m, i) in messages" :key="i" class="msg" :class="[m.who, { hot: m.hot }]">
      <template v-if="m.who === 'event'">
        <span class="ev"><span class="t mono">{{ m.time }}</span> {{ m.text }}</span>
      </template>
      <template v-else>
        <div class="meta">
          <span class="who">{{ m.who === 'agent' ? agent : human }}</span>
          <span class="t mono">{{ m.time }}</span>
        </div>
        <div class="bubble" v-html="m.text" />
      </template>
    </div>
  </div>
</template>

<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.msg {
  display: flex;
  flex-direction: column;
  max-width: 82%;
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
  gap: 0.4rem;
  align-items: baseline;
  font-size: 0.5rem;
  color: var(--muted);
  margin: 0 0.4rem 0.08rem;
}
.who {
  font-weight: 700;
  color: var(--ink-2);
}
.bubble {
  font-size: 0.64rem;
  line-height: 1.3;
  padding: 0.26rem 0.5rem;
  border-radius: 12px;
  color: var(--ink);
}
.agent .bubble {
  background: var(--surface-2);
  border: 1px solid var(--hair);
  border-top-left-radius: 4px;
}
.human .bubble {
  background: rgba(57, 135, 229, 0.22);
  border: 1px solid rgba(57, 135, 229, 0.45);
  border-top-right-radius: 4px;
}
.hot .bubble {
  border-color: rgba(255, 138, 61, 0.65);
  box-shadow: 0 0 0 1px rgba(255, 138, 61, 0.18);
}
.bubble :deep(code) {
  font-size: 0.62rem;
}
.ev {
  font-size: 0.62rem;
  color: var(--ink-2);
  background: rgba(255, 255, 255, 0.04);
  border: 1px dashed var(--axis);
  border-radius: 999px;
  padding: 0.12rem 0.65rem;
}
.ev .t {
  color: var(--muted);
  margin-right: 0.25rem;
}
.hot .ev {
  border-color: rgba(255, 138, 61, 0.6);
  color: var(--ink);
}
</style>
