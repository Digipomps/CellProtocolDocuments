# BRIEF — rådgiverpanel: fem uavklarte valg for «formålsdekomponeringen over på PerspectiveNode»

Mappe: `CellProtocolDocuments/Deliverables/PDD_mcp-tilgangsbevis_2026-09-12/panel/` · 2026-09-13 · Losen
Kjetils instruks, ordrett: «goalDefinition er kjernen her så det må inn i dekodingen. Ta med Astras innvendinger - om du syns spørsmålene er uavklart bruk rådgiverpanel. Gå etter effektiv, fleksibel og robust løsning.»

## 1. Formål med panelet

Velge mellom konkrete løsningsformer på fem punkter der analysen (`../PERSPECTIVENODE_KONSEKVENS.md`, iterasjon 2) og Astras gjennomgang (`../handoff/CODEX_REVIEW_PERSPECTIVENODE.md`) ikke landet, eller der valget har varige konsekvenser for CellBase. Kriteriene er Kjetils: **effektiv** (minst nytt, mest gjenbruk, kort vei til noe som kjører), **fleksibel** (tåler neste bruk uten omskriving), **robust** (feiler lukket, lar seg ikke misforstå, etterprøvbar på artefaktet).

Panelet **avgjør ikke**. Det gir Losen to uavhengige standpunkt med belegg; Losen skriver `../BESLUTNINGER.md`; Kjetil kan overprøve.

## 2. Faktagrunnlag (lest i kode; stier relative til `HAVEN/`)

- `Purpose: PerspectiveNodeImpl` med `goal: CellConfiguration?`, `helperCells: [CellConfiguration]`, `composition: PurposeComposition?`, egen `init(from:)` og `encode(to:)`; CodingKeys har **ikke** `goalDefinition` — `CellProtocol/Sources/CellBase/PurposeAndInterest/Purpose.swift:13–100`.
- `GoalDefinition` (`haven.goal-definition.v1`) har selv `purposeRef`, `helperCells: [GoalHelperCellRef]`, `evidenceSources`, `predicate`, `lifecycle`, `evaluatorKind` — `GoalDefinition.swift:197–260`. `fromPerspectiveFields` lager `kind: evidence-rule / operation: satisfies` som motoren ikke har gren for (`:259`, `GoalEvaluationEngine.swift:247`).
- `GoalEvaluationEngine`: innsendte observasjoner; predikater `all/any/contains-label/event-seen/value(strenglikhet, contains)/network-ping`; manglende/ukjent predikat → `active`; manglende deklarert kilde → `unknown`; `denied/error` → `blocked`; tom kildeliste → tom evidens; `lifecycle/requiredGrant/visibility/helperCells/freshnessSeconds` brukes ikke — `GoalEvaluationEngine.swift:66–263`. Adapter: `CellProtocol/Sources/CellBase/Cells/Purpose/GoalEvaluationCell.swift` (`goal.evaluate`, lagrer siste, emitter flow).
- `PurposeComposition` (Swift): `purpose|allOf|anyOf|sequence|atLeast`; blad = **siste suksess** (`PurposeComposition.swift:38`); `partial/unsatisfied/satisfied`; `sequence` sjekker fullføringstid, ikke start (`:319`); tom `allOf`/`sequence` → `satisfied` (`:233`, `:303`); `atLeast ≤ 0` → `satisfied` (`:363`). Tester: `CellProtocol/Tests/CellBaseTests/PurposeCompositionTests.swift` (5 tester).
- Book 36 / `CellProtocolDocuments/Tools/PurposePackages/purpose_composition.py`: `allOf/sequence/anyOf(min)/firstOf/invariant(over)` som nodeegenskap + `childOrder`; tilstander `green/red/blocked/unverified`; blad = siste måling og siste forsøk (`:205`); `blocked` propageres før disjunksjon (`:219`); `sequence` sjekker tilstand før hvert forsøk (`:288`); `firstOf` registrerer gren (`:242`); `invariant` måles før/etter hvert steg (`:306`); kjøringslogg `attempts/measurements/reports/opinions` (Book 34-skillet måling/slutning/mening).
- Autorisasjon: `CellAuthorization.swift:16` tar celle+keypath+operasjon+requester; **`ownerProof` behandles før kontraktgrants** og gir bred eiertilgang (`:194`, `:228`, `:258`); `GeneralCell.getEmitterWithLabel` krever `-w--` også for GET (`GeneralCell.swift:2429`); traverserende GET bruker `try?` og kan falle til bredere rotlesing (`:1893`); `CellProtocolClient` kaller Meddle direkte forbi resolverens preflight (`CellScaffold/Sources/ScaffoldKit/CellProtocolClient.swift:122`).
- Challenge: `AdmissionChallengePayload` (`CellProtocol/Sources/CellBase/Agreement/AdmissionContracts.swift:47`), `connect.challenge` i attach/admit/signContract (`GeneralCell.swift:542, :660, :977`), `retryAdmissionSession` (`:569`). Gjelder tilkobling, ikke avvist enkeltoperasjon.
- Signering i agenten: `HavenAgentD::Sources/HavenAgentRuntime/AgentSignatureStatement.swift` — `AgentSignStatementRequest{purposeRef, audience{entityRef, publicKeyBase64URL}, payloadSHA256Base64URL, expiresAt, nonce}`, `maxValiditySeconds = 86_400`. Gjensidig signert lenke: `AgentEntityLinkContract{domain_a, pubkey_a, domain_b, pubkey_b, scope, revocation}` med `verifyMutualSignatures()`. Grant-allowliste i config: `RemoteIntentVerifier.swift::TrustedRemoteIntentIssuer{issuerID, publicSigningKeyBase64, allowedTopics, allowedActionIDs}`.
- Kjetils beslutninger (2026-09-12): grantene i en celle han eier; keypath er datareferanse uten autoritet — hver celle avgjør ved traversering (tillat/avvis/Agreement challenge); brukeren må ha verktøy (varslingssenter) for å løse en challenge; baselinen i en annen celle enn grantene; `goalDefinition` skal inn i `Purpose`-dekodingen.

## 3. Spørsmålene

Svar på alle fem, i rekkefølge, overskrift per spørsmål. Ta stilling — «det avhenger» uten et forslag teller ikke. Merk hver påstand `[belagt: fil:linje]`, `[vurdering]` eller `[usikker]`.

### P1 — Composition: hvilken semantikk skal være normativ, og tåler vi å endre Swift?

To modeller, samme navn, ulik oppførsel (§3.1 i analysen). Alternativer:
- **(a)** Swift `PurposeComposition` utvides med `firstOf([…])`, `invariant(over:)` og en `blocked`-tilstand, **og** evalueringen endres til Book 36-semantikken: blad = siste post (ikke siste suksess), `blocked` som egen tilstand før disjunksjon, `sequence` krever at neste ikke *startes* før forrige er grønt, tomme uttrykk avvises, `atLeast` krever 1…n. Python blir en portering med delte testvektorer. Fem eksisterende Swift-tester endres.
- **(b)** Book 36 snevres til Swift-semantikken; metoden mister `blocked ≠ red`, sekvensstart-regelen og `invariant`.
- **(c)** To lag: Swift beholder dagens «resolution»-semantikk for runtime-celler; PDD-metoden får en egen `VerificationComposition` (Book 36) som *wrapper* og mapper ned til Swift-typen for lagring, med eksplisitt tapstabell.
Vurder mot kriteriene. Er det noe i Swift-semantikken (siste-suksess, tom = satisfied) som *runtime-celler* faktisk trenger, eller er det tilfeldig?

### P2 — `goalDefinition` inn i `Purpose`: hvilken form?

Kjetil har bestemt *at*. Spørsmålet er *hvordan*:
- inline `goalDefinition: GoalDefinition?` (selvbærende Purpose-JSON) **eller** `goalRefs: [String]` med oppslag (ett mål delt av flere formål, mål kan endres uten å røre formålet) **eller** begge;
- skal validatoren kreve `goalDefinition.purposeRef == purpose.reference`?
- hva betyr `Purpose.goal: CellConfiguration?` ved siden av — og hva gjør vi med **to** helper-lister (`Purpose.helperCells: [CellConfiguration]` og `GoalDefinition.helperCells: [GoalHelperCellRef]`)?
- dekoding av eldre JSON uten feltet må fortsatt virke (tilbakekompatibilitet), og `fromPerspectiveFields` må rettes så den ikke lager predikater motoren ikke kan kjøre.

### P3 — Beviset: bærernøkkel med grant, eller et token som «er» Kjetil?

- **A (impersonering):** agenten signerer et utsagn som lar bæreren (Claude/Codex) opptre *som* Kjetils identitet, innsnevret av grant-cellen. Cellens `ownerProof`-vei ville slippe bæreren bredt inn med mindre det legges inn en regel «agentutstedt bevis teller aldri som ownerProof».
- **B (delegert nøkkel):** bæreren har **egen** nøkkel. Agenten utsteder — fra Kjetils nøkkel — en **signert grant-kontrakt** til bærerens nøkkel: (celle, datareferanse, operasjon, utløp, grant-digest, nonce). Cellen autoriserer via den eksisterende grant-/kontraktveien (`CellAuthorization.swift:228`); `ownerProof` matcher aldri; revisjonsloggen navngir bæreren av seg selv.
Hvilken er mest robust, fleksibel, effektiv? Hva mangler for B (nøkkelprovisjonering for bæreren, kontrakttype — `AgentEntityLinkContract` er gjensidig og bred, `TrustedRemoteIntentIssuer` ligger i config; revokasjon)? Finnes det en grant-kontrakttype i CellBase som B kan gjenbruke direkte? Svar med sti.

### P4 — Porter (G1/G2/G3) som mål: hvordan bindes Kjetils ord?

Forslag: en godkjenning = Kjetils **signerte utsagn** (`AgentSignatureStatement`, formål `personal.identity.sign.statement`, payload = digest av artefaktene som godkjennes) → `GoalObservation` `event-seen: gate.approved` til et `GoalDefinition(evaluatorKind: .humanConfirmation, lifecycle: .oneShot)`. Motoren verifiserer ikke signaturer — hvor skal verifiseringen ligge (GoalEvaluationCell? en port-celle? `purpose_dev.py gates`)? Hvordan uttrykkes portrekkefølgen (G1 før G2; G1-GUI før G2 for GUI) — som `sequence` i composition, eller som predikat? Er dette robust, eller er «Kjetil skriver `godkjent <dato>` i STATUS.md» faktisk bedre på kriteriene, i dag?

### P5 — Avdrift: hvordan bevises ro?

Motoren gir tom evidens ved tom kildeliste, `allSatisfy` på tom liste er sann, og predikatavvik gir `active`, ikke `at-risk`. Alternativer for å hindre falsk ro:
- **(a)** nytt felt på `GoalDefinition`: `requireAllDeclaredSourcesFresh: Bool` + `expectedSourceCount: Int?`, håndhevet i motoren;
- **(b)** nytt predikat-kind `sources-complete` i `GoalPredicate`, evaluert som resten;
- **(c)** ingen motorendring: konsumenten (avdriftscellen) sjekker selv før den kaller motoren, og sender `status: .missing` for kilder den ikke fikk lest.
Og: `at-risk` må settes av et eksplisitt predikat på «grant-sett ≠ baseline». Trenger `value`-predikatet `≤`/`⊆`/numerisk (Q7 i analysen), eller løses avdrift med `event-seen` fra en forhåndsberegnet diff?

## 4. Format på svaret

1. Tre setninger øverst: hva du er sikrest på, hva du er mest usikker på, hva Losen bør spørre Kjetil om.
2. P1–P5 som egne seksjoner, hvert med: **valg**, **hvorfor (mot de tre kriteriene)**, **hva som må bygges**, **hva som kan gå galt**.
3. Avslutt med én tabell: P | ditt valg | sikkerhet (høy/middels/lav).
4. Norsk. 1 500–2 500 ord. Ingen kode, ingen planer, ingen andre filer.
