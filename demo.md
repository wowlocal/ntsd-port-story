---
theme: default
title: Белковый на подхвате — NTSD 2.4, демодень
titleTemplate: '%s'
info: |
  Белковый на подхвате. Месяц с агентом, который портировал игру по одному exe.
  Доклад на 10–15 минут для демодня.
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
exportFilename: ntsd-demo-day-trust
favicon: /img/icon.png
layout: hero
image: /img/menu-back-naruto-vs-sasuke.jpg
align: center
shade: 0.5
---

<div class="cover">
<Kicker>демодень · 26 октября 2026</Kicker>
<h1 class="cover-title">Белковый<br><span class="hl">на подхвате</span></h1>
<p class="cover-sub">Месяц с агентом, который портировал игру по одному exe</p>
<div class="cover-strip pixel">
<span><b>1</b> EXE</span><span><b>0</b> строк исходников</span><span><b>37</b> дней</span><span><b>756</b> коммитов</span><span><b>58 / 58</b> матчей = оригинал</span>
</div>
</div>

<style>
.cover { display: flex; flex-direction: column; align-items: center; }
.cover-title { font-size: 3.6rem !important; line-height: 1.02 !important; margin: 0.5rem 0 0.9rem !important; text-shadow: 0 6px 30px rgba(0,0,0,.7); }
.cover-sub { max-width: 34rem; font-size: 1.05rem; color: var(--ink) !important; text-shadow: 0 2px 12px rgba(0,0,0,.9); }
.cover-strip { display: flex; gap: 1.4rem; margin-top: 1.8rem; font-size: 0.8rem; color: var(--ink-2); background: rgba(10,13,19,.72); padding: .5rem 1.2rem; border: 1px solid var(--hair); }
.cover-strip b { color: var(--naruto); font-size: 1.1rem; margin-right: 0.3rem; font-weight: 400; }
</style>

<!--
Доклад на 10–15 минут для демодня. Схема: проблема → контекст → решение → демо → результаты → уроки; часть подсвечена в правом верхнем углу каждого слайда. Полная версия — 195 слайдов, ветка main.
-->

---
src: ./pages/demo-day.md
---
