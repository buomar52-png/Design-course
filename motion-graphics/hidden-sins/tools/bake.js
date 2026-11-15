// Samples the GSAP timeline in index.html into per-element channels (tools/bake.json),
// which tools/build_lottie.py turns into Lottie. Usage: node tools/bake.js [--fps 30]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const root = path.resolve(__dirname, '..');
const fpsArg = process.argv.indexOf('--fps');
const FPS = fpsArg > 0 ? +process.argv[fpsArg + 1] : 30;

const setup = () => {
    const $$ = s => [...document.querySelectorAll(s)];
    const TEXT_UNITS = '.w, .reveal, .hw, #header .name, #count-roll span, #s2 .ref, #card .who, #card .src, #handle';
    const BOX_UNITS = '#bg-grid, #bg-a, #bg-b, .dot b, .dot i, #card, #header .bar';
    const SVG_UNITS = '#heart-dashed path, #heart-fill, #heart-line, #send';
    const units = [];
    const all = $$([TEXT_UNITS, BOX_UNITS, SVG_UNITS].join(','));   // document (paint) order
    const st = document.createElement('style');
    st.textContent = '.__rel{position:relative} .__mk{position:absolute;width:0;height:0;pointer-events:none}';
    document.head.appendChild(st);

    all.forEach((el, i) => {
      const kind = el.matches(SVG_UNITS) ? 'svg' : el.matches(TEXT_UNITS) ? 'text' : 'box';
      const u = { i, kind, id: el.id || '', cls: el.className.baseVal ?? el.className, el };
      if (kind !== 'svg') {
        if (getComputedStyle(el).position === 'static') el.classList.add('__rel');
        u.mk = [[0, 0], [100, 0], [0, 100]].map(([x, y]) => {
          const m = document.createElement('span'); m.className = '__mk';
          m.style.left = x + 'px'; m.style.top = y + 'px';
          // markers must be measured relative to the padding box origin
          el.appendChild(m); return m;
        });
      }
      units.push(u);
    });
    window.__units = units;
};

(async () => {
  const browser = await chromium.launch();
  const open = async () => {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
    await page.goto('file://' + path.join(root, 'index.html') + '?render');
    await page.evaluate(() => window.__ready);
    await page.waitForTimeout(300);
    await page.evaluate(setup);
    return page;
  };
  let page = await open();

  const statics = await page.evaluate(() => {
    const $$ = s => [...document.querySelectorAll(s)];
    const units = window.__units, all = units.map(u => u.el);

    // Neutralise every GSAP inline style -> pure layout state (transforms do not affect layout).
    gsap.set($$('#stage *').filter(e => !e.classList.contains('__mk')),
      { clearProps: 'transform,opacity,visibility,filter,clipPath,backgroundSize,strokeDashoffset,textShadow' });
    gsap.set('.hw', { xPercent: 50, yPercent: -50 });

    const rgba = c => { const m = c.match(/[\d.]+/g).map(Number); return [m[0] / 255, m[1] / 255, m[2] / 255, m.length > 3 ? m[3] : 1]; };
    const out = units.map(u => {
      const el = u.el, cs = getComputedStyle(el);
      const o = { i: u.i, kind: u.kind, id: u.id, cls: String(u.cls) };
      if (u.kind !== 'svg') {
        const p0 = u.mk[0].getBoundingClientRect();
        o.origin = [p0.left, p0.top];
        const r = el.getBoundingClientRect();
        o.rect = [r.left - p0.left, r.top - p0.top, r.width, r.height];
      }
      if (u.kind === 'text') {
        o.runs = [];
        const walk = n => {
          n.childNodes.forEach(c => {
            if (c.nodeType === 3) {
              if (!c.textContent.trim()) return;
              const rg = document.createRange(); rg.selectNodeContents(c);
              const rr = rg.getBoundingClientRect(), pc = getComputedStyle(c.parentElement);
              const p0 = u.mk[0].getBoundingClientRect();
              o.runs.push({ text: c.textContent, size: parseFloat(pc.fontSize), weight: +pc.fontWeight,
                color: rgba(pc.color), rect: [rr.left - p0.left, rr.top - p0.top, rr.width, rr.height] });
            } else if (c.nodeType === 1 && !c.classList.contains('__mk')) {
              if (c.classList.contains('hl')) {
                const rr = c.getBoundingClientRect(), p0 = u.mk[0].getBoundingClientRect();
                o.hl = { id: c.id, rect: [rr.left - p0.left, rr.top - p0.top, rr.width, rr.height] };
              }
              walk(c);
            }
          });
        };
        if (el.classList.contains('hl')) {
          const rr = el.getBoundingClientRect(), p0 = u.mk[0].getBoundingClientRect();
          o.hl = { id: el.id, rect: [rr.left - p0.left, rr.top - p0.top, rr.width, rr.height] };
        }
        walk(el);
        if (el.matches('#card .who')) o.whoDot = true;
        if (el.closest('#count-roll')) {
          const b = el.closest('.count').getBoundingClientRect();
          o.clipBox = [b.left, b.top, b.width, b.height];
        }
      } else if (u.kind === 'box') {
        o.bg = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' ? rgba(cs.backgroundColor) : null;
        o.radius = parseFloat(cs.borderTopLeftRadius) || 0;
        o.radiusIsCircle = cs.borderTopLeftRadius === '50%';
      } else {
        o.d = el.tagName === 'svg' ? [...el.querySelectorAll('path')].map(p => p.getAttribute('d')) : [el.getAttribute('d')];
        const ps = el.tagName === 'svg' ? el : el;
        const sc = getComputedStyle(ps);
        o.fill = sc.fill !== 'none' ? rgba(sc.fill) : null;
        o.stroke = sc.stroke !== 'none' ? rgba(sc.stroke) : null;
        o.strokeWidth = parseFloat(sc.strokeWidth);
        o.dash = sc.strokeDasharray !== 'none' && el.id !== 'heart-line' ? sc.strokeDasharray.split(/[ ,]+/).map(parseFloat) : null;
        o.linecap = sc.strokeLinecap; o.linejoin = sc.strokeLinejoin;
        if (el.id === 'heart-line') o.length = el.getTotalLength();
      }
      return o;
    });
    return out;
  });

  await page.close();
  page = await open();   // fresh page: untouched timeline, same markers
  const frames = [];
  const duration = await page.evaluate(() => window.__duration);
  const N = Math.round(duration * FPS);
  for (let f = 0; f <= N; f++) {
    const t = Math.min(f / FPS, duration);
    frames.push(await page.evaluate(t => {
      window.__seek(t);
      const op = el => { let o = 1; for (let e = el; e && e.id !== 'stage'; e = e.parentElement) {
        const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none') return 0; o *= +cs.opacity; } return o; };
      return window.__units.map(u => {
        const el = u.el, r = {};
        if (u.kind === 'svg') {
          const m = el.getScreenCTM(); r.m = [m.a, m.b, m.c, m.d, m.e, m.f];
          r.o = op(el.tagName === 'svg' ? el : el.ownerSVGElement) * +getComputedStyle(el).opacity;
          if (el.id === 'heart-line') r.dash = parseFloat(getComputedStyle(el).strokeDashoffset);
        } else {
          const p = u.mk.map(m => { const b = m.getBoundingClientRect(); return [b.left, b.top]; });
          r.m = [(p[1][0] - p[0][0]) / 100, (p[1][1] - p[0][1]) / 100, (p[2][0] - p[0][0]) / 100, (p[2][1] - p[0][1]) / 100, p[0][0], p[0][1]];
          r.o = op(el);
          const cs = getComputedStyle(el);
          if (cs.clipPath && cs.clipPath !== 'none') r.clip = parseFloat(cs.clipPath.match(/inset\(([^)]*)\)/)[1].split(/\s+/)[3]);
          const hl = el.classList.contains('hl') ? el : el.querySelector('.hl');
          if (hl) r.hl = parseFloat(getComputedStyle(hl).backgroundSize.split(' ')[0]);
        }
        return r;
      });
    }, t));
    if (f % FPS === 0) process.stdout.write(`\r${f / FPS}s`);
  }
  await browser.close();
  fs.writeFileSync(path.join(__dirname, 'bake.json'), JSON.stringify({ fps: FPS, duration, units: statics, frames }));
  console.log('\nbaked', statics.length, 'units,', frames.length, 'frames');
})();
