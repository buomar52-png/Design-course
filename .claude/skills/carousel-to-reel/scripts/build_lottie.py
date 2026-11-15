"""Build Lottie from <project>/output/bake.json (made by bake.js).

  python3 build_lottie.py <project-dir> [--scenes]

Outputs (in <project>/lottie/):
  <name>-reel.json        the whole reel, 1080x1920, every text converted to vector shapes
  <name>-scene-N.json     (--scenes) each scene as its own standalone Lottie

Text is shaped with HarfBuzz (Arabic joining + harakat) using the project's fonts/, so the
Lottie needs no fonts at playback. Requires: pip install uharfbuzz fonttools
"""
import json, math, re, os
from pathlib import Path
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen

import sys
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ".").resolve()
FONTS = ROOT / "fonts"
OUT = ROOT / "lottie"
R2 = lambda v: round(v, 2)

# ---------------------------------------------------------------- fonts
class Font:
    def __init__(self, weight):
        path = str(FONTS / f"IBMPlexSansArabic-{weight}.ttf")
        self.tt = TTFont(path)
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upem = self.tt["head"].unitsPerEm
        hh = self.tt["hhea"]
        self.asc, self.desc = hh.ascent, -hh.descent
        blob = hb.Blob.from_file_path(path)
        self.hbfont = hb.Font(hb.Face(blob))
        self.cache = {}

    def outline(self, gid):
        if gid not in self.cache:
            pen = LottiePen(self.gs)
            self.gs[self.order[gid]].draw(pen)
            self.cache[gid] = pen.contours
        return self.cache[gid]

class LottiePen(BasePen):
    """Collects contours as (vertices, in-tangents, out-tangents) in font units."""
    def __init__(self, gs):
        super().__init__(gs); self.contours = []; self.c = None
    def _moveTo(self, p):
        self.c = [[p], [(0, 0)], [(0, 0)]]; self.contours.append(self.c)
    def _lineTo(self, p):
        v, i, o = self.c; v.append(p); i.append((0, 0)); o.append((0, 0))
    def _curveToOne(self, c1, c2, p):
        v, i, o = self.c; p0 = v[-1]
        o[-1] = (c1[0] - p0[0], c1[1] - p0[1])
        v.append(p); i.append((c2[0] - p[0], c2[1] - p[1])); o.append((0, 0))
    def _qCurveToOne(self, q, p):
        p0 = self.c[0][-1]
        c1 = (p0[0] + 2 / 3 * (q[0] - p0[0]), p0[1] + 2 / 3 * (q[1] - p0[1]))
        c2 = (p[0] + 2 / 3 * (q[0] - p[0]), p[1] + 2 / 3 * (q[1] - p[1]))
        self._curveToOne(c1, c2, p)
    def _closePath(self):
        v, i, o = self.c
        if len(v) > 1 and abs(v[0][0] - v[-1][0]) < 1e-6 and abs(v[0][1] - v[-1][1]) < 1e-6:
            i[0] = i[-1]; v.pop(); i.pop(); o.pop()
    _endPath = _closePath

FONT = {}
def font(w):
    w = min((400, 500, 600, 700), key=lambda x: abs(x - w))
    if w not in FONT: FONT[w] = Font(w)
    return FONT[w]

def text_shapes(run):
    """Shape one text run and return Lottie 'sh' items placed in the run's local rect."""
    f = font(run["weight"]); size = run["size"]; s = size / f.upem
    buf = hb.Buffer(); buf.add_str(run["text"]); buf.guess_segment_properties()
    if buf.direction == "ltr" and not re.search(r"[A-Za-z0-9]", run["text"]):
        buf.direction = "rtl"   # neutral-only runs («, », ؛ …) sit in RTL context: mirror like the browser does
    hb.shape(f.hbfont, buf, {})
    infos, pos = buf.glyph_infos, buf.glyph_positions       # visual order (left -> right)
    width = sum(p.x_advance for p in pos) * s
    x0, y0, w, h = run["rect"]
    n_adv = sum(1 for p in pos if p.x_advance) or 1
    extra = (w - width) / n_adv                              # absorbs letter-spacing / rounding
    baseline = y0 + h * f.asc / (f.asc + f.desc)
    pen_x = x0
    items = []
    for info, p in zip(infos, pos):
        ox, oy = pen_x + p.x_offset * s, baseline - p.y_offset * s
        for v, ti, to in f.outline(info.codepoint):
            items.append({"ty": "sh", "ks": {"a": 0, "k": {
                "v": [[R2(ox + x * s), R2(oy - y * s)] for x, y in v],
                "i": [[R2(x * s), R2(-y * s)] for x, y in ti],
                "o": [[R2(x * s), R2(-y * s)] for x, y in to],
                "c": True}}})
        pen_x += p.x_advance * s + (extra if p.x_advance else 0)
    return items

# ---------------------------------------------------------------- lottie helpers
def static(v): return {"a": 0, "k": v}
def tr(): return {"ty": "tr", "p": static([0, 0]), "a": static([0, 0]), "s": static([100, 100]),
                  "r": static(0), "o": static(100), "sk": static(0), "sa": static(0)}
def fill(rgba, extra_alpha=1):
    return {"ty": "fl", "c": static([R2(c) for c in rgba[:3]] + [1]), "o": static(R2(rgba[3] * extra_alpha * 100)), "r": 1}
def group(items, name=""): return {"ty": "gr", "nm": name, "it": items + [tr()]}
def rect(x, y, w, h, r=0): return {"ty": "rc", "d": 1, "s": static([R2(w), R2(h)]), "p": static([R2(x + w / 2), R2(y + h / 2)]), "r": static(R2(r))}
def ellipse(x, y, w, h): return {"ty": "el", "d": 1, "s": static([R2(w), R2(h)]), "p": static([R2(x + w / 2), R2(y + h / 2)])}
def box_path(x0, y0, x1, y1):
    return {"v": [[R2(x0), R2(y0)], [R2(x1), R2(y0)], [R2(x1), R2(y1)], [R2(x0), R2(y1)]],
            "i": [[0, 0]] * 4, "o": [[0, 0]] * 4, "c": True}

def simplify(samples, tol):
    """Ramer-Douglas-Peucker over frames: indices to keep so linear interpolation stays within tol."""
    n = len(samples)
    if n < 3: return list(range(n))
    tol = tol if isinstance(tol, (list, tuple)) else [tol] * len(samples[0])
    keep = {0, n - 1}; stack = [(0, n - 1)]
    while stack:
        a, b = stack.pop()
        if b - a < 2: continue
        worst, wi = 0, -1
        for k in range(a + 1, b):
            t = (k - a) / (b - a)
            d = max(abs(samples[a][j] + (samples[b][j] - samples[a][j]) * t - samples[k][j]) / tol[j]
                    for j in range(len(tol)))
            if d > worst: worst, wi = d, k
        if worst > 1: keep.add(wi); stack += [(a, wi), (wi, b)]
    return sorted(keep)

def animated(samples, tol, wrap=lambda v: v, scalar=False):
    """samples: list of vectors (one per frame) -> Lottie property."""
    idx = simplify(samples, tol)
    val = lambda v: wrap([R2(x) for x in v]) if not scalar else R2(v[0])
    if len(idx) == 1:
        return static(val(samples[0]))
    if len(idx) == 2 and all(abs(a - b) < 1e-9 for a, b in zip(samples[0], samples[-1])) \
            and simplify(samples, tol) == [0, len(samples) - 1]:
        return static(val(samples[0]))
    k = []
    for n, f in enumerate(idx):
        kf = {"t": f, "s": val(samples[f]) if not scalar else [val(samples[f])]}
        if n < len(idx) - 1: kf.update({"o": {"x": [0], "y": [0]}, "i": {"x": [1], "y": [1]}})
        k.append(kf)
    return {"a": 1, "k": k}

def decompose(m):
    a, b, c, d, e, f = m
    return [e, f], math.degrees(math.atan2(b, a)), [math.hypot(a, b) * 100, math.hypot(c, d) * 100]

def transform_ks(frames_m, frames_o):
    P, R, S = zip(*[decompose(m) for m in frames_m])
    # keep rotation continuous
    R = list(R)
    for k in range(1, len(R)):
        while R[k] - R[k - 1] > 180: R[k] -= 360
        while R[k] - R[k - 1] < -180: R[k] += 360
    return {"a": static([0, 0, 0]),
            "p": animated([list(p) + [0] for p in P], [0.25, 0.25, 1]),
            "r": animated([[r] for r in R], 0.05, scalar=True),
            "s": animated([list(s) + [100] for s in S], [0.08, 0.08, 1]),
            "o": animated([[o * 100] for o in frames_o], 0.4, scalar=True)}

def shape_layer(ind, name, ks, shapes, op, masks=None, parent=None):
    L = {"ddd": 0, "ind": ind, "ty": 4, "nm": name, "sr": 1, "ks": ks, "ao": 0, "shapes": shapes,
         "ip": 0, "op": op, "st": 0, "bm": 0}
    if masks: L["hasMask"] = True; L["masksProperties"] = masks
    if parent: L["parent"] = parent
    return L

# ---------------------------------------------------------------- svg paths
def parse_path(d):
    toks = re.findall(r"[MLCZ]|-?\d*\.?\d+", d)
    contours, cur, i = [], None, 0
    while i < len(toks):
        t = toks[i]; i += 1
        if t == "M":
            cur = [[], [], []]; contours.append(cur)
            cur[0].append((float(toks[i]), float(toks[i + 1]))); cur[1].append((0, 0)); cur[2].append((0, 0)); i += 2
        elif t == "L":
            cur[0].append((float(toks[i]), float(toks[i + 1]))); cur[1].append((0, 0)); cur[2].append((0, 0)); i += 2
        elif t == "C":
            c1 = (float(toks[i]), float(toks[i + 1])); c2 = (float(toks[i + 2]), float(toks[i + 3])); p = (float(toks[i + 4]), float(toks[i + 5])); i += 6
            p0 = cur[0][-1]; cur[2][-1] = (c1[0] - p0[0], c1[1] - p0[1])
            cur[0].append(p); cur[1].append((c2[0] - p[0], c2[1] - p[1])); cur[2].append((0, 0))
        elif t == "Z":
            v, ii, o = cur
            if len(v) > 1 and v[0] == v[-1]: ii[0] = ii[-1]; v.pop(); ii.pop(); o.pop()
            cur.append(True)
    out = []
    for c in contours:
        out.append({"ty": "sh", "ks": static({"v": [[R2(x), R2(y)] for x, y in c[0]], "i": [[R2(x), R2(y)] for x, y in c[1]],
                                              "o": [[R2(x), R2(y)] for x, y in c[2]], "c": len(c) > 3})})
    return out

LC = {"butt": 1, "round": 2, "square": 3}; LJ = {"miter": 1, "round": 2, "bevel": 3}

# ---------------------------------------------------------------- unit -> shapes
def unit_shapes(u, frames_u, fps):
    """Return (shapes, masks) in the unit's local coordinates."""
    shapes, masks = [], None
    k = u["kind"]
    if k == "text":
        by_color = {}
        for run in u["runs"]:
            by_color.setdefault((tuple(run["color"])), []).extend(text_shapes(run))
        for col, items in by_color.items():
            shapes.append(group(items + [fill(list(col))], "text"))
        if u.get("whoDot"):
            x, y, w, h = u["rect"]
            shapes.append(group([ellipse(w - 2 - 18, h / 2 - 7, 18, 18), fill([0.71, 0.86, 0.33, 1])], "dot"))
        if u.get("hl"):
            hx, hy, hw, hh = u["hl"]["rect"]
            bar_h = hh * 0.40; bar_y = hy + (hh - bar_h) * 0.82; right = hx + hw
            pct = [fr.get("hl", 100) / 100 for fr in frames_u]
            size = animated([[hw * p, bar_h] for p in pct], [0.5, 0.5])
            posn = animated([[right - hw * p / 2, bar_y + bar_h / 2] for p in pct], [0.25, 0.25])
            shapes.append(group([{"ty": "rc", "d": 1, "s": size, "p": posn, "r": static(0)},
                                 fill([0.824, 0.933, 0.58, 1])], "highlight"))
        if any("clip" in fr for fr in frames_u):          # right-to-left reveal (clip-path inset)
            x, y, w, h = u["rect"]
            samples = [[w * (fr.get("clip") or 0) / 100] for fr in frames_u]
            idx = simplify(samples, 0.5)
            kf = []
            for n, f in enumerate(idx):
                e = {"t": f, "s": [box_path(samples[f][0], -0.4 * h, w + 4, 1.4 * h)]}
                if n < len(idx) - 1: e.update({"o": {"x": [0], "y": [0]}, "i": {"x": [1], "y": [1]}})
                kf.append(e)
            masks = [{"inv": False, "mode": "a", "nm": "reveal", "o": static(100), "x": static(0),
                      "pt": {"a": 1, "k": kf} if len(kf) > 1 else static(kf[0]["s"][0])}]
        if u.get("clipBox"):                                  # counter window (overflow: hidden)
            bx, by, bw, bh = u["clipBox"]
            samples = [[bx - fr["m"][4], by - fr["m"][5]] for fr in frames_u]
            idx = simplify(samples, [0.25, 0.25]); kf = []
            for n, f in enumerate(idx):
                lx, ly = samples[f]
                e = {"t": f, "s": [box_path(lx, ly, lx + bw, ly + bh)]}
                if n < len(idx) - 1: e.update({"o": {"x": [0], "y": [0]}, "i": {"x": [1], "y": [1]}})
                kf.append(e)
            masks = [{"inv": False, "mode": "a", "nm": "window", "o": static(100), "x": static(0), "pt": {"a": 1, "k": kf}}]
    elif k == "box":
        x, y, w, h = u["rect"]
        if u["id"] == "bg-grid":
            col = [40 / 255, 80 / 255, 95 / 255, 0.075]; items = []
            for gx in range(-8, 1081, 56): items.append(rect(gx, 0, 1.5, 1920))
            for gy in range(-8, 1921, 56): items.append(rect(0, gy, 1080, 1.5))
            shapes.append(group(items + [fill(col)], "grid"))
        elif u["id"] in ("bg-a", "bg-b"):
            if u["id"] == "bg-a": cx, cy, R, rgb, stops = w - 120, 120, 620, (140, 196, 220), [(0, .42), (260 / 620, .18), (1, 0)]
            else:                 cx, cy, R, rgb, stops = 120, h - 120, 640, (205, 232, 150), [(0, .45), (260 / 640, .20), (1, 0)]
            c = [v / 255 for v in rgb]
            g = [x for p, _ in stops for x in [R2(p)] + [R2(v) for v in c]] + [x for p, a in stops for x in (R2(p), a)]
            shapes.append(group([rect(0, 0, w, h), {"ty": "gf", "o": static(100), "r": 1, "t": 2,
                "s": static([R2(cx), R2(cy)]), "e": static([R2(cx + R), R2(cy)]),
                "g": {"p": len(stops), "k": static(g)}, "h": static(0), "a": static(0)}], u["id"]))
        elif u.get("isCard"):
            shapes.append(group([rect(0, 0, w, h, u["radius"]), fill([1, 1, 1, 1])], "card"))
            shapes.append(group([rect(4, 18, w - 8, h - 8, u["radius"] - 4), fill([215 / 255, 225 / 255, 228 / 255, .9])], "edge"))
            for k2, a in ((30, .035), (18, .03)):
                shapes.append(group([rect(-6, k2, w + 12, h, u["radius"] + 6), fill([30 / 255, 60 / 255, 70 / 255, a])], "shadow"))
        elif u["radiusIsCircle"]:
            shapes.append(group([ellipse(0, 0, w, h), fill(u["bg"])], "dot"))
        else:
            shapes.append(group([rect(0, 0, w, h, u["radius"]), fill(u["bg"])], "box"))
    else:  # svg
        items = [sh for d in u["d"] for sh in parse_path(d)]
        if u["stroke"]:
            st = {"ty": "st", "c": static([R2(c) for c in u["stroke"][:3]] + [1]), "o": static(R2(u["stroke"][3] * 100)),
                  "w": static(u["strokeWidth"]), "lc": LC.get(u["linecap"], 1), "lj": LJ.get(u["linejoin"], 1), "ml": 4}
            if u.get("dash"):
                st["d"] = [{"n": "d", "nm": "dash", "v": static(u["dash"][0])}, {"n": "g", "nm": "gap", "v": static(u["dash"][1])},
                           {"n": "o", "nm": "offset", "v": static(0)}]
            items.append(st)
        if u["fill"]: items.append(fill(u["fill"]))
        if u.get("draw"):
            L = u["length"]
            items.insert(1, {"ty": "tm", "s": static(0), "o": static(0), "m": 1,
                             "e": animated([[max(0, min(100, (1 - fr.get("dash", 0) / L) * 100))] for fr in frames_u], 0.1, scalar=True)})
        shapes.append(group(items, u["id"] or "svg"))
    return shapes, masks

def name_of(u):
    if u["kind"] == "text": return " ".join(r["text"].strip() for r in u["runs"])[:40]
    if u["kind"] == "svg" and not u["id"]: return "path"
    return u["id"] or u["cls"]

def stage_bg(op, w=1080, h=1920):
    return shape_layer(9999, "background", {"a": static([0, 0, 0]), "p": static([0, 0, 0]), "r": static(0),
                       "s": static([100, 100, 100]), "o": static(100)},
                       [group([rect(0, 0, w, h), fill([243 / 255, 245 / 255, 244 / 255, 1])], "bg")], op)

# ---------------------------------------------------------------- builds
def build_reel(bake, f0=0, f1=None, title="reel", markers=True):
    fps, units = bake["fps"], bake["units"]
    frames = bake["frames"][f0:f1]
    N = len(frames)
    layers = []
    for j, u in enumerate(units):
        fu = [fr[j] for fr in frames]
        if max(f["o"] for f in fu) < 0.004: continue
        shapes, masks = unit_shapes(u, fu, fps)
        layers.append(shape_layer(j + 1, name_of(u), transform_ks([f["m"] for f in fu], [f["o"] for f in fu]), shapes, N, masks))
    layers.reverse()  # Lottie: first layer is on top; DOM order paints bottom-up
    layers.append(stage_bg(N))
    mk = []
    sc = bake.get("scenes") or {}
    keys = sorted([k for k in sc if k != "end"], key=lambda k: sc[k])
    if markers:
        for n, k in enumerate(keys):
            end = sc[keys[n + 1]] if n + 1 < len(keys) else sc.get("end", bake["duration"])
            mk.append({"tm": round(sc[k] * fps), "cm": k, "dr": round((end - sc[k]) * fps)})
    return {"v": "5.7.4", "fr": fps, "ip": 0, "op": N - 1, "w": 1080, "h": 1920, "nm": title,
            "ddd": 0, "assets": [], "markers": mk, "layers": layers}

if __name__ == "__main__":
    bake = json.load(open(ROOT / "output" / "bake.json"))
    OUT.mkdir(exist_ok=True)
    name = ROOT.name
    outs = [(f"{name}-reel.json", build_reel(bake, title=name))]
    if "--scenes" in sys.argv and bake.get("scenes"):
        sc, fps = bake["scenes"], bake["fps"]
        keys = sorted([k for k in sc if k != "end"], key=lambda k: sc[k])
        for n, k in enumerate(keys):
            end = sc[keys[n + 1]] if n + 1 < len(keys) else sc.get("end", bake["duration"])
            outs.append((f"{name}-scene-{n + 1}.json",
                         build_reel(bake, round(sc[k] * fps), round(end * fps) + 1, f"{name} {k}", markers=False)))
    for fn, data in outs:
        p = OUT / fn
        p.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
        print(f"lottie/{fn}  {p.stat().st_size / 1024:.0f} KB  layers={len(data['layers'])}")
