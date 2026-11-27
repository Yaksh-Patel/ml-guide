# Figure revamp status

Read this first, then only the current chunk in `PLAN.md`. Update this file last.

**Current chunk:** F2 (model: **Opus**). **Waiting on Yaksh:** review the F1 style sample
(06 bias–variance, 29 gradient descent, 53 complexity) before the batch redraws use it.
**Branch:** `figure-revamp`.

## Handoff
- Tools: `tools/figure_lint.mjs` (copy to `/tmp/domtest` like the other .mjs tools),
  `tools/figkit.py`, `tools/figures/build.py`. One-offs in `/tmp/domtest` (not in the repo):
  `figshots.mjs <repo> <out> <width> <theme> [nums]` screenshots every figure,
  `sheets.py <dir> 8 2 640` tiles them into contact sheets (needs Pillow; run without `-I`).
- Lint after F1: 63 figures, 14 with problems, 4 clipped labels, 17 overlapping pairs. The lint
  sees text-on-text only; text over lines needs the screenshots.
- F0 decisions: FIG_SCALE 1.45; SVG text in IBM Plex Sans Condensed; per-figure def ids.

## Log

### 2026-11-27: F0 + F1 done (Opus)
- Audit of all 63 figures (PLAN §3). Content errors found in 06-0, 29-1, 53-0; 54-0's "wrong
  connectors" were the vanishing-arrowhead bug (G2).
- F0: `normaliseFigures()` in app.js (scale cap + def-id prefix), condensed face, lint and kit.
  Phone min-width + sideways scroll tried and reverted (PLAN §1).
- F1: three figures redrawn with figkit on a 560 canvas; lint 0/0; checked in both themes.
  All checks green: check_topics, audit_markup, css hooks, smoke 23/23, kxstrict/kxinline 0,
  assets.py counts unchanged.
