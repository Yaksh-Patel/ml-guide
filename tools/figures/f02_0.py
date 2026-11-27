"""02 probability: the base-rate trap as a frequency tree.

10,000 people, 1% prevalence, a test that is 99% sensitive and 99% specific.
The tree splits the population by disease, then by test result; the two
positive leaves (99 true, 99 false) flow into one box of 198 positive tests,
of which half are sick. The old figure laid the same four counts out as two
rows of boxes with a header sentence and a footnote in tiny grey; now the
branch percentages sit on the edges and the only sentence is the answer.
"""
from figkit import Fig, GREEN, RED, AMBER, BLUE, FAINT, MUTED, INK, LABEL, SMALL, TINY

TARGET = ('02-probability', 0)


def draw():
    f = Fig(560, 234, 'brt')
    BW, BH = 92, 38
    # columns: population → disease → test result → the positives
    X0, X1, X2, X3 = 14, 136, 282, 438
    root = f.box(X0, 112 - BH / 2, 82, BH, '10,000', 'people', stroke=BLUE, color=BLUE, size=LABEL)
    sick = f.box(X1, 60 - BH / 2, BW, BH, '100 sick', None, stroke=MUTED, color=INK, size=LABEL)
    well = f.box(X1, 164 - BH / 2, BW, BH, '9,900 healthy', None, stroke=MUTED, color=INK, size=LABEL)
    leaves = [(24, '99 test +', 'true positive', GREEN, INK),
              (80, '1 test −', 'false negative', FAINT, MUTED),
              (144, '99 test +', 'false positive', RED, INK),
              (200, '9,801 test −', 'true negative', FAINT, MUTED)]
    L = [f.box(X2, y - BH / 2, BW + 6, BH, a, b, stroke=c, color=(c if c != FAINT else t), size=LABEL)
         for (y, a, b, c, t) in leaves]
    tp, fn, fp, tn = L
    pos = f.box(X3 - 10, 84 - 24, 124, 48, '198 test +', '99 / 198 are sick', stroke=AMBER, color=AMBER, size=LABEL)

    f.connect(root, sick)
    f.connect(root, well)
    f.connect(sick, tp)
    f.connect(sick, fn)
    f.connect(well, fp)
    f.connect(well, tn)
    f.connect(tp, pos, GREEN, 1.6)
    f.connect(fp, pos, RED, 1.6)

    # branch rates, on the outer side of each edge (above the upper branch, below the lower)
    for a, b, s, up in ((root, sick, '1%', True), (root, well, '99%', False),
                        (sick, tp, '99%', True), (sick, fn, '1%', False),
                        (well, fp, '1%', True), (well, tn, '99%', False)):
        p, q = a.edge_toward(b.cx, b.cy), b.edge_toward(a.cx, a.cy)
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        dx, dy = q[0] - p[0], q[1] - p[1]
        n = (dx * dx + dy * dy) ** 0.5
        nx, ny = (dy / n, -dx / n) if up else (-dy / n, dx / n)
        c = [(mx + nx * k, my + ny * k + 3.2, 'middle') for k in (11, 14, 17)]
        f.label(s, c, MUTED, SMALL)

    f.label('P(sick | +) = 50%', [(pos.cx, pos.b + 20, 'middle')], GREEN, LABEL, weight=600, mono=True)
    f.label('drawn from a pool 99× larger', [(fp.r + 10, fp.cy + 12, 'start'), (fp.r + 10, fp.cy + 4, 'start')], RED, SMALL)
    return f
