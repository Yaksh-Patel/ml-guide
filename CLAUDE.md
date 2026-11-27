# ML Atlas

Static site (no build step), GitHub Pages. 55 topic fragments in `topics/`, router in
`assets/js/app.js`, the **only** topic manifest in `assets/js/topics.js`, the whole design system
in `assets/style.css` (tokens at the top). README has the full architecture, invariants,
tools and traps. Read the relevant README section before touching that area.

## Active work
Visual revamp. Read `docs/visual-revamp/STATUS.md`, then **only** the chunk it names in
`docs/visual-revamp/PLAN.md`. Update STATUS last.

## Rules that bite
- Topic root stays `<section class="section" id="sec-<id>">`, matching `topics.js`.
- No `<style>` blocks in topic files; style lives in `style.css`.
- Every class the JS adds needs a CSS rule (`tools/check_css_hooks.py`).
- Rewrite *around* diagrams, code and tables, never retype them; check with `tools/assets.py`.
- Diagrams use the legacy hexes; style.css §8 maps them to theme tokens.
- `.mjs` tools and their npm deps live in `/tmp/domtest`, never a `package.json` in the repo.
- Push once per chunk. Pages cancels overlapping builds.

## Verify
```bash
python3 tools/check_topics.py --all && python3 tools/audit_markup.py --all && python3 tools/check_css_hooks.py
python3 tools/assets.py cdf20c9 --all   # any count going down = a lost diagram/code/table
python3 tools/run_runners.py
cd /tmp/domtest && node smoke.mjs <repo> && node kxstrict.mjs <repo> && node kxinline.mjs <repo>
python3 -m http.server 8000   # preview; topics need HTTP, not file://
```
