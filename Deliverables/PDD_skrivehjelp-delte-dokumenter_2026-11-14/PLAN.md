# PLAN — skrivehjelp i delte dokumenter

Status: G2 godkjent 2026-11-18 med krav om paritet med Binding (WP6b). G1 godkjent 2026-11-15. G1-GUI bedt om på bildene v2.
Utgangspunkt: CellScaffold `9612217` (origin/main 15.11), CellProtocol `14fd9dc`.
Arbeidet gjøres på en egen gren fra origin/main i CellScaffold, aldri i hovedcheckouten på Mac-en (`/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold` står på en Codex-gren med ukommitterte endringer).

## Hvordan det henger sammen

```
Student (web eller Binding)
  │  document.assist.ask {mode, passageId|selection, question}
  ▼
RichDocumentCell  ── sjekker Agreement-grant «assist», modellhjelp på, teksten finnes
  │  (utenfor mutasjonslåsen)
  ▼
cell:///AIGateway (state.draft til den som spør) → ChatAIGatewayRequest → PurposeBoundAIGateway
  │  svar: ren tekst, lengdegrense
  ▼
RichDocumentCell  ── lagrer rad i assist-loggen (hendelse + document.change-Flow), alle ser den
  │  document.assist.apply {entryId}
  ▼
vanlig delta med den som trykket som forfatter, bare hvis teksten står uendret nøyaktig én gang
```

Mønsteret er kopiert fra `PublicationPortfolioCell.pageAssistant` (CellScaffold `Sources/App/Cells/Publication/PublicationPortfolioCell.swift:230–300`): forespørselen bygges fra rutevalget til den som spør, tilgang og tekst sjekkes før og etter kallet, og et forslag lagres aldri automatisk.

## Arbeidspakker

| WP | purposeRef | Hva | Utfører | Tester som skal bli grønne | Leverer til §3 |
|---|---|---|---|---|---|
| WP0 | purpose://quality.build-and-regression | Baseline: CI på en tom gren fra origin/main; noter antall tester og røde | Claude (gren + CI) | test.build, test.regression (før) | TESTRESULT.md#baseline |
| WP1 | …consent, …access | Modellhjelp per dokument: `assistEnabled` i dokumenttilstanden, `assist.enable` bare for eier, hendelse alle ser. Nye grants i `configureGrants()`: `assist` (rw), `assistPanel` (r). Deltakere får dem bare gjennom dokumentets Agreement | Claude | test.skrivehjelp.av-som-standard, test.cell.auth-negative (feil requester, mangler grant, leser uten skriv) | #6 |
| WP2 | …ask, …route | `document.assist.ask`: bygg forespørsel fra AIGateway-draften til den som spør, send bare spørsmål + valgt tekst, kall `PurposeBoundAIGateway` utenfor mutasjonslåsen, én forespørsel om gangen per person. `noRoute` gir varsel uten kall. Modus `guide` bruker dagens `RichDocumentGuide` | Claude | test.skrivehjelp.bare-markert-tekst-sendes, test.skrivehjelp.rute-er-spørrerens, test.skrivehjelp.ingen-rute | #6 |
| WP3 | …untrusted-output | Svarparser som i `PublicationPageAssistant.parse`: JSON med `explanation` og ev. `text`, maks lengde, ingen `<`/`>`, ingen andre nøkler | Claude | test.skrivehjelp.svar-er-ren-tekst | #6 |
| WP4 | …shared-log | Assist-loggen i dokumenttilstanden (maks 1000 rader, som `help`): spørrer, leverandør, modell, revisjon, valgt tekst, svar, tilstand. Lagres med samme persistens og Flow som andre hendelser | Claude | test.skrivehjelp.logg-deles, test.skrivehjelp.innsyn | #1, #6 |
| WP5 | …apply | `document.assist.apply` / `dismiss` / `retry`: delta bare hvis teksten finnes nøyaktig én gang i nåværende dokument, ellers `stale` uten endring | Claude | test.skrivehjelp.bruk-forslag, test.skrivehjelp.foreldet-forslag | #1, #3 |
| WP6 | …swift-native, purpose://gui.ways-in-are-reachable | `document.assistPanel` (per person: rutelinje, varsler, avsnitt, valgt tekst, utkast, rader) og skrivehjelp-panelet fra `skeleton/skrivehjelp-panel.v1.json` inn i `RichDocumentCell.configuration()`, i stedet for `documentHelp`. Web: markering i editoren sendes som `selectPassage`. Migrering av lagrede Dokument-skjeletter med eksakt digest (som #416) | Claude | test.skeleton.no-unreachable-elements, test.skeleton.purpose-actions-reachable, playwright `rich-document.spec.js` + ny `rich-document-assist.spec.js` | #1–#3 |
| WP6b | …swift-native | Paritet med Binding (Kjetil 18.11): dokumentchat (meldinger + skriv + send) og dokumentteksten som lesevisning (avsnitt som tekst) av vanlige skeleton-elementer fra `document.assistPanel`/`document.chatPanel`. Web beholder Quill-editoren; Binding får alt unntatt redigering i editoren | Claude | test.gui.parity (Binding), `rich-document-assist.spec.js` | #1–#4 |
| WP7 | …swift-native | Binding: screenshot av panelet mot en lokal CellScaffold eller staging, via Remote Control på Mac-en | Claude via Remote Control (Kjetils Mac) | test.gui.parity (Binding) | #4 |
| WP8 | purpose://quality.docs-in-same-change | Oppdater `RichDocumentGuide` (fjern «Ingen automatisk AI-tekstgenerering» der det ikke lenger stemmer), Explore-beskrivelser og `Documentation/` | Claude | test.docs-updated | ACCEPT.md#docs |
| WP9 | root | FORESPOERSEL til Deploy etter grønn CI og Mac-bygg; e2e mot staging med to studentkontoer når deling (egen tråd) og modellrute finnes | Claude skriver forespørselen; Deploy/Kjetil kjører toget | test.skrivehjelp.e2e-to-studenter, test.gui.load-time | #5 |

## Rekkefølge og avhengigheter

- WP0 → WP1 → WP2/WP3 → WP4 → WP5 → WP6 → WP8 i én PR i CellScaffold. WP7 når PR-en bygger.
- WP9 venter på to ting utenfor denne PDD-en:
  1. Deling mellom studenter (tråden «La studenter dele dokumenter med hverandre»). Fram til da testes to deltakere med Agreement i Swift-tester, slik `testCellGetSetSharingDenialAndRestore` gjør.
  2. En modellrute studentene har. Fram til Kjetil bestemmer operatørmodell, bruker testene en test-invoker, og staging-testen bruker en testkonto med egen nøkkel som Kjetil gir.
- Ingen endring i CellProtocol. Panelet bruker bare elementer CellApple allerede tegner.

## Hvordan det bygges og testes

- Skycontaineren har ingen Swift. Swift-bygg og tester kjøres av CI på PR-en (`ci/run-tests.sh`, `ci/test-filter.txt` har allerede `RichDocumentCellTests`), og på Mac-en via Remote Control før noe går til Deploy (regelen fra 12.11: ingenting i køen før bygget er verifisert).
- Web-panelet testes med Playwright i skycontaineren (samme oppsett som bildene).
- Tester på cellen bruker en injisert invoker, som `assistantInvoker` i Publisering, så ingen betalte kall skjer i CI.
- Risiko i WP6: Porthole-web legger svaret fra en handling inn i flatetilstanden etter etikett (`applyActionResultState` i `Public/js/porthole-webo.js`). #441 måtte gi «publication» egen behandling fordi svaret ellers ble lagret feil. Svarene fra `document.assist.*` skal derfor returnere hele `assistPanel`, og Playwright-testen skal kjøre gjennom `porthole-webo.js`, ikke bare `skeleton-runtime.js`.
- `ValueType`-objekter sammenlignes som sortert JSON (lesson.valuetype-equality-false-for-objects).

## Dataflyt (kant → kontrakt)

| Kant | Kontrakt |
|---|---|
| Flate → `document.assist.ask` | ny Explore-kontrakt i `RichDocumentSchemas` (`assistCommand`) |
| RichDocumentCell → `cell:///AIGateway` `state` | eksisterende, leses som i `PublicationPageAssistant.configured` |
| RichDocumentCell → `cell:///PurposeBoundAIGateway` `ai.invokePurposeBound` | eksisterende `AIGatewayPurposePolicy` v1.1.0 |
| RichDocumentCell → Flow `document.change` | eksisterende, ny `kind` `assist.*` |
| Flate ← `document.assistPanel` | ny Explore-kontrakt (`assistPanel`) |

## Ikke med i denne planen

- Full native dokumenteditor og dokumentchat i Binding (egen tråd ved behov). Dokumentchatten er også bare web i dag; samme grep som panelet (vanlige skeleton-elementer) kan gi chat i Binding som en liten ekstra arbeidspakke hvis du vil.
- Operatørbetalt modell for studenter.
- Deling av dokumenter og flere dokumenter per student.
