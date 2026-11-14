// node render.js <ut-mappe> — rendrer skjelettet med CellScaffold sin skeleton-runtime.js og porthole-webo.css
const path = require("node:path");
const { chromium } = require("playwright");
const { analyseromSkeleton } = require("./analyserom-skeleton.js");
const states = require("./analyserom-states.js");
const publicDir = process.env.CELLSCAFFOLD_PUBLIC || "/home/user/cellscaffold/Public";
const out = process.argv[2];
(async () => {
  const browser = await chromium.launch();
  for (const [vname, vp] of [["laptop", { width: 1280, height: 900 }], ["iphone", { width: 390, height: 844 }]]) {
    for (const [sname, state] of Object.entries(states)) {
      const page = await browser.newPage({ viewport: vp, deviceScaleFactor: 2 });
      const errors = []; page.on("pageerror", (e) => errors.push(e.message));
      await page.route("**/*", async (route) => {
        const url = new URL(route.request().url());
        if (url.pathname === "/") return route.fulfill({ contentType: "text/html", body: `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/css/porthole-webo.css"></head><body style="margin:0;background:#fff"><main class="canvas view-mode"><div id="root" class="skeleton-host"></div></main><script src="/js/skeleton-runtime.js"></script></body></html>` });
        if (url.pathname === "/js/skeleton-runtime.js") return route.fulfill({ path: path.join(publicDir, "js", "skeleton-runtime.js"), contentType: "application/javascript" });
        if (url.pathname === "/css/porthole-webo.css") return route.fulfill({ path: path.join(publicDir, "css", "porthole-webo.css"), contentType: "text/css" });
        return route.abort();
      });
      await page.goto("http://analyserom.test/");
      await page.evaluate(({ skeleton, state, w, h }) => {
        const root = document.getElementById("root");
        window.HavenSkeletonRuntime.createRenderer({ rootElement: root, skeleton, layoutContext: { availableWidth: root.clientWidth || w, availableHeight: h }, onAction: async () => {} }).update(state);
      }, { skeleton: analyseromSkeleton, state, w: vp.width, h: vp.height });
      await page.waitForTimeout(800);
      const file = path.join(out, `analyserom-${sname}-${vname}-v1.png`);
      await page.screenshot({ path: file, fullPage: true });
      console.log(file, errors.length ? "FEIL: " + errors.join(" | ") : "");
      await page.close();
    }
  }
  await browser.close();
})();
