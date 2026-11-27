"""51 MLOps: the ML CI/CD pipeline, drawn as the loop it is.

Code feeds in at the top left; Data → Train → Evaluate run along the top,
Register → Deploy → Monitor come back along the bottom, and drift detected
by Monitor triggers the next run, closing the loop. The two stages the prose
says a software pipeline does not have are the amber ones: the data gate
before training and the metric gate after it, each able to stop the run.
Register carries the version tags the prose asks for (git SHA, data hash).

History: the old figure was a single row of seven boxes with 7-unit text.
Its retrain arrow re-entered at Train, skipping validation; a retrain on
fresh data has to pass the data gate, so the loop now re-enters at Data.
"""
from figkit import Fig, BLUE, GREEN, AMBER, RED, PURPLE, FAINT, MUTED, INK, BORD, LABEL, SMALL, TINY

TARGET = ('51-mlops', 1)

BW, BH = 112, 44
C1, C2, C3 = 160, 298, 436       # the three loop columns
R1, R2 = 70, 168                 # the two rows (top edge)


def draw():
    f = Fig(560, 250, 'cicd')

    code = f.box(14, R1, 102, BH, 'Code', 'git push', stroke=BORD, color=INK, size=LABEL)
    data = f.box(C1, R1, BW, BH, 'Validate data', 'data gate', stroke=AMBER, color=AMBER, size=LABEL,
                 sub_color=AMBER, width=1.6)
    train = f.box(C2, R1, BW, BH, 'Train', 'managed job', stroke=BLUE, color=BLUE, size=LABEL)
    ev = f.box(C3, R1, BW, BH, 'Evaluate', 'metric gate', stroke=AMBER, color=AMBER, size=LABEL,
               sub_color=AMBER, width=1.6)
    reg = f.box(C3, R2, BW, BH, 'Register', 'SHA + data hash', stroke=PURPLE, color=PURPLE, size=LABEL)
    dep = f.box(C2, R2, BW, BH, 'Deploy', 'canary → prod', stroke=BLUE, color=BLUE, size=LABEL)
    mon = f.box(C1, R2, BW, BH, 'Monitor', 'drift alerts', stroke=GREEN, color=GREEN, size=LABEL)

    for a, b in ((code, data), (data, train), (train, ev), (ev, reg), (reg, dep), (dep, mon)):
        f.connect(a, b, FAINT, 1.5)
    # drift closes the loop
    f.arrow(mon.cx, mon.t, data.cx, data.b, AMBER, 1.6, dash='5 4')

    # each gate can stop the run
    for g in (data, ev):
        f.arrow(g.cx, g.t, g.cx, g.t - 26, RED, 1.4)

    # labels last
    my = (data.b + mon.t) / 2
    f.label('drift → retrain', [(data.cx - 10, my + 4, 'end')], AMBER, SMALL, weight=600)
    f.label('schema or shift fails → stop', [(data.cx, data.t - 34, 'middle')], RED, SMALL)
    f.label('loses to champion → stop', [(ev.cx, ev.t - 34, 'middle'), (ev.r, ev.t - 34, 'end')], RED, SMALL)
    f.label('Same commit + new data = a different model, so the pipeline gates the data and the metric.',
            [(f.w / 2, f.h - 10, 'middle')], AMBER, SMALL)
    return f
