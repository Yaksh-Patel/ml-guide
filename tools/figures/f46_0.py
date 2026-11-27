"""46 GNNs: one layer is one hop of neighbourhood averaging, the GCN update
that does it, and why stacking it over-smooths.

The graph is the code card's (edges 0–1, 0–2, 1–2, 2–3, 3–4). Node 2 takes
messages from 0, 1, 3 and itself (the self-loop is the +I). The over-smoothing
curve is the code card's own measurement, the mean distance of each node's
embedding from the mean after k applications of D^-½(A+I)D^-½ to one-hot
features: 100, 41, 31, 25, 20, 16, 13, 11, 9 % of the start (the prose quotes
41% after one layer, 9% after eight).

History: the old curve was a generic decay with no scale. The GraphSAGE
paragraph inside the figure was dropped; the code card says it.
"""
import math
from figkit import (Fig, BLUE, AMBER, RED, GREEN, INK, MUTED, FAINT, BORD, SURF, BG,
                    LABEL, SMALL)

TARGET = ('46-gnns', 0)

NODES = {0: (52, 104), 1: (122, 62), 2: (126, 158), 3: (204, 122), 4: (214, 206)}
EDGES = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)]
R = 13
SPREAD = [1.0, 0.410, 0.307, 0.245, 0.198, 0.160, 0.131, 0.109, 0.091]


def toward(a, b, d):
    (x1, y1), (x2, y2) = a, b
    L = math.dist(a, b)
    return x1 + (x2 - x1) * d / L, y1 + (y2 - y1) * d / L


def draw():
    f = Fig(560, 300, 'gcn')

    # ---- left: one hop ------------------------------------------------------
    f.text(20, 22, 'one layer = one hop', INK, LABEL, weight=600)
    for a, b in EDGES:
        pa, pb = NODES[a], NODES[b]
        if 2 in (a, b):                     # a message into node 2
            src, dst = (pa, pb) if b == 2 else (pb, pa)
            p, q = toward(src, dst, R), toward(dst, src, R)
            f.arrow(*p, *q, BLUE, 1.8)
        else:
            p, q = toward(pa, pb, R), toward(pb, pa, R)
            f.line(*p, *q, FAINT, 1.4)
    # self-loop under node 2 (the +I)
    x2, y2 = NODES[2]
    a0, a1 = math.radians(90 + 58), math.radians(90 - 58)
    p0 = (x2 + (R + 1) * math.cos(a0), y2 + (R + 1) * math.sin(a0))
    p1 = (x2 + (R + 4) * math.cos(a1), y2 + (R + 4) * math.sin(a1))
    f.qcurve(p0, (x2, y2 + 62), p1, BLUE, 1.6, arrow=True)
    for k, (x, y) in NODES.items():
        if k == 2:
            f.circle(x, y, R, fill=SURF, stroke=AMBER, width=2.2)
            col = AMBER
        elif k == 4:
            f.circle(x, y, R, fill=SURF, stroke=BORD, width=1.6)
            col = FAINT
        else:
            f.circle(x, y, R, fill=SURF, stroke=BLUE, width=1.6)
            col = INK
        f.text(x, y + 3.4, str(k), col, LABEL, 'middle', weight=600, mono=True, halo=False, check=False)

    # ---- right top: the update --------------------------------------------------
    fx = 300
    f.text(fx, 36, 'H′ = σ( D⁻½ (A+I) D⁻½ · H · W )', INK, LABEL, mono=True, weight=600)
    f.text(fx, 58, '+I', GREEN, SMALL, mono=True, weight=600)
    f.text(fx + 30, 58, 'self-loops, or a node forgets itself', MUTED, SMALL)
    f.text(fx, 74, 'D⁻½', GREEN, SMALL, mono=True, weight=600)
    f.text(fx + 30, 74, 'normalise, or hubs drown their neighbours', MUTED, SMALL)

    # ---- right bottom: over-smoothing -----------------------------------------
    p = f.plot_area(300, 122, 520, 236, (0, 8), (0, 1.05))
    p.axes(ylabel='node spread, % of the start')
    f.text((p.x0 + p.x1) / 2, p.Y(0) + 28, 'depth (layers) →', FAINT, SMALL, 'middle')
    for d in (1, 2, 4, 8):
        f.text(p.X(d), p.Y(0) + 13, str(d), FAINT, SMALL, 'middle', mono=True)
    x3 = p.X(3)
    f.raw(f'<rect x="{p.X(2):.1f}" y="{p.y0:.1f}" width="{p.X(3) - p.X(2):.1f}" height="{p.y1 - p.y0:.1f}" '
          f'fill="{AMBER}" fill-opacity=".10"/>')
    pts = [(p.X(d), p.Y(v)) for d, v in enumerate(SPREAD)]
    f.path(pts, RED, 2.4)
    curve = pts
    for x, y in pts:
        f.circle(x, y, 2.8, fill=RED, stroke=BG, width=1)

    # labels last
    f.label('message', [(84, 146, 'end'), (80, 150, 'end')], BLUE, SMALL)
    f.label('node 2 averages 0, 1, 3 and itself', [(126, 222, 'middle'), (110, 236, 'middle')], AMBER, SMALL, weight=600)
    f.label('reached at layer 2', [(214 - 20, 206 + 24, 'start'), (214, 230, 'middle'), (232, 210, 'start')], FAINT, SMALL)
    f.label('41%', [(pts[1][0] + 8, pts[1][1] - 4, 'start')], RED, SMALL, weight=600, mono=True)
    f.label('9% after 8', [(pts[8][0], pts[8][1] - 12, 'end'), (pts[8][0] - 6, pts[8][1] - 10, 'end')], RED, SMALL, weight=600)
    f.label('2–3 layers', [((p.X(2) + x3) / 2, p.y0 + 12, 'middle'), (x3 + 6, p.y0 + 12, 'start')], AMBER, SMALL, weight=600)
    f.along(curve, 'over-smoothing', [0.5, 0.45, 0.62], fill=RED, size=LABEL, weight=600)

    f.text(280, 290, 'On a graph, depth is radius, not capacity: stop at 2–3 layers.', MUTED, LABEL, 'middle')
    return f
