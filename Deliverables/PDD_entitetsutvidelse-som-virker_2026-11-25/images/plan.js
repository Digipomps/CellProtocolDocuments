// Tegner planen som baner: én bane per aktør, én boks per arbeidspakke. Kjør: node plan.js
const path = require("path");
const { chromium } = require("playwright");
const COLS = ["Nå", "WP0", "WP1", "WP2", "WP3", "WP4", "WP5", "WP6", "WP7", "WP8", "WP9", "WP10", "WP11", "G3"];
const LANES = [
  ["Kjetil", { "Nå": "Si «G2 godkjent»", "WP1": "Flette #114", "WP5": "Flette leveranse 1", "WP8": "Flette leveranse 2", "WP11": "Passkey på ekte enhet", "G3": "Lese ACCEPT.md" }, "#FFE9C7"],
  ["Claude (sky, Linux)", { "WP0": "Dagens svar", "WP1": "Avtaler følger entiteten", "WP2": "Bærbart bevis", "WP3": "Fersk passkey", "WP4": "Statusliste", "WP5": "Python, Go, prøvesett", "WP6": "Kartposter", "WP7": "Hjelp og tilstander", "WP8": "Flatene", "WP9": "Rester", "WP10": "Pin og meny", "WP11": "Måling og aksept" }, "#D8E8FF"],
  ["Mac (macOS, tidsluke)", { "WP0": "grunnlinje", "WP1": "test", "WP2": "test", "WP3": "test", "WP4": "test", "WP6": "test", "WP7": "test", "WP8": "test", "WP9": "test", "WP10": "bygg", "WP11": "vert 2" }, "#DDF3E0"],
  ["HAVEN-Deploy", { "WP9": "Telle kontrakter", "WP11": "Staging" }, "#EADCF7"],
];
const groups = [["", 1], ["", 1], ["Leveranse 1: avtaler og bærbar lenke", 5], ["Leveranse 2: kartet og flatene", 3], ["Leveranse 3: rester og virkelig bruk", 3], ["", 1]];
const html = `<html><body style="margin:0;padding:24px;font-family:-apple-system,Helvetica,Arial,sans-serif;background:#fff;color:#111">
<h2 style="margin:0 0 14px">Plan: entitetsutvidelse som virker</h2>
<table style="border-collapse:separate;border-spacing:4px;font-size:12px">
<tr><td></td>${groups.map(([t, n]) => `<td colspan="${n}" style="text-align:center;font-weight:600;${t ? "background:#EEF1F5;border-radius:6px;padding:6px" : ""}">${t}</td>`).join("")}</tr>
<tr><td></td>${COLS.map((c) => `<th style="width:104px;color:#5F6B7A;font-weight:600">${c}</th>`).join("")}</tr>
${LANES.map(([name, cells, colour]) => `<tr><th style="text-align:left;padding-right:10px;white-space:nowrap;font-size:13px">${name}</th>${COLS.map((c) => cells[c] ? `<td style="background:${colour};border-radius:6px;padding:8px 6px;text-align:center;height:34px">${cells[c]}</td>` : "<td></td>").join("")}</tr>`).join("")}
</table><p style="font-size:12px;color:#5F6B7A;margin:12px 0 0">Tiden går mot høyre. Alt felles ligger i CellProtocol, PyCellProtocol og gocellprotocol. CellScaffold får bare tilkobling.</p></body></html>`;
(async () => {
  const b = await chromium.launch();
  const page = await b.newPage({ viewport: { width: 1760, height: 400 }, deviceScaleFactor: 2 });
  await page.setContent(html);
  await page.locator("body").screenshot({ path: path.join(__dirname, "plan-v1.png") });
  await b.close();
})();
