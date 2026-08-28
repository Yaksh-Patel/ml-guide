#!/usr/bin/env python3
"""Section-8 gotcha audits of REVAMP-PLAN.md, in one pass.

Usage:  python3 tools/audit_markup.py            # all topics
        python3 tools/audit_markup.py 46-gnns    # named topics

check_topics.py deliberately watches only div/section, because those are the
only tags the router depends on. This catches the rest of section 8:
  1. full tag balance over EVERY tag (not just div/section)
  2. .bl labels: must close immediately, contain no <p>
  3. boxes found by regex-with-attrs and depth-matched (style attrs don't hide them)
  4. two '$' inside one text node -> KaTeX renders prose as inline maths
"""
from html.parser import HTMLParser
import pathlib, sys, re

VOID = {'area','base','br','col','embed','hr','img','input','link','meta',
        'param','source','track','wbr','path','circle','line','rect','polygon',
        'polyline','ellipse','use','stop','image'}
RAW  = {'pre','script','textarea','style'}

class Bal(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.st=[]; self.err=[]; self.raw=None; self.svg=0
    def handle_starttag(self,t,a):
        if self.raw: return
        if t in RAW: self.raw=t; return
        if t=='svg': self.svg+=1
        if self.svg or t in VOID: return
        self.st.append((t,self.getpos()[0]))
    def handle_startendtag(self,t,a): pass
    def handle_endtag(self,t):
        if self.raw:
            if t==self.raw: self.raw=None
            return
        if t=='svg':
            self.svg=max(0,self.svg-1); return
        if self.svg or t in VOID: return
        if self.st and self.st[-1][0]==t: self.st.pop()
        else: self.err.append(('extra </%s>'%t, self.getpos()[0]))

class Dollars(HTMLParser):
    """KaTeX matches $...$ inside ONE text node. The bug signature is not
    'two dollars in a node' -- intentional inline maths does that constantly --
    it is an ODD number of '$', or a would-be math span whose content reads as
    prose (two or more plain words, no LaTeX control characters)."""
    WORD = re.compile(r'[A-Za-z]{2,}')
    def __init__(self):
        super().__init__(convert_charrefs=True); self.hits=[]; self.raw=None
    def handle_starttag(self,t,a):
        if t in RAW: self.raw=t
    def handle_endtag(self,t):
        if self.raw and t==self.raw: self.raw=None
    def handle_data(self,d):
        # a lone '$' in its own text node can never pair -- that IS the fix
        if self.raw or '$$' in d or d.count('$') < 2: return
        flat = re.sub(r'\s+',' ',d.strip())
        if d.count('$') % 2:
            self.hits.append('odd $ count: %r' % flat[:110]); return
        for seg in d.split('$')[1::2]:            # the would-be math spans
            if any(c in seg for c in '\\^_{}'): continue
            if len(self.WORD.findall(seg)) >= 2:
                self.hits.append('prose inside $...$: %r' % re.sub(r'\s+',' ',seg)[:80])

def boxes(s):
    out=[]
    for m in re.finditer(r'<div class="box [a-z ]+"[^>]*>', s):
        start,depth=m.start(),0
        for d in re.finditer(r'<div\b[^>]*>|</div>', s[start:]):
            depth += 1 if d.group(0).startswith('<div') else -1
            if depth==0:
                out.append(s[start:start+d.end()]); break
    return out

names=sys.argv[1:]
if not names or names==['--all']:
    names=sorted(q.stem for q in pathlib.Path('topics').glob('*.html'))
bad=0
tot_box=0
for n in names:
    s=pathlib.Path('topics/%s.html'%n).read_text()
    b=Bal(); b.feed(s)
    probs=[]
    if b.st:  probs.append('unclosed %s'%b.st[:4])
    if b.err: probs.append('%s'%b.err[:4])
    # .bl labels
    for m in re.finditer(r'<div class="bl">', s):
        seg=s[m.start():m.start()+400]
        e=seg.find('</div>')
        lab=seg[:e] if e>=0 else seg
        if e<0: probs.append('bl never closes')
        elif '<p' in lab or '<div' in lab[len('<div class="bl">'):]:
            probs.append('bl contains block markup: %r'%lab[:70])
    bx=boxes(s); tot_box+=len(bx)
    for x in bx:
        if '<div class="bl">' in x and x.count('</div>')<2:
            probs.append('box label malformed')
    d=Dollars(); d.feed(s)
    for h in d.hits: probs.append('prose $..$: %r'%h)
    if s.count('$$')%2: probs.append('odd $$')
    if probs:
        bad+=1; print('FAIL %-24s'%n); [print('    -',p) for p in probs]
print('checked %d topics, %d boxes, %d with problems'%(len(names),tot_box,bad))
sys.exit(1 if bad else 0)
