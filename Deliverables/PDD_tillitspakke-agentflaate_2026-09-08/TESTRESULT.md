# TESTRESULT — tillitspakke for agentflåte

Dato: 2026-09-08 (Europe/Oslo, UTC+02:00).

## Baseline <a id="baseline"></a>

**WP0 (historisk):** Uten `--disable-sandbox` feilet bygg og test i begge repoer med `sandbox-exec: sandbox_apply: Operation not permitted`; ingen tester ble kjørt.

**WP0b (historisk):** Med `--disable-sandbox` var begge bygg grønne, men XCTest-lastingen feilet med `incompatible architecture (have 'arm64', need 'x86_64')`; ingen tester ble kjørt.

**WP0c · `purpose://quality.build-and-regression`: `blocked` for ny SwiftPM-bygg/test-baseline; direkte XCTest-kjøring fullført og rød i begge repoer.** `arch -arm64`-byggene og ett `--skip-build`-forsøk per repo stopper i manifestfasen på nektet skrivetilgang til Clangs modulcache. Reservekommandoen `xcrun --sdk macosx xctest <bundle>` laster begge eksisterende bundler og fullfører XCTest-kjøringene. Arkitektur-lastefeilen fra WP0b opptrer ikke i disse direktekjøringene.

**Avgrensning:** Bundlene eksisterte før WP0c og ble ikke bygget på nytt i denne kjøringen. Testresultatene gjelder disse binærfilene; de dokumenterer ikke et nytt grønt bygg av gjeldende kildekode. Direkte `xctest` er ikke en fullført `swift test`-kjøring; Swift Testing-delen er ikke verifisert i WP0c. Årsaken til WP0b sitt arkitekturavvik er fortsatt uavklart.

Kjørt 2026-09-08, med repo-røttene som arbeidskatalog. Hver kommando er målt med `time.monotonic()` (veggklokketid, inkludert manifestfasen). Klokkeslett nedenfor er Europe/Oslo (UTC+02:00). Byggene ble kjørt sekvensielt, deretter ett `--skip-build`-forsøk per repo, deretter direkte XCTest per bundle. Testleddet etter `&&` ble ikke startet fordi byggleddet feilet. Ingen ekstra Swift-flagg eller miljøoverstyringer ble lagt til. Ventetid mellom forsøk inngår ikke i samlet kommandotid.

| Repo, eksisterende XCTest-bundle | XCTest `Executed` | Hoppet over | Rapporterte `failures` | Røde testtilfeller | Exit |
|---|---:|---:|---:|---:|---:|
| CellProtocol | 1060 | 8 | 6 | 6 | 1 |
| CellScaffold | 2046 | 11 | 148 | 46 | 1 |

`Executed`-tallene gjengir XCTest og inkluderer de oppgitte hoppede testene. `failures` teller feilrapporter; én test kan ha flere. Suite-, bundle- og «All tests»-summer skal ikke summeres med hverandre.

### Arkitekturdiagnostikk — kommandoer og ekte utdata

`arch` — exit 0:

```text
arm64
```

`uname -m` — exit 0:

```text
arm64
```

`sysctl -n sysctl.proc_translated` — exit 1:

```text
sysctl: sysctl fmt -1 1024 1: Operation not permitted
```

`file "$(readlink /Users/kjetil/.local/bin/codex)" | head -2` — exit 0:

```text
/Applications/ChatGPT.app/Contents/Resources/codex: Mach-O 64-bit executable arm64
```

`file "$(xcrun -f xctest)" | head -2` — exit 0:

```text
/Applications/Xcode.app/Contents/Developer/usr/bin/xctest: Mach-O universal binary with 2 architectures: [x86_64:Mach-O 64-bit executable x86_64] [arm64:Mach-O 64-bit executable arm64]
/Applications/Xcode.app/Contents/Developer/usr/bin/xctest (for architecture x86_64):	Mach-O 64-bit executable x86_64
```

`arch`, `uname -m` og Codex-binærfilen viser `arm64` i denne økten; `xctest` er universell med både `x86_64` og `arm64`. `sysctl.proc_translated` er **blocked** av `Operation not permitted`, så den forespurte Rosetta-kontrollen kan ikke fullføres. Ingen verdi for denne sysctl-en er utledet eller antatt.

### CellProtocol

Arbeidskatalog: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/`.

Bestilt kjede (test bare ved exit 0 fra bygg):

```sh
arch -arm64 swift build --disable-sandbox && arch -arm64 swift test --disable-sandbox
```

| Kommando | Start–slutt (Europe/Oslo) | Varighet | Exit | Resultat |
|---|---|---:|---:|---|
| `arch -arm64 swift build --disable-sandbox` | 19:39:52–19:39:54 | 1.102 s | 1 | `blocked`: manifest/modulcache |
| `arch -arm64 swift test --disable-sandbox` | — | — | — | `blocked`: ikke startet etter feilet bygg (`&&`) |
| `arch -arm64 swift test --disable-sandbox --skip-build` | 20:42:53–20:42:54 | 1.360 s | 1 | `blocked`: manifest/modulcache |
| `xcrun --sdk macosx xctest /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/.build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest` | 20:43:13–20:45:18 | 125.406 s | 1 | Fullført, rød: 6 feil i 6 tester |

Samlet målt kommandotid: **127.868 s**. Bygg og `--skip-build` utførte 0 tester; røde testnavn kunne ikke måles i disse forsøkene. Navnene nedenfor kommer fra direkte XCTest.

#### `arch -arm64 swift build --disable-sandbox` — ekte feilutdata

Første forekomst av hver relevant feillinje; gjentatte manifestkommandoer er utelatt.

```text
<unknown>:0: error: error opening '/Users/kjetil/.cache/clang/ModuleCache/Swift-3M9PW99GOL2CE.swiftmodule' for output: /Users/kjetil/.cache/clang/ModuleCache/Swift-3M9PW99GOL2CE.swiftmodule: Operation not permitted
<unknown>:0: error: unable to load standard library for target 'arm64-apple-macosx14.0'
error: ExitCode(rawValue: 1)
```

#### `arch -arm64 swift test --disable-sandbox --skip-build` — ekte feilutdata

Første forekomst av hver relevant feillinje; gjentatte manifestkommandoer er utelatt.

```text
<unknown>:0: error: error opening '/Users/kjetil/.cache/clang/ModuleCache/Swift-3M9PW99GOL2CE.swiftmodule' for output: /Users/kjetil/.cache/clang/ModuleCache/Swift-3M9PW99GOL2CE.swiftmodule: Operation not permitted
<unknown>:0: error: unable to load standard library for target 'arm64-apple-macosx14.0'
error: ExitCode(rawValue: 1)
```

#### Direkte XCTest — ekte totalsummer

```text
Test Suite 'CellProtocolPackageTests.xctest' failed at 2026-09-08 20:45:18.492.
	 Executed 1060 tests, with 8 tests skipped and 6 failures (5 unexpected) in 124.659 (124.785) seconds
Test Suite 'All tests' failed at 2026-09-08 20:45:18.492.
	 Executed 1060 tests, with 8 tests skipped and 6 failures (5 unexpected) in 124.659 (124.787) seconds
```

#### Røde testnavn — 6 testtilfeller, ekte utdata

```text
Test Case '-[CellBaseTests.AppleIdentityVaultKeyStorageTests testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns]' failed (0.827 seconds).
Test Case '-[CellBaseTests.AppleIdentityVaultKeyStorageTests testLegacyEmbeddedPrivateKeyStillSigns]' failed (0.001 seconds).
Test Case '-[CellBaseTests.AppleIdentityVaultKeyStorageTests testScopedSecretDataStaysStableInUnsignedTestHost]' failed (0.009 seconds).
Test Case '-[CellBaseTests.EntityScannerAgreementSurfaceTests testAgreementTemplateExposesOnlyTheApprovedSurface]' failed (0.001 seconds).
Test Case '-[CellBaseTests.OID4VPSignedRequestTrustVerifierTests testVerifiesX509HashSignedRequest]' failed (0.003 seconds).
Test Case '-[CellBaseTests.OID4VPSignedRequestTrustVerifierTests testVerifiesX509SanDNSSignedRequest]' failed (0.001 seconds).
```

<details>
<summary>Første diagnostiske feillinje per rød test — ekte utdata</summary>

Utvalget nedenfor viser én feilrapport per rød test, i samme rekkefølge som navnene over; øvrige feilrapporter finnes i fulloggen. Sammenflettet stdout/stderr er beholdt ordrett.

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/IdentityVault.swift:1369: error: -[CellBaseTests.AppleIdentityVaultKeyStorageTests testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns] : failed: caught error: "Creating private key failed with error: Optional(Swift.Unmanaged<__C.CFErrorRef>(_value: Error Domain=NSOSStatusErrorDomain Code=-50 "failed to generate CDSA key" (paramErr: error in user parameter list) UserInfo={numberOfErrorsDeep=0, NSDescription=failed to generate CDSA key}))"
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/IdentityVault.swift:1369: error: -[CellBaseTests.AppleIdentityVaultKeyStorageTests testLegacyEmbeddedPrivateKeyStillSigns] : failed: caught error: "Creating private key failed with error: Optional(Swift.Unmanaged<__C.CFErrorRef>(_value: Error Domain=NSOSStatusErrorDomain Code=-50 "failed to generate CDSA key" (paramErr: error in user parameter list) UserInfo={numberOfErrorsDeep=0, NSDescription=failed to generate CDSA key}))"
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/IdentityVault.swift:610: error: -[CellBaseTests.AppleIdentityVaultKeyStorageTests testScopedSecretDataStaysStableInUnsignedTestHost] : failed: caught error: "unhandledError(status: -50)"
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Tests/CellBaseTests/EntityScannerAgreementSurfaceTests.swift:75: error: -[CellBaseTests.EntityScannerAgreementSurfaceTests testAgreementTemplateExposesOnlyTheApprovedSurface] : XCTAssertTrue failed - EntityScannerCell.agreementTemplate eksponerer nøkler som ikke er gjennomgått: ["radar", "select"]. Legg dem til fasiten i denne testen bare hvis du har vurdert hva en innsluppet motpart kan lese gjennom dem — se F1 i Codex_FixList_NearbyScanner_2026-08-24.md.
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/VerifiableCredentials/Standards/OpenID4VP/OID4VPSignedRequestTrustVerifier.swift:353: error: -[CellBaseTests.OID4VPSignedRequestTrustVerifierTests testVerifiesX509HashSignedRequest] : failed: caught error: "invalidX509CertificateChain"
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/VerifiableCredentials/Standards/OpenID4VP/OID4VPSignedRequestTrustVerifier.swift:348: error: -[CellBaseTests.OID4VPSignedRequestTrustVerifierTests testVerifiesX509SanDNSSignedRequest] : failed: caught error: "invalidX509CertificateChain"
```

</details>

<details>
<summary>Alle XCTest «Executed»-linjer med suitekontekst — ekte utdata</summary>

```text
Test Suite 'AdmissionAndCatalogContractModelsTests' passed at 2026-09-08 20:43:13.735.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.029 (0.029) seconds
Test Suite 'AgreementCodingTests' passed at 2026-09-08 20:43:13.745.
	 Executed 22 tests, with 0 failures (0 unexpected) in 0.009 (0.010) seconds
Test Suite 'AppleBridgeTransportTests' passed at 2026-09-08 20:43:13.751.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'AppleIdentityVaultKeyStorageTests' failed at 2026-09-08 20:43:14.746.
	 Executed 12 tests, with 7 tests skipped and 3 failures (3 unexpected) in 0.995 (0.996) seconds
Test Suite 'AppleIntelligenceCellContractTests' passed at 2026-09-08 20:43:14.884.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.137 (0.137) seconds
Test Suite 'AppleRuntimeStorageTests' passed at 2026-09-08 20:43:14.895.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'AudioAnalysisRecordTests' passed at 2026-09-08 20:43:14.897.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'AudioSignalAnalysisTests' passed at 2026-09-08 20:43:14.897.
	 Executed 1 test, with 1 test skipped and 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'BridgeInboundPayloadValidatorTests' passed at 2026-09-08 20:43:14.897.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'BridgeMultiplexingTests' passed at 2026-09-08 20:43:15.117.
	 Executed 18 tests, with 0 failures (0 unexpected) in 0.218 (0.220) seconds
Test Suite 'BridgeTests' passed at 2026-09-08 20:45:03.046.
	 Executed 48 tests, with 0 failures (0 unexpected) in 107.917 (107.930) seconds
Test Suite 'CalendarContractTests' passed at 2026-09-08 20:45:03.081.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.034 (0.034) seconds
Test Suite 'CellAccessGraphContractsTests' passed at 2026-09-08 20:45:03.085.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'CellBaseTests' passed at 2026-09-08 20:45:03.089.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'CellJSONCoderTests' passed at 2026-09-08 20:45:03.090.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'CellLifecycleTests' passed at 2026-09-08 20:45:07.027.
	 Executed 9 tests, with 0 failures (0 unexpected) in 3.935 (3.937) seconds
Test Suite 'CellResolverProtocolLightweightBridgeTransportTests' passed at 2026-09-08 20:45:07.028.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'CellRuntimeEnvironmentTests' passed at 2026-09-08 20:45:07.030.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'CellRuntimeReadinessContractTests' passed at 2026-09-08 20:45:07.189.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.158 (0.159) seconds
Test Suite 'CellSecurityKitTests' passed at 2026-09-08 20:45:07.194.
	 Executed 20 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'ChatCellTests' passed at 2026-09-08 20:45:07.546.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.349 (0.352) seconds
Test Suite 'ClaimCompositionTests' passed at 2026-09-08 20:45:07.549.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.002 (0.003) seconds
Test Suite 'ClaimDefinitionTests' passed at 2026-09-08 20:45:07.549.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'ClaimSchemeTests' passed at 2026-09-08 20:45:07.552.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.002 (0.003) seconds
Test Suite 'CommonsCellsTests' passed at 2026-09-08 20:45:07.580.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.027 (0.028) seconds
Test Suite 'ConferenceOrganizerAccessModelsTests' passed at 2026-09-08 20:45:07.590.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'ConferenceSwarmSignalMatchingTests' passed at 2026-09-08 20:45:07.602.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.011 (0.012) seconds
Test Suite 'ContractProbeCellTests' passed at 2026-09-08 20:45:10.277.
	 Executed 11 tests, with 0 failures (0 unexpected) in 2.674 (2.676) seconds
Test Suite 'CorrespondenceCellTests' passed at 2026-09-08 20:45:10.325.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.047 (0.048) seconds
Test Suite 'CrossRuntimeWireFixtureTests' passed at 2026-09-08 20:45:10.326.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'DIDDocumentValidatorTests' passed at 2026-09-08 20:45:10.328.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'DIDInteroperabilityTests' passed at 2026-09-08 20:45:10.330.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'DeviceIngressContractTests' passed at 2026-09-08 20:45:10.547.
	 Executed 20 tests, with 0 failures (0 unexpected) in 0.167 (0.217) seconds
Test Suite 'DeviceIngressWireFixtureTests' passed at 2026-09-08 20:45:10.550.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'DiagnosticLoggingTests' passed at 2026-09-08 20:45:10.550.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'EntityAtlasInspectorCellTests' passed at 2026-09-08 20:45:10.566.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
Test Suite 'EntityAtlasProjectionTests' passed at 2026-09-08 20:45:10.590.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.024 (0.024) seconds
Test Suite 'EntityAuthorityCommitTests' passed at 2026-09-08 20:45:10.646.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.055 (0.056) seconds
Test Suite 'EntityAuthorityReplicaStoreTests' passed at 2026-09-08 20:45:10.697.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.050 (0.050) seconds
Test Suite 'EntityRelationRecordV1Tests' passed at 2026-09-08 20:45:10.705.
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.008 (0.008) seconds
Test Suite 'EntityRepresentationAgreementTests' passed at 2026-09-08 20:45:10.706.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'EntityScannerAgreementSurfaceTests' failed at 2026-09-08 20:45:10.709.
	 Executed 3 tests, with 1 failure (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'EntityScannerCellContractTests' passed at 2026-09-08 20:45:10.728.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.019 (0.019) seconds
Test Suite 'EntityValidatedContactRecordV1Tests' passed at 2026-09-08 20:45:10.731.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'ExploreContractValidatorTests' passed at 2026-09-08 20:45:10.732.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'FileCryptoCellTests' passed at 2026-09-08 20:45:10.738.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.006 (0.007) seconds
Test Suite 'FlowCacheCellTests' passed at 2026-09-08 20:45:10.750.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.011 (0.012) seconds
Test Suite 'FlowEnvelopeCryptoTests' passed at 2026-09-08 20:45:10.753.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'FlowEnvelopeSerializationTests' passed at 2026-09-08 20:45:10.754.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'FlowInspectionCellsTests' passed at 2026-09-08 20:45:10.937.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.183 (0.183) seconds
Test Suite 'GeneralCellInterfaceTests' passed at 2026-09-08 20:45:11.027.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.087 (0.090) seconds
Test Suite 'GoalDefinitionTests' passed at 2026-09-08 20:45:11.032.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'GoalEvaluationCellTests' passed at 2026-09-08 20:45:11.036.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'GoalEvaluationEngineTests' passed at 2026-09-08 20:45:11.037.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'GraphIndexCellTests' passed at 2026-09-08 20:45:11.047.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'IdentitiesCellContractTests' passed at 2026-09-08 20:45:11.048.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'IdentityAgreementTests' passed at 2026-09-08 20:45:11.056.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
Test Suite 'IdentityDomainBindingTests' passed at 2026-09-08 20:45:11.057.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'IdentityLinkingModelsTests' passed at 2026-09-08 20:45:11.075.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.017 (0.018) seconds
Test Suite 'IdentityPublicKeySignatureVerifierTests' passed at 2026-09-08 20:45:11.079.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'IntegrationTests' passed at 2026-09-08 20:45:13.048.
	 Executed 35 tests, with 0 failures (0 unexpected) in 1.962 (1.969) seconds
Test Suite 'JOSEAESKeyWrapTests' passed at 2026-09-08 20:45:13.067.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.019 (0.019) seconds
Test Suite 'JOSEJWSVerifierSecurityTests' passed at 2026-09-08 20:45:13.073.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'KeyPathResolverTests' passed at 2026-09-08 20:45:13.077.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.004 (0.005) seconds
Test Suite 'LightweightBridgeTransportTests' passed at 2026-09-08 20:45:13.465.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.385 (0.387) seconds
Test Suite 'LobbyCellContractTests' passed at 2026-09-08 20:45:13.493.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.028 (0.028) seconds
Test Suite 'MatchStrategyPlannerTests' passed at 2026-09-08 20:45:13.495.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'NearbyBeaconTests' passed at 2026-09-08 20:45:13.498.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.003 (0.004) seconds
Test Suite 'NearbyDisclosurePolicyTests' passed at 2026-09-08 20:45:13.499.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'NearbyPeerStateMachineTests' passed at 2026-09-08 20:45:13.500.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'NearbyProbeTests' passed at 2026-09-08 20:45:13.501.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'OID4VCICredentialOfferTests' passed at 2026-09-08 20:45:13.502.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'OID4VCIIssuerMetadataTests' passed at 2026-09-08 20:45:13.504.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'OID4VCIMetadataClientTests' passed at 2026-09-08 20:45:13.506.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'OID4VPDCQLTests' passed at 2026-09-08 20:45:13.508.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'OID4VPDirectPostJWTEncryptionTests' passed at 2026-09-08 20:45:13.518.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'OID4VPDirectPostJWTSubmissionAdapterTests' passed at 2026-09-08 20:45:13.521.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'OID4VPDirectPostTests' passed at 2026-09-08 20:45:13.523.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'OID4VPRequestMatcherTests' passed at 2026-09-08 20:45:13.523.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'OID4VPRequestObjectTests' passed at 2026-09-08 20:45:13.524.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'OID4VPResponseTests' passed at 2026-09-08 20:45:13.524.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'OID4VPSignedRequestObjectTests' passed at 2026-09-08 20:45:13.528.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'OID4VPSignedRequestTrustVerifierTests' failed at 2026-09-08 20:45:13.536.
	 Executed 7 tests, with 2 failures (2 unexpected) in 0.008 (0.008) seconds
Test Suite 'OID4VPStaticVerifierMetadataProviderTests' passed at 2026-09-08 20:45:13.537.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'OID4VPVerifierMetadataResolverTests' passed at 2026-09-08 20:45:13.537.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'OID4VPVerifierMetadataTests' passed at 2026-09-08 20:45:13.538.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'PersistedCellFileIOTests' passed at 2026-09-08 20:45:13.544.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'PersistenceTests' passed at 2026-09-08 20:45:13.560.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
Test Suite 'PerspectiveCellContractTests' passed at 2026-09-08 20:45:13.560.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'PerspectiveCellMatchPayloadTests' passed at 2026-09-08 20:45:13.572.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
Test Suite 'PerspectiveEntityProjectionTests' passed at 2026-09-08 20:45:13.576.
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'PerspectiveSchemaTests' passed at 2026-09-08 20:45:13.579.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'PortholeViewModelAvailabilityTests' passed at 2026-09-08 20:45:13.638.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.059 (0.059) seconds
Test Suite 'PurposeAndInterestMatchingTests' passed at 2026-09-08 20:45:13.641.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.002 (0.003) seconds
Test Suite 'PurposeBoundExternalActionTests' passed at 2026-09-08 20:45:13.649.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.008 (0.008) seconds
Test Suite 'PurposeCompositionTests' passed at 2026-09-08 20:45:13.649.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'PurposeGoalLintTests' passed at 2026-09-08 20:45:13.650.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'PurposeInterestAdjacencyIndexTests' passed at 2026-09-08 20:45:13.650.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'PurposeInterestBenchmarkArtifactTests' passed at 2026-09-08 20:45:13.671.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.020 (0.020) seconds
Test Suite 'PurposeInterestBenchmarkReportTests' passed at 2026-09-08 20:45:13.699.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.028 (0.028) seconds
Test Suite 'PurposeInterestChallengeExperimentTests' passed at 2026-09-08 20:45:13.706.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'PurposeInterestRuntimeComparisonTests' passed at 2026-09-08 20:45:13.749.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.043 (0.043) seconds
Test Suite 'PurposeInterestScenarioExperimentTests' passed at 2026-09-08 20:45:13.753.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'PurposeInterestScenarioRankingTests' passed at 2026-09-08 20:45:13.759.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'RadarEntityLedgerTests' passed at 2026-09-08 20:45:13.762.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'RealCellContractTests' passed at 2026-09-08 20:45:13.799.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.036 (0.037) seconds
Test Suite 'RelationalLearningCellContractTests' passed at 2026-09-08 20:45:14.118.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.319 (0.320) seconds
Test Suite 'RelationalLearningEngineTests' passed at 2026-09-08 20:45:14.123.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.004 (0.005) seconds
Test Suite 'ResolverTests' passed at 2026-09-08 20:45:14.159.
	 Executed 33 tests, with 0 failures (0 unexpected) in 0.035 (0.036) seconds
Test Suite 'RestaurantPurposeRecommendationTests' passed at 2026-09-08 20:45:14.161.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'RuntimeLifecyclePropertyTests' passed at 2026-09-08 20:45:14.179.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.018 (0.018) seconds
Test Suite 'SDGPilotPurposeCatalogTests' passed at 2026-09-08 20:45:14.180.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'ScannerServiceInvitationTests' passed at 2026-09-08 20:45:14.862.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.680 (0.681) seconds
Test Suite 'SerializationTests' passed at 2026-09-08 20:45:14.870.
	 Executed 18 tests, with 0 failures (0 unexpected) in 0.006 (0.008) seconds
Test Suite 'SkeletonActionButtonExecutionTests' passed at 2026-09-08 20:45:14.873.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.003 (0.004) seconds
Test Suite 'SkeletonButtonResolutionTests' passed at 2026-09-08 20:45:14.874.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'SkeletonLocalizationTests' passed at 2026-09-08 20:45:16.234.
	 Executed 9 tests, with 0 failures (0 unexpected) in 1.360 (1.360) seconds
Test Suite 'SkeletonReachabilityAuditTests' passed at 2026-09-08 20:45:16.236.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'SkeletonStyleParityTests' passed at 2026-09-08 20:45:16.237.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'SkeletonTests' passed at 2026-09-08 20:45:16.253.
	 Executed 51 tests, with 0 failures (0 unexpected) in 0.014 (0.016) seconds
Test Suite 'TaxonomyResolverTests' passed at 2026-09-08 20:45:16.267.
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
Test Suite 'TrustPacketCellTests' passed at 2026-09-08 20:45:16.289.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.022 (0.022) seconds
Test Suite 'TrustedIssuerCellContractTests' passed at 2026-09-08 20:45:16.291.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'TrustedIssuerCellTests' passed at 2026-09-08 20:45:17.306.
	 Executed 11 tests, with 0 failures (0 unexpected) in 1.014 (1.015) seconds
Test Suite 'TrustedIssuerEvaluationReceiptTests' passed at 2026-09-08 20:45:17.309.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'TrustedIssuerSignedEvaluationTests' passed at 2026-09-08 20:45:17.314.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'UserDataResilienceTests' passed at 2026-09-08 20:45:18.097.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.783 (0.783) seconds
Test Suite 'VCIssuerServiceSecurityTests' passed at 2026-09-08 20:45:18.099.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'VaporBridgeTransportTests' passed at 2026-09-08 20:45:18.139.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.040 (0.040) seconds
Test Suite 'VaporCellRuntimeReadinessContractTests' passed at 2026-09-08 20:45:18.193.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.054 (0.054) seconds
Test Suite 'VaporIdentityVaultStrictTests' passed at 2026-09-08 20:45:18.474.
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.280 (0.281) seconds
Test Suite 'VaultCellTests' passed at 2026-09-08 20:45:18.491.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
Test Suite 'VaultContractsTests' passed at 2026-09-08 20:45:18.492.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'CellProtocolPackageTests.xctest' failed at 2026-09-08 20:45:18.492.
	 Executed 1060 tests, with 8 tests skipped and 6 failures (5 unexpected) in 124.659 (124.785) seconds
Test Suite 'All tests' failed at 2026-09-08 20:45:18.492.
	 Executed 1060 tests, with 8 tests skipped and 6 failures (5 unexpected) in 124.659 (124.787) seconds
```

</details>

### CellScaffold

Arbeidskatalog: `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/`.

Bestilt kjede (test bare ved exit 0 fra bygg):

```sh
arch -arm64 swift build --disable-sandbox && arch -arm64 swift test --disable-sandbox
```

| Kommando | Start–slutt (Europe/Oslo) | Varighet | Exit | Resultat |
|---|---|---:|---:|---|
| `arch -arm64 swift build --disable-sandbox` | 19:39:54–19:39:54 | 0.799 s | 1 | `blocked`: manifest/modulcache |
| `arch -arm64 swift test --disable-sandbox` | — | — | — | `blocked`: ikke startet etter feilet bygg (`&&`) |
| `arch -arm64 swift test --disable-sandbox --skip-build` | 20:42:54–20:42:55 | 0.630 s | 1 | `blocked`: manifest/modulcache |
| `xcrun --sdk macosx xctest /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/.build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest` | 20:45:18–20:59:40 | 862.311 s | 1 | Fullført, rød: 148 feil i 46 tester |

Samlet målt kommandotid: **863.740 s**. Bygg og `--skip-build` utførte 0 tester; røde testnavn kunne ikke måles i disse forsøkene. Navnene nedenfor kommer fra direkte XCTest.

#### `arch -arm64 swift build --disable-sandbox` — ekte feilutdata

Første forekomst av hver relevant feillinje; gjentatte manifestkommandoer er utelatt.

```text
<unknown>:0: error: error opening '/Users/kjetil/.cache/clang/ModuleCache/Swift-3M9PW99GOL2CE.swiftmodule' for output: /Users/kjetil/.cache/clang/ModuleCache/Swift-3M9PW99GOL2CE.swiftmodule: Operation not permitted
<unknown>:0: error: unable to load standard library for target 'arm64-apple-macosx14.0'
error: ExitCode(rawValue: 1)
```

#### `arch -arm64 swift test --disable-sandbox --skip-build` — ekte feilutdata

Første forekomst av hver relevant feillinje; gjentatte manifestkommandoer er utelatt.

```text
<unknown>:0: error: error opening '/Users/kjetil/.cache/clang/ModuleCache/Swift-3M9PW99GOL2CE.swiftmodule' for output: /Users/kjetil/.cache/clang/ModuleCache/Swift-3M9PW99GOL2CE.swiftmodule: Operation not permitted
<unknown>:0: error: unable to load standard library for target 'arm64-apple-macosx14.0'
error: ExitCode(rawValue: 1)
```

#### Direkte XCTest — ekte totalsummer

```text
Test Suite 'CellsContainerPackageTests.xctest' failed at 2026-09-08 20:59:40.733.
	 Executed 2046 tests, with 11 tests skipped and 148 failures (9 unexpected) in 859.566 (859.744) seconds
Test Suite 'All tests' failed at 2026-09-08 20:59:40.734.
	 Executed 2046 tests, with 11 tests skipped and 148 failures (9 unexpected) in 859.566 (859.746) seconds
```

#### Røde testnavn — 46 testtilfeller, ekte utdata

```text
Test Case '-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsHAVENTeachingSwarmAndAppendsProviderTurns]' failed (2.057 seconds).
Test Case '-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsLocalOnlyHAVENTeachingSwarmWithoutAPIKeys]' failed (0.005 seconds).
Test Case '-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelLocalBorealisChatsAgainstSharedBackend]' failed (0.006 seconds).
Test Case '-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelMixedHostedAndLocalChatsWithRouteCredentials]' failed (0.005 seconds).
Test Case '-[AppTests.ArendalsukaEventAtlasCellTests testDecodedParticipantProgramCanEnsureRuntimeBindingsBeforeStateRead]' failed (0.009 seconds).
Test Case '-[AppTests.ArendalsukaEventAtlasCellTests testParticipantPreviewReadsDecodedRegisteredAtlasWithoutJournalFallback]' failed (0.009 seconds).
Test Case '-[AppTests.ArendalsukaEventAtlasCellTests testParticipantProgramReadsAtlasPreviewWithoutPersistingUntilExplicitAction]' failed (0.010 seconds).
Test Case '-[AppTests.ArendalsukaEventAtlasCellTests testParticipantProgramUsesAtlasPreviewForMissingProgramInPartialOverlay]' failed (0.008 seconds).
Test Case '-[AppTests.ArendalsukaImportAuthorizationRoutesTests testAdminDelegatesIdentityBoundCredentialToNonAdminImporter]' failed (0.314 seconds).
Test Case '-[AppTests.BookReferenceRoutesTests testConferenceConnectionHubLifecycleSlugRouteRendersMermaidInline]' failed (4.421 seconds).
Test Case '-[AppTests.BookReferenceRoutesTests testConferenceOwnershipSlugRouteRendersMermaidInline]' failed (2.377 seconds).
Test Case '-[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview]' failed (0.551 seconds).
Test Case '-[AppTests.ChatMVPRoutesTests testPaidStateAndMessageRoutesAwaitDecodedChatReadiness]' failed (0.251 seconds).
Test Case '-[AppTests.ConferenceEntityDiscoveryCellTests testChatLaunchCellCanStartConversationAndProjectMessageFeedback]' failed (0.019 seconds).
Test Case '-[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionHandsOffCapturedLeadToSponsorOwnedFollowUp]' failed (0.030 seconds).
Test Case '-[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionUsesConsentBoundAggregateSignalsWhenAvailable]' failed (0.026 seconds).
Test Case '-[AppTests.ConferencePublishedContentCellTests testPublishedContentCellRecognizesStableOrganizerIdentityWhenVaultContextIsPoisoned]' failed (0.001 seconds).
Test Case '-[AppTests.ConferenceSchedulingCellTests testRouterDelegatesSharedMeetingRequestAndLocalExportToSchedulingCell]' failed (0.020 seconds).
Test Case '-[AppTests.ConferenceSponsorLeadAggregateCellTests testSponsorLeadAggregateSyncsConsentBoundParticipantsAndCapturesLead]' failed (0.008 seconds).
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionAcceptsStoredImportAccessVC]' failed (0.882 seconds).
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionSupportsAdminSessionAndRejectsMismatchedSignedProof]' failed (0.883 seconds).
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication]' failed (0.224 seconds).
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublishedApiReadsUseAgreementWithoutDebugAccess]' failed (0.288 seconds).
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testConferencePageAccessPolicies]' failed (0.239 seconds).
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testConferencePagesExposeCanonicalSurfaceMetadataForWebNavigator]' failed (0.217 seconds).
Test Case '-[AppTests.ConfigurationCatalogSkeletonParityTests testConferenceParticipantPortalDocumentationConfigurationMatchesRuntimeFactory]' failed (0.026 seconds).
Test Case '-[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeRetryBlocksConsumedCredentialReplay]' failed (0.243 seconds).
Test Case '-[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction]' failed (0.240 seconds).
Test Case '-[AppTests.HavenWorkbenchConfigurationTests testHavenWorkbenchUsesLocalTabsAndSupportedVisualizations]' failed (0.008 seconds).
Test Case '-[AppTests.MermaidRendererCellTests testWebViewDeterministicModeStableAcrossThreeBypassRuns]' failed (6.182 seconds).
Test Case '-[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersPNGWithoutClientTimeout]' failed (2.119 seconds).
Test Case '-[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersSVGAndCacheHit]' failed (4.139 seconds).
Test Case '-[AppTests.MermaidRendererCellTests testWebViewRendersConferenceDiagramFilesAndExposesPreviewState]' failed (2.105 seconds).
Test Case '-[AppTests.MicropaymentsMVPRoutesTests testPaymentProofDoorAuthorizeConsumesCredentialAndBlocksReplay]' failed (0.243 seconds).
Test Case '-[AppTests.MusicPublishingCellsTests testScaffoldRecoversPersistedMusicLibraryWhenNamedEmitterRegistryIsEmpty]' failed (0.018 seconds).
Test Case '-[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction]' failed (2.761 seconds).
Test Case '-[AppTests.ProductionSkeletonBindingIntegrityTests testArendalsukaEventAtlasPortholeTabsAndDetailsDoNotReturnNotFound]' failed (0.186 seconds).
Test Case '-[AppTests.ProductionSkeletonBindingIntegrityTests testArendalsukaParticipantProgramRendersSourceBackedProgramRowsWithoutBrokenKeypaths]' failed (0.520 seconds).
Test Case '-[AppTests.ProductionSkeletonBindingIntegrityTests testHavenWorkbenchSetupThroughPortholeKeepsSkeletonBindingsResolvable]' failed (7.049 seconds).
Test Case '-[AppTests.SkeletonElementParityMatrixTests testMatrixRevisionMatchesPackagePin]' failed (0.003 seconds).
Test Case '-[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips]' failed (0.007 seconds).
Test Case '-[AppTests.SkeletonRuntimeSourceTests testPortholeBootstrapUsesHttpSnapshotNotSocketFallbackWarning]' failed (0.017 seconds).
Test Case '-[AppTests.TopUpCheckoutTests testProductionStartupRejectsMissingRuntimeIdentityManifestBeforePublishingResolver]' failed (0.014 seconds).
Test Case '-[AppTests.TopUpCheckoutTests testSimulatedTopUpAllowsExplicitProductionAllowlistedUser]' failed (0.011 seconds).
Test Case '-[AppTests.TopUpCheckoutTests testSimulatedTopUpDefaultsToDeniedInProductionLikeEnvironment]' failed (0.011 seconds).
Test Case '-[AppTests.WorkbenchAccessGrantConfigurationTests testIdentityBoundPregrantUsesIssuerVaultWhenTargetOwnerWasDecodedSnapshot]' failed (0.020 seconds).
```

<details>
<summary>Første diagnostiske feillinje per rød test — ekte utdata</summary>

Utvalget nedenfor viser én feilrapport per rød test, i samme rekkefølge som navnene over; øvrige feilrapporter finnes i fulloggen. Sammenflettet stdout/stderr er beholdt ordrett.

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AIAssistantThreadCellTests.swift:186: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsHAVENTeachingSwarmAndAppendsProviderTurns] : XCTAssertEqual failed: ("2") is not equal to ("3")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AIAssistantThreadCellTests.swift:274: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsLocalOnlyHAVENTeachingSwarmWithoutAPIKeys] : XCTAssertEqual failed: ("[]") is not equal to ("["qwen-learner", "local-chatgpt-teacher", "local-claude-teacher"]")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AIAssistantThreadCellTests.swift:346: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelLocalBorealisChatsAgainstSharedBackend] : XCTAssertEqual failed: ("[]") is not equal to ("["borealis-privacy", "borealis-architect", "borealis-concise"]")
AIInvokeStarte/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AIAssistantThreadCellTests.swift:454: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelMixedHostedAndLocalChatsWithRouteCredentials] : XCTUnwrap failed: expected non-nil value of type "AIGatewayProviderRoute"
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ArendalsukaEventAtlasCellTests.swift:1256: error: -[AppTests.ArendalsukaEventAtlasCellTests testDecodedParticipantProgramCanEnsureRuntimeBindingsBeforeStateRead] : XCTAssertEqual failed: ("Optional(false)") is not equal to ("Optional(true)")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ArendalsukaEventAtlasCellTests.swift:1401: error: -[AppTests.ArendalsukaEventAtlasCellTests testParticipantPreviewReadsDecodedRegisteredAtlasWithoutJournalFallback] : XCTAssertEqual failed: ("Optional(false)") is not equal to ("Optional(true)")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ArendalsukaEventAtlasCellTests.swift:1146: error: -[AppTests.ArendalsukaEventAtlasCellTests testParticipantProgramReadsAtlasPreviewWithoutPersistingUntilExplicitAction] : XCTAssertEqual failed: ("Optional(false)") is not equal to ("Optional(true)")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ArendalsukaEventAtlasCellTests.swift:1222: error: -[AppTests.ArendalsukaEventAtlasCellTests testParticipantProgramUsesAtlasPreviewForMissingProgramInPartialOverlay] : XCTAssertEqual failed: ("Optional(false)") is not equal to ("Optional(true)")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ArendalsukaImportAuthorizationRoutesTests.swift:223: error: -[AppTests.ArendalsukaImportAuthorizationRoutesTests testAdminDelegatesIdentityBoundCredentialToNonAdminImporter] : XCTAssertEqual failed: ("500 Internal Server Error") is not equal to ("200 OK")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/BookReferenceRoutesTests.swift:121: error: -[AppTests.BookReferenceRoutesTests testConferenceConnectionHubLifecycleSlugRouteRendersMermaidInline] : XCTAssertTrue failed
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/BookReferenceRoutesTests.swift:102: error: -[AppTests.BookReferenceRoutesTests testConferenceOwnershipSlugRouteRendersMermaidInline] : XCTAssertTrue failed
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ButterpopStudioProductTests.swift:899: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: threw error "Error Domain=ButterpopStudioProductTests Code=1 "(null)""
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ChatMVPRoutesTests.swift:379: error: -[AppTests.ChatMVPRoutesTests testPaidStateAndMessageRoutesAwaitDecodedChatReadiness] : XCTAssertEqual failed: ("502 Bad Gateway") is not equal to ("200 OK") - {"reason":"PaymentGate did not issue the simulated usage quota.","error":true}
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/CellResolver/Cast/ResolverAuditor.swift:167: error: -[AppTests.ConferenceEntityDiscoveryCellTests testChatLaunchCellCanStartConversationAndProjectMessageFeedback] : failed: caught error: "registerAtAlreadyTakenEndpoint"
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ConferenceOrganizerProjectionCellTests.swift:223: error: -[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionHandsOffCapturedLeadToSponsorOwnedFollowUp] : XCTAssertTrue failed
**** Creating BrowserClientIdentityVault for identitydDomain: conference-orga/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ConferenceOrganizerProjectionCellTests.swift:133: error: -[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionUsesConsentBoundAggregateSignalsWhenAvailable] : XCTAssertTrue failed
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/ScaffoldKit/BrowserClientIdentityVault.swift:864: error: -[AppTests.ConferencePublishedContentCellTests testPublishedContentCellRecognizesStableOrganizerIdentityWhenVaultContextIsPoisoned] : failed: caught error: "persistedIdentityUnavailable"
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ConferenceSchedulingCellTests.swift:152: error: -[AppTests.ConferenceSchedulingCellTests testRouterDelegatesSharedMeetingRequestAndLocalExportToSchedulingCell] : XCTAssertTrue failed
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/ScaffoldKit/BrowserClientIdentityVault.swift:864: error: -[AppTests.ConferenceSponsorLeadAggregateCellTests testSponsorLeadAggregateSyncsConsentBoundParticipantsAndCapturesLead] : failed: caught error: "persistedIdentityUnavailable"
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2617: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionAcceptsStoredImportAccessVC] : XCTAssertEqual failed: ("500 Internal Server Error") is not equal to ("200 OK")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:700: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionSupportsAdminSessionAndRejectsMismatchedSignedProof] : XCTAssertEqual failed: ("500 Internal Server Error") is not equal to ("200 OK")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2468: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication] : XCTAssertEqual failed: ("503 Service Unavailable") is not equal to ("200 OK")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2397: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublishedApiReadsUseAgreementWithoutDebugAccess] : XCTAssertEqual failed: ("503 Service Unavailable") is not equal to ("200 OK")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:102: error: -[AppTests.ConferenceSurfaceRoutesTests testConferencePageAccessPolicies] : XCTAssertEqual failed: ("200 OK") is not equal to ("303 See Other")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:311: error: -[AppTests.ConferenceSurfaceRoutesTests testConferencePagesExposeCanonicalSurfaceMetadataForWebNavigator] : XCTAssertEqual failed: ("200 OK") is not equal to ("303 See Other")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ConfigurationCatalogSkeletonParityTests.swift:316: error: -[AppTests.ConfigurationCatalogSkeletonParityTests testConferenceParticipantPortalDocumentationConfigurationMatchesRuntimeFactory] : failed - Key mismatch at $.skeleton.VStack[1].Tabs.panels[1].content[0].Section.content[4].Tabs.panels[0].content[2].List. Missing from runtime: []. Missing from documentation: ["activationActionKeypath"].
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ContractChallengeMVPRoutesTests.swift:113: error: -[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeRetryBlocksConsumedCredentialReplay] : XCTAssertEqual failed: ("402 Payment Required") is not equal to ("200 OK")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ContractChallengeMVPRoutesTests.swift:66: error: -[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("issued")") - string("error: failed to resolve identity domain")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/HavenWorkbenchConfigurationTests.swift:46: error: -[AppTests.HavenWorkbenchConfigurationTests testHavenWorkbenchUsesLocalTabsAndSupportedVisualizations] : XCTAssertEqual failed: ("["status", "all", "board", "inbox", "triage", "backlog", "projects", "roadmap", "graph", "github", "docs"]") is not equal to ("["status", "board", "inbox", "triage", "backlog", "projects", "roadmap", "graph", "github", "docs"]")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/MermaidRendererCellTests.swift:144: error: -[AppTests.MermaidRendererCellTests testWebViewDeterministicModeStableAcrossThreeBypassRuns] : XCTAssertTrue failed
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/MermaidRendererCellTests.swift:112: error: -[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersPNGWithoutClientTimeout] : XCTAssertTrue failed - Expected PNG render to succeed quickly, got: ["Render timed out after 2000ms"]
MermaidRenderFailed corr/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/MermaidRendererCellTests.swift:75: error: -[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersSVGAndCacheHit] : XCTAssertTrue failed - Expected first render to succeed: ["Render timed out after 2000ms"]
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/MermaidRendererCellTests.swift:216: error: -[AppTests.MermaidRendererCellTests testWebViewRendersConferenceDiagramFilesAndExposesPreviewState] : XCTAssertTrue failed - Expected conference-system-overview.mmd to render without errors, got: ["Render timed out after 2000ms"]
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/MicropaymentsMVPRoutesTests.swift:39: error: -[AppTests.MicropaymentsMVPRoutesTests testPaymentProofDoorAuthorizeConsumesCredentialAndBlocksReplay] : XCTAssertEqual failed: ("402 Payment Required") is not equal to ("200 OK")
Loading identity named emitters failed with error: Error Domain=NSCocoaErrorDomain Code=260 "Filen «IdentityNamedEmitters.json» kunne ikke åpnes fordi filen ikke finnes." UserInfo={NSFilePath=/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/MusicPublishingCellsTests-007677FC-5667-4993-8FAD-1AEB4FD5D270/CellsContainer/ScaffoldOrchestrator/IdentityNamedEmitters.json, NSURL=file:///var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/MusicPublishingCellsTests-007677FC-5667-4993-8FAD-1AEB4FD5D270/CellsContainer/ScaffoldOrchestrator/IdentityNamedEmitters.json, NSUnd/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/MusicPublishingCellsTests.swift:182: error: -[AppTests.MusicPublishingCellsTests testScaffoldRecoversPersistedMusicLibraryWhenNamedEmitterRegistryIsEmpty] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("5F1BDE80-78F8-4142-B3D6-EF940C7F7746")")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:968: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertTrue failed - Expected webview render to succeed: [CellBase.ValueType.string("Render timed out after 2000ms")]
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ProductionSkeletonBindingIntegrityTests.swift:451: error: -[AppTests.ProductionSkeletonBindingIntegrityTests testArendalsukaEventAtlasPortholeTabsAndDetailsDoNotReturnNotFound] : XCTAssertGreaterThanOrEqual failed: ("0") is less than ("3")
Initial loading of cellConfiguration in orchestrator failed with error: Error Domain=NSCocoaErrorDomain Code=260 "Filen «CellConfiguration.json» kunne ikke åpnes fordi filen ikke finnes." UserInfo={NSFilePath=/var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/Cell/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ProductionSkeletonBindingIntegrityTests.swift:142: error: -[AppTests.ProductionSkeletonBindingIntegrityTests testArendalsukaParticipantProgramRendersSourceBackedProgramRowsWithoutBrokenKeypaths] : XCTAssertGreaterThanOrEqual failed: ("0") is less than ("3")
Saving identity named cells: 3 ide/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/ProductionSkeletonBindingIntegrityTests.swift:79: error: -[AppTests.ProductionSkeletonBindingIntegrityTests testHavenWorkbenchSetupThroughPortholeKeepsSkeletonBindingsResolvable] : XCTAssertTrue failed - Broken skeleton bindings in HAVEN Workbench:
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/SkeletonElementParityMatrixTests.swift:124: error: -[AppTests.SkeletonElementParityMatrixTests testMatrixRevisionMatchesPackagePin] : XCTUnwrap failed: expected non-nil value of type "Dictionary<String, Any>"
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/SkeletonElementParityMatrixTests.swift:89: error: -[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips] : XCTAssertTrue failed - Binding renderer source evidence is missing at /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/.build/checkouts/CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/SkeletonRuntimeSourceTests.swift:87: error: -[AppTests.SkeletonRuntimeSourceTests testPortholeBootstrapUsesHttpSnapshotNotSocketFallbackWarning] : XCTAssertTrue failed
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Support/CellScaffoldRuntimeIdentityManifest.swift:128: error: -[AppTests.TopUpCheckoutTests testProductionStartupRejectsMissingRuntimeIdentityManifestBeforePublishingResolver] : failed: caught error: "buildMetadataMissing"
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Support/CellScaffoldRuntimeIdentityManifest.swift:128: error: -[AppTests.TopUpCheckoutTests testSimulatedTopUpAllowsExplicitProductionAllowlistedUser] : failed: caught error: "buildMetadataMissing"
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Support/CellScaffoldRuntimeIdentityManifest.swift:128: error: -[AppTests.TopUpCheckoutTests testSimulatedTopUpDefaultsToDeniedInProductionLikeEnvironment] : failed: caught error: "buildMetadataMissing"
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/CellResolver/Cast/ResolverAuditor.swift:171: error: -[AppTests.WorkbenchAccessGrantConfigurationTests testIdentityBoundPregrantUsesIssuerVaultWhenTargetOwnerWasDecodedSnapshot] : failed: caught error: "personalInstanceAlreadyRegistered"
```

</details>

<details>
<summary>Alle XCTest «Executed»-linjer med suitekontekst — ekte utdata</summary>

```text
Test Suite 'AIAssistantThreadCellTests' failed at 2026-09-08 20:45:23.105.
	 Executed 14 tests, with 4 tests skipped and 12 failures (0 unexpected) in 2.115 (2.115) seconds
Test Suite 'AIGatewayCellTests' passed at 2026-09-08 20:45:23.217.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.110 (0.112) seconds
Test Suite 'AIGatewayConfigurationFactoryTests' passed at 2026-09-08 20:45:23.218.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'AccessRequirementPromptCellTests' passed at 2026-09-08 20:45:23.676.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.457 (0.458) seconds
Test Suite 'AccessSensitiveRuntimeReadinessTests' passed at 2026-09-08 20:45:23.700.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.024 (0.024) seconds
Test Suite 'AdminAccessRequestCellTests' passed at 2026-09-08 20:45:23.720.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.019 (0.019) seconds
Test Suite 'AdminAuthenticatedVaporBridgeTransportTests' passed at 2026-09-08 20:45:23.896.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.176 (0.176) seconds
Test Suite 'AdminBridgeHandshakeAuthenticationTests' passed at 2026-09-08 20:45:23.911.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.014 (0.015) seconds
Test Suite 'AdminCatalogRoutesTests' passed at 2026-09-08 20:45:25.055.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.144 (1.145) seconds
Test Suite 'AdminControlPlaneRoutingTests' passed at 2026-09-08 20:45:25.072.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
Test Suite 'AdminCopilotWorkspaceConfigurationTests' passed at 2026-09-08 20:45:26.608.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.536 (1.537) seconds
Test Suite 'AdminCredentialPolicyTests' passed at 2026-09-08 20:45:26.610.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'AdminCredentialRevocationTests' passed at 2026-09-08 20:45:26.614.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'AdminDeploymentSupervisorCellTests' passed at 2026-09-08 20:45:26.659.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.045 (0.045) seconds
Test Suite 'AdminEntityProofPersistenceSupportTests' passed at 2026-09-08 20:45:27.172.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.513 (0.513) seconds
Test Suite 'AdminFundingCellTests' passed at 2026-09-08 20:45:27.682.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.509 (0.510) seconds
Test Suite 'AdminNodeFleetCellTests' passed at 2026-09-08 20:45:27.832.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.150 (0.151) seconds
Test Suite 'AdminOperationsMetricsTests' passed at 2026-09-08 20:45:28.155.
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.320 (0.322) seconds
Test Suite 'AdminPersistedRuntimeReadinessTests' passed at 2026-09-08 20:45:28.477.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.322 (0.323) seconds
Test Suite 'AdminRoleEnrollmentCellTests' passed at 2026-09-08 20:45:28.485.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.008 (0.008) seconds
Test Suite 'AdminScaffoldBootstrapTests' passed at 2026-09-08 20:45:28.502.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
Test Suite 'AdminScaffoldBridgeMultiplexRouteTests' passed at 2026-09-08 20:45:28.508.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.005 (0.006) seconds
Test Suite 'AdminScaffoldRuntimeTests' passed at 2026-09-08 20:45:28.738.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.229 (0.230) seconds
Test Suite 'AdminScaffoldSnapshotIngestTests' passed at 2026-09-08 20:45:28.751.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
Test Suite 'AdminSecurityPolicyCellTests' passed at 2026-09-08 20:45:28.756.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'AdminWorkspaceConfigurationFactoryTests' passed at 2026-09-08 20:45:28.770.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.014 (0.015) seconds
Test Suite 'AgeProofDoorCellTests' passed at 2026-09-08 20:45:28.774.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'AgentActionCapabilityCatalogV1Tests' passed at 2026-09-08 20:45:29.605.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.831 (0.831) seconds
Test Suite 'AgentConversationInboxCellTests' passed at 2026-09-08 20:45:29.633.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.027 (0.027) seconds
Test Suite 'AgreementWorkbenchCellTests' passed at 2026-09-08 20:45:29.834.
	 Executed 21 tests, with 0 failures (0 unexpected) in 0.200 (0.201) seconds
Test Suite 'AgreementWorkbenchConfigurationFactoryTests' passed at 2026-09-08 20:45:29.848.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
Test Suite 'AppTests' passed at 2026-09-08 20:45:30.540.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.692 (0.692) seconds
Test Suite 'ArendalsukaConfigurationPublisherAuthorizationRoutesTests' passed at 2026-09-08 20:45:30.818.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.278 (0.278) seconds
Test Suite 'ArendalsukaConfigurationPublisherCellTests' passed at 2026-09-08 20:45:31.467.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.649 (0.649) seconds
Test Suite 'ArendalsukaEventAtlasCellTests' failed at 2026-09-08 20:45:32.558.
	 Executed 40 tests, with 14 failures (0 unexpected) in 1.088 (1.091) seconds
Test Suite 'ArendalsukaImportAuthorizationRoutesTests' failed at 2026-09-08 20:45:32.872.
	 Executed 1 test, with 3 failures (0 unexpected) in 0.314 (0.314) seconds
Test Suite 'ArendalsukaKnowledgeCellTests' passed at 2026-09-08 20:45:32.881.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'ArendalsukaKnowledgeSQLiteStoreTests' passed at 2026-09-08 20:45:32.892.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'ArendalsukaPersistedAtlasRecoveryTests' passed at 2026-09-08 20:45:38.007.
	 Executed 9 tests, with 0 failures (0 unexpected) in 5.114 (5.115) seconds
Test Suite 'ArendalsukaPublicSurfaceRouteTests' passed at 2026-09-08 20:45:38.028.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.020 (0.020) seconds
Test Suite 'ArtistSalesChannelCellTests' passed at 2026-09-08 20:45:38.086.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.058 (0.059) seconds
Test Suite 'AssistantCorrespondenceAdminRoutesTests' passed at 2026-09-08 20:45:38.976.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.889 (0.890) seconds
Test Suite 'AssistantCorrespondenceCellTests' passed at 2026-09-08 20:45:39.135.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.158 (0.159) seconds
Test Suite 'AssistantCorrespondenceOnboardingRoutesTests' passed at 2026-09-08 20:45:39.381.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.246 (0.246) seconds
Test Suite 'AssociatedDomainsRouteTests' passed at 2026-09-08 20:45:39.387.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'BookReferenceRoutesTests' failed at 2026-09-08 20:45:49.472.
	 Executed 6 tests, with 2 failures (0 unexpected) in 10.084 (10.085) seconds
Test Suite 'BrowserClientIdentityOfflineInspectorTests' passed at 2026-09-08 20:45:49.539.
	 Executed 20 tests, with 0 failures (0 unexpected) in 0.066 (0.067) seconds
Test Suite 'BrowserClientIdentityReconciliationTests' passed at 2026-09-08 20:45:49.543.
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'BrowserClientIdentityRecoveryExecutorTests' passed at 2026-09-08 20:45:49.686.
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.131 (0.143) seconds
Test Suite 'BrowserClientIdentityVaultKeyAgreementTests' passed at 2026-09-08 20:45:49.687.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'BrowserClientIdentityVaultTests' passed at 2026-09-08 20:45:50.133.
	 Executed 31 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.444 (0.446) seconds
Test Suite 'ButterpopPilotReadinessTests' passed at 2026-09-08 20:45:50.135.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'ButterpopStudioProductTests' failed at 2026-09-08 20:45:54.575.
	 Executed 11 tests, with 18 failures (1 unexpected) in 4.440 (4.440) seconds
Test Suite 'CalendarSurfaceConfigurationTests' passed at 2026-09-08 20:45:54.593.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.017 (0.018) seconds
Test Suite 'CellConfigurationStudioImportTests' passed at 2026-09-08 20:45:54.861.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.267 (0.268) seconds
Test Suite 'CellProtocolIdentityProofTests' passed at 2026-09-08 20:45:54.867.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'CellScaffoldRuntimeIdentityManifestTests' passed at 2026-09-08 20:45:55.014.
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.146 (0.147) seconds
Test Suite 'CellScaffoldRuntimeIdentityMigrationCandidateCommandTests' passed at 2026-09-08 20:45:55.080.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.066 (0.066) seconds
Test Suite 'CellScaffoldRuntimeIdentityMigrationPlannerTests' passed at 2026-09-08 20:45:55.095.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
Test Suite 'CellScaffoldRuntimeIdentityProvisionerTests' passed at 2026-09-08 20:45:55.226.
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.129 (0.131) seconds
Test Suite 'CellScaffoldRuntimeIdentityRegistryTests' passed at 2026-09-08 20:45:55.291.
	 Executed 21 tests, with 0 failures (0 unexpected) in 0.064 (0.065) seconds
Test Suite 'CellScaffoldRuntimeStorageRootTests' passed at 2026-09-08 20:45:55.295.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'CellScaffoldServiceIdentityManifestTests' passed at 2026-09-08 20:45:55.301.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'CellScaffoldServiceIdentityRegistryTests' passed at 2026-09-08 20:45:55.322.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.021 (0.021) seconds
Test Suite 'ChatAIGatewayDiscoveryCacheTests' passed at 2026-09-08 20:45:55.323.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'ChatAuthTokenManagerTests' passed at 2026-09-08 20:45:55.324.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'ChatCellTests' passed at 2026-09-08 20:45:55.366.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.041 (0.041) seconds
Test Suite 'ChatInterpreterEscalationCeilingTests' passed at 2026-09-08 20:45:55.375.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'ChatMVPLoginScopingTests' passed at 2026-09-08 20:45:56.129.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.754 (0.754) seconds
Test Suite 'ChatMVPRoutesTests' failed at 2026-09-08 20:46:00.534.
	 Executed 10 tests, with 7 failures (0 unexpected) in 4.404 (4.405) seconds
Test Suite 'ChatPurposeResourceRouterTests' passed at 2026-09-08 20:46:01.074.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.536 (0.539) seconds
Test Suite 'ChatScopedAIProviderRegistryPersistenceTests' passed at 2026-09-08 20:46:01.160.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.086 (0.086) seconds
Test Suite 'ChatScopedAIProviderRouterTests' passed at 2026-09-08 20:46:01.179.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.017 (0.019) seconds
Test Suite 'CodableTests' passed at 2026-09-08 20:46:01.181.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'ConciergeKnowledgeCorpusCellTests' passed at 2026-09-08 20:46:01.320.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.139 (0.140) seconds
Test Suite 'ConferenceAIAssistantConfigurationTests' passed at 2026-09-08 20:46:01.337.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
Test Suite 'ConferenceAgendaCellTests' passed at 2026-09-08 20:46:01.475.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.138 (0.138) seconds
Test Suite 'ConferenceAudienceDiscoveryCellTests' passed at 2026-09-08 20:46:01.611.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.135 (0.136) seconds
Test Suite 'ConferenceBroadcastStudioCellTests' passed at 2026-09-08 20:46:01.663.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.052 (0.052) seconds
Test Suite 'ConferenceConfigurationCatalogTests' passed at 2026-09-08 20:46:05.109.
	 Executed 3 tests, with 0 failures (0 unexpected) in 3.446 (3.446) seconds
Test Suite 'ConferenceConnectionHubCellTests' passed at 2026-09-08 20:46:05.345.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.236 (0.236) seconds
Test Suite 'ConferenceDemoStoryCellTests' passed at 2026-09-08 20:46:05.416.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.071 (0.071) seconds
Test Suite 'ConferenceEntityDiscoveryCellTests' failed at 2026-09-08 20:46:05.560.
	 Executed 11 tests, with 1 failure (1 unexpected) in 0.143 (0.143) seconds
Test Suite 'ConferenceInsightAggregateCellTests' passed at 2026-09-08 20:46:05.579.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.019 (0.019) seconds
Test Suite 'ConferenceLiveInteractionShellBridgeTests' passed at 2026-09-08 20:46:05.602.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.023 (0.023) seconds
Test Suite 'ConferenceMVPSkeletonTests' passed at 2026-09-08 20:46:05.604.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ConferenceMessageExchangeAcceptanceTests' passed at 2026-09-08 20:46:05.783.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.180 (0.180) seconds
Test Suite 'ConferenceOnboardingCellTests' passed at 2026-09-08 20:46:05.832.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.049 (0.049) seconds
Test Suite 'ConferenceOrganizerProjectionCellTests' failed at 2026-09-08 20:46:05.906.
	 Executed 3 tests, with 7 failures (0 unexpected) in 0.073 (0.073) seconds
Test Suite 'ConferencePlaywrightIdentityVaultTests' passed at 2026-09-08 20:46:05.959.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.053 (0.053) seconds
Test Suite 'ConferencePreviewWrapperResolverSupportTests' passed at 2026-09-08 20:46:07.579.
	 Executed 6 tests, with 0 failures (0 unexpected) in 1.620 (1.620) seconds
Test Suite 'ConferenceProofChatLaunchCellTests' passed at 2026-09-08 20:46:07.606.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.027 (0.027) seconds
Test Suite 'ConferencePublicProfileCellTests' passed at 2026-09-08 20:46:08.129.
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.522 (0.523) seconds
Test Suite 'ConferencePublicShellReadinessTests' passed at 2026-09-08 20:46:08.553.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.424 (0.424) seconds
Test Suite 'ConferencePublishedContentCellTests' failed at 2026-09-08 20:46:08.608.
	 Executed 10 tests, with 1 failure (1 unexpected) in 0.054 (0.055) seconds
Test Suite 'ConferenceRecommendationCellTests' passed at 2026-09-08 20:46:08.661.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.053 (0.053) seconds
Test Suite 'ConferenceRegistrationCellTests' passed at 2026-09-08 20:46:08.674.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
Test Suite 'ConferenceSchedulingCellTests' failed at 2026-09-08 20:46:08.711.
	 Executed 2 tests, with 1 failure (0 unexpected) in 0.037 (0.037) seconds
Test Suite 'ConferenceShellCellsTests' passed at 2026-09-08 20:46:14.163.
	 Executed 68 tests, with 0 failures (0 unexpected) in 5.447 (5.452) seconds
Test Suite 'ConferenceShellConfigurationFactoryTests' passed at 2026-09-08 20:46:14.438.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.275 (0.275) seconds
Test Suite 'ConferenceSimulationClockCellTests' passed at 2026-09-08 20:46:14.441.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ConferenceSimulationPlaybackCellTests' passed at 2026-09-08 20:46:14.550.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.110 (0.110) seconds
Test Suite 'ConferenceSimulationPopulationCellTests' passed at 2026-09-08 20:46:14.908.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.357 (0.357) seconds
Test Suite 'ConferenceSimulationStudioCellTests' passed at 2026-09-08 20:46:14.920.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
Test Suite 'ConferenceSponsorLeadAggregateCellTests' failed at 2026-09-08 20:46:14.930.
	 Executed 2 tests, with 1 failure (1 unexpected) in 0.009 (0.010) seconds
Test Suite 'ConferenceSurfaceRoutesTests' failed at 2026-09-08 20:47:03.460.
	 Executed 39 tests, with 21 failures (0 unexpected) in 48.527 (48.530) seconds
Test Suite 'ConfigurationArchitectWorkspaceTests' passed at 2026-09-08 20:47:03.485.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.025 (0.025) seconds
Test Suite 'ConfigurationCatalogCellTests' passed at 2026-09-08 20:47:05.401.
	 Executed 31 tests, with 0 failures (0 unexpected) in 1.914 (1.916) seconds
Test Suite 'ConfigurationCatalogClientTests' passed at 2026-09-08 20:47:05.405.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'ConfigurationCatalogSkeletonParityTests' failed at 2026-09-08 20:47:05.889.
	 Executed 17 tests, with 2 tests skipped and 1 failure (0 unexpected) in 0.484 (0.485) seconds
Test Suite 'ContactEndpointCellTests' passed at 2026-09-08 20:47:07.572.
	 Executed 14 tests, with 0 failures (0 unexpected) in 1.681 (1.683) seconds
Test Suite 'ContactRegistryCellTests' passed at 2026-09-08 20:47:07.592.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.020 (0.021) seconds
Test Suite 'ContextTransitionPayloadFactoryTests' passed at 2026-09-08 20:47:07.593.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'ContractChallengeMVPRoutesTests' failed at 2026-09-08 20:47:08.794.
	 Executed 5 tests, with 9 failures (0 unexpected) in 1.200 (1.200) seconds
Test Suite 'CredentialSealingTests' passed at 2026-09-08 20:47:08.795.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'DevelopmentStatusRoutesTests' passed at 2026-09-08 20:47:10.901.
	 Executed 5 tests, with 0 failures (0 unexpected) in 2.106 (2.106) seconds
Test Suite 'DevelopmentStatusSnapshotProducerTests' passed at 2026-09-08 20:47:11.123.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.222 (0.223) seconds
Test Suite 'DevelopmentStatusSnapshotTests' passed at 2026-09-08 20:47:11.169.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.045 (0.046) seconds
Test Suite 'DeviceCallbackCapabilityServerTests' passed at 2026-09-08 20:47:11.234.
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.064 (0.065) seconds
Test Suite 'DeviceRegistrationReadinessTests' passed at 2026-09-08 20:47:11.246.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
Test Suite 'DocumentationWorkbenchRoutesTests' passed at 2026-09-08 20:47:11.466.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.219 (0.220) seconds
Test Suite 'EntityAnchorDataV1ContractTests' passed at 2026-09-08 20:47:11.705.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.239 (0.240) seconds
Test Suite 'EntityAtlasRoutesTests' passed at 2026-09-08 20:47:12.164.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.459 (0.459) seconds
Test Suite 'EntityCellGraphCellTests' passed at 2026-09-08 20:47:12.186.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.021 (0.022) seconds
Test Suite 'EntityGraphStorageTests' passed at 2026-09-08 20:47:12.188.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'EntityMergePolicyRegistryV0Tests' passed at 2026-09-08 20:47:12.235.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.046 (0.046) seconds
Test Suite 'EntityOperationEnvelopeV0Tests' passed at 2026-09-08 20:47:12.266.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.031 (0.032) seconds
Test Suite 'EntityScaffoldEnrollmentCellTests' passed at 2026-09-08 20:47:12.467.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.200 (0.201) seconds
Test Suite 'EntityStudioCellTests' passed at 2026-09-08 20:47:12.792.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.323 (0.324) seconds
Test Suite 'EntityStudioConfigurationFactoryTests' passed at 2026-09-08 20:47:12.806.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.014 (0.015) seconds
Test Suite 'EventPlatformRoutesTests' passed at 2026-09-08 20:47:14.501.
	 Executed 6 tests, with 0 failures (0 unexpected) in 1.695 (1.695) seconds
Test Suite 'EventPublisherRegistryCellTests' passed at 2026-09-08 20:47:14.513.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'ExecutablePurposeGroundingCellTests' passed at 2026-09-08 20:47:15.810.
	 Executed 36 tests, with 0 failures (0 unexpected) in 1.275 (1.297) seconds
Test Suite 'FlowDebugProbeCellTests' passed at 2026-09-08 20:47:15.847.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.036 (0.037) seconds
Test Suite 'FundingEntitlementAgreementTests' passed at 2026-09-08 20:47:15.849.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'GitHubWorkSyncCellTests' passed at 2026-09-08 20:47:15.852.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'GraphStoreCellTests' passed at 2026-09-08 20:47:16.122.
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.268 (0.269) seconds
Test Suite 'GuidedOnboardingCellTests' passed at 2026-09-08 20:47:16.308.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.186 (0.186) seconds
Test Suite 'HAVENAgentCapabilityBrokerCellTests' passed at 2026-09-08 20:47:16.405.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.096 (0.097) seconds
Test Suite 'HavenWorkbenchConfigurationTests' failed at 2026-09-08 20:47:16.495.
	 Executed 6 tests, with 1 failure (0 unexpected) in 0.089 (0.090) seconds
Test Suite 'IdeaTaskWorkspaceTests' passed at 2026-09-08 20:47:17.542.
	 Executed 20 tests, with 0 failures (0 unexpected) in 1.046 (1.048) seconds
Test Suite 'JWTAuthRoutesTests' passed at 2026-09-08 20:47:29.866.
	 Executed 13 tests, with 0 failures (0 unexpected) in 12.323 (12.324) seconds
Test Suite 'LeadVaultCellTests' passed at 2026-09-08 20:47:29.875.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.008 (0.009) seconds
Test Suite 'LeadVaultRoutesTests' passed at 2026-09-08 20:47:30.516.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.640 (0.641) seconds
Test Suite 'LiveInteractionCellTests' passed at 2026-09-08 20:47:30.640.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.124 (0.124) seconds
Test Suite 'LocalLLMGatewayCellTests' passed at 2026-09-08 20:47:30.652.
	 Executed 4 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.012 (0.012) seconds
Test Suite 'MVPAdminAccessTests' passed at 2026-09-08 20:47:30.655.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'MarkdownRendererCellTests' passed at 2026-09-08 20:47:30.680.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.024 (0.024) seconds
Test Suite 'MediaCollectionCellTests' passed at 2026-09-08 20:47:30.713.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.032 (0.033) seconds
Test Suite 'MermaidRendererCellTests' failed at 2026-09-08 20:47:46.123.
	 Executed 11 tests, with 14 failures (0 unexpected) in 15.409 (15.411) seconds
Test Suite 'MicropaymentsAuditRoutesTests' passed at 2026-09-08 20:47:47.190.
	 Executed 2 tests, with 0 failures (0 unexpected) in 1.066 (1.067) seconds
Test Suite 'MicropaymentsMVPRoutesTests' failed at 2026-09-08 20:47:47.433.
	 Executed 1 test, with 4 failures (0 unexpected) in 0.243 (0.243) seconds
Test Suite 'MintClientBootstrapTests' passed at 2026-09-08 20:47:47.434.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'MultilevelCodableTests' passed at 2026-09-08 20:47:47.436.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'MusicPublishingCellsTests' failed at 2026-09-08 20:47:47.586.
	 Executed 26 tests, with 3 failures (0 unexpected) in 0.149 (0.151) seconds
Test Suite 'MusicPublishingConfigurationFactoryTests' passed at 2026-09-08 20:47:47.646.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.060 (0.060) seconds
Test Suite 'MusicPublishingMVPRoutesTests' passed at 2026-09-08 20:47:47.944.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.298 (0.298) seconds
Test Suite 'NativeLocalModelBridgeTests' passed at 2026-09-08 20:47:47.945.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'NodeAdminAgentDeliveryTests' passed at 2026-09-08 20:47:47.946.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'NodeAdminAgentSnapshotBuilderTests' passed at 2026-09-08 20:47:49.378.
	 Executed 8 tests, with 0 failures (0 unexpected) in 1.431 (1.433) seconds
Test Suite 'NodeAdminDockerCollectorTests' passed at 2026-09-08 20:47:49.433.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.055 (0.055) seconds
Test Suite 'NotificationPushProviderTests' passed at 2026-09-08 20:47:49.659.
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.224 (0.225) seconds
Test Suite 'NotificationRuntimeReadinessTests' passed at 2026-09-08 20:47:49.727.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.068 (0.068) seconds
Test Suite 'ObjectStorageAdapterCellTests' passed at 2026-09-08 20:47:49.765.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.037 (0.038) seconds
Test Suite 'ObsidianAIWorkspaceConfigurationTests' passed at 2026-09-08 20:47:49.780.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
Test Suite 'OrchestratorPersistenceTests' passed at 2026-09-08 20:47:53.398.
	 Executed 7 tests, with 0 failures (0 unexpected) in 3.617 (3.618) seconds
Test Suite 'OwnerScopedCredentialCellTests' passed at 2026-09-08 20:47:53.453.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.055 (0.055) seconds
Test Suite 'OwnerScopedCredentialStoreTests' passed at 2026-09-08 20:47:53.479.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.025 (0.026) seconds
Test Suite 'PalazzoCommunaleRoutesTests' passed at 2026-09-08 20:47:53.728.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.250 (0.250) seconds
Test Suite 'PalazzoCommunaleServiceTests' passed at 2026-09-08 20:47:53.753.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.024 (0.025) seconds
Test Suite 'ParticipationHubCellTests' passed at 2026-09-08 20:47:53.792.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.039 (0.039) seconds
Test Suite 'ParticipationHubConfigurationFactoryTests' passed at 2026-09-08 20:47:53.805.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
Test Suite 'PaymentAccessCredentialStoreLifecycleTests' passed at 2026-09-08 20:47:56.062.
	 Executed 13 tests, with 0 failures (0 unexpected) in 2.257 (2.257) seconds
Test Suite 'PaymentGateCellTests' passed at 2026-09-08 20:47:58.315.
	 Executed 14 tests, with 0 failures (0 unexpected) in 2.252 (2.253) seconds
Test Suite 'PaymentGateOwnerIdentitySupportTests' passed at 2026-09-08 20:47:58.322.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
Test Suite 'PaymentProofDoorCellTests' passed at 2026-09-08 20:47:58.339.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
Test Suite 'PersistedRuntimeReadinessTests' passed at 2026-09-08 20:47:59.055.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.715 (0.716) seconds
Test Suite 'PersonalAIProviderPolicyTests' passed at 2026-09-08 20:47:59.063.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.007 (0.008) seconds
Test Suite 'PersonalAssistantProfileCellTests' passed at 2026-09-08 20:47:59.093.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.030 (0.030) seconds
Test Suite 'PersonalChatPromptEvaluationTests' passed at 2026-09-08 20:48:32.871.
	 Executed 11 tests, with 0 failures (0 unexpected) in 33.776 (33.778) seconds
Test Suite 'PersonalCopilotCollaborationInviteTests' passed at 2026-09-08 20:48:33.059.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.187 (0.188) seconds
Test Suite 'PersonalCopilotV1Tests' passed at 2026-09-08 20:48:44.669.
	 Executed 70 tests, with 0 failures (0 unexpected) in 11.606 (11.611) seconds
Test Suite 'PersonalDataTrustPackageCellTests' passed at 2026-09-08 20:48:44.684.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
Test Suite 'PersonalEntityActivityDashboardConfigurationTests' passed at 2026-09-08 20:48:45.339.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.654 (0.655) seconds
Test Suite 'PersonalPagePublisherCellTests' passed at 2026-09-08 20:48:45.361.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.022 (0.022) seconds
Test Suite 'PersonalPagePublisherConfigurationTests' passed at 2026-09-08 20:48:45.364.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'PersonlogProjectionCellTests' passed at 2026-09-08 20:48:45.471.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.107 (0.107) seconds
Test Suite 'PerspectiveCellTests' passed at 2026-09-08 20:48:45.481.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'PortholeBootstrapProjectionTests' passed at 2026-09-08 20:48:45.498.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
Test Suite 'PortholeConfigurationLoadingTests' failed at 2026-09-08 20:58:42.346.
	 Executed 45 tests, with 2 failures (0 unexpected) in 596.843 (596.848) seconds
Test Suite 'PortholeIdentityContinuityRoutesTests' passed at 2026-09-08 20:58:54.285.
	 Executed 4 tests, with 0 failures (0 unexpected) in 11.939 (11.939) seconds
Test Suite 'PortholeMenuFallbackTests' passed at 2026-09-08 20:58:54.416.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.130 (0.130) seconds
Test Suite 'PortholeRuntimeBindingEnsuringTests' passed at 2026-09-08 20:58:57.803.
	 Executed 10 tests, with 0 failures (0 unexpected) in 3.386 (3.387) seconds
Test Suite 'PortholeWebActionStateSourceTests' passed at 2026-09-08 20:58:57.814.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'PortholeWebEditorSupportTests' passed at 2026-09-08 20:58:57.821.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.007 (0.008) seconds
Test Suite 'PortholeWebPayloadTests' passed at 2026-09-08 20:58:57.888.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.067 (0.067) seconds
Test Suite 'PortholeWebSessionPersonaTests' passed at 2026-09-08 20:59:00.806.
	 Executed 15 tests, with 0 failures (0 unexpected) in 2.917 (2.918) seconds
Test Suite 'ProductionOwnerIdentityContinuityTests' passed at 2026-09-08 20:59:00.813.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
Test Suite 'ProductionRuntimeAdmissionMiddlewareTests' passed at 2026-09-08 20:59:00.826.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.012 (0.013) seconds
Test Suite 'ProductionSkeletonBindingIntegrityTests' failed at 2026-09-08 20:59:08.594.
	 Executed 4 tests, with 19 failures (1 unexpected) in 7.767 (7.768) seconds
Test Suite 'ProjectOperationsTests' passed at 2026-09-08 20:59:08.642.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.048 (0.048) seconds
Test Suite 'ProjectPortfolioCellTests' passed at 2026-09-08 20:59:08.683.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.041 (0.041) seconds
Test Suite 'ProofDoorMVPRouteSecurityTests' passed at 2026-09-08 20:59:08.686.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'PublishedConfigurationCatalogCellTests' passed at 2026-09-08 20:59:08.826.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.140 (0.140) seconds
Test Suite 'PurposeQualityMonitorCellTests' passed at 2026-09-08 20:59:08.837.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.010 (0.011) seconds
Test Suite 'QuestionnaireCampaignCellTests' passed at 2026-09-08 20:59:08.969.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.132 (0.132) seconds
Test Suite 'QuestionnaireCampaignRoutesTests' passed at 2026-09-08 20:59:10.043.
	 Executed 2 tests, with 0 failures (0 unexpected) in 1.074 (1.074) seconds
Test Suite 'QuestionnaireResponseCellTests' passed at 2026-09-08 20:59:10.055.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
Test Suite 'RAGCellAccessSecurityTests' passed at 2026-09-08 20:59:10.066.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'RAGGatewayCellTests' passed at 2026-09-08 20:59:10.088.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.021 (0.022) seconds
Test Suite 'RAGGatewayConfigTests' passed at 2026-09-08 20:59:10.089.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'RAGGatewayConfigurationFactoryTests' passed at 2026-09-08 20:59:10.090.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'RAGGatewayHTTPClientTests' passed at 2026-09-08 20:59:10.096.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.005 (0.006) seconds
Test Suite 'RAGIngestionCellTests' passed at 2026-09-08 20:59:10.105.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'RAGMVPRoutesTests' passed at 2026-09-08 20:59:11.201.
	 Executed 5 tests, with 0 failures (0 unexpected) in 1.096 (1.096) seconds
Test Suite 'RAGPersistedRuntimeReadinessTests' passed at 2026-09-08 20:59:11.280.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.078 (0.078) seconds
Test Suite 'RAGPromptAdminCellTests' passed at 2026-09-08 20:59:11.305.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.024 (0.025) seconds
Test Suite 'RAGPromptAdminConfigurationFactoryTests' passed at 2026-09-08 20:59:11.305.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'RemoteBridgeheadAccessTests' passed at 2026-09-08 20:59:11.308.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'RestaurantExperiencePlanCellTests' passed at 2026-09-08 20:59:11.323.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
Test Suite 'RestaurantOnboardingCellTests' passed at 2026-09-08 20:59:11.327.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'RestaurantPublishedContentCellTests' passed at 2026-09-08 20:59:11.333.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'RestaurantShellCellsTests' passed at 2026-09-08 20:59:11.362.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.029 (0.029) seconds
Test Suite 'RestaurantSurfaceRoutesTests' passed at 2026-09-08 20:59:12.936.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.574 (1.574) seconds
Test Suite 'RestaurantVisitContextCellTests' passed at 2026-09-08 20:59:12.942.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'SMIAgreementSettlementCellTests' passed at 2026-09-08 20:59:12.970.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.028 (0.028) seconds
Test Suite 'SalesWorkspaceCellTests' passed at 2026-09-08 20:59:13.006.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.035 (0.036) seconds
Test Suite 'ScaffoldLaunchRegistryCellTests' passed at 2026-09-08 20:59:13.050.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.044 (0.044) seconds
Test Suite 'ScaffoldNotificationContractsTests' passed at 2026-09-08 20:59:13.053.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.002 (0.003) seconds
Test Suite 'ScaffoldOwnerAdminRoutesTests' passed at 2026-09-08 20:59:14.768.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.715 (1.715) seconds
Test Suite 'ScaffoldSetupCellTests' passed at 2026-09-08 20:59:18.148.
	 Executed 15 tests, with 0 failures (0 unexpected) in 3.378 (3.380) seconds
Test Suite 'ScaffoldSurfaceGatePolicyTests' passed at 2026-09-08 20:59:18.202.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.053 (0.053) seconds
Test Suite 'ScaffoldTruthSourceCatalogTests' passed at 2026-09-08 20:59:18.205.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'SecureDevelopmentStatusSnapshotFileTests' passed at 2026-09-08 20:59:18.222.
	 Executed 9 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.017 (0.017) seconds
Test Suite 'SecureRuntimeIdentityManifestFileTests' passed at 2026-09-08 20:59:18.239.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
Test Suite 'SecurityWorkbenchCellTests' passed at 2026-09-08 20:59:18.264.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.024 (0.025) seconds
Test Suite 'SkeletonElementParityMatrixTests' failed at 2026-09-08 20:59:18.613.
	 Executed 3 tests, with 2 failures (0 unexpected) in 0.349 (0.349) seconds
Test Suite 'SkeletonParityRoutesTests' passed at 2026-09-08 20:59:19.567.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.954 (0.954) seconds
Test Suite 'SkeletonPortableModelTests' passed at 2026-09-08 20:59:19.613.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.046 (0.046) seconds
Test Suite 'SkeletonRuntimeDecoderTests' passed at 2026-09-08 20:59:19.615.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'SkeletonRuntimeSourceTests' failed at 2026-09-08 20:59:19.769.
	 Executed 16 tests, with 1 failure (0 unexpected) in 0.153 (0.154) seconds
Test Suite 'SkeletonStyleParityCSSDriftTests' passed at 2026-09-08 20:59:19.789.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.020 (0.020) seconds
Test Suite 'SpatialCellsTests' passed at 2026-09-08 20:59:19.804.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.014 (0.015) seconds
Test Suite 'SpatialRegistryRemoteIntegrationTests' passed at 2026-09-08 20:59:19.804.
	 Executed 1 test, with 1 test skipped and 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'SproutBridgeDiscoveryRoutesTests' passed at 2026-09-08 20:59:21.085.
	 Executed 5 tests, with 0 failures (0 unexpected) in 1.280 (1.281) seconds
Test Suite 'SproutExecutableCatalogRoutesTests' passed at 2026-09-08 20:59:21.339.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.254 (0.255) seconds
Test Suite 'SproutResolverRoutesTests' passed at 2026-09-08 20:59:22.013.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.673 (0.673) seconds
Test Suite 'StrictIdentityVaultReadinessMonitorTests' passed at 2026-09-08 20:59:22.014.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'SwarmIdentityAdmissionCellTests' passed at 2026-09-08 20:59:22.052.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.038 (0.039) seconds
Test Suite 'TodoCellConfigurationTests' passed at 2026-09-08 20:59:22.053.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'TodoPlannerCopilotConfigurationTests' passed at 2026-09-08 20:59:22.068.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
Test Suite 'TopUpCheckoutTests' failed at 2026-09-08 20:59:24.851.
	 Executed 19 tests, with 3 failures (3 unexpected) in 2.782 (2.783) seconds
Test Suite 'TranscriptStoreCellTests' passed at 2026-09-08 20:59:24.884.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.033 (0.033) seconds
Test Suite 'TrustPacketConfigurationFactoryTests' passed at 2026-09-08 20:59:24.992.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.108 (0.108) seconds
Test Suite 'UserSimulationScaffoldTests' passed at 2026-09-08 20:59:27.339.
	 Executed 28 tests, with 1 test skipped and 0 failures (0 unexpected) in 2.341 (2.347) seconds
Test Suite 'VaporProductControlDurabilityTests' passed at 2026-09-08 20:59:27.394.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.054 (0.055) seconds
Test Suite 'VaultMVPRoutesTests' passed at 2026-09-08 20:59:30.511.
	 Executed 6 tests, with 0 failures (0 unexpected) in 3.117 (3.117) seconds
Test Suite 'VaultStudioWorkspaceTests' passed at 2026-09-08 20:59:30.534.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.023 (0.023) seconds
Test Suite 'WebKnowledgeCellsTests' passed at 2026-09-08 20:59:30.568.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.033 (0.033) seconds
Test Suite 'WorkItemCellTests' passed at 2026-09-08 20:59:30.593.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.025 (0.025) seconds
Test Suite 'WorkbenchAccessGrantConfigurationTests' failed at 2026-09-08 20:59:33.018.
	 Executed 24 tests, with 1 failure (1 unexpected) in 2.423 (2.425) seconds
Test Suite 'WorkbenchOwnerSetupCellTests' passed at 2026-09-08 20:59:40.733.
	 Executed 7 tests, with 0 failures (0 unexpected) in 7.715 (7.715) seconds
Test Suite 'CellsContainerPackageTests.xctest' failed at 2026-09-08 20:59:40.733.
	 Executed 2046 tests, with 11 tests skipped and 148 failures (9 unexpected) in 859.566 (859.744) seconds
Test Suite 'All tests' failed at 2026-09-08 20:59:40.734.
	 Executed 2046 tests, with 11 tests skipped and 148 failures (9 unexpected) in 859.566 (859.746) seconds
```

</details>

Midlertidige fullstendige logger og måledata: `/private/tmp/wp0c-baseline-ujg4x43v/` (`diagnostics.json`, og `CellProtocol`/`CellScaffold` × `build`/`test-skip-build`/`xctest`, hver med `.log` og `.json`). De relevante feilene, alle røde testnavn og alle `Executed`-linjer er bevart i dette dokumentet. Ingen kjøringer ble avbrutt; ingen kodeendringer eller git-kommandoer ble utført.

## WP0 — sluttmelding

WP0 baseline er **blocked**. `swift build` og `swift test` er forsøkt i begge repoer; alle fire avsluttet med exit-kode 1 på `sandbox-exec: sandbox_apply: Operation not permitted`. Ingen tester ble kjørt, så antall røde og røde testnavn kunne ikke fastslås. Kommandoer, målte varigheter og ekte feilutdata er dokumentert over.

`STATUS.md` er oppdatert med én linje under «Logg». Ingen kodeendringer, git-kommandoer eller arbeid på andre slicer er utført.

## WP0b — sluttmelding

WP0b baseline er **blocked** ved testlasting. `swift build --disable-sandbox` er grønn i begge repoer; `swift test --disable-sandbox` avslutter med exit 1 i begge fordi XCTest-pakken har `arm64`, mens lasteren krever `x86_64`. **0 tester utført per repo; antall røde ikke målbart; ingen røde testnavn rapportert.** Kommandoer, målte varigheter og ekte utdata er dokumentert i [baseline](#baseline).

`STATUS.md` er oppdatert med én linje under «Logg». Ingen kodeendringer, reparasjonsforsøk eller git-kommandoer er utført.

## WP0c — sluttmelding

WP0c er dokumentert: ny SwiftPM-bygg/test-baseline er **blocked** fordi manifestkompileringen ikke får skrive til `~/.cache/clang/ModuleCache` (`Operation not permitted`). Begge `arch -arm64`-bygg og ett `--skip-build`-forsøk per repo feilet på dette. Testleddene etter `&&` ble ikke startet.

Reservekommandoen `xcrun --sdk macosx xctest <bundle>` **virket for lasting og full testkjøring** av begge eksisterende bundler, uten WP0b sin arkitekturfeil. Resultatene er røde: **CellProtocol: 1060 tester, 8 hoppet over, 6 feil i 6 testtilfeller; CellScaffold: 2046 tester, 11 hoppet over, 148 feil i 46 testtilfeller.** Direktekjøringene tok henholdsvis **125.406 s** og **862.311 s**. Alle røde testnavn, ekte utdata og kommandotider står i [baseline](#baseline). Bundlene ble ikke bygget på nytt; dette er ingen bekreftelse på grønt bygg av gjeldende kildekode.

Arkitekturdiagnostikken viser `arm64` for kommandomiljøet og Codex-binærfilen. `sysctl.proc_translated` er **blocked** av sandkassen, så Rosetta-hypotesen er ikke bekreftet. `STATUS.md` har fått én linje under «Logg». Ingen kodeendringer eller git-kommandoer er utført.

## Projeksjon <a id="projeksjon"></a>

purposeRef: `purpose://candidate.tillitspakke-agentflaate.projeksjon`. Kun WP1.

### Baseline før WP1-endring

2026-09-08: Kommandoen fra regel 10 ble forsøkt før kodeendring fra `CellProtocol`, startet via Python `subprocess.run` for tidsmåling:

```sh
xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest
```

`blocked`: exit 80, 0 tester lastet, ingen `Executed`-linje. WP0c (1060 tester, 8 hoppet, 6 feil) beholdes som historisk sammenligningsgrunnlag. Ekte utdata:

```text
Pakken «CellProtocolPackageTests.xctest» kunne ikke lastes inn fordi den ikke inneholder en versjon for den nåværende arkitekturen. Prøv å installere en Universal-versjon av pakken.
(dlopen_preflight(/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/.build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest/Contents/MacOS/CellProtocolPackageTests) => false, tried: '/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/.build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest/Contents/MacOS/CellProtocolPackageTests' (mach-o file, but is an incompatible architecture (have 'arm64', need 'x86_64')), '/System/Volumes/Preboot/Cryptexes/OS/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/.build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest/Contents/MacOS/CellProtocolPackageTests' (no such file), '/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/.build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest/Contents/MacOS/CellProtocolPackageTests' (mach-o file, but is an incompatible architecture (have 'arm64', need 'x86_64')))
```

Diagnose innen WP1: `uname -m` fra skallet ga `arm64`, mens `python3 -c 'import platform; print(platform.machine())'` ga `x86_64`. Måle-wrapperen introduserte dermed et arkitekturavvik; forsøket over er ikke bevis for at regel 10 feiler når kommandoen startes direkte fra skallet. Videre bygg/test startes direkte, uten Python-wrapper eller `arch`-prefiks.

### Implementasjon og kontraktavgrensning

- `AgentTrustPackage` og undertyper ligger i `CellBase/Agreement/AgentTrustPackage.swift`; `modelRoute`, `instruction`, `templateGrants`, `contracts`, `ceiling` og `policy` er valgfrie per celle. De utelates ved koding når de mangler.
- `AgentTrustPackageCanonicalEncoder.encode(_:)` gir sorterte JSON-nøkler, ingen strukturell whitespace, uescapede skråstreker og uendret array-rekkefølge. `canonicalBytes(for:)` utelater bare toppnivåets `packageDigest`; `digest(for:)` bruker `PurposeBindingDigest.sha256(domain: "haven.agent-trust-package.v0", components: [canonicalBytes])`. Digest oppdateres eksplisitt på pakken før eksport.
- `generatedAt` og `expiresAt` følger eksisterende modellstil som strenger og valideres/normaliseres ved koding til RFC3339 UTC. Offset konverteres, avsluttende nuller i brøkdelen fjernes, øvrige brøkdelssekunder bevares uten avrunding. Ukjent offset `-00:00`, ugyldige datoer og ukjent schema avvises ved koding.
- Hemmelighetsvakten går rekursivt gjennom objektfelt og lister. Feltnavn med `key`, `secret`, `token`, `password` eller `prompt` avvises uten hensyn til store/små bokstaver; kun det eksakte feltnavnet `keypath` er unntatt. Verdier med nøkkelprefiksmønstrene og lange base64-lignende strenger avvises. Feilene gjengir verken avvist feltnavn eller verdi. Også vanlig `JSONEncoder().encode(package)` bruker vakten. Testverdiene er syntetiske mønstereksempler, ingen ekte credentials.
- Vakten er en konservativ mønstergjenkjenner, ikke bevis for at vilkårlig prosa er fri for hemmeligheter eller instruksjonstekst. Den kan avvise ufarlige lange identifikatorer. Modellen har ingen prompt-tekstfelt; instruksjonen er bare `keypath` + digest.
- **Fixture-avvik:** kontrakten beskriver `reach` som liste, mens `fleet-webfetch.package.json` inneholder `"see fleet-webfetch.reach.json"`. `Reach.entries` støtter kontraktens liste, og `Reach.fixtureReference` bevarer kun denne eksakte henvisningen for tapsfri round-trip. Henvisningen løses ikke; digest binder teksten, ikke innholdet i den separate filen. Listeformen testes separat med `fleet-webfetch.reach.json`. Beregning av transitiv rekkevidde tilhører WP3.
- Pakken og digest gir ingen rettigheter. WP1 verifiserer datamodell og koding av fixtures, ikke innhenting fra levende celler eller autentisering av oppgitte Contracts. Disse oppgavene ligger i senere slicer.

### Byggforsøk

De første byggforsøkene fant en navnekollisjon (`CellBase.DecodingError` skygger standardbibliotekets feiltype). Første rettingsforsøk kvalifiserte feilaktig med `Foundation`; endelig kode bruker `Swift.DecodingError`. Ekte kompileringsfeil fra de to forsøkene:

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Agreement/AgentTrustPackage.swift:210:41: error: type 'DecodingError' has no member 'dataCorruptedError'
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Agreement/AgentTrustPackage.swift:210:27: error: module 'Foundation' has no member named 'DecodingError'
```

Endelig bygg kjørt direkte fra `CellProtocol`, exit 0:

```sh
swift build --disable-sandbox --build-tests
```

```text
Build complete! (16.71s)
```

Ingen feil eller advarsler peker på de nye WP1-filene i dette bygget. Bygget rapporterte eksisterende SwiftPM-cache-/ressursadvarsler og advarsler i andre kildefiler.

### Isolert WP1-testklasse

Kjørt direkte fra `CellProtocol`, exit 0:

```sh
xcrun --sdk macosx xctest -XCTest CellBaseTests.AgentTrustPackageTests .build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest
```

Ekte utdata:

```text
Test Suite 'Selected tests' started at 2026-09-08 21:26:12.597.
Test Suite 'CellProtocolPackageTests.xctest' started at 2026-09-08 21:26:12.600.
Test Suite 'AgentTrustPackageTests' started at 2026-09-08 21:26:12.600.
Test Case '-[CellBaseTests.AgentTrustPackageTests testCanonicalKeysAreSortedCompactAndSlashesUnescaped]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testCanonicalKeysAreSortedCompactAndSlashesUnescaped]' passed (0.003 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testContractReachArrayRoundTripsAndBindsItsContents]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testContractReachArrayRoundTripsAndBindsItsContents]' passed (0.010 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testDatesNormalizeToUTCWithoutLosingFractionalPrecision]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testDatesNormalizeToUTCWithoutLosingFractionalPrecision]' passed (0.008 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testFixtureRoundTripWritesCopyWithComputedDigest]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testFixtureRoundTripWritesCopyWithComputedDigest]' passed (0.007 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testIdenticalInputProducesIdenticalCanonicalBytesAndDigest]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testIdenticalInputProducesIdenticalCanonicalBytesAndDigest]' passed (0.006 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testInvalidDatesUnknownSchemaAndUnknownReachReferenceFailClosed]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testInvalidDatesUnknownSchemaAndUnknownReachReferenceFailClosed]' passed (0.001 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testKeypathAndNonSecretReferenceValuesPass]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testKeypathAndNonSecretReferenceValuesPass]' passed (0.001 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testOmittedCellDetailsRemainAbsent]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testOmittedCellDetailsRemainAbsent]' passed (0.000 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testOneTemplateGrantPermissionChangeChangesDigest]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testOneTemplateGrantPermissionChangeChangesDigest]' passed (0.002 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testPackageDigestIsExcludedButOtherFieldsAndArrayOrderAreBound]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testPackageDigestIsExcludedButOtherFieldsAndArrayOrderAreBound]' passed (0.005 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testPlainJSONEncoderAndDigestCannotBypassPackageSecretGuard]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testPlainJSONEncoderAndDigestCannotBypassPackageSecretGuard]' passed (0.001 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testSecretGuardRejectsAPIKeyObject]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testSecretGuardRejectsAPIKeyObject]' passed (0.000 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testSecretGuardRejectsEachValuePatternEvenUnderKeypath]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testSecretGuardRejectsEachValuePatternEvenUnderKeypath]' passed (0.000 seconds).
Test Case '-[CellBaseTests.AgentTrustPackageTests testSecretGuardRejectsForbiddenNamesRecursivelyAndCaseInsensitively]' started.
Test Case '-[CellBaseTests.AgentTrustPackageTests testSecretGuardRejectsForbiddenNamesRecursivelyAndCaseInsensitively]' passed (0.000 seconds).
Test Suite 'AgentTrustPackageTests' passed at 2026-09-08 21:26:12.645.
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.045 (0.045) seconds
Test Suite 'CellProtocolPackageTests.xctest' passed at 2026-09-08 21:26:12.646.
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.045 (0.045) seconds
Test Suite 'Selected tests' passed at 2026-09-08 21:26:12.646.
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.045 (0.048) seconds
```

Generert fixture: `contract/fixtures/fleet-webfetch.package.generated.json`. Kun `packageDigest` er semantisk endret fra originalen. Digest-grunnlag: 2180 UTF-8-bytes. Beregnet digest:

```text
sha256:d6e82deda41dce717cae5f971b347ed7a50a3ffc1b71eac4ef7c04cad97209ea
```

Testen sammenligner mot en uavhengig Python `json.dumps(sort_keys=True, ensure_ascii=False, separators=(',', ':'))` + `hashlib.sha256`-beregning med samme domeneseparasjon og big-endian UInt64-lengdeprefiks. Separat filkontroll bekreftet at original og generert fixture bare skiller seg i `packageDigest`.

### Full CellProtocol XCTest-bundle etter WP1

Kjørt direkte fra `CellProtocol`, exit 1 (samme kjente røde som WP0c):

```sh
xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest
```

| Kjøring | Executed | Hoppet over | Feilrapporter | Røde testtilfeller |
|---|---:|---:|---:|---:|
| WP0c, historisk baseline | 1060 | 8 | 6 | 6 |
| WP1, nybygd bundle | 1074 | 8 | 6 | 6 |
| Endring | +14 | 0 | 0 | 0 |

**Ingen nye røde testtilfeller.** Eksakt sammenligning av røde testnavn mot `#baseline` gir samme sett: tre `AppleIdentityVaultKeyStorageTests` (keychain/CDSA i sandkassen), én `EntityScannerAgreementSurfaceTests` (`radar`, `select`) og to `OID4VPSignedRequestTrustVerifierTests` (`invalidX509CertificateChain`). Ingen eksisterende tester er endret, fjernet eller svekket.

Ekte feilutdata og røde testnavn fra fullkjøringen:

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/IdentityVault.swift:1369: error: -[CellBaseTests.AppleIdentityVaultKeyStorageTests testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns] : failed: caught error: "Creating private key failed with error: Optional(Swift.Unmanaged<__C.CFErrorRef>(_value: Error Domain=NSOSStatusErrorDomain Code=-50 "failed to generate CDSA key" (paramErr: error in user parameter list) UserInfo={numberOfErrorsDeep=0, NSDescription=failed to generate CDSA key}))"
Test Case '-[CellBaseTests.AppleIdentityVaultKeyStorageTests testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns]' failed (0.472 seconds).
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/IdentityVault.swift:1369: error: -[CellBaseTests.AppleIdentityVaultKeyStorageTests testLegacyEmbeddedPrivateKeyStillSigns] : failed: caught error: "Creating private key failed with error: Optional(Swift.Unmanaged<__C.CFErrorRef>(_value: Error Domain=NSOSStatusErrorDomain Code=-50 "failed to generate CDSA key" (paramErr: error in user parameter list) UserInfo={numberOfErrorsDeep=0, NSDescription=failed to generate CDSA key}))"
Test Case '-[CellBaseTests.AppleIdentityVaultKeyStorageTests testLegacyEmbeddedPrivateKeyStillSigns]' failed (0.001 seconds).
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/IdentityVault.swift:610: error: -[CellBaseTests.AppleIdentityVaultKeyStorageTests testScopedSecretDataStaysStableInUnsignedTestHost] : failed: caught error: "unhandledError(status: -50)"
Test Case '-[CellBaseTests.AppleIdentityVaultKeyStorageTests testScopedSecretDataStaysStableInUnsignedTestHost]' failed (0.046 seconds).
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Tests/CellBaseTests/EntityScannerAgreementSurfaceTests.swift:75: error: -[CellBaseTests.EntityScannerAgreementSurfaceTests testAgreementTemplateExposesOnlyTheApprovedSurface] : XCTAssertTrue failed - EntityScannerCell.agreementTemplate eksponerer nøkler som ikke er gjennomgått: ["radar", "select"]. Legg dem til fasiten i denne testen bare hvis du har vurdert hva en innsluppet motpart kan lese gjennom dem — se F1 i Codex_FixList_NearbyScanner_2026-08-24.md.
Test Case '-[CellBaseTests.EntityScannerAgreementSurfaceTests testAgreementTemplateExposesOnlyTheApprovedSurface]' failed (0.001 seconds).
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/VerifiableCredentials/Standards/OpenID4VP/OID4VPSignedRequestTrustVerifier.swift:353: error: -[CellBaseTests.OID4VPSignedRequestTrustVerifierTests testVerifiesX509HashSignedRequest] : failed: caught error: "invalidX509CertificateChain"
Test Case '-[CellBaseTests.OID4VPSignedRequestTrustVerifierTests testVerifiesX509HashSignedRequest]' failed (0.007 seconds).
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/VerifiableCredentials/Standards/OpenID4VP/OID4VPSignedRequestTrustVerifier.swift:348: error: -[CellBaseTests.OID4VPSignedRequestTrustVerifierTests testVerifiesX509SanDNSSignedRequest] : failed: caught error: "invalidX509CertificateChain"
Test Case '-[CellBaseTests.OID4VPSignedRequestTrustVerifierTests testVerifiesX509SanDNSSignedRequest]' failed (0.001 seconds).
```

<details>
<summary>Alle ekte suiteavslutninger og Executed-linjer fra WP1-fullkjøringen</summary>

```text
Test Suite 'AdmissionAndCatalogContractModelsTests' passed at 2026-09-08 21:26:18.893.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'AgentTrustPackageTests' passed at 2026-09-08 21:26:18.926.
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.033 (0.033) seconds
Test Suite 'AgreementCodingTests' passed at 2026-09-08 21:26:18.932.
	 Executed 22 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'AppleBridgeTransportTests' passed at 2026-09-08 21:26:18.936.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'AppleIdentityVaultKeyStorageTests' failed at 2026-09-08 21:26:19.801.
	 Executed 12 tests, with 7 tests skipped and 3 failures (3 unexpected) in 0.865 (0.866) seconds
Test Suite 'AppleIntelligenceCellContractTests' passed at 2026-09-08 21:26:19.941.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.139 (0.140) seconds
Test Suite 'AppleRuntimeStorageTests' passed at 2026-09-08 21:26:19.953.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'AudioAnalysisRecordTests' passed at 2026-09-08 21:26:19.953.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'AudioSignalAnalysisTests' passed at 2026-09-08 21:26:19.954.
	 Executed 1 test, with 1 test skipped and 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'BridgeInboundPayloadValidatorTests' passed at 2026-09-08 21:26:19.954.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'BridgeMultiplexingTests' passed at 2026-09-08 21:26:20.375.
	 Executed 18 tests, with 0 failures (0 unexpected) in 0.419 (0.421) seconds
Test Suite 'BridgeTests' passed at 2026-09-08 21:28:09.456.
	 Executed 48 tests, with 0 failures (0 unexpected) in 109.063 (109.081) seconds
Test Suite 'CalendarContractTests' passed at 2026-09-08 21:28:09.483.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.027 (0.027) seconds
Test Suite 'CellAccessGraphContractsTests' passed at 2026-09-08 21:28:09.487.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'CellBaseTests' passed at 2026-09-08 21:28:09.489.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'CellJSONCoderTests' passed at 2026-09-08 21:28:09.490.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'CellLifecycleTests' passed at 2026-09-08 21:28:13.920.
	 Executed 9 tests, with 0 failures (0 unexpected) in 4.427 (4.430) seconds
Test Suite 'CellResolverProtocolLightweightBridgeTransportTests' passed at 2026-09-08 21:28:13.921.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'CellRuntimeEnvironmentTests' passed at 2026-09-08 21:28:13.925.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.003 (0.004) seconds
Test Suite 'CellRuntimeReadinessContractTests' passed at 2026-09-08 21:28:14.051.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.125 (0.126) seconds
Test Suite 'CellSecurityKitTests' passed at 2026-09-08 21:28:14.054.
	 Executed 20 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'ChatCellTests' passed at 2026-09-08 21:28:14.482.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.426 (0.428) seconds
Test Suite 'ClaimCompositionTests' passed at 2026-09-08 21:28:14.485.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'ClaimDefinitionTests' passed at 2026-09-08 21:28:14.486.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'ClaimSchemeTests' passed at 2026-09-08 21:28:14.489.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'CommonsCellsTests' passed at 2026-09-08 21:28:14.516.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.027 (0.028) seconds
Test Suite 'ConferenceOrganizerAccessModelsTests' passed at 2026-09-08 21:28:14.526.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.009 (0.010) seconds
Test Suite 'ConferenceSwarmSignalMatchingTests' passed at 2026-09-08 21:28:14.535.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'ContractProbeCellTests' passed at 2026-09-08 21:28:17.289.
	 Executed 11 tests, with 0 failures (0 unexpected) in 2.752 (2.754) seconds
Test Suite 'CorrespondenceCellTests' passed at 2026-09-08 21:28:17.340.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.050 (0.051) seconds
Test Suite 'CrossRuntimeWireFixtureTests' passed at 2026-09-08 21:28:17.341.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'DIDDocumentValidatorTests' passed at 2026-09-08 21:28:17.343.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'DIDInteroperabilityTests' passed at 2026-09-08 21:28:17.344.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'DeviceIngressContractTests' passed at 2026-09-08 21:28:17.433.
	 Executed 20 tests, with 0 failures (0 unexpected) in 0.088 (0.089) seconds
Test Suite 'DeviceIngressWireFixtureTests' passed at 2026-09-08 21:28:17.438.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'DiagnosticLoggingTests' passed at 2026-09-08 21:28:17.438.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'EntityAtlasInspectorCellTests' passed at 2026-09-08 21:28:17.448.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'EntityAtlasProjectionTests' passed at 2026-09-08 21:28:17.468.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.020 (0.020) seconds
Test Suite 'EntityAuthorityCommitTests' passed at 2026-09-08 21:28:17.512.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.044 (0.044) seconds
Test Suite 'EntityAuthorityReplicaStoreTests' passed at 2026-09-08 21:28:17.552.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.040 (0.041) seconds
Test Suite 'EntityRelationRecordV1Tests' passed at 2026-09-08 21:28:17.557.
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.004 (0.005) seconds
Test Suite 'EntityRepresentationAgreementTests' passed at 2026-09-08 21:28:17.557.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'EntityScannerAgreementSurfaceTests' failed at 2026-09-08 21:28:17.559.
	 Executed 3 tests, with 1 failure (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'EntityScannerCellContractTests' passed at 2026-09-08 21:28:17.573.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.013 (0.014) seconds
Test Suite 'EntityValidatedContactRecordV1Tests' passed at 2026-09-08 21:28:17.575.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ExploreContractValidatorTests' passed at 2026-09-08 21:28:17.576.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'FileCryptoCellTests' passed at 2026-09-08 21:28:17.581.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'FlowCacheCellTests' passed at 2026-09-08 21:28:17.591.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'FlowEnvelopeCryptoTests' passed at 2026-09-08 21:28:17.593.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'FlowEnvelopeSerializationTests' passed at 2026-09-08 21:28:17.593.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'FlowInspectionCellsTests' passed at 2026-09-08 21:28:17.851.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.257 (0.258) seconds
Test Suite 'GeneralCellInterfaceTests' passed at 2026-09-08 21:28:17.920.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.067 (0.069) seconds
Test Suite 'GoalDefinitionTests' passed at 2026-09-08 21:28:17.922.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'GoalEvaluationCellTests' passed at 2026-09-08 21:28:17.925.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'GoalEvaluationEngineTests' passed at 2026-09-08 21:28:17.925.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'GraphIndexCellTests' passed at 2026-09-08 21:28:17.934.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'IdentitiesCellContractTests' passed at 2026-09-08 21:28:17.935.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'IdentityAgreementTests' passed at 2026-09-08 21:28:17.937.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'IdentityDomainBindingTests' passed at 2026-09-08 21:28:17.938.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'IdentityLinkingModelsTests' passed at 2026-09-08 21:28:17.950.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
Test Suite 'IdentityPublicKeySignatureVerifierTests' passed at 2026-09-08 21:28:17.953.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'IntegrationTests' passed at 2026-09-08 21:28:20.388.
	 Executed 35 tests, with 0 failures (0 unexpected) in 2.428 (2.435) seconds
Test Suite 'JOSEAESKeyWrapTests' passed at 2026-09-08 21:28:20.403.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
Test Suite 'JOSEJWSVerifierSecurityTests' passed at 2026-09-08 21:28:20.406.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'KeyPathResolverTests' passed at 2026-09-08 21:28:20.411.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'LightweightBridgeTransportTests' passed at 2026-09-08 21:28:21.006.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.593 (0.595) seconds
Test Suite 'LobbyCellContractTests' passed at 2026-09-08 21:28:21.035.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.029 (0.029) seconds
Test Suite 'MatchStrategyPlannerTests' passed at 2026-09-08 21:28:21.036.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'NearbyBeaconTests' passed at 2026-09-08 21:28:21.038.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'NearbyDisclosurePolicyTests' passed at 2026-09-08 21:28:21.039.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'NearbyPeerStateMachineTests' passed at 2026-09-08 21:28:21.040.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'NearbyProbeTests' passed at 2026-09-08 21:28:21.042.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'OID4VCICredentialOfferTests' passed at 2026-09-08 21:28:21.044.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'OID4VCIIssuerMetadataTests' passed at 2026-09-08 21:28:21.046.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'OID4VCIMetadataClientTests' passed at 2026-09-08 21:28:21.048.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'OID4VPDCQLTests' passed at 2026-09-08 21:28:21.050.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'OID4VPDirectPostJWTEncryptionTests' passed at 2026-09-08 21:28:21.062.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
Test Suite 'OID4VPDirectPostJWTSubmissionAdapterTests' passed at 2026-09-08 21:28:21.065.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'OID4VPDirectPostTests' passed at 2026-09-08 21:28:21.067.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'OID4VPRequestMatcherTests' passed at 2026-09-08 21:28:21.067.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'OID4VPRequestObjectTests' passed at 2026-09-08 21:28:21.068.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'OID4VPResponseTests' passed at 2026-09-08 21:28:21.069.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'OID4VPSignedRequestObjectTests' passed at 2026-09-08 21:28:21.071.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'OID4VPSignedRequestTrustVerifierTests' failed at 2026-09-08 21:28:21.083.
	 Executed 7 tests, with 2 failures (2 unexpected) in 0.012 (0.013) seconds
Test Suite 'OID4VPStaticVerifierMetadataProviderTests' passed at 2026-09-08 21:28:21.084.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'OID4VPVerifierMetadataResolverTests' passed at 2026-09-08 21:28:21.084.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'OID4VPVerifierMetadataTests' passed at 2026-09-08 21:28:21.085.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'PersistedCellFileIOTests' passed at 2026-09-08 21:28:21.089.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'PersistenceTests' passed at 2026-09-08 21:28:21.101.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
Test Suite 'PerspectiveCellContractTests' passed at 2026-09-08 21:28:21.101.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'PerspectiveCellMatchPayloadTests' passed at 2026-09-08 21:28:21.111.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.009 (0.010) seconds
Test Suite 'PerspectiveEntityProjectionTests' passed at 2026-09-08 21:28:21.113.
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'PerspectiveSchemaTests' passed at 2026-09-08 21:28:21.115.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'PortholeViewModelAvailabilityTests' passed at 2026-09-08 21:28:21.143.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.028 (0.028) seconds
Test Suite 'PurposeAndInterestMatchingTests' passed at 2026-09-08 21:28:21.145.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'PurposeBoundExternalActionTests' passed at 2026-09-08 21:28:21.147.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'PurposeCompositionTests' passed at 2026-09-08 21:28:21.147.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'PurposeGoalLintTests' passed at 2026-09-08 21:28:21.148.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'PurposeInterestAdjacencyIndexTests' passed at 2026-09-08 21:28:21.148.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'PurposeInterestBenchmarkArtifactTests' passed at 2026-09-08 21:28:21.156.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.008 (0.008) seconds
Test Suite 'PurposeInterestBenchmarkReportTests' passed at 2026-09-08 21:28:21.180.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.024 (0.024) seconds
Test Suite 'PurposeInterestChallengeExperimentTests' passed at 2026-09-08 21:28:21.185.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'PurposeInterestRuntimeComparisonTests' passed at 2026-09-08 21:28:21.214.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.029 (0.029) seconds
Test Suite 'PurposeInterestScenarioExperimentTests' passed at 2026-09-08 21:28:21.217.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'PurposeInterestScenarioRankingTests' passed at 2026-09-08 21:28:21.222.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'RadarEntityLedgerTests' passed at 2026-09-08 21:28:21.223.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'RealCellContractTests' passed at 2026-09-08 21:28:21.252.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.029 (0.030) seconds
Test Suite 'RelationalLearningCellContractTests' passed at 2026-09-08 21:28:21.646.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.393 (0.394) seconds
Test Suite 'RelationalLearningEngineTests' passed at 2026-09-08 21:28:21.653.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.006 (0.007) seconds
Test Suite 'ResolverTests' passed at 2026-09-08 21:28:21.690.
	 Executed 33 tests, with 0 failures (0 unexpected) in 0.036 (0.037) seconds
Test Suite 'RestaurantPurposeRecommendationTests' passed at 2026-09-08 21:28:21.692.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'RuntimeLifecyclePropertyTests' passed at 2026-09-08 21:28:21.706.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.013 (0.014) seconds
Test Suite 'SDGPilotPurposeCatalogTests' passed at 2026-09-08 21:28:21.707.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'ScannerServiceInvitationTests' passed at 2026-09-08 21:28:22.794.
	 Executed 5 tests, with 0 failures (0 unexpected) in 1.085 (1.087) seconds
Test Suite 'SerializationTests' passed at 2026-09-08 21:28:22.805.
	 Executed 18 tests, with 0 failures (0 unexpected) in 0.009 (0.012) seconds
Test Suite 'SkeletonActionButtonExecutionTests' passed at 2026-09-08 21:28:22.810.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.004 (0.005) seconds
Test Suite 'SkeletonButtonResolutionTests' passed at 2026-09-08 21:28:22.811.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'SkeletonLocalizationTests' passed at 2026-09-08 21:28:24.503.
	 Executed 9 tests, with 0 failures (0 unexpected) in 1.691 (1.692) seconds
Test Suite 'SkeletonReachabilityAuditTests' passed at 2026-09-08 21:28:24.505.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'SkeletonStyleParityTests' passed at 2026-09-08 21:28:24.506.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'SkeletonTests' passed at 2026-09-08 21:28:24.520.
	 Executed 51 tests, with 0 failures (0 unexpected) in 0.013 (0.015) seconds
Test Suite 'TaxonomyResolverTests' passed at 2026-09-08 21:28:24.533.
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.012 (0.013) seconds
Test Suite 'TrustPacketCellTests' passed at 2026-09-08 21:28:24.554.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.021 (0.021) seconds
Test Suite 'TrustedIssuerCellContractTests' passed at 2026-09-08 21:28:24.556.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'TrustedIssuerCellTests' passed at 2026-09-08 21:28:25.490.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.933 (0.934) seconds
Test Suite 'TrustedIssuerEvaluationReceiptTests' passed at 2026-09-08 21:28:25.492.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.003) seconds
Test Suite 'TrustedIssuerSignedEvaluationTests' passed at 2026-09-08 21:28:25.497.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'UserDataResilienceTests' passed at 2026-09-08 21:28:26.195.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.698 (0.699) seconds
Test Suite 'VCIssuerServiceSecurityTests' passed at 2026-09-08 21:28:26.197.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'VaporBridgeTransportTests' passed at 2026-09-08 21:28:26.226.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.029 (0.029) seconds
Test Suite 'VaporCellRuntimeReadinessContractTests' passed at 2026-09-08 21:28:26.273.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.046 (0.046) seconds
Test Suite 'VaporIdentityVaultStrictTests' passed at 2026-09-08 21:28:26.512.
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.239 (0.239) seconds
Test Suite 'VaultCellTests' passed at 2026-09-08 21:28:26.525.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
Test Suite 'VaultContractsTests' passed at 2026-09-08 21:28:26.525.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'CellProtocolPackageTests.xctest' failed at 2026-09-08 21:28:26.525.
	 Executed 1074 tests, with 8 tests skipped and 6 failures (5 unexpected) in 127.567 (127.641) seconds
Test Suite 'All tests' failed at 2026-09-08 21:28:26.525.
	 Executed 1074 tests, with 8 tests skipped and 6 failures (5 unexpected) in 127.567 (127.642) seconds
```

</details>

Direkte `xctest` dekker XCTest-bundlen; eventuelle Swift Testing-mål er ikke kjørt med denne banen. WP1-testene er XCTest og er kjørt både isolert og i full bundle. Midlertidige logger ligger i `/private/tmp/wp1-agent-trust-nmlg758s/`; relevant evidens er bevart over. Ingen git-kommandoer er kjørt.

## WP1 — sluttmelding

WP1 — pakke-modell + digest er **ferdig** for `purpose://candidate.tillitspakke-agentflaate.projeksjon`.

`AgentTrustPackage.swift` leverer Codable/Equatable/Sendable-modellen, valgfrie celledetaljer, kanonisk koding, domeneseparert SHA-256 og dokumentert rekursiv hemmelighetsvakt. `AgentTrustPackageTests.swift` har 14 nye tester; alle passerer. `fleet-webfetch.package.generated.json` er skrevet av testen med ekte digest og er ellers semantisk identisk med original-fixturen.

Bygg: grønt. Full nybygd XCTest-bundle: **1074 tester, 8 hoppet over, samme 6 røde som WP0c, ingen nye røde**. Ekte kommandoer, feil og `Executed`-linjer står i [Projeksjon](#projeksjon).

Avvik: fixture bruker en teksthenvisning i `reach` i stedet for kontraktens liste. Begge former støttes eksplisitt; henvisningen løses ikke og binder ikke den separate filens innhold. Det første baseline-forsøket ble blokkert fordi Python-måle-wrapperen kjørte som x86_64; videre direkte skallkjøringer fungerte. Korrigerte kompileringsforsøk er dokumentert over. Swift Testing er ikke dekket av direkte XCTest-banen.

`STATUS.md` har fått én WP1-linje under Logg. Arbeidet er avgrenset til WP1; ingen celle er laget, CellScaffold er urørt, og ingen git-kommandoer er kjørt. Formål og pakke gir ingen rettigheter.

## Kontrakt og autorisasjon <a id="contract"></a>

<a id="auth"></a>

### WP2 — baseline før endring

Formål: `purpose://candidate.tillitspakke-agentflaate.projeksjon`, `purpose://cell.contract-explicit`, `purpose://cell.authorization-honours-keypath`.

Eksisterende mønstercelle, direkte fra `CellScaffold` uten arch-prefiks:

```sh
xcrun --sdk macosx xctest -XCTest AppTests.PersonalDataTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

```text
Test Suite 'PersonalDataTrustPackageCellTests' passed at 2026-09-08 21:50:22.856.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.026 (0.026) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-08 21:50:22.856.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.026 (0.026) seconds
Test Suite 'Selected tests' passed at 2026-09-08 21:50:22.856.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.026 (0.027) seconds
```

Full sammenligningsbaseline er WP0c ovenfor: 2046 tester, 11 hoppet over, 46 røde testtilfeller / 148 feilrapporter / 9 uventede.

### WP2 — implementasjon og kildegrenser

- `AgentTrustPackageCell.swift` bruker WP1s `CellBase.AgentTrustPackage` og `AgentTrustPackageCanonicalEncoder`, uten ny pakkemodell. `fleet.set` og `regenerate` leser resolver-oppløste, eierkontrollerte lokale celler. Én eksplisitt generering om gangen; ingen nettverksinvokasjon, justering, Contract-utstedelse eller godkjenning.
- De fire GET- og ti SET-keypathene og Grants matcher kontraktfilen. `configuration` er i tillegg den ordinære scaffold-flateinngangen. De strenge `registerGet`/`registerSet`-variantene kaller `registerExploreContract` før hver handler installeres. Underfelt i `trustPackage.state` leses fra den eksakte, autoriserte state-operasjonen; det finnes ingen bred `trustPackage`-Grant. Ukjente metoder/keypaths feiler lukket.
- Alle personlige lesinger og handlinger krever både runtime-autorisasjon for eksakt keypath og `requesterProvesOwnership`. `packageSchema` bruker ordinær keypath-autorisasjon for admitted requester. Ingen operasjon har `purposeRef` som autoritetsgrunnlag; payload med `purposeRef`/`purposeRefs` avvises eksplisitt. Negativtesten bruker `purpose://prompt.unknown`.
- `agreementTemplate.grants` projiseres som keypath + RWXS. Contracts hentes fra identitetens EntityAnchor `signedAgreementEntity`, med samme kryptografiske `AgreementProductionVerification.verifyEntityRecord`-bane som Entity Studio. Bare verifisert owner-/subject-bundet Contract og signert read-after-write-kvittering blir med. Utilgjengelig EntityAnchor gir tom Contract-liste og radens `verified=false`; en påstått `verified`-status uten kryptografisk evidens avvises. Eksisterende verifier støtter owner-snapshots, ikke vilkårlige bilaterale/andre subject-baner. Contracts er evidens for identiteten; WP2 utleder ingen kant eller rekkevidde fra dem.
- Policy og destinasjons-/dataklasse-ceilings for en konkret `PurposeBoundAIGatewayCell` tas fra `AIGatewayPurposePolicy.executionPolicy(createdAt:)`. **Kildeavvik:** denne cellen eksponerer bare `ai.invokePurposeBound`, ikke en lesbar gjeldende modellrute eller systeminstruksjon. Rute og instruksjon følger invokasjonspayloaden. WP2 finner derfor ingen gjeldende rute/instruksjon der: `modelRoute=nil`, `instruction=nil`, `hasModel=false`, `hasInstruction=false`, med tydelig norsk label. Ingen modell fra mockupen eller nedarvet, ueksponert default-utkast presenteres som gjeldende. Vanlig `AIGatewayCell` har et lesbart `state.draft`: denne kilden støttes som **utkast**, normalisert til `AIGatewayProviderRoute`, med URL-digest og instruksjons-keypath + digest. Nøkler, aliaser og prompt-tekst kopieres ikke til pakke eller state. En fersk modellrute for PurposeBound krever en egen, faktisk kildebinding; WP2 introduserer ikke en slik ny invokasjons-/konfigurasjonsmekanisme.
- WebFetch leses på `webFetch.ceiling` dersom den keypathen annonseres; ugyldig/avvist kilde gir ingen avledet pakke. Dagens WebFetch har ikke keypathen: `hostPatterns=[]`, label **«ingen whitelist ennå (WP5)»**. GET/https-metadata er dagens kode, ikke påstand om en håndhevet whitelist. WebFetch-koden er urørt.
- Norske labels skiller utkast, tom flåte og mislykket projeksjon. `reach`/`edges` er tomme. Godkjenningslabelen sier eksplisitt at godkjenning/startport ikke er implementert (WP7). De åtte reserverte SET-handlerne og audit-GET svarer `not-implemented`; listen står i [ACCEPT.md#stubs](ACCEPT.md#stubs).
- Valgt flåte og genereringsepoke persistéres; epoken holdes stabil ved re-generering slik at uendrede kilder gir samme digest. Pakke/rader gjenbrukes ikke som fersk evidens ved dekoding: kildene må re-leses. Testen bekrefter at samme kilder etter restore gir samme digest. Feilet kildelesing trekker tilbake den viste projeksjonen og gir `package_not_derived` ved pakke-GET.
- Factoryen inneholder godkjent JSON-struktur uendret (samme elementer, bindings og handlinger), og `discovery.purpose` er `purpose://candidate.tillitspakke-agentflaate.root`. Testen sammenligner hele dekodede skeleton-treet. Porthole-/Binding-paritet, knappenes runtime-payload-substitusjon og skjermbilder er ikke testet i WP2 (WP11).
- Registrert `.identityUnique`, `.persistant` ved begge PersonalDataTrustPackage-registreringene i `configure.swift`. Ingen git-kommandoer.

### WP2 — bygg og korrigerte forsøk

Alle bygg er kjørt i `CellScaffold` med `swift build --disable-sandbox --build-tests`, uten arch-prefiks. Følgende kompileringsdiagnoser i ny kode/testoppsett ble rettet før grønn kjøring:

```text
build.log
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift:114:53: error: 'async' call in an autoclosure that does not support concurrency
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift:119:45: error: 'KeyValueErrors' is inaccessible due to 'internal' protection level
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift:124:74: error: 'KeyValueErrors' is inaccessible due to 'internal' protection level
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift:127:94: error: 'KeyValueErrors' is inaccessible due to 'internal' protection level
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift:132:63: error: 'KeyValueErrors' is inaccessible due to 'internal' protection level
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift:150:83: error: 'KeyValueErrors' is inaccessible due to 'internal' protection level
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift:197:91: error: 'KeyValueErrors' is inaccessible due to 'internal' protection level
build-2.log
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift:176:49: error: call can throw but is not marked with 'try'
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift:193:30: error: call can throw but is not marked with 'try'
build-3.log
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageCellTests.swift:119:72: error: argument type 'String' does not conform to expected type 'Decoder'
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageCellTests.swift:119:72: error: missing argument label 'from:' in call
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageCellTests.swift:23:37: error: 'makeIsolatedForTesting' is inaccessible due to '@_spi' protection level
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageCellTests.swift:25:86: error: cannot infer contextual base in reference to member 'identityUnique'
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageCellTests.swift:26:73: error: cannot infer contextual base in reference to member 'identityUnique'
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageCellTests.swift:27:81: error: cannot infer contextual base in reference to member 'identityUnique'
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageCellTests.swift:28:73: error: cannot infer contextual base in reference to member 'identityUnique'
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageCellTests.swift:93:56: error: cannot convert value of type 'FlowElementValueType' to expected argument type 'ValueType'
build-5.log
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift:57:74: error: missing argument label 'options:' in call
error: input file '/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift' was modified during the build
```

Ekte grønne bygglinjer (build-4 før testoppsettretting; build-6 er produksjonskodebygget før fixture-store-innstrammingen):

```text
build-4.log
Build complete! (10.50s)
build-6.log
Build complete! (17.17s)
```

### WP2 — isolert testklasse

```sh
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Første kjøring feilet i test-fixture før celleadferden kunne testes: resolveren manglet fixture-vault. Rettet ved å koble `CellBase.defaultIdentityVault` til testidentitetens vault. Autorisasjon er på (`debugValidateAccessForEverything=false`), ingen produksjonsbypass. Ekte eksempel og totalsummer:

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/CellResolver/CellResolve.swift:84: error: -[AppTests.AgentTrustPackageCellTests testCanonicalPackageAndTwoRegenerationsHaveSameDigestAndEmitEvidence] : failed: caught error: "noVaultIdentity"
	 Executed 13 tests, with 13 failures (13 unexpected) in 1.115 (1.116) seconds
	 Executed 13 tests, with 13 failures (13 unexpected) in 1.115 (1.116) seconds
	 Executed 13 tests, with 13 failures (13 unexpected) in 1.115 (1.119) seconds
```

Grønn kjøring før fixture-store-innstrammingen — alle 13 nye tester grønne:

```text
Test Suite 'Selected tests' started at 2026-09-08 22:06:49.304.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-08 22:06:49.305.
Test Suite 'AgentTrustPackageCellTests' started at 2026-09-08 22:06:49.305.
Test Case '-[AppTests.AgentTrustPackageCellTests testCanonicalPackageAndTwoRegenerationsHaveSameDigestAndEmitEvidence]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testCanonicalPackageAndTwoRegenerationsHaveSameDigestAndEmitEvidence]' passed (0.048 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testChangingOneTemplateGrantChangesDigest]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testChangingOneTemplateGrantChangesDigest]' passed (0.013 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testClaimedVerifiedEntityRecordWithoutCryptographicReceiptIsExcluded]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testClaimedVerifiedEntityRecordWithoutCryptographicReceiptIsExcluded]' passed (0.011 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testConfigurationPreservesApprovedSkeletonAndNestedStateBindings]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testConfigurationPreservesApprovedSkeletonAndNestedStateBindings]' passed (0.008 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testDeferredOperationsReturnExplicitNotImplementedWithoutChangingDigest]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testDeferredOperationsReturnExplicitNotImplementedWithoutChangingDigest]' passed (0.013 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testFixtureFleetProjectsActualTemplatesAndHonestMissingSources]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testFixtureFleetProjectsActualTemplatesAndHonestMissingSources]' passed (0.009 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testInvalidEndpointAndMissingResolverDoNotProduceDerivedEvidence]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testInvalidEndpointAndMissingResolverDoNotProduceDerivedEvidence]' passed (0.010 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testPersistedSelectionRequiresFreshSourceReadAndRetainsDigest]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testPersistedSelectionRequiresFreshSourceReadAndRetainsDigest]' passed (0.015 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testReadableDraftRouteAndInstructionAreProjectedWithoutPromptOrCredentials]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testReadableDraftRouteAndInstructionAreProjectedWithoutPromptOrCredentials]' passed (0.013 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testStrictExploreContractsMatchNormativeKeysAndGrants]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testStrictExploreContractsMatchNormativeKeysAndGrants]' passed (0.006 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownKeypathsAndWrongMethodsFailClosed]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownKeypathsAndWrongMethodsFailClosed]' passed (0.002 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownPurposeCannotAuthorizeOrAlterFleet]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownPurposeCannotAuthorizeOrAlterFleet]' passed (0.014 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testWrongRequesterCannotReadWriteOrUseDeferredActions]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testWrongRequesterCannotReadWriteOrUseDeferredActions]' passed (0.011 seconds).
Test Suite 'AgentTrustPackageCellTests' passed at 2026-09-08 22:06:49.476.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.170 (0.171) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-08 22:06:49.476.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.170 (0.171) seconds
Test Suite 'Selected tests' passed at 2026-09-08 22:06:49.476.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.170 (0.172) seconds
```

### WP2 — statisk Explore-audit

```sh
python3 CellProtocolDocuments/Tools/Explore/explore_contract_audit.py --repo-root CellProtocol
python3 CellProtocolDocuments/Tools/Explore/explore_contract_audit.py --repo-root CellScaffold --source-dir Sources/App/Cells/AgentTrustPackage --json-output /private/tmp/wp2-agent-trust/explore-cell.json
```

Ekte utdata, henholdsvis eksisterende protokollkilder og ny celle:

```text
{
  "completeContracts": 305,
  "errors": 7,
  "handlerOperations": 316,
  "warnings": 19
}
{
  "completeContracts": 2,
  "errors": 0,
  "handlerOperations": 2,
  "warnings": 0
}
```

Protokollskannens 7 feil/19 advarsler gjelder urørte kilder. Cellens statiske skann har 0 funn; den teller to registreringsuttrykk i løkker, ikke alle ekspanderte operasjoner. `testStrictExploreContractsMatchNormativeKeysAndGrants` verifiserer alle 14 normative operasjoner og Grants ved runtime, i strict Explore-modus.

### WP2 — fixture-store og ny helkjøring

Etter grønn isolert kjøring avdekket kildegjennomgangen at vanlig AIGateways `state` også kaller credential-storen for å vise tilgjengelighet (`AIGatewayCell.setupObject`). WP2-testklassen er derfor bundet til en eksplisitt tom, requester-scopet fixture-store i `setUp`, med opprinnelig factory gjenopprettet i `tearDown` (handoff regel 5). Produksjonskoden er uendret. Ingen nøkkel eller instruksjonstekst er skrevet til testartefakter.

Første fullkjøring (`full.log`) ble avbrutt med SIGINT / exit 130 for å bygge og kjøre på nytt med det endelige testoppsettet. Den er **ikke** akseptansebevis for hele bundlen. Ved siste opptelling før avbrudd: 1551 fullførte testtilfeller, 35 røde, ingen nye navn mot baseline. Endelig fullkjøring rapporteres nedenfor.

Endelig bygg og isolert testklasse etter fixture-store-innstrammingen (samme regel 10-kommandoer):

```text
Build complete! (13.79s)
Test Suite 'Selected tests' started at 2026-09-08 22:12:42.771.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-08 22:12:42.773.
Test Suite 'AgentTrustPackageCellTests' started at 2026-09-08 22:12:42.773.
Test Case '-[AppTests.AgentTrustPackageCellTests testCanonicalPackageAndTwoRegenerationsHaveSameDigestAndEmitEvidence]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testCanonicalPackageAndTwoRegenerationsHaveSameDigestAndEmitEvidence]' passed (0.039 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testChangingOneTemplateGrantChangesDigest]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testChangingOneTemplateGrantChangesDigest]' passed (0.013 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testClaimedVerifiedEntityRecordWithoutCryptographicReceiptIsExcluded]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testClaimedVerifiedEntityRecordWithoutCryptographicReceiptIsExcluded]' passed (0.010 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testConfigurationPreservesApprovedSkeletonAndNestedStateBindings]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testConfigurationPreservesApprovedSkeletonAndNestedStateBindings]' passed (0.007 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testDeferredOperationsReturnExplicitNotImplementedWithoutChangingDigest]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testDeferredOperationsReturnExplicitNotImplementedWithoutChangingDigest]' passed (0.014 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testFixtureFleetProjectsActualTemplatesAndHonestMissingSources]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testFixtureFleetProjectsActualTemplatesAndHonestMissingSources]' passed (0.010 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testInvalidEndpointAndMissingResolverDoNotProduceDerivedEvidence]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testInvalidEndpointAndMissingResolverDoNotProduceDerivedEvidence]' passed (0.010 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testPersistedSelectionRequiresFreshSourceReadAndRetainsDigest]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testPersistedSelectionRequiresFreshSourceReadAndRetainsDigest]' passed (0.014 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testReadableDraftRouteAndInstructionAreProjectedWithoutPromptOrCredentials]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testReadableDraftRouteAndInstructionAreProjectedWithoutPromptOrCredentials]' passed (0.013 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testStrictExploreContractsMatchNormativeKeysAndGrants]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testStrictExploreContractsMatchNormativeKeysAndGrants]' passed (0.005 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownKeypathsAndWrongMethodsFailClosed]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownKeypathsAndWrongMethodsFailClosed]' passed (0.002 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownPurposeCannotAuthorizeOrAlterFleet]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownPurposeCannotAuthorizeOrAlterFleet]' passed (0.015 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testWrongRequesterCannotReadWriteOrUseDeferredActions]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testWrongRequesterCannotReadWriteOrUseDeferredActions]' passed (0.011 seconds).
Test Suite 'AgentTrustPackageCellTests' passed at 2026-09-08 22:12:42.937.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.164 (0.164) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-08 22:12:42.937.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.164 (0.164) seconds
Test Suite 'Selected tests' passed at 2026-09-08 22:12:42.937.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.164 (0.166) seconds
```

### WP2 — endelig full CellScaffold XCTest-bundle

```sh
xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Sammenligning av faktiske røde testnavn mot WP0c-listen (ikke bare antall):

```json
{
  "baselineFailedTestCases": 46,
  "currentFailedTestCases": 46,
  "newFailedTestCases": [],
  "baselineFailuresAbsentNow": [],
  "total": "Executed 2059 tests, with 11 tests skipped and 151 failures (9 unexpected) in 857.721 (857.868) seconds"
}
```

Nye feilrapporter:

```text
Ingen nye røde testnavn. Tre ekstra assert-rapporter i den allerede røde Mermaid-testen er dokumentert under.
```

<details>
<summary>Ekte suite- og Executed-linjer fra hele den endelige bundlen</summary>

```text
Test Suite 'AIAssistantThreadCellTests' failed at 2026-09-08 22:12:56.094.
	 Executed 14 tests, with 4 tests skipped and 12 failures (0 unexpected) in 2.136 (2.137) seconds
Test Suite 'AIGatewayCellTests' passed at 2026-09-08 22:12:56.251.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.155 (0.158) seconds
Test Suite 'AIGatewayConfigurationFactoryTests' passed at 2026-09-08 22:12:56.253.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'AccessRequirementPromptCellTests' passed at 2026-09-08 22:12:56.776.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.522 (0.522) seconds
Test Suite 'AccessSensitiveRuntimeReadinessTests' passed at 2026-09-08 22:12:56.811.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.031 (0.035) seconds
Test Suite 'AdminAccessRequestCellTests' passed at 2026-09-08 22:12:56.830.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.020 (0.020) seconds
Test Suite 'AdminAuthenticatedVaporBridgeTransportTests' passed at 2026-09-08 22:12:56.957.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.126 (0.126) seconds
Test Suite 'AdminBridgeHandshakeAuthenticationTests' passed at 2026-09-08 22:12:56.964.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.007 (0.008) seconds
Test Suite 'AdminCatalogRoutesTests' passed at 2026-09-08 22:12:57.967.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.002 (1.003) seconds
Test Suite 'AdminControlPlaneRoutingTests' passed at 2026-09-08 22:12:57.976.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.008 (0.009) seconds
Test Suite 'AdminCopilotWorkspaceConfigurationTests' passed at 2026-09-08 22:12:59.247.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.271 (1.271) seconds
Test Suite 'AdminCredentialPolicyTests' passed at 2026-09-08 22:12:59.248.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'AdminCredentialRevocationTests' passed at 2026-09-08 22:12:59.250.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'AdminDeploymentSupervisorCellTests' passed at 2026-09-08 22:12:59.293.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.043 (0.043) seconds
Test Suite 'AdminEntityProofPersistenceSupportTests' passed at 2026-09-08 22:12:59.810.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.517 (0.517) seconds
Test Suite 'AdminFundingCellTests' passed at 2026-09-08 22:13:00.351.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.541 (0.541) seconds
Test Suite 'AdminNodeFleetCellTests' passed at 2026-09-08 22:13:00.547.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.196 (0.196) seconds
Test Suite 'AdminOperationsMetricsTests' passed at 2026-09-08 22:13:00.869.
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.320 (0.322) seconds
Test Suite 'AdminPersistedRuntimeReadinessTests' passed at 2026-09-08 22:13:01.179.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.310 (0.310) seconds
Test Suite 'AdminRoleEnrollmentCellTests' passed at 2026-09-08 22:13:01.186.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
Test Suite 'AdminScaffoldBootstrapTests' passed at 2026-09-08 22:13:01.199.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
Test Suite 'AdminScaffoldBridgeMultiplexRouteTests' passed at 2026-09-08 22:13:01.204.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'AdminScaffoldRuntimeTests' passed at 2026-09-08 22:13:01.334.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.130 (0.131) seconds
Test Suite 'AdminScaffoldSnapshotIngestTests' passed at 2026-09-08 22:13:01.346.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'AdminSecurityPolicyCellTests' passed at 2026-09-08 22:13:01.350.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'AdminWorkspaceConfigurationFactoryTests' passed at 2026-09-08 22:13:01.364.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
Test Suite 'AgeProofDoorCellTests' passed at 2026-09-08 22:13:01.368.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'AgentActionCapabilityCatalogV1Tests' passed at 2026-09-08 22:13:01.587.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.220 (0.220) seconds
Test Suite 'AgentConversationInboxCellTests' passed at 2026-09-08 22:13:01.613.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.026 (0.026) seconds
Test Suite 'AgentTrustPackageCellTests' passed at 2026-09-08 22:13:01.770.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.155 (0.156) seconds
Test Suite 'AgreementWorkbenchCellTests' passed at 2026-09-08 22:13:01.970.
	 Executed 21 tests, with 0 failures (0 unexpected) in 0.199 (0.201) seconds
Test Suite 'AgreementWorkbenchConfigurationFactoryTests' passed at 2026-09-08 22:13:01.984.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
Test Suite 'AppTests' passed at 2026-09-08 22:13:02.636.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.651 (0.652) seconds
Test Suite 'ArendalsukaConfigurationPublisherAuthorizationRoutesTests' passed at 2026-09-08 22:13:02.872.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.236 (0.236) seconds
Test Suite 'ArendalsukaConfigurationPublisherCellTests' passed at 2026-09-08 22:13:03.454.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.582 (0.582) seconds
Test Suite 'ArendalsukaEventAtlasCellTests' failed at 2026-09-08 22:13:04.608.
	 Executed 40 tests, with 14 failures (0 unexpected) in 1.152 (1.154) seconds
Test Suite 'ArendalsukaImportAuthorizationRoutesTests' failed at 2026-09-08 22:13:05.053.
	 Executed 1 test, with 3 failures (0 unexpected) in 0.445 (0.445) seconds
Test Suite 'ArendalsukaKnowledgeCellTests' passed at 2026-09-08 22:13:05.062.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'ArendalsukaKnowledgeSQLiteStoreTests' passed at 2026-09-08 22:13:05.073.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'ArendalsukaPersistedAtlasRecoveryTests' passed at 2026-09-08 22:13:09.908.
	 Executed 9 tests, with 0 failures (0 unexpected) in 4.835 (4.836) seconds
Test Suite 'ArendalsukaPublicSurfaceRouteTests' passed at 2026-09-08 22:13:09.927.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.019 (0.019) seconds
Test Suite 'ArtistSalesChannelCellTests' passed at 2026-09-08 22:13:09.985.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.057 (0.057) seconds
Test Suite 'AssistantCorrespondenceAdminRoutesTests' passed at 2026-09-08 22:13:10.908.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.923 (0.923) seconds
Test Suite 'AssistantCorrespondenceCellTests' passed at 2026-09-08 22:13:11.047.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.138 (0.139) seconds
Test Suite 'AssistantCorrespondenceOnboardingRoutesTests' passed at 2026-09-08 22:13:11.297.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.250 (0.250) seconds
Test Suite 'AssociatedDomainsRouteTests' passed at 2026-09-08 22:13:11.303.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'BookReferenceRoutesTests' failed at 2026-09-08 22:13:21.317.
	 Executed 6 tests, with 2 failures (0 unexpected) in 10.013 (10.014) seconds
Test Suite 'BrowserClientIdentityOfflineInspectorTests' passed at 2026-09-08 22:13:21.407.
	 Executed 20 tests, with 0 failures (0 unexpected) in 0.089 (0.090) seconds
Test Suite 'BrowserClientIdentityReconciliationTests' passed at 2026-09-08 22:13:21.411.
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.003 (0.004) seconds
Test Suite 'BrowserClientIdentityRecoveryExecutorTests' passed at 2026-09-08 22:13:21.548.
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.136 (0.137) seconds
Test Suite 'BrowserClientIdentityVaultKeyAgreementTests' passed at 2026-09-08 22:13:21.548.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'BrowserClientIdentityVaultTests' passed at 2026-09-08 22:13:22.032.
	 Executed 31 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.481 (0.484) seconds
Test Suite 'ButterpopPilotReadinessTests' passed at 2026-09-08 22:13:22.034.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ButterpopStudioProductTests' failed at 2026-09-08 22:13:26.269.
	 Executed 11 tests, with 18 failures (1 unexpected) in 4.234 (4.234) seconds
Test Suite 'CalendarSurfaceConfigurationTests' passed at 2026-09-08 22:13:26.285.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
Test Suite 'CellConfigurationStudioImportTests' passed at 2026-09-08 22:13:26.547.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.261 (0.261) seconds
Test Suite 'CellProtocolIdentityProofTests' passed at 2026-09-08 22:13:26.553.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'CellScaffoldRuntimeIdentityManifestTests' passed at 2026-09-08 22:13:26.694.
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.140 (0.141) seconds
Test Suite 'CellScaffoldRuntimeIdentityMigrationCandidateCommandTests' passed at 2026-09-08 22:13:26.767.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.072 (0.073) seconds
Test Suite 'CellScaffoldRuntimeIdentityMigrationPlannerTests' passed at 2026-09-08 22:13:26.784.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
Test Suite 'CellScaffoldRuntimeIdentityProvisionerTests' passed at 2026-09-08 22:13:26.921.
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.136 (0.137) seconds
Test Suite 'CellScaffoldRuntimeIdentityRegistryTests' passed at 2026-09-08 22:13:26.980.
	 Executed 21 tests, with 0 failures (0 unexpected) in 0.059 (0.059) seconds
Test Suite 'CellScaffoldRuntimeStorageRootTests' passed at 2026-09-08 22:13:26.984.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'CellScaffoldServiceIdentityManifestTests' passed at 2026-09-08 22:13:26.991.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'CellScaffoldServiceIdentityRegistryTests' passed at 2026-09-08 22:13:27.017.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.026 (0.026) seconds
Test Suite 'ChatAIGatewayDiscoveryCacheTests' passed at 2026-09-08 22:13:27.018.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'ChatAuthTokenManagerTests' passed at 2026-09-08 22:13:27.020.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ChatCellTests' passed at 2026-09-08 22:13:27.064.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.044 (0.044) seconds
Test Suite 'ChatInterpreterEscalationCeilingTests' passed at 2026-09-08 22:13:27.074.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.009 (0.010) seconds
Test Suite 'ChatMVPLoginScopingTests' passed at 2026-09-08 22:13:27.765.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.691 (0.691) seconds
Test Suite 'ChatMVPRoutesTests' failed at 2026-09-08 22:13:32.265.
	 Executed 10 tests, with 7 failures (0 unexpected) in 4.500 (4.501) seconds
Test Suite 'ChatPurposeResourceRouterTests' passed at 2026-09-08 22:13:32.764.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.496 (0.499) seconds
Test Suite 'ChatScopedAIProviderRegistryPersistenceTests' passed at 2026-09-08 22:13:32.774.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'ChatScopedAIProviderRouterTests' passed at 2026-09-08 22:13:32.782.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
Test Suite 'CodableTests' passed at 2026-09-08 22:13:32.782.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'ConciergeKnowledgeCorpusCellTests' passed at 2026-09-08 22:13:32.890.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.108 (0.108) seconds
Test Suite 'ConferenceAIAssistantConfigurationTests' passed at 2026-09-08 22:13:32.905.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
Test Suite 'ConferenceAgendaCellTests' passed at 2026-09-08 22:13:32.984.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.079 (0.079) seconds
Test Suite 'ConferenceAudienceDiscoveryCellTests' passed at 2026-09-08 22:13:33.114.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.130 (0.130) seconds
Test Suite 'ConferenceBroadcastStudioCellTests' passed at 2026-09-08 22:13:33.165.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.051 (0.052) seconds
Test Suite 'ConferenceConfigurationCatalogTests' passed at 2026-09-08 22:13:36.833.
	 Executed 3 tests, with 0 failures (0 unexpected) in 3.667 (3.667) seconds
Test Suite 'ConferenceConnectionHubCellTests' passed at 2026-09-08 22:13:37.066.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.233 (0.233) seconds
Test Suite 'ConferenceDemoStoryCellTests' passed at 2026-09-08 22:13:37.139.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.072 (0.073) seconds
Test Suite 'ConferenceEntityDiscoveryCellTests' failed at 2026-09-08 22:13:37.299.
	 Executed 11 tests, with 1 failure (1 unexpected) in 0.159 (0.160) seconds
Test Suite 'ConferenceInsightAggregateCellTests' passed at 2026-09-08 22:13:37.313.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
Test Suite 'ConferenceLiveInteractionShellBridgeTests' passed at 2026-09-08 22:13:37.335.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.021 (0.021) seconds
Test Suite 'ConferenceMVPSkeletonTests' passed at 2026-09-08 22:13:37.337.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ConferenceMessageExchangeAcceptanceTests' passed at 2026-09-08 22:13:37.516.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.179 (0.179) seconds
Test Suite 'ConferenceOnboardingCellTests' passed at 2026-09-08 22:13:37.563.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.047 (0.047) seconds
Test Suite 'ConferenceOrganizerProjectionCellTests' failed at 2026-09-08 22:13:37.641.
	 Executed 3 tests, with 7 failures (0 unexpected) in 0.078 (0.078) seconds
Test Suite 'ConferencePlaywrightIdentityVaultTests' passed at 2026-09-08 22:13:37.689.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.048 (0.048) seconds
Test Suite 'ConferencePreviewWrapperResolverSupportTests' passed at 2026-09-08 22:13:39.100.
	 Executed 6 tests, with 0 failures (0 unexpected) in 1.411 (1.411) seconds
Test Suite 'ConferenceProofChatLaunchCellTests' passed at 2026-09-08 22:13:39.124.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.024 (0.024) seconds
Test Suite 'ConferencePublicProfileCellTests' passed at 2026-09-08 22:13:39.560.
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.435 (0.436) seconds
Test Suite 'ConferencePublicShellReadinessTests' passed at 2026-09-08 22:13:39.968.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.408 (0.408) seconds
Test Suite 'ConferencePublishedContentCellTests' failed at 2026-09-08 22:13:40.022.
	 Executed 10 tests, with 1 failure (1 unexpected) in 0.054 (0.054) seconds
Test Suite 'ConferenceRecommendationCellTests' passed at 2026-09-08 22:13:40.073.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.051 (0.051) seconds
Test Suite 'ConferenceRegistrationCellTests' passed at 2026-09-08 22:13:40.085.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.011 (0.012) seconds
Test Suite 'ConferenceSchedulingCellTests' failed at 2026-09-08 22:13:40.122.
	 Executed 2 tests, with 1 failure (0 unexpected) in 0.037 (0.037) seconds
Test Suite 'ConferenceShellCellsTests' passed at 2026-09-08 22:13:45.641.
	 Executed 68 tests, with 0 failures (0 unexpected) in 5.514 (5.519) seconds
Test Suite 'ConferenceShellConfigurationFactoryTests' passed at 2026-09-08 22:13:45.871.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.230 (0.230) seconds
Test Suite 'ConferenceSimulationClockCellTests' passed at 2026-09-08 22:13:45.872.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ConferenceSimulationPlaybackCellTests' passed at 2026-09-08 22:13:45.974.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.102 (0.102) seconds
Test Suite 'ConferenceSimulationPopulationCellTests' passed at 2026-09-08 22:13:46.201.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.227 (0.227) seconds
Test Suite 'ConferenceSimulationStudioCellTests' passed at 2026-09-08 22:13:46.207.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'ConferenceSponsorLeadAggregateCellTests' failed at 2026-09-08 22:13:46.217.
	 Executed 2 tests, with 1 failure (1 unexpected) in 0.010 (0.010) seconds
Test Suite 'ConferenceSurfaceRoutesTests' failed at 2026-09-08 22:14:36.280.
	 Executed 39 tests, with 21 failures (0 unexpected) in 50.060 (50.063) seconds
Test Suite 'ConfigurationArchitectWorkspaceTests' passed at 2026-09-08 22:14:36.303.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.023 (0.023) seconds
Test Suite 'ConfigurationCatalogCellTests' passed at 2026-09-08 22:14:38.115.
	 Executed 31 tests, with 0 failures (0 unexpected) in 1.810 (1.812) seconds
Test Suite 'ConfigurationCatalogClientTests' passed at 2026-09-08 22:14:38.119.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'ConfigurationCatalogSkeletonParityTests' failed at 2026-09-08 22:14:38.617.
	 Executed 17 tests, with 2 tests skipped and 1 failure (0 unexpected) in 0.497 (0.498) seconds
Test Suite 'ContactEndpointCellTests' passed at 2026-09-08 22:14:40.214.
	 Executed 14 tests, with 0 failures (0 unexpected) in 1.596 (1.597) seconds
Test Suite 'ContactRegistryCellTests' passed at 2026-09-08 22:14:40.236.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.021 (0.022) seconds
Test Suite 'ContextTransitionPayloadFactoryTests' passed at 2026-09-08 22:14:40.237.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'ContractChallengeMVPRoutesTests' failed at 2026-09-08 22:14:41.449.
	 Executed 5 tests, with 9 failures (0 unexpected) in 1.212 (1.212) seconds
Test Suite 'CredentialSealingTests' passed at 2026-09-08 22:14:41.462.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.012 (0.013) seconds
Test Suite 'DevelopmentStatusRoutesTests' passed at 2026-09-08 22:14:43.591.
	 Executed 5 tests, with 0 failures (0 unexpected) in 2.129 (2.129) seconds
Test Suite 'DevelopmentStatusSnapshotProducerTests' passed at 2026-09-08 22:14:43.833.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.241 (0.242) seconds
Test Suite 'DevelopmentStatusSnapshotTests' passed at 2026-09-08 22:14:43.889.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.054 (0.055) seconds
Test Suite 'DeviceCallbackCapabilityServerTests' passed at 2026-09-08 22:14:43.972.
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.082 (0.083) seconds
Test Suite 'DeviceRegistrationReadinessTests' passed at 2026-09-08 22:14:43.986.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
Test Suite 'DocumentationWorkbenchRoutesTests' passed at 2026-09-08 22:14:44.208.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.222 (0.222) seconds
Test Suite 'EntityAnchorDataV1ContractTests' passed at 2026-09-08 22:14:44.430.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.221 (0.221) seconds
Test Suite 'EntityAtlasRoutesTests' passed at 2026-09-08 22:14:44.871.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.441 (0.441) seconds
Test Suite 'EntityCellGraphCellTests' passed at 2026-09-08 22:14:45.067.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.195 (0.196) seconds
Test Suite 'EntityGraphStorageTests' passed at 2026-09-08 22:14:45.069.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'EntityMergePolicyRegistryV0Tests' passed at 2026-09-08 22:14:45.152.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.081 (0.083) seconds
Test Suite 'EntityOperationEnvelopeV0Tests' passed at 2026-09-08 22:14:45.170.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.017 (0.018) seconds
Test Suite 'EntityScaffoldEnrollmentCellTests' passed at 2026-09-08 22:14:45.373.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.203 (0.204) seconds
Test Suite 'EntityStudioCellTests' passed at 2026-09-08 22:14:45.688.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.313 (0.314) seconds
Test Suite 'EntityStudioConfigurationFactoryTests' passed at 2026-09-08 22:14:45.715.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.027 (0.027) seconds
Test Suite 'EventPlatformRoutesTests' passed at 2026-09-08 22:14:47.238.
	 Executed 6 tests, with 0 failures (0 unexpected) in 1.522 (1.523) seconds
Test Suite 'EventPublisherRegistryCellTests' passed at 2026-09-08 22:14:47.249.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'ExecutablePurposeGroundingCellTests' passed at 2026-09-08 22:14:48.507.
	 Executed 36 tests, with 0 failures (0 unexpected) in 1.256 (1.258) seconds
Test Suite 'FlowDebugProbeCellTests' passed at 2026-09-08 22:14:48.544.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.036 (0.037) seconds
Test Suite 'FundingEntitlementAgreementTests' passed at 2026-09-08 22:14:48.547.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'GitHubWorkSyncCellTests' passed at 2026-09-08 22:14:48.551.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'GraphStoreCellTests' passed at 2026-09-08 22:14:49.069.
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.516 (0.518) seconds
Test Suite 'GuidedOnboardingCellTests' passed at 2026-09-08 22:14:49.302.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.232 (0.232) seconds
Test Suite 'HAVENAgentCapabilityBrokerCellTests' passed at 2026-09-08 22:14:49.466.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.164 (0.165) seconds
Test Suite 'HavenWorkbenchConfigurationTests' failed at 2026-09-08 22:14:49.606.
	 Executed 6 tests, with 1 failure (0 unexpected) in 0.139 (0.140) seconds
Test Suite 'IdeaTaskWorkspaceTests' passed at 2026-09-08 22:14:50.637.
	 Executed 20 tests, with 0 failures (0 unexpected) in 1.030 (1.032) seconds
Test Suite 'JWTAuthRoutesTests' passed at 2026-09-08 22:15:02.794.
	 Executed 13 tests, with 0 failures (0 unexpected) in 12.156 (12.157) seconds
Test Suite 'LeadVaultCellTests' passed at 2026-09-08 22:15:02.803.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'LeadVaultRoutesTests' passed at 2026-09-08 22:15:03.419.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.616 (0.616) seconds
Test Suite 'LiveInteractionCellTests' passed at 2026-09-08 22:15:03.555.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.135 (0.136) seconds
Test Suite 'LocalLLMGatewayCellTests' passed at 2026-09-08 22:15:03.563.
	 Executed 4 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.008 (0.008) seconds
Test Suite 'MVPAdminAccessTests' passed at 2026-09-08 22:15:03.566.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'MarkdownRendererCellTests' passed at 2026-09-08 22:15:03.593.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.027 (0.027) seconds
Test Suite 'MediaCollectionCellTests' passed at 2026-09-08 22:15:03.625.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.031 (0.032) seconds
Test Suite 'MermaidRendererCellTests' failed at 2026-09-08 22:15:19.181.
	 Executed 11 tests, with 14 failures (0 unexpected) in 15.554 (15.556) seconds
Test Suite 'MicropaymentsAuditRoutesTests' passed at 2026-09-08 22:15:19.646.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.465 (0.465) seconds
Test Suite 'MicropaymentsMVPRoutesTests' failed at 2026-09-08 22:15:19.878.
	 Executed 1 test, with 4 failures (0 unexpected) in 0.231 (0.231) seconds
Test Suite 'MintClientBootstrapTests' passed at 2026-09-08 22:15:19.879.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'MultilevelCodableTests' passed at 2026-09-08 22:15:19.880.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'MusicPublishingCellsTests' failed at 2026-09-08 22:15:20.033.
	 Executed 26 tests, with 3 failures (0 unexpected) in 0.152 (0.153) seconds
Test Suite 'MusicPublishingConfigurationFactoryTests' passed at 2026-09-08 22:15:20.092.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.058 (0.058) seconds
Test Suite 'MusicPublishingMVPRoutesTests' passed at 2026-09-08 22:15:20.302.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.210 (0.210) seconds
Test Suite 'NativeLocalModelBridgeTests' passed at 2026-09-08 22:15:20.303.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'NodeAdminAgentDeliveryTests' passed at 2026-09-08 22:15:20.304.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'NodeAdminAgentSnapshotBuilderTests' passed at 2026-09-08 22:15:21.717.
	 Executed 8 tests, with 0 failures (0 unexpected) in 1.412 (1.414) seconds
Test Suite 'NodeAdminDockerCollectorTests' passed at 2026-09-08 22:15:21.772.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.054 (0.055) seconds
Test Suite 'NotificationPushProviderTests' passed at 2026-09-08 22:15:21.972.
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.199 (0.200) seconds
Test Suite 'NotificationRuntimeReadinessTests' passed at 2026-09-08 22:15:22.040.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.067 (0.068) seconds
Test Suite 'ObjectStorageAdapterCellTests' passed at 2026-09-08 22:15:22.083.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.043 (0.043) seconds
Test Suite 'ObsidianAIWorkspaceConfigurationTests' passed at 2026-09-08 22:15:22.097.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
Test Suite 'OrchestratorPersistenceTests' passed at 2026-09-08 22:15:25.348.
	 Executed 7 tests, with 0 failures (0 unexpected) in 3.251 (3.251) seconds
Test Suite 'OwnerScopedCredentialCellTests' passed at 2026-09-08 22:15:25.405.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.057 (0.057) seconds
Test Suite 'OwnerScopedCredentialStoreTests' passed at 2026-09-08 22:15:25.428.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.022 (0.023) seconds
Test Suite 'PalazzoCommunaleRoutesTests' passed at 2026-09-08 22:15:25.660.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.232 (0.232) seconds
Test Suite 'PalazzoCommunaleServiceTests' passed at 2026-09-08 22:15:25.685.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.025 (0.025) seconds
Test Suite 'ParticipationHubCellTests' passed at 2026-09-08 22:15:25.724.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.039 (0.039) seconds
Test Suite 'ParticipationHubConfigurationFactoryTests' passed at 2026-09-08 22:15:25.737.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.012 (0.013) seconds
Test Suite 'PaymentAccessCredentialStoreLifecycleTests' passed at 2026-09-08 22:15:27.915.
	 Executed 13 tests, with 0 failures (0 unexpected) in 2.178 (2.179) seconds
Test Suite 'PaymentGateCellTests' passed at 2026-09-08 22:15:29.936.
	 Executed 14 tests, with 0 failures (0 unexpected) in 2.020 (2.020) seconds
Test Suite 'PaymentGateOwnerIdentitySupportTests' passed at 2026-09-08 22:15:29.943.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.007 (0.008) seconds
Test Suite 'PaymentProofDoorCellTests' passed at 2026-09-08 22:15:29.960.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
Test Suite 'PersistedRuntimeReadinessTests' passed at 2026-09-08 22:15:30.624.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.663 (0.663) seconds
Test Suite 'PersonalAIProviderPolicyTests' passed at 2026-09-08 22:15:30.629.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'PersonalAssistantProfileCellTests' passed at 2026-09-08 22:15:30.653.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.024 (0.024) seconds
Test Suite 'PersonalChatPromptEvaluationTests' passed at 2026-09-08 22:16:04.584.
	 Executed 11 tests, with 0 failures (0 unexpected) in 33.931 (33.931) seconds
Test Suite 'PersonalCopilotCollaborationInviteTests' passed at 2026-09-08 22:16:04.799.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.214 (0.214) seconds
Test Suite 'PersonalCopilotV1Tests' passed at 2026-09-08 22:16:16.661.
	 Executed 70 tests, with 0 failures (0 unexpected) in 11.858 (11.863) seconds
Test Suite 'PersonalDataTrustPackageCellTests' passed at 2026-09-08 22:16:16.677.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
Test Suite 'PersonalEntityActivityDashboardConfigurationTests' passed at 2026-09-08 22:16:17.441.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.764 (0.765) seconds
Test Suite 'PersonalPagePublisherCellTests' passed at 2026-09-08 22:16:17.463.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.022 (0.022) seconds
Test Suite 'PersonalPagePublisherConfigurationTests' passed at 2026-09-08 22:16:17.466.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.003) seconds
Test Suite 'PersonlogProjectionCellTests' passed at 2026-09-08 22:16:17.581.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.115 (0.115) seconds
Test Suite 'PerspectiveCellTests' passed at 2026-09-08 22:16:17.591.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'PortholeBootstrapProjectionTests' passed at 2026-09-08 22:16:17.608.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.016 (0.017) seconds
Test Suite 'PortholeConfigurationLoadingTests' failed at 2026-09-08 22:26:15.560.
	 Executed 45 tests, with 5 failures (0 unexpected) in 597.943 (597.952) seconds
Test Suite 'PortholeIdentityContinuityRoutesTests' passed at 2026-09-08 22:26:27.139.
	 Executed 4 tests, with 0 failures (0 unexpected) in 11.578 (11.578) seconds
Test Suite 'PortholeMenuFallbackTests' passed at 2026-09-08 22:26:27.267.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.128 (0.128) seconds
Test Suite 'PortholeRuntimeBindingEnsuringTests' passed at 2026-09-08 22:26:30.769.
	 Executed 10 tests, with 0 failures (0 unexpected) in 3.500 (3.503) seconds
Test Suite 'PortholeWebActionStateSourceTests' passed at 2026-09-08 22:26:30.781.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'PortholeWebEditorSupportTests' passed at 2026-09-08 22:26:30.788.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.007 (0.008) seconds
Test Suite 'PortholeWebPayloadTests' passed at 2026-09-08 22:26:30.855.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.066 (0.067) seconds
Test Suite 'PortholeWebSessionPersonaTests' passed at 2026-09-08 22:26:33.652.
	 Executed 15 tests, with 0 failures (0 unexpected) in 2.796 (2.796) seconds
Test Suite 'ProductionOwnerIdentityContinuityTests' passed at 2026-09-08 22:26:33.658.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'ProductionRuntimeAdmissionMiddlewareTests' passed at 2026-09-08 22:26:33.672.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
Test Suite 'ProductionSkeletonBindingIntegrityTests' failed at 2026-09-08 22:26:41.325.
	 Executed 4 tests, with 19 failures (1 unexpected) in 7.652 (7.652) seconds
Test Suite 'ProjectOperationsTests' passed at 2026-09-08 22:26:41.369.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.044 (0.045) seconds
Test Suite 'ProjectPortfolioCellTests' passed at 2026-09-08 22:26:41.409.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.039 (0.040) seconds
Test Suite 'ProofDoorMVPRouteSecurityTests' passed at 2026-09-08 22:26:41.411.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'PublishedConfigurationCatalogCellTests' passed at 2026-09-08 22:26:41.551.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.139 (0.139) seconds
Test Suite 'PurposeQualityMonitorCellTests' passed at 2026-09-08 22:26:41.566.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.015 (0.016) seconds
Test Suite 'QuestionnaireCampaignCellTests' passed at 2026-09-08 22:26:41.765.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.197 (0.198) seconds
Test Suite 'QuestionnaireCampaignRoutesTests' passed at 2026-09-08 22:26:42.762.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.997 (0.997) seconds
Test Suite 'QuestionnaireResponseCellTests' passed at 2026-09-08 22:26:42.774.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
Test Suite 'RAGCellAccessSecurityTests' passed at 2026-09-08 22:26:42.784.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'RAGGatewayCellTests' passed at 2026-09-08 22:26:42.807.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.022 (0.022) seconds
Test Suite 'RAGGatewayConfigTests' passed at 2026-09-08 22:26:42.808.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'RAGGatewayConfigurationFactoryTests' passed at 2026-09-08 22:26:42.809.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'RAGGatewayHTTPClientTests' passed at 2026-09-08 22:26:42.815.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.005 (0.006) seconds
Test Suite 'RAGIngestionCellTests' passed at 2026-09-08 22:26:42.824.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'RAGMVPRoutesTests' passed at 2026-09-08 22:26:43.884.
	 Executed 5 tests, with 0 failures (0 unexpected) in 1.060 (1.060) seconds
Test Suite 'RAGPersistedRuntimeReadinessTests' passed at 2026-09-08 22:26:43.962.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.077 (0.078) seconds
Test Suite 'RAGPromptAdminCellTests' passed at 2026-09-08 22:26:43.986.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.024 (0.024) seconds
Test Suite 'RAGPromptAdminConfigurationFactoryTests' passed at 2026-09-08 22:26:43.986.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'RemoteBridgeheadAccessTests' passed at 2026-09-08 22:26:43.989.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'RestaurantExperiencePlanCellTests' passed at 2026-09-08 22:26:44.004.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
Test Suite 'RestaurantOnboardingCellTests' passed at 2026-09-08 22:26:44.007.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'RestaurantPublishedContentCellTests' passed at 2026-09-08 22:26:44.013.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'RestaurantShellCellsTests' passed at 2026-09-08 22:26:44.040.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.028 (0.028) seconds
Test Suite 'RestaurantSurfaceRoutesTests' passed at 2026-09-08 22:26:45.526.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.485 (1.485) seconds
Test Suite 'RestaurantVisitContextCellTests' passed at 2026-09-08 22:26:45.532.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'SMIAgreementSettlementCellTests' passed at 2026-09-08 22:26:45.559.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.027 (0.027) seconds
Test Suite 'SalesWorkspaceCellTests' passed at 2026-09-08 22:26:45.596.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.036 (0.036) seconds
Test Suite 'ScaffoldLaunchRegistryCellTests' passed at 2026-09-08 22:26:45.640.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.044 (0.044) seconds
Test Suite 'ScaffoldNotificationContractsTests' passed at 2026-09-08 22:26:45.642.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ScaffoldOwnerAdminRoutesTests' passed at 2026-09-08 22:26:47.323.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.680 (1.680) seconds
Test Suite 'ScaffoldSetupCellTests' passed at 2026-09-08 22:26:50.498.
	 Executed 15 tests, with 0 failures (0 unexpected) in 3.174 (3.175) seconds
Test Suite 'ScaffoldSurfaceGatePolicyTests' passed at 2026-09-08 22:26:50.551.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.052 (0.053) seconds
Test Suite 'ScaffoldTruthSourceCatalogTests' passed at 2026-09-08 22:26:50.554.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'SecureDevelopmentStatusSnapshotFileTests' passed at 2026-09-08 22:26:50.574.
	 Executed 9 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.020 (0.020) seconds
Test Suite 'SecureRuntimeIdentityManifestFileTests' passed at 2026-09-08 22:26:50.592.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.018 (0.018) seconds
Test Suite 'SecurityWorkbenchCellTests' passed at 2026-09-08 22:26:50.616.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.024 (0.024) seconds
Test Suite 'SkeletonElementParityMatrixTests' failed at 2026-09-08 22:26:50.954.
	 Executed 3 tests, with 2 failures (0 unexpected) in 0.338 (0.338) seconds
Test Suite 'SkeletonParityRoutesTests' passed at 2026-09-08 22:26:51.821.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.866 (0.866) seconds
Test Suite 'SkeletonPortableModelTests' passed at 2026-09-08 22:26:51.865.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.044 (0.045) seconds
Test Suite 'SkeletonRuntimeDecoderTests' passed at 2026-09-08 22:26:51.867.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'SkeletonRuntimeSourceTests' failed at 2026-09-08 22:26:52.029.
	 Executed 16 tests, with 1 failure (0 unexpected) in 0.161 (0.162) seconds
Test Suite 'SkeletonStyleParityCSSDriftTests' passed at 2026-09-08 22:26:52.057.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.028 (0.028) seconds
Test Suite 'SpatialCellsTests' passed at 2026-09-08 22:26:52.072.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
Test Suite 'SpatialRegistryRemoteIntegrationTests' passed at 2026-09-08 22:26:52.073.
	 Executed 1 test, with 1 test skipped and 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'SproutBridgeDiscoveryRoutesTests' passed at 2026-09-08 22:26:53.169.
	 Executed 5 tests, with 0 failures (0 unexpected) in 1.097 (1.097) seconds
Test Suite 'SproutExecutableCatalogRoutesTests' passed at 2026-09-08 22:26:53.391.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.221 (0.221) seconds
Test Suite 'SproutResolverRoutesTests' passed at 2026-09-08 22:26:54.073.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.682 (0.682) seconds
Test Suite 'StrictIdentityVaultReadinessMonitorTests' passed at 2026-09-08 22:26:54.074.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'SwarmIdentityAdmissionCellTests' passed at 2026-09-08 22:26:54.110.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.037 (0.037) seconds
Test Suite 'TodoCellConfigurationTests' passed at 2026-09-08 22:26:54.111.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'TodoPlannerCopilotConfigurationTests' passed at 2026-09-08 22:26:54.126.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
Test Suite 'TopUpCheckoutTests' failed at 2026-09-08 22:26:56.752.
	 Executed 19 tests, with 3 failures (3 unexpected) in 2.625 (2.626) seconds
Test Suite 'TranscriptStoreCellTests' passed at 2026-09-08 22:26:56.786.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.033 (0.034) seconds
Test Suite 'TrustPacketConfigurationFactoryTests' passed at 2026-09-08 22:26:56.896.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.109 (0.110) seconds
Test Suite 'UserSimulationScaffoldTests' passed at 2026-09-08 22:26:58.573.
	 Executed 28 tests, with 1 test skipped and 0 failures (0 unexpected) in 1.674 (1.677) seconds
Test Suite 'VaporProductControlDurabilityTests' passed at 2026-09-08 22:26:58.637.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.063 (0.064) seconds
Test Suite 'VaultMVPRoutesTests' passed at 2026-09-08 22:27:01.512.
	 Executed 6 tests, with 0 failures (0 unexpected) in 2.875 (2.876) seconds
Test Suite 'VaultStudioWorkspaceTests' passed at 2026-09-08 22:27:01.536.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.023 (0.024) seconds
Test Suite 'WebKnowledgeCellsTests' passed at 2026-09-08 22:27:01.569.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.033 (0.033) seconds
Test Suite 'WorkItemCellTests' passed at 2026-09-08 22:27:01.594.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.024 (0.024) seconds
Test Suite 'WorkbenchAccessGrantConfigurationTests' failed at 2026-09-08 22:27:03.929.
	 Executed 24 tests, with 1 failure (1 unexpected) in 2.334 (2.336) seconds
Test Suite 'WorkbenchOwnerSetupCellTests' passed at 2026-09-08 22:27:11.822.
	 Executed 7 tests, with 0 failures (0 unexpected) in 7.892 (7.893) seconds
Test Suite 'CellsContainerPackageTests.xctest' failed at 2026-09-08 22:27:11.822.
	 Executed 2059 tests, with 11 tests skipped and 151 failures (9 unexpected) in 857.721 (857.866) seconds
Test Suite 'All tests' failed at 2026-09-08 22:27:11.825.
	 Executed 2059 tests, with 11 tests skipped and 151 failures (9 unexpected) in 857.721 (857.868) seconds
```

</details>

Direkte `xctest` dekker XCTest-bundlen. Swift Testing-mål er ikke kjørt med denne banen. WP2-testene er XCTest og er kjørt både isolert og i full bundle. Logger og maskinell sammenligning: `/private/tmp/wp2-agent-trust/`; relevant evidens er bevart her.

### WP2 — avvik i feilrapportantall: 151 mot 148

Fullkjøringen har **samme 46 røde testtilfeller** som baseline, men 3 ekstra assert-rapporter i den allerede røde `PortholeConfigurationLoadingTests.testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction`. Ingen andre testtilfeller har endret antall feilrapporter (maskinelt sammenlignet: 148 → 151). De tre gjelder bootstrap-projeksjonen etter eksisterende WebView-render-timeout:

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:993: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertEqual failed: ("Optional(CellBase.ValueType.bool(false))") is not equal to ("Optional(CellBase.ValueType.bool(true))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:994: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertTrue failed - Expected rendered preview HTML in projected bootstrap state.
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:998: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertEqual failed: ("Render timed out after 2000ms") is not equal to ("")
```

Målrettet omkjøring av akkurat dette testtilfellet, uendret kildekode/bundle:

```sh
xcrun --sdk macosx xctest -XCTest AppTests.PortholeConfigurationLoadingTests/testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Ekte utdata fra omkjøringen:

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:968: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertTrue failed - Expected webview render to succeed: [CellBase.ValueType.string("Render timed out after 2000ms")]
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:969: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertNotNil failed
Test Case '-[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction]' failed (5.392 seconds).
	 Executed 1 test, with 2 failures (0 unexpected) in 5.392 (5.392) seconds
	 Executed 1 test, with 2 failures (0 unexpected) in 5.392 (5.392) seconds
	 Executed 1 test, with 2 failures (0 unexpected) in 5.392 (5.395) seconds
```

Omkjøringen ga de samme 2 rapportene som baseline (`968`/`969`), mens fullkjøringen også ga `993`/`994`/`998`. Dette viser variasjon i den allerede røde render-/bootstrap-banen. Den er ikke rettet eller svekket i WP2. Kravet om ingen nye røde testtilfeller utenfor baseline-listen er oppfylt; totalen for fullkjøringen rapporteres fortsatt som **151**, ikke 148.

## WP2 — sluttmelding

WP2 er **levert med dokumenterte kildeavvik**, for `purpose://candidate.tillitspakke-agentflaate.projeksjon`, `purpose://cell.contract-explicit` og `purpose://cell.authorization-honours-keypath`.

Levert i CellScaffold: `AgentTrustPackageCell.swift`, `AgentTrustPackageContract.swift`, `AgentTrustPackageConfigurationFactory.swift`, begge `.identityUnique`/`.persistant`-registreringene i `configure.swift`, og `AgentTrustPackageCellTests.swift`. WP1s pakkemodell brukes direkte. Alle normative keypaths/Grants er registrert; `fleet.set` og `regenerate` projiserer kilder med stabil digest; utsatte handlinger gir eksplisitt `not-implemented`. Godkjent skeleton-struktur er bevart. `ACCEPT.md#stubs` lister de utsatte handlerne.

Bygg grønt. **13/13 nye tester grønne** både isolert og i helkjøringen. Endelig full XCTest-bundle: **2059 tester, 11 hoppet over, samme 46 røde testtilfeller som baseline, ingen nye røde testnavn**. Fullkjøringen tok **857.868 s** og hadde **151 feilrapporter (9 uventede)**; økningen på 3 ligger i én tidligere rød Mermaid-test, og målrettet omkjøring ga baseline-antallet 2. Ekte utdata og sammenligning står under [Kontrakt og autorisasjon](#contract).

Kildeavvik: PurposeBoundAIGateway har ingen lesbar gjeldende modellrute/systeminstruksjon; de følger invokasjonen. WP2 markerer fraværet ærlig og viser den faktiske statiske execution-policyen. Vanlig AIGateways lesbare utkast kan projiseres som utkast med rute- og instruksjons-digest. EntityAnchor-data uten verifiserbar kilde/kvittering blir aldri tatt med som Contracts (`verified=false` i state). WebFetch viser tom hostliste og «ingen whitelist ennå (WP5)». Ingen rekkevidde, godkjenning/startport, WebFetch-endring eller Porthole-paritetsleveranse er implementert her. Swift Testing er ikke dekket av direkte xctest-banen.

`STATUS.md` har fått én WP2-linje under Logg. Ingen git-kommandoer er kjørt. Formål og pakke gir ingen rettigheter.

## Rekkevidde <a id="rekkevidde"></a>

purposeRef: `purpose://candidate.tillitspakke-agentflaate.rekkevidde`. Kun WP3.

### WP3 — baseline før endring

Kjørt i `CellScaffold`, uten arch-prefiks:

```sh
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Ekte utdata (exit 0 for begge):

```text
Build complete! (16.33s)
Test Suite 'AgentTrustPackageCellTests' started at 2026-09-08 22:32:37.438.
Test Suite 'AgentTrustPackageCellTests' passed at 2026-09-08 22:32:37.625.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.187 (0.187) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.187 (0.187) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.187 (0.189) seconds
```

WP3-testklassen finnes ikke før endringen. WP2-baseline er 13 tester, 0 feil. Logger: `/private/tmp/wp3-agent-trust/baseline-build.log` og `baseline-cell.log`. Full bundle er **ikke kjørt i WP3**; den er ikke påkrevd her (WP5/WP13). Direkte xctest dekker ikke Swift Testing-mål.

### WP3 — implementasjon og kildegrenser

Levert `CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustReach.swift`, koblet til `AgentTrustPackageCell.regenerate` og `trustPackage.state.reach`. Hjelpetypen er ren og resolver-fri; ingen CellBase-/resolverendring. Formål: `purpose://candidate.tillitspakke-agentflaate.rekkevidde` (kommentarer i berørte kodefiler).

- `edges` avledes på nytt fra kilder. Contract må være verifisert av WP2s eksisterende kryptografiske re-lesing, binde subject til kildecellens eieridentitet, være u-utløpt og ha gyldig rwxs-form. Mål-keypath må finnes eksakt i mål-templaten. Bare keypath uten mål-felt må være entydig i flåten; alternativt støttes `cell:///Target#keypath` i den projiserte Grant-adressen. Ukjent/tvetydig mål, feil subject, utløp eller manglende Grant gir ingen kant. Identiske kanter dedupliseres; forskjellige keypaths/flagg beholdes.
- Leser annonserte `configuration`, `cellConfiguration` og `skeletonConfiguration` som typet CellConfiguration. Initiale GET/SET-keypaths i `cellReferences`, deres tildelinger, nestede subscriptions og kjente tilgjengelige skeleton-handlinger gir kandidater. Referanse alene gir ingen kant. Kandidatens eksakte keypath/flagg må finnes i mål-templaten og bestå eksisterende `validateAccess` med requesteren som har bevist eierskap til caller-cellen. Ingen konfigurasjon installeres og ingen flåtehandling utføres. Payloads tas ikke med i evidensen. Dette er kjente deklarerte kall, ikke en analyse av vilkårlige Swift-kall eller modellens fremtidige handlinger.
- V1 beholder WP2s eieravgrensning: alle valgte celler må tilhøre requesteren. Den offentlige eieridentiteten brukes til Contract-subject-binding; eksisterende innlogget identitet med bevis brukes til runtime-tilgang. WP2s begrensning til verifiserbare owner-snapshots i EntityAnchor er beholdt; ingen nye bilaterale Contract-/identitetsmekanismer er implementert.
- Per `role=agent`: alle enkle cellestier, maks 4 kanter, uten gjenbesøk. Observerte bakkant-/selvkant-Grants kan stå i `edges`, men gir ingen syklisk sti. Parallelle Grants og ledd på samme sti summeres med snitt av rwxs-flagg; separate enkle stier beholdes. Over 4096 stier per agent avvises hele projeksjonen (ingen stille avkorting).
- Destinasjoner tas fra målcellens ceiling: WebFetch bruker utelukkende `hostPatterns`, øvrige celler `destinations`. Tom liste vises eksplisitt som «ingen». Hver flåtecelle uten påvist sti fra agenten får en fraværsrad med `----`, `credentials=false` og «Ingen vei. Ingen Grant.». Fireleddsgrensen gjelder også disse radene.
- `credentials=true` bare når agenten har en sti innen dybdegrensen med r/x-Grant til `cell:///ScopedCredential` på `credentials` eller en eksakt annonsert under-keypath. Read på `state`, `credential.upsert`, write-only eller en annen secrets-celle er ikke tilstrekkelig. Flagget beskriver tilgjengelig credential-Grant for agenten; det påstår ikke at WebFetch bruker en credential. WebFetchs separate `allowCredentials` vises i summary. Ingen credential løses opp under projeksjon eller tester.
- Fixturens lokale leverandørrad `[aigateway]` viser `--x-` som invokasjonseffekt fra den annonserte `ai.invokePurposeBound`/`ai.invoke`-operasjonen og disclosure-ceiling. Den lager ingen syntetisk selvkant. Fixture-Contract `web.fetch --x-` og dagens template `web.fetch rw--` er forskjellige; WP3 bevarer Contract-flaggene og krever template-keypath, uten å gjøre dette til runtime-autorisasjon. Den faktiske konfigurasjonstesten får `rw--` fra uendret WebFetch. Kant→kontrakt-tabell og alle tre fixture-radene er dokumentert under [PLAN.md#dataflow](PLAN.md#dataflow), **lagt til etter E1–E10**.
- Både `edges` og listeformen av `reach` settes før WP1s kanoniske digest beregnes. Tester isolerer edge-only- og reach-only-endringer fra Contract-endringer og viser ny digest. Uendret input og tilbakeført kjent konfigurasjonskall gir samme digest. Norske `{pathLabel, summaryLabel}` avledes fra samme pakke; runtime-testen sammenligner hele state-listens kanoniske wire-representasjon med pakkeprojeksjonen.
- WP2-testens tidligere plassholderkrav `reach.count == 0` er erstattet med **3 rader og eksplisitt «Ingen vei. Ingen Grant.» for både WebFetch og ScopedCredential**. Ingen test er fjernet; alle øvrige WP2-krav består. Nye tester er i `CellScaffold/Tests/AppTests/AgentTrustPackageReachTests.swift`.

Dagens WebFetch har fortsatt ingen implementert whitelist-ceiling: hostlisten forblir tom og vises som ingen. Fixture-domener er syntetiske testinput, ikke påstått levende konfigurasjon. Ingen endring i WebFetch, justerings-/godkjenningshandlinger, startport, skeleton eller registrering. Ingen ny autorisasjonsmekanisme, ingen git-kommandoer.

### WP3 — første målrettede forsøk og retting

Første implementasjonsbygg var grønt: `Build complete! (58.68s)`. Første WP3-kjøring fant 4 assert-feil i én runtime-test (9 øvrige tester grønne): offentlig eier-snapshot manglet runtime-nøkkelbevis, slik at den kjente konfigurasjonskanten ble utelatt. Rettet ved å bruke requesteren som allerede beviser eierskap til kildecellen; samme ordinære `validateAccess` beholdes. Én av de fire assertionene sammenlignet `ValueType.list/object` direkte, men core returnerer alltid false for slik likhet; testen sammenligner nå sortert, kodet wire-data. To supplerende tester dekker nestede kall/tildelinger og transitive credentials per agent med parallelle Grant-flagg.

Ekte utdata fra første forsøk (`reach-1.log`, exit 1):

```text
Test Case '-[AppTests.AgentTrustPackageReachTests testRuntimeConfigurationEdgeUpdatesPackageDigestAndState]' failed (1.799 seconds).
	 Executed 10 tests, with 4 failures (0 unexpected) in 1.843 (1.843) seconds
	 Executed 10 tests, with 4 failures (0 unexpected) in 1.843 (1.843) seconds
	 Executed 10 tests, with 4 failures (0 unexpected) in 1.843 (1.845) seconds
```

WP2 var også grønn under dette forsøket (`cell-1.log`, 13 tester, 0 feil); endelig omkjøring følger nedenfor.

### WP3 — endelig bygg og målrettede tester

Kjørt i `CellScaffold` i denne rekkefølgen, etter regel 9/10, alle exit 0:

```sh
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageReachTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Ekte byggutdata (`build-2.log`):

```text
Build complete! (23.63s)
```

Ekte WP3-testutdata (`reach-2.log`):

```text
Test Suite 'Selected tests' started at 2026-09-08 22:45:04.621.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-08 22:45:04.626.
Test Suite 'AgentTrustPackageReachTests' started at 2026-09-08 22:45:04.626.
Test Case '-[AppTests.AgentTrustPackageReachTests testConfigurationReferencesRequireKnownKeypathTemplateAndRuntimeAdmission]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testConfigurationReferencesRequireKnownKeypathTemplateAndRuntimeAdmission]' passed (0.025 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testCredentialGrantChangesReachAndDigestWithoutResolvingAnyCredential]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testCredentialGrantChangesReachAndDigestWithoutResolvingAnyCredential]' passed (0.062 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testCredentialMetadataWriteAndUnreachableGrantsNeverSetCredentialFlag]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testCredentialMetadataWriteAndUnreachableGrantsNeverSetCredentialFlag]' passed (0.023 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testCycleAToBToATerminatesWithoutRepeatedCellsInPaths]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testCycleAToBToATerminatesWithoutRepeatedCellsInPaths]' passed (0.002 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testDepthFourAndMinimumCommonPermissionsOnTransitivePaths]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testDepthFourAndMinimumCommonPermissionsOnTransitivePaths]' passed (0.002 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testEmptyHostPatternsMeanNoDestinationsEvenWithOtherCeilingDestinations]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testEmptyHostPatternsMeanNoDestinationsEvenWithOtherCeilingDestinations]' passed (0.004 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testEveryEdgeHasContractGrantAndExactTargetTemplateAndFabricationsAreRejected]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testEveryEdgeHasContractGrantAndExactTargetTemplateAndFabricationsAreRejected]' passed (0.003 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testExpiredUnverifiedWrongSubjectMalformedAndAmbiguousContractsFailClosed]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testExpiredUnverifiedWrongSubjectMalformedAndAmbiguousContractsFailClosed]' passed (0.003 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testFixtureFleetMatchesThreeReachRowsSemantically]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testFixtureFleetMatchesThreeReachRowsSemantically]' passed (0.009 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testInitialReadsAssignmentsAndNestedSubscriptionsYieldOnlyTemplateCandidates]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testInitialReadsAssignmentsAndNestedSubscriptionsYieldOnlyTemplateCandidates]' passed (0.001 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testRuntimeConfigurationEdgeUpdatesPackageDigestAndState]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testRuntimeConfigurationEdgeUpdatesPackageDigestAndState]' passed (0.098 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testTransitiveCredentialsAreScopedPerAgentAndParallelPermissionsUseIntersection]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testTransitiveCredentialsAreScopedPerAgentAndParallelPermissionsUseIntersection]' passed (0.002 seconds).
Test Suite 'AgentTrustPackageReachTests' passed at 2026-09-08 22:45:04.863.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.235 (0.237) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-08 22:45:04.863.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.235 (0.237) seconds
Test Suite 'Selected tests' passed at 2026-09-08 22:45:04.863.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.235 (0.243) seconds
```

Ekte WP2-regresjonsutdata (`cell-2.log`):

```text
Test Suite 'Selected tests' started at 2026-09-08 22:45:13.665.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-08 22:45:13.666.
Test Suite 'AgentTrustPackageCellTests' started at 2026-09-08 22:45:13.666.
Test Case '-[AppTests.AgentTrustPackageCellTests testCanonicalPackageAndTwoRegenerationsHaveSameDigestAndEmitEvidence]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testCanonicalPackageAndTwoRegenerationsHaveSameDigestAndEmitEvidence]' passed (0.098 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testChangingOneTemplateGrantChangesDigest]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testChangingOneTemplateGrantChangesDigest]' passed (0.043 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testClaimedVerifiedEntityRecordWithoutCryptographicReceiptIsExcluded]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testClaimedVerifiedEntityRecordWithoutCryptographicReceiptIsExcluded]' passed (0.032 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testConfigurationPreservesApprovedSkeletonAndNestedStateBindings]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testConfigurationPreservesApprovedSkeletonAndNestedStateBindings]' passed (0.019 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testDeferredOperationsReturnExplicitNotImplementedWithoutChangingDigest]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testDeferredOperationsReturnExplicitNotImplementedWithoutChangingDigest]' passed (0.039 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testFixtureFleetProjectsActualTemplatesAndHonestMissingSources]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testFixtureFleetProjectsActualTemplatesAndHonestMissingSources]' passed (0.031 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testInvalidEndpointAndMissingResolverDoNotProduceDerivedEvidence]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testInvalidEndpointAndMissingResolverDoNotProduceDerivedEvidence]' passed (0.031 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testPersistedSelectionRequiresFreshSourceReadAndRetainsDigest]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testPersistedSelectionRequiresFreshSourceReadAndRetainsDigest]' passed (0.050 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testReadableDraftRouteAndInstructionAreProjectedWithoutPromptOrCredentials]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testReadableDraftRouteAndInstructionAreProjectedWithoutPromptOrCredentials]' passed (0.082 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testStrictExploreContractsMatchNormativeKeysAndGrants]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testStrictExploreContractsMatchNormativeKeysAndGrants]' passed (0.017 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownKeypathsAndWrongMethodsFailClosed]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownKeypathsAndWrongMethodsFailClosed]' passed (0.005 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownPurposeCannotAuthorizeOrAlterFleet]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownPurposeCannotAuthorizeOrAlterFleet]' passed (0.045 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testWrongRequesterCannotReadWriteOrUseDeferredActions]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testWrongRequesterCannotReadWriteOrUseDeferredActions]' passed (0.032 seconds).
Test Suite 'AgentTrustPackageCellTests' passed at 2026-09-08 22:45:14.195.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.527 (0.528) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-08 22:45:14.195.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.527 (0.529) seconds
Test Suite 'Selected tests' passed at 2026-09-08 22:45:14.195.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.527 (0.530) seconds
```

**Full XCTest-bundle er ikke kjørt i WP3.** Den er ikke påkrevd for denne slicen og hører til WP5/WP13. Swift Testing-mål er heller ikke kjørt/dekket av direkte xctest; de to valgte klassene er XCTest. Det er ikke gjort noen påstand om status for resten av bundlen. Logger ligger i `/private/tmp/wp3-agent-trust/`; relevante ekte utdata er bevart over.

## WP3 — sluttmelding

WP3 — rekkevidde er **levert** for `purpose://candidate.tillitspakke-agentflaate.rekkevidde`. Ren `AgentTrustReach` avleder Grant-kanter og rekkevidde inntil fire ledd, viser utilgjengelige tjenester eksplisitt, og mater norske state-rader og pakke-digest i `AgentTrustPackageCell`.

Bygg grønt. **12/12 WP3-tester og 13/13 WP2-tester grønne**, med ekte `Executed`-linjer over. Testene dekker fixture-radene, Grant-evidens og fabrikert kant, credential-Grant med ny digest, syklus, dybdegrense, rwxs-snitt, negative kilder, tom hostliste, konfigurasjonskall og runtime-state/digest. Første runtime-testfeil ble rettet uten å svekke tilgangskontrollen.

Kant→kontrakt-tabellen er lagt til i `PLAN.md#dataflow`; `STATUS.md` har én WP3-linje under Logg. Dokumenterte kildegrenser: fixture-Contract `--x-` mot template `rw--`, eier-scopede kilder, begrenset kjent konfigurasjonskallflate og fortsatt manglende live WebFetch-ceiling. Full bundle er **ikke kjørt i WP3**. WebFetch, justering og godkjenning er urørt. Ingen git. Formål og pakke gir aldri rettigheter.

## Leverandørverktøy <a id="provider-tools"></a>

purposeRef: `purpose://candidate.tillitspakke-agentflaate.leverandorverktoy`. Kun WP4.

### WP4 — baseline før endring

Kjørt i `CellScaffold`, uten arch-prefiks, alle exit 0:

```sh
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.AIGatewayCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Ekte utdata (`baseline-build.log`):

```text
Build complete! (22.68s)
```

Ekte utdata (`baseline-cell.log`):

```text
Test Suite 'Selected tests' started at 2026-09-08 22:59:42.360.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-08 22:59:42.361.
Test Suite 'AgentTrustPackageCellTests' started at 2026-09-08 22:59:42.361.
Test Suite 'AgentTrustPackageCellTests' passed at 2026-09-08 22:59:42.604.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.242 (0.243) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-08 22:59:42.604.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.242 (0.243) seconds
Test Suite 'Selected tests' passed at 2026-09-08 22:59:42.604.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.242 (0.244) seconds
```

Ekte utdata (`baseline-gateway.log`):

```text
Test Suite 'Selected tests' started at 2026-09-08 23:00:13.339.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-08 23:00:13.339.
Test Suite 'AIGatewayCellTests' started at 2026-09-08 23:00:13.339.
Test Suite 'AIGatewayCellTests' passed at 2026-09-08 23:00:13.474.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.133 (0.135) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-08 23:00:13.474.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.133 (0.135) seconds
Test Suite 'Selected tests' passed at 2026-09-08 23:00:13.474.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.133 (0.136) seconds
```

Ny WP4-testklasse finnes ikke før endringen. Baseline: 13 pakketester og 48 gatewaytester, 0 feil. Logger i `/private/tmp/wp4-provider-tools/`. Full bundle er ikke påkrevd i WP4 og er ikke kjørt. Direkte xctest dekker ikke Swift Testing-mål; de valgte klassene er XCTest.

### WP4 — produksjonsbane og implementasjon

Last verified against code: 2026-09-08.

Alle rutene bruker `AIGatewayOpenAICompatibleProvider` i `CellScaffold/Sources/App/Cells/AI/AIGatewaySupport.swift:953`. `invoke` kaller `requestBody` på linje 994, og serialiserer resultatet til `URLRequest.httpBody` på linje 995. Dispatch skjer i `requestBody` på linje 1050:

| Provider / format | Produksjonens body-bygger | WP4-dekning |
|---|---|---|
| openai / chat completions | `openAIChatCompletionsBody`, linje 1065 | uten policy + denyAll + allowListed + auditOnly |
| openai / responses | `openAIResponsesBody`, linje 1085 | samme fire varianter |
| openai-compatible / chat completions | `openAIChatCompletionsBody`, linje 1065 | samme fire varianter |
| openai-compatible / responses | `openAIResponsesBody`, linje 1085 | samme fire varianter |
| anthropic / messages | `anthropicMessagesBody`, linje 1109 | samme fire varianter |
| mistral / chat completions | `openAIChatCompletionsBody`, linje 1065 | samme fire varianter |
| local-llm / chat completions | `openAIChatCompletionsBody`, linje 1065 | samme fire varianter, loopback-profil uten credential |
| local-gemma4 / chat completions | `openAIChatCompletionsBody`, linje 1065 | samme fire varianter, loopback-profil uten credential |

`AIGatewayCell.swift:233` velger denne produksjonsadapteren og linje 1836 kaller den med rutet request. `LocalLLMGatewayCell.swift:456` velger samme adapter; linje 681 og 745 kaller den. Ingen av disse cellene bygger en egen provider-HTTP-body. LocalLLMGateway har derfor ingen separat body-bygger som måtte endres. Kildekontrollen fant ingen verktøykanal i body-byggerne. **Adapterne, AIGatewayCell og LocalLLMGatewayCell er uendret.** Endringen i AIGatewaySupport gjelder bare den felles hasheren.

`AIGatewayProviderToolsOffTests.swift` bruker produksjonens `invoke` med injisert `URLSession`/`URLProtocol`, leser den ferdig serialiserte bodyen (også `httpBodyStream`) og kontrollerer URL, metode, modell og prompt/formatsærpreg. Bare transportresponsen er en fixture; ingen nettverkskall eller levende provider-/credential-oppslag. Det bygges ingen kopi av request-bodyen i testen. Alle **32 HTTP-bodyer** sjekkes rekursivt for `tools`, `tool_choice`, `functions`, `function_call`, `web_search`, `web_search_options`, `code_interpreter`, `computer_use`, `mcp_servers`, `builtin_tools`; også prefiksene `web_search*` og `computer*` fanges opp. Testene krever lik body med og uten toolPolicy når adapterinput ellers er likt.

Hashing: eksisterende normalisering av `AIGatewayInvokeRequest` og cache-nøkkel er beholdt. Den tidligere encoder-/SHA256-koden er samlet i en `contentHash<Payload: Encodable>(for:)`-overload som både den eksisterende normaliserte produksjonsbanen og body-testene bruker. For hver fanget body legges hvert av de ti feltene til separat på roten og dypt i objekt/array; `AIGatewayHasher().contentHash(for:)` må endres. Feltets verdi true→false må også endre hash. Kontroll av skanneren verifiserer faktiske feltstier, inkludert prefiksvarianter; verktøynavn i vanlig prompttekst regnes ikke som JSON-felt. Den separate typede request-testen viser ny contentHash ved toolPolicy og ved hvert deklarert verktøynavn. Sortering/whitespace i body-JSON gir stabil hash.

**Presis hashgrense:** den normaliserte invoke-hashen og hashen av provider-bodyen gjelder forskjellige representasjoner. `AIGatewayInvokeRequest` har ikke vilkårlige provider-felt; testen later ikke som om JSONDecoder bevarer ukjente toppnivåfelt i denne typen. Body-mutasjonene hashes som hele dekodede JSON-bodyer gjennom den felles produksjonshasheren. WP4 endrer ikke kvitteringsformatet eller `AIGatewayPurposePolicy` sin `payloadDigest` til en hash av HTTP-bytes. Eksisterende purpose-bane binder fortsatt normalisert request og `no-tools` i planDigest. Regresjonsvakten mot en fremtidig adapter er den faktiske body-skanningen sammen med hashens endringssensitivitet; dette er ikke en påstand om hva leverandøren gjør internt eller beholder.

`AgentTrustPackageCell.swift` bruker én `requiredProviderTools = .off`-regel og én eksakt label: **«Leverandørverktøy (web search, kodekjøring): AV — bundet i forespørselen»**. PurposeBoundAIGateway, vanlig AIGateway og LocalLLMGateway projiseres som agenter med denne verdien i `ceiling.providerTools` før WP1s kanoniske pakke-digest beregnes. Tjenester får ingen agent-label. Vanlig/lokal gateway uten lesbar execution-policy har fortsatt `policy=nil` og viser «ingen lesbar effekt-policy»; den nødvendige ceiling-strukturen har tomme destinasjons-/dataklasse-/metodelister og false for ukjente effektflagg, ikke en ny policy eller nye Grants. `https` er false for LocalLLMGateway og true for de øvrige gatewayklassene. WP2s kildegrenser for gjeldende rute og instruksjon er ikke utvidet i WP4.

To nye tester i `AgentTrustPackageCellTests.swift` kontrollerer pakke-JSON og reell `trustPackage.state`/under-keypath for de tre gatewayklassene. En generert pakkekopi får agentens providerTools endret fra `off` til `n/a` (den andre eksisterende v0-enumverdien): ny kanonisk digest og varsel fra **samme statusLabel-funksjon som runtime-GET bruker**. Manglende ceiling varsler også; ukjent enumverdi `on` avvises allerede ved dekoding. Ingen test-SET, privat mutasjonsbakdør eller pakkeimport er lagt til for å installere den manipulerte kopien. Produksjonscellens pakke forblir uendret. Warning er presentasjon av evidens; godkjenning/startport hører fortsatt til WP7.

Ingen offentlige keypaths/Grants, resolverregler, skeletons, pakke-modell i CellProtocol, WebFetch, justering, godkjenning eller kvitteringer er endret. Ingen eksisterende tester er fjernet eller svekket. PurposeRef står i alle fire berørte Swift-filer. Ingen git-kommandoer.

### WP4 — første verifikasjon

Første bygg etter implementasjon var grønt (`build-1.log`): `Build complete! (61.22s)`. Første målrettede tester var alle grønne: 10 provider-tester, 15 pakketester og 48 gatewaytester. Deretter ble ceiling-labelen presisert slik at bare kjent tools-off-regel ikke fremstilles som en lesbar execution-policy for vanlig/lokal gateway; en assertion beskytter denne grensen. Endelig bygg og tester følger nedenfor.

### WP4 — endelig bygg og målrettede tester

Kjørt i `CellScaffold`, uten arch-prefiks, alle exit 0:

```sh
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest -XCTest AppTests.AIGatewayProviderToolsOffTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageReachTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.LocalLLMGatewayCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.AIGatewayCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Ekte byggutdata (`build-final.log`):

```text
Build complete! (36.64s)
```

Ekte XCTest-utdata (`provider-final.log`):

```text
Test Suite 'Selected tests' started at 2026-09-08 23:08:38.028.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-08 23:08:38.029.
Test Suite 'AIGatewayProviderToolsOffTests' started at 2026-09-08 23:08:38.029.
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testAnthropicMessagesToolsOff]' started.
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testAnthropicMessagesToolsOff]' passed (0.019 seconds).
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testBodyHashIsCanonicalAndRecursiveScannerIgnoresText]' started.
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testBodyHashIsCanonicalAndRecursiveScannerIgnoresText]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testLocalGemmaSharedProductionAdapterToolsOff]' started.
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testLocalGemmaSharedProductionAdapterToolsOff]' passed (0.009 seconds).
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testLocalLLMSharedProductionAdapterToolsOff]' started.
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testLocalLLMSharedProductionAdapterToolsOff]' passed (0.009 seconds).
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testMistralChatCompletionsToolsOff]' started.
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testMistralChatCompletionsToolsOff]' passed (0.009 seconds).
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testOpenAIChatCompletionsToolsOff]' started.
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testOpenAIChatCompletionsToolsOff]' passed (0.009 seconds).
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testOpenAICompatibleChatCompletionsToolsOff]' started.
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testOpenAICompatibleChatCompletionsToolsOff]' passed (0.008 seconds).
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testOpenAICompatibleResponsesToolsOff]' started.
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testOpenAICompatibleResponsesToolsOff]' passed (0.008 seconds).
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testOpenAIResponsesToolsOff]' started.
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testOpenAIResponsesToolsOff]' passed (0.007 seconds).
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testTypedInvokeHashBindsToolPolicyAndEveryRequestedTool]' started.
Test Case '-[AppTests.AIGatewayProviderToolsOffTests testTypedInvokeHashBindsToolPolicyAndEveryRequestedTool]' passed (0.002 seconds).
Test Suite 'AIGatewayProviderToolsOffTests' passed at 2026-09-08 23:08:38.111.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.080 (0.081) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-08 23:08:38.111.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.080 (0.081) seconds
Test Suite 'Selected tests' passed at 2026-09-08 23:08:38.111.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.080 (0.083) seconds
```

Ekte XCTest-utdata (`cell-final.log`):

```text
Test Suite 'Selected tests' started at 2026-09-08 23:08:47.925.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-08 23:08:47.926.
Test Suite 'AgentTrustPackageCellTests' started at 2026-09-08 23:08:47.926.
Test Case '-[AppTests.AgentTrustPackageCellTests testCanonicalPackageAndTwoRegenerationsHaveSameDigestAndEmitEvidence]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testCanonicalPackageAndTwoRegenerationsHaveSameDigestAndEmitEvidence]' passed (0.051 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testChangingOneTemplateGrantChangesDigest]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testChangingOneTemplateGrantChangesDigest]' passed (0.020 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testClaimedVerifiedEntityRecordWithoutCryptographicReceiptIsExcluded]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testClaimedVerifiedEntityRecordWithoutCryptographicReceiptIsExcluded]' passed (0.016 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testConfigurationPreservesApprovedSkeletonAndNestedStateBindings]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testConfigurationPreservesApprovedSkeletonAndNestedStateBindings]' passed (0.009 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testDeferredOperationsReturnExplicitNotImplementedWithoutChangingDigest]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testDeferredOperationsReturnExplicitNotImplementedWithoutChangingDigest]' passed (0.021 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testEveryGatewayAgentProjectsToolsOffInPackageAndRuntimeState]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testEveryGatewayAgentProjectsToolsOffInPackageAndRuntimeState]' passed (0.035 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testFixtureFleetProjectsActualTemplatesAndHonestMissingSources]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testFixtureFleetProjectsActualTemplatesAndHonestMissingSources]' passed (0.014 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testInvalidEndpointAndMissingResolverDoNotProduceDerivedEvidence]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testInvalidEndpointAndMissingResolverDoNotProduceDerivedEvidence]' passed (0.014 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testPersistedSelectionRequiresFreshSourceReadAndRetainsDigest]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testPersistedSelectionRequiresFreshSourceReadAndRetainsDigest]' passed (0.024 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testProviderToolsDeviationChangesDigestAndWarnsThroughRuntimeStatusProjection]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testProviderToolsDeviationChangesDigestAndWarnsThroughRuntimeStatusProjection]' passed (0.019 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testReadableDraftRouteAndInstructionAreProjectedWithoutPromptOrCredentials]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testReadableDraftRouteAndInstructionAreProjectedWithoutPromptOrCredentials]' passed (0.042 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testStrictExploreContractsMatchNormativeKeysAndGrants]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testStrictExploreContractsMatchNormativeKeysAndGrants]' passed (0.006 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownKeypathsAndWrongMethodsFailClosed]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownKeypathsAndWrongMethodsFailClosed]' passed (0.003 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownPurposeCannotAuthorizeOrAlterFleet]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testUnknownPurposeCannotAuthorizeOrAlterFleet]' passed (0.020 seconds).
Test Case '-[AppTests.AgentTrustPackageCellTests testWrongRequesterCannotReadWriteOrUseDeferredActions]' started.
Test Case '-[AppTests.AgentTrustPackageCellTests testWrongRequesterCannotReadWriteOrUseDeferredActions]' passed (0.016 seconds).
Test Suite 'AgentTrustPackageCellTests' passed at 2026-09-08 23:08:48.237.
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.309 (0.310) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-08 23:08:48.237.
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.309 (0.311) seconds
Test Suite 'Selected tests' passed at 2026-09-08 23:08:48.237.
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.309 (0.311) seconds
```

Ekte XCTest-utdata (`reach-final.log`):

```text
Test Suite 'Selected tests' started at 2026-09-08 23:08:48.333.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-08 23:08:48.334.
Test Suite 'AgentTrustPackageReachTests' started at 2026-09-08 23:08:48.334.
Test Case '-[AppTests.AgentTrustPackageReachTests testConfigurationReferencesRequireKnownKeypathTemplateAndRuntimeAdmission]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testConfigurationReferencesRequireKnownKeypathTemplateAndRuntimeAdmission]' passed (0.009 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testCredentialGrantChangesReachAndDigestWithoutResolvingAnyCredential]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testCredentialGrantChangesReachAndDigestWithoutResolvingAnyCredential]' passed (0.013 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testCredentialMetadataWriteAndUnreachableGrantsNeverSetCredentialFlag]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testCredentialMetadataWriteAndUnreachableGrantsNeverSetCredentialFlag]' passed (0.011 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testCycleAToBToATerminatesWithoutRepeatedCellsInPaths]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testCycleAToBToATerminatesWithoutRepeatedCellsInPaths]' passed (0.001 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testDepthFourAndMinimumCommonPermissionsOnTransitivePaths]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testDepthFourAndMinimumCommonPermissionsOnTransitivePaths]' passed (0.001 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testEmptyHostPatternsMeanNoDestinationsEvenWithOtherCeilingDestinations]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testEmptyHostPatternsMeanNoDestinationsEvenWithOtherCeilingDestinations]' passed (0.002 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testEveryEdgeHasContractGrantAndExactTargetTemplateAndFabricationsAreRejected]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testEveryEdgeHasContractGrantAndExactTargetTemplateAndFabricationsAreRejected]' passed (0.001 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testExpiredUnverifiedWrongSubjectMalformedAndAmbiguousContractsFailClosed]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testExpiredUnverifiedWrongSubjectMalformedAndAmbiguousContractsFailClosed]' passed (0.002 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testFixtureFleetMatchesThreeReachRowsSemantically]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testFixtureFleetMatchesThreeReachRowsSemantically]' passed (0.005 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testInitialReadsAssignmentsAndNestedSubscriptionsYieldOnlyTemplateCandidates]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testInitialReadsAssignmentsAndNestedSubscriptionsYieldOnlyTemplateCandidates]' passed (0.000 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testRuntimeConfigurationEdgeUpdatesPackageDigestAndState]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testRuntimeConfigurationEdgeUpdatesPackageDigestAndState]' passed (0.040 seconds).
Test Case '-[AppTests.AgentTrustPackageReachTests testTransitiveCredentialsAreScopedPerAgentAndParallelPermissionsUseIntersection]' started.
Test Case '-[AppTests.AgentTrustPackageReachTests testTransitiveCredentialsAreScopedPerAgentAndParallelPermissionsUseIntersection]' passed (0.001 seconds).
Test Suite 'AgentTrustPackageReachTests' passed at 2026-09-08 23:08:48.421.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.086 (0.086) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-08 23:08:48.421.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.086 (0.086) seconds
Test Suite 'Selected tests' passed at 2026-09-08 23:08:48.421.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.086 (0.087) seconds
```

Ekte XCTest-utdata (`local-final.log`):

```text
Test Suite 'Selected tests' started at 2026-09-08 23:08:48.517.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-08 23:08:48.518.
Test Suite 'LocalLLMGatewayCellTests' started at 2026-09-08 23:08:48.518.
Test Case '-[AppTests.LocalLLMGatewayCellTests testContextPreviewBudgetsRedactsAndAuditsContextPack]' started.
Test Case '-[AppTests.LocalLLMGatewayCellTests testContextPreviewBudgetsRedactsAndAuditsContextPack]' passed (0.010 seconds).
Test Case '-[AppTests.LocalLLMGatewayCellTests testGenerateUsesLocalRouteWithoutSecretAndCachesEquivalentCalls]' started.
Test Case '-[AppTests.LocalLLMGatewayCellTests testGenerateUsesLocalRouteWithoutSecretAndCachesEquivalentCalls]' passed (0.004 seconds).
Test Case '-[AppTests.LocalLLMGatewayCellTests testHealthCallsLocalBackendAndReportsHealthy]' started.
Test Case '-[AppTests.LocalLLMGatewayCellTests testHealthCallsLocalBackendAndReportsHealthy]' passed (0.002 seconds).
Test Case '-[AppTests.LocalLLMGatewayCellTests testRealLocalBackendSmokeWhenEnabled]' started.
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/LocalLLMGatewayCellTests.swift:209: -[AppTests.LocalLLMGatewayCellTests testRealLocalBackendSmokeWhenEnabled] : Test skipped - Set LOCAL_LLM_REAL_BACKEND_SMOKE=1 to run against a live llama-server.
Test Case '-[AppTests.LocalLLMGatewayCellTests testRealLocalBackendSmokeWhenEnabled]' skipped (0.002 seconds).
Test Suite 'LocalLLMGatewayCellTests' passed at 2026-09-08 23:08:48.536.
	 Executed 4 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.018 (0.018) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-08 23:08:48.536.
	 Executed 4 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.018 (0.018) seconds
Test Suite 'Selected tests' passed at 2026-09-08 23:08:48.536.
	 Executed 4 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.018 (0.019) seconds
```

Ekte XCTest-utdata (`gateway-final.log`):

```text
Test Suite 'Selected tests' started at 2026-09-08 23:09:47.765.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-08 23:09:47.766.
Test Suite 'AIGatewayCellTests' started at 2026-09-08 23:09:47.766.
Test Case '-[AppTests.AIGatewayCellTests testAccountingJournalPersistsAcrossEncodingAndExcludesPromptAndOutput]' started.
Test Case '-[AppTests.AIGatewayCellTests testAccountingJournalPersistsAcrossEncodingAndExcludesPromptAndOutput]' passed (0.008 seconds).
Test Case '-[AppTests.AIGatewayCellTests testAgreementPricingPolicyAppliesMarkupToPreflightQuotaDefault]' started.
Test Case '-[AppTests.AIGatewayCellTests testAgreementPricingPolicyAppliesMarkupToPreflightQuotaDefault]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayCellTests testAnthropicMessagesProviderBuildsNativeRequestAndParsesUsage]' started.
Test Case '-[AppTests.AIGatewayCellTests testAnthropicMessagesProviderBuildsNativeRequestAndParsesUsage]' passed (0.004 seconds).
Test Case '-[AppTests.AIGatewayCellTests testCacheKeyStableAcrossEquivalentRequests]' started.
Test Case '-[AppTests.AIGatewayCellTests testCacheKeyStableAcrossEquivalentRequests]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayCellTests testConcreteProviderEgressPolicyRunsBeforeSecretLookup]' started.
Test Case '-[AppTests.AIGatewayCellTests testConcreteProviderEgressPolicyRunsBeforeSecretLookup]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testDecodedGatewayIsImmediatelyReadyIdempotentAndRejectsUnprovedRequesters]' started.
Test Case '-[AppTests.AIGatewayCellTests testDecodedGatewayIsImmediatelyReadyIdempotentAndRejectsUnprovedRequesters]' passed (0.009 seconds).
Test Case '-[AppTests.AIGatewayCellTests testEgressPolicyAllowsOnlyCanonicalRemoteAndTrustedLocalRoutes]' started.
Test Case '-[AppTests.AIGatewayCellTests testEgressPolicyAllowsOnlyCanonicalRemoteAndTrustedLocalRoutes]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayCellTests testEgressPolicyRejectsCallerSuppliedEndpointAuthorityAndTransportMismatches]' started.
Test Case '-[AppTests.AIGatewayCellTests testEgressPolicyRejectsCallerSuppliedEndpointAuthorityAndTransportMismatches]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayCellTests testEnvironmentSecretStoreResolvesVendorDefaultAliases]' started.
Test Case '-[AppTests.AIGatewayCellTests testEnvironmentSecretStoreResolvesVendorDefaultAliases]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayCellTests testExactPostUsageSettlementAdjustsBelowPreflightReservation]' started.
Test Case '-[AppTests.AIGatewayCellTests testExactPostUsageSettlementAdjustsBelowPreflightReservation]' passed (0.003 seconds).
Test Case '-[AppTests.AIGatewayCellTests testFailureRedactsSecretAndRollsBackQuota]' started.
Test Case '-[AppTests.AIGatewayCellTests testFailureRedactsSecretAndRollsBackQuota]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testGatewayAuthoritySurfacesCanonicalizePersistedTemplates]' started.
Test Case '-[AppTests.AIGatewayCellTests testGatewayAuthoritySurfacesCanonicalizePersistedTemplates]' passed (0.003 seconds).
Test Case '-[AppTests.AIGatewayCellTests testGatewayOverheadBelowBudgetWithStubProvider]' started.
Test Case '-[AppTests.AIGatewayCellTests testGatewayOverheadBelowBudgetWithStubProvider]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testInvokeDraftCarriesLocalTimeoutToProviderRoute]' started.
Test Case '-[AppTests.AIGatewayCellTests testInvokeDraftCarriesLocalTimeoutToProviderRoute]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testInvokeDraftFallsBackToEnvironmentConfiguredRoutes]' started.
Test Case '-[AppTests.AIGatewayCellTests testInvokeDraftFallsBackToEnvironmentConfiguredRoutes]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testInvokeDraftUsesSessionCredentialAndUpdatesSetupState]' started.
Test Case '-[AppTests.AIGatewayCellTests testInvokeDraftUsesSessionCredentialAndUpdatesSetupState]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testInvokeFailoverUsesSecondRouteAndCommitsQuotaOnce]' started.
Test Case '-[AppTests.AIGatewayCellTests testInvokeFailoverUsesSecondRouteAndCommitsQuotaOnce]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testInvokeUsesCacheAndSkipsSecondQuotaCharge]' started.
Test Case '-[AppTests.AIGatewayCellTests testInvokeUsesOwnerScopedCredentialCellSecret]' started.
Test Case '-[AppTests.AIGatewayCellTests testInvokeUsesOwnerScopedCredentialCellSecret]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testLegacyGatewayCannotSelectPurposeAuthoritySurface]' started.
Test Case '-[AppTests.AIGatewayCellTests testLegacyGatewayCannotSelectPurposeAuthoritySurface]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testMakeDefaultUsesConfiguredRouteOrderFromEnvironment]' started.
Test Case '-[AppTests.AIGatewayCellTests testMakeDefaultUsesConfiguredRouteOrderFromEnvironment]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayCellTests testMultiTurnPlannerExecutorLoopAggregatesUsageAndHistory]' started.
Test Case '-[AppTests.AIGatewayCellTests testMultiTurnPlannerExecutorLoopAggregatesUsageAndHistory]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testNoRedirectDelegateRejectsRedirectRequest]' started.
Test Case '-[AppTests.AIGatewayCellTests testNoRedirectDelegateRejectsRedirectRequest]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayCellTests testOpenAICompatibleProviderBuildsDeterministicBody]' started.
Test Case '-[AppTests.AIGatewayCellTests testOpenAICompatibleProviderBuildsDeterministicBody]' passed (0.001 seconds).
Test Case '-[AppTests.AIGatewayCellTests testOpenAIResponsesProviderBuildsRecommendedRequestShape]' started.
Test Case '-[AppTests.AIGatewayCellTests testOpenAIResponsesProviderBuildsRecommendedRequestShape]' passed (0.001 seconds).
Test Case '-[AppTests.AIGatewayCellTests testPaidAIUsageCanaryBuildsAgreementBackedQuotaRequest]' started.
Test Case '-[AppTests.AIGatewayCellTests testPaidAIUsageCanaryBuildsAgreementBackedQuotaRequest]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayCellTests testPaidAIUsageCanaryInvokesModelAndSettlesUsageQuotaWithMarkup]' started.
Test Case '-[AppTests.AIGatewayCellTests testPaidAIUsageCanaryInvokesModelAndSettlesUsageQuotaWithMarkup]' passed (0.003 seconds).
Test Case '-[AppTests.AIGatewayCellTests testParallelFanOutRunsAllRoutesAndSettlesActualAggregateUsage]' started.
Test Case '-[AppTests.AIGatewayCellTests testParallelFanOutRunsAllRoutesAndSettlesActualAggregateUsage]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testPerAgentToolPolicyDeniesUndeclaredToolsBeforeProviderCall]' started.
Test Case '-[AppTests.AIGatewayCellTests testPerAgentToolPolicyDeniesUndeclaredToolsBeforeProviderCall]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testProductionSkeletonPayloadsAndRuntimeResultsMatchExploreContracts]' started.
Test Case '-[AppTests.AIGatewayCellTests testProductionSkeletonPayloadsAndRuntimeResultsMatchExploreContracts]' passed (0.012 seconds).
Test Case '-[AppTests.AIGatewayCellTests testProviderProfilesCoverHostedAndLocalModelRoutes]' started.
Test Case '-[AppTests.AIGatewayCellTests testProviderProfilesCoverHostedAndLocalModelRoutes]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayCellTests testProviderRejectsResponseURLChangedByRedirect]' started.
Test Case '-[AppTests.AIGatewayCellTests testProviderRejectsResponseURLChangedByRedirect]' passed (0.001 seconds).
Test Case '-[AppTests.AIGatewayCellTests testPurposeBoundCacheDoesNotReuseAnotherDecisionReceipt]' started.
Test Case '-[AppTests.AIGatewayCellTests testPurposeBoundCellHasOneGrantAndRejectsMixedGrantAgreement]' started.
Test Case '-[AppTests.AIGatewayCellTests testPurposeBoundCellHasOneGrantAndRejectsMixedGrantAgreement]' passed (0.004 seconds).
Test Case '-[AppTests.AIGatewayCellTests testPurposeBoundInvocationAuthorizesBeforeCredentialAndReturnsCompletedReceipt]' started.
Test Case '-[AppTests.AIGatewayCellTests testPurposeBoundInvocationAuthorizesBeforeCredentialAndReturnsCompletedReceipt]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testPurposeBoundPayloadDriftIsDeniedBeforeCredentialLookup]' started.
Test Case '-[AppTests.AIGatewayCellTests testPurposeBoundPayloadDriftIsDeniedBeforeCredentialLookup]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testPurposeBoundTrustEvidenceCannotAuthorizeOutsider]' started.
Test Case '-[AppTests.AIGatewayCellTests testPurposeBoundTrustEvidenceCannotAuthorizeOutsider]' passed (0.003 seconds).
Test Case '-[AppTests.AIGatewayCellTests testPurposeBoundV1RejectsMultiEffectRequestBeforeCredentialLookup]' started.
Test Case '-[AppTests.AIGatewayCellTests testPurposeBoundV1RejectsMultiEffectRequestBeforeCredentialLookup]' passed (0.001 seconds).
Test Case '-[AppTests.AIGatewayCellTests testQuotaExceededUpdatesQuotaStatusAndSetupState]' started.
Test Case '-[AppTests.AIGatewayCellTests testQuotaExceededUpdatesQuotaStatusAndSetupState]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testRequesterCannotUseAnotherIdentityScopedCredential]' started.
Test Case '-[AppTests.AIGatewayCellTests testRequesterCannotUseAnotherIdentityScopedCredential]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testRequesterScopedLookupCanUseLegacyEnvironmentFallbackWhenExplicitlyAllowed]' started.
Test Case '-[AppTests.AIGatewayCellTests testRequesterScopedLookupCanUseLegacyEnvironmentFallbackWhenExplicitlyAllowed]' passed (0.006 seconds).
Test Case '-[AppTests.AIGatewayCellTests testRequesterScopedLookupDoesNotUseLegacyEnvironmentFallbackByDefault]' started.
Test Case '-[AppTests.AIGatewayCellTests testSettlementFailureFailsClosedAfterProviderSuccess]' started.
Test Case '-[AppTests.AIGatewayCellTests testSettlementFailureFailsClosedAfterProviderSuccess]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testSwarmAppliesAgentRolesAndUsesAdjudicatorOutput]' started.
Test Case '-[AppTests.AIGatewayCellTests testSwarmAppliesAgentRolesAndUsesAdjudicatorOutput]' passed (0.002 seconds).
Test Case '-[AppTests.AIGatewayCellTests testValidatorAllowsCanonicalTrustedLocalLoopbackRoute]' started.
Test Case '-[AppTests.AIGatewayCellTests testValidatorAllowsCanonicalTrustedLocalLoopbackRoute]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayCellTests testValidatorAllowsManyModelInstanceRoutesWithinProductionLimit]' started.
Test Case '-[AppTests.AIGatewayCellTests testValidatorAllowsManyModelInstanceRoutesWithinProductionLimit]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayCellTests testValidatorRejectsPrivateEndpointBeforeProviderInvocation]' started.
Test Case '-[AppTests.AIGatewayCellTests testValidatorRejectsPrivateEndpointBeforeProviderInvocation]' passed (0.000 seconds).
Test Case '-[AppTests.AIGatewayCellTests testVotingSelectsNormalizedMajorityDeterministically]' started.
Test Case '-[AppTests.AIGatewayCellTests testVotingSelectsNormalizedMajorityDeterministically]' passed (0.002 seconds).
Test Suite 'AIGatewayCellTests' passed at 2026-09-08 23:09:47.877.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.109 (0.111) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-08 23:09:47.877.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.109 (0.111) seconds
Test Suite 'Selected tests' passed at 2026-09-08 23:09:47.877.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.109 (0.112) seconds
```

Full XCTest-bundle er **ikke kjørt og ikke påkrevd i WP4**. Ingen konklusjon om hele bundlens eksisterende røde tester trekkes fra de valgte klassene. Direkte xctest dekker ikke Swift Testing-mål. Tilleggsregresjonen for LocalLLMGateway rapporterer 4 tester, hvorav 1 eksisterende opt-in live-backend-smoke er hoppet over (`LOCAL_LLM_REAL_BACKEND_SMOKE` er ikke slått på), 0 feil. Ingen live lokal modell eller leverandør er startet. Bygget har eksisterende SwiftPM-/kildeadvarsler, men ingen byggefeil. Ekte `Executed`-linjer er bevart over; øvrige logger ligger i `/private/tmp/wp4-provider-tools/`.

## WP4 — sluttmelding

WP4 — leverandørverktøy av er **levert** for `purpose://candidate.tillitspakke-agentflaate.leverandorverktoy`.

Levert: `CellScaffold/Tests/AppTests/AIGatewayProviderToolsOffTests.swift`, felles kanonisk hashing i `AIGatewaySupport.swift`, providerTools-projeksjon/labels/avviksvarsel i `AgentTrustPackageCell.swift`, og to nye tester i `AgentTrustPackageCellTests.swift`. Provider-adapterne er uendret: produksjonens ferdige HTTP-bodyer inneholder ingen av verktøyfeltene. 8 rute-/formatkombinasjoner × 4 toolPolicy-varianter er testet. Pakken binder `off` i digesten; endring til `n/a` endrer digest og gir varsel gjennom runtime-statusfunksjonen. Hashgrensen mellom normalisert invoke-request og provider-body er dokumentert over; kvitteringsformatet er ikke endret.

Endelig bygg grønt. **10/10 leverandørtester og 15/15 pakketester grønne.** Tilleggsregresjon: 12/12 rekkeviddetester og 48/48 AIGateway-tester grønne; LocalLLMGateway 4 rapportert / 1 live-smoke hoppet over / 0 feil. Full bundle er ikke påkrevd i WP4 og er ikke kjørt; Swift Testing og live leverandøratferd er ikke dekket.

`STATUS.md` har én WP4-linje. Kun WP4 er utført; ingen git-kommandoer. Formål og pakke gir ingen rettigheter.

## WebFetch-ceiling <a id="webfetch"></a>

purposeRef: `purpose://candidate.tillitspakke-agentflaate.webfetch-ceiling`. Kun WP5.

### WP5 — baseline før endring

Bygg og XCTest kjørt etter handoff regel 9–10. Ny WebFetchCeilingTests finnes ikke før endringen.

```text
$ cd CellScaffold
$ swift build --disable-sandbox --build-tests
Build complete! (24.13s)
$ xcrun --sdk macosx xctest -XCTest AppTests.WebKnowledgeCellsTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.054 (0.055) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.054 (0.055) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.054 (0.055) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.658 (0.660) seconds
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.658 (0.660) seconds
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.658 (0.661) seconds
```

Fullbundlens sammenligningsgrunnlag er WP0c: 2046 tester, 46 røde testnavn (148 assertion-feil, 9 unexpected), 11 hoppet over; rålogg `/private/tmp/wp0c-baseline-ujg4x43v/CellScaffold-xctest.log`. Nye målrettede baseline-kjøringer over: 8 WebKnowledge + 15 AgentTrustPackage, 0 feil.

### WP5 — implementasjon og avgrensning

- `WebKnowledgeCells.swift`: `WebFetchCeiling: Codable` (`haven.webfetch-ceiling.v0`) lagres i cellens eksisterende Codable-snapshot, separat per instans. `webFetch.ceiling` er GET `r---`; `webFetch.ceiling.set` er SET `rw--` med eksplisitt eierbevis. De eksisterende `.identityUnique` / `.persistant`-registreringene i `configure.swift` gjenbrukes. SET ber resolveren om `persistCellSnapshot`; responsen oppgir `persisted`, og en uhostet/ephemeral celle lover ikke en lagring den ikke har. Ingen ny EntityAnchor-database eller runtime-persistensmekanisme innføres.
- Ceiling leses for hver fetch. Manglende/udekodbar data feiler lukket; ukjent schema/felt, ugyldige mønstre, metodeutvidelse, credentials, redirect-aktivering og ugyldig bytegrense godtas ikke. Maksimum er 256000 bytes, og eieren kan sette en lavere positiv grense.
- Etter ceiling-kontrollen håndheves scheme → metode/body → host/port → credentials. Payload-flagget `allowInsecureHTTP` åpner ikke HTTP. `followRedirects` og `maxBytes` i request endrer ikke cellens ceiling. Bare et nytt, eksplisitt `webFetch.ceiling.set` fra eieren kan endre dataene. Ukjente request-felt avvises. URL-userinfo og header-payload avvises også som credentials.
- v0 tillater bare `allowCredentials=false`; ingen gyldig v0-ceiling kan åpne et credential-oppslag. Den gamle direkte `ScopedCredentialRegistry.secret`-banen i fetch er fjernet. Testene fyller session-butikken gjennom `ScopedCredentialCell` og teller faktiske `secret`-lesinger, med et positivt kontrolloppslag som viser at telleren virker. En delegert fetch-Grant gir ingen credential-rett. Ingen live hemmelighetslager eller `.env` leses av disse testene.
- Ephemeral `URLSession` med injiserbare URL-protokoller, egen serialisert delegate, ingen cookie-/credential-/URL-cache. Alle redirects stoppes; cellen sjekker 3xx/Location selv. En tillatt redirect returnerer `redirect_not_followed`, uten ny request. Utenfor whitelist, ugyldig eller manglende Location gir `denied` / `redirect_outside_whitelist`. Bufferen begrenses under mottak, og transfer kanselleres ved `maxBytes`; `byteCount` er antall beholdte bytes og `limitReached` sier at mottaket traff grensen. Dette er ikke en garanti om eksakt antall bytes på nettverksledningen: en allerede levert transportchunk kan være større enn den beholdte bufferen.
- Typed avvisninger har `status=denied`, enum-basert `reason` og eventuelt vert; ingen URL-path, query, userinfo, Location-innhold eller rå nettverksfeil returneres. `code` er en kompatibilitetskopi av reason.
- `AgentTrustPackageCell` leser den faktiske GET-kilden, projiserer `hostPatterns` i pakken og viser «Ceiling: kun GET · https · whitelist: … · credentials: NEI». Manglende ceiling vises som «Ceiling mangler — alle fetch nektes». Hostendring endrer pakke-digest. Ingen WP6-/WP7-handlere implementert.

Apple-kilder kontrollert for transportimplementasjonen: [redirect-delegaten](https://developer.apple.com/documentation/foundation/urlsessiontaskdelegate/urlsession(_:task:willperformhttpredirection:newrequest:completionhandler:)) beskriver `nil` som avslag på redirect i ephemeral/default sessions; [URLSessionDataDelegate](https://developer.apple.com/documentation/foundation/urlsessiondatadelegate) beskriver løpende datamottak, og [session-konfigurasjonen](https://developer.apple.com/documentation/foundation/urlsessionconfiguration) cookie-/credential-butikker.

**Eksisterende tester oppdatert:** `WebKnowledgeCellsTests.testWebFetchBlocksInsecureHTTPByDefault` setter nå eksplisitt ceiling for `example.com` før scheme-asserten. Testens `https_required`-assert er beholdt. WP2s forventning om «ingen whitelist ennå (WP5)» er erstattet med den implementerte, lukkede mangler-tilstanden. Ingen eksisterende test er fjernet eller svekket.

### WP5 — første målrettede kjøring og retting

Første kompilering krevde retting av flow-innholdstype og en navnekollisjon med den globale `error`-hjelperen. En fixture-identitet manglet initializer-argumenter. Disse byggefeilene er rettet. Første kjørbare testklasse avdekket dessuten at `GeneralCell.requesterProvesOwnership` godtar et offentlig eier-snapshot under `debugValidateAccessForEverything=true`. WP5 styrker bare denne cellens ceiling-SET med eksisterende `IdentitySigningChallenge`, signering og verifikasjon mot lagret eiernøkkel; den endrer ikke kjernens autorisasjonsmotor. Testen er beholdt og utvidet med kopiert offentlig nøkkel koblet til feil vault.

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/WebFetchCeilingTests.swift:221: error: -[AppTests.WebFetchCeilingTests testOnlyProvenOwnerCanSetCeilingEvenUnderDebugBypass] : XCTAssertEqual failed: ("Optional(CellBase.ValueType.string("ceiling_set"))") is not equal to ("Optional(CellBase.ValueType.string("denied"))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/WebFetchCeilingTests.swift:221: error: -[AppTests.WebFetchCeilingTests testOnlyProvenOwnerCanSetCeilingEvenUnderDebugBypass] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.string("owner_required"))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/WebFetchCeilingTests.swift:221: error: -[AppTests.WebFetchCeilingTests testOnlyProvenOwnerCanSetCeilingEvenUnderDebugBypass] : XCTAssertEqual failed: ("Optional(CellBase.ValueType.bool(true))") is not equal to ("Optional(CellBase.ValueType.bool(false))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/WebFetchCeilingTests.swift:221: error: -[AppTests.WebFetchCeilingTests testOnlyProvenOwnerCanSetCeilingEvenUnderDebugBypass] : XCTAssertTrue failed
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/WebFetchCeilingTests.swift:226: error: -[AppTests.WebFetchCeilingTests testOnlyProvenOwnerCanSetCeilingEvenUnderDebugBypass] : XCTAssertEqual failed: ("Optional(["evil.com"])") is not equal to ("Optional(["*.example.org", "docs.claude.com"])")
	 Executed 17 tests, with 5 failures (0 unexpected) in 1.616 (1.617) seconds
	 Executed 17 tests, with 5 failures (0 unexpected) in 1.616 (1.617) seconds
	 Executed 17 tests, with 5 failures (0 unexpected) in 1.616 (1.617) seconds
```

Andre målrettede kjøring: den nye testen for «feil vault» brukte testhjelperens delte standard-vault, som faktisk inneholdt eierens nøkkel. Signaturkontrollen godtok derfor et gyldig eierbevis. Fixturen er rettet til en separat `EphemeralIdentityVault`; avvisningsassertene er uendret. Den første snapshot/debug-feilen er rettet i produksjonskoden.

```text
	 Executed 17 tests, with 9 failures (0 unexpected) in 1.296 (1.297) seconds
	 Executed 17 tests, with 9 failures (0 unexpected) in 1.296 (1.297) seconds
	 Executed 17 tests, with 9 failures (0 unexpected) in 1.296 (1.298) seconds
```

### WP5 — endelig bygg og målrettet verifikasjon

Et forsøk på å samle tilleggsregresjonen med Python `subprocess` valgte x86_64-laster og feilet med `incompatible architecture` (exit 80, ingen tester kjørt). Det er en kjøringsfeil; alle klassene nedenfor er deretter kjørt direkte med `xcrun` etter regel 10. Ingen `arch`-prefiks, ingen `swift test`.

```text
$ cd CellScaffold
$ swift build --disable-sandbox --build-tests
Build complete! (8.47s)
$ xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
Test Case '-[AppTests.WebFetchCeilingTests test302OutsideWhitelistNeverMakesSecondRequestAndRedactsLocation]' started.
Test Case '-[AppTests.WebFetchCeilingTests test302OutsideWhitelistNeverMakesSecondRequestAndRedactsLocation]' passed (0.016 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testAdmittedNonOwnerCannotBypassCeilingOrResolveCredential]' started.
Test Case '-[AppTests.WebFetchCeilingTests testAdmittedNonOwnerCannotBypassCeilingOrResolveCredential]' passed (0.010 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testAllElevenNormativeWhitelistFixtureRowsThroughCell]' started.
Test Case '-[AppTests.WebFetchCeilingTests testAllElevenNormativeWhitelistFixtureRowsThroughCell]' passed (0.009 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testAllowedFetchHasNoCredentialsBodyOrCookiesAndHonoursMaxBytes]' started.
Test Case '-[AppTests.WebFetchCeilingTests testAllowedFetchHasNoCredentialsBodyOrCookiesAndHonoursMaxBytes]' passed (0.003 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testAllowedSmallFetchPreservesContentAndLastFetch]' started.
Test Case '-[AppTests.WebFetchCeilingTests testAllowedSmallFetchPreservesContentAndLastFetch]' passed (0.003 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testCaseInsensitiveHostExactWildcardAndExplicitPort]' started.
Test Case '-[AppTests.WebFetchCeilingTests testCaseInsensitiveHostExactWildcardAndExplicitPort]' passed (0.006 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testCeilingExplorePermissionsAndOwnerMutationFlow]' started.
Test Case '-[AppTests.WebFetchCeilingTests testCeilingExplorePermissionsAndOwnerMutationFlow]' passed (0.002 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testCeilingIsPerInstanceAndRereadOnEveryFetch]' started.
Test Case '-[AppTests.WebFetchCeilingTests testCeilingIsPerInstanceAndRereadOnEveryFetch]' passed (0.004 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testCeilingPersistsThroughResolverSnapshotAndReload]' started.
Test Case '-[AppTests.WebFetchCeilingTests testCeilingPersistsThroughResolverSnapshotAndReload]' passed (0.010 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testCredentialAliasDeniedBeforeFixtureStoreLookupEvenForOwner]' started.
Test Case '-[AppTests.WebFetchCeilingTests testCredentialAliasDeniedBeforeFixtureStoreLookupEvenForOwner]' passed (0.006 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testEmptyCeilingDeniesAll]' started.
Test Case '-[AppTests.WebFetchCeilingTests testEmptyCeilingDeniesAll]' passed (0.002 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testEvery3xxIsCheckedAndEvenAllowedRedirectIsNotFollowed]' started.
Test Case '-[AppTests.WebFetchCeilingTests testEvery3xxIsCheckedAndEvenAllowedRedirectIsNotFollowed]' passed (0.022 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testInvalidPatternsAndWiderOrUnknownCeilingsNeverReplaceStoredData]' started.
Test Case '-[AppTests.WebFetchCeilingTests testInvalidPatternsAndWiderOrUnknownCeilingsNeverReplaceStoredData]' passed (0.013 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testLegacyAndCorruptedPersistenceFailClosed]' started.
Test Case '-[AppTests.WebFetchCeilingTests testLegacyAndCorruptedPersistenceFailClosed]' passed (0.004 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testMissingCeilingDeniesAllWithoutRequests]' started.
Test Case '-[AppTests.WebFetchCeilingTests testMissingCeilingDeniesAllWithoutRequests]' passed (0.002 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testOnlyProvenOwnerCanSetCeilingEvenUnderDebugBypass]' started.
Test Case '-[AppTests.WebFetchCeilingTests testOnlyProvenOwnerCanSetCeilingEvenUnderDebugBypass]' passed (0.003 seconds).
Test Case '-[AppTests.WebFetchCeilingTests testValidationOrderAndPayloadCannotOpenHTTPWritesOrCredentials]' started.
Test Case '-[AppTests.WebFetchCeilingTests testValidationOrderAndPayloadCannotOpenHTTPWritesOrCredentials]' passed (0.005 seconds).
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.121 (0.122) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.121 (0.122) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.121 (0.123) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.282 (0.283) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.282 (0.283) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.282 (0.283) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.WebKnowledgeCellsTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.044 (0.044) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.044 (0.044) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.044 (0.045) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageReachTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.069 (0.069) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.069 (0.069) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.069 (0.070) seconds
```

Målrettet resultat: **17 + 16 + 8 + 12 = 53 tester, 0 feil**. WebFetch-klassen inkluderer alle 11 normative fixture-rader, faktiske URL-protokoll-requesttellere, redirect-delegate-callback, hele 3xx-intervallets representative statuser, port/case/wildcard, manglende/tom/korrupt ceiling, ekte delegert Contract, credential-butikkteller, eierbevis uten debug-bypass, isolerte instanser, ny ceiling ved neste fetch, begrenset mottak, vedvarende snapshot og flow. Pakke-testen bruker produksjonens resolver/GET-kilde og sjekker label, hostPatterns og endret digest.

Explore-audit:

```text
$ python3 CellProtocolDocuments/Tools/Explore/explore_contract_audit.py --repo-root CellProtocol
{
  "completeContracts": 305,
  "errors": 7,
  "handlerOperations": 316,
  "warnings": 19
}
$ python3 CellProtocolDocuments/Tools/Explore/explore_contract_audit.py --repo-root CellScaffold --source-dir Sources/App/Cells/WebKnowledge
{
  "completeContracts": 3,
  "errors": 0,
  "handlerOperations": 43,
  "warnings": 40
}
```

CellProtocol-auditens 7 feil / 19 varsler er samme eksisterende tall som WP2; ingen CellProtocol-kode er endret. WebKnowledge har 3 komplette kontrakter for de endrede/nye operasjonene, 0 feil, 40 varsler om gamle dynamiske/implisitte handlerkontrakter i filens øvrige operasjoner. Exit 0 i auditen uten `--fail-on-error` betyr ikke at de eksisterende CellProtocol-funnene er grønne.

### WP5 — full XCTest-bundle

Fullført med direkte `xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest`, exit 1 på kjente baseline-feil. Rålogg: `/private/tmp/wp5-webfetch/full-bundle.log`. Direkte xctest kjører XCTest, ikke Swift Testing-mål.

**2101 tester, 11 hoppet over, 151 feilrapporter (9 unexpected), 46 røde testnavn — nøyaktig samme 46 som baseline, ingen nye og ingen manglende.** WP5s 17 ceiling-tester og den nye pakkeprojeksjonstesten er grønne også her. Alle 16 pakketester, 8 WebKnowledge-tester og 12 rekkeviddetester er grønne i fullbundlen. 55 flere tester enn WP0c består av tidligere WP2–WP4-tillegg og WP5s 18 nye testtilfeller; eksisterende tester er beholdt.

Fullkjøringens rapporterte tid er **1053.507 s** (17 min 34 s), mot baseline 859.566 s. Den store Porthole-konfigurasjonstesten er grønn, men tok 595.795 s mot 485.182 s. Tidsøkningen er målt; årsaken er ikke isolert i denne slicen. Dette er ingen WP11-paritets-/lastetidsverifikasjon.

Alle `Executed`-linjer fra fullkjøringen følger, med tilhørende suite når den står rett foran:

```text
$ cd CellScaffold
$ xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest

Test Suite 'AIAssistantThreadCellTests' failed at 2026-09-08 23:33:49.614.
	 Executed 14 tests, with 4 tests skipped and 12 failures (0 unexpected) in 1.889 (1.890) seconds
Test Suite 'AIGatewayCellTests' passed at 2026-09-08 23:33:49.799.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.181 (0.185) seconds
Test Suite 'AIGatewayConfigurationFactoryTests' passed at 2026-09-08 23:33:49.800.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'AIGatewayProviderToolsOffTests' passed at 2026-09-08 23:33:49.865.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.064 (0.064) seconds
Test Suite 'AccessRequirementPromptCellTests' passed at 2026-09-08 23:33:50.348.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.483 (0.483) seconds
Test Suite 'AccessSensitiveRuntimeReadinessTests' passed at 2026-09-08 23:33:50.372.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.024 (0.024) seconds
Test Suite 'AdminAccessRequestCellTests' passed at 2026-09-08 23:33:50.404.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.032 (0.032) seconds
Test Suite 'AdminAuthenticatedVaporBridgeTransportTests' passed at 2026-09-08 23:33:50.580.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.175 (0.176) seconds
Test Suite 'AdminBridgeHandshakeAuthenticationTests' passed at 2026-09-08 23:33:50.593.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.012 (0.013) seconds
Test Suite 'AdminCatalogRoutesTests' passed at 2026-09-08 23:33:51.932.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.338 (1.338) seconds
Test Suite 'AdminControlPlaneRoutingTests' passed at 2026-09-08 23:33:51.938.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'AdminCopilotWorkspaceConfigurationTests' passed at 2026-09-08 23:33:53.261.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.323 (1.323) seconds
Test Suite 'AdminCredentialPolicyTests' passed at 2026-09-08 23:33:53.262.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
Test Suite 'AdminCredentialRevocationTests' passed at 2026-09-08 23:33:53.264.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'AdminDeploymentSupervisorCellTests' passed at 2026-09-08 23:33:53.308.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.043 (0.044) seconds
Test Suite 'AdminEntityProofPersistenceSupportTests' passed at 2026-09-08 23:33:53.805.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.497 (0.497) seconds
Test Suite 'AdminFundingCellTests' passed at 2026-09-08 23:33:54.350.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.545 (0.545) seconds
Test Suite 'AdminNodeFleetCellTests' passed at 2026-09-08 23:33:54.553.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.203 (0.203) seconds
Test Suite 'AdminOperationsMetricsTests' passed at 2026-09-08 23:33:54.874.
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.320 (0.321) seconds
Test Suite 'AdminPersistedRuntimeReadinessTests' passed at 2026-09-08 23:33:55.193.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.319 (0.319) seconds
Test Suite 'AdminRoleEnrollmentCellTests' passed at 2026-09-08 23:33:55.202.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'AdminScaffoldBootstrapTests' passed at 2026-09-08 23:33:55.207.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'AdminScaffoldBridgeMultiplexRouteTests' passed at 2026-09-08 23:33:55.211.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'AdminScaffoldRuntimeTests' passed at 2026-09-08 23:33:55.380.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.168 (0.169) seconds
Test Suite 'AdminScaffoldSnapshotIngestTests' passed at 2026-09-08 23:33:55.392.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
Test Suite 'AdminSecurityPolicyCellTests' passed at 2026-09-08 23:33:55.397.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
Test Suite 'AdminWorkspaceConfigurationFactoryTests' passed at 2026-09-08 23:33:55.412.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
Test Suite 'AgeProofDoorCellTests' passed at 2026-09-08 23:33:55.415.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'AgentActionCapabilityCatalogV1Tests' passed at 2026-09-08 23:33:55.641.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.225 (0.226) seconds
Test Suite 'AgentConversationInboxCellTests' passed at 2026-09-08 23:33:55.668.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.027 (0.027) seconds
Test Suite 'AgentTrustPackageCellTests' passed at 2026-09-08 23:33:55.946.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.277 (0.278) seconds
Test Suite 'AgentTrustPackageReachTests' passed at 2026-09-08 23:33:56.007.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.061 (0.061) seconds
Test Suite 'AgreementWorkbenchCellTests' passed at 2026-09-08 23:33:56.209.
	 Executed 21 tests, with 0 failures (0 unexpected) in 0.201 (0.202) seconds
Test Suite 'AgreementWorkbenchConfigurationFactoryTests' passed at 2026-09-08 23:33:56.224.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.014 (0.015) seconds
Test Suite 'AppTests' passed at 2026-09-08 23:33:56.872.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.648 (0.648) seconds
Test Suite 'ArendalsukaConfigurationPublisherAuthorizationRoutesTests' passed at 2026-09-08 23:33:57.125.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.253 (0.253) seconds
Test Suite 'ArendalsukaConfigurationPublisherCellTests' passed at 2026-09-08 23:33:57.887.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.762 (0.762) seconds
Test Suite 'ArendalsukaEventAtlasCellTests' failed at 2026-09-08 23:33:59.232.
	 Executed 40 tests, with 14 failures (0 unexpected) in 1.342 (1.345) seconds
Test Suite 'ArendalsukaImportAuthorizationRoutesTests' failed at 2026-09-08 23:33:59.546.
	 Executed 1 test, with 3 failures (0 unexpected) in 0.314 (0.314) seconds
Test Suite 'ArendalsukaKnowledgeCellTests' passed at 2026-09-08 23:33:59.556.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.009 (0.010) seconds
Test Suite 'ArendalsukaKnowledgeSQLiteStoreTests' passed at 2026-09-08 23:33:59.565.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'ArendalsukaPersistedAtlasRecoveryTests' passed at 2026-09-08 23:34:05.726.
	 Executed 9 tests, with 0 failures (0 unexpected) in 6.159 (6.160) seconds
Test Suite 'ArendalsukaPublicSurfaceRouteTests' passed at 2026-09-08 23:34:05.747.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.021 (0.022) seconds
Test Suite 'ArtistSalesChannelCellTests' passed at 2026-09-08 23:34:05.812.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.064 (0.065) seconds
Test Suite 'AssistantCorrespondenceAdminRoutesTests' passed at 2026-09-08 23:34:06.689.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.877 (0.877) seconds
Test Suite 'AssistantCorrespondenceCellTests' passed at 2026-09-08 23:34:06.841.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.151 (0.152) seconds
Test Suite 'AssistantCorrespondenceOnboardingRoutesTests' passed at 2026-09-08 23:34:07.103.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.261 (0.262) seconds
Test Suite 'AssociatedDomainsRouteTests' passed at 2026-09-08 23:34:07.109.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'BookReferenceRoutesTests' failed at 2026-09-08 23:34:17.987.
	 Executed 6 tests, with 2 failures (0 unexpected) in 10.878 (10.878) seconds
Test Suite 'BrowserClientIdentityOfflineInspectorTests' passed at 2026-09-08 23:34:18.069.
	 Executed 20 tests, with 0 failures (0 unexpected) in 0.081 (0.082) seconds
Test Suite 'BrowserClientIdentityReconciliationTests' passed at 2026-09-08 23:34:18.073.
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.003 (0.004) seconds
Test Suite 'BrowserClientIdentityRecoveryExecutorTests' passed at 2026-09-08 23:34:18.195.
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.121 (0.122) seconds
Test Suite 'BrowserClientIdentityVaultKeyAgreementTests' passed at 2026-09-08 23:34:18.196.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'BrowserClientIdentityVaultTests' passed at 2026-09-08 23:34:18.611.
	 Executed 31 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.413 (0.415) seconds
Test Suite 'ButterpopPilotReadinessTests' passed at 2026-09-08 23:34:18.613.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ButterpopStudioProductTests' failed at 2026-09-08 23:34:23.089.
	 Executed 11 tests, with 18 failures (1 unexpected) in 4.475 (4.476) seconds
Test Suite 'CalendarSurfaceConfigurationTests' passed at 2026-09-08 23:34:23.109.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.020 (0.020) seconds
Test Suite 'CellConfigurationStudioImportTests' passed at 2026-09-08 23:34:23.372.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.263 (0.264) seconds
Test Suite 'CellProtocolIdentityProofTests' passed at 2026-09-08 23:34:23.379.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.006 (0.007) seconds
Test Suite 'CellScaffoldRuntimeIdentityManifestTests' passed at 2026-09-08 23:34:23.571.
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.191 (0.192) seconds
Test Suite 'CellScaffoldRuntimeIdentityMigrationCandidateCommandTests' passed at 2026-09-08 23:34:23.659.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.088 (0.088) seconds
Test Suite 'CellScaffoldRuntimeIdentityMigrationPlannerTests' passed at 2026-09-08 23:34:23.677.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
Test Suite 'CellScaffoldRuntimeIdentityProvisionerTests' passed at 2026-09-08 23:34:23.829.
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.151 (0.153) seconds
Test Suite 'CellScaffoldRuntimeIdentityRegistryTests' passed at 2026-09-08 23:34:23.932.
	 Executed 21 tests, with 0 failures (0 unexpected) in 0.101 (0.102) seconds
Test Suite 'CellScaffoldRuntimeStorageRootTests' passed at 2026-09-08 23:34:23.936.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'CellScaffoldServiceIdentityManifestTests' passed at 2026-09-08 23:34:23.942.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.006 (0.007) seconds
Test Suite 'CellScaffoldServiceIdentityRegistryTests' passed at 2026-09-08 23:34:23.974.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.031 (0.032) seconds
Test Suite 'ChatAIGatewayDiscoveryCacheTests' passed at 2026-09-08 23:34:23.975.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'ChatAuthTokenManagerTests' passed at 2026-09-08 23:34:23.976.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ChatCellTests' passed at 2026-09-08 23:34:24.030.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.054 (0.054) seconds
Test Suite 'ChatInterpreterEscalationCeilingTests' passed at 2026-09-08 23:34:24.040.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'ChatMVPLoginScopingTests' passed at 2026-09-08 23:34:24.705.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.665 (0.666) seconds
Test Suite 'ChatMVPRoutesTests' failed at 2026-09-08 23:34:29.095.
	 Executed 10 tests, with 7 failures (0 unexpected) in 4.389 (4.389) seconds
Test Suite 'ChatPurposeResourceRouterTests' passed at 2026-09-08 23:34:29.629.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.531 (0.534) seconds
Test Suite 'ChatScopedAIProviderRegistryPersistenceTests' passed at 2026-09-08 23:34:29.638.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'ChatScopedAIProviderRouterTests' passed at 2026-09-08 23:34:29.645.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
Test Suite 'CodableTests' passed at 2026-09-08 23:34:29.646.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'ConciergeKnowledgeCorpusCellTests' passed at 2026-09-08 23:34:29.774.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.127 (0.127) seconds
Test Suite 'ConferenceAIAssistantConfigurationTests' passed at 2026-09-08 23:34:29.790.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
Test Suite 'ConferenceAgendaCellTests' passed at 2026-09-08 23:34:29.908.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.118 (0.118) seconds
Test Suite 'ConferenceAudienceDiscoveryCellTests' passed at 2026-09-08 23:34:30.048.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.139 (0.140) seconds
Test Suite 'ConferenceBroadcastStudioCellTests' passed at 2026-09-08 23:34:30.104.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.056 (0.056) seconds
Test Suite 'ConferenceConfigurationCatalogTests' passed at 2026-09-08 23:34:33.623.
	 Executed 3 tests, with 0 failures (0 unexpected) in 3.519 (3.519) seconds
Test Suite 'ConferenceConnectionHubCellTests' passed at 2026-09-08 23:34:33.867.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.243 (0.244) seconds
Test Suite 'ConferenceDemoStoryCellTests' passed at 2026-09-08 23:34:33.940.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.073 (0.073) seconds
Test Suite 'ConferenceEntityDiscoveryCellTests' failed at 2026-09-08 23:34:34.082.
	 Executed 11 tests, with 1 failure (1 unexpected) in 0.142 (0.142) seconds
Test Suite 'ConferenceInsightAggregateCellTests' passed at 2026-09-08 23:34:34.099.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
Test Suite 'ConferenceLiveInteractionShellBridgeTests' passed at 2026-09-08 23:34:34.120.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.021 (0.021) seconds
Test Suite 'ConferenceMVPSkeletonTests' passed at 2026-09-08 23:34:34.122.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ConferenceMessageExchangeAcceptanceTests' passed at 2026-09-08 23:34:34.307.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.185 (0.185) seconds
Test Suite 'ConferenceOnboardingCellTests' passed at 2026-09-08 23:34:34.357.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.050 (0.050) seconds
Test Suite 'ConferenceOrganizerProjectionCellTests' failed at 2026-09-08 23:34:34.431.
	 Executed 3 tests, with 7 failures (0 unexpected) in 0.074 (0.074) seconds
Test Suite 'ConferencePlaywrightIdentityVaultTests' passed at 2026-09-08 23:34:34.482.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.051 (0.051) seconds
Test Suite 'ConferencePreviewWrapperResolverSupportTests' passed at 2026-09-08 23:34:35.919.
	 Executed 6 tests, with 0 failures (0 unexpected) in 1.436 (1.437) seconds
Test Suite 'ConferenceProofChatLaunchCellTests' passed at 2026-09-08 23:34:35.946.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.027 (0.027) seconds
Test Suite 'ConferencePublicProfileCellTests' passed at 2026-09-08 23:34:36.361.
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.415 (0.416) seconds
Test Suite 'ConferencePublicShellReadinessTests' passed at 2026-09-08 23:34:36.779.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.418 (0.418) seconds
Test Suite 'ConferencePublishedContentCellTests' failed at 2026-09-08 23:34:36.836.
	 Executed 10 tests, with 1 failure (1 unexpected) in 0.056 (0.057) seconds
Test Suite 'ConferenceRecommendationCellTests' passed at 2026-09-08 23:34:36.891.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.055 (0.055) seconds
Test Suite 'ConferenceRegistrationCellTests' passed at 2026-09-08 23:34:36.904.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
Test Suite 'ConferenceSchedulingCellTests' failed at 2026-09-08 23:34:36.943.
	 Executed 2 tests, with 1 failure (0 unexpected) in 0.039 (0.039) seconds
Test Suite 'ConferenceShellCellsTests' passed at 2026-09-08 23:34:42.635.
	 Executed 68 tests, with 0 failures (0 unexpected) in 5.686 (5.691) seconds
Test Suite 'ConferenceShellConfigurationFactoryTests' passed at 2026-09-08 23:34:42.887.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.252 (0.253) seconds
Test Suite 'ConferenceSimulationClockCellTests' passed at 2026-09-08 23:34:42.889.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ConferenceSimulationPlaybackCellTests' passed at 2026-09-08 23:34:43.043.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.154 (0.154) seconds
Test Suite 'ConferenceSimulationPopulationCellTests' passed at 2026-09-08 23:34:43.383.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.340 (0.340) seconds
Test Suite 'ConferenceSimulationStudioCellTests' passed at 2026-09-08 23:34:43.389.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'ConferenceSponsorLeadAggregateCellTests' failed at 2026-09-08 23:34:43.399.
	 Executed 2 tests, with 1 failure (1 unexpected) in 0.010 (0.010) seconds
Test Suite 'ConferenceSurfaceRoutesTests' failed at 2026-09-08 23:35:44.159.
	 Executed 39 tests, with 21 failures (0 unexpected) in 60.728 (60.760) seconds
Test Suite 'ConfigurationArchitectWorkspaceTests' passed at 2026-09-08 23:35:44.183.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.024 (0.024) seconds
Test Suite 'ConfigurationCatalogCellTests' passed at 2026-09-08 23:35:46.671.
	 Executed 31 tests, with 0 failures (0 unexpected) in 2.485 (2.488) seconds
Test Suite 'ConfigurationCatalogClientTests' passed at 2026-09-08 23:35:46.677.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
Test Suite 'ConfigurationCatalogSkeletonParityTests' failed at 2026-09-08 23:35:47.302.
	 Executed 17 tests, with 2 tests skipped and 1 failure (0 unexpected) in 0.623 (0.624) seconds
Test Suite 'ContactEndpointCellTests' passed at 2026-09-08 23:35:49.000.
	 Executed 14 tests, with 0 failures (0 unexpected) in 1.696 (1.698) seconds
Test Suite 'ContactRegistryCellTests' passed at 2026-09-08 23:35:49.031.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.031 (0.032) seconds
Test Suite 'ContextTransitionPayloadFactoryTests' passed at 2026-09-08 23:35:49.032.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'ContractChallengeMVPRoutesTests' failed at 2026-09-08 23:35:50.499.
	 Executed 5 tests, with 9 failures (0 unexpected) in 1.466 (1.467) seconds
Test Suite 'CredentialSealingTests' passed at 2026-09-08 23:35:50.500.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'DevelopmentStatusRoutesTests' passed at 2026-09-08 23:35:53.142.
	 Executed 5 tests, with 0 failures (0 unexpected) in 2.642 (2.642) seconds
Test Suite 'DevelopmentStatusSnapshotProducerTests' passed at 2026-09-08 23:35:53.428.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.284 (0.285) seconds
Test Suite 'DevelopmentStatusSnapshotTests' passed at 2026-09-08 23:35:53.484.
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.055 (0.056) seconds
Test Suite 'DeviceCallbackCapabilityServerTests' passed at 2026-09-08 23:35:53.582.
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.097 (0.099) seconds
Test Suite 'DeviceRegistrationReadinessTests' passed at 2026-09-08 23:35:53.602.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.019 (0.020) seconds
Test Suite 'DocumentationWorkbenchRoutesTests' passed at 2026-09-08 23:35:53.905.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.303 (0.303) seconds
Test Suite 'EntityAnchorDataV1ContractTests' passed at 2026-09-08 23:35:54.201.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.295 (0.296) seconds
Test Suite 'EntityAtlasRoutesTests' passed at 2026-09-08 23:35:54.797.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.596 (0.596) seconds
Test Suite 'EntityCellGraphCellTests' passed at 2026-09-08 23:35:54.828.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.030 (0.030) seconds
Test Suite 'EntityGraphStorageTests' passed at 2026-09-08 23:35:54.832.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'EntityMergePolicyRegistryV0Tests' passed at 2026-09-08 23:35:54.837.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.004 (0.005) seconds
Test Suite 'EntityOperationEnvelopeV0Tests' passed at 2026-09-08 23:35:54.848.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.011 (0.012) seconds
Test Suite 'EntityScaffoldEnrollmentCellTests' passed at 2026-09-08 23:35:54.991.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.142 (0.143) seconds
Test Suite 'EntityStudioCellTests' passed at 2026-09-08 23:35:55.356.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.363 (0.364) seconds
Test Suite 'EntityStudioConfigurationFactoryTests' passed at 2026-09-08 23:35:55.372.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
Test Suite 'EventPlatformRoutesTests' passed at 2026-09-08 23:35:57.537.
	 Executed 6 tests, with 0 failures (0 unexpected) in 2.164 (2.165) seconds
Test Suite 'EventPublisherRegistryCellTests' passed at 2026-09-08 23:35:57.550.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.013 (0.014) seconds
Test Suite 'ExecutablePurposeGroundingCellTests' passed at 2026-09-08 23:35:59.610.
	 Executed 36 tests, with 0 failures (0 unexpected) in 2.055 (2.059) seconds
Test Suite 'FlowDebugProbeCellTests' passed at 2026-09-08 23:35:59.656.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.045 (0.046) seconds
Test Suite 'FundingEntitlementAgreementTests' passed at 2026-09-08 23:35:59.660.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'GitHubWorkSyncCellTests' passed at 2026-09-08 23:35:59.664.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
Test Suite 'GraphStoreCellTests' passed at 2026-09-08 23:36:00.052.
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.387 (0.388) seconds
Test Suite 'GuidedOnboardingCellTests' passed at 2026-09-08 23:36:00.278.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.226 (0.227) seconds
Test Suite 'HAVENAgentCapabilityBrokerCellTests' passed at 2026-09-08 23:36:00.405.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.126 (0.126) seconds
Test Suite 'HavenWorkbenchConfigurationTests' failed at 2026-09-08 23:36:00.513.
	 Executed 6 tests, with 1 failure (0 unexpected) in 0.107 (0.108) seconds
Test Suite 'IdeaTaskWorkspaceTests' passed at 2026-09-08 23:36:01.769.
	 Executed 20 tests, with 0 failures (0 unexpected) in 1.255 (1.257) seconds
Test Suite 'JWTAuthRoutesTests' passed at 2026-09-08 23:36:16.797.
	 Executed 13 tests, with 0 failures (0 unexpected) in 15.027 (15.028) seconds
Test Suite 'LeadVaultCellTests' passed at 2026-09-08 23:36:16.808.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'LeadVaultRoutesTests' passed at 2026-09-08 23:36:17.761.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.952 (0.953) seconds
Test Suite 'LiveInteractionCellTests' passed at 2026-09-08 23:36:17.996.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.234 (0.235) seconds
Test Suite 'LocalLLMGatewayCellTests' passed at 2026-09-08 23:36:18.007.
	 Executed 4 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'MVPAdminAccessTests' passed at 2026-09-08 23:36:18.010.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
Test Suite 'MarkdownRendererCellTests' passed at 2026-09-08 23:36:18.044.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.033 (0.033) seconds
Test Suite 'MediaCollectionCellTests' passed at 2026-09-08 23:36:18.083.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.039 (0.040) seconds
Test Suite 'MermaidRendererCellTests' failed at 2026-09-08 23:36:33.608.
	 Executed 11 tests, with 14 failures (0 unexpected) in 15.523 (15.525) seconds
Test Suite 'MicropaymentsAuditRoutesTests' passed at 2026-09-08 23:36:34.230.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.621 (0.621) seconds
Test Suite 'MicropaymentsMVPRoutesTests' failed at 2026-09-08 23:36:34.580.
	 Executed 1 test, with 4 failures (0 unexpected) in 0.350 (0.350) seconds
Test Suite 'MintClientBootstrapTests' passed at 2026-09-08 23:36:34.582.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'MultilevelCodableTests' passed at 2026-09-08 23:36:34.583.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'MusicPublishingCellsTests' failed at 2026-09-08 23:36:34.745.
	 Executed 26 tests, with 3 failures (0 unexpected) in 0.160 (0.162) seconds
Test Suite 'MusicPublishingConfigurationFactoryTests' passed at 2026-09-08 23:36:34.810.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.065 (0.065) seconds
Test Suite 'MusicPublishingMVPRoutesTests' passed at 2026-09-08 23:36:35.069.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.259 (0.259) seconds
Test Suite 'NativeLocalModelBridgeTests' passed at 2026-09-08 23:36:35.071.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'NodeAdminAgentDeliveryTests' passed at 2026-09-08 23:36:35.072.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'NodeAdminAgentSnapshotBuilderTests' passed at 2026-09-08 23:36:36.482.
	 Executed 8 tests, with 0 failures (0 unexpected) in 1.409 (1.411) seconds
Test Suite 'NodeAdminDockerCollectorTests' passed at 2026-09-08 23:36:36.541.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.058 (0.059) seconds
Test Suite 'NotificationPushProviderTests' passed at 2026-09-08 23:36:36.778.
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.236 (0.238) seconds
Test Suite 'NotificationRuntimeReadinessTests' passed at 2026-09-08 23:36:36.855.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.076 (0.076) seconds
Test Suite 'ObjectStorageAdapterCellTests' passed at 2026-09-08 23:36:36.896.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.041 (0.041) seconds
Test Suite 'ObsidianAIWorkspaceConfigurationTests' passed at 2026-09-08 23:36:36.914.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
Test Suite 'OrchestratorPersistenceTests' passed at 2026-09-08 23:36:40.950.
	 Executed 7 tests, with 0 failures (0 unexpected) in 4.035 (4.036) seconds
Test Suite 'OwnerScopedCredentialCellTests' passed at 2026-09-08 23:36:41.007.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.057 (0.058) seconds
Test Suite 'OwnerScopedCredentialStoreTests' passed at 2026-09-08 23:36:41.033.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.025 (0.026) seconds
Test Suite 'PalazzoCommunaleRoutesTests' passed at 2026-09-08 23:36:41.307.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.273 (0.273) seconds
Test Suite 'PalazzoCommunaleServiceTests' passed at 2026-09-08 23:36:41.335.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.028 (0.028) seconds
Test Suite 'ParticipationHubCellTests' passed at 2026-09-08 23:36:41.379.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.044 (0.044) seconds
Test Suite 'ParticipationHubConfigurationFactoryTests' passed at 2026-09-08 23:36:41.394.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
Test Suite 'PaymentAccessCredentialStoreLifecycleTests' passed at 2026-09-08 23:36:44.718.
	 Executed 13 tests, with 0 failures (0 unexpected) in 3.323 (3.324) seconds
Test Suite 'PaymentGateCellTests' passed at 2026-09-08 23:36:47.162.
	 Executed 14 tests, with 0 failures (0 unexpected) in 2.443 (2.444) seconds
Test Suite 'PaymentGateOwnerIdentitySupportTests' passed at 2026-09-08 23:36:47.170.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.008 (0.008) seconds
Test Suite 'PaymentProofDoorCellTests' passed at 2026-09-08 23:36:47.192.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.021 (0.022) seconds
Test Suite 'PersistedRuntimeReadinessTests' passed at 2026-09-08 23:36:47.882.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.690 (0.690) seconds
Test Suite 'PersonalAIProviderPolicyTests' passed at 2026-09-08 23:36:47.891.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'PersonalAssistantProfileCellTests' passed at 2026-09-08 23:36:47.917.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.026 (0.026) seconds
Test Suite 'PersonalChatPromptEvaluationTests' passed at 2026-09-08 23:37:28.760.
	 Executed 11 tests, with 0 failures (0 unexpected) in 40.841 (40.842) seconds
Test Suite 'PersonalCopilotCollaborationInviteTests' passed at 2026-09-08 23:37:28.975.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.215 (0.215) seconds
Test Suite 'PersonalCopilotV1Tests' passed at 2026-09-08 23:37:42.699.
	 Executed 70 tests, with 0 failures (0 unexpected) in 13.719 (13.724) seconds
Test Suite 'PersonalDataTrustPackageCellTests' passed at 2026-09-08 23:37:42.716.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.016 (0.017) seconds
Test Suite 'PersonalEntityActivityDashboardConfigurationTests' passed at 2026-09-08 23:37:43.461.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.744 (0.744) seconds
Test Suite 'PersonalPagePublisherCellTests' passed at 2026-09-08 23:37:43.486.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.025 (0.025) seconds
Test Suite 'PersonalPagePublisherConfigurationTests' passed at 2026-09-08 23:37:43.489.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'PersonlogProjectionCellTests' passed at 2026-09-08 23:37:43.636.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.147 (0.148) seconds
Test Suite 'PerspectiveCellTests' passed at 2026-09-08 23:37:43.647.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'PortholeBootstrapProjectionTests' passed at 2026-09-08 23:37:43.665.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.018 (0.019) seconds
Test Suite 'PortholeConfigurationLoadingTests' failed at 2026-09-08 23:49:58.334.
	 Executed 45 tests, with 5 failures (0 unexpected) in 734.613 (734.668) seconds
Test Suite 'PortholeIdentityContinuityRoutesTests' passed at 2026-09-08 23:50:11.753.
	 Executed 4 tests, with 0 failures (0 unexpected) in 13.418 (13.419) seconds
Test Suite 'PortholeMenuFallbackTests' passed at 2026-09-08 23:50:12.074.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.319 (0.321) seconds
Test Suite 'PortholeRuntimeBindingEnsuringTests' passed at 2026-09-08 23:50:16.151.
	 Executed 10 tests, with 0 failures (0 unexpected) in 4.075 (4.076) seconds
Test Suite 'PortholeWebActionStateSourceTests' passed at 2026-09-08 23:50:16.178.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.027 (0.027) seconds
Test Suite 'PortholeWebEditorSupportTests' passed at 2026-09-08 23:50:16.223.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.044 (0.045) seconds
Test Suite 'PortholeWebPayloadTests' passed at 2026-09-08 23:50:16.308.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.085 (0.085) seconds
Test Suite 'PortholeWebSessionPersonaTests' passed at 2026-09-08 23:50:19.700.
	 Executed 15 tests, with 0 failures (0 unexpected) in 3.390 (3.392) seconds
Test Suite 'ProductionOwnerIdentityContinuityTests' passed at 2026-09-08 23:50:19.707.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.007 (0.008) seconds
Test Suite 'ProductionRuntimeAdmissionMiddlewareTests' passed at 2026-09-08 23:50:19.722.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.014 (0.015) seconds
Test Suite 'ProductionSkeletonBindingIntegrityTests' failed at 2026-09-08 23:50:37.314.
	 Executed 4 tests, with 19 failures (1 unexpected) in 17.591 (17.592) seconds
Test Suite 'ProjectOperationsTests' passed at 2026-09-08 23:50:37.489.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.174 (0.176) seconds
Test Suite 'ProjectPortfolioCellTests' passed at 2026-09-08 23:50:37.986.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.493 (0.496) seconds
Test Suite 'ProofDoorMVPRouteSecurityTests' passed at 2026-09-08 23:50:37.996.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
Test Suite 'PublishedConfigurationCatalogCellTests' passed at 2026-09-08 23:50:38.379.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.383 (0.384) seconds
Test Suite 'PurposeQualityMonitorCellTests' passed at 2026-09-08 23:50:38.676.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.295 (0.297) seconds
Test Suite 'QuestionnaireCampaignCellTests' passed at 2026-09-08 23:50:40.766.
	 Executed 13 tests, with 0 failures (0 unexpected) in 2.088 (2.091) seconds
Test Suite 'QuestionnaireCampaignRoutesTests' passed at 2026-09-08 23:50:45.122.
	 Executed 2 tests, with 0 failures (0 unexpected) in 4.355 (4.356) seconds
Test Suite 'QuestionnaireResponseCellTests' passed at 2026-09-08 23:50:45.168.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.045 (0.046) seconds
Test Suite 'RAGCellAccessSecurityTests' passed at 2026-09-08 23:50:45.251.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.070 (0.083) seconds
Test Suite 'RAGGatewayCellTests' passed at 2026-09-08 23:50:45.405.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.152 (0.154) seconds
Test Suite 'RAGGatewayConfigTests' passed at 2026-09-08 23:50:45.415.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
Test Suite 'RAGGatewayConfigurationFactoryTests' passed at 2026-09-08 23:50:45.432.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
Test Suite 'RAGGatewayHTTPClientTests' passed at 2026-09-08 23:50:45.612.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.176 (0.180) seconds
Test Suite 'RAGIngestionCellTests' passed at 2026-09-08 23:50:45.729.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.112 (0.116) seconds
Test Suite 'RAGMVPRoutesTests' passed at 2026-09-08 23:50:49.527.
	 Executed 5 tests, with 0 failures (0 unexpected) in 3.798 (3.798) seconds
Test Suite 'RAGPersistedRuntimeReadinessTests' passed at 2026-09-08 23:50:49.795.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.267 (0.268) seconds
Test Suite 'RAGPromptAdminCellTests' passed at 2026-09-08 23:50:49.846.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.050 (0.050) seconds
Test Suite 'RAGPromptAdminConfigurationFactoryTests' passed at 2026-09-08 23:50:49.847.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'RemoteBridgeheadAccessTests' passed at 2026-09-08 23:50:50.001.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.154 (0.154) seconds
Test Suite 'RestaurantExperiencePlanCellTests' passed at 2026-09-08 23:50:50.223.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.222 (0.222) seconds
Test Suite 'RestaurantOnboardingCellTests' passed at 2026-09-08 23:50:50.231.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
Test Suite 'RestaurantPublishedContentCellTests' passed at 2026-09-08 23:50:50.242.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
Test Suite 'RestaurantShellCellsTests' passed at 2026-09-08 23:50:50.381.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.139 (0.139) seconds
Test Suite 'RestaurantSurfaceRoutesTests' passed at 2026-09-08 23:50:52.338.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.956 (1.956) seconds
Test Suite 'RestaurantVisitContextCellTests' passed at 2026-09-08 23:50:52.345.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.008 (0.008) seconds
Test Suite 'SMIAgreementSettlementCellTests' passed at 2026-09-08 23:50:52.386.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.040 (0.040) seconds
Test Suite 'SalesWorkspaceCellTests' passed at 2026-09-08 23:50:52.425.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.039 (0.040) seconds
Test Suite 'ScaffoldLaunchRegistryCellTests' passed at 2026-09-08 23:50:52.477.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.051 (0.051) seconds
Test Suite 'ScaffoldNotificationContractsTests' passed at 2026-09-08 23:50:52.479.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
Test Suite 'ScaffoldOwnerAdminRoutesTests' passed at 2026-09-08 23:50:54.427.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.947 (1.948) seconds
Test Suite 'ScaffoldSetupCellTests' passed at 2026-09-08 23:50:58.038.
	 Executed 15 tests, with 0 failures (0 unexpected) in 3.610 (3.611) seconds
Test Suite 'ScaffoldSurfaceGatePolicyTests' passed at 2026-09-08 23:50:58.169.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.131 (0.131) seconds
Test Suite 'ScaffoldTruthSourceCatalogTests' passed at 2026-09-08 23:50:58.175.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.005 (0.006) seconds
Test Suite 'SecureDevelopmentStatusSnapshotFileTests' passed at 2026-09-08 23:50:58.202.
	 Executed 9 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.026 (0.027) seconds
Test Suite 'SecureRuntimeIdentityManifestFileTests' passed at 2026-09-08 23:50:58.234.
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.032 (0.033) seconds
Test Suite 'SecurityWorkbenchCellTests' passed at 2026-09-08 23:50:58.287.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.052 (0.052) seconds
Test Suite 'SkeletonElementParityMatrixTests' failed at 2026-09-08 23:50:58.695.
	 Executed 3 tests, with 2 failures (0 unexpected) in 0.408 (0.408) seconds
Test Suite 'SkeletonParityRoutesTests' passed at 2026-09-08 23:50:59.795.
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.100 (1.100) seconds
Test Suite 'SkeletonPortableModelTests' passed at 2026-09-08 23:50:59.863.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.067 (0.067) seconds
Test Suite 'SkeletonRuntimeDecoderTests' passed at 2026-09-08 23:50:59.866.
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.002 (0.003) seconds
Test Suite 'SkeletonRuntimeSourceTests' failed at 2026-09-08 23:51:00.116.
	 Executed 16 tests, with 1 failure (0 unexpected) in 0.248 (0.250) seconds
Test Suite 'SkeletonStyleParityCSSDriftTests' passed at 2026-09-08 23:51:00.147.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.031 (0.031) seconds
Test Suite 'SpatialCellsTests' passed at 2026-09-08 23:51:00.177.
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.029 (0.030) seconds
Test Suite 'SpatialRegistryRemoteIntegrationTests' passed at 2026-09-08 23:51:00.178.
	 Executed 1 test, with 1 test skipped and 0 failures (0 unexpected) in 0.001 (0.001) seconds
Test Suite 'SproutBridgeDiscoveryRoutesTests' passed at 2026-09-08 23:51:01.559.
	 Executed 5 tests, with 0 failures (0 unexpected) in 1.381 (1.382) seconds
Test Suite 'SproutExecutableCatalogRoutesTests' passed at 2026-09-08 23:51:01.849.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.289 (0.289) seconds
Test Suite 'SproutResolverRoutesTests' passed at 2026-09-08 23:51:02.828.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.979 (0.979) seconds
Test Suite 'StrictIdentityVaultReadinessMonitorTests' passed at 2026-09-08 23:51:02.829.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
Test Suite 'SwarmIdentityAdmissionCellTests' passed at 2026-09-08 23:51:02.874.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.045 (0.045) seconds
Test Suite 'TodoCellConfigurationTests' passed at 2026-09-08 23:51:02.874.
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'TodoPlannerCopilotConfigurationTests' passed at 2026-09-08 23:51:02.893.
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.018 (0.019) seconds
Test Suite 'TopUpCheckoutTests' failed at 2026-09-08 23:51:06.035.
	 Executed 19 tests, with 3 failures (3 unexpected) in 3.140 (3.142) seconds
Test Suite 'TranscriptStoreCellTests' passed at 2026-09-08 23:51:06.075.
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.040 (0.040) seconds
Test Suite 'TrustPacketConfigurationFactoryTests' passed at 2026-09-08 23:51:06.224.
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.149 (0.149) seconds
Test Suite 'UserSimulationScaffoldTests' passed at 2026-09-08 23:51:07.226.
	 Executed 28 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.999 (1.002) seconds
Test Suite 'VaporProductControlDurabilityTests' passed at 2026-09-08 23:51:07.282.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.056 (0.056) seconds
Test Suite 'VaultMVPRoutesTests' passed at 2026-09-08 23:51:10.614.
	 Executed 6 tests, with 0 failures (0 unexpected) in 3.331 (3.332) seconds
Test Suite 'VaultStudioWorkspaceTests' passed at 2026-09-08 23:51:10.639.
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.025 (0.026) seconds
Test Suite 'WebFetchCeilingTests' passed at 2026-09-08 23:51:10.755.
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.114 (0.115) seconds
Test Suite 'WebKnowledgeCellsTests' passed at 2026-09-08 23:51:10.792.
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.037 (0.037) seconds
Test Suite 'WorkItemCellTests' passed at 2026-09-08 23:51:10.821.
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.028 (0.029) seconds
Test Suite 'WorkbenchAccessGrantConfigurationTests' failed at 2026-09-08 23:51:13.733.
	 Executed 24 tests, with 1 failure (1 unexpected) in 2.910 (2.912) seconds
Test Suite 'WorkbenchOwnerSetupCellTests' passed at 2026-09-08 23:51:21.506.
	 Executed 7 tests, with 0 failures (0 unexpected) in 7.770 (7.773) seconds
Test Suite 'CellsContainerPackageTests.xctest' failed at 2026-09-08 23:51:21.506.
	 Executed 2101 tests, with 11 tests skipped and 151 failures (9 unexpected) in 1053.507 (1053.782) seconds
Test Suite 'All tests' failed at 2026-09-08 23:51:21.508.
	 Executed 2101 tests, with 11 tests skipped and 151 failures (9 unexpected) in 1053.507 (1053.785) seconds
```

Maskinell sammenligning av røde testnavn mot WP0c (`failure-comparison.json` i råloggmappen):

```text
Baseline failed names: 46
Current failed names: 46
New failed names: []
Missing failed names: []
```

De samme 46 røde testnavnene:

```text
-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsHAVENTeachingSwarmAndAppendsProviderTurns]
-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsLocalOnlyHAVENTeachingSwarmWithoutAPIKeys]
-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelLocalBorealisChatsAgainstSharedBackend]
-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelMixedHostedAndLocalChatsWithRouteCredentials]
-[AppTests.ArendalsukaEventAtlasCellTests testDecodedParticipantProgramCanEnsureRuntimeBindingsBeforeStateRead]
-[AppTests.ArendalsukaEventAtlasCellTests testParticipantPreviewReadsDecodedRegisteredAtlasWithoutJournalFallback]
-[AppTests.ArendalsukaEventAtlasCellTests testParticipantProgramReadsAtlasPreviewWithoutPersistingUntilExplicitAction]
-[AppTests.ArendalsukaEventAtlasCellTests testParticipantProgramUsesAtlasPreviewForMissingProgramInPartialOverlay]
-[AppTests.ArendalsukaImportAuthorizationRoutesTests testAdminDelegatesIdentityBoundCredentialToNonAdminImporter]
-[AppTests.BookReferenceRoutesTests testConferenceConnectionHubLifecycleSlugRouteRendersMermaidInline]
-[AppTests.BookReferenceRoutesTests testConferenceOwnershipSlugRouteRendersMermaidInline]
-[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview]
-[AppTests.ChatMVPRoutesTests testPaidStateAndMessageRoutesAwaitDecodedChatReadiness]
-[AppTests.ConferenceEntityDiscoveryCellTests testChatLaunchCellCanStartConversationAndProjectMessageFeedback]
-[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionHandsOffCapturedLeadToSponsorOwnedFollowUp]
-[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionUsesConsentBoundAggregateSignalsWhenAvailable]
-[AppTests.ConferencePublishedContentCellTests testPublishedContentCellRecognizesStableOrganizerIdentityWhenVaultContextIsPoisoned]
-[AppTests.ConferenceSchedulingCellTests testRouterDelegatesSharedMeetingRequestAndLocalExportToSchedulingCell]
-[AppTests.ConferenceSponsorLeadAggregateCellTests testSponsorLeadAggregateSyncsConsentBoundParticipantsAndCapturesLead]
-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionAcceptsStoredImportAccessVC]
-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionSupportsAdminSessionAndRejectsMismatchedSignedProof]
-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication]
-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublishedApiReadsUseAgreementWithoutDebugAccess]
-[AppTests.ConferenceSurfaceRoutesTests testConferencePageAccessPolicies]
-[AppTests.ConferenceSurfaceRoutesTests testConferencePagesExposeCanonicalSurfaceMetadataForWebNavigator]
-[AppTests.ConfigurationCatalogSkeletonParityTests testConferenceParticipantPortalDocumentationConfigurationMatchesRuntimeFactory]
-[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeRetryBlocksConsumedCredentialReplay]
-[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction]
-[AppTests.HavenWorkbenchConfigurationTests testHavenWorkbenchUsesLocalTabsAndSupportedVisualizations]
-[AppTests.MermaidRendererCellTests testWebViewDeterministicModeStableAcrossThreeBypassRuns]
-[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersPNGWithoutClientTimeout]
-[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersSVGAndCacheHit]
-[AppTests.MermaidRendererCellTests testWebViewRendersConferenceDiagramFilesAndExposesPreviewState]
-[AppTests.MicropaymentsMVPRoutesTests testPaymentProofDoorAuthorizeConsumesCredentialAndBlocksReplay]
-[AppTests.MusicPublishingCellsTests testScaffoldRecoversPersistedMusicLibraryWhenNamedEmitterRegistryIsEmpty]
-[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction]
-[AppTests.ProductionSkeletonBindingIntegrityTests testArendalsukaEventAtlasPortholeTabsAndDetailsDoNotReturnNotFound]
-[AppTests.ProductionSkeletonBindingIntegrityTests testArendalsukaParticipantProgramRendersSourceBackedProgramRowsWithoutBrokenKeypaths]
-[AppTests.ProductionSkeletonBindingIntegrityTests testHavenWorkbenchSetupThroughPortholeKeepsSkeletonBindingsResolvable]
-[AppTests.SkeletonElementParityMatrixTests testMatrixRevisionMatchesPackagePin]
-[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips]
-[AppTests.SkeletonRuntimeSourceTests testPortholeBootstrapUsesHttpSnapshotNotSocketFallbackWarning]
-[AppTests.TopUpCheckoutTests testProductionStartupRejectsMissingRuntimeIdentityManifestBeforePublishingResolver]
-[AppTests.TopUpCheckoutTests testSimulatedTopUpAllowsExplicitProductionAllowlistedUser]
-[AppTests.TopUpCheckoutTests testSimulatedTopUpDefaultsToDeniedInProductionLikeEnvironment]
-[AppTests.WorkbenchAccessGrantConfigurationTests testIdentityBoundPregrantUsesIssuerVaultWhenTargetOwnerWasDecodedSnapshot]
```

**Feilrapportantall 148 → 151:** eneste endring er `PortholeConfigurationLoadingTests.testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction`, fra 2 til 5 assertion-feil. Dette er samme test, linjer og render-/bootstrap-variasjon som dokumentert i WP2. Ingen andre testtilfeller har endret feilrapportantall. Ekte utdata fra WP5-fullkjøringen:

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:968: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertTrue failed - Expected webview render to succeed: [CellBase.ValueType.string("Render timed out after 2000ms")]
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:969: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertNotNil failed
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:993: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertEqual failed: ("Optional(CellBase.ValueType.bool(false))") is not equal to ("Optional(CellBase.ValueType.bool(true))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:994: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertTrue failed - Expected rendered preview HTML in projected bootstrap state.
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:998: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertEqual failed: ("Render timed out after 2000ms") is not equal to ("")
```

Én isolert omkjøring, med uendret bundle/kilde, ga baseline-antallet 2 feil. Ingen Mermaid-/Porthole-kode eller test er endret i WP5:

```text
$ xcrun --sdk macosx xctest -XCTest AppTests.PortholeConfigurationLoadingTests/testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:968: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertTrue failed - Expected webview render to succeed: [CellBase.ValueType.string("Render timed out after 2000ms")]
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:969: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertNotNil failed
	 Executed 1 test, with 2 failures (0 unexpected) in 6.337 (6.337) seconds
	 Executed 1 test, with 2 failures (0 unexpected) in 6.337 (6.337) seconds
	 Executed 1 test, with 2 failures (0 unexpected) in 6.337 (6.338) seconds
```

Kildehashene fra starten av fullkjøringen er kontrollert uendret etter testene. Loggene ligger i `/private/tmp/wp5-webfetch/`; nødvendig kjørings- og avviksevidens er bevart i denne filen. Ingen git-kommandoer er kjørt.

## WP5 — sluttmelding

WP5 — WebFetch-ceiling er **levert** for `purpose://candidate.tillitspakke-agentflaate.webfetch-ceiling`. Grensen håndheves i `WebFetchCell` fra persistent data per instans, med eksplisitt eierbevis for SET, deny-all ved manglende/ukjent ceiling, HTTPS/GET/ingen body, host-/portmønstre, null credential-oppslag, stoppede redirects og begrenset mottak. Pakken leser den faktiske ceiling-kilden og viser whitelist/ceilingLabel; hostendringer endrer pakke-digest.

Endrede kodefiler: `CellScaffold/Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift`, `CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift`, ny `CellScaffold/Tests/AppTests/WebFetchCeilingTests.swift`, samt de eksisterende `WebKnowledgeCellsTests.swift` og `AgentTrustPackageCellTests.swift`. Kontraktens denyReasons i `P/contract/agent_trust_package_contract_v0.json` er oppdatert med de implementerte typede grunnene, inkludert `ceiling_missing`.

Bygg grønt. **17/17 ceiling-tester grønne; 53/53 målrettede tester grønne. Full XCTest-bundle: 2101 tester / 11 hoppet over / samme 46 røde testnavn som baseline / ingen nye.** Fullbundlen er fortsatt rød med 151 feilrapporter; de 3 ekstra mot WP0c er samme kjente Mermaid-variasjon som i WP2, og isolert omkjøring gir baseline 2. Varighet 1053.507 s; Swift Testing ikke dekket.

`STATUS.md` har én WP5-linje. Kun WP5 er utført: ingen nye justerings-keypaths, ingen godkjenningsport, ingen git. Formål og pakke gir ingen rettigheter.


## Justering <a id="justering"></a>

purposeRef: `purpose://candidate.tillitspakke-agentflaate.justering`. Kun WP6.

### WP6 — baseline før endring

Bygg/test etter handoff regel 9–10, uten arch-prefiks. Ny justeringsklasse finnes ikke ennå (0 tester).

```text
$ cd CellScaffold
$ swift build --disable-sandbox --build-tests
Build complete! (24.36s)
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAdjustTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.160 (0.162) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.160 (0.162) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.160 (0.163) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.410 (0.411) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.410 (0.411) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.410 (0.412) seconds
```

Baseline: 17 WebFetch + 16 pakke = 33 tester, 0 feil. Første testforsøk fra Python-subprocess valgte x86_64-lasteren (exit 80, `incompatible architecture (have arm64, need x86_64)`); ingen tester kjørte. Direkte `xcrun` fra shell som regel 10 angir, kjørte grønt. Python-wrapperen brukes ikke videre. Full bundle er ikke påkrevd i WP6.

### WP6 — implementasjon og avgrensning

- `trustPackage.adjust.whitelist`, `.credentials` og `.webfetchWrite` er implementert med de avtalte objekt-payloadene og `rw--`. Eksakt keypath-autorisasjon og et eksplisitt signeringsbevis for eieren kreves; offentlig identity-snapshot, kopiert offentlig nøkkel/feil vault og debug-bypass gir ikke justeringsrett. Enum-baserte avvisningsgrunner returneres uten rå kildeverdier. Ingen justering skriver til `agreementTemplate` eller utsteder Contracts/Grants.
- Whitelist bruker WP5s faktiske parser for både syntaks og delmengdekontroll. Eksakt vert, wildcard under domenet (aldri apex), eksakt port og standard 443 gjelder. Hver linje trimmes; CRLF støttes, casing normaliseres og duplikater fjernes. Tom tekst og blanke linjer gir `invalid_pattern`. Første ikke-tomme liste ved manglende/aldri-initialisert tom ceiling tillates fra templatens HTTPS-tak. Historikkflagget bor i WebFetch-instansens snapshot og overlever reload; en senere tom liste eller ny pakkecelle gir ikke en ny førstegangsåpning.
- Alle flåtemål og foreslåtte mønstre valideres før første skriving. Utvidelse gir `denied(expansion_not_allowed)`, med uendret pakke og WebFetch-ceiling. Godtatte endringer skrives gjennom `WebFetch.webFetch.ceiling.set`, re-leses og regenererer pakken med ny digest når kildene endres. Gjentatt SET av identiske verdier er idempotent og beholder digest, som den eksisterende determinismekontrakten krever. `adjust.whitelistText` viser sorterte gjeldende mønstre.
- WebFetch v0s implementerte tak er fortsatt HTTPS/GET, uten credentials eller redirects. Derfor avvises `credentials:true` og `webfetchWrite:true` med `expansion_not_allowed`, også når eieren selv kan administrere WebFetch eller en ScopedCredential-celle finnes i flåten. Tilstedeværelse av en credential-celle er ingen credential-Grant; `w` på en administrasjons-/fetch-keypath er heller ikke HTTP POST-rett. PurposeBoundAIGateway har ingen `web.fetch w`-Grant eller ekstern skriveeffekt i A4-templaten. `false` skriver henholdsvis `allowCredentials=false` og `methods=[GET]`.
- PurposeBoundAIGateway har nå eierkontrollerte dataoperasjoner `ai.executionPolicy.ceiling` (GET `r---`, kanonisk CellExecutionPolicy-JSON) og `ai.executionPolicy.ceiling.set` (SET `rw--`). Innsnevringen lagres som `trustPackageExecutionPolicyCeiling` ved siden av templaten i cellens snapshot. Bare delmengder av både gjeldende policy og Swift-templatens tak tillates; bindende authority-/purpose-/provenance-felt kan ikke endres. De tre pakkejusteringene skriver også denne policy-ceilingen på flåtens PurposeBoundAIGateway-mål. Provider-invokasjonen leser samme lagrede ceiling. Den signerte template-bindingen beholdes som myndighetstak; ved innsnevret policy bruker pakkens `policy.policyDigest` domenet `haven.agent-trust-package.effective-policy.v0` over hele policy-dataene, slik at også endret dataklasse hos bare én leverandør endrer pakke-digest. Uendret template-policy beholder tidligere digest.
- A4 beholder én provider-invokasjon, med to nye eierstyrte dataoperasjoner. De eksisterende AIGateway-testene krever nå den eksakte listen på tre keypaths ved init/reload; kontrollene av signert policy-binding, avvist mixed-Grant-avtale og fravær av legacy `state` er beholdt. Ny negativ test kjører produksjonens `invokePurposeBound` og krever 0 provider-kall / 0 credential-oppslag etter at provider-ceiling er fjernet. Ingen kjernetemplate-/resolver-semantikk er endret.
- Lagringen følger WP5s dokumenterte mekanisme: Codable-data per mål-instans og eksisterende `CellResolver.persistCellSnapshot`, med `.identityUnique`/`.persistant`-registreringene som allerede finnes. Det er ikke innført en separat EntityAnchor-tabell eller ny lagringsmotor. Ephemeral testceller verifiserer encode/decode, ikke varig disk-commit. Skriving over flere celler er ikke en distribuert transaksjon; ved teknisk feil etter at skriving har begynt trekkes pakkeprojeksjonen tilbake til «Ikke avledet» fremfor å vise gammel digest som gjeldende. Vanlige avslag på utvidelse skjer før dette punktet.
- `hasChangesSinceApproval` er bool i state/Explore. Et eventuelt `approved`-record leses defensivt fra Codable-data; bare det valgfrie `digest`-feltet brukes til presentasjon. Ved avvik er labelen eksakt «Ikke godkjent — pakken er endret etter siste godkjenning». Uten record er flagget false. Testens injiserte record er kun en UI-fixture, aldri et signerings-/godkjenningsbevis. `approve`, startport og audit er fortsatt senere slicer.

### WP6 — rettede bygg-/testforsøk

Første bygg fant to nye Swift-typefeil: `registerGet`/`registerSet` krever ikke-kastende handler-closures. De er rettet med typede avvisningsreturer. Første justeringskjøring fant én feil i reload-fixturen (`personalInstanceAlreadyRegistered`); testen bruker nå en ny resolver, som ved reell reload. Neste kjøring fant at direkte `ValueType.list`-likhet ikke sammenligner innhold strukturelt. Permission-listen dekodes nå før samme eksakte assert (`[rw--]`); produksjonskoden er uendret av denne rettingen.

```text
build-1.log
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift:3331:113: error: invalid conversion from throwing function of type '(Identity) async throws -> ValueType' to non-throwing function type '(Identity) async -> ValueType'
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift:3338:120: error: invalid conversion from throwing function of type '(Identity, ValueType) async throws -> ValueType?' to non-throwing function type '(Identity, ValueType) async -> ValueType?'
adjust-first.log
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Cells/CellResolver/Cast/ResolverAuditor.swift:171: error: -[AppTests.AgentTrustPackageAdjustTests testFirstWhitelistFromMissingOrEmptyCeilingIsAllowedAndSurvivesReload] : failed: caught error: "personalInstanceAlreadyRegistered"
	 Executed 12 tests, with 1 failure (1 unexpected) in 4.908 (4.909) seconds
	 Executed 12 tests, with 1 failure (1 unexpected) in 4.908 (4.909) seconds
	 Executed 12 tests, with 1 failure (1 unexpected) in 4.908 (4.910) seconds
adjust-second.log
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAdjustTests.swift:320: error: -[AppTests.AgentTrustPackageAdjustTests testGatewayPolicyManagementIsOwnerOnlyAndExploreContractsAreExplicit] : XCTAssertEqual failed: ("Optional(CellBase.ValueType.list([CellBase.ValueType.string("rw--")]))") is not equal to ("Optional(CellBase.ValueType.list([CellBase.ValueType.string("rw--")]))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAdjustTests.swift:320: error: -[AppTests.AgentTrustPackageAdjustTests testGatewayPolicyManagementIsOwnerOnlyAndExploreContractsAreExplicit] : XCTAssertEqual failed: ("Optional(CellBase.ValueType.list([CellBase.ValueType.string("rw--")]))") is not equal to ("Optional(CellBase.ValueType.list([CellBase.ValueType.string("rw--")]))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAdjustTests.swift:320: error: -[AppTests.AgentTrustPackageAdjustTests testGatewayPolicyManagementIsOwnerOnlyAndExploreContractsAreExplicit] : XCTAssertEqual failed: ("Optional(CellBase.ValueType.list([CellBase.ValueType.string("rw--")]))") is not equal to ("Optional(CellBase.ValueType.list([CellBase.ValueType.string("rw--")]))")
	 Executed 13 tests, with 3 failures (0 unexpected) in 2.303 (2.306) seconds
	 Executed 13 tests, with 3 failures (0 unexpected) in 2.303 (2.306) seconds
	 Executed 13 tests, with 3 failures (0 unexpected) in 2.303 (2.306) seconds
```

### WP6 — endelig bygg og tester

Kjørt fra `CellScaffold`, direkte fra shell etter regel 10, uten `arch`-prefiks. De tre påkrevde klassene og AIGateway-regresjonene er grønne. **Full bundle er ikke påkrevd i WP6 og er ikke kjørt. Swift Testing-mål dekkes ikke av denne XCTest-banen.** Ingen live modell eller eksternt nettverk brukes i de nye testene; fetch-positivkontrollen og avvisningene bruker injisert URLProtocol.

```text
$ swift build --disable-sandbox --build-tests
Build complete! (10.93s)
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAdjustTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.507 (0.508) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.507 (0.508) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.507 (0.509) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.126 (0.127) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.126 (0.127) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.126 (0.127) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.331 (0.332) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.331 (0.332) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.331 (0.333) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AIGatewayCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.132 (0.134) seconds
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.132 (0.134) seconds
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.132 (0.135) seconds
```

Resultat: **14/14 justering + 17/17 WebFetch + 16/16 pakke + 49/49 AIGateway = 96 tester, 0 feil.** De tre påkrevde klassene utgjør 47 grønne tester.

De 14 justeringstestene dekker (a)–(f), faktisk transport-positivkontroll og 0 requests etter domene-fjerning, wildcard/apex/port-delmengder, førstegangsregelen ved manglende/tom ceiling, reload uten gjenåpning, uendret pakke/ceiling ved avslag, idempotens, persisterbart snapshot for begge måltyper, hele flåten validert før skriving, godkjenningslabel/flagget med defensiv fixture-lesing, per-provider policy-data i digest samt strict Explore og gateway-eierkontroll.

Explore-audit er kjørt som ferdigheten krever. Uendret CellProtocol-kilde gir 305 komplette kontrakter / 316 handler-operasjoner / 7 feil / 19 advarsler. De 7 feilene ligger i eksisterende `CellApple/EntityRadar/EntityScannerCell.swift` (2) og `CellApple/PurposeAndInterest/Cells/PerspectiveCell+Entities.swift` (5). Avgrenset audit av `Sources/App/Cells/AgentTrustPackage` og `Sources/App/Cells/AI` gir 30 komplette / 47 operasjoner / 17 feil; alle feilene ligger i uendrede `AIAssistantThreadCell.swift` (11) og `LocalLLMGatewayCell.swift` (6), ingen i WP6-filene. Statisk audit er ikke en full runtime-kontraktstest; den nye strict-Explore-testen er grønn. Rå JSON-rapporter og kjørelogger ligger i `/private/tmp/wp6-justering/`.

### WP6 — endrede filer

- `CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift`
- `CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageContract.swift`
- `CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageAdjustment.swift` (ny)
- `CellScaffold/Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift`
- `CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift`
- `CellScaffold/Tests/AppTests/AgentTrustPackageAdjustTests.swift` (ny)
- `CellScaffold/Tests/AppTests/AIGatewayCellTests.swift`
- `P/contract/agent_trust_package_contract_v0.json`, `P/TESTRESULT.md`, `P/STATUS.md`

## WP6 — sluttmelding

WP6 — justering er **levert** for `purpose://candidate.tillitspakke-agentflaate.justering`. Eierens tre justeringshandlinger skriver ceiling-data til målcellene og regenererer pakken. Utvidelse og ugyldige mønstre avvises før skriving med typed grunn; digest og WebFetch-ceiling er uendret ved slike avslag. Førstegangsregelen, whitelist-speiling, defensivt `hasChangesSinceApproval` og den eksakte endret-etter-godkjenning-labelen er implementert. Ingen WP7-godkjenning eller startport er implementert.

**Bygg grønt. 96/96 målrettede XCTest-tester grønne (47/47 i de tre påkrevde klassene).** Full bundle er ikke påkrevd/kjørt i WP6; Swift Testing er ikke dekket. Kjente Explore-auditfunn ligger i uendrede filer. Lagringen følger WP5s per-instans resolver-snapshot; identisk SET gir stabil digest og fler-celle-skriving er ikke en distribuert transaksjon. Én WP6-linje er lagt til STATUS. Ingen git-kommandoer er kjørt.


## Godkjenning <a id="godkjenning"></a>

purposeRef: `purpose://candidate.tillitspakke-agentflaate.godkjenning`. Kun WP7.

### WP7 — baseline før endring

Kjørt etter regel 9–10 fra CellScaffold. Ingen arch-prefiks.

```text
$ swift build --disable-sandbox --build-tests
Build complete! (19.08s)
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.129 (0.130) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.129 (0.130) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.129 (0.130) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAdjustTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.482 (0.483) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.482 (0.483) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.482 (0.484) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.435 (0.436) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.435 (0.436) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.435 (0.437) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AIGatewayCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.297 (0.304) seconds
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.297 (0.304) seconds
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.297 (0.305) seconds
```

96 eksisterende tester / 0 feil. Ny klasse: 0 tester før implementasjon. Fullbundle sammenlignes med WP0c (2046 tester, 46 røde testnavn); siste fullkjøring WP5 hadde 2101 tester og samme 46 navn. Swift Testing dekkes ikke av direkte XCTest.

### WP7 — bygg-/testrettinger underveis

Første byggforsøk ble startet fra HAVEN-roten og fant ingen Package.swift. Neste forsøk brukte riktig CellScaffold-cwd og regel 10. Nye typefeil (intern Permission-property, FlowElement-innholdstype og Dictionary-inferens) ble rettet. Ett bygg ble ugyldig fordi AIGateway-kilden ble endret mens kompileringen pågikk; senere bygg kjøres med kildene i ro. Testfixturen manglet deretter `deterministicMode` og brukte feil responsfelt; dette ble rettet uten å endre testkrav.

Første kjørbare WP7-bundle: 15 tester / 2 feil, begge fra AIGateway-responsen. Porten nektet, men typed grunn ble satt i feil catch-gren og nådde ikke responsen. Grunnen settes nå i `invokeRejected`-grenen og returneres også som `status=denied, reason, code` gjennom SET-flaten. Eksisterende regresjoner fant dessuten to forventninger som WP7 endrer: manifestet har nå 5 operasjoner (4 keypaths; bindingen har GET og SET), og approvalLabel er «Ikke godkjent», ikke WP7-placeholder. De eksakte kontrollene er oppdatert; ingen tester er fjernet eller svekket.

```text
approval-first.log
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageApprovalTests.swift:308: error: -[AppTests.AgentTrustPackageApprovalTests testGatewayStartPortDeniesBeforeCredentialsAndDetectsPolicyChanges] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(App.AgentTrustApprovalDenial.notApproved)")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageApprovalTests.swift:318: error: -[AppTests.AgentTrustPackageApprovalTests testGatewayStartPortDeniesBeforeCredentialsAndDetectsPolicyChanges] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(App.AgentTrustApprovalDenial.digestMismatch)")
	 Executed 15 tests, with 2 failures (0 unexpected) in 2.425 (2.426) seconds
	 Executed 15 tests, with 2 failures (0 unexpected) in 2.425 (2.426) seconds
	 Executed 15 tests, with 2 failures (0 unexpected) in 2.425 (2.430) seconds
first-AIGatewayCellTests.log
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AIGatewayCellTests.swift:593: error: -[AppTests.AIGatewayCellTests testPurposeBoundCellHasOneGrantAndRejectsMixedGrantAgreement] : XCTAssertEqual failed: ("5") is not equal to ("4")
	 Executed 49 tests, with 1 failure (0 unexpected) in 1.122 (1.124) seconds
	 Executed 49 tests, with 1 failure (0 unexpected) in 1.122 (1.124) seconds
	 Executed 49 tests, with 1 failure (0 unexpected) in 1.122 (1.125) seconds
first-AgentTrustPackageCellTests.log
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageCellTests.swift:104: error: -[AppTests.AgentTrustPackageCellTests testFixtureFleetProjectsActualTemplatesAndHonestMissingSources] : XCTAssertTrue failed
	 Executed 16 tests, with 1 failure (0 unexpected) in 1.357 (1.358) seconds
	 Executed 16 tests, with 1 failure (0 unexpected) in 1.357 (1.358) seconds
	 Executed 16 tests, with 1 failure (0 unexpected) in 1.357 (1.358) seconds
```

### WP7 — grønt bygg og målrettede tester før ekstra persistensregresjon

```text
$ swift build --disable-sandbox --build-tests
Build complete! (27.09s)
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.712 (0.713) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.712 (0.713) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.712 (0.715) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.118 (0.118) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.118 (0.118) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.118 (0.119) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAdjustTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.445 (0.445) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.445 (0.445) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.445 (0.446) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.276 (0.277) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.276 (0.277) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.276 (0.277) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AIGatewayCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.106 (0.107) seconds
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.106 (0.107) seconds
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.106 (0.108) seconds
```

**17 nye + 96 eksisterende = 113 tester / 0 feil.** De fire påkrevde klassene har 64 tester / 0 feil. Testene bruker virkelig CellProtocol-signering og EntityAnchor-commit mot midlertidig testlagring. URLProtocol/provider/credential-butikker er injiserte fixtures; ingen live modell eller eksternt nettverk.

### WP7 — avsluttende persistensgjennomgang

Første fullkjøring ble avbrutt med SIGINT (exit 130) etter at gjennomgangen fant en manglende avvisningsgren: en persistent WP7-celle kunne kvittere suksess hvis `defaultCellResolver` manglet eller ikke støttet den eksisterende snapshot-committen. Felles persistenshjelper returnerer nå feil i dette tilfellet. Flåtebinding rulles tilbake ved manglende lagring; aktive bindinger kan ikke forsvinne gjennom en mislykket unbind. Godkjenning aktiveres ikke ved mislykket snapshot-lagring. Stopp som ikke kan lagres returnerer `persistence_failed` og beholder avvisning i minnet; det er ingen påstand om varig tilbakekalling når lagringen feiler. Ephemeral preview-/testceller lover ikke varig cellelagring.

Den eksisterende nye persistensregresjonen dekker nå både resolver uten lagringsbackend og helt manglende resolver. Fullkjøringen nedenfor startes på nytt med den siste bundlen; den avbrutte kjøringen er ikke brukt som sluttresultat. Logg: `/private/tmp/wp7-godkjenning/full-bundle-interrupted.log`.

### WP7 — implementasjon og verifisert grense

- `trustPackage.approve {packageDigest}` krever eksakt `rw-s`-tilgang og eierens signeringsbevis. Kildene regenereres før digest-sammenligningen; tom/ikke-avledet pakke gir `package_not_derived`, feil eller gammel digest gir `digest_mismatch`. Etter den asynkrone committen re-leses kildene også før godkjenningen aktiveres.
- Snapshotet `{schema, fleetID, packageDigest, approvedAt, policyDigests}` kodes kanonisk (sorterte nøkler, uten whitespace, RFC3339 UTC-tid). Hele JSON-teksten ligger i `Agreement.name`, altså inne i bytes som `Contract.ownerSignedSnapshot` signerer. Agreement har **ingen Grants og ingen conditions**. Issuer = subject = eier; domain = eierens EntityAnchor-domene. Dette bruker eksisterende signering/verifisering i CellProtocol, ingen ny kryptografi.
- `signedAgreementEntity.commit` skriver den immutable recorden og signert persistenskvittering gjennom faktisk EntityAnchor. Returstatus må være `persisted`, og `AgreementProductionVerification.verifyEntityRecord` må verifisere record, receipt, eiernøkkel og bindinger. Cellens `trustPackage.approved` lagrer `digest`, `approvedAt`, `recordRef`, `signatureValid` og tilhørende record/receipt. GET er `r---`, kun bevist eier. Ved hver GET verifiseres signaturene på nytt; et lagret bool-flagg er aldri bevis. Godkjenningsrecorden filtreres ut av Contract-projeksjonen så signeringen ikke endrer sin egen pakke-digest.
- Snapshotets `policyDigests` er indeksert på celleinstansens UUID og binder konkret celletype, eiernøkkel-fingerprint, eksakte template-keypaths og begge permission-gruppene samt hele effekt-policyen/ceiling-dataene. Tilfeldige Grant-/Permission-deskriptor-UUIDer påvirker ikke digesten. WebFetch inkluderer blant annet `maxBytes` og `followRedirects`; disse detaljene finnes ikke alle i den kompakte WP1-pakkeprojeksjonen, men bindes i det signerte WP7-snapshotet. En bytegrense-endring nektes derfor selv når den kompakte `packageDigest` er uendret.
- Eierstyrte GET/SET-data er `webFetch.fleetBinding` på WebFetch og `ai.fleetBinding` på PurposeBoundAIGateway. SET er `rw--`, GET `r---`; payload `{fleetID, endpoint}` bruker pakkecellens UUID og `cell:///AgentTrustPackage` i dette ene scaffoldet. Kun eieren kan bevisst fjerne binding med `null`. Ugyldig lagret binding feiler dekoding og blir aldri stille ubundet. Binding lagres i eksisterende per-instans Codable/resolver-snapshot. Persistente celler krever vellykket snapshot-lagring; en mislykket unbind rulles tilbake.
- Bundne kall bruker vertscellens verifiserte runtime-eier til et eierbeskyttet resolver-oppslag av `trustPackage.approved`. Det gis ingen ny rett til invokasjonens requester. Pakketype, flåte-ID, eier og signert record må stemme. Gjeldende regenererte pakke og policyDigests må stemme, inkludert denne celleinstansen. Porten ligger før credential-, cache-, kvote- og provider-/fetch-nettverksbanen; WebFetch bruker samme ceiling-snapshot som ble kontrollert. En ubundet celle beholder den eksisterende autorisasjons-/ceiling-banen.
- Typede startavslag er `package_not_approved`, `package_digest_mismatch`, `package_unavailable` og `package_approval_invalid`. Manglende/feil flåte, utilgjengelig resolver/pakkecelle, busy read eller manglende runtime-eierbevis feiler lukket. AIGateway har additivt `trustPackageDenial` på intern responsmodell og `status=denied, reason, code` på SET-responsen. Ingen signert action-/effect-kvittering er innført (WP9 er fortsatt utenfor).
- `trustPackage.fleet.stop {}` er eierstyrt `rw--` med samme eksplisitte signeringsbevis. Den beholder recorden, setter `revokedAt` idempotent og trekker aktiv godkjenning. Ny approve beholder tidligere record i `approvalHistory`. Signaturens historiske gyldighet beholdes etter stopp; den gir ingen startadgang. Stopp stenger nye kall, men kansellerer ikke en effekt som allerede er tatt inn. Det kreves fungerende persistent resolver-lagring for å kvittere en varig endring; det er ingen distribuert transaksjon mellom EntityAnchor og cellens snapshot.
- `approvalLabel` viser «Ikke godkjent», «Godkjent <tid>» eller «Ikke godkjent — pakken er endret etter siste godkjenning». `statusLabel` viser «Godkjent <tid>» eller «Avvik — endret etter godkjenning» når disse tilstandene gjelder; eksisterende tom-/utkast-/ikke-avledet-tilstander beholdes ellers. `hasChangesSinceApproval` inkluderer de fulle policy-digestene. Ingen skeleton-struktur er endret.

De **17 nye testene** dekker alle (a)–(h), signaturmanipulering, ekte EntityAnchor-record/receipt, gammel digest uten eksplisitt regenerering, manglende archive, full WebFetch-ceiling, tilbakekalt historikk og reload, fremmed/offentlig/feil-vault requester også med debug-bypass, delegert fetch som fortsatt krever separat Contract, ukjent flåte/utilgjengelig pakke, forfalsket approval-bool, ugyldig lagret binding, feilet persistent unbind, strict Explore og faktisk AIGateway provider-positivkontroll. Ingen eksisterende test er fjernet eller svekket.

Explore-audit: uendret CellProtocol gir 305 komplette / 316 handler-operasjoner / 7 feil / 19 advarsler (samme tidligere EntityScanner/Perspective-funn). Avgrenset CellScaffold-audit for AgentTrustPackage, AI og WebKnowledge gir 35 komplette / 92 handler-operasjoner / 17 feil / 40 advarsler. Alle 17 feil ligger i uendrede `AIAssistantThreadCell.swift` og `LocalLLMGatewayCell.swift`. Denne statiske auditen kan ikke utlede alle beregnede keypaths; strict runtime-Explore-testen for de nye operasjonene er grønn. Rårapporter ligger i `/private/tmp/wp7-godkjenning/explore-*.log` og `explore-scaffold-final.json`.

### WP7 — endelig målrettet kjøring etter persistensretting

```text
$ swift build --disable-sandbox --build-tests
Build complete! (20.83s)
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.705 (0.706) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.705 (0.706) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.705 (0.708) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.116 (0.117) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.116 (0.117) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.116 (0.117) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAdjustTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.458 (0.459) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.458 (0.459) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.458 (0.459) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.286 (0.287) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.286 (0.287) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.286 (0.288) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AIGatewayCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.104 (0.105) seconds
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.104 (0.105) seconds
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.104 (0.106) seconds
```

**113/113 målrettede XCTest-tester grønne (64/64 i de fire påkrevde klassene).** Swift Testing dekkes ikke av direkte XCTest.

### WP7 — endrede filer

- `CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageApproval.swift` (ny)
- `CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift`
- `CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageContract.swift`
- `CellScaffold/Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift`
- `CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift`
- `CellScaffold/Sources/App/Cells/AI/AIGatewayModels.swift`
- `CellScaffold/Tests/AppTests/AgentTrustPackageApprovalTests.swift` (ny)
- `CellScaffold/Tests/AppTests/AgentTrustPackageCellTests.swift`
- `CellScaffold/Tests/AppTests/AIGatewayCellTests.swift`
- `P/contract/agent_trust_package_contract_v0.json`, `P/TESTRESULT.md`, `P/STATUS.md`

Ingen CellProtocol-kilde, skeleton-struktur, deployment eller git er endret/kjørt i WP7. Book/WP8–WP13 er utenfor denne slicen.

### WP7 — full XCTest-bundle og baseline-sammenligning

Kjørt direkte fra `CellScaffold` etter regel 10 med den endelige bundlen. Exit 1 skyldes de eksisterende røde testene. **2133 tester / 11 hoppet over / 46 røde testnavn / ingen nye navn.** WP0c hadde 2046 tester og de samme 46 røde navnene; WP5 hadde 2101 og de samme 46. WP6 la til 15 tester (14 Adjust + én AIGateway-regresjon); WP7 legger til 17. Fullbundlen er fortsatt rød med 151 feilrapporter, hvorav 9 unexpected.

```text
$ xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
Test Suite 'CellsContainerPackageTests.xctest' failed at 2026-09-09 01:04:57.722.
	 Executed 2133 tests, with 11 tests skipped and 151 failures (9 unexpected) in 785.340 (785.448) seconds
Test Suite 'All tests' failed at 2026-09-09 01:04:57.725.
	 Executed 2133 tests, with 11 tests skipped and 151 failures (9 unexpected) in 785.340 (785.451) seconds
```

Navnesammenligning, maskinelt fra de faktiske `Test Case … failed`-linjene i WP0c og WP7:

```text
WP0c failed names: 46
WP7 failed names: 46
newFailedNames: []
baselineNamesNowGreen: []
sourceHashesUnchanged: true
```

**151 mot WP0cs 148 feilrapporter:** eneste endrede assertion-antall er `PortholeConfigurationLoadingTests.testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction`, fra 2 til 5. Dette er nøyaktig samme kjente +3-variasjon som WP5s fullkjøring (og dokumentert i WP2). Ingen Mermaid-/Porthole-kilde er endret i WP7. De fem ekte feilrapportene fra denne kjøringen:

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:968: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertTrue failed - Expected webview render to succeed: [CellBase.ValueType.string("Render timed out after 2000ms")]
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:969: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertNotNil failed
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:993: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertEqual failed: ("Optional(CellBase.ValueType.bool(false))") is not equal to ("Optional(CellBase.ValueType.bool(true))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:994: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertTrue failed - Expected rendered preview HTML in projected bootstrap state.
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/PortholeConfigurationLoadingTests.swift:998: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertEqual failed: ("Render timed out after 2000ms") is not equal to ("")
```

Alle 17 nye godkjenningstester samt WebFetchCeilingTests, AgentTrustPackageAdjustTests, AgentTrustPackageCellTests og AIGatewayCellTests er også grønne inne i fullbundlen. Ingen ny kildeendring ble gjort etter siste bygg/teststart; SHA-256 for de ni endrede Swift-filene er kontrollert før og etter fullkjøringen. Full logg og sammenligning: `/private/tmp/wp7-godkjenning/full-bundle.log`, `comparison.json`, `tested-source-hashes.json`. Nødvendige kjørings- og avviksdata er bevart her. **Swift Testing-mål dekkes ikke av denne XCTest-banen.**

## WP7 — sluttmelding

WP7 — godkjenning + startport er **levert** for `purpose://candidate.tillitspakke-agentflaate.godkjenning`. Eierens approve signerer et subject-bundet snapshot med eksisterende `Contract.ownerSignedSnapshot` og verifisert EntityAnchor-commit. `trustPackage.approved` er eierbeskyttet, persisterbar og re-verifisert ved lesing. `fleet.stop` beholder tilbakekallingshistorikk. Eierstyrt flåtebinding aktiverer fail-closed startport på WebFetch og PurposeBoundAIGateway før credential-/nettverksbanen; endret ceiling/policy krever ny godkjenning. Ubundne celler beholder eksisterende oppførsel. Pakken og formål gir aldri rettigheter; snapshotet har ingen Grants.

**Bygg grønt. 113/113 målrettede XCTest-tester grønne, inkludert 17 nye. Full bundle: 2133 tester / 11 hoppet over / samme 46 røde navn som baseline / ingen nye; 151 feilrapporter (kjent Mermaid +3), 9 unexpected, 785.451 s.** Fullbundlen er fortsatt rød på baseline-feilene; Swift Testing er ikke dekket.

Kontrakten er oppdatert, og STATUS.md har én WP7-linje. Kun WP7 er utført. Ingen git, deploy, nye Grants fra pakken, ny kryptografi eller WP8–WP13-implementasjon.


## Injeksjon <a id="injeksjon"></a>

### WP8 — fullført etter gjenopptakelse 2026-09-09

purposeRef: `purpose://candidate.tillitspakke-agentflaate.skal-ikke.modell-utvider`. **Bestått.** Tidligere blocked-kjøring nedenfor er historikk; regel 11-forhåndssjekken og ny grønn baseline står også nedenfor.

`AgentTrustPackageAntiPurposeTests.testModelOutputRemainsProposalWithoutToolLoopAndLogsFourOwnerDenials` leser alle fire tekstene direkte fra `neg-injection-outputs.json`. En injisert fixture-provider returnerer dem gjennom produksjonens `PurposeBoundAIGatewayCell.invokePurposeBound` → startport → policy/autorisasjon → AIGateway-motor → provider → respons. Pakken er først generert og reelt eiergodkjent med EntityAnchor. Ingen kopiert modellparser eller ny tool-løkke.

Hver faktisk returtekst blir neste prompt med nytt, eksplisitt beregnet intent. Den originale `AIGatewayInvokeRequest` og begge requestene mottatt av provideren sammenlignes som kanoniske bytes mot sine avtalte input. `tools` finnes ikke og `toolPolicy` er nil. Åtte provider-kall totalt er nøyaktig to per fixture; ingen skjult ekstra modell-/verktøyrunde. Bare prompt og den tilhørende intent-bindingen endres ved den bevisste neste invokasjonen.

En separat signerende testidentitet representerer agenten som handler på modellens forslag. Den får aldri eierens nøkkel. Modellinvokasjonene er autorisert av scaffold-eieren; etterfølgende forslag kjøres som agenten gjennom ekte SET-grenser. For hver tekst: `trustPackage.adjust.whitelist` med returteksten kaster `ownerRequired`; et gyldig, utvidet `webFetch.ceiling.set` gir `owner_required`; `web.fetch` gir `access_denied`. Ceiling-digest over den faktisk leste, fullstendige ceiling-en og regenerert pakke-digest forblir like før/etter hver rad. Ingen WebFetch-nettverksrequest eller ScopedCredential-oppslag fra agenten. Providerens fixture-store får bare aliaset `fixture-provider`, aldri tekstens `anthropic`.

**S — testavdekket minimal tetting:** WP5/WP7 returnerte avslag, men hadde ingen lagret liste/teller for avviste justeringer. `trustPackage.state.deniedAttempts` er derfor lagt til: monoton, trådsikret Int-teller for `trustPackage.adjust.*`-SET som avvises av eierbeviset, med metning ved Int.max. Ingen offentlig reset/SET; gamle snapshots starter på 0. Den inkluderer ikke WebFetch-cellens separate avvisningsresponser. Testen krever 0 → 1 → 2 → 3 → **4**, samt 4 etter regenerering og Codable-reload, lesing av den eksakte underkeypathen og avvist reset. State har oppdatert Explore-skjema og testen kjører i strict-modus.

Fire celleutstedte hendelser inneholder bare `action`, `reason` og `deniedAttempts`. Testen teller de fire og kontrollerer det eksakte feltsettet; ingen rå forslag, identiteter eller hemmeligheter inngår i dette hendelsesinnholdet. Telleren kodes i eksisterende snapshot, og eksisterende persistenshjelper forsøkes etter avslag. Ved lagringsfeil beholdes avslag og teller i minnet; testen beviser snapshot/reload, ikke varig lagring ved I/O-feil. Dette er ingen signert receipt eller WP10-auditlogg.

#### Rødt før produksjonsendring

Etter retting av testens byggfeil (`ValueType.integer` og faktisk digest-API) og tillegg av tom `reach` i den ekstra, kanoniserte fixture-varianten, kjørte begge tester mot uendret produksjonskode. Målt **2 tester / 9 assertion-feil / 0 unexpected**. Syv teller-asserts feilet fordi feltet manglet; de to øvrige hører til pakke-tilstanden nedenfor. Ingen eksisterende tester er svekket.

```text
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAntiPurposeTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 2 tests, with 9 failures (0 unexpected) in 1.507 (1.508) seconds
	 Executed 2 tests, with 9 failures (0 unexpected) in 1.507 (1.508) seconds
	 Executed 2 tests, with 9 failures (0 unexpected) in 1.507 (1.510) seconds
```

Ekte feillinjer for telleren:

```text
AIInvokeC/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAntiPurposeTests.swift:94: error: -[AppTests.AgentTrustPackageAntiPurposeTests testModelOutputRemainsProposalWithoutToolLoopAndLogsFourOwnerDenials] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.integer(0))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAntiPurposeTests.swift:141: error: -[AppTests.AgentTrustPackageAntiPurposeTests testModelOutputRemainsProposalWithoutToolLoopAndLogsFourOwnerDenials] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.integer(1))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAntiPurposeTests.swift:141: error: -[AppTests.AgentTrustPackageAntiPurposeTests testModelOutputRemainsProposalWithoutToolLoopAndLogsFourOwnerDenials] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.integer(2))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAntiPurposeTests.swift:141: error: -[AppTests.AgentTrustPackageAntiPurposeTests testModelOutputRemainsProposalWithoutToolLoopAndLogsFourOwnerDenials] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.integer(3))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAntiPurposeTests.swift:141: error: -[AppTests.AgentTrustPackageAntiPurposeTests testModelOutputRemainsProposalWithoutToolLoopAndLogsFourOwnerDenials] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.integer(4))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAntiPurposeTests.swift:148: error: -[AppTests.AgentTrustPackageAntiPurposeTests testModelOutputRemainsProposalWithoutToolLoopAndLogsFourOwnerDenials] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.integer(4))")
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAntiPurposeTests.swift:153: error: -[AppTests.AgentTrustPackageAntiPurposeTests testModelOutputRemainsProposalWithoutToolLoopAndLogsFourOwnerDenials] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.integer(4))")
```

Første kjøring etter tetting hadde én ekstra feil: hendelser sendt med den avviste requesteren manglet `feed`-rettighet og nådde ikke eierens abonnement. Cellen bruker nå eksisterende `makeCellOwnedFlowEmitterForRuntimeBinding` under runtime-installasjon, uten å gi agenten noen feed-Grant. Ekte feillinje og resultattall før denne rettingen:

```text
AIInvokeStarted correlationId=ni/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAntiPurposeTests.swift:163: error: -[AppTests.AgentTrustPackageAntiPurposeTests testModelOutputRemainsProposalWithoutToolLoopAndLogsFourOwnerDenials] : Asynchronous wait failed: Exceeded timeout of 2 seconds, with unfulfilled expectations: "four redacted owner-denial events".
```
```text
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAntiPurposeTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 2 tests, with 1 failure (0 unexpected) in 3.805 (3.806) seconds
	 Executed 2 tests, with 1 failure (0 unexpected) in 3.805 (3.806) seconds
	 Executed 2 tests, with 1 failure (0 unexpected) in 3.805 (3.808) seconds
```

#### Endelig bygg og målrettet kjøring

Alle kommandoer fra `CellScaffold`, etter regel 10, uten `arch`-prefiks:

```text
$ swift build --disable-sandbox --build-tests
Build complete! (49.87s)
```
```text
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAntiPurposeTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.485 (0.485) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.485 (0.485) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.485 (0.486) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.124 (0.125) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.124 (0.125) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.124 (0.125) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.727 (0.728) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.727 (0.728) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.727 (0.729) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAdjustTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.474 (0.475) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.474 (0.475) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.474 (0.475) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.294 (0.295) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.294 (0.295) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.294 (0.296) seconds
```

**36/36 i de tre bestilte klassene; 66/66 med de to ekstra celle-/justeringsregresjonene.** De to ekstra klassene er kjørt fordi tettingene berører pakkecellens SET, regenerering, state og snapshot. Ingen full bundle er påkrevd i WP8, og ingen full bundle er kjørt. Direkte XCTest dekker ikke Swift Testing-mål. Ingen live modell eller eksternt nettverk; kun fixture-provider, fixture-secret-store og URLProtocol.

Explore: pakkecellens siste statiske audit gir 4 komplette / 4 handler-operasjoner / 0 feil / 0 varsler. Strict runtime-testen er grønn. Uendret CellProtocol gir 305 komplette / 316 handler-operasjoner / 7 feil / 19 varsler, samme kjente funn som WP7; de er ikke rapportert som grønne eller rettet i WP8. Rålogger og audit-JSON ligger i `/private/tmp/wp8-antiformaal-rerun/`.

### Historikk — tidligere blocked-kjøring og ny baseline


purposeRef: `purpose://candidate.tillitspakke-agentflaate.skal-ikke.modell-utvider`. Kun WP8. **blocked — WP5–WP7-kildene mangler i den angitte CellScaffold-arbeidskopien.** Kontrollert 2026-09-09 før kodeendring.

### WP8 — baseline og kildeavvik

`handoff/README.md` regel 9–10, WP8 i PLAN, FORMAALSSPEC §1/§2/§5, kontrakten, begge negative fixtures og WP5–WP7-resultatene er lest. [Kandidatgren-overleveringen](handoff/KANDIDATGREN.md) sier eksplisitt at post 0 returnerte CellScaffold til originalgrenen, og at WP8–WP10 trenger PDD-koden på kandidatgrenen. Notatet oppgir kandidatcommit `1dbdee23f5272a3485a4c6b8263c84c4351eaf28`; dette er dokumentkilden, ikke en ny git-verifikasjon.

Faktisk fil-/innholdskontroll fra `CellScaffold`:

```text
Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift: MISSING
Sources/App/Cells/AgentTrustPackage/AgentTrustPackageApproval.swift: MISSING
Tests/AppTests/WebFetchCeilingTests.swift: MISSING
Tests/AppTests/AgentTrustPackageApprovalTests.swift: MISSING
Tests/AppTests/AgentTrustPackageAntiPurposeTests.swift: MISSING
Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift: webFetch.ceiling.set: ABSENT
Sources/App/Cells/AI/AIGatewayCell.swift: ai.fleetBinding: ABSENT
```

Søk etter `*AgentTrustPackage*` i HAVENs arbeidsmapper (med `.git`, `.build`, `.swiftpm` og `node_modules` utelatt) fant bare WP1-modellen og WP1-testen i CellProtocol. Ingen alternativ arbeidsmappe med CellScaffolds PDD-kilder ble funnet.

Bygg før endring, direkte fra `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold`, uten `arch`-prefiks. Alle tre direkte XCTest-kommandoer returnerte exit 0, men **ingen av de etterspurte testklassene finnes i den nybygde bundlen**. Null utførte tester er ikke grønn WP8 eller grønn regresjon.

```text
$ swift build --disable-sandbox --build-tests
Build complete! (81.97s)
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAntiPurposeTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.002) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
```

**Målt baseline: 0 tester / 0 feilrapporter; WP8 og de to påkrevde regresjonsklassene er blocked.** WP7s tidligere 17 + 17 tester er historisk evidens og gjelder ikke denne arbeidskopien. Rålogger: `/private/tmp/wp8-antiformaal/baseline-build.log`, `baseline-AgentTrustPackageAntiPurposeTests.log`, `baseline-WebFetchCeilingTests.log`, `baseline-AgentTrustPackageApprovalTests.log`, `source-availability.log`.

De fire `modelOutputs` i `neg-injection-outputs.json` er lest, men ikke kjørt som modell-output gjennom en WP5–WP7-produksjonsbane. Digest-/request-uendret, eieravvisning og fire loggede avslag er derfor **ikke verifisert**. Ingen ny testfil, fixture-provider eller `deniedAttempts`-tetting er skrevet: manglende forgjengerkode er en arbeidskopiblokkering, ikke et testavdekket implementasjonshull. Kun testdokumentasjon er endret.


### WP8 — gjenopptatt 2026-09-09: forhåndssjekk og baseline

Forrige blocked-kjøring over er historikk. Regel 11 er nå oppfylt: seks filer i `Sources/App/Cells/AgentTrustPackage/`, `WebFetchCeilingTests.swift` finnes og eksplisitt pålagt grenlesing viste `pdd/tillitspakke-agentflaate`. Ingen andre git-kommandoer. Ny `AgentTrustPackageAntiPurposeTests.swift` finnes ikke før endring; nulltester brukes ikke som baseline.

Bygg/test fra CellScaffold etter regel 10, før endringer:

```text
$ swift build --disable-sandbox --build-tests
Build complete! (24.20s)
$ xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.173 (0.174) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.173 (0.174) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.173 (0.176) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.766 (0.767) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.766 (0.767) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.766 (0.768) seconds
```

Baseline: 34 tester, 0 feil. Full bundle er ikke påkrevd og kjøres ikke i WP8. Direkte XCTest dekker ikke Swift Testing. Rålogger: `/private/tmp/wp8-antiformaal-rerun/`.

## Pakke gir ikke rett <a id="pakke-gir-rett"></a>

### WP8 — fullført etter gjenopptakelse 2026-09-09

purposeRef: `purpose://candidate.tillitspakke-agentflaate.skal-ikke.pakke-gir-rett`. **Bestått.** Tidligere blocked-kjøring nedenfor er historikk.

`AgentTrustPackageAntiPurposeTests.testHandcraftedApprovedPackageCannotGrantFetchOrCredentialsAndIsNotDerived` manipulerer eksisterende snapshot-JSON og dekoder den gjennom produksjonens `AgentTrustPackageCell.init(from:)`. Den legger hele `neg-extra-grant.package.json` i et `package`-felt og påstår godkjenning med `approved.digest` / `signatureValid=true`. Ingen produksjons-API for import eller utvidede rettigheter er opprettet.

Originalfixturen påstår en `credentials`-Grant, ikke en `web.fetch`-Grant. Testen kjører derfor også en avledet testvariant med eksplisitt `web.fetch rw--`-Grant og kant, aktuell fleetID, tom `reach` (originalen mangler dette påkrevde WP1-feltet) og korrekt beregnet SHA-256-digest. Originalfilen er uendret og lastes også som den er. Dermed dekker testen både den oppgitte credential-påstanden og brukerens konkrete krav om en fetch-rett som bare finnes i pakken.

Begge variantene gir `access_denied` for faktisk `web.fetch` fra agentidentiteten, med og uten credential-alias, på en ellers tillatt vert. `validateAccess` bekrefter at agenten mangler rettigheten. Før manipulering viser en eier-fetch med ekte godkjenning at mål og nettverksfixture virker. Etter eksplisitt eierregenerering og ny ekte godkjenning avvises agenten fortsatt; først en reell signert WebFetch-Agreement gir vellykket fetch. Den gir fortsatt ikke credential-rett (`credential_not_granted`). Ingen nettverk eller credential-oppslag skjer i de avviste angrepskallene.

**Testavdekket minimal tetting:** Snapshot-dekoderen ignorerte det innlagte `package`-feltet. Avslagene holdt allerede, men state viste «Avvik — endret etter godkjenning» og approve ga `digest_mismatch`, fremfor den avtalte «ikke avledet» / `package_not_derived`. Ekte feillinjer før produksjonsendring:

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAntiPurposeTests.swift:202: error: -[AppTests.AgentTrustPackageAntiPurposeTests testHandcraftedApprovedPackageCannotGrantFetchOrCredentialsAndIsNotDerived] : XCTAssertTrue failed - Optional(CellBase.ValueType.string("Avvik — endret etter godkjenning"))
/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/Tests/AppTests/AgentTrustPackageAntiPurposeTests.swift:203: error: -[AppTests.AgentTrustPackageAntiPurposeTests testHandcraftedApprovedPackageCannotGrantFetchOrCredentialsAndIsNotDerived] : XCTAssertEqual failed: ("Optional(CellBase.ValueType.string("digest_mismatch"))") is not equal to ("Optional(CellBase.ValueType.string("package_not_derived"))")
```

Nå setter tilstedeværelse av `package` i snapshot et separat `untrustedStoredPackage`-flagg. Pakken leses aldri som myndighet og den rå JSON-en beholdes ikke. Flagget overlever encode/decode, automatiske state-/approval-lesinger kan ikke fjerne det, state viser «Ikke avledet — kildene kunne ikke verifiseres», og approve gir `package_not_derived`. Bare en vellykket, eksplisitt `trustPackage.regenerate` eller `trustPackage.fleet.set` fra eieren erstatter tilstanden med en projeksjon fra de faktiske kildene. Testen dekker også en ekstra snapshot-reload før status/approve og denne eksplisitte gjenopprettingen. Ingen template, Grant, resolverregel eller WebFetch-/AIGateway-kode er endret.

Ekte `Executed`-linjer fra samme endelige kjøring som under Injeksjon (gjengitt her, ikke ekstra kjøringer):

```text
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAntiPurposeTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.485 (0.485) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.485 (0.485) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.485 (0.486) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.124 (0.125) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.124 (0.125) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.124 (0.125) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.727 (0.728) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.727 (0.728) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.727 (0.729) seconds
```

**Bestilt dekning: 2 nye + 17 WebFetch + 17 Approval = 36 tester, 0 feil.** Totalt 66 med celle-/justeringsregresjonene dokumentert under Injeksjon. Full bundle er ikke påkrevd og er ikke kjørt; Swift Testing er ikke dekket.

### Historikk — tidligere blocked-kjøring


purposeRef: `purpose://candidate.tillitspakke-agentflaate.skal-ikke.pakke-gir-rett`. Kun WP8. **blocked av samme manglende WP5–WP7-kilder.** `neg-extra-grant.package.json` er lest, men kan ikke lastes inn i en AgentTrustPackageCell som mangler fra arbeidskopien. `web.fetch`-avslag på en Grant som bare står i pakken, `statusLabel` med «ikke avledet» og `approve → package_not_derived` er **ikke verifisert**.

De relevante ekte `Executed`-linjene fra samme baseline-kjøring over (gjengitt her, ikke en ekstra kjøring):

```text
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAntiPurposeTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.002) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
```

For å fortsette må de eksisterende WP2–WP7-filene, inklusive blandede endringer i AI/WebFetch og testene, gjøres tilgjengelige i den angitte CellScaffold-arbeidskopien eller i en oppgitt arbeidsmappe. Brukerens «Ingen git» er fulgt; ingen grenbytte, gjeninnføring fra git eller endring i WP1–WP7 er utført. Ny produksjonskode kan først vurderes etter at en reell WP8-test av denne koden avdekker et hull.

**Full bundle er ikke påkrevd i WP8 og er ikke kjørt. Swift Testing-mål dekkes ikke av direkte XCTest.** Ingen live modell, credential-oppslag eller eksterne web.fetch-kall er kjørt.

## WP8 — sluttmelding (historikk: tidligere blocked-kjøring)

WP8 — antiformål er **blocked, ikke levert**: dagens CellScaffold mangler AgentTrustPackageCell, WebFetch-ceiling/flåteport og begge påkrevde regresjonsklassene etter post 0s dokumenterte tilbakebytte. Regel 10-bygget er grønt ((81.97s)); direkte XCTest med hvert av de tre filtrene utførte **0 tester**, så antiformålene er ikke verifisert.

Ekte testutdata og kildeavvik er bevart under `#injeksjon` og `#pakke-gir-rett`. STATUS.md har én WP8-linje. Ingen Swift-kode eller eksisterende tester er endret; ingen git er brukt. Full bundle er ikke påkrevd/kjørt, og Swift Testing er ikke dekket. Gjenopptak krever en arbeidskopi med kandidatens eksisterende WP2–WP7-kode; deretter gjenstår hele WP8-testimplementasjonen og de tre målrettede kjøringene.


## Kvittering <a id="receipt"></a>

purposeRef: `purpose://candidate.tillitspakke-agentflaate.signert-kvittering`. Kun WP9, 2026-09-09.

### WP9 — baseline før endring

Regel 9–10 fulgt: `swift build --disable-sandbox --build-tests` uten `arch`, deretter direkte `xcrun --sdk macosx xctest`. Ingen git.

CellProtocol, cwd `HAVEN/CellProtocol`:

```sh
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest
xcrun --sdk macosx xctest -XCTest CellBaseTests.PurposeBoundExternalActionTests .build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest
```

Ekte bygg-/testutdata (utdrag; full logg i `/private/tmp/wp9-receipts/baseline-cellprotocol-*.log`):

```text
Build complete! (13.77s)
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/IdentityVault.swift:1369: error: -[CellBaseTests.AppleIdentityVaultKeyStorageTests testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns] : failed: caught error: "Creating private key failed with error: Optional(Swift.Unmanaged<__C.CFErrorRef>(_value: Error Domain=NSOSStatusErrorDomain Code=-50 "failed to generate CDSA key" (paramErr: error in user parameter list) UserInfo={numberOfErrorsDeep=0, NSDescription=failed to generate CDSA key}))"
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/IdentityVault.swift:1369: error: -[CellBaseTests.AppleIdentityVaultKeyStorageTests testLegacyEmbeddedPrivateKeyStillSigns] : failed: caught error: "Creating private key failed with error: Optional(Swift.Unmanaged<__C.CFErrorRef>(_value: Error Domain=NSOSStatusErrorDomain Code=-50 "failed to generate CDSA key" (paramErr: error in user parameter list) UserInfo={numberOfErrorsDeep=0, NSDescription=failed to generate CDSA key}))"
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellApple/IdentityVault.swift:610: error: -[CellBaseTests.AppleIdentityVaultKeyStorageTests testScopedSecretDataStaysStableInUnsignedTestHost] : failed: caught error: "unhandledError(status: -50)"
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Tests/CellBaseTests/EntityScannerAgreementSurfaceTests.swift:75: error: -[CellBaseTests.EntityScannerAgreementSurfaceTests testAgreementTemplateExposesOnlyTheApprovedSurface] : XCTAssertTrue failed - EntityScannerCell.agreementTemplate eksponerer nøkler som ikke er gjennomgått: ["radar", "select"]. Legg dem til fasiten i denne testen bare hvis du har vurdert hva en innsluppet motpart kan lese gjennom dem — se F1 i Codex_FixList_NearbyScanner_2026-08-24.md.
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/VerifiableCredentials/Standards/OpenID4VP/OID4VPSignedRequestTrustVerifier.swift:353: error: -[CellBaseTests.OID4VPSignedRequestTrustVerifierTests testVerifiesX509HashSignedRequest] : failed: caught error: "invalidX509CertificateChain"
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/VerifiableCredentials/Standards/OpenID4VP/OID4VPSignedRequestTrustVerifier.swift:348: error: -[CellBaseTests.OID4VPSignedRequestTrustVerifierTests testVerifiesX509SanDNSSignedRequest] : failed: caught error: "invalidX509CertificateChain"
	 Executed 1074 tests, with 8 tests skipped and 6 failures (5 unexpected) in 128.145 (128.221) seconds
	 Executed 1074 tests, with 8 tests skipped and 6 failures (5 unexpected) in 128.145 (128.222) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.003 (0.004) seconds
```

Målt: **1074 tester, 8 hoppet over, 6 feil (5 unexpected)**. Baseline-avvik: tre Apple Keychain/OSStatus -50-feil, EntityScanner-template med `radar`/`select` utenfor fasit, to ugyldige X509-kjeder. Samme seks testnavn som tidligere baseline; de rettes ikke i WP9. Den eksisterende PurposeBoundExternalAction-klassen: 7/0.

CellScaffold, cwd `HAVEN/CellScaffold`:

```sh
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

```text
Build complete! (21.29s)
$ xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
Test Suite 'Selected tests' started at 2026-09-09 01:47:15.334.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-09 01:47:15.335.
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-09 01:47:15.335.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'Selected tests' passed at 2026-09-09 01:47:15.335.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
Test Suite 'Selected tests' started at 2026-09-09 01:47:15.334.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-09 01:47:15.335.
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-09 01:47:15.335.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'Selected tests' passed at 2026-09-09 01:47:15.335.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
```

**CellScaffold-integrasjon og de to regresjonsklassene er blocked.** Kildesøk i `Sources/App/Cells` og `Tests/AppTests` finner ikke WP5–WP7s WebFetchCeiling/flåtebinding, AgentTrustPackageCell eller de to testklassene. `PurposeBoundAIGatewayCell` finnes som underklasse nederst i `Sources/App/Cells/AI/AIGatewayCell.swift`, men mangler WP7-porten. `handoff/KANDIDATGREN.md` og WP8-resultatet dokumenterer at arbeidskopien ble returnert til originalgrenen. Null tester er ikke grønn regresjon. Brukeren er spurt om en arbeidsmappe med WP2–WP7 tilgjengelig; ingen grenbytte/gjeninnføring er gjort.

### WP9 — implementert del og avgrensning

CellProtocol-modellen er implementert uavhengig av den manglende CellScaffold-kandidaten:

- `Sources/CellBase/Agreement/PurposeBoundExternalAction.swift`: additiv `signature: ReceiptSignature?`, `signed(by:)` og `verify(against:)`; gammel JSON uten signatur gir `.unsigned`. Endret innhold, inkludert `recordingExecution`, beholder en nå ugyldig gammel signatur til kvitteringen signeres på nytt.
- `Sources/CellBase/Agreement/ReceiptSignature.swift`: `ReceiptSignature`, `.valid/.invalid/.unsigned`, eksisterende `Identity.sign` og `IdentityPublicKeySignatureVerifier`. P256-ECDSA-SHA256 eller Ed25519 velges fra identitetens offentlige nøkkel. Verifisering krever caller-pinned Identity og trenger ikke vault. Kanonisk JSON er kompakt, sortert, uten slash-escaping og uten signaturfeltet.
- `Sources/CellBase/Agreement/AgentTrustPackage.swift`: kun synligheten til WP1s UTC-normalisering endres fra fileprivate til modul-intern, slik at kvitteringene bruker samme fraksjonsbevarende koding.
- `Sources/CellBase/Agreement/EffectReceipt.swift`: schema `haven.effect-receipt.v0`, de bestilte metadatafeltene, valgfrie `ceilingDigest` (når ceiling er lest) og `packageDigest` (når bundet). Vert kan være tom ved uparsbar forespørsel; URL, sti/query, brukerinfo og port avvises i vertsfeltet. Koding/dekoding avviser også negativ bytecount og fritekst i reason (kun begrenset kode). Ingen felt for body, headers eller credential-alias.
- `Tests/CellBaseTests/ReceiptSignatureTests.swift`: 12 modell-/signaturtester, inkludert ekte eksisterende signerings-API med EphemeralIdentityVault og en isolert P256-vault-fixture.
- `Book/04_Agreements_Contracts.md` §8: modellens faktiske API-er og gjenværende celleintegrasjon er beskrevet; dato 2026-09-09.

**Tidssemantikk:** Signaturfeltet er utelatt fra signeringsbytes etter bestillingen. Derfor må `signedAt` være lik det kanoniske, signerte `createdAt`, og verifier avviser avvik. Dette er utstederens oppgitte utstedelsestid, ikke et uavhengig tidsstempel. Cellen må sette sin faktiske kvitteringstid ved utstedelse; modellen utleder ingen signeringstid fra systemklokken. SignerRef/algoritme kontrolleres mot forventet offentlig identitet. Formål og gyldig signatur gir aldri rettigheter.

**Ikke levert/blokkert i CellScaffold:** én kvittering per allowed/denied `web.fetch`, binding til faktisk WP5-ceiling/WP7-pakke ved effektøyeblikket, signering ved AIGateway-retur, append-only `webFetch.receipts` og `ai.receipts` med eier-GET/Explore, samt `Tests/AppTests/EffectReceiptTests.swift` med produksjonsbanens allowed/denied- og lekkasjeskann. Ingen erstatning for WP5–WP7 er laget. Modelltesten er uttrykkelig merket som modelltest og teller ikke som WebFetch-akseptanse. Ingen CellScaffold-produksjonskode eller eksisterende tester er endret.

### WP9 — målrettet modelltest

```sh
# cwd HAVEN/CellProtocol
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest -XCTest CellBaseTests.ReceiptSignatureTests .build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest
```

Første nye testkjøring hadde 12 tester / 1 feil: testen antok identiske signaturbytes ved gjentatt Ed25519-signering. Testen er rettet til å sammenligne de kanoniske meldingsbytes og verifisere begge signaturer; byteidentitet i vaultets signaturoutput er ikke kvitteringskontrakten. Produksjonskoden ble ikke endret for dette. Første rålogg: `/private/tmp/wp9-receipts/ReceiptSignatureTests-first.log`.

Siste bygg og ekte komplett utdata fra den målrettede testen:

```text
Build complete! (4.00s)
Test Suite 'Selected tests' started at 2026-09-09 01:54:30.865.
Test Suite 'CellProtocolPackageTests.xctest' started at 2026-09-09 01:54:30.866.
Test Suite 'ReceiptSignatureTests' started at 2026-09-09 01:54:30.866.
Test Case '-[CellBaseTests.ReceiptSignatureTests testCanonicalTimestampNormalizationAndResigningIgnoreOldSignature]' started.
Test Case '-[CellBaseTests.ReceiptSignatureTests testCanonicalTimestampNormalizationAndResigningIgnoreOldSignature]' passed (0.007 seconds).
Test Case '-[CellBaseTests.ReceiptSignatureTests testChangingDecisionExecutionOrIssuanceInvalidatesSignature]' started.
Test Case '-[CellBaseTests.ReceiptSignatureTests testChangingDecisionExecutionOrIssuanceInvalidatesSignature]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ReceiptSignatureTests testChangingOneBindingDigestInvalidatesDecisionSignature]' started.
Test Case '-[CellBaseTests.ReceiptSignatureTests testChangingOneBindingDigestInvalidatesDecisionSignature]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ReceiptSignatureTests testEffectHostRejectsURLPathQueryCredentialsAndPortOnEncodeAndDecode]' started.
Test Case '-[CellBaseTests.ReceiptSignatureTests testEffectHostRejectsURLPathQueryCredentialsAndPortOnEncodeAndDecode]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ReceiptSignatureTests testEffectSignatureRoundTripAndTamperedCeilingAndPackageDigests]' started.
Test Case '-[CellBaseTests.ReceiptSignatureTests testEffectSignatureRoundTripAndTamperedCeilingAndPackageDigests]' passed (0.002 seconds).
Test Case '-[CellBaseTests.ReceiptSignatureTests testLegacyJSONWithoutSignatureDecodesAsUnsigned]' started.
Test Case '-[CellBaseTests.ReceiptSignatureTests testLegacyJSONWithoutSignatureDecodesAsUnsigned]' passed (0.000 seconds).
Test Case '-[CellBaseTests.ReceiptSignatureTests testMissingVaultAndInvalidTimestampDoNotProduceSignature]' started.
Test Case '-[CellBaseTests.ReceiptSignatureTests testMissingVaultAndInvalidTimestampDoNotProduceSignature]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ReceiptSignatureTests testP256SignsViaIdentityVaultAPIAndPublicKeyVerifier]' started.
Test Case '-[CellBaseTests.ReceiptSignatureTests testP256SignsViaIdentityVaultAPIAndPublicKeyVerifier]' passed (0.002 seconds).
Test Case '-[CellBaseTests.ReceiptSignatureTests testSignatureMetadataAndMalformedBase64FailClosed]' started.
Test Case '-[CellBaseTests.ReceiptSignatureTests testSignatureMetadataAndMalformedBase64FailClosed]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ReceiptSignatureTests testSignsWithVaultAndVerifiesWithPublicIdentityOnly]' started.
Test Case '-[CellBaseTests.ReceiptSignatureTests testSignsWithVaultAndVerifiesWithPublicIdentityOnly]' passed (0.001 seconds).
Test Case '-[CellBaseTests.ReceiptSignatureTests testUnsignedEffectRoundTripAndNoRawContentFields]' started.
Test Case '-[CellBaseTests.ReceiptSignatureTests testUnsignedEffectRoundTripAndNoRawContentFields]' passed (0.000 seconds).
Test Case '-[CellBaseTests.ReceiptSignatureTests testWrongKeyWithSameUUIDCannotVerify]' started.
Test Case '-[CellBaseTests.ReceiptSignatureTests testWrongKeyWithSameUUIDCannotVerify]' passed (0.001 seconds).
Test Suite 'ReceiptSignatureTests' passed at 2026-09-09 01:54:30.883.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.017 (0.018) seconds
Test Suite 'CellProtocolPackageTests.xctest' passed at 2026-09-09 01:54:30.884.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.017 (0.018) seconds
Test Suite 'Selected tests' passed at 2026-09-09 01:54:30.884.
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.017 (0.019) seconds
```

### WP9 — full CellProtocol-regresjon etter endring

```sh
# cwd HAVEN/CellProtocol
xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest
```

Ekte `Executed`-linjer for hver suite, uten redigering (full rålogg `/private/tmp/wp9-receipts/cellprotocol-tests-final.log`):

```text
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.008 (0.008) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.034 (0.035) seconds
	 Executed 22 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 12 tests, with 7 tests skipped and 3 failures (3 unexpected) in 1.037 (1.037) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.120 (0.121) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.007 (0.008) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 1 test, with 1 test skipped and 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 18 tests, with 0 failures (0 unexpected) in 0.446 (0.446) seconds
	 Executed 48 tests, with 0 failures (0 unexpected) in 108.721 (108.733) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 4.293 (4.294) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.085 (0.086) seconds
	 Executed 20 tests, with 0 failures (0 unexpected) in 0.003 (0.004) seconds
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.340 (0.342) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.018 (0.018) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.008 (0.009) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.008 (0.009) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 2.892 (2.895) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.044 (0.045) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 20 tests, with 0 failures (0 unexpected) in 0.164 (0.167) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.056 (0.056) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.063 (0.064) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.064 (0.065) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.009 (0.010) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 3 tests, with 1 failure (0 unexpected) in 0.002 (0.003) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.018 (0.018) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.005 (0.006) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.015 (0.016) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.021 (0.022) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.240 (0.241) seconds
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.147 (0.152) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.020 (0.020) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.005 (0.006) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.039 (0.039) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.007 (0.008) seconds
	 Executed 35 tests, with 0 failures (0 unexpected) in 2.333 (2.337) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.512 (0.514) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.021 (0.021) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 7 tests, with 2 failures (2 unexpected) in 0.015 (0.015) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.018 (0.019) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.024 (0.025) seconds
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.004 (0.005) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.003) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.021 (0.022) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.037 (0.037) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.050 (0.051) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.007 (0.008) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.008 (0.009) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.051 (0.051) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.021 (0.022) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.448 (0.449) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.023 (0.023) seconds
	 Executed 33 tests, with 0 failures (0 unexpected) in 0.304 (0.308) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.004) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.022 (0.023) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 1.026 (1.026) seconds
	 Executed 18 tests, with 0 failures (0 unexpected) in 0.003 (0.004) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 2.002 (2.003) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
	 Executed 51 tests, with 0 failures (0 unexpected) in 0.022 (0.024) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.016 (0.017) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.050 (0.051) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 2.007 (2.009) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 1.204 (1.205) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.090 (0.091) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.142 (0.142) seconds
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.395 (0.398) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.039 (0.040) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
	 Executed 1086 tests, with 8 tests skipped and 6 failures (5 unexpected) in 130.049 (130.144) seconds
	 Executed 1086 tests, with 8 tests skipped and 6 failures (5 unexpected) in 130.049 (130.145) seconds
```

Målt: **1086 tester, 8 hoppet over, 6 feil (5 unexpected), 130.145 s**. Økning +12 tester. De seks røde testnavnene er identiske med baseline; ingen nye eller bortfalte feil. Røde feil er derfor eksisterende avvik, ikke grønn full suite. Direkte XCTest dekker ikke Swift Testing-mål.

### WP9 — CellScaffold-bygg og kompatibilitet etter endring

Det første regel 10-bygget etter nye CellBase-filer brukte en foreldet SwiftPM-filliste; `CellBase.build/sources` manglet `ReceiptSignature.swift` og `EffectReceipt.swift`. Ekte feilutdrag:

```text
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift:541:27: error: cannot find type 'ReceiptSignature' in scope
/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift:541:27: error: cannot find type 'ReceiptSignature' in scope
```

Bygggrafen ble regenerert med SwiftPMs dokumenterte lokale `--disable-build-manifest-caching`, og de nye kildefilene ble bekreftet i `CellBase.build/sources`:

```sh
# cwd HAVEN/CellScaffold
swift build --disable-sandbox --build-tests --disable-build-manifest-caching
```

```text
Build complete! (67.95s)
```

En ekstra kompatibilitetskjøring av den eksisterende `AIGatewayCellTests` krasjet så med exit 139. Isolert purpose-positive test krasjet ved kompilatorgenerert kopi av `ActionDecisionReceipt?`; samme bundle hadde ikke rekompilert `AIGatewayCellTests.swift` etter strukturendringen. Testkildenes mtime ble oppfrisket for å tvinge rekompilering av de avhengige testobjektene. **265/265 Swift-testfiler er SHA256-kontrollert byteidentiske før/etter**; ingen test er endret, fjernet eller svekket. Ingen cache-sletting, Package.swift-endring eller git.

Nybygg og hele den eksisterende AIGateway-klassen ble deretter kjørt:

```sh
# cwd HAVEN/CellScaffold
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest -XCTest AppTests.AIGatewayCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

```text
[134/276] Compiling AppTests AIGatewayCellTests.swift
Build complete! (16.66s)
Test Suite 'Selected tests' started at 2026-09-09 02:00:13.259.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-09 02:00:13.260.
Test Suite 'AIGatewayCellTests' started at 2026-09-09 02:00:13.260.
Test Suite 'AIGatewayCellTests' passed at 2026-09-09 02:00:13.375.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.113 (0.115) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-09 02:00:13.375.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.113 (0.115) seconds
Test Suite 'Selected tests' passed at 2026-09-09 02:00:13.375.
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.113 (0.116) seconds
```

**48 tester / 0 feil**, inklusive eksisterende purpose-positive, digest-drift/denied og cache-kvitteringstester. Krasjet forsvant ved rekompilering uten innholdsendringer; dette underbygger stale build-objekter som årsak. Dette er bakoverkompatibilitet for modellen, ikke test av WP9-signering i AIGateway, som fortsatt ikke er integrert. Første krasjlogger, isolerte reproduksjoner, bygglogger og SHA256-listen er bevart i `/private/tmp/wp9-receipts/`.

De tre bestilte WP9-/regresjonsfiltrene er også kjørt direkte igjen mot den sist bygde bundlen. Ekte komplette utdata:

```text
$ xcrun --sdk macosx xctest -XCTest AppTests.EffectReceiptTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
Test Suite 'Selected tests' started at 2026-09-09 02:00:48.326.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-09 02:00:48.327.
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-09 02:00:48.327.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'Selected tests' passed at 2026-09-09 02:00:48.327.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
Test Suite 'Selected tests' started at 2026-09-09 02:00:48.326.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-09 02:00:48.327.
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-09 02:00:48.327.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'Selected tests' passed at 2026-09-09 02:00:48.327.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
Test Suite 'Selected tests' started at 2026-09-09 02:00:48.326.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-09 02:00:48.327.
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-09 02:00:48.327.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'Selected tests' passed at 2026-09-09 02:00:48.327.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
```

**Alle tre er blocked: 0 utførte tester, ikke en bestått WP9-akseptanse.** De to regresjonsklassene mangler fra arbeidskopien; den nye produksjonsbanetesten er ikke laget mot en erstatning for WP5–WP7. Full CellScaffold-bundle er ikke påkrevd i WP9 og er ikke kjørt. Direkte XCTest dekker ikke Swift Testing. Ingen nye celle-keypaths er implementert, så Explore-audit av nye GET-kontrakter gjenstår sammen med celleintegrasjonen.

Siste kildekontroll (`/private/tmp/wp9-receipts/source-availability.log`):

```text
CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift: exists=False
CellScaffold/Sources/App/Cells/WebKnowledge/WebFetchCeiling.swift: exists=False
CellScaffold/Tests/AppTests/WebFetchCeilingTests.swift: exists=False
CellScaffold/Tests/AppTests/AgentTrustPackageApprovalTests.swift: exists=False
CellScaffold/Tests/AppTests/EffectReceiptTests.swift: exists=False
CellScaffold/Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift: WebFetchCeiling count=0
CellScaffold/Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift: webFetch.fleetBinding count=0
CellScaffold/Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift: webFetch.receipts count=0
CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift: class PurposeBoundAIGatewayCell count=1
CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift: ai.fleetBinding count=0
CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift: ai.receipts count=0
```

Book-lenken er kontrollert, eksisterende kapittel-/katalogmetadata er uendret, og alle fire berørte produksjonsfiler har WP9s purposeRef-kommentar. Avklaringen om kandidatens arbeidsmappe har ikke fått svar i denne kjøringen.

### WP9b — baseline før CellScaffold-endring (2026-09-09)

Regel 11: seks AgentTrustPackage-filer, WebFetchCeilingTests.swift og aktiv gren `pdd/tillitspakke-agentflaate` bekreftet før bygg. Ingen grenbytte eller øvrige git-operasjoner.

Kjørt i CellScaffold: `swift build --disable-sandbox --build-tests`, deretter `xcrun --sdk macosx xctest -XCTest AppTests.<klasse> .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest`. Full bundle er ikke påkrevd i WP9b og kjøres ikke.

```text
build
Build complete! (23.30s)
WebFetchCeilingTests
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.133 (0.134) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.133 (0.134) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.133 (0.135) seconds
AgentTrustPackageApprovalTests
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.713 (0.714) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.713 (0.714) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.713 (0.714) seconds
```

Baseline: 17 + 17 = 34 XCTest, null feil. EffectReceiptTests finnes ikke før denne slicen. Rålogger: `/private/tmp/wp9b-receipts/baseline-*.log`.

### WP9b — mellomkjøringer og rettelser

Første kompilering traff feil i nye Explore-schema-kall/closure-signaturer; to videre testbygg traff en feil referanse til egress-validering i den nye provider-fixturen. Rettet til eksisterende API. Bygglogger ligger i `/private/tmp/wp9b-receipts/`. Ett umiddelbart byggforsøk fra HAVEN-roten fant ikke Package.swift og ble korrigert til CellScaffold. Ingen full bundle kjørt.

Første komplette testkjøring: manglende kvittering ved tidlig AI-intent-avslag, lagringsfeil som overskygget et allerede korrekt flåteavslag, og to feil i negativ vault-fixture. AI-avslag med dekodet intent/observerbare bindings får nå signert avslag; persistensfeil bevarer beslutningen og rapporteres separat som `receiptPersistence=failed` (WebFetch) / `receipt_persistence_failed` (AI-diagnostikk).

Den andre kjøringen isolerte vault-fixturen: den påstått fremmede vaulten var samme EphemeralIdentityVault som eierens og hadde derfor eiernøkkelen. Testen bruker nå en separat vault og kontrollerer eksplisitt at denne ikke kan bevise eierskap. Ingen eksisterende test er fjernet/svekket.

```text
EffectReceiptTests — first
	 Executed 8 tests, with 7 failures (3 unexpected) in 2.101 (2.102) seconds
	 Executed 8 tests, with 7 failures (3 unexpected) in 2.101 (2.102) seconds
	 Executed 8 tests, with 7 failures (3 unexpected) in 2.101 (2.113) seconds
WebFetchCeilingTests — first
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.184 (0.184) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.184 (0.184) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.184 (0.185) seconds
AgentTrustPackageApprovalTests — first
	 Executed 17 tests, with 2 failures (0 unexpected) in 1.850 (1.851) seconds
	 Executed 17 tests, with 2 failures (0 unexpected) in 1.850 (1.851) seconds
	 Executed 17 tests, with 2 failures (0 unexpected) in 1.850 (1.852) seconds
EffectReceiptTests — second
	 Executed 8 tests, with 2 failures (0 unexpected) in 1.519 (1.519) seconds
	 Executed 8 tests, with 2 failures (0 unexpected) in 1.519 (1.519) seconds
	 Executed 8 tests, with 2 failures (0 unexpected) in 1.519 (1.521) seconds
WebFetchCeilingTests — second
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.186 (0.187) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.186 (0.187) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.186 (0.187) seconds
AgentTrustPackageApprovalTests — second
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.758 (0.759) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.758 (0.759) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.758 (0.759) seconds
```

Tillegg før sluttkontrollen: ni nye tester var utvidet med redirect og full GET-schema-kontroll. To schema-asserts feilet fordi `ValueType.list` ikke har strukturell likhet; begge sammenligningene er rettet til dekodede permissions / kanonisk JSON. Produksjonsautorisasjonen ble ikke endret for disse to feilene. Feil-/avslagssvar på de nye GET-nøklene er også avstemt mot deklarert schema (`action` inkludert).

```text
	 Executed 9 tests, with 2 failures (0 unexpected) in 1.234 (1.235) seconds
	 Executed 9 tests, with 2 failures (0 unexpected) in 1.234 (1.235) seconds
	 Executed 9 tests, with 2 failures (0 unexpected) in 1.234 (1.236) seconds
```

### WP9b — levert CellScaffold-integrasjon og sluttkontroll

purposeRef: `purpose://candidate.tillitspakke-agentflaate.signert-kvittering`.

- `CellScaffold/Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift`: én eier-signert `EffectReceipt` per håndtert `web.fetch`, inkludert dispatch-avslag, ugyldig input, manglende/stale pakke, whitelist/credential-avslag, HTTP-suksess, redirect og transportfeil. Utstedelsen samles per kall. `destinationHost` inneholder bare vert; ugyldig fritekstmetode blir `UNKNOWN`. Bytes teller mottatte responsbytes i URLSession-data-callbacks, inkludert bytes som ikke beholdes i forhåndsvisningen. Redirect-kvitteringen beskriver første vert, ingen redirect-URL eller ny request. `credentialsUsed=false` følger gjeldende credential-forbud i v0.
- `CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageApproval.swift`: startporten returnerer verifisert pakke-digest sammen med samme admission-beslutning. `bindings.ceilingDigest` er eksisterende komplette operative policy-/ceiling-digest fra `AgentTrustApprovalEvidence.policyDigest` (instans, eksakte template-Grants og ceiling-data). Pakke-digest kommer fra verifisert godkjenningssnapshot og beholdes ved stale/revoked avslag. Hvis ingen verifiserbar godkjenning finnes, er digest utelatt; den fabrikeres ikke. Ceiling og binding beholdes fra admission selv om eieren endrer ceiling under overføringen.
- `CellScaffold/Sources/App/Cells/AI/AIGatewayCell.swift`: `ActionDecisionReceipt` signeres etter endelig execution-status og returneres også på SET-wireflaten. Cache-treff får en ny signert beslutningskvittering. Tidlige intent-/flåteavslag med dekodet intent og observerbare bindings får signert avslag uten provider-kall. Runtime-genererte kvitterings-/kontekst-ID-er og hash av klientens intent-ID hindrer referansefeltene i å lagre rå input. Utstedelsestid settes av cellen ved retur.
- `CellScaffold/Sources/App/Cells/SignedCellReceiptStore.swift`: append-only lager per instans, Codable snapshot, ingen SET/reset/trim-keypaths. GET `webFetch.receipts` / `ai.receipts` returnerer en liste med kvitteringsobjekter; komplett Explore-schema og `r---`. Eierens nøkkel må bevises før dispatch og i handler, også under debug-bypass eller eksplisitt Contract-Grant til en annen requester. Eksisterende `web.clear` sletter ikke kvitteringer.
- `CellScaffold/Tests/AppTests/EffectReceiptTests.swift`: ni nye tester. Verifisering mot offentlig eieridentitet, manipulerte bytes/digests, innholdsskann, denial før nettverk, eierbeskyttelse med uavhengig angripervault, per-instans-historikk, clear/SET-forsøk, snapshot/reload, bytes ved avkorting, transportfeil, redirects, endring under pågående transfer, godkjent/stale pakke og AI-retur/cache/avslag/SET-wire.
- `CellScaffold/Tests/AppTests/AIGatewayCellTests.swift`: eksisterende eksakte forventninger er additivt oppdatert for den nye `ai.receipts`-GET-en (seks Explore-operasjoner totalt) og hashed intent-korrelasjon. Riktig `r---` og signatur verifiseres; ingen test fjernet eller svekket.

Avgrensninger: Append-only gjelder celle-API-et; Codable-snapshot er ikke en kryptografisk kjedet eller slettesikker journal. Snapshot/reload er testet, ikke en full vertsomstart med varig lagring. Feilet persistens beholder kvitteringen i minnet og rapporterer lagringsfeilen separat. Manglende eier-signering feiler eksplisitt; det lages ingen erstatningsnøkkel eller usignert suksesskvittering. Helt udekodbar AI-input, manglende intent eller forespørsler som ikke kan gi observerbare v1-bindings beholder eksisterende feilretur uten `ActionDecisionReceipt`. CellProtocol-modellene og Book er ikke endret av WP9b; WP9s modellutdata ovenfor er bevart.

Kommandoer, cwd `HAVEN/CellScaffold`:

```sh
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest -XCTest AppTests.EffectReceiptTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.WebFetchCeilingTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.AIGatewayCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Ekte bygg-/testutdata, rålogger `/private/tmp/wp9b-receipts/acceptance-*.log`:

```text
Build complete! (17.00s)
EffectReceiptTests
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.151 (0.151) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.151 (0.151) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.151 (0.152) seconds
WebFetchCeilingTests
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.178 (0.179) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.178 (0.179) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.178 (0.180) seconds
AgentTrustPackageApprovalTests
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.738 (0.739) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.738 (0.739) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.738 (0.740) seconds
AIGatewayCellTests
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.121 (0.122) seconds
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.121 (0.123) seconds
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.121 (0.123) seconds
```

**Resultat: 43/43 påkrevde XCTest grønne (9 + 17 + 17), i tillegg 49/49 AIGatewayCellTests; totalt 92/92, null feil.** Full CellScaffold-bundle er ikke påkrevd i WP9b og er ikke kjørt. Direkte XCTest dekker ikke Swift Testing-mål. Ingen CellProtocol-bygg/test gjentatt i denne slicen.

Explore-audit er kjørt med `Tools/Explore/explore_contract_audit.py --repo-root CellProtocol` og tilsvarende `--repo-root CellScaffold --source-dir Sources/App/Cells`. De brede statiske auditene er ikke grønne: CellProtocol 7 feil / 19 varsler; CellScaffold 1051 feil / 390 varsler. JSON og logger: `/private/tmp/wp9b-receipts/explore-*`. Dette er ikke en repo-sertifisering; dynamisk registrering gjennom den generiske receipt-helperen må kontrolleres i runtime. Den nye testklassen kontrollerer eksakt GET-schema/permissions, og den eksisterende AIGateway-klassen kontrollerer komplett key-/operations-sett.

Regel 11 sluttkontroll: `CellScaffold/.git/HEAD` peker fortsatt på `refs/heads/pdd/tillitspakke-agentflaate`. Ingen git-operasjoner utover den uttrykkelig pålagte innledende grenlesingen; ingen commit, checkout eller push.

## WP9 — sluttmelding

**Delvis levert, blocked på CellScaffold-integrasjon; WP9 er ikke ferdig.** `ActionDecisionReceipt` har additiv signatur og sign/verify med eksisterende identitets-API. `EffectReceipt`-modellen har de bestilte metadatafeltene og tilsvarende signering. 12 nye modelltester er grønne. Begge repoer bygger etter oppfrisking av SwiftPM-graf/testobjekter. Full CellProtocol-bundle: **1086 tester, 8 hoppet over, samme 6 røde som baseline 1074, ingen nye røde navn**. Eksisterende CellScaffold AIGatewayCellTests: **48/48 grønne** etter rekompilering, uten endring av tester.

WebFetch/AIGateway-utstedelse, begge append-only instanslagre med eier-GET og Explore, faktiske ceiling-/pakkebindinger og produksjonsbanens `EffectReceiptTests` gjenstår. De bestilte CellScaffold-filtrene utfører 0 tester fordi WP2–WP7-koden/testene mangler fra den oppgitte arbeidskopien etter kandidatgren-handoffens tilbakebytte. Fortsettelse krever en tilgjengelig arbeidsmappe med denne eksisterende koden; `Ingen git` er respektert. Ingen WP5–WP7-erstatning, WP10-funksjonalitet, skeleton, deployment eller ny kryptografi er laget.

`Book/04_Agreements_Contracts.md` §8 beskriver kun implementert modell og den eksplisitte integrasjonsbegrensningen, med «Last verified against code: 2026-09-09». STATUS.md har én WP9-linje. Alle kvitterings-/baseline-/regresjonsutdata står under [Kvittering](#receipt). Full CellScaffold-bundle er ikke kjørt; Swift Testing er ikke dekket.

## Diff <a id="diff"></a>

### WP10 — gjenopptatt 2026-09-09: baseline før endring

purposeRef: `purpose://candidate.tillitspakke-agentflaate.etterproving`. Regel 11 bestod: seks kildefiler, WebFetchCeilingTests.swift og `pdd/tillitspakke-agentflaate`. Ingen git etter den pålagte grenlesingen. WP9b-lagrene finnes. Tidligere blocked-kjøring nedenfor er historikk.

Regel 10: `swift build --disable-sandbox --build-tests`, så direkte `xcrun --sdk macosx xctest -XCTest AppTests.<klasse> .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest` i CellScaffold. Nye AuditTests finnes ikke før endringen. Rålogger: `/private/tmp/wp10b-audit/`.

```text
baseline-build
Build complete! (23.45s)
baseline-cell
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.296 (0.297) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.296 (0.297) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.296 (0.298) seconds
baseline-approval
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.727 (0.728) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.727 (0.728) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.727 (0.729) seconds
```

Baseline: 16 + 17 = 33 tester, null feil.


purposeRef: `purpose://candidate.tillitspakke-agentflaate.etterproving`. Kun WP10, 2026-09-09.

### WP10 — mellomkontroller og kildeavgrensninger

Ny produksjonskode er avgrenset til AgentTrustPackageCell, audit-helper, kontrakt/schema og config-factory. WP9-modeller og kvitteringsutstedelse er uendret. Det gamle WP2-reservasjonstesttilfellet er erstattet med kontroll av faktisk navigasjon, ugyldig payload, ingen godkjenning og uendret digest; øvrige eksisterende tester beholdes.

Første byggforsøk ble startet fra HAVEN-roten og fant ingen Package.swift. Korrigert til CellScaffold. Første kompilering av ny kode fant en feilplassert switch-gren i registreringen. Et påfølgende bygg leste filen før rettelsen var ferdig og rapporterte også endring under bygg; fra neste kjøring ble bygg og kildeendringer holdt sekvensielle. Testkompilering avdekket en ikke-eksisterende route-helper og et async-kall i en XCTest-autoclosure. Rettet til eksisterende API. Rålogger: `first-build.log`, `compile-1.log`–`compile-5.log` i `/private/tmp/wp10b-audit/`.

Første fullførte målrettede kjøring: fixture, manipulering, alle fem avvikstyper, navigasjon, eiervern, snapshot/reload og manglende kilder bestod. Den ekstra produksjonstesten antok at Anthropic-kallet ville bli tillatt. Faktisk kilde (`CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift`, `exactCeiling = …first`) velger første ceiling for action/formål før destinasjon sjekkes, mens gateway-policyen har separate provider-ceilings med OpenAI først. Anthropic ble derfor nektet med `destination_not_allowed`. Dette eksisterende runtime-forholdet er **ikke rettet i WP10**. Produksjonstestens positive kontroll bruker OpenAI; den normative sju-kvitteringsfixturen er eksplisitt syntetisk og beholder Anthropic-metadata.

```text
compile-4
Build complete! (50.13s)
first-audit
	 Executed 10 tests, with 3 failures (0 unexpected) in 2.424 (2.425) seconds
	 Executed 10 tests, with 3 failures (0 unexpected) in 2.424 (2.425) seconds
	 Executed 10 tests, with 3 failures (0 unexpected) in 2.424 (2.427) seconds
first-cell
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.346 (0.347) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.346 (0.347) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.346 (0.348) seconds
first-approval
	 Executed 17 tests, with 0 failures (0 unexpected) in 1.019 (1.020) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 1.019 (1.020) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 1.019 (1.021) seconds
```

### WP10 — implementasjon og målrettet akseptanse

- `AgentTrustPackageCell.swift`: GET samler eierinnslupne `webFetch.receipts` / `ai.receipts` fra **godkjent** flåteutvalg siden signert `approvedAt`. Originale metadata lagres append-only per flåtecelle, med innholdsdigest som nøkkel. Gjentatt GET dedupliserer; endret innhold med samme receiptID beholder begge og viser `unknown_policy_version`. Ingen offentlig append/reset/trim. Signatur kontrolleres mot flåteeierens offentlige nøkkel, og kildeinstansen må finnes i signert `policyDigests`.
- Godkjenning beholder `packageSnapshot` som kanonisk JSON ved siden av signert record. Snapshot-digest beregnes på nytt og må stemme med signert godkjenning. Senere justering, tomt flåteutvalg, stop og snapshot/reload erstatter ikke audit-grunnlaget. WP7-godkjenning uten snapshot kan bare fylles inn fra faktisk gjeldende pakke når den fortsatt gir identisk signert digest; ellers vises ufullstendig etterprøving.
- `AgentTrustPackageAudit.swift`: de fem `ViolationKind`-verdiene, norske kontraktslabels, egne tellerverdier for effekter/innenfor/nektet, signaturstatus ved faktisk verifisering. Både denied-forsøk og gjennomførte brudd telles. En effekt kan ha flere avvik; «innenfor» teller effekter uten avvik. Usignert/manipulert kvittering gir `unknown_policy_version`, også når manipulert tidsfelt prøver å skjule kvitteringen før godkjenning.
- `trustPackage.open.*` returnerer kun `{status: navigate, endpoint, keypath}`. Receipt peker til bevart originalkvittering i `trustPackage.audit.receipts.<innholdsdigest>`, package til `configuration` for innsnevring/godkjenning, instruction til eksisterende instruksjonskilde. Ukjent/ambig receipt-ID og ugyldig payload får eksplisitt avslag. Ingen instruksjonstekst eller kvitteringsinnhold returneres i navigasjonssvaret.
- `AgentTrustPackageContract.swift`: eksplisitte Explore-skjemaer for audit/navigasjon/arkiv og eier-GET (`r---`). `configuration.audit` returnerer egen `Agent Trust Package — etterprøving` fra factory. Skeletonens elementer, keypaths, payloads og discovery er bevart fra `skeleton/tillitspakke-etter.json`; test sammenligner kodet skeleton strukturelt. `contract/agent_trust_package_contract_v0.json` avstemmer tillegget.
- `AgentTrustPackageAuditTests.swift`: ti tester, inkludert den normative fixturen normalisert til ekte WP9-signerte modeller, negativ signatur/tid, alle fem typer, ingen godkjenning, referanseoppslag, bevaring/deduplisering, kildefeil, eierbevis under debug-bypass, skeleton/Explore og produksjonsutstedelse gjennom både WebFetch og PurposeBoundAIGateway med mocket nettverk/provider. Ingen live modell eller eksterne effekter.

**Evidensgrenser:** WP9s EffectReceipt har vert og årsakskoder, men ingen sti/query, port, redirect-mål, alias eller caller-agent. Audit dikter ikke opp disse; avvist port/scheme/redirect utledes av den signerte årsakskoden. ActionDecisionReceipt v1 har ingen lesbar route/destinasjon eller verktøyliste: audit sammenligner bindings-/manifest-/plan-digester, signerte ceiling-checks og reasonCodes. Den gir ikke uavhengig rekonstruksjon av et AI-kall. Ved innsnevret AI-policy kan pakkens effektive policy-digest avvike fra receiptens template-digest; dette vises konservativt som `unknown_policy_version`. Append-only gjelder API og bevaring ved innsamling, ikke en slettesikker/kryptografisk kjedet journal; innhold som er fjernet fra en kilde **før første innsamling** kan ikke oppdages. Snapshot/reload er testet; full vertsomstart/varig disk-I/O og Porthole/Binding-navigasjon er ikke verifisert i WP10. Kilde-/persistensfeil gir ufullstendig status, aldri «Overholdt».

Kommandoer i CellScaffold, regel 10:

```sh
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAuditTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

```text
compile-5
Build complete! (28.18s)
acceptance-audit
	 Executed 10 tests, with 0 failures (0 unexpected) in 1.541 (1.542) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 1.541 (1.542) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 1.541 (1.562) seconds
acceptance-cell
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.367 (0.368) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.367 (0.368) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.367 (0.368) seconds
acceptance-approval
	 Executed 17 tests, with 0 failures (0 unexpected) in 1.051 (1.052) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 1.051 (1.052) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 1.051 (1.053) seconds
```

**43/43 målrettede tester grønne (10 + 16 + 17).** Direkte XCTest dekker ikke Swift Testing-mål. Full bundle er dokumentert i neste avsnitt.

Statisk Explore-audit er kjørt med `--repo-root CellProtocol` og `--repo-root CellScaffold --source-dir Sources/App/Cells`. Resultatene er samme globale nivå som WP9b: CellProtocol 7 feil / 19 varsler; CellScaffold 1051 feil / 390 varsler. Ingen funn på AgentTrustPackage i den statiske rapporten; runtime-testene kontrollerer faktisk registrering. Dette er ikke en grønn repo-sertifisering. JSON/logg i `/private/tmp/wp10b-audit/explore-*`.

### WP10 — full CellScaffold-bundle etter endring

Kjørt etter grønt bygg og 43/43 målrettede tester, cwd `HAVEN/CellScaffold`:

```sh
xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Rålogg: `/private/tmp/wp10b-audit/full-bundle.log`. Maskinell navnesammenligning: `/private/tmp/wp10b-audit/failure-comparison.json`. Baseline er den faktiske WP0c-loggen med 2046 tester / 46 røde navn. Direkte XCTest dekker ikke Swift Testing.

Kjøringen har 2154 testnavn (108 flere enn baseline), 46 røde navn, 0 nye røde navn, 0 tidligere røde navn som nå er borte. 0 baseline-testnavn mangler i kjøringen.

Ekte sluttlinje:

```text
	 Executed 2154 tests, with 11 tests skipped and 151 failures (9 unexpected) in 827.109 (827.281) seconds
```

Røde testnavn i fullkjøringen (nøyaktig samme sett som baseline):

- `AppTests.AIAssistantThreadCellTests testPostUserMessageStartsHAVENTeachingSwarmAndAppendsProviderTurns`
- `AppTests.AIAssistantThreadCellTests testPostUserMessageStartsLocalOnlyHAVENTeachingSwarmWithoutAPIKeys`
- `AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelLocalBorealisChatsAgainstSharedBackend`
- `AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelMixedHostedAndLocalChatsWithRouteCredentials`
- `AppTests.ArendalsukaEventAtlasCellTests testDecodedParticipantProgramCanEnsureRuntimeBindingsBeforeStateRead`
- `AppTests.ArendalsukaEventAtlasCellTests testParticipantPreviewReadsDecodedRegisteredAtlasWithoutJournalFallback`
- `AppTests.ArendalsukaEventAtlasCellTests testParticipantProgramReadsAtlasPreviewWithoutPersistingUntilExplicitAction`
- `AppTests.ArendalsukaEventAtlasCellTests testParticipantProgramUsesAtlasPreviewForMissingProgramInPartialOverlay`
- `AppTests.ArendalsukaImportAuthorizationRoutesTests testAdminDelegatesIdentityBoundCredentialToNonAdminImporter`
- `AppTests.BookReferenceRoutesTests testConferenceConnectionHubLifecycleSlugRouteRendersMermaidInline`
- `AppTests.BookReferenceRoutesTests testConferenceOwnershipSlugRouteRendersMermaidInline`
- `AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview`
- `AppTests.ChatMVPRoutesTests testPaidStateAndMessageRoutesAwaitDecodedChatReadiness`
- `AppTests.ConferenceEntityDiscoveryCellTests testChatLaunchCellCanStartConversationAndProjectMessageFeedback`
- `AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionHandsOffCapturedLeadToSponsorOwnedFollowUp`
- `AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionUsesConsentBoundAggregateSignalsWhenAvailable`
- `AppTests.ConferencePublishedContentCellTests testPublishedContentCellRecognizesStableOrganizerIdentityWhenVaultContextIsPoisoned`
- `AppTests.ConferenceSchedulingCellTests testRouterDelegatesSharedMeetingRequestAndLocalExportToSchedulingCell`
- `AppTests.ConferenceSponsorLeadAggregateCellTests testSponsorLeadAggregateSyncsConsentBoundParticipantsAndCapturesLead`
- `AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionAcceptsStoredImportAccessVC`
- `AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionSupportsAdminSessionAndRejectsMismatchedSignedProof`
- `AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication`
- `AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublishedApiReadsUseAgreementWithoutDebugAccess`
- `AppTests.ConferenceSurfaceRoutesTests testConferencePageAccessPolicies`
- `AppTests.ConferenceSurfaceRoutesTests testConferencePagesExposeCanonicalSurfaceMetadataForWebNavigator`
- `AppTests.ConfigurationCatalogSkeletonParityTests testConferenceParticipantPortalDocumentationConfigurationMatchesRuntimeFactory`
- `AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeRetryBlocksConsumedCredentialReplay`
- `AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction`
- `AppTests.HavenWorkbenchConfigurationTests testHavenWorkbenchUsesLocalTabsAndSupportedVisualizations`
- `AppTests.MermaidRendererCellTests testWebViewDeterministicModeStableAcrossThreeBypassRuns`
- `AppTests.MermaidRendererCellTests testWebViewIntegrationRendersPNGWithoutClientTimeout`
- `AppTests.MermaidRendererCellTests testWebViewIntegrationRendersSVGAndCacheHit`
- `AppTests.MermaidRendererCellTests testWebViewRendersConferenceDiagramFilesAndExposesPreviewState`
- `AppTests.MicropaymentsMVPRoutesTests testPaymentProofDoorAuthorizeConsumesCredentialAndBlocksReplay`
- `AppTests.MusicPublishingCellsTests testScaffoldRecoversPersistedMusicLibraryWhenNamedEmitterRegistryIsEmpty`
- `AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction`
- `AppTests.ProductionSkeletonBindingIntegrityTests testArendalsukaEventAtlasPortholeTabsAndDetailsDoNotReturnNotFound`
- `AppTests.ProductionSkeletonBindingIntegrityTests testArendalsukaParticipantProgramRendersSourceBackedProgramRowsWithoutBrokenKeypaths`
- `AppTests.ProductionSkeletonBindingIntegrityTests testHavenWorkbenchSetupThroughPortholeKeepsSkeletonBindingsResolvable`
- `AppTests.SkeletonElementParityMatrixTests testMatrixRevisionMatchesPackagePin`
- `AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips`
- `AppTests.SkeletonRuntimeSourceTests testPortholeBootstrapUsesHttpSnapshotNotSocketFallbackWarning`
- `AppTests.TopUpCheckoutTests testProductionStartupRejectsMissingRuntimeIdentityManifestBeforePublishingResolver`
- `AppTests.TopUpCheckoutTests testSimulatedTopUpAllowsExplicitProductionAllowlistedUser`
- `AppTests.TopUpCheckoutTests testSimulatedTopUpDefaultsToDeniedInProductionLikeEnvironment`
- `AppTests.WorkbenchAccessGrantConfigurationTests testIdentityBoundPregrantUsesIssuerVaultWhenTargetOwnerWasDecodedSnapshot`

Alle faktiske `Executed`-linjer fra fullkjøringen:

```text
	 Executed 14 tests, with 4 tests skipped and 12 failures (0 unexpected) in 1.816 (1.817) seconds
	 Executed 49 tests, with 0 failures (0 unexpected) in 0.146 (0.148) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.073 (0.074) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.528 (0.529) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.022 (0.023) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.019 (0.019) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.225 (0.226) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.101 (1.101) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.008 (0.009) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.369 (1.369) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.054 (0.054) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.531 (0.531) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.600 (0.600) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.265 (0.265) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.494 (0.495) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.375 (0.375) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.014 (0.015) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.419 (0.420) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.032 (0.032) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.234 (0.234) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.026 (0.027) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.507 (0.508) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.954 (0.954) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 1.839 (1.861) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 1.244 (1.245) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.354 (0.355) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.114 (0.115) seconds
	 Executed 21 tests, with 0 failures (0 unexpected) in 0.308 (0.309) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.015 (0.016) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.751 (0.752) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.299 (0.299) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.745 (0.745) seconds
	 Executed 40 tests, with 14 failures (0 unexpected) in 1.218 (1.222) seconds
	 Executed 1 test, with 3 failures (0 unexpected) in 0.338 (0.338) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.095 (0.095) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 5.536 (5.537) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.026 (0.026) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.089 (0.089) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.992 (0.992) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.147 (0.148) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.236 (0.236) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
	 Executed 6 tests, with 2 failures (0 unexpected) in 11.024 (11.028) seconds
	 Executed 20 tests, with 0 failures (0 unexpected) in 0.621 (0.623) seconds
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.010 (0.011) seconds
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.292 (0.293) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 31 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.790 (0.792) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.002 (0.003) seconds
	 Executed 11 tests, with 18 failures (1 unexpected) in 4.878 (4.879) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.016 (0.017) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.251 (0.251) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.137 (0.138) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.060 (0.060) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.123 (0.124) seconds
	 Executed 21 tests, with 0 failures (0 unexpected) in 0.061 (0.062) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.023 (0.023) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.037 (0.037) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.008 (0.009) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.605 (0.605) seconds
	 Executed 10 tests, with 7 failures (0 unexpected) in 3.953 (3.954) seconds
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.458 (0.460) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.006 (0.007) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.124 (0.125) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.216 (0.217) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.200 (0.200) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.058 (0.059) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 4.091 (4.092) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.239 (0.239) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.065 (0.065) seconds
	 Executed 11 tests, with 1 failure (1 unexpected) in 0.122 (0.123) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.021 (0.021) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.173 (0.173) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.045 (0.045) seconds
	 Executed 3 tests, with 7 failures (0 unexpected) in 0.069 (0.069) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.046 (0.047) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 1.613 (1.613) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.051 (0.051) seconds
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.424 (0.425) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.424 (0.424) seconds
	 Executed 10 tests, with 1 failure (1 unexpected) in 0.054 (0.055) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.056 (0.056) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
	 Executed 2 tests, with 1 failure (0 unexpected) in 0.039 (0.039) seconds
	 Executed 68 tests, with 0 failures (0 unexpected) in 5.981 (5.985) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.226 (0.226) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.113 (0.113) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.218 (0.218) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
	 Executed 2 tests, with 1 failure (1 unexpected) in 0.012 (0.012) seconds
	 Executed 39 tests, with 21 failures (0 unexpected) in 55.290 (55.293) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.046 (0.046) seconds
	 Executed 31 tests, with 0 failures (0 unexpected) in 2.192 (2.205) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.013 (0.014) seconds
	 Executed 17 tests, with 2 tests skipped and 1 failure (0 unexpected) in 0.823 (0.824) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 1.648 (1.650) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.022 (0.023) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 5 tests, with 9 failures (0 unexpected) in 1.203 (1.204) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 2.542 (2.543) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.412 (0.413) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.049 (0.049) seconds
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.076 (0.076) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.219 (0.219) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.133 (0.134) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.267 (0.268) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.537 (0.537) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.100 (0.101) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.125 (0.125) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.295 (0.296) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 1.807 (1.807) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
	 Executed 36 tests, with 0 failures (0 unexpected) in 1.378 (1.380) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.057 (0.057) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.491 (0.492) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.179 (0.180) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.131 (0.131) seconds
	 Executed 6 tests, with 1 failure (0 unexpected) in 0.157 (0.157) seconds
	 Executed 20 tests, with 0 failures (0 unexpected) in 1.177 (1.179) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 12.991 (12.992) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.030 (0.031) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.725 (0.725) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.144 (0.145) seconds
	 Executed 4 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.007 (0.008) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.046 (0.046) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.072 (0.072) seconds
	 Executed 11 tests, with 14 failures (0 unexpected) in 15.716 (15.718) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.458 (0.458) seconds
	 Executed 1 test, with 4 failures (0 unexpected) in 0.215 (0.215) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 26 tests, with 3 failures (0 unexpected) in 0.141 (0.142) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.054 (0.054) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.200 (0.200) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 2.180 (2.181) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.056 (0.056) seconds
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.248 (0.249) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.067 (0.067) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.034 (0.034) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 3.632 (3.633) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.587 (0.588) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.237 (0.239) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.352 (0.352) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.026 (0.027) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.056 (0.057) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 2.656 (2.657) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 2.612 (2.613) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.006 (0.007) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.594 (0.594) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.020 (0.021) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 33.143 (33.144) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.178 (0.178) seconds
	 Executed 70 tests, with 0 failures (0 unexpected) in 11.156 (11.160) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.634 (0.635) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.021 (0.021) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.100 (0.100) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
	 Executed 45 tests, with 5 failures (0 unexpected) in 548.998 (549.002) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 10.825 (10.825) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.123 (0.123) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 3.189 (3.189) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.007 (0.008) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.064 (0.064) seconds
	 Executed 15 tests, with 0 failures (0 unexpected) in 2.685 (2.686) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
	 Executed 4 tests, with 19 failures (1 unexpected) in 7.260 (7.260) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.039 (0.039) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.038 (0.039) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.133 (0.133) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.009 (0.010) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.124 (0.125) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.950 (0.950) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.020 (0.021) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 1.015 (1.015) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.076 (0.076) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.020 (0.021) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.026 (0.026) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.441 (1.442) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.026 (0.026) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.032 (0.032) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.043 (0.044) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.690 (1.690) seconds
	 Executed 15 tests, with 0 failures (0 unexpected) in 2.980 (2.981) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.054 (0.054) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 9 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.015 (0.015) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.015 (0.016) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.023 (0.023) seconds
	 Executed 3 tests, with 2 failures (0 unexpected) in 0.330 (0.330) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.796 (0.796) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.044 (0.044) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 16 tests, with 1 failure (0 unexpected) in 0.147 (0.148) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.022 (0.022) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.013 (0.014) seconds
	 Executed 1 test, with 1 test skipped and 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 1.009 (1.009) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.212 (0.212) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.719 (0.720) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.033 (0.033) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
	 Executed 19 tests, with 3 failures (3 unexpected) in 2.524 (2.525) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.031 (0.032) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.101 (0.102) seconds
	 Executed 28 tests, with 1 test skipped and 0 failures (0 unexpected) in 2.361 (2.366) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.056 (0.056) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 2.719 (2.719) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.021 (0.021) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.162 (0.162) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.031 (0.031) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.023 (0.024) seconds
	 Executed 24 tests, with 1 failure (1 unexpected) in 2.213 (2.214) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 8.209 (8.210) seconds
	 Executed 2154 tests, with 11 tests skipped and 151 failures (9 unexpected) in 827.109 (827.280) seconds
	 Executed 2154 tests, with 11 tests skipped and 151 failures (9 unexpected) in 827.109 (827.281) seconds
```

### WP10 — siste tekstpresisering og sluttkontroll

Fullkjøringen ovenfor gjelder den ferdige funksjonelle implementasjonen før én avsluttende label-presisering: `redirect_outside_whitelist` sier nå at omdirigering **fra** den lagrede verten ble nektet, og at målvert ikke er lagret. Den opprinnelige verten fremstilles dermed ikke som den forbudte målverten. Avviksregler, telling, bindingskontroll, signering og lagring er uendret. Etter denne tekstendringen er regel 10-bygg og alle tre målrettede klasser kjørt på nytt; full bundle er ikke gjentatt for ordlydsendringen.

Ekte sluttkontrollutdata (`/private/tmp/wp10b-audit/final-*.log`):

```text
final-build
Build complete! (18.45s)
final-audit
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.796 (0.796) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.796 (0.796) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.796 (0.797) seconds
final-cell
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.304 (0.305) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.304 (0.305) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.304 (0.305) seconds
final-approval
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.804 (0.805) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.804 (0.805) seconds
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.804 (0.806) seconds
```

Sluttbygget er grønt, **18.45 s**. Siste målrettede kjøring: **43/43 grønne**. Full bundle: **2154 tester / 11 hoppet over / 151 feilrapporter (9 unexpected) / nøyaktig samme 46 røde navn som baseline / ingen nye / ingen manglende baseline-testnavn**, 827.281 s. Regresjonsavvikene er eksisterende og full suite er derfor ikke grønn.

### WP10 — kontroll av forutsetninger

**Implementasjon blocked: nødvendig WP2–WP7-cellekode og WP9-kvitteringslagre mangler i oppgitt arbeidskopi.** Brukerens premiss om ferdig WP9-integrasjon stemmer ikke med kildefilene eller siste [WP9-sluttmelding](#receipt), som sier «Delvis levert, blocked på CellScaffold-integrasjon». WP9 har levert signatur-/kvitteringsmodeller i CellProtocol, men ikke utstedelse og append-only `webFetch.receipts`/`ai.receipts` i CellScaffold.

Et filsøk under HAVEN, med `.git`, bygge- og cachemapper utelatt, fant ingen eksisterende kandidatkopi av `AgentTrustPackageCell.swift`, konfigurasjonsfabrikken, `AgentTrustPackageApprovalTests.swift`, `WebFetchCeiling.swift` eller `EffectReceiptTests.swift`. [KANDIDATGREN.md](handoff/KANDIDATGREN.md) dokumenterer at WP2–WP7 ble pakket i CellScaffold-kandidaten `pdd/tillitspakke-agentflaate` ved `1dbdee23f5272a3485a4c6b8263c84c4351eaf28`, før arbeidskopien ble byttet tilbake. Dette er dokumentert historikk, ikke en ny git-kontroll. Ingen git er brukt.

Ekte kildekontroll, `/private/tmp/wp10-audit/source-availability.log`:

```text
CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageCell.swift: exists=False
CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageConfigurationFactory.swift: exists=False
CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageApproval.swift: exists=False
CellScaffold/Sources/App/Cells/AgentTrustPackage/AgentTrustPackageContract.swift: exists=False
CellScaffold/Tests/AppTests/AgentTrustPackageAuditTests.swift: exists=False
CellScaffold/Tests/AppTests/AgentTrustPackageCellTests.swift: exists=False
CellScaffold/Tests/AppTests/AgentTrustPackageApprovalTests.swift: exists=False
CellScaffold/Tests/AppTests/EffectReceiptTests.swift: exists=False
CellProtocol/Sources/CellBase/Agreement/AgentTrustPackage.swift: exists=True
CellProtocol/Sources/CellBase/Agreement/EffectReceipt.swift: exists=True
CellProtocol/Sources/CellBase/Agreement/ReceiptSignature.swift: exists=True
CellScaffold/Sources/App: webFetch.receipts count=0
CellScaffold/Sources/App: ai.receipts count=0
CellScaffold/Sources/App: class AgentTrustPackageCell count=0
CellScaffold/Sources/App: class AgentTrustPackageCellTests count=0
CellScaffold/Sources/App: class AgentTrustPackageApprovalTests count=0
CellScaffold/Sources/App: class AgentTrustPackageAuditTests count=0
CellScaffold/Sources/App: trustPackage.fleet.stop count=0
CellScaffold/Tests/AppTests: webFetch.receipts count=0
CellScaffold/Tests/AppTests: ai.receipts count=0
CellScaffold/Tests/AppTests: class AgentTrustPackageCell count=0
CellScaffold/Tests/AppTests: class AgentTrustPackageCellTests count=0
CellScaffold/Tests/AppTests: class AgentTrustPackageApprovalTests count=0
CellScaffold/Tests/AppTests: class AgentTrustPackageAuditTests count=0
CellScaffold/Tests/AppTests: trustPackage.fleet.stop count=0
```

Celleimplementasjon, lagerinnhenting, diff, norske audit-labels, `open.*`-referanser, fabrikkregistrering og de nye WP10-testene er derfor ikke implementert. WP5–WP9 er ikke rekonstruert som del av WP10. Eksisterende produksjonskode, tester, kontrakt og skeleton er uendret. Arbeidsmappe med forutsetningene er etterspurt under kjøringen.

Fixturen `audit-two-violations.receipts.json` har sju metadata-rader, forventet r-1042/new_destination og r-1043/credential_resolved, men bruker den syntetiske tekstmarkøren `"signature": "valid"`, forkortet pakke-digest og ingen `createdAt`. Ved gjenopptakelse må testoppsettet materialisere disse som ekte WP9-kvitteringer med testidentitet, signatur, bindings-digester og tidspunkt etter godkjenning. Tekstmarkøren er ikke signaturbevis. Ingen avvikstelling eller signaturverifikasjon mot produksjonsbanen er påstått utført.

### WP10 — bygg og målrettet baseline

Regel 9–10 fulgt. Cwd: `HAVEN/CellScaffold`.

```sh
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAuditTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Ekte byggutdata (full logg `/private/tmp/wp10-audit/build-baseline.log`, exit 0):

```text
Build complete! (23.85s)
```

Ekte komplette XCTest-utdata, alle tre kommandoer exit 0:

```text
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAuditTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
Test Suite 'Selected tests' started at 2026-09-09 02:05:19.795.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-09 02:05:19.796.
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-09 02:05:19.796.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'Selected tests' passed at 2026-09-09 02:05:19.796.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageCellTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
Test Suite 'Selected tests' started at 2026-09-09 02:05:19.795.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-09 02:05:19.796.
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-09 02:05:19.796.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'Selected tests' passed at 2026-09-09 02:05:19.796.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
$ xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
Test Suite 'Selected tests' started at 2026-09-09 02:05:19.795.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-09 02:05:19.796.
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-09 02:05:19.796.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
Test Suite 'Selected tests' passed at 2026-09-09 02:05:19.796.
	 Executed 0 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
```

**0 utførte tester i hvert filter = blocked, ikke bestått akseptanse eller regresjon.** Klassene finnes ikke i denne arbeidskopien. Direkte XCTest dekker ikke Swift Testing-mål. Bygget hadde eksisterende advarsler om skrivebeskyttet manifestcache og CellProtocol dependency identity; det fullførte uten kildeendringer.

### WP10 — full bundle

Fullført mot uendret arbeidskopi, exit 1:

```sh
# cwd HAVEN/CellScaffold
xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

**2046 tester, 11 hoppet over, 151 feilrapporter (9 unexpected), 46 røde testnavn, 779.519 s.** Eksakt navnesammenligning med WP0c (2046 tester / 46 røde navn) viser ingen nye eller manglende røde navn, og samme sett av alle 2046 testnavn. De tre ekstra assertion-feilrapportene mot baseline 148 ligger alle i den allerede røde `PortholeConfigurationLoadingTests.testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction` (2 → 5), samme kjente variasjon som WP2/WP5/WP7. Ingen tester er endret eller svekket.

Dette er regresjonsmåling av den tilgjengelige arbeidskopien, ikke WP10-akseptanse. WP2–WP7-testene fra WP7s tidligere bundle med 2133 tester er ikke til stede; dagens 2046 er derfor ikke bevis på at den senere kandidatleveransen virker. Swift Testing er ikke dekket.

Maskinelt generert sammenligning fra ekte `Test Case … failed/started`-linjer:

```json
{
  "baseline": "/private/tmp/wp0c-baseline-ujg4x43v/CellScaffold-xctest.log",
  "current": "/private/tmp/wp10-audit/full-bundle.log",
  "baselineFailedNames": 46,
  "currentFailedNames": 46,
  "newFailedNames": [],
  "missingFailedNames": [],
  "baselineTestNames": 2046,
  "currentTestNames": 2046,
  "addedTestNames": [],
  "missingTestNames": [],
  "finalExecutedLine": "\t Executed 2046 tests, with 11 tests skipped and 151 failures (9 unexpected) in 779.403 (779.519) seconds"
}
```

Alle ekte `Executed`-linjer fra fullkjøringen, uten redigering. Full rålogg: `/private/tmp/wp10-audit/full-bundle.log`; uttrekk: `executed-lines.log`; sammenligning: `failure-comparison.json` i samme mappe.

```text
	 Executed 14 tests, with 4 tests skipped and 12 failures (0 unexpected) in 1.912 (1.913) seconds
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.096 (0.098) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.396 (0.397) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.020 (0.020) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.016 (0.016) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.254 (0.254) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.023 (0.024) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.997 (0.998) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.078 (1.078) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.035 (0.035) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.424 (0.424) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.443 (0.443) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.161 (0.161) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.474 (0.476) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.276 (0.276) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.111 (0.111) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.195 (0.195) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.022 (0.023) seconds
	 Executed 21 tests, with 0 failures (0 unexpected) in 0.177 (0.178) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.644 (0.644) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.226 (0.226) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.527 (0.527) seconds
	 Executed 40 tests, with 14 failures (0 unexpected) in 0.972 (0.979) seconds
	 Executed 1 test, with 3 failures (0 unexpected) in 0.289 (0.289) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.008 (0.008) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 4.614 (4.614) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.053 (0.053) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.785 (0.785) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.123 (0.123) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.205 (0.205) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 6 tests, with 2 failures (0 unexpected) in 9.834 (9.835) seconds
	 Executed 20 tests, with 0 failures (0 unexpected) in 0.055 (0.056) seconds
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.105 (0.105) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 31 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.616 (0.619) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 11 tests, with 18 failures (1 unexpected) in 3.505 (3.506) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.231 (0.232) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.142 (0.143) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.058 (0.058) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.122 (0.123) seconds
	 Executed 21 tests, with 0 failures (0 unexpected) in 0.060 (0.060) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.018 (0.018) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.037 (0.037) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.008 (0.008) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.586 (0.587) seconds
	 Executed 10 tests, with 7 failures (0 unexpected) in 3.901 (3.901) seconds
	 Executed 48 tests, with 0 failures (0 unexpected) in 0.466 (0.468) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.006 (0.007) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.099 (0.100) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.158 (0.159) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.152 (0.153) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.047 (0.048) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 4.216 (4.216) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.234 (0.234) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.070 (0.070) seconds
	 Executed 11 tests, with 1 failure (1 unexpected) in 0.122 (0.122) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.019 (0.019) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.165 (0.165) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.042 (0.042) seconds
	 Executed 3 tests, with 7 failures (0 unexpected) in 0.065 (0.065) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.046 (0.046) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 1.327 (1.328) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.023 (0.023) seconds
	 Executed 15 tests, with 0 failures (0 unexpected) in 0.370 (0.371) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.367 (0.367) seconds
	 Executed 10 tests, with 1 failure (1 unexpected) in 0.048 (0.048) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.047 (0.047) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
	 Executed 2 tests, with 1 failure (0 unexpected) in 0.033 (0.033) seconds
	 Executed 68 tests, with 0 failures (0 unexpected) in 4.851 (4.854) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.281 (0.281) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.093 (0.093) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.182 (0.182) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 2 tests, with 1 failure (1 unexpected) in 0.011 (0.011) seconds
	 Executed 39 tests, with 21 failures (0 unexpected) in 43.399 (43.401) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.019 (0.020) seconds
	 Executed 31 tests, with 0 failures (0 unexpected) in 1.683 (1.684) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 17 tests, with 2 tests skipped and 1 failure (0 unexpected) in 0.445 (0.446) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 1.556 (1.557) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.018 (0.018) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 5 tests, with 9 failures (0 unexpected) in 1.063 (1.064) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 1.948 (1.949) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.199 (0.199) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.040 (0.041) seconds
	 Executed 19 tests, with 0 failures (0 unexpected) in 0.087 (0.088) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.024 (0.024) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.213 (0.213) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.207 (0.208) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.402 (0.402) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.017 (0.017) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.007 (0.007) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.100 (0.101) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.251 (0.252) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 1.342 (1.342) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
	 Executed 36 tests, with 0 failures (0 unexpected) in 1.148 (1.150) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.030 (0.030) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 0.502 (0.504) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.158 (0.158) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.089 (0.089) seconds
	 Executed 6 tests, with 1 failure (0 unexpected) in 0.081 (0.081) seconds
	 Executed 20 tests, with 0 failures (0 unexpected) in 1.089 (1.090) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 11.646 (11.647) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.008 (0.008) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.590 (0.590) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.118 (0.118) seconds
	 Executed 4 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.007 (0.007) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.002 (0.003) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.037 (0.037) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.029 (0.030) seconds
	 Executed 11 tests, with 14 failures (0 unexpected) in 15.595 (15.597) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.437 (0.437) seconds
	 Executed 1 test, with 4 failures (0 unexpected) in 0.223 (0.223) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.002) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 26 tests, with 3 failures (0 unexpected) in 0.126 (0.127) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.052 (0.052) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.200 (0.200) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 2.221 (2.223) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.053 (0.053) seconds
	 Executed 25 tests, with 0 failures (0 unexpected) in 0.262 (0.263) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.066 (0.067) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.032 (0.032) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 3.113 (3.114) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.048 (0.049) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.019 (0.019) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.271 (0.271) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.022 (0.022) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.035 (0.035) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 1.974 (1.975) seconds
	 Executed 14 tests, with 0 failures (0 unexpected) in 1.866 (1.867) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.591 (0.591) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.004 (0.004) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.020 (0.020) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 31.222 (31.223) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.170 (0.170) seconds
	 Executed 70 tests, with 0 failures (0 unexpected) in 10.860 (10.863) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.621 (0.622) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.019 (0.019) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.099 (0.099) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.008 (0.008) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
	 Executed 45 tests, with 5 failures (0 unexpected) in 538.305 (538.309) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 10.909 (10.910) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.122 (0.122) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 3.241 (3.245) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.011 (0.011) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.006 (0.006) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.063 (0.063) seconds
	 Executed 15 tests, with 0 failures (0 unexpected) in 2.700 (2.701) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.005 (0.006) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.012 (0.012) seconds
	 Executed 4 tests, with 19 failures (1 unexpected) in 7.192 (7.192) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.043 (0.043) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.036 (0.036) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.134 (0.134) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.008 (0.008) seconds
	 Executed 13 tests, with 0 failures (0 unexpected) in 0.119 (0.119) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.951 (0.951) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.020 (0.020) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.004 (0.005) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.009 (0.009) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.994 (0.995) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.074 (0.074) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.020 (0.020) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.003 (0.003) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.005 (0.005) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.026 (0.026) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.476 (1.477) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.010 (0.010) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.025 (0.025) seconds
	 Executed 12 tests, with 0 failures (0 unexpected) in 0.028 (0.029) seconds
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.039 (0.039) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 1.633 (1.633) seconds
	 Executed 15 tests, with 0 failures (0 unexpected) in 2.873 (2.874) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.054 (0.054) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.002 (0.002) seconds
	 Executed 9 tests, with 1 test skipped and 0 failures (0 unexpected) in 0.016 (0.017) seconds
	 Executed 11 tests, with 0 failures (0 unexpected) in 0.015 (0.015) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.022 (0.022) seconds
	 Executed 3 tests, with 2 failures (0 unexpected) in 0.328 (0.328) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.810 (0.811) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.046 (0.046) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 0.001 (0.001) seconds
	 Executed 16 tests, with 1 failure (0 unexpected) in 0.218 (0.219) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.025 (0.025) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 0.013 (0.013) seconds
	 Executed 1 test, with 1 test skipped and 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 5 tests, with 0 failures (0 unexpected) in 1.012 (1.012) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.215 (0.215) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.640 (0.640) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.000 (0.001) seconds
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.032 (0.032) seconds
	 Executed 1 test, with 0 failures (0 unexpected) in 0.000 (0.000) seconds
	 Executed 2 tests, with 0 failures (0 unexpected) in 0.014 (0.014) seconds
	 Executed 19 tests, with 3 failures (3 unexpected) in 2.434 (2.435) seconds
	 Executed 9 tests, with 0 failures (0 unexpected) in 0.030 (0.031) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 0.099 (0.099) seconds
	 Executed 28 tests, with 1 test skipped and 0 failures (0 unexpected) in 1.306 (1.310) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.067 (0.067) seconds
	 Executed 6 tests, with 0 failures (0 unexpected) in 2.853 (2.854) seconds
	 Executed 3 tests, with 0 failures (0 unexpected) in 0.022 (0.022) seconds
	 Executed 8 tests, with 0 failures (0 unexpected) in 0.031 (0.032) seconds
	 Executed 16 tests, with 0 failures (0 unexpected) in 0.021 (0.022) seconds
	 Executed 24 tests, with 1 failure (1 unexpected) in 2.367 (2.368) seconds
	 Executed 7 tests, with 0 failures (0 unexpected) in 8.083 (8.084) seconds
	 Executed 2046 tests, with 11 tests skipped and 151 failures (9 unexpected) in 779.403 (779.516) seconds
	 Executed 2046 tests, with 11 tests skipped and 151 failures (9 unexpected) in 779.403 (779.519) seconds
```

## WP10 — sluttmelding

**Blocked — WP10 er ikke implementert eller akseptert.** Oppgitt CellScaffold-arbeidskopi mangler `AgentTrustPackageCell`, konfigurasjonsfabrikken, approval-koden og de påkrevde regresjonstestene. WP9 leverte signerte modeller i CellProtocol, men siste WP9-sluttmelding og nytt kildesøk bekrefter at celleutstedelse og append-only `webFetch.receipts`/`ai.receipts` ikke er levert her. Uten disse forutsetningene kan WP10 ikke samle kvitteringer, diff-e mot et godkjent snapshot eller koble navigasjon og «etter»-flaten til den eksisterende cellen innenfor «kun WP10».

Regel 10-bygg er grønt (**23.85 s**). De tre bestilte testfiltrene kjører **0 tester hver**, som er blocked, ikke bestått. Full CellScaffold-XCTest er kjørt: **2046 tester / 11 hoppet over / 151 feilrapporter / nøyaktig samme 46 røde testnavn som WP0c / ingen nye navn**, **779.519 s**. Samme sett av alle testnavn som WP0c; kjent Mermaid-variasjon 2 → 5 feilrapporter. Swift Testing er ikke dekket. Ekte bygg-/testutdata og kildeevidens står under [Diff](#diff).

Kun denne WP10-dokumentasjonen i `TESTRESULT.md` og én linje i `STATUS.md` er endret. Ingen produksjonskode, tester, kontrakt eller skeleton er endret; ingen git, WP11-arbeid eller deployment. Gjenopptakelse trenger en tilgjengelig arbeidsmappe med WP2–WP7-kandidaten og fullført WP9-celleintegrasjon. Kandidatens dokumenterte plassering er [handoff/KANDIDATGREN.md](handoff/KANDIDATGREN.md); den er ikke hentet ut eller byttet inn. Avklaringen om riktig arbeidsmappe fikk ikke svar under kjøringen.


## WP8 — sluttmelding

**WP8 er fullført.** Regel 11-forhåndssjekken bestod; aktiv gren ved den pålagte kontrollen var `pdd/tillitspakke-agentflaate`. Deretter ingen git-kommandoer, grenbytte eller commit.

Ny `AgentTrustPackageAntiPurposeTests.swift` kjører fire injeksjonstekster gjennom produksjonens PurposeBound/AIGateway-bane, videre som neste prompt og agentforsøk på SET/fetch. Ceiling- og pakke-digest samt avtalte request-bytes er uendret; ingen tools åpnes; fire eieravviste justeringer telles og fire hendelser observeres. Håndlaget «godkjent pakke», også med korrekt digest og ekstra fetch-Grant, gir ingen tilgang; state viser «ikke avledet», og approve gir `package_not_derived`. Positive kontroller krever faktisk eiergodkjenning og separat signert Agreement.

To testavdekkede hull er minimalt tettet i `AgentTrustPackageCell.swift`: S-teller med snapshot/Explore og celleutstedte avvisningshendelser, samt avvisningstilstand for innlagt pakke-JSON frem til eksplisitt eierregenerering. `AgentTrustPackageContract.swift` og `contract/agent_trust_package_contract_v0.json` beskriver tillegget. Ingen øvrig produksjonskode eller eksisterende test er endret. I tillegg er denne `TESTRESULT.md` oppdatert og én linje lagt til i `STATUS.md`.

Baseline **34/34**, endelig **66/66 XCTest-tester grønne**, hvorav **36/36** i de tre bestilte klassene. Endelig regel 10-bygg: **49.87 s**. Rødt-før/grønt-etter og ekte `Executed`-linjer står under [Injeksjon](#injeksjon) og [Pakke gir ikke rett](#pakke-gir-rett). Full bundle er ikke påkrevd og ikke kjørt; Swift Testing er ikke dekket. Tellerpersistens er verifisert gjennom snapshot/reload, ikke ved I/O-feil. Ingen live modell, eksternt nettverk eller senere WP er utført.

## WP9b — sluttmelding

WP9b er fullført i CellScaffold: eier-signerte effekt-/beslutningskvitteringer, append-only `webFetch.receipts` / `ai.receipts` med eier-GET (`r---`) og komplette Explore-skjemaer. Ingen sti/query/innhold i kvitteringene. Verifisering, manipulasjonsvern, owner-denial, faktisk byteopptelling, pakke-/ceiling-binding, cache, redirect, feil og snapshot/reload er testet.

Siste bygg grønt (17.00 s). Påkrevde testklasser: 9 + 17 + 17 = **43/43 grønne**; ekstra AI-regresjon **49/49 grønne**, totalt **92/92**. Full bundle ikke påkrevd/ikke kjørt; Swift Testing ikke dekket. WP9s CellProtocol-utdata er bevart under [Kvittering](#receipt), med faktiske WP9b-utdata lagt til. Globale Explore-auditfunn og lagrings-/AI-input-avgrensninger er beskrevet samme sted.

CellScaffold er fortsatt på `pdd/tillitspakke-agentflaate`. Ingen commit, grenbytte eller push. WP10 kan fortsette mot de to nye kvitterings-GET-ene.

## WP10 — sluttmelding

**WP10 — etterprøving er implementert og kontrollert.** Regel 11 bestod på `pdd/tillitspakke-agentflaate`. Bare den pålagte innledende grenlesingen er brukt; ingen commit, grenbytte, push eller øvrig git.

`AgentTrustPackageCell` samler og bevarer WP9-kvitteringer per flåte, kontrollerer signaturer og bindings-/ceiling-avvik mot bevart, digest-verifisert godkjent pakke og leverer norske audit-labels. Den normative fixturen gir nøyaktig `new_destination` for r-1042 og `credential_resolved` for r-1043: **7 effekter, 5 innenfor, 2 avvik**. Manipulert/usignert kvittering gir `unknown_policy_version` og «usignert/ugyldig». Manglende godkjenning/kilde/snapshot gir ingen falsk «Overholdt»-status.

`open.receipt`, `open.package` og `open.instruction` returnerer bare navigasjonsreferanser; oppslag er testet. Egen `configuration.audit` og factory-skeleton samsvarer med godkjent «etter»-JSON. Endrede kodefiler: `AgentTrustPackageCell.swift`, ny `AgentTrustPackageAudit.swift`, `AgentTrustPackageContract.swift`, `AgentTrustPackageConfigurationFactory.swift`, ny `AgentTrustPackageAuditTests.swift` og ett oppdatert WP2-testtilfelle i `AgentTrustPackageCellTests.swift`. PDD-kontrakten, denne rapporten og én linje i STATUS er avstemt.

Siste bygg: **18.45 s, grønt**. Nye + eksisterende påkrevde klasser: **43/43 grønne**. Full CellScaffold-XCTest: **2154 tester, 11 hoppet over, 151 feilrapporter (9 unexpected), samme 46 røde testnavn som baseline, ingen nye, ingen bortfalte baseline-tester**, **827.281 s**. Fullkjøringen gikk før siste ordlydspresisering for redirect; sluttbygget og 43/43 er kjørt etter den. Faktiske `Executed`-linjer og navnesammenligning står under [Diff](#diff). Swift Testing er ikke dekket.

Avgrensninger er dokumentert under #diff: AI-v1 gir digester/signerte kontroller, ikke en rekonstruerbar route; WebFetch lagrer ikke full URL, redirect-mål, alias eller caller. Journalen er append-only via API, ikke slettesikker; snapshot/reload er testet. Eksisterende Anthropic-avslag i core-autorisatorens valg av første ceiling er observert og dokumentert, ikke rettet i WP10. Ingen Porthole-/Binding-paritet eller senere WP er utført.


## WP12 — sluttmelding

**WP12 — docs i samme endring er fullført**, 2026-09-09, for `purpose://quality.docs-in-same-change` og `purpose://cell.contract-explicit`. Forhåndssjekken fant begge navngitte filer (`AgentTrustPackageCell.swift` og `WebFetchCeilingTests.swift`), og den pålagte `git branch --show-current` i CellScaffold ga `pdd/tillitspakke-agentflaate`. Intet filantall ble brukt som kriterium. Ingen senere git-kommando, grenbytte, kodeendring eller bygg er utført.

Levert: `Book/36_Agent_Trust_Package.md` med «Last verified against code: 2026-09-09», projeksjonens kildegrenser, eksakte keypaths/Grants, kanonisk digest, innsnevring, eier-signert godkjenning, eksplisitt flåtebinding/fail-closed port, WebFetch-matcheregler, signerte kvitteringer og etterprøvingsdiff. `lesson.planned-documented-as-implemented` er anvendt: Porthole-paritet, per-Grant V2, flerpartssignering og distribuert revokasjon er under «Ikke implementert», sammen med de øvrige dokumenterte kilde-/journalgrensene. WP1–WP10-rapportens siste sluttmeldinger og faktisk kildekode er brukt; tidligere blocked-resultater er historikk.

`P/contract/agent_trust_package_contract_v0.json` har bare endret toppnivåets `status`; `Book/agent_trust_package_contract_v0.json` er en byteidentisk kopi. Alle 6 deklarerte GET- og 10 SET-keypaths er implementert etter WP10; ingen av dem er fortsatt en `not-implemented`-stub. Fremtidige funksjoner merkes separat uten å dikte opp keypaths. Status beskriver også to konfigurasjons-GET-er, målcellens operasjoner og fixture-referansenes base i PDD-mappen. Dette er dokumentert implementasjonsstatus, ikke nye runtime-operasjoner.

Book/04 §8 har én kort peker til kapittel 36 som erstatter det foreldede WP9-integrasjonsforbeholdet. Book/23 §8 har én kort kandidatpeker; ingen noder er promotert til kanonisk taksonomi, som krever Kjetil. `book_catalog.json` har én ny oppføring for kapittel 36, i tråd med dokumentasjonsferdighetens krav om katalogføring. `ACCEPT.md#docs` har avkrysninger og tabell som knytter hver doc-diff til kodeendringer og WP-evidens; STATUS har én ny linje. WP2-stublisten i ACCEPT er eksplisitt forklart som historikk.

**test.docs-updated: bestått.** Inline Python-kontrollen leste Swift-kontraktens konstanter/operasjonslister og sammenlignet keypaths og Grants mot begge JSON-kontraktene og Book-tabellen, kontrollerte lenkemål/ankere i nye og endrede Markdown-linjer, fixture-referanser, eksplisitte mangler og at eksisterende katalogoppføringer var bevart. Ekte utdata:

```json
{
  "result": "passed",
  "declaredGet": 6,
  "declaredSet": 10,
  "grantsMatchSwiftContract": true,
  "contractCopiesByteIdentical": true,
  "onlyPddContractStatusChanged": true,
  "fixturesResolved": 6,
  "newOrChangedMarkdownLinksChecked": 40,
  "catalogPreservesPriorEntries": true,
  "explicitNotImplementedBoundaries": true,
  "buildOrXCTestRun": false
}
```

Eksisterende Docs-MCP-kontroll, cwd `CellProtocolDocuments`, exit 0:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 Tools/HavenDocsMCP/haven_docs_mcp.py --search 'cell:///AgentTrustPackage'
```

Resultat: 8 søketreff; første treff er `book-36-agent-trust-package`, sti `Book/36_Agent_Trust_Package.md`, ressurs `haven-docs://book/book-36-agent-trust-package`. Dette verifiserer lokal dokumentoppdagelse, ikke en Porthole-flate. Midlertidig før-kopi/diff og kontrollutdata: `/private/tmp/wp12-docs-review/` (`docs.diff`, `validation.json`, `catalog-search.json`); nødvendig resultatevidens er bevart her.

Avgrensning: ingen Swift-bygg, XCTest, Swift Testing, live modell, deploy, WP11-paritet eller WP13-akseptanse er kjørt i WP12. Tidligere kjøringer er referert med sine dokumenterte avvik; WP10s fulle bundle er fortsatt rød på samme 46 baseline-testnavn. G3 og kanonisk formålstaksonomi er urørt. Kandidatgrenen er ikke byttet.

## WP13 — e2e <a id="e2e"></a>

2026-09-09, `purpose://candidate.tillitspakke-agentflaate.root`, `test.tp.e2e`.

**Bestått med fixture-modell, ingen live leverandørkall.** Ny [AgentTrustPackageE2ETests.swift](../../../CellScaffold/Tests/AppTests/AgentTrustPackageE2ETests.swift) kjører produksjonscellene AgentTrustPackage, PurposeBoundAIGateway (AIGateway-varianten med startport/kvitteringer), WebFetch, ScopedCredential og EntityAnchor i en isolert resolver med ephemeral eieridentitet. Ingen produksjonskode eller eksisterende test er endret i WP13.

Regel 11 bestod: begge navngitte filer fantes, og innledende `git -C CellScaffold branch --show-current` ga `pdd/tillitspakke-agentflaate`. Ingen filantall ble brukt som kriterium. Ingen senere git-kommandoer eller grenbytte. Testet kildefils SHA-256 og fixture-avgrensning er bevart i [run-context.json](evidence/wp13/run-context.json).

Før kodeendringen: regel 10-bygg grønt, `Build complete! (23.43s)`, veggtid 25.52 s, exit 0. Relevante eksisterende klasser AgentTrustPackageAuditTests og AgentTrustPackageApprovalTests: 27/27 grønne. Kommandoer, cwd `CellScaffold`:

```sh
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageAuditTests,AppTests.AgentTrustPackageApprovalTests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Ekte baseline-utdata (komplette logger: [bygg](evidence/wp13/cellscaffold-baseline-build.log), [tester](evidence/wp13/cellscaffold-baseline-tests.log)):

```text
Test Suite 'Selected tests' started at 2026-09-09 06:33:56.432.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-09 06:33:56.434.
Test Suite 'AgentTrustPackageApprovalTests' started at 2026-09-09 06:33:56.434.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testAdjustAfterApprovalDeniesUntilNewApprovalAndShowsDeviation]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testAdjustAfterApprovalDeniesUntilNewApprovalAndShowsDeviation]' passed (0.160 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testAdmittedNonOwnerStillRequiresApprovalAndCannotReadOrCreateIt]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testAdmittedNonOwnerStillRequiresApprovalAndCannotReadOrCreateIt]' passed (0.050 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testApprovalAndBindingExploreContractsAreExplicitUnderStrictMode]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testApprovalAndBindingExploreContractsAreExplicitUnderStrictMode]' passed (0.046 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testApprovedFetchStillRequiresWhitelistAndOtherExistingLimits]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testApprovedFetchStillRequiresWhitelistAndOtherExistingLimits]' passed (0.065 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testApproveSignsEntireSnapshotWithOwnerKeyAndCommitsVerifiableEntityRecord]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testApproveSignsEntireSnapshotWithOwnerKeyAndCommitsVerifiableEntityRecord]' passed (0.057 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testBindingsSurviveReloadAndMalformedBindingCannotSilentlyUnbind]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testBoundWebFetchWithoutApprovalDeniedBeforeNetworkOrCredentialLookup]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testBoundWebFetchWithoutApprovalDeniedBeforeNetworkOrCredentialLookup]' passed (0.015 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testCompleteCeilingAndInstanceAreBoundEvenWhenDisplayProjectionUnchanged]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testCompleteCeilingAndInstanceAreBoundEvenWhenDisplayProjectionUnchanged]' passed (0.047 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testFailedPersistentUnbindRetainsClosedPort]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testFailedPersistentUnbindRetainsClosedPort]' passed (0.019 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testForgedApprovalSignatureCannotOpenPortAfterReload]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testForgedApprovalSignatureCannotOpenPortAfterReload]' passed (0.052 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testGatewayStartPortDeniesBeforeCredentialsAndDetectsPolicyChanges]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testMissingWrongFleetAndUnavailablePackageFailClosed]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testMissingWrongFleetAndUnavailablePackageFailClosed]' passed (0.017 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testOtherPublicAndForgedRequestersCannotApproveStopReadOrRebind]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testOtherPublicAndForgedRequestersCannotApproveStopReadOrRebind]' passed (0.054 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testPackageNotDerivedAndUnavailableArchiveCannotApprove]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testPackageNotDerivedAndUnavailableArchiveCannotApprove]' passed (0.016 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testStopRevokesAndRetainsHistoryAcrossSnapshotReload]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testUnboundCellsKeepExistingBehavior]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testUnboundCellsKeepExistingBehavior]' passed (0.016 seconds).
Test Case '-[AppTests.AgentTrustPackageApprovalTests testWrongAndStaleDigestRejectedAgainstRegeneratedSources]' started.
Test Case '-[AppTests.AgentTrustPackageApprovalTests testWrongAndStaleDigestRejectedAgainstRegeneratedSources]' passed (0.028 seconds).
Test Suite 'AgentTrustPackageApprovalTests' passed at 2026-09-09 06:33:57.262.
	 Executed 17 tests, with 0 failures (0 unexpected) in 0.827 (0.828) seconds
Test Suite 'AgentTrustPackageAuditTests' started at 2026-09-09 06:33:57.262.
Test Case '-[AppTests.AgentTrustPackageAuditTests testApprovedSnapshotAndCollectedReceiptsSurviveAdjustmentSelectionStopAndReload]' started.
Test Case '-[AppTests.AgentTrustPackageAuditTests testApprovedSnapshotAndCollectedReceiptsSurviveAdjustmentSelectionStopAndReload]' passed (0.104 seconds).
Test Case '-[AppTests.AgentTrustPackageAuditTests testAuditExploreAndAfterSkeletonMatchAndOwnerProofIsRequired]' started.
Test Case '-[AppTests.AgentTrustPackageAuditTests testEveryViolationKindAndMismatchedBindingAreDetected]' started.
Test Case '-[AppTests.AgentTrustPackageAuditTests testEveryViolationKindAndMismatchedBindingAreDetected]' passed (0.054 seconds).
Test Case '-[AppTests.AgentTrustPackageAuditTests testFixtureTwoDeniedAttemptsAreExactlyTwoViolationsSevenEffectsFiveWithin]' started.
Test Case '-[AppTests.AgentTrustPackageAuditTests testFixtureTwoDeniedAttemptsAreExactlyTwoViolationsSevenEffectsFiveWithin]' passed (0.073 seconds).
Test Case '-[AppTests.AgentTrustPackageAuditTests testNoApprovalHasNothingToAuditAndNoFalseOverholdt]' started.
Test Case '-[AppTests.AgentTrustPackageAuditTests testNoApprovalHasNothingToAuditAndNoFalseOverholdt]' passed (0.016 seconds).
Test Case '-[AppTests.AgentTrustPackageAuditTests testOldValidReceiptsExcludedAndChangedSameIDCannotOverwriteArchive]' started.
Test Case '-[AppTests.AgentTrustPackageAuditTests testOldValidReceiptsExcludedAndChangedSameIDCannotOverwriteArchive]' passed (0.057 seconds).
Test Case '-[AppTests.AgentTrustPackageAuditTests testOpenActionsReturnOnlyReferencesAndTargetsCanBeRead]' started.
Test Case '-[AppTests.AgentTrustPackageAuditTests testOpenActionsReturnOnlyReferencesAndTargetsCanBeRead]' passed (0.111 seconds).
Test Case '-[AppTests.AgentTrustPackageAuditTests testProductionFetchAndAIReceiptsAreCollectedThroughOwnerGETs]' started.
Test Case '-[AppTests.AgentTrustPackageAuditTests testTamperedAndUnsignedReceiptsAreInvalidUnknownPolicyEvenWithOldForgedTime]' started.
Test Case '-[AppTests.AgentTrustPackageAuditTests testTamperedAndUnsignedReceiptsAreInvalidUnknownPolicyEvenWithOldForgedTime]' passed (0.049 seconds).
Test Case '-[AppTests.AgentTrustPackageAuditTests testUnavailableSourcesAndInvalidApprovedSnapshotCannotClaimCompliance]' started.
Test Case '-[AppTests.AgentTrustPackageAuditTests testUnavailableSourcesAndInvalidApprovedSnapshotCannotClaimCompliance]' passed (0.046 seconds).
Test Suite 'AgentTrustPackageAuditTests' passed at 2026-09-09 06:33:57.914.
	 Executed 10 tests, with 0 failures (0 unexpected) in 0.651 (0.652) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-09 06:33:57.914.
	 Executed 27 tests, with 0 failures (0 unexpected) in 1.479 (1.480) seconds
Test Suite 'Selected tests' passed at 2026-09-09 06:33:57.914.
	 Executed 27 tests, with 0 failures (0 unexpected) in 1.479 (1.482) seconds
real 3.59
user 1.42
sys 0.17
```

Testforløp og hva som faktisk er bevist:

1. Fixture-modellen kjøres én gang gjennom produksjonens `PurposeBoundAIGatewayCell.invokePurposeBound`; den returnerer tre URL-forslag. AI-kvitteringen er celleutstedt og signaturverifisert. Dette er forberedelse **før flåtebinding/godkjenning**, ikke en post-godkjent effekt. Modellen eller dens tekst får ingen rettigheter.
2. Flåten settes til PurposeBoundAIGateway + WebFetch + ScopedCredential. Begge startportene bindes til pakken. Den opprinnelige whitelisten er `*.digipomps.org`, `*.wikipedia.org`, `docs.claude.com`. Uendret regenerering må gi samme digest.
3. `trustPackage.adjust.whitelist` fjerner `docs.claude.com`. Ny pakke-digest må være forskjellig fra før og stemme med kanonisk beregning. Faktisk WebFetch-ceiling må ha de to gjenværende mønstrene, GET, credentials=false og followRedirects=false.
4. Godkjenning med den gamle digesten nektes med `digest_mismatch`. Godkjenning med den nye blir issuer-signert og re-verifisert mot EntityAnchor-record/receipt; den binder den nye pakkedigesten og WebFetch-policyen. Audit er tom ved start.
5. Testdriveren sender de tre returnerte forslagene gjennom ekte `web.fetch`-SET: `research.digipomps.org` og `en.wikipedia.org` blir `fetched`; det fjernede `docs.claude.com` blir `denied(host_not_whitelisted)`. URLProtocol mottar nøyaktig to requests. Den tredje nektes før transporten.
6. `trustPackage.state.audit` og audit inni hel-state stemmer overens: nøyaktig én avviksrad av typen `new_destination`, tre effekter, to innenfor og ett nektet forsøk. Alle tre effektkvitteringer har nye unike ID-er, korrekt pakke-/ceiling-binding og verifiserbar signatur via eierens **offentlige** identitet. Endret digest gir ugyldig signatur. De to fullførte har faktisk fixture-byteantall; den nektede har 0 bytes og `notAttempted`. Gjentatte lesinger bevarer tre arkivposter; pakken endres ikke ved kjøringen.

**Avgrensning:** Ingen generell modell→celle-verktøyløkke finnes i denne PDD-en; XCTest sender forslagene eksplisitt på eierens autoriserte bane. Den faktiske flåten bruker PurposeBoundAIGateway, hvis gjeldende rute/systeminstruksjon ikke kan leses ut som lagret kilde; e2e-testen fyller ikke dette dokumenterte kildegapet. Provider-fixture og URLProtocol erstatter leverandør/nettverk, og ScopedCredential inneholder ingen ekte hemmeligheter. Godkjenningen har sekundoppløsning uten injiserbar klokke; testen venter 1.1 s før godkjenningen og asserter at den gyldige AI-forberedelseskvitteringen er eldre, slik at post-godkjent audit teller de tre fetch-forsøkene. Dette er API-e2e, ikke Porthole-/Binding-paritet, persistent prosessrestart eller live modell-e2e. Ekte modellkjøring gjenstår separat når Kjetil har kreditt/nøkkel (§2 gjør fixture-modell tilstrekkelig for v1).

Første bygg av den nye testfilen feilet på escaped anførselstegn i en Swift-strenginterpolasjon og testhelperens håndtering av valgfritt SET-resultat. Bare testfilen ble rettet; ingen assertion ble svekket og ingen runtime-feil var observert. [Første bygglogg](evidence/wp13/cellscaffold-build-1.log), exit 1, 19.96 s. Neste regel 10-bygg var grønt: `Build complete! (9.75s)`, veggtid 10.73 s, exit 0 — [sluttbygg](evidence/wp13/cellscaffold-build-2.log).

Kommando, cwd `CellScaffold`, exit 0 — [full e2e-logg](evidence/wp13/cellscaffold-e2e-1.log):

```sh
xcrun --sdk macosx xctest -XCTest AppTests.AgentTrustPackageE2ETests .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Ekte utdata:

```text
Test Suite 'Selected tests' started at 2026-09-09 06:39:02.708.
Test Suite 'CellsContainerPackageTests.xctest' started at 2026-09-09 06:39:02.709.
Test Suite 'AgentTrustPackageE2ETests' started at 2026-09-09 06:39:02.709.
Test Case '-[AppTests.AgentTrustPackageE2ETests testFixtureModelGenerateNarrowApproveFetchAndAuditOneViolation]' started.
Test Case '-[AppTests.AgentTrustPackageE2ETests testFixtureModelGenerateNarrowApproveFetchAndAuditOneViolation]' passed (1.369 seconds).
Test Suite 'AgentTrustPackageE2ETests' passed at 2026-09-09 06:39:04.078.
	 Executed 1 test, with 0 failures (0 unexpected) in 1.369 (1.369) seconds
Test Suite 'CellsContainerPackageTests.xctest' passed at 2026-09-09 06:39:04.078.
	 Executed 1 test, with 0 failures (0 unexpected) in 1.369 (1.369) seconds
Test Suite 'Selected tests' passed at 2026-09-09 06:39:04.078.
	 Executed 1 test, with 0 failures (0 unexpected) in 1.369 (1.370) seconds
WP13_E2E fixtureProviderCalls=1 before=sha256:c457e5dac1f50c1fb736ed6cde5dd579dd40c40cdf7a9e4172e1c3e6ea7bbe63 after=sha256:b3d681d6185f82cf8a94579f95d91f262a6c6d31c09ef388df7796c55305bb9a approved=sha256:b3d681d6185f82cf8a94579f95d91f262a6c6d31c09ef388df7796c55305bb9a
WP13_E2E Siden godkjenning 2026-09-09T04:39:03Z: 3 effekter, 2 innenfor, 1 nektet. violation=new_destination signedVerified=3 networkRequests=2
real 3.13
user 0.26
sys 0.04
```

## WP13 — full regresjon <a id="regression"></a>

**test.regression: bestått etter kravet «ingen nye røde testnavn». Begge fulle XCTest-bundler er fortsatt røde på baseline-feilene.** Testene er bygget fra gjeldende arbeidstre før kjøring; bare WP13s nye testfil er tilsiktet kodeendring. CellProtocol og CellScaffold er kjørt i hver sin repo-rot med regel 10, uten `arch` eller `swift test`:

```sh
# cwd HAVEN/CellProtocol
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/CellProtocolPackageTests.xctest

# cwd HAVEN/CellScaffold
swift build --disable-sandbox --build-tests
xcrun --sdk macosx xctest .build/arm64-apple-macosx/debug/CellsContainerPackageTests.xctest
```

Byggkommandoene er kjørt direkte fra skall (ingen Python-wrapper/arkitekturoverstyring); hver kommando er målt med `/usr/bin/time -p`, og stdout/stderr er bevart i lenkede logger. De to fulle XCTest-bundlene ble kjørt sekvensielt. CellScaffolds sluttbygg nedenfor er det samme som ble brukt til både isolert e2e og full regresjon; testkildens SHA-256 er kontrollert uendret etter fullkjøringen.

| Repo | Bygg, ekte `Build complete!` | Veggtid bygg | Exit bygg | Bygglogg |
| --- | --- | ---: | ---: | --- |
| CellProtocol | 11.04 s | 11.98 s | 0 | [Logg](evidence/wp13/cellprotocol-build.log) |
| CellScaffold | 9.75 s | 10.73 s | 0 | [Logg](evidence/wp13/cellscaffold-build-2.log) |

Eksisterende advarsler om manifest-cache med skrivevern og motstridende CellProtocol-avhengighetsidentitet stopper ikke byggene. Første testkompileringsforsøk og rettingen i WP13 er dokumentert under [e2e](#e2e).

| Repo | WP0c total / røde navn | WP13 total | Bestått | Hoppet over | Feilrapporter (unexpected) | Røde navn | Nye røde navn | Bortfalte røde baseline-tester | Veggtid full kjøring | Exit XCTest |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |

| CellProtocol | 1060 / 6 | 1086 | 1072 | 8 | 6 (5) | 6 | 0 | 0 | 125.09 s | 1 |

| CellScaffold | 2046 / 46 | 2155 | 2098 | 11 | 150 (9) | 46 | 0 | 0 | 842.33 s | 1 |


`Executed` inkluderer hoppede tester; feilrapporter og røde testnavn er ulike mål. Direkte XCTest dekker **ikke Swift Testing**. Ingen skip er omtalt som verifisert grønt. Totaløkning mot WP0c er 26 i CellProtocol og 109 i CellScaffold; WP13 legger til én XCTest i CellScaffold. Øvrige tillegg er fra tidligere slicer. WP0c kjørte eksisterende bundler uten nytt bygg; det er de eksplisitt bestilte målte navnesettene vi sammenligner med, ikke en påstått grønn kildebaseline.

[compare_regression.py](evidence/wp13/compare_regression.py) henter baseline-navnene fra den opprinnelige #baseline-delen, krever komplette «All tests»-summer, sjekker at antall unike startede/avsluttede tester stemmer med XCTest-totalen, og sammenligner røde navn som mengder. Alle 6 + 46 baseline-røde tester ble faktisk kjørt igjen. Maskinresultatet er [regression-comparison.json](evidence/wp13/regression-comparison.json), med SHA-256 for begge fulle logger.

Kjøringen av sammenligningsskriptet, cwd HAVEN, exit 0:

```sh
python3 CellProtocolDocuments/Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/evidence/wp13/compare_regression.py
```

Ekte utdata:

```json
{
  "CellProtocol": {
    "baselineTotal": 1060,
    "total": 1086,
    "passed": 1072,
    "skipped": 8,
    "failureReports": 6,
    "unexpectedFailureReports": 5,
    "baselineRedCount": 6,
    "redCount": 6,
    "newRed": [],
    "resolvedRed": [],
    "absentBaselineRed": [],
    "wallSeconds": 125.09,
    "logSHA256": "131548d917cf7ec374d93e98a089a4146f7a7e67d81b035ec4e188855a159dd2"
  },
  "CellScaffold": {
    "baselineTotal": 2046,
    "total": 2155,
    "passed": 2098,
    "skipped": 11,
    "failureReports": 150,
    "unexpectedFailureReports": 9,
    "baselineRedCount": 46,
    "redCount": 46,
    "newRed": [],
    "resolvedRed": [],
    "absentBaselineRed": [],
    "wallSeconds": 842.33,
    "logSHA256": "4d46f1c4b9928ff15ed2acbea206545f5ba2006456315da7e2634cab17f7aa0c"
  }
}
```


### CellProtocol — ekte totalsummer og alle røde navn

[Full rålogg](evidence/wp13/cellprotocol-regression.log). Navnefiler sortert identisk, ett testnavn per linje for rad-for-rad-sammenligning: [WP0c](evidence/wp13/cellprotocol-baseline-red.txt) → [WP13](evidence/wp13/cellprotocol-red.txt). [Nye røde](evidence/wp13/cellprotocol-new-red.txt) og [tidligere røde som nå er grønne](evidence/wp13/cellprotocol-resolved-red.txt) er tomme.

```text
Test Suite 'CellProtocolPackageTests.xctest' failed at 2026-09-09 06:39:49.636.
	 Executed 1086 tests, with 8 tests skipped and 6 failures (5 unexpected) in 123.604 (123.787) seconds
Test Suite 'All tests' failed at 2026-09-09 06:39:49.636.
	 Executed 1086 tests, with 8 tests skipped and 6 failures (5 unexpected) in 123.604 (123.788) seconds
real 125.09
user 4.91
sys 0.81
```

Alle 6 røde testnavn, med ekte `failed`-linjer fra fullkjøringen:

```text
Test Case '-[CellBaseTests.AppleIdentityVaultKeyStorageTests testLegacyEmbeddedPrivateKeyMigratesToApplicationTagAndSigns]' failed (0.892 seconds).
Test Case '-[CellBaseTests.AppleIdentityVaultKeyStorageTests testLegacyEmbeddedPrivateKeyStillSigns]' failed (0.003 seconds).
Test Case '-[CellBaseTests.AppleIdentityVaultKeyStorageTests testScopedSecretDataStaysStableInUnsignedTestHost]' failed (0.013 seconds).
Test Case '-[CellBaseTests.EntityScannerAgreementSurfaceTests testAgreementTemplateExposesOnlyTheApprovedSurface]' failed (0.001 seconds).
Test Case '-[CellBaseTests.OID4VPSignedRequestTrustVerifierTests testVerifiesX509HashSignedRequest]' failed (0.002 seconds).
Test Case '-[CellBaseTests.OID4VPSignedRequestTrustVerifierTests testVerifiesX509SanDNSSignedRequest]' failed (0.001 seconds).
```


### CellScaffold — ekte totalsummer og alle røde navn

[Full rålogg](evidence/wp13/cellscaffold-regression.log). Navnefiler sortert identisk, ett testnavn per linje for rad-for-rad-sammenligning: [WP0c](evidence/wp13/cellscaffold-baseline-red.txt) → [WP13](evidence/wp13/cellscaffold-red.txt). [Nye røde](evidence/wp13/cellscaffold-new-red.txt) og [tidligere røde som nå er grønne](evidence/wp13/cellscaffold-resolved-red.txt) er tomme.

```text
Test Suite 'CellsContainerPackageTests.xctest' failed at 2026-09-09 06:55:19.347.
	 Executed 2155 tests, with 11 tests skipped and 150 failures (9 unexpected) in 841.890 (842.096) seconds
Test Suite 'All tests' failed at 2026-09-09 06:55:19.349.
	 Executed 2155 tests, with 11 tests skipped and 150 failures (9 unexpected) in 841.890 (842.099) seconds
real 842.33
user 764.46
sys 24.83
```

Alle 46 røde testnavn, med ekte `failed`-linjer fra fullkjøringen:

```text
Test Case '-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsHAVENTeachingSwarmAndAppendsProviderTurns]' failed (1.892 seconds).
Test Case '-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsLocalOnlyHAVENTeachingSwarmWithoutAPIKeys]' failed (0.006 seconds).
Test Case '-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelLocalBorealisChatsAgainstSharedBackend]' failed (0.006 seconds).
Test Case '-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelMixedHostedAndLocalChatsWithRouteCredentials]' failed (0.004 seconds).
Test Case '-[AppTests.ArendalsukaEventAtlasCellTests testDecodedParticipantProgramCanEnsureRuntimeBindingsBeforeStateRead]' failed (0.009 seconds).
Test Case '-[AppTests.ArendalsukaEventAtlasCellTests testParticipantPreviewReadsDecodedRegisteredAtlasWithoutJournalFallback]' failed (0.010 seconds).
Test Case '-[AppTests.ArendalsukaEventAtlasCellTests testParticipantProgramReadsAtlasPreviewWithoutPersistingUntilExplicitAction]' failed (0.008 seconds).
Test Case '-[AppTests.ArendalsukaEventAtlasCellTests testParticipantProgramUsesAtlasPreviewForMissingProgramInPartialOverlay]' failed (0.008 seconds).
Test Case '-[AppTests.ArendalsukaImportAuthorizationRoutesTests testAdminDelegatesIdentityBoundCredentialToNonAdminImporter]' failed (0.307 seconds).
Test Case '-[AppTests.BookReferenceRoutesTests testConferenceConnectionHubLifecycleSlugRouteRendersMermaidInline]' failed (4.415 seconds).
Test Case '-[AppTests.BookReferenceRoutesTests testConferenceOwnershipSlugRouteRendersMermaidInline]' failed (2.277 seconds).
Test Case '-[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview]' failed (0.404 seconds).
Test Case '-[AppTests.ChatMVPRoutesTests testPaidStateAndMessageRoutesAwaitDecodedChatReadiness]' failed (0.241 seconds).
Test Case '-[AppTests.ConferenceEntityDiscoveryCellTests testChatLaunchCellCanStartConversationAndProjectMessageFeedback]' failed (0.019 seconds).
Test Case '-[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionHandsOffCapturedLeadToSponsorOwnedFollowUp]' failed (0.030 seconds).
Test Case '-[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionUsesConsentBoundAggregateSignalsWhenAvailable]' failed (0.025 seconds).
Test Case '-[AppTests.ConferencePublishedContentCellTests testPublishedContentCellRecognizesStableOrganizerIdentityWhenVaultContextIsPoisoned]' failed (0.001 seconds).
Test Case '-[AppTests.ConferenceSchedulingCellTests testRouterDelegatesSharedMeetingRequestAndLocalExportToSchedulingCell]' failed (0.020 seconds).
Test Case '-[AppTests.ConferenceSponsorLeadAggregateCellTests testSponsorLeadAggregateSyncsConsentBoundParticipantsAndCapturesLead]' failed (0.008 seconds).
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionAcceptsStoredImportAccessVC]' failed (0.806 seconds).
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionSupportsAdminSessionAndRejectsMismatchedSignedProof]' failed (0.879 seconds).
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication]' failed (0.215 seconds).
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublishedApiReadsUseAgreementWithoutDebugAccess]' failed (0.228 seconds).
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testConferencePageAccessPolicies]' failed (0.223 seconds).
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testConferencePagesExposeCanonicalSurfaceMetadataForWebNavigator]' failed (0.216 seconds).
Test Case '-[AppTests.ConfigurationCatalogSkeletonParityTests testConferenceParticipantPortalDocumentationConfigurationMatchesRuntimeFactory]' failed (0.026 seconds).
Test Case '-[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeRetryBlocksConsumedCredentialReplay]' failed (0.225 seconds).
Test Case '-[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction]' failed (0.220 seconds).
Test Case '-[AppTests.HavenWorkbenchConfigurationTests testHavenWorkbenchUsesLocalTabsAndSupportedVisualizations]' failed (0.003 seconds).
Test Case '-[AppTests.MermaidRendererCellTests testWebViewDeterministicModeStableAcrossThreeBypassRuns]' failed (6.320 seconds).
Test Case '-[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersPNGWithoutClientTimeout]' failed (2.068 seconds).
Test Case '-[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersSVGAndCacheHit]' failed (4.083 seconds).
Test Case '-[AppTests.MermaidRendererCellTests testWebViewRendersConferenceDiagramFilesAndExposesPreviewState]' failed (2.081 seconds).
Test Case '-[AppTests.MicropaymentsMVPRoutesTests testPaymentProofDoorAuthorizeConsumesCredentialAndBlocksReplay]' failed (0.231 seconds).
Test Case '-[AppTests.MusicPublishingCellsTests testScaffoldRecoversPersistedMusicLibraryWhenNamedEmitterRegistryIsEmpty]' failed (0.017 seconds).
Test Case '-[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction]' failed (2.652 seconds).
Test Case '-[AppTests.ProductionSkeletonBindingIntegrityTests testArendalsukaEventAtlasPortholeTabsAndDetailsDoNotReturnNotFound]' failed (0.180 seconds).
Test Case '-[AppTests.ProductionSkeletonBindingIntegrityTests testArendalsukaParticipantProgramRendersSourceBackedProgramRowsWithoutBrokenKeypaths]' failed (0.510 seconds).
Test Case '-[AppTests.ProductionSkeletonBindingIntegrityTests testHavenWorkbenchSetupThroughPortholeKeepsSkeletonBindingsResolvable]' failed (7.072 seconds).
Test Case '-[AppTests.SkeletonElementParityMatrixTests testMatrixRevisionMatchesPackagePin]' failed (0.003 seconds).
Test Case '-[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips]' failed (0.007 seconds).
Test Case '-[AppTests.SkeletonRuntimeSourceTests testPortholeBootstrapUsesHttpSnapshotNotSocketFallbackWarning]' failed (0.018 seconds).
Test Case '-[AppTests.TopUpCheckoutTests testProductionStartupRejectsMissingRuntimeIdentityManifestBeforePublishingResolver]' failed (0.011 seconds).
Test Case '-[AppTests.TopUpCheckoutTests testSimulatedTopUpAllowsExplicitProductionAllowlistedUser]' failed (0.010 seconds).
Test Case '-[AppTests.TopUpCheckoutTests testSimulatedTopUpDefaultsToDeniedInProductionLikeEnvironment]' failed (0.011 seconds).
Test Case '-[AppTests.WorkbenchAccessGrantConfigurationTests testIdentityBoundPregrantUsesIssuerVaultWhenTargetOwnerWasDecodedSnapshot]' failed (0.020 seconds).
```


De ti WP13-relevante CellScaffold-klassene (pakke, rekkevidde, justering, godkjenning, antiformål, audit, signerte effekter, WebFetch-ceiling, provider-tools og e2e) bestod med **108/108 tester** i fullkjøringen. Ekte suite-/Executed-linjer: [cellscaffold-trust-suites.txt](evidence/wp13/cellscaffold-trust-suites.txt).

CellScaffold rapporterte 150 feilrapporter mot 148 i WP0c og 151 i WP10, men eksakt samme 46 røde navn; navnekriteriet er oppfylt. Feilrapporttallet alene er ikke brukt til å erklære nye regresjoner. Råloggen har enkelte sammenflettede UTF-8-bytes fra stdout/stderr; loggfilen er bevart uendret, mens sammenligningsskriptet bruker erstatningstegn ved dekoding av disse bytes. XCTest-navnene/summene er ASCII og kunne avstemmes komplett.

### E2e i full CellScaffold-regresjon — ekte utdata

```text
Test Case '-[AppTests.AgentTrustPackageE2ETests testFixtureModelGenerateNarrowApproveFetchAndAuditOneViolation]' started.
Test Case '-[AppTests.AgentTrustPackageE2ETests testFixtureModelGenerateNarrowApproveFetchAndAuditOneViolation]' passed (1.394 seconds).
WP13_E2E fixtureProviderCalls=1 before=sha256:cb354b5b9a1510b56d2d5f19db88927e376ebac03d2204280db175ddafb031bb after=sha256:6bc275fa7530b00eb9c0fa46543b52b7c061a82fd0ed3994bd0c32a1a95fbdcd approved=sha256:6bc275fa7530b00eb9c0fa46543b52b7c061a82fd0ed3994bd0c32a1a95fbdcd
WP13_E2E Siden godkjenning 2026-09-09T04:41:28Z: 3 effekter, 2 innenfor, 1 nektet. violation=new_destination signedVerified=3 networkRequests=2
```

[ACCEPT](ACCEPT.md#acceptance) avstemmer alle 14 §3-leveransene. Porthole-/Binding-paritet, tre lastetidsmålinger og rendererens konkrete brukerhandlinger er **ikke levert/verifisert i WP11**; WP11s siste dokumenterte stopp var det senere rettede filantallskriteriet, ikke en målt oppstartsfeil. Dette er ikke gjort grønt av API-e2e eller generell regresjon. Test.status-current kontrollerer at STATUS har én ny WP13-linje, at G3 fortsatt venter, og at tabellen har 14 rader med eksisterende fil-/ankerreferanser.

## WP13 — sluttmelding

**WP13 er fullført innenfor den bestilte slicen:** én ny `AgentTrustPackageE2ETests.swift`, fixture-e2e grønn både isolert og i full bundle; generer → fjern domene → godkjenn ny digest → tre fetch gir nøyaktig ett `new_destination`, tre effekter, to innenfor og tre signerte/verifiserbare effektkvitteringer. Gammel digest avvises, nye digest-/ceiling-bindinger bekreftes, og bare to requests når fixture-transporten. Fixture-modellen kjører én gang som forberedelse før godkjenning; ingen live leverandørkall eller generell tool-løkke er verifisert.

Begge bygg er grønne. Full nybygd XCTest: **CellProtocol 1086 / 8 hoppet over / samme 6 røde navn; CellScaffold 2155 / 11 hoppet over / samme 46 røde navn; ingen nye røde navn og ingen bortfalte baseline-røde tester**. Bundlene er fortsatt røde med henholdsvis 6 og 150 feilrapporter. Alle navn, råsummer, bygglogger og maskinell sammenligning står under [regression](#regression). Swift Testing er ikke dekket.

ACCEPT har én forventet→faktisk-rad for hver av de 14 §3-leveransene, med ærlig status for uleverte flater/kildegrenser. TESTRESULT har ekte #e2e- og #regression-utdata; STATUS har én ny linje. Produksjonskode, eksisterende tester, skeleton, Book og kontrakter er ikke tilsiktet endret i WP13. Kandidatgrenen er urørt; bare pålagt innledende grenlesing, ellers ingen git.

Før G3 kan gis gjenstår WP11 med faktisk Porthole-/Binding-paritet, nåbare handlinger og tre lastetidsmålinger, samt Kjetils eksplisitte akseptanse av leveransen og de dokumenterte kilde-/baselineavvikene; ekte modellkjøring gjenstår separat når kreditt/nøkkel finnes.

## Paritet <a id="parity"></a>

**WP11, 2026-09-09: blocked.** Rettet forhåndssjekk bestod: `AgentTrustPackageCell.swift` og `WebFetchCeilingTests.swift` finnes; pålagt `git branch --show-current` ga `pdd/tillitspakke-agentflaate`. Filantall er ikke kontrollert. [Forhåndssjekk](evidence/wp11/precheck.json).

Ett oppstartsforsøk, kjørt i `CellScaffold` fra 04:59:51 til 05:00:17 UTC (26 sekunder, avrundet til hele sekunder), exit **133**. Oppskrift: [RAG_MVP_UI.md, Local smoke test](../../../CellScaffold/Documentation/RAG_MVP_UI.md), med SwiftPMs `--disable-sandbox` fra handoffens regel 9, eksplisitt loopback og separat runtime-/SQLite-lagring:

```sh
CELL_SCAFFOLD_RUNTIME_ROOT=/private/tmp/wp11-agenttrustpackage-20260909 \
SQLITE_DATABASE_PATH=/private/tmp/wp11-agenttrustpackage-20260909/db.sqlite \
swift run --disable-sandbox Run serve --hostname 127.0.0.1 --port 9089
```

Ekte utdata fra [startup.log](evidence/wp11/startup.log):

```text
Build of product 'Run' complete! (4.02s)
```

Databasemigreringene og resolver-bootstrap ble utført. Deretter:

```text
Loading named emitters failed with error: outsideStorageRoot.
Loading identity named emitters failed with error: outsideStorageRoot.
Loading CellConfiguration failed with error: outsideStorageRoot. Initializing only the missing configuration.
[ NOTICE ] LiveInteraction conference mapping ready: 24 created, 0 existing, 24 sessions discovered.
Swift/ErrorType.swift:254: Fatal error: Error raised at top level: CellBase.CellStoragePathPolicy.Violation.outsideStorageRoot
```

Dette påviser en fatal avvisning i applikasjonens lagringsstivakt under oppstart med det angitte runtime-oppsettet. Den underliggende årsaken er ikke isolert; ingen port-, Docker-, nettverks- eller secret-feil er påvist. Det er heller ikke bevis for et rendereravvik. Ingen ny oppstart, alternativ runtime-konfigurasjon eller Docker-kjøring er forsøkt, i samsvar med grensen på ett oppstartsforsøk. [Starttid](evidence/wp11/startup.started), [sluttid](evidence/wp11/startup.finished), [exitkode](evidence/wp11/startup.exit).

Begge preview-kjøringene er **ikke kjørt**, fordi oppstartsprosessen avsluttet før Porthole kunne verifiseres. Følgende er de uutførte WP11-kommandoene, med cwd `CellScaffold` og eksplisitt localhost; de er dokumentasjon for oppfølging, ikke kjøreresultater:

```sh
npm run skeleton:iterate -- --mode preview --base-url http://127.0.0.1:9089 --configurationName "Agent Trust Package" --sourceCellEndpoint cell:///AgentTrustPackage --skeletonFile ../CellProtocolDocuments/Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/skeleton/tillitspakke-for.json
npm run skeleton:iterate -- --mode preview --base-url http://127.0.0.1:9089 --configurationName "Agent Trust Package" --sourceCellEndpoint cell:///AgentTrustPackage --skeletonFile ../CellProtocolDocuments/Deliverables/PDD_tillitspakke-agentflaate_2026-09-08/skeleton/tillitspakke-etter.json
```

Ingen faktiske screenshots er produsert i `images/actual/`. [ACCEPT#parity](ACCEPT.md#parity) har referanse→faktisk-tabell og alle sju `_verify_in_porthole`-punkter med eksplisitt uverifisert status. Ingen runtime-preview er committet. Staging og Binding er ikke kontaktet/kjørt. Kandidatgrenen er beholdt; ingen git-kommando utover pålagt innledende grenlesing.

### HAVEN-Deploy — registrering blokkert av eksisterende kølås

Oppstartssjekkene fra HAVEN-Deploys AGENTS.md ble kjørt i angitt rekkefølge:

| Kommando i `HAVEN-Deploy` | Resultat | Evidens |
| --- | --- | --- |
| `python3 tools/hd.py validate` | Exit 0: `validated 303 records, 0 problem(s)` | [Logg](evidence/wp11/hd-validate.log) |
| `python3 tools/hd.py board` | Exit 0; ingen WP11-post i tavlen | [Logg](evidence/wp11/hd-board.log) |
| `python3 tools/hd.py advisor-brief` | Exit 0; høyeste alvorlighet `block`: G2/HD-0001 (koordinering) og G6/HD-0011 (verifikasjon uten evidens), eksisterende forhold | [Logg](evidence/wp11/hd-advisor-brief.log) |
| `python3 tools/hd.py coord status` | Exit 2: eksisterende kølås | [Logg](evidence/wp11/hd-coord-status.log) |

Nøyaktig feil:

```text
hd: lock busy: /Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/queue/.write.lock
```

Kølåsen er fortsatt der. **Ingen HAVEN-Deploy-post er opprettet, og ingen task-id tildelt.** `task new` ble ikke kjørt etter at `coord status` påviste den felles skrivelåsen; oppdragets uttrykkelige alternativ er å skrive dette i rapporten. Låsen er ikke fjernet eller omgått. De eksisterende advisor-funnene er ikke årsaken til at registreringen stoppet.

Den bestilte posten er bevart her for registrering når køen er tilgjengelig; eier **kjetil**, repo **CellScaffold**, need **approval:kjetil-kjorer-scaffold-lokalt**, origin **losen**:

```sh
python3 tools/hd.py task new --title "WP11 Porthole-paritet for AgentTrustPackage-flatene" --purpose "Verifisere at de to flatene rendres som de godkjente referansebildene, mot kjørende CellScaffold" --owner kjetil --repo CellScaffold --need "approval:kjetil-kjorer-scaffold-lokalt" --origin losen
```

Neste steg, eier Kjetil: få CellScaffold kjørende lokalt med gyldig lagringsrot, registrer oppfølgingsposten når kølåsen er avklart, og fullfør de to preview-kjøringene, bilder, handlinger, audit og lastetid. Oppstartsfeilen i denne rapporten er reproduksjonsevidens; WP11 er ikke grønn og G3 er ikke gitt.

## Lastetid <a id="load-time"></a>

**WP11: blocked / ikke målt.** Kravet er ≤5 sekunder per lasting, tre målinger. Ingen flate ble lastet i en verifisert kjørende Porthole. Oppstartsvarigheten over er ikke en lastetidsmåling.

| Flate | Måling 1 | Måling 2 | Måling 3 | Resultat |
| --- | --- | --- | --- | --- |
| Før | Ikke målt | Ikke målt | Ikke målt | blocked |
| Etter | Ikke målt | Ikke målt | Ikke målt | blocked |

## Reachability <a id="reachability"></a>

**WP11: blocked / ikke kjørt.** SkeletonReachabilityAudit og `reachableActionKeypaths` er ikke kjørt/målt for de to flatene. Ingen tom liste eller grønn audit utledes fra JSON-lesing. `test.skeleton.no-unreachable-elements` og `test.skeleton.purpose-actions-reachable` er uverifisert i denne slicen. Se [ACCEPT#ways-in](ACCEPT.md#ways-in). Tidligere XCTest-resultater videreføres som historikk, ikke nye WP11-resultater.
