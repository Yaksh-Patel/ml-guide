"""24 hyperparameter tuning: nine evaluations as a 3 × 3 grid and as nine
random draws, with the score curve of the one parameter that matters on top.

The prose's argument is about projections: if only one parameter matters, a
grid spends its budget on 3 distinct values of it (each re-tested 3 times),
random search on 9. Each panel now shows that directly: every trial projects
up onto the score curve of the important parameter, and the best value tried
is ringed. The random draws are fixed (stratified on the important axis, so
the picture is typical rather than lucky) and the peak sits between grid
columns, the usual case for a grid.
"""
import math
from figkit import Fig, BLUE, GREEN, AMBER, FAINT, MUTED, BORD, LABEL, SMALL

TARGET = ('24-hyperparameter-tuning', 0)

PEAK, WID = 0.62, 0.075
GRID = [(a, b) for a in (1 / 6, 3 / 6, 5 / 6) for b in (1 / 6, 3 / 6, 5 / 6)]
RAND = [(0.05, 0.62), (0.16, 0.18), (0.27, 0.86), (0.38, 0.41), (0.49, 0.07),
        (0.61, 0.70), (0.72, 0.29), (0.83, 0.93), (0.94, 0.52)]
S, TOP, BASE, SQ0, SQ1 = 184, 40, 92, 106, 202     # panel width; strip top/base; square top/bottom


def score(u):
    return 0.08 + 0.92 * math.exp(-((u - PEAK) / WID) ** 2 / 2)


def panel(f, x0, pts, col):
    sc = f.plot_area(x0, TOP, x0 + S, BASE, (0, 1), (0, 1))
    sq = f.plot_area(x0, SQ0, x0 + S, SQ1, (0, 1), (0, 1))
    f.rect(x0, SQ0, S, SQ1 - SQ0, fill='none', stroke=BORD, r=4)
    curve = sc.curve(score, FAINT, width=1.8)
    for u in sorted({p[0] for p in pts}):          # projection of each distinct value
        top = min(sq.Y(v) for (uu, v) in pts if uu == u)
        f.line(sq.X(u), top - 6, sq.X(u), sc.Y(score(u)) + 5, col, 1, dash='2 3', opacity=0.75)
        f.circle(sq.X(u), sc.Y(score(u)), 3, fill=col)
    for u, v in pts:
        f.circle(sq.X(u), sq.Y(v), 4.2, fill=col)
    best = max(pts, key=lambda p: score(p[0]))[0]
    f.circle(sq.X(best), sc.Y(score(best)), 6.5, stroke=AMBER, width=1.8)
    return sc, sq, curve, best


def draw():
    f = Fig(560, 266, 'hp')
    gx, rx = 68, 308
    g = panel(f, gx, GRID, BLUE)
    r = panel(f, rx, RAND, GREEN)

    for (sc, sq, curve, best), x0 in ((g, gx), (r, rx)):
        f.label('important parameter →', [(x0 + S, SQ1 + 15, 'end')], FAINT, SMALL)
        f.label('best tried', [(sc.X(best) + 10, sc.Y(score(best)) - 3, 'start'),
                               (sc.X(best) - 10, sc.Y(score(best)) - 3, 'end')], AMBER, SMALL)
    f.label('score', [(gx - 8, g[0].Y(0.5) + 3, 'end')], FAINT, SMALL)
    f.label('unimportant', [(gx - 8, (SQ0 + SQ1) / 2 + 3, 'end')], FAINT, SMALL)
    f.label('grid: 3 distinct values', [(gx + S / 2, SQ1 + 34, 'middle')], BLUE, LABEL, weight=600)
    f.label('random: 9 distinct values', [(rx + S / 2, SQ1 + 34, 'middle')], GREEN, LABEL, weight=600)
    f.label('nine trials each; only the horizontal parameter moves the score',
            [(280, 258, 'middle')], MUTED, SMALL)
    return f
