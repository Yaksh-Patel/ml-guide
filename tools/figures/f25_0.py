"""25 ensembles: bagging, boosting and stacking side by side, each with the
error it is betting on.

History: the old figure said stacking "attacks BOTH" bias and variance. The
prose (and its table) says stacking attacks model-selection error: it learns
the weighting instead of picking one model. That is the label now. Bagging
and stacking share one shape (three models into a combiner) so the only
visible difference is the combiner: a plain average versus a meta-learner
trained on out-of-fold predictions. Boosting is a chain. The bottom warning
no longer sits on the meta-learner box.
"""
from figkit import Fig, BLUE, RED, PURPLE, AMBER, FAINT, MUTED, LABEL, SMALL, TINY

TARGET = ('25-ensemble-methods', 0)

MW, MH, MG = 46, 20, 5          # base-model box
MX = 96                         # left edge of the base models
CX, CW = 246, 92                # combiner box
EX = 378                        # effect text column


def fan(f, y0, combiner, sub, col):
    ms = [f.box(MX, y0 + k * (MH + MG), MW, MH, f'm{k + 1}', size=SMALL, weight=None, color=MUTED)
          for k in range(3)]
    cy = ms[1].cy
    c = f.box(CX, cy - 19, CW, 38, combiner, sub, stroke=col, color=col)
    for m in ms:
        f.arrow(m.r, m.cy, c.l, cy + (m.cy - cy) * 0.35, FAINT, 1.3)
    return ms, c


def draw():
    f = Fig(560, 268, 'ens')

    # bagging: independent models, averaged
    bag, bavg = fan(f, 14, 'average', 'equal votes', BLUE)
    # boosting: a chain, each model fitting what the last one missed
    by = 118
    chain = [f.box(MX + k * 76, by - MH / 2, MW, MH, f'm{k + 1}', size=SMALL, weight=None, color=MUTED)
             for k in range(3)]
    for a, b in zip(chain, chain[1:]):
        f.connect(a, b, AMBER, 1.4)
    # stacking: same shape as bagging, but the combiner is learned
    stk, meta = fan(f, 160, 'meta-learner', 'on out-of-fold preds', PURPLE)

    # labels last
    for (y, name, col) in ((bag[1].cy, 'bagging', BLUE), (by, 'boosting', AMBER), (stk[1].cy, 'stacking', PURPLE)):
        f.label(name, [(MX - 14, y + 4, 'end')], col, LABEL, weight=600)
    f.label('each fits the residuals of the one before', [((chain[0].l + chain[-1].r) / 2, by + 24, 'middle')],
            MUTED, TINY)
    rows = [(bag[1].cy, 'attacks variance', 'deep trees; more members never overfit', BLUE),
            (by, 'attacks bias', 'shallow trees; needs early stopping', AMBER),
            (stk[1].cy, 'attacks model-selection error', 'learns the weighting; can overfit', PURPLE)]
    for y, a, b, col in rows:
        f.label(a, [(EX, y - 1, 'start')], col, LABEL, weight=600)
        f.label(b, [(EX, y + 12, 'start')], MUTED, TINY)
    f.label('A meta-learner trained on in-fold predictions leaks: it trusts a column that is nearly y.',
            [(f.w / 2, f.h - 8, 'middle')], RED, SMALL)
    return f
