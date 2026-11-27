"""29 gradient descent: a ball hops down a loss bowl, steps shrinking as the
slope flattens.

History: the original figure drew the loss as a hill and walked the steps UP
to its peak (labelled θ*), though it did animate the steps in. Gradient
descent minimises: the curve is a bowl and θ* is the bottom. On a quadratic
each step keeps (1 − 2kα) of the distance to θ*, so the hops shrink
geometrically, which is the point the animation makes.

Motion (one 7s clock): the ball hops from θ₀ to each iterate, each hop's arc
draws itself under it, a dot stays where it landed; hold, fade, repeat.
Reduced motion shows the 5.6s frame: every hop drawn, ball at the last one.
"""
from figkit import (Fig, Anim, BLUE, GREEN, AMBER, RED, FAINT, MUTED, BG, LABEL, SMALL,
                    quad_points, polyline_length)

TARGET = ('29-backpropagation', 1)

TSTAR, K, C = 0.66, 2.1, 0.08
ALPHA = 0.11          # 1 - 2·K·ALPHA = 0.538: each step keeps ~54% of the distance
STEPS = 5


def loss(t):
    return K * (t - TSTAR) ** 2 + C


def grad(t):
    return 2 * K * (t - TSTAR)


def draw():
    f = Fig(560, 290, 'gd')
    p = f.plot_area(56, 40, 520, 236, (0, 1), (0, 1.05))
    p.axes(xlabel='parameter θ →', ylabel='loss L(θ)')
    bowl = p.curve(loss, BLUE, width=2.6)

    # the minimum
    xs, ys = p.X(TSTAR), p.Y(loss(TSTAR))
    f.line(xs, ys + 8, xs, p.Y(0), GREEN, 1.2, dash='4 4')
    f.circle(xs, ys, 5, fill=GREEN)

    # the iterates and the hops between them (lifted above the curve)
    ts = [0.07]
    for _ in range(STEPS):
        ts.append(ts[-1] - ALPHA * grad(ts[-1]))
    P = [(p.X(t), p.Y(loss(t))) for t in ts]
    hops = []
    for (x1, y1), (x2, y2) in zip(P, P[1:]):
        lift = max(10, min(34, 0.38 * abs(x2 - x1)))
        c = ((x1 + x2) / 2, min(y1, y2) - lift)
        hops.append(((x1, y1 - 6), c, (x2, y2 - 6)))
    lens = [polyline_length(quad_points(*h)) for h in hops]
    total = sum(lens)

    A = Anim(7.0)
    t0, hop, pause = 0.5, 0.72, 0.16
    times = [t0 + i * (hop + pause) for i in range(STEPS)]    # start of hop i
    end_all = times[-1] + hop
    f.still = round(end_all + 0.4, 2)

    g = [f'<g>{A.attr("opacity", [(0, 1), (6.2, 1), (6.7, 0), (7, 0)])}']
    # arcs: each draws itself during its hop
    for i, h in enumerate(hops):
        (a, b), (cx, cy), (x2, y2) = h
        s, e = times[i], times[i] + hop
        g.append(f'<path d="M{a:.1f},{b:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="{RED}" '
                 f'stroke-width="1.8" stroke-linecap="butt" pathLength="1" stroke-dasharray="1 1" opacity=".85">'
                 f'{A.attr("stroke-dashoffset", [(0, 1), (s, 1), (e, 0), (7, 0)], spline=True)}</path>')
        f.segs += list(zip(quad_points(*h), quad_points(*h)[1:]))
    # landing dots
    for i, (x, y) in enumerate(P[1:]):
        land = times[i] + hop
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{AMBER}" stroke="{BG}" stroke-width="1.2">'
                 f'{A.attr("opacity", [(0, 0), (land - 0.02, 0), (land, 1), (7, 1)])}</circle>')
        f.segs += [((x - 4, y - 4), (x + 4, y + 4))]
    # the ball, travelling along all hops in turn
    d = f'M{hops[0][0][0]:.1f},{hops[0][0][1]:.1f} ' + ' '.join(
        f'Q{c[0]:.1f},{c[1]:.1f} {e[0]:.1f},{e[1]:.1f}' for (_, c, e) in hops)
    pairs, acc = [(0, 0.0), (times[0], 0.0)], 0.0
    for i, L in enumerate(lens):
        acc += L / total
        pairs.append((times[i] + hop, min(acc, 1.0)))
        if i < STEPS - 1:
            pairs.append((times[i + 1], min(acc, 1.0)))
    pairs.append((7.0, 1.0))
    g.append(f'<circle r="6" fill="{AMBER}" stroke="{BG}" stroke-width="1.5">{A.motion(d, pairs)}</circle>')
    g.append('</g>')
    f.raw('\n'.join(g))

    # the start point stays put, outside the fading group
    f.circle(*P[0], 5, fill=AMBER, stroke=BG, width=1.5)

    # labels last
    f.label('θ₀', [(P[0][0] - 10, P[0][1] + 4, 'end'), (P[0][0], P[0][1] + 20, 'middle')], AMBER, LABEL, weight=600)
    f.label('θ*  (minimum)', [(xs, p.Y(0) + 18, 'middle')], GREEN, SMALL, weight=600)
    f.along(bowl, 'L(θ)', [0.96, 0.92], fill=BLUE, size=LABEL, weight=600)
    mx = (P[0][0] + P[1][0]) / 2
    f.label('steep slope → big step', [(mx + 10, hops[0][1][1] - 2, 'start'), (mx, hops[0][1][1] - 10, 'middle')], RED)
    c3 = hops[3][1]
    f.label('flat near the bottom → small steps',
            [(c3[0] - 10, c3[1] - 30, 'middle'), (c3[0] + 10, c3[1] - 44, 'middle'), (c3[0], c3[1] - 58, 'middle')], RED)
    f.label('step:  θ ← θ − α·∇L(θ)', [(p.X(0.02), p.Y(0) + 18, 'start')], MUTED, mono=True)
    return f
