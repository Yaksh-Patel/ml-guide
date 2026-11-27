"""52 system design: the two-stage search funnel.

query → dense (ANN) and sparse (BM25) retrieval → merge & dedupe → LTR
rerank → top-K. Under each stage, a bar for how many items are still in play
(log scale: ~100M → ~500 → 50 → 10), which is the funnel the prose argues is
forced by arithmetic. The takeaway is the prose's ceiling: end-to-end recall
cannot beat stage-one recall. The old 7-unit sub-labels overflowed their
boxes; boxes are now sized to their text.
"""
import math
from figkit import Fig, BLUE, GREEN, AMBER, PURPLE, FAINT, MUTED, INK, BORD, LABEL, SMALL, TINY

TARGET = ('52-system-design', 0)


def draw():
    f = Fig(560, 252, 'srch')
    cy = 78
    q = f.box(12, cy - 18, 66, 36, 'Query', stroke=BLUE, color=BLUE, size=LABEL)
    dn = f.box(110, cy - 52, 112, 40, 'Dense retrieval', 'ANN index (FAISS)', stroke=GREEN, color=GREEN, size=LABEL)
    sp = f.box(110, cy + 12, 112, 40, 'Sparse retrieval', 'BM25 keyword match', stroke=GREEN, color=GREEN, size=LABEL)
    mg = f.box(254, cy - 20, 82, 40, 'Merge', 'and dedupe', stroke=AMBER, color=AMBER, size=LABEL)
    rr = f.box(366, cy - 20, 104, 40, 'LTR reranker', 'LambdaMART / XGBoost', stroke=PURPLE, color=PURPLE, size=LABEL)
    tk = f.box(498, cy - 20, 52, 40, 'Top-K', 'served', stroke=BLUE, color=BLUE, size=LABEL)
    for a, b in ((q, dn), (q, sp), (dn, mg), (sp, mg), (mg, rr), (rr, tk)):
        f.connect(a, b)

    # the funnel: items in play per stage, log scale
    base, per_decade, bw = 214, 7.0, 34
    stages = [(dn.cx, 1e8, '~100M docs', GREEN), (mg.cx, 500, '~500', AMBER),
              (rr.cx, 50, '50', PURPLE), (tk.cx, 10, '10', BLUE)]
    f.line(q.l, base, tk.r, base, FAINT, 1)
    tops = []
    for x, n, _, col in stages:
        h = per_decade * math.log10(n)
        f.rect(x - bw / 2, base - h, bw, h, fill=col, stroke=col, r=2, opacity=.55)
        tops.append(base - h)

    # labels last
    f.label('"best running shoes"', [(q.cx - 2, q.b + 14, 'middle'), (q.l, q.b + 14, 'start')], MUTED, TINY)
    for (x, n, s, col), t in zip(stages, tops):
        f.label(s, [(x, t - 6, 'middle')], col, LABEL, weight=600)
    f.label('items in play', [(q.l, base - 18, 'start')], FAINT, TINY)
    f.label('(log scale)', [(q.l, base - 6, 'start')], FAINT, TINY)
    f.label('end-to-end recall ≤ retrieval recall: no reranker can rescue what stage one dropped',
            [(f.w / 2, 240, 'middle')], AMBER, SMALL)
    return f
