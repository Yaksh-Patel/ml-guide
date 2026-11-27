"""50 data engineering: point-in-time correctness, one user joined two ways.

The prose's example (and the code under it): user 1's score is 610 from
1 January, 655 from 1 April, 700 from 1 June; the label event is 1 March.
Drawn as the score over time (a step), the label event as a line through it
and everything to its right as the future that 1 March could not see. The
as-of join looks back from the event and finds 610; "latest value per user"
reaches forward into June and finds 700.

History: the old figure put 1 March halfway between January and April; on a
month scale it is two thirds of the way. The timeline is to scale now.
"""
from figkit import Fig, BLUE, GREEN, AMBER, RED, FAINT, MUTED, INK, BORD, LABEL, SMALL, TINY

TARGET = ('50-data-engineering', 0)

X0, X1 = 70, 530            # 1 Jan .. 1 Jul
AX = 190                     # time axis


def mx(m):                   # m = months after 1 Jan
    return X0 + (X1 - X0) * m / 6


def sy(v):                   # score -> y
    return 164 - (v - 600) * 0.6


def draw():
    f = Fig(560, 240, 'pit')
    ev = mx(2)

    # the future, as seen from 1 March
    f.raw(f'<rect x="{ev:.1f}" y="34" width="{X1 + 8 - ev:.1f}" height="{AX - 34}" fill="{BORD}" opacity=".28"/>')

    # time axis with month ticks
    f.arrow(X0 - 14, AX, X1 + 18, AX, FAINT, 1.2, gap=0)
    for i, m in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']):
        f.line(mx(i), AX - 3, mx(i), AX + 3, FAINT, 1.1)
        f.text(mx(i), AX + 16, m, FAINT, SMALL, 'middle')

    # the score, valid from each change until the next
    vals = [(0, 610), (3, 655), (5, 700)]
    pts = []
    for k, (m, v) in enumerate(vals):
        end = vals[k + 1][0] if k + 1 < len(vals) else 6
        pts += [(mx(m), sy(v)), (mx(end), sy(v))]
    f.path(pts, BLUE, 2.4)
    for m, v in vals:
        f.circle(mx(m), sy(v), 4.5, fill=BLUE)

    # the label event
    f.line(ev, 46, ev, AX - 7, AMBER, 1.4, dash='4 3')
    f.circle(ev, AX, 5.5, fill=AMBER)

    # the two joins, from where the event line meets the score
    y610, y700 = sy(610), sy(700)
    f.qcurve((ev - 7, y610 - 8), ((ev + mx(0)) / 2, y610 - 44), (mx(0) + 5, y610 - 10), GREEN, 1.8, arrow=True)
    f.qcurve((ev + 7, y610 - 10), ((ev + mx(5)) / 2, y700 - 52), (mx(5) - 6, y700 - 8), RED, 1.8, arrow=True,
             dash='5 4')

    # labels last
    f.label('label event · 1 March', [(ev, 30, 'middle')], AMBER, SMALL, weight=600)
    f.label('not yet known on 1 March', [(X1 + 2, 48, 'end')], FAINT, TINY)
    for m, v in vals:
        f.label(str(v), [(mx(m) + 10, sy(v) + 16, 'start'), (mx(m) - 8, sy(v) + 16, 'end')], BLUE, LABEL,
                weight=600)
    f.label('score', [(X1 + 6, sy(700) + 4, 'start'), (X1 - 4, sy(700) - 8, 'end')], BLUE, SMALL)
    gx = (ev + mx(0)) / 2
    f.label('as-of join, backwards → 610', [(gx, y610 - 52 - k, 'middle') for k in range(0, 30, 2)], GREEN, LABEL,
            weight=600)
    f.label('the only value that existed', [(gx, y610 - 40, 'middle')], MUTED, TINY)
    rx = (ev + mx(5)) / 2 - 10
    f.label('latest value per user → 700', [(rx, y700 - 42 - k, 'middle') for k in range(0, 30, 2)], RED, LABEL,
            weight=600)
    f.label('a June fact on a March label', [(rx, y700 - 30, 'middle')], MUTED, TINY)
    f.label('Join on when a value became available, not when it happened: offline jobs can see the future.',
            [(f.w / 2, f.h - 10, 'middle')], AMBER, SMALL)
    return f
