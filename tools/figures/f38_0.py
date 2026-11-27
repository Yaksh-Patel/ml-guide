"""38 BERT: the attention mask is the whole encoder-vs-decoder distinction.

Two 5×5 masks, rows = the query position, columns = the key it may attend
to. BERT's is full; GPT's is lower-triangular (causal). Query 3 is outlined
in both, so the difference reads as one sentence: it sees 1–5 in BERT and
only 1–3 in GPT. Same content as the old figure, larger and with keys,
queries and the cut-off made explicit.
"""
from figkit import Fig, GREEN, BLUE, AMBER, MUTED, FAINT, BORD, SURF, LABEL, SMALL

TARGET = ('38-bert', 0)

N, CW, CH, G = 5, 28, 22, 4
GY = 72                   # grid top
T_ROW = 2                 # query 3 (0-based 2) is the highlighted row


def cell(f, x, y, color, on):
    if on:
        f.raw(f'<rect x="{x:.1f}" y="{y:.1f}" width="{CW}" height="{CH}" rx="3" fill="{color}" '
              f'fill-opacity=".42" stroke="{color}" stroke-width="1"/>',
              pts=[(x, y), (x + CW, y), (x + CW, y + CH), (x, y + CH), (x, y)])
    else:
        f.rect(x, y, CW, CH, fill=SURF, stroke=BORD, r=3, width=1)


def grid(f, gx, color, title, causal, sub, seen):
    gw = N * CW + (N - 1) * G
    for i in range(N):
        for j in range(N):
            cell(f, gx + j * (CW + G), GY + i * (CH + G), color, (not causal) or j <= i)
    # the highlighted query row
    ry = GY + T_ROW * (CH + G)
    f.rect(gx - 4, ry - 4, gw + 8, CH + 8, fill='none', stroke=AMBER, r=5, width=1.8)

    # indices
    for j in range(N):
        f.text(gx + j * (CW + G) + CW / 2, GY - 8, str(j + 1), FAINT, SMALL, 'middle', mono=True)
    for i in range(N):
        f.text(gx - 10, GY + i * (CH + G) + CH / 2 + 3.2, str(i + 1),
               AMBER if i == T_ROW else FAINT, SMALL, 'end', mono=True)
    f.text(gx, GY - 24, 'key →', FAINT, SMALL)
    f.text(gx - 24, GY + CH / 2 + 3.2, 'query ↓', FAINT, SMALL, 'end')

    f.text(gx + gw / 2, GY - 44, title, color, LABEL, 'middle', weight=600)
    f.text(gx + gw + 10, ry + CH / 2 + 3.4, seen, AMBER, SMALL, weight=600)
    f.text(gx + gw / 2, GY + N * (CH + G) + 14, sub, MUTED, SMALL, 'middle')


def draw():
    f = Fig(560, 262, 'msk')
    grid(f, 92, GREEN, 'BERT  (encoder)', False, 'every position sees every other', '3 sees 1–5')
    grid(f, 336, BLUE, 'GPT  (decoder)', True, 'position t sees only 1 … t', '3 sees 1–3')
    f.text(280, 250, 'So BERT cannot generate: when token 3 is being produced, 4 and 5 do not exist yet.',
           MUTED, LABEL, 'middle')
    return f
