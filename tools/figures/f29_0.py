"""29 backprop on a computation graph: a forward pass, then δ handed back down.

Three tiers, one per kind of quantity: the forward row (values, blue
arrows), the gradient row under it (red, flowing right to left, each arrow
labelled with the local derivative it multiplies in), and the weight
gradients (amber) branching off δ² and δ¹. Labels sit under their arrows
instead of on top of arrows and boxes.

History: the old figure labelled the first backward arrow ∂L/∂ŷ = ŷ − y and
then multiplied by σ′(z²), which would make δ² = (ŷ − y)·σ′(z²). The topic's
worked example uses BCE with a sigmoid output, where ∂L/∂ŷ = (ŷ − y)/(ŷ(1 − ŷ))
and the σ′ factor cancels it: δ² = ŷ − y. The gradient row now says exactly
that (∂L/∂ŷ, × σ′(z²), δ² = ŷ − y). The 𝟙(z¹ > 0) factor is written ReLU′(z¹).

Motion (one 9s clock): the forward arrows draw left to right and each value
box lights as it is computed (0.3–2.7s); the loss turns the signal round,
then the red arrows draw right to left, each gradient node appearing as δ
reaches it, and the amber weight gradients branch off as soon as their δ
exists (3.0–5.9s). Hold, fade, repeat. Reduced motion shows the 7s frame:
every arrow, node and gradient drawn.
"""
import math
from figkit import Fig, Anim, BLUE, RED, AMBER, INK, BORD, GAP, LABEL, SMALL, quad_points

TARGET = ('29-backpropagation', 0)

T = 9.0
FADE = 8.0
Y1, Y2, BH = 62, 138, 28            # forward row, gradient row, box height

# (label, width) for the forward row; x positions packed with equal gaps
FWD = [('x', 34), ('z¹ = W¹x + b¹', 76), ('h = ReLU(z¹)', 72), ('z² = W²h + b²', 76), ('ŷ = σ(z²)', 60), ('L(ŷ, y)', 50)]
MARGIN = 20


def layout(w):
    gap = (w - 2 * MARGIN - sum(b for _, b in FWD)) / (len(FWD) - 1)
    xs, x = [], MARGIN
    for _, bw in FWD:
        xs.append(x)
        x += bw + gap
    return xs


def timeline(A, on, off=None):
    """opacity 0 until `on`, then 1 until the fade."""
    return A.attr('opacity', [(0, 0), (on - 0.01, 0), (on + 0.15, 1), (FADE, 1), (FADE + 0.5, 0), (T, 0)])


def draw_arrow(f, A, p, q, col, s, e, width=1.6):
    """A straight arrow that draws itself from p to q over [s, e]; the head pops in at e."""
    d = math.dist(p, q)
    ux, uy = (q[0] - p[0]) / d, (q[1] - p[1]) / d
    mk = f.marker(col)
    f.raw(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{col}" '
          f'stroke-width="{width}" pathLength="1" stroke-dasharray="1 1" stroke-linecap="butt">'
          f'{A.attr("stroke-dashoffset", [(0, 1), (s, 1), (e, 0), (FADE, 0), (FADE + 0.5, 1), (T, 1)], spline=True)}</line>'
          f'<line x1="{q[0] - ux:.1f}" y1="{q[1] - uy:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{col}" '
          f'stroke-width="{width}" marker-end="url(#{mk})">{timeline(A, e)}</line>',
          pts=[p, q])


def draw_curve(f, A, p0, c, p1, col, s, e, width=1.6):
    pts = quad_points(p0, c, p1)
    ux, uy = p1[0] - c[0], p1[1] - c[1]
    n = math.hypot(ux, uy)
    ux, uy = ux / n, uy / n
    mk = f.marker(col)
    f.raw(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} Q{c[0]:.1f},{c[1]:.1f} {p1[0]:.1f},{p1[1]:.1f}" fill="none" '
          f'stroke="{col}" stroke-width="{width}" pathLength="1" stroke-dasharray="1 1" stroke-linecap="butt">'
          f'{A.attr("stroke-dashoffset", [(0, 1), (s, 1), (e, 0), (FADE, 0), (FADE + 0.5, 1), (T, 1)], spline=True)}</path>'
          f'<line x1="{p1[0] - ux:.1f}" y1="{p1[1] - uy:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" stroke="{col}" '
          f'stroke-width="{width}" marker-end="url(#{mk})">{timeline(A, e)}</line>',
          pts=pts)


def draw():
    W = 560
    f = Fig(W, 248, 'bp')
    A = Anim(T)
    f.still = 7.0
    xs = layout(W)

    # forward row: static boxes, each lights (blue tint) when its value is computed
    fwd = []
    f_start = [0.3 + 0.5 * i for i in range(5)]           # arrow i: box i -> box i+1
    f_end = [s + 0.4 for s in f_start]
    lit = [0.2] + f_end
    for (lab, bw), x, on in zip(FWD, xs, lit):
        b = f.box(x, Y1 - BH / 2, bw, BH, lab, stroke=BORD, color=INK, size=LABEL, weight=None)
        f.raw(f'<rect x="{x:.1f}" y="{Y1 - BH / 2:.1f}" width="{bw}" height="{BH}" rx="6" fill="{BLUE}" '
              f'stroke="{BLUE}" stroke-width="1.2" fill-opacity=".14" opacity="0">{timeline(A, on)}</rect>')
        fwd.append(b)
    for i in range(5):
        a, b = fwd[i], fwd[i + 1]
        draw_arrow(f, A, (a.r + GAP, Y1), (b.l - GAP, Y1), BLUE, f_start[i], f_end[i])

    # gradient row, under ŷ, z², h, z¹ (columns 4, 3, 2, 1)
    G = {4: '∂L/∂ŷ', 3: 'δ² = ŷ − y', 2: '∂L/∂h', 1: 'δ¹'}
    g_on = {4: 3.5, 3: 4.1, 2: 4.7, 1: 5.3}
    grad = {}
    for col, lab in G.items():
        x, bw = xs[col], FWD[col][1]
        f.raw(f'<g opacity="0">{timeline(A, g_on[col])}')
        grad[col] = f.box(x, Y2 - BH / 2, bw, BH, lab, stroke=RED, color=RED, size=LABEL, weight=None)
        f.raw('</g>')

    # loss turns the signal round: L (bottom) -> ∂L/∂ŷ (right side)
    Lb, gy = fwd[5], grad[4]
    p0 = (Lb.cx, Lb.b + GAP)
    p1 = (gy.r + GAP, Y2)
    draw_curve(f, A, p0, (Lb.cx, Y2), p1, RED, 3.0, 3.5)

    # backward arrows (right to left) and their local factors
    back = [(4, 3, '× σ′(z²)', 3.7), (3, 2, '× W²ᵀ', 4.3), (2, 1, '⊙ ReLU′(z¹)', 4.9)]
    for a, b, lab, s in back:
        A_, B_ = grad[a], grad[b]
        draw_arrow(f, A, (A_.l - GAP, Y2), (B_.r + GAP, Y2), RED, s, s + 0.4)

    # weight gradients branch off δ² and δ¹
    WG = [(3, '∂L/∂W² = δ² hᵀ', 4.3), (1, '∂L/∂W¹ = δ¹ xᵀ', 5.5)]
    wy = 196
    for col, lab, s in WG:
        g = grad[col]
        draw_arrow(f, A, (g.cx, g.b + GAP), (g.cx, wy - 12), AMBER, s, s + 0.4)

    # labels last: the animated ones are wrapped so they appear with their arrow
    for a, b, lab, s in back:
        mx = (grad[a].l + grad[b].r) / 2
        f.raw(f'<g opacity="0">{timeline(A, s + 0.4)}')
        f.label(lab, [(mx, Y2 + BH / 2 + 15, 'middle')], RED, SMALL, pad=2)
        f.raw('</g>')
    for col, lab, s in WG:
        f.raw(f'<g opacity="0">{timeline(A, s + 0.4)}')
        f.label(lab, [(grad[col].cx, wy, 'middle')], AMBER, SMALL, pad=2)
        f.raw('</g>')
    f.label('forward pass', [(MARGIN, 30, 'start')], BLUE, SMALL, weight=600)
    f.label('backward pass', [(MARGIN, Y2 + 3, 'start')], RED, SMALL, weight=600)
    f.label('Each layer multiplies δ by its local derivative and hands it down; weight gradients branch off it.',
            [(W / 2, 236, 'middle')], INK, SMALL)
    return f
