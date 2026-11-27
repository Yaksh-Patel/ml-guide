"""34 attention: one decoder step of Bahdanau attention, "I love Paris" →
"J'aime Paris".

The decoder is about to produce "Paris" (step 3). Its previous state s₂ is
the query; it scores every encoder state hᵢ, the softmax turns the scores
into weights αᵢ (0.1, 0.2, 0.7: drawn as bars and as line widths), and the
weighted sum c₃ = Σ αᵢ hᵢ goes into s₃.

History: the old figure's weights were the ones for producing "Paris"
(0.7 on the source "Paris") but its context arrow ran into s₁, the step that
produces "J'". Here the context feeds s₃ and the query comes from s₂, as in
e_ti = score(s_{t−1}, hᵢ). The old "TRANSFORMER = …" banner overflowed its box
and is a different idea; the next section of the prose covers it. Static.
"""
from figkit import Fig, BLUE, GREEN, AMBER, MUTED, FAINT, INK, GAP, LABEL, SMALL, TINY

TARGET = ('34-attention-architecture', 0)

ALPHA = (0.1, 0.2, 0.7)


def draw():
    f = Fig(560, 286, 'att')
    bw, bh, by = 58, 32, 200
    ex = [62, 152, 242]
    dx = [338, 418, 498]
    enc = [f.box(x - bw / 2, by, bw, bh, f'h{"₁₂₃"[i]}', stroke=BLUE, color=BLUE, size=LABEL)
           for i, x in enumerate(ex)]
    dec = [f.box(x - bw / 2, by, bw, bh, f's{"₁₂₃"[i]}', stroke=AMBER if i == 2 else GREEN,
                 color=AMBER if i == 2 else GREEN, size=LABEL, width=1.8 if i == 2 else 1.2)
           for i, x in enumerate(dx)]
    for a, b in zip(enc, enc[1:]):
        f.connect(a, b, BLUE, 1.4)
    for a, b in zip(dec, dec[1:]):
        f.connect(a, b, GREEN, 1.4)

    # attention weights as bars on the encoder states
    base, hmax, w = by - 10, 56, 26
    tops = []
    for x, a in zip(ex, ALPHA):
        h = hmax * a / max(ALPHA)
        f.rect(x - w / 2, base - h, w, h, fill=AMBER, stroke=AMBER, r=2, width=1, opacity=0.35 + 0.6 * a / max(ALPHA))
        tops.append((x, base - h))

    # weighted sum → context
    c = f.box(102, 52, 100, 30, 'c₃ = Σ αᵢ hᵢ', stroke=AMBER, color=AMBER, size=LABEL, width=1.6)
    for (x, y), a in zip(tops, ALPHA):
        tx = c.cx + (x - c.cx) * 0.35
        f.line(x, y - 3, tx, c.b + 3, AMBER, 1 + 5 * a, opacity=0.9)
    # context → s3
    f.qcurve((c.r + GAP, c.cy), (dx[2], c.cy), (dx[2], by - 5), AMBER, 1.8, arrow=True)
    # query s2 → the scores
    f.qcurve((dx[1] - 14, by - 4), (dx[1] - 40, 150), (ex[2] + 26, 156), GREEN, 1.3, arrow=True, dash='4 3')

    words_src = ('I', 'love', 'Paris')
    words_tgt = ("J'", 'aime', 'Paris')
    for x, s in zip(ex, words_src):
        f.text(x, by + bh + 18, s, INK, LABEL, 'middle')
    for i, (x, s) in enumerate(zip(dx, words_tgt)):
        f.text(x, by + bh + 18, s, AMBER if i == 2 else INK, LABEL, 'middle', 600 if i == 2 else None)
    f.text(ex[1], by + bh + 40, 'encoder: source', BLUE, SMALL, 'middle', 600)
    f.text(dx[1], by + bh + 40, 'decoder: target', GREEN, SMALL, 'middle', 600)

    for (x, y), a in zip(tops, ALPHA):
        f.label(f'{a}', [(x - 19, base - 2, 'end'), (x + 19, base - 2, 'start'), (x, y - 6, 'middle')], AMBER, SMALL, weight=600)
    f.label('αᵢ = softmax(score(s₂, hᵢ))', [(266, 132, 'start'), (266, 122, 'start'), (266, 142, 'start')], AMBER, SMALL)
    f.label('context c₃', [(330, c.cy - 8, 'middle'), (300, c.cy - 8, 'middle')], AMBER, SMALL, weight=600)
    f.label('query s₂', [(dx[1] - 44, 146, 'end'), (dx[1] - 30, 140, 'end')], GREEN, SMALL)
    f.label('a fresh context for every output word, built from all the encoder states',
            [(16, 22, 'start')], MUTED, SMALL)
    return f

