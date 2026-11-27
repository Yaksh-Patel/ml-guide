"""06 bias–variance explorer (interactive): the static frame.

The curves never change, so they are drawn here with the same functions as
f06_0 (and the same colours: bias² red, variance blue, total green). The
topic's script only moves the cursor and the three dots (ids bvx-*) and
fills the HTML readout below.

History: the old explorer added the noise twice (inside bias² and again in
the total) and drew the noise line at twice the noise; its legend and its
readout were printed over the curves; "sweet spot" was a fixed 25–55% band
of the slider rather than the actual minimum.
"""
from figkit import Fig, BLUE, GREEN, AMBER, RED, FAINT, LABEL, SMALL
from f06_0 import bias2, var, total, NOISE

TARGET = ('06-bias-variance', 1)

# shared with the topic script (keep in step)
X0, Y0, X1, Y1, YMAX = 56, 26, 520, 196, 1.15


def draw():
    f = Fig(560, 236, 'bvx')
    p = f.plot_area(X0, Y0, X1, Y1, (0, 1), (0, YMAX))
    p.axes()
    f.path([(p.X(0), p.Y(NOISE)), (p.X(1), p.Y(NOISE))], FAINT, 1.2, dash='3 4')
    b = p.curve(bias2, RED)
    v = p.curve(var, BLUE)
    t = p.curve(total, GREEN, width=3)
    cmin = min((i / 1000 for i in range(1001)), key=total)
    f.circle(p.X(cmin), p.Y(total(cmin)), 4, fill=AMBER)

    # moving parts: start at the script's initial value (30%), ids for the script
    c0 = 0.30
    x = p.X(c0)
    f.raw(f'<line id="bvx-cursor" x1="{x:.1f}" y1="{Y0 - 4}" x2="{x:.1f}" y2="{Y1}" stroke="{AMBER}" '
          f'stroke-width="1.4" stroke-dasharray="4 4"/>')
    for key, fn, col in (('b', bias2, RED), ('v', var, BLUE), ('t', total, GREEN)):
        f.raw(f'<circle id="bvx-d{key}" cx="{x:.1f}" cy="{p.Y(fn(c0)):.1f}" r="5" fill="{col}" '
              f'stroke="#0b0d12" stroke-width="1.5"/>')

    f.along(t, 'total error', [0.86, 0.8, 0.92], fill=GREEN, size=LABEL, weight=600)
    f.along(v, 'variance', [0.96, 0.9], fill=BLUE, size=LABEL, weight=600)
    f.along(b, 'bias²', [0.12, 0.08, 0.18], fill=RED, size=LABEL, weight=600)
    f.label('noise floor', [(p.X(0.02), p.Y(NOISE) - 7, 'start'), (p.X(0.25), p.Y(NOISE) - 7, 'start'), (p.X(0.72), p.Y(NOISE) + 14, 'start')], FAINT)
    f.label('lowest total', [(p.X(cmin), p.Y(total(cmin)) + 18, 'middle')], AMBER)
    f.label('model complexity →', [(X1 + 12, Y1 + 18, 'end')], FAINT)
    f.label('error', [(X0 + 8, Y0 - 8, 'start')], FAINT)
    return f
