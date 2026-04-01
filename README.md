# ML/DS Master Study Guide

> A self-contained, interactive reference for machine learning and data science — built for interview prep, concept revision, and continuous learning.

[![Open Guide](https://img.shields.io/badge/Open%20Guide-Live%20Site-5b7df8?style=for-the-badge&logo=github)](https://yaksh-patel.github.io/ml-guide)
![Topics](https://img.shields.io/badge/Topics-47-22d3a0?style=for-the-badge)
![No Dependencies](https://img.shields.io/badge/Dependencies-None-f5a623?style=for-the-badge)

---

## What This Is

A single-file-per-topic HTML guide covering the full ML/DS interview and job-readiness stack — from linear algebra fundamentals to production LLM deployment. Every topic is self-contained: formula, intuition, animation, code (where relevant), and an ideal interview answer.

No framework, no build step, no install. Open `index.html` via a local server and everything works.

---

## Features

| | Detail |
|---|---|
| **47 topics** | Mathematical foundations → classical ML → deep learning → NLP → production |
| **LaTeX rendering** | All formulas rendered via KaTeX — clean, properly spaced math |
| **SVG animations** | 14 topics include animated diagrams: backprop flow, CNN convolution, LSTM gates, attention weights, encoder-decoder, bias-variance curve, and more |
| **Runnable Python** | Topics 28 and 29 include in-browser Python via Pyodide — edit and re-run without any install |
| **Interview answers** | Every topic ends with a 🎯 Interview Gold box — a model answer for that topic |
| **Dark / Light mode** | Toggle in topbar, preference persisted to localStorage |
| **Sidebar search** | Instant filter across all 47 topics · `Ctrl+K` to focus |
| **Shareable URLs** | Each topic updates the URL hash — bookmark or share any section |
| **Zero dependencies** | Pure HTML + CSS + Vanilla JS. Pyodide and KaTeX loaded from CDN on first use |

---

## Topic Map

```
topics/
│
├── 🔢  Mathematical Foundations
│   ├── 01-linear-algebra.html          vectors, matrices, eigenvalues, SVD
│   ├── 02-probability.html             Bayes' theorem, distributions, MLE vs MAP
│   ├── 03-statistics.html              p-values, confidence intervals, hypothesis tests
│   └── 04-calculus.html                gradients, chain rule, optimization
│
├── 🧭  ML Thinking & Evaluation
│   ├── 05-ml-paradigms.html            supervised, unsupervised, self-supervised, RL
│   ├── 06-bias-variance.html           tradeoff, learning curves, diagnostics
│   ├── 07-cross-validation.html        k-fold, stratified, time-series split
│   ├── 08-eval-metrics.html            MAE, RMSE, F1, MAPE, metric selection framework
│   ├── 09-confusion-roc.html           TP/FP matrix, AUC-ROC, PR-AUC, KS statistic
│   └── 10-calibration-explainability   Platt scaling, ECE, SHAP, LIME, feature importance
│
├── 🌳  Classical ML Algorithms
│   ├── 11-linear-logistic.html         OLS, sigmoid, assumptions, regularized variants
│   ├── 12-knn.html                     lazy learning, distance metrics, curse of dimensionality
│   ├── 13-naive-bayes.html             Gaussian / Multinomial / Bernoulli, Laplace smoothing
│   ├── 14-svm.html                     margin, kernel trick, RBF, soft margin, C parameter
│   ├── 15-decision-trees.html          Gini, entropy, pruning, interpretability
│   ├── 16-random-forest.html           bagging, OOB error, feature importance biases
│   ├── 17-gradient-boosting.html       algorithm, XGBoost vs LightGBM vs CatBoost
│   ├── 18-xgboost.html                 objective, second-order Taylor expansion, split gain
│   ├── 19-clustering.html              K-Means, DBSCAN, hierarchical, silhouette score
│   └── 20-dimensionality-reduction     PCA, t-SNE, UMAP
│
├── ⚙️  Data & Model Engineering
│   ├── 21-feature-engineering.html     missing values, encoding, scaling, selection
│   ├── 22-imbalanced.html              SMOTE, class weights, Focal Loss, PR-AUC
│   ├── 23-regularization.html          L1, L2, dropout, early stopping, BatchNorm
│   ├── 24-hyperparameter-tuning.html   grid, random, Bayesian (Optuna + Hyperopt)
│   └── 25-ensemble-methods.html        bagging, boosting, stacking, blending
│
├── 🧠  Neural Network Foundations
│   ├── 26-mlp.html                     perceptron, forward pass, universal approximation
│   ├── 27-activations.html             ReLU, GELU, Swish, sigmoid, dying ReLU fix
│   ├── 28-loss-functions.html          MSE, BCE, CCE, Huber, Focal, KL, label smoothing  ▶
│   ├── 29-backpropagation.html         chain rule, vanishing/exploding grads, BatchNorm  ▶
│   ├── 30-optimizers.html              SGD, Momentum, Adam, AdamW, LR scheduling
│   └── 31-weight-init.html             Xavier / Glorot, He / Kaiming, orthogonal
│
├── 🤖  Deep Learning Architectures
│   ├── 32-cnns.html                    convolution op, ResNet skip connections, EfficientNet
│   ├── 33-rnns-lstms.html              LSTM gates, GRU, bidirectional RNN, vanishing grads
│   ├── 34-attention-architecture.html  Q/K/V attention, multi-head, Seq2Seq→Transformer lineage
│   ├── 35-transformers.html            encoder-decoder, positional encoding, variants table
│   └── 36-transfer-distillation.html   fine-tuning, LoRA/PEFT, catastrophic forgetting,
│                                       teacher-student distillation, temperature τ, DistilBERT
│
├── 💬  NLP & Language Models
│   ├── 37-tokenization-embeddings.html BPE, Word2Vec, SBERT, contextual embeddings
│   ├── 38-bert.html                    MLM, fine-tuning, RoBERTa, domain-specific BERT
│   └── 39-llms-rlhf.html               GPT architecture, scaling laws, RLHF, DPO, SLMs
│
├── 📡  Specialized Domains
│   ├── 40-time-series.html             ARIMA, Prophet, TFT, walk-forward CV, stationarity
│   ├── 41-credit-risk.html             WOE/IV, scorecards, IFRS 9, PSI/KS/Gini
│   └── 46-bipartite-graphs.html        user-item graphs, collaborative filtering, GNNs
│
└── 🚀  Production & System Design
    ├── 42-mlops.html                   serving patterns, drift detection, feature store
    ├── 43-system-design.html           fraud detection design, latency vs accuracy
    ├── 44-python-sql-dsa.html          pandas patterns, window functions, DSA
    ├── 45-model-cheatsheet.html        algorithm selection guide, loss guide, diagnostics
    └── 47-tf-keras-pytorch.html        framework comparison, starter code for all three
```

▶ = includes runnable in-browser Python (Pyodide)

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

> Topics are loaded dynamically via `fetch()`. A local server is required; opening `index.html` directly as a `file://` URL will not work.

---

## Project Structure

```
ml-guide/
├── index.html                  shell: topbar, sidebar, content pane, theme toggle
├── assets/
│   ├── style.css               full design system — dark + light theme, cards, formulas
│   ├── nav.js                  routing, sidebar search, Pyodide runner, topic registry
│   └── prism-theme.css         syntax highlighting for code blocks
├── topics/
│   ├── 00-home.html            landing page and study map
│   └── 01–47-*.html            one file per topic (see map above)
└── README.md
```

Each topic file is a single `<section>` block — no boilerplate, no imports. The shell handles everything else.

---

## Adding a New Topic

**1. Create the file:**
```bash
touch topics/48-diffusion-models.html
```

**2. Write the content** — just a `<section>`, no boilerplate needed:
```html
<section class="section" id="sec-diffusion">
  <div class="sec-title">Diffusion Models</div>
  <div class="sec-desc">DDPM, DDIM, score matching — generative models that learn to reverse a noise process.</div>

  <div class="card">
    <div class="card-title">Forward Process</div>
    <div class="formula math-formula">
      $$q(x_t | x_{t-1}) = \mathcal{N}(x_t;\, \sqrt{1-\beta_t}\,x_{t-1},\, \beta_t I)$$
    </div>
  </div>

  <div class="box ideal">
    <div class="bl">🎯 Interview Gold</div>
    <p>"Diffusion models define a forward process that gradually adds Gaussian noise..."</p>
  </div>
</section>
```

**3. Register in `assets/nav.js`:**
```js
diffusion: 'topics/48-diffusion-models.html',
```

**4. Add sidebar entry in `index.html`:**
```html
<div class="sb-item" onclick="nav('diffusion','Deep Learning','Diffusion Models')">
  <span class="n">48</span>Diffusion Models
</div>
```

**5. Commit and push:**
```bash
git add topics/48-diffusion-models.html assets/nav.js index.html
git commit -m "add: topic 48 — diffusion models (DDPM, DDIM, score matching)"
git push
```

GitHub Pages auto-deploys in ~30 seconds.

---

## Adding Runnable Code

Paste this template into any topic. The runner is wired by `nav.js` automatically:

```html
<div class="card cc">
  <div class="card-title">▶ Run It: Your Title</div>
  <div class="code-runner" id="runner-UNIQUE-ID">
    <div class="code-runner-header">
      <span>🐍 Python · numpy</span>
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
| `card cc` | code bg | runnable code blocks |

| Box class | Use for |
|---|---|
| `box ideal` | 🎯 Interview Gold answer |
| `box warn` | ⚠️ Common mistake or gotcha |
| `box story` | 📖 Intuition analogy |
| `box mem` | 💡 Memory tip / key insight |

---

## Tech Stack

| | |
|---|---|
| **HTML + CSS + Vanilla JS** | Zero build step, zero npm, zero dependencies |
| **[KaTeX](https://katex.org)** | Fast client-side LaTeX rendering for all math |
| **[Pyodide](https://pyodide.org)** | Python in the browser via WebAssembly |
| **[Prism.js](https://prismjs.com)** | Syntax highlighting for code blocks |
| **GitHub Pages** | Static hosting, auto-deploys on push to `main` |

---

## Full Topic List

| # | Topic | Group |
|---|-------|-------|
| 01 | Linear Algebra | Math Foundations |
| 02 | Probability Theory | Math Foundations |
| 03 | Statistics & Inference | Math Foundations |
| 04 | Calculus & Optimization | Math Foundations |
| 05 | ML Paradigms | ML Thinking |
| 06 | Bias-Variance Tradeoff | ML Thinking |
| 07 | Cross-Validation | ML Thinking |
| 08 | Evaluation Metrics | ML Thinking |
| 09 | Confusion Matrix & ROC | ML Thinking |
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
| 26 | Multi-Layer Perceptrons | Neural Networks |
| 27 | Activation Functions | Neural Networks |
| 28 | Loss Functions ▶ | Neural Networks |
| 29 | Backpropagation & Training ▶ | Neural Networks |
| 30 | Optimizers | Neural Networks |
| 31 | Weight Initialization | Neural Networks |
| 32 | Convolutional Neural Networks | Deep Learning |
| 33 | RNNs & LSTMs | Deep Learning |
| 34 | Attention & Transformer Architecture | Deep Learning |
| 35 | Transformers | Deep Learning |
| 36 | Transfer Learning & Knowledge Distillation | Deep Learning |
| 37 | Tokenization & Embeddings | NLP |
| 38 | BERT & Encoder Models | NLP |
| 39 | LLMs, SLMs & RLHF | NLP |
| 40 | Time Series Modeling | Domains |
| 41 | Credit Risk Modeling | Domains |
| 42 | MLOps | Production |
| 43 | ML System Design | Production |
| 44 | Python, SQL & DSA | Production |
| 45 | Model Cheatsheet | Reference |
| 46 | Bipartite Graphs & Recommenders | Domains |
| 47 | TF, Keras & PyTorch | Reference |

▶ = runnable in-browser Python

---

*Built by [Yaksh Patel](https://yaksh-patel.github.io)*
