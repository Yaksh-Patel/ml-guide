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
import html, pathlib, re, subprocess, sys, tempfile

TA = re.compile(r'<textarea class="code-input">(.*?)</textarea>', re.S)

names = sys.argv[1:]
paths = ([pathlib.Path('topics/%s.html' % n) for n in names] if names
         else sorted(pathlib.Path('topics').glob('*.html')))

bad = total = 0
for p in paths:
    src = p.read_text()
    for i, block in enumerate(TA.findall(src)):
        total += 1
        code = html.unescape(block)
        with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
            f.write(code)
            tmp = f.name
        r = subprocess.run([sys.executable, tmp], capture_output=True, text=True, timeout=180)
        tag = '%s[%d]' % (p.stem, i) if i else p.stem
        if r.returncode:
            bad += 1
            print('FAIL %s' % tag)
            for line in (r.stderr or '').strip().splitlines()[-4:]:
                print('       ' + line)
        else:
            print('  ok %s' % tag)

print('\n%d runner(s) executed, %d failed' % (total, bad))
sys.exit(1 if bad else 0)
