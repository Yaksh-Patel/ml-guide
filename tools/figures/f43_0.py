"""43 multimodal: CLIP's contrastive batch as a B × B similarity matrix.

Images index the rows (image encoder on the left), captions index the columns
(text encoder on top), so the reader can see where each axis comes from. The
diagonal holds the true pairs; every other cell in a row is a negative that
the batch supplied for free. The old four-line paragraph inside the SVG is
now two direct labels, and the takeaway uses the prose's number (CLIP's batch
of 32,768).
"""
from figkit import Fig, BLUE, GREEN, AMBER, PURPLE, FAINT, MUTED, BORD, LABEL, SMALL, TINY

TARGET = ('43-multimodal', 0)
B = 5
SUB = '₁₂₃₄₅'
# off-diagonal similarity, a little uneven so it reads as data, not a pattern
OFF = [[0, .16, .10, .22, .12],
       [.14, 0, .26, .10, .16],
       [.10, .20, 0, .14, .10],
       [.24, .10, .12, 0, .18],
       [.12, .16, .10, .20, 0]]


def draw():
    f = Fig(560, 300, 'clip')
    cs, cg = 28, 4
    mx0, my0 = 226, 100
    size = B * cs + (B - 1) * cg
    mcx, mcy = mx0 + size / 2, my0 + size / 2

    txt = f.box(mcx - 60, 10, 120, 38, 'text encoder', 'caption → unit vector', stroke=PURPLE, color=PURPLE, size=LABEL)
    img = f.box(40, mcy - 19, 120, 38, 'image encoder', 'image → unit vector', stroke=BLUE, color=BLUE, size=LABEL)
    f.arrow(txt.cx, txt.b, txt.cx, my0 - 20)
    f.arrow(img.r, img.cy, mx0 - 30, img.cy)

    for r in range(B):
        for c in range(B):
            x, y = mx0 + c * (cs + cg), my0 + r * (cs + cg)
            if r == c:
                fill, op = GREEN, .8
            else:
                fill, op = BLUE, OFF[r][c]
            f.raw(f'<rect x="{x}" y="{y}" width="{cs}" height="{cs}" rx="4" fill="{fill}" fill-opacity="{op}" '
                  f'stroke="{BORD}" stroke-width="1"/>',
                  pts=[(x, y), (x + cs, y), (x + cs, y + cs), (x, y + cs), (x, y)])

    # axis labels for the matrix (fixed positions, part of the grid)
    for i in range(B):
        c = mx0 + i * (cs + cg) + cs / 2
        f.text(c, my0 - 8, 'T' + SUB[i], PURPLE, SMALL, 'middle', weight=600)
        r = my0 + i * (cs + cg) + cs / 2 + 3
        f.text(mx0 - 9, r, 'I' + SUB[i], BLUE, SMALL, 'end', weight=600)

    # labels last
    right = mx0 + size + 12
    last = my0 + (B - 1) * (cs + cg) + cs / 2 + 3
    first = my0 + cs / 2 + 3
    f.label('diagonal: the true pairs', [(right, last, 'start')], GREEN, LABEL, weight=600)
    f.label('pulled together', [(right, last + 13, 'start')], MUTED, SMALL)
    f.label('off-diagonal: negatives', [(right, first, 'start')], BLUE, LABEL, weight=600)
    f.label('pushed apart, B − 1 per row', [(right, first + 13, 'start')], MUTED, SMALL)
    f.label(f'cosine similarity, B × B  (B = {B} here)', [(mcx, my0 + size + 16, 'middle')], FAINT, TINY)
    f.label("CLIP's batch is 32,768: each image must pick its caption out of 32,768",
            [(f.w / 2, 290, 'middle')], AMBER, SMALL)
    return f
