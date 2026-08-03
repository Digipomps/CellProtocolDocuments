# Modenhetsevaluering: AIGatewayCell som vert for rådgiverpanelet

**Dato:** 2026-08-03 · **Oppdragsgiver:** Kjetil
**Spørsmål:** Hvor modent er celle-oppsettet for å kjøre rådgiverpanel på linje
med det vi kjørte 02.–03.08?

**Metode:** Kodelesing i `CellScaffold` og `CellProtocolDocuments` på merget
`main` (e11bc32). **Ingenting er kompilert eller kjørt.** Alle påstander under
er lest ut av kilde og tester, ikke observert i drift. Dette er min egen
vurdering — ikke en panelkjøring.

---

## 0. To avklaringer først

**Din antakelse stemmer.** `run_advisory_panel.py` er frittstående: ingen
referanse til CellProtocol, AIGateway eller `cell://`. Den snakker direkte med
et OpenAI-kompatibelt endepunkt over `urllib`, med API-nøkkelen fra en
miljøvariabel. Panelet vi har kjørt har ikke rørt celle-laget.

**`AIAgentCell` finnes ikke som celle** — og det er ikke en mangel. Navnet
opptrer to steder, begge som *brukerytringer*:

- `CellScaffold/Documentation/GuidedOnboardingDialogue.md:133` — eksempel på hva
  en bruker kan si: «jeg vil bruke AIAgentCell med min egen API-nøkkel»
- `CellScaffold/Tests/AppTests/ChatPurposeResourceRouterTests.swift:280` —
  testen `testRoutesAdvisorPanelAPIKeySetupPromptToAIWorkspace` router nettopp
  frasen «sett opp rådgiverpanelet mitt med egne API-nøkler i AIAgentCell» til
  AIGateway-workspacet

Altså: et tilsiktet brukersynonym som routeren håndterer med vilje. Den
implementerte cellen heter **`AIGatewayCell`**, og evalueringen gjelder den.

Verdt å merke seg: **«rådgiverpanel» er allerede et modellert brukerformål** i
onboarding-flyten. Noen har tenkt på dette bruket før.

---

## 1. Hva som allerede er modent

`AIGatewayCell` er 3072 linjer med 33 tester (1992 linjer). Dette er ikke en
skisse.

### Fan-out med roller — strukturelt nesten identisk med panelmetoden

`invokeRouteAttemptsInParallel` (`AIGatewayCell.swift:1563`) kjører N ruter
parallelt med bundet samtidighet, beholder **alle** resultater og sorterer dem
på `routeIndex`. Hver rute får en rolle via `role(for:)`.

Orkestreringsmodusene er implementert og testet, ikke bare deklarert:

| Modus | Testdekning |
|---|---|
| `orderedFailover` | `testInvokeFailoverUsesSecondRouteAndCommitsQuotaOnce` |
| `parallelFanOut` | `testParallelFanOutRunsAllRoutesAndSettlesActualAggregateUsage` |
| `voting` | `testVotingSelectsNormalizedMajorityDeterministically` |
| `adjudicated` / `swarm` | `testSwarmAppliesAgentRolesAndUsesAdjudicatorOutput` |

Swarm-testen er den avslørende. Den setter opp to ruter med
`agentInstructions` («Create a plan.» / «Find risks.»), en egen
`adjudicatorRoute`, og verifiserer at adjudikatoren får kandidatene i prompten
(«Candidate 0»). **Det er runde 1 + runde 2 av vår metode, i én celle.**

### Kandidatposten er rikere enn vår

`AIGatewayOrchestrationCandidate` (`AIGatewayModels.swift:807`) bærer
`routeIndex`, `providerID`, `model`, `role`, `status`, `selected`,
`outputText`, `finishReason`, `usage`, `durationMs`, `warnings`, `error` og
`toolPolicyDecision`. Vår runner lagrer mindre.

### Nøkkelhåndtering er klart bedre enn vår

Vår runner tar en rå `NANOGPT_API_KEY` fra miljøet. Cellen har alias-basert
secret store, requester-scopede credentials, sesjonsnøkler, redaksjon av
hemmeligheter ved feil, og tester på at én identitet ikke får bruke en annens
nøkkel (`testRequesterCannotUseAnotherIdentityScopedCredential`).

### Kapasitet og transport holder

- 12 ruter validerer innenfor produksjonsgrensen; vi brukte 7 panelister
- `baseURL` er konfigurerbar per rute → NanoGPT går som `openAICompatible`
- Tre API-dialekter: OpenAI Responses, OpenAI Chat Completions, Anthropic Messages
- Billing med preflight-reservasjon, eksakt etteroppgjør og fail-closed

---

## 2. Hva som mangler for vårt bruk

Fire gap. To er reelle blokkere.

### B1 — Ingen retrieval. **Blokker.**

Dette er det tyngste. Verdien i begge panelkjøringene kom fra å **hente kilder
før claims ble lukket** — D2s G1, og det som snudde flest konklusjoner begge
dager. Cellen har verktøy*policy* (`denyAll`, `allowListed`, `auditOnly`,
per-agent-håndhevet og testet i `testPerAgentToolPolicyDeniesUndeclaredToolsBeforeProviderCall`),
men ingen web- eller hentesverktøy i kapabilitetskatalogen.

Konsekvens: retrieval må uansett skje utenfor cellen. Det er ikke
diskvalifiserende — det er slik vi jobber i dag — men det betyr at cellen
ikke kan kjøre metoden alene.

### B2 — Ingen varig transkripsjon. **Blokker.**

Kandidatene lever kun i responsobjektet. Regnskapsjournalen utelater prompt og
output **med vilje** — det er testet:
`testAccountingJournalPersistsAcrossEncodingAndExcludesPromptAndOutput`.

For panelarbeid er de ordrette transkriptene *selve evidensen*. Runde 1-svarene
i `round1/` er det leveransen hviler på. En kjøring gjennom cellen slik den står
ville produsert et svar og kastet grunnlaget.

Delvis vei ut: `AIAssistantThreadCell` persisterer `messages` med
tilgangsgrants (`AIAssistantThreadCell.swift:186–293`). Den er den naturlige
verten hvis transkripsjon skal overleve.

### G3 — Ingen proveniens-hashing av prompt og svar

`AIGatewayHasher.sha256Hex` finnes, men brukes til journal-ID-er,
requester-hash og feildigest. `LocalLLMGatewayCell` har `promptHash`;
`AIGatewayCell` har ikke prompt/respons-hash slik vår runner skriver dem.
Uten det kan man ikke i ettertid bevise at et sitert panelsvar er uendret.
Liten jobb, men den mangler.

### G4 — Metodeformen er én runde, ikke flere

Swarm er fan-out + adjudikasjon i ett kall. Vår metode er runde 1 → *menneskelig
retrieval* → runde 2 med korrigert brief (D2 G4), og to adjudikatorer der den
andre får en utfordring (G5). `adjudicatorRoute` er entall.

Dette er løsbart ved å kalle `invoke` flere ganger — men cellen har ingen
forestilling om en korreksjonsrunde, og ingenting håndhever briefgranskingen
(G2/G3). De er ren promptinnhold, så det er ingen sperre; det er bare ikke
modellert.

### En felle du bør kjenne til

`selectionStrategy: .normalizedMajority` ser ut som en gave til panelbruk. **Den
er metodisk gal her.** Book 30 sier eksplisitt at panelet ikke er en
stemmemaskin, og at uenighet mellom roller er signal, ikke støy å midle bort.
Begge kjøringene våre bekreftet det: i Ceuta-saken var adjudikatorenes uenighet
selve funnet, og i KI-saken felte adjudikator B panelet, ikke objektet.

`voting`/`normalizedMajority` er riktig for «hvilket svar er mest robust»,
ikke for «hva bærer argumentasjonen». Bruk `adjudicated`/`swarm`.

---

## 3. Modenhet per lag

| Lag | Modenhet | Vurdering |
|---|---|---|
| Transport, fan-out, roller | **Moden** | Implementert, testet, kapasitet holder. Kan tas i bruk som den står |
| Credentials og styring | **Modnere enn vår** | Klar oppgradering fra rå miljøvariabel |
| Billing og kvote | **Moden** | Vi har ingenting tilsvarende |
| Adjudikasjon | **Delvis** | Én adjudikator finnes; to med utfordring gjør ikke |
| Evidensbevaring | **Ikke klar** | Blokker B2 |
| Retrieval | **Fraværende** | Blokker B1 |
| D2-guards | **Ikke modellert** | Fungerer som prompt, men håndheves ikke |

---

## 4. Anbefaling

**Ikke migrer hele metoden. Flytt transportlaget, behold resten utenfor.**

Konkret, i rekkefølge:

1. **Legg til prompt/respons-hashing** i `AIGatewayCell` (G3). Minst arbeid,
   størst gevinst for etterprøvbarhet, og gjør cellen sammenlignbar med runneren.
2. **Bestem hvor transkriptene skal bo** (B2). Enten utvide
   `AIAssistantThreadCell` til å persistere orkestreringskandidater, eller la
   runneren fortsatt skrive leveransefilene og la cellen eie kall og betaling.
   Sistnevnte er billigst og bevarer dagens arbeidsflyt.
3. **Bytt runnerens HTTP-lag mot `AIGatewayCell.invoke`** med
   `mode: .swarm`, `agentInstructions` per panelist. Da arver vi
   secret store, kvote og verktøypolicy gratis, og mister ingenting — forutsatt
   at 1 og 2 er på plass.
4. **La retrieval bli værende utenfor** (B1) til det finnes hentesverktøy.
   Ikke bygg det for panelets skyld alene.
5. **Ikke bruk `normalizedMajority`.** Modellér den andre adjudikatoren som en
   egen `invoke` med utfordringen i prompten.

Nettoen: cellen er **moden nok til å eie kallene**, men ikke til å eie
*metoden*. Det er en riktigere arbeidsdeling uansett — metoden hører hjemme i
Book 30 og skillen, ikke i en gateway.

---

## 5. Det jeg ikke har verifisert

| Punkt | Hvorfor det står åpent |
|---|---|
| Om NanoGPT faktisk virker gjennom `openAICompatible` | Lest ut av `baseURL`-håndtering, ikke testet mot ekte endepunkt |
| Om 7 samtidige `:thinking`-modeller tåler cellens timeout-regime | Vi så `RemoteDisconnected` på 340 s med runneren; cellens `timeoutMs` er per rute, men grensene er ikke prøvd |
| Om billing-laget vil belaste ekte kvote under paneldrift | `AIGatewayNoopQuotaAuthorizer` brukes i test; produksjonsatferd ikke undersøkt |
| Om `AIAssistantThreadCell` faktisk kan bære orkestreringskandidater | Den persisterer `messages`; om kandidatstrukturen passer, er ikke sjekket |

Punkt 2 og 3 bør avklares før noen migrering, ikke etter.
