"""29 backprop stepper (interactive): the static frame.

x → z₁ = W₁x → h₁ = ReLU(z₁) → z₂ = W₂h₁ → ŷ = σ(z₂) → L = BCE(ŷ, y), with
x = 2.0, W₁ = 0.5, W₂ = 0.8, y = 1. Values flow right along the top of the
row (blue); gradients flow left underneath it (red), and up into the
weights (purple). Every number is drawn here, hidden; the topic script
reveals them step by step (ids bpx-*), drawing each arrow as it goes, and
fills the step chip and the note.

History: the old stepper was a 580-unit SVG with 22-unit nodes, its
"L = BCE" box ran off the right edge, and its edge highlights never showed
(an inline style lost to the theme's !important colour mapping). It jumped
from L straight to ∂L/∂z₂; the chain now passes through ∂L/∂ŷ = −y/ŷ, so
the sigmoid–BCE cancellation (ŷ − y) is visible rather than asserted. The
gradient into x (never used) is gone.
"""
import math
from figkit import (Fig, BLUE, AMBER, RED, PURPLE, FAINT, MUTED, INK, BORD, SURF, GAP,
                    HEAD_L, HEAD_W, LABEL, SMALL, TINY)

TARGET = ('29-backpropagation', 2)

X, W1, W2, Y = 2.0, 0.5, 0.8, 1.0
Z1 = W1 * X
H1 = max(0.0, Z1)
Z2 = W2 * H1
YH = 1 / (1 + math.exp(-Z2))
L = -(Y * math.log(YH) + (1 - Y) * math.log(1 - YH))
G_YH = -Y / YH + (1 - Y) / (1 - YH)
G_Z2 = YH - Y
G_H1 = G_Z2 * W2
G_Z1 = G_H1 * (1 if Z1 > 0 else 0)
G_W2 = G_Z2 * H1
G_W1 = G_Z1 * X

BW, BH, TOP = 58, 56, 96          # main-row boxes
WW, WH, WTOP = 58, 28, 22         # weight / label boxes
CX = [55 + 90 * i for i in range(6)]


def num(v, d=2):
    return f'{v:.{d}f}'.replace('-', '−')


def overlay(f, key, x1, y1, x2, y2, col, width=1.8):
    """An arrow the script draws in: a dashed-off line (pathLength 1) plus
    its own head, so the head can appear when the line arrives."""
    d = math.dist((x1, y1), (x2, y2))
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    bx, by = x2 - ux * HEAD_L, y2 - uy * HEAD_L
    px, py = -uy * HEAD_W / 2, ux * HEAD_W / 2
    f.raw(f'<g id="bpx-{key}"><path d="M{x1:.1f},{y1:.1f} L{bx + ux:.1f},{by + uy:.1f}" fill="none" '
          f'stroke="{col}" stroke-width="{width}" stroke-linecap="butt" pathLength="1" '
          f'stroke-dasharray="1 1" stroke-dashoffset="1"/>'
          f'<path d="M{x2:.1f},{y2:.1f} L{bx + px:.1f},{by + py:.1f} L{bx - px:.1f},{by - py:.1f} z" '
          f'fill="{col}" opacity="0"/></g>', [(x1, y1), (x2, y2)])


def node(f, key, x, y, w, h):
    f.raw(f'<rect id="bpx-n-{key}" x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="7" fill="{SURF}" '
          f'fill-opacity="1" stroke="{BORD}" stroke-width="1.4"/>',
          [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)])


def draw():
    f = Fig(560, 192, 'bpx')
    mid = TOP + BH / 2
    keys = ('x', 'z1', 'h1', 'z2', 'yh', 'L')
    sym = ('x', 'z₁', 'h₁', 'z₂', 'ŷ', 'L')
    form = ('input', 'W₁ · x', 'ReLU(z₁)', 'W₂ · h₁', 'σ(z₂)', 'BCE(ŷ, y)')
    vals = (num(X, 1), num(Z1), num(H1), num(Z2), num(YH, 3), num(L, 3))
    grads = (None, G_Z1, G_H1, G_Z2, G_YH, 1.0)
    gname = (None, '∂L/∂z₁', '∂L/∂h₁', '∂L/∂z₂', '∂L/∂ŷ', '∂L/∂L')

    # ---- boxes -----------------------------------------------------------------
    for i, k in enumerate(keys):
        node(f, k, CX[i] - BW / 2, TOP, BW, BH)
    tops = {1: ('w1', f'W₁ = {W1}'), 3: ('w2', f'W₂ = {W2}'), 5: ('y', f'y = {Y:.0f}')}
    for i, (k, s) in tops.items():
        node(f, k, CX[i] - WW / 2, WTOP, WW, WH)
        f.text(CX[i], WTOP + WH / 2 + 3.5, s, INK, SMALL, 'middle', 600, halo=False)

    # ---- forward edges: grey structure + blue overlays -------------------------------
    for i in range(5):
        x1, x2 = CX[i] + BW / 2 + GAP, CX[i + 1] - BW / 2 - GAP
        f.arrow(x1, mid, x2, mid, FAINT, 1.4, gap=0)
        overlay(f, f'f-{keys[i]}', x1, mid, x2, mid, BLUE)
    for i, (k, _) in tops.items():
        xx = CX[i] - (8 if k != 'y' else 0)
        y1, y2 = WTOP + WH + GAP, TOP - GAP
        f.arrow(xx, y1, xx, y2, FAINT, 1.4, gap=0)
        overlay(f, f'f-{k}', xx, y1, xx, y2, BLUE)
    # ---- backward edges (hidden until the backward pass) -------------------------------
    gy = TOP + BH + 20
    for i in range(1, 5):
        overlay(f, f'b-{keys[i + 1]}', CX[i + 1] - 24, gy, CX[i] + 24, gy, RED)
    for i, k in ((1, 'w1'), (3, 'w2')):
        overlay(f, f'b-{k}', CX[i] + 8, TOP - GAP, CX[i] + 8, WTOP + WH + GAP, PURPLE)

    # ---- node text: symbol, formula, value (value hidden until computed) ---------------
    for i, k in enumerate(keys):
        f.text(CX[i], TOP + 15, sym[i], INK, LABEL, 'middle', 600, halo=False)
        f.text(CX[i], TOP + 28, form[i], MUTED, TINY, 'middle', halo=False)
        col = AMBER if k == 'L' else BLUE
        op = '' if k == 'x' else ' opacity="0"'
        f.text(CX[i], TOP + 46, vals[i], INK if k == 'x' else col, LABEL, 'middle', 600, mono=True, halo=False,
               extra=f' id="bpx-v-{k}"{op}')
    # ---- gradients under the row, and beside the weights (hidden) ----------------------
    for i in range(1, 6):
        g = '1' if i == 5 else num(grads[i], 3)
        f.text(CX[i], gy - 2, g, RED, SMALL, 'middle', 600, mono=True, extra=f' id="bpx-g-{keys[i]}" opacity="0"')
        f.text(CX[i], gy + 10, gname[i], RED, TINY, 'middle', extra=f' id="bpx-gn-{keys[i]}" opacity="0"')
    for i, k, g, nm in ((1, 'w1', G_W1, '∂L/∂W₁'), (3, 'w2', G_W2, '∂L/∂W₂')):
        x = CX[i] + WW / 2 + 8
        f.text(x, WTOP + 12, num(g, 3), PURPLE, SMALL, 'start', 600, mono=True, extra=f' id="bpx-g-{k}" opacity="0"')
        f.text(x, WTOP + 24, nm, PURPLE, TINY, 'start', extra=f' id="bpx-gn-{k}" opacity="0"')

    f.label('forward →', [(CX[0] - BW / 2, TOP - 12, 'start')], BLUE, SMALL, weight=600)
    f.label('← backward', [(CX[0] - BW / 2, gy + 4, 'start')], RED, SMALL, weight=600)
    return f
