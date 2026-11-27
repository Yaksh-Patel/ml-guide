"""54 model cheatsheet: model selection as a decision procedure.

One question (what shape is the data?) fans out to four defaults, the same
ones pick_model() in the code below returns: gradient boosting for tabular,
TF-IDF + linear for text (a fine-tuned encoder past ~10k rows), fine-tuning
a pretrained CNN/ViT for images (scratch needs ~1M+ images), temporal
features + GBM for sequences (a transformer only if that baseline loses).
The regulator check hangs off the tabular default, as it does in the code
and the prose, instead of spanning every column.

History: the old sequence box read "features → GBM / only if the GBM loses",
which says the GBM is used only if the GBM loses. The code says the
transformer is the fallback; the box says so now.
"""
from figkit import _esc, Fig, BLUE, GREEN, AMBER, RED, PURPLE, FAINT, MUTED, INK, BORD, SURF, LABEL, SMALL, TINY

TARGET = ('54-model-cheatsheet', 0)

CW, GAP, X0 = 130, 8, 7         # column width, gap, left edge
TY, TH = 82, 28                  # data-type pills
DY, DH = 142, 46                 # default boxes


def draw():
    f = Fig(560, 286, 'msel')
    q = f.box(280 - 92, 18, 184, 32, 'what shape is the data?', stroke=BORD, color=INK, size=LABEL)

    cols = [('tabular', GREEN, 'gradient boosting', 'XGBoost / LightGBM'),
            ('text', BLUE, 'TF-IDF → linear', 'encoder past ~10k rows'),
            ('image', PURPLE, 'fine-tune CNN / ViT', 'scratch needs ~1M+ images'),
            ('sequence', AMBER, 'temporal features → GBM', 'transformer only if it loses')]
    defaults = []
    for i, (name, col, d, sub) in enumerate(cols):
        x = X0 + i * (CW + GAP)
        t = f.box(x + 20, TY, CW - 40, TH, name, stroke=col, color=col, size=LABEL, r=14)
        f.arrow(q.cx + (i - 1.5) * 50, q.b, t.cx, t.t, FAINT, 1.4)
        b = f.box(x, DY, CW, DH, d, sub, stroke=BORD, color=INK, size=LABEL)
        f.connect(t, b, col, 1.5)
        defaults.append(b)

    # the regulator override, hanging off the tabular default
    tab = defaults[0]
    ry, rh, rw = 222, 30, 376
    f.rect(X0, ry, rw, rh, SURF, RED, 6, 1.4)
    f.arrow(tab.cx, tab.b, tab.cx, ry, RED, 1.4, dash='4 3')
    # one line, two colours: the question, then the answer
    qn, ans = 'explained to a regulator?', ' \u00a0→\u00a0 scorecard, or a GBM with monotone constraints + SHAP'
    tx, ty = X0 + rw / 2, ry + rh / 2 + 3.4
    f.raw(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="{LABEL}" text-anchor="middle" font-family="DM Sans">'
          f'<tspan fill="{RED}" font-weight="600">{qn}</tspan><tspan fill="{INK}">{_esc(ans)}</tspan></text>')
    w = len(qn + ans) * LABEL * 0.44           # rendered width (the kit's 0.5 is deliberately generous)
    f.texts.append((tx - w / 2, ty - LABEL * 0.76, tx + w / 2, ty + LABEL * 0.22, qn + ans))

    f.label('A baseline you can ship beats a model you cannot explain.', [(f.w / 2, f.h - 10, 'middle')],
            AMBER, SMALL)
    return f
