# PLAN — dele dokumenter mellom studenter

G1 og G1-GUI godkjent av Kjetil 2026-11-20. Denne planen ber om G2.

Grunnlag: CellScaffold `272580b` (main 20.11, med #465 analyserom, #466 skrivehjelp, #468 chat-grant), CellProtocol `669850b` (main 20.11), PyCellProtocol og GoCellProtocol `main`.

§6 i spesifikasjonen, slik planen tolker G1: spm. 1 er besluttet (felles del i CellBase). For spm. 2–4 følger planen anbefalingene som sto i spesifikasjonen da G1 ble gitt: (2) `DocumentInstance` + biblioteket «Dokumenter», (3) «Lag dokument for samtalen» er med, (4) native editor i Binding blir en egen tråd. Si fra hvis noe av dette er feil, så endrer jeg planen før koden.

Utførere: Claude skriver koden i skycontaineren. Swift kan ikke bygges der, så alle Swift-bygg og -tester kjøres på Kjetils Mac gjennom en Remote Control-økt (`/Users/kjetil/Build/Digipomps/HAVEN/`), i egne kloner under `/tmp` og aldri i den skitne hovedutsjekken av CellScaffold. Python og Go kjøres i skycontaineren.

## Arbeidspakker

| WP | purposeRef | Hva | Test som skal bli grønn | Utfører | Artefakt |
|---|---|---|---|---|---|
| WP0 | quality.build-and-regression | Baseline: full `swift test` på ren eksport av CellProtocol `origin/main` og CellScaffold `origin/main`. Antall tester og røde skrives ned, med feil som allerede er kjent | test.regression (baseline) | Mac (RC) | TESTRESULT.md#baseline |
| WP1 | many-documents, admission | Måler de tre «ikke målt»-radene i §2: (a) kan en invitert uten kontrakt nå en `.template`+`.persistant`-celle med `cell:///<uuid>` og presentere aksepten, (b) åpner web-Porthole en konfigurasjon med referansen `cell:///<uuid>`, (c) overlever mange dokumentceller per identitet en omstart. Sonde-tester, ingen produktkode | sondene | Claude + Mac | TESTRESULT.md#maaling |
| WP2 | shared-admission | CellBase: `InvitationAdmission` trekkes ut av `ChatCell` (invitasjon, signert artefakt, aksept, `audience.admission.*`, `audience.admissionConditions`, tilbakekalling). `ChatCell` bruker den med uendrede keypaths og uendret oppførsel. Først leser jeg `GeneralCell.agreementDerivedFromTemplate` for å finne ut hvordan rollen (skrive/lese) kan ligge i Agreement-vilkåret og ikke i en egen sjekk. Krever det en endring i hvordan maler matches, sier jeg fra før jeg skriver den | test.dele.chat-uendret, test.dele.invitasjon-signert-og-bundet, test.dele.opptak-via-vilkaar | Claude + Mac | PR CellProtocol |
| WP3 | cross-language | Gyldne fixtures (artefakt, aksept, forventet opptak/avslag, rolle) skrevet fra Swift. Samme del i PyCellProtocol og GoCellProtocol, og deres chat bruker den | test.dele.interop-fixtures | Claude | PR Py, PR Go |
| WP4 | roles, admission | CellScaffold: `RichDocumentCell` tar i bruk `InvitationAdmission`. Skrive = `current`, `feed`, `change`, `assist`, `chat`, `assistPanel`, `chatPanel`. Lese = `current`, `feed`, `chat`, `chatPanel`, `assistPanel` | test.dele.roller, test.cell.auth-negative | Claude + Mac | PR CellScaffold |
| WP5 | many-documents, library | Registrering `DocumentInstance` (`.template`, `.persistant`, `RichDocumentCell`) og bibliotekcellen «Dokumenter» (`.identityUnique`): lag, gi navn, list mine / delt med meg / invitasjoner, åpne, forlat. Gamle `cell:///RichDocument` vises som «Mitt første dokument» | test.dele.flere-dokumenter, test.dele.gammelt-dokument-bevart, test.dele.bibliotek-viser-riktig | Claude + Mac | samme PR |
| WP6 | invite, accept | Levering: bibliotekets nøkkel for innkomne invitasjoner tar bare imot en signert artefakt som navngir bibliotekets eier. Beviset er autoriteten, slik `acceptInvitationArtifact` er i dag. Varsel som for chat-invitasjoner. Personvelgeren henter kontakter fra Samtaler | test.dele.godta-avslaa | Claude + Mac | samme PR |
| WP7 | library, invite, accept, swift-native | Flatene fra de godkjente bildene (`images/*-v1.png`), bygget av vanlige skeleton-elementer: «Dokumenter», «Del dokumentet» ved editoren, invitasjonen og «Ingen tilgang» | test.gui.parity (web), skjermbilder mot bildene | Claude | `images/` faktisk ved siden av godkjent |
| WP8 | revoke | «Fjern» deltaker, «Trekk tilbake» invitasjon, «Forlat» for deltakeren. Neste `get`/`set` avvises og feeden stopper | test.dele.tilbakekall | Claude + Mac | samme PR |
| WP9 | chat-link | «Lag dokument for samtalen» i Samtaler: lager et dokument og inviterer alle i samtalen | test.dele.fra-samtale | Claude + Mac | samme PR |
| WP10 | shared-admission | Analyserommet (#465) bytter til den felles delen og til samme adressering. Avtales med tråden «Bygg dokument- og argumentanalyse for studentene», som eier rommet | rommets egne tester uendret grønne | tråd C | PR CellScaffold (tråd C) |
| WP11 | swift-native | Binding (Swift) bygges mot ny CellProtocol. Flatene fra WP7 tegnes og virker i Binding: godta, avslå, fjern, forlat | test.gui.parity (Binding) | Mac (RC) | skjermbilder i ACCEPT.md |
| WP12 | quality.build-and-regression | Full `swift test` CellProtocol og CellScaffold mot WP0-baselinen, `pytest`, `go test`. Ingen nye røde, og antallet øker med nøyaktig antallet nye tester | test.build, test.regression | Mac (RC) + Claude | TESTRESULT.md#build, #regression |
| WP13 | root | FORESPOERSEL til Deploy når bygget er verifisert. Etter at det er deployet: Playwright på staging med tre nye studentkontoer (A inviterer B, B skriver, C avvises), med video | test.dele.e2e-to-studenter | Claude | TESTRESULT.md#e2e + video |
| WP14 | — | ACCEPT.md (§3 rad for rad, med bilder side om side) og nye lærdommer | G3 | Claude | ACCEPT.md |

Rekkefølge: WP0 og WP1 først. Viser WP1 at `.template`-celler ikke kan nås før kontrakt, endres WP5 før det skrives kode. Deretter WP2 → WP3 parallelt med WP4 → WP5–9 → WP11 → WP12 → WP13 → WP14. WP10 kan starte når PR-en fra WP2 er oppe.

## Avgrensning

- Native dokumenteditor i Binding er ikke med (§6 spm. 4). Det er bedt om en egen tråd for den.
- Ingen merge, tag eller deploy fra denne tråden. Staging bare via FORESPOERSEL etter grønt bygg på Mac.
- CellScaffold skal følge siste CellProtocol. Pinnen løftes i samme PR som WP4, og bare til en CellProtocol-commit som ligger på `main`.
