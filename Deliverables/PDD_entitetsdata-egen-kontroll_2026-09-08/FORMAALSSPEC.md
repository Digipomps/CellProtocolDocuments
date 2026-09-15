# Formålsspesifikasjon — entitetsdata egen kontroll

Oppgavemappe: `PDD_entitetsdata-egen-kontroll_2026-09-08` · Opprettet 2026-09-08 · Iterasjon 4 · **G1 godkjent 2026-09-15** · venter på G1-GUI

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Når jeg skal gjøre endringer i mine entitydata må det være innenfor min entity - det betyr at jeg kan gjøre en fileupload for eksempel eller be en ai i AIGatewayCell administrere og utføre endringen innenfor min entitet — altså med celler jeg eier - om det ikke er nok funksjonalitet til å gjøre det må vi lage dem. ai modellen må være en jeg stoler på - men det kan godt være hostet i en annen tjeneste så lenge jeg har indikert at jeg stoler på den. Eller det kan være en lokal - eventuelt bare funksjonalitet som redigerer i datastrukturen uten noe ai-hjelp - men det må være under min private kontroll. Det skal være umulig for andre å endre mine entitetsdata om jeg ikke eksplisitt gir tillatelse.

**Tillegg 2026-09-08 (ordrett):**

> Legg inn filimporten. Men det skal være umulig om du ikke kan bevise at du er autentisert mot din egen Entitet å både lese og mutere entitydata. Det steget som er viktigst av alt er når en bruker starter HAVEN funksjonalitet første gang og entiteten sikrer seg data og midler slik at bare den som initsierte den noen gang kan slippe inn. Men vi trenger gode verktøy, også chat som kan slå opp keypaths og gjøre endringer i tillegg til et enkelt å bruke og helt generelt gui verktøy.

**Klargjøring 2026-09-15 (ordrett), sammen med G1-godkjenning:**

> EntityAnchor vil lages med en gang entiteten trenger å persistere entitydata - altså med en gang en onboarding starter å samle data som må persisteres i entitydata. Import av adressebok-data for å invitere personer som ikke har en representasjon i HAVEN - eller som vi ikke vet har det skal føre til opprettelse av entitydata. VC beviser skal også i entitydata. Jeg har gått igjennom G1 og den er godkjent. Vi må legge inn støtte for betalinger etterhvert med palazzos egen psp. Men det krever at vi får inn `DiMyMint` og `DiMyMicropayments`

Tre valg tatt av Kjetil 2026-09-08, før dekomponering:

1. **AI-autoritet:** modellen *foreslår*, eieren *signerer*. Modellen har aldri skriverett.
2. **Gateway:** ny `cell:///AIGateway` registrert `identityUnique` i Binding, eid av eierens private identitet.
3. **Tillitsregister:** egen post under EntityAnchor (`trustedModels.<id>`), ikke TrustedIssuers.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| `AIGatewayCell` finnes | **retrieved** — men bare i CellScaffold, registrert `identityUnique` + `.persistant` | `CellScaffold/Sources/App/configure.swift:1162,1248` |
| `AIGateway` er tilgjengelig i min egen app | **contradicted** — ingen `name: "AIGateway"` i Binding; resolverens registreringsliste ved kjøring inneholder den ikke | grep over `Binding/`; DIAG-logg `bind8.log` |
| Binding har likevel en AI-vei | **retrieved** — `ConferenceAIAssistantGatewayProxyCell` peker på `cell:///AIGateway` (uregistrert lokalt) og faller tilbake til `cell://staging.haven.digipomps.org/ConferenceAIGatewayPreview` | `Binding/Binding/BootstrapView.swift:2925-2927` |
| Lokale modeller finnes | **retrieved** — `LocalLLM`, `RemoteLLM`, `AppleIntelligence` er registrert i Binding | `Binding/Binding/BootstrapView.swift` |
| Filopplasting med drop er mulig i skeleton | **retrieved** — `SkeletonFileUpload` med `supportsDrop`, `uploadMode`, `acceptedContentTypes` | `CellProtocol/Sources/CellBase/Skeleton/AttachmentSurface.swift:292` |
| Andre kan ikke skrive i mine entitetsdata i dag | **retrieved** — `validateIdentityUniqueOwner` krever samme uuid *og* samme signeringsfingeravtrykk *og* `bindStoredOwnerToRuntimeIdentity`; `checkIdentityOrigin` signerer en utfordring og verifiserer mot lagret nøkkel | `CellProtocol/Sources/CellBase/Cells/CellResolver/CellResolver.swift:2765-2800`, `GeneralCell.swift:2129` |
| Entitetsskriving går gjennom en eiersignert journal | **retrieved** — `EntityBatchPersistEnvelope` + `persist(envelope:mutationID:purposeRef:requester:…)`; EntityAnchor slipper relasjonsnavnerommet inn kun via batch-veien | `Binding/Binding/PersonalChatChronicle.swift:415-`, `CellProtocol/.../EntityAnchorCell.swift` |
| Et tillitsregister for *modeller* finnes | **unavailable** — `TrustedIssuers` gjelder utstedere av legitimasjon og er dessuten `scaffoldUnique` | `Binding/Binding/BootstrapView.swift:766-771` |
| Relasjonsflaten kan ta imot en fil i dag | **contradicted** — sju seksjoner er uoppnåelige, blant dem `pickFile` og `import.commit` | `testNoLocalSurfaceHidesItsOwnWaysIn`, rød 2026-09-05 |
| ~~Eieren har *én* identitet~~ — **feil premiss, rettet av Kjetil 2026-09-08** | **contradicted** — Entiteten er eierenheten; Identiteter er (i utgangspunktet) anonyme representanter for den, uten antallsbegrensning, knyttet til identityDomains. Oppstart og Face ID er to Identiteter for *samme* Entitet. | Kjetil, 2026-09-08 |
| Entitetsmodellen finnes i koden | **retrieved** — `EntityBindingDescriptor` (`localEntityAnchor`/`pairwise`/`blinded`), `SameEntityIdentityLinkCredentialSubject` med `approvedDomains`, `approvedIdentityContexts`, `approvedScopes`, `validUntil`, `revocationReference` | `CellProtocol/Sources/CellBase/Identity/IdentityLinkingModels.swift:23,51,247` |
| Entitetslenker leses av entitetsankeret | **retrieved** | `Sources/CellApple/Cells/EntityAnchorCell.swift`, `Sources/CellVapor/Cells/EntityAnchorCell.swift` |
| **Autorisasjonen kjenner entiteten** | **contradicted** — hverken `GeneralCell.swift` eller `CellResolver.swift` refererer `IdentityLink` i det hele tatt. Eierskap avgjøres Identitet-mot-Identitet: samme uuid *og* samme signeringsfingeravtrykk. | `GeneralCell.validateIdentityUniqueOwner`, `CellResolver.swift` — søk gir null treff på `IdentityLink` |
| Entiteten forsegles ved første kjøring | **contradicted** — `EntityAnchorCell` har ingen genesis, founder, seal, firstIdentity eller bootstrap. Søk på alle seks gir null treff. | `Sources/CellApple/Cells/EntityAnchorCell.swift` |
| Entitetsankeret håndhever eierskap | **contradicted** — kommentar i kilden der håndhevelsen burde vært: «This cell will only be accessed from it's owner so adding grants will not be necessary». Det er en antakelse om kallmønster, ikke en kontroll. | `EntityAnchorCell.swift:84` |
| `entityAuthority` er en rettighetsmodell | **contradicted** — den returnerer `authorityCommitStateValue()`, altså journaltilstanden for signerte mutasjoner. Den sier hva som er skjedd, ikke hvem som får gjøre noe. | `EntityAnchorCell.swift:142-148` |
| Lesing krever bevis i dag | **contradicted** — lokale flater lastes med oppstartsidentiteten uten biometrisk port; lesing er fri innenfor prosessen. | `ContentView.shouldLoadWithoutAuthenticatedRuntimeBootstrap` |
| Genesis utløses av et brukersteg | **contradicted av Kjetil 2026-09-15** — ankeret opprettes når entiteten *trenger å persistere* entitydata, ikke ved en egen velkomstseremoni. Første onboarding som samler data som må lagres, utløser det. | Kjetil, 2026-09-15 |
| Adressebok-import er en vanlig mutasjon | **contradicted** — import av adressebokdata for å invitere noen uten kjent HAVEN-representasjon *skal føre til opprettelse av entitydata*, altså er den en genesis-utløser. | Kjetil, 2026-09-15 |
| VC-bevis hører hjemme et annet sted | **contradicted** — VC-bevis skal i entitydata. `EntityAnchorCell` serverer allerede `proofs`. | Kjetil 2026-09-15; `EntityAnchorCell.swift` nøkkelliste |
| Betaling er i scope | **unavailable** — Palazzos egen PSP kommer «etterhvert» og avhenger av at `DiMyMint` og `DiMyMicropayments` hentes inn. Ingen av dem er i Binding eller CellProtocol i dag. | Kjetil, 2026-09-15 |
| Entiteten holder «midler» i dag | **unavailable** — ingen wallet-, verdi- eller mint-celle i Binding eller CellProtocol. `DiMyMint` og `DiMyMicropayments` er egne repoer utenfor denne appen. | søk over `Binding/`, `CellProtocol/Sources` |
| Alt på et scaffold tilhører én Entitet | **retrieved (uttalt)** — inntil Entiteten eventuelt gir tilgang til en annen Entitets Identitet. Å bytte owner til en annen Entitets identitet frarådes, unntatt midlertidige celler verten trenger (f.eks. scanner-invitasjon). | Kjetil, 2026-09-08 |

## 1. Formålstre

Rot for oppgaven er en eksisterende Book 23-node: **`purpose://self-determination.data`** — «The owner decides the purpose, extent, place, manner, recipients and duration of any use of their own and derived data, and can verify that the decision was honoured.» Intensjonen *er* den noden. Alt under klassifiseres på dens eksisterende barn.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://self-determination.data` | Data self-determination | `purpose://root` | Enhver bruk av eierens data skjer under en avtale eieren kan lese, endre og trekke tilbake, og etterlater etterprøvbart spor. | Alle bladene under er grønne. | active (Book 23) |
| `purpose://candidate.entitetsdata.genesis-seals-to-initiator` | **Første kjøring forsegler entiteten til den som startet den** | `purpose://self-determination.data.verifiability` | I det øyeblikket entiteten først trenger å persistere entitydata — for eksempel når en adressebok-import henter inn noen som skal inviteres — oppretter den sitt anker og fester grunnleggernøkkelen slik at ingen senere identitet kan bindes til entiteten uten grunnleggerens signatur. Genesis skjer én gang og kan verken kjøres på nytt, overskrives eller gjenskapes fra utsiden. Det entiteten sikrer — data nå, midler når de kommer — er dekket av samme forsegling. | `test.entitet.genesis-once`, `test.entitet.no-refounding` | candidate |
| `purpose://candidate.entitetsdata.read-requires-entity-proof` | Lesing krever bevis, ikke bare mutasjon | `purpose://self-determination.data.scope` | Både lesing og endring av entitetsdata krever at den som spør kan bevise at den er autentisert mot *denne* entiteten. Uten bevis: ingen data ut, ikke bare ingen data inn. | `test.entitet.read-without-proof-refused` | candidate |
| `purpose://candidate.entitetsdata.keypath-chat` | Chat som slår opp keypaths og endrer | `purpose://self-determination.data.exercisability` | Eieren kan spørre i klartekst hvor noe ligger, få keypath og nåværende verdi, og be om en endring — som går gjennom foreslå→signer som ethvert annet forslag. | `test.entitet.chat-keypath-lookup`, `test.entitet.chat-change-is-a-proposal` | candidate |
| `purpose://candidate.entitetsdata.general-editor` | Et enkelt og helt generelt redigeringsverktøy | `purpose://self-determination.data.exercisability` | Én flate som viser entitetsdataene som de er — keypath, verdi, opprinnelse — og lar eieren endre hva som helst av dem uten å kjenne cellenavn. Generell, ikke én flate per datatype. | `test.entitet.general-editor-covers-anchor` | candidate |
| `purpose://candidate.entitetsdata.file-into-entity` | En fil eieren slipper inn lander i egen entitet — og utløser genesis om nødvendig | `purpose://self-determination.data.exercisability` | Eieren kan slippe eller velge en fil på flaten, se hva som blir lagt inn før det skjer, og bekrefte — uten ekspertkunnskap og på under ett minutt. Er dette første gang entitetsdata må persisteres, opprettes og forsegles ankeret som del av samme handling, uten et eget steg eieren må forstå. | `test.entitet.file-roundtrip` | candidate |
| `purpose://candidate.entitetsdata.direct-edit` | Ren redigering uten AI | `purpose://self-determination.data.exercisability` | Eieren kan endre et felt i egne entitetsdata direkte fra flaten, uten at noen modell er involvert. | `test.entitet.direct-edit` | candidate |
| `purpose://candidate.entitetsdata.ai-proposes-owner-signs` | Modellen foreslår, eieren signerer | `purpose://self-determination.data.manner` | En modell kan produsere et *forslag* til mutasjon i eierens entitetsdata. Ingenting skrives før eierens nøkkel har signert forslaget. Modellen har talerett, aldri skriverett. | `test.entitet.unsigned-proposal-refused` | candidate |
| `purpose://candidate.entitetsdata.gateway-inside-entity` | Gatewayen bor i entiteten | `purpose://self-determination.data.locality` | `cell:///AIGateway` er registrert `identityUnique` i Binding og eid av eierens private identitet. Nøkler, prompt og logg ligger innenfor entiteten, uansett hvor modellen kjører. | `test.entitet.linked-identity-accepted` | command | En annen Identitet av *samme* Entitet, innenfor godkjent identityDomain og med gyldig lenkepost, får lese og skrive. | Negativ/positiv XCTest mot autorisasjonsveien. | `TESTRESULT.md#auth` |
| `test.entitet.foreign-entity-refused` | command | En Identitet uten lenke til eiende Entitet, en revokert lenke, og en lenke utenfor godkjent domene — alle avvist. | Negativ XCTest. | `TESTRESULT.md#auth` |
| `test.entitet.genesis-once` | command | Genesis kjører én gang; andre forsøk avvises og endrer ingenting. | Negativ XCTest mot EntityAnchor. | `TESTRESULT.md#genesis` |
| `test.entitet.no-refounding` | command | En identitet uten grunnleggersignatur kan ikke binde seg til entiteten, heller ikke ved å gjenskape ankeret. | Negativ XCTest. | `TESTRESULT.md#genesis` |
| `test.entitet.read-without-proof-refused` | command | Lesing av entitetsdata uten entitetsbevis avvises. | Negativ XCTest. | `TESTRESULT.md#auth` |
| `test.entitet.chat-keypath-lookup` | command | Klartekstspørsmål gir riktig keypath og verdi. | XCTest mot chat-cellen. | `TESTRESULT.md#chat` |
| `test.entitet.chat-change-is-a-proposal` | command | En endring bedt om i chat blir et forslag, ikke en skriving. | Negativ XCTest. | `TESTRESULT.md#chat` |
| `test.entitet.general-editor-covers-anchor` | inspection | Redigeringsflaten når hver nøkkel EntityAnchor serverer. | Sammenlign flatens keypaths mot ankerets nøkkelliste. | `ACCEPT.md#editor` |
| `test.entitet.gateway-owned` | candidate |
| `purpose://candidate.entitetsdata.trusted-model-declaration` | Tillit til en modell er en erklæring eieren gjør | `purpose://self-determination.data.recipients` | `trustedModels.<id>` under EntityAnchor: hvem modellen er, hvor den kjører, hva den får foreslå, når erklæringen ble gitt. Eiersignert, inspiserbar, revokerbar. Ingen modell utenfor registeret får foreslå noe. | `test.entitet.untrusted-model-refused` | candidate |
| `purpose://candidate.entitetsdata.authorization-resolves-entity` | Autorisasjonen kjenner entiteten, ikke bare identiteten | `purpose://self-determination.data.recipients` | En mutasjon slippes gjennom når den forespurte Identiteten er en representant for den *Entiteten* som eier cellen — bevist med en lenkepost Entiteten har signert, innenfor godkjent identityDomain — og avvises ellers. I dag finnes entitetsmodellen i dataene og ikke i tilgangskontrollen. | `test.entitet.linked-identity-accepted`, `test.entitet.foreign-entity-refused` | candidate |
| `purpose://candidate.entitetsdata.no-write-without-owner-proof` | Ingen andre kan endre mine entitetsdata | `purpose://self-determination.data.verifiability` | Feil identitet, usignert forslag, revokert modell, ukjent formål og direkte skriving utenom batch-veien blir alle avvist — bevist med negative tester, ikke med en policy-tekst. | `test.entitet.auth-negative` | candidate |
| `purpose://candidate.entitetsdata.change-leaves-a-trace` | Hver endring etterlater spor | `purpose://self-determination.data.verifiability` | Hver akseptert endring ligger i chronicle med hvem som signerte, hva som ble endret, og hvilken modell som eventuelt foreslo det. | `test.entitet.trace` | candidate |
| `purpose://candidate.entitetsdata.surface-offers-three-ways` | Flaten tilbyr faktisk de tre veiene | `purpose://skeleton.owner-entity-access` | Filopplasting, AI-forslag og direkte redigering er alle synlige og nåbare på flaten — ikke bare implementert. | `test.skeleton.purpose-actions-reachable` | candidate |

Nye noder er navngitt her, ikke av en modell (`lesson.decomposition-is-classification`). Seks av ni foreldre er eksisterende Book 23-noder.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en reparasjon av de sju døde seksjonene i Relasjoner-flaten. Den feilen er rapportert og har egen rød test; formål H *avhenger* av at den er løst, men løsningen hører ikke hjemme her.
- Ikke en rendererendring. Å la rot-scope-betingelser slå opp mot absorbert celletilstand er Kjetils avgjørelse og eget arbeid.
- Ikke modellhosting, inferens-infrastruktur eller valg av leverandør.
- Ikke korrespondanse, invitasjon eller relasjonssynk.
- Ikke sletting/varighet (`self-determination.data.duration`) — egen runde.
- **Ikke betaling.** Palazzos egen PSP kommer etterhvert og avhenger av at `DiMyMint` og `DiMyMicropayments` hentes inn. Forseglingen skrives så den dekker det entiteten holder, uansett hva det senere blir; selve verdihåndteringen designes ikke her, og skal gjennom `dimy-payment-regulatory-guardrails` før den designes.

| Kapabilitet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| Eierbevis ved oppslag | `CellResolver.validateIdentityUniqueOwner`, `GeneralCell.checkIdentityOrigin` | Dekker eierskap til *cellen*. Sier ingenting om hvem som foreslo innholdet. | Ja — `test.entitet.auth-negative` |
| Eiersignert batch-skriving | `EntityBatchPersistEnvelope`, `BindingPersonalChatChronicle.persist` | Idempotent på mutasjons-id. Dekker ikke forslag-før-signatur i dag. | Ja |
| `SkeletonFileUpload` med `supportsDrop` | `AttachmentSurface.swift:292` | Rendereren sender kortlivet payload; mål-cellen må validere type/størrelse selv. | Ja — for formål A |
| Flatereachability | `SkeletonReachabilityAudit` | Finner elementer som aldri kan sees. Sier ikke om handlingen gjør riktig ting. | Ja — for formål H |
| **Entiteten som eierenhet i autorisasjonen** | `IdentityLinkingModels.swift`; `EntityAnchorCell`; `GeneralCell.validateIdentityUniqueOwner` | **Åpent hull.** Modellen finnes i dataene, ikke i tilgangskontrollen. Uten den leser autorisasjonen en annen Identitet av samme Entitet som en fremmed — derfor kan «umulig for andre» i dag også bety «umulig for meg selv fra en annen identitet». | Ja — `test.entitet.linked-identity-accepted` |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Genesis: entiteten forsegles til den som startet den | bilde | `images/` | `entitet-forsegling-v1.png` | G1-GUI |
| Vei inn A1: filimport, tom tilstand med slipp-sone | bilde | `images/` | `import-tom-v1.png` | G1-GUI |
| Vei inn A2: filimport, forhåndsbilde før signatur | bilde | `images/` | `import-forhandsbilde-v1.png` | G1-GUI |
| Vei inn B: generell entitetsdata-editor | bilde | `images/` | `entitetsdata-editor-v1.png` | G1-GUI |
| Vei inn C1: modellforslag som venter på eiersignatur | bilde | `images/` | `forslag-venter-signatur-v1.png` | G1-GUI |
| Vei inn C2: keypath-chat som slår opp og foreslår | bilde | `images/` | `keypath-chat-v1.png` | G1-GUI |
| Hva skjelettet *ikke* kan rendre av bildene | fil | `images/README.md` | — | G1-GUI |
| `cell:///AIGateway` registrert i Binding, med kontrakt-JSON | fil | `contract/aigateway_contract_v1.json` | — | nei |
| `trustedModels`-skjema + validator med positive/negative fixtures | fil | `contract/trustedmodels_v1.json` | — | nei |
| Negative autorisasjonstester som viser at andre ikke slipper til | testutdata | `TESTRESULT.md#auth` | — | nei |
| Kjørende flate der du slipper inn `HAVEN_import_bokprosjekt.xlsx` og bekrefter | kjørende flate | Binding, Relasjoner | — | nei |
| Reachability grønn for flaten | testutdata | `TESTRESULT.md#reachability` | — | nei |
| Chronicle-spor per endring, med signatur og eventuell modell | testutdata | `TESTRESULT.md#trace` | — | nei |

## 5. Avledede tester

| testRef | Type | Beskrivelse | Hvordan | Bevis |
|---|---|---|---|---|
| `test.entitet.file-roundtrip` | command | Fil inn via `FileUpload` → forhåndsbilde → bekreft → data i entiteten. | XCTest gjennom cellene, som `BookProjectImportEndToEndTests`. | `TESTRESULT.md#file` |
| `test.entitet.direct-edit` | command | Endring av ett felt uten modell involvert. | XCTest. | `TESTRESULT.md#edit` |
| `test.entitet.unsigned-proposal-refused` | command | Et forslag uten eiersignatur skriver ingenting. | Negativ XCTest mot AIGateway + EntityAnchor. | `TESTRESULT.md#auth` |
| `test.entitet.untrusted-model-refused` | command | Modell utenfor `trustedModels`, og revokert modell, avvises begge. | Negativ XCTest. | `TESTRESULT.md#auth` |
| `test.entitet.gateway-owned` | inspection | `AIGateway` er `identityUnique`, eid av privat identitet, og nøkler ligger ikke utenfor entiteten. | Registreringssjekk + kildeinspeksjon. | `ACCEPT.md#gateway` |
| `test.entitet.auth-negative` | command | Feil requester, feil keypath, `purpose://prompt.unknown`, direkte skriving utenom batch — alle avvist. | `pkg.std.cell-contract`. | `TESTRESULT.md#auth` |
| `test.entitet.trace` | command | Hver akseptert endring finnes i chronicle med signatur og modellreferanse. | XCTest. | `TESTRESULT.md#trace` |
| `test.skeleton.purpose-actions-reachable` | inspection | De tre veiene inn finnes i `reachableActionKeypaths`. | `SkeletonReachabilityAudit`. | `ACCEPT.md#ways-in` |
| `test.skeleton.no-unreachable-elements` | command | Ingen flate skjuler egne veier inn. | `testNoLocalSurfaceHidesItsOwnWaysIn`. | `TESTRESULT.md#reachability` |
| `test.build`, `test.regression` | command | `pkg.std.everything-works`. | xcodebuild + swift test. | `TESTRESULT.md#build` |

## 6. Åpne spørsmål (endrer treet)

**Avklart 2026-09-08 (Kjetil):** Entiteten er eierenheten — det brukeren kontrollerer og har tilgang til i HAVEN. Identiteter er i utgangspunktet anonyme representanter for Entiteten, uten antallsbegrensning, knyttet til identityDomains. Oppstartsidentiteten og Face ID-identiteten er derfor *ikke* to personer; de er to representanter for samme Entitet, og at autorisasjonen ikke ser det er en implementasjonsfeil, ikke en modellvalg. Alt på et scaffold tilhører én Entitet inntil Entiteten gir en annen Entitets Identitet tilgang; å bytte owner til en annen Entitets identitet frarådes, unntatt midlertidige celler verten trenger (scanner-invitasjon).

**Avklart 2026-09-15 (Kjetil, sammen med G1):** Ankeret opprettes i det øyeblikket entiteten trenger å persistere entitydata. Adressebok-import for å invitere noen uten kjent HAVEN-representasjon er en slik hendelse. Dermed faller §6.1 og §6.2 fra iterasjon 3 bort: importen og genesis er *samme flyt*, ikke to runder i rekkefølge. Spørsmålet om å levere importen «først under den gamle regelen» kan ikke stilles, fordi importen er det som skaper entitetsdataene.

Fortsatt åpent:

1. **«Midler» og forseglingen.** Forseglingen skrives så den dekker det entiteten holder. Men verdihåndtering kommer med Palazzos PSP, `DiMyMint` og `DiMyMicropayments`, og treffer da e-penger, forvaring og MiCA/PSD2. Den delen designes ikke i denne runden, og skal gjennom `dimy-payment-regulatory-guardrails` før den designes — ikke etterpå.
2. **Skal flere Identiteter kunne dele samme identityDomain?** Kjetil: antagelig ja, men det bør deklareres dersom det *ikke* er greit. `approvedDomains` på lenkeposten bærer avgjørelsen.
3. **Ikke-representasjonsbevis** — forskning, utenfor denne runden, registrert for å ikke bli borte.

## 7. Iterasjoner

| # | Dato | Hva endret seg |
|---|---|---|
| 4 | 2026-09-15 | **G1 godkjent.** Fire klargjøringer fra Kjetil: genesis utløses av første behov for å persistere entitydata, ikke av et eget steg; adressebok-import er en slik utløser; VC-bevis hører i entitydata; betaling venter på DiMyMint og DiMyMicropayments og ligger utenfor runden. §6.1 og §6.2 bortfaller — importen og genesis er samme flyt. Neste port: G1-GUI. |
| 3 | 2026-09-08 | Filimporten inn, men kravet hevet: både lesing og mutasjon krever bevis for autentisering mot egen Entitet. Fire nye formål — genesis-forsegling (uttalt som viktigst av alt), lesebevis, keypath-chat, generelt redigeringsverktøy. Seks nye tester. Funn: EntityAnchorCell har ingen genesis/forsegling, og håndhever ikke eierskap — den antar det i en kommentar. Anbefaling om å dele i to runder ligger i §6. |
| 2 | 2026-09-08 | Kjetil rettet grunnpremisset: Entiteten er eierenheten, Identiteter er anonyme representanter knyttet til identityDomains. Nytt formål `authorization-resolves-entity` med to tester; §0 og §2 rettet; §6 sitter igjen med tre åpne punkter, ett ubesvart. |
| 1 | 2026-09-08 | Første dekomponering. Tre valg tatt av Kjetil før skriving (AI-autoritet, gateway-plassering, tillitsregister). Ni formål, seks under eksisterende Book 23-noder. To åpne spørsmål i §6. |

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
- purpose://digital-work.collect-structured-input [active] — Collect structured input
- purpose://questionnaire.campaign.complete [active] — Complete questionnaire campaign
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance
- purpose://questionnaire.access.audit [active] — Questionnaire access audit
- purpose://test.acceptance.questionnaire [active] — Questionnaire acceptance tests
- purpose://knowledge.explain-policy [draft] — Explain policy or rules
- purpose://self-determination.data.manner [candidate] — Manner of processing and derived data

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
| 0 | 2026-09-08 | Opprettet | Losen |
