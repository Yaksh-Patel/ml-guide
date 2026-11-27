# Visual revamp status

Read this first, then only the current chunk in `PLAN.md`. Update this file last.

**Current chunk:** 3, sidebar and icons (model: **Sonnet**). **Blocked on Yaksh's review of chunk 2** (PLAN says he reviews before chunk 3).
**Branch:** `visual-revamp`, pushed. Chunks 0, 1 and 2 are committed.
**Blocker:** review of chunk 2.
**CI not yet seen running:** `validate.yml` only runs on pushes to `main`, on PRs, and on manual
dispatch, and `gh` here is the work account (403 on this repo). Opening a PR from `visual-revamp`
(on github.com) runs it, including the layout check that has never run on a runner.

## Handoff to chunk 3
- Tools live in `/tmp/domtest` (layout check, smoke, kxstrict, kxinline, plus two one-offs not in the
  repo: `dd_test.mjs` and `elshots.mjs`, which screenshots single elements:
  `node elshots.mjs <repo> <out> <width> <theme> 'dtree|> .card > .tbl|1' ...`). After editing any
  `tools/*.mjs`, copy it over again. `/tmp` clears on reboot: reinstall with
  `npm i jsdom katex puppeteer-core@24.10.0`.
- `run_runners.py` fails locally only because this Mac's python3 has **no numpy** (see chunk 1 note).
- `--grp` / `--grp-bg` / `--grp-bd` exist on `.main` (style.css §1), set from `data-group`. Use them
  for the sidebar's current-group accent and per-group progress bars rather than adding a new map.
  The home map's `.tn-*` classes still hold their own copy of the same pairing (§7); chunk 4 can fold them in.
- The crumb in the top bar now has a group-coloured dot **and** still the emoji (`paintTopbar`
  builds it from `groupIcon`). Chunk 3 replaces the emoji there too.
- Callout labels no longer carry emoji (CSS draws the icon). Emoji are still in: `topics.js` group
  icons, the sidebar, the palette meta line, the crumb, and runner headers (`🐍 Python · numpy`, in
  21 topic files). The runner one is content: leave it for chunk 7 or strip it with the same kind of
  one-line regex used for `.bl` labels.
- Baselines: `main` screenshots in `/tmp/domtest/baseline-shots/`, chunk 1 in `c1-shots/`, chunk 2 in `c2-shots/`.

## Log

### 2026-11-27: chunk 2 done (Opus)
- **Open sections (D2):** a top-level `.card` has no box. It spans the article column, and its children
  follow the column rules (text at `--prose-w`, `.anim-wrap .g2 .g3 .code-runner` wide). This replaced
  the container-query breakout planned in chunk 1's handoff: one level of selectors does the same job.
  Numbered heading via a CSS counter in `--grp`, hairline above each section, 56px rhythm. Inside a
  section, one vertical rhythm (`!important`, because ~700 blocks carry inline `margin-top: 8-10px`).
  Nested cards in `.g2/.g3` keep a light box, and their colour class is now a 2px **top** edge.
- **Group colour (D3):** `paintTopbar()` sets `data-group` on `.main`, and §1 maps it to `--grp/-bg/-bd`. It drives
  section numbers, the active rail/dropdown entry, the progress bar, a crumb dot, figure captions,
  pull-quote rules, `ol` markers and the Run button. The 60 "Part N" headings (11 older topics, inline
  colours) are forced to a `--grp` mono kicker with a rule above until chunk 7 rewrites them.
- **Type (D4):** body 16/1.72 in `--text`, lead paragraph 17px, title 36px from 1440px. Table headers in sans 12.5px.
  Inline code is `--text` on `--bg3` with no border.
- **Components (D5):** display maths unboxed and centred. Pseudo-code `.formula` blocks get a quiet `--bg3` panel. Callouts
  have a 3px semantic rule, a 6% tint and a CSS-mask line icon. `.box.mem` is an upright 17px pull-quote. Tables have no box,
  are `fit-content` with the text column as the minimum, and are never wider than the article. Diagrams are `--surface`
  figures with the caption below (flex `order`) and the SVG capped at 460px tall. The runner header is sans, with a filled Run button.
- **prism-theme.css trimmed** to token colours + `<pre>`. It is lazy-loaded *after* style.css and was
  overriding runner, inline-code, `.formula-block` and KaTeX styles (with an undefined `--r-lg`), so
  pages looked different depending on whether they had static code. style.css owns those now.
- **Topic files:** only the leading emoji was stripped from 67 `.bl` labels (e.g. "🎯 In an interview"),
  because the CSS icon replaced it. The diff was checked: every changed line is a `.bl`. `assets.py` shows no count going down.
- Topic-column rules are scoped to `.section:not(#sec-home)`, because home has a top-level how-to card. Chunk 4 owns home.
- `layout_check` A3 now also measures `.card-body` and `.sec-desc`: topics write most prose as
  `div.card-body`, so A3 was barely checking anything.
- README: component table rows for `.card`, `.box`, `.anim-wrap`, plus the prism-theme line.
- **Checks:** layout_check passes all 96 cases. Smoke 23/23. kxstrict and kxinline 0 failures. check_topics, audit_markup
  and check_css_hooks clean. Runners not re-run (no numpy locally; runner JS untouched).
- Before/after pairs at 1440 for dtree, biasvar, confusion and attention, both themes:
  `/tmp/domtest/c2-pairs/` (main left, chunk 2 right).
- **For Yaksh's review:** wide figures at 1728+ are big (biasvar explorer's legend labels about 16px). The
  460px height cap limits it, but a figure-width token (about 920px) is the next lever if it feels loud.

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
