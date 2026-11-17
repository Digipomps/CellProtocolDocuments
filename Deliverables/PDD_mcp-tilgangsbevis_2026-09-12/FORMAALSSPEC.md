# Formålsspesifikasjon — MCP-initiert tilgangsbevis

Oppgavemappe: `PDD_mcp-tilgangsbevis_2026-09-12` · Opprettet 2026-09-12 · Iterasjon 6 · **G1 godkjent 2026-09-12** med vilkår: riktig formålsarkitektur (PerspectiveNode) — se `PERSPECTIVENODE_KONSEKVENS.md`

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

---

## 0. Intensjon (ordrett) og brief-audit

### 0.1 Kjetils tekst, uendret

**(a) 2026-09-11, da oppgaven ble reist:**

> Jeg vil også at du vurderer å bruke det at mcp'en kan be agenten om å få tilganger slik at jeg kan bruke min identitet for å få tilgang i min entitet, men begrenset med grants i en celle jeg eier i agenten som bestemmer hva mcp'en får lov til å gjøre (er jo tross alt potensielt) Dette gjør det mulig å fra innenfor min entitet utstede bevis som du eller codex kan bruke som adgangsbevis inn i celler som jeg eier for å teste ny funksjonalitet. Slik at jeg ikke trenger å logge inn i Chrome så du kan teste i web-flaten. Med en slik funksjonalitet har vi to nåver vi kan teste på.

**(b) 2026-09-12, bestillingen av denne dekomponeringen:**

> Ok - gi meg en grundig formålsdekomponering. Legg inn at vi må ha en periodisk sjekk for om tilgangene har sklidd for mye. Her kan vi vurdere å ha beskrivelsen av baseline i en alltid tilgjengelig HAVEN celle. Det er alltid brukerens valg, men det er lov å komme med råd om hva som er en god ide - så lenge det foreligger gode argumenter for det.

**(c) 2026-09-12, G1-svaret med korreksjoner:**

> "…men de grantene ligger ikke i en celle Kjetil eier. De ligger i agentens konfigurasjonsfil" - det må de gjøre for å bruke cellprotocol riktig.  "Autorisasjonen i scaffold-cellene respekterer keypath, ikke bare eierskap" - dette er i tilfelle en feil. Man bruker en keypath som datareferanse. Referansen kan ikke ha autoritet i seg selv. Forespørselen kan bli avvist eller komme med en Agreement challenge for hvert steg hvor det blir spurt om tilgang. Aka når keypathen traverserer mellom celler. (Og bare for å si ifra - da må brukeren ha verktøy for å løse dette - som en notifikasjon i varslingssenteret hvor brukeren enten direkte får oppfylt et vilkår, eller åpner et verktøy for det) Du må - men hjelp av Codex og eventuelt rådgivere sjekke om vi bruker riktig formålsstrukturer - som er PerspectiveNode og gå igjennom all bruk av og dokumentasjon av formålsdekomponering og sjekke hvilke knsekvenser det vil ha å flytte det over og mitigere eventuelle negative konsekvenser. Har sett igjennom G1 og synes dette er bra så gå videre med det men gjør det med riktig formålsarkitektur. baselinen skal ikke ligge i samme celle som grantene.

**(d) 2026-09-17, om hvor grensene faktisk går:**

> Men vil presisere at det ikke er min grense. Det er grenser satt av deg fordi du ikke får gjort det. Jeg har foreslått veier rundt men vi får stadig regresjon - begrensninger i sandbox kan vi lage veier rundt med å flytte funksjonalitet over på agenten her lokalt eller på verten hvor vi startet å lage måter å kjøre kommandoer på fra prosesser på verten som har nok tilgang.

**(e) 2026-09-17, utførelsesveien og formål som grensesnitt:**

> Dette skal gå igjennom HAVENAgentD på laptopen min. Det skal det også være funksjonalitet for å overvåke en folder slik at fil-hendelser kan mottas og håndteres. Den kjører som min bruker på laptopen og har tilgang til .ssh hvor hetzner sertifikatet ligger. Prosesser som skal bruke dette trenger ikke å vite noe om hvordan agenten gjør dette men skal vite hvilke formål agenten kan løse (og notere seg for om agenten løser formålet på en hensiktmessig måte). Formål er en myk beskrivelse av hva man ka gjøre. Grants i Agreement er en hard grense. Bruk av formål kan gjøre at vi ikke trenger å gi tilgang til hver enkelt kommando - for eksempel git kommandoer eller andre terminalkommandoer. Som en del av formålsdefinisjonen kan det være at dette formålet skal bare lese - innenfor ett eller annet skope eller dette formålet krever skriving eller utføring. Det vil  kreve forskjellige godkjenninger. Husk alltid at vi må ha generelle perspektiver på slik funksjonalitet.

### 0.1.1 Avledede krav fra (d) og (e) — iterasjon 6

Disse er utledet, ikke sitert. De er skrevet ned her for å måles mot, og flere av
dem treffer utenfor treet slik det ble godkjent 2026-09-12. **Ingen av dem er
lagt inn i §1 ennå.** Utvidelse av et godkjent tre krever Kjetils ord (§6 Q9).

| # | Krav | Treffer | Status |
|---|---|---|---|
| K-A1 | Utførelsesveien er HAVENAgentD på Kjetils laptop, som kjører som hans bruker og har `~/.ssh` med Hetzner-sertifikatet. Ikke skykontaineren, som verken har nøkkel eller nettverksrute (målt 2026-09-17: `ssh` og `scp` finnes i enhets-VM-en, men port 22 mot 89.167.90.101 er «Network is unreachable», og `~/.ssh` finnes ikke der) | Ny forutsetning, ikke i §2 | åpen |
| K-A2 | Agenten skal kunne overvåke en katalog og motta og håndtere fil-hendelser som utløser | Delvis dekket: `Docs/DeviceActionRelay.md` har `Inbox/Requests` med `Processed`/`Failed`/`Replies`, men lager i dag **godkjenningstickets til telefonen** — den utfører ingenting lokalt | gap |
| K-A3 | Kallende prosess skal ikke vite **hvordan** agenten løser noe, bare **hvilke formål** agenten kan løse. Formålskatalogen er grensesnittet | Nytt. `NetworkHealthPurposeCatalog.swift` finnes som mønster for ett domene; en generell katalog gjør det ikke | gap |
| K-A4 | Kallende prosess skal kunne **notere seg om agenten løste formålet på en hensiktsmessig måte**. Altså en tilbakemeldingskanal om formålsoppfyllelse, ikke bare om exit-kode | Nytt. Sikkerhetsloggen registrerer i dag bare avslag (Astra, 2026-09-14) | gap |
| K-A5 | **Formål er en myk beskrivelse. Grants i Agreement er den harde grensen.** De to må aldri forveksles: et formål åpner ingenting av seg selv | Presiserer B3 og D5. Konsistent med at et agentutstedt bevis aldri regnes som `ownerProof` (Q8) | dekket, men skal stå ordrett |
| K-A6 | Formål skal gjøre at vi **slipper å gi tilgang per kommando** — ikke én grant per git-kommando eller terminalkommando | Nytt. `TrustedRemoteIntentIssuer` har i dag `allowedActionIDs`, altså nettopp per-handling-lister | gap, og en retning bort fra dagens form |
| K-A7 | Formålsdefinisjonen skal bære en **modus**: bare lese innenfor et skop, eller skrive, eller utføre. Ulik modus krever ulik godkjenning | Nytt. Nærmeste eksisterende er `rw-s`-grants i CellProtocol; koblingen formål → modus → godkjenningsnivå finnes ikke | gap |
| K-A8 | Funksjonaliteten skal ha **generelle perspektiver** — ikke en løsning for denne ene oppgaven | Metodekrav som gjelder hele §1 | står |

**Konsekvens.** K-A2, K-A3, K-A4, K-A6 og K-A7 er gap mot dagens kode, ikke
konfigurasjon. K-A1 er grunnen til at ingenting av dette kan bæres av
skykontaineren. Og alt sammen står bak **D7**: en ny agent-binær drepes i dag av
macOS (`SIGKILL (Code Signature Invalid)` / Launch Constraint Violation), så ny
agentkode kan ikke testes på maskinen. D7 har ligget hos Codex siden
2026-09-11. Så lenge D7 er rød, leverer «legg det i agenten» ingenting
kjørbart — og det er den faktiske kilden til regresjonen (d) beskriver.

### 0.2 Brief-audit {#audit}

Én rad per faktapåstand og per kapabilitet intensjonen forutsetter. Bare `retrieved` kan bære planen.

| # | Påstand i intensjonen / antatt kapabilitet | Audit | Kilde (lest denne økten) |
|---|---|---|---|
| A1 | «mcp'en kan be agenten om å få tilganger» — det finnes en MCP-flate mot agenten med verktøy som ber agenten gjøre noe på Kjetils vegne | **retrieved** | `HavenAgentD::Sources/HavenAgentDMCP/HavenAgentMCPService.swift` — verktøyene `agent.identity.sign_statement` (l. 210, impl. l. 960), `agent.operator.request` (l. 213), `agent.operator.request_and_wait` (l. 219) |
| A2 | Agenten kan utstede et signert, mottaker- og tidsbundet utsagn med et formål | **retrieved** | `HavenAgentD::Sources/HavenAgentRuntime/AgentSignatureStatement.swift` — `AgentSignStatementRequest{purposeRef, audience, expiresAt, nonce, payloadSHA256Base64URL…}`, `maxValiditySeconds = 86_400`, `minNonceLength = 16` |
| A3 | «min identitet» er noe agenten kjenner og kan bevise — det finnes et begrep om «den parrede operatøren» | **retrieved** | `HavenAgentD::Sources/HavenAgentCells/LocalControlCellAccess.swift` — `isPairedOperator(_:)` sammenligner requesterens `publicSecureKey.compressedKey` med `pairedOperatorSnapshot().operatorPublicKeyBase64URL` |
| A4 | «grants … som bestemmer hva mcp'en får lov til å gjøre» — huset har allerede en grant-form av denne typen | **retrieved** | `HavenAgentD::Sources/HavenAgentRuntime/RemoteIntentVerifier.swift` — `TrustedRemoteIntentIssuer{issuerID, publicSigningKeyBase64, allowedTopics, allowedActionIDs}`, `RemoteIntentPolicy{issuers, requireExpiry, maxClockSkewSeconds, maxArgumentCount}` |
| A5 | …men de grantene ligger **ikke** i en celle Kjetil eier. De ligger i agentens konfigurasjonsfil | **retrieved** (dette er gapet) — **bekreftet av Kjetil 2026-09-12:** «det må de gjøre for å bruke cellprotocol riktig» | `HavenAgentD::Sources/HavenAgentRuntime/AgentConfig.swift:422` `public var remoteIntentPolicy`, dekodes l. 467, default-issuers settes i kode l. 611–612 |
| A6 | «en celle jeg eier i agenten» — agenten er en celleholder, og cellene har eier-/requester-basert autorisasjon | **retrieved** | `HavenAgentD::Sources/HavenAgentCells/` — 14 celler (`AgentIdentityCell`, `AgentSignatureCell`, `SecretCredentialCell`, `RemoteIntentReviewCell` …) + `LocalControlCellAccess.swift` som gate |
| A7 | Kontrollflaten mot agenten er loopback-bundet og token-gated (ikke åpen) | **retrieved** | `HavenAgentD::Sources/HavenAgentCellRuntime/AgentControlBridgeServer.swift:23–25` (token fra query, ellers `Abort(.unauthorized)`), l. 166 + 192 (`loopbackOnly`) |
| A8 | Entitetsutvidelse krever bevis for å eie begge entiteter | **retrieved** | `HavenAgentD::Sources/HavenAgentRuntime/AgentEntityLinkContract.swift` — `verifyMutualSignatures()` krever `requiredKeys = [pubkey_a, pubkey_b]`; `verifySignature(_:canonical:)` |
| A9 | «adgangsbevis inn i celler som jeg eier» — et signert utsagn brukes i dag som **adgang** et sted | **contradicted** | `AgentSignatureStatement.purposeRef = "personal.identity.sign.statement"`, `purposeRefs` = tre *utsagns*-formål. Ingen konsument leser et signert utsagn som adgang. Beviset finnes som *representasjon*; adgangsveien finnes ikke |
| A10 | Web-flaten kan slippe inn en ikke-interaktiv kaller (bevis i stedet for Chrome-innlogging) | **unavailable** | `CellScaffold`/`PalazzoScaffold` er ikke montert i denne økten. Rekognosering bestilt hos Codex; resultatet hører i §2 som egen avhengighet med verifier, ikke som antakelse |
| A11 | ~~Autorisasjonen i scaffold-cellene respekterer keypath, ikke bare eierskap~~ **Omformulert etter Kjetils korreksjon 2026-09-12:** en keypath er en *datareferanse* uten egen autoritet. Tilgang avgjøres av **hver celle** når keypathen traverserer inn i den — tillat, avvis, eller reis en Agreement challenge | **contradicted** (kjent hull, riktig beskrevet nå) | `lesson.cellscaffold-two-holes` (2026-09-01, blocker): «autorisasjon som kaster nøkkelstien og bare sjekker eierskap». Hullet er at cellen ikke *tar en avgjørelse ved inngang*, bare sjekker eier. Et bevis som sier «jeg er Kjetil» får da *alt*. Rettingen er avgjørelse ved traversering — **ikke** keypath som autoritet |
| A12 | «to nøkler vi kan teste på» forutsetter at de to er til å skille fra hverandre i ettertid | **unavailable** | Ingen kilde lest som viser at en handling kan attribueres til en utstedt nøkkel framfor til Kjetil selv. Blir eget formål (§1, gren 4) |
| A13 | «en alltid tilgjengelig HAVEN celle» finnes som begrep jeg kan peke på | **recalled** | Ikke verifisert denne økten. Behandles som åpent spørsmål (§6 Q2), ikke som bærende antakelse |
| A14 | En ny agent-binær kan i dag startes på maskinen | **contradicted** | Ny binær drepes av macOS: `SIGKILL (Code Signature Invalid)` / `CODESIGNING / Launch Constraint Violation`. Overlevert Codex: `HavenAgentD::Docs/Handoff_Agentbinaer_Launch_Constraint_20260911.md`. **Blokkerer all testing av ny agentkode** → §2 |
| A15 | Book 23 har en aktiv node som dekker nettopp «tilgang etter eksplisitte grants, med etterprøvbart spor» | **retrieved** | `CellProtocolDocuments::Book/haven_purpose_knowledge_base_v0.json` (57 noder) — `purpose://access.audit.privacy`, forelder `purpose://governance`, status `active`. Outcome ordrett: «Reads, writes, shares, and exports follow explicit grants and leave reviewable evidence.» Suksessignaler: «Resolver denies missing grants», «Sensitive action plans identify risk level and confirmation needs», «Audit/feed entries explain successful mutations.» Verifier: «Resolver policy tests and flow/audit assertions» |
| A16 | `lookup`-forslagene `skeleton.owner-entity-access` og `questionnaire.access.audit` er **ikke** riktige foreldre | **retrieved** | Samme fil: `skeleton.owner-entity-access` har forelder `gui.quality.functional-accessible` og handler om at et skeleton ikke låser eieren ute av sin egen entitet; `questionnaire.access.audit` er barn av `access.audit.privacy` og gjelder spørreskjema. Begge opptrer ellers som **facetRefs**, ikke som foreldre. Leksikalsk treff, ikke semantisk |
| A17 | Book 23 har en hel gren som svarer på dette: `purpose://self-determination.data` med åtte barn | **retrieved** | Samme fil: `.use-purpose` (Purpose binding for data use), `.scope` (Extent of data made available), `.recipients` (**Recipients and delegation**), `.duration` (Duration, withdrawal and deletion), `.verifiability` (Verifiability instead of trust), `.exercisability` (Control that can actually be exercised), `.locality`, `.manner` — alle status `candidate`. Grenene i §1 er klassifisert mot disse |
| A18 | `purpose://prompt.unknown` finnes som node og feiler lukket | **retrieved** | Samme fil: `purpose://prompt.unknown`, forelder `purpose://root`, status `active`. Testene i §5 som bruker den er dermed jordet |

**Konsekvens av auditen for treet:** A9 og A12 er grunnen til at dette er et *nytt* formål og ikke en konfigurasjonsendring. A11 og A14 er grunnen til at §2 har to blokkerende avhengigheter. A13 er grunnen til at ett spørsmål i §6 må besvares før treet er endelig. A15–A18 gjør §1 til **klassifisering** framfor oppfinnelse: roten henger under en aktiv node, og fem av fem grener henger under eksisterende `self-determination.data`-noder. Bare bladene er nye.

---

## 1. Formålstre

Rot, fem grener, tre antiformål. Dybde 3. `candidate`-noder er navngitt her, ikke av en modell.

**Klassifisering først (A15–A17).** Roten henger under en *aktiv* Book 23-node, og hver gren henger under en eksisterende node i `purpose://self-determination.data`-grenen. Bare bladene er nye `candidate`-noder. Kartet:

| Gren | Forelder i Book 23 | Hvorfor den passer |
|---|---|---|
| 1 Myndigheten er en celle | `purpose://self-determination.data.scope` — «Extent of data made available» | Grantene *er* omfanget: hvilke keypather og operasjoner som er gjort tilgjengelige |
| 2 Utstedelse innenfor grants | `purpose://self-determination.data.use-purpose` — «Purpose binding for data use» + `.duration` | Beviset er formålsbundet og tidsbundet; det er nøyaktig disse to nodene |
| 3 Konsumenten slipper ikke inn mer | `purpose://self-determination.data.recipients` — «Recipients and delegation» | Claude og Codex er mottakere av en delegert, snever nøkkel |
| 4 To nøkler til å skille | `purpose://self-determination.data.verifiability` — «Verifiability instead of trust» | Attribusjon i revisjonsloggen er etterprøvbarhet, ikke tillit |
| 5 Avdrift mot baseline | `purpose://self-determination.data.exercisability` — «Control that can actually be exercised» + `purpose://preference.owner-controlled` | En kontroll du ikke får utøvd i praksis er ingen kontroll; avdriftssjekken er det som gjør innsnevring utøvbar |

De åtte `self-determination.data`-nodene har status `candidate` i Book 23. Det betyr at denne PDD-en, hvis den lander, er den første som gir dem derivedTests — og i P6 er det et argument for å fremme dem (Book 23 §8, med ditt ord).

### 1.0 Rot

| purposeRef | Tittel | Forelder | Goal (outcome) | Suksessignaler | Verifier | Status |
|---|---|---|---|---|---|---|
| `purpose://candidate.mcp-tilgangsbevis.root` | Låne ut en snever nøkkel til sin egen entitet — og se hva den gjorde | `purpose://access.audit.privacy` (**verifisert**, active — outcome: «Reads, writes, shares, and exports follow explicit grants and leave reviewable evidence») | Kjetil kan la agenten utstede et kortlevd bevis som Claude eller Codex bruker til å komme inn i celler han eier, uten at han logger inn i Chrome, og uten at beviset kan gjøre mer enn han har skrevet ned i en celle han eier | (1) En testkjøring i web-flaten fullføres uten Chrome-sesjon. (2) Fem nektelser (feil keypath, feil operasjon, utløpt, gammel grant-digest, ukjent formål) er røde i revisjonsloggen og grønne som tester. (3) Han kan se hva nøkkelen gjorde, skilt fra hva han selv gjorde | Terminal-transkript + skjermbilde av flate nådd uten sesjon + revisjonslogg-utdrag | candidate |

### 1.1 Gren 1 — Myndigheten er en celle han eier

Forelder: `purpose://self-determination.data.scope`

| purposeRef | Tittel | Goal (outcome) | Suksessignaler | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.mcp-tilgangsbevis.grant-authority-is-a-cell` | Grantene bor i en celle, ikke i en konfigurasjonsfil | Det finnes én celle i agenten, eid av Kjetils entitet, som er den eneste kilden til hva et bevis får lov til. Agentens config er ikke lenger myndighet for dette | Agenten nekter å utstede når cellen ikke kan leses | Kontraktfixtures + negativ test | candidate |
| `purpose://candidate.mcp-tilgangsbevis.grant-cell-is-owned` | **Blad.** Cellen er Kjetils, og ingen annen får lese den | Lesing av grant-cellen fra en annen requester enn parret operatør avvises med `deniedNoGrant`, ikke med tom liste | Tre negative tester: feil requester, feil keypath, `purpose://prompt.unknown` | `test.grant.auth-negative` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.grant-change-requires-kjetil` | **Blad.** Bare Kjetil selv kan utvide et grant | En skriving mot grant-cellen som presenterer et agentutstedt bevis avvises, uansett hva beviset ellers tillater. Bare den parrede operatørens egen nøkkel kan utvide | Negativ test: bevis forsøker å utvide sitt eget grant → nektet | `test.grant.proof-cannot-widen-itself` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.grants-are-keypath-and-operation` | **Blad.** Et grant er (celle, keypath, operasjon, tidstak) — ikke en rolle og ikke fritekst | Kontrakten avviser et grant uten keypath, uten operasjon eller uten tidstak. Ingen grant-form kan uttrykke «alt» | Schema-fixtures: 3 positive, 5 negative | `test.grant.contract-fixtures` | candidate |

### 1.2 Gren 2 — Utstedelse skjer bare innenfor de levende grantene

Forelder: `purpose://self-determination.data.use-purpose`, med `…proof-expiry-is-short` også under `purpose://self-determination.data.duration`

| purposeRef | Tittel | Goal (outcome) | Suksessignaler | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.mcp-tilgangsbevis.issuance-within-grants` | Beviset kan aldri være videre enn cellen sa i utstedelsesøyeblikket | Hvert bevis er en delmengde av det levende grant-settet, lest ved utstedelse | Se blader | — | candidate |
| `purpose://candidate.mcp-tilgangsbevis.issuance-reads-live-cell` | **Blad.** Utstedelsen leser cellen, ikke en kopi og ikke MCP-argumentet | Etter at et grant er innsnevret, nekter neste utstedelse den innsnevrede retten — uten omstart av agenten | Snevre inn, be om bevis, få nektelse; så utvide og få bevis | `test.issue.reads-live-grants` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.proof-binds-grant-digest` | **Blad.** Beviset bærer digesten av grant-settet det ble utstedt under | Digesten kan regnes om fra cellen og sammenlignes med det som står **i beviset selv** (bytene, ikke feltnavnet) | Dekod beviset, regn `sha256` over kanonisk grant-sett, sammenlign | `test.issue.digest-on-artifact` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.proof-expiry-is-short` | **Blad.** Et testbevis lever i minutter, ikke i et døgn | `expiresAt − issuedAt ≤ tidstaket i grantet`, og taket er ≤ 15 min med mindre Kjetil har satt noe annet. `maxValiditySeconds = 86_400` er et tak for utsagn, ikke for adgang | Måling på utstedt artefakt, tre utstedelser | `test.issue.expiry-ceiling` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.issuance-is-visible` | **Blad.** Kjetil ser at en nøkkel ble lånt ut, der han allerede ser etter | Hver utstedelse gir en rad der han ser: hva som ble gitt, til hvem, hvor lenge, og hvor han kan trekke den tilbake | Utsted, se raden i utfordringsinnboksen/menylinjen | `test.issue.visible-to-kjetil` | candidate |

### 1.3 Gren 3 — Konsumenten slipper ikke inn mer enn beviset sier

Forelder: `purpose://self-determination.data.recipients`

| purposeRef | Tittel | Goal (outcome) | Suksessignaler | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.mcp-tilgangsbevis.consumer-honours-the-proof` | Adgangen er like snever hos mottakeren som hos utstederen | Et gyldig bevis kommer inn på nøyaktig de granta keypathene og ingen andre | Se blader | — | candidate |
| `purpose://candidate.mcp-tilgangsbevis.each-cell-decides-at-traversal` | **Blad.** Cellen avgjør ved inngang; eierskap alene er ikke adgang | Når en keypath traverserer inn i en celle Kjetil eier, tar **den cellen** avgjørelsen: tillat, avvis, eller Agreement challenge. Et bevis er evidens cellen ser ved inngangen — ikke et adgangskort som sjekkes sentralt, og keypathen bærer ingen autoritet selv. Feil datareferanse og feil operasjon avvises selv når beviset er utstedt for riktig eier. (Dette er `lesson.cellscaffold-two-holes` gjort til en test, riktig formulert) | Tre negative tester i cellens egen inngangsavgjørelse | `test.consume.auth-negative` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.challenge-is-resolvable-from-notification` | **Blad.** Brukeren har verktøy for å løse en Agreement challenge | Når en celle reiser en Agreement challenge ved traversering, får Kjetil en notifikasjon i varslingssenteret der han **enten oppfyller vilkåret direkte** i varselet **eller åpner verktøyet** for det. En challenge uten vei til handling er en blindgate. (Kjetils krav 2026-09-12. Arkitektur, presisert av Astra: mekanismen som finnes er `AdmissionChallengePayload` + `connect.challenge` + `retryAdmissionSession` i *tilkoblings*forløpet, `CellProtocol/Sources/CellBase/Agreement/AdmissionContracts.swift:47`, `GeneralCell.swift:542, :660, :977, :569`; for et avvist *steg* må koblingen bygges — M13 i konsekvensanalysen. `GoalDefinition.helperCells` er en peker, ikke mekanismen) | Så en traversering som krever et grant han ikke har gitt → varsel → svar i varselet → traverseringen fullføres | `test.consume.challenge-resolvable` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.consumer-checks-expiry-and-digest` | **Blad.** Utløpt bevis og gammel grant-digest avvises | Et bevis utstedt under et grant-sett som siden er endret, avvises — det er dette som hindrer at adgang «sklir» | To negative tester | `test.consume.stale-proof-denied` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.web-surface-without-chrome-login` | **Blad.** Flaten nås med beviset alene | Web-flaten svarer på en forespørsel som bare bærer beviset, fra en klient uten sesjonscookie, og Kjetil trenger ikke logge inn for at noe skal kunne testes | Kjøring mot flaten fra ren klient + skjermbilde. **Avhenger av §2 D5/D6** | `test.consume.web-no-session` | candidate |

### 1.4 Gren 4 — De to nøklene er til å skille fra hverandre

Forelder: `purpose://self-determination.data.verifiability`

| purposeRef | Tittel | Goal (outcome) | Suksessignaler | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.mcp-tilgangsbevis.two-keys-distinguishable` | «To nøkler» er bare verdt noe hvis du etterpå vet hvilken som gjorde hva | Hver handling utført med et bevis er attribuert til beviset, ikke til Kjetil | Se blader | — | candidate |
| `purpose://candidate.mcp-tilgangsbevis.audit-names-the-proof` | **Blad.** Revisjonsloggen navngir beviset | Hver innslipp logger bevis-id, grant-digest og formål, og er i loggen forskjellig fra Kjetils egne handlinger | Les revisjonsraden etter en testhandling | `test.audit.names-the-proof` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.revocation-is-one-act` | **Blad.** Én handling dreper alle utestående bevis | Etter tilbaketrekking avvises alle tidligere utstedte bevis, og Kjetil ser at det tok | Utsted to, trekk tilbake, begge nektes | `test.revoke.kills-all` | candidate |

### 1.5 Gren 5 — Avdrift oppdages mot en erklært baseline

Forelder: `purpose://self-determination.data.exercisability`; `…drift-check-proposes-never-acts` også under `purpose://preference.owner-controlled`

| purposeRef | Tittel | Goal (outcome) | Suksessignaler | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.mcp-tilgangsbevis.drift-is-detected` | Tilgangene kan ikke skli uten at noen sier det | En periodisk sjekk sammenligner levende grants med en erklært baseline og rapporterer forskjellen | Se blader | — | candidate |
| `purpose://candidate.mcp-tilgangsbevis.baseline-is-declared-and-readable` | **Blad.** Baselinen er erklært, og lesbar når som helst | Beskrivelsen av hva grant-settet *skal* være ligger i en HAVEN-celle som kan leses uavhengig av om agenten kjører | Les baselinen med agenten stoppet | `test.drift.baseline-readable-agent-down` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.drift-check-runs-unasked` | **Blad.** Sjekken går av seg selv | Sjekken kjører etter en tidsplan; forrige kjøring er synlig med tidsstempel, og «ikke kjørt siden X» er i seg selv et funn | To påfølgende kjøringer med tidsstempel | `test.drift.runs-on-schedule` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.drift-report-is-per-source` | **Blad.** Én rad per kjent kilde, med tilstand | Hver kilde har tilstand `read` / `unreadable` / `not-configured` og en påkrevd grunn når den ikke er lest. `claimsAllClear` er sann på nøyaktig ett sted i visningsmodellen | Test som går over **alle** feilutfall og krever `claimsAllClear == false` og ikke-tom liste | `test.drift.no-false-calm` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.drift-report-names-act-and-place` | **Blad.** Rapporten sier hva som har sklidd, siden når, og hvor han gjør noe med det | Ved sådd avdrift navngir rapporten grantet, retningen (utvidet/ny/utløpt-men-brukt), tidspunktet, og hvor handlingen hører: menylinje, admin-vindu, telefon | Inspeksjon av rapport fra sådd avdrift | `test.drift.report-content` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.drift-check-proposes-never-acts` | **Blad.** Sjekken retter ikke selv | Sjekken skriver aldri til grant-cellen. Den foreslår innsnevringen; handlingen er Kjetils | Negativ test: ingen skriving mot grant-cellen fra sjekkens kodevei | `test.drift.read-only` | candidate |

### 1.6 Antiformål (`polarity: prohibited`)

| purposeRef | Tittel | «Skal ikke …» | Verifier | Status |
|---|---|---|---|---|
| `purpose://candidate.mcp-tilgangsbevis.never-widens` | Et bevis skal aldri kunne mer enn Kjetil selv | Et bevis **skal ikke** gi adgang til noe Kjetils egen identitet ikke allerede har. Et formål **skal ikke** opprette, utvide eller arve en rettighet — bare innsnevre | Sett-sammenligning: `bevisets adgangssett ⊆ Kjetils adgangssett`, kjørt som test, ikke som påstand | candidate |
| `purpose://candidate.mcp-tilgangsbevis.never-survives-narrowing` | Et gammelt bevis skal ikke overleve en innsnevring | Et bevis utstedt under et tidligere grant-sett **skal ikke** godtas etter at settet er endret | `test.consume.stale-proof-denied` | candidate |
| `purpose://candidate.mcp-tilgangsbevis.never-reports-calm-when-unread` | Stillhet skal ikke se ut som ro | Avdriftssjekken **skal ikke** rapportere «ingen avdrift» når en kilde ikke kunne leses, og **skal ikke** vise tom liste som ro | `test.drift.no-false-calm` | candidate |

### 1.7 Formålssammensetning (Book 36)

`purpose_dev.py gates` rapporterer i dag **`Composition-port: unverified`** for denne oppgaven. Grunnen er ikke noe i dette treet: tre av Book 23-nodene i omfanget (`access.audit.privacy`, `gui.quality.functional-accessible`, `test.acceptance`) mangler eksplisitt `composition`, og validatoren sier uttrykkelig «No composition is inferred for legacy parents». Totalt 18 av 57 Book 23-noder mangler den — det er en pågående migrering, ikke en mangel ved denne dekomponeringen.

Sammensetningen dette treet *ville* erklært, lest mot validatorens egne regler (`Tools/PurposePackages/purpose_composition.py`: `KINDS = {allOf, sequence, anyOf, firstOf, invariant}`, `childOrder` påkrevd for `sequence`/`firstOf`, `invariant.over` må peke på en annen samling i samme tre):

| Node | `composition` | Begrunnelse |
|---|---|---|
| `…mcp-tilgangsbevis.root` | `{"kind": "allOf"}` | Alle fem grener må være grønne. Rekkefølgen (1 → 2 → 3, så 4 og 5) er en *plan*opplysning og hører i PLAN.md, ikke i sammensetningen |
| `…grant-authority-is-a-cell` | `{"kind": "allOf"}` | Eierskap, endringsrett og grant-formen må alle holde; ingen av dem er valgfri |
| `…issuance-within-grants` | `{"kind": "allOf"}` | Fire blader, alle påkrevd |
| `…consumer-honours-the-proof` | `{"kind": "allOf"}` | Tre blader, alle påkrevd |
| `…two-keys-distinguishable` | `{"kind": "allOf"}` | To blader, begge påkrevd |
| `…drift-is-detected` | `{"kind": "allOf"}` | Fem blader, alle påkrevd |
| `…invariants` (ny samling over de tre antiformålene i §1.6) | `{"kind": "invariant", "over": "purpose://candidate.mcp-tilgangsbevis.root"}` | Et antiformål er nettopp en invariant over hele samlingen, ikke et trinn i den. Dette er formen validatoren har for det |

Merk: jeg har lest validatorens *regler*, ikke dens evalueringssemantikk (`Composition.evaluate`). Erklæringen over er derfor et forslag til P6-promotering, ikke en påstand om hva porten vil svare. Se §6 Q6.

**Iterasjon 4:** CellBase har sin egen `PurposeComposition` (`CellProtocol/Sources/CellBase/PurposeAndInterest/PurposeComposition.swift`: `purpose | allOf | anyOf | sequence | atLeast`) som Book 36 ikke kjente til. Tabellen over skrives om til Swift-uttrykk når forsoningen (M3 i `PERSPECTIVENODE_KONSEKVENS.md`) er avgjort. `invariant` finnes ikke i Swift i dag; inntil da bæres antiformålene som `GoalDefinition(lifecycle: .continuous)` som må forbli `satisfied`.
---

## 2. Avgrensning og avhengigheter

### 2.1 Hva dette IKKE er

- **Ikke entitetsutvidelse.** En entitetslenke slår sammen to entiteter og krever bevis for å eie begge (`AgentEntityLinkContract.verifyMutualSignatures()`). Dette låner ut en snever nøkkel og slår ingenting sammen. De to må ikke blandes — en lenke er permanent og bred, et bevis er kortlevd og smalt.
- **Ikke en erstatning for Chrome-innloggingen** i vanlig bruk. Formålet er testing, og bare testing.
- **Ikke delegering til andre personer.** Ett subjekt (Kjetil), én bruk (teste ny funksjonalitet i egne celler).
- **Ikke en endring av hvordan Kjetils egen nøkkel lagres eller parres.**
- **Ikke en rettighet til MCP-en.** MCP-en spør; cellen avgjør. At MCP-en *kan* be om noe er aldri grunn til at det gis.
- **Ikke correspondence-pollingen og ikke varselsarbeidet.** De er egne oppgaver; denne PDD-en skal ikke utvide seg til dem.
- **Ikke en ny nøkkelbærer.** Claude og Codex bærer beviset; de eier det ikke og kan ikke utstede det.

### 2.2 Kapabiliteter og avhengigheter oppgaven bygger på

| # | Kapabilitet / avhengighet | Kilde (fil) | Avgrensning — hva den ikke dekker | Må virke før test? | Verifier |
|---|---|---|---|---|---|
| D1 | MCP kan be agenten signere et mottaker- og tidsbundet utsagn | `Sources/HavenAgentDMCP/HavenAgentMCPService.swift:960` | Dekker **ikke** at utsagnet er adgang noe sted (A9) | Ja | Utsted et utsagn, dekod artefaktet |
| D2 | Agenten kjenner «den parrede operatøren» som Kjetils identitet | `Sources/HavenAgentCells/LocalControlCellAccess.swift` | Dekker **ikke** grants; bare binær «er det ham» | Ja | `identity_descriptor` returnerer parret operatør |
| D3 | Kontrollbroen er loopback-bundet og token-gated | `Sources/HavenAgentCellRuntime/AgentControlBridgeServer.swift:23–25, 166, 192` | Token gjelder *flaten*, ikke hva kalleren får lov til inne i cellene | Ja | `/health` svarer 200 med token, 401 uten |
| D4 | Huset har allerede en allow-liste-form for grants | `Sources/HavenAgentRuntime/RemoteIntentVerifier.swift` (`TrustedRemoteIntentIssuer`) | Ligger i config (`AgentConfig.swift:422`), **ikke** i en celle Kjetil eier | Nei (mønster, ikke avhengighet) | Les strukturen |
| D5 | **Celleavgjørelsene bevarer den snevre forespørselen gjennom alle innganger** (Astra-presisert 2026-09-12) | `CellProtocol/Sources/CellBase/Cells/GeneralCell/CellAuthorization.swift:16, :194, :228, :258`; `GeneralCell.swift:1893, :2429`; `ScaffoldKit/CellProtocolClient.swift:122`; `lesson.cellscaffold-two-holes` | Koden spør allerede cellens policy med celle+keypath+operasjon+requester — men (1) `ownerProof` behandles før kontraktgrants og gir *bred* eiertilgang, (2) traverserende GET bruker `try?` og kan falle til bredere rotlesing som ikke bevarer barnets avslag, (3) `CellProtocolClient` kaller Meddle direkte forbi resolverens preflight. Keypathen er datareferanse, aldri autoritet. Operasjonsspesifikk challenge/retry finnes ikke (M13) | **Ja — blokkerende** | `test.cell.auth-negative` grønn i **cellens egen** avgjørelse på **hver** inngang; et agentutstedt bevis regnes aldri som `ownerProof` (Q8 i konsekvensanalysen) |
| D6 | Web-flaten har en vei inn for en ikke-interaktiv kaller | **ikke verifisert** (A10) — rekognosering bestilt | Ukjent om det finnes sesjon/bearer/bevis-vei i det hele tatt | **Ja — blokkerende for gren 3 blad 3** | Rekognoseringssvar i `contract/scaffold-admission.md` før G2 |
| D7 | **En ny agent-binær kan startes på maskinen** | `Docs/Handoff_Agentbinaer_Launch_Constraint_20260911.md` | `SIGKILL (Code Signature Invalid)` / Launch Constraint Violation stopper all ny agentkode i dag | **Ja — blokkerende for alt** | Installer ny binær, `/health` svarer fra den nye |
| D8 | Pinnet CellProtocol-revisjon er forfar av CellProtocols egen main | `Scripts/assert_dependencies_are_on_their_main.sh` | — | Ja (for at CI skal kunne bygge) | Skriptet grønt i CI |
| D9 | En «alltid tilgjengelig HAVEN celle» finnes å legge baselinen i | **ikke verifisert** (A13) | Ukjent hvilken celle, og hva «alltid tilgjengelig» betyr i drift | Ja for gren 5 blad 1 | §6 Q2 besvart + cellen lest |
| D10 | Utfordringsinnboksen kan bære en ny kilde og vise hvor noe hører hjemme | `Sources/HavenAgentRuntime/AgentChallenge.swift` (grenen `varsler-20260911`) | Ligger på gren, ikke på `origin/main` ennå | Ja for gren 2 blad 5 | Fixture med ny kilde grønn |
| D11 | Composition-porten (Book 36) kan bli verifisert | `Tools/PurposePackages/purpose_composition.py`; `gates`-utdata 2026-09-12 | `unverified` i dag fordi 18 Book 23-noder mangler `composition` — pågående migrering, ikke innført av denne oppgaven | Nei for G1; ja hvis du vil ha porten grønn ved G3 | `purpose_dev.py gates` viser `Composition-port` ≠ `unverified` |

**Merk til D7 og D5:** `lesson.corr-approval-surfaces-timed-out` er nettopp dette mønsteret — en funksjon ble aldri testet fordi avhengighetene ikke virket da testen skulle kjøres. D7 er i dag rød og ligger hos Codex. Planen (P2) skal ikke legge implementering foran D7; den skal legge D7 som første arbeidspakke med Kjetil/Codex som utfører.

---

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per ting Kjetil faktisk får. Etter G2 er dette den eneste tabellen fremdrift måles mot.

| # | Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|---|
| L1 | Grant-kontrakten: hva et grant er, med 3 positive og 5 negative fixtures | fil | `contract/haven.agent-access-grant.v1.schema.json` + `fixtures/` | — | nei |
| L2 | Bevis-kontrakten: hva et bevis bærer (grant-digest, keypather, operasjoner, utløp, bevis-id) | fil | `contract/haven.agent-access-proof.v1.schema.json` + `fixtures/` | — | nei |
| L3 | Baseline-kontrakten: hvordan «slik skal grant-settet være» skrives ned | fil | `contract/haven.access-baseline.v1.schema.json` + `fixtures/` | — | nei |
| L4 | Rekognoseringssvaret om web-flatens adgangsvei (D6), med filstier og linjenumre | fil | `contract/scaffold-admission.md` | — | nei |
| L5 | Grant-oversikten, **tom tilstand** — ingen bevis utlånt | bilde | `images/` | `images/grants-tom-v1.png` | nei |
| L6 | Grant-oversikten, **fylt** — to utestående bevis med hva de kan og når de dør | bilde | `images/` | `images/grants-fylt-v1.png` | nei |
| L7 | Avdriftsrapporten, **ingen avdrift** — med eksplisitt «N kilder lest, alle lesbare» | bilde | `images/` | `images/avdrift-ren-v1.png` | nei |
| L8 | Avdriftsrapporten, **avdrift funnet** — hvilket grant, retning, siden når, hvor han gjør noe | bilde | `images/` | `images/avdrift-funnet-v1.png` | nei |
| L9 | Avdriftsrapporten, **kilde uleselig** — den tilstanden som ikke får se rolig ut | bilde | `images/` | `images/avdrift-uleselig-v1.png` | nei |
| L10 | Dataflyt: utstedelse → bærer → konsument → revisjonslogg → avdriftssjekk, hver kant navngitt med endepunkt | fil | `dataflow.md` | — | nei |
| L11 | Transkript: et bevis utstedt, presentert og sluppet inn — med ekte utdata | testutdata | `TESTRESULT.md#happy-path` | — | nei |
| L12 | Transkript: de fem nektelsene (feil keypath, feil operasjon, utløpt, gammel digest, ukjent formål) | testutdata | `TESTRESULT.md#auth` | — | nei |
| L13 | Transkript: et bevis som prøver å utvide sitt eget grant → nektet | testutdata | `TESTRESULT.md#auth` | — | nei |
| L14 | Web-flaten nådd med beviset alene, fra klient uten sesjon | kjørende flate + skjermbilde | `ACCEPT.md#web-no-session` | — | nei |
| L15 | Revisjonslogg-utdrag der Kjetils egen handling og bevisets handling står side om side og er til å skille | testutdata | `TESTRESULT.md#audit` | — | nei |
| L16 | `⊆`-testen: bevisets adgangssett mot Kjetils adgangssett, kjørt | testutdata | `TESTRESULT.md#never-widens` | — | nei |
| L17 | Akseptanse rad for rad, og gate-tilstand | fil | `ACCEPT.md`, `STATUS.md` | — | nei |

**GUI-merknad (G1-GUI):** L5–L9 er bilder, ikke beskrivelser. Dersom flaten ikke kan rendres gjennom Porthole-preview av skeleton-JSON, blir de mockups, og `images/README.md` må si eksplisitt at de er mockups og hva dagens skeleton ikke kan rendre (`lesson.scaffold-without-porthole-host-has-no-preview`). Paritet (`test.gui.parity`) planlegges som egen slice, ikke som del av implementeringen.

---

## 4. Tilknyttede formålspakker og lærdommer

### 4.1 Festede pakker

| Pakke | Relevans her |
|---|---|
| `pkg.std.everything-works` | Alltid. Bygg + full regresjon + docs i samme endring + STATUS oppdatert. |
| `pkg.std.cell-contract` | Kjernen: to–tre nye cellekontrakter, og `test.cell.auth-negative` er selve poenget her, ikke en formalitet. |
| `pkg.std.cell-combination` | Fem kanter (utstedelse, bærer, konsument, revisjon, avdrift) må erklæres i `dataflow.md`. |
| `pkg.std.gui-surface` | Gjelder: grant-oversikt og avdriftsrapport er flater Kjetil skal se på. L5–L9 er G1-GUI-artefaktene. |
| `pkg.std.codex-handoff` | Gjelder: D7 og alt bygg/test på macOS går via Codex. Idempotente skript, `--dry-run` som standard, ingen kommentar på samme linje som en kommando. |

### 4.2 Lærdommer som har formet treet (sitert, ikke oppsummert)

- **`lesson.purpose-never-grants-rights`** (blocker, 2026-08-03): «Et formål kan innsnevre en rettighet, aldri opprette, utvide eller arve en; exact match; `purpose://prompt.unknown` feiler lukket.» → Antiformål 1.6 `never-widens`, og `⊆`-testen som L16. Dette er hele sikkerhetsbunnen: beviset er en *innsnevring av Kjetil*, ikke en ny rettighetsbærer.
- **`lesson.cellscaffold-two-holes`** (blocker, 2026-09-01): «CellScaffold har … autorisasjon som kaster nøkkelstien og bare sjekker eierskap.» → D5 som **blokkerende** avhengighet, og gren 3 blad 1. Uten dette er grantene dekorasjon.
- **`lesson.ciphertext-field-held-plaintext-hash`** (blocker, 2026-09-10): «En påstand om at noe er kryptert, signert eller verifisert skal bekreftes på artefaktet — les bytene, ikke feltet.» → `proof-binds-grant-digest` testes ved å **dekode beviset og regne om digesten**, ikke ved å lese et felt som heter `grantDigest`.
- **`lesson.test-the-representation-not-the-issuance-flow`** (minor, 2026-09-09): «Skille to spørsmål: hvordan får noen rollen, og hva gir rollen.» → Gren 2 (utstedelse) og gren 3 (konsumpsjon) er bevisst skilt, med egne tester. Konsument-testene installerer beviset på husets etablerte måte og tester *virkningen*.
- **`lesson.empty-list-must-not-look-like-calm`** (major, 2026-09-10): «En kilde som svarer 403, et token som er feil, en agent som ikke svarer — alle tre gir en tom liste, og en tom liste ser ut som at ingenting venter … ha én boolsk verdi (`claimsAllClear`) som er sann på nøyaktig ett sted.» → Hele gren 5 blad 3, antiformål 1.6 `never-reports-calm-when-unread`, og L9 som eget bilde.
- **`lesson.corr-approval-surfaces-timed-out`** (major, 2026-08-30): «Corr-godkjenningen er utestet fordi flater/godkjenninger timet ut før testing rakk å skje.» → §2.2 lister D5–D7 som egne rader med verifier, og D7 er første arbeidspakke i P2.
- **`lesson.bridge-inferred-architecture-from-one-use`** (major, 2026-08-09): → §0.2 har 15 rader med kilde, og A10/A12/A13/A15 står som `unavailable`/`recalled` framfor å bli antatt.
- **`lesson.new-cell-must-declare-its-provisioning-mode`** (major, 2026-09-09): → Grant-cellen og baseline-cellen må hver svare på de tre spørsmålene (require-existing mot fersk lagring? kanonisk eager-bootstrap? Porthole-publisert flate?) **før** de registreres. Tas inn som egen rad i §5.
- **`lesson.plan-instead-of-delivery`** (major, 2026-08-21): → §3 er forventningskontrakten; dette dokumentet er ikke leveransen.
- **`lesson.local-main-is-not-main`** (major, 2026-09-11) og **`lesson.branch-is-empty-after-eight-work-packages`** (major, 2026-09-09): → P2 legger en commit-pakke inn etter første grønne bygg, og baseline måles mot en ren eksport av `origin/main`, ikke mot arbeidstreet.
- **`lesson.codex-mcp-60s`** og **`lesson.codex-workspace-write-cannot-build-cellscaffold`**: → alle bygg og testkjøringer kjøres detached via Codex med `danger-full-access`, aldri som MCP-kall eller `workspace-write`-køjobb.

---

## 5. Avledede tester

### 5.1 Pakketester (auto)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| `test.build` | `purpose://quality.build-and-regression` | Detached `swift build` på macOS via Codex | `TESTRESULT.md#build` | venter |
| `test.regression` | `purpose://quality.build-and-regression` | Full `swift test`; antall før/after fra ekte kjøring, ikke fra rapport | `TESTRESULT.md#regression` | venter |
| `test.docs-updated` | `purpose://quality.docs-in-same-change` | Docs-diff med «Last verified against code»-dato | `ACCEPT.md#docs` | venter |
| `test.status-current` | `purpose://quality.work-is-visible` | STATUS.md mot filene i mappen | `ACCEPT.md#status` | venter |
| `test.gui.reference-image-exists` | `purpose://gui.expectation-agreed-before-build` | `purpose_dev.py validate` sjekker `images/` mot §3 (L5–L9) | `images/` | venter |
| `test.gui.parity` | `purpose://gui.parity-with-approved-image` | Screenshot i samme viewport side om side med referansen | `ACCEPT.md#parity` | venter |
| `test.gui.load-time` | `purpose://gui.surface-loads-in-time` | Tre målinger, logg sjekket for navnebom | `TESTRESULT.md#load-time` | venter |
| `test.skeleton.no-unreachable-elements` | `purpose://gui.ways-in-are-reachable` | `CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` | `TESTRESULT.md#reachability` | venter |
| `test.skeleton.purpose-actions-reachable` | `purpose://gui.ways-in-are-reachable` | §3-radene mot `SkeletonReachabilityAudit.reachableActionKeypaths` | `ACCEPT.md#ways-in` | venter |
| `test.cell.contract-fixtures` | `purpose://cell.contract-explicit` | Kontraktvalidator mot alle fixtures i `contract/` | `TESTRESULT.md#contract` | venter |
| `test.cell.auth-negative` | `purpose://cell.authorization-honours-keypath` | Feil requester / feil keypath / ukjent formål | `TESTRESULT.md#auth` | venter |
| `test.cell.stub-scan` | `purpose://cell.no-empty-stubs` | Ingen no-op-handler uten `not-implemented` | `ACCEPT.md#stubs` | venter |
| `test.cells.dataflow-matches-contracts` | `purpose://cells.dataflow-declared` | Hver kant i `dataflow.md` finnes i en kontrakt | `PLAN.md#dataflow` | venter |
| `test.cells.capability-audit` | `purpose://cells.capabilities-declared-with-boundary` | Alle 15 rader i §0.2 har status; bare `retrieved` bærer planen | `FORMAALSSPEC.md#audit` | venter |
| `test.handoff.dry-run` | `purpose://handoff.runnable-without-guessing` | Alle overleveringsskript uten `--go` gir 0 og lister hva de ville gjort | `TESTRESULT.md#dry-run` | venter |

### 5.2 Tester avledet av bladene i §1

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| `test.grant.contract-fixtures` | `…grants-are-keypath-and-operation` | 3 positive + 5 negative fixtures: grant uten keypath, uten operasjon, uten tidstak, med «alt»-jokertegn, med rolle i stedet for keypath | `TESTRESULT.md#contract` | venter |
| `test.grant.auth-negative` | `…grant-cell-is-owned` | Tre enhetstester navngitt etter tilfellet; **feil requester skal få `deniedNoGrant`, ikke tom liste** | `TESTRESULT.md#auth` | venter |
| `test.grant.proof-cannot-widen-itself` | `…grant-change-requires-kjetil` | Presenter et gyldig bevis, forsøk `set` mot grant-cellen → nektet; så gjør samme skriving som parret operatør → godtatt | `TESTRESULT.md#auth` | venter |
| `test.grant.provisioning-mode-declared` | `lesson.new-cell-must-declare-its-provisioning-mode` | Grant-cellen og baseline-cellen svarer skriftlig på de tre spørsmålene; `OrchestratorPersistenceTests` og `TopUpCheckoutTests` fortsatt grønne | `ACCEPT.md#provisioning` | venter |
| `test.issue.reads-live-grants` | `…issuance-reads-live-cell` | Snevre inn grantet, be om bevis → nektet uten omstart; utvid → bevis utstedt | `TESTRESULT.md#issue` | venter |
| `test.issue.digest-on-artifact` | `…proof-binds-grant-digest` | Dekod det utstedte beviset, regn `sha256` over kanonisk grant-sett fra cellen, sammenlign. **Les bytene, ikke feltet** | `TESTRESULT.md#issue` | venter |
| `test.issue.expiry-ceiling` | `…proof-expiry-is-short` | Tre utstedelser; mål `expiresAt − issuedAt` på artefaktet; krev ≤ grantets tak og ≤ 15 min som standard | `TESTRESULT.md#issue` | venter |
| `test.issue.visible-to-kjetil` | `…issuance-is-visible` | Utsted, les utfordringsinnboksen; raden navngir hva, til hvem, hvor lenge, hvor den trekkes tilbake | `ACCEPT.md#visible` | venter |
| `test.consume.auth-negative` | `…each-cell-decides-at-traversal` | Tre negative i **cellens egen inngangsavgjørelse**: feil datareferanse, feil operasjon, `purpose://prompt.unknown` — og én positiv: riktig bevis gir tillat *eller* Agreement challenge, aldri stille eierskapsgjennomslipp | `TESTRESULT.md#auth` | venter |
| `test.consume.challenge-resolvable` | `…challenge-is-resolvable-from-notification` | Så en traversering inn i en celle uten grant; assert (1) cellen reiser en Agreement challenge, ikke stille avvisning, (2) varselet finnes i varslingssenteret med `handleAt`, (3) svar i varselet oppfyller vilkåret, (4) traverseringen fullføres. Negativ: ingen challenge uten vei til handling | `TESTRESULT.md#challenge` | venter |
| `test.consume.stale-proof-denied` | `…consumer-checks-expiry-and-digest` + `never-survives-narrowing` | (1) utløpt bevis → nektet. (2) endre grant-settet, presenter gammelt bevis → nektet med grunn «stale grant digest» | `TESTRESULT.md#auth` | venter |
| `test.consume.web-no-session` | `…web-surface-without-chrome-login` | Kall flaten fra klient uten sesjonscookie, med beviset; skjermbilde av resultatet. **Blokkert til D6/D7** | `ACCEPT.md#web-no-session` | venter |
| `test.audit.names-the-proof` | `…audit-names-the-proof` | Gjør samme handling (a) som Kjetil, (b) med bevis; les de to revisjonsradene; de skal være forskjellige og beviset navngitt | `TESTRESULT.md#audit` | venter |
| `test.revoke.kills-all` | `…revocation-is-one-act` | Utsted to bevis, trekk tilbake én gang, begge nektes; Kjetil ser bekreftelsen | `TESTRESULT.md#revoke` | venter |
| `test.drift.baseline-readable-agent-down` | `…baseline-is-declared-and-readable` | Stopp agenten, les baselinen, få innhold — ikke feil | `TESTRESULT.md#drift` | venter |
| `test.drift.runs-on-schedule` | `…drift-check-runs-unasked` | To påfølgende kjøringer med tidsstempel uten at noen ba om det; «ikke kjørt siden X» er eget funn | `TESTRESULT.md#drift` | venter |
| `test.drift.no-false-calm` | `…drift-report-is-per-source` + `never-reports-calm-when-unread` | Gå over **alle** feilutfall (celle 403, token feil, agent nede, baseline mangler, grant-celle tom) og krev `claimsAllClear == false` og ikke-tom liste i hvert tilfelle | `TESTRESULT.md#drift` | venter |
| `test.drift.report-content` | `…drift-report-names-act-and-place` | Så en avdrift; rapporten navngir grantet, retningen, siden når, og hvor handlingen hører (menylinje / admin-vindu / telefon) | `ACCEPT.md#drift` | venter |
| `test.drift.read-only` | `…drift-check-proposes-never-acts` | Negativ: ingen skriveoperasjon mot grant-cellen i sjekkens kodevei (kodesøk + test med skrivebeskyttet celle) | `TESTRESULT.md#drift` | venter |
| `test.never-widens.subset` | `…never-widens` | Regn ut bevisets adgangssett og Kjetils adgangssett, krev `⊆`. Kjøres som test, ikke som påstand i et dokument | `TESTRESULT.md#never-widens` | venter |

---

## 6. Åpne spørsmål og råd

Bare spørsmål som endrer treet. Rådene er råd — valget er ditt. Argumentene står sammen med hvert råd.

### Q1 — Klassifiseringen: bekreft eller korriger

Besvart ved å lese Book 23, ikke ved å gjette. To av `lookup`s tre forslag var leksikalske bom (A16). Roten hører under `purpose://access.audit.privacy` (active), og de fem grenene under `purpose://self-determination.data.{scope, use-purpose, recipients, verifiability, exercisability}` — se kartet i §1. **Spørsmål:** godtar du den plasseringen, eller ser du en bedre? Dette er det eneste stedet der jeg har tolket din intensjon inn i *ditt* tre, så det er verdt et blikk.

### Q2 — Hvilken celle er «alltid tilgjengelig»?

Du foreslo at baselinen kan ligge i en alltid tilgjengelig HAVEN-celle. Jeg har ikke verifisert hvilken celle det er, eller hva «alltid tilgjengelig» betyr i drift (når agenten er nede? når maskinen er av?). **Spørsmål:** navngi cellen, eller si at dette er en ny celle.

### R1 — ~~Råd~~ **Vedtatt 2026-09-12 (Kjetil): «baselinen skal ikke ligge i samme celle som grantene.»**

*Argument:* en baseline er bare verdt noe hvis den er vanskeligere å endre enn det den måler. Ligger de i samme celle, kan den som utvider et grant utvide baselinen i samme skriving — og avdriftssjekken blir stille nøyaktig i det øyeblikket den skulle ropt. Derfor: grants i en celle du eier i agenten (din formulering), baseline i en separat celle som **bare din egen nøkkel** kan endre — aldri et agentutstedt bevis. Da kan ikke agenten heve sitt eget tak. Dette er en skjerping av ditt eget forslag, ikke en innvending mot det.

### R2 — Råd: beviset bør bære digesten av grant-settet det ble utstedt under

*Argument:* «tilgangene har sklidd» har to former. Den ene er at grantene er blitt videre. Den andre er at et gammelt bevis fortsatt virker etter at du har snevret inn. Bare den andre kan hindres teknisk, og bare hvis beviset sier hvilket grant-sett det tilhører. Med digesten i beviset kan konsumenten avvise et foreldet bevis, og avdriftssjekken har en grunnsannhet å sammenligne mot. Uten den er «jeg snevret inn i går» bare en hensikt.

### R3 — Råd: grants som (celle, keypath, operasjon, tidstak) — ikke roller, ikke scope-strenger

*Presisering etter Kjetils korreksjon:* keypathen i et grant er **datareferansen** grantet gjelder for — hva i cellen. Autoriteten er cellens avgjørelse ved inngang, aldri referansen selv. *Argument:* `lesson.cellscaffold-two-holes` sier at det finnes autorisasjonskode i huset som kaster nøkkelstien og bare sjekker eierskap. En scope-streng («test», «read») vil slik kode lese som «eier, altså alt». Et grant som navngir keypath og operasjon kan ikke utvides stille av eierskapskode — for da feiler den negative testen høyt. Og huset har mønsteret fra før: `TrustedRemoteIntentIssuer` har `allowedTopics` og `allowedActionIDs`, ikke en rolle.

### R4 — Råd: minutter, ikke et døgn

*Argument:* `AgentSignatureStatement.maxValiditySeconds` er 86 400. Det er et fornuftig tak for et *utsagn*, men et testbevis som lever et døgn er den enkleste måten dette lekker på — det overlever økten det ble laget for. Jeg foreslår 15 minutter som standardtak i grantet, med mulighet for at du setter noe annet per grant. Kort levetid gjør også avdriftssjekken mindre å rydde etter.

### R5 — Råd: beviset skal ikke se ut som deg i revisjonsloggen

*Argument:* «to nøkler vi kan teste på» er bare verdt noe hvis du etterpå kan se hvilken nøkkel som gjorde hva. Presenterer beviset seg som Kjetil, blir revisjonsloggen ubrukelig nettopp der den betyr mest — når en test gjorde noe uventet i dine egne celler. Derfor bør innslipp loggføres som «kjetil via bevis `<id>`, grant-digest `<…>`», ikke som «kjetil».

### R6 — Råd: avdriftssjekken foreslår, du snevrer inn

*Argument:* du sa «det er alltid brukerens valg». Jeg er enig også av en teknisk grunn: en sjekk som kan skrive til grant-cellen er i praksis en andre vei til å endre tilganger, og da må den sikres som en sådan. En sjekk som bare leser og rapporterer kan ikke misbrukes til å endre noe. Den bør derfor foreslå innsnevringen ferdig formulert, og la handlingen være din.

### Q6 — Skal jeg foreslå `composition` for `purpose://access.audit.privacy` i Book 23?

Composition-porten står `unverified` fordi tre Book 23-noder i omfanget mangler `composition` (§1.7). Jeg kan foreslå den for `access.audit.privacy`, men Book 23 endres aldri kanonisk uten ditt ord. **Spørsmål:** (a) la porten stå `unverified` og notere hvorfor, (b) jeg foreslår composition for den ene noden som er *vår* (`access.audit.privacy`) og du ser diffen, eller (c) det tas som egen sak i migreringen og holdes utenfor denne PDD-en? Mitt forslag er (b) for den ene noden, (c) for de sytten andre.

### Q3 — Hvor skal avdriftsrapporten dukke opp, og hvor ofte?

Kandidatene er menylinjen (du ser den hele tiden), utfordringsinnboksen (du behandler den allerede der), eller e-post/varsel ved funn. Periode: daglig, ukentlig, eller ved hver utstedelse pluss ukentlig. **Spørsmål:** hvilken kombinasjon? Mitt forslag: ukentlig full rapport i utfordringsinnboksen, pluss et funn med én gang hvis et grant er blitt videre siden sist.

### Q4 — Skal `web-surface-without-chrome-login` (gren 3, blad 3) være med i denne PDD-en?

Den avhenger av D6 (ukjent) og D5 (kjent hull i scaffold-autorisasjonen). Den er også det du faktisk ba om. **Spørsmål:** beholder vi den som blad her og godtar at PDD-en ikke kan lukkes før D5 er rettet, eller skiller vi den ut som egen PDD som denne leverer beviset til? Mitt forslag: behold den, men som siste blad, og la D5 være en navngitt sak med egen eier.

### Q5 — D7 blokkerer alt

Ny agent-binær kan ikke startes (`Launch Constraint Violation`), og saken ligger hos Codex. Ingenting i gren 1–4 kan testes før den er løst. **Spørsmål:** skal P2 legge D7 som arbeidspakke 0 med Codex som utfører, eller venter vi med G2 til D7 er grønn?

---

**Q9 (nytt 2026-09-17, til Kjetil).** (e) legger inn fem krav som ikke er i det
godkjente treet: katalogovervåking som utløser (K-A2), formålskatalogen som
grensesnitt utad (K-A3), tilbakemelding om formålsoppfyllelse (K-A4), formål i
stedet for kommandolister (K-A6), og modus lese/skrive/utføre med ulikt
godkjenningsnivå (K-A7). Skal de inn som en sjette gren i denne PDD-en, eller er
de en egen PDD som låner formålsmodellen herfra? Claudes råd: **egen PDD**, fordi
denne handler om å *utstede et bevis* mens (e) handler om å *utføre på Kjetils
vegne* — to forskjellige formål som deler grant-modellen. Argumentet mot: de
deler så mye mekanikk at to spesifikasjoner kan drive fra hverandre. Kjetil
avgjør.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-12 | Opprettet av `purpose_dev.py new` | Losen |
| 1 | 2026-09-12 | §0 ordrett intensjon (to meldinger) + brief-audit; §1 tre med rot, 5 grener, 3 antiformål, 17 blader; §2 avgrensning + 10 avhengigheter (D5/D6/D7 blokkerende); §3 17 leveranser inkl. 5 bilder; §4 11 siterte lærdommer; §5 15 pakketester + 19 avledede; §6 spørsmål + 6 råd med argumenter | Losen |
| 2 | 2026-09-12 | Leste Book 23 (57 noder) og klassifiserte treet mot den: roten under `access.audit.privacy` (active), de fem grenene under `self-determination.data.{scope, use-purpose, recipients, verifiability, exercisability}`. A15 gikk fra `recalled` til `retrieved`; A16–A18 lagt til; to av `lookup`s tre forslag avvist som leksikalske bom. Q1 besvart | Losen |
| 3 | 2026-09-12 | Kjørte `purpose_dev.py validate` (exit 0) og `gates` (G1-artefakt ✓, port venter). Leste Book 36-validatoren; la til §1.7 formålssammensetning, D11 og Q6. Composition-porten er `unverified` av en grunn som lå der fra før | Losen |
| 4 | 2026-09-12 | **G1 godkjent av Kjetil** med vilkår «riktig formålsarkitektur». Korreksjoner tatt inn: A5 bekreftet; A11 og D5 omformulert (keypath er datareferanse, cellen avgjør ved traversering: tillat/avvis/Agreement challenge); gren 3 blad 1 omdøpt til `each-cell-decides-at-traversal`; nytt blad `challenge-is-resolvable-from-notification` (brukeren må ha verktøy: varslingssenter, oppfyll direkte eller åpne verktøy) med `test.consume.challenge-resolvable`; R1 vedtatt (baseline i annen celle); R3 presisert; §1.7 merket for omskriving til `PurposeComposition`. Konsekvensanalysen ligger i `PERSPECTIVENODE_KONSEKVENS.md` | Losen |
| 5 | 2026-09-12 | Astras gjennomgang (`handoff/CODEX_REVIEW_PERSPECTIVENODE.md`) tatt inn: D5 presisert med de tre inngangene som svekker den snevre forespørselen (`ownerProof` før grants, `try?`-fallback, `CellProtocolClient` forbi preflight); blad `challenge-is-resolvable-from-notification` peker nå på den faktiske mekanismen (`AdmissionChallengePayload`/`connect.challenge`) og på gapet (M13). Konsekvensanalysen er i iterasjon 2 | Losen |
