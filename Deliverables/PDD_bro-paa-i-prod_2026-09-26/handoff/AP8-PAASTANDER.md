STATUS: DELVIS — andre gjennomgang 2026-09-28 06:50Z; ingen falsk påstand om kontakt over CellScaffold-broen funnet. Broen har vært kjent av siden **29.08** (ikke 02.09 som først rapportert), og ble funnet seks ganger uten leveranse eller avvisning

# AP8 — påstander siden 13.07 om kontakt med prod/staging over broen

Formål: `purpose://candidate.bro-paa-i-prod.aerlige-paastander`. Utført av Losen.

## Hva som er søkt

- Runde 1 (28.09 01:50Z): 3 734 filer (`.md`, `.json`, `.log`) endret etter 2026-07-13 under `HAVEN-Deploy/_handoff` og `CellProtocolDocuments/Deliverables`, regex på bridgehead / «over broen» / «via broen» / «over bridge» innen 120 tegn fra prod / staging / haven.digipomps.org: 52 treff, 23 dokumenter. Prosjektdokumentene (morgenrapporter 23.–27.09, release-planen 26.09) via prosjektsøk.
- Runde 2 (28.09 06:45Z): 1 385 filer (`.md`, `.txt`, `.json`) endret etter 2026-07-13 under `Binding/Documentation`, `HavenAgentD`, `CellScaffold/Documentation`, `Losen` og `Claude outputs`, samme regex utvidet med «via bridge», «over the bridge», «broen virker/fungerer/er oppe»: 26 treff i 17 dokumenter. Losens hendelseslogg lest rundt treffene.
- **Ikke søkt:** Codex-rapporter utenfor disse mappene, samtaler, git-commitmeldinger.

## Tidslinje: når broen var kjent av

| Dato | Dokument | Hva det sier |
|---|---|---|
| 29.08 | `Binding/Documentation/HAVEN_Skeleton_Render_Audit_2026-08-29.md` | **Første funn.** 40 av 40 celler røde mot staging og prod; `/bridgehead` gir 404 fra Vapor; årsak commit `14b50a51` (13.07). Sier eksplisitt: «Dette er en beslutning, ikke en bug å fikse i Binding» med valgene (a) autentisert generell bro, (b) native-porthole med kontrakt, (c) appen snakker ikke lenger med hovedscaffoldet. Første anbefaling: «Bestem hva som skal erstatte `/bridgehead`.» |
| 02.09 | `Binding/Documentation/HAVEN_Bro_Forensikk_og_Status_2026-09-02.md` | Fire rutesamlinger avregistrert; CP-klientpatch og `VaporCellBridge` med origin-bevis skissert. |
| 03.09 | `CellScaffold/Documentation/Operations/natt-qa-20260903/Paritet_Binding_Web.md` | Alle fjernflater mot staging/prod feiler med −1011; den generelle broen er fjernet. |
| ~12.09 | `Losen/logg/Losen_Hendelseslogg.md`, `HAVEN-Deploy/_handoff/KO-REGISTER.md` HD-0073 | «staging har ingen bridgehead — bare Sprout med allowlist»; HD-0073 registrert med eier Kjetil, «trenger hans valg». |
| 14.09 | `Losen/logg/Losen_Hendelseslogg.md` (HD-0078), `Binding/Documentation/HAVEN_Parity_Night_2026-09-14.md` | «Eksternt scaffold over bridgehead kan altså ikke lastes i Porthole i dag»; paritetsnatten noterer 29.08-funnet som historisk evidens. |
| 15.09 | `Deliverables/Bro_Gjenoppretting_2026-09-15/`, `Deliverables/Bro_Maaling_2026-09-15/` | Utkast til autentisert gjenoppretting, stoppet på tre sikkerhetsfunn; måling 404/1006. |
| 16.09 | `HAVEN-Deploy/_handoff/HD-0040/` | Registrering av `VaporBridgehead` stoppet (typen er ingen RouteCollection). |

## Funn per dokument

| Dokument | Hva det sier | Vurdering |
|---|---|---|
| Dokumentene i tidslinjen over | Broen er borte / stoppet | Riktige. Problemet er at ingen av dem førte til leveranse eller avvisning. |
| `PDD_correspondence-varsel-hendelsesbasert_2026-09-12` (FORMAALSSPEC, VALIDERING b2, dataflow) | Ingen `/bridgehead` på staging; daemon→staging må gå via Sprout eller gjenopprettet bro | Riktig, markert som driftsendring (HD-0073). |
| `Deliverables/Bro_Maaling_2026-09-15/README.md` | Palazzo-broen (`/palazzo-concierge/bridgehead/…`) svarer `ready` på staging og prod | Riktig. Palazzo-broen er en egen rute i PalazzoScaffold med token og peer-bevis. |
| `PDD_palazzo-porthole-fjernt-scaffold_2026-09-14/ACCEPT.md` §1 WP2 | «Oppslag over bridgehead gir 200» | TESTRESULT er ærlig (in-memory, XCTVapor, testtransport), men ACCEPT-raden «Produksjonens Porthole-action … gir 200» kunne leses som prod. **Rettet 28.09**: presisert at det er en in-memory-test med produksjonskode, ikke en prøve mot staging/prod over noen av broene. |
| `PDD_palazzo-raadgiverpanel-signalmatching_2026-09-26` FORMAALSSPEC | «contradicted: broen er av i produksjon» | Riktig. |
| `CellScaffold/Documentation/Operations/HAVEN_Bridge_Multipleks_og_E2E_Status_2026-08-20.md` | Kodestatus for multipleksing/E2E; «vertssiden finnes ikke» | Ingen påstand om kontakt. Oppdaget ikke at `/bridgehead` var borte. |
| `CellScaffold/Documentation/ProjectControl/HAVEN_DevTooling_Work_Intake_2026-08-19.json` | «loopback-bro oppe» (lokal adresse) og «bootstrap gyldig mot staging» | Gjelder daemonens lokale loopback-bro, ikke CellScaffolds rute. Ikke falsk. |
| `Binding/Documentation/HAVEN_Catalog_Render_Guarantee_2026-08-20.md`, `ATS_TransportScheme_Handoff_2026-08-24.md` | Bridgehead-websocket feiler (bad response / ATS) | Riktige feilobservasjoner; årsaken (avregistrert rute) ble ikke funnet før 29.08. |
| `HavenAgentD/.worktrees/…/Binding/Documentation/Conference*` (datert april 2026) | «live staging bridgehead … verified» | Skrevet før 13.07 og da riktig. Kopiene i worktree har ny mtime, men er historiske. |
| Morgenrapporter 23.–27.09 | Ingen påstand om kontakt over CellScaffold-broen | — |

## Konklusjon så langt

1. Jeg har **ikke** funnet et dokument som påstår at noe har kommunisert med prod eller staging over CellScaffolds `/bridgehead` etter 13.07.
2. Det alvorlige funnet: **broen ble funnet av seks ganger (29.08, 02.09, 03.09, ~12.09, 14.09, 15.–16.09)**. 29.08-rapporten sa uttrykkelig at dette var en beslutning og la fram valgene. Den nærmeste forespørselen til Kjetil jeg har funnet er HD-0073 (~12.09, «trenger hans valg»), som gjaldt staging for correspondence, ikke broen generelt. Losen skrev en ny spesifikasjon 26.09 uten å lese noe av dette. Lærdom: `HAVEN-Deploy/lessons/L-2026-09-28-tidligere-arbeid-ikke-lest-for-ny-plan.json`.
3. Det som faktisk virker mot prod over bro i dag er **Palazzo-broen** og **native-porthole** (med Sprout-kontrakt). Påstander om «bro mot prod» må skille disse fra CellScaffold-broen.
4. Rettelse av min egen melding til Kjetil 28.09 01:40Z: jeg skrev «kjent av siden 02.09»; riktig tidligste dato er **29.08**.

## Rettelser som gjenstår

- HD-0073 i KO-registeret: lukke med henvisning til denne PDD-en når broen er i prod.
- Søke Codex-rapporter utenfor de søkte mappene og commitmeldinger (lav forventet verdi).
