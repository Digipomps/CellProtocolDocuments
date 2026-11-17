# Revisjon: er formål oppdatert med PerspectiveNode, så signalmatching kan brukes?

Dato: 2026-09-11 · Losen · Bestilt av Kjetil: «Gå igjennom alt som bruker formål og sjekk om det er oppdatert med PerspectiveNode-implementasjon av formål og interesser så vi kan bruke signal matching. Gå igjennom tester vi tidligere har gjort på performance og kvalitet på oppslag fra formålsdekomponering. Det er vel endel taksonomi som må sjekkes også.»

Stier er relative til repo-rot. Alle tall er **målt i denne revisjonen** der annet ikke står; påstander merket `[vurdering]` er mine.

## Kort svar

Grafen finnes og er god. Formålene er bare ikke i den.

`Purpose` og `Interest` **er** allerede `PerspectiveNodeImpl` med `match(signal:)` — arvegrunnlaget er på plass. Men de eneste stedene i produksjonskode som faktisk *lager* slike noder er demodata inne i `Purpose.swift` («Be with friends», «LA GARROTXA», «Volcano», «Medieval»). HAVENs egne formål lever som `purpose://`-strenger i to andre trær som ikke snakker med grafen, og som heller ikke er like. Signalmatching kan derfor i dag ikke matche på HAVENs formål — den matcher på et laboratorium.

## 1. Fire parallelle representasjoner av formål

| # | Representasjon | Hvor | Form | Hvem bruker den |
|---|---|---|---|---|
| R1 | `PurposeTaxonomy` | `CellScaffold/Sources/App/Support/PurposeDecomposition.swift` | 44 `purpose://`-strenger med forelder/alias/kjede | formålsdekomponering i drift |
| R2 | Purpose Knowledge Base v0 | `CellProtocolDocuments/Book/haven_purpose_knowledge_base_v0.json` + index | 57 noder med Goals og facets | Book 23, evaluator, `ExecutablePurposeGroundingCell` |
| R3 | `Purpose`/`Interest` som grafnoder | `CellProtocol/Sources/CellBase/PurposeAndInterest/` | `PerspectiveNodeImpl` med `types/subTypes/parts/partOf/interests/purposes/entities/states`, vektet | signalmatching, `PerspectiveCell` |
| R4 | `PalazzoSignalMatcher`, `PalazzoMenuSignal`, `PalazzoContentSignal` | `PalazzoScaffold/Sources/App/Cells/PalazzoEntityCell.swift` m.fl. | egen signalmodell med id/version/kind | Palazzo-matchingen |

I tillegg finnes **KSM-porten** i `Kallimachos/Forskning/Flerlags_Signalmatching/Swift/SignalMatching/` — bevisst en forskningspakke, men den er en femte Swift-implementasjon av samme idé.

`purpose://`-strenger brukes bredt (TrustPacket, Correspondence, AgentTrustPackage, EffectReceipt, PurposeQualityMonitor, WorkItems, QuestionnaireCampaign, PersonalCopilot, Palazzo). `PerspectiveNode`/`Signal`/`WeightedGraphRuntime` refereres **bare** innenfor `PurposeAndInterest/`-mappen selv, pluss `CellApple/Intelligence/Tools/GraphMatchTool.swift` og de to `PerspectiveCell`-ene. Det er skillelinjen.

## 2. Taksonomi-divergens — målt

R1 (runtime, 44 noder) mot R2 (dokumentert, 57 noder): **31 felles.**

**13 noder finnes i runtime, ikke i Book 23** — de er udokumenterte:
`analysis.advisory-panel`, `analysis.decision-support`, `analysis.evidence-ledger`, `analysis.meta-evaluation`, `analysis.problem-framing`, `analysis.synthesis`, `capability.construct-cellconfiguration`, `capability.delivery`, `capability.request-human-review`, `capability.request-new-functionality`, `capability.reuse-visible-configuration`, `questionnaire.campaign`, `questionnaire.response`.

**26 noder finnes i Book 23, ikke i runtime** — de kan ikke løses opp av dekomponeringen. Blant dem hele `self-determination.data`-grenen (8 noder: scope, use-purpose, recipients, duration, locality, manner, exercisability, verifiability), `human-agency`, `contact.*`, `event.*`, `skeleton.owner-entity-access`, `knowledge.explain-policy`, `personal-context.semantic-state`, `purpose-taxonomy.capture-and-place`, `test.acceptance.hallucination-evaluation`.

**Konsekvensen er ikke kosmetisk.** A1/A4-kontrakten bygger på *exact match* på `primaryPurposeRef`, og AgentTrustPackage binder en `taxonomyDigest`. Når to trær er uenige om hvilke refs som finnes, avhenger svaret av hvem du spør — og digesten binder bare det ene. `[vurdering]` Dette er den mest presserende enkeltfeilen i revisjonen.

## 3. Signalmatching er implementert — to ganger, og ingen av dem fôres av formålene

**I CellProtocol** finnes en komplett motor: `Signal` med `relationship`, `weight`, `tolerance`, `token`, `ttl`, `hops`, **`localVariables`** og `HitCollector`; `WeightedGraphRuntime` (693 linjer); `MatchStrategyPlanner` med `system1Preconfigured`/`system2Reconfiguration`, strategiene `cachedWeightedSignal`/`sparseVectorFilter`/`layeredSignal`/`deepReconfiguration`, plassering `cpuLocal`/`cpuParallel`/`gpuBatch`/`remoteAccelerated`, og eskaleringstriggere (lav konfidens, tvetydig topp-K, manglende dekning, ny kunnskap, personvernport, budsjett overskredet). Det er september-forskningen, realisert.

Testene finnes og er reelle — `PurposeInterestRuntimeComparisonTests` har blant annet `testLayeredConferenceScenariosCarryLocalVariablesIntoNextMatchLayer`, `testScaleRuntimeComparisonReportsMultipleProfileSizesAndQuality` og `testIndexedWeightedSignalMatchesWeightedSignalTopRanking`.

**Men:** KSM-porten fra forskningspakken er **ikke integrert** i CellProtocol (søk etter `SignalMatching`/`ksm` i `CellProtocol/Sources` gir null treff), selv om beslutningen 2026-09-05 var at matchingen skal eies av CellProtocol og implementeres i Swift. Porten er grønn på alle tre konformansnivåene (202 kontroller, 0 avvik). Vi har altså to Swift-motorer for samme sak, og den som er konformanstestet er den som ikke er i produkt. `[vurdering]`

**Og:** `PurposeInterestAdjacencyIndex` — bindeleddet mellom `purposeRef`-strenger og vekter — brukes **ingen steder** utenfor sin egen fil. `PerspectiveCell` seeder grafen med ett bootstrap-hjelpeformål (`perspective.bootstrap.helper`), ikke med taksonomien. Det er derfor grafen står tom for HAVENs faktiske formål.

Det finnes dessuten **to `PerspectiveCell`-implementasjoner**: `CellProtocol/Sources/CellApple/PurposeAndInterest/Cells/PerspectiveCell.swift` og `CellScaffold/Sources/App/Cells/Perspective/PerspectiveCell.swift`. Begge registreres som `cell:///Perspective` i sine respektive scaffolds.

## 4. Tester på ytelse og kvalitet — hva som finnes og hvor ferskt det er

| Måling | Resultat | Dato | Fersk? |
|---|---|---|---|
| Kvalitet på formålsoppslag (`latest-purpose-eval.json`) | **56/56 saker, 100 %**, 20 kategorier, 4 kilder | generert 2026-08-09 | **Nei** — før september-nodene, før AgentTrustPackage-kandidatene |
| E1–E4 modelleksperimenter (shortlist, microtask, yes-kalibrering, kaskade) | rådata i `Tools/PurposeKnowledge/results/` | juli 2026 | Nei |
| KSM-ytelse E1 skala (5 mønstre, branch 8, 24 ankere) | se under | 2026-09-02/03 | Ja |
| Konformans (uttrykk/lag/mønster) | 202 kontroller, 0 avvik; Swift-porten bit-identisk med Python | 2026-09-03 | Ja, men utenfor produkt |
| Hallusinasjonsporten (Book 23) | definert som draft med terskler (≤1 % hallusinerte refs, ≤3 % ubelagte påstander, ≥90 % «unknown») | — | **Aldri kjørt periodisk** |

**KSM-tallene, som svarer direkte på arbeidshypotesen din:**

| profiler | noder | kanter | konfigurering | validering | indeks | statistikk | planlegging |
|---|---|---|---|---|---|---|---|
| 50 | 170 | 604 | 4,66 ms | 0,080 | 0,196 | 4,191 | 0,239 |
| 800 | 2420 | 9567 | 7,94 ms | 0,083 | 2,983 | 4,702 | 0,249 |

Matching, samme kjøring: **32–267 µs kompilert mot 445–2970 µs naivt, 5–30× raskere.** N* (hvor mange gjentakelser før kompilering lønner seg) er 0,4–3,6.

**Hypotesen holder, men med en presisering.** Konfigurering er dyrere enn matching — og planleggingen er *konstant* 0,24 ms mens grafen tidobles, mens matching er mikrosekunder. Men «dyrt» er 5–8 millisekunder, ikke sekunder, og statistikk-steget er det som dominerer (4,2–4,7 ms). `[vurdering]` Den virkelige kostnaden i Kallimachos blir ikke matchingen eller planleggingen, men tokens i det øyeblikket en språkmodell må inn for å dekomponere noe ukjent. Det er nettopp derfor R1↔R3-broen er verdt å bygge: hver gang et formål allerede finnes som node, slipper man modellen.

## 5. Hva som skal til, i rekkefølge

1. **Én taksonomi.** Velg Book 23 JSON som kilde og generer Swift-runtimens tabell fra den (eller motsatt), med en test som feiler på divergens. 26 dokumenterte noder mangler i runtime og 13 udokumenterte lever der. Dette blokkerer alt annet, og er også det A4s `taxonomyDigest` faktisk skal binde. **S–M.**
2. **Bro fra ref til node.** En loader som bygger `Purpose`/`Interest`-noder med vekter fra taksonomien og tar `PurposeInterestAdjacencyIndex` i bruk, slik at grafen inneholder HAVENs formål. Uten denne er signalmatching ikke tilgjengelig for noe som helst produktformål. **M.**
3. **Én motor.** Enten port KSM inn i CellProtocol som besluttet 2026-09-05, eller erklær CellProtocols egen motor som gjeldende og pensjoner porten til referanse. Behold konformansvektorene uansett — de er fasit for begge. **M–L.**
4. **Palazzo.** Adapter `PalazzoSignal*` til CellProtocols `Signal`, eller skriv ned hvorfor den skal være separat. **S for beslutningen.**
5. **Kjør evalueringen på nytt** og gjør den til en port som kjører ved endring i taksonomien — den er en måned gammel og dekker ikke dagens tre. **S.**

Ingen av disse krever nye kapabiliteter. Alt er skrevet; det som mangler er at delene peker på hverandre.
