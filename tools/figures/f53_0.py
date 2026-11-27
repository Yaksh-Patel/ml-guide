"""53 complexity classes: five growth rates, each labelled where its line ends.

The old figure listed the labels in a column that did not line up with the
curves (O(1) sat next to the steepest line). Here a curve that leaves the
top of the plot is labelled at its exit point; the others at their right end.
The dataframe-loop note sits in the empty top-right corner in the O(n²)
colour, with no leader line to cross the other curves.
"""
import math
from figkit import Fig, BLUE, GREEN, AMBER, RED, PURPLE, MUTED, LABEL, SMALL

TARGET = ('53-python-sql-dsa', 0)

N, YMAX = 20, 40
CURVES = [   # (label, fn, colour)
    ('O(1)',       lambda n: 1.0,                         GREEN),
    ('O(log n)',   lambda n: math.log2(max(n, 1)),        BLUE),
    ('O(n)',       lambda n: n,                           PURPLE),
    ('O(n log n)', lambda n: n * math.log2(max(n, 1)),    AMBER),
    ('O(n²)',      lambda n: n * n,                       RED),
]


def draw():
    f = Fig(560, 290, 'cx')
    p = f.plot_area(56, 40, 470, 236, (1, N), (-2, YMAX))
    p.axes(xlabel='input size n →', ylabel='operations')
    ends = []
    for label, fn, col in CURVES:
        pts = p.curve(fn, col, width=2.4)
        ends.append((label, col, pts[-1]))
    for label, col, (x, y) in ends:
        if y <= p.y0 + 0.5:        # left through the top: label just above the exit
            f.label(label, [(x, y - 9, 'middle')], col, LABEL, weight=600, mono=True, pad=1)
        else:                      # right end
            f.label(label, [(x + 8, y + 4, 'start')], col, LABEL, weight=600, mono=True, pad=1)

    tx, ty = p.X(11.5), p.Y(33)
    f.label('a nested loop over a dataframe is O(n²),', [(tx, ty, 'start')], RED, SMALL, weight=600)
    f.label('with a Python-sized constant on every step', [(tx, ty + 13, 'start')], MUTED, SMALL)
    return f
