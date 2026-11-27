"""30 optimisers: SGD, momentum and Adam on the same ill-conditioned ravine.

History: the old paths were hand-drawn zig-zags. These are simulated, with
the update rules exactly as the prose writes them, on L = ½(x² + 25y²) (the
walls are 25× steeper than the floor), from (−3, 0.9), 30 steps each:
  SGD       θ ← θ − α∇L,                       α = 0.075
  momentum  v ← βv + (1−β)∇L, θ ← θ − αv,      β = 0.9, α = 0.08
  Adam      bias-corrected m/√v,               β₁ = 0.9, β₂ = 0.999, α = 0.12
SGD flips sides every step (the bounce) and has only reached x ≈ −0.29;
momentum's averaging cancels the step-to-step flip, so its path is one
smooth sway, and it reaches the minimum (x ≈ 0.08); Adam's steps are about α
per coordinate, so it heads in diagonally and then runs along the floor.

Motion (one 7.5s clock): the three paths draw themselves together with a
ball on each tip; hold, fade, repeat. Reduced motion shows the 5.8s frame:
all three paths complete.
"""
import math
from figkit import Fig, Anim, RED, AMBER, GREEN, BORD, SURF, FAINT, MUTED, BG, LABEL, SMALL

TARGET = ('30-optimizers', 0)

A, B = 1.0, 25.0
START, STEPS = (-3.0, 0.9), 30
RULES = [  # name, colour, rule, alpha, note
    ('SGD', RED, 'sgd', 0.075, 'bounces wall to wall'),
    ('momentum', AMBER, 'mom', 0.08, 'the bounce cancels, the floor builds'),
    ('Adam', GREEN, 'adam', 0.12, 'every step about α, per coordinate'),
]


def run(rule, a):
    x, y = START
    pts = [(x, y)]
    vx = vy = mx = my = sx = sy = 0.0
    for t in range(1, STEPS + 1):
        gx, gy = A * x, B * y
        if rule == 'sgd':
            x, y = x - a * gx, y - a * gy
        elif rule == 'mom':
            vx, vy = 0.9 * vx + 0.1 * gx, 0.9 * vy + 0.1 * gy
            x, y = x - a * vx, y - a * vy
        else:
            mx, my = 0.9 * mx + 0.1 * gx, 0.9 * my + 0.1 * gy
            sx, sy = 0.999 * sx + 0.001 * gx * gx, 0.999 * sy + 0.001 * gy * gy
            c1, c2 = 1 - 0.9 ** t, 1 - 0.999 ** t
            x -= a * (mx / c1) / (math.sqrt(sx / c2) + 1e-8)
            y -= a * (my / c1) / (math.sqrt(sy / c2) + 1e-8)
        pts.append((x, y))
    return pts


def draw():
    f = Fig(560, 196, 'opt')
    PW, PH, GAP, PX0, PY = 170, 104, 10, 10, 14
    XR, YR = (-3.35, 0.95), (-1.15, 1.15)
    sc = (PW - 14) / (XR[1] - XR[0])            # px per unit, same on both axes
    T = Anim(7.5)
    t0, t1 = 0.5, 5.0
    f.still = 5.8
    f.raw('<defs>' + ''.join(
        f'<clipPath id="opt-cp{k}"><rect x="{PX0 + k * (PW + GAP)}" y="{PY}" width="{PW}" height="{PH}" rx="7"/></clipPath>'
        for k in range(3)) + '</defs>')
    moving = []
    for k, (name, col, rule, a, note) in enumerate(RULES):
        px = PX0 + k * (PW + GAP)
        cx = px + 7 - XR[0] * sc                 # canvas x of the minimum
        cy = PY + PH / 2
        X = lambda v: cx + v * sc
        Y = lambda v: cy - v * sc
        f.rect(px, PY, PW, PH, SURF, BORD, 7)
        rings = ''.join(
            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{math.sqrt(2 * c / A) * sc:.1f}" ry="{math.sqrt(2 * c / B) * sc:.1f}" '
            f'fill="none" stroke="{BORD}" stroke-width="1"/>' for c in (0.15, 0.7, 1.8, 3.4, 5.4))
        pts = [(X(x), Y(y)) for x, y in run(rule, a)]
        d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        f.raw(f'<g clip-path="url(#opt-cp{k})">{rings}</g>')
        f.circle(cx, cy, 4, stroke=GREEN, width=1.6)                    # minimum
        f.circle(*pts[0], 3.5, fill=AMBER, stroke=BG, width=1.2)        # start
        moving.append(
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.8" stroke-linejoin="round" '
            f'stroke-linecap="butt" pathLength="1" stroke-dasharray="1 1" clip-path="url(#opt-cp{k})">'
            f'{T.attr("stroke-dashoffset", [(0, 1), (t0, 1), (t1, 0), (7.5, 0)], spline=True)}</path>'
            f'<circle r="4" fill="{col}" stroke="{BG}" stroke-width="1.2">'
            f'{T.motion(d, [(0, 0), (t0, 0), (t1, 1), (7.5, 1)])}</circle>')
        f.label(name, [(px + PW / 2, PY + PH + 18, 'middle')], col, LABEL, weight=600)
        f.label(note, [(px + PW / 2, PY + PH + 32, 'middle')], MUTED, SMALL)
    f.raw(f'<g>{T.attr("opacity", [(0, 1), (6.6, 1), (7.1, 0), (7.5, 0)])}' + ''.join(moving) + '</g>')
    f.label('same ravine, same start, 30 steps each; the ring marks the minimum',
            [(280, PY + PH + 54, 'middle')], FAINT, SMALL)
    return f
