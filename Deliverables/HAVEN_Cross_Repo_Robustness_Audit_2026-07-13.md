# HAVEN cross-repository robustness audit — 2026-07-13

- Status: seven repository/package repair waves verified; HAVEN-wide goals remain open
- Human decision owner: Kjetil
- Primary checkout: `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold`
- First-party scope root: `/Users/kjetil/Build/Digipomps/HAVEN`
- Audit base: CellScaffold `m0/green-test-suite` at `12e74027024cf230110f13074e74ae6cb8a15cf7`; delivered readiness commit `15e068b1db1cabe397213c09dae8ce0fe95531a8`
- Delivery policy followed: narrow repo-scoped commits and pushes after verification; no deploy, authorization weakening, private-data fallback, or unrelated dirty-tree repair.

## Executive result

The decoded-cell readiness hypothesis is confirmed as a real failure class, but it is not universal across all runtimes.

The first concrete defect was repaired in CellScaffold. `ConfigurationCatalogCell` restored runtime grants, intercepts, and defaults from a detached `Task` in `init(from:)`, while direct catalog clients and both orchestrators could resolve and immediately call actions/reads. The catalog now participates in the established waitable, serialized, idempotent `PortholeRuntimeBindingEnsuring` contract, and all direct catalog access routes through a readiness-aware client. A real encode/decode/immediate-action/read regression and concurrent idempotency coverage are green.

The identity selection used during readiness installation was also hardened. Same UUID is no longer sufficient to hydrate or substitute a signing identity: UUID and signing-public-key fingerprint must match. The negative test proves that a requester with the owner's UUID but different key cannot install or use the decoded catalog bindings; the real owner can.

No CellProtocol-core lifecycle change was made. The shared runtime has 23 heuristic source hits where a decoded Cell launches asynchronous setup, while `GeneralCell.doneInitializing()` has no consumer and `CellJSONCoder` returns decoded instances without a readiness await. Introducing a universal core readiness protocol would change shared semantics across Swift and dependent ports and therefore needs an explicit Kjetil decision plus compatibility fixtures. The lowest correct first-wave repair remained in the CellScaffold host/adapter layer.

The second repair wave closed the concrete SwiftWebScaffold occurrence. `ScaffoldInfoCell` no longer launches any setup from `init(from:)`. The first host access now enters one retryable, serialized install; all supported HTTP get/set routes await it. Owner hydration requires UUID plus signing-key fingerprint. Four tests pass, including 40 concurrent awaiters, real decoded action/state, and a same-UUID/different-key failure followed by successful retry with the proof-capable owner vault.

The third and fourth repair waves proved and fixed the production Binding families. Before repair, 41 existing parity tests passed while the new real `BindingPersonalChatHubCell` encode -> decode -> immediate-read test failed with `notFound`; a stronger follow-up then exposed duplicated decoded Agreement grants (496 became 990). A Binding-local base removes detached decoded setup, serializes and retries installation at the Cell `get`/`set` boundary, hydrates owner proof only on UUID plus signing-key fingerprint equality, and keeps grants idempotent. Personal Chat Hub, Apple Intelligence, Local LLM, Contact Endpoint, Graph Index, and the twelve `PersonalCopilotLocalCell` subclasses now use that boundary. The production `PersonalIdentityLocalCell` executes an immediate account-export action after decode. The current chat/workbench suite passes 45 tests and native catalog absorb passes one.

The same audit found nine direct detached-decoded-setup occurrences in the nested HavenAgentD package: supervisor, identity, remote intent inbox/review, local model, network sentinel, secret credential, mail draft, and signature. They now share one requester-aware readiness base, start no setup from decoded initialization, restore only exact UUID+signing-fingerprint owners, and keep permissions idempotent. The first real supervisor regression failed with `notFound`; the final stable `swift test --no-parallel` run passes all 118 package tests, including identity, signature, credential, bridge-401, lifecycle, scheduler, and the new all-nine round trips. A direct Ed25519 verification was added to the sign-statement test. Intermediate failures while CellProtocol source changed during compilation are recorded as dirty-work overlap, not accepted product evidence.

The fifth verified repair wave closed the clean Add2Entity candidate. `Add2EntityCaptureCell` no longer launches decoded setup, awaits one retryable requester-proof installation at `get`/`set`, and preserves exact Agreement grants. Its new target proves 40 concurrent first awaiters, real state and side-effect-free preview, stable grants, same-UUID/different-key rejection, and owner-requester retry. The complete package now passes 16 tests instead of the previous 14.

The sixth verified repair wave closes DiMy's three runtime candidates with the same narrow local pattern without changing pricing, access, mint, spend, redemption, transferability, cash-out, or wallet semantics. The tests use only state, merchant configuration, a local pricing update, and an empty coin deposit. A concurrent missing `return` in the dirty shared `WeightedGraphRuntime.swift` temporarily blocked execution; after that owner restored a compilable snapshot, the focused tests passed 2/2 and the complete DiMy package passed 12/12.

The seventh verified wave closes the three direct SpatialRegistryScaffold candidates. `ScaffoldInfoCell`, `ContactRegistryCell`, and `ContactEndpointCell` no longer launch setup from decoded initialization and share requester-proof, serialized, retryable, idempotent readiness at `get`/`set`. Two production-class round-trip tests cover state, actions, concurrency, stable grants, wrong-key rejection, and owner retry. The complete package executes 10 tests with 9 passed, the explicitly destructive PostGIS test skipped, and 0 failures. Three other spatial Cells retain a setup Task but are safe by construction because their `get`/`set` boundary awaits the retained task.

No remaining direct Tier-1 candidate identified in the bounded Add2Entity/DiMy/Spatial wave is left unrepaired. CellUtility and several HAVEN_MVP Cells instead use `fatalError` in decoded initialization; those are explicit persistence-support gaps, not readiness races. Broad heuristic queues, restart/deep-link paths, missing/stale-proof matrices, and unbuilt product repositories remain open.

Go, Rust, and Python construct local Cells synchronously and have explicit transport-ready handshakes. Their current suites are green, but a single Swift-originated shared wire/persistence/readiness fixture is still missing, so cross-runtime parity is only partly proven.

Current staging was reverified on 2026-07-13 at approximately 08:09Z. `/health/build` reports revision `12e74027024cf230110f13074e74ae6cb8a15cf7`; `/health/ready` returns 200 and accepts traffic. The Arendalsuka data canary reports 2,218 sessions, 268 local actors, 468 map features, 80 visible sessions, loaded journals, the expected configuration, landing redirect, GET import issuance blocked with 405, and unauthenticated POST issuance blocked with 401. This proves current data/route health on the pre-repair revision; it does not prove that the local readiness repair is deployed.

No P0 defect was found. Open P1 candidates remain, so the statement “all CellProtocol functionality is robust” is not supported.

## Purpose tree and Goal evaluation

No new Purpose node was added. Canonical lookup found that the three requested existing nodes are sufficient for routing, ownership, security review, and termination. No unmatched intent justified `purpose://prompt.unknown` or promotion.

| Purpose | Goal | Current status | Evidence | Missing before terminal success |
|---|---|---|---|---|
| `purpose://quality` | `goal.haven.cross-repo.runtime-correctness` | **Open / partial** | CellScaffold, SwiftWeb, Binding chat/PersonalCopilot, all nine HavenAgentD Cells, Add2Entity, DiMy, and Spatial direct candidates repaired and tested | Restart/persisted-container and remote/deep-link gates; completion of manual classification for broad CellScaffold/core hit sets; explicit support policy for fatal-decode Cells |
| `purpose://test.acceptance` | `goal.haven.cross-repo.regression-gates` | **Open / partial** | Real round trips and actions across all seven repaired areas; concurrent/idempotent installation; wrong-key negatives; 118-test HavenAgent package; Workbench/Arendalsuka/Conference/Co-Pilot/Spatial dynamic paths; live Arendalsuka canary; cross-language suites | Shared golden fixture; process-restart gates; missing/stale-proof matrix; tailored conference shared-owner readiness tests; browser artifacts; full negative production-surface gate |
| `purpose://access.audit.privacy` | `goal.haven.cross-repo.security-preservation` | **Pass for verified changed paths; HAVEN-wide open** | UUID+fingerprint owner matching and same-UUID/different-key negatives in all seven repaired areas; public Arendalsuka Agreement path; live admin issuance rejection | Missing-proof and stale-proof cases for every changed/future host; classification of remaining broad heuristic hits |

`purpose://gui.quality.functional-accessible` and `purpose://skeleton.owner-entity-access` remain useful facets for later GUI and owner-access waves, but no new taxonomy was necessary in this wave.

## Audit method and classification

The static search targeted required `init(from:)` near `Task {}`, `Task.detached`, permission/key setup, intercept registration, Porthole endpoints, persistence, catalog publication, and immediate host reads/actions. A heuristic match is not itself a defect.

- **Vulnerable**: decoded setup is asynchronous, a supported host can read/act immediately, and no waitable gate is present.
- **Safe by construction**: setup is synchronous before publication/return, or decode is explicitly unsupported and cannot be published as persisted support.
- **Tested safe**: the production Cell and payload execute encode/decode plus immediate supported operations through a readiness gate, including concurrency where relevant.
- **Unknown**: a candidate exists, but publication/host/restart evidence is incomplete.

The bounded multi-line search found 23 matching CellProtocol source files and 110 matching CellScaffold source files. These are audit queues, not 133 asserted defects. Several matches are false positives, have narrower ownership, or are already covered by the Porthole ensuring adapter.

## Repository inventory and risk tiers

Dirty counts are the final verification snapshot. Existing and concurrently arriving changes were preserved. CellScaffold contains 7 audit files and 23 unrelated Butterpop, MusicPublishing, PaymentGate, and Co-Pilot paths; the canonical documents checkout contains 19 pre-existing paths plus the 2 audit artifacts. Nested documentation checkouts are listed as duplicates; `test/test` is a disposable clone and is excluded from first-party modification scope.

| Repository | Role / dependency | Branch / HEAD | Dirty | Risk and evidence |
|---|---|---|---:|---|
| Binding | Native SwiftUI host, renderer, remote/deep-link and identity surface; includes HavenAgentD | `main` / `953e190d9101` | 15 | **Tier 1, locally repaired for audited families.** Five workbench Cells, twelve PersonalCopilot subclasses, and nine HavenAgentD Cells now have requester-aware readiness. Chat/workbench 45, catalog 1, and HavenAgentD 118 pass. Remote/deep-link and separate-process restart remain open. |
| Binding/CellProtocolDocuments | Nested docs duplicate | `main` / `e138166d1cb8` | 0 | Excluded from canonical docs edits; primary docs checkout owns delivery. |
| CellProtocol | Swift reference contracts, resolver, persistence, identity | `main` / `8e96499ee216` | 16 | **Tier 1, open policy and active overlap.** 23 heuristic decode/Task files. Forty-six focused lifecycle/persistence/identity/contract tests passed on the earlier stable snapshot; later concurrent identity/permission/weighted-graph/docs edits were preserved. A temporary missing `return` blocked a dependent build, but its owner restored compilation before final DiMy/Spatial verification. No audit edit was made in core. |
| CellProtocolDocuments | Canonical Book, security, Purpose, deliverables | `main` / `ccc11559f7c5` | 21 | **Tier 2.** Nineteen unrelated dirty paths preserved; this report and its staging-evidence JSON are the two audit artifacts. |
| CellScaffold | Porthole/web host, catalog, skeleton runtime, products | `m0/green-test-suite` / `12e74027024c` | 30 | **Tier 1.** Seven audit files repair the confirmed catalog defect; 23 unrelated concurrent paths remain untouched. Sixteen locally constructible ensuring Cells have generic concurrency/idempotency coverage. Two specialized conference shared-owner Cells still need tailored coverage. |
| CellScaffold/CellProtocolDocuments | Nested docs duplicate | `main` / `a08f72f369fa` | 0 | Excluded from canonical docs edits. |
| CellUtility | Xcode utility and EventEmitter sample | `main` / `cae2cadd9422` | 0 | **Tier 3.** `EventEmitterCell.init(from:)` is `fatalError`, not a race. Three unit tests passed; UI test target was skipped by Xcode. Persistence support remains absent. |
| DiMy Source Editor Extension | Source editor extension | `main` / `fecf9746c7b8` | 0 | **Tier 3.** No Swift decode/async-setup hit in the bounded scan; not built in this wave. |
| DiMyDevRAG | Development RAG service | `main` / `2d6e3addff2c` | 0 | **Tier 3.** No Swift decoded-cell hit; service-level persistence/functional behavior not exercised. |
| DiMyDocuments | Documentation | `micropayments-production-hardening` / `e11442ebcbb4` | 44 | Docs only; unrelated dirty work preserved. |
| DiMyMicropayments | Payment/access/wallet Cell packages | `main` / `3179c22f5863` | 10 | **Tier 1, repaired and tested.** The three runtime Cells no longer launch decoded setup. Two new round-trip/action/proof tests pass, and the full package is 12/12 green. Four unrelated pre-existing files plus `Package.resolved` are preserved. No payment/value semantics were broadened. |
| DiMyMint | Mint service/package | `micropayments-production-hardening` / `656ccad6564c` | 2 | **Tier 2.** No bounded decode/Task hit; dirty package work preserved; not retested. |
| GoCellProtocol | Go protocol port and CloudBridge | `main` / `c686d0dbb48a` | 0 | **Tier 2.** Local construction is synchronous; transport has explicit ready behavior. `go test ./...` passed. Shared Swift golden readiness/persistence fixture missing. |
| HAVEN_MVP | Legacy app prototypes | `main` / `5dc692fc5e39` | 0 | **Tier 3/open persistence.** Several Cells use `fatalError` for decode. This is unsupported persistence, not the detached-setup race. Not built. |
| PyCellProtocol | Python protocol/scaffold port | `main` / `1a4b3c982d9b` | 13 | **Tier 2.** Local async APIs construct synchronously with explicit bridge ready. Twenty-nine tests passed. Existing upstream-sync dirty work preserved. Shared Swift fixture missing. |
| RustCellProtocol | Rust protocol port | `codex/cellprotocol-upstream-sync` / `35f7732bfe5d` | 0 | **Tier 2.** Local construction is synchronous; bridge has `wait_ready`. Twenty-three tests passed. README correctly limits parity claims; shared Swift fixture missing. |
| SafariExtentions/Add2Entity | Browser capture/RAG preparation Cell | `main` / `ff0a35080b3c` | 3 | **Tier 1, repaired and tested.** The capture Cell uses serialized requester-proof readiness; two new decoded production tests and all fourteen prior tests pass (16 total). |
| SpatialRegistryScaffold | Spatial service, contact endpoints, Co-Pilot routing | `main` / `c0074c5fd7ff` | 8 | **Tier 1, repaired for direct candidates.** Three spatial Cells retain and await a deferred setup Task and are safe by that construction. `ScaffoldInfoCell`, `ContactRegistryCell`, and `ContactEndpointCell` now use guarded readiness. The full package executes 10 tests: 9 passed, 1 destructive PostGIS test skipped, 0 failed. Three unrelated dirty paths and overlapping prompt additions in two touched files were preserved. |
| SwiftWebScaffold | Portable Swift/Vapor scaffold template | `main` / `6743d23ffbc9` | 3 | **Tier 1 path repaired locally.** `ScaffoldInfoCell` no longer launches decoded setup; supported routes await retryable readiness. Four tests cover routes, decode, 40-way concurrency, action/state, wrong-key rejection, and proof-vault retry. |
| UniverseSimulation | Simulation product | `master` / `a2a19e0fde98` | 19 | **Tier 3.** No bounded Swift decode/Task hit; dirty work preserved; not built. |
| WatchPong | Watch product | `main` / `e57e6c015191` | 0 | **Tier 3.** No bounded Swift decode/Task hit; not built. |
| sprout | Product/application | `main` / `7d82016067a9` | 27 | **Tier 3.** No bounded Swift decode/Task hit; dirty work preserved; not built. |
| test/test | Disposable/test clone | `main` / `019280c14a06` | 0 | Excluded duplicate/test checkout. |

Non-git first-party directories (`GUI/Chat`, `AppleWatchApps/MeditationWatch`, `Ensamble`, `InnovasjonNorge`, `PyPalazzoConciergeScaffold`, `SafariExtentions/CookieSwap`) were classified as product/docs/tooling directories rather than independent Git delivery units. The bounded Swift scan found no direct readiness-class hit in `GUI/Chat`; they were not claimed tested.

## Findings and repairs

### D1 — ConfigurationCatalog decoded runtime can be observed before bindings exist

Severity: P1 correctness

Status: repaired and tested locally

`ConfigurationCatalogCell.init(from:)` launched permission, key, and defaults setup in a detached `Task`. `ConfigurationCatalogClient` and both orchestrators resolved the catalog and immediately issued `catalog.syncScaffoldGoals`, `catalog.allConfigurations`, or menu reads. The production catalog can therefore be healthy in persisted state while exposing missing actions/empty data during the race.

Repair:

- `ConfigurationCatalogCell` now conforms to `PortholeRuntimeBindingEnsuring`.
- Fresh and decoded construction route through the same serialized/idempotent installer.
- The installer owns permissions, intercepts, and default bootstrapping as one waitable unit.
- `ConfigurationCatalogClient` provides readiness-aware list and value operations.
- Both orchestrators use that client instead of resolving and reading directly.

Production evidence: real catalog encode/decode, immediate ensured sync/read, non-empty defaults, `HAVEN Workbench` presence, and state count all pass.

### D2 — Runtime identity hydration trusted UUID equality too broadly

Severity: P1 security risk, exploitability not asserted

Status: hardened and negatively tested

The readiness helper could choose a requester/vault identity from UUID equality alone. Identity selection now requires both UUID and signing-public-key fingerprint before hydration/substitution. The real stored owner remains the installation candidate when an attacker presents the same UUID with another signing key. `GeneralCell` challenge/proof enforcement remains active; no cookie/admin bypass or broad grant was introduced.

### D3 — Existing tests can be green while decoded runtime support is untested

Severity: P1 regression-coverage gap

Status: repaired for the three direct candidate repositories; broader coverage gap remains

SpatialRegistryScaffold, DiMyMicropayments, and Add2Entity all passed their prior suites while the candidate decoded Cells had no round-trip/readiness test. This directly supports C4. Each now has a real production-class encode/decode, immediate read/action, concurrency, idempotency, and wrong-key gate. Separate-process restart and broader product coverage remain open.

### D4 — Shared runtime exposes no consumed local readiness lifecycle

Severity: architectural decision, not changed

Status: open, owner Kjetil

`GeneralCell` contains a private `initialized` flag and `doneInitializing()`, but no runtime consumer. `CellJSONCoder.decodeEmitCell` returns the decoded instance immediately. The resolver touches lifecycle after resolution but has no general decoded-runtime binding await. A core protocol would need to define which decoded types require readiness, error/cancellation/timeout semantics, idempotency, and compatibility behavior for Go/Rust/Python. This wave intentionally did not move app setup semantics into CellProtocol core.

### D5 — Other concrete Swift candidates

Status: direct candidates closed locally; broader queues remain open

- Binding: workbench, PersonalCopilot, and all nine HavenAgentD direct candidates are repaired and tested. Native catalog absorb remains green, but restart/deep-link replay is open.
- SpatialRegistryScaffold: three spatial Cells are safe by awaited `deferredSetupTask`; the scaffold/contact Cells are repaired and tested.
- DiMyMicropayments: three runtime Cells are repaired and the complete 12-test package is green.
- Add2Entity: the capture Cell is repaired and all 16 tests are green.

### D6 — Explicit decode support gaps

Status: open but separately classified

CellUtility `EventEmitterCell` and several HAVEN_MVP Cells call `fatalError` from required decoded initialization. They cannot honestly claim persisted/reloaded support. The correct future repair is either an implemented, tested decode path or registration/configuration that explicitly rejects persistence for those types before runtime decode; converting them to detached setup without readiness would be rejected.

### D7 — SwiftWebScaffold detached decoded setup and immediate HTTP access

Severity: P1 correctness/security

Status: repaired and tested locally

The initial new regression failed with missing keys and `notFound`, proving that simply retaining a decoded setup Task was not enough when the decoded owner no longer had a proof-capable vault. The final repair removes asynchronous work from `init(from:)` entirely. A per-Cell actor serializes the first lazy installation, propagates an explicit error when owner proof is unavailable, and permits a later retry. Only a default-vault identity with the stored UUID and signing-key fingerprint is accepted. The two template routes and generic Cell get/set routes await the contract.

The negative test installs an attacker vault containing the same UUID with another key, observes fail-closed readiness and absent template keys, then switches to the real owner vault and proves a successful retry. Concurrent callers share one installation generation, preventing an older failed waiter from clearing a newer retry task.

### D8 — Binding persistent chat-workbench Cells fail immediate decoded reads

Severity: P1 correctness/security

Status: repaired and tested locally for five Cells

The new production round trip initially failed with `notFound` while the other 41 chat parity tests passed. After serializing lazy installation, a stricter grant-stability assertion exposed a second defect: decoded `Agreement` grants were installed again, increasing the chat hub's list from 496 to 990 entries. The final Binding-local base class starts no setup from `init(from:)`, intercepts the polymorphic Cell `get`/`set` boundary, shares one retryable installation generation, and adds only grants absent from the persisted Agreement.

`BindingPersonalChatHubCell`, `BindingAppleIntelligenceProviderCell`, `BindingLocalLLMCell`, `BindingContactEndpointCell`, and `BindingGraphIndexCell` now use the base. Proof hydration accepts the stored identity directly when it retains a vault; otherwise the default vault must contain the same UUID and signing-key fingerprint. A same-UUID/different-key vault fails closed, and switching to the real owner vault permits retry. The test uses 40 simultaneous first reads for the chat hub and 20 simultaneous installations for each of the other four Cells, followed by real state reads and a chat composer action.

### D9 — Binding PersonalCopilot base launched decoded setup for twelve Cells

Severity: P1 correctness/security

Status: repaired and tested at the shared base plus one real production action

`PersonalCopilotLocalCell` now inherits the same serialized Binding readiness boundary. Fresh instances mark installation complete; decoded instances start no detached work; `get`/`set` await exact owner proof. All twelve subclasses inherit the fix. `PersonalIdentityLocalCell` is round-tripped and exercised with 40 concurrent state reads, stable grants, and immediate `requestExport`. Per-subclass actions for the other eleven Cells and separate-process restart remain open.

### D10 — Nine HavenAgentD Cells had the direct failure pattern

Severity: P1 correctness/security

Status: repaired and fully package-tested locally

The new `HavenAgentRuntimeBindingCell` serializes installation, rejects same-UUID/different-key requesters, allows requester-bound exact owner proof even when the mutable global default vault belongs to another identity, and makes permission setup idempotent. The nine production Cells no longer launch `Task` from decoded initialization. The regression suite round-trips every Cell, concurrently ensures each, reads real state, and exercises supervisor and signing paths. The stable final gate is 118/118 with `swift test --no-parallel`.

### D11 — Add2Entity capture adapter exposed a decoded race

Severity: P1 correctness/security

Status: repaired and tested locally

`Add2EntityCaptureCell` now owns a retryable local readiness coordinator and awaits it at the actual `get`/`set` boundary. The source contract, Explore metadata, flow payload, and side-effect policy are unchanged. The new test proves decoded state, side-effect-free preview, concurrent first access, grant stability, wrong-key rejection, and correct requester retry. The complete package passes 16 tests.

### D12 — DiMy access/pricing/wallet setup was detached after decode

Severity: P1 correctness/security; payment guardrails apply

Status: repaired and tested locally

`DiMyAccessRuntimeCell`, `DiMyPricingPolicyCell`, and `DiMyWalletRuntimeCell` now share `DiMyRuntimeBindingCell`. No value model or payment action was added or broadened. Access and pricing remain existing internal contracts; wallet value remains a technical-lab variant with no new P2P transfer, cash-out, external acceptance, or custody claim. Tests cover state, merchant configuration, local pricing, empty deposit, concurrency, stable exact grants, and wrong-key retry. After a concurrent shared-core edit was repaired by its owner, the focused gate passed 2/2 and the full package passed 12/12.

### D13 — Spatial scaffold/contact Cells launched unawaited decoded setup

Severity: P1 correctness/security

Status: repaired and tested locally

`ScaffoldInfoCell`, `ContactRegistryCell`, and `ContactEndpointCell` could expose decoded instances before their grants and intercepts existed. The two contact Cells additionally tried to decode an `owner` from their own keyed container even though their encoder did not write that key there, so setup could be omitted rather than merely late. They now share `SpatialRuntimeBindingCell`: decoded initialization starts no Task; first `get`/`set` serializes a retryable install; owner hydration requires UUID plus signing-key fingerprint; grants are exact and idempotent. The tests round-trip all three real classes, concurrently ensure them, exercise state and actions, compare grant counts, reject a forged same-UUID key, and then succeed with the real requester proof.

The three Task hits in `SpatialCells.swift` were not rewritten: each stores `deferredSetupTask`, and its overridden `get`/`set` awaits that task before access. They remain classified safe by construction, not ignored false positives.

## Changed files in CellScaffold

- `Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift`
- `Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogClient.swift`
- `Sources/App/Cells/SimpleProjectManager/OrchestratorCell.swift`
- `Sources/App/Cells/SimpleProjectManager/ScaffoldOrchestratorCell.swift`
- `Sources/App/Support/PortholeRuntimeBindingEnsuring.swift`
- `Tests/AppTests/ConfigurationCatalogClientTests.swift`
- `Tests/AppTests/PortholeRuntimeBindingEnsuringTests.swift`

The final focused diff is 238 insertions and 38 deletions across seven files. `git diff --check` passes. `Package.resolved` changes caused by test planning were restored. Butterpop, PaymentGate, MusicPublishing, and the newly present Co-Pilot architecture document were not edited, staged, or reverted; some of those unrelated edits appeared while this audit was running.

## Changed files in SwiftWebScaffold

- `Sources/App/Cells/ScaffoldInfoCell.swift`
- `Sources/App/routes.swift`
- `Tests/AppTests/SwiftWebScaffoldTests.swift`

The focused diff is 205 insertions and 10 deletions across three files. `git diff --check` passes, and `Package.resolved` remains unchanged.

## Changed files in Binding

- `Binding/BootstrapView.swift`
- `Binding/ChatWorkbenchParityCells.swift`
- `BindingTests/ChatWorkbenchParityTests.swift`
- `HavenAgentD/Sources/HavenAgentCells/HavenAgentRuntimeBindingCell.swift`
- `HavenAgentD/Sources/HavenAgentCells/AgentIdentityCell.swift`
- `HavenAgentD/Sources/HavenAgentCells/AgentLocalModelCell.swift`
- `HavenAgentD/Sources/HavenAgentCells/AgentMailDraftCell.swift`
- `HavenAgentD/Sources/HavenAgentCells/AgentSignatureCell.swift`
- `HavenAgentD/Sources/HavenAgentCells/AgentSupervisorCell.swift`
- `HavenAgentD/Sources/HavenAgentCells/NetworkSentinelCell.swift`
- `HavenAgentD/Sources/HavenAgentCells/RemoteIntentInboxCell.swift`
- `HavenAgentD/Sources/HavenAgentCells/RemoteIntentReviewCell.swift`
- `HavenAgentD/Sources/HavenAgentCells/SecretCredentialCell.swift`
- `HavenAgentD/Tests/HavenAgentCellsTests/AgentCellsTests.swift`
- `HavenAgentD/Tests/HavenAgentRuntimeTests/AgentSignStatementCommandServiceTests.swift`

`git diff --check` passes. Binding was clean before this audit; these fifteen paths are the complete local Binding/HavenAgentD audit wave.

## Changed files in Add2Entity

- `Package.swift`
- `Sources/Add2EntityCell/Add2EntityCaptureCell.swift`
- `Tests/Add2EntityCellTests/Add2EntityCaptureCellRuntimeBindingTests.swift`

`git diff --check` passes. No pre-existing dirty file was present.

## Changed files in DiMyMicropayments

- `Package.swift`
- `Sources/DiMyCellProtocolCells/DiMyRuntimeBindingCell.swift`
- `Sources/DiMyCellProtocolCells/DiMyAccessRuntimeCell.swift`
- `Sources/DiMyCellProtocolCells/DiMyPricingPolicyCell.swift`
- `Sources/DiMyCellProtocolCells/DiMyWalletRuntimeCell.swift`
- `Tests/DiMyCellProtocolCellsTests/DiMyRuntimeBindingTests.swift`

`git diff --check` passes. Pre-existing `Package.resolved`, `Sources/DiMyPaymentTypes/PaymentTypes.swift`, `Tests/DiMyWalletCellTests/WalletCellTests.swift`, and `docs/api-reference.md` changes were preserved and are not part of this repair.

## Changed files in SpatialRegistryScaffold

- `Sources/App/Cells/SpatialRuntimeBindingCell.swift`
- `Sources/App/Cells/ScaffoldInfoCell.swift`
- `Sources/App/Cells/ContactEndpoint/ContactRegistryCell.swift`
- `Sources/App/Cells/ContactEndpoint/ContactEndpointCell.swift`
- `Tests/AppTests/SwiftWebScaffoldTests.swift`

`git diff --check` passes. Pre-existing work in `README.md`, `Sources/App/Cells/Spatial/SpatialCells.swift`, `Sources/App/routes.swift`, and the existing prompt/routing additions in `ScaffoldInfoCell.swift` and `SwiftWebScaffoldTests.swift` was preserved. The audit changed only lifecycle/readiness code in the shared files and appended two focused tests plus one helper.

## Verification ledger

### CellScaffold repair and production paths

| Command | Result | What it proves / does not prove |
|---|---|---|
| `scripts/run_tests_isolated.sh --filter PortholeRuntimeBindingEnsuringTests` | 3 passed | Real decoded catalog, same-UUID/different-key rejection, and concurrent/idempotent ensuring for 16 locally constructible Cells. Specialized conference shared-owner Cells remain outside this generic constructor. |
| `scripts/run_tests_isolated.sh --filter ConfigurationCatalogClientTests` | 4 passed | Client invokes readiness before immediate action/read and keeps decode behavior. |
| `scripts/run_tests_isolated.sh --filter ProductionSkeletonBindingIntegrityTests` | 4 passed | Production Workbench and Arendalsuka configurations/payloads keep resolvable keypaths, Agreement-backed atlas reads, non-empty rows, and detail/tab actions. |
| `scripts/run_tests_isolated.sh --filter ConferenceSurfaceRoutesTests/testAuthenticatedPortholeConferenceDemoFlowSupportsCanonicalPersonaLockedSequence` | 1 passed | Authenticated local HTTP/Porthole Conference sequence with canonical personas. No real browser screenshot. |
| `scripts/run_tests_isolated.sh --filter PersonalCopilotV1Tests/testChatPromptSubmitRoutesPortholeCommandsBeforeActiveHelper` | 1 passed | Co-Pilot routes Porthole commands before an active helper without unintended helper action. |
| `git diff --check` | passed | Patch whitespace integrity only. |

The first unprivileged rerun of the production-skeleton suite failed because SwiftPM's internal `sandbox-exec` could not apply its sandbox. The same isolated command was rerun outside that sandbox and passed. This was an execution-environment failure, not a product test failure.

### Core, Binding, ports, and services

| Repository / command | Result | Limitation |
|---|---|---|
| CellProtocol: `swift test --filter 'GeneralCellInterfaceTests|PersistenceTests|CellLifecycleTests|ContractProbeCellTests|IdentityDomainBindingTests'` | 46 passed | No universal decode-readiness contract. |
| Binding: `Scripts/test_binding.sh CODE_SIGNING_ALLOWED=NO -only-testing:BindingTests/ChatWorkbenchParityTests` | 45 passed | Workbench plus the production PersonalIdentity decoded path; immediate/concurrent state/action; stable grants; wrong-key rejection and retry. No separate-process restart. Latest artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/Binding-erntjstdfcrbeachccbemadrrbon/Logs/Test/Test-HAVEN-2026.07.13_11-01-33-+0200.xcresult`. |
| Binding: `Scripts/test_binding.sh CODE_SIGNING_ALLOWED=NO -only-testing:BindingTests/CatalogAbsorbXCTest` | 1 passed | Native Porthole catalog resolution and attached state remain green against the current shared core. Artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/Binding-erntjstdfcrbeachccbemadrrbon/Logs/Test/Test-HAVEN-2026.07.13_11-13-07-+0200.xcresult`. A direct non-script workspace run hit stale persistent app-container owner proof and was rejected; no bypass was added. |
| HavenAgentD: `swift test --no-parallel` | 118 passed | All nine decoded Cells, identity/signature, credential, bridge 401, lifecycle and scheduler paths. No process restart. |
| GoCellProtocol: `go test ./...` | passed | No shared Swift readiness fixture. |
| RustCellProtocol: `cargo test` | 23 passed | No shared Swift readiness fixture. |
| PyCellProtocol: `pytest -q` | 29 passed | No shared Swift readiness fixture; pre-existing dirty sync work. |
| SwiftWebScaffold: `swift test --disable-automatic-resolution` | 4 passed | Covers decoded `ScaffoldInfoCell`, immediate action/state, 40 concurrent awaiters, wrong-key rejection and retry; module-cache warnings remain. |
| CellUtility: `xcodebuild -project CellUtility.xcodeproj -scheme KeychainUtility -destination 'platform=macOS,arch=arm64' CODE_SIGNING_ALLOWED=NO test` | 3 unit tests passed; UI target skipped | `EventEmitterCell` decode remains unsupported. Artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/CellUtility-fxbvepqsfkvodlhidadiuzrseiih/Logs/Test/Test-KeychainUtility-2026.07.13_10-00-23-+0200.xcresult`. |
| SpatialRegistryScaffold: `swift test` | 10 executed, 1 destructive PostGIS test skipped, 0 failures | Includes two decoded scaffold/contact gates, production state/actions, concurrency, stable grants, wrong-key rejection and retry. No external PostGIS or separate-process restart proof. |
| DiMyMicropayments: `swift test --filter DiMyRuntimeBindingTests`; `swift test` | 2/2 focused; 12/12 full package | Real access/pricing/wallet round trips and actions, concurrency, stable grants, wrong-key rejection and retry. No payment rail, external-value, or separate-process test. |
| Add2Entity: `swift test` | 16 passed | Includes two decoded capture Cell tests: 40-way readiness, immediate state/preview, grant stability, wrong-key rejection and requester-proof retry. |

Build warnings remain: Swift 6 Sendable warnings in CellProtocol consumers, two unhandled Conference markdown files in CellScaffold, and expected first-run missing-file/optional-cell diagnostics in isolated runtime logs. They did not fail these focused gates and are not treated as resolved.

The first executing Binding regression run failed only the new decoded chat test with `notFound` while 41 existing tests passed; artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/Binding-erntjstdfcrbeachccbemadrrbon/Logs/Test/Test-HAVEN-2026.07.13_10-32-46-+0200.xcresult`. The first serialized-install version then failed the new grant-stability assertions because 496 persisted grants became 990; artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/Binding-erntjstdfcrbeachccbemadrrbon/Logs/Test/Test-HAVEN-2026.07.13_10-39-25-+0200.xcresult`. HavenAgentD's first supervisor decode regression likewise failed with `notFound`. These are preserved as red-before-green evidence.

Rechecks against the later shared-core snapshot: CellScaffold `PortholeRuntimeBindingEnsuringTests` passes 3/3 and SwiftWebScaffold passes 4/4. The CellScaffold `ConfigurationCatalogClientTests` recheck is temporarily unbuildable because a concurrent unrelated `PersonalCopilotV1Tests.swift` edit references a missing `asInt`; the earlier isolated 4/4 result remains the last valid evidence. `Package.resolved` did not change during the recheck.

### Current staging evidence

Commands:

```text
curl -fsS https://staging.haven.digipomps.org/health/build
curl -i -sS https://staging.haven.digipomps.org/health/ready
npm run arendalsuka:data-health -- --base-url https://staging.haven.digipomps.org --min-sessions 2000 --min-local-actors 50 --min-map-features 50
```

Observed:

Machine-readable artifact: `Deliverables/HAVEN_Cross_Repo_Robustness_Audit_2026-07-13_Staging_Arendalsuka.json`.

| Check | Current result |
|---|---|
| Build | `status=ok`, build timestamp `2026-07-13T05:22:50Z`, app revision `12e74027024cf230110f13074e74ae6cb8a15cf7` |
| Ready | HTTP 200, `mode=serving`, `acceptsNewTraffic=true` |
| Arendalsuka | 2,218 sessions; 268 local actors; 468 map features; 80 visible sessions |
| Journals/config | both journals loaded; `Arendalsuka Participant Program` skeleton present; landing redirects to its Porthole deep link |
| Security canaries | import issuance GET 405; unauthenticated POST 401 |

No mutating Workbench staging canary, deploy, or browser journey was run. The persistence/shared-access canaries create identities and state, so they were not inferred from permission to perform a read-only audit and local repair.

## Claim adjudication

| Claim | Support | Counterargument / undercut | Evaluation | Deduced work |
|---|---|---|---|---|
| C1: readiness race is a general latent class across multiple hosted Cells | Confirmed in CellScaffold, SwiftWeb, Binding workbench/PersonalCopilot, nine HavenAgentD Cells, Add2Entity, DiMy, and Spatial direct candidates; 23 core and 110 CellScaffold heuristic file hits | Many hits are already gated, false positives, specialized, or never published; Go/Rust/Python are synchronous locally; fatal decode is a different failure | **Strongly supported as a multi-repo latent Swift failure class; scope not fully enumerated as defects** | Retain and complete a per-published-Cell matrix |
| C2: detached decoded setup can cause empty/broken GUI | CellScaffold needed explicit ensuring; Binding's real decoded chat read failed with `notFound` while 41 existing tests passed | Empty GUI can also come from source failure, access denial, bad skeleton keypath, or all-or-nothing preview fallback | **Strongly supported, not exclusive as a cause** | Keep diagnostics able to distinguish not-ready, denied, not-found, and empty-source states |
| C3: host must await readiness before state/action | Porthole and SwiftWeb host adapters plus Binding, Add2, DiMy, and Spatial Cell boundaries fixed confirmed paths without changing core semantics | Cells with synchronous setup or an awaited retained task need no additional wait; a universal core rule still needs cancellation/error/timeout/wire design; `keys()` is not open for subclass interception | **Accepted:** every asynchronously restored supported Cell must be awaited at its narrowest host/Cell adapter; universal core promotion remains a separate compatibility decision | Apply the local adapter pattern to future confirmed candidates; propose core change only if a required host surface cannot be safely intercepted |
| C4: coverage is insufficient if known data can render empty while tests pass | Binding had 41 green parity tests beside a new real decoded `notFound`; HavenAgentD and the three later repos also needed real decode gates; Add2 grew from 14 to 16 tests | Existing tests remain valuable for other contracts | **Accepted** | Add restart and negative empty-data canaries |
| C5: reliability fixes must not bypass identity/capability | UUID+fingerprint hardening and wrong-key negatives in all seven repaired areas; requester-bound HavenAgent proof prevents mutable-default-vault races; Agreement-backed Arendalsuka and live 401/405 | Missing/stale cases are not exhaustive | **Accepted and preserved in verified changed paths; full matrix open** | Add missing/stale/public cases alongside remaining classification and restart work |
| C6: shared wire fixtures can primarily guard cross-runtime parity | Go/Rust/Python suites cover wire, bridge ready, identity, replay, and configuration semantics; runtime-specific smokes fit above | No single Swift-exported readiness/persistence golden fixture is consumed by all ports | **Partially supported** | Define one versioned Swift fixture set for encode/decode/state/action/error and consume it in Go/Rust/Python; retain host-specific functional smokes |

Adviser voting was not used. Evaluation follows source, executable tests, live responses, and explicit gaps.

## Access/privacy preservation matrix

| Case | Evidence in this wave | Status |
|---|---|---|
| Same UUID, wrong signing key | New decoded CellScaffold, SwiftWeb, Binding, HavenAgentD, Add2Entity, DiMy, and Spatial negative tests | Pass in all seven repaired areas |
| Unauthenticated privileged import | Live POST returns 401 | Pass for this endpoint |
| Wrong method on privileged import | Live GET returns 405 | Pass |
| Public read through owner Agreement | Arendalsuka production skeleton Agreement test | Pass for this path |
| Missing proof | Not executed for every changed/candidate path | Open |
| Stale proof | Not executed for every changed/candidate path | Open |
| Cookie/admin convenience bypass | No such bypass added; authenticated Conference test retained canonical persona/identity bootstrap | No known bypass in changed path |

## Functional coverage map

| Journey | Real input and dynamic assertions | Saved artifact | Honest status |
|---|---|---|---|
| HAVEN Workbench | Production configuration through local Porthole; supported keypaths/actions asserted | Test log only | Local pass; no live mutating persistence/shared-access canary |
| Arendalsuka Participant/Event Atlas | Production configurations/fixtures locally plus current live data/security canary | This report contains exact live observations | Local and read-only live pass on pre-repair staging revision |
| Conference | Authenticated Porthole HTTP sequence with canonical personas | Test log only | Local pass; no real browser screenshot or Binding parity replay |
| Co-Pilot routing/chat | Real `PersonalCopilotV1` Cell action path asserts routing order | Test log only | Local pass for selected route; not an exhaustive chat journey |
| Binding | Native production chat/PersonalIdentity Cells, all nine HavenAgentD Cells, plus catalog absorb | Red-before-green and final `.xcresult`/Swift package results above | Audited families pass locally; per-PersonalCopilot-subclass actions, remote/deep-link replay, and restart remain open |
| SwiftWebScaffold | Real decoded Cell plus HTTP routes | Test log only | Local pass; no deployment or separate-process restart |
| Add2Entity | Real decoded capture Cell and production preview payload | Test log only | Local pass; preview remains side-effect-free; no native extension/restart journey |
| DiMy | Real decoded access/pricing/wallet tests | Test log only | Focused 2/2 and package 12/12 pass; no external payment rail or restart journey |
| SpatialRegistryScaffold | Real decoded scaffold/contact Cells plus production HTTP map, privacy, entitlement, prompt, publish/query/outcome/revoke flows | Test log only | 10 tests pass with the explicitly destructive PostGIS test skipped; no deployment or separate-process restart |

Screenshot-only evidence was not used. Conversely, this wave does not claim browser-visible parity where no browser artifact was captured.

## Decision log

1. Kept the first repair in CellScaffold's established Porthole/runtime-binding adapter because the confirmed defect included app-specific catalog defaults and menu semantics.
2. Removed detached decoded setup from SwiftWebScaffold and made its host routes own the awaited, retryable local contract.
3. Moved five Binding workbench Cells to one Binding-local readiness base that intercepts the actual polymorphic `get`/`set` boundary; no renderer or transport was made to own their setup semantics.
4. Did not change CellProtocol core. Three successful local ownership patterns show that universal semantics are not yet necessary; a core proposal would still require explicit approval and port compatibility design.
5. Required signing-key fingerprint equality in addition to UUID for readiness identity hydration.
6. Made restored Agreement grants idempotent after the Binding regression proved that serialized setup alone could still duplicate persisted grants.
7. Applied the same local ownership pattern to Binding PersonalCopilot, HavenAgentD, Add2Entity, DiMy, and the three Spatial direct candidates; did not promote app semantics into CellProtocol core.
8. Required requester-bound exact proof where mutable global default vaults could race, especially HavenAgentD and the new Add2/DiMy/Spatial bases.
9. Classified DiMy wallet runtime as technical-lab wallet value and changed no transferability, cash-out, external acceptance, custody, mint, spend, or redemption semantics.
10. Did not weaken `validateAccess`, introduce admin-cookie authorization, broaden grants, or substitute private/admin source data.
11. Reused canonical Purpose nodes; no candidate improved routing or termination enough to justify taxonomy change.
12. Preserved every unrelated dirty workstream. Did not repair the temporary concurrent CellProtocol weighted-graph syntax error (its owner restored it before final tests) or the unrelated CellScaffold `asInt` error.
13. After Kjetil explicitly requested delivery, committed and pushed the seven narrow repo packages recorded below. No deploy was performed; live staging therefore remains on the base HEAD without the local repairs.
14. Did not run mutating staging canaries without explicit effectful authorization.

## Post-audit delivery

Kjetil explicitly requested commit and push after the local repair audit. Each code package was staged file-by-file or hunk-by-hunk, checked with `git diff --cached --check`, committed independently, pushed to its existing origin branch, and then verified with local `HEAD == @{upstream}`. Overlapping ArtistSales, Workbench, Spatial prompt/outcome, payment-type, documentation, and later-arriving Binding/HavenAgent work remained uncommitted by this audit.

| Repository | Branch | Commit | Push status |
|---|---|---|---|
| CellScaffold | `m0/green-test-suite` | `15e068b1db1cabe397213c09dae8ce0fe95531a8` | `origin/m0/green-test-suite`, verified equal |
| SwiftWebScaffold | `main` | `ac6627e82b063631911b1ce30fc2fb35f736c8af` | `origin/main`, verified equal |
| Binding, including HavenAgentD | `main` | `0bfcd3821c0f0256808887f951216e5268c2e3f1` | `origin/main`, verified equal |
| SafariExtentions/Add2Entity | `main` | `038f33918ff959e08ddbc4c5d4fed98bff6d25c8` | `origin/main`, verified equal |
| DiMyMicropayments | `main` | `065f75e85b835a055a3be5aac26f3f15595da314` | `origin/main`, verified equal |
| SpatialRegistryScaffold | `main` | `f5fda30fa96d5f8c66a6663a0b8a036ccfcda9b0` | `origin/main`, verified equal |

## Residual-risk ledger and owners

| Priority | Residual risk | Owner / blocker | Required terminal evidence |
|---|---|---|---|
| P1 | Binding audited families lack separate-process restart and remote/deep-link replay; eleven PersonalCopilot subclasses lack individual action coverage | Binding/HavenAgentD owner | Per-subclass critical action sampling, native remote/deep-link replay, restart, missing/stale proof |
| P1 | CellProtocol's 23 and CellScaffold's 110 heuristic hits are not fully manually adjudicated | Cross-repo audit owner; volume and specialized ownership | Per-type vulnerable/safe/tested/unknown matrix tied to actual publication/host path |
| P2 | Two conference shared-owner ensuring Cells are not in generic constructor coverage | CellScaffold owner | Tailored ownership-aware concurrency and decode test |
| P2 | No shared Swift-origin golden readiness/persistence fixture across Go/Rust/Python | Cross-language contract owner | Versioned fixture plus runtime consumer tests and error parity |
| P2 | Process restart/persisted-container reload is not proven for all Tier-1 Cells | Each host owner | Separate-process or durable-container restart gate with immediate reads/actions |
| P2 | Partial source-preview recovery is not comprehensively tested; all-or-nothing fallback may still hide healthy sections | Porthole/source-preview owner | Production source with one failing and one healthy section; healthy content remains visible with explicit diagnostic |
| P2 | Missing/stale-proof negatives are incomplete | Identity/security owner | Resolver-enforced matrix for all changed Tier-1 paths |
| P2 | Browser-visible Porthole/Binding parity and “Something went wrong”/unexpected empty-state gates are incomplete | GUI verification owner | Same production configuration/payload in web and Binding, DOM/native assertions, screenshots/traces, no forbidden states |
| P3 | CellUtility/HAVEN_MVP decode `fatalError` paths can crash if treated as persisted Cells | Respective product owners | Implement and test decode, or prevent persisted registration with a deterministic error |
| P3 | Skipped PostGIS smoke and unbuilt lower-risk product repos leave service-specific uncertainty | Respective repo owners and environment availability | Non-destructive test environment or explicitly approved service smokes |

## Precise completion statement

Proven in this wave:

- The CellScaffold ConfigurationCatalog readiness defect is repaired locally at every identified direct catalog call site.
- The SwiftWebScaffold `ScaffoldInfoCell` path is repaired locally with lazy retryable readiness at every supported HTTP get/set route.
- Five persistent Binding chat-workbench Cells are repaired locally at their polymorphic state/action boundary; their decoded grants remain stable.
- The shared PersonalCopilot base and all nine HavenAgentD direct candidates are repaired locally; representative production action and full HavenAgent package gates pass.
- Add2Entity capture readiness is repaired locally and all 16 package tests pass.
- DiMy's three candidates are repaired with the same guarded pattern; focused tests pass 2/2 and the full package passes 12/12.
- Spatial's three direct scaffold/contact candidates are repaired; the package executes 10 tests with 9 passed, the explicitly destructive PostGIS gate skipped, and 0 failures.
- The repairs are serialized/idempotent under concurrent ensuring for the covered Cells.
- Same UUID with different signing key is rejected for runtime owner hydration in all seven repaired areas.
- Selected production Workbench, Arendalsuka, Conference, and Co-Pilot local paths pass dynamic assertions.
- Current staging is serving the base revision and its Arendalsuka known-data/security canary passes.
- Focused core, Binding repair/parity, HavenAgentD, cross-language, SwiftWeb, CellUtility, Spatial, DiMy, and Add2Entity suites have the results recorded above.

Not proven:

- All CellProtocol functionality, all first-party products, all published Cells, or all persistence/restart paths are robust.
- Binding, HavenAgentD, Spatial, DiMy, Add2Entity, CellUtility, or HAVEN_MVP are safe for every persisted/decoded Cell; repaired paths still lack comprehensive separate-process restart/deployment proof.
- The local repair is deployed.
- Full web/native renderer and action parity.
- Complete unauthorized/wrong-identity/missing-proof/stale-proof/public-read matrices.
- Cross-runtime parity from a single shared fixture.
- Absence of every P0/P1 defect outside the investigated failure class and selected Purpose-driven paths.

Therefore `goal.haven.cross-repo.runtime-correctness` and `goal.haven.cross-repo.regression-gates` remain non-terminal. `goal.haven.cross-repo.security-preservation` is satisfied for the changed paths but remains open for unclassified candidates and incomplete missing/stale-proof coverage. The evidence supports continuing with narrow repository-local adapters; Kjetil remains the decision owner only if a later finding justifies a deliberately versioned CellProtocol-core contract proposal.
