"""48 confounding: severity drives both who is treated and how they do.

History: the old figure printed "naive difference −0.9"; the topic's own code
(n = 20,000, seed 0; outcome = 2.0·treated − 3.0·severity + noise) gives
−1.13, which is also what the prose says ("reads −1.13. Not attenuated: the
wrong sign"), and +2.03 once severity is adjusted for (true effect +2.0).
The two estimates are now drawn on one number line, so the sign flip is the
picture, not a sentence.
"""
from figkit import Fig, BLUE, GREEN, AMBER, RED, FAINT, MUTED, INK, LABEL, SMALL

TARGET = ('48-causal-inference', 1)
NAIVE, ADJ, TRUE = -1.13, 2.03, 2.0


def draw():
    f = Fig(560, 268, 'cf')
    sev = f.box(225, 14, 110, 40, 'severity', 'the confounder', stroke=AMBER, color=AMBER)
    tre = f.box(60, 104, 110, 40, 'treated', 'yes / no', stroke=BLUE, color=BLUE)
    out = f.box(390, 104, 110, 40, 'outcome', 'higher is better', stroke=GREEN, color=GREEN)
    f.connect(sev, tre, AMBER, 1.6)
    f.connect(sev, out, AMBER, 1.6)
    f.connect(tre, out, BLUE, 1.8)
    f.label('sicker → more often treated', [(130, 66, 'end'), (140, 62, 'end')], AMBER)
    f.label('sicker → worse outcome', [(430, 66, 'start'), (420, 62, 'start')], AMBER)
    f.label('true effect +2.0', [(280, 118, 'middle'), (280, 116, 'middle')], BLUE, SMALL, weight=600)

    # the two estimates on one number line
    x0, x1, lo, hi = 150, 520, -1.5, 2.5
    X = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
    ya, yb = 184, 214
    f.line(X(0), ya - 14, X(0), yb + 14, FAINT, 1.2)
    for v in (-1, 1, 2):
        f.line(X(v), yb + 12, X(v), yb + 16, FAINT, 1)
    f.raw(f'<rect x="{X(NAIVE):.1f}" y="{ya - 7}" width="{X(0) - X(NAIVE):.1f}" height="14" rx="3" fill="{RED}" opacity=".85"/>',
          [(X(NAIVE), ya - 7), (X(0), ya - 7), (X(0), ya + 7), (X(NAIVE), ya + 7), (X(NAIVE), ya - 7)])
    f.raw(f'<rect x="{X(0):.1f}" y="{yb - 7}" width="{X(ADJ) - X(0):.1f}" height="14" rx="3" fill="{GREEN}" opacity=".85"/>',
          [(X(0), yb - 7), (X(ADJ), yb - 7), (X(ADJ), yb + 7), (X(0), yb + 7), (X(0), yb - 7)])
    f.line(X(TRUE), ya - 12, X(TRUE), yb + 10, BLUE, 1.2, dash='3 3')
    f.label('compare the two groups', [(x0 - 10, ya + 3.5, 'end')], RED, SMALL, weight=600)
    f.label('adjust for severity', [(x0 - 10, yb + 3.5, 'end')], GREEN, SMALL, weight=600)
    f.label('−1.13: wrong sign', [(X(NAIVE) - 6, ya + 3.5, 'end'), (X(0) + 6, ya + 3.5, 'start')], RED, SMALL, mono=True)
    f.label('+2.03', [(X(ADJ) + 6, yb + 3.5, 'start')], GREEN, SMALL, mono=True)
    f.label('true +2.0', [(X(TRUE) + 6, ya - 6, 'start'), (X(TRUE), ya - 16, 'middle')], BLUE, SMALL)
    for v, s in ((-1, '−1'), (0, '0'), (1, '+1'), (2, '+2')):
        f.label(s, [(X(v), yb + 27, 'middle')], FAINT, SMALL, mono=True, pad=1)
    f.label('randomise, adjust for the confounder, or use diff-in-diff; never just compare the groups',
            [(280, 262, 'middle')], AMBER, SMALL)
    return f
