#!/usr/bin/env python3
"""figkit: the v2 drawing kit for ML Atlas diagrams.

One figure = one module in tools/figures/ with TARGET = (topic file stem,
figure index) and draw() -> Fig. `python3 tools/figures/build.py` renders it
and swaps it into that topic's Nth .anim-wrap, keeping the wrapper and the
caption. Rules are in docs/figure-revamp/PLAN.md §2; in short:

  * Canvas 560 wide (up to 640 if the content needs it). app.js renders at
    most 1.45 px per unit; a 560 canvas gets ~1.36 at 1440 with the rail, so
    a 10-unit label is ~13.5px.
  * Text sizes: LABEL 10, SMALL 9, TINY 8.5. Nothing smaller.
  * Labels sit next to what they name, never on a line. Fig.check() enforces
    it: text may not overlap other text, any stroke, or the canvas edge.
  * Every label gets a thin halo in the panel colour, so near-misses stay clean.
  * Arrows: one arrowhead size everywhere (user units, not stroke-scaled),
    and arrows stop GAP units short of what they point at.
  * Motion is SMIL on one shared clock (Anim). The figure declares a still
    time: under prefers-reduced-motion app.js freezes it there, so the still
    frame must show the complete picture.
  * Colours are the legacy hexes (style.css §8 maps them to both themes).
"""
import math, html as _html

INK, MUTED, FAINT = '#e6e9f4', '#8e97b8', '#4e5a7a'
SURF, BORD, BG = '#1a1f2e', '#2e3a58', '#0b0d12'
BLUE, GREEN, AMBER, RED, PURPLE = '#5ba4fb', '#22d3a0', '#f5a623', '#f06767', '#b97cf8'
LABEL, SMALL, TINY = 10, 9, 8.5
GAP = 4            # arrows stop this far short of their target
HEAD_W, HEAD_L = 6, 7

# Average advance per character as a fraction of font size: IBM Plex Sans
# Condensed (the diagram face) and JetBrains Mono. Deliberately generous.
_W_SANS, _W_MONO = 0.50, 0.62


def _esc(s):
    return _html.escape(str(s), quote=True)


def _seg_hits_rect(x1, y1, x2, y2, r):
    """Does segment (x1,y1)-(x2,y2) touch rectangle r = (x0, y0, x1, y1)?"""
    rx0, ry0, rx1, ry1 = r
    dx, dy = x2 - x1, y2 - y1
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x1 - rx0), (dx, rx1 - x1), (-dy, y1 - ry0), (dy, ry1 - y1)):
        if p == 0:
            if q < 0:
                return False
        else:
            t = q / p
            if p < 0:
                if t > t1: return False
                t0 = max(t0, t)
            else:
                if t < t0: return False
                t1 = min(t1, t)
    return t0 <= t1


def quad_points(p0, c, p1, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1])
            for t in (i / n for i in range(n + 1))]


def polyline_length(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


class Fig:
    def __init__(self, w, h, fid):
        self.w, self.h, self.fid = w, h, fid
        self.parts = []
        self.texts = []          # (x0, y0, x1, y1, s)
        self.segs = []           # stroke segments, for the text-vs-line check
        self.markers = {}        # colour -> marker id
        self.still = None        # seconds: the frame shown under reduced motion

    # ---- helpers ---------------------------------------------------------------
    def marker(self, color=FAINT):
        if color not in self.markers:
            self.markers[color] = f'{self.fid}-ah{len(self.markers)}'
        return self.markers[color]

    def _record(self, pts):
        self.segs += list(zip(pts, pts[1:]))

    def raw(self, s, pts=None):
        """Raw markup. Pass the drawn geometry as pts so check() can see it."""
        self.parts.append(s)
        if pts:
            self._record(pts)

    # ---- primitives ------------------------------------------------------------
    def text(self, x, y, s, fill=MUTED, size=SMALL, anchor='start', weight=None, mono=False,
             halo=True, check=True, extra=''):
        """y is the baseline."""
        w = len(str(s)) * size * (_W_MONO if mono else _W_SANS)
        x0 = {'start': x, 'middle': x - w / 2, 'end': x - w}[anchor]
        if check:
            self.texts.append((x0, y - size * 0.76, x0 + w, y + size * 0.22, str(s)))
        fam = 'JetBrains Mono' if mono else 'DM Sans'   # style.css maps both
        wt = f' font-weight="{weight}"' if weight else ''
        hl = (f' stroke="{SURF}" stroke-width="3" paint-order="stroke" stroke-linejoin="round"'
              if halo else '')
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" '
                          f'text-anchor="{anchor}" font-family="{fam}"{wt}{hl}{extra}>{_esc(s)}</text>')

    def line(self, x1, y1, x2, y2, stroke=FAINT, width=1.2, dash=None, arrow=False, opacity=None,
             gap=0, extra=''):
        if gap:
            d = math.dist((x1, y1), (x2, y2)) or 1
            ux, uy = (x2 - x1) / d, (y2 - y1) / d
            x1, y1, x2, y2 = x1 + ux * gap, y1 + uy * gap, x2 - ux * gap, y2 - uy * gap
        da = f' stroke-dasharray="{dash}"' if dash else ''
        op = f' opacity="{opacity}"' if opacity is not None else ''
        mk = f' marker-end="url(#{self.marker(stroke)})"' if arrow else ''
        self.parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                          f'stroke="{stroke}" stroke-width="{width}" stroke-linecap="round"{da}{op}{mk}{extra}/>')
        self._record([(x1, y1), (x2, y2)])

    def arrow(self, x1, y1, x2, y2, stroke=FAINT, width=1.4, gap=GAP, **kw):
        self.line(x1, y1, x2, y2, stroke, width, arrow=True, gap=gap, **kw)

    def path(self, pts, stroke, width=2.2, dash=None, fill='none', opacity=None, extra=''):
        d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ''
        op = f' opacity="{opacity}"' if opacity is not None else ''
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" '
                          f'stroke-linecap="round" stroke-linejoin="round"{da}{op}{extra}/>')
        self._record(pts)

    def circle(self, cx, cy, r, fill=None, stroke=None, width=1.6, opacity=None, extra='', body=''):
        f = f' fill="{fill}"' if fill else ' fill="none"'
        s = f' stroke="{stroke}" stroke-width="{width}"' if stroke else ''
        op = f' opacity="{opacity}"' if opacity is not None else ''
        if body:
            self.parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}"{f}{s}{op}{extra}>{body}</circle>')
        else:
            self.parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}"{f}{s}{op}{extra}/>')
        # a dot is an obstacle for labels too
        self._record([(cx - r, cy - r), (cx + r, cy + r)])
        self._record([(cx - r, cy + r), (cx + r, cy - r)])

    def rect(self, x, y, w, h, fill=SURF, stroke=BORD, r=6, width=1, opacity=None):
        op = f' opacity="{opacity}"' if opacity is not None else ''
        self.parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"{op}/>')
        self._record([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)])

    # ---- label placement -----------------------------------------------------------
    def _box(self, x, y, s, size, mono, anchor):
        w = len(str(s)) * size * (_W_MONO if mono else _W_SANS)
        x0 = {'start': x, 'middle': x - w / 2, 'end': x - w}[anchor]
        return (x0, y - size * 0.76, x0 + w, y + size * 0.22)

    def _free(self, b, pad=3):
        a0, b0, a1, b1 = b
        if a0 < 2 or b0 < 2 or a1 > self.w - 2 or b1 > self.h - 2:
            return False
        r = (a0 - pad, b0 - pad, a1 + pad, b1 + pad)
        for (c0, d0, c1, d1, _) in self.texts:
            if min(r[2], c1) > max(r[0], c0) and min(r[3], d1) > max(r[1], d0):
                return False
        return not any(_seg_hits_rect(p[0], p[1], q[0], q[1], r) for p, q in self.segs)

    def label(self, s, cands, fill=MUTED, size=SMALL, weight=None, mono=False, pad=3):
        """Place s at the first candidate (x, y, anchor) that is clear of every
        label, stroke and the canvas edge by `pad`. Draw geometry first."""
        for (x, y, anchor) in cands:
            if self._free(self._box(x, y, s, size, mono, anchor), pad):
                self.text(x, y, s, fill, size, anchor, weight, mono)
                return x, y, anchor
        raise ValueError(f'no free spot for label {s!r}')

    @staticmethod
    def around(x, y, d=12, size=SMALL):
        """Candidate spots around a point, nearest first."""
        up, dn = y - d, y + d + size * 0.7
        return [(x + d, up, 'start'), (x - d, up, 'end'), (x + d, dn, 'start'), (x - d, dn, 'end'),
                (x, up - 2, 'middle'), (x, dn + 2, 'middle'),
                (x + d + 4, y + size * 0.3, 'start'), (x - d - 4, y + size * 0.3, 'end')]

    def along(self, pts, s, frac_list, d=12, **kw):
        """Label a curve: try spots around points at the given fractions of it."""
        cands = []
        for fr in frac_list:
            x, y = pts[min(len(pts) - 1, int(fr * (len(pts) - 1)))]
            cands += self.around(x, y, d, kw.get('size', SMALL))
        return self.label(s, cands, **kw)

    # ---- plotting ----------------------------------------------------------------
    def plot_area(self, x0, y0, x1, y1, xr, yr):
        """Data → canvas mapping. y0 is the TOP edge, y1 the bottom."""
        return Plot(self, x0, y0, x1, y1, xr, yr)

    # ---- output --------------------------------------------------------------------
    def check(self):
        errs = []
        for (a0, b0, a1, b1, s) in self.texts:
            if a0 < -0.5 or b0 < -0.5 or a1 > self.w + 0.5 or b1 > self.h + 0.5:
                errs.append(f'off canvas: {s!r}')
        T = self.texts
        for i in range(len(T)):
            for j in range(i + 1, len(T)):
                a, b = T[i], T[j]
                if min(a[2], b[2]) - max(a[0], b[0]) > 0.5 and min(a[3], b[3]) - max(a[1], b[1]) > 0.5:
                    errs.append(f'text over text: {a[4]!r} × {b[4]!r}')
        for (a0, b0, a1, b1, s) in T:
            r = (a0 - 1, b0 - 1, a1 + 1, b1 + 1)
            if any(_seg_hits_rect(p[0], p[1], q[0], q[1], r) for p, q in self.segs):
                errs.append(f'text over a line or shape: {s!r}')
        return errs

    def svg(self):
        defs = '<defs>' + ''.join(
            f'<marker id="{mid}" markerUnits="userSpaceOnUse" markerWidth="{HEAD_L}" markerHeight="{HEAD_W}" '
            f'refX="{HEAD_L - 0.5}" refY="{HEAD_W / 2}" orient="auto">'
            f'<path d="M0,0 L{HEAD_L},{HEAD_W / 2} L0,{HEAD_W} z" fill="{col}"/></marker>'
            for col, mid in self.markers.items()) + '</defs>'
        still = f' data-still="{self.still}"' if self.still is not None else ''
        body = '\n'.join(self.parts)
        return (f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" '
                f'role="img" data-fig="v2"{still}>\n{defs}\n{body}\n</svg>')


class Plot:
    def __init__(self, fig, x0, y0, x1, y1, xr, yr):
        self.f, self.x0, self.y0, self.x1, self.y1 = fig, x0, y0, x1, y1
        self.xa, self.xb = xr
        self.ya, self.yb = yr

    def X(self, v):
        return self.x0 + (self.x1 - self.x0) * (v - self.xa) / (self.xb - self.xa)

    def Y(self, v):
        return self.y1 - (self.y1 - self.y0) * (v - self.ya) / (self.yb - self.ya)

    def axes(self, xlabel=None, ylabel=None):
        f = self.f
        f.arrow(self.x0, self.y1, self.x1 + 12, self.y1, FAINT, 1.2, gap=0)
        f.arrow(self.x0, self.y1, self.x0, self.y0 - 12, FAINT, 1.2, gap=0)
        if xlabel:
            f.text(self.x1 + 12, self.y1 + 18, xlabel, FAINT, SMALL, anchor='end')
        if ylabel:
            f.text(self.x0 + 8, self.y0 - 10, ylabel, FAINT, SMALL)

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
            elif pts:
                edge = self.yb if y > self.yb else self.ya
                pv, py = prev
                vc = pv + (edge - py) * (v - pv) / (y - py)
                pts.append((self.X(vc), self.Y(edge)))
                break
            prev = (v, y)
        self.f.path(pts, color, width, dash)
        return pts


class Anim:
    """One shared SMIL clock for a figure: every animation runs for `period`
    seconds and repeats; key times are given in seconds. Fig.still says which
    second the reduced-motion still frame shows."""

    def __init__(self, period):
        self.T = period

    def kt(self, secs):
        return ';'.join(f'{min(max(s / self.T, 0), 1):.4f}' for s in secs)

    def attr(self, name, pairs, spline=False):
        """pairs = [(second, value), ...]: first at 0, last at the period."""
        vals = ';'.join(str(p[1]) for p in pairs)
        sp = ''
        if spline:
            sp = ' calcMode="spline" keySplines="' + ';'.join(['.45 0 .25 1'] * (len(pairs) - 1)) + '"'
        return (f'<animate attributeName="{name}" dur="{self.T}s" repeatCount="indefinite" '
                f'values="{vals}" keyTimes="{self.kt([p[0] for p in pairs])}"{sp}/>')

    def motion(self, d, pairs):
        """animateMotion along path d; pairs = [(second, fraction of the path)]."""
        kp = ';'.join(f'{p[1]:.4f}' for p in pairs)
        sp = ';'.join(['.45 0 .25 1'] * (len(pairs) - 1))
        return (f'<animateMotion dur="{self.T}s" repeatCount="indefinite" path="{d}" '
                f'keyPoints="{kp}" keyTimes="{self.kt([p[0] for p in pairs])}" calcMode="spline" keySplines="{sp}"/>')
