# P1/P3 — uavhengig kilde- og sikkerhetslesing

Dato: 2026-10-13. Leser: Codex-subagent `project_context_security_reader`.

Lesingen ble fullført mot rent CellScaffold-tre på `3a6680446e55fc1644afb368ac2bf48dd0720e30`, i det isolerte prosjektarbeidstreet `project-workspace-20261013/CellScaffold`. Ingen kildefiler ble endret, tester kjørt eller køhandlinger utført. Denne rapporten er lagring av den ferdige rapporten sendt til parent; lagringen utvider ikke lesingen eller omfanget.

G2-grunnlaget er `CellProtocolDocuments/Deliverables/PDD_project-workspace_2026-10-12/PLAN.md` og `CellProtocolDocuments/Deliverables/PDD_project-workspace_2026-10-12/contract/project-workspace-v1.json`. Godkjenningen er registrert separat; historisk ventetekst i originalplanen er ikke en ny port. Alle kildestier nedenfor er relative til HAVEN-roten og viser linjer ved ovennevnte revisjon.

## Konklusjon

P1 må isolere **konfigurasjonen, prosjektkonteksten og projeksjonen per visning**. Å flytte `selectedProjectID` til en HTTP-session alene løser ikke problemet.

### 1. To faner deler allerede samme Porthole

`WebCellEmbeddings` løser identity-unique `cell:///Porthole`; egne WebSocket-tilkoblinger gjenbruker samme `controlCell`. HTTP bruker cookie/session eller `user.cellId`, uten visnings-ID. `addConfiguration` skriver dermed til samme Orchestrator som begge faner bootstrapper fra.

Kilder:
- `CellScaffold/Sources/App/Cells/interface/WebCellEmbeddings.swift:58`
- `CellScaffold/Sources/App/Cells/interface/WebCellEmbeddings.swift:83`
- `CellScaffold/Sources/App/Controllers/VaporBrowserhead.swift:517`
- `CellScaffold/Sources/App/Controllers/PortholeWebSessionSupport.swift:4880`

### 2. Dagens prosjektåpning krever skriverett og muterer ved lesing

Discovery legger bare `projectSelection` i payload når `setStatus` er tillatt. Åpneruten laster konfigurasjonen og kaller deretter `projectPortfolio.select`. Denne skriver persistert global valgt-ID, øker `stateVersion` og sender mutasjon. Leseren får derfor ikke sitt prosjekt valgt.

Kilder:
- `CellScaffold/Sources/App/Cells/WorkbenchAccess/WorkbenchAccessGrantCell.swift:571`
- `CellScaffold/Sources/App/Cells/WorkbenchAccess/WorkbenchAccessGrantCell.swift:593`
- `CellScaffold/Sources/App/Controllers/PortholeWebSessionSupport.swift:3509`
- `CellScaffold/Sources/App/Controllers/PortholeWebSessionSupport.swift:5497`
- `CellScaffold/Sources/App/Cells/WorkItems/ProjectPortfolioCell.swift:1292`

### 3. Bootstrap eksponerer brede kildeprojeksjoner

`bootstrapProjectionState` leser alltid `state` først, uavhengig av hvilke bladfelter Skeleton trenger. Å referere Portfolio/WorkItem/Graph direkte og filtrere i nettleseren er derfor ikke en sikker prosjektprojeksjon. Portfolio `state` inneholder alle prosjekter/tellinger, og valgt prosjekt faller tilbake til første post.

Kilder:
- `CellScaffold/Sources/App/Controllers/PortholeWebSessionSupport.swift:1504`
- `CellScaffold/Sources/App/Cells/WorkItems/ProjectPortfolioCell.swift:1960`

### 4. Revokering må overstyre klientens optimistiske lagring

`preserveRecentCellActionStatesDuringRefresh` kopierer gammel label-state over bootstrap når en handling er nyere etter lokal sekvens. Den vurderer ikke tilgangsavslag. En refresh startet før en handling kan derfor få sitt autoritative avslag overskrevet av tidligere private data. Component-rendereren gjenoppretter også felter/fokus ved definisjonsbytte. Dette er en konkret grense den nye flaten må håndtere, ikke bare ved å skjule knapper.

Kilder:
- `CellScaffold/Public/js/porthole-webo.js:2878`
- `CellScaffold/Public/js/porthole-webo.js:2912`
- `CellScaffold/Public/js/skeleton-runtime.js:1105`

### 5. Mount-ruting finnes, men gir verken prosjektbinding eller autoritet

`ComponentActionMount(instanceID, componentID, revision)` går separat fra brukerpayload via TaskLocal. Mounted actions bruker faktisk autentisert HTTP-requester og ordinær Resolver/get/set. Remote bridge og WS mount-handlinger avvises eksplisitt. Metadata valideres for form, men er ikke knyttet til en serverregistrert visning/prosjektbinding. Ny prosjektkode må gjøre denne bindingen selv.

Kilder:
- `CellScaffold/Sources/ScaffoldKit/ComponentActionContext.swift:4`
- `CellScaffold/Sources/App/Controllers/VaporBrowserhead.swift:396`
- `CellScaffold/Sources/App/Controllers/PortholeWebSessionSupport.swift:3327`
- `CellScaffold/Sources/App/Cells/interface/WebCellEmbeddings.swift:284`

## Foreslått minste sammenhengende implementeringsrekkefølge innen P1/P3

1. Innfør typed `ProjectWorkspaceContext` og visningsregister med nøkkel som inkluderer **bevist requester-binding**, `sessionID`, `viewInstanceID` og valgfri `mountID`. Verdien inneholder konkret `portfolioUUID`, eksakt `projectID`, konfigurasjons-/returkontekst og tilgangsgenerasjon. Nøkkelen må ikke være bare UUID eller client-supplied mount-ID. Valgt tab/node er lokal, ikke kildeobjektets tilstand.

2. Før view-konteksten gjennom **både** bootstrap, action og eventabonnement. I dagens webklient går bootstrap og handlinger over HTTP, mens WS varsler refresh: `CellScaffold/Public/js/porthole-webo.js:10108`. Et tab-lokalt view-ID må overleve refresh; det gir ingen rettigheter. Åpning av nytt prosjekt må enten velge en view-lokal transient Orchestrator eller en eksplisitt view-lokal konfigurasjons-/projeksjonsgren. Den må aldri skrive den delte legacy-Orchestratorens konfigurasjon ved prosjektåpning.

3. Lag en egen autorisert prosjektprojeksjon som Skeleton refererer. Løs konkret Portfolio-UUID gjennom Resolver som faktisk requester, les via eksisterende `get("projects", requester:)`, match eksakt prosjekt-ID og returner ingen fallback. Senere WorkItem/idea/graph/job-kilder autoriseres uavhengig før objekter, relasjoner, etiketter, søk eller tellinger inkluderes. Returner `partial/unavailable` for manglende kilde, ikke null som implisitt null antall.

4. Gjenbruk de eksisterende gode kontrollene: `accessibleProjects` gjør requester-signaturkontroll, konkret UUID-oppslag, eierbinding og kontroll av aktuelle delinger; `grantedTarget` og `acceptedTargetLookupIdentity` beholder mottakeren som requester. Ikke gå gjennom utility-/owner-dispatch for ny prosjektprojeksjon.

   Kilder:
   - `CellScaffold/Sources/App/Cells/WorkbenchAccess/WorkbenchAccessGrantCell.swift:456`
   - `CellScaffold/Sources/App/Cells/WorkbenchAccess/WorkbenchAccessGrantCell.swift:751`
   - `CellScaffold/Sources/App/Controllers/PortholeWebSessionSupport.swift:682`

   Merk begrensningen: eksisterende deling gir brede Portfolio-nøkler (`state/projects/...`), **ikke et per-project grant**. Det er etablert Portfolio-autoritet, ikke bevis for ny prosjektavgrenset jobbkontroll. Prosjektkoblingen må fortsatt sjekkes, og P5 trenger sin egen eksplisitte prosjektbundne kommandokontrakt. Grantnøkler: `CellScaffold/Sources/App/Cells/WorkbenchAccess/WorkbenchAccessGrantCell.swift:1822`.

5. Legg til den nye åpnepayloaden additivt, og la begge nye Åpne-innganger bruke samme prosjektåpner. Bevar gammel `projectSelection`/`select` for eksisterende konsumenter/tester. Nye felt som `projectWorkspacePayload` kan gjøre dette uten å endre kontrakten som committed tester eksplisitt forventer. Delvis prosjektlesing må heller ikke blokkeres av at en helt annen delt Workbench-kilde er utilgjengelig; dette skiller seg fra dagens whole-Workbench `launchAvailable`.

6. Gi historikk egen prosjektidentitet: dagens navigation-ID er kun konfigurasjons-UUID eller endpoint+navn, og `currentConfigurationNavigationEntry()` rekonstruerer fra konfigurasjonen uten valgt prosjekt. Historikken må inkludere konkret prosjektkontekst og returreferanse; to prosjekter i samme konfigurasjon skal ikke dedupliseres.

   Kilder:
   - `CellScaffold/Public/js/porthole-webo.js:4149`
   - `CellScaffold/Public/js/porthole-webo.js:4201`

7. På revokering: øk tilgangsgenerasjonen, kanseller abonnement, avvis forsinket publikasjon fra tidligere generasjon og tøm snapshot, søk, tellinger, graf, remembered fields og mount-state. Gjør sluttkontroll etter await før publisering. P2s sekvens/cursor kan bygges på dette; gamle WS-refreshsignaler eller Flow-grants er ikke i seg selv autorisert prosjekt-eventlevering.

## Nye tester — forslag, ikke skrevet eller kjørt

Konkrete nye tester bør opprettes i nye filer; ingen eksisterende test trenger redigering for første additive leveranse:

- `ProjectWorkspaceIsolationTests`: samme ekte Portfolio med to prosjekter/to views, samme navn/ulike ID-er, samme prosjekt-ID/ulike Portfolio-UUID-er, refresh/back, leser uten `select`, uendrede persisted bytes/stateVersion/eventlog etter åpning.
- `ProjectWorkspaceAuthorizationTests`: ny requester, samme UUID/feil nøkkel, manipulert Portfolio, ukjent prosjekt/formål, utløpt/tilbakekalt deling; ingen private etiketter/tellinger/søketreff; revoke under suspendert kildeget og før publication.
- `ProjectWorkspaceMountTests`: to mounts på samme kilde, to requestere med identisk client view/mount-ID, payload kan ikke bytte registrert project scope; mounted read/get beholder TaskLocal separat.
- `ProjectWorkspaceOpenTests`: **ekte** `ConfigurationCatalogCell.projectPortfolioConfiguration()` og Developer Workbench Skeleton; ikke `Text("Portfolio")`-substituttet i `CellScaffold/Tests/AppTests/WorkbenchAccessGrantConfigurationTests.swift:1570`.
- Ny JS-fil for refresh/back/view-kontekst og revokering etter action; nytt browser-scenario med to reelle faner og to ComponentSurface-mounts.

Gjenbruk fixturemønsteret i `CellScaffold/Tests/AppTests/PortholeComponentSourceActionTests.swift:25`: ekte signerte Agreements, ikke agreementTemplate alene. Discoverytestene er nyttig baseline, særlig kontrakttilbaketrekking i `CellScaffold/Tests/AppTests/WorkbenchAccessGrantConfigurationTests.swift:1817`. Fixture-metodene er private, så et nytt testoppsett må lages uten å endre committed testfiler.

## Begrensninger og læring til parent

Dette dekker grunnlaget for P1/P3, ikke fullfører P2/P4/P5/P6. Jobbkontroll, graf-/kildetilgang, native Binding-paritet og hendelsesbevis gjenstår akkurat som godkjent. Kildegjennomgangen er ikke runtime-/deploybevis. Ingen tester ble kjørt av denne leseren.

Gjenbrukbar læring til parentens obligatoriske capture: **egen WebSocket-tilkobling betyr ikke egen visningstilstand når OrchestratorCell fortsatt er delt; tilbakekalling må dessuten vinne over optimistisk state-merge.** Ingen skill-endring inngår i denne rapportleveransen.
