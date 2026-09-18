# Formålsspesifikasjon — Ark (tabell som tåler regnearkbruk)

Oppgavemappe: `PDD_ark-regneark_2026-09-17` · Opprettet 2026-09-17 · Iterasjon 1 (ikke godkjent)

> Regel: ingen plan før G1 er godkjent av Kjetil. For GUI: ingen implementering før G1-GUI (rendret bilde) er godkjent.
> Et dokument om leveransen teller aldri som leveransen.

## 0. Intensjon (ordrett) og brief-audit

> Ok - jobb med tabell funksjonaliteten - vi bør ha noe som er effektivt nok til å kunne brukes som regneark.

### 0.1 Kravet velter mitt eget forrige forslag

For to dager siden anbefalte jeg `Grid`/`GridRow` fra SwiftUI som vei til felles kolonnebredde
(`SKELETON_UTVIDELSESFORSLAG_2026-09-15.md`, F1b). **Det forslaget holder ikke mot regnearkkravet, og
det er min feil at jeg ikke så det da.** SwiftUI-ens `Grid` finner kolonnebredden ved å måle alle
barna sine. Å måle alle barna er nøyaktig det et regneark ikke kan gjøre: et ark med 50 000 rader har
ingen «alle barn» som får plass i minnet.

Det riktige grepet er det motsatte, og det er også det Excel, Numbers og Sheets gjør: **kolonnebredde
er lagret tilstand, ikke en måling.** Brukeren drar i kanten, verdien lagres, og «tilpass bredde» er
en eksplisitt handling som ser på de radene som allerede er hentet. Da trengs ingen målepass, og
rendereren kan holde seg lat hele veien.

Det snur også svaret på det andre spørsmålet: hva som er flaskehalsen.

### 0.2 Flaskehalsen er datakontrakten, ikke rutenettet

`SkeletonGrid.getItems()` (`Sources/CellBase/Skeleton/SkeletonDescription.swift:2372`) gjør ett
`resolver.get` og forventer hele lista tilbake. `SkeletonList.elements` er likeledes en hel
`ValueTypeList`. Det finnes ingen offset, ingen grense, ingen markør noe sted i skjelettets
dataveier. Rendereren er lat — `LazyVGrid` bygger bare synlige ruter — men *dataene* er det ikke.
Et ark med 250 000 rader og 20 kolonner betyr 250 000 `Object`-ordbøker og fem millioner
`ValueType`-bokser i minnet før første rad kan vises, og `ValueType` er en `indirect enum`
(`Sources/CellBase/ValueTypes/ValueType.swift:11`), så hver av dem er en egen allokering.

**Ingen renderer-endring redder dette.** Derfor er hovedsaken i denne oppgaven et vindu i
datakontrakten, ikke et nytt layoutelement.

### 0.3 Hva prototypen faktisk viser

`prototype/ark.html` er en kjørende modell — ikke en mockup. Den har virtualiserte rader, låst
overskrift og låste kolonner, bredder som tilstand med dra-i-kanten, celle- og områdemerking,
tastaturnavigasjon, og redigering som blir et forslag i stedet for en skriving. Datakilden bak er
skrevet slik at den **bare** kan svare på vinduer, for at kontrakten skal være til å ta og føle på.

Målt med Playwright, 60 tilfeldige hopp per størrelse:

| Rader i arket | Tegnetid median | p95 | Celler i DOM | Heap |
|---|---|---|---|---|
| 1 000 | 2,3 ms | 6,1 ms | 880 | 9,5 MB |
| 50 000 | 3,6 ms | 18,9 ms | 880 | 9,5 MB |
| 250 000 | 3,0 ms | 8,1 ms | 880 | 9,5 MB |

Poenget er ikke tallene i seg selv, men at **de tre radene er like**. Celler i DOM og minnebruk er
konstante; bare rulleboksens høyde vokser. p95-toppene er de kalde blokkhentingene på 200 rader.
Det er formen vi vil ha i Swift også.

**Hva prototypen ikke viser:** den sier ingenting om SwiftUI-ytelse. En nettleser og
`LazyVStack` er ikke det samme. Den avgjør interaksjonsmodellen og datakontrakten — som er det som
må avgjøres før noen skriver Swift — og den etterlater ett tall vi ikke har målt, se §6.1.

### 0.4 Brief-audit

| Påstand / antatt kapabilitet | Audit | Kilde |
|---|---|---|
| Rendereren er lat | **retrieved** — `LazyVGrid`, bygger bare synlige ruter | `CellGridView.swift:84` |
| Dataveien er lat | **contradicted** — hele lista hentes i ett kall | `SkeletonDescription.swift:2372` |
| SwiftUI `Grid` gir felles kolonnebredde | **retrieved, men uegnet** — den måler alle barn | Apple-dokumentasjon; F1b i utvidelsesforslaget |
| Ett element per rutenettrute i dag | **retrieved** | `CellGridView.swift:84-95` |
| `elements` og `keypath` utelukker hverandre | **retrieved** — `if hasDynamicSource / else` | `CellGridView.swift:85,89` |
| `List` har allerede radvalg og radaktivering | **retrieved** | `SkeletonDescription.swift:1413-1419` |
| Virtualisering + lagrede bredder holder til 250 000 rader | **retrieved (prototype)** — i nettleser, ikke i SwiftUI | `prototype/ark.html`, tabellen over |
| Konstant minnebruk i Swift med samme form | **unavailable** — ikke målt, se §6.1 | — |
| En celleendring i entitetsdata krever eiersignatur | **retrieved** — G1 godkjent 2026-09-15 | `PDD_entitetsdata-egen-kontroll_2026-09-08` |

### 0.4b Bekreftet av Kjetil 2026-09-18

> Det du sier om Grid er at den er mer egnet for flater mens tabell er det riktige verktøyet for å
> vise tabell. Høres logisk ut - jeg er for.

Det er delingen jeg foreslo, sagt kortere enn jeg klarte: **`Grid` er et layoutverktøy for flater,
og et ark er verktøyet for å vise tabell.** Det avgjør §0.5 under — grensen mellom `List` og `Sheet`
— og det avgjør at `Grid` ikke skal bygges ut til å bli en halv tabell. F1a i
`SKELETON_UTVIDELSESFORSLAG_2026-09-15.md` (la overskriftsrad og dynamiske rader leve i samme `Grid`)
står fortsatt, fordi det er en layoutsak. F1b — kolonner på `List` — hører til tabellsiden og
behandles her.

Retningen er dermed godkjent. Selve formålstreet venter fortsatt på G1.

### 0.5 Grensen mot `List` — to ting, ikke ett

Det er fristende å la ett element dekke begge behov. Det bør det ikke.

- **En tabellvisning av en liste.** Raden er enheten; cellene er presentasjon. Titalls til noen tusen
  rader. Importforhåndsbildet med 189 rader er dette. Løses av `columns` på `SkeletonList`, som
  foreslått i F1b — og den saken står fortsatt.
- **Et ark.** *Cellen* er enheten: den har en adresse, kan merkes, redigeres og siden refereres til.
  Tusenvis til hundretusener av rader. Det er denne oppgaven.

Prøven er om enheten er forskjellig, og det er den. Ulik meningsbærende enhet gir ulikt element.
Å legge vindushenting, celleadressering, frosne kolonner, bredde-tilstand og celleredigering på
`List` ville gjort `List` til et regneark som noen ganger ser ut som en liste.

## 1. Formålstre

| purposeRef | Tittel | Forelder | Goal (outcome) | Verifier | Status |
|---|---|---|---|---|---|
| `purpose://human-agency` | Human agency and understanding | — | Eksisterende rot | — | active (gjenbruk) |
| **A** `purpose://candidate.ark.window-not-whole-set` | Arket ber om vinduer, aldri om alt | `human-agency` | Rendereren henter bare de radene den skal tegne. Antall rader i kilden påvirker ikke minnebruk eller første visning. | Målt: minne og antall bygde celler er konstant fra 1 000 til 250 000 rader. | candidate |
| **B** `purpose://candidate.ark.cell-owns-paging` | Cellen eier sidepolitikken | `candidate.ark.window-not-whole-set` | Skjelettet ber om et område og leser et svar; cellen bestemmer hvordan det skaffes. Ingen funksjonskall fra skjelettet. | Kontraktsinspeksjon: bare keypath inn og handling ut, som `selectionActionKeypath`. | candidate |
| **C** `purpose://candidate.ark.width-is-state` | Bredde er tilstand, ikke måling | `candidate.ark.window-not-whole-set` | Kolonnebredde er en lagret verdi brukeren kan dra i. Ingen layoutpass måler innhold som ikke er hentet. | Negativ test: ingen kodesti måler celler utenfor det hentede vinduet. «Tilpass bredde» ser bare på vinduet. | candidate |
| **D** `purpose://candidate.ark.cell-has-an-address` | Cellen har en adresse | `human-agency` | Rad og kolonne identifiserer en celle entydig, så den kan merkes, redigeres og senere refereres til. | Merking av område og tastaturnavigasjon virker over vindusgrenser. | candidate |
| **E** `purpose://candidate.ark.edit-is-a-proposal` | En redigering er et forslag | `self-determination.data` | Over entitetsdata skriver arket aldri direkte. Endringer samles og skrives først ved eiersignatur, i én batch med ett chronicle-innslag. | Negativ test: celleredigering uten signatur persisterer ingenting. | candidate |
| **F** `purpose://candidate.ark.frozen-edges-hold` | Låste kanter følger med | `human-agency` | Overskriftsrad og låste kolonner holder seg synlige og i takt med rullingen i begge retninger. | Visuell test + rullesynkronisering. | candidate |
| **G** `purpose://candidate.ark.large-is-not-slower` | Stort ark er ikke tregere enn lite | `candidate.ark.window-not-whole-set` | Rulling i et ark med 100 000 rader kjennes likt som i ett med 1 000. | Ytelsestest i Binding med begge størrelser, samme budsjett. | candidate |
| **H** `purpose://gui.ways-in-are-reachable` | Flaten skjuler ikke sine egne veier inn | `pkg.std.gui-surface` | Arkflaten viser veiene inn i tom tilstand. | `SkeletonReachabilityAudit`. | active (gjenbruk) |

## 2. Avgrensning og avhengigheter

**Hva dette ikke er:**

- Ikke formler. Et uttrykkspråk med avhengighetsgraf og omregning er et eget lag over arket, og en
  egen oppgave. Formål D legger grunnlaget ved å gi cellen en adresse, men ingenting mer.
- Ikke `columns` på `List` (F1b i utvidelsesforslaget). Den saken lever videre for tabellvisninger av
  lister, og løses uavhengig av denne.
- Ikke import eller eksport av regnearkfiler. Den veien inn hører til entitetsdata-oppgaven.
- Ikke sortering og filtrering på tvers av hele settet. Med vindushenting er det cellens ansvar, og
  må spesifiseres der. Se §6.3.

| Kapabilitet | Kilde | Avgrensning | Må virke før test? |
|---|---|---|---|
| Lat rendering av ruter | `CellGridView.swift:84` | Later bare views, ikke data. | Ja — formål A |
| Radvalg og radaktivering | `SkeletonDescription.swift:1413-1419` | Rad, ikke celle. Mønster å gjenbruke, ikke løsning. | Ja — formål D |
| Handlings-keypath-mønsteret | `selectionActionKeypath` | Fungerer i dag for enkelthendelser; ikke prøvd for noe som fyres av under rulling. | Ja — formål B |
| Eiersignert batch-skriving | `EntityBatchPersistEnvelope` | Finnes. Har ingen forslagskø foran seg. | Ja — formål E |
| Vindushenting fra en celle | **finnes ikke** | — | Ja — formål A, B |
| `SkeletonReachabilityAudit` | CellProtocol | Ser struktur, ikke ytelse. | Ja — formål H |

## 3. Forventningskontrakt — «Det du kommer til å se»

Tre av radene er allerede levert som kjørende prototype og bilder; de er merket slik.

| Leveranse | Type | Hvor | Referanse | Godkjent |
|---|---|---|---|---|
| Arket med 50 000 rader, låst kolonne, merket område | bilde | `images/` | `ark-50k-v1.png` | levert, venter G1-GUI |
| Forslag som venter på signatur | bilde | `images/` | `ark-forslag-v1.png` | levert, venter G1-GUI |
| Datakontrakten forklart i flaten | bilde | `images/` | `ark-datakontrakt-v1.png` | levert, venter G1-GUI |
| Kjørende modell av interaksjon og datakontrakt | kjørende flate | `prototype/` | `ark.html` | levert |
| `Sheet`-elementets kontrakt som JSON-skjema med fixtures | fil | `contract/sheet_v1.json` | — | nei |
| Tom tilstand: ark uten rader, med veiene inn synlige | bilde | `images/` | `ark-tom-v1.png` | nei |
| Målt ytelse i Binding: 1 000 mot 100 000 rader, samme budsjett | testutdata | `TESTRESULT.md#ytelse` | — | nei |
| Negativ test: celleredigering uten signatur skriver ingenting | testutdata | `TESTRESULT.md#negative` | — | nei |
| Hva dagens skeleton ikke kan rendre av bildene | fil | `images/README.md` | — | nei |
| Kjørende flate i Binding med bokprosjektrelasjonene i et ark | kjørende flate | Binding, Relasjoner | — | nei |

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
- purpose://skeleton.owner-entity-access [draft] — Owner entity access affordance


## 5. Avledede tester

| testRef | Type | Beskrivelse | Hvordan | Formål | Bevis |
|---|---|---|---|---|---|
| `test.ark.memory-is-flat` | command | Minnebruk og antall bygde celler er innenfor samme budsjett ved 1 000 og 100 000 rader. | Ytelsestest i Binding, begge størrelser i samme kjøring. | A, G | `TESTRESULT.md#ytelse` |
| `test.ark.window-only` | command | Cellen får bare vindusforespørsler, aldri en forespørsel om hele settet. | Tellende test-dobbel bak keypathen. | A | `TESTRESULT.md#ytelse` |
| `test.ark.no-function-calls` | inspection | Skjelettet kaller ingen funksjon; det leser keypath og fyrer handling. | Kildeinspeksjon av `Sheet`-rendereren. | B | `ACCEPT.md#kontrakt` |
| `test.ark.width-never-measures-unloaded` | command | Ingen kodesti måler celler utenfor det hentede vinduet. «Tilpass bredde» ser bare på vinduet. | Negativ test med instrumentert målefunksjon. | C | `TESTRESULT.md#negative` |
| `test.ark.address-survives-window` | command | Merket område og tastaturnavigasjon holder når rader faller ut av vinduet og hentes inn igjen. | XCTest + UI-test. | D | `TESTRESULT.md#ark` |
| `test.ark.edit-without-signature-writes-nothing` | command | Redigerte celler over entitetsdata persisterer ingenting før signatur. | Negativ XCTest mot EntityAnchor. | E | `TESTRESULT.md#negative` |
| `test.ark.signature-is-one-batch` | command | Signering gir én `entity.batchPersist` med alle endringene og ett chronicle-innslag. | XCTest. | E | `TESTRESULT.md#trace` |
| `test.ark.frozen-stays-in-sync` | command | Låst overskrift og låste kolonner følger rullingen i begge retninger. | UI-test med skjermbilde. | F | `TESTRESULT.md#ark` |
| `test.skeleton.no-unreachable-elements` | command | Arkflaten skjuler ikke sine egne veier inn. | `testNoLocalSurfaceHidesItsOwnWaysIn`. | H | `TESTRESULT.md#reachability` |
| `test.build`, `test.regression` | command | `pkg.std.everything-works`. | xcodebuild + swift test. | — | `TESTRESULT.md#build` |

En foreslått måling av dagens datavei ligger i `proposed-tests/SkeletonTableDataPathBenchmarkTests.swift`.
**Den er skrevet, men aldri bygget** — Cowork-VM-en har ingen Swift-verktøykjede — og ligger derfor
utenfor testmålet, ikke i `Tests/`. Den må kompileres og kjøres på macOS før noe tall fra den siteres.

## 6. Åpne spørsmål til Kjetil

**6.1 Hvem måler Swift-siden?**
Prototypen viser at formen bærer i en nettleser. Det tallet som mangler er om `LazyVStack` med
lagrede bredder holder samme budsjett i SwiftUI. Det krever et bygg på macOS, som jeg ikke kan kjøre
herfra. Skal jeg sette opp et skript Codex kan fyre av, eller vil du kjøre det i Xcode?

**6.2 Hvor stort ark skal vi faktisk love?**
«Effektivt nok til å brukes som regneark» kan bety 10 000 rader eller 1 000 000. Det avgjør om
vindushenting alene holder, eller om vi også må ha et kolonnelagret format på cellesiden. Jeg
foreslår at vi fester et tall i formål G — mitt forslag er 100 000 rader og 50 kolonner som krav, med
lineær oppførsel over det.

**6.3 Hvem sorterer og filtrerer?**
Med vindushenting kan ikke rendereren sortere — den ser bare 200 rader. Sortering og filtrering må da
være noe cellen gjør, og arket ber om. Det er riktig, men det betyr at et ark over en dum datakilde
ikke kan sorteres i det hele tatt. Skal `Sheet` kreve at cellen kan sortere, eller skal det være en
kapabilitet arket spør om og skjuler når den mangler?

**6.4 Formler — nå eller senere?**
Jeg har holdt dem utenfor. Men hvis ark skal brukes som regneark i praksis, kommer spørsmålet. Formål
D gir cellen en adresse, som er det formler trenger. Skal jeg skissere uttrykkslaget som en egen
formålsoppgave nå, eller vente til arket står?

## 7. Revisjonslogg

- 2026-09-17, iterasjon 0: opprettet av `purpose_dev.py new`.
- 2026-09-18: Kjetil bekreftet delingen — Grid for flater, ark for tabell. Retningen godkjent;
  formålstreet venter fortsatt på G1.
- 2026-09-17, iterasjon 1: prototype bygget og målt, formålstre skrevet. Retter mitt eget F1b-forslag
  fra 15.09: SwiftUI `Grid` måler alle barn og kan ikke brukes til et ark. Venter på G1.
