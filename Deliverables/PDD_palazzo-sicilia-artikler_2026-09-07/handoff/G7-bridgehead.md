# Codex-handoff — G7: gjeste- og innholdscellen over bridgehead (2026-09-08, godkjent av Kjetil «Ja absolutt»)

Formål: Porthole og HAVEN-appen (Binding) skal kunne nå `PalazzoGuestShell` og `PalazzoContent` over bridgehead,
slik at de tre Sicilia-flatene (gjesteliste, artikkel, husets tagger) faktisk kan vises i appen — med samme
token-krav som i dag. Antiformål: ingen svekkelse av tilgang — cellene får ikke flere rettigheter enn `validateAccess`
gir i dag; bridgehead-token er fortsatt påkrevd; gjesteidentitet gir ikke husinnsyn.

Bakgrunn: `Rapport_Sicilia_GUI_2026-09-07.md` og `images/verify/NATIVE.md`/`AVVIK.md`: `PalazzoBridgehead.isPublishable`
omfatter ikke `Cells.guestShell`/`Cells.content`; CellScaffold sender ikke `PALAZZO_BRIDGEHEAD_TOKEN` på `cell://`-oppslag.

| # | Hva | Test |
|---|---|---|
| B1 | `PalazzoBridgehead.isPublishable`: legg til `PalazzoScaffoldContract.Cells.guestShell` og `.content` (bruk de faktiske kontraktnavnene). Test: bridgehead-oppkobling mot begge cellene lykkes med token, avvises uten token, og en ukjent celle avvises fortsatt. | test.bridgehead.publish-guest-content, test.bridgehead.token-required |
| B2 | Tilgang gjennom bridgehead: en gjesteidentitet som når `PalazzoContent` over bridgehead får `content.configuration` (hus-flaten) nektet; husets eier får den. `guest.configuration` og `guest.article.configuration` fungerer for gjesten. Reaksjon via bridgehead lagres som ved HTTP. | test.bridgehead.guest-vs-house, test.bridgehead.reaction |
| B3 | CellScaffold: finn hvor `cell://host:port/...`-oppslag mot en fjern bridgehead bygges (`skeleton-iterate`/Porthole-klient), og sørg for at bridgehead-token kan gis (miljøvariabel, f.eks. `HAVEN_BRIDGEHEAD_TOKEN` eller det navnet CellScaffold allerede bruker for tilsvarende) og sendes som Bearer/WS-query slik `PalazzoBridgehead` krever. Minimal endring; ingen ny protokoll. Dokumenter variabelen i `Documentation/Skeleton_Runtime_Iteration_Workflow.md`. Hvis CellScaffold allerede har en slik mekanisme: bruk den, ikke lag ny. | test i CellScaffold sin eksisterende suite (unit) |
| B4 | Oppdater `PalazzoScaffold/docs/sicilia-gui-evidence/run-g5.sh` slik at Porthole-steget får token (fra B3) — og rett eventuelle andre feil du finner ved en tørrkjøring av seed-steget mot en XCTVapor-instans. Ikke kjør hele skriptet (sandkassen nekter bind/Chromium). | bash -n + seed-tørrkjøring |

Regler: CellProtocol og Binding røres ikke; CellScaffold endres bare i B3 (minimal); ingen test fjernes/svekkes; ingen git;
`swift build/test --disable-sandbox` i PalazzoScaffold, og CellScaffold sin egen testkommando for B3.
Rapport: `PalazzoScaffold/docs/Rapport_Sicilia_G7_2026-09-08.md` (rå utdata før/etter, per slice gjort/avvik, filliste inkl. CellScaffold-filer).
Svar kun med rapporten.
