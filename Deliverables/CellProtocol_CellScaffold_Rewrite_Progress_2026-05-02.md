# CellProtocol / CellScaffold Rewrite Progress - 2026-05-02

This note captures the current implementation state so a later Codex thread can resume without relying on chat history.

## Repositories

- CellProtocol: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol`
- CellScaffold: `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold`
- Notes repo: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments`

## Completed In This Batch

- CellProtocol persistence cleanup: `TypedCellsUtility` and `CellJSONCoder` now use diagnostic logging instead of unconditional prints, with tests around missing persisted-cell diagnostics.
- CellProtocol agreement/access cleanup: `Agreement` and `Grant` legacy decode no longer use `try!`; legacy state fallback is explicit, unknown legacy state decodes to signed with diagnostics, and empty condition mutation is covered by tests.
- CellProtocol resolver cleanup: `CellResolver` noisy prints were moved to diagnostics, optional debug interpolation was fixed, and delete results are handled explicitly.
- CellProtocol resolver auditor cleanup: duplicate personal-instance registration now throws `AuditorError.personalInstanceAlreadyRegistered` instead of `fatalError`, covered by a regression test.
- CellProtocol Vapor bridge transport cleanup: `VaporBridgeTransport` now uses a shared event loop group instead of creating unmanaged event loop groups per setup, and noisy transport prints were moved to bridge diagnostics.
- CellProtocol transport/sendability cleanup: `VaporBridgeTransport` now has locked delegate/socket/cleanup state, idempotent close cleanup, no-websocket send cleanup, and a sendable identity snapshot path for visiting identities. `LightweightBridgeTransport` now uses sendable protocol surfaces, locked weak delegate storage, sendable reconnect context/plan, and no longer carries an unused mutable `Identity` through reconnect state.
- CellProtocol Vapor transport regressions: added `VaporBridgeTransportTests` for idempotent delegate unregister on close, text-mode no-websocket cleanup, and identity snapshot round-tripping.
- CellProtocol build cleanup encountered during transport warning pass: `IdentityLinkCompletion.swift` now propagates the throwing identity descriptor call instead of failing compilation when the file participates in SwiftPM builds.
- CellScaffold bridgehead cleanup: corrected public implementation name to `VaporBridgehead`, kept legacy `VaporBrigehead` typealias, preserved `/bridgehead/:pubId/:bridgeId`, replaced force-unwrapped parameters with Vapor parameter validation, and moved setup prints to request logging.
- CellScaffold test isolation: `PersonalCopilotV1Tests` now saves/restores `CellBase.defaultCellResolver` so direct chat-hub tests do not leak resolver state from other suites.
- Skeleton tooling cleanup: `scripts/skeleton-iterate.js` now accepts common kebab-case CLI aliases such as `--base-url` in addition to existing camelCase flags like `--baseURL`, preventing accidental fallback to the staging host.

## Important Prior Work Already Present

- `ValueTypeCodec` and related deterministic value encoding/decoding work is present.
- `BridgeCommand` has safe decode and payload key handling while preserving existing wire keys.
- `BridgeBase` has cid-correlated routing for admit/agreement/sign responses and keeps the legacy config initializer source-compatible.
- Bridge, serialization, skeleton, persistence, resolver, and agreement tests have been expanded.

## Verification Completed

- CellProtocol full suite, unsandboxed: `swift test` passed 381 tests, 0 failures after the transport/sendability batch.
- CellScaffold full suite with local CellProtocol: `CELLPROTOCOL_LOCAL_PACKAGE_PATH=/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol swift test` passed 579 tests, 3 skipped, 0 failures.
- Targeted CellProtocol checks passed: `PersistenceTests`, `ResolverTests`, `AgreementCodingTests`, `BridgeTests`, `LightweightBridgeTransportTests`, `VaporBridgeTransportTests`.
- CellProtocol warning-oriented target build passed: `swift build --target CellVapor -Xswiftc -warn-concurrency`. Remaining warnings are mainly broader global/runtime isolation work such as `CellBase.defaultCellResolver`, `CellBase.sendDataAsText`, identity vault globals, and unrelated domain-cell isolation warnings.
- Targeted CellScaffold checks passed: `PersonalCopilotV1Tests`, `ConferenceSurfaceRoutesTests`.
- JavaScript syntax check passed: `node --check scripts/skeleton-iterate.js`.
- Skeleton scenarios passed against local `http://127.0.0.1:9099`:
  - `conference-participant-portal.preview.json`: `test-results/skeleton-iterate/conference-participant-portal.preview-2026-05-02T08-20-33-739Z`
  - `conference-participant-chat.preview.json`: `test-results/skeleton-iterate/conference-participant-chat.preview-2026-05-02T09-04-49-109Z`
  - `personal-invite-chat.preview.json`: `test-results/skeleton-iterate/personal-invite-chat.preview-2026-05-02T09-06-47-078Z`
- Alias regression check passed: portal scenario also passed with `--base-url`, artifact `test-results/skeleton-iterate/conference-participant-portal.preview-2026-05-02T09-16-13-793Z`.

## Notes And Caveats

- Sandboxed `swift test` can fail because SwiftPM, build.db, Documents, and keychain access are blocked. The authoritative full suite results above were run unsandboxed.
- `Scripts/run_skeleton_parity_suite.sh` was not run in CellScaffold because that script is not present there. It appears to belong to a different repo/workflow; ask Kjetil before running a Binding-level parity suite.
- Swift 6 sendability warnings remain, but the earlier focused Lightweight transport warnings are cleared. The remaining warnings are mostly global runtime state and broader identity/domain isolation work, so they should be handled as the `CellRuntimeEnvironment`/global-state cleanup rather than by suppressing warnings locally.
- Test logs still contain expected/noisy diagnostics such as initial missing files, denied demo references, and identity-vault serialization warnings. These are not test failures, but they are useful future cleanup if we want lower-noise CI.
- Both repos have many dirty files and untracked additions that predate or sit outside this specific batch. Do not revert broad worktree changes without explicit approval.
- During the final full test, `EntityAnchorCell` briefly reported missing `identityLinks` helpers while another SwiftPM process/build snapshot was active. A subsequent targeted `swift build --target CellVapor` and full `swift test` both passed, so this was treated as a stale/concurrent build snapshot rather than a current source error.

## Recommended Next Steps

1. Continue the "thin adapter" work for platform transports by reviewing `AppleBridgeTransport` against the now-cleaner Lightweight/Vapor semantics: ready handshake, text/binary send behavior, close cleanup, delegate routing, and visiting identity vault behavior.
2. Start the `CellRuntimeEnvironment`/global-state cleanup behind existing `CellBase.*` source-compatible statics; this should reduce the remaining `CellBase.defaultCellResolver`, vault, storage, websocket-policy, and logging warnings without changing public API.
3. Reduce noisy runtime prints/logs in Porthole bootstrap and scaffold setup where they are not contractually useful.
4. Run CellScaffold full suite again after the next integration-affecting CellProtocol batch.
5. Ask before running external parity suites outside CellScaffold, especially the Binding-level `Scripts/run_skeleton_parity_suite.sh`.
