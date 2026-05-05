# Documentation Audit — 2026-04-29

## Scope

Reviewed repositories in `HAVEN`:

- `Binding`
- `CellProtocol`
- `CellProtocolDocuments`
- `CellScaffold`
- `CellUtility`
- `DiMy Source Editor Extension`
- `DiMyDocuments`
- `DiMyMicropayments`
- `DiMyMint`
- `HAVEN_MVP`
- `sprout`

Explicitly excluded:

- `UniverseSimulation`
- Apple Watch app surfaces (`WatchPong`, `AppleWatchApps`)

## Method

The audit used four checks:

1. Inventory of repo-level and docs-folder markdown.
2. Local markdown link validation for active documentation.
3. Diffing of mirrored `CellProtocolDocuments` copies inside `Binding` and `CellScaffold` against the canonical `CellProtocolDocuments` repo.
4. Spot verification of documentation claims against current code, package manifests, controllers, scripts, and tests.

## Executive Summary

The documentation is **not uniformly up to date** across the workspace.

What is in good shape:

- `CellScaffold` documentation is largely current and is backed by real scripts/tests.
- `CellProtocol/commons` documentation is current and aligned with the actual CLI/cell surfaces.
- `sprout` documentation is current and consistent with package/app layout.
- Smaller repos with intentionally lightweight docs (`CellUtility`, `DiMy Source Editor Extension`, `HAVEN_MVP`, `DiMyDocuments`) are mostly accurate within their stated scope.

What is not in good shape:

- `CellProtocolDocuments` is still presented as canonical, but key parts are stale relative to current code.
- Mirrored `CellProtocolDocuments` copies in `Binding` and `CellScaffold` have drifted.
- `Binding/Documentation/README.md` has broken quick links.
- `Binding/Documentation/SkeletonModifiers.md` looks malformed/corrupted, not just old.
- `DiMyMicropayments` doc indexes are stale and no longer reflect all iteration docs.
- `DiMyMint/README.md` is outdated relative to the current package manifest and persistence layer.

## Repo Status

### `Binding`

Status: **Partially current, but not fully trustworthy as a docs entrypoint**

Verified current:

- Root README reflects active standalone-boundary work and points to existing docs.
- Conference verifier doc and runner both exist.
- Binding-specific docs are numerous and actively maintained.

Problems:

- `Documentation/README.md` has broken quick links because it links to `Documentation/...` from inside the `Documentation` folder instead of linking to sibling files.
- `Documentation/SkeletonModifiers.md` is malformed and contains pasted code / broken references.
- `Binding/CellProtocolDocuments` is not in sync with canonical `CellProtocolDocuments`.

### `CellProtocol`

Status: **Current and relevant**

Verified current:

- `commons/README.md` matches the actual `haven-commons` executable target and the documented `cell:///CommonsResolver`, `cell:///CommonsTaxonomy`, and `cell:///EntityAtlas` surfaces.
- `commons/docs/README.md` points to real docs and current concepts.

Note:

- The `commons` documentation is in better shape than the canonical protocol book for implementation details that have moved quickly.

### `CellProtocolDocuments`

Status: **Canonical in intent, but stale in important implementation details**

Verified current:

- Structure and major book chapters still exist.
- Quickstart and developer guide still broadly match the current Swift runtime.

Problems:

- `README-CellProtocol.md` links to `SSH_SETUP.md`, but that file does not exist in the repo.
- `Book/12_Skeleton_Spec.md` is behind current code:
  - it documents only array-style `HStack/VStack`, while the runtime also supports object form with `elements`, `spacing`, and `modifiers`
  - it does not document `styleRole` / `styleClasses`
  - it does not document `Picker`, which is implemented in the core model and Apple renderer
- Repo head is older than recent `CellProtocol`, `Binding`, and `CellScaffold` work, so “canonical” status is currently not enough on its own.

### `CellScaffold`

Status: **Current and relevant**

Verified current:

- README route docs match actual controllers and tests.
- RAG gateway env vars match real config/service code.
- AI gateway env vars in README match Docker and runtime code.
- `Documentation/ConfigurationCatalog/README.md` points to a real regeneration script and parity tests.

Note:

- `CellScaffold/CellProtocolDocuments` is not a clean mirror of canonical `CellProtocolDocuments`; it contains local drift and extra local chapters. That is acceptable only if treated as a forked surface, not a mirror.

### `CellUtility`

Status: **Current within limited scope**

- The README accurately says standalone docs are minimal and source files are the main reference.

### `DiMy Source Editor Extension`

Status: **Current within limited scope**

- The README accurately reflects an early-stage project with lightweight documentation.

### `DiMyDocuments`

Status: **Current as a document-first archive/workbench**

- The README accurately describes the repo as a documentation-first collection with both active and archival material.

### `DiMyMicropayments`

Status: **Core docs mostly current, but indexes are stale**

Verified current:

- Package/module docs match `Package.swift`.
- API/runtime/env-var docs match current code for `registerScaffoldCells`, `registerBindingCells`, `DIMY_MINT_INTERNAL_TOKEN`, and `DIMY_SIGNATURE_ENVELOPE_FORMAT`.

Problems:

- `README.md` only indexes iterations through `ITERATION-11`, while the repo contains later iterations.
- `docs/README.md` is also stale and stops at `ITERATION-11`.
- `docs/iterations/README.md` includes through `ITERATION-15`, but the repo also contains `ITERATION-16`.

### `DiMyMint`

Status: **README is outdated**

Verified current:

- The repo now has real persistence and Postgres integration.
- Package manifest defines `DiMyMintPersistence` and depends on `postgres-nio`.

Problems:

- `README.md` does not mention `DiMyMintPersistence`.
- `README.md` still says the package depends on sibling `../DiMyMicropayments` and should later switch to Git, but `Package.swift` already uses a Git dependency.
- `README.md` still describes production storage as “next phase”, while the repo already contains a concrete persistence module.

### `HAVEN_MVP`

Status: **Relevant as historical documentation**

- The README accurately describes the repo as a historical MVP reference rather than an active implementation target.

### `sprout`

Status: **Current and relevant**

Verified current:

- README status matches current product split (`sprout`, `sprout-updater`, `sprout-macos`).
- `docs/developer_guide.md` matches actual package/app layout, including `sprout-admin`.
- `Apps/sprout-ios/README.md` confirms the iOS wrapper is still placeholder-only, which aligns with README scope statements.

## Concrete Findings

### 1. `Binding/Documentation/README.md` quick links are broken

Evidence:

- `Binding/Documentation/README.md` links sibling docs as `Documentation/<file>.md` from inside the `Documentation` directory.
- Example lines: `345-367`.

Impact:

- The main Binding docs index is not a reliable navigation surface.

### 2. `Binding/Documentation/SkeletonModifiers.md` is malformed, not just stale

Evidence:

- The file is commented-out prose for the first 94 lines.
- At line `116` it opens a JSON code block and then drifts into pasted UIKit code without closing the example cleanly.
- At lines `142-143` it links to `SkeletonElements.md`, which does not exist.

Impact:

- This document should not be used as normative Skeleton guidance in its current state.

### 3. Canonical `CellProtocolDocuments` links to a missing `SSH_SETUP.md`

Evidence:

- `CellProtocolDocuments/README-CellProtocol.md:45`
- The same broken reference is repeated in the mirrored copies under `Binding` and `CellScaffold`.

Impact:

- A canonical entrypoint currently points readers to a non-existent setup document.

### 4. Canonical Skeleton spec is behind current runtime capabilities

Evidence:

- `CellProtocolDocuments/Book/12_Skeleton_Spec.md:120-131` documents only array-form `HStack/VStack`.
- Runtime code supports object-form stacks with `elements`, `spacing`, and `modifiers`:
  - `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:583-646`
  - `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:650-706`
- `CellProtocolDocuments/Book/12_Skeleton_Spec.md` does not document `styleRole` or `styleClasses`.
- Runtime code exposes them in `SkeletonModifiers`:
  - `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:31-39`
- `CellProtocolDocuments/Book/12_Skeleton_Spec.md` does not document `Picker`.
- Runtime code defines `SkeletonPicker`:
  - `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1613-1764`

Impact:

- The canonical UI spec is no longer sufficient for current implementation work.

### 5. Mirrored `CellProtocolDocuments` copies have drifted

Evidence:

- `Binding/CellProtocolDocuments/README-CellProtocol.md` omits chapters `15` and `16`, plus newer index entries.
- `CellScaffold/CellProtocolDocuments/README-CellProtocol.md` omits chapter `16`, `00_Book_Home`, and `book_catalog.json`.
- Book diffs show additional drift:
  - `Binding/CellProtocolDocuments/Book`: `diff_count 8`
  - `CellScaffold/CellProtocolDocuments/Book`: `diff_count 5`, `extra_count 2`

Impact:

- Readers can get different protocol guidance depending on which repo-local copy they open.

### 6. `DiMyMicropayments` indexes are stale

Evidence:

- `DiMyMicropayments/README.md:144-161` stops at `ITERATION-11`.
- `DiMyMicropayments/docs/README.md:11-24` also stops at `ITERATION-11`.
- `DiMyMicropayments/docs/iterations/README.md:3-18` goes through `ITERATION-15`.
- The repo also contains `docs/iterations/ITERATION-16-sprint1-cell-productivity-backlog.md`.

Impact:

- Repo readers do not see the actual latest planning/iteration material from the primary entrypoints.

### 7. `DiMyMint/README.md` no longer matches the package manifest

Evidence:

- `DiMyMint/README.md:5-14` documents only `DiMyMintCore`, `DiMyMintHTTP`, and `DiMyMintServer`, and says sibling package dependency should later be switched to Git.
- `DiMyMint/Package.swift:11-20` now includes `DiMyMintPersistence`, Git-based `DiMyMicropayments`, and `postgres-nio`.

Impact:

- New readers get an older architecture picture than what the repo actually builds today.

## Recommended Priority

### P0

- Fix `Binding/Documentation/README.md` quick links.
- Replace or rewrite `Binding/Documentation/SkeletonModifiers.md`.
- Remove or restore the `SSH_SETUP.md` reference in canonical `CellProtocolDocuments`.
- Update canonical `Book/12_Skeleton_Spec.md` to match current runtime.

### P1

- Decide whether `Binding/CellProtocolDocuments` and `CellScaffold/CellProtocolDocuments` are true mirrors or intentional forks.
- If mirrors: sync them from canonical immediately.
- If forks: label them clearly as forked/local documentation surfaces.

### P2

- Refresh `DiMyMicropayments` indexes to include iterations 12-16.
- Refresh `DiMyMint/README.md` to mention persistence, Postgres, and the current Git dependency model.

## Bottom Line

The documentation set is **partially updated, but not fully verified as current**.

The main risk is not that everything is stale. The risk is that the most authoritative-looking surfaces are inconsistent:

- `CellProtocolDocuments` still looks canonical, but parts of it lag current code.
- repo-local mirrored copies disagree with the canonical repo
- some high-traffic entrypoints (`Binding/Documentation/README.md`, `DiMyMicropayments` indexes, `DiMyMint/README.md`) are outdated or broken

For day-to-day implementation guidance today, `CellScaffold` docs, `CellProtocol/commons`, and `sprout` are the strongest surfaces. `CellProtocolDocuments` needs a refresh before it can safely be treated as the single source of truth again.
