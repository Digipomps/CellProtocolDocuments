# Formålsspesifikasjon — skeleton render paritet

Oppgavemappe: `PDD_skeleton-render-paritet_2026-09-07` · Opprettet 2026-09-07 · Iterasjon 0 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Gå gjennom alle lokale flater: alle elementer virker, dataene som vises er relevante, flaten oppfyller sitt formål, den rendrer effektivt, og den ser helt likt ut i HAVEN-appen som i web-rendereren.

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| «alle lokale flater» er en avgrenset, kjennbar mengde | **retrieved** — korpuset bygges av menykonfigurasjoner + navigasjonsdestinasjoner + verifiseringshjelperen, dedupliseres, og feiler om det er mindre enn appens meny | `BindingTests/CellConfigurationVerifierXCTest.swift:436–454` |
| Det finnes allerede en test på at elementer kan nås | **retrieved** — `testNoLocalSurfaceHidesItsOwnWaysIn` kjører `SkeletonReachabilityAudit.reachableActionKeypaths` per flate | `CellConfigurationVerifierXCTest.swift:436,466`; `CellProtocol/Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift:65` |
| Det finnes allerede en test på lastetid og beskrivelse | **retrieved** — `testEveryLocalSurfaceLoadsFastIsDescribedAndFindable` | `CellConfigurationVerifierXCTest.swift:305` |
| Det finnes en paritetsmatrise mellom web og native | **retrieved** — 24 caser, delt fixture | `CellScaffold/Tests/fixtures/SkeletonElementParityMatrix.v1.json` |
| …og at Binding faktisk måles mot den | **contradicted** — matrisen leses av `CellScaffold/Tests/AppTests/SkeletonElementParityMatrixTests.swift` og av to Playwright-spec-er. **Ingen fil i Binding refererer den.** Native-siden av hver case er `"binding": "source-inspected-explicit-switch"` — påstanden er etablert ved å lese Bindings kildekode fra CellScaffold, ikke ved å rendre den | grep over `Binding/**/*.swift`: null treff |
| «ser helt likt ut» kan avgjøres av en maskin | **unavailable** — det finnes ingen felles referanse i dag: web rendres i `Public/js/skeleton-runtime.js` (7073 linjer), native i `BindingSkeletonView`. Ingen delt viewport, ingen delt tokenisering, ingen bildesammenligning | — |
| «dataene som vises er relevante» er testbart i dag | **unavailable** — nærmeste er den statiske strukturauditen (`testConfigurationCatalogSkeletonsPassStaticStructureAudit`), som ser på form, ikke på om innholdet svarer på flatens formål | `CellConfigurationVerifierXCTest.swift:567` |
| «rendrer effektivt» er målt | **retrieved, men delvis** — lastetid er målt (74/77 flater < 100 ms per 2026-09-02); *render* er ikke målt i produksjonens kodevei, kun i verifikatorens NSHostingView-harness | `Binding/_audit-skeleton-render-20260828/reports/surface-audit-20260902T214435Z.json` |
| Codex kan kjøre dette via MCP | **contradicted** — `codex-local` avviser i dag med «The 'gpt-6-astra' model requires a newer version of Codex» | forsøk 2026-09-07 |
| Fjernflater (`cell://<vert>/…`) er del av oppgaven | **contradicted av avgrensningen** — de er blokkert av en manglende bro-rute og følges i eget spor | `Binding/Documentation/HAVEN_Bro_Forensikk_og_Status_2026-09-02.md` |

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://candidate.render-paritet.root` | Eieren ser samme flate uansett klient | `purpose://gui.quality.functional-accessible` | Hver lokale flate gir samme innhold, samme handlinger og samme visuelle resultat i HAVEN-appen som i Porthole-web | Alle blad under grønne | candidate |
| `purpose://gui.ways-in-are-reachable` | Veiene inn finnes | pakke `pkg.std.gui-surface` | Ingen flate har elementer som aldri kan sees; handlingene §3 navngir finnes i `reachableActionKeypaths` | `test.skeleton.no-unreachable-elements`, `test.skeleton.purpose-actions-reachable` | active (pakke) |
| `purpose://candidate.render-paritet.elements-behave` | Elementene virker, ikke bare vises | `…root` | Hvert interaktivt element i hver flate treffer en ekte keypath: knapper utfører, felt tar imot, lister får rader | `test.elements.execute` | candidate |
| `purpose://candidate.render-paritet.data-is-relevant` | Dataene svarer på flatens formål | `…root` | For hver flate: hver bundet verdi som vises kan spores til en kilde som er relevant for flatens erklærte formål, og ingen flate viser teknisk fyll eller tomme felt der eieren venter innhold | `test.data.relevance` | candidate |
| `purpose://candidate.render-paritet.purpose-is-served` | Flaten oppfyller formålet sitt | `…root` | Flatens `discovery.purpose` navngir handlinger eieren skal kunne utføre; alle finnes i `reachableActionKeypaths` og utfører noe | `test.purpose.actions-exist` | candidate |
| `purpose://gui.surface-loads-in-time` | Flaten er der raskt nok | pakke `pkg.std.gui-surface` | Terskel for denne oppgaven: **last ≤ 100 ms** og **første meningsfulle innhold ≤ 300 ms**, målt tre ganger i produksjonens kodevei | `test.gui.load-time` | active (pakke) |
| `purpose://candidate.render-paritet.same-in-both` | Samme resultat i app og web | `…root` | For hver av de 24 casene i paritetsmatrisen produserer Binding-rendereren samme observerbare resultat som web-rendereren, målt av samme fixture på begge sider | `test.parity.matrix-native` | candidate |
| `purpose://candidate.render-paritet.parity-corpus-is-shipped` | Paritet måles på det som sendes ut | `…same-in-both` | Paritetskorpuset er de faktiske flatene eieren kan åpne, ikke bare 24 syntetiske caser | `test.parity.real-corpus` | candidate |
| `purpose://candidate.render-paritet.recognisable` | Det er åpenbart samme flate | `…same-in-both` | En som kjenner flaten i web kjenner den igjen i appen uten å bli fortalt at det er samme flate: samme hierarki, samme gruppering, samme vekting av primærhandling | `test.parity.agreed-roles-cover-surfaces` | candidate |

## 2. Avgrensning og avhengigheter

Hva dette **ikke** er:
- Ikke fjernflater over `cell://<vert>/…`. 26 av flatene er røde fordi bro-ruten mangler; det følges i `HAVEN_Bro_Forensikk_og_Status_2026-09-02.md` og skal ikke blandes inn her.
- Ikke skeleton-parity-fixturene på staging/prod (`/skeleton-parity/*/api/configuration` → 500 på grunn av strict runtime-vault). Egen sak, egen deploy.
- Ikke ny funksjonalitet i skeleton-formatet. Finner Codex noe som krever et nytt elementtype eller felt, skal det stoppes og legges fram for Kjetil (`cellconfiguration-skeleton-authoring`).
- Ikke redesign. Referansen er hvordan flaten ser ut i web i dag, med mindre Kjetil godkjenner et nytt bilde i G1-GUI.

| Kapabilitet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| Korpus over eierens flater | `CellConfigurationVerifierXCTest.swift:436–454` | Dekker lokale flater; fjernflater faller ut når verten er nede | ja |
| `SkeletonReachabilityAudit` | `CellProtocol/Sources/CellBase/Skeleton/SkeletonReachabilityAudit.swift:65` | Sier hva som *kan* nås, ikke om handlingen gjør noe nyttig | ja |
| Paritetsmatrise, 24 caser | `CellScaffold/Tests/fixtures/SkeletonElementParityMatrix.v1.json` | Native-kolonnen er kildeinspeksjon, ikke rendering | ja |
| Web-renderer | `CellScaffold/Public/js/skeleton-runtime.js` | 7073 linjer; ingen delt tokenisering med native | ja |
| Playwright | `CellScaffold/playwright/skeleton-element-catalog.spec.js` | Kan ikke kjøres fra Codex' sandkasse (`MachPortRendezvousServer … Permission denied`) — kjøres av Kjetil eller i CI | ja |
| Byggegaten | `haven-swiftpm.sh` | Nekter cache uten markørfil `.haven-swiftpm-cache-v1` | ja |
| Codex via MCP | `codex-local` | **Nede 2026-09-07** (krever nyere Codex for `gpt-6-astra`) — bruk `codex exec` fra terminalen | ja |

## 3. Forventningskontrakt — «Det du kommer til å se»

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Referansebilde per flate og tilstand, fra web-rendereren | bilde | `images/<flate>-<tilstand>-web-v1.png` | web er referansen | nei |
| Samme flate rendret i HAVEN-appen, samme viewport | bilde | `images/<flate>-<tilstand>-app-v1.png` | mot web-bildet | nei |
| Avviksliste per flate, hvert avvik rettet eller godkjent med begrunnelse | fil | `ACCEPT.md#parity` | — | nei |
| Paritetsmatrisen kjørt **native**, ikke kildeinspisert | testutdata | `TESTRESULT.md#parity-native` | 24 caser | nei |
| Reachability + handlinger per flate | testutdata | `TESTRESULT.md#reachability` | — | nei |
| Lastetid og første innhold, tre målinger per flate | testutdata | `TESTRESULT.md#load-time` | ≤100 ms / ≤300 ms | nei |
| Relevansvurdering per flate: formål → viste data → dom | fil | `ACCEPT.md#data-relevance` | — | nei |

## 3b. Toleransen for «likt» — nedskrevet

Kjetil, 2026-09-07: *«samme elementer, rekkefølge, tekst, tilstand og handlinger,
med en nedskrevet toleranse for typografi og spacing — men det skal være lett
gjenkjennelig at det er den samme flaten.»*

Sammenligningen skjer på et skeleton normalisert med
`SkeletonStyleParity.normalizedForParity(...)`
(`CellProtocol/Sources/CellBase/Skeleton/SkeletonStyleParity.swift`), slik at
tokens ingen av rendrerne er enige om ikke telles som avvik.

### Nivå 1 — identisk, ingen toleranse

| Egenskap | Krav |
|---|---|
| Elementsekvens | Samme elementtyper i samme rekkefølge, fra normalisert skeleton. Ingen droppet, ingen ekstra. |
| Synlig tekst | Identisk etter trimming. Ingen JSON-hermetegn, ingen rå keypath, ingen UUID. |
| Tilstand | Tom, fylt og feil gir samme innhold begge steder. |
| Handlinger | `reachableActionKeypaths` er identiske mengder. |

Et avvik her er en feil, ikke en toleransesak.

### Nivå 2 — toleranse

| Egenskap | Toleranse | Hvorfor |
|---|---|---|
| Skriftfamilie | Plattformens systemfont er tillatt å avvike | SwiftUI og CSS har ulik base |
| Absolutt skriftstørrelse | Kan avvike | plattformbase er ulik |
| **Relativ typeskala** | Forholdet mellom nivåene (overskrift : brødtekst : sekundær) innenfor **±10 %** | dette er det som bærer hierarkiet |
| Avstand (padding, gap) | **±25 % eller ±4 pt**, det største, per avstand | stack-spacing og margin summerer ulikt |
| Linjebrytning | Fritt. Antall linjer er ikke et avvik; innholdet er | ulik tekstmotor |
| Farge | Samme rolle (bakgrunn / flate / aksent). Eksakt verdi kan avvike kun der rollen **ikke** er i `agreedRoles` | ellers er det udefinert kontrakt, ikke en bug |

### Nivå 3 — gjenkjennelighet

Kravet ditt over toleransene: samme visuelle hierarki (det som er overskrift ett
sted er overskrift det andre), samme gruppering i seksjoner og kort, samme
vekting av primærhandlingen.

**Dette er ikke en toleranse. Det er en kontrakt som ikke finnes ennå.**

`SkeletonStyleParity.agreedRoles` er **tom med vilje** — filens egen kommentar
sier at ingen rolle i dag hedres av begge rendrerne, og at å gjøre en rolle
normativ er en produktbeslutning, ikke en opprydding.

**Målt på nytt 2026-09-07** (første telling sa 19 roller og «null tolket av
web». Begge tallene var feil — den fanget bare literale `styleRole = "..."` og
bare `webOnlyRoles`. Rettet under; den gamle teksten er strøket fra revisjonen.)

| | Antall |
|---|---|
| Distinkte roller appens flater faktisk setter | **34** |
| Roller web-rendreren styler via `.style-role-<navn>` i CSS | **61** |
| **Av appens roller: stylet av web, ikke av SwiftUI** | **5** |
| Av appens roller: tolket av SwiftUI, ikke av web | 2 |
| Av appens roller: ingen rendrer tolker | **27** |
| Roller web styler som appen aldri setter | 56 |
| Av appens roller i `agreedRoles` | **0** |

De 34 kommer fra fire skrivemåter, ikke bare literalen: `styleRole = "x"`,
`role: String = "x"` som standardparameter, `role: "x"` ved kallstedet, og to
ternærer. Kilder: `Binding/Cells/*.swift`, `Binding/Binding/SkeletonPresentationOverlayView.swift`.

### Funn: `SkeletonStyleParity.webOnlyRoles` er ufullstendig

`skeleton-runtime.js:4027` legger på `style-role-<navn>` som CSS-klasse for
**hver eneste** rolle, betingelsesløst. Web styler derfor en rolle på to måter:

1. JS-spesialbehandling — `admin-page-heading`, `admin-section-heading`,
   `admin-form-field`. Disse tre er `webOnlyRoles`, og de har **ingen** CSS-regel.
2. CSS-klasseregel — 61 roller i `Public/css/porthole-webo.css` og
   `Public/css/conference-mvp.css`. Disse er `webOnlyRoles` **ikke** klar over.

Fem av appens roller havner i gruppe 2: `chat-active-tool-chip`,
`chat-active-tool-chips`, `chat-helper-tabs`, `chat-helper-tabs-compact`,
`chat-prompt-log`.

**Presist hva som er galt.** `classify` returnerer `nil` bare for roller i
`agreedRoles`; alt annet strykes fra JSON-en uansett hvilken `TokenKind` det
får. Stryking er altså *ikke* forskjellig for de fem — feilen er **merkelappen**.
De rapporteres som `.unclaimed`, hvis egen dokumentasjon sier «ingen rendrer
tolker den», når web faktisk styler dem og SwiftUI ikke gjør det. Funnstrømmen
fra `normalizedForParity` — det eneste stedet som forteller hva du *valgte å
ikke sammenligne* — sier dermed at forskjellen ikke finnes.

Konsekvensen er ikke feil normalisert JSON. Den er at enhver triage av funn
nedprioriterer fem ekte web/native-avvik som «ren metadata». Og at
`webOnlyRoles`, lest som en oversikt over hva web styler, er feil med 61.

Rettet 2026-09-07 utenfor porten på Kjetils ord — se `patch/`. Se §5,
`test.parity.style-parity-knows-web-css`.

### Rollene som bærer flatene

De 27 ingen rendrer tolker inneholder alt som gir de personlige flatene struktur,
etter faktisk bruk:

| Bruk | Rolle | Hva den bærer |
|---|---|---|
| **35** | `personal-list-row` | hver liste i appen |
| 7 | `personal-key-value-block` | nøkkel/verdi-oppsett |
| 5 | `personal-audit-row` | revisjonslinjer |
| 4 | `personal-hero` | toppen av flaten |
| 4 | `personal-card` | seksjonskort |
| 4 | `personal-chat-item`, `personal-consent-prompt`, `personal-draft-composer` | |
| 3 | `personal-section-header`, `personal-action-row`, `personal-match-card` | seksjonsinndeling |
| 2 | `tabstrip` | navigasjon i flaten |

Nivå 3 er derfor ikke oppnåelig ved å måle piksler. Den krever at et utvalg av
disse løftes inn i `agreedRoles` og implementeres i **begge** rendrerne. Hvilke,
og i hvilken rekkefølge, er en produktbeslutning for Kjetil — §6 spørsmål 1.

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
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance

## 5. Avledede tester (samlet)

| testRef | Formål | Hvordan | Evidens | Status |
|---|---|---|---|---|
| test.build | `purpose://quality.build-and-regression` | `xcodebuild -project Binding.xcodeproj -scheme HAVEN -destination 'platform=macOS,arch=arm64' CODE_SIGNING_ALLOWED=NO build` | TESTRESULT.md#build | venter |
| test.regression | `purpose://quality.build-and-regression` | `Scripts/test_binding.sh` — antall tester før/etter skal ikke synke | TESTRESULT.md#regression | venter |
| test.docs-updated | `purpose://quality.docs-in-same-change` | Diff mot dokumenter som beskriver renderer-atferd; «Last verified against code»-dato | ACCEPT.md#docs | venter |
| test.status-current | `purpose://quality.work-is-visible` | STATUS.md mot mappen | ACCEPT.md#status | venter |
| test.gui.reference-image-exists | `purpose://gui.expectation-agreed-before-build` | `purpose_dev.py validate` mot §3 | images/ | venter |
| test.gui.parity | `purpose://gui.parity-with-approved-image` | Web-screenshot og app-screenshot i samme viewport, side om side per flate | ACCEPT.md#parity | venter |
| test.gui.load-time | `purpose://gui.surface-loads-in-time` | Tre målinger per flate i produksjonens kodevei. Terskel 100 ms last / 300 ms første innhold | TESTRESULT.md#load-time | venter |
| test.skeleton.no-unreachable-elements | `purpose://gui.ways-in-are-reachable` | `-only-testing:BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn` | TESTRESULT.md#reachability | venter |
| test.skeleton.purpose-actions-reachable | `purpose://gui.ways-in-are-reachable` | §3-radene mot `SkeletonReachabilityAudit.reachableActionKeypaths` | ACCEPT.md#ways-in | venter |
| **test.parity.matrix-native** | `…same-in-both` | Ny XCTest i Binding som leser `SkeletonElementParityMatrix.v1.json` og rendrer hver case gjennom `BindingSkeletonView`. Erstatter `"binding": "source-inspected-explicit-switch"` med et faktisk rendret resultat | TESTRESULT.md#parity-native | venter |
| **test.parity.agreed-roles-cover-surfaces** | `…recognisable` | Tell distinkte `styleRole` i eierens flater; hver som bærer hierarki skal være i `SkeletonStyleParity.agreedRoles` og ha en implementasjon i både `skeleton-runtime.js` og `SkeletonView.swift`. Feiler med listen over roller som mangler | TESTRESULT.md#agreed-roles | venter |
| **test.parity.style-parity-knows-web-css** | `…same-in-both` | `SkeletonStyleParity.webOnlyRoles` skal inneholde hver rolle som har en `.style-role-<navn>`-regel i `CellScaffold/Public/css/*.css`, ikke bare de tre JS-spesialbehandlede. Testen skanner CSS-en og feiler med differansen. I dag mangler 61 roller, hvorav 5 er i bruk i appen | TESTRESULT.md#style-parity-source | venter |
| **test.parity.real-corpus** | `…parity-corpus-is-shipped` | Utvid matrisen fra 24 syntetiske caser til å dekke elementtypene som faktisk forekommer i eierens flater; feil hvis en type forekommer i korpuset uten en case | TESTRESULT.md#parity-corpus | venter |
| **test.elements.execute** | `…elements-behave` | Per flate: kjør hver statisk knapp gjennom rendererens egen eksekveringsvei og krev et svar som ikke er `notFound`/`denied`; felt tar imot input | TESTRESULT.md#elements | venter |
| **test.data.relevance** | `…data-is-relevant` | Per flate: list bundne keypaths og verdien hver ga; en menneskelig dom per flate i ACCEPT.md. Automatiserbar del: ingen synlig verdi er tom, teknisk (`cell:///…`, rå UUID) eller et JSON-sitat | ACCEPT.md#data-relevance | venter |
| **test.purpose.actions-exist** | `…purpose-is-served` | `discovery.purpose` per flate → navngitte handlinger → finnes i `reachableActionKeypaths` og utfører noe | ACCEPT.md#purpose | venter |

## 6. Åpne spørsmål til Kjetil

**Besvart 2026-09-07:**

- **Hvor strengt er «likt»?** → Samme elementer, rekkefølge, tekst, tilstand og
  handlinger; nedskrevet toleranse for typografi og spacing; og det skal være
  lett gjenkjennelig at det er samme flate. Skrevet ut i §3b.
- **Er web referansen?** → **Ja.** Web slik den er i dag er fasit.
  Referansebildene i §3 tas som web-screenshots, og appen tilpasses dem.
- **Hvilke `styleRole` blir normative?** → **De seks foreslåtte.** Puljen som
  skal inn i `agreedRoles` og implementeres i *begge* rendrerne:

  | Rolle | Bruk | Bærer |
  |---|---|---|
  | `personal-list-row` | 35 | hver liste i appen |
  | `personal-key-value-block` | 7 | nøkkel/verdi |
  | `personal-hero` | 4 | toppen av flaten |
  | `personal-card` | 4 | seksjonskortet |
  | `personal-section-header` | 3 | seksjonsinndelingen |
  | `tabstrip` | 2 | navigasjonen i flaten |

  En rolle føres inn i `agreedRoles` **og** implementeres i både
  `skeleton-runtime.js` og `SkeletonView.swift` i samme endring. Å legge den inn
  uten implementasjon gjør det motsatte av hensikten: da slutter
  `normalizedForParity` å stryke rollen, og paritetsmålingen begynner å
  sammenligne noe bare den ene rendreren tolker. Dette er P3-arbeid bak G2.
- **Skal `SkeletonStyleParity` rettes nå?** → **Ja, utenfor porten.** Gjort
  2026-09-07, se `patch/`. Bygg og test gjenstår — de krever macOS.

**Fortsatt åpent:**

1. **Terskelen 100 ms last / 300 ms første innhold** — riktig? 74 av 77 flater
   klarer 100 ms i dag; render er ikke målt i produksjonens vei.
2. **Relevansdommen per flate** — skal Codex foreslå en dom du kvitterer på,
   eller vil du dømme selv? Det er den eneste av de fem kriteriene en maskin
   ikke kan avgjøre alene.
3. **Rekkefølgen på de seks rollene.** Alle seks i én endring, eller
   `personal-list-row` alene først som mønster de fem andre kopierer? Den
   dekker 35 av bruken, så den beviser kontrakten billigst.

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-09-07 | Opprettet | Losen |
| 1 | 2026-09-07 | §0–§3, §5, §6 fylt ut fra kildelesing; hovedfunn: paritetsmatrisen leses ikke av Binding | Losen |
| 2 | 2026-09-07 | Kjetil definerte «likt». §3b skrevet: tre nivåer med tall. Funn: 19 styleRole i bruk, 0 i agreedRoles — nivå 3 krever produktbeslutning, ikke måling | Losen |
| 3 | 2026-09-07 | Telte om. Rad 2 var feil: **34** roller i bruk, ikke 19 (fanget bare literaler, ikke standardparametre, kallsteds-overstyringer og ternærer). Og **ikke** 0 tolket av web: `skeleton-runtime.js:4027` legger på `style-role-<navn>` betingelsesløst, og 61 roller har CSS-regel — 5 av dem i bruk i appen. `SkeletonStyleParity.webOnlyRoles` (3 roller) kjenner ingen av dem, så `normalizedForParity` stryker et ekte avvik som støy. Ny test `test.parity.style-parity-knows-web-css`. §6 spørsmål 1 omskrevet med riktige tall | Losen |
| 4 | 2026-09-07 | Kjetil svarte: web er fasit; de seks foreslåtte rollene blir normative; `SkeletonStyleParity` rettes utenfor porten. Presiserte §3b: `classify` stryker alt utenfor `agreedRoles` uansett `TokenKind`, så feilen er **merkelappen** (`.unclaimed` i stedet for `.webOnly`), ikke strykingen. Min forrige formulering overdrev. Fiksen ligger i `patch/` med ett-kommandos apply-skript | Losen |
