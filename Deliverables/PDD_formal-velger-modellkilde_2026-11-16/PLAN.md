# PLAN — La formålet velge språkmodellkilde

Oppgavemappe: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_formal-velger-modellkilde_2026-11-16/` · Skrevet 2026-11-17 · G1 og G1-GUI godkjent 17.11 · **G2 venter**

Målt mot: CellScaffold `57ce8c0` (main 17.11), HavenAgentD `0e18eff` (main 10.11), CellProtocolDocuments `3cd1031`.

## Fakta planen bygger på (lest 17.11)

- AgentD melder laptop-modellen automatisk ved tilkobling: `HavenAgentD/Sources/HavenAgentRuntime/PortholeIngressSession.swift:187–197` setter `native.localModel.register` med `contractID` og `providerID` når kontrakten har `cap.local_model.generate`. Profilen har `role` (`test-playground`, `gdpr-local-norwegian-assistant`) og `isExperimental` (`AgentLocalModelCell.swift:23–120`), men de sendes ikke med.
- På verten tar `OrchestratorCell` imot (`CellScaffold/Sources/App/Cells/SimpleProjectManager/OrchestratorCell.swift:340`), og `NativeLocalModelBridgeRegistry` holder økten til socketen lukkes (`VaporSproutResolver.swift:88–100`). Ingen tilbaketrekking, ingen hendelser.
- Valglisten: `chatHub.state.assistant.providerChoices` i AI-panelet (`PersonalCopilotConfigurationFactory.swift:2270–2290`).
- Bygg: hele CellScaffold App bygger ikke i skyen (private DiMy-pakker). Rene Swift-filer kan kompileres og testes i Docker `swift:6.1-noble` i en egen pakke. App-tester kjøres i CI og på Macen. HavenAgentD-menyen er macOS og bygges bare på Macen.

## Endring i oppførsel du bør vite om

I dag blir laptop-modellen synlig for deg i det øyeblikket AgentD kobler til. Etter planen er tilkoblingen bare et håndtrykk: modellen blir ikke synlig før du sier «tilgjengelig» i AgentD-menyen. Det følger av «når jeg sier den er tilgjengelig» (G1).

## Arbeidspakker

Én pakke per bladformål, i rekkefølgen de må bygges. Utfører: **Claude** skriver kode og tester i skyen og lager PR; **Mac** betyr at bygg/test kjøres på Macen din (Codex eller Remote Control) før PR-en tas ut av utkast; **Kjetil** er dine valg.

| WP | purposeRef (blad) | Hva | Filer | Test(er) som skal bli grønne | Utfører |
|---|---|---|---|---|---|
| 0 | quality.build-and-regression | Baseline: CI på CellScaffold main, `swift test` i HavenAgentD på Macen. Tallene skrives i TESTRESULT.md før første endring | — | test.build, test.regression (baseline) | Claude (CI), Mac (AgentD) |
| 1 | likt-i-alle-sprak, kilde-fakta, formal-krav | Kontrakt + fixtures: kildefakta, kravene til de tre formålene, egnethetsvektorer (formål × kilde → ja/nei + grunn) og hendelsesskjemaet | CellProtocolDocuments `Book/model_source_eligibility_contract_v1.json`, `Book/fixtures/model-source-eligibility/*.json` | test.cell.contract-fixtures, T-KRAV | Claude |
| 2 | hardt-filter (kjernen) | Ren Swift-funksjon `ModelSourceEligibility.evaluate(purpose:source:) -> (eligible, unmetRequirements)` | CellScaffold `Sources/App/Support/ModelSourceEligibility.swift` + `Tests/AppTests/ModelSourceEligibilityTests.swift` | T-KRAV, fixturene fra WP1 (kjøres i Docker før PR) | Claude |
| 3 | kilde-fakta | Nye felt på `ChatScopedAIProviderDescriptor` (`servingClass`, `servesWhom`, `availableWhenOwnerOffline`, `measuredHealth`, `region`, `pricePerMTokInput/Output`, `offeredByDiMy`) fylt for alle sju kildetyper; ukjent = `unknown` | `ChatScopedAIProviderRouter.swift` | T-FAKTA | Claude |
| 4 | uttalt-formal, hardt-filter | `route(...)` filtrerer på formålets krav før `score(...)`. Formålet hentes fra Perspective/flaten; ukjent = «tjeneste for andre» | `ChatScopedAIProviderRouter.swift`, `PersonalCopilotCloudStore.swift:10896` | T-FILTER, T-UTTALT | Claude |
| 5 | vertscelle-tilgjengelighet | Ny celle `cell:///LocalModelAvailability` på verten: tilstand per erklært laptop-modell, lesing via Agreement-vilkår (eier + dem eieren har gitt Agreement) | CellScaffold `Sources/App/Cells/LocalModelAvailability/*` + registrering i resolveren | T-VERTSCELLE, test.cell.auth-negative | Claude |
| 6 | si-fra-tilgjengelig (vert) | `localModel.availability.declare` godtas bare fra broens identitet med `cap.local_model.generate`; `withdraw` fra eieren hvor som helst; lukket socket / utløpt kontrakt / feilet helse trekker tilbake med grunn. Registreringen i `NativeLocalModelBridgeRegistry` gjør ikke lenger modellen synlig alene | `NativeLocalModelBridge.swift`, `OrchestratorCell.swift`, `VaporSproutResolver.swift` | T-SI-FRA | Claude |
| 7 | enhetsregister, si-fra-tilgjengelig (laptop) | AgentD-menyen får «Gjør laptop-modellen tilgjengelig / utilgjengelig». Erklæringen sender modellprofil, `role` og `isExperimental`; rollen `test-playground` blir `utvikling` | HavenAgentD `AgentMenuModel.swift`, `PortholeIngressSession.swift`, `AgentLocalModelCell.swift` | T-ENHET, T-SI-FRA (laptopsiden) | Claude skriver, **Mac** bygger og tester |
| 8 | hendelser | Vertscellen poster FlowElement på `haven.agent.local-model.availability.v1`: `available`, `unavailable`(grunn), `health`, `fallback_used`, `selected`. Ingen prompttekst | vertscellen + `PersonalCopilotCloudStore.swift:7750` (tilbakefall) | T-HENDELSER | Claude |
| 9 | malt-helse | Lett helsesjekk for laptop og lokal LLM, hurtiglagret N min; `unknown` uten måling | `NativeLocalModelBridge.swift`, ny `ModelSourceHealth.swift` | T-HELSE | Claude |
| 10 | likeverdig-valg | `providerChoices` får `whereLabel`, `factsLabel`, `badge`; laptopen vises for Agreement-holdere, aldri autovalgt for andre; panelet får «Min maskin» og «Hendelser» som i bildene | `PersonalCopilotConfigurationFactory.swift`, `PersonalCopilotCloudStore.swift`, `PersonalCopilotCells.swift` (grants) | T-LIKEVERDIG, test.gui.parity (web), test.skeleton.* | Claude (web), **Mac** (Binding-paritet) |
| 11 | tjeneste-for-andre | Kallimachos «lokal» brukes bare med målt helse; ellers hostet rute fra DiMys liste eller beskjed | `Cells/AI/KallimachosAdvisorCell.swift:107` | T-TJENESTE | Claude; hostet rute venter på tråden «Mistral med dagsgrense» |
| 12 | ingen-egnet | Ny art `requirementNotMet` i `ModelRouteUnavailability` med navnet på kravet | `Support/ModelRouteUnavailability.swift` (fra #445) | T-INGEN | Claude; venter på at #445 lander |
| 13 | forklart-valg | Kvitteringen får `purposeRef`, `servingClass`, `requirementsRevision`; panelet viser «valgt fordi …» | `PersonalCopilotCloudStore.swift` (`appendProviderUsageReceipt`) | T-FORKLART | Claude |
| 14 | vertsfakta | Vertsfakta som fixture (16.11-målingen); `operator_host`-kilder får dem ved siden av seg | WP1-fixtures + `ModelSourceEligibility.swift` | T-VERT | Claude |
| 15 | tilgang-via-agreement | Negative tester på tvers: fremmed, utløpt Agreement, `purpose://prompt.unknown` | tester i WP5/WP10 | test.cell.auth-negative | Claude |
| 16 | likt-i-alle-sprak | Samme egnethetsfunksjon i PyCellProtocol og GoCellProtocol, testet på WP1-fixturene | PyCellProtocol, GoCellProtocol | T-SPRAK | Claude |
| 17 | everything-works | Full regresjon, Book 24 (modellkilder) oppdatert med «Last verified against code», TESTRESULT/ACCEPT, FORESPOERSEL til HAVEN-Deploy etter grønt bygg | — | test.build, test.regression, test.docs-updated, test.status-current | Claude; **Mac** for full kjøring |
| 18 | abonnement-bare-eier | Kontrakt: `source.credentialKind`, `context.audienceIncludesOthers`, kravet `owner_only_subscription` (vurderes rett etter `owner_or_explicit_choice`), nye vektorer, Python-referansen. CellScaffold: feltet på `ChatScopedAIProviderDescriptor` (AgentD-laptopen melder `local_weights` når den kjører llama-server; uten melding `unknown`), felles chat setter `audienceIncludesOthers` når det er flere deltakere enn spørreren. HavenAgentD: erklæringen fra WP7 får `credentialKind`. Py/Go i WP16 | CellProtocolDocuments `Book/model_source_eligibility_contract_v1.json`, `Tools/ModelSourceEligibility/*`; CellScaffold `ModelSourceEligibility.swift`, `ChatScopedAIProviderRouter.swift`; HavenAgentD erklæringen | T-ABONNEMENT | Claude (skyen + CI), Mac for AgentD |

## Leveranse i PR-er

1. CellProtocolDocuments: WP1 (kontrakt og fixtures).
2. CellScaffold, én PR: WP2–6, 8–10, 13–15. Utkast til CI og Mac-kjøring er grønne.
3. HavenAgentD: WP7.
4. CellScaffold, oppfølging: WP11 og WP12 når Mistral-listen og #445 har landet.
5. PyCellProtocol + GoCellProtocol: WP16.

## Dataflyt

| Kant | Fra → til | Endepunkt / hendelse | Kontrakt |
|---|---|---|---|
| Erklær | AgentD (laptop) → `LocalModelAvailability` | set `localModel.availability.declare` over broen | WP1 |
| Trekk tilbake | Eier (web/Binding/AgentD) → `LocalModelAvailability` | set `localModel.availability.withdraw` | WP1 |
| Bro lukket | `VaporSproutResolver` → `LocalModelAvailability` | intern kall ved `socket.onClose` | WP1 (grunn `bridge_closed`) |
| Hendelser | `LocalModelAvailability` → abonnenter med Agreement | FlowElement `haven.agent.local-model.availability.v1` | WP1 |
| Kandidater | `LocalModelAvailability` + AIGateway + katalog → `ChatScopedAIProviderRouter.route` | `get localModel.availability.state` | WP1 |
| Valg | `route` → Co-Pilot-panel / Kallimachos | `chatHub.state.assistant.providerChoices` | WP1 |

## Kobling til Informasjonssystemer-gruppa (lagt til 17.11, ikke godkjent)

Tråden «Opprett Informasjonssystemer som gruppeentitet» (CellProtocolDocuments PR #46, G1 spurt) foreslår at gruppa utsteder rolle-VC-er (student med kull, researcher, supervisor) som celler sjekker med `ProvedClaimCondition` og `TrustedIssuer`. WP5 kan da bruke «har studentrolle fra Informasjonssystemer» som Agreement-vilkår for hvem som ser laptop-modellen, i stedet for et eget vilkår. Det forutsetter at den PDD-en får G1; inntil da bygges WP5 med eierens egne Agreement.

## Ikke i denne planen

- Binding-knapp for «tilgjengelig» på laptopen. AgentD-menyen er første vei inn; Binding viser panelet (web-skjelettet) og kan trekke tilbake.
- Selve DiMy-listen og mikrobetalingen (tråden «Mistral med dagsgrense»).
- Fullt enhetsregister for alle enheter i entiteten (telefon, andre maskiner). WP7 gir laptopen rolle; resten bygger på maskinprofil F1 i Sprout-PDD-en, som ikke er lest her.

## Risiko

- App bygger ikke i skyen. Det første fulle bygget av CellScaffold-endringen skjer i CI. For at ikke noe ubygget skal havne i staging-køen, tas PR-en ikke ut av utkast før CI og en kjøring på Macen er grønne.
