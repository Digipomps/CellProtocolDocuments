# STATUS — Python-forskningsscaffold

- surfaces: cell, python, scaffold, terminal
- tags: python, reproducibility, research
- Oppdrag: implementere med start i WP1; inkludert CellBridge-svar til andre scaffolds.
- Planstatus: planforslag levert etter kildekontroll og uavhengig gjennomgang; tre funn rettet og kontrollert på nytt.
- Produktstatus: WP1 lokal runtime og Python-scaffold CellBridge implementert/verifisert; native Swift get/set, autorisert Flow og avmelding er verifisert. Ubetinget Agreement-opptak og signert kvittering er verifisert 8. november. WP2 datasettinntak og WP3 lineær regresjon er implementert og verifisert; WP4–WP6 gjenstår.

## Porter
- G1: godkjent 2026-11-07
- G1-GUI: venter — figurens visuelle referanse lages og vurderes ved implementeringsforberedelse; ingen app-GUI inngår i v1.
- G2: godkjent 2026-11-07
- G3: venter

G1 og G2 følger brukerens eksplisitte plangodkjenning og implementeringsbestilling nedenfor. G3 er ikke godkjent av Codex.

## Planbytter
- 2026-11-06: samlet formål og plan levert i samme planoppdrag; ingen implementeringsstart.

## Logg
- 2026-11-06: kildeinspeksjon av PyCellProtocol på registrert revisjon, uten produktendringer eller runtime-kjøring.
- WP1 er nå implementert; neste arbeidspakke er WP2.
- 2026-11-06: planens regnefasit kontrollert; lokal portkonsistens uten feil. Global PDD-validator har fem eksisterende registerreferansefeil; se PLAN_REVIEW.md.

## Godkjenning og presisering 2026-11-07

> Ja, planen er godkjent. Begynn å implementere forskningsscaffoldet, og start med WP1: verifiser PyCellProtocol-grunnlaget og bygg den lokale runtimen. Den skal svare på CellBridge fra andre scaffolds.

Dette utvider WP1 med inbound CellBridge. Lokal-only/no-listener-avgrensningen i opprinnelig plan er erstattet av WP1_ADDENDUM.md. G1-GUI og G3 er ikke godkjent; WP1 endrer ingen figurflate.

- 2026-11-07: 46 upstream-tester, 54 WP1-tester og ren wheel-/separat-scaffold-test bestått. Ingen permanente tjenester startet. Native Swift-vault/resolver med protected get/set og typed denial bestått; se TESTRESULT_WP1.md. G3 står fortsatt åpen.

## Oppfølging 7. november 2026

Autorisert Swift Flow, siste avmelding og resultatlesing besto etter en avgrenset stopFeed-retting. 56 scaffold-tester besto. Ved uautorisert feed observerte Swift ingen Combine-avslutning etter serverens avslag. Full Agreement-paritet er motbevist. Se [paritetsrapporten](../../../PyResearchScaffold/docs/SWIFT_PARITY.md).

## Agreement 8. november 2026

PyCellProtocol 0.1.1 og forskningsscaffoldet besto fem målte Agreement-sammenligninger med native Swift. Se [rapporten](../../../PyResearchScaffold/docs/AGREEMENT_2026-11-08.md).

- 2026-11-08: Swift ved e3ea7a4 leverte ACCESS_DENIED som avsluttende feil på to avviste feeds. En etterfølgende GET på samme WebSocket besto etter hvert avslag. [Før- og ettermåling](../../../PyResearchScaffold/docs/COMBINE_FLOW_2026-11-08.md).

## Demonstrasjon 10. november 2026

WP1 kjørte prøvemetoden med 123 målinger og returnerte 612745. Jobben passerte queued, running og completed. Nettleseren viste de to offentlige HTTP-operasjonene. Swift-proben mottok terminalt ACCESS_DENIED og leste tjenestestatus etterpå på samme WebSocket. De fem Agreement-sammenligningene, 52 protokolltester og 58 scaffold-tester besto. WP2 med datasettinntak er neste planlagte arbeidspakke.

- [Kjøreeksempel og faktisk skjermbilde](https://github.com/Digipomps/PyResearchScaffold/tree/09030ab).
- [Observerte Flow- og Agreement-svar](https://github.com/Digipomps/PyResearchScaffold/blob/09030ab/docs/evidence/demo-20261110/swift.json).
- [PyCellProtocol med avtalehåndtering](https://github.com/Digipomps/PyCellProtocol/commit/a34c65975124ff56faa3e0d5d51f40c2af296758) og [Swift med avsluttende feed-feil](https://github.com/Digipomps/CellProtocol/commit/e3ea7a4ecab326bb632c0b572ac2efa4a01f1156).

## WP2 datasettinntak 10. november 2026

Brukeren bestilte «Fortsett med WP2. Implementer datasettinntak for det syntetiske kalibreringsdatasettet, og vis at en klient kan registrere det og lese det tilbake via CellBridge.»

PyResearchScaffold 0.2.0 ved d83c9f1 implementerer en registrert DatasetCell med streng CSV- og metadatavalidering, atomisk SQLite-lagring og gjenlesing gjennom ResearchRuntime over CellBridge. Den separate klientprosessen registrerte 11 rader og leste begge filene tilbake byte for byte. Alle 91 tester besto fra installert wheel, inkludert 33 WP2-tester. Inputhashen var 7fe9e51e42da61cc7e951ad9250da6fe96901a7862ce787f3cf58e784c4253f0. De tidligere Swift Flow-/Agreement-kontrollene besto. WP3 analyse er neste arbeidspakke.

[Kontrakt, kjøreoppskrift og testresultater](https://github.com/Digipomps/PyResearchScaffold/blob/d83c9f1/docs/WP2_DATASETS.md). Dette registrerer implementering og målinger. G3-avklaring står hos brukeren.


## WP3 lineær regresjon 11. november 2026

Brukeren bestilte «Fortsett med WP3. Implementer lineær regresjonsanalyse av det registrerte kalibreringsdatasettet, verifiser resultatene mot den uavhengige fasiten, og vis at en klient kan starte analysen og lese resultatet via CellBridge.» Brukeren meldte også at den lokale nettsiden ikke var tilgjengelig.

PyResearchScaffold 0.3.0 ved d0afa67 implementerer AnalysisCell og linear-regression/v1 over registrerte, identitetsavgrensede datasett. En separat CellBridge-klient registrerte 11 rader, startet analysen, mottok queued/running/completed og leste resultat og alle 11 residualer. Gjentatt requestId ga samme jobb-ID. Stigning 2 mV/V, konstantledd 1 mV, SSE 0,14 mV² og R² 22000/22007 ble kontrollert mot eksakt Fraction-regning; standardfeil og 95 % intervaller ble kontrollert med en separat Student-t-beregning. Alle 107 tester besto fra installert wheel, inkludert 16 WP3-tester. Swift Flow og de fem eksisterende Agreement-kontrollene besto.

Den lokale API-visningen på port 8099 drives nå av launchd-brukertjenesten org.haven.pyresearch.local, konfigurert med RunAtLoad og KeepAlive. Running og HTTP ready/version 0.3.0/WP3 ble observert etter at oppstartskommandoen hadde avsluttet. Innlogging og maskinstart er ikke praktisk omstartstestet.

[Kontrakt, tall, testbevis og kjøreoppskrift](https://github.com/Digipomps/PyResearchScaffold/blob/d0afa67/docs/WP3_ANALYSIS.md). Uavhengig dokumentgjennomgang kontrollerte påstandene mot koden og bevisfilene; en presisering om residualpaginering ble rettet. Neste arbeidspakke er WP4 figur. G3-avklaring står hos brukeren.
