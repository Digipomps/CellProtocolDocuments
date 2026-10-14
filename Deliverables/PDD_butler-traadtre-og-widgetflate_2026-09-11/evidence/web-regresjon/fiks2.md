Runtime-rot: `/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/tmp.RYBN6hUmgo` (midlertidig). Binaerer fra `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/.build/out/Products/Debug`.

Testverten svarer: `{"app_revision":"dbf6667df3c2f35da9d8fb606f1e9757ec80dd5a","dimymicropayments_revision":"836ba8e6d71663d78836e2ec67a1e6f38bd8655b","environment":"testing","dimymint_revision":"af41630bbc01cece2a26f300`

## `butler-explicit-helper-placement.spec.js` lokalt

exit 1.

```text

      52 |       const beforeMetrics = await visibleLayoutMetrics(page, composer, assistantBubble);
      53 |       await testInfo.attach(`${viewport.id}-viewport-metrics`, { body: JSON.stringify(beforeMetrics), contentType: "application/json" });
    > 54 |       expect(beforeMetrics.composerInsideViewport).toBe(true);
         |                                                    ^
      55 |       const sendBox = await page.getByRole("button", { name: /^(Finn forslag|Send)$/ }).first().boundingBox();
      56 |       expect(sendBox.y + sendBox.height).toBeLessThanOrEqual(viewport.height + 1);
      57 |       expect(beforeMetrics.responseInsideDocument).toBe(true);
        at /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/butler-explicit-helper-placement.spec.js:54:52

    attachment #1: desktop-assistant-response (text/plain) ─────────────────────────────────────────
    B
    Butler
    11:10
    Jeg har fanget idéen med konteksten fra samtalen. Den lagres når du bekrefter.
    Forslag klart
    Lokal tolkning (fallback)
    Lagre idé
    Avvis
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #3: screenshot (image/png) ──────────────────────────────────────────────────────────
    test-results/playwright/butler-explicit-helper-pla-5fbb2-l-the-user-opens-one-helper/test-failed-1.png
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #4: video (video/webm) ──────────────────────────────────────────────────────────────
    test-results/playwright/butler-explicit-helper-pla-5fbb2-l-the-user-opens-one-helper/video.webm
    ────────────────────────────────────────────────────────────────────────────────────────────────

    Error Context: test-results/playwright/butler-explicit-helper-pla-5fbb2-l-the-user-opens-one-helper/error-context.md

    attachment #6: trace (application/zip) ─────────────────────────────────────────────────────────
    test-results/playwright/butler-explicit-helper-pla-5fbb2-l-the-user-opens-one-helper/trace.zip
    Usage:

        npx playwright show-trace test-results/playwright/butler-explicit-helper-pla-5fbb2-l-the-user-opens-one-helper/trace.zip

    ────────────────────────────────────────────────────────────────────────────────────────────────


[1A[2K[2/3] playwright/butler-explicit-helper-placement.spec.js:16:5 › Butler explicit helper placement › mobile-375 keeps the response in chat until the user opens one helper
[1A[2K[3/3] playwright/butler-explicit-helper-placement.spec.js:117:1 › unapproved external model is selectable and blocked without consent
[1A[2K  1 failed
    playwright/butler-explicit-helper-placement.spec.js:16:5 › Butler explicit helper placement › desktop keeps the response in chat until the user opens one helper 
  2 did not run
```

## Maal fra spec-en

```text
```

Bilder lagt i `evidence/web-regresjon/plassering/`: 1 stk.
