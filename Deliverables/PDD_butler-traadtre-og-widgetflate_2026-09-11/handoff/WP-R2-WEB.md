# WP-R2b — Web-rendereren, gjenopptatt
STATUS: DELVIS — commit 943a3bce6ff8bbaa9a0e3884fecf78915fd1e8c5 på pdd/skjelett-elementer-web — mangler: ComponentSurface-kildehandlinger i Porthole, T-F3-nettleserbevis

**Forbehold:** Tree, komponentvisning og modifikatorene er implementert i grenen,
men T-F3 er ikke grønn.
Playwright er kjørt: alle 10 tester stopper ved Chromium-start, før testinnholdet
kjøres. Ingen nettleserinteraksjon, beregnet CSS, skjermbilde eller native paritet
påstås verifisert. Kildehandlingsruten er et separat, kjent verts-/transportgap.

Dato: 2026-09-19. Utfører: Astra (Codex).

## Port og eksakt arbeidsgrunnlag

Første utførte kontroll var `awk '/^STATUS:/{print; exit}'` på
`handoff/WP-R1-FORMAT.md`. Linjen var:

```text
STATUS: LEVERT — commit d224a4ed2b6b6b384dff4b8942978bae9f56ade0 på pdd/skjelett-elementer — T-F1/T-F2 grønne
```

R1-worktree-ens HEAD var og er denne SHA-en. T-F1/T-F2-statusen kommer fra R1s
rapport; disse Swift-testene er ikke kjørt på nytt av WP-R2b. Kontrakten lest er
**SKJELETT_ELEMENTER.md iterasjon 6, inkludert hele §2.2**, og hele den opprinnelige
`_losen-queue/done/wp-r2-web-20260919.prompt.md`.

Ny CellScaffold-worktree: `/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919`.
Grenen ble opprettet fra lokalt tilgjengelig `origin/main` ved **e3ae9fc0526e3582128a0ae88ab2d93d5bd5f2d8**.
Ingen fetch, push, PR eller deploy er utført. Arbeidet bruker R1-SHA-ens
JSON-format og byte-identiske kopier av de tre fixturene; SHA-256 står i
[summary.json](../evidence/wp-r2-web/summary.json). Fellesfasiten ble også
sammenlignet direkte med `git show d224a4ed2b6b6b384dff4b8942978bae9f56ade0:fixtures/skeleton-wp-r1/<fil>`.

Bare JavaScript/CSS og lokale tester/fixtures er endret. Swift-dekoderen er ikke
endret eller bygget. En senere Swift-testvert må bruke
`CELLPROTOCOL_LOCAL_PACKAGE_PATH=/Users/kjetil/Build/Digipomps/HAVEN/CellProtocol/_wt-skjellettelementer-wp-r1-20260918`
og kontrollere at HEAD fortsatt er `d224a4ed2b6b6b384dff4b8942978bae9f56ade0`.

## Per element — bygget, kilder og testutfall

**N = Node-kontrakt-/logikktest kjørt og bestått. B = Playwright-test skrevet og
kjøringsforsøkt, men blokkert ved nettleserstart. B er ikke et funksjonspass.**
Alle lenkene peker til den nye worktree-en. Native-kolonnen er **ikke kjørt** for
samtlige rader; tabellen dokumenterer webkandidaten, ikke oppnådd C1-paritet.

| Element | Bygget | Fil/linje og atferd | Tester skrevet og kjørt — utfall |
|---|---|---|---|
| Tree | Ja | [runtime:882](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:882), [runtime:975](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:975). Eget radskall, cellelevert synlig rekkefølge, roving fokus ved ID, alle avtalte taster, selection/expansion adskilt, bekreftet tilstand, forelderfokus ved lukking, scroll-til-fokus, ARIA-nivå fra data. Validator kjenner casen. | [katalog:174](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:174), [katalog:254](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:254): B. [Node:79](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:79): N for eksakte payloads og uendret celletilstand; validering også N. |
| ComponentSurface visning/binding | Ja | [runtime:1029](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:1029), [runtime:1051](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:1051). Oppløst mount, item før root uten omskriving, cache ved instanceID, ny revisjon remonterer definisjonen; feltutkast/fokus/scroll gjenopprettes for gjenfunnede felt/elementer. | [katalog:269](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:269), [katalog:294](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:294): B. [Node:51](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:51): N mot delt fasit; dette er ikke DOM-identitetsbevis. |
| ComponentSurface kildehandlinger | Delvis: renderer ja, Porthole-transport nei | [runtime:1046](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:1046). Callback får original payload og separate `sourceCellEndpoint`/`mount`. [webvert:8854](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/porthole-webo.js:8854) avviser eksplisitt i dagens vert. | [Node:69](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:69), [Node:176](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:176): N. Fixture-knappeklikk: B. Ingen faktisk kildecelle/Agreement-utveksling kjørt. |
| ComponentSurface kortpreview | Ja | [runtime:6149](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:6149). Klonet komponentkort, inert og uten ekstra tilgjengelige handlinger i preview. | [katalog:404](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:404): B; dragbildet er ikke visuelt verifisert. |
| M1 paddingInsets | Ja | [runtime:4956](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:4956). Logiske kanter, eksplisitt null overstyrer padding; utelatt kant faller tilbake til uniform padding/0. | [Node:134](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:134): N. [katalog:363](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:363): B. |
| M2 typografi | Ja | [runtime:4961](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:4961). Ordnet fontliste med vertsfont som fallback, lineHeightMultiple, signert letterSpacing, proportional/tabular → font-variant-numeric. | [Node:134](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:134): N for oversettelsen. [katalog:363](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:363): B for beregnet CSS. |
| M3 listerader | Ja | [runtime:4961](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:4961), [runtime:7237](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:7237). itemSpacing, rowInsets og rowDecoration:none. Endrer ikke listescrolling/tomtilstand. | [katalog:363](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:363): B; ingen faktisk CSS-verifikasjon av M3. |
| M4 størrelser/flex | Ja | [runtime:4961](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:4961). minHeight/maxHeight/minWidth/flexGrow, inklusive null. | [Node:134](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:134): N for felttolkning. [katalog:363](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:363): B. |
| M5 controlStyle/accessibilityLabel | Ja | [runtime:4961](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:4961), generisk CSS i [CSS:6010](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/css/porthole-webo.css:6010). Plain dekorasjon og tilgjengelig navn på kontroller; eksplisitt knappnavn beholdes over label-binding. | [Node:134](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:134): N for attributtoversettelse. [katalog:363](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:363): B for tilgjengelig knapp og klikk. |
| M6 kanter/skygge/klipp | Ja | [runtime:5183](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:5183), [runtime:4961](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:4961). borderStyle, logiske borderEdges, signert shadowSpread, faktisk overflow-klipp med cornerRadius. | [Node:134](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:134): N for stiloversettelse. [katalog:363](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:363): B for CSS og hit-test utenfor klippet. |
| M7/V3-A layoutVariants | Ja | [runtime:5002](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:5002), [runtime:5019](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:5019), [runtime:5044](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:5044); vertsdeklarasjon i [webvert:8342](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/porthole-webo.js:8342). Første treff, inklusive grenser, ukjent størrelse matcher ikke terskler, alle kapabiliteter må finnes. Grid/faste paneler snevrer inn. Samme DOM brukes ved variantskifte. | [Node:93](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:93), [Node:104](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:104), [Node:128](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:128): N, inklusive 236px kolonne på 1200px flate. [katalog:320](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:320), [katalog:351](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:351): B for DOM/fokus/utkast og ingen doble tilgjengelige handlinger. |
| M8 + R4 | Ja, samlet | [runtime:5116](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:5116), [runtime:5146](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:5146), [runtime:5153](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:5153), [runtime:5963](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:5963). Felles kortlivet vertskontekst, alle aksepterende flater markeres fra dragstart, ryddes ved drop/cancel. dragSource vinner per egenskap over dragActive. hover/focusVisible støttes. | [Node:161](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:161): N for prioritet og tilbakeføring. [katalog:404](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:404), [katalog:445](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:445): B for faktiske muse-/tastatur-/drop-interaksjoner. |
| M9 tekstdekorasjon/rotasjon | Ja | [runtime:4961](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:4961). textDecoration og textRotationDegrees; utsatt textTransform er ikke innført. | [Node:134](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:134): N. [katalog:363](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:363): B. |
| M10 leadingMarker | Ja | [runtime:4961](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:4961), [CSS:6012](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/css/porthole-webo.css:6012). Pseudoelement ved logisk leading med eksplisitt geometri, uten layout-/hitflate. | [Node:134](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:134): N for verdier. [katalog:363](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:363): B for pseudoelementets geometri. |
| R1 fontWeight | Ja på web | [runtime:4949](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:4949). ultralight/thin/light/regular/medium/semibold/bold/heavy/black svarer til 100…900; ukjent → 400. | [Node:152](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/skeleton-wp-r2-contract.test.js:152): N for alle ni par. [katalog:363](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:363): B. Native-likhet krever WP-R3; den gamle native numeriske tolkningen på formatgrenen er ikke rettet her. |
| R7 firstTextBaseline | Ja på web | [runtime:5166](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:5166). Horisontal stack bruker first baseline for kryssaksen. | [katalog:363](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:363): B; ingen grønn nettleser-/native-baselinemåling. |
| R8 nullkant / spread uten blur | Ja | [runtime:5183](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Public/js/skeleton-runtime.js:5183). borderWidth ≥ 0 anvendes, og shadowSpread gir skygge også ved shadowRadius:0. | [katalog:363](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/playwright/skeleton-element-catalog.spec.js:363): B. Testen kontrollerer også borderWidth:0 på en plattformknapp uten controlStyle:plain. |

## Eksakte kjøringer og bevis

Arbeidsmappe er den nye worktree-en med mindre annet er angitt.

| Kommando | Utfall |
|---|---|
| `node --check Public/js/skeleton-runtime.js` | Kjørt, exit 0. |
| `node --check Public/js/porthole-webo.js` | Kjørt, exit 0. |
| `node --check playwright/skeleton-element-catalog.spec.js` | Kjørt, exit 0. |
| `node --check scripts/skeleton-wp-r2-contract.test.js` | Kjørt, exit 0. |
| `git diff --check` og `git diff --cached --check` | Kjørt før commit, exit 0. |
| `node --test scripts/skeleton-wp-r2-contract.test.js` | **11/11 bestått**, exit 0. [Logg](../evidence/wp-r2-web/node-contract.log). |
| `node --test scripts/skeleton-wp-r2-contract.test.js scripts/porthole-arendalsuka-action-state.test.js` | **20/21 bestått**, exit 1. Én eksisterende testfeil, se nedenfor. [Logg](../evidence/wp-r2-web/node-contract-and-regression.log). |
| `./node_modules/.bin/playwright test --config=playwright.config.js playwright/skeleton-element-catalog.spec.js --list` | Kjørt, exit 0; 10 tester funnet (1 eksisterende + 9 nye). Dette kjører ikke testene. |
| `./node_modules/.bin/playwright test --config=playwright.config.js playwright/skeleton-element-catalog.spec.js` | **Kjørt, exit 1: 0 bestått, 10 feilet ved browser launch.** [Full logg](../evidence/wp-r2-web/playwright-catalog.log), [representativ launch-trace](../evidence/wp-r2-web/chromium-launch-trace.zip). |

Den konkrete Playwright-blokkeringen er:

```text
FATAL:base/apple/mach_port_rendezvous_mac.cc:158
bootstrap_check_in org.chromium.Chromium.MachPortRendezvousServer.<pid>: Permission denied (1100)
```

Chromium Headless Shell 1193 finnes lokalt, men denne macOS-sandkassen tillater
ikke oppstarten. Ingen test-body fikk kjøre. Ingen omgåelse av sandkassen er
forsøkt, og ingen screenshots/pikselbevis er produsert.

Node-regresjonen heter `refresh, websocket, and heartbeat shell renders keep
hostChanged at zero` (`scripts/porthole-arendalsuka-action-state.test.js:359`).
Den feiler med `document.createElement is not a function` i testharnessen.
Samme test og feil er gjenskapt med uendret baseversjon av `porthole-webo.js`:

```sh
# Fra CellScaffold-worktree-en:
mkdir -p /private/tmp/wp-r2-main-baseline/Public/js
git show origin/main:Public/js/porthole-webo.js > /private/tmp/wp-r2-main-baseline/Public/js/porthole-webo.js
# Arbeidsmappe /private/tmp/wp-r2-main-baseline:
node --test /Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/scripts/porthole-arendalsuka-action-state.test.js
```

Baseutfall: **9/10 bestått, samme ene feil**, exit 1.
[Baselinelogg](../evidence/wp-r2-web/node-main-baseline.log). Den eksisterende
regresjonstesten er ikke endret for å skjule feilen.

## Gjenstående gap og avgrensninger

1. **Kildehandlinger i ComponentSurface:** Web har keypath-ruting via deklarerte
   cellereferanser, så funnet er ikke at ingen handling kan nå en annen celle.
   Det presise gapet er at
   [PortholeActionRequest](/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Sources/App/Controllers/PortholeWebSessionSupport.swift:10)
   bare bærer `keypath/payload/command/args`, uten mount-kontraktens kilde-endepunkt
   og separate monteringsmetadata. Dagens fallback skriver til controlCell
   (/Users/kjetil/Build/Digipomps/HAVEN/CellScaffold/_wt-skjellettelementer-web-20260919/Sources/App/Controllers/PortholeWebSessionSupport.swift:3454).
   Rendereradapteren er klar; Porthole avviser disse handlingene med synlig
   melding før feil ruting kan skje. Backend-ruting og vanlig Agreement-flyt
   må leveres og integrasjonstestes før dette kan markeres levert.
2. **T-F3 må kjøres i et miljø hvor Chromium får starte.** Katalogspeccen serverer
   kun grenens lokale runtime/CSS og fixturedata; staging trengs ikke. Kjør samme
   kommando fra tabellen, og rett eventuelle faktiske browserfeil før grønn status.
   Node-testene bruker VM/stilobjekter og erstatter ikke dette.
3. **V3-A-grensen er beholdt:** udeklarerte containere arver størrelsen. Det er
   ingen måling per skjelettelement og ingen viewportClass. Porthole har én
   ResizeObserver for vertsgrensen (rot og forelder). Vilkårlige CSS-overstyrte
   størrelser blir ikke automatisk en ny portabel layoutkontekst.
4. Tree viser cellens bekreftede liste også mens en utbrettingshandling venter.
   Egen loading/error-datamodell er fortsatt ikke definert i formatet; ingen ny
   slik kontrakt er oppfunnet. R3-abonnement/persistens, native R6 og R5 fullflate
   er ikke implementert i denne webpakken.

Swift-bygg, native tester, T-P1/T-P2, staging og produksjon er ikke kjørt.
Ingen komplett funksjons- eller paritetsgodkjenning gis.

## Git og overlevering

Kodecommiten er **943a3bce6ff8bbaa9a0e3884fecf78915fd1e8c5**, på forespurt gren. Den nye worktree-en er ren etter
commit. Eksisterende endringer i hovedarbeidstrærne er ikke rørt.
Denne rapporten og `evidence/wp-r2-web/` er skrevet i den eksisterende, urene
CellProtocolDocuments-worktree-en og er **ikke committet** der; ingen øvrige
dokumentendringer er staged eller tatt med. Ingen push, PR eller deploy.
