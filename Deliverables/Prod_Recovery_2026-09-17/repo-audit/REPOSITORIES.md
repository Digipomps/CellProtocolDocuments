# All non-CellScaffold repository snapshot

Measured 2026-09-17T21:04:27.947578+00:00. Read-only Git metadata and source comparison; not build or production acceptance.

| Repository | Snapshot base | Local refs | Remote refs | Worktrees | Dirty primary paths | Stashes |
|---|---|---:|---:|---:|---:|---:|
| Binding | `origin/main 285dc235c0` | 60 | 56 | 12 | 41531 | 4 |
| CellProtocol | `origin/main 36372c5b95` | 63 | 38 | 18 | 35 | 0 |
| CellProtocolDocuments | `origin/main 357f2cfa0b` | 31 | 32 | 8 | 752 | 1 |
| CellUtility | `origin/main cae2cadd94` | 2 | 2 | 1 | 0 | 0 |
| DiMy Source Editor Extension | `origin/main fecf9746c7` | 1 | 2 | 1 | 0 | 0 |
| DiMyDevRAG | `origin/main 2d6e3addff` | 1 | 2 | 1 | 0 | 0 |
| DiMyDocuments | `origin/main 4c28a68de1` | 4 | 4 | 1 | 1 | 0 |
| DiMyMicropayments | `origin/main c3544c2f7b` | 12 | 11 | 6 | 33 | 0 |
| DiMyMint | `origin/main 25b679bafc` | 12 | 14 | 5 | 4 | 0 |
| GoCellProtocol | `origin/main 2f717dce31` | 3 | 2 | 1 | 0 | 0 |
| HAVEN-Deploy | `main d62d297ae9` | 1 | 0 | 1 | 635 | 0 |
| HAVEN_MVP | `origin/main 5dc692fc5e` | 1 | 2 | 1 | 0 | 0 |
| HavenAgentD | `origin/main 551d37a4df` | 17 | 16 | 7 | 107 | 0 |
| PalazzoScaffold | `origin/main 6a3acf5473` | 2 | 2 | 1 | 0 | 0 |
| PyCellProtocol | `origin/main 5a6e19f486` | 2 | 2 | 1 | 0 | 0 |
| PyPalazzoConciergeScaffold | `origin/main 0e58cdea5d` | 2 | 3 | 1 | 34 | 0 |
| RustCellProtocol | `origin/main 2bbdfe6a25` | 4 | 2 | 1 | 0 | 0 |
| SpatialRegistryScaffold | `origin/main 466eab6e39` | 2 | 3 | 1 | 0 | 0 |
| SwiftWebScaffold | `origin/main 89f6681ca0` | 2 | 2 | 1 | 0 | 0 |
| UniverseSimulation | `origin/master 2151655eaf` | 4 | 3 | 1 | 731 | 0 |
| WatchPong | `origin/main e57e6c0151` | 1 | 2 | 1 | 0 | 0 |
| sprout | `origin/main 473d6998bf` | 5 | 3 | 2 | 52 | 0 |

## Every local and remote branch

See `branches.tsv` for the full branch table and `inventory-enriched.json` for exact commit lists, patch-equivalence output, changed paths, worktree status and merge-base evidence. Every branch is retained; no branch has been discarded based on date or PR availability.

## Assessment meanings

- `ANCESTRY_IN_MAIN`: branch tip is already reachable from measured main.
- `PATCH_EQUIVALENT_IN_MAIN`: all branch-only non-merge patches match history on main; this is history evidence, not proof against a later revert.
- `CHANGED_PATHS_IDENTICAL_TO_MAIN`: with a proven common ancestor, all branch-changed path contents match current main.
- `POSSIBLE_SQUASH_OR_PARTIAL_IN_MAIN`: matching subjects and/or partial byte equality; needs semantic reconciliation.
- `UNIQUE_OR_REBASED_REQUIRES_REVIEW`: remaining differences; not proof every line must be restored.
- `DIVERGENT_HISTORY_REQUIRES_REVIEW`: no common ancestor; triple-dot comparison is unavailable. Never interpreted as empty or already integrated.
- `ARCHIVE_REQUIRES_CONTENT_TRIAGE`: archive content retained and inventoried; name is not a rejection reason.

## Freshness and scope

Root reported fetching CellProtocol, Binding, DiMyMicropayments, DiMyMint and HavenAgentD during this audit; their refreshed remote refs are included. Remaining remote refs are potentially stale. Sprout was specifically found missing the object for the pin used by current HavenAgentD/main. Root is integrating concurrently; refs/worktrees created after this snapshot are outside this report. CellScaffold and its worktrees belong to another audit slice. Ignored files were not exhaustively scanned; Git status inventories tracked/untracked nonignored paths. Credential contents and real user runtime data were not inspected.
