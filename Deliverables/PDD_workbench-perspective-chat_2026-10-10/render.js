// Offline design harness using unchanged CellScaffold origin/main renderer.
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const {chromium} = require('playwright');
const ROOT=__dirname, OUT=path.join(ROOT,'skeleton'), IMG=path.join(ROOT,'images');
const read=f=>JSON.parse(fs.readFileSync(path.join(OUT,f),'utf8'));
fs.mkdirSync(IMG,{recursive:true});
function html(theme) {
  return `<!doctype html><html lang="nb"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Workbench hjelpechat · designkandidat</title><link rel="stylesheet" href="/porthole-webo.css"><link rel="stylesheet" href="/developer-workbench.css"><link rel="stylesheet" href="/candidate.css">
  <style>html{color-scheme:${theme}}body{margin:0;background:${theme==='dark'?'#1c1c1f':'#f5f5f7'};font:14px/1.5 -apple-system,BlinkMacSystemFont,'Helvetica Neue',sans-serif}
  .canvas{padding:0;border:0;border-radius:0}#fixture-label{padding:6px 18px;background:${theme==='dark'?'#42424a':'#e4e4e9'};color:${theme==='dark'?'#fff':'#333'};font-size:11px;letter-spacing:.03em}
  </style><body><div id="fixture-label">DESIGNKANDIDAT · EKSEMPELDATA · INGEN MODELLER ELLER JOBBER KJØRES</div>
  <main class="canvas view-mode"><div id="porthole-skeleton-root" data-workbench-theme="${theme}" class="skeleton-host"></div></main>
  <script src="/haven-localization.js"></script><script src="/skeleton-runtime.js"></script></body></html>`;
}
async function makePage(browser,shot) {
  const page=await browser.newPage({viewport:{width:shot.width,height:shot.height},deviceScaleFactor:1});
  const errors=[];
  page.on('pageerror', e=>errors.push(String(e)));
  page.on('console', m=>{if(['warning','error'].includes(m.type()))errors.push(m.text())});
  await page.route('**/*',async route=>{
    const u=new URL(route.request().url());
    if(u.hostname!=='workbench.design.test')return route.abort();
    if(u.pathname==='/')return route.fulfill({contentType:'text/html',body:html(shot.theme)});
    if(u.pathname==='/candidate.css')return route.fulfill({path:path.join(ROOT,'candidate.css'),contentType:'text/css'});
    if(['/skeleton-runtime.js','/haven-localization.js','/porthole-webo.css','/developer-workbench.css'].includes(u.pathname))
      return route.fulfill({path:path.join(ROOT,'renderer',u.pathname.slice(1)),contentType:u.pathname.endsWith('.css')?'text/css':'application/javascript'});
    return route.abort();
  });
  await page.goto('http://workbench.design.test/');
  const cfg=read(shot.configuration), state=read(shot.state);
  await page.evaluate(({skeleton,state,width,height})=>{
    window.__actions=[];window.__fixture=state;
    window.__renderer=window.HavenSkeletonRuntime.createRenderer({rootElement:document.getElementById('porthole-skeleton-root'),skeleton,
      onAction:async(keypath,payload,meta)=>{window.__actions.push({keypath,payload,meta});return {status:'fixture-recorded',effectExecuted:false}}});
    window.__renderer.setLayoutContext({availableWidth:width,availableHeight:height,
      capabilities:width<700?['touch']:['pointer','hover','keyboard','drag']});
    window.__renderer.update(state);
  },{skeleton:cfg.skeleton,state,width:shot.width,height:shot.height});
  await page.waitForTimeout(150);
  return {page,errors};
}
async function inspect(page) {
  return page.evaluate(()=>{
    const rgb=c=>(c.match(/[\d.]+/g)||[]).slice(0,3).map(Number);
    const lum=c=>rgb(c).map(v=>{v/=255;return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4)}).reduce((s,v,i)=>s+v*[0.2126,0.7152,0.0722][i],0);
    const contrast=[];
    for(const el of document.querySelectorAll('.skeleton-text,.skeleton-picker-label,button,input,textarea,select')){
      if(!el.getBoundingClientRect().width)continue;
      const s=getComputedStyle(el);let parent=el,bg='rgb(255,255,255)';
      while(parent){const candidate=getComputedStyle(parent).backgroundColor;if(candidate!=='rgba(0, 0, 0, 0)'&&candidate!=='transparent'){bg=candidate;break;}parent=parent.parentElement;}
      const a=lum(s.color),b=lum(bg);const ratio=(Math.max(a,b)+0.05)/(Math.min(a,b)+0.05);
      contrast.push({text:(el.textContent||el.placeholder||'').slice(0,60),ratio:Math.round(ratio*100)/100,foreground:s.color,background:bg});
    }
    const controls=[...document.querySelectorAll('button,input,textarea,select')].map(e=>({
      tag:e.tagName,text:e.textContent?.trim()||e.getAttribute('placeholder'),disabled:e.disabled,
      visible:e.getBoundingClientRect().width>0 && e.getBoundingClientRect().height>0}));
    return {unsupported:[...document.querySelectorAll('[data-skeleton-error]')].map(e=>e.textContent),
      componentErrors:[...document.querySelectorAll('.skeleton-component-surface-error')].map(e=>e.textContent),
      width:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth,
      contrast,
      layout:[...document.querySelectorAll('.skeleton-hstack')].slice(0,5).map(e=>({style:e.getAttribute('style'),axis:e.dataset.axis,variant:e.dataset.layoutVariant,width:e.getBoundingClientRect().width})),
      height:document.documentElement.scrollHeight,controls,text:document.getElementById('porthole-skeleton-root').innerText};
  });
}
async function recordAllControls(page) {
  // Record actual renderer payloads. No backend is present; UI state is not a successful effect.
  const buttons=page.locator('button:visible');
  for(let i=0;i<await buttons.count();i++) { await buttons.nth(i).click(); }
  const inputs=page.locator('input:visible');
  for(let i=0;i<await inputs.count();i++){await inputs.nth(i).fill('GUI-prøve '+i);await inputs.nth(i).press('Enter');}
  const areas=page.locator('textarea:visible');
  for(let i=0;i<await areas.count();i++){await areas.nth(i).fill('Eget utkast '+i);await areas.nth(i).press('Control+Enter');}
  const pickers=page.locator('select:visible');
  for(let i=0;i<await pickers.count();i++) {
    const values=await pickers.nth(i).locator('option').evaluateAll(opts=>opts.map(o=>o.value));
    for(const val of values) await pickers.nth(i).selectOption(val);
  }
  return page.evaluate(()=>window.__actions);
}
(async()=>{
  const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{})});
  const report={kind:'P1-GUI candidate, not product acceptance',rendererCommit:'7678b2c3d293978b5b179cdcada5e843f17c5b73',
    knownIntegrationGaps:['Latest TextArea/input value is not automatically sent by adjacent Send/Save/Search buttons in this renderer-only harness. Host adapter and cell contracts remain implementation work.'],cases:[]};
  const shots=read('shots.json').filter(s=>!process.env.SHOT || s.name.includes(process.env.SHOT));
  try {
    for(const shot of shots){
      const {page,errors}=await makePage(browser,shot);
      const dom=await inspect(page);
      await page.screenshot({path:path.join(IMG,shot.name+'.png'),fullPage:true});
      const actions=await recordAllControls(page);
      const entry={...shot,errors,dom,actions};
      report.cases.push(entry);
      console.log(shot.name,JSON.stringify({height:dom.height,overflow:dom.scrollWidth-dom.width,errors:errors.length,actions:actions.length}));
      assert.equal(dom.unsupported.length,0,shot.name+' unsupported');
      assert.equal(dom.componentErrors.length,0,shot.name+' component errors');
      assert.equal(errors.length,0,shot.name+' JS errors');
      assert.equal(dom.scrollWidth,dom.width,shot.name+' horizontal overflow');
      assert.ok(dom.contrast.every(x=>x.ratio>=4.5),shot.name+' text contrast');
      if(shot.name.startsWith('two-mounts')){
        const draftActions=actions.filter(a=>a.keypath==='helper.setDraftMessage');
        assert.ok(draftActions.some(a=>a.meta.mount.instanceID==='mount-A'&&a.payload==='Eget utkast 0'));
        assert.ok(draftActions.some(a=>a.meta.mount.instanceID==='mount-B'&&a.payload==='Eget utkast 1'));
        const sends=actions.filter(a=>a.keypath==='helper.send');
        assert.deepEqual(sends.map(a=>a.payload.sessionID),['demo-session-01','demo-session-02']);
        entry.mountPayloadIsolation=true;
        await page.locator('textarea').nth(0).fill('NYTT UTKAST SOM MÅ SENDES');
        const before=await page.evaluate(()=>window.__actions.length);
        await page.locator('[data-instance-id="mount-A"]').getByRole('button',{name:'Send',exact:true}).click();
        entry.draftSendGap=await page.evaluate(before=>window.__actions.slice(before).map(a=>({keypath:a.keypath,payload:a.payload,mount:a.meta.mount})),before);
        assert.equal(entry.draftSendGap.length,1);
        assert.equal(entry.draftSendGap[0].keypath,'helper.send');
        assert.ok(!JSON.stringify(entry.draftSendGap[0].payload).includes('NYTT UTKAST SOM MÅ SENDES'));
        // This assertion records an existing integration gap, not successful message delivery.
        entry.projectionUpdate=await page.evaluate(()=>{
          const drafts=()=>[...document.querySelectorAll('textarea')].map(e=>e.value);
          const before=drafts();
          const beforePerspectives=[...document.querySelectorAll('select[aria-label="Perspektiv"]')].map(e=>e.selectedOptions[0].text);
          window.__fixture.chat.item.selectedPerspective='purpose';
          window.__renderer.update(window.__fixture);
          const independent=[...document.querySelectorAll('select[aria-label="Perspektiv"]')].map(e=>e.selectedOptions[0].text);
          window.__fixture.chatB.item.sessionID=window.__fixture.chat.item.sessionID;
          window.__fixture.chat.item.selectedPerspective='agreement';
          window.__fixture.chatB.item.selectedPerspective='agreement';
          window.__renderer.update(window.__fixture);
          return {before,beforePerspectives,after:drafts(),independent,shared:[...document.querySelectorAll('select[aria-label="Perspektiv"]')].map(e=>e.selectedOptions[0].text),
                  kind:'fixture projection injection only; not actual Flow/session storage'};
        });
        assert.deepEqual(entry.projectionUpdate.before,entry.projectionUpdate.after);
        assert.deepEqual(entry.projectionUpdate.independent,['Formålstrær',entry.projectionUpdate.beforePerspectives[1]]);
        assert.deepEqual(entry.projectionUpdate.shared,['Agreement og tilgang','Agreement og tilgang']);
      }
      if(shot.name.startsWith('packages-filled')){
        await page.locator('textarea').fill('NY INSTRUKSJON SOM MÅ LAGRES');
        const before=await page.evaluate(()=>window.__actions.length);
        await page.getByRole('button',{name:'Lagre ny versjon',exact:true}).click();
        entry.draftSaveGap=await page.evaluate(before=>window.__actions.slice(before).map(a=>({keypath:a.keypath,payload:a.payload})),before);
        assert.equal(entry.draftSaveGap.length,1);
        assert.ok(!JSON.stringify(entry.draftSaveGap[0].payload).includes('NY INSTRUKSJON SOM MÅ LAGRES'));
      }
      await page.close();
    }
  } finally {
    fs.writeFileSync(path.join(IMG,'render-report.json'),JSON.stringify(report,null,2)+'\n');
    await browser.close();
  }
})().catch(e=>{console.error(e);process.exitCode=1});
