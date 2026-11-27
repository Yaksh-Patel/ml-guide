"""19 clustering: the same two moons under k-means, DBSCAN and Ward.

History: the old figure drew Ward following both moons as cleanly as DBSCAN
("follows linkage"). Running the topic's own code (make_moons(600, noise=.06,
random_state=0), standardised; KMeans(2), DBSCAN(eps=.3, min_samples=5),
AgglomerativeClustering(2, linkage='ward')) gives adjusted Rand index 0.48 for
k-means, 1.00 for DBSCAN and 0.61 for Ward: Ward minimises within-cluster
variance, which the prose calls "the closest hierarchical analogue of
k-means", and it also cuts across the moons. The old k-means boundary was a
vertical line; the real one is the perpendicular bisector of the two
centroids, a diagonal. The points below are every 4th of the 600, with the
labels from fitting all 600 (scikit-learn 1.6.1); colours are matched to the
true moon each cluster mostly covers, and a red ring marks a point put with
the other moon (DBSCAN's labels equal the true ones, ARI 1.00).
"""
from figkit import Fig, BLUE, PURPLE, RED, GREEN, FAINT, MUTED, INK, LABEL, SMALL

TARGET = ('19-clustering', 0)

# x, y (standardised), then labels for k-means, DBSCAN, Ward
DATA = """
0.36,-1.52,111;-1.12,1.11,000;0.50,-1.50,111;-0.88,1.33,000;1.01,-1.59,111;1.39,-1.12,111;
0.88,-1.62,111;0.49,-1.65,111;-0.32,-0.88,111;0.10,1.18,000;-0.47,-0.36,010;-1.45,0.73,000;
0.28,-1.60,111;0.49,-0.07,100;-1.69,-0.08,000;0.92,-1.11,111;1.61,-0.38,111;0.10,-1.16,111;
0.50,0.23,100;-0.47,-0.57,110;0.27,-1.52,111;-1.36,0.88,000;0.29,0.68,000;1.49,-0.11,111;
0.40,-1.51,111;0.55,-0.43,100;0.30,0.90,000;1.83,0.00,111;-0.50,-0.13,010;-0.19,-1.21,111;
-0.24,1.36,000;-0.11,-1.26,111;1.62,0.39,111;1.58,-0.57,111;-1.67,0.11,000;-0.87,1.32,000;
1.39,-1.03,111;0.08,-1.16,111;0.64,-1.32,111;-0.27,-1.04,111;-0.79,1.42,000;1.58,0.13,111;
0.02,-1.16,111;0.53,0.34,100;-0.40,-0.73,110;-0.19,-0.71,110;1.59,-0.31,111;-1.70,0.09,000;
-1.67,-0.41,000;-1.36,0.76,000;-1.08,1.43,000;-0.66,1.72,000;0.07,-1.30,111;-1.51,0.26,000;
0.31,0.74,000;0.64,-1.49,111;-0.64,0.65,010;-0.33,1.60,000;-1.04,1.41,000;0.52,-1.31,111;
-1.04,1.43,000;-0.62,1.51,000;0.44,0.45,000;-0.61,0.18,010;0.27,0.57,000;-1.71,-0.50,000;
-0.80,1.38,000;1.40,-1.17,111;0.38,0.58,000;-0.74,1.33,000;-1.40,1.23,000;0.45,-1.73,111;
-0.56,1.67,000;1.54,-0.49,111;0.79,-1.25,111;1.55,-0.53,111;-0.48,0.29,010;1.70,0.39,111;
0.02,-1.12,111;0.22,-1.53,111;0.71,-1.43,111;1.61,-0.11,111;-0.07,-1.01,111;-1.14,1.30,000;
1.59,-0.71,111;-0.11,-1.03,111;-1.38,0.90,000;-1.41,0.70,000;1.73,0.37,111;1.36,-0.64,111;
1.34,-0.96,111;1.23,-1.33,111;1.44,-0.82,111;-0.33,1.50,000;0.51,0.39,100;-1.19,1.22,000;
0.27,-1.60,111;1.50,-0.68,111;0.48,-0.02,100;1.19,-1.21,111;-1.27,1.00,000;-0.64,1.58,000;
-1.31,1.28,000;1.43,-0.86,111;-1.27,1.11,000;-1.76,0.30,000;-1.33,0.99,000;-0.39,1.24,000;
-1.58,0.24,000;1.37,-0.97,111;-0.54,0.04,010;-0.29,1.65,000;1.43,-1.09,111;-0.21,1.20,000;
0.34,0.17,100;-0.57,1.57,000;0.01,1.24,000;-0.46,1.44,000;-0.40,-0.35,010;1.54,-0.59,111;
0.91,-1.55,111;-1.75,-0.48,000;-1.43,0.82,000;-0.20,1.50,000;1.54,-0.05,111;1.77,0.47,111;
1.70,0.10,111;-0.56,0.55,010;0.49,0.50,000;0.35,0.40,000;-0.23,1.59,000;0.55,0.11,100;
-0.20,-0.93,111;-1.56,-0.38,000;1.83,-0.02,111;-1.41,0.96,000;0.34,0.52,000;-0.01,-1.34,111;
-0.09,1.47,000;-1.69,0.24,000;-0.11,-1.18,111;1.60,-0.52,111;0.56,-0.00,100;-0.41,1.50,000;
-1.67,0.18,000;-0.97,1.51,000;-0.27,1.23,000;0.22,1.06,000;-0.15,-1.18,111;0.46,-0.37,100
"""
CENTRES = [(-0.739, 0.78), (0.739, -0.78)]     # k-means centroids
ARI = (0.48, 1.00, 0.61)


def points():
    out = []
    for tok in DATA.replace('\n', '').split(';'):
        x, y, l = tok.split(',')
        out.append((float(x), float(y), [int(c) for c in l]))
    return out


def draw():
    f = Fig(560, 236, 'cl')
    pts = points()
    pw, ph, gap, top = 162, 136, 22, 46
    x0 = (560 - (3 * pw + 2 * gap)) / 2
    panels = []
    for k in range(3):
        px = x0 + k * (pw + gap)
        p = f.plot_area(px, top, px + pw, top + ph, (-2.0, 2.0), (-1.85, 1.95))
        panels.append(p)
        for x, y, lab in pts:
            col = BLUE if lab[k] == 0 else PURPLE
            f.circle(p.X(x), p.Y(y), 2.3, fill=col, opacity=0.9)
            if lab[k] != lab[1]:                # DBSCAN recovers the true moons exactly (ARI 1.00)
                f.circle(p.X(x), p.Y(y), 4.2, stroke=RED, width=1.1)

    # k-means: the boundary is the perpendicular bisector of the centroids (y = 0.947 x)
    p = panels[0]
    (ax, ay), (bx, by) = CENTRES
    nx, ny = bx - ax, by - ay                   # normal; the line passes through the origin
    s = -nx / ny
    xa, xb = -1.85, 1.85
    ya, yb = s * xa, s * xb
    lim = 1.85
    if abs(ya) > lim:
        xa, ya = -lim / abs(s), -lim * (1 if s > 0 else -1)
        xb, yb = -xa, -ya
    f.line(p.X(xa), p.Y(ya), p.X(xb), p.Y(yb), RED, 1.4, dash='4 4')
    for cx, cy in CENTRES:
        X, Y = p.X(cx), p.Y(cy)
        f.line(X - 4, Y - 4, X + 4, Y + 4, INK, 2)
        f.line(X - 4, Y + 4, X + 4, Y - 4, INK, 2)

    names = ('k-means', 'DBSCAN', 'Ward')
    verdict = (('cuts both moons', RED), ('follows the moons', GREEN), ('cuts them too', RED))
    for p, n, (v, col), a in zip(panels, names, verdict, ARI):
        cx = (p.x0 + p.x1) / 2
        f.label(n, [(cx, top - 16, 'middle')], INK, LABEL, weight=600)
        f.label(f'{v} · ARI {a:.2f}', [(cx, p.y1 + 22, 'middle')], col, SMALL, weight=600)
    f.label('k-means and Ward both minimise variance, so both draw compact, convex groups',
            [(280, 228, 'middle')], MUTED, SMALL)
    return f
