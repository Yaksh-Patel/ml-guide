"""16 random forest: the two sources of decorrelation, and what they buy.

Top: bootstrap rows. Three trees, ten training rows each drawn with
replacement; a number marks a row drawn more than once, hollow cells are the
tree's out-of-bag rows. Bottom: at every split only a random √d of the d
features are on offer (3 of 9 here), so the strongest feature, x₁, is
unavailable at most splits. Both feed "less correlated trees": ρ falls from
about 0.70 (bagging) to 0.30 (forest), the numbers the prose works through.

The old figure showed the same two ideas as unlabelled grids with tiny grey
captions, and wrote √p where the prose says √d. Duplicate draws and the
strongest feature are new: they are what "with replacement" and "a dominant
feature is unavailable at most nodes" look like.
"""
from figkit import Fig, BLUE, PURPLE, AMBER, GREEN, FAINT, MUTED, INK, LABEL, SMALL, TINY

TARGET = ('16-random-forest', 0)

DRAWS = [[1, 0, 2, 1, 0, 1, 0, 2, 1, 2],     # each row sums to 10: a bootstrap of n = 10
         [0, 1, 1, 0, 3, 1, 0, 1, 2, 1],
         [2, 0, 1, 0, 2, 1, 2, 0, 2, 0]]
SPLITS = [{0, 4, 7}, {2, 5, 8}, {1, 3, 6}]   # √9 = 3 features offered per split
C, P = 15, 19                                # cell size, pitch
GX = 84                                      # grid left edge


def cell(f, x, y, col, filled, outline=None):
    if filled:
        f.raw(f'<rect x="{x}" y="{y}" width="{C}" height="{C}" rx="3" fill="{col}" opacity=".45"/>')
    f.rect(x, y, C, C, fill='none', stroke=outline or (col if filled else FAINT), r=3,
           width=1.3 if outline else 1)


def draw():
    f = Fig(560, 262, 'rf')

    # 1 — bootstrap the rows
    ya = 34
    f.text(GX - 50, ya - 12, '1 · bootstrap the rows', BLUE, LABEL, weight=600)
    for t, counts in enumerate(DRAWS):
        y = ya + t * P
        f.text(GX - 10, y + C / 2 + 3.2, f'tree {t + 1}', MUTED, SMALL, 'end')
        for i, n in enumerate(counts):
            x = GX + i * P
            cell(f, x, y, BLUE, n > 0)
            if n > 1:
                f.text(x + C / 2, y + C / 2 + 3.2, str(n), INK, TINY, 'middle', weight=600, halo=False)
    f.text(GX, ya + 3 * P + 12, 'with replacement · hollow = out-of-bag (~36.8%)', MUTED, SMALL)

    # 2 — random features at every split
    yb = ya + 3 * P + 66
    f.text(GX - 50, yb - 26, '2 · a random √d features at every split', PURPLE, LABEL, weight=600)
    for i in range(9):
        f.text(GX + i * P + C / 2, yb - 6, f'x{"₁₂₃₄₅₆₇₈₉"[i]}', AMBER if i == 0 else FAINT, SMALL, 'middle',
               weight=600 if i == 0 else None)
    for s, offered in enumerate(SPLITS):
        y = yb + s * P
        f.text(GX - 10, y + C / 2 + 3.2, f'split {s + 1}', MUTED, SMALL, 'end')
        for i in range(9):
            cell(f, GX + i * P, y, PURPLE, i in offered, outline=AMBER if i == 0 else None)
    f.text(GX, yb + 3 * P + 12, 'the strongest feature, x₁, is on offer at 1 split in 3', MUTED, SMALL)

    # both → less correlated trees
    res = f.box(GX + 10 * P + 74, (ya + yb + 3 * P) / 2 - 25, 160, 50, 'less correlated trees', 'ρ ≈ 0.70 → 0.30', stroke=GREEN, color=GREEN, size=LABEL)
    ea = (GX + 10 * P + 6, ya + P + C / 2)
    eb = (GX + 9 * P + 6, yb + P + C / 2)
    f.arrow(*ea, res.l, res.cy - 8, FAINT, 1.4)
    f.arrow(*eb, res.l, res.cy + 8, FAINT, 1.4)

    f.label('averaging B trees leaves a floor of ρσ²: only a lower ρ moves it',
            [(f.w / 2, f.h - 8, 'middle')], MUTED, SMALL)
    return f
