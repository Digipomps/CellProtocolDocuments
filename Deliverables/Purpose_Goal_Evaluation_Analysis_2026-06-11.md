# Purpose / Goal Evaluation Analysis

Dato: 2026-06-11

Status: analyse, anbefalt implementasjonsplan og første implementasjonssteg.
Dette er ikke en ferdig kanonisk protokollspesifikasjon.

## Implementeringsstatus 2026-06-11

Første v1-steg er implementert i `CellProtocol`:

- `Sources/CellBase/PurposeAndInterest/GoalDefinition.swift`
  - `GoalDefinition`
  - `GoalEvaluation`
  - evidence sources, predicates, toleranser, status policy, helper-celler og
    privacy policy
  - bridge fra eksisterende PerspectiveGoal-lignende felter
- `Sources/CellBase/PurposeAndInterest/GoalEvaluationEngine.swift`
  - sideeffektfri, deterministisk evaluering av `GoalDefinition` mot eksplisitte
    `GoalObservation`-verdier
  - støtter nå composite all/any, semantic labels, human confirmation events,
    value predicates og network ping-status
- `Sources/CellBase/Cells/Purpose/GoalEvaluationCell.swift`
  - `GeneralCell`-adapter over den rene evalueringsmotoren
  - kontrakter:
    - `goal.state`
    - `goal.definition.current`
    - `goal.observations.current`
    - `goal.lastEvaluation`
    - `goal.definition`
    - `goal.observations`
    - `goal.evaluate`
    - `goal.reset`
  - emitter `goal.evaluation.updated`, og `goal.satisfied` når evalueringen
    faktisk tilfredsstiller målet
- Tester:
  - `Tests/CellBaseTests/GoalDefinitionTests.swift`
  - `Tests/CellBaseTests/GoalEvaluationEngineTests.swift`
  - `Tests/CellBaseTests/GoalEvaluationCellTests.swift`

Verifisering kjørt i `CellProtocol`:

- `swift test --filter 'GoalDefinitionTests|GoalEvaluationEngineTests|PurposeGoalLintTests|PerspectiveCellContractTests|PerspectiveSchemaTests'`
  - 17 tester, 0 feil
- `swift test --filter 'GoalDefinitionTests|GoalEvaluationEngineTests|GoalEvaluationCellTests|PurposeGoalLintTests|PerspectiveCellContractTests|PerspectiveSchemaTests'`
  - 20 tester, 0 feil
- `swift test`
  - 481 tester, 0 feil

Viktig avgrensning: dette kobler ennå ikke til ekte GPS, native klokke,
nettverk eller Porthole GUI. `GoalEvaluationCell` er en live `GeneralCell`, men
den evaluerer bare eksplisitt innsendte observasjoner. Det holder v1 fri for
gjetting og skjulte profiler.

## Kort konklusjon

HAVEN har allerede et sterkt konseptuelt grunnlag for Purpose og Goal, men
Goal finnes i tre delvis overlappende former:

1. `Purpose.goal` i CellBase peker til en `CellConfiguration`.
2. commons-perspektivskjemaet har målbare felter som `metric`, `target`,
   `timeframe`, `data_source` og `evidence_rule`.
3. `PurposeDecomposition` i CellScaffold har `PurposeGoalRequirement` med
   `outcome`, `successSignal`, `verification` og `measurable`.

Det som mangler er et felles runtime-kontraktobjekt for:

- hva som skal måles,
- hvilken celle eller hendelsesstrøm som er autoritativ evidens,
- hvilken toleranse/ferskhet som gjelder,
- hvilke statuser som finnes før, under og etter måloppnåelse,
- hvilke hjelpe-celler som kan analysere eller reparere situasjonen.

Anbefalingen er å innføre `GoalDefinition` og `GoalEvaluation` som små,
portable CellBase-modeller først, og så lage diskrete evaluator-celler for
sted, tid, nettverk, human confirmation, contract/probe-resultater og
generelle keypath/event-predikater.

## Kilder sjekket

Lokale autoritative kilder:

- `Book/09_Purpose_Interests.md`
- `Book/14_Perspective_Runtime_Matching.md`
- `CellScaffold/Documentation/PerspectiveCell_Runtime_Context.md`
- `CellProtocol/Sources/CellBase/PurposeAndInterest/Purpose.swift`
- `CellProtocol/Sources/CellBase/PurposeAndInterest/Goal.swift`
- `CellProtocol/commons/schemas/haven.perspective/Sources/HavenPerspectiveSchemas/PerspectiveSchema.swift`
- `CellScaffold/Sources/App/Support/PurposeDecomposition.swift`
- `CellScaffold/Sources/App/Cells/Perspective/PerspectiveCell.swift`
- `CellScaffold/Tests/AppTests/PerspectiveCellTests.swift`
- `CellProtocol/Tests/HavenCommonsTests/PerspectiveSchemaTests.swift`

Ekstern kilde sjekket 2026-06-11:

- W3C Geolocation Candidate Recommendation Snapshot, 2026-03-26,
  `https://www.w3.org/TR/geolocation/`. Relevant fordi den beskriver at
  posisjon har `latitude`, `longitude`, `accuracy`, tidsstempel, permission,
  `getCurrentPosition`, `watchPosition`, `maximumAge`, `timeout`, og sterke
  privacy-krav for lokasjonsdata.

## Hva vi har definert til nå

### 1. Konseptet i Book 09

Book 09 sier at en Purpose er deklarert intensjon, og at Goals skal definere
målbar suksess. Eksemplene er allerede i riktig retning:

- naa waypoint innen toleranse
- fjern skadelig melding
- fullfør treningsmodul
- valider datasettoppdatering
- synkroniser delt dokument

Dette er presist nok som filosofi, men ikke nok som runtime-kontrakt. Det sier
ikke hvordan man evaluerer, hvor ofte, hvilke statuser som finnes, eller hvilke
data som er autoritative.

### 2. CellBase `Purpose`

`Purpose` har:

- `goal: CellConfiguration?`
- `helperCells: [CellConfiguration]`

Dette er viktig: Goal var opprinnelig tenkt som noe en egen celle kan løse, ikke
bare tekst. Det passer veldig godt med ideen om at ett formål kan ha et mål og
hjelpere som kan reparere situasjonen.

Svakheten er at `CellConfiguration` alene ikke beskriver:

- evalueringsstatus,
- evidens,
- toleranse,
- trigger-policy,
- om målet er engangs, kontinuerlig eller venter på menneske,
- hvordan andre celler skal abonnere på endringer.

### 3. CellBase `Goal`

`Goal.swift` er foreløpig et tidlig skall. Kommentaren der er likevel den beste
arkitektursetningen vi har:

- Goals må ha en maskinløselig måte å avgjøre om de er løst.
- Noen mål kan være å få et menneske til å trykke på en knapp.
- Vi bør skille mellom kontinuerlige mål og mål med definitiv slutt.

Dette bør løftes til førsteordens kontrakt.

### 4. commons `PerspectiveDocument`

`PerspectiveGoal` har allerede:

- `goal_id`
- `purpose_id`
- `description`
- `metric`
- `baseline`
- `target`
- `timeframe`
- `data_source`
- `evidence_rule`
- `indicator_refs`
- `incentive_only`

Dette er det beste eksisterende dataspråket for mål. Det mangler bare runtime-
feltene: evaluator, statusmodell, evidence-freshness, toleranse og events.

Eksemplene i `commons/examples/perspectives` viser gode menneskelige mål, men
flere `data_source` peker til interesser i perspektivet. Det er bra for plan,
men for faktisk måloppnåelse må `data_source` ofte peke til en tilstand eller
hendelse som kan observeres:

- lokasjonssnapshot,
- tidsslot,
- ping-resultat,
- response-count,
- publiseringsstatus,
- contract-probe-artifact,
- menneskelig bekreftelses-event.

### 5. CellScaffold `PurposeDecomposition`

`PurposeDecomposition` har `PurposeNode` og `PurposeGoalRequirement`.
Spørreundersøkelse-dekomponeringen dekker allerede:

- respondent-skjema,
- admin authoring,
- mottaker/samtykke/utsending,
- responsinnsamling,
- lese/eksportere/analysere svar,
- GUI-kvalitet,
- tilgang/audit,
- acceptance tests,
- preference context,
- source methodology.

Dette er riktig formålsdekomponering. Neste steg er at hvert node-goal bør kunne
uttrykkes som en faktisk `GoalDefinition`, ikke bare tekstlig `successSignal`.

### 6. CellScaffold `PerspectiveCell`

Scaffold-versjonen av `PerspectiveCell` har allerede:

- `perspective.applyEvent`
- `perspective.reconfigureForEvent`
- `perspective.setLifecycleSegment`
- `perspective.configureScaffoldContext`
- lifecycle-segmenter som `home_breakfast`, `commute_work`, `work_focus`,
  `lunch`, `evening_home`, `conference_participant`

Den kan reagere på eventer og endre aktive formål/interesser. Den evaluerer
ikke ennå om de aktive formålene har møtt sine Goals.

Det er riktig rollefordeling:

- context/event-celler observerer verden,
- Perspective vekter formål,
- Goal-evaluator avgjør oppnåelse,
- helper-celler foreslår eller utfører tiltak innen eksplisitte grants.

## Foreslått felles kontrakt

### `GoalDefinition`

Minimum v1:

```json
{
  "schema": "haven.goal-definition.v1",
  "goalID": "goal.personal.location.work-at-lunch",
  "purposeRef": "purpose://personal.be-at-work-for-lunch",
  "title": "Be at work during lunch",
  "description": "Satisfied when the represented person is within their owner-defined Work semantic location during their owner-defined lunch time window.",
  "lifecycle": "continuous",
  "evaluatorKind": "composite",
  "evidenceSources": [
    {
      "sourceID": "semantic-location",
      "endpoint": "cell:///SemanticLocation",
      "keypath": "semanticLocation.state.currentLabels",
      "requiredGrant": "location.semantic.read",
      "freshnessSeconds": 300
    },
    {
      "sourceID": "semantic-time",
      "endpoint": "cell:///SemanticTime",
      "keypath": "semanticTime.state.currentLabels",
      "requiredGrant": "time.semantic.read",
      "freshnessSeconds": 60
    }
  ],
  "predicate": {
    "all": [
      {"sourceID": "semantic-location", "containsLabel": "work"},
      {"sourceID": "semantic-time", "containsLabel": "lunch"}
    ]
  },
  "tolerance": {
    "locationAccuracyMeters": 100,
    "timeSkewSeconds": 300
  },
  "statusPolicy": {
    "approachingWindowSeconds": 900,
    "missedAfterSeconds": 1800
  },
  "helperCells": [
    {
      "endpoint": "cell:///Perspective",
      "purposeRef": "purpose://personal.context.reweight"
    }
  ],
  "privacy": {
    "rawEvidenceVisibility": "owner-only",
    "publishableStatus": ["unknown", "approaching", "satisfied", "missed"],
    "doNotExportRawLocation": true
  }
}
```

### `GoalEvaluation`

Minimum v1:

```json
{
  "schema": "haven.goal-evaluation.v1",
  "goalID": "goal.personal.location.work-at-lunch",
  "purposeRef": "purpose://personal.be-at-work-for-lunch",
  "status": "satisfied",
  "progress": 1.0,
  "confidence": 0.93,
  "evaluatedAt": "2026-06-11T10:59:00Z",
  "evidence": [
    {
      "sourceID": "semantic-location",
      "status": "fresh",
      "summary": "Inside owner-defined Work label.",
      "observedAt": "2026-06-11T10:58:40Z"
    },
    {
      "sourceID": "semantic-time",
      "status": "fresh",
      "summary": "Inside owner-defined lunch time.",
      "observedAt": "2026-06-11T10:59:00Z"
    }
  ],
  "missing": [],
  "nextCheckAt": "2026-06-11T11:04:00Z",
  "emittedEvents": [
    "goal.satisfied",
    "perspective.context.changed"
  ]
}
```

Statusverdier bør være:

- `unknown`: mangler permission, evidens eller evaluator
- `not_started`: målperioden har ikke begynt
- `approaching`: målperioden eller terskelen nærmer seg
- `active`: målperioden er aktiv, men mål er ikke oppnådd ennå
- `satisfied`: målet er oppnådd
- `at_risk`: fortsatt mulig, men sannsynlig risiko
- `missed`: perioden er passert eller negativ terskel nådd
- `blocked`: policy/grant/permission gjør evaluering eller handling umulig
- `cancelled`: menneske eller policy stoppet målet

## Evalueringsklasser

### 1. State predicate

Brukes når målet kan sjekkes mot en keypath:

- `questionnaireCampaign.config.lifecycle.status == active`
- `publicPage.state.publicationStatus == published`
- `agent.setup.status.connected == true`

Trenger:

- endpoint,
- keypath,
- operator,
- expected value,
- freshness,
- grant.

### 2. Event predicate

Brukes når målet er oppnådd ved at en hendelse skjer:

- `message.sent`
- `questionnaire.response.submitted`
- `goal.confirmedByHuman`
- `contractProbe.completed`

Trenger:

- topic/event type,
- causation ID,
- allowed age,
- count eller sequence rule.

### 3. Location / geofence

Brukes for "være hjemme", "på jobb", "på Storsenteret".

Trenger minst to celler:

- `SemanticLocationCell`
  - eier-definerte labels: `home`, `work`, `storsenteret`
  - hver label kan ha ett eller flere områder
  - område har center/radius eller polygon, confidence og kilde
  - rå koordinater holdes owner-only
  - emitter `semantic.location.entered`, `approaching`, `exited`, `unknown`
- `LocationSignalCell` eller native bridge
  - henter rå posisjon med permission
  - leverer accuracy/timestamp
  - støtter stale/permission-denied/status

W3C Geolocation understøtter denne designen: posisjon har koordinater,
accuracy og timestamp; `watchPosition` kan gi løpende oppdateringer; permission
og privacy må håndteres eksplisitt. HAVEN bør derfor aldri la "Home" eller
"Work" være global profil; det må være owner-scoped semantic label over lokal
evidens.

### 4. Time window / semantic time

Brukes for "lunsjtid", "arbeidstid", "kveld", "helg".

Trenger:

- `SemanticTimeCell`
  - eier-definerte labels: `lunch`, `work_hours`, `evening`
  - kan være regler, kalenderankre eller lærte forslag som må bekreftes
  - emitter `semantic.time.approaching`, `active`, `ended`, `unknown`
- evaluator må bruke lokal timezone og eksplisitt datoperiode.

"Lunsjtid" bør ikke være en global sannhet. Den bør være en owner-scoped
label som kan bety 11:00-13:00 for én person, og 12:30-14:00 for en annen.

### 5. Human confirmation

Brukes når målet er "vente på at mennesket trykker".

Eksempler:

- godkjenn agent-handling,
- bekreft questionnaire-spørsmål,
- bekreft at et mål faktisk er oppnådd i den virkelige verden.

Trenger:

- `HumanConfirmationGoalCell`
  - oppretter en confirmation request
  - status `waiting_on_human`, `confirmed`, `declined`, `expired`
  - FlowElement med `goal.confirmed` eller `goal.declined`
  - UI kan være skeleton button, notification eller chat helper.

### 6. Network / scaffold contact

Brukes for "scaffoldet skal være i kontakt med resten av HAVEN".

Trenger:

- `NetworkReachabilityGoalCell`
  - endpoint eller remote `cell://host`
  - ping/health/readiness check
  - timeout og antall påfølgende feil/suksesser
  - status `satisfied`, `degraded`, `missed`, `blocked`
- helper-celler:
  - bridge diagnostics,
  - credential/identity repair,
  - MCP/agent bridge review,
  - deployment/rollback helper.

Goal kan være:

```json
{
  "goalID": "goal.scaffold.network.contact-haven",
  "purposeRef": "purpose://scaffold.maintain-haven-contact",
  "lifecycle": "continuous",
  "evaluatorKind": "networkPing",
  "target": {
    "endpoint": "cell://staging/health",
    "timeoutMilliseconds": 3000,
    "requiredConsecutiveSuccesses": 1,
    "maxConsecutiveFailures": 3
  },
  "statusPolicy": {
    "approachingAfterFailures": 1,
    "missedAfterFailures": 3
  },
  "helperCells": [
    {"endpoint": "cell:///BridgeDiagnostics"},
    {"endpoint": "cell:///AgentReview"},
    {"endpoint": "cell:///DeploymentStatus"}
  ]
}
```

### 7. Contract/probe and GUI

Brukes for formål som "GUI skal virke" eller "cellen er produksjonsklar".

Trenger:

- `ContractProbeCell` som evidence source
- Browser smoke/canary artifact som evidence source
- klare predicates:
  - alle forventede keypaths finnes,
  - alle knapper har action,
  - ingen testfeil,
  - ingen blocking accessibility/keyboard-feil,
  - ingen overlapp i relevante viewports.

## Mapping av eksisterende formål til Goal-behov

| Formålstype | Eksempel i repo | Hva Goal må kunne måle |
|---|---|---|
| Prompt til verktøy | `personal.chat.assist.resource-router` | Riktig capability valgt, ingen sideeffekt før brukerhandling, ingen duplikat/ambiguous match uten valg. |
| Spørreundersøkelse | `purpose://questionnaire.campaign.complete` | Admin kan sette opp, respondent kan svare med samtykke, responses lagres, export fungerer, GUI-smoke passerer. |
| GUI-kvalitet | `purpose://gui.quality.functional-accessible` | Browser/probe-resultat viser fungerende knapper/felt, fokus/keyboard, ingen overlapp. |
| Personlig lokasjon | `personal.mobility.commute`, planlagt `home/work/storsenteret` | SemanticLocation label er aktiv innen toleranse og ferskhet; raw GPS holdes privat. |
| Personlig tid | `lunch`, `evening_home`, `work_focus` | SemanticTime label er approaching/active/ended i lokal timezone. |
| Kombinert kontekst | "på jobb til lunsjtid" | Composite goal over semantic location + semantic time. |
| Nettverk/scaffold drift | `scaffold.cloud.background-orchestration`, agent/scaffold contact | Ping/health/readiness svarer innen timeout; konsekutive feil gir `at_risk`/`missed`. |
| Human approval | agent review, onboarding confirm, questionnaire confirm | Confirmation event fra riktig requester innen frist. |
| RAG/docs | `personal.chat.assist.rag-query`, `cellprotocol.docs.lookup` | Svar eller dokument åpnet med kilde, read-only, ingen private data lekket. |
| Public presence | `personal.public-presence.publish` | Publisert/unpublisert/delete-state er eksplisitt og verifiserbar. |
| Conference networking | `purpose.meet_relevant_people` | Antall kvalifiserte introer/møter/follow-up tråder når terskel. |
| Admin cleanup | `admin.cell-lifecycle.cleanup-review` | Dormant/orphaned cells identifisert, review fullført, ingen destruktiv handling uten confirmation. |

## Anbefalt implementasjonsrekkefølge

### P0: Samle kontrakten

Lag i CellBase:

- `GoalDefinition`
- `GoalEvidenceSource`
- `GoalPredicate`
- `GoalEvaluation`
- `GoalStatus`
- `GoalLifecycle`
- `GoalEvaluatorKind`

Legg kun til modeller og codable roundtrip-tester først. Ikke koble rå GPS,
nettverk eller GUI ennå.

Koble eksisterende konsepter slik:

- `PerspectiveGoal` kan eksporteres/importeres til `GoalDefinition`.
- `PurposeGoalRequirement` kan inkludere et valgfritt `goalDefinition`.
- `Purpose.goal: CellConfiguration?` beholdes som legacy/helper peker, men bør
  suppleres av `goalDefinitions`.

### P1: Sideeffektfri evaluator

Status: v1 implementert som `GoalEvaluationEngine` + `GoalEvaluationCell`.
Neste steg er å koble faktiske observasjonskilder til denne cellen.

`GoalEvaluationCell` har nå:

- `goal.evaluate`
- `goal.lastEvaluation`
- `goal.definition`
- `goal.definition.current`
- `goal.observations`
- `goal.observations.current`
- `goal.state`
- `goal.reset`

Watch-start/stop er ikke implementert ennå. V1 er bevisst pull/evaluate-basert,
slik at observasjoner må leveres eksplisitt.

V1 bør støtte:

- state predicate,
- event predicate,
- human confirmation,
- composite AND/OR over andre evaluations.

Implementert støtte: semantic label predicates, event predicates, value
predicates, human confirmation, network ping og composite all/any. Generell
state predicate mot eksterne cell-keypaths krever neste observasjonsbro.

Den skal returnere `GoalEvaluation` og emitte `goal.evaluation.updated`, men
ikke utføre remediation selv.

### P1: Semantic context cells

Lag små celler:

- `SemanticLocationCell`
- `SemanticTimeCell`
- `ContextEventBridgeCell`

Disse skal emitte owner-scoped context events som `PerspectiveCell` kan reagere
på. Rå sensorverdier skal ikke inn i Perspective. Perspective skal se labels og
status, ikke full GPS-logg.

### P1: Network watchdog

Lag `NetworkReachabilityGoalCell` for scaffold/HAVEN-contact:

- ping/health/readiness,
- consecutive failures,
- next check,
- helper suggestions.

Dette gir umiddelbar verdi for staging, MCP og multi-scaffold drift.

### P2: Decomposition output

Oppdater `grounding.decompose` slik at hver `PurposeNode.goal` også inneholder:

- `goalDefinition`,
- `evaluatorKind`,
- `evidenceSources`,
- `statusPolicy`.

Da kan et prompt som "lag en spørreundersøkelse" ikke bare gi en liste med
formål, men også en testbar plan for når hvert formål er oppnådd.

### P2: Goal UI / Workbench

Lag en liten `GoalWorkbenchCell`:

- viser aktive goals,
- status,
- evidens,
- mangler,
- helper-celler,
- "vent på menneske"-knapper,
- retry/evaluate now.

Dette blir nyttig både for mennesker som planlegger ferie og scaffolds som
drifter seg selv.

## Akseptansetester for v1

1. `GoalDefinition` roundtripper med location/time/network/human/composite.
2. `GoalEvaluationCell` evaluerer state predicate mot en testcelle.
3. `GoalEvaluationCell` evaluerer event predicate mot en synthetic FlowElement.
4. Human confirmation goal går fra `waiting_on_human` til `satisfied` når riktig
   requester trykker.
5. Semantic location test bruker syntetisk koordinat og eierlabel `work`; rå
   koordinat vises ikke i Perspective.
6. Semantic time test bruker fast klokke og label `lunch`.
7. Composite "work + lunch" blir `satisfied` bare når begge under-goals er
   `satisfied`.
8. Network goal blir `at_risk` etter første feil og `missed` etter tre
   konsekutive feil.
9. `PerspectiveCell` reagerer på `semantic.location.*` og `semantic.time.*`
   uten å lagre rå sensorhistorikk.
10. `grounding.decompose` for spørreundersøkelse returnerer goalDefinitions for
    alle obligatoriske nodes.

## Viktige designgrenser

- Purpose er ikke permission. Grants bestemmer fortsatt tilgang.
- GoalEvaluation er ikke sannhet om personen; det er en evaluering av et
  definert mål mot eksplisitte evidenskilder.
- Semantic labels som "hjemme", "jobb" og "lunsjtid" er owner-scoped og kan
  slettes/revideres.
- Raw location skal aldri være nødvendig for vanlig Perspective-matching.
- Helper-celler kan analysere og foreslå tiltak, men remediation må følge egne
  grants og confirmation-regler.
- `unknown` er en legitim status, ikke en feil som skal fylles med gjetning.

## Min anbefaling

Starten er nå gjort med kontraktsmodeller, tester, ren evaluator og
`GoalEvaluationCell` i `CellProtocol`, uten native GPS. Neste steg er synthetic
location/time/network fixtures. Først når kontrakten er stabil kobler vi
Binding/native lokasjon og staging network health inn som ekte evidenskilder.

Dette gir en ren bro fra:

- menneskelig formål: "jeg vil være på jobben til lunsjtid",
- til maskinmål: semantic location + semantic time innen toleranse,
- til event: `goal.satisfied`,
- til Perspective: reweight context,
- til helper-celler: analyser eller løs situasjonen hvis status blir `at_risk`
  eller `missed`.
