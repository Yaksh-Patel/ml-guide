"""17 gradient boosting: each tree removes a fraction η of what is left, so the
residual decays geometrically, and halving η doubles the trees needed.

History: the old figure showed three sine waves labelled "residual amplitude
1.00 / 0.45 / 0.10" at rounds 1 / 5 / 50. Those numbers fit no single learning
rate (0.45 after four rounds needs η ≈ 0.18; 0.10 after 49 needs η ≈ 0.046)
and appear nowhere in the prose. The prose's own model is that (1 − η) of the
error survives each round, with the table η = 0.10 → 29 rounds and η = 0.05 →
59 rounds to remove 95%. The figure now draws exactly that: residual stems
shrinking by 0.9 per tree, and both decay curves (1 − η)^m reaching the 5%
line at m = 29 and m = 59.

Motion (one 8s clock): the red residual stems shrink tree by tree from m = 0
to m = 29 while an amber marker rides the η = 0.1 curve in step; hold, fade,
repeat. Reduced motion shows the 6.6s frame: m = 29, residuals almost gone
against the grey m = 0 outline, marker on the 5% line.
"""
from figkit import Fig, Anim, BLUE, PURPLE, AMBER, RED, FAINT, MUTED, BG, LABEL, SMALL

TARGET = ('17-gradient-boosting', 0)

R0 = [0.55, -0.80, 0.30, 0.95, -0.45, -0.70, 0.65, 0.20, -0.95, 0.50, -0.30, 0.85]
ETA, M = 0.1, 29
T = 8.0
T0, T1 = 0.7, 6.0          # m = 0 at T0, m = 29 at T1
FADE = 7.3


def draw():
    f = Fig(560, 282, 'gb')
    A = Anim(T)
    f.still = 6.6
    times = [T0 + (T1 - T0) * m / M for m in range(M + 1)]
    shrink = [(1 - ETA) ** m for m in range(M + 1)]

    # ---- left: residual per row ---------------------------------------------------
    lx0, lx1, ly0, amp = 44, 236, 132, 72
    f.line(lx0 - 6, ly0, lx1 + 6, ly0, FAINT, 1, dash='3 4')
    step = (lx1 - lx0) / (len(R0) - 1)
    xs = [lx0 + i * step for i in range(len(R0))]
    for x, r in zip(xs, R0):                      # m = 0 outline
        y = ly0 - r * amp
        f.line(x, ly0, x, y, FAINT, 1.2)
        f.circle(x, y, 3.2, fill=BG, stroke=FAINT, width=1.2)

    live = [f'<g>{A.attr("opacity", [(0, 0), (0.3, 1), (FADE, 1), (FADE + 0.4, 0), (T, 0)])}']
    for x, r in zip(xs, R0):
        ys = [ly0 - r * amp * s for s in shrink]
        pairs = [(0, ys[0])] + [(t, y) for t, y in zip(times, ys)] + [(T, ys[-1])]
        anim = A.attr('y2', [(t, f'{y:.1f}') for t, y in pairs])
        animc = A.attr('cy', [(t, f'{y:.1f}') for t, y in pairs])
        live.append(f'<line x1="{x:.1f}" y1="{ly0}" x2="{x:.1f}" y2="{ys[-1]:.1f}" stroke="{RED}" '
                    f'stroke-width="2.6" stroke-linecap="round">{anim}</line>')
        live.append(f'<circle cx="{x:.1f}" cy="{ys[-1]:.1f}" r="3.4" fill="{RED}">{animc}</circle>')
    live.append('</g>')
    f.raw('\n'.join(live))

    # ---- right: share of error left vs trees ---------------------------------------
    p = f.plot_area(296, 46, 520, 214, (0, 64), (0, 1.0))
    p.axes(ylabel='error left')
    thr = 0.05
    f.line(p.X(0), p.Y(thr), p.X(64), p.Y(thr), AMBER, 1.1, dash='3 4')
    slow = p.curve(lambda m: 0.95 ** m, PURPLE, width=2.4)
    fast = p.curve(lambda m: 0.90 ** m, BLUE, width=2.4)
    for m, col in ((29, BLUE), (59, PURPLE)):
        x = p.X(m)
        f.line(x, p.Y(thr) + 5, x, p.Y(0), col, 1, dash='2 3')
        f.circle(x, p.Y(0.95 ** m if col == PURPLE else 0.9 ** m), 3.6, fill=col, stroke=BG, width=1.2)

    # the marker, in step with the stems
    mk = [(0, p.X(0), p.Y(1))] + [(t, p.X(m), p.Y(shrink[m])) for m, t in enumerate(times)] + \
         [(T, p.X(M), p.Y(shrink[M]))]
    cx = A.attr('cx', [(t, f'{x:.1f}') for t, x, _ in mk])
    cy = A.attr('cy', [(t, f'{y:.1f}') for t, _, y in mk])
    op = A.attr('opacity', [(0, 0), (0.3, 1), (FADE, 1), (FADE + 0.4, 0), (T, 0)])
    f.raw(f'<circle cx="{p.X(M):.1f}" cy="{p.Y(shrink[M]):.1f}" r="6.5" fill="none" stroke="{AMBER}" '
          f'stroke-width="2.2">{cx}{cy}{op}</circle>')

    # ---- labels last ----------------------------------------------------------------
    f.label('residual  yᵢ − F(xᵢ)', [(lx0 - 6, p.y0 - 10, 'start')], RED, LABEL, weight=600)
    i3 = 3
    f.label('m = 0', [(xs[i3] + 8, ly0 - R0[i3] * amp + 3, 'start')], FAINT, SMALL)
    f.label('rows i →', [((lx0 + lx1) / 2, p.Y(0) + 30, 'middle')], FAINT, SMALL)
    f.label('trees m →', [((p.x0 + p.x1) / 2, p.Y(0) + 30, 'middle')], FAINT, SMALL)
    # right of the steep part of the blue curve, in the gap before the purple one
    f.label('η = 0.1 · 29 trees', [(p.X(29), p.Y(0) + 15, 'middle')], BLUE, SMALL, weight=600)
    f.label('η = 0.05 · 59 trees', [(p.X(59), p.Y(0) + 15, 'middle'), (p.X(64) + 14, p.Y(0) + 15, 'end')],
            PURPLE, SMALL, weight=600)
    f.label('5% left', [(p.X(1.5), p.Y(thr) - 6, 'start'), (p.X(64) + 14, p.Y(thr) + 3, 'start')], AMBER, SMALL)
    f.label('each tree keeps (1 − η) of the error: halve η, double the trees',
            [(280, 272, 'middle')], MUTED, SMALL)
    return f
