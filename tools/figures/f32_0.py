"""32 convolution: a 2×2 kernel slides over a 5×5 input and fills a 4×4 feature map.

History: the old kernel [[1, 0], [-1, 1]] was labelled "edge detector" but is
not one, the feature map was random shading unrelated to any input, and the
window visited only 9 of the 16 positions. Now the input is a real image (a
bright region with a stepped edge), the kernel [[-1, 1], [-1, 1]] responds to
a dark-to-bright step left to right, and every output cell is the actual sum
Σ in·K under the window, so the feature map traces the edge. Output size
(5 − 2)/1 + 1 = 4, as in the prose's formula. The 🟡 emoji is gone.

Motion (one 10s clock): the window steps through all 16 positions in reading
order; as it lands, the matching output cell (outlined in step) gets its
value. Hold, fade the outputs, repeat. Reduced motion shows the 8.2s frame:
window at the last position, the whole feature map filled.
"""
from figkit import (Fig, Anim, BLUE, AMBER, PURPLE, FAINT, MUTED, INK, BORD, SURF,
                    LABEL, SMALL, TINY)

TARGET = ('32-cnns', 0)

IMG = [[0, 0, 1, 1, 1],
       [0, 0, 1, 1, 1],
       [0, 0, 0, 1, 1],
       [0, 0, 0, 1, 1],
       [0, 0, 0, 0, 1]]
K = [[-1, 1],
     [-1, 1]]
C = 26                     # cell size
IX, IY = 47, 50            # input grid origin
KX, KY = 267, 89           # kernel origin
OX, OY = 409, 63           # output grid origin
T = 10.0
T0, STEP, MOVE = 0.4, 0.45, 0.2
FADE_OUT, RESET = 9.0, 9.3


def conv():
    n = len(IMG) - len(K) + 1
    return [[sum(IMG[i + m][j + q] * K[m][q] for m in range(2) for q in range(2))
             for j in range(n)] for i in range(n)]


def cell(f, x, y, fill=SURF, stroke=BORD, opacity=None):
    op = f' fill-opacity="{opacity}"' if opacity is not None else ''
    f.raw(f'<rect x="{x:.1f}" y="{y:.1f}" width="{C}" height="{C}" fill="{fill}"{op} '
          f'stroke="{stroke}" stroke-width="1"/>',
          pts=[(x, y), (x + C, y), (x + C, y + C), (x, y + C), (x, y)])


def num(f, x, y, v, col):
    f.text(x + C / 2, y + C / 2 + 3.2, v, col, SMALL, 'middle', mono=True, halo=False)


def draw():
    f = Fig(560, 222, 'cnn')
    out = conv()
    A = Anim(T)
    f.still = 8.2

    # input image
    for i, row in enumerate(IMG):
        for j, v in enumerate(row):
            x, y = IX + j * C, IY + i * C
            if v:
                cell(f, x, y, BLUE, BORD, 0.28)
            else:
                cell(f, x, y)
            num(f, x, y, v, INK if v else FAINT)

    # kernel
    for m in range(2):
        for q in range(2):
            x, y = KX + q * C, KY + m * C
            cell(f, x, y, AMBER, AMBER, 0.14)
            num(f, x, y, str(K[m][q]).replace('-', '−'), AMBER)

    # empty output grid
    for i in range(4):
        for j in range(4):
            cell(f, OX + j * C, OY + i * C)

    # flow arrows
    f.arrow(IX + 5 * C + 14, IY + 2.5 * C, KX - 14, IY + 2.5 * C, FAINT, 1.4, gap=0)
    f.arrow(KX + 2 * C + 14, IY + 2.5 * C, OX - 14, IY + 2.5 * C, FAINT, 1.4, gap=0)

    # timing: position k (reading order) is reached at arrive[k]
    arrive = [T0 + k * STEP for k in range(16)]
    pos = [(k // 4, k % 4) for k in range(16)]

    def track(coord, origin):
        pairs = [(0, origin(pos[0])), (arrive[0], origin(pos[0]))]
        for k in range(1, 16):
            pairs += [(arrive[k] - MOVE, origin(pos[k - 1])), (arrive[k], origin(pos[k]))]
        pairs += [(RESET, origin(pos[15])), (RESET + 0.35, origin(pos[0])), (T, origin(pos[0]))]
        return A.attr(coord, [(t, f'{v:.1f}') for t, v in pairs], spline=True)

    # output values appear as the window lands
    for k, (i, j) in enumerate(pos):
        v = out[i][j]
        x, y = OX + j * C, OY + i * C
        on = arrive[k]
        g = [f'<g opacity="0">{A.attr("opacity", [(0, 0), (on, 0), (on + 0.12, 1), (FADE_OUT, 1), (FADE_OUT + 0.4, 0), (T, 0)])}']
        if v:
            g.append(f'<rect x="{x + 1:.1f}" y="{y + 1:.1f}" width="{C - 2}" height="{C - 2}" fill="{PURPLE}" '
                     f'fill-opacity="{0.22 + 0.22 * v:.2f}"/>')
        col = INK if v else FAINT
        g.append(f'<text x="{x + C / 2:.1f}" y="{y + C / 2 + 3.2:.1f}" fill="{col}" font-size="{SMALL}" '
                 f'text-anchor="middle" font-family="JetBrains Mono">{v}</text></g>')
        f.raw(''.join(g))

    # the sliding window and its output cell, on the same clock
    f.raw(f'<rect x="{IX:.1f}" y="{IY:.1f}" width="{2 * C}" height="{2 * C}" rx="2" fill="{AMBER}" '
          f'fill-opacity=".08" stroke="{AMBER}" stroke-width="2.2">'
          f'{track("x", lambda p: IX + p[1] * C)}{track("y", lambda p: IY + p[0] * C)}</rect>')
    f.raw(f'<rect x="{OX:.1f}" y="{OY:.1f}" width="{C}" height="{C}" rx="2" fill="none" '
          f'stroke="{AMBER}" stroke-width="2.2">'
          f'{track("x", lambda p: OX + p[1] * C)}{track("y", lambda p: OY + p[0] * C)}</rect>')

    # labels last
    f.label('input 5×5', [(IX + 2.5 * C, IY - 12, 'middle')], MUTED, LABEL, weight=600)
    f.label('kernel 2×2', [(KX + C, KY - 12, 'middle')], AMBER, LABEL, weight=600)
    f.label('feature map 4×4', [(OX + 2 * C, OY - 12, 'middle')], PURPLE, LABEL, weight=600)
    f.label('out = Σ in · K', [(KX + C, KY + 2 * C + 18, 'middle')], MUTED, TINY, mono=True)
    f.label('(5 − 2)/1 + 1 = 4', [(OX + 2 * C, OY + 4 * C + 18, 'middle')], MUTED, TINY, mono=True)
    f.label('The same 4 weights at all 16 positions: the edge lights up wherever it is.',
            [(280, 212, 'middle')], INK, SMALL)
    return f
