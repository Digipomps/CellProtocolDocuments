# Formålsspesifikasjon — palazzo husk det jeg sa

Oppgavemappe: `PDD_palazzo-husk-det-jeg-sa_2026-09-05` · Opprettet 2026-09-05 · Iterasjon 2 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> D2 Ja, tillitspakken er for å gjøre dommen verifiserbar. D3 Ja - orverraskelse som grant. Ta «husk det jeg sa» nå.

Kontekst (Kjetils beslutninger samme dag, `PalazzoComunaleScaffold/docs/Vurdering_Signalmatching_Familietilhorighet_2026-09-05.md` §9): D1 matching i gjestens entitet · D2 dom + forklaring gjesten har godkjent + tillitspakke · D3 samtykke som signert Agreement, overraskelse er et grant (innsyn + handling) · D4 «husk det jeg sa» = gjestekommentar × menyendring, ett lag, én polaritet · D5 Palazzo betaler.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| PalazzoScaffold bygger og 48 tester er grønne (`swift build/test --disable-sandbox`) | retrieved | `PalazzoComunaleScaffold/docs/Rapport_PalazzoScaffold_Celler_2026-09-03.md:8–22` |
| Gjestens entitet har poster av typene visit/booking/interaction/purpose/interest/constraint med `source` = `self` / `house` / `staff:<uuid>`, `tags`, `attributes` | retrieved | `PalazzoScaffold/Sources/App/Models/PalazzoEntityModels.swift:9–30` |
| Det finnes allerede en match-spørring i gjestens entitet: `insight.query.interests.match` tar husets interesseliste og **returnerer overlap-listen + score** til requester med aktiv policy | retrieved — **strider mot D2** (lekker gjestens etiketter, ikke bare dom) | `PalazzoScaffold/Sources/App/Cells/PalazzoEntityCell.swift:226–263` |
| Samtykke er én bit per requester (`PalazzoConsentPolicy`, `LookupCondition target.consent.policy.autoApprove.$identity`); kontrakter signerer seg selv når biten står | retrieved — **avgrensning:** granularitet er requester × keypath, ikke per treff; per-treff-grant finnes ikke | `PalazzoScaffold/Sources/App/Support/PalazzoConsentLedger.swift:7–40`, `PalazzoScaffoldContract.swift:74–93` |
| Samtykkemodal med «Godkjenn denne gangen / Godkjenn alltid / Avslå» finnes som CellConfiguration (`.modal`) | retrieved | `PalazzoScaffold/Sources/App/Skeleton/PalazzoConsentConfigurationFactory.swift:52, 112–114` |
| Huset publiserer meny (`content.published`, `menuHighlights`), og `content.publish` kan avgjøre hva som endret seg (`differences()`) | retrieved — **avgrensning:** ingen hendelse/signal sendes ut ved publisering, og `menuHighlights` har ingen stabil id per rett | `PalazzoScaffold/Sources/App/Cells/PalazzoContentCell.swift:66–91, 297–309` |
| «Signert Agreement» i CellProtocol = utsteder-signert, subjekt-bundet snapshot (`Contract.ownerSignedSnapshot`); ikke bilateral signering | retrieved — gjesten er utsteder, huset er subjekt; «to grants» = to keypaths/kontrakter fra gjesten, ikke to signaturer | `CellProtocolDocuments/Book/04_Agreements_Contracts.md §8–9` |
| Custodial gjesteidentitet fra VaporIdentityVault kan signere (`Identity.sign`) | retrieved — PalazzoAccessContractCell krever bevis for signeringsnøkkel | `PalazzoScaffold/Sources/App/Cells/PalazzoAccessContractCell.swift:72, 109, 613` |
| Gjesteflaten «Palazzo Gjest» finnes som CellConfiguration | retrieved | `PalazzoScaffold/Sources/App/Skeleton/PalazzoGuestConfigurationFactory.swift:15–16` |
| Flerlags signalmatcher i CellProtocol (Book-eid, Swift) | unavailable — besluttet, ikke bygd. Denne oppgaven bygger ett lag lokalt i PalazzoEntity bak et grensesnitt matcheren senere kan erstatte | beslutning 2026-09-04 (minne) |
| Kelnerbrief v1 (prioritert foran dette i D4) | unavailable — ikke levert. Kelnersiden i denne oppgaven begrenses til data-keypath + én linje; se §6.2 | `PalazzoComunaleScaffold/research/2026-09-02/gjestebrief_concierge.md` A1 |
| Formålsgren `purpose://service.hospitality` i Book 23 | unavailable — 36 noder finnes i `PalazzoComunaleScaffold/purposes/`, ikke i Book 23 ennå | `PalazzoComunaleScaffold/docs/Scaffold_Avgrensning_og_Formal_2026-08-26.md` |

Ingen `recalled`-rad bærer planen.

## 1. Formålstre

Rot og invariant: gjesten opplever at Palazzo husker det gjesten sa — og det gjesten sa forlater ikke gjesten før gjesten selv sier ja. Overraskelsen skal kunne forklares med gjestens egne ord.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.palazzo-husk.root | «Husk det jeg sa» | purpose://self-determination.data.manner (Book 23) · `service.hospitality.F` (Palazzo-formålssett, familiefølelse) | En gjest som skrev en kommentar får, når huset publiserer en menyendring som treffer den, et treffkort på egen telefon; sier gjesten ja, ser kelneren én linje «Husker: …» med gjestens ord; sier gjesten nei eller ingenting, ser huset ingenting. | Ende-til-ende-test §5 `test.husk.e2e` + G3 side-om-side | candidate |
| purpose://candidate.palazzo-husk.signal-published | Huset publiserer menyendring som signal | root | `content.publish` som endrer `menuHighlights` produserer et signal med stabil id, versjon, tagger/nøkkelord, tittel og gyldighetsvindu, lesbart under `content.published`-kontrakten (publisert lesing). Uendret meny gir intet nytt signal. Kompileringen skjer hos huset (D5). | `test.husk.signal` | candidate |
| purpose://candidate.palazzo-husk.signal-tags-approved-by-house | Tagger foreslås, huset godkjenner | signal-published | Ved publisering av en ny/endret rett avledes taggforslag deterministisk av rettens navn og ingredienser (ordliste, ingen modell), vises huset i draft-flaten for redigering, og først godkjente tagger kompileres inn i signalet. Et signal uten godkjente tagger publiseres ikke. | `test.husk.tags` | candidate |
| purpose://candidate.palazzo-husk.match-in-guest-entity | Matching skjer i gjestens entitet | root | Gjestens `interaction`-poster med `source == self` matches mot signalets tagger/nøkkelord, ett lag, positiv polaritet. Resultatet lagres som ny post av typen `match` i gjestens entitet med tilstand `pending`. Ingen requester utenfor eieren kan lese en `match` i `pending`. Dom-typen har tre verdier (positiv / negativ / ikke avgjort) fra start, selv om bare positiv produseres nå. | `test.husk.match`, `test.cell.auth-negative` | candidate |
| purpose://candidate.palazzo-husk.explanation-in-guest-words | Forklaring i gjestens ord | match-in-guest-entity | Forklaringen lages deterministisk uten modell: «Fordi du skrev "<ordrett sitat>" <dato>» + signalets tittel. Den vises gjesten i treffkortet før noe deles, og bare den godkjente teksten kan krysse grensen. | `test.husk.explanation` (streng ⊆ gjestens post + signaltittel) | candidate |
| purpose://candidate.palazzo-husk.two-grants | Overraskelse er et grant: innsyn + handling | root | Gjesten avgjør i samtykkemodalen (Godkjenn denne gangen / Godkjenn alltid / Avslå), per grant: **innsyn** (huset får dommen) og **handling** (huset får gjøre noe ved bordet). Hver godkjenning er en gjeste-utstedt, signert kontrakt med huset som subjekt og med treff-id + sitting som omfang. «Alltid» = stående policy for signaltypen *menyendring* hos dette huset. Avslag og ubesvart gir huset ingenting. | `test.husk.grants` (4 tilfeller: ingen / innsyn / innsyn+handling / avslått), `test.cell.auth-negative` | candidate |
| purpose://candidate.palazzo-husk.trust-packet | Tillitspakke gjør dommen verifiserbar | two-grants | Når innsyn er gitt, utsteder gjestens entitet en pakke signert av gjestens identitet: `signalRef` (id+versjon), `verdict` (polaritet), `explanation` (godkjent tekst), `provenanceHash` (hash av posten forklaringen peker til, uten posten), `grantRefs`, `sittingRef`, `issuedAt`. Huset kan verifisere signatur og signalRef; endret pakke feiler; pakken inneholder ingen felt fra posten ut over `explanation` (allowlist). | `test.husk.trust-packet` (verifiser / manipuler / allowlist) | candidate |
| purpose://candidate.palazzo-husk.house-receives-packet-only | Huset mottar bare pakken | root | Huset (via `PalazzoHouse`) mottar pakken på ett endepunkt og eksponerer den til kelner som keypath `brief.remembered` (liste av `explanation`-tekster med signaltittel). Ingen endepunkt i scaffoldet returnerer gjestens etiketter, overlap-lister eller score uten per-treff-grant. | `test.husk.house-endpoint`, `test.husk.no-label-leak` (antiformål) | candidate |
| purpose://candidate.palazzo-husk.guest-sees-what-house-got | Gjesten ser hva Palazzo har fått | root | Gjesteflaten har en seksjon «Delt med Palazzo» som lister utstedte pakker (signaltittel, forklaring, grants, dato) med knapp «Trekk tilbake» som setter treffet til `revoked` og gjør `brief.remembered` tom for det treffet ved neste lesing. | `test.husk.revoke` + GUI-bilde | candidate |
| purpose://candidate.palazzo-husk.no-inference | Skal ikke: treff uten gjestens egne ord | root · polarity: prohibited | Ingen `match` oppstår fra poster med `source != self` (husets eller personalets notater), og huset ser aldri et treff i `pending`, `declined` eller `revoked`. | `test.husk.no-inference` | candidate |
| purpose://gui.expectation-agreed-before-build | Bilde før kode (pakke) | pkg.std.gui-surface | Treffkort (tom/fylt/feil), samtykkemodal med to grants, «Delt med Palazzo», kelnerlinje — godkjent som bilder. | `test.gui.reference-image-exists` | active |

Utenfor treet (bevisst): flerlags matching, negativ polaritet på allergen, innholdssignaler ut over meny, budsjett-«ikke avgjort» som produsert dom. Alle fire er neste skritt i D4 og skal ikke smugles inn her.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke den flerlags signalmatcheren (Book-eid). Ett lag, tagg/nøkkelord-match, lokalt i `PalazzoEntity`, bak et protokoll-grensesnitt (`PalazzoSignalMatcher`) slik at matcheren senere kan byttes inn uten å røre grants og pakke.
- Ikke kelnerbrief v1. Kelnersiden får én keypath (`brief.remembered`) og én linje i eksisterende staff-konsoll; briefens layout og rekkefølge (A1) er ikke denne oppgaven.
- Ikke innholdspublisering/artikler/kalender som signalkilde. Bare `menuHighlights`.
- Ikke språkmodell noe sted i kjeden. Forklaringen er sitat + mal.
- Ikke en endring i CellProtocol. Alt skjer i PalazzoScaffold-pakken (regelen fra fase 2).

| Kapabilitet / avhengighet | Kilde (fil) | Avgrensning | Må virke før test? |
|---|---|---|---|
| `PalazzoEntity` med poster og `entity.record`-append | `PalazzoEntityCell.swift:98–171` | Ny Kind `match` og tilstand må legges til modellen; eksisterende 48 tester må forbli grønne | ja — `test.build`, `test.regression` |
| Samtykkebit + `LookupCondition`-mal | `PalazzoConsentLedger.swift`, `PalazzoScaffoldContract.swift:86` | Dekker requester × keypath. Per-treff-omfang må uttrykkes som keypath-suffiks (`match.<id>.verdict`) eller som egen kontrakt per treff — velges i PLAN | ja |
| Samtykkemodal `.modal` | `PalazzoConsentConfigurationFactory.swift` | Viser i dag én liste av keypaths og tre knapper; må kunne vise to grants med hver sin avgjørelse. Om skeleton-formatet tillater to knapperader i én modal verifiseres i P1-GUI | ja — bildet |
| `content.publish` + `differences()` | `PalazzoContentCell.swift:157–175, 297–309` | Ingen stabil id på `menuHighlights`-elementer; må legges til for `signalRef` | ja |
| Gjeste-utstedt signert kontrakt med huset som subjekt | `Book/04 §8–9`, `PalazzoAccessContractCell.swift:324–357` | Registeret håndterer i dag husets maler; gjeste-utstedt kontrakt per treff er ny bruk av samme mekanisme, ikke ny mekanisme | ja — `test.husk.grants` |
| Porthole-preview av CellConfiguration for gjesteflaten | `cellconfiguration-skeleton-authoring` | Bare for bildene; hvis Porthole ikke når PalazzoScaffold lokalt, mockup i samme størrelse med liste over hva skeleton ikke kan rendre | ja — G1-GUI |
| Codex kjører `swift build/test --disable-sandbox` på Kjetils maskin | `Rapport_PalazzoScaffold_Celler_2026-09-03.md:24` | Ingen Swift-toolchain i skyen eller VM; alle byggtester utføres av Codex | ja |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Treffkort på gjestens telefon, fylt: signaltittel, forklaring «Fordi du skrev "…"», to grants med tre valg | bilde | `images/` | `images/gjest-treffkort-fylt-v1.png` | nei |
| Treffkort, tom tilstand (ingen treff) — seksjonen skjules, ikke plassholdertekst | bilde | `images/` | `images/gjest-treffkort-tom-v1.png` | nei |
| Treffkort, feil (signal utløpt før svar) | bilde | `images/` | `images/gjest-treffkort-feil-v1.png` | nei |
| «Delt med Palazzo» med én pakke og «Trekk tilbake» | bilde | `images/` | `images/gjest-delt-v1.png` | nei |
| Husets draft-flate: foreslåtte tagger per rett med rediger/godkjenn før publisering | bilde | `images/` | `images/hus-tagger-v1.png` | nei |
| Kelnerkonsoll med linjen «Husker: …» (én linje i eksisterende konsoll) | bilde | `images/` | `images/kelner-husker-v1.png` | nei |
| Skeleton-JSON bildene er rendret fra | fil | `skeleton/` | `skeleton/gjest-treffkort.json` m.fl. | nei |
| Kontrakt for signal, match, grants og tillitspakke med positive/negative fixtures | fil | `contract/palazzo_remember_contract_v0.json` + `contract/fixtures/` | — | nei |
| Dataflyt huset → signal → gjestens entitet → grants → pakke → hus → kelner | fil | `dataflow.md` | — | nei |
| Testutdata: signal, match, forklaring, grants (4 tilfeller), pakke (verifiser/manipuler/allowlist), no-inference, revoke, e2e, auth-negative, build, regression | testutdata | `TESTRESULT.md` | ankre `#signal #match #explanation #grants #trust-packet #no-inference #revoke #e2e #auth #build #regression` | nei |
| Kjørende gjesteflate i PalazzoScaffold der Kjetil selv skriver en kommentar, huset publiserer en menyendring (seed-skript), treffkortet dukker opp, og «Husker: …» vises hos kelneren etter ja | kjørende flate | Porthole mot lokal PalazzoScaffold | seed-skript i `handoff/` | nei |

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
- purpose://human-agency [draft] — Human agency and understanding
- purpose://contact.communication [draft] — Contact and communication
- purpose://event.privacy-preserving-networking [draft] — Privacy-preserving event networking
- purpose://questionnaire.campaign.complete [active] — Complete questionnaire campaign
- purpose://questionnaire.respondent.form [active] — Respondent questionnaire form
- purpose://questionnaire.delivery.consent [active] — Questionnaire delivery and consent
- purpose://gui.quality.functional-accessible [active] — Functional accessible GUI
- purpose://governance [active] — Governance
- purpose://questionnaire.access.audit [active] — Questionnaire access audit
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
| test.husk.signal | purpose://candidate.palazzo-husk.signal-published | XCTest: publish patch som endrer `menuHighlights` → nytt signal med stabil id/versjon/tagger; publish uten endring → ingen. | TESTRESULT.md#signal | venter |
| test.husk.tags | purpose://candidate.palazzo-husk.signal-tags-approved-by-house | XCTest: draft med ny rett → forslag fra ordliste; publish uten godkjenning → intet signal; redigert+godkjent → signal bærer nøyaktig de godkjente taggene. | TESTRESULT.md#tags | venter |
| test.husk.match | purpose://candidate.palazzo-husk.match-in-guest-entity | XCTest: post `interaction`/self «vil prøve chambre» + signal tag `chambre` → `match` pending; requester=hus får denied på match-keypath. | TESTRESULT.md#match | venter |
| test.husk.explanation | purpose://candidate.palazzo-husk.explanation-in-guest-words | XCTest: forklaring = mal + ordrett sitat + dato + signaltittel; ingen andre tegn fra posten. | TESTRESULT.md#explanation | venter |
| test.husk.grants | purpose://candidate.palazzo-husk.two-grants | XCTest, 4 tilfeller: ingen svar / innsyn / innsyn+handling / avslått → hva huset kan lese/skrive. «Alltid» → neste signal av samme type auto-godkjennes, annen type ikke. | TESTRESULT.md#grants | venter |
| test.husk.trust-packet | purpose://candidate.palazzo-husk.trust-packet | XCTest: verifiser signatur+signalRef grønt; endret `explanation` → rødt; pakkens nøkler ⊆ allowlist; `provenanceHash` = hash(post) uten post. | TESTRESULT.md#trust-packet | venter |
| test.husk.house-endpoint | purpose://candidate.palazzo-husk.house-receives-packet-only | XCTest: huset mottar pakke → `brief.remembered` viser forklaring; ugyldig pakke avvises. | TESTRESULT.md#house | venter |
| test.husk.no-label-leak | purpose://candidate.palazzo-husk.house-receives-packet-only (antiformål) | Inspeksjon + XCTest: ingen keypath lesbar for hus returnerer `matches`/`interests`/`score` uten per-treff-grant; `insight.query.interests.match` avstemt etter §6.1. | TESTRESULT.md#no-label-leak | venter |
| test.husk.revoke | purpose://candidate.palazzo-husk.guest-sees-what-house-got | XCTest: «Trekk tilbake» → `brief.remembered` tom for treffet; pakken listes som tilbakekalt hos gjesten. | TESTRESULT.md#revoke | venter |
| test.husk.no-inference | purpose://candidate.palazzo-husk.no-inference | XCTest: post med `source: house` / `staff:…` gir aldri match; pending/declined/revoked usynlig for hus-requester. | TESTRESULT.md#no-inference | venter |
| test.husk.e2e | purpose://candidate.palazzo-husk.root | Kjørende: seed-skript → gjest skriver → publish → treffkort → ja → kelnerlinje; skjermbilder i ACCEPT.md. | TESTRESULT.md#e2e, ACCEPT.md#parity | venter |

## 6. Åpne spørsmål til Kjetil

Besvart 2026-09-05: 1 → fjern liste og score (deprecated). 2 → keypath + én linje i konsollen, med bilde. 3 → ordrett sitat (forslag, ikke motsagt). 4 → signaltype × hus, per grant. 5 → **avledes som utgangspunkt, presenteres huset for manuell redigering og godkjenning** — ny bladnode `signal-tags-approved-by-house` i §1, ny bilderad i §3, `test.husk.tags` i §5.

Opprinnelige spørsmål:

1. **`insight.query.interests.match` lekker etiketter.** Den returnerer i dag overlap-listen og score til huset. Forslag: fjern `matches`-listen og score fra svaret og la den nye treff-flyten erstatte den (endepunktet beholdes som `not-implemented`/deprecated til brief v1 avgjør om score-only trengs). Alternativ: behold som er, bak eksisterende policy. Velg.
2. **Kelnersiden nå eller vente på brief v1?** Forslag: bare keypath `brief.remembered` + én linje i eksisterende konsoll (bilde `kelner-husker-v1.png`), så brief v1 arver den. Alternativ: bare keypath, intet bilde, til brief v1.
3. **Forklaringen: ordrett sitat eller omskriving?** Forslag: ordrett sitat i anførselstegn + dato, ingen modell. Omskriving ville bryte «gjestens egne ord».
4. **Omfang for «Godkjenn alltid».** Forslag: signaltype *menyendring* × dette huset, per grant (innsyn kan være «alltid», handling «denne gangen»). Bekreft.
5. **Signaltagger ved publisering.** Hvem setter taggene på en ny rett — huset manuelt i draft-patchen (forslag, D5: huset betaler kompileringen), eller avledes av rettens navn/ingredienser? Manuelt gir presise treff og ingen inferens.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-05 | Opprettet | Losen |
| 2 | 2026-09-05 | §6 besvart av Kjetil; tagger avledes + godkjennes av huset → ny bladnode, bilde og test; §6.1 deprecation av interests.match inn i antiformål-testen | Kjetil/Losen |
| 1 | 2026-09-05 | §0 audit (11 rader, alle retrieved/unavailable), §1 tre med 9 kandidatformål + 1 antiformål, §2 avgrensning, §3 forventningskontrakt (10 rader), §5 +10 tester, §6 fem spørsmål | Losen |
