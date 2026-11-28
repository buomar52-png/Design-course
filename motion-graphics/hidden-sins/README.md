# المعاصي الخفية — موشن جرافكس (٩:١٦، ٤٠ ثانية)

تحويل تصميم الكاروسيل (٤ صفحات) إلى موشن عمودي 1080×1920، والنصوص منقولة حرفيًا من الملف.

| الملف | الاستخدام |
|---|---|
| `output/hidden-sins-reel.mp4` | الفيديو النهائي (H.264، ‏30fps، ‏40 ثانية، بدون صوت) جاهز تضيف عليه تعليقك الصوتي |
| `index.html` | المصدر الحي (GSAP). افتحه في المتصفح: تشغيل وإيقاف، شريط تقديم، وزر **Safe zone** يُظهر مناطق واجهة ريلز |
| `lottie/hidden-sins-reel.json` | الريل كاملًا بصيغة Lottie، والنصوص محوّلة لأشكال متجهة فلا يحتاج خطوطًا |
| `lottie/heart-loop.json` | عنصر القلب بالذنوب الخفية، لوب ثانيتين بخلفية شفافة |
| `reels/cover.png` | غلاف الريل |
| `reels/voiceover-script.md` | نص تعليق صوتي مقترح مضبوط على توقيت المشاهد |
| `reels/captions.srt` | ترجمة نصية للتعليق المقترح (للرفع على المنصة أو برامج المونتاج) |
| `reels/post-caption.txt` | وصف المنشور والهاشتاقات |

## المشاهد
| الوقت | المشهد |
|---|---|
| 0–9 ث | الغلاف: «ذنوبٌ لا يراها الناس…» + القلب |
| 9–19 ث | الآية: الأنعام ١٢٠ |
| 19–31 ث | الخطر الحقيقي + كلام السعدي |
| 31–40 ث | طاعة السر |

## دمج الصوت مع الفيديو
```bash
ffmpeg -i output/hidden-sins-reel.mp4 -i voice.m4a -c:v copy -c:a aac -b:a 192k -shortest reel-with-voice.mp4
```

## إعادة التصدير بعد أي تعديل في `index.html`
```bash
node tools/render.js                 # MP4 (يتطلب playwright و ffmpeg)
node tools/bake.js && python3 tools/build_lottie.py   # Lottie (pip install uharfbuzz fonttools)
```
