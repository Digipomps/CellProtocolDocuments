// Renders dokument-med-skrivehjelp.v1.json with CellScaffold's real web runtime.
// Usage: NODE_PATH=<playwright>/node_modules node render-v2.js <CellScaffold/Public> <outdir>
const path = require('node:path');
const { chromium } = require('playwright');
const [publicDir, out] = process.argv.slice(2);
const cfg = require('./dokument-med-skrivehjelp.v1.json');
const states = require('./tilstander.v1.json');
const ops = states._document;
(async () => {
  for (const [w, h, suffix] of [[1280, 900, 'laptop'], [390, 844, 'iphone']]) {
    for (const name of ['forslag', 'av', 'feil']) {
      const browser = await chromium.launch();
      const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
      const actions = [];
      await page.exposeFunction('record', a => actions.push(a));
      await page.route('https://document.test/**', route => {
        const p = new URL(route.request().url()).pathname;
        if (p === '/') return route.fulfill({ contentType: 'text/html; charset=utf-8', body: '<!doctype html><html lang="nb"><head><link rel="stylesheet" href="/css/porthole-webo.css"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><main id="root" class="canvas view-mode" style="padding:24px"></main><script src="/vendor/quill/quill.js"></script><script src="/js/skeleton-runtime.js"></script></body></html>' });
        return route.fulfill({ path: path.join(publicDir, p), contentType: p.endsWith('.css') ? 'text/css' : 'application/javascript; charset=utf-8' });
      });
      await page.goto('https://document.test/');
      await page.evaluate(({ skeleton, ops, panel }) => {
        const current = { schema: 'haven.document.v1', documentId: 'mock', revision: 13, sequence: 40, ops, events: [], comments: [], presence: [],
          messages: [{ id: 'm1', author: 'Petter', text: 'Metodeavsnittet trenger mer om måling.' }], help: [], onboarding: '' };
        window.renderer = HavenSkeletonRuntime.createRenderer({ rootElement: document.getElementById('root'), skeleton,
          onAction: async (key, payload) => { window.record({ key, payload }); return { status: 'accepted' }; } });
        window.renderer.update({ document: { current, assistPanel: panel } });
      }, { skeleton: cfg.skeleton, ops, panel: states[name] });
      await page.waitForSelector('.ql-editor'); await page.waitForTimeout(700);
      await page.screenshot({ path: path.join(out, `skrivehjelp-${name}-${suffix}-v2.png`), fullPage: true });
      // Behaviour probe: every button in the panel reaches a keypath.
      if (suffix === 'laptop') {
        const labels = await page.$$eval('button', bs => bs.map(b => b.textContent.trim()).filter(Boolean));
        for (const label of ['Be om forslag', 'Bruk forslaget', 'Forkast', 'Be om nytt forslag', 'Slå på modellhjelp for dokumentet', 'Velg modell']) {
          const b = page.getByRole('button', { name: label, exact: true });
          if (await b.count()) { await b.first().click(); }
        }
        await page.waitForTimeout(300);
        console.log(JSON.stringify({ state: name, buttons: labels, actions }));
      }
      await browser.close();
    }
  }
})();
