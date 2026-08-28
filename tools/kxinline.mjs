import katex from 'katex'; import fs from 'fs'; import path from 'path';
const root=process.argv[2]; let n=0,warn=0,bad=0;
for (const f of fs.readdirSync(root+'/topics').filter(x=>x.endsWith('.html')).sort()) {
  let s=fs.readFileSync(path.join(root,'topics',f),'utf8');
  s=s.replace(/<textarea[\s\S]*?<\/textarea>/g,'').replace(/<pre[\s\S]*?<\/pre>/g,'')
     .replace(/<script[\s\S]*?<\/script>/g,'').replace(/<svg[\s\S]*?<\/svg>/g,'')
     .replace(/\$\$[\s\S]*?\$\$/g,'');            // drop display blocks
  // per text node, exactly how KaTeX auto-render sees it
  const unesc = t => t.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"')
                      .replace(/&#x27;|&apos;/g,"'").replace(/&nbsp;/g,' ').replace(/&amp;/g,'&');
  // the browser decodes entities BEFORE KaTeX sees the text node -- match that
  for (const node of s.split(/<[^>]*>/).map(unesc)) {
    for (const m of node.match(/\$[^$\n]+\$/g)||[]) { n++;
      try { katex.renderToString(m.slice(1,-1),{displayMode:false,throwOnError:true,strict:'error'}); }
      catch(e){ const st=/Unrecognized Unicode|LaTeX-incompatible/.test(e.message);
        if(st) warn++; else bad++;
        console.log(`${st?'STRICT':'FAIL'} ${f}: ${e.message.slice(0,100)}\n   ${m.slice(0,80)}`); } }
  }
}
console.log(`\n${n} inline formulas: ${bad} hard failures, ${warn} strict warnings`);
if (bad || warn) { console.log('FAIL: every inline $...$ must compile under strict:\'error\'.'); process.exit(1); }
