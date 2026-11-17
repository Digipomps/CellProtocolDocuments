# Native HAVEN/Binding — Sicilia GUI, 2026-09-07

**Status: manuell overlevering; ingen native skjermbilder eller native paritetsgodkjenning.** Binding er ikke installert, bygget, startet eller endret i denne kjøringen.

## Undersøkt snapshot-vei

- `Binding/BindingUITests/BindingUITests.swift`: skjermbilder for Butterpop og Arendalsuka; ingen Palazzo-test eller argument for en vilkårlig CellConfiguration-fil.
- `Binding/Scripts/run_conference_configuration_verifier.sh`: faste konferanseflater; ingen parameter for de tre Palazzo-flatene.
- `Binding/Scripts/run_skeleton_parity_suite.sh`: konferanse-/stagingtester, ikke Palazzo-snapshot.
- `Binding/Scripts/run_conference_demo_smoke.sh`: faste konferansesteg, agent-staging/installasjon og start/stopp av app/agent. Ikke kjørt: dette oppfyller ikke de bestilte tre snapshottene og strider mot «ikke installer eller endre Binding».

[Lesende søkebevis](../../../../../PalazzoScaffold/docs/sicilia-gui-evidence/native-path-audit.txt).

## Eksakte flater og operasjoner

Forutsatt en nåbar Palazzo-server på `127.0.0.1:18083`, med eksisterende bridgehead-forbindelse og korrekt requester-identitet:

| Flate | Konfigurasjonsnavn | Celle fra native | Operasjon |
|---|---|---|---|
| Gjest | `Palazzo Gjest` | `cell://127.0.0.1:18083/PalazzoGuestShell` | GET `guest.configuration` |
| Første publiserte artikkel | `Palazzo artikkel` | samme gjestecelle | GET `guest.article.configuration` |
| Pistasjartikkelen fra bildet | `Palazzo artikkel` | samme gjestecelle | SET `guest.article.open` med `{"articleID":"art-pistasj-bronte"}`; alternativt velg denne raden i gjestelistens single-selection |
| Husets utkast | `Palazzo Hus — utkast` | `cell://127.0.0.1:18083/PalazzoContent` | GET `content.configuration`, som husets eier |

De to GET-konfigurasjonsrutene for gjest/artikkel er `http://127.0.0.1:18083/api/guest/configuration` og `/api/guest/article/configuration`. Husets er `/api/content/configuration`. Vilkårlig celleoperasjon kan kontrolleres med POST `/api/cell/get` eller `/api/cell/set`, der `endpoint` er **lokal** `cell:///PalazzoGuestShell` eller `cell:///PalazzoContent` inne i Palazzo-serveren. HTTP-API-et bruker `X-Palazzo-Principal`; dette er ikke en erstatning for native bridge-identitet.

## Hva Kjetil må gjøre

1. Start Palazzo fra `PalazzoScaffold` med `.build/debug/Run serve --hostname 127.0.0.1 --port 18083`, isolert `CELL_VAULT_DOCUMENT_ROOT`, egen `PALAZZO_GATEWAY_TOKEN`, `PALAZZO_BRIDGEHEAD_ENABLED=true` og `PALAZZO_BRIDGEHEAD_TOKEN`. Start i et miljø som tillater portbinding. Seed minst tre artikler gjennom draft/approve/publish; kildefixturen er `../../content/artikler_v1.json`. Ingressene fra listebildet mangler i denne fixturen og må avklares som seed-data før eksakt bildesammenligning.
2. Koble HAVEN til denne bridgehead-kilden med gjestens identitet; husflaten krever husets faktiske eieridentitet. En gjesteidentitet kan ikke gis husinnsyn ved bare å endre `X-Palazzo-Principal` i native. Eksisterende identitets-/same-entity-flyt må være fullført der den trengs.
3. Hent konfigurasjonene i tabellen og la den eksisterende native Porthole-lasteren laste den returnerte `CellConfiguration`. Ved fjernlasting må `cell:///`-referansene i konfigurasjonen få Palazzo-kildens origin, slik Bindings eksisterende katalog-normalisering gjør. Rå lokal JSON peker ellers på feil runtime.
4. For vanlig åpning med en `haven://`-lenke må disse konfigurasjonene først finnes i en autorisert `ConfigurationCatalog.configurations`, med tilhørende `ScaffoldLaunchRegistry.publishedRoutes` og registrerte `surfaceID`-er. Binding leser katalogene fra `BINDING_REMOTE_CATALOG_ENDPOINTS` (og standardkatalogen hvis den er aktivert). PalazzoScaffold publiserer ikke disse to katalogcellene i dag. Det finnes derfor **ingen dokumentert, allerede fungerende native åpningslenke for de tre flatene**. Å etablere denne runtime-publiseringen/tilkoblingen er et gjenstående integrasjonssteg; det er ikke utført eller simulert her.
5. Når et faktisk `surfaceID` er publisert, er Bindings eksisterende lenkeformat `haven://open?schema=haven.surface-launch.v1&surfaceID=<registrert-ID>&intent=view`. Åpne gjesteflaten, velg Pistasjartikkelen, og åpne husutkastet med riktig eier. Lagre `native-gjest-sicilia-liste-v1.png`, `native-gjest-sicilia-artikkel-v1.png`, `native-hus-artikkel-tagger-v1.png` her. Kontroller faktisk reaksjon/kommentar, taggredigering/godkjenning/publisering og fravær av debugtekst etter handlingene.

Kildesjekk: `Binding/Binding/PortableSurfaceSupport.swift` definerer lenkeformat, katalogmiljøvariablene og `ScaffoldLaunchRegistry`; `Binding/Binding/ContentView.swift` sin `openRuntimeSurfaceLaunch` krever publisert rute og konfigurasjon før last. Dette dokumentet skiller derfor mellom eksakte, testede Palazzo-operasjoner og native oppkobling som ennå ikke er verifisert.
