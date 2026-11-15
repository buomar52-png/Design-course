# Builds motion-graphics/quran-tadabbur/index.html — القالب الليلي بدون مربعات (template ٤)
# Transition: «مدّ ضوئي» — a feathered light tide rises through the frame: the outgoing scene dissolves
# upward behind a soft glowing band while the next scene is revealed beneath it. One continuous background.
# Declarative spec: data-t = spoken time of each word (audio/voice-clean.m4a), data-in = when a card/pill/ref
# appears, data-fx = big|up|card|pill|chip, data-mark = when a highlight draws.
ROOT = "/home/user/Design-course"
OUT = f"{ROOT}/motion-graphics/quran-tadabbur/index.html"

def kl(text, t, cls=""):
    return f'<span class="line kline {cls}" data-t="{t}">{text}</span>'
def c(top, fs, w, inner, at, fx="up", lh=None, extra_style=""):
    lhs = f"line-height:{lh};" if lh else ""
    return f'      <div class="c" style="top:{top}px;font-size:{fs}px;font-weight:{w};{lhs}{extra_style}" data-in="{at}" data-fx="{fx}">{inner}</div>\n'
def pill(top, fs, text, t, at, kind="dash", kcls=""):
    return f'      <div class="pillrow" style="top:{top}px;font-size:{fs}px" data-in="{at}" data-fx="pill"><span class="pill {kind}"><span class="kline {kcls}" data-t="{t}">{text}</span></span></div>\n'
def ref(top, text, at):
    return f'      <div class="refchip" style="top:{top}px" data-in="{at}" data-fx="chip"><span>{text}</span></div>\n'
def scene(i, theme, start, body, num=None):          # theme / num kept for spec compatibility (single night look)
    return f'    <!-- ===== S{i} ({start}s) ===== -->\n    <section class="scene" id="s{i}" data-start="{start}">\n{body}    </section>\n\n'

S = []
# 1 day — كتاب الله مختلف
S.append(scene(1, "day", 0,
  c(430, 96, 700, kl("كتابُ اللهِ عزَّ وجلّ", "0,0.36,0.54,0.76"), 0.05) +
  c(600, 250, 700, kl("مختلف", "1.08", "acc"), 0.85, "big", 1.15) +
  c(920, 76, 500, kl("عن جميعِ الكتب", "1.54,1.72,2.06"), 1.3) +
  c(1050, 64, 500, kl("مهما حوت من مواعظَ وحِكَم،", "2.56,2.94,3.28,3.52,4.14"), 2.3) +
  c(1150, 64, 500, kl('إلا أنّ كتابَ الله عزّ وجلّ <span class="acc">مختلف</span>', "4.70,5.00,5.16,5.60,5.76,6.02,6.36"), 4.45)))
# 2 night — ومن يتق الله يجعل له مخرجا
S.append(scene(2, "night", 6.9,
  c(470, 80, 500, kl("أنت تقرأ على سبيل المثال:", "6.98,7.22,7.64,7.80,8.36"), 6.95) +
  f'      <div class="glass" style="top:640px" data-in="8.5" data-fx="card"><div class="quote" style="font-size:104px;font-weight:600;line-height:1.5">'
  + kl("﴿وَمَن يَتَّقِ اللَّهَ", "8.82,9.08,9.44", "gl") + kl('يَجْعَل لَّهُ <span class="mark" data-mark="10.6">مَخْرَجًا﴾</span>', "9.66,10.20,10.40", "gl")
  + '</div></div>\n' + ref(1020, "[الطلاق: ٢]", 10.6)))
# 3 day — حزين → فتستبشر
S.append(scene(3, "day", 10.95,
  c(470, 84, 500, kl("تقرؤها وأنت حزين", "11.06,11.60,11.98"), 11.0) +
  c(620, 220, 700, kl("فتستبشر", "12.46", "acc"), 12.25, "big", 1.15) +
  c(930, 76, 500, kl('بأنّ اللهَ سيجعلُ لك <span class="acc">مخرجًا</span>', "13.22,13.54,13.84,15.70,15.94"), 13.0), num="١"))
# 4 night — ضائقة مالية → فتتيقن
S.append(scene(4, "night", 17.85,
  c(430, 72, 500, kl("تقرؤها وأنت تشعر بضائقةٍ ماليّة", "17.98,18.60,19.10,19.82,20.50"), 17.95) +
  c(590, 220, 700, kl("فتتيقّن", "20.98", "acc"), 20.75, "big", 1.15) +
  c(880, 72, 500, kl("بأنّ مَن ترك شيئًا لله", "21.82,22.12,23.46,23.86,24.30"), 21.6) +
  c(990, 72, 600, kl("عوّضه اللهُ خيرًا منه", "24.70,25.22,25.44,26.02"), 24.45) +
  pill(1140, 60, "فسيجعلُ لك مخرجًا", "26.32,26.84,27.06", 26.1, "solid", "onlime"), num="٢"))
# 5 day — التباس → ومن يتق الله
S.append(scene(5, "day", 27.45,
  c(430, 72, 500, kl("تقرؤها وأنت تشعر بالتباسٍ", "27.60,28.28,28.60,29.18"), 27.5) +
  c(540, 96, 700, kl('بين <span class="acc">الحقّ</span> والباطل', "29.84,30.06,30.58"), 29.6) +
  c(700, 64, 500, kl("وبسهولةِ وقوعِ الشبهةِ على قلبك", "31.46,33.00,33.36,33.84,34.04"), 31.25) +
  f'      <div class="glass" style="top:860px" data-in="34.5" data-fx="card"><div class="quote" style="font-size:92px;font-weight:600;line-height:1.5">'
  + kl("﴿وَمَن يَتَّقِ اللَّهَ", "34.78,36.20,36.54", "gl") + kl('يَجْعَل لَّهُ <span class="mark" data-mark="37.6">مَخْرَجًا﴾</span>', "36.68,37.16,37.36", "gl")
  + '</div></div>\n', num="٣"))
# 6 night — فتتيقن ... الحق واضحا جليا ... ويسر لك
S.append(scene(6, "night", 38.0,
  c(430, 220, 700, kl("فتتيقّن", "38.12", "acc"), 38.0, "big", 1.15) +
  c(720, 72, 500, kl("بأنّ اللهَ عزّ وجلّ سيبيّنُ لك", "39.58,40.18,40.44,40.68,41.08,42.14"), 39.35) +
  c(830, 104, 700, kl("الحقَّ واضحًا جليًّا", "42.38,42.90,43.70", "acc"), 42.15) +
  pill(1040, 50, "ويُيسّرُ لك الانقيادَ له والعملَ به", "44.46,45.52,45.80,46.36,46.62,47.72", 44.2, "solid", "onlime")))
# 7 day — يا أيها الذين آمنوا إن تتقوا الله
S.append(scene(7, "day", 48.0,
  c(520, 104, 600, kl("﴿يَا أَيُّهَا الَّذِينَ آمَنُوا", "48.12,48.82,49.08,49.38"), 48.05, lh=1.55) +
  c(690, 104, 600, kl("إِن تَتَّقُوا اللَّهَ", "49.92,50.52,51.10"), 49.7, lh=1.55) +
  c(860, 104, 600, kl('يَجْعَل لَّكُمْ <span class="mark" data-mark="52.95">فُرْقَانًا﴾</span>', "51.36,52.22,52.74"), 51.15, lh=1.55) +
  ref(1090, "[الأنفال: ٢٩]", 50.3)))
# 8 night — كلما رددت آياته ازدادت جمالا رونقا
S.append(scene(8, "night", 53.4,
  c(430, 84, 500, kl("كتابُ اللهِ عزّ وجلّ", "53.52,54.30,54.44,54.66"), 53.45) +
  c(540, 84, 500, kl("كلما رددتَ آياتِه", "55.04,55.66,56.12"), 54.85) +
  c(700, 72, 500, kl("ازدادت", "56.78"), 56.6) +
  c(790, 200, 700, kl("جمالًا", "57.60", "acc"), 57.35, "big", 1.15) +
  c(1050, 72, 500, kl("ازدادت", "58.32"), 58.15) +
  c(1140, 200, 700, kl("رونقًا", "58.98", "acc"), 58.75, "big", 1.15)))
# 9 day — الشاطبي
S.append(scene(9, "day", 59.35,
  c(450, 64, 600, kl('كما يقول <span class="acc">الإمام الشاطبي:</span>', "59.48,59.90,60.20,60.52"), 59.4) +
  f'      <div class="glass" style="top:600px;padding:40px 30px 44px" data-in="60.75" data-fx="card"><div class="quote poem">'
  + kl("وَإِنَّ كِتَابَ اللهِ أَوْثَقُ شَافِعٍ", "61.10,61.54,62.00,62.26,62.92", "gl")
  + kl("وَأَغْنَى غَنَاءٍ وَاهِبًا مُتَفَضِّلَا", "63.40,64.12,64.52,65.20", "gl")
  + kl('وَخَيْرُ جَلِيسٍ لَا يُمَلُّ <span class="mark" data-mark="68.0">حَدِيثُهُ</span>', "66.00,66.58,66.96,67.06,67.36", "gl")
  + kl("وَتَرْدَادُهُ يَزْدَادُ فِيهِ تَجَمُّلَا", "68.10,69.22,70.30,70.74", "gl")
  + '</div></div>\n'))
# 10 night — قلب طاهر نقي
S.append(scene(10, "night", 71.35,
  c(440, 76, 500, kl("قراءةُ القرآنِ والإقبالُ عليه", "71.48,71.90,72.32,72.84"), 71.4) +
  c(560, 76, 500, kl("لا يحتاج إلى كثيرِ علم", "73.06,73.26,73.76,73.96,74.74"), 72.85) +
  c(720, 76, 500, kl("ولكن يحتاج إلى", "75.22,75.56,76.02"), 75.0) +
  c(820, 260, 700, kl("قلب", "76.16", "acc"), 75.95, "big", 1.15) +
  c(1210, 88, 600, kl("طاهرٍ نقيّ", "76.60,77.00"), 76.4)))
# 11 day — جزء من آية / آية / آية أو سورة
S.append(scene(11, "day", 77.55,
  pill(460, 52, "جزءٌ من آيةٍ كفيلٌ بأن يغيّر حياتك", "77.40,77.86,78.04,78.56,79.06,79.52,80.74", 77.6, "dash") +
  pill(620, 58, "آيةٌ كفيلةٌ بأن تغيّر حياتك", "81.40,82.00,82.46,82.90,83.54", 81.2, "solid", "lime") +
  c(820, 124, 700, kl("آيةٌ أو سورةٌ", "84.20,84.58,84.84", "acc"), 84.0) +
  c(1010, 84, 500, kl('تجعلك تعيش <span class="acc">معناها</span>', "85.32,85.82,86.76"), 85.1)))
# 12 night — الآية الختامية
S.append(scene(12, "night", 87.5,
  c(450, 100, 600, kl("﴿إِنَّ فِي ذَٰلِكَ لَذِكْرَىٰ", "88.02,88.36,89.34,90.08"), 87.85, lh=1.6) +
  c(610, 100, 600, kl('لِمَن كَانَ لَهُ <span class="mark" data-mark="91.95">قَلْبٌ</span>', "90.76,90.98,91.26,91.68"), 90.5, lh=1.6) +
  c(770, 100, 600, kl("أَوْ أَلْقَى السَّمْعَ", "92.28,92.98,93.40"), 92.05, lh=1.6) +
  c(930, 100, 600, kl("وَهُوَ شَهِيدٌ﴾", "93.94,94.56"), 93.7, lh=1.6) +
  ref(1160, "[ق: ٣٧]", 95.0)))

END = 97.6


HTML = r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>كتاب الله مختلف — ليلي</title>
<!-- ريل «كتاب الله مختلف» بالقالب الليلي بدون مربعات. الانتقال: «مدّ ضوئي». يُولَّد من tools/build.py -->
<style>
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-400.ttf") format("truetype"); font-weight: 400; }
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-500.ttf") format("truetype"); font-weight: 500; }
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-600.ttf") format("truetype"); font-weight: 600; }
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-700.ttf") format("truetype"); font-weight: 700; }
  /* القالب ٤ — الليلي بدون مربعات */
  :root {
    --bg: #0e1416; --ink: #eef3f4; --muted: #8a979c; --teal: #4cb3d6; --teal-line: #5aaccb;
    --green: #b5dc55; --hl: rgba(181, 220, 85, .38); --card: #172024;
    --card-edge: rgba(0, 0, 0, .45); --card-shadow: rgba(0, 0, 0, .35); --handle: #66737a;
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

  /* one continuous background for the whole reel */
  .glow { position: absolute; inset: -160px; pointer-events: none; }
  #glow-a { background: radial-gradient(circle at calc(100% - 160px) 160px, rgba(40, 130, 170, .40) 0px, rgba(40, 130, 170, .17) 270px, rgba(40, 130, 170, 0) 660px); }
  #glow-b { background: radial-gradient(circle at 160px calc(100% - 160px), rgba(120, 170, 50, .26) 0px, rgba(120, 170, 50, .11) 270px, rgba(120, 170, 50, 0) 680px); }

  /* scenes are transparent layers; the transition masks them with a feathered edge driven by --p */
  .scene { position: absolute; inset: 0; --p: 0%;
           -webkit-mask-image: linear-gradient(to top, #000 0%, #000 calc(var(--p) - 22%), transparent var(--p));
                   mask-image: linear-gradient(to top, #000 0%, #000 calc(var(--p) - 22%), transparent var(--p)); }
  .scene.out { -webkit-mask-image: linear-gradient(to top, transparent 0%, transparent calc(var(--p) - 22%), #000 var(--p));
                       mask-image: linear-gradient(to top, transparent 0%, transparent calc(var(--p) - 22%), #000 var(--p)); }
  .scene.live { -webkit-mask-image: none; mask-image: none; }
  #tide { position: absolute; left: -10%; right: -10%; height: 520px; top: 0; pointer-events: none; opacity: 0; mix-blend-mode: screen;
          background: radial-gradient(ellipse 60% 50% at 50% 50%, rgba(76, 179, 214, .55), rgba(76, 179, 214, .16) 45%, transparent 72%),
                      radial-gradient(ellipse 34% 22% at 50% 50%, rgba(181, 220, 85, .45), transparent 70%); filter: blur(18px); }

  .c { position: absolute; left: 0; right: 0; text-align: center; }
  .line { display: block; white-space: nowrap; }
  .k { display: inline-block; }
  .acc { color: var(--teal); }
  .c[data-fx="big"] .k { color: var(--teal); }
  .mark { background-image: linear-gradient(var(--hl), var(--hl)); background-repeat: no-repeat; background-position: 100% 86%; background-size: 0% 38%; padding: 0 8px; }

  .glass { position: absolute; left: 80px; right: 80px; border-radius: 42px; background: var(--card); padding: 44px 46px 48px; text-align: center;
           box-shadow: 0 2px 0 rgba(0, 0, 0, .2), 0 14px 0 -4px var(--card-edge), 0 30px 60px var(--card-shadow); }
  .glass .gl { display: block; white-space: nowrap; }
  .poem { font-size: 60px; font-weight: 600; line-height: 1.95; }
  .pillrow { position: absolute; left: 0; right: 0; text-align: center; }
  .pill { display: inline-block; padding: 14px 44px 22px; border-radius: 999px; font-weight: 600; white-space: nowrap; }
  .pill.dash { border: 3px dashed rgba(238, 243, 244, .2); color: var(--muted); }
  .pill.solid { background: var(--teal); color: #0b1214; }
  .refchip { position: absolute; left: 0; right: 0; text-align: center; font-size: 40px; color: var(--muted); }

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

  /* split every .kline into word spans; data-t = spoken time of each word */
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

  /* ---- house motion (template ٤) ---- */
  const wordIn = (w, at, dur = 0.7) => tl.fromTo(w, { y: 60, opacity: 0, filter: 'blur(12px)' }, { y: 0, opacity: 1, filter: 'blur(0px)', duration: dur }, at);
  const bigIn  = (w, at) => tl.fromTo(w, { y: 80, opacity: 0, scale: 0.86, filter: 'blur(26px)' }, { y: 0, opacity: 1, scale: 1, filter: 'blur(0px)', duration: 1.0, ease: 'expo.out' }, at);
  const FX = {
    card: (el, at) => tl.fromTo(el, { y: 150, opacity: 0, rotation: -1.2 }, { y: 0, opacity: 1, rotation: 0, duration: 0.95, ease: 'expo.out' }, at),
    pill: (el, at) => tl.fromTo(el.firstElementChild, { y: 40, opacity: 0, scale: 0.92 }, { y: 0, opacity: 1, scale: 1, duration: 0.7, ease: 'back.out(1.8)' }, at),
    chip: (el, at) => tl.fromTo(el.firstElementChild, { y: 18, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, at),
  };

  /* ---- «مدّ ضوئي»: the light tide ---- */
  const TIDE = 1.15;
  const tide = (prev, next, a) => {
    const t0 = a - 0.62;
    tl.set(prev, { className: 'scene out', '--p': '0%' }, t0)
      .set(next, { className: 'scene', '--p': '0%' }, t0)
      .to([prev, next], { '--p': '130%', duration: TIDE, ease: 'power2.inOut' }, t0)
      .to($$(':scope > *', prev), { y: -46, filter: 'blur(8px)', duration: TIDE, ease: 'power2.in' }, t0)
      .fromTo('#tide', { y: 1920, opacity: 0 }, { y: -520, duration: TIDE, ease: 'power2.inOut' }, t0)
      .to('#tide', { opacity: 1, duration: TIDE * 0.35, ease: 'sine.out' }, t0)
      .to('#tide', { opacity: 0, duration: TIDE * 0.4, ease: 'sine.in' }, t0 + TIDE * 0.6)
      .set(next, { className: 'scene live' }, t0 + TIDE)
      .set(prev, { autoAlpha: 0 }, t0 + TIDE);
  };

  /* background: one slow continuous drift + a breath of light on every transition */
  tl.fromTo('#glow-a', { opacity: 0 }, { opacity: 1, duration: 1.4 }, 0)
    .fromTo('#glow-b', { opacity: 0 }, { opacity: 1, duration: 1.4 }, 0.2)
    .to('#glow-a', { x: -70, y: 60, duration: END, ease: 'sine.inOut' }, 0)
    .to('#glow-b', { x: 70, y: -50, duration: END, ease: 'sine.inOut' }, 0)
    .fromTo('#handle', { opacity: 0 }, { opacity: 1, duration: 0.8 }, 0.6)
    .fromTo('#dot', { scale: 0 }, { scale: 1, duration: 0.6, ease: 'back.out(3)' }, 0.2)
    .fromTo('#dot b', { scale: 1, opacity: 1 }, { scale: 2.4, opacity: 0, duration: 1.4, ease: 'sine.out', repeat: Math.floor(END / 1.4) - 1 }, 0.8);

  scenes.forEach((S, i) => {
    const a = starts[i];
    if (i > 0) {
      tide(scenes[i - 1], S, a);
      tl.to('#glow-a', { opacity: 0.6, duration: 0.5, ease: 'sine.inOut', yoyo: true, repeat: 1 }, a - 0.6);
    }
    $$('[data-in]', S).forEach(el => { if (FX[el.dataset.fx]) FX[el.dataset.fx](el, +el.dataset.in); });
    $$('[data-mark]', S).forEach(m => tl.to(m, { backgroundSize: '100% 38%', duration: 0.55, ease: 'power2.inOut' }, +m.dataset.mark));
    const dash = $('.pill.dash', S), solid = $('.pill.solid', S);
    if (dash && solid) tl.to(dash, { opacity: 0.4, scale: 0.95, duration: 0.6 }, +solid.parentElement.dataset.in + 0.1);
    if (i === scenes.length - 1) tl.to(S, { scale: 1.03, duration: END - a - 0.8, ease: 'sine.inOut', transformOrigin: '50% 40%' }, a + 0.6);
  });

  /* words appear exactly when they are spoken (big words with the heavy blur-in) */
  lines.forEach(L => {
    const big = L.el.closest('[data-fx="big"]');
    L.ws.forEach((w, i) => {
      const t = L.times[Math.min(i, L.times.length - 1)] + Math.max(0, i - L.times.length + 1) * 0.12;
      big ? bigIn(w, t - 0.22) : wordIn(w, t - 0.14, 0.65);
    });
  });

  tl.eventCallback('onUpdate', sync);
  tl.to({}, { duration: 0.001 }, END - 0.001);

  /* -------- player / render API -------- */
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
open(OUT, "w", encoding="utf-8").write(out)
print("written", len(out))
