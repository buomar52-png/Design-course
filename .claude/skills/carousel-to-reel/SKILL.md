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
| `output/<slug>-reel-light.mp4` (+ `-light-voice.mp4`) | Day version (`--theme light`). Only when the user asks for النهاري / الفاتح |
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
  - the signature elements (dots, highlight marker, card, handle, icons).
- Carousel-only UI is dropped in video: «اسحب ←» and **the page counter (`٢ / ٤`)**. The user's rule: no page numbering at the top of a reel, and no day/night toggle icon.

### 2. Plan scenes and timing
- Usually **one page = one scene**. Budget the time by reading load: about 2.5 words/s for display text, and more for verses and quotes.
- The hidden-sins split for 40 s with 4 pages was **9 / 10 / 12 / 9**.
- The last scene holds at least 2 s after its final element lands.
- Each scene's out-transition starts 0.55 s before the next scene, and is handled automatically by `sceneOut`.

### 3. Scaffold: the five approved templates (القوالب الخمسة المعتمدة)
```bash
bash .claude/skills/carousel-to-reel/scripts/new_reel.sh <slug> "عنوان الريل" --style <style>
```
| # | `--style` | Template | Source |
|---|---|---|---|
| ١ | `day-grid` | النهاري بالمربعات | `template/` |
| ٢ | `night-grid` | الليلي بالمربعات | `template/` |
| ٣ | `day` | النهاري بدون مربعات | `template/` |
| ٤ | `night` | **الليلي بدون مربعات (default)** | `template/` |
| ٥ | `dual` | المزدوج: ليل ونهار بدون مربعات | `template-dual/` |

- If the user names one of these (by number or name), use it. Otherwise use ٤.
- Styles ١–٤ are one template with the look baked in as the project's `DEFAULTS`. Any of them can still be exported in another look with `--theme` / `--grid`.
- Style ٥ (`template-dual/`):
  - scenes alternate `section.scene.night` / `.day`;
  - an iris wipe opens from the top centre;
  - karaoke text: `.kline` words appear dimmed and light up. Spoken times go in `data-t`; without it they light up in sequence;
  - giant outlined numerals, soft blobs, film grain, a glass card, pill chips, and lime `#c6f36b` with the identity teal;
  - reference: `motion-graphics/quran-hifz-trend/`;
  - **MP4 only:** `bake.js` / Lottie don't support its karaoke spans or iris clip-path yet.
- **The top of the screen stays empty in every template:** no series name, no page counter, no day/night toggle. Drop the series title from the user's design (e.g. «المعاصي الخفية») in the reel.

Then edit `motion-graphics/<slug>/index.html`:
- **Tokens** in `:root`: match the file's colours.
- **Scenes:** replace every `__placeholder__`. Delete, duplicate or reorder scene blocks to fit the pages. Each scene uses the motion library (`wordIn`, `popIn`, `bigIn`, `reveal`, `highlight`, `dotIn`, `fadeUp`, `sceneIn`, `sceneOut`, `spread`).
- **All scene times come from `T`.** Write every tween as `a + offset`, where `a = T.sN`. Never use absolute seconds; that is what makes voice sync a one-line change.
- **Signature visual** (`#visual`): design the post's key graphic from the file (hidden-sins used a heart with the sin names floating inside, drawn by a stroke and then beating). Use SVG with `path.draw` for drawn strokes and `.u` / `.w` for text, so it exports to Lottie.

### Default look: night, no grid (ليلي بدون مربعات)
**New reels default to the night theme on a plain background (no grid). This is the user's chosen house default.**
The template's `DEFAULTS = { theme: 'dark', grid: 'off' }` sets it; `?theme=light` and `?grid=on` override it.
- The template ships with two palettes:
  - `:root` (day);
  - `:root[data-theme="dark"]` (night: the default).
- **Every colour on the page must come from a CSS variable.** When you add an element (a signature visual, an icon), give it a token in **both** palettes. Never hard-code a hex/rgba in a rule or SVG attribute: use `fill="var(--x)"`.
- GSAP cannot tween `var()`. For animated colours (text glow), read the value with `tok('--accent-glow')`.
- When you change the day palette to match a user's file, derive the night one from it:
  - background very dark, tinted with the accent hue;
  - text near-white;
  - accent lifted about 25% in lightness for contrast;
  - highlight becomes a translucent tint (alpha about .38) so light text stays readable;
  - card one step lighter than the background;
  - glows dimmer.
- Export:
  ```bash
  node $S/render.js <dir> [--audio …]                      # default: night, no grid -> <slug>-reel(-voice).mp4
  node $S/render.js <dir> --theme light [--audio …]        # day version -> <slug>-reel-light(-voice).mp4
  node $S/bake.js <dir> && python3 $S/build_lottie.py <dir> [--scenes]   # default look
  node $S/bake.js <dir> --theme light && python3 $S/build_lottie.py <dir> --theme light   # day Lottie
  ```
- QA the default stills; if you also deliver the day version, QA it with `--theme light --stills … --sheet`.
- The grid is off by default. To show it (the user may ask: أظهر المربعات), use `--grid on` (`?grid=on`); the output gets a `-grid` suffix.
- Older projects (`hidden-sins`, `quran-hifz`) predate this default: they are day + grid unless you pass `--theme dark` / `--no-grid`.

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
- Background: plain (night) with a blue glow top-right, a green glow bottom-left, and a slow drift across the whole reel. An optional soft grid of 56px cells can be turned on with `?grid=on`.

### 5. House style: motion
| Element | Motion |
|---|---|
| Headline words | `wordIn`: rise 70px + blur 14→0, stagger 0.1–0.14s, word by word |
| Key/emphasis words | `popIn` (scale 1.6 → 1, back ease) or `bigIn` (expo + heavy blur) |
| Verses, quotes, long lines | `reveal`: right-to-left clip wipe, one line after another |
| Highlight marker | `highlight`, drawn right→left **after** its line has appeared |
| Card | rises 160px with a slight rotation, expo |
| Green dot | `dotIn` pop + halo pulses |
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

## Approved audio settings (إعدادات الصوت المعتمدة)
These are the settings of the voice the user approved («مبدع») on quran-hifz-trend. Keep them as the default for every reel:
- `clean_voice.py` defaults:
  - spectral denoise, strength 0.85, profile from the pauses;
  - pauses: 0.32 s after a sentence end, 0.16 s for a mid-sentence hesitation, pauses under 0.4 s kept;
  - 12 ms fades at cuts;
  - high-pass 70 Hz;
  - **linear** loudnorm to -16 LUFS / -1.5 dBTP;
  - **no compressor**.
- `render.js --audio` muxes the voice untouched (AAC 192k, padded with silence to the video's end).
- Always listen for clipped word tails; fix them with `--protect`.

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
   - find the talk's spine (e.g. "three things to keep in mind") and let the hook scene announce it (e.g. three dots ١ ٢ ٣ that pop in). Never put a page counter in the header;
   - scene starts = the first word of each idea, minus about 0.25 s.
5. **Sync to words:**
   - use the `wordsAt(els, [times])` helper, so each word enters at the moment it is spoken (times from `timing.json`, written as `a + offset`);
   - text may lead the voice by up to about 0.4 s, never trail it;
   - a word that appears must stay on screen for at least about 0.8 s before its scene exits.
6. Add a 🔊 button and `<audio src="audio/voice-clean.m4a">` to the player (see quran-hifz/index.html).
7. Render with `--audio audio/voice-clean.m4a`. The deliverable is `output/<slug>-reel-voice.mp4`.
8. Set `T.end` to the audio length + about 2 s, so the last scene holds after the voice ends.
9. `captions.srt` = the MSA text timed to the real words.

### Editing the speech: retractions, repeats, stumbles, reordering
Reference: `motion-graphics/quran-tadabbur/`, a 126 s recording cut down to 95 s.
- Listen for the speaker's own instructions: «قلت هذه فألغيها» means remove that sentence.
- **Repeated sentence:** keep the take that is better worded and flows into what follows; cut the other.
- **Stumble or false start** (e.g. «جليس لـ… لا يُمَلّ»): cut the fragment only.
- **Closing verse requested last:** `--move-to-end a-b`. It keeps the verse's recited pauses, with 0.7 s of silence before it.
- Find exact boundaries from the 20–40 ms loudness envelope, not from Whisper's word times (they drift by 0.1–0.5 s near pauses). Leave ~0.3 s of pause at each join.

  ```bash
  python3 $S/clean_voice.py voice.m4a transcript.json <dir>/audio --cut a-b … --move-to-end a-b
  ```
- **After cleaning, transcribe `voice-clean.m4a` again.** This finds repeats the first pass merged (e.g. «كلما رددت آياته» twice) and gives the karaoke its exact word times. Where Whisper still misplaces a word, estimate it from the loudness.
- Word Whisper is unsure of: pick the most plausible MSA word and **tell the user explicitly**.
- Long reels (more than ~8 scenes): build the HTML from a declarative spec (`motion-graphics/quran-tadabbur/tools/build.py`):
  - `data-in`: when the element appears;
  - `data-fx`: up | big | card | pill | chip;
  - `data-t`: spoken word times;
  - `data-mark`: when the highlight draws.

  Then retiming is a data edit.
- **Transitions:** the camera transition was tried and rejected by the user («لم تعجبني»). **Never use it.** Approved options:
  - the iris wipe (dual template);
  - **«مدّ ضوئي» (light tide)**, used on quran-tadabbur with the night template. Scenes are transparent layers over one continuous background. Each change:
    - starts 0.62 s before the scene start and lasts 1.15 s with power2.inOut;
    - animates `--p` 0→130% on both scenes: a feathered `mask-image` (22% feather) rising from the bottom hides the old scene and reveals the new one;
    - drifts the old content up 46 px with blur 8;
    - a soft teal/lime glow band (`#tide`, screen blend, blur 18) rides the edge.

    The last scene gets a slow 1→1.03 push. Reference: `motion-graphics/quran-tadabbur/tools/build.py`.
- Big display words (≥200 px): drop the tanween (مختلفٌ → مختلف). It collides with the neighbouring lines.

## Gotchas (learned the hard way)
- **Hiss (الوشّة):** never put a compressor or a dynamic `loudnorm` on a voice-over. They raise the background noise between words; on quran-hifz the hiss was only 15 dB under the voice. `clean_voice.py` now does:
  - spectral denoise (noisereduce, profile learned from the pauses);
  - linear loudness at -16 LUFS;

  `render.js` muxes the voice untouched. To re-clean without changing the sync, use `--reuse-cuts <old timing.json>`. If the user prefers the untouched sound, use `--raw`.
- A text run made only of neutral characters (e.g. a lone «, » inside a span such as `.orn`) must be shaped RTL so the glyph mirrors the way the browser mirrors it. `build_lottie.py` now does this; check the quotation marks in the Lottie frames anyway.
- `window.__seek` must **return nothing** (`t => { tl.seek(t, false); }`). If it returns the timeline, Playwright tries to serialise it and hangs.
- GSAP overrides a CSS `transform: translate(...)` on any element it animates, and parses it before the fonts load, which shifts it. Use `gsap.set(el, { xPercent, yPercent })`. For the Lottie bake, also put `data-xpercent` / `data-ypercent` on such elements, so the layout pass can re-apply them.
- A fully revealed `clip-path: inset(-40% 0% -40% 0%)` serialises in short form (`inset(-40% 0%)`). `bake.js` handles this; keep the `-40%` vertical overscan so diacritics are never cut.
- `bake.js` measures the layout and samples the frames in **two separate page loads**. Never clear GSAP styles on the sampling page.
- Lottie layers paint first-on-top. `build_lottie.py` reverses the DOM order and appends the background last.
- Keep the fonts and `gsap.min.js` local (relative paths), so rendering is deterministic and works offline.
