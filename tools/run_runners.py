#!/usr/bin/env python3
"""Execute the code inside every interactive .code-runner and fail if any errors.

The runners promise "press Run and it works". Nothing else in the toolchain
opens them, so a card that was fine as static prose can be shipped broken --
that is exactly how 01-linear-algebra reached main with an assert that had
never once been executed (it compared a covariance spectrum against the SVD of
UNCENTRED data).

This runs under CPython + numpy, not Pyodide, so it is a proxy rather than a
guarantee: it catches syntax errors, bad assertions and wrong maths, but not a
package Pyodide happens to lack. Keep runners to numpy/stdlib and the proxy is
tight. Usage: python3 tools/run_runners.py [topic ...]
"""
import ast, html, pathlib, re, subprocess, sys, tempfile

# the runner block, so data-packages and the code stay associated
RUNNER = re.compile(
    r'<div class="code-runner"[^>]*id="(?P<rid>[^"]+)"(?P<attrs>[^>]*)>'
    r'.*?<textarea class="code-input">(?P<code>.*?)</textarea>', re.S)
THIRD = {'numpy', 'pandas', 'scipy', 'sklearn', 'matplotlib', 'statsmodels'}
PIP = {'sklearn': 'scikit-learn'}          # import name -> distribution name


def imports_of(code):
    """Third-party top-level modules the code actually imports."""
    mods = set()
    for n in ast.walk(ast.parse(code)):
        if isinstance(n, ast.Import):
            for a in n.names:
                mods.add(a.name.split('.')[0])
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            mods.add(n.module.split('.')[0])
    return mods & THIRD


def declared(attrs):
    m = re.search(r'data-packages="([^"]*)"', attrs)
    return {x.strip() for x in m.group(1).split(',') if x.strip()} if m else {'numpy'}


def scan(paths):
    for p in paths:
        for m in RUNNER.finditer(p.read_text()):
            yield p, m.group('rid'), declared(m.group('attrs')), html.unescape(m.group('code'))


# `--packages` prints the pip install list CI needs, derived from the runners
if '--packages' in sys.argv:
    need = set()
    for _, _, dec, _ in scan(sorted(pathlib.Path('topics').glob('*.html'))):
        need |= dec
    print(' '.join(sorted(PIP.get(x, x) for x in need)))
    raise SystemExit(0)

names = [a for a in sys.argv[1:] if not a.startswith('-')]
paths = ([pathlib.Path('topics/%s.html' % n) for n in names] if names
         else sorted(pathlib.Path('topics').glob('*.html')))

bad = total = 0
for p, rid, dec, code in scan(paths):
    total += 1

    # A runner must DECLARE every package it imports: data-packages is what the
    # browser loads into Pyodide, so an undeclared import is a ModuleNotFoundError
    # for the reader even when it runs fine here. This is not hypothetical --
    # 45-credit-risk and 49-responsible-ai both imported pandas and declared only
    # numpy, and only CI (which installs exactly the declared set) caught it.
    missing = imports_of(code) - dec
    if missing:
        bad += 1
        print('FAIL %s (%s): imports %s but data-packages="%s"'
              % (p.stem, rid, ','.join(sorted(missing)), ','.join(sorted(dec))))
        continue

    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
        f.write(code)
        tmp = f.name
    r = subprocess.run([sys.executable, tmp], capture_output=True, text=True, timeout=180)
    if r.returncode:
        bad += 1
        print('FAIL %s (%s)' % (p.stem, rid))
        for line in (r.stderr or '').strip().splitlines()[-4:]:
            print('       ' + line)
    else:
        print('  ok %s' % p.stem)

print('\n%d runner(s) executed, %d failed' % (total, bad))
sys.exit(1 if bad else 0)
