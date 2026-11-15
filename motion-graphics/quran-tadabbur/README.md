# كتاب الله مختلف — القالب المزدوج (يبدأ نهاري) · ٩:١٦ · ٩٨ ثانية

ريل من تسجيل صوتي: النص على الشاشة بالفصحى، والصوت منظّف من التقطيع والتكرار، والآية الكريمة ﴿إِنَّ فِي ذَٰلِكَ لَذِكْرَىٰ…﴾ في آخره. تفاصيل التعديلات في `reels/transcript.md`.

| الملف | الاستخدام |
|---|---|
| `output/quran-tadabbur-reel-voice.mp4` | **الفيديو النهائي مع الصوت** |
| `output/quran-tadabbur-reel.mp4` | نفس الفيديو بدون صوت |
| `index.html` | المصدر الحي، فيه زر 🔊 للتشغيل مع الصوت. يُولَّد من `tools/build.py` |
| `audio/voice-clean.m4a` | الصوت بعد التنظيف والتعديلات |
| `audio/voice-original.m4a` | التسجيل الأصلي |
| `reels/transcript.md` | النص على الشاشة وسجل تعديلات الصوت |

## إعادة البناء والتصدير
```bash
python3 tools/build.py                                      # يولّد index.html من مواصفات المشاهد
S=../../.claude/skills/carousel-to-reel/scripts
node $S/render.js . --audio audio/voice-clean.m4a
```

### تنظيف الصوت (للإعادة)
```bash
python3 $S/clean_voice.py audio/voice-original.m4a transcript.json audio \
  --cut 30.85-36.40 --cut 53.55-60.50 --cut 71.20-73.30 --cut 85.46-85.74 \
  --cut 111.10-115.25 --cut 123.79-126.19 --move-to-end 99.00-106.22
```
