const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',headless:true}).catch(()=>chromium.launch({headless:true}));
const p=await b.newPage({viewport:{width:1100,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
const shots=[['register','fylt'],['register','tom'],['register','utdatert'],['register','selskap'],['lager','ikke-satt-opp'],['lager','satt-opp'],['lager','feil']];
for(const [v,s] of shots){await p.goto('file://'+__dirname+'/mockup.html?view='+v+'&state='+s);await p.screenshot({path:__dirname+`/images/${v==='lager'?'mitt-lager':'register'}-${s}-v1.png`,fullPage:true});}
await p.setViewportSize({width:390,height:844});await p.goto('file://'+__dirname+'/mockup.html?view=register&state=fylt');
const of=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth);await p.screenshot({path:__dirname+'/images/register-smal-v1.png',fullPage:true});
console.log(JSON.stringify({shots:shots.length+1,errs,overflow:of}));await b.close()})().catch(e=>{console.error(e);process.exit(1)});
