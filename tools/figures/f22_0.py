"""22 imbalanced data: four responses, placed at the pipeline stage each one
changes.

History: the old figure put focal loss on a "model" stage and described it
as down-weighting "the easy majority". Focal loss is a loss function, and the
prose is explicit that it down-weights easy examples of either class (by
difficulty, not by class). So the pipeline is three stages (data, loss,
decision) and the loss stage carries two responses: class_weight (by class)
and focal loss (by difficulty). The dotted leaders that ran through labels
are now short arrows from each response up to the stage it acts on.
"""
from figkit import Fig, GREEN, AMBER, RED, PURPLE, FAINT, MUTED, INK, LABEL, SMALL, TINY

TARGET = ('22-imbalanced', 0)

Y0, BH = 18, 40


def draw():
    f = Fig(560, 172, 'imb')
    data = f.box(14, Y0, 100, BH, 'training data', 'rows the model sees', size=LABEL)
    loss = f.box(150, Y0, 260, BH, 'training loss', 'what each row costs', size=LABEL)
    thr = f.box(450, Y0, 96, BH, 'threshold', 'flag if p > t', size=LABEL)
    f.connect(data, loss)
    f.connect(loss, thr)

    resp = [  # (x, name, note 1, note 2, colour)
        (data.cx, 'resample / SMOTE', 'synthesises minority rows;', 'only inside the CV fold', RED),
        (215, 'class_weight', 'reweights rows by class;', 'no data invented', AMBER),
        (345, 'focal loss', 'down-weights easy rows', 'of either class', PURPLE),
        (thr.cx, 'move the cut', 'changes only the decision;', 'p stays calibrated', GREEN),
    ]
    ny = Y0 + BH + 38
    for x, name, a, b, col in resp:
        f.arrow(x, ny - 12, x, Y0 + BH, col, 1.3)
        f.text(x, ny, name, col, LABEL, 'middle', weight=600)
        f.text(x, ny + 14, a, MUTED, TINY, 'middle')
        f.text(x, ny + 26, b, MUTED, TINY, 'middle')

    f.label('Try the last one first: it costs nothing, invents no data, and is usually competitive.',
            [(f.w / 2, f.h - 10, 'middle')], GREEN, SMALL)
    return f
