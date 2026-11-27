"""41 vector databases: what turning ef buys, and the three HNSW knobs.

Recall@10 climbs fast and flattens below exact search (1.0) as the query
width ef grows; latency keeps climbing with it. The curve starts at ef = k,
because ef below k cannot return k neighbours. Tick marks are the ef values
the code below the figure sweeps (10, 50, 200). The knobs card on the right
replaces the old two-column table whose long names ran into their notes.
"""
import math
from figkit import Fig, BLUE, GREEN, AMBER, RED, FAINT, MUTED, INK, BORD, LABEL, SMALL, TINY

TARGET = ('41-vector-databases', 0)
K = 10
EF_MAX = 250


def recall(ef):
    return 0.955 - 0.56 * math.exp(-(ef - K) / 30)


def latency(ef):           # drawn on the same 0..1 frame, roughly linear in ef
    return 0.07 + 0.82 * (ef - K) / (EF_MAX - K)


def draw():
    f = Fig(560, 262, 'vdb')
    p = f.plot_area(52, 44, 300, 214, (0, EF_MAX), (0, 1.08))
    p.axes(xlabel='ef →')
    f.text(p.x0 + 8, p.y0 - 10, 'recall@10', GREEN, SMALL, weight=600)

    # exact search ceiling
    ex = [(p.X(0), p.Y(1)), (p.X(EF_MAX), p.Y(1))]
    f.path(ex, FAINT, 1.1, dash='3 4')

    # ef >= k floor
    xk = p.X(K)
    f.line(xk, p.Y(0), xk, p.Y(1) + 6, AMBER, 1.2, dash='3 3')

    lat = p.curve(latency, RED, width=2.2, dash='5 4', xr=(K, EF_MAX))
    rec = p.curve(recall, GREEN, width=2.8, xr=(K, EF_MAX))

    for ef in (50, 200):
        x = p.X(ef)
        f.line(x, p.y1, x, p.y1 + 4, FAINT, 1.1)
    f.circle(*rec[0], 3.5, fill=GREEN)

    # knobs card
    cx, cy, cw, ch = 334, 40, 208, 176
    f.rect(cx, cy, cw, ch, r=8)
    f.text(cx + 14, cy + 22, 'HNSW knobs', BLUE, LABEL, weight=600, halo=False)
    rows = [('M', 'edges per node → memory'),
            ('ef_construction', 'build quality, one-off cost'),
            ('ef', 'query width, must be ≥ k')]
    for i, (name, note) in enumerate(rows):
        y = cy + 52 + i * 42
        if i:
            f.line(cx + 12, y - 19, cx + cw - 12, y - 19, BORD, 1)
        f.text(cx + 14, y, name, AMBER if name == 'ef' else INK, LABEL, weight=600, mono=True, halo=False)
        f.text(cx + 14, y + 15, note, MUTED, SMALL, halo=False)

    # labels last
    for ef in (50, 200):
        f.label(str(ef), [(p.X(ef), p.y1 + 16, 'middle')], FAINT, TINY, mono=True)
    f.label(f'k = {K}', [(xk, p.y1 + 16, 'middle')], AMBER, TINY)
    f.label('exact search = 1.0', [(p.X(EF_MAX), p.Y(1) - 7, 'end')], FAINT, TINY)
    f.label('recall saturates', [(p.X(150), p.Y(recall(150)) + 20, 'middle'), (p.X(120), p.Y(recall(120)) + 20, 'middle')],
            GREEN, LABEL, weight=600)
    f.along(lat, 'latency keeps climbing', [0.62, 0.7, 0.55], fill=RED, size=LABEL, weight=600)
    f.label('measure recall against brute force before you ship the index',
            [(f.w / 2, 252, 'middle')], AMBER, SMALL)
    return f
