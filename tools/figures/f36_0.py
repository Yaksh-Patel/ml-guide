"""36 LoRA: h = Wx + ABx. The input goes through the frozen W and, in
parallel, through the trained low-rank pair, squeezed to rank r and widened
back; the two are added.

The pair is drawn as two trapezoids so the bottleneck is a shape, not a
label: B narrows k → r, A widens r → d.

History: the old figure ran x through A (d × r) first and then B (r × k).
With the prose's ΔW = AB, A ∈ ℝ^(d×r), B ∈ ℝ^(r×k), the input meets B first
(ABx = A(Bx)), and only that order type-checks. It also used r = 4 where the
prose's worked example is r = 16, and a lock emoji. Static.
"""
from figkit import Fig, BLUE, GREEN, AMBER, INK, MUTED, FAINT, SURF, GAP, LABEL, SMALL, TINY

TARGET = ('36-transfer-distillation', 0)


def trapezoid(f, x0, x1, cy, h0, h1, color):
    pts = [(x0, cy - h0 / 2), (x1, cy - h1 / 2), (x1, cy + h1 / 2), (x0, cy + h0 / 2), (x0, cy - h0 / 2)]
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ' Z'
    f.raw(f'<path d="{d}" fill="{color}" fill-opacity=".14" stroke="{color}" stroke-width="1.6" '
          f'stroke-linejoin="round"/>', pts)


def draw():
    f = Fig(560, 240, 'lora')
    ty, by_ = 62, 166                 # the two paths
    xb = f.box(20, 98, 42, 32, 'x', stroke=FAINT, color=INK, size=LABEL)
    w = f.box(128, ty - 34, 148, 68, 'W', 'd × k · frozen', stroke=BLUE, color=BLUE, size=LABEL)

    bx0, bx1, ax0, ax1 = 128, 186, 218, 276
    trapezoid(f, bx0, bx1, by_, 66, 16, GREEN)
    trapezoid(f, ax0, ax1, by_, 16, 66, GREEN)
    f.arrow(bx1, by_, ax0, by_, GREEN, 1.6, gap=2)
    f.text(bx0 + 20, by_ + 3.6, 'B', GREEN, LABEL, 'middle', 600, halo=False)
    f.text(ax1 - 20, by_ + 3.6, 'A', GREEN, LABEL, 'middle', 600, halo=False)

    sx, sy = 350, 114
    f.circle(sx, sy, 11, fill=SURF, stroke=AMBER, width=1.8)
    f.text(sx, sy + 4.5, '+', AMBER, 13, 'middle', 600, halo=False, check=False)
    hb = f.box(404, sy - 16, 42, 32, 'h', stroke=AMBER, color=AMBER, size=LABEL)

    # x splits into the two paths; they meet at +
    f.qcurve((xb.r + GAP, xb.cy - 6), (96, ty), (w.l - GAP, ty), FAINT, 1.4, arrow=True)
    f.qcurve((xb.r + GAP, xb.cy + 6), (96, by_), (bx0 - GAP, by_), FAINT, 1.4, arrow=True)
    f.qcurve((w.r + GAP, ty), (sx, ty), (sx, sy - 11 - GAP), BLUE, 1.6, arrow=True)
    f.qcurve((ax1 + GAP, by_), (sx, by_), (sx, sy + 11 + GAP), GREEN, 1.6, arrow=True)
    f.arrow(sx + 11, sy, hb.l, sy, AMBER, 1.6)

    f.label('r × k · init 0', [((bx0 + bx1) / 2, by_ + 48, 'middle')], GREEN, TINY)
    f.label('d × r · init random', [((ax0 + ax1) / 2 + 6, by_ + 48, 'middle')], GREEN, TINY)
    f.label('rank r', [((bx1 + ax0) / 2, by_ - 14, 'middle')], GREEN, SMALL, weight=600)
    f.label('trained', [(bx0 - 8, by_ + 30, 'end'), (bx0 - 8, by_ - 26, 'end')], GREEN, SMALL, weight=600)
    f.label('h = Wx + ABx', [(hb.r + 12, sy + 4, 'start')], AMBER, LABEL, weight=600, mono=True)
    f.label('trainable parameters  d·k → r(d+k):  4096 × 4096 = 16M → 131K at r = 16 (0.8%)',
            [(20, 232, 'start')], MUTED, SMALL)
    return f
