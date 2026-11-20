# EXPERIMENT (not a template): «فضلٌ ورحمة» in a paper-collage / scrapbook style, same palette and voice.
# Every slide is a torn paper sheet that slides in and lands on the stack. Words are cut-out paper chips that
# slap on when spoken; key words sit on torn coloured strips; icons are die-cut stickers held with tape;
# verses are on torn notebook paper with a stamped reference; marker doodles; paper grain; stop-motion boil.
import json, random
ROOT = "/home/user/Design-course"
DIR = f"{ROOT}/motion-graphics/fadl-allah-collage"
END = round(json.load(open(f"{DIR}/audio/timing.json"))["duration"] + 2.4, 2)
R = random.Random(7)

# icons: reuse the exact drawings of the original reel
_src = open(f"{ROOT}/motion-graphics/fadl-allah/tools/build.py", encoding="utf-8").read()
exec(_src[_src.index("SVG = '<svg"):_src.index("# recap: the four earlier icons")])

# ------------------------------------------------------------------ torn-paper shapes
def torn(top=0.0, bottom=0.0, side=0.0, step=4.0):
    """CSS polygon with jagged edges; amplitudes in % of the element box."""
    pts = []
    x = 0.0
    while x < 100:
        pts.append((x, R.uniform(0, top) if top else 0)); x += R.uniform(step * .6, step * 1.4)
    pts.append((100, R.uniform(0, top) if top else 0))
    y = 0.0
    while y < 100:
        y += R.uniform(step * 1.5, step * 3)
        if y < 100: pts.append((100 - (R.uniform(0, side) if side else 0), y))
    x = 100.0
    while x > 0:
        pts.append((x, 100 - (R.uniform(0, bottom) if bottom else 0))); x -= R.uniform(step * .6, step * 1.4)
    pts.append((0, 100 - (R.uniform(0, bottom) if bottom else 0)))
    y = 100.0
    while y > 0:
        y -= R.uniform(step * 1.5, step * 3)
        if y > 0: pts.append(((R.uniform(0, side) if side else 0), y))
    return "polygon(" + ",".join(f"{a:.1f}% {b:.1f}%" for a, b in pts) + ")"

def rot(lo=-4, hi=4): return round(R.uniform(lo, hi), 1)

# ------------------------------------------------------------------ collage pieces
def chips(top, fs, words, w=700, gap=0.06):
    """words: list of (text, time, colour) -> a row of torn paper chips, each slaps on when spoken."""
    out = f'      <div class="row" style="top:{top}px;font-size:{fs}px;font-weight:{w}">'
    for text, t, col in words:
        out += (f'<span class="chip c-{col} boil" data-t="{t}" data-r="{rot(-5, 5)}" '
                f'style="clip-path:{torn(7, 7, 1.6, 9)}">{text}</span>')
    return out + '</div>\n'
def strip(top, fs, text, t, col="teal", r=None):
    r = rot(-4, 4) if r is None else r
    return (f'      <div class="row" style="top:{top}px;font-size:{fs}px;font-weight:700">'
            f'<span class="strip c-{col} boil" data-strip="{t}" data-r="{r}" style="clip-path:{torn(5, 5, 3.5, 3)}">{text}</span></div>\n')
def tape(x, y, r, col="w", w=170):
    return (f'<span class="tape t-{col}" style="left:{x}px;top:{y}px;width:{w}px;rotate:{r}deg;'
            f'clip-path:{torn(0, 0, 6, 12)}"></span>')
def sticker(top, size, svg, at, r=None, left=None):
    r = rot(-7, 7) if r is None else r
    pos = f"left:{left}px;" if left is not None else f"left:50%;margin-left:-{size // 2}px;"
    return (f'      <div class="sticker boil" data-in="{at}" data-r="{r}" style="top:{top}px;{pos}width:{size}px;height:{size}px">'
            f'<div class="die">{svg}</div><div class="ic">{svg}</div>'
            f'{tape(size // 2 - 85, -22, rot(-9, 9))}</div>\n')
def note(top, at, lines_html, r=None, fs=86):
    r = rot(-2, 2) if r is None else r
    return (f'      <div class="note boil" data-in="{at}" data-r="{r}" style="top:{top}px;font-size:{fs}px">'
            f'<div class="paper" style="clip-path:{torn(2.2, 2.2, 0, 3)}">{lines_html}</div>'
            f'{tape(40, -26, -12)}{tape(760, -24, 10, "g")}</div>\n')
def nline(text, t): return f'<span class="nl" data-t="{t}">{text}</span>'
def stamp(top, text, at, side="left:150px", r=-8):
    return f'      <div class="stamp" data-stamp="{at}" style="top:{top}px;{side};rotate:{r}deg">{text}</div>\n'
def doodle(d, at, col="#b5dc55", w=9):
    return (f'      <svg class="doodle" viewBox="0 0 1080 1920"><path data-doodle="{at}" d="{d}" stroke="{col}" '
            f'stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>\n')
def label(top, fs, text_words, at, r=-2):
    inner = " ".join(f'<span class="lw" data-t="{t}">{w}</span>' for w, t in text_words)
    return (f'      <div class="row" style="top:{top}px;font-size:{fs}px;font-weight:700">'
            f'<span class="label boil" data-in="{at}" data-r="{r}" style="clip-path:{torn(0, 0, 4, 10)}">{inner}</span></div>\n')
def scene(i, start, body):
    r = 0 if i == 1 else rot(-1.6, 1.6)
    return (f'    <section class="scene" id="s{i}" data-start="{start}" data-r="{r}">\n'
            f'      <div class="sheetwrap"><div class="sheet" style="clip-path:{torn(0.9, 0.6, 0.5, 2)}"></div></div>\n'
            f'{body}    </section>\n\n')

S = []
# 1 — صلاة الفجر
S.append(scene(1, 0,
  sticker(270, 330, ic_fajr(0.05), 0.0, -6) +
  chips(650, 64, [("تسعد", 0.05, "white"), ("بمحافظتك", 0.48, "white"), ("على", 1.28, "white"), ("صلاة", 1.36, "white")]) +
  strip(800, 190, "الفجر", 1.62, "teal", -3) +
  doodle("M300 1075 C380 1058 460 1092 540 1072 S700 1058 790 1078", 1.95) +
  chips(1110, 78, [("في", 2.06, "lime"), ("جماعة", 2.18, "lime")])))
# 2 — تتلذذ بقراءة القرآن
S.append(scene(2, 2.66,
  sticker(270, 340, ic_book(2.62), 2.6, 5) +
  strip(690, 180, "تتلذّذ", 2.66, "lime", 2) +
  doodle("M196 690 l14 36 l36 14 l-36 14 l-14 36 l-14 -36 l-36 -14 l36 -14 Z", 2.95, "#1b7a9c", 6) +
  doodle("M884 1000 l10 26 l26 10 l-26 10 l-10 26 l-10 -26 l-26 -10 l26 -10 Z", 3.75, "#b5dc55", 6) +
  chips(980, 92, [("بقراءة", 3.20, "white"), ("القرآن", 3.70, "teal")])))
# 3 — سماع ما ينفع
S.append(scene(3, 4.59,
  sticker(270, 330, ic_car(4.55), 4.5, -4) +
  chips(660, 58, [("تستغلّ", 4.59, "white"), ("وقتك", 4.92, "white"), ("في", 5.26, "white"), ("السيارة", 5.38, "white")], 600) +
  chips(770, 92, [("في", 5.90, "white"), ("سماع", 6.06, "white"), ("ما", 6.42, "white"), ("ينفع", 6.56, "teal")]) +
  label(950, 64, [("وما", 7.08), ("يدفع", 7.34), ("للطاعة", 7.74)], 6.95, -2) +
  doodle("M170 1080 C130 1010 150 960 214 940 M190 924 L216 940 L198 966", 7.9, "#1b7a9c", 7)))
# 4 — صحبة صالحة + الآية
S.append(scene(4, 8.61,
  sticker(250, 290, ic_friends(8.55), 8.5, 3) +
  chips(560, 80, [("تأنس", 8.61, "white"), ("بصحبةٍ", 8.92, "white"), ("صالحةٍ", 9.24, "teal")]) +
  chips(700, 54, [("تتذكر", 9.68, "white"), ("معهم", 10.16, "white"), ("ما", 10.56, "white"), ("خُلقت", 10.70, "white"), ("لأجله:", 11.06, "white")], 600) +
  note(830, 11.35, nline("﴿وَمَا خَلَقْتُ الْجِنَّ", "11.60,11.98,12.45")
       + nline('وَالْإِنسَ إِلَّا <span class="hm" data-hm="13.95">لِيَعْبُدُونِ﴾</span>', "12.82,13.16,13.56"), -1.4, 88) +
  stamp(1200, "الذاريات: ٥٦", 13.9, "left:140px", -8)))
# 5 — كل هذه الأمور فضل ورحمة (moodboard of the four stickers)
mini = [ic_fajr(-9), ic_book(-9), ic_car(-9), ic_friends(-9)]
pos = [(780, 270, -9), (540, 300, 7), (300, 262, -5), (60, 300, 8)]
S.append(scene(5, 14.47,
  "".join(sticker(y, 210, mini[k], 14.45 + k * 0.14, r, x) for k, (x, y, r) in enumerate(pos)) +
  chips(560, 70, [("كلُّ", 14.47, "white"), ("هذه", 14.56, "white"), ("الأمور", 14.66, "white")]) +
  strip(670, 150, "فضلٌ", 15.05, "teal", -4) +
  strip(915, 150, "ورحمةٌ", 15.86, "lime", 3) +
  doodle("M540 650 C770 640 940 750 935 905 C930 1080 770 1170 540 1170 C310 1170 140 1090 140 915 C140 770 300 660 520 662",
         16.3, "#1b7a9c", 6) +
  chips(1215, 70, [("من", 16.73, "white"), ("اللهِ", 16.85, "white"), ("سبحانه", 16.98, "white"), ("وتعالى", 17.62, "white")])))
# 6 — ولكن الله حبب إليكم الإيمان وزينه في قلوبكم
S.append(scene(6, 18.92,
  sticker(240, 300, ic_heart(18.9, 22.06, 22.3), 18.85, -5) +
  note(600, 18.95, nline("﴿وَلَٰكِنَّ اللَّهَ حَبَّبَ", "18.92,19.14,19.38")
       + nline('إِلَيْكُمُ <span class="acc">الْإِيمَانَ</span>', "19.82,20.26")
       + nline('وَزَيَّنَهُ فِي <span class="hm" data-hm="22.3">قُلُوبِكُمْ﴾</span>', "21.14,21.70,22.06"), 1.2, 92) +
  stamp(1185, "الحجرات: ٧", 22.6, "right:150px", 7) +
  '      <div class="sendchip" data-send="23.1"><svg viewBox="0 0 48 48" fill="none" stroke="#151718" stroke-width="3.2" '
  'stroke-linejoin="round" stroke-linecap="round"><path d="M43 5 L5 19 L21 27 L29 43 Z"/><path d="M43 5 L21 27"/></svg></div>\n'))

HTML = r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>فضلٌ ورحمة — كولاج</title>
<!-- تجربة: ستايل الكولاج (غير معتمد كقالب). يُولَّد من tools/build.py -->
<style>
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-400.ttf") format("truetype"); font-weight: 400; }
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-500.ttf") format("truetype"); font-weight: 500; }
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-600.ttf") format("truetype"); font-weight: 600; }
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-700.ttf") format("truetype"); font-weight: 700; }
  :root { --bg: #f3f5f4; --ink: #151718; --muted: #7b8386; --teal: #1b7a9c; --teal-line: #4a93b0; --lime: #b5dc55; --desk: #dfe6e3; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; }
  body { background: #1d2124; font-family: "Plex Ar", system-ui, sans-serif; color: var(--ink); overflow: hidden;
         display: flex; flex-direction: column; align-items: center; justify-content: center; }
  #viewport { position: relative; flex: 1; width: 100%; overflow: hidden; }
  #stage { position: absolute; left: 50%; top: 50%; width: 1080px; height: 1920px; transform-origin: 50% 50%; overflow: hidden;
           background: radial-gradient(ellipse 90% 70% at 50% 45%, #e9eeec, var(--desk) 70%, #cfd9d5); }
  body.render { background: var(--desk); display: block; }
  body.render #viewport { position: fixed; inset: 0; }
  body.render #stage { left: 0; top: 0; transform: none !important; }
  body.render #controls { display: none; }

  /* paper sheets stacking on the desk */
  .scene { position: absolute; inset: 0; transform-origin: 50% 60%; }
  .sheetwrap { position: absolute; left: 34px; right: 34px; top: 120px; bottom: 120px; filter: drop-shadow(0 18px 26px rgba(20, 50, 60, .22)) drop-shadow(0 2px 2px rgba(20, 50, 60, .18)); }
  .sheet { position: absolute; inset: 0; background: var(--bg); }
  .sheet::after { content: ""; position: absolute; inset: 0; opacity: .5; mix-blend-mode: multiply;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='p'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/><feColorMatrix values='0 0 0 0 .55  0 0 0 0 .58  0 0 0 0 .56  0 0 0 .18 0'/></filter><rect width='400' height='400' filter='url(%23p)'/></svg>"); }

  .row { position: absolute; left: 60px; right: 60px; text-align: center; line-height: 1.05; filter: drop-shadow(0 5px 0 rgba(20, 50, 60, .14)) drop-shadow(0 10px 14px rgba(20, 50, 60, .12)); }
  .chip { display: inline-block; padding: .06em .3em .2em; margin: .07em .05em; white-space: nowrap; }
  .strip { display: inline-block; padding: .02em .38em .14em; white-space: nowrap; transform-origin: 100% 50%; }
  .c-white { background: #fff; color: var(--ink); }
  .c-teal { background: var(--teal); color: #fff; }
  .c-lime { background: var(--lime); color: var(--ink); }
  .label { display: inline-block; padding: .14em .7em .26em; background: rgba(181, 220, 85, .85); color: var(--ink);
           background-image: repeating-linear-gradient(90deg, rgba(255,255,255,.18) 0 2px, transparent 2px 9px); }
  .lw { display: inline-block; }

  .tape { position: absolute; height: 52px; background: rgba(255, 255, 255, .62); box-shadow: 0 1px 2px rgba(0,0,0,.06);
          background-image: repeating-linear-gradient(90deg, rgba(255,255,255,.4) 0 2px, transparent 2px 7px); z-index: 3; }
  .tape.t-g { background-color: rgba(181, 220, 85, .55); }

  .sticker { position: absolute; filter: drop-shadow(0 10px 12px rgba(20, 50, 60, .22)); }
  .sticker .die, .sticker .ic { position: absolute; inset: 0; }
  .sticker svg { width: 100%; height: 100%; overflow: visible; }
  .die * { stroke: #fff !important; stroke-width: 30px !important; fill: #fff !important; opacity: 1 !important; fill-opacity: 1 !important; }

  .note { position: absolute; left: 70px; right: 70px; filter: drop-shadow(0 10px 14px rgba(20, 50, 60, .18)); }
  .note .paper { background: #fff; padding: .55em .7em .7em; text-align: center; line-height: 1.62; font-weight: 600;
                 background-image: linear-gradient(90deg, transparent 64px, rgba(181,220,85,.7) 64px 68px, transparent 68px),
                                   repeating-linear-gradient(180deg, transparent 0 calc(1.62em - 2px), rgba(27,122,156,.16) calc(1.62em - 2px) 1.62em);
                 background-position: 0 .5em; }
  .nl { display: block; white-space: nowrap; }
  .nl .k { display: inline-block; }
  .acc { color: var(--teal); }
  .hm { background-image: linear-gradient(100deg, transparent 2%, rgba(181,220,85,.85) 4%, rgba(181,220,85,.7) 92%, transparent 97%);
        background-repeat: no-repeat; background-size: 0% 46%; background-position: 100% 84%; padding: 0 .1em; }
  .stamp { position: absolute; font-size: 40px; font-weight: 700; color: var(--teal); border: 5px solid var(--teal); border-radius: 12px;
           padding: 4px 22px 10px; mix-blend-mode: multiply; opacity: 0; letter-spacing: .5px; }
  .doodle { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; overflow: visible; }
  .sendchip { position: absolute; left: 120px; top: 1330px; width: 120px; height: 120px; background: #fff; padding: 24px; border-radius: 26px;
              filter: drop-shadow(0 8px 10px rgba(20, 50, 60, .2)); rotate: -6deg; }
  .sendchip svg { width: 100%; height: 100%; }

  #grain { position: absolute; inset: -100px; pointer-events: none; opacity: .14; mix-blend-mode: multiply;
           background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .3  0 0 0 0 .3  0 0 0 0 .3  0 0 0 1 0'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>"); }
  #handle { position: absolute; left: 0; right: 0; top: 1700px; text-align: center; direction: ltr; font-size: 34px; color: #8e999c; letter-spacing: .5px; }

  #safe { display: none; pointer-events: none; } #safe.on { display: block; }
  #safe div { position: absolute; background: rgba(255, 60, 60, .14); border: 2px dashed rgba(255, 60, 60, .5); }
  #controls { width: min(760px, 100%); padding: 12px 16px 16px; display: flex; gap: 12px; align-items: center; color: #e8ecee; font-size: 15px; direction: ltr; }
  #controls button { font: inherit; color: inherit; background: #2f3539; border: 1px solid #454c51; border-radius: 8px; padding: 7px 12px; cursor: pointer; white-space: nowrap; }
  #controls input[type=range] { flex: 1; accent-color: #b5dc55; min-width: 60px; }
  #time { font-variant-numeric: tabular-nums; min-width: 92px; text-align: center; }
</style>
</head>
<body>
<div id="viewport">
  <div id="stage">
__SCENES__
    <div id="grain"></div>
    <div id="handle">@abdulla_7amdan</div>
    <div id="safe" style="position:absolute;inset:0">
      <div style="left:0;right:0;top:0;height:220px"></div>
      <div style="left:0;right:0;bottom:0;height:380px"></div>
      <div style="right:0;width:140px;top:1040px;bottom:380px"></div>
    </div>
  </div>
</div>

<div id="controls">
  <button id="play">▶ تشغيل</button>
  <input type="range" id="scrub" min="0" max="40" step="0.01" value="0">
  <span id="time"></span>
  <button id="soundBtn" title="تشغيل مع الصوت">🔊</button>
  <button id="safeBtn">Safe zone</button>
</div>
<audio id="voice" src="audio/voice-clean.m4a" preload="auto"></audio>

<script src="gsap.min.js"></script>
<script>
(() => {
  const params = new URLSearchParams(location.search);
  const END = __END__;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const tl = gsap.timeline({ paused: true, defaults: { ease: 'power3.out' } });

  /* note lines -> word spans */
  $$('.nl').forEach(el => {
    const walk = node => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(p => {
          if (!p) return;
          if (/^\s+$/.test(p)) return frag.appendChild(document.createTextNode(p));
          const s = document.createElement('span'); s.className = 'k'; s.textContent = p; frag.appendChild(s);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1) walk(n);
    });
    walk(el);
  });

  /* base rotations live in the CSS `rotate` property (the stop-motion boil adds to it) */
  const boil = $$('.boil');
  boil.forEach(el => { el.style.rotate = (+el.dataset.r || 0) + 'deg'; });

  /* ---- paper sheets: each slide lands on the stack, in step with the first spoken word ---- */
  const scenes = $$('.scene'), starts = scenes.map(s => +s.dataset.start);
  scenes.forEach((S, i) => {
    const a = starts[i], r = +S.dataset.r;
    if (i === 0) { tl.fromTo(S, { y: 60, rotation: -3, opacity: 0 }, { y: 0, rotation: r, opacity: 1, duration: 0.6 }, 0); return; }
    gsap.set(S, { y: 2100, rotation: i % 2 ? 7 : -7 });
    const t0 = a - 0.32;
    tl.to(S, { y: 0, rotation: r, duration: 0.62, ease: 'power3.out' }, t0)
      .to(S, { keyframes: { y: [0, -10, 0] }, duration: 0.3, ease: 'sine.inOut' }, t0 + 0.6)
      .to(scenes[i - 1], { scale: 0.965, y: 16, duration: 0.6, ease: 'power2.out' }, t0);
    if (i >= 2) tl.set(scenes[i - 2], { autoAlpha: 0 }, t0 + 0.7);
  });

  /* ---- pieces ---- */
  $$('.chip[data-t]').forEach(c => tl.fromTo(c, { scale: 1.5, opacity: 0, rotation: 9 }, { scale: 1, opacity: 1, rotation: 0, duration: 0.32, ease: 'back.out(2.2)' }, +c.dataset.t - 0.08));
  $$('[data-strip]').forEach(s => tl.fromTo(s, { scaleX: 0.15, opacity: 0 }, { scaleX: 1, opacity: 1, duration: 0.38, ease: 'power3.out' }, +s.dataset.strip - 0.12)
      .fromTo(s, { scale: 1.08 }, { scale: 1, duration: 0.25, ease: 'back.out(2)' }, +s.dataset.strip + 0.2));
  $$('.sticker').forEach(st => { const t = +st.dataset.in;
    tl.fromTo(st, { scale: 1.6, opacity: 0, rotation: -16 }, { scale: 1, opacity: 1, rotation: 0, duration: 0.45, ease: 'back.out(1.7)' }, t)
      .fromTo(st.querySelector('.tape'), { scale: 1.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.22, ease: 'power2.out' }, t + 0.3); });
  $$('.note').forEach(n => { const t = +n.dataset.in;
    tl.fromTo(n, { y: 140, opacity: 0, rotation: -5 }, { y: 0, opacity: 1, rotation: 0, duration: 0.55, ease: 'expo.out' }, t);
    $$('.tape', n).forEach((tp, k) => tl.fromTo(tp, { scale: 1.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.2 }, t + 0.25 + k * 0.1)); });
  $$('.nl').forEach(L => { const ts = L.dataset.t.split(',').map(Number);
    $$('.k', L).forEach((w, i) => tl.fromTo(w, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.35 }, (ts[Math.min(i, ts.length - 1)] + Math.max(0, i - ts.length + 1) * 0.1) - 0.05)); });
  $$('.label').forEach(l => tl.fromTo(l, { scaleX: 0.1, opacity: 0, transformOrigin: '100% 50%' }, { scaleX: 1, opacity: 1, duration: 0.35 }, +l.dataset.in));
  $$('.lw').forEach(w => tl.fromTo(w, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.3 }, +w.dataset.t - 0.05));
  $$('[data-hm]').forEach(h => tl.to(h, { backgroundSize: '100% 46%', duration: 0.45, ease: 'power2.inOut' }, +h.dataset.hm));
  $$('[data-stamp]').forEach(s => tl.fromTo(s, { scale: 2.1, opacity: 0 }, { scale: 1, opacity: 0.92, duration: 0.28, ease: 'power4.in' }, +s.dataset.stamp)
      .to(s, { keyframes: { x: [0, -3, 2, 0] }, duration: 0.2 }, +s.dataset.stamp + 0.28));
  $$('[data-doodle]').forEach(p => { const L = p.getTotalLength(); gsap.set(p, { strokeDasharray: L, strokeDashoffset: L });
    tl.to(p, { strokeDashoffset: 0, duration: 0.55, ease: 'power2.inOut' }, +p.dataset.doodle); });
  $$('[data-send]').forEach(s => tl.fromTo(s, { x: -160, y: 160, opacity: 0, rotation: -30 }, { x: 0, y: 0, opacity: 1, rotation: 0, duration: 0.8, ease: 'back.out(1.6)' }, +s.dataset.send)
      .to(s, { y: -10, duration: 0.4, ease: 'sine.inOut', yoyo: true, repeat: 1 }, +s.dataset.send + 0.9));

  /* ---- icon motion (only the ink layer .ic; the white die-cut layer stays whole) ---- */
  $$('.ic path.draw, .ic circle.draw').forEach(p => { const L = p.getTotalLength(); gsap.set(p, { strokeDasharray: L, strokeDashoffset: L }); });
  $$('.ic [data-draw]').forEach(p => { const t = +p.dataset.draw; if (t > 0) tl.to(p, { strokeDashoffset: 0, duration: 0.6, ease: 'power2.inOut' }, t); else gsap.set(p, { strokeDashoffset: 0 }); });
  $$('.ic [data-pop]').forEach(g => { const t = +g.dataset.pop; if (t > 0) tl.fromTo(g, { scale: 0, opacity: 0, transformOrigin: '50% 50%' }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(2.4)' }, t); });
  $$('.ic [data-rise]').forEach(g => { const t = +g.dataset.rise; if (t > 0) tl.fromTo(g, { y: 46, opacity: 0 }, { y: 0, opacity: 1, duration: 1.0, ease: 'expo.out' }, t); });
  $$('.ic [data-wave]').forEach(g => { const t = +g.dataset.wave; if (t > 0) [...g.children].forEach((w, k) =>
      tl.fromTo(w, { opacity: 0.35, scaleY: 0.35, transformOrigin: '50% 100%' }, { opacity: 1, scaleY: 1, duration: 0.28, ease: 'sine.inOut', yoyo: true, repeat: 9 }, t + k * 0.09)); });
  $$('.ic [data-fill]').forEach(p => tl.to(p, { attr: { 'fill-opacity': 0.95 }, duration: 0.6, ease: 'power2.out' }, +p.dataset.fill));
  $$('.ic [data-beat]').forEach(b => { const st = b.closest('.sticker'), t = +b.dataset.beat;
    [0, 0.55].forEach(d => tl.to(st, { keyframes: { scale: [1, 1.08, 1, 1.04, 1] }, duration: 0.45, ease: 'none' }, t + d)); });
  $$('.die [data-fill]').forEach(p => p.setAttribute('fill-opacity', 1));

  /* ---- stop-motion boil (8 fps) + grain shimmer, both driven by timeline time ---- */
  const grain = $('#grain');
  const hash = (n, k) => { const x = Math.sin(n * 12.9898 + k * 78.233) * 43758.5453; return x - Math.floor(x); };
  tl.eventCallback('onUpdate', () => {
    const f = Math.floor(tl.time() * 8);
    boil.forEach((el, k) => {
      el.style.translate = `${(hash(f, k) - .5) * 2.2}px ${(hash(f, k + 99) - .5) * 2.2}px`;
      el.style.rotate = ((+el.dataset.r || 0) + (hash(f, k + 7) - .5) * 0.7) + 'deg';
    });
    grain.style.transform = `translate(${(hash(f, 1) - .5) * 80}px, ${(hash(f, 2) - .5) * 80}px)`;
    sync();
  });
  tl.to({}, { duration: 0.001 }, END - 0.001);

  const stage = $('#stage'), vp = $('#viewport'), voice = $('#voice');
  const fit = () => { stage.style.transform = `translate(-50%, -50%) scale(${Math.min(vp.clientWidth / 1080, vp.clientHeight / 1920)})`; };
  if (params.has('render')) document.body.classList.add('render'); else { addEventListener('resize', fit); fit(); }
  window.__duration = END;
  window.__scenes = Object.fromEntries(starts.map((s, i) => ['s' + (i + 1), s]).concat([['end', END]]));
  window.__seek = t => { tl.seek(t, false); };
  window.__ready = document.fonts.ready.then(() => true);

  const playBtn = $('#play'), scrub = $('#scrub'), time = $('#time');
  let withSound = false;
  scrub.max = END;
  function sync() { scrub.value = tl.time(); time.textContent = `${tl.time().toFixed(2)} / ${END.toFixed(1)}`; }
  sync();
  tl.eventCallback('onComplete', () => { playBtn.textContent = '↺ إعادة'; voice.pause(); });
  const play = () => { if (withSound) { voice.currentTime = tl.time(); voice.play().catch(() => {}); } tl.play(); };
  const pause = () => { tl.pause(); voice.pause(); };
  playBtn.onclick = () => {
    if (tl.progress() >= 1) { tl.seek(0); play(); } else if (tl.paused()) play(); else pause();
    playBtn.textContent = tl.paused() ? '▶ تشغيل' : '❚❚ إيقاف';
  };
  $('#soundBtn').onclick = () => { withSound = !withSound; $('#soundBtn').style.opacity = withSound ? 1 : .5; if (!tl.paused()) { voice.currentTime = tl.time(); withSound ? voice.play() : voice.pause(); } };
  $('#soundBtn').style.opacity = .5;
  scrub.oninput = () => { pause(); tl.seek(+scrub.value); playBtn.textContent = '▶ تشغيل'; sync(); };
  $('#safeBtn').onclick = () => $('#safe').classList.toggle('on');
  addEventListener('keydown', e => { if (e.code === 'Space') { e.preventDefault(); playBtn.click(); } });
  if (params.has('t')) tl.seek(+params.get('t'));
  else if (!params.has('render')) window.__ready.then(() => { tl.play(); playBtn.textContent = '❚❚ إيقاف'; });
})();
</script>
</body>
</html>
'''

out = HTML.replace("__SCENES__", "".join(S)).replace("__END__", str(END))
open(f"{DIR}/index.html", "w", encoding="utf-8").write(out)
print("written", len(out), "END", END)
