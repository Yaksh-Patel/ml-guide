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

// snapshot NOW -- navigating away below deactivates this section
const snap = {
  attentionActive: d.querySelector('#sec-attention')?.classList.contains('active'),
  homeInactive:    !d.querySelector('#sec-home')?.classList.contains('active'),
  pagerLinks:      q('#sec-attention .pager-link'),
  tocEntries:      q('#toc a[data-toc]'),
};

// the previously-unreachable topic
await window.nav('bipartite');
await new Promise(r => setTimeout(r, 400));
console.log('\nafter nav("bipartite"):  loaded =', d.querySelector('#sec-bipartite') ? 'yes' : 'NO',
            '| title =', JSON.stringify(txt('#tb-title')));

console.log('\nerrors:', errors.length ? errors : 'none');

// ---- assertions: this is what makes the smoke test a gate, not a report ----
const checks = [];
const check = (name, cond, got) => checks.push({ name, ok: !!cond, got });

check('sidebar items === manifest total', q('.sb-item') === TOTAL, q('.sb-item'));
check('home cards === manifest total',    q('.ht')      === TOTAL, q('.ht'));
check('topic-map nodes === manifest total', q('.tmap-node') === TOTAL, q('.tmap-node'));
check('sidebar groups === manifest groups', q('.sb-grp') === GROUPS.length, q('.sb-grp'));
check('home section rendered', d.querySelector('#sec-home'));
check('app globals present',
  ['nav','runCode','resetCode','resetProgress','updateProgressUI']
    .every(k => typeof window[k] === 'function'));
check('nav("attention") loaded + active', snap.attentionActive, snap.attentionActive);
check('home deactivated after nav', snap.homeInactive, snap.homeInactive);
check('pager rendered', snap.pagerLinks === 2, snap.pagerLinks);
check('toc populated', snap.tocEntries > 0, snap.tocEntries);
check('nav("bipartite") loaded', d.querySelector('#sec-bipartite'));
check('no console/jsdom errors', errors.length === 0, errors.length);

// every topic in the manifest must have a file whose section id matches it --
// the invariant the router depends on, checked for all of them, not just two
const manifestProblems = [];
for (const t of TOPICS) {
  const f = path.join(ROOT, t.file);
  if (!fs.existsSync(f)) { manifestProblems.push(`${t.id}: missing ${t.file}`); continue; }
  const src = fs.readFileSync(f, 'utf8');
  if (!new RegExp(`id="sec-${t.id}"`).test(src))
    manifestProblems.push(`${t.id}: ${t.file} has no id="sec-${t.id}"`);
}
check('every manifest topic resolves to a matching section id',
      manifestProblems.length === 0, manifestProblems.slice(0, 5));

console.log('\n---- checks ----');
for (const c of checks)
  console.log(`  ${c.ok ? 'PASS' : 'FAIL'}  ${c.name}${c.ok ? '' : '   got: ' + JSON.stringify(c.got)}`);
const failed = checks.filter(c => !c.ok).length;
console.log(`\n${checks.length - failed}/${checks.length} checks passed`);
process.exit(failed ? 1 : 0);
