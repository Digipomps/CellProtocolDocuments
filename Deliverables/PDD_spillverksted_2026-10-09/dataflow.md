# Dataflyt: spillverksted, runde 1

```
Barn (Porthole) --ønske--> Arbeidsbenk-assistent --library.lookup--> GameToolLibraryCell
                                    |                                     (game-tool-library.v1.json, lese-only)
                                    v
                           GameProjectCell --project.propose--> pending
                                    |  project.applyProposal / revert / discard
                                    v
                           versions[] (persistent)  --project.preview--> /spill/sandbox/<id>/<versjon>
                                    |                                            |
                                    v                                            v
                  ProjectPortfolio + 2 WorkItems (capture)        iframe sandbox="allow-scripts", CSP, KAPLAY vendret
```

| Fra | Til | Hva | Tilgang | Test |
|---|---|---|---|---|
| Porthole | GameToolLibraryCell `library.lookup` | `purposeRef` og/eller tekst | `rw--` (spørring, lagrer ikke) | GameToolLibraryCellTests, T-C2 |
| Porthole | GameProjectCell `project.*` | opprett, foreslå, ta i bruk, forkast, rull tilbake, velg | `rw--`, bare eier | GameProjectCellTests |
| GameProjectCell | ProjectPortfolio `capture`, WorkItem `capture` ×2 | prosjekt og to barnelesbare oppgaver | eierens identitet | testCreateLinksCanonicalPortfolioAndTwoWorkItems |
| GameProjectCell | `/spill/sandbox/...` | koden som tekst, aldri kjørt i cellen | `r---` på `project.preview.<id>` | GameSandboxTests, testSandboxRejectsForeignRequester… |
| Sandkasse-ruten | nettleserens iframe | HTML med koden som JSON-streng | CSP `sandbox allow-scripts`, ingen cookies, ingen nettverk | GameSandboxTests, playwright/game-sandbox.spec.js |
