// Rendrer G1-GUI-bildene med den ekte web-rendereren (CellScaffold Public/js/skeleton-runtime.js).
// Bruk: node render.js <cellscaffold-mappe> <utmappe>
const path = require('node:path');
const fs = require('node:fs');
const { chromium } = require('playwright');
const [cellscaffold, out] = process.argv.slice(2);
const publicDir = path.join(cellscaffold, 'Public');
const here = __dirname;
const studio = JSON.parse(fs.readFileSync(path.join(here, '..', '..', 'skeleton', 'studio-hjelp-v2.skeleton.json'), 'utf8'));
const todoDraft = JSON.parse(fs.readFileSync(path.join(here, '..', '..', 'skeleton', 'utkast-gjoremal.cellconfiguration.json'), 'utf8'));
const states = require('./states_v2.js');
const helper = JSON.parse(fs.readFileSync(path.join(here, '..', '..', 'skeleton', 'hjelper-v2.skeleton.json'), 'utf8'));

function withPreview(skeleton, preview) {
  // Forhåndsvisningen tegnes inn der Studio i dag viser utkastet; Reference-plassholderen byttes ut.
  return JSON.parse(JSON.stringify(skeleton), (k, v) => (v && v.Reference && v.Reference.keypath === 'preview') ? (preview || { Text: { text: '' } }) : v);
}

async function shot(browser, width, name, skeleton, state) {
  const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: 2 });
  await page.route('https://studio.test/**', route => {
    const p = new URL(route.request().url()).pathname;
    if (p === '/theme.css') return route.fulfill({ path: path.join(here, '..', '..', 'theme', 'Cell Configuration Studio.css'), contentType: 'text/css' });
    if (p === '/') return route.fulfill({ contentType: 'text/html; charset=utf-8', body: '<!doctype html><html lang="nb"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/css/porthole-webo.css"><link rel="stylesheet" href="/theme.css"></head><body><main class="canvas product-view view-mode" style="min-height:100vh"><div id="root" class="skeleton-host"></div></main><script src="/js/skeleton-runtime.js"></script></body></html>' });
    return route.fulfill({ path: path.join(publicDir, p), contentType: p.endsWith('.css') ? 'text/css' : 'application/javascript; charset=utf-8' });
  });
  await page.goto('https://studio.test/');
  await page.evaluate(({ skeleton, state, width }) => {
    const root = document.getElementById('root');
    HavenSkeletonRuntime.createRenderer({ rootElement: root, skeleton, layoutContext: { availableWidth: root.clientWidth || width, availableHeight: 900 }, onAction: async () => ({}) }).update(state);
  }, { skeleton, state, width });
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(out, name), fullPage: true });
  await page.close();
}

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  for (const s of states.all) {
    const skeleton = s.skeleton === 'helper' ? helper : withPreview(studio, s.preview ? todoDraft.skeleton : null);
    for (const [suffix, width] of [['', 1280], ['-iphone', 390]]) {
      await shot(browser, width, `${s.name}${suffix}.png`, skeleton, s.state);
    }
  }
  await browser.close();
})();
