# Formålsspesifikasjon — palazzo sicilia artikler

Oppgavemappe: `PDD_palazzo-sicilia-artikler_2026-09-07` · Opprettet 2026-09-07 · Iterasjon 0 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Vi bør også lage et område for små artikler om Sicilia og maten derfra som kan pirre gjestens nysgjerrighet og bygge opp gjestens formål og interesser rundt temaet. Dette må lagres i entitydataene. (og være persistent) Slik at huset kan gjøre spørringer senere.

Sammenheng: dette er det tredje steget i D4 (innholdssignaler) fra `Vurdering_Signalmatching_Familietilhorighet_2026-09-05.md` §5 — «innholdet er profileringsinstrumentet». Bygger på `PDD_palazzo-husk-det-jeg-sa_2026-09-05` (tagger, signaler, matching) og skal ikke starte før den er grønn.

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Huset har allerede `articles` i publisert innhold (`content.published`), publisert lesing | retrieved | `PalazzoScaffold/Sources/App/Cells/PalazzoContentCell.swift:7, 297–309` (`articles` i `differences()`) |
| Gjestens entitet har poster av typene `purpose` og `interest` med `tags`, skrevet av `self`, og de persisteres med cellens snapshot | retrieved | `PalazzoEntityModels.swift:9–30`; `PalazzoEntityCell.swift:164` (append + event) |
| Huset kan spørre `insight.purposes` / `insight.interests` bare med aktiv samtykkepolicy | retrieved | `PalazzoEntityCell.swift:172–195` |
| Ordliste for tagger (`PalazzoTagLexicon`) og godkjenning av tagger før publisering | unavailable — lages i husk-oppgaven WP1; denne oppgaven utvider den til artikler | `PDD_palazzo-husk-det-jeg-sa_2026-09-05/PLAN.md` WP1 |
| Gjesteflaten «Palazzo Gjest» med seksjoner | retrieved | `PalazzoGuestConfigurationFactory.swift` |
| Artikkeltekster om Sicilia og maten | unavailable — må skrives (forslag: Losen skriver 8 utkast, Andre/huset godkjenner) | — |

## 1. Formålstre

Rot: gjesten møter små tekster om Sicilia og maten som vekker nysgjerrighet; det gjesten *gjør* med dem (lagrer, «vil smake», «ikke for meg», kommenterer) blir formåls- og interesseposter i gjestens egen entitet, i gjestens ord, varig — og huset kan spørre om dem senere bare gjennom samtykke. Invariant: samme som husk — alt som senere brukes skal kunne forklares med gjestens egen handling.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.palazzo-sicilia.root | Artikler som bygger formål og interesser | purpose://candidate.palazzo-husk.root · `service.hospitality.F` | Etter å ha reagert på tre artikler har gjesten tre poster (`interest`/`purpose`, `source: self`) i egen entitet som overlever omstart av scaffoldet, og huset kan — med policy — få `insight.interests` som inneholder artikkeltaggene, ellers denied. | `test.sicilia.e2e` | candidate |
| purpose://candidate.palazzo-sicilia.articles-published-with-tags | Artikler publiseres med godkjente tagger | root | Artikkel = {id, tittel, ingress, brødtekst ≤ 900 tegn, tagger (godkjent av huset via samme tagg-flyt som retter), region, opphav/kilde}. Publisert lesing. En artikkel uten godkjente tagger publiseres, men gir ingen signal. | `test.sicilia.articles` | candidate |
| purpose://candidate.palazzo-sicilia.reaction-becomes-record | Reaksjon blir post i gjestens entitet | root | «Vil smake» → `purpose` (tags = artikkelens tagger, title = artikkelens tittel); «Interessant» → `interest`; «Ikke for meg» → `interest` med `attributes.polarity = negative`; valgfri kommentar → `interaction` med gjestens tekst. Alle via eksisterende `entity.record`, `source: self`. Ingen post uten en handling fra gjesten. | `test.sicilia.reaction` | candidate |
| purpose://candidate.palazzo-sicilia.persistent | Postene er varige | reaction-becomes-record | Poster overlever prosessomstart (snapshot lastes), og `entity.records` viser dem med `recordedAt`. | `test.sicilia.persist` | candidate |
| purpose://candidate.palazzo-sicilia.queryable-by-consent | Huset kan spørre senere, bare med samtykke | root | `insight.interests` / `insight.purposes` inneholder artikkeltaggene når policy er aktiv; uten policy → denied. Negative interesser leveres som egen liste `avoid`, aldri blandet inn i `interests`. | `test.sicilia.query`, `test.cell.auth-negative` | candidate |
| purpose://candidate.palazzo-sicilia.articles-are-signals | Artikler er også signaler (kobling til husk) | articles-published-with-tags | Artikkel med godkjente tagger kompileres til `PalazzoContentSignal(kind: article)` i `content.signals`, så en gjests tidligere kommentar kan treffe en ny artikkel — samme matcher, samme grants. Aktiveres først når husk-oppgaven er grønn. | `test.sicilia.signal` | candidate |
| purpose://candidate.palazzo-sicilia.no-reading-surveillance | Skal ikke: lesing registreres | root · polarity: prohibited | Ingen post, ingen event og ingen telling per gjest av hvilke artikler som er åpnet eller hvor lenge. | `test.sicilia.no-tracking` | candidate |
| purpose://gui.expectation-agreed-before-build | Bilde før kode (pakke) | pkg.std.gui-surface | «Fra Sicilia»-seksjon i gjesteflaten (liste + åpen artikkel med tre knapper og kommentarfelt), tom tilstand, husets artikkel-utkast med tagger. | `test.gui.reference-image-exists` | active |

Utenfor treet: anbefalt rekkefølge på artikler ut fra profil (det er matching og hører til husk-laget), lesestatistikk, artikler fra andre hus.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke et CMS. Artikler skrives i husets draft-patch (`content.draft.apply` med `articles`), som i dag; 8–12 korte tekster i første runde.
- Ikke sporing. Bare eksplisitte handlinger blir poster.
- Ikke ny matcher. Artikkelsignaler bruker husk-matcheren når den finnes.
- Ikke språkmodell i kjeden — Losen kan skrive artikkelutkastene utenfor kjeden; huset godkjenner.

| Kapabilitet / avhengighet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| husk-oppgaven WP1 (tagg-godkjenning, `content.signals`) | `PDD_palazzo-husk-det-jeg-sa_2026-09-05/PLAN.md` | denne oppgaven utvider lexikon + signal-kind; kan ikke starte før WP1 er grønn | ja |
| `entity.record` med `kind`/`tags`/`attributes` | `PalazzoEntityCell.swift:98–171` | `attributes.polarity` er ny konvensjon, ikke ny modell | ja |
| Snapshot-persistens for `PalazzoEntity` | `PalazzoEntityCell.swift` (persistCellSnapshot) | verifiseres ved omstart i test | ja |
| Gjesteflate-fabrikk | `PalazzoGuestConfigurationFactory.swift` | ny seksjon «Fra Sicilia»; åpen artikkel som egen konfigurasjon (`guest.article.configuration`) siden skeleton ikke har «expand» | ja — bilder |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| «Fra Sicilia» i gjesteflaten: 3 artikkelkort (tittel, ingress, region) | bilde | `images/` | `images/gjest-sicilia-liste-v1.png` | nei |
| Åpen artikkel: tekst + «Vil smake» / «Interessant» / «Ikke for meg» + kommentarfelt | bilde | `images/` | `images/gjest-sicilia-artikkel-v1.png` | nei |
| Tom tilstand (ingen artikler publisert) — seksjonen skjules | bilde | `images/` | `images/gjest-sicilia-tom-v1.png` | nei |
| Husets artikkel-utkast med foreslåtte tagger (samme flate som retter) | bilde | `images/` | `images/hus-artikkel-tagger-v1.png` | nei |
| 8 artikkelutkast (NO, ≤ 900 tegn, opphav/kilde, foreslåtte tagger) til Andre for godkjenning | fil | `content/artikler_v1.md` | — | nei |
| Testutdata: articles, reaction, persist, query, signal, no-tracking, e2e | testutdata | `TESTRESULT.md` | ankre | nei |
| Kjørende gjesteflate: Kjetil leser en artikkel, trykker «Vil smake», starter scaffoldet på nytt og ser posten i `entity.records`; huset får taggen i `insight.purposes` etter «Godkjenn alltid» | kjørende flate | lokal PalazzoScaffold | — | nei |

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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://gui.quality.functional-accessible [active] — Functional accessible GUI
- purpose://self-determination.data.use-purpose [candidate] — Purpose binding for data use

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
| test.sicilia.articles | articles-published-with-tags | XCTest: draft med artikkel → taggforslag → approve → publish → `content.published.articles` har id/tagger; uten approve → publisert, intet signal. | TESTRESULT.md#articles | venter |
| test.sicilia.reaction | reaction-becomes-record | XCTest: «Vil smake» → `purpose` med artikkelens tagger, `source: self`; «Ikke for meg» → `interest` med `polarity: negative`; kommentar → `interaction` med gjestens tekst. | TESTRESULT.md#reaction | venter |
| test.sicilia.persist | persistent | XCTest: skriv post, kast cellen, last snapshot → posten finnes. | TESTRESULT.md#persist | venter |
| test.sicilia.query | queryable-by-consent | XCTest: uten policy → denied; med policy → `interests` inneholder taggene, `avoid` de negative, aldri blandet. | TESTRESULT.md#query | venter |
| test.sicilia.signal | articles-are-signals | XCTest: gjestekommentar «vil smake pasta alla norma» + artikkel med tag `norma` → match pending (husk-matcher). | TESTRESULT.md#signal | venter |
| test.sicilia.no-tracking | no-reading-surveillance (antiformål) | Inspeksjon + XCTest: åpne artikkel-konfigurasjonen som gjest → `entity.records` uendret, ingen event med gjest-id + artikkel-id. | TESTRESULT.md#no-tracking | venter |
| test.sicilia.e2e | root | Kjørende: tre reaksjoner → omstart → poster finnes → policy → insight. | TESTRESULT.md#e2e | venter |

## 6. Åpne spørsmål til Kjetil

1. **Hvem skriver artiklene?** Forslag: Losen skriver 8 utkast (arancini, caponata, pasta alla Norma, pistasj fra Bronte, Etna-vin, granita, cannoli, pasta con le sarde) med opphav/kilde; Andre godkjenner og retter. Alternativ: Andre skriver selv.
2. **«Ikke for meg»** — lagres? Forslag: ja, som `interest` med `polarity: negative`, levert som egen `avoid`-liste bare med samtykke. Alternativ: bare positive lagres.
3. **Rekkefølge:** etter husk-oppgaven er grønn (avhengighet WP1). Alternativ: parallelt med egen tagg-flyt.
4. **Artikler som signaler** — bladnoden tas med nå, aktiveres når husk-matcheren er grønn. Alternativ: utsett noden.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-07 | Opprettet | Losen |
| 1 | 2026-09-07 | §0–§3 (7 formål + 1 antiformål), §5 +7 tester, §6 fire spørsmål; venter G1 | Losen |
