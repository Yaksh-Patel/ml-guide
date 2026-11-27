"""39 ReAct: Thought → Action → (tool) → Observation → back to Thought, as a
loop, with the question coming in and the answer leaving only when the
model decides it is done.

The old figure drew the loop as a straight line with a second "Thought" box
and a faint return arc, small in a wide panel. Drawing it as a ring makes
the repetition the shape, and the tool sits outside the model's boxes
(dashed) because it is the part that is not the model. Static.
"""
from figkit import Fig, BLUE, GREEN, AMBER, PURPLE, INK, MUTED, FAINT, SURF, GAP, LABEL, SMALL, TINY, Box

TARGET = ('39-llms-rlhf', 0)


def dashed_box(f, x, y, w, h, label, sub, color):
    f.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{SURF}" stroke="{color}" '
          f'stroke-width="1.3" stroke-dasharray="4 3"/>',
          [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)])
    f.text(x + w / 2, y + h / 2 - 2, label, INK, SMALL, 'middle', 600, halo=False)
    f.text(x + w / 2, y + h / 2 + TINY + 3, sub, MUTED, TINY, 'middle', halo=False)
    return Box(x, y, w, h)


def draw():
    f = Fig(560, 270, 'react')
    W, H = 118, 44
    th = f.box(150, 104, W, H, 'Thought', 'reason about the task', stroke=BLUE, color=BLUE, size=LABEL, width=1.6)
    ac = f.box(300, 26, W, H, 'Action', 'call a tool', stroke=GREEN, color=GREEN, size=LABEL, width=1.6)
    ob = f.box(300, 182, W, H, 'Observation', 'what the tool returned', stroke=AMBER, color=AMBER, size=LABEL, width=1.6)
    tl = dashed_box(f, 452, 104, 92, H, 'Tool', 'search · API · code', FAINT)
    q = f.box(16, 108, 84, 36, 'Question', stroke=FAINT, color=INK, size=SMALL)
    an = f.box(150, 220, W, 36, 'Answer', stroke=PURPLE, color=PURPLE, size=LABEL, width=1.6)

    f.connect(q, th, FAINT, 1.4)
    # the ring: each hop leaves one box and turns into the next
    rx = th.cx + 24
    f.qcurve((rx, th.t - GAP), (rx, ac.cy), (ac.l - GAP, ac.cy), BLUE, 1.6, arrow=True)
    f.qcurve((ac.r + GAP, ac.cy), (tl.cx, ac.cy), (tl.cx, tl.t - GAP), GREEN, 1.6, arrow=True)
    f.qcurve((tl.cx, tl.b + GAP), (tl.cx, ob.cy), (ob.r + GAP, ob.cy), FAINT, 1.6, arrow=True)
    f.qcurve((ob.l - GAP, ob.cy), (rx, ob.cy), (rx, th.b + GAP), AMBER, 1.6, arrow=True)
    f.line(th.cx - 24, th.b, th.cx - 24, an.t, PURPLE, 1.6, arrow=True, gap=GAP)

    f.label('when done', [(th.cx - 32, (th.b + an.t) / 2 + 3, 'end')], PURPLE, SMALL, weight=600)
    f.label('each observation', [(ac.cx, 112, 'middle')], MUTED, SMALL)
    f.label('grounds the next thought', [(ac.cx, 125, 'middle')], MUTED, SMALL)
    f.label('repeat, up to a step limit', [(ac.cx, 144, 'middle')], FAINT, TINY)
    return f
