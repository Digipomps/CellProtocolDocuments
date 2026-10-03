# WP-R4 — CellScaffold-integrasjon mot CellProtocol-kandidaten
STATUS: DELVIS — commit f851df4990e6da595b8daec40d34f2d6df6b3d10 på pdd/skjelett-elementer-web — mangler: grønt CI-filter; 21 stackkrasj og to feil i parity-matrisens revisjonskontroll

Bygget og de avgrensede WP-R4-testene er grønne uten midlertidig kodepatch. **Mergeporten er rød:** hele CI-filteret ble kjørt, og 22 av 30 bolker feilet. Det er ikke grunnlag for å si at grenen består CI.

## Grunnlag og porter

Kontrollert før øvrig arbeid:

- `WP-R1-FORMAT.md`: `STATUS: LEVERT — commit d224a4ed2b6b6b384dff4b8942978bae9f56ade0 ...`.
- `WP-R3-NATIVE.md`: `STATUS: DELVIS — commit c81a39799c3f664d77afa5f5de131ddac70f3c9c ...`.
- `WP-R2C-KILDEHANDLINGER.md`: `STATUS: DELVIS — commit bd60709b904244a804e1e4b49096ee1299d4dbd7 ...`.

Begge kode-worktrees var rene ved start. CellScaffold startet på `bd60709b904244a804e1e4b49096ee1299d4dbd7`, gren `pdd/skjelett-elementer-web`. CellProtocol-worktree `CellProtocol/_wt-skjellettelementer-wp-r1-20260918` stod og står på **`c81a39799c3f664d77afa5f5de131ddac70f3c9c`**, gren `pdd/skjelett-elementer`.

Kontrakten er [SKJELETT_ELEMENTER.md](SKJELETT_ELEMENTER.md), **iterasjon 7, §2.3**. Dette er lokal macOS-verifikasjon med Apple Swift 6.4, arm64 og Node v22.14.0. Workflowen bruker Linux / Swift 6.1; ingen GitHub Actions-kjøring eller Linux-kjøring er påstått.

## Permanent rettelse

Filnavn og linjer nedenfor gjelder CellScaffold-committen `f851df49`.

| Fil og linje | Endring og begrunnelse |
|---|---|
| `Sources/App/Cells/ConferenceMVP/Skeleton/ConferencePublicConfigurationPolicy.swift:87` | `Tree` avvises med `public configuration cannot contain trees; they always dispatch selection and expansion actions`. Formatets to handlingsfelt er obligatoriske; et tre kan ikke være skrivebeskyttet. |
| Samme fil, `:89` | `ComponentSurface` avvises med `public configuration cannot mount component surfaces`. Ekstern definisjon og kildehandlinger kan ikke behandles som offentlig skrivebeskyttet innhold. |
| Samme fil, `:120` og `:121` | Begge elementenes egne `modifiers` returneres. Switchene er fortsatt uttømmende; ingen `default:` eller `fatalError`. |
| `Tests/AppTests/ProductionSkeletonBindingIntegrityTests.swift:666` | `Tree` validerer data- og valgt-ID-binding, begge handlingenes referanselabel, krav om ikke-tom liste, strukturfelt i første rad og radmalen i radkontekst. Samme representative-rad-prinsipp som eksisterende `List`-sjekk. |
| Samme fil, `:696` | `ComponentSurface` validerer vertens `sourceKeypath`. Kildehandlinger skal ikke valideres mot vertens `cellReferences`; oppløst definisjon og autorisert kilderuting har egne format-/integrasjonstester. Dette er ikke en ny full mount-audit. |
| `Tests/AppTests/ConferenceEntityDiscoveryCellTests.swift:38,144,241,330,432,549,623,694,751` | Ni tvetydige typer kvalifiseres til `App.ChatCell`. CellBase har nå også `ChatCell`; dette er navnekollisjonen beskrevet i §2.3. |
| `Tests/AppTests/ConferenceShellCellsTests.swift:1343,4818` | Samme mekaniske kvalifisering på to steder. |
| `Tests/AppTests/ConferencePublicConfigurationPolicyTests.swift:9,34,51` | Tre nye tester: begge avslag ved rot og inni `VStack`; gyldig offentlig produksjonskonfigurasjon beholdes, også med nye visuelle modifikatorer. |
| `ci/test-filter.txt:457` | Ny separat bolk med `ConferencePublicConfigurationPolicyTests` og `PortholeComponentSourceActionTests`. Begge manglet som suiteoppføringer før endringen; kildehandlingene er nå inkludert i CI (R-E41). |

**Ingen ytterligere kompileringsbrudd ble funnet** i bygg eller kompilering av testmålene. Eksisterende advarsler står igjen, blant annet Sendable-advarsler og den allerede dupliserte `NavigationBar`-grenen i bindingtesten. «Bygg grønt» betyr exit 0, ikke advarselsfritt.

### Hvorfor modifikatorsjekken er uendret

Kontrollert i `SkeletonDescription.swift` ved CellProtocol `c81a3979`:

- `skeletonKnownKeys` (`:560`) avviser ukjente felt.
- `SkeletonInteractionStyle` (`:635`) har bare `background`, `foregroundColor`, `opacity`; dekoderen bruker den lukkede nøkkellisten. `SkeletonInteractionStyles` (`:679`) har bare de fire navngitte stiltilstandene.
- `SkeletonLayoutVariant` (`:785`, dekoding fra `:842`) har betingelse, mål, kapabiliteter og typede layout-/fargefelt. Ingen handlingsfelt; dekoderen bruker også `skeletonKnownKeys`.
- `SkeletonTree` (`:1963`) krever ikke-tomme `selectionActionKeypath` og `expansionActionKeypath` ved dekoding/enkoding.

Dette bekrefter formatkontrakten, ikke bare oppdragets påstand. `modifierValidationError` (`ConferencePublicConfigurationPolicy.swift:106`) er kontrollert byte-identisk med utgangspunktet: fortsatt bare forbud mot presentasjonens close-action og elementets drop-action. Formatets egne negative modifikatortester ble lest; CellProtocol-testsuiten ble ikke kjørt på nytt i WP-R4.

## Eksakte kommandoer og resultater

Arbeidskatalog for alle bygg-/testkommandoer:

```sh
cd /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919
mkdir -p /tmp/wp-r4-deps
ln -sfn /Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918 /tmp/wp-r4-deps/CellProtocol
ln -sfn /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/.build/checkouts/DiMyMicropayments /tmp/wp-r4-deps/DiMyMicropayments
ln -sfn /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/.build/checkouts/DiMyMint /tmp/wp-r4-deps/DiMyMint
export CELLPROTOCOL_LOCAL_PACKAGE_PATH=/tmp/wp-r4-deps/CellProtocol
export CLANG_MODULE_CACHE_PATH=/tmp/wp-r4-clang-cache
export SWIFTPM_MODULECACHE_OVERRIDE=/tmp/wp-r4-swift-cache
```

| Eksakt kommando | Exit | Tester og resultat |
|---|---:|---|
| `swift build --disable-sandbox` | **0** | Bygg fullført; ingen midlertidig kildepatch. [Logg](../evidence/wp-r4-integration/swift-build.log). |
| `swift test --disable-sandbox --filter 'PortholeComponentSourceActionTests\|ConferencePublicConfigurationPolicy'` | **0** | **13 bestått, 0 feil, 0 skippet**: 10 kildehandlingstester og 3 nye policytester. [Logg](../evidence/wp-r4-integration/swift-focused.log). |
| `ci/run-tests.sh` med miljø og wrapper under | **1** | Alle **30** CI-filterbolker forsøkt; **22 feilet**, 8 grønne. **1 232 testeksekveringer: 1 205 bestått, 2 feilet, 4 skippet, 21 avbrutt**. De resterende valgte testene i krasjede prosesser fikk ikke kjøre. [Samlelogg](../evidence/wp-r4-integration/swift-ci.log). |
| `swift build --disable-sandbox --force-resolved-versions --jobs 2 --product AdminScaffold` | **0** | CI-skriptets AdminScaffold-forberedelse; ingen tester. |
| `swift build --disable-sandbox --show-bin-path --force-resolved-versions` | **0** | CI-skriptets AdminScaffold-forberedelse; ingen tester. |
| `node --test scripts/skeleton-wp-r2-contract.test.js scripts/porthole-component-source-action.test.js` | **0** | **17 bestått, 0 feil, 0 skippet**. [Logg](../evidence/wp-r4-integration/node-test.log). |
| `HAVEN_PYTHON=/usr/bin/python3 ci/check-value-literals.sh` | **0** | 6 selvtester bestått; 27 store literaler, alle allerede i baseline. [Logg](../evidence/wp-r4-integration/value-literals-system-python.log). |
| `ci/test-suite-coverage.sh` | **0** | 333 suiter funnet, 313 dekket, 21 oppføringer i unntaksfilen; ingen suite uten registrering. |
| `/usr/bin/python3 scripts/verify-skeleton-parity-pin.py` | **0** | Kjørt etter at `Package.resolved` var gjenopprettet: den inncheckede matrisen og publiserte pinnen stemmer fortsatt med `533b42d5`. Dette opphever ikke de to kandidatfeilene under. |
| `git diff --check` og `git diff --cached --check` | **0** | Ingen whitespacefeil. |

`focused-tests` i `.github/workflows/admin-scaffold-image.yml:225` bruker faktisk `ci/run-tests.sh`, ikke én stor OR-kjøring. Jeg kjørte **det uendrede CI-skriptet**, med dets 20-linjers bolkdeling, eksplisitte `---`-grenser, `--jobs 2`, `--force-resolved-versions` og alle fem `--skip` fra `ci/test-skips.txt`:

```sh
export CI_SWIFT_BIN=/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/evidence/wp-r4-integration/ci-swift.py
export CI_TEST_LOGDIR=/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/evidence/wp-r4-integration/ci-chunks
ci/run-tests.sh
```

[Wrapperen](../evidence/wp-r4-integration/ci-swift.py) legger bare til `--disable-sandbox`, kjører kapasitetskontrollen og registrerer eksakt kommando og returkode. Den endrer ingen kildekode, filter eller forventning. Den faktiske formen er `swift test --disable-sandbox --force-resolved-versions --jobs 2 --skip ... --filter '<eksakt CI-bolk>'`.

**Alle 30 fullstendige kommandoer, exit-koder, antall tester per bolk og testnavn står i [CI-RESULTATER.md](../evidence/wp-r4-integration/CI-RESULTATER.md)**; maskinlesbare resultater i [ci-summary.json](../evidence/wp-r4-integration/ci-summary.json) og [ci-commands.jsonl](../evidence/wp-r4-integration/ci-commands.jsonl). Filteruttrykkene er uavhengig rekonstruert fra den committede `ci/test-filter.txt` og sammenlignet identisk med de kjørte argumentene ([bevis](../evidence/wp-r4-integration/filter-equivalence.json)). Bolk 30 inneholder de to nye oppføringene: **13 tester, exit 0**.

Testtallene er eksekveringer, ikke unike metodenavn på tvers av bolker: CI-filterets eksisterende delstrengsmatching kan kjøre samme suite i flere bolker. Avbrutt betyr at en test startet uten sluttstatus før prosesskrasj. Fem metoder er ekskludert med CI-skriptets `--skip`; de fire rapporterte skippene over er i tillegg tester som XCTest selv rapporterte som skippet.

### Feilende testnavn: revisjonskontroll

Begge er i bolk 23, exit 1, og begge forventer `533b42d5dc25cf1453cbe5ad08f523d47d5d32e9`, men observerer den påkrevde kandidaten `c81a39799c3f664d77afa5f5de131ddac70f3c9c`:

- `SkeletonElementParityMatrixTests.testMatrixRevisionMatchesPackagePin` — `Tests/AppTests/SkeletonElementParityMatrixTests.swift:125`.
- `SkeletonElementParityMatrixTests.testNamedCorpusMatchesPinnedSkeletonElementEnumAndRoundTrips` — samme fil `:87`.

Matrisens corpus er fortsatt de 24 gamle elementcasene (`:62` i testen). Å erstatte revisjonsfeltet alene ville ikke være nytt paritetsbevis. Jeg endrer derfor verken matrise, assertions eller skips for å få grønt. Kandidat-/publiseringsproveniens må avklares sammen med corpus og den senere publiserte pinoppdateringen; dette er ikke et mekanisk kompileringsbrudd.

### Tester avbrutt av stackkrasj

Alle de 21 prosesskrasjene er bekreftet av egne macOS-rapporter med `Thread stack size exceeded`, `SIGBUS`, signal **10**. [Utdrag med tidsstempel, PID og stack-symboler](../evidence/wp-r4-integration/crash-summary.json). Stackene peker blant annet på `ConfigurationCatalogCell.retintClaudeVisuals`, `PersonalCopilotConfigurationFactory.chatHubSkeletonBody` og skeleton-JSON-enkoding. Disse rutinenes kildekode er uendret i WP-R4; det er **ikke** dermed bevist at samme feil oppstår på uendret main eller i Linux-CI. Det ble ikke lagt inn større teststack eller annen midlertidig omgåelse.

| Bolk | Test som startet, men ble avbrutt |
|---|---|
| 1 | `AppTests.PortholeWebSessionPersonaTests.testBootstrapConfigurationListsAreLightweightSummaries` |
| 2 | `AppTests.PortholeIdentityContinuityRoutesTests.testCoPilotChatLoadsWhileUnprovenHistoricalAuxiliariesRemainUntouched` |
| 4 | `AppTests.AdminCopilotWorkspaceConfigurationTests.testAdminOperationsWorkspaceBootstrapHydratesNodeFleetDashboard` |
| 5 | `AppTests.ChatPurposeResourceRouterTests.testScaffoldEntityAtlasDedupeRuntimeDuplicateByEndpointAndName` |
| 6 | `AppTests.ConfigurationCatalogCellTests.testCatalogContractsExposeSharedContractShapeAndParityFixtures` |
| 7 | `AppTests.ArendalsukaConfigurationPublisherCellTests.testPortholeCommitRuntimePersistsOfficialSkeletonAcrossFreshSession` |
| 8 | `AppTests.ConferenceShellCellsTests.testPortholeSessionDetailPreparesLiveThreadForSelectedPreviewSession` |
| 9 | `AppTests.PortholeMenuFallbackTests.testDefaultCatalogBuildsOnceWithinRequestScope` |
| 10 | `AppTests.PurposeCellTests.testPalazzoFixtureDecodesLosslesslyIntoPurposeModelAndConfigurationIsPublished` |
| 12 | `AppTests.CellConfigurationStudioImportTests.testDecodedStudioInstallsPrivateImportRuntimeBindingBeforeStateRead` |
| 16 | `AppTests.ButlerSignalMatcherTests.testAnalysePromptNowReachesTheAdvisoryReportHelper` |
| 18 | `AppTests.ConferenceConfigurationCatalogTests.testConferenceCatalogConfigurationsLoadAsWorkspaces` |
| 19 | `AppTests.ConfigurationCatalogCellTests.testCatalogBootstrapsRAGGatewayEntryAndExposesMenuConfiguration` |
| 20 | `AppTests.ExecutablePurposeGroundingCellTests.testAdvisoryPanelPromptWithoutSubjectReportsMissingContext` |
| 21 | `AppTests.OrchestratorPersistenceTests.testLegacyPortholeSnapshotRecoversConfigurationFromSidecar` |
| 22 | `AppTests.ProductionSkeletonBindingIntegrityTests.testArendalsukaEventAtlasPortholeTabsAndDetailsDoNotReturnNotFound` |
| 24 | `AppTests.SwarmIdentityAdmissionCellTests.testAdminObserverCatalogIncludesSwarmAdmissionOnlyForProvedRequester` |
| 25 | `AppTests.PersonalCopilotHelperTreeTests.testPromptSubmitRecordsSelectedNodeThroughProductionAppendPath` |
| 27 | `AppTests.PersonalCopilotWidgetCanvasTests.testCancelWithoutDropLeavesTheCellAndDiskUnchanged` |
| 28 | `AppTests.PortholeWebRemoteConfigurationTests.testBuiltInAdminNavigationResolvesLocalFactoryBeforeRemoteExportAdmission` |
| 29 | `AppTests.ButlerBuiltInConfigurationUpgradeTests.testNormalBootstrapAndSameSurfaceLoadPersistThreadControls` |

Denne delen stoppes som runtime-/stackarbeid, ikke repareres ved å svekke testene. Særlig `ProductionSkeletonBindingIntegrityTests` i bolk 22 ble avbrutt i den eksisterende Arendalsuka-testen; fullført kompilering av dens nye switch er derfor ikke det samme som en grønn integritetssuite.

### Kjent Node-feil

`porthole-arendalsuka-action-state.test.js:359` er **ikke i `ci/test-filter.txt`**, som er et Swift-filter. `focused-tests`-jobben kaller heller ikke npm-scriptet `test:arendalsuka-action-state`. Filen ble ikke kjørt i WP-R4 og ikke endret. Påstanden om feil på uendret main kommer fra oppdraget/tidligere bevis; WP-R4 har ikke repetert den målingen. De to uttrykkelig bestilte Node-filene ble kjørt og bestod alle 17 tester.

## Maskinavvik og avgrensning

- De eksplisitte Swift-kommandoene i oppdraget ble fulgt, som i WP-R2c, fremfor AGENTS.md sin generelle bounded-runner-regel. Eksisterende `.build` ble gjenbrukt; ingen ny scratch-buildrot ble opprettet.
- `HAVEN_BUILD_MIN_FREE_PERCENT=10 scripts/check_build_capacity.sh .` ga først **exit 75**: ca. 82,0 GiB ledig, 72,0 GiB etter reserve, 7 %. Repoets faktiske kapasitetskript har imidlertid en dokumentert **5 %** standard, i strid med 10 %-teksten i AGENTS.md. Standardkommandoen `scripts/check_build_capacity.sh .` bestod før bygg (81,6 GiB ledig; 71,6 GiB / 7 % etter reserve) og før hvert Swift-testkall. Denne forskjellen skjules ikke som et bestått 10 %-krav.
- Literalvakten feilet først med **exit 1** fordi Bash valgte `/usr/local/bin/python3.12` med feil CPU-arkitektur. Forsøk med `HAVEN_PYTHON=python3` feilet også fordi Bash valgte `/usr/local/bin/python3`. Den støttede miljøvariabelen ble deretter satt til fungerende `/usr/bin/python3`; samme vakt og alle seks selvtester bestod. Ingen kildeendring for dette miljøproblemet.
- Hele deploy-/image-workflowen, Playwright, Python-vedlikeholdsgatene og remote CI ble ikke kjørt. Resultatet gjelder de uttrykkelig bestilte kommandogruppene og tilleggssjekkene listet over.

## Commit og videre integrasjonsrekkefølge

**Én commit**: `f851df4990e6da595b8daec40d34f2d6df6b3d10` på `pdd/skjelett-elementer-web`, med forelder `bd60709b904244a804e1e4b49096ee1299d4dbd7`. Committen inneholder bare de seks filene i endringstabellen. [Full committet diff](../evidence/wp-r4-integration/working-change.patch).

`Package.resolved` er gjenopprettet **byte for byte** til inngangsverdien etter lokal SwiftPM-resolusjon: SHA-256 `39ae0a400e5e26783ff16e59dad05fbcc117ddf81c1d5de7aa1693da4515caf8`. Verken denne filen eller `Package.swift` er i committen. CellProtocol er ikke endret. Ingen `git push`, `gh`, `ssh` eller `curl` ble kjørt.

CellScaffold-worktree-en er ren etter commit. Dokumentrepoet hadde mange eksisterende endringer og uregistrerte leveranser ved start; de er bevart. Denne handoffen og evidensmappen er lokale dokumentleveranser, uten en ekstra dokumentcommit.

Pinnen oppdateres først etter at CellProtocol-grenen er merget til main, som bestilt. Før en grønn mergeport kan hevdes, må stackfeilene håndteres og kandidatens parity-proveniens/corpus avklares, deretter må hele CI-filteret kjøres grønt. WP-R4 har ikke levert dette siste beviset.
