"""55 TF/Keras/PyTorch: eager vs compiled execution, as two timelines.

The same seven training steps run both ways. Eager: every op is dispatched
from Python, with Python in the gaps between ops, so each value exists as
the line runs and pdb works anywhere. Compiled: the first batch pauses to
trace and compile (Python side effects run then, once), after which each
step is one fused kernel with no Python in between, roughly a third shorter
here, inside the prose's "commonly 30–50%"; a shape change forces a
recompile, which is why compiled code rewards fixed shapes. The lengths are
illustrative, not measured.

History: the old figure was two boxes of four grey sentences each; it said
"faster" without showing where the time goes or what compiling costs.
The Keras/Lightning footnote moved out: it is not about execution mode.
"""
from figkit import Fig, BLUE, GREEN, AMBER, FAINT, MUTED, LABEL, SMALL, TINY

TARGET = ('55-tf-keras-pytorch', 0)

TX0 = 24
LH = 22                          # lane height
OP, OG, SG = 15, 4, 14           # eager: op width, gap between ops, gap between steps
FK, FG = 36, 6                   # compiled: fused step width, gap
COMP, RECOMP = 76, 52            # compile pause, recompile pause
STEPS = 7


def block(f, x, y, w, col, op=.7):
    f.rect(x, y, w, LH, fill=col, stroke=col, r=3, width=1.2, opacity=op)


def draw():
    f = Fig(560, 232, 'eagc')
    E, C = 46, 132                # lane tops

    # eager: three ops per step, Python between each
    x = TX0
    for s in range(STEPS):
        for k in range(3):
            block(f, x, E, OP, BLUE)
            x += OP + (OG if k < 2 else 0)
        x += SG
    e_end = x - SG

    # compiled: one compile pause, fused steps, a recompile when the shape changes
    x = TX0
    f.rect(x, C, COMP, LH, fill=AMBER, stroke=AMBER, r=3, width=1.2, opacity=.3)
    f.text(x + COMP / 2, C + LH / 2 + 3, 'trace + compile', AMBER, TINY, 'middle', weight=600, halo=False)
    comp_cx = x + COMP / 2
    x += COMP + FG
    fused = []
    for s in range(STEPS):
        if s == 3:
            f.rect(x, C, RECOMP, LH, fill=AMBER, stroke=AMBER, r=3, width=1.2, opacity=.3)
            f.text(x + RECOMP / 2, C + LH / 2 + 3, 'recompile', AMBER, TINY, 'middle', weight=600, halo=False)
            re_cx = x + RECOMP / 2
            x += RECOMP + FG
        block(f, x, C, FK, GREEN)
        fused.append(x + FK / 2)
        x += FK + FG
    c_end = x - FG

    # time axis
    ay = 198
    f.arrow(TX0, ay, 520, ay, FAINT, 1.2, gap=0)

    # labels last
    f.label('eager  (PyTorch default)', [(TX0, E - 10, 'start')], BLUE, LABEL, weight=600)
    f.label('compiled  (torch.compile, tf.function)', [(TX0, C - 10, 'start')], GREEN, LABEL, weight=600)
    for end, yy in ((e_end, E), (c_end, C)):
        f.label('7 steps', [(end + 8, yy + LH / 2 + 3, 'start')], FAINT, SMALL)
    f.label('every op dispatched from Python: each value exists as the line runs, pdb works anywhere',
            [(TX0, E + LH + 17, 'start')], MUTED, SMALL)
    f.label('Python side effects run here, once', [(TX0, C + LH + 15, 'start')], AMBER, TINY)
    f.label('shape changed', [(re_cx, C + LH + 15, 'middle')], AMBER, TINY)
    f.label('one fused kernel per step, no Python between ops: commonly 30–50% faster',
            [(TX0, C + LH + 32, 'start')], MUTED, SMALL)
    f.label('time', [(528, ay + 3.5, 'start')], FAINT, SMALL)
    f.label('Write and debug eagerly, then compile the hot loop.', [(f.w / 2, f.h - 8, 'middle')], AMBER, SMALL)
    return f
