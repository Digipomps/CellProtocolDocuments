# TESTRESULT — PZ1, 2026-09-14

**Skrevet, verifisert med avgrenset test.** WP1–WP4 er skrevet. Bygg og alle 8 nye Swift-tester passerer; avtalt regresjonsfilter har én eksisterende feil, gjentatt før endring. WP5 har en eksplisitt integrasjonsbegrensning: Palazzo-applikasjonen er ikke kjørt sammen med Porthole. G3 er ikke godkjent; G5/parity er Kjetils WP6.

## baseline

Målt på eksisterende arbeidstre før kodeendring, uten git-kommandoer. Handoffens opplysning om ucommittede B3-filer er lagt til grunn; mtime/hash er filinventar, ikke bevis for git-status eller forholdet til origin/main. Ingen nettverkskontroll av revisjoner eller CI er utført.

Kommando fra HAVEN-roten (samme isolerte testinngang som handoffen):

```sh
HAVEN_SWIFTPM_RUNNER="$(pwd)/PalazzoScaffold/docs/sicilia-g7-evidence/swiftpm-local-runner.sh" zsh CellScaffold/scripts/run_tests_isolated.sh --filter 'PortholeWeb|ConfigurationCatalog|RemoteBridgeheadAccess|AdminAuthenticatedVaporBridgeTransport|AdminControlPlaneRouting'
```

Runneren bruker isolert test-HOME og lokal `.build`, med `--disable-sandbox --skip-update --disable-automatic-resolution`. Ingen annen SwiftPM-inngang ble brukt.

| Kjøring | Bygg | Tester | Hoppet over | Feil | Exit |
|---|---:|---:|---:|---:|---:|
| WP0 før | 95,01 s, pass | 121 | 2 | 1 | 1 |
| WP0 gjentatt før | 17,58 s, pass | 121 | 2 | 1 | 1 |
| WP5 etter | 23,58 s, pass | 129 | 2 | 1 | 1 |

Forventet ≈ 121 eksisterende tester, målt i denne kjøringens WP0; etter = 121 + 8 nye. Rålogger: [før](evidence/wp0-tests.log), [gjentatt før](evidence/wp0-tests-repeat.log), [etter](evidence/wp5-regression.log).

B3-filene før endring (mtime i UTC; full SHA-256 i [B3-inventaret](evidence/wp0-b3-files.json)):

| Fil i CellScaffold | Bytes | mtime UTC |
|---|---:|---|
| `Sources/App/configure.swift` | 142955 | 2026-09-09 01:27:49 |
| `Sources/ScaffoldKit/AdminAuthenticatedVaporBridgeTransport.swift` | 18520 | 2026-09-09 01:27:49 |
| `Sources/ScaffoldKit/RemoteBridgeheadAccess.swift` | 3188 | 2026-09-08 10:51:44 |
| `Tests/AppTests/AdminAuthenticatedVaporBridgeTransportTests.swift` | 3837 | 2026-09-08 23:59:26 |
| `Tests/AppTests/AdminControlPlaneRoutingTests.swift` | 7755 | 2026-09-08 23:59:26 |
| `Tests/AppTests/RemoteBridgeheadAccessTests.swift` | 6038 | 2026-09-08 23:59:26 |

Bare `RemoteBridgeheadAccess.swift` ble endret blant disse. [Fullt filinventar før](evidence/wp0-file-inventory.json) inneholder 1526 filer; førkopier av de berørte eksisterende filene ligger i `evidence/before/`.

## build

**Pass innen avtalt testbygg.** Sluttkjøringens rålogg viser:

```text
Build complete! (23.58s)
```

`swift test` gjennom den isolerte runneren bygde berørte moduler og testproduktet; dette er ikke et separat release-bygg. Sandkassen blokkerte ikke bygget. `KJOR-SELV-build.sh`-stoppregelen ble derfor ikke utløst.

Utviklingskjøringene er bevart: [første forsøk](evidence/wp5-remote-tests.log) hadde en manglende `payload: nil` i testens BridgeCommand-konstruktør; [andre](evidence/wp5-remote-tests-2.log) avdekket manglende resolver i lokaltest og synkron svarlevering i minnetransporten; [tredje](evidence/wp5-remote-tests-3.log) avdekket testens antakelse om IPv6-klammer i Foundation `URL.host`. Testoppsettet ble rettet, ingen produksjonsomgåelse eller svekkelse av forventninger. Endelig bygg/test er `wp5-regression.log`.

## regression

**Eksisterende feil fortsatt rød; ingen nye feil i det avtalte filteret.** Samme feil i begge førkjøringer og etterkjøringen:

```text
ConfigurationCatalogSkeletonParityTests.swift:316
 testConferenceParticipantPortalDocumentationConfigurationMatchesRuntimeFactory
Key mismatch at $.skeleton.VStack[1].Tabs.panels[1].content[0].Section.content[4].Tabs.panels[0].content[2].List.
Missing from runtime: []. Missing from documentation: ["activationActionKeypath"].
```

Sluttresultat:

```text
PortholeWebRemoteConfigurationTests: Executed 8 tests, with 0 failures
Selected tests: Executed 129 tests, with 2 tests skipped and 1 failure
```

Den eksisterende dokumentasjons-/factory-feilen er ikke rettet i denne slicen. De 310 eksisterende test-/fixturefilene i inventaret er uendret. Den statiske `portholeSupportedEndpoints`-listen er byte-identisk. Se [scope-kontroll](evidence/scope-check.json). Full testmengde, release-bygg og GUI-kjøring er ikke utført.

## remote-lookup

**Pass for avgrenset in-memory-kontrakttest; full Palazzo-integrasjon ikke verifisert.**

`testRemoteLookupLoadsExportOverInMemoryBridgeAndReadsLivePublisher` kjører produksjonens `executeAction` → `loadRequestedConfiguration` gjennom XCTVapors HTTP-testinngang. Session/requester settes i testharnessen; innlogging og den vanlige rutens session-oppslag inngår ikke.

- `{name:"Palazzo Gjest", sourceCellEndpoint:"cell://127.0.0.1:18083/PalazzoGuestShell", keypath:"guest.configuration"}` → HTTP 200, aktiv konfigurasjon «Palazzo Gjest».
- Både bart og innpakket oppslag leser keypath. Navn/UUID på aktiv konfigurasjon hopper ikke over ny henting.
- `RemoteBridgeheadAccess.registerRemoteHosts` brukes med ekte `CellResolver`; testtransporten kontrollerer vert, port og `/bridgehead/<publisher>/<bridge-id>`.
- Ekte `BridgeBase` finnes på begge sider. Tilknyttet `guest` er en bro; `guest.guest.state.house.headline` leses to ganger med endret verdi på kilden mellom lesingene.
- Ugyldig konfigurasjonsverdi fra en ny keypath gir HTTP 400, selv når samme flate allerede er aktiv.

Kilden i testen er en GeneralCell-probe som publiserer den uendrede Palazzo-eksporten. Ingen Palazzo-celler er kopiert inn. Palazzo og CellScaffold har begge en intern `App`-modul; dagens CellScaffold-testmål har ingen Palazzo-avhengighet, og CellScaffold publiserer ikke Porthole-App som bibliotek. En sammensatt test i Palazzo ville derfor også kreve endret pakkestruktur. Dette ble ikke innført i denne slicen. HTTP-upgrade/Bearer-validering mot **selve PalazzoBridgehead** og virkelig Palazzo-tilstand er dermed et gjenstående integrasjonskrav, ikke dokumentert som bestått. B2/G7-loggene er historikk, ikke en ny kjøring.

Resolverens fjernruting for den avtalte `127.0.0.1:18083`-adressen fungerte i testen, så WP2-stoppregelen om manglende resolverkapabilitet ble ikke utløst. `localhost` er derimot reservert for lokal ruting i `CellProtocol/Sources/CellBase/Cells/CellResolver/CellResolver.swift:1396`; Porthole avviser denne formen eksplisitt. Ingen CellProtocol-kode er endret.

## trust

**Pass.** `testTrustRejectsBeforeAnyResolverCallEvenWhenActiveUUIDMatches` bekrefter HTTP 400 og tom resolver-kalliste for ukjent vert, feil port, manglende/blank keypath, manglende port, userinfo, query og `localhost`. Aktiv UUID matches med vilje for å beskytte mot snarveier. Manglende token avvises også uten resolver-kall.

`testBridgeheadAdmissionReusesEnvironmentValidation` bekrefter opt-in, samme token/vertsparser, ugyldig token/vertsliste, korrekt port, vertsnavn uavhengig av store/små bokstaver og IPv6. Ingen ny miljøvariabel for produksjon er innført; requester videreføres til resolver og cellens GET.

## rewrite

**Pass.** Testfixturen er en byte-identisk kopi av `PalazzoScaffold/docs/sicilia-gui-evidence/inputs/gjest-sicilia-liste.cellconfiguration.json`.

`testRewriteExportChangesOnlyDiscoveryAndTopLevelReferenceEndpoints` sammenligner kanonisk JSON: bare discovery-endepunkt og øverste cellReferences-endepunkt endres. Labels, skeleton, subscriptions og setup-verdier beholdes; innverdien muteres ikke. Egen test dekker IPv6, allerede fjerne referanser, HTTPS og gjentatt omskriving. `testLocalLookupWithKeypathUsesExistingConfigurationWithoutRewriting` laster en lokal aktiv flate gjennom den eksisterende kodeveien og sammenligner hele konfigurasjonen.

## allowlist

**Pass.** `testPublishedAllowlistMatrixAndTokenScope`:

| Tilfelle | Resultat |
|---|---|
| Lokal kjent (`AgreementWorkbench`) | true |
| Lokal ukjent (`PalazzoGuestShell` i CellScaffold) | false |
| Fjern, godkjent vert og port med token | true |
| Fjern, ikke godkjent vert | false |
| Fjern, feil port eller uten token | false |

Kontrollplanets navnebegrensning evalueres fortsatt før den nye bridgehead-regelen. Den statiske lokale listen er uendret.

## preview-tool

**Pass for offline-kontrakt og syntaks.**

```text
node --check CellScaffold/scripts/skeleton-iterate.js — exit 0
bash -n PalazzoScaffold/docs/sicilia-gui-evidence/run-g5.sh — exit 0
```

Rålogger: [node](evidence/wp4-node-check.log), [bash](evidence/wp4-bash-check.log), [offline-kontrakttest](evidence/wp4-preview-tool.log).

`CellScaffold/scripts/tests/skeleton-iterate-configuration-keypath.test.js` leser de faktiske tre G5-kommandolinjene, kjører produksjonsparser/normalisering/payloadbygging/filskriving, og erstatter bare HTTP-/browseroperasjonene med opptakere. Den kontrollerer CLI/scenario, CLI-prioritet, kebab-case og gammel payload uten keypath.

| Flate | keypath | Lagret input |
|---|---|---|
| Liste | `guest.configuration` | [input.json](evidence/preview-tool/gjest-sicilia-liste/input.json) |
| Artikkel | `guest.article.configuration` | [input.json](evidence/preview-tool/gjest-sicilia-artikkel/input.json) |
| Hus | `content.configuration` | [input.json](evidence/preview-tool/hus-artikkel-tagger/input.json) |

Artikkelens skeleton er identisk med den eksporterte konfigurasjonens skeleton og inneholder `art-pistasj-bronte`. GET-keypathen velger første publiserte artikkel; den eksisterende preview-skeletonen gir den avtalte artikkelbindingen. Ingen input-eksport eller historisk preview-logg er endret.

`run-g5.sh.pre-keypath` er byte-identisk med skriptet før endring. Kun de tre pålagte keypath-argumentene og en purposeRef-/bindingskommentar er lagt til. Valgfri tomtilstand er uendret og mangler derfor fortsatt keypath; den dekkes ikke av denne slicen. G5-skriptet er **ikke kjørt**.

## files

[Filliste med SHA-256](evidence/files.json) bruker HAVEN-relative stier. Den inkluderer kilde, tester, docs, førkopier og evidens; manifestet unntar sin egen hash. Diff mot førkopier ligger i `evidence/*.diff`.

Endrede eksisterende produktfiler: `PortholeWebPayloads.swift`, `PortholeWebSessionSupport.swift`, `ConfigurationCatalogCell.swift`, `RemoteBridgeheadAccess.swift`, `skeleton-iterate.js`, `Skeleton_Runtime_Iteration_Workflow.md` i CellScaffold og de tre preview-kommandoene i Palazzo `run-g5.sh`.

Nye testfiler: `PortholeWebRemoteConfigurationTests.swift`, Palazzo-eksportfixture med proveniens-README og `scripts/tests/skeleton-iterate-configuration-keypath.test.js`. Oppgavens PLAN/STATUS, denne rapporten og ACCEPT er oppdatert. Ingen git-kommandoer, nettverksoperasjoner, `pkill -f`, endringer under `CellProtocol/` eller endringer av eksisterende tester er utført.

<!-- PZ1 FERDIG -->
