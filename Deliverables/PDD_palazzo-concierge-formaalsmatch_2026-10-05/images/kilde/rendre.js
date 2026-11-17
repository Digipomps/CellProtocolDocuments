// Rendrer rammene og setter dem sammen til de ni bildene (og ett tillegg).
// Grunnlaget er sidens egen HTML, CSS og JavaScript (kopiert fra PalazzoScaffold/Public, commit c5058f49 på nett).
// Sidens eget skript tegner svaret av en konvolutt; det nye legges på etterpå av skissen (skisse.css og funksjonen under).
// Bruk: NODE_PATH=/home/claude/.npm-global/lib/node_modules node rendre.js [ramme ...]
"use strict";
const http = require("http");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { RAMMER, BILDER } = require("./tilstander.js");

const SIDE = "/home/claude/natt/pdd3/side";
const HER = __dirname;
const RAMMEMAPPE = path.join(HER, "rammer");
const UTMAPPE = path.join(HER, "ut");
const SKALA = 1.5;
const TYPER = { ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "application/javascript; charset=utf-8", ".png": "image/png", ".woff2": "font/woff2" };

function tjener() {
  return http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split("?")[0]);
    let fil;
    if (p === "/palazzo" || p === "/palazzo/") fil = path.join(SIDE, "palazzo/index.html");
    else if (p === "/skisse.css") fil = path.join(HER, "skisse.css");
    else if (p.startsWith("/rammer/")) fil = path.join(HER, p);
    else fil = path.join(SIDE, p);
    if (!fil.startsWith(SIDE) && !fil.startsWith(HER)) { res.writeHead(403); res.end(); return; }
    fs.readFile(fil, (err, data) => {
      if (err) { res.writeHead(404); res.end("ikke funnet"); return; }
      res.writeHead(200, { "Content-Type": TYPER[path.extname(fil)] || "application/octet-stream" });
      res.end(data);
    });
  });
}

// Kjøres i siden. Legger på det nye. Rører ikke sidens egne regler.
function leggPaaSkisse(s) {
  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; };
  const link = document.createElement("link"); link.rel = "stylesheet"; link.href = "/skisse.css"; document.head.append(link);
  const panel = document.getElementById("answer-panel");
  const answer = document.getElementById("answer-text");
  const warning = document.getElementById("answer-warning");
  const sources = document.getElementById("source-section");
  const card = document.querySelector(".conversation-card");
  const ctx = document.getElementById("question-context");
  panel.dataset.kind = s.kind || "";
  if (s.kind === "receipt" || s.kind === "ask-model") panel.dataset.verified = "true";
  if (s.eyebrow) document.getElementById("answer-eyebrow").textContent = s.eyebrow;
  if (s.title) document.getElementById("answer-title").textContent = s.title;
  if (s.badge !== undefined) document.getElementById("answer-confidence").textContent = s.badge;
  // Forslaget: et svar som tilbyr eller nevner retter, har ingen merkelapp om sikkerhet.
  // `viserSidensMerkelapp` gjør ingenting her; rammen viser da merkelappen sidens eget skript satte.
  if (s.hideBadge) document.getElementById("answer-confidence").style.display = "none";
  if (s.questionLabel) document.getElementById("question-context-label").textContent = s.questionLabel;
  if (s.question) document.getElementById("submitted-question").textContent = s.question;
  if (s.intro) document.querySelector(".concierge-intro > p:not(.eyebrow)").textContent = s.intro;
  if (s.understood) {
    const u = el("p", "understood-line"); u.append("Slik forsto jeg deg: "); u.append(el("strong", "", s.understood)); answer.before(u);
  }
  if (s.modelMark) { answer.before(el("span", "model-mark", s.modelMark)); }
  let etter = answer;
  if (s.modelNote) { const n = el("p", "model-note", s.modelNote); etter.after(n); etter = n; }
  if (s.actions) {
    const row = el("div", "answer-actions");
    s.actions.forEach((a) => { const b = el("button", a.primary ? "primary" : "secondary", a.label); b.type = "button"; row.append(b); });
    etter.after(row); etter = row;
    if (s.note) { const n = el("p", "answer-note", s.note); etter.after(n); etter = n; }
  }
  if (s.hideWarning) warning.hidden = true;
  if (s.hideSources) sources.hidden = true;
  if (s.kind === "strip-only") { ctx.hidden = true; panel.hidden = true; }
  if (s.noted && s.noted.length) {
    const strip = el("div", "noted-strip"); strip.id = "noted-strip";
    strip.append(el("p", "eyebrow", "Notert i denne samtalen"));
    const chips = el("div", "noted-chips");
    s.noted.forEach((n) => {
      const c = el("span", "noted-chip" + (n.cls ? " " + n.cls : ""), n.text);
      const x = el("button", "", "✕"); x.type = "button"; x.setAttribute("aria-label", "Fjern «" + n.text + "»"); c.append(x); chips.append(c);
    });
    const clear = el("button", "noted-clear", "Fjern alt"); clear.type = "button"; chips.append(clear);
    strip.append(chips);
    if (s.keepLink) { const rad = el("p", "noted-keep"); const k = el("button", "noted-clear", s.keepLink); k.type = "button"; k.style.marginLeft = "0"; rad.append(k); strip.append(rad); }
    if (s.notedHelp) strip.append(el("p", "noted-help", s.notedHelp));
    card.append(strip);
  }
  if (s.keep) {
    const k = el("div", "keep-panel"); k.id = "keep-panel";
    k.append(el("h4", "", s.keep.title)); k.append(el("p", "", s.keep.text));
    s.keep.items.forEach((it) => {
      const l = el("label"); const cb = el("input"); cb.type = "checkbox"; cb.checked = !!it.checked; l.append(cb);
      const t = el("span", "", it.text); if (it.small) t.append(el("small", "", it.small)); l.append(t); k.append(l);
    });
    const row = el("div", "answer-actions"); row.style.marginTop = "0.9rem";
    s.keep.actions.forEach((a) => { const b = el("button", a.primary ? "primary" : "secondary", a.label); b.type = "button"; row.append(b); });
    k.append(row); card.append(k);
  }
}

// Kjøres i siden: samler spørsmålet, svaret og det notert i et utsnitt uten skrivefeltet.
function lagUtsnitt(bredde) {
  const wrap = document.createElement("div");
  wrap.id = "skisse-utsnitt";
  wrap.style.cssText = "align-self:start;width:" + bredde + "px;padding:1.4rem 1.5rem 1.5rem;border:1px solid var(--line);border-radius:1.25rem;background:var(--paper);";
  document.body.style.background = "#fff";
  document.querySelector(".concierge-layout").style.cssText = "display:block;max-width:none;margin:0;padding:8px;background:#fff;";
  document.querySelector(".concierge-intro").hidden = true;
  const card = document.querySelector(".conversation-card");
  ["question-context", "answer-panel", "noted-strip", "keep-panel"].forEach((id) => {
    const e = document.getElementById(id); if (e && !e.hidden) wrap.append(e);
  });
  if (wrap.firstElementChild) {
    wrap.firstElementChild.style.marginTop = "0";
    if (wrap.firstElementChild.id === "noted-strip") { wrap.firstElementChild.style.borderTop = "0"; wrap.firstElementChild.style.paddingTop = "0"; }
  }
  card.replaceWith(wrap);
}

async function rendreRamme(browser, port, navn) {
  const r = RAMMER[navn];
  if (!r) throw new Error("ukjent ramme: " + navn);
  const ctx = await browser.newContext({ viewport: { width: r.bredde, height: 1100 }, deviceScaleFactor: SKALA, locale: "nb-NO", reducedMotion: "reduce" });
  const page = await ctx.newPage();
  let neste = null;
  await page.route("**/palazzo/api/state", (route) => route.fulfill({ contentType: "application/json", body: JSON.stringify({ serviceStatus: "available", serviceMessage: "Concierge bruker et datert kunnskapsgrunnlag. Dagens opplysninger må bekreftes av Palazzo." }) }));
  await page.route("**/palazzo/api/ask", (route) => route.fulfill({ contentType: "application/json", body: JSON.stringify(neste) }));
  await page.goto("http://127.0.0.1:" + port + "/palazzo", { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  let sistSagt = "";
  for (const steg of r.steg) {
    neste = steg.svar;
    if (steg.si) sistSagt = steg.si;
    await page.fill("#question", sistSagt);
    await page.press("#question", "Enter");
    await page.waitForFunction((t) => {
      const p = document.getElementById("answer-panel");
      return p && !p.hidden && document.getElementById("answer-text").textContent === t;
    }, steg.svar.answer);
  }
  await page.evaluate(leggPaaSkisse, r.skisse);
  await page.evaluate(() => { if (document.activeElement) document.activeElement.blur(); });
  await page.waitForLoadState("networkidle");
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(150);
  const fil = path.join(RAMMEMAPPE, navn + ".png");
  let maal;
  if (r.modus === "layout") maal = page.locator(".concierge-layout");
  else if (r.modus === "card") maal = page.locator(".conversation-card");
  else { await page.evaluate(lagUtsnitt, 560); maal = page.locator("#skisse-utsnitt"); }
  const boks = await maal.boundingBox();
  await maal.screenshot({ path: fil });
  await ctx.close();
  return { navn, bredde: Math.round(boks.width), hoyde: Math.round(boks.height) };
}

function settSammenHtml(bilde, maal) {
  const esc = (t) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const figur = (c) => {
    const m = maal[c.ramme];
    return "<figure style='width:" + m.bredde + "px'><img src='/rammer/" + c.ramme + ".png' width='" + m.bredde + "' height='" + m.hoyde + "' alt=''><figcaption>" + esc(c.tekst) + "</figcaption></figure>";
  };
  const rader = bilde.kolonner
    ? "<div class='rad'>" + bilde.kolonner.map((kol) => "<div class='kol'>" + kol.map(figur).join("") + "</div>").join("") + "</div>"
    : bilde.rader.map((rad) => "<div class='rad'>" + rad.map(figur).join("") + "</div>").join("");
  return "<!doctype html><html lang='no'><head><meta charset='utf-8'><link rel='stylesheet' href='/css/palazzo-communale.css'><style>" +
    "body{margin:0;padding:28px 32px 30px;background:#fff;color:var(--ink);font-family:var(--sans);width:max-content;min-width:900px}" +
    "h1{margin:0 0 6px;font-family:var(--display);font-size:30px;font-weight:500;color:var(--forest);max-width:1200px;line-height:1.15}" +
    ".ingress{margin:0 0 4px;max-width:1150px;font-size:16px;line-height:1.45;color:var(--ink)}" +
    ".merke{margin:0 0 20px;font-size:12.5px;color:var(--muted);letter-spacing:.02em}" +
    ".rad{display:flex;gap:26px;align-items:flex-start;margin-bottom:24px}.kol{display:flex;flex-direction:column;gap:22px}" +
    "figure{margin:0}figure img{display:block;border:1px solid rgba(85,107,63,.25);border-radius:6px}" +
    "figcaption{margin-top:8px;font-size:14px;line-height:1.4;color:var(--ink)}" +
    "</style></head><body><h1>" + esc(bilde.tittel) + "</h1><p class='ingress'>" + esc(bilde.ingress) + "</p>" +
    "<p class='merke'>Forslag til G1-GUI · " + esc(bilde.fil) + ".png · rendret 7. oktober 2026 fra sidens egen HTML og CSS (PalazzoScaffold, commit c5058f49, den som står på nett). Det nye er skissert; ingen programkode har laget svarene.</p>" +
    rader + "</body></html>";
}

(async () => {
  fs.mkdirSync(RAMMEMAPPE, { recursive: true }); fs.mkdirSync(UTMAPPE, { recursive: true });
  const srv = tjener(); await new Promise((ok) => srv.listen(0, "127.0.0.1", ok));
  const port = srv.address().port;
  const browser = await chromium.launch();
  const bare = process.argv.slice(2);
  const maal = {};
  const maalfil = path.join(RAMMEMAPPE, "maal.json");
  if (fs.existsSync(maalfil)) Object.assign(maal, JSON.parse(fs.readFileSync(maalfil, "utf8")));
  for (const navn of Object.keys(RAMMER)) {
    if (bare.length && !bare.includes(navn)) continue;
    const m = await rendreRamme(browser, port, navn);
    maal[navn] = { bredde: m.bredde, hoyde: m.hoyde };
    console.log("ramme", navn, m.bredde + "x" + m.hoyde);
  }
  fs.writeFileSync(maalfil, JSON.stringify(maal, null, 1));
  for (const bilde of BILDER) {
    if (bare.length && !(bilde.kolonner || bilde.rader).flat().some((c) => bare.includes(c.ramme))) continue;
    const ctx = await browser.newContext({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: SKALA });
    const page = await ctx.newPage();
    await page.route("**/__sett-sammen", (route) => route.fulfill({ contentType: "text/html; charset=utf-8", body: settSammenHtml(bilde, maal) }));
    await page.goto("http://127.0.0.1:" + port + "/__sett-sammen", { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);
    const body = page.locator("body");
    await body.screenshot({ path: path.join(UTMAPPE, bilde.fil + ".png") });
    const b = await body.boundingBox();
    console.log("bilde", bilde.fil, Math.round(b.width) + "x" + Math.round(b.height));
    await ctx.close();
  }
  await browser.close(); srv.close();
})().catch((e) => { console.error("FEIL:", e); process.exit(1); });
