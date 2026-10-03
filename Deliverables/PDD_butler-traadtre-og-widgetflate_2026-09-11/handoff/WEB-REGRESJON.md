STATUS: LEVERT — reprodusert og sammenliknet

# Web-regresjonene fra CI — reprodusert

Skrevet av `HAVEN-Deploy/_handoff/WP-R/wp-web-regresjon.sh` 2026-09-22T09:03:23Z. Bevis: `evidence/web-regresjon/`.

## Hva runden endret i web-laget

```text
 Public/css/porthole-webo.css        |  62 ++-
 Public/css/themes/Co-Pilot Chat.css |  44 +++
 Public/js/porthole-webo.js          |  88 ++++-
 Public/js/skeleton-runtime.js       | 734 ++++++++++++++++++++++++++++++++++--
 4 files changed, 884 insertions(+), 44 deletions(-)
```

### Lytterne i `createRenderer` — linjene rundt dem, foer og naa

```text
--- paa main:
--- paa grenen:
318-    };
319-    // One transient drag context per host, shared by mounted definitions.
320-    if (!options.dragContext) {
321-      document.addEventListener("dragstart", state.beginExternalDrag);
322-      document.addEventListener("dragend", state.cancelDrag);
323-      document.addEventListener("drop", state.cancelDrag);
324:      document.addEventListener("keydown", state.cancelDrag);
325-    }
326-    updateLayoutContext(state);
```

## `porthole-skeleton-atomic-swap.spec.js` lokalt

exit 1.

```text
      Object {
    -   "added": 0,
    -   "removed": 0,
    +   "added": 1,
    +   "removed": 1,
      }

      245 |   await expect(page.locator("#porthole-skeleton-validation-error")).toContainText("forced candidate update failure");
      246 |   const balance = await page.evaluate(() => window.__listenerBalance);
    > 247 |   expect(balance).toEqual({ added: 0, removed: 0 });
          |                   ^
      248 |
      249 |   await page.evaluate(() => {
      250 |     window.HavenSkeletonRuntime.createRenderer = window.__originalCreateRenderer;
        at /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/porthole-skeleton-atomic-swap.spec.js:247:19

    attachment #1: screenshot (image/png) ──────────────────────────────────────────────────────────
    test-results/playwright/porthole-skeleton-atomic-s-b2808-activating-global-listeners/test-failed-1.png
    ────────────────────────────────────────────────────────────────────────────────────────────────

    attachment #2: video (video/webm) ──────────────────────────────────────────────────────────────
    test-results/playwright/porthole-skeleton-atomic-s-b2808-activating-global-listeners/video.webm
    ────────────────────────────────────────────────────────────────────────────────────────────────

    Error Context: test-results/playwright/porthole-skeleton-atomic-s-b2808-activating-global-listeners/error-context.md

    attachment #4: trace (application/zip) ─────────────────────────────────────────────────────────
    test-results/playwright/porthole-skeleton-atomic-s-b2808-activating-global-listeners/trace.zip
    Usage:

        npx playwright show-trace test-results/playwright/porthole-skeleton-atomic-s-b2808-activating-global-listeners/trace.zip

    ────────────────────────────────────────────────────────────────────────────────────────────────


[1A[2K[4/5] playwright/porthole-skeleton-atomic-swap.spec.js:256:1 › Porthole rejects malformed action editor state without replacing the rendered node
[1A[2K[5/5] playwright/porthole-skeleton-atomic-swap.spec.js:312:1 › Porthole exposes typed source write failure and keeps the working surface
[1A[2K  1 failed
    playwright/porthole-skeleton-atomic-swap.spec.js:176:1 › Porthole rejects an uncommitted renderer without activating global listeners 
  4 passed (2.6s)
```

## Samme spec mot main-versjonen av de to JS-filene

exit 0. (Filene er lagt tilbake; sporede endringer etterpaa: 0.)

```text

Running 5 tests using 1 worker

[1A[2K[1/5] playwright/porthole-skeleton-atomic-swap.spec.js:35:1 › reordered JSON object fields preserve a document and its pending image read
[1A[2K[2/5] playwright/porthole-skeleton-atomic-swap.spec.js:91:1 › Porthole retains the rendered node when a refreshed skeleton is malformed
[1A[2K[3/5] playwright/porthole-skeleton-atomic-swap.spec.js:176:1 › Porthole rejects an uncommitted renderer without activating global listeners
[1A[2K[4/5] playwright/porthole-skeleton-atomic-swap.spec.js:256:1 › Porthole rejects malformed action editor state without replacing the rendered node
[1A[2K[5/5] playwright/porthole-skeleton-atomic-swap.spec.js:312:1 › Porthole exposes typed source write failure and keeps the working surface
[1A[2K  5 passed (1.6s)
```

**Konklusjon: regresjonen er innfoert i denne runden** — spec-en er groenn med main-versjonen av de to filene og roed med vaar.
