const fs=require('node:fs');const path=require('node:path');const assert=require('node:assert/strict');
const {chromium}=require('/Users/kjetil/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const base=__dirname;const out=path.join(base,'images');fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const page=await browser.newPage({viewport:{width:1440,height:1040},deviceScaleFactor:1,reducedMotion:'reduce'});page.setDefaultTimeout(6000);
 const errors=[];page.on('pageerror',e=>errors.push(String(e)));const checks=[];
 await page.route('**/*',async route=>{const u=new URL(route.request().url());if(u.hostname!=='hd0154-preview.test')throw new Error('Unexpected network request');const relative=u.pathname==='/'?'index.html':u.pathname.slice(1);const f=path.resolve(base,relative);if(!f.startsWith(base+path.sep)||!fs.existsSync(f))return route.abort();await route.fulfill({path:f});});
 try{
 await page.goto('http://hd0154-preview.test/');
 await page.waitForSelector('.skeleton-list-row');
 assert.equal(await page.locator('.skeleton-list-row').count(),4);checks.push('Four explicit fixture rows rendered');
 for(const theme of ['dark','light']){
  await page.selectOption('#review-theme',theme);
  for(const state of ['filled','empty','error']){
   await page.selectOption('#review-state',state);
   assert.equal(await page.getByRole('tab',{name:'Filer og mapper',exact:true}).getAttribute('aria-selected'),'true');
   assert.equal(await page.locator('.skeleton-list-row').count(),state==='filled'?4:0);
   await page.screenshot({path:path.join(out,`oversikt-${state}-${theme}-v1.png`),fullPage:true});
  }
 }
 checks.push('Filled, empty and connection-error states rendered in dark/light; Files tab preserved');
 await page.selectOption('#review-state','filled');
 await page.getByRole('combobox',{name:'Maskin',exact:true}).selectOption({label:'Vert'});
 assert.equal(await page.locator('.skeleton-list-row').count(),2);
 assert.match(await page.locator('.skeleton-list').innerText(),/Vert/);
 await page.getByRole('button',{name:'Vis detaljer',exact:true}).last().click();
 assert.match(await page.locator('.skeleton-section').last().innerText(),/eksempel-39/);
 assert.equal(await page.getByRole('tab',{name:'Filer og mapper',exact:true}).getAttribute('aria-selected'),'true');
 checks.push('Host filter yields exactly two rows; row selection updates artifact details without changing tab');
 await page.getByRole('tab',{name:'Relasjoner',exact:true}).click();
 assert.equal(await page.getByRole('tab',{name:'Relasjoner',exact:true}).getAttribute('aria-selected'),'true');
 assert.match(await page.locator('.skeleton-tabs-panel').innerText(),/Claude · bygg 43 → bruker → SwiftPM-cache/);
 await page.selectOption('#review-theme','dark');
 await page.screenshot({path:path.join(out,'relasjoner-dark-v1.png'),fullPage:true});
 await page.getByRole('button',{name:'Vis cachen i filoversikten',exact:true}).click();
 assert.equal(await page.getByRole('tab',{name:'Filer og mapper',exact:true}).getAttribute('aria-selected'),'true');
 assert.match(await page.locator('.skeleton-section').last().innerText(),/SwiftPM · delt byggcache/);
 checks.push('Relationship list leads back to the cache detail; network geometry defect remains recorded for implementation');
 await page.getByRole('tab',{name:'Bevaring',exact:true}).click();
 assert.match(await page.locator('.skeleton-tabs-panel').innerText(),/utløpt frist gir et forslag/);
 await page.screenshot({path:path.join(out,'bevaring-dark-v1.png'),fullPage:true});
 await page.getByRole('tab',{name:'Filer og mapper',exact:true}).click();
 await page.selectOption('#review-state','filled');await page.setViewportSize({width:390,height:844});
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth),false);
 assert.equal(await page.locator('#porthole-skeleton-root').count(),1);
 await page.screenshot({path:path.join(out,'oversikt-filled-mobile-v1.png'),fullPage:false});
 await page.locator('.skeleton-section').last().scrollIntoViewIfNeeded();
 await page.screenshot({path:path.join(out,'detaljer-mobile-v1.png'),fullPage:false});
 checks.push('390px width has no horizontal document overflow');
 assert.deepEqual(errors,[]);
 const skeleton=await page.evaluate(()=>window.reviewSkeleton);fs.writeFileSync(path.join(base,'candidate.skeleton.json'),JSON.stringify(skeleton,null,2)+'\n');
 fs.writeFileSync(path.join(base,'render-result.json'),JSON.stringify({status:'passed',checks,pageErrors:errors,fixtureOnly:true,liveActions:false,rendererRevision:JSON.parse(fs.readFileSync(path.join(base,'sources.json'))).sourceRevision,actions:await page.evaluate(()=>window.reviewActions)},null,2)+'\n');
 console.log(JSON.stringify({status:'passed',checks,images:fs.readdirSync(out)},null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
