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
const LAST_KEY     = 'ml-guide-last';            // last topic opened, for home "Continue reading"

const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

/* Motion (PLAN D7) is an enhancement only: content is visible by default, and
   none of it runs under prefers-reduced-motion or without IntersectionObserver. */
const MOTION = typeof window.matchMedia === 'function'
  && !window.matchMedia('(prefers-reduced-motion: reduce)').matches
  && 'IntersectionObserver' in window;

/* A sprite icon (index.html). `id` is a <symbol> id such as a group's `icon`. */
const ico = (id, cls = '') => `<svg class="ico${cls ? ' ' + cls : ''}" aria-hidden="true"><use href="#${id}"/></svg>`;

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
  const hpl = $('.home-pct-label');      if (hpl) hpl.textContent = pct + '%';
  const hpi = $('#home-progress-count'); if (hpi) hpi.textContent = `${done} of ${TOTAL} topics`;
  const arc = $('#home-ring-arc');       // r = 21, so the circumference is 2π·21
  if (arc) arc.style.strokeDashoffset = String(2 * Math.PI * 21 * (1 - done / TOTAL));

  // per-group progress on home: grid headers and map rows
  GROUPS.forEach(g => {
    const n = g.topics.filter(t => p[t.id]).length, of = g.topics.length;
    const hg = $(`.home-grp[data-group="${g.id}"]`);
    if (hg) {
      $('.hg-count', hg).textContent = `${n} / ${of} read`;
      $('.hg-fill', hg).style.width = (n / of * 100) + '%';
    }
    const row = $(`.tmap-row[data-group="${g.id}"] .tmap-count`);
    if (row) row.textContent = `${n}/${of}`;
  });
  paintContinue(p);

  // per-group progress in the sidebar: a small bar plus the count
  GROUPS.forEach(g => {
    const gl = $(`.sb-gl[data-grp-id="${g.id}"]`);
    if (!gl) return;
    const n = g.topics.filter(t => p[t.id]).length, of = g.topics.length;
    $('.grp-count', gl).textContent = `${n} of ${of} read`;
    $('.grp-prog-fill', gl).style.width = (n / of * 100) + '%';
    gl.title = `${g.label}: ${n} of ${of} read`;
  });

  updateReadButton(current);
}

/* ═══════════════ SIDEBAR (generated) ═══════════════ */

function buildSidebar() {
  const mount = $('#sb-groups');
  if (!mount) return;
  mount.innerHTML = GROUPS.map(g => `
    <div class="sb-grp" data-grp="${g.id}" data-group="${g.id}">
      <button class="sb-gl" data-grp-id="${g.id}" aria-expanded="true">
        ${ico(g.icon, 'grp-icon')}
        <span class="grp-name">${g.label}<span class="grp-prog" aria-hidden="true"><span class="grp-prog-fill"></span></span></span>
        <span class="grp-count sr-only"></span>
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

  // open the group of the topic in the URL now, not after it loads (no jump)
  paintGroups(BY_ID[location.hash.slice(1)]?.group ?? null);

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

/* Which groups are open. A group the reader toggled by hand keeps that state
   (GROUP_KEY: '1' collapsed, '0' open). Every other group is collapsed unless it
   holds the current topic. The current topic's group is always opened on
   arrival, so the active entry is never hidden; that is not stored. */
function paintGroups(currentGroup) {
  $$('.sb-grp').forEach(grp => {
    const saved = store.get(GROUP_KEY(grp.dataset.grp));
    const isCur = grp.dataset.grp === currentGroup;
    const collapsed = isCur ? false : saved !== null ? saved === '1' : true;
    grp.classList.toggle('grp-collapsed', collapsed);
    grp.classList.toggle('grp-current', isCur);
    $('.sb-gl', grp)?.setAttribute('aria-expanded', String(!collapsed));
  });
}

function setAllGroups(collapsed) {
  $$('.sb-grp').forEach(grp => {
    grp.classList.toggle('grp-collapsed', collapsed);
    $('.sb-gl', grp)?.setAttribute('aria-expanded', String(!collapsed));
    store.set(GROUP_KEY(grp.dataset.grp), collapsed ? '1' : '0');
  });
}

/* ═══════════════ HOME (generated from the manifest) ═══════════════ */

/* Hero art: a small feed-forward network whose edges carry signals left to
   right. Plain SVG; style.css §7 animates .hn-sig and .hn-glow and stops
   both under prefers-reduced-motion. Seeded, so it is the same every visit. */
function heroNetwork() {
  const layers = [3, 5, 5, 2], W = 400, H = 300, xs = [44, 152, 260, 360];
  let seed = 7;
  const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const nodes = layers.map((n, li) => Array.from({ length: n }, (_, i) =>
    ({ x: xs[li], y: H / 2 + (i - (n - 1) / 2) * (li === 0 || li === 3 ? 70 : 52) })));
  let edges = '', sigs = '';
  for (let li = 0; li < layers.length - 1; li++) {
    for (const a of nodes[li]) for (const b of nodes[li + 1]) {
      const d = `M${a.x} ${a.y}L${b.x} ${b.y}`;
      edges += `<path class="hn-edge" d="${d}"/>`;
      if (rnd() < .42) {
        const delay = (li * .7 + rnd() * 2.2).toFixed(2);
        sigs += `<path class="hn-sig hn-c${Math.floor(rnd() * 3)}" d="${d}" pathLength="100" style="animation-delay:${delay}s"/>`;
      }
    }
  }
  const dots = nodes.map((col, li) => col.map(n => {
    const r = li === layers.length - 1 ? 10 : 8;
    const delay = (li * .7 + .5 + rnd() * .6).toFixed(2);
    return `<g${li === layers.length - 1 ? ' class="hn-out"' : ''}>
      <circle class="hn-ring" cx="${n.x}" cy="${n.y}" r="${r}"/>
      <circle class="hn-glow" cx="${n.x}" cy="${n.y}" r="${r - 3.5}" style="animation-delay:${delay}s"/></g>`;
  }).join('')).join('');
  return `<svg class="hero-net" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet">
    <g>${edges}</g><g>${sigs}</g><g>${dots}</g></svg>`;
}

function buildHome() {
  const art = $('#home-hero-art');
  if (art && !art.dataset.built) { art.dataset.built = '1'; art.innerHTML = heroNetwork(); }

  const grid = $('#home-grid-mount');
  if (grid && !grid.dataset.built) {
    grid.dataset.built = '1';
    grid.innerHTML = GROUPS.map(g => `
      <div class="home-grp" data-group="${g.id}">
        <div class="grp-label">
          ${ico(g.icon)}<span class="hg-name">${g.label}</span>
          <span class="hg-count"></span>
          <span class="hg-bar" aria-hidden="true"><span class="hg-fill"></span></span>
        </div>
        <div class="home-grid">
          ${g.topics.map((t, i) => `
            <a class="ht" href="#${t.id}" data-topic-id="${t.id}" style="--i:${i}">
              <div class="ht-header">
                <span class="hn">${t.num}</span>
                <span class="htime">${t.time} min</span>
                <span class="ht-check" title="Read"><svg aria-hidden="true"><use href="#i-check"/></svg></span>
              </div>
              <div class="hname">${t.title}</div>
              ${t.blurb ? `<div class="hsub">${t.blurb}</div>` : ''}
              ${t.prereqs.length
                ? `<div class="hpre">After ${t.prereqs.map(p => BY_ID[p]?.short || p).join(', ')}</div>`
                : ''}
              ${t.badge === 'new' ? '<div class="hbadges"><span class="hnew">new</span></div>' : ''}
            </a>`).join('')}
        </div>
      </div>`).join('');
  }

  // Learning path: one line per group, one stop per topic, filled when read.
  const map = $('#topic-map-mount');
  if (map && !map.dataset.built) {
    map.dataset.built = '1';
    map.innerHTML = GROUPS.map(g => `
      <div class="tmap-row" data-group="${g.id}">
        <div class="tmap-label">${ico(g.icon)}<span class="tmap-name">${g.label}</span><span class="tmap-count"></span></div>
        <div class="tmap-nodes">
          ${g.topics.map(t =>
            `<a class="tmap-node" href="#${t.id}" data-topic-id="${t.id}" data-title="${t.title}" aria-label="${t.num} ${t.title}" style="--i:${ORDER.indexOf(t.id)}"><span>${t.num}</span></a>`
          ).join('')}
        </div>
      </div>`).join('');
  }
}

/* Home "Continue reading": the last topic opened if it is unread, else the
   next unread topic after it, else the first unread topic. */
function paintContinue(p = getProgress()) {
  const link = $('#home-continue-link');
  if (!link) return;
  const saved = store.get(LAST_KEY);
  const last = BY_ID[saved] ? saved : null;
  const unreadAfter = from => {
    const i = ORDER.indexOf(from);
    for (let k = 1; k <= TOTAL; k++) { const id = ORDER[(i + k) % TOTAL]; if (!p[id]) return id; }
    return null;
  };
  let id, kicker;
  if (last && !p[last]) { id = last; kicker = 'Continue reading'; }
  else if (last)        { id = unreadAfter(last); kicker = 'Up next'; }
  else                  { id = ORDER.find(x => !p[x]); kicker = 'Start here'; }
  if (!id) { id = last || ORDER[0]; kicker = `All ${TOTAL} read · revisit`; }
  const t = BY_ID[id];
  $('#home-continue-kicker').textContent = kicker;
  link.href = '#' + id;
  link.dataset.group = t.group;
  link.innerHTML = `<span class="hc-num">${t.num}</span>${t.title}`;
  const btn = $('#home-continue-btn'); if (btn) btn.href = '#' + id;
}

/* ═══════════════ MOTION ═══════════════ */

/* Blocks below the fold fade and rise once as they enter the viewport.
   Only blocks that start below the fold get .rv, so the first screen never
   waits; .rv hides nothing until JS has added it (style.css §2). */
let revealIO = null;
function reveal(section) {
  if (!MOTION || !section) return;
  revealIO ??= new IntersectionObserver(entries => entries.forEach(en => {
    if (!en.isIntersecting) return;
    en.target.classList.add('rv-in');
    revealIO.unobserve(en.target);
  }), { rootMargin: '0px 0px -6% 0px' });
  const sel = section.id === 'sec-home'
    ? ':scope > :is(.home-continue, .topic-map, .home-h), :scope > #home-grid-mount > .home-grp'
    : ':scope > :not(script, style, .pager)';
  const fold = window.innerHeight;
  $$(sel, section).forEach(el => {
    if (el.classList.contains('rv-in') || el.getBoundingClientRect().top < fold) return;
    el.classList.add('rv');
    revealIO.observe(el);
  });
}

/* Home on arrival: the ring fills and its number counts up, and read stops
   on the learning path fill in reading order (style.css §7, .tmap-anim). */
function homeEntrance() {
  if (!MOTION) return;
  const p = getProgress();
  const done = ORDER.filter(id => p[id]).length, pct = Math.round(done / TOTAL * 100);
  const C = 2 * Math.PI * 21;
  const arc = $('#home-ring-arc');
  if (arc) {
    arc.style.transition = 'none';
    arc.style.strokeDashoffset = String(C);
    arc.getBoundingClientRect();
    arc.style.transition = '';
    arc.style.strokeDashoffset = String(C * (1 - done / TOTAL));
  }
  const label = $('.home-pct-label');
  if (label && pct > 0) {
    const t0 = performance.now();
    const step = now => {
      const k = Math.min(1, (now - t0) / 800), e = 1 - Math.pow(1 - k, 3);
      label.textContent = Math.round(pct * e) + '%';
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }
  const map = $('#topic-map-mount');
  if (map) { map.classList.remove('tmap-anim'); void map.offsetWidth; map.classList.add('tmap-anim'); }
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
        <span class="pal-meta">${ico(r.t.groupIcon)} ${r.t.groupLabel} · ${r.t.time} min${isRead(r.t.id) ? ' · read' : ''}</span>
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
  const dd = $('#toc-dd');
  if (!rail) return;
  if (tocObserver) { tocObserver.disconnect(); tocObserver = null; }
  if (dd) dd.open = false;

  const titles = $$(':scope > .card > .card-title, :scope > .g2 > .card > .card-title, :scope > .anim-wrap > .anim-title', section);
  if (titles.length < 4) {
    rail.hidden = true; rail.innerHTML = '';
    if (dd) { dd.hidden = true; $('.toc-dd-panel', dd).innerHTML = ''; }
    return;
  }

  titles.forEach((el, i) => {
    const host = el.closest('.card, .anim-wrap');
    if (host && !host.id) host.id = 'x-' + section.id + '-' + i;
  });

  // One list of links, rendered twice: the rail (>= 1280px) and the top-bar
  // dropdown (below). CSS decides which one is visible.
  const linksHtml = titles.map(el => {
    const host = el.closest('.card, .anim-wrap');
    return `<a href="#${host.id}" data-toc="${host.id}">${escapeHtml(el.textContent.trim())}</a>`;
  }).join('');

  rail.hidden = false;
  rail.innerHTML = `
    <div class="toc-label">On this page</div>
    <nav class="toc-list${MOTION ? ' has-marker' : ''}">${linksHtml}${MOTION ? '<span class="toc-marker" aria-hidden="true"></span>' : ''}</nav>`;
  // The active marker slides between entries instead of jumping.
  const marker = $('.toc-marker', rail);
  const moveMarker = id => {
    const a = $(`a[data-toc="${id}"]`, rail);
    if (!marker || !a) return;
    marker.style.transform = `translateY(${a.offsetTop}px)`;
    marker.style.height = a.offsetHeight + 'px';
    marker.classList.add('on');
  };
  if (dd) { dd.hidden = false; $('.toc-dd-panel', dd).innerHTML = linksHtml; }

  // scroll-spy, shared by both lists
  const allLinks = [...$$('a[data-toc]', rail), ...(dd ? $$('a[data-toc]', dd) : [])];
  tocObserver = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        allLinks.forEach(a => a.classList.toggle('active', a.dataset.toc === en.target.id));
        moveMarker(en.target.id);
      }
    });
  }, { rootMargin: '-72px 0px -70% 0px' });
  titles.forEach(el => {
    const host = el.closest('.card, .anim-wrap');
    if (host) tocObserver.observe(host);
  });
}

function jumpToc(e) {
  const a = e.target.closest('a[data-toc]');
  if (!a) return;
  e.preventDefault();
  const dd = $('#toc-dd');
  if (dd) dd.open = false;
  document.getElementById(a.dataset.toc)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function initToc() {
  $('#toc')?.addEventListener('click', jumpToc);
  const dd = $('#toc-dd');
  if (!dd) return;
  dd.addEventListener('click', jumpToc);
  // close on outside click and on Escape, like any menu
  document.addEventListener('click', e => { if (dd.open && !dd.contains(e.target)) dd.open = false; });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && dd.open) { dd.open = false; dd.querySelector('summary')?.focus(); }
  });
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
  if (looksLikeMath(html)) renderMath(section).then(() => scrollHints(section)).catch(() => {});
  scrollHints(section);
  if (section.querySelector('.code-runner')) initRunners(section);
}

/* Maths and tables that are wider than the column scroll sideways. Fade the
   edge that has more content behind it, so the scroll is discoverable
   (style.css .xs-l / .xs-r). Re-measured on resize. */
function scrollHints(root) {
  if (!root) return;
  $$('.katex-display, .tbl', root).forEach(el => {
    const paint = () => {
      const over = el.scrollWidth > el.clientWidth + 1;
      el.classList.toggle('xs-l', over && el.scrollLeft > 1);
      el.classList.toggle('xs-r', over && el.scrollLeft + el.clientWidth < el.scrollWidth - 1);
    };
    paint();
    if (!el.dataset.xs) { el.dataset.xs = '1'; el.addEventListener('scroll', paint, { passive: true }); }
  });
}
let xsTimer = 0;
window.addEventListener('resize', () => {
  clearTimeout(xsTimer);
  xsTimer = setTimeout(() => scrollHints($('.section.active')), 150);
});

async function go(id, { push = true, scroll = true } = {}) {
  if (id !== 'home' && !BY_ID[id]) id = 'home';
  current = id;

  await loadTopic(id);

  $$('.section.active').forEach(s => s.classList.remove('active'));
  const section = document.getElementById('sec-' + id);
  section?.classList.add('active');

  paintGroups(id === 'home' ? null : BY_ID[id].group);
  if (id !== 'home') store.set(LAST_KEY, id);
  $$('.sb-item').forEach(i => i.classList.toggle('active', i.dataset.topicId === id));
  $(`.sb-item[data-topic-id="${id}"]`)?.scrollIntoView({ block: 'nearest' });

  paintTopbar(id);
  if (section) { buildToc(section); paintPager(id, section); }

  if (push && location.hash.slice(1) !== id) history.pushState({ id }, '', '#' + id);
  if (scroll) window.scrollTo({ top: 0, behavior: 'instant' in window ? 'instant' : 'auto' });

  $('#sidebar')?.classList.remove('open');
  paintProgress();
  reveal(section);
  if (id === 'home') homeEntrance();

  // warm the next topic while the reader is busy with this one
  const next = ORDER[ORDER.indexOf(id) + 1];
  if (next) prefetch(BY_ID[next].file);
}

function paintTopbar(id) {
  const t = id === 'home' ? null : BY_ID[id];
  $('.main')?.setAttribute('data-group', t ? t.group : 'home');   // drives --grp (style.css §1)
  $('#tb-crumb').innerHTML = t ? `${ico(t.groupIcon)}${t.groupLabel}` : 'Start here';
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
  btn.innerHTML = `<svg><use href="#i-check"/></svg><span class="tb-lbl">${read ? 'Read' : 'Mark read'}</span>`;
  btn.title = read ? 'Read. Click to mark unread (m)' : 'Mark this topic read (m)';
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
  // In the phone/tablet drawer, "hide" closes the drawer; it must not collapse the desktop sidebar.
  if (window.matchMedia?.('(max-width: 768px)').matches) { $('#sidebar').classList.remove('open'); return; }
  const collapsed = $('#sidebar').classList.toggle('sb-collapsed');
  document.body.classList.toggle('sb-is-collapsed', collapsed);
  store.set(SIDEBAR_KEY, collapsed ? '1' : '0');
}

const toggleMobileSidebar = () => $('#sidebar').classList.toggle('open');
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && $('#sidebar')?.classList.contains('open')) { $('#sidebar').classList.remove('open'); $('#tb-menu')?.focus(); }
});

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
  $('#tb-menu')?.addEventListener('click', toggleMobileSidebar);
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
  initToc();
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
