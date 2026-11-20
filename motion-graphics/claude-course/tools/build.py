# Builds motion-graphics/claude-course/index.html — القالب النهاري بدون مربعات (template ٣), no title / no counter.
# Voice-first reel «تعلّم Claude في ٤ خطوات» (إعلان دورة أساسيات Claude). Times = audio/voice-clean.m4a. Transition: «مدّ ضوئي» (day variant), continuous with the speech.
# Declarative: data-t (spoken word times), data-in / data-fx (big|up|card|pill|chip), data-mark, data-strike,
# icon attributes: data-draw, data-pop, data-rise, data-wave, data-fill, data-beat, data-shoot, data-tilt, data-drip, data-swing.
import json, math
ROOT = "/home/user/Design-course"
DIR = f"{ROOT}/motion-graphics/claude-course"
END = round(json.load(open(f"{DIR}/audio/timing.json"))["duration"] + 2.4, 2)
SEND = 50.45

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
SMALL = '<svg viewBox="0 0 200 200" fill="none" stroke-linecap="round" stroke-linejoin="round">{}</svg>'
def ri(svg, at):
    return f'<span class="ri" data-pop="{at}">{svg}</span>'
def chip(top, fs, svg, text, t, at, cls=""):
    return (f'      <div class="pillrow" style="top:{top}px;font-size:{fs}px" data-in="{at}" data-fx="pill">'
            f'<span class="pill chip {cls}">{ri(svg, at + 0.15)}<span class="kline inl" data-t="{t}">{text}</span></span></div>\n')

def steps(k, at):          # 4-step progress track at the top; step k fills now
    out = '      <div class="track">'
    for i in range(1, 5):
        cls = "done" if i < k else ("now" if i == k else "")
        g = f' data-grow="{at},0.6"' if i == k else ""
        out += f'<i class="{cls}"><b{g}></b></i>'
    return out + f'<span class="stepno">الخطوة {"١٢٣٤"[k - 1]}</span></div>\n'

# ---------------------------------------------------------------- illustrations
def ic_found(t):           # the basics: a foundation built block by block
    rows = [(150, (30, 76, 122)), (110, (53, 99)), (70, (76,))]
    out, k = "", 0
    for y, xs in rows:
        for x in xs:
            col = (G, HL, TL, "#fff", G, HL)[k]
            out += f'<rect data-pop="{t + k * 0.16}" x="{x}" y="{y}" width="44" height="38" rx="8" fill="{col}" stroke="{T}" stroke-width="5"/>'
            k += 1
    return SVG.format(d("M14 192 H186", t - 0.1, T, 8) + out)

CLAUDE_ORANGE = "#d97757"
def spark(cx, cy, R):      # the Claude spark (drawn approximation): tapered rays of uneven length
    out = ""
    for k in range(12):
        a = math.radians(k * 30 + (7 if k % 3 == 0 else -4))
        L = R * (1.0 if k % 2 == 0 else 0.78) * (0.92 if k % 3 == 1 else 1)
        w = R * 0.11
        px, py = -math.sin(a) * w, math.cos(a) * w
        x1, y1 = cx + math.cos(a) * R * 0.12, cy + math.sin(a) * R * 0.12
        x2, y2 = cx + math.cos(a) * L, cy + math.sin(a) * L
        out += f'<path d="M{x1 + px:.1f} {y1 + py:.1f} L{x2:.1f} {y2:.1f} L{x1 - px:.1f} {y1 - py:.1f} Z" fill="{CLAUDE_ORANGE}"/>'
    return out + f'<circle cx="{cx}" cy="{cy}" r="{R * 0.16:.1f}" fill="{CLAUDE_ORANGE}"/>'

def ic_tools(t, open_):    # capabilities: Claude at the centre, its abilities orbit around it
    sats = [
        ("<path d='M-9 9 L5 -5 L9 -1 L-5 13 Z M-9 9 L-11 15 L-5 13' fill='#b5dc55' stroke='#1b7a9c' stroke-width='2.5'/>"),   # writing
        ("<rect x='-12' y='-10' width='24' height='20' rx='3' fill='#fff' stroke='#1b7a9c' stroke-width='2.5'/><path d='M-10 8 L-2 -1 L4 5 L7 2 L11 8 Z' fill='#4a93b0'/><circle cx='5' cy='-4' r='3' fill='#b5dc55'/>"),  # images
        ("<rect x='-11' y='0' width='6' height='10' fill='#4a93b0'/><rect x='-3' y='-6' width='6' height='16' fill='#b5dc55'/><rect x='5' y='-11' width='6' height='21' fill='#1b7a9c'/>"),  # charts
        ("<path d='M-6 -8 L-13 0 L-6 8 M6 -8 L13 0 L6 8 M3 -11 L-3 11' stroke='#1b7a9c' stroke-width='3' fill='none'/>"),  # code
        ("<path d='M-6 -10 L11 0 L-6 10 Z' fill='#b5dc55' stroke='#1b7a9c' stroke-width='2.5'/>"),  # video
    ]
    out = f'<circle data-pop="{t}" cx="100" cy="100" r="74" stroke="#dfe5e7" stroke-width="3" stroke-dasharray="3 7"/>'
    for k, g in enumerate(sats):
        a = math.radians(-90 + k * 72); x, y = 100 + 74 * math.cos(a), 100 + 74 * math.sin(a)
        out += d(f"M{100 + 34 * math.cos(a):.1f} {100 + 34 * math.sin(a):.1f} L{100 + 56 * math.cos(a):.1f} {100 + 56 * math.sin(a):.1f}", open_ + k * 0.12, TL, 3)
        out += (f'<g data-pop="{open_ + 0.1 + k * 0.12}"><rect x="{x - 19:.1f}" y="{y - 19:.1f}" width="38" height="38" rx="10" fill="#fff" stroke="{T}" stroke-width="3"/>'
                f'<g transform="translate({x:.1f} {y:.1f})">{g}</g></g>')
    core = (f'<g data-pop="{t + 0.1}"><circle cx="100" cy="100" r="32" fill="#fff" stroke="#f0d9cf" stroke-width="4"/>'
            f'<g data-spin="{t + 0.3},6,90">{spark(100, 100, 24)}</g></g>')
    return SVG.format(out + core)

def ic_door(t, open_):     # a wide field for creativity: a door swings open onto light
    rays = "".join(f'<path data-pop="{open_ + 0.15 + k * 0.08}" d="M100 110 L{100 + 90 * c:.0f} {110 + 90 * s:.0f}" stroke="{G}" stroke-width="7"/>'
                   for k, (c, s) in enumerate(((-1, -0.2), (-0.8, -0.7), (-0.3, -1), (0.3, -1), (0.8, -0.7), (1, -0.2))))
    stars = "".join(f'<path data-pop="{open_ + 0.5 + k * 0.12}" d="M{x} {y - 10} L{x + 3} {y - 3} L{x + 10} {y} L{x + 3} {y + 3} L{x} {y + 10} L{x - 3} {y + 3} L{x - 10} {y} L{x - 3} {y - 3} Z" fill="{T}"/>'
                    for k, (x, y) in enumerate(((40, 40), (164, 52), (28, 120), (176, 130))))
    return SVG.format(f'''{rays}
        <rect x="66" y="56" width="68" height="124" rx="6" fill="{HL}"/>
        <g data-sx="{open_},0.18,66,118"><rect x="66" y="56" width="68" height="124" rx="6" fill="#fff" stroke="{T}" stroke-width="6"/>
          <circle cx="122" cy="122" r="5" fill="{T}"/></g>
        {d("M58 48 H142 V184 H58 Z", t, T, 7)}{d("M40 186 H160", t + 0.2, T, 7)}{stars}''')

MONT = SMALL.format(f'<rect x="16" y="40" width="168" height="120" rx="12" fill="#fff" stroke="{T}" stroke-width="9"/><path d="M16 70 H184 M16 130 H184" stroke="{T}" stroke-width="7"/><path d="M40 40 V70 M76 40 V70 M112 40 V70 M148 40 V70 M40 130 V160 M76 130 V160 M112 130 V160 M148 130 V160" stroke="{T}" stroke-width="6"/><path d="M86 84 L116 100 L86 116 Z" fill="{G}"/>')
PAL = SMALL.format(f'<path d="M100 26 Q30 26 30 96 Q30 170 92 172 Q112 172 106 150 Q100 132 122 132 H150 Q174 132 174 104 Q174 26 100 26 Z" fill="#fff" stroke="{T}" stroke-width="9"/><circle cx="70" cy="84" r="13" fill="{G}"/><circle cx="106" cy="62" r="13" fill="{TL}"/><circle cx="142" cy="88" r="13" fill="{HL}" stroke="{T}" stroke-width="4"/>')
SUMM = SMALL.format(f'<path d="M36 40 H164 M36 76 H164 M36 112 H120" stroke="{TL}" stroke-width="12"/><path d="M60 150 H140 M100 130 V170" stroke="{T}" stroke-width="0"/><rect x="36" y="140" width="128" height="34" rx="10" fill="{G}"/>')
DECK = SMALL.format(f'<rect x="20" y="30" width="160" height="110" rx="12" fill="#fff" stroke="{T}" stroke-width="9"/><rect x="40" y="88" width="20" height="34" fill="{TL}"/><rect x="72" y="66" width="20" height="56" fill="{G}"/><rect x="104" y="50" width="20" height="72" fill="{T}"/><path d="M100 140 V170 M70 176 H130" stroke="{T}" stroke-width="9"/>')

def ic_wand(t, wow):       # wow: a wand sweeps and the screen fills with sparkle
    stars = "".join(f'<path data-pop="{wow + k * 0.1}" d="M{x} {y - s} L{x + s * 0.3:.0f} {y - s * 0.3:.0f} L{x + s} {y} L{x + s * 0.3:.0f} {y + s * 0.3:.0f} L{x} {y + s} L{x - s * 0.3:.0f} {y + s * 0.3:.0f} L{x - s} {y} L{x - s * 0.3:.0f} {y - s * 0.3:.0f} Z" fill="{col}"/>'
                    for k, (x, y, s, col) in enumerate(((150, 40, 22, G), (182, 92, 12, TL), (112, 22, 10, T), (176, 152, 14, HL), (128, 80, 9, G))))
    return SVG.format(f'''<g data-rot="{t + 0.2},-30,40,170"><path d="M40 170 L132 78" stroke="var(--ink)" stroke-width="14"/>
        <path d="M116 94 L132 78" stroke="{G}" stroke-width="14"/></g>{stars}''')

def ic_cycle(t, done):     # edit → feedback → edit… until it becomes your template
    return SVG.format(f'''
        {d("M100 22 A78 78 0 0 1 178 100", t, TL, 8)}{d("M100 178 A78 78 0 0 1 22 100", t + 0.2, TL, 8)}
        <path data-pop="{t + 0.5}" d="M170 82 L178 100 L190 86" stroke="{TL}" stroke-width="8"/><path data-pop="{t + 0.6}" d="M30 118 L22 100 L10 114" stroke="{TL}" stroke-width="8"/>
        <g data-swing="{t + 1.2}"><rect x="58" y="54" width="84" height="96" rx="10" fill="#fff" stroke="{T}" stroke-width="6"/>
          <path d="M72 76 H128 M72 94 H120 M72 112 H126" stroke="#c4cacc" stroke-width="6"/>
          <path data-draw="{t + 1.0}" class="draw" d="M70 84 Q90 70 110 86 T132 80" stroke="#d9534f" stroke-width="5"/>
          <path data-draw="{t + 1.6}" class="draw" d="M120 120 L132 112" stroke="#d9534f" stroke-width="5"/></g>
        <g data-pop="{done}"><rect x="58" y="54" width="84" height="96" rx="10" fill="{G}" stroke="{T}" stroke-width="6"/>
          <path d="M80 102 L96 118 L124 86" stroke="#fff" stroke-width="10"/></g>''')

def ic_motion(t):          # motion graphics: preview window + keyframed timeline + moving playhead
    kf = lambda x, y, at, col: f'<path data-pop="{at}" d="M{x} {y - 7} L{x + 7} {y} L{x} {y + 7} L{x - 7} {y} Z" fill="{col}" stroke="{T}" stroke-width="2.5"/>'
    return SVG.format(f'''
        {d("M14 10 H186 V104 H14 Z", t, fill="#fff")}
        <path data-pop="{t + 0.3}" d="M40 84 C70 84 70 36 104 40 S150 70 164 30" stroke="{TL}" stroke-width="3" stroke-dasharray="5 7"/>
        <g data-move="{t + 0.6},2.2,124,-50,62,-46"><circle cx="40" cy="84" r="13" fill="{G}" stroke="{T}" stroke-width="4"/></g>
        <rect data-pop="{t + 0.25}" x="138" y="70" width="34" height="24" rx="5" fill="{HL}" stroke="{T}" stroke-width="3"/>
        {d("M14 116 H186 V190 H14 Z", t + 0.15, T, 6)}
        <path d="M26 136 H174 M26 156 H174 M26 176 H174" stroke="#e3e8ea" stroke-width="10"/>
        <rect data-grow="{t + 0.4},0.5" x="40" y="131" width="96" height="10" rx="5" fill="{G}"/>
        <rect data-grow="{t + 0.55},0.5" x="70" y="151" width="90" height="10" rx="5" fill="{TL}"/>
        <rect data-grow="{t + 0.7},0.5" x="30" y="171" width="64" height="10" rx="5" fill="{HL}"/>
        {kf(40, 136, t + 0.9, "#fff")}{kf(136, 136, t + 1.0, G)}{kf(70, 156, t + 1.1, "#fff")}{kf(160, 156, t + 1.2, G)}{kf(94, 176, t + 1.3, "#fff")}
        <g data-move="{t + 0.6},2.2,140,0"><path d="M26 112 V194" stroke="#d9534f" stroke-width="4"/><path d="M20 108 H32 L26 116 Z" fill="#d9534f"/></g>''')

def ic_board(t, build):    # presentations: a deck fans out, the front slide builds itself
    back = lambda ang, col, at: (f'<g data-pop="{at}"><g transform="rotate({ang} 100 96)"><rect x="26" y="40" width="148" height="100" rx="10" fill="{col}" stroke="{T}" stroke-width="3"/></g></g>')
    return SVG.format(f'''
        {back(-15, "#eef3f4", t)}{back(11, HL, t + 0.12)}
        <g data-pop="{t + 0.25}"><rect x="22" y="34" width="156" height="108" rx="10" fill="#fff" stroke="{T}" stroke-width="4"/></g>
        <rect data-grow="{build},0.45" x="40" y="50" width="78" height="12" rx="4" fill="{T}"/>
        {d("M40 76 H100 M40 90 H94 M40 104 H98", build + 0.2, TL, 5)}
        <circle cx="146" cy="96" r="20" stroke="#e3e8ea" stroke-width="9"/>
        <circle class="draw" data-draw="{build + 0.35}" cx="146" cy="96" r="20" stroke="{G}" stroke-width="9"/>
        <rect data-pop="{build + 0.5}" x="40" y="118" width="12" height="12" rx="3" fill="{G}"/><rect data-pop="{build + 0.6}" x="58" y="118" width="12" height="12" rx="3" fill="{TL}"/>
        <g data-pop="{build + 0.3}"><circle cx="88" cy="158" r="4" fill="{T}"/><circle cx="100" cy="158" r="4" fill="#d7dfe1"/><circle cx="112" cy="158" r="4" fill="#d7dfe1"/></g>
        <g data-move="{build + 0.9},0.7,-38,-46"><path data-pop="{build + 0.8}" d="M150 170 L150 196 L157 189 L162 200 L167 198 L162 187 L172 187 Z" fill="#fff" stroke="var(--ink)" stroke-width="3"/></g>''')

def ic_puzzle(t, join):    # building skills with Claude: two pieces click together
    P = "M20 60 H70 Q70 40 86 40 Q102 40 102 60 H120 V100 Q140 100 140 116 Q140 132 120 132 V172 H20 Z"
    return SVG.format(f'''
        <g data-rise="{t}"><path d="{P}" fill="{G}" stroke="{T}" stroke-width="7"/></g>
        <g data-slidein="{join}"><path d="M120 100 Q140 100 140 116 Q140 132 120 132 V172 H184 V60 H120 Z" transform="translate(4 0)" fill="{HL}" stroke="{T}" stroke-width="7"/></g>''')

def ic_journey(t, go):     # a straight line across the width: «no experience» (right) → «experience» (left)
    lab = lambda x, txt, col, w: f'<text x="{x}" y="124" text-anchor="middle" font-size="9" font-weight="{w}" fill="{col}" font-family="Plex Ar">{txt}</text>'
    arrive = t + 0.75
    return SVG.format(f'''
        <path data-pop="{t}" d="M186 100 H14" stroke="#dfe5e7" stroke-width="2.4" stroke-dasharray="0.5 5"/>
        <path class="draw" data-draw="{t + 0.05}" d="M186 100 H14" stroke="{T}" stroke-width="2.4"/>
        <g data-pop="{t}"><circle cx="186" cy="100" r="6.5" fill="#fff" stroke="#9aa1a4" stroke-width="2.4"/></g>
        <g data-pop="{t + 0.05}">{lab(186, "بلا تجربة", "#7b8386", 500)}</g>
        <g data-pop="{t + 0.1}"><circle cx="14" cy="100" r="6.5" fill="#fff" stroke="{T}" stroke-width="2.4"/></g>
        <circle data-ring="{go}" opacity="0" cx="14" cy="100" r="10" stroke="{G}" stroke-width="2.4"/>
        <g data-pop="{arrive}"><circle cx="14" cy="100" r="6.5" fill="{G}" stroke="{T}" stroke-width="2.4"/><path d="M11 100 L13.3 102.4 L17.4 97.6" stroke="#fff" stroke-width="1.8"/></g>
        <g data-pop="{arrive + 0.1}">{lab(14, "بالتجربة", "#1b7a9c", 700)}</g>
        <g data-out="{arrive - 0.05}"><g data-move="{t + 0.08},0.65,-172,0"><circle data-pop="{t + 0.05}" cx="186" cy="100" r="3.6" fill="{T}"/></g></g>''')

def ic_devices(t, no, tab, ph):   # no laptop needed — the tablet or the phone is enough
    return SVG.format(f'''
        <g data-out="{tab - 0.2}">{d("M40 40 H160 V112 H40 Z", t, fill="#fff")}{d("M20 120 H180 L170 132 H30 Z", t + 0.2, T, 6)}
          <path data-draw="{no}" class="draw" d="M30 30 L170 140" stroke="#d9534f" stroke-width="10"/></g>
        <g data-pop="{tab}"><rect x="28" y="54" width="96" height="128" rx="14" fill="#fff" stroke="{T}" stroke-width="7"/><rect x="40" y="68" width="72" height="96" rx="6" fill="{HL}"/><circle cx="76" cy="172" r="4" fill="{T}"/></g>
        <g data-pop="{ph}"><rect x="134" y="84" width="50" height="98" rx="10" fill="#fff" stroke="{T}" stroke-width="7"/><rect x="142" y="96" width="34" height="68" rx="4" fill="{G}"/></g>''')

def ic_pin(t):             # in person
    return SVG.format(f'''<g data-rise="{t}"><path d="M100 186 Q40 116 40 80 A60 60 0 1 1 160 80 Q160 116 100 186 Z" fill="{G}" stroke="{T}" stroke-width="7"/>
        <circle cx="100" cy="80" r="22" fill="#fff" stroke="{T}" stroke-width="6"/></g>''')

def tap(t):
    return SVG.format(f'''
        <circle data-ring="{t}" cx="70" cy="60" r="40" stroke="{G}" stroke-width="6"/>
        <g data-pop="{t - 0.3}"><path d="M70 60 V150 Q70 172 92 176 H130 Q152 172 156 150 V110 Q156 98 144 98 Q132 98 132 110 V104 Q132 92 120 92 Q108 92 108 104 V100 Q108 88 96 88 Q86 88 86 98 V60 Q86 46 78 46 Q70 46 70 60 Z" fill="#fff" stroke="var(--ink)" stroke-width="6"/></g>''')

def carousel(t, s1, s2):   # a seamless carousel: three connected slides, one line runs through them, the frame swipes along
    W, Y, H = 60, 62, 76
    xs = (134, 74, 14)                                   # RTL: the first slide is on the right
    slides = "".join(f'<g data-pop="{t + k * 0.15}"><rect x="{x}" y="{Y}" width="{W}" height="{H}" fill="{("#fff", "#f4f8f1", "#fff")[k]}" stroke="#d7dfe1" stroke-width="1.5"/></g>'
                     for k, x in enumerate(xs))
    content = f'''
        <rect data-grow="{t + 0.5},0.4" x="146" y="74" width="36" height="7" rx="3" fill="{T}"/>
        <path data-pop="{t + 0.6}" d="M146 88 H178 M146 96 H170" stroke="{TL}" stroke-width="3"/>
        <g data-pop="{t + 0.4}"><rect x="146" y="104" width="36" height="24" rx="4" fill="{HL}"/><path d="M148 126 L158 114 L165 121 L170 116 L180 126 Z" fill="{TL}"/></g>
        <circle cx="104" cy="96" r="13" stroke="#e3e8ea" stroke-width="6"/>
        <circle class="draw" data-draw="{s1}" cx="104" cy="96" r="13" stroke="{G}" stroke-width="6"/>
        <path data-pop="{s1 + 0.2}" d="M86 124 H122" stroke="{TL}" stroke-width="3"/>
        <rect data-pop="{s2 + 0.1}" x="22" y="112" width="44" height="14" rx="7" fill="{G}"/>
        <path data-pop="{s2}" d="M24 76 H58 M24 86 H50" stroke="{TL}" stroke-width="3"/>'''
    wave = f'<path class="draw" data-draw="{t + 0.3}" d="M194 120 C170 150 150 90 124 112 S90 150 64 108 S30 80 14 100" stroke="{G}" stroke-width="3.5"/>'
    frame = (f'<g data-pop="{t + 0.2}"><g data-move="{s1 - 0.3},0.45,-60,0"><g data-move="{s2 - 0.3},0.45,-60,0">'
             f'<rect x="130" y="56" width="68" height="88" rx="8" stroke="var(--ink)" stroke-width="3.5"/>'
             f'<rect x="152" y="51" width="24" height="5" rx="2.5" fill="var(--ink)"/></g></g></g>')
    dots = "".join(f'<circle cx="{112 - k * 12}" cy="162" r="3.5" fill="#d7dfe1"/>' for k in range(3))
    act = f'<g data-pop="{t + 0.3}"><g data-move="{s1 - 0.3},0.45,-12,0"><g data-move="{s2 - 0.3},0.45,-12,0"><rect x="106" y="158.5" width="12" height="7" rx="3.5" fill="{T}"/></g></g></g>'
    return SVG.format(slides + content + frame + dots + act)


S = []
# 1 — نصّية: أفضل طريقة لتعلّم Claude … ٤ خطوات
S.append(scene(1, 0,
  c(330, 76, 500, kl("أفضل طريقة لتعلّم", "0.0,0.36,0.88"), 0.0) +
  c(440, 150, 700, kl(A("Claude"), "1.56"), 1.4, "big", 1.2) +
  pill(660, 56, "حسب تجربتي", "1.86,2.12", 1.75, "soft") +
  c(760, 560, 700, kl(A("٤"), "3.18"), 3.0, "big", 1.0) +
  c(1260, 110, 700, kl("خطوات", "3.54"), 3.4, "big", 1.2)))
# 2 — الخطوة ١: الأساسيات
S.append(scene(2, 3.86,
  steps(1, 3.9) +
  icon(470, 360, ic_found(3.9)) +
  c(900, 84, 500, kl("معرفة", "3.9"), 3.8) +
  c(1010, 140, 700, kl(A("الأساسيات"), "4.32"), 4.15, "big", 1.2)))
# 3 — الخطوة ٢: القدرات والإمكانات
S.append(scene(3, 5.48,
  steps(2, 5.52) +
  icon(400, 470, ic_tools(5.45, 6.0)) +
  c(880, 84, 600, kl(f'معرفة {A("القدرات والإمكانات")}', "5.52,5.88,6.34"), 5.4) +
  c(1000, 68, 500, kl("التي يقدّمها لك هذا التطبيق", "6.9,7.3,7.62,7.82,8.06"), 6.75)))
# 4 — رسم: باب يُفتح على الإبداع
S.append(scene(4, 8.5,
  icon(420, 560, ic_door(8.5, 9.0)) +
  c(1060, 72, 500, kl(f'تفتح لك {A("مجالًا واسعًا")} للإبداع', "8.72,8.96,9.16,9.36,9.8"), 8.6)))
# 5 — الخطوة ٣: نصّية «التجربة» ×٣
S.append(scene(5, 10.26,
  steps(3, 10.3) +
  c(470, 84, 500, kl('<span class="mute">التجربة</span>', "10.30"), 10.2) +
  c(590, 56, 500, kl('<span class="mute">ثمّ</span>', "10.98"), 10.85) +
  c(670, 120, 600, kl("التجربة", "11.20"), 11.05, "big", 1.2) +
  c(840, 56, 500, kl('<span class="mute">ثمّ</span>', "11.72"), 11.6) +
  c(920, 190, 700, kl(mark(A("التجربة"), 12.1), "11.94"), 11.8, "big", 1.2)))
# 6 — مزدوجة: جرّبه في
S.append(scene(6, 12.36,
  c(420, 96, 600, kl("جرّبه في:", "12.4,12.74"), 12.3) +
  chip(575, 76, MONT, "المونتاج", "12.82", 12.64) +
  chip(770, 76, PAL, "التصميم", "13.26", 13.1) +
  chip(965, 76, SUMM, "التلخيص", "13.72", 13.55) +
  chip(1160, 76, DECK, "العروض التقديمية", "14.38,14.58", 14.2)))
# 7 — مزدوجة: ستنبهر
S.append(scene(7, 14.98,
  icon(400, 400, ic_wand(14.9, 15.3)) +
  c(860, 160, 700, kl(A("ستنبهر"), "15.02"), 14.9, "big", 1.2) +
  c(1080, 84, 500, kl("بالنتائج الأوليّة", "15.44,15.9"), 15.3)))
# 8 — نصّية: ثم الخطوة الأهم
S.append(scene(8, 16.26,
  c(560, 96, 500, kl("ثمّ", "16.3"), 16.2) +
  c(690, 130, 700, kl("الخطوة", "16.8"), 16.65, "big", 1.2) +
  c(860, 230, 700, kl(mark(A("الأهمّ"), 17.4), "17.14"), 17.0, "big", 1.1)))
# 9 — الخطوة ٤: التعديل حتى القالب
S.append(scene(9, 17.5,
  steps(4, 17.54) +
  icon(430, 380, ic_cycle(17.5, 20.66)) +
  c(860, 84, 600, kl(f'التعديل والملاحظات {A("المستمرّة")}', "17.54,18.82,19.4"), 17.4) +
  c(990, 68, 500, kl("حتى تصل إلى " + mark("القوالب", 20.8), "19.94,20.24,20.52,20.66"), 19.8) +
  c(1090, 68, 500, kl("التي تعتمدها لمشاريعك", "21.06,21.42,21.86"), 20.9)))
# 10 — مزدوجة: دورة أساسيات Claude
S.append(scene(10, 22.48,
  c(440, 72, 500, kl("وهذا بالضبط ما سنتعلّمه في", "22.52,22.82,23.16,23.26,23.7"), 22.4) +
  card(600, 23.6, '<div style="font-size:64px;font-weight:500;color:var(--muted)">' + kl("دورة", "23.8") + '</div>'
       + '<div style="font-size:120px;font-weight:700;line-height:1.3">' + kl(f'أساسيات {A("Claude")}', "24.36,24.96") + '</div>') +
  c(1030, 72, 500, kl("تتعلّم فيها الأساسيات", "25.28,25.58,25.76"), 25.15)))
# 11 — مزدوجة: المشروع النهائي = كاروسيل
S.append(scene(11, 26.22,
  pill(340, 60, "المشروع النهائي", "26.26,26.64", 26.15, "soft") +
  icon(400, 520, carousel(26.9, 28.94, 29.78)) +
  c(920, 84, 600, kl(f'أن نصمّم {A("كاروسيل")}', "28.26,28.6,28.94"), 28.15) +
  c(1040, 68, 500, kl("مثل الموجود في الحساب", "29.4,29.78,30.16,30.26"), 29.25)))
# 12 — مزدوجة: فيديو مثل هذا (هاتف داخل هاتف)
S.append(scene(12, 30.5,
  icon(300, 520, ic_motion(30.6)) +
  c(860, 92, 600, kl(f'وفيديو {A("موشن جرافيك")}', "30.54,30.88,31.22"), 30.45) +
  c(990, 68, 500, kl("تمامًا مثل الفيديو الذي تشاهده الآن", "31.9,32.36,32.56,32.84,33.1,33.4"), 31.75)))
# 13 — مزدوجة: عروض تقديمية
S.append(scene(13, 33.68,
  icon(380, 440, ic_board(33.7, 34.3)) +
  c(860, 72, 500, kl("ومن خلال هذه التطبيقات", "33.72,34.02,34.28,34.42"), 33.6) +
  c(970, 92, 600, kl(f'تستطيع صنع {A("عروضٍ تقديميّة")}', "35.12,35.34,35.54,35.76"), 35.0)))
# 14 — مزدوجة: تبني المهارات مع Claude
S.append(scene(14, 36.12,
  icon(400, 360, ic_puzzle(36.1, 37.4)) +
  c(820, 72, 500, kl("ستتعلّم كيف تبني", "36.16,36.56,36.74"), 36.05) +
  c(930, 110, 700, kl(f'المهارات مع {A("Claude")}', "37.0,37.44,37.58"), 36.9, "big", 1.2)))
# 15 — نصّية: لمن هذه الدورة (سحابة شارات)
S.append(scene(15, 37.84,
  c(420, 96, 600, kl("سواء كنتَ", "37.88,38.16"), 37.8) +
  pill(590, 72, "معلّم", "38.42", 38.3) +
  pill(750, 72, "صانع محتوى", "38.76,39.06", 38.65, "soft") +
  pill(910, 72, "طالب", "39.7", 39.55) +
  pill(1070, 72, "مدرّب", "40.06", 39.95, "soft")))
# 16 — رسم + كلمة: انطلاقة
S.append(scene(16, 41.1,
  icon(80, 960, ic_journey(41.05, 42.2)) +
  c(860, 72, 500, kl("وبإذن الله، هذه الدورة", "41.14,41.44,41.54,41.8"), 41.05) +
  c(980, 108, 700, kl(f'ستكون {A("انطلاقةً")} لك', "42.02,42.26,42.7"), 41.9, "big", 1.2)))
# 17 — مزدوجة: لا لابتوب — يكفي الآيباد أو الجوال
S.append(scene(17, 42.84,
  icon(380, 420, ic_devices(42.8, 43.5, 44.73, 45.42)) +
  c(860, 76, 600, kl("لن تحتاج إلى لابتوب للتطبيق العملي", "42.88,42.96,43.2,43.4,43.66,44.16"), 42.75) +
  c(990, 110, 700, kl(f'يكفيك {A("الآيباد")} أو الجوال', "44.5,44.73,45.4,45.54"), 44.4, "big", 1.2)))
# 18 — دعوة: حضوريًّا + سجّل اهتمامك (+ أيقونة المشاركة)
S.append(scene(18, 46.02,
  icon(300, 200, ic_pin(46.02)) +
  c(530, 76, 600, kl(f'الدورة ستكون {A("حضوريّة")}', "46.06,46.54,47.18"), 45.97) +
  pill(690, 110, "سجّل اهتمامك", "47.52,47.86", 47.37) +
  icon(810, 200, tap(48.02)) +
  c(1050, 68, 500, kl("من الرابط في البايو", "48.36,48.42,48.46"), 48.22) +
  c(1150, 68, 500, kl(f'لتصلك التفاصيل {A("قريبًا")}', "48.94,49.32,49.96"), 48.82) +
  '      <svg id="send" viewBox="0 0 48 48" fill="none" stroke="var(--ink)" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round">'
  '<path d="M43 5 L5 19 L21 27 L29 43 Z"/><path d="M43 5 L21 27"/></svg>\n'))

HTML = r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>تعلّم Claude — نهاري</title>
<!-- ريل «تعلّم Claude في ٤ خطوات» بالقالب النهاري بدون مربعات، بلا عنوان ولا ترقيم. يُولَّد من tools/build.py -->
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
  .mute { color: var(--muted); }
  .pill.soft { background: var(--hl); color: var(--ink); }
  .pill.chip { background: #fff; color: var(--ink); box-shadow: 0 10px 0 -4px var(--card-edge), 0 24px 50px var(--card-shadow); padding: 18px 44px 26px 52px; }
  .track { position: absolute; left: 0; right: 0; top: 280px; display: flex; justify-content: center; gap: 14px; direction: rtl; }
  .track i { position: relative; width: 150px; height: 14px; border-radius: 7px; background: #dfe5e7; overflow: hidden; }
  .track i.done { background: var(--teal); }
  .track i b { position: absolute; inset: 0; border-radius: 7px; background: var(--green); transform: scaleX(0); transform-origin: 100% 50%; }
  .track i.now b { display: block; }
  .stepno { position: absolute; top: 34px; left: 0; right: 0; text-align: center; font-size: 44px; font-weight: 600; color: var(--teal); }
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
