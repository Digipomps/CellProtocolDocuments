# PLAN — palazzo tolkning og vektjustering

Oppgavemappe: `PDD_palazzo-tolkning-og-vektjustering_2026-09-26` · 2026-09-28 · Venter på G2

Figuren `images/plan-v1.png` viser rekkefølgen og hvem som gjør hva.

## Dette gjør du (Kjetil)

| Når | Hva | Hvorfor |
|---|---|---|
| Nå | Si ja til planen (G2) | Ingen kode skrives før det |
| Nå, eller før WP3 starter | Merge `codex/palazzo-vetofelle-20260924` inn i `pdd/palazzo-2026-09-14`, eller si at arbeidet kan bygges oppå vetofelle-grenen | WP3 og WP5 bygger på vetofelle-rettingen |
| Nå, gjerne | Se over de sju oppdiktede gjestene i WP4 (FORMAALSSPEC §6 spm. 2), og si fra hvis avvik 2 eller 3 i §3 ikke er greit | Benken er ikke bedre enn gjestene |
| Etter WP1a, **før** noe lander på CellProtocol main | Se på de native bildene (lukket, åpen og smal bredde) ved siden av referansen, og si ja | Regelen din: ny kapabilitet testes mot funksjon og formål før main |
| Når benken er kjørt (etter WP4) | Velg tallene fra `maaling/vektbenk-v1.md` | Kjetil 26.9: «Der må vi nok prøve oss fram» |
| Før WP8 | Ha Macen våken med Claude-appen oppe. Godkjenn datamaskinstyring for Binding når spørsmålet kommer | Skjermbildene tas i appen |
| Etter G3 | Merge pull requestene: Binding-pinnen (WP7) og Porthole-testen (WP2) | Binding er pinnet til `b5b7282`, og løftet tar med alt som er kommet på main siden |
| Til slutt | G3: se skjermbildene ved siden av bildet du godkjente | Akseptanse |

Alt annet gjør Losen og Codex. Lange bygg og testkjøringer går som skriptjobber i Losen-køen på Macen din.

## Allerede gjort, før planen: prøve av brikkene (A5)

To måter å bygge brikkene på ble prøvd i Porthole-rendereren fra CellScaffold `adf48d46`, med husets stilark. Skriptet er `images/actual/porthole-brikker-spike.py`.

- **S1: emnene som barn av raden, og brytning på hele lista.** Den første brikken havner på samme linje som radteksten. Forkastet.
- **S2: ett barn med en innvendig liste med brytning.** Brikkene brytes pent under raden, slik bildet viser. Lukket som standard, og åpne/lukke sender ingenting til cellen. **Valgt.**

Bilder: `images/actual/porthole-brikker-spike-S1-S2.png` og `…-S2-aapen.png`. Dette viser at strukturen virker i Porthole. Det viser ikke den native rendereren. Den må ha A1, og en test i WP1 må bekrefte at den innvendige lista leser emnene fra raden.

## Arbeidspakker

Hver pakke har et bladformål (purposeRef), en utfører, testene den må gjøre grønne og det den leverer til §3.

### Før WP1 — bildeveien prøves

SwiftUI `List` tegnes ikke av `ImageRenderer`. Bildene tas derfor med `NSHostingView` i et vindu utenfor skjermen, via `cacheDisplay(in:to:)`. Losen prøver at veien gir en PNG med innhold, som en liten skriptjobb, før WP1 starter.

### WP1 — Native tre-liste i CellApple · A1

- **purposeRef:** …native-tre-liste
- **Utfører:** Codex skriver i en egen worktree fra CellProtocol `origin/main`, `_worktrees/cellprotocol-native-treelist`, opprettet fra macOS. Losen verifiserer og lander med `HAVEN-Deploy/_handoff/LANDING/land-cellprotocol.sh`.
- **Innhold:**
  - En ren funksjon som flater ut treet, med samme regler som Portholes `flattenListTree` og `seedExpandedFromState`. Den kan testes uten skjerm.
  - `CellListView` bruker funksjonen, viser en pil på rader med barn og holder åpne/lukke lokalt.
  - En rad med barn kan ha en innvendig `List` med `wrap`, som leser fra radens egne data (struktur S2).
- **Tester:** ligger i `CellBaseTests`, bak `#if os(macOS)`. Den testmengden kjøres av macOS-CI-en (`security-regression-macos.yml`: `swift test`). Linux-CI-en bygger bare CellBase.
  - test.native.tree-list
  - test.native.tree-parity: samme data som `playwright/skeleton-list-tree.spec.js`, som skal gi samme synlige rader i samme rekkefølge
  - en test for at den innvendige lista i en rad leser `tags` fra raden
  - en test for at lista som leses inn på nytt med samme rad-id, beholder en åpen rad åpen
  - test.regression: hele CellProtocol på ren eksport av origin/main mot worktreen
  - test.docs-updated: skjelettdokumentasjonen sier at `childrenKeypath` rendres native. Oppdateres i samme commit.
- **WP1a leverer:** `images/actual/native-brikker-{lukket,aapen,smal}-v1.png` ved siden av referansen, på iPhone-bredde og smalere. **Kjetil ser dem og sier ja før WP1b.**
- **WP1b leverer:** commit på CellProtocol main med grønn CI.
- **Stopp:** krever en løsning et nytt skjelettelement eller en ny modifikator, stopper pakken og spørsmålet går til Kjetil.

### WP2 — Brikker i Porthole, som test · A5

- **purposeRef:** …emner-som-brikker
- **Utfører:** Codex legger strukturen S2 som ny Playwright-test i CellScaffold (`playwright/skeleton-list-tree-chips.spec.js`), med skjermbilde. Losen kjører den som skriptjobb.
- **Tester:** test.gui.chips-porthole.
- **Leverer:** `images/actual/porthole-brikker-v1.png`, og testen på en gren i CellScaffold (`pdd/palazzo-tolkning-brikker`) med pull request. Kjetil merger etter G3.

### WP3 — Vektmodellen · B1–B4 og prinsippene

- **purposeRef:** …siste-trykk-gjelder, …veto-bare-artikkelen, …vekt-avgjor, …justering-parametrisert, …prinsipper-holder
- **Utfører:** Codex i worktree `_worktrees/palazzoscaffold-vekter` fra `codex/palazzo-vetofelle-20260924`, eller fra `pdd/palazzo-2026-09-14` etter din merge. Losen verifiserer med samme mønster som `HAVEN-Deploy/_handoff/PALAZZO-VETO/test-vetofelle.sh`: hele Palazzo-suiten på ren eksport mot worktreen.
- **CellProtocol-versjon:** Palazzo bygger mot en ren eksport av en navngitt revisjon av CellProtocol main, satt med `CELLPROTOCOL_LOCAL_PACKAGE_PATH`. Revisjonen står i loggen. Den delte `../CellProtocol` brukes ikke, fordi den står på en annen tråds gren.
- **Innhold:**
  - `PalazzoWeightPolicy` samler alle tallene: vekt per reaksjon, hvor langt et nytt trykk flytter styrken, øvre grense, negativ emnevekt og terskel.
  - Grafen samler trykkene per artikkel til én gjeldende tilstand, beregnet fra den ordnede rekken. Ingen post skrives om.
  - Matcheren bruker den første negative posten i dag. Den byttes ut med siste trykk.
  - Vetoet gjelder bare selve artikkelen.
  - Summen over felles emner avgjør, med terskel og sortering. **Skalaen:** for en rett eller artikkel *c* er summen Σ over artiklene *a* hun har reagert på, av *vekt(a)* × *andelen av c sine emner som også står på a*. Én «Interessant» på arancini gir en rett som deler to av sju emner, 0,5 × 2/7 ≈ 0,14.
  - Dokumentasjonen, det vil si kommentarene i graf og matcher, oppdateres i samme commit.
- **Tallene** er foreløpige til du har valgt (WP6). Startverdiene står i koden merket «foreløpig».
- **Tester:**
  - test.weights.last-tap-decides, test.weights.sign-follows-last, test.weights.veto-article-only
  - test.weights.threshold, test.weights.monotone, test.weights.repeat-bounded, test.weights.policy-single-source
  - test.weights.single-positive-gets-offer: en gjest med ett positivt trykk får minst ett tilbud med standardtallene. Unntak bare hvis Kjetil uttrykkelig godtar noe annet i WP6.
  - test.principles, test.regression
- **Leverer:** en pushet gren (ikke merget) og TESTRESULT.md#weights.

### WP4 — Vektbenken · B5

- **purposeRef:** …vektbenk
- **Utfører:** Codex skriver benken som en test som bare kjører når `PALAZZO_WEIGHT_BENCH_PATH` er satt. Losen kjører den som skriptjobb, to ganger:
  - én gang i worktreen fra WP3, med et rutenett av parametre;
  - én gang på en ren eksport av `f548282`, med samme benkfil lagt inn og dagens matcher. Det er referansen.
- **Gjester:** sju simulerte gjester, hver med eget formål. Det er de seks i FORMAALSSPEC §6 spm. 2, pluss én som har trykket «Interessant» én gang og ingenting mer. Artiklene og rettene er fra Sicilia-dataene.
- **Rutenett:** hvor langt et trykk flytter styrken ∈ {0,25; 0,5; 1,0}, terskel ∈ {0; 0,05; 0,1; 0,2; 0,3} og negativ emnevekt ∈ {0,5; 1,0}. Til sammen 30 sett. Terskelene er valgt ut fra skalaen i WP3. De som gir samme tabell, slås sammen.
- **Tester:** test.maal.produksjonsvei, test.bench.inert-by-default, test.bench.has-null-reference.
- **Leverer:** `maaling/vektbenk-v1.md`. Per gjest: formålet, trykkene og hva hun får tilbudt i hvert sett og i dag. Tabellen markerer der en gjest ikke får det formålet hennes tilsier. Den har også en kolonne med antall tilbud i dag mot hvert sett, med **rødt flagg når en gjest får 0** og ikke fikk 0 i dag. Det er vernet mot en terskel som tar alt fra noen.

### WP5 — Reaksjonsraden og artikkelflaten · A2, A3

- **purposeRef:** …reaksjon-lesbar, …artikkelflate
- **Utfører:** Codex i samme worktree som WP3. Losen verifiserer.
- **Innhold:**
  - GET `entity.article.reaction.<artikkelnøkkel>` gir 0 eller 1 rad, bygget fra hennes siste egne reaksjon.
  - Raden har struktur S2: `{id, label, children:[{id, tags:[{label}]}]}`. `id` er artikkelnøkkelen, så den er stabil. Ellers lukkes en åpen rad ved hvert nytt trykk.
  - Artikkelkonfigurasjonen får en `List` med `childrenKeypath` og `expandedStateKeypath` som gir tom liste, så raden starter lukket.
  - Tekstene er de fra §3, med egen tekst for «Ikke for meg».
- **Tester:** test.cell.reaction-row, test.cell.auth-negative, test.cell.contract-fixtures, test.cell.stub-scan, test.skeleton.no-unreachable-elements, test.skeleton.purpose-actions-reachable (de tre reaksjonsknappene og kommentarfeltet), og en test av skjelett-JSON-en mot fixtures.
- **Leverer:** en pushet gren og `skeleton/artikkel.skeleton.json`.

### WP6 — Tallene du valgte

- **purposeRef:** …justering-parametrisert
- **Utfører:** Kjetil velger. Codex setter tallene som standardverdier og fjerner «foreløpig». Losen kjører WP3-testene og benken på nytt.
- **Leverer:** `maaling/vektbenk-v2.md` med de valgte tallene, og et oppdatert TESTRESULT.

### WP7 — Binding på ny CellProtocol

- **Utfører:** Codex løfter pinnen i `Package.resolved` til CellProtocol-commiten fra WP1, i en gren i Binding. Losen bygger med xcodebuild som skriptjobb. Kjetil merger pull requesten etter G3.
- **Tester:**
  - test.build (Binding)
  - test.regression: hele Binding-testmengden før og etter løftet, siden det tar med seg alt som er kommet på CellProtocol main siden `b5b7282`
  - test.skeleton.no-unreachable-elements i Binding

### WP8 — Paritet i kjørende app · A4

- **purposeRef:** purpose://gui.parity-with-approved-image
- **Utfører:** Losen. Palazzo kjører lokalt med grenen fra WP5/WP6, og Binding kobles til den via broen. Losen tar skjermbildene med datamaskinstyring på Macen din. Trengs det noe fra deg for å koble til, sier jeg det presist først.
- **Tester:** test.article.row-refresh (fire trinn), test.gui.parity, test.gui.load-time.
- **Leverer:** ACCEPT.md#parity, med bilde per trinn ved siden av referansen.

### WP9 — Avslutning

- Dokumentasjonen er allerede oppdatert i WP1 og WP3. Her sjekkes den med test.docs-updated.
- test.status-current: STATUS.md mot filene i mappen.
- Lærdommer legges inn i registeret.
- Justeringsmodellen foreslås som standard i `Tools/PurposePackages/` hvis den holder.
- STATUS.md holdes oppdatert.

## Rekkefølge

```
WP1a ──► (du ser bildene) ──► WP1b ──► WP7 ─┐
WP2 ─────────────────────────────────────────┤
WP3 ──► WP4 ──► (du velger) ──► WP6 ───────┼──► WP8 ──► G3 ──► WP9
WP3 ──► WP5 ───────────────────────────────┘
```

WP1, WP2 og WP3 kan starte samtidig. WP5 trenger WP3, siden raden skal vise siste trykk. WP8 trenger WP5, WP6 og WP7.

## Dataflyt

| Kant | Fra | Til | Kontrakt |
|---|---|---|---|
| Trykk | knapp på artikkelflaten | `entity.article.react` | PalazzoEntityCell, uendret |
| Raden | artikkelflaten (List) | `entity.article.reaction.<nøkkel>` | ny GET (WP5), bare eier |
| Tilbud | PalazzoEntityCell | PalazzoSignalGraphMatcher med policy | intern, WP3 |
| Åpne/lukke | rendereren | ingen | lokalt i rendereren |
