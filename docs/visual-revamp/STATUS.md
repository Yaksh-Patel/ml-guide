# Visual revamp status

Read this first, then only the current chunk in `PLAN.md`. Update this file last.

**Current chunk:** 1, layout shell (model: **Opus**)
**Branch:** `visual-revamp` (local only; chunk 0 work is not yet committed or pushed)
**Blocker:** none. Local server allowed in `.claude/settings.local.json` (gitignored).

## Handoff to chunk 1
- Tool: `tools/layout_check.mjs`. Run it from `/tmp/domtest` (deps already installed there:
  jsdom, katex, puppeteer-core@24.10.0). It serves the repo itself, so no http.server is needed for it.
  Copy the tool over after any edit: `cp tools/layout_check.mjs /tmp/domtest/`.
- CI runs it with `--expect-fail A3,A4`. **When chunk 1 lands, A3 and A4 must pass, so remove
  `--expect-fail A3,A4` from `.github/workflows/validate.yml`** (otherwise XPASS fails the build).
- Contracts the tool already checks, which chunk 1 must implement exactly:
  - Prose: any `p`/`li` outside wide blocks is ≤ **720px** (`PROSE_W`).
  - Wide blocks (`.anim-wrap .g2 .g3 .code-runner .cgrid`) are ≤ the `#topic-container` width.
  - Rail `#toc` visible at **≥1280px**, hidden below (`TOC_MIN_W`).
  - Below 1280px, a visible element with class **`.toc-dropdown`** must exist.
  - Rail clearance ≥ **24px** from any content (overlap guard; the 56px design gap is checked by eye).
  If a D1 number changes, change the constant at the top of `layout_check.mjs` in the same commit.
- Baseline screenshots (180, from `main` at 499b801): `/tmp/domtest/baseline-shots/`
  named `<page>-<width>-<theme>-<top|mid>.png`. `/tmp` clears on reboot; to regenerate, make a
  worktree of `main` and run the tool with `--shots`.

## Log

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
