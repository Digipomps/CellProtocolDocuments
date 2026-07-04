# HAVEN Rekursiv Funksjonalitet: Gap-Analyse Med GUI-Verifikasjon

Dato: 2026-07-03
Status: prosjekttilstand (deliverable), ikke kanonisk spesifikasjon.

Scope: CellProtocol-infrastruktur, Arendalsuka 2026, konferansetjenesten og
Co-Pilot Chat, vurdert mot målet om eksponensielt rekursiv funksjonalitet:
at brukere og aktører skal kunne skape ny funksjonalitet gjennom systemet
selv, slik at hver ny flate/aktør gjør systemet mer verdifullt for neste.

Metode: dokumentgjennomgang via HAVEN dokument-MCP, kodeverifikasjon i
CellScaffold/CellProtocol, GUI-verifikasjon på staging med Playwright
(fersk deltakerpersona), og Codex-samarbeid (`codex exec`, read-only) for
tilgangsoppskrift og implementasjonsstatus.

Staging-revisjoner testet:

- Første gjennomgang: `3d51a03` (build 2026-07-03T14:40Z)
- Re-test: `d8415fa` (build 2026-07-03T16:00Z, inkluderer
  `d0b6bed` "Improve Arendalsuka participant program UX" og
  `b115d8f` "Improve Co-Pilot chat clarification and inline polls")

## 1. Rekursjonskjeden og hvor den brytes

Ønsket sløyfe: bruker uttrykker formål i chat -> ruting til eksisterende
verktøy -> finnes ikke verktøyet, lages det -> publiseres gated i katalog ->
andre oppdager via purpose-matching -> aktører onboarder seg selv -> verdi
føres tilbake -> purpose-grafen vokser.

### Fungerer i dag (verifisert)

- Ledd 1-2 (formål -> verktøy): `ChatPurposeResourceRouter` +
  `ChatScopedAIProviderRouter` + `GroundedActionPlan`-verifisering.
  GUI-bevis: "jeg trenger mermaid diagram" ga korrekt match med direkte
  "Last inn flate" og kontraktsspråket "Ingenting lastes eller kjøres før
  du velger det". Idé-fangst matchet 0.80 med eksplisitt lagringskrav.
- Ledd 4 (gated publisering, lesesiden): `ConfigurationCatalogCell` med
  `matchPurpose`/`matchInterests`/`matchPrompt` og Agreement-gating
  (Arendalsuka-mønsteret med `remoteEventConfigurations.arendalsuka2026.*`).
- Ledd 5 (discovery): `PerspectiveCell` med portable purpose/interest-refs.
- Avtale/entity-fundament: aksepterte relasjoner persisteres kanonisk i
  begge parters `EntityAnchorCell` via `conference.relation.accepted.v1`
  (Book 18, fase 4 landet).

### Brudd (med kode-referanser)

1. Runtime-minting av nye flater finnes ikke.
   `addConfiguration`/`editConfiguration`/`updateConfiguration`/
   `removeConfiguration` i `ConfigurationCatalogCell` er deprecated stubs
   ("deprecated: edit owning cell configuration instead",
   `CellScaffold/Sources/App/Cells/ConfigurationCatalog/ConfigurationCatalogCell.swift`
   rundt linje 401). Nye celler krever Swift-kompilering og deploy.
2. Library/variant-arkitekturen er halvferdig. Implementert:
   `OwnedCellConfigurationLibraryStore` med `LibraryCellConfigurations.json`
   og `ActiveLibrarySelections.json`, `editableCellConfigurationLibrary`,
   `activeEditableCellConfiguration`, `selectEditableCellConfiguration`
   (`CellScaffold/Sources/App/Services/EditableCellConfigurationSupport.swift`).
   Ikke implementert: `library.fork`, `library.createFromCurrent`,
   `library.import` fra
   `CellScaffold/Documentation/CellConfiguration_Library_and_Variant_Architecture.md`
   (status proposed). "Library (91)" i Porthole er builtin-katalogen via
   `portholePublishedConfigurations()`, ikke et per-bruker-bibliotek.
3. Chat har ingen authoring-rute. Ingen kobling fra
   PersonalCopilot/ChatPurposeResourceRouter til `CellConfigurationStudioCell`
   eller library-laget. GUI-bevis (består på `d8415fa`): "lag en ny flate
   der frivillige kan koordinere vaktlister" ble flatet ut til å åpne
   eksisterende "Arendalsuka Event Atlas" (attpåtil admin/import-atlaset,
   ikke deltakerflaten).
4. Purpose-grafen er kompilert statisk. `PurposeKnowledgeBase.nodes` er
   `private static let` i
   `CellScaffold/Sources/App/Support/PurposeKnowledgeBase.swift`.
   Nye tjenester/aktører kan ikke registrere formål i runtime; grafen
   vokser bare ved rekompilering. (Ressurs-matchingen er derimot dynamisk
   mot synlige CellConfigurations.)
5. Aktør-onboarding via Co-Pilot er ikke bygget
   (`arendalsuka-2026-actor-onboarding-copilot`, P0 i workbench-seedet).
   Dette er den første ekte rekursjonssløyfen i produktplanen: aktører
   lager egne sider via chat med proof-gated publisering.
6. Modell-safety-gaten er ikke nådd. Beste frontier 82.1 % mot krav
   ~95 % intent/action og 100 % safety; safety svakest (55-65 %).
   Anbefalt fix (deterministisk HAVEN-policy for safety/action utenfor
   modellen) er dokumentert i
   `Deliverables/CoPilot_Chat_Quality_Evaluation_2026-06-23.md`, ikke
   implementert.
7. Entity/HAVENAgentD-credential-broen mangler. Blokkerte hosted-eval
   2026-07-01 og tvang nøkkelrotasjon i juni
   (`CellScaffold/Documentation/CoPilotChat_Advisor_Model_Access_2026-06-25.md`).
   Uten den kan ikke brukere/aktører trygt ta med egen AI-kapasitet.

Presisert hovedkonklusjon: infrastrukturen kan i dag gjenbruke, redigere og
variant-velge eksisterende flater i runtime, men ikke formere dem. Korteste
vei til rekursjon er å fullføre den allerede påbegynte library-arkitekturen
(fork/create/import) og eksponere den som chat-helper, ikke å bygge noe nytt.

## 2. GUI-verifikasjon på staging

Persona: fersk FidoUser via `/auth/register` (ingen agreements).
Artefakter: skjermbilder + sidetekst i Claude-scratchpad
(`gui-review-artifacts/`, sesjonsspesifikk katalog).

### Funn som består på `d8415fa` (re-testet)

- Agenda-feilruting: "Hva skjer etter lunsj på Arendalsuka i morgen?"
  rutes til invitasjonshjelperen ("Jeg bruker teksten som søk etter
  personen du vil invitere"). Book 19 kapittel 5 agenda-intent treffer ikke.
- "Lag en ny flate"-forespørsel åpner eksisterende atlas (rekursjonsgapet).
- Tomt hjelperpanel synlig i default ("Aktiv hjelper / 0 aktive hjelpere"
  med "Hent"/"Rydd alle"), i strid med Slice 1 i
  `CellScaffold/Documentation/CoPilotChat_CentralGUI_UXReview_2026-06-13.md`.
- "Ingen elementer" lekker flere steder rundt composeren.
- "Sendt til aktiv hjelper" vises samtidig med "0 aktive hjelpere".
- Engelsk statuslinje i deltakerflaten: "Synced 2218 session(s) and 0
  local actor(s) into participant-owned overlay."
- Nytt funn på `d8415fa` (bekreftet, ikke latency): fritekstsøk "demokrati"
  ga "2218 treff i filter" (ingen innsnevring) og "0 kort vises nå" i over
  50 sekunder etter Søk-klikk; programlisten forble "Velg filter for å
  starte". Fritekstsøket verken smalner filtertreff eller henter
  arrangementskort. Må feilsøkes som del av
  `arendalsuka-2026-program-ux-polish`.

### Forbedret på `d8415fa`

- Tomtilstanden i programfanen er nå korrekt norsk og guardrail-riktig:
  "2218 arrangementer er tilgjengelige. Velg dag, tema, formål eller søk
  for å vise et håndterlig utvalg."
- Dag/tema/formål-filtrene er fullt befolket etter overlay-sync.

### Datastatus Arendalsuka (endret i dag)

- Atlas-import kjørt på staging 2026-07-03T15:27Z: 2218 sesjoner.
- Deltaker-overlay krever eksplisitt sync per deltaker:
  "Oppdater program" -> `participant.refreshFromAtlas`
  (`CellScaffold/Sources/App/Cells/Arendalsuka/ArendalsukaParticipantProgramCell.swift`).
  Verifisert: synket 2218 sesjoner for to personas.
- 0 lokale aktører: POI-importen (restauranter, scener, praktiske punkter)
  er ikke kjørt. Blokkerer kart-milepælen og local-actor-formålene.
- Atlaset er identity-scoped; import må gå gjennom published
  surface-requester for at public reads skal se dataene
  (`CellScaffold/Sources/App/Controllers/VaporConferenceMVP.swift`, ca.
  linje 311).

### Konferanseflatene

`/conference-public` og `/conference-participant` fungerer med demodata
(DiMy 2026). Personvernmodellen er synlig i GUI (matchmaking on,
sponsorInsights off, aggregate-only organizer-språk). Gjenstående
arkitekturgap fra Book 17/18: `ConferenceConnectionHubCell` er fortsatt
"full truth in one cell", ikke gjenoppbyggbar indeks med entity-refs.

## 3. Prioritert rekkefølge

1. Nå: POI-import + fritekstsøk-feilen; katalog-tilgangsbeslutning
   (Agreement-beta vs. public flag) før Binding remote-load smoke.
2. Chat-kvalitet: deterministisk safety/action-policy utenfor modellen +
   agenda-ruting (feilrutingen er målbar og demo-kritisk).
3. Første rekursjonssløyfe: actor-onboarding-copilot (P0 for Arendalsuka
   og bevis på konseptet).
4. Runtime-minting, trygt: fullfør library fork/create/import per vedtatt
   arkitektur, proof/agreement-gated, og eksponer som chat-helper
   ("Lag din egen variant av denne flaten").
5. Levende purpose-graf: persistert runtime-overlay over
   PurposeKnowledgeBase med provenance.
6. Entity/HAVENAgentD credential-bro for bring-your-own-model.

## 4. Tilgangsoppskrift (for agenter)

Staging:

- Base: `https://staging.haven.digipomps.org` (helse: `/health/ready`,
  revisjon: `/health/build`)
- Auth: `POST /auth/register|login` med testbruker-mønsteret fra
  `CellScaffold/playwright/personal-chat-prompt.spec.js`
- Porthole deep links (web-shell `/browserhead/webo`, klassisk `/porthole`):
  - Co-Pilot Chat: `configurationName=Co-Pilot Chat`,
    `configurationEndpoint=cell:///PersonalChatHub`
  - Arendalsuka: `configurationName=Arendalsuka Participant Program`,
    `configurationEndpoint=cell:///ArendalsukaParticipantProgram`
  - Landing: `/arendalsuka` (videresender til deep link)
- Åpne uten login: `/conference-public`, `/conference-participant-preview`

Lokalt:

- `swift run Run` i CellScaffold (port 9089, localhost-fallback for
  passkeys). Arendalsuka er tom lokalt uten import.
- Skeleton-iterasjon uten rebuild:
  `npm run skeleton:iterate -- --scenario <fil>` (preview/commit-runtime/
  review), se
  `CellScaffold/Documentation/Skeleton_Runtime_Iteration_Workflow.md`.

Codex-samarbeid: `codex exec --sandbox read-only -C <repo> "<spørsmål>"`
fungerer godt; Codex MCP fra Claude Code trenger høyere klient-timeout enn
60 s for repo-utforskende spørsmål.

## 5. Usikkerheter

- "Treff i filter"-telleren kan ha annen semantikk enn antatt
  (matcher-i-filter vs. matcher-i-søk); selve kort-tomheten etter søk er
  uansett bekreftet over 50 s.
- Apple/Binding-paritet er ikke re-verifisert i denne runden; siste
  kjente status er 27/27 `ChatWorkbenchParityTests` på macOS/iPhone/iPad
  mini (2026-06-22/23), iPad Pro-simulator fortsatt ukjent.
