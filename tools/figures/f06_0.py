"""06 bias–variance: the classic decomposition, drawn the right way up.

The old figure drew total error as an inverted U with the "sweet spot" at its
peak. Total error = bias² + variance + irreducible noise is a U, and the sweet
spot is its minimum.
"""
import math
from figkit import Fig, BLUE, GREEN, AMBER, RED, FAINT, MUTED, LABEL, SMALL

TARGET = ('06-bias-variance', 0)


def bias2(c):
    return 0.06 + 0.86 * math.exp(-3.4 * c)


def var(c):
    return 0.02 + 0.80 * c ** 2.6


NOISE = 0.10


def total(c):
    return bias2(c) + var(c) + NOISE


def draw():
    f = Fig(560, 300, 'bv')
    p = f.plot_area(56, 40, 520, 246, (0, 1), (0, 1.15))
    p.axes(ylabel='error')
    f.text((p.x0 + p.x1) / 2, p.y1 + 34, 'model complexity →', FAINT, SMALL, anchor='middle')

    # irreducible noise floor
    f.line(p.X(0), p.Y(NOISE), p.X(1), p.Y(NOISE), FAINT, 1.2, dash='3 4')
    f.text(p.X(0.02), p.Y(NOISE) - 6, 'irreducible noise', FAINT, SMALL)

    p.curve(bias2, RED)
    p.curve(var, BLUE)
    tot = p.curve(total, GREEN, width=3)

    # the minimum of the total, found numerically
    cs = [i / 1000 for i in range(1001)]
    cmin = min(cs, key=total)
    x, y = p.X(cmin), p.Y(total(cmin))
    f.line(x, y + 7, x, p.Y(0), AMBER, 1.4, dash='4 4')
    f.circle(x, y, 5, fill=AMBER)
    f.text(x, y - 13, 'sweet spot', AMBER, LABEL, anchor='middle', weight=600)

    # direct labels, placed against each curve
    f.text(p.X(0.30) + 4, p.Y(bias2(0.30)) + 16, 'bias²', RED, LABEL, weight=600)
    f.text(p.X(0.93) - 6, p.Y(var(0.93)) + 4, 'variance', BLUE, LABEL, anchor='end', weight=600)
    f.text(p.X(0.80) - 2, p.Y(total(0.80)) - 9, 'total error', GREEN, LABEL, anchor='end', weight=600)

    # regimes under the axis
    f.text(p.X(0.10), p.Y(0) + 18, 'underfit', RED, SMALL, anchor='middle')
    f.text(p.X(0.92), p.Y(0) + 18, 'overfit', BLUE, SMALL, anchor='middle')
    return f
