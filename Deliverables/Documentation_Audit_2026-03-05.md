# Cross-Repo Documentation Audit (2026-03-05)

Scope: repositories under `HAVEN` workspace.

## 1. Summary

Audit result:

- Active and mostly synced docs: `CellProtocol`, `CellScaffold`, `DiMyMicropayments`, `sprout`
- Central canonical docs need cleanup: `CellProtocolDocuments`
- Root entry docs were missing in 5 repos and were added in this audit pass: `Binding`, `CellUtility`, `DiMyDocuments`, `WatchPong`, `DiMy Source Editor Extension`
- Legacy/minimal repo docs: `HAVEN_MVP`

## 2. Repo-by-Repo Findings

1. Binding
- Root README added in this audit pass.
- `Documentation/README.md` link structure was reviewed and is currently consistent.

2. CellProtocol
- README updated recently; no NLNet refs.
- Action: keep Book chapter list synced with `CellProtocolDocuments`.

3. CellProtocolDocuments
- `Book/13_Agent_Instructions.md` had stale Object caveat (fixed).
- `Book/12_Skeleton_Spec.md` caveat section stale for Object mismatch (fixed).
- `DEVELOPERS.md` was truncated/broken (fixed).
- Action: treat this repo as canonical source for protocol/runtime docs.

4. CellScaffold
- README had absolute local paths (fixed to relative).
- README lacked explicit admin catalog route notes (fixed).
- Action: keep `Documentation/RAG_MVP_UI.md` and README route list in sync with `VaporRAGMVP` and `VaporAdminMVP`.

5. DiMyMicropayments
- README had absolute local paths (fixed to relative).
- Runtime config lacked `DIMY_MINT_INTERNAL_TOKEN` note (fixed).

6. DiMyMint
- README is concise and still relevant for bootstrap scope.

7. HAVEN_MVP
- README was a stale one-liner (replaced with status + ownership pointers).

8. DiMyDocuments
- Root README added in this audit pass.
- Staging route status note was updated from static 404 claim to deploy-time verification checklist.
- Action: add canonical index with active vs archival docs.


9. CellUtility, WatchPong, DiMy Source Editor Extension
- Minimal root README entrypoints were added in this audit pass.

10. sprout
- Good baseline docs for quickstart, threat model, and guides.
- Action: add doc metadata fields for RAG ingestion consistency.

11. test/test
- Minimal sample/test repo; README aligns with low scope.
- Action: none (keep minimal).

12. tmp/FileUtils-c
- Vendor-style utility repo with stable minimal README.
- Action: none in this audit scope (treat as external dependency surface).

## 3. Practical Gaps for Search/RAG

1. Canonical ownership not explicit enough across repos.
2. Absolute local paths remain in multiple non-canonical docs.
3. No automatic stale-doc detection against code signatures.
4. Duplicated embedded copies of docs across repos can drift.

## 4. Recommended Next Implementation Steps

1. Build Documentation Catalog Cell (cross-repo index + metadata).
2. Build Contract Extractor Cell (routes/keypaths/signatures from code).
3. Add freshness scoring and stale-doc queue in staging admin UI.
4. Enforce relative path policy in markdown lint/check.
5. Add RAG query filters for `repo`, `interface`, `status`, `last_verified`.
