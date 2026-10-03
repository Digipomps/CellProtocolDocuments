# Formålsspesifikasjon — Entity-utvidelse begge veier mellom PalazzoScaffold og andre scaffolds, og å fange når koble/utvide skal tilbys

Oppgavemappe: `PDD_palazzo-entity-utvidelse-begge-veier_2026-09-14` · Opprettet 2026-09-14 · Iterasjon 3 (**G1 godkjent 2026-09-14**, G1-GUI godkjent på v1 — tekster rettet til v2 etter Astra-audit; G2 venter) · HAVEN-Deploy: HD-0079

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI (tilbudet om å koble/utvide er en flate): ingen implementering før G1-GUI.
> Stier er relative til repoet (`Repo::sti`).

## 0. Intensjon (ordrett) og brief-audit

Kjetil, 2026-09-14:

> Brukere via Identities vil nå Palazzo scaffoldet via en Identity i en Entity i andre scaffolds IdentityVault for Pallazzos identityDomain eller fra en lokal IdentityVault som holder brukerens Identity knyttet til Entity. Vi må altså støtte ,nær opp til, friksjonsløs utvidelse av Entity i begge retninger. Så vi må bli veldig flinke til å fange når vi skal tilby brukeren å kobler eller utvide.

Tidligere, 2026-09-02 (bestillingen av PalazzoScaffold): «alle aktører har egen entitet som kan utvides til resten av HAVEN eller utvide HAVEN-entiteten med Palazzo-entiteten, uten at brukerne merker det annet enn når det lages bevis for at to entiteter er samme entitet».

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Samme-entitet-bevis finnes: forespørsel → godkjenning i anker → fullføring med VC-presentasjon | retrieved | `PalazzoScaffold::README.md` §5; `PalazzoScaffold::Sources/App/Cells/PalazzoIdentityLinkCell.swift` (orkestrator + forbruker `extendAccess`: stående `*`-policy + full kontrakt i eierens PalazzoEntity); `PalazzoScaffold::Tests/AppTests/PalazzoIdentityLinkTests.swift` (2 tester); CellProtocol `IdentityLinkProtocolService` |
| Custodial identiteter per aktør i Palazzos domene (`guest:<id>`, `staff:<id>`, huset) i VaporIdentityVault | retrieved | `PalazzoScaffold::Sources/App/Support/PalazzoScaffoldContract.swift`; prosjektminne `palazzoscaffold-vapor` |
| Utvidelse *fra* HAVEN-entitet *til* Palazzo (HAVEN-bruker uten Palazzo-identitet åpner en Palazzo-flate) | **unavailable** — ingen kjent kode som oppdager situasjonen og tilbyr kobling | må kartlegges (Astra-analyse, handoff/ASTRA_BRIEF.md) |
| Utvidelse *fra* Palazzo-gjest (lokal vault) *til* HAVEN senere | **unavailable** — samme | samme |
| «Fange når vi skal tilby» — deteksjonsøyeblikk | **unavailable** — ikke definert | dette dokumentet §1/§6 |
| «IdentityLink-beviset skal i seg selv være like sikkert eller sikrere enn Vipps» | **contradicted som formulert** — IdentityLink beviser «samme nøkkelholder» (to signaturer), Vipps-innlogging beviser «person med BankID». De er svar på ulike spørsmål; se §6 Q4′ | `PalazzoScaffold::README.md` §5; Vipps/BankID: allment kjent, ikke lest fra kilde denne økten |
| Ankeret selv får ikke kontrakt (stub-GrantCondition i CellProtocol) | retrieved (Astra 2026-09-14): stub er belagt, men «aldri kontrakt» er for vidt | `CellProtocol::Sources/CellBase/Agreement/Condition/Implementation/GrantCondition.swift:16`, `CellVapor/Cells/EntityAnchorCell.swift:68` (handoff/ASTRA_ANALYSE.md) |
| Nøklene til custodial gjeste-/staff-identiteter ligger på Palazzos server, ikke på telefonen | retrieved (Astra) — **v1-bildenes «her på telefonen» var usant; rettet i v2** | `PalazzoScaffold::Sources/App/configure.swift:39`, `CellProtocol::Sources/CellVapor/VaporIdentityVault.swift:2412` |
| IdentityLink = flere signaturer over sammenkjedede strukturer (request → approval bundet til request-hash → SameEntity-VC → domenebundet presentasjon), med nonce/utløp/JTI | retrieved (Astra) | `CellProtocol::Sources/CellBase/Identity/IdentityLinkCompletion.swift:197,303,372,507` |
| Fire forhold gjør at (a) ikke er sant i dag: (1) VaporBridgeTransport fester lokal vault til presentert deskriptor → serveren kan signere for en innsluppet peer; (2) Palazzo-completion låser ikke issuer/anker/approval; (3) `freshAuthPerformedAt` settes til «nå» uten reell autentisering; (4) JTI/verifikasjon/lagring ikke atomisk, revoke rydder ikke avledet policy | retrieved (Astra, [usikker] ikke demonstrert ved kjøring) — **registrert som HD-0080/HD-0081** | `CellProtocol::Sources/CellVapor/CloudBridge/VaporBridgeTransport.swift:218`, `PalazzoScaffold::Sources/App/Cells/PalazzoIdentityLinkCell.swift:142,248,288`, `CellVapor/Cells/EntityAnchorCell.swift:890` |
| Ingen automatisk deteksjon/tilbud finnes; rollesimuleringen utfører ingen lenking | retrieved (Astra) | `PalazzoScaffold::Tests/Roles/roles/gjest.json`, `PalazzoIdentityLinkTests.swift:33` |

Kjetils svar 2026-09-14 på iterasjon 1 §6 (ordrett):

> 1. Gjør ditt forslag. 2. Begge, den som først ser riktig tilstand gjør det. 3. Jeg tenker mest på selve opplagelsen av koblingen. Det må oppleves trygt, helst være ett trykk og være forståelig. 4. IdentityLink-beviset - det skal i seg selv være like sikkert eller sikrere enn vipps. 5. Celle.

Kjetil, 2026-09-14 kveld, på Q4′ og bildene: «ja til (a)+(b) og til bildene».

## 1. Formålstre (iterasjon 2)

| purposeRef | Tittel | Forelder | Goal (outcome · signals · verifier) | Status |
|---|---|---|---|---|
| purpose://candidate.palazzo-entity-utvidelse.root | En person med entitet i ett scaffold kan bruke Palazzo, og en Palazzo-gjest kan bli HAVEN-bruker, uten å merke annet enn ett trygt, forståelig trykk der bevis for «samme entitet» lages | purpose://identity.* (Book 23 — node velges ved G1) | outcome: begge retninger ender med lenket identitet og stående policy · verifier: test.link-both-ways (rollesimulering, roller `gjest`/`annen-gjest`) | candidate |
| …detect | **Deteksjon (celle, Q5):** en celle fanger øyeblikkene der kobling bør tilbys — instansiert i begge scaffolds; den som først ser riktig tilstand tilbyr (Q2); tilbudet gis én gang per (identitet × scaffold) | root | outcome: hvert øyeblikk D1–D5 har et observerbart signal og gir nøyaktig ett tilbud · verifier: test.offer-moments, test.offer-once | candidate |
| …detect.D1 | HAVEN-identitet (annet scaffolds vault, Palazzos domene) kaller en Palazzo-celle over bro for første gang, uten Palazzo-entitet. **To løp (Astra):** D1a «ny Palazzo-entitet for allerede valgt domenenøkkel» (ingen to-identitetsbevis nødvendig) og D1b «lenke eksisterende gjest til annen nøkkel» (IdentityLink) | detect | signal: bridgehead/gateway ser identitet uten `EntityAnchor` i Palazzo · tilbud fra Palazzo-siden (images/gjest-koble-tilbud) og/eller HAVEN-siden (images/haven-koble-tilbud) · verifier: test.D1 | candidate |
| …detect.D2 | Palazzo-gjest (custodial `guest:<id>`) får senere en HAVEN-entitet | detect | signal: HAVEN-app presenterer Palazzo-kode/QR, eller Palazzo-flaten ser en HAVEN-identitet på samme enhet · verifier: test.D2 · **signal må bekreftes av Astra-analysen** | candidate |
| …detect.D3 | Huset ber om innsyn (`access.request`) mot en gjest hvis anker har en ulenket identitet i et annet domene | detect | signal: `PalazzoAccessContracts` ser requester-mål med lenkbar identitet · tilbud til gjesten før svaret · verifier: test.D3 | candidate |
| …detect.D4 | Samme person på to enheter (lokal vault på telefon + HAVEN på laptop) | detect | signal: to identiteter presenteres i samme sesjon/kode · verifier: test.D4 | candidate — **senere** (ikke i første plan) |
| …detect.D5 | Staff med HAVEN-identitet skal på bemanningslisten | detect | signal: `staff.roster`-registrering fra HAVEN-identitet · tilbud om å lenke `staff:<id>` · verifier: test.D5 | candidate |
| …detect.offer-once | Ett tilbud per (identitet × scaffold); «Ikke nå» = neste naturlige øyeblikk, tidligst etter 7 dager; «Aldri» = stille, reversibelt under «Koblinger» | detect | verifier: test.offer-once (tre kall → ett tilbud), test.never-is-reversible | candidate |
| …experience | **Opplevelsen (Q3):** koblingen oppleves trygg, tar ett trykk og er forståelig | root | verifier: G1-GUI-bildene + test.one-tap + test.understandable | candidate |
| …experience.one-tap | Fra tilbudet fullfører nøyaktig ett trykk koblingen **når motparten alt er sikkert valgt og brukeren bekrefter med enhetens egen autentisering (Face ID/kode)**; må den andre siden godkjenne, vises «venter»-tilstanden og koblingen fullføres uten flere trykk her. Første gang uten sikker motpart kreves ett ekstra bekreftende trykk (Astra) | experience | outcome: antall brukerhandlinger = 1 (samme enhet) / 1 + godkjenning på den andre (to enheter) · verifier: test.one-tap (GUI-test teller handlinger), images/gjest-koble-tilbud-v1.png, gjest-koble-venter-v1.png | candidate |
| …experience.understandable | Tilbudet sier i ≤ 3 setninger: hvem (bekreftet hus/domene + din identitet), hva som skjer (ett bevis, ingen data flyttes), hva som ikke endres (det du deler); «Hva betyr dette?» utvider uten å forlate flaten | experience | verifier: test.understandable (tekstaudit mot bildene), images/gjest-koble-tilbud-forklart-v1.png | candidate |
| …experience.safe | Flaten viser bekreftet motpart (signert husnavn + domene), hvor beviset lages og lagres, og at det kan angres; ingen data flyter før bevis + ja | experience | verifier: test.no-silent-merge + images/gjest-koble-koblet-v1.png (Angre 30 dager) | candidate |
| …experience.offer-surface | Tilbudet er et sheet etter samtykkemønsteret: primær «Koble — ett trykk», sekundær «Ikke nå», tertiær «Aldri for Palazzo», «Hva betyr dette?» | experience | **GUI → G1-GUI:** `images/*.png` (6 tilstander) · verifier: test.gui.parity | candidate |
| …proof | **Beviset (Q4, besluttet (a)+(b)):** (a) koblingen kan ikke forfalskes, kapres over bro eller spilles av, og custodial nøkler alene kan ikke fullføre den; (b) personforankring hentes fra en forankret identitet (Vipps-VC) når et formål krever det. Konkrete krav (Astra): broen bevarer ekstern signeringsproveniens; mottaker låser betrodd issuer, eksakt anker, request-hash, fingerprints og serveropprettet engangsutfordring; fersk brukerautentisering er reell (enhetens egen), ikke et tidsstempel; atomisk engangsbruk av JTI; revoke stopper avledet policy. «Minst like sikkert som Vipps» hevdes først når sammenligningsprofilen er kildeverifisert | root | verifier: HD-0080 + HD-0081 grønne; trusselmodell validert uavhengig; test.replay, test.bridge-provenance, test.custodial-compromise, test.fresh-auth | candidate |
| …proof.no-silent-merge | Ingen data mellom entitetene før bevis + ja; purpose gir aldri rett | proof | verifier: test.cell.auth-negative (før lenke 403; etter lenke uten grant 403) | candidate |
| …cell | **Cellen (Q5):** deteksjon + tilbud + «offer-once»-tilstand bor i én celle med kontrakt, instansierbar i PalazzoScaffold og på HAVEN-siden | root | verifier: pkg.std.cell-contract (contract/, auth-negative, stub-scan) · plassering (PalazzoScaffold først, CellProtocol når HAVEN-siden trenger samme type) avgjøres i G2 | candidate |

## 2. Avgrensning og avhengigheter

Hva dette IKKE er: ikke Vipps-VC-tjenesten (egen PDD) — men den er kandidat til «forankret identitet» i …proof; ikke scaffold-admin-delegering; ikke Porthole-lasting (PDD porthole-fjernt-scaffold); ikke deploy; ikke D4 i første plan.

| Kapabilitet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| PalazzoScaffold nåbart over bro fra CellScaffold/Porthole | PDD porthole-fjernt-scaffold (pz1 levert 2026-09-14, G5 venter) + B3 | Transport og Porthole-lasting, ikke identitetsflyt | Ja — verifier: test.g5 grønn |
| IdentityLinkProtocolService (request → approve → complete) | CellProtocol (sti bekreftes av Astra) + `PalazzoScaffold::Sources/App/Cells/PalazzoIdentityLinkCell.swift` | Dagens flyt er manuell/ API-drevet; ingen deteksjon, ingen flate | Ja — `PalazzoIdentityLinkTests` grønn |
| Samtykke-modal (mønster for sheetet) | `PalazzoScaffold::Sources/App/Skeleton/PalazzoConsentConfigurationFactory.swift` (`SkeletonPresentation(kind: .modal)`, mobileFallback sheet) | Rendering av avatar-rad, ekspander og kode-visning er ikke verifisert i skeleton — se images/README.md | Nei for G1 — ja for P5 |
| Rollesimulering mot kjørende server (WP10) | `PalazzoScaffold::Tests/Roles/` | Krever server + token; ikke kjørt ennå | Ja for test.link-both-ways |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Tilbudsflaten, gjest/Palazzo-side, lukket og forklart | bilde | `images/gjest-koble-tilbud-v1.png`, `images/gjest-koble-tilbud-forklart-v1.png` | G1-GUI | nei |
| «Venter på HAVEN-appen» (to enheter) | bilde | `images/gjest-koble-venter-v1.png` | G1-GUI | nei |
| «Koblet» med Angre (30 dager) | bilde | `images/gjest-koble-koblet-v1.png` | G1-GUI | nei |
| «Aldri» — stille, reversibel linje | bilde | `images/gjest-koble-aldri-v1.png` | G1-GUI | nei |
| Tilbudet sett fra HAVEN-siden (Q2: begge kan tilby) | bilde | `images/haven-koble-tilbud-v1.png` | G1-GUI | nei |
| Astra-analyse: mekanismer, hull, deteksjonssignaler, Q4′-vurdering | fil | `handoff/ASTRA_ANALYSE.md` | §6 | nei |
| Trusselmodell bevis vs. Vipps, uavhengig validert | fil | `handoff/TRUSSELMODELL_bevis.md` (etter Astra) | …proof | nei |
| Iterasjon 3 av dette dokumentet + PLAN.md | fil | denne mappen | — | nei |

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
- **lesson.codex-workspace-write-cannot-build-cellscaffold** (2026-09-09, major): WP0-baselinen i køen ble blocked: `sandbox-exec: sandbox_apply: Operation not permitted`. Testkommandoen brukte 1 604 sekunder uten at én eneste test startet.
    - forebygging: Lange bygg og testkjøringer legges ikke som `workspace-write`-køjobb. De kjøres som detached skript startet via Codex med `danger-full-access` og python Popen(start_new_session=True), med logg i en montert mappe som Cowork kan polle — samme mønster som produserte den notariserte HavenAgentD-pakken 2026-09-08. Køjobber brukes til analyse, kontrakter, dokumentasjon og korte kommandoer.
- **lesson.baseline-measured-another-pdds-branch** (2026-09-09, major): WP0 målte `pdd/tillitspakke-agentflaate` med 181 skitne oppføringer, ikke et rent utgangspunkt for sin egen PDD. En regresjonsbaseline derfra sier ingenting om hva denne PDD-en endrer.
    - forebygging: WP0 måler en ren eksport av den revisjonen arbeidet skal gå ut fra (`git archive <rev> | tar -x -C <scratch>`), ikke det delte arbeidstreet. Er arbeidstreet opptatt av en annen PDD, er det en planopplysning som hører i STATUS, ikke noe implementeringen skal jobbe rundt.
- **lesson.worktree-created-from-vm-has-unusable-gitdir** (2026-09-09, major): WP1 ble blocked etter ett minutt: `fatal: not a git repository: /sessions/<sesjon>/mnt/CellScaffold/.git/worktrees/_wt-sad-20260909`, exit 128. Branch og HEAD kunne ikke bekreftes.
    - forebygging: Opprett worktrees fra macOS (Codex), ikke fra VM-en. Er det allerede gjort fra VM-en: skriv om begge pekerfilene til macOS-stien og verifiser `branch --show-current` + `rev-parse HEAD` **fra macOS** før noen jobb legges i køen. En jobb skal aldri være første stedet en sti blir prøvd.
- **lesson.cellbase-decodingerror-shadows-swift** (2026-09-09, minor): WP1s nye celle ga 50 kompileringsfeil: `type 'DecodingError' has no member 'dataCorruptedError'` og `cannot infer contextual base in reference to member 'registry'`, alle fra én linje.
    - forebygging: I App-modulen: skriv `Swift.DecodingError` når du vil ha standardbibliotekets. Gjelder generelt for typenavn CellBase også definerer — sjekk med `grep -rn "enum <Navn>" CellProtocol::Sources/CellBase` før du antar at et kjent Foundation-navn er Foundations.
- **lesson.valuetype-equality-false-for-objects** (2026-09-09, major): Fire av sju WP1-tester feilet på `XCTAssertEqual` mellom to `ValueType.object` som hadde identisk innhold. Feilmeldingen viste samme nøkler og verdier på begge sider, i ulik rekkefølge.
    - forebygging: Aldri assert på hele sammensatte `ValueType`-verdier. Sammenlign kanonisk JSON (`JSONEncoder` med `.sortedKeys`) eller pakk ut og sammenlign felt for felt. Skalarer (`.string`, `.integer`, `.bool`, `.null`) sammenlignes trygt. Merk: dette er et funn i CellBase, ikke bare en testregel — App-kildene destrukturerer riktignok før sammenligning, men en fremtidig `==` på hele verdier vil stille behandle like verdier som ulike. Ikke revidert utover App-kildene.
- **lesson.syntax-check-reported-as-delivered** (2026-09-09, major): WP1 ble rapportert som «kode og 7 tester levert, syntakssjekken bestod». Et faktisk bygg ga 50 kompileringsfeil, og testene feilet 4 av 7 da de først kunne kjøre.
    - forebygging: En implementeringsslice er ikke levert før et detached bygg med `danger-full-access` er kjørt mot arbeidstreet og både bygg og de nye testene er grønne. Legg byggejobben klar FØR slicen kjøres, og skriv i prompten at slicen skal rapportere «skrevet, ikke verifisert» — ikke «levert».
- **lesson.cellbase-internal-members-look-public** (2026-09-09, minor): WP2 stoppet på `'fullPermissionString' is inaccessible due to 'internal' protection level`. Medlemmet finnes og brukes i CellBase selv, så det så ut som et gyldig API.
    - forebygging: Sjekk tilgangsnivå og faktisk returverdi før du bruker et CellBase-medlem fra App: `grep -n "var <navn>" CellProtocol::Sources/CellBase/...`. Et medlem som brukes internt i CellBase er ikke automatisk en del av API-et, og navnelikhet betyr ikke verdilikhet.
- **lesson.entityanchor-keypaths-are-registered** (2026-09-09, minor): WP2-testen skrev en sentinel til `profile` på abonnentens EntityAnchor og fikk `notFound` ved gjenlesing. Skrivingen ga ingen feil.
    - forebygging: Skriv aldri testdata til en oppdiktet keypath på en celle. Finn en keypath cellen faktisk registrerer, helst en annen test som allerede bruker den. At et `set` går gjennom er ikke bevis på at keypathen finnes.
- **lesson.new-cell-must-declare-its-provisioning-mode** (2026-09-09, major): To nye celler i CellScaffold ga tre nye regresjoner: `OrchestratorPersistenceTests testRequireExistingModeRejectsFreshStorageWithoutCreatingBootstrapCells` (opprettet en celle i require-existing-modus mot fersk lagring) og to `TopUpCheckoutTests` som teller celler i provision-only-modus (5 mot forventet 4).
    - forebygging: Enhver ny persistert celle i CellScaffold må eksplisitt svare på tre spørsmål før den registreres: (1) skal den opprettes i require-existing mot fersk lagring? Nei, med mindre den er kanonisk bootstrap. (2) Er den en av de kanoniske eager-bootstrap-cellene som provision-only skal lage? Nesten alltid nei — TopUpCheckoutTests teller dem eksplisitt. (3) Er den en Porthole-publisert flate? Bare da hører den i `reconcilePortholePublishedCellResolves`. Scaffold-intern tilstand registreres i egen funksjon, gated på policy OG provisionOnly, med gjenkjenning av eksisterende mapping.
- **lesson.branch-is-empty-after-eight-work-packages** (2026-09-09, major): Åtte arbeidspakker rapportert utført og verifisert, ACCEPT.md skrevet — men `git branch -v` viste at `pdd/scaffold-admin-delegering` fortsatt pekte på samme commit som `main` (`e1f3e22f`). All koden lå ucommittet i et worktree som bare finnes på én maskin. Ett tapt worktree = 2 750 linjer kode og test borte, med full dokumentasjon på at arbeidet var «levert».
    - forebygging: Skill «filene finnes» fra «branchen har dem». Sjekk `git rev-parse <branch>` mot `git rev-parse <base>` som del av hver verifikasjon som påstår at noe ligger på en branch; er de like, er branchen tom. Legg en commit-pakke inn i planen etter første grønne bygg, ikke etter siste arbeidspakke. Når worktreet bare kan leses fra macOS, kjør sjekken der — ikke hopp over den fordi verktøyet svarer feil.
- **lesson.ciphertext-field-held-plaintext-hash** (2026-09-10, blocker): Losen fortalte Kjetil at lyd allerede var kryptert i lagring. Det var feil: filene i prod begynner med ID3 og er vanlig MP3. To ting forte dit. (1) Krypteringskoden som ble lest tilhorer MusicIngestCell paa /mvp/ingest/local, mens Butterpop publiserer gjennom MusicAssetStoreCell.storeLocalAsset, som skriver bytene slik de kommer. (2) storeLocalAsset setter ciphertextSHA256 = plaintextSHA256 = sha256(data), saa manifestet ser kryptert ut selv naar encryptionPolicy er none.
    - forebygging: En paastand om at noe er kryptert, signert eller verifisert skal bekreftes paa artefaktet - les bytene, ikke feltet. Et felt som heter ciphertext* skal ikke settes naar encryptionPolicy er none; enten utelates det, eller navnet sier hva det er. Kan bli derivedTest: manifest med encryptionPolicy none har ingen ciphertext-verdi.
- **lesson.local-main-is-not-main** (2026-09-11, major): WP0-baselinen var rød og ble meldt som «main bygger ikke». Det var feil. Den commiten baselinen ble målt mot, `ba14895`, lå bare på den LOKALE main-grenen og var aldri pushet; den avhang av CellBase-kode som heller ikke var pushet. origin/main lå fire commits lenger fram, pinnet CellProtocol til en revisjon som ER på CellProtocol sin main, og hadde grønn CI hele tiden. Et helt døgns arbeid ble bygget oppå den lokale commiten.
    - forebygging: Før du måler en baseline eller sier at main er rød: `git fetch origin main` og sammenlign. Er lokal main foran origin/main, er de commitene ikke main for andre — bygg aldri videre på dem. Se på CI for origin/main før du konkluderer. `swift package edit` skal aldri være på når noe måles eller meldes verifisert. Og den eneste sjekken som virkelig avgjør: klon fra GitHub til en tom katalog og bygg der. HavenAgentD::Scripts/preflight_before_landing.sh stiller alle fire spørsmålene.
- **lesson.a-new-red-test-needs-a-repeated-baseline** (2026-09-10, minor): Første fulle kjøring med nye endringer viste to røde i stedet for baselinens én, og den nye lå i en fil jeg hadde endret. Det så ut som en regresjon jeg hadde innført.
    - forebygging: Når en ny rød dukker opp: kjør basen på nytt, i et eget rent worktree, **flere ganger** (tre holder som regel), før du enten tar på deg feilen eller avfeier den. Skriv resultatet av gjentakelsen i TESTRESULT — «2 av 3 på ren base» er et svar, «den er nok flaky» er ikke. Det koster ti minutter og avgjør om du bruker natten på å jage din egen feil eller andres.
- **lesson.swift-test-exit-code-lies-in-havenagentd** (2026-09-10, minor): `swift test` i HavenAgentD avslutter med 1 selv når samtlige 212 tester passerer. Et skript som leser `$?` melder rødt på et helt grønt tre.
    - forebygging: Les resultatet fra linjen `Test run with N tests in M suites passed/failed`, ikke fra exitkoden, i alle skript og køjobber for dette repoet. Og fjern det tomme XCTest-målet, eller bygg det for riktig arkitektur, før noen setter opp CI her — ellers vil CI være rød uansett hva som gjøres.
- **lesson.pin-must-be-on-their-main** (2026-09-11, major): En revisjonspin i Package.swift pekte på en CellProtocol-revisjon som ikke lå på CellProtocol sin main. Koden bygde bare på den ene maskinen som hadde revisjonen liggende lokalt.
    - forebygging: Å pinne er riktig — det er det som gjør bygget reproduserbart. Kravet er at revisjonen er en forfar av avhengighetens egen main. Da er «bygg fra andres main» og «reproduserbart bygg» samme krav. HavenAgentD::Scripts/assert_dependencies_are_on_their_main.sh håndhever det, og CI kjører den. Lander du en klient før cellen den bruker er på den andres main, har du laget et repo som bare bygger hos deg.
- **lesson.a-red-baseline-is-a-question-not-an-answer** (2026-09-11, major): En rød baseline ble behandlet som en opplysning om prosjektet, og arbeidet gikk videre med et tiltak som gjorde den grønn. Tiltaket skjulte årsaken i stedet for å fjerne den.
    - forebygging: Svar på tre spørsmål før du gjør noe med en rød baseline: er utsjekket mitt likt origin? er CI grønn på origin/main? hvilken commit gjorde den rød, og hvem eier den? Først når svaret er «prosjektet er faktisk rødt» er det riktig å jobbe rundt det — og da som en egen, navngitt sak, ikke som en stille lokal omgåelse.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance

## 5. Avledede tester (låses ved G1)

| test | type | hvordan | bevis |
|---|---|---|---|
| test.D1 / test.D3 / test.D5 | command | XCTVapor + bro i minnet: situasjonen oppstår → cellen emitterer ett tilbud med riktig innhold (hvem/hva/ikke) | TESTRESULT.md#offer-moments |
| test.D2 | command | som over, når signalet er bekreftet av Astra | TESTRESULT.md#offer-moments |
| test.offer-once / test.never-is-reversible | command | tre utløsninger → ett tilbud; «Aldri» → ingen tilbud, men tilstand kan endres | TESTRESULT.md#offer-once |
| test.one-tap | command | GUI-test (skeleton-iterate actions): fra tilbud til «Koblet» med én handling; to-enhets-vei: én handling + godkjenning på den andre | TESTRESULT.md#one-tap |
| test.understandable | inspection | tekstene på flaten mot §1 …experience.understandable (hvem/hva/ikke, ≤ 3 setninger) | ACCEPT.md#understandable |
| test.replay / test.bridge-mitm / test.custodial-compromise | command | avspilt bevis avvises; feil fingerprint over bro avvises; stjålet custodial nøkkel kan ikke fullføre uten den andre signaturen | TESTRESULT.md#proof |
| test.cell.auth-negative | command | før lenke 403; etter lenke uten grant 403; prompt.unknown avvises | TESTRESULT.md#auth |
| test.link-both-ways | artifact | rollesimulering mot kjørende server | RAPPORT_<dato>.md |
| test.gui.parity | inspection | Porthole-skjermbilder side om side med images/ | ACCEPT.md#parity |

## 6. Gjenstående beslutninger (fra Astra-analysen; Losens anbefaling i kursiv — sier Kjetil ingenting annet, gjelder anbefalingen ved G2)

1. D1 i to løp: bruk eksisterende Palazzo-domeneidentitet direkte når HAVEN-identiteten alt er i Palazzos domene; opprett custodial gjest bare når det faktisk trengs. *Anbefalt ja.*
2. (a)+(b) med konkrete sikkerhetskrav; Vipps-likhetsløftet utsettes til sammenligningen er kildeverifisert. **Besluttet av Kjetil 2026-09-14.**
3. Første leveranse krever en uavhengig HAVEN-nøkkel og fersk, reell brukerautentisering for kobling mot custodial Palazzo-identitet. *Anbefalt ja — det er dette som gjør «ett trykk» trygt.*
4. D2-signal = QR med kortkode som reserve + «Åpne HAVEN» på samme telefon; Palazzo-inbound som tilgangsløp; eksplisitt HAVEN-kvittering. *Anbefalt ja (images/gjest-koble-venter-v2).*
5. «Ett tilbud» = én aktiv tilbudssesjon på tvers av begge tilbydere (atomisk reservasjon før visning), sju dagers utsettelse, reversibelt «Aldri». *Anbefalt ja (Q2/Q6).*
6. Tilbakekalling («Koble fra») når som helst; stopper avledede rettigheter, beholder historikk. *Anbefalt ja (images/gjest-koble-koblet-v2).*
7. Full PalazzoEntity-mal som koblingens uttrykkelige tilgangsvalg, med de rettede bildetekstene (v2). *Anbefalt ja.*

## 7. Iterasjoner

| # | dato | hva endret seg |
|---|---|---|
| 1 | 2026-09-14 | Opprettet fra Kjetils tekst; tre og spørsmål som utkast; Astra-analyse bestilt |
| 2 | 2026-09-14 | Kjetils svar Q1–Q5 lagt inn: D1–D5 som bladformål (D4 senere), «begge tilbyr», opplevelsen som egen gren med ett-trykk/forståelig/trygt, beviset som gren med Q4′, celle. Seks G1-GUI-bilder rendret (images/). Astra-brief utvidet med Q4′ |
| 3 | 2026-09-14 kveld | Kjetil: «ja til (a)+(b) og til bildene» → G1 og G1-GUI satt. Astra-analysen (handoff/ASTRA_ANALYSE.md) lagt inn i §0-audit: tre bildetekster var usanne mot dagens mekanismer (nøkler på telefonen, «ingen data flyttes», «beviset slettes») → v2-bilder med rettede tekster; fire sikkerhetsforhold registrert som HD-0080/HD-0081; one-tap kvalifisert; D1 delt i to løp; §6 = Astras sju beslutninger med anbefaling. G2 venter |
