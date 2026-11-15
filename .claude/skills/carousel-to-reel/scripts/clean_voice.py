"""Remove the choppiness (التقطيع) from a voice-over: shorten long pauses and hesitations.

  python3 clean_voice.py voice.m4a transcript.json <out-dir> [--gap 0.32] [--mid 0.16] [--min 0.4] [--protect 3.4-4.2 ...] [--dry]

- Finds pauses from the loudness envelope (threshold = midpoint of the 10th/90th dB percentiles).
  Soft word endings (ـة/ـه breaths) can sit below that threshold and get clipped: always listen to the
  result, and rerun with --protect <from>-<to> (original-audio seconds) around any clipped tail.
- A pause that follows a sentence end (word ending in . ؟ ! ، : in the transcript) keeps --gap seconds;
  a pause in the middle of a sentence (hesitation) keeps --mid seconds; pauses shorter than --min stay.
- Every cut gets a 12 ms fade, then: high-pass, light FFT denoise, gentle compression, loudnorm -14 LUFS.
Writes <out-dir>/voice-clean.m4a and <out-dir>/timing.json (every word re-timed onto the cleaned audio,
ready for placing animations). --dry prints the plan without writing.
The words themselves are never cut; if the speaker repeated a word or said a filler, cut it by hand
(add its span to a "cuts" list) after checking with transcribe.py --literal.
"""
import json, subprocess, sys, os, re
import numpy as np

a = sys.argv[1:]
if len(a) < 3: sys.exit(__doc__)
src, tjson, outdir = a[0], a[1], a[2]
opt = lambda k, d: float(a[a.index("--" + k) + 1]) if "--" + k in a else d
GAP, MID, MIN = opt("gap", 0.32), opt("mid", 0.16), opt("min", 0.4)
SR = 48000

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32).copy()
dur = len(x) / SR
hop, win = SR // 100, int(SR * 0.03)
db = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + win] ** 2)) + 1e-9) for i in range(0, len(x) - win, hop)])
th = (np.percentile(db, 10) + np.percentile(db, 90)) / 2
quiet = db < th
pauses, i = [], 0
while i < len(quiet):
    if quiet[i]:
        j = i
        while j < len(quiet) and quiet[j]: j += 1
        if (j - i) / 100 >= 0.25: pauses.append((i / 100, j / 100))
        i = j
    else: i += 1

words = [w for s in json.load(open(tjson)) for w in s["words"]]
def before(t):
    prev = [w for w in words if w["e"] <= t + 0.45]
    return prev[-1]["w"].strip() if prev else ""

# --protect a-b (repeatable): never cut inside [a, b] of the ORIGINAL audio (e.g. a soft word ending)
protect = [tuple(map(float, a[k + 1].split("-"))) for k in range(len(a)) if a[k] == "--protect"]
def unprotect(s, e):
    for pa, pb in protect:
        if pa < e and pb > s:          # overlap -> keep the part after the protected range
            s = max(s, pb)
    return s, e

cuts = []
for s, e in pauses:
    s, e = unprotect(s, e)
    if e >= dur - 0.1: cuts.append((s + 0.35, dur)); continue
    if s < 0.05: cuts.append((0, max(0, e - 0.12))); continue
    if e - s < MIN: continue
    keep = GAP if re.search(r"[.؟?!،,:؛]$", before(s)) else MID
    k1 = min(0.14, keep * 0.45)
    cuts.append((s + k1, e - (keep - k1)))

print(f"threshold {th:.1f} dB · {len(pauses)} pauses · {len(cuts)} cuts")
for s, e in cuts: print(f"  cut {s:6.2f}-{e:6.2f} ({e - s:.2f}s)  after «{before(s)}»")
keep, t = [], 0.0
for s, e in cuts:
    if s > t: keep.append((t, s))
    t = e
if t < dur: keep.append((t, dur))
total = sum(e - s for s, e in keep)
print(f"{dur:.2f}s -> {total:.2f}s")
if "--dry" in a: sys.exit()

fade = int(0.012 * SR); parts = []
for s, e in keep:
    seg = x[int(s * SR):int(e * SR)].copy()
    if len(seg) > 2 * fade: seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    parts.append(seg)
os.makedirs(outdir, exist_ok=True)
tmp = os.path.join(outdir, ".cut.f32"); np.concatenate(parts).astype(np.float32).tofile(tmp)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp,
                "-af", "highpass=f=70,afftdn=nf=-42:nr=10,acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120,loudnorm=I=-14:TP=-1.5:LRA=9",
                "-c:a", "aac", "-b:a", "192k", os.path.join(outdir, "voice-clean.m4a")], check=True)
os.remove(tmp)
def remap(v):
    acc = 0.0
    for s, e in keep:
        if v < s: return acc
        if v <= e: return acc + (v - s)
        acc += e - s
    return acc
json.dump({"duration": total, "cuts": cuts,
           "words": [{"w": w["w"].strip(), "s": round(remap(w["s"]), 2), "e": round(remap(w["e"]), 2)} for w in words]},
          open(os.path.join(outdir, "timing.json"), "w"), ensure_ascii=False, indent=1)
print("->", os.path.join(outdir, "voice-clean.m4a"), "+ timing.json")
