"""09 threshold explorer (interactive): the static frame.

Confusion matrix | ROC | PR, side by side. The curves are fixed, so they
are drawn here from the same 1,000 scores the topic script generates (same
seeded LCG, 200 positives around 0.65, 800 negatives around 0.35, sd 0.18;
checked count-for-count against the script). The script only moves the two
amber dots, rewrites the four counts and their cell tints (ids thx-*), and
fills the HTML readout and note below.

History: the old explorer drew the curves in a separate 260-unit SVG beside
an HTML table, so its labels came out at 7 units and the rotated "TPR" was
clipped; it had a legend box; and at threshold 1.00 (no predicted
positives) its PR dot fell to precision 0 while the curve it sits on uses 1.
The PR curve now follows the threshold sweep instead of a sort by recall.
"""
import math
from figkit import Fig, BLUE, GREEN, AMBER, RED, PURPLE, FAINT, MUTED, BG, LABEL, SMALL, TINY

TARGET = ('09-confusion-roc', 0)

# shared with the topic script (keep in step)
CX, CY, CW, CH, CG = 70, 40, 64, 60, 4          # matrix cells
ROC = (246, 40, 370, 164)                        # x0, y0, x1, y1
PR = (420, 40, 544, 164)
T0 = 0.50                                        # the slider's initial value


def scores():
    """The topic script's data, bit for bit: s = (s*1664525 + 1013904223) | 0."""
    s = 42

    def rand():
        nonlocal s
        v = (s * 1664525 + 1013904223) % 2 ** 32
        s = v - 2 ** 32 if v >= 2 ** 31 else v
        return (s % 2 ** 32) / 0xffffffff

    def randn():
        a = math.sqrt(-2 * math.log(rand() + 1e-9))
        return a * math.cos(2 * math.pi * rand())

    out = [(min(.999, max(.001, .65 + randn() * .18)), 1) for _ in range(200)]
    out += [(min(.999, max(.001, .35 + randn() * .18)), 0) for _ in range(800)]
    return out


def counts(S, th):
    tp = sum(1 for s, y in S if s >= th and y)
    fp = sum(1 for s, y in S if s >= th and not y)
    return tp, 200 - tp, fp, 800 - fp          # tp, fn, fp, tn


def tint(n):
    return f'{0.07 + 0.3 * n / 1000:.3f}'


def draw():
    f = Fig(560, 196, 'thx')
    S = scores()
    sweep = [counts(S, t / 100) for t in range(101)]
    roc = [(fp / 800, tp / 200) for tp, fn, fp, tn in sweep]
    pr = [(tp / 200, tp / (tp + fp) if tp + fp else 1.0) for tp, fn, fp, tn in reversed(sweep)]

    def area(pts):
        return sum(abs(b[0] - a[0]) * (a[1] + b[1]) / 2 for a, b in zip(pts, pts[1:]))
    auc_roc, auc_pr = area(roc), area(sorted(pr, key=lambda p: p[0]))

    # ---- confusion matrix ------------------------------------------------------
    tp, fn, fp, tn = counts(S, T0)
    cells = (('tp', 'TP', tp, GREEN, 0, 0), ('fn', 'FN', fn, RED, 1, 0),
             ('fp', 'FP', fp, RED, 0, 1), ('tn', 'TN', tn, GREEN, 1, 1))
    for key, name, n, col, c, r in cells:
        x, y = CX + c * (CW + CG), CY + r * (CH + CG)
        f.raw(f'<rect id="thx-c{key}" x="{x}" y="{y}" width="{CW}" height="{CH}" rx="6" fill="{col}" '
              f'fill-opacity="{tint(n)}" stroke="{col}" stroke-opacity=".55" stroke-width="1"/>',
              [(x, y), (x + CW, y), (x + CW, y + CH), (x, y + CH), (x, y)])
        f.text(x + CW / 2, y + CH / 2 - 6, name, col, SMALL, 'middle', 600, halo=False)
        f.text(x + CW / 2, y + CH / 2 + 12, str(n), col, LABEL, 'middle', 600, mono=True, halo=False,
               extra=f' id="thx-{key}"')
    for c, s in enumerate(('predicted +', 'predicted −')):
        f.text(CX + c * (CW + CG) + CW / 2, CY - 10, s, MUTED, SMALL, 'middle')
    for r, s in enumerate(('actual +', 'actual −')):
        f.text(CX - 8, CY + r * (CH + CG) + CH / 2 + 3, s, MUTED, SMALL, 'end')

    # ---- ROC -------------------------------------------------------------------
    p = f.plot_area(*ROC, (0, 1), (0, 1))
    p.axes()
    f.line(p.X(0), p.Y(0), p.X(1), p.Y(1), FAINT, 1, dash='3 4')
    rpts = [(p.X(a), p.Y(b)) for a, b in roc]
    f.path(rpts, BLUE, 2.2)
    # ---- PR --------------------------------------------------------------------
    q = f.plot_area(*PR, (0, 1), (0, 1))
    q.axes()
    f.line(q.X(0), q.Y(0.2), q.X(1), q.Y(0.2), FAINT, 1, dash='3 4')
    ppts = [(q.X(a), q.Y(b)) for a, b in pr]
    f.path(ppts, PURPLE, 2.2)

    # ---- the current threshold (moved by the script) ---------------------------
    tpr, fpr, prec = tp / 200, fp / 800, tp / (tp + fp)
    f.circle(p.X(fpr), p.Y(tpr), 5, fill=AMBER, stroke=BG, width=1.5, extra=' id="thx-rdot"')
    f.circle(q.X(tpr), q.Y(prec), 5, fill=AMBER, stroke=BG, width=1.5, extra=' id="thx-pdot"')

    # ---- labels last -------------------------------------------------------------
    for pl, (yl, xl) in ((p, ('TPR', 'FPR →')), (q, ('precision', 'recall →'))):
        f.label(yl, [(pl.x0 + 8, pl.y0 - 10, 'start')], FAINT)
        f.label(xl, [(pl.x1 + 12, pl.y1 + 18, 'end')], FAINT)
        f.label('1', [(pl.x0 - 6, pl.y0 + 3, 'end')], FAINT, TINY)
    f.label('ROC', [(p.X(0.28), p.Y(0.76), 'start'), (p.X(0.3), p.Y(0.74), 'start')], BLUE, LABEL, weight=600)
    f.label(f'AUC {auc_roc:.2f}', [(p.X(0.28), p.Y(0.76) + 13, 'start'), (p.X(0.3), p.Y(0.74) + 13, 'start')], BLUE, SMALL)
    f.label('chance', [(p.X(0.56), p.Y(0.42), 'start'), (p.X(0.6), p.Y(0.5), 'start')], FAINT, TINY)
    f.label('PR', [(q.X(0.3), q.Y(0.70), 'middle'), (q.X(0.4), q.Y(0.62), 'middle')], PURPLE, LABEL, weight=600)
    f.label(f'AUC {auc_pr:.2f}', [(q.X(0.3), q.Y(0.70) + 13, 'middle')], PURPLE, SMALL)
    f.label('base rate 0.20', [(q.X(0.04), q.Y(0.2) - 6, 'start'), (q.X(0.04), q.Y(0.2) + 13, 'start')], FAINT, TINY)
    return f
