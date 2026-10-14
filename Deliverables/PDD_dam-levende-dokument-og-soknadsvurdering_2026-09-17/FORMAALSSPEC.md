# Formålsspesifikasjon — dam levende dokument og soknadsvurdering

Oppgavemappe: `PDD_dam-levende-dokument-og-soknadsvurdering_2026-09-17` · Opprettet 2026-09-17 · Iterasjon 1 (ikke godkjent — venter G1)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Funksjonaliteten i dette artefaktet må du definere i CellProtocol og implementere i CellScaffold. Vi skal kombinere dette med argumentanalyse og formålsdekomponering slik at vi kan pakke det som et produkt. Bruk det du har av rådgivere, dokumentasjon og implementasjon til å beskrive dette som et produkt og steg til å ha det som et ferdig produkt. Start en ny tråd i Damm prosjektet for dette. Vi skal vise dem akkurat dette.

Presisering fra Kjetil samme dag: «Det viste seg at det var med en m. Her er link: https://www.dam.no vi skal se om vi kan bruke vår funksjonalitet for å virdere kvaliteten i søknader.»

| Påstand i intensjonen / antatt kapabilitet | Audit (retrieved / recalled / unavailable / contradicted) | Kilde |
|---|---|---|
| «Dette artefaktet» er Claude-dokumentet «Vedtekter for Norsk tårntitterforening (utkast)», med funksjonene F1–F10 | retrieved (observert i bruk 2026-09-17) | BRIEF.md §2; https://claude.ai/code/artifact/3615ce25-e770-43db-8b78-602b9cb477a7 |
| Funksjonaliteten finnes ikke allerede som celle i CellScaffold | unavailable (rask skanning fant ingen dokumentcelle med ankrede kommentarer, revisjoner og pending-seksjoner; ikke dybdeverifisert) | BRIEF.md §5 |
| HAVEN har argumentanalyse | retrieved (kontrakt + referanseverktøy + v0 runtime-modell) | Book/27_Text_Reliability_Analysis.md; Book/29_Claim_Argument_Model.md; CellProtocol::Sources/CellBase/PurposeAndInterest/ClaimComposition.swift |
| HAVEN har formålsdekomponering | retrieved (kunnskapsbase, resolver-celle, PDD-verktøy) | Book/23_Purpose_Knowledge_Base.md; Book/35_Purpose_Driven_Development_Workflow.md; CellScaffold::Sources/App/Support/PurposeDecomposition.swift |
| HAVEN har rådgivere som kan brukes | retrieved (metode og tidligere panelkjøringer), men `cell:///AdvisorPanel` er ikke ferdig i drift | Book/30_Panel_Task_Decomposition_Workflow.md; CellScaffold::Deliverables/PDD_radgiverpanel-og-persona_2026-09-05/ |
| «Dem» = Stiftelsen Dam, og bruken er vurdering av søknadskvalitet | retrieved (Kjetils presisering) | https://www.dam.no |
| Dam tillater bruk av KI i søknadsvurdering | contradicted for fagutvalg Helse: KI er forbudt i selve vurderingen og ved opplasting av søknadstekst, men tillatt for å forbedre egen tilbakemelding. Forskningsinstruksen nevner ikke KI. | https://www.dam.no/instruks-fagutvalg-helse/; https://www.dam.no/instruks-fagutvalg-forskning/ (hentet 2026-09-17) |
| Vurdering av søknader hos Dam har et reelt kvalitetsproblem produktet kan adressere | retrieved: Dam oppgir 15–20 prosent svært store avvik (≥ 2 karakterer) mellom vurderere | https://www.dam.no/feil/ |

## 1. Formålstre

Metoden (Kjetils presisering 2026-09-12): *at noe skal finnes* er ett formål; *hva det skal løse* er andre formål. Derfor er treet delt i to greiner: **1A Problemformål** (hva produktet skal løse, grunnlagt i Dams egne publiserte tall og regler) og **1B Produktformål** (hva som skal finnes for å løse dem). Løsningen velges som den som best oppfyller 1A.

### 1A. Problemformål — hva produktet skal løse

| purposeRef | Tittel | Forelder | Goal (outcome) | successSignals | Verifier | Status |
|---|---|---|---|---|---|---|
| `purpose://candidate.dam-soknadskvalitet.root` | Kvalitet i søknader til Stiftelsen Dam | `purpose://digital-work` | En søker og en søkerorganisasjon kan se, før innsending, hvor søknaden svikter mot Dams egne kriterier — uten at noen maskin vurderer søknaden på Dams vegne. | (1) Søker kan navngi minst én konkret svakhet hen ikke så selv; (2) ingen karakter er satt av produktet; (3) ingen søknadstekst er sendt til Dam-eksterne systemer uten søkers eget valg. | Demo på syntetisk søknad + §3 forventningskontrakt | candidate |
| `purpose://candidate.dam-soknadskvalitet.fewer-wasted-applications` | Færre bortkastede søknader | root | Søker får et begrunnet svar på «passer dette prosjektet dette programmet nå?» **før** søknaden skrives. | Egnethetssjekken peker på hvilket kriterium som ikke er dekket, med sitat fra Dams egen programtekst; søker kan velge bort å søke. | `test.egnethet.begrunnet-frarading` | candidate |
| `purpose://candidate.dam-soknadskvalitet.criteria-coverage` | Søknaden svarer på det Dam faktisk måler | root | Hvert av Dams fire kriterier (Soliditet, Virkning, Gjennomføring, Stiftelsens prioriteringer) har en identifiserbar dekning i teksten, og argumentkjeden behov → mål → metode → plan → budsjett → virkning er hel. | Kriterier uten dekning er navngitt; brutte ledd i kjeden er navngitt med sitat. | `test.kriterier.dekning`, `test.argument.brutt-ledd` | candidate |
| `purpose://candidate.dam-soknadskvalitet.reader-for-everyone` | En ekstra leser for alle søkere | root | Dams eget søketips «Få noen til å lese søknaden» blir tilgjengelig også for organisasjoner uten rådgiverressurs. | En ekstern leser (menneske eller agent) kan inviteres inn i dokumentet, kommentere ankret på passasje, og søker beholder eierskap og siste ord. | `test.leser.invitasjon-og-ankring` | candidate |
| `purpose://candidate.dam-soknadskvalitet.rules-respected` | Ingen regelbrudd hos Dam | root | Produktet kan ikke brukes til å bryte Dams instruks av 12.08.2026: ingen KI i selve vurderingen, ingen søknadstekst inn i KI-verktøy på vurdererens side. | Vurderersnittet (B) stopper tekst som ser ut som sitat fra en søknad; ingen flate i produktet viser en foreslått karakter. | `test.personvern.sitatvakt`, `test.ingen-karakter` | candidate |
| `purpose://candidate.dam-soknadskvalitet.feedback-quality` | Vurdererens egen tilbakemelding blir bedre (snitt B, betinget) | root | Vurdererens **eget utkast** måles mot kriteriene og skalabeskrivelsene, uten at søknadstekst går inn. | Utkastet får konkrete funn: «ingen konkret styrke under Virkning», «vurderende ord uten kobling til skalabeskrivelsen». | `test.tilbakemelding.kriteriedekning` | candidate — **avventer Kjetils valg (§6 Q1) og skriftlig bekreftelse fra Dam** |
| `purpose://candidate.dam-soknadskvalitet.no-wrongful-discouragement` | Ingen uriktig fraråding | fewer-wasted-applications | Et godt prosjekt skal aldri frarådes av produktet, og «vet ikke» skal være et gyldig svar. | Andel gode syntetiske prosjekter som frarådes er under terskel; hver fraråding har begrunnelse et menneske kan etterprøve. | `test.egnethet.ingen-uriktig-fraading` | candidate |
| `purpose://candidate.dam-soknadskvalitet.source-versioning` | Riktig og datert kildegrunnlag | criteria-coverage | Anbefalinger bygger på den utlysnings- og instruksversjonen som gjaldt, og blir merket utdatert når Dam endrer teksten. | Hver anbefaling bærer versjon og hentedato; endret kilde gir merking, ikke stille feil råd. | `test.utlysning.versjon` | candidate |
| `purpose://candidate.dam-soknadskvalitet.recipient-fit` | Begrunnelsen kommer fram dit den skal | criteria-coverage | Innholdet får plass i Damnetts faktiske felt. Dam sier at lenker i fritekstfelt ikke er del av vurderingsgrunnlaget, så et råd som ender i en lenke er ikke levert. | Eksporttest mot feltstruktur og tegngrenser | `test.eksport.mottakerfelt` | candidate |
| `purpose://candidate.dam-soknadskvalitet.access-revocation` | Tilgang kan tas tilbake | reader-for-everyone | Søker ser hvem som har tilgang, kan trekke den tilbake, og kan slette. Gjelder både mennesker og agenter. | Revokasjon virker umiddelbart; logg viser hvem som hadde tilgang når | `test.tilgang.revokasjon` | candidate |
| `purpose://candidate.dam-soknadskvalitet.disagreement-visible` | Uenighet mellom vurderere blir synlig (snitt C) | root | Der to vurderere spriker med ≥ 2 karakterer, kan de se hvilke påstander de leser ulikt. | — | — | **utenfor denne leveransen** (krever at Dam endrer egen regel 1; se §2) |

### 1B. Produktformål — hva som skal finnes

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Test (§5) |
|---|---|---|---|---|---|
| `purpose://candidate.dam-soknadskvalitet.living-document` | Levende søknadsdokument (F1, F2, F4, F9) | criteria-coverage | Dokumentet fødes med formålsseksjon og tomme, navngitte seksjoner; hver endring har revisjon; menneskets endring vinner over agentens. | Celle med `draft`/`version`-kontrakt og konfliktregel | `test.menneske-vinner`, `test.skjelett-foedsel` |
| `purpose://candidate.dam-soknadskvalitet.anchored-comments` | Ankrede kommentarer (F5) | reader-for-everyone | En kommentar peker på nøyaktig passasje og overlever redigering av teksten rundt. | Ankeret løser til samme span etter endring | `test.ankring` |
| `purpose://candidate.dam-soknadskvalitet.criteria-purpose-pack` | Dams kriterier som formålspakke | criteria-coverage | Dams fire kriterier og skalabeskrivelsene 1–7 finnes som formålsnoder med successSignals, sitert fra dam.no med hentedato. | Pakkefil + validator | `test.kriterier.dekning` |
| `purpose://candidate.dam-soknadskvalitet.argument-analysis` | Argumentanalyse som celle | criteria-coverage | Påstander, kildegrunning og argumentgraf hentes ut av teksten **deterministisk**, uten språkmodell og uten å skrive om teksten. | Kjøring gir samme resultat to ganger på samme tekst | `test.analyse.determinisme`, `test.argument.brutt-ledd` |
| `purpose://candidate.dam-soknadskvalitet.fit-check` | Egnethetssjekk før skriving | fewer-wasted-applications | Prosjektidé (ikke søknadstekst) dekomponeres mot program og kriterier og gir «søk / styrk X først / søk et annet program», med sitat fra Dams tekst. | Kjøring på tre syntetiske ideer | `test.egnethet.begrunnet-frarading` |
| `purpose://candidate.dam-soknadskvalitet.privacy-guard` | Personvernvakt og sitatvakt | rules-respected | Tekst som ser ut som helseopplysning om enkeltperson, navn, eller sitat fra en søknad blir markert og stoppet før den forlater brukerens flate. | Negative tester på syntetiske tekster | `test.personvern.sitatvakt` |
| `purpose://candidate.dam-soknadskvalitet.no-score` | Produktet setter aldri karakter | rules-respected | Ingen utdata inneholder en tallkarakter, en anslått karakter eller en rangering av søknaden. | Skjemaskann av all utdata | `test.ingen-karakter` |
| `purpose://candidate.dam-soknadskvalitet.trust-package` | Tillitspakke ved bruk | rules-respected | Før kjøring ser brukeren hvilke modeller/rettigheter som brukes og hva som sendes hvor; etterpå kan det etterprøves. | `cell:///AgentTrustPackage`-projeksjon | `test.tillit.foer-og-etter` |
| `purpose://candidate.dam-soknadskvalitet.external-reader-sync` | Synk med ekstern leser (F6, F7) | reader-for-everyone | Innspill fra en invitert leser eller agent kommer inn i riktig seksjon, merket med opphav, uten å overskrive menneskets endringer. | Correspondence-kontrakt (Book 33), hendelsesbasert | `test.leser.invitasjon-og-ankring` |
| `purpose://candidate.dam-soknadskvalitet.export` | Eksport og deling (F10) | criteria-coverage | Søknaden kan eksporteres til formatet den skal inn i, uten tap av struktur; deling styres av søker. | Eksporttest med sammenligning | `test.eksport.tapsfri` |

**Erklærte bortvalg** (etter Astras validering): F3 «kildegrunnet innhold» er i denne omgang redusert til *å markere manglende eller usjekket kilde* — produktet henter og verifiserer ikke kilder. F8 «åpne spørsmål som sjekkliste» og F9 «norm skilt fra forklaring» er egenskaper ved dokumentflaten som først får egne formål hvis Kjetil vil ha dem inn; de er ikke smuglet inn i `living-document` uten test.

Åpne spørsmål som *endrer treet* står i §6. Noder merket «utenfor denne leveransen» skal ikke planlegges i G2.

## 2. Avgrensning og avhengigheter

**Hva dette IKKE er:**
- Ikke et verktøy som vurderer søknader på Dams vegne. Dams instruks for fagutvalg Helse og Utvikling (endret 12.08.2026) forbyr KI i selve vurderingen; produktet setter aldri karakter og rangerer ikke.
- Ikke et verktøy som skriver søknadsteksten. Analysen peker på svakheter i brukerens egen tekst; den omskriver ikke (Book 27s eget designvalg).
- Ikke en integrasjon i Damnett, og ingen behandling av ekte søknadstekst i denne leveransen. Alle demoer bruker tydelig merket syntetisk tekst.
- Ikke snitt C (argumentkart for Dams vurderere). Det krever at Dam endrer regel 1 og skal ikke tilbys før Dam selv tar opp uenighet mellom vurderere.
- Ikke en juridisk avklaring. GDPR-, AI Act- og EØS-spørsmål er listet som *det som må avklares*, ikke som avklart.

**Kapabiliteter og avhengigheter (hver med kilde, hva den ikke dekker, og verifisert dato):**

| Kapabilitet | Kilde (relativ sti) | Avgrensning | Verifisert |
|---|---|---|---|
| Deterministisk argument- og kildeanalyse | `CellProtocolDocuments::Tools/TextReliability/text_reliability.py` (1363 linjer) | v1 heuristikk, henter ikke kilder, kaller ingen språkmodell; dyp argumentrekonstruksjon krever menneske eller modell | Kjørt 2026-09-17 på syntetisk søknad → `demo/syntetisk_soknad_v1.analysis.md` |
| Påstands- og argumentmodell i runtime | `CellProtocol::Sources/CellBase/PurposeAndInterest/ClaimDefinition.swift`, `ClaimComposition.swift`, `ClaimScheme.swift` + `Tests/CellBaseTests/Claim*Tests.swift` | v0 runtime-modell, «draft chapter», ikke koblet til noen flate eller dokumentflyt | Book 29 «Last verified against code: 2026-07-03»; filer og tester finnes 2026-09-17 |
| Utkast og versjoner med hash | `CellScaffold::Sources/App/Cells/ProjectOperations/DraftVersionCell.swift` (505 linjer; `contentHash` ved commit, linje 280) | `draft.update` erstatter payload uten revisjonsvakt og uten menneske/agent-konfliktregel (linje 218); `version.compare` sier selv at semantisk diff ikke er implementert (linje 369). En hash er ikke et samarbeidssystem | Verifisert av Astra 2026-09-17 |
| Formålsdekomponering og resolver | `CellScaffold::Sources/App/Support/PurposeDecomposition.swift`, `ExecutablePurposeGrounding.swift`, `PurposeKnowledgeBase.swift`; Book 23/36 | Dams kriterier er ikke modellert som formål i dag | Lest 2026-09-17 |
| Tillitspakke | `CellProtocolDocuments::Book/36_Agent_Trust_Package.md`, `CellScaffold::Sources/App/Cells/AgentTrustPackage/` | Kapitlet sier selv: WP1–WP10 i lokal kode, **ikke** attest for deploy eller ende-til-ende-akseptanse | Lest 2026-09-17 |
| Correspondence (ekstern leser/agent) | `CellScaffold::Sources/App/Cells/Agent/AssistantCorrespondenceCell.swift` (signert send/list/read/ack) + `Tests/AppTests/AssistantCorrespondence*Tests.swift`; Book 33 | Cellen finnes og har tester; den dekker **meldinger**, ikke innfletting i et dokument, ankerflytting eller menneske-vinner. Én godkjenningsflate timet ut i august (`lesson.corr-approval-surfaces-timed-out`) — det gjelder den flaten, ikke alle baner | Verifisert av Astra 2026-09-17 |
| Rådgiverpanel som celle | `CellScaffold::Sources/App/Support/PurposeDecomposition.swift:1417` (paneldekomponering, roller, mål — `capabilityEndpoint: nil`) | **Ingen kjørende panelcelle.** Planstrukturen finnes; utføreren gjør ikke. Panelet i denne oppgaven ble kjørt som agenter | Verifisert av Astra 2026-09-17 |
| Gjenbruk før nye celler defineres | `Cells/WorkItems/WorkItemCell.swift:157` (kommentarlivssyklus uten passasjeanker), `Cells/MusicPublishing/MusicWorkspaceReviewCell.swift:188,375` (invitasjoner, roller, kommentar bundet til versjon), `Cells/Markdown/MarkdownRendererCell.swift:96` | Ingen av dem gir tekstspenn som overlever redigering. De er inngangsdata til S3/S4, ikke en ferdig løsning | Verifisert av Astra 2026-09-17 |
| F1–F10 «levende dokument» | Claude Docs (artefaktet) | **Ikke funnet** i søk 2026-09-17 over `CellScaffold/Sources` (323 filer under `Cells`, 33 under `Support`) og `CellProtocol/Sources`: ingen celle som kombinerer seksjonsmodell, stabile passasjeankre, samtidighetskontroll og menneske-vinner. Fravær i genererte mapper, worktrees og deploymiljø er ikke verifisert | Søk verifisert av Astra 2026-09-17 |

## 3. Forventningskontrakt — «Det du kommer til å se»

| # | Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|---|
| 1 | Produktbeskrivelse Kjetil kan vise Dam | fil + nettside | `Deliverables/PDD_dam-.../PRODUKT_Dam.md` + publisert artefaktside | — | nei |
| 2 | Steg til ferdig produkt med grafikk og eier per steg | fil + figur | `PRODUKT_Dam.md` §7 + artefaktsiden | — | nei |
| 3 | Denne formålsspesifikasjonen, klar for G1 | fil | `FORMAALSSPEC.md` | — | **til G1** |
| 4 | Bevis på hva som virker i dag: syntetisk søknad kjørt gjennom analysen | testutdata | `demo/syntetisk_soknad_v1.md`, `demo/syntetisk_soknad_v1.analysis.md` | kjørt 2026-09-17 | ja (foreligger) |
| 5 | Referansebilder, søknadsflaten: tom / fylt / funn | bilde | `images/soknad-<tilstand>-v1.png` | etter G1 | nei (G1-GUI) |
| 6 | Referansebilde, egnethetssjekk før skriving | bilde | `images/egnethet-v1.png` | etter G1 | nei (G1-GUI) |
| 7 | Referansebilde, personvern-/sitatvakt utløst | bilde | `images/vakt-utloest-v1.png` | etter G1 | nei (G1-GUI) |
| 8 | Referansebilde, tillitspakke før/etter kjøring | bilde | `images/tillit-v1.png` | etter G1 | nei (G1-GUI) |
| 9 | Kontrakter i CellProtocol (Book-kapittel + `*_contract_v0.json` + fixtures) | fil | CellProtocol/CellProtocolDocuments | etter G2 | nei |
| 10 | Celler i CellScaffold med tester grønne | kjørende kode | `CellScaffold::Sources/App/Cells/...` | etter G2 | nei |
| 11 | Kjørende flate i Porthole/Binding, paritet mot bilde | kjørende flate | scaffold | etter G2 | nei |

Rad 1–4 er det Kjetil kan vise Dam nå. Rad 5–11 er arbeid som krever G1, G1-GUI og G2.

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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://contact.communication [draft] — Contact and communication
- purpose://event.participation [draft] — Event participation
- purpose://event.privacy-preserving-networking [draft] — Privacy-preserving event networking
- purpose://digital-work [active] — Digital work
- purpose://governance [active] — Governance
- purpose://access.audit.privacy [active] — Access, audit and privacy
- purpose://questionnaire.access.audit [active] — Questionnaire access audit

## 5. Avledede tester (samlet)

Pakketestene fra §4 gjelder uendret. Tabellen under er skjerpet etter Astras validering 2026-09-17: hver test er formulert slik at den ikke kan bestås av en attrapp.

| testRef | Formål | Hvordan (skjerpet) | Evidens | Status |
|---|---|---|---|---|
| test.egnethet.begrunnet-frarading | fit-check | Fire tilfeller, ikke tre: (1) klart egnet prosjekt — skal **ikke** frarådes; (2) feil program; (3) manglende informasjon — svaret skal være «vet ikke, spør om X»; (4) uegnet prosjekt. Uavhengig fasit avgjør om sitatet faktisk begrunner rådet. Et system som alltid svarer «styrk brukermedvirkning» skal feile. | TESTRESULT.md#egnethet | venter |
| test.egnethet.ingen-uriktig-fraading | no-wrongful-discouragement | På et korpus av syntetiske ideer med kjent fasit måles andelen gode prosjekter som frarådes. Terskel settes i PLAN.md; over terskel er rødt. | TESTRESULT.md#fraading | venter |
| test.kriterier.dekning | criteria-purpose-pack | Tre negative varianter: beholdt overskrift med irrelevant innhold; gyldig dekning flyttet til en annen seksjon; slettet seksjon. Riktig status i alle tre. Pakken sjekkes også mot hele den daterte utlysningsteksten. | TESTRESULT.md#kriterier | venter |
| test.argument.kontrollpunkter | argument-analysis | Analysen skal produsere setnings- og seksjonsankrede kontrollpunkter med sitat, og **ikke** påstå at argumentkjeden er hel eller brutt. En utdata som hevder en faglig slutning uten menneskelig bekreftelse er rødt. (Erstatter `test.argument.brutt-ledd`: dagens graf bygger på seksjonsrekkefølge, ikke på slutninger — `text_reliability.py:772`.) | TESTRESULT.md#argument | venter |
| test.analyse.determinisme | argument-analysis | Kanonisk resultatdel (funn, ankre, statuser) med algoritme- og policyversjon bundet inn gir identisk digest; tidsstempler holdes utenfor digesten. En relevant endring i policy eller algoritme **skal** endre digesten. `analysis_id` alene teller ikke (den hashes i dag fra inputsammendraget, `text_reliability.py:1113`). | TESTRESULT.md#determinisme | venter |
| test.ingen-karakter | no-score | Semantisk, ikke ordskann: utdata skal verken inneholde tall på 1–7-skalaen anvendt på søknaden, skalabeskrivelsens ord brukt som dom («fremragende søknad»), fargekoding som rangerer, eller sannsynlighet for innvilgelse. Sitert regeltekst fra Dam skal ikke gi falskt rødt. | TESTRESULT.md#ingen-karakter | venter |
| test.personvern.sitatvakt | privacy-guard | Måles med feilrater på et korpus: ordrette sitat, parafraser, indirekte identifikatorer og ren egen tekst. Vakten kan ikke avgjøre opphav — den skal derfor varsle og stoppe, ikke påstå at noe er kopiert. I tillegg dataflyttest: hva forlot maskinen, målt utenfor produktet selv. | TESTRESULT.md#vakt | venter |
| test.menneske-vinner | living-document | Begge ankomstrekkefølger (agent før og etter menneske), forsinket agentsvar mot nyere menneskeendring, gammel base, og reload. Menneskets tekst står i alle; agentens forslag er bevart og synlig, ikke tapt. | TESTRESULT.md#konflikt | venter |
| test.skjelett-foedsel | living-document | Nytt dokument fødes med formålsseksjon og navngitte tomme seksjoner, **og** hver seksjon kan redigeres, lagres og gjenopptas etter reload uten tap. | ACCEPT.md#skjelett | venter |
| test.ankring | anchored-comments | Endring før, etter og **inne i** passasjen; duplikatsitat i samme dokument; flyttet passasje; slettet passasje. Tvetydighet gir eksplisitt uavklart anker — aldri stille ny plassering. | TESTRESULT.md#ankring | venter |
| test.leser.invitasjon-og-ankring | external-reader-sync | To ekte identiteter gjennom brukerens faktiske innvei (ingen testsnarvei), feil mottaker, tilbakekalt tilgang, duplikatmelding og forsinket innspill. Innspill merkes med opphav og overskriver ingenting. | TESTRESULT.md#leser | venter |
| test.tilgang.revokasjon | access-revocation | Tilbakekalt leser mister tilgang umiddelbart; sletting fjerner innhold og kopier; loggen viser hvem som hadde tilgang når. | TESTRESULT.md#tilgang | venter |
| test.tillit.foer-og-etter | trust-package | Ikke sirkulær: en uventet utgående destinasjon og en uinstrumentert bane injiseres. Testen er grønn bare hvis avviket eller den manglende dekningen blir synlig for brukeren. | TESTRESULT.md#tillit | venter |
| test.eksport.mottakerfelt | export | Mot Damnetts faktiske feltstruktur og tegnbegrensninger: innholdet må få plass i tillatte felt. Lenker i fritekst teller ikke som vurderingsgrunnlag hos Dam, så testen skal feile hvis begrunnelsen bare finnes i en lenke. Interne kommentarer og opphavsmerking skal **ikke** følge med i innsendt søknad. | TESTRESULT.md#eksport | venter |
| test.utlysning.versjon | source-versioning | Hver anbefaling bærer hvilken utlysnings-/instruksversjon og hentedato den bygger på; når kilden er endret, merkes anbefalingen som utdatert i stedet for å vises som gyldig. | TESTRESULT.md#versjon | venter |
| test.tilbakemelding.kriteriedekning | feedback-quality (betinget) | Krever **begge** porter: Kjetils valg i §6 Q1 og skriftlig bekreftelse fra Dam. Testen sammenligner med vurdererens ferdige original og feiler hvis det faglige innholdet er endret eller nye vurderinger er tilført. | TESTRESULT.md#tilbakemelding | blokkert av Q1 + Dam-bekreftelse |

Merknad til pakketesten `test.cells.capability-audit` (§4): den krever i dag at alle kapabilitetspåstander har status `retrieved`. Det kan belønne feilmerking. Her gjelder den skjerpede formen: hver avhengighet skal ha **riktig** auditstatus med belegg, og en sann negativ observasjon skal aldri skrives om til positiv.

## 6. Åpne spørsmål til Kjetil (bare de som endrer treet)

1. **Hvilke snitt går vi for?** Panelets anbefaling: **søkersiden (A) + egnethetssjekk før skriving (D)** som produkt nå; **B (vurdererens egen tilbakemelding)** bare som et *spørsmål* til Dam, ikke som tilbud; **C ikke nevnt** med mindre Dam selv tar opp uenigheten. Motsieren mener B er lite verdt og ligger i gråsonen til regel 2, og at C kan skade møtet. Sier du B skal med, blir `feedback-quality` et bladformål med egen flate og egen personvernvakt.
2. **Hvem er kunden?** Søkerorganisasjonen (som kvalitetssikrer mange søknader), den enkelte søkeren, eller Dam? Dette avgjør om `reader-for-everyone` betyr flerbruker-oversikt (rådgiver ser mange søknader) eller enkeltdokument. Rettferdighetsinnvendingen — at ressurssterke organisasjoner får mest ut av verktøyet — må ha et svar før møtet; et svar er at det tilbys gjennom søkerorganisasjonene og er gratis for små.
3. **Skal produktet kunne kjøre helt uten språkmodell som standard?** Analysen i dag er deterministisk (ingen modell). Hvis «ingen modell» er standard og modell er et valg brukeren tar, blir personvernargumentet mot Dams regel 2 vesentlig sterkere — men funnene blir grovere. Dette endrer `argument-analysis` og `privacy-guard`.
4. **Møtet hos Dam:** når, for hvem, og finnes en kontaktperson? Ukjent per 2026-09-17. Det avgjør hvor mye som må være rendret (G1-GUI) før møtet.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-17 | Opprettet | Losen |
| 1 | 2026-09-17 | §1 formålstre delt i problemformål (1A) og produktformål (1B) etter Kjetils formålsmetode; §2 avgrensning og avhengigheter med verifiserte stier og to negative funn (AdvisorPanel mangler i Sources, F1–F10 finnes ikke som HAVEN-celle); §3 forventningskontrakt; §5 tolv nye avledede tester; §6 fire åpne spørsmål. Grunnlag: rådgiverpanel med motsier, regulatorisk rådgiver og fire simulerte brukere; Dam-fakta hentet på nytt 2026-09-17 | Losen |
| 2 | 2026-09-17 | Motprøvd av Astra (`ASTRA_VALIDERING.md`). Endret: argumentgrafen er seksjonsrekkefølge, ikke slutninger — `test.argument.brutt-ledd` erstattet av `test.argument.kontrollpunkter`; determinismetesten bundet til kanonisk resultat, ikke `analysis_id`; fire nye problemformål (uriktig fraråding, kildeversjon, mottakerfelt, revokasjon); §2-rader korrigert for Correspondence, rådgiverpanel, DraftVersion og søkets rekkevidde; gjenbruksrad lagt til; alle §5-tester skjerpet mot attrapp-bestått; F3/F8/F9 erklært som bortvalg | Losen |
