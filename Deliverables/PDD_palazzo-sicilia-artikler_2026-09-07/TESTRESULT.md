# TESTRESULT — Sicilia-artikler, WP0–WP5 og G1–G6

Last verified against code: 2026-09-07

Kjørt i `HAVEN/PalazzoScaffold`. WP0–WP5-resultatene under er den opprinnelige implementasjonskjøringen, hvor WP-GUI var uttrykkelig blokkert. Den senere autoriserte G1–G6-kjøringen er dokumentert i GUI-ankrene nederst: 100 Swift-tester består; visuell GUI-akseptanse er fortsatt blokkert.

## build

`swift build --disable-sandbox`: PASS før og etter. Første baseline-bygg: 33,89 s. Et rent baseline-bygg etter `swift package clean`: 157,39 s. Sluttbygg: 15,08 s, exit 0.

Råutdata: [før](../../../PalazzoScaffold/docs/sicilia-evidence/before-build.log), [rent før](../../../PalazzoScaffold/docs/sicilia-evidence/before-build-clean.log), [etter](../../../PalazzoScaffold/docs/sicilia-evidence/after-build.log).

## regression

Baseline: 82 tester, 0 feil. Slutt: 95 tester, 0 feil; 13 nye Sicilia-tester. Alle opprinnelige test-/fixture-filer er byte-identiske med starten. Ingen test ble fjernet, svekket eller hoppet over.

```text
Test Suite 'All tests' started at 2026-09-07 22:45:45.990.
	 Executed 82 tests, with 0 failures (0 unexpected) in 1.186 (1.190) seconds
Test Suite 'All tests' passed at 2026-09-07 22:45:47.182.
	 Executed 82 tests, with 0 failures (0 unexpected) in 1.186 (1.191) seconds
Test Suite 'All tests' started at 2026-09-07 23:04:23.808.
	 Executed 95 tests, with 0 failures (0 unexpected) in 2.545 (2.550) seconds
Test Suite 'All tests' passed at 2026-09-07 23:04:26.359.
	 Executed 95 tests, with 0 failures (0 unexpected) in 2.545 (2.551) seconds
SICILIA E2E: processes [53299, 53300]; 3 identical records after restart; 403 before consent; interests/avoid/purposes verified. Evidence: /var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/sicilia-restart-9EA3B8E5-D709-4756-B150-DB829D7385E3
```

Første baseline-test krasjet med signal 11 i eksisterende `testHuskSkeletonFactoriesUseReachableConcreteActions`. Større stakk og alternativ køinnstilling løste det ikke. Etter rensing av PalazzoScaffolds genererte byggeprodukter og full gjenbygging bestod alle 82, uten kildeendringer. Dette peker på utdaterte byggeprodukter; den eksakte binærårsaken er ikke bevist.

Råutdata: [første krasj](../../../PalazzoScaffold/docs/sicilia-evidence/before-test.log), [stakkforsøk](../../../PalazzoScaffold/docs/sicilia-evidence/before-test-stack.log), [køforsøk](../../../PalazzoScaffold/docs/sicilia-evidence/before-test-queues.log), [grønn baseline](../../../PalazzoScaffold/docs/sicilia-evidence/before-test-clean.log), [full sluttkjøring](../../../PalazzoScaffold/docs/sicilia-evidence/after-test.log), [Sicilia alene](../../../PalazzoScaffold/docs/sicilia-evidence/sicilia-tests-final.log).

## articles

PASS — `testSiciliaArticles`, `testSiciliaArticleValidationAndLegacySnapshots`, `testSiciliaArticleTagEditSkipAndVersioning`.

8 fixture-artikler; body/kilde/region/ID; godkjente tagger; ingen signal uten godkjenning; edit/skip/versjonering; eldre JSON og ugyldige patcher.

## reaction

PASS — `testSiciliaReaction`.

Tre reaksjonstyper, privat proveniens, godkjente tagger, kilde self, ordrett kommentar; ugyldig reaksjon/artikkel/kommentar gir ingen poster.

## persist

PASS — `testSiciliaPersist`, `testSiciliaE2E`.

Faktisk cellefil lastes etter tømt resolverminne og sluppet cellereferanse. E2E verifiserer også to uavhengige prosesser.

## query

PASS — `testSiciliaQuery`.

403 uten samtykke, positiv interesse og separat avoid etter kontrakt+policy, artikkeltagger i purposes, 403 etter revoke.

## signal

PASS — `testSiciliaSignal`, `testSiciliaArticleDoesNotInheritMenuStandingGrant`.

Begge signalkinds; kommentar om Norma gir pending-treff; huset nektes før eksakt innsyn-grant; råposter nektes fortsatt. Stående menuChange-policy utvides ikke til artikler.

## no-tracking

PASS — `testSiciliaNoTracking`.

Tre runder med HTTP-konfigurasjon, publisert artikkelliste og guest.state; record- og event-snapshots uendret. Positiv kontroll viser at faktisk reaksjon emitterer event.

## e2e

PASS — `testSiciliaE2E`.

To separate XCTest-prosesser kjører appens Vapor-ruter med samme isolerte lager. Tre poster, record-ID, recordedAt, entity-ID og identity-ID beholdes. 403 før policy; interests/avoid/purposes etter samtykke.

[Skriveprosess](../../../PalazzoScaffold/docs/sicilia-evidence/process-restart/write.log), [ny leseprosess](../../../PalazzoScaffold/docs/sicilia-evidence/process-restart/read.log), [hele record-fixturen](../../../PalazzoScaffold/docs/sicilia-evidence/process-restart/records.json).

Supplerende TCP-smoke ble forsøkt med en separat `Run`-server. Sandboxen avviste `bind(127.0.0.1:18937)` med `Operation not permitted` før første HTTP-kall. TCP-transport er ikke verifisert; E2E ovenfor bruker faktiske HTTP-ruter via XCTVapor uten nettverksport. [Råfeil](../../../PalazzoScaffold/docs/sicilia-evidence/process-1.log), [kjøringslogg](../../../PalazzoScaffold/docs/sicilia-evidence/process-e2e.log). Scriptet `PalazzoScaffold/scripts/check_sicilia_restart.py` er klart for et miljø som kan åpne lokal port.

## auth

PASS — `testCellAuthNegativeWrongRequester`, `testCellAuthNegativeWrongKeypath`, `testCellAuthNegativeUnknownPurpose`.

Feil forespørrer og feil keypath avvises med 403. purpose://prompt.unknown avvises ved access.request med 400 og gir ingen innsynsrettighet.

## contract

PalazzoScaffold Explore-audit: 89 registreringssteder, 89 komplette operasjonskontrakter, 0 funn. [Rårapport](../../../PalazzoScaffold/docs/sicilia-evidence/explore-app.md).

Den pålagte, lesende audit-kjøringen over urørt CellProtocol rapporterte 7 feil og 19 advarsler utenfor denne oppgaven. Disse er ikke rettet eller regnet som grønne. [Rårapport](../../../PalazzoScaffold/docs/sicilia-evidence/explore-core.md).

## scope

[SHA-256-/handlerkontroll](../../../PalazzoScaffold/docs/sicilia-evidence/scope-and-auth.txt): 26 registreringssteder i Entity, 13 i Content og 4 i GuestShell har eksplisitt validateAccess. De fire eksisterende fabrikkfilene og alle opprinnelige tester er uendret. Ingen CellProtocol-endringer eller git-kommandoer.

Ingen GUI-paritet, visuell lastetid eller godkjenning av artikkeltekstenes faktainnhold hevdes. Fixture-JSON er kopiert uendret fra overleveringen; kildetekstene ble ikke nettverifisert eller publisert som produksjonsinnhold.

## skeleton-list

PASS i Swift/cellelaget — `test.skeleton.sicilia-list` (`testSkeletonSiciliaList`) og `test.skeleton.sicilia-empty` (`testSkeletonSiciliaEmpty`). Ny seksjon etter huset, riktige listefelter/kort/selection/keypaths/payload, faktisk list-kontrakt og utelatelse ved tom liste. Eksakt visuell innholdsparitet er ikke verifisert; seed mangler bildeingressene.

## skeleton-article

PASS i Swift/cellelaget — `test.skeleton.sicilia-article` (`testSkeletonSiciliaArticle`) og eksisterende `test.sicilia.reaction`. JSON-sammenligning, konkrete lesebindinger, tre reaksjoner og ordrett kommentar, feil requester/ukjent artikkel/ugyldig kommentar. TextArea bruker egen artikkelbundet comment-keypath fordi formatet ikke støtter fast TextArea-payload. `testSiciliaNoTracking` er utvidet og består med uendrede record-/event-snapshots ved faktisk konfigurasjonslesing og åpning.

## skeleton-house

PASS i Swift/cellelaget — `test.skeleton.house-article-tags` (`testSkeletonHouseArticleTags`). Artikkeloverskrift, eksisterende radfelt, faktisk valg/redigering/godkjenning/Uten signal/publisering og kontroll av publiserte tagger. Row-payload erstatter eksempelverdien `$id`; Publiser har eksplisitt SET-payload.

## porthole-parity

BLOKKERT — `test.skeleton.porthole-parity` er ikke bestått. Tre `npm run skeleton:iterate -- --mode preview`-forsøk fra urørt CellScaffold, desktop+mobil, stoppet før sideåpning med Chromium MachPortRendezvous Permission denied (1100). Palazzo-kilden fikk EPERM ved lokal bind. Ingen screenshots. Eksporterte faktiske konfigurasjoner/kontrakter og åtte taggodkjente fixture-artikler er celletestbevis, ikke Porthole-paritet. Rå skeleton-validator har fortsatt triagerte funn; den er ikke meldt grønn.

[AVVIK](images/verify/AVVIK.md) · [rålogger og inndata](../../../PalazzoScaffold/docs/sicilia-gui-evidence/).

## native

MANUELL OVERLEVERING — ingen passende ferdig Palazzo-snapshot-vei funnet i Binding. Ingen native installasjon/endring/kjøring eller bilder. [NATIVE](images/verify/NATIVE.md) oppgir eksakte celler/keypaths/konfigurasjonsnavn og påpeker at katalog-/launchpublisering og riktig bridge-identitet må være på plass før en native URL kan fungere.

GUI-sluttkontroll: `swift build --disable-sandbox`, exit 0; `swift test --disable-sandbox`, exit 0, **100 tester, 0 feil** (før: 95/0). [Full GUI-rapport](../../../PalazzoScaffold/docs/Rapport_Sicilia_GUI_2026-09-07.md) · [sluttbygg](../../../PalazzoScaffold/docs/sicilia-gui-evidence/after-build.log) · [sluttest](../../../PalazzoScaffold/docs/sicilia-gui-evidence/after-test.log).
