# Formålsspesifikasjon — tillitspakke agentflaate

Oppgavemappe: `PDD_tillitspakke-agentflaate_2026-09-08` · Opprettet 2026-09-08 · Iterasjon 2 (ikke godkjent — Q1–Q5 besvart, venter på G1-ordet)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Er det en ide å ha muligheten for å generere en tillitspakke brukeren kan se igjennom før brukeren setter opp og konfigurerer en eller en flåte med AIAgenter slik at det er tydelig å se hvilke modeller er i ferd med å bli brukt, linker til instruksjoner og en liste med Grants cellene har så brukeren både kan gjøre seg opp en mening først og eventuelt justere og å verifisere at tillitspakken ble overhold etterpå. Det kan f.eks være at en AIGatewayCell har rettigheter til å bruke en fetch celle - med eller uten credentials - og bare har tilgang til å lese, evt. på en whitelist av sites. Dette er begrensninger språkmodellen inne i AIGatewayCellen ikke kan gå utenfor. (Om ikke selve modellen tillater det der den kjører - men det må den instrueres til å ikke gjøre - eller vi kjører modellen selv)
>
> Dekomponer nå

Bakgrunn: `Deliverables/Formaal_Celler_Agentstyring_Vurdering_2026-09-08/VURDERING.md` §7 (P0 «ramme-objekt», P1 «signert kvittering») og §11 (denne ideen, vurdert). Astras «oppgaveprofil» (M3) er maskinobjektet; tillitspakken er den menneskelesbare projeksjonen av det samme.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Det finnes en fetch-celle | **retrieved** — `cell:///WebFetch` (`WebFetchCell: GeneralCell`), https-only som default, `maxBytes` 256 000, timeout 15 s, `web.fetch`/`web.setURLDraft`/`web.clear` | `CellScaffold/Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift:11–19, 401–541` |
| Fetch-cellen kan begrenses til whitelist av sider | **contradicted for i dag** — ingen host-/domeneliste i cellen; bare skjema-sjekk (`https_required`). Whitelist må bygges (C1) | samme fil, 512–517 |
| Fetch «med eller uten credentials» | **retrieved, delvis** — `cell:///ScopedCredential` finnes (eier-scopede hemmeligheter, redigert metadata i state); WebFetch bruker i dag *ingen* credential. Kobling må bygges (C1) | `WebKnowledgeCells.swift:35–41, 191–310` |
| Grants per celle finnes som liste | **retrieved** — hver `GeneralCell` har ett `agreementTemplate` med `addGrant("rw--", for: keypath)`; WebFetch: `r---` på state-keypaths, `rw--` på `web.fetch`, `web.setURLDraft`, `web.clear` | `WebKnowledgeCells.swift:444–448`; `Purpose_Bound_External_Action_Contract_2026-08-03/A4_AUTHORITY_ISOLATION_DECISION.md` |
| Utstedte Contracts kan leses tilbake verifisert | **retrieved** — `signedAgreementEntity.commit` i EntityAnchor med read-after-write-kvittering; Entity Studio viser bare re-lest, verifisert projeksjon | `Book/04_Agreements_Contracts.md` §9, §11 |
| Effekt-ceilings (destinasjoner, dataklasser, execute/storage/disclosure) finnes som objekt | **retrieved** — `CellExecutionPolicy` med `effectCeilings`, `Bindings` (config/policy/taxonomy-digest), `Provenance` | `CellProtocol/Sources/CellBase/Agreement/PurposeBoundExternalAction.swift:218–260`; `CellScaffold/…/AIGatewayPurposePolicy.swift:86–121` |
| Modellene som skal brukes kan leses ut | **retrieved** — `AIGatewayProviderRoute` (providerID, model, baseURL, apiPath) i forespørselen; seed-katalog `model_provider_catalog_v0.json` (offentlige metadata, aldri nøkler) | `AIGatewayPurposePolicy.swift:229–246`; `Book/model_provider_catalog_v0.json`; `Book/24_Model_Providers_Credentials_And_Selection.md` |
| Instruksjoner kan lenkes | **retrieved, delvis** — `AIGatewayInvokeRequest.systemPrompt` finnes (dataklasse `system-instruction`); persona-celle er besluttet, ikke levert. «Lenke» = keypath + digest, ikke tekst i pakken | `AIGatewayPurposePolicy.swift:31–33`; `CellScaffold/Deliverables/PDD_radgiverpanel-og-persona_2026-09-05/STATUS.md` |
| Modellen kan ikke gå utenfor cellens begrensninger | **retrieved for A4-banen** — modelloutput er proposal; policy leser wire-felt; `no-tools` i `planDigest`; adapterne sender aldri `tools` til leverandør (eneste treff på «tools» i `AIGatewaySupport.swift` er en grense for `toolPolicy`) | `AIGatewayPurposePolicy.swift:20–28`; `AIGatewaySupport.swift:321`; `VURDERING.md` §4 |
| «Modellen må instrueres til ikke å gjøre det» | **contradicted som mekanisme** — instruksjon er den svake spaken; leverandørverktøy holdes av ved at forespørselen aldri slår dem på, og det er digest-bundet (A3). Egen kjøring fjerner kanalen | `VURDERING.md` §11 |
| Verifisere etterpå mot kvitteringer | **retrieved, med hull** — `ActionDecisionReceipt` bærer alle bindings-digester og decision/execution-status, men er **usignert** (ingen signaturfelt) | `PurposeBoundExternalAction.swift:516–545` |
| Det finnes et tillitspakke-mønster i HAVEN | **retrieved** — `PersonalDataTrustPackageCell` (`externalRequests` med method/url/purpose, retention, entityStorage, disclosure; `replaceProposal` med `confirm`) — data-siden av samme idé | `CellScaffold/Sources/App/Cells/PersonalDataTrustPackage/PersonalDataTrustPackageCell.swift:15–30, 387–460` |
| Tillitspakke er evidens, ikke myndighet | **retrieved** — A1 semantisk lås 6 (T10 trust theater) | `Purpose_Bound_External_Action_Contract_2026-08-03/README.md` |
| AIGateway kan løse opp hemmeligheter i dag | **contradicted** — `resolve(alias:requester:)` gir `nil` uten `HAVEN_CREDENTIAL_MASTER_KEY`; ingen live modellkjøring mulig nå (kreditt) | `PDD_radgiverpanel-og-persona_2026-09-05/STATUS.md` D1/D5 |
| Porthole-preview av CellScaffold-flater er mulig | **recalled** — må verifiseres før P1-GUI (jf. `lesson.scaffold-without-porthole-host-has-no-preview`) | — |

## 1. Formålstre

Rot-prinsipp fra Book 23: `purpose://root` — alle mennesker er like mye verdt; ingen aksepterte formål krever skjult profilering eller uforklart myndighet. Forelder i taksonomien: `purpose://access.audit.privacy` (governance), med `purpose://self-determination.data.verifiability` («verifiability instead of trust», candidate) og `purpose://knowledge.explain-policy` (draft) som beslektede noder.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.tillitspakke-agentflaate.root | Brukeren ser, justerer og etterprøver agentflåtens myndighet | purpose://access.audit.privacy | **Før** oppsett finnes én generert pakke som viser, per celle og transitivt for flåten, hvilke modeller, instruksjons-referanser, Grants og effekt-ceilings som vil gjelde; brukeren kan snevre inn før noe kjører; **etter** kjøring viser en diff planlagt/observert null avvik eller lister hvert avvik. Ingen del av pakken gir myndighet. | test.tp.e2e | candidate |
| purpose://candidate.tillitspakke-agentflaate.projeksjon | Pakken er en projeksjon av det som håndheves | root | Pakke-JSON genereres fra faktiske kilder — `agreementTemplate` per celle, utstedte Contracts til flåtens identiteter (EntityAnchor), `CellExecutionPolicy.effectCeilings`, `AIGatewayProviderRoute` (provider/model/baseURL), instruksjons-keypath + digest — og bærer én pakke-digest over alt. Regenerering med uendrede kilder gir identisk digest; én endret Grant gir ny digest. Aldri nøkler, aldri prompt-tekst i pakken. | test.tp.projeksjon-deterministisk, test.tp.ingen-hemmeligheter | candidate |
| purpose://candidate.tillitspakke-agentflaate.rekkevidde | Transitiv rekkevidde er synlig | root | Pakken viser grafen «hvem kan kalle hvem med hvilke Grants» og summert rekkevidde per agent: destinasjoner, credentials ja/nei, lese/skrive/utføre/lagre. For fixture-flåten AIGateway→WebFetch viser pakken «`r---`/`--x-` på `web.fetch`, uten credentials, domener: ‹liste›». | test.tp.rekkevidde-matcher-kontrakter | candidate |
| purpose://candidate.tillitspakke-agentflaate.leverandorverktoy | Leverandørverktøy er synlig av | root | Per modellrute viser pakken «leverandørverktøy (web search, kodekjøring, computer use): av», og fraværet er bundet i forespørselens payload-digest slik at kvitteringen kan bekrefte det. | test.tp.provider-tools-off | candidate |
| purpose://candidate.tillitspakke-agentflaate.justering | Brukeren snevrer inn før oppsett | root | Fra pakken kan eieren fjerne en Grant, slå av credentials, snevre whitelist eller bytte modellrute; endringen lagres som **data ved siden av templaten** (Q2: ceiling/condition per celle-instans i EntityAnchor; Swift-templaten er taket) *før* noen celle starter, og gir ny pakke-digest. Pakken kan bare **innsnevre** — aldri legge til rettigheter templaten ikke har. | test.tp.justering-innsnevrer, test.tp.justering-kan-ikke-utvide | candidate |
| purpose://candidate.tillitspakke-agentflaate.godkjenning | Eierens ja er bundet til pakke-digest | root | Eieren av scaffoldet signerer pakke-digesten (Q1/Q5: v1 = ett scaffold, eieren godkjenner; issuer-signert, subject-bundet snapshot som Book 04 §8; motpart-godkjenning er egen node senere); flåten starter bare når gjeldende policy-digest matcher en godkjent pakke-digest; avvik → `denied` med typed grunn, aldri stille fallback. | test.tp.start-uten-godkjent-digest-nektes | candidate |
| purpose://candidate.tillitspakke-agentflaate.webfetch-ceiling | Fetch-cellen håndhever whitelist, credentials og lese-bare | root | `cell:///WebFetch` får host-whitelist med **mønstre** (Q4: `*.example.org` matcher subdomener, ikke `example.org` selv med mindre begge står; eksakt vert uten `*` matcher bare seg selv; port må matche om oppgitt, ellers bare 443; bare `https`), credentials-eller-ikke (alias fra `ScopedCredential` bare når Grant tillater) og lese-bare (kun GET, ingen body) som ceiling/condition **i cellen**, uavhengig av hvem som kaller og av hva modellen skriver. Utenfor whitelist → `denied` før nettverk; **redirect** til vert utenfor whitelist → avbrutt og `denied`; credential uten rett → `denied` før oppslag. Whitelisten er en del av pakke-digesten. | test.tp.webfetch-whitelist-negativ, test.tp.webfetch-monster-kanttilfeller, test.tp.webfetch-redirect-negativ, test.tp.webfetch-credential-negativ | candidate |
| purpose://candidate.tillitspakke-agentflaate.skal-ikke.modell-utvider | Skal ikke: modellen kan utvide noe | root · polarity: prohibited | Ingenting modellen produserer (tekst, JSON, «tool call»-lignende tekst, injisert instruks) kan legge til destinasjon, credential, Grant eller slå på leverandørverktøy; policy og ceiling leser bare validerte wire-felt og data eieren har lagret. | test.tp.injeksjon-endrer-ingenting | candidate |
| purpose://candidate.tillitspakke-agentflaate.skal-ikke.pakke-gir-rett | Skal ikke: pakken gir myndighet | root · polarity: prohibited | En pakke som lister en rett cellen ikke har i template/Contract, gir ikke retten; cellen avviser som før (A1 lås 6: trust package er evidens). | test.tp.pakke-uten-contract-nektes | candidate |
| purpose://candidate.tillitspakke-agentflaate.etterproving | Planlagt mot observert | root | Hver effekt-kvittering bærer bindings-digestene; «etter»-visningen diff-er kvitteringer mot godkjent pakke-digest per agent og viser 0 avvik, eller lister hvert avvik med type (ny destinasjon / credential løst opp / dataklasse utenfor / verktøy på / ukjent policy-versjon). Et syntetisk brudd vises. | test.tp.diff-viser-brudd | candidate |
| purpose://candidate.tillitspakke-agentflaate.signert-kvittering | Kvitteringen kan vises til andre | etterproving | `ActionDecisionReceipt` (og effekt-kvittering) signeres av cellens/scaffoldens identitet; verifisering feiler på manipulert kvittering. Uten dette er «overholdt» bare lokalt lesbart (VURDERING §7 P1). | test.tp.receipt-signatur | candidate |
| purpose://gui.expectation-agreed-before-build → «før»-flate | «Før»-flaten: pakken som skeleton | pkg.std.gui-surface | Flate med celle-liste, rekkevidde-graf/tabell, modellruter, instruksjonslenker (keypath), justeringshandlinger og «Godkjenn pakke». Tilstander: tom (ingen flåte), fylt (fixture-flåte), feil (policy-digest avviker). | test.gui.reference-image-exists, test.gui.parity, test.skeleton.purpose-actions-reachable | candidate |
| purpose://gui.expectation-agreed-before-build → «etter»-flate | «Etter»-flaten: diff og brudd | pkg.std.gui-surface | Flate med planlagt/observert per agent, avviksliste, siste kvitteringer med signaturstatus. Tilstander: ingen avvik, brudd. | test.gui.reference-image-exists, test.gui.parity | candidate |

Utenfor treet (bevisst): generell tool-løkke fra modell til celler (VURDERING §7 P0 for generell bane — egen PDD); per-Grant purpose V2; flåte over bridge/scaffold-grenser (v1 = ett scaffold); persona-celle (egen PDD); innholdsmoderering; bevis for hva leverandøren beholder.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en agent-orkestrator og ikke en tool-løkke. Pakken beskriver og begrenser myndighet; den starter ikke jobber og velger ikke handlinger.
- Ikke en ny kilde til rettigheter. Alt pakken viser må finnes som template/Contract/ceiling; pakken kan bare snevre inn (lesson.purpose-never-grants-rights, A1 lås 6).
- Ikke innholdskontroll. En tillatt fetch mot en whitelistet side kan fortsatt gi dårlig innhold; det er utenfor.
- Ikke bevis for leverandørens oppførsel (retention, trening). Pakken beviser hva *vi* sendte og hvor, ikke hva de gjorde.
- Ikke flåte over bridge i v1. Første versjon er én scaffold (CellScaffold) med fixture-flåten AIGateway + WebFetch + ScopedCredential.
- Ikke persona-/instruksjonsredigering. Pakken *lenker* til instruksjons-keypath med digest; redigering skjer der instruksjonen bor.

Kapabiliteter og avhengigheter oppgaven bygger på (hver med kilde og hva den ikke dekker):
| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| `GeneralCell.agreementTemplate` med Grants per keypath | `CellProtocol/Sources/CellBase/Cells/GeneralCell/GeneralCell.swift`; `WebKnowledgeCells.swift:444–448` | Templaten er definert i Swift ved init; ingen data-lagret innsnevring per instans i dag → «justering» må lagre ceilings som data ved siden av templaten (§6 Q3) | ja |
| EntityAnchor `signedAgreementEntity.commit` + verifisert re-lesing | `Book/04_Agreements_Contracts.md` §9, §11; `CellProtocol/Sources/CellApple/Cells/EntityAnchorCell.swift` | Issuer-signert, subject-bundet — ikke bilateral. Godkjenning av pakke = eierens snapshot over pakke-digest | ja |
| `CellExecutionPolicy` / `effectCeilings` / `PurposeActionBindings` / `ActionDecisionReceipt` | `PurposeBoundExternalAction.swift:218–545` | Bare brukt av `PurposeBoundAIGateway` i dag; WebFetch har ingen ceiling-objekt; receipt usignert | ja |
| `cell:///WebFetch` | `WebKnowledgeCells.swift:401–541` | https-only, 256 KB, 15 s; **ingen whitelist, ingen credentials**; `web.fetch` er `rw--` i templaten | ja |
| `cell:///ScopedCredential` + AIGateway `resolve(alias:requester:)` | `WebKnowledgeCells.swift:35–41, 293–310`; `AIGatewaySupport.swift:414–460` | Krever `HAVEN_CREDENTIAL_MASTER_KEY` for å løse opp (D1 i rådgiverpanel-PDD) — uten den er «med credentials» bare testbar med fixture-store | ja for C1-credential-test |
| Provider-adaptere sender aldri `tools` | `AIGatewaySupport.swift` (eneste «tools»-treff: linje 321, grense for toolPolicy) | Gjelder dagens adaptere; må låses med test så en fremtidig adapter ikke åpner kanalen | ja |
| `PersonalDataTrustPackageCell` (mønster: proposal → confirm → state) | `PersonalDataTrustPackageCell.swift:15–30, 387–460` | Data-siden; agent-pakken gjenbruker mønsteret, ikke cellen | nei (referanse) |
| Modellkatalog (offentlige metadata) | `Book/model_provider_catalog_v0.json`, `Book/24_…` | Seed; ingen nøkler; ruten i pakken tas fra faktisk `AIGatewayProviderRoute`, katalogen gir bare navn/lenke | nei |
| Explore-kontrakter for keypaths (så «instruksjonslenke» kan valideres) | `Book/22_Explore_Contracts_For_Skeleton_Authoring.md`; `Tools/Explore/skeleton_explore_validator.py` | Validerer at keypath finnes, ikke at innholdet er en instruksjon | ja for GUI-validering |
| Porthole-preview av CellScaffold-skeleton | `cellconfiguration-skeleton-authoring` (skill) | **recalled** — verifiser vert før P1-GUI; ellers mockup med eksplisitt liste (lesson.scaffold-without-porthole-host-has-no-preview) | ja for G1-GUI |
| Live modellkjøring for ekte kvitteringer | `PDD_radgiverpanel-og-persona_2026-09-05/STATUS.md` D5 | Ingen kreditt/nøkkel nå; «etter»-testen kjøres mot syntetiske kvitteringer (fixtures) til det finnes; A4-banen utelukker lokale modeller | nei for v1 (fixtures), ja for ekte e2e |

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2.
**GUI-oppgave:** hver flate og hver viktig tilstand (tom, fylt, feil) må ha et rendret bilde i `images/` som Kjetil har godkjent før G1-GUI. Porthole-preview av skeleton-JSON når formatet tillater det; ellers mockup med eksplisitt liste over hva dagens skeleton ikke kan rendre.
| Leveranse | Type (bilde / fil / testutdata / kjørende flate) | Hvor | Referanse (images/…-v1.png osv.) | Godkjent |
|---|---|---|---|---|
| «Før»-flate, tom (ingen flåte konfigurert) | bilde | `images/` | `images/tillitspakke-for-tom-v1.png` | nei |
| «Før»-flate, fylt: fixture-flåte AIGateway → WebFetch (uten credentials, whitelist 3 domener) + ScopedCredential; modellrute; instruksjonslenke; rekkevidde-tabell; justeringshandlinger; «Godkjenn pakke» | bilde | `images/` | `images/tillitspakke-for-fylt-v1.png` | nei |
| «Før»-flate, feil: gjeldende policy-digest ≠ godkjent pakke-digest | bilde | `images/` | `images/tillitspakke-for-feil-v1.png` | nei |
| «Etter»-flate, ingen avvik | bilde | `images/` | `images/tillitspakke-etter-ok-v1.png` | nei |
| «Etter»-flate, brudd (syntetisk: fetch utenfor whitelist + credential løst opp) | bilde | `images/` | `images/tillitspakke-etter-brudd-v1.png` | nei |
| Skeleton-/CellConfiguration-JSON bildene er rendret fra (eller `images/README.md` som sier «mockup» og hva skeleton ikke kan) | fil | `skeleton/` | — | nei |
| Kontrakt for pakke-cellen: keypaths, pakke-skjema, fixtures (positiv/negativ) | fil | `Book/agent_trust_package_contract_v0.json` + `contract/` | — | nei |
| Generert pakke for fixture-flåten (JSON) med pakke-digest — og en regenerert kopi med identisk digest | fil + testutdata | `contract/fixtures/fleet-webfetch.package.json`, `TESTRESULT.md#projeksjon` | — | nei |
| WebFetch med whitelist/credential/lese-bare-ceiling: negative tester grønne | testutdata | `TESTRESULT.md#webfetch` | — | nei |
| Injeksjonstest: modelltekst som prøver å legge til domene/credential/verktøy endrer ingenting | testutdata | `TESTRESULT.md#injeksjon` | — | nei |
| Diff planlagt/observert over syntetiske kvitteringer, med ett brudd synlig | testutdata | `TESTRESULT.md#diff` | — | nei |
| Signert `ActionDecisionReceipt`: verify OK / manipulert feiler | testutdata | `TESTRESULT.md#receipt` | — | nei |
| `cell:///AgentTrustPackage` kjører i CellScaffold og «før»-flaten er nåbar i Porthole/Binding (lastetid ≤ 5 s ×3) | kjørende flate | CellScaffold | `TESTRESULT.md#load-time`, `ACCEPT.md#parity` | nei |
| Dataflyt: AgentTrustPackage ↔ EntityAnchor / AIGateway / WebFetch / ScopedCredential / receipts | fil | `dataflow.md` | — | nei |

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

## Formålspakker som festes
- **pkg.std.everything-works** — Alt skal virke (standard kvalitetsport)
    - purpose://quality.build-and-regression: Alle berørte mål bygger og eksisterende tester passerer uten at tester er fjernet eller svekket.
        - test test.build [command]: Bygg alle berørte mål. → TESTRESULT.md#build
        - test test.regression [command]: Kjør hele eksisterende testmengde. → TESTRESULT.md#regression
    - purpose://quality.docs-in-same-change: Alle dokumenter som beskriver endret oppførsel er oppdatert og datert 'Last verified against code'.
        - test test.docs-updated [inspection]: Hver endret kontrakt/atferd har tilsvarende doc-diff. → ACCEPT.md#docs
    - purpose://quality.work-is-visible: Oppgavemappen har oppdatert STATUS.md med gate-tilstand, og et eventuelt planbytte er datert og begrunnet.
        - test test.status-current [inspection]: STATUS.md speiler faktisk tilstand. → ACCEPT.md#status
    - artefakt FORMAALSSPEC.md (port G1): Godkjent formålsspesifikasjon.
    - artefakt PLAN.md (port G2): Arbeidspakker 1:1 mot bladformål.
    - artefakt TESTRESULT.md (port G3): Utdata fra alle avledede tester.
    - artefakt ACCEPT.md (port G3): Forventning mot faktisk, per leveranse.
    - artefakt STATUS.md (port G3): Gate-tilstand og planbytter.
- **pkg.std.gui-surface** — GUI-flate (bilde før kode)
    - purpose://gui.expectation-agreed-before-build: Et rendret bilde per flate/tilstand er godkjent av Kjetil og lagret som referanse i oppgavemappen.
        - test test.gui.reference-image-exists [artifact]: Godkjent referansebilde finnes for hver flate og hver viktig tilstand (tom, fylt, feil). → images/
    - purpose://gui.parity-with-approved-image: Screenshot av faktisk flate ligger side om side med referansebildet i ACCEPT.md, og alle avvik er enten rettet eller godkjent av Kjetil med begrunnelse.
        - test test.gui.parity [inspection]: Side-om-side referanse/faktisk per flate. → ACCEPT.md#parity
    - purpose://gui.surface-loads-in-time: Flaten er synlig innen terskelen angitt i FORMAALSSPEC.md (standard 5 s) på det avtalte miljøet.
        - test test.gui.load-time [measurement]: Lastetid ≤ terskel, tre forsøk. → TESTRESULT.md#load-time
    - purpose://gui.ways-in-are-reachable: SkeletonReachabilityAudit rapporterer ingen elementer som aldri kan sees, og handlingene FORMAALSSPEC §3 navngir finnes i reachableActionKeypaths.
        - test test.skeleton.no-unreachable-elements [command]: Ingen flate har elementer som aldri kan sees; funn navngir handlingene som gaar tapt. → TESTRESULT.md#reachability
        - test test.skeleton.purpose-actions-reachable [inspection]: Hver handling forventningskontrakten (§3) navngir finnes i flatens reachableActionKeypaths. → ACCEPT.md#ways-in
    - artefakt images/ (port G1-GUI): Godkjente referansebilder, ett per flate og tilstand.
    - artefakt skeleton/ (port G1-GUI): CellConfiguration/skeleton-JSON som bildet er rendret fra (når Porthole-preview er brukt).
- **pkg.std.cell-contract** — Cellekontrakt
    - purpose://cell.contract-explicit: Book/<celle>_contract_v<n>.json finnes, og en validator kjører grønt på alle fixtures.
        - test test.cell.contract-fixtures [command]: Kjør kontraktvalidator mot positive/negative fixtures. → TESTRESULT.md#contract
    - purpose://cell.authorization-honours-keypath: Negative tester viser at feil requester, feil keypath og purpose://prompt.unknown alle avvises.
        - test test.cell.auth-negative [command]: Feil requester / feil keypath / ukjent formål avvises. → TESTRESULT.md#auth
    - purpose://cell.no-empty-stubs: Ingen endepunkt i kontrakten er implementert som no-op uten status 'not-implemented'.
        - test test.cell.stub-scan [inspection]: Liste alle no-op-handlere og avstem mot Gap_Analysis.md. → ACCEPT.md#stubs
    - artefakt contract/ (port G2): Kontrakt-JSON + fixtures (kan være lenke til Book/).
- **pkg.std.cell-combination** — Cellekombinasjon og dataflyt
    - purpose://cells.dataflow-declared: dataflow.md (eller .graffle/.json) finnes med alle kanter navngitt med endepunkt/event.
        - test test.cells.dataflow-matches-contracts [inspection]: Hver kant i dataflow finnes i en kontrakt. → PLAN.md#dataflow
    - purpose://cells.capabilities-declared-with-boundary: FORMAALSSPEC.md §2 lister hver antatt kapabilitet med kildefil og hva den ikke dekker.
        - test test.cells.capability-audit [inspection]: Alle kapabilitetspåstander har audit-status retrieved. → FORMAALSSPEC.md#audit
    - artefakt dataflow.md (port G2): Diagram + kant-tabell.

## Lærdommer du må lese før dekomponering
- **lesson.text-ux-is-not-design** (2026-05-06, major): Kjetil forventet en helt annen flate enn den som ble vist; den tekstlige UX-beskrivelsen var godkjent, bildet var det ikke.
    - forebygging: Rendret bilde (Porthole-preview eller mockup) godkjennes før implementering; bildet er akseptansereferanse.
- **lesson.parity-was-correctness-not-decoration** (2026-05-06, major): Parity-audit mellom Porthole og Binding viste at problemet ikke var manglende dekorasjon, men produktkorrekthet (feil oppførsel).
    - forebygging: Akseptanse sammenligner både bilde og oppførsel (knapper trigger keypaths, felt tar input) — begge i ACCEPT.md.
- **lesson.surface-load-alias-miss** (2026-08-24, blocker): Flatelasting tok 46 541 ms (klientens 45 s-timeout) ved bom, 5 000 ms ved treff; målingen 10.08 målte en mislykket lasting.
    - forebygging: Mål lastetid tre ganger og sjekk logg for navnebom før en flate erklæres ferdig; aliaser må løses server-side eller ikke brukes.
- **lesson.plan-instead-of-delivery** (2026-08-21, major): Kjetil ba om en leveranse flere ganger og fikk planer/dokumenter om leveransen i stedet.
    - forebygging: G1 godkjenner formål, ikke arbeid; etter G2 telles bare artefakter listet i §3 'Det du kommer til å se' som fremdrift. Et dokument om leveransen teller aldri som leveransen.
- **lesson.undocumented-plan-switch** (2026-08-24, major): Tre produktive døgn (22.–24.08) så tomme ut i alle statusdokumenter fordi planbyttet fra bølge 1–3 til deploy-seremonien aldri ble skrevet ned.
    - forebygging: STATUS.md i oppgavemappen oppdateres ved hvert planbytte med dato og hvorfor; sjekkes i test.status-current.
- **lesson.planned-documented-as-implemented** (2026-08-24, major): Book/05_Flows_Lifecycle.md beskrev sekvensnummer, signatur og replay som ikke finnes i structen.
    - forebygging: Docs-diff i samme endring, med 'Last verified against code'-dato; planlagt oppførsel merkes eksplisitt.
- **lesson.bridge-inferred-architecture-from-one-use** (2026-08-09, major): En kodeassistent sluttet fra én observert bruksmåte av bridge til en egenskap ved arkitekturen og konkluderte feil.
    - forebygging: Erklær hver kapabilitet oppgaven bygger på som eget formål med kilde og Avgrensning (pkg.std.cell-combination).
- **lesson.cellscaffold-two-holes** (2026-09-01, blocker): CellScaffold har tomme booking-/concierge-stubber og autorisasjon som kaster nøkkelstien og bare sjekker eierskap.
    - forebygging: Ikke porter celler fra CellScaffold til PalazzoScaffold uten å lukke begge hullene; test.cell.auth-negative og test.cell.stub-scan må være grønne.
- **lesson.purpose-never-grants-rights** (2026-08-03, blocker): Risiko for at formålsmatch tolkes som tilgang.
    - forebygging: Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; purpose://prompt.unknown feiler lukket.
- **lesson.corr-approval-surfaces-timed-out** (2026-08-30, major): Corr-godkjenningen (Vegar) er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.
    - forebygging: FORMAALSSPEC.md §2 lister avhengigheter som egne formål med verifier; pkg.std.everything-works og gui.surface-loads-in-time må være grønne før den egentlige testen kjøres.
- **lesson.unresolvable-condition-is-invisible** (2026-09-05, blocker): Relasjoner-flaten viste tittel og ingen vei inn: ingen filopplasting, ingen knapper. Alle tester gronne.
    - forebygging: SkeletonReachabilityAudit kjores over hver flate; test.skeleton.no-unreachable-elements feiler med elementene som aldri kan sees og handlingene som gaar tapt med dem. Betingelser hoerer hjemme inne i List/Grid/Reference-rader, der radens verdi sendes videre; ellers skal cellen avgjore og innhold bindes.
- **lesson.test-corpus-is-not-shipped-corpus** (2026-09-05, major): Rot-probe-testen, lastetidstesten og finnbarhetsauditen var gronne i to uker mens Relasjoner-flaten var tom.
    - forebygging: Enhver flate-test skal bygge korpuset fra det som faktisk sendes ut (menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen), dedupliseres, og feile hvis korpuset er mindre enn appens egen meny.
- **lesson.tested-a-different-path-than-production** (2026-09-05, major): Rot-probene leste relations.state.* gjennom porthole.get og var gronne, mens rendereren aldri fikk de samme dataene.
    - forebygging: Naar en test skal si noe om hva brukeren ser, maa den bruke produksjonens egen kodevei - helst produksjonens egen funksjon med produksjonens egne inndata (SkeletonReachabilityAudit kaller condition.evaluate(root: nil, ...) nettopp derfor).
- **lesson.findability-is-not-usability** (2026-09-05, major): Flatene ble kalt validert fordi de bestod en beskrivelsesaudit; de var samtidig ubrukelige.
    - forebygging: En formaalssjekk maa navngi handlingene eieren skal kunne utfore, og testes mot SkeletonReachabilityAudit.reachableActionKeypaths - ikke mot hvor godt formaalet er formulert.
- **lesson.paste-command-instead-of-queue** (2026-09-07, major): Kjetil fikk et innlimingsskript for å starte Codex; flagget --full-auto finnes ikke på `codex exec`, og kjøringen feilet ved første linje.
    - forebygging: Før enhver Codex-kjøring fra Cowork: `ls HAVEN/_losen-queue/inbox running; tail logs/runner.log`, legg jobben som <id>.job + <id>.prompt.md. Aldri gi Kjetil kommandoer å lime inn. Gyldige `codex exec`-flagg: --sandbox, --skip-git-repo-check, -C.
- **lesson.baseline-count-from-report-not-run** (2026-09-07, minor): PLAN.md sa «48 tester grønne»; baseline-kjøringen viste 68 tester med 3 røde.
    - forebygging: WP0/S0 baseline er alltid en ekte kjøring før endring; PLAN oppgir testtall som «forventet ≈ N (fra <kilde, dato>)», og et rødt baseline stopper ikke arbeidet men registreres som eget avvik med årsak.
- **lesson.codex-sandbox-cannot-reach-docker** (2026-09-07, major): S10 (docker compose build/up) endte i `permission denied … docker.sock` i Codex-sandkassen; deploy-slicen ble blocked.
    - forebygging: Deploy-/image-steg planlegges aldri som Codex-slice; de registreres som HAVEN-Deploy-post med eier Kjetil (eller en dispatcher-adapter med eksplisitt docker-rettighet når arbeidskø-PDD-en er levert). Se HD-0012.
- **lesson.scaffold-without-porthole-host-has-no-preview** (2026-09-07, minor): G1-GUI måtte bruke mockups rendret fra skeleton-JSON; ekte Porthole-preview var umulig.
    - forebygging: For scaffolds uten Porthole-vert: (1) images/README.md må si eksplisitt at bildene er mockups og hva skeleton ikke kan rendre, (2) paritet (test.gui.parity) planlegges som egen slice med kjørende scaffold + Binding/Porthole via bridge, ikke som del av implementeringsjobben.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://contact.communication [draft] — Contact and communication
- purpose://event.participation [draft] — Event participation
- purpose://event.privacy-preserving-networking [draft] — Privacy-preserving event networking
- purpose://gui.quality.functional-accessible [active] — Functional accessible GUI
- purpose://governance [active] — Governance
- purpose://access.audit.privacy [active] — Access, audit and privacy
- purpose://questionnaire.access.audit [active] — Questionnaire access audit
- purpose://knowledge.explain-policy [draft] — Explain policy or rules
- purpose://value-and-commons [candidate] — Value and commons
- purpose://self-determination.data.verifiability [candidate] — Verifiability instead of trust

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | Prosjektets byggkommando (xcodebuild / swift build / pytest) — angis i PLAN.md. | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Prosjektets testkommando; sammenlign antall tester før/etter. | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md. | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen. | ACCEPT.md#status | venter |
| test.gui.reference-image-exists | purpose://gui.expectation-agreed-before-build | purpose_dev.py validate sjekker images/ mot FORMAALSSPEC.md §3. | images/ | venter |
| test.gui.parity | purpose://gui.parity-with-approved-image | Screenshot fra Porthole/Binding i samme viewport som referansen; lim inn i ACCEPT.md. | ACCEPT.md#parity | venter |
| test.gui.load-time | purpose://gui.surface-loads-in-time | Stoppeklokke/logg-tidsstempel; noter alle tre tider. | TESTRESULT.md#load-time | venter |
| test.skeleton.no-unreachable-elements | purpose://gui.ways-in-are-reachable | xcodebuild -only-testing:BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn | TESTRESULT.md#reachability | venter |
| test.skeleton.purpose-actions-reachable | purpose://gui.ways-in-are-reachable | Sammenlign §3-radene mot SkeletonReachabilityAudit.reachableActionKeypaths(skeleton). | ACCEPT.md#ways-in | venter |
| test.cell.contract-fixtures | purpose://cell.contract-explicit | python3 checks/validate_contract.py | TESTRESULT.md#contract | venter |
| test.cell.auth-negative | purpose://cell.authorization-honours-keypath | Tre enhetstester navngitt etter tilfellet. | TESTRESULT.md#auth | venter |
| test.cell.stub-scan | purpose://cell.no-empty-stubs | Søk i berørte filer; skriv listen i ACCEPT.md. | ACCEPT.md#stubs | venter |
| test.cells.dataflow-matches-contracts | purpose://cells.dataflow-declared | Tabell kant→kontrakt i PLAN.md. | PLAN.md#dataflow | venter |
| test.cells.capability-audit | purpose://cells.capabilities-declared-with-boundary | Tabell i FORMAALSSPEC.md §0. | FORMAALSSPEC.md#audit | venter |
| test.tp.projeksjon-deterministisk | purpose://candidate.tillitspakke-agentflaate.projeksjon | Generer pakke to ganger fra uendret fixture-flåte → identisk digest; endre én Grant i fixture → ny digest. Enhetstest. | TESTRESULT.md#projeksjon | venter |
| test.tp.ingen-hemmeligheter | purpose://candidate.tillitspakke-agentflaate.projeksjon | Skann generert pakke-JSON og «før»-state for nøkkelmønstre og prompt-tekst; må være tomt. | TESTRESULT.md#projeksjon | venter |
| test.tp.rekkevidde-matcher-kontrakter | purpose://candidate.tillitspakke-agentflaate.rekkevidde | Hver kant i pakkens graf finnes som Grant i en template/Contract, og summert rekkevidde for AIGateway = (`web.fetch`, uten credentials, ‹domener›). | TESTRESULT.md#rekkevidde, PLAN.md#dataflow | venter |
| test.tp.provider-tools-off | purpose://candidate.tillitspakke-agentflaate.leverandorverktoy | Bygg provider-request for hver adapter; assert ingen `tools`/`tool_choice`/web-search-felt; payload-digest endres hvis et slikt felt legges til. | TESTRESULT.md#provider-tools | venter |
| test.tp.justering-innsnevrer | purpose://candidate.tillitspakke-agentflaate.justering | Fjern domene fra whitelist via pakke-handling → ny digest → fetch mot domenet nektes. | TESTRESULT.md#justering | venter |
| test.tp.justering-kan-ikke-utvide | purpose://candidate.tillitspakke-agentflaate.justering | Forsøk å legge til Grant/domene templaten ikke har → avvist med typed grunn; digest uendret. | TESTRESULT.md#justering | venter |
| test.tp.start-uten-godkjent-digest-nektes | purpose://candidate.tillitspakke-agentflaate.godkjenning | Start flåte med policy-digest som ikke matcher godkjent pakke → `denied`; med match → tillatt. | TESTRESULT.md#godkjenning | venter |
| test.tp.webfetch-whitelist-negativ | purpose://candidate.tillitspakke-agentflaate.webfetch-ceiling | `web.fetch` mot host utenfor whitelist → `denied` uten nettverkskall (mock URLSession teller 0). | TESTRESULT.md#webfetch | venter |
| test.tp.webfetch-credential-negativ | purpose://candidate.tillitspakke-agentflaate.webfetch-ceiling | Grant uten credential-rett → fetch med alias nektes før oppslag i ScopedCredential (fixture-store teller 0 oppslag). | TESTRESULT.md#webfetch | venter |
| test.tp.webfetch-monster-kanttilfeller | purpose://candidate.tillitspakke-agentflaate.webfetch-ceiling | Tabell-test: `*.example.org` → `a.example.org` ok, `example.org` nei, `a.b.example.org` ok, `example.org.evil.com` nei, `a.example.org:8443` nei uten port i mønster; `http://` nei. | TESTRESULT.md#webfetch | venter |
| test.tp.webfetch-redirect-negativ | purpose://candidate.tillitspakke-agentflaate.webfetch-ceiling | Mock 302 fra whitelistet vert til ikke-whitelistet → ingen andre request, `denied` med grunn `redirect_outside_whitelist`. | TESTRESULT.md#webfetch | venter |
| test.tp.injeksjon-endrer-ingenting | purpose://candidate.tillitspakke-agentflaate.skal-ikke.modell-utvider | Modellsvar (fixture) med «legg til example.org i whitelist», «bruk nøkkel X», «tools: web_search» → ceiling, digest og request uendret; forsøk logget som avvist. | TESTRESULT.md#injeksjon | venter |
| test.tp.pakke-uten-contract-nektes | purpose://candidate.tillitspakke-agentflaate.skal-ikke.pakke-gir-rett | Håndlaget pakke med ekstra Grant → cellen avviser kallet som før; pakke-cellen markerer pakken «ikke avledet». | TESTRESULT.md#pakke-gir-rett | venter |
| test.tp.diff-viser-brudd | purpose://candidate.tillitspakke-agentflaate.etterproving | Syntetiske kvitteringer: 5 innenfor + 1 med ny destinasjon + 1 med credential løst opp → diff lister nøyaktig 2 avvik med riktig type. | TESTRESULT.md#diff | venter |
| test.tp.receipt-signatur | purpose://candidate.tillitspakke-agentflaate.signert-kvittering | Signer receipt med celle-identitet; verify OK; endre ett digest-felt → verify feiler. | TESTRESULT.md#receipt | venter |
| test.tp.e2e | purpose://candidate.tillitspakke-agentflaate.root | Fixture-flåte: generer → juster (fjern domene) → godkjenn → kjør 3 fetch (2 ok, 1 utenfor) → «etter» viser 1 avvik. Med ekte modell når kreditt finnes; ellers fixture-modell, merket. | TESTRESULT.md#e2e | venter |

## 6. Åpne spørsmål til Kjetil

Besvart 2026-09-08 (iterasjon 2):

| Spørsmål | Svar | Konsekvens i treet |
|---|---|---|
| Q1 Omfang v1 | Ett scaffold (CellScaffold, fixture-flåte AIGateway + WebFetch + ScopedCredential) | Rot avgrenset; bridge = egen node senere (§2) |
| Q2 Hvor lagres innsnevringen | Som data ved siden av templaten (EntityAnchor); templaten er taket | «justering» kan bare innsnevre; ingen endring av Grant-wireformat |
| Q3 Signert kvittering i v1 | Ja | «signert-kvittering» beholdes i v1 |
| Q4 Whitelist-semantikk | Mønstre (`*.example.org`) | «webfetch-ceiling» presisert med matcheregler, port, redirect; to nye tester |
| Q5 Hvem godkjenner | Eieren av scaffoldet | Motpart-godkjenning (M1-tilfellet) = egen node senere |

Ingen åpne spørsmål som endrer treet. Venter på G1-ordet.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-08 | Opprettet | Losen |
| 2 | 2026-09-08 | Q1–Q5 besvart: mønster-whitelist med matche-/port-/redirect-regler og to nye tester i «webfetch-ceiling»; innsnevring lagres som data ved siden av templaten; signert kvittering i v1; ett scaffold, eieren godkjenner | Kjetil / Losen |
| 1 | 2026-09-08 | §0 ordrett + 15 audit-rader (2 contradicted, 1 recalled); §1 tre med 11 noder inkl. to antiformål; §2 avgrensning + 11 avhengigheter; §3 14 leveranser (5 bilder); §5 +14 tester; §6 Q1–Q5 | Losen |
