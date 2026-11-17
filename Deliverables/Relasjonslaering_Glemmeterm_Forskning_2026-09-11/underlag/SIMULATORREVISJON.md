# Independent simulator adjudication

Date: 2026-09-12. Read-only review; parent simulator was not edited by this reviewer. Reviewed `/tmp/relational-study/simulering/study.py` SHA256 `27a95dbe869f393c724f4f8f734ab8bcc38d0924ccf4a39754b79fa6185a9fa0` and `parity.py` SHA256 `c6e06826c3d7b83cd12ef024cf96652df3d124f8b5d4fcb3572bb956f3f45bf8`, plus preregistration. This is independent adjudication of a bounded exploratory experiment, not production implementation approval.

## Verdict

The main candidate matrix is suitable for **bounded instrumentation/design conclusions**, provided the report states the deviations below and the completed fresh run's hashes/replay checks pass. It does not establish a preferred production learning default from the authored target labels. No remaining matrix arithmetic bug was found after the parent fixed the ordering/reference issues identified below. Full-matrix runtime completion/results were still pending at this review; reported 17-fixture / 1,063 binary-float baseline parity was communicated by the parent, not independently rerun by this reviewer.

### C1: Does hybrid forgetting solve the observed clamp problem?

**No general solution follows.** For the fully active, symmetric, success-only case, bounded hybrid equilibrium satisfies

`0 = alpha*(1-w) - beta*(n*w)^2*w`, or `beta*y^3 + alpha*y - alpha*n = 0`, where `y=n*w`.

Hence equilibrium raw y<=1 requires beta>=alpha*(n-1). With alpha=.08, n=6 requires beta>=.40 and n=20 requires beta>=1.52; tested beta<=.08 does not meet either. This analytic control is for symmetric fixed activity and an equilibrium, not a proof of arbitrary discrete-time convergence. It explains why a lower norm or lower saturation fraction in selected logs must not be labeled a complete clamp fix. Clamped-y hybrid has equilibrium `w=alpha/(alpha+beta)` while y is saturated, so density remains decisive.

### C2: Is an L2 unit budget enough to solve scoring saturation?

**No.** `raw=w·x<=||w||₂||x||₂`; with unit weight norm and n fully active inputs, the raw maximum is sqrt(n). Equal weights reach sqrt(n), so n>1 can saturate clamp01. Unit budget is a weight-competition design, not a normalization proof. It also does not remain a global invariant after exact explicit preferences: six preferences of .6 have norm sqrt(6)*.6>1 until a later budget success. The dedicated preference control correctly exposes this tradeoff.

### C3: Can the synthetic labels justify a production default?

**No.** The generator explicitly rewards its chosen purpose with .9 success probability versus .3 for others. Performance relative to those labels is about that simulation. Candidate selection by those authored labels would be scenario-dependent tuning, not demonstrated utility for user preferences. A recommendation **AVVIST as production learning change now**, with a separate concrete ranking fix, is consistent with the evidence and preregistration. An exploratory budget candidate can be described as the simpler future comparison, without promoting it to approved production default.

## Verified strengths

- Baseline uses explicit sorted left folds, stored-weight updates and the same current Noa arithmetic order. The semantic union/gates/defaults match the audited engine on valid, unique plain-JSON synthetic inputs.
- Candidate y and the vector are frozen before any per-edge update. Competition reaches all known same-purpose edges; absence ablation contrasts this against eligible-only updates.
- Centered mode uses the prior 32 successful eligible episodes, zero for absent features, and does not include the current observation in its own mean. Projection to [0,1] is explicit; no centered PCA guarantee should be claimed.
- Failure remains baseline and preference events set supplied weights immediately. Competition-only absent-edge decreases retain timestamps, an explicitly documented candidate deviation.
- Tau-b handles all-tie input as undefined; deterministic total-ranking tau is distinct. Stable adaptation requires ten consecutive tops and retains right-censoring. Aggregates preserve observed-only median alongside censor count.
- The main matrix contains no parameter optimization using a weighted total. Pairwise direction preservation and seedwise win/loss/tie supplement cardinal comparisons.
- Runtime references cover saturation, ranking, tau, norm, weight change, bit difference, adaptation and—after review—top accuracy and signed margin.

## Issues found and resolved before fresh full run

1. Weight-change norm iterated an unordered set of edge keys. Hash randomization could change floating sum order and metric artifact bytes across processes even though replayed edges matched. Parent changed it to `sorted(set(current)|set(previous_edges))`; verified at study.py line 213.
2. Source hash was previously read only at end, allowing an edited script to be hashed instead of the one executing. Parent now snapshots it at main entry and asserts unchanged before manifest output (258,288).
3. Top-accuracy and signed-margin metrics lacked explicit instrument references if used in decisions. Parent added null/positive controls at lines 155–157.
4. Parent reported that an earlier Noa arithmetic mismatch was corrected (normalizing sigmoid product before multiplying by .95), older interrupted run discarded, and a fresh matrix started. Current lines 33–40 match the actual engine's operation sequence. Only fresh final evidence should be delivered.
5. Initial primary top/saturation metrics padded absent purposes with zero, unlike the engine. Parent now computes saturation and top accuracy from actual stored-purpose candidates, with no top when the candidate set is empty; verified in the final reviewed source. Histories record candidate_count. Padding remains only in explicitly diagnostic fixed-cohort comparisons.

## Required reporting limits, not requests to broaden implementation

- Diagnostic tau, signed margin and transform-sign comparisons pad all three candidate purposes A/B/C with zero to maintain a fixed comparison cohort. State this evaluation convention. Primary saturation/top metrics now use actual stored-purpose candidates and agree with engine candidate availability.
- Main `preference_change` simultaneously changes the desired purpose's success-probability regime and inserts a preference event. Its latency cannot be attributed solely to explicit preference. The separate immediate preference control checks exact weight/projection semantics, not an isolated product adaptation experiment.
- `edge_event_replay_equal` is a research-record edge projection check. It replays `en.updates` into an edge dictionary; it does not decode actual RelationalWeightUpdateEvent envelopes, validate their IDs, restore centering history or restore complete session/context/policy state. Use the phrase **edge projection equality**, with actual Swift source/weight/mixed evidence cited separately.
- The simulator's `weightUpdate` branch does not reproduce production generated-ID deduplication when lifecycle and generated updates are mixed. Its `seen` set contains source envelope keys, but internally generated updates have no production deterministic event IDs. Therefore the numerical source-log matrix is valid within scope, while general mixed-log replay parity is unsupported. Do not call it a complete reimplementation of event-sourcing contracts.
- `Engine.snapshot()` encodes edges and centered history, not all live session/context/policy/idempotency state. Closed, fully consumed main logs leave no open session; the measured exact-repeat claim should name the compared state. Current replay checks do not prove full engine-state reconstruction for arbitrary prefixes.
- Config values are fixed to defaults; malformed events, duplicate context keys, custom-zero eligibility and production journal capacity checks are outside simulator validation. Main source logs are small enough for production's 2,048-record cap; larger auxiliary controls are algorithm controls and should not imply persistence validation.
- “True Oja” is correct for the specified success equation, but the entire candidate retains baseline failure updates, nonnegative projection, an expanding observed feature set and fixed eta. Name it **Oja success-step candidate** rather than importing canonical convergence/PCA claims for the whole engine.
- Low L2 change can arise because all weights are suppressed. It is not inherently improved stability or usefulness. Interpret it beside margins, rankings, norm and projection behavior.

## Recommended HD-0051 ranking contract

Sort by raw score and purposeId only for an exact raw-score tie. A bounded display `raw/(1+raw)` is reasonable and strictly increasing over nonnegative real numbers. Do not sort exclusively by that transformed Double if exact preservation of representable raw distinctions is required.

Measured counterexample in Python Double: raw `4.0` and `math.nextafter(4.0,+inf)=4.000000000000001` both display as `0.8`. Likewise 10.0 and its next float both display as 0.9090909090909091. Thus zero sign changes on tested matrix pairs is an empirical result, not a proof that the Float transform never creates a tie. Raw ordering retains the distinction. Improvements from unclipping are recovered existing directional evidence, not newly learned information.

## Supporting original-engine test evidence

`/tmp/relational-engine-audit.md` provides provenance/line anchors and oracle restrictions. `/tmp/relational-oracle/build.sh` compiles the actual unchanged three production files and the actual unchanged original seven Engine tests with plain-JSON/CryptoKit dependency shims. Native XCTest ran 7 tests, 0 failures; `direct-tests-output.txt` and `source-hashes.txt` are preserved. This does not cover full CellProtocol package or CellApple contract integration. No production file or original test was edited.
