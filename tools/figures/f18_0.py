"""18 XGBoost: the four additions over plain gradient boosting, and the split
gain that two of them produce.

History: the old figure gave the gain as "½ · G²/(H+λ) − γ", which is one
leaf's score, not the gain of a split; the prose's formula (and its worked
example, G = 4, H = 10, λ = 1 → 2.606 − γ) needs both children minus the
parent. The histogram box claimed "O(n) splits instead of O(n log n) sorts",
which the prose never says; the prose's point is ~256 bins searched instead of
every distinct value, so the box says that. The tiny grey sentences and the
monotone-constraints footnote (covered in its own prose section) are gone.

The formula's H terms are drawn in the 2nd-order colour and λ, γ in the
regularised colour, so each box points at the part of the formula it adds.
"""
from figkit import Fig, BLUE, PURPLE, INK, MUTED, FAINT, BORD, LABEL, SMALL, TINY

TARGET = ('18-xgboost', 0)

FS = LABEL                        # formula size (the spec maximum)
W_CH = 0.46                       # formula advance (figkit's 0.5 is for running text)


def _w(parts):
    return sum(len(s) * (TINY if k == 'sub' else FS) * W_CH for s, _, k in parts)


def _tspans(parts):
    """parts = [(text, colour, 'n' | 'sub')] -> tspans; subscripts drop 3 units and return."""
    out, low = [], False
    for s, col, k in parts:
        sub = k == 'sub'
        dy = ' dy="3"' if sub and not low else (' dy="-3"' if low and not sub else '')
        size = f' font-size="{TINY}"' if sub else ''
        out.append(f'<tspan fill="{col}"{size}{dy}>{s}</tspan>')
        low = sub
    return ''.join(out)


def _put(f, cx, y, parts, weight=600):
    """Centred formula text with subscripts; registered with check()."""
    w = _w(parts)
    f.raw(f'<text x="{cx:.1f}" y="{y:.1f}" font-size="{FS}" text-anchor="middle" font-family="DM Sans" '
          f'font-weight="{weight}">{_tspans(parts)}</text>')
    f.texts.append((cx - w / 2, y - FS * 0.76, cx + w / 2, y + FS * 0.22 + 3, ''.join(p[0] for p in parts)))


def draw():
    f = Fig(560, 216, 'xg')

    # ---- the four additions ----------------------------------------------------------
    boxes = [('2nd-order', 'gradient G and Hessian H', BLUE),
             ('regularised', 'λ on leaf weights, γ per leaf', PURPLE),
             ('sparsity-aware', 'learns where NaNs go', INK),
             ('histogram splits', '~256 bins, not every value', INK)]
    bw, bh, gap, by = 126, 50, 8, 34
    x0 = (560 - (4 * bw + 3 * gap)) / 2
    for i, (t, s, col) in enumerate(boxes):
        f.box(x0 + i * (bw + gap), by, bw, bh, t, s, stroke=col if col != INK else BORD,
              color=col, size=LABEL, width=1.4)
    f.text(x0, by - 12, 'plain gradient boosting, plus', FAINT, SMALL)

    # ---- the split gain ------------------------------------------------------------------
    G, H, LAM, GAM = INK, BLUE, PURPLE, PURPLE
    num_L = [('G', G, 'n'), ('L', G, 'sub'), ('²', G, 'n')]
    den_L = [('H', H, 'n'), ('L', H, 'sub'), (' + ', MUTED, 'n'), ('λ', LAM, 'n')]
    num_R = [('G', G, 'n'), ('R', G, 'sub'), ('²', G, 'n')]
    den_R = [('H', H, 'n'), ('R', H, 'sub'), (' + ', MUTED, 'n'), ('λ', LAM, 'n')]
    num_P = [('G²', G, 'n')]
    den_P = [('H', H, 'n'), (' + ', MUTED, 'n'), ('λ', LAM, 'n')]
    seq = [('t', [('Gain = ½ [', INK, 'n')]),
           ('f', num_L, den_L, 'left child'),
           ('t', [('+', INK, 'n')]),
           ('f', num_R, den_R, 'right child'),
           ('t', [('−', INK, 'n')]),
           ('f', num_P, den_P, 'parent'),
           ('t', [('] − ', INK, 'n'), ('γ', GAM, 'n')])]
    pad = 14
    widths = []
    for item in seq:
        if item[0] == 't':
            widths.append(_w(item[1]) + pad)
        else:
            widths.append(max(_w(item[1]), _w(item[2])) + pad + 8)
    total = sum(widths)
    x, mid = (560 - total) / 2, 136          # mid = fraction-bar height
    for item, w in zip(seq, widths):
        cx = x + w / 2
        if item[0] == 't':
            _put(f, cx, mid + 3.6, item[1])
        else:
            _, num, den, note = item
            fw = max(_w(num), _w(den)) + 4
            f.line(cx - fw / 2, mid, cx + fw / 2, mid, INK, 1.1)
            _put(f, cx, mid - 9, num)
            _put(f, cx, mid + 13, den)
            f.label(note, [(cx, mid + 34, 'middle')], MUTED, SMALL)
        if item[0] == 't' and item[1][-1][0] == 'γ':
            gx = cx + _w(item[1]) / 2 - FS * W_CH / 2
            f.label('price of a leaf', [(gx, mid + 34, 'middle'), (gx + 8, mid + 34, 'middle')], PURPLE, SMALL)
        x += w

    f.label('a split whose gain does not pay γ is never made: that is the pruning',
            [(280, 206, 'middle')], MUTED, SMALL)
    return f
