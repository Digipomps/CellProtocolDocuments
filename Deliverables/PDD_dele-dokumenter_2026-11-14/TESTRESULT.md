# TESTRESULT — dele dokumenter

## baseline

WP0, 2026-11-22, kjørt på Kjetils Mac (Remote Control). Rene `git clone` i `/Volumes/Backup/build/dele-dok-20261122/` (`/tmp/dele-dok-20261122` er en symlink dit). Hovedutsjekkene er ikke rørt.

| Repo | Commit | Kommando | Resultat |
|---|---|---|---|
| CellProtocol main | `4f099cc4f25dc10fc315760e94119aca77ec0629` | `swift test` | CellBaseTests 2043 (6 hoppet over, 0 feilet), HavenCommonsTests 26, CellNearbyTests 3. Til sammen 2072, 0 røde. **Grønn** |
| CellScaffold main | `98c9aed69219b012ca5f9f7a07896f8c4ab14783`, mot CellProtocol `dc1de6f83221b034c9d5511e8979717d5120acbf` (Package.resolved), `CELLPROTOCOL_PUBLISHED_API=1` | `swift test` | AppTests 3727 (24 hoppet over), 39 røde testcaser (144 feilede påstander). UserSimulationScaffoldTests 28, NodeAdminDockerCollectorTests 4, FlowPlacementHomeTests 5, AdminPlaneTests 36, alle uten feil. Til sammen 3800. Exit 1. **Ikke grønn** |

De 39 røde i CellScaffold main fantes før denne oppgaven: AIAssistantThreadCellTests 4, ArendalsukaImportAuthorizationRoutesTests 1, BookReferenceRoutesTests 8, ButterpopStudioProductTests 1, ConferenceEntityDiscoveryCellTests 1, ConferenceOrganizerProjectionCellTests 2, ConferencePublishedContentCellTests 1, ConferenceSchedulingCellTests 1, ConferenceSponsorLeadAggregateCellTests 1, ConferenceSurfaceRoutesTests 8, ContractChallengeMVPRoutesTests 2, MarkdownRendererCellTests 4, MicropaymentsMVPRoutesTests 1, MusicPublishingCellsTests 1, PortholeConfigurationLoadingTests 1, SkeletonRuntimeSourceTests 2. Hele listen ligger på Macen: `/Volumes/Backup/build/dele-dok-20261122/baseline-cellscaffold-failed.txt`. Loggene ligger i `/Volumes/Backup/build/dele-dok-20261122/logs/`.

Konsekvens for WP12: kravet er «ingen nye røde utover disse 39», og antallet tester skal øke med nøyaktig antallet nye. Det er ikke det samme som «grønn». Årsakene til de 39 er ikke undersøkt.

Avvik fra PLAN.md: baselinen er tatt på dagens main (CellScaffold `98c9aed`, CellProtocol `4f099cc`). Planen ble skrevet mot `272580b` og `669850b`.

## workbench

2026-11-22: ikke ført. Broen fra agenten (haven-agentd) har bare `state` og `query` mot `kjetil2-staging-work` og `kjetil2-staging-projects`. `capture` mangler, og `review.import` finnes ikke der. Eneste vei er Kjetils innloggede Chrome-økt mot https://staging.haven.digipomps.org (passkey). Et utkast som ikke er kjørt ligger i `/Volumes/Backup/build/dele-dok-20261122/pdd/workbench-payload-UKJORT.json`. Det er ingen Workbench-post.
