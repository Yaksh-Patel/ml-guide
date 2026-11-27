"""33 RNNs & LSTMs: the same recurrence twice, so the one difference stands out.

Top row: a vanilla RNN unrolled over four steps. The gradient runs back
through the same W_hh at every hop (red arcs, fading), which is the
"one matrix raised to the sequence length" problem the prose sets up.
Bottom row: one LSTM cell. The cell state C runs straight through; the
forget gate multiplies it (x), the input gate adds i*g to it (+), and the
output gate reads tanh(C) out as h_t. Along C the per-step factor is f_t,
a learned number, not W_hh.

The old figure put both ideas in one crowded panel, with the x labels under
the RNN cells sitting on their input arrows and the LSTM gates drawn as four
unconnected dots. Static.
"""
from figkit import Fig, BLUE, GREEN, AMBER, RED, PURPLE, INK, MUTED, FAINT, BORD, SURF, LABEL, SMALL, TINY

TARGET = ('33-rnns-lstms', 0)

COL = 112          # diagrams start here; the left column carries the row titles


def op(f, x, y, sym, color):
    """A small circular operator node (x or +)."""
    f.circle(x, y, 8, fill=SURF, stroke=color, width=1.6)
    f.text(x, y + 3.6, sym, color, LABEL, 'middle', 600, halo=False, check=False)


def draw():
    f = Fig(560, 304, 'rnn')

    # ---------------- RNN, unrolled ----------------
    cw, ch, top = 62, 34, 52
    xs = [COL + 50 + i * 112 for i in range(4)]
    cells = [f.box(x - cw / 2, top, cw, ch, 'tanh', stroke=BLUE, color=BLUE, size=LABEL) for x in xs]
    for a, b in zip(cells, cells[1:]):
        f.connect(a, b, GREEN, 1.8)
    for x in xs:
        f.arrow(x, top + ch + 26, x, top + ch, FAINT, 1.3)
    # the gradient going back, once per step, through the same matrix
    for i in range(3, 0, -1):
        x2, x1 = xs[i], xs[i - 1]
        op_ = (0.95, 0.65, 0.35)[3 - i]
        f.qcurve((x2 - 10, top - 4), ((x1 + x2) / 2, top - 28), (x1 + 10, top - 4), RED, 1.6,
                 arrow=True, opacity=op_, dash='4 3')

    f.text(16, top + 14, 'RNN', BLUE, LABEL, weight=600)
    f.text(16, top + 28, 'gradient: × Wₕₕ', MUTED, SMALL)
    f.text(16, top + 40, 'at every step', MUTED, SMALL)

    for i in range(3):
        f.label(f'h{"₁₂₃"[i]}', [((xs[i] + xs[i + 1]) / 2, top + ch / 2 - 6, 'middle')], GREEN, SMALL, weight=600)
    for i, x in enumerate(xs):
        f.label(f'x{"₁₂₃₄"[i]}', [(x, top + ch + 37, 'middle')], MUTED, SMALL)
    f.label('fades (λ < 1) or blows up (λ > 1)', [(xs[0] - 22, top - 26, 'start'), (xs[0], top - 30, 'start')], RED, SMALL)

    # divider
    f.line(16, 146, 544, 146, BORD, 1)

    # ---------------- LSTM cell ----------------
    hy = 178                      # the cell-state highway
    cell = (COL + 46, 160, 340, 128)
    f.rect(*cell, fill=SURF, stroke=PURPLE, r=8, width=1.4)
    fx, px, ox = COL + 112, COL + 222, COL + 330
    f.arrow(COL, hy, fx - 9, hy, AMBER, 2.6, gap=0)
    f.arrow(fx + 9, hy, px - 9, hy, AMBER, 2.6, gap=0)
    f.arrow(px + 9, hy, 546, hy, AMBER, 2.6, gap=0)
    op(f, fx, hy, '×', RED)
    op(f, px, hy, '+', BLUE)

    gy, gh, gw = 236, 30, 54
    f.box(fx - gw / 2, gy, gw, gh, 'f', 'forget', stroke=RED, color=RED, size=LABEL)
    f.box(px - 34 - gw / 2, gy, gw, gh, 'i', 'input', stroke=BLUE, color=BLUE, size=LABEL)
    f.box(px + 34 - gw / 2, gy, gw, gh, 'g', 'candidate', stroke=GREEN, color=GREEN, size=LABEL)
    f.box(ox - gw / 2, gy, gw, gh, 'o', 'output', stroke=PURPLE, color=PURPLE, size=LABEL)

    f.arrow(fx, gy, fx, hy + 8, RED, 1.4)
    my = 210
    op(f, px, my, '×', BLUE)
    f.line(px - 34, gy, px - 6, my + 6, BLUE, 1.3, gap=2)
    f.line(px + 34, gy, px + 6, my + 6, GREEN, 1.3, gap=2)
    f.arrow(px, my - 8, px, hy + 8, BLUE, 1.4)
    # output: h_t = o * tanh(C_t)
    op(f, ox, my, '×', PURPLE)
    f.arrow(ox, hy, ox, my - 8, AMBER, 1.3, gap=2)
    f.arrow(ox, gy, ox, my + 8, PURPLE, 1.4)
    f.arrow(ox + 8, my, 546, my, PURPLE, 1.6, gap=0)

    # gates all read [h_{t-1}, x_t] from one bus
    by = 278
    f.line(COL, by, ox, by, FAINT, 1.2)
    for gx in (fx, px - 34, px + 34, ox):
        f.line(gx, by, gx, gy + gh, FAINT, 1.2)

    f.text(16, hy + 26, 'LSTM', PURPLE, LABEL, weight=600)
    f.text(16, hy + 40, 'gradient along C:', MUTED, SMALL)
    f.text(16, hy + 52, '× fₜ at every step', MUTED, SMALL)

    f.label('Cₜ₋₁', [(COL + 2, hy - 8, 'start')], AMBER, SMALL, weight=600)
    f.label('Cₜ', [(544, hy - 8, 'end')], AMBER, SMALL, weight=600)
    f.label('hₜ', [(544, my - 7, 'end'), (544, my + 14, 'end')], PURPLE, SMALL, weight=600)
    f.label('tanh', [(ox + 6, (hy + my) / 2 + 3, 'start'), (ox - 6, (hy + my) / 2 + 3, 'end')], FAINT, TINY)
    f.label('hₜ₋₁, xₜ', [(COL, by + 14, 'start'), (COL, by - 6, 'start')], FAINT, SMALL)
    return f
