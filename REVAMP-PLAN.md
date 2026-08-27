# ML Atlas — content revamp: state and handoff

Live: **https://yaksh-patel.github.io/ml-guide/**
Repo: `Yaksh-Patel/ml-guide`, branch `main`, local clone at
`~/Documents/Personal/Claude_Projects/ml-guide-main`

This file is the working state of a long content rewrite. It is kept in the
repo deliberately, so the work survives closing a session. **Read this before
touching anything.** Delete the file when every chunk is checked off.

---

## 1. Where things stand

Structure, chronology, maths rendering, code examples and diagrams are **done
for all 55 topics**. The remaining work is the prose itself.

| Aspect | State |
|---|---|
| Chronology / numbering | done — 01–55 in reading order, filename number = position |
| Groups | done — 11 groups, `assets/js/topics.js` is the single source of truth |
| Maths rendering | done — KaTeX loads lazily; detector handles multi-line `$$` |
| Code example | done — all 55 topics |
| Diagram | done — all 55 topics |
| Markup validity | done — all 56 fragments balanced, `$$` paired |
| **Prose quality** | **C1–C5 done (16 topics), C6–C20 remaining (39 topics)** |

### Prose progress: 16 / 55

- [x] C1  01 linear-algebra · 02 probability · 03 statistics · 04 calculus
- [x] C2  05 ml-paradigms · 06 bias-variance · 07 cross-validation
- [x] C3  08 eval-metrics · 09 confusion-roc · 10 calibration
- [x] C4  11 linear-logistic · 12 knn · 13 naive-bayes
- [x] C5  14 svm · 15 decision-trees · 16 random-forest
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

One chunk per batch. **Commit and push after each chunk**, and tick the box in
this file as part of that commit.

---

## 2. The quality bar for a revamped topic

1. **An opening that earns the topic.** `sec-desc` says what the thing is *for*
   and what breaks without it. Not a definition restated from the title.
2. **Intuition before formalism.** One concrete mental model, then the maths.
   ("A vector is one row of your dataframe." "Conditioning is shrinking the
   world." "Eigenvectors are the directions a transform does not turn.")
3. **Maths that is explained.** Name every symbol on first use. Say what the
   formula *does*, not only what it equals. Use `\underbrace` labels where a
   term has a name worth learning.
4. **A worked number.** At least one place where real values pass through the
   formula so the reader can check themselves. These land hardest — e.g.
   `0.25^10 = 9.5e-07` as the vanishing-gradient argument; the 10,000-person
   rare-disease table; TPR 0.90 / FPR 0.009 / precision 0.09 from one model.
5. **Reasons, not rules.** "L1 selects *because its ball has corners on the
   axes*." "PCA uses SVD *because forming XᵀX squares the condition number*."
6. **The failure mode, with its symptom.** What goes wrong in practice and what
   you would actually observe (a gradient-norm curve, a train/val gap, a
   suspiciously good CV score).
7. **Interview framing that gives the answer**, including what *not* to say.
   No "they may ask about X".
8. **Keep every existing asset.** Diagram, code card, tables, callouts. Rewrite
   prose *around* them. See §4 — this is where the real risk is.
9. **Voice.** Direct and specific. Prefer "a model that leaks future
   information scores beautifully offline and loses money in production" to
   "data leakage is an important consideration".

### Open question for the owner
Revamped topics grow roughly 4 KB each (the 10 done went ~118 KB → ~162 KB).
Fragments load on demand so first paint is unaffected. **If you would rather
the remaining chunks be sharper-and-shorter than fuller, say so** — the current
default is "fuller, better framed".

---

## 3. How to do a chunk

Do **not** hand-edit the HTML with f-strings — LaTeX braces fight Python's
f-string escaping and it wasted time twice. Use placeholder substitution:

```bash
# 1. see what assets the topic has
python3 -c "
import sys; sys.path.insert(0,'tools')
from assets import counts, fmt, blocks
import pathlib, re
s = pathlib.Path('topics/11-linear-logistic.html').read_text()
print(fmt(counts(s)))
for b in blocks(s): print(re.sub(r'\s+',' ', b[:90]))
for t in re.findall(r'<div class=\"card-title\">([^<]{0,55})', s): print(' -', t)
"

# 2. write the new body to a temp file with __DIAGRAM__ / __CODECARD__ /
#    __INTERACTIVE__ / __TABLE__ placeholders  (heredoc with quoted 'EOF',
#    so nothing is expanded)
cat > /tmp/t11.html <<'HTMLEOF'
<section class="section" id="sec-linlog">
...
__DIAGRAM__
...
__CODECARD__
</section>
HTMLEOF

# 3. substitute the preserved assets back in
python3 - <<'PY'
import sys, pathlib; sys.path.insert(0,'tools')
from assets import blocks, codecard
src = pathlib.Path('topics/11-linear-logistic.html').read_text()
bl = blocks(src)
new = (pathlib.Path('/tmp/t11.html').read_text()
       .replace('__DIAGRAM__', bl[0] if bl else '')
       .replace('__CODECARD__', codecard(src)))
pathlib.Path('topics/11-linear-logistic.html').write_text(new)
PY

# 4. validate — both of these, every time
python3 tools/check_topics.py 11-linear-logistic
python3 tools/assets.py cdf20c9 11-linear-logistic

# 5. smoke-test the app, then commit + push and tick the box here
```

---

## 4. Asset retention — the one thing that has actually gone wrong

Two interactive widgets were nearly lost during C2/C3:

* **`06-bias-variance`** — its Bias-Variance Explorer wrapper carries a
  `style` attribute, so matching the literal `<div class="anim-wrap">` missed it.
* **`09-confusion-roc`** — its ROC explorer keeps its `<script>` **outside**
  the wrapper div, so a div-depth walk alone dropped the script and left a dead
  widget.

`tools/assets.py` handles both. **Use `blocks()` from it; never hand-roll the
regex.** And always run:

```bash
python3 tools/assets.py cdf20c9 <topics...>
```

`cdf20c9` is the commit immediately before the prose revamp began, so it is the
correct baseline. **Any count going down is a lost asset, not a simplification.**

---

## 5. Invariants

- Root element stays `<section class="section" id="sec-<id>">`, one per file.
  The router looks the section up by that id; it must match `topics.js`.
- `div`/`section` balanced, `$$` paired — `tools/check_topics.py` checks both
  with a real HTML parser, not a line count.
- No page-level `<style>` blocks in topic files. `assets/style.css` owns styling.
- Diagram colours use the **legacy palette hexes** (`#5ba4fb`, `#22d3a0`,
  `#f5a623`, `#f06767`, `#b97cf8`, `#4e5a7a`, `#1a1f2e`, `#2e3a58`…). Section 8
  of `style.css` maps those 15 values onto the live design tokens, so diagrams
  follow both themes for free. `tools/svgkit.py` draws in that vocabulary.
- Topic metadata lives **only** in `assets/js/topics.js`.
- `{{` and `{%` are fine now that `.nojekyll` exists, but keep them inside
  `<pre>`/`<textarea>` (there is a dbt snippet in `50-data-engineering`).

---

## 6. Tools in this repo

| Path | Does |
|---|---|
| `tools/check_topics.py` | structural validation. `--all` or named topics |
| `tools/assets.py` | asset accounting vs a baseline commit; `blocks()`, `codecard()` |
| `tools/svgkit.py` | shared SVG vocabulary for diagrams (axes, plot, box, arrow, node, bar) |
| `tools/smoke.mjs` | jsdom smoke test: boots the app, renders home, navigates, checks pager/TOC/progress |

The smoke test needs jsdom, which is not vendored:

```bash
mkdir -p /tmp/domtest && cd /tmp/domtest && npm init -y >/dev/null && npm i jsdom --silent
cp ~/Documents/Personal/Claude_Projects/ml-guide-main/tools/smoke.mjs .
node smoke.mjs ~/Documents/Personal/Claude_Projects/ml-guide-main
# expect: 55 sidebar items, 55 home cards, pager links, "errors: none"
```

---

## 7. Deploy notes (learned the hard way)

- **Push once per chunk.** GitHub Pages cancels an in-progress build when a new
  one starts. Three rapid pushes cancelled each other and a whole commit never
  deployed — it looked like CDN lag but the build had been cancelled.
- **`.nojekyll` is required and present.** This is a plain static site; the
  default Jekyll build was pure overhead and slow enough for pushes to collide.
- **Fragments are CDN-cached for 600s** (`cache-control: max-age=600`). A topic
  can serve old content for ten minutes after a successful deploy. To verify
  content immediately, check `raw.githubusercontent.com`, not the Pages URL.
- Check a build: `curl -s "https://api.github.com/repos/Yaksh-Patel/ml-guide/actions/runs?per_page=3"`
  and parse with `json.load(f, strict=False)` — the payload contains control
  characters that strict JSON rejects.

---

## 8. Recently fixed — do not "re-fix" these

- **Maths rendered as raw LaTeX.** `looksLikeMath` in `assets/js/lazy.js`
  required both `$` on one line; display maths spans newlines. Fixed.
- **Content overlapping the "on this page" rail.** Grid/flex children default
  to `min-width: auto`, so a wide KaTeX block forced its `.g2` column past the
  container. Fixed with `min-width: 0` on card/grid containers plus
  `overflow-x: auto` on `.katex-display`.
- **Diagram labels in a serif fallback.** 294 SVG `text` elements named DM
  Sans / Syne / Inter, which this build no longer loads. One CSS rule in the
  compat layer remaps them.
- **Five pre-existing markup bugs** (unclosed cards in 14/48, stray `</div>` in
  28/29, an orphaned `\end{aligned}$$` printing literal LaTeX in 28). All fixed.
