/* ==========================================================
   app.js — router, generated navigation, search, progress.

   Everything structural is derived from topics.js, so adding a
   topic never means editing markup in more than one place.
   ========================================================== */

import { GROUPS, TOPICS, BY_ID, ORDER, TOTAL, HOME } from './topics.js';
import { renderMath, highlight, looksLikeMath, loadCodeMirror, loadPyodide_, prefetch } from './lazy.js';

const PROGRESS_KEY = 'ml-guide-progress-v2';   // same key as before: progress carries over
const THEME_KEY    = 'ml-guide-theme';
const SIDEBAR_KEY  = 'ml-guide-sb';
const GROUP_KEY    = id => 'ml-grp-' + id;

const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

const store = {
  get(k, fallback = null) { try { return localStorage.getItem(k) ?? fallback; } catch { return fallback; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch {} },
  json(k, fallback) { try { return JSON.parse(localStorage.getItem(k) || '') ?? fallback; } catch { return fallback; } },
};

/* ═══════════════ PROGRESS ═══════════════ */

const getProgress = () => store.json(PROGRESS_KEY, {}) || {};
const isRead = id => !!getProgress()[id];

function setRead(id, done) {
  const p = getProgress();
  if (done) p[id] = Date.now(); else delete p[id];
  store.set(PROGRESS_KEY, JSON.stringify(p));
  paintProgress();
}

function resetProgress() {
  if (!confirm('Clear reading progress for all topics?')) return;
  store.set(PROGRESS_KEY, '{}');
  paintProgress();
}

function paintProgress() {
  const p = getProgress();
  const done = ORDER.filter(id => p[id]).length;
  const pct = Math.round((done / TOTAL) * 100);

  $$('.sb-item[data-topic-id]').forEach(el => el.classList.toggle('sb-read', !!p[el.dataset.topicId]));
  $$('.ht[data-topic-id]').forEach(el => el.classList.toggle('ht-read', !!p[el.dataset.topicId]));
  $$('.tmap-node[data-topic-id]').forEach(el => el.classList.toggle('tmap-read', !!p[el.dataset.topicId]));

  const bar = $('#progress-bar-fill');   if (bar) bar.style.width = pct + '%';
  const lab = $('#progress-label');      if (lab) lab.textContent = `${done} / ${TOTAL} read`;
  const hp  = $('#home-pct');            if (hp) hp.textContent = pct + '%';
  const hb  = $('#home-progress-fill');  if (hb) hb.style.width = pct + '%';
  const hpl = $('.home-pct-label');      if (hpl) hpl.textContent = pct + '%';
  const hbi = $('.home-progress-bar-inner'); if (hbi) hbi.style.width = pct + '%';
  const hpi = $('#home-progress-count'); if (hpi) hpi.textContent = `${done} of ${TOTAL} topics`;

  // per-group counts in the sidebar
  GROUPS.forEach(g => {
    const el = $(`.sb-gl[data-grp-id="${g.id}"] .grp-count`);
    if (el) el.textContent = `${g.topics.filter(t => p[t.id]).length}/${g.topics.length}`;
  });

  updateReadButton(current);
}

/* ═══════════════ SIDEBAR (generated) ═══════════════ */

function buildSidebar() {
  const mount = $('#sb-groups');
  if (!mount) return;
  mount.innerHTML = GROUPS.map(g => `
    <div class="sb-grp" data-grp="${g.id}">
      <button class="sb-gl" data-grp-id="${g.id}" aria-expanded="true">
        <span class="grp-icon">${g.icon}</span>
        <span class="grp-name">${g.label}</span>
        <span class="grp-count"></span>
        <svg class="grp-arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>
      </button>
      <div class="sb-items">
        ${g.topics.map(t => `
          <a class="sb-item" href="#${t.id}" data-topic-id="${t.id}">
            <span class="n">${t.num}</span>
            <span class="sb-label">${t.short}</span>
            ${t.badge === 'new' ? '<span class="sb-new">new</span>' : ''}
            ${t.badge === 'coming' ? '<span class="sb-coming">soon</span>' : ''}
            <span class="read-dot" aria-hidden="true"></span>
          </a>`).join('')}
      </div>
    </div>`).join('');

  // restore collapsed groups
  GROUPS.forEach(g => {
    if (store.get(GROUP_KEY(g.id)) === '1') {
      const grp = $(`.sb-grp[data-grp="${g.id}"]`);
      grp?.classList.add('grp-collapsed');
      $('.sb-gl', grp)?.setAttribute('aria-expanded', 'false');
    }
  });

  mount.addEventListener('click', e => {
    const gl = e.target.closest('.sb-gl');
    if (gl) {
      const grp = gl.closest('.sb-grp');
      const collapsed = grp.classList.toggle('grp-collapsed');
      gl.setAttribute('aria-expanded', String(!collapsed));
      store.set(GROUP_KEY(gl.dataset.grpId), collapsed ? '1' : '0');
    }
  });

  // hover prefetch: warm the fragment before the click lands
  mount.addEventListener('pointerover', e => {
    const item = e.target.closest('.sb-item');
    if (item) prefetch(BY_ID[item.dataset.topicId]?.file);
  }, { passive: true });
}

function setAllGroups(collapsed) {
  $$('.sb-grp').forEach(grp => {
    grp.classList.toggle('grp-collapsed', collapsed);
    $('.sb-gl', grp)?.setAttribute('aria-expanded', String(!collapsed));
    store.set(GROUP_KEY(grp.dataset.grp), collapsed ? '1' : '0');
  });
}

/* ═══════════════ HOME (generated from the manifest) ═══════════════ */

function buildHome() {
  const grid = $('#home-grid-mount');
  if (grid && !grid.dataset.built) {
    grid.dataset.built = '1';
    grid.innerHTML = GROUPS.map(g => `
      <div class="grp-label">${g.icon} ${g.label}</div>
      <div class="home-grid">
        ${g.topics.map(t => `
          <a class="ht" href="#${t.id}" data-topic-id="${t.id}">
            <div class="ht-header">
              <span class="hn">${t.num}</span>
              <span class="htime">${t.time} min</span>
            </div>
            <div class="hname">${t.title}</div>
            ${t.blurb ? `<div class="hsub">${t.blurb}</div>` : ''}
            ${t.prereqs.length
              ? `<div class="hpre">after ${t.prereqs.map(p => BY_ID[p]?.short || p).join(', ')}</div>`
              : ''}
            ${t.badge === 'new' ? '<div class="hbadges"><span class="hnew">new</span></div>' : ''}
          </a>`).join('')}
      </div>`).join('');
  }

  const map = $('#topic-map-mount');
  if (map && !map.dataset.built) {
    map.dataset.built = '1';
    map.innerHTML = GROUPS.map(g => `
      <div class="tmap-row">
        <div class="tmap-label">${g.label}</div>
        <div class="tmap-nodes">
          ${g.topics.map(t =>
            `<a class="tmap-node tn-${g.id}" href="#${t.id}" data-topic-id="${t.id}" title="${t.title}">${t.num}</a>`
          ).join('')}
        </div>
      </div>`).join('');
  }
}

/* ═══════════════ SEARCH ═══════════════ */
/* The old build only indexed topics you had already opened, so search
   was empty on a fresh visit. The index is now built from every topic,
   fetched in parallel — but not until you actually search, or the
   browser goes idle. */

const index = new Map();
let indexing = null;

function buildIndex() {
  if (indexing) return indexing;
  indexing = (async () => {
    const results = await Promise.allSettled(TOPICS.map(async t => {
      const res = await fetch(t.file);
      if (!res.ok) throw new Error(String(res.status));
      const tmp = document.createElement('div');
      tmp.innerHTML = await res.text();
      tmp.querySelectorAll('script,svg,style').forEach(n => n.remove());
      index.set(t.id, (tmp.textContent || '').replace(/\s+/g, ' ').trim().toLowerCase());
    }));
    return results.filter(r => r.status === 'fulfilled').length;
  })();
  return indexing;
}

function search(q) {
  const ql = q.trim().toLowerCase();
  if (ql.length < 2) return [];
  const out = [];
  for (const t of TOPICS) {
    const title = (t.title + ' ' + t.short + ' ' + t.groupLabel).toLowerCase();
    const inTitle = title.includes(ql);
    const body = index.get(t.id) || '';
    const at = body.indexOf(ql);
    if (!inTitle && at < 0) continue;
    let snippet = '';
    if (at >= 0) {
      const s = Math.max(0, at - 50), e = Math.min(body.length, at + ql.length + 90);
      snippet = (s > 0 ? '…' : '') + body.slice(s, e).trim() + (e < body.length ? '…' : '');
    }
    out.push({ t, snippet, score: (inTitle ? 100 : 0) + (at >= 0 ? 10 : 0) });
  }
  return out.sort((a, b) => b.score - a.score).slice(0, 12);
}

let paletteOpen = false;
let paletteSel = 0;
let paletteResults = [];

function openPalette(seed = '') {
  paletteOpen = true;
  const p = $('#palette');
  p.hidden = false;
  document.body.classList.add('palette-open');
  const input = $('#palette-input');
  input.value = seed;
  input.focus();
  renderPalette(seed);
  buildIndex().then(() => { if (paletteOpen) renderPalette($('#palette-input').value); });
}

function closePalette() {
  paletteOpen = false;
  $('#palette').hidden = true;
  document.body.classList.remove('palette-open');
}

function renderPalette(q) {
  const list = $('#palette-list');
  const hint = $('#palette-hint');
  paletteResults = q.trim().length >= 2
    ? search(q)
    : TOPICS.filter(t => !isRead(t.id)).slice(0, 8).map(t => ({ t, snippet: '', score: 0 }));
  paletteSel = 0;

  hint.textContent = q.trim().length >= 2
    ? `${paletteResults.length} result${paletteResults.length === 1 ? '' : 's'}`
    : 'Up next';

  if (!paletteResults.length) {
    list.innerHTML = `<div class="pal-empty">Nothing matches “${escapeHtml(q)}”.</div>`;
    return;
  }

  list.innerHTML = paletteResults.map((r, i) => `
    <a class="pal-item${i === 0 ? ' sel' : ''}" href="#${r.t.id}" data-i="${i}">
      <span class="pal-num">${r.t.num}</span>
      <span class="pal-body">
        <span class="pal-title">${mark(r.t.title, q)}</span>
        <span class="pal-meta">${r.t.groupIcon} ${r.t.groupLabel} · ${r.t.time} min${isRead(r.t.id) ? ' · read' : ''}</span>
        ${r.snippet ? `<span class="pal-snippet">${mark(r.snippet, q)}</span>` : ''}
      </span>
    </a>`).join('');
}

function movePalette(delta) {
  if (!paletteResults.length) return;
  paletteSel = (paletteSel + delta + paletteResults.length) % paletteResults.length;
  $$('.pal-item').forEach((el, i) => el.classList.toggle('sel', i === paletteSel));
  $$('.pal-item')[paletteSel]?.scrollIntoView({ block: 'nearest' });
}

const escapeHtml = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function mark(text, q) {
  const safe = escapeHtml(text);
  const ql = q.trim();
  if (ql.length < 2) return safe;
  return safe.replace(new RegExp(ql.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), m => `<mark>${m}</mark>`);
}

/* ═══════════════ TOC (per topic, from card titles) ═══════════════ */

let tocObserver = null;

function buildToc(section) {
  const rail = $('#toc');
  if (!rail) return;
  if (tocObserver) { tocObserver.disconnect(); tocObserver = null; }

  const titles = $$(':scope > .card > .card-title, :scope > .g2 > .card > .card-title, :scope > .anim-wrap > .anim-title', section);
  if (titles.length < 4) { rail.hidden = true; rail.innerHTML = ''; return; }

  titles.forEach((el, i) => {
    const host = el.closest('.card, .anim-wrap');
    if (host && !host.id) host.id = 'x-' + section.id + '-' + i;
  });

  rail.hidden = false;
  rail.innerHTML = `
    <div class="toc-label">On this page</div>
    <nav class="toc-list">
      ${titles.map((el, i) => {
        const host = el.closest('.card, .anim-wrap');
        return `<a href="#${host.id}" data-toc="${host.id}">${escapeHtml(el.textContent.trim())}</a>`;
      }).join('')}
    </nav>`;

  // scroll-spy
  const links = new Map($$('a[data-toc]', rail).map(a => [a.dataset.toc, a]));
  tocObserver = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        links.forEach(a => a.classList.remove('active'));
        links.get(en.target.id)?.classList.add('active');
      }
    });
  }, { rootMargin: '-72px 0px -70% 0px' });
  titles.forEach(el => {
    const host = el.closest('.card, .anim-wrap');
    if (host) tocObserver.observe(host);
  });

  rail.onclick = e => {
    const a = e.target.closest('a[data-toc]');
    if (!a) return;
    e.preventDefault();
    document.getElementById(a.dataset.toc)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };
}

/* ═══════════════ ROUTER ═══════════════ */

const loaded = new Set();
let current = null;

async function loadTopic(id) {
  if (loaded.has(id)) return;
  const meta = id === 'home' ? HOME : BY_ID[id];
  const container = $('#topic-container');
  try {
    const res = await fetch(meta.file);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const html = await res.text();
    container.insertAdjacentHTML('beforeend', html);
    loaded.add(id);

    const section = document.getElementById('sec-' + id);
    if (!section) return;

    // insertAdjacentHTML never executes <script>; the interactive
    // diagrams in a handful of topics need theirs to run.
    $$('script', section).forEach(old => {
      const s = document.createElement('script');
      [...old.attributes].forEach(a => s.setAttribute(a.name, a.value));
      s.textContent = old.textContent;
      old.replaceWith(s);
    });

    if (id === 'home') buildHome();

    // Progressive enhancement, deliberately NOT awaited: the topic must be
    // readable the moment its HTML lands. Waiting on KaTeX or Prism here
    // would put a third-party CDN in front of the content.
    enhance(section, html);
  } catch (err) {
    container.insertAdjacentHTML('beforeend', `
      <section class="section" id="sec-${id}">
        <div class="sec-title">${escapeHtml(meta?.title || id)}</div>
        <div class="sec-desc">This topic could not be loaded. It may still be in progress.</div>
        <div class="card ca"><div class="card-title">Not available yet</div>
        <div class="card-body">Use the sidebar to explore the other topics.</div></div>
      </section>`);
    loaded.add(id);
  }
}

/* Syntax highlighting, maths and editors are applied after the topic is
   already on screen. Each is independently lazy and independently failable. */
function enhance(section, html) {
  highlight(section).catch(() => {});
  if (looksLikeMath(html)) renderMath(section).catch(() => {});
  if (section.querySelector('.code-runner')) initRunners(section);
}

async function go(id, { push = true, scroll = true } = {}) {
  if (id !== 'home' && !BY_ID[id]) id = 'home';
  current = id;

  await loadTopic(id);

  $$('.section.active').forEach(s => s.classList.remove('active'));
  const section = document.getElementById('sec-' + id);
  section?.classList.add('active');

  $$('.sb-item').forEach(i => i.classList.toggle('active', i.dataset.topicId === id));
  $(`.sb-item[data-topic-id="${id}"]`)?.scrollIntoView({ block: 'nearest' });

  paintTopbar(id);
  if (section) { buildToc(section); paintPager(id, section); }

  if (push && location.hash.slice(1) !== id) history.pushState({ id }, '', '#' + id);
  if (scroll) window.scrollTo({ top: 0, behavior: 'instant' in window ? 'instant' : 'auto' });

  $('#sidebar')?.classList.remove('open');
  paintProgress();

  // warm the next topic while the reader is busy with this one
  const next = ORDER[ORDER.indexOf(id) + 1];
  if (next) prefetch(BY_ID[next].file);
}

function paintTopbar(id) {
  const t = id === 'home' ? null : BY_ID[id];
  $('#tb-crumb').textContent = t ? `${t.groupIcon} ${t.groupLabel}` : 'Start here';
  $('#tb-title').textContent = t ? t.title : 'Home';
  $('#tb-time').textContent  = t ? `${t.time} min` : `${TOTAL} topics`;
  const home = $('#tb-home-btn');
  if (home) home.hidden = id === 'home';
}

function paintPager(id, section) {
  let pager = $('.pager', section);
  if (!pager) {
    pager = document.createElement('nav');
    pager.className = 'pager';
    section.appendChild(pager);
  }
  const i = ORDER.indexOf(id);
  const prev = i > 0 ? BY_ID[ORDER[i - 1]] : null;
  const next = i >= 0 && i < ORDER.length - 1 ? BY_ID[ORDER[i + 1]] : (i < 0 ? BY_ID[ORDER[0]] : null);
  pager.innerHTML = `
    ${prev ? `<a class="pager-link prev" href="#${prev.id}"><span class="pager-dir">← Previous</span><span class="pager-name">${escapeHtml(prev.title)}</span></a>` : '<span></span>'}
    ${next ? `<a class="pager-link next" href="#${next.id}"><span class="pager-dir">Next →</span><span class="pager-name">${escapeHtml(next.title)}</span></a>` : '<span></span>'}`;
}

function updateReadButton(id) {
  const btn = $('#tb-read-btn');
  if (!btn) return;
  const valid = id && id !== 'home' && BY_ID[id];
  btn.hidden = !valid;
  if (!valid) return;
  const read = isRead(id);
  btn.textContent = read ? '✓ Read' : 'Mark read';
  btn.classList.toggle('tb-read-done', read);
  btn.onclick = () => setRead(id, !isRead(id));
}

/* ═══════════════ CODE RUNNERS ═══════════════ */

function initRunners(section) {
  $$('.code-input', section).forEach(ta => {
    if (!ta.hasAttribute('data-original')) ta.setAttribute('data-original', ta.value);
  });
  loadCodeMirror().catch(() => {});
}

async function runCode(runnerId) {
  const runner = document.getElementById(runnerId);
  if (!runner) return;
  const out = runner.querySelector('.code-output');
  const btn = runner.querySelector('.run-btn');
  const ta  = runner.querySelector('.code-input');
  const cm  = window.__cmEditors?.[runnerId];
  const code = cm ? cm.state.doc.toString() : ta.value;

  const label = btn.textContent;
  btn.disabled = true;
  out.textContent = '';
  out.className = 'code-output';

  try {
    const pkgs = (runner.dataset.packages ?? 'numpy')
      .split(',').map(x => x.trim()).filter(Boolean);
    const py = await loadPyodide_(msg => { btn.textContent = msg; }, pkgs);
    btn.textContent = 'Running…';
    py.runPython('import sys, io\nsys.stdout = io.StringIO()\nsys.stderr = sys.stdout');
    let err = null;
    try { await py.runPythonAsync(code); } catch (e) { err = e.message || String(e); }
    const stdout = py.runPython('sys.stdout.getvalue()');
    out.textContent = err ? `${stdout}\n${err}` : (stdout || 'Ran successfully (no output)');
    out.classList.add(err ? 'err' : 'ok');
  } catch {
    out.textContent = 'Python runtime unavailable — try this in Jupyter or Colab.';
    out.classList.add('err');
  } finally {
    btn.disabled = false;
    btn.textContent = label;
  }
}

function resetCode(runnerId) {
  const runner = document.getElementById(runnerId);
  if (!runner) return;
  const ta = runner.querySelector('.code-input');
  const original = ta?.getAttribute('data-original') || '';
  const cm = window.__cmEditors?.[runnerId];
  if (cm) cm.dispatch({ changes: { from: 0, to: cm.state.doc.length, insert: original } });
  else if (ta) ta.value = original;
  const out = runner.querySelector('.code-output');
  if (out) { out.textContent = ''; out.className = 'code-output'; }
}

/* ═══════════════ THEME / CHROME ═══════════════ */

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const use = $('#theme-icon use');
  if (use) use.setAttribute('href', theme === 'dark' ? '#i-sun' : '#i-moon');
  window.__cmSyncTheme?.();
  if (window.Prism?.highlightAll) window.Prism.highlightAll();
}

function toggleTheme() {
  const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  store.set(THEME_KEY, next);
  applyTheme(next);
}

function toggleSidebar() {
  const collapsed = $('#sidebar').classList.toggle('sb-collapsed');
  document.body.classList.toggle('sb-is-collapsed', collapsed);
  store.set(SIDEBAR_KEY, collapsed ? '1' : '0');
}

const toggleMobileSidebar = () => $('#sidebar').classList.toggle('open');

/* Thin scroll-progress line under the topbar. */
function initScrollProgress() {
  const bar = $('#read-progress');
  if (!bar) return;
  const paint = () => {
    const h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = `scaleX(${h > 0 ? Math.min(1, window.scrollY / h) : 0})`;
  };
  paint();
  window.addEventListener('scroll', paint, { passive: true });
  window.addEventListener('resize', paint);
}

/* ═══════════════ BOOT ═══════════════ */

function initKeys() {
  document.addEventListener('keydown', e => {
    const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) || e.target.isContentEditable;

    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault(); paletteOpen ? closePalette() : openPalette();
      return;
    }
    if (paletteOpen) {
      if (e.key === 'Escape') { e.preventDefault(); closePalette(); }
      else if (e.key === 'ArrowDown') { e.preventDefault(); movePalette(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); movePalette(-1); }
      else if (e.key === 'Enter') {
        e.preventDefault();
        const r = paletteResults[paletteSel];
        if (r) { closePalette(); go(r.t.id); }
      }
      return;
    }
    if (typing) return;

    const i = ORDER.indexOf(current);
    if (e.key === '/') { e.preventDefault(); openPalette(); }
    else if (e.key === 'ArrowRight' || e.key === 'j') { if (i < ORDER.length - 1) go(ORDER[i + 1]); }
    else if (e.key === 'ArrowLeft' || e.key === 'k') { if (i > 0) go(ORDER[i - 1]); }
    else if (e.key === 'h') go('home');
    else if (e.key === 'm' && current && current !== 'home') setRead(current, !isRead(current));
    else if (e.key === '?') openPalette('');
  });
}

function initChrome() {
  $('#sb-expand-all')?.addEventListener('click', () => setAllGroups(false));
  $('#sb-collapse-all')?.addEventListener('click', () => setAllGroups(true));
  $('#sb-toggle')?.addEventListener('click', toggleSidebar);
  $('#sb-expand-btn')?.addEventListener('click', toggleSidebar);
  $('#theme-toggle')?.addEventListener('click', toggleTheme);
  $('#mob-tog')?.addEventListener('click', toggleMobileSidebar);
  $('.mob-overlay')?.addEventListener('click', toggleMobileSidebar);
  $('#tb-home-btn')?.addEventListener('click', () => go('home'));
  $('#search-trigger')?.addEventListener('click', () => openPalette());
  $('#palette-backdrop')?.addEventListener('click', closePalette);

  const input = $('#palette-input');
  input?.addEventListener('input', () => renderPalette(input.value));
  $('#palette-list')?.addEventListener('click', e => {
    const a = e.target.closest('.pal-item');
    if (!a) return;
    e.preventDefault();
    const r = paletteResults[+a.dataset.i];
    closePalette();
    if (r) go(r.t.id);
  });

  if (store.get(SIDEBAR_KEY) === '1') {
    $('#sidebar').classList.add('sb-collapsed');
    document.body.classList.add('sb-is-collapsed');
  }

  // one delegated handler for every in-app link, sidebar/home/map/pager alike
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (!a || a.dataset.toc) return;
    const id = a.getAttribute('href').slice(1);
    if (id !== 'home' && !BY_ID[id]) return;
    e.preventDefault();
    go(id);
  });
}

window.addEventListener('popstate', e => {
  const id = e.state?.id || location.hash.slice(1) || 'home';
  go(id, { push: false });
});

function boot() {
  buildSidebar();
  initChrome();
  initKeys();
  initScrollProgress();
  applyTheme(document.documentElement.getAttribute('data-theme') || 'dark');
  go(location.hash.slice(1) || 'home', { push: false });

  // Build the search index when the browser is idle, so the first
  // Ctrl+K is instant without costing anything on first paint.
  const idle = window.requestIdleCallback || (fn => setTimeout(fn, 4000));
  idle(() => buildIndex());
}

document.readyState === 'loading'
  ? document.addEventListener('DOMContentLoaded', boot)
  : boot();

/* Legacy globals: topic HTML calls nav(...) in 114 places, plus a few
   diagrams call runCode/resetCode/updateProgressUI. Keep them working. */
window.nav = (id) => go(id);
window.runCode = runCode;
window.resetCode = resetCode;
window.resetProgress = resetProgress;
window.updateProgressUI = paintProgress;
window.toggleTheme = toggleTheme;
window.toggleSidebar = toggleSidebar;
window.toggleMobileSidebar = toggleMobileSidebar;
