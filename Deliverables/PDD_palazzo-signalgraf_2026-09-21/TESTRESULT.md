> Oppdatert sluttstatus finnes i «Sluttport 2026-09-22 — natt1b» nederst. Resten dokumenterer natt1 historisk.

# TESTRESULT — Palazzo signalgraf 2026-09-21

Verifisert 21.–22.09.2026 i `PalazzoScaffold`, gren `pdd/palazzo-2026-09-14`.
S0-commit: `516e2d2ee6e446d08174a9d642f5eea12cdd051d`.
Sluttkode og dokumentasjon ligger i arbeidstreet; ingen push eller deploy.
CellProtocol-pin: `b5b7282b495e96a7899a189087592581426f4bfb`.

Alle evidensfiler nedenfor ligger i `PalazzoScaffold/docs/signalgraf-evidence/`.
App-kontrakten står i `PalazzoScaffold/docs/Signalgraf_2026-09-21.md`.

## build

Kommando: `swift build --disable-sandbox`, med
`CELLPROTOCOL_LOCAL_PACKAGE_PATH=/private/tmp/palazzo-signalgraf-20260921/CellProtocol`.
Dette er et uendret `git archive`-uttrekk av den eksakte CI-pinnen. Søskenrepoene
CellProtocol, CellScaffold og Binding er ikke endret.

Rå avslutning, før:

```text
Build complete! (64,96 sek)
```

Rå avslutning, etter:

```text
Build complete! (1,39 sek)
```

Begge exit 0. Fullt: `baseline-build.txt`, `final-build.txt`.
`Package.resolved` fikk swift-crypto 4.5.2 fordi CI-pinnens manifest krever
`from: "4.5.2"`; den gamle lockfilen hadde 3.15.1.

## regression

Kommando: `swift test --disable-sandbox`. Separate midlertidige test-vaults via
`CELL_VAULT_DOCUMENT_ROOT`; ingen språkmodell eller ekstern matchetjeneste.

Før, rå XCTest-sammendrag:

```text
Executed 127 tests, with 8 failures (1 unexpected) in 23.092 (23.100) seconds
```

Tre røde tester, åtte feilregistreringer:

- `PalazzoBridgeheadTests.testBridgeheadGuestVsHouse`: `Guest must receive guest.configuration`.
- `PalazzoBridgeheadTests.testBridgeheadReaction`: `Abort.408: No bridge WebSocket frame within five seconds`.
- `PalazzoG5SeedDryRunTests.testG5SeedAgainstXCTVapor`: seks assertions; Python-prosessen exit 126,
  `env: python3: Bad CPU type in executable`.

G5 kjøres uendret med `PATH=/usr/bin:/bin:/usr/sbin:/sbin`; dette velger systemets
Python, ikke Intel-programmet i `/usr/local/bin/python3`. Ingen assertions er fjernet.

Etter, rå XCTest-sammendrag:

```text
Executed 142 tests, with 2 failures (1 unexpected) in 34.199 (34.206) seconds
```

140 grønne, bare de samme to bro-testene røde. Begge hele testkommandoene exit 1.
Ingen nye skip. Den forbudte brotesten beholder også sin gamle `kind == purpose`-assertion;
en fremtidig brorettelse vil måtte håndtere denne eksplisitte kontraktendringen separat. Alle 15 nye signalgraftester består. G5 består.
Fullt: `baseline-test.txt`, `final-test.txt`. Delkjøringer: `slice-test-results.txt`.

De eksisterende matchertestene er beholdt og omskrevet til grafmotoren. Sicilia-
testene beholder innhold/proveniens/tilgang/persistens-assertions og tester det
uttrykkelig godkjente semantikkskiftet: «Vil smake» er interesse, ikke hensikt.
Ingen endring av bro-testene etter S0-commiten.

## graf

`testGraphReplaysWeightsProvenanceAndLegacyIntentDeterministically` verifiserer
CellProtocol-typer, 1.0/0.8/0.5/-1.0, kildefilter, historisk `wantToTaste`,
kantproveniens, deterministisk rebuild og replay etter record-Codable.
Grafen er avledet fra postene og persisteres dessuten som `derivedGraphCache`.
`testPinnedCodableCacheRoundTripsWeightedGraphWithPublicFacilitators` beviser
ordinær JSONEncoder/JSONDecoder-roundtrip med offentlige `Facilitator`-typer,
like vekter, motorhits og deterministisk cache. Ingen direkte kodekbruk;
lasting gjenbygger alltid fra de autoritative postene.

`testGraphAndInsightProjectionsUseTheSamePrivateGraph` og
`testActionPromotesInterestAndOwnerFulfilmentReplays` laster faktisk cellefil
med `TypedCellUtility`/`LargeStackCellStorage` og sammenligner eierens graf.

## match

- `testSiciliaReactionGivesMatch`: virkelige HTTP-ruter; «Vil smake» på godkjent
  pistasjartikkel gir nøyaktig ett treffkort for pistasjretten.
- `testMatcherUsesTwoHopsForReactionsPurposesAndWrittenWords`: direkte
  `WeightedGraphRuntime`-bevis med depth=2, og adapterens reaksjoner/formål/egne ord.
- `testNegativeAndExhaustedBudgetsAreNotPositive`: negativ forrang, TTL=0,
  hops=1 og maxHits=1 gir aldri positiv dom; irrelevant tagg gir intet treff.
- `testWrittenInterestAndPurposeTitlesMatchWithoutInventingGuestQuotes`:
  egenskrevne titler matcher; generert Purpose får en handlingsforklaring.
- `testDuplicateRecordIDsKeepExactProvenanceThroughGrantAndPromotion`:
  to poster med id=same og ulike tagger gir korrekt kildehash for sitron-treffet,
  én promoteringskant til riktig interesse, og tvetydig gammel kilde avvises.
- Alle 14 `PalazzoRememberTests` består med den ene nye motoren.

## negativ

`testNegativeJudgmentOnlyFiltersThisGuestsSurfaceWithoutEvents` bruker to gjester,
virkelige celle-/HTTP-kall og abonnement på privat feed, husets feed og innholdsfeed.
Eksplisitt reaksjon og huspublisering er positive kontroller med venting på faktisk
asynkron levering. Etter dom/lesing/refresh er husets hendelseslogg, `content.signals`,
`content.published`, private poster og private hendelser uendret. Bare riktig
persons meny/artikler filtreres; direkte artikkelåpning avvises.

`testNegativeUntaggedArticleIsHiddenOnlyForItsGuest` dekker også publisering uten
godkjente tagger: bare reagerende gjest mister liste/åpning, huset er uendret.

`testNewNegativePreferenceBlocksAnOlderPositiveMatchGrant` tester at både ny
innsyns- og handling-grant avvises etter negativ reaksjon.

## hensikt

`testActionPromotesInterestAndOwnerFulfilmentReplays` verifiserer interesse før
handling, ingen forfremmelse ved bare innsyn, nøyaktig én Purpose ved handling,
bevart originalpost, vektet kobling til interessen, måltekst, idempotent eierstyrt
oppfyllelse, faktisk disklasting og fravær av ny anbefaling av samme valgte innhold.

Avvik: `Purpose.goal` er `nil`. Måltekst og oppfyllelse er Palazzo-tilstand med
append-only proveniens. Oppfyllelse er gjestens egen attestasjon. Ingen gjesteknyttet
bestillings-/serveringshendelse finnes i dag; `entity.purpose.fulfil` er fallbacken.

## projeksjon

`testGraphAndInsightProjectionsUseTheSamePrivateGraph` kontrollerer de eksakte
svarnøklene for `insight.interests`/`avoid`/`insight.purposes` og likhet med grafens
projeksjoner, samt `entity.graph` etter disklasting. Alle 13 Sicilia-tester og fem
Sicilia-GUI-kontrakttester består; toprosess-E2E/replay er beholdt.

Den samlede relevante delkjøringen hadde 58 tester, null feil (se `review-regression.txt`). Appens Explore-audit:

```json
{"completeContracts":103,"errors":0,"handlerOperations":103,"warnings":0}
```

Kommando: `/usr/bin/python3 ../CellProtocolDocuments/Tools/Explore/explore_contract_audit.py --repo-root . --source-dir Sources/App --json-output docs/signalgraf-evidence/explore-audit.json --markdown-output docs/signalgraf-evidence/explore-audit.md --fail-on-error`.

Ingen visuell Porthole-/Binding-kjøring er utført; denne leveransen verifiserer
Swift-konfigurasjonens bindinger og de virkelige data-/handlingsbanene.

## auth

- `testGraphAuthRejectsWrongRequester`: huset og en annen gjest får ikke lese
  grafen eller oppfylle formål i den første gjestens entitet.
- `testGraphAuthRejectsGrantOnWrongKeypath`: reell signert tilgang til
  `insight.interests` virker, men gir ikke `entity.graph` eller `entity.purpose.fulfil`.
- `testFulfilRejectsUnknownPurposeAndAnInterest`: ukjent ID, Interest-ID og tom
  payload avvises uten append.

Begge nye keypaths kaller `validateAccess` og krever eierskap; de har eksplisitte
Explore-kontrakter. Ingen ny utskrift av gjestedata, felles personnode eller no-op-handler.

## push-port

`HAVEN-Deploy/_handoff/HD-0077/KJETIL-SVAR-BRO-TESTER.md` finnes ikke ved S7-kontroll.
Handoff §6 krever derfor stopp uten push. Ingen `XCTSkip`, endring av bro-testene,
imagepublisering eller S8-deploy er utført.


## Sluttport 2026-09-22 — natt1b

Dette tillegget oppdaterer statusen over; natt1s rå før-/etterutdata er beholdt.
S6b er løst i CellProtocol [PR #43](https://github.com/Digipomps/CellProtocol/pull/43),
merget som `0f688b57e6e976482c2c045bed2cf13040a2fad2` etter fem grønne CI-kontroller.
`CELLPROTOCOL_REF_DEFAULT` er oppdatert til denne SHA-en. Sluttport følger
oppdatert handoff §6 og brukerens direkte bestilling; ingen svarfil er nødvendig.

```text
Build complete! (4,90 sek)
Executed 145 tests, with 0 failures (0 unexpected) in 5.892 (5.899) seconds
```

Begge kommandoer exit 0, null skip i Palazzo. Rålogger: PalazzoScaffold/docs/bro-evidence/final-build.txt
og final-test.txt. Explore-audit: 103 handlere/komplette kontrakter, null feil/advarsler.

Desktop-reviewets alle konkrete funn er verifisert, inkludert artikkelavvisning
etter tagging/omtagging og gamle kort som ikke lenger kan få noen av de to grants.
S4s Interest-forventning gjelder også brotesten; alle tidligere sikkerhets-,
persistens- og HTTP-paritetsassertions er beholdt. Ny brotest avviser huset og
kopiert gjesteidentitet ved lesing av gjestens poster og graf.

CellProtocol: 63 målrettede tester grønt, ingen skip. Full CI: 1193 tester, null
feil og ett eksisterende skip for manglende lydreferanse. Den lokale fulle
CP-kjøringen hadde tre sandbox-Keychain-feil og åtte eksisterende skip; dette
er holdt atskilt fra CI-resultatet. Ingen skip er innført som rettelse.

Full årsak, filstier, kode-SHA og pushkvittering står i
`PalazzoScaffold/docs/Rapport_Bro_2026-09-21.md`. S8 er fortsatt natt2s jobb.
