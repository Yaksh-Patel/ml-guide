"""45 credit risk: WoE by score band, PSI between training and live, and the
bands each number is read against.

Left: WoE per score band, monotone across the bands. Right: the training
and live score distributions; the live one is shifted by exactly the amount
that gives PSI 0.31 over training deciles (computed below, not eyeballed).
Under each panel, the IV and PSI bands the prose quotes, drawn as strips
instead of two lines of mono text; the PSI strip marks where 0.31 falls.

History: the old WoE panel drew low score bands negative (red) and high bands
positive, i.e. WoE = ln(good share / bad share). The prose defines WoE as
ln(bad share / good share), "so negative is safer than average and positive
is riskier", so the bars are flipped: risky low bands sit above zero. (The
code block below the figure uses the other sign convention; the prose and the
figure now agree with each other.)
"""
import math
from statistics import NormalDist
from figkit import Fig, BLUE, GREEN, AMBER, RED, FAINT, MUTED, INK, LABEL, SMALL, TINY

TARGET = ('45-credit-risk', 0)
WOE = [1.1, 0.74, 0.42, 0.15, -0.12, -0.4, -0.72, -1.06]   # ln(bad% / good%), low → high band
PSI_TARGET = 0.31


def psi(shift):
    """PSI of N(shift, 1) against N(0, 1), over the training deciles."""
    cuts = [NormalDist().inv_cdf(i / 10) for i in range(1, 10)]
    live = NormalDist(shift, 1)
    cdf = [0] + [live.cdf(c) for c in cuts] + [1]
    return sum((a - .1) * math.log(a / .1) for a in (cdf[i + 1] - cdf[i] for i in range(10)))


def shift_for(target):
    lo, hi = 0.0, 2.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if psi(mid) < target else (lo, mid)
    return (lo + hi) / 2


def strip(f, x0, y, segs, ticks):
    """Ordinal band strip: segs = [(width, colour or None, word)], ticks at the joins."""
    x = x0
    for w, col, word in segs:
        f.rect(x, y, w, 16, fill=col or FAINT, stroke=col or FAINT, r=3, opacity=.22 if col else .12)
        if word:
            f.text(x + w / 2, y + 11.5, word, col, TINY, 'middle', weight=600, halo=False)
        x += w
    xs, x = [], x0
    for w, _, _ in segs[:-1]:
        x += w
        xs.append(x)
    for xt, t in zip(xs, ticks):
        f.text(xt, y + 28, t, FAINT, TINY, 'middle', mono=True)
    return xs


def draw():
    f = Fig(560, 268, 'woe')

    # ---- WoE panel
    p = f.plot_area(48, 42, 236, 172, (0, 8), (-1.25, 1.25))
    p.axes(ylabel='WoE')
    zero = p.Y(0)
    f.line(p.x0, zero, p.x1 + 6, zero, FAINT, 1, dash='3 3')
    bw = 15
    for i, w in enumerate(WOE):
        cx = p.X(i + 0.5)
        col = RED if w > 0 else GREEN
        top, bot = (p.Y(w), zero) if w > 0 else (zero, p.Y(w))
        f.rect(cx - bw / 2, top, bw, bot - top, fill=col, stroke=col, r=2, opacity=.8)

    # ---- PSI panel
    q = f.plot_area(330, 42, 518, 172, (-3.2, 3.8), (0, 0.46))
    q.axes(ylabel='share of applicants')
    d = shift_for(PSI_TARGET)
    assert round(psi(d), 2) == PSI_TARGET
    train = q.curve(NormalDist(0, 1).pdf, BLUE, width=2.4)
    live = q.curve(NormalDist(d, 1).pdf, RED, width=2.4, dash='5 4')

    # ---- band strips
    iv_x = strip(f, 34, 216, [(46, FAINT, 'useless'), (30, None, ''), (50, GREEN, 'strong'),
                              (30, None, ''), (50, RED, 'suspicious')],
                 ['0.02', '0.1', '0.3', '0.5'])
    ps_x = strip(f, 330, 216, [(66, GREEN, 'stable'), (66, AMBER, 'investigate'), (66, RED, 'rebuild')],
                 ['0.10', '0.25'])
    # where 0.31 falls: linear inside the >0.25 segment, taking 0.25–0.40 as its span
    mx = ps_x[1] + 66 * (PSI_TARGET - 0.25) / 0.15
    f.raw(f'<path d="M{mx - 5:.1f},207 L{mx + 5:.1f},207 L{mx:.1f},213 z" fill="{RED}"/>',
          pts=[(mx - 5, 207), (mx + 5, 207), (mx, 213), (mx - 5, 207)])

    # ---- labels last
    f.label('riskier', [(p.X(0.5) + bw / 2 + 5, p.Y(WOE[0]) + 7, 'start')], RED, SMALL, weight=600)
    f.label('safer', [(p.X(7.5) - bw / 2 - 5, p.Y(WOE[-1]) + 3, 'end')], GREEN, SMALL, weight=600)
    f.label('monotonic: the binning is sound', [(p.X(4.4), p.Y(0.95), 'start'), (p.X(3.6), p.Y(1.1), 'start')],
            MUTED, SMALL)
    f.label('score band, low → high', [((p.x0 + p.x1) / 2, p.y1 + 16, 'middle')], FAINT, SMALL)
    f.label('score →', [(q.x1 + 12, q.y1 + 16, 'end')], FAINT, SMALL)
    f.along(train, 'training', [0.3, 0.25, 0.35], fill=BLUE, size=LABEL, weight=600)
    f.along(live, 'live', [0.72, 0.78, 0.66], fill=RED, size=LABEL, weight=600)
    f.label('IV of a feature', [(34, 207, 'start')], FAINT, TINY)
    f.label('PSI of the score', [(330, 207, 'start')], FAINT, TINY)
    f.label(f'this shift: {PSI_TARGET}', [(mx, 201, 'middle'), (mx - 9, 210, 'end')], RED, TINY, weight=600)
    return f
