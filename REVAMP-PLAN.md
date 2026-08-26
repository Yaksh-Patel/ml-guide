# Content revamp — working plan

Progress tracker for the per-topic prose rewrite. Kept in the repo so the work
survives a context reset. Delete this file when every topic is marked done.

## Why

Structure, chronology, maths, code and diagrams are done for all 55 topics.
The remaining gap is the writing itself, and it is uneven: topics written first
are thin and note-like, topics written later are much fuller.

    01–25   ~6–13 KB   terse, bullet-heavy, assumes the reader already knows
    34–55   ~18–39 KB  fuller, better framed

## What "revamped" means for a topic

1. **Opening that earns the topic.** `sec-desc` states what the thing is *for*
   and what breaks without it — not a definition restated from the title.
2. **Intuition before formalism.** One concrete mental model, then the maths.
3. **Maths that is explained, not dumped.** Every symbol named on first use;
   say what the formula *does*, not just what it equals.
4. **A worked number.** At least one place where real values go through the
   formula, so the reader can check themselves.
5. **The failure mode.** What goes wrong in practice, why, and the symptom you
   would actually observe.
6. **Interview framing.** The question as it is really asked, and what a strong
   answer contains — no "they may ask about X".
7. **Keep** the existing diagram, code card, tables and callouts. Rewrite prose
   around them; do not delete working assets.
8. **Voice.** Direct, specific, no filler. Prefer "a model that leaks future
   information scores beautifully offline and loses money in production" over
   "data leakage is an important consideration".

## Chunks

Ordered thinnest-and-most-foundational first, since those are read most and
are currently weakest. One chunk per session-batch; commit after each.

- [ ] C1  01 linear-algebra · 02 probability · 03 statistics · 04 calculus
- [ ] C2  05 ml-paradigms · 06 bias-variance · 07 cross-validation
- [ ] C3  08 eval-metrics · 09 confusion-roc · 10 calibration
- [ ] C4  11 linear-logistic · 12 knn · 13 naive-bayes
- [ ] C5  14 svm · 15 decision-trees · 16 random-forest
- [ ] C6  17 gradient-boosting · 18 xgboost · 19 clustering · 20 dimred
- [ ] C7  21 feature-engineering · 22 imbalanced · 23 regularization
- [ ] C8  24 hyperparameter-tuning · 25 ensemble-methods
- [ ] C9  26 mlp · 27 activations · 28 loss-functions
- [ ] C10 29 backpropagation · 30 optimizers · 31 weight-init
- [ ] C11 32 cnns · 33 rnns-lstms
- [ ] C12 34 attention · 35 transformers · 36 transfer-distillation
- [ ] C13 37 tokenization · 38 bert · 39 llms-rlhf
- [ ] C14 40 rag · 41 vector-databases
- [ ] C15 42 agentic-ai · 43 multimodal
- [ ] C16 44 time-series · 45 credit-risk
- [ ] C17 46 gnns · 47 bipartite-graphs
- [ ] C18 48 causal-inference · 49 responsible-ai
- [ ] C19 50 data-engineering · 51 mlops · 52 system-design
- [ ] C20 53 python-sql-dsa · 54 model-cheatsheet · 55 tf-keras-pytorch

## Invariants to re-check after every chunk

    python3 - <<'EOF'
    # div/section balance, paired $$, one <section> per file
    EOF
    node run.mjs <repo>          # jsdom smoke test in the scratchpad

- root element stays `<section class="section" id="sec-<id>">`
- no page-level `<style>` blocks in topic files
- no `{{` or `{%` outside a `<pre>`/`<textarea>` (dbt snippets are fine now
  that `.nojekyll` exists, but keep them inside code blocks)
- `assets/js/topics.js` is the only place topic metadata lives
