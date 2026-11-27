"""15 decision trees: the first two splits of the iris tree, with the Gini of
every node and the impurity the root split buys.

Same numbers as the old figure (root 0.667 at 50/50/50, a pure setosa leaf,
0.500 on the right, then 0.168 / 0.043 after the petal-width split). New:
the second split shows its threshold and class counts (iris: petal width
≤ 1.75 gives 0/49/5 and 0/1/45, which is where 0.168 and 0.043 come from),
and the root's gain is written out as the size-weighted sum the prose
describes: 0.667 − (⅓·0 + ⅔·0.500) = 0.333.
"""
from figkit import Fig, GREEN, AMBER, INK, MUTED, BORD, LABEL, SMALL, TINY

TARGET = ('15-decision-trees', 0)

BW, BH = 128, 38


def draw():
    f = Fig(560, 262, 'dt')

    root = f.box(280 - BW / 2, 14, BW, BH, 'gini 0.667', '50 / 50 / 50', size=LABEL)
    left = f.box(120 - BW / 2, 102, BW, BH, 'gini 0.000', '50 / 0 / 0   pure', stroke=GREEN,
                 color=GREEN, size=LABEL)
    right = f.box(400 - BW / 2, 102, BW, BH, 'gini 0.500', '0 / 50 / 50', size=LABEL)
    rl = f.box(330 - 112 / 2, 190, 112, BH, 'gini 0.168', '0 / 49 / 5', size=LABEL, color=MUTED)
    rr = f.box(470 - 112 / 2, 190, 112, BH, 'gini 0.043', '0 / 1 / 45', size=LABEL, color=MUTED)

    # edges leave from the bottom of the parent and land on the top of the child
    def edge(a, b):
        x0 = a.cx + (18 if b.cx > a.cx else -18)
        f.arrow(x0, a.b, b.cx, b.t, width=1.4)
        return ((x0 + b.cx) / 2, (a.b + b.t) / 2)

    m1, m2, m3, m4 = edge(root, left), edge(root, right), edge(right, rl), edge(right, rr)

    # labels last: split conditions sit beside their edges, clear of the line
    f.label('petal length ≤ 2.45', [(m1[0] - 12, m1[1] + 3, 'end'), (m1[0] - 16, m1[1] - 4, 'end')], AMBER, SMALL)
    f.label('> 2.45', [(m2[0] + 12, m2[1] + 3, 'start'), (m2[0] + 16, m2[1] - 4, 'start')], AMBER, SMALL)
    f.label('petal width ≤ 1.75', [(m3[0] - 10, m3[1] + 3, 'end'), (m3[0] - 14, m3[1] - 2, 'end')], AMBER, SMALL)
    f.label('> 1.75', [(m4[0] + 10, m4[1] + 3, 'start'), (m4[0] + 14, m4[1] - 2, 'start')], AMBER, SMALL)
    f.label('setosa / versicolor / virginica', [(root.r + 10, root.b - 6, 'start')], MUTED, TINY)

    gx, gy = left.cx, 180
    f.label('gain at the root, weighted by node size', [(gx, gy, 'middle')], MUTED, SMALL)
    f.label('0.667 − (⅓·0 + ⅔·0.500) = 0.333', [(gx, gy + 16, 'middle')], INK, LABEL, weight=600)
    f.label('Summed over every split on a feature, this gain is its feature_importances_.',
            [(f.w / 2, f.h - 8, 'middle')], MUTED, SMALL)
    return f
