"""05 ML paradigms: four rows, read across — what arrives with the data,
what the model learns from it, and where the training signal comes from.

The old figure had the same four rows at small size, a grey header sentence
and a grey footnote. The third column (the signal) is new: it is the
distinction the prose draws — a human label, nothing, the data itself, or a
reward that may arrive long after the action.
"""
from figkit import Fig, GREEN, BLUE, PURPLE, AMBER, FAINT, MUTED, INK, BORD, LABEL, SMALL

TARGET = ('05-ml-paradigms', 0)

ROWS = [('supervised', 'X, y', 'f(X) → y', 'a human label', GREEN),
        ('unsupervised', 'X', 'structure in X', 'none', BLUE),
        ('self-supervised', 'X, part hidden', 'predict the hidden part', 'the data itself', PURPLE),
        ('reinforcement', 'state, reward', 'a policy: act for reward', 'reward, often late', AMBER)]


def draw():
    f = Fig(560, 220, 'par')
    NX, DX, DW, TX, TW, SX = 110, 122, 104, 256, 150, 424
    Y0, DY, H = 32, 42, 28
    for i, (name, data, task, sig, col) in enumerate(ROWS):
        y = Y0 + i * DY
        d = f.box(DX, y, DW, H, data, stroke=col, color=INK, size=LABEL, weight=600)
        t = f.box(TX, y, TW, H, task, stroke=BORD, color=INK, size=LABEL, weight=None)
        f.connect(d, t)
        f.text(NX, y + H / 2 + 3.5, name, col, LABEL, 'end', weight=600)
        f.text(SX + 12, y + H / 2 + 3.5, sig, col if i == 0 else MUTED, LABEL, weight=600 if i == 0 else None)

    # column heads
    for x, s, a in ((DX + DW / 2, 'arrives with the data', 'middle'), (TX + TW / 2, 'the model learns', 'middle'),
                    (SX + 12, 'signal comes from', 'start')):
        f.text(x, Y0 - 12, s, FAINT, SMALL, a)

    f.label('Only the first row needs a person to have labelled anything.',
            [(f.w / 2, Y0 + 4 * DY + 12, 'middle')], MUTED, SMALL)
    return f
