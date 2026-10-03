# Formålsspesifikasjon — innholdsvern lyd 20260909

Oppgavemappe: `PDD_innholdsvern-lyd-20260909_2026-09-10` · Opprettet 2026-09-10 · Iterasjon 0 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Det bør som default være så umulig som det lar seg gjøre å laste ned en ukryptert
> lydfil - og dette skal virke både i app og web. […] jeg vil at vi skal gjøre det
> vanskelig å laste ned sangene om man ikke har blitt grantet read og store. […]
> sangen representerer et åndsverk som er eid av noen. Da er det vår oppgave å gi
> artister verktøy til å bestemme selv hvor trygt det skal være.

| Påstand / antatt kapabilitet | Audit | Kilde (relativ til CellScaffold) |
|---|---|---|
| Lyd ligger ubeskyttet i lagring | **RETTET 2026-09-10: bekreftet — lyd er IKKE kryptert.** Filene i prod begynner med `ID3`, altså vanlig MP3. Publiseringsløypa bruker `MusicAssetStoreCell.storeLocalAsset`, som skriver bytene slik de kommer og lar `encryptionPolicy` falle til `.none` | `MusicPublishingCells.swift:623-652`, `MusicReleasePipeline.swift:226`; verifisert med `od -c` på `/app/Database/MusicAssets/assets/music-full-*.bin` i prod |
| ~~Kryptering ved lagring finnes~~ | **min egen feil, rettet** — jeg leste `encryptionPolicy: .cellManaged, keyScope: .perTrack, chachaPoly` på `MusicPublishingCells.swift:943-958` og generaliserte til hele systemet. Den koden er ekte, men tilhører `MusicIngestCell.ingest` — en annen celle på en annen sti (`/mvp/ingest/local`, `VaporMusicPublishingMVP.swift:66`). Butterpop-publiseringen går aldri innom den. Dette er `lesson.bridge-inferred-architecture-from-one-use` begått av meg | `MusicPublishingCells.swift:817,905` |
| Manifestet forteller sannheten om kryptering | **contradicted, og det er en felle** — `storeLocalAsset` setter `ciphertextSHA256 = sha256(data)` og `plaintextSHA256 = sha256(data)`, altså samme verdi. Et felt som heter «ciphertext» inneholder hashen av klartekst. Det er dette som lurte meg | `MusicPublishingCells.swift:645,652` |
| Det finnes ikke noe vokabular for «hvor trygt» | **contradicted** — `MusicEncryptionPolicy {none, storageManaged, cellManaged}` og `MusicEncryptionKeyScope {none, perCell, perTrack, externalKMS}` finnes per spor | `Sources/App/Cells/MusicPublishing/MusicPublishingSupport.swift:64-75` |
| Skillet «høre» vs «beholde» må bygges fra bunnen | **contradicted** — `deliveryModes: [.progressive, .download]` er modellert, og `downloadEnabled` er `false` i `MusicTrackPolicy.default` | `MusicPublishingSupport.swift:279`, `:162,180` |
| HLS-segmentering finnes | **delvis, og verre enn det ser ut** — `MusicHLSVariant`, `hlsMasterPlaylistStorageKey`, `hlsSegmentStoragePrefix` finnes som *struct*, men ingen rute serverer m3u8 og `hlsVariants: nil` settes ved opprettelse. Null treff på `m3u8` i `Sources/App/Controllers` og `Public/js` | `MusicPublishingSupport.swift:94-99,282-284`; `MusicPublishingCells.swift:958` |
| Vernet holder helt fram til lytteren | **contradicted** — fila dekrypteres på serveren og sendes som klartekst. Ruta returnerer `data`, `mimeType` og `Content-Range`; det som lander i nettleseren er en vanlig lydfil | `Sources/App/Controllers/VaporButterpopStudio.swift:661-730` |
| Det finnes en terskel i dag | **retrieved, men lav** — kortlevd token, lease-cookie, rate limit på lease-lesning. Hever innsatsen, men gir ingen beskyttelse av selve bytene | `VaporButterpopStudio.swift:661-672` |

**HLS-funnet er en forekomst av `lesson.planned-documented-as-implemented`:** formen
finnes i structen, oppførselen finnes ikke. Den må ikke telles som halvferdig arbeid.

**Det ærlige taket, skrevet ned før noen lover noe:** lyd som kan høres, kan tas opp.
Widevine L3 brytes rutinemessig. Ingen av trinnene under fjerner det. Løftet til
artisten er derfor ikke «umulig», men *«det krever en bevisst teknisk handling å
bryte det, og du bestemmer selv hvor høy terskelen er»*.

## 1. Formålstre

Rot: `purpose://candidate.innholdsvern-lyd-20260909.root` — *En låt skal ikke kunne
hentes ut som spillbar fil av noen som bare har fått lov til å høre den, og artisten
skal kunne bestemme hvor høy terskelen er.*
Forelder i Book 23: `purpose://access.audit.privacy` (nærmeste; kandidat for egen
gren om «rettighetshaverens kontroll» ved P6).

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `…root` | Åndsverket forlater ikke huset som fil | `purpose://access.audit.privacy` | Den som har rett til å høre, får høre. Den som ikke har rett til å beholde, får ingen spillbar fil uten en bevisst teknisk handling | Hele kjeden testet fra produksjonsstien, ikke fra cellen | candidate |
| `…klartekst-forlater-aldri-serveren` | Klartekst forlater aldri serveren | `…root` | Ingen respons fra noen lyd-rute inneholder en spillbar, ukryptert lydfil for en lytter uten `store`-grant | Hent alt ruta gir, lagre til fil, forsøk å spille den → feiler | candidate |
| `…noekkelen-foelger-samme-autorisasjon` | Nøkkelen går samme vei som lyden | `…klartekst-forlater-aldri-serveren` | Dekrypteringsnøkkelen utleveres bare gjennom samme autorisasjonssti som lyden, med samme levetid, og er bundet til økten | Be om nøkkel uten gyldig token → avvist; med utløpt token → avvist | candidate |
| `…read-er-ikke-store` | «Høre» er ikke «beholde» | `…root` | `deliveryModes` håndheves ved levering: `.progressive` gir en strøm som ikke kan lagres som spillbar fil; `.download` gir en fil, og krever eget grant | Lytter med bare read → ingen fil; med read+store → fil | candidate |
| `…artisten-velger-vernnivaa` | Artisten bestemmer terskelen | `…root` | Artisten setter vernnivå per låt, og flaten sier hva hvert nivå faktisk gir og ikke gir | Sett nivå, publiser, verifiser at leveringen endrer seg tilsvarende | candidate |
| `…lofte-uten-overslag` | Vi lover ikke «umulig» | `…artisten-velger-vernnivaa` | Ingen tekst i produktet, dokumentasjonen eller markedsføringen sier at nedlasting er umulig eller at innholdet er «sikret». Opptaksmuligheten nevnes der artisten velger nivå | Claim-audit av all tekst på flaten mot `haven-claim-review` | candidate |
| `…virker-likt-i-web-og-binding` | Samme vern i app og web | `…root` | Binding får minst samme terskel som web; en låt som ikke kan hentes ut i nettleser kan heller ikke hentes ut fra appen | Samme uttrekksforsøk kjørt mot begge klienter | candidate |
| `…navnene-lyver-ikke` | Manifestet påstår ikke kryptering det ikke har | `…root` | Et manifest med `encryptionPolicy: none` har ikke en `ciphertextSHA256` som er lik `plaintextSHA256`. Feltet er enten fraværende eller likt klartekst-hashen med et navn som sier det | Les manifestet for en åpen låt → ingen «ciphertext»-verdi som gir inntrykk av kryptering | candidate |
| `…to-nivaaer-ikke-flere` | Beskyttet eller åpent, ikke en matrise | `…artisten-velger-vernnivaa` | Artisten velger mellom nøyaktig to: **beskyttet** (kryptert, segmentert levering) og **åpent**. `encryptionPolicy`/`keyScope`/`deliveryModes` utledes av valget, ikke av artisten | Flaten viser to valg; ingen tredje tilstand kan settes fra GUI | candidate |
| `…gamle-laater-blir-beskyttet` | De som ligger der blir med | `…root` | Alle allerede publiserte låter krypteres og pakkes om, uten at tjenesten stanser og uten at noe som virket slutter å virke | Før/etter: hver publiserte låt spilles av ende-til-ende i nettleser; katalogen svarer 200 gjennom hele jobben | candidate |
| `…migrering-er-reversibel` | Ompakkingen kan rulles tilbake | `…gamle-laater-blir-beskyttet` | Originalen finnes til migreringen er verifisert, og det finnes en vei tilbake til dagens levering per låt | Rull tilbake én låt etter migrering → den spiller fortsatt | candidate |
| `…testet-paa-produksjonsstien` | Testene treffer den ruta lytteren bruker | `…root` | Hver verntest går gjennom HTTP-ruta en klient faktisk kaller, ikke gjennom cellen direkte | Test som kaller cellen direkte er ikke gyldig bevis; ACCEPT.md navngir ruta hver test traff | candidate |

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- **Ikke EME/DRM i denne omgangen.** FairPlay og Widevine er sterkere, men krever
  lisensserver, CENC-pakking og deployment-pakke fra Apple. Det er et lisens- og
  integrasjonsprosjekt, ikke et kodeproblem, og hører hjemme når det finnes noe å
  beskytte som er verdt den jobben.
- **Ikke den analoge veien.** Opptak av utgangen er alltid mulig. Vi later ikke som
  noe annet.
- **Ikke vannmerking.** Sporing av hvem som lekket er et annet formål med andre
  personvernkonsekvenser.
- **Ikke migrering av allerede publiserte låter** før det er avklart hva som skjer
  med dem (se §6).

| Kapabilitet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| Kryptering ved lagring | `MusicPublishingCells.swift:943-958` | Dekker lagring, ikke levering | ja |
| Vernvokabular per spor | `MusicPublishingSupport.swift:64-75` | Er felter; ingen håndhevelse henger på dem i dag | ja |
| `deliveryModes` | `MusicPublishingSupport.swift:279` | Modellert, ikke håndhevet ved levering | ja |
| Ett lesepunkt for lyd | `VaporButterpopStudio.swift:661-730` | Dekker stream og preview; nedlasting går egen vei | ja |
| Agreement/grants | `CellProtocol: Sources/CellBase/Agreement/Agreement.swift` | `checkGrant` matcher grant mot liste; ingen valgfrie vilkår | ja |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Artistens vernvalg per låt, i Publiser-fanen | bilde, så kjørende flate | `/butterpop` → Publiser | `images/vernvalg-v1.png` | nei |
| Uttrekksforsøket som feiler: fanget respons lagret til fil, som ikke lar seg spille | testutdata + fil | `TESTRESULT.md#uttrekk` | — | nei |
| Samme uttrekksforsøk mot Binding | testutdata | `TESTRESULT.md#uttrekk-binding` | — | nei |
| Levering med segmentert, kryptert strøm | kjørende flate | staging `/butterpop` | — | nei |
| `contract/` for leverings- og nøkkelendepunktene med positive og negative fixtures | fil | `contract/` | — | nei |
| Claim-audit av all vern-tekst | fil | `ACCEPT.md#claims` | — | nei |

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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://project-work.share-selected-intent [active] — Share selected project intent
- purpose://questionnaire.delivery.consent [active] — Questionnaire delivery and consent
- purpose://governance [active] — Governance
- purpose://access.audit.privacy [active] — Access, audit and privacy
- purpose://value-and-commons [candidate] — Value and commons

## 5. Avledede tester

| test | type | Formål | Hvordan | Bevis |
|---|---|---|---|---|
| `test.uttrekk.ingen-spillbar-fil` | command | `…klartekst-forlater-aldri-serveren` | Spill av som lytter med bare read. Fang **alt** ruta returnerer, skriv til fil, kjør `ffprobe` → skal feile | `TESTRESULT.md#uttrekk` |
| `test.uttrekk.produksjonsstien` | inspection | `…testet-paa-produksjonsstien` | Hver verntest navngir HTTP-ruta den traff. En test som kaller cellen direkte teller ikke | `ACCEPT.md#stier` |
| `test.noekkel.uten-token-avvist` | command | `…noekkelen-foelger-samme-autorisasjon` | Be om nøkkel uten token, med fremmed token, med utløpt token → tre avvisninger | `TESTRESULT.md#noekkel` |
| `test.noekkel.levetid` | measurement | `…noekkelen-foelger-samme-autorisasjon` | Nøkkelens levetid ≤ tokenets | `TESTRESULT.md#noekkel` |
| `test.grant.read-gir-ikke-fil` | command | `…read-er-ikke-store` | read → ingen nedlastingsrute svarer 200 | `TESTRESULT.md#grant` |
| `test.grant.read-og-store-gir-fil` | command | `…read-er-ikke-store` | read+store → fil leveres | `TESTRESULT.md#grant` |
| `test.nivaa.endrer-levering` | command | `…artisten-velger-vernnivaa` | Sett hvert nivå, verifiser at leveringen faktisk endrer seg | `TESTRESULT.md#nivaa` |
| `test.tekst.ingen-overslag` | inspection | `…lofte-uten-overslag` | Claim-audit: ingen «umulig», «sikret», «beskyttet» uten forbehold | `ACCEPT.md#claims` |
| `test.binding.samme-terskel` | command | `…virker-likt-i-web-og-binding` | Samme uttrekksforsøk mot Binding | `TESTRESULT.md#uttrekk-binding` |
| `test.gui.parity` | inspection | `pkg.std.gui-surface` | Godkjent bilde mot faktisk | `ACCEPT.md#parity` |
| `test.build` / `test.regression` | command | `pkg.std.everything-works` | `swift build --target App`, full suite | `TESTRESULT.md#build` |

## 6. Åpne spørsmål (bare de som endrer treet)

Alle besvart. Beslutningene, samlet:

| # | Spørsmål | Kjetils svar | Dato |
|---|---|---|---|
| 1 | Trinn på stigen | Segmentert HLS med AES-128, nøkkel gjennom samme autorisasjon som lyden. Ikke EME/DRM nå | 09-10 |
| 2 | Eksisterende låter | Alle til **beskyttet**. Gjøres som en validering | 09-17 |
| 3 | Antall nivåer | To: **beskyttet** (kryptert) eller **åpent** | 09-10 |
| 4 | Hva «åpent» betyr | Både fritt hentbar URL og helt åpen fil | 09-17 |
| 5 | Default | **Beskyttet**, «slik at vi viser at vi tar på alvor å beskytte åndsverk» | 09-17 |
| 6 | Opptak | Akseptert som mulig | 09-10 |

**Tolkning av svar 4, som må korrigeres hvis den er feil:** «åpent» er ett nivå, ikke
to. Velger artisten åpent, gjelder begge egenskapene samtidig — adressen virker for
hvem som helst, og det man får er en vanlig lydfil. «Strøm eller nedlasting» er en
egen akse (`deliveryModes`) som finnes fra før, ikke et tredje vernnivå.

**Konsekvens av svar 2 som endrer planen:** låtene skal byttes til lossless rett
etter at dette er i prod. Migreringen er derfor ikke en bevaringsoppgave — den er en
**generalprøve på den beskyttede publiseringsløypa**, med innhold som uansett skal
erstattes. Det senker kravet til reversibilitet på selve filene, og hever kravet til
at løypa virker. `…migrering-er-reversibel` justeres tilsvarende: originalene
beholdes til migreringen er verifisert, men vi bygger ikke en tilbakerullingsmekanisme
for innhold som skal ut uansett.

## 7. Iterasjoner

| # | Dato | Hva endret seg |
|---|---|---|
| 0 | 2026-09-10 | Første dekomponering. |
| 2 | 2026-09-17 | Alle åpne spørsmål besvart. Default = beskyttet. «Åpent» tolket som ett nivå der både fri URL og åpen fil gjelder. Migreringen omdefinert fra bevaring til generalprøve, fordi låtene byttes til lossless rett etterpå. |
| 1 | 2026-09-10 | **Auditen i iterasjon 0 var delvis feil, og feilen var min.** Lyd er ikke kryptert i lagring; filene i prod er vanlig MP3. Jeg hadde lest krypteringskoden i `MusicIngestCell` og generalisert til hele systemet uten å sjekke hvilken sti Butterpop faktisk bruker. Bekreftet med `od -c` på serveren. Nye formål: `…navnene-lyver-ikke`, `…to-nivaaer-ikke-flere`, `…gamle-laater-blir-beskyttet`, `…migrering-er-reversibel`. Kjetil valgte trinn (HLS+AES-128), to nivåer, og at eksisterende låter skal med. |
