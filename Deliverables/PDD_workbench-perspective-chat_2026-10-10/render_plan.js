const fs=require('fs');
const path=require('path');
const crypto=require('crypto');
const {chromium}=require('playwright');
(async()=>{
 const root=__dirname;
 if(!process.env.CHROMIUM_PATH) throw new Error('Set CHROMIUM_PATH to an existing approved browser; no download.');
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH});
 try {
  const page=await browser.newPage({viewport:{width:1880,height:980},deviceScaleFactor:1});
  const failures=[];
  page.on('pageerror',e=>failures.push(e.message));
  await page.route('**/*',route=>route.abort());
  await page.setContent(fs.readFileSync(path.join(root,'images/plan-g2-v1.html'),'utf8'),{waitUntil:'load'});
  await page.screenshot({path:path.join(root,'images/plan-g2-v1.png'),fullPage:true});
  if(failures.length) throw new Error(JSON.stringify(failures));
  const buf=fs.readFileSync(path.join(root,'images/plan-g2-v1.png'));
  const receipt={scope:'G2 plan diagram; separate from approved product GUI',image:'images/plan-g2-v1.png',sha256:crypto.createHash('sha256').update(buf).digest('hex'),bytes:buf.length,viewport:{width:1880,height:980},browser:await browser.version(),pageErrors:failures,productTests:'not run'};
  fs.writeFileSync(path.join(root,'evidence/plan-image.json'),JSON.stringify(receipt,null,2)+'\n');
  console.log(JSON.stringify(receipt));
 } finally { await browser.close(); }
})().catch(e=>{console.error(e.message);process.exitCode=1;});
