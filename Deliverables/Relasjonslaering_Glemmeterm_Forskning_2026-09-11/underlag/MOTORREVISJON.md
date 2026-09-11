# Source audit and bounded actual-engine oracle

Audit date: 2026-09-11–12 (Europe/Oslo). Scope: the handoff's F1–F6 and simulator parity semantics. No CellProtocol production files or tests were edited. No git mutations were performed. This is a source/instrumentation audit, not a claim that the suggested learning rule improves a product or models human learning.

## Provenance and brief audit

The handoff was treated as a list of hypotheses to check, not as an authoritative implementation specification. Local checkout `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol` is branch `pdd/tillitspakke-agentflaate`, HEAD `4096760fe2b47d93d65d143320acfb51b4d50ff7`; local `origin/main` is `c430a24c0d93d2cec9984149c4fb7546c6341bd3`. `git diff --exit-code origin/main --` for Engine, Models, Decay and Cell returned 0. This does not claim the remote was fetched. The checkout has substantial unrelated dirty/untracked work; none was touched. Events are declared in Models, not a separate Events file.

Sources abbreviated below (all relative to that repository):

- Engine: `Sources/CellBase/PurposeAndInterest/RelationalLearningEngine.swift`
- Models: `Sources/CellBase/PurposeAndInterest/RelationalLearningModels.swift`
- Decay: `Sources/CellBase/PurposeAndInterest/RelationalDecayPolicy.swift`
- Cell: `Sources/CellApple/PurposeAndInterest/Cells/RelationalLearningCell.swift`
- Tests: `Tests/CellBaseTests/RelationalLearningEngineTests.swift`
- Architecture: `Docs/RelationalLearning_Architecture_NO.md`
- Operations: `Docs/RelationalLearning_Bruk_og_Drift_NO.md`

SHA256:

| File | SHA256 |
|---|---|
| Engine | `1413b6114f52299be1c83b0e4934edce92c314a8f1303b47ddc2017f5bb1ddc8` |
| Models | `758bad42c7055304dfd709af62082e5bbf3341f4f36314545eeccf357c0d1f75` |
| Decay | `42d50aba5917e2782091fd0c366dad4c9badafaecf269cd135d3ae2b9f1550fe` |
| Cell | `cfdbf8034a140bd405a40729fd25faad28f48b397731c0f9b5691388fba06774` |
| Engine tests | `2d24095fa9a7d6e491099e1e3a84642fd7d5ac4bcdd85d3dcb655937a64305c4` |
| Cell contract tests | `e37754a3cacd9e7291eb4cb20eb600cd6d1d8269bf43a90766410deb9795aed4` |
| Architecture | `742ff05b93a63798d0aee2d83b029bf7ad745d534b07e3178b37f5c53d3790ca` |
| Operations | `08ecb10de902bebfac8ebd1885cb1c3c3dcd107872fbfcc0cd39960afc8ad811` |

Both prompt files were read. `relational_learning_deepresearch_prompt.md` has a broader candidate-table requirement (3 update rules and 3 decay families) than the handoff alone. `relational_learning_code_assistant_prompt.md` requests additive APIs, replay, edge explainability, local processing and versioned decay. These are delivery constraints for a future implementation, not permission to alter production code here.

## F1–F6 adjudication

| Claim | Audit verdict | Evidence / qualification |
|---|---|---|
| F1 today's bounded success/failure rule | Confirmed | Engine 629–645; defaults Models 448–456. Success is `w + a e (1-w)`, failure `w - a e w`, clamped. This is not literally canonical Oja/Hebb `eta*x*y`. Explicit preference is the event's supplied weight, default 0.6, not invariably 0.6: Engine 338–389, Models 283–305. |
| F2 decay is separate versioned read-time layer | Confirmed, with timestamp nuance | Engine 461–477, 686–703; Decay 39–64, 81–110. Learning changes stored weights without applying Noa; scoring multiplies retention. Every generated lifecycle update, including FAILURE, resets `lastReinforcedAt` to completion time (Engine 302–309). |
| F3 score saturation and alphabetical ties | Confirmed with material corrections | Models 518–520; Engine 434–469, 497–502. Six active stored edges after one default success give raw 1.032 and score 1 in the actual compiled engine. Ten stored 0.1 edges give raw 0.9999999999999999, not exactly 1 under Swift left-fold floating addition. Eleven give 1.0999999999999999 and score 1. An unknown relation does not contribute 0.1 at scoring: absent edges produce no candidate or contribution. `unknownWeight` is the default previous weight only when a trace creates an edge (Engine 285–300). |
| F4 eligibility not centered | Confirmed for active trace values; qualify absolutes | Eligible defaults are nonnegative 1, .3, .5*confidence, not centered. But absent features have zero eligibility at scoring, and `purposePurpose` always zero (Engine 649–684); custom config can set active/passive eligibility zero. Missing traces are not iterated during learning. Dominance of an always-active feature is a hypothesis to measure, not established solely by positivity. |
| F5 mapping formål to Oja post-node | A design proposal, not code fact | Purpose is the aggregation target semantically although stored graph edges point outward; Engine 429–469 and Models 23–27. Choosing y=raw, clamped raw, stored-weight score, or effective-weight score has not happened in the engine. Current success lacks Oja's `y` factor. Adding only `-eta*y*y*w` to current success is not canonical Oja and inherits no Oja unit-norm/PCA theorem automatically. |
| F6 no forgetting-policy event/config exists | Confirmed; migration risk measured | Models 83–105, 309–341, 459–487. Config is engine-initialization state, not part of source journal. Generated IDs encode source ID/outcome/edge identity, not learning config or policy (Engine 533–551). Replaying lifecycle logs under changed config changes history; including old generated weight events does not reliably protect it because generated IDs are already marked applied. |

## Exact episode and eligibility semantics for simulator parity

1. Sessions are keyed by purpose ID, not a globally unique episode ID (Engine 53, 239–250). A second `started` event for the same purpose replaces the prior session. The stored start event ID/time do not enter the update formula. Completion without start is accepted and creates a session from the completion payload.
2. Start copies active/passive interests/entities into sets. Completion unions each corresponding set. Active and passive membership can coexist; trace upsert keeps the strictly larger eligibility. At default config active wins. Equal eligibility preserves the first inserted trace/reason, hence active at equal config values (Engine 17–40, 554–626). No within-episode continuous activity integration is implemented.
3. Context identity is the string `domain:blockId` (Models 220–237). `contextTransition` replaces one global signal per domain (Engine 226–235); `fromBlockId` does not affect state transitions. The session records global contexts at start and completion. Intermediate transitions are not accumulated into open sessions. Thus A(start)→B(intermediate)→C(completion) produces A and C traces, not B.
4. Start/completion explicitly provided context blocks are merged by node ID, then global current contexts overwrite identical IDs (Engine 242–255). Different IDs of the same domain can coexist in the session. A low-confidence current signal can replace a high-confidence payload signal for the same node.
5. A lifecycle-level `contextConfidence` gates the entire episode (Engine 256–258), defaulting to 1 if absent. Completion non-nil confidence replaces start confidence; absence retains start confidence. A <.6 confidence drops interest/entity updates too. Independently each context signal must have confidence >=.6 and contributes `.5*confidence` (Engine 597–606).
6. Unknown edges begin at `unknownWeight` only for traces being learned. Existing edges absent from the episode are not updated and retain timestamps. To apply `-eta*y²*w` when x=0, a candidate must explicitly expand the update scope to other already-known edges of the same purpose. That is a documented semantic change, essential to the desired competition test.
7. Baseline completion (success/failure) emits one update per trace, including zero configured eligibility, and refreshes timestamp even when delta is zero (Engine 278–332). A forgetting-only update that blindly reuses this behavior would refresh Noa timestamps on unrelated edges; v2 must specify what counts as reinforcement versus update time.
8. Config's `explicitPreferenceWeight` is currently unused by `deriveExplicitPreferenceWeightUpdate`; the event initializer's default uses the static default 0.6. Simulator preference events should carry an explicit weight.
9. Duplicate context node IDs in a start payload or score snapshot can trigger `Dictionary(uniqueKeysWithValues:)` precondition failures (Engine 25,442); validation checks signal shapes/confidence but not uniqueness (809–814). This was identified in source, not crash-tested. Keep synthetic inputs unique and report this rather than inventing a merge rule.

## Scoring, order and floating-point constraints

Scoring iterates only stored edges, groups by purpose ID, includes purposes with stored edges even when the query makes all contributions zero, and produces no absent-purpose candidate (Engine 434–449). Snapshot eligibility is separate from lifecycle eligibility; global active contexts are not automatically inserted by Engine.scorePurposes. Supply the explicit snapshot.

Sum order: relationType.rawValue, target node type rawValue, target node ID, then lastReinforcedAt (Engine 716–727). Accumulation is a `rawScore += contribution` loop (469), not a compensated sum. Python 3.12+ built-in `sum` may use compensated addition, so use explicit ordered left-fold loops for parity. `edges()` sort uses purpose ID, relation type, target ID (506–517). Ranking uses normalized score descending and purpose ID ascending only on exact score equality (497–502). Explain ordering is contribution descending, relation type, node type, node ID, effective weight descending, timestamp descending (729–746); even explainTopN=0 returns a prefix of at least one item (483).

Noa exact formula: delta=max(0,now-lastReinforcedAt); scaledK1=max(1,k1*t1), scaledK2=max(1,k2*t2); sigmoid product is divided by its value at delta=0, then mapped into [rMin,1] and clamped (Decay 85–110). Do not use a sigmoid with k as a bare inverse-time slope. At zero/negative delta retention=1; at large positive delta approaches .05. Policy at score time is latest effective policy by profile, then version; fallback is edge version, otherwise latest candidate, otherwise defaultNoa (Engine 686–713). Learning stamps selected current Noa profile/version, including for preexisting edges.

All measured values below are from actual unmodified Engine+Models+Decay with the support shim described below. For seeds, 0.1 edges were explicitly stored via preference events; they were not unmaterialized unknown edges. Seed query time=0; success query time=100 and learning completion=100, ensuring R=1 for compared rows.

| Stored edge count | Seeded raw (w=.1) | Seeded raw IEEE754 big-endian hex | After one success raw | Success score |
|---:|---:|---|---:|---:|
| 2 | 0.2 | 3fc999999999999a | 0.34400000000000003 | 0.34400000000000003 |
| 6 | 0.6 | 3fe3333333333333 | 1.032 | 1 |
| 10 | 0.9999999999999999 | 3fefffffffffffff | 1.7199999999999998 | 1 |
| 11 | 1.0999999999999999 | 3ff1999999999999 | 1.8919999999999997 | 1 |
| 20 | 2.0000000000000004 | 4000000000000001 | 3.440000000000001 | 1 |

## Replay paths and measured migration trap

Three distinct routes matter:

- `applyEnvelopeTransaction` validates and applies input in arrival order. It deduplicates by eventType|eventID, generates and immediately applies lifecycle/preference weight updates, then journals only the SOURCE envelope (Engine 99–170).
- `replayTransaction` prevalidates the batch and sorts by emittedAt, eventType raw string, eventID, canonical JSON payload, then uses the transaction function (173–195,764–781). Raw event-type order at ties is contextTransition, decayPolicyUpdated, explicitPreference, purposeLifecycle, weightUpdate.
- `restore(from:)` walks persisted journal SEQUENCE, never sorting by timestamp, and requires exact revision reconstruction (79–96). This preserves arrival order, which need not equal sorted replay.

The public low-level `ingestPurposeLifecycleEvent` derives but does not apply returned edge updates or journal source events. `applyWeightUpdateEvent` applies the supplied newWeightStored and edge timestamp/metadata directly, ignores previousWeightStored consistency, and performs no rule recomputation (392–403). Its direct API is less validated than transaction API. Source lifecycle/preference generation applies IDs before later duplicate emitted weight events can apply.

Cell.handleLifecycleEvent journals/applies source, emits source, then emits each generated update (Cell 376–405). This supports source-only journal restore, generated-weight-only edge reconstruction, and mixed transport logs with idempotency—provided derivation semantics are fixed.

Measured config change from alphaSuccess .08 to .2 on the SAME episode:

| Replay input | Active-edge final weight |
|---|---:|
| Original source log, old config | .17200000000000001 |
| Original source log, new config | .28 |
| Original generated weight events only, new config | .17200000000000001 |
| Mixed old source + old weight events, new config | .28 |

Files: `/tmp/relational-oracle/{old_sources_new_config,old_weights_new_config,mixed_old_sources_weights_new_config}.{input,output}.json`, `migration_summary.json`. This is a measured counterexample to “old update events make changed source replay automatically safe.” A v2 needs deterministic learning-policy selection at source timestamp and old default fallback; adding config fields alone does not freeze history. Events' canonical ID version can identify algorithm changes, but distinct IDs alone do not resolve conflicting old/source-generated mixed updates without a specified authority/deduplication rule.

Measured tie-order counterexample: arrival `[started(id=z-start,t=0,feature=start-only), succeeded(id=a-end,t=0,feature=end-only)]` learns both edges. Sorted source replay runs a-end first, learns only end-only, and leaves z-start pending. Exact journal restore preserves both. This is a concrete scoped follow-up for equal-time ordering semantics, not a reason to broaden this research into a runtime rewrite. Deterministic replay of a fixed sorted log can still be perfectly repeatable.

Journal hard bounds are 2,048 records / 2 MiB and version=1 (Models 138–185). `ensureJournalCapacity` pre-counts adding envelopes, including duplicates before idempotence (Engine 749–761), so batching old duplicate replay can fail capacity even when fewer would ultimately apply. Large simulation logs must either keep per-scenario within bounds or clearly report bypassing the production persistence envelope limit.

## Bounded oracle and original tests

Directory: `/tmp/relational-oracle/`.

`build.sh [CellProtocol path]` compiles the actual three production files by their original paths with no edits. It also compiles those same files as a temporary testable module CellBase and compiles/runs the unchanged original seven Engine tests using native XCTest.defaultTestSuite. Build uses only paths under /tmp for artifacts/module caches. Swift version: Apple Swift 6.2.4, arm64-apple-macosx26.0; Xcode framework paths are derived with xcode-select.

Support.swift is an explicit **limited dependency shim**, not production ValueType: plain JSON bool/int/double/string/object/list/null with matching primitive decode order; Object alias; only FlowElement's content/topic/id fields; ValueTypeError; SHA256 via Apple CryptoKit instead of package Crypto. The three production files themselves are unmodified. The synthetic events use only that subset. No claims are made about wrapped ValueType values, the complete Flow layer, real CellBase package wiring, CellApple integration or concurrency contracts. Production ValueType's wrapped decoders, malformed-object behavior and wide dependency graph are not reproduced. This is a bounded engine oracle, not a passing full CellProtocol build.

Rebuild and tests:

```sh
bash /tmp/relational-oracle/build.sh /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol
python3 /tmp/relational-oracle/fixtures.py
```

Arbitrary input:

```sh
/tmp/relational-oracle/oracle < input.json > result.json
python3 /tmp/relational-oracle/run_jsonl.py events.jsonl --queries queries.json > result.json
```

Input.json: `{events:[RelationalLearningEventEnvelope],queries:[{at:timestamp,snapshot:RelationalContextSnapshot}],config?:RelationalLearningConfig}`. Include all array fields in snapshots and lifecycle payloads. Oracle applies events in input order, returns final edges, scores at each query timestamp, generated updates and journal. It compares sorted replay, ordered journal restore, generated-weight-only reconstruction and mixed-log reconstruction to arrival state. Querying an old timestamp after later events does not reconstruct historical edges; it only changes decay time. Use a prefix per historical query. Flags concern encoded edge equality, not full intermediate session/policy state; weight-only reconstruction does not retain source sessions/context or policy updates.

Eleven instrument fixtures are in `fixtures.py` with complete raw input/output and `summary.json`: empty graph, saturation, session union and A/B/C transition, global context overwrite, whole-episode confidence gate, inherited start confidence, double-start replacement, failure timestamp refresh, absent-edge no update, equal-time order, explicit preference override. Ten fixtures have all four edge equality flags true; equal-time fixture intentionally has replayEqual=false while journal restore/mixed/weight-only match arrival. The fixture expected behavior is recorded, not silently “fixed.”

Original seven tests executed: replay identical edges/scores, Noa monotonic endpoints, policy cutover, journal restore/generated IDs, invalid replay atomic rejection, oversized journal rejection, invalid edge-shape rejection. Result: **7 executed, 0 failures**, native XCTest, first success 2026-09-12 00:04:40 local; rerun by preserved build.sh also passed. Evidence `direct-tests-output.txt` and `source-hashes.txt`.

## What did not work and limits

- SwiftPM temporary isolated package attempt failed before target compilation because nested `sandbox-exec` returned `sandbox_apply: Operation not permitted`. Captured `test-output.txt`. No sandbox disabling or shared .build workaround was used.
- Initial direct XCTest compilation needed Xcode platform framework/import/library/rpath flags; cross-platform XCTMain/asyncTest helpers are unavailable in Apple's XCTest. Replaced harness with native defaultTestSuite, retaining original test file unchanged. Final build.sh is reproducible and passes.
- Full package and seven `RelationalLearningCellContractTests` were not executed. Contract-test source names cover decoded grants, journal persistence/replay atomicity, concurrent reinforcement and source flow order; that is outside a standalone engine shim's validity.
- Duplicate context-key crash path identified by source only; not executed.
- The original tests do not validate a new Oja rule, centered-state evolution, policy migration or usefulness of score rankings. New measured reference fixtures are still required before those endpoints gate anything.

## Suggested parent simulator parity fixtures / decisions

Use ordered source envelopes for all rules, identical explicit scoring snapshots, fixed seeds, synthetic-only logs, per-scenario journal sizes below bounds. Compare baseline to this Swift oracle at every completion or selected deterministic prefixes for edges, timestamps, reasons, raw scores and raw bits. Compare same-runtime deterministic hashes separately from cross-runtime tolerance checks involving exp; do not label numeric tolerance as bit equality. Avoid Python compensated sums in baseline.

Minimum parity: start/end unions with duplicate active/passive membership; both context confidence gates; final/global overwrite; A→B→C sampling; completion without start; double start; absent existing edge unchanged; explicit preference weight other than .6; failure timestamp refresh; mixed/source/weight-only replay; same-time reversal; policy cutover at exact boundary; zero eligibility custom config. For candidate comparisons document expanded x=0 update scope, frozen pre-update y and vector, whether failure also forgets, whether preference immediately projects a norm, and which timestamp a competitive decrease uses. Pure Oja, bounded additive forgetting, centering and budget projection are distinct algorithms.
