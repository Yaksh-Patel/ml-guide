#!/usr/bin/env python3
"""Render figure modules and swap them into their topics.

    python3 tools/figures/build.py              # every module in tools/figures/
    python3 tools/figures/build.py f06_0 f29_1  # named modules
    python3 tools/figures/build.py --check      # render + check layout only, write nothing
    python3 tools/figures/build.py --verify     # also fail if a topic's svg differs from
                                                # what its module renders (CI)

Each module sets TARGET = ('06-bias-variance', 0) — topic file stem and the
index of the .anim-wrap in that file — and defines draw() -> figkit.Fig.
Only the first <svg>…</svg> inside that .anim-wrap is replaced; the wrapper,
its caption (.anim-title) and anything else in it are left exactly as they are.
"""
import importlib, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))


def wraps(src):
    """(start, end) of each top-level .anim-wrap div, matched by depth."""
    out = []
    for m in re.finditer(r'<div class="anim-wrap"[^>]*>', src):
        depth = 0
        for t in re.finditer(r'<div\b[^>]*>|</div>', src[m.start():]):
            depth += 1 if t.group(0).startswith('<div') else -1
            if depth == 0:
                out.append((m.start(), m.start() + t.end()))
                break
    # drop nested ones
    return [(a, b) for (a, b) in out if not any(c < a and b < d for (c, d) in out)]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    verify = '--verify' in sys.argv
    check_only = '--check' in sys.argv or verify
    mods = args or sorted(p.stem for p in HERE.glob('f*.py'))
    failed = False
    for name in mods:
        mod = importlib.import_module(name)
        fig = mod.draw()
        errs = fig.check()
        if errs:
            failed = True
            print(f'!! {name}: {len(errs)} layout problem(s)')
            for e in errs:
                print('     ', e)
            continue
        stem, idx = mod.TARGET
        path = ROOT / 'topics' / f'{stem}.html'
        src = path.read_text()
        a, b = wraps(src)[idx]
        block = src[a:b]
        s0 = block.index('<svg')
        s1 = block.index('</svg>', s0) + len('</svg>')
        new_block = block[:s0] + fig.svg() + block[s1:]
        if new_block == block:
            print(f'== {name}: up to date')
            continue
        if verify:
            # the topic no longer matches its module: someone edited the svg by
            # hand, or changed the module without running build.py
            failed = True
            print(f'!! {name}: {stem}.html figure {idx} differs from what the module renders; run build.py {name}')
            continue
        if check_only:
            print(f'ok {name} -> {stem}.html figure {idx} (not written)')
            continue
        path.write_text(src[:a] + new_block + src[b:])
        print(f'++ {name} -> {stem}.html figure {idx}')
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
