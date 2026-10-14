# Formålsspesifikasjon — palazzo tolkning og vektjustering

Oppgavemappe: `PDD_palazzo-tolkning-og-vektjustering_2026-09-26` · Opprettet 2026-09-26 · Iterasjon 3 (G1 godkjent 2026-09-28)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

> ### Avgjort av Kjetil 2026-09-28 (G1)
> «G1-GUI godkjent. 1. CellProtocol main 2. Forslaget er godkjent. 3. avgjøre om noe tilbys i det hele tatt 4. Fiks avviket.»
> 1. **Native tre-liste på CellProtocol main.** Ja, testet mot funksjon og formål før landing (A1).
> 2. **Siste trykk bestemmer om emnene teller for eller mot, og styrken glir (modell a).** Godkjent (B1).
> 3. **Vekten avgjør om noe tilbys i det hele tatt.** Det skal altså være en terskel (B3). Tallet velges fra benken.
> 4. **Fiks avviket.** Tolket som avvik 1: emnene skal vises som brikker, slik bildet viser (A5). Avvik 2 og 3 er ikke visuelle, og står som i §3.

## 0. Intensjon (ordrett) og brief-audit

> 2026-09-24, punkt 4 om at gjesten skal kunne se hvilke emner reaksjonen hennes ble tolket som:
> «Gjesten må ha mulighet til det men det bør i utgangpunktet ikke ta noe særlig plass.»
>
> 2026-09-26: «Har sett på G1-GUI. Vi går for B. Ved flere trykk på samme artikkel skal vektene justeres. Der må vi nok prøve oss fram litt med hvor mye et trykk skal justere. Som du erfarte er det noe menig som er mer absolutt enn annen.»
>
> 2026-09-28: «G1-GUI godkjent. 1. CellProtocol main 2. Forslaget er godkjent. 3. avgjøre om noe tilbys i det hele tatt 4. Fiks avviket.»
>
> 2026-09-26, svar på tre spørsmål:
> - Nytt positivt trykk etter «Ikke for meg» på samme artikkel: **«Ja, siste trykk gjelder»**.
> - Hva som er absolutt: **«Bare artikkelen»**. Emnene får negativ vekt som trekker ned annet innhold, men stenger det ikke.
> - Gjennomgang av husets emner før gjesten ser dem: **«Nei, de er gode nok»**.

<a id="audit"></a>

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Reaksjonsposten fryser artikkelens emner i det hun trykker. Normaliseringen gjør bare små bokstaver og fjerner duplikater. | retrieved | PalazzoScaffold::Sources/App/Cells/PalazzoEntityCell.swift (`entity.article.react`) og Sources/App/Models/PalazzoRememberModels.swift (`PalazzoTagLexicon.normalized`), `0b74f90` |
| Etter et trykk endrer ingenting seg på artikkelflaten i dag. | retrieved | PalazzoScaffold::Sources/App/Skeleton/PalazzoArticleConfigurationFactory.swift |
| `List.childrenKeypath` og `List.expandedStateKeypath` finnes i skjelettformatet. | retrieved | CellProtocol::Sources/CellBase/Skeleton/SkeletonDescription.swift (`SkeletonList`, U2 2026-09-05) |
| Porthole rendrer det. Løses ikke `expandedStateKeypath`, starter alt lukket. Barn rendres med **samme radmal** som forelderen, med innrykk. | retrieved | CellScaffold::Public/js/skeleton-runtime.js (`seedExpandedFromState`, `flattenListTree`), origin/main `6c70a59` |
| Den native rendereren som Binding bruker, har det ikke. | retrieved (git grep uten treff) | CellProtocol::Sources/CellApple/Cells/Porthole/Utility Views/CellListView.swift, origin/main |
| **Rettelse til G1-GUI-bildet:** bildet sa «arbeid i Binding». Den native listerendereren ligger i CellProtocol (CellApple), så endringen går til CellProtocol main. | retrieved | samme fil |
| Vekt per reaksjon: Vil smake 0.8, Interessant 0.5, Ikke for meg −1.0, egne ord 1.0. | retrieved | PalazzoScaffold::Sources/App/Models/PalazzoSignalGraph.swift |
| **Vekten påvirker ikke utfallet i dag.** Én positiv post med felles emne gir positiv dom, og én negativ post med felles emne gir veto for alt innholdet. | retrieved | PalazzoScaffold::Sources/App/Models/PalazzoSignalGraphMatcher.swift, `f548282` |
| Hvert trykk er en egen post, og trykk på samme artikkel stables. | retrieved | PalazzoSignalGraph.swift (én `Entry` per post) |
| Artikkelavvisningen bruker den **første** negative posten for artikkelen. Et senere positivt trykk opphever den ikke. Det strider mot «siste trykk gjelder». | retrieved | PalazzoSignalGraphMatcher.swift (`rejection = graph.entries.first { $0.negative && … }`) |
| Postene endres aldri. Grafen bygges på nytt fra den ordnede rekken, så justering kan beregnes uten å skrive om historikk. | retrieved | PalazzoSignalGraph.swift («Rebuild, never edit») |
| Vetofelle-rettingen er pushet, men ikke merget inn i `pdd/palazzo-2026-09-14`. | retrieved | HAVEN-Deploy/_handoff/PALAZZO-VETO/test-siste.md |
| Binding pinner CellProtocol til en fast revisjon (`b5b7282`), så pinnen må løftes før Binding viser A1. | retrieved | Binding::Binding.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved, origin/main |
| `modifiers.wrap` finnes og rendres i begge renderere, så lister og HStack brytes som brikker. | retrieved | CellProtocol::Sources/CellBase/Skeleton/SkeletonDescription.swift (`wrap`), CellApple::…/CellListView.swift:187 og …/Skeleton/FlowLayout.swift, CellScaffold::Public/js/skeleton-runtime.js |
| At `wrap` virker sammen med `childrenKeypath`, eller i en liste inne i en rad | unavailable | Prøves i Porthole-preview før bygging (A5) |

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.palazzo-tolkning-og-vektjustering.root | Gjestens egne trykk styrer det hun får, og hun kan se hvordan | — | Om en artikkel er stengt, og om emnene teller for eller mot, følger det hun sist sa. Styrken justeres av flere trykk. Hun kan se hva hvert trykk ble tolket som. | Alle bladene under er grønne | candidate |
| …tolkning-synlig | Hun kan se tolkningen uten at den tar plass | root | Etter et trykk står én lukket rad under knappene. Emnene vises først når hun åpner raden. | A1–A4 | candidate |
| …native-tre-liste (A1) | Den native rendereren viser tre-lister som Porthole | tolkning-synlig | `CellListView` rendrer `childrenKeypath`: lukket når `expandedStateKeypath` gir tom liste eller ikke kan løses, med lokal åpne/lukke uten rundtur til cellen. Oppførselen er lik Porthole. | test.native.tree-list, test.native.tree-parity | candidate |
| …reaksjon-lesbar (A2) | Entitetscellen gir hennes gjeldende reaksjon på én artikkel | tolkning-synlig | GET `entity.article.reaction.<artikkelnøkkel>` gir 0 eller 1 rad `{label, children:[{label}]}`. Raden bygges fra hennes siste egne reaksjonspost for artikkelen og emnene som er frosset på den. Bare eieren får lese. | test.cell.reaction-row, test.cell.auth-negative | candidate |
| …artikkelflate (A3) | Artikkelflaten viser raden på riktig sted og holder den oppdatert | tolkning-synlig | Før første trykk vises ingen rad. Etter et trykk vises én lukket rad. Etter et nytt trykk viser raden den nye reaksjonen, i begge renderere. | test.skeleton.no-unreachable-elements, test.article.row-refresh | candidate |
| …emner-som-brikker (A5) | Emnene vises som brikker, slik bildet viser | tolkning-synlig | Åpnet rad viser emnene som brikker som brytes over linjer. Det bygges med `wrap` fra dagens format, uten nytt skjelettelement. Går det ikke, stopper arbeidet og spørsmålet går til Kjetil. | test.gui.chips-porthole, test.gui.parity | candidate |
| purpose://gui.parity-with-approved-image (A4) | Flaten ser ut som det godkjente bildet | tolkning-synlig | Skjermbilder av lukket og åpen rad ligger ved siden av `images/artikkel-tolkning-v1.png`. Kjente avvik er listet i §3. | test.gui.parity | pakke |
| …gjentatte-trykk-justerer | Flere trykk på samme artikkel justerer vektene i stedet for å stable dem | root | Trykkene på én artikkel blir én gjeldende vekt per artikkel. Hvor mye hvert trykk flytter vekten, velger Kjetil fra benken (B5). | B1–B5 | candidate |
| …siste-trykk-gjelder (B1) | Siste trykk avgjør om artikkelen er stengt, og om emnene teller for eller mot | gjentatte-trykk-justerer | Artikkelen er stengt bare når siste trykk på den er «Ikke for meg». Emnenes fortegn følger siste trykk, så raden og virkningen aldri peker hver sin vei. Styrken glir mot det nye trykket (modell a, godkjent 28.9). | test.weights.last-tap-decides, test.weights.sign-follows-last | candidate |
| …veto-bare-artikkelen (B2) | «Ikke for meg» stenger bare artikkelen | gjentatte-trykk-justerer | Artikkelen er stengt. Emnene får negativ vekt som trekker ned annet innhold med felles emne, men ikke stenger det. | test.weights.veto-article-only | candidate |
| …vekt-avgjor (B3) | Vekten avgjør om noe tilbys | gjentatte-trykk-justerer | Innhold tilbys bare når vektsummen over felles emner når terskelen, og det sorteres etter summen (Kjetil 28.9). Terskelen velges fra benken. | test.weights.threshold, test.weights.monotone | candidate |
| …justering-parametrisert (B4) | Hvor mye et trykk justerer, er samlet på ett sted | gjentatte-trykk-justerer | Alle tallene (vekt per reaksjon, hvor langt et nytt trykk flytter vekten, negativ emnevekt, terskel) ligger i én navngitt struktur. Ingen tall ligger spredt i koden. | test.weights.policy-single-source | candidate |
| …vektbenk (B5) | Vi kan prøve oss fram | gjentatte-trykk-justerer | Simulerte gjester, hver med egne formål og en rekke trykk, kjøres gjennom **produksjonens** matcher for flere parametersett. Dagens oppførsel er med som referanse. Utdata er én tabell over hva hver gjest får under hvert sett. | test.maal.produksjonsvei, test.bench.inert-by-default, test.bench.has-null-reference | candidate |
| …prinsipper-holder | Prinsippene fra 24.9 gjelder fortsatt | root | Veto for artikkelen, «uavklart» ved ufullstendig søk, avvisningsminne (nå: siste trykk) og bare egne poster er dekket av tester. Eksisterende tester er grønne. | test.regression, test.principles | candidate |
| purpose://quality.build-and-regression | Alt virker | root | Se pakken pkg.std.everything-works. | test.build, test.regression | pakke |

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.
Hvert bladformål skal ha en test i §5. Et formål uten observerbart Goal er ikke klart til arbeid.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en endring av hvordan huset merker artikler. Emnene vises slik huset skrev dem (Kjetil 26.9).
- Ikke kommentarposten. Emnene på den vises ikke, og vekten på egne ord er uendret.
- Ikke en endring i CellBase-runtimen eller `InterestPurposeWeightedSum`.
- Ikke valg av endelige tall. Benken viser utfallene, Kjetil velger, og valget skrives inn som standardverdier.
- Ikke gjestens redigering av tallene ennå. Tallene er gjestens data (Kjetil 28.9) og skal kunne endres av henne senere. Her gjøres de bare klare for det: én Codable-struktur uten logikk. Selve redigeringen blir et eget formål: `purpose://candidate.palazzo-tolkning-og-vektjustering.gjesten-eier-vektene`.
- Ikke endringer i Porthole, som allerede støtter tre-lister.
- Ikke et nytt oppsett i biblioteket ennå. Viser justeringsmodellen seg holdbar, foreslås den til `Tools/PurposePackages/` i P6.

Kapabiliteter og avhengigheter oppgaven bygger på:

| Kapabilitet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| Vetofelle-rettingen `f548282` | PalazzoScaffold, grenen `codex/palazzo-vetofelle-20260924` | Palazzo-arbeidet bygger på denne grenen. Merge inn i `pdd/palazzo-2026-09-14` er Kjetils valg, og bør skje før arbeidet bygges oppå. | ja |
| Native tre-liste på CellProtocol main (A1) | CellProtocol::Sources/CellApple/… | Egen worktree fra origin/main, ikke den delte `../CellProtocol`. Må landes med `HAVEN-Deploy/_handoff/LANDING/land-cellprotocol.sh`, og CI må være grønn. Hele regresjonen dekker de andre brukerne av `CellListView`. Kjetils regel: testet mot funksjon og formål før main. Krever ja i boksen øverst. | ja, for A3/A4 |
| At PalazzoScaffold og Binding bygger mot en CellProtocol som har A1 | PalazzoScaffold::Package.swift. Binding: ukjent (se §0). | PalazzoScaffold har bygget mot den delte `../CellProtocol`, som står på en annen tråds gren, med GitHub som reserve. | ja, for A4 |
| Kjørende gjesteflate for paritet: Binding mot Palazzo via bro | lesson.scaffold-without-porthole-host-has-no-preview | Egen slice, ikke del av implementeringen | ja, for A4 |
| Rendereren leser lista på nytt etter trykket | ukjent, må testes | Leses den ikke på nytt, står raden stille. Da er A3 rød. | ja, for A3 |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Referansebilde: artikkel med raden lukket og åpen (variant B) | bilde | `images/artikkel-tolkning-v1.png` | godkjent 2026-09-26 («Vi går for B») | ja |
| Native tre-liste i CellApple, lukket og åpen | testutdata + skjermbilde | TESTRESULT.md#native-tree, `images/actual/` | Porthole-oppførselen | — |
| Artikkelflaten i Binding mot Palazzo: før trykk, lukket, åpen, etter nytt trykk | kjørende flate + skjermbilder | ACCEPT.md#parity | `images/artikkel-tolkning-v1.png` | — |
| Vektbenken: hva hver simulerte gjest får under hvert parametersett og med dagens oppførsel | fil | `maaling/vektbenk-v1.md` | — | du velger sett |
| Commit på CellProtocol main med grønn CI, og pushet Palazzo-gren | commit + CI | TESTRESULT.md#landing | — | — |

Kjente avvik fra det godkjente bildet. Hvert må godtas eller endres:

| # | Avvik | Hvorfor | Godkjent |
|---|---|---|---|
| 1 | ~~Emnene vises ikke som brikker.~~ **Rettes (Kjetil 28.9): «Fiks avviket».** Brikkene bygges med `wrap` (A5). | — | rettes |
| 2 | **Teksten for «Ikke for meg»** er «Registrert: Ikke for meg · tolket som mindre interesse for N emner». | Artikkelen er stengt, og emnene trekker ned annet innhold (B2). | — |
| 3 | **Raden viser siste trykk.** Styrken bak kan være justert av tidligere trykk, men fortegnet følger alltid det raden viser (B1). | Flere trykk justerer vekten. | — |

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
- **lesson.judgement-without-decoys-yields-all-yes** (2026-09-14, major): Første dommerrunde for formålsoppslag ga 197 «ja» og 0 «nei» på 197 rader. Fasiten skilte ikke mellom noen kandidater, og tidskurven (7 094 s på første oppgave, 25–44 s på de fem siste) viste at de siste var klikket gjennom, ikke dømt.
    - forebygging: En menneskelig fasit-runde skal alltid blande inn lokkeduer fra utenfor topp-10, blindt, så et «nei» kan attesteres og en alle-ja-dommer avsløres. Kriteriet skal kreve et navn («hvilket valg/test/avgrensning ville den endret»), ikke et ja. Maks fem oppgaver per økt. Og en runde uten negativer merkes instrumenteringsrunde — den teller ikke som fasit, samme regel som PurposeContract håndhever for null- og positiv referanse.
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

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance
- purpose://self-determination.data.use-purpose [candidate] — Purpose binding for data use

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.native.tree-list | A1 native-tre-liste | CellApple-tester som bygger en `SkeletonList` med `childrenKeypath`, og sjekker: lukket når `expandedStateKeypath` gir `[]` eller ikke kan løses; alt åpent når feltet mangler; åpne/lukke endrer bare synlige rader og sender ingenting til cellen | TESTRESULT.md#native-tree | venter |
| test.gui.chips-porthole | A5 | Porthole-preview av artikkelflaten med åpen rad, iPhone-bredde. Skjermbilde ved siden av referansen. To oppbygginger prøves, se PLAN WP2 | `images/actual/porthole-brikker-v1.png` | venter |
| test.native.tree-parity | A1 | Samme skjelett og data i Porthole (eksisterende `playwright/skeleton-list-tree.spec.js`) og i native: samme synlige rader i samme rekkefølge, lukket og åpen | TESTRESULT.md#native-tree | venter |
| test.cell.reaction-row | A2 reaksjon-lesbar | Ingen reaksjon → 0 rader. Ett trykk → 1 rad med emnene frosset på posten. To trykk → raden viser det siste. Huset endrer emnene på artikkelen etterpå → raden er uendret | TESTRESULT.md#cell | venter |
| test.cell.auth-negative | A2 | Annen requester, feil keypath og `purpose://prompt.unknown` blir alle avvist | TESTRESULT.md#auth | venter |
| test.skeleton.no-unreachable-elements | A3 artikkelflate | `SkeletonReachabilityAudit` på artikkelkonfigurasjonen. Ingen funn, og de tre reaksjonsknappene og kommentarfeltet er nåbare | TESTRESULT.md#reachability | venter |
| test.article.row-refresh | A3 | I kjørende flate, fra artikkel uten reaksjon: (1) «Interessant» → én lukket rad; (2) åpne raden, trykk «Vil smake» → raden viser «Vil smake» og er fortsatt åpen; (3) «Ikke for meg» → teksten fra avvik 2; (4) «Vil smake» igjen → positiv tekst. Ingen navigering ut og inn mellom trinnene. Skjermbilde per trinn, i Binding. | ACCEPT.md#parity | venter |
| test.gui.parity | A4 | Skjermbilder i samme viewport ved siden av referansen, med avvikene fra §3 listet | ACCEPT.md#parity | venter |
| test.weights.last-tap-decides | B1 | [Ikke for meg, Vil smake] → artikkelen er ikke stengt. [Vil smake, Ikke for meg] → stengt. [Ikke for meg, Interessant, Ikke for meg] → stengt | TESTRESULT.md#weights | venter |
| test.weights.veto-article-only | B2 | «Ikke for meg» på caponata. En rett med «oliven» er ikke stengt, men summen for den er lavere enn uten trykket. Selve artikkelen er stengt | TESTRESULT.md#weights | venter |
| test.weights.threshold | B3 | Innhold under terskelen blir ikke anbefalt. Innhold på eller over blir det | TESTRESULT.md#weights | venter |
| test.weights.monotone | B3 | (a) Et positivt trykk på en *annen* artikkel senker aldri summen for innhold med felles emne. (b) Et sterkere trykk («Vil smake») gir aldri lavere sum enn et svakere («Interessant») på samme plass i rekken. Kjøres på mange tilfeldige rekker med fast frø, slik at kjøringen kan gjentas. | TESTRESULT.md#weights | venter |
| test.weights.repeat-bounded | B (kjernen) | «Vil smake» én, to og tre ganger på samme artikkel. Vekten øker ikke over en øvre grense, og den er ikke summen av trykkene | TESTRESULT.md#weights | venter |
| test.weights.sign-follows-last | B1 | Etter [Ikke for meg, Vil smake] teller emnene for, ikke mot. Etter [Vil smake, Ikke for meg] teller de mot. Modell (a), godkjent 28.9 | TESTRESULT.md#weights | venter |
| test.weights.single-positive-gets-offer | B3 | En gjest med ett positivt trykk får minst ett tilbud med standardtallene, med mindre Kjetil uttrykkelig godtar noe annet i WP6 | TESTRESULT.md#weights | venter |
| test.weights.policy-single-source | B4 | Søk etter tallkonstanter i graf- og matcherfilene. Ingen vekter eller terskler utenfor `PalazzoWeightPolicy` | ACCEPT.md#policy | venter |
| test.maal.produksjonsvei | B5 vektbenk | Benken kaller `PalazzoSignalGraphMatcher.match` med policyen, ikke en kopi av logikken | TESTRESULT.md#bench | venter |
| test.bench.inert-by-default | B5 | Uten miljøvariabelen `PALAZZO_WEIGHT_BENCH_PATH` gjør benken ingenting og skriver ingenting | TESTRESULT.md#bench | venter |
| test.bench.has-null-reference | B5 | Tabellen har en kolonne «dagens oppførsel» målt på `f548282`. Et parametersett som gir samme tabell som dagens, er merket som likt | `maaling/vektbenk-v1.md` | venter |
| test.principles | prinsipper-holder | Uavklart ved utløpt budsjett, bare `source == "self"`, veto for artikkelen og ingen ny anbefaling av en artikkel hun allerede har reagert på. Én test per prinsipp, nye eller eksisterende, navngitt | TESTRESULT.md#principles | venter |
| test.build | quality | `swift build` i CellProtocol og PalazzoScaffold. Binding-bygg for A4 | TESTRESULT.md#build | venter |
| test.regression | quality | Hele testmengden på ren eksport av utgangsrevisjonen mot arbeidstreet (`land-cellprotocol.sh`, og `test-vetofelle.sh`-mønsteret for Palazzo) | TESTRESULT.md#regression | venter |
| test.docs-updated | quality | Kodekommentarene i graf og matcher, pluss skjelettdokumentasjonen for native støtte av `childrenKeypath` | ACCEPT.md#docs | venter |
| test.status-current | quality | STATUS.md mot filene i mappen | ACCEPT.md#status | venter |

## 6. Åpne spørsmål til Kjetil

Ordforklaring: *matcheren* er koden som avgjør hva gjesten tilbys. *Benken* er en testkjøring med oppdiktede gjester som viser hva hver av dem ville fått. *Vekt* er hvor sterkt et emne teller.

Avgjort 28.9: modell (a) og terskel. Disse to endrer ikke treet og kan besvares når benken er kjørt:

1. ~~Fast i koden, eller skal gjesten kunne endre tallene?~~ **Avgjort 28.9:** «Fast i koden nå, men det er brukerens data så brukeren må kunne endre senere.» `PalazzoWeightPolicy` lages som data (Codable, uten logikk), og gjestens redigering blir et eget formål senere (§2).
2. ~~Benkens gjester~~ **Avgjort 28.9:** «Bruk de simulerte gjestene du foreslo.» Sju, hver med sitt eget formål. Én ombestemmer seg, én liker Palermo men ikke fritert mat, én er vegetar, én trykker mye «Interessant» og aldri noe annet, én gir bare «Ikke for meg», én trykker samme knapp flere ganger, og én har trykket «Interessant» én gang og ingenting mer. Den siste vokter terskelen. Legg gjerne til flere.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-26 | Opprettet | Losen |
| 1 | 2026-09-26 | §0–§3, §5 og §6 skrevet fra G1-GUI-valget (B), Kjetils tre svar og kildelesning. Rettelse: den native rendereren ligger i CellProtocol/CellApple, ikke i Binding. | Losen |
| 2 | 2026-09-26 | Fabels gjennomgang: B3 merket som Losens slutning og flyttet til §6. Modellen for fortegn og styrke er gjort til et valg. Monotonitesten er rettet, så den ikke motsier glidende vekt. Nye tester: repeat-bounded og sign-follows-last. Row-refresh er utvidet. Hvert avvik har egen godkjent-rute. Beslutningsboksen og ordforklaringen er lagt til. | Losen |
| 4 | 2026-09-28 | G2 godkjent. §6 besvart: tallene er fast i koden nå, men er gjestens data og skal kunne endres av henne senere (ny avgrensning i §2). Benkens sju gjester er godkjent. | Losen |
| 3 | 2026-09-28 | Kjetils svar på G1-valgene: CellProtocol main, modell (a), terskel og «fiks avviket». Nytt formål A5 (brikker med `wrap`). Audit: Binding pinner CellProtocol til `b5b7282`, og `wrap` finnes i begge renderere. **G1 godkjent.** Etter Fabels gjennomgang av planen: sju gjester i benken, en test for at ett positivt trykk gir tilbud, og sign-follows-last gjelder bare modell (a). | Losen |
