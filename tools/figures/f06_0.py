"""06 bias–variance: the classic decomposition, drawn the right way up.

The old figure drew total error as an inverted U with the "sweet spot" at its
peak. Total error = bias² + variance + irreducible noise is a U, and the sweet
spot is its minimum.
"""
import math
from figkit import Fig, BLUE, GREEN, AMBER, RED, FAINT, LABEL, SMALL

TARGET = ('06-bias-variance', 0)
NOISE = 0.10


def bias2(c):
    return 0.06 + 0.86 * math.exp(-3.4 * c)


def var(c):
    return 0.02 + 0.80 * c ** 2.6


def total(c):
    return bias2(c) + var(c) + NOISE


def draw():
    f = Fig(560, 290, 'bv')
    p = f.plot_area(56, 40, 520, 236, (0, 1), (0, 1.15))
    p.axes(ylabel='error')

    noise = [(p.X(0), p.Y(NOISE)), (p.X(1), p.Y(NOISE))]
    f.path(noise, FAINT, 1.2, dash='3 4')
    b = p.curve(bias2, RED)
    v = p.curve(var, BLUE)
    t = p.curve(total, GREEN, width=3)

    cmin = min((i / 1000 for i in range(1001)), key=total)
    x, y = p.X(cmin), p.Y(total(cmin))
    f.line(x, y + 8, x, p.Y(0), AMBER, 1.4, dash='4 4')
    f.circle(x, y, 5, fill=AMBER)

    # labels last, so the placer sees every line
    f.label('sweet spot', [(x, y - 14, 'middle')], AMBER, LABEL, weight=600)
    f.along(t, 'total error', [0.78, 0.7, 0.86], fill=GREEN, size=LABEL, weight=600)
    f.along(v, 'variance', [0.93, 0.88, 0.8], fill=BLUE, size=LABEL, weight=600)
    f.along(b, 'bias²', [0.3, 0.38, 0.22], fill=RED, size=LABEL, weight=600)
    f.label('irreducible noise', [(p.X(0.03), p.Y(NOISE) - 8, 'start'), (p.X(0.6), p.Y(NOISE) - 8, 'start')], FAINT)
    f.label('underfit', [(p.X(0.08), p.Y(0) + 18, 'middle')], RED)
    f.label('overfit', [(p.X(0.93), p.Y(0) + 18, 'middle')], BLUE)
    f.label('model complexity →', [((p.x0 + p.x1) / 2, p.Y(0) + 34, 'middle')], FAINT)
    return f
