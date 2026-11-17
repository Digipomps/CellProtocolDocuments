**Tre: bindingskontrakt og mangler**

Alle navn under `helperTree` nedenfor er **forslag**, ikke eksisterende cellekontrakt. KEYPATH-MANGLER står bare i denne kommentarfilen, aldri i JSON. Kandidaten bruker dem fordi eksisterende flate hjelpertyper/tråder ikke er det etterspurte hierarkiet. Den er dermed ikke koblet til virksomme tree-data på dagens server. Ingen innbakte 4/34/12/5-tellere erstatter manglende celledata.

Konfigurasjonen er `Co-Pilot Chat`, referanselabel `chatHub`, source endpoint `cell:///PersonalChatHub`. Kilde: **origin/main** `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift:234`; `CellProtocol/Sources/CellBase/PersonalCopilot/PersonalCopilotContracts.swift:110`. Kandidaten er bare SkeletonElement, og preview må bevare konfigurasjonens cellReferences; selve formatfeltet finnes i `CellProtocol/Sources/CellBase/CellConfiguration/CellConfiguration.swift:154`.

| binding i kandidaten | foreslått verdi / krav | status |
|---|---|---|
| `chatHub.state.ui.helperTree.conversationSummary` | String; fixture fylt «4 samtaler», tom «1 samtale». Telledefinisjonen må avtales; ikke antall synlige rader. | KEYPATH-MANGLER:chatHub.state.ui.helperTree.conversationSummary |
| `chatHub.state.ui.helperTree.scopeSummary` | String; «Undertre · 2 grener» / «Undertre · 0 grener» eller tilsvarende for node-modus. | KEYPATH-MANGLER:chatHub.state.ui.helperTree.scopeSummary |
| `chatHub.state.ui.helperTree.visibleRows` | Array av radobjekter i preorden, inkludert Butler-roten; synlige etter expanded. Tom chat har én rot, ikke tom array. | KEYPATH-MANGLER:chatHub.state.ui.helperTree.visibleRows |
| `chatHub.state.ui.helperTree.scopeControlRows` | 0/1 array; normalt én rad `{mode:"subtree"}` eller `{mode:"node"}`. 0 betyr at kontrollgrunnlaget ikke er levert. | KEYPATH-MANGLER:chatHub.state.ui.helperTree.scopeControlRows |
| `chatHub.ui.helperTree.selectNode` | action `{nodeID:String}`; ikke dagens setActiveHelper | KEYPATH-MANGLER:chatHub.ui.helperTree.selectNode |
| `chatHub.ui.helperTree.setExpanded` | action `{nodeID:String,expanded:Bool}` | KEYPATH-MANGLER:chatHub.ui.helperTree.setExpanded |
| `chatHub.ui.helperTree.setScopeMode` | action `{mode:"subtree"\|"node"}` | KEYPATH-MANGLER:chatHub.ui.helperTree.setScopeMode |
| `chatHub.ui.helperTree.open` | action `{}`; kompakt treinngang. Kandidaten har ingen drawer. | KEYPATH-MANGLER:chatHub.ui.helperTree.open |

| lokale rad-keypaths brukt i JSON | type / semantikk | status |
|---|---|---|
| `title` | String; nodeinstansens navn, roten «Butler». Button-fallback «Butler» er ikke bevis for at rotdata finnes. | KEYPATH-MANGLER:visibleRows[].title |
| `countText` | String; ferdig teller fra cellen, ikke formattering/filtrering i skjelettet. | KEYPATH-MANGLER:visibleRows[].countText |
| `visualDepth` | Int 0,1,2; velger konstant mal. 0 brukes både for Butler og toppsamtalene i referansen. Andre verdier er utenfor kandidaten. | KEYPATH-MANGLER:visibleRows[].visualDepth |
| `rowState` | String normal/selected/inscope; cellen bestemmer prioritet. Manglende verdi gjør at ingen variant vises. | KEYPATH-MANGLER:visibleRows[].rowState |
| `tone` | String neutral/branchA/branchB/declined; alle rader må levere en av disse. | KEYPATH-MANGLER:visibleRows[].tone |
| `kindSummary` | String «», «gren» eller «gren · avslo»; tom streng skjuler bare merket. | KEYPATH-MANGLER:visibleRows[].kindSummary |
| `hasChildren` | Bool; skiller disclosure-knapp fra tom pilplass. Mockupens piler på bladlignende rader avgjør ikke denne verdien. | KEYPATH-MANGLER:visibleRows[].hasChildren |
| `disclosureGlyph` | String ▾/▸, bare når hasChildren; en tegnevariant, ikke utbrettingslogikk. | KEYPATH-MANGLER:visibleRows[].disclosureGlyph |
| `selectionPayload` | Object `{nodeID:String}`; stabil instans-ID | KEYPATH-MANGLER:visibleRows[].selectionPayload |
| `expansionPayload` | Object `{nodeID:String,expanded:Bool}` med ønsket ny tilstand | KEYPATH-MANGLER:visibleRows[].expansionPayload |
| `mode` | String subtree/node i scopeControlRows; lokal visibility, aldri root-condition | KEYPATH-MANGLER:scopeControlRows[].mode |

Lokale oppslag, knappenes labelKeypath/payloadKeypath og VStack som listemal er påvist i `CellProtocol/Sources/CellBase/Skeleton/SkeletonDescription.swift:1464`, `:1752`; web-radkontekst i `CellScaffold/Public/js/skeleton-runtime.js:5854`, `:6380`. At feltet `title` finnes på eksisterende helperRows gjør ikke det nye visibleRows-feltet eksisterende. Alle radbetingelser bruker scope:item; root-problemet er beskrevet i `CellProtocol/Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift:23` og appens evaluering i `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:1095`.

Data som trengs for det foreslåtte Tree-elementet, men **ikke er bundet i dagens kandidat**: node-ID, parentID, semantisk level, leadingInset, expanded, selectedNodeID, referert verktøy/celle/chat og event-/ruteopphav. Disse er nye kontraktkrav, KEYPATH-MANGLER:helperTree.nodeModel. For eksempel må to instansnoder kunne referere samme verktøy uten å få samme node-ID. Kravet kommer fra `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/FORMAALSSPEC.md:60`; ingen publisert Explore-shape for forslaget er påvist.

Eksisterende kontrakter som **ikke** brukes som erstatning:

| finnes i origin/main | hvorfor det ikke er trekontrakten | kilde |
|---|---|---|
| `chatHub.state.ui.helpers`, `activeHelper`, `chatHub.ui.setActiveHelper` | Flate verktøytyper; action setter activeTab mer og activeMoreTab verktoy, ikke skop. | `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift:2666`; `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:1070`, `:1282`, `:3133` |
| `chatHub.state.threads` | Chattråder finnes, men ingen parent-egenskap i den leste Thread-modellen; ikke hjelperinstanshierarkiet. | `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift:1532`; `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:146`, `:2483` |
| `chatHub.state.ui.showStarters`, `promptMessageCount` | Tomhet/teller for promptMessages; verken treets rotbarn eller antall meldinger i valgt undertre. | `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift:3880`; `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:1227`, `:1237` |

Live Explore ble ikke hentet (ingen nettverk), og en manifestvalidering av de nye bindingene er ikke utført. Før preview med meningsfulle innholdsasserts må neste tråd levere eller hente en godkjent testkontrakt/fixture med disse feltene. `CellProtocolDocuments/Tools/Explore/skeleton_explore_validator.py:640` krever operasjonsgrunnlag fra manifest; en kildekodelesning eller tom rapport kan ikke erstatte dette.
