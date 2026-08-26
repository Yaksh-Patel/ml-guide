# ML/DS Master Study Guide

A 55-topic machine learning and data science reference — maths foundations through
classical ML, neural networks, deep learning, NLP, the LLM era, specialised domains and
production system design. Static site, no build step, hosted on GitHub Pages.

**Live:** https://yaksh-patel.github.io/ml-guide/

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
runtime that then installed numpy and scikit-learn through micropip. Only 2 of 55 topics
have a code runner, and only 4 use syntax highlighting. Now:

| Dependency | Loaded when |
|---|---|
| KaTeX | a topic that actually contains `$…$` math is opened |
| Prism | a topic containing `language-*` code is opened |
| CodeMirror | a topic containing `.code-runner` is opened |
| Pyodide | you press **Run** — never before |

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
| `.code-runner` | interactive Python block |

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

## Progress storage

Read state lives in `localStorage` under `ml-guide-progress-v2` — per browser, never sent
anywhere. The key is unchanged from the previous version, so existing progress carries
over. "Reset" on the home page clears it.
