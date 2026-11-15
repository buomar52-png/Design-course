// Sample a reel project's GSAP timeline into per-element channels for Lottie export.
//   node bake.js <project-dir> [--fps 30]   -> <dir>/output/bake.json  (then: python3 build_lottie.py <dir>)
//
// Units follow the template conventions:
//   text : .w  .reveal  .u            box : #bg-grid #bg-a #bg-b  .dot b  .dot i  .card  .ubox
//   svg  : svg.usvg  path.upath  path.draw (stroke drawn on -> Lottie trim path)
//   extras: .hl highlight bar, .who green bullet, .clipwin overflow window
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
const dir = path.resolve(args[0] && !args[0].startsWith('--') ? args[0] : '.');
const fpsArg = args.indexOf('--fps');
const FPS = fpsArg >= 0 ? +args[fpsArg + 1] : 30;

const setup = () => {
  const TEXT = '.w, .reveal, .u', BOX = '#bg-grid, #bg-a, #bg-b, .dot b, .dot i, .card, .ubox', SVG = 'svg.usvg, path.upath, path.draw';
  const st = document.createElement('style');
  st.textContent = '.__rel{position:relative} .__mk{position:absolute;width:0;height:0;pointer-events:none}';
  document.head.appendChild(st);
  window.__SEL = { TEXT, BOX, SVG };
  window.__units = [...document.querySelectorAll([TEXT, BOX, SVG].join(','))]   // paint (document) order
    .filter(el => !(el.matches('path') && el.closest('svg.usvg')))              // paths of a usvg belong to it
    .map((el, i) => {
      const kind = el.matches(SVG) ? 'svg' : el.matches(TEXT) ? 'text' : 'box';
      const u = { i, kind, el };
      if (kind !== 'svg') {
        if (getComputedStyle(el).position === 'static') el.classList.add('__rel');
        u.mk = [[0, 0], [100, 0], [0, 100]].map(([x, y]) => {
          const m = document.createElement('span'); m.className = '__mk';
          m.style.left = x + 'px'; m.style.top = y + 'px'; el.appendChild(m); return m;
        });
      }
      return u;
    });
};

(async () => {
  const browser = await chromium.launch();
  const open = async () => {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
    page.on('pageerror', e => console.error('page error:', e.message));
    await page.goto('file://' + path.join(dir, 'index.html') + '?render');
    await page.evaluate(() => window.__ready);
    await page.waitForTimeout(300);
    await page.evaluate(setup);
    return page;
  };

  // ---- pass 1: static layout (all animated props cleared; transforms don't affect layout) ----
  let page = await open();
  const statics = await page.evaluate(() => {
    const { TEXT } = window.__SEL;
    const units = window.__units;
    gsap.set([...document.querySelectorAll('#stage *')].filter(e => !e.classList.contains('__mk')),
      { clearProps: 'transform,opacity,visibility,filter,clipPath,backgroundSize,strokeDashoffset,textShadow' });
    // re-apply layout-only sets the template relies on
    document.querySelectorAll('[data-xpercent]').forEach(e => gsap.set(e, { xPercent: +e.dataset.xpercent, yPercent: +(e.dataset.ypercent || 0) }));
    const rgba = c => { const m = c.match(/[\d.]+/g).map(Number); return [m[0] / 255, m[1] / 255, m[2] / 255, m.length > 3 ? m[3] : 1]; };
    return units.map(u => {
      const el = u.el, cs = getComputedStyle(el);
      const o = { i: u.i, kind: u.kind, id: el.id || '', cls: String(el.className.baseVal ?? el.className) };
      const p0 = u.mk ? u.mk[0].getBoundingClientRect() : null;
      const rel = r => [r.left - p0.left, r.top - p0.top, r.width, r.height];
      if (u.kind !== 'svg') { o.origin = [p0.left, p0.top]; o.rect = rel(el.getBoundingClientRect()); }
      if (u.kind === 'text') {
        o.runs = [];
        const grab = e => { if (e.classList && e.classList.contains('hl')) o.hl = { id: e.id, rect: rel(e.getBoundingClientRect()) }; };
        grab(el);
        const walk = n => n.childNodes.forEach(c => {
          if (c.nodeType === 3) {
            if (!c.textContent.trim()) return;
            const rg = document.createRange(); rg.selectNodeContents(c);
            const pc = getComputedStyle(c.parentElement);
            o.runs.push({ text: c.textContent, size: parseFloat(pc.fontSize), weight: +pc.fontWeight, color: rgba(pc.color), rect: rel(rg.getBoundingClientRect()) });
          } else if (c.nodeType === 1 && !c.classList.contains('__mk') && !c.matches(TEXT)) { grab(c); walk(c); }
        });
        walk(el);
        if (el.matches('.who')) o.whoDot = true;
        const win = el.closest('.clipwin');
        if (win) { const b = win.getBoundingClientRect(); o.clipBox = [b.left, b.top, b.width, b.height]; }
      } else if (u.kind === 'box') {
        o.bg = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' ? rgba(cs.backgroundColor) : null;
        o.radius = parseFloat(cs.borderTopLeftRadius) || 0;
        o.radiusIsCircle = cs.borderTopLeftRadius === '50%';
        o.isCard = el.matches('.card');
      } else {
        const paths = el.tagName === 'svg' ? [...el.querySelectorAll('path')] : [el];
        const sc = getComputedStyle(paths[0]);
        o.d = paths.map(p => p.getAttribute('d'));
        o.fill = sc.fill !== 'none' ? rgba(sc.fill) : null;
        o.stroke = sc.stroke !== 'none' ? rgba(sc.stroke) : null;
        o.strokeWidth = parseFloat(sc.strokeWidth);
        o.linecap = sc.strokeLinecap; o.linejoin = sc.strokeLinejoin;
        o.draw = el.matches('path.draw');
        o.dash = !o.draw && sc.strokeDasharray !== 'none' ? sc.strokeDasharray.split(/[ ,]+/).map(parseFloat) : null;
        if (o.draw) o.length = el.getTotalLength();
      }
      return o;
    });
  });
  await page.close();

  // ---- pass 2: fresh page, untouched timeline, same markers -> sample every frame ----
  page = await open();
  const duration = await page.evaluate(() => window.__duration);
  const frames = [];
  const N = Math.round(duration * FPS);
  for (let f = 0; f <= N; f++) {
    frames.push(await page.evaluate(t => {
      window.__seek(t);
      const op = el => { let o = 1; for (let e = el; e && e.id !== 'stage'; e = e.parentElement) {
        const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none') return 0; o *= +cs.opacity; } return o; };
      return window.__units.map(u => {
        const el = u.el, r = { o: op(el) };
        if (u.kind === 'svg') {
          const m = el.getScreenCTM(); r.m = [m.a, m.b, m.c, m.d, m.e, m.f];
          if (el.matches('path.draw')) r.dash = parseFloat(getComputedStyle(el).strokeDashoffset) || 0;
        } else {
          const p = u.mk.map(m => { const b = m.getBoundingClientRect(); return [b.left, b.top]; });
          r.m = [(p[1][0] - p[0][0]) / 100, (p[1][1] - p[0][1]) / 100, (p[2][0] - p[0][0]) / 100, (p[2][1] - p[0][1]) / 100, p[0][0], p[0][1]];
          const cp = getComputedStyle(el).clipPath;
          if (cp && cp !== 'none') { const v = cp.match(/inset\(([^)]*)\)/)[1].trim().split(/\s+/); r.clip = parseFloat(v[3] ?? v[1] ?? v[0]) || 0; }
          const hl = el.classList.contains('hl') ? el : el.querySelector('.hl');
          if (hl) r.hl = parseFloat(getComputedStyle(hl).backgroundSize.split(' ')[0]) || 0;
        }
        return r;
      });
    }, Math.min(f / FPS, duration)));
    if (f % FPS === 0) process.stdout.write(`\r${f / FPS}s / ${duration}s`);
  }
  fs.mkdirSync(path.join(dir, 'output'), { recursive: true });
  const scenes = await page.evaluate(() => window.__scenes || null);
  fs.writeFileSync(path.join(dir, 'output', 'bake.json'), JSON.stringify({ fps: FPS, duration, scenes, units: statics, frames }));
  await browser.close();
  console.log(`\nbaked ${statics.length} units x ${frames.length} frames -> output/bake.json`);
})();
