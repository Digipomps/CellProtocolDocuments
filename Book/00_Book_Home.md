# Book Home

This note is the vault-first landing page for `CellProtocolDocuments/Book`.

Use it when `Book` is opened directly in Obsidian, through the `/book` browser, or from a future native Swift reference browser.

The goal is one canonical markdown landing page that works across vault, web, Swift, and RAG.

## Start Here

- [Chapter 17 — Documentation Workbench Landing and Development Plan](17_Documentation_Workbench_Landing_and_Development_Plan.md)
- [Chapter 16 — Book Reference Workspace](16_Book_Reference_Workspace.md)
- [Chapter 15 — Documentation Discovery and RAG](15_Documentation_Discovery_and_RAG.md)
- [Chapter 10 — Quickstart](10_Quickstart.md)
- [Chapter 11 — Developer Guide: Implementing a Cell](11_Developer_Guide_Cell.md)
- [Chapter 12 — Skeleton Specification](12_Skeleton_Spec.md)
- [Chapter 22 — Explore Contracts for Skeleton and Cell Authoring](22_Explore_Contracts_For_Skeleton_Authoring.md)
- [Chapter 29 — Claim Argument Model](29_Claim_Argument_Model.md)

## What We Have Right Now

### Working documentation surfaces

- `/book` gives a browsable documentation site backed by this markdown source tree.
- `cell:///MarkdownRenderer` renders Book markdown to both web and Swift payloads.
- `cell:///MermaidRenderer` renders Mermaid blocks inline from fenced markdown.
- `Book/book_catalog.json` provides stable `doc_id`, slug, order, and grouping for browse and citation flows.

### Working adjacent tools

- `/rag-mvp` is a separate authenticated RAG work surface with query, corpus, links, and member administration.
- `/vault/api/*` exposes note create, update, get, list, and link operations for Vault/Obsidian-style note work.
- `/todo-mvp/api/*` exposes Todo state and actions, but does not yet have a real integrated UI surface.

### Important truth about current parity

- The shared markdown source is strong.
- The Book browser exists.
- RAG exists.
- Vault and Todo exist as capabilities.
- What is still missing is one unified documentation workbench that ties these surfaces together cleanly.

## Browse by Section

### Core Protocol

- [Chapter 01 — CellProtocol Core](01_CellProtocol_Core.md)
- [Chapter 02 — Cell Interfaces](02_Cell_Interfaces.md)

### Identity and Authorization

- [Chapter 03 — Identity Model](03_Identity_Model.md)
- [Chapter 04 — Agreements and Contracts](04_Agreements_Contracts.md)

### Event Model and Execution

- [Chapter 05 — Flows and Stream Lifecycle](05_Flows_Lifecycle.md)
- [Chapter 06 — CellResolver](06_CellResolver.md)
- [Chapter 07 — Scaffold and Runtime Model](07_Scaffold_Runtime.md)

### Connectivity and Semantics

- [Chapter 08 — Bridging and Transport](08_Bridging_Transport.md)
- [Chapter 21 — Contact Endpoint Cell](21_Contact_Endpoint_Cell.md)

### Semantics, Trust, and Human Alignment

- [Chapter 09 — Purpose and Interests](09_Purpose_Interests.md)
- [Chapter 29 — Claim Argument Model](29_Claim_Argument_Model.md)

### Developer Guides

- [Chapter 10 — Quickstart](10_Quickstart.md)
- [Chapter 11 — Developer Guide: Implementing a Cell](11_Developer_Guide_Cell.md)
- [Chapter 12 — Skeleton Specification](12_Skeleton_Spec.md)
- [Chapter 13 — Agent Instructions (Cells + Skeleton UI)](13_Agent_Instructions.md)
- [Chapter 14 — Perspective Runtime Matching (Phase 0 + 1)](14_Perspective_Runtime_Matching.md)
- [Chapter 15 — Documentation Discovery and RAG](15_Documentation_Discovery_and_RAG.md)
- [Chapter 16 — Book Reference Workspace](16_Book_Reference_Workspace.md)
- [Chapter 17 — Documentation Workbench Landing and Development Plan](17_Documentation_Workbench_Landing_and_Development_Plan.md)
- [Chapter 22 — Explore Contracts for Skeleton and Cell Authoring](22_Explore_Contracts_For_Skeleton_Authoring.md)

### Supplementary Material

- [Chapter 17 — Conference Ownership and Dataflow](17_Conference_Ownership_Dataflow.md)
- [Chapter 18 — ConferenceConnectionHubCell, Agreements, and Entity Lifecycle](18_Conference_ConnectionHub_Agreement_Entity_Lifecycle.md)
- [Book Extras](Book_Extras.md)

## Operational Entry Points

Use these when moving from reading to working:

- [Book browser](/book)
- [RAG MVP](/rag-mvp)
- `GET /book/api/tree`
- `GET /book/api/doc/:docID`
- `GET /book/api/rendered/:docID`
- `GET /vault/api/notes`
- `GET /vault/api/note/:id`
- `POST /vault/api/note`
- `POST /vault/api/link`
- `GET /todo-mvp/api/state`
- `POST /todo-mvp/api/action`

## Recommended Reading Paths

### If you are trying to understand the documentation workspace itself

- [Chapter 15 — Documentation Discovery and RAG](15_Documentation_Discovery_and_RAG.md)
- [Chapter 16 — Book Reference Workspace](16_Book_Reference_Workspace.md)
- [Chapter 17 — Documentation Workbench Landing and Development Plan](17_Documentation_Workbench_Landing_and_Development_Plan.md)

### If you are implementing cells or UI

- [Chapter 10 — Quickstart](10_Quickstart.md)
- [Chapter 11 — Developer Guide: Implementing a Cell](11_Developer_Guide_Cell.md)
- [Chapter 12 — Skeleton Specification](12_Skeleton_Spec.md)
- [Chapter 13 — Agent Instructions (Cells + Skeleton UI)](13_Agent_Instructions.md)
- [Chapter 22 — Explore Contracts for Skeleton and Cell Authoring](22_Explore_Contracts_For_Skeleton_Authoring.md)

### If you are working on docs plus AI retrieval

- [Chapter 15 — Documentation Discovery and RAG](15_Documentation_Discovery_and_RAG.md)
- [Chapter 16 — Book Reference Workspace](16_Book_Reference_Workspace.md)
- [Chapter 17 — Documentation Workbench Landing and Development Plan](17_Documentation_Workbench_Landing_and_Development_Plan.md)

## Reference Workspace Notes

- `book_catalog.json` is the machine-readable tree for vault, Swift, web, and RAG browse flows.
- `16_Book_Reference_Workspace.md` defines the canonical browse/render contract for the book itself.
- Mermaid fences should stay in source markdown and render inline in clients that implement the reference workspace contract.
- The documentation workbench chapter captures the current ground truth and the recommended next implementation steps for a proper docs workbench.
- The conference supplementary chapters capture ownership/dataflow and ConnectionHub/agreement lifecycle ground truth.
- The contact endpoint chapter defines the CellProtocol-closed pattern for leaving a reachable, TTL-bound contact cell in a scaffold.
- The claim argument model chapter defines the runtime structures for claims,
  support nodes, counterarguments with polarity, and deterministic graded
  argument evaluation, sharing wire vocabulary with the text reliability chapter.
