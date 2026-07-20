# Utviklermiljø for HAVEN og CellProtocol — funksjonsrapport og plan

Dato: 2026-07-20
Status: utkast til beslutning
Forfatter: Claude (på oppdrag fra Kjetil)

Denne rapporten svarer på: hva slags funksjonalitet må på plass for et
utviklermiljø for HAVEN og CellProtocol, hva har vi allerede som kan
gjenbrukes, hva må bygges nytt, og hvordan bygger vi inn insentiver,
gamifisering og — viktigst — et sosialt miljø som faktisk fungerer.

Rapporten bygger på kartlegging av CellScaffold, CellProtocol,
CellProtocolDocuments og DiMyDocuments per 2026-07-20, og komplementerer
`DevPlatform_Hetzner_CoPilot_Plan_2026-06-11.md` (som dekker
infrastruktur: bygg-node, CI, deploy). Denne rapporten dekker
utviklermiljøet som **produktflate i HAVEN selv**.

---

## 1. Sammendrag

- Vi har overraskende mye gjenbrukbart: dokumentasjonskorpus med
  RAG-flate, prosjekt-/todo-celler med GitHub-synk, invitasjons- og
  deltakelsesceller, chat, presence, purpose-matching og en spesifisert
  (men ubygget) `ContributionProofCell` for bidragsbevis.
- Det største hullet er ikke enkeltceller, men **samlingen**: det finnes
  ingen DeveloperWorkbench-flate som setter dokumentasjon, oppgaver,
  samarbeid og anerkjennelse sammen til ett miljø.
- Insentivmodellen bør bygges på HAVENs egne primitiver — verifiserbare
  bidragsbevis (proofs) og verdiretur (DiMy) — ikke på løsrevne
  XP-poeng. Gamifisering brukes som anerkjennelse og fremdriftsfølelse,
  ikke som konkurransepress.
- Foreslått plan: 6 faser, der fase 0–1 (samleflate + onboarding +
  dokumentasjon) kan settes opp nesten utelukkende med eksisterende
  celler og en ny CellConfiguration.

---

## 2. Prinsipper (førende for alt under)

1. **Utviklermiljøet er selv HAVEN.** Vi bygger det med native
   HAVEN-celler (integrasjonsceller er OK der eksterne systemer er
   primærkilde). Dogfooding er selve poenget: miljøet er den beste
   demoen av CellProtocol.
2. **GitHub er alltid primærkilde** for kode og issues; HAVEN-celler
   speiler og beriker, de erstatter ikke.
3. **Chat er sentralvinduet** (Book 19). Utviklermiljøet nås og styres
   fra Chat Workbench; egne flater åpnes derfra.
4. **Skeleton-formatets grenser respekteres.** Ny UI må uttrykkes i
   dagens CellConfiguration/skeleton-format; nye skeleton-kapabiliteter
   krever egen beslutning.
5. **Sosialt design foran mekanikk.** Anerkjennelse, synlighet og
   tilhørighet er målet; poeng og merker er bare virkemidler.

---

## 3. Funksjonell målbilde — hva et utviklermiljø må inneholde

| Område | Behov |
|---|---|
| Dokumentasjon | Søkbar og browsebar Book, maskinlesbar katalog, RAG-svar med kildehenvisning, gap-oversikt |
| Kode | Innsyn i repoer, PR-/issue-status, byggstatus, eksempler og maler for nye celler |
| Onboarding | «Første 60 minutter»: identitet, tilgang, første celle kjørende, første bidrag |
| Prosjekt/todo | Backlog, arbeidsoppgaver, porteføljeoversikt, GitHub-synk begge veier |
| Samarbeid | Invitasjoner, delte arbeidsflater, chat-rom per prosjekt, presence («hvem er her nå») |
| Sosialt | Utviklerprofiler, bidragshistorikk, matching av folk (mentor/pairing), showcase av arbeid |
| Insentiver | Verifiserbare bidragsbevis, anerkjennelse på profil, kobling til DiMy-verdiretur |
| Gamifisering | Kvester/oppdrag, milepæler, merker — uten rangeringspress |

---

## 4. Gjenbrukbar funksjonalitet (kartlagt)

### 4.1 Dokumentasjon og kunnskap — i stor grad på plass

- **Book-korpuset** (`CellProtocolDocuments/Book`, 33 kapitler +
  `book_catalog.json` + kontrakts-JSON-er). Kap. 10/11 (quickstart og
  celle-utviklerguide), 13 (agentinstruksjoner), 22 (Explore-kontrakter)
  er direkte utvikler-rettet.
- **HavenDocsMCP** (`Tools/HavenDocsMCP/haven_docs_mcp.py`) — read-only
  docs-MCP for agenter.
- **RAG-cellene**: `RAGGatewayCell`, `RAGCatalogIngestionCell`,
  `RAGPromptAdminCell` (+ konfigurasjonsfabrikker) gir docs-spørring som
  HAVEN-flate.
- **DiMyDevRAG** — korpuspolicy for privat utvikler-RAG.
- **Gap_Analysis.md** — vedlikeholdt oversikt over dokumentasjonshull.
- **Claude-skills** (20+ HAVEN-spesifikke) — de facto «pakket
  utviklerkompetanse» for agent-assistert utvikling.

Vurdering: innholdet finnes; det som mangler er en **lesbar flate i
HAVEN** (docs-browser-celle) i stedet for rå markdown på GitHub.

### 4.2 Prosjekt og oppgaver — kjernen finnes

- **`WorkItemCell` + `ProjectPortfolioCell` + `GitHubWorkSyncCell` +
  `WorkMutationSync`** (Cells/WorkItems) — arbeidsoppgaver med
  GitHub-repo-mapping, import og utgående synk. Dette er den viktigste
  gjenbruksgevinsten i hele kartleggingen.
- **`TodoCell`** — enkel todo, allerede brukt som byggekloss av
  `IdeaTaskWorkspaceCell` (idé → oppgave → deling via
  `IdeaTaskShareCell`, koblet mot Vault/VaultStudio).
- **`SimpleProjectManager`** (OrchestratorCell, ProjectOverviewCell,
  SimpleChatCell m.fl.) — eldre, men demonstrerer prosjekt-samleflate.
- **`ProjectOperations`** (DraftVersionCell, ServiceCatalogCell) og
  `Personlog`-projeksjonene (jobbprojeksjon, spørsmålsinnboks).
- **Sprint-konvensjon** finnes allerede
  (`Deliverables/Cell_Productivity_Tool_Sprint1/Sprint1_Backlog_Index.md`).

### 4.3 Samarbeid og sosialt — flere sterke primitiver

- **`ParticipationHubCell`** — invitasjoner (inbox/outbox), workspace-
  katalog, purpose-basert ruting av invitasjoner, klargjorte
  launch-konfigurasjoner. Dette er ryggraden for «bli med i prosjekt».
- **`ChatCell` / Chat Workbench** (Book 19) — sentralvinduet; scoped
  AI-provider-ruting finnes (ChatScopedAIProviderRouter).
- **`EntityPresenceRegistryCell`** — presence-register («hvem er her»).
- **Purpose/Interest-matching** (Book 09/14/26, MatchMaker-cellene) —
  gjenbrukbart for mentor-/pairing-matching og oppgaveanbefaling.
- **`ContactEndpointCell`** (Book 21) — kontakt på tvers uten å lekke
  identitet; riktig primitiv for å kontakte en vedlikeholder.
- **Offentlige profiler** (public presence-celler,
  `ConferencePublicProfileCell`) — grunnlag for utviklerprofiler.
- **Varsler**: `ScaffoldNotificationContracts` — kontraktfestet
  varselflyt.
- **`EntityGraph`/`Graph`-celler** — relasjonsgrafer, kan vise
  hvem-bidrar-hvor.

### 4.4 Insentiver og verdi — spesifisert, delvis bygget

- **ValueRedistribution-korpuset** (DiMyDocuments): `ContributionProof`
  og `ContributionProofCell` er spesifisert i `03_MECHANISM_SPEC.md`;
  ValuePoolPolicy/MicropayoutPolicy likeså. **Cellen er ikke bygget.**
- **`SMIAgreementSettlementCell`** (SomebodyMakeIt) — avtale →
  betingelser → bevis → oppgjør; malen for «bounty»-lignende oppdrag.
- **`AgreementWorkbenchCell`**, **`TrustPacketWorkbenchCell`**,
  **`PaymentGateCell`/`PaymentProofDoorCell`** — avtaler, tillit og
  betalingsporter.
- **`ProvingClaims`** (EventAdmissionIssuer/Verifier) — utsteder/
  verifiserer-mønsteret som bidragsmerker bør bygges på.
- Regulatoriske skinner finnes som skill
  (`dimy-payment-regulatory-guardrails`) — må brukes når insentiver
  nærmer seg pengeverdi.

### 4.5 Onboarding og distribusjon

- **`GuidedOnboardingCell`** (PersonalCopilot) — guidet onboarding
  finnes som mønster.
- **Developer Identity Pack** (Book 31 + Tools) — simulerte entiteter,
  identiteter og vault-referanser for realistisk testing uten delte
  hemmeligheter. Nøkkelbrikke for utvikler-onboarding.
- **`ScaffoldSetupCell`**, **`SoftwareDistributionCell`**, signert
  pkg + provisioning-pack (HAVENAgentD/Victoria) — distribusjonsløypa
  er løst for macOS-agenten.
- **Test- og verifikasjonsverktøy**: ScaffoldTestKit,
  kontrakttest-skills, parity-testing, funksjonell verifisering — alt
  gjenbrukbart som «kvalitetsport» for bidrag.

---

## 5. Hull — foreslått ny funksjonalitet

Prioritert rekkefølge:

1. **`DeveloperWorkbenchCell` + CellConfiguration (P0).** Samleflaten:
   faner for Docs, Mine oppgaver, Prosjekter, Folk, Min profil. Mest
   komposisjon av eksisterende celler; lite ny logikk. Startes fra Chat
   Workbench.
2. **`DocsBrowserCell` (P0).** Book-katalogen som navigerbar flate
   (kapittelliste fra `book_catalog.json`, visning via Markdown-cellen,
   «spør dokumentasjonen» via RAGGateway med kildehenvisning).
3. **Utvider `GitHubWorkSyncCell` med PR-/byggstatus (P1).** I dag
   issues/arbeidsoppgaver; utvid til PR-projeksjon og CI-status slik at
   «mitt bidrag» kan følges fra idé til merge. GitHub forblir primær.
4. **`ContributionProofCell` (P1).** Implementer spesifikasjonen fra
   ValueRedistribution 03: verifiserbart bevis for merget PR,
   dokumentasjonsbidrag, parity-fiks, review. Utstedes etter
   ProvingClaims-mønsteret; vises på profil.
5. **`RecognitionCell` / bidragsmerker (P2).** Merker («Første celle»,
   «Docs-forbedrer», «Parity-fikser», «Mentor») som *utstedte proofs*,
   ikke poeng i en database. Milepæler og valgfri fremdriftsvisning.
6. **Kvest-/oppdragsformat (P2).** Kuraterte, avgrensede oppgaver
   («bygg en celle som …») med definert belønning: SMI-avtalemønsteret
   for oppdrag med verdi, enkle WorkItems med merke-utfall ellers.
7. **`DeveloperPresence`-visning (P2).** ParticipationHub + presence-
   registeret: hvem er aktive nå, på hvilket prosjekt, åpne for hjelp?
8. **Mentor-/pairing-matching (P3).** Purpose-matching over
   utviklerprofiler: «vil lære skeleton-authoring» ↔ «kan veilede».
9. **Showcase-galleri (P3).** Publiserte CellConfigurations med
   attribusjon (ConfigurationCatalog + public presence): «se hva folk
   har bygget» — sterkeste sosiale draget for nye bidragsytere.

---

## 6. Insentiver og gamifisering — designvalg

**Grunnprinsipp:** indre motivasjon først (mestring, autonomi, mening),
ytre belønning som forsterkning. Forskningen er entydig på at
rangeringspress og poengjag korroderer nettopp den typen fellesskap
HAVEN trenger.

Anbefalt modell, i lag:

1. **Synlighet** (gratis, umiddelbart): bidrag vises på profilen og i
   prosjektets flate. «Noen så det jeg gjorde» er den sterkeste enkle
   motivatoren.
2. **Anerkjennelse**: merker som verifiserbare proofs — de har verdi
   fordi de kan *bevises*, ikke fordi de gir poeng. Takk-mekanisme i
   chat (lettvekts «kudos» knyttet til konkret bidrag).
3. **Fremdrift**: personlige milepæler og kvester («din første celle»,
   «ditt første merge»), aldri sammenlignende leaderboards som standard.
   Eventuelle fellesskapstall vises som *lagets* fremdrift («vi lukket
   14 oppgaver denne uka»).
4. **Verdiretur**: der bidrag har målbar verdi kobles ContributionProof
   til DiMy-mekanismene (ValuePool/Micropayout) — men all
   pengenær design går gjennom regulatorisk guardrails-sjekk før
   lansering. Start med ikke-monetær anerkjennelse; monetær pilot
   som egen beslutning.

**Sosiale funksjoner som må virke** (og som avgjør om miljøet lever):
invitasjon inn i prosjekt uten friksjon (ParticipationHub), chat-rom
per prosjekt med AI-hjelp i konteksten, presence, profil med historikk,
og et sted å vise frem arbeid (showcase). Alt annet er sekundært.

---

## 7. Plan

### Fase 0 — Samleflate av eksisterende celler (~1 uke)
DeveloperWorkbench-CellConfiguration med Todo/WorkItems,
ProjectPortfolio, ParticipationHub, Chat og RAG-spørring. Ingen nye
celler; ren komposisjon + skeleton-authoring. Verifiseres med
funksjonell service-verifisering.

### Fase 1 — Onboarding + dokumentasjon (1–2 uker)
DocsBrowserCell; utvikler-variant av GuidedOnboardingCell som bruker
Developer Identity Pack; mål: **ny utvikler har kjørende celle og
synlig profil innen 60 minutter**. Gap_Analysis-punkter som blokkerer
onboarding prioriteres.

### Fase 2 — Oppgaveflyt mot GitHub (1–2 uker)
GitHubWorkSyncCell utvides med PR-/CI-projeksjon; kvest-format v1
(kuraterte førstegangsoppgaver). Sprint-konvensjonen fra
Cell_Productivity_Tool_Sprint1 gjenbrukes.

### Fase 3 — Sosial kjerne (2 uker)
Prosjekt-chat-rom, presence-visning, invitasjonsflyt polert,
utviklerprofil (public presence-variant) med bidragshistorikk.

### Fase 4 — Anerkjennelse (2 uker)
ContributionProofCell + RecognitionCell/merker + kudos i chat.
Kun ikke-monetært i denne fasen.

### Fase 5 — Verdiretur-pilot (egen beslutning)
Kobling ContributionProof → ValuePool/Micropayout for utvalgte
bidragstyper. Forutsetter regulatorisk gjennomgang
(dimy-payment-regulatory-guardrails) og egen pilotramme.

**Tverrgående forutsetninger:**
- CellScaffold-testisolasjonen (kjente rekkefølgeavhengige feil) må
  lukkes før miljøet tar imot eksterne bidrag i skala — grønn suite er
  kvalitetsporten bidragsytere møter.
- Infrastruktur (bygg-node/CI/deploy) følger Hetzner-planen; denne
  rapportens faser er ortogonale, men fase 2 får full effekt først med
  CI-status å projisere.
- Hendelsesdrevet varsling (ikke polling) for alt som venter på
  GitHub/CI, i tråd med etablert arbeidsflytpraksis.

---

## 8. Risikoer

| Risiko | Avbøtning |
|---|---|
| Gamifisering oppleves som gimmick eller press | Anerkjennelse/proofs foran poeng; ingen rangering som standard; mål på *lagets* fremdrift |
| Insentiver blir pengenære uten regulatorisk avklaring | Fase 5 er egen beslutning bak guardrails-skill; fase 0–4 er ikke-monetære |
| Enda en flate som ikke vedlikeholdes | Alt bygges av celler som allerede har eiere/tester; GitHub forblir primærkilde så ingenting «dør» i HAVEN-speilet |
| Sosiale rom uten folk (kaldstart) | Start med det eksisterende miljøet (Kjetil + agenter + pilotbrukere); showcase og kvester gir innhold før fellesskapet vokser |
| Skeleton-formatet begrenser ønsket UI | Alle nye flater spesifiseres innenfor dagens format; utvidelser flagges som egne beslutninger |

---

## 9. Anbefalte neste steg

1. Beslutte navn/omfang for DeveloperWorkbench (fase 0) og starte
   CellConfiguration-komposisjonen.
2. Panelkjøring (haven-panel-task-decomposition) på insentivmodellen i
   kap. 6 før fase 4 designes i detalj.
3. Legge fasene inn som WorkItems med GitHub-synk — miljøet bygger seg
   selv fra dag én.
