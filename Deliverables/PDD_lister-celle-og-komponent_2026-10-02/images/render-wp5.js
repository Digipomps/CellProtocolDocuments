// WP5 — rendrer «Mine lister» og verten med ComponentSurface fra cellens EKTE lists.state
// (skeleton/state-fra-cellen.json, skrevet av ListsCellTests.testPrintsRealStateForTheWebHarness),
// og måler oppførsel inne i en montering: handlingen skal bære mount.instanceID == listId.
// Kjør fra images/:  node render-wp5.js   (WEB_SRC = mappe med skeleton-runtime.js, porthole-webo.css, haven-localization.js)
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");
const SRC = process.env.WEB_SRC || "/mnt/user-data/uploads/HAVEN/_to_delete/losen-lister-render-20261002";
const OUT = process.env.OUT || path.join(__dirname, "..", "skeleton");
const IMG = process.env.IMG || __dirname;
const WEB = { width: 1180, height: 820 };
const APP = { width: 390, height: 844 };
function harnessHTML() {
  return ["<!doctype html><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
    "<title>Lister — fra cellen</title><link rel=\"stylesheet\" href=\"/css/porthole-webo.css\">",
    "<style>body{margin:0;background:#fff;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif;}.canvas{padding:0}</style></head>",
    "<body><main class=\"canvas product-view view-mode\"><div id=\"root\" class=\"skeleton-host\"></div></main>",
    "<script src=\"/js/haven-localization.js\"></script><script src=\"/js/skeleton-runtime.js\"></script></body></html>"].join("");
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
async function mount(page, skeleton, state, viewport, capabilities) {
  await page.evaluate(({ skeleton, state, viewport, capabilities }) => {
    window.__actions = [];
    const root = document.getElementById("root"); root.innerHTML = "";
    window.__renderer = window.HavenSkeletonRuntime.createRenderer({ rootElement: root, skeleton,
      onAction: async (keypath, payload, meta) => { window.__actions.push({ keypath, payload, meta }); return { status: "ok" }; } });
    window.__renderer.setLayoutContext?.({ availableWidth: viewport.width - 32, availableHeight: viewport.height, capabilities });
    window.__renderer.update(state);
  }, { skeleton, state, viewport, capabilities });
  await page.waitForTimeout(150);
}
const load = (f) => JSON.parse(fs.readFileSync(path.join(OUT, f), "utf8"));
const arrowSel = "[data-skeleton-icon='chevron.up'],[data-skeleton-icon='chevron.down']";
(async () => {
  const b = await chromium.launch();
  const cfg = load("mine-lister.cellconfiguration.json");
  const host = load("vert-med-komponenter.cellconfiguration.json");
  const state = load("state-fra-cellen.json");
  const DRAG = ["pointer", "hover", "keyboard", "drag"], NODRAG = ["touch"];
  const report = { source: "skeleton/state-fra-cellen.json (ListsCellTests.testPrintsRealStateForTheWebHarness)", shots: {}, variants: {}, mountBehaviour: {} };
  const shots = [
    ["mine-lister-web-fra-cellen", cfg.skeleton, WEB, DRAG],
    ["mine-lister-app-fra-cellen", cfg.skeleton, APP, NODRAG],
    ["vert-komponenter-web-fra-cellen", host.skeleton, WEB, DRAG],
  ];
  for (const [name, skeleton, viewport, caps] of shots) {
    const page = await b.newPage({ viewport, deviceScaleFactor: 2 });
    const errors = [];
    page.on("pageerror", (e) => errors.push(String(e)));
    page.on("console", (m) => { if (m.type() === "warning" || m.type() === "error") errors.push(m.type() + ": " + m.text()); });
    await route(page); await page.goto("http://lister.fra-cellen.test/");
    await page.waitForFunction(() => Boolean(window.HavenSkeletonRuntime?.createRenderer));
    await mount(page, skeleton, state, viewport, caps);
    await page.screenshot({ path: path.join(IMG, `${name}-v1.png`), fullPage: true });
    report.shots[name] = { errors, dom: await page.evaluate((arrowSel) => ({
      unsupported: Array.from(document.querySelectorAll("[data-skeleton-error]")).map((e) => e.textContent),
      componentErrors: Array.from(document.querySelectorAll(".skeleton-component-surface")).map((e) => e.dataset.skeletonError || "ok"),
      unmappedIcons: Array.from(document.querySelectorAll("[data-skeleton-icon]")).filter((s) => s.dataset.skeletonIconResolved === "circle-question-mark").map((s) => s.dataset.skeletonIcon),
      arrowsVisible: Array.from(document.querySelectorAll(arrowSel)).filter((s) => !s.closest("[data-layout-hidden='true']") && !s.closest("[data-visibility-state='hidden']")).length,
      titles: Array.from(document.querySelectorAll("input[placeholder='Listenavn']")).map((i) => i.value),
    }), arrowSel) };
    console.log("ok", name, JSON.stringify(report.shots[name].dom), errors.length ? errors.slice(0, 2) : "");
    await page.close();
  }
  for (const [label, caps, viewport] of [["drag", DRAG, WEB], ["noDrag", NODRAG, WEB], ["narrowNoDrag", NODRAG, APP]]) {
    const page = await b.newPage({ viewport }); await route(page); await page.goto("http://lister.fra-cellen.test/");
    await page.waitForFunction(() => Boolean(window.HavenSkeletonRuntime?.createRenderer));
    await mount(page, cfg.skeleton, state, viewport, caps);
    report.variants[label] = await page.evaluate((arrowSel) => ({
      arrowButtonsTotal: document.querySelectorAll(arrowSel).length,
      arrowsLayoutHidden: Array.from(document.querySelectorAll(arrowSel)).filter((s) => s.closest("[data-layout-hidden='true']")).length,
      arrowsVisibleOpenRows: Array.from(document.querySelectorAll(arrowSel)).filter((s) => !s.closest("[data-layout-hidden='true']") && !s.closest("[data-visibility-state='hidden']")).length,
      columnsFlexDirection: (() => { const c = document.querySelector("#root > * > *"); return c ? getComputedStyle(c).flexDirection : "?"; })(),
    }), arrowSel);
    console.log("variant", label, JSON.stringify(report.variants[label]));
    await page.close();
  }
  const page = await b.newPage({ viewport: WEB }); await route(page); await page.goto("http://lister.fra-cellen.test/");
  await page.waitForFunction(() => Boolean(window.HavenSkeletonRuntime?.createRenderer));
  await mount(page, host.skeleton, state, WEB, DRAG);
  const surfaces = page.locator(".skeleton-component-surface");
  report.mountBehaviour.mounts = await surfaces.count();
  const second = surfaces.nth(1);
  report.mountBehaviour.secondInstance = await second.getAttribute("data-instance-id");
  await second.locator("button:visible", { hasText: "○" }).first().click();
  const add = second.locator("input[placeholder='Legg til …']").first();
  await add.fill("Kjøpe gave"); await add.press("Enter");
  await page.waitForTimeout(200);
  report.mountBehaviour.actions = await page.evaluate(() => window.__actions.map((a) => ({ keypath: a.keypath, payload: a.payload, mount: a.meta && a.meta.mount, sourceCellEndpoint: a.meta && a.meta.sourceCellEndpoint })));
  console.log("mountBehaviour", JSON.stringify(report.mountBehaviour, null, 1));
  await page.close();
  fs.writeFileSync(path.join(IMG, "render-report-wp5.json"), JSON.stringify(report, null, 2));
  await b.close();
})().catch((e) => { console.error(e); process.exit(1); });
