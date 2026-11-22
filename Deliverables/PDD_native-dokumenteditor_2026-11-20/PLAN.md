# PLAN — native dokumenteditor i Binding

Oppgavemappe: `PDD_native-dokumenteditor_2026-11-20` · G1 og G1-GUI godkjent 2026-11-22 · G2 godkjent 2026-11-22.

Leveres samlet (Kjetil 21.11: «alt i en levering»): **én CellProtocol-PR** (CellBase + CellApple) og **én Binding-gren** med pinløft. CellScaffold endres ikke: dokumentcellen og kontrakten er som på main 272580b, så staging trenger ingen ny utrulling for at Binding skal kunne skrive. Ingenting går i HAVEN-Deploy-køen fra denne oppgaven.

Hvor ting kjøres:
- CellBase (ren Swift): Docker `swift:6.1-noble` i skyen, og på Macen.
- CellApple (macOS + iOS), Binding, skjermbilder, staging-test: Kjetils Mac via Remote Control, i en egen worktree i `/Users/kjetil/Build/Digipomps/HAVEN/worktrees/`, aldri i delte arbeidstrær (minne `haven-long-runs-placement`).
- Fixture-paritet mot web: Playwright i skyen, med `CellScaffold/Public/vendor/quill/quill.js` (den Quill-versjonen web faktisk laster; `Quill.import("delta")`).

## Arbeidspakker (1:1 med bladformål, i rekkefølge)

| WP | purposeRef | Hva | Test som skal bli grønn | Utfører | Artefakter |
|---|---|---|---|---|---|
| WP0 | (§2-avhengigheter) | Mål fra Binding mot staging: `get document.current`, `set document.change` med svar, og om Flow `document.change` når Binding. Ren eksport av CellProtocol main og Binding main som baseline (bygg + testantall) | §2-radene får «målt» med tall | Claude via Mac RC | TESTRESULT.md#baseline, #avhengigheter |
| WP1 | delta-parity | `CellBase/RichText/RichTextDelta.swift`: ops (insert tekst/objekt, retain, delete, attributter), compose, transform(prioritet), transformPosition, UTF-16, U+FFFC. Korpus `Tests/CellBaseTests/Fixtures/rich-text-delta.v1.json` (≥ 60 tilfeller, også emoji og surrogatpar) | test.native.delta-fixtures-swift, test.native.delta-fixtures-quill | Claude (Docker + Mac) | kode, korpus, `checks/delta-fixtures.mjs` |
| WP2 | write | `CellApple/RichDocument/RichDocumentTextCodec.swift`: `NSAttributedString` ↔ delta. Tegnformat → font-trekk/understrek/gjennomstrek/lenke; linjeformat (header 1–3, list, blockquote) på avsnittets `\n`; avviser lenker som ikke er http/https/mailto | test.native.format-rundtur (+ fixture: hver delta godtas av `RichDocumentState.applyDelta`, kopiert som JSON fra CellScaffold) | Claude | kode, tester |
| WP3 | sync | `RichDocumentSession` (actor): kø, én forespørsel i lufta, samme `operationId` ved nytt forsøk, rebase ved `conflict`, `duplicate` = levert, remote events flettes inn, markør transformeres. Transport som protokoll; ny hjelper ved siden av `setValueType` som beholder `{status, current}` | test.native.konflikt-rebase, test.native.retry-samme-operasjon | Claude | kode, tester med falsk celle |
| WP4 | draft-safe | Ikke-bekreftet kø lagres per `documentId` i Application Support (samme felt som web sin `sessionStorage`-nøkkel). Sendes ved neste åpning | test.native.utkast-overlever-omstart | Claude | kode, test |
| WP5 | live | Abonner på Flow `document.change` hvis WP0 viser at den når fram; ellers og i tillegg: hent `current` hvert 2. s mens flaten er synlig og ingenting er i lufta | test.native.live-oppdatering | Claude (Mac + staging) | kode, målinger |
| WP6 | write, access-from-agreement | Editorflaten etter bildene: `UITextView` (iOS, formatlinje over tastaturet) og `NSTextView` (Mac, verktøylinje, statuslinje). `denied` eller uten `rw--` → skrivebeskyttet med forklaring. tvOS: skrivebeskyttet tekst | test.native.ui-format-iphone-mac, test.native.lesetilgang | Claude | kode, skjermbilder |
| WP7 | comments-presence | Kommentarer (sidepanel Mac, ark iPhone), «Vis i teksten», «Løs», markering i teksten; `presence` sendt som web (600 ms etter markering, hjerteslag 30 s); andres markør med navn | test.native.kommentar-rundtur | Claude | kode, skjermbilder |
| WP8 | embeds | Bilder (`NSTextAttachment`), diagram/nettverk/tabell tegnet med CellApples eksisterende visualiseringsvisninger; sett inn bilde fra Bilder/Filer (PNG/JPEG ≤ 2 MB); sett inn diagram (samme skjema som web) | test.native.embed-rundtur | Claude | kode |
| WP9 | export | Markdown fra delta (begge), PDF (begge), Word på Mac (`NSAttributedString` officeOpenXML). Systemets delingsark | test.native.eksport | Claude | kode, eksempelfiler i evidence/ |
| WP10 | legacy-kinds | `documentHelp`/`documentChat` natively: liste + tekstfelt + send (`help.ask`/`chat.post`) | test.native.legacy-kinds | Claude | kode, snapshot |
| WP11 | build-and-regression | `SkeletonView`-bryteren får `richdocument`, `documenthelp`, `documentchat`. Fullt bygg: `swift build`/`swift test` CellProtocol, `xcodebuild` CellApple macOS + iOS-simulator, Binding med CellProtocol-grenen og BindingTests. Antall tester før/etter = baseline + nye | test.build, test.regression | Claude via Mac RC | TESTRESULT.md#build, #regression |
| WP12 | gui.parity | Skjermbilder fra ekte Binding (Mac + iPhone-simulator) i de sju tilstandene, side om side med de godkjente bildene | test.gui.parity | Claude via Mac RC (computer use der skjermopptak krever det) | ACCEPT.md#parity |
| WP13 | root | Staging: Mac-Binding, iPhone-simulator og web skriver 2 min i samme dokument; sammenlign med `document.current`; video | test.native.e2e-tre-klienter | Claude via Mac RC; Kjetil svarer på macOS-dialoger for skjermopptak | video, TESTRESULT.md#e2e |
| WP14 | docs, work-is-visible | Book-kapittel om `richDocument`-visualiseringen (web + native, kontrakt, begrensninger), STATUS, ACCEPT bygget fra bevisfilene og kontrollert av en uavhengig tråd, lærdommer | test.docs-updated, test.status-current | Claude | docs-diff, ACCEPT.md |

## Det som krever Kjetil

- G2 (denne planen).
- Merge og tag av CellProtocol-PR-en, og merge av Binding-grenen (Claude merger, tagger og ruller aldri ut).
- Svar på macOS-dialoger for skjermopptak i WP12–WP13.

## Dataflyt (kant → kontrakt)

| Fra | Til | Kontrakt |
|---|---|---|
| Binding editor | RichDocumentCell `document.current` (get) | `haven.document.v1` |
| Binding editor | RichDocumentCell `document.change` (set) | `haven.document.change.v1` → `{status, current}` |
| RichDocumentCell | Binding (Flow) | topic `document.change`, title `document.<kind>` (målt i WP0) |
| Binding | enhetens disk | utkast per `documentId`, aldri sendt noe annet sted |

## Risiko

- `UITextView`/`NSTextView` gir tekstendringer som områder, ikke som delta. WP2/WP3 må lage delta fra (område, ny tekst, attributter) presist i UTF-16; fixture-korpuset fra WP1 er vernet.
- Om Flow ikke når Binding, blir live-oppdatering 2 s henting. Målet på 3 s holder fortsatt.
- Store dokumenter (cellen tillater 100 000 tegn): mål innlasting og skriving i et dokument på 50 000 tegn i WP11.
