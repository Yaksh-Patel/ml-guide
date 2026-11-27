"""31 weight init: activation variance through ten ReLU layers, on a log scale.

History: the old figure plotted "activation std" on a linear axis, where the
exploding line hit the ceiling after one layer and the vanishing one hugged
the floor, so neither showed the per-layer factor the prose is about. On a
log axis a constant per-layer factor is a straight line:
  * He, Var(w) = 2/n_in: the ReLU halving is cancelled, variance stays 1.
  * Xavier, Var(w) = 1/n_in, with ReLU: ×½ per layer, 1/1024 ≈ 0.00098 at
    layer 10 (the prose's table: 0.5, 0.031, 0.00098 at 1, 5, 10).
  * Too large (illustrative, e.g. Var(w) = 4/n_in with ReLU): ×2 per layer,
    1024 at layer 10, the mirror image.
Labels now sit beside their lines, not on them, and the formula line that
collided with "layer depth" is gone (the prose and the next figure carry it).
"""
from figkit import Fig, GREEN, RED, FAINT, MUTED, INK, LABEL, SMALL, TINY

TARGET = ('31-weight-init', 0)
DEPTH = 10


def draw():
    f = Fig(560, 256, 'wi')
    p = f.plot_area(70, 38, 462, 200, (0, DEPTH), (-12.5, 11))     # y = log2(variance)
    p.axes(ylabel='activation variance (log scale)')

    for e in (10, -10):          # faint guides at 1024 and 1/1024
        f.line(p.x0, p.Y(e), p.x1, p.Y(e), FAINT, 0.8, dash='2 4', opacity=0.7)

    series = [(1, RED), (0, GREEN), (-1, RED)]    # log2 factor per layer
    lines = {}
    for k, col in series:
        pts = [(p.X(l), p.Y(k * l)) for l in range(DEPTH + 1)]
        f.path(pts, col, 2.4)
        for (x, y) in pts[1:]:
            f.circle(x, y, 2.6, fill=col)
        lines[k] = pts
    f.circle(p.X(0), p.Y(0), 3.4, fill=INK)

    # labels last
    for e, s in ((10, '1024'), (0, '1'), (-10, '1/1024')):
        f.label(s, [(p.x0 - 6, p.Y(e) + 3, 'end')], FAINT, TINY, mono=True, pad=1)
    for l in (0, 5, 10):
        f.label(str(l), [(p.X(l), p.y1 + 13, 'middle')], FAINT, TINY, mono=True, pad=1)
    f.label('layer →', [((p.x0 + p.x1) / 2, p.y1 + 26, 'middle')], FAINT, SMALL)

    f.label('He, Var(w) = 2/n_in: variance held at 1',
            [(p.X(5.4), p.Y(0) - 9, 'start'), (p.X(5.4), p.Y(0) + 16, 'start')], GREEN, LABEL, weight=600)
    up, dn = lines[1], lines[-1]
    f.label('init too large: ×2 per layer',
            [(p.X(4.6), p.Y(4.6) - 8, 'end'), (p.X(4.2), p.Y(4.2) - 8, 'end')], RED, LABEL, weight=600)
    f.label('Xavier with ReLU: ×½ per layer',
            [(p.X(4.6), p.Y(-4.6) + 12, 'end'), (p.X(4.2), p.Y(-4.2) + 12, 'end')], RED, LABEL, weight=600)
    f.label('vanishing', [(dn[-1][0] + 9, dn[-1][1] + 4, 'start')], RED, SMALL)
    f.label('exploding → NaN', [(up[-1][0] + 9, up[-1][1] + 4, 'start')], RED, SMALL)

    f.label('Per-layer factors multiply: a ×½ slip in scale is 1/1024 after ten layers.',
            [(280, 248, 'middle')], INK, SMALL)
    return f
