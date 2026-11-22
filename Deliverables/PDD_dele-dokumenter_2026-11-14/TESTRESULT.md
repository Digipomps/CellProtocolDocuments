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

2026-11-22 kl. 21.30, ført i Developer Workbench på https://staging.haven.digipomps.org fra Kjetils innloggede Chrome-økt (requester kjetil2). Lest tilbake etter at siden var lastet på nytt.

- Formål: `review.import` med id `dele-dokumenter-2026-11-14`, revisjon 1 (25 noder, port G3). G1, G1-GUI og G2 er ikke ført som beslutninger i Workbench.
- Prosjekt `dele-dok-20261114-project`: event `event-12dc60a5-c84b-48db-b77c-cdae8b5c7b97`, stateVersion 135, 15 workItemRefs.
- WorkItems `dele-dok-20261114-wp0` … `wp14`: stateVersion 678–692 (`eventsSince(676)` → 692). wp0 er done med evidens fra baselinen, wp1 er in-progress, wp2–wp14 er ready. Avhengighetene ligger som dependencyRefs.
- Skjermbilder på Macen: `/Volumes/Backup/build/dele-dok-20261122/pdd/workbench-formaal-20261122.jpg` og `/Volumes/Backup/build/dele-dok-20261122/pdd/workbench-prosjekt-20261122.jpg`.
- GraphStore-replay av graphUpdates er ikke verifisert.
