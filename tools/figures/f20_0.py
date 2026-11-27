"""20 dimensionality reduction: a scree plot with its cumulative curve, and
what separates PCA from the visualisation methods.

History: the old cumulative line was drawn on a different scale from the bars
and ran off the top of the plot, so it never showed the 68% it was meant to.
Here bars (per-component share) and the cumulative curve share one 0–100%
axis, and the curve passes through 68% at component 3. The old card also
lumped UMAP with t-SNE as "no transform()"; the prose says UMAP does provide
a transform for new points (it is the one usable as features), so UMAP now
has its own row and only t-SNE is marked look-only.
"""
from figkit import Fig, BLUE, GREEN, AMBER, RED, PURPLE, FAINT, MUTED, BORD, LABEL, SMALL, TINY

TARGET = ('20-dimensionality-reduction', 0)

SHARE = [0.34, 0.21, 0.13, 0.08, 0.06, 0.05, 0.04, 0.03, 0.03, 0.03]   # sums to 1; first 3 = 0.68


def draw():
    f = Fig(560, 250, 'scree')
    p = f.plot_area(50, 34, 290, 196, (0.4, 10.6), (0, 1.0))
    p.axes(ylabel='variance explained')

    # gridlines at 50% and 100%
    for v in (0.5, 1.0):
        f.line(p.x0, p.Y(v), p.x1, p.Y(v), BORD, 1, dash='2 4')

    bw = (p.X(1) - p.X(0)) * 0.62
    for i, s in enumerate(SHARE, start=1):
        x = p.X(i)
        f.rect(x - bw / 2, p.Y(s), bw, p.Y(0) - p.Y(s), fill=BLUE if i <= 3 else FAINT,
               stroke='none', r=2, opacity=0.9 if i <= 3 else 0.7)
        f.text(x, p.Y(0) + 13, str(i), FAINT, TINY, 'middle')

    cum, acc = [], 0.0
    for i, s in enumerate(SHARE, start=1):
        acc += s
        cum.append((p.X(i), p.Y(acc)))
    f.path(cum, GREEN, 2.2)
    for x, y in cum:
        f.circle(x, y, 2.4, fill=GREEN)

    # the read-off at k = 3
    x3, y3 = cum[2]
    f.line(p.x0, y3, x3 - 6, y3, AMBER, 1.2, dash='3 3')
    f.circle(x3, y3, 4.5, fill=AMBER)

    # the right-hand card: what each method can be used for
    cx, cw = 330, 214
    rows = [('PCA', 'linear · invertible · has transform()', 'reduce features, inside a pipeline', GREEN),
            ('UMAP', 'non-linear · has transform()', 'features if needed; axes mean nothing', PURPLE),
            ('t-SNE', 'no transform() · stochastic', 'for looking at only', RED)]
    y = 34
    for name, a, b, col in rows:
        f.rect(cx, y, cw, 48, stroke=col, width=1.2)
        f.text(cx + 12, y + 17, name, col, LABEL, weight=600, halo=False)
        f.text(cx + 12, y + 30, a, MUTED, TINY, halo=False)
        f.text(cx + 12, y + 41, b, FAINT if col != RED else RED, TINY, halo=False)
        y += 56

    # labels last
    f.label('first 3 hold 68%', [(p.X(3) + 12, y3 + 16, 'start'), (p.X(3) + 10, y3 + 26, 'start')],
            AMBER, SMALL, weight=600)
    f.label('68%', [(p.x0 - 6, y3 + 3, 'end')], AMBER, TINY)
    f.label('100%', [(p.x0 - 6, p.Y(1.0) + 3, 'end')], FAINT, TINY)
    f.label('50%', [(p.x0 - 6, p.Y(0.5) + 3, 'end')], FAINT, TINY)
    f.along(cum, 'cumulative', [0.62, 0.7, 0.55], fill=GREEN, size=SMALL, weight=600)
    f.label('component', [(p.x1 + 12, p.Y(0) + 26, 'end')], FAINT, SMALL)
    f.label('Do not read cluster sizes or gaps off a t-SNE plot, and never feed it to a model.',
            [(f.w / 2, f.h - 8, 'middle')], MUTED, SMALL)
    return f
