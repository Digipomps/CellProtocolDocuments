# TESTRESULT — entitetsdata egen kontroll

Runde 1 (WP1 genesis, WP2 herdinger). Kjørt 2026-09-22 på Kjetils Mac i worktreet
`~/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata`, gren `pdd/entitetsdata-egen-kontroll`
fra `origin/main` 473357c, commit `ebb0b7f`. Rå logger ligger i `handoff/runde1/verify-*.log`.
Tallene under er kopiert fra loggene, ikke skrevet fra hukommelsen.

## #build

**CellProtocol** (worktreet, gren `pdd/entitetsdata-egen-kontroll`, commit `e66b7f1` — tabellen under sa `ebb0b7f`, se rettelse 24.09 — på `origin/main` 473357c):
`swift build` → **Build: OK**. Hele `CellBaseTests` → **1244 tester, 0 feil** (1 hoppet over, som før).

**Nedstrøms**, bygget i rene worktrees under `~/Build/pdd-check/` med CellProtocol pekt lokalt, først
med CellProtocol @ `origin/main` (baseline) og så @ `ebb0b7f` (endringen). Logg:
`handoff/runde1/downstream-20260922-172908.log` og `-171950.log`.

| Prosjekt | Baseline (CellProtocol @ main) | Endringen (@ ebb0b7f) | Skyldes runde 1? |
|---|---|---|---|
| CellScaffold @ main | **rød** — kan ikke løse avhengigheter: `cellprotocol` krever swift-crypto 4.5.2..<5.0.0, `dimymint` (pinnet 1718fda) krever 3.0.0..<4.0.0 | rød, samme feil | **Nei.** Identisk uten patchen. DiMyMint må bumpe swift-crypto før CellScaffold main kan bygge mot CellProtocol main. |
| Binding @ main | **rød** — `switch must be exhaustive` i `SkeletonEditor/SkeletonElementParameterCatalog.swift:1293`, `SkeletonTreeMutations.swift:161`, `SkeletonTreeQueries.swift:18,53` | rød, nøyaktig samme fire linjer | **Nei.** CellProtocol #44 la til `Tree` og `ComponentSurface`; Binding main sin skjeletteditor har ikke fått de nye casene. Det er filene en annen tråd allerede har ucommittet. |

Runde 1 legger ikke til noe nedstrøms må håndtere: ingen nye caser i eksisterende enum-er,
ingen endrede signaturer. De to nye typene (`EntityGenesisTrigger`, `EntityGenesisError`) brukes
ikke nedstrøms. Så «kompiler i prosjektene som bruker det» ga et ærlig svar: **prosjektene ligger
bak CellProtocol main av grunner som ikke har med denne runden å gjøre.** Det står her fordi det er
sant, ikke fordi det er behagelig.

Første kjøring av nedstrøms-skriptet var ugyldig og er forkastet: `/usr/local/bin/python3` er en
x86-binær uten Rosetta («Bad CPU type»), så pbxproj-byttet til lokal pakke skjedde ikke og Binding
bygde mot GitHub-pinnen sin (b5b7282) — «BUILD SUCCEEDED» der sa ingenting om endringen. Skriptet
bruker nå `/usr/bin/perl`, og logger om byttet faktisk skjedde.

### #build — oppdatert 2026-09-24: alt grønt, og branchen er pushet

Kjetil 24.09: «Fiks det som blokker. Er ikke pdd/entitetsdata-egen-kontroll pushet så må den det.»

**Tre rettelser til tabellen over, alle målt på nytt (logger i `handoff/runde1/`):**

1. **Commiten var `e66b7f1`, ikke `ebb0b7f`.** `commit.sh` laget en ny commit-hash; tabellen over
   siterer den gamle. Branchen var *ikke* pushet (ingen remote-tracking ref).
2. **CellScaffold-rød var skriptets feil, ikke prosjektets.** `downstream.sh` hardkodet DiMyMint
   `1718fda` (swift-crypto 3.x). CellScaffold main pinner `af41630`, som løser swift-crypto 4.5.2 —
   `Package.resolved` på origin/main sier det. Skriptet leser nå pinnene fra CellScaffold sin egen
   `Package.swift`. Med riktig pin: **Build complete** mot CellProtocol main (172 s) og mot branchen.
   Lærdom: `lesson.downstream-pin-must-come-from-the-consumer`.
3. **Binding-rød var to ting oppå hverandre.** (a) pdd-check-worktreet satt fast på `72f6a6c9` fordi
   pbxproj-byttet fra forrige kjøring blokkerte `checkout` — skriptet gjør nå `reset --hard` og fjerner
   `Package.resolved` før byttet. (b) Mot Binding `8ce634f6` manglet branchen typene fra CellProtocol
   #45 (`DatabaseOwnerApprovalPackage`, `AppleDatabaseSecretHandle`) fordi den sto på 473357c.
   `sync-main.sh` flettet origin/main (60bcf1d) inn: rent merge, `swift build` OK, runde 1-testene
   16/16, hele CellBaseTests **1248 tester, 0 feil** (2 hoppet over), pushet som `94a4bed`.

| Prosjekt | Baseline (CellProtocol @ main 60bcf1d) | Endringen (@ 94a4bed) | Logg |
|---|---|---|---|
| CellProtocol | — | Build OK · 16/16 runde 1 · **1248/1248** CellBaseTests | `sync-20260924-133148.log`, `.full.log.alle` |
| CellScaffold @ 6c70a592 (DiMyMint af41630, Micro 836ba8e) | **Build complete** (75,6 s) | **Build complete** (78,6 s) | `downstream-20260924-134224.log` |
| Binding @ 8ce634f6 | **BUILD SUCCEEDED** | **BUILD SUCCEEDED** | samme |

Pushet: `origin/pdd/entitetsdata-egen-kontroll` = `94a4bed` (e66b7f1 + merge av main). Utkast-PR
[#47](https://github.com/Digipomps/CellProtocol/pull/47) er åpnet for CI — ikke merget; det er
Kjetils ord. `push-20260924-131712.log`. De fire «switch must be exhaustive» fra 22.09 er borte på
Binding main 8ce634f6 — de var Binding `72f6a6c9` sin sak, ikke CellProtocol sin, og de ucommitterte
SkeletonEditor-filene i Kjetils utsjekk er ikke rørt.

## #genesis

`test.entitet.genesis-once` og `test.entitet.no-refounding`.

| Suite | Test | Resultat | Tid |
|---|---|---|---|
| `EntityAnchorGenesisTests` | `testAnchorStartsUnsealed` | grønn | 0.002 s |
| `EntityAnchorGenesisTests` | `testExplicitGenesisSealsAnchorToOwner` | grønn | 0.003 s |
| `EntityAnchorGenesisTests` | `testGenesisCannotBeRevokedOrOverwritten` | grønn | 0.004 s |
| `EntityAnchorGenesisTests` | `testGenesisRecordWithoutValidSealIsNotHonoured` | grønn | 0.003 s |
| `EntityAnchorGenesisTests` | `testPairwiseLinkDoesNotOpenTheAnchor` | grønn | 0.004 s |
| `EntityAnchorGenesisTests` | `testSecondGenesisIsRefused` | grønn | 0.004 s |
| `EntityGenesisTests` | `testGenesisKeypathsAreRecognisedAsImmutable` | grønn | 0.000 s |
| `EntityGenesisTests` | `testGenesisSealsToInitiatorAndVerifies` | grønn | 0.001 s |
| `EntityGenesisTests` | `testInitiatorWithoutSigningKeyCannotSeal` | grønn | 0.000 s |
| `EntityGenesisTests` | `testPairwiseRecordIsRejected` | grønn | 0.000 s |
| `EntityGenesisTests` | `testSealDoesNotVerifyAgainstAnotherIdentitysRecord` | grønn | 0.001 s |
| `EntityGenesisTests` | `testTamperedSealFailsVerification` | grønn | 0.000 s |

**Blokkert, med vilje synlig:** forsegling ved første `batchPersist` er implementert
(`persistBatchEnvelope`, begge ankrene) men **ikke testet**. Batch-veien er en feed-intercept som bare
kjører når ankeret absorberer en annen celles flow gjennom auditoren; `GeneralCell.intercepts` er
privat. Runde 2 bygger den harnessen. Status for den halvparten av `genesis-once`: **blocked**.

## #auth

`test.entitet.linked-identity-accepted` og `test.entitet.foreign-entity-refused`.

| Suite | Test | Resultat | Tid |
|---|---|---|---|
| `EntityAnchorGenesisTests` | `testGenesisRecordWithoutValidSealIsNotHonoured` | grønn | 0.003 s |
| `EntityAnchorGenesisTests` | `testIdentityFromAnotherEntityIsRefused` | grønn | 0.003 s |
| `EntityAnchorGenesisTests` | `testLinkedIdentityWithoutKeyControlIsRefused` | grønn | 0.004 s |
| `EntityAnchorGenesisTests` | `testLinkedSecondIdentityReadsAndWrites` | grønn | 0.006 s |
| `EntityAnchorGenesisTests` | `testPairwiseLinkDoesNotOpenTheAnchor` | grønn | 0.004 s |
| `IdentityLinkRegistryBindingTests` | `testOnlyLocalEntityAnchorBindingOpensTheEntity` | grønn | 0.000 s |

Merk: selve resolveren (`IdentityLinkRegistry` + `GeneralCell.authorizationEvidence`) var allerede
på main fra en annen oppgave. Det denne runden la til er bindingskravet og seglkravet — se PLAN WP2.

## #regression

Eksisterende autorisasjons- og identitetstester, uendret:

| Suite | Test | Resultat | Tid |
|---|---|---|---|
| `CellRuntimeReadinessContractTests` | `testAdvertisedCellAndAgreementRedactRuntimeIdentityMetadata` | grønn | 0.010 s |
| `CellRuntimeReadinessContractTests` | `testAdvertisePropagatesReadinessFailureInsteadOfPublishingEmptyCell` | grønn | 0.001 s |
| `CellRuntimeReadinessContractTests` | `testAppleAndVaporDecodedCellsAreImmediatelyAndConcurrentlyReady` | grønn | 0.036 s |
| `CellRuntimeReadinessContractTests` | `testAppleEntityAnchorAndOrchestratorDispatchAfterStrictDecode` | grønn | 0.012 s |
| `CellRuntimeReadinessContractTests` | `testAsyncCellJSONDecoderReturnsPreparedCell` | grønn | 0.009 s |
| `CellRuntimeReadinessContractTests` | `testCellBaseDecodedCellsAreImmediatelyAndConcurrentlyReady` | grønn | 0.027 s |
| `CellRuntimeReadinessContractTests` | `testInertBridgeOperationsFailClosedWithTypedErrors` | grønn | 0.001 s |
| `CellRuntimeReadinessContractTests` | `testMalformedPersistedAgreementFailsDecodeWithoutCrashing` | grønn | 0.001 s |
| `CellRuntimeReadinessContractTests` | `testPersistedOwnerRuntimeBindingRequiresSameKeyControl` | grønn | 0.001 s |
| `CellRuntimeReadinessContractTests` | `testPreviouslyFatalPublicPathsFailClosedWithoutCrashing` | grønn | 0.001 s |
| `CellRuntimeReadinessContractTests` | `testRawInterceptCellsPublishCompleteContractsBeforeHandlersInStrictMode` | grønn | 0.006 s |
| `CellRuntimeReadinessContractTests` | `testRuntimeBindingPrivilegeExpiresBeforeEscapedChildTaskRuns` | grønn | 0.000 s |
| `CellRuntimeReadinessContractTests` | `testRuntimeBindingPrivilegeInstallsUnsignedFreshOwnerHandlersOnlyInsideTokenScope` | grønn | 0.000 s |
| `CellRuntimeReadinessContractTests` | `testRuntimeBindingPrivilegeIsInstanceBound` | grønn | 0.000 s |
| `CellRuntimeReadinessContractTests` | `testSourceBackedReadinessPreservesCorruptFilesAndFails` | grønn | 0.003 s |
| `CellRuntimeReadinessContractTests` | `testVerifiedRuntimeOwnerRemainsPendingUntilMatchingRequesterIsBound` | grønn | 0.001 s |
| `EntityAnchorEncryptionTests` | `testAppleSnapshotAndJournalEncryptionRestartAndLegacyMigration` | grønn | 0.021 s |
| `EntityAnchorEncryptionTests` | `testSharedCodecRejectsMissingWrongKeyAndCrossFileSubstitution` | grønn | 0.000 s |
| `EntityAnchorEncryptionTests` | `testVaporSnapshotAndJournalEncryptionRestartAndLegacyMigration` | grønn | 0.017 s |
| `EntityAuthorityCommitTests` | `testAuthorityCommitIsSignedHashChainedAndIdempotent` | grønn | 0.002 s |
| `EntityAuthorityCommitTests` | `testInterruptedSnapshotWriteRecoversFromPersistedJournalAfterRestart` | grønn | 0.003 s |
| `EntityAuthorityCommitTests` | `testJournalTamperingIsDetectedAndReplayRebuildsCommittedValues` | grønn | 0.002 s |
| `EntityAuthorityCommitTests` | `testLegacyBatchEnvelopeWireShapeRemainsCompatible` | grønn | 0.000 s |
| `EntityAuthorityCommitTests` | `testMutationIDCannotBeReboundToDifferentPayload` | grønn | 0.001 s |
| `EntityAuthorityCommitTests` | `testReplayRangeIsCompleteOnlyWhenContiguousAndReceiptVerified` | grønn | 0.004 s |
| `EntityAuthorityCommitTests` | `testReplicaQuorumCountsOnlyAuthorizedUniqueDurableFaultDomains` | grønn | 0.017 s |
| `EntityAuthorityCommitTests` | `testStaleRevisionAndUnavailableQuorumDoNotMutateJournal` | grønn | 0.002 s |
| `IdentityLinkRegistryTests` | `testLinkedIdentityReadsAsOwnerAndRevocationDeniesAgain` | grønn | 0.010 s |
| `IdentityLinkRegistryTests` | `testScopeAndDomainFailClosed` | grønn | 0.010 s |
| `IdentityLinkRegistryTests` | `testServerCannotMintLinkWhenPolicyRequiresFreshAuthEvidence` | grønn | 0.003 s |
| `IdentityLinkRegistryTests` | `testStolenLinkRecordWithoutKeyControlIsDenied` | grønn | 0.004 s |
| `IdentityLinkingModelsTests` | `testChatCryptoSuiteRequiresAgilityMetadata` | grønn | 0.000 s |
| `IdentityLinkingModelsTests` | `testContentCryptoPolicyDefaultsToExplicitSuiteSelection` | grønn | 0.000 s |
| `IdentityLinkingModelsTests` | `testEnrollmentApprovalCanonicalPayloadExcludesProof` | grønn | 0.000 s |
| `IdentityLinkingModelsTests` | `testEnrollmentRequestCanonicalPayloadExcludesProof` | grønn | 0.000 s |
| `IdentityLinkingModelsTests` | `testFreshAuthEvidenceChallengeMustMatchRequestHash` | grønn | 0.004 s |
| `IdentityLinkingModelsTests` | `testFreshAuthEvidenceIsRequiredWhenPolicyDemandsIt` | grønn | 0.003 s |
| `IdentityLinkingModelsTests` | `testFreshAuthEvidenceVerifierDecides` | grønn | 0.005 s |
| `IdentityLinkingModelsTests` | `testIdentityLinkCompletionAcceptsBoundCredentialAndRejectsReplay` | grønn | 0.004 s |
| `IdentityLinkingModelsTests` | `testIdentityLinkCompletionRejectsAudienceMismatch` | grønn | 0.003 s |
| `IdentityLinkingModelsTests` | `testIdentityLinkCompletionRejectsHolderKeySubstitution` | grønn | 0.004 s |
| `IdentityLinkingModelsTests` | `testIdentityLinkCompletionRejectsSameKeyOnBothSides` | grønn | 0.003 s |
| `IdentityLinkingModelsTests` | `testIdentityLinkCompletionRejectsWrongPresentationChallenge` | grønn | 0.004 s |
| `IdentityLinkingModelsTests` | `testSameEntityCredentialSubjectRoundTrips` | grønn | 0.000 s |
| `IdentityLinkingModelsTests` | `testSASWordsAreDeterministicFourWordsFromWordList` | grønn | 0.000 s |
| `TrustedIssuerCellTests` | `testDecodedTrustedIssuerAwaitsSingleRuntimeInstallAndSerializesConcurrentState` | grønn | 0.030 s |
| `TrustedIssuerCellTests` | `testEvaluationCachesAreBoundedAndColdRestoreCanonicalizesPersistedKeys` | grønn | 0.954 s |
| `TrustedIssuerCellTests` | `testEvaluationIdentifiersAreSizeBoundedAndSnapshotUsesCanonicalSHA256` | grønn | 0.016 s |
| `TrustedIssuerCellTests` | `testIssuerAndAttestationSourceTrustStayWithinActiveContexts` | grønn | 0.018 s |
| `TrustedIssuerCellTests` | `testProvedClaimConditionUsesTrustedIssuerEvaluation` | grønn | 0.019 s |
| `TrustedIssuerCellTests` | `testProvedClaimRejectsUUIDOnlyAndSameUUIDWrongKeySubjects` | grønn | 0.003 s |
| `TrustedIssuerCellTests` | `testTargetOwnerSignatureIsNotImplicitCredentialTrust` | grønn | 0.002 s |
| `TrustedIssuerCellTests` | `testTrustedIssuerCellEvaluateReturnsTrustedForValidCredential` | grønn | 0.003 s |
| `TrustedIssuerCellTests` | `testTrustedIssuerEvaluationRejectsStaleFutureUnsignedStatusAndWrongCallerProofs` | grønn | 0.013 s |
| `TrustedIssuerCellTests` | `testTrustedIssuerRejectsUnsupportedDidMethodsAndAdvertisesImplementedSet` | grønn | 0.001 s |
| `TrustedIssuerCellTests` | `testVCClaimInitializerBindsSubjectToProvidedIdentityKey` | grønn | 0.001 s |
| `VaporCellRuntimeReadinessContractTests` | `testVaporDecodedCellsAreImmediatelyAndConcurrentlyReady` | grønn | 0.006 s |
| `VaporCellRuntimeReadinessContractTests` | `testVaporEntityAnchorAndOrchestratorDispatchAfterStrictDecode` | grønn | 0.009 s |
| `VaporCellRuntimeReadinessContractTests` | `testVaporEntityAnchorPersistsVerifiedContractAndRejectsImmutableConflict` | grønn | 0.031 s |

Hele `CellBaseTests`: **Executed 1244 tests, with 1 test skipped and 0 failures (0 unexpected) in 131.507 (131.567) seconds**

## Hva som gikk galt underveis, og hvorfor det står her

1. **Patchen passet ikke mot `origin/main`.** Jeg hadde lest kildene fra den lokale grenen
   `pdd/tillitspakke-agentflaate`, som lå 70–100 linjer bak main i akkurat disse filene.
   `lesson.local-main-is-not-main`, en gang til.
2. **Main hadde allerede resolveren.** Den parallelle `EntityLinkAuthorizer`-en min ble forkastet
   før den nådde en commit. Ny lærdom under.
3. **`journalCorrupt("missingMasterKey")`.** Main krypterer entitetsdata i ro; testharnessen må sette
   `CellBase.persistedCellMasterKey`. To runder gikk med før feilmeldingen ble synlig — testen
   sammenlignet bare `status`. Rettet: hjelperen `expectOK` viser meldingen.
4. **`try XCTUnwrap(await …)`** kompilerer ikke. Sju forekomster, én årsak.

## #runde2 — WP3–WP5 (2026-09-26)

Branch `pdd/entitetsdata-runde2` = `d9bd69f` (399f6d2 + fix), fra origin/main 33ad8d7 (etter #47).
Utkast-PR [#50](https://github.com/Digipomps/CellProtocol/pull/50). Logger: `handoff/runde2/`.
Alle tester kjører **to ganger**: mot `CellApple.EntityAnchorCell` (appen — personlig scaffold) og
`CellVapor.EntityAnchorCell` (skyscaffold). Ett svar på begge (FORMAALSSPEC §2A.1).

| testRef | Test | Apple | Vapor | Bevis |
|---|---|---|---|---|
| `test.entitet.read-without-proof-refused` | `testReadWithoutProofRefused` — person, relations, proofs, agreements, identityLinks, chronicle, trace: eier leser; annen entitet nektes; nøkkelløs kopi av eierens deskriptor nektes | ✓ | ✓ | `fix1-20260926-024311.full.log.new` |
| `test.entitet.auth-negative` (1/5 feil identitet) | `testWrongIdentityCannotWriteOrAct` — skriving til person/relations, handlingene genesis/revoke/reloadStorage | ✓ | ✓ | samme |
| `test.entitet.auth-negative` (2/5 usignert forslag) | `testUnsignedProposalIsRefused` — signatur nullet ut → `request_signature_invalid`; ingenting skrevet, ingen sporpost | ✓ | ✓ | samme |
| `test.entitet.auth-negative` (3/5 revokert modell) | — | **blocked** | **blocked** | Modelltillit er WP12 (runde 4). Finnes ikke å revokere ennå. |
| `test.entitet.auth-negative` (4/5 ukjent formål) | `testUnknownPurposeFailsClosed` — `purpose://prompt.unknown` i signert commit og i løs metadata → `failed`, ingenting skrevet | ✓ | ✓ | samme |
| `test.entitet.auth-negative` (5/5 direkte skriving utenom batch) | `testDirectWriteOutsideBatchPathRequiresOwnerProof` — fremmed kan verken `attach` eller `absorbFlow`; eierens egen direkte skriving går, og etterlater én sporpost | ✓ | ✓ | samme |
| `test.entitet.admin-cannot-enter-foreign-cell` | `testScaffoldAdminCannotEnterForeignCell` — identiteten prosessen kjører som (eier av admin-planet) nektes lesing av 10 keypaths, skriving, genesis/revoke/reloadStorage, attach og absorbFlow; `debugValidateAccessForEverything` bekreftet av | ✓ | ✓ | samme |
| `test.entitet.agreement-grants-exactly-what-it-says` | `testAgreementGrantsExactlyWhatItSays` — avtale «r--- person» gir B lesing av person (`signedContract`), ikke relations/identityLinks, ikke skriving, ikke handlinger; B sin andre identitet arver ingenting | ✓ | ✓ | samme |
| `test.entitet.genesis-once` (første persist) | `testFirstPersistSealsAnchorToOwner` — batchPersist gjennom eierens feed forsegler ankeret, `trigger: firstPersist`. **Var blocked i runde 1.** | ✓ | ✓ | samme |
| `test.entitet.trace` | `testEachAcceptedBatchLeavesOneTraceEntry` — én post per batch (to felt = én post), signert-av, nøkkelfingeravtrykk, keypaths, purposeRef, modelRef, kvittering (entryHash + signatur som verifiserer); idempotent replay gir ingen ny post; sporet overlever restart fra disk | ✓ | ✓ | samme |

Regresjon: `EntityRelationHostParityTests` + runde 1 = 20/20. Hele CellBaseTests: **1262 tester, 0 feil**
(2 hoppet over, som før). Nedstrøms (CellScaffold, Binding) mot denne branchen: **ikke målt** —
kjøres når #50 skal merges.

**Én designavgjørelse tatt underveis, og den må du se:** sporet ligger på sitt eget rot-keypath
`trace`, ikke inne i `chronicle`. Første utkast la det i chronicle-listen; det knakk
`EntityRelationHostParityTests`, som sammenligner chronicle-listen post for post som en wire-kontrakt
mellom verter. Sporet er ankerets egen bok over hva det tok imot, og må aldri endre det en batch
skrev. FORMAALSSPEC sier «i chronicle» — det står nå som avvik i STATUS til du sier hva du vil.

**Tre ting som gikk galt i kjøringen, og som står her fordi de er sanne:**
1. `399f6d2` ble pushet rød (4 feil). Skriptets grønn-port grep'et etter «Executed … with 0 failures»
   og traff en *tidligere* suites linje. Rettet: bare siste linje teller, og mønsteret er
   « 0 failures (0 unexpected)» — sluttlinjen sier «with 2 tests skipped and 0 failures».
   Lærdom `lesson.green-gate-must-read-the-last-summary-line`.
2. `echo "$X" | grep -q` under `pipefail` ga rød på grønt tre (SIGPIPE). Rettet til POSIX `case`.
3. To kompileringsrunder på kjente ting: `await` inne i XCTAssert-autoclosure (lesson fra runde 1,
   ikke fulgt), og `CellApple`/`CellVapor` er både modul- og typenavn — løst med to typealias-filer.
