STATUS: STOPPET — byggevakt exit 75: 51,1 GiB ledig; etter 10 GiB reserve 41,1 GiB / 4 %, krav minst 40 GiB og 5 %; head b658ef53e14dccdb12009991e78b1b44d47dac8a

Anker-fingeravtrykk: **IKKE HENTET**. Ingen nøkkelinnrullering eller signering er forsøkt.

Codex, 29.09.2026, runde 4. `PDD_sindre-import-uten-bruker_2026-09-25.F1`.
[PR #270](https://github.com/Digipomps/CellScaffold/pull/270) er OPEN på samme head som arbeidstreet. **F1 er ikke levert eller lukket. Ingen commit, push, merge, utrulling eller ny CI.**

Forrige rapport er bevart byte-identisk som [HVELV-F1-runde3-20260929.md](HVELV-F1-runde3-20260929.md). Den inneholder tidligere kildeanalyse og krav-/testmatrise. Denne runden beviser en ny kapasitetsblokkering, ikke en ny kodeleveranse.

## Beslutningen er avklart

Kjetils nye instruks «I koden via PR» erstatter forrige rundes uavklarte innrulleringsvei. Anker A er fortsatt den offentlige delen av HavenAgentD-identiteten på hans Mac, **bare for mottakerbindinger**. Algoritme, offentlig nøkkel, fullt kanonisk fingeravtrykk og formål skal kompileres inn. Ingen produksjonsvei via miljø, konfigurasjon, manifest, vault eller kommandolinje skal erstatte eller supplere det. Kjetil sammenligner med egen Mac og merger anker-PR-en; bytte krever ny PR som han merger og ny release. Dette er besluttet, **ikke implementert**. Det skal ikke spørres om A eller kodeanker på nytt.

## Hvorfor arbeidet stopper nå

Fra `CellScaffold/_wt-forvaltet-import-20260926` ble følgende kjørt uten kapasitets-overstyringer:

```sh
scripts/run_swift_bounded.sh test --disable-sandbox --filter 'ManagedArtistRecipientBindingTests|ManagedArtistImportTests'
```

```text
Build capacity: 51.1 GiB free (5%); reserving 10 GiB leaves 41.1 GiB (4%).
ERROR: build blocked: projected free space must remain at or above 40 GiB and 5%.
```

Exitkode **75**, før Swift og før den bounded cache-runneren ble startet. Etterfølgende `df -Pk` målte **53 600 000 KiB tilgjengelig** av **971 298 980 KiB**. Både absolutt gulv og prosentgulv må passere; det er prosentgulvet som blokkerer. Den faktisk kjørte, uendrede `scripts/check_build_capacity.sh` bruker 5 %, selv om eldre AGENTS-/driftsnotattekst sier 10 %. Ingen terskel ble endret eller omgått. Se [kommando og utdata](evidence-hvelv-f1-code-anchor-20260929/build-capacity.txt).

Kjetils uttrykkelige regel: «Byggevakten skal ikke omgås; blokkerer den på diskplass, rapporter målt ledig plass og stopp.» Derfor er implementering, nøkkelhenting, øvrige tester og publisering stoppet. Ingen diskopprydding er forsøkt.

## Kravstatus

Filankre nedenfor er fra den arkiverte runde-3-rapporten og ASTRA-HVELV-2 §1 / ASTRA-HVELV-4, ikke en ny full kildekontroll. Kode- og testfiler er urørt i denne runden. Ingen av testene er kjørt nå. `V` = `Sources/App/Cells/ManagedArtistImport/ManagedArtistIssuanceVault.swift`, `B` = `ManagedArtistRecipientBinding.swift` i samme mappe, `I` = `Tests/AppTests/ManagedArtistImportTests.swift`, `T` = `Tests/AppTests/ManagedArtistRecipientBindingTests.swift`.

| Bestilt krav | Fil:linje og faktisk rest | Test / ville fanget original F1? |
|---|---|---|
| 1. Uforanderlig kodeanker og test-only-injeksjon | Ingen kodeankerdefinisjon. B:137 tar fortsatt `trustedOwner` fra kalleren i utkastet. Claim har ingen forankring. | Produksjonstest for miljø/konfig/manifest/vault/CLI-overstyring mangler. **Nei**. |
| 2. Offentlig nøkkel i egen commit, fingerprint i PR | Ingen lokal offentlig descriptor hentet; ingen ankerfil eller ankercommit. PR-beskrivelsen er uendret. | Ingen test/kontroll utført. **Nei**. Fail-closed tomt anker er heller ikke implementert. |
| 3. Signering på Mac og konvoluttverifikasjon | `scripts/managed_artist_recipient.py:96` har bare utkastets `fingerprint`/`prepare`. Eksisterende HavenAgentD-route er historisk kildeankret i runde 3. | T:40 `testApprovedBindingAndExistingAgentDEnvelopeVerify` gjelder fixture-helper, ikke lokal klient/daemon. **Nei for original claim**. |
| 4. Token + ankerbinding + fersk bundet nøkkelsignatur før attestasjon | V:452/483/489/506: ingen bindingspayload/gate/forbruk. Positiv tilfeldig-peer-test er ikke rettet. | I:359 `testClaimPreservesIDsAssetsAndNeverStoresArtistsPrivateKey` godtar originalfeilen. **Nei**. |
| 5a. Feil signer, felt, scope, utløp, overstyring | B:74/84/137 har uintegrerte kontroller; ingen ny produksjonsintegrasjon. | T:48 `testEveryBoundFieldMutationInvalidatesOwnerSignature`, T:65 `testValidSignatureStillNeedsExactScopeRecipientAndShortLifetime`, T:84 `testWrongOwnerAndForgedEnvelopeRejected`. **Nei for original claim**; integrerte rolle-/overstyringsprøver mangler. |
| 5b. Replay, atomisk varig forbruk, parallelle claims og retry | V:176 mangler bindingsforbruk. V:489 kontrollerer eksisterende claimant uten eierbinding. | I:393 `testInterruptedClaimHidesBothCellsAndCanResumeSameClaimant` er samme runtime/samme peer; I:314 `testConcurrentReplayHasExactlyOneSuccessfulImport` gjelder execute. **Nei** for bestilte F1-negativer. |
| 5c. Begge private nøkler fraværende fra serverlagring | Ingen ny lagrings-/transport-/logginspeksjon med to testidentiteter. Ingen ekte private nøkler lest. | I:359/377 inspiserer kunstnerfixture alene; T:105 `testUnknownAndPrivateFieldsAreRejectedAtEveryPayloadLevel` er uintegrert helper. **Nei** for hele eier-/kunstnerkjeden. |
| 6. Nøyaktig operatørsekvens og ankerbytte | Driftsnotatet har fått kodeankerbeslutningen og faktisk stoppgrunn. Den tidligere sekvensen er fortsatt tydelig merket uferdig. | Ingen ende-til-ende-prøve. **Nei**. |

Den fullstendige tidligere testmatrisen og signeringskildene er bevart i runde-3-rapporten. F4/F5/F6/F7/F8/F9 er ikke rettet eller godkjent i denne runden. Sentral strict-kode, eksisterende avvisningstester, skips/exclusions, package-pinner og byggevakt er uendret.

## Kjetil og Sindre — hva som konkret gjenstår

Før videre F1-arbeid må maskinen ha nok kapasitet til at den uendrede byggevakten passerer. Denne jobben har ikke ryddet disk eller endret grensen. Deretter skal neste kjøring fortsette på de sju autoriserte utkastene og samme PR-head.

Etter implementering og tester skal Kjetil vise egen offentlige HavenAgentD-descriptor, sammenligne hele ankerfingeravtrykket på Mac-en med den separate ankercommiten og PR-beskrivelsen, og selv merge når gjennomgangen er ferdig. Eksakt kommando for offentlig nøkkelvisning er **ikke verifisert/levert her**: stoppet kom før route-inspeksjon og nøkkelhenting. Det er ikke bevist at offentlig henting er utilgjengelig; ingen slik konklusjon eller oppdiktet kommando gis.

Sindre skal vise sitt fulle kanoniske fingeravtrykk på egen enhet og dele bare offentlig descriptor. Kjetil sammenligner samme streng med Sindre, kontrollerer import/slug/scaffold/mottaker/utløp og signerer bindingen lokalt på Mac-en. Sindre overtar med token, offentlig binding og fersk signatur fra nøyaktig den bundne nøkkelen. Dette er kravet til den kommende klientløypen, **ikke en levert produksjonsprosedyre**. Ingen produksjonsovertakelse skal brukes som første integrasjonstest. Kjetils ekte nøkkel skal ikke brukes i testene.

## Utført, ikke kjørt og bevart arbeid

Utført: lesing av forrige F1, ASTRA-HVELV-2 §1, ASTRA-HVELV-4, FORMAALSSPEC/PLAN, driftsnotatet og relevante ferdigheter; Git-status/head/arbeidstrelås; GitHub PR-state; kilde for bounded runner og kapasitetsvakt; ett blokkert testforsøk; arkivering og denne rapporten. PR-state er lagret i [pr-state.json](evidence-hvelv-f1-code-anchor-20260929/pr-state.json), filhashene i [source-state.json](evidence-hvelv-f1-code-anchor-20260929/source-state.json).

Ikke kjørt: Swift-bygg eller noen Swift-/Python-test, `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh`, `ci/test-suite-coverage.sh`, offentlig nøkkelhenting, sign-statement, testidentitetsløype, replay-/parallelle-/restartprøver, ny privatnøkkel-lagringsinspeksjon, staging/prod/GUI. Ingen ankercommit eller annen commit/push, ingen PR-body-endring og ingen ny CI. CI-ventevinduet på 60 minutter er ikke startet; historisk grønn CI er ikke F1-bevis.

De to sporede og fem usporede F1-utkastene var autoriserte og **ikke stoppgrunn**. Ingen fremmed endring er brukt som stoppgrunn. Ingen nye testrester ble produsert av den blokkerte kjøringen. Denne runden skriver bare rapport/arkiv/evidens, et datert tillegg i driftsnotatet og den obligatoriske læringsregistreringen. Øvrig WIP er bevart.

Læringsfangst: kodeankerbeslutningen er fanget som `L-2026-09-29-kjetil-valgte-29-09-2026-et-kildekodefestet` og skrevet i driftsnotatet. Docs distribueres via Git; fordi diskstoppet hindrer leveransen, er dette fortsatt lokal dokumentasjon.

Sluttkontroll: alle 11 registrerte kode-/test-/CI-/byggfiler har uendret hash, arkivet er byte-identisk, head er uendret og `git diff --check` passerer. Se `evidence-hvelv-f1-code-anchor-20260929/final-checks.json`. Læringspostens `applied` og `sync` er gjennomført; docs-sync betyr Git-distribusjon, ikke at noe er pushet. Global `haven_learn.py check --strict` returnerte 1 fordi en annen åpen Sprout-post (`L-2026-09-29-kjetil-presiserte-at-sprout-skal-vaere-en-lett`) fortsatt venter på måloppdatering. Den fremmede posten er urørt; denne F1-postens mål er oppdatert.
