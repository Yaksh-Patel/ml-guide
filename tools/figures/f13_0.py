"""13 Naive Bayes: the independence assumption is false, and the argmax survives.

Top: the factorisation, one factor per word. Bottom left: why it is false
("space" and "shuttle" travel together). Bottom right: the prose's worked
numbers as log-odds bars. The honest posterior is +0.41 (P = 0.60); Naive
Bayes adds about +2.8 of the same evidence again and reports +3.21 (P = 0.96).
Both bars sit on the spam side of the 0.5 line, so the decision is the same.

History: the old figure said the errors "bias both classes the same way and
cancel". The prose gives the real mechanism: double-counting inflates the
size of the log-odds but rarely flips their sign. The figure now shows that.
"""
from figkit import Fig, BLUE, GREEN, AMBER, RED, FAINT, MUTED, INK, SURF, BORD, LABEL, SMALL, TINY

TARGET = ('13-naive-bayes', 0)
HONEST, NAIVE = 0.41, 3.21


def draw():
    f = Fig(560, 224, 'nb')

    # the factorisation
    a = f.box(80, 16, 128, 34, 'P(class | words)', mono=True)
    b = f.box(252, 12, 230, 42, 'P(class) · Π P(wᵢ | class)', 'assumes the words are independent',
              stroke=GREEN, color=GREEN, mono=True)
    f.connect(a, b)

    # left: two pairs of words
    def pill(cx, cy, s):
        w = len(s) * SMALL * 0.62 + 18
        return f.box(cx - w / 2, cy - 11, w, 22, s, size=SMALL, r=11, mono=True, weight=None)

    s1, s2 = pill(54, 108, 'space'), pill(176, 108, 'shuttle')
    f.connect(s1, s2, RED, 1.8, arrow=False, gap=3)
    t1, t2 = pill(54, 156, 'the'), pill(176, 156, 'car')

    # right: log-odds bars, zero = P(spam) 0.5
    x0, k = 320, 46.0
    X = lambda v: x0 + k * v
    r1, r2, bh = 112, 150, 12
    f.rect(X(0), r1 - bh / 2, k * HONEST, bh, BLUE, BLUE, 2, opacity=0.9)
    f.rect(X(0), r2 - bh / 2, k * HONEST, bh, BLUE, BLUE, 2, opacity=0.9)
    f.rect(X(HONEST), r2 - bh / 2, k * (NAIVE - HONEST), bh, RED, RED, 2, opacity=0.9)
    f.line(X(0), r1 - 22, X(0), r2 + 20, AMBER, 1.4, dash='4 3')

    # labels last
    f.label('dependent', [((s1.r + s2.l) / 2, 124, 'middle')], RED, SMALL, weight=600)
    f.label('≈ independent', [((t1.r + t2.l) / 2, 159, 'middle')], FAINT, SMALL)
    f.label('some words travel together', [(24, 82, 'start')], MUTED, SMALL, weight=600)
    f.label('log-odds → P(spam): same sign, wrong size', [(X(0) - 64, 82, 'start')], MUTED, SMALL, weight=600)
    f.label('honest', [(X(0) - 8, r1 + 3, 'end')], BLUE, SMALL, weight=600)
    f.label('Naive Bayes', [(X(0) - 8, r2 + 3, 'end')], RED, SMALL, weight=600)
    f.label('+0.41 → 0.60', [(X(HONEST) + 8, r1 + 3, 'start')], BLUE, SMALL, mono=True)
    f.label('+3.21 → 0.96', [(X(NAIVE) + 8, r2 + 3, 'start')], RED, SMALL, mono=True)
    f.label('+2.8 from triple-counting', [((X(HONEST) + X(NAIVE)) / 2, r2 + 22, 'middle')], RED, SMALL)
    f.label('P = 0.5', [(X(0), r2 + 34, 'middle')], AMBER, SMALL, weight=600)
    f.label('spam →', [(X(NAIVE) + 8, r1 + 3, 'start'), (X(NAIVE) + 40, r1 - 14, 'end')], FAINT, SMALL)
    f.label('Use it for the ranking, never quote its probabilities.', [(280, 214, 'middle')], AMBER, LABEL, weight=600)
    return f
