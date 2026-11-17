# Kildeavklaring — 2026-10-12

CellScaffold lest på 9ff06f8446b6331da49272f5fd72b947b4092ece i det aktive Workbench-arbeidstreet. Dette er kildebevis, ikke bevis for hvilken revisjon staging kjører.

Uavhengig leser: `/root/workbench_spec_review`; tidsavgrenset, ingen skriving eller tester.
Alle linjer nedenfor er avgrensede utdrag, ikke hele gjennomleste mapper:

- `Sources/App/Cells/WorkItems/DeveloperWorkbenchConfiguration.swift`: 60–90 åpner addConfiguration med launchPayload; 126–169 eksisterende formålstre og node-dialog.
- `Sources/App/Cells/WorkbenchAccess/WorkbenchAccessGrantCell.swift`: 593–598 gir projectSelection bare ved canEdit; viewer kan fortsatt ha launchAvailable. Utestet i levende leserøkt.
- `Sources/App/Controllers/PortholeWebSessionSupport.swift`: 3509–3517 laster konfigurasjon, 5497–5521 validerer portfolioUUID og sender select. Ingen ny prosjektpost her.
- `Sources/App/Cells/WorkItems/ProjectPortfolioCell.swift`: 265–344 status/helse/prioritet/milepæler/ref; 424/450/489 én persistert selectedProjectID; 1292–1315 select + Flow, ingen dashboard-navigasjon; 1966 fallback første prosjekt.
- `Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift`: 8382ff fem faner, intake først og tom activeTabStateKeypath ved 8494; captureDraft ved 9034; WorkItem tavle/detaljer 9698–10131.
- `Sources/App/Cells/WorkItems/WorkItemCell.swift`: 2055–2087 query sammenligner prosjekttekst; 2091–2177 generell board/detaljstate. workItemRefs er ikke automatisk prosjektfiltrering.
- `Sources/App/Cells/Graph/GraphStoreCell.swift`: 1777–1855 noder/kanter/selectedNode/selectNode.
- `Sources/App/Cells/WorkItems/WorkMutationSync.swift`: 160ff asynkrone grafoppdateringer der feil ignoreres. Ingen garanti om fullstendighet.
- `Sources/App/Cells/WorkItems/AgentRunCell.swift`: 12 observasjonsrolle, 1052–1058 executionControlOperations=[]; `AgentRunWorkbenchConfiguration.swift`: 74–83 automatisk runtime-observasjon utilgjengelig.
- `Tests/AppTests/WorkbenchAccessGrantConfigurationTests.swift`: 1562–1599 prosjektvalg, men skjelettet byttes til én Text ved 1570. `ProjectPortfolioCellTests.swift`: 9–40 selection/state, ikke synlig dashboard.
- `Public/js/skeleton-runtime.js`: 3376–3575 purposeTree, 4393–4654 network klikking/pan/zoom, 7197 første tab fallback. Hovedtråd leste også network 4393–4625: mørke inline-farger og DOM gjenskapt på klikk; ikke jevn relasjonsfokusovergang.
- Andre utdrag hos leser: `Public/js/porthole-webo.js`: 4107; `Public/css/porthole-webo.css`: 6104; `Sources/App/Support/AgentActionCapabilityCatalogV1.swift`: 145.

Hovedtråd leste dessuten CellProtocol CellConfiguration.swift 1–130; SkeletonDescription.swift enum/Visualization/Tabs-ankere; SkeletonTests.swift Visualization/Tabs-testankere. Explore Chapter 22, PDD Chapter 35 og Purpose_Driven_Dev_Spec er lest for kontrakt/arbeidsmåte. Formålskanon og pakker/lessons er klassifiseringsgrunnlag, ikke runtime-bevis.

HavenAgentD primæruttrekk `Docs/AgentJobs.md` er gammel v1-beskrivelse på lokal main ba148955; den kan ikke bevise gjeldende durable submit/state/kansellering. MCP-katalogens annonserte submit/state/list er lest, ingen kall utført og ingen jobber startet. Aktuell AgentD-kandidat, full autorisasjonskjede, Binding/native, komplett grafkilde, live requester-ID og deploy-revisjon er ulest/umålt her.

Live Chrome: eksisterende innlogget side viste Live, 14 prosjekter, Portfolio; Åpne på Robotikkverksted markerte kortet uten detaljside. Ingen ny prosjektpost eller jobb opprettet. Brukerens to skjermbilder er inngangsevidens. Ny kandidat bruker utelukkende syntetiske eksempler.
