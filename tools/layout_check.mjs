// layout_check.mjs: real-browser layout assertions for ML Atlas.
//
// jsdom (smoke.mjs) applies no stylesheets and has no layout, so it cannot see
// sideways scrolling, content sliding under the "on this page" rail, or text
// columns that are too wide. This drives the installed Chrome via
// puppeteer-core and measures the rendered page.
//
//   node layout_check.mjs <repo> [--shots DIR] [--expect-fail A3,A4]
//                                [--pages id,id] [--widths 390,1440]
//
// Assertions (run on every page × width × theme):
//   A1  no sideways scroll: documentElement.scrollWidth <= innerWidth
//   A2  "on this page" rail never overlaps topic content: every content
//       element's visible right edge sits >= MIN_TOC_CLEARANCE px left of it
//   A3  prose (p, li outside wide blocks) is <= PROSE_W px wide, and wide
//       blocks are no wider than the article column
//   A4  rail visible at >= TOC_MIN_W, hidden below it, with a .toc-dropdown
//       in the top bar instead
//
// --expect-fail lists assertions that are known to fail today (CI keeps going).
// If an expected failure passes in *every* case it is reported as XPASS and the
// run fails: take it off the list. A list that can only grow is not a check.
//
// Install outside the repo, like the other .mjs tools:
//   cd /tmp/domtest && npm i puppeteer-core && cp <repo>/tools/layout_check.mjs .

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import puppeteer from 'puppeteer-core';

// ---- design contract (keep in step with docs/visual-revamp/PLAN.md §2 D1) --
const PROSE_W = 720;            // max text column width
const TOC_MIN_W = 1280;         // viewport width from which the rail shows
const MIN_TOC_CLEARANCE = 24;   // px between content and the rail, at least
const TOL = 1;                  // sub-pixel rounding

// ---- args -------------------------------------------------------------------
const argv = process.argv.slice(2);
const ROOT = path.resolve(argv.find(a => !a.startsWith('--')) || '.');
const opt = (name, dflt) => {
  const i = argv.indexOf('--' + name);
  return i >= 0 ? argv[i + 1] : dflt;
};
const SHOTS = opt('shots', null);
const EXPECT_FAIL = new Set((opt('expect-fail', '') || '').split(',').filter(Boolean));
const PAGES = (opt('pages', 'home,linalg,biasvar,confusion,dtree,attention,rag,mlops')).split(',');
const WIDTHS = (opt('widths', '390,768,1280,1440,1728,2560')).split(',').map(Number);
const THEMES = ['light', 'dark'];
const HEIGHT = 900;

if (!fs.existsSync(path.join(ROOT, 'index.html'))) {
  console.error(`not the repo root (no index.html): ${ROOT}`);
  process.exit(2);
}
if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });

// ---- static server over the repo ----------------------------------------------
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.css': 'text/css', '.svg': 'image/svg+xml', '.json': 'application/json',
  '.png': 'image/png', '.ico': 'image/x-icon', '.woff2': 'font/woff2',
};
const server = http.createServer((req, res) => {
  let rel = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (rel.endsWith('/')) rel += 'index.html';
  const file = path.join(ROOT, path.normalize(rel));
  if (!file.startsWith(ROOT + path.sep) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    res.writeHead(404); res.end(); return;
  }
  res.writeHead(200, { 'content-type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const BASE = `http://127.0.0.1:${server.address().port}/`;

// ---- browser -------------------------------------------------------------------------
const CHROME = process.env.CHROME_PATH || [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium',
].find(p => fs.existsSync(p));
if (!CHROME) { console.error('no Chrome found; set CHROME_PATH'); process.exit(2); }

const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: true,
  args: ['--no-sandbox', '--hide-scrollbars', '--font-render-hinting=none'],
});

// ---- measurement, runs inside the page -------------------------------------------------
function measure({ PROSE_W, TOC_MIN_W, MIN_TOC_CLEARANCE, TOL, isHome, deviceWidth }) {
  const out = { A1: [], A2: [], A3: [], A4: [] };
  // Judge against the device width we asked for, not innerWidth: under mobile
  // emulation Chrome zooms out to fit over-wide content, which inflates
  // innerWidth to match it and hides the very overflow A1 looks for.
  const vw = deviceWidth;
  const label = el => {
    const cls = typeof el.className === 'string' && el.className.trim()
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    const txt = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    return `${el.tagName.toLowerCase()}${cls}${txt ? ` "${txt}"` : ''}`;
  };
  const visible = el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return false;
    const cs = getComputedStyle(el);
    return cs.display !== 'none' && cs.visibility !== 'hidden';
  };
  // Right edge of what the reader actually sees: clipped by any ancestor that
  // scrolls or hides overflow sideways (a wide table inside a scroller is fine).
  const visibleRight = el => {
    let right = el.getBoundingClientRect().right;
    for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
      const ox = getComputedStyle(a).overflowX;
      if (ox !== 'visible') right = Math.min(right, a.getBoundingClientRect().right);
    }
    return right;
  };

  // A1 sideways scroll
  const sw = Math.max(document.documentElement.scrollWidth, window.innerWidth);
  if (sw > vw + TOL) out.A1.push(`page is ${sw}px wide on a ${vw}px screen`);

  if (isHome) return out;

  const container = document.querySelector('#topic-container');
  const section = document.querySelector('.section.active');
  if (!container || !section) { out.A2.push('no active topic section'); return out; }

  const WIDE = '.anim-wrap, .tbl, .g2, .g3, .code-runner, .cgrid, table, pre, .katex-display, .formula, .math-formula, .formula-block';

  // A2 rail overlap
  const toc = document.querySelector('#toc');
  const tocShown = toc && visible(toc) && toc.children.length > 0;
  if (tocShown) {
    const tocLeft = toc.getBoundingClientRect().left;
    let worst = null;
    for (const el of section.querySelectorAll('*')) {
      if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') continue; // SVG children ignore clipPath
      if (!visible(el)) continue;
      const gap = tocLeft - visibleRight(el);
      if (gap < MIN_TOC_CLEARANCE - TOL && (!worst || gap < worst.gap)) worst = { gap, el };
    }
    if (worst) out.A2.push(`content ${Math.round(worst.gap)}px from rail (need ${MIN_TOC_CLEARANCE}): ${label(worst.el)}`);
  }

  // A3 prose width, wide-block width
  let widestProse = null;
  for (const el of section.querySelectorAll('p, li')) {
    if (el.closest(WIDE) || !visible(el)) continue;
    const w = el.getBoundingClientRect().width;
    if (w > PROSE_W + TOL && (!widestProse || w > widestProse.w)) widestProse = { w, el };
  }
  if (widestProse) out.A3.push(`prose ${Math.round(widestProse.w)}px > ${PROSE_W}: ${label(widestProse.el)}`);
  const colW = container.getBoundingClientRect().width;
  for (const el of section.querySelectorAll('.anim-wrap, .g2, .g3, .code-runner, .cgrid')) {
    if (!visible(el)) continue;
    const w = el.getBoundingClientRect().width;
    if (w > colW + TOL) { out.A3.push(`wide block ${Math.round(w)}px > column ${Math.round(colW)}: ${label(el)}`); break; }
  }

  // A4 rail vs dropdown by width
  const hasHeadings = section.querySelector('.card-title, h2, h3');
  if (hasHeadings) {
    const dd = document.querySelector('.toc-dropdown');
    const ddShown = dd && visible(dd);
    if (vw >= TOC_MIN_W && !tocShown) out.A4.push(`rail hidden at ${vw}px (should show from ${TOC_MIN_W})`);
    if (vw < TOC_MIN_W && tocShown) out.A4.push(`rail shown at ${vw}px (should hide below ${TOC_MIN_W})`);
    if (vw < TOC_MIN_W && !ddShown) out.A4.push(`no .toc-dropdown at ${vw}px`);
  }
  return out;
}

// ---- run -----------------------------------------------------------------------------
const results = [];   // { a: assertion, caseName, msg }
const ran = new Set();
let cases = 0;

for (const theme of THEMES) {
  for (const width of WIDTHS) {
    const page = await browser.newPage();
    const pageErrors = [];
    page.on('pageerror', e => pageErrors.push(e.message));
    await page.setViewport({ width, height: HEIGHT, isMobile: width < 800, hasTouch: width < 800, deviceScaleFactor: 1 });
    await page.evaluateOnNewDocument(t => {
      try { localStorage.setItem('ml-guide-theme', t); } catch {}
    }, theme);

    for (const id of PAGES) {
      const isHome = id === 'home';
      const caseName = `${id} @${width} ${theme}`;
      cases++;
      await page.goto(BASE + (isHome ? '' : '#' + id), { waitUntil: 'networkidle2', timeout: 30000 }).catch(() => {});
      await page.waitForSelector(`#sec-${id}.active`, { timeout: 15000 }).catch(() => {});
      await page.evaluate(() => document.fonts && document.fonts.ready);
      // Topic changes are same-document hash navigations, so scroll position
      // carries over from the previous page unless reset.
      await page.evaluate(() => window.scrollTo(0, 0));
      await new Promise(r => setTimeout(r, 350));   // .section.active fade-in

      const out = await page.evaluate(measure, { PROSE_W, TOC_MIN_W, MIN_TOC_CLEARANCE, TOL, isHome, deviceWidth: width });
      for (const [a, msgs] of Object.entries(out)) {
        if (isHome && a !== 'A1') continue;
        ran.add(a);
        msgs.forEach(msg => results.push({ a, caseName, msg }));
      }

      if (SHOTS) {
        const base = `${id}-${width}-${theme}`;
        await page.screenshot({ path: path.join(SHOTS, `${base}-top.png`) });
        if (!isHome) {
          await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight * 0.4));
          await new Promise(r => setTimeout(r, 200));
          await page.screenshot({ path: path.join(SHOTS, `${base}-mid.png`) });
        }
      }
    }
    if (pageErrors.length) results.push({ a: 'JS', caseName: `@${width} ${theme}`, msg: [...new Set(pageErrors)].join(' | ') });
    await page.close();
  }
}

await browser.close();
server.close();

// ---- report --------------------------------------------------------------------------
let hardFail = false;
for (const a of ['A1', 'A2', 'A3', 'A4', 'JS']) {
  const rows = results.filter(r => r.a === a);
  const xf = EXPECT_FAIL.has(a);
  if (rows.length) {
    console.log(`\n${xf ? 'XFAIL' : 'FAIL '} ${a}: ${rows.length} case(s)`);
    rows.slice(0, 12).forEach(r => console.log(`   ${r.caseName.padEnd(26)} ${r.msg}`));
    if (rows.length > 12) console.log(`   … ${rows.length - 12} more`);
    if (!xf) hardFail = true;
  } else if (xf && ran.has(a)) {
    console.log(`\nXPASS ${a}: listed in --expect-fail but passes everywhere; remove it from the list`);
    hardFail = true;
  } else if (ran.has(a)) {
    console.log(`ok    ${a}`);
  }
}
console.log(`\n${cases} cases (${PAGES.length} pages × ${WIDTHS.length} widths × ${THEMES.length} themes)` +
  (SHOTS ? `, screenshots in ${SHOTS}` : ''));
console.log(hardFail ? 'layout_check: FAILED' : 'layout_check: passed');
process.exit(hardFail ? 1 : 0);
