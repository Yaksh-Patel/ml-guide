/* ==========================================================
   nav.js — ML/DS Guide: navigation, search, theme, Pyodide
   ========================================================== */

// ─── TOPIC REGISTRY ────────────────────────────────────────────
const TOPIC_FILES = {
  home:         'topics/00-home.html',
  linalg:       'topics/01-linear-algebra.html',
  prob:         'topics/02-probability.html',
  stats:        'topics/03-statistics.html',
  calc:         'topics/04-calculus.html',
  mlconcepts:   'topics/05-ml-paradigms.html',
  biasvar:      'topics/06-bias-variance.html',
  crossval:     'topics/07-cross-validation.html',
  metrics:      'topics/08-eval-metrics.html',
  confusion:    'topics/09-confusion-roc.html',
  calibration:  'topics/10-calibration-explainability.html',
  linlog:       'topics/11-linear-logistic.html',
  knn:          'topics/12-knn.html',
  naivebayes:   'topics/13-naive-bayes.html',
  svm:          'topics/14-svm.html',
  dtree:        'topics/15-decision-trees.html',
  rf:           'topics/16-random-forest.html',
  boosting:     'topics/17-gradient-boosting.html',
  xgb:          'topics/18-xgboost.html',
  clustering:   'topics/19-clustering.html',
  dimred:       'topics/20-dimensionality-reduction.html',
  featureeng:   'topics/21-feature-engineering.html',
  imbalanced:   'topics/22-imbalanced.html',
  reg:          'topics/23-regularization.html',
  hyperparam:   'topics/24-hyperparameter-tuning.html',
  ensemble:     'topics/25-ensemble-methods.html',
  nn_basics:    'topics/26-mlp.html',
  activations:  'topics/27-activations.html',
  loss:         'topics/28-loss-functions.html',
  backprop:     'topics/29-backpropagation.html',
  optim:        'topics/30-optimizers.html',
  weightinit:   'topics/31-weight-init.html',
  cnn:          'topics/32-cnns.html',
  rnn:          'topics/33-rnns-lstms.html',
  attention:    'topics/34-attention-architecture.html',
  transformers: 'topics/35-transformers.html',
  transfer:     'topics/36-transfer-distillation.html',
  tokenization: 'topics/37-tokenization-embeddings.html',
  bert:         'topics/38-bert.html',
  llm:          'topics/39-llms-rlhf.html',
  timeseries:   'topics/40-time-series.html',
  creditrisk:   'topics/41-credit-risk.html',
  mlops:        'topics/42-mlops.html',
  systemdesign: 'topics/43-system-design.html',
  coding:       'topics/44-python-sql-dsa.html',
  compare:      'topics/45-model-cheatsheet.html',
  gnns:         'topics/46-gnns.html',
  frameworks:   'topics/47-tf-keras-pytorch.html',
  rag:          'topics/48-rag.html',
  vectordb:     'topics/49-vector-databases.html',
  agents:       'topics/50-agentic-ai.html',
  responsibleai:'topics/51-responsible-ai.html',
  causal:       'topics/52-causal-inference.html',
  dataeng:      'topics/53-data-engineering.html',
  multimodal:   'topics/54-multimodal.html',
};

// ─── TOPIC METADATA (reading time, prereqs, section) ───────────
const TOPIC_META = {
  linalg:       { time: 12, prereqs: [],                              section: 'Math' },
  prob:         { time: 10, prereqs: ['linalg'],                      section: 'Math' },
  stats:        { time: 10, prereqs: ['prob'],                        section: 'Math' },
  calc:         { time: 12, prereqs: ['linalg'],                      section: 'Math' },
  mlconcepts:   { time: 8,  prereqs: ['stats'],                       section: 'ML Thinking' },
  biasvar:      { time: 8,  prereqs: ['mlconcepts'],                  section: 'ML Thinking' },
  crossval:     { time: 10, prereqs: ['biasvar'],                     section: 'ML Thinking' },
  metrics:      { time: 8,  prereqs: ['mlconcepts'],                  section: 'ML Thinking' },
  confusion:    { time: 8,  prereqs: ['metrics'],                     section: 'ML Thinking' },
  calibration:  { time: 10, prereqs: ['confusion'],                   section: 'ML Thinking' },
  linlog:       { time: 10, prereqs: ['calc','stats'],                section: 'Classical ML' },
  knn:          { time: 6,  prereqs: ['mlconcepts'],                  section: 'Classical ML' },
  naivebayes:   { time: 6,  prereqs: ['prob'],                        section: 'Classical ML' },
  svm:          { time: 12, prereqs: ['calc','linlog'],               section: 'Classical ML' },
  dtree:        { time: 8,  prereqs: ['mlconcepts'],                  section: 'Classical ML' },
  rf:           { time: 8,  prereqs: ['dtree'],                       section: 'Classical ML' },
  boosting:     { time: 10, prereqs: ['dtree','calc'],                section: 'Classical ML' },
  xgb:          { time: 12, prereqs: ['boosting'],                    section: 'Classical ML' },
  clustering:   { time: 10, prereqs: ['linalg','metrics'],            section: 'Classical ML' },
  dimred:       { time: 10, prereqs: ['linalg','prob'],               section: 'Classical ML' },
  featureeng:   { time: 10, prereqs: ['mlconcepts'],                  section: 'Data Eng' },
  imbalanced:   { time: 8,  prereqs: ['metrics','featureeng'],        section: 'Data Eng' },
  reg:          { time: 8,  prereqs: ['linlog','calc'],               section: 'Data Eng' },
  hyperparam:   { time: 8,  prereqs: ['biasvar','crossval'],          section: 'Data Eng' },
  ensemble:     { time: 8,  prereqs: ['dtree','rf'],                  section: 'Data Eng' },
  nn_basics:    { time: 12, prereqs: ['calc','linalg'],               section: 'Neural Nets' },
  activations:  { time: 8,  prereqs: ['nn_basics'],                   section: 'Neural Nets' },
  loss:         { time: 14, prereqs: ['nn_basics','prob'],            section: 'Neural Nets' },
  backprop:     { time: 18, prereqs: ['nn_basics','calc'],            section: 'Neural Nets' },
  optim:        { time: 10, prereqs: ['backprop'],                    section: 'Neural Nets' },
  weightinit:   { time: 6,  prereqs: ['nn_basics','calc'],            section: 'Neural Nets' },
  cnn:          { time: 14, prereqs: ['nn_basics','backprop'],        section: 'Deep Learning' },
  rnn:          { time: 12, prereqs: ['nn_basics','backprop'],        section: 'Deep Learning' },
  attention:    { time: 20, prereqs: ['rnn','linalg'],                section: 'Deep Learning' },
  transformers: { time: 14, prereqs: ['attention'],                   section: 'Deep Learning' },
  transfer:     { time: 14, prereqs: ['cnn','transformers'],          section: 'Deep Learning' },
  tokenization: { time: 8,  prereqs: ['prob'],                        section: 'NLP' },
  bert:         { time: 8,  prereqs: ['transformers','tokenization'], section: 'NLP' },
  llm:          { time: 12, prereqs: ['bert','optim'],                section: 'NLP' },
  rag:          { time: 14, prereqs: ['llm','vectordb'],              section: 'LLM Era' },
  vectordb:     { time: 10, prereqs: ['linalg','tokenization'],       section: 'LLM Era' },
  agents:       { time: 14, prereqs: ['llm','rag'],                   section: 'LLM Era' },
  multimodal:   { time: 12, prereqs: ['cnn','bert'],                  section: 'LLM Era' },
  timeseries:   { time: 12, prereqs: ['stats','rnn'],                 section: 'Domains' },
  creditrisk:   { time: 12, prereqs: ['linlog','xgb','metrics'],      section: 'Domains' },
  gnns:         { time: 12, prereqs: ['nn_basics','linalg'],          section: 'Domains' },
  responsibleai:{ time: 10, prereqs: ['metrics','mlconcepts'],        section: 'Domains' },
  causal:       { time: 14, prereqs: ['stats','prob'],                section: 'Domains' },
  dataeng:      { time: 12, prereqs: ['featureeng'],                  section: 'Production' },
  mlops:        { time: 12, prereqs: ['nn_basics','featureeng'],      section: 'Production' },
  systemdesign: { time: 12, prereqs: ['mlops','metrics'],             section: 'Production' },
  coding:       { time: 12, prereqs: [],                              section: 'Production' },
  compare:      { time: 8,  prereqs: [],                              section: 'Production' },
  frameworks:   { time: 14, prereqs: ['backprop'],                    section: 'Production' },
};

const TOPIC_NAMES = {
  linalg:'Linear Algebra', prob:'Probability Theory', stats:'Statistics & Inference',
  calc:'Calculus & Optimization', mlconcepts:'ML Paradigms', biasvar:'Bias-Variance',
  crossval:'Cross-Validation', metrics:'Eval Metrics', confusion:'Confusion Matrix & ROC',
  calibration:'Calibration & SHAP', linlog:'Linear & Logistic Reg.', knn:'k-NN',
  naivebayes:'Naive Bayes', svm:'SVM', dtree:'Decision Trees', rf:'Random Forest',
  boosting:'Gradient Boosting', xgb:'XGBoost Deep Dive', clustering:'Clustering',
  dimred:'Dim. Reduction', featureeng:'Feature Engineering', imbalanced:'Imbalanced Data',
  reg:'Regularization', hyperparam:'Hyperparameter Tuning', ensemble:'Ensemble Methods',
  nn_basics:'Perceptron & MLP', activations:'Activation Functions', loss:'Loss Functions',
  backprop:'Backprop & Training Loop', optim:'Optimizers', weightinit:'Weight Initialization',
  cnn:'CNNs', rnn:'RNNs & LSTMs', attention:'Attention & Architecture',
  transformers:'Transformers', transfer:'Transfer & Distillation',
  tokenization:'Tokenization & Embeddings', bert:'BERT & Encoder Models', llm:'LLMs & RLHF',
  rag:'RAG & Retrieval', vectordb:'Vector Databases', agents:'Agentic AI',
  multimodal:'Multimodal Models', timeseries:'Time Series', creditrisk:'Credit Risk & Scorecards',
  gnns:'Graph Neural Networks', responsibleai:'Responsible AI & Fairness',
  causal:'Causal Inference & A/B Testing', dataeng:'Data Engineering for ML',
  mlops:'MLOps & Deployment', systemdesign:'ML System Design', coding:'Python, SQL & DSA',
  compare:'Model Cheatsheet', frameworks:'TF, Keras & PyTorch',
};

// ─── PROGRESS TRACKING ─────────────────────────────────────────
const PROGRESS_KEY = 'ml-guide-progress-v2';

function getProgress() {
  try { return JSON.parse(localStorage.getItem(PROGRESS_KEY) || '{}'); } catch(e) { return {}; }
}

function setTopicRead(id, done) {
  const p = getProgress();
  if (done) p[id] = Date.now(); else delete p[id];
  try { localStorage.setItem(PROGRESS_KEY, JSON.stringify(p)); } catch(e) {}
  updateProgressUI();
}

function isRead(id) { return !!getProgress()[id]; }

function updateProgressUI() {
  const p = getProgress();
  const total = Object.keys(TOPIC_META).length;
  const done  = Object.keys(p).length;
  const pct   = Math.round((done / total) * 100);

  document.querySelectorAll('.sb-item[data-topic-id]').forEach(item => {
    const id = item.dataset.topicId;
    item.classList.toggle('sb-read', !!p[id]);
    const dot = item.querySelector('.read-dot');
    if (dot) dot.style.opacity = p[id] ? '1' : '0';
  });

  const bar   = document.getElementById('progress-bar-fill');
  const label = document.getElementById('progress-label');
  if (bar)   bar.style.width = pct + '%';
  if (label) label.textContent = done + ' / ' + total + ' read';

  const homePct  = document.getElementById('home-pct');
  const homeBar  = document.getElementById('home-progress-fill');
  if (homePct) homePct.textContent = pct + '%';
  if (homeBar) homeBar.style.width = pct + '%';

  document.querySelectorAll('.ht[data-topic-id]').forEach(card => {
    const id = card.dataset.topicId;
    card.classList.toggle('ht-read', !!p[id]);
  });
}

// ─── FULL-TEXT SEARCH INDEX ────────────────────────────────────
const searchIndex = {};

function indexTopicContent(id, html) {
  const tmp = document.createElement('div');
  tmp.innerHTML = html;
  const text = (tmp.textContent || tmp.innerText || '').replace(/\s+/g, ' ').toLowerCase();
  searchIndex[id] = { title: TOPIC_NAMES[id] || id, text };
}

function fullTextSearch(q) {
  if (!q || q.length < 2) return null;
  q = q.toLowerCase();
  const results = [];
  for (const [id, data] of Object.entries(searchIndex)) {
    if (id === 'home') continue;
    const inTitle = data.title.toLowerCase().includes(q);
    const idx     = data.text.indexOf(q);
    if (inTitle || idx >= 0) {
      let snippet = '';
      if (idx >= 0) {
        const start = Math.max(0, idx - 40);
        const end   = Math.min(data.text.length, idx + q.length + 80);
        snippet = (start > 0 ? '…' : '') + data.text.slice(start, end).trim() + (end < data.text.length ? '…' : '');
      }
      results.push({ id, title: data.title, snippet, inTitle });
    }
  }
  return results.sort((a, b) => (b.inTitle ? 1 : 0) - (a.inTitle ? 1 : 0)).slice(0, 8);
}

// ─── SEARCH DROPDOWN UI ────────────────────────────────────────
let searchDropdown = null;

function showSearchDropdown(results, q) {
  hideSearchDropdown();
  if (!results || results.length === 0) return;
  searchDropdown = document.createElement('div');
  searchDropdown.className = 'search-dropdown';
  results.forEach(r => {
    const item = document.createElement('div');
    item.className = 'search-result-item';
    const titleHl = r.title.replace(new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), m => `<mark>${m}</mark>`);
    item.innerHTML = `<div class="sr-title">${titleHl}</div>${r.snippet ? `<div class="sr-snippet">${r.snippet}</div>` : ''}`;
    item.addEventListener('mousedown', (e) => {
      e.preventDefault();
      const meta = TOPIC_META[r.id] || {};
      nav(r.id, meta.section || '', r.title);
      hideSearchDropdown();
      document.getElementById('srch').value = '';
      filterSidebar('');
    });
    searchDropdown.appendChild(item);
  });
  const searchBox = document.querySelector('.sb-search');
  if (searchBox) searchBox.appendChild(searchDropdown);
}

function hideSearchDropdown() {
  if (searchDropdown) { searchDropdown.remove(); searchDropdown = null; }
}

// ─── LOADED TOPICS ─────────────────────────────────────────────
const loadedTopics = new Set();

// ─── NAVIGATION ────────────────────────────────────────────────
async function nav(id, crumb, title) {
  document.querySelectorAll('.section.active').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.sb-item').forEach(i => i.classList.remove('active'));
  document.querySelectorAll('.sb-item[data-topic-id="' + id + '"]').forEach(i => i.classList.add('active'));

  document.getElementById('tb-crumb').textContent = crumb || '';
  document.getElementById('tb-title').textContent = title || '';

  const homeBtn = document.getElementById('tb-home-btn');
  if (homeBtn) homeBtn.style.display = (id === 'home') ? 'none' : '';

  updateReadButton(id);
  try { history.pushState({ id, crumb, title }, '', '#' + id); } catch(e) {}

  if (!loadedTopics.has(id)) {
    const filePath = TOPIC_FILES[id];
    if (filePath) {
      try {
        const res = await fetch(filePath);
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const html = await res.text();
        document.getElementById('topic-container').insertAdjacentHTML('beforeend', html);
        loadedTopics.add(id);
        indexTopicContent(id, html);

        const justLoaded = document.getElementById('sec-' + id);
        if (justLoaded) {
          if (window.Prism) Prism.highlightAllUnder(justLoaded);
          if (window.renderMathInElement) {
            renderMathInElement(justLoaded, {
              delimiters: [
                { left: '$$', right: '$$', display: true  },
                { left: '$',  right: '$',  display: false }
              ],
              throwOnError: false
            });
          }
          if (window.__cmSyncTheme) window.__cmSyncTheme();
        }
      } catch (err) {
        const name = TOPIC_NAMES[id] || id;
        document.getElementById('topic-container').insertAdjacentHTML('beforeend',
          `<section class="section" id="sec-${id}">
            <div class="sec-title">${name}</div>
            <div class="sec-desc">This topic is coming soon and will be added in the next content update.</div>
            <div class="card ca" style="margin-top:20px">
              <div class="card-title">🚧 In Progress</div>
              <div class="card-body">Use the sidebar to explore the existing topics while this one is being written.</div>
            </div>
          </section>`
        );
        loadedTopics.add(id);
      }
    }
  }

  const target = document.getElementById('sec-' + id);
  if (target) target.classList.add('active');

  window.scrollTo({ top: 0, behavior: 'smooth' });
  document.getElementById('sidebar').classList.remove('open');
  updateProgressUI();
}

// ─── MARK READ BUTTON ──────────────────────────────────────────
function updateReadButton(id) {
  const btn = document.getElementById('tb-read-btn');
  if (!btn) return;
  if (!id || id === 'home' || !TOPIC_META[id]) { btn.style.display = 'none'; return; }
  btn.style.display = '';
  const read = isRead(id);
  btn.textContent = read ? '✓ Read' : '○ Mark read';
  btn.className   = 'tb-read-btn' + (read ? ' tb-read-done' : '');
  btn.onclick = () => { setTopicRead(id, !isRead(id)); updateReadButton(id); };
}

// ─── BACK / FORWARD ────────────────────────────────────────────
window.addEventListener('popstate', (e) => {
  if (e.state && e.state.id) nav(e.state.id, e.state.crumb, e.state.title);
});

window.addEventListener('DOMContentLoaded', () => {
  const hash = location.hash.slice(1);
  if (hash && TOPIC_FILES[hash]) {
    nav(hash, '', TOPIC_NAMES[hash] || hash);
  } else {
    nav('home', 'Start Here', 'Home');
  }
  updateProgressUI();
});

// ─── SIDEBAR COLLAPSE ──────────────────────────────────────────
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const collapsed = sidebar.classList.toggle('sb-collapsed');
  const icon = document.getElementById('sb-collapse-icon');
  if (icon) icon.textContent = collapsed ? '▶' : '◀';
  try { localStorage.setItem('ml-guide-sb', collapsed ? '1' : '0'); } catch(e) {}
}

function toggleMobileSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

(function() {
  try {
    if (localStorage.getItem('ml-guide-sb') === '1') {
      document.addEventListener('DOMContentLoaded', () => {
        document.getElementById('sidebar').classList.add('sb-collapsed');
        const icon = document.getElementById('sb-collapse-icon');
        if (icon) icon.textContent = '▶';
      });
    }
  } catch(e) {}
})();

// ─── GROUP COLLAPSE ────────────────────────────────────────────
function toggleGroup(headerEl) {
  const grp = headerEl.closest('.sb-grp');
  const collapsed = grp.classList.toggle('grp-collapsed');
  const arrow = headerEl.querySelector('.grp-arrow');
  if (arrow) arrow.textContent = collapsed ? '▸' : '▾';
  const key = 'ml-grp-' + headerEl.dataset.grpId;
  try { localStorage.setItem(key, collapsed ? '1' : '0'); } catch(e) {}
}

function expandAllGroups() {
  document.querySelectorAll('.sb-grp').forEach(grp => {
    grp.classList.remove('grp-collapsed');
    const arrow = grp.querySelector('.grp-arrow');
    if (arrow) arrow.textContent = '▾';
  });
}

function collapseAllGroups() {
  document.querySelectorAll('.sb-grp').forEach(grp => {
    grp.classList.add('grp-collapsed');
    const arrow = grp.querySelector('.grp-arrow');
    if (arrow) arrow.textContent = '▸';
  });
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.sb-gl[data-grp-id]').forEach(header => {
    const key = 'ml-grp-' + header.dataset.grpId;
    try {
      if (localStorage.getItem(key) === '1') {
        header.closest('.sb-grp').classList.add('grp-collapsed');
        const arrow = header.querySelector('.grp-arrow');
        if (arrow) arrow.textContent = '▸';
      }
    } catch(e) {}
  });
});

// ─── SEARCH ────────────────────────────────────────────────────
let searchTimer = null;

function filterSidebar(q) {
  q = q.trim();
  clearTimeout(searchTimer);
  const ql = q.toLowerCase();

  document.querySelectorAll('.sb-item').forEach(item => {
    item.style.display = (!ql || item.textContent.toLowerCase().includes(ql)) ? '' : 'none';
  });
  document.querySelectorAll('.sb-gl').forEach(gl => {
    const grp = gl.parentElement;
    const hasVisible = [...grp.querySelectorAll('.sb-item')].some(i => i.style.display !== 'none');
    gl.style.display = (hasVisible || !ql) ? '' : 'none';
    if (ql && hasVisible) grp.classList.remove('grp-collapsed');
  });

  if (q.length >= 2) {
    searchTimer = setTimeout(() => {
      const results = fullTextSearch(q);
      if (results && results.length > 0) showSearchDropdown(results, q);
      else hideSearchDropdown();
    }, 250);
  } else {
    hideSearchDropdown();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const srch = document.getElementById('srch');
  if (srch) {
    srch.addEventListener('input', function() { filterSidebar(this.value); });
    srch.addEventListener('blur',  () => setTimeout(hideSearchDropdown, 150));
    srch.addEventListener('focus', function() { if (this.value.length >= 2) filterSidebar(this.value); });
  }
});

document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault(); document.getElementById('srch').focus();
  }
  if (e.key === 'Escape') {
    document.getElementById('srch').blur();
    document.getElementById('srch').value = '';
    filterSidebar(''); hideSearchDropdown();
  }
});

// ─── THEME ─────────────────────────────────────────────────────
function toggleTheme() {
  const html = document.documentElement;
  const newTheme = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', newTheme);
  document.getElementById('theme-icon').textContent = newTheme === 'light' ? '☀️' : '🌙';
  document.getElementById('theme-lbl').textContent  = newTheme === 'light' ? 'Light' : 'Dark';
  try { localStorage.setItem('ml-guide-theme', newTheme); } catch(e) {}
  if (window.__cmSyncTheme) window.__cmSyncTheme();
  if (window.Prism) Prism.highlightAll();
}

(function () {
  try {
    const saved = localStorage.getItem('ml-guide-theme');
    if (saved) {
      document.documentElement.setAttribute('data-theme', saved);
      document.addEventListener('DOMContentLoaded', () => {
        const icon = document.getElementById('theme-icon');
        const lbl  = document.getElementById('theme-lbl');
        if (icon) icon.textContent = saved === 'light' ? '☀️' : '🌙';
        if (lbl)  lbl.textContent  = saved === 'light' ? 'Light' : 'Dark';
      });
    }
  } catch(e) {}
})();

// ─── PYODIDE ───────────────────────────────────────────────────
let pyodideInstance = null;
let pyodideCallbacks = [];

async function initPyodide() {
  if (pyodideInstance) return pyodideInstance;
  document.querySelectorAll('.run-btn').forEach(btn => { btn.textContent = '⏳ Loading Python…'; btn.disabled = true; });
  try {
    pyodideInstance = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/' });
    await pyodideInstance.loadPackage(['numpy', 'micropip']);
    await pyodideInstance.runPythonAsync('import micropip\nawait micropip.install(["scikit-learn"])');
    document.querySelectorAll('.run-btn').forEach(btn => { btn.textContent = '▶ Run'; btn.disabled = false; });
    pyodideCallbacks.forEach(cb => cb(pyodideInstance));
    pyodideCallbacks = [];
    return pyodideInstance;
  } catch(err) {
    document.querySelectorAll('.run-btn').forEach(btn => { btn.textContent = '▶ Run (offline)'; btn.disabled = false; btn.title = 'Pyodide failed to load.'; });
    throw err;
  }
}

async function runCode(runnerId) {
  const runner = document.getElementById(runnerId);
  if (!runner) return;
  const textarea = runner.querySelector('.code-input');
  const output   = runner.querySelector('.code-output');
  const btn      = runner.querySelector('.run-btn');
  const cmView   = window.__cmEditors && window.__cmEditors[runnerId];
  const code     = cmView ? cmView.state.doc.toString() : textarea.value;
  btn.textContent = '⏳ Running…'; btn.disabled = true;
  output.textContent = ''; output.className = 'code-output';
  try {
    const pyodide = await initPyodide();
    pyodide.runPython('import sys, io\nsys.stdout = io.StringIO()\nsys.stderr = sys.stdout');
    let errMsg = null;
    try { await pyodide.runPythonAsync(code); } catch(pyErr) { errMsg = pyErr.message || String(pyErr); }
    const stdout = pyodide.runPython('sys.stdout.getvalue()');
    if (errMsg) { output.textContent = stdout + '\n❌ ' + errMsg; output.classList.add('err'); }
    else { output.textContent = stdout || '✓ Ran successfully (no output)'; output.classList.add('ok'); }
  } catch(err) {
    output.textContent = '❌ Pyodide not available — run this in a local Jupyter or Colab.';
    output.classList.add('err');
  } finally { btn.textContent = '▶ Run'; btn.disabled = false; }
}

function resetCode(runnerId) {
  const runner = document.getElementById(runnerId);
  if (!runner) return;
  const textarea = runner.querySelector('.code-input');
  const original = textarea.getAttribute('data-original') || '';
  const cmView   = window.__cmEditors && window.__cmEditors[runnerId];
  if (cmView) { cmView.dispatch({ changes: { from: 0, to: cmView.state.doc.length, insert: original } }); }
  else { textarea.value = original; }
  const output = runner.querySelector('.code-output');
  output.textContent = ''; output.className = 'code-output';
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.code-input').forEach(ta => { ta.setAttribute('data-original', ta.value); });
  if (typeof loadPyodide !== 'undefined') { initPyodide().catch(() => {}); }
});
