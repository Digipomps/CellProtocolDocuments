# TESTRESULT — entitetsdata egen kontroll

Runde 1 (WP1 genesis, WP2 herdinger). Kjørt 2026-09-22 på Kjetils Mac i worktreet
`~/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata`, gren `pdd/entitetsdata-egen-kontroll`
fra `origin/main` 473357c, commit `ebb0b7f`. Rå logger ligger i `handoff/runde1/verify-*.log`.
Tallene under er kopiert fra loggene, ikke skrevet fra hukommelsen.

## #build

**CellProtocol** (worktreet, gren `pdd/entitetsdata-egen-kontroll`, commit `ebb0b7f` på `origin/main` 473357c):
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
