---
theme: default
title: NTSD 2.4 → macOS — история порта
titleTemplate: '%s'
info: |
  Как ИИ-агенты за 27 дней восстановили Windows-игру Naruto: The Setting Dawn 2.4
  из одного EXE нативным Swift-приложением для macOS — и проверили его против оригинала,
  а за следующие десять дней перенесли ту же игру на Linux, Windows, iPad, Android,
  Apple TV и в браузер и довели её до 60 кадров в секунду на бюджетном телефоне,
  а ещё через неделю она пошла на Steam Deck и вышла вторым релизом.
  Хроника по 756 коммитам и 31 коммиту main после них, методология, техника, цифры.
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
<span><b>37</b> дней</span><span><b>756</b> коммитов</span><span><b>1</b> EXE</span><span><b>0</b> строк исходников</span><span><b>14</b> хостов</span>
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
Это история про то, как ИИ-агенты за 27 дней восстановили Windows-игру 2008 года из исполняемого файла — и про методологию, которая не давала им угадывать. Главы 13–18 — десять дней после релиза: та же игра на девяти хостах, на телефоне, на телевизоре и в браузере. Глава 19 — 31 коммит main за 16–19 октября: Steam Deck, кнопки от игрока из Discord, второй релиз. Цифры обложки — с 7 сентября по 13 октября, коммит 5f5a8ee4; 14 хостов — 9 из главы 13 и Apple TV, WASI, Chromium, WebKit и iPhone, все пятеро в симуляторе или стенде.
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
src: ./pages/12-community.md
---

---
src: ./pages/13-hosts.md
---

---
src: ./pages/14-phone.md
---

---
src: ./pages/15-tier2.md
---

---
src: ./pages/16-loading.md
---

---
src: ./pages/17-web-tv.md
---

---
src: ./pages/18-release.md
---

---
src: ./pages/19-after.md
---

---
src: ./pages/20-lessons.md
---
