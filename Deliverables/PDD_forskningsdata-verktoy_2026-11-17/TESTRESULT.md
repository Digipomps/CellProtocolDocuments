# TESTRESULT — forskningsdata for studentene

## baseline

WP0, 2026-11-18/19. Ren eksport av `origin/main` (Swift på Macen, Py/Go i skycontaineren). Full rapport: `/Users/kjetil/Build/Digipomps/HAVEN/MasterHAVEN26/pdd-forskningsdata-2026-11-17/evidence/wp0/BASELINE.md`.

| Repo | Commit | Resultat |
|---|---|---|
| CellProtocol | b9e7576 | grønn: bygg ok, 1925 tester, 0 feil, 6 hoppet over |
| CellScaffold | 6a345d1a (CellProtocol-pin b440462) | rød: 40 av 3677 feil, 23 hoppet over. 13 skyldes eksporten (`git archive` mangler CellProtocolDocuments-submodulen; én paritetstest forventer `.build/checkouts`). 27 ikke klassifisert (mest Conference, PaymentProofDoor, AIAssistantThread) |
| Binding | 3262ef760, BindingTests | rød: arkiv-eksport bygger ikke (byggeskript kjører `git ls-files`); fra lokal klon 193 XCTest (2 feil, 25 hoppet over) og 546 Swift Testing (2 feil) |
| PyCellProtocol | b874d65 | grønn: 265 bestått |
| GoCellProtocol | 9ea5cc9 | grønn: 86 bestått, 0 feil |

Neste: kjør CellScaffold og Binding på nytt fra full klon med submoduler, så de 27 kan skilles fra eksportfeil før baselinen brukes som referanse.

Staging-måling av `AdminResolverStats`, `AdminCellLifecycle`, `AdminMetricsHistory`: venter på observer-rollen.
