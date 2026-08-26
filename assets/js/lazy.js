/* ==========================================================
   lazy.js — on-demand loaders for the heavy third-party deps.

   Why this file exists: the previous build loaded KaTeX, four
   Prism scripts, CodeMirror and *Pyodide* on every page view.
   Pyodide alone pulls a multi-megabyte WASM runtime plus numpy
   and scikit-learn via micropip — and only 2 of 55 topics have
   a code runner. Everything here is fetched the first time it
   is actually needed, once, and cached in a promise.
   ========================================================== */

const KATEX_VER   = '0.16.10';
const PRISM_VER   = '1.29.0';
const PYODIDE_VER = 'v0.25.1';

const cache = new Map();

/* Load a script/stylesheet once; repeat calls return the same promise. */
function once(key, fn) {
  if (!cache.has(key)) cache.set(key, fn());
  return cache.get(key);
}

function loadScript(src, { module = false } = {}) {
  return new Promise((resolve, reject) => {
    const s = document.createElement('script');
    s.src = src;
    if (module) s.type = 'module';
    s.onload = resolve;
    s.onerror = () => reject(new Error('Failed to load ' + src));
    document.head.appendChild(s);
  });
}

function loadCSS(href) {
  return new Promise((resolve) => {
    const l = document.createElement('link');
    l.rel = 'stylesheet';
    l.href = href;
    l.onload = l.onerror = resolve;   // never block rendering on a stylesheet
    document.head.appendChild(l);
  });
}

/* ---- KaTeX --------------------------------------------------------- */
const MATH_DELIMS = [
  { left: '$$', right: '$$', display: true },
  { left: '$',  right: '$',  display: false },
];

/* Cheap pre-check: only pull ~300KB of KaTeX if the fragment plausibly
   contains math. Two dollar signs on one line is the signal. */
export function looksLikeMath(html) {
  return /\$[^$\n]{1,200}\$/.test(html);
}

const loadKatex = () => once('katex', async () => {
  await Promise.all([
    loadCSS(`https://cdn.jsdelivr.net/npm/katex@${KATEX_VER}/dist/katex.min.css`),
    loadScript(`https://cdn.jsdelivr.net/npm/katex@${KATEX_VER}/dist/katex.min.js`),
  ]);
  await loadScript(`https://cdn.jsdelivr.net/npm/katex@${KATEX_VER}/dist/contrib/auto-render.min.js`);
});

export async function renderMath(el) {
  if (!el) return;
  try {
    await loadKatex();
    if (window.renderMathInElement) {
      window.renderMathInElement(el, { delimiters: MATH_DELIMS, throwOnError: false });
    }
  } catch (e) { /* math just stays as source text */ }
}

/* ---- Prism --------------------------------------------------------- */
const loadPrism = () => once('prism', async () => {
  await loadCSS('assets/prism-theme.css');
  await loadScript(`https://cdn.jsdelivr.net/npm/prismjs@${PRISM_VER}/prism.min.js`);
  window.Prism = window.Prism || {};
  window.Prism.manual = true;
  await Promise.all([
    loadScript(`https://cdn.jsdelivr.net/npm/prismjs@${PRISM_VER}/components/prism-python.min.js`),
    loadScript(`https://cdn.jsdelivr.net/npm/prismjs@${PRISM_VER}/components/prism-sql.min.js`),
  ]);
});

export async function highlight(el) {
  if (!el || !el.querySelector('[class*="language-"]')) return;
  try {
    await loadPrism();
    if (window.Prism?.highlightAllUnder) window.Prism.highlightAllUnder(el);
  } catch (e) { /* code stays unhighlighted */ }
}

/* ---- CodeMirror ---------------------------------------------------- */
export function loadCodeMirror() {
  return once('cm', () => loadScript('assets/codemirror-init.js', { module: true }));
}

/* ---- Pyodide ------------------------------------------------------- */
/* Reports progress so a multi-megabyte download isn't a frozen button. */
export function loadPyodide_(onStatus = () => {}) {
  return once('pyodide', async () => {
    onStatus('Loading Python runtime…');
    await loadScript(`https://cdn.jsdelivr.net/pyodide/${PYODIDE_VER}/full/pyodide.js`);

    onStatus('Starting interpreter…');
    const py = await window.loadPyodide({
      indexURL: `https://cdn.jsdelivr.net/pyodide/${PYODIDE_VER}/full/`,
    });

    onStatus('Loading numpy…');
    await py.loadPackage(['numpy', 'micropip']);

    onStatus('Loading scikit-learn…');
    await py.runPythonAsync('import micropip\nawait micropip.install(["scikit-learn"])');

    return py;
  });
}

/* ---- Prefetch ------------------------------------------------------ */
/* Warm the HTTP cache for a topic fragment without parsing it. */
const prefetched = new Set();
export function prefetch(url) {
  if (!url || prefetched.has(url)) return;
  prefetched.add(url);
  const l = document.createElement('link');
  l.rel = 'prefetch';
  l.href = url;
  l.as = 'fetch';
  document.head.appendChild(l);
}
