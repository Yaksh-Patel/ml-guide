"""01 eigenvectors: the worked example from the prose, drawn to scale.

A = [[2, 1], [1, 2]] acts on three vectors. v = [1, 1] comes out as [3, 3]:
same line, three times as long (λ = 3). [1, −1] comes out unchanged (λ = 1).
u = [1, 0] comes out as [2, 1]: it turns off its own line. Grey arrows go in,
coloured arrows come out, so there is no dashed/solid key to decode.

History: the old figure used made-up vectors not tied to any matrix, coloured
Au red while labelling it amber, and its caption text was clipped at the left.
"""
import math
from figkit import Fig, BLUE, PURPLE, MUTED, FAINT, INK, LABEL, SMALL

TARGET = ('01-linear-algebra', 0)

U = 56                      # px per unit, same on both axes
OX, OY = 214, 216           # origin on the canvas


def P(x, y):
    return OX + U * x, OY - U * y


def draw():
    f = Fig(560, 320, 'eig')

    # axes (no grid: labels need clean space) with ticks at 1, 2, 3
    f.line(OX - 1.3 * U, OY, OX + 3.6 * U, OY, FAINT, 1)
    f.line(OX, OY + 1.25 * U, OX, OY - 3.6 * U, FAINT, 1)
    for k in (2, 3):           # no tick at x = 1: u's arrowhead lands there
        f.line(OX + k * U, OY - 3, OX + k * U, OY + 3, FAINT, 1)
    for k in (1, 2, 3):
        f.line(OX - 3, OY - k * U, OX + 3, OY - k * U, FAINT, 1)

    # the line v lives on: A keeps every vector on it on it
    f.line(*P(-1.05, -1.05), *P(3.55, 3.55), BLUE, 1, dash='2 5', opacity=0.55)

    # outputs first (coloured), inputs on top (grey)
    f.arrow(*P(0, 0), *P(3, 3), BLUE, 2.6, gap=0)          # Av = 3v
    f.arrow(*P(0, 0), *P(2, 1), PURPLE, 2.6, gap=0)        # Au = [2, 1]
    f.arrow(*P(0, 0), *P(1, -1), BLUE, 2.6, gap=0)         # A[1,-1] = [1,-1]
    f.arrow(*P(0, 0), *P(1, 1), MUTED, 2.2, gap=0)         # v
    f.arrow(*P(0, 0), *P(1, 0), MUTED, 2.2, gap=0)         # u

    # the turn from u to Au, as an arc at radius 1.45
    a1 = math.atan2(1, 2)
    r = 1.45
    pts = [P(r * math.cos(a1 * t / 12), r * math.sin(a1 * t / 12)) for t in range(13)]
    f.path(pts, PURPLE, 1.3, opacity=0.9)

    # labels last
    vx, vy = P(1, 1)
    f.label('v = [1, 1]', [(vx - 2, vy - 8, 'end'), (vx - 6, vy - 4, 'end')], MUTED, LABEL, weight=600)
    f.label('Av = [3, 3] = 3v', [(P(3, 3)[0] + 12, P(3, 3)[1] + 6, 'start'),
                                 (P(3, 3)[0] + 10, P(3, 3)[1] + 16, 'start')], BLUE, LABEL, weight=600)
    f.label('λ = 3: same line, 3× longer', [(P(3, 3)[0] + 12, P(3, 3)[1] + 20, 'start'),
                                            (P(3, 3)[0] + 10, P(3, 3)[1] + 30, 'start')], BLUE, SMALL)
    f.label('u = [1, 0]', [(P(1, 0)[0] - 4, OY + 18, 'middle'), (P(1, 0)[0] + 4, OY + 18, 'start')],
            MUTED, LABEL, weight=600)
    f.label('Au = [2, 1]', [(P(2, 1)[0] + 10, P(2, 1)[1] + 4, 'start')], PURPLE, LABEL, weight=600)
    am = pts[6]
    f.label('turned', [(am[0] + 8, am[1] + 3, 'start'), (am[0] + 10, am[1] + 6, 'start')], PURPLE, SMALL)
    f.label('A[1, −1] = [1, −1]', [(P(1, -1)[0] + 12, P(1, -1)[1] + 4, 'start')], BLUE, LABEL, weight=600)
    f.label('λ = 1: unchanged', [(P(1, -1)[0] + 12, P(1, -1)[1] + 18, 'start')], BLUE, SMALL)

    # the matrix, and the key in words
    mx, my = 30, 40
    f.text(mx, my + 13, 'A =', INK, LABEL, weight=600, mono=True)
    for side, x in ((1, mx + 30), (-1, mx + 78)):
        f.path([(x + 4 * side, my - 2), (x, my - 2), (x, my + 22), (x + 4 * side, my + 22)], MUTED, 1.2)
    for r, row in enumerate(((2, 1), (1, 2))):
        for c, v in enumerate(row):
            f.text(mx + 44 + 20 * c, my + 7 + 13 * r, str(v), INK, LABEL, 'middle', 600, mono=True)
    f.label('grey: before A', [(mx, my + 46, 'start')], MUTED, SMALL)
    f.label('colour: after A', [(mx, my + 60, 'start')], MUTED, SMALL)
    f.label('an eigenvector stays on its own line; everything else turns',
            [(OX + 1.25 * U, 312, 'middle')], MUTED, SMALL)
    return f
