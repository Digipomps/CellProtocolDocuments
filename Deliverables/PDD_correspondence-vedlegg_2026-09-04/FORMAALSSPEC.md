# Formålsspesifikasjon — correspondence vedlegg

Oppgavemappe: `PDD_correspondence-vedlegg_2026-09-04` · Opprettet 2026-09-04 · Iterasjon 0 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Gjør B - og kjør igjennom formålsdekomponering. Vi burde på et tidspunkt lage en høyhastighets low latency chunked overføring av data som er uavhenging av om payload er kryptert eller hvor stor den er. Vi trenge full kruptering etterhvert også. Lag pakken til Vegard når vi mener vi har en brukbar løsnin.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| «Gjør B» = vedlegget lagres som objekt og meldingen bærer bare en referanse | retrieved (Kjetils melding i denne økten; modellen er omformet i §1 etter kontraktlesing, se §7 iter. 1) | denne økten |
| CorrespondenceCell finnes og er envelope-only med fire actions (inbox, readMessage, sendMessage, ackMessage) | retrieved | `CellProtocol/Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift` l.46–250 |
| Indre konvolutt har `subject, contentType, content, clientMessageID, owner, senderSignature` — ingen vedleggsfelt | retrieved | `CellProtocol/Sources/CellBase/Cells/Correspondence/CorrespondenceEnvelope.swift` l.56–62 |
| Ytre konvolutt eksponerer `ciphertextSize` til operatør; innhold og emne aldri | retrieved | `Book/correspondence_cell_contract_v0.json` §security.operatorVisibility |
| `ContentCryptoSuite.seal/open` forsegler **hele** innholdet i én operasjon over `combinedCiphertext: Data` | retrieved | `CellProtocol/Sources/CellBase/Crypto/ContentCryptoEnvelopeUtility.swift` l.64, l.185; `Crypto/CryptoAgilityModels.swift` l.258–261 |
| Det finnes ingen strømmende/chunket forsegling i dagens suiter | retrieved (søk etter `chunk`/`stream` i Crypto/ ga null treff) | samme som over |
| MCP-en sender fortsatt **plaintext** `content`, `maxLength: 16384` — S5 (MCP som celleklient) er ikke gjort | retrieved | `HavenAgentD/Sources/HavenCorrespondenceMCP/CorrespondenceMCPService.swift` l.107–108; ingen treff på `Envelope`/`seal(` i den mappen |
| Ekstern Agreement har nøyaktig fire grants; `neverGranted` er uttømmende | retrieved | `Book/correspondence_cell_contract_v0.json` §externalAgreementTemplate |
| Utløp sletter ytre og indre sammen, aldri bare kroppen | retrieved | samme, §retention.expiryDeletes |
| Medlemsendring lukker cellen (Kjetils beslutning 01.09.) | retrieved | `Codex_Handoff_Correspondence_First_Class_2026-09-01.md` §Decisions 2 |
| «Full kryptering etterhvert» | retrieved (Kjetils ord) — merk at kontrakten allerede krever E2E for meldinger; det som mangler er *strømmende* kryptering for store payloads | denne økten + kontrakt §envelope |
| `purpose://access.audit.privacy` er en egnet forelder | recalled (leksikalsk forslag fra `purpose_dev.py lookup`, ikke verifisert mot Book 23-noden) | lookup-utdata |
| Vegard-pakken skal lages «når vi mener vi har en brukbar løsning» | retrieved (Kjetils ord); gatene fra 01.09. står fortsatt | denne økten + `Codex_Handoff_Konvolutt_Celle_Entitet_2026-09-01.md` |

**Konsekvens av auditen:** to `retrieved`-funn flytter oppgaven. (1) Operatørblindhet for vedlegg krever *ikke* en egen celle med egen Agreement — konvolutten gir den allerede; en egen celle ville i tillegg bryte `hosting.constraint` («no outer field may assume both parties on one scaffold»). (2) Chunket, størrelsesuavhengig overføring er **ikke** mulig med dagens suiter; det er et krypto-arbeid, ikke et transportarbeid.

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.correspondence-vedlegg.root` | Melding kan bære ikke-tekstlig innhold | `purpose://access.audit.privacy` (recalled) | En melding kan bære bilde/fil av vilkårlig størrelse; operatøren ser aldri innholdet; kanalen blir ikke en filserver | Alle blad under grønne | candidate |
| `…root.referenced-not-inlined` | Vedlegg refereres, ikke inlines | root | Meldingens indre konvolutt bærer et manifest; bytene ligger som eget forseglet objekt adressert med `attachmentID` | test.att.manifest-only, test.att.no-new-cell | candidate |
| `…referenced-not-inlined.manifest-in-inner` | Manifestet ligger i det indre konvoluttet | over | `attachmentID`, `mediaType`, `byteLength`, `plaintextDigest`, `caption` finnes bare inne i chifferteksten; manifestet er **eneste** adresse til vedlegget (Kjetil 04.09.) | test.att.manifest-only, test.att.one-message-only | candidate |
| `…referenced-not-inlined.object-in-same-cell` | Objektet bor i relasjonscellen | over | Ingen ny celle, ingen ny Agreement, ingen ny medlemsliste opprettes for et vedlegg | test.att.no-new-cell | candidate |
| `…referenced-not-inlined.no-sender-side-fetch` **(prohibited)** | Mottaker skal ikke måtte nå avsenders scaffold | over | Hentestien består av `cellID` + `attachmentID` alene; ingen vertsadresse i noe ytre felt | test.att.no-host-in-outer | candidate |
| `…root.operator-blind` | Operatørblind for vedlegg | root | Et scaffold-dump viser opake bytes og størrelse — ingen mediaType, filnavn, caption eller klartekst | test.att.dump-opaque | candidate |
| `…operator-blind.no-unobservability-claim` **(prohibited)** | Ikke påstå uobserverbarhet | over | Ingen kontrakt-, doc- eller pakketekst antyder at størrelse, tidspunkt eller frekvens er skjult | test.att.claim-scan | candidate |
| `…root.lifecycle-follows-message` | Livsløpet følger meldingen | root | Vedlegget lever og dør med meldingen det hører til | test.att.expiry-together, test.att.close-kills-fetch | candidate |
| `…lifecycle-follows-message.expiry-together` | Utløp sletter vedlegget med meldingen | over | Etter `expiresAt` er ytre rad, indre chiffertekst og vedleggsbytene borte i samme operasjon | test.att.expiry-together | candidate |
| `…lifecycle-follows-message.close-kills-fetch` | Lukket celle stenger henting | over | `cell.closed` og medlemsendring gjør pågående og nye hentinger til `cellClosed` | test.att.close-kills-fetch | candidate |
| `…root.chunked-transfer-payload-agnostic` | Chunket overføring uavhengig av payload | root | Overføringslaget adresserer opake byte-intervaller og trenger aldri en nøkkel; ytelse og minnebruk er uavhengig av størrelse | test.att.transport-keyless, test.att.constant-memory, test.att.resume, test.att.ttfb | candidate |
| `…chunked.transport-keyless` **(prohibited: transport skal ikke dekryptere)** | Transporten dekrypterer ikke | over | Chunk-laget har ingen tilgang til nøkler; hver chunk verifiseres med egen chiffertekst-digest | test.att.transport-keyless | **låst i kontrakt, bygges etter S5** |
| `…chunked.constant-memory` | Størrelsesuavhengig | over | Konstant minnebruk hos scaffold og klient over 10 MB / 100 MB / 1 GB | test.att.constant-memory | **låst i kontrakt, bygges etter S5** |
| `…chunked.resume` | Gjenopptagbar | over | Avbrutt overføring gjenopptas fra siste verifiserte chunk uten å sende det som allerede er kommet | test.att.resume | **låst i kontrakt, bygges etter S5** |
| `…chunked.ttfb` | Lav latens | over | Tid til første byte er uavhengig av objektstørrelse innenfor en oppgitt margin | test.att.ttfb | **låst i kontrakt, bygges etter S5** |
| `…chunked.streaming-crypto-suite` | Strømmende forsegling (`attachmentStreamV1`) | over | En suite som forsegler per chunk med felles innholdsnøkkel og per-chunk nonce, registrert i `ContentCryptoSuite`; ingen størrelsesgrense i formatet | test.att.suite-roundtrip, test.att.suite-tamper, test.att.suite-no-size-cap | **blad i DENNE oppgaven** (Kjetil 04.09.) |
| `…root.rights-do-not-grow` | MCP-ens rettigheter vokser ikke | root | Nøyaktig to nye grants; `neverGranted` uendret; ingen filsystemrettighet | test.att.grants-exactly-two, test.att.no-fs-right, test.att.fetch-only-addressed | candidate |
| `…rights-do-not-grow.grants-exactly-two` | To nye grants og ikke flere | over | `attachToMessage` (-w--) og `fetchAttachmentRange` (-w--) i den eksterne malen; ingenting annet | test.att.grants-exactly-two | candidate |
| `…rights-do-not-grow.no-fs-right` **(prohibited)** | Ingen filsystemrettighet til MCP-en | over | `attachToMessage` tar bytes inline i prosessen, aldri en sti | test.att.no-fs-right | candidate |
| `…rights-do-not-grow.fetch-only-addressed` | Henting bare på egne meldinger | over | Henting på en melding som ikke er adressert til requesteren avvises med `grantNotHeld` | test.att.fetch-only-addressed | candidate |
| `…root.no-attachments-on-plaintext-path` **(prohibited)** | Ingen vedlegg på dagens plaintext-vei | root | `attachToMessage` er umulig så lenge klienten er HTTP-adapteren; vedlegg forutsetter S5 | test.att.gated-on-s5 | candidate |

Merknad om navngivning: alle noder er `candidate` og navngitt her av Losen. Forelder `purpose://access.audit.privacy` er `recalled` og må verifiseres mot Book 23 før G2.

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.
Hvert bladformål skal ha en test i §5. Et formål uten observerbart Goal er ikke klart til arbeid.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke generell fildeling, filsynk eller CDN. Et vedlegg er bundet til én melding i én relasjon.
- Ikke en ny celle per vedlegg, og ikke lagring i correspondence-serverens eget lager.
- Ikke GUI. Ingen vedleggsknapp i Butler Chat eller noen annen flate i denne oppgaven.
- Ikke migrering av eksisterende plaintext-meldinger.
- Ikke sending til Vegard, og ingen invitasjon eller pakke ut av huset.
- Ikke uobserverbarhet. Trafikkmønster — volum, tidspunkt, størrelse — lekker uansett.

| Kapabilitet / avhengighet | Kilde (fil) | Avgrensning — hva den ikke dekker | Må virke før test? |
|---|---|---|---|
| `CorrespondenceCell`, envelope-only, fire actions | `CellProtocol/Sources/CellBase/Cells/Correspondence/CorrespondenceCell.swift` | Ingen vedleggs-keypath, ingen objektlagring | ja |
| Indre/ytre konvolutt | `…/Correspondence/CorrespondenceEnvelope.swift` l.17–62 | Indre har ingen manifest-plass; ytre har bare `ciphertextSize` for meldingen | ja |
| `ContentCryptoEnvelopeUtility.seal/open` og suite-registeret | `…/Crypto/ContentCryptoEnvelopeUtility.swift` l.64, l.185, l.291; `Crypto/CryptoAgilityModels.swift` l.258–261 | **Engangsforsegling over hele `combinedCiphertext: Data`.** Ingen strømming, ingen per-chunk-nonce. Dekker derfor ikke vedlegg — `attachmentStreamV1` skrives som ny suite ved siden av (Kjetil 04.09.), eksisterende suiter røres ikke | ja — for `test.att.suite-*` |
| Ekstern Agreement-mal og `neverGranted` | `Book/correspondence_cell_contract_v0.json` | Nevner ikke vedlegg; må utvides bevisst, ikke ved analogi | ja |
| Retensjon sletter ytre+indre sammen | samme, §retention | Sier ingenting om et tredje objekt | ja |
| MCP som celleklient (S5) | `Codex_Handoff_Correspondence_First_Class_2026-09-01.md` §S5 | **Ikke gjort.** Dagens MCP sender plaintext, `maxLength 16384` (`CorrespondenceMCPService.swift` l.107–108). Meldingen Losen sendte 04.09. gikk i klartekst gjennom operatørens rute | ja — blokkerende for hele oppgaven |
| Notariseringsgaten | `Codex_Handoff_Konvolutt_Celle_Entitet_2026-09-01.md` §Slice A | Åpen siden 18. juli. Gjelder Vegard-pakken, ikke vedleggsarbeidet | nei (men blokkerer §3-raden om pakken) |

`lesson.corr-approval-surfaces-timed-out`: raden over om S5 er nettopp den avhengigheten som må være grønn før den *egentlige* vedleggstesten kjøres. Vi tester ikke vedlegg på en kanal som ikke er blitt E2E ennå.

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2.
(ingen GUI-flate deklarert — sett `surfaces` i STATUS.md hvis det er feil)
| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Utvidet cellekontrakt med vedleggsobjekt, manifest-felt, to nye grants og chunk-adressering | fil | `CellProtocolDocuments/Book/correspondence_cell_contract_v1.json` | — | nei |
| Kontrakt-fixtures, positive og negative (bl.a. plaintext-manifest, feil requester, ukjent formål) | fil | `contract/fixtures/` | — | nei |
| Dataflytdiagram med kant-tabell: `sendMessage` → `attachToMessage` → `fetchAttachmentRange` | fil | `dataflow.md` | — | nei |
| Swift-implementasjon i `CorrespondenceCell` + `CorrespondenceEnvelope` | testutdata | `TESTRESULT.md#build`, `#regression` | — | nei |
| Scaffold-dump som viser opake bytes, størrelse og ingenting annet | testutdata | `TESTRESULT.md#dump` | — | nei |
| Måling: konstant minnebruk og tid til første byte over 10 / 100 / 1000 MB | testutdata | `TESTRESULT.md#chunk-memory`, `#ttfb` | — | nei |
| Negative autorisasjonstester (feil requester, feil keypath, `purpose://prompt.unknown`, ikke-adressert melding) | testutdata | `TESTRESULT.md#auth` | — | nei |
| Ett ekte vedlegg sendt fra Losen til `victoria-lille-robot` og hentet tilbake med digest-match | testutdata | `TESTRESULT.md#e2e` | — | nei |
| **Vegard-pakken** | *leveres ikke i denne oppgaven* | egen oppgavemappe etter G3 her + de to gatene fra 01.09. | — | n/a |

Kartet «Losens kart» som utløste saken er levert utenfor kanalen, per post via Kjetil. Den omveien er borte når `#e2e` er grønn — det er kriteriet på at problemet faktisk er løst.

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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://access.audit.privacy [active] — Access, audit and privacy
- purpose://questionnaire.access.audit [active] — Questionnaire access audit

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | purpose://quality.build-and-regression | Prosjektets byggkommando (xcodebuild / swift build / pytest) — angis i PLAN.md. | TESTRESULT.md#build | venter |
| test.regression | purpose://quality.build-and-regression | Prosjektets testkommando; sammenlign antall tester før/etter. | TESTRESULT.md#regression | venter |
| test.docs-updated | purpose://quality.docs-in-same-change | Les diff; kryss av i ACCEPT.md. | ACCEPT.md#docs | venter |
| test.status-current | purpose://quality.work-is-visible | Sammenlign STATUS.md med filene i mappen. | ACCEPT.md#status | venter |
| test.cell.contract-fixtures | purpose://cell.contract-explicit | python3 checks/validate_contract.py | TESTRESULT.md#contract | venter |
| test.cell.auth-negative | purpose://cell.authorization-honours-keypath | Tre enhetstester navngitt etter tilfellet. | TESTRESULT.md#auth | venter |
| test.cell.stub-scan | purpose://cell.no-empty-stubs | Søk i berørte filer; skriv listen i ACCEPT.md. | ACCEPT.md#stubs | venter |
| test.cells.dataflow-matches-contracts | purpose://cells.dataflow-declared | Tabell kant→kontrakt i PLAN.md. | PLAN.md#dataflow | venter |
| test.cells.capability-audit | purpose://cells.capabilities-declared-with-boundary | Tabell i FORMAALSSPEC.md §0. | FORMAALSSPEC.md#audit | venter |
| test.att.manifest-only | `…manifest-in-inner` | Serialiser en lagret melding med vedlegg; assert at `mediaType`, `caption`, `plaintextDigest` og filnavn ikke finnes utenfor chifferteksten. | TESTRESULT.md#dump | venter |
| test.att.no-new-cell | `…object-in-same-cell` | Tell celleinstanser før og etter et vedlegg; assert uendret. Assert at vedlegget har meldingens `membershipFingerprint`. | TESTRESULT.md#dump | venter |
| test.att.no-host-in-outer | `…no-sender-side-fetch` (anti) | Inspiser ytre konvolutt og manifest: ingen vertsnavn, URL eller scaffold-id. Hent vedlegg i en oppsett-test der partene har hver sin resolver-rute. | TESTRESULT.md#e2e | venter |
| test.att.dump-opaque | `…operator-blind` | Scaffold-side dump av cellen; assert bare `attachmentID`, `byteLength`, chiffertekst. | TESTRESULT.md#dump | venter |
| test.att.claim-scan | `…no-unobservability-claim` (anti) | Søk i endrede docs/kontrakt etter «uobserverbar», «skjult størrelse», «untraceable» o.l.; listen skal være tom. | ACCEPT.md#claims | venter |
| test.att.expiry-together | `…expiry-together` | Sett klokken forbi `expiresAt`; assert at ytre rad, indre chiffertekst og vedleggsbytene alle er borte. | TESTRESULT.md#expiry | venter |
| test.att.close-kills-fetch | `…close-kills-fetch` | Start en henting, lukk cellen, fortsett; assert `cellClosed` og at ny henting avvises. | TESTRESULT.md#expiry | venter |
| test.att.transport-keyless | `…transport-keyless` (anti) | Kjør chunk-laget med nøkkelleverandøren fjernet; overføringen skal fullføre og hver chunk verifiseres på chiffertekst-digest. | TESTRESULT.md#chunk | venter — kjøres først etter S5 |
| test.att.constant-memory | `…constant-memory` | Mål toppminne hos scaffold og klient for 10 / 100 / 1000 MB; assert flat kurve. | TESTRESULT.md#chunk-memory | venter — kjøres først etter S5 |
| test.att.resume | `…resume` | Avbryt ved ~40 %; gjenoppta; assert at bare resterende chunks sendes og at digest stemmer til slutt. | TESTRESULT.md#chunk | venter — kjøres først etter S5 |
| test.att.ttfb | `…ttfb` | Mål tid til første byte for 1 MB og 1 GB; assert innenfor margin oppgitt i PLAN.md. | TESTRESULT.md#ttfb | venter — kjøres først etter S5 |
| test.att.suite-roundtrip | `…streaming-crypto-suite` | Forsegl og åpne et flerchunk-objekt med `attachmentStreamV1`; assert felles innholdsnøkkel, unik nonce per chunk, og at klartekst-digest stemmer. | TESTRESULT.md#chunk | venter |
| test.att.suite-tamper | `…streaming-crypto-suite` | Endre én byte i én chunk; assert at åpningen feiler på nøyaktig den chunken og at ingen klartekst returneres. Fjern én chunk; assert at kuttet oppdages (chunk-teller i AAD). | TESTRESULT.md#chunk | venter |
| test.att.suite-no-size-cap | `…streaming-crypto-suite` | Forsegl og åpne 1 GB gjennom suiten alene, uten wire-laget; assert konstant minnebruk og ingen hardkodet grense i formatet. | TESTRESULT.md#chunk-memory | venter |
| test.att.one-message-only | `…manifest-in-inner` | Forsøk å referere samme `attachmentID` fra en andre melding; assert avvisning. | TESTRESULT.md#auth | venter |
| test.att.grants-exactly-two | `…grants-exactly-two` | Diff `externalAgreementTemplate` v0→v1; assert nøyaktig to nye grants og uendret `neverGranted`. | ACCEPT.md#grants | venter |
| test.att.no-fs-right | `…no-fs-right` (anti) | Inspiser MCP-verktøyskjema: ingen `path`/`file_path`-parameter; kjør MCP-prosessen uten lesetilgang til hjemmemappen og assert at attach fortsatt virker. | TESTRESULT.md#auth | venter |
| test.att.fetch-only-addressed | `…fetch-only-addressed` | Hent vedlegg på en melding adressert til en annen; assert `grantNotHeld`. | TESTRESULT.md#auth | venter |
| test.att.gated-on-s5 | `…no-attachments-on-plaintext-path` (anti) | Kjør attach mot HTTP-adapteren; assert avvisning. Assert at MCP-en ikke annonserer attach-verktøyene før den er celleklient. | TESTRESULT.md#auth | venter |
| test.att.e2e | `…root` | Send et ekte vedlegg til `victoria-lille-robot`; hent det tilbake; assert `plaintextDigest`-match og at operatørdumpen er opak. | TESTRESULT.md#e2e | venter |

## 6. Åpne spørsmål til Kjetil

**Alle tre besvart av Kjetil 4. september 2026.**

1. **Bindingen mellom vedlegg og melding** → *bundet til nøyaktig én melding.* Manifestet i det indre konvoluttet er eneste adresse. Vedlegget arver meldingens medlemskap, retensjon og utløp. Ny test: `test.att.one-message-only`.

2. **Rekkefølge mot S5** → *lås i kontrakten nå, bygg wire-laget etter S5.* `…chunked.transport-keyless`, `…constant-memory`, `…resume` og `…ttfb` står som kontraktkrav med status «låst», og testene deres kjøres først når MCP-en er celleklient.

3. **Krypteringssuiten** → *ny `attachmentStreamV1` nå.* Ikke engangsforsegling med tak.

**Konsekvens av 2 og 3 sammen — verdt å se før G1.** De to svarene deler gren 4 i to lag som er uavhengige, og det er nettopp det som gjør kombinasjonen mulig:

- **Kryptolaget** (`attachmentStreamV1`) bor i `CellProtocol/Sources/CellBase/Crypto/`. Det har ingen MCP-avhengighet og ingen scaffold-avhengighet — det forsegler og åpner en bytestrøm i minnet mot `IdentityVault`. Det kan bygges og enhetstestes i denne oppgaven, i dag, uten at S5 er ferdig. Det er derfor `test.att.suite-*` står `venter` og ikke `blocked`.
- **Wire-laget** (chunk-adressering, gjenopptagelse, TTFB) trenger en klient som snakker celle-actions. Den finnes ikke før S5.

Det som forsvinner med svar 3: 8 MB-taket, og hele behovet for å merke gren 4 «planlagt, ikke implementert» i kontrakten — formatet blir størrelsesuavhengig fra v1, det er bare transporten som kommer senere. Det er en bedre tilstand å dokumentere, fordi kontrakten da beskriver noe som faktisk finnes.

**Én ny konsekvens jeg vil ha frem før G1:** en strømmende suite endrer hva `ciphertextSize` i det ytre konvoluttet betyr for vedlegg. Med per-chunk-forsegling ser operatøren *antall chunks og størrelsen på hver*, ikke bare en totalsum. Det er ikke verre enn i dag i praksis, men det er en ny observerbar detalj, og den skal stå i kontraktens `operatorVisibility.canSee` — ikke oppdages senere. Fanget som `test.att.claim-scan`.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-04 | Opprettet | Losen |
| 1 | 2026-09-04 | §1 omformet etter lesing av `correspondence_cell_contract_v0.json`: modell B endret fra «egen celle i avsenders scaffold + egen Agreement» til «forseglet objekt i samme relasjonscelle, adressert fra det indre konvoluttet». Grunn: konvolutten gir allerede operatørblindhet, så en egen celle kjøper ingenting — og den ville brutt `hosting.constraint` ved å forutsette at mottaker når avsenders scaffold. Kontrakt-lesing avdekket også at `seal/open` er engangs, som gjør chunk-grenen til kryptoarbeid, ikke transportarbeid. | Losen |
| 2 | 2026-09-04 | Kjetil besvarte alle tre spørsmålene i §6: vedlegg bundet til én melding; chunk-transport låses i kontrakt og bygges etter S5; `attachmentStreamV1` bygges nå. Gren 4 delt i kryptolag (blad her) og wire-lag (låst). 8 MB-taket falt bort. Fire nye tester. | Losen |
