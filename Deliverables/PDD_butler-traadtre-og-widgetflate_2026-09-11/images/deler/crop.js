const path=require('path'); const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const M='file:///mnt/user-data/outputs/g1gui/mockup.html';
  const jobs = [
    // [outname, url, viewport, selector]
    ...['fylt','tom','feil','drag'].flatMap(st => [
      [`tre-web-${st==='drag'?'dra':st}`,  M+(st==='fylt'?'':`?state=${st}`), [2000,1250], '.panel.rail'],
      [`chat-web-${st==='drag'?'dra':st}`, M+(st==='fylt'?'':`?state=${st}`), [2000,1250], '.panel.chat'],
      [`flate-web-${st==='drag'?'dra':st}`,M+(st==='fylt'?'':`?state=${st}`), [2000,1250], '.panel.canvas'],
    ]),
    ['topbar-web-fylt', M, [2000,1250], '.topbar'],
    ['chat-web-full-dokket', M+'?state=full', [2000,1250], '.panel.chat'],
    ['flate-web-full', M+'?state=full', [2000,1250], '.panel.canvas'],
    ...['normal','drag','tom'].flatMap(st => [
      [`topbar-app-${st==='drag'?'dra':st}`, M+'?viewport=app'+(st==='normal'?'':`&state=${st}`), [780,1688], '.topbar'],
      [`chat-app-${st==='drag'?'dra':st}`,   M+'?viewport=app'+(st==='normal'?'':`&state=${st}`), [780,1688], '.panel.chat'],
      [`flate-app-${st==='drag'?'dra':st}`,  M+'?viewport=app'+(st==='normal'?'':`&state=${st}`), [780,1688], '.panel.canvas'],
    ]),
  ];
  for (const [n,u,[w,h],sel] of jobs) {
    const p = await b.newPage({ viewport:{width:w,height:h}, deviceScaleFactor:1 });
    await p.goto(u); await p.waitForTimeout(150);
    const el = await p.$(sel); const box = await el.boundingBox();
    await el.screenshot({ path: path.join(__dirname,'deler',`${n}.png`) });
    console.log(n, Math.round(box.width)+'x'+Math.round(box.height));
    await p.close();
  }
  await b.close();
})();
