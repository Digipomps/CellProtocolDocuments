# Testresultat — lagringsceller og tjenesteregister, leveranse 1

Oppdatert 2026-10-08. Kilde: GitHub Actions «AdminScaffold immutable images», jobben «Focused control-plane gates» (Linux, swift:6.1). Swift ble ikke kjørt der koden ble skrevet; CI er første og eneste kompilering.

<a id="baseline"></a>
## Grunnlinje (AP0)

Ikke kjørt som egen tom PR. Erstattet av: main `fdcfe7a5` var grønn i CI 2026-09-30, og i kjøringene under feiler ingen test utenfor denne oppgavens filer. Det er svakere enn en egen grunnlinje og står her som avvik.

<a id="build"></a>
## Bygg

| Commit | Resultat | Hva |
|---|---|---|
| `cadf056` (PR A) | rød | ukjent fra skyen (loggen ligger på en vert proxyen stenger) |
| `0cde97c` (PR A) | rød | `ObjectStorageS3.swift:165` «unable to type-check this expression in reasonable time» (lest fra ny annotasjon) |
| `1f173d8` (PR A) | grønn | uttrykket delt opp |
| `ac7936d` (PR B) | rød | `StorageServiceRegistryCellTests.swift:137` «'?' pattern cannot match values of type 'ValueType'» |
| `21dd5a5` (PR A) | **grønn** | |

<a id="regression"></a>
## Regresjon og nye tester

| Commit | Resultat | Feilende tester |
|---|---|---|
| `8fbd829` (PR A) | rød, 1 av 30 bolker | `ObjectStorageS3Tests.testServiceThatStoresOtherBytesIsRejected`, `…testEtagMismatchRemovesTheBadObjectFromTheService` — feil i testens etterligning (ETag regnet før bytene ble endret), ikke i cellen |
| `21dd5a5` (PR A) | **grønn, alle 30 bolker** | — |
| `b75d6b9` (PR B) | rød, 1 av 30 bolker | `CellScaffoldRuntimeIdentityRegistryTests.testCanonicalEncodingHasStableSHA256GoldenAndNoSecretsOrPaths` — forventet: gullkornet endres når en konsument legges til |
| `a26932a` (PR B) | venter | nytt gullkorn lest fra CI |

## Avledede tester (§5)

| Test | Status | Bevis |
|---|---|---|
| test.lagring.rundtur | grønn mot etterligning (CI); **ikke kjørt mot ekte tjeneste** | `ObjectStorageS3Tests.testSmallFileRoundTripsThroughServiceAndNotOntoHostDisk`, `…testSignedUploadIsConfirmedAgainstSizeAtServiceAndMarkedDeclared` |
| test.lagring.les-bytene | delvis: ETag-kontroll mot tjenesten grønn i CI; lesing utenom cellen mot ekte tjeneste ikke kjørt | `…testServiceThatStoresOtherBytesIsRejected`, `…testEtagMismatchRemovesTheBadObjectFromTheService`, `…testKMSEncryptedBucketIsNotMistakenForEtagMismatch` |
| test.lagring.bytt-tjeneste | grønn (CI) | `…testSwitchingServiceKeepsOlderReferencesReadable` |
| test.lagring.ingen-hemmeligheter | grønn (CI) | `…testKeysNeverEnterStateUsagePersistenceOrProviderRecords` |
| test.cell.auth-negative | grønn (CI), uten debug-snarveien | `…testOutsiderIsDeniedEveryStorageAction`; registeret: `StorageServiceRegistryCellTests.testAnyProvenIdentityReadsAndRanksAndOnlyTheOwnerApproves` |
| test.lagring.maaling | grønn mot etterligning; avvik mot tjenestens egne tall **ikke målt** | `…testUsageCountsStoredBytesExactlyAndEgressAsEstimate` |
| test.lagring.vert-vokser-ikke | delvis: ingen fil på disk ved S3-leverandør (CI); på verten ikke kjørt (AP10/AP12) | `…testSmallFileRoundTripsThroughServiceAndNotOntoHostDisk` |
| test.pris.mikroore, test.pris.kost-pluss-paaslag | grønn (CI) | `StoragePricingTests` (6) |
| test.register.oppforing-komplett, test.register.utdatert-merkes | venter på `a26932a` | `StorageServiceRegistryCellTests` |
| test.register.rangering | venter på `a26932a` | samme |
| test.register.tilgang-per-klasse | blokkert: entitetsklasse finnes ikke (AP8) | — |
| Signering (SigV4) | grønn (CI) mot fasit fra botocore 1.43.109 | tre signaturtester |
| test.gui.* | ikke startet (PR C) | — |
