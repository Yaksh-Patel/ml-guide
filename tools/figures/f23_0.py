"""23 regularisation: coefficient paths under L2 and L1, drawn from the
closed forms the prose gives (orthonormal features):

    ridge  w / (1 + λ)            lasso  sign(w) · max(|w| − λ, 0)

with the prose's own unpenalised weights 2.0, 0.8 and 0.4.

History: the old paths were hand-shaped curves against an unlabelled log α
axis, so nothing in them could be checked against the table above the
figure. Now λ is linear, the L1 paths are straight lines that reach zero
exactly at λ = |w| (0.4, 0.8, 2.0, marked on the axis), and the L2 paths are
the 1/(1 + λ) decay that never arrives. The panel notes no longer sit on
the λ axis title.
"""
from figkit import Fig, BLUE, PURPLE, AMBER, FAINT, MUTED, LABEL, SMALL, TINY

TARGET = ('23-regularization', 0)

W = [2.0, 0.8, 0.4]
LMAX, YMAX = 2.4, 2.15


def panel(f, x0, x1, fn, col, stop=None):
    p = f.plot_area(x0, 52, x1, 192, (0, LMAX), (0, YMAX))
    p.axes(xlabel='λ', ylabel='coefficient')
    curves = [p.curve(lambda l, w=w: fn(w, l), col, width=2.2, n=160, clip=False,
                      xr=(0, stop(w) if stop else LMAX)) for w in W]
    return p, curves


def draw():
    f = Fig(560, 244, 'reg')
    pl, cl = panel(f, 44, 246, lambda w, l: w / (1 + l), BLUE)
    pr, cr = panel(f, 330, 532, lambda w, l: max(w - l, 0.0), PURPLE, stop=lambda w: w)

    # L1: each weight lands on zero at λ = |w|
    for w in W:
        x, y = pr.X(w), pr.Y(0)
        f.circle(x, y, 3.6, fill=AMBER)

    # labels last: the unpenalised weight doubles as the y tick
    for p, col in ((pl, BLUE), (pr, PURPLE)):
        for w in W:
            f.label(f'{w:.1f}', [(p.x0 - 6, p.Y(w) + 3, 'end')], col, SMALL, weight=600, pad=1)
    for w in W:
        f.label(f'{w:.1f}', [(pr.X(w), pr.Y(0) + 15, 'middle')], AMBER, TINY, pad=1)

    f.label('L2 · ridge:  w / (1 + λ)', [((pl.x0 + pl.x1) / 2, 18, 'middle')], BLUE, LABEL, weight=600)
    f.label('L1 · lasso:  max(|w| − λ, 0)', [((pr.x0 + pr.x1) / 2, 18, 'middle')], PURPLE, LABEL, weight=600)
    f.label('shrinks, never reaches zero', [(pl.x1, pl.Y(1.75), 'end'), (pl.x1, pl.Y(1.5), 'end')], MUTED, SMALL)
    f.label('exactly zero once λ ≥ |w|', [(pr.x1, pr.Y(1.75), 'end'), (pr.x1, pr.Y(1.5), 'end')], MUTED, SMALL)
    f.label('Subtraction has a floor; multiplication does not.', [(f.w / 2, f.h - 8, 'middle')], MUTED, SMALL)
    return f
