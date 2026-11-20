# Formålsspesifikasjon — native dokumenteditor i Binding

Oppgavemappe: `PDD_native-dokumenteditor_2026-11-20` · Opprettet 2026-11-20 · Iterasjon 1 (ikke godkjent)
Tråd: «Bygg native dokumenteditor i Binding», startet fra «La studenter dele dokumenter med hverandre» (G1 der 20.11, spm. 4: egen tråd).

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

Kjetil, 20.11.2026 (i tråden «La studenter dele dokumenter»), svar på spm. 4 «Skal native editor i Binding (CellApple) være en del av denne oppgaven, eller en egen tråd …? Jeg anbefaler egen tråd»:

> G1 og G1-GUI Godkjent.

Oppdraget fra koordinatoren: native støtte i Binding (CellApple) for visualiseringene `richDocument`, `documentHelp` og `documentChat`, som i dag bare finnes på web, slik at deling av dokumenter, skrivehjelp (pakke D) og argumentanalyse (pakke C) virker for studenter som skriver i Binding. Swift er førsteklasses.

| Påstand i intensjonen / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Binding viser «Visualization kind '…' støttes ikke ennå» for dokumentet | **retrieved** | `CellProtocol/Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/Suggestion/SkeletonView.swift:2648` (main 669850b). Linjen har flyttet seg fra :2593 |
| Tre visualiseringer mangler: `richDocument`, `documentHelp`, `documentChat` | **delvis contradicted** | På CellScaffold main 272580b bruker «Dokument»-oppsettet bare `richDocument` (`RichDocumentCell.swift:481`). Skrivehjelp og chat er nå vanlige skeleton-elementer (`RichDocumentSkeleton.swift`, PR #466), som Binding allerede tegner. `documentHelp`/`documentChat` finnes bare i lagrede oppsett fra før #466 som migreringen ikke tok, fordi de var endret (`RichDocumentBuiltInConfigurationUpgrade.swift:16–37`) |
| Webeditoren er Quill, cellen eier tilstand og autoritet | **retrieved** | `CellScaffold/Public/js/haven-rich-document.js` (308 linjer); `skeleton-runtime.js:4065–4103` monterer den og sender til `actionKeypath` |
| Kontrakten er språknøytral og kan snakkes fra Swift | **retrieved** | Les `document.current` → `haven.document.v1` (ops, revision, sequence, comments, presence, messages, help, events). Skriv `document.change` med `haven.document.change.v1` (`operationId`, `clientId`, `baseRevision`, `kind` ∈ delta/presence/comment.add/comment.resolve/help.ask/chat.post) → `{status: accepted\|duplicate\|conflict\|invalid\|capacity\|operationCollision\|persistencePending, current}`. `RichDocumentModel.swift:33–140`, `RichDocumentCell.swift:88–155` |
| Posisjoner er UTF-16 og innebygde objekter teller 1 | **retrieved** | `RichDocumentModel.swift:5,17,228` (U+FFFC for bilde/diagram). Samme enhet som `NSString`/`NSTextStorage`, og `NSTextAttachment` bruker også U+FFFC |
| Formatene cellen godtar | **retrieved** | Tegn: bold, italic, underline, strike, link (http/https/mailto). Linje: header 1–3, list ordered/bullet, blockquote. Innebygd: PNG/JPEG data-URI ≤ 3 MB, visualisering chart/network/table (`RichDocumentModel.swift:280–312`) |
| CellApple kan sende en set og lese svaret | **retrieved** | `Meddle.set(keypath:value:requester:) -> ValueType?` (`CellBase/Protocols/CellProtocol.swift:52`). Dagens hjelper `setValueType` kaster svaret og gir bare `Bool` (`SkeletonView.swift:498–513`), så editoren trenger en egen vei som beholder `{status, current}` |
| Binding får andres endringer uten å laste på nytt | **ikke målt** | Cellen sender Flow `document.<kind>` med topic `document.change` (`RichDocumentCell.swift:174`). Visualiseringer i CellApple oppdateres bare ved egen endring (`localMutationVersion`, `SkeletonView.swift:2667–2676`); bare radar poller. Om Flow fra dokumentcellen når Binding over bridge er ikke målt |
| CellApple har en rik tekstredigerer vi kan bygge på | **retrieved, men smal** | `RichMarkdownTextEditor` (NSViewRepresentable, bare macOS, Markdown-tekst) `SkeletonView.swift:4419`. Ikke iOS, ikke Quill-delta. Ny redigerer trengs |
| Plattformgulv | **retrieved** | CellProtocol `Package.swift:11–12`: macOS 13, iOS 16. SwiftUI `TextEditor` med `AttributedString` krever nyere OS, så redigereren må bygges på `UITextView`/`NSTextView` |
| Swift kan bygges i skycontaineren | **delvis** | Ren Swift (CellBase) bygges og testes i Docker `swift:6.1-noble` (minne `haven-cloud-swift-docker`). CellApple/SwiftUI og Binding krever Kjetils Mac (Remote Control) |

## 1. Formålstre

Rot: en student kan skrive i et dokument i Binding (Mac og iPhone), og det de skriver er det samme dokumentet som andre ser på web og i Binding, med samme formatering og uten tapte tegn.

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| purpose://candidate.native-dokumenteditor.root | Studenter skriver i dokumenter i Binding | purpose://digital-work | På staging: A skriver i Binding (Mac), B i Binding (iPhone), C på web, i samme dokument. Hver ser de andres tekst innen 3 s. Etter 2 min samtidig skriving er teksten lik hos alle tre og lik `document.current` | test.native.e2e-tre-klienter | candidate |
| purpose://candidate.native-dokumenteditor.delta-parity | Samme delta-regler i Swift som i Quill | root | En ren Swift-modul (compose, transform, transformPosition, UTF-16, U+FFFC) gir samme resultat som `quill-delta` for et felles fixture-korpus. Ligger i CellBase så den testes på Linux og kan brukes av CellScaffold senere | test.native.delta-fixtures-swift, test.native.delta-fixtures-quill | candidate |
| purpose://candidate.native-dokumenteditor.write | Skrive og formatere | root | Tekst, fet, kursiv, understreket, gjennomstreket, overskrift 1–3, punkt- og nummerliste, sitat og lenke kan skrives i Binding og kommer ut som de samme Quill-attributtene cellen godtar. Det cellen avviser (f.eks. andre lenkeskjema) kan ikke lages i UI | test.native.format-rundtur, test.native.ui-format-iphone-mac | candidate |
| purpose://candidate.native-dokumenteditor.sync | Ingen tapte tegn | root | Lokale endringer går i kø, én forespørsel i lufta med samme `operationId` ved nytt forsøk. Ved `conflict` rebases køen på det nye `current`. Ved `duplicate` regnes den som levert. Andres endringer flettes inn uten at markøren hopper | test.native.konflikt-rebase, test.native.retry-samme-operasjon | candidate |
| purpose://candidate.native-dokumenteditor.live | Andres endringer kommer av seg selv | root | Mens dokumentet er åpent kommer andres endringer innen 3 s, via Flow `document.change` når den når fram, ellers ved henting hvert 2. sekund mens flaten er synlig | test.native.live-oppdatering | candidate |
| purpose://candidate.native-dokumenteditor.draft-safe | Utkastet overlever frakobling og omstart | root | Ikke-bekreftede endringer lagres per dokument-id på enheten. Etter frakobling, eller at appen avsluttes, sendes de når dokumentet åpnes igjen. Status sier «Lagrer …», «Alle endringer er lagret», eller hva som er galt | test.native.utkast-overlever-omstart | candidate |
| purpose://candidate.native-dokumenteditor.comments-presence | Kommentarer og andres markør | root | Marker tekst → «Kommenter». Kommentarer vises i et sidepanel (Mac) eller ark (iPhone) med «Vis i teksten» og «Løs». Andre skriveres markør vises med navn. Samme kommandoer som web (`comment.add`, `comment.resolve`, `presence`) | test.native.kommentar-rundtur | candidate |
| purpose://candidate.native-dokumenteditor.embeds | Bilder og diagrammer | root | Bilder og diagrammer i dokumentet vises i Binding (diagrammer med CellApples eksisterende `VisualizationChartView`). Et bilde kan settes inn fra Bilder/Filer (PNG/JPEG, ≤ 2 MB som web) | test.native.embed-rundtur | candidate |
| purpose://candidate.native-dokumenteditor.export | Eksport | root | «Del / eksporter» gir Markdown og PDF på Mac og iPhone. Word (.docx) se §6 spm. 2 | test.native.eksport | candidate |
| purpose://candidate.native-dokumenteditor.legacy-kinds | Gamle oppsett virker også | root | Et lagret oppsett med `documentHelp` eller `documentChat` viser chat og spørsmål/svar natively (liste + tekstfelt + send), i stedet for «støttes ikke ennå» | test.native.legacy-kinds | candidate |
| purpose://candidate.native-dokumenteditor.access-from-agreement | Tilgang bare fra cellen | root | Editoren gjør ingen egen tilgangssjekk. `denied` fra cellen gir skrivebeskyttet visning med forklaring. Skrive/lese-rollen fra delings-PDD-en (Agreement-vilkår) virker uten endring her | test.native.lesetilgang | candidate |
| purpose://quality.build-and-regression | Alt bygger, eksisterende tester passerer | pkg.std.everything-works | CellBase (Linux + macOS), CellApple macOS og iOS, Binding bygger. Eksisterende tester like grønne som før | test.build, test.regression | fra pakke |
| purpose://gui.expectation-agreed-before-build | Bildene er godkjent før koding | pkg.std.gui-surface | Bildene i `images/` er godkjent av Kjetil | test.gui.reference-image-exists | fra pakke |
| purpose://gui.parity-with-approved-image | Det som bygges ser ut som bildet | pkg.std.gui-surface | Skjermbilde fra Binding (Mac og iPhone-simulator) ved siden av referansen, samme tilstand | test.gui.parity | fra pakke |

Regler: velg fra Book 23 og pakkene først; nye noder får `purpose://candidate.…` og navngis her, aldri av en modell.

## 2. Avgrensning og avhengigheter

Hva dette IKKE er:
- Ikke en ny dokumentmodell. Cellen er fortsatt eneste revisjonsautoritet, og Quill-delta er fortsatt formatet. Binding blir en klient til, som web.
- Ikke deling/invitasjon. Det er tråden «La studenter dele dokumenter med hverandre». Denne editoren virker på det dokumentet flaten peker på, enten `cell:///RichDocument` eller et delt `cell:///<uuid>`.
- Ikke skrivehjelp- eller chatpanelet. De er alt vanlige skeleton-elementer og virker i Binding. Men «Bruk forslaget» lager en delta på serveren, og editoren må ta den inn som en hvilken som helst annen endring (dekket av `sync`/`live`).
- Ikke argumentkart (pakke C har egen `argumentmap`-visualisering i CellApple).
- Ikke tvOS. CellApple bygges for tvOS, der viser editoren skrivebeskyttet tekst.
- Ikke offline samtidig redigering mellom to enheter uten server.

Avhengigheter. Hver skal være målt før G1 der det går, ellers står det «ikke målt».

| Kapabilitet | Kilde (fil) | Avgrensning | Målt? | Må virke før test? |
|---|---|---|---|---|
| `document.current` og `document.change` på RichDocumentCell | `CellScaffold/Sources/App/Cells/RichDocument/RichDocumentCell.swift:57–155` | Krever `r---` på current og `rw--` på change | Kontrakten lest i kode. Ikke kjørt fra Binding | ja |
| Binding når dokumentcellen via bridge og kan gjøre `set` med svar | `SkeletonView.swift:483–513` | Dagens hjelper beholder ikke svaret | **Ikke målt.** WP0 måler `get current` og `set change` fra Binding mot staging | ja |
| Flow `document.change` når Binding | `RichDocumentCell.swift:174`, `PortholeViewModel.swift:132` | Ukjent om Porthole-flow i Binding får celle-Flow fra en referanse | **Ikke målt.** WP0 måler. Henting hvert 2. s er reserven | nei (reserven holder) |
| Delt dokument som `cell:///<uuid>` | delings-PDD WP1 | Kommer fra den andre tråden | Ikke målt | nei (rot-testen kan kjøres på `cell:///RichDocument` med Agreement fra enhetstesten) |
| `quill-delta` i node for fixture-paritet | `CellScaffold/node_modules` / `Public/vendor/quill` | Samme versjon som web bruker | Ikke målt | ja for test.native.delta-fixtures-quill |
| Mac med Xcode via Remote Control | minne `haven-long-runs-placement` | CellApple/Binding-bygg og skjermbilder | Virket 18.11 | ja |

## 3. Forventningskontrakt — «Det du kommer til å se»

| # | Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|---|
| 1 | Editoren på iPhone: tomt dokument, fylt dokument med formatering, kommentar og annen skrivers markør, og frakoblet med utkast som venter | bilde (mockup) | `images/` | `editor-tom-iphone-v1.png`, `editor-fylt-iphone-v1.png`, `editor-frakoblet-iphone-v1.png`, `kommentarer-iphone-v1.png` | nei |
| 2 | Samme på Mac | bilde (mockup) | `images/` | `editor-tom-mac-v1.png`, `editor-fylt-mac-v1.png`, `editor-frakoblet-mac-v1.png` | nei |
| 3 | Skjermbilder fra ekte Binding (Mac + iPhone-simulator) i de samme tilstandene | skjermbilde | Binding mot staging | ACCEPT.md#parity | nei |
| 4 | Opptak: Mac, iPhone og web skriver samtidig i samme dokument, teksten blir lik | video + TESTRESULT | staging | test.native.e2e-tre-klienter | nei |
| 5 | Grønne tester: delta-fixtures i Swift (CellBase, Linux og macOS) og i node mot `quill-delta`, CellApple-tester for kø/rebase/utkast | testutdata | CI på PR-ene + Mac | TESTRESULT.md#build, #regression, #delta | nei |
| 6 | En CellProtocol-PR (CellBase-delta + CellApple-editor) og en Binding-pinløft, begge bygget på Mac før noe går i kø | PR + byggelogg | GitHub | TESTRESULT.md#build | nei |

Bildene er HTML-mockups i iPhone- og Mac-størrelse, ikke Binding-skjermbilder, fordi SwiftUI ikke kan rendres i skycontaineren. Det som ikke kan vises i mockupen, men gjelder: systemets tastatur og tekstmarkering, systemets delingsark, og systemfonter som avviker litt fra mockupens. `images/README.md` sier det samme.

## 4. Tilknyttede formålspakker og lærdommer (auto fra purpose_dev.py lookup)

Lærdommene som styrer denne oppgaven mest, og hvor de er tatt inn:
- `lesson.parity-was-correctness-not-decoration`: aksept sammenligner oppførsel (tekst lik hos alle klienter), ikke bare bilde → rot-testen og `test.native.format-rundtur`.
- `lesson.tested-a-different-path-than-production`: delta-testene kjøres både mot Swift-modulen og mot den `quill-delta` web faktisk bruker → to fixture-tester.
- `lesson.valuetype-equality-false-for-objects`: ops med innebygde objekter sammenlignes som sortert JSON, som `RichDocumentOp ==` alt gjør.
- `lesson.syntax-check-reported-as-delivered` og minnet om #466: ingen PR tilbys før Mac-bygg av CellApple (macOS + iOS) og Binding er grønt.
- `lesson.sketch-assumed-a-renderer-it-did-not-have`: mockupene er HTML; §3 lister hva de ikke viser.
- `lesson.pin-must-be-on-their-main`: Binding-pinen løftes først når CellProtocol-PR-en er på main.


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
- **lesson.host-mutation-without-reading-the-coordination-file** (2026-10-02, major): 30.09 satte en Claude-tråd ut en gren-commit på staging og byttet invitasjonene, med Kjetils ja, men uten claim. En Codex-tråd hadde claim på samme container (HD-0141), staging var reservert for 2026.9.4, og deploykøen trodde i to døgn at staging kjørte forrige utgivelse.
    - forebygging: Før enhver vertsmutasjon: les `_losen-queue/KOORDINERING.md`, kjør `hd coord status`, ta egen claim på en HD-oppgave, og før utsettingen inn i køen etterpå. Test: jobbloggen for utsettingen viser `hd coord status` uten annen claim på samme tjeneste, og egen claim, før første kommando mot verten. Eierens ja til å sette ut erstatter ikke sjekken.
- **lesson.remembered-install-state-is-not-measured** (2026-10-02, minor): En plan sa at agenten på Macen var bygget fra en bestemt gren, og bygde grenvalg og et åpent spørsmål til eieren på det. Agenten var installert på nytt fra `main` av en annen tråd seks dager tidligere.
    - forebygging: Hva som er installert, måles før en plan bygger på det: dato og navn på binærene og sikkerhetskopiene i `bin/`, `launchctl print`, og om commiten er på `origin/main`. Test: påstandstabellen merker installasjonstilstand som hentet med måletidspunkt, aldri som husket.
- **lesson.own-committed-tests-changed-without-asking** (2026-10-03, major): Ti tester tråden selv hadde committet tidligere samme dag, ble endret uten å spørre: tretten endringer, og sju av dem snudde eller fjernet noe en test krevde godtatt.
    - forebygging: En committet test er eksisterende, uansett hvem som skrev den og når. Før hver commit leses testendringene rett fra git; en endring i en committet test er et spørsmål til eieren. Test: skriptet som lister testendringer fra git, viser ingen endring i en committet test uten en godkjenning ført i STATUS.md.
- **lesson.accept-written-from-memory-had-27-errors** (2026-10-03, major): Første utkast til ACCEPT.md og TESTRESULT.md hadde 27 feil da en uavhengig tråd holdt det mot bevisfilene; ett av dem var påstanden om at hver frosset utgave ble angrepet etter at den var satt ut.
    - forebygging: Tall, klokkeslett, commit-numre og sitater i ACCEPT.md og TESTRESULT.md fylles inn fra bevisfilene av kode, og en uavhengig tråd holder hver påstand mot bevisene før eieren får dokumentene. Test: rapporten fra kontrollen ligger blant bevisene, med en dom per påstand.
- **lesson.red-first-claimed-for-tests-that-were-not** (2026-10-04, minor): TESTRESULT.md sa at hver ny eller endret test var kjørt rød først. Tolv endringer i tester som alt fantes, og ti av de 24 nye i første runde, kom inn sammen med koden og var aldri kjørt røde.
    - forebygging: En påstand om alle tester føres per test: «rød først» listes med hvilke tester som fantes i den røde kjøringen, og hvilke som kom til etterpå. Test: antall tester i den røde og i den grønne kjøringen står i TESTRESULT.md, og differansen er forklart.
- **lesson.estimate-assumed-one-attack-round** (2026-10-04, minor): Planen sa «rundt tre og en halv time etter G1». Den siste utgaven var målt på nett 34 timer og 50 minutter etter.
    - forebygging: Et anslag for arbeid som skal angripes av en uavhengig tråd, oppgis per runde, og sier at antall runder er ukjent til første angrep er målt. Test: planen har tid per runde, ikke en sluttid.
- **lesson.full-path-rule-broken-in-short-references** (2026-10-05, major): Kjetil måtte for tredje gang si at filer skal stå med hele stien («Du må legge med hele banen til filer som dette: ACCEPT.md»): meldingene og spørsmålene ved G3 hadde bare filnavnet.
    - forebygging: Hver melding til eieren kontrolleres maskinelt før den sendes: et ord som ender på en filendelse og ikke begynner med en rot, stopper sendingen. Det gjelder hver gang en fil nevnes, også i spørsmål. Test: skriptet som kontrollerer meldinger, gir null funn på hver melding som ber om en port.
- **lesson.file-copied-to-the-mac-was-the-previous-version** (2026-10-05, major): En commit gikk ut med testen, men uten endringen den prøvde: filkopien fra skyøkten til Macen meldte «written», og fila på Macen var forrige utgave. To skript mistet dessuten kjørbar-biten på veien.
    - forebygging: Hver utgave som skal til Macen, legges under et nytt filnavn i utdatamappen. Sjekksummen på Macen sammenlignes med den i skyen i et eget steg, og neste steg (commit eller køjobb) startes ikke i samme kommando. Test: commit-jobben viser «git diff --cached --stat --summary» før commit, og lista over filer og moduser sammenlignes med det som skulle med.
- **lesson.pr-opened-without-reading-the-base-branch-ci** (2026-10-05, minor): PR #30 ble opprettet uten at CI-tilstanden på main var lest: løpet sto til tidsgrensen på 25 minutter av en grunn som hadde stått på main i seks dager, og den første lesningen av loggen, at det stoppet før PR-ens tester hadde startet, ble felt av den uavhengige kontrollen.
    - forebygging: Før en PR opprettes, listes løpene for basisgrenen; har hodet ikke noe grønt løp med samme testskript, rettes det først, eller rettelsen tas med. Før en årsak skrives ned for et rødt løp, leses avsnittet om CI i skillen, og siste linje i en logg kalles ikke stedet det stoppet. Test: skriptet som oppretter en PR, viser siste løp på basisgrenen og stopper når det er rødt.
- **lesson.status-message-sent-before-the-documents-were-checked** (2026-10-06, minor): Dokumentene og meldingen til eieren 06.10 om kvelden skrev slutninger som målinger («haven-deploy ville blitt kjørt med umask 077», «skallet ventet fem sekunder: målt»), gjenga kontrollenes merknader som «en feil» og «alle rettet», utelot ett av fire svar der en vakt ble beskrevet, og ga et klokkeslett for når en kjøring ville være ferdig, uten grunnlag. Meldingen var sendt et kvarter før kontrollen av dokumentene.
    - forebygging: Dokumenter, LES-MEG ved siden av et skript og meldingen til eieren kontrolleres mot kildene av en som ikke har skrevet dem, før meldingen sendes. Ved hver påstand står det om den er målt, lest eller sluttet, og et tidsanslag gis som et spenn med grunnlaget. Test: kontrollrapporten er eldre enn meldingen, og rettelser gjort etter kontrollen er merket som ukontrollert.
- **lesson.commit-file-built-on-a-stale-copy-and-the-check-got-the-same-copy** (2026-10-06, major): README.md i commiten `c5058f49` fikk 172 endrede linjer (104 ut, 68 inn) der rundt 50 nye var ventet: tekst fra tre tidligere commiter falt ut.
    - forebygging: Hver fil i en commit-pakke bygges på git-objektet i foreldercommiten, og skriptet som committer, krever ventet antall linjer inn og ut per fil og stopper ellers. Kontrolltråden får commiten og finner grunnlaget selv. Test: skriptet stopper når forskjellen mot forelderen ikke er den ventede.
- **lesson.brake-file-written-after-the-chain-had-passed-the-brake** (2026-10-06, minor): Bremsefilen ble lagt 13 sekunder etter at kjedeskriptet hadde passert bremsesjekken foran pushen, så en commit med en kjent feil ble pushet.
    - forebygging: Et tall et menneske må lese før neste steg som ikke kan angres, deler kjeden i to jobber, eller skriptet krever tallet selv. Test: kjeden stopper foran pushen når commitens linjetall avviker fra det ventede.
- **lesson.check-ran-before-the-last-numbers-and-did-not-read-the-message** (2026-10-06, minor): Kontrollen av akseptdokumentet ble gjort før de 27 siste kallene var målt, og meldingen til eieren var ikke med. En ny kontroll rett før sending fant åtte ting, blant annet at meldingen la en svakhet til angrepet alene der råsvarene fra nett viste det samme.
    - forebygging: Den siste uavhengige kontrollen kommer etter at siste tall er ført inn, regner tallene på nytt fra råfilene og leser meldingen eieren får. Test: kontrollrapporten er yngre enn siste bevisfil og eldre enn meldingen.
- **lesson.approved-image-had-no-way-to-be-photographed-on-the-live-page** (2026-10-06, minor): Telefonbildet som ble godkjent ved G1-GUI, kunne ikke få et skjermbilde fra nett ved siden av seg ved G3: nettleserverktøyet holder vinduet på 1280 punkter, og siden nekter å bli vist i en ramme.
    - forebygging: Ved G1-GUI står det for hvert bilde hvordan motstykket på nett skal tas ved G3, og veien er prøvd én gang mot siden slik den står. Kan et bilde ikke tas, sies det ved G1-GUI. Test: hvert godkjent bilde har en navngitt opptaksvei som har gitt en fil.
- **lesson.early-return-rule-changed-what-happens-when-the-lookup-is-down** (2026-10-06, minor): Et spørsmål med et ord fra ordlisten får henvisningen (HTTP 200) også når oppslaget ikke kan nås, der andre spørsmål får 503 eller 403. Det sto verken i spesifikasjonen eller i en test.
    - forebygging: For hver regel som svarer før en avhengighet spørres, sier spesifikasjonen hva som skjer når avhengigheten er nede, og en test holder det fast. Test: en test der avhengigheten er tatt bort, med ventet svar for begge grener.
- **lesson.way-back-was-called-a-way-back-after-dry-runs-only** (2026-10-06, minor): Veien tilbake fra utsettingen er tørrkjørt to ganger, men selve byttet tilbake er aldri kjørt, der spesifikasjonen krever en vei som virker også når siden er nede.
    - forebygging: En vei tilbake er vist når byttet er kjørt, for eksempel mot en egen container med samme image. Ellers står den som «ikke vist» i planen eieren godkjenner. Test: bevis for et gjennomført bytte, eller linjen «ikke vist» i planen.
- **lesson.order-of-steps-changed-to-keep-a-promised-time** (2026-10-06, minor): Utgaven ble satt ut før rettelsen av README.md var committet, mot planen, fordi kontrollen av rettelsen tok 28 minutter der 15 var ventet.
    - forebygging: Planen sier hvilke steg som kan bytte plass når noe tar lengre tid, og kontroller får en hard tidsgrense. Test: hvert planbytte har en linje i STATUS.md med hva som tapes.
- **lesson.correction-to-a-list-removed-words-it-already-caught** (2026-10-06, minor): To rettelser i ordlisten ga nye hull: et unntak som ble sammenlignet etter at ø var brettet til o, tok bort «nøtte», og en innsnevring tok bort «tolererer».
    - forebygging: Hver utgave av en liste kjøres mot alle tidligere eksempler, både ord som skal treffe og ord som ikke skal, og eksemplene ligger som fikstur. Test: en fikstur med ett eksempelord per oppføring og en liste med ord som ikke skal treffe.
- **lesson.rewritten-draft-got-new-errors-where-it-was-rewritten** (2026-10-06, minor): Seks utkast til spesifikasjonen ble lest i fem kontrollrunder som fant 110 ting til sammen. Hver runde fant feil i det som var skrevet om etter den forrige.
    - forebygging: Etter en omskriving kontrolleres det omskrevne på nytt, og eieren får vite når siste utgave ikke er kontrollert. Tall fylles inn av kode. Test: dokumentet sier hvilken utgave kontrollen leste.
- **lesson.known-pitfall-repeated-in-a-small-follow-up-without-lookup** (2026-10-06, minor): Testen for avvik 4 sammenlignet to like svarkonvolutter med `XCTAssertEqual` og var rød mot riktig kode. Den grønne kjøringen fanget det før commit.
    - forebygging: `lookup` kjøres for hvert steg som skriver kode eller tester, også små oppfølginger, og oppgaven til kontrolltråden ber den holde testen mot lærdommene for taggene. Test: commit-trinnet stopper uten grønt bevis for nettopp filene som committes.
- **lesson.full-path-rule-passed-the-checker-in-descriptions-and-file-cards** (2026-10-06, minor): Meldingen som ba om G3, gikk gjennom kontrollskriptet for hele banen, men fem filer ble sendt som kort uten bane i sendingen, og dokumenter ble nevnt med en beskrivelse («akseptdokumentet») før banen sto.
    - forebygging: Hver fil som leveres i samtalen, står med hele banen i meldingen som følger med, og en beskrivelse av en fil får banen ved første nevning. Test: antall leverte filer er lik antall baner i meldingen.
- **lesson.status-did-not-say-status-or-what-to-do** (2026-10-06, major): Eieren 06.10 om statusen han fikk: «Dette sier meg ingenting om hva status er eller hva jeg skal gjøre.» Han skrev selv formålet og spurte hva som gjensto for å få prøvd med de to mottakerne.
    - forebygging: En statusmelding åpner med hvor formålet står for dem det gjelder, så det eieren skal gjøre i nummererte punkter, så leddene som gjenstår. Arbeid på et sidespor kalles et sidespor. Test: kontrolløren får eierens ord fra §0 og svarer på om første avsnitt sier hva mottakerne har fått.
- **lesson.few-steps-was-counted-for-the-recipient-and-not-for-the-owner** (2026-10-07, minor): Utkastet til G1 talte tre håndgrep for mottakeren og skrev «én gang per person» for eieren («ett trykk» i spesifikasjonen bak). Bildet viste to Touch ID per person og en kode å sammenligne, og rekkefølgen på eierens steg sto feil. Kontrollen før framlegget fant det.
    - forebygging: Der «få håndgrep» er et formål, telles håndgrepene for hver part, eieren først, per person og per runde, fra bildene og i rekkefølgen de skjer. Et steg som følger av et forslag, merkes som forslag. Test: et opptak på en ren maskin der håndgrepene er telt.
- **lesson.a-second-safeguard-hid-that-the-first-had-no-test** (2026-10-06, major): Én av 145 innsatte feil, kalt nr. 100 i filnavnene for omkjøringen («fila legges tilbake mens haven-deploy kanskje går»), ble ikke fanget, og alle 133 testene var grønne med den.
    - forebygging: To vern foran samme handling får hver sin test der det andre ikke kan svare. En innsatt feil som ingen test fanger, leses i utskriften før den regnes som ufarlig. Test: for hvert vern finnes et tilfelle der bare det vernet står mellom skriptet og handlingen.
- **lesson.deadline-request-left-out-what-follows-when-it-passes** (2026-10-06, minor): Utkastet til meldingen etter byttet ba eieren godkjenne to forespørsler innen 24 timer, uten å si at invitasjonen da er brukt opp og at en ny trengs (etter kontrollørens lesning: nytt bytte og ny omstart av staging), og uten steget etter: hans godkjenning av mottakernes egne forespørsler. Kontrollen før sending fant det.
    - forebygging: En forespørsel med frist sier hva som skjer når fristen går ut, og nevner hvert senere steg som er eierens. Test: kontrolløren spør for hver frist i meldingen «hva følger hvis den ikke holdes?» og «hva er hans neste steg etter dette?».
- **lesson.question-used-the-repos-words-and-came-back-as-a-question** (2026-10-07, minor): To av fem nummererte punkter til eieren kom tilbake som spørsmål: «Hva gjør assistentidentiteten?» og «Hva mener du med at vedlegg kan gå til main? Vi skal ikke lagre vedlegg i git så forklar hva du mener.»
    - forebygging: Et spørsmål til eieren bruker hans ord og sier hva en ting gjør før det spør om den. Test: kontrolløren leser hvert spørsmål, slik det blir sendt, som en som ikke kjenner repoet, og sier hvilke ord som må forklares.
- **lesson.render-candidate-skeleton-with-the-web-renderer-before-g1-gui** (2026-10-02, major): G1-GUI-bilder har vært mockups (butler-PDD-en) eller krevd en kjørende CellScaffold med Porthole-preview. Begge gir enten feil piksler eller en byggerunde før Kjetil får se noe.
    - forebygging: For en ny flate: eksporter de to filene fra CellScaffold origin/main (md5 i images/README.md), rendre kandidat-skjelett-JSON med eksempeldata i Playwright/Chromium (images/render.js i PDD_lister), lagre bildene som G1-GUI-referanse og mål oppførsel (onAction-payloads) i samme kjøring. Etter implementering: en test som krever at Swift-fabrikken gir kanonisk byte-lik JSON som fixturen bildet ble rendret fra, og en ny render fra cellens ekte state med pikseldiff mot referansen. PDD_lister: 0 piksler avvik på tre flater.
- **lesson.shared-swiftpm-cache-lost-its-ownership-marker** (2026-10-08, minor): Første bygg i et nytt CellProtocol-arbeidstre stoppet etter 4 s: haven-swiftpm.sh exit 64, «existing cache lacks the required ownership marker: …/T/haven-swiftpm-bounded/caches/90c10549…».
    - forebygging: Byggeskript for en PDD setter HAVEN_SWIFTPM_CACHE_KEY=<pdd-slug> (egen cache) i stedet for å reparere den delte; koster ett kaldt bygg (6 min for CellProtocol). Test: skriptet skriver cache-key i rapporten.
- **lesson.xctest-stdout-export-interleaves-with-its-own-log** (2026-10-08, minor): En test printet 49 kB JSON til stdout mellom markører for at byggeskriptet skulle klippe den ut; fila ble ugyldig ved byte 49156 — XCTests egen «Test Case '…' passed»-linje lå midt inne i JSON-en.
    - forebygging: En test som skal levere data til et skript, skriver til en fil (NSTemporaryDirectory()) og printer bare stien; skriptet validerer JSON før det kopierer. Og: /usr/local/bin/python3 på Kjetils Mac er en x86-binær («Bad CPU type in executable») under launchd — bruk /usr/bin/python3 eller node i skript.
- **lesson.textfield-cannot-carry-instance-identity-in-a-mount** (2026-10-08, major): Inne i en ComponentSurface-montering kan Button si hvilken liste den gjelder (payload fra raden), men TextField sender bare en string til en fast targetKeypath — «Legg til …» i montering nr. 2 ville havnet i aktiv liste.
    - forebygging: Kjetil valgte A (2026-10-08): SkeletonComponentActionContext (struct + @TaskLocal) i CellBase; cellen leser mount.instanceID; CellScaffold bytter ScaffoldKit-typen til en typealias i integrasjonspakken. Regel for nye komponenter: alt som skal vite instansen går via Button-payload eller monteringskonteksten — aldri via aktiv-tilstand i cellen. Test: ListsCellTests.testMountedComponentContextTargetsTheMountedListNotTheActiveOne.
- **lesson.capability-based-layout-variant-replaces-client-checks** (2026-10-08, minor): Flytting av punkter trengte piler i appen og dra-og-slipp på web, uten to skjeletter eller klientnavn.
    - forebygging: layoutVariants: [{requiresCapability: [drag], hidden: true}] på pilene: web erklærer drag (porthole-webo.js), Binding erklærer pointer/hover/keyboard eller touch (PortholeView.swift) — pilene forsvinner av seg selv den dagen appen får drag-adapteren. Test: layoutVariant(in:) med begge kapabilitetssett (ListsConfigurationTests) + web-harness variants (render-report-wp5.json).
- **lesson.explore-requiredkeys-match-codable** (2026-10-12, major): Schema-gyldig konfigurasjon kunne mangle felt som Codable krever.
    - forebygging: Sammenlign requiredKeys med avvisning ved fjerning av hvert required felt; ta med nested visibility/privacy og recursive kind/all/any.
- **lesson.context-startup-independent-task-cycle** (2026-10-12, major): TaskLocal vernet samme kallkjede, men kildekontroll fant mulig motsatt gate-rekkefølge for to oppstarts-Tasks.
    - forebygging: Serialiser uavhengige røtter før lokale gates og bevar nested scope; test to samtidige røtter i en allerede syklisk fixture.
- **lesson.shared-cellresolver-fixture-unique-names** (2026-10-12, minor): Integrasjon kunne treffe en tidligere emitter selv om nytt registerkall ikke kastet.
    - forebygging: Bruk unike registreringsnavn i sharedInstance-fixtures, og mål actual loadCell/flow mot den nye cellen.
- **lesson.gui-image-number-from-another-source** (2026-11-17, minor): G1-GUI-bildet for dekningsvisningen sa «21 elementer»; den bygde flaten sa 19. Oppdaget i ACCEPT (parity), ikke før.
    - forebygging: Hvert tall i et G1-GUI-bilde regnes av samme kode og samme data som flaten kommer til å bruke, eller merkes som plassholder i §3 med kilden oppgitt. Sammenlign tallene i bildet mot datakilden før bildet sendes til godkjenning.
- **lesson.placeholder-text-in-approved-image** (2026-11-17, minor): Dialogen i det godkjente bildet viste rapportnavnet «coverage/spillverksted-2026-11-09.json»; den bygde flaten viser kjørerens ekte reportRef «playwright/purpose-driver». Avviket måtte godkjennes i ettertid.
    - forebygging: Ingen oppdiktede strenger i et G1-GUI-bilde: bruk den verdien kjøreren faktisk skriver, eller sett «eksempel» synlig i bildet og list strengen i §3 som noe som vil endre seg.
- **lesson.await-inside-xctunwrap-autoclosure** (2026-11-17, major): To Mac-bygg (1047 s kaldt + 207 s) gikk tapt på `try XCTUnwrap(object(try await state(...)))` i en ny Swift-test: «'async' call in an autoclosure that does not support concurrency».
    - forebygging: Før en Swift-test sendes til bygg: `grep -n 'XCTUnwrap(.*await' Tests/` skal være tomt; await på egen linje, så XCTUnwrap på verdien. Legg sjekken i jobben som første steg.
- **lesson.denied-is-thrown-not-returned** (2026-11-17, minor): Negativ test ventet `{"error": "not_authorized"}` fra cellen når en fremmed identitet skrev; testen falt med «caught error: denied(...)» fra GeneralCell.
    - forebygging: Negative tilgangstester bruker do/catch, godtar både kastet `denied` og svarobjekt, og leser tilstanden etterpå for å vise at ingenting endret seg.

## Book 23-noder som kan være forelder/gjenbruk (leksikalsk forslag, verifiser)
- purpose://digital-work [active] — Digital work
- purpose://gui.quality.functional-accessible [active] — Functional accessible GUI
- purpose://self-determination.data.use-purpose [candidate] — Purpose binding for data use
- purpose://candidate.workbench-assistant.select-tools-by-purpose [candidate] — Velger verktøy og GUI-elementer ut fra formål

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
| test.native.delta-fixtures-swift | purpose://candidate.native-dokumenteditor.delta-parity | `swift test --filter RichTextDeltaTests` i Docker og på Mac. Korpus `Tests/Fixtures/rich-text-delta.v1.json` (compose, transform med prioritet, transformPosition, emoji/surrogatpar, U+FFFC) | TESTRESULT.md#delta | venter |
| test.native.delta-fixtures-quill | purpose://candidate.native-dokumenteditor.delta-parity | `node checks/delta-fixtures.mjs` kjører samme korpus mot web-versjonen av `quill-delta` | TESTRESULT.md#delta | venter |
| test.native.format-rundtur | purpose://candidate.native-dokumenteditor.write | Enhetstest: attributtert tekst → delta → attributtert tekst for hvert format; resultatet godtas av `RichDocumentState.applyDelta` (fixture fra CellScaffold) | TESTRESULT.md#format | venter |
| test.native.ui-format-iphone-mac | purpose://candidate.native-dokumenteditor.write | XCUITest/off-screen-render i Binding: skriv, merk, trykk Fet/Overskrift/Liste, les `document.current` | TESTRESULT.md#ui | venter |
| test.native.konflikt-rebase | purpose://candidate.native-dokumenteditor.sync | Enhetstest med falsk celle som svarer `conflict` med nyere `current`; køen rebases og sendes, sluttekst lik forventet | TESTRESULT.md#sync | venter |
| test.native.retry-samme-operasjon | purpose://candidate.native-dokumenteditor.sync | Falsk celle kaster nettverksfeil etter å ha tatt imot; nytt forsøk har samme `operationId` og svaret `duplicate` tømmer køen | TESTRESULT.md#sync | venter |
| test.native.live-oppdatering | purpose://candidate.native-dokumenteditor.live | Staging: skriv på web, mål tid til teksten står i Binding, tre ganger | TESTRESULT.md#live | venter |
| test.native.utkast-overlever-omstart | purpose://candidate.native-dokumenteditor.draft-safe | Enhetstest av lagret kø + manuell: flymodus, skriv, avslutt app, slå på, åpne | TESTRESULT.md#draft | venter |
| test.native.kommentar-rundtur | purpose://candidate.native-dokumenteditor.comments-presence | Kommentar laget i Binding vises på web og omvendt; «Løs» virker begge veier | TESTRESULT.md#comments | venter |
| test.native.embed-rundtur | purpose://candidate.native-dokumenteditor.embeds | Bilde satt inn i Binding vises på web; diagram satt inn på web vises i Binding | TESTRESULT.md#embeds | venter |
| test.native.eksport | purpose://candidate.native-dokumenteditor.export | Eksporter fylt dokument til .md og .pdf på begge plattformer; åpne filene | TESTRESULT.md#export | venter |
| test.native.legacy-kinds | purpose://candidate.native-dokumenteditor.legacy-kinds | Snapshot-render av et oppsett med `documentHelp`/`documentChat`; ingen «støttes ikke ennå» | TESTRESULT.md#legacy | venter |
| test.native.lesetilgang | purpose://candidate.native-dokumenteditor.access-from-agreement | Identitet med bare `r---`: teksten vises, redigering er av, ingen `change` sendes | TESTRESULT.md#auth | venter |
| test.native.e2e-tre-klienter | purpose://candidate.native-dokumenteditor.root | Staging, tre klienter, 2 min skriving, sammenlign tekst hos alle tre med `document.current` | TESTRESULT.md#e2e + video | venter |

## 6. Åpne spørsmål til Kjetil

1. **Hvor bor delta-reglene?** Jeg foreslår en liten ren Swift-modul i CellBase (arbeidsnavn `RichTextDelta`: compose, transform, transformPosition), testet mot samme fixtures som `quill-delta` på web. Da kan den testes på Linux i skyen, og CellScaffold kan senere bruke den i stedet for sin egen `applyDelta`. Alternativet er å legge den inne i CellApple, men da kan den bare testes på Mac. Jeg anbefaler CellBase.
2. **Eksport til Word.** Markdown og PDF kan lages likt på Mac og iPhone. Word (.docx) kan macOS lage med systemet, iOS kan ikke uten eget bibliotek. Forslag: Markdown og PDF på begge nå, Word på Mac nå, Word på iPhone senere. Greit, eller skal Word vente på begge?
3. **Hvor mye i første runde?** Forslag til rekkefølge, hver del en egen PR som bygger på Mac: (a) delta-modul + skrive/formatere + sync + utkast, (b) live-oppdatering + kommentarer + markører, (c) bilder/diagrammer + eksport + gamle oppsett. Studentene kan skrive i Binding etter (a). Greit, eller vil du ha alt i én levering?

## 7. Revisjonslogg

| Iterasjon | Dato | Hva endret seg | Hvem |
|---|---|---|---|
| 0 | 2026-11-20 | Opprettet med `purpose_dev.py new` | Claude |
| 1 | 2026-11-20 | §0 audit mot CellProtocol main 669850b og CellScaffold main 272580b; funnet at bare `richDocument` gjenstår på main; §1 tre med 11 formål + pakker; §2; §3; §5 14 nye tester; §6 tre spørsmål; 7 mockup-bilder | Claude (tråden «Bygg native dokumenteditor i Binding») |
