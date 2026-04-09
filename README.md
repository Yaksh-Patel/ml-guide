# ML/DS Master Study Guide

> A self-contained, interactive reference for machine learning and data science — built for interview prep, concept revision, and continuous learning.

[![Open Guide](https://img.shields.io/badge/Open%20Guide-Live%20Site-5b7df8?style=for-the-badge&logo=github)](https://yaksh-patel.github.io/ml-guide)
![Topics](https://img.shields.io/badge/Topics-57-22d3a0?style=for-the-badge)
![No Dependencies](https://img.shields.io/badge/Dependencies-None-f5a623?style=for-the-badge)

---

## What This Is

A single-file-per-topic HTML guide covering the full ML/DS interview and job-readiness stack — from linear algebra fundamentals to frontier LLM deployment. Every topic is self-contained: formula, intuition, animation, code (where relevant), and an ideal interview answer.

No framework, no build step, no install. Open `index.html` via a local server and everything works.

---

## Features

| | Detail |
|---|---|
| **57 topics** | Math foundations → classical ML → deep learning → LLMs → RAG → agents → production |
| **Progress tracking** | Mark topics as read — persists in localStorage, progress bar in sidebar |
| **Interactive diagrams** | Bias-variance slider, attention heatmap, backprop step-through, confusion matrix + ROC explorer |
| **LaTeX rendering** | All formulas rendered via KaTeX — clean, properly spaced math |
| **SVG animations** | 14+ topics include animated diagrams: backprop flow, CNN convolution, LSTM gates, attention weights, encoder-decoder |
| **Runnable Python** | In-browser Python via Pyodide — edit and re-run without any install |
| **Interview answers** | Every topic ends with a 🎯 Interview Gold box — a model answer with follow-up Q&A |
| **Common mistakes** | Every topic includes a common misconceptions section |
| **Company examples** | Every topic includes "How it's used at top companies" |
| **Dark / Light mode** | Toggle in topbar, preference persisted to localStorage |
| **Full-text search** | Searches across loaded topic content (not just titles) with snippet preview · `Ctrl+K` |
| **Shareable URLs** | Each topic updates the URL hash — bookmark or share any section |
| **Prereq tags** | Each topic card on the home page shows what to read first |
| **Reading times** | Estimated reading time shown on every topic card |
| **Zero dependencies** | Pure HTML + CSS + Vanilla JS. Pyodide and KaTeX loaded from CDN on first use |

---

## Topic Map

```
topics/
│
├── 🔢  Mathematical Foundations
│   ├── 01-linear-algebra.html              vectors, matrices, eigenvalues, SVD
│   ├── 02-probability.html                 Bayes' theorem, distributions, MLE vs MAP
│   ├── 03-statistics.html                  p-values, confidence intervals, hypothesis tests
│   └── 04-calculus.html                    gradients, chain rule, optimization
│
├── 🧭  ML Thinking & Evaluation
│   ├── 05-ml-paradigms.html                supervised, unsupervised, self-supervised, RL
│   ├── 06-bias-variance.html               tradeoff, learning curves, interactive curve explorer ✦
│   ├── 07-cross-validation.html            k-fold, stratified, time-series split
│   ├── 08-eval-metrics.html                MAE, RMSE, F1, MAPE, metric selection framework
│   ├── 09-confusion-roc.html               confusion matrix + interactive ROC/PR threshold explorer ✦
│   └── 10-calibration-explainability.html  Platt scaling, ECE, SHAP, LIME, feature importance
│
├── 🌳  Classical ML Algorithms
│   ├── 11-linear-logistic.html             OLS, sigmoid, assumptions, regularized variants
│   ├── 12-knn.html                         lazy learning, distance metrics, curse of dimensionality
│   ├── 13-naive-bayes.html                 Gaussian / Multinomial / Bernoulli, Laplace smoothing
│   ├── 14-svm.html                         margin, kernel trick, RBF, soft margin, C parameter
│   ├── 15-decision-trees.html              Gini, entropy, pruning, interpretability
│   ├── 16-random-forest.html               bagging, OOB error, feature importance
│   ├── 17-gradient-boosting.html           GBM, LightGBM, CatBoost — algorithm deep dive
│   ├── 18-xgboost.html                     objective, second-order Taylor expansion, split gain
│   ├── 19-clustering.html                  K-Means, DBSCAN, hierarchical, silhouette score
│   └── 20-dimensionality-reduction.html    PCA, t-SNE, UMAP
│
├── ⚙️  Data & Model Engineering
│   ├── 21-feature-engineering.html         missing values, encoding, scaling, selection
│   ├── 22-imbalanced.html                  SMOTE, class weights, Focal Loss, PR-AUC
│   ├── 23-regularization.html              L1, L2, dropout, early stopping, BatchNorm
│   ├── 24-hyperparameter-tuning.html       grid, random, Bayesian search (Optuna + Hyperopt)
│   └── 25-ensemble-methods.html            bagging, boosting, stacking, blending
│
├── 🧠  Neural Network Foundations
│   ├── 26-mlp.html                         perceptron, forward pass, universal approximation
│   ├── 27-activations.html                 ReLU, GELU, Swish, sigmoid, dying ReLU fix
│   ├── 28-loss-functions.html              MSE, BCE, CCE, Huber, Focal, KL, label smoothing  ▶
│   ├── 29-backpropagation.html             chain rule, animated step-through computation graph ✦ ▶
│   ├── 30-optimizers.html                  SGD, Momentum, Adam, AdamW, LR scheduling
│   └── 31-weight-init.html                 Xavier / Glorot, He / Kaiming, orthogonal
│
├── 🤖  Deep Learning Architectures
│   ├── 32-cnns.html                        convolution op, ResNet skip connections, EfficientNet
│   ├── 33-rnns-lstms.html                  LSTM gates, GRU, bidirectional RNN, vanishing grads
│   ├── 34-attention-architecture.html      Q/K/V, multi-head, interactive attention heatmap ✦
│   ├── 35-transformers.html                encoder-decoder, positional encoding, variants
│   └── 36-transfer-distillation.html       fine-tuning, LoRA/QLoRA/PEFT deep dive,
│                                           teacher-student distillation, temperature τ
│
├── 💬  NLP & Language Models
│   ├── 37-tokenization-embeddings.html     BPE, Word2Vec, SBERT, contextual embeddings
│   ├── 38-bert.html                        MLM, fine-tuning, RoBERTa, domain-specific BERT
│   └── 39-llms-rlhf.html                   GPT architecture, scaling laws, RLHF, DPO, ORPO,
│                                           prompt engineering, eval frameworks, hallucination
│
├── ✨  LLM Era  (new)
│   ├── 48-rag.html                         chunking, hybrid search, reranking, RAGAS eval
│   ├── 49-vector-databases.html            HNSW, IVF+PQ, FAISS, Pinecone/Qdrant/Weaviate
│   └── 50-agentic-ai.html                  ReAct, tool calling, multi-agent, memory, guardrails
│
├── 📡  Specialized Domains
│   ├── 40-time-series.html                 ARIMA, Prophet, TFT, walk-forward CV, stationarity
│   ├── 41-credit-risk.html                 WOE/IV, scorecards, IFRS 9, PSI/KS/Gini
│   ├── 46-gnns.html                        message passing, GCN, GraphSAGE, GAT, fraud/recsys
│   ├── 51-responsible-ai.html              fairness metrics, bias mitigation, model cards, EU AI Act
│   ├── 52-causal-inference.html            A/B testing, power analysis, CUPED, DiD, uplift models
│   └── 53-data-engineering.html            Spark, dbt, Delta Lake, Iceberg, feature pipelines
│
└── 🚀  Production & System Design
    ├── 42-mlops.html                       serving patterns, drift detection, CI/CD, vLLM, costs
    ├── 43-system-design.html               fraud, recsys, search/ranking, real-time inference
    ├── 44-python-sql-dsa.html              pandas patterns, window functions, DSA
    ├── 45-model-cheatsheet.html            algorithm selection guide, loss guide, diagnostics
    ├── 47-tf-keras-pytorch.html            framework comparison, starter code for all three
    └── 54-multimodal.html                  CLIP, ViT, LLaVA, VLMs, image-text embeddings
```

✦ = interactive diagram (slider / clickable / step-through animation)  
▶ = runnable in-browser Python (Pyodide)

---

## Full Topic List

| # | Topic | Group |
|---|-------|-------|
| 01 | Linear Algebra | Math Foundations |
| 02 | Probability Theory | Math Foundations |
| 03 | Statistics & Inference | Math Foundations |
| 04 | Calculus & Optimization | Math Foundations |
| 05 | ML Paradigms | ML Thinking |
| 06 | Bias-Variance Tradeoff ✦ | ML Thinking |
| 07 | Cross-Validation | ML Thinking |
| 08 | Evaluation Metrics | ML Thinking |
| 09 | Confusion Matrix & ROC ✦ | ML Thinking |
| 10 | Calibration & Explainability | ML Thinking |
| 11 | Linear & Logistic Regression | Classical ML |
| 12 | k-Nearest Neighbors | Classical ML |
| 13 | Naive Bayes | Classical ML |
| 14 | Support Vector Machines | Classical ML |
| 15 | Decision Trees | Classical ML |
| 16 | Random Forest | Classical ML |
| 17 | Gradient Boosting | Classical ML |
| 18 | XGBoost Deep Dive | Classical ML |
| 19 | Clustering | Classical ML |
| 20 | Dimensionality Reduction | Classical ML |
| 21 | Feature Engineering | Data Engineering |
| 22 | Imbalanced Data | Data Engineering |
| 23 | Regularization | Data Engineering |
| 24 | Hyperparameter Tuning | Data Engineering |
| 25 | Ensemble Methods | Data Engineering |
| 26 | Perceptron & MLP | Neural Networks |
| 27 | Activation Functions | Neural Networks |
| 28 | Loss Functions ▶ | Neural Networks |
| 29 | Backpropagation & Training ✦ ▶ | Neural Networks |
| 30 | Optimizers | Neural Networks |
| 31 | Weight Initialization | Neural Networks |
| 32 | CNNs | Deep Learning |
| 33 | RNNs & LSTMs | Deep Learning |
| 34 | Attention & Architecture ✦ | Deep Learning |
| 35 | Transformers | Deep Learning |
| 36 | Transfer Learning & Distillation | Deep Learning |
| 37 | Tokenization & Embeddings | NLP |
| 38 | BERT & Encoder Models | NLP |
| 39 | LLMs, SLMs & RLHF | NLP |
| 40 | Time Series Modeling | Domains |
| 41 | Credit Risk & Scorecards | Domains |
| 42 | MLOps & Deployment | Production |
| 43 | ML System Design | Production |
| 44 | Python, SQL & DSA | Production |
| 45 | Model Cheatsheet | Reference |
| 46 | Graph Neural Networks | Domains |
| 47 | TF, Keras & PyTorch | Reference |
| 48 | RAG & Retrieval ✨ | LLM Era |
| 49 | Vector Databases ✨ | LLM Era |
| 50 | Agentic AI ✨ | LLM Era |
| 51 | Responsible AI & Fairness ✨ | Domains |
| 52 | Causal Inference & A/B Testing ✨ | Domains |
| 53 | Data Engineering for ML ✨ | Production |
| 54 | Multimodal Models ✨ | LLM Era |

✦ = interactive diagram &nbsp;|&nbsp; ▶ = runnable Python &nbsp;|&nbsp; ✨ = new topic

---

## Running Locally

```bash
# Clone
git clone https://github.com/Yaksh-Patel/ml-guide.git
cd ml-guide

# Serve (required — browser blocks file:// fetch for security)
python -m http.server 8080

# Open
open http://localhost:8080
```

> Topics are loaded dynamically via `fetch()`. A local server is required — opening `index.html` directly as a `file://` URL will not work.

---

## Project Structure

```
ml-guide/
├── index.html                  shell: topbar, sidebar, progress bar, search, theme toggle
├── assets/
│   ├── style.css               full design system — dark + light theme, cards, formulas
│   ├── nav.js                  routing, progress tracking, full-text search, Pyodide runner
│   ├── prism-theme.css         syntax highlighting for code blocks
│   └── codemirror-init.js      CodeMirror editor for interactive code runners
├── topics/
│   ├── 00-home.html            landing page, visual topic map, study path, progress ring
│   └── 01–54-*.html            one file per topic (see map above)
└── README.md
```

Each topic file is a single `<section>` block — no boilerplate, no imports. The shell handles all routing, theming, search, and progress tracking.

---

## Adding a New Topic

**1. Create the file:**
```bash
touch topics/55-diffusion-models.html
```

**2. Write the content** — just a `<section>`, no boilerplate needed:
```html
<section class="section" id="sec-diffusion">
  <div class="sec-title">Diffusion Models</div>
  <div class="sec-desc">DDPM, DDIM, score matching — generative models that learn to reverse a noise process.</div>

  <div class="card cb">
    <div class="card-title">Forward Process</div>
    <div class="formula math-formula">
      $$q(x_t | x_{t-1}) = \mathcal{N}(x_t;\, \sqrt{1-\beta_t}\,x_{t-1},\, \beta_t I)$$
    </div>
  </div>

  <div class="card cr">
    <div class="card-title">Common Mistakes & Misconceptions</div>
    <ul class="bul">
      <li><strong>Diffusion ≠ GANs:</strong> no adversarial training, no mode collapse...</li>
    </ul>
  </div>

  <div class="box ideal">
    <div class="bl">🎯 Interview Gold</div>
    <p>...</p>
  </div>
</section>
```

**3. Register in `assets/nav.js`** — add to both `TOPIC_FILES` and `TOPIC_META`:
```js
// In TOPIC_FILES:
diffusion: 'topics/55-diffusion-models.html',

// In TOPIC_META:
diffusion: { time: 14, prereqs: ['nn_basics','optim'], section: 'Deep Learning' },

// In TOPIC_NAMES:
diffusion: 'Diffusion Models',
```

**4. Add sidebar entry in `index.html`:**
```html
<div class="sb-item" data-topic-id="diffusion"
     onclick="nav('diffusion','Deep Learning','Diffusion Models')">
  <span class="n">55</span>Diffusion Models<span class="read-dot"></span>
</div>
```

**5. Add to home page (`topics/00-home.html`)** in the appropriate section grid.

**6. Commit and push:**
```bash
git add topics/55-diffusion-models.html assets/nav.js index.html topics/00-home.html
git commit -m "add: topic 55 — diffusion models (DDPM, DDIM, score matching)"
git push
```

GitHub Pages auto-deploys in ~30 seconds.

---

## Adding Interactive Diagrams

Topic files are loaded via `fetch()` and injected with `insertAdjacentHTML()`. The nav.js automatically re-executes any `<script>` tags found in the injected HTML — so interactive diagrams work just like they would if opened directly.

Use the `anim-wrap` container for consistent styling:

```html
<div class="anim-wrap" style="padding:16px 20px">
  <div class="anim-title">Interactive — Your diagram title here</div>

  <!-- Controls -->
  <div style="display:flex;align-items:center;gap:12px;margin:10px 0">
    <label style="font-size:12px;color:var(--text2)">Parameter</label>
    <input type="range" id="my-slider" min="0" max="100" value="50"
           style="flex:1;max-width:280px">
    <span id="my-readout" style="font-size:12px;font-weight:700;color:var(--accent)">50</span>
  </div>

  <!-- SVG canvas -->
  <svg viewBox="0 0 560 200" style="width:100%;display:block">
    <path id="my-path" fill="none" stroke="#5ba4fb" stroke-width="2"/>
  </svg>

  <!-- Explanation -->
  <div id="my-explain" style="font-size:12px;color:var(--text2);margin-top:6px;
       padding:8px 10px;background:var(--bg3);border-radius:7px"></div>
</div>

<script>
(function(){
  function update(v) {
    document.getElementById('my-readout').textContent = v;
    document.getElementById('my-explain').textContent = 'Value is ' + v;
    // draw your SVG path here
  }
  document.getElementById('my-slider').addEventListener('input', function() {
    update(+this.value);
  });
  update(50);
})();
</script>
```

The IIFE wrapper `(function(){ ... })()` keeps your variables scoped so multiple diagrams on different topics don't conflict.

---

## Adding Runnable Code

```html
<div class="card cc">
  <div class="card-title">▶ Run It: Your Title</div>
  <div class="code-runner" id="runner-UNIQUE-ID">
    <div class="code-runner-header">
      <span>🐍 Python · numpy · sklearn</span>
      <div class="runner-btns">
        <button class="reset-btn" onclick="resetCode('runner-UNIQUE-ID')">↺ Reset</button>
        <button class="run-btn"   onclick="runCode('runner-UNIQUE-ID')">▶ Run</button>
      </div>
    </div>
    <textarea class="code-input">
import numpy as np
print("Hello from Pyodide!")
    </textarea>
    <pre class="code-output">Click ▶ Run to execute…</pre>
  </div>
</div>
```

**Available packages:** `numpy`, `scikit-learn`, `scipy`, `pandas`, `sympy`, `networkx`  
**Not available in-browser:** `torch`, `tensorflow` — link to Colab for those.

---

## Card & Box Reference

| Class | Colour | Use for |
|---|---|---|
| `card` | neutral | general content |
| `card cb` | blue | strengths, key concepts |
| `card cg` | green | correct approach, solutions |
| `card cr` | red | weaknesses, pitfalls, warnings |
| `card ca` | amber | caution, important notes |
| `card cp` | purple | advanced / deeper concepts |
| `card cc` | cyan | code blocks |

| Box class | Use for |
|---|---|
| `box ideal` | 🎯 Interview Gold answer |
| `box warn` | ⚠️ Common mistake or gotcha |
| `box story` | 📖 Intuition analogy |
| `box info` | 💡 Key insight / tip |
| `box tip` | 🔧 Practical how-to |
| `box mem` | 💡 Memory tip |

---

## Tech Stack

| | |
|---|---|
| **HTML + CSS + Vanilla JS** | Zero build step, zero npm, zero dependencies |
| **[KaTeX](https://katex.org)** | Fast client-side LaTeX rendering for all math |
| **[Pyodide](https://pyodide.org)** | Python in the browser via WebAssembly |
| **[Prism.js](https://prismjs.com)** | Syntax highlighting for code blocks |
| **[CodeMirror 6](https://codemirror.net)** | IDE-quality editor for interactive runners |
| **GitHub Pages** | Static hosting, auto-deploys on push to `main` |

---

*Built by [Yaksh Patel](https://yaksh-patel.github.io)*
