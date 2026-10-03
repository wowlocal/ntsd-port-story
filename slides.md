---
theme: default
title: NTSD 2.4 → macOS — история порта
titleTemplate: '%s'
info: |
  Как ИИ-агенты за 27 дней восстановили Windows-игру Naruto: The Setting Dawn 2.4
  из одного EXE нативным Swift-приложением для macOS — и проверили его против оригинала.
  Хроника по 463 коммитам, методология, техника, цифры.
colorSchema: dark
aspectRatio: 16/9
canvasWidth: 980
fonts:
  sans: Onest,Pixelify Sans,Unbounded
  mono: JetBrains Mono
  weights: '400,500,600,700'
transition: slide-left
mdc: true
lineNumbers: false
drawings:
  persist: false
routerMode: hash
exportFilename: ntsd-port-story
favicon: /img/icon.png
layout: hero
image: /img/menu-back-naruto-vs-sasuke.jpg
align: center
shade: 0.5
---

<div class="cover">
<Kicker>история одного порта · сентябрь — октябрь 2026</Kicker>
<h1 class="cover-title">NTSD 2.4<br><span class="hl">→ macOS</span></h1>
<p class="cover-sub">Как ИИ-агенты заново собрали Windows-игру из одного <code>.exe</code> — и доказали, что она играет так же</p>
<div class="cover-strip pixel">
<span><b>27</b> дней</span><span><b>463</b> коммита</span><span><b>1</b> EXE</span><span><b>0</b> строк исходников</span>
</div>
</div>

<style>
.cover { display: flex; flex-direction: column; align-items: center; }
.cover-title { font-size: 3.6rem !important; line-height: 1.02 !important; margin: 0.5rem 0 0.9rem !important; text-shadow: 0 6px 30px rgba(0,0,0,.7); }
.cover-sub { max-width: 30rem; font-size: 1.05rem; color: var(--ink) !important; text-shadow: 0 2px 12px rgba(0,0,0,.9); }
.cover-strip { display: flex; gap: 1.6rem; margin-top: 2rem; font-size: 0.85rem; color: var(--ink-2); background: rgba(10,13,19,.72); padding: .5rem 1.2rem; border: 1px solid var(--hair); }
.cover-strip b { color: var(--naruto); font-size: 1.15rem; margin-right: 0.3rem; font-weight: 400; }
</style>

<!--
Это история про то, как ИИ-агенты за 27 дней восстановили Windows-игру 2008 года из исполняемого файла — и про методологию, которая не давала им угадывать.
-->

---
src: ./pages/01-intro.md
---

---
src: ./pages/02-prologue.md
---

---
src: ./pages/03-sprint.md
---

---
src: ./pages/04-rules.md
---

---
src: ./pages/05-proof.md
---

---
src: ./pages/06-turn.md
---

---
src: ./pages/07-game.md
---

---
src: ./pages/08-crosscheck.md
---

---
src: ./pages/09-curiosities.md
---

---
src: ./pages/10-numbers.md
---

---
src: ./pages/11-agents.md
---

---
src: ./pages/12-lessons.md
---
