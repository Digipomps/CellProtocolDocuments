> Fresh-ref update, 2026-09-18: see [FRESH-REF-UPDATE-20260918.md](FRESH-REF-UPDATE-20260918.md). CP/MP recovery packages are now on main; all configured remotes were fetched by root. The historical findings below retain their original snapshot context.

# Issuer candidate: bounded source review, 2026-09-17

Reviewed `/private/tmp/haven-prod-20260917/DiMyMicropayments-issuer`, HEAD `b92725ffd650757bb4835d16771da7b891122b01` (issuer cherry-pick) over origin/main `c3544c2f7b9be967a71dd9d8c87ae1a999f707a2`, including the unpublished public-subclass, strict malformed-quarantine and runtime epoch configuration fixes present during review. Root reports 51 passing tests; this audit ran **no build or test**. Read-only source/Git inspection, no network, source mutation or personal persisted records. Line references are to the inspected candidate and may move with subsequent fixes.

## Decision

Include issuer segregation after wiring its production consumer and closing receipt binding. Existing main functionality genuinely consumes this wallet: CellScaffold `AIGatewaySupport.swift:1375–1473` calls `DiMyWallet/spend` and `DiMyAccess/verifyAndRedeem`; `PaymentGateCell.swift:2093–2160` does the same. These are not made obsolete by the separate Mint entitlement model. This review does not establish that real production paid traffic or issuer configuration is active.

## Required small corrections

### P1: Runtime Access leaves the issuer allowlist unset

`Sources/DiMyCellProtocolCells/DiMyAccessRuntimeCell.swift:354–361` constructs `AccessCell` without `acceptedMintKeyIDs`. In `Sources/DiMyAccessCell/AccessCell.swift:59–70,93–100`, nil accepts every otherwise verified issuer. Consequently the actual CS endpoint never enforces the merchant issuer restriction introduced by the branch; a globally trusted key for a different pot is enough to pass that check.

Smallest correction: resolve a deterministic, explicit accepted-issuer set in runtime construction, independent of the list of keys retained for historical verification. The existing selected `DIMY_MINT_KEY_ID` can be the compatibility default; an explicit multi-issuer list must be deliberate. Reject malformed/blank configured policy, with no fallback to an unrestricted nil. Preserve the development-key default only in the already defined development compatibility case. Do not infer merchant acceptance from every key in `DIMY_MINT_PUBLIC_KEYS_JSON`.

Test through the actual runtime cell's owner-authorized `set(verifyAndRedeem)`: configure keys A+B but accept A; a valid uniform B bundle is refused **before** mint invocation, while A succeeds. Cover explicit empty/malformed policy and runtime reconstruction. Direct actor tests alone do not catch the missing wiring.

### P1: A signed receipt is not bound to this issuer or merchant

`AccessCell.swift:134–140` validates only the returned bundle hash and cryptographic signature. `SpendReceiptSignatureVerifier` (`PaymentTypes.swift:677–698`) verifies the receipt's own declared issuer; it does not compare that issuer or merchant to the request. A mint client returning a valid B-signed receipt for A's hash, or an A-signed receipt for a different merchant, therefore causes an AccessGrant. This is a missing logical binding even when every signature is authentic. Receipt fields are signed (`PaymentTypes.swift:1065–1073`); there is no separate amount field to compare, because bundleHash binds the complete bundle.

Smallest correction: before accepting/caching a fresh receipt, require `receipt.mintKeyID == bundleIssuer` and `receipt.merchantID == merchantID`, in addition to the current hash and signature checks. Use specific errors. Maintain the current catch cleanup of pending replay reservations.

Tests: synthetic two-key registry and valid signed receipt mutations, not an always-true verifier. For each wrong issuer/wrong merchant/wrong hash, assert no grant, no cached receipt, and no accepted replay mutation; retry the same bundle with a correctly bound receipt through a controllable fake mint and verify success. Preserve the existing concurrent redemption tests. If strict current receipt epoch is adopted, apply it to **fresh redemption**, not historical audit receipt decoding.

### P2: Schema 3 can still silently lose an absent/null quarantine field

Root's removal of `try?` at `DiMyWalletRuntimeCell.swift:152` correctly makes malformed non-null quarantine fail decode. `decodeIfPresent ?? []` still treats a missing or explicit null `quarantinedCoins` as no value, including schema 3, where the encoder always writes it (`:193,196`). This differs from the existing strict required-value policy for storedCoins/cachedBundles and can discard quarantined records on a subsequent encode of a damaged object.

Smallest correction: require `[Coin]` with `decode` for schema 3; permit a missing field only for schemas 1/2. If a legacy object includes the field, reject malformed or null data rather than silently resetting it. Keep accepting old objects that genuinely predate the field.

Tests: actual encoded schema-3 wallet with real signed quarantined coin; missing/null/wrong-type quarantine each throws. A schema-2 object lacking quarantine still migrates. Full encode/decode/re-encode preserves the exact coin records and signatures. Existing `IssuerBoundWalletCellTests` partition-helper tests use directly constructed coins and do not exercise decoder signature checks, schema dispatch or persistence.

## Migration and pending-spend constraints

### P2: Pending legacy bundles are preserved but are not classified as blocked

`DiMyWalletRuntimeCell.swift:161–176` cryptographically validates stored/quarantined/pending coins, partitions only stored+quarantined coins, then restores cachedBundles unchanged. `:309–329` exposes only a pending count and quarantined **loose** coin count. A valid old foreign/mixed/retired pending bundle survives decode but rollback will fail in `WalletCell.swift:206–217,246–280`. It remains in cachedBundles because removal happens only after successful rollback (`DiMyWalletRuntimeCell.swift:431–434`). This is fail-closed with respect to available balance, but its state has no explanation that the reservation is blocked by migration policy.

Smallest safe handling: keep each bundle intact and reserved; compute/expose blocked pending count and non-sensitive reason codes (foreign issuer/mixed issuers/retired epoch). Do **not** split such a bundle into available coins or automatically release it into usable quarantine: the external mint might already have redeemed it. A genuine reconciliation/finalization feature is a separate operation requiring receipt evidence, not a decoder cleanup.

Meaningful migration test: construct a schema-2 object with separate available A/current, available B, retired A, and pending foreign/mixed/retired bundles with unique serials and genuine signatures. Decode under A binding and epoch policy; only A/current is spendable. Encode and reload; all original unavailable records are byte-for-byte representable, blocked pending stays reserved, rollback returns a specific error without changing any balance/cache, and depositing a pending serial remains refused. Also test valid current pending rollback succeeds exactly once across restart. Never widen rollback to make the test green.

### Historical public keys must remain available during cohort rotation

`validatePersistedWalletState` (`:543–549`) uses signature-only verification, correctly distinguishing an expired authentic coin from corruption. It still requires its public key in the runtime registry. Removing an old key, rather than keeping it with an epoch retirement threshold, makes even quarantined or pending records fail decode and blocks the whole wallet. That is an availability/migration requirement, not proof of deletion. In the inspected CP candidate, `FileSystemCellStorage.swift:24–38` propagates decode failures and `CellResolver.swift:1914–1922` only recreates genuinely missing/mismatched references, not corrupt wallet state.

Keep historical verification keys in the registry when applying epoch policy. Test unknown-key decode failure separately from known-key/retired-epoch quarantine, and assert a corrupt/unknown-key persisted wallet is not overwritten with empty state through the host persistence path. Do not disable signatures to force an old wallet to load. No production persisted data was inspected.

## Adjacent existing behavior to preserve/report

- `DiMyAccessRuntimeCell.swift:120–127` validates cached receipt hash+signature, while the actor constructor additionally filters merchant at `AccessCell.swift:75–79`. Runtime `receipt` returns its own cache directly (`:316–326`); changing merchant (`:330–336`) retains historical receipts/replay sets. Do not delete replay history or reject all historical receipts merely because issuer acceptance/epoch/merchant policy changes. If returning historical receipts is supported, describe them as historical and retain their signed merchant. New grants must satisfy current policy. Filtering active receipt lookups can be separate from preserving anti-replay history.
- `SpendReceiptSignatureVerifier` intentionally has no epoch check. Tightening it globally would make old access histories fail decode after retirement. A fresh-receipt current-cohort guard and historical signature-only validation are different operations.
- The in-memory development mint (`MintClient.swift:101–149`) verifies all registry-known coins but does not require their issuer to match its signingKeyID or recompute request.bundleHash. With a two-key registry it can produce the wrong-issuer receipt itself; this is a useful concrete negative fixture. Harden that development client too if it is claimed to model issuer separation, without treating it as production settlement authority.
- Neither CS paid consumer finalizes the wallet's cached bundle after successful redemption: AIGateway reads balance at `AIGatewaySupport.swift:1458–1473`; PaymentGate does the same at `PaymentGateCell.swift:2160`. Wallet only removes cachedBundles on rollback. Therefore pendingBundles includes successful spends, and later owner rollback can make an already spent signed coin appear in local balance; mint/access anti-replay should still prevent a second accepted grant. This predates the issuer patch. Do not claim pending count equals unresolved transactions, and do not add automatic migration release. A receipt-backed finalize/reconcile API plus consumer calls requires its own end-to-end test.
- CS production mint bootstrap (`MintClientBootstrap.swift:12–60`) selects an unavailable client unless a remote base URL is configured; embedded mint HTTP is development/testing only (`VaporDiMyMint.swift:81–84`). Preserve these guards. Passing issuer unit tests does not establish that a production issuer is provisioned.

## Minimum verification before root integration

Run the existing full MP suite against the intended CP pin plus (1) runtime A/B allowlist, (2) real-signature receipt issuer/merchant binding and clean retry, (3) schema-3 required quarantine, (4) schema-2 complete signed migration/pending roundtrip, and (5) no-reset-on-unverifiable-persisted-value regression. Re-run the existing CS AIGateway and PaymentGate paid-path tests using the revised MP pin; ensure refusal reaches consumers and leaves expected wallet state. The review itself did not run these tests and makes no production functionality claim.
