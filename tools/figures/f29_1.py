"""29 gradient descent: steps down a loss bowl, shrinking as the slope flattens.

The old figure drew the loss as a hill and walked the steps UP to its peak,
labelled θ*. Gradient descent minimises: the curve is a bowl and θ* is the
bottom. On a quadratic each step multiplies the distance to θ* by (1 − 2kα),
so the steps shrink geometrically — that is what is drawn.
"""
from figkit import Fig, BLUE, GREEN, AMBER, RED, FAINT, MUTED, LABEL, SMALL

TARGET = ('29-backpropagation', 1)

TSTAR, K, C = 0.66, 2.1, 0.08
ALPHA = 0.11          # 1 - 2·K·ALPHA = 0.538: each step keeps ~54% of the distance


def loss(t):
    return K * (t - TSTAR) ** 2 + C


def grad(t):
    return 2 * K * (t - TSTAR)


def draw():
    f = Fig(560, 300, 'gd')
    p = f.plot_area(56, 40, 520, 246, (0, 1), (0, 1.05))
    p.axes(xlabel='parameter θ →', ylabel='loss L(θ)')
    p.curve(loss, BLUE, width=2.6)
    f.text(p.X(0.97), p.Y(loss(0.97)) - 12, 'L(θ)', BLUE, LABEL, anchor='middle', weight=600)

    # the minimum
    xs, ys = p.X(TSTAR), p.Y(loss(TSTAR))
    f.line(xs, ys + 8, xs, p.Y(0), GREEN, 1.2, dash='4 4')
    f.circle(xs, ys, 5, fill=GREEN)
    f.text(xs, p.Y(0) + 18, 'θ*  (minimum)', GREEN, SMALL, anchor='middle', weight=600)

    # the iterates
    t = 0.07
    pts = [t]
    for _ in range(5):
        t = t - ALPHA * grad(t)
        pts.append(t)
    # each step as a hop above the curve, so it never lies on top of it
    for a, b in zip(pts, pts[1:]):
        x1, y1, x2, y2 = p.X(a), p.Y(loss(a)), p.X(b), p.Y(loss(b))
        lift = min(28, 0.35 * abs(x2 - x1))
        cx, cy = (x1 + x2) / 2, min(y1, y2) - lift
        f.raw(f'<path d="M{x1:.1f},{y1 - 7:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2 - 7:.1f}" fill="none" '
              f'stroke="{RED}" stroke-width="1.8" marker-end="url(#{f.marker(RED)})" opacity=".9"/>')
    for i, t in enumerate(pts):
        f.circle(p.X(t), p.Y(loss(t)), 5 if i == 0 else 4, fill=AMBER, stroke='#0b0d12', width=1.5)
    f.text(p.X(pts[0]) - 10, p.Y(loss(pts[0])) + 4, 'θ₀', AMBER, LABEL, anchor='end', weight=600)

    # the two regimes the prose names
    a, b = pts[0], pts[1]
    mx, my = (p.X(a) + p.X(b)) / 2, (p.Y(loss(a)) + p.Y(loss(b))) / 2
    f.text(mx + 4, my - 40, 'steep slope → big step', RED, SMALL)
    c = pts[3]
    f.text(p.X(c) + 10, p.Y(loss(c)) - 46, 'flat near the bottom → small steps', RED, SMALL, anchor='middle')
    f.text(p.X(0.04), p.Y(0) + 18, 'step:  θ ← θ − α·∇L(θ)', MUTED, SMALL, mono=True)
    return f
