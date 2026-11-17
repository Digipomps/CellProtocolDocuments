#!/usr/bin/env node
// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

const fs = require("node:fs/promises");
const path = require("node:path");
const crypto = require("node:crypto");
const { chromium, expect } = require("@playwright/test");

const defaultBaseURL = process.env.CONFERENCE_DEMO_BASE_URL || "https://staging.haven.digipomps.org";
const generatedUsername = `conference-skeleton-iterate-${crypto.randomUUID().slice(0, 8)}`;
const generatedPassword = `skeleton-${crypto.randomUUID()}`;
const defaultUsername = process.env.CONFERENCE_DEMO_USERNAME || generatedUsername;
const defaultPassword = process.env.CONFERENCE_DEMO_PASSWORD || generatedPassword;
const defaultViewports = [
  { name: "desktop", width: 1440, height: 1000 },
  { name: "mobile", width: 390, height: 844 },
];
const allowedModes = new Set(["export", "preview", "commit-runtime", "review", "view-smoke"]);

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const scenario = await loadScenario(args);
  const config = normalizeConfig(scenario, args);
  const skeleton = config.skeletonPath ? await readJSON(config.skeletonPath) : null;
  const outputDir = await prepareOutputDir(config);
  const browser = await chromium.launch({ headless: !config.headed });
  const runSummary = {
    mode: config.mode,
    baseURL: config.baseURL,
    persona: config.persona || null,
    configurationName: config.configurationName,
    sourceCellEndpoint: config.sourceCellEndpoint,
    skeletonSource: config.skeletonSource,
    outputDir,
    viewports: [],
    startedAt: new Date().toISOString(),
  };

  try {
    for (const viewport of config.viewports) {
      const result = await runViewport({
        browser,
        config,
        skeleton,
        viewport,
        outputDir,
      });
      runSummary.viewports.push(result);
    }

    runSummary.finishedAt = new Date().toISOString();
    await fs.writeFile(
      path.join(outputDir, "run-summary.json"),
      JSON.stringify(runSummary, null, 2),
      "utf8"
    );

    if (config.mode === "review") {
      await writeReviewBundle({ outputDir, config, skeleton, runSummary });
    }

    console.log(`skeleton:iterate ${config.mode} completed`);
    console.log(`artifacts: ${outputDir}`);

    if (config.mode === "export") {
      const exported = runSummary.viewports.find((entry) => entry.exported)?.exported;
      if (exported) {
        console.log(`configuration: ${exported.configurationPath}`);
        console.log(`skeleton:      ${exported.skeletonPath}`);
        console.log(`manifest:      ${exported.manifestPath}`);
        console.log(`revision:      ${exported.manifest.committedSourceRevision ?? "none"} (skeleton sha256 ${exported.manifest.skeletonSha256.slice(0, 12)})`);
        if (exported.manifest.canEdit !== true) {
          console.log("note: this Identity cannot commit runtime changes here. An owner-authorized Agreement must grant rw-s for applyEditableCellConfiguration on this source cell.");
        }
      }
    }
  } finally {
    await browser.close();
  }
}

async function runViewport({ browser, config, skeleton, viewport, outputDir }) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    ignoreHTTPSErrors: config.ignoreHTTPSErrors,
  });
  const page = await context.newPage();
  const consoleMessages = [];
  const pageErrors = [];
  const actionResults = [];
  const viewportDir = path.join(outputDir, viewport.name);
  let tracing = false;
  await fs.mkdir(viewportDir, { recursive: true });

  page.on("console", (message) => {
    consoleMessages.push({
      type: message.type(),
      text: message.text(),
    });
  });
  page.on("pageerror", (error) => {
    pageErrors.push({
      name: error?.name || "Error",
      message: error?.message || String(error),
    });
  });

  try {
    await context.tracing.start({ screenshots: true, snapshots: true, sources: true });
    tracing = true;
    await authenticateBrowserSession(context, config);
    await openPorthole(page, config);

    await ensureConfigurationLoaded(page, context, config);
    const beforeBootstrap = await requestBootstrap(context, config);

    if (config.mode === "export") {
      const exported = await writeExportBundle({
        page,
        config,
        bootstrap: beforeBootstrap,
        viewportDir,
      });
      await fs.writeFile(
        path.join(viewportDir, "console.json"),
        JSON.stringify({ consoleMessages, pageErrors }, null, 2),
        "utf8"
      );
      return {
        name: viewport.name,
        width: viewport.width,
        height: viewport.height,
        screenshotPath: exported.screenshotPath,
        domPath: exported.domPath,
        consoleMessageCount: consoleMessages.length,
        pageErrorCount: pageErrors.length,
        commitVerification: null,
        exported,
      };
    }

    if (config.mode === "view-smoke") {
      await discardPreviewWorkingState(context, config);
      await reloadPorthole(page, config);
      await expectActiveConfiguration(page, config.configurationName);
      await applyExpectations(page, config.expects);
      await expectNoConferenceCriticalLeaks(page, config);
      await runActions(page, context, config, config.actions || [], actionResults);
      await runActions(page, context, config, config.notificationChecks || [], actionResults);
      await expectNoConferenceCriticalLeaks(page, config);

      const afterBootstrap = await requestBootstrap(context, config);
      const screenshotPath = path.join(viewportDir, `${viewport.name}.png`);
      const domPath = path.join(viewportDir, `${viewport.name}.dom.txt`);
      const htmlPath = path.join(viewportDir, `${viewport.name}.html`);
      await page.screenshot({ path: screenshotPath, fullPage: true });
      await fs.writeFile(domPath, await page.locator("body").innerText().catch(() => ""), "utf8");
      await fs.writeFile(htmlPath, await page.content().catch(() => ""), "utf8");
      await fs.writeFile(path.join(viewportDir, "bootstrap-before.json"), JSON.stringify(beforeBootstrap, null, 2), "utf8");
      await fs.writeFile(path.join(viewportDir, "bootstrap-after-view.json"), JSON.stringify(afterBootstrap, null, 2), "utf8");
      await fs.writeFile(path.join(viewportDir, "action-results.json"), JSON.stringify(actionResults, null, 2), "utf8");
      await fs.writeFile(
        path.join(viewportDir, "console.json"),
        JSON.stringify({ consoleMessages, pageErrors }, null, 2),
        "utf8"
      );

      return {
        name: viewport.name,
        width: viewport.width,
        height: viewport.height,
        screenshotPath,
        domPath,
        consoleMessageCount: consoleMessages.length,
        pageErrorCount: pageErrors.length,
        commitVerification: null,
      };
    }

    if (config.mode !== "commit-runtime") {
      await discardPreviewWorkingState(context, config);
    } else {
      assertCommitRuntimeAccess(beforeBootstrap, config);
    }
    const workingSkeleton = resolveCandidateSkeleton({
      configuredSkeleton: skeleton,
      beforeBootstrap,
      config,
    });
    await postAction(context, config, "editor.mode.set", { mode: "edit" });
    await reloadPorthole(page, config);
    await postAction(context, config, "editor.working.setSkeleton", workingSkeleton);
    await reloadPorthole(page, config);
    await expectActiveConfiguration(page, config.configurationName);

    await applyExpectations(page, config.expects);
    await expectNoConferenceCriticalLeaks(page, config);
    await runActions(page, context, config, config.actions || [], actionResults);
    await runActions(page, context, config, config.notificationChecks || [], actionResults);
    await expectNoConferenceCriticalLeaks(page, config);

    const afterBootstrap = await requestBootstrap(context, config);
    const screenshotPath = path.join(viewportDir, `${viewport.name}.png`);
    const domPath = path.join(viewportDir, `${viewport.name}.dom.txt`);
    const htmlPath = path.join(viewportDir, `${viewport.name}.html`);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    await fs.writeFile(domPath, await page.locator("body").innerText().catch(() => ""), "utf8");
    await fs.writeFile(htmlPath, await page.content().catch(() => ""), "utf8");
    await fs.writeFile(path.join(viewportDir, "bootstrap-before.json"), JSON.stringify(beforeBootstrap, null, 2), "utf8");
    await fs.writeFile(path.join(viewportDir, "bootstrap-after-preview.json"), JSON.stringify(afterBootstrap, null, 2), "utf8");
    await fs.writeFile(path.join(viewportDir, "action-results.json"), JSON.stringify(actionResults, null, 2), "utf8");

    let commitVerification = null;
    if (config.mode === "commit-runtime") {
      const applyResult = await postAction(context, config, "editor.apply", null);
      if (applyResult?.result !== "applied") {
        throw new Error(`Porthole editor.apply did not commit the runtime configuration: ${JSON.stringify(applyResult)}`);
      }
      const committedBootstrap = await requestBootstrap(context, config);
      await fs.writeFile(path.join(viewportDir, "bootstrap-after-commit.json"), JSON.stringify(committedBootstrap, null, 2), "utf8");
      commitVerification = await verifyCommittedRuntime({
        browser,
        config,
        viewport,
        outputDir,
        expectedSkeleton: workingSkeleton,
      });
    }

    await fs.writeFile(
      path.join(viewportDir, "console.json"),
      JSON.stringify({ consoleMessages, pageErrors }, null, 2),
      "utf8"
    );
    if (config.mode !== "commit-runtime") {
      await discardPreviewWorkingState(context, config);
    }

    return {
      name: viewport.name,
      width: viewport.width,
      height: viewport.height,
      screenshotPath,
      domPath,
      consoleMessageCount: consoleMessages.length,
      pageErrorCount: pageErrors.length,
      commitVerification,
    };
  } catch (error) {
    await fs.writeFile(path.join(viewportDir, "action-results.json"), JSON.stringify(actionResults, null, 2), "utf8").catch(() => {});
    await requestBootstrap(context, config)
      .then((bootstrap) => fs.writeFile(path.join(viewportDir, "failure-bootstrap.json"), JSON.stringify(bootstrap, null, 2), "utf8"))
      .catch(() => {});
    if (tracing) {
      await context.tracing.stop({ path: path.join(viewportDir, "failure.trace.zip") }).catch(() => {});
      tracing = false;
    }
    await captureFailureArtifacts(page, viewportDir, error, consoleMessages, pageErrors);
    throw error;
  } finally {
    if (config.mode !== "commit-runtime" && config.mode !== "export") {
      await discardPreviewWorkingState(context, config);
    }
    if (tracing) {
      await context.tracing.stop().catch(() => {});
    }
    await context.close();
  }
}

async function writeExportBundle({ page, config, bootstrap, viewportDir }) {
  const editorState = bootstrap?.editorState || null;
  const configuration = bootstrap?.configuration || null;
  if (!configuration) {
    throw new Error("The Porthole bootstrap returned no active configuration to export.");
  }
  const skeleton = editorState?.committedSkeleton || configuration?.skeleton || null;
  if (!skeleton) {
    throw new Error("The active configuration exposed no skeleton to export.");
  }

  const targetDir = config.exportDir || viewportDir;
  await fs.mkdir(targetDir, { recursive: true });

  const configurationPath = path.join(targetDir, "active.cellconfiguration.json");
  const skeletonPath = path.join(targetDir, "active.skeleton.json");
  const manifestPath = path.join(targetDir, "export-manifest.json");
  const screenshotPath = path.join(viewportDir, "active.png");
  const domPath = path.join(viewportDir, "active.dom.txt");

  const exportedConfiguration = structuredClone(configuration);
  exportedConfiguration.skeleton = structuredClone(skeleton);

  const manifest = {
    capturedAt: new Date().toISOString(),
    baseURL: config.baseURL,
    configurationName: config.configurationName,
    sourceCellEndpoint: config.sourceCellEndpoint,
    sourceBacked: editorState?.sourceBacked ?? null,
    canEdit: editorState?.canEdit ?? null,
    isDirty: editorState?.isDirty ?? null,
    committedSourceRevision: editorState?.committedSourceRevision ?? null,
    hasStoredOverride: Number.isFinite(editorState?.committedSourceRevision)
      && editorState.committedSourceRevision > 0,
    accessSummary: editorState?.accessSummary ?? null,
    accessInstruction: editorState?.accessInstruction ?? null,
    skeletonSha256: sha256Hex(stableJSON(skeleton)),
    configurationSha256: sha256Hex(stableJSON(exportedConfiguration)),
    files: {
      configuration: displayPath(configurationPath),
      skeleton: displayPath(skeletonPath),
    },
    previewCommand: [
      "npm run skeleton:iterate --",
      "--mode preview",
      `--base-url ${config.baseURL}`,
      `--configuration-name ${JSON.stringify(config.configurationName)}`,
      `--source-cell-endpoint ${config.sourceCellEndpoint}`,
      `--skeleton-file ${displayPath(skeletonPath)}`,
    ].join(" "),
  };

  await fs.writeFile(configurationPath, JSON.stringify(exportedConfiguration, null, 2), "utf8");
  await fs.writeFile(skeletonPath, JSON.stringify(skeleton, null, 2), "utf8");
  await fs.writeFile(manifestPath, JSON.stringify(manifest, null, 2), "utf8");
  await fs.writeFile(path.join(viewportDir, "bootstrap-export.json"), JSON.stringify(bootstrap, null, 2), "utf8");
  await page.screenshot({ path: screenshotPath, fullPage: true }).catch(() => {});
  await fs.writeFile(domPath, await page.locator("body").innerText().catch(() => ""), "utf8");

  return { configurationPath, skeletonPath, manifestPath, screenshotPath, domPath, manifest };
}

// Relative inside the repo, absolute outside it, so the manifest never hands
// the reader a path that only resolves from one working directory.
function displayPath(target) {
  const relative = path.relative(process.cwd(), target);
  return relative && !relative.startsWith("..") ? relative : target;
}

function sha256Hex(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

async function discardPreviewWorkingState(context, config) {
  let discarded = false;
  try {
    await postAction(context, config, "editor.discard", null);
    discarded = true;
  } catch {}

  if (!discarded) {
    return;
  }

  await postAction(context, config, "editor.mode.set", { mode: "view" }).catch(() => {});
}

async function ensureConfigurationLoaded(page, context, config) {
  let addConfigurationError = null;
  try {
    await postAction(context, config, "addConfiguration", {
      configurationLookup: {
        name: config.configurationName,
        sourceCellEndpoint: config.sourceCellEndpoint,
      },
    });
  } catch (error) {
    addConfigurationError = error;
  }

  await reloadPorthole(page, config);
  try {
    await expectActiveConfiguration(page, config.configurationName);
  } catch (error) {
    throw addConfigurationError || error;
  }
}

async function verifyCommittedRuntime({ browser, config, viewport, outputDir, expectedSkeleton }) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    ignoreHTTPSErrors: config.ignoreHTTPSErrors,
  });
  const page = await context.newPage();
  const verifyDir = path.join(outputDir, viewport.name, "commit-verification");
  await fs.mkdir(verifyDir, { recursive: true });
  try {
    await authenticateBrowserSession(context, config);
    await openPorthole(page, config);
    await ensureConfigurationLoaded(page, context, config);
    await applyExpectations(page, config.expects);
    const bootstrap = await requestBootstrap(context, config);
    assertCommittedRuntimeBootstrap(bootstrap, config, expectedSkeleton);
    await fs.writeFile(path.join(verifyDir, "bootstrap-reloaded.json"), JSON.stringify(bootstrap, null, 2), "utf8");
    await page.screenshot({ path: path.join(verifyDir, `${viewport.name}.reloaded.png`), fullPage: true });
    await fs.writeFile(path.join(verifyDir, "dom.txt"), await page.locator("body").innerText().catch(() => ""), "utf8");
    return { ok: true, artifactDir: verifyDir };
  } finally {
    await context.close();
  }
}

function resolveCandidateSkeleton({ configuredSkeleton, beforeBootstrap, config }) {
  if (config.skeletonSource === "file") {
    if (!configuredSkeleton) {
      throw new Error("A skeleton file was selected but no skeleton was loaded.");
    }
    return structuredClone(configuredSkeleton);
  }

  const activeSkeleton = beforeBootstrap?.editorState?.committedSkeleton
    || beforeBootstrap?.editorState?.workingSkeleton
    || beforeBootstrap?.configuration?.skeleton
    || null;
  if (!activeSkeleton) {
    throw new Error("The active configuration did not expose a skeleton for the runtime commit probe.");
  }
  return skeletonWithToggledRuntimeProbe(activeSkeleton, config.runtimeProbeStyleClasses);
}

function skeletonWithToggledRuntimeProbe(skeleton, markerClasses) {
  const [firstMarker, secondMarker] = markerClasses;
  const candidate = structuredClone(skeleton);
  const elementPayload = findFirstElementPayload(candidate, ["Section", "Text"]);
  if (!elementPayload) {
    throw new Error("Could not find a Section or Text element for the runtime commit probe.");
  }
  const modifiers = isPlainObject(elementPayload.modifiers) ? elementPayload.modifiers : {};
  const existingClasses = Array.isArray(modifiers.styleClasses)
    ? modifiers.styleClasses.filter((entry) => typeof entry === "string")
    : [];
  const hadFirstMarker = existingClasses.includes(firstMarker);
  modifiers.styleClasses = [
    ...existingClasses.filter((entry) => entry !== firstMarker && entry !== secondMarker),
    hadFirstMarker ? secondMarker : firstMarker,
  ];
  elementPayload.modifiers = modifiers;
  return candidate;
}

function findFirstElementPayload(value, preferredElementNames) {
  if (Array.isArray(value)) {
    for (const item of value) {
      const found = findFirstElementPayload(item, preferredElementNames);
      if (found) return found;
    }
    return null;
  }
  if (!isPlainObject(value)) return null;

  for (const elementName of preferredElementNames) {
    if (isPlainObject(value[elementName])) {
      return value[elementName];
    }
  }
  for (const nested of Object.values(value)) {
    const found = findFirstElementPayload(nested, preferredElementNames);
    if (found) return found;
  }
  return null;
}

function assertCommitRuntimeAccess(bootstrap, config) {
  const editorState = bootstrap?.editorState;
  if (!editorState || editorState.sourceBacked !== true) {
    throw new Error("commit-runtime requires a source-backed CellConfiguration.");
  }
  if (editorState.canEdit !== true) {
    throw new Error(`commit-runtime is blocked for this Identity. An owner-authorized Agreement must grant rw-s for applyEditableCellConfiguration on ${config.sourceCellEndpoint}.`);
  }
  if (editorState.sourceCellEndpoint !== config.sourceCellEndpoint) {
    throw new Error(`commit-runtime resolved ${editorState.sourceCellEndpoint || "no source endpoint"}, expected ${config.sourceCellEndpoint}.`);
  }
}

function assertCommittedRuntimeBootstrap(bootstrap, config, expectedSkeleton) {
  assertCommitRuntimeAccess(bootstrap, config);
  const editorState = bootstrap.editorState;
  if (editorState.isDirty !== false) {
    throw new Error("The reloaded runtime editor state is still dirty after commit.");
  }
  if (!Number.isFinite(editorState.committedSourceRevision) || editorState.committedSourceRevision < 1) {
    throw new Error("The reloaded runtime configuration has no committed source revision.");
  }
  const committedSkeleton = editorState.committedSkeleton || bootstrap?.configuration?.skeleton || null;
  if (stableJSON(committedSkeleton) !== stableJSON(expectedSkeleton)) {
    throw new Error("The skeleton reloaded from the source cell does not match the committed runtime skeleton.");
  }
}

function stableJSON(value) {
  if (Array.isArray(value)) {
    return `[${value.map(stableJSON).join(",")}]`;
  }
  if (isPlainObject(value)) {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableJSON(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

function isPlainObject(value) {
  return value !== null && typeof value === "object" && Array.isArray(value) === false;
}

async function writeReviewBundle({ outputDir, config, skeleton, runSummary }) {
  const firstViewport = runSummary.viewports[0]?.name || "desktop";
  const firstViewportDir = path.join(outputDir, firstViewport);
  const beforePath = path.join(firstViewportDir, "bootstrap-before.json");
  const beforeBootstrap = await readJSON(beforePath).catch(() => ({}));
  const beforeSkeleton =
    beforeBootstrap?.editorState?.committedSkeleton ??
    beforeBootstrap?.editorState?.workingSkeleton ??
    null;
  const bootstrapConfiguration = beforeBootstrap?.configuration ?? null;
  const candidateConfiguration = {
    name: config.configurationName,
    sourceCellEndpoint: config.sourceCellEndpoint,
    persona: config.persona || null,
    skeleton,
    bootstrapConfiguration,
    workingReferences: beforeBootstrap?.editorState?.workingReferences ?? [],
  };

  await fs.writeFile(
    path.join(outputDir, "candidate.skeleton.json"),
    JSON.stringify(skeleton, null, 2),
    "utf8"
  );
  await fs.writeFile(
    path.join(outputDir, "candidate.cellconfiguration.json"),
    JSON.stringify(candidateConfiguration, null, 2),
    "utf8"
  );
  await fs.writeFile(
    path.join(outputDir, "before-after.diff"),
    makeJSONDiff(beforeSkeleton, skeleton),
    "utf8"
  );

  const desktopDom = await fs.readFile(path.join(firstViewportDir, `${firstViewport}.dom.txt`), "utf8").catch(() => "");
  const consolePayload = await readJSON(path.join(firstViewportDir, "console.json")).catch(() => ({}));
  await fs.writeFile(path.join(outputDir, "dom.txt"), desktopDom, "utf8");
  await fs.writeFile(path.join(outputDir, "console.json"), JSON.stringify(consolePayload.consoleMessages || [], null, 2), "utf8");
  await fs.writeFile(path.join(outputDir, "page-errors.json"), JSON.stringify(consolePayload.pageErrors || [], null, 2), "utf8");

  const notes = [
    `# Skeleton Runtime Review`,
    ``,
    `- Configuration: ${config.configurationName}`,
    `- Source cell: ${config.sourceCellEndpoint}`,
    `- Persona: ${config.persona || "live requester"}`,
    `- Mode: review preview, no runtime commit performed`,
    `- Generated: ${new Date().toISOString()}`,
    ``,
    `## Recommendation`,
    ``,
    `Keep this as a runtime variant until the screenshots and action checks are approved. Promote to Swift factory only in a separate task after reviewing candidate.skeleton.json, screenshots, and before-after.diff.`,
    ``,
    `## Artifacts`,
    ``,
    `- candidate.cellconfiguration.json`,
    `- candidate.skeleton.json`,
    `- before-after.diff`,
    `- ${runSummary.viewports.map((viewport) => `${viewport.name}/${viewport.name}.png`).join("\n- ")}`,
  ].join("\n");
  await fs.writeFile(path.join(outputDir, "promotion-notes.md"), notes, "utf8");
}

async function authenticateBrowserSession(context, config) {
  const loginResponse = await context.request.post(absoluteURL(config.baseURL, "/auth/login"), {
    data: { username: config.username, password: config.password },
    failOnStatusCode: false,
  });
  if (loginResponse.ok()) {
    return;
  }

  const shouldRegister = !config.usernameProvided && !config.passwordProvided && [400, 401, 404].includes(loginResponse.status());
  if (!shouldRegister) {
    throw new Error(`Authentication request to /auth/login failed with ${loginResponse.status()}: ${await loginResponse.text().catch(() => "")}`);
  }

  const registerResponse = await context.request.post(absoluteURL(config.baseURL, "/auth/register"), {
    data: { username: config.username, password: config.password },
    failOnStatusCode: false,
  });
  if (!registerResponse.ok()) {
    throw new Error(`Authentication request to /auth/register failed with ${registerResponse.status()}: ${await registerResponse.text().catch(() => "")}`);
  }
}

async function openPorthole(page, config) {
  const url = new URL("/porthole", config.baseURL);
  if (config.persona) {
    url.searchParams.set("conferencePersona", config.persona);
  }
  await page.goto(url.toString(), { waitUntil: "domcontentloaded" });
  await waitForPortholeReady(page, config.actionTimeoutMs);
  await waitForPortholeHydrationIdle(page);
}

async function reloadPorthole(page, config) {
  await page.reload({ waitUntil: "domcontentloaded" });
  await waitForPortholeReady(page, config.actionTimeoutMs);
  await waitForPortholeHydrationIdle(page);
}

async function waitForPortholeReady(page, timeoutMs = 15000) {
  await expect(page.getByRole("heading", { name: "Porthole" })).toBeVisible({ timeout: timeoutMs });
  await expect(page.locator("#porthole-skeleton-root")).toBeVisible({ timeout: timeoutMs });
}

async function waitForPortholeHydrationIdle(page) {
  await page.waitForLoadState("networkidle", { timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(250);
}

async function waitForOptionalPortholeActionResponse(page, timeoutMs = 5000) {
  return page.waitForResponse((response) => (
    response.url().includes("/browserhead/porthole/action") &&
    response.request().method() === "POST"
  ), { timeout: timeoutMs }).catch(() => null);
}

async function expectActiveConfiguration(page, configurationName) {
  await page.waitForFunction(
    (expectedName) => {
      const canvas = document.querySelector(".canvas");
      const activeName = canvas instanceof HTMLElement ? canvas.dataset.activeConfiguration : "";
      if (activeName === expectedName) {
        return true;
      }
      const label = document.querySelector(".active-configuration strong, .toolbar-navigation-current");
      return label && label.textContent && label.textContent.includes(expectedName);
    },
    configurationName,
    { timeout: 15000 }
  );
  const activeConfiguration = page.locator(".active-configuration, .toolbar-navigation-current").first();
  if (await activeConfiguration.count()) {
    await expect(activeConfiguration).not.toContainText(/\(laster/i, { timeout: 15000 });
  }
}

async function postAction(context, config, keypath, payload) {
  const response = await context.request.post(absoluteURL(config.baseURL, "/browserhead/porthole/action"), {
    data: { keypath, payload: payload ?? null },
    failOnStatusCode: false,
    timeout: config.actionTimeoutMs,
  });
  if (!response.ok()) {
    throw new Error(`Porthole action ${keypath} failed with ${response.status()}: ${await response.text().catch(() => "")}`);
  }
  return response.json();
}

async function requestBootstrap(context, config) {
  const response = await context.request.get(absoluteURL(config.baseURL, "/browserhead/porthole/bootstrap"), {
    failOnStatusCode: false,
    timeout: config.actionTimeoutMs,
  });
  if (!response.ok()) {
    throw new Error(`Porthole bootstrap failed with ${response.status()}: ${await response.text().catch(() => "")}`);
  }
  return response.json();
}

async function applyExpectations(page, expects = {}) {
  for (const entry of asArray(expects.text)) {
    await expect(page.getByText(toTextMatcher(entry)).first()).toBeVisible({ timeout: timeoutFor(entry) });
  }
  for (const entry of asArray(expects.notText)) {
    await expect(page.getByText(toTextMatcher(entry)).first()).toHaveCount(0, { timeout: timeoutFor(entry) });
  }
  for (const entry of asArray(expects.buttons)) {
    await expect(page.getByRole("button", { name: toTextMatcher(entry) }).first()).toBeVisible({ timeout: timeoutFor(entry) });
  }
  for (const entry of asArray(expects.inputs)) {
    await expect(page.getByPlaceholder(toTextMatcher(entry)).first()).toBeVisible({ timeout: timeoutFor(entry) });
  }
  for (const entry of asArray(expects.selectors)) {
    await expect(page.locator(selectorFor(entry)).first()).toBeVisible({ timeout: timeoutFor(entry) });
  }
  for (const entry of asArray(expects.listRows)) {
    const selector = selectorFor(entry);
    const min = typeof entry === "object" && Number.isFinite(entry.min) ? entry.min : 1;
    await expect(page.locator(selector)).toHaveCountGreaterThanOrEqual(min, { timeout: timeoutFor(entry) });
  }
}

async function expectNoConferenceCriticalLeaks(page, config) {
  const configurationName = String(config.configurationName || "");
  if (!configurationName.startsWith("Conference ") && !configurationName.startsWith("Arendalsuka ")) {
    return;
  }
  await expect(page.locator("body")).not.toContainText(
    /CellAuthorizationDecision|identity_public_key_mismatch|denied\(CellBase\.CellAuthorizationDecision|error:\s*denied|debugValidateAccessForEverything/i,
    { timeout: Number(config.actionTimeoutMs || 10000) }
  );
}

async function runActions(page, context, config, actions, actionResults = []) {
  for (const action of actions) {
    const type = String(action?.type || "").trim();
    if (!type) {
      continue;
    }
    if (type === "click") {
      const locator = locatorFromAction(page, action);
      const actionResponse = action.waitForAction === false
        ? Promise.resolve(null)
        : waitForOptionalPortholeActionResponse(page, Number(action.waitForActionTimeoutMs || 5000));
      if (action.dispatch === true) {
        await locator.dispatchEvent("click", {}, { timeout: timeoutFor(action) });
      } else {
        await locator.click({
          timeout: timeoutFor(action),
          force: Boolean(action.force),
        });
      }
      await actionResponse;
      await waitForPortholeHydrationIdle(page);
    } else if (type === "fill") {
      await locatorFromAction(page, action).fill(String(action.text ?? ""), { timeout: timeoutFor(action) });
    } else if (type === "press") {
      await locatorFromAction(page, action).press(String(action.key || "Enter"), { timeout: timeoutFor(action) });
    } else if (type === "postAction") {
      const keypath = String(action.keypath || "");
      const result = await postAction(context, config, keypath, action.payload ?? null);
      actionResults.push({
        type,
        keypath,
        payload: action.payload ?? null,
        result,
      });
      if (action.reload !== false) {
        await reloadPorthole(page, config);
      }
    } else if (type === "expectText" || type === "waitForText") {
      const matcher = toTextMatcher(action.text || action.name);
      const locator = action.selector
        ? page.locator(selectorFor(action)).getByText(matcher).first()
        : page.getByText(matcher).first();
      await expect(locator).toBeVisible({ timeout: timeoutFor(action) });
    } else if (type === "expectNoText" || type === "waitForNoText") {
      const matcher = toTextMatcher(action.text || action.name);
      const locator = action.selector
        ? page.locator(selectorFor(action)).getByText(matcher)
        : page.getByText(matcher);
      await expect(locator).toHaveCount(0, { timeout: timeoutFor(action) });
    } else if (type === "expectHiddenText" || type === "waitForHiddenText") {
      const matcher = toTextMatcher(action.text || action.name);
      await expectVisibleTextAbsent(page, action, matcher);
    } else if (type === "expectInput" || type === "waitForInput") {
      const matcher = toTextMatcher(action.placeholder || action.text || action.name);
      await expect(page.getByPlaceholder(matcher).first()).toBeVisible({ timeout: timeoutFor(action) });
    } else if (type === "wait") {
      await page.waitForTimeout(Number(action.ms || 500));
    } else {
      throw new Error(`Unsupported skeleton action type: ${type}`);
    }
  }
}

async function expectVisibleTextAbsent(page, action, matcher) {
  const selector = action.selector ? selectorFor(action) : "body";
  const matcherPayload = matcher instanceof RegExp
    ? { regex: matcher.source, flags: matcher.flags }
    : { text: String(matcher || "") };
  await page.waitForFunction(
    ({ selector, matcherPayload }) => {
      const roots = selector ? Array.from(document.querySelectorAll(selector)) : [document.body];
      if (roots.length === 0) {
        return true;
      }
      const matches = (value) => {
        if (matcherPayload.regex) {
          return new RegExp(matcherPayload.regex, matcherPayload.flags || "").test(value);
        }
        return String(value || "").includes(matcherPayload.text || "");
      };
      return roots.every((root) => matches(root.innerText || "") === false);
    },
    { selector, matcherPayload },
    { timeout: timeoutFor(action) }
  );
}

function locatorFromAction(page, action) {
  if (action.selector) {
    return page.locator(String(action.selector)).first();
  }
  if (action.placeholder) {
    return page.getByPlaceholder(toTextMatcher(action.placeholder)).first();
  }
  if (action.role) {
    return page.getByRole(String(action.role), { name: toTextMatcher(action.name || action.text || "") }).first();
  }
  if (action.button || action.name) {
    return page.getByRole("button", { name: toTextMatcher(action.button || action.name) }).first();
  }
  if (action.text) {
    return page.getByText(toTextMatcher(action.text)).first();
  }
  throw new Error(`Action requires selector, placeholder, role/name, button, or text: ${JSON.stringify(action)}`);
}

async function captureFailureArtifacts(page, outputDir, error, consoleMessages, pageErrors) {
  await fs.mkdir(outputDir, { recursive: true });
  await fs.writeFile(path.join(outputDir, "failure.txt"), String(error?.stack || error), "utf8");
  await fs.writeFile(path.join(outputDir, "console.json"), JSON.stringify({ consoleMessages, pageErrors }, null, 2), "utf8");
  await page.screenshot({ path: path.join(outputDir, "failure.png"), fullPage: true }).catch(() => {});
  await fs.writeFile(path.join(outputDir, "failure.dom.txt"), await page.locator("body").innerText().catch(() => ""), "utf8");
  await fs.writeFile(path.join(outputDir, "failure.html"), await page.content().catch(() => ""), "utf8");
}

function parseArgs(argv) {
  const args = { _: [] };
  const booleanFlags = new Set(["headed", "help", "ignoreHTTPSErrors"]);
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      args._.push(token);
      continue;
    }
    const withoutPrefix = token.slice(2);
    const equalsIndex = withoutPrefix.indexOf("=");
    const rawKey = equalsIndex >= 0 ? withoutPrefix.slice(0, equalsIndex) : withoutPrefix;
    const key = normalizeArgKey(rawKey);
    const inlineValue = equalsIndex >= 0 ? withoutPrefix.slice(equalsIndex + 1) : null;
    if (booleanFlags.has(key) && inlineValue === null) {
      args[key] = true;
      continue;
    }
    const value = inlineValue ?? argv[index + 1];
    if (inlineValue === null) {
      index += 1;
    }
    if (args[key] === undefined) {
      args[key] = value;
    } else if (Array.isArray(args[key])) {
      args[key].push(value);
    } else {
      args[key] = [args[key], value];
    }
  }
  if (args.help) {
    printHelpAndExit();
  }
  return args;
}

function normalizeArgKey(key) {
  const aliases = {
    "action-timeout-ms": "actionTimeoutMs",
    "base-url": "baseURL",
    "configuration-name": "configurationName",
    "expect-button": "expectButton",
    "export-dir": "exportDir",
    "expect-text": "expectText",
    "ignore-http-errors": "ignoreHTTPSErrors",
    "output-dir": "outputDir",
    "skeleton-file": "skeletonFile",
    "skeleton-source": "skeletonSource",
    "source-cell-endpoint": "sourceCellEndpoint",
  };
  return aliases[key] || key;
}

async function loadScenario(args) {
  if (!args.scenario) {
    return {};
  }
  const scenarioPath = path.resolve(String(args.scenario));
  const scenario = await readJSON(scenarioPath);
  scenario.__scenarioPath = scenarioPath;
  scenario.__scenarioDir = path.dirname(scenarioPath);
  return scenario;
}

function normalizeConfig(scenario, args) {
  const mode = String(args.mode || scenario.mode || "preview");
  if (!allowedModes.has(mode)) {
    throw new Error(`Unsupported mode '${mode}'. Expected one of: ${Array.from(allowedModes).join(", ")}`);
  }
  const baseURL = String(args.baseURL || scenario.baseURL || defaultBaseURL);
  const configurationName = String(args.configurationName || scenario.configurationName || "");
  const sourceCellEndpoint = String(args.sourceCellEndpoint || scenario.sourceCellEndpoint || "");
  const skeletonFile = String(args.skeletonFile || scenario.skeletonFile || "");
  const skeletonSource = String(args.skeletonSource || scenario.skeletonSource || (skeletonFile ? "file" : ""));
  const supportsActiveSkeleton = skeletonSource === "active-configuration";
  const readOnlyMode = mode === "export" || mode === "view-smoke";
  if (!configurationName || !sourceCellEndpoint || (!readOnlyMode && !skeletonFile && !supportsActiveSkeleton)) {
    throw new Error("configurationName and sourceCellEndpoint are required. Preview/commit also requires skeletonFile or skeletonSource=active-configuration.");
  }
  if (mode === "export" && (skeletonFile || supportsActiveSkeleton)) {
    throw new Error("export reads the live configuration and takes no skeletonFile or skeletonSource.");
  }
  if (skeletonSource && skeletonSource !== "file" && supportsActiveSkeleton === false) {
    throw new Error(`Unsupported skeletonSource '${skeletonSource}'. Expected file or active-configuration.`);
  }
  if (supportsActiveSkeleton && mode !== "commit-runtime") {
    throw new Error("skeletonSource=active-configuration is reserved for commit-runtime probes.");
  }

  const scenarioDir = scenario.__scenarioDir || process.cwd();
  const skeletonPath = skeletonFile ? path.resolve(scenarioDir, skeletonFile) : null;
  const scenarioName = path.basename(scenario.__scenarioPath || configurationName).replace(/\.[^.]+$/, "");
  const outputDir = path.resolve(
    String(args.outputDir || scenario.outputDir || path.join("test-results", "skeleton-iterate", `${sanitizeName(scenarioName)}-${timestampSlug()}`))
  );
  return {
    mode,
    baseURL,
    persona: args.persona || scenario.persona || "",
    configurationName,
    sourceCellEndpoint,
    skeletonSource: skeletonSource || "none",
    skeletonPath,
    runtimeProbeStyleClasses: normalizeRuntimeProbeStyleClasses(scenario.runtimeProbeStyleClasses),
    exportDir: (args.exportDir || scenario.exportDir)
      ? path.resolve(scenarioDir, String(args.exportDir || scenario.exportDir))
      : null,
    // export writes one bundle, so a second viewport would only overwrite it.
    viewports: mode === "export"
      ? normalizeViewports(args.viewports || scenario.viewports).slice(0, 1)
      : normalizeViewports(args.viewports || scenario.viewports),
    expects: mergeExpectations(scenario.expects || {}, args),
    actions: scenario.actions || [],
    notificationChecks: scenario.notificationChecks || [],
    outputDir,
    headed: booleanValue(args.headed ?? scenario.headed, false),
    ignoreHTTPSErrors: booleanValue(args.ignoreHTTPSErrors ?? scenario.ignoreHTTPSErrors, false),
    username: String(args.username || scenario.username || defaultUsername),
    password: String(args.password || scenario.password || defaultPassword),
    usernameProvided: Boolean(args.username || scenario.username || process.env.CONFERENCE_DEMO_USERNAME),
    passwordProvided: Boolean(args.password || scenario.password || process.env.CONFERENCE_DEMO_PASSWORD),
    actionTimeoutMs: Number(args.actionTimeoutMs || scenario.actionTimeoutMs || 15000),
  };
}

function normalizeRuntimeProbeStyleClasses(raw) {
  const values = asArray(raw).map((entry) => String(entry || "").trim()).filter(Boolean);
  if (values.length === 0) {
    return ["runtime-commit-probe-a", "runtime-commit-probe-b"];
  }
  if (values.length !== 2 || values[0] === values[1]) {
    throw new Error("runtimeProbeStyleClasses must contain two distinct class names.");
  }
  return values;
}

function mergeExpectations(expects, args) {
  const merged = { ...expects };
  if (args.expectText) {
    merged.text = [...asArray(merged.text), ...asArray(args.expectText)];
  }
  if (args.expectButton) {
    merged.buttons = [...asArray(merged.buttons), ...asArray(args.expectButton)];
  }
  return merged;
}

function normalizeViewports(raw) {
  if (!raw) {
    return defaultViewports;
  }
  if (Array.isArray(raw)) {
    return raw.map(normalizeViewport);
  }
  return String(raw)
    .split(",")
    .map((entry) => entry.trim())
    .filter(Boolean)
    .map((entry) => {
      if (entry === "desktop") {
        return defaultViewports[0];
      }
      if (entry === "mobile") {
        return defaultViewports[1];
      }
      const match = entry.match(/^([^:]+):(\d+)x(\d+)$/);
      if (!match) {
        throw new Error(`Invalid viewport '${entry}'. Use desktop,mobile or name:WIDTHxHEIGHT.`);
      }
      return { name: match[1], width: Number(match[2]), height: Number(match[3]) };
    });
}

function normalizeViewport(viewport) {
  if (!viewport || typeof viewport !== "object") {
    throw new Error(`Invalid viewport entry: ${JSON.stringify(viewport)}`);
  }
  const width = Number(viewport.width);
  const height = Number(viewport.height);
  if (!Number.isFinite(width) || !Number.isFinite(height)) {
    throw new Error(`Viewport requires numeric width and height: ${JSON.stringify(viewport)}`);
  }
  return {
    name: String(viewport.name || `${width}x${height}`),
    width,
    height,
  };
}

async function prepareOutputDir(config) {
  await fs.mkdir(config.outputDir, { recursive: true });
  await fs.writeFile(
    path.join(config.outputDir, "input.json"),
    JSON.stringify({
      mode: config.mode,
      baseURL: config.baseURL,
      persona: config.persona || null,
      configurationName: config.configurationName,
      sourceCellEndpoint: config.sourceCellEndpoint,
      skeletonSource: config.skeletonSource,
      skeletonPath: config.skeletonPath,
      runtimeProbeStyleClasses: config.runtimeProbeStyleClasses,
      viewports: config.viewports,
      expects: config.expects,
      actions: config.actions,
      notificationChecks: config.notificationChecks,
    }, null, 2),
    "utf8"
  );
  return config.outputDir;
}

function toTextMatcher(value) {
  if (value && typeof value === "object" && value.regex) {
    return new RegExp(value.regex, value.flags || "");
  }
  return String(value || "");
}

function selectorFor(value) {
  if (value && typeof value === "object") {
    return String(value.selector || value.css || "");
  }
  return String(value || "");
}

function timeoutFor(value) {
  if (value && typeof value === "object" && Number.isFinite(value.timeoutMs)) {
    return Number(value.timeoutMs);
  }
  return 12000;
}

function asArray(value) {
  if (value === undefined || value === null) {
    return [];
  }
  return Array.isArray(value) ? value : [value];
}

function booleanValue(value, fallback) {
  if (value === undefined || value === null || value === "") {
    return fallback;
  }
  if (typeof value === "boolean") {
    return value;
  }
  const normalized = String(value).trim().toLowerCase();
  if (["1", "true", "yes", "on"].includes(normalized)) {
    return true;
  }
  if (["0", "false", "no", "off"].includes(normalized)) {
    return false;
  }
  return fallback;
}

async function readJSON(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

function absoluteURL(baseURL, urlPath) {
  return new URL(urlPath, baseURL).toString();
}

function sanitizeName(value) {
  return String(value || "skeleton")
    .toLowerCase()
    .replace(/[^a-z0-9._-]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80) || "skeleton";
}

function timestampSlug() {
  return new Date().toISOString().replace(/[:.]/g, "-");
}

function makeJSONDiff(before, after) {
  const beforeLines = JSON.stringify(before, null, 2).split("\n");
  const afterLines = JSON.stringify(after, null, 2).split("\n");
  const hash = crypto
    .createHash("sha256")
    .update(JSON.stringify({ before, after }))
    .digest("hex")
    .slice(0, 12);
  return [
    `--- committed.skeleton.json`,
    `+++ candidate.skeleton.json`,
    `@@ skeleton-preview ${hash} @@`,
    ...beforeLines.map((line) => `- ${line}`),
    ...afterLines.map((line) => `+ ${line}`),
    "",
  ].join("\n");
}

function printHelpAndExit() {
  console.log(`Usage:
  npm run skeleton:iterate -- --scenario playwright/skeleton-scenarios/conference-participant-chat.preview.json
  npm run skeleton:iterate -- --mode preview --configurationName "Conference Participant Chat" --sourceCellEndpoint cell:///ConferenceChatLaunch --skeletonFile ./candidate.json
  npm run skeleton:iterate -- --scenario playwright/skeleton-scenarios/arendalsuka-participant-program.commit-runtime.json
  npm run skeleton:iterate -- --mode export --configuration-name "Arendalsuka Participant Program" --source-cell-endpoint cell:///ArendalsukaConfigurationPublisher --export-dir ./_skeleton-work

Modes:
  export         Read the live active CellConfiguration and skeleton to files. Read-only: never enters edit mode and never discards working state.
  preview        Render a candidate skeleton in a throwaway working state.
  commit-runtime Persist a candidate skeleton on the source cell (requires rw-s Agreement).
  review         Produce a promotion bundle for a Swift factory decision.
  view-smoke     Assert the committed surface without touching the editor.

Flags:
  CamelCase and common kebab-case aliases are accepted, e.g. --baseURL and --base-url.

Credentials:
  Use CONFERENCE_DEMO_USERNAME / CONFERENCE_DEMO_PASSWORD or --username / --password for an existing host.
  If no credentials are provided, the script generates a one-off requester and attempts self-registration.

Modes:
  preview         Set working skeleton in edit mode and test without applying.
  commit-runtime  Apply source-backed runtime override and verify reload in a new session.
  review          Preview and write review bundle artifacts.
  view-smoke      Load the committed/factory configuration in view mode and verify user-facing UI only.
`);
  process.exit(0);
}

expect.extend({
  async toHaveCountGreaterThanOrEqual(locator, expected, options = {}) {
    const timeout = options.timeout ?? options.timeoutMs ?? 12000;
    const startedAt = Date.now();
    let count = 0;
    while (Date.now() - startedAt < timeout) {
      count = await locator.count();
      if (count >= expected) {
        return {
          pass: true,
          message: () => `expected locator count ${count} not to be >= ${expected}`,
        };
      }
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
    return {
      pass: false,
      message: () => `expected locator count to be >= ${expected}, received ${count}`,
    };
  },
});

main().catch((error) => {
  console.error(error?.stack || error);
  process.exit(1);
});
