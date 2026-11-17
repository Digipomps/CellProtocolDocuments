// Rendrer referansebildene i denne mappen fra mockupen (ekte piksler, Chromium).
// Kjør fra denne mappen:  node render.js
// Krever `playwright` (npm i playwright) og en Chromium; sett CHROMIUM=/sti/til/chromium ved behov.
// Mockup: HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html (Kjetils mockup + tilstandene tom/feil).
const path = require('path');
const { chromium } = require('playwright');

const MOCKUP = process.env.MOCKUP
  || path.resolve(__dirname, '../../../../HAVEN-Deploy/_handoff/DESIGN/butlerchatmockup-tilstander.html');
const url = q => 'file://' + MOCKUP + (q ? '?' + q : '');
const WEB = { width: 2000, height: 1250 };
const APP = { width: 780, height: 1688 };

const shots = [
  ['web-fylt-v1',   url(''),                        WEB],
  ['web-dra-v1',    url('state=drag'),              WEB],
  ['web-full-v1',   url('state=full'),              WEB],
  ['web-tom-v1',    url('state=tom'),               WEB],
  ['web-feil-v1',   url('state=feil'),              WEB],
  ['app-normal-v1', url('viewport=app'),            APP],
  ['app-dra-v1',    url('viewport=app&state=drag'), APP],
  ['app-tom-v1',    url('viewport=app&state=tom'),  APP],
];

(async () => {
  const opts = process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {};
  const b = await chromium.launch(opts);
  for (const [name, u, viewport] of shots) {
    const p = await b.newPage({ viewport, deviceScaleFactor: 1 });
    await p.goto(u);
    await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(__dirname, `${name}.png`) });
    await p.close();
    console.log('ok', name);
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
