const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900},deviceScaleFactor:2});
for (const n of ['utviklerbenk-fylt','utviklerbenk-tom','admin-utgivelser']){await p.goto('file://'+process.cwd()+'/'+n+'.html');await p.screenshot({path:n+'-v1.png',fullPage:true});}
await b.close();})();
