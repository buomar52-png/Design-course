// Render a reel project (index.html built from the template) to MP4 or stills.
//
//   node render.js <project-dir>                          -> <dir>/output/<name>-reel.mp4  (30fps)
//   node render.js <project-dir> --audio voice.m4a        -> also <name>-reel-voice.mp4 (voice muxed in)
//   node render.js <project-dir> --stills 2,8.5,14,30     -> <dir>/output/stills/t-<sec>.png
//   options: --fps 60   --out path.mp4   --sheet  (with --stills: also a contact sheet stills/sheet.png)
//            --theme dark   (index.html?theme=dark; outputs get a -dark suffix)
//
// Needs: playwright (Chromium) and ffmpeg on PATH.
const { chromium } = require('playwright');
const { spawn, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const flag = k => args.includes('--' + k);
const dir = path.resolve(args[0] && !args[0].startsWith('--') ? args[0] : '.');
const name = path.basename(dir);
const fps = +opt('fps', 30);
const out = path.resolve(dir, opt('out', `output/${name}-reel${opt('theme', null) ? '-' + opt('theme', null) : ''}.mp4`));
const stills = opt('stills', null);
const audio = opt('audio', null);
const theme = opt('theme', null);

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => { console.error('page error:', e.message); process.exitCode = 1; });
  await page.goto('file://' + path.join(dir, 'index.html') + '?render' + (theme ? '&theme=' + theme : ''));
  await page.evaluate(() => window.__ready);
  await page.waitForTimeout(300);
  const duration = await page.evaluate(() => window.__duration);

  if (stills) {
    const sdir = path.join(dir, 'output/stills');
    fs.mkdirSync(sdir, { recursive: true });
    const files = [];
    for (const t of stills.split(',').map(Number)) {
      await page.evaluate(t => window.__seek(t), t);
      const f = path.join(sdir, `t-${t.toFixed(2).padStart(6, '0')}${theme ? '-' + theme : ''}.png`);
      await page.screenshot({ path: f }); files.push(f);
    }
    await browser.close();
    if (flag('sheet')) {
      const n = files.length;
      spawnSync('ffmpeg', ['-y', '-loglevel', 'error', ...files.flatMap(f => ['-i', f]),
        '-filter_complex', files.map((_, i) => `[${i}]scale=360:640[v${i}]`).join(';') + ';' +
        files.map((_, i) => `[v${i}]`).join('') + `hstack=inputs=${n}`, path.join(sdir, 'sheet.png')], { stdio: 'inherit' });
      if (n === 1) fs.copyFileSync(files[0], path.join(sdir, 'sheet.png'));
    }
    console.log('stills ->', sdir);
    return;
  }

  fs.mkdirSync(path.dirname(out), { recursive: true });
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
    '-movflags', '+faststart', '-r', String(fps), out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const total = Math.round(duration * fps);
  for (let f = 0; f < total; f++) {
    await page.evaluate(t => window.__seek(t), f / fps);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % fps === 0) process.stdout.write(`\r${(f / fps).toFixed(0)}s / ${duration}s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('\nvideo ->', out);

  if (audio) {
    const withVoice = out.replace(/\.mp4$/, '-voice.mp4');
    const r = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', out, '-i', path.resolve(audio),
      '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
      '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11,apad', '-shortest', withVoice], { stdio: 'inherit' });
    console.log(r.status === 0 ? 'video + voice -> ' + withVoice : 'audio mux failed');
  }
})();
