<script setup lang="ts">
// How the Apple TV host reads its controls (TVOS_WEB T1b, 64b6e7ef): the Siri Remote as menu keys sampled
// through GameController every 25 ms, Bluetooth gamepads as the game's own joysticks through the sampler the
// AppKit host already had (OriginalGameControllerJoysticks, shared by Mac, iPad and Apple TV).
// A drawing of the controls, not to scale; every mapping is from the card and the T1b evidence.
const W = 420
const H = 262
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" width="100%" role="img" aria-label="Пульт Siri Remote: кольцо и свайпы — стрелки, центр — Enter, Menu не назначена; геймпад — джойстик игры">
    <!-- remote -->
    <g transform="translate(14 8)">
      <rect x="0" y="0" width="58" height="172" rx="20" fill="#1c2230" stroke="#4a5366" stroke-width="1.6" />
      <circle cx="29" cy="40" r="23" fill="#232a3b" stroke="var(--s1)" stroke-width="2" />
      <circle cx="29" cy="40" r="10" fill="#2e3647" stroke="var(--s1)" stroke-width="1.4" />
      <circle cx="16" cy="84" r="8" fill="#2e3647" stroke="var(--naruto)" stroke-width="1.4" />
      <path d="M18,80 l-4,4 l4,4" fill="none" stroke="var(--ink-2)" stroke-width="1.4" />
      <circle cx="42" cy="84" r="8" fill="#2e3647" />
      <rect x="38" y="81" width="8" height="6" rx="1" fill="none" stroke="var(--muted)" stroke-width="1" />
      <circle cx="16" cy="108" r="8" fill="#2e3647" />
      <circle cx="42" cy="108" r="8" fill="#2e3647" />
      <rect x="21" y="124" width="16" height="38" rx="8" fill="#2e3647" />
      <text x="29" y="137" text-anchor="middle" class="glyph">+</text>
      <text x="29" y="157" text-anchor="middle" class="glyph">−</text>
    </g>
    <!-- leaders -->
    <path d="M66,30 H112" class="ld" />
    <path d="M43,48 L58,58 H112" class="ld" />
    <path d="M30,92 L42,108 H112" class="ld" />

    <text x="118" y="25" class="k">кольцо и свайпы</text>
    <text x="118" y="39" class="v">→ стрелки в меню</text>
    <text x="118" y="56" class="k">центр или клик</text>
    <text x="118" y="70" class="v">→ Enter</text>
    <text x="118" y="104" class="k">Menu ‹</text>
    <text x="118" y="118" class="v">→ ничего: Esc в игре всегда</text>
    <text x="118" y="131" class="v">спрашивает «выйти?»</text>

    <!-- gamepad -->
    <g transform="translate(8 198)">
      <path d="M14,8 C24,0 54,0 64,8 L72,40 C74,52 62,56 56,46 L50,36 H28 L22,46 C16,56 4,52 6,40 Z" fill="#1c2230" stroke="var(--s1)" stroke-width="1.6" />
      <path d="M18,20 h6 v-6 h4 v6 h6 v4 h-6 v6 h-4 v-6 h-6 z" fill="#4a5366" />
      <circle cx="56" cy="16" r="2.6" fill="#5b6476" /><circle cx="62" cy="22" r="2.6" fill="#5b6476" />
      <circle cx="50" cy="22" r="2.6" fill="#5b6476" /><circle cx="56" cy="28" r="2.6" fill="#5b6476" />
    </g>
    <path d="M86,212 H112" class="ld" />
    <text x="118" y="196" class="k">Xbox, PlayStation, MFi по Bluetooth</text>
    <text x="118" y="210" class="v">→ джойстики самой игры: стик и крестовина —</text>
    <text x="118" y="223" class="v">оси, A/B/X/Y — кнопки 1–4. Один код опроса</text>
    <text x="118" y="236" class="v">на Mac, iPad и Apple TV</text>
    <text x="118" y="254" class="m">игра считает джойстики при запуске, как в Windows</text>
  </svg>
</template>

<style scoped>
.ld {
  fill: none;
  stroke: var(--axis);
  stroke-width: 1;
}
.k {
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-weight: 650;
  fill: var(--ink);
}
.v {
  font-family: var(--font-sans);
  font-size: 11px;
  fill: var(--ink-2);
}
.m {
  font-family: var(--font-sans);
  font-size: 10px;
  fill: var(--muted);
}
.glyph {
  font-family: var(--font-sans);
  font-size: 12px;
  fill: var(--muted);
}
</style>
