// Setter bildene for én flate sammen til ett oversiktsark. Kjør: node sheet.js
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const SHEETS = {
  "oversikt-min-entitet-v1": [["Alt nåbart", "min-entitet-web-alt-naabart-v1"], ["Ett sted utilgjengelig", "min-entitet-web-ett-sted-utilgjengelig-v1"], ["Én lenke trukket", "min-entitet-web-lenke-trukket-v1"], ["Tom", "min-entitet-web-tom-v1"], ["Telefon: alt nåbart", "min-entitet-app-alt-naabart-v1"], ["Telefon: én lenke trukket", "min-entitet-app-lenke-trukket-v1"]],
  "oversikt-koble-enhet-v1": [["Eier 1: velg", "koble-enhet-web-eier-start-v1"], ["Eier 2: koden", "koble-enhet-web-eier-kode-v1"], ["Eier 3: godkjenn", "koble-enhet-web-eier-godkjenn-v1"], ["Eier 4: ferdig", "koble-enhet-web-eier-ferdig-v1"], ["Ny enhet 1: skriv koden", "koble-enhet-app-ny-start-v1"], ["Ny enhet 2: venter", "koble-enhet-app-ny-venter-v1"], ["Ny enhet 3: ferdig", "koble-enhet-app-ny-ferdig-v1"], ["Avvist: koden er utløpt", "koble-enhet-app-avvist-utlopt-v1"], ["Avvist: avslått", "koble-enhet-app-avvist-avslaatt-v1"], ["Avvist: passkey", "koble-enhet-web-avvist-passkey-v1"]],
  "oversikt-hjemmescaffold-v1": [["Ikke koblet", "hjemmescaffold-web-ikke-koblet-v1"], ["Koblet", "hjemmescaffold-web-koblet-v1"], ["Passkey ikke godtatt", "hjemmescaffold-web-feil-passkey-v1"]],
};
(async () => {
  const b = await chromium.launch();
  for (const [name, items] of Object.entries(SHEETS)) {
    const cells = items.map(([label, file]) => {
      const data = fs.readFileSync(path.join(__dirname, file + ".png")).toString("base64");
      const phone = file.includes("-app-");
      return `<figure style="width:${phone ? 300 : 640}px"><figcaption>${label}<small>${file}.png</small></figcaption><img src="data:image/png;base64,${data}"></figure>`;
    }).join("");
    const page = await b.newPage({ viewport: { width: 1360, height: 800 }, deviceScaleFactor: 2 });
    await page.setContent(`<html><body style="margin:0;padding:24px;background:#E9EDF2;font-family:-apple-system,Helvetica,Arial,sans-serif"><div style="display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start">${cells}</div><style>figure{margin:0}figcaption{font-weight:600;font-size:15px;margin-bottom:6px;color:#111}small{display:block;font-weight:400;font-size:11px;color:#5F6B7A}img{width:100%;display:block;border-radius:8px;background:#fff}</style></body></html>`);
    await page.screenshot({ path: path.join(__dirname, name + ".png"), fullPage: true });
    await page.close();
    console.log("ok", name);
  }
  await b.close();
})();
