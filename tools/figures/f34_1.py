"""34 attention weights: the query "bank" attends to every token of
"I went to bank to deposit $", and the softmax puts most of the weight on
"deposit" (0.42) and "$" (0.25). The weights sum to 1.

History: the old bars were not drawn to scale (0.04 filled 18% of its track,
0.42 filled 97%, and every track had a different length), so the picture
overstated the contrast. Bars now share one scale and stand on the tokens
they belong to. The list of head specialisations is dropped: it is the
prose's point (multi-head), not this figure's. Static.
"""
from figkit import Fig, BLUE, GREEN, AMBER, MUTED, INK, BORD, SURF, LABEL, SMALL

TARGET = ('34-attention-architecture', 1)

TOKENS = ('I', 'went', 'to', 'bank', 'to', 'deposit', '$')
ALPHA = (0.04, 0.06, 0.10, 0.08, 0.05, 0.42, 0.25)
QUERY, HIGH = 3, (5, 6)


def draw():
    f = Fig(560, 214, 'atb')
    bw, gap, ty, th = 62, 12, 140, 28
    x0 = (560 - (len(TOKENS) * bw + (len(TOKENS) - 1) * gap)) / 2
    cx = [x0 + bw / 2 + i * (bw + gap) for i in range(len(TOKENS))]
    base, scale, w = ty - 8, 230, 28

    for i, (s, a) in enumerate(zip(TOKENS, ALPHA)):
        col = GREEN if i in HIGH else BLUE
        h = a * scale
        f.rect(cx[i] - w / 2, base - h, w, h, fill=col, stroke=col, r=2, width=1, opacity=0.85 if i in HIGH else 0.6)
        f.text(cx[i], base - h - 6, f'{a:.2f}', col, SMALL, 'middle', 600 if i in HIGH else None, mono=True)
        if i == QUERY:
            f.box(cx[i] - bw / 2, ty, bw, th, s, stroke=AMBER, color=AMBER, size=LABEL, width=1.8)
        elif i in HIGH:
            f.box(cx[i] - bw / 2, ty, bw, th, s, stroke=GREEN, color=GREEN, size=LABEL)
        else:
            f.box(cx[i] - bw / 2, ty, bw, th, s, stroke=BORD, color=INK, size=LABEL, weight=None)

    f.label('query', [(cx[QUERY], ty + th + 14, 'middle')], AMBER, SMALL, weight=600)
    f.label('attention weight from "bank" to each token (softmax: they sum to 1)', [(x0, 18, 'start')], MUTED, SMALL)
    f.label('most of the weight lands on "deposit" and "$": this "bank" holds money, not a river',
            [(280, 206, 'middle')], MUTED, SMALL)
    return f
