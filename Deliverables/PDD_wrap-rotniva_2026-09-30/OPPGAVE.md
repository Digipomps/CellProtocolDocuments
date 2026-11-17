# Oppgave: wrap-liste på rotnivå i native (ikke startet)

Status: **venter**. Kjetil 2026-09-30: «Egen oppgave senere». Ingen formålsdekomponering er gjort, og ingen G1.

## Det som er observert

- Gjelder en `List` med `wrap: true` som er rotelement i en flate, eller som av andre grunner går gjennom `ScrollView`-veien i CellListView fordi dataene ikke er rad-relative.
- Når bredden bare så vidt holder til brikkene, havner hver brikke på egen linje. Inne i en rad eller en `VStack` pakkes de riktig.
- Diagnosekjøringer 29.9 (`HAVEN-Deploy/_handoff/PALAZZO-VEKT/diag2-*`, `diag3-*`): FlowLayout får midlertidig forslag og grenser med bredde 0 fra ScrollView-veien, både på `origin/main` 81601a6 og med WP1a. Avviket fantes altså før WP1a.
- Årsaken er ikke funnet.
- Kan ramme brikkelister som leser cellestatus: Arendalsukas `interestRows` og Butlers `scopeChips` og `branchChips`. Det er ikke sett i kjørende app.
- Dokumentert som kjent avvik i `CellProtocol/Documentation/Skeleton_List_Tree.md` (commit 253b4af). `testWrappedListItemsTakeTheirOwnWidth` tester bare det nestede tilfellet.

## Neste steg, når Kjetil vil

Start med PDD-P0 og P1: formålet (hvem ser brikkelisten, og hva skal de kunne), og om det må vises i kjørende app før noe rettes.
