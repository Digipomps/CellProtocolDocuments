// Rendrer kandidat-skjelettet gjennom CellScaffolds egen web-renderer
// (web-src/ eksportert fra origin/main 7678b2c3, md5 i README.md) i Chromium.
// Kjør: NODE_PATH=<playwright> node render.js   (etter python3 gen_skeleton.py)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const SRC = path.join(__dirname, "..", "web-src");
const SK = path.join(__dirname, "..", "skeleton");
const WEB = { width: 1180, height: 820 };
const APP = { width: 390, height: 844 };

const harness = `<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Venter på deg</title>
<link rel="stylesheet" href="/css/porthole-webo.css">
<style>body{margin:0;background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif}</style>
</head><body><main class="canvas product-view view-mode"><div id="root" class="skeleton-host"></div></main>
<script src="/js/haven-localization.js"></script><script src="/js/skeleton-runtime.js"></script></body></html>`;

async function route(page) {
  await page.route("**/*", async (r) => {
    const u = new URL(r.request().url());
    if (u.pathname === "/") return r.fulfill({ contentType: "text/html", body: harness });
    const map = { "/js/skeleton-runtime.js": "skeleton-runtime.js", "/js/haven-localization.js": "haven-localization.js", "/css/porthole-webo.css": "porthole-webo.css" };
    if (map[u.pathname]) return r.fulfill({ path: path.join(SRC, map[u.pathname]) });
    return r.abort();
  });
}

async function mount(page, skeleton, state, viewport) {
  await page.evaluate(({ skeleton, state, viewport }) => {
    window.__actions = [];
    const root = document.getElementById("root");
    root.innerHTML = "";
    const r = window.HavenSkeletonRuntime.createRenderer({
      rootElement: root, skeleton,
      onAction: async (keypath, payload) => { window.__actions.push({ keypath, payload }); return { status: "ok" }; },
    });
    if (r.setLayoutContext) {
      const capabilities = viewport.width < 700 ? ["touch"] : ["pointer", "hover", "keyboard", "drag"];
      r.setLayoutContext({ availableWidth: viewport.width - 32, availableHeight: viewport.height, capabilities });
    }
    r.update(state);
  }, { skeleton, state, viewport });
  await page.waitForTimeout(150);
}

const load = (f) => JSON.parse(fs.readFileSync(path.join(SK, f), "utf8"));

(async () => {
  const b = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const sk = load("venter-paa-deg.skeleton.json");
  const shots = [
    ["venter-paa-deg-web-fylt", "state-fylt.json", WEB],
    ["venter-paa-deg-web-tom", "state-tom.json", WEB],
    ["venter-paa-deg-web-foreldet", "state-foreldet.json", WEB],
    ["venter-paa-deg-app-fylt", "state-fylt.json", APP],
  ];
  const report = {};
  for (const [name, st, vp] of shots) {
    const page = await b.newPage({ viewport: vp, deviceScaleFactor: 2 });
    const errors = [];
    page.on("pageerror", (e) => errors.push(String(e)));
    page.on("console", (m) => { if (["warning", "error"].includes(m.type())) errors.push(m.type() + ": " + m.text()); });
    await route(page);
    await page.goto("http://venter.kandidat.test/");
    await page.waitForFunction(() => Boolean(window.HavenSkeletonRuntime?.createRenderer));
    await mount(page, sk, load(st), vp);
    await page.screenshot({ path: path.join(__dirname, `${name}-v2.png`), fullPage: true });
    report[name] = { errors, unsupported: await page.evaluate(() => Array.from(document.querySelectorAll("[data-skeleton-error]")).map((e) => e.textContent)) };
    console.log("ok", name, JSON.stringify(report[name]));
    await page.close();
  }
  // Oppførsel: hva sender knappene til cellen?
  const page = await b.newPage({ viewport: WEB });
  await route(page);
  await page.goto("http://venter.kandidat.test/");
  await page.waitForFunction(() => Boolean(window.HavenSkeletonRuntime?.createRenderer));
  await mount(page, sk, load("state-fylt.json"), WEB);
  for (const label of ["Merk som løst", "Bekreftet", "Køe på nytt", "Køe inn igjen", "Spør"]) {
    await page.locator("button:visible", { hasText: label }).first().click();
  }
  report.behaviour = await page.evaluate(() => window.__actions);
  report.links = await page.evaluate(() => Array.from(document.querySelectorAll("a")).map((a) => ({ text: a.textContent.trim(), href: a.href, visible: a.offsetParent !== null })));
  console.log(JSON.stringify(report.links));
  console.log(JSON.stringify(report.behaviour, null, 1));
  fs.writeFileSync(path.join(__dirname, "render-report.json"), JSON.stringify(report, null, 2));
  await b.close();
})().catch((e) => { console.error(e); process.exit(1); });
