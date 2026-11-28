# استحضر عند حفظ القرآن — ريل موشن (٩:١٦، ٢٧ ثانية)

ريل من تسجيل صوتي باللهجة البحرينية. الكلام على الشاشة بالفصحى، والصوت منظّف من الوقفات. التصميم بنفس هوية «المعاصي الخفية» (مهارة `carousel-to-reel`).

| الملف | الاستخدام |
|---|---|
| `output/quran-hifz-reel-voice.mp4` | **الفيديو النهائي مع الصوت**، جاهز للنشر |
| `output/quran-hifz-reel.mp4` | نفس الفيديو بدون صوت |
| `output/quran-hifz-reel-dark-voice.mp4` | **النسخة الليلية** مع الصوت (`index.html?theme=dark`) |
| `output/quran-hifz-reel-dark.mp4` | النسخة الليلية بدون صوت |
| `output/quran-hifz-reel-dark-nogrid-voice.mp4` | النسخة الليلية **بدون مربعات الخلفية** مع الصوت (`?theme=dark&grid=off`) |
| `index.html` | المصدر الحي. افتحه في المتصفح، واضغط 🔊 لتشغيله مع الصوت |
| `lottie/quran-hifz-reel.json` | الريل كاملًا بصيغة Lottie (النصوص أشكال متجهة) |
| `lottie/quran-hifz-scene-N.json` | كل مشهد في ملف مستقل |
| `audio/voice-clean.m4a` | التسجيل بعد التنظيف |
| `audio/voice-original.m4a` | التسجيل الأصلي |
| `audio/timing.json` | توقيت كل كلمة على التسجيل المنظّف |
| `reels/` | الغلاف، والترجمة بالفصحى `captions.srt`، والتفريغ `transcript.md`، ووصف المنشور |

## المشاهد
| الوقت | المشهد |
|---|---|
| 0–4.2 ث | إذا أردتَ أن **تحفظ القرآن** + مصحف يُرسم بالخطوط |
| 4.2–8.7 ث | ١ / ٣: «خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ» |
| 8.7–17.4 ث | ٢ / ٣: «كَانَ خُلُقُهُ الْقُرْآنَ» + وكانت رسالتُه القرآن |
| 17.4–27 ث | ٣ / ٣: ويكفي الإنسانَ **شرفًا** أنه يحفظ القرآن |

## إعادة التصدير
```bash
S=../../.claude/skills/carousel-to-reel/scripts
node $S/render.js . --audio audio/voice-clean.m4a
node $S/render.js . --audio audio/voice-clean.m4a --theme dark   # النسخة الليلية
node $S/bake.js . && python3 $S/build_lottie.py . --scenes
```
