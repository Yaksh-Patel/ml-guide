import katex from 'katex'; import fs from 'fs'; import path from 'path';
const root=process.argv[2]; let n=0,warn=0,bad=0;
for (const f of fs.readdirSync(root+'/topics').filter(x=>x.endsWith('.html'))) {
  const s=fs.readFileSync(path.join(root,'topics',f),'utf8');
  const clean=s.replace(/<textarea[\s\S]*?<\/textarea>/g,'').replace(/<pre[\s\S]*?<\/pre>/g,'').replace(/<script[\s\S]*?<\/script>/g,'');
  for (const m of clean.match(/\$\$[\s\S]*?\$\$/g)||[]) { n++;
    try { katex.renderToString(m.slice(2,-2),{displayMode:true,throwOnError:true,strict:'error'}); }
    catch(e){ if(/Unrecognized Unicode|LaTeX-incompatible/.test(e.message)){warn++; console.log(`STRICT ${f}: ${e.message.slice(0,90)}\n   ${m.slice(0,90)}`);} else {bad++; console.log(`FAIL ${f}: ${e.message}`);} } }
}
console.log(`\n${n} display formulas: ${bad} hard failures, ${warn} strict-mode warnings`);
if (bad || warn) { console.log('FAIL: every $$ block must compile under strict:\'error\'.'); process.exit(1); }
