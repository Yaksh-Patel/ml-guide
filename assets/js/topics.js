/* ==========================================================
   topics.js — SINGLE SOURCE OF TRUTH for the guide's contents.

   Add a topic here and it appears everywhere: sidebar, home grid,
   topic map, search index, prev/next, progress total, breadcrumbs.
   Nothing else needs editing.

   id       stable slug; also the URL hash and the topic file's
            section id must be  sec-<id>
   num      display number shown in the sidebar and home card
   title    full title (breadcrumb, topic map, home card)
   short    shorter label for the sidebar
   file     path to the topic HTML fragment
   time     estimated read time in minutes
   prereqs  topic ids worth reading first
   badge    'new' | 'coming' | null
   ========================================================== */

export const GROUPS = [
  {
    id: 'math', icon: '🔢', label: 'Mathematical Foundations',
    topics: [
      { id: 'linalg', num: '01', title: 'Linear Algebra', short: 'Linear Algebra', blurb: 'Vectors, matrices, eigenvalues, SVD',
        file: 'topics/01-linear-algebra.html', time: 12, prereqs: [], badge: null },
      { id: 'prob', num: '02', title: 'Probability Theory', short: 'Probability Theory', blurb: 'Bayes, distributions, expectation',
        file: 'topics/02-probability.html', time: 10, prereqs: ['linalg'], badge: null },
      { id: 'stats', num: '03', title: 'Statistics & Inference', short: 'Statistics & Inference', blurb: 'p-values, CI, hypothesis tests',
        file: 'topics/03-statistics.html', time: 10, prereqs: ['prob'], badge: null },
      { id: 'calc', num: '04', title: 'Calculus & Optimization', short: 'Calculus & Optimization', blurb: 'Gradients, chain rule, convexity',
        file: 'topics/04-calculus.html', time: 12, prereqs: ['linalg'], badge: null },
    ],
  },
  {
    id: 'mlthink', icon: '🧭', label: 'ML Thinking & Evaluation',
    topics: [
      { id: 'mlconcepts', num: '05', title: 'ML Paradigms', short: 'ML Paradigms', blurb: 'Supervised, unsupervised, semi-, RL',
        file: 'topics/05-ml-paradigms.html', time: 8, prereqs: ['stats'], badge: null },
      { id: 'biasvar', num: '06', title: 'Bias-Variance Tradeoff', short: 'Bias-Variance Tradeoff', blurb: 'Overfitting, underfitting tradeoff',
        file: 'topics/06-bias-variance.html', time: 8, prereqs: ['mlconcepts'], badge: null },
      { id: 'crossval', num: '07', title: 'Cross-Validation', short: 'Cross-Validation', blurb: 'k-fold, stratified, time-series split',
        file: 'topics/07-cross-validation.html', time: 10, prereqs: ['biasvar'], badge: null },
      { id: 'metrics', num: '08', title: 'Evaluation Metrics', short: 'Evaluation Metrics', blurb: 'MSE, MAE, accuracy, F1, RMSE',
        file: 'topics/08-eval-metrics.html', time: 8, prereqs: ['mlconcepts'], badge: null },
      { id: 'confusion', num: '09', title: 'Confusion Matrix & ROC', short: 'Confusion Matrix & ROC', blurb: 'TP/FP/AUC/KS/PR-AUC',
        file: 'topics/09-confusion-roc.html', time: 8, prereqs: ['metrics'], badge: null },
      { id: 'calibration', num: '10', title: 'Calibration & Explainability', short: 'Calibration & Explainability', blurb: 'Reliability diagrams, LIME, SHAP',
        file: 'topics/10-calibration-explainability.html', time: 10, prereqs: ['confusion'], badge: null },
    ],
  },
  {
    id: 'classical', icon: '🌳', label: 'Classical ML Algorithms',
    topics: [
      { id: 'linlog', num: '11', title: 'Linear & Logistic Regression', short: 'Linear & Logistic Regression', blurb: 'OLS, sigmoid, assumptions',
        file: 'topics/11-linear-logistic.html', time: 10, prereqs: ['calc', 'stats'], badge: null },
      { id: 'knn', num: '12', title: 'k-Nearest Neighbors', short: 'k-Nearest Neighbors', blurb: 'Lazy learning, distance metrics',
        file: 'topics/12-knn.html', time: 6, prereqs: ['mlconcepts'], badge: null },
      { id: 'naivebayes', num: '13', title: 'Naive Bayes', short: 'Naive Bayes', blurb: 'Conditional independence, Laplace',
        file: 'topics/13-naive-bayes.html', time: 6, prereqs: ['prob'], badge: null },
      { id: 'svm', num: '14', title: 'Support Vector Machines', short: 'Support Vector Machines', blurb: 'Margin, kernel trick, soft margin',
        file: 'topics/14-svm.html', time: 12, prereqs: ['calc', 'linlog'], badge: null },
      { id: 'dtree', num: '15', title: 'Decision Trees', short: 'Decision Trees', blurb: 'Gini, entropy, pruning',
        file: 'topics/15-decision-trees.html', time: 8, prereqs: ['mlconcepts'], badge: null },
      { id: 'rf', num: '16', title: 'Random Forest', short: 'Random Forest', blurb: 'Bagging, OOB, feature importance',
        file: 'topics/16-random-forest.html', time: 8, prereqs: ['dtree'], badge: null },
      { id: 'boosting', num: '17', title: 'Gradient Boosting', short: 'Gradient Boosting', blurb: 'GBM, LightGBM, CatBoost',
        file: 'topics/17-gradient-boosting.html', time: 10, prereqs: ['dtree', 'calc'], badge: null },
      { id: 'xgb', num: '18', title: 'XGBoost Deep Dive', short: 'XGBoost Deep Dive', blurb: 'Obj function, Taylor expansion, split gain',
        file: 'topics/18-xgboost.html', time: 12, prereqs: ['boosting'], badge: null },
      { id: 'clustering', num: '19', title: 'Clustering', short: 'Clustering', blurb: 'K-Means, DBSCAN, hierarchical',
        file: 'topics/19-clustering.html', time: 10, prereqs: ['linalg', 'metrics'], badge: null },
      { id: 'dimred', num: '20', title: 'Dimensionality Reduction', short: 'Dimensionality Reduction', blurb: 'PCA, t-SNE, UMAP',
        file: 'topics/20-dimensionality-reduction.html', time: 10, prereqs: ['linalg', 'prob'], badge: null },
    ],
  },
  {
    id: 'dataeng', icon: '⚙️', label: 'Data & Model Engineering',
    topics: [
      { id: 'featureeng', num: '21', title: 'Feature Engineering', short: 'Feature Engineering', blurb: 'Encoding, scaling, interactions',
        file: 'topics/21-feature-engineering.html', time: 10, prereqs: ['mlconcepts'], badge: null },
      { id: 'imbalanced', num: '22', title: 'Imbalanced Datasets', short: 'Imbalanced Datasets', blurb: 'SMOTE, class weights, threshold',
        file: 'topics/22-imbalanced.html', time: 8, prereqs: ['metrics', 'featureeng'], badge: null },
      { id: 'reg', num: '23', title: 'Regularization', short: 'Regularization', blurb: 'L1, L2, dropout, early stopping',
        file: 'topics/23-regularization.html', time: 8, prereqs: ['linlog', 'calc'], badge: null },
      { id: 'hyperparam', num: '24', title: 'Hyperparameter Tuning', short: 'Hyperparameter Tuning', blurb: 'Grid, random, Bayesian, Optuna',
        file: 'topics/24-hyperparameter-tuning.html', time: 8, prereqs: ['biasvar', 'crossval'], badge: null },
      { id: 'ensemble', num: '25', title: 'Ensemble Methods', short: 'Ensemble Methods', blurb: 'Bagging, boosting, stacking, blending',
        file: 'topics/25-ensemble-methods.html', time: 8, prereqs: ['dtree', 'rf'], badge: null },
    ],
  },
  {
    id: 'nn', icon: '🧠', label: 'Neural Network Foundations',
    topics: [
      { id: 'nn_basics', num: '26', title: 'Perceptron & MLP', short: 'Perceptron & MLP', blurb: 'Layers, forward pass, universal approx.',
        file: 'topics/26-mlp.html', time: 12, prereqs: ['calc', 'linalg'], badge: null },
      { id: 'activations', num: '27', title: 'Activation Functions', short: 'Activation Functions', blurb: 'ReLU, sigmoid, GELU, softmax',
        file: 'topics/27-activations.html', time: 8, prereqs: ['nn_basics'], badge: null },
      { id: 'loss', num: '28', title: 'Loss Functions', short: 'Loss Functions', blurb: 'BCE, MSE, focal loss, KL divergence',
        file: 'topics/28-loss-functions.html', time: 14, prereqs: ['nn_basics', 'prob'], badge: null },
      { id: 'backprop', num: '29', title: 'Backpropagation & Training Loop', short: 'Backpropagation & Training Loop', blurb: 'Chain rule, GD steps, zero_grad, clip',
        file: 'topics/29-backpropagation.html', time: 18, prereqs: ['nn_basics', 'calc'], badge: null },
      { id: 'optim', num: '30', title: 'Optimizers', short: 'Optimizers', blurb: 'SGD, Adam, AdamW, warmup schedules',
        file: 'topics/30-optimizers.html', time: 10, prereqs: ['backprop'], badge: null },
      { id: 'weightinit', num: '31', title: 'Weight Initialization', short: 'Weight Initialization', blurb: 'Xavier, He, orthogonal init',
        file: 'topics/31-weight-init.html', time: 6, prereqs: ['nn_basics', 'calc'], badge: null },
    ],
  },
  {
    id: 'dl', icon: '🤖', label: 'Deep Learning Architectures',
    topics: [
      { id: 'cnn', num: '32', title: 'CNNs', short: 'CNNs', blurb: 'Convolution, pooling, ResNet, EfficientNet',
        file: 'topics/32-cnns.html', time: 14, prereqs: ['nn_basics', 'backprop'], badge: null },
      { id: 'rnn', num: '33', title: 'RNNs & LSTMs', short: 'RNNs & LSTMs', blurb: 'Sequence modelling, gates, BPTT',
        file: 'topics/33-rnns-lstms.html', time: 12, prereqs: ['nn_basics', 'backprop'], badge: null },
      { id: 'attention', num: '34', title: 'Attention & Architecture', short: 'Attention & Architecture', blurb: 'Q/K/V, multi-head, RNN→GPT lineage',
        file: 'topics/34-attention-architecture.html', time: 20, prereqs: ['rnn', 'linalg'], badge: null },
      { id: 'transformers', num: '35', title: 'Transformers', short: 'Transformers', blurb: 'Encoder-decoder, positional encoding',
        file: 'topics/35-transformers.html', time: 14, prereqs: ['attention'], badge: null },
      { id: 'transfer', num: '36', title: 'Transfer & Distillation', short: 'Transfer & Distillation', blurb: 'Fine-tuning, LoRA, teacher-student',
        file: 'topics/36-transfer-distillation.html', time: 14, prereqs: ['cnn', 'transformers'], badge: null },
    ],
  },
  {
    id: 'nlp', icon: '💬', label: 'NLP & Language Models',
    topics: [
      { id: 'tokenization', num: '37', title: 'Tokenization & Embeddings', short: 'Tokenization & Embeddings', blurb: 'BPE, WordPiece, Word2Vec, BERT embed',
        file: 'topics/37-tokenization-embeddings.html', time: 8, prereqs: ['prob'], badge: null },
      { id: 'bert', num: '38', title: 'BERT & Encoder Models', short: 'BERT & Encoder Models', blurb: 'MLM, bidirectional context, NSP',
        file: 'topics/38-bert.html', time: 8, prereqs: ['transformers', 'tokenization'], badge: null },
      { id: 'llm', num: '39', title: 'LLMs, SLMs & RLHF', short: 'LLMs, SLMs & RLHF', blurb: 'GPT, Claude, SLMs, PPO fine-tuning',
        file: 'topics/39-llms-rlhf.html', time: 12, prereqs: ['bert', 'optim'], badge: null },
    ],
  },
  {
    id: 'llmera', icon: '✨', label: 'LLM Era',
    topics: [
      { id: 'rag', num: '48', title: 'RAG & Retrieval', short: 'RAG & Retrieval', blurb: 'Chunking, hybrid search, reranking, RAGAS eval',
        file: 'topics/48-rag.html', time: 14, prereqs: ['llm', 'vectordb'], badge: 'new' },
      { id: 'vectordb', num: '49', title: 'Vector Databases', short: 'Vector Databases', blurb: 'FAISS, HNSW, ANN search, embedding pipelines',
        file: 'topics/49-vector-databases.html', time: 10, prereqs: ['linalg', 'tokenization'], badge: 'new' },
      { id: 'agents', num: '50', title: 'Agentic AI', short: 'Agentic AI', blurb: 'ReAct, tool calling, multi-agent, memory, guardrails',
        file: 'topics/50-agentic-ai.html', time: 14, prereqs: ['llm', 'rag'], badge: 'new' },
      { id: 'multimodal', num: '54', title: 'Multimodal Models', short: 'Multimodal Models', blurb: 'CLIP, LLaVA, vision-language, image-text embeddings',
        file: 'topics/54-multimodal.html', time: 12, prereqs: ['cnn', 'bert'], badge: 'new' },
    ],
  },
  {
    id: 'domains', icon: '📡', label: 'Specialized Domains',
    topics: [
      { id: 'timeseries', num: '40', title: 'Time Series Modeling', short: 'Time Series Modeling', blurb: 'ARIMA, Prophet, LSTM forecasting',
        file: 'topics/40-time-series.html', time: 12, prereqs: ['stats', 'rnn'], badge: null },
      { id: 'creditrisk', num: '41', title: 'Credit Risk & Scorecards', short: 'Credit Risk & Scorecards', blurb: 'PD, LGD, scorecard, WOE/IV',
        file: 'topics/41-credit-risk.html', time: 12, prereqs: ['linlog', 'xgb', 'metrics'], badge: null },
      { id: 'gnns', num: '46', title: 'Graph Neural Networks', short: 'Graph Neural Networks', blurb: 'Message passing, GraphSAGE, GCN, link prediction',
        file: 'topics/46-gnns.html', time: 12, prereqs: ['nn_basics', 'linalg'], badge: 'new' },
      { id: 'responsibleai', num: '51', title: 'Responsible AI & Fairness', short: 'Responsible AI & Fairness', blurb: 'Bias metrics, demographic parity, model cards, governance',
        file: 'topics/51-responsible-ai.html', time: 10, prereqs: ['metrics', 'mlconcepts'], badge: 'new' },
      { id: 'causal', num: '52', title: 'Causal Inference & A/B Testing', short: 'Causal Inference & A/B Testing', blurb: 'Power, uplift models, DiD, DoWhy',
        file: 'topics/52-causal-inference.html', time: 14, prereqs: ['stats', 'prob'], badge: 'new' },
      { id: 'dataeng', num: '53', title: 'Data Engineering for ML', short: 'Data Engineering for ML', blurb: 'dbt, Spark, feature pipelines, Delta Lake',
        file: 'topics/53-data-engineering.html', time: 12, prereqs: ['featureeng'], badge: 'new' },
      { id: 'bipartite', num: '55', title: 'Bipartite Graphs in ML', blurb: 'Recommendations, matching, collaborative filtering', short: 'Bipartite Graphs',
        file: 'topics/46-bipartite-graphs.html', time: 10, prereqs: ['gnns', 'linalg'], badge: 'new' },
    ],
  },
  {
    id: 'prod', icon: '🚀', label: 'Production & System Design',
    topics: [
      { id: 'mlops', num: '42', title: 'MLOps & Deployment', short: 'MLOps & Deployment', blurb: 'CI/CD, model drift, feature stores',
        file: 'topics/42-mlops.html', time: 12, prereqs: ['nn_basics', 'featureeng'], badge: null },
      { id: 'systemdesign', num: '43', title: 'ML System Design', short: 'ML System Design', blurb: 'Recsys, fraud, search, latency',
        file: 'topics/43-system-design.html', time: 12, prereqs: ['mlops', 'metrics'], badge: null },
      { id: 'coding', num: '44', title: 'Python, SQL & DSA', short: 'Python, SQL & DSA', blurb: 'Pandas, SQL joins, sliding windows',
        file: 'topics/44-python-sql-dsa.html', time: 12, prereqs: [], badge: null },
      { id: 'compare', num: '45', title: 'Model Cheatsheet', short: 'Model Cheatsheet', blurb: 'Algorithm comparison, when to use what',
        file: 'topics/45-model-cheatsheet.html', time: 8, prereqs: [], badge: null },
      { id: 'frameworks', num: '47', title: 'TF, Keras & PyTorch', short: 'TF, Keras & PyTorch', blurb: 'Framework comparison, training APIs',
        file: 'topics/47-tf-keras-pytorch.html', time: 14, prereqs: ['backprop'], badge: null },
    ],
  },
];

/* ---- Derived lookups: built once, never hand-maintained ---- */
export const TOPICS = GROUPS.flatMap(g =>
  g.topics.map(t => ({ ...t, group: g.id, groupLabel: g.label, groupIcon: g.icon }))
);

export const BY_ID = Object.fromEntries(TOPICS.map(t => [t.id, t]));

/* Reading order for prev/next — sidebar order, which is the intended path. */
export const ORDER = TOPICS.map(t => t.id);

export const TOTAL = TOPICS.length;

export const HOME = { id: 'home', file: 'topics/00-home.html', title: 'Home', short: 'Home' };
