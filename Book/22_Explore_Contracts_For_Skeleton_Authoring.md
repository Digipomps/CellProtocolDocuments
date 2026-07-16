# Chapter 22 - Explore Contracts for Skeleton and Cell Authoring

Last verified against code: 2026-07-14

Status: Phase 1 started. The current runtime has the necessary foundation in
`ExploreContract`, `ExploreContractCatalog`, `ExploreManifest`, and
`CellContractHarness`, but not every production cell has complete explicit
contracts yet.

## Purpose

Explore is the public, machine-readable contract surface for a Cell. Its job is
to let a human, agent, Porthole, Binding, or another runtime understand what a
Cell exposes without reading Swift source code.

For skeleton and cell authoring, Explore must answer:

- which keys exist
- whether each key is read, write/action, or both
- what payload shape a write/action accepts
- what shape a read/action returns
- what permissions are required
- which flow topics are emitted as side effects
- whether the contract is stable enough for generated UI or generated code

This chapter defines the authoring standard. It is stricter than the legacy
minimum protocol, because the legacy minimum only guarantees `keys(...)` and
`typeForKey(...)`.

## Current Implementation Ground Truth

Authoritative runtime sources:

- `CellProtocol/Sources/CellBase/Protocols/CellProtocol.swift`
- `CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift`
- `CellProtocol/Sources/CellBase/Cells/GeneralCell/ExploreContract.swift`
- `CellProtocol/Sources/CellBase/Cells/GeneralCell/ExploreContractCatalog.swift`
- `CellProtocol/Sources/CellBase/Cells/GeneralCell/ExploreManifest.swift`
- `CellProtocol/Tests/CellBaseTests/TestSupport/CellContractHarness.swift`

Current guarantees:

- `Explore.keys(requester:)` returns advertised keys.
- `Explore.typeForKey(key:requester:)` returns a `ValueType`.
- `GeneralCell` retains the legacy per-key `schemaDict` view and stores explicit
  method-aware operation contracts in a `(key, method)` sidecar.
- Strict handler registration requires a complete contract for the exact key
  and method. A GET contract does not authorize SET registration, or vice
  versa.
- `ExploreContract.keyContract(...)` can encode a structured operation contract.
- `ExploreContractCatalogBuilder` exports distinct GET and SET records for a
  dual-method key while retaining stable legacy IDs where possible.
- `ExploreManifestBuilder` can combine operation contracts with discovery intent.

Current limits:

- `schemaDescriptionForKey(...)` exists on `GeneralCell`, but is not part of the
  formal `Explore` protocol.
- Some cells and computed-key registrations still require manual contract
  review; a zero-error source audit is not a runtime schema proof.
- The formal `Explore` protocol and remote Bridge
  `typeForKey(key:requester:)` still expose one legacy value per key. Local
  strict dispatch and catalogs are method-aware, but remote discovery of both
  methods for one key needs a deliberately versioned wire contract and
  cross-runtime fixtures.
- Legacy methodless schemas remain readable in permissive/warn modes for
  compatibility. Strict mode rejects handler installation until an exact
  method contract exists.

## Normative Operation Contract

Each public operation must advertise one contract identified by `(key,
method)`. Local catalogs can expose more than one operation for a key. The
legacy remote `typeForKey(...)` view cannot by itself prove both operations.

Required fields:

```json
{
  "contractVersion": 1,
  "key": "example.action",
  "method": "set",
  "input": {
    "type": "object",
    "properties": {
      "title": { "type": "string" }
    },
    "requiredKeys": ["title"]
  },
  "returns": {
    "type": "object",
    "properties": {
      "status": { "type": "string" }
    },
    "requiredKeys": ["status"]
  },
  "permissions": ["-w--"],
  "required": true,
  "flowEffects": [
    {
      "trigger": "set",
      "topic": "example.completed",
      "contentType": "object",
      "minimumCount": 1
    }
  ],
  "summary": "Runs the example action."
}
```

Required semantics:

- `method` is `get` or `set`.
- `input` is `.null` for plain `get` keys.
- `input` must be explicit for every `set` key.
- `returns` must be explicit for every key unless the return is intentionally
  `null`.
- `permissions` must name the effective access expectation.
  Permission strings are canonical four-character `rwxs` values as defined in
  [Chapter 04](04_Agreements_Contracts.md#21-canonical-rwxs-permission-form).
  Read permission does not imply Storage permission, and Storage permission
  does not imply forwarding authority.
- `flowEffects` must list observable flow topics caused by this operation.
- `summary` is human-facing, but should remain concise enough for RAG snippets.

Recommended Phase 1 additions:

- `examples`: named sample inputs and expected outputs.
- `stability`: `stable`, `experimental`, `demo`, or `deprecated`.
- `capabilities`: machine-readable capability tags such as
  `profile.read`, `message.send`, or `attachment.upload`.
- `error`: structured error envelope schema when the operation returns errors
  as data instead of throwing.

## Schema Dialect

The runtime currently uses HAVEN `ValueType` descriptors:

- `string`
- `integer`
- `float`
- `bool`
- `object`
- `list`
- `data`
- `null`
- `oneOf`
- `unknown`

For external tooling and cross-runtime exports, prefer a JSON Schema-compatible
subset:

- HAVEN `list` maps to JSON Schema `array`.
- HAVEN `bool` maps to JSON Schema `boolean`.
- HAVEN `requiredKeys` maps to JSON Schema `required`.
- HAVEN `properties` maps directly to JSON Schema `properties`.
- HAVEN `oneOf` maps directly to JSON Schema `oneOf`.

Do not invent free-form shapes in new contracts. If the current helper cannot
express a shape, document the gap and add a typed helper instead of embedding
ambiguous prose.

## Contract Completeness Levels

Use these levels in audits, docs, and reviews:

- `complete`: explicit method, input, returns, permissions, summary, and flow
  effects when applicable.
- `partial`: method exists, but input or returns are `unknown` or missing.
- `implicit`: key was registered by an intercept and fell back to
  `ExploreContract.defaultContract(...)`.
- `unimplemented`: `keys` or `typeForKey` returns placeholder data.
- `unverifiable`: contract exists but no test, probe, or sample verifies it.

Production skeletons should only bind to `complete` contracts, except during a
clearly marked migration preview.

## Skeleton Binding Rules

Skeleton authoring must validate every remote binding before preview or commit.

Minimum binding expectations:

- `Text.keypath` and `Text.url`: matching `get` operation with displayable
  return type.
- `TextField.sourceKeypath`: matching `get` operation with scalar return type.
- `TextField.targetKeypath`: matching `set` operation with scalar-compatible
  input.
- `TextArea.sourceKeypath`: matching `get` operation with string/scalar return
  type.
- `TextArea.targetKeypath`: matching `set` operation with string/scalar input.
- `List.keypath`: matching `get` operation returning `list`/`array`.
- `Grid.keypath`: matching `get` operation returning `list`/`array`.
- `Picker.keypath`: matching `get` operation returning `list`/`array`.
- `Button.keypath` with `payload`: matching `set` operation.
- `Button.keypath` without `payload`: matching `get` operation, or a design
  review if the intent is actually an action.
- `Toggle.keypath`: matching `set` operation accepting `bool`/`boolean`.
- `FileUpload.actionKeypath`: matching `set` operation accepting object/list/data
  upload payload.
- `Reference.keypath`: matching readable list/object feed source.
- `Tabs.tabsKeypath`: matching `get` operation returning `list`/`array`.
- `Tabs.activeTabStateKeypath` and `Tabs.selectionActionKeypath`: matching `set`
  operations.
- `Visualization.keypath`: matching `get` operation returning object/list.
- `Visualization.actionKeypath`: matching `set` operation.
- `modifiers.visibility.when.keypath` with `scope: "root"` or omitted scope:
  matching `get` operation with a displayable/scalar/object/list/null-compatible
  return type. `scope: "item"` and `scope: "context"` are local render-context
  reads and should be checked against the item/context schema where available,
  not treated as remote Cell reads by default.
- `modifiers.presentation.openStateKeypath`: matching `get` operation when
  provided. Portable skeletons should still use `modifiers.visibility` as the
  open/closed source of truth.
- `modifiers.presentation.closeActionKeypath`: matching `set` operation when
  Escape/backdrop/native dismiss can close the presentation.

Calendar skeletons use the same rule: `Visualization(kind: "calendar")` must
bind to a readable `haven.calendar.visualization.v1` or store-state object, and
all public calendar paths must have explicit Explore contracts before publication:
`calendar.state`, `calendar.collections`, `calendar.items`, `calendar.occurrences`,
`calendar.queryOccurrences`, `calendar.createItem`, `calendar.updateItem`,
`calendar.deleteItem`, `calendar.import`, `calendar.export`, and
`calendar.permissionStatus`.

Relative keypaths resolve to the skeleton's default endpoint, usually
`cell:///Porthole`, unless the first path segment matches a
`CellConfiguration.cellReferences[].label`. For example, `chat.messages` can
resolve to the endpoint labelled `chat` if that label exists.

Nested paths may match a parent contract, such as `state.title` matching a
contract for `state`. That is allowed only as a warning until the parent schema
declares child properties.

## New Tools

Phase 1 introduces two repository-local tools in
`CellProtocolDocuments/Tools/Explore`.

### Explore contract audit

```bash
python3 Tools/Explore/explore_contract_audit.py \
  --repo-root ../CellProtocol \
  --json-output /tmp/explore-audit.json \
  --markdown-output /tmp/explore-audit.md
```

The audit scans Swift source for:

- `addInterceptForGet`
- `addInterceptForSet`
- `registerExploreContract`
- `registerExploreSchema`
- `registerGet`
- `registerSet`

The auditor applies these source-level rules:

- metadata-free `registerGet`/`registerSet` and raw intercept calls are handler
  registrations, not weak contracts;
- typed `registerGet`/`registerSet` calls cover their own handler, while
  `registerExploreContract`/`registerExploreSchema` are separate contract
  publications;
- a separate contract covers a handler only in the same nominal Cell scope
  (or the same file when no Cell type is recoverable), for the exact key and
  method, and only when it is reached earlier in the same function or through
  an earlier direct same-Cell helper call;
- literal string and tuple loops are expanded into their statically knowable
  operations;
- computed key expressions and computed loops remain manual-review warnings;
- framework registration declarations and known forwarders are excluded from
  production-handler counts.

This remains a regex-based static source scan, not a Swift compiler or runtime
probe. It does not prove conditional dominance, early-return behavior,
registration launched in a deferred `Task`, overloaded-helper resolution,
runtime schema conformance, permission alignment, or flow-effect correctness.
Interpret `0 errors` as “no uncovered literal operation under this audit
model,” never as complete Explore or remote-wire proof.

Auditor regressions, including an optional live Chat golden, run with:

```bash
CELLPROTOCOL_REPO=../CellProtocol \
  python3 -m unittest discover -s Tools/Explore/tests -v
```

### Skeleton Explore validator

```bash
python3 Tools/Explore/skeleton_explore_validator.py \
  --configuration path/to/CellConfiguration.json \
  --manifest path/to/ExploreManifest.json \
  --default-endpoint cell:///Porthole \
  --require-owner-access \
  --json-output /tmp/skeleton-validation.json \
  --markdown-output /tmp/skeleton-validation.md
```

For multiple cells:

```bash
python3 Tools/Explore/skeleton_explore_validator.py \
  --configuration path/to/CellConfiguration.json \
  --contract cell:///Porthole=path/to/porthole.manifest.json \
  --contract cell:///Chat=path/to/chat.manifest.json
```

The validator accepts:

- `ExploreManifest` with `operations`
- `ExploreContractCatalog` with `records`
- raw operation arrays
- a manifest index containing endpoint/path pairs

It extracts skeleton bindings, including root-scoped
`modifiers.visibility.when.keypath` conditions and presentation
`openStateKeypath`/`closeActionKeypath` fields, and checks that each binding has
a matching Explore operation with a compatible method and type. The validator
recurses through `allOf`, `anyOf`, and `not` visibility expressions. It does not
currently validate `item`/`context` visibility paths against per-item schemas;
review those manually until item schema export is available.

When `--require-owner-access` is set, the validator also checks for a visible
owner/entity access affordance. This is the static guardrail for
`purpose://skeleton.owner-entity-access`: a generated or user-authored skeleton
must leave the owner a path back to their own entity, Co-Pilot, or an
equivalent shell-provided recovery interface. The v1 checker recognizes
existing `Button`, `Reference`, `TextField`/`TextArea`, list/grid/picker/tab
bindings whose label, endpoint, keypath, topic, or payload clearly points to
Co-Pilot, chat, owner entity, entity anchor, or entity extension access.

If a runtime shell guarantees this affordance outside the portable skeleton,
document that shell guarantee in the scenario/review artifact. Do not rely on
`modifiers.visibility` to hide or reveal the only owner-access path; access to
the recovery affordance must not depend on data the broken skeleton might fail
to load.

## Authoring Workflow

When implementing or changing a Cell:

1. Define public `get` and `set` keys before writing UI.
2. Register every key with `registerExploreContract(...)` or strict-friendly
   `registerGet`/`registerSet` helpers.
3. Add `CellContractHarness` tests for at least one read, one write/action, and
   each declared flow side effect.
4. Run `explore_contract_audit.py` and fix new implicit contracts.
5. Export or build the relevant `ExploreManifest`.
6. Build or update the `CellConfiguration` and skeleton.
7. Run `skeleton_explore_validator.py` before runtime preview.
8. Run Porthole/Binding preview only after contract validation is clean or
   warnings are understood.

When authoring a skeleton from existing Cells:

1. Gather the relevant `ExploreManifest` or `ExploreContractCatalog` for each
   referenced cell.
2. Choose `cellReferences` and labels.
3. Generate only bindings that match the manifests.
4. Validate the skeleton statically.
5. Preview in Porthole.
6. Treat missing contracts as Cell work, not UI polish.
7. For production skeletons, run the owner-access check or document the
   renderer shell that guarantees equivalent access.

When a desired UI cannot be validated:

- If the key exists in code but not Explore, backfill the Explore contract.
- If the key does not exist, write the desired contract first.
- If the skeleton element type cannot express the UI, document the missing
  skeleton capability and ask Kjetil before implementing it.

## Migration Plan

### Phase 1 - Active now

- Make this chapter the normative contract authoring standard.
- Add audit and skeleton validator tools.
- Update agent prompts and skills to require Explore-first authoring.
- Run the audit and capture high-priority backfill targets.

### Phase 2

- Add complete explicit contracts to production cells used by current
  CellConfigurations.
- Design versioned operation-aware bridge discovery while preserving legacy
  `keys` and `typeForKey` consumers.
- Add manifest exports to normal scaffold diagnostics.

### Phase 3

- Gate CI for new production intercepts without explicit contracts.
- Gate skeleton scenario preview on `skeleton_explore_validator.py`.
- Export RAG chunks for every stable operation.

### Phase 4

- Generate skeleton drafts from Explore manifests.
- Generate Cell contract stubs from skeleton intent when required keys do not
  exist.
- Promote JSON Schema-compatible export for cross-language runtimes.

## Done Criteria

Explore is ready for skeleton and cell building everywhere when:

- every production Cell exposes complete explicit operation contracts
- bridge transports preserve Explore contracts
- every production skeleton validates against Explore before preview/commit
- no production skeleton depends on an unknown keypath
- contract tests/probes verify the declared behavior
- agents can build a basic skeleton from manifests without reading Swift source
- missing data/action support is reported as contract work, not hidden behind
  fake UI
