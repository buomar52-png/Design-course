# Builds motion-graphics/course-promo/index.html — القالب النهاري بدون مربعات (template ٣), no title / no counter.
# Voice-first story ad for the course (إعلان الدورة). Times = audio/voice-clean.m4a. Transition: «مدّ ضوئي» (day variant), continuous with the speech.
# Declarative: data-t (spoken word times), data-in / data-fx (big|up|card|pill|chip), data-mark, data-strike,
# icon attributes: data-draw, data-pop, data-rise, data-wave, data-fill, data-beat, data-shoot, data-tilt, data-drip, data-swing.
import json
ROOT = "/home/user/Design-course"
DIR = f"{ROOT}/motion-graphics/course-promo"
END = round(json.load(open(f"{DIR}/audio/timing.json"))["duration"] + 2.4, 2)
SEND = 50.75

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
def ic_note(t, clock):     # a written page left waiting: lines, then an hourglass
    lines = "".join(d(f"M72 {y} H{x}", t + 0.3 + k * 0.12, TL, 6) for k, (y, x) in enumerate(((78, 134), (100, 134), (122, 118), (144, 128))))
    return SVG.format(f'''
        {d("M52 22 H128 L152 46 V182 H52 Z", t, fill="var(--bg)")}{d("M128 22 V46 H152", t + 0.2, T, 6)}{lines}
        <g data-pop="{clock}"><circle cx="152" cy="160" r="30" fill="{G}"/>
          <path d="M140 144 H164 M140 176 H164 M143 145 Q152 160 143 175 M161 145 Q152 160 161 175" stroke="var(--ink)" stroke-width="4"/></g>''')

def ic_clones(t0, same):   # nine identical results
    out = ""
    for k in range(9):
        x, y = 8 + (k % 3) * 64, 8 + (k // 3) * 64
        out += (f'<g data-pop="{t0 + k * 0.2}"><rect x="{x}" y="{y}" width="56" height="56" rx="12" fill="#fff" stroke="{TL}" stroke-width="3"/>'
                f'<circle cx="{x + 40}" cy="{y + 18}" r="8" fill="{G}"/><path d="M{x + 12} {y + 36} H{x + 44} M{x + 12} {y + 46} H{x + 34}" stroke="{TL}" stroke-width="4"/></g>')
    return SVG.format(f'<g data-beat="{same}">{out}</g>')

def ic_phone(t, play):     # this very story: a phone with story bars filling
    bars = "".join(f'<rect x="{x}" y="28" width="24" height="5" rx="2.5" fill="#d7dfe1"/><rect data-grow="{t + 0.5 + k * 0.8},0.8" x="{x}" y="28" width="24" height="5" rx="2.5" fill="{G}"/>'
                   for k, x in enumerate((116, 88, 60)))
    return SVG.format(f'''
        {d("M64 12 H136 Q150 12 150 26 V174 Q150 188 136 188 H64 Q50 188 50 174 V26 Q50 12 64 12 Z", t, fill="var(--bg)")}{bars}
        <path data-pop="{play}" d="M88 80 L124 100 L88 120 Z" fill="{T}"/>
        {d("M70 148 H130", t + 0.4, TL, 6)}{d("M82 162 H118", t + 0.5, TL, 6)}''')

def ri(svg, at):           # small icon at the start (right) of a list row
    return f'<span class="ri" data-pop="{at}">{svg}</span>'
SMALL = '<svg viewBox="0 0 200 200" fill="none" stroke-linecap="round" stroke-linejoin="round">{}</svg>'
THINK = SMALL.format(f'<path d="M64 122 Q40 122 40 100 Q40 78 64 80 Q68 54 96 54 Q118 54 126 70 Q154 66 160 92 Q176 98 172 114 Q168 128 150 128 H70 Z" fill="{HL}" stroke="{T}" stroke-width="9"/><circle cx="56" cy="150" r="10" fill="{T}"/><circle cx="40" cy="172" r="6" fill="{T}"/>')
BLOCKS = SMALL.format(f'<rect x="30" y="118" width="64" height="56" rx="10" fill="{G}" stroke="{T}" stroke-width="8"/><rect x="104" y="118" width="64" height="56" rx="10" fill="{HL}" stroke="{T}" stroke-width="8"/><rect x="66" y="54" width="64" height="56" rx="10" fill="#fff" stroke="{T}" stroke-width="8"/>')
COMPASS = SMALL.format(f'<circle cx="100" cy="100" r="74" fill="#fff" stroke="{T}" stroke-width="9"/><path d="M100 40 L116 100 L100 160 L84 100 Z" fill="{G}" stroke="{T}" stroke-width="6"/><circle cx="100" cy="100" r="9" fill="{T}"/>')

def ic_print(t, spark):    # a fingerprint draws itself: results that carry YOUR style
    out = ""
    for k, r in enumerate((14, 30, 46, 62, 78)):
        col = T if k % 2 == 0 else TL
        out += d(f"M{100 - r} {150 - k * 4} V110 A{r} {r} 0 0 1 {100 + r} 110 V{140 + k * 6}", t + k * 0.28, col, 7)
    stars = "".join(f'<path data-pop="{spark + k * 0.15}" d="M{x} {y - 14} L{x + 4} {y - 4} L{x + 14} {y} L{x + 4} {y + 4} L{x} {y + 14} L{x - 4} {y + 4} L{x - 14} {y} L{x - 4} {y - 4} Z" fill="{G}"/>'
                    for k, (x, y) in enumerate(((176, 44), (24, 70), (180, 168))))
    return SVG.format(out + d("M100 150 V118", t + 1.4, T, 7) + stars)

def ic_prompt(t, typing, send):   # a prompt being written, then sent
    dots = "".join(f'<rect data-pop="{typing + k * 0.18}" x="{150 - k * 18}" y="94" width="12" height="12" rx="3" fill="{TL}"/>' for k in range(6))
    return SVG.format(f'''
        {d("M24 76 H176 Q194 76 194 100 Q194 124 176 124 H24 Q6 124 6 100 Q6 76 24 76 Z", t, fill="#fff")}{dots}
        <g data-pop="{send}"><circle cx="34" cy="100" r="16" fill="{G}"/><path d="M26 100 H42 M34 92 L26 100 L34 108" stroke="var(--ink)" stroke-width="4"/></g>
        <path data-pop="{t + 0.4}" d="M100 22 L106 40 L124 46 L106 52 L100 70 L94 52 L76 46 L94 40 Z" fill="{G}" stroke="{T}" stroke-width="4"/>''')

def ic_pen(t):             # useful content being written
    lines = "".join(d(f"M64 {y} H{x}", t + 0.4 + k * 0.35, TL, 6) for k, (y, x) in enumerate(((70, 140), (94, 140), (118, 124), (142, 134))))
    return SVG.format(f'''
        {d("M44 26 H156 V178 H44 Z", t, fill="#fff")}{lines}
        <g data-rise="{t + 0.2}"><path d="M150 132 L176 106 L188 118 L162 144 L146 148 Z" fill="{G}" stroke="{T}" stroke-width="5"/></g>''')

def carousel(t, s1, s2):   # cards that swipe
    cards = ""
    for k, col in enumerate((G, HL, TL)):
        x = 40 + k * 130
        cards += (f'<rect x="{x}" y="36" width="120" height="120" rx="16" fill="#fff" stroke="{T}" stroke-width="5"/>'
                  f'<rect x="{x + 16}" y="52" width="88" height="44" rx="8" fill="{col}"/><path d="M{x + 18} {x * 0 + 116} H{x + 100} M{x + 18} {x * 0 + 134} H{x + 74}" stroke="{TL}" stroke-width="6"/>')
    dots = "".join(f'<circle cx="{88 + k * 12}" cy="182" r="5" fill="#d7dfe1"/>' for k in range(3))
    act = f'<circle data-pop="{t + 0.3}" cx="112" cy="182" r="6" fill="{T}"/><circle data-pop="{s1 + 0.3}" cx="100" cy="182" r="6" fill="{T}"/><circle data-pop="{s2 + 0.3}" cx="88" cy="182" r="6" fill="{T}"/>'
    return SVG.format(f'''<defs><clipPath id="cv"><rect x="34" y="28" width="132" height="136"/></clipPath></defs>
        <g clip-path="url(#cv)"><g data-pop="{t}"><g data-slide="{s1},{s2},-130">{cards}</g></g></g>{dots}{act}''')

def ic_clap(t, snap, play):   # short videos: the clapper snaps, the film plays
    return SVG.format(f'''
        {d("M26 84 H174 V176 H26 Z", t, fill="#fff")}
        <g data-rot="{snap},-24,26,80"><path d="M26 54 L170 54 L174 80 L26 80 Z" fill="var(--ink)"/>
          <path d="M50 54 L62 80 M86 54 L98 80 M122 54 L134 80" stroke="#fff" stroke-width="7"/></g>
        <path data-pop="{play}" d="M86 106 L120 128 L86 150 Z" fill="{G}" stroke="{T}" stroke-width="4"/>
        <rect x="26" y="186" width="148" height="6" rx="3" fill="#d7dfe1"/><rect data-grow="{play},1.4" x="26" y="186" width="148" height="6" rx="3" fill="{T}"/>''')

def ic_slide(t, redo):     # a slide built from scratch, then redesigned
    return SVG.format(f'''
        {d("M14 34 H186 V156 H14 Z", t, fill="#fff")}{d("M100 156 V176 M72 182 H128", t + 0.2, T, 6)}
        <g data-out="{redo}">{d("M34 58 H120", t + 0.4, "#9aa1a4", 8)}{d("M34 84 H160 M34 104 H150 M34 124 H140", t + 0.6, "#c4cacc", 6)}</g>
        <g data-pop="{redo + 0.15}"><rect x="30" y="50" width="70" height="88" rx="10" fill="{G}"/><path d="M112 62 H170" stroke="{T}" stroke-width="10"/>
          <path d="M112 88 H166 M112 106 H156 M112 124 H162" stroke="{TL}" stroke-width="6"/></g>
        <g data-pop="{redo - 0.25}"><circle cx="170" cy="34" r="20" fill="{T}"/><path d="M160 34 A10 10 0 1 1 170 44 M160 34 L156 28 M160 34 L166 30" stroke="#fff" stroke-width="4"/></g>''')

def ic_key(t, skills):     # a method = a key that keeps opening new skills
    return SVG.format(f'''
        <g data-swing="{t + 0.9}">{d("M100 112 m-30 0 a30 30 0 1 0 60 0 a30 30 0 1 0 -60 0", t, T, 8)}
          {d("M100 82 V24 M100 40 H120 M100 58 H114", t + 0.3, T, 8)}<circle cx="100" cy="112" r="10" fill="{G}"/></g>
        <rect data-pop="{skills}" x="16" y="150" width="40" height="40" rx="10" fill="{G}"/>
        <rect data-pop="{skills + 0.2}" x="80" y="160" width="40" height="40" rx="10" fill="{HL}" stroke="{T}" stroke-width="4"/>
        <rect data-pop="{skills + 0.4}" x="144" y="150" width="40" height="40" rx="10" fill="{TL}"/>''')

def tap(t):                # a finger taps the button, ripples spread
    return SVG.format(f'''
        <circle data-ring="{t}" cx="70" cy="60" r="40" stroke="{G}" stroke-width="6"/>
        <g data-pop="{t - 0.3}"><path d="M70 60 V150 Q70 172 92 176 H130 Q152 172 156 150 V110 Q156 98 144 98 Q132 98 132 110 V104 Q132 92 120 92 Q108 92 108 104 V100 Q108 88 96 88 Q86 88 86 98 V60 Q86 46 78 46 Q70 46 70 60 Z" fill="#fff" stroke="var(--ink)" stroke-width="6"/></g>''')

S = []
# 1 — مزدوجة: محتوى ينتظر
S.append(scene(1, 0,
  icon(250, 330, ic_note(0.0, 2.68)) +
  c(660, 80, 600, kl("هل لديك محتوى كتبتَه", "0.0,0.20,0.44,0.80"), 0.0) +
  c(780, 80, 600, kl(f'منذ فترة، {A("ولم تنشره")}', "1.14,1.32,1.70,1.92"), 1.0) +
  c(920, 64, 500, kl("لأنه لا وقتَ لديك للتصميم؟", "2.68,2.86,3.20,3.30,3.40"), 2.55)))
# 2 — نصّية: بأسلوبك وهويتك
S.append(scene(2, 3.86,
  c(470, 76, 500, kl("هل تودّ أن تصمّم", "3.92,4.16,4.40,4.54"), 3.8) +
  pill(610, 100, "كاروسيل", "4.96", 4.8) +
  c(790, 64, 500, kl("أو", "5.66"), 5.5) +
  pill(880, 100, "عرضًا تقديميًّا", "5.84,6.20", 5.7) +
  c(1080, 120, 700, kl("بأسلوبِك " + mark("وهويّتِك؟", 7.3), "6.56,7.06"), 6.4, "big", 1.3)))
# 3 — مزدوجة: نتائج متشابهة
S.append(scene(3, 7.52,
  icon(240, 400, ic_clones(7.6, 10.4)) +
  c(740, 76, 500, kl("لكنّ نتائجَ الذكاء الاصطناعي", "7.58,7.82,8.28,8.54"), 7.45) +
  c(870, 120, 700, kl(f'دائمًا {A("متشابهة")}', "9.48,10.38"), 9.3, "big", 1.2)))
# 4 — مزدوجة: فيديو مثل هذا
S.append(scene(4, 10.84,
  icon(230, 380, ic_phone(10.8, 11.6)) +
  c(700, 84, 600, kl(f'هل تودّ أن تصمّم {A("فيديو")}', "10.88,10.96,11.10,11.22,11.58"), 10.75) +
  c(830, 84, 600, kl("بنفسِ طريقةِ هذا الفيديو؟", "11.92,12.76,13.34,13.46"), 11.8)))
# 5 — نصّية: في هذه الدورة
S.append(scene(5, 14.02,
  c(660, 160, 700, kl(f'في هذه {A("الدورة")}', "14.08,14.32,14.46"), 13.95, "big", 1.2) +
  c(900, 96, 500, kl("سنتعلّم", "14.84"), 14.7)))
# 6 — مزدوجة: قائمة "كيف"
S.append(scene(6, 15.52,
  c(560, 84, 600, ri(THINK, 15.45) + kl("كيف نفكّر", "15.58,16.22", "inl"), 15.45) +
  c(760, 84, 600, ri(BLOCKS, 16.85) + kl("كيف نبني المهارات", "16.94,17.30,17.56", "inl"), 16.85) +
  c(960, 84, 600, ri(COMPASS, 18.05) + kl(f'كيف نوجّه {A("الذكاء الاصطناعي")}', "18.16,18.46,18.84,19.14", "inl"), 18.05)))
# 7 — رسم فقط: بصمتك
S.append(scene(7, 19.58,
  icon(470, 640, ic_print(19.6, 22.4))))
# 8 — مزدوجة: هندسة الأوامر
S.append(scene(8, 22.78,
  icon(330, 420, ic_prompt(22.75, 25.1, 25.9)) +
  c(820, 76, 500, kl("سنتعلّم أساسيات الذكاء الاصطناعي", "22.82,23.60,24.34,24.70"), 22.7) +
  pill(960, 96, "وهندسةَ الأوامر", "25.08,25.46", 24.95)))
# 9 — مزدوجة: المحتوى النافع
S.append(scene(9, 26.02,
  icon(260, 360, ic_pen(26.0)) +
  c(720, 80, 500, kl("كيف نصنع", "26.06,26.52"), 25.95) +
  c(840, 130, 700, kl(f'المحتوى {A("النافع")}', "27.60,28.26"), 27.45, "big", 1.2)))
# 10 — مزدوجة: الكاروسيل الدعوي
S.append(scene(10, 29.22,
  icon(260, 400, carousel(29.2, 29.9, 30.5)) +
  c(740, 80, 500, kl("كيف نصنع", "29.26,29.54"), 29.15) +
  c(860, 120, 700, kl(f'الكاروسيل {A("الدعوي")}', "29.82,30.44"), 29.7, "big", 1.2)))
# 11 — رسم فقط: الفيديوهات القصيرة
S.append(scene(11, 31.44,
  icon(500, 600, ic_clap(31.4, 31.75, 32.3))))
# 12 — مزدوجة: عرض من الصفر أو إعادة تصميم
S.append(scene(12, 33.40,
  icon(250, 400, ic_slide(33.4, 35.94)) +
  c(720, 76, 500, kl(f'كيف نصمّم {A("عرضًا تقديميًّا")}', "33.44,33.78,34.14,34.50"), 33.35) +
  c(830, 76, 500, kl("من الصفر", "34.90,35.40"), 34.75) +
  pill(970, 76, "أو نعيد تصميم عرضٍ موجود", "35.80,35.94,36.44,36.92,37.58", 35.65)))
# 13 — نصّية: الأهم
S.append(scene(13, 38.50,
  c(720, 170, 700, kl(f'{A("الأهمّ")}', "38.54"), 38.4, "big", 1.2) +
  c(960, 96, 600, kl("من كلّ ذلك", "39.04,39.20,39.38"), 38.95)))
# 14 — مزدوجة: منهجية
S.append(scene(14, 39.58,
  icon(220, 330, ic_key(39.55, 42.86)) +
  c(620, 84, 600, kl("سنتعلّم " + mark("منهجيّةً", 40.6), "39.62,40.16"), 39.5) +
  c(740, 68, 500, kl("نستطيع استخدامها مستقبلًا", "40.66,40.90,41.44"), 40.5) +
  c(840, 68, 500, kl(f'في اكتساب {A("مهاراتٍ جديدة")}', "42.06,42.24,42.86,43.32"), 41.9) +
  c(970, 60, 500, kl("وليس فقط المهارات", "43.70,43.82,43.98"), 43.55) +
  c(1060, 60, 500, kl("التي نتعلّمها في الدورة", "44.36,44.50,45.02,45.14"), 44.2)))
# 15 — دعوة: سجّل اهتمامك (+ أيقونة المشاركة)
S.append(scene(15, 45.50,
  c(470, 80, 600, kl("يشرّفني وجودُك", "45.54,45.98"), 45.45) +
  c(580, 80, 600, kl("في هذه الدورة", "46.38,46.46,46.60"), 46.25) +
  pill(740, 110, "سجّل اهتمامك", "47.06,47.44", 46.9) +
  icon(860, 220, tap(47.6), "tapper") +
  c(1110, 64, 500, kl("وبإذن الله أوافيك بالتفاصيل", "48.06,48.36,48.44,48.92"), 47.9) +
  c(1200, 64, 500, kl(f'في {A("أقرب وقت")}', "49.64,49.76,50.10"), 49.5) +
  '      <svg id="send" viewBox="0 0 48 48" fill="none" stroke="var(--ink)" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round">'
  '<path d="M43 5 L5 19 L21 27 L29 43 Z"/><path d="M43 5 L21 27"/></svg>\n'))

HTML = r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>إعلان الدورة — نهاري</title>
<!-- ستوري «إعلان الدورة» بالقالب النهاري بدون مربعات، بلا عنوان ولا ترقيم. يُولَّد من tools/build.py -->
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
  .glass { position: absolute; left: 50px; right: 50px; border-radius: 48px; background: var(--card); padding: 58px 40px 44px; text-align: center;
           box-shadow: 0 2px 0 rgba(30, 60, 70, .05), 0 14px 0 -4px var(--card-edge), 0 30px 60px var(--card-shadow); }
  .glass .gl { display: block; white-space: nowrap; }
  .pillrow { position: absolute; left: 0; right: 0; text-align: center; }
  .pill { display: inline-block; padding: 14px 48px 22px; border-radius: 999px; font-weight: 600; white-space: nowrap; background: var(--teal); color: #fff; }
  .pill.ghost { background: transparent; color: var(--muted); border: 4px dashed var(--teal-line); position: relative; }
  .strike { position: absolute; left: 30px; right: 30px; top: 52%; height: 8px; border-radius: 8px; background: #d9534f; transform: scaleX(0); transform-origin: 100% 50%; }
  .cardref { margin-top: 26px; font-size: 44px; font-weight: 500; color: var(--muted); }
  .cardref span { display: inline-block; }
  .refchip { position: absolute; left: 0; right: 0; text-align: center; font-size: 40px; color: var(--muted); }
  .icon { position: absolute; left: 50%; }
  .icon svg, .mini svg { width: 100%; height: 100%; overflow: visible; }
  .mini { position: absolute; border-radius: 40px; background: #fff; padding: 18px;
          box-shadow: 0 10px 0 -4px var(--card-edge), 0 24px 50px var(--card-shadow); }
  .line.inl { display: inline-block; }
  .ri { display: inline-block; width: 1.25em; height: 1.25em; vertical-align: -0.32em; margin-left: 0.35em; }
  .ri svg { width: 100%; height: 100%; overflow: visible; }
  #send { position: absolute; left: 110px; top: 1330px; width: 96px; height: 96px; }
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
  $$('svg [data-draw]').forEach(p => tl.to(p, { strokeDashoffset: 0, duration: 0.7, ease: 'power2.inOut' }, +p.dataset.draw));
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

out = HTML.replace("__SCENES__", "".join(S)).replace("__END__", str(END)).replace("__SEND__", str(SEND))
open(f"{DIR}/index.html", "w", encoding="utf-8").write(out)
print("written", len(out), "END", END)
