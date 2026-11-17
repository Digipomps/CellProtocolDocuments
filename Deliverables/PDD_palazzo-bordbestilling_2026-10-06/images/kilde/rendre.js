const { chromium } = require("playwright");
const path = require("path");
(async () => {
  const browser = await chromium.launch();
  for (const [inn, ut] of [["hvor.html", "tillegg-hvor-ligger-hva-v1.png"], ["bordbok.html", "husflate-bordbok-dagen-v1.png"], ["gjest.html", "gjesteflate-bestill-bord-v1.png"]]) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 2 });
    await page.goto("file://" + path.join(__dirname, inn));
    await page.evaluate(() => document.fonts.ready);
    const el = await page.$(".ark");
    await el.screenshot({ path: path.join(__dirname, "ut", ut) });
    const box = await el.boundingBox();
    console.log(ut, Math.round(box.width) + "x" + Math.round(box.height));
    await page.close();
  }
  await browser.close();
})();
