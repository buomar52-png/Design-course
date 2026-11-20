// Render frames of a Lottie file with lottie-web to verify it (compare against render.js stills).
//   node check_lottie.js <file.json> <out-prefix> <frame> [frame...] [--lib path/to/lottie.min.js]
// lottie-web: `npm i lottie-web@5.12.2` in any scratch folder, then pass --lib or run from there.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const a = process.argv.slice(2);
const li = a.indexOf('--lib');
const lib = li >= 0 ? a.splice(li, 2)[1] : (() => {
  try { return require.resolve('lottie-web/build/player/lottie.min.js', { paths: [process.cwd(), __dirname] }); }
  catch { console.error('lottie-web not found: npm i lottie-web@5.12.2 (or pass --lib)'); process.exit(1); }
})();
const [file, prefix, ...frames] = a;
const data = JSON.parse(fs.readFileSync(file, 'utf8'));

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: data.w, height: data.h } });
  await p.setContent(`<body style="margin:0;background:#fff"><div id=a style="width:${data.w}px;height:${data.h}px"></div></body>`);
  await p.addScriptTag({ path: lib });
  await p.evaluate(d => { window.an = lottie.loadAnimation({ container: document.getElementById('a'), renderer: 'svg', loop: false, autoplay: false, animationData: d }); }, data);
  await p.waitForTimeout(400);
  for (const f of frames) {
    await p.evaluate(f => an.goToAndStop(+f, true), f);
    await p.waitForTimeout(50);
    await p.screenshot({ path: `${prefix}-${f}.png` });
  }
  await b.close();
  console.log(`${frames.length} frame(s) -> ${path.resolve(prefix)}-*.png`);
})();
