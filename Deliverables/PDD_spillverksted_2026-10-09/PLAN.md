# PLAN — spillverksted

Plan til G2 for `PDD_spillverksted_2026-10-09`. Skrevet 2026-10-09 etter at G1 (08:56Z) og G1-GUI (spillflatene 09:59Z, verktøyflaten 14:05Z) ble godkjent.

Én arbeidspakke per bladformål i FORMAALSSPEC §1, i rekkefølgen de avhenger av hverandre. Hver pakke sier hvem som gjør den, hvilken test fra §5 som må bli grønn, og hva som havner i §3.

- **Utførere.** «Codex» er Swift i CellScaffold, bygget med `scripts/run_swift_bounded.sh`. «Claude» er JS, Python, skjeletter, dokumentasjon og målinger. «Xcode» er sjekk med `scripts/xcode-check.sh`. «Kjetil» er det bare Kjetil kan gjøre.
- **Kodegrunnlag.** CellScaffold `origin/main` `9a0e8c2`. Filreferanser under er lest derfra 2026-10-09.

## Tre beslutninger som trengs ved G2

1. **Forhåndsvisning i Porthole trenger et nytt skjelettelement.**
   - Skjelett-rendreren (`Public/js/skeleton-runtime.js`) har ingen iframe eller sandkasse. `renderVisualization` på linje 2602 har bare `map`, `chart`, `timeline`/`gantt` og lignende.
   - Forslag: en ny `Visualization`-type `gamePreview` som viser spillet i en iframe med `sandbox="allow-scripts"`, fra en egen rute.
   - Skjelettformatet utvides ikke uten ditt ja. Binding (SwiftUI) får ikke `gamePreview` i denne planen.
2. **Nye formål i Book 23.**
   - Bibliotek v0 bruker 14 kandidatformål `purpose://candidate.game.*` (`contract/game-tool-library.v0.json`). I tillegg kommer de 27 bladene i treet.
   - Forslag: de legges fram som `proposals/*` i Formålstrær, og bare de du godkjenner tas inn.
3. **Hjelperen blir lastet fra en profil i stedet for kode.**
   - I dag er hjelperne en fast `switch` på `helperRoute.keypath` (`PersonalCopilotCloudStore.swift`, rundt linje 5080 i `8861090`).
   - WP-B5 legger til et register for profiler ved siden av denne switchen. De eksisterende hjelperne flyttes ikke.

## Allerede gjort i fase 1

| Formål | Status | Bevis |
|---|---|---|
| D1 motorvalg | grønn | `TESTRESULT.md#motor`: 10 av 10 spill kjører, KAPLAY 342 mot Phaser 515 linjer |
| C4 åpne lisenser | delvis | Lisens og kilde finnes for alle 20 oppføringer i bibliotek v0. Kenney-pakkene er ikke lastet ned og kontrollert. |
| A2 forklaring | delvis | Prototypen viser hvorfor og markerer nye linjer. T-A2 med ti ekte forslag er ikke kjørt. |
| B2 forhåndsvisning | delvis | Prototypen kjører forslaget før det lagres. Tiden er ikke målt (T-B2). |
| H1 eget område | grønn | `Documentation/Arbeidsbenkassistent/`, `Documentation/Spillverksted/` med fil:linje |

## Fase 0: før koding (avhengigheter som må måles først)

| WP | Formål | Utfører | Hva | Test |
|---|---|---|---|---|
| WP-0a | (avhengighet) | Kjetil, så Claude | Åpne prototypen i Claude og be om én endring. Det viser om KAPLAY lastes fra jsDelivr inne i sandkassen og om Claude-kallet virker. | §2-rad «prototype i Claude-visning», notert i TESTRESULT.md#prototype |
| WP-0b | (avhengighet) | Claude | Mål hva Porthole gjør i dag med en `Visualization` av ukjent type, og om et skjelett kan lastes uten rekompilering (`editor.working.setSkeleton`, `PortholeWebSessionSupport.swift`) | TESTRESULT.md#porthole-grunnlag |
| WP-0c | (beslutning 2) | Claude, så Kjetil | Legg de 14 spillformålene og bladene fram i Formålstrær som forslag | proposals godkjent eller avvist |

## Fase 2: arbeidsbenken i HAVEN

| WP | Formål | Utfører | Hva | Test | Leveranse i §3 |
|---|---|---|---|---|---|
| WP-C1 | C1 purpose-keyed-entries | Claude | Validator for bibliotekfilen: nekter oppføring uten `purposeRefs`, lisens og kilde, og nekter refs som ikke finnes | T-C1 | `Tools/GameToolLibrary/validate.py` + TESTRESULT.md#bibliotek-validator |
| WP-C3 | C3 derived-from-sources | Claude | Generator som bygger API-oppføringene fra KAPLAY `dist/doc.d.ts` for en låst versjon; formålskoblingen ligger i en liten håndskrevet tabell | T-C3 | `game-tool-library.v1.json`, TESTRESULT.md#utledet |
| WP-C2 | C2 purpose-first-lookup | Codex | `GameToolLibraryCell` (`cell:///GameToolLibrary`) med `library.lookup`: formål først, så ordsøk | T-C2 | celle + TESTRESULT.md#oppslag |
| WP-D2 | D2 sandbox-isolation | Codex | Egen rute som serverer spillet med CSP `sandbox allow-scripts` og ingen informasjonskapsler; et ondsinnet testspill prøver å lese økt og kalle API | T-D2 | rute + Playwright-test, TESTRESULT.md#sandkasse |
| WP-GUI | B2, D2 (beslutning 1) | Claude, så Codex | `Visualization`-typen `gamePreview` i `skeleton-runtime.js`, pluss tre CellConfigurations, «Lag spill», «Verktøy» og «Prosjekter», som skal matche de godkjente bildene | GUI-paritet mot `images/*-v1.png` | `skeleton/*.json`, skjermbilder side om side i ACCEPT.md#gui |
| WP-D3 | D3 swappable-adapter | Claude | Forhåndsvisningsadapter med én fil per motor (KAPLAY nå, Phaser som bevis) | T-D3 | ACCEPT.md#adapter |
| WP-E1 | E1 uses-haven-workbench | Codex | Spillprosjekt som `ProjectPortfolio`-prosjekt med `WorkItem`-poster (`Sources/App/Cells/WorkItems/`) | T-E1 | ACCEPT.md#prosjekt |
| WP-E2 | E2 versioned-changes | Codex | `GameProjectCell` med `project.applyProposal` og `project.revert`; hver godtatt endring er en versjon | T-E2 | TESTRESULT.md#versjoner |
| WP-B4 | B4 propose-human-decides | Codex | Forslag går som `GroundedActionPlan`; målcellen sjekker tilgang. Negative tester: endring uten klikk, feil bruker, ukjent formål | T-B4 | TESTRESULT.md#auth |
| WP-B5 | B5 reusable-profile (beslutning 3) | Codex | Register som laster profiler etter `contract/workbench-assistant-profile.v0.schema.json`; spillverkstedet og en liten Developer Workbench-profil lastes av samme motor | T-B5 | TESTRESULT.md#profil |
| WP-B3 | B3 select-tools-by-purpose | Codex + Claude | Hjelperen henter verktøy fra `library.lookup`, og hvert forslag har `usedLibrary` | T-B3 | ACCEPT.md#verktoyvalg |
| WP-B1 | B1 understand-intent | Claude | Måling av tjue barneformulerte ønsker skrevet av en uavhengig tråd, før og etter | T-B1 | TESTRESULT.md#forsta |
| WP-B6 | B6 child-safe-dialogue | Claude, så Kjetil | Regler i profilen (`audience`) og et testsett med vanskelige meldinger som Kjetil går gjennom | T-B6 | ACCEPT.md#trygg |
| WP-B2 | B2 preview-before-change | Claude | Måle tiden fra forslag til synlig forhåndsvisning, tre forsøk på den ekte flaten | T-B2 | TESTRESULT.md#forhandsvisning |
| WP-A2 | A2 explain-each-change | Claude | Ti ekte forslag har forklaring og markerte linjer | T-A2 | TESTRESULT.md#forklaring |
| WP-A1 | A1 progression-path | Claude, så Kjetil | Nivåene fra profilen styrer hva som er synlig; nivå 1–2 prøves med Sverre | T-A1 | ACCEPT.md#laeringssti |
| WP-E3 | E3 child-readable-tasks | Claude, så Kjetil | Oppgavetekster i barnespråk på prosjektflaten; Sverre forklarer tre | T-E3 | ACCEPT.md#oppgaver |
| WP-A3 | A3 mentor-oversight | Codex | Kjetils oversikt over Sverres økter og forslag i Developer Workbench | T-A3 | TESTRESULT.md#mentor |
| WP-H2 | H2 skills | Claude | Skills `workbench-assistant-authoring` og `game-workshop-mentor`; en ny tråd lager en Developer Workbench-profil bare med skillen | T-H2 | ACCEPT.md#skills |

## Fase 3: publisering

| WP | Formål | Utfører | Hva | Test | Leveranse i §3 |
|---|---|---|---|---|---|
| WP-F2 | F2 guardian-approval | Codex | Publisering krever Kjetils godkjenning per versjon; ny versjon krever ny godkjenning | T-F2 | TESTRESULT.md#godkjenning |
| WP-F1 | F1 public-address | Codex | Egen rute for publiserte spill ved siden av `/pub` (`Sources/App/Controllers/VaporPublication.swift:39`) | T-F1 | TESTRESULT.md#publisering |
| WP-F3 | F3 child-privacy | Claude | Inspeksjon av publisert spill: ingen persondata, CSP `connect-src` stengt | T-F3 | ACCEPT.md#personvern |
| WP-G2 | G2 split-out-criteria | Claude | Måle kriteriene for å skille ut en egen spillvert | T-G2 | ACCEPT.md#scaffold |

## Gjennom alle faser

| WP | Formål | Utfører | Test |
|---|---|---|---|
| WP-G1 | G1 no-new-scaffold-yet | Claude | T-G1: ingen ny Package-target før WP-G2 er målt |
| WP-H1 | H1 dedicated-area | Claude | T-H1: hver påstand om implementert oppførsel har fil:linje |
| WP-H3 | H3 lesson-capture | Claude | T-H3: `purpose_dev.py validate` grønn etter hver fase |

## Avhengigheter

```
WP-0a, WP-0b, WP-0c
  → WP-C1 → WP-C3 → WP-C2 → WP-B3
  → WP-D2 → WP-GUI → WP-D3 → WP-B2
  → WP-E1 → WP-E2 → WP-B4 → WP-B5 → WP-B1, WP-B6
  → WP-A2, WP-A1, WP-E3, WP-A3, WP-H2
  → fase 3: WP-F2 → WP-F1 → WP-F3 → WP-G2
```

## Ikke med i planen

- Binding (SwiftUI) får ikke `gamePreview` eller de nye flatene.
- Ingen barne- eller foresattmodell i HAVEN. Kjetil godkjenner som eier.
- Ikke vektorsøk i biblioteket med mindre WP-C2 viser at ordsøk ikke holder.
- Lyd og bilder lastet fra nettet i spillene. Kenney-pakkene kommer først når C4 er kontrollert.

## Overlevering til Codex

Codex-pakkene (WP-C2, WP-D2, WP-E1, WP-E2, WP-B4, WP-B5, WP-A3, WP-F1, WP-F2) skrives som oppdrag i `handoff/README.md` etter G2. Hvert oppdrag har mål, formålsref, testen som skal bli grønn og byggekommando etter `AGENTS.md`:

- `scripts/run_swift_bounded.sh`
- `ci/check-value-literals.sh`
- høyst 20 oppføringer per `.object`/`.list`
