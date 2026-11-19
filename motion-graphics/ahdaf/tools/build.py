# Builds motion-graphics/ahdaf/index.html — القالب النهاري بدون مربعات (template ٣), no title / no counter.
# Voice-first reel «الأهداف». Times = audio/voice-clean.m4a. Transition: «مدّ ضوئي» (day variant), continuous with the speech.
# Declarative: data-t (spoken word times), data-in / data-fx (big|up|card|pill|chip), data-mark, data-strike,
# icon attributes: data-draw, data-pop, data-rise, data-wave, data-fill, data-beat, data-shoot, data-tilt, data-drip, data-swing.
import json
ROOT = "/home/user/Design-course"
DIR = f"{ROOT}/motion-graphics/ahdaf"
END = round(json.load(open(f"{DIR}/audio/timing.json"))["duration"] + 2.4, 2)
SEND = 82.75

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
def card(top, at, inner):
    return f'      <div class="glass" style="top:{top}px" data-in="{at}" data-fx="card">{inner}</div>\n'
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

def ic_calendar(t, a, b, cc):   # day, month, year: three cells light up as each is spoken
    cells = "".join(f'<rect x="{x}" y="{y}" width="22" height="22" rx="6" fill="#d7dfe1"/>'
                    for y in (100, 134) for x in (48, 78, 108, 138))
    return SVG.format(f'''
        {d("M30 60 Q30 46 44 46 H156 Q170 46 170 60 V162 Q170 176 156 176 H44 Q30 176 30 162 Z", t, fill="var(--bg)")}
        {d("M30 82 H170", t + 0.25)}{d("M70 32 V58", t + 0.3, w=8)}{d("M130 32 V58", t + 0.3, w=8)}
        <g data-pop="{t + 0.5}">{cells}</g>
        <rect data-pop="{a}" x="48" y="100" width="22" height="22" rx="6" fill="{G}"/>
        <rect data-pop="{b}" x="45" y="131" width="118" height="28" rx="9" fill="{G}"/>
        <rect data-pop="{cc}" x="42" y="94" width="124" height="68" rx="12" fill="none" stroke="{T}" stroke-width="5"/>''')

def ic_bulb(t, lit):
    B = "M100 30 C66 30 44 56 44 86 C44 108 56 122 70 134 C76 140 78 146 78 154 H122 C122 146 124 140 130 134 C144 122 156 108 156 86 C156 56 134 30 100 30 Z"
    return SVG.format(f'''
        <path data-fill="{lit}" fill="{G}" fill-opacity="0" d="{B}"/>
        {d(B, t)}{d("M84 168 H116", t + 0.3)}{d("M90 182 H110", t + 0.4)}
        {d("M90 154 V120 Q100 108 110 120 V154", t + 0.45, TL, 5)}
        <g data-pop="{lit + 0.2}" stroke="{G}" stroke-width="7"><path d="M100 14 V2"/><path d="M40 30 L30 20"/><path d="M160 30 L170 20"/><path d="M22 86 H8"/><path d="M178 86 H192"/></g>''')

def ic_target(t, hit):
    return SVG.format(f'''
        <circle class="draw" data-draw="{t}" cx="96" cy="104" r="74" stroke="{T}" stroke-width="7"/>
        <circle class="draw" data-draw="{t + 0.15}" cx="96" cy="104" r="48" stroke="{TL}" stroke-width="6"/>
        <circle data-fill="{hit}" cx="96" cy="104" r="22" fill="{G}" fill-opacity="0" stroke="{T}" stroke-width="6"/>
        <g data-shoot="{hit - 0.4}" stroke="var(--ink)" stroke-width="7">
          <path d="M98 102 L176 24"/><path d="M176 24 H196 M176 24 V4"/><path d="M162 38 H182 M162 38 V18"/></g>''')

def ic_mihrab(t, a, b):
    return SVG.format(f'''
        {d("M40 178 V96 Q40 38 100 26 Q160 38 160 96 V178", t)}
        {d("M66 178 V108 Q66 70 100 58 Q134 70 134 108 V178", t + 0.2, TL, 5)}
        {d("M24 178 H176", t - 0.05)}
        {d("M100 58 V84", t + 0.4, TL, 4)}
        <path data-pop="{a}" d="M86 86 H114 L108 108 Q100 116 92 108 Z" fill="{G}" stroke="{T}" stroke-width="5"/>
        <g data-pop="{b}" stroke="{G}" stroke-width="5"><path d="M100 126 V140"/><path d="M80 118 L72 128"/><path d="M120 118 L128 128"/></g>''')

def ic_books(t, a, b, cc):
    def book(y, x, w, col, at):
        return (f'<g data-pop="{at}"><rect x="{x}" y="{y}" width="{w}" height="30" rx="7" fill="var(--bg)" stroke="{col}" stroke-width="6"/>'
                f'<path d="M{x + 22} {y} V{y + 30}" stroke="{col}" stroke-width="5"/><path d="M{x + 40} {y + 15} H{x + w - 18}" stroke="{col}" stroke-width="4"/></g>')
    return SVG.format(f'''
        {d("M14 176 H186", t)}
        {book(140, 28, 144, T, a)}{book(104, 40, 124, TL, b)}{book(68, 50, 104, T, cc)}
        <g data-pop="{cc + 0.6}" stroke="{G}" stroke-width="7"><path d="M100 50 V20"/><path d="M86 34 L100 20 L114 34"/></g>''')

def ic_network(t, grow, big):
    main = [(100, 100, 40, 50), (100, 100, 160, 50), (100, 100, 34, 140), (100, 100, 166, 140), (100, 100, 100, 176)]
    sub = [(40, 50, 14, 20), (40, 50, 64, 14), (160, 50, 186, 20), (160, 50, 136, 14), (34, 140, 8, 170), (166, 140, 192, 170)]
    out = "".join(d(f"M{x1} {y1} L{x2} {y2}", t + k * 0.1, TL, 5) for k, (x1, y1, x2, y2) in enumerate(main))
    out += "".join(d(f"M{x1} {y1} L{x2} {y2}", grow + k * 0.12, TL, 4) for k, (x1, y1, x2, y2) in enumerate(sub))
    out += "".join(f'<circle data-pop="{t + 0.3 + k * 0.1}" cx="{x2}" cy="{y2}" r="12" fill="var(--bg)" stroke="{T}" stroke-width="5"/>' for k, (_, _, x2, y2) in enumerate(main))
    out += "".join(f'<circle data-pop="{big + k * 0.08}" cx="{x2}" cy="{y2}" r="9" fill="{G}"/>' for k, (_, _, x2, y2) in enumerate(sub))
    return SVG.format(out + f'<circle data-pop="{t}" cx="100" cy="100" r="18" fill="{T}"/>')

def ic_pie(t, w, silly):
    sl = [("M100 104 L100 34 A70 70 0 0 1 170 104 Z", TL), ("M100 104 L170 104 A70 70 0 0 1 100 174 Z", G), ("M100 104 L100 174 A70 70 0 0 1 30 104 Z", "#d2ee94")]
    out = "".join(f'<path data-pop="{w + k * 0.35}" d="{p}" fill="{col}"/>' for k, (p, col) in enumerate(sl))
    return SVG.format(f'''<g data-swing="{silly}">
        {out}
        <circle class="draw" data-draw="{t}" cx="100" cy="104" r="70" stroke="{T}" stroke-width="7"/>
        {d("M100 104 V54", t + 0.4, "var(--ink)", 6)}{d("M100 104 L132 120", t + 0.5, "var(--ink)", 6)}</g>''')

def ic_funnel(t, a):
    dots = [(48, 24, TL), (82, 14, G), (118, 22, T), (152, 12, "#d2ee94")]
    out = "".join(f'<circle data-pop="{t + 0.3 + k * 0.1}" cx="{x}" cy="{y}" r="11" fill="{col}"/>' for k, (x, y, col) in enumerate(dots))
    return SVG.format(f'''
        {d("M24 44 H176 L118 112 V166 L82 184 V112 Z", t, fill="var(--bg)")}
        {out}<circle data-pop="{a}" cx="100" cy="140" r="11" fill="{G}"/>''')

def ic_lantern(t, lit):
    body = "M70 58 H130 L122 150 H78 Z"
    return SVG.format(f'''
        <path data-fill="{lit}" fill="{G}" fill-opacity="0" d="{body}"/>
        <circle class="draw" data-draw="{t}" cx="100" cy="22" r="9" stroke="{T}" stroke-width="6"/>
        {d("M78 58 L88 36 H112 L122 58 Z", t + 0.1, fill="var(--bg)")}
        {d(body, t + 0.25)}{d("M100 58 V150", t + 0.45, TL, 4)}{d("M74 104 H126", t + 0.5, TL, 4)}
        {d("M84 150 H116 L108 172 H92 Z", t + 0.55)}
        <g data-pop="{lit + 0.2}" stroke="{G}" stroke-width="7"><path d="M40 104 H22"/><path d="M160 104 H178"/><path d="M50 60 L38 48"/><path d="M150 60 L162 48"/><path d="M52 150 L40 162"/><path d="M148 150 L160 162"/></g>''')

def ic_cup(t, drip, full):
    cup = "M48 74 H152 L140 166 Q138 178 126 178 H74 Q62 178 60 166 Z"
    drops = "".join(f'<path d="M{x} 6 Q{x + 9} 20 {x + 9} 26 A9 9 0 0 1 {x - 9} 26 Q{x - 9} 20 {x} 6 Z" fill="{TL}"/>' for x in (100, 86, 114))
    return SVG.format(f'''
        <g data-drip="{drip}">{drops}</g>
        <path data-fill="{full}" d="M56 112 H144 L140 166 Q138 174 126 174 H74 Q62 174 60 166 Z" fill="{G}" fill-opacity="0"/>
        {d(cup, t)}{d("M152 96 Q178 96 178 120 Q178 144 146 146", t + 0.3, T, 6)}''')

def ic_scale(t, level):
    pan = lambda x: (f'<path d="M{x} 62 L{x - 18} 112 M{x} 62 L{x + 18} 112" stroke="{TL}" stroke-width="4"/>'
                     f'<path d="M{x - 26} 112 H{x + 26} Q{x} 136 {x - 26} 112 Z" fill="var(--bg)" stroke="{T}" stroke-width="6"/>')
    return SVG.format(f'''
        {d("M100 46 V170", t)}{d("M64 176 H136", t + 0.1)}
        <circle data-pop="{t + 0.2}" cx="100" cy="40" r="10" fill="{G}"/>
        <g data-tilt="{t + 0.4},{level}">{d("M34 62 H166", t + 0.3)}{pan(34)}{pan(166)}</g>''')

def ic_book(t):    # the open mushaf (same as earlier reels)
    return SVG.format(f'''
        {d("M100 74 C80 62 52 60 26 66 V154 C52 148 80 150 100 162 C120 150 148 148 174 154 V66 C148 60 120 62 100 74 Z", t, fill="var(--bg)")}
        {d("M100 74 V162", t + 0.25, w=5)}
        <g stroke="{TL}" stroke-width="4">
          {d("M86 94 C70 86 54 85 40 88", t + 0.4, TL, 4)}{d("M86 112 C70 104 54 103 40 106", t + 0.47, TL, 4)}
          {d("M114 94 C130 86 146 85 160 88", t + 0.4, TL, 4)}{d("M114 112 C130 104 146 103 160 106", t + 0.47, TL, 4)}</g>
        <g stroke="{G}" stroke-width="6" data-pop="{t + 0.7}"><path d="M100 48 V30"/><path d="M74 54 L64 40"/><path d="M126 54 L136 40"/></g>''')

def ic_peak(t, flag):
    return SVG.format(f'''
        {d("M14 176 L76 72 L106 118 L128 92 L186 176 Z", t, fill="var(--bg)")}
        {d("M60 100 L76 112 L92 98", t + 0.4, TL, 5)}
        {d("M76 72 V22", flag - 0.3, "var(--ink)", 6)}
        <path data-pop="{flag}" d="M78 24 L120 36 L78 50 Z" fill="{G}" stroke="{T}" stroke-width="4"/>''')

def ic_check(t, a, b, cc):
    rows = ""
    for k, (y, at) in enumerate(((76, a), (112, b), (148, cc))):
        rows += f'<rect x="58" y="{y}" width="24" height="24" rx="6" stroke="{TL}" stroke-width="5"/>'
        rows += d(f"M96 {y + 12} H144", t + 0.4 + k * 0.1, TL, 5)
        rows += d(f"M60 {y + 10} L70 {y + 22} L90 {y - 4}", at, G, 8)
    return SVG.format(f'''
        {d("M48 40 Q40 40 40 50 V176 Q40 186 50 186 H150 Q160 186 160 176 V50 Q160 40 152 40", t, fill="var(--bg)")}
        <rect data-pop="{t + 0.25}" x="76" y="28" width="48" height="24" rx="8" fill="{T}"/>
        {rows}''')

def ic_juggle(t, swing):   # many goals at once: three balls teetering on one tray
    return SVG.format(f'''
        {d("M100 132 V176", t)}{d("M66 178 H134", t + 0.1)}
        <g data-swing="{swing}">{d("M24 130 H176", t + 0.2, T, 8)}
          <circle data-pop="{t + 0.3}" cx="52" cy="106" r="20" fill="{TL}"/>
          <circle data-pop="{t + 0.45}" cx="100" cy="106" r="20" fill="{G}"/>
          <circle data-pop="{t + 0.6}" cx="148" cy="106" r="20" fill="#d2ee94" stroke="{T}" stroke-width="5"/>
          <circle data-pop="{t + 0.75}" cx="76" cy="66" r="18" fill="{T}"/>
          <circle data-pop="{t + 0.9}" cx="124" cy="66" r="18" fill="{TL}"/></g>''')

S = []
# 1 — قبل أن تخطط ليومك أو لشهرك أو حتى لسنتك
S.append(scene(1, 0,
  icon(250, 360, ic_calendar(0.0, 0.92, 1.52, 2.48)) +
  c(700, 84, 500, kl("قبل أن تخطّطَ", "0.0,0.24,0.36"), 0.0) +
  c(830, 104, 700, kl(f'ليومِك، أو {A("لشهرِك")}،', "0.92,1.36,1.52"), 0.75) +
  c(970, 104, 700, kl(f'أو حتى {A("لسنتِك")}', "2.02,2.18,2.48"), 1.9)))
# 2 — ضع في بالك أمورًا أهم
S.append(scene(2, 3.48,
  icon(250, 360, ic_bulb(3.45, 4.58)) +
  c(700, 84, 500, kl("ضعْ في بالِك", "3.54,3.66,3.72"), 3.4) +
  c(820, 170, 700, kl(f'أمورًا {A("أهمَّ")}', "4.08,4.58"), 3.95, "big", 1.2) +
  c(1050, 84, 500, kl("من هذه الأشياء", "5.00,5.16,5.36"), 4.9)))
# 3 — الأهداف ... وأهمها رضا الله
S.append(scene(3, 5.72,
  icon(190, 330, ic_target(5.68, 10.75)) +
  c(570, 96, 600, kl(f'وهي {A("الأهداف")}', "5.76,6.02"), 5.6) +
  c(710, 68, 500, kl("التي تسعى إليها، ومطالبُك", "6.70,6.99,7.37,7.57"), 6.55) +
  c(810, 68, 500, kl("التي تتحرّك من أجلها", "8.19,8.40,8.87,9.05"), 8.05) +
  c(940, 68, 500, kl("وأهمُّ شيءٍ في هذه المطالب", "9.45,9.67,9.83,9.91,10.11"), 9.3) +
  c(1050, 140, 700, kl(f'رضا {A("الله")}', "10.75,11.13"), 10.6, "big", 1.2) +
  c(1250, 68, 500, kl("عزّ وجلّ", "11.37,11.81"), 11.2)))
# 4 — أهداف تتعلق بعبادة رب العالمين: الفرائض ثم النوافل
S.append(scene(4, 12.12,
  icon(180, 290, ic_mihrab(12.08, 17.07, 18.13)) +
  c(530, 76, 500, kl("ولا بدّ أن تكون لدينا", "12.53,12.71,12.90,13.11,13.29"), 12.0) +
  c(640, 76, 500, kl("أهدافٌ تتعلّق بعبادة", "13.67,14.11,14.49"), 13.5) +
  c(750, 120, 700, kl(A("ربِّ العالمين"), "15.13,15.37"), 14.95, "big", 1.2) +
  c(920, 76, 500, kl("أولًا: نركّز على " + mark("الفرائض", 17.15), "16.03,16.49,16.97,17.07"), 15.9) +
  pill(1050, 76, "ثمّ النوافل", "17.69,18.13", 17.5)))
# 5 — أهداف أخرى: حفظ القرآن، علوم الشريعة... مطالب عالية
S.append(scene(5, 18.80,
  icon(170, 270, ic_books(18.75, 20.35, 21.33, 23.69)) +
  c(500, 72, 500, kl("ونضعُ لنا أهدافًا أخرى، مثلًا:", "18.85,19.07,19.25,19.65,19.95"), 18.7) +
  pill(620, 72, "حفظُ القرآن", "20.35,20.71", 20.2) +
  c(770, 72, 500, kl("أو دراسةُ ما تيسّر", "21.17,21.33,21.77,21.93"), 21.0) +
  c(870, 72, 500, kl(f'من {A("علوم الشريعة")}', "22.45,22.59,22.95"), 22.3) +
  c(970, 72, 500, kl("أو أيٍّ من العلوم النافعة", "23.43,23.69,23.95,24.21,24.69"), 23.3) +
  c(1110, 84, 700, kl("كلُّ هذه المطالب " + mark("مطالبُ عالية", 26.5), "25.11,25.32,25.46,26.04,26.42"), 24.95)))
# 6 — الأهداف الشخصية: كبير ومتشعب
S.append(scene(6, 26.90,
  icon(190, 300, ic_network(26.88, 30.16, 32.32)) +
  c(570, 84, 600, kl(f'ولكلٍّ منّا أهدافٌ {A("شخصيّة")}', "27.51,27.69,27.97,28.75"), 26.8) +
  c(710, 68, 500, kl("والمهمّ: كلّما توسّعتَ في الأهداف", "29.30,29.82,30.16,30.58,30.72"), 29.15) +
  c(820, 68, 500, kl("ستكتشف أنّ الموضوع", "31.10,31.62,31.74"), 30.95) +
  c(950, 140, 700, kl(f'كبيرٌ {A("ومتشعّب")}', "32.32,32.91"), 32.15, "big", 1.2)))
# 7 — لا يكفي تقسيم غير واقعي
S.append(scene(7, 33.86,
  icon(230, 340, ic_pie(33.82, 35.29, 37.45)) +
  c(670, 84, 600, kl("ولا يكفي أن نقسّمَ يومَنا", "33.91,34.13,34.39,34.55,34.93"), 33.75) +
  c(800, 84, 500, kl("بتقسيمٍ فيه", "35.29,35.85"), 35.15) +
  c(930, 104, 700, kl(f'شيءٌ من {A("عدمِ الواقعيّة")}', "36.25,36.75,36.98,37.34"), 36.1, "big", 1.2)))
# 8 — أو تقتصر على نوع معين
S.append(scene(8, 37.97,
  icon(220, 320, ic_funnel(37.93, 39.50)) +
  c(620, 80, 500, kl("أو أن نقتصرَ على نوعٍ", "38.02,38.36,38.62,39.10,39.24"), 37.85) +
  c(740, 80, 600, kl(f'{A("معيّنٍ")} من الأهداف', "39.50,39.80,39.90"), 39.35) +
  pill(890, 72, "مثلَ التجارة", "40.30,40.60", 40.15) +
  pill(1020, 72, "أو القراءة", "41.20,41.36", 41.05) +
  c(1160, 68, 500, kl("أو غيرِها من الأهداف", "41.88,42.12,42.61,42.75"), 41.7)))
# 9 — كثير منا لا يستطيع الجمع على الوجه الأفضل
S.append(scene(9, 43.28,
  icon(220, 320, ic_juggle(43.24, 45.44)) +
  c(640, 84, 600, kl(f'وكثيرٌ منّا {A("لا يستطيع")}', "43.93,44.34,44.66,44.76"), 43.8) +
  c(770, 84, 500, kl("أن يجمع بين هذه الأمور", "45.02,45.44,46.11,46.69,47.15"), 44.9) +
  c(910, 96, 700, kl(f'على الوجهِ الأفضلِ {A("والأحسن")}', "47.20,47.30,47.39,48.01"), 47.05, "big", 1.2)))
# 10 — مبادئ نبوية
S.append(scene(10, 48.48,
  icon(180, 290, ic_lantern(48.44, 51.35)) +
  c(520, 80, 600, kl("لكنّ النبيَّ ﷺ", "48.53,48.93,49.43"), 48.4) +
  c(640, 104, 700, kl(f'علّمنا {A("مبادئَ")}', "50.45,51.35"), 50.3, "big", 1.2) +
  c(800, 68, 500, kl("إذا استمررنا عليها", "52.03,52.31,52.73"), 51.9) +
  c(905, 68, 500, kl("نستطيع أن نجمع بين", "53.05,53.20,53.39,53.75"), 52.9) +
  c(1020, 96, 700, kl("أكبرِ قدرٍ من الأهداف", "53.95,54.51,54.99,55.11"), 53.8) +
  c(1160, 130, 700, kl(A("والطموح"), "55.91"), 55.75, "big", 1.2)))
# 11 — أحب الأعمال إلى الله أدومها وإن قل
S.append(scene(11, 56.38,
  icon(170, 280, ic_cup(56.34, 59.04, 61.40)) +
  c(520, 76, 500, kl("ومن أبسطِ هذه المبادئ", "56.43,56.58,56.94,57.08"), 56.3) +
  c(630, 76, 600, kl("حديثُ النبيِّ ﷺ:", "57.56,57.86,58.12"), 57.4) +
  card(780, 58.75, '<div class="quote" style="font-size:84px;font-weight:600;line-height:1.55">'
       + kl("«أَحَبُّ الْأَعْمَالِ إِلَى اللَّهِ", "59.04,59.58,60.08,60.24", "gl")
       + kl(mark("أَدْوَمُهَا", 60.7) + " وَإِنْ قَلَّ»", "60.60,61.29,61.50", "gl") + '</div>') +
  ref(1150, "[متفق عليه]", 61.55)))
# 12 — اكلفوا من الأعمال ما تطيقون
S.append(scene(12, 61.94,
  icon(220, 330, ic_scale(61.9, 65.73)) +
  c(650, 80, 600, kl("وكذلك قولُ النبيِّ ﷺ:", "61.99,62.39,62.67,62.95"), 61.85) +
  card(800, 63.65, '<div class="quote" style="font-size:96px;font-weight:600;line-height:1.55">'
       + kl("«اكْلَفُوا مِنَ الْأَعْمَالِ", "63.93,64.61,64.83", "gl")
       + kl(mark("مَا تُطِيقُونَ»", 65.8), "65.57,65.73", "gl") + '</div>') +
  ref(1170, "[رواه البخاري]", 65.85)))
# 13 — لا يكلف الله نفسًا إلا وسعها
S.append(scene(13, 66.38,
  icon(220, 320, ic_book(66.34)) +
  c(640, 80, 600, kl("وكذلك قولُ الله عزّ وجلّ:", "66.43,66.93,67.17,67.33,67.61"), 66.3) +
  card(790, 67.8, '<div class="quote" style="font-size:96px;font-weight:600;line-height:1.55">'
       + kl("﴿لَا يُكَلِّفُ اللَّهُ نَفْسًا", "68.05,68.31,69.07,69.27", "gl")
       + kl("إِلَّا " + mark("وُسْعَهَا﴾", 70.25), "69.97,70.19", "gl") + '</div>') +
  ref(1150, "[البقرة: ٢٨٦]", 70.3)))
# 14 — ليست للتخفيف فقط، بل في العزائم
S.append(scene(14, 70.68,
  icon(200, 300, ic_peak(70.64, 74.92)) +
  c(570, 76, 500, kl("قد يظنّ البعضُ أنّ هذه الآية", "70.73,71.03,71.31,71.61,71.71,71.97"), 70.6) +
  pill(690, 72, "للتخفيف", "72.45", 72.3, "ghost", strike=73.05) +
  c(850, 76, 500, kl("لكنّ هذه الآية", "73.03,73.22,73.52"), 72.9) +
  pill(970, 80, "تُؤخذ حتى في العزائم", "73.90,74.26,74.72,74.92", 73.75)))
# 15 — يعرف قدرته ويضع أهدافه وفقًا لذلك (+ share icon)
S.append(scene(15, 75.38,
  icon(190, 290, ic_check(75.34, 77.74, 79.77, 80.62)) +
  c(540, 72, 500, kl("وأنّ المرءَ لا بدّ أن يعرفَ", "75.42,75.98,76.38,76.54,76.74,77.04"), 75.3) +
  c(650, 72, 500, kl(f'مدى {A("قدرتِه")}، ومدى الإمكانات', "77.50,77.74,78.32,78.65"), 77.35) +
  c(760, 72, 500, kl("الموجودة عنده", "79.21,79.77"), 79.05) +
  c(890, 130, 700, kl(f'ويضعَ {A("أهدافَه")}', "80.09,80.62"), 79.95, "big", 1.2) +
  c(1100, 100, 600, kl(mark("وفقًا لذلك", 82.3), "81.42,82.16"), 81.25) +
  '      <svg id="send" viewBox="0 0 48 48" fill="none" stroke="var(--ink)" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round">'
  '<path d="M43 5 L5 19 L21 27 L29 43 Z"/><path d="M43 5 L21 27"/></svg>\n'))

HTML = r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>الأهداف — نهاري</title>
<!-- ريل «الأهداف» بالقالب النهاري بدون مربعات، بلا عنوان ولا ترقيم. يُولَّد من tools/build.py -->
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
  .pill.ghost { background: transparent; color: var(--muted); border: 4px dashed var(--teal-line); position: relative; }
  .strike { position: absolute; left: 30px; right: 30px; top: 52%; height: 8px; border-radius: 8px; background: #d9534f; transform: scaleX(0); transform-origin: 100% 50%; }
  .refchip { position: absolute; left: 0; right: 0; text-align: center; font-size: 40px; color: var(--muted); }
  .icon { position: absolute; left: 50%; }
  .icon svg, .mini svg { width: 100%; height: 100%; overflow: visible; }
  .mini { position: absolute; border-radius: 40px; background: #fff; padding: 18px;
          box-shadow: 0 10px 0 -4px var(--card-edge), 0 24px 50px var(--card-shadow); }
  #send { position: absolute; left: 110px; top: 1300px; width: 96px; height: 96px; }
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
      tl.fromTo(w, { opacity: 0.35, scaleY: 0.35, transformOrigin: '50% 100%' }, { opacity: 1, scaleY: 1, duration: 0.28, ease: 'sine.inOut', yoyo: true, repeat: 9 }, +g.dataset.wave + k * 0.09)));
  $$('.icon [data-fill]').forEach(p => tl.to(p, { attr: { 'fill-opacity': 0.9 }, duration: 0.7, ease: 'power2.out' }, +p.dataset.fill));
  $$('.icon').forEach(ic => { const r = ic.querySelector('[data-beat]'); if (r) {      // heartbeat once the heart is full
      const t = +r.dataset.beat;
      [0, 0.55].forEach(d => tl.to(ic, { keyframes: { scale: [1, 1.08, 1, 1.04, 1] }, duration: 0.45, ease: 'none' }, t + d)); } });
  if (document.getElementById('send'))                   // share icon flies in at the end
    tl.fromTo('#send', { x: -140, y: 140, opacity: 0, rotation: -25 }, { x: 0, y: 0, opacity: 1, rotation: 0, duration: 0.9, ease: 'expo.out' }, __SEND__)
      .to('#send', { x: 10, y: -10, duration: 0.45, ease: 'sine.inOut', yoyo: true, repeat: 1 }, __SEND__ + 0.9);

  $$('.icon [data-shoot]').forEach(g => tl.fromTo(g, { x: 110, y: -110, opacity: 0 }, { x: 0, y: 0, opacity: 1, duration: 0.4, ease: 'power4.in' }, +g.dataset.shoot)
      .to(g.closest('.icon'), { keyframes: { x: [0, -10, 6, 0] }, duration: 0.35, ease: 'none' }, +g.dataset.shoot + 0.4));
  $$('.icon [data-tilt]').forEach(g => { const [t, lv] = g.dataset.tilt.split(',').map(Number);
      gsap.set(g, { svgOrigin: '100 62' });
      tl.fromTo(g, { rotation: -16 }, { rotation: 12, duration: 1.0, ease: 'sine.inOut' }, t)
        .to(g, { rotation: -8, duration: 0.9, ease: 'sine.inOut' }, t + 1.0)
        .to(g, { rotation: 5, duration: 0.8, ease: 'sine.inOut' }, t + 1.9)
        .to(g, { rotation: 0, duration: 0.7, ease: 'back.out(2)' }, lv); });
  $$('.icon [data-drip]').forEach(g => [...g.children].forEach((w, k) =>
      tl.fromTo(w, { y: 0, opacity: 0 }, { keyframes: { y: [0, 40, 90], opacity: [0, 1, 0] }, duration: 0.7, ease: 'power1.in', repeat: 2, repeatDelay: 0.2 }, +g.dataset.drip + k * 0.3)));
  $$('.icon [data-swing]').forEach(g => { gsap.set(g, { svgOrigin: '100 104' });
      tl.to(g, { keyframes: { rotation: [0, -14, 10, -6, 3, 0] }, duration: 1.2, ease: 'none' }, +g.dataset.swing); });
  $$('[data-strike]').forEach(s => tl.to(s, { scaleX: 1, duration: 0.45, ease: 'power2.inOut' }, +s.dataset.strike)
      .to(s.closest('.pillrow'), { opacity: 0.45, duration: 0.4 }, +s.dataset.strike + 0.3));

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
