"""36 distillation: two targets for one student. The teacher's softened
output (τ = 4) and the hard label y sit on the top row; the student's
output below is pulled toward both: KL to the teacher, CE to the label.

The bars carry no numbers on purpose: the shapes are the old figure's
(the teacher spreads mass over the related classes), and the point is that
the soft target has structure a one-hot label does not.

History: the old figure named the teacher "BERT-large, 340M". DistilBERT
was distilled from BERT-base (110M), which is what the prose says further
down ("BERT-Base (110M params) to DistilBERT (66M params)").

Motion (one 6s clock): a pulse runs down each loss link, then the student's
bars move from an untrained, near-flat guess to the teacher's shape; hold,
then reset. Reduced motion shows the 4.6s frame: the trained student.
"""
from figkit import (Fig, Anim, BLUE, GREEN, AMBER, PURPLE, INK, MUTED, FAINT, BG, GAP,
                    LABEL, SMALL, TINY)

TARGET = ('36-transfer-distillation', 1)

CLASSES = ('cat', 'dog', 'fox', 'wolf')
TEACHER = (0.15, 0.25, 0.43, 0.21)     # the old figure's bar heights
HARD = (0, 0, 1, 0)
UNTRAINED = (0.27, 0.22, 0.25, 0.26)
BAR_W, STEP, HMAX = 18, 26, 54


def axis(f, x0, base, n=4):
    f.line(x0 - 5, base, x0 + (n - 1) * STEP + BAR_W + 5, base, FAINT, 1)
    for i, c in enumerate(CLASSES):
        f.text(x0 + i * STEP + BAR_W / 2, base + 11, c, MUTED, TINY, 'middle')


def draw():
    f = Fig(560, 276, 'kd')
    A = Anim(6.0)
    f.still = 4.6

    top, bot = 92, 222                      # bar baselines of the two rows
    xin = f.box(16, 132, 46, 34, 'input x', stroke=FAINT, color=INK, size=SMALL)
    tch = f.box(100, top - 52, 112, 50, 'Teacher', 'BERT-base · 110M', stroke=PURPLE, color=PURPLE, size=LABEL)
    stu = f.box(100, bot - 52, 112, 50, 'Student', 'DistilBERT · 66M', stroke=BLUE, color=BLUE, size=LABEL)
    f.connect(xin, tch, FAINT, 1.4)
    f.connect(xin, stu, FAINT, 1.4)

    tx, gx, sx = 262, 432, 347              # left edges of the three bar groups
    gw = 3 * STEP + BAR_W
    for x0, base in ((tx, top), (gx, top), (sx, bot)):
        axis(f, x0, base)
    f.arrow(tch.r, tch.cy, tx - 10, tch.cy, PURPLE, 1.4)
    f.arrow(stu.r, stu.cy, sx - 10, stu.cy, BLUE, 1.4)

    for i, v in enumerate(TEACHER):
        h = v * HMAX
        f.rect(tx + i * STEP, top - h, BAR_W, h, fill=PURPLE, stroke=PURPLE, r=2, width=1, opacity=0.85)
    for i, v in enumerate(HARD):          # one-hot: a full bar and three empty slots
        h = max(2, v * HMAX * 0.6)
        f.rect(gx + i * STEP, top - h, BAR_W, h, fill=GREEN, stroke=GREEN, r=1, width=1, opacity=0.85 if v else 0.5)
    # the student's bars move from an untrained guess to the teacher's shape
    for i, (u, t) in enumerate(zip(UNTRAINED, TEACHER)):
        x = sx + i * STEP
        hu, ht = u * HMAX, t * HMAX
        hv = [(0, hu), (1.6, hu), (3.6, ht), (5.4, ht), (6, hu)]
        f.raw(f'<rect x="{x:.1f}" y="{bot - ht:.1f}" width="{BAR_W}" height="{ht:.1f}" rx="2" fill="{BLUE}" '
              f'stroke="{BLUE}" stroke-width="1" opacity=".85">'
              f'{A.attr("height", [(s, f"{v:.1f}") for s, v in hv], spline=True)}'
              f'{A.attr("y", [(s, f"{bot - v:.1f}") for s, v in hv], spline=True)}</rect>',
              [(x, bot - ht), (x + BAR_W, bot - ht)])

    # the two loss links: teacher → student (KL), label → student (CE)
    kl0, kl1 = (tx + gw / 2 + 14, top + 20), (sx + gw / 2 - 26, bot - HMAX - 8)
    ce0, ce1 = (gx + gw / 2 - 14, top + 20), (sx + gw / 2 + 26, bot - HMAX - 8)
    f.line(*kl0, *kl1, PURPLE, 1.6, arrow=True, dash='4 3', gap=0)
    f.line(*ce0, *ce1, GREEN, 1.6, arrow=True, dash='4 3', gap=0)
    for (p, q), col in (((kl0, kl1), PURPLE), ((ce0, ce1), GREEN)):
        d = f'M{p[0]:.1f},{p[1]:.1f} L{q[0]:.1f},{q[1]:.1f}'
        f.raw(f'<circle r="4" fill="{col}" stroke="{BG}" stroke-width="1.2">'
              f'{A.motion(d, [(0, 0), (0.3, 0), (1.5, 1), (6, 1)])}'
              f'{A.attr("opacity", [(0, 0), (0.3, 0), (0.4, 1), (1.4, 1), (1.7, 0), (6, 0)])}</circle>')

    f.label('teacher, softened (τ = 4)', [(tx + gw / 2, top - HMAX - 8, 'middle')], PURPLE, SMALL, weight=600)
    f.label('hard label: fox', [(gx + gw / 2, top - HMAX - 8, 'middle')], GREEN, SMALL, weight=600)
    f.label('student', [(sx + gw + 12, bot - 6, 'start')], BLUE, SMALL, weight=600)
    mid = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    m = mid(kl0, kl1)
    f.label('KL', [(m[0] - 10, m[1] + 3, 'end'), (m[0] - 14, m[1] + 3, 'end')], PURPLE, SMALL, weight=600)
    m = mid(ce0, ce1)
    f.label('CE', [(m[0] + 10, m[1] + 3, 'start'), (m[0] + 14, m[1] + 3, 'start')], GREEN, SMALL, weight=600)
    f.label('L = α·CE(label, student) + (1 − α)·τ²·KL(teacher ‖ student)', [(16, 264, 'start')], AMBER, SMALL, mono=True)
    return f
