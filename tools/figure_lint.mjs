// figure_lint.mjs: measure every diagram's text in a real browser.
//   node figure_lint.mjs <repo> [--only 01,06] [--json out.json] [--width 1440]
// Per figure (.anim-wrap > svg), in SVG user units:
//   CLIP     text whose box leaves the viewBox (it is cut off on screen)
//   OVERLAP  two text boxes that intersect (labels printed over each other)
//   SCALE    rendered px per user unit (text size = font-size × this)
// Exits 1 if any CLIP or OVERLAP is found.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
import puppeteer from 'puppeteer-core';
const argv = process.argv.slice(2);
const ROOT = path.resolve(argv.find(a => !a.startsWith('--')) || '.');
const opt = (n, d) => { const i = argv.indexOf('--' + n); return i >= 0 ? argv[i + 1] : d; };
const ONLY = opt('only', ''), JSON_OUT = opt('json', ''), W = +opt('width', '1440');
const T = { '.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml' };
const server = http.createServer((req, res) => { let rel = decodeURIComponent(new URL(req.url,'http://x').pathname); if (rel.endsWith('/')) rel += 'index.html';
  const f = path.join(ROOT, path.normalize(rel)); if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, {'content-type': T[path.extname(f)] || 'application/octet-stream'}); fs.createReadStream(f).pipe(res); });
await new Promise(r => server.listen(0, '127.0.0.1', r));
const BASE = `http://127.0.0.1:${server.address().port}/`;
const src = fs.readFileSync(path.join(ROOT, 'assets/js/topics.js'), 'utf8');
let ids = [...src.matchAll(/\{ id: '([^']+)', num: '(\d+)'/g)].map(m => [m[1], m[2]]);
if (ONLY) ids = ids.filter(([id, n]) => ONLY.split(',').includes(n) || ONLY.split(',').includes(id));
const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const page = await browser.newPage();
await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
await page.setViewport({ width: W, height: 1000 });
const all = [];
for (const [id, num] of ids) {
  await page.goto(BASE + '#' + id, { waitUntil: 'networkidle2' }).catch(() => {});
  await page.waitForSelector(`#sec-${id}.active`, { timeout: 15000 }).catch(() => {});
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 500));
  const figs = await page.evaluate(id => {
    const out = [];
    document.querySelectorAll(`#sec-${id} .anim-wrap`).forEach((wrap, fi) => {
      const svg = wrap.querySelector(':scope > svg') || wrap.querySelector('svg');
      if (!svg) return;
      const vb = svg.viewBox.baseVal; const has = vb && vb.width > 0;
      const r = svg.getBoundingClientRect();
      const scale = has ? Math.min(r.width / vb.width, r.height / vb.height) : 1;
      const texts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && getComputedStyle(t).display !== 'none');
      const boxes = texts.map(t => {
        // bbox in the svg's user space (account for transforms between text and svg)
        const b = t.getBBox(); const m = svg.getScreenCTM().inverse().multiply(t.getScreenCTM());
        const pts = [[b.x, b.y], [b.x + b.width, b.y], [b.x, b.y + b.height], [b.x + b.width, b.y + b.height]]
          .map(([x, y]) => [m.a * x + m.c * y + m.e, m.b * x + m.d * y + m.f]);
        const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
        return { s: t.textContent.trim().slice(0, 40), x0: Math.min(...xs), x1: Math.max(...xs), y0: Math.min(...ys), y1: Math.max(...ys) };
      });
      const clip = has ? boxes.filter(b => b.x0 < vb.x - 0.5 || b.x1 > vb.x + vb.width + 0.5 || b.y0 < vb.y - 0.5 || b.y1 > vb.y + vb.height + 0.5).map(b => b.s) : [];
      const over = [];
      const pad = 0.5;   // glyph boxes include line spacing; ignore hairline touches
      for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
        const a = boxes[i], b = boxes[j];
        const ix = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0), iy = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
        if (ix > pad && iy > Math.min(a.y1 - a.y0, b.y1 - b.y0) * 0.25) over.push(`${a.s} × ${b.s}`);
      }
      out.push({ fi, vb: has ? [vb.width, vb.height] : null, px: [Math.round(r.width), Math.round(r.height)], scale: +scale.toFixed(2),
        minFont: Math.min(...texts.map(t => parseFloat(getComputedStyle(t).fontSize) || 0)) * scale, clip, over, n: texts.length });
    });
    return out;
  }, id);
  for (const f of figs) all.push({ num, id, ...f });
}
await browser.close(); server.close();
let bad = 0;
for (const f of all) {
  const flag = f.clip.length || f.over.length; if (flag) bad++;
  console.log(`${f.num}-${f.fi} ${f.id.padEnd(14)} scale ${String(f.scale).padEnd(4)} min ${f.minFont.toFixed(1).padStart(4)}px  clip ${String(f.clip.length).padStart(2)}  overlap ${String(f.over.length).padStart(2)}` +
    (flag ? '   ' + [...f.clip.map(s => 'CLIP ' + s), ...f.over.slice(0, 3).map(s => 'OVER ' + s)].join(' | ').slice(0, 160) : ''));
}
const tc = all.reduce((a, f) => a + f.clip.length, 0), to = all.reduce((a, f) => a + f.over.length, 0);
console.log(`\n${all.length} figures, ${bad} with problems; ${tc} clipped labels, ${to} overlapping label pairs`);
if (JSON_OUT) fs.writeFileSync(JSON_OUT, JSON.stringify(all, null, 1));
process.exit(bad ? 1 : 0);
