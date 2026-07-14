# HAVEN cross-repository robustness audit — 2026-07-13

- Status: current verified checkpoint for the published core, Binding, Go, Rust, Python, and SwiftWeb repair waves; CellUtility is verified and committed locally but its archived origin rejected push; HAVEN-wide goals remain open wherever this report says **NOT PROVEN**
- Human decision owner: Kjetil
- Primary checkout: `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold`
- First-party scope root: `/Users/kjetil/Build/Digipomps/HAVEN`
- Audit base: CellScaffold `m0/green-test-suite` at `12e74027024cf230110f13074e74ae6cb8a15cf7`; latest audit-owned delivered commit `71854ceb6672671d25b434e91de300268f6ffdbb`. After that push, an independent security workstream advanced the checkout to local `14b50a51fbfd` and upstream `e3d4049fbcdc`; both contain the audit commit.
- Delivery policy followed: narrow repo-scoped commits and pushes after verification; no deploy, authorization weakening, private-data fallback, or unrelated dirty-tree repair.

> Current-truth note, 2026-07-14: the audit chronology below is retained as
> red-before-green evidence. This release-continuation section supersedes older
> statements that CellProtocol core had no readiness contract, that the Binding
> full target was still red, or that the strict Agreement/TrustedIssuer
> integration existed only as uncommitted overlap. It also supersedes the
> earlier `7bb9e414…` core tip and the older list of open local flow-lifecycle
> limitations. Historical failures remain documented because they explain why
> the later gates are necessary.

## Current authoritative checkpoint — 2026-07-14

This section is the authoritative current checkpoint of the audit. It
supersedes every conflicting repository SHA, test count, defect status, or capability statement
in the chronological material below it. The chronology is retained as
red-before-green evidence and as a record of why the gates were added.

The correct top-level conclusion is **NOT PROVEN**: the audit repaired and
published a substantial set of concrete failures. Later waves found additional
P1 correctness defects in EntityScanner, Lobby, and RelationalLearning after an
earlier checkpoint had reported no concrete P0/P1. Those identified defects are
repaired and their reviewed gates are green, but the residual-risk ledger
remains authoritative. The audit did not prove all CellProtocol functionality,
every first-party repository, every live service, or every persistence and
restart path.

### Canonical Purpose and Goal result

No Purpose node was added. The existing canonical tree was sufficient:

- `purpose://quality` → `goal.haven.cross-repo.runtime-correctness`
- `purpose://test.acceptance` → `goal.haven.cross-repo.regression-gates`
- `purpose://access.audit.privacy` → `goal.haven.cross-repo.security-preservation`
- Existing facets were used only for routing: GUI functional quality,
  owner-entity access, and current project status.

| Goal | Current evaluation | Evidence closed | Why the HAVEN-wide target is not satisfied |
|---|---|---|---|
| `goal.haven.cross-repo.runtime-correctness` | **At risk / NOT PROVEN** | Shared decoded readiness, persisted cold-key restore, waitable connection mutation, runtime deep-link discovery, TrustedIssuer and Apple Intelligence hardening, explicit EntityScanner actions, deterministic Lobby publication, RelationalLearning's versioned journal, method-aware local Explore operations, proof-bound Chat actions, strict contract-before-handler publication in nine raw-intercept Cells, and a fresh strict Apple Intelligence 24-operation publication matrix | No clean full suite was run here on the exact current graph CellScaffold `8fb2c059…` + CellProtocol `0901692…`; remote method-aware Explore/wire parity, all-operation dispatch, broad live-service, separate-process, crash, and power-loss coverage are incomplete |
| `goal.haven.cross-repo.regression-gates` | **At risk / NOT PROVEN** | CellProtocol **756/756**, including Apple Intelligence **10/10**, RelationalLearning **14/14**, decoded-readiness **16/16**, and affected contract/readiness suites **59/59**; Explore regex/source audit **0 errors, 19 manually adjudicated false-positive warnings**; Explore auditor **11/11**; Binding 398 planned (378 passed, 20 explicit skips) plus runtime-surface gates; CellUtility 13/13; Python 35/35; shared Swift/Python/Rust fixtures | CellUtility UI runner is not runnable, fixture consumption is not CI-enforced across every runtime, comprehensive separate-process restart is absent, and top live user journeys were not all rerun on final SHAs |
| `goal.haven.cross-repo.security-preservation` | **Pass for changed paths; HAVEN-wide NOT PROVEN** | Wrong identity/key, proof-bearing admission, fail-closed restore/source behavior, outsider disconnect denial, atomic authorization decisions, exact RelationalLearning `-w--` action and `r---` read grants, no feed-injection grant, and draft-only Agreement editing | Full public proof issuance/session flows and live owner-published public-read paths remain incomplete in several runtimes; no audit may infer authorization from renderer, cookie, or private/admin fallback |

### Current repository publication and verification map

| Repository | Current audit SHA / state | Verification | Honest boundary |
|---|---|---|---|
| CellProtocol | `090169231d160e7efd723b3f8b8aa1958c6c816e`, published `origin/main` and `ls-remote` verified | `swift test`: **756 passed, 0 failed**; Apple Intelligence **10/10** with a 24-operation fresh strict publication matrix; affected suites **59/59**; strict contract-order regression **1/1**; Chat **56 handlers / 56 complete operation contracts / 0 findings**; repo Explore regex/source audit **0 errors, 19 manually adjudicated false-positive warnings**; auditor tests **11/11**; final advisers found no concrete blocker | The former 54 Chat warnings were scanner false positives, not weak production contracts. All 19 current Apple computed-key warnings are also exact-mapped false positives, but the scanner stays conservative. Local package proof is not deployment, all 24 handler dispatches, decoded 24-operation parity, permission/semantic parity for every operation, remote method-aware Explore/wire parity, every service, or separate-process/crash restore |
| Binding, including HavenAgentD | `2c295d8ce2ddf78562cc7541aa8f93132a77b8a7`, published `origin/main` and `ls-remote` verified | Binding full target: **398 planned, 378 passed, 20 explicit skips, 0 failed**; runtime-surface/scene slice passed; generic iOS Simulator `build-for-testing`: exit **0**; production EntityScanner uses the contracted boolean start payload and the suite is serialized against shared runtime state | Runtime mappings and catalog sources are configurable; scene-local dispatch is covered in-process. Remote-only cases, deployed owner-published launch, and a real Finder/browser cold launch remain bounded as recorded below |
| GoCellProtocol | `60476377f5f6efdeddde21c9f3b006fcc6756b41`, published `origin/main` | `go test ./...` passed | Owner-approved Agreement path is fail-closed; full proof/session and Swift parity remain **NOT PROVEN** |
| RustCellProtocol | `e5ea7e56d1f697c94660706786da9a6c76d015a2`, published `origin/main` | `cargo test` passed its unit and 27 integration tests; missing configuration UUID decode and the shared fixture mirror are covered | Automatic proof-bearing admission, CI-enforced checkout of the authoritative Swift fixture, and durable production parity remain **NOT PROVEN** |
| PyCellProtocol | `4ed979ccac685962246105e995de19ce0d1b6805`, published `origin/main` | `pytest`: **35 passed**; `pip check` clean; final adviser found no P0/P1 | Swift-origin wire roundtrip is covered, but live network, multiprocess, power-loss, protected remote sessions, and full parity are **NOT PROVEN** |
| SwiftWebScaffold | `89f6681ca0248a99114d462401b02557fe116b10`, published `origin/main` | Focused decoded-readiness/access suite passed | Public proof mint/session is not implemented; protected POST remains fail-closed, not silently public |
| CellUtility | local commit `b25841d31c50c763ba3f33914a46740c09187785` | Workspace and project entry points each ran **13 passed, 0 failed** against exact CellProtocol `7bb9e414…`; final adviser found no P0/P1 | Push is **BLOCKED**: `origin` is archived read-only `Digipomps/CellUtility-history-20260506`; remote `main` remains `cae2cadd9422388ba6866e577037f14117f0d03c` |
| CellScaffold | `origin/main` and `origin/m0/green-test-suite` were both `8fb2c05921bb548f9753779ec269e41645d77232` at this audit observation | This task made no CellScaffold write. Saved earlier dependency-snapshot suites each executed **1,358 tests, 9 skipped, 0 failed** | Those suites do not prove the exact current CellScaffold + CellProtocol `0901692…` graph or deployed user journeys. The separate release task owns the branch snapshot and final clean-graph verdict. Current HAVEN-wide robustness remains **NOT PROVEN** |

The remaining first-party inventory, including SpatialRegistryScaffold,
GUI/Chat, DiMy repositories, Add2Entity, HAVEN_MVP, sprout, WatchPong,
UniverseSimulation, documentation checkouts, archives, clones, and generated
dependencies, is recorded in the detailed inventory below. A repository being
inventoried is not equivalent to its user journeys being proven.

### Current CellProtocol repair wave

The current core sequence after the earlier release snapshot is:

- `494fa1f30f891b8b527270ab3724d797f73dcc0f`: cold persisted reads restore
  the scoped key before decode/access; transient state is not serialized; the
  authorization result remains tri-state and fails closed.
- `63f9659ec63e2a8d9034c129f33f49df71f23916`: additive waitable
  `detachAndWait` and `dropFlowAndWait` APIs remove host-side disconnect races
  without changing legacy protocol requirements.
- `2d4127982a247a826bc9e7a026a6b2320130d1dd`: leaf Emit connections appear
  in `attachedStatuses`, while nested Absorb child statuses retain their
  prefixes.
- `82595f1d0db638b139db320d6cd05b713aa52fee`: requester authorization is
  enforced for waitable disconnects, outsider mutation is rejected, and
  BridgeBase preserves the label in remote detach/drop wire commands.
- `7bb9e41419ed99ac6f769556ec81c714a0e82b4b`: the public detach operation
  makes one authorization decision and then performs private local cleanup,
  eliminating a TOCTOU window that could otherwise leave a hidden live
  subscription after its visible emitter label was removed.
- `bfc176ffecd4f718cd47e4a9db6183a2b0378def`: the complete local
  `GeneralCell` flow lifecycle is generation-isolated and resource-owned. It
  adds source-side `-w--` enforcement, per-label single-flight setup, shared
  terminal results, object-identity replacement even for the same UUID,
  canonical/cycle-safe status, ordered async intercept processing, a bounded
  256-event fail-closed buffer, exact-capacity completion handling, waitable
  forwarding-lease teardown, cancellation re-entry isolation, overflow
  self-heal that reloads the current emitter, and deinit cancellation that does
  not retain the Cell across suspended intercepts or blocked subscribers.
- `1bde79c7b9b207c828aad1a9786d3fa5fc90b6ca`: CellApple resolves a
  Skeleton button against its row first and then invokes an optional,
  host-local transform. The default remains a no-op, so portable wire schema
  and non-Binding renderers are unchanged.
- `306b51aac7d168af473f25634c46d423a729212a`: the transform closure is
  explicitly `@Sendable` and the wrapper uses checked `Sendable` conformance;
  the initially reviewed `@unchecked Sendable` escape hatch was removed.
- `caa4183d08da9b44b04f0db2aa00772e120da6e1`: TrustedIssuer evaluation now
  enforces candidate and recursive-source status, context, issuer-kind, and DID
  policy; invalidates graph-dependent current results after policy-source
  changes; bounds retained current/history caches and identifiers; normalizes
  cold-retained keys; verifies new SHA-256 and genuine legacy snapshots while
  dropping corrupt records; rejects malformed integer policy inputs and VC
  candidates over 1 MiB before cryptographic work. The exact proof-bearing
  evaluation exception remains narrow and admin mutations remain denied.
- `d9638de009a019b9dc93eb84a54f2532efb21f17`: Apple Intelligence now has
  Codable-persisted, round-trippable, retention-bounded logical runtime state
  with immediate post-decode contracts;
  read-only state fields cannot be mutated through root dispatch; request tools
  preserve the actual requester; sensitive outbox/tool diagnostics and dequeue
  stay cryptographically owner-only even for signed non-owners; a signed
  non-owner cannot use the public bootstrap helper to clear private state,
  while an owner reset atomically invalidates an in-flight discovery
  generation. Action results no longer claim success when
  purpose/cluster work is unavailable, discovery is generation-isolated, and
  prompt plus optional response enqueue atomically. The advertised `ai.send`
  schema and runtime accept only object/string/data; every corresponding outbox
  entry includes an ID and survives real `ValueType` to `FlowElement` decode,
  encode, and decode. Richer internal values are object-wrapped rather than
  mislabeled on the wire.
- `e84cf485a9757dd079a1bf223addb4447b2496f9`: a versioned Swift-origin CellConfiguration wire fixture and
  runtime mirrors establish shared schema evidence for Swift, Python, and Rust.
- `55f927035cb349a945b13cd2c44f7380a24fe746`: strict Explore contracts must be installed before handlers, so
  advertised actions cannot remain weakly shaped or silently undispatchable.
- `9a8b4b717342cc9c2d3e29e98059ee9e1f56a751`: Apple and Vapor hosted Cells install strict contracts through the
  same decoded-readiness boundary.
- `f845db97e12aee0a2a2f2b3e1e44c834f7073f97`: EntityScanner replaces broad
  implicit behavior with explicit contracted state/actions, exact grants, real
  production payload tests, and stable decoded readiness.
- `080bb934bf4457ac59a1fe7679d598b2beaf4bc7`: Lobby publication becomes
  deterministic, exposes public purpose reads only through an owner-authorized
  signed `r---` Agreement, and keeps purpose updates owner-only.
- `d9d95145fc67910d2b4242c78af0ccc30cdabd6d`: RelationalLearning installs ten
  explicit strict contracts, normalizes action/read grants, persists a
  versioned sequenced journal, restores supported state/actions immediately
  after decode, rejects malformed, mismatched-edge, and unsupported events
  without partial mutation, derives deterministic SHA-based weight-event IDs,
  serializes action/journal/flow order, and separates authorized action
  execution from feed-injection authority.
- `74d89b49a0fc991415f507d5b0c0063f9e65ffc4`: local Explore publication and
  strict enforcement become operation-aware by `(key, method)` without
  removing legacy methodless schemas. This closes the four real Chat
  GET/SET single-slot collisions at `audience.mode`, `crypto.persistenceMode`,
  `compose.body`, and `compose.contentType`; adds canonical SET operations for
  `start` and `stop`; and preserves the deprecated mutating GET aliases as an
  explicit compatibility residual. Chat now publishes 56 complete operations
  over 50 keys, including six dual-method keys. The same repair prevents an
  exact child grant from reaching a legacy root handler, binds envelope opening
  to the live requester's proof/signing identity/Agreement, rejects bulk target
  payloads atomically when any target is invalid, and emits flows through
  Cell-owned authority. It does not claim a new remote wire protocol.
- `8e2196478fd9a4b8f5de2b53ff9e707d8ea3d2c7`: a corrected source auditor
  exposed 60 real strict-order errors across nine raw-intercept Cells:
  Perspective, CommonsResolver, CommonsTaxonomy, EntityAtlasInspector,
  FileCrypto, ContractProbe, GraphIndex, Vault, and Identities. Each now
  publishes its complete contracts before installing handlers. A production
  strict-mode regression instantiates all nine and proves one representative
  expected key per Cell remains installed; the source audit, not that runtime
  test, accounts for all 60 repaired handler operations.
- `090169231d160e7efd723b3f8b8aa1958c6c816e`: every Apple Intelligence
  `(key, method)` mapping behind the 19 conservative source warnings was
  manually adjudicated, then guarded by a fresh-Cell strict publication matrix:
  exactly 24 contracts, no duplicates, complete non-unknown input/return
  schemas, and all 20 expected keys installed. The adviser also found that two
  SET return descriptions incorrectly promised raw echo values while handlers
  return confirmation-prefixed strings; the descriptions now match behavior.
  The externally visible `New promtpt text:` typo is intentionally corrected
  to `New prompt text:`; no first-party exact-string consumer was found.

Closing evidence for this core checkpoint:

```text
swift test --filter RelationalLearning
# 14 tests, 0 failures

swift test --filter CellRuntimeReadinessContractTests
# 16 tests, 0 failures, including the Vapor-named matching suite

swift test --filter \
  'CellRuntimeReadinessContractTests|RealCellContractTests|ContractProbeCellTests|FileCryptoCellTests|GraphIndexCellTests|VaultCellTests|IdentitiesCellContractTests|CommonsCellsTests|EntityAtlasInspectorCellTests'
# 59 tests, 0 failures

swift test --filter AppleIntelligenceCellContractTests
# 10 tests, 0 failures; includes fresh strict 24-operation publication matrix

swift test
# 756 tests, 0 failures

python3 .../explore_contract_audit.py \
  --repo-root .../cellprotocol-chat-hardening \
  --source-dir Sources/CellBase/Cells/Chat --fail-on-error
# 56 handlers, 56 complete contracts, 0 errors, 0 warnings

python3 .../explore_contract_audit.py \
  --repo-root .../cellprotocol-chat-hardening --fail-on-error
# 277 handlers, 273 complete contracts, 0 errors, 19 manual-review warnings

CELLPROTOCOL_REPO=.../cellprotocol-chat-hardening \
  python3 -m unittest discover -s Tools/Explore/tests -v
# 11 tests, 0 failures

git diff --check
# clean

git ls-remote origin refs/heads/main
# 090169231d160e7efd723b3f8b8aa1958c6c816e
```

The red-before-green regressions prove more than happy-path status:

- an outsider cannot pause or detach the owner's connection;
- a one-shot cell-specific policy cannot authorize label removal while a
  second check denies subscription cleanup;
- no post-detach event leaks from a hidden cancellable/subscription;
- remote bridge commands encode both operation and exact label;
- parent status, leaf status, active/inactive transition, and final detach are
  observable only after the waitable operation returns.

The final independent core advisers found no concrete P0/P1 after these
repairs. The adviser loops caught and closed stale same-UUID emitter capture
across overflow cleanup, an auditor/resource retain cycle while a downstream
subscriber was synchronously blocked, a signed-non-owner Apple bootstrap
bypass, and advertised Apple outbox types that did not survive a `FlowElement`
wire roundtrip.

Current non-P1 boundaries are narrower and explicit:

- generation isolation is not global transaction serialization; a new local
  generation may start while old external cancellation finishes, but the old
  generation cannot mutate the new one;
- the 256-event bound is local `GeneralCell` forwarding behavior, not universal
  transport backpressure;
- waitable local teardown is not proof that a live remote peer acknowledged the
  mutation;
- generic `FlowElement` does not itself guarantee signatures, timestamps,
  global sequence, durable storage, or exact replay;
- the package suite is not deployment, process-restart, renderer, or
  cross-language evidence.

Exact closing evidence:

```text
swift test --filter IntegrationTests
# 35 passed, 0 failed

swift test --filter GeneralCellInterfaceTests/testSequentialAttachRequestsDoNotMutatePublishedAgreementTemplate
# 1 passed, 0 failed

swift test
# 718 passed, 0 failed

swift test list
# 718 discovered tests

swift test --filter AppleIntelligenceCellContractTests
# 9 passed, 0 failed

swift test --filter CellRuntimeReadinessContractTests/testAppleAndVaporDecodedCellsAreImmediatelyAndConcurrentlyReady
# 1 passed, 0 failed

python3 /Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Tools/Explore/explore_contract_audit.py --repo-root /private/tmp/haven-robustness-cellprotocol --source-dir Sources/CellApple/Intelligence
# 0 errors, 0 warnings

git diff --check
# clean

git ls-remote origin refs/heads/main
# d9638de009a019b9dc93eb84a54f2532efb21f17
```

### Final CellUtility repair wave

CellUtility now:

- uses one single-flight, retryable readiness state and blocks supported state,
  action, configuration, and connection operations until ready;
- loads runtime CellConfiguration sources serially and preserves valid files
  when sibling files fail, while an all-invalid known-nonempty required source
  fails instead of rendering a false empty state;
- restores an encrypted persisted OrchestratorCell with the same UUID, owner,
  scoped SHA-256 key, supported keys/state, and immediate get access after
  clearing the master key and resolver runtime state;
- uses waitable connection mutation and shows completed status before returning;
- traverses arbitrary-depth `parent.child` status paths to the GeneralCell that
  owns the leaf, so selection, pause, resume, and detach do not become root-level
  no-ops;
- keeps Agreement interaction draft/review/dismiss only; it does not manufacture
  owner authorization, sign, accept, decline, or retry admission;
- reports operation failures visibly and removes optimistic UI toggles;
- uses a relative workspace reference and pins the project plus both identical
  lock files to CellProtocol `7bb9e41419ed99ac6f769556ec81c714a0e82b4b`.

Both exact commands succeeded:

```text
xcodebuild test -workspace CellUtility.xcworkspace -scheme KeychainUtility \
  -destination 'platform=macOS' \
  -clonedSourcePackagesDirPath /private/tmp/cellutility-sourcepackages \
  -disableAutomaticPackageResolution CODE_SIGNING_ALLOWED=NO

xcodebuild test -project CellUtility.xcodeproj -scheme KeychainUtility \
  -destination 'platform=macOS' \
  -derivedDataPath /Users/kjetil/Library/Developer/Xcode/DerivedData/CellUtility-fwpxmenjvyijbicbxcbmylwgcexw \
  -clonedSourcePackagesDirPath /private/tmp/cellutility-sourcepackages \
  -disableAutomaticPackageResolution CODE_SIGNING_ALLOWED=NO
```

Each executed 13 passing unit tests. Eleven are meaningful gates; two are the
unchanged Xcode example/performance templates. The UI target was skipped in
both commands because `UITargetAppPath` is not configured. The cold-reload test
simulates restart by resetting runtime state in one process; it is not a real
second executable process. Production `configureRuntime`, default
machine-specific configuration discovery, crash-atomic persisted JSON writes,
and end-to-end GUI use therefore remain **NOT PROVEN**. A literal dot in a
connection label is currently indistinguishable from the nested-path separator;
no production occurrence was found, so this is residual rather than a P1.

The commit is intentionally preserved even though publication failed:

```text
b25841d31c50c763ba3f33914a46740c09187785
Harden CellUtility runtime readiness and recovery
```

GitHub confirmed `archived: true`; the push error was `This repository was
archived so it is read-only.` Selecting or creating a replacement repository,
or unarchiving this one, is an external ownership decision for Kjetil and was
not guessed by the audit.

### Runtime-configurable deep-link decision

The published Binding design remains the accepted implementation. External
links carry a stable schema, opaque `surfaceID`, and view intent. Runtime
catalog sources resolve the ID; compiled code does not define the mutable
surface mapping. Source configuration is controlled by
`BINDING_REMOTE_CATALOG_ENDPOINTS`,
`BINDING_INCLUDE_DEFAULT_REMOTE_CATALOG`, and
`BINDING_DEFAULT_REMOTE_CATALOG_ENDPOINT`. Ambiguity and protected-source
failures fail closed. The route is not identity, proof, capability, or
authorization. Binding `c0054360a364599cd472ab2094282a739baa5698`
additionally binds every adapted runtime-surface button to the originating
scene UUID, recursively covers presented containers plus delegated
List/Reference row templates, and preserves the adapter
endpoint/keypath/payload after row resolution. A hostile row therefore cannot
replace the scene token or turn a view-only route into another action. The host
hook is local Environment state, not wire schema or authority. A full
Finder/browser cold launch into a fresh Binding process and a deployed
owner-published catalog journey are still **NOT PROVEN**.

Exact final Binding evidence against published CellProtocol
`306b51aac7d168af473f25634c46d423a729212a`:

```text
xcodebuild build-for-testing -quiet -project Binding.xcodeproj -scheme HAVEN \
  -destination 'platform=macOS,arch=arm64' \
  -derivedDataPath /private/tmp/BindingSceneLocalDerivedData \
  -parallel-testing-enabled NO

xcodebuild test-without-building -project Binding.xcodeproj -scheme HAVEN \
  -destination 'platform=macOS,arch=arm64' \
  -derivedDataPath /private/tmp/BindingSceneLocalDerivedData \
  -parallel-testing-enabled NO -only-testing:BindingTests
# /private/tmp/BindingSceneLocalFull2-20260714T0554.xcresult
# 398 total: 378 passed, 20 skipped, 0 failed

xcodebuild test-without-building ... <eight exact runtime-surface selectors>
# /private/tmp/BindingSceneLocalTargeted3-20260714T0555.xcresult
# 8 passed, 0 failed

xcodebuild build-for-testing -quiet -project Binding.xcodeproj -scheme HAVEN \
  -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath /private/tmp/BindingSceneLocalIOSDerivedData \
  -parallel-testing-enabled NO
# exit 0

git ls-remote --heads origin main
# c0054360a364599cd472ab2094282a739baa5698
```

The repeated Xcode messages about a passcode-protected physical device were
unrelated to the explicit macOS and generic iOS Simulator destinations. The
terminal command and `.xcresult` outcomes above, rather than those warnings,
determine the gate.

### Final adviser findings and closure decisions

The last adversarial pass caught four defects after earlier green suites:

1. waitable disconnect initially ignored requester authorization;
2. CellUtility displayed nested leaf status but sent mutations to the root;
3. BridgeBase discarded the detach/drop label on the wire;
4. the first authorization fix double-checked across an await boundary and
   could leave a hidden subscription under a changing policy.

All four received a red regression, a lowest-layer repair, a full relevant
suite, and a final read-only review. The subsequent GeneralCell flow review
then found and closed dropped completion at exact buffer capacity,
post-overflow forwarding, slow-intercept/resource retention, setup-overflow
result disagreement, cross-thread lock/actor deadlock, stale delivery after
detach, cancellation callback re-entry, detach-before-late-setup disagreement,
same-UUID stale emitter capture, and blocked-subscriber auditor retention.
That adviser result closed its then-current snapshot, but later Purpose-driven
waves found real EntityScanner, Lobby, and RelationalLearning defects. Those
later advisers required strict contract shape, deterministic publication,
journal persistence, atomic replay, operation serialization, relation/node
integrity, and emitter-factory access negatives before issuing a final `SHIP`
verdict for the RelationalLearning commit. The Binding review specifically caught presentation,
List, Reference, row-override, and unchecked-Sendable gaps before publication.
The first final Binding run then produced a false green with only 347 of 398
planned tests; explicit selectors exposed one incorrect test expectation. After
correcting that expectation to match production's deliberate suppression of
deferred presentation fields, the eight targeted tests passed and a second
full run planned all 398 tests with 378 passes, 20 explicit skips, and no
failure. This demonstrates why a green result without count and contract
inspection was insufficient evidence.

The final Explore adviser independently reran the corrected tool on exact
CellProtocol `8e219647…`: auditor tests were 11/11, Chat was 56 handlers / 56
complete contracts / 0 findings, and the repository was 277 handlers / 273
explicit-shape contracts / 0 errors / 19 computed-key warnings. Running the
same auditor on parent `74d89b49…` reproduced exactly 60 strict-order errors.
The adviser found no code blocker in the nine ordering moves, but required the
runtime claim to stay at one representative key per Cell and required the Book
to document that the auditor is regex/static: it cannot prove conditional
dominance, early-return or deferred-Task behavior, overloaded helpers, runtime
schema validity, permission alignment, or flow-effect correctness.

The Apple follow-up adviser mapped all 19 remaining warnings to 24 exact
operations and found zero missing mappings. It reviewed `090169231…`, reran
Apple **10/10**, and found no code blocker. Its required boundary is narrower
than “all handlers proven”: the matrix covers fresh local strict publication,
exact membership/count, non-unknown input/return shapes, and installed keys. It
does not dispatch all 24 handlers, verify every permission/required/semantic
return, repeat the 24-operation matrix after decode, or prove remote transport.

### Current C1–C6 adjudication

| Claim | Current evaluation | Support and counterargument |
|---|---|---|
| C1 | **Supported across multiple hosted Swift Cells; not universal** | Real core/Scaffold/Binding/host cases establish the class. Synchronous constructors and Cells with no decoded runtime bindings are counterexamples. |
| C2 | **Supported, not exclusive** | Detached decoded setup and non-waitable disconnects produced immediate-read/action/status failures. Authorization denial, source outage, bad keypaths, and legitimate empty datasets remain alternate causes. |
| C3 | **Accepted for supported host access and mutation boundaries** | Hosts await optional readiness and waitable mutations; RelationalLearning restores its own journal/contracts behind that boundary while app semantics remain in the Cell. This is not a mandate to push application semantics into protocol core. |
| C4 | **Accepted** | Old green tests coexisted with empty/broken production behavior and later permitted RelationalLearning state loss, method-blind Explore collisions, late strict contract publication, nondeterministic IDs, and unsafe replay. Real payload, cold reload, exact `(key, method)`, registration-order, negative access, and known-data tests caught failures. The former 54 Chat warnings were separately adjudicated as scanner false positives rather than promoted to defects. |
| C5 | **Accepted and preserved in changed paths** | No admin/cookie/private fallback was added. RelationalLearning action grants do not grant feed injection; Chat decrypt binds live proof, signing identity, and Agreement; exact child grants cannot reach legacy root handlers; outsider, wrong-key, proof, Agreement, and fail-closed source cases remain enforced. |
| C6 | **Partially supported as a testing strategy, not proven as full capability** | Shared Swift/Python/Rust wire fixtures plus runtime-specific tests catch schema drift, but Relational journal/ID parity and authoritative fixture checkout are not CI-enforced across all runtimes; lifecycle, resolver security, persistence durability, renderer parity, and live transport remain outside fixture proof. |

### Precise current **NOT PROVEN** statement

This audit does **not** prove:

- that all CellProtocol functionality or every first-party HAVEN repository is
  robust;
- that current CellScaffold `8fb2c059…` is green on the exact current
  CellProtocol `0901692…` dependency graph; two earlier dependency snapshots
  have clean 1,358-case suites, but they are not silently promoted to final-graph proof;
- a real process restart for every persisted Tier-1 Cell, crash/power-loss
  durability, or simultaneous multi-process access;
- a complete live bridge/WebSocket detach/drop roundtrip with remote denial;
- universal FlowElement signing/sequencing, durable replay, transport-level
  backpressure, or remote teardown acknowledgement;
- bounded allocation while decoding a hostile persisted TrustedIssuer payload,
  a signed append-only TrustedIssuer audit trail, VP challenge/domain checks,
  attestation-proof verification, or fixed-time deterministic trust replay;
- bounded allocation before decoding hostile persisted Apple Intelligence
  candidate/outbox collections; the repair bounds retained state after decode,
  but `Codable` materializes the input first;
- live Foundation Models availability, model-output correctness, a deployed
  Apple Intelligence user journey, or a production host that drains the
  owner-only outbox through its explicit dequeue contract;
- that every CellProtocol Explore contract is complete or schema-aligned. The
  corrected repo-wide source audit emits **0 errors and 19 warnings** under its
  regex/static model; all 19 Apple computed-key warnings are manually mapped
  false positives and the fresh strict 24-operation publication matrix is
  green, but all-operation dispatch, decoded parity, and per-operation
  permission/semantic-return checks are not complete;
- remote Bridge `Explore.typeForKey(key:)` or any cross-runtime wire consumer
  can discover both methods for a dual-method key. Method-aware strict dispatch
  and catalogs are proven locally, but remote operation-aware Explore/wire v2 is
  **NOT PROVEN** and was not invented in this repair;
- that every mutating operation is SET-only: Chat's canonical `start` and
  `stop` operations are SET, but their mutating GET aliases remain deprecated
  compatibility behavior;
- a RelationalLearning restore in a separate executable/process, durable
  container, crash, power-loss, or simultaneous multi-process access;
- bounded hostile allocation before `JSONDecoder` materializes a persisted
  RelationalLearning journal, or long-running journal saturation, compaction,
  and archive behavior;
- cross-runtime deterministic RelationalLearning IDs/journal replay through a
  shared golden fixture, arbitrary replay-versus-incoming-flow concurrency, or
  journaling for legacy direct engine mutation APIs;
- a precise Explore declaration of conditional lifecycle-generated
  `weightUpdate` flow effects; the current schema cannot express an optional
  effect with minimum count zero;
- a full OS cold-launch deep link, deployed owner-published runtime launch,
  every Binding remote-only path, or current web/native renderer parity on
  deployed production payloads;
- CellUtility UI behavior, production runtime boot, or remote publication;
- public proof minting/session establishment and full Agreement/capability
  parity across Go, Rust, Python, and SwiftWeb;
- current Workbench, Arendalsuka Participant/Event Atlas, Conference, Co-Pilot,
  and every other Tier-1 user journey on the final published dependency graph;
- that an archived CellUtility remote contains the local verified commit.

These are explicit evidence or ownership gaps, not inferred passes. The three
Goals therefore remain non-terminal at HAVEN-wide scope. Kjetil owns the
CellUtility repository decision and the separate CellScaffold release task owns
the final clean full-suite verdict.

## Earlier release continuation and audit chronology — 2026-07-14

### Published release state

| Repository | Published `origin/main` | Release contents | Remote verification |
|---|---|---|---|
| CellProtocol | `0ef84bcfbb81d2e112e961719821ed218cf95169` | Strict Agreement admission; optional decoded-runtime activation; complete resolver test reset; identity-scoped restore; proof-bearing TrustedIssuer admission; Porthole resolver-race crash guard | `git ls-remote origin refs/heads/main` equals local release HEAD |
| Binding, including HavenAgentD | `d8933b72bbcb94eae7f04abad3806e03c614247d` | Runtime-driven deeplink/catalog discovery; scene/window-local queued delivery; fail-closed bootstrap; decoded hosted-Cell readiness; partial source recovery; identity/proof retry; HavenAgentD readiness and CellProtocol pin | `git ls-remote origin refs/heads/main` equals local release HEAD |
| CellScaffold | `52d6de28ba42159432f5bb3cd6576db3ec890c6d` on `main`; `90d10a0efda7d213a5649033ce42227c9dd89f08` on `m0/green-test-suite` when observed | Owned by the separate release-coordination task | Read only; this continuation made no CellScaffold edit, commit, push, or deploy |

CellProtocol was delivered in five ordered commits after the earlier audit
snapshot:

- `543af37` — strict, owner-authorized Agreement admission and persisted
  authorization behavior.
- `ef74000` — shared decoded-runtime activation and identity verification.
- `6d4df4c` — complete DEBUG test reset for resolver registries, auditor, and
  lifecycle tracker.
- `780df47` — identity-scoped restore and the narrow proof-bearing
  TrustedIssuer admission path.
- `0ef84bc` — Porthole view-model availability handling during resolver races.

Binding was delivered in two commits:

- `44d4da78` — hosted-Cell readiness, runtime-configured deeplink/catalog
  sources, bounded scene-local delivery, fail-closed bootstrap, live partial
  source recovery, and regression gates.
- `d8933b72` — HavenAgentD decoded readiness plus an exact remote fallback pin
  to CellProtocol `0ef84bc`.

### Lowest-layer repair now in CellProtocol

The earlier report correctly rejected putting application-specific setup in
the protocol core. Later source and compatibility evidence justified a smaller
shared mechanism: an optional activation hook for Cells that actually need
runtime reinstallation.

`GeneralCell.ensureRuntimeReady()` now provides single-flight, retryable,
idempotent activation around the overridable
`installCellRuntimeBindingsForAccess()` hook. Cells with only synchronous
decoded state remain no-op by default. The runtime awaits this contract at the
supported generic access and persistence boundaries, including Cell
encode/decode/storage, resolver delivery, and state/action dispatch. Concrete
shared Cells that had detached decoded setup moved their runtime binding work
into the hook. This is a lifecycle mechanism, not permission policy: Agreement,
owner proof, resolver, and per-Cell access checks still decide authority.

The release also closes the test-only full-suite contamination reported by the
CellScaffold release task. `CellResolver.resetRuntimeStateForTesting()` now
clears named resolves, facilitators, auditor state, and lifecycle state. The
reset is DEBUG SPI for tests; production lifecycle semantics are unchanged.

### Agreement and TrustedIssuer security preservation

The earlier owner-published Agreement regression is no longer merely a dirty
worktree overlap. Strict admission is committed and covered in CellProtocol.
During condition evaluation, recursive contract lookup still returns no
ordinary grants. `TrustedIssuerCell` therefore has one deliberately narrow
cell-specific exception:

- exact permission `-w--` only;
- root dispatch key `trustedIssuers` and exact intercept key
  `trustedIssuers.evaluate` only;
- requester must carry a cryptographically verifiable identity-control proof;
- policy, issuer, and attestation mutations remain denied to the same outsider.

The regression executes real `GeneralCell.addAgreement`, proves that a valid
trusted credential can satisfy `ProvedClaimCondition` during admission, proves
the evaluation side effect, and proves that no-proof, broader-permission,
child-keypath, policy, issuer, or attestation attempts fail without state
mutation. No admin cookie, implicit owner identity, renderer authorization,
private-state fallback, or broad public grant was introduced.

The final `caa4183…` continuation closed additional policy and retained-state
defects found by the adviser loop:

- an issuer registered only for context A can no longer be trusted in context
  B; an empty active context list is rejected rather than interpreted as global
  trust;
- inactive, wrong-context, wrong-kind, or unsupported-DID recursive attestation
  sources neither contribute score nor satisfy independent-source counts;
- changing an issuer or attestation invalidates every dependent current result
  conservatively, while wrong-kind untrusted results preserve runtime/round-trip
  parity;
- proof-bearing callers cannot grow `evaluations.current` with arbitrary
  unregistered issuers; current and history retain at most 512 valid records,
  identifiers are limited to 512 UTF-8 bytes, and encoded VC input is limited to
  1 MiB before cryptographic verification;
- new snapshots use sorted-key SHA-256, genuine legacy base64 snapshots remain
  readable, and corrupt snapshots are dropped during restore.

These are cache and policy guarantees, not an audit-log claim. The 512-entry
history can be churned and emits no signed append-only evidence. JSON decoding
also materializes the complete persisted arrays/maps before the post-decode
512-record normalization, so hostile-payload allocation before retention is
**NOT PROVEN bounded**. VP challenge/domain verification, attestation-proof
verification, fixed-time replay, and separately persisted signed audit
references remain proposal targets, not implemented capability.

### Binding runtime-configurable deeplinks

The external link is stable and contains intent, not compiled routing or
authority:

`haven://open?schema=haven.surface-launch.v1&surfaceID=<opaque-id>&intent=view`

The host resolves `surfaceID` through runtime-configured catalog sources. The
source list is controlled at runtime by:

- `BINDING_REMOTE_CATALOG_ENDPOINTS`
- `BINDING_INCLUDE_DEFAULT_REMOTE_CATALOG`
- `BINDING_DEFAULT_REMOTE_CATALOG_ENDPOINT`

Configured sources are all queried; one unavailable source does not suppress a
later healthy source. Ambiguous matches fail closed. A valid live result may be
used when a sibling source is denied, but protected remote state is never
replaced with an unreceipted cache or private/admin fallback. Production
Conference fallback fixtures were removed.

Delivery is bounded and host-local: each scene/window has a queue of at most 32
items, a 20-second deadline, bounded retry intervals, one-at-a-time leases,
token-checked acknowledgement/release, operation-generation invalidation, and
late-commit fencing. Query material is not logged. Runtime bootstrap returns a
Boolean and every production caller handles failure by stopping the load or
action; Root/Bootstrap show a retry surface rather than exposing a partially
initialized `ContentView`.

### Historical release verification ledger at `0ef84bc` / `d8933b72`

| Gate | Result | Evidence boundary |
|---|---|---|
| CellProtocol `swift test` at `0ef84bc` | **672 passed, 0 failed** | Full Swift package on the published release; no live deployment proof |
| Binding full `BindingTests` target | **307 passed in 12 suites, 0 failed** | Exact historical checkpoint snapshot; 20 remote-only cases are intentionally skipped when the remote sentinel is absent; artifact `/tmp/haven-binding-derived/Logs/Test/Test-HAVEN-2026.07.14_00-07-49-+0200.xcresult`. The superseding current result is 398 planned, 378 passed, 20 explicit skips, 0 failed; see the authoritative map above. |
| Binding runtime bootstrap focused gate | **4 passed, 0 failed** | Concurrent registration, shared result, bounded failure, fail-closed recovery |
| Binding deeplink focused gate | **12 passed, 0 failed** | Parser, queue, lease, timeout, retry, targeting, runtime discovery, ambiguity, and fail-closed behavior |
| Binding remote Skeleton parity | **18 executed: 15 passed, 3 explicit skips, 0 failed** | Exact checkpoint code against staging; artifact `/tmp/haven-binding-derived/Logs/Test/Test-HAVEN-2026.07.14_00-16-23-+0200.xcresult` |
| HavenAgentD `swift test --filter HavenAgentCellsTests` | **18 passed, 0 failed** locally and again through the remote dependency fallback | Clean fallback had no sibling CellProtocol; both `Package.resolved` and checkout HEAD were exactly `0ef84bcfbb81d2e112e961719821ed218cf95169` |
| `git diff --check` before each commit | passed | Patch integrity only |
| `git ls-remote` after push | CellProtocol `0ef84bc`; Binding `d8933b72` | Confirms branch tips at this historical checkpoint, not deployment. The superseding current tips are recorded in the authoritative map above. |

The final Binding adviser performed a fresh control-flow and production-call
scan after the last fail-closed rewrite and found no remaining P0/P1 in the
snapshot. It explicitly retracted an earlier stale-waiter concern after proving
that joiners return directly from the stored `Task<Bool>` and only the creator
clears it. The adviser made no source edits.

### Adviser-triggered findings that keep the HAVEN-wide Goals open

The final read-only Purpose and inventory pass found three concrete
CellScaffold occurrences that are still vulnerable on the inspected release
snapshot. They are persistent, catalog-published Cells whose decoded
initializers launch required binding installation in a `Task`, while they
conform to neither `PortholeRuntimeBindingEnsuring` nor the shared
`installCellRuntimeBindingsForAccess()` hook:

- `Sources/App/Cells/Media/MediaCollectionCell.swift`: decoded Task at lines
  49-68 and required key/intercept installation at 144-151; persistent
  registration is in `Sources/App/configure.swift:641`, and catalog publication
  is in `ConfigurationCatalogCell.swift:185`.
- `Sources/App/Cells/CellConfigurationStudio/CellConfigurationStudioCell.swift`:
  decoded Task at lines 35-50, grants at 77-87, and intercepts at 90-99;
  persistent registration is at `configure.swift:563`, and catalog publication
  is at `ConfigurationCatalogCell.swift:143`.
- `Sources/App/Cells/Participation/ParticipationHubCell.swift`: decoded setup at
  lines 61-82, grants at 112-151, and intercepts at 154-158; persistent
  registration is at `configure.swift:645`, and catalog publication is at
  `ConfigurationCatalogCell.swift:174`.

This distinction matters: `GeneralCell.keys()`, `get`, and `set` await the
shared coordinator, but the default installation hook is intentionally empty.
The Porthole helper likewise returns immediately when the app-specific optional
cast does not match. A generic await therefore cannot install subclass
semantics that the subclass has not exposed. `EventAdmissionVerifier`,
`EventAdmissionIssuer`, legacy `ConferenceCell`, and `SQLiteCell` remain
unclassified candidates rather than asserted defects.

The latest available CellScaffold full-suite artifact is also red. In
`/private/tmp/cellscaffold-full-0ef84bc-r1.log`, the run at 2026-07-14 00:02
executed 1,356 tests with 9 skipped and 72 failures, 11 unexpected.
`WorkbenchAccessGrantConfigurationTests` alone executed 21 tests with 5
failures, including `ownerAuthorityUnavailable` and a target owner absent from
the correct home vault. This is access/fixture/runtime evidence, not evidence
that the readiness race caused the Workbench failures. The CellScaffold release
task has materially changed its dirty snapshot since that run; only a newer
clean full suite may supersede this artifact.

The cross-language adviser found that green local unit suites are not enough to
claim protocol parity or production-safe authorization:

| Runtime/repo snapshot | Current executable evidence | Concrete result and boundary |
|---|---|---|
| GoCellProtocol clean `main` `c686d0d` | `go test ./...` | **passed**; nevertheless caller-supplied Agreement admission, unsynchronized scoped resolution, legacy permission wire forms, and unconstrained remote signing remain open P1s |
| RustCellProtocol clean feature branch `35f7732`, four commits ahead of `origin/main` | `cargo test --all-targets` | **23 passed, 0 failed**; the unshipped branch still exposes direct Cell access outside resolver policy, non-cryptographic Agreement replacement, legacy permissions, and only in-memory persistence |
| PyCellProtocol dirty `main` worktree at `1a4b3c9` | `pytest -q -p no:cacheprovider` | **29 passed, 0 failed** on the dirty snapshot only; UUID-derived signing material, permissive `validate_access`, unlocked scoped resolution, and absent durable restore mean the port must not be treated as security-capable |
| SwiftWebScaffold clean `main` `ac6627e` | existing focused decoded-readiness tests; current clean dependency run not yet established | `ScaffoldInfoCell` has a real readiness contract, but public request `identityContext` can select an identity that the server vault loads or creates without proof binding the HTTP caller; dependency selection also prefers a sibling checkout and otherwise tracks unpinned `main` |
| CellUtility clean historical `main` `cae2cad` | no meaningful readiness/restart/security gate found | host startup and configuration loading use unawaited Tasks; Agreement save uses an empty Cell name; zero conditions can create an invalid closed range; dependency sources conflict |

The SwiftWebScaffold verification attempt in this wave first failed against the
dirty primary CellProtocol checkout because an untracked verifier source was
referenced but not included in the build snapshot. A second attempt explicitly
pointing at the clean release worktree failed before compilation because SwiftPM
derived the temporary directory name `haven-robustness-cellprotocol` as the
package identity while targets require `CellProtocol`. Neither failure is
accepted as a SwiftWeb product failure or a green test; reproducible dependency
selection is itself part of the pending repair.

### Historical Goal checkpoint — superseded by the final closure snapshot

| Purpose | Goal | Status at this checkpoint | Newly closed evidence | What kept it non-terminal |
|---|---|---|---|---|
| `purpose://quality` | `goal.haven.cross-repo.runtime-correctness` | **At risk / not satisfied** | Shared CellProtocol activation was published; full core was 672/672; Binding was 307/307; HavenAgentD remote fallback was 18/18; no concrete P0/P1 was found in the reviewed core/Binding diff and exercised paths at this checkpoint | Three concrete persistent/catalog CellScaffold readiness P1s, the checkpoint's red CellScaffold full suite, cross-runtime host/access defects, process-restart gaps, and product/service paths not rerun on that release |
| `purpose://test.acceptance` | `goal.haven.cross-repo.regression-gates` | **At risk / not satisfied** | Red-before-green readiness, concurrent single-flight, full resolver reset, exact action/read, wrong-key, deep-link negative, remote parity, full core, and full Binding gates were green | The available CellScaffold full suite was red at this checkpoint; three remote parity paths were explicit skips; no OS cold-launch deeplink, comprehensive separate-process restart, or single shared Swift-origin cross-runtime fixture |
| `purpose://access.audit.privacy` | `goal.haven.cross-repo.security-preservation` | **Pass only for the published CellProtocol/Binding repair paths; HAVEN-wide not satisfied** | Strict Agreement admission and proof-bearing TrustedIssuer evaluation are published; policy/issuer/attestation mutation remains denied; protected Binding catalog/cache paths fail closed | Go/Rust/Python/SwiftWeb security findings, previously reported CellScaffold device-ingress and relay-capability questions, and missing live owner-published public-read/catalog evidence remain open |

No new Purpose node was needed. The canonical tree already contains the three
root nodes and the relevant GUI, owner-entity-access, and project-status facets;
there is no unmatched intent requiring `purpose://prompt.unknown`.

### Claim re-evaluation after the release continuation

| Claim | Current evaluation | New evidence / retained counterargument |
|---|---|---|
| C1 | **Strongly supported for multiple hosted Swift Cells; not universal** | Core, Scaffold, Binding, HavenAgentD, and service candidates established the class; synchronous Go/Rust/Python construction and no-op synchronous Cells remain counterexamples |
| C2 | **Strongly supported, not exclusive** | Real decoded `notFound`, duplicated grants, empty-source risk, and pre-ready host reads were reproduced; Agreement denial, source outage, bad keypaths, and legitimate empty data remain alternate causes |
| C3 | **Accepted and now enforced at the lowest shared optional boundary** | Generic core access/persistence/resolver paths await `ensureRuntimeReady`; synchronous Cells pay only the no-op default; application semantics remain in the Cell |
| C4 | **Accepted** | Old parity passed beside decoded failure; the final gates execute production Cells, payloads, actions, concurrency, and remote surfaces |
| C5 | **Accepted and preserved in the published release** | UUID plus signing-key proof, strict Agreement admission, exact TrustedIssuer exception, and fail-closed remote/cache behavior; HAVEN-wide device/relay questions remain outside this release |
| C6 | **Partially supported as a strategy; current capability is not proven** | Shared wire fixtures can guard schema compatibility, but not lifecycle, resolver security, concurrency, or rendering. Go/Python locks are stale, the Rust improvements are unshipped, and no common current golden corpus exists |

### Historical **NOT PROVEN** checkpoint after its green release gates

At this checkpoint, the report deliberately did **not** infer any of the
following from 672 core tests, 307 Binding tests, or the focused staging parity
run:

- that every CellProtocol feature, every first-party repository, every
  catalog-published Cell, or every persisted product path is robust;
- a real OS cold-launch deeplink from Finder/browser into a fresh Binding
  process;
- separate-process restart and durable-container reload for every Tier-1 Cell;
- live owner-Agreement multi-catalog failover or live selective-grant partial
  source recovery;
- the three skipped remote paths: owner-scoped Conference Participant Shell,
  direct grant-gated staging surfaces, and ConfigurationCatalog publication;
- an owner-published read-only ConfigurationCatalog projection. Current
  staging asks the foreign read-only client to sign a mixed owner-approval
  contract, so Binding correctly refuses to self-admit;
- a complete missing-proof, stale-proof, replay, revocation, and public-read
  matrix across every changed first-party path;
- a shared Swift-origin golden readiness/persistence fixture consumed by Go,
  Rust, and Python;
- deployment of the local CellScaffold release branch or resolution of every
  CellScaffold security finding. CellScaffold is owned by the separate release
  task and was read-only here;
- a green CellScaffold full suite. The checkpoint artifact executed 1,356 tests
  with 72 failures; its Workbench failures are owner-authority failures and
  must not be relabeled as readiness failures;
- readiness for every CellScaffold persisted/catalog-published Cell. A fresh
  read-only scan found `MediaCollectionCell`, `CellConfigurationStudioCell`,
  and `ParticipationHubCell` starting decoded `Task` setup without either
  `PortholeRuntimeBindingEnsuring` or an
  `installCellRuntimeBindingsForAccess()` override. Legacy `ConferenceCell`
  and Event Admission issuer/verifier types require the same classification.
  The default core hook is intentionally a no-op, so generic `get`/`set`
  cannot make those subclasses ready automatically;
- absence of P0/P1 defects outside the audited lifecycle, routing, Agreement,
  TrustedIssuer, resolver-reset, and Porthole-race paths.
- production-safe authorization in GoCellProtocol, RustCellProtocol,
  PyCellProtocol, or SwiftWebScaffold; the concrete findings above remain open
  until their negative tests and published fixes are green;
- a ready, durable, reproducibly built CellUtility host.

These are evidence gaps, not hidden passes. They remain in the residual-risk
ledger until the owning repository supplies the exact user-path, access, or
restart artifact.

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

Three additional production waves were completed after the earlier report snapshot. `ConferencePublicShellCell` and `DeviceRegistrationCell` were moved onto the same waitable, requester-proof runtime-binding contract. The notification path `ConferenceBroadcastStudio -> NotificationPolicy -> NotificationOutbox -> DeviceCallbackBridge` now restores decoded behavior without detached setup; a persisted pipeline test exercises the actual dependency chain after round-trip, and the direct Porthole, Personlog, Contact, Sales, Agent, and Vapor consumers await readiness.

The adjacent audit then confirmed four more real occurrences. `ContactEndpointCell` and `AgentConversationInboxCell` are production-persistent P1 paths; `PersonlogQuestionInboxCell` and `PersonlogJobProjectionCell` are currently P2 latent because no production registration was found. All four now start no decoded work, serialize runtime installation, and have real encode/decode/immediate-use coverage. Contact preserves and retires a known endpoint; Agent preserves and clears a known prompt; Personlog executes its real refresh/resync actions; 40 concurrent callers do not grow grants. A same-UUID/different-signing-key Contact requester can neither read private state nor retire the endpoint, and the owner subsequently observes unchanged state.

The same security review found a separate exposed P1 in the device HTTP ingress. All three staging POST routes are live, unauthenticated input is replaced with the trusted Scaffold identity, registration can overwrite caller-selected participant/device records, and callback ticket lookup is not bound to an enrolled device signing key. A signature alone is insufficient because the current Contact-style envelope verifies against the identity embedded by the caller. The correct repair needs owner-approved device enrollment that binds participant/device, signing-key fingerprint, audience, exact actions, expiry, revocation, and replay state. This audit did not introduce a shared secret, cookie/admin bypass, push-token authority, or auto-bless legacy registrations.

### Continuation: runtime-configurable deeplinks and Binding catalog readiness

Kjetil's follow-up requirement that deeplinks remain configurable at runtime is implemented without making the link an authorization channel. CellScaffold now owns one persistent, scaffold-unique `ScaffoldLaunchRegistryCell`. An owner publishes an opaque `surfaceID` mapped to a stable `CellConfiguration` lookup, revision, enabled state, and optional source endpoint. Readers still need an explicit Agreement. The canonical external form is view-only:

`haven://open?schema=haven.surface-launch.v1&surfaceID=<opaque-id>&intent=view`

The link carries no requester, token, action, endpoint, private payload, or capability. Safe `surfaceID` values now survive the unauthenticated login redirect. CellScaffold seeds default routes through a versioned bootstrap projection and reconciles remap and removal across persisted encode/decode re-instantiation without a detached decoded task. Both Porthole and Binding consume only `publishedRoutes`; an enabled but unpublished or legacy route fails closed.

Binding now adapts a real Skeleton `addConfiguration + surfaceLaunch` button to a Binding-local Cell rather than sending an invalid payload to Porthole. The adapter carries the actual Skeleton requester to the host, captures non-authoritative macOS window routing metadata, and rejects missing/mismatched targets so one click cannot navigate every `WindowGroup` window. Resolution is remote-first to prevent a local registry/catalog from shadowing the configured owner-published remote corpus. Only a configuration admitted from that same catalog corpus can be opened. The clean-snapshot gate executes the adapted `SkeletonButton` through the bootstrap-registered resolver endpoint and passes six focused tests.

Routes can therefore be added, revised, disabled, removed, and repointed through persisted Cell state without recompiling the host. The registry Cell type and bootstrap endpoint remain compiled infrastructure; arbitrary registry discovery is not claimed. The default public factory still contains direct compiled `configurationLookup` fallbacks. Switching those defaults remains blocked until the current core security wave supplies a tested owner-signed Agreement issuance path. The audit rejected both an app-local authorization workaround and the dirty `getOwner(requester:) -> locallyRestoredOwner()` hunk, which would expose proof-capable owner material to ordinary API callers.

The security adviser also found a separate P1 identity-link parser risk while reviewing the new URL boundary. Duplicate query names could trap during dictionary construction; arbitrary HTTP/S paths containing an identity-link substring were accepted; a new challenge did not clear all derived signing/completion state; completion was not bound to the exact locally signed request; and raw URL material could reach diagnostics. The Binding repair now requires exact custom routes, rejects duplicate/oversized/authority-bearing input, accepts only configured trusted audience/origin values for signing, caps TTL at one hour, clears derived state on challenge replacement, requires the exact request hash for completion, and logs a validated route summary rather than raw input. No universal-link HTTP/S route is accepted until a trusted association policy is implemented.

A second real Binding readiness occurrence was then confirmed in `ConfigurationCatalogCell`: decoded initialization launched grants, intercepts, metadata migration, and default bootstrap from an unawaited `Task`. The first regression failed because readiness reinstallation grew 69 persisted grants to 136. The Cell now inherits the Binding-local waitable runtime-binding boundary, starts no work from decoded initialization, serializes concurrent ensure calls, and normalizes exact `(keypath, permission)` grant contracts. The final production round trip performs twelve concurrent ensures followed by immediate non-empty configuration state and a real `matching.promptText` action with a stable Agreement.

Two further CellScaffold production paths were then repaired. `AccessRequirementPromptCell` no longer starts access-sensitive permission/action setup from decoded initialization. Direct Porthole lookup, including stale-mapping recovery, awaits the same serialized readiness gate before state or draft actions. Two decoded tests prove 40 concurrent awaiters, immediate real read/action, exact grant stability, and that the same UUID with another signing key can neither read nor mutate state before the real owner retries. The real blocked-reference Porthole bootstrap path and the common runtime-binding gate pass. The four unrelated pre-existing failures in the full `AccessRequirementPromptCellTests` class remain explicitly red and are not counted as readiness success.

`ArendalsukaEventAtlasCell` was the next adviser-ranked production defect: it is persistent, catalog-published, and read immediately by the participant source-preview path, while decoded initialization previously returned before `state`/`export`/action intercepts existed. The Cell now owns serialized readiness; Participant Program awaits it before requesting an owner-published read Agreement or reading export. The regression uses an encoded non-empty Atlas registered in the real resolver with journals disabled, and proves the participant preview sees all three known sessions from that same decoded Atlas instead of falling through to a new journal-backed instance. Owner state/export/action, 40-way idempotency, and wrong-signing-key read/write negatives pass.

`ConferenceAgendaCell` was the next source-proven application candidate. Its decoded initializer returned before agenda state and action intercepts were installed, while `ConferenceParticipantShellCell` resolved and immediately delegated agenda reads/actions. Agenda now uses the same serialized, retryable, exact-grant runtime binding contract and the shell awaits it before returning the dependency. Two decoded regressions prove persisted selection state, a real track-selection action, 40 concurrent ensures, stable grants, and same-UUID/different-signing-key read/write denial followed by an unchanged owner retry. Two real Participant Shell delegation/action tests also pass.

The next clean application candidate was CellScaffold's own `ChatCell`, not the separate shared `CellProtocol` Chat family. Its decoded initializer launched grant and key/action installation in a detached `Task`, could search or create a global `scaffold`/`Scaffold`/`private` identity, and was returned immediately by both the paid/authenticated HTTP host and Conference chat launch. Decoded Chat now restores state only, installs runtime handlers through the serialized requester-proof gate, and deliberately does not recreate persisted Agreement authority during activation. Both hosts await readiness after their existing authentication/payment checks. The regression covers 40 concurrent ensures, persisted known message/draft, immediate real `postMessage`, exact grant stability, same-UUID/different-signing-key read/write denial, a paid/authenticated encode/decode HTTP state/action/state path, and a decoded Conference chat backend. Five combined production-focused tests pass. The broader Chat class still has one pre-existing read-only Agreement test red under the active shared-core Agreement refactor; no bypass was added.

The current shared `CellProtocol` checkout contains a separate uncommitted security refactor owned by another workstream. Its new `GeneralCell.addAgreement` requires an authorization-enforcing template condition while the same refactor removes the default `GrantCondition`; the existing Arendalsuka owner-published public-read Agreement test therefore currently fails (empty preview, no final read grant). This audit did not weaken that policy or insert an admin/public bypass. The readiness commit is isolated; the Agreement policy integration is a P1 overlap that must be resolved by the core security owner.

These continuation changes are pushed as CellScaffold `b716d69`, `af9f24d`, `029a590`, `e7faabc`, `682dd18`, `bff5fea`, `16089c1`, `d451ccd`, `448fdcf`, `aa0149f`, `384c14a`, `106ccd6`, and `71854ce`; Binding `0a9752e7`, `b26fe5fb`, and `1fe09943`. No deployment was performed by this audit.

## Purpose tree and Goal evaluation

No new Purpose node was added. Canonical lookup found that the three requested existing nodes are sufficient for routing, ownership, security review, and termination. No unmatched intent justified `purpose://prompt.unknown` or promotion.

| Purpose | Goal | Current status | Evidence | Missing before terminal success |
|---|---|---|---|---|
| `purpose://quality` | `goal.haven.cross-repo.runtime-correctness` | **Open / partial** | CellScaffold catalog, Access Requirement Prompt, Arendalsuka Participant/Atlas, Conference Agenda/Shell, app Chat/HTTP/Conference host, Public Shell, Device Registration, notification pipeline, Contact/Agent/Personlog hosts, SwiftWeb, Binding chat/PersonalCopilot/catalog, all nine HavenAgentD Cells, Add2Entity, DiMy, and Spatial direct candidates repaired and tested; versioned published-only route projection and the native Binding button path pass focused gates | Remaining published-Cell classification; repair and deploy the authenticated owner-published runtime-launch path; default factory conversion after owner-signed Agreement issuance; explicit support policy for fatal-decode Cells |
| `purpose://test.acceptance` | `goal.haven.cross-repo.regression-gates` | **Open / partial** | Real round trips/actions across repaired areas; concurrent/idempotent installation; wrong-key read/write negatives; decoded non-empty source preview; one persisted notification dependency-chain reload; versioned route encode/decode re-instantiation and projection tests; real native Skeleton button -> resolver -> exact-requester test; strict deeplink/window/route negatives; 118-test HavenAgent package; selected dynamic paths and cross-language suites | Shared golden fixture; comprehensive separate-process restart gates; current public-read Agreement policy regression; device enrollment/proof negatives; browser artifacts; deployed macOS/web parity; full negative production-surface gate |
| `purpose://access.audit.privacy` | `goal.haven.cross-repo.security-preservation` | **Pass for committed readiness/deeplink changes; HAVEN-wide open / exposed device P1** | UUID+fingerprint owner matching; same-UUID/different-key read/write negatives; published-only route projection; opaque view-only launch references; the currently rejected Agreement path fails closed with no fallback/public bypass | Replace unauthenticated Scaffold-elevated device ingress with owner-approved enrolled-device capability/proof; resolve core Agreement-template overlap; missing/stale-proof cases; deployed wrong-identity runtime-launch proof |

`purpose://gui.quality.functional-accessible` and `purpose://skeleton.owner-entity-access` remain useful facets for later GUI and owner-access waves, but no new taxonomy was necessary in this wave.

## Audit method and classification

The static search targeted required `init(from:)` near `Task {}`, `Task.detached`, permission/key setup, intercept registration, Porthole endpoints, persistence, catalog publication, and immediate host reads/actions. A heuristic match is not itself a defect.

- **Vulnerable**: decoded setup is asynchronous, a supported host can read/act immediately, and no waitable gate is present.
- **Safe by construction**: setup is synchronous before publication/return, or decode is explicitly unsupported and cannot be published as persisted support.
- **Tested safe**: the production Cell and payload execute encode/decode plus immediate supported operations through a readiness gate, including concurrency where relevant.
- **Unknown**: a candidate exists, but publication/host/restart evidence is incomplete.

The bounded multi-line search found 23 matching CellProtocol source files and 110 matching CellScaffold source files. These are audit queues, not 133 asserted defects. Several matches are false positives, have narrower ownership, or are already covered by the Porthole ensuring adapter.

## Repository inventory and risk tiers at discovery time

This table is the chronological discovery/evidence snapshot used to route the
audit, not the authoritative final publication map. Its branch/HEAD and dirty
columns intentionally preserve the state observed when each repository entered
the audit; some rows therefore predate later repair commits. The exact final
published SHAs and verification results are recorded in **Final repository
publication and verification map** above and in the release ledger below.
Existing and concurrently arriving changes were preserved. CellScaffold
contained 7 audit files and 23 unrelated Butterpop, MusicPublishing,
PaymentGate, and Co-Pilot paths; the canonical documents checkout contained 19
pre-existing paths plus the 2 audit artifacts. Nested documentation checkouts
are listed as duplicates; `test/test` is a disposable clone and is excluded
from first-party modification scope.

| Repository | Role / dependency | Branch / HEAD | Dirty | Risk and evidence |
|---|---|---|---:|---|
| Binding | Native SwiftUI host, renderer, remote/deep-link and identity surface; includes HavenAgentD | `main` / `c0054360a364` | 10+ | **Tier 1, repaired for audited families.** Five workbench Cells, twelve PersonalCopilot subclasses, nine HavenAgentD Cells, and `ConfigurationCatalogCell` now have requester-aware readiness. A native Skeleton button routes through the Binding-local adapter with the actual requester, published-only remote-first catalog resolution, recursive presentation/List/Reference adaptation, hostile-row protection, and originating-scene targeting. The final full target plans 398 cases with 0 failures, the focused runtime slice is 8/8, and iOS Simulator compilation exits 0. Separate-process restart, deployed remote launch/OS cold start, and test-discovery repeatability remain open. |
| Binding/CellProtocolDocuments | Nested docs duplicate | `main` / `e138166d1cb8` | 0 | Excluded from canonical docs edits; primary docs checkout owns delivery. |
| CellProtocol | Swift reference contracts, resolver, persistence, identity | `main` / `8e96499ee216` | 20+ | **Tier 1, open policy and active overlap.** Adviser audit source-proved vulnerable shared `ChatCell`, Apple/Vapor Orchestrator/EntityAnchor, Calendar, Vault, GraphIndex, TrustPacket, TrustedIssuer, and Commons families; the existing Chat round-trip sleeps 20 ms after decode and masks readiness. Current unrelated security work also makes the Arendalsuka public Agreement gate fail. No audit edit was made in core. |
| CellProtocolDocuments | Canonical Book, security, Purpose, deliverables | `main` / `d8cff5d39fd8` before this report update | 20+ | **Tier 2.** Unrelated Book, Purpose-eval, RWXS, research, and deliverable work is preserved; only this canonical audit report is changed in the continuation. |
| CellScaffold | Porthole/web host, catalog, skeleton runtime, products | `m0/green-test-suite`; audit-owned `71854ceb6672`; later observed local `14b50a51fbfd`, upstream `e3d4049fbcdc` | 2 | **Tier 1.** Prior repaired paths plus versioned launch bootstrap, login forwarding, and published-only route projection are pushed and remain ancestors of both later heads. Runtime surface mapping is persisted and owner-published; default compiled button fallbacks remain pending owner-signed Agreement issuance. The public device POST ingress is an exposed P1 pending owner-approved enrollment/proof. The later security commits and current `Package.resolved`/PaymentGate edits are independent and were not staged by this audit. |
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

### D14 — Compiled deeplink destinations prevented runtime surface publication

Severity: P1 configurability/correctness and access-boundary risk

Status: published-only projection and native Binding button path repaired, tested, and pushed; authenticated remote Agreement path blocked

The prior startup and URL flows could select compiled configuration names or carry more routing detail in the external link. That couples launch behavior to host code and makes it tempting to put endpoints, identities, or authorization hints in a URL. `ScaffoldLaunchRegistryCell` now owns the mutable mapping from opaque `surfaceID` to a stable configuration lookup. Publication is owner-only and revision-checked; reads require an explicit Agreement; disabled, unpublished, legacy-missing-publication, and endpoint-only entries fail closed. Porthole and Binding read only `publishedRoutes`. Login forwards only a validated opaque `surfaceID`; it does not forward tokens, requester, action, endpoint, or capability material.

The registry has create/read, flow, encode/decode, concurrent readiness, wrong-identity/wrong-key, optimistic-concurrency, malformed-entry, versioned seed/remap/removal across same-process re-instantiation, and published-projection tests. The authenticated HTTP acceptance test is currently red because the overlapping dirty core rejects the legacy two-argument Agreement issuance; it is not treated as product-green evidence. Binding's clean-snapshot suite separately proves the real native button executes through the registered adapter/resolver and preserves the exact requester. `Explore` static audit reports zero errors and zero warnings for the registry Cell.

### D15 — Binding identity-link intake accepted ambiguous or stale security state

Severity: P1 security/correctness

Status: repaired and focused gates green

Exact route matching replaces substring matching; arbitrary HTTP/S links are rejected pending a trusted universal-link association; query names must be unique; URLs, payloads, and lists are bounded; raw link material is not logged. A replacement challenge clears signed and completion-derived state. Signing requires a trusted HAVEN audience/origin and a maximum one-hour TTL. Completion requires the exact hash of the locally signed enrollment request. These changes preserve the existing Identity/Agreement path and add no cookie, admin, renderer, or transport authorization.

### D16 — Binding ConfigurationCatalog repeated the decoded readiness race

Severity: P1 correctness/security

Status: repaired, red-before-green, and pushed

Binding's separate `ConfigurationCatalogCell` used an unawaited decoded `Task` for metadata migration, grants, intercepts, and default bootstrap. The first real production round-trip regression proved the Cell could reinstall duplicated contracts: 69 persisted grants became 136. The final implementation inherits `BindingRuntimeBindingCell`, routes fresh and decoded setup through one installer, starts no decoded work, and normalizes exact grant contracts. Twelve concurrent first callers share the install, then immediately read the non-empty production configuration list and execute the `matching.promptText` action. The final grant contract set is identical to the persisted set.

### D17 — Access Requirement Prompt could expose unbound access actions after decode

Severity: P1 access-sensitive correctness

Status: repaired, focused gates green, and pushed

`AccessRequirementPromptCell.init(from:)` launched permission and action registration in an unawaited `Task`, while the direct Porthole helper immediately read `state` or prefilled `loadRequirementDraft`. It now participates in the serialized runtime-binding contract, uses exact grant deduplication, and both the initial and stale-mapping recovery paths await readiness. A forged identity with the owner's UUID but another signing key is denied both the `state` read and a real mutation; the real owner can then retry and observe unchanged state. The full class remains red in four pre-existing Agreement/proof/configuration cases, so only the exact two readiness tests, common concurrency gate, and real Porthole bootstrap path are accepted evidence.

### D18 — Decoded Event Atlas could trigger empty/lossy Participant fallback

Severity: P1 production correctness and access boundary

Status: repaired, focused gates green, and pushed

`ArendalsukaEventAtlasCell` is scaffold-unique, persistent, catalog-published, and used as the source for Participant Program. Its decoded initializer returned before `state`, `export`, and actions were registered. Participant Program requested an Agreement and immediately read `export`; a temporary `notFound` then entered the journal-backed fallback and could hide the decoded non-empty source. Atlas now owns serialized, idempotent readiness, and Participant awaits it before Agreement/read. The production-class regression registers an encoded three-session Atlas in the resolver with journals disabled and proves source-backed preview reads all three rows from the same UUID without replacement. Owner read/export/search, stable grants, and wrong-key read/write denial also pass.

### D19 — Current core Agreement hardening breaks owner-published public read

Severity: P1 security-policy integration regression

Status: open; blocked by overlapping uncommitted CellProtocol work

The current shared checkout changes `Agreement` defaults from a `GrantCondition` template to no conditions, while `GeneralCell.addAgreement` now requires matching conditions and at least one authorization-enforcing `ProvedClaimCondition` or target/resolve `LookupCondition`. The existing Arendalsuka public-read Agreement therefore rejects, leaving Participant preview empty even though the Atlas is healthy. The audit did not add an implicit public/admin grant or weaken the resolver. The core security owner must define the intended explicit public-publication condition and restore the existing positive test with wrong/missing/stale-proof negatives.

### D20 — Binding broad tests are not isolated from shared runtime or AppKit host lifecycle

Severity: P1 acceptance-gate integrity

Status: source-diagnosed; repair blocked by current core compile overlap

Swift Testing's `.serialized` trait does not serialize unrelated peer suites. Six Binding suites mutate process-wide `CellBase` defaults, with 247 assignments in the target; a lock around individual reads/writes is not a lease across `save -> install -> await -> restore`. The narrow repair is one outer serialized suite containing only global-mutating suites. Separately, the app-hosted tests start runtime warmup and key-window animations while a renderer test creates and closes its own key `NSWindow`, matching the `_NSWindowTransformAnimation` crash. The advised repair is an offscreen `NSHostingView` test plus an `XCTestConfigurationFilePath` host guard, not sleeps, retries, animation disabling, or relaxed proof checks. Execution is currently blocked because the dirty shared core fails Binding compilation at `BridgeBase.swift:1278` (`identitiesReferenceSame` missing).

### D21 — Conference Participant Shell could use a decoded Agenda before bindings existed

Severity: P1 application correctness and access boundary

Status: repaired, focused gates green, and pushed

`ConferenceAgendaCell.init(from:)` launched permission and key/action setup in an unawaited `Task`; `ConferenceParticipantShellCell` returned the resolved dependency without a readiness await. Agenda now starts no decoded work, installs exact grants and runtime handlers through one serialized, retryable gate, and the shell awaits that gate. The decoded tests cover 40 concurrent callers, persisted session selection, a real `selectTrack` action, stable grant contracts, wrong-signing-key read/write denial, and unchanged owner state after retry. Two production Participant Shell tests cover domain-slice delegation and agenda-action state propagation.

### D22 — CellScaffold Chat hosts could return a decoded backend before actions existed

Severity: P1 application correctness and access boundary

Status: repaired, focused gates green, and pushed

`App.ChatCell.init(from:)` launched permission and runtime-key setup in an unawaited `Task`, including a global-vault fallback that could search or create a substitute identity. `VaporChatMVP` and `ConferenceChatLaunchCell` then returned the resolved Chat immediately. Decoded initialization now restores persisted state only. A serialized, retryable requester-proof activation installs runtime handlers without recreating or broadening persisted Agreement grants, and both production hosts await it after their existing authentication/payment or conversation resolution. A combined same-process run passes five focused tests: decoded known state and real action, wrong-signing-key denial, paid/authenticated HTTP state/action/state, decoded Conference backend, and the common idempotency gate. One broader pre-existing read-only Agreement test remains red under the dirty shared-core policy refactor and is recorded as an external blocker rather than bypassed.

### D23 — Public Shell and Device Registration repeated the decoded readiness race

Severity: P1 application correctness and access boundary

Status: repaired, focused gates green, and pushed

The public Conference shell and device-registration Cell were both persisted/hosted paths whose decoded initialization could return before supported state and actions existed. Each now uses the established requester-aware serialized installer, starts no detached decoded work, and is awaited by its immediate host. These repairs change lifecycle only; they do not turn a public shell into implicit public authority or make possession of a device identifier or push token an authorization proof.

### D24 — Notification and adjacent Contact/Agent/Personlog Cells could be consumed before decoded bindings existed

Severity: P1 for the production notification, Contact, and Agent paths; P2 latent for unregistered Personlog projections

Status: repaired, focused gates green, and pushed

`ConferenceBroadcastStudioCell`, `NotificationPolicyCell`, `NotificationOutboxCell`, `DeviceCallbackBridgeCell`, `ContactEndpointCell`, `AgentConversationInboxCell`, `PersonlogQuestionInboxCell`, and `PersonlogJobProjectionCell` all had required decoded initialization that could return before handlers were installed. Direct consumers included Porthole notification summary, Personlog projections, Contact/Sales/Agent workspaces, Vapor callbacks/replies, simulation publication, and the internal Studio -> Policy -> Outbox -> Callback chain. The Cells now decode state only and install runtime behavior through one idempotent readiness gate; every identified immediate production consumer awaits it.

The exact notification dependency pipeline has a persisted reload gate. A second regression covers all four adjacent Cells with 40 concurrent ensures and real immediate operations. The Contact and Agent fixtures preserve non-empty state through round-trip before a real mutation. The same-UUID/different-signing-key Contact negative proves private read and retirement denial with no mutation. Forty-three of forty-four selected consumer tests pass; the lone existing `ConferenceDemoStoryCell` decode-restore test fails `notFound` both with and without the new readiness hunk, so it is recorded separately rather than attributed to this wave.

### D25 — Public device callbacks elevate unauthenticated input to Scaffold authority

Severity: P1 security; promote to P0 only if current high-value traffic/exploitation evidence is established

Status: exposed in staging, not repaired; owner/multi-repo decision required

`VaporDeviceCallback` mounts register, resolve, and submit POST routes without authentication, decodes caller-selected participant/device/ticket/routing fields, and then replaces the external caller with the trusted Scaffold identity. Registration records are keyed by the supplied participant/device pair; callback validation does not prove control of an enrolled signing key; ticket lookup is not bound to device identity; caller routing hints can select downstream Contact or Agent behavior. Binding currently sends unsigned JSON.

Live, non-mutating malformed-body probes return HTTP 400 on all three exact POST paths, proving the routes are mounted on staging revision `12e7402`; HEAD returns 404 because only POST is registered. Current real traffic was not proven, so P0 is not asserted.

The smallest correct permanent repair is coordinated: an owner-issued enrollment Agreement/capability binds exact participant/device, subject identity and signing-key fingerprint, allowed registration/resolve/submit actions, audience, expiry, revocation, and one-time enrollment ID. Every request then signs a canonical action/method/path/query/body-hash envelope with bounded time and persisted nonce; Cells enforce signer binding, ticket scope, replay, expiry, and state transition. Legacy records must be unverified until owner-approved re-enrollment. Cookie/admin/shared-secret/push-token authority and public dual mode are rejected.

### D26 — Runtime launch exists, but default button targets are not fully decompiled

Severity: P2 configurability/completeness

Status: partial by design; no security boundary removed

The `surfaceID` registry, versioned bootstrap, published projection, Porthole resolver, Binding parser/adapter, and runtime remapping tests prove the configurable route contract below the authenticated remote read. The standard public configuration factory still emits some direct compiled `configurationLookup` targets as a fallback. Deterministic seeding and reconciliation of stable registry IDs now exist, but removing the direct targets safely still requires a green owner-authorized Agreement issuance path while preserving compiled endpoint admission as a security boundary. This audit records that residual explicitly instead of describing all deeplinks as runtime-owned.

### Advisory-panel evaluation for the continuation

Three independent roles were used before implementation:

- The consumer-path reviewer found no generic runtime surface deeplink and identified compiled startup reset behavior as the lock-in point. It required a shared launch reference and view-only negative tests.
- The architecture reviewer rejected overloading `ConfigurationCatalogCell` as a global route table and recommended a scaffold-unique persistent launch registry with revisioned `surfaceID -> configurationLookup` entries. That is the implemented ownership boundary.
- The security reviewer found the identity-link P1 issues above and required opaque route IDs, exact parsing, no authority in links, fail-closed stale state, and resolver/Agreement enforcement after resolution.

Counterargument retained: a compiled registry Cell type and bootstrap endpoint still exist, and Porthole publication has a compiled supported-endpoint boundary. The repair makes route content runtime-configurable; it does not claim arbitrary executable endpoint discovery. No new Purpose node was needed because the existing quality, acceptance, and access-audit nodes routed and terminated the work adequately.

The next adviser wave was also read-only and adversarial:

- The CellScaffold auditor classified 78 catalog endpoint names: 14 were already host-waitable, two self-await their deferred setup, nine use a synchronous conference restore helper, one has no decoded async setup, two external types remained unknown, and roughly fifty published endpoint types still need individual adjudication. It ranked Event Atlas first and Conference Agenda next. It also disproved the all-or-nothing preview hypothesis for Participant Program: either healthy sessions or healthy actors are retained.
- The core auditor proved that `CellJSONCoder`/Resolver return decoded Cells without activation and that repeated setup is not generally idempotent. It ranked shared `ChatCell` first because the existing test sleeps 20 ms after decode, followed by Apple Orchestrator/EntityAnchor, Calendar, Vault, GraphIndex, TrustPacket, TrustedIssuer, Commons, and conditional Apple Intelligence. Plain `GeneralCell`, `AnyCell`, Agreement, and Identity were explicit counterexamples.
- The Binding auditor separated two causes: peer suites marked `.serialized` still race over process-wide runtime defaults, while the AppKit crash belongs to app-host/key-window lifecycle. It recommended one outer serialized global-state suite, an offscreen renderer, and a unit-test-host guard. It rejected sleeps, retries, animation disabling, swallowed proof errors, and authorization relaxation.
- The application-candidate reviewer ranked CellScaffold app `ChatCell` as the next clean executable occurrence because it is persistent, Porthole/HTTP-published, and also used by Conference chat. Agreement Workbench was source-relevant but overlapped an unrelated dirty RWXS workstream; Personal Page Publisher remained the next clean lower-ranked candidate.
- The Conference counter-auditor ranked `ConferencePublicShellCell`, then Device Registration and the Onboarding fan-out, as the next direct-host checks. It also identified synchronous restore helpers that are only conditionally safe because their five-second timeout is ignored by callers.
- The core feasibility reviewer rejected using the app-Chat repair as evidence for changing shared `CellBase.ChatCell`: a correct core repair needs an optional activation contract, resolver/host compatibility proof, and the active Agreement/identity refactor resolved first. Persisted Agreement authority must remain authoritative; decoded activation must not silently recreate compiled grants.
- The adjacent-host reviewer independently classified ContactEndpoint and Agent Conversation Inbox as production-persistent P1s and both Personlog projections as P2 latent. It located every immediate consumer and warned that Contact's self-contained signature verification is a cryptographic primitive, not a registered-key authority proof.
- The device-security reviewer traced an end-to-end unauthenticated overwrite/ticket/routing chain, rejected merely signing caller-selected identities, and required owner-approved device enrollment plus Cell-owned replay and action policy. Its recommendation to fail closed on public staging conflicts with compatibility for current unsigned Binding builds and is therefore a Kjetil-owned coordinated rollout decision, not an app-local convenience patch.
- The runtime-link counter-review accepted the persistent owner-published registry but found default direct targets and malformed/dead target validation as residuals. It explicitly retained the compiled supported-endpoint allowlist as an access boundary.
- The native Binding counter-review reproduced the actual renderer defect: a Skeleton `surfaceLaunch` button still went to local Porthole, returned a non-nil `error: invalid payload`, and displayed false success. It required a Binding-local adapter carrying the real requester, remote-first admitted catalog matching, visible malformed-payload failure, and macOS window targeting. A second adversarial pass found and then cleared the process-global multi-window fan-out before commit.
- The core security review rejected splitting the current forty-file dirty identity/Agreement wave or using `getOwner` as a proof-capable identity vending API. The safe future boundary is opt-in strict owner-authorized Agreement issuance with exact template/grant/signatory/domain/key/expiry binding, plus concurrency and actual-use expiry tests. Until then the default public factories remain compiled fallbacks.

## Continuation changed files

CellScaffold runtime launch (`b716d69`):

- `Sources/App/Cells/ScaffoldLaunch/ScaffoldLaunchRegistryCell.swift`
- `Sources/App/Controllers/PortholeWebSessionSupport.swift`
- `Sources/App/configure.swift` (two registry bootstrap lines only)
- `Sources/App/routes.swift`
- `Tests/AppTests/ConferenceSurfaceRoutesTests.swift`
- `Tests/AppTests/PortholeRuntimeBindingEnsuringTests.swift` (one registry coverage hunk only)
- `Tests/AppTests/ScaffoldLaunchRegistryCellTests.swift`

Binding runtime launch and identity-link hardening (`0a9752e7`):

- `Binding/BootstrapView.swift`
- `Binding/ContentView.swift`
- `Binding/PortableSurfaceSupport.swift`
- `BindingTests/BindingTests.swift`
- `BindingTests/CellConfigurationVerifierXCTest.swift`

Binding catalog readiness (`b26fe5fb`):

- `Cells/ConfigurationCatalogCell.swift` (four lifecycle/idempotency hunks only; Personal Butler hunks excluded)
- `BindingTests/ConfigurationCatalogReadinessTests.swift`

CellScaffold Access Requirement Prompt readiness (`af9f24d`):

- `Sources/App/Cells/AccessRequirementPrompt/AccessRequirementPromptCell.swift`
- `Sources/App/Controllers/PortholeWebSessionSupport.swift` (two direct-helper readiness hunks only)
- `Tests/AppTests/AccessRequirementPromptCellTests.swift`
- `Tests/AppTests/PortholeRuntimeBindingEnsuringTests.swift` (one Access Prompt hunk only)

CellScaffold Arendalsuka Event Atlas readiness (`029a590`):

- `Sources/App/Cells/Arendalsuka/ArendalsukaEventAtlasCell.swift`
- `Sources/App/Cells/Arendalsuka/ArendalsukaParticipantProgramCell.swift` (one source-read readiness line)
- `Tests/AppTests/ArendalsukaEventAtlasCellTests.swift`
- `Tests/AppTests/PortholeRuntimeBindingEnsuringTests.swift` (one Event Atlas hunk only)

CellScaffold Conference Agenda readiness (`e7faabc`):

- `Sources/App/Cells/ConferenceMVP/Cells/ConferenceAgendaCell.swift`
- `Sources/App/Cells/ConferenceMVP/Cells/ConferenceParticipantShellCell.swift` (one dependency readiness line)
- `Tests/AppTests/ConferenceAgendaCellTests.swift`
- `Tests/AppTests/PortholeRuntimeBindingEnsuringTests.swift` (one Conference Agenda hunk only)

CellScaffold app Chat readiness (`682dd18`):

- `Sources/App/Cells/Chat/ChatCell.swift`
- `Sources/App/Cells/ConferenceMVP/Cells/ConferenceChatLaunchCell.swift` (one backend readiness line)
- `Sources/App/Controllers/VaporChatMVP.swift` (one host readiness await)
- `Tests/AppTests/ChatCellTests.swift`
- `Tests/AppTests/ChatMVPRoutesTests.swift`
- `Tests/AppTests/ConferenceEntityDiscoveryCellTests.swift` (one decoded-backend production-path setup)
- `Tests/AppTests/PortholeRuntimeBindingEnsuringTests.swift` (local test vault and one Chat hunk only; four unrelated worktree additions excluded)

CellScaffold public shell/device/runtime-launch continuation (`bff5fea`, `16089c1`, `d451ccd`):

- public Conference shell readiness and direct host await
- device-registration readiness and direct host await
- owner-published runtime `surfaceID` navigation, public configuration policy, route handling, and focused tests

CellScaffold notification dependency chain (`448fdcf`):

- `ConferenceBroadcastStudioCell`, `NotificationPolicyCell`, `NotificationOutboxCell`, and `DeviceCallbackBridgeCell`
- every identified direct notification/Personlog/Contact/Sales/Agent/Vapor consumer
- concurrent/idempotent readiness and persisted dependency-pipeline reload tests

CellScaffold adjacent hosted Cells (`aa0149f`):

- `ContactEndpointCell`, `AgentConversationInboxCell`, `PersonlogQuestionInboxCell`, and `PersonlogJobProjectionCell`
- Device Callback, Agent reply, Conference simulation, and Demo Story direct-host awaits
- four decoded immediate-use regressions plus Contact wrong-signing-key/no-mutation coverage

CellScaffold runtime route continuation (`384c14a`, `106ccd6`, `71854ce`):

- safe runtime `surfaceID` forwarding through login
- versioned default route bootstrap with remap, removal, and persisted encode/decode re-instantiation tests
- public projection enforcement in resolver and Porthole; unpublished and legacy routes fail closed

Binding native runtime surface adapter (`1fe09943`):

- `Binding/PortableSurfaceSupport.swift`
- `Binding/SkeletonPresentationOverlayView.swift`
- `Binding/BootstrapView.swift`
- `Binding/ContentView.swift`
- `BindingTests/BindingTests.swift`

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
| `scripts/run_tests_isolated.sh --filter PortholeRuntimeBindingEnsuringTests` | 3 passed | Real decoded catalog, same-UUID/different-key rejection, and concurrent/idempotent ensuring for 16 locally constructible Cells including Conference Agenda. Other specialized conference shared-owner Cells remain outside this generic constructor. |
| `scripts/run_tests_isolated.sh --filter ConfigurationCatalogClientTests` | 4 passed | Client invokes readiness before immediate action/read and keeps decode behavior. |
| `scripts/run_tests_isolated.sh --filter ProductionSkeletonBindingIntegrityTests` | 4 passed | Production Workbench and Arendalsuka configurations/payloads keep resolvable keypaths, Agreement-backed atlas reads, non-empty rows, and detail/tab actions. |
| `scripts/run_tests_isolated.sh --filter ConferenceSurfaceRoutesTests/testAuthenticatedPortholeConferenceDemoFlowSupportsCanonicalPersonaLockedSequence` | 1 passed | Authenticated local HTTP/Porthole Conference sequence with canonical personas. No real browser screenshot. |
| `scripts/run_tests_isolated.sh --filter PersonalCopilotV1Tests/testChatPromptSubmitRoutesPortholeCommandsBeforeActiveHelper` | 1 passed | Co-Pilot routes Porthole commands before an active helper without unintended helper action. |
| `swift test --filter ScaffoldLaunchRegistryCellTests` | 10 passed | Owner publication/resolution and flow; encode/decode plus concurrent readiness; exact-grant stability; wrong identity and same UUID/wrong key denial; optimistic concurrency; malformed, endpoint-only, unpublished, versioned seed, remap, removal, and same-process persisted re-instantiation behavior. This is not a process-restart gate. |
| `swift test --filter ConferencePublicShellReadinessTests/testRuntimePublicConfigurationPersistsSafeDeeplinkAndRejectsMutationControlsWithoutRevisionChange` | 1 passed | Persists the real public runtime configuration, preserves the safe opaque deeplink, and rejects mutation controls without the required revision. |
| `swift test --filter ConferenceSurfaceRoutesTests/testAuthenticatedPortholeResolvesOwnerPublishedRuntimeSurfaceIDThroughAgreement` | failed: 4 assertions | The current dirty core rejects the legacy two-argument owner Agreement (`rejected` rather than `signed`), so Porthole stays empty. The fixture now explicitly publishes the route and grants only `publishedRoutes`; no authorization bypass was added. |
| `swift test --filter PortholeRuntimeBindingEnsuringTests/testCommonRuntimeBindingCoordinatorKeepsGrantsStableUnderConcurrentEnsureCalls` | 1 passed after each continuation | Launch Registry, Access Requirement Prompt, Event Atlas, Conference Agenda, and app Chat participate in the common concurrent/idempotent readiness gate. The test now owns a local ephemeral vault so unrelated tests cannot replace its proof source; four unrelated worktree additions in the same file were not staged by this audit. |
| `swift test --filter 'AccessRequirementPromptCellTests/testDecodedPrompt'` | 2 passed | Decoded immediate state/action, 40 concurrent ensures, stable exact grants, wrong-key read/write denial, unchanged state, and real-owner retry. |
| `swift test --filter PortholeConfigurationLoadingTests/testBootstrapAddsAccessRequirementOverlayAndPrefillsPromptForBlockedReference` | 1 passed | Real Porthole bootstrap resolves and prefills the protected-reference prompt through the readiness-aware helper. |
| `swift test --filter 'ArendalsukaEventAtlasCellTests/testDecodedEventAtlas'` | 2 passed | Decoded owner state/export/search with three known sessions; 40-way readiness and stable grants; same-UUID/wrong-key read/write denial and owner retry. |
| `swift test --filter ArendalsukaEventAtlasCellTests/testParticipantPreviewReadsDecodedRegisteredAtlasWithoutJournalFallback` | 1 passed | Real resolver returns the encoded non-empty Atlas; Participant source-backed preview reads all three sessions with journals disabled and preserves the decoded Atlas UUID. |
| `swift test --filter ArendalsukaEventAtlasCellTests/testParticipantProgramGetsPublishedAtlasReadAgreementForPublicProgram` | failed: 3 assertions | Current unrelated core Agreement-template hardening rejects the owner-published public-read Agreement. No bypass added; core security integration remains P1. |
| `swift test --filter 'ConferenceAgendaCellTests/testDecodedAgenda'` | 2 passed | Decoded persisted selection and real track action; 40 concurrent ensures; stable grants; same-UUID/wrong-key read/write denial; unchanged state after owner retry. |
| `swift test --filter 'ConferenceShellCellsTests/(testParticipantShellDelegatesToDomainBackedSlices|testParticipantShellAgendaActionReturnsUpdatedProgramState)'` | 2 passed | Real Participant Shell dependency delegation waits for Agenda and propagates the agenda action result. No process restart or browser artifact. |
| `swift test --filter 'ChatCellTests/testDecodedChat|ChatMVPRoutesTests/testPaidStateAndMessageRoutesAwaitDecodedChatReadiness|ConferenceEntityDiscoveryCellTests/testChatLaunchCellCanStartConversationAndProjectMessageFeedback|PortholeRuntimeBindingEnsuringTests/testCommonRuntimeBindingCoordinatorKeepsGrantsStableUnderConcurrentEnsureCalls'` | 5 passed, 0 failures | One process covers 40-way decoded Chat activation, persisted message/draft, real action, wrong-signing-key denial, paid/authenticated HTTP state/action/state, decoded Conference backend, and common idempotency. No deployment or process restart. |
| `swift test --filter NotificationRuntimeReadinessTests` | 4 passed, 0 failures | Notification chain plus Contact/Agent/Personlog encode/decode, 40 concurrent ensures, stable grants, persisted non-empty Contact/Agent state, immediate real actions, and same-UUID/wrong-key Contact no-mutation. |
| `swift test --filter 'NotificationPushProviderTests|ConferenceBroadcastStudioCellTests|PersonlogProjectionCellTests|SalesWorkspaceCellTests'` | 37 passed, 0 failures | Existing production notification, callback, projection, sales, and persisted Studio -> Policy -> Outbox -> Callback behavior remains green after the notification repair. |
| `swift test --filter 'ContactEndpointCellTests|AgentConversationInboxCellTests|PersonlogProjectionCellTests|ConferenceDemoStoryCellTests|ConferenceSimulationPopulationCellTests|NotificationPushProviderTests'` | 44 executed: 43 passed, 1 failed | All directly affected Contact/Agent/Personlog/callback/reply/simulation paths pass. The existing Demo Story decode-restore test fails `notFound`; an A/B run without the new readiness hunk fails identically, so it is not counted as a regression or a green gate. |
| `swift test --filter ConferenceDemoStoryCellTests/testDecodedStoryCellRestoresActionsBeforePortholeClick` with and without the new readiness hunk | failed both times: `KeyValueErrors.notFound` | Proves an independent decoded-action restoration defect remains in Demo Story. It does not undercut the adjacent readiness tests, and it was not hidden or weakened. |
| `swift test --skip-build --filter 'ChatCellTests|ChatMVPRoutesTests'` | HTTP 8/8 passed; Chat 9/10 passed | Broad app-Chat coverage remains useful, but `testChatCellEditableConfigurationRejectsReadOnlyRequesterApply` fails under the current shared-core Agreement-template refactor. The focused readiness paths remain green and no authorization bypass was added. |
| `python3 Tools/Explore/explore_contract_audit.py --repo-root CellScaffold --json-output /tmp/scaffold-launch-explore.json` | 0 errors, 0 warnings | Static Explore coverage for the new production registry; not a runtime authorization test. |
| `git diff --check` | passed | Patch whitespace integrity only. |

The first unprivileged rerun of the production-skeleton suite failed because SwiftPM's internal `sandbox-exec` could not apply its sandbox. The same isolated command was rerun outside that sandbox and passed. This was an execution-environment failure, not a product test failure.

### Core, Binding, ports, and services

| Repository / command | Result | Limitation |
|---|---|---|
| CellProtocol: `swift test --filter 'GeneralCellInterfaceTests|PersistenceTests|CellLifecycleTests|ContractProbeCellTests|IdentityDomainBindingTests'` | 46 passed | No universal decode-readiness contract. |
| CellProtocol adviser source audit | read-only ranked matrix | `ChatCell` is highest shared candidate; its test sleeps 20 ms after decode. Apple Orchestrator/EntityAnchor, Calendar, Vault, GraphIndex, TrustPacket, TrustedIssuer, Commons, and conditional Apple Intelligence are also source-vulnerable. Plain `GeneralCell`/`AnyCell`/Agreement/Identity are counterexamples; `PerspectiveCell` is only conditionally safe because its semaphore has a five-second timeout. |
| Binding: `Scripts/test_binding.sh CODE_SIGNING_ALLOWED=NO -only-testing:BindingTests/ChatWorkbenchParityTests` | 45 passed | Workbench plus the production PersonalIdentity decoded path; immediate/concurrent state/action; stable grants; wrong-key rejection and retry. No separate-process restart. Latest artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/Binding-erntjstdfcrbeachccbemadrrbon/Logs/Test/Test-HAVEN-2026.07.13_11-01-33-+0200.xcresult`. |
| Binding: `Scripts/test_binding.sh CODE_SIGNING_ALLOWED=NO -only-testing:BindingTests/CatalogAbsorbXCTest` | 1 passed | Native Porthole catalog resolution and attached state remain green against the current shared core. Artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/Binding-erntjstdfcrbeachccbemadrrbon/Logs/Test/Test-HAVEN-2026.07.13_11-13-07-+0200.xcresult`. A direct non-script workspace run hit stale persistent app-container owner proof and was rejected; no bypass was added. |
| Binding: `xcodebuild test ...` with eight explicit `BindingTests` identity-link/runtime-surface `-only-testing` selectors | 8 passed | Exact route/duplicate/size/authority negatives, challenge reset/expiry, opaque view-only launch parsing, published lookup projection, remote source retargeting, and disabled/endpoint-only rejection. This does not prove the currently red authenticated Agreement issuance path. Current artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/Binding-erntjstdfcrbeachccbemadrrbon/Logs/Test/Test-HAVEN-2026.07.13_12-34-02-+0200.xcresult`. |
| Binding clean HEAD snapshot plus the five-file native adapter diff: `Scripts/test_binding.sh CODE_SIGNING_ALLOWED=NO` with six explicit runtime-surface selectors | 6 passed | Real Skeleton extraction and `SkeletonButton.execute` through the bootstrap-registered adapter/resolver; exact requester propagation; published-only resolution; malformed/disabled/endpoint-only negatives; remote-first ordering; macOS missing/mismatched-window rejection. Artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/Binding-cyoybuufknhjmscuziaasvutngfk/Logs/Test/Test-HAVEN-2026.07.13_15-50-46-+0200.xcresult`. The primary tree's unrelated `PersonalButlerPolicy.swift` compile errors were excluded by the clean snapshot rather than repaired. |
| Binding: `xcodebuild test ... -only-testing:BindingTests/CellConfigurationVerifierXCTest/testConferenceIdentityLinkCompletionFlowWritesEntityAnchorRecord` | 1 passed | Real completion flow signs the exact trusted challenge/request and accepts only the matching completion package. |
| Binding: `xcodebuild test ... '-only-testing:BindingTests/ConfigurationCatalogReadinessTests/decodedCatalogIsReadyForImmediateConcurrentStateAndAction()'` | failed first, then 1 passed | Red run exposed grant growth from 69 to 136. Green run proves encode/decode, 12 concurrent ensures, immediate non-empty production configurations, real action, and stable exact grant contracts. Artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/Binding-erntjstdfcrbeachccbemadrrbon/Logs/Test/Test-HAVEN-2026.07.13_12-31-04-+0200.xcresult`. |
| Binding isolation follow-up: mixed global-state gate with `-parallel-testing-enabled NO` | build blocked, no tests executed | Read-only diagnosis proved peer `.serialized` suites still race over global `CellBase` defaults and identified a separate app-host/key-window lifecycle for the AppKit crash. Execution stopped at the current shared-core compile error `BridgeBase.swift:1278: cannot find identitiesReferenceSame`; artifact `/tmp/BindingIsolationGate.xcresult`. |
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

A broad Binding target run executed 359 tests: 335 passed, 20 skipped, and 4 were reported failed. One was the runtime-source retarget assertion, which was corrected and then passed in the focused 8-test rerun. The other three reports belonged to one concurrent AppKit `SIGSEGV` incident in `_NSWindowTransformAnimation` deallocation while three tests were active. The mixed follow-up also demonstrated that suites marked `.serialized` still run concurrently with other suites and can overwrite shared `CellBase.defaultIdentityVault/defaultCellResolver` state; one PersonalChatHub test failed `ownerProofUnavailable`, and Xcode then blocked while saving a crashed test record. The affected readiness tests pass individually. These are unresolved test-host/isolation defects, not accepted evidence of production correctness, and the full 359-test target was not rerun green after the focused fix. Broad artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/Binding-erntjstdfcrbeachccbemadrrbon/Logs/Test/Test-HAVEN-2026.07.13_12-16-34-+0200.xcresult`.

The first executing Binding regression run failed only the new decoded chat test with `notFound` while 41 existing tests passed; artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/Binding-erntjstdfcrbeachccbemadrrbon/Logs/Test/Test-HAVEN-2026.07.13_10-32-46-+0200.xcresult`. The first serialized-install version then failed the new grant-stability assertions because 496 persisted grants became 990; artifact: `/Users/kjetil/Library/Developer/Xcode/DerivedData/Binding-erntjstdfcrbeachccbemadrrbon/Logs/Test/Test-HAVEN-2026.07.13_10-39-25-+0200.xcresult`. HavenAgentD's first supervisor decode regression likewise failed with `notFound`. These are preserved as red-before-green evidence.

Rechecks against the later shared-core snapshot: CellScaffold `PortholeRuntimeBindingEnsuringTests` passes 3/3 and SwiftWebScaffold passes 4/4. The CellScaffold `ConfigurationCatalogClientTests` recheck is temporarily unbuildable because a concurrent unrelated `PersonalCopilotV1Tests.swift` edit references a missing `asInt`; the earlier isolated 4/4 result remains the last valid evidence. `Package.resolved` did not change during the recheck.

### Current staging evidence

Commands:

```text
curl -fsS https://staging.haven.digipomps.org/health/build
curl -i -sS https://staging.haven.digipomps.org/health/ready
npm run arendalsuka:data-health -- --base-url https://staging.haven.digipomps.org --min-sessions 2000 --min-local-actors 50 --min-map-features 50
curl -sS -o /dev/null -w '%{http_code}\n' -X POST -H 'content-type: application/json' --data '{}' https://staging.haven.digipomps.org/conference-mvp/api/device/{register,callback/resolve,callback/submit}
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
| Device route presence | malformed, non-mutating `{}` POST returns 400 on register, callback/resolve, and callback/submit; routes are mounted without an authentication middleware in source |

No valid device request, mutating Workbench staging canary, deploy, or browser journey was run. The malformed device payload fails decoding before Cell resolution or mutation. The persistence/shared-access canaries create identities and state, so they were not inferred from permission to perform a read-only audit and local repair.

## Claim adjudication

| Claim | Support | Counterargument / undercut | Evaluation | Deduced work |
|---|---|---|---|---|
| C1: readiness race is a general latent class across multiple hosted Cells | Confirmed in CellScaffold including Access Prompt, Event Atlas, Conference Agenda/Public Shell, app Chat, Device Registration, the four-Cell notification chain, ContactEndpoint, Agent Inbox, and both Personlog projections; also SwiftWeb, Binding, HavenAgentD, Add2Entity, DiMy, and Spatial; shared core families remain source-proven | Many hits are already gated, false positives, specialized, or never published; the Personlog pair is currently latent/test-only; Go/Rust/Python are synchronous locally; fatal decode is a different failure | **Strongly supported as a multi-repo latent Swift failure class; scope not fully enumerated as defects** | Retain a per-published-Cell matrix; defer shared core changes until activation/Agreement compatibility can be proven |
| C2: detached decoded setup can cause empty/broken GUI | Binding's real decoded chat read failed with `notFound` while 41 existing tests passed; decoded Event Atlas could make a known-three-session Participant preview empty; notification/Contact/Agent hosts had the same immediate-use structure | Empty GUI can also come from source failure, Agreement denial, bad skeleton keypath, legitimate no-data state, or independent decode restoration such as current Demo Story | **Strongly supported, not exclusive as a cause** | Keep diagnostics able to distinguish not-ready, denied, not-found, empty-source, and fallback states |
| C3: host must await readiness before state/action | Direct Porthole, Participant, Chat, Public Shell, notification, Contact, Agent, Personlog, simulation, Vapor, SwiftWeb, Binding, Add2, DiMy, and Spatial consumers now await asynchronously restored Cells | Synchronous Cells and self-awaiting Cells need no extra gate; a universal core rule still needs cancellation/error/timeout/wire design | **Accepted:** every asynchronously restored supported Cell must expose and be awaited through the narrowest shared integration contract | Continue app-host repairs; design shared core compatibility only after the security overlap is clean |
| C4: coverage is insufficient if known data can render empty while tests pass | Binding had 41 green parity tests beside decoded `notFound`; the native runtime button returned a non-nil Porthole error and displayed false success until the exact button path was tested; catalog exposed 69 -> 136 grants; Atlas needed a real encoded three-row resolver/preview gate | Existing tests remain valuable for their declared contracts | **Accepted** | Add restart/empty-state canaries; repair Binding global/AppKit test isolation; require real persisted source payloads and exact action paths for each critical surface |
| C5: reliability fixes must not bypass identity/capability | UUID+fingerprint hardening and wrong-key read/write negatives; runtime links carry opaque view intent only; readiness changes add no authority | The current core Agreement overlap breaks public read, and the separate live device ingress already elevates unauthenticated callers to Scaffold authority | **Accepted and preserved in committed readiness/deeplink paths; HAVEN-wide security goal remains open** | Define explicit public publication; replace device ingress with owner-approved enrollment/proof; add wrong/missing/stale/replay negatives; do not insert admin/public/shared-secret shortcuts |
| C6: shared wire fixtures can primarily guard cross-runtime parity | Go/Rust/Python suites cover wire, bridge ready, identity, replay, and configuration semantics; runtime-specific smokes fit above | No single Swift-exported readiness/persistence golden fixture is consumed by all ports | **Partially supported** | Define one versioned Swift fixture set for encode/decode/state/action/error and consume it in Go/Rust/Python; retain host-specific functional smokes |

Adviser voting was not used. Evaluation follows source, executable tests, live responses, and explicit gaps.

## Access/privacy preservation matrix

| Case | Evidence in this wave | Status |
|---|---|---|
| Same UUID, wrong signing key | New decoded CellScaffold catalog/Access Prompt/Event Atlas/Conference Agenda/app Chat, SwiftWeb, Binding, HavenAgentD, Add2Entity, DiMy, and Spatial negative tests | Pass in every focused repaired path; Atlas, Access Prompt, Conference Agenda, and app Chat deny both read and write |
| Unauthenticated privileged import | Live POST returns 401 | Pass for this endpoint |
| Wrong method on privileged import | Live GET returns 405 | Pass |
| Public read through owner Agreement | Existing Arendalsuka positive test rerun against the current dirty shared core | **Fail / blocked:** core Agreement-template hardening rejects publication; no fallback or bypass added |
| Runtime surface route read through owner Agreement | Projection/unit/native adapter tests use `publishedRoutes` and the actual requester; authenticated Porthole positive rerun against the current dirty core | **Blocked:** legacy Agreement issuance is rejected by the overlapping strict-core work; no owner/admin/private fallback added |
| Deeplink as authority | Runtime link parser rejects requester, token, action, unknown/duplicate fields, non-view intent, oversized input, disabled routes, and endpoint-only entries | Local pass; deployed remote negative matrix open |
| Identity-link stale/cross-request completion | New challenge clears derived state; completion hash must equal the locally signed enrollment request | Local pass |
| Public device register/callback | Source audit plus live malformed-body route probes | **Fail / P1:** external caller is not authenticated and is replaced with Scaffold authority; no enrolled signing-key/capability binding |
| Device callback replay/cross-device ticket | No correct enrollment proof exists yet | **Open / blocked:** require persisted nonce, exact ticket/device/fingerprint binding, expiry, revocation, and state-transition negatives |
| Missing proof | Not executed for every changed/candidate path | Open |
| Stale proof | Not executed for every changed/candidate path | Open |
| Cookie/admin convenience bypass | No such bypass added; authenticated Conference test retained canonical persona/identity bootstrap | No known bypass in changed path |

## Functional coverage map

| Journey | Real input and dynamic assertions | Saved artifact | Honest status |
|---|---|---|---|
| HAVEN Workbench | Production configuration through local Porthole; supported keypaths/actions asserted | Test log only | Local pass; no live mutating persistence/shared-access canary |
| Arendalsuka Participant/Event Atlas | Production configurations/fixtures locally plus current live data/security canary | This report contains exact live observations | Local and read-only live pass on pre-repair staging revision |
| Conference | Authenticated Porthole HTTP sequence with canonical personas plus decoded Agenda and decoded Chat backend delegation/actions | Test log only | Local pass; no real browser screenshot or Binding parity replay |
| App Chat | Real persisted message/draft, paid/authenticated HTTP state/action/state, and Conference chat backend | Test log only | Focused local pass; one broader read-only Agreement test remains red under shared-core policy overlap; no deployment/restart artifact |
| Notification / phone callback | Persisted Studio -> Policy -> Outbox -> Callback local chain plus real Contact/Agent/Personlog consumer suites; live route presence only | Test logs and exact HTTP status probes | Readiness paths pass locally; public ingress authorization fails audit and no valid staging callback was sent |
| Co-Pilot routing/chat | Real `PersonalCopilotV1` Cell action path asserts routing order | Test log only | Local pass for selected route; not an exhaustive chat journey |
| Binding | Native production chat/PersonalIdentity/catalog Cells, all nine HavenAgentD Cells, catalog absorb, strict identity-link flow, and real Skeleton button -> adapter -> resolver execution | Red-before-green and final `.xcresult`/Swift package results above | Eight-test native runtime-launch slice and complete 398-case macOS target pass; iOS Simulator compiles. Deployed remote Agreement path, real OS cold-launch/multi-scene delivery, per-PersonalCopilot-subclass actions, restart, and test-discovery/global-state repeatability remain open |
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
15. Chose a scaffold-unique persistent launch registry rather than extending the general configuration catalog with global routing semantics. Route content is runtime state; registry bootstrap remains compiled infrastructure.
16. Defined runtime links as opaque, view-only references. Resolution never supplies identity, Agreement, proof, capability, endpoint authority, or an action from the link.
17. Treated the advisory security review as a blocking implementation input and repaired the adjacent Binding identity-link P1 issues in the same URL-boundary wave.
18. Reused Binding's established local readiness base for its catalog instead of changing CellProtocol core; the red grant-growth regression required exact semantic idempotency.
19. Treated Access Requirement Prompt as access-sensitive: readiness can install declared bindings but cannot approve, grant, submit proof, or accept a same-UUID/different-key requester. Added a wrong-key mutation negative before delivery.
20. Repaired Event Atlas at Cell ownership and at the immediate Participant source consumer. Did not remove the fallback globally; the real decoded-source regression proves fallback is not entered merely because bindings are late.
21. Rejected an app-local workaround for the current public Agreement failure. The overlapping core security policy must define explicit owner-publication semantics; renderer, transport, cookie, admin, and private-data fallback remain invalid owners.
22. Accepted the advisers' core finding that C1 is now source-proven beyond app Cells, but deferred shared semantics until a generic optional activation contract and cross-host compatibility tests can be changed in a clean core worktree.
23. Diagnosed Binding global-state and AppKit test-host failures read-only. No sleeps, retries, global animation switch, swallowed proof error, or auth relaxation was used as a test fix.
24. Repaired CellScaffold app Chat locally instead of conflating it with the shared core Chat type. Decoded activation installs behavior but does not recreate persisted Agreement authority; both real hosts own the readiness await after their existing access/payment gates.
25. Made the shared readiness regression use its own ephemeral identity vault after a combined run exposed test-order dependence on mutable process-wide defaults. Staged only the local-vault and Chat hunks; four concurrent additions in the same file remain untouched.
26. Deferred shared core Chat despite source proof because the correct activation contract overlaps the active resolver/identity/Agreement workstream and needs multi-host compatibility evidence. The next app audit target is Conference Public Shell.
27. Repaired Public Shell, Device Registration, the notification dependency chain, ContactEndpoint, Agent Inbox, and both latent Personlog projections at Cell ownership plus every identified immediate host; no core lifecycle semantics changed.
28. Treated runtime surface mapping as configurable but did not claim every factory button is decompiled. Retained the compiled endpoint allowlist; the later continuation added stable versioned `surfaceID` seeding/reconciliation, while default-factory conversion remains blocked on owner-authorized Agreement issuance.
29. Classified the mounted device ingress as an exposed P1. Rejected a self-selected signing identity, cookie, admin status, shared token, push token, or legacy auto-blessing as authority. A breaking fail-closed rollout versus coordinated Binding enrollment remains Kjetil's decision.
30. A/B-tested the red Demo Story decode-restore gate with and without the new readiness hunk. Because both fail identically, preserved it as an independent open defect rather than weakening the test or folding it into the adjacent commit.
31. Versioned the default runtime route bootstrap and made both web and native hosts consume only the published projection. Missing publication metadata is private by default.
32. Rejected direct source fallback in Binding after registry resolution: the mapped configuration must exist in the explicitly admitted catalog corpus, with remote endpoints tried before local fallback.
33. Treated adviser findings as pre-commit gates. A first pass caught a missing `published: true` fixture; a second caught process-global multi-window navigation and missing real-button execution. Both were repaired before delivery.
34. Reopened the earlier core-Chat deferral only after a clean CellProtocol
    worktree and method-aware compatibility design were available. Kept legacy
    methodless schemas and deprecated GET lifecycle aliases, but made local
    strict enforcement and catalogs operation-aware. Did not silently redefine
    Bridge or cross-runtime wire semantics.
35. Rejected the report's earlier interpretation of 54 Chat warnings after the
    adviser mapped all 56 current handlers to 56 complete contracts. Repaired
    the source auditor instead of annotating production code to satisfy a bad
    heuristic. The corrected order-aware audit then found 60 different, real
    strict-order errors across nine Cells; those were fixed at Cell ownership
    and guarded by a strict production-type regression.
36. Kept the 19 Apple computed-key findings visible in the regex auditor rather
    than implementing a partial Swift evaluator that could guess keys green.
    Manually mapped all 24 operations and added a local fresh strict publication
    matrix. Recorded that it is not an all-handler dispatch, decoded, permission,
    semantic-return, or remote-transport proof.

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
| CellScaffold runtime launch continuation | `m0/green-test-suite` | `b716d69e7c290c669986df60f65c0e6f50cd50b6` | `origin/m0/green-test-suite`, verified equal |
| Binding runtime launch + identity-link hardening | `main` | `0a9752e7` | `origin/main`, later superseded by and ancestor of `b26fe5fb` |
| Binding catalog readiness continuation | `main` | `b26fe5fb93289aab17ac72ed571709f4595d08a2` | `origin/main`, verified equal |
| CellScaffold Access Requirement Prompt readiness | `m0/green-test-suite` | `af9f24d98f1e1c9dac9e7212b1a6753b72981c7f` | `origin/m0/green-test-suite`, verified equal |
| CellScaffold Arendalsuka Event Atlas readiness | `m0/green-test-suite` | `029a590c3c199bbb7b669efb25f96e1a3a8adcd6` | `origin/m0/green-test-suite`, verified equal |
| CellScaffold Conference Agenda readiness | `m0/green-test-suite` | `e7faabcce225405704e1c0925af6724c500f7285` | `origin/m0/green-test-suite`, verified equal |
| CellScaffold app Chat readiness | `m0/green-test-suite` | `682dd18070de5468478210e0ff4638c234cf800c` | `origin/m0/green-test-suite`, verified equal |
| CellScaffold public shell readiness | `m0/green-test-suite` | `bff5fea` | `origin/m0/green-test-suite`, pushed in this continuation chain |
| CellScaffold device registration readiness | `m0/green-test-suite` | `16089c1` | `origin/m0/green-test-suite`, pushed in this continuation chain |
| CellScaffold runtime public surface navigation | `m0/green-test-suite` | `d451ccdf1e5403b77920e682057bcf4474a59eaf` | `origin/m0/green-test-suite`, pushed and later verified as ancestor of current head |
| CellScaffold notification pipeline readiness | `m0/green-test-suite` | `448fdcf38f55c2962957cd500a9e558a33e09b85` | `origin/m0/green-test-suite`, pushed and later verified as ancestor of current head |
| CellScaffold adjacent hosted Cells | `m0/green-test-suite` | `aa0149fc545fc4df22f2349b3c8ca17278fa6af5` | `origin/m0/green-test-suite`, verified equal |
| CellScaffold safe runtime launch through login | `m0/green-test-suite` | `384c14ab838d0899250234f561c4c575740573d0` | `origin/m0/green-test-suite`, pushed and verified as ancestor of current head |
| CellScaffold versioned runtime route bootstrap | `m0/green-test-suite` | `106ccd6e92d0163d74059329188c8e9363f602c4` | `origin/m0/green-test-suite`, pushed and verified as ancestor of current head |
| CellScaffold published-only runtime route projection | `m0/green-test-suite` | `71854ceb6672671d25b434e91de300268f6ffdbb` | Pushed to `origin/m0/green-test-suite`; later verified as an ancestor of local `14b50a51fbfd` and upstream `e3d4049fbcdc` after an independent security workstream advanced the branch |
| Binding native runtime surface adapter | `main` | `1fe09943a141533cd8ca5aee239e3028146d69a0` | `origin/main`, verified equal |
| CellProtocol host-safe Skeleton button hook | `main` | `1bde79c7b9b207c828aad1a9786d3fa5fc90b6ca` | `origin/main`, ancestor of the checked-Sendable follow-up |
| CellProtocol checked-Sendable host hook | `main` | `306b51aac7d168af473f25634c46d423a729212a` | `origin/main`, `ls-remote` verified equal; 707/707 package tests |
| CellProtocol TrustedIssuer policy/cache hardening | `main` | `caa4183d08da9b44b04f0db2aa00772e120da6e1` | `origin/main`, `ls-remote` verified equal; 710/710 package tests; 11/11 TrustedIssuer; 1/1 contract; adviser found no P0/P1 |
| CellProtocol persisted Apple Intelligence runtime | `main` | `d9638de009a019b9dc93eb84a54f2532efb21f17` | `origin/main`, `ls-remote` verified equal; 718/718 package tests; 9/9 Apple contracts; 1/1 shared decoded-readiness; target Explore audit 0/0; adviser found no P0/P1 |
| Binding scene-local runtime surfaces | `main` | `c0054360a364599cd472ab2094282a739baa5698` | `origin/main`, `ls-remote` verified equal; full macOS target 398/398 planned with 0 failures and iOS Simulator build exit 0 |
| CellProtocol shared cross-runtime wire fixture | `main` | `e84cf485a9757dd079a1bf223addb4447b2496f9` | `origin/main`; Swift fixture plus Python/Rust mirrors and consumer gates |
| CellProtocol strict Explore installation | `main` | `55f927035cb349a945b13cd2c44f7380a24fe746` | `origin/main`; strict handler installation and contract gates |
| CellProtocol Apple/Vapor strict readiness | `main` | `9a8b4b717342cc9c2d3e29e98059ee9e1f56a751` | `origin/main`; decoded host contract installation covered |
| CellProtocol explicit EntityScanner actions | `main` | `f845db97e12aee0a2a2f2b3e1e44c834f7073f97` | `origin/main`; production configuration/payload action tests |
| CellProtocol deterministic Lobby publication | `main` | `080bb934bf4457ac59a1fe7679d598b2beaf4bc7` | `origin/main`; signed public-read Agreement and wrong-key negatives |
| CellProtocol RelationalLearning persistence/concurrency | `main` | `d9d95145fc67910d2b4242c78af0ccc30cdabd6d` | `origin/main`, `ls-remote` verified equal; full package 737/737; RelationalLearning 14/14; readiness 15/15; focused Explore 0/0; repo Explore 0 errors/58 warnings; adviser verdict `SHIP` |
| CellProtocol method-aware Explore and Chat authorization | `main` | `74d89b49a0fc991415f507d5b0c0063f9e65ffc4` | `origin/main`; full package 754/754; GeneralCell 45/45; Chat 43/43; TrustedIssuer 12/12; readiness 15/15; final advisers found no concrete P0/P1 in changed scope |
| CellProtocol strict raw-handler contract ordering | `main` | `8e2196478fd9a4b8f5de2b53ff9e707d8ea3d2c7` | `origin/main`, `ls-remote` verified equal; full package 755/755; affected suites 59/59; strict nine-Cell regression 1/1; corrected Explore audit 0 errors/19 manual-review warnings |
| CellProtocol Apple Intelligence operation publication | `main` | `090169231d160e7efd723b3f8b8aa1958c6c816e` | `origin/main`, `ls-remote` verified equal; full package 756/756; Apple 10/10; fresh strict 24-operation/20-key publication matrix; adviser found no blocker |
| Binding scanner/runtime isolation follow-up | `main` | `2c295d8ce2ddf78562cc7541aa8f93132a77b8a7` | `origin/main`; full target 398 planned, 378 passed, 20 explicit skips, 0 failures |
| Rust missing-UUID/shared-fixture parity | `main` | `e5ea7e56d1f697c94660706786da9a6c76d015a2` | `origin/main`; unit plus 27 integration tests passed |

## Residual-risk ledger and owners

| Priority | Residual risk | Owner / blocker | Required terminal evidence |
|---|---|---|---|
| P1 | Binding audited families lack separate-process restart and deployed remote runtime-launch proof; eleven PersonalCopilot subclasses lack individual action coverage; a real OS cold launch and deployed cross-process scene delivery have not been exercised | Binding/HavenAgentD owner | Per-subclass critical action sampling, deployed owner-published launch with wrong/missing/stale-proof negatives, OS cold launch into the intended scene, restart |
| P1 | CellProtocol's 23 and CellScaffold's 110 heuristic hits are not fully manually adjudicated | Cross-repo audit owner; volume and specialized ownership | Per-type vulnerable/safe/tested/unknown matrix tied to actual publication/host path |
| P2 | Binding's final broad target is green with all 398 cases planned (378 passed, 20 explicit skips), but a preceding run falsely planned only 347 cases; parallel suites still share mutable `CellBase` defaults and an earlier AppKit crash incident shows the gate needs repeatability evidence | Binding test owner | Add an expected-test-count/discovery gate plus project-wide isolation/serial trait or dependency injection for globals; repeat the full target on the final dependency graph without underdiscovery, AppKit crash, or cross-suite proof failure |
| P1 | Swift strict Agreement and proof-bearing TrustedIssuer admission are published, but safe owner-authorized public issuance/session use is not proven across every live route or across Go/Rust/Python/SwiftWeb | CellProtocol identity/security and port owners | Pass owner-published public read plus wrong identity, missing proof, stale proof, non-released, concurrent-idempotency, and actual-use expiry negatives without app/renderer bypass in each supported runtime |
| P1 | Staging device register/resolve/submit routes accept unauthenticated input and elevate it to Scaffold authority; participant/device/ticket is not bound to an owner-enrolled signing key | Kjetil plus CellScaffold/Binding identity-security owners; breaking coordinated migration | Owner-approved enrollment Agreement/capability, canonical signed requests, exact device/ticket/action/audience binding, persisted replay and revocation, legacy re-enrollment, full negative matrix, staged coordinated rollout |
| P1 | `VaporAgentConversationReplies` uses a shared relay bearer token and reads private inbox records directly instead of the Cell's explicit reader-grant path | Agent relay/identity owner | Decide the intended service identity/capability; prove wrong token, wrong identity/key, missing/stale proof, record filtering, and revocation without transport-owned policy |
| P2 | Shared optional activation and the local GeneralCell flow lifecycle are published, but adviser-ranked Chat/Orchestrator/EntityAnchor/Calendar/Vault/GraphIndex/TrustPacket/Commons/Apple Intelligence families do not all have real per-family persisted immediate state/action, restart, and multi-host gates | CellProtocol/CellApple owners | Per-family production-contract tests, separate-process reload where state is durable, stable-grant checks, and multi-host compatibility evidence |
| P2 | Apple Intelligence retained state and owner-only dequeue are locally proven, but hostile pre-decode allocation, live Foundation Models output, separate-process restore, and a production generic-host drain are not | CellApple/host owners | Size-bounded envelope or streaming decode before allocation; separate-process restore; real available/unavailable model gates; host integration that dequeues and publishes without broadening owner authority |
| P2 | The corrected CellProtocol Explore regex/source audit emits 0 errors and 19 warnings. All 19 Apple warnings are manually mapped false positives, with a fresh local strict 24-operation publication matrix; Chat is 56/56/0 under the source model. The Apple matrix does not dispatch every handler or cover decoded/remote publication. Local strict/catalog lookup is method-aware, but remote Bridge `Explore.typeForKey(key:)` and cross-runtime wire consumers remain legacy single-key discovery | CellProtocol contract, transport, and port owners | Add decoded and representative dispatch/permission/semantic-return coverage across all operation families; design versioned operation-aware remote Explore before changing wire behavior; add shared Swift/Go/Rust/Python consumer fixtures without breaking legacy methodless lookup |
| P2 | RelationalLearning is proven only through in-process round-trip/concurrency tests; separate-process/crash restore, pre-decode bounds, saturation/compaction, arbitrary replay-versus-incoming concurrency, legacy direct-engine journaling, and cross-runtime journal/ID fixtures remain open | CellProtocol persistence, concurrency, and port owners | Separate-process durable-container gate, bounded envelope/streaming decode, explicit saturation policy, adversarial concurrency test, transaction-only or documented legacy API boundary, and shared cross-runtime golden fixtures |
| P2 | TrustedIssuer retained state is normalized to 512 valid records, but JSON decoding materializes complete persisted maps/arrays before normalization; local history is a churnable cache, not signed durable audit evidence | CellProtocol identity/security and persistence owners | Bounded streaming/envelope decode before allocation, hostile-size negative, separate-process reload, signed append-only audit design and verification |
| P1 | Remaining catalog-published CellScaffold endpoint types are not fully adjudicated after closing Event Atlas, Agenda, Chat, Public Shell, Device Registration, notification, Contact, and Agent paths; Onboarding fan-out and ignored synchronous-restore timeouts remain prominent | CellScaffold owners | Candidate-by-candidate publication/host audit, persisted known-data decode/immediate-read/action gates for each real vulnerable type, and explicit timeout classification |
| P1 | `ConferenceDemoStoryCell` decoded state/actions remain absent in its existing exact restore gate (`notFound`) independent of the new endpoint-readiness hunk | Conference application owner; current dirty shared-core/restore overlap | Repair through the same waitable/idempotent activation pattern or prove synchronous restoration, then pass decoded state, activate, and next-step actions |
| P2 | Two conference shared-owner ensuring Cells are not in generic constructor coverage | CellScaffold owner | Tailored ownership-aware concurrency and decode test |
| P2 | No shared Swift-origin golden readiness/persistence fixture across Go/Rust/Python | Cross-language contract owner | Versioned fixture plus runtime consumer tests and error parity |
| P2 | Process restart/persisted-container reload is not proven for all Tier-1 Cells | Each host owner | Separate-process or durable-container restart gate with immediate reads/actions |
| P2 | Partial source-preview recovery is not comprehensively tested; all-or-nothing fallback may still hide healthy sections | Porthole/source-preview owner | Production source with one failing and one healthy section; healthy content remains visible with explicit diagnostic |
| P2 | Missing/stale-proof negatives are incomplete | Identity/security owner | Resolver-enforced matrix for all changed Tier-1 paths |
| P2 | Browser-visible Porthole/Binding parity and “Something went wrong”/unexpected empty-state gates are incomplete | GUI verification owner | Same production configuration/payload in web and Binding, DOM/native assertions, screenshots/traces, no forbidden states |
| P2 | Runtime route entries and versioned default seeds are dynamic, but default factory buttons still use compiled direct targets because the authenticated owner-published route path is blocked by Agreement issuance; registry endpoint admission remains compiled infrastructure | CellProtocol identity/security owner plus Scaffold/Binding owners | Prove owner-authorized Agreement issuance, then convert default factories to stable `surfaceID` references; retain or deliberately version endpoint admission and add deployed web/Binding parity gates |
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
- CellScaffold can persist, version-seed, remap, remove, re-instantiate through encode/decode, and project only explicitly published runtime `surfaceID` routes; safe opaque IDs survive login without forwarding authority-bearing material.
- Binding accepts only an opaque view-only runtime launch contract, routes the real production Skeleton button through its registered local adapter with the exact requester, resolves published routes remote-first from configured scaffold catalog origins, admits only configurations from that same catalog corpus, and fails visibly on malformed launch payloads.
- The native launch bridge carries the originating scene UUID from the runtime-rendered button and only the matching scene handles it. AppKit window-number routing remains a fail-closed fallback for events without a scene token; the complete 398-case macOS target and focused eight-test runtime slice pass, and the iOS Simulator build exits 0.
- Binding identity-link input and completion are exact-route, bounded, duplicate-safe, trusted-origin/audience, reset-on-replacement, and exact-request-hash bound in the focused tests.
- Binding `ConfigurationCatalogCell` is repaired at the same requester-aware readiness boundary; its red-before-green regression proves stable grants plus immediate production state/action after decode.
- Access Requirement Prompt is readiness-safe at direct Porthole lookup/recovery; decoded state/action and wrong-key read/write negatives pass without granting or approving access.
- A decoded, registered, non-empty Event Atlas now feeds Participant source-backed preview before any fallback; all three known sessions survive immediate resolution, and wrong-key reads/writes remain denied.
- Conference Participant Shell now awaits a decoded Agenda before delegation; persisted state, real agenda actions, concurrent idempotency, stable grants, and wrong-key read/write denial pass.
- CellScaffold app Chat no longer launches decoded setup or searches/creates substitute global identities. Paid/authenticated HTTP and Conference chat hosts await it; known persisted state, real actions, concurrency, stable grants, and wrong-key read/write denial pass in one combined run.
- Conference Public Shell, Device Registration, the four-Cell notification dependency chain, ContactEndpoint, Agent Conversation Inbox, and both Personlog projections no longer launch detached decoded binding setup; every identified immediate host awaits readiness.
- The notification chain has a real persisted dependency reload gate. Contact and Agent have known-nonempty round trips followed by real mutations; Personlog has immediate real refresh/resync actions; concurrent grant stability and Contact wrong-key/no-mutation pass.
- Runtime `surfaceID` publication, versioned bootstrap reconciliation, remapping, removal, and persisted encode/decode re-instantiation work without recompiling the host route mapping, while the external link remains opaque and view-only.
- The repairs are serialized/idempotent under concurrent ensuring for the covered Cells.
- Same UUID with different signing key is rejected for runtime owner hydration in every focused repaired path recorded above.
- Selected production Workbench, Arendalsuka, Conference, and Co-Pilot local paths pass dynamic assertions.
- At the recorded staging observation, staging served the base revision and its read-only Arendalsuka known-data/security canary passed; this is not deployment proof for the later commits.
- Focused core, Binding repair/parity, HavenAgentD, cross-language, SwiftWeb, CellUtility, Spatial, DiMy, and Add2Entity suites have the results recorded above.
- EntityScanner now exposes explicit strict action/state contracts with exact
  grants and uses the real production boolean start payload in both core and
  Binding gates.
- Lobby publishes deterministic purposes, removes random dev-only lifecycle
  behavior, permits public reads only through an owner-authorized signed
  Agreement, and keeps updates owner-only.
- RelationalLearning persists and cold-restores a versioned sequenced journal,
  performs immediate decoded reads/actions, serializes mutation/journal/source
  flow order, rejects malformed and relation-shape-invalid events atomically,
  derives deterministic generated IDs, and denies action members arbitrary
  feed/emitter-factory authority. Its focused tests pass 14/14 and the complete
  CellProtocol package passes 756/756.
- Local GeneralCell Explore dispatch, strict enforcement, and catalog records
  distinguish GET from SET for the same key. Chat's 56 operations have 56
  complete contracts; exact child grants cannot fall through to legacy root
  handlers; decrypt is bound to live requester proof/signing identity/Agreement;
  invalid bulk targets fail atomically; and flows use Cell-owned authority.
- Perspective, CommonsResolver, CommonsTaxonomy, EntityAtlasInspector,
  FileCrypto, ContractProbe, GraphIndex, Vault, and Identities publish complete
  contracts before raw handlers. All nine expose their expected production key
  under strict enforcement in the regression gate.
- All errors currently emitted by the Explore regex/source audit are fixed
  under that model. The
  current repo-wide result is 0 errors and 19 conservative computed-key
  warnings; all 19 are manually mapped Apple false positives, the fresh strict
  Apple publication matrix is 24 operations / 20 keys, and Chat is 56 handlers
  / 56 complete contracts / 0 findings. This does not prove all-operation
  dispatch, decoded parity, complete remote/cross-runtime contracts, or absence
  of broader runtime/service defects.

Not proven:

- All CellProtocol functionality, all first-party products, all published Cells, or all persistence/restart paths are robust.
- Binding, HavenAgentD, Spatial, DiMy, Add2Entity, CellUtility, or HAVEN_MVP are safe for every persisted/decoded Cell; repaired paths still lack comprehensive separate-process restart/deployment proof.
- The local repair is deployed.
- Public device registration/callback authorization is safe; the live routes currently elevate unauthenticated input to Scaffold authority and require coordinated owner-approved device enrollment/proof.
- Every standard public button target is runtime-owned; versioned registry seeds now exist, but direct compiled factory fallbacks remain until owner-authorized Agreement issuance and the authenticated route path are green.
- The existing Demo Story decoded restore path; its exact state/action test currently fails `notFound` independently of the adjacent readiness hunk.
- Full web/native renderer and action parity.
- Deployment proof for the new runtime registry and native Binding launch path.
- The authenticated owner-published runtime-route HTTP path on the current
  published dependency graph; an earlier focused positive was red because
  legacy two-argument Agreement issuance was rejected, and this audit did not
  rerun the full live owner-publication journey after the later security fixes.
- A real OS cold-launch/deployed multi-scene journey; in-process targeting and iOS compilation are proven, but Finder/browser delivery into a newly created scene is not.
- Binding test-discovery repeatability and cross-suite shared-global isolation; the final full target is green, but one preceding false-green run omitted 51 planned cases and the older AppKit crash remains relevant infrastructure history.
- Owner-published Arendalsuka public read on the final release dependency graph; the historical positive failed before the strict-policy/TrustedIssuer integration repairs, and this task did not rerun that live owner-publication journey.
- Complete per-family persisted immediate state/action and separate-process restart proof for shared core Chat/Orchestrator/EntityAnchor/Calendar/Vault/GraphIndex/TrustPacket/TrustedIssuer/Commons; the shared activation boundary and local flow lifecycle are published, but those family-specific gates remain incomplete.
- Apple Intelligence hostile pre-decode allocation bounds, live Foundation
  Models semantics, a separate-process restore, and an actual production host
  draining its owner-only outbox; local persistence, contracts, access, action,
  concurrency, and wire roundtrip are proven, but those broader paths are not.
- Complete Explore contract coverage: the repo-wide source audit is now 0
  errors and 19 computed-key warnings, all manually mapped for Apple. Local
  fresh Apple publication and Chat source mapping are proven, but decoded/all-
  handler Apple behavior, remote method-aware `typeForKey`, cross-runtime wire
  fixtures, and transport consumers are not proven.
- RelationalLearning separate-process/crash/power-loss restore, hostile
  pre-decode allocation bounds, journal saturation/compaction, arbitrary
  replay-versus-incoming concurrency, legacy direct-engine journaling, and
  cross-runtime journal/ID golden-fixture parity.
- Complete unauthorized/wrong-identity/missing-proof/stale-proof/public-read matrices.
- Full cross-runtime parity from the current shared fixture corpus.
- Absence of every P0/P1 defect outside the investigated failure class and selected Purpose-driven paths.

Therefore all three Goals remain non-terminal. The committed readiness,
GeneralCell flow, Agreement/TrustedIssuer, and runtime-link paths preserve their
tested access boundaries, but `goal.haven.cross-repo.security-preservation`
cannot be terminal while device ingress still elevates unauthenticated callers
and live owner-published issuance/session evidence is incomplete across routes
and ports. The evidence supports continuing with narrow ownership-layer repairs,
one owner-published runtime registry, an enrolled-device capability migration,
and per-family restart/action gates above the now-published shared activation
and flow lifecycle. Kjetil remains the decision owner for the breaking device
rollout and any further versioned CellProtocol-core change.
