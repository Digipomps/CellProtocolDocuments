# CellScaffold origin/main — bygg- og testmåling 2026-09-29

Bygg: **bestått**. Tester: **feilet**. Dette dokumentet gjengir målingen; det gir ingen vurdering av G3.

## Revisjon og isolasjon

- Målt commit: `adf48d4615d1ed143d5bdc190fcf63e266214c8f`.
- `git fetch origin main` lyktes før arbeidstreet ble opprettet.
- Eget arbeidstre: `/tmp/cs-g3-20260929`, detached HEAD fra `origin/main`.
- Cache: `/tmp/cs-g3-20260929-cache/ModuleCache`; `TMPDIR=/tmp/cs-g3-20260929-cache/tmp`.
- Ingen lokale pakkeoverstyringer eller overstyringer av byggevaktens terskler var satt.
- `git diff --stat` var tom etter bygg og etter test: ingen sporede kilde- eller låsefiler endret i målearbeidstreet.
- Eksisterende CellScaffold-arbeidstrær og lokale grener ble ikke endret. Ingen prune, sletting, commit eller push ble kjørt. Arbeidstreet, cache og rålogger er beholdt.

`git log -1 --format='%H %ci %s' origin/main`, hentet før opprettelse av arbeidstreet:

`````text
adf48d4615d1ed143d5bdc190fcf63e266214c8f 2026-09-28 10:38:30 +0200 Merge pull request #272 from Digipomps/codex/idea-selection-20260928
`````

Swift-versjon:

`````text
Apple Swift version 6.4 (swiftlang-6.4.0.34.1 clang-2100.3.34.1)
Target: arm64-apple-macosx27.0.0
swift-driver version: 1.168.6 
`````

## Kommandoer og byggevakt

Begge Swift-kommandoer ble kjørt med de bestilte cache-overstyringene og `--disable-sandbox`. Bash `pipefail` var satt for å registrere kommandostatus, men dommen nedenfor er lest fra loggene.

`````text
export CACHE=/tmp/cs-g3-20260929-cache/ModuleCache
export CLANG_MODULE_CACHE_PATH="$CACHE" SWIFTPM_MODULECACHE_OVERRIDE="$CACHE"
export TMPDIR=/tmp/cs-g3-20260929-cache/tmp
export GIT_CONFIG_COUNT=2
export GIT_CONFIG_KEY_0=credential.helper GIT_CONFIG_VALUE_0=
export GIT_CONFIG_KEY_1=credential.helper
export GIT_CONFIG_VALUE_1='!/opt/homebrew/bin/gh auth git-credential'
cd /tmp/cs-g3-20260929
swift build --disable-sandbox 2>&1 | tee bygg.log | tail -5
swift test --disable-sandbox 2>&1 | tee test.log | tail -80
`````

`bash scripts/check_build_capacity.sh /tmp/cs-g3-20260929` ble kjørt før hver Swift-kommando og returnerte 0 begge ganger. Ordrett:

`````text
Build capacity: 69.0 GiB free (7%); reserving 10 GiB leaves 59.0 GiB (6%).
Build capacity: 63.7 GiB free (6%); reserving 10 GiB leaves 53.7 GiB (5%).
`````

På den målte SHA-en har `scripts/check_build_capacity.sh` standardverdiene 10 GiB reserve, minst 40 GiB og minst **5 %** ledig etter reserve. `AGENTS.md` på samme SHA og ryddeoppskriften omtaler 10 %. Dette er et observert avvik mellom kode og dokumentasjon. Vakten ble kjørt uendret, uten terskeloverstyringer. Ingen rydding ble utført.

## Byggdom, ordrett

`````text
Build complete! (285,28 sek)
`````

Avhengigheter ble hentet fra nett. SwiftPM skrev blant annet advarsler om skrivebeskyttet manifestcache, og kompilatoren skrev advarsler; byggkommandoen fullførte. Ingen justering eller ny kjøring ble gjort for å fjerne advarslene.

Testkommandoens kompilering, ordrett:

`````text
Build complete! (67,17 sek)
`````

## Alle «Test run with …»-linjer, ordrett

`````text
􁁛  Test run with 0 tests in 0 suites passed after 0.001 seconds.
􁁛  Test run with 0 tests in 0 suites passed after 0.001 seconds.
􁁛  Test run with 0 tests in 0 suites passed after 0.001 seconds.
􁁛  Test run with 0 tests in 0 suites passed after 0.001 seconds.
`````

Antall tester summert fra disse fire linjene: **0 + 0 + 0 + 0 = 0**. De er tomme Swift Testing-kjøringer. XCTest kjørte de faktiske testene nedenfor; disse null-linjene dokumenterer ikke at XCTest var grønn. Ingen `recorded an issue`-linjer finnes i testloggen.

## XCTest-dommer og totalt antall tester

Her telles hver `.xctest`-oppsummering én gang. De dupliserte `All tests`-oppsummeringene summeres ikke i tillegg.

| Testmål | Rapporterte tester | Hoppet over | Rapporterte feil | Dom |
|---|---:|---:|---:|---|
| UserSimulationScaffoldTests | 28 | 1 | 0 | passed |
| NodeAdminDockerCollectorTests | 4 | 0 | 0 | passed |
| AppTests | 2725 | 18 | 164 (8 unexpected) | failed |
| AdminPlaneTests | 21 | 0 | 0 | passed |
| **Sum** | **2778** | **19** | **164** | **failed** |

**Totalt: 2778 rapporterte testtilfeller**, hvorav 19 hoppet over og 2759 gjennomført. Kontrollert mot 2778 unike testnavn: **2714 bestått, 45 feilet, 19 hoppet over**. De 45 feilende testene fordeler seg på 20 konkrete suiter og har til sammen 164 XCTest-feilmeldinger. Flere feilmeldinger kan tilhøre samme test.

Alle fire XCTest-målenes dommer og oppsummeringer, ordrett:

`````text
Test Suite 'UserSimulationScaffoldTests.xctest' passed at 2026-09-29 09:42:19.532.
	 Executed 28 tests, with 1 test skipped and 0 failures (0 unexpected) in 2.388 (2.392) seconds
Test Suite 'NodeAdminDockerCollectorTests.xctest' passed at 2026-09-29 09:42:19.857.
	 Executed 4 tests, with 0 failures (0 unexpected) in 0.055 (0.055) seconds
Test Suite 'AppTests.xctest' failed at 2026-09-29 09:47:35.899.
	 Executed 2725 tests, with 18 tests skipped and 164 failures (8 unexpected) in 313.801 (313.971) seconds
Test Suite 'AdminPlaneTests.xctest' passed at 2026-09-29 09:47:37.866.
	 Executed 21 tests, with 0 failures (0 unexpected) in 0.028 (0.029) seconds
`````

Sluttmelding, ordrett:

`````text
Note: Some test targets reported failures:
  - AppTests (XCTest)
`````

## Hver rød test og hver feilende suite, ordrett

Følgende utdrag inneholder alle 45 feilende testdommer, alle 164 XCTest-feilmeldinger og alle feilende suitedommer. Ingen rotårsak er tilordnet eller feil rettet. Full kontekst finnes i [test.log](test.log).

### AppTests.AIAssistantThreadCellTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/AIAssistantThreadCellTests.swift:186: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsHAVENTeachingSwarmAndAppendsProviderTurns] : XCTAssertEqual failed: ("2") is not equal to ("3")
/private/tmp/cs-g3-20260929/Tests/AppTests/AIAssistantThreadCellTests.swift:187: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsHAVENTeachingSwarmAndAppendsProviderTurns] : XCTAssertEqual failed: ("["chatgpt-teacher", "claude-teacher"]") is not equal to ("["chatgpt-teacher", "qwen-learner", "claude-teacher"]")
/private/tmp/cs-g3-20260929/Tests/AppTests/AIAssistantThreadCellTests.swift:191: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsHAVENTeachingSwarmAndAppendsProviderTurns] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(false)")
/private/tmp/cs-g3-20260929/Tests/AppTests/AIAssistantThreadCellTests.swift:196: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsHAVENTeachingSwarmAndAppendsProviderTurns] : XCTUnwrap failed: expected non-nil value of type "(route: AIGatewayProviderRoute, request: AIGatewayInvokeRequest)"
Test Case '-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsHAVENTeachingSwarmAndAppendsProviderTurns]' failed (4.940 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/AIAssistantThreadCellTests.swift:274: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsLocalOnlyHAVENTeachingSwarmWithoutAPIKeys] : XCTAssertEqual failed: ("[]") is not equal to ("["local-chatgpt-teacher", "qwen-learner", "local-claude-teacher"]")
/private/tmp/cs-g3-20260929/Tests/AppTests/AIAssistantThreadCellTests.swift:276: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsLocalOnlyHAVENTeachingSwarmWithoutAPIKeys] : XCTUnwrap failed: expected non-nil value of type "(route: AIGatewayProviderRoute, request: AIGatewayInvokeRequest)"
Test Case '-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsLocalOnlyHAVENTeachingSwarmWithoutAPIKeys]' failed (0.006 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/AIAssistantThreadCellTests.swift:346: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelLocalBorealisChatsAgainstSharedBackend] : XCTAssertEqual failed: ("[]") is not equal to ("["borealis-architect", "borealis-privacy", "borealis-concise"]")
/private/tmp/cs-g3-20260929/Tests/AppTests/AIAssistantThreadCellTests.swift:351: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelLocalBorealisChatsAgainstSharedBackend] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(App.AIGatewayOrchestrationMode.swarm)")
/private/tmp/cs-g3-20260929/Tests/AppTests/AIAssistantThreadCellTests.swift:352: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelLocalBorealisChatsAgainstSharedBackend] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(3)")
/private/tmp/cs-g3-20260929/Tests/AppTests/AIAssistantThreadCellTests.swift:353: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelLocalBorealisChatsAgainstSharedBackend] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(App.AIGatewayToolPolicyMode.denyAll)")
/private/tmp/cs-g3-20260929/Tests/AppTests/AIAssistantThreadCellTests.swift:354: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelLocalBorealisChatsAgainstSharedBackend] : XCTUnwrap failed: expected non-nil value of type "AIGatewayProviderRoute"
Test Case '-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelLocalBorealisChatsAgainstSharedBackend]' failed (0.006 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/AIAssistantThreadCellTests.swift:454: error: -[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelMixedHostedAndLocalChatsWithRouteCredentials] : XCTUnwrap failed: expected non-nil value of type "AIGatewayProviderRoute"
Test Case '-[AppTests.AIAssistantThreadCellTests testPostUserMessageStartsParallelMixedHostedAndLocalChatsWithRouteCredentials]' failed (0.005 seconds).
Test Suite 'AIAssistantThreadCellTests' failed at 2026-09-29 09:42:26.924.
	 Executed 14 tests, with 4 tests skipped and 12 failures (0 unexpected) in 4.995 (4.997) seconds
`````

### AppTests.ArendalsukaImportAuthorizationRoutesTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/ArendalsukaImportAuthorizationRoutesTests.swift:223: error: -[AppTests.ArendalsukaImportAuthorizationRoutesTests testAdminDelegatesIdentityBoundCredentialToNonAdminImporter] : XCTAssertEqual failed: ("500 Internal Server Error") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/ArendalsukaImportAuthorizationRoutesTests.swift:225: error: -[AppTests.ArendalsukaImportAuthorizationRoutesTests testAdminDelegatesIdentityBoundCredentialToNonAdminImporter] : XCTUnwrap failed: expected non-nil value of type "Dictionary<String, Any>"
/private/tmp/cs-g3-20260929/Tests/AppTests/ArendalsukaImportAuthorizationRoutesTests.swift:214: error: -[AppTests.ArendalsukaImportAuthorizationRoutesTests testAdminDelegatesIdentityBoundCredentialToNonAdminImporter] : failed - (extension in XCTest):__C_Synthesized.related decl 'e' for XCTestErrorCode.(unknown context at $101d7699c).UnwrappingOptional(errorCode: 105, errorUserInfo: ["XCTestErrorUserInfoKeyShouldIgnore": true])
Test Case '-[AppTests.ArendalsukaImportAuthorizationRoutesTests testAdminDelegatesIdentityBoundCredentialToNonAdminImporter]' failed (0.331 seconds).
Test Suite 'ArendalsukaImportAuthorizationRoutesTests' failed at 2026-09-29 09:42:43.318.
	 Executed 1 test, with 3 failures (0 unexpected) in 0.331 (0.331) seconds
`````

### AppTests.BookReferenceRoutesTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:16: error: -[AppTests.BookReferenceRoutesTests testBookHomeRouteRendersLandingPage] : XCTAssertEqual failed: ("500 Internal Server Error") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:17: error: -[AppTests.BookReferenceRoutesTests testBookHomeRouteRendersLandingPage] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:18: error: -[AppTests.BookReferenceRoutesTests testBookHomeRouteRendersLandingPage] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:19: error: -[AppTests.BookReferenceRoutesTests testBookHomeRouteRendersLandingPage] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:20: error: -[AppTests.BookReferenceRoutesTests testBookHomeRouteRendersLandingPage] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:21: error: -[AppTests.BookReferenceRoutesTests testBookHomeRouteRendersLandingPage] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:22: error: -[AppTests.BookReferenceRoutesTests testBookHomeRouteRendersLandingPage] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:23: error: -[AppTests.BookReferenceRoutesTests testBookHomeRouteRendersLandingPage] : XCTAssertTrue failed
Test Case '-[AppTests.BookReferenceRoutesTests testBookHomeRouteRendersLandingPage]' failed (0.230 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:78: error: -[AppTests.BookReferenceRoutesTests testBookSlugRouteRendersHTMLDocument] : XCTAssertEqual failed: ("503 Service Unavailable") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:79: error: -[AppTests.BookReferenceRoutesTests testBookSlugRouteRendersHTMLDocument] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:80: error: -[AppTests.BookReferenceRoutesTests testBookSlugRouteRendersHTMLDocument] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:81: error: -[AppTests.BookReferenceRoutesTests testBookSlugRouteRendersHTMLDocument] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:82: error: -[AppTests.BookReferenceRoutesTests testBookSlugRouteRendersHTMLDocument] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:83: error: -[AppTests.BookReferenceRoutesTests testBookSlugRouteRendersHTMLDocument] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:84: error: -[AppTests.BookReferenceRoutesTests testBookSlugRouteRendersHTMLDocument] : XCTAssertTrue failed
Test Case '-[AppTests.BookReferenceRoutesTests testBookSlugRouteRendersHTMLDocument]' failed (0.217 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:39: error: -[AppTests.BookReferenceRoutesTests testBookTreeEndpointExposesBookHomeAndReferenceWorkspace] : XCTAssertEqual failed: ("500 Internal Server Error") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:40: error: -[AppTests.BookReferenceRoutesTests testBookTreeEndpointExposesBookHomeAndReferenceWorkspace] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:41: error: -[AppTests.BookReferenceRoutesTests testBookTreeEndpointExposesBookHomeAndReferenceWorkspace] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:42: error: -[AppTests.BookReferenceRoutesTests testBookTreeEndpointExposesBookHomeAndReferenceWorkspace] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:43: error: -[AppTests.BookReferenceRoutesTests testBookTreeEndpointExposesBookHomeAndReferenceWorkspace] : XCTAssertTrue failed
Test Case '-[AppTests.BookReferenceRoutesTests testBookTreeEndpointExposesBookHomeAndReferenceWorkspace]' failed (0.226 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:119: error: -[AppTests.BookReferenceRoutesTests testConferenceConnectionHubLifecycleSlugRouteRendersMermaidInline] : XCTAssertEqual failed: ("503 Service Unavailable") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:120: error: -[AppTests.BookReferenceRoutesTests testConferenceConnectionHubLifecycleSlugRouteRendersMermaidInline] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:121: error: -[AppTests.BookReferenceRoutesTests testConferenceConnectionHubLifecycleSlugRouteRendersMermaidInline] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:122: error: -[AppTests.BookReferenceRoutesTests testConferenceConnectionHubLifecycleSlugRouteRendersMermaidInline] : XCTAssertTrue failed
Test Case '-[AppTests.BookReferenceRoutesTests testConferenceConnectionHubLifecycleSlugRouteRendersMermaidInline]' failed (0.304 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:100: error: -[AppTests.BookReferenceRoutesTests testConferenceOwnershipSlugRouteRendersMermaidInline] : XCTAssertEqual failed: ("503 Service Unavailable") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:101: error: -[AppTests.BookReferenceRoutesTests testConferenceOwnershipSlugRouteRendersMermaidInline] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:102: error: -[AppTests.BookReferenceRoutesTests testConferenceOwnershipSlugRouteRendersMermaidInline] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:103: error: -[AppTests.BookReferenceRoutesTests testConferenceOwnershipSlugRouteRendersMermaidInline] : XCTAssertTrue failed
Test Case '-[AppTests.BookReferenceRoutesTests testConferenceOwnershipSlugRouteRendersMermaidInline]' failed (0.235 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:59: error: -[AppTests.BookReferenceRoutesTests testRenderedEndpointSupportsSwiftBackend] : XCTAssertEqual failed: ("503 Service Unavailable") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:60: error: -[AppTests.BookReferenceRoutesTests testRenderedEndpointSupportsSwiftBackend] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/BookReferenceRoutesTests.swift:62: error: -[AppTests.BookReferenceRoutesTests testRenderedEndpointSupportsSwiftBackend] : XCTAssertTrue failed
Test Case '-[AppTests.BookReferenceRoutesTests testRenderedEndpointSupportsSwiftBackend]' failed (0.241 seconds).
Test Suite 'BookReferenceRoutesTests' failed at 2026-09-29 09:42:51.766.
	 Executed 6 tests, with 31 failures (0 unexpected) in 1.455 (1.456) seconds
`````

### AppTests.ButterpopStudioProductTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:1347: error: -[AppTests.ButterpopStudioProductTests testLocalButterpopMP3TranscodesPublishesAndPreviewsWhenAvailable] : XCTAssertEqual failed: ("Optional("error")") is not equal to ("Optional("published")") - ["status": CellBase.ValueType.string("error"), "message": CellBase.ValueType.string("The selected mix has no readable source asset.")]
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:1348: error: -[AppTests.ButterpopStudioProductTests testLocalButterpopMP3TranscodesPublishesAndPreviewsWhenAvailable] : XCTUnwrap failed: expected non-nil value of type "String"
Test Case '-[AppTests.ButterpopStudioProductTests testLocalButterpopMP3TranscodesPublishesAndPreviewsWhenAvailable]' failed (0.338 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:899: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: threw error "Error Domain=ButterpopStudioProductTests Code=1 "(null)""
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:913: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("Optional(0)") is not equal to ("Optional(100)")
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:929: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("402 Payment Required") is not equal to ("200 OK") - {
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:931: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("Optional("payment_required")") is not equal to ("Optional("issued")")
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:932: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(10)")
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:933: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("Optional(0)") is not equal to ("Optional(90)")
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:939: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("/butterpop/api/audio/player")")
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:948: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("Optional(10)") is not equal to ("Optional(7)")
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:949: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("Optional(1)") is not equal to ("Optional(2)")
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:962: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("402 Payment Required") is not equal to ("200 OK") - {
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:964: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(7)")
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:965: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("Optional(0)") is not equal to ("Optional(83)")
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:962: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("402 Payment Required") is not equal to ("200 OK") - {
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:964: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(5)")
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:965: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("Optional(0)") is not equal to ("Optional(78)")
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:977: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertEqual failed: ("Optional(10)") is not equal to ("Optional(5)")
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:978: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/ButterpopStudioProductTests.swift:983: error: -[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview] : XCTUnwrap failed: expected non-nil value of type "String"
Test Case '-[AppTests.ButterpopStudioProductTests testSharedWorkspacePublishesApprovedWaveAndServesRangePreview]' failed (0.473 seconds).
Test Suite 'ButterpopStudioProductTests' failed at 2026-09-29 09:43:08.003.
	 Executed 11 tests, with 20 failures (1 unexpected) in 4.594 (4.595) seconds
`````

### AppTests.CellScaffoldRuntimeIdentityProvisionerTests

`````text
/private/tmp/cs-g3-20260929/Sources/App/Support/CellScaffoldRuntimeIdentityProvisioner.swift:923: error: -[AppTests.CellScaffoldRuntimeIdentityProvisionerTests testWriterRejectsExtendedAttributesOnExistingManifest] : failed: caught error: "manifestWritePreconditionFailed"
Test Case '-[AppTests.CellScaffoldRuntimeIdentityProvisionerTests testWriterRejectsExtendedAttributesOnExistingManifest]' failed (0.002 seconds).
/private/tmp/cs-g3-20260929/Sources/App/Support/CellScaffoldRuntimeIdentityProvisioner.swift:878: error: -[AppTests.CellScaffoldRuntimeIdentityProvisionerTests testWriterRejectsOverwriteWithoutExactOldDigestAndUses0600] : failed: caught error: "manifestWritePreconditionFailed"
Test Case '-[AppTests.CellScaffoldRuntimeIdentityProvisionerTests testWriterRejectsOverwriteWithoutExactOldDigestAndUses0600]' failed (0.001 seconds).
Test Suite 'CellScaffoldRuntimeIdentityProvisionerTests' failed at 2026-09-29 09:43:08.911.
	 Executed 31 tests, with 2 failures (2 unexpected) in 0.163 (0.164) seconds
`````

### AppTests.ConferenceEntityDiscoveryCellTests

`````text
******** Directory does not exist trying to create. path: /var/folders/7s/xyjsdm211_xggqqzw1nmx8xc0000gn/T/CellScaffoldTestH/private/tmp/cs-g3-20260929/.build/checkouts/CellProtocol/Sources/CellBase/Cells/CellResolver/Cast/ResolverAuditor.swift:167: error: -[AppTests.ConferenceEntityDiscoveryCellTests testChatLaunchCellCanStartConversationAndProjectMessageFeedback] : failed: caught error: "registerAtAlreadyTakenEndpoint"
Test Case '-[AppTests.ConferenceEntityDiscoveryCellTests testChatLaunchCellCanStartConversationAndProjectMessageFeedback]' failed (0.021 seconds).
Test Suite 'ConferenceEntityDiscoveryCellTests' failed at 2026-09-29 09:43:17.900.
	 Executed 11 tests, with 1 failure (1 unexpected) in 0.158 (0.159) seconds
`````

### AppTests.ConferenceOrganizerProjectionCellTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceOrganizerProjectionCellTests.swift:223: error: -[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionHandsOffCapturedLeadToSponsorOwnedFollowUp] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceOrganizerProjectionCellTests.swift:224: error: -[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionHandsOffCapturedLeadToSponsorOwnedFollowUp] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceOrganizerProjectionCellTests.swift:225: error: -[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionHandsOffCapturedLeadToSponsorOwnedFollowUp] : XCTAssertEqual failed: ("0") is not equal to ("1")
Test Case '-[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionHandsOffCapturedLeadToSponsorOwnedFollowUp]' failed (0.047 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceOrganizerProjectionCellTests.swift:133: error: -[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionUsesConsentBoundAggregateSignalsWhenAvailable] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceOrganizerProjectionCellTests.swift:134: error: -[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionUsesConsentBoundAggregateSignalsWhenAvailable] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceOrganizerProjectionCellTests.swift:138: error: -[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionUsesConsentBoundAggregateSignalsWhenAvailable] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceOrganizerProjectionCellTests.swift:139: error: -[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionUsesConsentBoundAggregateSignalsWhenAvailable] : XCTAssertTrue failed
Test Case '-[AppTests.ConferenceOrganizerProjectionCellTests testOrganizerProjectionUsesConsentBoundAggregateSignalsWhenAvailable]' failed (0.039 seconds).
Test Suite 'ConferenceOrganizerProjectionCellTests' failed at 2026-09-29 09:43:18.347.
	 Executed 3 tests, with 7 failures (0 unexpected) in 0.108 (0.109) seconds
`````

### AppTests.ConferencePublishedContentCellTests

`````text
/private/tmp/cs-g3-20260929/Sources/ScaffoldKit/BrowserClientIdentityVault.swift:864: error: -[AppTests.ConferencePublishedContentCellTests testPublishedContentCellRecognizesStableOrganizerIdentityWhenVaultContextIsPoisoned] : failed: caught error: "persistedIdentityUnavailable"
Test Case '-[AppTests.ConferencePublishedContentCellTests testPublishedContentCellRecognizesStableOrganizerIdentityWhenVaultContextIsPoisoned]' failed (0.001 seconds).
Test Suite 'ConferencePublishedContentCellTests' failed at 2026-09-29 09:43:20.611.
	 Executed 10 tests, with 1 failure (1 unexpected) in 0.061 (0.061) seconds
`````

### AppTests.ConferenceSchedulingCellTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSchedulingCellTests.swift:152: error: -[AppTests.ConferenceSchedulingCellTests testRouterDelegatesSharedMeetingRequestAndLocalExportToSchedulingCell] : XCTAssertTrue failed
Test Case '-[AppTests.ConferenceSchedulingCellTests testRouterDelegatesSharedMeetingRequestAndLocalExportToSchedulingCell]' failed (0.024 seconds).
Test Suite 'ConferenceSchedulingCellTests' failed at 2026-09-29 09:43:20.772.
	 Executed 2 tests, with 1 failure (0 unexpected) in 0.044 (0.045) seconds
`````

### AppTests.ConferenceSponsorLeadAggregateCellTests

`````text
/private/tmp/cs-g3-20260929/Sources/ScaffoldKit/BrowserClientIdentityVault.swift:864: error: -[AppTests.ConferenceSponsorLeadAggregateCellTests testSponsorLeadAggregateSyncsConsentBoundParticipantsAndCapturesLead] : failed: caught error: "persistedIdentityUnavailable"
Test Case '-[AppTests.ConferenceSponsorLeadAggregateCellTests testSponsorLeadAggregateSyncsConsentBoundParticipantsAndCapturesLead]' failed (0.007 seconds).
Test Suite 'ConferenceSponsorLeadAggregateCellTests' failed at 2026-09-29 09:43:25.913.
	 Executed 2 tests, with 1 failure (1 unexpected) in 0.008 (0.008) seconds
`````

### AppTests.ConferenceSurfaceRoutesTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2617: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionAcceptsStoredImportAccessVC] : XCTAssertEqual failed: ("500 Internal Server Error") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2619: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionAcceptsStoredImportAccessVC] : XCTUnwrap failed: expected non-nil value of type "Dictionary<String, Any>"
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2608: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionAcceptsStoredImportAccessVC] : failed - (extension in XCTest):__C_Synthesized.related decl 'e' for XCTestErrorCode.(unknown context at $101d7699c).UnwrappingOptional(errorCode: 105, errorUserInfo: ["XCTestErrorUserInfoKeyShouldIgnore": true])
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionAcceptsStoredImportAccessVC]' failed (0.848 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:700: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionSupportsAdminSessionAndRejectsMismatchedSignedProof] : XCTAssertEqual failed: ("500 Internal Server Error") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:702: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionSupportsAdminSessionAndRejectsMismatchedSignedProof] : XCTUnwrap failed: expected non-nil value of type "Dictionary<String, Any>"
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:691: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionSupportsAdminSessionAndRejectsMismatchedSignedProof] : failed - (extension in XCTest):__C_Synthesized.related decl 'e' for XCTestErrorCode.(unknown context at $101d7699c).UnwrappingOptional(errorCode: 105, errorUserInfo: ["XCTestErrorUserInfoKeyShouldIgnore": true])
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaImportActionSupportsAdminSessionAndRejectsMismatchedSignedProof]' failed (0.894 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2468: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication] : XCTAssertEqual failed: ("503 Service Unavailable") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2469: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2471: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(1)")
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2475: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication] : XCTAssertEqual failed: ("503 Service Unavailable") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2476: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2477: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication] : XCTAssertTrue failed
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublicKnowledgeRoutesUseIndexedStoreWithoutAuthentication]' failed (0.625 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2397: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublishedApiReadsUseAgreementWithoutDebugAccess] : XCTAssertEqual failed: ("503 Service Unavailable") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2398: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublishedApiReadsUseAgreementWithoutDebugAccess] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("public, max-age=60, stale-while-revalidate=300")")
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2402: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublishedApiReadsUseAgreementWithoutDebugAccess] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2407: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublishedApiReadsUseAgreementWithoutDebugAccess] : XCTAssertEqual failed: ("503 Service Unavailable") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:2408: error: -[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublishedApiReadsUseAgreementWithoutDebugAccess] : XCTAssertTrue failed
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testArendalsukaPublishedApiReadsUseAgreementWithoutDebugAccess]' failed (0.460 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:102: error: -[AppTests.ConferenceSurfaceRoutesTests testConferencePageAccessPolicies] : XCTAssertEqual failed: ("200 OK") is not equal to ("303 See Other")
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:103: error: -[AppTests.ConferenceSurfaceRoutesTests testConferencePageAccessPolicies] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("/porthole?configurationName=Arendalsuka%20Participant%20Program&configurationEndpoint=cell:///ArendalsukaConfigurationPublisher")")
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testConferencePageAccessPolicies]' failed (0.241 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:311: error: -[AppTests.ConferenceSurfaceRoutesTests testConferencePagesExposeCanonicalSurfaceMetadataForWebNavigator] : XCTAssertEqual failed: ("200 OK") is not equal to ("303 See Other")
/private/tmp/cs-g3-20260929/Tests/AppTests/ConferenceSurfaceRoutesTests.swift:312: error: -[AppTests.ConferenceSurfaceRoutesTests testConferencePagesExposeCanonicalSurfaceMetadataForWebNavigator] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("/porthole?configurationName=Arendalsuka%20Participant%20Program&configurationEndpoint=cell:///ArendalsukaConfigurationPublisher")")
Test Case '-[AppTests.ConferenceSurfaceRoutesTests testConferencePagesExposeCanonicalSurfaceMetadataForWebNavigator]' failed (0.245 seconds).
Test Suite 'ConferenceSurfaceRoutesTests' failed at 2026-09-29 09:43:47.319.
	 Executed 39 tests, with 21 failures (0 unexpected) in 21.403 (21.406) seconds
`````

### AppTests.ContractChallengeMVPRoutesTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/ContractChallengeMVPRoutesTests.swift:113: error: -[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeRetryBlocksConsumedCredentialReplay] : XCTAssertEqual failed: ("402 Payment Required") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/ContractChallengeMVPRoutesTests.swift:115: error: -[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeRetryBlocksConsumedCredentialReplay] : XCTAssertEqual failed: ("Optional("blocked")") is not equal to ("Optional("granted")")
/private/tmp/cs-g3-20260929/Tests/AppTests/ContractChallengeMVPRoutesTests.swift:117: error: -[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeRetryBlocksConsumedCredentialReplay] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(false)")
Test Case '-[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeRetryBlocksConsumedCredentialReplay]' failed (0.267 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/ContractChallengeMVPRoutesTests.swift:66: error: -[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("issued")") - string("error: failed to resolve identity domain")
/private/tmp/cs-g3-20260929/Tests/AppTests/ContractChallengeMVPRoutesTests.swift:70: error: -[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction] : XCTAssertEqual failed: ("402 Payment Required") is not equal to ("200 OK") - {
/private/tmp/cs-g3-20260929/Tests/AppTests/ContractChallengeMVPRoutesTests.swift:71: error: -[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction] : XCTAssertEqual failed: ("Optional("blocked")") is not equal to ("Optional("granted")")
/private/tmp/cs-g3-20260929/Tests/AppTests/ContractChallengeMVPRoutesTests.swift:72: error: -[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("user-authorized-microtransaction")")
/private/tmp/cs-g3-20260929/Tests/AppTests/ContractChallengeMVPRoutesTests.swift:74: error: -[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(1)")
/private/tmp/cs-g3-20260929/Tests/AppTests/ContractChallengeMVPRoutesTests.swift:75: error: -[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(1000)")
Test Case '-[AppTests.ContractChallengeMVPRoutesTests testPaymentProofDoorAuthorizeUsesOneMinorUnitMicrotransaction]' failed (0.251 seconds).
Test Suite 'ContractChallengeMVPRoutesTests' failed at 2026-09-29 09:43:51.279.
	 Executed 5 tests, with 9 failures (0 unexpected) in 1.243 (1.243) seconds
`````

### AppTests.MarkdownRendererCellTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:94: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceConnectionHubLifecycleDocumentEmbedsMermaidAndAgreementContent] : XCTAssertEqual failed: ("error") is not equal to ("ok")
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:95: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceConnectionHubLifecycleDocumentEmbedsMermaidAndAgreementContent] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("book-18-conference-connectionhub-agreement-lifecycle")")
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:96: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceConnectionHubLifecycleDocumentEmbedsMermaidAndAgreementContent] : XCTAssertFalse failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:98: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceConnectionHubLifecycleDocumentEmbedsMermaidAndAgreementContent] : XCTAssertFalse failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:99: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceConnectionHubLifecycleDocumentEmbedsMermaidAndAgreementContent] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:100: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceConnectionHubLifecycleDocumentEmbedsMermaidAndAgreementContent] : XCTAssertTrue failed
Test Case '-[AppTests.MarkdownRendererCellTests testRenderConferenceConnectionHubLifecycleDocumentEmbedsMermaidAndAgreementContent]' failed (0.001 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:56: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceOwnershipDocumentEmbedsMermaidSVGAndStoresLastRenderState] : XCTAssertEqual failed: ("error") is not equal to ("ok")
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:57: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceOwnershipDocumentEmbedsMermaidSVGAndStoresLastRenderState] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("book-17-conference-ownership-dataflow")")
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:58: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceOwnershipDocumentEmbedsMermaidSVGAndStoresLastRenderState] : XCTAssertFalse failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:60: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceOwnershipDocumentEmbedsMermaidSVGAndStoresLastRenderState] : XCTAssertFalse failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:61: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceOwnershipDocumentEmbedsMermaidSVGAndStoresLastRenderState] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:69: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceOwnershipDocumentEmbedsMermaidSVGAndStoresLastRenderState] : XCTAssertEqual failed: ("nil") is not equal to ("Optional(CellBase.ValueType.string("book-17-conference-ownership-dataflow"))")
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:71: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceOwnershipDocumentEmbedsMermaidSVGAndStoresLastRenderState] : XCTAssertFalse failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:72: error: -[AppTests.MarkdownRendererCellTests testRenderConferenceOwnershipDocumentEmbedsMermaidSVGAndStoresLastRenderState] : XCTAssertTrue failed
Test Case '-[AppTests.MarkdownRendererCellTests testRenderConferenceOwnershipDocumentEmbedsMermaidSVGAndStoresLastRenderState]' failed (0.001 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:17: error: -[AppTests.MarkdownRendererCellTests testRenderDocumentByDocIDProducesCanonicalMetadata] : XCTAssertEqual failed: ("error") is not equal to ("ok")
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:18: error: -[AppTests.MarkdownRendererCellTests testRenderDocumentByDocIDProducesCanonicalMetadata] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("book-home")")
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:19: error: -[AppTests.MarkdownRendererCellTests testRenderDocumentByDocIDProducesCanonicalMetadata] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("book-home")")
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:20: error: -[AppTests.MarkdownRendererCellTests testRenderDocumentByDocIDProducesCanonicalMetadata] : XCTAssertFalse failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:21: error: -[AppTests.MarkdownRendererCellTests testRenderDocumentByDocIDProducesCanonicalMetadata] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("swift")")
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:22: error: -[AppTests.MarkdownRendererCellTests testRenderDocumentByDocIDProducesCanonicalMetadata] : XCTAssertFalse failed
Test Case '-[AppTests.MarkdownRendererCellTests testRenderDocumentByDocIDProducesCanonicalMetadata]' failed (0.002 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:34: error: -[AppTests.MarkdownRendererCellTests testRenderRawSourceResolvesRelativeMarkdownLinkAgainstBookCatalog] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("book-10-quickstart")")
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:35: error: -[AppTests.MarkdownRendererCellTests testRenderRawSourceResolvesRelativeMarkdownLinkAgainstBookCatalog] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("/book/quickstart")")
/private/tmp/cs-g3-20260929/Tests/AppTests/MarkdownRendererCellTests.swift:36: error: -[AppTests.MarkdownRendererCellTests testRenderRawSourceResolvesRelativeMarkdownLinkAgainstBookCatalog] : XCTAssertTrue failed
Test Case '-[AppTests.MarkdownRendererCellTests testRenderRawSourceResolvesRelativeMarkdownLinkAgainstBookCatalog]' failed (0.002 seconds).
Test Suite 'MarkdownRendererCellTests' failed at 2026-09-29 09:44:18.855.
	 Executed 4 tests, with 23 failures (0 unexpected) in 0.007 (0.007) seconds
`````

### AppTests.MermaidRendererCellTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:144: error: -[AppTests.MermaidRendererCellTests testWebViewDeterministicModeStableAcrossThreeBypassRuns] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:145: error: -[AppTests.MermaidRendererCellTests testWebViewDeterministicModeStableAcrossThreeBypassRuns] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:146: error: -[AppTests.MermaidRendererCellTests testWebViewDeterministicModeStableAcrossThreeBypassRuns] : XCTAssertTrue failed
Test Case '-[AppTests.MermaidRendererCellTests testWebViewDeterministicModeStableAcrossThreeBypassRuns]' failed (6.485 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:112: error: -[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersPNGWithoutClientTimeout] : XCTAssertTrue failed - Expected PNG render to succeed quickly, got: ["Render timed out after 2000ms"]
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:114: error: -[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersPNGWithoutClientTimeout] : XCTAssertNotNil failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:115: error: -[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersPNGWithoutClientTimeout] : XCTAssertTrue failed
Test Case '-[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersPNGWithoutClientTimeout]' failed (2.086 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:75: error: -[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersSVGAndCacheHit] : XCTAssertTrue failed - Expected first render to succeed: ["Render timed out after 2000ms"]
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:77: error: -[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersSVGAndCacheHit] : XCTAssertNotNil failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:78: error: -[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersSVGAndCacheHit] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:79: error: -[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersSVGAndCacheHit] : XCTAssertTrue failed
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:82: error: -[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersSVGAndCacheHit] : XCTAssertTrue failed - Expected second render to succeed: ["Render timed out after 2000ms"]
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:83: error: -[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersSVGAndCacheHit] : XCTAssertTrue failed
Test Case '-[AppTests.MermaidRendererCellTests testWebViewIntegrationRendersSVGAndCacheHit]' failed (4.181 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:216: error: -[AppTests.MermaidRendererCellTests testWebViewRendersConferenceDiagramFilesAndExposesPreviewState] : XCTAssertTrue failed - Expected conference-system-overview.mmd to render without errors, got: ["Render timed out after 2000ms"]
/private/tmp/cs-g3-20260929/Tests/AppTests/MermaidRendererCellTests.swift:220: error: -[AppTests.MermaidRendererCellTests testWebViewRendersConferenceDiagramFilesAndExposesPreviewState] : XCTUnwrap failed: expected non-nil value of type "String" - Expected SVG output for conference-system-overview.mmd
Test Case '-[AppTests.MermaidRendererCellTests testWebViewRendersConferenceDiagramFilesAndExposesPreviewState]' failed (2.112 seconds).
Test Suite 'MermaidRendererCellTests' failed at 2026-09-29 09:44:34.708.
	 Executed 11 tests, with 14 failures (0 unexpected) in 15.818 (15.819) seconds
`````

### AppTests.MicropaymentsMVPRoutesTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/MicropaymentsMVPRoutesTests.swift:39: error: -[AppTests.MicropaymentsMVPRoutesTests testPaymentProofDoorAuthorizeConsumesCredentialAndBlocksReplay] : XCTAssertEqual failed: ("402 Payment Required") is not equal to ("200 OK")
/private/tmp/cs-g3-20260929/Tests/AppTests/MicropaymentsMVPRoutesTests.swift:41: error: -[AppTests.MicropaymentsMVPRoutesTests testPaymentProofDoorAuthorizeConsumesCredentialAndBlocksReplay] : XCTAssertEqual failed: ("Optional("blocked")") is not equal to ("Optional("granted")")
/private/tmp/cs-g3-20260929/Tests/AppTests/MicropaymentsMVPRoutesTests.swift:42: error: -[AppTests.MicropaymentsMVPRoutesTests testPaymentProofDoorAuthorizeConsumesCredentialAndBlocksReplay] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("user-authorized-microtransaction")")
/private/tmp/cs-g3-20260929/Tests/AppTests/MicropaymentsMVPRoutesTests.swift:43: error: -[AppTests.MicropaymentsMVPRoutesTests testPaymentProofDoorAuthorizeConsumesCredentialAndBlocksReplay] : XCTAssertFalse failed
Test Case '-[AppTests.MicropaymentsMVPRoutesTests testPaymentProofDoorAuthorizeConsumesCredentialAndBlocksReplay]' failed (0.235 seconds).
Test Suite 'MicropaymentsMVPRoutesTests' failed at 2026-09-29 09:44:35.534.
	 Executed 1 test, with 4 failures (0 unexpected) in 0.235 (0.235) seconds
`````

### AppTests.MusicPublishingCellsTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/MusicPublishingCellsTests.swift:182: error: -[AppTests.MusicPublishingCellsTests testScaffoldRecoversPersistedMusicLibraryWhenNamedEmitterRegistryIsEmpty] : XCTAssertEqual failed: ("nil") is not equal to ("Optional("8557A702-5207-4078-88EF-11A1FCE10F20")")
/private/tmp/cs-g3-20260929/Tests/AppTests/MusicPublishingCellsTests.swift:189: error: -[AppTests.MusicPublishingCellsTests testScaffoldRecoversPersistedMusicLibraryWhenNamedEmitterRegistryIsEmpty] : XCTAssertEqual failed: ("C0E61270-BA34-4EA1-A548-624890204302") is not equal to ("8557A702-5207-4078-88EF-11A1FCE10F20")
/private/tmp/cs-g3-20260929/Tests/AppTests/MusicPublishingCellsTests.swift:199: error: -[AppTests.MusicPublishingCellsTests testScaffoldRecoversPersistedMusicLibraryWhenNamedEmitterRegistryIsEmpty] : XCTAssertEqual failed: ("Optional(0)") is not equal to ("Optional(1)")
Test Case '-[AppTests.MusicPublishingCellsTests testScaffoldRecoversPersistedMusicLibraryWhenNamedEmitterRegistryIsEmpty]' failed (0.018 seconds).
Test Suite 'MusicPublishingCellsTests' failed at 2026-09-29 09:44:35.656.
	 Executed 27 tests, with 3 failures (0 unexpected) in 0.117 (0.118) seconds
`````

### AppTests.PortholeConfigurationLoadingTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/PortholeConfigurationLoadingTests.swift:1211: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertTrue failed - Expected webview render to succeed: [CellBase.ValueType.string("Render timed out after 2000ms")]
/private/tmp/cs-g3-20260929/Tests/AppTests/PortholeConfigurationLoadingTests.swift:1212: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertNotNil failed
/private/tmp/cs-g3-20260929/Tests/AppTests/PortholeConfigurationLoadingTests.swift:1236: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertEqual failed: ("Optional(CellBase.ValueType.bool(false))") is not equal to ("Optional(CellBase.ValueType.bool(true))")
/private/tmp/cs-g3-20260929/Tests/AppTests/PortholeConfigurationLoadingTests.swift:1237: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertTrue failed - Expected rendered preview HTML in projected bootstrap state.
/private/tmp/cs-g3-20260929/Tests/AppTests/PortholeConfigurationLoadingTests.swift:1241: error: -[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction] : XCTAssertEqual failed: ("Render timed out after 2000ms") is not equal to ("")
Test Case '-[AppTests.PortholeConfigurationLoadingTests testMermaidRendererPlaygroundLoadsThroughPortholeAddConfigurationAction]' failed (2.581 seconds).
Test Suite 'PortholeConfigurationLoadingTests' failed at 2026-09-29 09:46:23.169.
	 Executed 51 tests, with 5 failures (0 unexpected) in 56.745 (56.748) seconds
`````

### AppTests.SecureRuntimeIdentityManifestFileTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/SecureRuntimeIdentityManifestFileTests.swift:29: error: -[AppTests.SecureRuntimeIdentityManifestFileTests testReadsExactContainerOwned0700And0400File] : XCTAssertEqual failed: threw error "manifestMetadataUnsafe"
Test Case '-[AppTests.SecureRuntimeIdentityManifestFileTests testReadsExactContainerOwned0700And0400File]' failed (0.002 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/SecureRuntimeIdentityManifestFileTests.swift:122: error: -[AppTests.SecureRuntimeIdentityManifestFileTests testRejectsEmptyAndOversizedFile] : XCTAssertEqual failed: ("Optional(App.CellScaffoldRuntimeIdentityManifestFailure.manifestMetadataUnsafe)") is not equal to ("Optional(App.CellScaffoldRuntimeIdentityManifestFailure.manifestNoncanonical)")
/private/tmp/cs-g3-20260929/Tests/AppTests/SecureRuntimeIdentityManifestFileTests.swift:128: error: -[AppTests.SecureRuntimeIdentityManifestFileTests testRejectsEmptyAndOversizedFile] : XCTAssertEqual failed: ("Optional(App.CellScaffoldRuntimeIdentityManifestFailure.manifestMetadataUnsafe)") is not equal to ("Optional(App.CellScaffoldRuntimeIdentityManifestFailure.manifestTooLarge)")
Test Case '-[AppTests.SecureRuntimeIdentityManifestFileTests testRejectsEmptyAndOversizedFile]' failed (0.004 seconds).
Test Suite 'SecureRuntimeIdentityManifestFileTests' failed at 2026-09-29 09:47:11.796.
	 Executed 11 tests, with 3 failures (1 unexpected) in 0.021 (0.022) seconds
`````

### AppTests.SkeletonElementParityMatrixTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/SkeletonElementParityMatrixTests.swift:218: error: -[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips] : failed: caught error: "Error Domain=SkeletonElementParityMatrixTests Code=1 "managed SwiftPM cache does not expose the resolved CellProtocol checkout" UserInfo={NSLocalizedDescription=managed SwiftPM cache does not expose the resolved CellProtocol checkout}"
Test Case '-[AppTests.SkeletonElementParityMatrixTests testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips]' failed (0.002 seconds).
Test Suite 'SkeletonElementParityMatrixTests' failed at 2026-09-29 09:47:12.212.
	 Executed 3 tests, with 1 failure (1 unexpected) in 0.381 (0.381) seconds
`````

### AppTests.SkeletonRuntimeSourceTests

`````text
/private/tmp/cs-g3-20260929/Tests/AppTests/SkeletonRuntimeSourceTests.swift:103: error: -[AppTests.SkeletonRuntimeSourceTests testPortholeBootstrapUsesHttpSnapshotNotSocketFallbackWarning] : XCTAssertTrue failed
Test Case '-[AppTests.SkeletonRuntimeSourceTests testPortholeBootstrapUsesHttpSnapshotNotSocketFallbackWarning]' failed (0.025 seconds).
/private/tmp/cs-g3-20260929/Tests/AppTests/SkeletonRuntimeSourceTests.swift:45: error: -[AppTests.SkeletonRuntimeSourceTests testRuntimeDispatchesDropTargetPayloadAndHorizontalScrollAxis] : XCTAssertTrue failed
Test Case '-[AppTests.SkeletonRuntimeSourceTests testRuntimeDispatchesDropTargetPayloadAndHorizontalScrollAxis]' failed (0.016 seconds).
Test Suite 'SkeletonRuntimeSourceTests' failed at 2026-09-29 09:47:14.467.
	 Executed 18 tests, with 2 failures (0 unexpected) in 0.220 (0.221) seconds
`````

Samlede feilende suitedommer, ordrett:

`````text
Test Suite 'AppTests.xctest' failed at 2026-09-29 09:47:35.899.
Test Suite 'All tests' failed at 2026-09-29 09:47:35.903.
`````

## CI på main

Kontrollert 2026-09-29T09:41:29+02:00 med følgende kommando og samme credential-helper-oppsett som over:

`````text
/opt/homebrew/bin/gh run list --repo Digipomps/CellScaffold --branch main --limit 3 --json databaseId,conclusion,createdAt,headSha
`````

| Run | Opprettet (UTC) | SHA | Conclusion | Samme SHA som lokalt bygg |
|---|---|---|---|---|
| [36398574469](https://github.com/Digipomps/CellScaffold/actions/runs/36398574469) | 2026-09-28T08:38:33Z | `adf48d4615d1ed143d5bdc190fcf63e266214c8f` | `failure` | Ja |
| [36396091283](https://github.com/Digipomps/CellScaffold/actions/runs/36396091283) | 2026-09-28T08:13:34Z | `24b084690c23f3eb43de026c6d2cbc9a61cb1d3b` | `success` | Nei |
| [36384208337](https://github.com/Digipomps/CellScaffold/actions/runs/36384208337) | 2026-09-28T05:58:10Z | `c2dbbdd7191ba40bbe3436d39cc8a0b340487f71` | `success` | Nei |

Siste kjøring på den målte SHA-en er **failure**. De to grønne kjøringene i listen gjelder andre SHA-er. Ingen grønn CI-kjøring for den bygde SHA-en er dokumentert av denne tre-kjøringers listen.

Et forsøk på å hente detaljer for den røde kjøringen fikk følgende feil. CI-statusen over ble hentet vellykket både før bygg og under test; detaljfeilen er ikke grunnlaget for statusen.

`````text
failed to get run: Get "https://api.github.com/repos/Digipomps/CellScaffold/actions/runs/36398574469?exclude_pull_requests=true": net/http: TLS handshake timeout
`````

## Tidsbruk

Tidene nedenfor er målt med monoton klokke rundt hele kommandoen. Byggetiden inkluderer avhengighetshenting og versjonsberegning; testtiden inkluderer kompilering av testmålene.

| Kommando | Start (Europe/Oslo) | Slutt (Europe/Oslo) | Veggklokketid | Pipefail-status, kun til orientering |
|---|---|---|---:|---:|
| swift build | 2026-09-29T09:13:20+02:00 | 2026-09-29T09:40:18+02:00 | 1617.73 s (26 min 57.73 s) | 0 |
| swift test | 2026-09-29T09:40:54+02:00 | 2026-09-29T09:47:38+02:00 | 403.70 s (6 min 43.70 s) | 1 |

Swift oppgir selv 285,28 sek for bygg og 67,17 sek for kompileringen inne i testkommandoen. Disse tallene er gjengitt ordrett over og er ikke lik hele kommandotiden.

## Diskplass før og etter

`df -h /` før byggeforsøket:

`````text
Filesystem        Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s1s1   926Gi    13Gi    69Gi    16%    484k  725M    0%   /
`````

`df -h /` umiddelbart etter testkommandoen:

`````text
Filesystem        Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s1s1   926Gi    13Gi    63Gi    18%    484k  666M    0%   /
`````

Rapportert tilgjengelig plass: **69 GiB før, 63 GiB etter**. Dette er avrundede målinger for det delte filsystemet; differansen kan ikke tilordnes denne jobben alene.

## Råevidens og kontroll av opptelling

Råloggene er kopiert uendret fra målearbeidstreet. `measurement.json` inneholder tidene og kapasitetssjekkene; `ci-runs.json` inneholder det vellykkede CI-svaret.

Målefallgruve observert i denne kjøringen: enkelte XCTest-dommer er sammenføyd med annen stdout på samme linje. En opptelling som krever `Test Case` ved linjestart finner bare 2731 tilfeller. Opptellingen her søker også inne på linjene og stemmer med de fire mål-oppsummeringene: 2778 unike testnavn. De fire tomme Swift Testing-dommene er holdt adskilt fra XCTest.

| Fil | SHA-256 |
|---|---|
| [bygg.log](bygg.log) | `ef8a49d204db6e5250ccd887c009a514100e7f0c75c95ad97871b484004f9bd7` |
| [test.log](test.log) | `81f61f93cf244405f505f081ea764089e0ba1fe52ef80c53cc5dc780a0ea7a35` |
| [measurement.json](measurement.json) | `3308ec5e3843500f0be9111cbac652d7a80c652761557d44191f11d6211765d0` |
| [ci-runs.json](ci-runs.json) | `c530de69f2095cf623af2b3c59fa85feea72acae7976a90fa21b89abcb836dad` |
