---
name: carousel-to-reel
description: Turn a user's carousel / post design (PDF or images, usually Arabic) into a vertical 9:16 motion-graphics reel in the house style — GSAP HTML source, MP4 video, Lottie (whole reel + per scene), and a reels kit (cover, timed voice-over script, SRT, post caption) — and later sync it to the user's recorded voice-over. Also builds a reel from a voice recording alone (any Arabic dialect): transcribes, rewrites the screen text in فصحى, removes pauses/choppiness (التقطيع) and syncs every word. Use whenever the user sends a design file or a voice recording and asks for a reel, motion, موشن, ريل, فيديو, or sends a voice recording for an existing reel.
---

# من كاروسيل إلى ريل (Carousel → Reel)

> **باختصار:** المستخدم يرسل ملف تصميم (عادةً كاروسيل من عدة صفحات)، ونحوّله إلى ريل عمودي متحرك بنفس هويته.
> **ما يظهر على الشاشة يكون من الملف حرفيًا.** والمستخدم يسجّل التعليق الصوتي بنفسه.
> المرجع المعتمد لهذا الأسلوب هو `motion-graphics/hidden-sins/` (المعاصي الخفية). افتحه وشاهده قبل أول ريل.

## Deliverables (every reel)
All files go in `motion-graphics/<slug>/`:

| Path | What |
|---|---|
| `index.html` | GSAP source, plays in a browser (player, scrubber, **Safe zone** toggle) |
| `output/<slug>-reel.mp4` | 1080×1920, H.264, 30fps, silent |
| `lottie/<slug>-reel.json` (+ `-scene-N.json`) | Text converted to vector shapes, so no fonts are needed |
| `reels/cover.png` | A settled frame from scene 1 |
| `reels/voiceover-script.md` | Table: time · scene · on-screen text · suggested VO (≈2 words/s) |
| `reels/captions.srt` | Captions of the suggested VO, timed to the scenes |
| `reels/post-caption.txt` | Post text + hashtags |
| `README.md` | Files, scene table, re-export commands (copy the shape of hidden-sins/README.md) |

The default is **9:16 and ≤ 40 s** unless the user says otherwise. Ask nothing that the file already answers.

## Setup (once per environment)
- `ffmpeg`, Playwright + Chromium (`require('playwright')`), Python 3.
- `pip install uharfbuzz fonttools brotli pillow`
- For checking Lottie: `npm i lottie-web@5.12.2` in the scratchpad.
- Fonts and GSAP are vendored in `template/`. To fetch another Google font as TTF: request the css2 URL with header `User-Agent: Mozilla/4.0` and download the `.ttf` URLs it returns.

## Workflow

### 1. Read the design completely
- Read **every page** of the PDF/images. Transcribe all on-screen text **verbatim**: punctuation, «», diacritics, and Arabic-Indic digits.
- **Quran / hadith text:** reproduce the harakat exactly as in the file, and double-check them against the known text of the verse. Never paraphrase or retype from memory without checking. Keep the reference line (e.g. `[سورة الأنعام: ١٢٠]`).
- Note the identity:
  - colours (sample pixels with PIL from a rendered page);
  - font (the template uses IBM Plex Sans Arabic);
  - the signature elements (dots, highlight marker, card, header bar, page counter, handle, icons).
- Carousel-only UI such as «اسحب ←» is dropped in video. The page counter `٢ / ٤` is kept: it rolls in the header.

### 2. Plan scenes and timing
- Usually **one page = one scene**. Budget the time by reading load: about 2.5 words/s for display text, and more for verses and quotes.
- The hidden-sins split for 40 s with 4 pages was **9 / 10 / 12 / 9**.
- The last scene holds at least 2 s after its final element lands.
- Each scene's out-transition starts 0.55 s before the next scene, and is handled automatically by `sceneOut`.

### 3. Scaffold
```bash
bash .claude/skills/carousel-to-reel/scripts/new_reel.sh <slug> "عنوان الريل"
```
Then edit `motion-graphics/<slug>/index.html`:
- **Tokens** in `:root`: match the file's colours.
- **Scenes:** replace every `__placeholder__`. Delete, duplicate or reorder scene blocks to fit the pages. Each scene uses the motion library (`wordIn`, `popIn`, `bigIn`, `reveal`, `highlight`, `dotIn`, `fadeUp`, `sceneIn`, `sceneOut`, `counterTo`, `spread`).
- **All scene times come from `T`.** Write every tween as `a + offset`, where `a = T.sN`. Never use absolute seconds; that is what makes voice sync a one-line change.
- **Signature visual** (`#visual`): design the post's key graphic from the file (hidden-sins used a heart with the sin names floating inside, drawn by a stroke and then beating). Use SVG with `path.draw` for drawn strokes and `.u` / `.w` for text, so it exports to Lottie.

### 4. House style: layout
- Stage 1080×1920, side padding 100px, text right-aligned (RTL).
- **Reels safe zones:** keep key content out of the top 220px, the bottom 380px, and the right 140px of the lower half. Check with the Safe zone button.
- Type scale used:

  | Element | Size |
  |---|---|
  | Hook headline | 116px / 700 |
  | Accent word | 220–236px teal |
  | Verse | 84px / 500, centred, line-height 1.62 |
  | Statement | 92px |
  | Card quote | 45px |
  | Closing lines | 64px |
  | Handle | 36px at y≈1660 |

- Lines are `white-space: nowrap`. **You must verify that no line overflows** (step 6), and shrink the font or rebreak the line when one does.
- Background: soft grid of 56px cells, a blue glow top-right, a green glow bottom-left, and a slow drift across the whole reel.

### 5. House style: motion
| Element | Motion |
|---|---|
| Headline words | `wordIn`: rise 70px + blur 14→0, stagger 0.1–0.14s, word by word |
| Key/emphasis words | `popIn` (scale 1.6 → 1, back ease) or `bigIn` (expo + heavy blur) |
| Verses, quotes, long lines | `reveal`: right-to-left clip wipe, one line after another |
| Highlight marker | `highlight`, drawn right→left **after** its line has appeared |
| Card | rises 160px with a slight rotation, expo |
| Green dot | `dotIn` pop + halo pulses |
| Header | bar grows, name slides in, counter rolls with `counterTo` |
| Focal visual | stroke draw → fill → items pop in from the centre → heartbeat or float |
| Scene exit | up 60px + blur + fade, 0.55s |

**Never animate Arabic letter by letter**: it breaks the letter joining. Animate by word or by line mask.

### 6. QA loop (do not skip)
```bash
S=.claude/skills/carousel-to-reel/scripts
node $S/render.js motion-graphics/<slug> --stills 8,13.5,17,29.5,39.5 --sheet
```
- Look at the stills: one settled frame per scene, plus mid-transition frames.
- Check for:
  - overflowing or clipped lines;
  - clipped harakat;
  - overlaps;
  - text inside the safe zones;
  - visual items crossing their container (e.g. words outside the heart).
- Fix and repeat. Inspect at full resolution before "fixing" glow edges: downscaled sheets show false hard edges.

### 7. Export
```bash
node $S/render.js motion-graphics/<slug>                    # MP4, ~6 min for 40 s, so run it in the background
node $S/bake.js motion-graphics/<slug>                      # samples the timeline -> output/bake.json
python3 $S/build_lottie.py motion-graphics/<slug> --scenes  # lottie/<slug>-reel.json + per-scene files
node $S/check_lottie.js motion-graphics/<slug>/lottie/<slug>-reel.json /tmp/lt 240 600 1000 --lib <lottie.min.js>
```
- Compare the Lottie frames with the HTML stills (frame = seconds × 30). They should match closely; blur is not carried into Lottie, only opacity and transforms.
- Check the MP4 with `ffprobe`: duration, 1080×1920, 30fps.
- Cover: `node $S/render.js <dir> --stills <settled time in scene 1>`, then copy it to `reels/cover.png`.
- Write the reels kit files and the README.

### 8. Deliver
- Send the MP4 and the cover with SendUserFile (`render`). Attach the Lottie files, the script, the SRT and the caption (`attach`).
- Commit `motion-graphics/<slug>/` and push to the session's branch. `output/bake.json` and `output/stills/` are gitignored.
- Reply in Arabic with:
  - a short scene table;
  - the file list;
  - an offer: "send me your recording and I'll sync the motion to your voice".

### 9. When the voice-over arrives
```bash
python3 $S/voice_sync.py voice.m4a --scenes 4        # prints phrases, pauses and a suggested T
```
1. Check the suggested cuts against the script: each cut must sit where a new page's idea starts, which is not always the longest pause.
2. Put the result in `T`, including `end` ≈ audio length + 0.8 s.
3. If a scene got much shorter or longer, rebalance the offsets inside that scene with `spread(n, from, to)` so its elements fill the new window.
4. Re-run the QA stills, then:
   ```bash
   node $S/render.js motion-graphics/<slug> --audio voice.m4a   # -> <slug>-reel.mp4 and <slug>-reel-voice.mp4 (loudness normalised)
   ```
5. Rebuild the Lottie and update the SRT to the real words when the user wants captions.

## Voice-first reel (the user sends only a recording)
Reference: `motion-graphics/quran-hifz/`, built from a Bahraini-dialect recording. Typical asks:
- the on-screen text in **الفصحى**;
- the same theme;
- remove the choppiness (**احذف التقطيع**).

1. **Transcribe:**
   ```bash
   python3 $S/transcribe.py voice.m4a <scratch>/transcript.json
   ```
   - Whisper large-v3 normalises dialect toward MSA, which makes a good draft.
   - Run it again with `--literal` to expose fillers and repeated words.
   - Fix mishearings from context: «أم نعاش» was «أمُّنا عائشة».
2. **Clean the voice:**
   ```bash
   python3 $S/clean_voice.py voice.m4a transcript.json motion-graphics/<slug>/audio --dry
   ```
   - Review the plan, then run it without `--dry`.
   - Pauses after a sentence end keep 0.32 s; mid-sentence hesitations keep 0.16 s.
   - Output: `audio/voice-clean.m4a` + `audio/timing.json` (every word re-timed onto the cleaned audio).
   - Keep the original as `audio/voice-original.m4a`.
3. **Screen text = the speech rewritten in correct MSA:**
   - keep the meaning, drop the dialect words (تبي → تريد/أردتَ, هذي → هذه, ثانية → أخرى);
   - quoted Quran/hadith get full harakat and their source (e.g. [رواه البخاري]). Only add a source you are certain of, and tell the user you added it;
   - deliver `reels/transcript.md`, a dialect | MSA table.
4. **Structure:**
   - find the talk's spine (e.g. "three things to keep in mind"), give the header counter that count (١ / ٣ …), and make the hook scene announce it;
   - scene starts = the first word of each idea, minus about 0.25 s.
5. **Sync to words:**
   - use the `wordsAt(els, [times])` helper, so each word enters at the moment it is spoken (times from `timing.json`, written as `a + offset`);
   - text may lead the voice by up to about 0.4 s, never trail it;
   - a word that appears must stay on screen for at least about 0.8 s before its scene exits.
6. Add a 🔊 button and `<audio src="audio/voice-clean.m4a">` to the player (see quran-hifz/index.html).
7. Render with `--audio audio/voice-clean.m4a`. The deliverable is `output/<slug>-reel-voice.mp4`.
8. Set `T.end` to the audio length + about 2 s, so the last scene holds after the voice ends.
9. `captions.srt` = the MSA text timed to the real words.

## Gotchas (learned the hard way)
- A text run made only of neutral characters (e.g. a lone «, » inside a span such as `.orn`) must be shaped RTL so the glyph mirrors the way the browser mirrors it. `build_lottie.py` now does this; check the quotation marks in the Lottie frames anyway.
- `window.__seek` must **return nothing** (`t => { tl.seek(t, false); }`). If it returns the timeline, Playwright tries to serialise it and hangs.
- GSAP overrides a CSS `transform: translate(...)` on any element it animates, and parses it before the fonts load, which shifts it. Use `gsap.set(el, { xPercent, yPercent })`. For the Lottie bake, also put `data-xpercent` / `data-ypercent` on such elements, so the layout pass can re-apply them.
- A fully revealed `clip-path: inset(-40% 0% -40% 0%)` serialises in short form (`inset(-40% 0%)`). `bake.js` handles this; keep the `-40%` vertical overscan so diacritics are never cut.
- `bake.js` measures the layout and samples the frames in **two separate page loads**. Never clear GSAP styles on the sampling page.
- Lottie layers paint first-on-top. `build_lottie.py` reverses the DOM order and appends the background last.
- Keep the fonts and `gsap.min.js` local (relative paths), so rendering is deterministic and works offline.
