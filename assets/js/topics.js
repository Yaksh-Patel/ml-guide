/* ==========================================================
   topics.js — SINGLE SOURCE OF TRUTH for the guide's contents.

   Add a topic here and it appears everywhere: sidebar, home grid,
   learning-path map, search index, prev/next order, progress
   total, breadcrumbs. Nothing else needs editing.

   Order in this file IS the reading order and the numbering.
   Keep `num` matching the topic's position, and keep the file
   name prefixed with the same number.

   id       stable slug; the URL hash, and the topic file's root
            section must be  id="sec-<id>"
   num      display number
   title    full title (breadcrumb, map tooltip, home card)
   blurb    one line shown on the home card
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
      { id: 'linalg', num: '01', title: 'Linear Algebra', blurb: 'Vectors, matrices, eigenvalues, SVD', short: 'Linear Algebra',
        file: 'topics/01-linear-algebra.html', time: 12, prereqs: [], badge: null },
      { id: 'prob', num: '02', title: 'Probability Theory', blurb: 'Bayes, distributions, expectation', short: 'Probability Theory',
        file: 'topics/02-probability.html', time: 10, prereqs: ['linalg'], badge: null },
      { id: 'stats', num: '03', title: 'Statistics & Inference', blurb: 'p-values, CI, hypothesis tests', short: 'Statistics & Inference',
        file: 'topics/03-statistics.html', time: 10, prereqs: ['prob'], badge: null },
      { id: 'calc', num: '04', title: 'Calculus & Optimization', blurb: 'Gradients, chain rule, convexity', short: 'Calculus & Optimization',
        file: 'topics/04-calculus.html', time: 12, prereqs: ['linalg'], badge: null },
    ],
  },
  {
    id: 'mlthink', icon: '🧭', label: 'ML Thinking & Evaluation',
    topics: [
      { id: 'mlconcepts', num: '05', title: 'ML Paradigms', blurb: 'Supervised, unsupervised, semi-, RL', short: 'ML Paradigms',
        file: 'topics/05-ml-paradigms.html', time: 8, prereqs: ['stats'], badge: null },
      { id: 'biasvar', num: '06', title: 'Bias-Variance Tradeoff', blurb: 'Overfitting, underfitting tradeoff', short: 'Bias-Variance Tradeoff',
        file: 'topics/06-bias-variance.html', time: 8, prereqs: ['mlconcepts'], badge: null },
      { id: 'crossval', num: '07', title: 'Cross-Validation', blurb: 'k-fold, stratified, time-series split', short: 'Cross-Validation',
        file: 'topics/07-cross-validation.html', time: 10, prereqs: ['biasvar'], badge: null },
      { id: 'metrics', num: '08', title: 'Evaluation Metrics', blurb: 'MSE, MAE, accuracy, F1, RMSE', short: 'Evaluation Metrics',
        file: 'topics/08-eval-metrics.html', time: 8, prereqs: ['mlconcepts'], badge: null },
      { id: 'confusion', num: '09', title: 'Confusion Matrix & ROC', blurb: 'TP/FP/AUC/KS/PR-AUC', short: 'Confusion Matrix & ROC',
        file: 'topics/09-confusion-roc.html', time: 8, prereqs: ['metrics'], badge: null },
      { id: 'calibration', num: '10', title: 'Calibration & Explainability', blurb: 'Reliability diagrams, LIME, SHAP', short: 'Calibration & Explainability',
        file: 'topics/10-calibration-explainability.html', time: 10, prereqs: ['confusion'], badge: null },
    ],
  },
  {
    id: 'classical', icon: '🌳', label: 'Classical ML Algorithms',
    topics: [
      { id: 'linlog', num: '11', title: 'Linear & Logistic Regression', blurb: 'OLS, sigmoid, assumptions', short: 'Linear & Logistic Regression',
        file: 'topics/11-linear-logistic.html', time: 10, prereqs: ['calc', 'stats'], badge: null },
      { id: 'knn', num: '12', title: 'k-Nearest Neighbors', blurb: 'Lazy learning, distance metrics', short: 'k-Nearest Neighbors',
        file: 'topics/12-knn.html', time: 6, prereqs: ['mlconcepts'], badge: null },
      { id: 'naivebayes', num: '13', title: 'Naive Bayes', blurb: 'Conditional independence, Laplace', short: 'Naive Bayes',
        file: 'topics/13-naive-bayes.html', time: 6, prereqs: ['prob'], badge: null },
      { id: 'svm', num: '14', title: 'Support Vector Machines', blurb: 'Margin, kernel trick, soft margin', short: 'Support Vector Machines',
        file: 'topics/14-svm.html', time: 12, prereqs: ['calc', 'linlog'], badge: null },
      { id: 'dtree', num: '15', title: 'Decision Trees', blurb: 'Gini, entropy, pruning', short: 'Decision Trees',
        file: 'topics/15-decision-trees.html', time: 8, prereqs: ['mlconcepts'], badge: null },
      { id: 'rf', num: '16', title: 'Random Forest', blurb: 'Bagging, OOB, feature importance', short: 'Random Forest',
        file: 'topics/16-random-forest.html', time: 8, prereqs: ['dtree'], badge: null },
      { id: 'boosting', num: '17', title: 'Gradient Boosting', blurb: 'GBM, LightGBM, CatBoost', short: 'Gradient Boosting',
        file: 'topics/17-gradient-boosting.html', time: 10, prereqs: ['dtree', 'calc'], badge: null },
      { id: 'xgb', num: '18', title: 'XGBoost Deep Dive', blurb: 'Obj function, Taylor expansion, split gain', short: 'XGBoost Deep Dive',
        file: 'topics/18-xgboost.html', time: 12, prereqs: ['boosting'], badge: null },
      { id: 'clustering', num: '19', title: 'Clustering', blurb: 'K-Means, DBSCAN, hierarchical', short: 'Clustering',
        file: 'topics/19-clustering.html', time: 10, prereqs: ['linalg', 'metrics'], badge: null },
      { id: 'dimred', num: '20', title: 'Dimensionality Reduction', blurb: 'PCA, t-SNE, UMAP', short: 'Dimensionality Reduction',
        file: 'topics/20-dimensionality-reduction.html', time: 10, prereqs: ['linalg', 'prob'], badge: null },
    ],
  },
  {
    id: 'dataeng', icon: '⚙️', label: 'Data & Model Engineering',
    topics: [
      { id: 'featureeng', num: '21', title: 'Feature Engineering', blurb: 'Encoding, scaling, interactions', short: 'Feature Engineering',
        file: 'topics/21-feature-engineering.html', time: 10, prereqs: ['mlconcepts'], badge: null },
      { id: 'imbalanced', num: '22', title: 'Imbalanced Datasets', blurb: 'SMOTE, class weights, threshold', short: 'Imbalanced Datasets',
        file: 'topics/22-imbalanced.html', time: 8, prereqs: ['metrics', 'featureeng'], badge: null },
      { id: 'reg', num: '23', title: 'Regularization', blurb: 'L1, L2, dropout, early stopping', short: 'Regularization',
        file: 'topics/23-regularization.html', time: 8, prereqs: ['linlog', 'calc'], badge: null },
      { id: 'hyperparam', num: '24', title: 'Hyperparameter Tuning', blurb: 'Grid, random, Bayesian, Optuna', short: 'Hyperparameter Tuning',
        file: 'topics/24-hyperparameter-tuning.html', time: 8, prereqs: ['biasvar', 'crossval'], badge: null },
      { id: 'ensemble', num: '25', title: 'Ensemble Methods', blurb: 'Bagging, boosting, stacking, blending', short: 'Ensemble Methods',
        file: 'topics/25-ensemble-methods.html', time: 8, prereqs: ['dtree', 'rf'], badge: null },
    ],
  },
  {
    id: 'nn', icon: '🧠', label: 'Neural Network Foundations',
    topics: [
      { id: 'nn_basics', num: '26', title: 'Perceptron & MLP', blurb: 'Layers, forward pass, universal approx.', short: 'Perceptron & MLP',
        file: 'topics/26-mlp.html', time: 12, prereqs: ['calc', 'linalg'], badge: null },
      { id: 'activations', num: '27', title: 'Activation Functions', blurb: 'ReLU, sigmoid, GELU, softmax', short: 'Activation Functions',
        file: 'topics/27-activations.html', time: 8, prereqs: ['nn_basics'], badge: null },
      { id: 'loss', num: '28', title: 'Loss Functions', blurb: 'BCE, MSE, focal loss, KL divergence', short: 'Loss Functions',
        file: 'topics/28-loss-functions.html', time: 14, prereqs: ['nn_basics', 'prob'], badge: null },
      { id: 'backprop', num: '29', title: 'Backpropagation & Training Loop', blurb: 'Chain rule, GD steps, zero_grad, clip', short: 'Backpropagation & Training Loop',
        file: 'topics/29-backpropagation.html', time: 18, prereqs: ['nn_basics', 'calc'], badge: null },
      { id: 'optim', num: '30', title: 'Optimizers', blurb: 'SGD, Adam, AdamW, warmup schedules', short: 'Optimizers',
        file: 'topics/30-optimizers.html', time: 10, prereqs: ['backprop'], badge: null },
      { id: 'weightinit', num: '31', title: 'Weight Initialization', blurb: 'Xavier, He, orthogonal init', short: 'Weight Initialization',
        file: 'topics/31-weight-init.html', time: 6, prereqs: ['nn_basics', 'calc'], badge: null },
    ],
  },
  {
    id: 'dl', icon: '🤖', label: 'Deep Learning Architectures',
    topics: [
      { id: 'cnn', num: '32', title: 'CNNs', blurb: 'Convolution, pooling, ResNet, EfficientNet', short: 'CNNs',
        file: 'topics/32-cnns.html', time: 14, prereqs: ['nn_basics', 'backprop'], badge: null },
      { id: 'rnn', num: '33', title: 'RNNs & LSTMs', blurb: 'Sequence modelling, gates, BPTT', short: 'RNNs & LSTMs',
        file: 'topics/33-rnns-lstms.html', time: 12, prereqs: ['nn_basics', 'backprop'], badge: null },
      { id: 'attention', num: '34', title: 'Attention & Architecture', blurb: 'Q/K/V, multi-head, RNN→GPT lineage', short: 'Attention & Architecture',
        file: 'topics/34-attention-architecture.html', time: 20, prereqs: ['rnn', 'linalg'], badge: null },
      { id: 'transformers', num: '35', title: 'Transformers', blurb: 'Encoder-decoder, positional encoding', short: 'Transformers',
        file: 'topics/35-transformers.html', time: 14, prereqs: ['attention'], badge: null },
      { id: 'transfer', num: '36', title: 'Transfer & Distillation', blurb: 'Fine-tuning, LoRA, teacher-student', short: 'Transfer & Distillation',
        file: 'topics/36-transfer-distillation.html', time: 14, prereqs: ['cnn', 'transformers'], badge: null },
    ],
  },
  {
    id: 'nlp', icon: '💬', label: 'NLP & Language Models',
    topics: [
      { id: 'tokenization', num: '37', title: 'Tokenization & Embeddings', blurb: 'BPE, WordPiece, Word2Vec, BERT embed', short: 'Tokenization & Embeddings',
        file: 'topics/37-tokenization-embeddings.html', time: 8, prereqs: ['prob'], badge: null },
      { id: 'bert', num: '38', title: 'BERT & Encoder Models', blurb: 'MLM, bidirectional context, NSP', short: 'BERT & Encoder Models',
        file: 'topics/38-bert.html', time: 8, prereqs: ['transformers', 'tokenization'], badge: null },
      { id: 'llm', num: '39', title: 'LLMs, SLMs & RLHF', blurb: 'GPT, Claude, SLMs, PPO fine-tuning', short: 'LLMs, SLMs & RLHF',
        file: 'topics/39-llms-rlhf.html', time: 12, prereqs: ['bert', 'optim'], badge: null },
    ],
  },
  {
    id: 'llmera', icon: '✨', label: 'The LLM Era',
    topics: [
      { id: 'rag', num: '40', title: 'RAG & Retrieval', blurb: 'Chunking, hybrid search, reranking, RAGAS eval', short: 'RAG & Retrieval',
        file: 'topics/40-rag.html', time: 14, prereqs: ['llm', 'vectordb'], badge: 'new' },
      { id: 'vectordb', num: '41', title: 'Vector Databases', blurb: 'FAISS, HNSW, ANN search, embedding pipelines', short: 'Vector Databases',
        file: 'topics/41-vector-databases.html', time: 10, prereqs: ['linalg', 'tokenization'], badge: 'new' },
      { id: 'agents', num: '42', title: 'Agentic AI', blurb: 'ReAct, tool calling, multi-agent, memory, guardrails', short: 'Agentic AI',
        file: 'topics/42-agentic-ai.html', time: 14, prereqs: ['llm', 'rag'], badge: 'new' },
      { id: 'multimodal', num: '43', title: 'Multimodal Models', blurb: 'CLIP, LLaVA, vision-language, image-text embeddings', short: 'Multimodal Models',
        file: 'topics/43-multimodal.html', time: 12, prereqs: ['cnn', 'bert'], badge: 'new' },
    ],
  },
  {
    id: 'domains', icon: '📡', label: 'Specialised Domains',
    topics: [
      { id: 'timeseries', num: '44', title: 'Time Series Modeling', blurb: 'ARIMA, Prophet, LSTM forecasting', short: 'Time Series Modeling',
        file: 'topics/44-time-series.html', time: 12, prereqs: ['stats', 'rnn'], badge: null },
      { id: 'creditrisk', num: '45', title: 'Credit Risk & Scorecards', blurb: 'PD, LGD, scorecard, WOE/IV', short: 'Credit Risk & Scorecards',
        file: 'topics/45-credit-risk.html', time: 12, prereqs: ['linlog', 'xgb', 'metrics'], badge: null },
      { id: 'gnns', num: '46', title: 'Graph Neural Networks', blurb: 'Message passing, GraphSAGE, GCN, link prediction', short: 'Graph Neural Networks',
        file: 'topics/46-gnns.html', time: 12, prereqs: ['nn_basics', 'linalg'], badge: 'new' },
      { id: 'bipartite', num: '47', title: 'Bipartite Graphs in ML', blurb: 'Recommendations, matching, collaborative filtering', short: 'Bipartite Graphs',
        file: 'topics/47-bipartite-graphs.html', time: 10, prereqs: ['gnns', 'linalg'], badge: 'new' },
      { id: 'causal', num: '48', title: 'Causal Inference & A/B Testing', blurb: 'Power, uplift models, DiD, DoWhy', short: 'Causal Inference & A/B Testing',
        file: 'topics/48-causal-inference.html', time: 14, prereqs: ['stats', 'prob'], badge: 'new' },
      { id: 'responsibleai', num: '49', title: 'Responsible AI & Fairness', blurb: 'Bias metrics, demographic parity, model cards, governance', short: 'Responsible AI & Fairness',
        file: 'topics/49-responsible-ai.html', time: 10, prereqs: ['metrics', 'mlconcepts'], badge: 'new' },
    ],
  },
  {
    id: 'prod', icon: '🚀', label: 'Production & MLOps',
    topics: [
      { id: 'pipelines', num: '50', title: 'Data Engineering for ML', blurb: 'dbt, Spark, feature pipelines, Delta Lake', short: 'Data Engineering for ML',
        file: 'topics/50-data-engineering.html', time: 12, prereqs: ['featureeng'], badge: 'new' },
      { id: 'mlops', num: '51', title: 'MLOps & Deployment', blurb: 'CI/CD, model drift, feature stores', short: 'MLOps & Deployment',
        file: 'topics/51-mlops.html', time: 12, prereqs: ['nn_basics', 'featureeng'], badge: null },
      { id: 'systemdesign', num: '52', title: 'ML System Design', blurb: 'Recsys, fraud, search, latency', short: 'ML System Design',
        file: 'topics/52-system-design.html', time: 12, prereqs: ['mlops', 'metrics'], badge: null },
      { id: 'coding', num: '53', title: 'Python, SQL & DSA', blurb: 'Pandas, SQL joins, sliding windows', short: 'Python, SQL & DSA',
        file: 'topics/53-python-sql-dsa.html', time: 12, prereqs: [], badge: null },
    ],
  },
  {
    id: 'ref', icon: '📎', label: 'Reference',
    topics: [
      { id: 'compare', num: '54', title: 'Model Cheatsheet', blurb: 'Algorithm comparison, when to use what', short: 'Model Cheatsheet',
        file: 'topics/54-model-cheatsheet.html', time: 8, prereqs: [], badge: null },
      { id: 'frameworks', num: '55', title: 'TF, Keras & PyTorch', blurb: 'Framework comparison, training APIs', short: 'TF, Keras & PyTorch',
        file: 'topics/55-tf-keras-pytorch.html', time: 14, prereqs: ['backprop'], badge: null },
    ],
  },
];

/* ---- Derived lookups: built once, never hand-maintained ---- */
export const TOPICS = GROUPS.flatMap(g =>
  g.topics.map(t => ({ ...t, group: g.id, groupLabel: g.label, groupIcon: g.icon }))
);

export const BY_ID = Object.fromEntries(TOPICS.map(t => [t.id, t]));
export const ORDER = TOPICS.map(t => t.id);
export const TOTAL = TOPICS.length;

export const HOME = { id: 'home', file: 'topics/00-home.html', title: 'Home', short: 'Home' };
