# PLAN — Porthole laster flater fra eksternt scaffold

G1 godkjent 2026-09-14; G2 auto samme dag. Arbeidspakker 1:1 mot bladformål i FORMAALSSPEC §1.
Stier er relative til repoet (`Repo::sti`); køjobben kjører med cwd = HAVEN-rot, så `CellScaffold/…` og `PalazzoScaffold/…` virker direkte.

| WP | Bladformål | Utfører | Test | Hva det innebærer | Status |
|---|---|---|---|---|---|
| WP0 | baseline | Codex | test.build, test.regression | Bygg CellScaffold via isolert runner; kjør den avgrensede testfilteret FØR endring; noter tall som «forventet ≈ N». Arbeidstreet er skittent (B3-filene ucommittet) — det er en planopplysning, ikke noe å jobbe rundt: baselinen måles på treet slik det er, og filene listes i TESTRESULT.md#baseline | venter |
| WP1 | remote-lookup (oppslag) | Codex | test.trust-boundary | `CellScaffold::Sources/App/Controllers/PortholeWebPayloads.swift`: `CellConfigurationLookup` får valgfritt `keypath`; `decodeLookupObject` leser det | venter |
| WP2 | remote-lookup (henting) | Codex | test.remote-lookup | `CellScaffold::Sources/App/Controllers/PortholeWebSessionSupport.swift` `resolveRequestedCellConfiguration`: når `sourceCellEndpoint` har vert:port og verten er bridgehead-godkjent, hent cellen via resolveren (`registerRemoteHosts` er alt gjort i configure), `get(keypath:)`, dekod `CellConfiguration`, kjør omskriving (WP3), returner. Uten keypath eller ukjent vert: 400 med grunn, ingen nettverkskall | venter |
| WP3 | reference-rewrite + published-allowlist | Codex | test.reference-rewrite, test.allowlist | Ren funksjon som skriver om `cell:///X` → `cell://host:port/X` i `discovery.sourceCellEndpoint` og `cellReferences[].endpoint`; `ConfigurationCatalogCell.isPortholePublishedConfiguration` godtar fjern vert:port fra `RemoteBridgeheadAccess` (eksponer et lite `isRemoteHostAllowed(host:port:)` i ScaffoldKit, ikke en ny env) | venter |
| WP4 | preview-tool | Codex | test.preview-tool | `CellScaffold::scripts/skeleton-iterate.js`: `--configurationKeypath` (og scenario-felt `configurationKeypath`) sendes i `configurationLookup`; `PalazzoScaffold::docs/sicilia-gui-evidence/run-g5.sh` og `g5-*-preview.log`-argumentene får keypath per flate (`guest.configuration`, `guest.article.configuration` med artikkelbinding slik eksporten gjorde det, `content.configuration` for huset) | venter |
| WP5 | quality.* | Codex | test.build, test.regression, test.docs-updated, test.status-current | Avsnitt i `CellScaffold::Documentation/Skeleton_Runtime_Iteration_Workflow.md`; TESTRESULT.md med alle ankre; filliste med SHA-256; rapport «skrevet, verifisert med avgrenset test» — aldri «levert» | venter |
| WP6 | root (test.g5) | **Kjetil** | test.g5 | `bash <PalazzoScaffold::docs/sicilia-gui-evidence/run-g5.sh>`; siste linje `G5 DONE`; Losen leser loggen og skriver ACCEPT.md#parity side om side med images/ | venter |
| WP7 | commit-pakke | Codex (egen køjobb, git) | `git rev-parse` ≠ base | Etter første grønne bygg: commit i CellScaffold (inkl. B3-filene) og PalazzoScaffold på egne grener — `lesson.branch-is-empty-after-eight-work-packages` | venter |

## Hva Kjetil selv skal gjøre
1. Ingenting før Codex-jobben er ferdig (`_losen-queue/done/pz1-porthole-fjernt-scaffold-20260914.svar.md`).
2. Så: kjør `run-g5.sh` én gang (WP6). Feiler den, si fra — loggen ligger i en mappe Losen leser.
3. Si G3 når ACCEPT.md viser bildene side om side og du er enig.

## Rekkefølge og risiko
WP1→WP2→WP3 er én sammenhengende Swift-endring; WP4 er JS+bash; WP5 samler. Største risiko: CellScaffold-bygget i kø-sandkassen (`lesson.codex-workspace-write-cannot-build-cellscaffold`). Mønsteret fra G7 (isolert runner + filter) virket 2026-09-08 for 18 tester og er det som skal brukes. Feiler byggingen i sandkassen, leverer jobben koden som «skrevet, ikke verifisert» pluss `KJOR-SELV-build.sh` som Kjetil kjører.
