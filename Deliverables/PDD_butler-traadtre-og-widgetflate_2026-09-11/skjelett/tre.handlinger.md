**Tre: handlinger personen må kunne ta**

Dette er akseptansekontrakten for videre reachability og faktiske brukerprøver. Alle `chatHub.ui.helperTree.*`-navn er foreslått og mangler i dagens fabrikk; se `tre.keypaths.md`. De skal ikke omtales som fungerende bare fordi Button dekodes. Grunnlag: `CellProtocolDocuments/Deliverables/PDD_butler-traadtre-og-widgetflate_2026-09-11/FORMAALSSPEC.md:60`, `:63`, `:66`, `:69`.

| personens handling | action-keypath / payload | kandidat nå | akseptanse etter implementering |
|---|---|---|---|
| Velg Butler-roten eller en annen node | `chatHub.ui.helperTree.selectNode`, `{nodeID}` fra selectionPayload | Button på tittelen, ikke hele raden | Valgt ID, markør, skopfot og loggutvalg oppdateres samlet; modus beholdes. |
| Velg «Undertre» | `chatHub.ui.helperTree.setScopeMode`, `{mode:"subtree"}` | Button i scopeControlRows | Noden og alle transitive etterkommere inngår, uavhengig av hva som er visuelt foldet inn. |
| Velg «Bare denne» | Samme action, `{mode:"node"}` | Button i scopeControlRows | Bare valgt nodes meldinger; bytte tilbake gjenoppretter utvalget uten tap. |
| Brett ut en node | `chatHub.ui.helperTree.setExpanded`, `{nodeID,expanded:true}` | Disclosure-Button når hasChildren | Barn blir synlige; valgt skop og loggutvalg endres ikke. Ingen dobbelt selectNode. |
| Brett inn en node | Samme action, `{nodeID,expanded:false}` | Samme Button med cellelevert expansionPayload | Underliggende synlige rader fjernes; fokus flyttes til forelder ved behov, valgt skop bevares. |
| Åpne treet i app-bredde | `chatHub.ui.helperTree.open`, `{}` | «Tråder»-Button er synlig i begge kandidatviewports; innhold åpnes ikke av kandidaten | Samme tre/valg/utbretting i kompakt drawer. Fokus inn i treet. |
| Lukk kompakt tre med kontroll, Escape eller backdrop hvis valgt | `chatHub.ui.helperTree.close`, `{}` (**mangler**, ikke i JSON) | Ikke tilbudt; drawer ikke beskrevet i kandidaten | Lukk uten skopendring og gi fokus tilbake til «Tråder». Hvilken åpen-geometri/backdrop som skal brukes er ukjent. |
| Flytt fokus med opp/ned/Home/End | Ingen celle-action; lokalt rendererfokus | Ikke implementert av kandidaten/List | Riktig synlig node, rulles inn i synsfeltet; ingen logg-/skopendring. |
| Venstre/høyre på trenode | setExpanded ved ut-/innbretting, ellers ingen action ved fokusflytting | Bare knappeklikk finnes | Følger trekontrakten i rapporten; stabile ID-er ved live innsetting. |
| Enter/Space på fokusert node | selectNode, `{nodeID}` | Tittel-Button kan aktiveres, men ingen samlet trefokusmodell | Samme virkning som radklikk, ett actionkall. |
| Se at en hjelper avslo og Butler overtok | Ingen action nødvendig for selve treets markering | tone/kindSummary-binding | Oransje og «gren · avslo», valgt ID bevares. Lenker for rute/tilgang ligger i chatdelen og er utenfor denne jobben. |
| Se ny godkjent hjelper i treet | Ingen ekstra tre-action: oppdaterte visibleRows | Ny rad hvis cellen leverer kjent visualDepth | Innsetting med stabil forelder, ingen tap av valg/fokus. Godkjenning av forslag tilhører A4s celle-/chatflyt, ikke en oppfunnet knapp i rail. |

Foreslått reachability-mål for kandidatens deklarerte actions er `{selectNode,setScopeMode,setExpanded,open}` med prefikset `chatHub.ui.helperTree.`. Fire unike keypaths finnes i JSON; mange radvarianter gir ikke flere domenehandlinger. `close` må tilføyes når kompakt tre faktisk beskrives. **Ingen SkeletonReachabilityAudit er kjørt.** Node-validatorens statiske opptelling er bare ekstraksjon.

Dagens audit henter Button.keypath og List-selection/activation, men ikke presentation.closeActionKeypath. Den vet heller ikke om visibleRows/scopeControlRows er tomme eller om actionen lykkes. Kilder: `CellProtocol/Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift:79`, `:138`, `:315`. En senere godkjenning må derfor kombinere audit med faktisk radtilstedeværelse, tastatur, action-resultat og endret skop-/loggdata; statisk keypath-dekning er ikke aksept.

Web sender Button-action fra click i `CellScaffold/Public/js/skeleton-runtime.js:1233`, og Porthole kobler den til runAction i `CellScaffold/Public/js/porthole-webo.js:7954`. Appen rendrer en vanlig Button i `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:1771`. Det bekrefter transporten av handling, ikke at de foreslåtte målkeypathene finnes. Dagens setActiveHelper åpner en verktøyfane og kan ikke brukes som selectNode (`origin/main`, `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:3133`).
