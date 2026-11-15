# Builds motion-graphics/quran-tadabbur/index.html — القالب الليلي بدون مربعات (template ٤) — v3: icons, holds, no «جزء من آية» scene
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

import json as _json
# Spec times are written on the previous cleaned timeline; SHIFT adds the breathing pauses inserted since then.
def SHIFT(t):
    t = float(t)
    return round(t + 0.3 * (t >= 7.0) + 0.4 * (t >= 49.6) + 0.4 * (t >= 55.5) + 0.9 * (t >= 61.4), 2)
def T(s):   # "1.2,3.4" -> shifted string
    return ",".join(str(SHIFT(x)) for x in str(s).split(","))
_kl, _c, _pill, _ref, _scene = kl, c, pill, ref, scene
def kl(text, t, cls=""): return _kl(text, T(t), cls)
def c(top, fs, w, inner, at, fx="up", lh=None, extra_style=""): return _c(top, fs, w, inner, SHIFT(at), fx, lh, extra_style)
def pill(top, fs, text, t, at, kind="dash", kcls=""): return _pill(top, fs, text, T(t), SHIFT(at), kind, kcls)
def ref(top, text, at): return _ref(top, text, SHIFT(at))
def scene(i, theme, start, body, num=None): return _scene(i, theme, SHIFT(start), body, num)
def mark(text, at, cls=""): return f'<span class="mark {cls}" data-mark="{SHIFT(at)}">{text}</span>'
def card(top, at, inner, style=""):
    return f'      <div class="glass" style="top:{top}px;{style}" data-in="{SHIFT(at)}" data-fx="card">{inner}</div>\n'
def icon(top, size, svg):
    return f'      <div class="icon" style="top:{top}px;width:{size}px;height:{size}px;margin-left:-{size // 2}px">{svg}</div>\n'
A = lambda t: SHIFT(t)   # times inside icon markup

# ---------------------------------------------------------------- icons (stroke drawings, animated by the engine)
ICON_SAD = lambda: f'''<svg viewBox="0 0 200 200" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <g class="sun" data-pop="{A(13.9)}">
          <circle cx="138" cy="70" r="24" fill="#b5dc55" stroke="none"/>
          <g stroke="#b5dc55" stroke-width="6"><path d="M138 30v-12M138 122v-12M98 70H86M190 70h-12M110 42l-8-8M174 106l-8-8M110 98l-8 8M174 34l-8 8"/></g>
        </g>
        <path class="draw cloud" data-draw="{A(12.75)}" stroke="var(--teal)" stroke-width="7" fill="var(--bg)"
              d="M55 128 H150 C168 128 178 113 172 98 C167 85 152 81 142 87 C138 67 120 55 100 57 C80 59 66 75 66 93 C52 91 40 101 41 113 C42 123 48 128 55 128 Z"/>
        <g class="rain" data-rain="{A(13.3)}" data-hide="{A(13.95)}" stroke="var(--teal-line)" stroke-width="6">
          <path d="M72 145v14"/><path d="M98 150v14"/><path d="M124 145v14"/><path d="M150 150v14"/>
        </g>
      </svg>'''
ICON_WALLET = lambda: f'''<svg viewBox="0 0 200 200" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <g class="coins">
          <g data-pop="{A(24.45)}"><circle cx="70" cy="44" r="17" fill="#b5dc55"/><path d="M70 36v16" stroke="#0e1416" stroke-width="4"/></g>
          <g data-pop="{A(24.65)}"><circle cx="104" cy="28" r="19" fill="#b5dc55"/><path d="M104 19v18" stroke="#0e1416" stroke-width="4"/></g>
          <g data-pop="{A(24.85)}"><circle cx="140" cy="44" r="16" fill="#b5dc55"/><path d="M140 37v14" stroke="#0e1416" stroke-width="4"/></g>
        </g>
        <g class="wallet" data-shake="{A(20.75)}">
          <path class="draw" data-draw="{A(19.1)}" stroke="var(--teal)" stroke-width="7" fill="var(--bg)"
                d="M36 78 H156 Q170 78 170 92 V156 Q170 170 156 170 H44 Q30 170 30 156 V84 Q30 78 36 78 Z"/>
          <path class="draw" data-draw="{A(19.3)}" stroke="var(--teal)" stroke-width="7" d="M34 80 Q34 64 52 62 L136 52 Q150 51 150 64 V78"/>
          <path class="draw" data-draw="{A(19.5)}" stroke="var(--teal)" stroke-width="7" fill="var(--bg)" d="M170 106 H142 Q132 106 132 116 V122 Q132 132 142 132 H170 Z"/>
          <circle cx="148" cy="119" r="5" fill="var(--teal)" data-pop="{A(19.7)}"/>
        </g>
      </svg>'''
ICON_FORK = lambda: f'''<svg viewBox="0 0 200 200" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path class="draw" data-draw="{A(28.4)}" stroke="var(--teal)" stroke-width="8" d="M100 188 V118"/>
        <g class="path-a" data-fade="{A(37.8)}">
          <path class="draw" data-draw="{A(28.75)}" stroke="var(--teal)" stroke-width="8" d="M100 118 C100 86 72 70 46 50"/>
          <path class="draw" data-draw="{A(29.15)}" stroke="var(--teal)" stroke-width="8" d="M44 74 L42 46 L70 44"/>
        </g>
        <g class="path-b" data-glow="{A(37.8)}">
          <path class="draw" data-draw="{A(28.75)}" stroke="var(--teal)" stroke-width="8" d="M100 118 C100 86 128 70 154 50"/>
          <path class="draw" data-draw="{A(29.15)}" stroke="var(--teal)" stroke-width="8" d="M156 74 L158 46 L130 44"/>
        </g>
        <text x="100" y="78" text-anchor="middle" font-size="58" font-weight="700" fill="#b5dc55" stroke="none"
              data-pop="{A(29.6)}" data-fade="{A(37.8)}" font-family="Plex Ar">؟</text>
      </svg>'''

S = []
# 1 — كتاب الله مختلف
S.append(scene(1, "night", 0,
  c(430, 96, 700, kl("كتابُ اللهِ عزَّ وجلّ", "0,0.36,0.54,0.76"), 0.05) +
  c(600, 250, 700, kl("مختلف", "1.08", "acc"), 0.85, "big", 1.15) +
  c(920, 76, 500, kl("عن جميعِ الكتب", "1.54,1.72,2.06"), 1.3) +
  c(1050, 64, 500, kl("مهما حوت من مواعظَ وحِكَم،", "2.56,2.96,3.30,3.52,4.14"), 2.3) +
  c(1150, 64, 500, kl('إلا أنّ كتابَ الله عزّ وجلّ <span class="acc">مختلف</span>', "4.70,5.00,5.16,5.60,5.76,6.00,6.36"), 4.45)))
# 2 — ومن يتق الله يجعل له مخرجا  (now holds on «مخرجًا» before the transition)
S.append(scene(2, "night", 7.67,
  c(470, 80, 500, kl("أنت تقرأ على سبيل المثال:", "7.70,7.95,8.24,8.40,8.90"), 7.7) +
  card(640, 9.2, '<div class="quote" style="font-size:104px;font-weight:600;line-height:1.5">'
       + kl("﴿وَمَن يَتَّقِ اللَّهَ", "9.44,9.68,10.04", "gl")
       + kl('يَجْعَل لَّهُ ' + mark("مَخْرَجًا﴾", 11.25), "10.26,10.82,11.00", "gl") + '</div>') +
  ref(1020, "[الطلاق: ٢]", 11.35)))
# 3 — حزين → فتستبشر  (icon: rain cloud → sun)
S.append(scene(3, "night", 12.70,
  icon(250, 290, ICON_SAD()) +
  c(590, 84, 500, kl("تقرؤها وأنت حزين", "12.73,13.10,13.48"), 12.7) +
  c(710, 220, 700, kl("فتستبشر", "13.96", "acc"), 13.75, "big", 1.15) +
  c(1010, 76, 500, kl('بأنّ اللهَ سيجعلُ لك <span class="acc">مخرجًا</span>', "14.64,15.02,15.32,15.88,16.12"), 14.4)))
# 4 — ضائقة مالية → فتتيقن  (icon: wallet → coins)
S.append(scene(4, "night", 18.99,
  icon(240, 270, ICON_WALLET()) +
  c(560, 72, 500, kl("تقرؤها وأنت تشعر بضائقةٍ ماليّة", "19.02,19.46,19.96,20.72,21.38"), 19.0) +
  c(690, 220, 700, kl("فتتيقّن", "21.84", "acc"), 21.6, "big", 1.15) +
  c(960, 72, 500, kl("بأنّ مَن ترك شيئًا لله", "22.82,23.08,23.30,23.56,24.00"), 22.6) +
  c(1060, 72, 600, kl("عوّضه اللهُ خيرًا منه", "24.40,24.92,25.14,25.72"), 24.15) +
  pill(1195, 60, "فسيجعلُ لك مخرجًا", "26.02,26.54,26.74", 25.8, "solid")))
# 5 — التباس → ومن يتق الله  (icon: fork with a question → the right path lights up)
S.append(scene(5, "night", 28.30,
  icon(235, 260, ICON_FORK()) +
  c(540, 72, 500, kl("تقرؤها وأنت تشعر بالتباسٍ", "28.33,28.68,29.00,29.58"), 28.3) +
  c(640, 96, 700, kl('بين <span class="acc">الحقّ</span> والباطل', "30.24,30.46,30.98"), 30.0) +
  c(795, 64, 500, kl("وبسهولةِ وقوعِ الشبهةِ على قلبك", "31.86,33.40,33.76,34.24,34.42"), 31.65) +
  card(930, 34.9, '<div class="quote" style="font-size:92px;font-weight:600;line-height:1.5">'
       + kl("﴿وَمَن يَتَّقِ اللَّهَ", "35.18,36.60,36.96", "gl")
       + kl('يَجْعَل لَّهُ ' + mark("مَخْرَجًا﴾", 38.0), "37.10,37.56,37.74", "gl") + '</div>')))
# 6 — فتتيقن ... الحق واضحا جليا
S.append(scene(6, "night", 39.79,
  c(430, 220, 700, kl("فتتيقّن", "39.85", "acc"), 39.65, "big", 1.15) +
  c(720, 72, 500, kl("بأنّ اللهَ عزّ وجلّ سيبيّنُ لك", "40.68,41.28,41.56,41.78,42.20,43.24"), 40.45) +
  c(830, 104, 700, kl("الحقَّ واضحًا جليًّا", "43.48,44.00,44.80", "acc"), 43.25) +
  pill(1040, 50, "ويُيسّرُ لك الانقيادَ له والعملَ به", "45.56,46.60,46.90,47.44,47.72,48.80", 45.3, "solid")))
# 7 — يا أيها الذين آمنوا
S.append(scene(7, "night", 50.04,
  c(520, 104, 600, kl("﴿يَا أَيُّهَا الَّذِينَ آمَنُوا", "50.07,50.40,50.72,50.98"), 50.05, lh=1.55) +
  c(690, 104, 600, kl("إِن تَتَّقُوا اللَّهَ", "51.52,52.10,52.70"), 51.3, lh=1.55) +
  c(860, 104, 600, kl('يَجْعَل لَّكُمْ ' + mark("فُرْقَانًا﴾", 54.6), "52.96,53.84,54.34"), 52.75, lh=1.55) +
  ref(1090, "[الأنفال: ٢٩]", 51.6)))
# 8 — كلما رددت آياته ازدادت جمالا رونقا
S.append(scene(8, "night", 55.81,
  c(430, 84, 500, kl("كتابُ اللهِ عزّ وجلّ", "55.84,56.40,56.54,56.76"), 55.8) +
  c(540, 84, 500, kl("كلما رددتَ آياتِه", "57.22,57.76,58.22"), 57.0) +
  c(700, 72, 500, kl("ازدادت", "58.90"), 58.7) +
  c(790, 200, 700, kl("جمالًا", "59.94", "acc"), 59.7, "big", 1.15) +
  c(1050, 72, 500, kl("ازدادت", "60.40"), 60.2) +
  c(1140, 200, 700, kl("رونقًا", "61.08", "acc"), 60.85, "big", 1.15)))
# 9 — الشاطبي (audio kept complete)
S.append(scene(9, "night", 61.52,
  c(450, 64, 600, kl('كما يقول <span class="acc">الإمام الشاطبي:</span>', "61.55,62.00,62.30,62.62"), 61.55) +
  card(600, 63.0, '<div class="quote poem">'
       + kl("وَإِنَّ كِتَابَ اللهِ أَوْثَقُ شَافِعٍ", "63.80,64.00,64.44,64.68,65.32", "gl")
       + kl("وَأَغْنَى غَنَاءٍ وَاهِبًا مُتَفَضِّلَا", "65.84,66.54,66.94,67.64", "gl")
       + kl('وَخَيْرُ جَلِيسٍ لَا يُمَلُّ ' + mark("حَدِيثُهُ", 70.9), "68.42,69.28,69.70,69.94,70.36", "gl")
       + kl("وَتَرْدَادُهُ يَزْدَادُ فِيهِ تَجَمُّلَا", "71.02,72.50,73.58,74.04", "gl") + '</div>',
       "padding:40px 30px 44px")))
# 10 — قلب طاهر نقي
S.append(scene(10, "night", 75.65,
  c(440, 76, 500, kl("قراءةُ القرآنِ والإقبالُ عليه", "75.68,75.92,76.32,76.86"), 75.65) +
  c(560, 76, 500, kl("لا يحتاج إلى كثيرِ علم", "77.08,77.28,77.78,77.96,78.76"), 76.85) +
  c(720, 76, 500, kl("ولكن يحتاج إلى", "79.22,79.58,80.04"), 79.0) +
  c(820, 260, 700, kl("قلب", "80.18", "acc"), 79.95, "big", 1.15) +
  c(1210, 88, 600, kl("طاهرٍ نقيّ", "80.60,81.00"), 80.4)))
# 11 — الآية الختامية (the former «جزء من آية» scene is removed)
S.append(scene(11, "night", 82.56,
  c(450, 100, 600, kl("﴿إِنَّ فِي ذَٰلِكَ لَذِكْرَىٰ", "82.59,83.14,83.44,84.20"), 82.6, lh=1.6) +
  c(610, 100, 600, kl('لِمَن كَانَ لَهُ ' + mark("قَلْبٌ", 86.1), "84.86,85.10,85.38,85.82"), 84.6, lh=1.6) +
  c(770, 100, 600, kl("أَوْ أَلْقَى السَّمْعَ", "86.36,86.62,87.00"), 86.1, lh=1.6) +
  c(930, 100, 600, kl("وَهُوَ شَهِيدٌ﴾", "87.22,88.14"), 87.0, lh=1.6) +
  ref(1160, "[ق: ٣٧]", 88.6)))

END = round(_json.load(open(f"{ROOT}/motion-graphics/quran-tadabbur/audio/timing.json"))["duration"] + 2.4, 2)


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

  .icon { position: absolute; left: 50%; }
  .icon svg { width: 100%; height: 100%; overflow: visible; }
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

  /* ---- animated icons ---- */
  $$('.icon path.draw').forEach(p => { const L = p.getTotalLength(); gsap.set(p, { strokeDasharray: L, strokeDashoffset: L }); });
  $$('.icon [data-draw]').forEach(p => tl.to(p, { strokeDashoffset: 0, duration: 0.8, ease: 'power2.inOut' }, +p.dataset.draw));
  $$('.icon [data-pop]').forEach(g => tl.fromTo(g, { scale: 0, opacity: 0, transformOrigin: '50% 50%' },
      { scale: 1, opacity: 1, duration: 0.6, ease: 'back.out(2.4)' }, +g.dataset.pop));
  $$('.icon .sun').forEach(g => {                     // the sun rises from behind the cloud; the cloud steps aside
    const t = +g.dataset.pop;
    tl.fromTo(g, { y: 28 }, { y: 0, duration: 0.9, ease: 'expo.out' }, t)
      .to(g, { rotation: 40, svgOrigin: '138 70', duration: 3.5, ease: 'none' }, t + 0.4)
      .to(g.parentNode.querySelector('.cloud'), { x: -16, y: 8, duration: 0.8, ease: 'power2.out' }, t);
  });
  $$('.icon [data-rain]').forEach(g => {                // rain falls until the hope arrives
    const a = +g.dataset.rain, b = +g.dataset.hide;
    [...g.children].forEach((d, k) => tl.fromTo(d, { y: -6, opacity: 0 }, { y: 16, opacity: 1, duration: 0.42, ease: 'sine.in',
        repeat: Math.max(0, Math.floor((b - a - k * 0.11) / 0.42) - 1) }, a + k * 0.11));
    tl.to(g, { opacity: 0, duration: 0.35 }, b);
  });
  $$('.icon [data-shake]').forEach(g => tl.to(g, { keyframes: { rotation: [0, -7, 6, -5, 4, -2, 0] }, svgOrigin: '100 124',
      duration: 0.9, ease: 'none' }, +g.dataset.shake));
  $$('.icon .coins > g').forEach(g => tl.fromTo(g, { y: 70 }, { y: 0, duration: 0.7, ease: 'back.out(2.2)' }, +g.dataset.pop));
  $$('.icon [data-fade]').forEach(g => tl.to(g, { opacity: 0.22, duration: 0.6 }, +g.dataset.fade));
  $$('.icon [data-glow]').forEach(g => tl.to(g.querySelectorAll('path'), { stroke: '#b5dc55', duration: 0.5 }, +g.dataset.glow)
      .fromTo(g, { filter: 'drop-shadow(0 0 0 rgba(181,220,85,0))' }, { filter: 'drop-shadow(0 0 14px rgba(181,220,85,.7))', duration: 0.6 }, +g.dataset.glow));
  $$('.icon').forEach(ic => tl.fromTo(ic, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6 },
      +ic.closest('.scene').dataset.start - 0.05));

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
