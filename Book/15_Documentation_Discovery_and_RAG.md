# Chapter 15 - Documentation Discovery and RAG

This chapter defines required functionality for practical documentation search and retrieval across HAVEN repositories, for both human developers and AI coding assistants.

## 1. Goals

- Find the right doc quickly from code-level questions.
- Preserve one canonical source per contract/topic.
- Make retrieval deterministic enough for automated coding flows.
- Support staging operations and production hardening without prompt archaeology.

## 2. Discovery Contract (Minimum)

Every major feature area should expose:

- canonical doc path
- owner repo
- owning module/cell
- last verified date
- related runtime endpoints/keypaths
- deprecation/replacement status

Recommended front matter fields:

- `doc_id`
- `title`
- `repo`
- `owner`
- `audience` (`human`, `ai`, `both`)
- `status` (`active`, `legacy`, `draft`)
- `last_verified`
- `source_code`
- `interfaces`

## 3. Retrieval Units for RAG

RAG ingestion should chunk docs by semantic units, not fixed-size slices:

- contract blocks (`Input`, `Output`, `Errors`)
- endpoint/keypath lists
- runbook procedures
- migration caveats
- compatibility notes

Required metadata per chunk:

- `repo`
- `path`
- `section_heading`
- `interfaces`
- `last_verified`
- `status`

## 4. Staging Gaps to Close

Observed gaps from current repositories:

1. Missing root README/index in several repos causes weak discoverability.
2. Absolute local paths in docs reduce portability and retrieval quality.
3. Some docs lag code for newly added endpoints/contracts.
4. Duplicated copies of docs across repos create drift risk.

## 5. Required Feature Additions (Cell-based Documentation)

1. Documentation Catalog Cell
- Index all docs as typed records with metadata fields above.
- Expose query by topic, interface, repo, and status.

2. Contract Extractor Cell
- Parse source code (routes, keypaths, structs) into machine-readable contract snapshots.
- Diff against docs and emit stale-doc alerts.

3. DocLink Resolver Cell
- Map runtime symbols to canonical docs (for UI hover/help and AI retrieval).
- Resolve aliases and deprecated paths.

4. Freshness Scoring Cell
- Compute staleness score using last code change vs last doc verification.
- Emit prioritized backlog entries.

5. RAG Query Audit Cell
- Log which doc chunks were used to answer operational and coding questions.
- Surface low-confidence/low-coverage queries for doc improvements.

## 6. RAG API Requirements (Staging)

The staging RAG gateway should support:

- query by repository + interface (`repo=CellScaffold`, `interface=/rag-mvp/api/:caseID/query`)
- query by symbol (`VaporRAGMVP`, `flowElementSkeleton`)
- explicit source citations (path + heading)
- result filtering by `status=active`
- freshness filter (`last_verified >= X`)

## 7. Workflow for Teams and AI Agents

1. Code change lands.
2. Contract Extractor identifies affected interfaces.
3. Freshness Scoring flags impacted docs.
4. Agent/human updates canonical docs.
5. Catalog Cell and RAG index refresh.
6. Query Audit validates retrievability.

## 8. Done Definition

Documentation search is considered production-ready when:

- interface-to-doc lookup succeeds for core runtime surfaces
- stale-doc alerts are generated automatically
- AI answers include canonical sources and no stale aliases
- onboarding developers can find endpoint/keypath docs without prompt-only guidance
