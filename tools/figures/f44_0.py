"""44 time series: forward-chaining validation, and the rolling-window leak.

History: the old figure, under this caption, drew a single train/validate
cut over a trend line and put the leak in a sentence; there were no folds and
no window. Now the top half is forward-chaining as the prose defines it
(train on [0, t], validate on (t, t+h], step forward, repeat), and the bottom
half draws the leak the code card warns about: y.rolling(28) at day t spans
t−27…t, so the feature contains the value being predicted; y.shift(1)
.rolling(28) spans t−28…t−1. The decomposition line and the seasonal-naive
note were dropped: the prose before the figure covers the baseline.
"""
from figkit import Fig, BLUE, AMBER, GREEN, RED, INK, MUTED, FAINT, LABEL, SMALL

TARGET = ('44-time-series', 0)

# folds
FX0, FX1 = 100, 520
CUTS, H = [0.40, 0.55, 0.70, 0.85], 0.15
FY, FH, FP = 40, 16, 24
# rolling windows: days −30 … 0, day 0 = t
SX0, SX1, D0 = 214, 494, -30


def fx(v):
    return FX0 + (FX1 - FX0) * v


def dx(d):           # centre of day d
    cw = (SX1 - SX0) / (1 - D0)
    return SX0 + cw * (d - D0 + 0.5)


def bar(f, x0, x1, y, h, color, op=.30):
    f.raw(f'<rect x="{x0:.1f}" y="{y:.1f}" width="{x1 - x0:.1f}" height="{h}" rx="3" fill="{color}" '
          f'fill-opacity="{op}" stroke="{color}" stroke-width="1.2"/>',
          pts=[(x0, y), (x1, y), (x1, y + h), (x0, y + h), (x0, y)])


def draw():
    f = Fig(560, 298, 'fc')

    # ---- forward-chaining ------------------------------------------------------
    f.text(20, 20, 'forward-chaining', INK, LABEL, weight=600)
    for k, c in enumerate(CUTS):
        y = FY + k * FP
        bar(f, fx(0), fx(c) - 1.5, y, FH, BLUE)
        bar(f, fx(c) + 1.5, fx(c + H), y, FH, AMBER)
        f.text(FX0 - 10, y + FH / 2 + 3.2, f'fold {k + 1}', FAINT, SMALL, 'end')
    ay = FY + 4 * FP + 2
    f.arrow(FX0, ay, FX1 + 14, ay, FAINT, 1.2, gap=0)
    f.text(FX1 + 14, ay + 15, 'time →', FAINT, SMALL, 'end')
    y4 = FY + 3 * FP
    f.text(fx(CUTS[3]) / 2 + FX0 / 2, y4 + FH / 2 + 3.4, 'train: only the past', BLUE, SMALL, 'middle', weight=600, halo=False)
    f.text(fx(CUTS[0] + H) + 10, FY + FH / 2 + 3.4, 'validate: the next slice', AMBER, SMALL, weight=600)

    # ---- the rolling-window leak ---------------------------------------------
    by = 184
    f.text(20, by - 10, 'the rolling-window leak', INK, LABEL, weight=600)
    cw = (SX1 - SX0) / (1 - D0)
    ra, rb, rh = by + 6, by + 32, 15
    # day t, the value being predicted
    f.rect(dx(0) - cw / 2 - 1, ra - 5, cw + 2, rb + rh - ra + 10, fill='none', stroke=AMBER, r=3, width=1.4)
    bar(f, dx(-27) - cw / 2 + 1, dx(0) + cw / 2 - 1, ra, rh, RED, .32)
    bar(f, dx(-28) - cw / 2 + 1, dx(-1) + cw / 2 - 1, rb, rh, GREEN, .28)
    f.text(SX0 - 12, ra + rh / 2 + 3.2, 'y.rolling(28)', RED, SMALL, 'end', mono=True)
    f.text(SX0 - 12, rb + rh / 2 + 3.2, 'y.shift(1).rolling(28)', GREEN, SMALL, 'end', mono=True)
    f.text(dx(0) + cw / 2 + 10, ra + rh / 2 + 3.4, 'sees t: leak', RED, SMALL, weight=600)
    f.text(dx(0) + cw / 2 + 10, rb + rh / 2 + 3.4, 'past only', GREEN, SMALL, weight=600)

    # day ruler
    ry = rb + rh + 12
    f.line(SX0, ry, SX1, ry, FAINT, 1)
    for d in range(D0, 1):
        tall = d in (0, -28)
        f.line(dx(d), ry, dx(d), ry + (6 if tall else 3), FAINT, 1)
    f.text(dx(-28), ry + 17, 't−28', FAINT, SMALL, 'middle', mono=True)
    f.text(dx(0), ry + 17, 't', AMBER, SMALL, 'middle', mono=True, weight=600)
    f.text(dx(0) - 12, ry + 17, 'day t, the value being predicted', AMBER, SMALL, 'end')

    f.text(280, 290, 'Shift before you roll, or the CV score is beautiful and fake.', MUTED, LABEL, 'middle')
    return f
