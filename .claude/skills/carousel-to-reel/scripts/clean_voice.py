"""Remove the choppiness (التقطيع) from a voice-over: shorten long pauses and hesitations.

  python3 clean_voice.py voice.m4a transcript.json <out-dir> [--gap 0.32] [--mid 0.16] [--min 0.4] [--protect 3.4-4.2 ...] [--dry]

- Finds pauses from the loudness envelope (threshold = midpoint of the 10th/90th dB percentiles).
  Soft word endings (ـة/ـه breaths) can sit below that threshold and get clipped: always listen to the
  result, and rerun with --protect <from>-<to> (original-audio seconds) around any clipped tail.
- A pause that follows a sentence end (word ending in . ؟ ! ، : in the transcript) keeps --gap seconds;
  a pause in the middle of a sentence (hesitation) keeps --mid seconds; pauses shorter than --min stay.
- Background hiss is removed first with spectral noise reduction (pip install noisereduce), learning the
  noise from the pauses (--denoise 0.85 = strength 0..1; --no-denoise to skip; --raw = original quality:
  cuts + plain gain only). Every cut gets a 12 ms fade, then high-pass + LINEAR loudness normalisation
  to -16 LUFS. Never add a compressor or dynamic loudnorm: they lift the hiss between words.
- --cut a-b (repeatable) removes a retracted sentence, a repeated sentence (keep the better-worded take),
  a stumble or a filler; --move-to-end a-b plays that passage last (e.g. a closing verse) after
  --move-gap 0.7 s of silence, keeping its own pauses as recited (--trim-moved to shorten them).
  Times are original-audio seconds; find them from the transcript + loudness.
- --reuse-cuts old/timing.json applies the exact cuts of an earlier run (motion stays in sync);
  --name file.m4a sets the output name.
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

# --reuse-cuts timing.json: apply exactly the cuts of an earlier run (keeps the motion in sync)
if "--reuse-cuts" in a:
    cuts = [tuple(c) for c in json.load(open(a[a.index("--reuse-cuts") + 1]))["cuts"]]
    print("reusing", len(cuts), "cuts from", a[a.index("--reuse-cuts") + 1])
# --cut a-b (repeatable): remove a retracted sentence, a repeat or a stumble (ORIGINAL-audio seconds)
manual = [tuple(map(float, a[k + 1].split("-"))) for k in range(len(a)) if a[k] == "--cut"]
# --move-to-end a-b: play that passage last (e.g. a closing verse), after --move-gap seconds of silence
mv = tuple(map(float, a[a.index("--move-to-end") + 1].split("-"))) if "--move-to-end" in a else None
MOVE_GAP = opt("move-gap", 0.7)
def overlaps(c, r): return c[0] < r[1] and c[1] > r[0]
auto = [c for c in cuts if not any(overlaps(c, m) for m in manual)]
main_cuts = sorted(manual + [c for c in auto if not (mv and overlaps(c, mv))] + ([mv] if mv else []))
# the moved passage (usually a verse) keeps its recited pauses unless --trim-moved
moved_cuts = sorted(c for c in auto if mv and mv[0] <= c[0] and c[1] <= mv[1]) if "--trim-moved" in a else []
auto = [c for c in auto if not (mv and overlaps(c, mv) and "--trim-moved" not in a)]
cuts = sorted(manual + auto)                     # recorded in timing.json for --reuse-cuts

print(f"threshold {th:.1f} dB · {len(pauses)} pauses · {len(auto)} pause cuts · {len(manual)} manual cuts" + (f" · moving {mv[0]}-{mv[1]} to the end" if mv else ""))
for s, e in cuts: print(f"  {'cut ' if (s, e) in auto else 'CUT '}{s:6.2f}-{e:6.2f} ({e - s:.2f}s)  after «{before(s)}»")
def keep_between(cs, a0, a1):
    out, t = [], a0
    for s, e in sorted(cs):
        if e <= a0 or s >= a1: continue
        if s > t: out.append((t, s))
        t = max(t, e)
    if t < a1: out.append((t, a1))
    return out
keep = keep_between(main_cuts, 0.0, dur)
if mv:
    while keep and keep[-1][1] - keep[-1][0] < 0.02: keep.pop()
    keep += [("gap", MOVE_GAP)] + keep_between(moved_cuts, *mv)
seg_len = lambda k: k[1] if k[0] == "gap" else k[1] - k[0]
total = sum(seg_len(k) for k in keep)
print(f"{dur:.2f}s -> {total:.2f}s")
if "--dry" in a: sys.exit()

# ---- denoise (before cutting, so the noise profile comes from the real pauses) ----
RAW = "--raw" in a                      # original quality: cuts + gain only, no processing at all
if not RAW and "--no-denoise" not in a:
    try:
        import noisereduce as nr
        prof = np.concatenate([x[int(s * SR):int(e * SR)] for s, e in pauses if e - s > 0.2] or [x[: SR // 2]])
        strength = opt("denoise", 0.85)
        x = nr.reduce_noise(y=x, sr=SR, y_noise=prof, stationary=True, prop_decrease=strength,
                            n_fft=2048, freq_mask_smooth_hz=500, time_mask_smooth_ms=60).astype(np.float32)
        print(f"denoised (noisereduce, strength {strength}, profile {len(prof) / SR:.1f}s)")
    except ImportError:
        print("! noisereduce not installed (pip install noisereduce): using ffmpeg afftdn instead")
        RAW_FALLBACK = True

fade = int(0.012 * SR); parts = []
for s, e in keep:
    if s == "gap": parts.append(np.zeros(int(e * SR), dtype=np.float32)); continue
    seg = x[int(s * SR):int(e * SR)].copy()
    if len(seg) > 2 * fade: seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    parts.append(seg)
os.makedirs(outdir, exist_ok=True)
tmp = os.path.join(outdir, ".cut.f32"); np.concatenate(parts).astype(np.float32).tofile(tmp)
# ---- loudness: LINEAR two-pass loudnorm (a plain gain). No compressor and no dynamic loudnorm:
#      both lift the quiet parts and make the background hiss (الوشّة) audible between words.
pre = "" if RAW else "highpass=f=70," + ("afftdn=nf=-45:nr=12," if "RAW_FALLBACK" in globals() else "")
meas = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp,
                       "-af", pre + "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
ln = (f"loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
      f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}")
out_name = opt_s = a[a.index("--name") + 1] if "--name" in a else "voice-clean.m4a"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp,
                "-af", pre + ln, "-ar", "48000", "-c:a", "aac", "-b:a", "192k", os.path.join(outdir, out_name)], check=True)
os.remove(tmp)
def remap(v):                                    # original time -> cleaned time (segments in output order)
    acc = 0.0
    for s, e in keep:
        if s != "gap" and s <= v <= e: return acc + (v - s)
        acc += seg_len((s, e))
    return None                                  # the word was cut

json.dump({"duration": total, "cuts": cuts, "keep": keep,
           "words": sorted([{"w": w["w"].strip(), "s": round(remap(w["s"]), 2), "e": round(remap(w["e"]) or remap(w["s"]), 2)}
                            for w in words if remap(w["s"]) is not None], key=lambda w: w["s"])},
          open(os.path.join(outdir, "timing.json"), "w"), ensure_ascii=False, indent=1)
print("->", os.path.join(outdir, out_name), "+ timing.json")
