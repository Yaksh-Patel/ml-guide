"""12 KNN: the decision boundary at k = 1, 15 and n on the same 30 points.

Every boundary and every tinted region here is computed: each panel runs
k-nearest-neighbour voting on a fine grid over the same 30 labelled points
(two of them on the wrong side of the true boundary), tints each cell by the
predicted class, and traces the 50% contour.

History: the old figure drew the three boundaries by hand — a random zig-zag
for k = 1, a sine for k = 15, and a horizontal line for k = n. A k = n model
has no boundary at all: every query averages the whole dataset and predicts
the majority class everywhere, which is what the prose says. That panel is
now one colour with no line.
"""
import math, random
from figkit import Fig, BLUE, PURPLE, AMBER, INK, MUTED, BG, BORD, LABEL, SMALL

TARGET = ('12-knn', 0)
N = 30


MID, AMP = 0.47, 0.16
NOISE = [(0.50, 0.20, True), (0.64, 0.76, False)]   # deep on the wrong side
SEED = 18


def edge(x):
    return MID + AMP * math.sin(2 * math.pi * (x - 0.15))


def points(seed=SEED):
    rnd = random.Random(seed)
    pts = list(NOISE)
    while len(pts) < N:
        x, y = 0.03 + 0.94 * rnd.random(), 0.04 + 0.92 * rnd.random()
        if abs(y - edge(x)) < 0.06:          # keep a clear margin round the true boundary
            continue
        if any(math.dist((x, y), (a, b)) < 0.095 for a, b, _ in pts):
            continue
        pts.append((x, y, y > edge(x)))
    return pts


def predict(pts, k, x, y):
    """Signed score: > 0 means class True (blue)."""
    ds = sorted((math.dist((x, y), (a, b)), c) for a, b, c in pts)
    if k == 1:
        db = next(d for d, c in ds if c)
        dp = next(d for d, c in ds if not c)
        return dp - db                       # zero set = the 1-NN boundary
    votes = sum(1 if c else -1 for _, c in ds[:k])
    return votes / k


def contour(F, xs, ys):
    """Marching squares: zero contour of F[j][i] as joined polylines."""
    segs = []
    for j in range(len(ys) - 1):
        for i in range(len(xs) - 1):
            c = [(xs[i], ys[j], F[j][i]), (xs[i + 1], ys[j], F[j][i + 1]),
                 (xs[i + 1], ys[j + 1], F[j + 1][i + 1]), (xs[i], ys[j + 1], F[j + 1][i])]
            cr = []
            for a, b in zip(c, c[1:] + c[:1]):
                if (a[2] > 0) != (b[2] > 0):
                    t = a[2] / (a[2] - b[2])
                    cr.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
            if len(cr) == 2:
                segs.append(tuple(cr))
            elif len(cr) == 4:
                segs += [(cr[0], cr[1]), (cr[2], cr[3])]
    key = lambda p: (round(p[0], 4), round(p[1], 4))
    ends = {}
    for s in segs:
        for p in s:
            ends.setdefault(key(p), []).append(s)
    used, lines = set(), []
    for s in segs:
        if id(s) in used:
            continue
        used.add(id(s))
        line = [s[0], s[1]]
        for grow in (0, 1):
            while True:
                tip = line[-1]
                nxt = [t for t in ends[key(tip)] if id(t) not in used]
                if not nxt:
                    break
                t = nxt[0]
                used.add(id(t))
                line.append(t[1] if key(t[0]) == key(tip) else t[0])
            line.reverse()
        lines.append(line)
    return lines


def chaikin(pts, n=2):
    closed = math.dist(pts[0], pts[-1]) < 1e-6
    for _ in range(n):
        out = [pts[0]] if not closed else []
        for a, b in zip(pts, pts[1:]):
            out += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]),
                    (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        if closed:
            out.append(out[0])
        else:
            out.append(pts[-1])
        pts = out
    return pts


def smooth_ma(pts, r=3):
    """Moving average (endpoints kept): takes the grid staircase out of a
    contour of the piecewise-constant vote field."""
    closed = math.dist(pts[0], pts[-1]) < 1e-6
    n, out = len(pts), []
    for i in range(n):
        lo, hi = max(0, i - r), min(n, i + r + 1)
        if not closed and (i == 0 or i == n - 1):
            out.append(pts[i]); continue
        w = pts[lo:hi]
        out.append((sum(p[0] for p in w) / len(w), sum(p[1] for p in w) / len(w)))
    return out


def blur(F, r=3):
    """Box blur of the vote field over a few grid cells (a few units on the
    page): removes the grid staircase and one-cell specks, so the tint and
    the traced boundary agree. The sign — the prediction — is unchanged
    except within a couple of units of the boundary."""
    ny, nx = len(F), len(F[0])
    H = [[sum(F[j][max(0, i - r):i + r + 1]) / len(F[j][max(0, i - r):i + r + 1]) for i in range(nx)] for j in range(ny)]
    return [[sum(H[jj][i] for jj in range(max(0, j - r), min(ny, j + r + 1))) / (min(ny, j + r + 1) - max(0, j - r))
             for i in range(nx)] for j in range(ny)]


def panel(f, pts, k, x0, y0, w, h, idx, step=1.5):
    pad = 8                         # points stay this far inside the panel
    X = lambda u: x0 + pad + u * (w - 2 * pad)
    Y = lambda v: y0 + h - pad - v * (h - 2 * pad)
    # the grid covers the whole panel, not just the padded data area
    ua, ub = -pad / (w - 2 * pad), 1 + pad / (w - 2 * pad)
    va, vb = -pad / (h - 2 * pad), 1 + pad / (h - 2 * pad)
    nx, ny = int(w / step), int(h / step)
    us = [ua + (ub - ua) * i / nx for i in range(nx + 1)]
    vs = [va + (vb - va) * j / ny for j in range(ny + 1)]
    du, dv = (ub - ua) / nx, (vb - va) / ny
    F = [[predict(pts, k, u, v) for u in us] for v in vs]
    if k > 1:
        F = blur(blur(F))
    cid = f'{f.fid}-clip{idx}'
    f.raw(f'<clipPath id="{cid}"><rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="6"/></clipPath>'
          f'<g clip-path="url(#{cid})">')
    # tint: one path per class, horizontal runs of grid cells (cells centred on grid nodes)
    for cls, col in ((True, BLUE), (False, PURPLE)):
        d = []
        for j, v in enumerate(vs):
            i = 0
            while i < len(us):
                if (F[j][i] > 0) == cls:
                    s = i
                    while i < len(us) and (F[j][i] > 0) == cls:
                        i += 1
                    xa = X(us[s] - du / 2) - 0.2; xb = X(us[i - 1] + du / 2) + 0.2
                    ya = Y(v + dv / 2) - 0.3; yb = Y(v - dv / 2) + 0.3
                    d.append(f'M{xa:.1f},{ya:.1f}H{xb:.1f}V{yb:.1f}H{xa:.1f}z')
                else:
                    i += 1
        if d:
            f.raw(f'<path d="{"".join(d)}" fill="{col}" opacity=".13"/>')
    # boundary
    for line in contour(F, us, vs):
        if len(line) < 3:
            continue
        if k > 1:
            line = smooth_ma(line)
        f.path([(X(u), Y(v)) for u, v in chaikin(line)], AMBER, 1.9)
    f.raw('</g>')
    f.rect(x0, y0, w, h, fill='none', stroke=BORD, r=6)
    for u, v, c in pts:
        f.circle(X(u), Y(v), 3.3, fill=BLUE if c else PURPLE, stroke=BG, width=1)


def draw():
    pts = points()
    f = Fig(560, 180, 'knn')
    W, H, G, X0, Y0 = 168, 128, 14, 13, 8
    specs = [(1, 'k = 1', 'an island round every noisy point'),
             (15, 'k = 15', 'smooth boundary'),
             (N, f'k = n = {N}', 'no boundary: majority everywhere')]
    for i, (k, name, sub) in enumerate(specs):
        x = X0 + i * (W + G)
        panel(f, pts, k, x, Y0, W, H, i)
        f.text(x + W / 2, Y0 + H + 20, name, INK, LABEL, 'middle', weight=600)
        f.text(x + W / 2, Y0 + H + 34, sub, MUTED, SMALL, 'middle')
    return f

