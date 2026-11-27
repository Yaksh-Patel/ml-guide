"""08 precision and recall against the decision threshold: one model, one
ranking, a different trade at every cut.

Curves come from a binormal score model (positives and negatives two unit
normals apart, 30% positives), so their shapes are real: recall falls from 1
to 0; precision climbs from the base rate toward 1. The amber line is a chosen
threshold, deliberately not at 0.5, with its two read-offs marked.
"""
import math
from figkit import Fig, BLUE, GREEN, AMBER, FAINT, MUTED, LABEL, SMALL

TARGET = ('08-eval-metrics', 0)
PI, SEP = 0.30, 2.0
TAU = 0.36


def _sf(z):                     # P(Z > z)
    return 0.5 * math.erfc(z / math.sqrt(2))


def _cut(tau):                  # threshold on the [0, 1] axis -> latent score
    return (tau - 0.5) * 6


def recall(tau):
    return _sf(_cut(tau) - SEP / 2)


def precision(tau):
    tp = PI * _sf(_cut(tau) - SEP / 2)
    fp = (1 - PI) * _sf(_cut(tau) + SEP / 2)
    return tp / (tp + fp)


def draw():
    f = Fig(560, 266, 'prt')
    p = f.plot_area(56, 44, 500, 204, (0, 1), (0, 1.04))
    p.axes()
    f.line(p.X(0) - 4, p.Y(1), p.X(0), p.Y(1), FAINT, 1)

    for v in (0, 0.5, 1):
        f.line(p.X(v), p.Y(0), p.X(v), p.Y(0) + 4, FAINT, 1)

    r = p.curve(recall, BLUE, n=160)
    pr = p.curve(precision, GREEN, n=160)

    x = p.X(TAU)
    f.line(x, p.Y(0), x, p.Y(1.04) - 4, AMBER, 1.4, dash='4 4')
    for fn, col in ((recall, BLUE), (precision, GREEN)):
        f.circle(x, p.Y(fn(TAU)), 4.5, fill=col, stroke='#0b0d12', width=1.2)

    # labels last
    f.label('your threshold', [(x, p.Y(1.04) - 10, 'middle')], AMBER, SMALL, weight=600)
    f.along(pr, 'precision', [0.86, 0.9, 0.8], fill=GREEN, size=LABEL, weight=600)
    f.label('recall', [(p.X(0.08), p.Y(recall(0.08)) + 18, 'start'), (p.X(0.14), p.Y(recall(0.14)) + 18, 'start')],
            BLUE, LABEL, weight=600)
    f.label('1', [(p.X(0) - 8, p.Y(1) + 3, 'end')], FAINT, SMALL)
    for v in (0, 0.5, 1):
        f.label(f'{v:g}', [(p.X(v), p.Y(0) + 16, 'middle')], FAINT, SMALL)
    f.label('← catch everything', [(p.X(0), p.Y(0) + 32, 'start')], BLUE, SMALL)
    f.label('only fire when sure →', [(p.X(1), p.Y(0) + 32, 'end')], GREEN, SMALL)
    f.label('decision threshold', [(p.X(0.5), p.Y(0) + 32, 'middle')], FAINT, SMALL)
    f.label('where you put this line is a business decision, not 0.5 by default',
            [(p.X(0.5), 258, 'middle')], MUTED, SMALL)
    return f
