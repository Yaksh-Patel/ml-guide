"""34 self-attention explorer (interactive): the static frame.

"The cat sat on the mat because it was tired". One row of tokens; arcs fan
out above from the query to every other token, width ∝ its attention
weight; under each token a heat cell holds the weight itself (the query's
row of the attention matrix; each row sums to 1). Clicking a token (or
Enter on it) makes it the query: the topic script rebuilds the arcs and
recolours the boxes and cells (ids atx-*), and fills the readout and note.
Drawn here in the initial state, query "it", whose strongest arc goes to
"cat" (0.38), as the prose says.

History: the old figure repeated the sentence three times (text, buttons,
fan), printed the weights under the fan where the lines ran through them,
and drew its thickest line across the labels into the query box.
"""
from figkit import Fig, BLUE, AMBER, INK, BORD, SURF, LABEL, SMALL

TARGET = ('34-attention-architecture', 2)

# shared with the topic script (keep in step)
TOKENS = ('The', 'cat', 'sat', 'on', 'the', 'mat', 'because', 'it', 'was', 'tired')
X0, BW, GAP_X, TY, TH, CY, CH = 13, 48, 6, 112, 24, 142, 24
QUERY = 7
ROW = (0.06, 0.38, 0.12, 0.06, 0.06, 0.06, 0.08, 0.08, 0.06, 0.04)


def cx(i):
    return X0 + BW / 2 + i * (BW + GAP_X)


def arc(q, j):
    """Start, control, end of the arc from query q to token j (same as the script)."""
    sx = cx(q) + (8 if j > q else -8)
    ex = cx(j)
    h = 12 + 0.17 * abs(ex - sx)
    return (sx, TY - 2), ((sx + ex) / 2, TY - 2 - 2 * h), (ex, TY - 2)


def draw():
    f = Fig(560, 172, 'atx')
    f.raw('<g id="atx-arcs">')
    for j, w in enumerate(ROW):
        if j == QUERY:
            continue
        p0, c, p1 = arc(QUERY, j)
        f.qcurve(p0, c, p1, BLUE, round(0.8 + 12 * w, 2),
                 extra=f' stroke-opacity="{min(0.95, 0.35 + 1.4 * w):.2f}"')
    f.raw('</g>')
    for i, (s, w) in enumerate(zip(TOKENS, ROW)):
        x = cx(i) - BW / 2
        q = i == QUERY
        f.raw(f'<rect id="atx-b{i}" x="{x:.1f}" y="{TY}" width="{BW}" height="{TH}" rx="6" '
              f'fill="{AMBER if q else SURF}" fill-opacity="{".16" if q else "1"}" '
              f'stroke="{AMBER if q else BORD}" stroke-width="{1.8 if q else 1.2}"/>',
              [(x, TY), (x + BW, TY), (x + BW, TY + TH), (x, TY + TH), (x, TY)])
        f.text(cx(i), TY + TH / 2 + 3.5, s, AMBER if q else INK, LABEL, 'middle', 600 if q else None,
               halo=False, extra=f' id="atx-t{i}"')
        f.raw(f'<rect id="atx-c{i}" x="{x:.1f}" y="{CY}" width="{BW}" height="{CH}" rx="4" '
              f'fill="{BLUE}" fill-opacity="{0.06 + 1.3 * w:.3f}" stroke="{AMBER if q else BORD}" '
              f'stroke-width="{1.6 if q else 1}"/>',
              [(x, CY), (x + BW, CY), (x + BW, CY + CH), (x, CY + CH), (x, CY)])
        f.text(cx(i), CY + CH / 2 + 3.2, f'{w:.2f}', INK, SMALL, 'middle', 600 if w > 0.15 else None,
               mono=True, halo=False, extra=f' id="atx-w{i}"')
    # click targets: one per token column, on top of everything
    for i, s in enumerate(TOKENS):
        x = cx(i) - BW / 2 - GAP_X / 2
        f.raw(f'<rect id="atx-k{i}" x="{x:.1f}" y="{TY - 4}" width="{BW + GAP_X}" height="{CY + CH - TY + 6}" '
              f'fill="transparent" tabindex="0" role="button" aria-label="Make &quot;{s}&quot; the query" '
              f'style="cursor:pointer;outline-offset:-2px"/>')
    return f
