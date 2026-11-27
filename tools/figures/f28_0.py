"""28 what each loss punishes: MSE vs Huber on a residual, BCE vs focal on p(true class).

History: the old left panel rescaled Huber so it met MSE at both edges, which
hid the whole point (Huber grows linearly, MSE quadratically). Both are now on
one honest scale over r in [-3, 3]: MSE = r², Huber with δ = 1 (½r² inside
±δ, |r| − ½ outside), the same definitions that give the prose's "r = 50:
MSE 2500, Huber 49.5". Right panel (p from 0.01, y clipped at 2.4): BCE = −ln p and focal = −(1 − p)² ln p
(γ = 2, no α), so at p = 0.9 focal keeps (0.1)² = 1% of BCE, as the prose says.
Axis titles and notes now have their own rows instead of colliding.
"""
import math
from figkit import Fig, BLUE, GREEN, RED, PURPLE, FAINT, MUTED, INK, LABEL, SMALL, TINY

TARGET = ('28-loss-functions', 0)
DELTA = 1.0


def huber(r):
    a = abs(r)
    return 0.5 * r * r if a <= DELTA else DELTA * (a - 0.5 * DELTA)


def draw():
    f = Fig(560, 272, 'loss')
    TOP, BOT = 40, 186

    # left: regression losses
    L = f.plot_area(52, TOP, 250, BOT, (-3, 3), (0, 9.4))
    L.axes(ylabel='penalty')
    for s in (-1, 1):
        x = L.X(s * DELTA)
        f.line(x, L.Y(0) - 3, x, L.Y(4.2), FAINT, 1, dash='2 3')
    mse = L.curve(lambda r: r * r, RED, n=160)
    hub = L.curve(huber, GREEN, n=160)

    # right: classification losses
    R = f.plot_area(322, TOP, 520, BOT, (0, 1), (0, 2.4))
    R.axes(ylabel='loss')
    bce = R.curve(lambda p: -math.log(p), BLUE, n=200, xr=(0.01, 1))
    foc = R.curve(lambda p: -(1 - p) ** 2 * math.log(p), PURPLE, n=200, xr=(0.01, 1))
    x9 = R.X(0.9)

    # labels last
    cxL, cxR = (L.x0 + L.x1) / 2, (R.x0 + R.x1) / 2
    f.label('residual r →', [(cxL, BOT + 28, 'middle')], FAINT, SMALL)
    f.label('p (true class) →', [(cxR, BOT + 28, 'middle')], FAINT, SMALL)
    f.label('0', [(L.X(0), L.Y(0) + 13, 'middle')], FAINT, TINY, mono=True)
    f.label('0', [(R.X(0), R.Y(0) + 13, 'middle')], FAINT, TINY, mono=True)
    f.label('−δ', [(L.X(-DELTA), L.Y(0) + 13, 'middle')], FAINT, TINY, mono=True)
    f.label('δ', [(L.X(DELTA), L.Y(0) + 13, 'middle')], FAINT, TINY, mono=True)
    f.label('1', [(R.X(1), R.Y(0) + 13, 'middle')], FAINT, TINY, mono=True)
    f.label('0.9', [(x9, R.Y(0) + 13, 'middle')], FAINT, TINY, mono=True)
    f.along(mse, 'MSE', [0.86, 0.8, 0.9], fill=RED, size=LABEL, weight=600)
    f.along(hub, 'Huber (δ = 1)', [0.9, 0.85, 0.8], fill=GREEN, size=LABEL, weight=600)
    f.along(bce, 'BCE', [0.2, 0.25, 0.3], fill=BLUE, size=LABEL, weight=600)
    # focal hugs the axis on the right, so its label sits in the gap between the curves
    cands = []
    for k in range(40):
        pm = 0.3 + 0.01 * k
        ym = (R.Y(-math.log(pm)) + R.Y(-(1 - pm) ** 2 * math.log(pm))) / 2
        cands.append((R.X(pm), ym + 4, 'middle'))
    f.label('focal', cands, PURPLE, LABEL, weight=600, pad=2)

    f.label('at r = 50:  MSE 2500,  Huber 49.5', [(cxL, 236, 'middle')], MUTED, SMALL)
    f.label('focal γ = 2:  at p = 0.9 it keeps 1% of BCE', [(cxR, 236, 'middle')], MUTED, SMALL)
    f.label('Pick the loss for the failure you care about: outliers (Huber) or a drowned minority class (focal).',
            [(280, 262, 'middle')], INK, SMALL)
    return f
