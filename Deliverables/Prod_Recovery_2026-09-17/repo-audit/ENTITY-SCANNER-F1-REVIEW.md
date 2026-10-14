# EntityScanner radar/select F1 regression review

Read-only review of `/private/tmp/haven-prod-20260917/CellProtocol`, 2026-09-17. No code changes or tests run by this audit slice. Line numbers describe the candidate before root's corrective edit.

**Recommendation: radar and select must remain private owner surfaces. Remove both from the remote agreement template. Do not broaden EntityScannerAgreementSurfaceTests' accepted grant set.** The failing sentinel is catching a real exposure, not a stale expected result.

## Evidence

- `Tests/CellBaseTests/EntityScannerAgreementSurfaceTests.swift:7–14,75` explicitly protects the F1 boundary: an admitted peer must not read another peer's data or the owner's private intent. Its expected readable keys are verificationMethods, capabilities, encounters plus the inherited feed/displayName.
- The original written F1 rationale is in `Binding/Documentation/Codex_FixList_NearbyScanner_2026-08-24.md:85–107`: whole maps across remote UUIDs must not be exposed through a generic agreement. A peer-specific surface would need filtering to the authenticated requesting peer.
- `Sources/CellApple/EntityRadar/EntityScannerCell.swift:124` newly puts select in the write-grant list; `:135` grants radar read. The radar getter `:171–189` checks only validateAccess(radar) before creating the whole ledger snapshot.
- `Sources/CellApple/EntityRadar/RadarModels.swift:494–543` returns all current entities, including UUID, display name, connection/status, measured direction/position, distance, age, match score, beacon-overlap count, kind, and selectedID. There is no requester filter. Hiding only selectedAdvertisement/accessChallenge in `EntityScannerCell.swift:176–185` does not protect the other peers or the owner's selection.
- Select already has an explicit isAdvertisementOwner check at `:239`. The Explore description at `:2245` expressly says owner-only selection. Granting it to peers contradicts the implementation and product description, even though that explicit check currently blocks a direct peer invocation.

## Smallest secure correction

1. Remove `select` from `actionKeys` at `EntityScannerCell.swift:124`; remove ensureGrant(radar) at `:135`.
2. In setupPermissions, explicitly remove persisted grants for both `radar` and `select` as well. Removing only new grant construction leaves a decoded older template's grants intact.
3. Gate the whole radar getter with the same `isAdvertisementOwner(requester)` plus `await validateAccess("r---", at: "radar", for: requester)` pattern used by the advertisement getter at `:193–194`. Keep both: UUID/public-key equality in the helper alone is not proof of private-key control. GeneralCell validateAccess obtains owner proof through `authorizationEvidence` / `checkIdentityOrigin` at `GeneralCell.swift:1978–1982`.
4. Keep select's owner check and validateAccess. Keep Explore registration so the owner can still discover and render the surface. Mark radar's Explore description at `:2232` explicitly owner-only.
5. Add radar/select to the sentinel's forbiddenKeys rather than expected readable/writable sets. Test a decoded cell too, including intentionally seeded old template grants.

## New selection flow is a second channel

`EntityScannerCell.swift:256–263` emits an event containing the owner's selected remoteUUID, displayName, status, and distanceMeters. The requesterOverride passed into `pushScannerEvent` is the identity authorized to emit, not a recipient restriction. `pushScannerEvent:1169–1181` calls `GeneralCell.pushFlowElement:2479–2484`, which sends to the shared feedPublisher. `GeneralCell.flow(requester:):1216–1225` grants feed subscription without per-event peer filtering. The F1-approved template includes feed.

Therefore the private selection can still leak after fixing radar-getter access. The bounded correction is to emit only a neutral refresh marker such as `{event:"selected"}` on that shared flow, leaving selectedID and details in the owner-only snapshot. The ledger was already selected at `EntityScannerCell.swift:253`; the detailed outgoing event is not needed to set it. Verify owner UI refresh via the marker. Alternatively use an established owner-restricted event path, but do not treat requesterOverride as one.

This review identifies a new selection leak; it does not certify all older scanner flow events. Existing found/proximity events also contain peer metadata. Redacting the new selection event is necessary but not sufficient to claim the entire scanner feed is peer-redacted.

## Required meaningful regressions

- Existing EntityScannerAgreementSurfaceTests passes with its approved set unchanged and radar/select explicitly forbidden.
- Fresh and decoded cells both omit radar/select even when decoded template data contains old grants.
- Real owner with valid signing authority can read radar and select a synthetic discovered peer; explicit ordinary peer grants cannot bypass the owner gate.
- Same owner UUID with a different signing key, and copied public descriptor without signing control, cannot read/select. Keep GeneralCell cryptographic authorization in the path.
- A peer with admitted feed subscription does not receive selected peer UUID, name, or distance from the new select action; owner can observe the neutral refresh marker and read selectedID through radar.
- Existing EntityScannerCellContractTests, RadarEntityLedgerTests, nearby advertisement/proof tests, and the relevant complete suite remain green. No hardware permission or radio activity is needed for the synthetic authorization tests.

The separate trust-fixture path issue is owned by root and is not an authorization justification for changing this F1 sentinel.
