# Formålsspesifikasjon — Mistral med dagsgrense for studentene

Oppgavemappe: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_mistral-studentkvote_2026-11-15/` · Opprettet 2026-11-15 · Iterasjon 4 (ikke godkjent)

Målt mot: CellScaffold `9612217` (origin/main 15.11 01:58), CellProtocol `14fd9dc` (main), CellProtocolDocuments `c99467a`. Staging kjører CellScaffold `8e8f8e05` (audit 14.11).

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

Kjetils valg 15.11.2026 01:12Z på beslutningskortet i tråden «Sikre studentene språkmodellverktøy i HAVEN»:

> Lokal modell + Mistral-kvote

Kjetil 15.11.2026 22:26Z i tråden «Sikre studentene språkmodellverktøy i HAVEN» (ordrett):

> Vi må fange og si ifra på en god måte for brukeren at den ikke er tilgjengelig. Men hvorfor er det nede? Det oppfyller vel neppe formålet dens. Kjører den på ren cpu? Kallimachos bør bruke noe nyere enn 4o-mini. Men vi kan godt få det inn i DiMy's liste over tilgjengelige modeller - sammen med mistral og anthropic, hvor vi belaster mikrobetlinger for tokenbruk. Om det ikke er modent nok til å kjøre mikrobetalinger  må det fikses. Vi må også kjøre kvalitetstester med språkmodell drevet Kallimachos. (Bruk anledningen til å forbedre native matching også. )

Kjetil 20.11.2026 22:52Z, svar på spørsmål 3 (ordrett):

> 3. Kallimachos er en samling insrtuksjoner/prompter og tillatelser som definerer personaen Kallimachos som i prinsippet kan bruke hvilken som helst språkmodell. Altså en generell AI Gateway, kan være lokalt, mistral, openai, anthropic eller en modell på nanoGPT. Valget er opp til den som bruker og betaler for det. Bruk lokal, hostet av DiMy eller egne API nøkler eller abonnement. Vi bør tilgjengeliggjøre å kunne bruke Claude og Codex desktop også (via agent og mcp)

Kjetil 20.11.2026 22:53Z, svar på spørsmål 4 og 5 (ordrett):

> 4. gjør forslaget 5. ja

Denne oppgaven tar delen «hostede modeller i DiMys liste, belastet med mikrobetaling for tokenbruk», med Mistral først og studentenes kvote som første bruker. Den lokale modellen (hvorfor nede, CPU) og kvalitetstestene og native matching i Kallimachos hører til andre tråder (se §2).

Kortets innhold slik det ble lagt fram: gratis lokal Qwen som standard, Mistral på operatørens nøkkel med dagsgrense per student, og OpenAI-ruten (gpt-4o-mini) i Kallimachos «kapabel modell» stenges for studentkontoer.

| Påstand / antatt kapabilitet | Audit | Kilde (CellScaffold `9612217` med mindre annet står) |
|---|---|---|
| Studentene får ingen språkmodell på staging i dag | retrieved (audit 14.11) | `/mnt/project-files/masterhaven26/sprakmodell-audit-2026-11-14.md` |
| Det finnes en førstepartstjeneste for modellbruk på operatørens nøkkel med pris, dagsbudsjett, reservasjon, avregning og signert kvittering | retrieved | `Sources/App/Services/FirstPartyAIService.swift`, `FirstPartyAITariff.swift`, `FirstPartyAIConfiguration.swift`; ruter i `Controllers/VaporFirstPartyAI.swift` (`/ai-usage`, `/admin/ai-usage`) |
| Den tjenesten kan bruke Mistral | **contradicted** | `FirstPartyAIProvider.swift` har fast URL `https://api.openai.com/v1/responses`; `FirstPartyAIConfiguration.update` godtar bare nøkler som starter med `sk-` («Bruk en gyldig OpenAI-prosjektnøkkel») |
| `dailyLimitMinorUnits` er en grense per student | **contradicted** | `FirstPartyAIService.swift:65–76`: summerer *alle* rader for døgnet (`rows`, ikke `ownRows`). Det er et samlet døgnbudsjett for tjenesten. Per person finnes bare «høyst 500 forespørsler» og «ingen uavstemt forespørsel» |
| Hver forespørsel reserveres mot personens egen brukskvote i PaymentGate | retrieved | `FirstPartyAIService.swift:85` `reserveMeasuredUsage`; uten kvote gir PaymentGate `payment_required` (`PaymentGateCell.swift` ~3298) |
| Operatøren kan utstede ikke-overførbar brukskvote til en identitet | retrieved | `Cells/Admin/AdminFundingCell.swift` `issuePrepaid` (operatørrolle, `-w--`) |
| Mistral finnes som rute i AIGateway | retrieved | `AIGatewayModels.swift:1017` profil `mistral` (`mistral-large-4`, `https://api.mistral.ai`); egress-regel `AIGatewaySupport.swift:712` tillater bare `https://api.mistral.ai` |
| Butler har en låst EU-rute til Mistral | retrieved (ikke aktivert) | `Services/ButlerProviderCatalog.swift`: `https://api.eu.mistral.ai`, `mistral-small-2603`, ingen fallback. `Documentation/ButlerPaidModel.md`: «Ingen rute er aktivert … Ingen live transport, konto, modelltilgang eller nettgeografi er bevist» |
| `api.eu.mistral.ai` finnes og gir EU-inferens | recalled / ikke målt | Bare påstått i Butler-dokumentasjonen. Nettverket i denne økten når ikke Mistral (curl mot begge vertene: ingen forbindelse) |
| Kallimachos «kapabel» går til OpenAI gpt-4o-mini på operatørens nøkkel | retrieved | `Cells/AI/KallimachosAdvisorCell.swift:126–176` (standard `openai`, alias `openai`); bare samtykke kreves |
| Kallimachos har et «lokal»-nivå mot Qwen på 127.0.0.1:8083 | retrieved | `KallimachosAdvisorCell.swift:105–124`. På staging nås den ikke (tråden «Få språkmodellen på staging tilbake») |
| Det finnes et begrep «student» eller et kull i HAVEN | **contradicted** | Ingen celle, gruppe eller Agreement-mal for kull i `Sources/` (grep `student|cohort|kull` gir bare treff i konferanse- og spørreskjemaceller) |
| Tilgang skal avgjøres av Agreement-vilkår, likt i Swift, Python og Go | retrieved (Kjetils regel 28.10) | prosjektminnet `haven-access-via-agreement`; mønsteret i `CellBase/Cells/Chat/ChatCell.swift:1918` |
| #433 (Codex, utkast) lar Kallimachos bruke egen nøkkel eller en DiMy-ressurs | retrieved | CellScaffold PR #433, oppdatert 13.11, åpen |
| #435 (Codex) kobler Butler-invoke til PaymentGate og den låste Mistral-ruten | retrieved | CellScaffold PR #435, åpen; sier selv at realtransporten avviser EU-endepunktet |
| #440 gjør sikker nøkkelinnlegging nåbar fra Biblioteket | retrieved | CellScaffold PR #440, merget 15.11 00:49 |
| DiMy har en liste over modeller | retrieved | `Sources/App/Cells/ModelCatalog/` og `Resources/ModelCatalog/model-catalog.v1.json` (gjennomgått 06.11): OpenAI, Anthropic, Mistral, Google, lokal. Den er en oversikt med status og anbefalinger; den sier ikke hvilke modeller DiMy *tilbyr* med pris, og har ingen pris per modell |
| gpt-4o-mini er gammel | retrieved | Katalogen merker `gpt-4o-mini` som `retiring`; `mistral-small-2603` er `current`, `claude-haiku-5-5` og `claude-sonnet-5-5` er `current` |
| Mikrobetaling per kall finnes | retrieved, med to parallelle spor | (a) `FirstPartyAIService`: reservasjon i PaymentGate, måling av faktiske tokens, avregning, signert kvittering, avstemming. Bare OpenAI. (b) Butler S3c (#435, Codex): egen journal, PaymentGate-reservasjon, oppgjør, kvittering, låst til Mistral EU. Ingen av dem er koblet til Kallimachos eller modellkatalogen |
| Studentkvoten er regulatorisk lav risiko | retrieved (intern matrise, ikke juridisk råd) | `DiMyDocuments/ValueRedistribution/02_PRODUCT_VARIANT_AND_REGULATORY_MATRIX.md`: «Usage quota … Tillatt i v0», ikke overførbar, ingen innløsning, ingen ekstern aksept. Offisielle kilder sist sjekket i prosjektet 02.05.2026; ikke sjekket på nytt i denne økten (nettet når dem ikke herfra) |
| Mistral-prisen | recalled | Butler-fixturen (17.10, historisk): 155 810 / 623 238 cost ticks per 1000 input/output ≈ 1,6 kr / 6,2 kr per million tokens inkl. påslag. Ikke gjeldende pris |

## 1. Formålstre

Rot: **DiMy tilbyr hostede modeller fra en liste, og hvert kall belastes med mikrobetaling for faktisk tokenbruk. Første bruker er studentene: de får Mistral på en kvote operatøren gir, med dagsgrense, uten egen nøkkel og uten å betale selv.**

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.mistral-studentkvote.root | Modell for studentene innen en kjent kostnad | — | En student uten egen nøkkel får svar fra en modell i HAVEN; summen operatøren kan betale per student per døgn og totalt er satt og håndhevet | T-ROT: to studentkontoer bruker modellen på staging, web og Binding; den tredje kontoen (ikke student) får ikke Mistral | candidate |
| purpose://candidate.mistral-studentkvote.dimy-liste | Modeller DiMy tilbyr | root | Modellkatalogen sier for hver modell om DiMy tilbyr den: `offeredByDiMy`, `servingClass=hosted_provider`, `region`, `pricePerMTokInput`, `pricePerMTokOutput` (NOK, desimalstreng), leverandør og endepunkt. Feltnavnene er avtalt med PDD_formal-velger-modellkilde. Bare tilbudte modeller kan kalles på DiMys regning. Rekkefølge (Kjetil 20.11, sp. 5 «ja»): Mistral `mistral-small-2603` (EU) først, så `claude-haiku-5-5` og en OpenAI-modell som katalogen merker `current`, hver slått på med Kjetils ja og en tariff. nanoGPT kan legges til med samme mekanisme | T-LISTE: `catalog.offered` gir bare tilbudte modeller; et kall mot en modell som ikke er tilbudt avvises før transport | candidate |
| purpose://candidate.mistral-studentkvote.mikrobetaling | Ett målespor for alle hostede modeller | root | Alle kall til en tilbudt modell går gjennom samme målespor: reservasjon i PaymentGate før kall, faktiske tokens fra svaret, pris fra katalogens tariff, avregning og signert kvittering, avstemming ved ukjent utfall. Ingen kall uten reservasjon. Førstepartstjenesten gjøres leverandøruavhengig og knyttes til katalogen. Codex-eieren av #435 blir bedt om å la Butler bruke samme spor når #435 lander (Kjetil 20.11, sp. 4 «gjør forslaget») | T-MIKRO: samme fixture gir samme belastning og kvittering for Mistral og OpenAI; uten kvote ingen transport | candidate |
| purpose://candidate.mistral-studentkvote.kallimachos-modell | Kallimachos er en persona, ikke en modell | root | Kallimachos (instruksjoner, prompter, tillatelser) kan kjøre på hvilken som helst modell via AIGateway. Brukeren som betaler velger kilden: lokal, hostet av DiMy (kvote eller mikrobetaling), egen API-nøkkel eller eget abonnement (#433). Valget går gjennom samme kildevelger som PDD_formal-velger-modellkilde. Claude og Codex desktop via agent og MCP hører til tråden for egne agenter og knyttes til her, men bygges ikke her | T-KALLIMACHOS-KILDE: samme spørsmål med fire kilder gir samme persona og kildeinfo i svaret; ingen kilde valgt gir svar uten modell | candidate |
| purpose://candidate.mistral-studentkvote.hvem | Hvem er student | root | En konto er student når den har rolle-VC-en `InformasjonssystemerRoleCredential` med `role="student"` og `cohort="MasterHAVEN26"`, utstedt av gruppeentiteten Informasjonssystemer og sjekket med ProvedClaimCondition + TrustedIssuer (PDD i PR #46), likt i Swift, Python og Go. Tilbaketrukket eller utløpt VC stopper neste kall. Ukjent status (speilet eldre enn 10 min) gir `role_status_unknown`, ikke «ikke student» | T-HVEM: positiv + negative (fremmed, tilbaketrukket, utløpt, ukjent status) | candidate |
| purpose://candidate.mistral-studentkvote.mistral | Mistral som leverandør i førstepartstjenesten | mikrobetaling | Tjenesten kan kalle Mistral (chat completions, fast URL, ingen omdirigering, ingen fallback til annen leverandør) og leser faktiske brukstall fra svaret; nøkkelen lagres forseglet og vises aldri | T-MISTRAL (fake transport + fixture), T-MISTRAL-LIVE (ett ekte kall etter Kjetils ja) | candidate |
| purpose://candidate.mistral-studentkvote.dagsgrense | Dagsgrense per student | root | Ingen student kan bruke mer enn grensen per døgn (Europe/Oslo). Kallet som ville gått over, avvises før leverandøren kalles. Tjenestens samlede døgnbudsjett gjelder i tillegg | T-DAG: 20 kall på grensen gir nøyaktig så mange som får plass; neste avvises uten leverandørkall; ny dag åpner igjen | candidate |
| purpose://candidate.mistral-studentkvote.tak | Totaltak per student (semester) | root | Operatøren utsteder en ikke-overførbar kvote per student ved opptak; når den er brukt, stopper Mistral for den studenten | T-TAK (bruker eksisterende `issuePrepaid` + `payment_required`) | candidate |
| purpose://candidate.mistral-studentkvote.lokal-forst | Lokal modell først | root | Når den lokale modellen svarer, brukes den, gratis og uten å røre kvoten. Mistral brukes når studenten velger det eller den lokale er nede. Uten noen modell faller flaten tilbake til svar uten modell, med beskjed | T-LOKAL (lokal oppe / nede / kvote tom) | candidate |
| purpose://candidate.mistral-studentkvote.betaler-velger | Ingen kall på operatørens regning uten at brukeren har valgt det | root | Ingen persona eller flate kaller en hostet modell på DiMys nøkkel uten at brukeren har valgt «hostet av DiMy» og har kvote. Kallimachos' faste OpenAI-rute på operatørens nøkkel fjernes. Egen nøkkel belastes brukerens egen konto og rører ikke kvoten | T-BETALER: transportspion viser null kall på operatørens nøkkel for en konto uten valg eller kvote | candidate |
| purpose://candidate.mistral-studentkvote.synlig | Studenten ser modell og kvote | root | Ved hvert svar står hvilken modell som svarte (lokal / Mistral EU) og hva som er igjen i dag og i semesteret; når kvoten er brukt, står det når den fornyes | T-SYNLIG + bilder (G1-GUI) | candidate |
| purpose://candidate.mistral-studentkvote.drift | Operatøren styrer og ser kostnaden | root | Kjetil kan slå Mistral av/på, sette dagsgrense og tak, og se forbruk per student og totalt i `/admin/ai-usage`; leverandørmodus krever eksplisitt bekreftelse | T-DRIFT | candidate |
| purpose://candidate.mistral-studentkvote.en-port | Én port for alle studentverktøy | root | Kallimachos, Butler og de nye flatene (tekstanalyse, skrivehjelp, skeletonhjelp, felles chat) spør samme Swift-funksjon om studentens modell, i stedet for å bygge hver sin rute | T-EN-PORT: grep + test at hvert verktøy går gjennom porten | candidate |
| purpose://candidate.mistral-studentkvote.svarform | Felles svarform for kvote | en-port | Kallet går alltid med den spørrende studentens identitet og trekker fra hens kvote. Hvert svar og hvert avslag har `quota` med `remainingTodayMinorUnits`, `dailyLimitMinorUnits`, `remainingCallsToday` og `dailyCallLimit` (antatt antall kall ut fra taket per kall), `resetsAt`. Avslag har egen kode: `student_quota_exhausted_today`, `student_quota_exhausted_term`, `service_budget_exhausted`, `not_eligible`, `role_status_unknown` | T-SVARFORM | candidate |

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke å finne ut hvorfor den lokale modellen er nede eller om den kjører på CPU. Det eies av tråden «Få språkmodellen på staging tilbake».
- Ikke kvalitetstester av Kallimachos med modell eller bedre native matching. Det er egne oppgaver i tråden «Sikre studentene språkmodellverktøy i HAVEN».
- Ikke ekte innbetaling (Stripe/Vipps) eller lommebok. Kvoten er en ikke-overførbar brukskvote fra én utsteder, uten innløsning og uten ekstern aksept (matrisens «Usage quota», v0). Overføring mellom studenter, innløsning eller aksept hos andre er harde stopp. Dette er ikke juridisk råd.
- Ikke ekte betaling fra studentene. Kvoten er operatørfinansiert, ikke-overførbar og kan ikke innløses (samme vilkår som `issuePrepaid`).
- Ikke å få den lokale Qwen-modellen opp på staging. Det eies av tråden «Få språkmodellen på staging tilbake»; her brukes den når den svarer.
- Ikke Butlers betalte modell (#435) eller Kallimachos med egen nøkkel/DiMy-ressurs (#433). De er Codex sitt arbeid; denne oppgaven skal ikke duplisere dem, og koordineres med eierne (se §6 sp. 4).
- Ikke nye verktøy (tekstanalyse, skrivehjelp, skeletonhjelp, felles chat). De bruker porten herfra når den finnes.
- Ikke å slå på betalt bruk eller legge inn nøkkelen. Det krever Kjetils eksplisitte ja i tråden, etter G3 på testmodus.
- Ikke en Python/Go-port av førstepartstjenesten (den finnes bare i CellScaffold). Studentvilkåret bygges som en vanlig Agreement-betingelse som finnes i alle tre språk.

Avhengigheter (hver måles før den egentlige testen):
| Kapabilitet | Kilde (fil) | Avgrensning | Målt? |
|---|---|---|---|
| Førstepartstjenesten virker i simulert modus | `Tests/AppTests/FirstPartyAIUsageTests.swift` | OpenAI-format | ikke kjørt her (ingen Swift i økten); kjøres i CI før endring |
| Førstepartstjenestens modus på staging | `/admin/ai-usage` | | **ikke målt** (krever operatørinnlogging) |
| PaymentGate gir `payment_required` uten kvote | `PaymentGateCell.swift` ~3298 | | lest i kode, ikke målt |
| Mistral-endepunkt og modellnavn | `ButlerProviderCatalog.swift` | | **ikke målt**: når ikke Mistral herfra; krever ett ekte kall med nøkkelen |
| Agreement-vilkår «invitasjon akseptert» | `ChatCell.swift:1918` | | målt 28.10 i interop-matrisen (27/27) |
| Kallimachos lokal-nivå på staging | `KallimachosAdvisorCell.swift:105` | | målt 14.11: **nede** |
| Binding viser Kallimachos-flaten | Binding | | ikke målt i denne oppgaven |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Studentens svar med modellnavn og gjenstående kvote (fylt) | bilde, så kjørende flate | Kallimachos på staging, web og Binding | `images/kvote-fylt-laptop-v1.png`, `-iphone-v1.png` (lages etter G1) | nei |
| Kvoten er brukt opp i dag | bilde, så kjørende flate | samme | `images/kvote-tom-…-v1.png` | nei |
| Ikke student: ingen Mistral, forklaring | bilde, så kjørende flate | samme | `images/ikke-student-…-v1.png` | nei |
| Operatørens innstillinger og forbruk per student | bilde, så kjørende flate | `/admin/ai-usage` | `images/drift-…-v1.png` | nei |
| Swift-endringer med tester | PR | CellScaffold (+ CellProtocol hvis vilkåret trenger det) | — | nei |
| Testutdata for alle §5-rader | fil | `TESTRESULT.md` | — | nei |
| FORESPOERSEL til HAVEN-Deploy etter grønt bygg | fil | `/Users/kjetil/Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/RELEASE/` | — | nei |

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
    - artefakt skeleton/ (port G1-GUI): CellConfiguration/skeleton-JSON som bildet er rendret fra. Er bildet en mockup i stedet for Porthole-preview, kreves i stedet en renderingserklæring i images/README.md som lister hva skjelettet ikke kan rendre.
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
- **lesson.a-conditional-artifact-must-still-cost-something** (2026-09-18, minor): purpose_dev.py validate ble rød på PDD_entitetsdata-egen-kontroll fordi artefaktet 'skeleton/' manglet, selv om G1-GUI var godkjent på bilder Kjetil faktisk hadde sett. Pakken beskrev artefaktet som påkrevd «når Porthole-preview er brukt»; validatoren krevde det alltid.
    - forebygging: Et betinget krav oppfylles av et *annet krav*, aldri av et fravær. Feltet 'satisfiedByDeclaration' peker på en fil og en overskrift og krever minst ett punkt under den: enten viser du skjelett-JSON-en bildet er rendret fra, eller du skriver ned hva skjelettet ikke kan rendre. Begge tvinger frem spørsmålet «kan flaten dette?». Feilmeldingen navngir begge veier ut. Sjekket begge veier: rød uten erklæring, grønn med.
- **lesson.location-is-not-ownership** (2026-09-22, major): dataflow.md begrunnet at AIGateway matte ligge i appen med at «en gateway utenfor entiteten gjor prompten til noen andres data». Kjetil: en celle i skyen som eies av meg er pr definisjon innenfor min entitet.
    - forebygging: Regelen er uniform og gjelder alle scaffolds likt: ingen andre, scaffold-admin inkludert, nar data ELLER funksjonalitet i en celle jeg eier uten en Agreement som sier det. Et vern som bare gjelder skyen er et tegn pa at grensen er tegnet feil. Negative tester skal kjores i begge oppsett, lokalt og sky, og gi samme svar — og de skal dekke handlinger, ikke bare felter. Den positive motsatsen ma ogsa testes: en Agreement apner nayktig sitt eget omfang.
- **lesson.read-origin-main-before-writing-a-mechanism** (2026-09-22, major): Runde 1 av PDD_entitetsdata skrev en egen resolver for lenkede identiteter (EntityLinkAuthorizer, ny CellAuthorizationPath.linkedIdentity, ny hook pa GeneralCell). Da patchen ble lagt mot origin/main viste det seg at IdentityLinkRegistry og GeneralCell.authorizationEvidence allerede gjorde det samme, landet av en annen oppgave (purpose://candidate.entity-link.resolver-honours-link). Hele resolveren ble forkastet.
    - forebygging: Brief-audit skal si HVILKEN revisjon noe ble lest fra, og for et formal som skal endre en mekanisme skal kilden vaere origin/main (git show origin/main:<fil>), ikke utsjekket. Preflight-skriptet sjekker na at patchen passer mot origin/main i et eget worktree for noe legges pa. Og: for du skriver en mekanisme, grep pa main etter navnet pa det den skal gjore (her: sameEntity, linkedIdentity) - ikke bare etter typen du planlegger a lage.
- **lesson.method-lived-only-on-one-machine** (2026-09-24, major): Metoden selv — Book 35 (PDD-arbeidsflyten), Book 36, lærdomsregisteret med 50 lærdommer, formålspakkene, purpose_dev.py — lå bare i ett utsjekk på Kjetils Mac på grenen codex/docs-cleanup-20260810, aldri på main; derfor verken i HAVEN eller hos andre utviklere.
    - forebygging: Metodeartefakter landes som kode: PR til main og pin-oppdatering i HAVEN. Test: git cat-file -e origin/main:<fil> for hver metodefil.
- **lesson.downstream-pin-must-come-from-the-consumer** (2026-09-24, major): Nedstrøms-baselinen for CellScaffold var rød 22.09 («cellprotocol krever swift-crypto 4.5.2, dimymint krever 3.x») og ble rapportert som prosjektets blokkering. CellScaffold main pinnet DiMyMint af41630, som løser swift-crypto 4.x; skriptet hadde hardkodet en eldre revisjon (1718fda).
    - forebygging: Et nedstrøms-skript leser alle transitive pinner fra forbrukerens egen Package.swift/Package.resolved på origin/main ved kjøring, og logger dem. En rød avhengighetsoppløsning i et skript med hardkodede pinner er ikke et funn før pinnene er bekreftet mot forbrukerens resolved.
- **lesson.disposable-worktree-must-be-reset-before-checkout** (2026-09-24, minor): pdd-check/Binding ble stående på 72f6a6c9 i to kjøringer selv om skriptet ba om origin/main: «Your local changes to project.pbxproj would be overwritten by checkout». Baselinen målte feil Binding-revisjon uten å si fra.
    - forebygging: Engangs-worktrees resettes hardt (`git reset --hard` + fjern Package.resolved) før hver utsjekk, og skriptet skriver ut revisjonen den faktisk står på — en avvikende revisjon skal stoppe kjøringen, ikke logges forbi.
- **lesson.report-the-commit-you-pushed-not-the-one-you-planned** (2026-09-24, minor): TESTRESULT og PLAN sa «commit ebb0b7f». Branchen sto på e66b7f1 — commit.sh hadde laget en ny hash — og var ikke pushet. Push-skriptets EXPECT måtte rettes før det kunne kjøre.
    - forebygging: Etter hver commit/push: les `git rev-parse --short HEAD` og `git ls-remote --heads origin <branch>` og lim inn utdataene i STATUS/TESTRESULT. Sjekk også for remote-tracking ref før du sier «pushet» (lesson.branch-is-empty-after-eight-work-packages, samme familie).
- **lesson.lookup-again-when-a-surface-is-added** (2026-09-24, major): De nye seksjonene i «Utvid entiteten» (B10) var portet på synlighet med rot-scope, og listen med verktøyets forespørsel forsvant — samme feil som lesson.unresolvable-condition-is-invisible fra 05.09.
    - forebygging: For hver ny eller endret skjelettflate: kjør `purpose_dev.py lookup --tags skeleton gui` før utformingen, og `BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` + `testPersonalCopilotLocalSurfacesLoadWithoutReferenceFailures` før flaten vises eller committes.
- **lesson.picker-state-keypath-is-read-and-written** (2026-09-24, minor): Velgeren «Verktøy» i «Gi tilgang» sto på «Velg verktøy» selv om cellen hadde valgt verktøyet.
    - forebygging: `selectionStateKeypath` skal være en nøkkel cellen både leser (`{selected}`) og skriver; test rundturen (`pickerSelectionRoundTrips`).
- **lesson.pairing-can-outlive-the-identity** (2026-09-24, major): Agenten var paret med en HAVEN-identitet fra 4. mai («Binding Local Session», nøkkel 13BF…), mens HAVEN brukte en annen privat identitet (D362…, identitetsfilen skrevet 18.09). Svar fra HAVEN ville blitt avvist; ingen test i noen av endene kunne se det.
    - forebygging: En flate som ber eieren signere for agenten sammenligner egen nøkkel med agentens forankring og viser forskjellen før signering, med vei til ny paring (test: `offerIsRefusedHereWhenThisHavenHoldsAnotherKey`, `theOwnerNeverSignsWhatFailedTheCheck`). Sjekk nøkkelkontinuitet før live-test av noe som signeres.
- **lesson.screencapture-from-runner-can-fail** (2026-09-24, minor): `screencapture -l <vindu>` fra jobbløperen ga «could not create image from window» for HAVEN-vinduet, med samme vindus-ID som computer use så.
    - forebygging: Ta bilder av flater med computer use (eller be Kjetil), og ikke planlegg bevis som avhenger av `screencapture` fra løperen før det er målt at det virker den dagen.
- **lesson.sketch-assumed-a-renderer-it-did-not-have** (2026-09-25, major): Skissen v2 (HTML) var venstrestilt, men «Utvid entiteten» i HAVEN viste all tekst sentrert, også etter at hAlignment «leading» var satt.
    - forebygging: Før en skisse godkjennes: finn CellProtocol-committen HAVEN-bygget bruker, les hvordan Text/VStack/HStack rendres der, og list i §3 hva den ikke kan (her: venstrestilt tekst). Et HTML-bilde er ikke bevis for at rendreren kan det samme.
- **lesson.maxwidthinfinity-also-stretches-height** (2026-09-25, minor): En tekst i en listerad ble kuttet med «…» etter fem linjer når en HStack med wrap og maxWidthInfinity sto i samme rad; uten maxWidthInfinity ble teksten hel.
    - forebygging: Ikke sett maxWidthInfinity på elementer i listerader. Se etter «…» i skjermbildet av hver rad med lang tekst, i et smalt vindu.
- **lesson.wrap-gives-each-item-its-ideal-width** (2026-09-25, minor): Knappen «Par agenten med denne HAVEN-en» gikk ut over kortet og ble klippet i et smalt vindu.
    - forebygging: Knapper i vanlig HStack, som kan krympe og bryte teksten; wrap bare for korte merkelapper. Se på flaten i et smalt vindu før den vises fram.
- **lesson.empty-list-keeps-its-slot** (2026-09-25, minor): Tomme lister og tomme tekster ga store hull i «Utvid entiteten».
    - forebygging: Én liste per kort, der cellen bestemmer radene (`kind`) og en rad med en kort linje står der det ellers ville vært tomt. Ingen faste høyder på lister, og ingen tekst på toppnivå som kan bli tom.
- **lesson.pgrep-pattern-must-allow-arguments** (2026-09-25, minor): Byggejobben avsluttet ikke HAVEN, og `open` hentet bare fram det gamle bygget (startet 24.09 17:29) i stedet for å starte det nye.
    - forebygging: Bruk 'HAVEN( |$)' i mønsteret, og skriv ut prosessens starttid etter omstart og sammenlign den med byggetiden før noe vises fram.
- **lesson.computer-use-image-is-not-a-file** (2026-09-25, minor): Skjermbildene av den nye flaten kunne ikke sendes til Kjetil som fil; vinduet var i tillegg på et annet skrivebord og kunne ikke gjøres større i bakgrunnen.
    - forebygging: Planlegg bildebeviset med en vei som gir en fil (Kjetils eget skjermbilde, eller skjermopptakstilgang for løperen), og si det før arbeidet, ikke etter.
- **lesson.text-field-sends-a-string** (2026-09-25, major): Adressefeltet i «Utvid entiteten» kunne aldri starte en forespørsel: Enter ga alltid «Si hvilket scaffold dette gjelder — `audience` …».
    - forebygging: For hvert tekstfelt: en kontraktstest som sender feltets egen payload (.string) til targetKeypath og venter et svar som ikke er feil.
- **lesson.green-gate-must-read-the-last-summary-line** (2026-09-26, major): runde2.sh committet og pushet 399f6d2 med 4 røde tester. Porten grep'et «Executed … with 0 failures» i hele loggen og traff en grønn suites linje lenger opp; siste linje sa «1262 tests, with 2 tests skipped and 8 failures».
    - forebygging: En grønn-port leser bare den siste «Executed»-linjen (tail -1) og krever « 0 failures (0 unexpected)». Sammenligningen gjøres uten pipe (POSIX case), fordi `echo | grep -q` under pipefail kan gi rødt på grønt (SIGPIPE). Porten skriver ut nøyaktig hva den sammenlignet.
- **lesson.module-and-type-share-a-name-in-cellprotocol** (2026-09-26, minor): `CellApple.EntityAnchorCell` og `CellVapor.EntityAnchorCell` kompilerte ikke: «type 'CellApple' has no member 'EntityAnchorCell'». Begge modulene har en type med samme navn som modulen.
    - forebygging: Én fil per modul som importerer bare den ene og gir typen et unikt typealias (TestSupport/AppleEntityAnchorAlias.swift, VaporEntityAnchorAlias.swift). Testfilen importerer ingen av modulene direkte.
- **lesson.placeholder-example-leaks-into-judgement** (2026-09-28, minor): I «Dommerbenken — chat» v2 var plassholderen i fritekstfeltet «f.eks. «status på prosjektet»». Kjetil skrev nøyaktig «status på prosjektet» som sin egen tolkning i to av tretti saker («hvor står vi nå på prosjektet», «hva står igjen»). Eksempelet var hentet fra meningen til en sak i settet.
    - forebygging: Eksempler, plassholdere og hjelpetekst i en dommerflate skal hentes fra et domene som ikke finnes i settet, og testes: ingen sak i settet skal ha gold hvis tittel eller alias overlapper eksempelteksten. Rapporter saker der dommerens fritekst er lik eksempelet som svakere.
- **lesson.host-mutation-without-reading-the-coordination-file** (2026-10-02, major): 30.09 satte en Claude-tråd ut en gren-commit på staging og byttet invitasjonene, med Kjetils ja, men uten claim. En Codex-tråd hadde claim på samme container (HD-0141), staging var reservert for 2026.9.4, og deploykøen trodde i to døgn at staging kjørte forrige utgivelse.
    - forebygging: Før enhver vertsmutasjon: les `_losen-queue/KOORDINERING.md`, kjør `hd coord status`, ta egen claim på en HD-oppgave, og før utsettingen inn i køen etterpå. Test: jobbloggen for utsettingen viser `hd coord status` uten annen claim på samme tjeneste, og egen claim, før første kommando mot verten. Eierens ja til å sette ut erstatter ikke sjekken.
- **lesson.remembered-install-state-is-not-measured** (2026-10-02, minor): En plan sa at agenten på Macen var bygget fra en bestemt gren, og bygde grenvalg og et åpent spørsmål til eieren på det. Agenten var installert på nytt fra `main` av en annen tråd seks dager tidligere.
    - forebygging: Hva som er installert, måles før en plan bygger på det: dato og navn på binærene og sikkerhetskopiene i `bin/`, `launchctl print`, og om commiten er på `origin/main`. Test: påstandstabellen merker installasjonstilstand som hentet med måletidspunkt, aldri som husket.
- **lesson.own-committed-tests-changed-without-asking** (2026-10-03, major): Ti tester tråden selv hadde committet tidligere samme dag, ble endret uten å spørre: tretten endringer, og sju av dem snudde eller fjernet noe en test krevde godtatt.
    - forebygging: En committet test er eksisterende, uansett hvem som skrev den og når. Før hver commit leses testendringene rett fra git; en endring i en committet test er et spørsmål til eieren. Test: skriptet som lister testendringer fra git, viser ingen endring i en committet test uten en godkjenning ført i STATUS.md.
- **lesson.accept-written-from-memory-had-27-errors** (2026-10-03, major): Første utkast til ACCEPT.md og TESTRESULT.md hadde 27 feil da en uavhengig tråd holdt det mot bevisfilene; ett av dem var påstanden om at hver frosset utgave ble angrepet etter at den var satt ut.
    - forebygging: Tall, klokkeslett, commit-numre og sitater i ACCEPT.md og TESTRESULT.md fylles inn fra bevisfilene av kode, og en uavhengig tråd holder hver påstand mot bevisene før eieren får dokumentene. Test: rapporten fra kontrollen ligger blant bevisene, med en dom per påstand.
- **lesson.red-first-claimed-for-tests-that-were-not** (2026-10-04, minor): TESTRESULT.md sa at hver ny eller endret test var kjørt rød først. Tolv endringer i tester som alt fantes, og ti av de 24 nye i første runde, kom inn sammen med koden og var aldri kjørt røde.
    - forebygging: En påstand om alle tester føres per test: «rød først» listes med hvilke tester som fantes i den røde kjøringen, og hvilke som kom til etterpå. Test: antall tester i den røde og i den grønne kjøringen står i TESTRESULT.md, og differansen er forklart.
- **lesson.estimate-assumed-one-attack-round** (2026-10-04, minor): Planen sa «rundt tre og en halv time etter G1». Den siste utgaven var målt på nett 34 timer og 50 minutter etter.
    - forebygging: Et anslag for arbeid som skal angripes av en uavhengig tråd, oppgis per runde, og sier at antall runder er ukjent til første angrep er målt. Test: planen har tid per runde, ikke en sluttid.
- **lesson.full-path-rule-broken-in-short-references** (2026-10-05, major): Kjetil måtte for tredje gang si at filer skal stå med hele stien («Du må legge med hele banen til filer som dette: ACCEPT.md»): meldingene og spørsmålene ved G3 hadde bare filnavnet.
    - forebygging: Hver melding til eieren kontrolleres maskinelt før den sendes: et ord som ender på en filendelse og ikke begynner med en rot, stopper sendingen. Det gjelder hver gang en fil nevnes, også i spørsmål. Test: skriptet som kontrollerer meldinger, gir null funn på hver melding som ber om en port.
- **lesson.file-copied-to-the-mac-was-the-previous-version** (2026-10-05, major): En commit gikk ut med testen, men uten endringen den prøvde: filkopien fra skyøkten til Macen meldte «written», og fila på Macen var forrige utgave. To skript mistet dessuten kjørbar-biten på veien.
    - forebygging: Hver utgave som skal til Macen, legges under et nytt filnavn i utdatamappen. Sjekksummen på Macen sammenlignes med den i skyen i et eget steg, og neste steg (commit eller køjobb) startes ikke i samme kommando. Test: commit-jobben viser «git diff --cached --stat --summary» før commit, og lista over filer og moduser sammenlignes med det som skulle med.
- **lesson.pr-opened-without-reading-the-base-branch-ci** (2026-10-05, minor): PR #30 ble opprettet uten at CI-tilstanden på main var lest: løpet sto til tidsgrensen på 25 minutter av en grunn som hadde stått på main i seks dager, og den første lesningen av loggen, at det stoppet før PR-ens tester hadde startet, ble felt av den uavhengige kontrollen.
    - forebygging: Før en PR opprettes, listes løpene for basisgrenen; har hodet ikke noe grønt løp med samme testskript, rettes det først, eller rettelsen tas med. Før en årsak skrives ned for et rødt løp, leses avsnittet om CI i skillen, og siste linje i en logg kalles ikke stedet det stoppet. Test: skriptet som oppretter en PR, viser siste løp på basisgrenen og stopper når det er rødt.
- **lesson.status-message-sent-before-the-documents-were-checked** (2026-10-06, minor): Dokumentene og meldingen til eieren 06.10 om kvelden skrev slutninger som målinger («haven-deploy ville blitt kjørt med umask 077», «skallet ventet fem sekunder: målt»), gjenga kontrollenes merknader som «en feil» og «alle rettet», utelot ett av fire svar der en vakt ble beskrevet, og ga et klokkeslett for når en kjøring ville være ferdig, uten grunnlag. Meldingen var sendt et kvarter før kontrollen av dokumentene.
    - forebygging: Dokumenter, LES-MEG ved siden av et skript og meldingen til eieren kontrolleres mot kildene av en som ikke har skrevet dem, før meldingen sendes. Ved hver påstand står det om den er målt, lest eller sluttet, og et tidsanslag gis som et spenn med grunnlaget. Test: kontrollrapporten er eldre enn meldingen, og rettelser gjort etter kontrollen er merket som ukontrollert.
- **lesson.commit-file-built-on-a-stale-copy-and-the-check-got-the-same-copy** (2026-10-06, major): README.md i commiten `c5058f49` fikk 172 endrede linjer (104 ut, 68 inn) der rundt 50 nye var ventet: tekst fra tre tidligere commiter falt ut.
    - forebygging: Hver fil i en commit-pakke bygges på git-objektet i foreldercommiten, og skriptet som committer, krever ventet antall linjer inn og ut per fil og stopper ellers. Kontrolltråden får commiten og finner grunnlaget selv. Test: skriptet stopper når forskjellen mot forelderen ikke er den ventede.
- **lesson.brake-file-written-after-the-chain-had-passed-the-brake** (2026-10-06, minor): Bremsefilen ble lagt 13 sekunder etter at kjedeskriptet hadde passert bremsesjekken foran pushen, så en commit med en kjent feil ble pushet.
    - forebygging: Et tall et menneske må lese før neste steg som ikke kan angres, deler kjeden i to jobber, eller skriptet krever tallet selv. Test: kjeden stopper foran pushen når commitens linjetall avviker fra det ventede.
- **lesson.check-ran-before-the-last-numbers-and-did-not-read-the-message** (2026-10-06, minor): Kontrollen av akseptdokumentet ble gjort før de 27 siste kallene var målt, og meldingen til eieren var ikke med. En ny kontroll rett før sending fant åtte ting, blant annet at meldingen la en svakhet til angrepet alene der råsvarene fra nett viste det samme.
    - forebygging: Den siste uavhengige kontrollen kommer etter at siste tall er ført inn, regner tallene på nytt fra råfilene og leser meldingen eieren får. Test: kontrollrapporten er yngre enn siste bevisfil og eldre enn meldingen.
- **lesson.approved-image-had-no-way-to-be-photographed-on-the-live-page** (2026-10-06, minor): Telefonbildet som ble godkjent ved G1-GUI, kunne ikke få et skjermbilde fra nett ved siden av seg ved G3: nettleserverktøyet holder vinduet på 1280 punkter, og siden nekter å bli vist i en ramme.
    - forebygging: Ved G1-GUI står det for hvert bilde hvordan motstykket på nett skal tas ved G3, og veien er prøvd én gang mot siden slik den står. Kan et bilde ikke tas, sies det ved G1-GUI. Test: hvert godkjent bilde har en navngitt opptaksvei som har gitt en fil.
- **lesson.early-return-rule-changed-what-happens-when-the-lookup-is-down** (2026-10-06, minor): Et spørsmål med et ord fra ordlisten får henvisningen (HTTP 200) også når oppslaget ikke kan nås, der andre spørsmål får 503 eller 403. Det sto verken i spesifikasjonen eller i en test.
    - forebygging: For hver regel som svarer før en avhengighet spørres, sier spesifikasjonen hva som skjer når avhengigheten er nede, og en test holder det fast. Test: en test der avhengigheten er tatt bort, med ventet svar for begge grener.
- **lesson.way-back-was-called-a-way-back-after-dry-runs-only** (2026-10-06, minor): Veien tilbake fra utsettingen er tørrkjørt to ganger, men selve byttet tilbake er aldri kjørt, der spesifikasjonen krever en vei som virker også når siden er nede.
    - forebygging: En vei tilbake er vist når byttet er kjørt, for eksempel mot en egen container med samme image. Ellers står den som «ikke vist» i planen eieren godkjenner. Test: bevis for et gjennomført bytte, eller linjen «ikke vist» i planen.
- **lesson.order-of-steps-changed-to-keep-a-promised-time** (2026-10-06, minor): Utgaven ble satt ut før rettelsen av README.md var committet, mot planen, fordi kontrollen av rettelsen tok 28 minutter der 15 var ventet.
    - forebygging: Planen sier hvilke steg som kan bytte plass når noe tar lengre tid, og kontroller får en hard tidsgrense. Test: hvert planbytte har en linje i STATUS.md med hva som tapes.
- **lesson.correction-to-a-list-removed-words-it-already-caught** (2026-10-06, minor): To rettelser i ordlisten ga nye hull: et unntak som ble sammenlignet etter at ø var brettet til o, tok bort «nøtte», og en innsnevring tok bort «tolererer».
    - forebygging: Hver utgave av en liste kjøres mot alle tidligere eksempler, både ord som skal treffe og ord som ikke skal, og eksemplene ligger som fikstur. Test: en fikstur med ett eksempelord per oppføring og en liste med ord som ikke skal treffe.
- **lesson.rewritten-draft-got-new-errors-where-it-was-rewritten** (2026-10-06, minor): Seks utkast til spesifikasjonen ble lest i fem kontrollrunder som fant 110 ting til sammen. Hver runde fant feil i det som var skrevet om etter den forrige.
    - forebygging: Etter en omskriving kontrolleres det omskrevne på nytt, og eieren får vite når siste utgave ikke er kontrollert. Tall fylles inn av kode. Test: dokumentet sier hvilken utgave kontrollen leste.
- **lesson.known-pitfall-repeated-in-a-small-follow-up-without-lookup** (2026-10-06, minor): Testen for avvik 4 sammenlignet to like svarkonvolutter med `XCTAssertEqual` og var rød mot riktig kode. Den grønne kjøringen fanget det før commit.
    - forebygging: `lookup` kjøres for hvert steg som skriver kode eller tester, også små oppfølginger, og oppgaven til kontrolltråden ber den holde testen mot lærdommene for taggene. Test: commit-trinnet stopper uten grønt bevis for nettopp filene som committes.
- **lesson.full-path-rule-passed-the-checker-in-descriptions-and-file-cards** (2026-10-06, minor): Meldingen som ba om G3, gikk gjennom kontrollskriptet for hele banen, men fem filer ble sendt som kort uten bane i sendingen, og dokumenter ble nevnt med en beskrivelse («akseptdokumentet») før banen sto.
    - forebygging: Hver fil som leveres i samtalen, står med hele banen i meldingen som følger med, og en beskrivelse av en fil får banen ved første nevning. Test: antall leverte filer er lik antall baner i meldingen.
- **lesson.status-did-not-say-status-or-what-to-do** (2026-10-06, major): Eieren 06.10 om statusen han fikk: «Dette sier meg ingenting om hva status er eller hva jeg skal gjøre.» Han skrev selv formålet og spurte hva som gjensto for å få prøvd med de to mottakerne.
    - forebygging: En statusmelding åpner med hvor formålet står for dem det gjelder, så det eieren skal gjøre i nummererte punkter, så leddene som gjenstår. Arbeid på et sidespor kalles et sidespor. Test: kontrolløren får eierens ord fra §0 og svarer på om første avsnitt sier hva mottakerne har fått.
- **lesson.few-steps-was-counted-for-the-recipient-and-not-for-the-owner** (2026-10-07, minor): Utkastet til G1 talte tre håndgrep for mottakeren og skrev «én gang per person» for eieren («ett trykk» i spesifikasjonen bak). Bildet viste to Touch ID per person og en kode å sammenligne, og rekkefølgen på eierens steg sto feil. Kontrollen før framlegget fant det.
    - forebygging: Der «få håndgrep» er et formål, telles håndgrepene for hver part, eieren først, per person og per runde, fra bildene og i rekkefølgen de skjer. Et steg som følger av et forslag, merkes som forslag. Test: et opptak på en ren maskin der håndgrepene er telt.
- **lesson.a-second-safeguard-hid-that-the-first-had-no-test** (2026-10-06, major): Én av 145 innsatte feil, kalt nr. 100 i filnavnene for omkjøringen («fila legges tilbake mens haven-deploy kanskje går»), ble ikke fanget, og alle 133 testene var grønne med den.
    - forebygging: To vern foran samme handling får hver sin test der det andre ikke kan svare. En innsatt feil som ingen test fanger, leses i utskriften før den regnes som ufarlig. Test: for hvert vern finnes et tilfelle der bare det vernet står mellom skriptet og handlingen.
- **lesson.deadline-request-left-out-what-follows-when-it-passes** (2026-10-06, minor): Utkastet til meldingen etter byttet ba eieren godkjenne to forespørsler innen 24 timer, uten å si at invitasjonen da er brukt opp og at en ny trengs (etter kontrollørens lesning: nytt bytte og ny omstart av staging), og uten steget etter: hans godkjenning av mottakernes egne forespørsler. Kontrollen før sending fant det.
    - forebygging: En forespørsel med frist sier hva som skjer når fristen går ut, og nevner hvert senere steg som er eierens. Test: kontrolløren spør for hver frist i meldingen «hva følger hvis den ikke holdes?» og «hva er hans neste steg etter dette?».
- **lesson.question-used-the-repos-words-and-came-back-as-a-question** (2026-10-07, minor): To av fem nummererte punkter til eieren kom tilbake som spørsmål: «Hva gjør assistentidentiteten?» og «Hva mener du med at vedlegg kan gå til main? Vi skal ikke lagre vedlegg i git så forklar hva du mener.»
    - forebygging: Et spørsmål til eieren bruker hans ord og sier hva en ting gjør før det spør om den. Test: kontrolløren leser hvert spørsmål, slik det blir sendt, som en som ikke kjenner repoet, og sier hvilke ord som må forklares.
- **lesson.render-candidate-skeleton-with-the-web-renderer-before-g1-gui** (2026-10-02, major): G1-GUI-bilder har vært mockups (butler-PDD-en) eller krevd en kjørende CellScaffold med Porthole-preview. Begge gir enten feil piksler eller en byggerunde før Kjetil får se noe.
    - forebygging: For en ny flate: eksporter de to filene fra CellScaffold origin/main (md5 i images/README.md), rendre kandidat-skjelett-JSON med eksempeldata i Playwright/Chromium (images/render.js i PDD_lister), lagre bildene som G1-GUI-referanse og mål oppførsel (onAction-payloads) i samme kjøring. Etter implementering: en test som krever at Swift-fabrikken gir kanonisk byte-lik JSON som fixturen bildet ble rendret fra, og en ny render fra cellens ekte state med pikseldiff mot referansen. PDD_lister: 0 piksler avvik på tre flater.
- **lesson.shared-swiftpm-cache-lost-its-ownership-marker** (2026-10-08, minor): Første bygg i et nytt CellProtocol-arbeidstre stoppet etter 4 s: haven-swiftpm.sh exit 64, «existing cache lacks the required ownership marker: …/T/haven-swiftpm-bounded/caches/90c10549…».
    - forebygging: Byggeskript for en PDD setter HAVEN_SWIFTPM_CACHE_KEY=<pdd-slug> (egen cache) i stedet for å reparere den delte; koster ett kaldt bygg (6 min for CellProtocol). Test: skriptet skriver cache-key i rapporten.
- **lesson.xctest-stdout-export-interleaves-with-its-own-log** (2026-10-08, minor): En test printet 49 kB JSON til stdout mellom markører for at byggeskriptet skulle klippe den ut; fila ble ugyldig ved byte 49156 — XCTests egen «Test Case '…' passed»-linje lå midt inne i JSON-en.
    - forebygging: En test som skal levere data til et skript, skriver til en fil (NSTemporaryDirectory()) og printer bare stien; skriptet validerer JSON før det kopierer. Og: /usr/local/bin/python3 på Kjetils Mac er en x86-binær («Bad CPU type in executable») under launchd — bruk /usr/bin/python3 eller node i skript.
- **lesson.textfield-cannot-carry-instance-identity-in-a-mount** (2026-10-08, major): Inne i en ComponentSurface-montering kan Button si hvilken liste den gjelder (payload fra raden), men TextField sender bare en string til en fast targetKeypath — «Legg til …» i montering nr. 2 ville havnet i aktiv liste.
    - forebygging: Kjetil valgte A (2026-10-08): SkeletonComponentActionContext (struct + @TaskLocal) i CellBase; cellen leser mount.instanceID; CellScaffold bytter ScaffoldKit-typen til en typealias i integrasjonspakken. Regel for nye komponenter: alt som skal vite instansen går via Button-payload eller monteringskonteksten — aldri via aktiv-tilstand i cellen. Test: ListsCellTests.testMountedComponentContextTargetsTheMountedListNotTheActiveOne.
- **lesson.capability-based-layout-variant-replaces-client-checks** (2026-10-08, minor): Flytting av punkter trengte piler i appen og dra-og-slipp på web, uten to skjeletter eller klientnavn.
    - forebygging: layoutVariants: [{requiresCapability: [drag], hidden: true}] på pilene: web erklærer drag (porthole-webo.js), Binding erklærer pointer/hover/keyboard eller touch (PortholeView.swift) — pilene forsvinner av seg selv den dagen appen får drag-adapteren. Test: layoutVariant(in:) med begge kapabilitetssett (ListsConfigurationTests) + web-harness variants (render-report-wp5.json).
- **lesson.explore-requiredkeys-match-codable** (2026-10-12, major): Schema-gyldig konfigurasjon kunne mangle felt som Codable krever.
    - forebygging: Sammenlign requiredKeys med avvisning ved fjerning av hvert required felt; ta med nested visibility/privacy og recursive kind/all/any.
- **lesson.context-startup-independent-task-cycle** (2026-10-12, major): TaskLocal vernet samme kallkjede, men kildekontroll fant mulig motsatt gate-rekkefølge for to oppstarts-Tasks.
    - forebygging: Serialiser uavhengige røtter før lokale gates og bevar nested scope; test to samtidige røtter i en allerede syklisk fixture.
- **lesson.shared-cellresolver-fixture-unique-names** (2026-10-12, minor): Integrasjon kunne treffe en tidligere emitter selv om nytt registerkall ikke kastet.
    - forebygging: Bruk unike registreringsnavn i sharedInstance-fixtures, og mål actual loadCell/flow mot den nye cellen.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://grounding.local-model-assisted-decomposition [active] — Local model assisted decomposition
- purpose://candidate.game-workshop.engine [candidate] — Spillmotor og sandkasse

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| T-LISTE | dimy-liste | XCTest mot katalogen: tilbudt/ikke tilbudt; kall mot ikke tilbudt modell gir avslag og spion = 0 | TESTRESULT.md#liste | venter |
| T-MIKRO | mikrobetaling | XCTest: fixture for Mistral og OpenAI gir riktig pris, avregning og kvittering; uten kvote `payment_required` og spion = 0; ukjent utfall går til avstemming | TESTRESULT.md#mikro | venter |
| T-KALLIMACHOS-KILDE | kallimachos-modell | XCTest: lokal, DiMy-hostet, egen nøkkel og ingen kilde; persona og kildeinfo i svaret; DiMy-hostet går gjennom målesporet | TESTRESULT.md#kallimachos | venter |
| T-ROT | root | To studentkontoer og én vanlig konto på staging (web + Binding); spør Kallimachos med «kapabel» | ACCEPT.md#rot | venter |
| T-HVEM | hvem | XCTest: gyldig rolle-VC gir tilgang til kvoten; fremmed, tilbaketrukket og utløpt gir `not_eligible`; utdatert status gir `role_status_unknown`; samme vilkårsfixturer i Py/Go (fra PR #46) | TESTRESULT.md#hvem | venter |
| T-MISTRAL | mistral | XCTest med injisert transport: riktig URL, header, body (`max_tokens`, ingen verktøy), parsing av `usage.prompt_tokens/completion_tokens`; omdirigering avvises; manglende usage gir avstemming, ikke gjetting | TESTRESULT.md#mistral | venter |
| T-MISTRAL-LIVE | mistral | Ett ekte kall på staging etter Kjetils ja; kvittering med `providerModel` og faktiske tokens | TESTRESULT.md#live | venter |
| T-DAG | dagsgrense | XCTest: fyll opp til grensen, neste avvises før transport kalles (spion = 0); to studenter påvirker ikke hverandre; døgnskifte i Europe/Oslo | TESTRESULT.md#dag | venter |
| T-TAK | tak | XCTest: kvote brukt opp gir `payment_required` uten leverandørkall | TESTRESULT.md#tak | venter |
| T-LOKAL | lokal-forst | XCTest: lokal oppe → lokal brukt, kvote urørt; lokal nede → Mistral; kvote tom → svar uten modell med beskjed | TESTRESULT.md#lokal | venter |
| T-BETALER | betaler-velger | XCTest med transportspion: konto uten valg eller kvote gir null kall på operatørens nøkkel; egen nøkkel rører ikke kvoten | TESTRESULT.md#betaler | venter |
| T-SYNLIG | synlig | Skjermbilde web + Binding mot godkjente bilder | ACCEPT.md#parity | venter |
| T-DRIFT | drift | XCTest: leverandørmodus uten bekreftelse avvises; Mistral-nøkkel godtas, OpenAI-nøkkel i Mistral-felt avvises; forbruk per student i ledger | TESTRESULT.md#drift | venter |
| T-SVARFORM | svarform | XCTest: to studenter i samme felles chat; hver trekker fra egen kvote; avslag har riktig kode og tall | TESTRESULT.md#svarform | venter |
| T-EN-PORT | en-port | grep etter direkte ruter til leverandører i studentverktøyene + test at Kallimachos går gjennom porten | TESTRESULT.md#en-port | venter |
| test.build / test.regression | pakker | `swift build --build-tests` og `ci/run-tests.sh` på Linux i CI og på Mac | TESTRESULT.md#build | venter |
| test.cell.auth-negative | pakker | Inngår i T-HVEM | TESTRESULT.md#auth | venter |
| test.gui.parity / load-time / reachability | pakker | Etter G1-GUI | ACCEPT.md | venter |

## 6. Åpne spørsmål til Kjetil

1. **Beløp.** Forslag: dagsgrense 3 kr per student, semestertak 100 kr per student, samlet døgnbudsjett 50 kr. Med fixtureprisen for Mistral small (≈ 6 kr per million svartokens) er 3 kr i døgnet flere hundre lange svar. Merk: Opus 5.5, som Kallimachos nå bruker som standard (CellScaffold #487), kostet ≈ 0,04 USD per svar i testen 19.11; 3 kr er da omtrent 7 svar per dag.

Avgjort:
- Sp. 2 (hvem er student): rolle-VC fra Informasjonssystemer i stedet for egen Agreement for kullet, avtalt med tråden for gruppeentiteten. Godkjenningen av PR #46 gjelder for selve VC-en.
- Sp. 3 (OpenAI-ruten): Kallimachos er en persona som brukeren kjører på den kilden hen velger og betaler for (20.11).
- Sp. 4 (ett målespor): forslaget (20.11).
- Sp. 5 (første modeller): ja (20.11).

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-11-15 | Opprettet | Losen |
| 4 | 2026-11-20 | Kjetils svar på sp. 3–5. `kallimachos-modell` blir «persona, ikke modell» med brukerens kildevalg; `openai-stengt` blir `betaler-velger`; `hvem` bruker rolle-VC fra Informasjonssystemer; katalogfeltene avtalt med kildevelger-PDD-en; ny avslagskode `role_status_unknown`. Bare sp. 1 (beløp) står åpent | Claude |
| 3 | 2026-11-15 | Kjetils retning 22:26Z: modeller i DiMys liste med mikrobetaling for tokenbruk. Ny rot, tre nye formål (dimy-liste, mikrobetaling, kallimachos-modell), regulatorisk klassifisering i §2, spørsmål 3–5 skrevet om | Claude |
| 2 | 2026-11-15 | Nytt formål `svarform` etter ønske fra tråden «La språkmodellen delta i felles chat» (PR #43): identitet per spørrer, egne avslagskoder, gjenstående i kroner og kall | Claude |
| 1 | 2026-11-15 | Brief-audit mot kode (to påstander motsagt: tjenesten er bare OpenAI, og dagsgrensen er samlet, ikke per student), 10 formål, 11 formålstester, 5 spørsmål | Claude |
