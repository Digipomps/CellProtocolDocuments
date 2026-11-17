# Skeleton Runtime Iteration Workflow

This workflow lets an agent preview and test skeleton changes through Porthole without rebuilding or redeploying CellScaffold.

## Command

```bash
npm run skeleton:iterate -- --scenario playwright/skeleton-scenarios/conference-participant-chat.preview.json
```

Modes:

- `export`: reads the live active configuration and skeleton to files and writes nothing. It never enters edit mode and never discards working state, so it is safe against production. Takes no `skeletonFile`.
- `preview`: loads a configuration, enters edit mode, sets the working skeleton, tests it, and does not apply it.
- `commit-runtime`: runs the same preview loop, then calls `editor.apply` and verifies the committed runtime override in a new Porthole session.
- `review`: runs preview and writes a promotion bundle with candidate JSON, screenshots, DOM text, console data, page errors, and a diff.

## Scenario Contract

Required fields:

- `configurationName`
- `sourceCellEndpoint`
- `skeletonFile` (not used by `export` and `view-smoke`)

Common optional fields:

- `persona`
- `viewports`
- `expects.text`
- `expects.buttons`
- `expects.inputs`
- `actions`
- `notificationChecks`

## Target Server

`--base-url` (or `CONFERENCE_DEMO_BASE_URL`) selects the server. **The default is
staging, not localhost** (`scripts/skeleton-iterate.js`), so a command with no
`--base-url` acts on a live server. Pass `--base-url http://127.0.0.1:9089` when
you mean local.

## Access

`preview`, `export` and `review` only need a login. `commit-runtime` additionally
requires that the target configuration is source-backed and that the caller's
Identity holds an owner-authorized Agreement granting `rw-s` for
`applyEditableCellConfiguration` on the source cell. Without it the run stops in
`assertCommitRuntimeAccess` before anything is written. `export` reports this up
front as `canEdit` in `export-manifest.json`.

## Remote bridgehead token (Porthole / `cell://host:port/...`)

Set these variables on the **CellScaffold server process** before starting it:

```bash
export HAVEN_BRIDGEHEAD_HOSTS='127.0.0.1:18083,127.0.0.1:18084'
export HAVEN_BRIDGEHEAD_TOKEN="$PALAZZO_BRIDGEHEAD_TOKEN"
```

Both variables are required together. Hosts are a comma-separated allowlist of
exact `host:port` authorities (IPv6 uses `[::1]:18083`). CellScaffold registers
the existing dedicated `/bridgehead/<CellName>/<bridgeUUID>` route and sends
`Authorization: Bearer` only to the listed authorities under `/bridgehead/`.
The token is not appended to `sourceCellEndpoint`, browser URLs, or iteration
artifacts. Restart the server after changing the configuration. A conflicting
existing hostname route is rejected; resolver routes are keyed by hostname.

Keep the normal `--source-cell-endpoint cell://127.0.0.1:18083/PalazzoGuestShell`.
Setting the token only on the `npm run skeleton:iterate` process does not
configure the server. The existing authenticated Vapor transport adds the
header at the actual WebSocket connection; the generic query-items hook does
not cover the current dedicated `cell://` connection path. AdminScaffold HMAC
authentication takes precedence for its configured origin. Existing TLS policy
still applies (`ws` only where allowed for local development; `wss` remotely).

This token admits the transport connection. The requester's own identity and
the cell's existing access checks still govern configurations and actions.
It does not turn a Porthole guest into the Palazzo house owner or add support
for cell-specific configuration lookup/editing contracts.

## Scope: who sees a committed change

`cellScope` in `configure.swift` decides this, and it is easy to get wrong:

- `.scaffoldUnique` — one instance for the whole scaffold, so a committed
  override is **global**. Example: `ArendalsukaConfigurationPublisher`.
- `.identityUnique` — one instance per identity, so a committed override is
  **only visible to the identity that made it**. Example:
  `ConferenceParticipantShell`.

Check the scope before presenting a runtime change as landed for everyone.

## Persistence

A committed override is written to `CurrentCellConfiguration.json` in the cell's
directory (`OwnedCellConfigurationStore`, `EditableCellConfigurationSupport.swift`),
under `CELL_SCAFFOLD_RUNTIME_ROOT`. In production that path is bind-mounted from
the host, so overrides survive redeploy. The store is not cluster-aware; it
assumes a single node.

Runtime preview is the safe default. Permanent source-backed writes require `--mode commit-runtime`.

An end-to-end runbook for non-developers is in
`Documentation/Operations/skeleton-runtime-endring-20260831/README.md`.
