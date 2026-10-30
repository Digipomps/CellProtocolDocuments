# Skill-indeks (generert, forslag)

Generert av `Tools/SkillIndex/generate_skill_index.py`. Ikke rediger for hånd. Leser skill-mapper, endrer dem aldri.

- Unike navn: **43**. Med avvik mellom kopier: **21**. Bare ett sted: **7**. Med problemer: **1**.
- Steder: `user`, `scaffold`, `codex`, `cpdocs`, `ws-vegar-arendalsuka`, `ws-vegar-chat`, `ws-vegar-matching-design`, `ws-vegar-medvirkende`, `ws-vegar-personal-log`, `ws-vegar-stands`.

## Beskrivelsestegn per sted (det som havner i skill-listen)

| Sted | Tegn |
|---|---:|
| user | 15473 |
| scaffold | 14770 |
| codex | 0 |
| cpdocs | 1969 |
| ws-vegar-arendalsuka | 14567 |
| ws-vegar-chat | 7399 |
| ws-vegar-matching-design | 7165 |
| ws-vegar-medvirkende | 7165 |
| ws-vegar-personal-log | 13975 |
| ws-vegar-stands | 7165 |

Brukerskills pluss én worktree i samme økt (kopier med samme navn telles to ganger):

| Kombinasjon | Tegn |
|---|---:|
| user+ws-vegar-arendalsuka | 30040 |
| user+ws-vegar-chat | 22872 |
| user+ws-vegar-matching-design | 22638 |
| user+ws-vegar-medvirkende | 22638 |
| user+ws-vegar-personal-log | 29448 |
| user+ws-vegar-stands | 22638 |

Budsjettet i tegn er satt til 8000 for denne rapporten (se forutsetning i forslaget).

## Skills

| Navn | Sted | Formål (første setning) | Tegn | Avvik | Sist endret |
|---|---|---|---:|:-:|---|
| `align-on-change` | user | Pre-work alignment interview that interrogates a plan or change request until scope, success criteria, constraints, edge cases, and affected interfac… | 422 |  | mtime:2026-08-15 |
| `architecture-review` | user | Invariant-aware architecture review and deepening method — discover the project's actual invariants first, then check code against them and propose s… | 514 |  | mtime:2026-08-15 |
| `arendalsuka-data-pipeline` | user | Working knowledge of Vegar's Arendalsuka (Norway's largest political festival) data extraction, deduplication, and staging-export pipeline — the Duck… | 891 |  | mtime:2026-09-29 |
| `binding-skeleton-parity-testing` | 8 steder | Use when Codex or Claude needs to design, run, debug, or interpret parity tests for HAVEN CellConfiguration/Skeleton surfaces across CellScaffold web… | 574 | ja | mtime:2026-10-07 |
| `cellconfiguration-skeleton-authoring` | 8 steder | Generate, review, test, or edit CellConfiguration JSON and skeleton structures for HAVEN/CellProtocol. | 947 | ja | mtime:2026-09-29 |
| `cellprotocol-cell-authoring` | 4 steder | Use when creating, editing, reviewing, or testing individual HAVEN/CellProtocol Cells in the existing Swift runtime, including GeneralCell subclasses… | 374 | ja | mtime:2026-09-29 |
| `cellprotocol-contract-testing` | 4 steder | Use when writing, reviewing, or debugging HAVEN/CellProtocol contract tests, golden fixtures, replay determinism tests, resolver policy tests, skelet… | 285 |  | mtime:2026-09-29 |
| `cellprotocol-core-runtime-implementation` | 4 steder | Use when changing HAVEN/CellProtocol core runtime semantics or shared protocol machinery: Emit, Absorb, Meddle, Explore, FlowElement, ValueType, Cell… | 358 |  | mtime:2026-09-29 |
| `cellprotocol-cross-language-porting` | 4 steder | Use when implementing, reviewing, or planning CellProtocol in another language or runtime, especially Kotlin, Java, Rust, or Go. | 380 |  | mtime:2026-09-29 |
| `cellprotocol-distributed-entity-data` | 8 steder | Use when designing, implementing, reviewing or testing distributed HAVEN Entity/EntityAnchor data, replicas, offline sync, logical source of truth, o… | 340 |  | mtime:2026-09-29 |
| `cellprotocol-docs-and-rag-maintenance` | 9 steder | Use when updating, auditing, reorganizing, or generating CellProtocol documentation, Book chapters, machine-readable catalogs, agent entrypoints, rea… | 345 | ja | mtime:2026-09-29 |
| `cellprotocol-identity-capability-security` | 4 steder | Use when working on HAVEN/CellProtocol identity, domain-scoped identity, IdentityVaults, ownership proofs, agreements, conditions, capabilities/grant… | 335 |  | mtime:2026-09-29 |
| `cellprotocol-runtime-map` | user | Compact map of the CellProtocol architecture — its layer model, protocol invariants, source-of-truth model, and an index to the deep domain skills an… | 509 |  | mtime:2026-08-15 |
| `cellprotocol-scaffold-integration` | 4 steder | Use when integrating CellProtocol Cells, CellConfigurations, resolver wiring, runtime bootstrapping, diagnostics, Porthole, Binding, CellScaffold, pe… | 245 | ja | mtime:2026-10-07 |
| `cellprotocol-skeleton-renderer-porting` | 4 steder | Use when implementing, reviewing, or porting a CellProtocol Skeleton renderer or parser in SwiftUI, web, Kotlin Compose, Java UI, Rust UI, Go UI, or… | 386 | ja | mtime:2026-10-07 |
| `cellprotocol-transport-bridging` | 4 steder | Use when working on CellProtocol bridges, transport adapters, WebSocket/IPC/P2P/QUIC/WebRTC routing, cell:// endpoints, remote references, bridge pay… | 278 |  | mtime:2026-09-29 |
| `claim-drift-analysis` | 4 steder | Use when a text must be checked for whether it silently swapped the claim it was supposed to evaluate — reviewing articles, reports, expert opinions,… | 772 |  | mtime:2026-09-29 |
| `codex-collaboration` | 8 steder | Coordinate Claude and local Codex work through Codex MCP, `codex exec`, durable HAVEN handoffs, or explicitly requested swarm delegation. | 504 | ja | mtime:2026-09-29 |
| `diagnose` | user | Disciplined diagnosis loop for hard bugs, failures, and performance regressions — reproduce, minimize, localize, hypothesize, instrument, fix, then l… | 407 |  | mtime:2026-08-15 |
| `dimy-payment-regulatory-guardrails` | 8 steder | Use when a HAVEN/DiMy task involves credits, entitlements, prepaid value, wallet value, tokens, PSPs, Stripe, Vipps, MiCA, PSD2, e-money, AML/KYC, Fi… | 327 | ja | mtime:2026-09-29 |
| `dimy-value-redistribution` | 8 steder | Use when working on HAVEN/DiMy value redistribution, value-return pilots, ValuePoolPolicy, ContributionProof, MicropayoutPolicy, ProofDoor/AI entitle… | 383 | ja | mtime:2026-09-29 |
| `haven-assistant-correspondence` | 4 steder | Use when Claude lists, reads, sends, acknowledges, configures, or diagnoses HAVEN Assistant Correspondence. | 463 | ja | mtime:2026-10-06 |
| `haven-bounded-repository-analysis` | 4 steder | Run or review a bounded, token-disciplined, source-grounded repository audit of claims, arguments, premises, evidence, sources, provenance, contradic… | 407 |  | mtime:2026-09-29 |
| `haven-claim-review` | 8 steder | Use when reviewing or writing public claims about HAVEN, DiMy, CellProtocol, value redistribution, micropayments, trust/omdømme, commons, AI entitlem… | 322 | ja | mtime:2026-09-29 |
| `haven-copilot-onboarding-dialogue-authoring` | 7 steder | Use when designing, extending, or wiring a guided onboarding/setup dialogue that runs through Co-Pilot Chat's Personal Co-Pilot in HAVEN/CellProtocol… | 690 | ja | 2026-09-29 |
| `haven-copilot-onboarding-dialogue-authoring-workspace` | 7 steder |  | 0 |  |  |
| `haven-functional-service-verification` | 8 steder | Use when testing, verifying, debugging, or certifying whether a HAVEN/CellProtocol service, Porthole surface, CellConfiguration, demo story, action f… | 522 | ja | mtime:2026-09-29 |
| `haven-git-workflow` | 4 steder | Manage HAVEN Git, PRs, CI and coordinated package releases across repositories, preserving worktrees and linking verified source changes to Workbench… | 167 | ja | mtime:2026-10-07 |
| `haven-gui-testing` | 8 steder | Use when testing, debugging, or designing GUI verification for HAVEN surfaces across conference, DiMy, public presence, Porthole, Library-loaded Cell… | 412 | ja | mtime:2026-09-29 |
| `haven-learning-capture` | 4 steder | Use at the end of ANY HAVEN/CellProtocol/DiMy/Palazzo session that edited files or ran commands, and whenever a thread discovers something reusable f… | 848 |  | mtime:2026-09-29 |
| `haven-local-dev-environment-setup` | 7 steder | Use when setting up, restarting, or troubleshooting a local CellScaffold dev environment for design/interaction testing — building and running the lo… | 475 | ja | 2026-09-29 |
| `haven-panel-task-decomposition` | 5 steder | Use when giving the HAVEN AI advisory panel (rådgiverpanelet) a task, or when any nontrivial HAVEN/DiMy task needs purpose+goal grounding and claim/a… | 772 | ja | mtime:2026-09-29 |
| `haven-prompt-purpose-testing` | 8 steder | Use when testing or extending Co-Pilot Chat prompt routing, Purpose/Interest matching, GroundedActionPlan verification, prompt matrices, provider com… | 251 | ja | mtime:2026-09-29 |
| `haven-purpose-driven-dev` | cpdocs | Use for ANY development task in HAVEN/CellProtocol/Binding/Palazzo — code, CellConfiguration/skeleton, or cell combinations — when Kjetil states some… | 852 |  | 2026-10-14 |
| `haven-purpose-tree-review` | scaffold, ws-vegar-arendalsuka | Build a clickable purpose tree (formålstre) for a HAVEN PDD so the owner can read every purpose's goal in a popup, comment per purpose and approve th… | 592 | ja | 2026-10-09 |
| `haven-work-intake` | 4 steder | Capture and triage HAVEN ideas, bugs, features and project work; preserve owner-scoped Workbench records, provenance and evidence through agent execu… | 180 |  | mtime:2026-09-29 |
| `haven-xcode-workspace-recovery` | 8 steder | Use when Xcode reports missing CellProtocol package products or modules such as CellBase, CellApple, CellVapor, or CodableHelpers, or says CellProtoc… | 272 | ja | mtime:2026-09-29 |
| `kallimachos-dialogue-testing` | 4 steder | Design, run, inspect, and report source-grounded Kallimachos dialogue tests through CommonsLibrarian, AIGateway, and a local model. | 405 |  | mtime:2026-09-29 |
| `omnigraffle-illustrations` | 7 steder | Create, inspect, modify, and reason about OmniGraffle illustration files (.graffle), stencils (.gstencil), and templates (.gtemplate). | 389 | ja | 2026-09-29 |
| `personal-data-trust-package` | 8 steder | Use when an assistant, agent cluster, Codex or Claude finds, proposes, retrieves, transforms, stores, exports, discloses or submits data about the us… | 387 |  | mtime:2026-09-29 |
| `public-presence-cell-authoring` | 8 steder | Use when designing, creating, editing, reviewing, or publishing HAVEN/CellProtocol public presence cells: personal profile pages, public profile vari… | 391 |  | mtime:2026-09-29 |
| `write-a-skill` | scaffold, ws-vegar-arendalsuka, ws-vegar-personal-log | Create or update a Claude Code skill for the CellScaffold / HAVEN project. | 326 |  | 2026-09-09 |
| `zoom-out` | user | Explain an unfamiliar piece of code in the context of the whole system — its responsibility, where it sits, what depends on it, and which contract or… | 432 |  | mtime:2026-08-15 |

## Avvik mellom kopier

- `binding-skeleton-parity-testing`: 397144d0b3 = user · 3b790afcab = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands · f8aa77f800 = scaffold, ws-vegar-arendalsuka, ws-vegar-personal-log
- `cellconfiguration-skeleton-authoring`: 8c3e0b1c2c = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands · c008df0d03 = scaffold, user, ws-vegar-arendalsuka, ws-vegar-personal-log
- `cellprotocol-cell-authoring`: 658e6f3845 = user, ws-vegar-personal-log · 96c3fc1dae = scaffold, ws-vegar-arendalsuka
- `cellprotocol-docs-and-rag-maintenance`: 02cb24b67a = cpdocs · 323d1c8f37 = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands · b19fb136bb = scaffold, user, ws-vegar-arendalsuka, ws-vegar-personal-log
- `cellprotocol-scaffold-integration`: 1a9f6a819c = user · 66929e2cb6 = scaffold, ws-vegar-arendalsuka, ws-vegar-personal-log
- `cellprotocol-skeleton-renderer-porting`: b845de5edb = scaffold, ws-vegar-arendalsuka, ws-vegar-personal-log · d73b9b92b7 = user
- `codex-collaboration`: 3fa5461266 = scaffold, user, ws-vegar-arendalsuka, ws-vegar-personal-log · 5f3447cfaa = ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands · b8aff8ec55 = ws-vegar-chat
- `dimy-payment-regulatory-guardrails`: 539596e8d3 = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands · f343b9c526 = scaffold, user, ws-vegar-arendalsuka, ws-vegar-personal-log
- `dimy-value-redistribution`: 12de58fdd6 = scaffold, user, ws-vegar-arendalsuka, ws-vegar-personal-log · cf450128e9 = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands
- `haven-assistant-correspondence`: 0451b05089 = ws-vegar-arendalsuka, ws-vegar-personal-log · c6639f50b2 = scaffold, user
- `haven-claim-review`: 2490de6fcc = scaffold, user, ws-vegar-arendalsuka, ws-vegar-personal-log · 44624e6870 = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands
- `haven-copilot-onboarding-dialogue-authoring`: 36aa1855e8 = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands · ecd3a13269 = scaffold, ws-vegar-arendalsuka, ws-vegar-personal-log
- `haven-functional-service-verification`: 1189588dae = scaffold, ws-vegar-arendalsuka · 67354c156b = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands · a4565202d3 = user, ws-vegar-personal-log
- `haven-git-workflow`: 200b5b3c9e = user · 6ad9e632a2 = scaffold, ws-vegar-arendalsuka, ws-vegar-personal-log
- `haven-gui-testing`: 48b39edbae = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands · 756308be58 = scaffold, ws-vegar-arendalsuka · 9332f4d134 = user, ws-vegar-personal-log
- `haven-local-dev-environment-setup`: 78ef998efb = scaffold, ws-vegar-arendalsuka, ws-vegar-personal-log · 98ee1bc4b5 = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands
- `haven-panel-task-decomposition`: 601bb87380 = scaffold, user, ws-vegar-arendalsuka, ws-vegar-personal-log · ea011c6133 = cpdocs
- `haven-prompt-purpose-testing`: bd9031b2fe = scaffold, user, ws-vegar-arendalsuka, ws-vegar-personal-log · db075acc1b = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands
- `haven-purpose-tree-review`: 3b6636c3e5 = scaffold · 40ce639593 = ws-vegar-arendalsuka
- `haven-xcode-workspace-recovery`: 99d65a4312 = scaffold, user, ws-vegar-arendalsuka, ws-vegar-personal-log · b506a2d288 = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands
- `omnigraffle-illustrations`: 27b94a33e9 = ws-vegar-chat, ws-vegar-matching-design, ws-vegar-medvirkende, ws-vegar-stands · c5f9a41e47 = scaffold, ws-vegar-arendalsuka, ws-vegar-personal-log

## Mulig overlapp (heuristikk på ord i beskrivelsene, ikke dom)

- `cellprotocol-cross-language-porting` ↔ `cellprotocol-skeleton-renderer-porting` (0.27): another, authoring, cellconfiguration, cellprotocol, covers, golden
- `cellprotocol-contract-testing` ↔ `cellprotocol-cross-language-porting` (0.19): cellprotocol, determinism, fixtures, golden, parity, policy
- `cellprotocol-cell-authoring` ↔ `public-presence-cell-authoring` (0.15): cellprotocol, cells, creating, editing, existing, haven
- `dimy-value-redistribution` ↔ `haven-claim-review` (0.15): cellprotocol, commons, dimy, entitlement, grants, haven
- `cellprotocol-contract-testing` ↔ `cellprotocol-skeleton-renderer-porting` (0.14): cellprotocol, decode, golden, parity, reviewing, skeleton
- `haven-copilot-onboarding-dialogue-authoring` ↔ `haven-prompt-purpose-testing` (0.13): cellprotocol, chat, co-pilot, extending, groundedactionplan, haven
- `haven-git-workflow` ↔ `haven-work-intake` (0.13): evidence, haven, release, workbench

## Problemer

- `haven-copilot-onboarding-dialogue-authoring-workspace`: mangler SKILL.md (scaffold); mangler SKILL.md (ws-vegar-arendalsuka); mangler SKILL.md (ws-vegar-chat); mangler SKILL.md (ws-vegar-matching-design); mangler SKILL.md (ws-vegar-medvirkende); mangler SKILL.md (ws-vegar-personal-log); mangler SKILL.md (ws-vegar-stands)
- `arendalsuka-data-pipeline`: 6 hardkodede /Users/…-stier
- `binding-skeleton-parity-testing`: 9 hardkodede /Users/…-stier
- `cellconfiguration-skeleton-authoring`: 8 hardkodede /Users/…-stier
- `cellprotocol-docs-and-rag-maintenance`: 12 hardkodede /Users/…-stier
- `codex-collaboration`: 10 hardkodede /Users/…-stier
- `dimy-payment-regulatory-guardrails`: 1 hardkodede /Users/…-stier
- `dimy-value-redistribution`: 9 hardkodede /Users/…-stier
- `haven-claim-review`: 2 hardkodede /Users/…-stier
- `haven-local-dev-environment-setup`: 3 hardkodede /Users/…-stier
- `haven-prompt-purpose-testing`: 5 hardkodede /Users/…-stier
- `haven-xcode-workspace-recovery`: 9 hardkodede /Users/…-stier
- `omnigraffle-illustrations`: 3 hardkodede /Users/…-stier
- `write-a-skill`: 3 hardkodede /Users/…-stier
