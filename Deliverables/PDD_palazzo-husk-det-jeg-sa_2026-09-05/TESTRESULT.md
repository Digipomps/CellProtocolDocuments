# TESTRESULT — «Husk det jeg sa»

Dato: 2026-09-07

## #build

PASS — `swift build --disable-sandbox` avsluttet med exit 0.

```text
[0/1] Planning build
Building for debugging...
[0/3] Write swift-version--58304C5D6DBC2206.txt
Build complete! (8.76s)
```

## #regression

PASS — den ordrette kommandoen `swift test --disable-sandbox` kjørte full suite etter endring: 82 tester, 0 feil. Baseline var 68 tester, 3 feil. De tre baseline-feilene var i én eksisterende identity-link-test og skyldtes rekursiv/ikke-skrivbar `CellsContainer`-sti; dette ble rettet med prosesslokal testrot i PalazzoScaffolds `configure.swift`, uten endring i CellProtocol.

```text
Test Suite 'PalazzoScaffoldPackageTests.xctest' passed at 2026-09-07 15:30:37.922.
	 Executed 82 tests, with 0 failures (0 unexpected) in 1.373 (1.377) seconds
Test Suite 'All tests' passed at 2026-09-07 15:30:37.922.
	 Executed 82 tests, with 0 failures (0 unexpected) in 1.373 (1.377) seconds
```

## #signal

PASS — stabile rett-/signal-ID-er, versjonering og publiserte signaler.

```text
Test Case '-[AppTests.PalazzoRememberTests testHuskSignal]' passed (0.029 seconds).
```

## #tags

PASS — deterministiske ordlisteforslag, normalisering, godkjenning, skip og redigering; tom godkjenning avvises.

```text
Test Case '-[AppTests.PalazzoRememberTests testHuskTags]' passed (0.000 seconds).
```

## #match

PASS — én-lags matcher bak `PalazzoSignalMatcher`, kun egenregistrerte interaction-poster og bokstavelig tagg/ord-overlapp.

```text
Test Case '-[AppTests.PalazzoRememberTests testHuskMatch]' passed (0.000 seconds).
```

## #explanation

PASS — forklaringen bruker gjestens egne ord og deterministisk norsk datomal.

```text
Test Case '-[AppTests.PalazzoRememberTests testHuskExplanation]' passed (0.000 seconds).
```

## #grants

PASS — separate gjesteutstedte innsyns- og handlingsgrants, konkret match-keypath og standing-innsyn for neste signal av samme type.

```text
Test Case '-[AppTests.PalazzoRememberTests testHuskGrants]' passed (0.092 seconds).
Test Case '-[AppTests.PalazzoRememberTests testHuskStandingInsightAppliesToNextMenuChange]' passed (0.050 seconds).
```

## #trust-packet

PASS — uttømmende allowlist, kanonisk signering, provenance-hash og negativ manipuleringstest.

```text
Test Case '-[AppTests.PalazzoRememberTests testHuskTrustPacketTamperFails]' passed (0.003 seconds).
```

## #house

PASS — huset godtar bare verifisert pakke fra gjestens identitet; staff-brief avledes fra lagret minimalpost. Den gamle `insight.query.interests.match` returnerer bevisst bare `schema`, `query`, `status:"deprecated"` og `replacedBy:"match.*"`.

```text
Test Case '-[AppTests.PalazzoRememberTests testHuskHouseEndpoint]' passed (0.038 seconds).
Test Case '-[AppTests.PalazzoRememberTests testHuskLegacyMatchEndpointIsDeprecated]' passed (0.007 seconds).
```

## #no-label-leak

PASS — husets lagring og respons inneholder ikke `sourceRecordID`, `attributes`, `interests`, `matches`, `score` eller `tags`.

```text
Test Case '-[AppTests.PalazzoRememberTests testHuskNoLabelLeak]' passed (0.000 seconds).
```

## #revoke

PASS — tilbakekalling fjerner husets pakke og stenger tidligere avtaletilgang.

```text
Test Case '-[AppTests.PalazzoRememberTests testHuskRevoke]' passed (0.043 seconds).
```

## #no-inference

PASS — house/staff-kilder, feil record-kind og manglende bokstavelig overlapp gir ingen treff; ingen språkmodell brukes.

```text
Test Case '-[AppTests.PalazzoRememberTests testHuskNoInference]' passed (0.000 seconds).
```

## #e2e

PASS i Vapor/HTTP-testharnessen — registrer egen interaction → draft Chambre → godkjenn tagger → publish → refresh → innsyn+handling → pakke hos hus → remembered-linje hos staff → revoke → tomt.

```text
Test Case '-[AppTests.PalazzoRememberTests testHuskE2E]' passed (0.084 seconds).
```

## #auth

PASS — husets action uten action-grant og lesing av gjestens private match-kø blir `403 Forbidden`; samme action blir tilgjengelig etter eksplisitt grant. Nye handlere validerer den konkrete keypathen de betjener.

```text
Test Case '-[AppTests.PalazzoRememberTests testHuskGrants]' passed (0.092 seconds).
```

## #deploy

blocked: sandboxen nekter tilkobling til brukerens Docker-daemon-socket før imagebygging eller appstart. Compose-konfigurasjonen ble validert med lokal, ikke-produksjons tokenverdi; `docker compose --profile staging up`, container-GET og container-e2e kunne derfor ikke kjøres. Ingen omgåelse og ingen prod-push ble forsøkt.

```text
permission denied while trying to connect to the Docker daemon socket at unix:///Users/kjetil/.docker/run/docker.sock: Head "http://%2FUsers%2Fkjetil%2F.docker%2Frun%2Fdocker.sock/_ping": dial unix /Users/kjetil/.docker/run/docker.sock: connect: operation not permitted
```
