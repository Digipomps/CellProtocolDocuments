# Existing Admin bridge acceptance contract

2026-09-18. Read-only source audit of `/private/tmp/haven-prod-20260917/CellScaffold` and sibling CellProtocol, following `repo-audit/ADMIN-RUNTIME-COMPATIBILITY-20260918.md`. No SSH, network, browser, credentials/production state inspection, build, test or source/runtime/Git mutation. Report only.

## Result

There is an existing normal web/requester path that can prove a successful authorized remote AdminOverview read, **provided the existing requester already has the required authority**. There is no discovered packaged web/admin CLI that independently yields a production bridge-identity pass/fail without configuring new isolated identities. The M4 runner delegates to environment-owned executables; it does not implement those probes itself.

The current candidate also has a concrete pre-bridge regression in the normal `/admin` entry link. Correct it before certifying the GUI. Do not mistake this HTTP 400 for a failed HMAC/identity challenge.

## Newly found entry-link regression

`Sources/App/Controllers/VaporAdminMVP.swift:9` redirects `/admin` to `/porthole` with:

```text
configurationName=Admin Control Plane Overview
configurationEndpoint=cell://<configured-admin-authority>/AdminOverview
```

`PortholeWebSessionSupport.swift:4319` treats any lookup with a remote `sourceCellEndpoint` as an explicit external configuration fetch **before** the built-in catalog lookup. It requires a keypath, explicit port, and generic `HAVEN_BRIDGEHEAD_HOSTS`/token admission. The normal Admin link has no keypath and usually no explicit port; its legitimate transport uses the separate installed Admin HMAC credential. Consequently the source path reaches `Remote configuration lookup requires an explicit keypath` before opening an admin WebSocket. The JS menu also emits name/source lookups, so the distinction matters outside `/admin`.

Minimum correction: recognize an exact identity of a currently published **built-in AdminWorkspace** entry using current `AdminControlPlaneRouting`, and select that local configuration before the external-fetch branch. This selects an existing local factory; its remote references must still use the normal resolver/HMAC/requester boundary. Do not exempt arbitrary remote endpoints, names, UUIDs, keypaths, or user-supplied complete configurations. Preserve all generic external lookup admission checks and their negative tests.

Before that correction, a name-only lookup uses the existing catalog path and can diagnose the actual bridge. It is a diagnostic workaround, not evidence the ordinary `/admin` link works.

## Minimum existing request contract

Use an already authenticated normal web session belonging to the existing intended requester. Do not register a canary user, copy the admin owner into the request, add an MVP web role, issue an AdminEntry/AdminRole credential, or enable a surface gate. Opening a Porthole surface persists the active workspace through its ordinary action; save/restore the user's current surface through normal navigation if needed.

1. Establish/reuse that session at `GET /browserhead/webo`.
2. Send `POST /browserhead/porthole/action` with:

```json
{"keypath":"addConfiguration","payload":{"configurationLookup":{"name":"Admin Control Plane Overview"}}}
```

3. Read `GET /browserhead/porthole/bootstrap` without `phase=shell`.
4. After the entry-link correction, repeat via `/admin` or the real Admin menu, then obtain the same full bootstrap. This is the actual GUI acceptance route.

Example command shape, **not run here**; variable values must come from the existing session/runtime, not invented credentials:

```bash
curl --fail-with-body --silent --show-error --max-time 30 \
  --cookie "$EXISTING_WEB_COOKIE_JAR" --cookie-jar "$EXISTING_WEB_COOKIE_JAR" \
  --output "$PRIVATE_EVIDENCE_DIR/porthole-open.html" \
  "$WEB_ORIGIN/browserhead/webo"

curl --fail-with-body --silent --show-error --max-time 30 \
  --cookie "$EXISTING_WEB_COOKIE_JAR" --cookie-jar "$EXISTING_WEB_COOKIE_JAR" \
  --header 'Content-Type: application/json' \
  --data '{"keypath":"addConfiguration","payload":{"configurationLookup":{"name":"Admin Control Plane Overview"}}}' \
  --output "$PRIVATE_EVIDENCE_DIR/admin-load.json" \
  "$WEB_ORIGIN/browserhead/porthole/action"

curl --fail-with-body --silent --show-error --max-time 30 \
  --cookie "$EXISTING_WEB_COOKIE_JAR" --cookie-jar "$EXISTING_WEB_COOKIE_JAR" \
  --output "$PRIVATE_EVIDENCE_DIR/admin-bootstrap.json" \
  "$WEB_ORIGIN/browserhead/porthole/bootstrap"
```

These commands only check HTTP success. A validator must additionally require the real projected `state.adminOverview.state` object (handling the normal Porthole envelope), its `metricsSchemaVersion == "admin.metrics.v1"`, an actual numeric timestamp, and expected remote runtime revision/instance/environment. Require the returned `adminOverview` reference endpoint to match the installed remote routing and rule out local fallback. Compare `runtime.imageDigest` when installed; an `unconfigured` field is missing evidence, not a successful match. Avoid printing the full bootstrap, requester identity, credential, cookie or metrics payload; write a reduced receipt containing only acceptance results, revision/target and evidence hashes.

AdminOverview's web factory currently references only `AdminOverview` (`AdminWorkspaceConfigurationFactory.swift:54`). Do not claim this one request also read AdminNodeFleet. A separate normally authorized node-fleet surface/read is required for that claim.

## What each result proves

| Observed result | Defensible claim | Not established |
| --- | --- | --- |
| `/health/build`, liveness/readiness, TLS certificate | Deployed revision and HTTP service/transport health | Web HMAC handshake, CP identity proof, admin capability |
| Accepted WSS upgrade/`ready` and description using installed HMAC credential | Current transport path and channel authentication succeeded | End-user signing possession or AdminOverview read authority |
| Full bootstrap contains expected remote AdminOverview state | An ordinary web requester successfully read the remote surface through installed routing | A separately observed signing challenge, if a cell-specific/surface-gate authorization path could satisfy the read |
| Bound CP origin challenge succeeded during a correlated normal operation | Server ready, callback/signature path and possession of existing requester key worked for that exact scope | Permission for unrelated AdminOverview/state or another cell |
| AdminOverview denied/unavailable with transport response | A negative capability/error result, useful for diagnosis | Positive identity proof or working authorized admin GUI |

The HMAC credential authenticates the web transport. `/admin/api/session` reports `MVPAdminAccess` environment-scoped web roles only (`VaporAdminMVP.swift:203`, `MVPAdminAccess.swift:57`). Neither is an AdminRole credential or a grant. Do not use role-name equality between these systems as authorization evidence.

The new CP provenance path (`BridgeBase.swift:1220`) makes incoming requesters public snapshots with `BridgeIdentityVault`, not the admin process's local vault. Successful origin proof requires server ready (`:995`), a fresh `IdentitySigningChallenge`, and the client's active local operation lease restricted to the discovered/pinned domain/resource (`BridgeIdentityProofAuthorization.swift:51`, `:75`). Unsolicited `sign` calls cannot replace a normal proof-bearing operation; the permit deliberately rejects them.

GeneralCell owner and valid signed-contract paths perform the key proof (`GeneralCell.swift:1978`, `:2143`, `:2196`). AdminOverview also has cell-specific paths: its configured surface gate and verified observer credential (`AdminOverviewCell.swift:65`). Therefore a receipt that explicitly claims the signature callback was exercised needs correlated operation/auth-path evidence; merely seeing “Consume command sign” without its successful bound result is insufficient. Do not turn on a permissive gate just to make the read pass.

## Existing entry-credential verification path

`AdminMetricsSupport.hasVerifiedEntryProof` (`:1352`) resolves the configured remote AdminEntry as the requester, reads the requester's existing entry credential, then sends `set("verifyEntryCredential", {credential}, requester)`. The AdminEntry implementation validates issuer, signature, subject, expiry and revocation and uses `persist:false` (`AdminEntryCell.swift:127`, `:305`). This is the existing side-effect-free credential verification method; it does not mint or store new authority.

The existing `Scaffold Setup & Identity Link` Porthole surface invokes it when projecting `scaffoldSetup.state` (`ScaffoldSetupCell.swift:367`). `state.scaffoldSetup.state.bootstrap.requiresEntryProof == false` is a positive verification result; its entryStatus states the same result. That configuration also includes the remote AdminEntry reference (`ConfigurationCatalogCell.swift:5504`), so opening it still needs the ordinary resolution/access path.

However, the helper collapses missing credential, failed remote resolution, failed set and denied response into `false`. A `requiresEntryProof:true` result alone cannot distinguish unavailable bridge from absent/expired authority. There is no inspected JSON CLI exposing its internal failure stage. Do not repair that uncertainty by issuing a new credential.

Full admin bootstrap calls `AdminEntityProofPersistenceSupport.restoreAcceptedCredentials` (`PortholeWebSessionSupport.swift:743`). This re-presents **already existing** credentials through normal `requestEntry`/`requestRole`, possibly restoring their local presentation state; it is not a raw read-only storage operation. It does not mint new credentials. If absolutely no presentation-state mutation is allowed, the normal admin bootstrap is not that stricter probe; use the explicitly non-persisting verification method from an existing in-process requester-aware diagnostic, which is not packaged as a CLI today.

## M4 adapter and test limits

`scripts/run-admin-m4-gate.sh:89` executes `ADMIN_M4_HANDSHAKE_RUNNER` / `ADMIN_M4_USER_FLOW_RUNNER` supplied by the environment. Its validator only checks schema, pass status, exact commit and the two image strings (`:100`). It checks no observation, nonce, challenge response, request correlation or actual state. A fabricated static receipt can satisfy that validator; the environment runner must own the real assertions. The runbook explicitly says these secret-bearing environment adapters are not committed (`Documentation/AdminScaffold_M4_Runbook.md:211`). None was found in the candidate source.

Do not run the entire `staging` M4 gate as a “read-only bridge probe”: it includes certbot renewal dry-run, nginx reload, lifecycle/rotation/load/failure runners and a restore drill. A dedicated existing verified runner may be invoked alone if one is actually installed; no such installed host artifact was inspected here.

`AdminEntryRemoteBridgeLoopbackTests` is a valuable local/CI regression for server ready and remote entry verification. It launches an isolated AdminScaffold, creates an owner and a new credential, enables loopback plaintext and relaxes readiness requirements. It is not a command for probing the existing production requester. `playwright/admin-web.spec.js` mocks its HTTP results; it is not live bridge acceptance.

## Real blockers / next decision

- Correct the built-in Admin deep-link versus external-config-lookup regression and test the actual `/admin` entry.
- Root must determine, without exposing contents, whether the existing intended requester already has valid admin authority. If not, positive AdminOverview acceptance is unavailable under this slice's no-new-authority constraint. Transport success can still be reported separately.
- A fresh admin rollout closes server sockets, so the next normal web read should need a new handshake; prove the correlated new read rather than relying on old positive cache/session evidence.
- No existing separately callable production probe was discovered that returns a cryptographically grounded signing-pass receipt. Do not claim that the generic M4 JSON receipt fills this gap. The planned bounded controller/adapter must consume actual normal-requester observations or report the relevant stage as unverified/blocked.

All live acceptance remains for root. No pass result is claimed by this report.

## Follow-up: description, denied GET and existing Python client

### A description response is not a signing-round proof

The admin inbound bridge uses the installed local owner only for publisher resolution (`Sources/ScaffoldKit/AdminScaffoldBridgeRoutes.swift:389`, `BridgeBase.swift:862` / `:890`). `BridgeBase.processDescriptionCommand` (`:1529`) then calls the resolved publisher's `advertise(for:)`. `GeneralCell.advertise` (`Sources/CellBase/Cells/GeneralCell/GeneralCell.swift:1555`) builds an Explore manifest and a public agreement-template snapshot. Its schema/key/type helpers (`:220`, `:227`, `:249`, `:258`) do not call `validateAccess` or `checkIdentityOrigin`. AdminOverview does not override this path.

Therefore a correct public description can be returned by the old admin build whose server-side bridge never consumes `ready`. It proves the authenticated transport/publisher path, not that admin can call back to the web requester for a signature. The outbound web resolver's local `proveRemoteBridgePrincipal` (`CellResolver.swift:2404`) is also a distinct local proof, not evidence of that remote callback.

### An unknown ephemeral identity does not guarantee proof before denial

For a fresh identity with no owner match, linked identity, or existing valid contract, `GeneralCell.authorizationEvidence` (`:1978`) sets owner proof false without signing and finds no eligible contract. `authorizationContracts` (`:2114`) checks origin only after finding and validating an existing subject-bound contract and its conditions (`:2143`). A protected GET may therefore return no-grant denial without ever requesting a signature. Good and bad signing implementations can receive the same denial. Do not treat their identical responses, or denial alone, as verified identity possession.

Cell-specific AdminOverview credential lookup could cause additional nested accesses, but it is not a documented unconditional challenge probe and must not be used as a claim that every foreign requester signs first. The generic `admit` path also does not force an origin check for an unknown identity (`determineIdentityState`, `:2162`). The public Swift `verifyRequesterIdentityControl` helper (`:2192`) does force the existing origin check, but no inspected HTTP/Meddle/bridge endpoint exposes it as a production diagnostic. It is an in-process API, not a runnable existing remote probe.

### The existing Python bridge cannot serve the needed callback

Inspected repository: `/Users/kjetil/Build/Digipomps/HAVEN/PyCellProtocol`.

- `src/cellprotocol/bridge.py:297`: `WebSocketBridgeClient` accepts a URL, identity, optional custom `connect`, and timeout. No packaged admin-HMAC credential adapter or acceptance CLI was found. A custom connector would be new integration code, not an existing installed proof.
- `:437`: the receive loop recognizes `ready`, then routes by CID to streams/pending requests or `unhandled_commands`. It does not dispatch an incoming `sign` command to the local vault. It also does not first require a response command before satisfying a matching pending CID, so callback CID reuse cannot be assumed safe.
- `:194`: `BridgeEndpoint.handle` explicitly rejects `sign` with `Remote signing is unavailable until a validated purpose/audience/nonce/expiry challenge is implemented`.
- `:525`, `:580`: `CloudBridgePublisherSession` serves the unhandled queue through that same rejecting endpoint, so publishing a Python cell does not supply the missing callback support.
- `:289`: the available `sign` method sends an outbound command to the peer; it is not an implementation of the peer's incoming signing callback.

Consequently there is no existing Python command that can be honestly recommended to prove this admin fix with an ephemeral identity and good/bad challenge signatures. Do not transport the installed HMAC secret off-host, import production private keys into Python, issue a grant, or implement a permissive raw-sign handler to work around this gap. A reviewed challenge-aware adapter or a correlated normal Swift requester operation with actual origin-proof evidence remains necessary for the stronger signing claim. Existing normal authorized AdminOverview acceptance can still be performed and reported at its actual evidence level; the absence of standalone callback evidence must remain explicit.
