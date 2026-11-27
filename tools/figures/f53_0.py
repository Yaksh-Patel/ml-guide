"""53 complexity classes: five growth rates, each labelled where its line ends.

The old figure listed the labels in a column that did not line up with the
curves (O(1) sat next to the steepest line). Here a curve that leaves the
top of the plot is labelled at its exit point; the others at their right end.
"""
import math
from figkit import Fig, BLUE, GREEN, AMBER, RED, PURPLE, FAINT, MUTED, LABEL, SMALL

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
    f = Fig(560, 300, 'cx')
    p = f.plot_area(56, 40, 470, 246, (1, N), (-2, YMAX))
    p.axes(xlabel='input size n →', ylabel='operations')
    for label, fn, col in CURVES:
        pts = p.curve(fn, col, width=2.4)
        x, y = pts[-1]
        if y <= p.y0 + 0.5:        # left through the top: label just above the exit
            f.text(x, y - 8, label, col, LABEL, anchor='middle', weight=600, mono=True)
        else:                      # right end
            f.text(x + 8, y + 4, label, col, LABEL, weight=600, mono=True)

    # where a row-by-row dataframe loop lands
    xr, yr = p.X(5.2), p.Y(5.2 ** 2)
    f.circle(xr, yr, 5, stroke=RED, width=2)
    f.line(xr + 6, yr + 4, p.X(8.4) - 4, p.Y(16) - 6, FAINT, 1)
    f.text(p.X(8.4), p.Y(16), 'nested loop over a dataframe:', RED, SMALL)
    f.text(p.X(8.4), p.Y(16) + 13, 'O(n²), with a Python-sized constant', MUTED, SMALL)
    return f
