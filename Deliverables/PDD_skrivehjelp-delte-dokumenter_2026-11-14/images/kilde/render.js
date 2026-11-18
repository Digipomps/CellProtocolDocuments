const path = require('node:path');
const { chromium } = require('playwright');
const publicDir = '/home/user/cellscaffold/Public';
const out = process.argv[2];
const docOps = [
  { insert: 'Unik representasjon av personer i HAVEN' }, { insert: '\n', attributes: { header: 1 } },
  { insert: 'Problemstilling' }, { insert: '\n', attributes: { header: 2 } },
  { insert: 'Når én person har flere identiteter i ulike domener, må systemet kunne vise at det er samme person uten å avsløre mer enn nødvendig. Vi undersøker hvordan EntityAnchor og domeneavgrensede identiteter kan gi en slik unik representasjon, og hva som skjer når en identitet trekkes tilbake eller kompromitteres, og hvilke garantier som da fortsatt holder for de andre domenene som personen deltar i.\n' },
  { insert: 'Metode' }, { insert: '\n', attributes: { header: 2 } },
  { insert: 'Vi bygger en prototyp med to scaffolds og måler hvor mye informasjon som lekker mellom domener.\n' },
];
const help = [];
async function shot(width, height, name, mutate) {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 2 });
  await page.route('https://document.test/**', route => {
    const p = new URL(route.request().url()).pathname;
    if (p === '/') return route.fulfill({ contentType: 'text/html; charset=utf-8', body: '<!doctype html><html lang="nb"><head><link rel="stylesheet" href="/css/porthole-webo.css"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><main id="root" class="canvas view-mode" style="padding:24px"></main><script src="/vendor/quill/quill.js"></script><script src="/js/skeleton-runtime.js"></script></body></html>' });
    return route.fulfill({ path: path.join(publicDir, p), contentType: p.endsWith('.css') ? 'text/css' : 'application/javascript; charset=utf-8' });
  });
  await page.goto('https://document.test/');
  await page.evaluate(({ ops }) => {
    const current = { schema: 'haven.document.v1', documentId: 'mock', revision: 13, sequence: 40, ops, events: [], comments: [],
      presence: [], messages: [{ id: 'm1', author: 'Petter', text: 'Metodeavsnittet trenger mer om måling.' }], help: [],
      onboarding: 'Jeg hjelper dere å komme i gang med dokumentet.' };
    window.renderer = HavenSkeletonRuntime.createRenderer({ rootElement: document.getElementById('root'), skeleton: { VStack: { elements: [
      { Visualization: { kind: 'richDocument', keypath: 'document.current', actionKeypath: 'document.change' } },
      { Visualization: { kind: 'documentHelp', keypath: 'document.current', actionKeypath: 'document.change' } },
      { Visualization: { kind: 'documentChat', keypath: 'document.current', actionKeypath: 'document.change' } },
    ] } }, onAction: async () => ({ status: 'accepted' }) });
    window.renderer.update({ document: { current } });
  }, { ops: docOps });
  await page.waitForSelector('.ql-editor');
  await page.waitForTimeout(600);
  if (mutate) await page.evaluate(mutate);
  await page.waitForTimeout(200);
  await page.screenshot({ path: path.join(out, name), fullPage: true });
  await browser.close();
}
module.exports = { shot };
if (require.main === module) (async () => {
  await shot(1280, 900, 'dokument-i-dag-laptop.png');
})();
