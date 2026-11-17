> Fresh-ref update, 2026-09-18: see [FRESH-REF-UPDATE-20260918.md](FRESH-REF-UPDATE-20260918.md). CP/MP recovery packages are now on main; all configured remotes were fetched by root. The historical findings below retain their original snapshot context.

# Supplemental branch adjudication — 2026-09-17

This supplement supersedes the broad Mint, issuer-wallet, and Overlay recommendations in `AUDIT.md`. It is a read-only source review, not a successful build, production-state inspection, migration, or deployment. No network, builds, credential contents, personal records, Git mutation, or source edits were performed by this audit slice. Root owns integrations. Handoffs and older agent decisions are historical evidence, not fresh user instructions.

The complete inventory is in `inventory-enriched.json`, `branches.tsv`, and `dirty-code-inventory.json`. Detailed source snapshots and overlap evidence for this supplement are in `supplement-evidence.json`.

## Integration decisions

| Work | Decision | Smallest complete source package / current replacement |
|---|---|---|
| CP pdd/tillit | Integrate with current main guards | Root already integrated into candidate `38eed77`; retain main relation-signature validation and bound Skeleton modifiers. |
| CP bridge provenance | Integrate | `5fa0b96` + `f141c53`; root candidate `0d3d167` already includes it. |
| CP native parity | Integrate exact renderer deltas | Only SkeletonView hunks from `6218ed591387c7f2899a4441186e4877398def59`, then `fa7982d7fd5ecb3156ad2e576b9860e2ff3aca51`; preserve newer main modifiers. |
| CP entity continuity | Integrate optional package | `436b6a7`; root candidate `4f976a0` includes it. Network discovery is client-local and does not need a new production server service. |
| CP old Overlay element | Superseded / incomplete | Current `SkeletonModifiers.presentation` plus web presentation runtime and Binding `SkeletonPresentationOverlayView` cover this purpose. Do not add the duplicate incomplete enum from `ab5ead7d`. |
| CP signed caller / bridgehead | Relevant paired work, not proven deployable as-is | CP `04068ac1` and CellScaffold `ec437501` must be assessed together; replay/endpoint acceptance tests and server corrections required. Root currently excludes it. |
| MP issuer-bound wallet | Relevant unfinished hardening, not demonstrated superseded | `1a664f396917237d4bcee42dbcf58c9eb047c984`; runtime and migration defects below preclude an as-is production migration claim. |
| Mint legacy funding/payment hardening | Superseded for production; preserved test-only legacy work | Main's explicit Stripe entitlement provider contract and disabled public legacy routes are authoritative current product behavior. Do not enable old funding/mint/redeem HTTP routes. |
| Mint Stripe provider hardening branch | Already represented except newer main pin/gate metadata | Current main retains provider code and more recent release checks; do not replace main workflow/docs/verification script with older branch versions. |

## DiMyMint: concrete replacement, not age-based rejection

Reviewed main: `25b679bafcb37d42709c15615274fcf1c19b86db`. Main commit `e24dc84` deliberately introduced the Stripe entitlement provider boundary. The written replacement is `docs/stripe-entitlement-provider-v0.md` on main:

- Product purpose is `purpose://access.entitlement.payment-evidence`; service-local, nontransferable access entitlement / usage quota in Stripe test mode. Payment confirmation alone is not a Cell capability.
- Legacy public routes are deliberately disabled. There is no public provider route, automatic token issuance, production Stripe activation, or deployment path in this package.
- Wallet/stored value, redemption, reserve, payout, transferable value, cash-out, and multi-vendor acceptance are outside this provider's v0 scope.
- The replacement binds test account, order, subject, Agreement, product, amount, and currency and applies transactional Postgres entitlement issuance. Its tests include concurrent delivery; raw provider request bodies are not the intended evidence record.

Code enforcing that contract:

- `Sources/DiMyMintHTTP/MintHTTPRoutes.swift:82–86`: public router initializer uses `exposedRoutes = []`. Internal `localTestExposure` exists only to expose legacy handlers to local tests; handler dispatch rejects unexposed routes.
- `Sources/DiMyMintServer/DiMyMintServerMain.swift`: startup checks the public router and throws `publicHTTPExposureDisabled` before legacy funding/store setup.
- `scripts/verify-stripe-entitlement-provider.sh`: verifies exact dependency pins, disabled route source guard, tests, and the real Postgres provider migration/integration gate. `.github/workflows/stripe-entitlement-provider.yml` uses the matching pinned dependency checkout. Preserve these gates and update their matching pins only with an intentionally integrated dependency release.

**Disposition:** retain this current main behavior. Do not force the old money routes into the Butler deployment to satisfy a branch count. This is a documented behavioral replacement, unlike administrative rejection of old/no-PR branches. Root explicitly selected this disposition after review.

### Legacy source correspondence and conflicts

`micropayments-production-hardening` at `cce8f1e8402f0354851f1f97e2ee78d492cd8268` contains `a77ab51` funding hardening, `656ccad` older CI, and `cce8f1e` economic capture idempotency. `codex/dimy-entitlement-payment-hardening-20260719` at `96e8c91` contains equivalent product changes as `0c409e3` + `96e8c91`, with intermediate `69f19aa` older CI. **The two tips differ only in Package.swift / Package.resolved.** No product feature requires merging both histories.

If this legacy library work is later rehabilitated, the smallest product combination is `0c409e3` + `96e8c91`, keeping current Package.swift, lockfile, current entitlement workflow, public HTTP route disable, and server startup refusal. The route/server/tests conflicts cannot be resolved by taking the legacy side. Changed-path overlap with current main is Package.swift, MintHTTPRoutes.swift, DiMyMintServerMain.swift, and MintHTTPRouterTests.swift; the older production-hardening branch also overlaps Package.resolved. This is a changed-path overlap map, not a promise that Git will produce textual conflict markers on every path.

The branch `codex/stripe-entitlement-provider-hardening-20260719` at `bdf0e6e` has 13 of its 16 changed paths exactly equal to main; its remaining workflow, docs, and verification script are older than current pins and current DB gate. Preserve main.

### Reasons the legacy changes are not ready to activate

These are concrete source defects beyond the product replacement:

1. In `FundingService.swift` at `96e8c91`, webhook handling records a provider event before applying payment/cash/wallet projection effects (roughly lines 421–522). A store failure after event insertion makes retry classify the event as duplicate and skip the incomplete effect. The cash uniqueness barrier does not make all the later writes transactional.
2. `issueFromReservation` checks replay, consumes the reservation, then records coins, wallet event/balance, and finally the idempotency response (roughly 552–647). A crash after reservation consumption prevents a clean replay and can leave incomplete issuance.
3. Reservation reads/writes are separate awaited store operations (roughly 181–244). Actor isolation does not hold one logical transaction across awaits; concurrent reservations require an actual operation gate/DB transaction, not merely the actor declaration.
4. PostgresFundingStore uses individual execute/query operations. Atomic `insertPaymentCaptureIfAbsent` is a useful single-statement barrier but does not repair the multi-write failure cases.
5. Legacy `EnvironmentStripePaymentSessionCreator` accepts any nonempty `STRIPE_SECRET_KEY` and posts Checkout sessions. It does not enforce the current main provider's strict test-only boundary. No key contents were read.

Migration risks, if that work is revived:

- `0002_micropayments_production_hardening.sql` adds idempotency records, issued coins with ledger references, and spent serials. Main already contains a different `0002_stripe_entitlement_provider_v0.sql`; runners that key migrations by numeric prefix need an explicit version resolution.
- `0003_payment_capture_economic_idempotency.sql` creates a unique partial index on captured provider-payment IDs. Historical duplicate captures would make it fail. Check counts against a DB clone before migrating; never silently delete history.
- The current provider release script applies/tests its exact entitlement migration, not the legacy migrations. Passing that gate would not validate a new legacy schema.
- Require failure injection at each persistence boundary, same-event retries after restart, concurrent reservations/issuance/capture, replay consistency, migration from populated synthetic v1 data, and reconciliation. Existing FundingServiceTests / PostgresFundingStoreTests mostly test sequential success and mock SQL behavior, and do not establish crash-atomicity.

## DiMyMicropayments issuer branch: still consumed, incomplete

Reviewed main: `c3544c2f7b9be967a71dd9d8c87ae1a999f707a2`. Branch `1a664f3` is one unique commit, six behind main in the original snapshot, changing nine paths. Package.swift is the only overlap with main; retain current dependency pins and add only its `DiMyIssuerSegregationTests` target to the current manifest.

**It is not justified to call this wallet implementation obsolete because Mint adopted an entitlement contract.** Current source uses the same primitives for entitlement metering:

- CellScaffold main `configure.swift:1540` calls `DiMyCellRuntimeRegistration.registerScaffoldCells` under existing bootstrap and verified production-owner guards.
- MP `DiMyCellRuntimeRegistration.swift:49,57` registers `DiMyWalletRuntimeCell` / `DiMyAccessRuntimeCell`; Scaffold wallets/access cells use identity-unique, persistent scope.
- CellScaffold `AIGatewayCell.swift:235` defaults to `DiMyAIGatewayQuotaAuthorizer`. `AIGatewaySupport.swift:1367+` invokes `cell:///DiMyWallet.spend` and `cell:///DiMyAccess.verifyAndRedeem` for `.prepaidDimy` requests.
- `PaidAIUsageCanarySupport.swift:133` constructs that mode, labeling the product `usage_quota`. PaymentGate also resolves wallet/access primitives.

This establishes a conditional production code path, **not proof that production currently has any wallet state or active traffic**. This audit did not inspect production environment values, database records, or individual balances.

### What the commit contributes

One-issuer WalletCell behavior, mixed-issuer AccessCell bundle rejection, optional accepted mint allowlist, optional minimum key epoch, runtime type binding hooks, and schema-2-to-3 migration partitioning nonmatching coins into quarantine. These are relevant safety improvements if the wallet path is used.

### Corrections required before claiming the full feature deployed

1. `DiMyWalletRuntimeCell` changes `public final class` to `public class`, while its advertised use is external subclasses overriding `boundMintKeyID`. It must be `open` to permit cross-module inheritance. `@testable import` in IssuerBoundWalletCellTests masks this consumer problem. Test an ordinary importing consumer.
2. `MintPublicKeyRegistry.currentEpochByKeyID` is set only by the explicit initializer. `.runtime()` parses the existing public-key JSON but never loads epoch configuration. Runtime wrappers therefore expose `currentKeyEpoch = nil` and do not enforce retirement policy. Tests injecting a custom registry do not prove runtime policy. Define and validate the runtime minimum-epoch contract before using it; the implementation currently accepts epochs >= the threshold, rather than only exact equality.
3. `DiMyAccessRuntimeCell` constructs AccessCell without the new `acceptedMintKeyIDs` argument, leaving the default nil allowlist. Mixed bundles are rejected, but an issuer-specific merchant acceptance policy is not wired. State the actual policy rather than claiming allowlisted acceptance.
4. Quarantine decode uses `try? decodeIfPresent(...quarantinedCoins)` and replaces any error with `[]`. Malformed present quarantine must fail decoding; only an absent legacy field should default empty. Silently dropping persisted records contradicts its preservation goal.
5. Before partitioning, decoding requires all stored/quarantined/pending coins to verify against the current public-key registry. A foreign/retired issuer whose verification key has disappeared causes the whole decode to fail rather than preserve quarantine. Retain the needed verification keyring or define a safe explicit unverifiable-record state. Do not discard signed inventory.
6. `cachedBundles` are carried through unchanged after inventory partitioning. Foreign/mixed/retired pending bundles need explicit migration/rollback handling. The tests currently exercise the partition helper, not a complete encoded persisted runtime migration.
7. Schema 3 is not readable by the old schema-1/2 runtime. Rollback must preserve the pre-migration snapshot or use a compatible binary; switching an old executable onto rewritten data is not a rollback plan.

**Recommendation:** preserve this branch as relevant unfinished integration work; repair and test it before any wallet state migration. Do not claim it is already replaced, and do not deploy schema 3 solely to make every old branch disappear. If included in the recovery, the complete package is the commit plus the corrections above, current pins, and consumer persistence verification. Root decides integration sequencing.

Test target requirements: full MP suite, IssuerSegregationTests, IssuerBoundWalletCellTests, ordinary external consumer subclass compilation, full runtime encode/decode/restart from synthetic schemas 1/2, malformed quarantine, unknown/retired issuer keys, wrong issuer, mixed bundles, existing pending bundles, reservation rollback/completion, and unchanged issuer grant/access behavior. Test current CellScaffold PaymentGate and paid-quota consumer against the exact candidate dependency pin without issuing live charges.

## CellProtocol decisions and verification

Reviewed origin/main: `36372c5b95a7b57fbef92ffa54dea13bdf75a9e6`. Root candidate observed during review already had `38eed77`, `0d3d167`, `4f976a0`. Root continues changing it; these are a snapshot, not a final deployment SHA.

### Native parity: integrate the exact remaining layout change

The remaining native layout change is appropriate to preserve. **Do not merge the entire old parity branch or replace its whole SkeletonView file.** `6218ed5` also changes 102 resolver lines already represented by the tillit integration. Use only its SkeletonView hunks plus the full one-file `fa7982d` patch:

- HStack default spacing 8→10; frame alignment center→leading.
- VStack internal/frame alignment center→leading and default spacing 8→10.
- Section internal alignment leading, spacing 10, plus full-width leading frame.
- CellText frame alignment center→leading.

Preserve current `.applySkeletonModifiers(..., userInfoValue: userInfoValue)` calls, dynamic hAlignment/background bindings, relation security, List/followTail support, localization, and action resolution. No schema additions are required. Main web `porthole-webo.css:2270,2375,2955` confirms default gap 10 for these stacks/sections, but matching spacing alone is not semantic parity.

**Neither original commit adds tests.** Existing `SkeletonStyleParityTests` checks style-token vocabulary normalization, not native geometric rendering. Existing Binding `SkeletonRendererParityTests` covers navigation, visibility scopes, dynamic labels/payloads, list rows and NavigationBar; it does not assert these geometry changes. No tests were run by this audit.

Suggested real verification for the integrating owner:

1. CP `SkeletonTests`, `SkeletonStyleParityTests`, `SkeletonLocalizationTests`, `SkeletonActionButtonExecutionTests`, and `SkeletonButtonResolutionTests` on the candidate using its documented manifest/test commands.
2. Binding/macOS build against the exact candidate CP pin, with current `SkeletonRendererParityTests` and `ChatWorkbenchParityTests`. A Linux-only server build cannot compile/verify the SwiftUI layout.
3. Matched configuration in web/native: default and explicit-spacing HStack/VStack; Section with long wrapping header/content/footer; text with explicit leading/center/trailing modifiers; chat rows with per-item alignment/background; visible composer action and followTail after adding messages. Capture screenshots/semantic content and exercise actions. Explicit alignment must override defaults; include this as a regression check.

| Selected scenario | Schema/source | Web capture | Native capture | Action/geometry verdict |
|---|---|---|---|---|
| Default H/V/Section/Text | Existing supported schema; exact source delta reviewed | Not captured by audit | Not captured by audit | Pending integrating-owner verification |
| Explicit row alignment/background | Current main bindings must be retained | Not captured | Not captured | Pending regression verification |
| Chat composer / thread followTail | Existing current behavior must be retained | Not captured | Not captured | Pending dynamic verification |

### Bridge provenance: preserve the fail-closed behavior

`5fa0b96` makes `VaporBridgeTransport.identityVault(for:)` always return a BridgeIdentityVault for remotely presented identities, even when a remote descriptor copies a local identity/key or has no usable delegate. This prevents a remote descriptor from borrowing a local server signing vault. Visitor metadata registration remains separate. `f141c53` adjusts the test's expected AsyncError wrapper without weakening the denial. Run VaporBridgeTransportTests and existing BridgeIdentity / resolver security tests. Root already integrated the pair.

### Overlay: a real replacement exists

`ab5ead7d` introduces SkeletonOverlay with presentation state and dismiss fields but renders it as an unconditional native VStack; the proposed state/presentation/dismiss fields are not consumed. Its three test methods are located inside a private SkeletonElement extension, not the XCTestCase, so they are not test discovery evidence.

Current main already offers `SkeletonModifiers.presentation: SkeletonPresentation` (including overlay/drawer/sheet/popover/modal, open state, close action, backdrop, Escape/focus behavior and accessibility). Web `skeleton-runtime.js:4758+` consumes this presentation contract. Binding main `Binding/SkeletonPresentationOverlayView.swift` extracts `modifiers.presentation`, orders presentations, renders backdrops, and dispatches the configured close action. Keep this current mechanism; do not add the incomplete duplicate enum. Any old configuration using the draft element would need explicit translation to the current supported presentation contract before claiming it works.

### Nearby entity continuity: optional native adapter, not remote authority

`436b6a7` adds `Packages/CellNearby`, separate from the main server/runtime package. Its contract limits publishing to an existing invite, Bonjour metadata to protocol version + trusted HTTPS origin + random opaque offer + expiry, publishing to five minutes, discovery to two minutes, and redemption to trusted HTTPS without redirects before signed owner-link review. It grants no Cell authority by itself. Binding continuation/person-read-route work consumes it; native app usage-description/Bonjour declarations and actual local-network permission are required.

Run package tests and its synthetic two-process `Scripts/smoke_nearby.py` per README in an allowed local Network environment; report physical iPhone/macOS discovery separately. A server build does not test Bonjour or user permission. Root already integrated it.

### Signed caller: preserve the work, pair and verify before activation

CP `04068ac1` sends the signed proof it already creates using `bridge_proof` and `bridge_signature` query parameters plus provider query items. It validates own-vault reference/key/nonce and retains current cache identity/fingerprint/vault isolation and transport policy. The actual server consumer is **CellScaffold `ec437501`**, `Sources/App/Controllers/VaporCellBridge.swift`, not a file named VaporBridgehead.swift. It also registers a default-on bridgehead route unless explicitly disabled.

The server reconstructs the public key from the signed fingerprint, validates challenge scope/time/signature, and checks a resource based on `cell://<configured audience>/<cell name>`. But replay protection is an optional `if let signingChallengeReplayStore`; absent store accepts a valid replay. Require fail-closed absence behavior or a mandatory initialized replay store before activation. Verify exact resource agreement for host, port, path, and provider contract query variations; the client signs its full logical endpoint while the server reconstructs one from audience/cell name.

The CP commit's two added tests only assert provider query items are included/omitted in a test URL helper. They do not establish the signed upgrade path. The pair requires valid/forged/stale/repeated proof, wrong host/cell, absent replay store, connection lifecycle and actual remote-cell action tests, retaining the new provenance denial. Do not infer deployability from URL-construction tests. Root currently excludes this incomplete pair.

## Older rejection decisions: what the records actually establish

`HAVEN-Deploy/_handoff/ENDRINGSPAKKER/beslutninger.json` has 70 entries: 35 cite a closed unmerged PR, and 25 explicitly state that review was by title/scope and **not line by line**. Those records are largely CellScaffold decisions authored by Claude. Statements that a human already decided are not themselves primary evidence of that person's rationale. They do not settle whether a unique delta must be salvaged under the current user request.

The 39 non-CellScaffold refs classified `DIVERGENT_HISTORY_REQUIRES_REVIEW` in the complete inventory have **zero branch-name matches** in that decision file. No-common-ancestor is not patch equivalence and not evidence of replacement. Full refs and the empty decision matches are preserved in `supplement-evidence.json`. The bounded review does not assert that all 39 histories have now been adjudicated line by line.

Examples of meaningful distinctions in the written record:

- Archive/salvage rejection says preservation snapshots should not be wholesale merged, while explicitly allowing extraction of missing content. This rejects a merge strategy, not all functionality.
- Broad old-branch entries cite age, file counts, no PR, or a newer main in the same area. Without path/behavior comparison those remain hypotheses, not terminal content rejection.
- `codex/vegar-arendalsuka-runtime` has a later entry by Kjetil calling for bounded extraction against fresh main, with new verification instead of merging an old branch wholesale. That is consistent with the recovery approach.
- `CellScaffold/Documentation/Operations/Lokalt_Endringsinventar_2026-08-09.md` gives concrete replacement cases: older Kallimachos App placement moved into shared ScaffoldKit with later scope/retention hardening; an emergency Dockerfile change weakened the Book-copy guard and removed Mermaid/Chromium; the preserved-root-WIP bulk branch had heavy conflict but still required named missing pieces to be extracted. Verify the exact current replacement before closing any remaining content gap.
- `Git_Cleanup_Commit_Handoff_2026-08-10.md` documents thematic preservation commits and an unpushed/un-PR'd handoff, not permission to discard old work. Lockfile drift without an intended dependency release is separate from source functionality.

The explicit Mint provider boundary and current presentation implementation above are source-backed replacements. An old branch name, closed PR, archive label, stale age, or missing merge base alone is not.
