// Rendrer kandidat-skjelettene gjennom CellScaffolds EGEN web-renderer
// (Public/js/skeleton-runtime.js + Public/css/porthole-webo.css fra origin/main,
// md5 i images/README.md) i Chromium. Ingen piksel er tegnet for hånd.
// Kjør:  node render.js   (etter python3 gen_skeleton.py)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const SRC = process.env.WEB_SRC || "/mnt/user-data/uploads/HAVEN/_to_delete/losen-lister-render-20261002";
const OUT = process.env.OUT || path.join(__dirname, "..", "skeleton");
const IMG = process.env.IMG || __dirname;
fs.mkdirSync(IMG, { recursive: true });

const WEB = { width: 1180, height: 820 };
const APP = { width: 390, height: 844 };

function harnessHTML() {
  return [
    "<!doctype html><html><head><meta charset=\"utf-8\">",
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
    "<title>Lister — kandidat</title>",
    "<link rel=\"stylesheet\" href=\"/css/porthole-webo.css\">",
    "<style>body{margin:0;background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;}",
    ".canvas{padding:0}</style>",
    "</head><body><main class=\"canvas product-view view-mode\"><div id=\"root\" class=\"skeleton-host\"></div></main>",
    "<script src=\"/js/haven-localization.js\"></script>",
    "<script src=\"/js/skeleton-runtime.js\"></script></body></html>",
  ].join("");
}

async function route(page) {
  await page.route("**/*", async (r) => {
    const u = new URL(r.request().url());
    if (u.pathname === "/" ) return r.fulfill({ contentType: "text/html", body: harnessHTML() });
    if (u.pathname === "/js/skeleton-runtime.js") return r.fulfill({ path: path.join(SRC, "skeleton-runtime.js"), contentType: "application/javascript" });
    if (u.pathname === "/js/haven-localization.js") return r.fulfill({ path: path.join(SRC, "haven-localization.js"), contentType: "application/javascript" });
    if (u.pathname === "/css/porthole-webo.css") return r.fulfill({ path: path.join(SRC, "porthole-webo.css"), contentType: "text/css" });
    return r.abort();
  });
}

async function mountSkeleton(page, skeleton, state, viewport) {
  await page.evaluate(({ skeleton, state, viewport }) => {
    window.__actions = [];
    const root = document.getElementById("root");
    root.innerHTML = "";
    window.__renderer = window.HavenSkeletonRuntime.createRenderer({
      rootElement: root,
      skeleton,
      onAction: async (keypath, payload, meta) => { window.__actions.push({ keypath, payload, meta }); return { status: "ok" }; },
    });
    if (window.__renderer.setLayoutContext) {
      window.__renderer.setLayoutContext({ availableWidth: viewport.width - 32, availableHeight: viewport.height, capabilities: ["pointer", "hover", "keyboard", "drag"] });
    }
    window.__renderer.update(state);
  }, { skeleton, state, viewport });
  await page.waitForTimeout(120);
}

const load = (f) => JSON.parse(fs.readFileSync(path.join(OUT, f), "utf8"));

(async () => {
  const b = await chromium.launch();
  const cfg = load("mine-lister.cellconfiguration.json");
  const host = load("vert-med-komponenter.cellconfiguration.json");
  const shots = [
    ["mine-lister-web-fylt", cfg.skeleton, load("state-fylt.json"), WEB],
    ["mine-lister-web-tom", cfg.skeleton, load("state-tom.json"), WEB],
    ["mine-lister-web-ny-liste", cfg.skeleton, load("state-ny-liste.json"), WEB],
    ["mine-lister-web-feil", cfg.skeleton, load("state-feil.json"), WEB],
    ["mine-lister-app-fylt", cfg.skeleton, load("state-fylt.json"), APP],
    ["mine-lister-app-tom", cfg.skeleton, load("state-tom.json"), APP],
    ["vert-komponenter-web-fylt", host.skeleton, load("state-fylt.json"), WEB],
    ["vert-komponenter-app-fylt", host.skeleton, load("state-fylt.json"), APP],
  ];
  const report = {};
  for (const [name, skeleton, state, viewport] of shots) {
    const page = await b.newPage({ viewport, deviceScaleFactor: 2 });
    const errors = [];
    page.on("pageerror", (e) => errors.push(String(e)));
    page.on("console", (m) => { if (m.type() === "warning" || m.type() === "error") errors.push(m.type() + ": " + m.text()); });
    await route(page);
    await page.goto("http://lister.kandidat.test/");
    await page.waitForFunction(() => Boolean(window.HavenSkeletonRuntime?.createRenderer));
    await mountSkeleton(page, skeleton, state, viewport);
    const file = path.join(IMG, `${name}-v1.png`);
    await page.screenshot({ path: file, fullPage: true });
    const dom = await page.evaluate(() => ({
      unsupported: Array.from(document.querySelectorAll("[data-skeleton-error]")).map((e) => e.textContent),
      hiddenCount: document.querySelectorAll("[data-visibility-state='hidden']").length,
      buttons: document.querySelectorAll("button").length,
      inputs: document.querySelectorAll("input").length,
      componentErrors: Array.from(document.querySelectorAll(".skeleton-component-surface-error, .skeleton-component-surface")).map((e) => e.dataset.skeletonError || "ok"),
      unmappedIcons: Array.from(document.querySelectorAll("[data-skeleton-icon]")).filter((s) => s.dataset.skeletonIconResolved === "circle-question-mark").map((s) => s.dataset.skeletonIcon),
    }));
    report[name] = { file: path.basename(file), errors, dom };
    console.log("ok", name, JSON.stringify(dom), errors.length ? errors.slice(0, 3) : "");
    await page.close();
  }

  // Oppførselsprøve på web-rendereren: trykk, Enter i felt, drag — hva sendes til cellen?
  const page = await b.newPage({ viewport: WEB });
  await route(page);
  await page.goto("http://lister.kandidat.test/");
  await page.waitForFunction(() => Boolean(window.HavenSkeletonRuntime?.createRenderer));
  await mountSkeleton(page, cfg.skeleton, load("state-fylt.json"), WEB);
  const beh = {};
  // 1) kryss av «Melk»: første synlige ○-knapp
  const toggle = page.locator("button:visible", { hasText: "○" }).first();
  await toggle.click();
  // 2) skriv i «Legg til …» og trykk Enter
  const add = page.locator("input[placeholder='Legg til …']").first();
  await add.fill("Ost");
  await add.press("Enter");
  // 3) ny liste
  const nl = page.locator("input[placeholder='Ny liste … (Enter)']").first();
  await nl.fill("Pakkeliste");
  await nl.press("Enter");
  // 4) velg «Huskeliste» i listen av lister (radklikk)
  await page.locator("div.skeleton-text:visible", { hasText: "Huskeliste" }).first().click();
  // 5) dra «Brød» ned på «Kaffe»
  const rows = page.locator("[data-drop-target-role='list-item-slot']");
  beh.dropTargets = await rows.count();
  if (beh.dropTargets >= 4) {
    await rows.nth(1).dragTo(rows.nth(3));
  }
  await page.waitForTimeout(200);
  beh.actions = await page.evaluate(() => window.__actions);
  report.behaviour = beh;
  console.log("behaviour", JSON.stringify(beh, null, 1).slice(0, 4000));
  await page.close();
  fs.writeFileSync(path.join(IMG, "render-report.json"), JSON.stringify(report, null, 2));
  await b.close();
})().catch((e) => { console.error(e); process.exit(1); });
