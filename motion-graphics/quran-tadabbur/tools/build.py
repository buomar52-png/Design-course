# Builds motion-graphics/quran-tadabbur/index.html from the dual template's CSS + a declarative scene spec.
import re, sys
ROOT = "/home/user/Design-course"
tpl = open(f"{ROOT}/.claude/skills/carousel-to-reel/template-dual/index.html", encoding="utf-8").read()
head = tpl[:tpl.index("</style>")]
head = re.sub(r"<title>.*?</title>", "<title>كتاب الله مختلف — ليل ونهار</title>", head)
# drop the template's own scene-specific rules (#s1…#s4): this reel positions everything inline
head = re.sub(r"\n  #s\d[^{]*\{[^}]*\}[^\n]*", "", head)
head = re.sub(r"\n  /\* ===== S\d[^\n]*\*/", "", head)
head = re.sub(r"<!-- القالب الخامس.*?-->", "<!-- ريل «كتاب الله مختلف» — القالب المزدوج (يبدأ نهاري). بناء تصريحي: data-in = وقت الظهور، data-fx = نوع الحركة،\n     data-t = لحظة نطق كل كلمة على audio/voice-clean.m4a. أُنشئ من tools/build.py -->", head, flags=re.S)
extra = """
  /* ===== quran-tadabbur additions ===== */
  .pillrow { position: absolute; left: 0; right: 0; text-align: center; }
  .pill { display: inline-block; padding: 14px 44px 22px; border-radius: 999px; font-weight: 600; white-space: nowrap; }
  .pill.dash { border: 3px dashed var(--chip-line); }
  .day .pill.solid { background: var(--ink); }
  .day .pill.solid .k { color: rgba(243, 239, 230, .25); }
  .night .pill.solid { background: #c6f36b; }
  .night .pill.solid .k { color: rgba(10, 14, 19, .28); }
  .glass .gl { display: block; white-space: nowrap; }
  .refchip { position: absolute; left: 0; right: 0; text-align: center; }
  .poem { font-size: 60px; font-weight: 600; line-height: 1.95; }
"""
H = '      <div class="handle">@abdulla_7amdan</div>\n'

def kl(text, t, cls=""):
    return f'<span class="line kline {cls}" data-t="{t}">{text}</span>'
def c(top, fs, w, inner, at, fx="up", lh=None, extra_style=""):
    lhs = f"line-height:{lh};" if lh else ""
    return f'      <div class="c" style="top:{top}px;font-size:{fs}px;font-weight:{w};{lhs}{extra_style}" data-in="{at}" data-fx="{fx}">{inner}</div>\n'
def pill(top, fs, text, t, at, kind="dash", kcls=""):
    return f'      <div class="pillrow" style="top:{top}px;font-size:{fs}px" data-in="{at}" data-fx="pill"><span class="pill {kind}"><span class="kline {kcls}" data-t="{t}">{text}</span></span></div>\n'
def ref(top, text, at):
    return f'      <div class="refchip" style="top:{top}px" data-in="{at}" data-fx="chip"><span class="chip line">{text}</span></div>\n'
def scene(i, theme, start, body, num=None):
    n = f'      <div class="num">{num}</div>\n' if num else ""
    return f'    <!-- ===== S{i} — {"نهار" if theme == "day" else "ليل"} ({start}s) ===== -->\n    <section class="scene {theme}" id="s{i}" data-start="{start}">\n      <div class="blob a"></div><div class="blob b"></div>\n{n}{body}{H}    </section>\n\n'

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
body = '<body>\n<div id="viewport">\n  <div id="stage">\n\n' + "".join(S) + '''    <div id="grain"></div>
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
  const END = ''' + str(END) + ''';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const css = (el, name) => getComputedStyle(el).getPropertyValue(name).trim();

  /* words: every .kline is split into .k spans; data-t = spoken time of each word */
  const lines = $$('.kline').map(el => {
    const walk = node => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\\s+)/).forEach(p => {
          if (!p) return;
          if (/^\\s+$/.test(p)) return frag.appendChild(document.createTextNode(p));
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
  const KX = 540, KY = 272;
  scenes.slice(1).forEach(s => gsap.set(s, { clipPath: `circle(0px at ${KX}px ${KY}px)` }));

  const FX = {
    up:   (el, at) => tl.fromTo($$('.k', el).length ? $$('.k', el) : el, { y: 50, opacity: 0, filter: 'blur(10px)' }, { y: 0, opacity: 1, filter: 'blur(0px)', duration: 0.6, stagger: 0.07 }, at),
    big:  (el, at) => tl.fromTo($$('.k', el), { scale: 1.6, opacity: 0, filter: 'blur(30px)' }, { scale: 1, opacity: 1, filter: 'blur(0px)', duration: 0.9, ease: 'expo.out' }, at),
    card: (el, at) => { tl.fromTo(el, { y: 140, opacity: 0, scale: 0.94 }, { y: 0, opacity: 1, scale: 1, duration: 0.9, ease: 'expo.out' }, at);
                        tl.fromTo($$('.k', el), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, stagger: 0.04 }, at + 0.25); },
    pill: (el, at) => tl.fromTo(el.firstElementChild, { y: 40, opacity: 0, scale: 0.92 }, { y: 0, opacity: 1, scale: 1, duration: 0.7, ease: 'back.out(1.8)' }, at),
    chip: (el, at) => tl.fromTo(el.firstElementChild, { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 0.75, duration: 0.5, ease: 'back.out(2)' }, at),
  };

  scenes.forEach((S, i) => {
    const a = starts[i], b = starts[i + 1] ?? END;
    tl.fromTo($('.blob.a', S), { x: 0, y: 0 }, { x: -60, y: 50, duration: b - a + 0.4, ease: 'sine.inOut' }, Math.max(0, a - 0.4))
      .fromTo($('.blob.b', S), { x: 0, y: 0 }, { x: 70, y: -40, duration: b - a + 0.4, ease: 'sine.inOut' }, Math.max(0, a - 0.4));
    if (i > 0) {   // iris from the top centre + previous scene recedes
      tl.to(S, { clipPath: `circle(2300px at ${KX}px ${KY}px)`, duration: 0.85, ease: 'power3.inOut' }, a - 0.4)
        .to($$(':scope > *:not(.blob)', scenes[i - 1]), { scale: 0.94, opacity: 0.4, duration: 0.6, ease: 'power2.in' }, a - 0.4);
    } else tl.fromTo($('.handle', S), { opacity: 0 }, { opacity: 1, duration: 0.6 }, 0.6);
    const num = $('.num', S);
    if (num) tl.fromTo(num, { x: -200, opacity: 0 }, { x: 0, opacity: 1, duration: 1.2, ease: 'expo.out' }, a + 0.1);
    $$('[data-in]', S).forEach(el => FX[el.dataset.fx](el, +el.dataset.in));
    $$('[data-mark]', S).forEach(m => tl.to(m, { backgroundSize: '100% 38%', duration: 0.5, ease: 'power2.inOut' }, +m.dataset.mark));
    // a dashed pill dims when the next (solid) pill arrives
    const dash = $('.pill.dash', S), solid = $('.pill.solid', S);
    if (dash && solid) tl.to(dash, { opacity: 0.35, scale: 0.94, duration: 0.6 }, +solid.parentElement.dataset.in + 0.1);
  });

  /* karaoke: each word lights up when it is spoken */
  lines.forEach(L => {
    const S = L.el.closest('.scene');
    L.ws.forEach((w, i) => {
      const t = L.times[Math.min(i, L.times.length - 1)] + Math.max(0, i - L.times.length + 1) * 0.12;
      const color = L.el.classList.contains('onlime') ? '#0a0e13' : L.el.classList.contains('lime') ? '#c6f36b'
                  : (w.closest('.acc') || L.el.classList.contains('acc')) ? css(S, '--accent') : css(S, '--ink');
      tl.to(w, { color, duration: 0.18, ease: 'none' }, t - 0.05)
        .fromTo(w, { scale: 1 }, { scale: 1.08, duration: 0.12, ease: 'power2.out', yoyo: true, repeat: 1 }, t - 0.05);
    });
  });
'''
rest = tpl[tpl.index("  /* film grain: jitters"):]
rest = rest.replace("T.end", "END").replace("window.__scenes = T;", "window.__scenes = Object.fromEntries(starts.map((s, i) => ['s' + (i + 1), s]).concat([['end', END]]));")
out = head + extra + "</style>\n</head>\n" + body + rest
open(f"{ROOT}/motion-graphics/quran-tadabbur/index.html", "w", encoding="utf-8").write(out)
print("written", len(out))
