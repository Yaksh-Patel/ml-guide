"""47 bipartite graphs: users ↔ items, and the rating matrix R it is stored as.

The old figure printed ratings on the edges, where they sat on top of each
other and of the crossing lines. The ratings now live where the prose puts
them, in the biadjacency block R next to the graph: one row per user, one
column per item, a blank for every pair never observed, and the red cell is
the dashed edge the model is asked to predict. The four ratings the old figure
showed are kept (u₁–v₁ 5, u₁–v₂ 3, u₂–v₁ 4, u₃–v₄ 5); the other three
interactions get illustrative values.
"""
import math
from figkit import Fig, BLUE, GREEN, RED, FAINT, MUTED, INK, SURF, BORD, LABEL, SMALL, TINY, GAP

TARGET = ('47-bipartite-graphs', 0)
SUB = '₁₂₃₄'
R = [[5, 3, None, None],
     [4, None, 2, 5],
     [None, 4, None, 5]]
PREDICT = (0, 2)          # u₁ – v₃
NR = 15


def node(f, x, y, label, col):
    ring = [(x + NR * math.cos(t * math.pi / 12), y + NR * math.sin(t * math.pi / 12)) for t in range(25)]
    f.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{NR}" fill="{SURF}" stroke="{col}" stroke-width="2"/>', pts=ring)
    f.text(x, y + 3.6, label, col, LABEL, 'middle', weight=600, halo=False)


def draw():
    f = Fig(560, 248, 'bip')
    ux, vx = 70, 300
    uy = [70, 124, 178]
    vy = [48, 100, 152, 204]

    # the two sides
    for x, col in ((ux, BLUE), (vx, GREEN)):     # tinted panels, no outline for edges to cross
        f.raw(f'<rect x="{x - 36}" y="26" width="72" height="200" rx="12" fill="{col}" fill-opacity=".07"/>')

    def edge(i, j, **kw):
        (x1, y1), (x2, y2) = (ux, uy[i]), (vx, vy[j])
        d = math.dist((x1, y1), (x2, y2))
        ex, ey = (x2 - x1) / d, (y2 - y1) / d
        o = NR + 3
        f.line(x1 + ex * o, y1 + ey * o, x2 - ex * o, y2 - ey * o, **kw)
        return (x1 + ex * o, y1 + ey * o), (x2 - ex * o, y2 - ey * o)

    for i, row in enumerate(R):
        for j, v in enumerate(row):
            if v is not None:
                edge(i, j, stroke=MUTED, width=1.4, opacity=.75)
    edge(*PREDICT, stroke=RED, width=1.6, dash='5 4')

    for i, y in enumerate(uy):
        node(f, ux, y, 'u' + SUB[i], BLUE)
    for j, y in enumerate(vy):
        node(f, vx, y, 'v' + SUB[j], GREEN)

    # the rating matrix R
    cw, mx0, my0 = 30, 420, 78
    for i, row in enumerate(R):
        for j, v in enumerate(row):
            x, y = mx0 + j * cw, my0 + i * cw
            pred = (i, j) == PREDICT
            f.rect(x, y, cw, cw, fill=SURF, stroke=RED if pred else BORD, r=2, width=1.6 if pred else 1)
            if pred:
                f.text(x + cw / 2, y + cw / 2 + 3.6, '?', RED, LABEL, 'middle', weight=600, mono=True, halo=False)
            elif v is not None:
                f.text(x + cw / 2, y + cw / 2 + 3.6, str(v), INK, LABEL, 'middle', mono=True, halo=False)
    for j in range(4):
        f.text(mx0 + j * cw + cw / 2, my0 - 8, 'v' + SUB[j], GREEN, SMALL, 'middle', weight=600)
    for i in range(3):
        f.text(mx0 - 8, my0 + i * cw + cw / 2 + 3, 'u' + SUB[i], BLUE, SMALL, 'end', weight=600)

    # labels last
    f.label('U  users', [(ux, 18, 'middle')], BLUE, LABEL, weight=600)
    f.label('V  items', [(vx, 18, 'middle')], GREEN, LABEL, weight=600)
    f.label('R   users × items', [(mx0 + 2 * cw, my0 - 26, 'middle')], INK, LABEL, weight=600)
    f.label('blank = never observed', [(mx0 + 2 * cw, my0 + 3 * cw + 16, 'middle')], FAINT, TINY)
    f.label('? = the pair to predict', [(mx0 + 2 * cw, my0 + 3 * cw + 30, 'middle')], RED, TINY, weight=600)
    f.label('no edge inside U or inside V: everything the graph knows sits in R',
            [(f.w / 2, 242, 'middle')], MUTED, SMALL)
    return f
