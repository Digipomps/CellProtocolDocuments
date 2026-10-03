const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || undefined, args: ['--no-sandbox'] });
  const shots = [
    ['meny-v4.html?state=godkjenn', 'meny-jobb-godkjenning-v4.png', 1260, 340],
    ['meny-v4.html?state=ro', 'meny-planlagte-jobber-ro-v3.png', 1180, 540],
    ['meny-v4.html?state=feil', 'meny-planlagte-jobber-feil-v3.png', 1180, 520],
  ];
  for (const [page, out, w, h] of shots) {
    const p = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    await p.goto('file://' + __dirname + '/' + page);
    await p.waitForTimeout(150);
    await p.screenshot({ path: out });
    await p.close();
    console.log('ok', out);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
