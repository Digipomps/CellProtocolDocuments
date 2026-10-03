const fs=require('fs'); const {GUESTS,run}=require('./model.js');
const md=fs.readFileSync(process.argv[2],'utf8');
// Sett-parametre
const sets={}; for (const m of md.matchAll(/^\| (S\d{3}) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|$/gm)){
  const f=i=>parseFloat(m[i].replace(',','.'));
  sets[m[1]]={approach:f(2),threshold:f(3),negativeScale:f(4),reinforce:f(5),wantToTaste:f(6),interesting:f(7),notForMe:f(8),ownWords:f(9),cap:f(10)};
}
const secs=md.split(/^## (\d)\. .*$/m); let checked=0, bad=0;
for (let i=1;i<secs.length;i+=2){
  const g=GUESTS[+secs[i]-1]; const body=secs[i+1];
  for (const row of body.matchAll(/^\| G\d{3} \/ ([S\d, ]+) \| (.*?) \| (\d+) \| (.*?) \|/gm)){
    const ids=row[1].split(', ');
    const exp=row[2]==='Ingen'?[]:row[2].split('<br>').map(x=>{const mm=x.match(/`(.*?)` \(sum ([\d,\-]+)\)/);return [mm[1],parseFloat(mm[2].replace(',','.'))];});
    const closed=row[4]==='Ingen'?[]:[...row[4].matchAll(/`(.*?)`/g)].map(x=>x[1]);
    for (const s of ids){ const r=run(g,sets[s]); checked++;
      const got=r.offers.map(o=>[o.id,o.sum]);
      const same=got.length===exp.length && got.every((x,k)=>x[0]===exp[k][0]&&Math.abs(x[1]-exp[k][1])<1e-12) && JSON.stringify(r.closed)===JSON.stringify(closed);
      if(!same){bad++; console.log('AVVIK',secs[i],s,JSON.stringify(got),JSON.stringify(exp),r.closed,closed);}
    }
  }
}
console.log('sett', Object.keys(sets).length, 'kontrollert', checked, 'avvik', bad);
