"""04 chain rule: a forward pulse computes the loss, a backward pulse carries
the gradient home, multiplying in one local derivative per step.

Four stages x, W → h¹ = Wx → h² = σ(h¹) → L. Forward arrows (blue) run along
the row; backward arcs (red) run under it, each labelled with the factor it
multiplies in, so the bottom line ∂L/∂W = ∂L/∂h² · σ′(h¹) · xᵀ reads straight
off the arcs, right to left.

History: the old figure's backward arrows ended at the input x, but the
gradient that training uses is ∂L/∂W; the first box now holds x and W. Its
emoji legend is gone (direct labels instead).

Motion (one 7s clock): a blue dot runs the forward pass, lighting each box
as it lands; the loss box turns red; a red dot runs the arcs back, lighting
each box red. Hold, fade, repeat. Reduced motion shows the 6.2s frame: both
passes complete, every arrow at full strength, boxes settled.
"""
from figkit import (Fig, Anim, BLUE, RED, MUTED, INK, FAINT, BG, LABEL, SMALL, GAP,
                    quad_points)

TARGET = ('04-calculus', 0)

T = 7.0
FWD0, BWD0, HOP, STEP = 0.5, 2.9, 0.5, 0.7
FADE0, FADE1 = 6.3, 6.8


def draw():
    f = Fig(560, 172, 'chain')
    A = Anim(T)
    f.still = 6.2

    W, H, Y0 = 94, 42, 44
    xs = [22, 166, 310, 454]
    spec = [('x, W', 'input, weights'), ('h¹ = Wx', 'linear'),
            ('h² = σ(h¹)', 'activation'), ('L(h², y)', 'loss')]
    B = [f.box(x, Y0, W, H, s, sub, mono=True) for x, (s, sub) in zip(xs, spec)]

    def held(on, base=0.0):
        """opacity: base until `on`, 1 until the fade, then back to base."""
        return A.attr('opacity', [(0, base), (on - 0.01, base), (on + 0.15, 1), (FADE0, 1),
                                  (FADE1, base), (T, base)])

    def flash(t):
        """a box lights up as a pulse lands on it, then settles back."""
        return A.attr('opacity', [(0, 0), (t - 0.01, 0), (t + 0.12, 1), (t + 0.9, 1), (t + 1.3, 0), (T, 0)])

    out = []
    # forward arrows: faint at rest, full as the pulse crosses them
    fwd = []
    for i in range(3):
        a, b = B[i], B[i + 1]
        s = FWD0 + i * STEP
        f.raw(f'<g opacity=".3">{held(s, .3)}')
        f.arrow(a.r, a.cy, b.l, b.cy, BLUE, 1.8)
        f.raw('</g>')
        fwd.append(((a.r + GAP, a.cy), (b.l - GAP, b.cy), s))

    # backward arcs under the row, right to left
    bwd = []
    for j in range(3):
        a, b = B[3 - j], B[2 - j]
        p0 = (a.l + 14, a.b + GAP)
        p1 = (b.r - 14, b.b + GAP)
        c = ((p0[0] + p1[0]) / 2, a.b + 36)
        s = BWD0 + j * STEP
        f.raw(f'<g opacity=".3">{held(s, .3)}')
        f.qcurve(p0, c, p1, RED, 1.8, arrow=True)
        f.raw('</g>')
        bwd.append((p0, c, p1, s))

    # box highlights: blue when the forward pulse lands, red when the gradient does
    lands_f = [FWD0 - 0.2] + [s + HOP for (_, _, s) in fwd]
    lands_b = [s + HOP for (_, _, _, s) in reversed(bwd)] + [BWD0 - 0.3]
    for k, bx in enumerate(B):
        for col, t in ((BLUE, lands_f[k]), (RED, lands_b[k])):
            out.append(f'<rect x="{bx.x:.1f}" y="{bx.y:.1f}" width="{bx.w}" height="{bx.h}" rx="6" '
                       f'fill="none" stroke="{col}" stroke-width="1.8" opacity="0">{flash(t)}</rect>')

    # the travelling dots
    def dot(d, s, col):
        vis = A.attr('opacity', [(0, 0), (s - 0.01, 0), (s, 1), (s + HOP, 1), (s + HOP + 0.01, 0), (T, 0)])
        mv = A.motion(d, [(0, 0), (s, 0), (s + HOP, 1), (T, 1)])
        return f'<circle r="4" fill="{col}" stroke="{BG}" stroke-width="1.2" opacity="0">{vis}{mv}</circle>'

    for (p, q, s) in fwd:
        out.append(dot(f'M{p[0]:.1f},{p[1]:.1f} L{q[0]:.1f},{q[1]:.1f}', s, BLUE))
    for (p0, c, p1, s) in bwd:
        out.append(dot(f'M{p0[0]:.1f},{p0[1]:.1f} Q{c[0]:.1f},{c[1]:.1f} {p1[0]:.1f},{p1[1]:.1f}', s, RED))
    f.raw('\n'.join(out))

    # labels last
    for (p0, c, p1, _), s in zip(bwd, ('∂L/∂h²', '× σ′(h¹)', '× xᵀ')):
        apex = quad_points(p0, c, p1)[12]
        f.label(s, [(apex[0], apex[1] + 14, 'middle')], RED, SMALL, weight=600)
    f.label('forward pass: predict', [(B[0].l, Y0 - 12, 'start')], BLUE, SMALL, weight=600)
    f.label('backward pass: learn', [(B[3].r, B[3].b + 30, 'end'), (B[3].r, B[3].b + 44, 'end')], RED, SMALL, weight=600)
    f.label('∂L/∂W = ∂L/∂h² · σ′(h¹) · xᵀ', [(280, 162, 'middle')], INK, LABEL, mono=True)
    return f
