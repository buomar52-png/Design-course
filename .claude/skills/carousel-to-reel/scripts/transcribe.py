"""Transcribe a voice recording (Arabic, any dialect) with word timestamps.

  python3 transcribe.py voice.m4a out/transcript.json [--model large-v3] [--literal]

--literal  bias Whisper toward writing dialect words and fillers as spoken (to spot hesitations).
           Without it Whisper tends to normalise toward MSA, which is a good first draft for the screen text.
Needs: pip install faster-whisper   (the model downloads from huggingface.co on first use, ~3 GB for large-v3)
Audio is decoded with ffmpeg and handed over as samples (avoids PyAV version issues).
"""
import json, subprocess, sys, os
import numpy as np
from faster_whisper import WhisperModel

args = sys.argv[1:]
if len(args) < 2: sys.exit(__doc__)
src, out = args[0], args[1]
model = args[args.index("--model") + 1] if "--model" in args else "large-v3"
prompt = "امم.. يعني.. إيه، آآ" if "--literal" in args else "تسجيل صوتي باللهجة الخليجية."

pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
cache = os.environ.get("WHISPER_CACHE", os.path.expanduser("~/.cache/whisper"))
m = WhisperModel(model, device="cpu", compute_type="int8", download_root=cache)
segs, _ = m.transcribe(audio, language="ar", word_timestamps=True, beam_size=5, initial_prompt=prompt)
res = []
for s in segs:
    res.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                "words": [{"s": w.start, "e": w.end, "w": w.word, "p": w.probability} for w in s.words]})
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}")
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
