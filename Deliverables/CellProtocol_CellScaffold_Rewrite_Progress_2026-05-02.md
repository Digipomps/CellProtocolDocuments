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
- CellProtocol Apple transport cleanup: `AppleBridgeTransport` now has locked delegate/socket/cleanup state, idempotent unregister cleanup for disconnect/error/no-socket send, safe command routing via `BridgeCommand.command`, diagnostic logging instead of transport prints, binary/text send tests, and BridgeIdentityVault fallback for visiting identities when the delegate is a bridge.
- CellProtocol Apple websocket adapter cleanup: internal `WebSocketTaskConnection` wrappers are final, explicitly `@unchecked Sendable`, use locked weak delegate storage, and import Combine/OpenCombine with `@preconcurrency`, removing the focused WebSocketConnection sendability warnings without changing public wire behavior.
- CellProtocol Apple transport regressions: added `AppleBridgeTransportTests` for binary/text sends, no-socket cleanup, send-failure cleanup, disconnect/error cleanup, unknown command routing, and identity-vault fallback behavior.
- CellProtocol build cleanup encountered during transport warning pass: `IdentityLinkCompletion.swift` now propagates the throwing identity descriptor call instead of failing compilation when the file participates in SwiftPM builds.
- CellProtocol runtime/global-state cleanup: introduced internal `CellRuntimeEnvironment` behind source-compatible `CellBase.*` statics for resolver, vault, storage path, websocket policy, diagnostics, remote websocket query provider, and related global runtime settings.
- CellProtocol runtime locking cleanup: `CellRuntimeEnvironment` releases replaced resolver/vault/provider/path/handler state outside the runtime lock, preventing the resolver replacement/deinit diagnostic deadlock that was found during full-suite testing.
- CellProtocol runtime regressions: added `CellRuntimeEnvironmentTests` for legacy static proxy behavior, diagnostic domain filtering, remote websocket query provider compatibility, stable persisted-cell master key derivation, and the resolver replacement deadlock path.
- CellProtocol identity/vault sendability cleanup: `IdentityVaultProtocol`, `ScopedSecretProviderProtocol`, and `IdentityKeyRoleProviderProtocol` now explicitly conform to `Sendable`; `Identity` remains source-compatible as a mutable reference type and is annotated `@unchecked Sendable` for existing cross-actor API use.
- CellProtocol bridge/vault adapter cleanup: `BridgeIdentityVault` is now explicitly `@unchecked Sendable` as a stateless adapter over an existing bridge reference, preserving bridge signing behavior and remote visiting-identity fallback.
- CellProtocol platform vault cleanup: Apple and Vapor `VaultIdentity.valueForKey` no longer dispatch through `DispatchQueue.global()` just to read local properties; they now return deterministic Combine publishers while preserving legacy silent behavior for missing/unauthorized values.
- CellScaffold bridgehead cleanup: corrected public implementation name to `VaporBridgehead`, kept legacy `VaporBrigehead` typealias, preserved `/bridgehead/:pubId/:bridgeId`, replaced force-unwrapped parameters with Vapor parameter validation, and moved setup prints to request logging.
- CellScaffold test isolation: `PersonalCopilotV1Tests` now saves/restores `CellBase.defaultCellResolver` so direct chat-hub tests do not leak resolver state from other suites.
- CellScaffold `FileUpload` integration cleanup: Porthole bootstrap projection and editor tree kind mapping now handle `SkeletonElement.FileUpload` explicitly when built against the local CellProtocol skeleton spec.
- Skeleton tooling cleanup: `scripts/skeleton-iterate.js` now accepts common kebab-case CLI aliases such as `--base-url` in addition to existing camelCase flags like `--baseURL`, preventing accidental fallback to the staging host.

## Important Prior Work Already Present

- `ValueTypeCodec` and related deterministic value encoding/decoding work is present.
- `BridgeCommand` has safe decode and payload key handling while preserving existing wire keys.
- `BridgeBase` has cid-correlated routing for admit/agreement/sign responses and keeps the legacy config initializer source-compatible.
- Bridge, serialization, skeleton, persistence, resolver, and agreement tests have been expanded.

## Verification Completed

- CellProtocol full suite, unsandboxed: `swift test` passed 400 tests, 0 failures after the `CellRuntimeEnvironment` and identity/vault sendability batch.
- CellScaffold full suite with local CellProtocol: `CELLPROTOCOL_LOCAL_PACKAGE_PATH=/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol swift test` passed 579 tests, 3 skipped, 0 failures after the identity/vault sendability batch and `FileUpload` integration fix.
- Targeted CellProtocol checks passed: `PersistenceTests`, `ResolverTests`, `AgreementCodingTests`, `BridgeTests`, `AppleBridgeTransportTests`, `LightweightBridgeTransportTests`, `VaporBridgeTransportTests`, `CellRuntimeEnvironmentTests`, `DiagnosticLoggingTests`, `AppleIdentityVaultKeyStorageTests`, and bridge/vault signing fallback checks.
- CellProtocol warning-oriented target builds passed: `swift build --target CellVapor -Xswiftc -warn-concurrency`, `swift build --target CellApple -Xswiftc -warn-concurrency`, and `swift build --target CellBase -Xswiftc -warn-concurrency`. The focused `CellBase.swift` static mutable global warnings, `DIDIdentityVault` actor-boundary warnings, `IdentityVaultProtocol`/`Identity` sendability warnings, and Apple/Vapor `VaultIdentity.valueForKey` capture warnings are cleared. Remaining warnings are broader resolver/domain/runtime-isolation work such as `AnyCell.publishers`, `CellResolver.sharedInstance`, non-Sendable `Emit` task cache/value payloads, `ValueType`, formatter statics, Apple vault singleton/source-compat warnings, Porthole skeleton task captures, and unrelated domain-cell isolation warnings.
- Targeted CellScaffold checks passed: `PersonalCopilotV1Tests`, `ConferenceSurfaceRoutesTests`.
- Targeted Porthole checks passed: `PortholeBootstrapProjectionTests` and `PortholeWebEditorSupportTests`.
- JavaScript syntax check passed: `node --check scripts/skeleton-iterate.js`.
- Skeleton scenarios passed against local `http://127.0.0.1:9099`:
  - `conference-participant-portal.preview.json`: `test-results/skeleton-iterate/conference-participant-portal.preview-2026-05-02T08-20-33-739Z`
  - `conference-participant-chat.preview.json`: `test-results/skeleton-iterate/conference-participant-chat.preview-2026-05-02T09-04-49-109Z`
  - `personal-invite-chat.preview.json`: `test-results/skeleton-iterate/personal-invite-chat.preview-2026-05-02T09-06-47-078Z`
- Alias regression check passed: portal scenario also passed with `--base-url`, artifact `test-results/skeleton-iterate/conference-participant-portal.preview-2026-05-02T09-16-13-793Z`.

## Notes And Caveats

- Sandboxed `swift test` can fail because SwiftPM, build.db, Documents, and keychain access are blocked. The authoritative full suite results above were run unsandboxed.
- `Scripts/run_skeleton_parity_suite.sh` was not run in CellScaffold because that script is not present there. It appears to belong to a different repo/workflow; ask Kjetil before running a Binding-level parity suite.
- Swift 6 sendability warnings remain, but the earlier focused Lightweight/Vapor/Apple transport/WebSocketConnection warnings, the `CellBase.swift` static global warnings, and the core identity/vault protocol warnings are cleared. The remaining warnings are mostly shared resolver, formatter singleton, task-cache, value-payload, Apple singleton/source-compat, domain-cell, and Porthole isolation work; handle them through explicit ownership boundaries rather than local suppressions.
- Test logs still contain expected/noisy diagnostics such as initial missing files, denied demo references, and identity-vault serialization warnings. These are not test failures, but they are useful future cleanup if we want lower-noise CI.
- Both repos have many dirty files and untracked additions that predate or sit outside this specific batch. Do not revert broad worktree changes without explicit approval.
- During the final full test, `EntityAnchorCell` briefly reported missing `identityLinks` helpers while another SwiftPM process/build snapshot was active. A subsequent targeted `swift build --target CellVapor` and full `swift test` both passed, so this was treated as a stale/concurrent build snapshot rather than a current source error.

## Recommended Next Steps

1. Continue identity/vault cleanup around the remaining Apple-specific vault warnings (`IdentityVault.shared` mutability/source compatibility, `Facilitator` sendability, keychain singleton isolation, and old value-cancellable/noisy-print paths); keep legacy vault decode/migration behavior intact.
2. Reduce noisy runtime prints/logs in Porthole bootstrap and scaffold setup where they are not contractually useful.
3. Continue reducing remaining Swift 6 warnings in ownership-sized slices: `CellResolver.sharedInstance`, `AnyCell.publishers`, `Emit` task cache, `ValueType` sendability, formatter singletons, and Porthole skeleton task captures.
4. Run skeleton runtime scenarios (`npm run skeleton:iterate`) after the next Porthole/skeleton behavior change, especially if `FileUpload` surfaces are promoted into visible catalog configurations after the CellProtocol dependency is updated.
5. Ask before running external parity suites outside CellScaffold, especially the Binding-level `Scripts/run_skeleton_parity_suite.sh`.
