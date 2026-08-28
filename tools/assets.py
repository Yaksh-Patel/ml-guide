#!/usr/bin/env python3
"""Asset accounting for the revamp: never silently drop an interactive block.

Usage:  python3 tools/assets.py <baseline-commit> <topic> [<topic> ...]
        python3 tools/assets.py cdf20c9 --all

Prints anim / svg / script / code-runner / table / pre counts before and after.
ANY COUNT GOING DOWN IS A LOST ASSET, not a simplification. Two widgets were
nearly lost this way:
  * 06-bias-variance  wrapper carries a style attribute, so `<div class="anim-wrap">`
                      as a literal did not match
  * 09-confusion-roc  the widget's <script> sits OUTSIDE the wrapper div, so a
                      div-depth walk alone dropped it
blocks() below handles both. Use it, not a hand-rolled regex.

cdf20c9 is the commit immediately BEFORE the prose revamp began — the right
baseline for checking that a rewrite kept everything.
"""
import re, subprocess, sys, pathlib

TBL = 'class="tbl'

def counts(src):
    return dict(anim=src.count('anim-wrap'), svg=src.count('<svg'),
                script=src.count('<script'), runner=src.count('code-runner'),
                tbl=src.count(TBL), pre=src.count('<pre'))

def fmt(c):
    return ' '.join('%s=%d' % (k, v) for k, v in c.items())

def blocks(src):
    """Every anim-wrap / code-runner block, matched by div depth so wrappers
    carrying style attributes and inner <script> tags are captured too.

    Two subtleties, both learned from real breakage:
      * `code-runner\b` ALSO matches `code-runner-header`, because '-' is a
        non-word character. That returned a widget's own header as a separate
        "block" nested inside it, and substituting both placeholders duplicated
        the header. Hence the (?=["\s]) lookahead: the class name must end
        there. Affected 28-loss-functions and 29-backpropagation.
      * Belt and braces, any span wholly contained in another is dropped, so
        nesting can never produce duplicate substitutions again regardless of
        how a class gets named in future.
    """
    spans = []
    for m in re.finditer(r'<div class="(?:anim-wrap|code-runner)(?=["\s])[^>]*>', src):
        start, depth = m.start(), 0
        for d in re.finditer(r'<div\b[^>]*>|</div>', src[start:]):
            depth += 1 if d.group(0).startswith('<div') else -1
            if depth == 0:
                end = start + d.end()
                # a widget's <script> often sits immediately AFTER its wrapper
                tail = src[end:end + 400]
                if tail.lstrip().startswith('<script'):
                    end = src.index('</script>', end) + len('</script>')
                spans.append((start, end))
                break
    # drop any span strictly inside another (compare by position, not content,
    # so two identical widgets are both kept)
    keep = [(a, b) for (a, b) in spans
            if not any((c <= a and b <= d) and (c, d) != (a, b) for (c, d) in spans)]
    return [src[a:b] for a, b in sorted(keep)]

def codecard(src):
    m = re.search(r'<div class="card cc"><div class="card-title">In code</div>.*?</code></pre></div>', src, re.S)
    return m.group(0) if m else ''

def tables(src):
    return re.findall(r'<table class="tbl"[^>]*>.*?</table>', src, re.S)

if __name__ == '__main__':
    base = sys.argv[1]
    args = sys.argv[2:]
    if args == ['--all']:
        args = sorted(q.stem for q in pathlib.Path('topics').glob('*.html'))
    print('%-24s %-46s %s' % ('topic', 'before (' + base[:7] + ')', 'after'))
    n_lost = 0
    for name in args:
        p = 'topics/%s.html' % name
        old = subprocess.run(['git', 'show', '%s:%s' % (base, p)],
                             capture_output=True, text=True).stdout
        if not old:
            print('%-24s (not in %s -- new topic, nothing to compare)' % (name, base[:7]))
            continue
        new = pathlib.Path(p).read_text()
        co, cn = counts(old), counts(new)
        lost = {k: (co[k], cn[k]) for k in co if cn[k] < co[k]}
        flag = ('   LOST ' + str(lost)) if lost else ''
        if lost:
            n_lost += 1
        print('%-24s %-46s %s%s' % (name, fmt(co), fmt(cn), flag))
    if n_lost:
        print('\nFAIL: %d topic(s) lost an asset against %s.' % (n_lost, base[:7]))
        print('A count going down is a lost diagram/table/widget, not a simplification.')
    sys.exit(1 if n_lost else 0)
