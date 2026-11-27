"""03 central limit theorem: the sampling distribution of the mean narrows as √n.

A skewed population (inset, top left) still gives normal sample means. Both
curves are true densities on one x scale (units of σ/√30): n = 120 is four
times the data, so its SE is half, its peak twice as tall, and its 95% range
(the bars under the axis) exactly half as wide. That is the prose's "halving an
interval takes four times the data", made visible.

History: the old figure compared n = 30 with n = 300 but drew them at the
same height and only ~2.5× apart in width (it should be √10 ≈ 3.2×), so the
picture contradicted its own SE = σ/√n line. n = 120 (4×) lets the figure show
the takeaway directly.
"""
import math
from figkit import Fig, BLUE, GREEN, AMBER, FAINT, MUTED, LABEL, SMALL

TARGET = ('03-statistics', 0)


def normal(sd):
    return lambda x: math.exp(-0.5 * (x / sd) ** 2) / (sd * math.sqrt(2 * math.pi))


def draw():
    f = Fig(560, 290, 'clt')
    p = f.plot_area(56, 44, 500, 206, (-3.4, 3.4), (0, 0.86))
    p.axes(xlabel='sample mean →', ylabel='density')

    # μ
    f.line(p.X(0), p.Y(0), p.X(0), p.Y(0.84), FAINT, 1, dash='3 4')

    b = p.curve(normal(1.0), BLUE, n=160)
    g = p.curve(normal(0.5), GREEN, width=2.6, n=160)

    # 95% ranges of the sample mean, under the axis
    for sd, col, yy in ((1.0, BLUE, p.Y(0) + 26), (0.5, GREEN, p.Y(0) + 40)):
        a, c = p.X(-1.96 * sd), p.X(1.96 * sd)
        f.line(a, yy, c, yy, col, 2.4)
        f.line(a, yy - 4, a, yy + 4, col, 1.6)
        f.line(c, yy - 4, c, yy + 4, col, 1.6)

    # inset: a skewed population (gamma k=2 shape), no axes of its own
    ix, iy, iw, ih = 84, 50, 100, 38
    pop = [(ix + iw * t / 40, iy + ih - ih * (t / 40 * 6) * math.exp(-(t / 40 * 6) + 1) / 1.0)
           for t in range(41)]
    f.path(pop, MUTED, 1.6, opacity=0.8)
    f.line(ix, iy + ih, ix + iw, iy + ih, FAINT, 1)

    # labels last
    f.label('μ', [(p.X(0), p.Y(0.84) - 6, 'middle')], MUTED, LABEL, weight=600)
    f.along(b, 'n = 30', [0.62, 0.66, 0.58], fill=BLUE, size=LABEL, weight=600)
    f.along(g, 'n = 120  (4× the data)', [0.56, 0.6, 0.54], fill=GREEN, size=LABEL, weight=600)
    f.label('95% of sample means', [(p.X(-1.96) - 8, p.Y(0) + 29, 'end')], MUTED, SMALL)
    f.label('half as wide', [(p.X(0.98) + 8, p.Y(0) + 43, 'start')], GREEN, SMALL)
    f.label('population: skewed', [(ix, iy + ih + 14, 'start')], MUTED, SMALL)
    f.label('SE = σ/√n  →  four times the data halves the interval',
            [((p.x0 + p.x1) / 2, 282, 'middle')], AMBER, SMALL, mono=True)
    return f
