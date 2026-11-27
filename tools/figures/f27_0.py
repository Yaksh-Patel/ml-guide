"""27 activation shapes: sigmoid, ReLU, GELU and softmax as four small multiples.

Each panel gets its name above and one short note below, inside its own
column, so the notes no longer run into each other. The sigmoid panel also
draws σ′ (dashed): its peak of 0.25 is the number the prose builds on. GELU
is drawn exactly (x·Φ(x)), so its small dip below zero is visible. Softmax is
not a curve, so it is three logits (2.0, 1.0, 0.1) turned into probabilities
that sum to 1. The old "✓" glyph is gone.
"""
import math
from figkit import Fig, BLUE, GREEN, AMBER, PURPLE, FAINT, MUTED, LABEL, SMALL, TINY

TARGET = ('27-activations', 0)

TOP, BOT = 42, 150
CX = [76, 208, 340, 472]      # panel centres
HW = 54                       # half panel width


def sig(x):
    return 1 / (1 + math.exp(-x))


def gelu(x):
    return x * 0.5 * (1 + math.erf(x / math.sqrt(2)))


def axes(f, p):
    """Cross-hair axes through the origin, as in a textbook sketch."""
    f.line(p.x0, p.Y(0), p.x1, p.Y(0), FAINT, 1)
    f.line(p.X(0), p.y0, p.X(0), p.y1, FAINT, 1)


def draw():
    f = Fig(560, 192, 'act')
    names = [('Sigmoid', BLUE), ('ReLU', GREEN), ('GELU', PURPLE), ('Softmax', AMBER)]
    notes = ['saturates: σ′ peaks at 0.25', 'slope exactly 1 for x > 0',
             'smooth; transformer default', 'probabilities summing to 1']

    # sigmoid and its derivative
    c = CX[0]
    p = f.plot_area(c - HW, TOP, c + HW, BOT, (-6, 6), (-0.12, 1.12))
    axes(f, p)
    d = p.curve(lambda x: sig(x) * (1 - sig(x)), BLUE, width=1.4, dash='3 3')
    p.curve(sig, BLUE, width=2.4)
    sig_d = d

    # ReLU
    c = CX[1]
    p = f.plot_area(c - HW, TOP, c + HW, BOT, (-3, 3), (-0.6, 3.0))
    axes(f, p)
    p.curve(lambda x: max(0.0, x), GREEN, width=2.4)

    # GELU
    c = CX[2]
    p = f.plot_area(c - HW, TOP, c + HW, BOT, (-3, 3), (-0.6, 3.0))
    axes(f, p)
    p.curve(gelu, PURPLE, width=2.4)

    # softmax: three logits -> probabilities
    c = CX[3]
    z = [2.0, 1.0, 0.1]
    e = [math.exp(v) for v in z]
    pr = [v / sum(e) for v in e]
    bw, step = 22, 34
    f.line(c - HW, BOT, c + HW, BOT, FAINT, 1)
    scale = (BOT - TOP - 14) / max(pr)
    bars = []
    for i, (zi, pi) in enumerate(zip(z, pr)):
        x = c + (i - 1) * step
        h = pi * scale
        x0, y0 = x - bw / 2, BOT - h
        f.raw(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{bw}" height="{h:.1f}" rx="2" fill="{AMBER}" '
              f'fill-opacity=".4" stroke="{AMBER}" stroke-width="1.4"/>',
              pts=[(x0, BOT), (x0, y0), (x0 + bw, y0), (x0 + bw, BOT)])
        bars.append((x, BOT - h, zi, pi))

    # labels last
    for (name, col), cx, note in zip(names, CX, notes):
        f.label(name, [(cx, 26, 'middle')], col, LABEL, weight=600)
        f.label(note, [(cx, 180, 'middle')], MUTED, SMALL)
    f.along(sig_d, 'σ′', [0.62, 0.68, 0.38], fill=BLUE, size=SMALL, d=6)
    for x, top, zi, pi in bars:
        f.label(f'{pi:.2f}', [(x, top - 5, 'middle')], AMBER, TINY, mono=True, pad=1)
        f.label(f'z={zi:.1f}', [(x, BOT + 13, 'middle')], FAINT, TINY, mono=True, pad=1)
    return f
