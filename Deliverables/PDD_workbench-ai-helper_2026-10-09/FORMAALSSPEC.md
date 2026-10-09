# Formålsspesifikasjon — workbench ai helper

Oppgavemappe: `PDD_workbench-ai-helper_2026-10-09` · Opprettet 2026-10-09 · Iterasjon 1 · G1 godkjent 2026-10-09

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

Formålsside med detaljer og godkjenning: https://claude.ai/artifact/9uUQtFQmi5wpGbgabyTJj1 (kilde `formaalsside/tree.json`, bygget med `haven-purpose-tree-review/references/build_page.py`).

## 0. Intensjon (ordrett) og brief-audit

> Merge når den er klar. Jeg vil også ha med en AI-hjelper komponent i Developer Workbench slik som vi snakket om med Sverres spill flate. Vi må kunne redigere instruksjoner og prompts og ha fler sett. En for å teste gui i andre flater eller lage nye flater (F.eks kan sindre si "lag tiles av bildene og sett underteksten til 9 pkt farge #CCCCCC" eller sett underteksten til bilde av Slumbering Stones til "Lorem ipsum..."). En for hjelp med flaten man jobber i ("flytt alt fra inbox over til triage" eller beskriv hva slags spill man skal lage, eller ). Eller hjelp til å finne og oppdatere dokumentasjon eller si "evaluer disse ideene, lag tasks og start dem". VI har snakket tidligere om å alltid ha med en mulighet for å nå butleren så man alltid kan nå alt annet. Det må inn i formål om det ikke er der allerede. (nesten det samme som formålet med å ikke tillate at man bygger flater som gjør at man mister kontakten med egen entitet.)
>
> — Kjetil, 2026-10-09 13:05Z, tråden «Formålstre i Developer Workbench»

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Mønsteret fra Sverres spillflate finnes og er godkjent | retrieved | `PDD_spillverksted_2026-10-09` gren B (`candidate.workbench-assistant.*`), G1 godkjent 2026-10-09 08:56Z |
| Instruksjoner og prompts kan redigeres i dag | contradicted | Butler-hjelperne er hardkodet (`PersonalCopilotCloudStore.swift:1081-1194`, `helperPromptRoute` :3920). AIGateway har ett midlertidig `systemPrompt`-utkast (`AIGatewayCell.swift:514`). `PersonalAssistantProfileCell` er én profil per eier uten instruksjonstekst. `assistant-config.json` leses ikke av noen kode. |
| «Flytt alt fra inbox til triage» kan gjøres | delvis | `WorkItem setStatus` per element (`WorkItemCell.swift:929`), overgangen new→triage er lov (:2877). Ingen handling for mange. |
| Tiles og bildetekst på Sindres verk kan endres | contradicted | Publication har `setSiteTheme`/`setLayoutPreset` (:320, :328), men ingen tekst på publisert verk. ArtistSales og MediaCollection har bare utkast-felt (`ArtistSalesChannelCell.swift:369`, `MediaCollectionSupport.swift:28`). |
| Nye flater kan lages uten rekompilering | retrieved | Porthole-editoren `editor.working.setSkeleton` / `editor.apply` (`PortholeWebSessionSupport.swift:5929`, :6106). Bundet til en sesjon, ikke en celle-handling. |
| Dokumentasjon kan finnes og oppdateres | delvis | `docs-rag` i Butler søker bare i synlige dokumenter (`PersonalCopilotCloudStore.swift:2933`). Ingen skriving. `haven-docs` MCP finnes for utviklere, ikke i Scaffold. |
| Agentjobber kan startes fra Workbench | contradicted | `AgentRunCell` er projeksjon uten kjørekontroll (:12-45). Eneste vei: agent-review i Butler (`PersonalCopilotCloudStore.swift:7711`, :7756) og HavenAgentD. |
| Forslag bekreftes før utførelse | retrieved | `GroundedActionPlan.requiresUserConfirmation` (`ExecutablePurposeGrounding.swift:59`), `verify()` :493, `assistant.acceptSuggestion` (`PersonalCopilotCells.swift:1512`). |
| Butler kan alltid nås | delvis | Formålet `purpose://skeleton.owner-entity-access` (Book 23, draft) dekker vei til egen entitet / Co-Pilot. Eneste faktiske vei er Butler-knappen i Porthole-verktøylinjen (`porthole-webo.js:5159`). Developer Workbench har ingen egen. |

## 1. Formålstre

Anker: `purpose://candidate.workbench-assistant.root` (Hjelperen er Developer Workbench sin bruk av arbeidsbenk-assistent-mønsteret. Løkken (forstå, avklar, foreslå, vis, bestem, utfør, lær) og regelen om at modellen bare foreslår, er allerede godkjent der.)

| Kode og purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status · fase |
|---|---|---|---|---|---|
| R `purpose://candidate.workbench-ai-helper.root` | Developer Workbench har en AI-hjelper som gjør jobben med deg | — | Fra Developer Workbench kan eieren be hjelperen om en endring i et vanlig språk, se forslaget, godta det med ett klikk og se resultatet, i fire ulike typer oppgaver. Gjenbruker `purpose://candidate.workbench-assistant.root`. | T-R: Playwright-kjøring av de fire eksemplene mot staging | candidate · Fase 1 |
| A `purpose://candidate.workbench-ai-helper.instructions` | Du styrer hva hjelperen gjør og hvordan den svarer | R | Eieren har flere navngitte sett med instruksjoner og prompts, kan redigere dem i flaten, og kan se og angre endringer. | T-A | candidate · Fase 1 |
| A1 `purpose://candidate.workbench-ai-helper.instructions.editable` | Instruksjoner og prompts kan redigeres i flaten | A | Eieren åpner et sett, endrer instruksjonsteksten og lagrer. Neste svar fra det settet følger den nye teksten. | T-A1: celletest + Playwright | candidate · Fase 1 |
| A2 `purpose://candidate.workbench-ai-helper.instructions.multiple-sets` | Flere sett, og du velger hvilket du snakker med | A | Eieren velger mellom settene «Flater og GUI», «Denne flaten», «Dokumentasjon» og «Idéer til oppgaver», og kan lage nye. Gjenbruker `purpose://candidate.workbench-assistant.reusable-profile`. | T-A2 | candidate · Fase 1 |
| A3 `purpose://candidate.workbench-ai-helper.instructions.versioned` | Endringer i et sett kan sammenlignes og angres | A | Hvert lagret sett får en versjon. Eieren ser forskjellen mot forrige versjon og kan gå tilbake. | T-A3 | candidate · Fase 1 |
| A4 `purpose://candidate.workbench-ai-helper.instructions.limits-per-set` | Teksten i et sett gir aldri mer tilgang | A | Hvert sett har en fast liste over tillatte handlinger og et eskaleringstak. Instruksjonsteksten kan ikke utvide dem, og målcellen sjekker tilgang på hver handling. Gjenbruker `purpose://candidate.workbench-assistant.propose-human-decides`. | T-A4: celletest med fiendtlig instruks | candidate · Fase 1 |
| B `purpose://candidate.workbench-ai-helper.gui` | Lage og endre flater med ord | R | Eieren beskriver en endring eller en ny flate, ser den i forhåndsvisning og godtar den. Flaten lagres som ny versjon. Gjenbruker `purpose://candidate.workbench-assistant.preview-before-change`. | T-B | candidate · Fase 1 |
| B1 `purpose://candidate.workbench-ai-helper.gui.change-existing` | Endre en flate som finnes | B | «Lag tiles av bildene og sett underteksten til 9 pkt farge #CCCCCC» og «sett underteksten til Slumbering Stones til …» gir et forslag, en forhåndsvisning og en lagret endring. | T-B1: Playwright mot /pub/sindre-hustveit/verk i staging | candidate · Fase 2 |
| B2 `purpose://candidate.workbench-ai-helper.gui.create-new` | Lage en ny flate fra en beskrivelse | B | En beskrivelse gir et skjelett-utkast som vises i Porthole-editoren og kan lagres som ny konfigurasjon. | T-B2 | candidate · Fase 1 |
| B3 `purpose://candidate.workbench-ai-helper.gui.test-other-surface` | Teste GUI i andre flater | B | Eieren ber hjelperen sjekke en flate. Hjelperen åpner den, går gjennom det som ble bedt om, og rapporterer hva som virket og ikke, med bilder. Gjenbruker `purpose://gui.quality.functional-accessible`. | T-B3 | candidate · Fase 2 |
| B4 `purpose://candidate.workbench-ai-helper.gui.say-what-is-impossible` | Sier fra når flaten ikke kan det du ber om | B | Når skjelettformatet eller cellen ikke støtter ønsket, sier hjelperen det og hva som mangler, i stedet for å lage noe som ser riktig ut og ikke virker. | T-B4 | candidate · Fase 1 |
| C `purpose://candidate.workbench-ai-helper.surface` | Hjelp i flaten du står i | R | Hjelperen kjenner flaten eieren står i og kan gjøre flatens egne handlinger for henne, etter et klikk. Gjenbruker `purpose://candidate.workbench-assistant.understand-intent`. | T-C | candidate · Fase 1 |
| C1 `purpose://candidate.workbench-ai-helper.surface.act-on-many` | Gjør samme handling på mange elementer | C | «Flytt alt fra inbox til triage» viser hvilke elementer som flyttes, utføres etter ett klikk, og kan angres. | T-C1: celletest mot WorkItem | candidate · Fase 1 |
| C2 `purpose://candidate.workbench-ai-helper.surface.knows-context` | Vet hvilken flate og hvilket utvalg du har | C | Hjelperen får flatens handlingskontrakt og det som er valgt, og viser hva den bruker. Ingenting sendes i det skjulte. | T-C2 | candidate · Fase 1 |
| C3 `purpose://candidate.workbench-ai-helper.surface.describe-what-to-make` | Beskriv hva du vil lage, så spør hjelperen bare om det som mangler | C | I en flate som spillverkstedet beskriver brukeren et spill. Hjelperen stiller bare spørsmål som endrer resultatet. Gjenbruker `purpose://candidate.workbench-assistant.understand-intent`. | T-C3 | candidate · Fase 2 |
| D `purpose://candidate.workbench-ai-helper.docs` | Finne og oppdatere dokumentasjon | R | Hjelperen finner riktig dokument og foreslår oppdateringer som eieren godtar. | T-D | candidate · Fase 2 |
| D1 `purpose://candidate.workbench-ai-helper.docs.find` | Finner svaret i dokumentasjonen og viser hvor | D | Et spørsmål gir svar med lenke til Book-kapittel eller dokument, fra utvikler-RAG-en. Er kilden nede, sier hjelperen det. | T-D1 | candidate · Fase 2 |
| D2 `purpose://candidate.workbench-ai-helper.docs.propose-update` | Foreslår endringer i dokumentasjonen som en PR | D | Hjelperen viser endringen som diff. Godtar eieren, blir den en gren og en PR, aldri en direkte endring på main. | T-D2 | candidate · Fase 3 |
| E `purpose://candidate.workbench-ai-helper.ideas` | Fra idéer til oppgaver som kjører | R | «Evaluer disse idéene, lag tasks og start dem» gir en vurdering, oppgaver i Workbench og agentjobber som kjører, med godkjenning før hver del. | T-E | candidate · Fase 2 |
| E1 `purpose://candidate.workbench-ai-helper.ideas.evaluate` | Vurderer idéene mot formålene | E | Hver idé får en kort vurdering: hvilket formål den tjener, hva som mangler, og en anbefaling. Gjenbruker `purpose://analysis.decision-support`. | T-E1 | candidate · Fase 2 |
| E2 `purpose://candidate.workbench-ai-helper.ideas.create-tasks` | Lager oppgaver i Workbench | E | Godtatte idéer blir oppgaver med lenke til idéen og formålet. | T-E2 | candidate · Fase 2 |
| E3 `purpose://candidate.workbench-ai-helper.ideas.start-work` | Starter arbeidet hos agentene | E | Eieren godkjenner og arbeidet startes som jobb hos HavenAgentD. Workbench viser status, AgentD eier kjøringen. | T-E3 | candidate · Fase 3 |
| F `purpose://candidate.workbench-ai-helper.butler` | Butler er alltid innen rekkevidde | R | Fra hjelperen og fra hver flate kommer eieren til Butler i ett steg, og gjennom Butler til alt annet. Gjenbruker `purpose://skeleton.owner-entity-access`. | T-F | candidate · Fase 1 |
| F1 `purpose://candidate.butler.always-reachable` | Ett klikk til Butler, fra hvor som helst | F | Hver flate og hver hjelper har en synlig vei til Butler som virker. Det skal stå i Book 23 som eget formål ved siden av «egen entitet alltid nåbar». | T-F1: validering i CI + Playwright | candidate · Fase 1 |
| F2 `purpose://candidate.workbench-ai-helper.butler.handoff` | Hjelperen gir saken videre til Butler når den ikke kan selv | F | Ber eieren om noe settet ikke dekker, tilbyr hjelperen å sende samtalen og flaten videre til Butler, som ruter til riktig verktøy. | T-F2 | candidate · Fase 2 |
| F3 `purpose://candidate.workbench-ai-helper.butler.never-lose-entity` | En flate kan ikke låse deg ute fra din egen entitet | F | Flater som hjelperen lager eller endrer, får ikke lagres uten vei tilbake til egen entitet og Butler. Gjenbruker `purpose://skeleton.owner-entity-access`. | T-F3 | candidate · Fase 1 |

Regler: nye noder er `purpose://candidate.…`. Refs er engelske, titler norske. `purpose://candidate.butler.always-reachable` (F1) foreslås registrert i Book 23 ved siden av `purpose://skeleton.owner-entity-access`, ikke under hjelperen, fordi den gjelder alle flater.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en ny chatmotor. Butler Chat ruter og har autoriteten, AIGateway foreslår og får ikke verktøy (beslutning 2026-09-02).
- Ikke en ny kø. Agentjobber startes hos HavenAgentD, som eier kjøringen.
- Instruksjonstekst gir aldri rettigheter. Målcellen sjekker tilgang på hver handling.
- Ingen deling av sett mellom personer i første runde (spørsmål 2).

| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Arbeidsbenk-assistent-profil | spillverksted `contract/workbench-assistant-profile.v0.schema.json` | Har ingen instruksjonstekst eller versjoner | Ja (A) |
| Bekreft før utfør | `ExecutablePurposeGrounding.swift:45` | Bare chatHub kan godta forslag i dag | Ja (alle) |
| Porthole-editoren | `PortholeWebSessionSupport.swift:5929` | Sesjonsbundet kontrollerkode | Ja (B2) |
| WorkItem | `WorkItemCell.swift:929`, `:1018` | Ingen handling for mange | Ja (C1) |
| Publication / ArtistSales | `PublicationCell`, `ArtistSalesChannelCell.swift:369` | Ingen bildetekst på publisert verk | Ja (B1) |
| HavenAgentD | Workbench 1.0 WO-6 | Workbench er projeksjon | Ja (E3) |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Hjelperpanel i Developer Workbench (tom, fylt, feil) | bilde | `images/` | `hjelperpanel-{tom,fylt,feil}-v1.png` | venter (lagt fram 2026-10-09) |
| Redigering av et sett med versjoner | bilde | `images/` | `sett-rediger-v1.png` | venter (lagt fram 2026-10-09) |
| «Flytt alt fra inbox til triage» fra start til slutt | kjørende flate + testutdata | staging, `TESTRESULT.md#c1` | | nei |
| Sindres to eksempler | kjørende flate | `/pub/sindre-hustveit/verk` i staging | | nei |
| Butler-knapp i panelet og validering i CI | kjørende flate + testutdata | CI-logg | | nei |

## 6. Spørsmål som kan endre treet

1. Skal Butler-regelen (F1) inn i Book 23 som eget formål, eller utvide `skeleton.owner-entity-access`? Forslag: eget formål ved siden av.
2. Skal settene være eierens alene, eller delbare med Victoria, Vegar og Sindre? Forslag: eierens nå, deling senere.
3. Er fasene riktige: fase 1 sett, flaten du står i, ny flate og Butler; fase 2 Sindres eksempler, dokumentasjon og idéer; fase 3 PR for dokumenter og oppstart av agentjobber?

Ikke besvart ved G1 (2026-10-09). Standardsvarene gjelder til Kjetil sier noe annet: (1) eget formål i Book 23, (2) settene er eierens alene, (3) fasene som foreslått.

## 7. Iterasjoner
- 1 (2026-10-09): første tre, 6 grener og 19 bladformål. G1 godkjent 13:44Z.

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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://digital-work.collect-structured-input [active] — Collect structured input
- purpose://questionnaire.campaign.complete [active] — Complete questionnaire campaign
- purpose://gui.quality.functional-accessible [active] — Functional accessible GUI
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance
- purpose://questionnaire.access.audit [active] — Questionnaire access audit
- purpose://test.acceptance.questionnaire [active] — Questionnaire acceptance tests
- purpose://knowledge.explain-policy [draft] — Explain policy or rules
- purpose://self-determination.data.manner [candidate] — Manner of processing and derived data
- purpose://access.audit.privacy.database-key-custody [candidate] — Eierstyrt kryptering og nøkkellagring for celledata

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

## 6. Åpne spørsmål til Kjetil

1.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-10-09 | Opprettet | Losen |
