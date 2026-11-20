# Formålsspesifikasjon — språkmodell som deltaker i felles chat

Oppgavemappe: `PDD_modell-i-felles-chat_2026-11-15` · Opprettet 2026-11-15 · Iterasjon 2 (G1 og G1-GUI godkjent 2026-11-20)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

Kjetil, 14.11.2026 kl. 12.34 (prosjektchatten):

> Ha i bakhodet at dette skal være samarbeidsverktøy så funksjonalitet som chat er naturlig nok med

Kjetil, 15.11.2026 kl. ca. 02.12 Oslo, valg på beslutningskortet om modelltilgang: **«Lokal modell + Mistral-kvote»** (gratis lokal Qwen som standard, Mistral på operatørens nøkkel med dagsgrense per student, Kallimachos' OpenAI-rute stenges for studenter).

Denne PDD-en dekker arbeidspakke F i auditen (`/mnt/project-files/masterhaven26/sprakmodell-audit-2026-11-14.md`): **en språkmodell kan delta i en gruppesamtale mellom studenter**. Mistral-kvoten bygges i tråden «Gi studentene Mistral med dagsgrense», og den lokale modellen på staging i tråden «Få språkmodellen på staging tilbake». Begge er avhengigheter her (§2), ikke en del av denne PDD-en.

Brief-audit. Kildene er lest denne økten i CellScaffold `9612217` (main 15.11), CellProtocol `14fd9dc`, PyCellProtocol `251314c` og GoCellProtocol `9ea5cc9`.

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Studentene chatter i «Samtaler» (flere deltakere, invitasjonslenke) | retrieved | `CellScaffold/Sources/App/Cells/PersonalCopilot/PersonalCopilotConfigurationFactory.swift:1106` (`conversationsSkeleton`), `PersonalCopilotCloudStore.swift:17715` (`sendConversationMessage`) |
| Tilgang til en Samtaler-tråd avgjøres av en Agreement | **contradicted** | `PersonalCopilotCloudStore.swift:185` (`PersonalCopilotChatThread`): deltakerlisten er lagret tilstand i Co-Pilot-lageret, og `sendComposedMessage` (`:9913`) sjekker `thread.isParticipant`, ikke en Agreement. Samme funn som i PDD-en for dokumentdeling |
| Det finnes en chat der tilgang går via Agreement-vilkår, lik i Swift, Python og Go | retrieved | Swift: `CellProtocol/Sources/CellBase/Cells/Chat/ChatCell.swift:1918` (`ChatAdmissionCondition`: `invitationAccepted`, `member`, som `LookupCondition` på `target.audience.admission.*`). Python: `PyCellProtocol/src/cellprotocol/cells/chat.py:93`. Go: `GoCellProtocol/chat.go:13–43` |
| CellScaffold bruker allerede `ChatCell` som lager bak en flate | retrieved | `PersonalCopilotCloudStore.swift:2707` (`matchmakingChatBackend`), Arendalsuka-deltakerchatten |
| `ChatCell` lagrer sendte meldinger i klartekst, så en deltaker på serveren kan lese dem | retrieved | `ChatCell.swift:398` (`encryptedPersistenceMode = .draftCacheOnly`, «Sendte meldinger lagres som vanlig plaintext historikk») |
| Det finnes en celle der modeller skriver i en tråd | retrieved | `CellScaffold/Sources/App/Cells/AI/AIAssistantThreadCell.swift`: én tråd, «deltakere» telles fra meldingsforfattere (`:678`), modellen kalles via `cell:///AIGateway` med den som spør som requester (`:707–708`), konteksten er de siste 12 meldingene (`:2070`). Den har ingen invitasjon og ingen deltakerliste |
| Butler kan i dag svare med modell i en gruppesamtale | **contradicted** | Auditen 14.11: «Butler kan ikke delta med modell i felles chat». Ingen kodevei i `sendComposedMessage` kaller en modell |
| Mistral-rute finnes i koden | retrieved (ikke aktivert) | `CellScaffold/Sources/App/Services/ButlerProviderCatalog.swift:7–26`: `managed-mistral-small4-eu`, `https://api.eu.mistral.ai`, `mistral-small-2603` |
| Mistral med dagsgrense per student virker | unavailable | Bygges i tråden «Gi studentene Mistral med dagsgrense» (startet 15.11) |
| Lokal Qwen svarer på staging | **contradicted** (14.11) | Auditen. Årsak lest i kode: egress-policyen låser Qwen til `http://127.0.0.1:8083`, som i containeren er containerens egen loopback (`KallimachosAdvisorCell.swift:82`, minnenotat 14.11). Tråd A |
| Python og Go har en AIGateway | **contradicted** | Ingen gateway- eller modellkode i `PyCellProtocol/src` eller `GoCellProtocol/*.go` (søk på `gateway`, `llm`, `invoke_ai`) |
| Samtaler vises i Binding (Swift) | retrieved | Skjelettet er bare `List`, `Text`, `TextArea`, `Button`, `HStack/VStack` med `layoutVariants` og `visibility` med `scope: item` (`PersonalCopilotConfigurationFactory.swift:1106–1260`), som CellApple tegner. Ikke målt i Binding denne økten |

## 1. Formålstre

Rot: studenter i samme samtale kan spørre en språkmodell, og hele gruppen ser spørsmålet, svaret, hvem som spurte, hvilken modell som svarte og hva modellen fikk lese.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.modell-i-felles-chat.root | Språkmodell som deltaker i felles chat | purpose://digital-work | To studenter i samme samtale på staging: modellen legges til med begges ja, én spør, begge ser svaret merket med modell og spørrer, i web og i Binding | test.modellchat.e2e-to-studenter | candidate |
| purpose://candidate.modell-i-felles-chat.chat-on-agreement | Samtalen er en Agreement-styrt chat | root | En Samtaler-tråd er en `ChatCell`. Tilgang for mennesker og modell avgjøres av vilkårene i chattens Agreement, likt i Swift, Python og Go. Eksisterende tråder flyttes over uten tap | test.modellchat.samtale-er-chatcell, test.modellchat.migrering | candidate (avhengighet, se §6 spm. 1) |
| purpose://candidate.modell-i-felles-chat.model-is-participant | Modellen er en navngitt deltaker | root | Modellen har en egen identitet i chatten («Språkmodell»), står i deltakerlisten med merket «modell», og hver modellmelding er merket som modellmelding i meldingskontrakten (`authorKind: model`) | test.modellchat.deltaker-merket | candidate |
| purpose://candidate.modell-i-felles-chat.group-consent | Gruppen velger å ha modellen med | root | En deltaker foreslår modellen. Den kommer inn først når alle som er med har sagt ja. Nye deltakere ser at modellen er med før de godtar invitasjonen. Hvem som helst kan fjerne modellen, og da mister den tilgang straks | test.modellchat.alle-maa-si-ja, test.modellchat.fjern | candidate |
| purpose://candidate.modell-i-felles-chat.admission-condition | Modellens adgang er et Agreement-vilkår | group-consent | Nytt vilkår `modelConsent` (`target.audience.admission.modelConsent`) holder bare når alle nåværende menneskelige deltakere har samtykket og ingen har trukket det. Modellens kontrakt sjekkes ved hvert kall. Identisk i Swift, Python og Go, bevist med delte fixtures | test.modellchat.vilkaar-fixtures, test.cell.auth-negative | candidate |
| purpose://candidate.modell-i-felles-chat.addressed-only | Modellen svarer bare når noen spør den | root | Modellen leser og svarer bare når en deltaker trykker «Spør modellen» eller skriver `@modell`. Ingen bakgrunnslesing, ingen automatiske svar | test.modellchat.bare-naar-spurt | candidate |
| purpose://candidate.modell-i-felles-chat.bounded-context | Modellen får lese lite, og gruppen ser hva | addressed-only | Modellen får spørsmålet og høyst de 20 siste meldingene, og aldri meldinger fra før den ble lagt til. Svaret viser «leste N meldinger» | test.modellchat.kontekstgrense | candidate |
| purpose://candidate.modell-i-felles-chat.asker-route | Den som spør velger og betaler | root | Kallet går med den spørrendes identitet og modellvalg: lokal Qwen (gratis, standard) eller Mistral (trekker fra den spørrendes dagskvote). Aldri en annen deltakers kvote eller nøkkel. Svaret viser modell og hvem som spurte | test.modellchat.rute-er-spørrerens | candidate |
| purpose://candidate.modell-i-felles-chat.external-opt-in | Ekstern modell krever gruppens ja | asker-route | Lokal Qwen kjører på HAVENs egen server. Mistral er en ekstern leverandør (EU). Mistral kan bare velges i en samtale der alle har sagt ja til ekstern modell, og flaten sier hvor teksten går | test.modellchat.ekstern-krever-ja | candidate |
| purpose://candidate.modell-i-felles-chat.honest-failure | Feil sies rett ut, til den som spurte | root | Lokal modell nede, kvoten brukt opp, eller ingen rute: ingen modellmelding postes i chatten. Den som spurte får en melding som sier hva som skjedde og hva som kan gjøres («Prøv Mistral, 6 av 20 igjen i dag»). Spørsmålet står ikke ubesvart uten forklaring | test.modellchat.feil-til-spørrer | candidate |
| purpose://candidate.modell-i-felles-chat.untrusted-output | Modellsvar er data, ikke instruksjoner | root | Svaret er ren tekst med lengdegrense (4 000 tegn), kan ikke invitere, fjerne, endre vilkår eller kalle andre celler, og vises med samme moderering som andre meldinger | test.modellchat.svar-er-ren-tekst | candidate |
| purpose://candidate.modell-i-felles-chat.swift-native | Det samme virker i Binding | root | Forslag, samtykke, «Spør modellen», modellsvar og feilmelding er vanlige skeleton-elementer i Samtaler, og virker i Binding (Swift) som på web | test.gui.parity (Binding og web) | candidate |
| purpose://candidate.modell-i-felles-chat.cross-language | Samme kontrakt i Python og Go | root | `modelConsent`-vilkåret, deltakermerket og meldingskontrakten (`authorKind`, `askedBy`, `model`, `contextCount`) er like i Swift, Python og Go. Python og Go har ingen modell: der svarer modellen gjennom en innplugget leverandør, testet med en fast falsk leverandør | test.modellchat.vilkaar-fixtures, test.modellchat.interop | candidate (se §6 spm. 4) |
| purpose://quality.build-and-regression | Alt bygger, eksisterende tester passerer | pkg.std.everything-works | Som i pakken | test.build, test.regression | fra pakke |
| purpose://gui.expectation-agreed-before-build | Bildene er godkjent før koding | pkg.std.gui-surface | Bildene i `images/` er godkjent av Kjetil | test.gui.reference-image-exists | fra pakke |
| purpose://gui.ways-in-are-reachable | Alle handlinger kan nås | pkg.std.gui-surface | `chatHub.conversation.model.propose`, `.consent`, `.decline`, `.remove`, `.ask`, `.route` finnes i Samtalers `reachableActionKeypaths` | test.skeleton.purpose-actions-reachable | fra pakke |

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en modell som leser med og blander seg inn av seg selv. Den svarer bare når noen spør.
- Ikke Butler Chat (den personlige assistenten) og ikke «HAVEN Teaching Group Chat» (`AIAssistantThreadCell`), der modeller snakker med hverandre. Her er modellen én deltaker i en samtale mellom mennesker.
- Ikke modellbruk i dokumenter (tråd D) eller argumentanalyse (tråd C).
- Ikke selve Mistral-kvoten eller driften av lokal modell. Denne PDD-en bruker rutene de to trådene leverer, gjennom samme rutevalg.
- Ikke ende-til-ende-kryptert chat. `ChatCell` lagrer sendte meldinger i klartekst i dag. Blir chatten kryptert senere, må modellen være mottaker som alle andre, og det er en egen sak.

Avhengigheter. Hver må virke før den egentlige testen kjøres (`lesson.corr-approval-surfaces-timed-out`). Steget før modellsvaret er målt der det kan måles (HD-0077-regelen):

| Avhengighet | Verifier | Tilstand 15.11 |
|---|---|---|
| Lokal Qwen svarer fra staging-appen | Ett kall fra app-containeren til Qwen-ruten gir svar, målt på staging | **ikke målt, kjent nede** (tråd A, venter på Deploy) |
| Mistral med dagsgrense per student | En ny studentkonto på staging får svar fra Mistral, og kall nummer grense+1 avvises med kvotekode | **ikke målt** (tråd «Gi studentene Mistral med dagsgrense», CellProtocolDocuments PR #42, G1 venter). Kontrakt foreslått der: kallet går med den spørrendes identitet; hvert svar og avslag har `quota` (`remainingTodayMinorUnits`, `dailyLimitMinorUnits`, `remainingCallsToday`, `dailyCallLimit`, `resetsAt`); avslagskoder `student_quota_exhausted_today`, `student_quota_exhausted_term`, `service_budget_exhausted`, `not_eligible`. Grensen er i kroner, så «13 av 20 igjen» er en øvre grense |
| Samtaler med to studenter virker på staging | To nye kontoer: invitasjonslenke, godta, meldinger begge veier | målt 12.11 i tråden «Bevis at felles chat med Sara og Petter virker» (staging `4e629fb3`); ikke målt på dagens staging |
| Samtaler-tråder er `ChatCell` med Agreement-adgang | `test.modellchat.samtale-er-chatcell` | **mangler** (§6 spm. 1) |
| Felles adgangsdel i CellBase (fra dokumentdeling) | Kjetil valgte 15.11 en delt adgangsdel i CellBase for dokumenter (`InvitationAdmission`). Gjenbrukes her hvis den lander først | under arbeid i tråden «La studenter dele dokumenter med hverandre», G1 venter |
| Binding tegner Samtaler | Samtaler åpnet i Binding på Mac, skjermbilde | ikke målt denne økten |

Rekkevidde: så lenge lokal Qwen er nede og Mistral-kvoten ikke er levert, får **0 av 2** modellruter svar på staging. Da kan alt annet i denne PDD-en bygges og testes med en fast testleverandør, men målet i roten er ikke nådd.

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse |
|---|---|---|---|
| Samtaler med forslag om modell og samtykke (laptop og iPhone) | bilde | `images/modellchat-forslag-{laptop,iphone}-v1.png` | G1-GUI |
| Samtaler med modellen som deltaker og to modellsvar (laptop og iPhone) | bilde | `images/modellchat-fylt-{laptop,iphone}-v1.png` | G1-GUI |
| Samtaler når modellen ikke kan svare (laptop og iPhone) | bilde | `images/modellchat-feil-{laptop,iphone}-v1.png` | G1-GUI |
| Skeleton-JSON bildene er rendret fra | fil | `skeleton/samtaler-med-modell.v1.json`, `skeleton/tilstander.v1.json`, `skeleton/render.js` | G1-GUI |
| Samtaler på staging med modellsvar, to studenter | kjørende flate | staging, web | test.modellchat.e2e-to-studenter |
| Samme i Binding (Swift) | kjørende flate, skjermbilde | Binding på Mac | test.gui.parity |
| `modelConsent`-vilkåret i tre språk | testutdata | TESTRESULT.md#fixtures | test.modellchat.vilkaar-fixtures |
| Alle avledede tester | testutdata | TESTRESULT.md | §5 |

Hva bildene ikke viser: bildene er rendret med den ekte web-rendereren (`Public/js/skeleton-runtime.js` og `porthole-webo.css`) fra skeleton-JSON. De er ikke tatt fra Binding. Ingen nye skeleton-elementtyper trengs: alt er `Text`, `Button`, `List`, `TextArea`, `VStack/HStack` med `visibility` (rot og rad) og `backgroundKeypath`, som Samtaler bruker i dag.

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

Lærdommene som styrer denne PDD-en mest, og hvor de er brukt:

- `lesson.purpose-never-grants-rights` og `lesson.location-is-not-ownership`: modellen får ingen tilgang fordi den «hjelper». Adgang er vilkåret `modelConsent` i chattens Agreement, og negative tester dekker handlinger, ikke bare felter (§1 admission-condition, §5 test.cell.auth-negative).
- `lesson.corr-approval-surfaces-timed-out` og HD-0077-regelen: lokal Qwen og Mistral-kvoten står som egne avhengigheter med målt tilstand i §2, og rekkevidden er oppgitt som målt tall (0 av 2 ruter i dag).
- `lesson.empty-list-must-not-look-like-calm`: en modell som ikke svarer skal ikke se ut som stillhet (§1 honest-failure).
- `lesson.unresolvable-condition-is-invisible` og `lesson.findability-is-not-usability`: nye knapper ligger i rader eller bak rot-betingelser som kan bli sanne, og sjekkes med `reachableActionKeypaths` (§5).
- `lesson.text-ux-is-not-design`: bildene i `images/` er rendret fra skeleton-JSON med den ekte rendereren.
- `lesson.valuetype-equality-false-for-objects`: tester sammenligner sortert-nøkkel-JSON (§5 migrering).

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
- **lesson.stand-in-shared-the-callers-assumption** (2026-10-05, major): Første tørrkjøring på Macen stoppet fordi korrespondanseklienten svarte «No enrolled correspondence profile exists», mens 42 tester og 126 selvkontroller var grønne i skyen.
    - forebygging: Før kode skrives mot et eksternt program, måles kontrakten der programmet kjører: argumentene, avslutningskodene og den ordrette teksten når det nekter. Stedfortrederen i testene skal nekte på samme måte. Test: én test kjører stedfortrederen med inndataene det ekte programmet nektet, og krever samme kode og tekst; og når det gamle kallet settes tilbake i en kopi, blir testene røde.
- **lesson.file-copied-to-the-mac-was-the-previous-version** (2026-10-05, major): En commit gikk ut med testen, men uten endringen den prøvde: filkopien fra skyøkten til Macen meldte «written», og fila på Macen var forrige utgave. To skript mistet dessuten kjørbar-biten på veien.
    - forebygging: Hver utgave som skal til Macen, legges under et nytt filnavn i utdatamappen. Sjekksummen på Macen sammenlignes med den i skyen i et eget steg, og neste steg (commit eller køjobb) startes ikke i samme kommando. Test: commit-jobben viser «git diff --cached --stat --summary» før commit, og lista over filer og moduser sammenlignes med det som skulle med.
- **lesson.pr-opened-without-reading-the-base-branch-ci** (2026-10-05, minor): PR #30 ble opprettet uten at CI-tilstanden på main var lest: løpet sto til tidsgrensen på 25 minutter av en grunn som hadde stått på main i seks dager, og den første lesningen av loggen, at det stoppet før PR-ens tester hadde startet, ble felt av den uavhengige kontrollen.
    - forebygging: Før en PR opprettes, listes løpene for basisgrenen; har hodet ikke noe grønt løp med samme testskript, rettes det først, eller rettelsen tas med. Før en årsak skrives ned for et rødt løp, leses avsnittet om CI i skillen, og siste linje i en logg kalles ikke stedet det stoppet. Test: skriptet som oppretter en PR, viser siste løp på basisgrenen og stopper når det er rødt.
- **lesson.the-scripts-own-python-was-newer-in-the-tests-than-on-the-mac** (2026-10-06, minor): Testene av bytteskriptet kjørte skriptets egne Python-blokker med 3.11, mens Macen har 3.9.6, som avviser datoformer 3.11 tar.
    - forebygging: Testene bytter stien til tolken, i kopien av skriptet de kjører, til utgaven målmaskinen har, og én test krever at ingen annen tolk står igjen i kopien. Datoer tolkes uten funksjoner som oppfører seg ulikt mellom utgavene.
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
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance


## 5. Avledede tester (samlet)

| Test | Type | Hvordan | Bevis i |
|---|---|---|---|
| test.modellchat.e2e-to-studenter | measurement | To nye kontoer på staging: start samtale, legg til modell (begge ja), A spør, B ser svaret med «Spurt av A · Qwen lokalt · leste N meldinger». Playwright, samme skript som 12.11 | TESTRESULT.md#e2e |
| test.modellchat.samtale-er-chatcell | command | Swift-test: en ny Samtaler-tråd er en `ChatCell`; en identitet uten oppfylt vilkår får `denied` på `messages` og `sendMessage` | TESTRESULT.md#chatcell |
| test.modellchat.migrering | command | Lagrede tråder fra dagens format (fixture fra `Samtaler-pre416.json`) flyttes til `ChatCell` med samme deltakere og meldinger, sortert-nøkkel-JSON sammenlignet | TESTRESULT.md#migrering |
| test.modellchat.deltaker-merket | command | Etter samtykke står modellen i `participants` med `kind: model`; hver modellmelding har `authorKind: model`, `askedBy`, `model`, `contextCount` | TESTRESULT.md#deltaker |
| test.modellchat.alle-maa-si-ja | command | Tre deltakere, to ja: `modelConsent` er usann, modellens `get messages` gir `denied`. Tredje ja: sann. Ny deltaker etter samtykke: vilkåret er fortsatt sant, og invitasjonen viser at modellen er med | TESTRESULT.md#samtykke |
| test.modellchat.fjern | command | En deltaker fjerner modellen eller trekker sitt ja: neste modellkall avvises, uten restart | TESTRESULT.md#fjern |
| test.modellchat.vilkaar-fixtures | command | Swift genererer fixtures for `modelConsent` (sant, usant, trukket, ny deltaker). Python og Go gir samme svar på samme fixtures | TESTRESULT.md#fixtures |
| test.cell.auth-negative | command | Feil requester, en identitet som bare later som den er modellen, en ikke-deltaker som trykker «Spør modellen», og `purpose://prompt.unknown`: alle avvist | TESTRESULT.md#auth |
| test.modellchat.bare-naar-spurt | command | 50 meldinger uten `@modell` eller knappetrykk: null kall til gatewayen (tellende testleverandør) | TESTRESULT.md#bare-spurt |
| test.modellchat.kontekstgrense | command | 40 meldinger, modellen lagt til etter melding 25: forespørselen til leverandøren har høyst 20 meldinger og ingen fra før 26. `contextCount` stemmer med det som ble sendt | TESTRESULT.md#kontekst |
| test.modellchat.rute-er-spørrerens | command | A og B med ulike kvoter: A spør med Mistral, bare As kvote går ned. Requester mot gatewayen er A | TESTRESULT.md#rute |
| test.modellchat.ekstern-krever-ja | command | Uten gruppens ja til ekstern modell: Mistral-valget gir `external_not_allowed` og ingen kall. Med ja: kall går | TESTRESULT.md#ekstern |
| test.modellchat.feil-til-spørrer | command | Leverandøren nede, kvote brukt opp, ingen rute: ingen modellmelding i `messages`; den som spurte får egen tilstand med kode og tekst; de andre ser ingenting | TESTRESULT.md#feil |
| test.modellchat.svar-er-ren-tekst | command | Svar med HTML, skript, keypath-lignende tekst og 10 000 tegn: lagres som ren tekst, kortes til 4 000, ingen handling utløses | TESTRESULT.md#ren-tekst |
| test.modellchat.interop | command | PyCellProtocol `interop/matrix/run_matrix.py` utvidet: Swift-, Python- og Go-chat med modelldeltaker (fast falsk leverandør) gir samme meldingskontrakt | TESTRESULT.md#interop |
| test.gui.reference-image-exists | artifact | Bildene i §3 finnes og er godkjent | images/ |
| test.gui.parity | inspection | Skjermbilde fra staging (web) og Binding side om side med godkjent bilde, og knappene treffer keypathene | ACCEPT.md#parity |
| test.skeleton.purpose-actions-reachable | inspection | Handlingene i §1 finnes i `reachableActionKeypaths` for Samtaler | ACCEPT.md#ways-in |
| test.build / test.regression | command | Full `swift build --build-tests` og testkjøring for CellProtocol og CellScaffold, `pytest` og `go test` | TESTRESULT.md#build, #regression |

## 6. Åpne spørsmål til Kjetil

1. **Hvor bor samtalen?** I dag er Samtaler-tråder lagret tilstand i Co-Pilot-lageret, ikke en Agreement. Din regel sier at tilgang til en chat bare avgjøres av Agreement-vilkår. Valg: (a) Samtaler flyttes over på `ChatCell` (Agreement, finnes i Swift, Python og Go), og modellen kommer inn som deltaker der. Eksisterende tråder flyttes over. (b) Modellen legges inn i dagens Samtaler-lager uten Agreement, raskere men bryter regelen. **Anbefaling: (a).** Det er mer arbeid, men det er det eneste som holder regelen, og det samme trengs for dokumentdeling. **Besluttet 2026-11-15 11.31 Oslo: (a)** (Kjetil, beslutningskort «Ja, flytt Samtaler til ChatCell»).
2. **Hvem må si ja før modellen kommer inn?** (a) Alle som er med i samtalen. (b) Bare den som eier samtalen. **Anbefaling: (a),** fordi det er alles meldinger modellen får lese. **Besluttet 2026-11-20: (a).**
3. **Ekstern modell (Mistral) i en gruppesamtale:** (a) krever et eget ja fra alle, utover ja til lokal modell, (b) samme ja dekker begge. **Anbefaling: (a).** Lokal Qwen holder teksten på HAVENs server, Mistral sender den ut av huset (EU). **Besluttet 2026-11-20: (a).**
4. **Python og Go har ingen AIGateway.** (a) Python og Go får samme vilkår og meldingskontrakt, og modellen kobles inn som en innplugget leverandør (testet med falsk leverandør), (b) Python og Go får også et ekte modellkall. **Anbefaling: (a) nå,** (b) som egen sak. **Besluttet 2026-11-20: (a).**

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg |
|---|---|---|
| 2 | 2026-11-20 | Kjetil 23.43 Oslo: «2. a 3 a a nå G1 G1-GUI Godkjent». §6 spm. 2–4 besluttet (a). G1 og G1-GUI godkjent |
| 1c | 2026-11-15 | §6 spm. 1 besluttet av Kjetil: Samtaler flyttes til ChatCell (a). Spm. 2–4 og G1 venter |
| 1b | 2026-11-15 | §2: Mistral-kvotens svar- og avslagskontrakt fra PR #42 lagt inn. Feilmeldingen i chatten bruker avslagskodene derfra |
| 1 | 2026-11-15 | Første utkast: formålstre, avhengigheter med tilstand, forventningskontrakt, tester, fire åpne spørsmål. Seks bilder rendret fra skeleton-JSON |
