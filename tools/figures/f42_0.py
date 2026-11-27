"""42 agentic AI: the ReAct loop, with the two brakes drawn where they act.

The allow-list sits between the model's choice and the dispatch; a name the
model invented never runs, it comes back as an error observation (the red arc).
The step budget sits on the loop-back edge, so every pass has to get through
it. The old figure parked both brakes in boxes underneath, unconnected, and
their notes overflowed.

History: the old loop ran think → act → observe → answer?, checking for a final
answer after the observation. In the code below the figure (and in ReAct) the
model's output each step is either a tool call or a final answer, so the check
comes straight after the LLM call: think → final? → allow-list → act → observe.
"""
from figkit import GAP, Fig, BLUE, GREEN, AMBER, RED, PURPLE, FAINT, MUTED, LABEL, SMALL

TARGET = ('42-agentic-ai', 0)


def draw():
    f = Fig(560, 208, 'agl')
    W, H, G, X0, Y = 82, 40, 30, 15, 80
    spec = [('think', 'LLM call', BLUE),
            ('final?', None, AMBER),
            ('allow-list', 'known tools only', RED),
            ('act (tool)', 'run it', PURPLE),
            ('observe', 'append to history', GREEN)]
    B = []
    for i, (name, sub, col) in enumerate(spec):
        B.append(f.box(X0 + i * (W + G), Y, W, H, name, sub, stroke=col, color=col, size=LABEL))
    think, final, allow, act, obs = B
    for a, b in zip(B, B[1:]):
        f.connect(a, b)

    # yes: leave the loop
    f.arrow(final.cx, final.t, final.cx, 38, GREEN, 1.4)

    # unknown tool: error back in as an observation, skipping act
    f.qcurve((allow.cx, allow.t - 4), ((allow.cx + obs.cx) / 2, 18), (obs.cx, obs.t - 4),
             RED, 1.4, arrow=True, dash='4 3')

    # loop back through the step budget
    ly = 176
    sb = f.box(220, ly - 18, 120, 36, 'step budget', 'max_steps, then stop', stroke=RED, color=RED, size=LABEL)
    elbow(f, [(obs.cx, obs.b + GAP), (obs.cx, ly), (sb.r, ly)])
    elbow(f, [(sb.l, ly), (think.cx, ly), (think.cx, think.b)])

    # labels last
    f.label('return the answer', [(final.cx, 28, 'middle')], GREEN, SMALL, weight=600)
    f.label('yes', [(final.cx + 7, 62, 'start')], GREEN, SMALL)
    f.label('no', [((final.r + allow.l) / 2, Y + H / 2 - 7, 'middle')], MUTED, SMALL)
    f.label('invented tool name → error, fed back as an observation',
            [((allow.cx + obs.cx) / 2, 38, 'middle'), ((allow.cx + obs.cx) / 2, 26, 'middle')], RED, SMALL)
    f.label('loop again', [((obs.cx + sb.r) / 2, ly - 7, 'middle')], MUTED, SMALL)
    return f



def elbow(f, pts, color=FAINT, width=1.4):
    """Right-angled connector: one continuous stroke, arrowhead on the last
    segment, which alone stops GAP short of its target."""
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    end = (x2 - (x2 - x1) / d * GAP, y2 - (y2 - y1) / d * GAP)
    q = pts[:-1] + [end]
    mk = f.marker(color)
    f.raw('<path d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in q) + f'" fill="none" stroke="{color}" '
          f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#{mk})"/>', pts=q)
