# Konsekvensanalyse — formålsdekomponeringen over på PerspectiveNode

Mappe: `Deliverables/PDD_mcp-tilgangsbevis_2026-09-12/` · 2026-09-12 · Losen · **Iterasjon 2 — validert uavhengig av Astra (Codex), `handoff/CODEX_REVIEW_PERSPECTIVENODE.md`**

Stier er relative til repo-rot (`HAVEN/`). Alt merket **retrieved** er lest i fil, med sti. `[Astra]` markerer funn fra Codex-gjennomgangen, med dens sti:linje. Det som ikke er lest står som `ukjent`. `[vurdering]` er mine.

---

## 0. Bestillingen, ordrett

> Du må - men hjelp av Codex og eventuelt rådgivere sjekke om vi bruker riktig formålsstrukturer - som er PerspectiveNode og gå igjennom all bruk av og dokumentasjon av formålsdekomponering og sjekke hvilke knsekvenser det vil ha å flytte det over og mitigere eventuelle negative konsekvenser. Har sett igjennom G1 og synes dette er bra så gå videre med det men gjør det med riktig formålsarkitektur.

### Kort svar

**Nei, metoden bruker ikke PerspectiveNode.** Formålsdrevet utvikling (PDD) har sin egen formålsmodell i JSON og Python, og den har funnet opp igjen ting CellBase allerede har — sist `composition` (Book 36, 2026-09-09), ni uker etter `PurposeComposition.swift` (25.06). Flyttingen er riktig og gjennomførbar.

**Men iterasjon 1 av denne analysen overdrev hvor mye som allerede finnes.** Astras gjennomgang holder referansekartet (`Purpose` er `PerspectiveNodeImpl`, `purposeRef` overlever via `nodeIdentifier`, composition-evaluatoren har tester) — og avviser *kompatibilitetsbeviset*: M1 slik den sto endrer composition-formatet Python krever; `human-confirmation` er et predikat, ikke en godkjenningsmekanisme; AIGateway-digesten binder ikke Book-JSON; og challenge-mekanismen som finnes er `AdmissionChallengePayload`/`connect.challenge` i tilkoblingsforløpet, ikke `GoalDefinition`. Tre steder sa iterasjon 1 «det er mekanismen som finnes» der det riktige er «byggesteinene finnes, integrasjonen gjør det ikke». Det er rettet under, og hvert sted er merket.

Det som gjenstår etter rettelsene: **en dokumentert semantisk bro** (to composition-modeller med ulik historikk-semantikk), **riktig kilde- og godkjenningsbinding** for porter og avdrift, og **koblingen fra et avvist keypath-steg til en løsbar challenge**.

---

## 1. Hva «riktig formålsarkitektur» faktisk er (lest i kode)

`CellProtocol/Sources/CellBase/PurposeAndInterest/` — 29 filer, 8 210 linjer — pluss to celler utenfor mappen som Astra fant.

| Byggeblokk | Fil | Hva den er |
|---|---|---|
| `PerspectiveNode` | `Protocols.swift:81` | Protokoll: `name`, `reference`, **åtte vektede relasjoner** — `types`, `subTypes`, `parts`, `partOf`, `interests`, `purposes`, `entities`, `states` |
| `PerspectiveNodeImpl` | `PerspectiveNode.swift:41` | Basisklassen. `nodeIdentifier` gir stabil identitet; `reference` faller tilbake på `name`. **Stubber, presist:** `get(keypath:)` splitter og går gjennom nøkkelstien men leser/returnerer ingenting (`:85`); `set(keypath:)` og `init(from:)` er tomme (`:94`, `:107`); `==` sammenligner bare type og navn — ignorerer relasjoner **og `nodeIdentifier`**, så to ulikt identifiserte noder med samme navn er «like» (`:112`) `[Astra]` |
| `Purpose` | `Purpose.swift:13` | `PerspectiveNodeImpl` + `goal: CellConfiguration?`, `helperCells: [CellConfiguration]`, `composition: PurposeComposition?`, `description`. **Har egen fungerende dekoder** (`:58`) — basisklassens tomme `init(from:)` brukes ikke. Relasjonene er typet `Weight<Purpose>` / `Weight<Interest>` / `Weight<EntityRepresentation>`. `PurposeReference { keypath }` |
| `Weight<T>` | `Weight.swift` | `weight`, `value` **eller** `reference`. Facilitator-kravet ligger i `Weight.encode` (`:105`), ikke i `Purpose.encode`; en Purpose med tomme relasjoner rundturer uten facilitator (`Tests/CellBaseTests/PurposeCompositionTests.swift:160`) `[Astra]` |
| `PurposeComposition` | `PurposeComposition.swift` | Uttrykkstre `purpose \| allOf \| anyOf \| sequence \| atLeast(requiredCount)`, kodet som `type/children/requiredCount` (`:109`). Evalueres mot `PurposeResolutionRecord{purposeRef, status ∈ started/succeeded/failed, resolvedAt, metadata}` (`Constraint.swift:13–36`) → `satisfied/partial/unsatisfied`, `score`, `blockingIndex/Reason`. **Blad velger siste *suksess*, ikke siste tilstand** (`:38`) — en nyere `failed` opphever ikke en eldre suksess `[Astra]` |
| `GoalDefinition` | `GoalDefinition.swift` | Schema `haven.goal-definition.v1`: `lifecycle`, `evaluatorKind` (10 verdier), `evidenceSources[]` (med `requiredGrant`, `visibility`), `predicate`, `statusPolicy`, `helperCells: [GoalHelperCellRef{endpoint, purposeRef, actionKeypath, title}]`, `privacy`. **Datafelt — ikke operative kontroller**, se `GoalEvaluationEngine` under |
| `GoalEvaluationEngine` | `GoalEvaluationEngine.swift` (313 l.) — **lest av Astra, ikke av meg** | Tar *innsendte* observasjoner, returnerer `GoalEvaluation`. Én særskilt gren: `network-ping` (`:140`, `:178`). Alt annet går gjennom én felles predikatsjekk med `all`, `any`, `contains-label`, `event-seen`, `value` (bare strenglikhet/ulikhet/`contains`), `network-ping` (`:150`, `:218`, `:263`). **Manglende eller ukjent predikat → `false` → `active`**, ikke `unknown` (`:247`). `contract-probe`, `gui-smoke`, `custom`, `semantic-*` har ingen egen dispatch. Manglende deklarert kilde → `unknown`; innsendt `denied/error` → `blocked`; `stale` → `unknown` (`:73`, `:95`, `:110`). `lifecycle`, `timeframe`, `freshnessSeconds`, `requiredGrant`, `visibility`, `helperCells` **brukes ikke av motoren** (`:66`, `:158`) `[Astra]` |
| `GoalEvaluationCell` | `CellProtocol/Sources/CellBase/Cells/Purpose/GoalEvaluationCell.swift:7` — **oversett i iterasjon 1** | GeneralCell-adapter: definition, observations, `goal.evaluate` (`:147`), lagrer siste evaluering, flow-emisjon (`:216`). Tar fortsatt inn eksplisitte observasjoner — henter ikke evidens selv. Registrering/utrulling `ukjent` `[Astra]` |
| `Goal: GeneralCell` | `Goal.swift` | Den eldre goal-cellen: `goalDefinitionString` («still undefined») |
| `Perspective` | `Perspective.swift` (1 084 l.) | Konteksten. `addPurpose` er **ikke** upsert — append til valgfri container uten oppdatering av referansedict (`:197`); `findPurposeByReference` leser dict (`:426`); `updateRelation` slår sammen uten slettesemantikk (`:880`); `loadContext` rekonstruerer arrays fra dict-verdier og **mister kildeordning** (`:666`); `setPurposeJsonData` dekoder *aktive* `[Weight<Purpose>]`, ikke en taksonomi (`:1074`); `buildPurposeList` bygger fra hardkodede navn (`:310`) `[Astra]` |
| `PerspectiveEntityProjection` | `PerspectiveEntityProjection.swift:23`, `applyEntityProjection :142` | «One cell's claim on a slice of the entity graph» — kilde, `epoch`, sett-semantikk med fjerning. Gjelder **bare entiteter**; ingen `PerspectivePurposeProjection` finnes `[Astra]` |
| `PurposeInterestAdjacencyIndex` | `PurposeInterestAdjacencyIndex.swift:25, :41, :61` | Vektet Interest → purposeRef-indeks med rangering. Lager ikke `Purpose`-objekter eller foreldrekanter. Ubrukt utenfor egen fil (REVISJON) |
| `WeightedGraphRuntime`, `Signal`, `MatchStrategyPlanner` | samme mappe | Matchemotoren. Traverserer eksisterende kanter etter vekt/toleranse/`maxHops`/tidsfrist (`WeightedGraphRuntime.swift:420`, `:441`, `:454`); betingelsesfilteret evaluerer `Interest`, ikke en `Purpose`s status (`:587`) |
| **Challenge-maskineriet** | `CellProtocol/Sources/CellBase/Agreement/AdmissionContracts.swift:47`, `Agreement/Condition/ConnectChallengeDescriptor.swift:8, :35` | **`AdmissionChallengePayload`** bærer Agreement, ConnectContext, issues, session og helperkonfigurasjon; `ConnectChallengeDescriptor` beskriver remediering. Utstedes i tilkoblingsforløpet: `attach` → `admit` (`GeneralCell.swift:542`), `signContract` evaluerer Agreement-betingelser (`:660`), uløste betingelser gir admission-session + `connect.challenge` (`:977`), `retryAdmissionSession` (`:569`). Native Porthole leser `connect.challenge` og viser alert med «Open helper» (`CellApple/.../PortholeViewModel.swift:544, :584`) `[Astra]` |

**Tre goal-representasjoner i CellBase** (`Goal: GeneralCell`, `Purpose.goal: CellConfiguration?`, `GoalDefinition`+`GoalEvaluationCell`), ikke forent. `GoalDefinition` er den best dokumenterte og den eneste med adapter og produksjonsbruk (`HavenAgentD::Sources/HavenAgentRuntime/NetworkHealthPurposeCatalog.swift`). Men `goal` og `helperCells` på `Purpose` er **separate felt og API-er** (`Purpose.swift:14`, `:110`, `:123`) — iterasjon 1 kalte `Purpose.goal` «egentlig en helper»; det var feil `[Astra]`.

---

## 2. Inventar — all bruk og dokumentasjon av formålsdekomponering

Fem representasjoner. R1–R4 fra `Deliverables/Formaal_Perspective_Signalmatching_Revisjon_2026-09-11/REVISJON.md`; **R5 er metoden selv**, ny her.

| # | Representasjon | Hvor | Form | PerspectiveNode? |
|---|---|---|---|---|
| R1 | `PurposeTaxonomy` + `PurposeDecompositionEngine` **og `PurposeKnowledgeBase`** | `CellScaffold/Sources/App/Support/PurposeDecomposition.swift` (3 464 l., `PurposeTaxonomy :119`), `CellScaffold/Sources/App/Support/PurposeKnowledgeBase.swift:92` `[Astra]` | 44 `purpose://`-strenger; **to** hardkodede Swift-kataloger, egne `PurposeNode`/`PurposeGoalRequirement` | **Nei** |
| R2 | Purpose Knowledge Base v0 | `Book/haven_purpose_knowledge_base_v0.json` (+ index, schema) | 57 noder; `rootPrinciple`, `compatibility.model = single-parent-tree-with-cross-cutting-facets`, `changePolicy`, `statusMeanings`, `matchingHints` (`:7`, `:17`, `:19`, `:53`) | Nei |
| R3 | `Purpose`/`Interest` som grafnoder | `CellProtocol/Sources/CellBase/PurposeAndInterest/` | §1. Fylt med demodata (`Purpose.swift:191–252`) | **Ja — arkitekturen** |
| R4 | `PalazzoSignal*` | `PalazzoScaffold/…` | egen signalmodell | Nei (`ukjent` utover REVISJON) |
| **R5** | **PDD-metoden** | under | JSON + Python + markdown | **Nei** |

### 2.1 R5 — metodens egne deler

| Del | Sti | Hva den antar om formålsstrukturen |
|---|---|---|
| Book 35 | `Book/35_Purpose_Driven_Development_Workflow.md` | §2.1 «purpose node» = R2-formen. §5: filer i git er sannheten — med revurderingstrigger «*or the method has moved into cells …the natural home is a HAVEN cell that owns the register*». Utløst av Kjetils ord |
| Book 36 | `Book/36_Purpose_Composition.md` | **Forslag, venter Kjetils ord.** `composition` på ikke-løvnode: `allOf / sequence / anyOf(min) / firstOf / invariant(over)`. Søkte aldri i CellBase |
| Malen | `Prompts/Purpose_Driven_Dev_Spec.md` | R2-form, én forelder |
| Skillen | `.claude/skills/haven-purpose-driven-dev/SKILL.md` (+ kopi i `Tools/PurposePackages/`) | Klassifisering over Book 23; `candidate`-noder bare i markdown |
| `purpose_dev.py` | `Tools/PurposePackages/purpose_dev.py` | `lookup` bruker **tre ulike mekanismer**: pakker via `alwaysAttach`/jokertegn/OR over tags+surfaces (`:226`, `:230`), lærdommer via `tags ∩` eller `purposeRefs ∩` (`:239`), KB leksikalsk (`:261`); `gates` returnerer 0/1/2/3 for `green/red/blocked/unverified` (`:479`); `validate` kan gi 0 med manglende composition som advarsel (`:166`) `[Astra]` |
| `purpose_composition.py` (+ test) | `Tools/PurposePackages/purpose_composition.py` | Book 36-validator og -evaluator: `kind/min/over` + `childOrder` på noden (`:85`, `:95`), `green/red/blocked/unverified`, kjøringslogg `attempts/measurements/reports/opinions` (`:113`, `:334`). Blad bruker **siste måling og siste forsøk** (`:205`); `blocked` propageres **før** disjunksjon (`:219`); `sequence` sjekker tilstand **før hvert forsøk** (`:288`); `firstOf` registrerer valgt gren (`:242`); `invariant` måles før/etter hvert steg (`:306`) `[Astra]` |
| Skjemaer | `Book/haven_purpose_{knowledge_base,packages,composition,composition_run}_v0.schema.json` | Fire skjemaer for R5-formene |
| Pakker | `Book/haven_purpose_packages_v0.json` | 5 pakker, 13 pakkeformål, `derivedTests{kind, how, evidence}` (`how`/`evidence` påkrevd, `purpose_dev.py:135`), `requiredArtifacts` per port (`:201`) |
| Lærdommer | `Book/haven_lessons_register_v0.json` | 45 poster `{symptom, cause, prevention, purposeRefs, tags, severity, source}` |
| Oppgavemapper | `Deliverables/PDD_*` | **22 mapper**, FORMAALSSPEC i R2-form |
| Indeks og evaluator | `Tools/PurposeKnowledge/*.mjs` (12) | `derive_purpose_index.mjs` antar **ett tre**: én `parentRef`, DFS fra `rootPurposeRef`, avviser noder som ikke nås, ingen sykkelvern, bitposisjoner etter input-ordning, hasher rå `sourceText` (`:8`, `:27`, `:33`, `:53`, `:66`, `:167`, `:188`) `[Astra]` |

### 2.2 Konsumenter som berøres — med faktiske kallsteder `[Astra]`

| Konsument | Kallsted | Hva som må bevares |
|---|---|---|
| `ExecutablePurposeGroundingCell` | `decompose` → `assistedDecompose` (`CellScaffold/Sources/App/Cells/PersonalCopilot/ExecutablePurposeGroundingCell.swift:133`, `:200`); `resolveTaxonomy` (`:137`, `:206`); `resolvePurposeKnowledge` (`:141`, `:210`) → **`PurposeKnowledgeBase`**, ikke `PurposeTaxonomy`; `purposeContextPack` (`:145`, `:214`) | Samme refs, maler og responssemantikk (én foreldrekjede, fasetter, katalogmodell). Rå graf-JSON er ikke samme respons. Å endre `PurposeTaxonomy` oppdaterer **ikke** `PurposeKnowledgeBase` |
| `assistedDecompose` internt | `PurposeDecomposition.swift:685`, `:730`, `:2976` | Ruting hardkodet (spørreskjema/prosjekt/rådgivning/kapabilitet); modellforslag avgrenses til mal-ID-er. Grafgenerert katalog erstatter ikke logikken |
| `CellProtocolClient` | `resolvePurpose` (`purpose.knowledge.resolve`), `purposeContextPack` (`purpose.context.pack`) — `CellScaffold/Sources/ScaffoldKit/CellProtocolClient.swift:157`, `:169`, `:178` | Offentlige kontrakter; status/top/expanded/LCA |
| Capability-broker, PersonalCopilot-konfig | `HAVENAgentCapabilityBrokerCell.swift:265`, `PersonalCopilotConfigurationFactory.swift:507` | Annonserer `grounding.decompose` — referanser, ikke kall |
| Tester | `CellScaffold/Tests/AppTests/PurposeQualityMonitorCellTests.swift:175`, `ExecutablePurposeGroundingCellTests.swift:102` | Status nå `ukjent` |
| `AIGatewayPurposePolicy` | `CellScaffold/Sources/App/Cells/AI/AIGatewayPurposePolicy.swift:31`, `:49`, `:58` | `taxonomyDigest` binder **ikke** Book-JSON: én hardkodet, ordnet liste (primaryPurposeRef, actionRef, to dataklasserefs, tre provider-destinasjoner) under `haven.aigateway.taxonomy.v1`, hashet med domene-UTF8 + nullbyte + lengdeprefiksede komponenter (`PurposeBoundExternalAction.swift:10`). **`nodeIdentifier` i Book 23 endrer ikke denne digesten.** Foreldelse skjer når pakkesnapshot/policybindings faktisk endres (`AgentTrustPackage.swift:284`, `:314`; `AgentTrustPackageApproval.swift:195`) |
| To `PerspectiveCell`, `GraphMatchTool`, `NetworkHealthPurposeCatalog`, `SDGPilotPurposeCatalog`, 23 HavenAgentD-filer med `purposeRef` (to stavemåter) | som i iterasjon 1 | — |

### 2.3 Pågående arbeid som overlapper

- **`PDD_formaalsregister-som-graf_2026-09-11`** (G1 venter): R1↔R2↔R3 for *registeret*. Dekker ikke R5.
- **Book 36** (venter): i konflikt med CellBase-modellen, §3.
- `REVISJON.md` §5 punkt 1–5.

---

## 3. Kartet — rettet etter Astra

| PDD-begrep (R5) | CellBase-motstykke (R3) | Passform | Merknad (med rettelser) |
|---|---|---|---|
| `purposeRef` | `Purpose.reference` via `nodeIdentifier` | **1:1 for verdien** | `Purpose` koder/dekoder feltet (`Purpose.swift:66`, `:91`). Beviser ikke likhet (`==` ignorerer det) eller kompatibilitet for alle konsumenter |
| `parentRef` | `partOf`/`parts` | **delvis** | Separate, skrivbare relasjoner som konstruktøren **ikke** synkroniserer (`Purpose.swift:20`). Grafen har dessuten `types`/`subTypes` — klassifisering og oppdeling er ikke automatisk samme relasjon. Python utleder composition-barn fra `parentRef` (`purpose_composition.py:52`); Swift-composition peker på egne eksplisitte leaves (`PurposeComposition.swift:102`). **Klassifikasjonsforelder, oppgaveforelder og composition må skilles** — FORMAALSSPEC §1 henger grenene under ulike globale formål *og* krever alle fem i roten; én kanttype bevarer ikke begge |
| `facetRefs` | `purposes`-kanter til samme Purpose-noder | **delvis — valg** | Relasjonen har ingen fasettmarkør; eksportkontrakten må erklære betydningen. Fasett gir aldri autoritet (`PurposeBoundExternalAction.swift:721`) |
| `title`, `summary` | `name`, `description` | 1:1 som data | `description` er intern, ikke offentlig for en separat CLI-modul (`Purpose.swift:18`) |
| `status` / `prohibited` | **ingen** | **mangler deklarert semantikk** | `states` kan *lagre* Interest-kanter, men definerer ingen livssyklus eller forbudshåndheving; matchemotorens filter evaluerer `Interest`, ikke Purpose-status (`WeightedGraphRuntime.swift:587`). **`candidate` er en publiseringsgrense** (KB `:17`): å generere alle noder som aktive er en atferdsendring |
| `goal{…}` | `GoalDefinition` + `GoalEvaluationCell` | **delvis, med større gap** | `Purpose.goal` er fortsatt `CellConfiguration`; fritekst-`verifier` blir ikke automatisk en fungerende evaluator; `campaign → deadline` er et valg som trenger tidssemantikk. Og: **`fromPerspectiveFields` lager `kind: evidence-rule`, `operation: satisfies`, som motoren ikke har gren for → `active`** (`GoalDefinition.swift:259`, `GoalEvaluationEngine.swift:247`). «Typet mål» er allerede i dag svakere enn «kjørbart mål» |
| `composition{kind,min,over}` | `Purpose.composition` | **delvis — konflikt, dypere enn operatornavn** | Se §3.1 |
| `derivedTest{kind, how, evidence}` | `evaluatorKind` + `GoalEvidenceSource` | **delvis, som beskrivelse** | Motoren utfører verken kommandoer, inspeksjon eller GUI-tester; `endpoint` er valgfri streng, ikke et krav om cellebasert evidens (`GoalDefinition.swift:53`, `GoalEvaluationEngine.swift:66`) |
| kjøringslogg | `PurposeResolutionRecord` / `GoalEvaluation` | **delvis** | Swift-evalueringen er et snapshot; Python beholder forsøk, målinger, rapporter, meninger med ulike regler. `[String:String]`-metadata erstatter ikke forsøkstilknytning og før/etter-semantikk uten ny kontrakt. «Rikere» i iterasjon 1 var feil som generell rangering |
| pakke | Purpose-delgraf + `interests` | **mangler som begrep** | `alwaysAttach`, jokertegn og OR over tags/surfaces er eksplisitt oppførsel `match(signal:)` ikke definerer |
| lærdom | **ingen**; `helperCells` kan *peke* til veiledning | **mangler direkte modell** | Feltet inneholder ikke symptom/årsak/forebygging. At registeret må bli en celle følger ikke av typene — det er et designvalg (M6) |
| porter G1/G1-GUI/G2/G3 | `GoalDefinition(human-confirmation)` | **delvis** — iterasjon 1 sa «god» | Et innsendt bekreftelses-event kan evalueres (`GoalEvaluationEngineTests.swift:69`); **ingen identitets- eller artefaktbinding følger av enumverdien**; motoren oppretter ikke innboks, verifiserer ikke hvem som godkjente, binder ikke til artefaktversjon (`:232`). Portrekkefølgen (G1 før G2 osv.) og artefaktkravene må representeres separat (`purpose_dev.py:201`) |
| oppgavemappe | projeksjonsmønsteret | **mønster, ikke passform** | Entity-projeksjonen har kilde/epoke/settutskifting for entiteter; ingen formål, ingen oppgavemappe |
| `lookup` | `WeightedGraphRuntime.match` | **delvis alternativ** — iterasjon 1 sa «erstattes» | Kanttraversering beviser ikke riktig språklig startpunkt eller riktig pakke-/lærdomsvalg; bedre treff på A16 er **ikke bevist** |
| `validate` | ingen samlet erstatning | **mangler** | Python sjekker pakker, goals, tester, lærdomsreferanser og porter (`purpose_dev.py:107`, `:194`); Swift har lokal dekoding og sykkelvern under matching (`WeightedGraphRuntime.swift:465`) — ikke en validator |
| `purpose://prompt.unknown` | noden finnes i KB (`:1854`) | **ikke «samme» som sikkerhetsgaranti** | Swift-blad kan tilfredsstilles av en suksesspost for enhver ref (`PurposeComposition.swift:207`). Å kopiere noden innfører ingen avvisningsregel; autorisasjon avgjøres separat (`PurposeBoundExternalAction.swift:720` avviser foreldre-/fasettmatch som autoriserende) |

### 3.1 Composition — faktisk semantikk, utledet ved kodelesing `[Astra]`

| Tilfelle | Swift | Python (Book 36) |
|---|---|---|
| Blad uten evidens | `unsatisfied / missingPurposeResolution` | `unverified / mangler måling` — **feil og ukjent er ikke samme ting** |
| Suksess, så feil/nytt forsøk | Siste **suksess** vinner; nyere `failed` opphever ikke | Siste måling/forsøk; ny rød → `red`; måling eldre enn forsøk → `unverified` |
| `allOf(A,B)`, bare A grønn | `partial` | `unverified` hvis B umålt, `red` hvis B rød |
| `anyOf(A,B)`, A grønn, B blokkert | Kan ikke representere blokkert; oversatt til missing/failed → `satisfied` | `blocked` propageres **før** disjunksjonen |
| `sequence`, B startet før A grønn, fullført etter | Godtas (sjekker fullføringstid; lik tid godtas) | Avvises (sjekker tilstand før hvert forsøk) |
| Tom `allOf`/`sequence`; Purpose uten composition | `satisfied`; behandles som blad | Krever eksplisitt composition på samlinger og ≥ 1 barn |
| `atLeast(0)` / `anyOf.min` | 0/negativt → `satisfied` | `min` utenfor 1…n avvises |
| `firstOf`, `invariant` | finnes ikke | valgt gren registreres; måling før/etter hvert steg; historiske brudd |
| Kodeform | `type/children/requiredCount`, leaves eksplisitte | `kind/min/over` + `childOrder` på noden |

**Konsekvens:** forsoningen (M3) gjelder *historikk-, start- og tomhetssemantikk*, ikke bare to manglende operatorer og `blocked`. Og `gates` (0/1/2/3) og `validate` (advarsel) er to ulike kontroller som ikke må smelte sammen i en migrering.

---

## 4. Konsekvenser — rettet

### 4.1 Det som blir bedre (med Astras forbehold)

1. **Én modell.** R2, R3 og R5 kan bli samme graf. *Forbehold:* `taxonomyDigest` binder allerede noe annet enn JSON-en (§2.2), så «én ting å binde» er et mål, ikke en bieffekt.
2. **Oppslag kan bli matching — for deler av `lookup`.** Kanttraversering med vekter og `localVariables` er en kandidat for KB-delen; pakke- og lærdomsvalget har eksplisitt oppførsel som må defineres på nytt. A16-forbedringen er ikke bevist.
3. **Mål blir evaluerbare mot innsendte observasjoner og støttede predikater.** Predikatmotor og bekreftelsestest finnes (`GoalEvaluationEngineTests.swift:69`). *Forbehold:* `human-confirmation` trenger et eksplisitt predikat og en **autorisert bekreftelseskilde** som motoren ikke leverer; `value`-predikatet kan ikke `≤` eller `⊆`.
4. **Challenge-maskineriet finnes — for tilkobling.** `AdmissionChallengePayload`, `connect.challenge`, `retryAdmissionSession` og Portholes «Open helper» er implementert (§1). *Rettelse fra iterasjon 1:* `GoalDefinition.helperCells` er **ikke** denne mekanismen. Integrasjonen fra et **avvist Meddle-steg ved keypath-traversering** (`GeneralCell.swift:1640`, `CellResolver.swift:1212`) til varslingssenter og retry av samme snevre forespørsel **finnes ikke** — den må bygges.
5. **Avdriftssjekken kan bli et kontinuerlig mål.** `GoalEvaluation.evidence[]` har formen én rad per kilde. *Rettelse:* motoren rapporterer status bare for **deklarerte** kilder; kildeinnsamling, fullstendighet, ferskhet og tidsplan er konsumentens ansvar; tom kildeliste gir tom evidens, og `allSatisfy` på tom liste er sann; `GoalObservation(status: .missing)` med verdi stoppes ikke; generelt predikatavvik gir `active`, ikke `at-risk` (`GoalEvaluationEngine.swift:72`, `:110`, `:125`, `:150`, `:178`). **Iterasjon 1s `claimsAllClear`-formel er utilstrekkelig.** Ro må bevises av konsumenten: deklarert kildemengde = forventet kildemengde, ingen tom evidens, hver kilde `fresh`.
6. **Metoden blir celler.** Book 35 §5s trigger er utløst; `GoalEvaluationCell` er en eksisterende adapter å starte fra.

### 4.2 Det som koster eller brekker — rettet

| # | Konsekvens | Alvor | Rettelse |
|---|---|---|---|
| K1 | **Verktøyet er Python, grafen er Swift.** | **høy** | *Presisert:* wire-formatet er vanlig Codable-JSON, og Python kan lese/skrive det. Det som mangler er en **avtalt graf-JSON-kontrakt og en runtime-bro** (matching, validering). Facilitator-kravet gjelder `Weight.encode`, ikke Purpose |
| K2 | **To composition-modeller spriker — i semantikk, ikke bare navn.** | **høy** | §3.1. Også kodeformen (`type/children` mot `kind/min/over`+`childOrder`) |
| K3 | **Tre goal-representasjoner.** | middels | `goal` og `helperCells` er separate API-er; omdøping krever eksplisitt betydning for begge. `GoalEvaluationCell` tas inn i inventaret |
| K4 | **Fem begrep uten hjem:** `status`/`prohibited`, pakke, `requiredArtifacts`, lærdom, oppgavemappe | **høy** | Uendret — men `candidate` som publiseringsgrense legges til |
| K5 | **`PerspectiveNodeImpl` er ikke ferdig** | middels | *Presisert:* `Purpose` har egen dekoder og grafmatching bruker ikke basisklassens `get`. Den reelle mangelen er `==` (relasjoner + `nodeIdentifier`) og **projeksjonssemantikk i `Perspective`**: upsert, referanseindeks, sletting, deterministisk eksport (§1) |
| K6 | **Tre → graf.** | middels | `derive_purpose_index.mjs` avviser flere foreldre og har ikke sykkelvern; Swift-katalogens kjede/LCA antar tre (`PurposeDecomposition.swift:213`, `:228`). Mer enn ny `compatibility.model`-tekst |
| K7 | **Konsumentene** | **høy** | *Rettet:* JSON-bevaring alene kobler ikke R1 til grafen — `PurposeTaxonomy` **og** `PurposeKnowledgeBase` er hardkodede Swift-kataloger; `ExecutablePurposeGroundingCell` kaller begge; `CellProtocolClient`-kontraktene må bestå |
| K8 | **Vekter finnes ikke.** | middels | Uendret |
| K9 | **To `PerspectiveCell`** | lav her | graf-PDD eier |
| K10 | **Ytelse** | `ukjent` — iterasjon 1 sa «ingen» | Målt for motoren (graf-PDD); **ikke** målt for import/eksport/CLI/konsumentløpet |
| **K11** (ny) | **Digest-påstanden var feil.** `nodeIdentifier` i Book 23 invaliderer ikke AIGateway-policy eller pakkegodkjenning | — | §2.2. JS-indeksens hash av rå `sourceText` endres derimot ved ren formatering |
| **K12** (ny) | **KB-metadata har ikke plass i Purpose:** `rootPrinciple`, `compatibility`/`changePolicy`, `statusMeanings`, `matchingHints`; Swift-uttrykk bevarer ikke `childOrder` | middels | «Byte-identisk rundtur» er ikke mulig som formulert |

---

## 5. Mitigering — rettet

| # | Mitigering | Lukker | Rettelse fra iterasjon 1 |
|---|---|---|---|
| **M1** | **Én kilde, med en *erklært* projeksjonskontrakt.** Ny `PerspectivePurposeProjection` (mønster: `applyEntityProjection`) eid av én celle, med `epoch` og sett-semantikk. Eksporten er en **legacy-bevarende** form: `parentRef` utledet av `partOf` når det er én, `composition` i Book 36-form for Python **og** Swift-form for grafen — begge generert fra én kilde, med delt testvektor; KB-metadata (`rootPrinciple`, `changePolicy`, `statusMeanings`, `matchingHints`) bæres i et sidefelt kontrakten definerer | K1, K6, K7, K12 | «Alle konsumenter leser videre uten endring» og «byte-identisk» er **strøket**. Kompatibilitet er *betinget* av bevart legacy-format, metadata, ordning og semantikk. R1s hardkodede kataloger må *genereres fra* kilden for å bli konsumenter — JSON-bevaring gjør dem ikke til det |
| **M2** | **Swift-CLI (`haven-purpose`)** for `export`, `validate` (graf), og `match` som **kandidat** for KB-delen av `lookup`; Python faller tilbake på leksikalsk **og sier det**. Pakke- og lærdomsvalget beholder sin definerte oppførsel til noe annet er *målt* bedre på fasitsettet fra graf-PDD | K1, K5 (validator) | «`lookup` erstattes» → «deler av `lookup` kan erstattes, målt» |
| **M3** | **Forson composition som én normativ kontrakt med delte testvektorer** — dekker §3.1 rad for rad: siste-suksess mot siste-tilstand, `blocked` som egen tilstand før disjunksjon, sekvensstart mot fullføringstid, tomme uttrykk, `atLeast`-grenser, `firstOf` med registrert gren, `invariant` med før/etter-måling. Kjetils valg: (a) utvid Swift til Book 36-semantikken, eller (b) snevre Book 36 til Swift. `[vurdering]` (a), fordi metodens evidensregler (Book 34-skillet, `blocked` ≠ `red`) er det PDD er bygget på | K2 | «Nye enum-cases og `blocked`» er **ikke** nok; `.continuous` alene er ikke et invariant-alternativ i dagens motor |
| **M4** | **`GoalDefinition` + `GoalEvaluationCell` som goal-form.** `Purpose.goal: CellConfiguration?` beholdes som det det er — en separat cellekonfigurasjon — og forholdet til `GoalDefinition` avklares eksplisitt. `lifecycle`-mapping `event → one-shot`, `campaign → deadline` skrives ned med tidssemantikk. **`fromPerspectiveFields` rettes** så den ikke lager predikater motoren ikke kan evaluere | K3 | «Helperen den egentlig er» strøket |
| **M5** | **Porter som mål — med tre ting motoren ikke gir:** (1) en **autorisert bekreftelseskilde** (Kjetils nøkkel, ikke et vilkårlig `goal.confirmed`-event), (2) **artefaktbinding** (digest av artefaktene som ble godkjent), (3) **portrekkefølge** (G1 før G2, G1-GUI før G2 for GUI). Oppgavemappen kan eksponeres som celle, men lagring og kontroll holdes atskilt: `requiredGrant`/`visibility` håndheves ikke av motoren | K4 (porter, artefakter, mappe) | «En port *er* et mål med human-confirmation» → «en port kan *beskrives* som et mål; godkjenningen må bindes separat» |
| **M6** | **Lærdomsregisteret som celle** — designvalg, ikke typekonsekvens. Lenkes via `helperCells` (peker) + `interests` (oppslag); forebygginger som er `derivedTest` peker på sitt `GoalDefinition` | K4 (lærdommer) | Merket som valg |
| **M7** | **Pakker som Purpose-delgrafer** — med `alwaysAttach`, jokertegn og OR-regler **deklarert** i kontrakten, ikke antatt dekket av `match` | K4 (pakker) | Lagt til deklarasjonskravet |
| **M8** | **`status`/`prohibited` som `states`-kanter er *lagring*.** Håndheving (ingen `prohibited` i autorisasjon, `candidate` ikke i runtime før porting) må skrives som egne regler i validator og eksport | K4 (status) | Lagring ≠ kontroll |
| **M9** | **Projeksjonssemantikk i `Perspective` først:** upsert på `nodeIdentifier`, referanseindeks, sletting, deterministisk ordning; `==` med relasjoner og `nodeIdentifier`. Basisklassens keypath-stubber er *ikke* på kritisk sti | K5 | Omformulert fra «gjør basisklassen ferdig» |
| **M10** | Vekter 1,0 på strukturelle kanter, deklarert; ingen læring i fellesregisteret | K8 | Uendret |
| **M11** | **Mål ytelsen for hele løpet** (import → eksport → CLI → konsument), ikke bare motoren | K10 | Ny |
| **M12** | **Avdriftsmålets ro bevises av konsumenten:** deklarerte kilder = forventede kilder (tellet), ingen tom evidens, hver kilde `fresh`, og `at-risk` settes av et **eksplisitt** predikat på differansen — ikke av generelt avvik | §4.1 pkt 5 | Ny — erstatter iterasjon 1s formel |
| **M13** | **Fra avvist keypath-steg til løsbar challenge:** når en celle avviser i `authorizationDecision`, skal avslaget **bevares gjennom traverseringen** (ikke falle til `try?` + bredere rotlesing, `GeneralCell.swift:1893`), og kunne løftes til en `AdmissionChallengePayload`-lik challenge med helper — gjenbruk av `connect.challenge`-forløpet for én operasjon, med retry av *samme snevre* forespørsel | §4.1 pkt 4, FORMAALSSPEC gren 3 | Ny — dette er det bladet `challenge-is-resolvable-from-notification` faktisk krever |

---

## 6. Konsekvenser for `PDD_mcp-tilgangsbevis` — rettet

| Element | Slik det uttrykkes i arkitekturen — med forbehold |
|---|---|
| Roten og grenene | `Purpose`-noder, `nodeIdentifier = purpose://candidate.mcp-tilgangsbevis.*`. **Tre relasjoner holdes atskilt:** klassifikasjon (`types` → `self-determination.data.*`), oppgavestruktur (`partOf` → roten), composition (eksplisitte leaves i `Purpose.composition`). Iterasjon 1 brukte `partOf` for begge |
| Hvert blads goal | `GoalDefinition` med **predikater motoren faktisk støtter** (`event-seen`, `contains-label`, `value` likhet). `expiry-ceiling` (≤ 15 min) og `⊆`-testen kan **ikke** uttrykkes som `value`-predikat i dag — de blir `custom` med en navngitt ekstern evaluator, eller motoren utvides (egen sak) |
| Grant-cellen og baseline-cellen (**to celler, vedtatt**) | `GoalEvidenceSource` per celle. `requiredGrant`/`visibility` er **deklarasjon**; håndhevingen ligger i cellenes egen `authorizationDecision`. Baseline-cellen: bare eierens nøkkel kan skrive |
| Avdriftssjekken | Kontinuerlig `GoalDefinition` evaluert via `GoalEvaluationCell` på tidsplan **som konsumenten eier** (motoren planlegger ikke). Ro bevises per M12. `at-risk` settes av eksplisitt predikat på «grant-sett ≠ baseline» |
| Antiformålene | Inntil M3: kontinuerlige mål som må forbli `satisfied`, **med** eksplisitt predikat (ellers `active`). Etter M3(a): `invariant(over: root)` |
| **Keypath** (Kjetils korreksjon, presisert av Astra) | Koden behandler allerede referansen som forespørselsdata og spør cellens policy (`CellResolver.swift:1121–1184`, `CellAuthorization.swift:16`). **Den brede `ownerProof`-regelen er en avgjørelse** — eierbevis før kontraktgrants gir bred eiertilgang (`CellAuthorization.swift:194`, `:228`, `:258`). Tre ting svekker den snevre forespørselen: (1) `getEmitterWithLabel` krever skriverett `-w--` på label **også for GET** (`GeneralCell.swift:2429`); (2) traverserende GET bruker `try?` og kan falle til bredere rotlesing som ikke bevarer barnets avslag (`:1893`); (3) `CellProtocolClient` kaller Meddle direkte, så resolverens preflight gjelder ikke alle innganger (`CellProtocolClient.swift:122`). **D5 omformuleres igjen:** «eksisterende celleavgjørelser må bevare den snevre forespørselen gjennom alle innganger; operasjonsspesifikk challenge/retry finnes ikke» |
| **Challenge-verktøyet** | `AdmissionChallengePayload` + `connect.challenge` + Porthole «Open helper» finnes for **tilkobling**. For et avvist *steg* må M13 bygges. `handleAt` fra menylinje-arbeidet er visningssiden; `GoalHelperCellRef` er en peker — ingen av dem er mekanismen |
| Scaffold-regler er ikke bare eierskap | Questionnaire vurderer respondentens operasjon/keypath (`QuestionnaireCampaignCell.swift:2454`); WorkItem delegerer til `ScaffoldSurfaceGatePolicy` (modus, utløp, requester, flate, tillatte keypather — `ScaffoldSurfaceGatePolicy.swift:113`, `:134`). `lesson.cellscaffold-two-holes` gjelder de cellene som *ikke* gjør dette — listen er `ukjent` |
| §1.7 | Skrives om etter M3. Inntil da står Book 36-formen merket «venter forsoning» |

---

## 7. Rekkefølge — rettet (forslag til PLAN, ikke plan)

Astra: «Fase 1 avhenger av fase 2 slik M1 sto, og fase 4s integritetskrav trengs før fase 1.» Enig. Ny rekkefølge, og med Kjetils presisering fra i dag: *at broen skal finnes* er ett formål; *hva den løser* er andre. Fasene under er ordnet etter det siste.

| Fase | Formålet den løser | Innhold | Rundtur-test | Hvor |
|---|---|---|---|---|
| A | Én sannhet | **Kontrakten først:** graf-JSON-kontrakt (legacy-bevarende eksport + metadata-sidefelt + begge composition-former fra én kilde) og **composition-forsoningen** (M3) med delte testvektorer for §3.1 | Python og Swift gir samme svar på alle §3.1-rader | CellBase + Book 36 |
| B | Grafen kan bære registeret | **Integritet i `Perspective`** (M9): upsert på `nodeIdentifier`, referanseindeks, sletting, deterministisk eksport, `==` | Importer 57 noder to ganger → identisk graf; slett én → borte | CellBase |
| C | Broen finnes | `PerspectivePurposeProjection` + `haven-purpose` CLI (M1, M2) | Book 23 → graf → legacy-eksport validerer i **dagens** `purpose_dev.py validate` uten endring; R1-katalogene genereres fra kilden og `ExecutablePurposeGroundingCellTests` er fortsatt grønne | graf-PDD (`bro`, `celle`) |
| D | Mål er kjørbare | `GoalDefinition`-form (M4), `fromPerspectiveFields` rettet, porter med autorisert bekreftelse og artefaktbinding (M5), avdrift med M12 | Port uten Kjetils nøkkel → ikke `satisfied`; tom kildeliste → ikke ro | ny PDD |
| E | Brukeren kan løse det som stopper | M13: avvist steg → bevart avslag → challenge → varsel → retry | `test.consume.challenge-resolvable` | denne PDD-en (gren 3) |
| F | Metoden bor i celler | Lærdomsregister (M6), pakker (M7), status (M8), Book 35/36 «Last verified against code» | `gates` = `GoalEvaluation`; lærdomsoppslag ≥ dagens treff på fasitsett | ny PDD |
| 0 | Denne PDD-ens tre i Purpose-form | **Utsatt til etter A** — Astra: uten `goalDefinition` i `Purpose.CodingKeys` og uten `invariant` beviser vellykket dekoding ingenting (ukjente felt ignoreres) | — | her |

---

## 8. Spørsmål til Kjetil — med Astras standpunkt

| # | Spørsmål | Mitt forslag | Astra |
|---|---|---|---|
| Q1 | Fasetter: `purposes`-kanter til samme Purpose-noder, eller `Interest`? | `purposes`-kanter, med fasettrollen erklært i eksportkontrakten | **Enig** |
| Q2 | Composition: (a) utvid Swift til Book 36-semantikken, eller (b) snevre Book 36 til Swift? | (a) | **Enig i å bevare `firstOf`/`invariant`, uenig i at nye cases + `blocked` er nok** — historikk-, start- og tomhetssemantikk må inn (§3.1) |
| Q3 | `GoalDefinition` + `GoalEvaluationCell` som goal-form? | Ja | **Delvis enig**; `Purpose.goal` skal ikke omtales som helper — begge felt trenger eksplisitt betydning |
| Q4 | Fase D–F i graf-PDD-en eller ny PDD? | Ny PDD; graf-PDD eier fase C | **Delvis uenig:** format- og semantikkvalg (A) kan ikke være «senere konsekvenser» av broen — de går *foran*. Én eller to mapper er organisatorisk |
| Q5 | Book 36 — godkjenne? | Ikke i dagens form; la den bli den normative kontrakten etter M3 | **Enig** — men kontrakten må vise *begge* implementasjoners forskjeller, ikke miste metodens evidens-/invariantregler |
| Q6 | Rådgiverpanel i tillegg til Astra på Q1–Q3? | Astra holdt; panel bare hvis du vil ha en tredje stemme på Q2 | — |
| **Q7** (ny) | Predikatmotoren kan ikke `≤` eller `⊆`. Utvide `GoalPredicate`/motoren (egen sak), eller bære slike tester som `custom` med navngitt ekstern evaluator? | Egen liten sak: `value` med numerisk sammenligning og `subset` — ellers blir halvparten av §5-testene `custom` | — |
| **Q8** (ny) | `ownerProof` gir bred eiertilgang før kontraktgrants (`CellAuthorization.swift:194`). Skal et agentutstedt bevis **aldri** regnes som eierbevis, slik at det faller til grant-veien? | Ja — det er det som gjør «to nøkler» til to nøkler | — |

---

## 9. Det jeg ikke har verifisert

- `PalazzoScaffold` (R4).
- `GoalEvaluationEngine.swift`, `GoalEvaluationCell.swift`, `CellAuthorization.swift`, `AdmissionContracts.swift`, `ConnectChallengeDescriptor.swift`, `PurposeKnowledgeBase.swift`, `AIGatewayPurposePolicy.swift`, `derive_purpose_index.mjs`, `purpose_composition.py`s `evaluate` — **lest av Astra, ikke av meg**; alle sti:linje merket `[Astra]` står på dens lesing.
- Swift-testene i §3 er **lest, ikke kjørt**; passing status er `ukjent`. Filenes eksistens er ikke en grønn kjøring.
- Hvilke scaffold-celler som bare sjekker eierskap (listen bak `lesson.cellscaffold-two-holes`).
- Ytelse for hele import/eksport/CLI/konsumentløpet.

---

## 10. Revisjonslogg

| It. | Dato | Hva | Hvem |
|---|---|---|---|
| 1 | 2026-09-12 | Skrevet etter lesing av `PurposeAndInterest/` (10 filer), Book 35/36, graf-PDD, REVISJON. Codex-gjennomgang bestilt | Losen |
| 2 | 2026-09-12 | **Validert av Astra** (`handoff/CODEX_REVIEW_PERSPECTIVENODE.md`, 193 linjer, 15 rettelser). Tatt inn: `GoalEvaluationEngine`s faktiske oppførsel (§1), `GoalEvaluationCell` og `PurposeKnowledgeBase` i inventaret, challenge-maskineriet (`AdmissionChallengePayload`/`connect.challenge`) som det som finnes, digest-påstanden rettet (K11), KB-metadata (K12), composition-semantikk rad for rad (§3.1), `ownerProof` og de tre inngangene som svekker den snevre forespørselen (§6), M1 uten «byte-identisk», M5 med autorisert bekreftelse og artefaktbinding, M12 (ro bevises av konsumenten), M13 (avvist steg → challenge), faser omordnet A–F med kontrakt og integritet foran broen, fase 0 utsatt. Q7 og Q8 nye. Tre overdrivelser fra iterasjon 1 navngitt i §0 | Losen |
