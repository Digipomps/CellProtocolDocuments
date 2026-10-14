# Prosjektflate: CS17 R1 — klargjort, ikke godkjent eller kjørt

Formål: fullføre de 17 Workbench-journaltestene etter lokal pakkeidentitetsfeil,
uten å gjenta grønn baseline116 eller CellProtocol8. Ingen CI, push eller deploy.

## Resultater som er bevart

- `PROJECT-WORKSPACE-BASELINE-R1-20261013`:116/116 passed; avsluttet2026-10-13T21:40:13Z.
- `G2-W1-CONTINUE-20261013`:CP8/8 passed. CS stoppet22:12:47Z før én eneste test.
- Feil: DiMyMicropayments bruker `.package(path: localPath)` men targetproduktet
  navngir pakken `CellProtocol`. Den gamle kandidatens mappenavn ga identiteten
  `codex-workbench-entity-journal-20261012`, bekreftet i råloggen.
- Begge gamle pakker og alle gamle kvitteringer beholdes uendret. Pins er gjenopprettet.

## Konkret rettelse

En ny ekte, detached Git-worktree ligger i
`_worktrees/workbench-entity-cs17-20261014/CellProtocol` relativt til HAVEN-roten.
HEAD er samme b4100f5734bb0b3781600845a267e424e55c0989. Alle968 tracked/ikke-ignorerte
kildefiler, symlinkmål og executable-bits er sammenlignet med den testede kandidaten.
Originaltreet bevares. Ingen manifest-, produkt- eller testkilde er endret.
SwiftPM-resolusjon med den nye katalogen er ennå ikke kjørt, så rettelsen er
klargjort og statisk begrunnet, ikke erklært runtime-verifisert.

`run.py` endrer kun kandidatstien, binder de gamle grønne kvitteringene og det
komplette CP-kildeinventaret, og kjører CS17 alene. `driver.diff` viser endringen.
Eksakt kilde-/test-/skriptmanifest: `102f027723dee2aab2fb2bd639978c4c8db39094bdf8d1be203d08a1e36157d5`.

## Kontrollert før ny godkjenning

`PRECHECK.json` og de fire check/run-loggene viser Python/Bash-syntaks,
read-only check og avvist run uten godkjenning, både uten locale og med UTF-8.
Dette kjørte ingen Swift og opprettet ingen attempt-started eller ADMISSION.
Prosess-/kvitteringshjelperne er byteidentiske med forrige reviderte pakke;
deres tester er ikke kjørt om igjen som del av denne klargjøringen.

## Nøyaktig forespurt omfang

Kjetils nye ja gjelder én lokal kjøring av de samme17 testene i manifestet,
med samme CS-kilde9ff06f8446b6331da49272f5fd72b947b4092ece og CP-kildekopien over.
Ingen baseline-/CP8-omkjøring og ingen endring i committed tester.
AUTHORIZATION.json er false; ingen ADMISSION finnes. Bare køeieren
«Deploy prosjekt køadministrasjon» kan aktivere etter at et nytt ja er bundet
til dette manifestet og ferskt eksklusivt vindu er kontrollert. 2Swift-jobber,
administrert cache,40GiB OG5prosent etter10GiB reserve. Ingen manuell cache-sletting.
Rødt stopper og bevares; ingen automatisk retry. Grønt avstemmes med tidligere116+8,
deretter fortsetter allerede G2-godkjent prosjektflate i prosjektarbeidstreet.

Butler-kravet følger prosjektarbeidet: alle flater skal kunne hente Butler,
gjerne innebygd, med aktivt prosjekt/objekt og eksisterende tilgangsgrenser.
Dette er et krav, ikke en påstand om levert funksjonalitet.

Testpakke: `HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-CS17-R1-20261014/`.
