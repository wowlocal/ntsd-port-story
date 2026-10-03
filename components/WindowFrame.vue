<script setup lang="ts">
withDefaults(defineProps<{
  title?: string
  src?: string
  video?: string
  poster?: string
  kind?: 'mac' | 'win'
  pixel?: boolean
  caption?: string
  height?: string
  position?: string
}>(), {
  title: 'NTSD Native',
  kind: 'mac',
  pixel: true,
})
</script>

<template>
  <figure class="frame" :class="kind">
    <div class="bar">
      <template v-if="kind === 'mac'">
        <i class="dot r" /><i class="dot y" /><i class="dot g" />
      </template>
      <span class="title">{{ title }}</span>
      <template v-if="kind === 'win'">
        <span class="wbtn">_</span><span class="wbtn">□</span><span class="wbtn x">×</span>
      </template>
    </div>
    <div class="body">
      <video v-if="video" :src="video" :poster="poster" autoplay muted loop playsinline :class="{ pixelated: pixel }" />
      <img v-else-if="src" :src="src" :class="{ pixelated: pixel }" :style="height ? { height, objectFit: 'cover', objectPosition: position || 'center' } : undefined" alt="">
      <slot />
    </div>
    <figcaption v-if="caption">
      {{ caption }}
    </figcaption>
  </figure>
</template>

<style scoped>
.frame {
  margin: 0;
  background: #1d2230;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.45), 0 2px 0 rgba(255, 255, 255, 0.04) inset;
}
.bar {
  height: 22px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 9px;
  background: linear-gradient(180deg, #2a3142, #222838);
  border-bottom: 1px solid rgba(0, 0, 0, 0.35);
}
.win .bar {
  background: linear-gradient(180deg, #1f4fa8, #163c86);
}
.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  display: inline-block;
}
.r { background: #ff5f57; }
.y { background: #febc2e; }
.g { background: #28c840; }
.title {
  flex: 1;
  text-align: center;
  font-size: 0.62rem;
  color: rgba(255, 255, 255, 0.72);
  font-family: var(--font-sans);
  margin-right: 34px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.win .title {
  text-align: left;
  margin-right: 0;
  color: #fff;
}
.wbtn {
  width: 16px;
  height: 14px;
  font-size: 9px;
  line-height: 13px;
  text-align: center;
  color: #fff;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
}
.wbtn.x {
  background: #c94a3c;
}
.body {
  line-height: 0;
  background: #000;
}
.body img,
.body video {
  width: 100%;
  display: block;
}
figcaption {
  font-size: 0.64rem;
  color: var(--muted);
  padding: 0.35rem 0.6rem 0.4rem;
  line-height: 1.3;
  background: var(--surface);
}
</style>
