# Builds motion-graphics/salah/index.html — القالب الليلي بدون مربعات (template ٤), no title / no counter.
# Voice-first reel «الصلاة: قرّة العين» — night template. Times = audio/voice-clean.m4a. Transition: «مدّ ضوئي» (day variant), continuous with the speech.
# Declarative: data-t (spoken word times), data-in / data-fx (big|up|card|pill|chip), data-mark, data-strike,
# icon attributes: data-draw, data-pop, data-rise, data-wave, data-fill, data-beat, data-shoot, data-tilt, data-drip, data-swing.
import json, math
ROOT = "/home/user/Design-course"
DIR = f"{ROOT}/motion-graphics/salah"
END = round(json.load(open(f"{DIR}/audio/timing.json"))["duration"] + 2.4, 2)
SEND = 40.15

def kl(text, t, cls=""):
    return f'<span class="line kline {cls}" data-t="{t}">{text}</span>'
def c(top, fs, w, inner, at, fx="up", lh=None):
    lhs = f"line-height:{lh};" if lh else ""
    return f'      <div class="c" style="top:{top}px;font-size:{fs}px;font-weight:{w};{lhs}" data-in="{at}" data-fx="{fx}">{inner}</div>\n'
def pill(top, fs, text, t, at, cls="", strike=None):
    st = f'<i class="strike" data-strike="{strike}"></i>' if strike else ""
    return (f'      <div class="pillrow" style="top:{top}px;font-size:{fs}px" data-in="{at}" data-fx="pill">'
            f'<span class="pill {cls}"><span class="kline" data-t="{t}">{text}</span>{st}</span></div>\n')
def ref(top, text, at):
    return f'      <div class="refchip" style="top:{top}px" data-in="{at}" data-fx="chip"><span>{text}</span></div>\n'
def mark(text, at): return f'<span class="mark" data-mark="{at}">{text}</span>'
def card(top, at, inner, src=None, src_at=None):
    sr = f'<div class="cardref" data-in="{src_at}" data-fx="chip"><span>{src}</span></div>' if src else ""
    return f'      <div class="glass" style="top:{top}px" data-in="{at}" data-fx="card">{inner}{sr}</div>\n'
def icon(top, size, svg, cls=""):
    return f'      <div class="icon {cls}" style="top:{top}px;width:{size}px;height:{size}px;margin-left:-{size // 2}px">{svg}</div>\n'
def scene(i, start, body):
    return f'    <!-- ===== S{i} ({start}s) ===== -->\n    <section class="scene" id="s{i}" data-start="{start}">\n{body}    </section>\n\n'
A = lambda s: f'<span class="acc">{s}</span>'

# ------------------------------------------------------------------ icons (viewBox 200×200, stroke drawings)
SVG = '<svg viewBox="0 0 200 200" fill="none" stroke-linecap="round" stroke-linejoin="round">{}</svg>'
T, TL, G = "var(--teal)", "var(--teal-line)", "#b5dc55"
def d(path, t, col=T, w=7, fill=None):
    f = f' fill="{fill}"' if fill else ""
    return f'<path class="draw" data-draw="{t}" stroke="{col}" stroke-width="{w}"{f} d="{path}"/>'

HL = "#d2ee94"
GOLD = "#e2bd62"
CARD = "var(--card)"
FAINT = "rgba(238,243,244,.14)"

def lbl(x, top, text, at, cls=""):      # a label centred on stage-x
    return f'      <div class="lbl {cls}" style="left:{x - 170}px;top:{top}px" data-in="{at}" data-fx="chip"><span>{text}</span></div>\n'

def stars(t, pts):
    return "".join(f'<circle data-pop="{t + k * 0.12}" cx="{x}" cy="{y}" r="{r}" fill="#eef3f4" opacity=".85"/>' for k, (x, y, r) in enumerate(pts))

def ic_kaaba(t):           # the Kaaba under a night sky
    return SVG.format(f'''
        {stars(t + 0.5, ((24, 30, 2.5), (170, 24, 3), (186, 70, 2), (14, 84, 2), (120, 14, 2)))}
        <g data-rise="{t}">
          <path d="M44 74 L76 50 H168 L150 74 Z" fill="#1c2427" stroke="{T}" stroke-width="4"/>
          <path d="M150 74 L168 50 V156 L150 182 Z" fill="#0d1112" stroke="{T}" stroke-width="4"/>
          <path d="M44 74 H150 V182 H44 Z" fill="#070a0b" stroke="{T}" stroke-width="4"/>
          <path d="M44 100 H150 L168 76" stroke="{GOLD}" stroke-width="7"/>
          <path d="M50 108 H144" stroke="{GOLD}" stroke-width="2" opacity=".7"/>
          <rect x="112" y="128" width="22" height="54" rx="3" fill="{GOLD}" opacity=".9"/></g>
        {d("M8 186 H192", t + 0.3, TL, 4)}''')

def ic_moon(t):            # a crescent and a rising thread of light (a supplication ascending)
    return SVG.format(f'''
        <g data-pop="{t}"><path d="M116 36 A48 48 0 1 0 160 118 A38 38 0 1 1 116 36 Z" fill="{G}"/></g>
        {stars(t + 0.3, ((40, 50, 3), (60, 120, 2.5), (176, 40, 2.5), (30, 150, 2)))}''')

def ic_house(t, lit, moon):   # a home whose windows light up one by one
    win = lambda x, y, at: (f'<rect x="{x}" y="{y}" width="24" height="26" rx="4" fill="#0b1112" stroke="{T}" stroke-width="3"/>'
                            f'<rect data-fill="{at}" x="{x}" y="{y}" width="24" height="26" rx="4" fill="{GOLD}" fill-opacity="0"/>')
    return SVG.format(f'''
        <g data-pop="{moon}"><path d="M150 14 A20 20 0 1 0 170 46 A16 16 0 1 1 150 14 Z" fill="{G}"/></g>
        {d("M26 104 L100 42 L174 104", t, T, 7)}{d("M40 96 V182 H160 V96", t + 0.2, T, 7)}
        {win(56, 112, lit)}{win(120, 112, lit + 0.3)}
        <rect x="88" y="132" width="26" height="50" rx="12" fill="#0b1112" stroke="{T}" stroke-width="3"/>
        <rect data-fill="{lit + 0.6}" x="88" y="132" width="26" height="50" rx="12" fill="{GOLD}" fill-opacity="0"/>
        {d("M14 184 H186", t + 0.1, TL, 4)}''')

def ic_lanterns(t, a, b, c_):   # three lanterns: joy, intimacy, delight — each lights when it is said
    def lan(x, at):
        return (f'<circle data-fill="{at}" cx="{x}" cy="120" r="34" fill="{GOLD}" fill-opacity="0" filter="url(#blur)"/>'
                f'{d(f"M{x} 0 V70", t, FAINT, 2)}'
                f'<path d="M{x - 10} 70 H{x + 10} L{x + 6} 82 H{x - 6} Z" fill="{T}"/>'
                f'<path d="M{x - 13} 84 Q{x - 24} 117 {x - 13} 150 H{x + 13} Q{x + 24} 117 {x + 13} 84 Z" fill="#0b1112" stroke="{T}" stroke-width="4"/>'
                f'<path data-fill="{at}" d="M{x - 8} 92 Q{x - 16} 117 {x - 8} 142 H{x + 8} Q{x + 16} 117 {x + 8} 92 Z" fill="{GOLD}" fill-opacity="0"/>'
                f'<path d="M{x - 8} 150 H{x + 8} L{x} 162 Z" fill="{T}"/>')
    return SVG.format(f'<defs><filter id="blur" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="9"/></filter></defs>{lan(160, a)}{lan(100, b)}{lan(40, c_)}')

def ic_eye(t, open_):      # «the coolness of my eyes»: an eye opens, light in it
    return SVG.format(f'''<g data-sy="{open_},0.08,100,100">
        <path d="M14 100 Q100 22 186 100 Q100 178 14 100 Z" fill="#0b1112" stroke="{T}" stroke-width="6"/>
        <circle cx="100" cy="100" r="34" fill="{TL}"/><circle cx="100" cy="100" r="15" fill="#070a0b"/>
        <circle cx="112" cy="88" r="7" fill="#eef3f4"/></g>
        {stars(open_ + 0.3, ((30, 40, 3), (172, 36, 3.5), (160, 170, 2.5)))}''')

def ic_minaret(t, call):   # the adhan spreading from a minaret
    return SVG.format(f'''
        <circle data-ring="{call}" opacity="0" cx="100" cy="56" r="40" stroke="{G}" stroke-width="4"/>
        <g data-rise="{t}">
          <path d="M100 6 A7 7 0 1 0 106 18 A5.5 5.5 0 1 1 100 6 Z" fill="{G}"/>
          <path d="M88 64 Q100 22 112 64 Z" fill="{T}"/>
          <path d="M78 64 H122 V74 H78 Z" fill="{T}"/>
          <path d="M86 74 H114 V190 H86 Z" fill="#0b1112" stroke="{T}" stroke-width="5"/>
          <rect x="95" y="92" width="10" height="18" rx="5" fill="{GOLD}"/><rect x="95" y="130" width="10" height="18" rx="5" fill="{GOLD}" opacity=".6"/></g>''')

def ic_dawn(t):            # dawn: the sun rises behind a mosque on the horizon
    return SVG.format(f'''
        <g data-rise="{t + 0.3}"><circle cx="100" cy="128" r="46" fill="#f2c76b" opacity=".95"/>
          <g stroke="#f2c76b" stroke-width="5"><path d="M100 66 V50 M56 84 L46 74 M144 84 L154 74 M38 128 H24 M162 128 H176"/></g></g>
        <path d="M72 168 V140 Q72 116 100 106 Q128 116 128 140 V168 Z" fill="#070a0b" stroke="{T}" stroke-width="4"/>
        <path d="M142 168 V118 L148 106 L154 118 V168 Z" fill="#070a0b" stroke="{T}" stroke-width="4"/>
        <path d="M46 168 V118 L52 106 L58 118 V168 Z" fill="#070a0b" stroke="{T}" stroke-width="4"/>
        {d("M6 168 H194", t, TL, 5)}''')

def ic_guidance(t, steps_):   # «He increases them in guidance»: rings of light grow, one per word
    rings = "".join(f'<circle data-pop="{at}" cx="100" cy="100" r="{r}" stroke="{G}" stroke-width="{4 - k * 0.6:.1f}" opacity="{0.95 - k * 0.18:.2f}"/>'
                    for k, (r, at) in enumerate(zip((34, 52, 70, 88), steps_)))
    return SVG.format(f'''{rings}
        <circle data-ring="{steps_[-1] + 0.2}" opacity="0" cx="100" cy="100" r="60" stroke="{G}" stroke-width="3"/>
        <path data-pop="{t}" d="M100 70 L108 92 L130 100 L108 108 L100 130 L92 108 L70 100 L92 92 Z" fill="{G}"/>''')

S = []
# 1 — خليل الرحمن + آية الدعاء (شريحة واحدة)
S.append(scene(1, 0,
  c(410, 96, 600, kl(f'خليلُ {A("الرحمن")}', "0.02,1.18"), 0.0) +
  c(540, 76, 500, kl("إبراهيمُ عليه السلام", "1.82,2.26,2.44"), 1.7) +
  c(650, 62, 500, kl('<span class="mute">كان يدعو ويقول:</span>', "2.72,2.88,3.20"), 2.6) +
  card(790, 3.35, '<div class="quote" style="font-size:76px;font-weight:600;line-height:1.7">'
       + kl("﴿رَبِّ اجْعَلْنِي " + mark("مُقِيمَ الصَّلَاةِ", 4.95), "3.52,3.90,4.34,4.68", "gl")
       + kl("وَمِن ذُرِّيَّتِي ۚ رَبَّنَا", "5.34,5.60,6.24", "gl")
       + kl("وَتَقَبَّلْ دُعَاءِ﴾", "6.70,7.54", "gl") + '</div>', "[إبراهيم: ٤٠]", 7.8)))
# 2 — نصّية: مدح الله إسماعيل
S.append(scene(2, 8.18,
  c(560, 76, 500, kl('<span class="mute">واللهُ سبحانه وتعالى</span>', "8.22,8.34,8.64"), 8.1) +
  c(680, 96, 600, kl("مدحَ نبيَّه", "8.82,9.18"), 8.7) +
  c(830, 170, 700, kl(A("إسماعيلَ"), "9.54"), 9.4, "big", 1.2) +
  c(1050, 76, 500, kl("عليه السلام", "10.02,10.18"), 9.9) +
  c(1160, 64, 500, kl('<span class="mute">فقال:</span>', "10.52"), 10.4)))
# 3 — مزدوجة: يأمر أهله بالصلاة (بيت تضيء نوافذه)
S.append(scene(3, 11.06,
  icon(250, 340, ic_house(11.03, 12.32, 15.04)) +
  card(690, 11.0, '<div class="quote" style="font-size:72px;font-weight:600;line-height:1.7">'
       + kl("﴿وَكَانَ يَأْمُرُ أَهْلَهُ", "11.10,11.50,11.92", "gl")
       + kl(mark("بِالصَّلَاةِ", 12.45) + " وَالزَّكَاةِ", "12.32,12.92", "gl")
       + kl("وَكَانَ عِندَ رَبِّهِ مَرْضِيًّا﴾", "13.62,14.08,14.40,15.04", "gl") + '</div>', "[مريم: ٥٥]", 15.3)))
# 4 — مزدوجة: مصدر فرح وأنس وسرور (ثلاثة فوانيس)
S.append(scene(4, 16.00,
  c(330, 72, 500, kl("كانت الصلاةُ بالنسبة للنبيّ ﷺ", "16.03,16.20,16.52,16.90,17.20"), 15.95) +
  c(440, 96, 600, kl(A("مصدرَ"), "18.00"), 17.85) +
  icon(560, 600, ic_lanterns(16.1, 18.48, 18.88, 19.32)) +
  lbl(240 + 160 * 3, 1110, "فرحٍ", 18.45) + lbl(240 + 100 * 3, 1110, "وأُنسٍ", 18.85) + lbl(240 + 40 * 3, 1110, "وسرور", 19.3)))
# 5 — حديث: وجعلت قرة عيني في الصلاة (بلا أيقونة)
S.append(scene(5, 20.00,
  c(560, 72, 500, kl('<span class="mute">كان يقول:</span>', "20.03,20.15"), 19.95) +
  card(690, 20.2, '<div class="quote" style="font-size:86px;font-weight:600;line-height:1.75">'
       + kl("«وَجُعِلَتْ " + mark("قُرَّةُ عَيْنِي", 21.7), "20.36,20.94,21.46", "gl")
       + kl("فِي الصَّلَاةِ»", "22.06,22.22", "gl") + '</div>', "[رواه النسائي]", 22.4)))
# 6 — نصّية: ليرتاح بها لا ليرتاح منها
S.append(scene(6, 22.90,
  c(470, 76, 500, kl("وكان النبيُّ ﷺ", "22.92,23.10,23.50"), 22.85) +
  c(580, 76, 500, kl("يؤدّيها", "24.36"), 24.2) +
  pill(740, 110, "ليرتاحَ بها", "24.86,25.40", 24.7) +
  pill(960, 84, "لا ليرتاحَ منها", "25.74,25.98,26.60", 25.6, "dash", strike=26.9)))
# 7 — مزدوجة: يا بلال أقم الصلاة أرحنا بها (مئذنة)
S.append(scene(7, 27.18,
  icon(200, 380, ic_minaret(27.15, 29.6)) +
  c(600, 64, 500, kl("وكان يقول للصحابيّ الجليل", "27.21,27.30,27.64,28.04"), 27.1) +
  c(700, 76, 600, kl(f'{A("بلالٍ")} رضي الله عنه:', "28.40,28.64,28.90,29.02"), 28.3) +
  card(830, 29.45, '<div class="quote" style="font-size:78px;font-weight:600;line-height:1.7">'
       + kl("«يَا بِلَالُ أَقِمِ الصَّلَاةَ،", "29.60,29.80,30.51,30.80", "gl")
       + kl(mark("أَرِحْنَا بِهَا»", 32.3), "31.65,32.10", "gl") + '</div>', "[صحيح أبي داود]", 32.35)))
# 8 — مزدوجة: صلاة الفجر هي البداية (شروق)
S.append(scene(8, 32.86,
  icon(300, 400, ic_dawn(32.83)) +
  c(760, 96, 600, kl("صلاةُ", "32.91"), 32.8) +
  c(880, 170, 700, kl(A("الفجر"), "33.52"), 33.35, "big", 1.2) +
  c(1110, 96, 600, kl("هي " + mark("البداية", 34.6), "34.15,34.36"), 34.0) +
  c(1240, 64, 500, kl('<span class="mute">بإذن الله</span>', "34.86,35.24"), 34.7)))
# 9 — آية الختام (بلا أيقونة) + أيقونة المشاركة
S.append(scene(9, 36.16,
  card(640, 36.1, '<div class="quote" style="font-size:92px;font-weight:600;line-height:1.75">'
       + kl("﴿وَالَّذِينَ اهْتَدَوْا", "36.21,36.65", "gl")
       + kl(mark("زَادَهُمْ هُدًى", 37.85), "37.04,37.68", "gl")
       + kl("وَآتَاهُمْ تَقْوَاهُمْ﴾", "38.63,39.22", "gl") + '</div>', "[محمد: ١٧]", 39.5) +
  '      <svg id="send" viewBox="0 0 48 48" fill="none" stroke="var(--ink)" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round">'
  '<path d="M43 5 L5 19 L21 27 L29 43 Z"/><path d="M43 5 L21 27"/></svg>\n'))

HTML = r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>قرّة العين — ليلي</title>
<!-- ريل «قرّة العين» بالقالب الليلي بدون مربعات، بلا عنوان ولا ترقيم. يُولَّد من tools/build.py -->
<style>
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-400.ttf") format("truetype"); font-weight: 400; }
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-500.ttf") format("truetype"); font-weight: 500; }
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-600.ttf") format("truetype"); font-weight: 600; }
  @font-face { font-family: "Plex Ar"; src: url("fonts/IBMPlexSansArabic-700.ttf") format("truetype"); font-weight: 700; }
  /* القالب ٣ — النهاري بدون مربعات */
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

  .glow { position: absolute; inset: -160px; pointer-events: none; }
  #glow-a { background: radial-gradient(circle at calc(100% - 160px) 160px, rgba(40, 130, 170, .40) 0px, rgba(40, 130, 170, .17) 270px, rgba(40, 130, 170, 0) 660px); }
  #glow-b { background: radial-gradient(circle at 160px calc(100% - 160px), rgba(120, 170, 50, .26) 0px, rgba(120, 170, 50, .11) 270px, rgba(120, 170, 50, 0) 680px); }

  .scene { position: absolute; inset: 0; --p: 0%;
           -webkit-mask-image: linear-gradient(to bottom, #000 0%, #000 calc(var(--p) - 22%), transparent var(--p));
                   mask-image: linear-gradient(to bottom, #000 0%, #000 calc(var(--p) - 22%), transparent var(--p)); }
  .scene.out { -webkit-mask-image: linear-gradient(to bottom, transparent 0%, transparent calc(var(--p) - 22%), #000 var(--p));
                       mask-image: linear-gradient(to bottom, transparent 0%, transparent calc(var(--p) - 22%), #000 var(--p)); }
  .scene.live { -webkit-mask-image: none; mask-image: none; }
  /* day tide: a band of soft morning light */
  #tide { position: absolute; left: -10%; right: -10%; height: 520px; top: 0; pointer-events: none; opacity: 0; mix-blend-mode: screen;
          background: radial-gradient(ellipse 60% 50% at 50% 50%, rgba(76, 179, 214, .55), rgba(76, 179, 214, .16) 45%, transparent 72%),
                      radial-gradient(ellipse 34% 22% at 50% 50%, rgba(181, 220, 85, .45), transparent 70%); filter: blur(18px); }

  .c { position: absolute; left: 0; right: 0; text-align: center; }
  .line { display: block; white-space: nowrap; }
  .k { display: inline-block; }
  .acc { color: var(--teal); }
  .mark { background-image: linear-gradient(var(--hl), var(--hl)); background-repeat: no-repeat; background-position: 100% 86%; background-size: 0% 38%; padding: 0 8px; }
  .glass { position: absolute; left: 110px; right: 110px; border-radius: 48px; background: var(--card); padding: 58px 40px 44px; text-align: center;
           box-shadow: 0 2px 0 rgba(30, 60, 70, .05), 0 14px 0 -4px var(--card-edge), 0 30px 60px var(--card-shadow); }
  .glass .gl { display: block; white-space: nowrap; }
  .pillrow { position: absolute; left: 0; right: 0; text-align: center; }
  .pill { display: inline-block; padding: 14px 48px 22px; border-radius: 999px; font-weight: 600; white-space: nowrap; background: var(--teal); color: #0b1214; }
  .pill.ghost { background: transparent; color: var(--muted); border: 4px dashed var(--teal-line); position: relative; }
  .strike { position: absolute; left: 30px; right: 30px; top: 52%; height: 8px; border-radius: 8px; background: #d9534f; transform: scaleX(0); transform-origin: 100% 50%; }
  .cardref { margin-top: 26px; font-size: 44px; font-weight: 500; color: var(--muted); }
  .cardref span { display: inline-block; }
  .refchip { position: absolute; left: 0; right: 0; text-align: center; font-size: 40px; color: var(--muted); }
  .icon { position: absolute; left: 50%; }
  .icon svg, .mini svg { width: 100%; height: 100%; overflow: visible; }
  .mini { position: absolute; border-radius: 40px; background: #fff; padding: 18px;
          box-shadow: 0 10px 0 -4px var(--card-edge), 0 24px 50px var(--card-shadow); }
  .jr { position: absolute; right: 330px; left: 60px; text-align: right; direction: rtl; }
  .jr span { display: inline-block; }
  .jr.jt span { font-size: 64px; font-weight: 700; }
  .jr.ji span { font-size: 46px; font-weight: 500; color: var(--muted); background: #fff; padding: 12px 30px 18px; border-radius: 22px;
                box-shadow: 0 8px 0 -3px var(--card-edge), 0 18px 40px var(--card-shadow); white-space: nowrap; }
  .jr.ji.good span { font-size: 52px; color: var(--ink); font-weight: 600; background: var(--hl); }
  .jr i { display: inline-block; width: 26px; height: 26px; border-radius: 50%; margin-left: 16px; vertical-align: -2px; }
  .jr i.x { background: #d7dfe1; }
  .jr i.ok { background: var(--green); box-shadow: 0 0 0 5px rgba(27, 122, 156, .25); }
  .line.inl { display: inline-block; }
  .pill.dash { background: transparent; color: var(--muted); border: 4px dashed rgba(238, 243, 244, .25); position: relative; }
  .lbl { position: absolute; width: 340px; text-align: center; }
  .lbl span { display: inline-block; font-size: 64px; font-weight: 700; color: #e2bd62; }
  .glass .quote .k { color: var(--ink); }
  .mute { color: var(--muted); }
  .pill.soft { background: var(--hl); color: var(--ink); }
  .pill.chip { background: var(--card); color: var(--ink); box-shadow: 0 10px 0 -4px var(--card-edge), 0 24px 50px var(--card-shadow); padding: 18px 44px 26px 52px; }
  .track { position: absolute; left: 0; right: 0; top: 280px; display: flex; justify-content: center; gap: 14px; direction: rtl; }
  .track i { position: relative; width: 150px; height: 14px; border-radius: 7px; background: #dfe5e7; overflow: hidden; }
  .track i.done { background: var(--teal); }
  .track i b { position: absolute; inset: 0; border-radius: 7px; background: var(--green); transform: scaleX(0); transform-origin: 100% 50%; }
  .track i.now b { display: block; }
  .stepno { position: absolute; top: 34px; left: 0; right: 0; text-align: center; font-size: 44px; font-weight: 600; color: var(--teal); }
  .ri { display: inline-block; width: 1.25em; height: 1.25em; vertical-align: -0.32em; margin-left: 0.35em; }
  .ri svg { width: 100%; height: 100%; overflow: visible; }
  #send { position: absolute; left: 110px; top: 1440px; width: 96px; height: 96px; }
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
  $$('svg path.draw, svg circle.draw').forEach(p => { const L = p.getTotalLength(); gsap.set(p, { strokeDasharray: L, strokeDashoffset: L }); });
  $$('svg [data-draw]').forEach(p => tl.to(p, { strokeDashoffset: 0, duration: p.closest('.fast') ? 0.6 : 0.7, ease: 'power2.inOut' }, +p.dataset.draw));
  $$('svg [data-pop]').forEach(g => tl.fromTo(g, { scale: 0, opacity: 0, transformOrigin: '50% 50%' }, { scale: 1, opacity: 1, duration: 0.55, ease: 'back.out(2.4)' }, +g.dataset.pop));
  $$('svg [data-rise]').forEach(g => tl.fromTo(g, { y: 46, opacity: 0 }, { y: 0, opacity: 1, duration: 1.1, ease: 'expo.out' }, +g.dataset.rise)
      .to(g, { y: -4, duration: 1.2, ease: 'sine.inOut', yoyo: true, repeat: 1 }, +g.dataset.rise + 1.1));
  $$('svg [data-wave]').forEach(g => [...g.children].forEach((w, k) =>
      tl.fromTo(w, { opacity: 0.35, scaleY: 0.35, transformOrigin: '50% 100%' }, { opacity: 1, scaleY: 1, duration: 0.28, ease: 'sine.inOut', yoyo: true, repeat: 9 }, +g.dataset.wave + k * 0.09)));
  $$('svg [data-fill]').forEach(p => tl.to(p, { attr: { 'fill-opacity': 0.9 }, duration: 0.7, ease: 'power2.out' }, +p.dataset.fill));
  $$('.icon').forEach(ic => { const r = ic.querySelector('[data-beat]'); if (r) {      // heartbeat once the heart is full
      const t = +r.dataset.beat;
      [0, 0.55].forEach(d => tl.to(ic, { keyframes: { scale: [1, 1.08, 1, 1.04, 1] }, duration: 0.45, ease: 'none' }, t + d)); } });
  if (document.getElementById('send'))                   // share icon flies in at the end
    tl.fromTo('#send', { x: -140, y: 140, opacity: 0, rotation: -25 }, { x: 0, y: 0, opacity: 1, rotation: 0, duration: 0.9, ease: 'expo.out' }, __SEND__)
      .to('#send', { x: 10, y: -10, duration: 0.45, ease: 'sine.inOut', yoyo: true, repeat: 1 }, __SEND__ + 0.9);

  $$('svg [data-shoot]').forEach(g => tl.fromTo(g, { x: 110, y: -110, opacity: 0 }, { x: 0, y: 0, opacity: 1, duration: 0.4, ease: 'power4.in' }, +g.dataset.shoot)
      .to(g.closest('.icon'), { keyframes: { x: [0, -10, 6, 0] }, duration: 0.35, ease: 'none' }, +g.dataset.shoot + 0.4));
  $$('svg [data-tilt]').forEach(g => { const [t, lv] = g.dataset.tilt.split(',').map(Number);
      gsap.set(g, { svgOrigin: '100 62' });
      tl.fromTo(g, { rotation: -16 }, { rotation: 12, duration: 1.0, ease: 'sine.inOut' }, t)
        .to(g, { rotation: -8, duration: 0.9, ease: 'sine.inOut' }, t + 1.0)
        .to(g, { rotation: 5, duration: 0.8, ease: 'sine.inOut' }, t + 1.9)
        .to(g, { rotation: 0, duration: 0.7, ease: 'back.out(2)' }, lv); });
  $$('svg [data-drip]').forEach(g => [...g.children].forEach((w, k) =>
      tl.fromTo(w, { y: 0, opacity: 0 }, { keyframes: { y: [0, 40, 90], opacity: [0, 1, 0] }, duration: 0.7, ease: 'power1.in', repeat: 2, repeatDelay: 0.2 }, +g.dataset.drip + k * 0.3)));
  $$('svg [data-swing]').forEach(g => { gsap.set(g, { svgOrigin: '100 104' });
      tl.to(g, { keyframes: { rotation: [0, -14, 10, -6, 3, 0] }, duration: 1.2, ease: 'none' }, +g.dataset.swing); });
  $$('[data-strike]').forEach(s => tl.to(s, { scaleX: 1, duration: 0.45, ease: 'power2.inOut' }, +s.dataset.strike)
      .to(s.closest('.pillrow'), { opacity: 0.45, duration: 0.4 }, +s.dataset.strike + 0.3));

  $$('svg [data-grow]').forEach(r => { const [t, du] = r.dataset.grow.split(',').map(Number);
      tl.fromTo(r, { scaleX: 0, transformOrigin: '100% 50%' }, { scaleX: 1, duration: du, ease: 'none' }, t); });
  $$('svg [data-slide]').forEach(g => { const [a1, a2, dx] = g.dataset.slide.split(',').map(Number);
      tl.to(g, { x: dx, duration: 0.5, ease: 'power3.inOut' }, a1).to(g, { x: 2 * dx, duration: 0.5, ease: 'power3.inOut' }, a2); });
  $$('svg [data-rot]').forEach(g => { const [t, from, ox, oy] = g.dataset.rot.split(',').map(Number);
      gsap.set(g, { svgOrigin: ox + ' ' + oy, rotation: from });
      tl.to(g, { rotation: 0, duration: 0.22, ease: 'power4.in' }, t).to(g.closest('.icon'), { keyframes: { y: [0, 8, 0] }, duration: 0.25 }, t + 0.22); });
  $$('svg [data-out]').forEach(g => tl.to(g, { opacity: 0, y: 10, duration: 0.35 }, +g.dataset.out));
  $$('svg [data-ring]').forEach(r => [0, 0.7, 1.4].forEach(dl =>
      tl.fromTo(r, { scale: 0.3, opacity: 1, transformOrigin: '50% 50%' }, { scale: 1.8, opacity: 0, duration: 0.7, ease: 'sine.out', immediateRender: false }, +r.dataset.ring + dl)));
  $$('.track b[data-grow]').forEach(r => { const [t, du] = r.dataset.grow.split(',').map(Number);
      tl.fromTo(r, { scaleX: 0 }, { scaleX: 1, duration: du, ease: 'power2.out' }, t); });
  $$('svg [data-sx]').forEach(g => { const [t, to, ox, oy] = g.dataset.sx.split(',').map(Number);
      gsap.set(g, { svgOrigin: ox + ' ' + oy }); tl.to(g, { scaleX: to, duration: 0.6, ease: 'power3.inOut' }, t); });
  $$('svg [data-fly]').forEach(g => tl.fromTo(g, { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }, +g.dataset.fly - 0.9)
      .to(g, { y: -70, duration: 1.2, ease: 'power2.in' }, +g.dataset.fly).to(g, { y: -50, duration: 0.6, ease: 'sine.out' }, +g.dataset.fly + 1.2));
  $$('svg [data-slidein]').forEach(g => tl.fromTo(g, { x: 60, opacity: 0 }, { x: 40, opacity: 1, duration: 0.4 }, +g.dataset.slidein - 0.8)
      .to(g, { x: 0, duration: 0.35, ease: 'back.out(3)' }, +g.dataset.slidein));
  $$('svg [data-spin]').forEach(g => { const [t, du, deg] = g.dataset.spin.split(',').map(Number);
      gsap.set(g, { svgOrigin: '100 100' }); tl.to(g, { rotation: deg, duration: du, ease: 'none' }, t); });
  $$('svg [data-sy]').forEach(g => { const [t, from, ox, oy] = g.dataset.sy.split(',').map(Number);
      gsap.set(g, { svgOrigin: ox + ' ' + oy, scaleY: from }); tl.to(g, { scaleY: 1, duration: 0.6, ease: 'back.out(1.6)' }, t); });
  $$('svg [data-move]').forEach(g => { const v = g.dataset.move.split(',').map(Number), [t, du, dx, dy] = v;
      const kx = v.length > 4 ? [0, v[4], dx] : [0, dx], ky = v.length > 4 ? [0, v[5], dy] : [0, dy];
      tl.fromTo(g, { x: 0, y: 0 }, { keyframes: { x: kx, y: ky }, duration: du, ease: 'sine.inOut' }, t); });
  $$('.ri[data-pop]').forEach(g => tl.fromTo(g, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(2.4)' }, +g.dataset.pop));

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
  /* keep a wide margin on both sides: shrink any line or pill wider than the safe column */
  const MAXW = 1080 - 2 * 120;
  const fitW = () => {
    $$('.c').forEach(el => {
      const r = el.style.right, w0 = el.style.width;
      el.style.right = 'auto'; el.style.width = 'max-content';
      const w = el.offsetWidth; el.style.right = r; el.style.width = w0;
      if (w > MAXW) el.style.fontSize = (parseFloat(el.style.fontSize) * MAXW / w).toFixed(1) + 'px';
    });
    $$('.pillrow').forEach(el => { const w = el.firstElementChild.offsetWidth;
      if (w > MAXW) el.style.fontSize = (parseFloat(el.style.fontSize) * MAXW / w).toFixed(1) + 'px'; });
  };
  window.__ready = document.fonts.ready.then(() => { fitW(); return true; });

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

out = HTML.replace("__SCENES__", "".join(S)).replace("__END__", str(END)).replace("__SEND__", str(SEND))
open(f"{DIR}/index.html", "w", encoding="utf-8").write(out)
print("written", len(out), "END", END)
