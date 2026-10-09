# STATUS — workbench ai helper

- surfaces: cell, gui, porthole, skeleton, web
- tags: ai, chat, gui, workbench

## Porter
- G1: godkjent 2026-10-09 (Kjetil i tråden «Formålstre i Developer Workbench», 13:44Z: «G1 Godkjent»)
- G1-GUI: godkjent 2026-10-09 (Kjetil i tråden, 13:53Z: «G1-GUI på de fire bildene er godkjent.»)
- G2: godkjent 2026-10-09 (Kjetil i tråden, 14:01Z: «Planen er godkjent - utfør nå.»)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
- 2026-10-09: WP8 (B2, ny flate fra beskrivelse) og WP10 (F3 ved lagring av flate) flyttet til fase 2. Porthole-editoren har ingen cellehandling for forhåndsvisning og lagring (`PortholeWebSessionSupport.swift:5929`, `:6106`), og planen sa at B2 flyttes hvis den ikke går i fase 1.
- 2026-10-09: WP6 markerer ikke elementene i listen slik `hjelperpanel-fylt-v1.png` viser. `WorkItem select` velger bare ett element (`WorkItemCell.swift:1544`), så panelet lister dem i stedet. Avvik for G3.
- 2026-10-09: Modellbanen bruker AIGateway `ai.invoke` med en tekst-prompt og JSON-svar som cellen sjekker, ikke `grounding.analyze`. Grounding-motoren ruter til konfigurasjoner og hjelpere, ikke til en handling med argumenter som `setStatus` for mange elementer.

## Logg
- 2026-10-09: opprettet
- 2026-10-09: iterasjon 1 av FORMAALSSPEC og formålsside publisert (https://claude.ai/artifact/9uUQtFQmi5wpGbgabyTJj1). Godkjenning lagres i sidens `gates` (bare eieren skriver) og varsler økten `session_01J3x24PaQowsSj3iKTi8UWK`. Ingen kode.
- 2026-10-09: G1 godkjent av Kjetil 13:44Z (melding i tråden, ikke via formålssiden; `gates` på siden er tom). Spørsmålene i §6 ble ikke besvart, så standardsvarene gjelder (se FORMAALSSPEC §6).
- 2026-10-09: fase 1 etter G1: fire bilder til G1-GUI i `images/` med renderingserklæring, kontrakt for instruksjonssett i `contract/`.
- 2026-10-09: G1-GUI godkjent 13:53Z for de fire bildene. PLAN.md og dataflow.md skrevet til G2.
- 2026-10-09: G2 godkjent 14:01Z. Fase 1 startet. CellScaffold PR #305 (draft) med WorkbenchHelperCell, panel og fanen hjelper. Book 23: `purpose://candidate.butler.always-reachable` lagt inn som eget formål (status candidate).
