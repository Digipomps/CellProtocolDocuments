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

Kjøring 2 (full klon med submoduler, samme commits): de 13 eksportfeilene består. Igjen står 27 feil i CellScaffold og 4 i Binding, ingen ustabile (alle feiler også alene).

- CellScaffold (27): 402 i stedet for 200 (PaymentProofDoor), 500/503 fra Arendalsuka-rutene, 200 i stedet for 303 (sidetilgang), `persistedIdentityUnavailable`, `registerAtAlreadyTakenEndpoint`, AI-svermen gir 2 runder i stedet for 3.
- Binding (4): to provenance-tester får ikke kjøre `xcrun` i sandkassen, NearbyScanner får ikke skrive til /tmp (trolig samme sandkasse), og én test mot haven.digipomps.org avvises ved signContract for «Arendalsuka Participant Program».

Regel for resten av PDD-en: en **ny** feil er en feil som ikke står på disse to listene (27 + 4). Logger: `/Users/kjetil/Build/Digipomps/HAVEN/MasterHAVEN26/pdd-forskningsdata-2026-11-17/evidence/wp0/run2/`.

Staging-måling av `AdminResolverStats`, `AdminCellLifecycle`, `AdminMetricsHistory`: venter på observer-rollen.
