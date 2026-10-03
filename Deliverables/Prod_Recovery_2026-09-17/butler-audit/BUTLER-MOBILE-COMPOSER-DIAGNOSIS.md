# Mobile composer viewport diagnosis

2026-09-18. Read-only inspection of candidate source, supplied failure log and supplied screenshot. No source edits, builds, browser actions or tests executed.

## Confirmed failure

`logs/live-ui-final-2.log` records `playwright/butler-explicit-helper-placement.spec.js:53`: `beforeMetrics.composerInsideViewport` is false for 375 × 812. The screenshot shows toolbar, the truthful “Ingen modell er koblet til” banner, conversation tabs, then Butler conversation; the textarea extends below the viewport. This is not a missing element: Playwright's `toBeVisible()` accepts rendered elements outside the viewport.

The screenshot was inspected before the running root verification replaced the `test-results` directory. Position estimates below are visual estimates, not captured DOM metrics.

## Causal chain

- `Public/css/porthole-webo.css:4193` sets mobile conversation height to `clamp(500px, calc(100svh - 170px), 760px)`. At 812 px this is 642 px regardless of toolbar/banner/tab height.
- The screenshot conversation starts approximately 315 px below viewport top, so this rule places its bottom around 957 px. The outer shell has only `min-height:100vh` (`:56`), not a bounded viewport layout; the canvas also has `min-height:520px` (`:763`). There is no ancestor forcing the conversation to shrink into the remaining viewport.
- `.style-role-chat-composer-dock` (`:3821`) is sticky at the bottom of its containing layout/scroll context, not fixed to the visible viewport. It cannot compensate for its conversation extending below the viewport.
- `updateAssistantDegradationFromResult` (`Public/js/porthole-webo.js:2462`) creates the banner after a local-rules prompt response. `runAction` (`:1110`) then renders shell chrome around the mounted skeleton. `renderShell` places the banner before the canvas (`:5150`), shifting the conversation downward without reducing its fixed height.
- `renderSkeletonCanvas` (`:8215`) updates state but does not measure the conversation's remaining viewport height. The `window.resize` handler (`:225`) adjusts compact menus/editor panels only. There is no relevant ResizeObserver/visualViewport sizing path in the inspected JS.
- The test fills and clicks Send before waiting for two prompt rows. That click may scroll the composer into view before the response; the subsequent banner/chrome replacement changes geometry. Thus a previous pass does not demonstrate that the final post-response layout was intrinsically bounded. The specific reason the previous run passed was not independently established.
- The helper rail is closed in the failing screenshot. Its narrow-screen absolute overlay rule is not the immediate cause of this failure.

## Smallest targeted correction

Use the actual visible conversation top and available viewport bottom to size the conversation, scoped to the Butler product conversation. One practical small patch is a coalesced layout callback invoked after `renderSkeletonCanvas` finishes updating DOM, on window resize, and on `visualViewport.resize`. Compute viewport bottom from `visualViewport.offsetTop + visualViewport.height` when available, otherwise `innerHeight`; subtract the conversation bounding rect top and a small bottom gutter, then publish a CSS variable consumed by the scoped conversation-height rule.

The measured mobile rule must not retain the 500 px minimum, since the screenshot has less than 500 px remaining. Avoid a fixed extra subtraction for the current banner: wrapping, menu expansion, locale, and keyboard sizes change the occupied space. Keep the truthful banner visible.

A pure CSS bounded flex/grid ancestor chain would also solve this, but must carry `min-height:0` and the remaining-height constraint through canvas, skeleton host, tabs/panel, helper layout/chat wrapper and conversation; merely changing the outer shell height leaves the explicit conversation height overflowing. It is a broader patch than measuring the existing visible conversation.

At smaller heights, review `.style-role-chat-conversation > .skeleton-section-content` (`:3649`): its `minmax(140px,1fr)` row plus minimum-content dock can exceed the measured available space. Use an appropriately scoped `minmax(0,1fr) auto` layout and ensure the dock's optional starter/help/pinned content has a scrolling home if it cannot fit. Preserve both a usable composer and a usable log; clipping the dock is not a solution.

Do not fix this by adding `scrollIntoView` to the smoke or hiding the no-model banner. Preserve the mounted DOM and current reader scroll position. Avoid resetting the prompt log to the end on viewport/chrome changes.

## Focused verification recommendation

Extend the current 375 × 812 proof to assert the banner exists after the synthetic local-rules reply, then wait for stable layout via a bounded `expect.poll` and verify both textarea and Send bounds lie inside the viewport. Capture numeric rectangles and `window.scrollY`, prompt-scroll dimensions, conversation height, toolbar/banner bounds and visualViewport height/offset in the failure artifact. The existing test currently loses these details by asserting before attaching `beforeMetrics`.

Cover banner absent → present → removed, toolbar shown/hidden, helper open/close, and resize after response. Keep horizontal-overflow assertions and the existing mid-log reading-position regression. Check a short viewport/visual-viewport resize if implementing keyboard handling. A static test with the conversation at document top (`playwright/chat-conversation-layout.spec.js`) cannot catch the real shell/banner offset.

No new test result is claimed by this diagnosis.
