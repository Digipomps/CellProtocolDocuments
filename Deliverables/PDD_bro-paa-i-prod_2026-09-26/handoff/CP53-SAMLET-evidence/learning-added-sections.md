## Async publisher subscription races

Include the peer, Scanner, EntityScanner, record and mux suites in TSAN checks;
BridgeDescriptionConcurrencyTests alone does not exercise all their shared
helpers. CP53's expanded mux run exposed a race in CombineHelpers
`Publisher+Async.swift`: sink can deliver on another thread before returning its
AnyCancellable. Protecting only continuation resumption left the captured
subscription variable unsynchronized and could miss cancellation on late install.

Keep result completion, timeout ownership and subscription installation under
one lock. A subscription installed after completion must be cancelled. Move
cancel/resume outside the lock because cancellation may synchronously reenter.
Exercise synchronous first delivery, concurrent delivery during installation,
empty/failing publishers and timeout cancellation with both Combine and
OpenCombine. `PublisherAsyncLifetimeTests` and the actual mux test
`testParallelResolverLookupsShareSuspendedAuthenticatedHandshakeAndPrincipal`
cover these paths. Do not suppress the race or exclude the triggering suite.

## Scanner platform and native-load boundaries

An actor does not protect a mutable reference after returning it to callers.
Expanded CP53 CI TSAN caught `EphemeralIdentityVault.identity(forUUID:)` rewriting
`homeVaultReference` while `CellResolver.proveRemoteBridgePrincipal` read the same
published Identity. Bind metadata on explicit creation/insertion, and keep lookup
read-only. Test concurrent context/UUID lookups alongside external metadata reads,
preserve local signing and reject the same UUID with another public key. The
regression is `EphemeralIdentityVaultConcurrencyTests`; a green uninstrumented
run cannot establish absence of this race. This does not make arbitrary later
external Identity mutation safe.

Compile the iOS branch explicitly after Scanner/NI changes. macOS tests cannot
type-check code hidden behind `#if os(iOS)`: CP53's iOS 18 build found a stale
EntityScanner generic-feed call to the removed, unbound NI-token method after
the macOS suite had passed. Removing that entry point preserves the authenticated
ScannerConsumerContext path. Report target/SDK, simulator tests and physical
token/UWB tests separately; a successful cross-compile proves only compilation.

Before a native MC receiver deliberately stops acknowledging application data,
wait for both endpoints to finish full Scanner setup and drain their outstanding
data records. Use explicit cross-process readiness/drain markers. A setup record
left in the 32-record window can make the 32nd load send correctly wait until the
ten-second receipt deadline. Do not increase or disable the production timeout
to repair that fixture race. `ScannerPhysicalIsolationTests` exercises this
sequence, per-peer disconnect and continued healthy-sibling traffic.

When a malformed-wire test checks terminal cleanup, assert closed state and
released/retained quotas before the fixture's own stop/close; explicit cleanup
can otherwise hide the leak being tested.

