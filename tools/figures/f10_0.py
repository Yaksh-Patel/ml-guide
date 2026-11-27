"""10 reliability curve, before and after isotonic calibration.

Left: an overconfident model, below the diagonal (the prose's reading rule),
binned at 0.1…0.9; the curve is p^2.14 so that "says 0.80, delivers 0.62"
is exactly what the amber read-off shows. Right: the same model after
isotonic regression, on the diagonal to within bin noise.

History: the old left curve passed 0.655 at 0.8 while its label said 0.62;
the curve now matches the label.
"""
import math
from figkit import Fig, RED, GREEN, AMBER, FAINT, MUTED, BG, LABEL, SMALL

TARGET = ('10-calibration-explainability', 0)
K = math.log(0.62) / math.log(0.8)          # 0.8 ** K == 0.62
BINS = [0.1 * i for i in range(1, 10)]
WIGGLE = [0.02, -0.015, 0.012, -0.02, 0.015, -0.012, 0.01, 0.0, -0.01]   # after: bin noise


def before(p):
    return p ** K


def after(p):
    """the binned reliability after isotonic: through the bin dots, ends pinned."""
    xs = [0] + BINS + [1]
    ys = [0] + [b + w for b, w in zip(BINS, WIGGLE)] + [1]
    for (a, u), (b, v) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
        if p <= b:
            return u + (v - u) * (p - a) / (b - a)
    return 1.0


def panel(f, x0, title, col, fn, dots, readoff, note):
    s = 168
    p = f.plot_area(x0, 52, x0 + s, 52 + s, (0, 1), (0, 1))
    p.axes(ylabel='observed')
    f.path([(p.X(0), p.Y(0)), (p.X(1), p.Y(1))], FAINT, 1, dash='3 4')
    c = p.curve(fn, col, width=2.4, n=200)
    # amber read-off at 0.8
    xr, yr = p.X(0.8), p.Y(readoff)
    f.line(xr, p.Y(0), xr, yr + 6, AMBER, 1.2, dash='3 3')
    f.line(p.X(0), yr, xr - 6, yr, AMBER, 1.2, dash='3 3')
    for b, v in dots:
        f.circle(p.X(b), p.Y(v), 3.2, fill=col, stroke=BG, width=1)
    f.circle(xr, yr, 4.6, fill=AMBER, stroke=BG, width=1.2)
    return p, c, (xr, yr), (title, col, note)


def draw():
    f = Fig(560, 286, 'rel')
    L = panel(f, 56, 'before: overconfident', RED, before,
              [(b, before(b)) for b in BINS], 0.62, 'says 0.80, delivers 0.62')
    R = panel(f, 334, 'after isotonic', GREEN, after,
              [(b, b + w) for b, w in zip(BINS, WIGGLE)], 0.8, '0.80 now means 80%')

    # labels last
    for p, c, (xr, yr), (title, col, note) in (L, R):
        f.label(title, [((p.x0 + p.x1) / 2 + 6, 22, 'middle')], col, LABEL, weight=600)
        f.label('predicted →', [(p.x1 + 12, p.y1 + 18, 'end')], FAINT, SMALL)
        f.label(note, [(xr - 10, yr - 12, 'end'), (xr + 8, yr + 17, 'start'), (xr - 8, yr + 18, 'end'),
                       (xr + 10, yr - 12, 'start')], col, SMALL, weight=600)
    p = L[0]       # the diagonal is hidden under the curve on the right; name it once, on the left
    f.label('perfect', [(p.X(0.36), p.Y(0.36) - 10, 'end'), (p.X(0.3), p.Y(0.3) - 10, 'end')], FAINT, SMALL)
    f.label('calibration changes the numbers, not the order: AUC barely moves, Brier improves',
            [(280, 278, 'middle')], MUTED, SMALL)
    return f
