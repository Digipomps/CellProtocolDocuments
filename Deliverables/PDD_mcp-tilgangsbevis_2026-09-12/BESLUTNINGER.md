# Beslutninger — formålsarkitekturen for `PDD_mcp-tilgangsbevis`

2026-09-13/14 · Losen · **Iterasjon 2: begge rådgiverne har svart** — Fabel (`panel/FABEL_SVAR.md`, 2 448 ord) og Astra (`panel/ASTRA_SVAR.md`, 87 linjer, levert 23:40). Det som endret seg fra iterasjon 1 er merket **[it. 2]**. Én beslutning har reell uenighet mellom rådgiverne (B2) — der står begge standpunkt, mitt valg, og hvorfor.

Din instruks, ordrett: «goalDefinition er kjernen her så det må inn i dekodingen. Ta med Astras innvendinger - om du syns spørsmålene er uavklart bruk rådgiverpanel. Gå etter effektiv, fleksibel og robust løsning.»

Slik leser du dokumentet: hver beslutning har **hva den innebærer** i klartekst, **hvorfor** mot dine tre kriterier, **hva panelet sa**, og **hva du gjør** — som oftest ingenting, med mindre du er uenig. De tre spørsmålene som faktisk trenger deg står i §10.

Kilder: `PERSPECTIVENODE_KONSEKVENS.md` (it. 2), `handoff/CODEX_REVIEW_PERSPECTIVENODE.md` (Astra, 12.09), `panel/BRIEF.md`, `panel/FABEL_SVAR.md` (13.09), og `../PDD_formaalsregister-som-graf_2026-09-11/handoff/ASTRA_KEYPATH_DESIGN.md` (Astra, 13.09, fra din andre tråd). Stier relative til `HAVEN/`.

---

## B1 — `goalDefinition` inn i `Purpose`: inline, valgfri, med streng dekoding

**Beslutning.** `Purpose` får feltet `goalDefinition: GoalDefinition?`, kodet og dekodet med `decodeIfPresent`/`encodeIfPresent` på samme måte som `goal`, `helperCells` og `composition` i dag (`CellProtocol/Sources/CellBase/PurposeAndInterest/Purpose.swift:60–62`). Ikke `goalRefs`, ikke begge.

**Hva det innebærer.** Et formål bærer sitt eget mål i samme JSON. Gammel JSON uten feltet dekodes fortsatt (feltet blir `nil`). Tre regler håndheves *ved dekoding*, ikke senere:
1. `goalDefinition.purposeRef == purpose.reference` — et mål som tilhører et annet formål er korrupt data og kastes, ikke lastes stille.
2. `Purpose.goal: CellConfiguration?` beholdes og **får en erklært betydning**: det er konfigurasjonen av *cellen som evaluerer målet* (`GoalEvaluationCell` dekoder nettopp `definition` fra sin konfigurasjon, `CellProtocol/Sources/CellBase/Cells/Purpose/GoalEvaluationCell.swift:12–17, :29`). Er begge satt, må konfigurasjonens definisjon være lik `goalDefinition`.
3. De to hjelperlistene holdes atskilt med erklært mening: `Purpose.helperCells` er formålets egne hjelpere (konfigurasjoner); `GoalDefinition.helperCells` er pekere til remediering ved `blocked`/`at-risk`. Validator: en satt `GoalHelperCellRef.purposeRef` må være formålets egen referanse.

I samme pakke: `GoalDefinition.fromPerspectiveFields` rettes så den ikke lager predikatet `evidence-rule/satisfies` som motoren ikke har (`GoalDefinition.swift:280–285`, `GoalEvaluationEngine.swift:247`); og motoren gir `unknown` med `missing: ["predicate"]` for manglende eller ukjent predikat i stedet for stille `active`.

**Hvorfor.** *Effektiv:* én CodingKey, én dekoderlinje, én encodeIfPresent; mønsteret står i samme initialisator. `goalRefs` ville krevd et måloppslag som ikke finnes (`Perspective` har intet målregister). *Fleksibel:* «ett mål delt av flere formål» motsies av typen selv — `GoalDefinition` har ett `purposeRef` (`GoalDefinition.swift:202`). Skal noen peke på et mål i drift, finnes det som celleendepunkt (`goal.definition.current`, `GoalEvaluationCell.swift:67`). *Robust:* en Purpose med et annet formåls mål er «feltet sier X, bytene sier Y» — kast ved dekoding.

**Panel.** Fabel: inline, `decodeIfPresent`, likhet håndheves ved dekoding, `goal` = evaluatorkonfigurasjon, hjelperlistene atskilt — sikkerhet **høy**. Astra (panel) **[it. 2]**: inline, eksakt `purposeRef`-binding — sikkerhet **høy**. Enige. Astra legger til fire krav som tas inn: (i) dekoding skal skje **uten** celleoppretting, nettverksoppslag eller helperkjøring; (ii) aktive, utvekslede formål må ha stabil `nodeIdentifier` — navneendring flytter ikke målets identitet; (iii) validering av *aktive* mål sjekker referansebinding, skjema, kilde-ID-er og støttede predikater; (iv) gamle lesere skal ikke kunne bruke et mål de ikke forstår som godkjent grunnlag. Og en presisering av `fromPerspectiveFields`-rettingen: å døpe fritekst om til `custom` gjør den ikke kjørbar — fritekst beholdes som beskrivelse, og målet blir ikke aktivt før en evaluator er valgt. Slik A1 er skrevet gir `predicate: nil` + `evaluatorKind: .custom` + tag `evaluator:missing` nettopp `unknown` fra motoren, aldri `active` — det *er* «ikke aktivt før evaluator er valgt».

**Hva du gjør.** Ingenting — du har allerede sagt *at*; dette er *hvordan*. Si fra hvis du vil ha `goalRefs` likevel.

---

## B2 — Composition: Book 36-semantikken er normen; Swift porteres mot delte testvektorer

**Beslutning.** Alternativ (a) fra `panel/BRIEF.md` P1, med Fabels presisering: **Pythons kjørende evaluator er referansen**; Swift `PurposeComposition` porteres til den og består de samme testvektorene. Book 36 oppdateres etterpå fra det som kjører. Alternativ (c) — to lag med tapstabell — avvises.

**Hva det innebærer.** Seks endringer i `PurposeComposition.swift` (fase A), én utsatt:
1. `PurposeResolutionStatus` får `.blocked` (additivt; `purposeSolvedWithin` filtrerer på status og påvirkes ikke, `Constraint.swift:173–174`).
2. Bladet leser **siste post uansett status** — ikke siste suksess (`PurposeComposition.swift:38–41`). `started` nyere enn siste `succeeded` → `unknown`; `failed` → `unsatisfied`; ingen post → `unknown`. Statusenumet får `unknown` og `blocked`.
3. `blocked` propageres **før** `anyOf`/`atLeast`/`firstOf` — et blokkert alternativ gjør ikke samlingen grønn.
4. `sequence` bruker `started`-poster: et barn startet før forrige var `satisfied` blokkerer, uansett fullføringstid (i dag sjekkes bare `completedAt`, og lik tid godtas, `:325`).
5. Tomme barnelister og `requiredCount` utenfor 1…n avvises i `init(from:)` — feil på artefaktet, ikke en status.
6. Bladfallback bare for Purpose uten `parts`; med `parts` og uten composition → `unknown` (Book 36 §2 «ingen default»).
7. **Utsatt:** `firstOf` med registrert gren og `invariant(over:)` med før/etter-målinger trenger en typet evidenspost (`metadata: [String:String]` er ikke en kontrakt). Inntil da bæres antiformålene som `GoalDefinition(lifecycle: .continuous)` med eksplisitt predikat — og kontinuiteten er konsumentens, siden motoren ikke leser `lifecycle`.

Fem eksisterende Swift-tester endres (`PurposeCompositionTests.swift`). Testvektorene legges som `contract/composition-vectors.json` og kjøres av **begge** implementasjonene.

**Hvorfor.** *Robust:* Swift-semantikken bryter regelen om at feil og ukjent er to slags påstand — i dag havner en `failed`-post i `missingPurposeRefs` (`PurposeCompositionTests.swift:22–26, 35–40`), og tomhet er inkonsistent i samme fil (tom `allOf` grønn, tom `anyOf` rød). `blocked ≠ red` er det PDD hviler på. *Effektiv:* Python kjører allerede med ønsket oppførsel; korteste vei er å ta den som vektorer. *Fleksibel:* ett vokabular; `firstOf`/`invariant` følger vektorene når (7) tas.

**Panel — her er rådgiverne uenige [it. 2].**
- Fabel: **(a)** med Python som referanse, sikkerhet middels. Siste-suksess er «et valg ingen har forsvart»; (c) er «feltet sier signert, bytene sier noe annet» i composition-form.
- Astra: **(c)** med tapsfri lagring, sikkerhet middels. Argument: «hva som tidligere lyktes» (resolution) og «hva som nå er verifisert» er to spørsmål om samme graf, og én felles navngitt type er ikke alene et argument for én historikksemantikk. Nedmappingen til dagens Swift-form skal være en *merket* kompatibilitetsprojeksjon som aldri kan avgjøre porter.
- **Det begge fant:** ingen operativ produksjonskonsument av dagens resolution-semantikk. Astras eneste kallsted utenom testene er en benchmark som lager en ikke-tom `allOf` med syntetiske suksessposter (`CellProtocol/commons/benchmarks/purpose-interest/Sources/PurposeInterestBenchmarkSupport/ConferenceSwarmScenarioSupport.swift:1080`) — den dokumenterer ikke behov for «suksess etter senere feil». Fabel: `evaluate` har ingen kaller i evidensettet utenom testene.

**Mitt valg står: (a).** Grunnen er kriteriene dine. *Effektivt:* (a) endrer én type og fem tester; (c) legger til en ny type, en projeksjon, en tapstabell og holder to evaluatorer i live for en semantikk ingen bruker. *Robust:* med (c) finnes det en lagret form som kan si `satisfied` der verifikasjonen sier `blocked` — merket eller ikke, det er nøyaktig `lesson.ciphertext-field-held-plaintext-hash`. *Fleksibelt:* Astras «to spørsmål» er reelle, men de trenger ikke to typer — dukker en konsument av «siste suksess» opp, er det et `resolutionPolicy`-parameter på `evaluate`, ikke en parallell modell. K3 gjelder fortsatt: du bekrefter at eksisterende Swift-oppførsel kan endres.

**To ting Astra fant som tas inn uansett:** (1) Book 36 er **selvmotsigende** om `anyOf`: §3.3 sier «hvilken som helst holder» (eksempelet med SSH-inventar / deploy-CLI / statusflate), §4 sier «en samling der et barn er `blocked` er ikke grønn» (`Book/36_Purpose_Composition.md:69`, `:122`). Et SSH-avslag ville da stanse en fullt verifisert statusflate. Dette må avgjøres i testvektorene — **K4** under. (2) En evaluering kan *påvise* ulovlig sekvensstart, men ikke *forhindre* sideeffekten — den utførende cellen må kontrollere startadgang separat. Skrives inn som avgrensning i vektorfilen.

**Hva du gjør.** Bekreft at det er greit å endre oppførselen til eksisterende Swift-tester (§10 K3). Alt annet er dekket.

---

## B3 — Beviset er en delegert bærernøkkel med signert grant, ikke et token som «er» deg

**Beslutning.** Alternativ B fra P3. Claude og Codex har **hver sin nøkkel**. Agenten utsteder — fra identiteten i din entitet — en **signert grant-kontrakt** til bærerens nøkkel: (celle, datareferanse, operasjon, utløp, grant-digest, nonce). Cellen autoriserer via den eksisterende grant-/kontraktveien. Beviset er aldri et eierbevis — strukturelt, ikke ved regel.

**Hva det innebærer.**
- `CellAuthorizationPolicy.decide` returnerer ved eiertreff og når aldri grant-veien for en requester som ser ut som eieren (`CellProtocol/Sources/CellBase/Cells/GeneralCell/CellAuthorization.swift:194–212`). Under A (impersonering) får bæreren derfor enten *alt* eller *ingenting*; grantene leses ikke i noen av tilfellene. Under B har bæreren egen UUID og nøkkel; begge eierkontroller er falske; policyen går til `Grant(keypath:, permission:)` mot `contracts: [Agreement]` via `checkGrant` (`:228–243`); ingen kontrakt → `deniedNoGrant` (`:258–268`). Avgjørelsen bærer `contractRef`/`grantRef` og requesterens fingeravtrykk — attribusjonen (R5) følger av strukturen.
- Kontrakttypen som gjenbrukes er `Agreement` med `Grant(keypath, permission)` (`CellProtocol/Sources/CellBase/Agreement/Grant/Grant.swift`, `Agreement.swift:238`) — samme type som `AdmissionChallengePayload.agreement` bærer. **`Grant.granted` krever identisk keypath** (`Grant.swift:61`); ingen undertre-/jokersemantikk. Det er ikke en mangel her: et grant til Claude skal være eksakt (`lesson.purpose-never-grants-rights`: exact match).
- Det som må bygges: (1) en **signert konvolutt** rundt Agreement-grantet, modellert på `SignedRemoteIntentPayload{issuerID, nonce, issuedAt, expiresAt}` (`HavenAgentD::Sources/HavenAgentRuntime/RemoteIntentVerifier.swift:52–81`) og verifisert som `verify` gjør det — utstedernøkkel fra *policy*, utløp med skjevhet, tomme allowlister avvist (`:158–208`); pluss **grant-digest** av grant-cellens innhold i utstedelsesøyeblikket. (2) **Provisjonering:** bæreren lager nøkkelparet selv og sender bare offentlig nøkkel; agenten ser aldri privatnøkkelen. (3) **Revokasjon:** en endring i grant-cellen endrer digesten; hvert utestående bevis bærer den gamle og avvises som «stale grant digest» (R2, `never-survives-narrowing`). Én handling dreper alle (`revocation-is-one-act`).
- `AgentEntityLinkContract` er feil form (gjensidig, fritekst-`scope`, permanent, `AgentEntityLinkContract.swift:25–35`); bare `canonicalizeRemovingTopLevelKeys(keys: ["signatures"])` gjenbrukes for digesten (`:58–61`).
- Tre ting testene må hevde (fra Astra 13.09 og Fabel): `path != .debugBypass` — `debugValidateAccessForEverything` slipper alt forbi (`CellAuthorization.swift:181–192`); `Identity.granted` bruker `grants.contains(grant)` mens `Grant.==` bare sammenligner keypath, så **rettighetsmasken sammenlignes ikke på den veien** (`Identity.swift:182`, `Grant.swift:7`) — negativ test: riktig keypath, feil operasjon → nektet; og et rot-grant kan gi bredere adgang gjennom dispatch enn en nodeavgrensning (`GeneralCell.swift:1599, :1617, :1893`) — grantene i grant-cellen skal derfor aldri være rot-keypaths.

**Hvorfor.** *Robust:* A feiler åpent hvis beviset godtas; B feiler lukket. Q8 («aldri ownerProof») blir overflødig — en egenskap som følger av typen slår en regel noen må huske. *Effektiv:* B bruker grant-veien som den står; A krever omskriving av `decide`. *Fleksibel:* B gjelder enhver bærer, ikke bare deg.

**Panel.** Fabel: B, sikkerhet **høy** — «A er strukturelt umulig å innsnevre». Astra (panel) **[it. 2]**: B, sikkerhet **høy**, med eget UUID for bæreren — samme UUID som deg med annen nøkkel avvises før grant-veien (`CellAuthorization.swift:214`). Enige. Astra fant **typen som skal gjenbrukes**, og den endrer hva som må bygges:
- **`Contract.signed(agreement:issuer:subject:domain:)`** i `CellProtocol/Sources/CellBase/Agreement/Contract.swift:74, :86` binder utsteder og mottaker hver for seg, begge nøkkelfingeravtrykk, domene, Agreement og tidsrom i signaturen. **Ikke** `ownerSignedSnapshot` (`:116`) — den setter samme identitet på begge sider. Den signerte konvolutten i punkt (1) over erstattes altså av `Contract.signed`; bare grant-digest og eksakt målcelle må legges til, for payloaden har ingen `cellUUID`.
- **`GeneralCell` godtar kontrakten bare etter kontroll av at eier = utsteder, requester = mottaker, domene, gjeldende mal, betingelser og mottakerens nøkkelkontroll** (`GeneralCell.swift:2048`), og kontrakten må *installeres* gjennom et autorisert celleforløp — signaturen alene er ingen import. **Det skjerper K1:** utstederen må være *cellens eier*. Hvis scaffold-cellene dine eies av din operatøridentitet og ikke av agentidentiteten, kan agenten ikke utstede en gyldig kontrakt for dem — da må din nøkkel signere (via en bekreftelse du ser), eller eierskapet må være på entitetsnivå slik at entitetslenken gjør agentidentiteten til eier. Se K1.
- **Revisjonsloggen navngir ikke bæreren av seg selv** — jeg overdrev i iterasjon 1. Avgjørelsen har requester-felt, men sikkerhetsloggen registrerer bare *avslag* (`GeneralCell.swift:1997`); tillatt bruk trenger en eksplisitt kvittering. `audit-names-the-proof` er dermed noe som må bygges, ikke noe som følger.
- **Revokasjon:** lokal kontraktfjerning finnes (`GeneralAuditor.swift:441`) men ingen distribuert revokasjon eller vern mot gjeninnføring av gammel autoritet. Regel: utilgjengelig revokasjonsstatus → avslag for dette beviset. Kort utløp + revokasjonsgenerasjon + kontroll rett før sideeffekt.
- B løser ikke traverseringsfeilene (`try?` før fallback, skriverett på label for GET) — de er D4/E1.

**Hva du gjør.** Svar på §10 K1 — det avgjør *hvilken* identitet som signerer kontrakten.

---

## B4 — Porter: i dag er ditt ord i STATUS.md + transkriptet; «signert» får ikke brukes før port-cellen finnes

**Beslutning.** G1/G1-GUI/G2/G3 settes i dag ved at **du** skriver eller sier det, og Losen skriver `godkjent <dato>` i STATUS.md med henvisning til setningen i transkriptet. Claude og Codex skriver aldri den linjen på eget initiativ. Ordet «signert» står ikke i STATUS.md før mekanismen under finnes. Målformen (senere) er en **port-celle** som er eneste requester med `-w--` på `goal`, fôret av en operatørbekreftet signatur.

**Hva det innebærer.** Forslaget i BRIEF P4 — `AgentSignatureStatement` som «Kjetils ord» — holder ikke: `signStatement` signerer med **agentens** identitet (`owner.sign`, signer = `identityDescriptor`, «created by local HAVENAgentD identity», `HavenAgentD::Sources/HavenAgentRuntime/AgentSignatureStatement.swift:371–377, :390, :404`) og krever ingen operatørbekreftelse (`:353–369`). Kan MCP-klienten kalle `agent.identity.sign_statement` — og det kan den (`HavenAgentMCPService.swift:960`) — kan Claude eller Codex, partene som portes, selv skaffe en «gate.approved»-signatur. En godkjenning den godkjente kan utstede er ikke en port. `verifyEnvelope` verifiserer mot nøkkelen *inne i* konvolutten (`:408–419`) — selvkonsistens, ikke avsender. Og `GoalEvaluationCell.goal.evaluate` tar erstatningsobservasjoner fra enhver med `-w--` (`GoalEvaluationCell.swift:147–164, :229–231`) — evalueringscellen kan ikke være verifikator.

Når D7 er grønn: formål `personal.identity.approve-gate` som bare godtas via operatørbekreftelse (`validatePurpose`, `:421–425`), `correlationID` til bekreftelsen, payload = artefaktdigest, `audience.entityRef` = port-id + oppgavemappe (så en G1 ikke spilles av på en annen PDD). Verifisering i port-cellen med betrodd nøkkel i policy (mønster `RemoteIntentVerifier.swift:189–208`). Portrekkefølgen som `sequence` **etter** B2 — dagens `sequence` sjekker bare fullføringstid, og `event-seen` sammenligner ikke tid.

**Hvorfor.** *Robust:* det signerte alternativet er i dag *også* forfalskbart av dem som portes, og koster mer. Uforfalskbart er bare det du alene kan. *Effektiv:* STATUS.md + transkript koster null. Prosessregel, ikke mekanisme — og merket som det.

**Panel.** Fabel: STATUS.md + transkript nå; port-celle senere; «dagens `sign_statement` er ikke Kjetils ord» — sikkerhet **middels**. Astra (panel) **[it. 2]**: signert portkvittering kontrollert av eierstyrt port-celle, sikkerhet **middels**; STATUS.md er «utilstrekkelig som eneste bevis» fordi en tekstlinje ikke binder innholdet etter senere redigering — men «til løsningen virker, må dagens dokumenterte menneskebeslutning beskrives som manuell prosess». Det er det B4 gjør. Begge er enige om det viktigste: *bæreren som portes skal aldri kunne signere sin egen port grønn*, og agentutsagn ≠ din godkjenning (`AgentSignatureStatement.swift:353, :390`).

Astras krav til port-cellen tas inn i målformen: manifestet binder oppgave, port, beslutning, mål-/policyversjon, navngitte artefakter med digester **og forgjengerkvitteringer** (så G2 ikke kan registreres uten G1); verifikatoren kontrollerer forhåndsbetrodd godkjennernøkkel, domene, audience, payload, tidsrom og **engangsinnløsning**; innløsningsfristen skilles fra godkjenningens varighet (en godkjent artefakt trenger ikke ny godkjenning hvert døgn, men endrede artefakter gjør kjeden ubrukelig); `purpose_dev.py gates` blir konsument av samme kontrakt. `oneShot` i `GoalDefinition` er *ikke* innløsningsvern — motoren tester bare eventnavnet (`GoalEvaluationEngine.swift:232`).

**Hva du gjør.** Svar på §10 K1. Og: fortsett å si «G2 godkjent» med ord — det er porten.

---

## B5 — Avdrift: motorens hull lukkes som invarianter, og avdriftscellen sender én observasjon per baseline-kilde

**Beslutning.** Verken nytt felt (P5 a) eller nytt predikat (P5 b). **(d)** seks småendringer i `GoalEvaluationEngine.swift` uten skjemaendring, **pluss (c)** konsumentregelen. `at-risk` via generalisering av `statusPolicy`, ikke nye `value`-operatorer. Q7 (`≤`/`⊆`) lukkes: de testene er XCTester på artefaktet, ikke målpredikater.

**Hva det innebærer.**
I motoren: (1) predikat på udeklarert kilde → `unknown`, `missing: ["evidence-source:<id>(undeclared)"]` (i dag bygges `observationsBySource` av *alle* observasjoner men `evidence` bare av deklarerte, `GoalEvaluationEngine.swift:72, :77–93`, så et mål med `evidenceSources: []` kan bli `satisfied` med tom evidens — et artefakt som lyver); (2) `.missing`-observasjon behandles som manglende uansett verdi (`:110, :125`); (3) duplikat `sourceID` → `unknown`, aldri trap (`Dictionary(uniqueKeysWithValues:)`, `:72`); (4) tom `evidenceSources` med predikat → `unknown`; (5) ukjent predikat-kind → `unknown` (samme som B1); (6) `observedAt` mot `evaluatedAt` med `freshnessSeconds` → `stale` **beregnes**, ikke påstås (feltet deklareres i `GoalDefinition.swift:60` men leses aldri). De fem eksisterende testene deklarerer sine kilder og forblir grønne (`GoalEvaluationEngineTests.swift:77–80, :135–144, :157–160`).
I avdriftscellen: `evidenceSources` **genereres fra baselinen**, så deklarert = forventet ved konstruksjon; én observasjon per kilde; `denied` for 403, `error` for agent nede — begge gir `blocked` (`:110–123`), som er den ærlige tilstanden «ikke ro, ikke avdrift, stopp». Cellen beregner diffen og sender `labels: ["unchanged"|"widened"|"narrowed"]`; predikat `contains-label unchanged`. For `at-risk` framfor `active` generaliseres `statusPolicy.atRiskAfterFailures`/`missedAfterFailures` fra `networkPing` til alle evaluatorer (`:179–194`): cellen sender `consecutiveFailures` = påfølgende kjøringer med avdrift.
Rapporten viser per-kilde-raden **ved siden av** målstatusen — ellers skjuler én `blocked` kilde avdrift i de andre.

**Hvorfor.** *Robust:* hullene er i motoren, og en konsument kan ikke reparere et artefakt motoren har skrevet; invarianter kan ikke velges bort. Husets mønster er at deklarative felt på `GoalDefinition` ikke håndheves (`lifecycle`, `freshnessSeconds`, `requiredGrant`, `visibility`, `helperCells` er alle ulest) — en ny Bool som «må håndheves» er enda et felt å verifisere. *Effektiv:* seks småendringer i én fil. *Fleksibel:* `statusPolicy` for alle evaluatorer gir `at-risk` til alle kontinuerlige mål, ikke bare nettverk.

**Panel.** Fabel: (d)+(c), sikkerhet **høy**. Astra (panel) **[it. 2]**: (a) som obligatorisk streng modus for avdriftsmål, sikkerhet **høy** — men med samme motorfunn som Fabel (`.missing` med verdi stoppes ikke, `Dictionary(uniqueKeysWithValues:)` trapper på duplikat, `:72`, `:73`, `:110`). Uenigheten er formen, ikke innholdet: Astra vil ha en eksplisitt modus bundet til et eiergodkjent **kildemanifest**; Fabel vil ha ubetingede invarianter. **Valget står: invarianter** — Fabels argument om at deklarative felt på `GoalDefinition` historisk ikke håndheves veier tyngst (en modus som «må håndheves» er enda et felt å verifisere). Men Astras to skjerpinger tas inn: (1) **kildeidentitet, ikke antall** — `expectedSourceCount` alene er utilstrekkelig, to gale kilder kan ha riktig antall; derfor genereres `evidenceSources` fra baselinen med kildens *identitet og versjon*, og observasjonene bærer grant- og baseline-versjon. (2) **Diffen må sammenligne normaliserte rettigheter** (celle, keypath, RWXS, betingelser, utløp) — aldri `Grant.==`, som bare sammenligner keypath (`Grant.swift:7`). Og ro må være tids- og versjonsavgrenset: et gammelt «ingen avdrift» faller bort når kontrollfristen passeres eller grant-settet får ny versjon. Astras `atRiskWhen`-regel og Fabels generaliserte `statusPolicy` er samme ting; jeg tar `statusPolicy` fordi feltet finnes.

**Hva du gjør.** Ingenting.

---

## B6 — Tre relasjoner holdes atskilt: klassifikasjon, oppgavestruktur, composition

**Beslutning.** Klassifikasjonsforelder = `types` (→ `self-determination.data.*`, `access.audit.privacy`); oppgavestruktur = `partOf`/`parts` (→ denne PDD-ens rot og blader); composition = eksplisitte leaves i `Purpose.composition`. Fasetter = `purposes`-kanter til de samme Purpose-nodene, med fasettrollen erklært i eksportkontrakten. Fasett gir aldri autoritet (`PurposeBoundExternalAction.swift:721`).

**Hvorfor.** Astra (12.09): én kanttype bevarer ikke både klassifikasjon og oppgavestruktur; FORMAALSSPEC §1 henger grenene under ulike globale formål *og* krever alle fem i roten. Fabel og Astra enige om fasetter som `purposes`-kanter.

**Hva du gjør.** Ingenting.

---

## B7 — Hvor arbeidet bor

**Beslutning (forslag — organisatorisk, ditt valg).** Fase A (kontrakt + B2) og B (integritet i `Perspective`) og C (bro/projeksjon/CLI) legges inn i **`PDD_formaalsregister-som-graf`** som nye arbeidspakker — den står ved G2, har valgt CellProtocol som hjem og én motor, og eier allerede `bro`/`celle`/`en-kilde`. Fase D (grant-celle, baseline-celle, bevis, avdrift) og E (avvist steg → challenge) er **denne PDD-ens** blader og blir her. Fase F (metoden i celler: lærdomsregister, pakker, porter) blir egen PDD når A–C har landet. B1 (`goalDefinition`) er så liten at den går som **første arbeidspakke her**, fordi du pekte på den som kjernen.

**Panel.** Astra (12.09): format- og semantikkvalg (A) kan ikke være «senere konsekvenser» av broen — de går foran. Det er de nå.

**Hva du gjør.** Si ja eller pek på en annen deling (§10 K2).

---

## B8 — Book 36

**Beslutning.** Godkjennes **ikke** i dagens form. Etter B2 skrives den om til den normative kontrakten for composition — med testvektorene som bilag og begge implementasjoners forskjeller synlige til de er borte. Book 36 §1 får en rettelse: CellBase hadde `PurposeComposition` siden 25.06.

**Hva du gjør.** Ingenting nå; du godkjenner den omskrevne når den kommer.

---

## B9 — To celler, og hvem som får skrive i dem

**Beslutning (din, 12.09, bekreftet her).** Grantene i én celle du eier i agenten; baselinen i en annen. Med B3 presisert: grant-cellen er kilden til `Agreement`-grantene beviset bærer; baseline-cellen kan bare skrives av operatørnøkkelen — aldri av et agentutstedt bevis, og aldri av agenten selv. Det er det som hindrer at agenten hever sitt eget tak.

---

## 10. Spørsmål til deg — bare de som endrer noe

**K1 — Er agentens ord ditt ord?** Agenten signerer med sin egen identitet, ikke med din parrede operatørnøkkel (`AgentSignatureStatement.swift:371–377`). De to er lenket til én entitet gjennom entitetslenken. Spørsmålet avgjør to ting: (a) hvem som signerer grant-kontrakten i B3 — agentidentiteten (effektivt, men da kan alt agenten kan kalles til å gjøre også utstede bevis) eller operatørnøkkelen via en bekreftelse du ser (robust, men krever at du er til stede ved hver utstedelse, eller godkjenner en stående fullmakt med tak); (b) om en port-godkjenning noen gang kan være agentsignert. *Mitt forslag:* agentidentiteten utsteder bevis **innenfor** det grant-cellen tillater (den er din, og bare din nøkkel kan utvide den — B9), men port-godkjenninger krever din nøkkel. Da er «to nøkler» fortsatt to.

**K1, skjerpet [it. 2]:** `GeneralCell` godtar en kontrakt bare når *utsteder = cellens eier* (`GeneralCell.swift:2048`). Så spørsmålet er konkret: **hvem eier scaffold-cellene dine — din operatøridentitet, eller entiteten (slik at agentidentiteten via entitetslenken også er eier)?** Er svaret operatøridentiteten, kan agenten ikke utstede beviset alene; da må din nøkkel signere gjennom en bekreftelse du ser (menylinjen), eller du gir en stående fullmakt med tak som selv er en signert kontrakt. Jeg kan få Codex til å lese eierskapsmodellen i `GeneralCell` og entitetslenkens virkning før du svarer, hvis du vil.

**K2 — Deling av arbeidet (B7):** A–C inn i graf-PDD-en, D–E her, F senere som egen PDD?

**K3 — Endre oppførselen til eksisterende Swift-composition (B2)?** Fem tester i `PurposeCompositionTests.swift` får ny forventet oppførsel. Begge rådgiverne fant ingen produksjonskonsument (bare en benchmark med syntetiske data). Astra foretrekker likevel en parallell type (c); jeg foreslår (a). Ditt ord.

**K4 — Blokkert gren i `anyOf` [it. 2]:** Book 36 sier både «hvilken som helst holder» (§3.3) og «et blokkert barn hindrer grønt» (§4). *Mitt forslag:* i `anyOf`/`firstOf` blokkerer et blokkert barn **ikke** når minst `min` andre barn er grønne — men det blokkerte barnet **rapporteres alltid** i resultatet, aldri stille; i `allOf`/`sequence` blokkerer det. Da stanser ikke et SSH-avslag en verifisert statusflate, og ingenting ser roligere ut enn det er. Alternativet er Book 36 §4 bokstavelig (konservativt: alt stopper).

---

## 11. Revisjonslogg

| It. | Dato | Hva | Hvem |
|---|---|---|---|
| 1 | 2026-09-13 | B1–B9 skrevet etter Fabels panelsvar (2 448 ord, `panel/FABEL_SVAR.md`) og Astras keypath-motsvar fra graf-PDD-en. Astras panelsvar venter i køen | Losen |
| 2 | 2026-09-14 | Astras panelsvar tatt inn (`panel/ASTRA_SVAR.md`, 136 088 tokens hos Codex). Enighet på B1, B3, B4 (målform), B5 (innhold); uenighet på B2 — begge standpunkt står, valget (a) begrunnet mot kriteriene. Nytt: `Contract.signed` som gjenbrukstype (B3); utsteder må være cellens eier → K1 skjerpet; revisjonsloggen registrerer bare avslag → `audit-names-the-proof` må bygges; Book 36 selvmotsigende om `anyOf`/`blocked` → K4; kildeidentitet og normalisert rettighetsdiff i B5; port-manifest med forgjengerkvitteringer og engangsinnløsning i B4 | Losen |
