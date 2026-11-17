# Formålsspesifikasjon — lagringsceller og tjenesteregister

Oppgavemappe: `PDD_lagringsceller-og-tjenesteregister_2026-10-05` · Opprettet 2026-10-05 · Iterasjon 2 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Lag en eller flere celler som håndterer lagring til konfigurerbar lagringstjeneste. Vi må som et ledd i dette bygge opp en register over hvilke tjenester finnes, hvilke formål de løser og hva det koster. Dette bør ligge allment tilgjengelig i HAVEN. Men vi kan tenke etter om det skal være gratis for enkeltindivider i HAVEN men med en liten mikrobetaling for gruppeentiteter som selskaper. (Bør ideelle organisasjoner få like rettigheter som enkeltindivider? Kan være en Digipomps godkjenning) Når en fil skal persisteres sendes den til lagrings cellen som sender den videre til konfigurert lagringstjeneste. Vi må støtte at selskaper som DiMy kjøper lagringstjenesten og tilbyr lagrings celler til brukere mot mikrobetalinger. (da kan DiMy hjelpe til med å finne rimeligere lagring og spre lagringen så Dimy hjelper til å optimalisere lagrings bruken)

Last verified against code: 2026-10-05. Lest i CellScaffold. Arbeidstreet står på `codex/entitetsutvidelse-20260929`; lokal `origin/main` er `fdcfe7a5` (2026-09-30). Ingen fetch, så nyere main er ikke sett. Ingen produktfiler er endret.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde og grense |
|---|---|---|
| Det finnes en celle for lagring til en leverandør | retrieved | `Sources/App/Cells/ObjectStorage/ObjectStorageAdapterCell.swift` (lik origin/main). Leverandørtyper for S3, R2, B2, Wasabi er deklarert. Bare lokal disk virker: andre typer svarer «provider adapter requires external S3-compatible transport». |
| «Når en fil skal persisteres sendes den til lagringscellen» | contradicted (som nåtilstand) | `Sources/App/Cells/MusicPublishing/MusicPublishingSupport.swift:606–610` skriver rett til disk med FileManager. Ikke all persistering går via cellen i dag. |
| Cellen kan ta imot store filer | contradicted | `putObject` tar hele filen som `data` i payload. Alt går gjennom app-minnet (grense 768 MB). `presignRead` svarer `unsupported`. |
| Mikrobetaling finnes | retrieved fra origin/main | `Sources/App/Cells/Micropayments/PaymentGateCell.swift` og `CreditIssuer.swift` på origin/main (arbeidstreet mangler 1 395 linjer av dette). Brukskvote er en tilgangsrett: ikke overførbar, ikke uttakbar, bare gyldig hos utstederen. Pris settes per inngang (`setPrice`, `setVolumePrice`, `enter`). |
| Løpende pris for lagring (per GB per måned) | unavailable | Ikke funnet. Dagens prising er per handling, ikke per lagret mengde over tid. |
| En utsteder (DiMy) kan ha egen kvote for egne ressurser | retrieved fra origin/main | `CreditIssuer.acceptedResourcePrefixes`: kvote fra én utsteder brukes bare på utstederens ressurser. |
| Entitetsklasse (enkeltindivid / selskap / ideell) kan avgjøres | unavailable | Ingen slik type funnet i `Sources/App`. Codex arbeider på grenen `codex/entitetsutvidelse-20260929`; må avklares der før dette bygges. |
| Digipomps-godkjenning kan uttrykkes | recalled | `PaymentTrustedIssuerBootstrap.swift` og TrustedIssuers finnes. Ikke lest for dette formålet. Må leses før plan. |
| Brukerens nøkler til en lagringstjeneste kan oppbevares eier-scopet | recalled | Det eier-scopede nøkkelregisteret (HANDOFF.md). Status ikke målt i dag. |
| Vi vet hva tjenestene koster | retrieved 2026-10-01 | Dokumentet «Medielagring for HAVEN – alternativer» med kilder. Hetzner endret pris to ganger i 2026, så hver oppføring trenger dato og kilde. |
| Videresalg av lagring mot mikrobetaling er regulatorisk greit | unavailable | Ikke sjekket. Må gjennom `dimy-payment-regulatory-guardrails` før G2. |

## 1. Formålstre

Forankring i Book 23: `purpose://self-determination.data` (rot), `purpose://self-determination.data.locality`, `purpose://value-and-commons`, `purpose://access.audit.privacy`. Alle nye noder er kandidater. Forkortet prefiks: `c://` = `purpose://candidate.lagring.`

| purposeRef | Tittel | Forelder | Goal (outcome) | Success signals | Verifier | Status |
|---|---|---|---|---|---|---|
| c://root | Filer lagres der det tjener eieren | purpose://self-determination.data | Eieren får filer lagret hos en tjeneste som passer formålene hans, uten at verten fylles og uten innlåsing. | Alle bladmål består i ett forløp: velg tjeneste, lagre, les, bytt, betal. | test.lagring.forloep | candidate |
| c://persist | Lagre gjennom lagringscellen | c://root | En fil som skal persisteres sendes til lagringscellen, som sender den til konfigurert tjeneste. | Svaret er en referanse med sha256 og størrelse. Filen kan leses tilbake fra tjenesten. Vertens disk vokser ikke. | test.lagring.rundtur, test.lagring.vert-vokser-ikke | candidate |
| c://configure | Bytte tjeneste med konfigurasjon | c://root | Eieren velger og bytter lagringstjeneste uten ny kode. | Samme testsett er grønt mot to ulike tjenester. Filer lagret før byttet kan fortsatt leses. | test.lagring.bytt-tjeneste | candidate |
| c://own | Bare eieren rår over filer og nøkler | purpose://access.audit.privacy | Ingen andre, scaffold-admin inkludert, når filer eller funksjon uten avtale. Tjenestenøkler vises aldri. | Feil requester og feil keypath avvises. Ingen nøkkel finnes i state, flow eller logg. | test.cell.auth-negative, test.lagring.ingen-hemmeligheter | candidate |
| c://true-claims | Det cellen sier om filen er sant | purpose://self-determination.data.verifiability | Påstander om sha256, størrelse, sted og kryptering stemmer med bytene hos tjenesten. | Testen leser bytene hos tjenesten og sammenligner med referansen. | test.lagring.les-bytene | candidate |
| c://meter | Bruk måles per eier | c://root | Lagret mengde og utgående trafikk er målt per eier og kan forklares. | Målingen avviker under 2 % fra tjenestens egne tall i testbøtta. | test.lagring.maaling | candidate |
| c://register.find | Se hvilke tjenester som finnes | purpose://value-and-commons | Alle i HAVEN kan se tjenestene, hvilke formål de løser og hva de koster. | Hver oppføring har selskap, land, pris for lagring og trafikk, begrensninger, kilde og dato. Oppføring eldre enn 90 dager merkes utdatert. | test.register.oppforing-komplett, test.register.utdatert-merkes | candidate |
| c://register.choose | Velge tjeneste ut fra egne formål | c://register.find | Eieren oppgir formål og volum og får tjenestene rangert med anslått månedskost. | De tre scenariene fra dokumentet 01.10 gir samme tall som der (±1). Tjenester som bryter et krav vises som utelukket med grunn. | test.register.rangering | candidate |
| c://register.access | Rett tilgang for rett entitetsklasse | purpose://value-and-commons | Enkeltindivider bruker registeret gratis. Gruppeentiteter betaler en liten mikrobetaling. Godkjente ideelle behandles som enkeltindivider. | Fire requestere (individ, selskap, godkjent ideell, ikke-godkjent ideell) får hvert sitt forventede utfall og kvittering. | test.register.tilgang-per-klasse | candidate, avhenger av spørsmål 1 |
| c://resale.offer | En leverandør tilbyr lagringsceller | purpose://value-and-commons | Et selskap som DiMy kjøper lagring og tilbyr lagringsceller til brukere mot mikrobetaling. | En bruker uten egen tjenestekonto lagrer en fil via DiMys tilbud. Prisen trekkes fra brukskvote. Begge får kvittering. | test.videresalg.forloep | candidate |
| c://resale.optimize | Leverandøren kan flytte og spre lagringen | c://resale.offer | Leverandøren flytter filer til rimeligere tjeneste og holder kopier, uten at brukerens referanser brytes. | Etter flytting leser brukeren samme fil med samme referanse. Når én tjeneste er nede, leses filen fra kopien. | test.videresalg.flytt-uten-brudd, test.videresalg.kopi-overlever | candidate |
| c://resale.bounded | Leverandøren ser ikke mer enn avtalt | purpose://self-determination.data.recipients | Brukeren ser hvor filene ligger og hva leverandøren kan lese. Flytting skjer bare til steder brukerens krav tillater. | Flytting til en tjeneste som bryter brukerens krav (f.eks. utenfor EU) avvises. | test.videresalg.krav-overholdes | candidate |
| c://surfaces | Flatene viser dette | purpose://gui.quality.functional-accessible | Registeret, «Mitt lager» og leverandørens tilbud kan sees og brukes. | Godkjente bilder per flate og tilstand. Hver handling kan nås. | pkg.std.gui-surface | candidate |

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.

### Slik henger det sammen

```
Bruker ──fil──▶ Lagringscelle (eies av brukeren)
                  │  1. sjekker tilgang, lager referanse + sha256, måler bruk
                  │  2. sender videre til konfigurert tjeneste
                  ▼
        ┌─────────────────────────────┬──────────────────────────────┐
        │ Egen tjenestekonto          │ Tilbud fra leverandør (DiMy) │
        │ (brukerens egne nøkler)     │ DiMy eier nøklene, tar       │
        │                             │ mikrobetaling, flytter/sprer │
        └──────────┬──────────────────┴──────────────┬───────────────┘
                   ▼                                 ▼
            Hetzner / Scaleway / R2 / …  ◀── valgt ut fra ──  Tjenesteregister
                                                              (hva finnes, formål, pris)
```

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke videotranskoding eller CDN. Det er egne vedtak.
- Ikke et nytt betalingssystem. Mikrobetaling bruker PaymentGate og utstederkvote som finnes.
- Ikke penger: kvote er fortsatt en ikke-overførbar bruksrett.
- Ikke deploy. Utsetting på staging/prod går via deploykøen med egen claim.
- Et formålsmatch gir aldri tilgang. Rangering i registeret er et råd, ikke en rettighet.

| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Lagringscellens grunnmur | `Sources/App/Cells/ObjectStorage/ObjectStorageAdapterCell.swift` | Bare lokal disk. Ingen S3-transport, ingen signerte URL-er, hele filen i minnet. | Ja |
| Brukskvote og utstedere | origin/main: `Sources/App/Cells/Micropayments/` | Pris per handling i hele øre (`amountMinorUnits: UInt64`, `PaymentGateCell.swift:456`). Enheter under 1 øre og løpende lagringspris finnes ikke og må utformes. | Ja, for c://register.access og c://resale.* |
| Entitetsklasse | ukjent; Codex-grenen `codex/entitetsutvidelse-20260929` | Ikke funnet. Avklares med Astra før plan. | Ja, for c://register.access |
| Digipomps-godkjenning av ideelle | `PaymentTrustedIssuerBootstrap.swift`, TrustedIssuers | Ikke lest for dette. | Ja, for c://register.access |
| Eier-scopede tjenestenøkler | nøkkelregisteret (HANDOFF.md) | Status ikke målt. Uten det kan ikke brukeren ha egen tjenestekonto. | Ja, for c://configure |
| En ekte tjeneste å teste mot | S3-kompatibel tjeneste kjørt lokalt på Mac-en eller på verten (Kjetil 2026-10-08) | Ingen Hetzner-bøtte i leveranse 1. Testtjenesten startes for kjøringen og fjernes etterpå, med data og image; opprydding føres i TESTRESULT.md. | Ja, for test.lagring.* mot ekte protokoll |
| Regulatorisk vurdering av videresalg | `dimy-payment-regulatory-guardrails` | Ikke gjort. | Ja, før G2 |
| Fersk main | `git fetch origin main` fra macOS | Lokal ref er fra 30.09. | Ja, før plan |
| Ny persistert celle | lesson.new-cell-must-declare-its-provisioning-mode | Hver ny celle må svare på provisjoneringsspørsmålene. | Ja |

## 3. Forventningskontrakt — «Det du kommer til å se»

Én rad per leveranse. Dette er det eneste som teller som fremdrift etter G2.

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Tjenesteregisteret: tomt, fylt, med utdatert oppføring | bilde | `images/register-<tilstand>-v1.png` | `register-fylt-v1.png`, `register-tom-v1.png`, `register-utdatert-v1.png`, `register-selskap-v1.png`, `register-smal-v1.png` | nei |
| «Mitt lager»: ikke satt opp, satt opp, feil mot tjenesten | bilde | `images/mitt-lager-<tilstand>-v1.png` | `mitt-lager-ikke-satt-opp-v1.png`, `mitt-lager-satt-opp-v1.png`, `mitt-lager-feil-v1.png` | nei |
| Leverandørens tilbud (DiMy): pris, hvor filene ligger, kost mot inntekt | bilde | `images/tilbud-<tilstand>-v1.png` | leveranse 2; ikke laget | nei |
| Dataflyt mellom cellene | fil | `dataflow.md` | — | nei |
| Kontrakter for cellene med fixtures | fil | `contract/` | — | nei |
| En fil lastet opp i HAVEN ligger i Hetzner-testbøtta | kjørende flate + testutdata | staging, `TESTRESULT.md#rundtur` | — | nei |
| Registeret fylt med de ni tjenestene fra dokumentet 01.10 | kjørende flate | staging | — | nei |
| En bruker lagrer via DiMys tilbud og blir trukket kvote | testutdata | `TESTRESULT.md#videresalg` | — | nei |
| Utdata fra alle tester i §5 | fil | `TESTRESULT.md` | — | nei |

Bildene er HTML-skisser med eksempeldata, se `images/README.md` for hva skeleton ikke er bevist å kunne rendre. Leveranse 1 er radene uten videresalg; leveranse 2 er DiMys tilbud og betaling for lagring.

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
    - artefakt skeleton/ (port G1-GUI): CellConfiguration/skeleton-JSON som bildet er rendret fra. Er bildet en mockup i stedet for Porthole-preview, kreves i stedet en renderingserklæring i images/README.md som lister hva skjelettet ikke kan rendre.
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
- **lesson.a-conditional-artifact-must-still-cost-something** (2026-09-18, minor): purpose_dev.py validate ble rød på PDD_entitetsdata-egen-kontroll fordi artefaktet 'skeleton/' manglet, selv om G1-GUI var godkjent på bilder Kjetil faktisk hadde sett. Pakken beskrev artefaktet som påkrevd «når Porthole-preview er brukt»; validatoren krevde det alltid.
    - forebygging: Et betinget krav oppfylles av et *annet krav*, aldri av et fravær. Feltet 'satisfiedByDeclaration' peker på en fil og en overskrift og krever minst ett punkt under den: enten viser du skjelett-JSON-en bildet er rendret fra, eller du skriver ned hva skjelettet ikke kan rendre. Begge tvinger frem spørsmålet «kan flaten dette?». Feilmeldingen navngir begge veier ut. Sjekket begge veier: rød uten erklæring, grønn med.
- **lesson.location-is-not-ownership** (2026-09-22, major): dataflow.md begrunnet at AIGateway matte ligge i appen med at «en gateway utenfor entiteten gjor prompten til noen andres data». Kjetil: en celle i skyen som eies av meg er pr definisjon innenfor min entitet.
    - forebygging: Regelen er uniform og gjelder alle scaffolds likt: ingen andre, scaffold-admin inkludert, nar data ELLER funksjonalitet i en celle jeg eier uten en Agreement som sier det. Et vern som bare gjelder skyen er et tegn pa at grensen er tegnet feil. Negative tester skal kjores i begge oppsett, lokalt og sky, og gi samme svar — og de skal dekke handlinger, ikke bare felter. Den positive motsatsen ma ogsa testes: en Agreement apner nayktig sitt eget omfang.
- **lesson.read-origin-main-before-writing-a-mechanism** (2026-09-22, major): Runde 1 av PDD_entitetsdata skrev en egen resolver for lenkede identiteter (EntityLinkAuthorizer, ny CellAuthorizationPath.linkedIdentity, ny hook pa GeneralCell). Da patchen ble lagt mot origin/main viste det seg at IdentityLinkRegistry og GeneralCell.authorizationEvidence allerede gjorde det samme, landet av en annen oppgave (purpose://candidate.entity-link.resolver-honours-link). Hele resolveren ble forkastet.
    - forebygging: Brief-audit skal si HVILKEN revisjon noe ble lest fra, og for et formal som skal endre en mekanisme skal kilden vaere origin/main (git show origin/main:<fil>), ikke utsjekket. Preflight-skriptet sjekker na at patchen passer mot origin/main i et eget worktree for noe legges pa. Og: for du skriver en mekanisme, grep pa main etter navnet pa det den skal gjore (her: sameEntity, linkedIdentity) - ikke bare etter typen du planlegger a lage.
- **lesson.method-lived-only-on-one-machine** (2026-09-24, major): Metoden selv — Book 35 (PDD-arbeidsflyten), Book 36, lærdomsregisteret med 50 lærdommer, formålspakkene, purpose_dev.py — lå bare i ett utsjekk på Kjetils Mac på grenen codex/docs-cleanup-20260810, aldri på main; derfor verken i HAVEN eller hos andre utviklere.
    - forebygging: Metodeartefakter landes som kode: PR til main og pin-oppdatering i HAVEN. Test: git cat-file -e origin/main:<fil> for hver metodefil.
- **lesson.downstream-pin-must-come-from-the-consumer** (2026-09-24, major): Nedstrøms-baselinen for CellScaffold var rød 22.09 («cellprotocol krever swift-crypto 4.5.2, dimymint krever 3.x») og ble rapportert som prosjektets blokkering. CellScaffold main pinnet DiMyMint af41630, som løser swift-crypto 4.x; skriptet hadde hardkodet en eldre revisjon (1718fda).
    - forebygging: Et nedstrøms-skript leser alle transitive pinner fra forbrukerens egen Package.swift/Package.resolved på origin/main ved kjøring, og logger dem. En rød avhengighetsoppløsning i et skript med hardkodede pinner er ikke et funn før pinnene er bekreftet mot forbrukerens resolved.
- **lesson.disposable-worktree-must-be-reset-before-checkout** (2026-09-24, minor): pdd-check/Binding ble stående på 72f6a6c9 i to kjøringer selv om skriptet ba om origin/main: «Your local changes to project.pbxproj would be overwritten by checkout». Baselinen målte feil Binding-revisjon uten å si fra.
    - forebygging: Engangs-worktrees resettes hardt (`git reset --hard` + fjern Package.resolved) før hver utsjekk, og skriptet skriver ut revisjonen den faktisk står på — en avvikende revisjon skal stoppe kjøringen, ikke logges forbi.
- **lesson.report-the-commit-you-pushed-not-the-one-you-planned** (2026-09-24, minor): TESTRESULT og PLAN sa «commit ebb0b7f». Branchen sto på e66b7f1 — commit.sh hadde laget en ny hash — og var ikke pushet. Push-skriptets EXPECT måtte rettes før det kunne kjøre.
    - forebygging: Etter hver commit/push: les `git rev-parse --short HEAD` og `git ls-remote --heads origin <branch>` og lim inn utdataene i STATUS/TESTRESULT. Sjekk også for remote-tracking ref før du sier «pushet» (lesson.branch-is-empty-after-eight-work-packages, samme familie).
- **lesson.lookup-again-when-a-surface-is-added** (2026-09-24, major): De nye seksjonene i «Utvid entiteten» (B10) var portet på synlighet med rot-scope, og listen med verktøyets forespørsel forsvant — samme feil som lesson.unresolvable-condition-is-invisible fra 05.09.
    - forebygging: For hver ny eller endret skjelettflate: kjør `purpose_dev.py lookup --tags skeleton gui` før utformingen, og `BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` + `testPersonalCopilotLocalSurfacesLoadWithoutReferenceFailures` før flaten vises eller committes.
- **lesson.picker-state-keypath-is-read-and-written** (2026-09-24, minor): Velgeren «Verktøy» i «Gi tilgang» sto på «Velg verktøy» selv om cellen hadde valgt verktøyet.
    - forebygging: `selectionStateKeypath` skal være en nøkkel cellen både leser (`{selected}`) og skriver; test rundturen (`pickerSelectionRoundTrips`).
- **lesson.pairing-can-outlive-the-identity** (2026-09-24, major): Agenten var paret med en HAVEN-identitet fra 4. mai («Binding Local Session», nøkkel 13BF…), mens HAVEN brukte en annen privat identitet (D362…, identitetsfilen skrevet 18.09). Svar fra HAVEN ville blitt avvist; ingen test i noen av endene kunne se det.
    - forebygging: En flate som ber eieren signere for agenten sammenligner egen nøkkel med agentens forankring og viser forskjellen før signering, med vei til ny paring (test: `offerIsRefusedHereWhenThisHavenHoldsAnotherKey`, `theOwnerNeverSignsWhatFailedTheCheck`). Sjekk nøkkelkontinuitet før live-test av noe som signeres.
- **lesson.screencapture-from-runner-can-fail** (2026-09-24, minor): `screencapture -l <vindu>` fra jobbløperen ga «could not create image from window» for HAVEN-vinduet, med samme vindus-ID som computer use så.
    - forebygging: Ta bilder av flater med computer use (eller be Kjetil), og ikke planlegg bevis som avhenger av `screencapture` fra løperen før det er målt at det virker den dagen.
- **lesson.sketch-assumed-a-renderer-it-did-not-have** (2026-09-25, major): Skissen v2 (HTML) var venstrestilt, men «Utvid entiteten» i HAVEN viste all tekst sentrert, også etter at hAlignment «leading» var satt.
    - forebygging: Før en skisse godkjennes: finn CellProtocol-committen HAVEN-bygget bruker, les hvordan Text/VStack/HStack rendres der, og list i §3 hva den ikke kan (her: venstrestilt tekst). Et HTML-bilde er ikke bevis for at rendreren kan det samme.
- **lesson.maxwidthinfinity-also-stretches-height** (2026-09-25, minor): En tekst i en listerad ble kuttet med «…» etter fem linjer når en HStack med wrap og maxWidthInfinity sto i samme rad; uten maxWidthInfinity ble teksten hel.
    - forebygging: Ikke sett maxWidthInfinity på elementer i listerader. Se etter «…» i skjermbildet av hver rad med lang tekst, i et smalt vindu.
- **lesson.wrap-gives-each-item-its-ideal-width** (2026-09-25, minor): Knappen «Par agenten med denne HAVEN-en» gikk ut over kortet og ble klippet i et smalt vindu.
    - forebygging: Knapper i vanlig HStack, som kan krympe og bryte teksten; wrap bare for korte merkelapper. Se på flaten i et smalt vindu før den vises fram.
- **lesson.empty-list-keeps-its-slot** (2026-09-25, minor): Tomme lister og tomme tekster ga store hull i «Utvid entiteten».
    - forebygging: Én liste per kort, der cellen bestemmer radene (`kind`) og en rad med en kort linje står der det ellers ville vært tomt. Ingen faste høyder på lister, og ingen tekst på toppnivå som kan bli tom.
- **lesson.pgrep-pattern-must-allow-arguments** (2026-09-25, minor): Byggejobben avsluttet ikke HAVEN, og `open` hentet bare fram det gamle bygget (startet 24.09 17:29) i stedet for å starte det nye.
    - forebygging: Bruk 'HAVEN( |$)' i mønsteret, og skriv ut prosessens starttid etter omstart og sammenlign den med byggetiden før noe vises fram.
- **lesson.computer-use-image-is-not-a-file** (2026-09-25, minor): Skjermbildene av den nye flaten kunne ikke sendes til Kjetil som fil; vinduet var i tillegg på et annet skrivebord og kunne ikke gjøres større i bakgrunnen.
    - forebygging: Planlegg bildebeviset med en vei som gir en fil (Kjetils eget skjermbilde, eller skjermopptakstilgang for løperen), og si det før arbeidet, ikke etter.
- **lesson.text-field-sends-a-string** (2026-09-25, major): Adressefeltet i «Utvid entiteten» kunne aldri starte en forespørsel: Enter ga alltid «Si hvilket scaffold dette gjelder — `audience` …».
    - forebygging: For hvert tekstfelt: en kontraktstest som sender feltets egen payload (.string) til targetKeypath og venter et svar som ikke er feil.
- **lesson.green-gate-must-read-the-last-summary-line** (2026-09-26, major): runde2.sh committet og pushet 399f6d2 med 4 røde tester. Porten grep'et «Executed … with 0 failures» i hele loggen og traff en grønn suites linje lenger opp; siste linje sa «1262 tests, with 2 tests skipped and 8 failures».
    - forebygging: En grønn-port leser bare den siste «Executed»-linjen (tail -1) og krever « 0 failures (0 unexpected)». Sammenligningen gjøres uten pipe (POSIX case), fordi `echo | grep -q` under pipefail kan gi rødt på grønt (SIGPIPE). Porten skriver ut nøyaktig hva den sammenlignet.
- **lesson.module-and-type-share-a-name-in-cellprotocol** (2026-09-26, minor): `CellApple.EntityAnchorCell` og `CellVapor.EntityAnchorCell` kompilerte ikke: «type 'CellApple' has no member 'EntityAnchorCell'». Begge modulene har en type med samme navn som modulen.
    - forebygging: Én fil per modul som importerer bare den ene og gir typen et unikt typealias (TestSupport/AppleEntityAnchorAlias.swift, VaporEntityAnchorAlias.swift). Testfilen importerer ingen av modulene direkte.
- **lesson.placeholder-example-leaks-into-judgement** (2026-09-28, minor): I «Dommerbenken — chat» v2 var plassholderen i fritekstfeltet «f.eks. «status på prosjektet»». Kjetil skrev nøyaktig «status på prosjektet» som sin egen tolkning i to av tretti saker («hvor står vi nå på prosjektet», «hva står igjen»). Eksempelet var hentet fra meningen til en sak i settet.
    - forebygging: Eksempler, plassholdere og hjelpetekst i en dommerflate skal hentes fra et domene som ikke finnes i settet, og testes: ingen sak i settet skal ha gold hvis tittel eller alias overlapper eksempelteksten. Rapporter saker der dommerens fritekst er lik eksempelet som svakere.
- **lesson.corr-grant-expired-without-renewal-path** (2026-09-30, major): 30.09 fikk Vegar `recipient_not_allowed` da han sendte til `kjetil-vegar-codex-d`, Kjetils klient avviste sitt eget bevis, og meldingen til Victoria ble avvist på samme måte; korrespondansen sto stille i over ett døgn.
    - forebygging: En tilgang eller et bevis med utløpstid tas ikke i bruk før fornyelsesveien er testet ende til ende (utløpt tilgang → fersk invitasjon → eiergodkjenning → ny frist → sending virker), og fristen står i pilotens STATUS med en påminnelse minst sju dager før.
- **lesson.renewal-invite-must-carry-device-id** (2026-09-30, major): Gjennomgangen av korrespondanseklienten 30.09 viste at `setup` gjenbruker `identity.json`, men tar enhets-ID-en fra invitasjonen (`invite.deviceID ?? tilfeldig`); en fornyelsesinvitasjon uten profilens `deviceID` ville gitt ny enhet og `principal_already_enrolled` i stedet for fornyelse.
    - forebygging: En fornyelsesinvitasjon lages bare med `deviceID` hentet fra deltakergrafen eller profilen (`haven-correspondence-mcp identity`), og generatoren nekter uten; test: fornyelsesinvitasjonens `deviceID` er lik profilens, og `setup` gir `pending_approval` med `renewsGrantID`.
- **lesson.host-mutation-without-reading-the-coordination-file** (2026-10-02, major): 30.09 satte en Claude-tråd ut en gren-commit på staging og byttet invitasjonene, med Kjetils ja, men uten claim. En Codex-tråd hadde claim på samme container (HD-0141), staging var reservert for 2026.9.4, og deploykøen trodde i to døgn at staging kjørte forrige utgivelse.
    - forebygging: Før enhver vertsmutasjon: les `_losen-queue/KOORDINERING.md`, kjør `hd coord status`, ta egen claim på en HD-oppgave, og før utsettingen inn i køen etterpå. Test: jobbloggen for utsettingen viser `hd coord status` uten annen claim på samme tjeneste, og egen claim, før første kommando mot verten. Eierens ja til å sette ut erstatter ikke sjekken.
- **lesson.remembered-install-state-is-not-measured** (2026-10-02, minor): En plan sa at agenten på Macen var bygget fra en bestemt gren, og bygde grenvalg og et åpent spørsmål til eieren på det. Agenten var installert på nytt fra `main` av en annen tråd seks dager tidligere.
    - forebygging: Hva som er installert, måles før en plan bygger på det: dato og navn på binærene og sikkerhetskopiene i `bin/`, `launchctl print`, og om commiten er på `origin/main`. Test: påstandstabellen merker installasjonstilstand som hentet med måletidspunkt, aldri som husket.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://gui.quality.functional-accessible [active] — Functional accessible GUI
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance
- purpose://governance [active] — Governance
- purpose://access.audit.privacy [active] — Access, audit and privacy

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
| test.lagring.forloep | c://root | Ett sammenhengende forløp på staging: velg tjeneste, lagre, les, bytt, betal. | ACCEPT.md#forloep | venter |
| test.lagring.rundtur | c://persist | Lagre og les tilbake 1 KB, 50 MB og 500 MB mot etterligning (CI) og mot S3-kompatibel tjeneste lokalt eller på verten; sammenlign sha256. Testtjenesten fjernes etterpå. | TESTRESULT.md#rundtur | venter |
| test.lagring.vert-vokser-ikke | c://persist | `du` på vertens lagringsmappe før og etter 10 opplastinger. | TESTRESULT.md#vert | venter |
| test.lagring.bytt-tjeneste | c://configure | Samme testsett mot to tjenester; bytt og les gammel fil. | TESTRESULT.md#bytt | venter |
| test.lagring.ingen-hemmeligheter | c://own | Søk etter testnøkkelen i state, flow, logg og persistert celle. | TESTRESULT.md#hemmeligheter | venter |
| test.lagring.les-bytene | c://true-claims | Hent objektet direkte fra tjenesten utenom cellen; sammenlign med referansen. | TESTRESULT.md#bytene | venter |
| test.lagring.maaling | c://meter | Sammenlign cellens måling med testtjenestens egen bruksrapport for bøtta. | TESTRESULT.md#maaling | venter |
| test.pris.mikroore | c://meter | Enhetstester: summering av mange beløp under 1 øre gir eksakt sum; trekk i hele øre fører resten videre; ingen overflyt. | TESTRESULT.md#pris | venter |
| test.pris.kost-pluss-paaslag | c://register.choose | Enhetstester: pris = kostpris + påslag med kurs, kilde og dato; 1 øre per oppslag uttrykt i mikroøre. | TESTRESULT.md#pris | venter |
| test.register.oppforing-komplett | c://register.find | Validator: hver oppføring har alle påkrevde felt, kilde og dato. | TESTRESULT.md#register | venter |
| test.register.utdatert-merkes | c://register.find | Oppføring med dato 91 dager tilbake vises som utdatert. | TESTRESULT.md#register | venter |
| test.register.rangering | c://register.choose | De tre scenariene (1/3, 10/30, 50/150 TB) gir tallene fra dokumentet 01.10. | TESTRESULT.md#rangering | venter |
| test.register.tilgang-per-klasse | c://register.access | Fire requestere, forventet utfall og kvittering for hver. | TESTRESULT.md#tilgang | venter |
| test.videresalg.forloep | c://resale.offer | Bruker uten egen konto lagrer via leverandørens tilbud; kvote trekkes; kvitteringer hos begge. | TESTRESULT.md#videresalg | venter |
| test.videresalg.flytt-uten-brudd | c://resale.optimize | Flytt objekt mellom to tjenester; les med uendret referanse. | TESTRESULT.md#flytt | venter |
| test.videresalg.kopi-overlever | c://resale.optimize | Slå av den ene tjenesten i testen; les fra kopien. | TESTRESULT.md#kopi | venter |
| test.videresalg.krav-overholdes | c://resale.bounded | Forsøk flytting til tjeneste som bryter brukerens krav; forvent avvisning. | TESTRESULT.md#krav | venter |

## 6. Åpne spørsmål til Kjetil

Besvart av Kjetil 2026-10-05:

1. Registertilgang: enkeltindivider og Digipomps-godkjente ideelle gratis; selskaper betaler mikrobetaling per oppslag.
2. Bytes-vei: lagringscellen styrer alt. Små filer går gjennom cellen; for store filer gir cellen ut en signert adresse.
3. Registereier: leverandører foreslår, Digipomps godkjenner. Forslag vises som «Ikke kontrollert».
4. Omfang: leveranse 1 er lagringscelle mot én ekte tjeneste (Hetzner), register med de ni tjenestene, og bytte av tjeneste. Leveranse 2 er videresalg via DiMy (c://resale.*) og løpende lagringspris.

Følger av svarene: c://resale.offer, c://resale.optimize og c://resale.bounded står i treet, men hører til leveranse 2. c://register.access er i leveranse 1 og avhenger fortsatt av at entitetsklasse og Digipomps-godkjenning finnes i koden.

Besvart av Kjetil 2026-10-08:

5. Grense for «stor» fil: 8 MB. Over det gir cellen ut signert adresse. Web-flaten tar i dag bare ca. 2,9 MB gjennom cellen, så der brukes signert adresse fra ca. 2,9 MB til `FileUpload` kan mer.
6. Pris per oppslag for selskaper: 1 øre, men prismodellen må kunne uttrykke enheter mindre enn 1 øre og gjenspeile kostpris pluss eventuelt påslag.
7. Testtjeneste: ingen Hetzner-bøtte nå. Det testes mot S3-kompatibel tjeneste lokalt eller på verten, og testoppsettet ryddes bort etterpå.

Følger av svar 6 (forslag, avgjøres i G2): beløp lagres som heltall i mikroøre (1 øre = 1 000 000 mikroøre), slik at for eksempel 1 GB lagret i ett døgn hos Hetzner (ca. 0,25 øre) kan føres eksakt. Pris = kostpris + påslag (prosent og/eller fast beløp), og begge deler vises hver for seg. Kostpris i EUR/USD omregnes med en kurs som lagres med kilde og dato. Brøkdeler samles per eier, og det trekkes hele øre i `PaymentGateCell` når summen når 1 øre; resten føres videre.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-10-05 | Opprettet | Losen |
| 1 | 2026-10-05 | §0–§3, §5 og §6 fylt ut. Bilder ikke laget; venter på svar på §6. | Losen |
| 2 | 2026-10-05 | Kjetils fire svar ført inn i §6. Åtte skisser laget i `images/`. Omfang delt i leveranse 1 og 2. | Losen |
| 3 | 2026-10-08 | Svar 5–7 ført inn i §6: 8 MB, mikroøre med kostpris + påslag, testtjeneste lokalt/på vert i stedet for Hetzner-bøtte. §2 og §5 rettet tilsvarende. | Losen |
