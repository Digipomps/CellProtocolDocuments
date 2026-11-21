# Testresultat — Studentflater og skeletonhjelp

## local-check (WP2) — 2026-11-21

Kjørt: CellBase-port på Linux, Docker `swift:6.1-noble`, grenen
`claude/skeleton-check-20261121` (CellProtocol PR #105).

| Test | Resultat |
|---|---|
| `SkeletonConfigurationCheckTests` (10) | grønn |
| `SkeletonReachabilityAuditTests` (24) | grønn |
| `test.local-check.cli`: `skeleton-check` på 31 eksisterende konfigurasjoner | ingen falske «ukjent element»-funn |
| Guide-eksempelet `skeleton/utkast-gjoremal.cellconfiguration.json` med `--require todo.toggleTodo` | OK, handlingen nås |

Funnet underveis: dekoderen kan miste navnet på et ukjent element
(`Markdown` rapporteres som `text`). Sjekken leser derfor navnet fra rå-filen.

Sjekken rapporterer rot-scopede synlighetsbetingelser i 7 eksisterende filer
i CellScaffold (bl.a. `Public/skeletons/butterpop/*`, `kunstnerportefolje/*`,
`ConferenceDemoDashboard/journey`). Reelle funn, ikke rettet her.

Ikke verifisert: full pakke med CellApple på macOS.
