# Formålsspesifikasjon — entitetsnokler

Oppgavemappe: `PDD_entitetsnokler_2026-09-04` · Opprettet 2026-09-04 · Iterasjon 0 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Vi maa ha gode verktoy for aa legge inn nokler (som api nokler) i egen entitet. Det maa gjores en tilgjengelighetsvurdering men generelt bor nokler ligge i samme scaffold som der brukeren vil instansiere en AIGatewayCell.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| «nøkler bør ligge i samme scaffold som der brukeren vil instansiere en AIGatewayCell» — dette er *ikke* tilfelle i dag | retrieved | `Sources/App/Cells/WebKnowledge/WebKnowledgeCells.swift:186-190` — `ScopedCredentialRegistry` er `nonisolated(unsafe) private static var` ordbøker nøklet på `requester.uuid`, bak en `NSLock`. Prosessglobalt minne. |
| Cellen som holder legitimasjonen er allerede entitetsskopet og persistert | retrieved | `Sources/App/configure.swift:1228,1382` — `ScopedCredentialCell` registreres med `cellScope: .identityUnique, persistency: .persistant`. |
| …men cellens tilstand leser hemmeligheten fra den prosessglobale staticen, ikke fra egen persistert tilstand | retrieved | `WebKnowledgeCells.swift:759-773` — `stateValue(for:)` bygger `credentials` fra `ScopedCredentialRegistry.descriptors(for:)`. Ingenting skrives til cellens eget lager. |
| Cellen påstår i dag at hemmeligheten er eierskopet persistert | contradicted | `WebKnowledgeCells.swift:766` — `"secretPersistence": .string("owner_scoped_cell_in_v1")`. Det er planlagt oppførsel dokumentert som implementert (`lesson.planned-documented-as-implemented`). |
| Fallback finnes: Keychain, så env, bak `AI_GATEWAY_ALLOW_LEGACY_SECRET_FALLBACK` | retrieved | `Sources/App/Cells/AI/AIGatewayCell.swift:3347`, `AIGatewaySupport.swift:591-640`. |
| Keychain-stien finnes ikke i containeren | retrieved | `AIGatewaySupport.swift:594-600` — `supportsPersistentStorage` er `#if canImport(Security)`, altså `false` på Linux. Prod/staging har derfor ingen persistent nøkkelsti i dag. |
| `CELL_SCAFFOLD_RUNTIME_SECRET_DIRECTORY` kan bære krypteringsnøkkelen | **unavailable** | Nevnt i `Documentation/Staging_Deployment.md`, men `grep` i `Sources/` gir null treff. Den er en vertskonfigurasjon, ikke noe koden leser i dag. Kan ikke bære vekt før den er verifisert. |
| Nøkkelen resolves i det hele tatt i dag (legacy-sti) | retrieved | Kjøring 2026-09-04 05:31Z: `AIInvokeStarted … provider=openai` → `AIInvokeFailed … quotaStatus=providerQuotaExceeded`. Nøkkelen ble funnet og brukt; leverandøren avviste på kvote. |


## 1. Formålstre

Kjernen i én setning: **cellen som holder nøkkelen er allerede entitetsskopet og persistert — hemmeligheten er det ikke.** Den ligger i en prosessglobal static og dør ved omstart.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.entitetsnokler.root` | En nøkkel hører til entiteten som bruker den | `purpose://skeleton.owner-entity-access` | Eieren legger inn en nøkkel én gang, og den er der neste gang scaffoldet starter — uten env, uten Keychain, uten å legges inn på nytt | Restart-test, se `test.nokkel.overlever-omstart` | candidate |
| `purpose://candidate.entitetsnokler.secret-in-cell-state` | Hemmeligheten ligger i cellens egen persisterte tilstand | root | `ScopedCredentialCell` skriver hemmeligheten til sitt eget eierskopede lager; `ScopedCredentialRegistry` er ikke lenger sannhetskilde for hemmeligheter | Legg inn nøkkel → restart → `credential.upsert`-aliaset resolver fortsatt | candidate |
| `purpose://candidate.entitetsnokler.encrypted-at-rest` | Kryptert på hvile | root | Nøkkelen står ikke i klartekst noe sted på disk | `grep` etter nøkkelen i cellelageret gir null treff etter innlegging | candidate |
| `purpose://candidate.entitetsnokler.access-scope-explicit` | Tilgangsskopet er eksplisitt og fail-closed *(tilgjengelighetsvurderingen)* | root | Det er skrevet ned hvilke requestere og hvilke celler som når et alias, og en AIGatewayCell instansiert utenfor skopet får **ingen** nøkkel — ikke en stille fallback til vertens env | Negative tester: feil requester, feil scaffold, ukjent alias | candidate |
| `purpose://candidate.entitetsnokler.entry-surface` | Innlegging er en flate, ikke en env-variabel | root | Eieren kan legge inn, se hvilke aliaser som finnes, og fjerne — uten terminal | Rendret bilde godkjent (G1-GUI), deretter klikketest | candidate |
| `purpose://candidate.entitetsnokler.never-readable` | Nøkkelen kan ikke leses tilbake | root | Ingen keypath returnerer hemmeligheten; bare `hasSessionSecret`-formen | Kontrakttest: hvert lesende keypath inspiseres for hemmelighetslekkasje | candidate |
| `purpose://candidate.entitetsnokler.state-claims-are-true` | Cellen påstår bare det den gjør | root | `security.secretPersistence` beskriver faktisk lagring, i samme endring som lagringen endres | Inspeksjon: strengen mot implementasjonen | candidate |
| `purpose://candidate.entitetsnokler.container-parity` | Virker der det skal virke | root | Stien virker på Linux i containeren, der `canImport(Security)` er falsk | CI-bygg + test på Linux | candidate |
| `purpose://candidate.entitetsnokler.provider-refusal-is-distinct` | «Ingen nøkkel» og «leverandøren nektet» er to forskjellige svar | root | Flaten skiller de to; i dag gir begge samme deterministiske fallback | Fremtvunget kvotefeil vs. manglende alias gir ulik tilstand | candidate |


Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.
Hvert bladformål skal ha en test i §5. Et formål uten observerbart Goal er ikke klart til arbeid.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en generell hemmelighetsforvalter for HAVEN. Skopet er legitimasjon en entitet bruker mot en ekstern leverandør gjennom AIGatewayCell.
- Ikke en endring av leverandørmotoren i `AIGatewayCell`. Rutevalg, kvote og prising røres ikke.
- Ikke en løsning på kvoteproblemet som stoppet den kapable kjøringen 2026-09-04. Det er din OpenAI-konto, ikke koden.
- Ikke fjerning av legacy-fallbacken i denne omgang — men §6 spør om den skal dø når dette lander.

| Kapabilitet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| Persistert, entitetsskopet celle | `configure.swift:1228,1382` | Cellen persisteres; hva den persisterer bestemmer vi | ja |
| `credential.upsert` / `remove` / `clear` | `WebKnowledgeCells.swift:41-46` | Keypathene finnes; de skriver i dag til en static | ja |
| Kryptering på hvile | **ingen kilde** | `CELL_SCAFFOLD_RUNTIME_SECRET_DIRECTORY` finnes ikke i `Sources/`. Krypteringsnøkkelens hjem er et åpent spørsmål, §6 | ja — blokkerer `encrypted-at-rest` |
| Lokal modell for testing uten leverandørkvote | llama-server 8083, Qwen3-8B | Kjørte grønt 2026-09-04 | nei, men gjør testing billig |


## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2.
**GUI-oppgave:** hver flate og hver viktig tilstand (tom, fylt, feil) må ha et rendret bilde i `images/` som Kjetil har godkjent før G1-GUI. Porthole-preview av skeleton-JSON når formatet tillater det; ellers mockup med eksplisitt liste over hva dagens skeleton ikke kan rendre.
| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Innleggingsflaten, tre tilstander: tom, ett alias lagret, feil (leverandøren nektet) | bilde | `images/nokkelflate-{tom,lagret,feil}-v1.png` | settes ved G1-GUI | nei |
| Nøkkelen overlever omstart | testutdata | `TESTRESULT.md#overlever-omstart` | — | nei |
| Nøkkelen finnes ikke i klartekst på disk | testutdata | `TESTRESULT.md#kryptert` | — | nei |
| Tilgangsskopet, med negative tester | testutdata | `TESTRESULT.md#auth` | — | nei |
| Kjørende flate i Porthole på et lokalt scaffold | kjørende flate | `http://127.0.0.1:9101/porthole` | — | nei |
| Tilgjengelighetsvurderingen som eget dokument | fil | `TILGANGSSKOP.md` i denne mappa | — | nei |


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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance
- purpose://scaffold.operations [candidate] — Scaffold operations

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
| 0 | 2026-09-04 | Opprettet | Losen |

## 5. Avledede tester

| test | type | purposeRef | Hvordan | Evidens lander |
|---|---|---|---|---|
| `test.nokkel.overlever-omstart` | command | secret-in-cell-state | Legg inn alias via `credential.upsert` mot lokalt scaffold, stopp serveren, start den igjen, kall `ai.invoke` med samme alias | `TESTRESULT.md#overlever-omstart` |
| `test.nokkel.ikke-i-klartekst` | inspection | encrypted-at-rest | `grep -r "<nøkkelen>"` i cellelageret etter innlegging; skal gi null treff | `TESTRESULT.md#kryptert` |
| `test.nokkel.auth-negativ` | command | access-scope-explicit | Feil requester, feil scaffold, ukjent alias, `purpose://prompt.unknown` — alle skal avvises, ingen skal falle tilbake til vertens env | `TESTRESULT.md#auth` |
| `test.nokkel.aldri-lesbar` | inspection | never-readable | Gå gjennom hvert lesende keypath på cellen og vis at hemmeligheten ikke er i responsen | `TESTRESULT.md#lekkasje` |
| `test.nokkel.paastand-stemmer` | inspection | state-claims-are-true | `security.secretPersistence`-strengen mot faktisk lagring | `ACCEPT.md#docs` |
| `test.nokkel.linux` | command | container-parity | CI-bygg og suite på Linux, der `canImport(Security)` er falsk | `TESTRESULT.md#build` |
| `test.nokkel.nektelse-vs-mangel` | measurement | provider-refusal-is-distinct | Tving kvotefeil (kjent tilstand i dag) og manglende alias; vis at flaten sier to forskjellige ting | `TESTRESULT.md#nektelse` |
| `test.gui.reference-image-exists` | artifact | entry-surface | Bilde per tilstand godkjent før kode | `images/` |
| `test.gui.parity` | inspection | entry-surface | Referanse mot faktisk, side om side | `ACCEPT.md#parity` |
| `test.build`, `test.regression` | command | pkg.std.everything-works | `swift build --build-tests` og `ci/run-tests.sh` (alle tolv bolker) | `TESTRESULT.md#build`, `#regression` |

Merk: `ci/run-tests.sh` i sin helhet, ikke et håndplukket utvalg. Å plukke suiter for hånd er nettopp feilen som slapp `PortholeMenuFallbackTests` gjennom til CI 2026-09-03.

## 6. Åpne spørsmål som endrer treet

1. **Hvor bor krypteringsnøkkelen?** `CELL_SCAFFOLD_RUNTIME_SECRET_DIRECTORY` står i `Staging_Deployment.md`, men finnes ikke i `Sources/`. Uten et svar kan ikke `encrypted-at-rest` få en verifier, og da er formålet ikke klart til arbeid. Alternativer: (a) scaffoldets eksisterende vault-/identitetsmekanikk, (b) en fil i runtime-secret-katalogen som vertsoppsettet allerede lover, (c) eierens egen nøkkel, som gir «låst til eieren logger inn» — det var alternativ 3 du valgte bort.
2. **Skal legacy-fallbacken dø når dette lander?** I dag er `AI_GATEWAY_ALLOW_LEGACY_SECRET_FALLBACK=true` det som får den lokale kjøringen til å virke. Når nøkkelen kan bo i entiteten, er env-stien en bakvei som gjør tilgangsskopet uekte.
3. **Deler entiteter aliaser innenfor et scaffold, eller er alias strengt per entitet?** Dette er selve tilgjengelighetsvurderingen, og svaret endrer både datamodellen og de negative testene.

## 7. Iterasjoner

| # | Dato | Hva endret seg |
|---|---|---|
| 0 | 2026-09-04 | Første utkast. Bygget på kodelesing samme morgen, ikke på hukommelse. |
