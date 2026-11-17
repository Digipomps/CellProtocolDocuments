# Document CI failure audit — 2026-09-17

The current main failure is loss of an image during a document editor remount. The existing `bfc55ee0219d34360d9b9314624251e2cdda38db` fix on `origin/codex/entity-fabric-20260911` addresses the concrete mechanism. Do not increase the live assertion timeout or remove the large-image proof.

## Evidence

- Source: CellScaffold `b4a2779a`; failed run `35186146958`, job `105088525347`.
- `../ci-artifacts/main-job.log:113713–113734`: live proof fails at `playwright/rich-document-live.spec.js:40`, expecting exactly one image in session B within 30 seconds; actual count is zero. Earlier save-status and bidirectional text assertions passed. This is different from the older September 11 save-status failure described in `ROTAARSAK_DOKUMENTLOOP.md`.
- `../ci-artifacts/document-proof/rich-document-live-live-Po-baada-session-and-reload-persists/error-context.md`: B has both text markers and “Alle endringer er lagret i dokumentcellen”, but no image.
- The matching `trace.zip` contains 14 `Dokument` bootstrap responses: seven per browser. All 14 have identical skeleton values and array order; all 14 have different JSON object field ordering. Canonical JSON SHA-256 prefix is `b72cc38bd6` for every skeleton/name pair. Each successive bootstrap therefore changes the existing `JSON.stringify` renderer signature even though its layout is unchanged.
- Session A's recorded action requests comprise configuration load, two text deltas, and presence; there is no image delta action request at all. Session B's text deltas are accepted/duplicated normally. No JavaScript exception appears in the trace; console errors are missing optional theme stylesheets.
- In session A, `setInputFiles` spans monotonic `11007.839–11346.121` ms. Using its trace context clock (`wallTime=1789625613024`, `monotonicTime=2446.893`), this is approximately `06:13:41.585–41.923Z`. A bootstrap starting `06:13:41.095Z` takes `765.9` ms and completes within that interval. Its semantically identical skeleton has another different raw signature.

## Mechanism and minimal correction

`Public/js/porthole-webo.js:8167–8169` on main uses raw `JSON.stringify({ currentConfigurationName, renderedSkeleton })` to decide whether to replace a renderer. Swift's JSON object order is not stable. A bootstrap caused by document Flow can therefore destroy and replace the editor despite no layout change.

`Public/js/haven-rich-document.js:232–237` asynchronously reads the selected image with `FileReader`. If the editor is replaced while that read is pending, its callback inserts into the detached Quill instance. The old controller has `disposed=true`; its `pump` refuses to send the image. The visible replacement restores only committed content. The trace proves the signature churn, exact overlap and absent image request; the pre-existing deterministic browser regression isolates the pending-read/remount mechanism.

The minimal production fix already exists in commit `bfc55ee0`: `skeletonRenderSignature` sorts object keys recursively but leaves arrays ordered. `renderSkeletonCanvas` uses that signature. It also includes `playwright/porthole-skeleton-atomic-swap.spec.js` regression `reordered JSON object fields preserve a document and its pending image read`. The regression delays a real FileReader, refreshes the real Porthole shell with reordered object fields, checks editor DOM identity, resumes the image read, and requires one saved image mutation. The existing live test remains strict.

## Existing changes and candidate conflict resolution

- Main already contains `6c391437` (#244), equivalent to `a5ac0ab1` in the document-proof worktree: coalescing unsent typing plus the explicit 30-second save assertion. Reapplying that commit alone cannot repair today's failure.
- In the candidate merge, `Public/js/haven-rich-document.js` conflicts only between basic coalescing and entity-fabric's enhanced coalescing. Keep the entity-fabric side: it preserves sent envelopes, composes unsent tails, discards empty net changes after cancellation, and computes saved status from queue length. Its two additional browser tests cover delayed acknowledgement and cancelled unsent typing. The JSON-order correction is in `porthole-webo.js`, which merges without conflict.
- In `ci/test-filter.txt`, keep `PersonalCopilotWidgetCanvasTests` and all six entity test classes. Preserve a separate `---` test group boundary for the entity slice.
- Main's workflow static browser gate runs `rich-document.spec.js` but not `porthole-skeleton-atomic-swap.spec.js`. The integrated candidate already adds the latter to that exact invocation. Preserve this workflow change so the causal regression is required in future CI.

## Read-only verification performed

An in-memory Node check evaluated the exact `skeletonRenderSignature` implementation from `bfc55ee0` against all 14 bootstrap skeleton/name pairs extracted directly from the failing trace. It passed: 14 raw signatures become one stable signature. Separate assertions passed that changing array order and changing values still change the signature. No source, Git metadata, builds, dependency installs, network retries or live server state were modified by this audit.

The existing branch documentation records a prior red/green browser regression, but this audit did not rerun that browser test or the live server proof. Main and candidate live completion remain unverified until the root runs them.

## Required integration verification

1. Run both static browser suites together: `playwright/rich-document.spec.js` and `playwright/porthole-skeleton-atomic-swap.spec.js`. Keep coalescing, cancellation, persistence uncertainty, document switching, lost acknowledgement, malformed skeleton update and pending image read tests.
2. Run the original `playwright/rich-document-live.spec.js` unchanged against the built integrated candidate: initial load, typed save, bidirectional text, malformed websocket reply, image larger than 1 MiB base64 reaching the peer, help/chat, reload persistence, post-reload messaging, DOCX download and outsider websocket denial.
3. Keep the exact CI invocation and 30-second image assertion; a green static suite does not establish the live server proof.

`proposed-document-fix.patch` contains the existing `bfc55ee0` source/test correction for review or selective application. `proposed-ci-regression-gate.patch` adds the causal regression suite to CI relative to main. Both changes are present in the integrated entity candidate; do not apply them a second time.
