#!/usr/bin/env python3
"""Small SVG kit so every diagram in the guide shares one visual language.

Colours are the legacy palette hexes on purpose: style.css maps those 15
values onto the live design tokens, so anything drawn here follows both
themes automatically.
"""
import math, pathlib, html as HTML_

INK, MUTED, FAINT = '#e6e9f4', '#8e97b8', '#4e5a7a'
SURF, BORD        = '#1a1f2e', '#2e3a58'
BLUE, GREEN, AMBER, RED, PURPLE = '#5ba4fb', '#22d3a0', '#f5a623', '#f06767', '#b97cf8'

def txt(x, y, s, fill=MUTED, size=9.5, anchor='middle', weight=None, mono=False):
    w = f' font-weight="{weight}"' if weight else ''
    fam = 'JetBrains Mono' if mono else 'DM Sans'
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" '
            f'text-anchor="{anchor}" font-family="{fam}"{w}>{HTML_.escape(str(s))}</text>')

def axes(x0, y0, x1, y1, xlabel=None, ylabel=None):
    """L-shaped axes with optional labels. y0 is the BOTTOM (larger y)."""
    out = [f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{FAINT}" stroke-width="1"/>',
           f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{FAINT}" stroke-width="1"/>']
    if xlabel: out.append(txt((x0+x1)/2, y0+16, xlabel, FAINT, 9))
    if ylabel: out.append(f'<text x="{x0-9}" y="{(y0+y1)/2}" fill="{FAINT}" font-size="9" '
                          f'text-anchor="middle" font-family="DM Sans" '
                          f'transform="rotate(-90 {x0-9} {(y0+y1)/2})">{HTML_.escape(ylabel)}</text>')
    return out

def curve(pts, color, width=2.4, dash=None):
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{da}/>'

def plot(fn, x0, y0, x1, y1, xr=(-4, 4), yr=(0, 1), color=BLUE, n=90, **kw):
    """Sample fn over xr and map into the box (x0,y0)-(x1,y1)."""
    a, b = xr; lo, hi = yr
    pts = []
    for i in range(n + 1):
        xv = a + (b - a) * i / n
        yv = fn(xv)
        pts.append((x0 + (x1 - x0) * i / n,
                    y0 - (y0 - y1) * (min(max(yv, lo), hi) - lo) / (hi - lo)))
    return curve(pts, color, **kw)

def box(x, y, w, h, label, fill=SURF, stroke=BORD, color=INK, size=10, r=5, sub=None):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>']
    if sub:
        out.append(txt(x + w/2, y + h/2 - 2, label, color, size, weight='600'))
        out.append(txt(x + w/2, y + h/2 + 11, sub, FAINT, 8.5))
    else:
        out.append(txt(x + w/2, y + h/2 + size*0.36, label, color, size, weight='600'))
    return out

def arrow(x1, y1, x2, y2, color=FAINT, width=1.4, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{width}" marker-end="url(#ah)"{da}/>')

def node(cx, cy, r, label=None, fill=SURF, stroke=BLUE, color=INK, size=9):
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>']
    if label is not None: out.append(txt(cx, cy + size*0.36, label, color, size))
    return out

def bar(x, y_base, w, h, color, label=None, value=None):
    out = [f'<rect x="{x}" y="{y_base-h}" width="{w}" height="{h}" rx="2" fill="{color}" opacity=".85"/>']
    if label: out.append(txt(x + w/2, y_base + 13, label, FAINT, 8.5))
    if value: out.append(txt(x + w/2, y_base - h - 5, value, color, 8.5, mono=True))
    return out

DEFS = (f'<defs><marker id="ah" markerWidth="6" markerHeight="5" refX="5.5" refY="2.5" '
        f'orient="auto"><polygon points="0 0,6 2.5,0 5" fill="{FAINT}"/></marker></defs>')

def svg(width, height, body, title):
    inner = '\n'.join(body if isinstance(body, list) else [body])
    return (f'\n<div class="anim-wrap"><div class="anim-title">{HTML_.escape(title)}</div>\n'
            f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">\n'
            f'{DEFS}\n{inner}\n</svg></div>\n')

def insert(topic_id, markup, after_card=1):
    """Insert markup after the Nth top-level closing card of the topic."""
    target = None
    for f in pathlib.Path('topics').glob('*.html'):
        if f'id="sec-{topic_id}"' in f.read_text():
            target = f; break
    if not target:
        print(f'  !! no file for {topic_id}'); return False
    s = target.read_text()
    if '<svg' in s:
        print(f'  .. {topic_id}: already has a diagram'); return False
    # place it just before the "In code" card so it reads: concept -> picture -> code
    anchor = '\n<div class="card cc"><div class="card-title">In code</div>'
    if anchor in s:
        s = s.replace(anchor, markup + anchor, 1)
    else:
        s = s.rstrip()[:-len('</section>')] + markup + '</section>\n'
    target.write_text(s)
    print(f'  ++ {target.name}')
    return True
