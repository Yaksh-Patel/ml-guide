import { JSDOM, VirtualConsole } from 'jsdom';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.argv[2];
const errors = [];
const vc = new VirtualConsole();
vc.on('jsdomError', e => errors.push('jsdomError: ' + (e.message || e)));
vc.on('error', (...a) => errors.push('console.error: ' + a.join(' ')));

const dom = new JSDOM(fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8'), {
  runScripts: 'dangerously',
  url: 'http://localhost/ml-guide/',
  virtualConsole: vc,
  pretendToBeVisual: true,
});
const { window } = dom;

// serve local files for fetch(); block anything remote (fonts/CDNs)
window.fetch = async (url) => {
  const u = String(url);
  if (/^https?:/.test(u)) return { ok: false, status: 0, text: async () => '' };
  const p = path.join(ROOT, u.replace(/^\.?\//, '').split('?')[0]);
  if (!fs.existsSync(p)) return { ok: false, status: 404, text: async () => '' };
  return { ok: true, status: 200, text: async () => fs.readFileSync(p, 'utf8') };
};
window.requestIdleCallback = undefined;   // don't kick off the 55-file index

// hand-run the module graph: jsdom does not execute type="module"
const { GROUPS, TOPICS, TOTAL } = await import(path.join(ROOT, 'assets/js/topics.js'));
globalThis.window = window;
globalThis.document = window.document;
globalThis.localStorage = window.localStorage;
globalThis.location = window.location;
globalThis.history = window.history;
globalThis.IntersectionObserver = class { observe(){} disconnect(){} unobserve(){} };
globalThis.requestIdleCallback = undefined;
globalThis.confirm = () => false;
const mm = (q) => ({ matches: false, media: q, addEventListener(){}, removeEventListener(){}, addListener(){}, removeListener(){} });
window.matchMedia = window.matchMedia || mm;
globalThis.matchMedia = mm;
globalThis.fetch = window.fetch;
// jsdom implements neither of these
window.Element.prototype.scrollIntoView = function () {};
window.scrollTo = () => {};

await import(path.join(ROOT, 'assets/js/app.js'));
await new Promise(r => setTimeout(r, 700));

const d = window.document;
const q = s => d.querySelectorAll(s).length;
const txt = s => (d.querySelector(s)?.textContent || '').trim();

console.log('manifest      :', TOTAL, 'topics /', GROUPS.length, 'groups');
console.log('sidebar groups:', q('.sb-grp'));
console.log('sidebar items :', q('.sb-item'), '(expect', TOTAL + ')');
console.log('home cards    :', q('.ht'), '(expect', TOTAL + ')');
console.log('topic-map     :', q('.tmap-node'), 'nodes /', q('.tmap-row'), 'rows');
console.log('home rendered :', q('#sec-home') ? 'yes' : 'NO');
console.log('home active   :', d.querySelector('#sec-home')?.classList.contains('active') ? 'yes' : 'NO');
console.log('topbar title  :', JSON.stringify(txt('#tb-title')));
console.log('progress label:', JSON.stringify(txt('#progress-label')));
console.log('grp counts    :', [...d.querySelectorAll('.grp-count')].map(e => e.textContent).join(' '));
console.log('globals       :', ['nav','runCode','resetCode','resetProgress','updateProgressUI']
  .map(k => typeof window[k] === 'function' ? k : k + '=MISSING').join(' '));

// navigate to a real topic
await window.nav('attention');
await new Promise(r => setTimeout(r, 500));
console.log('\nafter nav("attention"):');
console.log('  section loaded :', d.querySelector('#sec-attention') ? 'yes' : 'NO');
console.log('  is active      :', d.querySelector('#sec-attention')?.classList.contains('active') ? 'yes' : 'NO');
console.log('  home inactive  :', !d.querySelector('#sec-home')?.classList.contains('active') ? 'yes' : 'NO');
console.log('  topbar         :', JSON.stringify(txt('#tb-title')), '/', JSON.stringify(txt('#tb-crumb')));
console.log('  sidebar active :', txt('.sb-item.active'));
console.log('  pager links    :', q('#sec-attention .pager-link'), JSON.stringify([...d.querySelectorAll('#sec-attention .pager-name')].map(e=>e.textContent)));
console.log('  toc entries    :', q('#toc a[data-toc]'));
console.log('  read btn       :', txt('#tb-read-btn'), '/ hidden =', d.querySelector('#tb-read-btn')?.hidden);
console.log('  hash           :', window.location.hash);

// the previously-unreachable topic
await window.nav('bipartite');
await new Promise(r => setTimeout(r, 400));
console.log('\nafter nav("bipartite"):  loaded =', d.querySelector('#sec-bipartite') ? 'yes' : 'NO',
            '| title =', JSON.stringify(txt('#tb-title')));

console.log('\nerrors:', errors.length ? errors : 'none');
