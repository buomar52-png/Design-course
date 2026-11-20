"""Suggest scene start times (the T object in index.html) from a voice-over recording.

  python3 voice_sync.py voice.m4a [--scenes 4] [--noise -35] [--min-silence 0.35]

How: ffmpeg's silencedetect finds pauses; the (scenes - 1) longest pauses become scene cuts.
Each cut is placed 0.25s before the next phrase starts, so the text lands just ahead of the voice.
Always review the printed phrases and adjust by ear: a cut belongs where a new idea (= a new
carousel page) begins, which is usually but not always one of the longest pauses.
"""
import re, subprocess, sys

args = sys.argv[1:]
if not args or args[0].startswith("--"):
    sys.exit(__doc__)
audio = args[0]
opt = lambda k, d: type(d)(args[args.index("--" + k) + 1]) if "--" + k in args else d
scenes, noise, min_sil = opt("scenes", 4), opt("noise", -35), opt("min-silence", 0.35)

dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio],
                           capture_output=True, text=True).stdout.strip())
log = subprocess.run(["ffmpeg", "-hide_banner", "-i", audio, "-af", f"silencedetect=noise={noise}dB:d={min_sil}", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
pauses = [(s, e) for s, e in zip(starts, ends)]

# speech phrases between pauses
phrases, t = [], 0.0
for s, e in pauses:
    if s - t > 0.15: phrases.append((t, s))
    t = e
if dur - t > 0.15: phrases.append((t, dur))
lead = phrases[0][0] if phrases else 0.0

inner = [(e - s, s, e) for s, e in pauses if s > lead + 0.5 and e < dur - 0.3]
cuts = sorted(sorted(inner, reverse=True)[: max(0, scenes - 1)], key=lambda p: p[1])
T = {"s1": 0}
for n, (_, s, e) in enumerate(cuts, start=2):
    T[f"s{n}"] = round(max(0, e - 0.25), 2)
T["end"] = round(min(dur + 0.8, 90), 2)

print(f"audio: {dur:.2f}s   speech starts at {lead:.2f}s   pauses found: {len(pauses)}\n")
print("phrases:")
for s, e in phrases:
    print(f"  {s:6.2f} - {e:6.2f}  ({e - s:4.1f}s)")
print("\nlongest pauses used as scene cuts:")
for d, s, e in cuts:
    print(f"  {s:6.2f} - {e:6.2f}  ({d:.2f}s)")
if len(cuts) < scenes - 1:
    print(f"\n! only {len(cuts)} usable pauses for {scenes} scenes — try --noise -30 or --min-silence 0.25")
print("\nput this in index.html:\n  const T = { " + ", ".join(f"{k}: {v:g}" for k, v in T.items()) + " };")
