"""11 linear vs logistic: the same linear core, one squashing function apart.

Left: linear regression, a line through a continuous target; it runs off the
top of the plot because nothing bounds it. Right: logistic regression on 0/1
labels; the same kind of linear score wx + b, passed through σ, stays between
the dashed 0 and 1. The σ arrow between the panels is the only difference.
"""
import math
from figkit import Fig, BLUE, GREEN, FAINT, MUTED, BG, LABEL, SMALL

TARGET = ('11-linear-logistic', 0)

# continuous target for the left panel (x, y), roughly y = 0.12 + 0.78x
LIN = [(0.06, 0.22), (0.14, 0.17), (0.22, 0.36), (0.3, 0.33), (0.38, 0.47), (0.46, 0.43),
       (0.54, 0.6), (0.62, 0.56), (0.7, 0.71), (0.78, 0.68), (0.86, 0.84)]
# binary labels for the right panel: mostly 0 on the left, mostly 1 on the right
BIN = [(0.05, 0), (0.12, 0), (0.2, 0), (0.28, 0), (0.36, 0), (0.44, 1), (0.5, 0), (0.58, 1),
       (0.64, 0), (0.7, 1), (0.78, 1), (0.86, 1), (0.94, 1)]


def line(x):
    return 0.12 + 0.86 * x


def sig(x):
    return 1 / (1 + math.exp(-11 * (x - 0.55)))


def draw():
    f = Fig(560, 262, 'lin')
    a = f.plot_area(56, 56, 232, 196, (0, 1), (0, 0.94))
    a.axes(xlabel='x →', ylabel='y')
    for x, y in LIN:
        f.circle(a.X(x), a.Y(y), 3, fill=BLUE, opacity=0.55)
    la = a.curve(line, BLUE, width=2.6, xr=(0, 1.1))

    b = f.plot_area(338, 56, 514, 196, (0, 1), (-0.12, 1.12))
    b.axes(xlabel='x →', ylabel='p(y = 1)')
    for v in (0, 1):
        f.line(b.X(0), b.Y(v), b.X(1), b.Y(v), FAINT, 1, dash='2 4')
    for x, y in BIN:
        f.circle(b.X(x), b.Y(y), 3, fill=GREEN, opacity=0.55)
    lb = b.curve(sig, GREEN, width=2.6)

    # σ between the panels
    my = (a.y0 + a.y1) / 2 + 6
    f.arrow(a.x1 + 32, my, b.x0 - 22, my, MUTED, 1.4)

    # labels last
    f.label('σ', [((a.x1 + b.x0) / 2 + 5, my - 9, 'middle')], MUTED, LABEL, weight=600, mono=True)
    f.label('linear: unbounded, fits the mean', [(a.x0, 24, 'start')], BLUE, LABEL, weight=600)
    f.label('logistic: squashed into (0, 1)', [(b.x0, 24, 'start')], GREEN, LABEL, weight=600)
    f.label('ŷ = wx + b', [(a.X(0.55) + 10, a.Y(line(0.55)) + 22, 'start'),
                           (a.X(0.6) + 12, a.Y(line(0.6)) + 18, 'start')], BLUE, SMALL, weight=600, mono=True)
    f.label('p = σ(wx + b)', [(b.X(0.62) + 10, b.Y(sig(0.62)) + 16, 'start'),
                              (b.X(0.66) + 10, b.Y(sig(0.66)) + 20, 'start')], GREEN, SMALL, weight=600, mono=True)
    for v in (0, 1):
        f.label(str(v), [(b.x0 - 8, b.Y(v) + 3, 'end')], FAINT, SMALL)
    f.label('the log-odds are linear in x; the probability is not', [(280, 254, 'middle')], MUTED, SMALL)
    return f
