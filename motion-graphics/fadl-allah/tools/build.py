# Builds motion-graphics/fadl-allah/index.html — القالب النهاري بدون مربعات (template ٣), no title / no counter.
# Voice-first reel. Times = audio/voice-clean.m4a. Transition: «مدّ ضوئي» (day variant), continuous with the speech.
# Declarative: data-t (spoken word times), data-in / data-fx (big|up|card|pill|chip), data-mark,
# icon attributes: data-draw, data-pop, data-rise, data-wave, data-fill, data-beat, data-glow.
import json
ROOT = "/home/user/Design-course"
DIR = f"{ROOT}/motion-graphics/fadl-allah"
END = round(json.load(open(f"{DIR}/audio/timing.json"))["duration"] + 2.4, 2)

def kl(text, t, cls=""):
    return f'<span class="line kline {cls}" data-t="{t}">{text}</span>'
def c(top, fs, w, inner, at, fx="up", lh=None):
    lhs = f"line-height:{lh};" if lh else ""
    return f'      <div class="c" style="top:{top}px;font-size:{fs}px;font-weight:{w};{lhs}" data-in="{at}" data-fx="{fx}">{inner}</div>\n'
def pill(top, fs, text, t, at):
    return f'      <div class="pillrow" style="top:{top}px;font-size:{fs}px" data-in="{at}" data-fx="pill"><span class="pill"><span class="kline" data-t="{t}">{text}</span></span></div>\n'
def ref(top, text, at):
    return f'      <div class="refchip" style="top:{top}px" data-in="{at}" data-fx="chip"><span>{text}</span></div>\n'
def mark(text, at): return f'<span class="mark" data-mark="{at}">{text}</span>'
def card(top, at, inner):
    return f'      <div class="glass" style="top:{top}px" data-in="{at}" data-fx="card">{inner}</div>\n'
def icon(top, size, svg, cls=""):
    return f'      <div class="icon {cls}" style="top:{top}px;width:{size}px;height:{size}px;margin-left:-{size // 2}px">{svg}</div>\n'
def scene(i, start, body):
    return f'    <!-- ===== S{i} ({start}s) ===== -->\n    <section class="scene" id="s{i}" data-start="{start}">\n{body}    </section>\n\n'

# ------------------------------------------------------------------ icons (viewBox 200×200, stroke drawings)
SVG = '<svg viewBox="0 0 200 200" fill="none" stroke-linecap="round" stroke-linejoin="round">{}</svg>'
def ic_fajr(t):   # the sun rises behind a mosque over the horizon
    return SVG.format(f'''
        <g data-rise="{t + 0.35}"><circle cx="100" cy="96" r="40" fill="#b5dc55"/>
          <g stroke="#b5dc55" stroke-width="6"><path d="M100 42v-16M60 58l-11-11M140 58l11-11M44 96H28M156 96h16"/></g></g>
        <path class="draw" data-draw="{t}" stroke="var(--teal)" stroke-width="7" fill="var(--bg)" d="M74 150 V124 Q74 98 100 90 Q126 98 126 124 V150"/>
        <path class="draw" data-draw="{t + 0.15}" stroke="var(--teal)" stroke-width="7" fill="var(--bg)" d="M142 150 V104 L148 94 L154 104 V150"/>
        <path class="draw" data-draw="{t + 0.3}" stroke="var(--teal)" stroke-width="5" d="M100 90 V80"/>
        <path class="draw" data-draw="{t - 0.05}" stroke="var(--teal)" stroke-width="7" d="M22 150 H178"/>
        <path class="draw" data-draw="{t + 0.4}" stroke="var(--teal-line)" stroke-width="5" d="M90 150 V134 Q90 126 100 124 Q110 126 110 134 V150"/>''')
def ic_book(t):    # an open mushaf, light rising from it
    return SVG.format(f'''
        <path class="draw" data-draw="{t}" stroke="var(--teal)" stroke-width="7" fill="var(--bg)" d="M100 74 C80 62 52 60 26 66 V154 C52 148 80 150 100 162 C120 150 148 148 174 154 V66 C148 60 120 62 100 74 Z"/>
        <path class="draw" data-draw="{t + 0.25}" stroke="var(--teal)" stroke-width="5" d="M100 74 V162"/>
        <g stroke="var(--teal-line)" stroke-width="4">
          <path class="draw" data-draw="{t + 0.4}" d="M86 94 C70 86 54 85 40 88"/><path class="draw" data-draw="{t + 0.47}" d="M86 112 C70 104 54 103 40 106"/>
          <path class="draw" data-draw="{t + 0.54}" d="M86 130 C72 123 60 122 50 124"/>
          <path class="draw" data-draw="{t + 0.4}" d="M114 94 C130 86 146 85 160 88"/><path class="draw" data-draw="{t + 0.47}" d="M114 112 C130 104 146 103 160 106"/>
          <path class="draw" data-draw="{t + 0.54}" d="M114 130 C128 123 140 122 150 124"/></g>
        <g stroke="#b5dc55" stroke-width="6" data-pop="{t + 0.7}"><path d="M100 48 V30"/><path d="M74 54 L64 40"/><path d="M126 54 L136 40"/></g>''')
def ic_car(t):     # a car with sound waves (listening on the road)
    return SVG.format(f'''
        <path class="draw" data-draw="{t}" stroke="var(--teal)" stroke-width="7" fill="var(--bg)" d="M28 140 V118 Q28 108 38 106 L60 103 L78 80 Q82 75 90 75 H130 Q138 75 142 81 L156 103 L168 106 Q176 108 176 118 V140 Z"/>
        <path class="draw" data-draw="{t + 0.2}" stroke="var(--teal-line)" stroke-width="5" d="M70 103 L84 84 H100 V103 Z M108 84 H128 L142 103 H108 Z"/>
        <circle class="draw" data-draw="{t + 0.3}" cx="64" cy="142" r="15" stroke="var(--teal)" stroke-width="7" fill="var(--bg)"/>
        <circle class="draw" data-draw="{t + 0.35}" cx="142" cy="142" r="15" stroke="var(--teal)" stroke-width="7" fill="var(--bg)"/>
        <g stroke="#b5dc55" stroke-width="6" data-wave="{t + 0.6}">
          <path d="M86 56 Q100 44 114 56"/><path d="M76 46 Q100 26 124 46"/><path d="M66 36 Q100 8 134 36"/></g>''')
def ic_friends(t):  # three companions, a small heart rises above them
    return SVG.format(f'''
        <circle class="draw" data-draw="{t}" cx="100" cy="74" r="20" stroke="var(--teal)" stroke-width="7"/>
        <path class="draw" data-draw="{t + 0.15}" stroke="var(--teal)" stroke-width="7" d="M68 160 Q68 104 100 104 Q132 104 132 160"/>
        <circle class="draw" data-draw="{t + 0.25}" cx="52" cy="92" r="16" stroke="var(--teal-line)" stroke-width="6"/>
        <path class="draw" data-draw="{t + 0.35}" stroke="var(--teal-line)" stroke-width="6" d="M26 156 Q26 118 52 118 Q70 118 76 132"/>
        <circle class="draw" data-draw="{t + 0.25}" cx="148" cy="92" r="16" stroke="var(--teal-line)" stroke-width="6"/>
        <path class="draw" data-draw="{t + 0.35}" stroke="var(--teal-line)" stroke-width="6" d="M174 156 Q174 118 148 118 Q130 118 124 132"/>
        <path data-pop="{t + 0.9}" fill="#b5dc55" d="M100 40 C92 30 76 34 80 46 C83 54 100 62 100 62 C100 62 117 54 120 46 C124 34 108 30 100 40 Z"/>''')
HEART = "M100 168 C64 140 30 116 30 80 C30 56 48 40 70 40 C84 40 94 48 100 60 C106 48 116 40 130 40 C152 40 170 56 170 80 C170 116 136 140 100 168 Z"
def ic_heart(t, fill_at, beat_at):
    return SVG.format(f'''
        <circle data-ring="{beat_at}" cx="100" cy="104" r="70" stroke="#b5dc55" stroke-width="4" opacity="0"/>
        <path data-fill="{fill_at}" fill="#b5dc55" fill-opacity="0" d="{HEART}"/>
        <path class="draw" data-draw="{t}" stroke="var(--teal)" stroke-width="8" d="{HEART}"/>
        <g data-pop="{fill_at + 0.3}" stroke="#ffffff" stroke-width="6"><path d="M70 82 Q72 64 90 62"/></g>''')

# recap: the four earlier icons, already drawn, gathered in one row
def recap(top, size, t0):
    items = [ic_fajr(-9), ic_book(-9), ic_car(-9), ic_friends(-9)]
    gap = 28; total = 4 * size + 3 * gap; x0 = (1080 - total) // 2
    out = ""
    for k, svg in enumerate(items):
        left = x0 + (3 - k) * (size + gap)          # RTL order: first blessing on the right
        out += (f'      <div class="mini" style="top:{top}px;left:{left}px;width:{size}px;height:{size}px" '
                f'data-mini="{t0 + k * 0.14}">{svg}</div>\n')
    return out

S = []
# 1 — صلاة الفجر
S.append(scene(1, 0,
  icon(250, 370, ic_fajr(0.05)) +
  c(690, 72, 500, kl("تسعد بمحافظتك على صلاة", "0.05,0.48,1.28,1.36"), 0.0) +
  c(800, 220, 700, kl("الفجر", "1.68", "acc"), 1.5, "big", 1.15) +
  c(1080, 84, 500, kl("في جماعة", "2.06,2.18"), 1.85)))
# 2 — تتلذذ بقراءة القرآن
S.append(scene(2, 2.66,
  icon(250, 380, ic_book(2.62)) +
  c(700, 200, 700, kl("تتلذّذ", "2.66", "acc"), 2.5, "big", 1.15) +
  c(970, 96, 500, kl('بقراءة <span class="acc">القرآن</span>', "3.20,3.70"), 3.0)))
# 3 — السيارة
S.append(scene(3, 4.59,
  icon(250, 370, ic_car(4.55)) +
  c(680, 76, 500, kl("تستغلّ وقتك في السيارة", "4.59,4.92,5.26,5.38"), 4.5) +
  c(800, 96, 700, kl('في سماع ما <span class="acc">ينفع</span>', "5.90,6.06,6.42,6.56"), 5.7) +
  pill(970, 64, "وما يدفع للطاعة", "7.08,7.34,7.74", 6.9)))
# 4 — الصحبة الصالحة
S.append(scene(4, 8.61,
  icon(240, 330, ic_friends(8.55)) +
  c(590, 84, 600, kl('تأنس بصحبٍ <span class="acc">صالح</span>', "8.61,8.92,9.24"), 8.5) +
  c(735, 64, 500, kl("تذكر معهم ما خُلقت لأجله:", "9.68,10.16,10.56,10.70,11.06"), 9.45) +
  card(860, 11.35, '<div class="quote" style="font-size:92px;font-weight:600;line-height:1.5">'
       + kl("﴿وَمَا خَلَقْتُ الْجِنَّ", "11.60,11.98,12.45", "gl")
       + kl('وَالْإِنسَ إِلَّا ' + mark("لِيَعْبُدُونِ﴾", 13.95), "12.82,13.16,13.56", "gl") + '</div>') +
  ref(1220, "[الذاريات: ٥٦]", 13.9)))
# 5 — كل هذه الأمور فضل ورحمة (the four icons gather)
S.append(scene(5, 14.47,
  recap(330, 170, 14.45) +
  c(580, 84, 500, kl("كلُّ هذه الأمور", "14.47,14.52,14.66"), 14.4) +
  c(720, 150, 700, kl('فضلٌ <span class="acc">ورحمةٌ</span>', "15.08,15.89", "acc"), 14.9, "big", 1.25) +
  c(980, 84, 500, kl("من اللهِ سبحانه وتعالى", "16.73,16.85,16.98,17.62"), 16.5)))
# 6 — ولكن الله حبب إليكم الإيمان وزينه في قلوبكم
S.append(scene(6, 18.92,
  icon(240, 330, ic_heart(18.9, 22.06, 22.3)) +
  c(620, 100, 600, kl("﴿وَلَٰكِنَّ اللَّهَ حَبَّبَ", "18.92,19.14,19.38"), 18.85, lh=1.6) +
  c(780, 100, 600, kl('إِلَيْكُمُ <span class="acc">الْإِيمَانَ</span>', "19.82,20.26"), 19.6, lh=1.6) +
  c(940, 100, 600, kl('وَزَيَّنَهُ فِي ' + mark("قُلُوبِكُمْ﴾", 22.3), "21.14,21.70,22.06"), 20.9, lh=1.6) +
  ref(1160, "[الحجرات: ٧]", 22.6)))

HTML = r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>فضلٌ ورحمة — نهاري</title>
<!-- ريل «فضلٌ ورحمة» بالقالب النهاري بدون مربعات، بلا عنوان ولا ترقيم. يُولَّد من tools/build.py -->
<style>
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-400.ttf") format("truetype"); font-weight: 400; }
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-500.ttf") format("truetype"); font-weight: 500; }
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-600.ttf") format("truetype"); font-weight: 600; }
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-700.ttf") format("truetype"); font-weight: 700; }
  /* القالب ٣ — النهاري بدون مربعات */
  :root {
    --bg: #f3f5f4; --ink: #151718; --muted: #7b8386; --teal: #1b7a9c; --teal-line: #4a93b0;
    --green: #b5dc55; --hl: #d2ee94; --card: #ffffff;
    --card-edge: rgba(215, 225, 228, .9); --card-shadow: rgba(30, 60, 70, .08); --handle: #9aa1a4;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; }
  body { background: #1d2124; font-family: "Plex Ar", system-ui, sans-serif; color: var(--ink); overflow: hidden;
         display: flex; flex-direction: column; align-items: center; justify-content: center; }
  #viewport { position: relative; flex: 1; width: 100%; overflow: hidden; }
  #stage { position: absolute; left: 50%; top: 50%; width: 1080px; height: 1920px; transform-origin: 50% 50%; background: var(--bg); overflow: hidden; }
  body.render { background: var(--bg); display: block; }
  body.render #viewport { position: fixed; inset: 0; }
  body.render #stage { left: 0; top: 0; transform: none !important; }
  body.render #controls { display: none; }

  .glow { position: absolute; inset: -160px; pointer-events: none; }
  #glow-a { background: radial-gradient(circle at calc(100% - 160px) 160px, rgba(140, 196, 220, .42) 0px, rgba(140, 196, 220, .18) 270px, rgba(140, 196, 220, 0) 660px); }
  #glow-b { background: radial-gradient(circle at 160px calc(100% - 160px), rgba(205, 232, 150, .45) 0px, rgba(205, 232, 150, .2) 270px, rgba(205, 232, 150, 0) 680px); }

  .scene { position: absolute; inset: 0; --p: 0%;
           -webkit-mask-image: linear-gradient(to bottom, #000 0%, #000 calc(var(--p) - 22%), transparent var(--p));
                   mask-image: linear-gradient(to bottom, #000 0%, #000 calc(var(--p) - 22%), transparent var(--p)); }
  .scene.out { -webkit-mask-image: linear-gradient(to bottom, transparent 0%, transparent calc(var(--p) - 22%), #000 var(--p));
                       mask-image: linear-gradient(to bottom, transparent 0%, transparent calc(var(--p) - 22%), #000 var(--p)); }
  .scene.live { -webkit-mask-image: none; mask-image: none; }
  /* day tide: a band of soft morning light */
  #tide { position: absolute; left: -10%; right: -10%; height: 520px; top: 0; pointer-events: none; opacity: 0;
          background: radial-gradient(ellipse 60% 46% at 50% 50%, rgba(255, 255, 255, .95), rgba(255, 255, 255, .5) 45%, transparent 72%),
                      radial-gradient(ellipse 50% 30% at 50% 50%, rgba(181, 220, 85, .35), transparent 70%),
                      radial-gradient(ellipse 80% 50% at 50% 50%, rgba(140, 196, 220, .25), transparent 70%); filter: blur(14px); }

  .c { position: absolute; left: 0; right: 0; text-align: center; }
  .line { display: block; white-space: nowrap; }
  .k { display: inline-block; }
  .acc { color: var(--teal); }
  .mark { background-image: linear-gradient(var(--hl), var(--hl)); background-repeat: no-repeat; background-position: 100% 86%; background-size: 0% 38%; padding: 0 8px; }
  .glass { position: absolute; left: 80px; right: 80px; border-radius: 42px; background: var(--card); padding: 44px 46px 48px; text-align: center;
           box-shadow: 0 2px 0 rgba(30, 60, 70, .05), 0 14px 0 -4px var(--card-edge), 0 30px 60px var(--card-shadow); }
  .glass .gl { display: block; white-space: nowrap; }
  .pillrow { position: absolute; left: 0; right: 0; text-align: center; }
  .pill { display: inline-block; padding: 14px 48px 22px; border-radius: 999px; font-weight: 600; white-space: nowrap; background: var(--teal); color: #fff; }
  .refchip { position: absolute; left: 0; right: 0; text-align: center; font-size: 40px; color: var(--muted); }
  .icon { position: absolute; left: 50%; }
  .icon svg, .mini svg { width: 100%; height: 100%; overflow: visible; }
  .mini { position: absolute; border-radius: 40px; background: #fff; padding: 18px;
          box-shadow: 0 10px 0 -4px var(--card-edge), 0 24px 50px var(--card-shadow); }
  .dot { position: absolute; width: 34px; height: 34px; margin: -17px 0 0 -17px; }
  .dot i, .dot b { position: absolute; inset: 0; border-radius: 50%; }
  .dot b { background: rgba(181, 220, 85, .35); }
  .dot i { inset: 7px; background: var(--green); }
  #handle { position: absolute; left: 0; right: 0; top: 1660px; text-align: center; direction: ltr; font-size: 36px; color: var(--handle); letter-spacing: .5px; }

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
    <div class="glow" id="glow-a"></div>
    <div class="glow" id="glow-b"></div>
    <div class="dot" id="dot" style="left: 985px; top: 250px;"><b></b><i></i></div>

__SCENES__
    <div id="tide"></div>
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

  const lines = $$('.kline').map(el => {
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
    return { el, ws: $$('.k', el), times: el.dataset.t.split(',').map(Number) };
  });

  const tl = gsap.timeline({ paused: true, defaults: { ease: 'power3.out' } });
  const scenes = $$('.scene'), starts = scenes.map(s => +s.dataset.start);
  scenes.forEach((s, i) => gsap.set(s, { '--p': i === 0 ? '130%' : '0%' }));
  gsap.set(scenes[0], { className: 'scene live' });

  const wordIn = (w, at) => tl.fromTo(w, { y: 56, opacity: 0, filter: 'blur(12px)' }, { y: 0, opacity: 1, filter: 'blur(0px)', duration: 0.6 }, at);
  const bigIn  = (w, at) => tl.fromTo(w, { y: 80, opacity: 0, scale: 0.86, filter: 'blur(26px)' }, { y: 0, opacity: 1, scale: 1, filter: 'blur(0px)', duration: 1.0, ease: 'expo.out' }, at);
  const FX = {
    card: (el, at) => tl.fromTo(el, { y: 150, opacity: 0, rotation: -1.2 }, { y: 0, opacity: 1, rotation: 0, duration: 0.9, ease: 'expo.out' }, at),
    pill: (el, at) => tl.fromTo(el.firstElementChild, { y: 40, opacity: 0, scale: 0.9 }, { y: 0, opacity: 1, scale: 1, duration: 0.7, ease: 'back.out(1.8)' }, at),
    chip: (el, at) => tl.fromTo(el.firstElementChild, { y: 18, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, at),
  };

  /* «مدّ ضوئي» — continuous: the light descends as the next idea's first word is spoken */
  const TIDE = 0.95;
  const tide = (prev, next, a) => {
    const t0 = a - 0.18;
    tl.set(prev, { className: 'scene out', '--p': '0%' }, t0)
      .set(next, { className: 'scene', '--p': '0%' }, t0)
      .to([prev, next], { '--p': '130%', duration: TIDE, ease: 'power2.inOut' }, t0)
      .to($$(':scope > *', prev), { y: 40, filter: 'blur(8px)', duration: TIDE, ease: 'power2.in' }, t0)
      .fromTo('#tide', { y: -520, opacity: 0 }, { y: 1920, duration: TIDE, ease: 'power2.inOut' }, t0)
      .to('#tide', { opacity: 1, duration: TIDE * 0.35, ease: 'sine.out' }, t0)
      .to('#tide', { opacity: 0, duration: TIDE * 0.4, ease: 'sine.in' }, t0 + TIDE * 0.6)
      .set(next, { className: 'scene live' }, t0 + TIDE)
      .set(prev, { autoAlpha: 0 }, t0 + TIDE);
  };

  tl.fromTo('#glow-a', { opacity: 0 }, { opacity: 1, duration: 1.2 }, 0)
    .fromTo('#glow-b', { opacity: 0 }, { opacity: 1, duration: 1.2 }, 0.1)
    .to('#glow-a', { x: -70, y: 60, duration: END, ease: 'sine.inOut' }, 0)
    .to('#glow-b', { x: 70, y: -50, duration: END, ease: 'sine.inOut' }, 0)
    .fromTo('#handle', { opacity: 0 }, { opacity: 1, duration: 0.8 }, 0.5)
    .fromTo('#dot', { scale: 0 }, { scale: 1, duration: 0.6, ease: 'back.out(3)' }, 0.1)
    .fromTo('#dot b', { scale: 1, opacity: 1 }, { scale: 2.4, opacity: 0, duration: 1.4, ease: 'sine.out', repeat: Math.floor(END / 1.4) - 1 }, 0.7);

  scenes.forEach((S, i) => {
    const a = starts[i];
    if (i > 0) tide(scenes[i - 1], S, a);
    $$('[data-in]', S).forEach(el => { if (FX[el.dataset.fx]) FX[el.dataset.fx](el, +el.dataset.in); });
    $$('[data-mark]', S).forEach(m => tl.to(m, { backgroundSize: '100% 38%', duration: 0.5, ease: 'power2.inOut' }, +m.dataset.mark));
    const ic = $('.icon', S);
    if (ic) tl.fromTo(ic, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, a - 0.12);
    if (i === scenes.length - 1) tl.to($$(':scope > *', S), { scale: 1.025, duration: END - a - 0.6, ease: 'sine.inOut', transformOrigin: '50% 40%' }, a + 0.5);
  });

  /* ---- icon motion ---- */
  $$('.icon path.draw, .icon circle.draw').forEach(p => { const L = p.getTotalLength(); gsap.set(p, { strokeDasharray: L, strokeDashoffset: L }); });
  $$('.icon [data-draw]').forEach(p => tl.to(p, { strokeDashoffset: 0, duration: 0.7, ease: 'power2.inOut' }, +p.dataset.draw));
  $$('.icon [data-pop]').forEach(g => tl.fromTo(g, { scale: 0, opacity: 0, transformOrigin: '50% 50%' }, { scale: 1, opacity: 1, duration: 0.55, ease: 'back.out(2.4)' }, +g.dataset.pop));
  $$('.icon [data-rise]').forEach(g => tl.fromTo(g, { y: 46, opacity: 0 }, { y: 0, opacity: 1, duration: 1.1, ease: 'expo.out' }, +g.dataset.rise)
      .to(g, { y: -4, duration: 1.2, ease: 'sine.inOut', yoyo: true, repeat: 1 }, +g.dataset.rise + 1.1));
  $$('.icon [data-wave]').forEach(g => [...g.children].forEach((w, k) =>
      tl.fromTo(w, { opacity: 0, scale: 0.7, transformOrigin: '50% 100%' }, { opacity: 1, scale: 1, duration: 0.35, ease: 'sine.out', yoyo: true, repeat: 5 }, +g.dataset.wave + k * 0.16)));
  $$('.icon [data-fill]').forEach(p => tl.to(p, { attr: { 'fill-opacity': 0.9 }, duration: 0.7, ease: 'power2.out' }, +p.dataset.fill));
  $$('.icon [data-ring]').forEach(r => tl.fromTo(r, { attr: { r: 60 }, opacity: 0.9 }, { attr: { r: 112 }, opacity: 0, duration: 1.1, ease: 'sine.out', repeat: 2 }, +r.dataset.ring));
  $$('.icon').forEach(ic => { const r = ic.querySelector('[data-ring]'); if (r) {
      const t = +r.dataset.ring;
      [0, 1.1, 2.2].forEach(d => tl.to(ic, { keyframes: { scale: [1, 1.08, 1, 1.04, 1] }, duration: 0.7, ease: 'none' }, t + d)); } });

  /* recap: the four blessings gather, then glow together on «فضلٌ ورحمة» */
  $$('.mini').forEach((m, k) => {
    const t = +m.dataset.mini;
    tl.fromTo(m, { y: 120, opacity: 0, scale: 0.6, rotation: (k - 1.5) * 8 }, { y: 0, opacity: 1, scale: 1, rotation: 0, duration: 0.7, ease: 'back.out(1.7)' }, t)
      .to(m, { boxShadow: '0 0 0 6px rgba(181,220,85,.9), 0 24px 60px rgba(181,220,85,.45)', duration: 0.5, ease: 'power2.out' }, 15.05 + k * 0.12)
      .to(m, { y: -10, duration: 0.6, ease: 'sine.inOut', yoyo: true, repeat: 1 }, 15.05 + k * 0.12);
  });

  /* words appear when they are spoken */
  lines.forEach(L => {
    const big = L.el.closest('[data-fx="big"]');
    L.ws.forEach((w, i) => {
      const t = L.times[Math.min(i, L.times.length - 1)] + Math.max(0, i - L.times.length + 1) * 0.12;
      big ? bigIn(w, t - 0.12) : wordIn(w, t - 0.06);
    });
  });

  tl.eventCallback('onUpdate', sync);
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
