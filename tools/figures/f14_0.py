"""14 SVM: the maximum-margin boundary, its two margin lines, and the three
points that hold it in place.

History: the old figure ringed two "support vectors" that sat well inside
their class, nowhere near the dashed margin lines. Support vectors are by
definition the points ON the margin (|wᵀx + b| = 1), so here they sit
exactly on the dashed lines and every other point is strictly outside the
corridor. The boundary is tilted so it reads as a hyperplane rather than an
axis threshold, and the margin is labelled with the prose's 2/‖w‖.
"""
import math
from figkit import Fig, BLUE, PURPLE, GREEN, AMBER, FAINT, MUTED, BG, LABEL, SMALL

TARGET = ('14-svm', 0)

C = (280, 126)                       # a point on the boundary
ANG = math.radians(25)               # tilt from vertical
D = (math.sin(ANG), -math.cos(ANG))  # along the boundary (upward)
N = (math.cos(ANG), math.sin(ANG))   # normal, toward the purple class
M = 32                               # half-margin, in canvas units
TOP, BOT = 26, 222                   # vertical extent of the lines


def P(s, t):
    return (C[0] + s * D[0] + t * N[0], C[1] + s * D[1] + t * N[1])


def s_at_y(t, y):
    return (y - C[1] - t * N[1]) / D[1]


BLUE_PTS = [(-110, -60), (-100, -118), (-60, -128), (-90, -70), (-10, -86), (10, -150),
            (40, -116), (70, -64)]
PURPLE_PTS = [(-62, 62), (-20, 96), (30, 76), (60, 122), (95, 68), (0, 146), (-55, 128)]
SV_BLUE = [(-45, -M), (55, -M)]
SV_PURPLE = [(5, M)]


def draw():
    f = Fig(560, 270, 'svm')

    # boundary and margin lines, clipped to the same vertical band
    ends = {}
    for t, col, w, dash in ((-M, GREEN, 1.3, '5 4'), (0, GREEN, 2.6, None), (M, GREEN, 1.3, '5 4')):
        a, b = P(s_at_y(t, BOT), t), P(s_at_y(t, TOP), t)
        f.line(*a, *b, col, w, dash=dash, opacity=None if dash is None else 0.75)
        ends[t] = (a, b)

    # margin width, measured perpendicular to the lines
    s0 = -80
    mid, lo, hi = P(s0, 0), P(s0, -M), P(s0, M)
    f.arrow(*mid, *lo, AMBER, 1.4, gap=0.5)
    f.arrow(*mid, *hi, AMBER, 1.4, gap=0.5)

    # points
    for s, t in BLUE_PTS:
        f.circle(*P(s, t), 5.5, fill=BLUE, opacity=0.9)
    for s, t in PURPLE_PTS:
        f.circle(*P(s, t), 5.5, fill=PURPLE, opacity=0.9)
    for (s, t), col in [(p, BLUE) for p in SV_BLUE] + [(p, PURPLE) for p in SV_PURPLE]:
        x, y = P(s, t)
        f.circle(x, y, 5.5, fill=col)
        f.circle(x, y, 10, stroke=AMBER, width=1.8)

    # labels last
    (_, top0), (_, topm), (_, topp) = ends[0], ends[-M], ends[M]
    f.label('wᵀx + b = 0', [(top0[0], top0[1] - 10, 'middle')], GREEN, LABEL, weight=600, pad=2)
    f.label('−1', [(topm[0] - 6, topm[1] + 2, 'end')], MUTED, SMALL, mono=True, pad=2)
    f.label('+1', [(topp[0] + 6, topp[1] + 2, 'start')], MUTED, SMALL, mono=True, pad=2)
    f.label('margin = 2/‖w‖', [(hi[0] + 10, hi[1] + 14, 'start'), (hi[0] + 12, hi[1] + 4, 'start'),
                              (hi[0] + 8, hi[1] + 24, 'start')], AMBER, LABEL, weight=600)
    sx, sy = P(*SV_PURPLE[0])
    f.label('support vectors', [(sx + 16, sy + 4, 'start'), (sx + 16, sy - 8, 'start'),
                                (sx + 16, sy + 16, 'start')], AMBER, LABEL, weight=600)
    f.label('Only the ringed points set the boundary: delete the rest, refit, and it does not move.',
            [(f.w / 2, f.h - 10, 'middle')], MUTED, SMALL)
    return f
