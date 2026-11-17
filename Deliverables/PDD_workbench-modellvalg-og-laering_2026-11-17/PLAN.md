# PLAN — modellvalg og læring i AI-hjelperen, fase 1

2026-11-17. Bygger på G1 (13:34Z) og G1-GUI (22:10Z). Kode: CellScaffold `origin/main` cfa0e74. Fase 2 (Sara og generell HAVEN-hjelp) er ikke med; grenen `haven-help.*` venter på Kjetils ord.

## Dette skal du gjøre

| Når | Hva | Hvorfor |
|---|---|---|
| Nå | Si «G2 godkjent», eller hva som skal endres. Svar gjerne på de to spørsmålene nederst. | Uten det bygger jeg ikke. |
| Når PR-en er grønn | Merge PR-en i CellScaffold, og la deploy-køen legge den på staging. | Jeg når ikke staging fra skyen. |
| Før første test | Sjekk at staging har `HAVEN_CREDENTIAL_MASTER_KEY`. Uten den sier flaten «Nøkkellageret er ikke satt opp på denne serveren». | Nøkkelen kan ikke forsegles uten. |
| På staging | Åpne Developer Workbench › hjelper › Mine modeller. Velg Anthropic, lim inn nøkkelen, trykk «Lagre og test». | Jeg skal aldri se nøkkelen. |
| Rett etterpå | Skriv «Flytt de som handler om innlogging til triage» i panelet i intake, og send meg et skjermbilde av svaret. | Det er T-A1 og T-A2. |

## Hvem gjør hva, i rekkefølge

| Steg | Kjetil | Losen i skyen | CI | Codex/Xcode på Macen |
|---|---|---|---|---|
| 1 | G2 | | | |
| 2 | | WP1–WP7, én PR | bygg og tester | |
| 3 | merge, deploy | | | |
| 4 | nøkkel inn, to prøver (WP8) | | | |
| 5 | | TESTRESULT, ACCEPT | | WP9 paritet i Binding |
| 6 | G3 | lærdommer (P6) | | |

## Arbeidspakker

| WP | purposeRef | Hva | Tester | Utfører |
|---|---|---|---|---|
| WP0 | quality.build-and-regression | Baseline: CI på main før endring, antall bolker og tester noteres. | test.build, test.regression | Losen (leser CI) |
| WP1 | mine-modeller | `ButlerProviderConfigurationStore` får én felles instans. WorkbenchHelperCell får `models.state`, `models.setDraftProvider`, `models.setDraftModel`, `models.setDraftTitle`, `models.add` (payload er nøkkelen fra det skjulte feltet; oppsett, engangstillatelse og forsegling skjer i ett kall), `models.replaceKey`, `models.remove`, `models.test`. Nøkkelen finnes aldri i `state`, i svar, i logg eller i læringen. | T-M1, test.cell.auth-negative | Losen |
| WP2 | velg | `models.use {configID}` lagrer aktiv modell hos eieren. `askModel` bygger ruten fra oppsettet og kaller AIGateway med eierens forseglede nøkkel (`invokeWithHostedKey`). Uten aktiv modell brukes ingen standardrute fra miljøet. | T-V1 | Losen |
| WP3 | si-fra | Egne meldinger for: ingen modell, nøkkel mangler, 401, 429/tom kreditt, ingen kontakt, nøkkellageret ikke satt opp. Hver sier hvor det rettes. | T-S1 | Losen |
| WP4 | mine-modeller, velg | Skjelettet: `Picker` for modell i hjelperpanelet på alle arbeidsfaner; seksjonene «Mine modeller» (liste, skjema med `secure: true`) og «Læring» i fanen hjelper. | T-M2 (skjelettdelen), test.skeleton.*, test.gui.reference-image-exists | Losen |
| WP5 | laer, data.manner | Hvert modellkall og hvert regeltreff gir ett eksempel hos eieren: bestilling, sett, modell, svar, handlingen hjelperen landet på, utfall. Utfør, Forkast og Angre oppdaterer utfallet. Bryter, «Slett» per rad og «Slett alt». Tak: 500 eksempler, eldste ut. | T-L1, T-P1 | Losen |
| WP6 | tren-formaalsanalysen | «Eksporter testsett» gir JSON med fasit og moteksempler. «Legg ordene i et utkast» ber den aktive modellen foreslå ordlinjer og legger dem i utkastet til settet; eieren lagrer selv. Treffraten måles med `PurposeQualityMonitor` (`quality.compareChatPrompts`) før og etter. Formatet leses fra cellen før eksporten skrives. | T-L2, T-L3 | Losen; T-L3 kjøres på staging-data fra Kjetil |
| WP7 | quality.docs-in-same-change, cell.contract-explicit, cells.dataflow-declared | `contract/` (tilstand, eksempel, testsett), `dataflow.md`, oppdatert `Documentation/Operations/Developer_Workbench_AI_Hjelper_*.md`. | test.docs-updated, test.cell.contract-fixtures, test.cells.dataflow-matches-contracts | Losen |
| WP8 | anthropic-forst, root | Staging: nøkkel inn, «Test», én bestilling reglene ikke forstår, tidtaking av «legg til» og lastetid tre ganger. | T-A1, T-A2, T-M2 (tiden), T-R1, test.gui.load-time, test.gui.parity | Kjetil; Losen skriver TESTRESULT fra skjermbildene |
| WP9 | gui.parity | Binding: modellvelger og skjult nøkkelfelt rendres og virker. | test.gui.parity (Binding) | Codex/Xcode |

## Dataflyt (kanter)

| Fra | Til | Keypath / kall |
|---|---|---|
| Skjelett (hjelperpanel, hjelper-fane) | `cell:///WorkbenchHelper` | `models.*`, `learning.*`, `helper.ask` |
| WorkbenchHelperCell | BYOK-lageret | `create`, `issueKeyInput`, `writeKey`, `secret`, `remove` |
| BYOK-lageret | `OwnerScopedCredentialStore` | forseglet nøkkel under reservert alias |
| WorkbenchHelperCell | `cell:///AIGateway` | `invokeWithHostedKey(rute fra oppsettet, eierens nøkkel)` |
| AIGateway | leverandøren | HTTPS, bare verter i egress-listen |
| WorkbenchHelperCell | `cell:///PurposeQualityMonitor` | `quality.compareChatPrompts` (T-L3) |

## Stoppregler

- Jeg endrer ingen eksisterende, committet test uten å spørre deg først.
- Rød CI rettes og pushes på nytt, slik som sist. Er feilen utenfor denne endringen, sier jeg fra og venter.
- Jeg rører ikke egress-listen, `ButlerDisclosurePolicy` eller Butler-chatten uten ditt ord.
- Jeg merger ikke.

## Det som ikke blir som på bildene

Står i `images/README.md`: seksjoner under hverandre i stedet for venstremeny, bryteren blir en knapp, fargeprikken blir tekst, og «Slett valgte» kan bli «Slett» per rad.

## To spørsmål

1. **nanoGPT.** AIGateway slipper bare ut til OpenAI, Anthropic, Mistral og lokale modeller. nanoGPT-nøkkelen din kan derfor ikke brukes i «Mine modeller» uten en ny linje i egress-listen. Anbefalt: ikke nå; egen liten endring etter at Anthropic virker.
2. **Regeltreff som læring.** Anbefalt: ja, også bestillinger reglene forstår uten modell blir eksempler, fordi de er fasit for formålsmatchingen.

Svarer du bare «G2 godkjent», gjelder anbefalingene.
