"""07 cross-validation: 5-fold CV, each fold taking its turn as validation.

The data is split into five folds (columns). Fit i trains on the other four
and is scored on fold i, giving L_i; the CV result is the mean of the five
scores with their spread, which the prose insists on reporting.

The old figure labelled the bars in the first two rows only and coloured the
validation fold red (an error colour); validation is now amber, the "look
here" colour, and every block is labelled the same way. History: the old
row labels called each row a "fold"; a row is one fit — the folds are the
columns.

Motion (one 9s clock): the fits appear one row at a time, so the validation
fold visibly walks along the diagonal; each row's score appears after it,
then the mean ± std. Hold, fade, repeat. Reduced motion shows the 7.2s
frame: all five rows, all five scores and the result.
"""
from figkit import Fig, Anim, BLUE, AMBER, GREEN, FAINT, MUTED, LABEL, SMALL

TARGET = ('07-cross-validation', 0)
K = 5
SUB = '₁₂₃₄₅'


def draw():
    f = Fig(560, 208, 'cv')
    X0, BW, G = 70, 72, 6
    Y0, BH, P = 34, 22, 30
    A = Anim(9.0)
    end = 8.2

    def fade(t_in):
        return A.attr('opacity', [(0, 0), (t_in, 0), (t_in + 0.45, 1), (end, 1), (end + 0.5, 0), (9.0, 0)], spline=True)

    for j in range(K):
        f.text(X0 + j * (BW + G) + BW / 2, Y0 - 10, f'fold {j + 1}', FAINT, SMALL, 'middle')

    starts = []
    for i in range(K):
        y = Y0 + i * P
        t_in = 0.4 + i * 1.05
        starts.append(t_in)
        f.raw(f'<g>{fade(t_in)}')
        f.text(X0 - 12, y + BH / 2 + 3.2, f'fit {i + 1}', MUTED, SMALL, 'end')
        for j in range(K):
            x = X0 + j * (BW + G)
            col = AMBER if i == j else BLUE
            f.raw(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="4" fill="{col}" opacity="{0.26 if i == j else 0.14}"/>')
            f.rect(x, y, BW, BH, fill='none', stroke=col, r=4, width=1.2 if i == j else 1)
            f.text(x + BW / 2, y + BH / 2 + 3.3, 'validate' if i == j else 'train', col, SMALL, 'middle',
                   weight=600 if i == j else None, halo=False)
        f.raw('</g>')
        # its score, a beat later
        f.raw(f'<g>{fade(t_in + 0.5)}')
        sx = X0 + K * (BW + G) + 8
        f.arrow(sx, y + BH / 2, sx + 22, y + BH / 2, FAINT, 1.3)
        f.text(sx + 30, y + BH / 2 + 3.5, f'L{SUB[i]}', AMBER, LABEL, weight=600)
        f.raw('</g>')

    t_res = starts[-1] + 1.2
    f.still = round(t_res + 1.4, 2)
    f.raw(f'<g>{fade(t_res)}')
    yl = Y0 + (K - 1) * P + BH + 7
    f.line(sx + 26, yl, sx + 50, yl, AMBER, 1.4)      # the "add them up" rule under the scores
    f.text(f.w - 14, yl + 17, 'CV score = mean(L₁ … L₅) ± std', GREEN, LABEL, 'end', weight=600)
    f.raw('</g>')
    return f
