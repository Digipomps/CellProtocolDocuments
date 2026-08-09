#!/usr/bin/env node

const assert = require("node:assert/strict");
const path = require("node:path");

const playwrightModule = process.env.PLAYWRIGHT_MODULE
  || path.resolve(__dirname, "../../../CellScaffold/node_modules/playwright");
const { chromium } = require(playwrightModule);

const baseURL = process.argv[2] || "http://127.0.0.1:4173";
const screenshotPath = process.argv[3] || "";

async function visibleHeroActions(page) {
  return page.locator(".hero .hero-actions a:visible");
}

async function verifyStaticJourney(browser, javaScriptEnabled) {
  const context = await browser.newContext({
    javaScriptEnabled,
    viewport: { width: 1280, height: 900 },
  });
  const page = await context.newPage();
  const response = await page.goto(`${baseURL}/`, { waitUntil: "domcontentloaded" });
  assert.equal(response.status(), 200);
  await page.waitForLoadState("load");
  assert.equal(await page.locator("section.hero").getAttribute("data-app-entry-state"), "blocked");

  const actions = await visibleHeroActions(page);
  assert.equal(await actions.count(), 2);
  assert.deepEqual(await actions.allTextContents(), [
    "Se et tidlig testbevis",
    "Mennesket først – ikke mennesket alene",
  ]);
  assert.equal(await actions.nth(0).getAttribute("href"), "/bevis/tilgangskontroll/");
  assert.equal(await actions.nth(1).getAttribute("href"), "#mennesket-og-fellesskapet");
  assert.equal(await actions.nth(0).getAttribute("target"), null);
  assert.equal(await actions.nth(1).getAttribute("target"), null);

  const loadedVisuals = await page.evaluate(() => ({
    logo: [...document.images].some((image) => image.src.includes("haven-logo.png") && image.complete && image.naturalWidth > 0),
    hero: [...document.images].some((image) => image.src.includes("haven-human-agency-20260803.webp") && image.complete && image.naturalWidth > 0),
    problem: [...document.images].some((image) => image.src.includes("haven-human-workshop.webp") && image.complete && image.naturalWidth > 0),
    controlLoop: [...document.images].some((image) => image.src.includes("haven-control-loop-20260803.webp") && image.complete && image.naturalWidth > 0),
    bodyBackground: getComputedStyle(document.body).backgroundColor,
    primaryBackground: getComputedStyle(document.querySelector(".hero .button-primary")).backgroundColor,
  }));
  assert.equal(loadedVisuals.logo, true);
  assert.equal(loadedVisuals.hero, true);
  assert.equal(loadedVisuals.problem, true);
  assert.equal(loadedVisuals.controlLoop, true);
  assert.notEqual(loadedVisuals.bodyBackground, "rgba(0, 0, 0, 0)");
  assert.notEqual(loadedVisuals.primaryBackground, "rgba(0, 0, 0, 0)");

  if (javaScriptEnabled && screenshotPath) {
    await page.screenshot({ path: screenshotPath, fullPage: true });
  }

  const devtools = await context.newCDPSession(page);
  const accessibilityTree = await devtools.send("Accessibility.getFullAXTree");
  const accessibleLinkNames = accessibilityTree.nodes
    .filter((node) => node.role?.value === "link")
    .map((node) => node.name?.value || "");
  assert(accessibleLinkNames.includes("Se et tidlig testbevis"));
  assert(accessibleLinkNames.includes("Mennesket først – ikke mennesket alene"));
  await devtools.detach();

  assert.equal(
    await page.locator("h1").textContent(),
    "Hva sa du egentlig ja til?",
  );
  assert.equal(await page.locator("#kjenner-du-deg-igjen .problem-card").count(), 3);
  // Filmen ligger i heroen, ikke i problemseksjonen, og skal finnes bare én gang.
  const film = page.locator("section.hero .hero-figure video");
  assert.equal(await film.count(), 1);
  assert.equal(await page.locator("video").count(), 1);
  assert.equal(await film.getAttribute("poster"), "/assets/haven-hero-film-poster-20260807.webp");
  assert.equal(
    await page.locator("section.hero .hero-figure source").getAttribute("src"),
    "/assets/haven-hero-film-20260807.mp4",
  );
  // Filmen skal ha samme format som i produksjon: maks 52rem og sentrert på siden.
  const filmBoks = await film.evaluate((node) => {
    const rect = node.getBoundingClientRect();
    return { left: rect.left, right: rect.right, width: rect.width, viewport: window.innerWidth };
  });
  assert.ok(
    filmBoks.width <= 52 * 16 + 1,
    `filmen er bredere enn 52rem: ${Math.round(filmBoks.width)}px`,
  );
  const filmSenter = (filmBoks.left + filmBoks.right) / 2;
  assert.ok(
    Math.abs(filmSenter - filmBoks.viewport / 2) <= 1,
    `filmen er ikke sentrert: senter ${Math.round(filmSenter)} mot side ${filmBoks.viewport / 2}`,
  );
  // Autoavspilling er stum og har kontroller, slik at bevegelsen kan stoppes (WCAG 2.2.2).
  assert.equal(await film.evaluate((node) => node.controls), true);
  assert.equal(await film.evaluate((node) => node.autoplay), true);
  assert.equal(await film.evaluate((node) => node.muted), true);
  // Filmen skal stoppe på siste bilde, ikke gå i sløyfe.
  assert.equal(await film.evaluate((node) => node.loop), false);
  assert.deepEqual(await page.locator("#kjenner-du-deg-igjen .stat-number").allTextContents(), [
    "244 timer",
    "50 prosent",
    "74 prosent",
  ]);
  const openingText = `${await page.locator("section.hero").innerText()} ${await page.locator("#kjenner-du-deg-igjen").innerText()}`.toLowerCase();
  for (const forbiddenOpeningTerm of ["agent", "protokoll", "cells", "myndighet"]) {
    assert.equal(openingText.includes(forbiddenOpeningTerm), false);
  }
  const mainText = (await page.locator("main").innerText()).toLowerCase();
  // Første forekomst av «agent» skal være ordet inne i definisjonssetningen,
  // som starter tre tegn tidligere («en agent …»).
  assert.equal(mainText.indexOf("agent"), mainText.indexOf("en agent er en tjeneste som handler for deg") + "en ".length);
  assert(mainText.indexOf("agent") > mainText.indexOf("ikke én app. ikke én plattform. et åpent økosystem."));
  assert.equal(await page.getByText("Hypotese – ikke dokumentert effekt", { exact: true }).count(), 1);
  assert.equal(await page.getByText("Retning / hypotese – ikke dokumentert effekt", { exact: true }).count(), 1);
  assert.equal(await page.getByText("En agent er en tjeneste som handler for deg.", { exact: false }).count(), 1);

  if (javaScriptEnabled) {
    const sourcePage = await context.newPage();
    const sourceResponse = await sourcePage.goto(`${baseURL}/kilder/#forside-statistikk`, { waitUntil: "domcontentloaded" });
    assert.equal(sourceResponse.status(), 200);
    assert.equal(await sourcePage.locator("#forside-statistikk tbody tr").count(), 4);
    for (const sourceID of ["stat-kontroll-2024", "stat-ubehag-2024", "stat-app-2024", "stat-vilkar-2008"]) {
      assert.equal(await sourcePage.locator(`#${sourceID}`).count(), 1);
    }
    await sourcePage.close();

    const articlePage = await context.newPage();
    const articleResponse = await articlePage.goto(`${baseURL}/artikler/verktoy-som-samarbeider/`, { waitUntil: "domcontentloaded" });
    assert.equal(articleResponse.status(), 200);
    assert.equal(await articlePage.locator("h1").textContent(), "Verktøy som samarbeider");
    assert.equal(await articlePage.getByText("Grensen", { exact: true }).count(), 1);
    await articlePage.close();
  }

  let focusedLabel = "";
  for (let index = 0; index < 20 && focusedLabel !== "Se et tidlig testbevis"; index += 1) {
    await page.keyboard.press("Tab");
    focusedLabel = await page.evaluate(() => document.activeElement?.textContent?.trim() || "");
  }
  assert.equal(focusedLabel, "Se et tidlig testbevis");
  const focusStyle = await page.evaluate(() => {
    const style = getComputedStyle(document.activeElement);
    return { outlineStyle: style.outlineStyle, outlineWidth: style.outlineWidth };
  });
  assert.notEqual(focusStyle.outlineStyle, "none");
  assert.notEqual(focusStyle.outlineWidth, "0px");

  await page.evaluate(() => {
    document.documentElement.style.fontSize = "200%";
  });
  const overflowingElements = await page.evaluate(() => {
    const viewportWidth = document.documentElement.clientWidth;
    if (document.documentElement.scrollWidth <= viewportWidth + 1) return [];
    return [...document.querySelectorAll("body *")]
      .map((element) => {
        const rectangle = element.getBoundingClientRect();
        return {
          tag: element.tagName.toLowerCase(),
          className: element.className?.toString() || "",
          text: element.textContent?.trim().slice(0, 60) || "",
          left: Math.round(rectangle.left),
          right: Math.round(rectangle.right),
          width: Math.round(rectangle.width),
        };
      })
      .filter((item) => item.left < -1 || item.right > viewportWidth + 1);
  });
  assert.deepEqual(overflowingElements, []);
  await context.close();
}

async function verifyMobile(browser) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await context.newPage();
  await page.goto(`${baseURL}/`, { waitUntil: "domcontentloaded" });
  assert.equal(await visibleHeroActions(page).then((actions) => actions.count()), 2);
  const horizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  assert.equal(horizontalOverflow, false);
  await context.close();
}

// Med redusert bevegelse skal filmen byttes ut med sluttkortet, uten layouthopp.
async function verifyReducedMotion(browser) {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    reducedMotion: "reduce",
  });
  const page = await context.newPage();
  await page.goto(`${baseURL}/`, { waitUntil: "load" });
  const state = await page.evaluate(() => {
    const video = document.querySelector(".hero-figure video");
    const still = document.querySelector(".hero-figure .hero-still");
    const box = (el) => {
      const rect = el.getBoundingClientRect();
      return { width: Math.round(rect.width), height: Math.round(rect.height) };
    };
    return {
      videoHidden: getComputedStyle(video).display === "none",
      stillShown: getComputedStyle(still).display !== "none",
      stillLoaded: still.complete && still.naturalWidth > 0,
      stillSrc: still.currentSrc,
      stillBox: box(still),
    };
  });
  assert.equal(state.videoHidden, true);
  assert.equal(state.stillShown, true);
  assert.equal(state.stillLoaded, true);
  // Stillbildet viser menneskene, ikke sluttkortet – filmen ender allerede på kortet,
  // og da ville de to flatene vist det samme motivet.
  assert.ok(
    state.stillSrc.includes("haven-human-agency-20260803.webp"),
    `stillbildet skal vise menneskene, ikke sluttkortet: ${state.stillSrc}`,
  );
  assert.ok(
    !state.stillSrc.includes("sluttkort"),
    `stillbildet duplikerer filmens sluttbilde: ${state.stillSrc}`,
  );
  await context.close();
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    await verifyStaticJourney(browser, true);
    await verifyStaticJourney(browser, false);
    await verifyMobile(browser);
    await verifyReducedMotion(browser);
    console.log("OK: new concern-first variant, blocked app entry, copy order, sources, images, no-JS, AX, keyboard focus, mobile layout and reduced-motion fallback passed.");
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
