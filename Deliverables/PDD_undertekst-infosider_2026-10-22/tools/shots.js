// Skjermbilder av de tre stedene underteksten står, for G1-GUI (lokalt) og G3 (produksjon).
// Bruk: NODE_PATH=$(npm root -g) node shots.js <base-url> <utmappe> <prefiks> [bare-ett-navn]
//   base-url  f.eks. http://127.0.0.1:4173 (lokal `python3 -m http.server` i Website/) eller https://digipomps.org
//   prefiks   f.eks. for / etter / prod
// Går via HTTPS_PROXY når den er satt (skyøkt); da godtas proxyens sertifikat for selve skjermbildet.
const { chromium } = require('playwright');
(async () => {
  const [base, outDir, tag, only] = process.argv.slice(2);
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy || '';
  const launchOpts = proxy ? { proxy: { server: proxy } } : {};
  let browser;
  try { browser = await chromium.launch(launchOpts); }
  catch (e) { browser = await chromium.launch({ ...launchOpts, executablePath: '/opt/pw-browsers/chromium' }); }
  const shots = [
    { path: '/', sel: '#mennesket-og-fellesskapet', name: 'forside-seksjon', width: 1280 },
    { path: '/', sel: '#mennesket-og-fellesskapet', name: 'forside-seksjon-mobil', width: 390, clip: true },
    { path: '/artikler/', sel: '#mennesket-forst', name: 'artikkeloversikt-kort', width: 1280 },
    { path: '/artikler/mennesket-forst/', sel: 'article#mennesket-forst', name: 'artikkel', width: 1280 },
  ];
  for (const s of shots) {
    if (only && s.name !== only) continue;
    const ctx = await browser.newContext({ viewport: { width: s.width, height: 900 }, deviceScaleFactor: 1, ignoreHTTPSErrors: !!proxy });
    const page = await ctx.newPage();
    await page.goto(base + s.path, { waitUntil: 'networkidle' });
    await page.evaluate(() => { if (document.activeElement) document.activeElement.blur(); });
    const el = page.locator(s.sel).first();
    if (s.clip) {
      // Helsideskjermbilde klippet til elementets boks i sidekoordinater: den klebrige toppmenyen og
      // hopp-til-innhold-lenken blir liggende øverst i dokumentet i stedet for over seksjonen.
      const box = await el.evaluate(e => { const r = e.getBoundingClientRect(); return { x: r.left + window.scrollX, y: r.top + window.scrollY, width: r.width, height: r.height }; });
      await page.screenshot({ path: `${outDir}/${tag}-${s.name}.png`, fullPage: true, clip: box });
    } else {
      await el.scrollIntoViewIfNeeded();
      await el.screenshot({ path: `${outDir}/${tag}-${s.name}.png` });
    }
    await ctx.close();
    console.log('ok', `${tag}-${s.name}.png`);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
