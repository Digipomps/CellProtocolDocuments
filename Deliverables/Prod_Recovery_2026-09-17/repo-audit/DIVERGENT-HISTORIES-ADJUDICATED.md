# Divergent histories and independent release packages — 2026-09-17

The 39 previously unresolved non-CellScaffold refs now map to **11 unique packages**: 25 refs already represented in main, 9 superseded or developer/archive-only refs, and 5 refs carrying the same unfinished Nearby Signals prototype. No divergent-history package supplies a demonstrated missing production Butler chat dependency.

This conclusion comes from source/tree/patch comparison, not branch age or closed-PR decisions. `divergent-adjudication.tsv` contains every one of the 39 refs and its package/decision. `divergent-adjudication.json` records source evidence and exact reviewed main SHAs. Raw supporting comparisons also live in `divergent-tree-evidence.json`, `divergent-patch-evidence.json`, and `sentinel-stash-crossrepo-evidence.json`.

Read-only audit: no tests, builds, fetches, source edits, Git writes, production inspection, or release actions. Root fetched Sprout; its current reviewed origin/main is `d5a70f3`. These decisions do not certify a deployed binary.

## The 39 refs, grouped by actual product content

| Unique package / old tips | Target | Decision and source evidence | Remaining integration chain |
|---|---|---|---|
| Binding historic product: `1e2d7cae`, `1cbd87b2`, `63ee4cf1` — 8 refs | Binding/main | **Already.** All tips are ancestors of old `c72bab2c`. `git diff c72bab2c 97a3fef9` shows only Xcode userdata, the docs submodule entry, and generated `out/Binding-live.app` removal. Product source is identical at the clean-main replacement. `63ee4cf1` is additionally patch-identical to main `7adb146a`. | None. Keep current main's later MCP/provisioning/security changes. |
| Binding breakpoint stashes `68aac40c`, `158a5a91` — 4 refs | Binding | **Superseded developer state.** Their first-parent stash deltas change only `xcuserdata/.../Breakpoints_v2.xcbkptlist`, not source. | None for a product release. Preserve the refs. |
| Network sentinel stash `f4bf2926` plus third parent `9d3d00af` — 2 refs | HavenAgentD/main | **Superseded by implemented source.** Three tracked registry/bridge changes and five untracked Swift files are implemented and extended at Binding `8a1befcc`, then in canonical HavenAgentD. Current registry creates NetworkSentinelCell and bridge exposes health/control. The newer implementation adds public counters, native interface enumeration, purpose-gated notices, richer tab/probe/capture state. | None from this stash. Release current HavenAgentD through its own native packaging path. Untracked Stripe skill resources in the stash are tooling, not app runtime. |
| Nearby Signals stash `7f9f3643` and branch `22e0a3d6` — 5 refs | Binding/main | **Unready, genuinely absent.** This is one prototype package, not five missing features. See detailed assessment below. | Rehabilitate missing `fc7d9d9a` + `22e0a3d6` product behavior against current main; do not wholesale merge the old branch. |
| Standalone extraction `f17cdcfa` — 1 ref in Binding | HavenAgentD/main | **Already, different repository owner.** The same f17 object exists in HavenAgentD and is an ancestor of `2aa9fa9d`; the complete `2aa9fa9d` tree exactly equals main `3420c81`. Restoring the extracted repository inside Binding would duplicate ownership. | None. Keep standalone HavenAgentD. |
| All five CP divergent tips: `858202b4`, `145e3997`, `e6b4c9cc`, `afdd427f`, `fe601a0b` — 5 refs | CellProtocol/main | **Already migrated.** Every tip is an ancestor of old `afdd427f`. `git diff afdd427f 49bdd59` has only deletion of an empty `.codex_identity_link_crypto_probe` plus CODEOWNERS/MAINTAINERS additions. There is no product source difference. | None. Do not resurrect historical storage names/debug helpers over current runtime. |
| Docs history: `54743ace`, `210d2f31`, `fe67d652`, `a4d8ab4e` — 7 refs | CellProtocolDocuments/main | **Already.** The older tips are ancestors of `210d2f31`; its entire tree is identical to main `42372c7b`, the canonical documentation snapshot. | None. |
| Docs stash `b01e9714` — 1 ref | CellProtocolDocuments/main | **Already.** Seven example/default lines change `publishersws` to `bridgehead`; all seven are present on main in Book 06, 08, and 10. | None. |
| Docs design package `73bdf529` — 1 ref | CellProtocolDocuments | **Delivered guides / archive remainder.** All five Deliverables design guides have exactly matching blobs in main. The 76 remaining additions are historical Artifacts screenshots/text/render helpers, not production functionality. Their contents remain preserved in Git; screenshots and personal records were not inspected. | Optional historic evidence archival only; no runtime integration. |
| AgentD auth/preflight: `66ff4972`, `2aa9fa9d` — 4 refs | HavenAgentD/main | **Already.** `66ff4972` has the same complete tree as `ebf62406`, which is ancestor of `2aa9fa9d`; the complete `2aa9fa9d` tree equals main `3420c81`. | None. |
| AgentD CI variant `fa161205` with `f155c138`, `baee272e`, `f51f21c7` — 2 refs | HavenAgentD/main | **Superseded CI strategy.** Current workflow keeps macOS 26, Xcode 26.3, Swift/Xcode major checks and scoped Sprout SSH auth. Main `69969e6` replaces local checkout pin routing with authoritative remote dependencies; current main additionally verifies every pin is on that dependency's own main. | None. Preserve current workflow and pins. |

### The genuinely missing Nearby Signals prototype

The smallest historic feature chain is `fc7d9d9a Add nearby signals personal copilot surface` followed by `22e0a3d6 Fix local nearby signals surface loading`. Its earlier `f9cbe8c7` and `a12828f7` Tabs editor/test-support behavior is already represented by current main: SkeletonTreeMutations handles Tabs updates/insertion/removal, SkeletonTreeQueries visits panels, current FullLibrary preserves sanitized Tabs, and current test helpers visit panel contents. Do not downgrade that newer code to the old flattened preview.

`7f9f3643` has the same principal feature source as `22e0a3d6`; the endpoint comparison within Binding/Cells/tests/docs differs in only three test/catalog files. Aggregate the stash and branch as one package. The stash's only third-parent untracked file is an empty `.codex_write_probe`.

Source at `22e0a3d6:Binding/BootstrapView.swift` demonstrates why this must not be labeled a working public feature:

- `NearbySignalLocalStore` (`:463–474`) is one global actor with in-memory arrays and one latestDraftPreview. It is not durable, federated, or partitioned per authenticated identity.
- `publishSignal` (`:480–539`) only appends to the local array but marks the signal Live/publicNearby and reports successful publication. No publishing transport is implemented in that path.
- `defaultCoarseLocation` (`:693–699`) hardcodes a location; preview similarly falls back to default coordinates when manual input is absent.
- `requestLocation` (`:1162–1167`) updates status text; it does not request/capture location there.
- `stripImageMetadata` (`:1168–1171`) changes strings/flags and says metadata was removed; it does not transform image bytes. This is a false success claim.
- The public display copy says another user published the signal, but the shown source is this local store. Current Binding/main has no NearbySignalDraftLocalCell, NearbySignalLocalStore, or personalNearbySignalsMenuConfiguration; CellScaffold/main Sources contains none of those three directory/draft/publisher cells either. Existing physical Nearby radar and new CellNearby entity-link discovery serve different purposes; they are not this implementation.

**Native release prerequisite:** transplant the relevant surface into current architecture; implement validated manual/native location behavior, actual image sanitization before publication, owner-isolated persistent drafts, explicit reviewed publication through a real transport/store, TTL/deletion/moderation behavior, and honest no-network/permission-denied states. Preserve current bootstrap, owner-proof and privacy boundaries. Tests must exercise two separate identities/devices, restart, expiry, denied permission, and inspect transformed bytes/actual publication—not merely success labels. This is unfinished product work, not already delivered functionality and not a reason to hold a working web Butler fix indefinitely.

## Additional requested repositories: missing independent packages

These were not among the 39 no-common-ancestor refs, but root requested priority adjudication of their unique work.

### CellUtility — must include in a separate native utility release

Target main reviewed: `cae2cadd9422388ba6866e577037f14117f0d03c`. Source commit: **`b25841d31c50c763ba3f33914a46740c09187785`**, `codex/haven-runtime-readiness`.

This is a real one-commit package, 15 files: single-flight runtime initialization, fail-closed initialization errors, serialized configuration mutation, recovery of valid configuration files without replacing unavailable persisted Porthole bytes, decoded runtime readiness, nested connection ownership and awaited detach/drop completion, visible operation errors, and detached non-persisting Agreement draft review instead of implying the utility can authorize admission. UI callers and Agreement view-model changes belong with CellTool; taking CellTool alone is incomplete.

Smallest chain: integrate this full source/UI/test package into current CellUtility main, retain its direct project workspace repair, update its **old CP `7bb9e414` pin** to the intended new immutable CP/main revision, and regenerate both Xcode lockfiles from that release dependency. Do not copy old lockfiles blindly. The local absolute optional configuration directory is existing developer setup and should not be claimed as a portable user default.

The commit contains meaningful `KeychainUtilityTests`: concurrent initialization, failure remains closed, configuration serialization, malformed configuration recovery, persisted Porthole byte preservation, encrypted cold restore, detached Agreement editing/review, completed connection state, and nested connection routing. These were inspected, not run. Run them against the exact new dependency and build the macOS app before releasing. No server migration or Butler web deploy dependency is apparent.

### Sprout — missing capability/proof forwarding, with compatibility correction

Root's fresh origin/main: **`d5a70f35`** (full SHA in JSON). Missing package: **`45ae325660aec802fac1159d302761343b754653`**, shared by `codex/archive-20260809/sprout-working-tree`, `codex/sprout-presence-seed-20260901`, and its remote archival ref. An archive label did not make the changes obsolete.

The six-path package adds CLI `--requested-capabilities`, unions that request with the selected bridge's capability requirements, and forwards entity_id/entity_inclusion_proof during capability requests and the inclusion proof into Porthole access. CellScaffold/main's SproutResolverCompatibility already accepts and uses these fields (`:314,507,689,782,794`). The existing new test verifies an explicitly requested local-model capability reaches the capability decision and Porthole access contract.

Smallest chain: apply the five code/test paths from `45ae3256` to fresh d5a70f3, preserve its Swift Crypto 4/Linux compatibility, optionally retain the associated historical assessment as documentation, and add backward-compatible decoding for BootstrapExecutionContext. The commit introduces nonoptional `requestedCapabilities: [String]` under synthesized Codable without `init(from:)`. The initializer's default `[]` does **not** default a missing serialized field, so older persisted execution contexts can fail decoding. Add a synthetic old-state decode/restart regression, unknown/malformed field handling, and valid/invalid inclusion-proof forwarding tests; preserve server-side resolver verification. Rebuild Sprout and any changed consumer pin after it lands on its own main.

Primary dirty Sprout also contains newer uncommitted onboarding, identity recovery and bounded HTTP work, fully inventoried in `dirty-code-inventory.json`; this focused package decision does not declare those edits integrated or obsolete.

### PalazzoScaffold — must include, separate service release

Target main reviewed: `6a3acf54730a521a1cadf677956c887472a5ee57`. Branch **`pdd/palazzo-2026-09-14`**, tip **`fed2a2029d407c7479533abbd02314d2d3f15ed9`**, is five commits:

1. `9c8a65fd` — `/palazzo` web assets and narrow public `/palazzo/api/*` facade.
2. `6a308884` — corrected G5 preview keypaths/evidence tooling.
3. `58643a62` — `/health/ready`, `/health/build`, build metadata, optional SSH Docker resolution, image CI.
4. `a96f3858` — CI input handling and image label/build-info mismatch failures.
5. `fed2a202` — Linux OpenCombine import in PalazzoSiciliaTests.

Take the complete chain on this service's main; it is not already in CellScaffold. The facade fixes the cell endpoint, principal, action keypath and guest audience; caller input is a bounded question, not arbitrary resolver authority. Existing generic API still uses PalazzoPrincipalGateway. Source gates query length/body/media type/rate; projection fails closed for malformed safety fields and unpublishable citations. Existing tests exercise forged facade principals against protected generic routes, invalid bodies, assets, denial, malformed projection and bounded question behavior. Those are substantive source tests but have not been executed in this audit.

Release conditions: pin/record the actual CP revision and include resources; build current Linux image; run facade/health/Sicilia tests and real `/palazzo` actions; verify build SHA, readiness and public static assets. Package.swift currently silently prefers a sibling CP checkout and otherwise a moving main branch, so a local green build alone does not establish the release dependency. The image workflow/metadata should bind the actual intended revision. The rate limiter trusts the first X-Forwarded-For value by explicit source contract: ingress must overwrite untrusted forwarded headers and direct backend exposure must not let clients forge their key. No live-ingress verification was done. Historical G5 failure artifacts on the branch are not current acceptance proof.

### PyPalazzoConciergeScaffold — relevant hardening, unready public-path evidence

Target main reviewed: `0e58cdea5d7e7663b96149b209f37352c2de22f0`. Branch **`claude/palazzo-p0-guardrails-20260821`**, commit **`f0fe0958fbf9664573a3fc8fc9f2ace9b778e415`**, remains unique.

It clamps staff-only result routes away from a caller-provided guest label, denies listed privileged actions without an operator UUID allowlist, tracks bounded denials, and replaces constant production_ready=true with measured/declarative checks. These corrections are relevant and not represented in this repo's current main. They are separate from the Swift Palazzo facade above.

Do not certify this as a complete authenticated bridge fix from its tests: `tests/test_bridge_authorization.py` calls private `_handle_action_set` / `_handle_action_get` directly with a StubIdentity carrying just a UUID. The allowlist helper also accepts strings/dictionaries; this layer proves membership of a label, not control of a signing key. Actual `app.py:154–172` exposes BridgeEndpoint over WebSocket. Current PyCellProtocol/main `BridgeEndpoint.handle` intentionally treats wire identity as a public reference and passes it to `GeneralCell.get/set`, whose `_require_access` verifies owner proof. Those real paths are not exercised by these direct-handler tests, and package/runtime dependency versions must be aligned. `feed_responses` in current PyCellProtocol still uses command.identity-or-owner, a separate boundary deserving a negative real-bridge test; this audit did not run a live exploit or claim one succeeded.

Smallest safe chain: preserve the useful clamp/readiness/deny-by-default package, integrate against the intended current PyCellProtocol with unchanged cryptographic checks, and exercise actual anonymous, copied-UUID, wrong-key and valid authorized operator WebSocket calls through public get/set/feed. Keep privileged actions disabled until that works; an allowlist being nonempty is not proof that bridge authorization is ready. Release independently of the production Butler repair.

## Integration order relative to production chat

1. Root's CP security/runtime integration and CellScaffold crash fix remain the immediate production dependency chain.
2. No wholesale merge of the 39 divergent refs is necessary. Their existing content/replacements are now accounted for; unfinished Nearby Signals remains explicit.
3. Sprout forwarding can land with its state compatibility fix and refreshed consumer pins. Native CellUtility and current HavenAgentD packaging can follow independently. Palazzo is its own service release with its own build and functional gates.
4. Source review is not deployment evidence. This report does not mark unexecuted tests, uncommitted onboarding, the incomplete native Nearby prototype, or the Python bridge as completed functionality.
