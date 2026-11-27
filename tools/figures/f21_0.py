"""21 feature engineering: target encoding computed in-fold (leaks) and
out-of-fold (honest), drawn as which folds feed the mean that encodes fold 3.

The old figure said the same thing as eight lines of repeated text ("row 1
encoding includes row 1 label", ...). Here the difference is one arrow: on
the left fold 3's own labels flow into its encoding, on the right they do
not. The smoothing formula now uses the prose's notation (m, not k) and is
written in words so it cannot clip.
"""
from figkit import Fig, GREEN, AMBER, RED, FAINT, MUTED, BORD, INK, LABEL, SMALL, TINY

TARGET = ('21-feature-engineering', 0)

FOLD_W, FOLD_H, FOLD_GAP, TOP = 66, 22, 6, 40
SELF = 2                                  # fold 3 is the one being encoded


def panel(f, px, leaky):
    col = RED if leaky else GREEN
    folds = []
    for k in range(5):
        y = TOP + k * (FOLD_H + FOLD_GAP)
        me = k == SELF
        folds.append(f.box(px + 18, y, FOLD_W, FOLD_H, f'fold {k + 1}', stroke=AMBER if me else BORD,
                           color=AMBER if me else MUTED, size=SMALL, weight=600 if me else None,
                           width=1.6 if me else 1.0))
    cy = folds[SELF].cy
    mean = f.box(px + 150, cy - 24, 98, 48, 'category mean', 'encodes fold 3', stroke=col, color=col)
    for k, b in enumerate(folds):
        if k == SELF and not leaky:
            continue
        ty = cy + (b.cy - cy) * 0.32
        if k == SELF:
            f.arrow(b.r, b.cy, mean.l, ty, RED, 2.0)
        else:
            f.arrow(b.r, b.cy, mean.l, ty, GREEN if not leaky else FAINT, 1.3)
    return folds, mean


def draw():
    f = Fig(560, 252, 'te')
    lf, lm = panel(f, 14, True)
    rf, rm = panel(f, 296, False)
    f.line(280, 14, 280, 196, BORD, 1, dash='2 4')

    # labels last
    f.label('in-fold mean (leaks)', [(lm.cx - 66, 22, 'middle')], RED, LABEL, weight=600)
    f.label('out-of-fold mean (correct)', [(rm.cx - 66, 22, 'middle')], GREEN, LABEL, weight=600)
    by = lf[-1].b + 20
    f.label('fold 3 is encoded with its own labels', [(lm.cx - 66, by, 'middle')], RED, SMALL)
    f.label('CV looks excellent; production does not', [(lm.cx - 66, by + 13, 'middle')], MUTED, SMALL)
    f.label('fold 3 never sees its own labels', [(rm.cx - 66, by, 'middle')], GREEN, SMALL)
    f.label('CV is lower, and honest', [(rm.cx - 66, by + 13, 'middle')], MUTED, SMALL)
    f.label('smoothed:  (n · category mean + m · global mean) / (n + m)  — thin categories fall back to the prior',
            [(f.w / 2, f.h - 10, 'middle')], MUTED, SMALL)
    return f
