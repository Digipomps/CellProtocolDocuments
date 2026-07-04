# CellProtocol Documentation Index

This repository contains the official documentation for HAVEN CellProtocol. It is intended to be used as a Git submodule in the CellProtocol code repository.

## Documentation Table of Contents

1. Core Protocol  
   - [01_CellProtocol_Core.md](Book/01_CellProtocol_Core.md)  
   - [02_Cell_Interfaces.md](Book/02_Cell_Interfaces.md)

2. Identity & Authorization  
   - [03_Identity_Model.md](Book/03_Identity_Model.md)  
   - [04_Agreements_Contracts.md](Book/04_Agreements_Contracts.md)

3. Event Model & Execution  
   - [05_Flows_Lifecycle.md](Book/05_Flows_Lifecycle.md)  
   - [06_CellResolver.md](Book/06_CellResolver.md)  
   - [07_Scaffold_Runtime.md](Book/07_Scaffold_Runtime.md)

4. Connectivity & Semantics  
   - [08_Bridging_Transport.md](Book/08_Bridging_Transport.md)
   - [21_Contact_Endpoint_Cell.md](Book/21_Contact_Endpoint_Cell.md)

5. Semantics, Trust & Human Alignment  
   - [09_Purpose_Interests.md](Book/09_Purpose_Interests.md)
   - [23_Purpose_Knowledge_Base.md](Book/23_Purpose_Knowledge_Base.md)
   - [27_Text_Reliability_Analysis.md](Book/27_Text_Reliability_Analysis.md)

6. Developer Guides  
   - [10_Quickstart.md](Book/10_Quickstart.md)  
   - [11_Developer_Guide_Cell.md](Book/11_Developer_Guide_Cell.md)  
   - [12_Skeleton_Spec.md](Book/12_Skeleton_Spec.md)  
   - [13_Agent_Instructions.md](Book/13_Agent_Instructions.md)  
   - [14_Perspective_Runtime_Matching.md](Book/14_Perspective_Runtime_Matching.md)
   - [15_Documentation_Discovery_and_RAG.md](Book/15_Documentation_Discovery_and_RAG.md)
   - [16_Book_Reference_Workspace.md](Book/16_Book_Reference_Workspace.md)
   - [22_Explore_Contracts_For_Skeleton_Authoring.md](Book/22_Explore_Contracts_For_Skeleton_Authoring.md)
   - [28_RAG_Prompt_Transformer_Cell.md](Book/28_RAG_Prompt_Transformer_Cell.md)

7. Supplementary Material  
   - [Book_Extras.md](Book/Book_Extras.md)

## Additional Files

- [Gap_Analysis.md](Gap_Analysis.md) — Implementation gaps vs current docs  
- [Documentation_Audit_2026-03-05.md](Deliverables/Documentation_Audit_2026-03-05.md) — Cross-repo doc freshness audit and actions  
- [00_Book_Home.md](Book/00_Book_Home.md) — Vault landing note for opening `Book` directly in Obsidian or another markdown browser
- [book_catalog.json](Book/book_catalog.json) — Machine-readable Book index for vault/web/RAG browse flows
- [rag_prompt_transformer_cell_contract_v0.json](Book/rag_prompt_transformer_cell_contract_v0.json) — Draft machine-readable contract for adapting RAG source packages into model-targeted prompt packages
- [SystemPrompts.md](Prompts/SystemPrompts.md) — Guidance for AI/system prompts
- [SSH_SETUP.md](SSH_SETUP.md) — SSH og package-resolve playbook for Digipomps
- [DEVELOPERS.md](DEVELOPERS.md) — Utviklerguide og inngang til verktøy og rutiner
- [Tools/HavenDocsMCP](Tools/HavenDocsMCP/README.md) — Read-only MCP server for canonical docs lookup

## Agent Entrypoint

If you are implementing code or UI:

- Start with [10_Quickstart.md](Book/10_Quickstart.md)
- Then follow [11_Developer_Guide_Cell.md](Book/11_Developer_Guide_Cell.md)
- Use [12_Skeleton_Spec.md](Book/12_Skeleton_Spec.md) for UI JSON
- Follow [13_Agent_Instructions.md](Book/13_Agent_Instructions.md) for workflow and checklist
- Use [14_Perspective_Runtime_Matching.md](Book/14_Perspective_Runtime_Matching.md) when implementing weighted purpose/interest queries and cross-perspective matching
- Use [23_Purpose_Knowledge_Base.md](Book/23_Purpose_Knowledge_Base.md) when grounding prompts in the HAVEN purpose tree, Goals, shared ancestry, and matching/index strategy
- Use [27_Text_Reliability_Analysis.md](Book/27_Text_Reliability_Analysis.md) when analyzing texts for argumentation, rhetoric, source support, reliability, or Add2Entity capture sidecars
- Use [15_Documentation_Discovery_and_RAG.md](Book/15_Documentation_Discovery_and_RAG.md) for practical documentation discovery and RAG requirements
- Use [16_Book_Reference_Workspace.md](Book/16_Book_Reference_Workspace.md) for the canonical vault/web/Swift browse contract for `Book`
- Use [Tools/HavenDocsMCP](Tools/HavenDocsMCP/README.md) when an MCP client needs read-only access to canonical docs, search, resources, and static reading-path prompts
- Use [28_RAG_Prompt_Transformer_Cell.md](Book/28_RAG_Prompt_Transformer_Cell.md) when RAG output must be adapted into a target-model prompt package
- Use [21_Contact_Endpoint_Cell.md](Book/21_Contact_Endpoint_Cell.md) when implementing CellProtocol-closed contact endpoints with TTL, private routes, notification wakeup, and entity anchoring
- Use [22_Explore_Contracts_For_Skeleton_Authoring.md](Book/22_Explore_Contracts_For_Skeleton_Authoring.md) before generating skeletons or new Cells from public key contracts
