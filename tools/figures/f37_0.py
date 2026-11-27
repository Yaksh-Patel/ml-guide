"""37 tokenisation: byte-pair encoding builds "lower" out of characters, one
merge at a time.

History: the old figure labelled each row with the merge that came *after*
it (the row tagged "merge (e,r)" still showed e and r apart), and it showed
three merges under a caption that says four. It now uses the end-of-word
marker </w> from the code card's BPE, which gives exactly four merges:
e+r, er+</w>, l+o, lo+w. Each row shows the result of its merge; the pair
about to be fused is bracketed in amber in the row above.

Motion (one 10s clock): row by row, the pair is bracketed, then the next row
drops in with the fused token. Hold, fade, repeat. Reduced motion shows the
7.6s frame: all four merges done, every bracket visible.
"""
from figkit import (Fig, Anim, GREEN, AMBER, INK, MUTED, FAINT, BORD, SURF, LABEL, SMALL)

TARGET = ('37-tokenization-embeddings', 0)

EOW = '</w>'
ROWS = [   # (tokens, pair merged to make this row, new token)
    (['l', 'o', 'w', 'e', 'r', EOW], None, None),
    (['l', 'o', 'w', 'er', EOW], ('e', 'r'), 'er'),
    (['l', 'o', 'w', 'er' + EOW], ('er', EOW), 'er' + EOW),
    (['lo', 'w', 'er' + EOW], ('l', 'o'), 'lo'),
    (['low', 'er' + EOW], ('lo', 'w'), 'low'),
]
X0, Y0, PITCH, TH, GAPX = 140, 30, 46, 24, 6
RX = 346                       # right-hand column
T = 10.0
S0, EVERY = 0.6, 1.7           # merge k starts at S0 + (k-1)·EVERY
OUT0, OUT1 = 8.8, 9.3          # fade out
EASE = '.45 0 .25 1'


def tile_w(tok):
    return max(24, 14 + 6.2 * len(tok))


def layout(tokens):
    xs, x = [], X0
    for t in tokens:
        xs.append((x, tile_w(t)))
        x += tile_w(t) + GAPX
    return xs


def group(f, start, anim):
    """Wrap everything drawn since parts[start] in one animated <g>."""
    f.parts.insert(start, f'<g opacity="0">{anim}')
    f.parts.append('</g>')


def draw():
    f = Fig(560, 292, 'bpe')
    A = Anim(T)
    f.still = 7.6
    merged = set()             # tokens built by a merge so far

    for r, (tokens, pair, new) in enumerate(ROWS):
        y = Y0 + r * PITCH
        start = len(f.parts)
        if new:
            merged.add(new)
        for tok, (x, w) in zip(tokens, layout(tokens)):
            if tok == new:
                f.rect(x, y, w, TH, fill=GREEN, stroke=GREEN, r=5, width=1.4, opacity=None)
                f.parts[-1] = f.parts[-1].replace(f'fill="{GREEN}"', f'fill="{GREEN}" fill-opacity=".18"')
                col, wt = GREEN, 600
            elif tok in merged:
                f.rect(x, y, w, TH, fill=SURF, stroke=GREEN, r=5, width=1.2)
                col, wt = GREEN, 600
            else:
                f.rect(x, y, w, TH, fill=SURF, stroke=BORD, r=5, width=1.2)
                col, wt = (FAINT if tok == EOW else INK), None
            f.text(x + w / 2, y + TH / 2 + 3.4, tok, col, LABEL, 'middle', wt, mono=True, halo=False)

        ly = y + TH / 2 + 3.3
        if r == 0:
            f.text(X0 - 14, ly, 'start', MUTED, SMALL, 'end', weight=600)
            f.text(RX + 12, ly, 'characters, plus an end-of-word mark', FAINT, SMALL)
            continue
        f.text(X0 - 14, ly, f'merge {r}', MUTED, SMALL, 'end', weight=600)
        a, b = pair
        lhs = f'{a} + {b}'
        f.text(RX + 62, ly, lhs, AMBER, SMALL, 'end', mono=True)
        f.text(RX + 72, ly, f'→ {new}', GREEN, SMALL, mono=True, weight=600)

        # this row drops in from just above as its merge happens
        s = S0 + (r - 1) * EVERY
        on0, on1 = s + 0.6, s + 1.1
        fade = A.attr('opacity', [(0, 0), (on0, 0), (on1, 1), (OUT0, 1), (OUT1, 0), (T, 0)])
        slide = (f'<animateTransform attributeName="transform" type="translate" dur="{T}s" '
                 f'repeatCount="indefinite" values="0 -14;0 -14;0 0;0 0" '
                 f'keyTimes="{A.kt([0, on0, on1, T])}" calcMode="spline" '
                 f'keySplines="{EASE};{EASE};{EASE}"/>')
        group(f, start, fade + slide)

        # the bracket under the pair in the row above, shown just before
        prev_tokens = ROWS[r - 1][0]
        pl = layout(prev_tokens)
        i = next(k for k in range(len(prev_tokens) - 1)
                 if (prev_tokens[k], prev_tokens[k + 1]) == pair)
        xl, xr = pl[i][0] + 3, pl[i + 1][0] + pl[i + 1][1] - 3
        yb = Y0 + (r - 1) * PITCH + TH + 4
        bstart = len(f.parts)
        f.path([(xl, yb), (xl, yb + 4), (xr, yb + 4), (xr, yb)], AMBER, 1.8)
        group(f, bstart, A.attr('opacity', [(0, 0), (s, 0), (s + 0.3, 1), (OUT0, 1), (OUT1, 0), (T, 0)]))

    f.text(280, 280, 'nothing is out of vocabulary: unseen "slower" is  s · low · er</w>',
           MUTED, LABEL, 'middle')
    return f
