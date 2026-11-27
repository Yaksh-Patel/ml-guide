"""26 MLP forward pass: a 3-4-3-1 network, activation flowing layer by layer.

The old figure sent one dot along a single path and wired only the last
layer in colour. Now the whole layer fires: the inputs light, every edge into
the next layer carries the signal at once, that layer lights, and so on to ŷ.
Under each block of edges is the shape of its weight matrix, which is the
prose's parameter count (m·n weights plus n biases per layer) in miniature.
The ⚡ emoji note is replaced by one takeaway line.

Motion (one 6s clock): inputs light at 0.3s, then each layer's edges draw
in 0.7s and its units light; ŷ lights at 3.6s. Hold, fade, repeat.
Reduced motion shows the 4.4s frame: every edge and unit lit.
"""
import math
from figkit import Fig, Anim, BLUE, GREEN, PURPLE, FAINT, MUTED, INK, BORD, SURF, LABEL, SMALL, TINY

TARGET = ('26-mlp', 0)

R = 15
LX = [84, 210, 336, 462]
SIZES = [3, 4, 3, 1]
CY, SP = 116, 44
T = 6.0
FADE = 5.0


def ys(n):
    return [CY + (i - (n - 1) / 2) * SP for i in range(n)]


def draw():
    f = Fig(560, 254, 'mlp')
    A = Anim(T)
    f.still = 4.4
    layers = [[(x, y) for y in ys(n)] for x, n in zip(LX, SIZES)]
    cols = [BLUE, PURPLE, PURPLE, GREEN]

    # timing: layer k lights at lit[k]; edges into layer k draw over [lit[k]-0.7, lit[k]]
    lit = [0.3, 1.3, 2.3, 3.3]
    DRAW = 0.7

    # base edges (faint) and the animated overlay drawing over them
    over = [f'<g>{A.attr("opacity", [(0, 1), (FADE, 1), (FADE + 0.5, 0), (T, 0)])}']
    for k in range(1, 4):
        s, e = lit[k] - DRAW, lit[k]
        for (x1, y1) in layers[k - 1]:
            for (x2, y2) in layers[k]:
                d = math.dist((x1, y1), (x2, y2))
                ux, uy = (x2 - x1) / d, (y2 - y1) / d
                a = (x1 + ux * (R + 2), y1 + uy * (R + 2))
                b = (x2 - ux * (R + 2), y2 - uy * (R + 2))
                f.line(*a, *b, BORD, 1)
                over.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                            f'stroke="{BLUE}" stroke-width="1.3" opacity=".75" pathLength="1" '
                            f'stroke-dasharray="1 1" stroke-linecap="butt">'
                            f'{A.attr("stroke-dashoffset", [(0, 1), (s, 1), (e, 0), (T, 0)], spline=True)}</line>')

    # units: outline always, fill lights up when the layer fires
    for k, (layer, col) in enumerate(zip(layers, cols)):
        on = lit[k] if k == 0 else lit[k]
        for (x, y) in layer:
            f.circle(x, y, R, fill=SURF, stroke=col, width=1.6)
            over.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R - 1}" fill="{col}" opacity="0">'
                        f'{A.attr("opacity", [(0, 0), (on, 0), (on + 0.3, 0.38), (T, 0.38)], spline=True)}</circle>')
    over.append('</g>')
    f.raw('\n'.join(over))

    # unit names (inside the circles, so not part of the label check)
    for i, (x, y) in enumerate(layers[0]):
        f.text(x, y + 3.6, f'x{"₁₂₃"[i]}', INK, LABEL, 'middle', halo=False, check=False)
    x, y = layers[3][0]
    f.text(x, y + 3.6, 'ŷ', INK, LABEL, 'middle', halo=False, check=False)

    # labels last
    titles = ['input x', 'hidden 1', 'hidden 2', 'output ŷ']
    for x, t, col in zip(LX, titles, cols):
        f.label(t, [(x, 24, 'middle')], col, LABEL, weight=600)
    shapes = ['3×4 weights + 4 biases', '4×3 weights + 3 biases', '3×1 weights + 1 bias']
    for k, s in enumerate(shapes):
        mx = (LX[k] + LX[k + 1]) / 2
        f.label(s, [(mx, 218, 'middle')], MUTED, SMALL)
    f.label('Every edge is one learnable weight; each hidden layer computes ReLU(W · input + b).',
            [(280, 244, 'middle')], INK, SMALL)
    return f
