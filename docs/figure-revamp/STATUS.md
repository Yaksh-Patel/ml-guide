# Figure revamp status

Read this first, then only the current chunk in `PLAN.md`. Update this file last.

**Where it stands (2026-11-27, end of the long session):** 45 figures redrawn and committed on
branch `figure-revamp` (not yet on `main`; live site has F0–F1b only). Yaksh approved the style
("these changes are better, go ahead with remaining figures").

**In flight when this was written**: four background agents, each writing into the working tree
(uncommitted) and leaving screenshots in `/tmp/domtest/<batch>/`:
- B1: 02, 05, 07, 12, 16; shots `/tmp/domtest/b1/`
- B2: 17, 18, 19, 24, 30; shots `/tmp/domtest/b2/`
- B3: 37, 38, 44, 46, 49; shots `/tmp/domtest/b3/`
- B5 (interactive): 09-0 explorer, 29-2 stepper, 34-1 (static), 34-2 heatmap; shots `/tmp/domtest/b5/`

## Resume here
1. `git status`: modified topics / untracked `tools/figures/f*.py` are B1–B3/B5 output. For each
   batch: look at its screenshots (tile them with PIL or `/tmp/domtest/sheets.py`), check every
   content change against the topic's own prose (agents record them as "History:" in the module
   docstring), run `python3 tools/figures/build.py --verify <modules>`, confirm the topic diff
   touches only the `<svg>` (interactives may also rewrite their wrapper HTML + script), then
   commit that batch alone. If a batch is half-done (agent stopped), finish or redo its figures.
2. Interactives: drive them in a browser (`/tmp/domtest/interact_test.mjs` is a template).
3. Full checks: check_topics, audit_markup, check_css_hooks, `assets.py 1ed04fd --all` (no count
   may go down), smoke, kxstrict, kxinline, motion_test, layout_check, figure_lint (must be 0
   everywhere; CI enforces it), `build.py --verify`.
4. Commit the README *Diagrams* section (already written in the working tree), delete
   `docs/figure-revamp/` and the CLAUDE.md "Active work" pointer, then ask Yaksh before
   fast-forwarding `main` and pushing (he reviews on the live site).
- Brief given to every batch agent: PLAN §2, plus: read the prose around the figure; fix wrong
  content and record it as History; keep/improve motion with figkit.Anim + Fig.still; verify in
  both themes at 2x; don't commit, don't edit figkit/app.js/style.css/captions.

## Open questions for Yaksh (not figure work)
- 45: the code card computes WoE as ln(good/bad); the prose and the corrected figure use
  ln(bad/good), positive = riskier. Flip the code?
- 36: a table row says "BERT-large → DistilBERT" (prose elsewhere: BERT-Base 110M); the
  "Why soft labels" example puts 0.72 on dog while saying fox is similar to cat.

## Done (committed on figure-revamp)
- F0 systemic (scale cap, per-figure def ids, condensed face); F1/F1b samples (06-0, 29-1 animated,
  53-0); kit v2 (`figkit`: label placement, text-vs-line check, halos, fixed arrowheads,
  box/connect/smooth, `Anim` + `data-still`); app.js reduced-motion freeze + off-screen pause.
- Batches A1–A5 (34 figures) and B4 (4); interactives 06-1 (rebuilt; noise was double-counted)
  and 48 (labels follow their curves); shared `.fx-*` styles; phone tap-to-expand viewer.
- ~25 figures contradicted their own prose; each fix is in its module's docstring.
- CI: figure_lint at zero + `build.py --verify` (fails when a topic's svg differs from its module).
