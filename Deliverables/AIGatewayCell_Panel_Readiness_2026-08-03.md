# Modenhetsevaluering: AIGatewayCell som vert for rådgiverpanelet

**Dato:** 2026-08-03 · **Oppdragsgiver:** Kjetil
**Spørsmål:** Hvor modent er celle-oppsettet for å kjøre rådgiverpanel på linje
med det vi kjørte 02.–03.08?

**Metode:** Kodelesing i `CellScaffold` og `CellProtocolDocuments` på merget
`main` (e11bc32). **Ingenting er kompilert eller kjørt.** Alle påstander under
er lest ut av kilde og tester, ikke observert i drift. Dette er min egen
vurdering — ikke en panelkjøring.

> **Revidert 2026-08-03 etter innspill fra Kjetil.** Første versjon påsto at
> retrieval manglet helt. **Det var galt.** `WebKnowledge`-cellene fantes, men
> katalogen falt utenfor listen jeg genererte, og jeg søkte etter feil ord —
> «web», «fetch» og «browse» i filnavn, ikke i klassenavn inne i en samlefil.
> Blokker B1 er trukket. B2 er innsnevret. Se §2.

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

## 2. Hva som mangler for vårt bruk — revidert

### B1 — TRUKKET. Retrieval-cellene finnes.

`CellScaffold/Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift` (1355
linjer) inneholder fem celler:

| Celle | Linje | Modenhet |
|---|---|---|
| `WebFetchCell` | 379 | **Fungerer** |
| `WebSearchCell` | 544 | **Tom sokkel** |
| `ScopedCredentialCell` | 679 | **Fungerer** |
| `SourceIngestionCell` | 816 | Kilderegistrering |
| `TruthSourceManagerCell` | 984 | Kildekatalog |

**`WebFetchCell` gjør ekte HTTP** (`URLSession.shared.data(for:)`, linje 510)
med reelle skranker: HTTPS-påkrevd som standard, vert må finnes, 15 s timeout,
byte-tak, klippet tekstforhåndsvisning. Hver henting blir en post med
`purposeRefs`, `interests` og `credentialAlias`, merket `sideEffect: false`,
med auditevent `web.fetch.completed`.

**`ScopedCredentialCell` er nettopp den du beskrev.** Owner-only tilgang,
per-requester scoping, hemmeligheter redigert bort i svar
(`"secret": .string("redacted")`), og `upsert`/`remove`/`clear`. Den har
allerede en bro til AI-laget: `upsertAIGatewaySecret`.

Koblingen mellom dem er stram på riktig måte — credential injiseres bare ved
**dobbelt samtykke**:

```swift
if let alias = optionalString("credentialAlias", in: object),
   WebKnowledgeValue.bool("allowCredentialUse", in: object),
   let secret = ScopedCredentialRegistry.secret(requester: requester, alias: alias) {
    request.setValue("Bearer \(secret)", forHTTPHeaderField: "Authorization")
}
```

**`WebSearchCell` er derimot ikke implementert i substans.**
`static var searchProvider` er `nil`, og **ingenting i hele kodebasen
registrerer en** — de eneste treffene utenfor cellen er to testlinjer som
setter den til `nil`. Cellen er ærlig om det: den rapporterer
`provider_unconfigured`, `providerConfigured: false` og
`queryIsSentToProvider: false`. Men den kan ikke søke.

**Testdekning: 8 tester, 214 linjer** — mot AIGatewayCells 33/1992. Og de
tester *sikkerhet*, ikke *funksjon*: owner-only, redaksjon, HTTPS-blokkering,
sideeffektfrihet uten leverandør. Det finnes **ingen test på at en henting
lykkes**, og **ingen test på at et scopet credential faktisk brukes** i en
autentisert henting. Lykkestien er uprøvd.

**Én begrensning som traff denne sesjonen direkte:** injeksjonen er
`Bearer <secret>` og ingenting annet. Ingen cookie, ingen sesjon, ingen
skjemainnlogging. Begge artiklene vi analyserte lå bak Aftenpostens
betalingsmur, og jeg kom gjennom via Safari med din innloggede sesjon.
`WebFetchCell` ville ikke klart det. Bearer-token-API-er ja;
cookie-baserte nettsteder nei.

### B2 — Innsnevret. Delene finnes, cellen gjør ikke.

Du har rett i at dette hører hjemme i en egen celle, og at det å skille den ut
gjør varianter enklere å bytte. Slik står det i dag:

- **Ingen dedikert celle finnes.** Søk på `TranscriptCell`, `TranscriptionCell`,
  `RetentionCell`, `ConversationArchive`, `EphemeralStore` gir null treff i
  både `CellProtocol` og `CellScaffold`.
- **`AIAssistantThreadCell`** persisterer `messages` med tilgangsgrants
  (`AIAssistantThreadCell.swift:186–293`). Nærmest på lagring.
- **`ObjectStorageAdapterCell`** har ekte `deleteObject` med lokal sletting og
  flow-event `object-storage.object.deleted.v1`. Men dens `ttlSeconds` gjelder
  presignerte lese-URL-er, ikke oppbevaring — og den kodestien returnerer
  `"status": "unsupported"`, `"enforceable_presign_not_configured"`.
- **`PersonalDataTrustPackageCell`** har retensjons-*vokabularet*
  (`retentionMode`, `expiresAt` i Explore-skjemaet, linje 66–83). Men den sier
  selv: «Clear the in-memory proposal. **Does not delete Entity data because
  this cell cannot write it.**» Den er en forslags- og samtykkeflate, ikke et
  lager.

De tre kravene dine — hold til brukeren flytter det, TTL med policystyrt
autosletting, og selvopprydding på kommando — har altså **vokabular** ett sted
og **lagring** et annet, men ingen celle som håndhever dem sammen. Det er en
mindre jobb enn jeg først anslo, men den er ikke gjort.

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
| Credentials og styring | **Modnere enn vår** | `ScopedCredentialCell` + AIGateways secret store. Klar oppgradering |
| Billing og kvote | **Moden** | Vi har ingenting tilsvarende |
| Adjudikasjon | **Delvis** | Én adjudikator finnes; to med utfordring gjør ikke |
| Henting av URL | **Fungerer, uprøvd lykkesti** | `WebFetchCell`. Bearer-auth, ikke cookie/sesjon |
| Websøk | **Sokkel uten leverandør** | `WebSearchCell.searchProvider` er `nil` og registreres aldri |
| Evidensbevaring | **Deler finnes, celle mangler** | Vokabular i PDTP, lagring i Thread/ObjectStorage |
| D2-guards | **Ikke modellert** | Fungerer som prompt, men håndheves ikke |

---

## 4. Anbefaling

Etter revisjonen er veien kortere enn jeg først skrev. Rekkefølgen er styrt av
hva som blokkerer hva:

1. **Skriv transkripsjonscellen.** Den er nå den eneste ekte blokkeren for å
   kjøre metoden i cellelaget. Bruk `PersonalDataTrustPackageCell`s
   retensjonsvokabular (`retentionMode`, `expiresAt`) som kontrakt, og la
   cellen eie tre operasjoner: hold, flytt ut, rydd. Autosletting ved TTL må
   være policystyrt, ikke innebygd — det er nettopp det som gjør varianter
   byttbare.
2. **Legg til prompt/respons-hashing** i `AIGatewayCell` (G3). Liten jobb,
   og uten den kan et sitert panelsvar ikke bevises uendret.
3. **Bytt runnerens HTTP-lag mot `AIGatewayCell.invoke`** med `mode: .swarm`
   og `agentInstructions` per panelist. Da arves secret store, kvote og
   verktøypolicy gratis.
4. **Skriv en test på lykkestien for `WebFetchCell`**, inkludert at et scopet
   credential faktisk brukes. Åtte tester som alle dekker sikkerhet og ingen
   som dekker funksjon, er ikke nok til å tørre å bygge retrieval oppå.
5. **Avgjør hva `WebSearchCell` skal være.** Enten registrer en leverandør, eller
   marker den eksplisitt som uferdig. Slik den står, ser den ferdig ut i
   celleoversikten og svarer `provider_unconfigured` i drift.
6. **Ikke bruk `normalizedMajority`.** Modellér den andre adjudikatoren som en
   egen `invoke` med utfordringen i prompten.

Nettoen står, men svakere enn før: cellelaget er **nærmere å kunne eie hele
metoden** enn jeg først vurderte. Retrieval finnes, credentials finnes,
fan-out og adjudikasjon finnes. Det som gjenstår er evidensbevaringen — og
den er en avgrenset celle, ikke et arkitekturproblem.

Metoden selv bør likevel bli værende i Book 30 og skillen. En gateway skal
ikke eie hva som teller som et lukket claim.

---

## 5. Det jeg ikke har verifisert

| Punkt | Hvorfor det står åpent |
|---|---|
| Om NanoGPT faktisk virker gjennom `openAICompatible` | Lest ut av `baseURL`-håndtering, ikke testet mot ekte endepunkt |
| Om 7 samtidige `:thinking`-modeller tåler cellens timeout-regime | Vi så `RemoteDisconnected` på 340 s med runneren; cellens `timeoutMs` er per rute, men grensene er ikke prøvd |
| Om billing-laget vil belaste ekte kvote under paneldrift | `AIGatewayNoopQuotaAuthorizer` brukes i test; produksjonsatferd ikke undersøkt |
| Om `AIAssistantThreadCell` faktisk kan bære orkestreringskandidater | Den persisterer `messages`; om kandidatstrukturen passer, er ikke sjekket |
| Om `WebFetchCell` faktisk henter mot et ekte endepunkt | Ingen test dekker lykkestien; jeg har lest koden, ikke kjørt den |
| Om `ScopedCredentialRegistry` overlever omstart | Den er `enum` med statisk lagring per requester; persistens er ikke undersøkt |

Punkt 2 og 3 bør avklares før noen migrering, ikke etter.

**Metodenotat om denne revisjonen.** Feilen min var ikke at jeg leste feil, men
at jeg lette feil: jeg søkte etter «web», «fetch» og «browse» i *filnavn*, og
`WebKnowledge`-katalogen falt dessuten utenfor en `head -60`-avkortet liste.
Fem celler lå i én samlefil. Det er samme klasse feil som D2 ble skrevet for å
fange — jeg konkluderte «finnes ikke» fra mitt eget søk uten å teste søket.
Riktig grep hadde vært å liste alle celle-kataloger fullstendig og grep-e etter
`final class .*Cell` i innholdet, ikke i filnavnene.
