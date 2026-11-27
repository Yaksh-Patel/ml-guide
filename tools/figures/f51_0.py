"""51 MLOps: serving a model on Kubernetes.

Clients → load balancer (Service / Ingress) → the Pods of one Deployment.
The supporting pieces point INTO the Deployment with what they supply:
features from the feature store, weights from the registry at startup, and a
replica count from the HPA, which is shown adding a fourth Pod. The old figure
used 7-unit text that overflowed its boxes, left the registry unconnected and
drew the HPA as a box hanging off Pod 2.
"""
from figkit import Fig, BLUE, GREEN, PURPLE, AMBER, FAINT, MUTED, INK, SURF, BORD, LABEL, SMALL, TINY

TARGET = ('51-mlops', 0)


def draw():
    f = Fig(560, 262, 'k8s')

    cl = f.box(12, 112, 74, 40, 'Clients', 'HTTP requests', stroke=BORD, color=INK, size=LABEL)
    lb = f.box(112, 109, 98, 46, 'Load balancer', 'Service / Ingress', stroke=BLUE, color=BLUE, size=LABEL)

    # the Deployment and its Pods
    gx, gy, gw, gh = 238, 26, 118, 206
    f.raw(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="10" fill="none" stroke="{FAINT}" '
          f'stroke-width="1.2" stroke-dasharray="5 4"/>',
          pts=[(gx, gy), (gx + gw, gy), (gx + gw, gy + gh), (gx, gy + gh), (gx, gy)])
    pods = []
    for i in range(3):
        pods.append(f.box(gx + 14, gy + 12 + i * 48, 90, 38, f'Pod {i + 1}', 'model-server :8080',
                          stroke=GREEN, color=GREEN, size=LABEL))
    # the Pod the HPA adds
    px, py = gx + 14, gy + 12 + 3 * 48
    f.raw(f'<rect x="{px}" y="{py}" width="90" height="38" rx="6" fill="{SURF}" stroke="{GREEN}" '
          f'stroke-width="1.2" stroke-dasharray="4 3" opacity=".7"/>',
          pts=[(px, py), (px + 90, py), (px + 90, py + 38), (px, py + 38), (px, py)])
    f.text(px + 45, py + 17, 'Pod 4', GREEN, LABEL, 'middle', weight=600, halo=False)
    f.text(px + 45, py + 30, 'added on load', MUTED, TINY, 'middle', halo=False)

    f.connect(cl, lb)
    for p in pods:                       # fan out from one point on the balancer
        f.arrow(lb.r, lb.cy, p.l, p.cy)
    f.arrow(lb.r, lb.cy, px, py + 19, dash='3 3')

    # what feeds the Deployment
    rx, rw = 408, 140
    fs = f.box(rx, 40, rw, 40, 'Feature store', 'Redis / Feast', stroke=BORD, color=INK, size=LABEL)
    mr = f.box(rx, 106, rw, 40, 'Model registry', 'MLflow / S3', stroke=BORD, color=INK, size=LABEL)
    hpa = f.box(rx, py - 3, rw, 44, 'HPA', 'Horizontal Pod Autoscaler', stroke=PURPLE, color=PURPLE, size=LABEL)
    gr = gx + gw
    f.arrow(fs.l, fs.cy, gr, fs.cy, BLUE)
    f.arrow(mr.l, mr.cy, gr, mr.cy, AMBER)
    f.arrow(hpa.l, py + 19, gr, py + 19, PURPLE, dash='4 3')

    # labels last
    mid = (gr + rx) / 2
    f.label('Deployment', [(gx + gw / 2, gy - 8, 'middle')], FAINT, SMALL)
    f.label('features', [(mid, fs.cy - 7, 'middle')], BLUE, TINY)
    f.label('weights', [(mid, mr.cy - 7, 'middle')], AMBER, TINY)
    f.label('replicas', [(mid, py + 12, 'middle')], PURPLE, TINY)
    f.label('a saturated GPU server can sit at 30% CPU: scale on requests/s or GPU use, not CPU',
            [(f.w / 2, 254, 'middle')], AMBER, SMALL)
    return f
