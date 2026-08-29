# ML Atlas

A field guide to machine learning and data science in 55 topics — maths foundations
through classical ML, neural networks, deep learning, NLP, the LLM era, specialised
domains, and production. Static site, no build step, hosted on GitHub Pages.

Reading order and numbering are defined by the order of `assets/js/topics.js`. The eleven
groups run foundations → thinking → algorithms → engineering → networks → architectures →
NLP → LLM era → domains → production → reference, and file names carry the same number as
the topic's position.

**Live:** https://yaksh-patel.github.io/ml-guide/

**Companion:** [Credit Scorecard Sandbox](https://yaksh-patel.github.io/credit-scorecard-sandbox/)
— an interactive build-and-operate scorecard covering the ground in topics 45, 49 and 52.
Those topics link into the relevant panel; the sandbox links back to the theory.

---

## Adding or editing a topic

### To edit content

Open the topic's file in `topics/`. Each one is a standalone HTML fragment whose root is

```html
<section class="section" id="sec-<id>"> … </section>
```

The `sec-<id>` must match the topic's `id` in the manifest — the router looks the section
up by that. Use the component classes below; don't add page-level `<style>` blocks.

### To add a topic

1. Write `topics/NN-slug.html` with `<section class="section" id="sec-<id>">`.
2. Add one entry to **`assets/js/topics.js`** — the single source of truth:

```js
{ id: 'myid', num: '56', title: 'Full Title', blurb: 'One line for the home card',
  short: 'Sidebar Label', file: 'topics/56-slug.html', time: 12,
  prereqs: ['linalg'], badge: 'new' },
```

That's it. The sidebar, home grid, learning-path map, search index, prev/next order,
progress total and breadcrumbs are all derived from that array. **Nothing else needs
editing** — the previous version required the same topic to be declared in four separate
places (sidebar markup, `TOPIC_FILES`, `TOPIC_META`, `TOPIC_NAMES`) plus twice more in the
home page, and one topic had already fallen out of sync and become unreachable.

---

## Architecture

```
index.html                 shell only: sidebar frame, topbar, palette, icon sprite
assets/style.css           the whole design system (tokens at the top)
assets/prism-theme.css     syntax colours, all driven by the same tokens
assets/js/
  topics.js                SOURCE OF TRUTH: groups, topics, metadata
  app.js                   router, generated nav, search, progress, TOC, pager
  lazy.js                  on-demand loaders for the heavy third-party deps
assets/codemirror-init.js  editor for the interactive runners (lazy)
topics/00-home.html        hero + curated study path + mount points
topics/NN-*.html           one fragment per topic
```

### Loading

Topics are fetched on demand and cached; the next topic is prefetched while you read the
current one, and hovering a sidebar item warms it too.

**Everything heavy is lazy.** The previous version loaded KaTeX, four Prism scripts,
CodeMirror *and Pyodide* on every single page view — Pyodide being a multi-megabyte WASM
runtime that then installed numpy and scikit-learn through micropip. Now:

| Dependency | Loaded when |
|---|---|
| KaTeX | a topic that actually contains `$…$` math is opened |
| Prism | a topic containing `language-*` code is opened |
| CodeMirror | a topic containing `.code-runner` is opened |
| Pyodide | you press **Run** — never before |

Python packages are loaded on demand too, from the runner's `data-packages` attribute
(default `numpy`). Every run used to install **scikit-learn via micropip** — by far the
slowest step — even though no runner imported it.

`assets/js/lazy.js` caches each loader in a promise, so nothing loads twice.

### Search

Full-text across every topic. The index is built by fetching all fragments in parallel,
triggered either by opening the palette or by `requestIdleCallback` after first paint —
whichever comes first. Previously the index only held topics you had already opened, so
search on a fresh visit returned nothing.

### Keyboard

| Key | Action |
|---|---|
| `⌘K` / `Ctrl+K` / `/` | open search palette |
| `↑` `↓` `↵` | move / open within the palette |
| `j` / `→` | next topic |
| `k` / `←` | previous topic |
| `m` | mark current topic read |
| `h` | home |
| `Esc` | close palette |

---

## Design system

Tokens are defined twice at the top of `style.css` — `:root, [data-theme="dark"]` and
`[data-theme="light"]`. **Change a colour there, never in a rule.** The theme is resolved
by an inline script in `<head>` before first paint, so there's no flash of the wrong
palette.

The palette matches [yaksh-patel.github.io](https://yaksh-patel.github.io): cool ink
neutrals, a signal-teal accent, Space Grotesk for display, IBM Plex Sans for body,
JetBrains Mono for metadata only.

### Component classes for topic content

| Class | Use |
|---|---|
| `.card` + `.cb .cg .ca .cr .cp .cc` | content card, optional coloured left edge |
| `.card-title` `.card-body` | inside a card |
| `.box` + `.story .ideal .mem .warn .info .tip` | callout; label goes in `.bl` |
| `.g2` `.g3` | two / three column grids (collapse on mobile) |
| `.bul` `.num` | styled `ul` / `ol` |
| `.tbl` | table (scrolls horizontally on small screens) |
| `.formula` `.math-formula` `.formula-block` | maths and pseudo-code blocks |
| `.tag` + `.tb .tg .ta .tr .tp .tc` | inline pills |
| `.cgrid` `.ch` `.cg-cc` `.ctp .ctn .cfp .cfn` | confusion-matrix grid |
| `.anim-wrap` `.anim-title` | wrapper for an inline SVG diagram |
| `.code-runner` | interactive Python block; `data-packages="numpy,pandas"` declares what Pyodide must load |

Every topic carries a diagram and a worked code example. The diagrams share one
visual language (L-shaped axes, mono micro-labels, the same six semantic hues),
so they read as one guide rather than 55 unrelated illustrations. Draw new ones
with the legacy palette hexes — section 8 of `style.css` maps those onto the
live tokens, so a diagram follows both themes for free.

### A note on diagram colours

The inline SVGs across the topic files carry hardcoded hexes from the original dark
palette. Section 8 of `style.css` maps those 15 values onto the current design tokens, so
the diagrams now follow **both** themes — previously they were dark-only with a light-mode
patch. New diagrams can keep using the same hexes and they will be remapped too.

---

## Running locally

Any static server works; the topic fetches need HTTP, not `file://`.

```bash
python3 -m http.server 8000     # then open http://localhost:8000
```

## Maintaining the content

The 55 topics were rewritten over 20 batches; the working notes lived in
`REVAMP-PLAN.md`, now deleted. What follows is the part worth keeping — the
invariants, the tooling, and the traps that cost real time to find.

### Invariants

- Root element stays `<section class="section" id="sec-<id>">`, one per file, and the
  id must match `topics.js` — the router looks the section up by it.
- `div`/`section` balanced and `$$` paired. `tools/check_topics.py` verifies both with
  a real HTML parser, not a line count.
- No page-level `<style>` blocks in topic files. `assets/style.css` owns styling.
- Diagram colours use the legacy palette hexes (`#5ba4fb`, `#22d3a0`, `#f5a623`,
  `#f06767`, `#b97cf8`, `#4e5a7a`, `#1a1f2e`, `#2e3a58`…), which section 8 of
  `style.css` remaps onto the live tokens. `tools/svgkit.py` draws in that vocabulary.
- Topic metadata lives **only** in `assets/js/topics.js`.
- `{{` and `{%` are fine now that `.nojekyll` exists, but keep them inside
  `<pre>`/`<textarea>` — there is a dbt snippet in `50-data-engineering`.

### CI

`.github/workflows/validate.yml` runs every check below on push and on pull request.
**Each tool exits non-zero on failure**, and that was verified the only way it can be —
by deliberately introducing each class of break and confirming the build goes red:
an unclosed `<div>`, a malformed `.bl` label, a deleted diagram, a `→` inside
`\text{}`, a bad inline formula, and a renamed section id. Before this existed all six
of those passed silently, because four of the tools printed their findings and still
exited 0.

If you add a tool, give it an exit code and prove it fails. A green check that cannot
go red is worse than no check.

### Tools

| Path | Does |
|---|---|
| `tools/check_topics.py` | structural validation. `--all` or named topics |
| `tools/assets.py` | asset accounting vs a baseline commit; `blocks()`, `codecard()` |
| `tools/check_css_hooks.py` | every class the JS adds must be matched by a CSS rule — catches dead class hooks, which no smoke test can see |
| `tools/audit_markup.py` | full tag balance, `.bl` labels, depth-matched boxes, `$` in prose |
| `tools/kxstrict.mjs` | renders every `$$` block under KaTeX `strict:'error'` |
| `tools/kxinline.mjs` | same for inline `$…$`, per text node — the display check misses these |
| `tools/svgkit.py` | shared SVG vocabulary for diagrams |
| `tools/run_runners.py` | executes the code inside every `.code-runner` and fails if any errors |
| `tools/smoke.mjs` | jsdom smoke test: boots the app, renders home, navigates, then asserts 13 invariants — sidebar/home/map counts against the manifest, the app globals, pager and TOC, and that **every** topic in `topics.js` resolves to a file with a matching `id="sec-<id>"` |

The `.mjs` tools need jsdom and katex, which are not vendored:

```bash
mkdir -p /tmp/domtest && cd /tmp/domtest && npm init -y >/dev/null && npm i jsdom katex --silent
cp <repo>/tools/{smoke,kxstrict,kxinline}.mjs .
node smoke.mjs <repo>      # expect: 13/13 checks passed
node kxstrict.mjs <repo>   # 152 display formulas: 0 failures, 0 strict warnings
node kxinline.mjs <repo>   # 174 inline formulas: 0 failures, 0 strict warnings
```

Install those deps **outside** the repo, as above. A `package.json` at the repo root
breaks module resolution for `tools/*.mjs`; `.gitignore` covers it, but the simplest
fix is not to create one there.

Also **run the code cards**. Every worked number in the prose should be one a reader
can reproduce, so extract a topic's `language-python` block and execute it in a
throwaway venv. This repeatedly caught numbers that no validator would see — a
printed vector computed a different way from the prose, a sample-size table using a
different formula than its own code card.

### Interactive runners

21 topics carry a live editor rather than a static block: every example whose imports stay
within numpy and the standard library. Adding more is a `data-packages` change — Pyodide
ships scipy, pandas and scikit-learn as native wheels, so `data-packages="pandas"` on the
runner is all a pandas example needs.

`tools/run_runners.py` executes all of them in CI. That check exists because a runner
promises "press Run and it works" and nothing else in the toolchain ever opens one — which
is how `01-linear-algebra` shipped an assertion that had never been executed, comparing a
covariance spectrum against the SVD of **uncentred** data. It runs under CPython + numpy
rather than Pyodide, so it is a tight proxy, not a guarantee; keep runners to numpy and the
stdlib and it stays tight.

### Traps that cost real time

- **A class hook with no CSS rule fails silently.** `codemirror-init.js` set
  `cm-active-runner` to hide the raw `<textarea>` once the editor mounted, and no rule ever
  matched it — so every runnable block showed its code twice, both copies editable, and only
  the CodeMirror copy was the one `runCode()` read. jsdom applies no stylesheets, so no smoke
  test could see it. `tools/check_css_hooks.py` now covers it. Note the textarea must stay
  visible when CodeMirror does *not* mount, because `runCode()` falls back to reading it.

- **Asset retention.** Rewrite prose *around* diagrams, code cards and tables; never
  retype them. Use `blocks()` from `tools/assets.py`, never a hand-rolled regex —
  wrappers carry `style` attributes (`06-bias-variance`), a widget's `<script>` can sit
  *outside* its wrapper div (`09-confusion-roc`), and `code-runner\b` also matches
  `code-runner-header`, which silently duplicated a header. Then check with
  `python3 tools/assets.py cdf20c9 <topics…>` — **any count going down is a lost asset,
  not a simplification.** Do not "fix" `counts()`: it deliberately counts raw string
  occurrences, so `runner=2` for a single widget is correct.
- **`check_topics.py` only tracks `div` and `section`.** A stray `</tt>`, an unclosed
  `<th>`, a malformed `.bl` label — none of it is caught, because the parser watches
  only the two tags the router depends on. Run `tools/audit_markup.py` alongside it,
  never instead of it. Note a `.bl` label that swallows its closing tag still leaves
  the divs *balanced*, so `check_topics.py` reports ok.
- **Unsupported Unicode inside `\text{}`.** KaTeX's text mode rejects `×`, `→`, `←`,
  `÷`, `≤`, `≥` and friends. Close the text group and emit `\times` / `\rightarrow` in
  maths mode. Em and en dashes are fine. Check with `strict:'error'`, not the default,
  which only warns.
- **Dollar amounts in prose rendering as maths.** KaTeX matches `$…$` within a *single
  text node*, so two `$` in one sentence render as inline maths. Wrap each amount in its
  own element so each `$` sits in its own text node. Scan with an HTMLParser pass over
  text nodes — a line-based grep both misses these and false-positives on multi-line
  `$$` blocks.
- **Maths rendered as raw LaTeX.** `looksLikeMath` in `lazy.js` used to require both `$`
  on one line; display maths spans newlines. Fixed — don't reintroduce it.
- **Content overlapping the "on this page" rail.** Grid/flex children default to
  `min-width: auto`, so a wide KaTeX block pushes its column past the container. Fixed
  with `min-width: 0` on card/grid containers plus `overflow-x: auto` on `.katex-display`.

### Deploying

- **Push once per batch.** GitHub Pages cancels an in-progress build when a new one
  starts; three rapid pushes once cancelled each other and a whole commit never
  deployed. It looked like CDN lag, but the build had been cancelled.
- **`.nojekyll` is required and present.** This is a plain static site; the default
  Jekyll build was pure overhead and slow enough for pushes to collide.
- **Fragments are CDN-cached for 600s.** A topic can serve old content for ten minutes
  after a successful deploy. To verify content immediately check
  `raw.githubusercontent.com`, not the Pages URL.
- Check a build with
  `curl -s "https://api.github.com/repos/Yaksh-Patel/ml-guide/actions/runs?per_page=3"`
  and parse with `json.load(f, strict=False)` — the payload contains control characters
  that strict JSON rejects.

---

## Progress storage

Read state lives in `localStorage` under `ml-guide-progress-v2` — per browser, never sent
anywhere. The key is unchanged from the previous version, so existing progress carries
over. "Reset" on the home page clears it.
