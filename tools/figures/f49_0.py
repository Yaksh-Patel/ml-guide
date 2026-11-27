"""49 responsible AI: the fairness impossibility result, drawn with the
topic's own audit numbers.

One group-blind model over two groups with base rates 30% (A) and 15% (B),
the table in the prose above the code card: selection rate 0.398 / 0.317,
TPR 0.875 / 0.886, FPR 0.206 / 0.219, PPV 0.631 / 0.411. Each metric is a
row with both groups on one 0–1 scale, so "equal opportunity looks
excellent, predictive parity is severe" is visible as two dots together and
two dots far apart.

History: the old figure was a grid of "equalise X → different Y" boxes; its
third row said equalising predictive parity changes TPR "again", whereas the
identity the prose gives (FPR = p/(1−p) · (1−PPV)/PPV · TPR) says that with
PPV and TPR fixed, unequal base rates force unequal FPR. The drawing now
shows measured numbers instead of slogans.
"""
from figkit import (Fig, BLUE, PURPLE, GREEN, RED, INK, MUTED, FAINT, BG,
                    LABEL, SMALL, TINY)

TARGET = ('49-responsible-ai', 0)

ROWS = [   # (metric, criterion, A, B, gap colour or None)
    ('base rate', 'where the groups differ', 0.30, 0.15, None),
    ('selection rate', 'demographic parity', 0.398, 0.317, MUTED),
    ('TPR', 'equal opportunity', 0.875, 0.886, GREEN),
    ('FPR', 'equalised odds, with TPR', 0.206, 0.219, GREEN),
    ('PPV', 'predictive parity', 0.631, 0.411, RED),
]
PX0, PX1 = 178, 448
Y0, PITCH = 40, 38


def X(v):
    return PX0 + (PX1 - PX0) * v


def draw():
    f = Fig(560, 270, 'fair')
    ys = [Y0 + i * PITCH + (8 if i else 0) for i in range(len(ROWS))]
    top, bot = ys[0] - 16, ys[-1] + 16

    # scale
    for v in (0, 0.25, 0.5, 0.75, 1):
        f.line(X(v), top, X(v), bot, FAINT, 1, dash='2 4', opacity=0.6)
        f.text(X(v), bot + 14, f'{v:g}', FAINT, SMALL, 'middle', mono=True)
    f.line(PX0 - 8, (ys[0] + ys[1]) / 2, PX1 + 8, (ys[0] + ys[1]) / 2, FAINT, 1, opacity=0.6)

    for (name, crit, a, b, gc), y in zip(ROWS, ys):
        xa, xb = X(a), X(b)
        lo, hi = min(xa, xb) + 5, max(xa, xb) - 5
        if hi > lo:
            f.line(lo, y, hi, y, gc or FAINT, 3 if gc else 1.6)
        f.circle(xa, y, 5.5, fill=BLUE, stroke=BG, width=1.2)
        f.circle(xb, y, 5, fill='none', stroke=PURPLE, width=2.2)
        f.text(PX0 - 18, y - 1, name, INK, SMALL, 'end', weight=600)
        f.text(PX0 - 18, y + 10, crit, FAINT, TINY, 'end')
        if gc:
            f.text(PX1 + 22, y + 3.2, f'gap {abs(a - b):.3f}', gc, SMALL, weight=600, mono=True)

    # direct labels for the two groups, on the base-rate row
    y = ys[0]
    f.label('B  15%', [(X(0.15) - 10, y + 3.4, 'end'), (X(0.15), y - 11, 'middle')], PURPLE, SMALL, weight=600)
    f.label('A  30%', [(X(0.30) + 10, y + 3.4, 'start'), (X(0.30), y - 11, 'middle')], BLUE, SMALL, weight=600)

    f.text(280, 262, 'Equal error rates, yet a 22-point PPV gap: unequal base rates force it.',
           MUTED, LABEL, 'middle')
    return f
