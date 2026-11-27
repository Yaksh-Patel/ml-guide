# ML Atlas: figure revamp plan

> **Session rule:** read `STATUS.md` first, then **only the chunk it names**. Update `STATUS.md`
> last. Yaksh may ask for several chunks in one session: commit each, verify each, stop at
> anything that needs his eyes.

Written 2026-11-27 after screenshotting all 63 figures (`.anim-wrap`) at 1440 in both themes.

## 1. What was wrong

| # | Problem | Cause | Status |
|---|---|---|---|
| G1 | Text size jumped between figures (1.1x–1.9x) and some figures had ~20px labels | SVGs stretched to the 1080 column | **fixed (F0)**: `normaliseFigures()` caps at 1.45 px/unit |
| G2 | Arrowheads vanished after visiting a few topics | 37 topics name their marker `ah`; `url(#ah)` resolves to the first one, inside a hidden topic | **fixed (F0)**: per-figure def ids |
| G3 | Labels overrun boxes and each other | laid out for DM Sans (never loaded), rendered in the wider IBM Plex Sans | **eased (F0)**: IBM Plex Sans Condensed for SVG text |
| G4 | Labels collide with axes, curves and captions; text cut at the edges | hand-placed coordinates | redraw (F2–F5) |
| G5 | Three figures taught the wrong thing | 06-0 total error drawn as ∩, sweet spot at the peak; 29-1 gradient descent climbing a hill; 53-0 O(·) labels not matching curves | **fixed (F1)** |
| G6 | Emoji in figures (🔵🔴 ⚡ 🟡) | old content | F5 |
| G7 | Interactives: dead space, legends over curves, clipped nodes | layout | F6 |
| G8 | Phones: a 500–640 unit figure in a 330px column has 5–6px labels | width | F7 (tap to expand) |

Tried and rejected: a minimum width with sideways scroll on phones. A chart whose point is its
shape showed only its left half on first view, which is worse than small text.

## 2. Spec for redrawn figures (settled)

- Built with `tools/figkit.py`, one module per figure in `tools/figures/fNN_i.py`, swapped in by
  `python3 tools/figures/build.py`. Only the `<svg>` changes; wrapper and caption stay.
- Canvas **560** wide (640 only if needed). Heights to fit, ≤ 320.
- Text: LABEL 10, SMALL 9, TINY 8.5 units. Weight 600 for labels that name a series.
- **Direct labels** against their curve/box, never on top of a line; no legend boxes.
- Axis titles: y title horizontal above the axis, x title at the end or centred below.
- At most one takeaway sentence inside the SVG. Long explanations belong in the prose.
- Colours: the legacy hexes in figkit (style.css §8 maps them). Semantic use: red = error / bad /
  bias, green = correct / total / good, blue = primary series, amber = the thing to look at
  (threshold, optimum, current point), purple = secondary series.
- Correctness first: if a figure's maths or shape is wrong, fix it and say so in the module
  docstring.
- Every figure: `figkit` check passes, `tools/figure_lint.mjs` shows 0 clip / 0 overlap, and
  a screenshot in both themes is looked at.

## 3. Audit (63 figures; index = order of `.anim-wrap` in the topic file)

- **A, wrong content:** 06-0, 29-1, 53-0. Done in F1.
- **B, redraw (collisions, clipping, scale):** 01-0, 03-0, 08-0, 10-0, 11-0, 13-0, 14-0, 15-0,
  20-0, 21-0, 22-0, 23-0, 25-0, 27-0, 28-0, 29-0, 31-0, 34-0, 35-0, 36-0, 41-0, 42-0, 43-0,
  45-0, 47-0, 52-0.
- **C, polish (emoji, sparse, small):** 04-0, 26-0, 32-0, 33-0, 36-1, 39-0, 40-0, 51-0.
- **Interactive:** 06-1, 09-0, 29-2, 34-1, 34-2, 48-0.
- **Fine as they are:** 02, 05, 07, 12, 16, 17, 18, 19, 24, 30, 37, 38, 44, 46, 49, 50,
  51-1, 54, 55 (check again after F0; re-lint).

## 4. Chunks

| # | Chunk | Model |
|---|---|---|
| F0 | Systemic: scale cap, own def ids, condensed face; `figure_lint.mjs`, `figkit.py`, `build.py` | Opus, **done** |
| F1 | Redraw the three wrong figures as the style sample | Opus, **done** |
| F2 | Redraw B: 01, 03, 08, 10, 11, 13, 14, 15 | Opus |
| F3 | Redraw B: 20, 21, 22, 23, 25, 27, 28, 29-0 | Opus |
| F4 | Redraw B: 31, 34-0, 35, 36-0, 41, 42, 43, 45, 47, 52 | Opus |
| F5 | Polish C, remove emoji; re-lint the "fine" list | Sonnet |
| F6 | Interactives: controls row, no dead space, labels off curves | Opus |
| F7 | Phones: tap a figure to open it full-screen (pinch-zoomable) | Sonnet |
| F8 | `figure_lint` in CI at zero; README *Diagrams*; delete this folder | Sonnet |

Per chunk: read the topic text around each figure first (the figure must say what the prose
says), redraw, `build.py --check`, lint, screenshot both themes (`/tmp/domtest/figshots.mjs`,
`sheets.py` for contact sheets), assets.py counts unchanged, commit.
