"""35 transformers: the encoder–decoder, with every sublayer drawn as the
prose writes it: x ← x + f(LN(x)), a residual stream with one skip per
sublayer joining at a +.

History: the old figure's decoder had no feed-forward sublayer (masked
self-attention, then cross-attention, then nothing); every decoder layer has
an FFN, and the prose's 12d² count depends on it. It also drew the residuals
as two loose "⌒" glyphs and the post-norm "Add & LayerNorm" blocks the prose
says modern models no longer use; the input label was clipped at the bottom.

Motion (one 6s clock): a token's vector rises through the encoder and leaves
its top as K, V; at the same time a vector rises through the decoder's masked
self-attention. They meet in cross-attention (Q from below, K, V from the
encoder), which lights up; the decoder vector carries on through the FFN and
out of the top. Reduced motion shows the 3.0s frame: the two meeting.
"""
import math
from figkit import (Fig, Anim, BLUE, PURPLE, AMBER, INK, MUTED, FAINT, BORD, SURF, BG,
                    LABEL, SMALL, TINY, GAP, polyline_length)

TARGET = ('35-transformers', 0)

BW, BH, UNIT = 124, 24, 64
FB = 270                    # frame bottom (both stacks)


def rounded(pts, r=10):
    """Polyline with rounded corners -> (path d, sampled points)."""
    d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    out = [pts[0]]
    for a, b, c in zip(pts, pts[1:], pts[2:]):
        la, lb = math.dist(a, b), math.dist(b, c)
        p = (b[0] + (a[0] - b[0]) * r / la, b[1] + (a[1] - b[1]) * r / la)
        q = (b[0] + (c[0] - b[0]) * r / lb, b[1] + (c[1] - b[1]) * r / lb)
        d += f' L{p[0]:.1f},{p[1]:.1f} Q{b[0]:.1f},{b[1]:.1f} {q[0]:.1f},{q[1]:.1f}'
        out += [p, q]
    d += f' L{pts[-1][0]:.1f},{pts[-1][1]:.1f}'
    out.append(pts[-1])
    return d, out


def stack(f, sx, names, side, strokes):
    """Draw one stack's stream, skips and + nodes. Returns the box rects
    (x, y, w, h) to draw later and the y of the stream's top."""
    boxes, y0 = [], FB
    for name, st in zip(names, strokes):
        bt, pl = y0 - 16 - BH, y0 - 54
        f.line(sx, y0, sx, bt + BH, FAINT, 1.4)          # stream into the box (box hides it)
        f.line(sx, bt, sx, pl + 7, FAINT, 1.4)            # box -> +
        # the skip: branch off below the box, rejoin at the +
        bx = sx + side * (BW / 2 + 12)
        d, pts = rounded([(sx, y0 - 8), (bx, y0 - 8), (bx, pl), (sx + side * 7, pl)], 7)
        f.raw(f'<path d="{d}" fill="none" stroke="{FAINT}" stroke-width="1.3" stroke-linecap="round" '
              f'marker-end="url(#{f.marker(FAINT)})"/>', pts)
        f.circle(sx, pl, 7, fill=SURF, stroke=MUTED, width=1.3)
        f.text(sx, pl + 3.3, '+', MUTED, LABEL, 'middle', 600, halo=False, check=False)
        boxes.append((sx - BW / 2, bt, BW, BH, name, st))
        f.line(sx, pl - 7, sx, y0 - UNIT, FAINT, 1.4)
        y0 -= UNIT
    return boxes, y0


def draw():
    f = Fig(560, 320, 'tf')
    ex, dx = 140, 420
    ef = (ex - 96, FB - 2 * UNIT - 10, 192, 2 * UNIT + 10)
    df = (dx - 96, FB - 3 * UNIT - 10, 192, 3 * UNIT + 10)
    f.rect(*ef, fill='none', stroke=BLUE, r=10, width=1.3)
    f.rect(*df, fill='none', stroke=PURPLE, r=10, width=1.3)

    eb, etop = stack(f, ex, ['Self-attention', 'Feed-forward'], -1, [BORD, BORD])
    db, dtop = stack(f, dx, ['Masked self-attention', 'Cross-attention', 'Feed-forward'], +1, [BORD, BLUE, BORD])

    # inputs and output
    f.arrow(ex, 298, ex, FB, FAINT, 1.4, gap=0)
    f.arrow(dx, 298, dx, FB, FAINT, 1.4, gap=0)
    f.line(ex, etop, ex, ef[1], FAINT, 1.4)
    f.arrow(dx, dtop, dx, df[1] - 22, FAINT, 1.4, gap=0)

    # encoder output -> K, V into cross-attention
    cross = db[1]
    cy = cross[1] + BH / 2
    kv_pts = [(ex, ef[1]), (ex, ef[1] - 22), (dx - 132, ef[1] - 22), (dx - 132, cy), (cross[0] - GAP - 1, cy)]
    kv_d, kv_s = rounded(kv_pts, 10)
    f.raw(f'<path d="{kv_d}" fill="none" stroke="{BLUE}" stroke-width="1.8" stroke-linecap="round" '
          f'stroke-linejoin="round" marker-end="url(#{f.marker(BLUE)})"/>', kv_s)

    # ---- motion: dots travel under the boxes, so they "enter" each layer ----
    A = Anim(6.0)
    f.still = 3.0
    enc_path = [(ex, 298), (ex, ef[1])] + kv_pts[1:]
    ed, es = rounded(enc_path, 10)
    split = polyline_length(es[:2]) / polyline_length(es)
    f.raw(f'<circle r="4.5" fill="{BLUE}" stroke="{BG}" stroke-width="1.2">'
          f'{A.motion(ed, [(0, 0), (0.3, 0), (1.8, split), (2.9, 1), (6, 1)])}'
          f'{A.attr("opacity", [(0, 0), (0.3, 0), (0.4, 1), (3.3, 1), (3.6, 0), (6, 0)])}</circle>')
    up = f'M{dx},298 L{dx},{df[1] - 20}'
    meet = (298 - (cross[1] + BH + 3)) / (298 - (df[1] - 20))
    f.raw(f'<circle r="4.5" fill="{PURPLE}" stroke="{BG}" stroke-width="1.2">'
          f'{A.motion(up, [(0, 0), (1.0, 0), (2.9, meet), (3.4, meet), (4.6, 1), (6, 1)])}'
          f'{A.attr("opacity", [(0, 0), (1.0, 0), (1.1, 1), (4.6, 1), (4.9, 0), (6, 0)])}</circle>')

    for (x, y, w, h, name, st) in eb + db:
        f.box(x, y, w, h, name, stroke=st, color=BLUE if st == BLUE else INK, size=SMALL,
              weight=600 if st == BLUE else 500, width=1.6 if st == BLUE else 1.2)
    # cross-attention lights up when Q meets K, V
    x, y, w, h = cross[:4]
    f.parts.append(f'<rect x="{x - 3:.1f}" y="{y - 3:.1f}" width="{w + 6:.1f}" height="{h + 6:.1f}" rx="8" '
                   f'fill="none" stroke="{AMBER}" stroke-width="2">'
                   f'{A.attr("opacity", [(0, 0), (2.7, 0), (2.95, 1), (3.5, 1), (4.0, 0), (6, 0)])}</rect>')

    # ---- labels ----
    f.text(ef[0] + 2, ef[1] - 8, 'Encoder', BLUE, LABEL, weight=600)
    f.text(df[0] + 2, df[1] - 8, 'Decoder', PURPLE, LABEL, weight=600)
    f.label('× 6', [(ef[0] + ef[2] - 8, ef[1] + 16, 'end')], BLUE, SMALL, weight=600, mono=True)
    f.label('× 6', [(df[0] + 8, df[1] + 16, 'start')], PURPLE, SMALL, weight=600, mono=True)
    f.label('K, V', [((ex + dx - 132) / 2, ef[1] - 28, 'middle')], BLUE, SMALL, weight=600)
    f.label('Q', [(dx - 6, cross[1] + BH + 12, 'end'), (dx + 6, cross[1] + BH + 12, 'start')], PURPLE, SMALL, weight=600)
    f.label('input + positional encoding', [(ex, 312, 'middle')], MUTED, SMALL)
    f.label('outputs so far + positional encoding', [(dx, 312, 'middle')], MUTED, SMALL)
    f.label('next-token probabilities', [(dx + 8, df[1] - 14, 'start')], MUTED, SMALL)
    f.label('every sublayer:  x ← x + f(LN(x))', [(ef[0], 66, 'start'), (16, 18, 'start')], MUTED, SMALL, mono=True)
    return f
