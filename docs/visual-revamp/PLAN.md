# ML Atlas: visual revamp plan

> **Session rule:** read `STATUS.md` first, then **only the chunk it names**. One chunk per
> session; update `STATUS.md` last, then `/clear`. Don't read the other chunks or re-discuss
> the decisions in §2. They are settled. Raise an objection in STATUS instead.

Written 2026-11-27, based on screenshots of the live site at 1440px, 1728px and 390px
widths in light and dark mode.

---

## 1. What's wrong today

The design underneath is good: fonts, teal accent, both themes, and the "on this page"
list. The problem is **density and sameness**: too many borders, too many boxes nested
inside each other, colour used with no meaning, and wide screens left mostly empty.

| # | Problem | Where | Evidence |
|---|---|---|---|
| P1 | **Boxes inside boxes.** Every section is a bordered card; formulas, callouts and tables inside it are boxes too, often three levels deep | all topics | 2,131 `.card`, 388 formula boxes, 171 `.box` |
| P2 | **Card edge colours mean nothing.** The six colours are spread almost evenly (`ca` 99, `cr` 88, `cb` 87, `cg` 82, `cc` 78, `cp` 64), so a long page reads blue, green, purple, red, amber, red | all topics | `.card.cb…cc` in style.css §5 |
| P3 | **Wide screens leave the right side empty.** Article is capped at 800px plus a 206px list, pinned to the left. On a 1728px screen about 340px sits empty; on 2560px about 1,100px | all topics | `.content-shell` / `#topic-container` |
| P4 | **Text is small and grey.** Body text is 14px in `--text2` grey, which is tiring over a 15–20 minute topic | all topics | `.card-body` |
| P5 | **Too many tiny monospace capital-letter labels**: breadcrumbs, table headers, box labels, home card subtitles | everywhere | 9–10px mono, uppercase |
| P6 | **Diagrams don't stand out.** They sit in the same grey box as formulas, though they're the best part of each page | 55 topics, 63 diagrams | `.anim-wrap` |
| P7 | **"On this page" list disappears below 1180px**, with nothing replacing it | laptops, tablets | `@media (max-width:1180px)` |
| P8 | **Home page is a flat wall** of 55 identical white cards; the hero is text only | home | `00-home.html` |
| P9 | **The learning-path map is the best idea on the home page, but the hardest to see** (26×22px faded squares) | home | `.tmap-node` |
| P10 | **Emoji group icons** (🔢🧭🌳🧠🚀) clash with the restrained type and accent | sidebar, home | `topics.js` `icon:` |
| P11 | **Older topics are written differently**: blue "Part 1 — …" headings, Title Case card headings | 11 topics, listed in chunk 7 | content |
| P12 | **Possible sideways scrolling on phones**: text cut off in a 390px screenshot. Not yet confirmed; headless Chrome can crop narrow windows | mobile | must measure |
| P13 | **No motion.** Pages swap with a 0.2s fade, nothing else | everywhere | Yaksh prefers expressive, animated UI |

---

## 2. Design decisions (settled)

### D1. Page layout on wide screens: three zones, list at the far right
```
| sidebar |   ← centred article column →   | gap | ON THIS PAGE |
|  272px  |  text 720px, wide items ≤1080px  | 56px|    224px     |
```
- `.content-shell` becomes a **two-column CSS grid**: `minmax(0,1fr) var(--toc-w)`.
  The "on this page" list gets **its own column pinned to the far right edge**, so it
  **cannot overlap content by construction**. Nothing in column 1 can reach column 2.
- Inside column 1 the article is centred. Plain text is capped at `--prose-w: 720px`
  (about 75 characters per line).
- **Wide items break out** up to `--wide-w: 1080px` (never past 100% of column 1):
  diagrams, tables, side-by-side grids (`.g2`, `.g3`), code editors, the confusion grid.
- The list column is shown from **≥1280px** (was 1180px, because 1180–1280 left the text too narrow).
  Below that, it turns into a **"On this page ▾" dropdown in the top bar** (fixes P7).
- With the sidebar collapsed, the same grid simply gets wider. No special case.
- Tokens: `--prose-w: 720px; --wide-w: 1080px; --toc-w: 224px; --toc-gap: 56px`.

### D2. Open sections instead of card-per-section
- **Top-level cards** (direct children of `.section`) lose their background, border
  and coloured edge. Each becomes an open section: a 22px heading with a small group-coloured
  section number (CSS counter, no content edits), 56px vertical spacing between sections,
  and a hairline rule between them.
- **Nested cards** (inside `.g2` / `.g3`) stay as light cards. Their authored colour becomes
  a thin **top** edge, kept because in pairs like "High bias / High variance" it means
  something.
- Done **entirely in CSS** using the existing structure. **Topic files are not edited** for this.

### D3. One colour per topic, taken from its group
- `app.js` sets `data-group="<id>"` on `.main`; CSS maps it to `--grp` / `--grp-bg`.
- Group to hue mapping (same as the current map): math + mlthink = blue,
  classical + dataeng = green, nn + dl = purple, nlp + llmera = teal (accent),
  domains = amber, prod = cyan, ref = neutral.
- `--grp` drives: section numbers, the active "on this page" marker, the reading-progress bar,
  the breadcrumb dot, figure captions.
- **Callout colours stay as they are** (`warn` red, `ideal` green, `info` blue, `tip` purple,
  `story` amber), because they are semantic.

### D4. Typography for reading
- Prose: **16px / 1.72**, colour `--text` for body (not `--text2`). `--text2` only for
  secondary text. Paragraph spacing 0.9em.
- Section headings: display font, 22px. Topic title stays at 28px with 36px on ≥1440px.
- **Monospace capital-letter labels only where they help**: sidebar group labels, top-bar breadcrumb, `.bl`
  callout labels. Table headers become 12.5px sans, semibold, normal case. Home card subtitles
  become sans.
- Inline `code`: `--text` colour on `--bg3` instead of accent-coloured, so it's quieter in dense paragraphs.

### D5. Lighter components
- **Display maths:** remove the box. Centred, with 18px top and bottom spacing.
  Code-style `.formula` blocks (pseudo-code) keep a subtle background with no border.
- **Callouts (`.box`):** a 3px left rule in the semantic colour, a very faint background, and a label with
  a small inline icon. `.box.mem` becomes a **pull-quote**: 17px, `--grp` left rule, no box.
- **Tables:** no outer box, hairline row separators, header in sans. Cell alignment stays
  as authored.
- **Diagrams become figures:** wide breakout, `--surface` panel with 12px radius, generous
  padding, and `.anim-title` restyled as a caption *below* (CSS `order`/flex, no markup change).
- **Code editors:** wide breakout, one consistent header bar (language · packages · Run).

### D6. Icons replace emoji
- 11 line icons (Lucide-style, 1.5px stroke) added to the **existing SVG sprite in
  `index.html`**. No new dependency. `topics.js` `icon:` becomes an icon id.
- Used in the sidebar group headers, home group headers and map stations.

### D7. Motion (all disabled under `prefers-reduced-motion`)
- Sections fade and rise as they enter the viewport (IntersectionObserver, runs once, 12px / 300ms).
- Crossfade between topics; "on this page" active marker slides between entries.
- Home: hero animation, staggered card entry, progress number counts up, map nodes
  fill when read.
- Hover: cards lift 2px with a soft shadow. Nothing that moves layout.

### D8. Home page
- **Hero, two columns on wide screens:** text left, an **animated SVG on the right**: a
  small neural network whose edges pulse, or a decision boundary drawing itself through scattered
  points. Pick one in chunk 4; plain SVG and CSS, no library.
- **"Continue reading" strip** merges the progress widget and the how-to card: last-opened
  topic, overall percentage ring, keyboard hint as a single line. Needs a `last-topic` localStorage key.
- **Learning-path map as the centrepiece:** a subway-style SVG, one line per group, one
  station per topic, filled when read, title on hover, click to open. It **replaces** the
  "recommended study order" pills, which say the same thing less well.
- **Topic grid:** each group gets a header with icon, colour band and "3 / 6 read" progress.
  Cards get a group-coloured top edge, a read-state check, and the blurb in sans.

### D9. Optional, last: margin notes on very wide screens
On ≥1680px, short callouts (`.box.mem`, `.box.tip`, "worked" examples) move into the
right margin of column 1 as side notes. Only after D1–D8 are stable, because it is the most
fragile layout change.

---

## 3. Verification (applies to every chunk)

Existing checks (README → *Tools*) keep running: `check_topics.py --all`, `audit_markup.py`,
**`check_css_hooks.py`** (every new class the JS adds needs a CSS rule), `smoke.mjs`,
`kxstrict.mjs`, `kxinline.mjs`, `run_runners.py`.

**New in chunk 0:** `tools/layout_check.mjs`, built with puppeteer-core against the installed
Chrome and set up outside the repo like the other `.mjs` tools. For a fixed set of pages
(home, linalg, biasvar, confusion, dtree, attention, rag, mlops) at widths
**390 · 768 · 1280 · 1440 · 1728 · 2560**, in both themes, it asserts:
1. no sideways scrolling: `document.documentElement.scrollWidth <= innerWidth`
2. **"on this page" list never intersects content**: its left edge ≥ the right edge of every
   element inside `#topic-container`, plus the gap
3. text column width ≤ `--prose-w` + 1px; wide items ≤ the column width
4. the list is visible ≥1280 and hidden below (with the dropdown present)

It also writes screenshots to the scratchpad for before/after comparison, and
**exits non-zero on any failure**. Prove it fails once by breaking the layout on purpose
(README rule: a check that can't fail is worse than none).

**Preview:** needs a local static server (`python3 -m http.server 8000`). Allow it once in
the project's Claude settings, or it gets blocked. Push **once per chunk** (Pages cancels
overlapping builds).

---

## 4. Chunks

| # | Chunk | Model | Fixes |
|---|---|---|---|
| 0 | Setup: branch, baseline screenshots, `layout_check.mjs` | Sonnet | P12 (measure) |
| 1 | Layout shell: grid, list at far right, wide breakout, top-bar dropdown | **Opus** | P3, P7, P12 |
| 2 | Declutter: open sections, typography, lighter components, group colour | **Opus** | P1, P2, P4, P5, P6 |
| 3 | Sidebar and icons | Sonnet | P10 |
| 4 | Home page | **Opus** | P8, P9 |
| 5 | Motion | Sonnet | P13 |
| 6 | Mobile and tablet pass, dark-mode audit | Sonnet | P12 |
| 7 | Content consistency for the 11 older topics | Sonnet | P11 |
| 8 | *(optional)* margin notes | Opus | D9 |
| 9 | Merge, deploy, update README, delete this folder | Sonnet | – |

Risk-first ordering: chunk 1 changes the frame every page sits in, so it goes first and has the
strictest checks. Chunk 2 is the biggest visual win and depends on chunk 1's widths.

### Chunk 0: setup and baseline
- **Goal:** a way to measure, before anything changes.
- Steps:
  1. `git switch -c visual-revamp` from `main`.
  2. Allow `python3 -m http.server` for this project (Yaksh approves once).
  3. Write `tools/layout_check.mjs` as specified in §3. Install puppeteer-core in `/tmp/domtest`,
     not in the repo.
  4. Run it against current `main`. Save screenshots to the scratchpad as the **baseline**.
     Record which assertions fail today in STATUS. Expect #3 (no prose cap) and possibly #1 at 390px.
  5. Add `layout_check.mjs` to `.github/workflows/validate.yml` (ubuntu runners have Chrome).
     Mark the not-yet-met assertions as expected-fail until chunk 1 so CI stays honest.
- **Done when:** the check runs locally and in CI, the baseline is captured, and P12 is
  confirmed or ruled out.

### Chunk 1: layout shell
- **Goal:** D1 exactly.
- Files: `style.css` §3 and §9, `app.js` (top-bar dropdown, built from the same headings as
  the list), `index.html` (dropdown container).
- Steps: add tokens → convert `.content-shell` to a grid → centre `#topic-container`, cap
  prose → breakout rule for `.anim-wrap, .tbl, .g2, .g3, .code-runner, .cgrid` → move the
  list breakpoint to 1280 → top-bar "On this page ▾" below 1280 → fix any overflow found in chunk 0.
- Watch: the README trap on `min-width: 0` for grid children; KaTeX display blocks must still
  scroll inside their column; the sticky list's `max-height` still works in its own column.
- **Done when:** `layout_check.mjs` passes **all** assertions at all widths, smoke and markup
  checks stay green, screenshots at 1440 and 1728 show the list at the far right with balanced gutters.

### Chunk 2: declutter topic pages
- **Goal:** D2–D5. Pages read as an article with figures, not a stack of boxes.
- Files: `style.css` §5 and §6, `prism-theme.css` (inline code colour), `app.js` (one line:
  set `data-group` on `.main`).
- Steps: group colour tokens → top-level card to open section (selector `.section > .card`,
  confirm first with a count that top-level cards are direct children) → nested card top edges →
  typography → maths without boxes → callouts and pull-quote → tables → diagrams as figures →
  code-editor header.
- Watch: `check_css_hooks.py` for new hooks; dark mode for every changed component;
  `09-confusion-roc` grid; the 21 code editors still work (the README's `cm-active-runner` trap).
- **Done when:** checks green; before/after screenshots of dtree, biasvar, confusion and attention in both
  themes show no nested borders at the top level and a single colour per page. Yaksh reviews before chunk 3.

### Chunk 3: sidebar and icons
- **Goal:** D6, plus a calmer sidebar.
- Steps: draw 11 icons into the sprite → `topics.js` `icon:` to ids → render in the sidebar →
  collapse every group except the current one by default (keep the user's manual toggles) →
  tooltips and `aria-label` on the three unlabelled buttons beside search → a small progress bar
  per group in place of the "0/6" text, or alongside it.
- **Done when:** no emoji remain in shell or home (`grep` for the old emoji in `assets/` and
  `topics/00-home.html`), smoke 13/13.

### Chunk 4: home page
- **Goal:** D8.
- Steps: hero layout and animated SVG (decide network or boundary; prototype both if
  unsure, 15 minutes max) → "Continue reading" strip with `last-topic` storage → subway map
  generated from `topics.js` (replaces the pills; keep the `#topic-map-mount` id so smoke
  checks still find it, or update smoke in the same commit) → grouped grid with headers and
  progress.
- Watch: smoke asserts home and map counts against the manifest. Keep them true.
- **Done when:** home screenshots at 390, 1440 and 1728 in both themes look intentional; smoke green.

### Chunk 5: motion
- **Goal:** D7.
- Steps: one small `motion.js` (or a section in `app.js`) with the IntersectionObserver reveal →
  topic crossfade → list marker slide → home stagger, count-up and map fill → hover lifts →
  a `prefers-reduced-motion` guard around all of it.
- Watch: reveal must not hide content if JS fails or the observer never fires (default
  visible, enhance with a class).
- **Done when:** motion works with no layout shift, and reduced-motion shows a static page.

### Chunk 6: mobile, tablet and dark mode
- **Goal:** phones and tablets as considered as desktop.
- Steps: `layout_check` at 390 and 768 → sidebar drawer, top bar (title truncation, buttons
  becoming icons), the dropdown → `.g2` stacking, tables scrolling, figures full-bleed
  → a dark-mode pass over every component changed in chunks 2–4.
- **Done when:** `layout_check` is green at all widths in both themes.

### Chunk 7: content consistency (11 topics)
- **Goal:** P11. Older topics match the house style.
- Topics with "Part N" headings: 34-attention-architecture, 36-transfer-distillation,
  39-llms-rlhf, 40-rag, 42-agentic-ai, 43-multimodal, 46-gnns, 48-causal-inference,
  49-responsible-ai, 50-data-engineering, 51-mlops.
- Steps per topic: remove or convert the "Part N" headings, change card titles to sentence case,
  and touch **nothing else**. Use `blocks()` from `tools/assets.py`, then
  `python3 tools/assets.py <baseline> <topics…>`: **any count going down is a lost asset**.
- **Done when:** all checks green, asset counts unchanged, `grep "Part [0-9]" topics/` is empty.

### Chunk 8 (optional): margin notes
- **Goal:** D9 on ≥1680px. Add `layout_check` assertion #2 for the notes too.

### Chunk 9: ship
- Merge `visual-revamp` into `main`, one push, confirm the Pages build
  (README → *Deploying*), check `raw.githubusercontent.com` for fresh files, and screenshot
  the live site.
- Update README: *Design system* (new tokens, layout zones, group colour, icons), *Component
  classes* (what changed visually), *Tools* (`layout_check.mjs`).
- Delete `docs/visual-revamp/`, as was done with the earlier `REVAMP-PLAN.md`.

---

## 5. Kick-off checklist (do this now)

1. **Allow the local server**: add `Bash(python3 -m http.server:*)` to this project's
   `.claude/settings.local.json` (or approve it when prompted in chunk 0).
2. **Open a fresh session** in `ml-guide-main/` and set the model to **Sonnet**.
3. Say: *"Read docs/visual-revamp/STATUS.md and do the current chunk."*
4. At the end of the session, check that STATUS names the next chunk and its model, then `/clear`.
5. Chunks 1, 2 and 4: switch to **Opus** before starting.
