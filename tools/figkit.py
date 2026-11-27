#!/usr/bin/env python3
"""figkit: the v2 drawing kit for ML Atlas diagrams.

One figure = one module in tools/figures/ with TARGET = (topic file stem,
figure index) and draw() -> Fig. `python3 tools/figures/build.py` renders it
and swaps it into that topic's Nth .anim-wrap, keeping the wrapper and the
caption. See README → Diagrams for the rules this kit enforces.

Rules, in short
  * Canvas 560 wide (up to 640 if the content needs it). app.js renders at most
    1.45 px per unit; a 560 canvas gets ~1.36 at 1440 with the rail, so a
    10-unit label is ~13.5px.
  * Text sizes: LABEL 10, SMALL 9, TINY 8.5. Nothing smaller.
  * Labels sit on their curve/box with clearance; no legend boxes.
  * At most one takeaway line inside the SVG; the prose does the explaining.
  * Colours are the legacy hexes (style.css §8 maps them to both themes).
  * Fig.check() rejects text that overlaps other text or leaves the canvas,
    using estimated widths; tools/figure_lint.mjs is the in-browser truth.
"""
import math, html as _html

INK, MUTED, FAINT = '#e6e9f4', '#8e97b8', '#4e5a7a'
SURF, BORD = '#1a1f2e', '#2e3a58'
BLUE, GREEN, AMBER, RED, PURPLE = '#5ba4fb', '#22d3a0', '#f5a623', '#f06767', '#b97cf8'
LABEL, SMALL, TINY = 10, 9, 8.5

# Average advance per character as a fraction of font size. IBM Plex Sans
# Condensed (diagram face) and JetBrains Mono. Deliberately generous.
_W_SANS, _W_MONO = 0.50, 0.62


def _esc(s):
    return _html.escape(str(s), quote=True)


class Fig:
    def __init__(self, w, h, fid):
        self.w, self.h, self.fid = w, h, fid
        self.parts = []
        self.texts = []          # (x0, y0, x1, y1, s) for check()
        self.markers = {}        # colour -> marker id

    def marker(self, color=FAINT):
        """Arrowhead marker id for a colour (one <marker> per colour used)."""
        if color not in self.markers:
            self.markers[color] = f'{self.fid}-ah{len(self.markers)}'
        return self.markers[color]

    # ---- primitives --------------------------------------------------------
    def raw(self, s):
        self.parts.append(s)

    def text(self, x, y, s, fill=MUTED, size=SMALL, anchor='start', weight=None, mono=False, check=True):
        """y is the baseline. Box estimate: cap height above, descender below."""
        w = len(str(s)) * size * (_W_MONO if mono else _W_SANS)
        x0 = {'start': x, 'middle': x - w / 2, 'end': x - w}[anchor]
        if check:
            self.texts.append((x0, y - size * 0.78, x0 + w, y + size * 0.24, str(s)))
        fam = 'JetBrains Mono' if mono else 'DM Sans'   # style.css maps both
        wt = f' font-weight="{weight}"' if weight else ''
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" '
                          f'text-anchor="{anchor}" font-family="{fam}"{wt}>{_esc(s)}</text>')

    def line(self, x1, y1, x2, y2, stroke=FAINT, width=1, dash=None, arrow=False, opacity=None):
        da = f' stroke-dasharray="{dash}"' if dash else ''
        op = f' opacity="{opacity}"' if opacity is not None else ''
        mk = f' marker-end="url(#{self.marker(stroke)})"' if arrow else ''
        self.parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                          f'stroke="{stroke}" stroke-width="{width}"{da}{op}{mk}/>')

    def path(self, pts, stroke, width=2.2, dash=None, fill='none', opacity=None):
        d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ''
        op = f' opacity="{opacity}"' if opacity is not None else ''
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" '
                          f'stroke-linecap="round" stroke-linejoin="round"{da}{op}/>')

    def circle(self, cx, cy, r, fill=None, stroke=None, width=1.6, opacity=None):
        f = f' fill="{fill}"' if fill else ' fill="none"'
        s = f' stroke="{stroke}" stroke-width="{width}"' if stroke else ''
        op = f' opacity="{opacity}"' if opacity is not None else ''
        self.parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}"{f}{s}{op}/>')

    def rect(self, x, y, w, h, fill=SURF, stroke=BORD, r=6, width=1, opacity=None):
        op = f' opacity="{opacity}"' if opacity is not None else ''
        self.parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"{op}/>')

    # ---- plotting -------------------------------------------------------------
    def plot_area(self, x0, y0, x1, y1, xr, yr):
        """Data → canvas mapping for a plot box. y0 is the TOP edge, y1 the bottom."""
        return Plot(self, x0, y0, x1, y1, xr, yr)

    # ---- output ---------------------------------------------------------------
    def check(self):
        errs = []
        for (a0, b0, a1, b1, s) in self.texts:
            if a0 < -0.5 or b0 < -0.5 or a1 > self.w + 0.5 or b1 > self.h + 0.5:
                errs.append(f'off canvas: {s!r} ({a0:.0f},{b0:.0f})-({a1:.0f},{b1:.0f})')
        T = self.texts
        for i in range(len(T)):
            for j in range(i + 1, len(T)):
                a, b = T[i], T[j]
                if min(a[2], b[2]) - max(a[0], b[0]) > 0.5 and min(a[3], b[3]) - max(a[1], b[1]) > 0.5:
                    errs.append(f'overlap: {a[4]!r} × {b[4]!r}')
        return errs

    def svg(self):
        defs = '<defs>' + ''.join(
            f'<marker id="{mid}" markerWidth="7" markerHeight="6" refX="6" refY="3" orient="auto">'
            f'<polygon points="0 0,7 3,0 6" fill="{col}"/></marker>' for col, mid in self.markers.items()) + '</defs>'
        body = '\n'.join(self.parts)
        return (f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" '
                f'role="img" data-fig="v2">\n{defs}\n{body}\n</svg>')


class Plot:
    def __init__(self, fig, x0, y0, x1, y1, xr, yr):
        self.f, self.x0, self.y0, self.x1, self.y1 = fig, x0, y0, x1, y1
        self.xa, self.xb = xr
        self.ya, self.yb = yr

    def X(self, v):
        return self.x0 + (self.x1 - self.x0) * (v - self.xa) / (self.xb - self.xa)

    def Y(self, v):
        return self.y1 - (self.y1 - self.y0) * (v - self.ya) / (self.yb - self.ya)

    def axes(self, xlabel=None, ylabel=None, arrows=True):
        f = self.f
        f.line(self.x0, self.y1, self.x1 + (8 if arrows else 0), self.y1, FAINT, 1.2, arrow=arrows)
        f.line(self.x0, self.y1, self.x0, self.y0 - (8 if arrows else 0), FAINT, 1.2, arrow=arrows)
        if xlabel:
            f.text(self.x1, self.y1 + 18, xlabel, FAINT, SMALL, anchor='end')
        if ylabel:
            # horizontal, above the y axis: never collides with tick labels or curves
            f.text(self.x0, self.y0 - 14, ylabel, FAINT, SMALL, anchor='start')

    def curve(self, fn, color, width=2.4, dash=None, n=120, clip=True, xr=None):
        """Sample fn over the x range. With clip, the curve ends exactly where it
        leaves the plot box (points before it enters are skipped). Returns the
        canvas points, so labels can be placed against the curve."""
        a, b = xr or (self.xa, self.xb)
        pts, prev = [], None
        for i in range(n + 1):
            v = a + (b - a) * i / n
            y = fn(v)
            inside = self.ya <= y <= self.yb
            if inside or not clip:
                pts.append((self.X(v), self.Y(y)))
            elif pts:   # leaving the box: end on the edge
                edge = self.yb if y > self.yb else self.ya
                pv, py = prev
                vc = pv + (edge - py) * (v - pv) / (y - py)
                pts.append((self.X(vc), self.Y(edge)))
                break
            prev = (v, y)
        self.f.path(pts, color, width, dash)
        return pts
