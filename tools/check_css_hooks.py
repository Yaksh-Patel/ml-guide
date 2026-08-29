#!/usr/bin/env python3
"""Every class the JS adds must be consumed by a CSS rule.

This exists because of a real bug. codemirror-init.js did:

    runner.classList.add('cm-active-runner');   // "Hide the raw textarea, show CM"

and no CSS rule ever matched that class. The raw <textarea> therefore stayed
visible underneath the mounted CodeMirror editor, so every runnable code block
displayed its code TWICE, both copies editable, and only the CodeMirror one was
the copy runCode() actually read. Nothing errored; the class was simply dead.

A dead class hook is invisible to a smoke test -- jsdom applies no stylesheets --
so this is a static check instead. Usage: python3 tools/check_css_hooks.py
"""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
css = ''.join(p.read_text() for p in sorted(root.glob('assets/**/*.css')))
# strip comments first: a class named only in a comment is not consumed by
# anything, and this check found itself passing on its own explanatory note
css = re.sub(r'/\*.*?\*/', ' ', css, flags=re.S)
dead = []
seen = 0

for js in sorted(root.glob('assets/**/*.js')):
    src = js.read_text()
    for m in re.finditer(r"classList\.(?:add|toggle)\(\s*'([A-Za-z][\w-]*)'", src):
        cls = m.group(1)
        seen += 1
        if not re.search(r'\.' + re.escape(cls) + r'\b', css):
            line = src[:m.start()].count('\n') + 1
            dead.append((cls, js.relative_to(root), line))

for cls, f, line in dead:
    print("FAIL %s:%d adds '%s' but no CSS rule matches it" % (f, line, cls))
print('%d class hook(s) checked, %d dead' % (seen, len(dead)))
sys.exit(1 if dead else 0)
