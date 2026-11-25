// Rendrer kandidat-skjelettene gjennom CellScaffolds EGEN web-renderer
// (Public/js/skeleton-runtime.js + Public/css/porthole-webo.css + Public/js/haven-localization.js
// fra origin/main, md5 i README.md) i Chromium. Ingen piksel er tegnet for hånd.
// Kjør:  python3 gen_skeleton.py && WEB_SRC=<mappe med de tre filene> node render.js
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const SRC = process.env.WEB_SRC;
if (!SRC) { console.error("WEB_SRC mangler"); process.exit(2); }
const SKEL = path.join(__dirname, "..", "skeleton");
const IMG = __dirname;

const WEB = { width: 1180, height: 820 };
const APP = { width: 390, height: 844 };

function harnessHTML() {
  return [
    "<!doctype html><html lang=\"nb\"><head><meta charset=\"utf-8\">",
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
    "<title>Entitetsutvidelse — kandidat</title>",
    "<link rel=\"stylesheet\" href=\"/css/porthole-webo.css\">",
    "<style>body{margin:0;background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;}",
    ".canvas{padding:0}</style>",
    "</head><body><main class=\"canvas view-mode\"><div id=\"root\" class=\"skeleton-host\"></div></main>",
    "<script src=\"/js/haven-localization.js\"></script>",
    "<script src=\"/js/skeleton-runtime.js\"></script></body></html>",
  ].join("");
}

async function route(page) {
  await page.route("**/*", async (r) => {
    const u = new URL(r.request().url());
    if (u.pathname === "/") return r.fulfill({ contentType: "text/html", body: harnessHTML() });
    if (u.pathname === "/js/skeleton-runtime.js") return r.fulfill({ path: path.join(SRC, "skeleton-runtime.js"), contentType: "application/javascript" });
    if (u.pathname === "/js/haven-localization.js") return r.fulfill({ path: path.join(SRC, "haven-localization.js"), contentType: "application/javascript" });
    if (u.pathname === "/css/porthole-webo.css") return r.fulfill({ path: path.join(SRC, "porthole-webo.css"), contentType: "text/css" });
    return r.abort();
  });
}

async function mount(page, skeleton, state, viewport) {
  await page.evaluate(({ skeleton, state, viewport }) => {
    window.__actions = [];
    const root = document.getElementById("root");
    root.innerHTML = "";
    window.__renderer = window.HavenSkeletonRuntime.createRenderer({
      rootElement: root,
      skeleton,
      onAction: async (keypath, payload, meta) => { window.__actions.push({ keypath, payload }); return { status: "ok" }; },
    });
    if (window.__renderer.setLayoutContext) {
      // Web (Porthole) erklærer drag; appen (Binding) erklærer touch.
      const capabilities = viewport.width < 700 ? ["touch"] : ["pointer", "hover", "keyboard", "drag"];
      window.__renderer.setLayoutContext({ availableWidth: viewport.width - 32, availableHeight: viewport.height, capabilities });
    }
    window.__renderer.update(state);
  }, { skeleton, state, viewport });
  await page.waitForTimeout(120);
}

const load = (f) => JSON.parse(fs.readFileSync(path.join(SKEL, f), "utf8"));

const SHOTS = [
  ["min-entitet", "alt-naabart", [WEB, APP]],
  ["min-entitet", "ett-sted-utilgjengelig", [WEB]],
  ["min-entitet", "lenke-trukket", [WEB, APP]],
  ["min-entitet", "tom", [WEB]],
  ["koble-enhet", "eier-start", [WEB]],
  ["koble-enhet", "eier-kode", [WEB]],
  ["koble-enhet", "eier-godkjenn", [WEB]],
  ["koble-enhet", "eier-ferdig", [WEB]],
  ["koble-enhet", "ny-start", [APP]],
  ["koble-enhet", "ny-venter", [APP]],
  ["koble-enhet", "ny-ferdig", [APP]],
  ["koble-enhet", "avvist-utlopt", [APP]],
  ["koble-enhet", "avvist-avslaatt", [APP]],
  ["koble-enhet", "avvist-passkey", [WEB]],
  ["hjemmescaffold", "ikke-koblet", [WEB]],
  ["hjemmescaffold", "koblet", [WEB]],
  ["hjemmescaffold", "feil-passkey", [WEB]],
];

async function open(browser, viewport, scale) {
  const page = await browser.newPage({ viewport, deviceScaleFactor: scale });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (m) => { if (m.type() === "warning" || m.type() === "error") errors.push(m.type() + ": " + m.text()); });
  await route(page);
  await page.goto("http://entitet.kandidat.test/");
  await page.waitForFunction(() => Boolean(window.HavenSkeletonRuntime?.createRenderer));
  return { page, errors };
}

(async () => {
  const browser = await chromium.launch();
  const report = { shots: {}, behaviour: {} };
  for (const [surface, stateName, viewports] of SHOTS) {
    const cfg = load(`${surface}.cellconfiguration.json`);
    const state = load(`state-${surface}-${stateName}.json`);
    for (const viewport of viewports) {
      const kind = viewport.width < 700 ? "app" : "web";
      const name = `${surface}-${kind}-${stateName}-v1`;
      const { page, errors } = await open(browser, viewport, 2);
      await mount(page, cfg.skeleton, state, viewport);
      // Bare flaten, ikke tomrommet under den.
      await page.locator("main.canvas").screenshot({ path: path.join(IMG, `${name}.png`) });
      const dom = await page.evaluate(() => ({
        unsupported: Array.from(document.querySelectorAll("[data-skeleton-error]")).map((e) => e.textContent),
        buttons: Array.from(document.querySelectorAll("button")).filter((b) => b.offsetParent !== null).map((b) => b.textContent.trim()),
        inputs: document.querySelectorAll("input").length,
        overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      }));
      report.shots[name] = { errors, dom };
      console.log("ok", name, JSON.stringify(dom), errors.slice(0, 2).join(" | "));
      await page.close();
    }
  }

  // Oppførselsprøve: hva sender hver knapp og hvert felt til cellen?
  const press = async (surface, stateName, viewport, act) => {
    const cfg = load(`${surface}.cellconfiguration.json`);
    const { page } = await open(browser, viewport, 1);
    await mount(page, cfg.skeleton, load(`state-${surface}-${stateName}.json`), viewport);
    await act(page);
    await page.waitForTimeout(150);
    report.behaviour[`${surface}/${stateName}`] = await page.evaluate(() => window.__actions);
    await page.close();
  };
  const click = (label, nth = 0) => (page) => page.locator("button:visible", { hasText: label }).nth(nth).click();
  await press("min-entitet", "alt-naabart", WEB, async (page) => {
    await click("Trekk tilbake", 0)(page);
    await click("Koble til en ny enhet")(page);
    await click("Sjekk nå")(page);
  });
  await press("koble-enhet", "eier-start", WEB, click("Lag koblingskode"));
  await press("koble-enhet", "eier-godkjenn", WEB, async (page) => { await click("Godkjenn med passkey")(page); await click("Avvis")(page); });
  await press("koble-enhet", "ny-start", APP, async (page) => {
    const field = page.locator("input").first();
    await field.fill("4F7K-92QD");
    await field.press("Enter");
  });
  await press("koble-enhet", "eier-ferdig", WEB, click("Se «Min entitet»"));
  await press("hjemmescaffold", "ikke-koblet", WEB, click("Koble til med passkey"));
  console.log("behaviour", JSON.stringify(report.behaviour, null, 1));
  fs.writeFileSync(path.join(IMG, "render-report.json"), JSON.stringify(report, null, 2) + "\n");
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
