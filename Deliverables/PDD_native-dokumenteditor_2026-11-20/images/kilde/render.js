const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();
const jobs=[["iphone","tom",393,852],["iphone","fylt",393,852],["iphone","frakoblet",393,852],["iphone","kommentarer",393,852],["mac","tom",1280,800],["mac","fylt",1280,800],["mac","frakoblet",1280,800]];
for(const [d,s,w,h] of jobs){const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:2});
await p.goto('file://'+path.resolve(__dirname,'mockup.html')+`?d=${d}&s=${s}`);
const name=s==="kommentarer"?`kommentarer-${d}-v1.png`:`editor-${s}-${d}-v1.png`;
await p.screenshot({path:path.resolve(__dirname,'..',name)});await p.close();console.log(name);}
await b.close();})();
