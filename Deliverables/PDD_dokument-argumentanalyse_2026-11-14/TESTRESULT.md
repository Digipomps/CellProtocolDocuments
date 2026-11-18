# TESTRESULT – dokument- og argumentanalyse

Faktiske kjøringer. Ingenting her er meldt levert før bygget det gjelder er grønt.

## #graf (WP1, WP2)

- **CellBase `ArgumentMapVisualizationTests`**: 6/6 grønne, 2026-11-18, Docker `swift:6.1-noble`, rigg som avhenger av CellProtocol-grenen `claude/argumentmap-visualization` (b133369) gjennom produktet CellBase. Felles layoutvektorer: `Tests/CellBaseTests/Fixtures/ArgumentMapLayoutVectors.v1.json` (mobilforbud, syklus, uten kanter, hengende/selv-kanter fjernes, barysenter-rekkefølge).
- **Web `playwright/argumentmap-visualization.spec.js`**: 4/4 grønne, 2026-11-18, Chromium, CellScaffold-grenen `claude/tekstanalyse` (6a6acba). Samme vektorfil som CellBase, så web og Swift plasserer hver påstand i samme rad og posisjon.
- **CellApple-renderer (WP3)**: skrevet, ikke bygget. Venter på Mac-kjøring.

## #paritet (WP4, T-PARITET, T-SITAT, T-KILDE)

- **`TextReliabilityAnalyzerParityTests`**: 5/5 grønne, 2026-11-18, Docker `swift:6.1-noble`. Fire fixtures (markdown_struktur, mobilforbud, add2entity_capture, project_description) gir sortert JSON lik Python-verktøyet for seksjoner, påstander, kildereferanser, retorikk og argument_map.
- **Rødsjekk**: ett felt endret i en golden-fil gjorde testen rød som forventet; filen er satt tilbake.
- Ikke portert (bevisst): klynger, matrise, graf, produktivitet og pålitelighetsdimensjoner. Rommet bruker argumentkartet i stedet for den gamle grafen.
