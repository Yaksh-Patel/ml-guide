# Visual revamp status

Read this first, then only the current chunk in `PLAN.md`. Update this file last.

**Current chunk:** 2, declutter topic pages (model: **Opus**). Yaksh reviews after it, before chunk 3.
**Branch:** `visual-revamp`, pushed. Chunks 0 and 1 are committed.
**Blocker:** none.

## Handoff to chunk 2
- Tools live in `/tmp/domtest`, which now has the layout check, smoke, kxstrict, kxinline and
  `dd_test.mjs` (a one-off dropdown test, not in the repo). After editing any `tools/*.mjs`, copy it
  over again. `/tmp` clears on reboot: reinstall with `npm i jsdom katex puppeteer-core@24.10.0`.
- `run_runners.py` fails 18 of 21 locally only because this Mac's python3 has **no numpy**. That is
  environmental: CI installs what the runners need. Locally, first run
  `python3 -m pip install $(python3 tools/run_runners.py --packages)`.
- Layout rules from chunk 1 that chunk 2 has to fit (style.css §3, "Content column + TOC rail"):
  - `#topic-container > .section > *` is capped at `--prose-w` and centred, with
    `margin-inline: auto !important` (60 "Part N" headings carry inline `margin: 28px 0 12px`).
  - Top-level `.anim-wrap .tbl .g2 .g3 .code-runner .cgrid` get `max-width: none`, so they fill
    the column (≤ `--wide-w` 1080).
  - **Not done yet, deliberately:** wide blocks *nested inside* a top-level card (189 tables,
    21 editors, 18 diagrams, 40 `.g2`) still fill the 720px card. Breaking them out of a bordered
    card looked broken. Once D2 removes the top-level card boxes, add the breakout:
    `container-type: inline-size` on `#topic-container`, then the nested wide block gets
    `width: min(var(--wide-w), 100cqw); margin-left: calc(50% - min(var(--wide-w), 100cqw) / 2)`
    (this works because the card is centred in the container). Check that no topic uses
    `position: fixed` inside a section first, since containers can trap it.
  - Interactive SVG diagrams scale with width, so at 1080px their labels get big (biasvar at 1728).
    Worth a `max-height` or a figure width cap when chunk 2 treats diagrams as figures.
- Baselines: `main` screenshots in `/tmp/domtest/baseline-shots/`, chunk 1 in `/tmp/domtest/c1-shots/`.

## Log

### 2026-11-27: chunk 1 done (Opus)
- `.content-shell` is a grid: `minmax(0,1fr)`, plus a `--toc-w` (224px) rail track at ≥1280px when
  a rail exists (`:has(> .toc:not([hidden]))`), with a 56px gap. On pages without a rail (home, or
  topics with fewer than 4 headings) the article is centred in the full width.
- Tokens added: `--prose-w 720`, `--wide-w 1080`, `--toc-w 224` (was 206), `--toc-gap 56`.
- Top-bar **"On this page ▾"** below 1280px: a `<details class="toc-dropdown">` in `.tb-right`,
  filled by `buildToc()` from the same links as the rail, with shared scroll-spy. Closes on jump,
  outside click and Escape. The panel is anchored to the sticky top bar, so it stays on screen at 390px.
- Rail/dropdown jumps now land below the sticky top bar (`scroll-margin-top: 72px` on `[id^="x-"]`).
- Phones (≤560px): the reading-time tag is hidden and Home is icon-only, so the title still shows.
  Without that, the new button pushed the 390px top bar 18px wider than the screen (A1).
- `--expect-fail A3,A4` removed from `validate.yml` and from the README command.
- **Checks:** `layout_check` passes all 96 cases (A1–A4); `dd_test` 27/27 at 390, 768 and 1180;
  smoke 23/23; kxstrict and kxinline 0 failures; check_topics, audit_markup and check_css_hooks clean.
  No topic file touched.
- Screenshots: at 1440 and 1728 the rail sits at the far right and the gutters are balanced; at 2560
  the article is centred with roughly 650px of gutter on each side.

### 2026-11-27: chunk 0 done (Opus, same session as the plan)
- Branch `visual-revamp` created. Plan files, CLAUDE.md and the .gitignore entry came along uncommitted.
- `tools/layout_check.mjs` written. 96 cases (8 pages × 6 widths × 2 themes), ~3 min.
- **Baseline on main:** A1 ok, A2 ok, **A3 fails in 42 cases** (prose 767px at 1440/1728/2560
  on all 7 topics), **A4 fails in 28 cases** (no dropdown at 390/768).
- **P12 ruled out:** no sideways scroll at 390px. The earlier cropped screenshot was headless
  Chrome's old 500px window minimum.
- Proved each assertion can fail: a temporary `body{min-width:1000px}` plus a negative right margin on
  `#topic-container` turned A1 and A2 red at 1440 and 390; A3 and A4 fail on real code; listing a
  passing assertion as expected-fail produced XPASS and exit 1. style.css restored from git each time.
- Two bugs found in the tool while proving it, both fixed:
  1. Topic switches are same-document, so scroll carried over between pages. It now scrolls to top first.
  2. Mobile emulation zooms out to fit over-wide content, inflating `innerWidth` and hiding overflow.
     It now judges against the requested device width.
- CI: `validate.yml` installs puppeteer-core and runs the check with `--expect-fail A3,A4`.
  YAML validated locally. **Not yet seen running on GitHub**: needs a push.
- README *Tools* updated with the new tool and install line.

### 2026-11-27: plan written (Opus)
- Reviewed live-site screenshots at 1440, 1728 and 390 widths in both themes.
- Yaksh's asks: less cluttered, more visually appealing; use the empty right-hand space on
  wide screens; "on this page" list at the **far right, never overlapping content**.
- Decisions D1–D9 settled in PLAN §2.
