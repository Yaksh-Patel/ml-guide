from html.parser import HTMLParser
import pathlib, sys

class C(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.st=[]; self.ex=[]; self.raw=None
    def handle_starttag(self, t, a):
        if self.raw: return
        if t in ('textarea','script','pre','style'): self.raw = t
        if t in ('div','section'): self.st.append((t, self.getpos()[0]))
    def handle_endtag(self, t):
        if self.raw:
            if t == self.raw: self.raw = None
            return
        if t in ('div','section'):
            if self.st and self.st[-1][0] == t: self.st.pop()
            else: self.ex.append((t, self.getpos()[0]))

TBL = 'class="tbl'
names = sys.argv[1:]
if names == ['--all'] or not names:
    names = sorted(q.stem for q in pathlib.Path('topics').glob('*.html'))
bad = 0
for name in names:
    p = pathlib.Path(f'topics/{name}.html')
    s = p.read_text(); c = C(); c.feed(s)
    ok = (not c.st and not c.ex and s.count('$$') % 2 == 0 and s.count('<section') == 1)
    if not ok: bad += 1
    print('  %-22s ok=%-5s bytes=%6d  svg=%d  tbl=%d  code=%d  cards=%d'
          % (name, ok, len(s), s.count('<svg'), s.count(TBL),
             1 if ('language-python' in s or 'class="code-runner' in s) else 0,
             s.count('<div class="card')))
    if not ok:
        print('       unclosed:', c.st, ' extra:', c.ex, ' $$:', s.count('$$'))
sys.exit(1 if bad else 0)
