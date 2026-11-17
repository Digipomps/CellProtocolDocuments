# Oppdrag til Codex: spillverksted, fase 2, første runde

Fra Claude, 2026-10-09, etter G2 i `PDD_spillverksted_2026-10-09` (godkjent 14:12Z).

- Plan: `../PLAN.md`
- Formål: `../FORMAALSSPEC.md` §1
- Tester: `../FORMAALSSPEC.md` §5

## Grunnlag

- **Repo:** CellScaffold (`github.com/Digipomps/CellScaffold`). Claudes del er merget til `main` (PR #306, 2026-10-09).
- **Worktree:** `/Users/kjetil/Build/Digipomps/HAVEN/tmp/codex-spillverksted-r1`, gren `codex/spillverksted-runde1` fra `origin/main`. Jobb bare der, ikke i hovedsjekkouten.
- **Relative stier** i dette dokumentet (`../PLAN.md` osv.) er relative til denne mappa: `/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_spillverksted_2026-10-09/handoff/`.
- **Godkjent:** G1, G1-GUI og G2 (Kjetil, 2026-10-09). Formålene i treet er godkjent som Book 23-forslag 17:27Z.
- **Allerede gjort av Claude** (JS og verktøy, ingen Swift):
  - `Visualization` `gamePreview` i `Public/js/skeleton-runtime.js`, med `playwright/game-preview-visualization.spec.js`
  - KAPLAY 3001.0.19 i `Public/vendor/kaplay/3001.0.19/`
  - `Tools/GameToolLibrary/` med `game-tool-library.v1.json` (20 oppføringer, 23 formål)
  - Kontrakten for `gamePreview` står i `Documentation/Spillverksted/README.md`.
- **Mal for en ny celle:** `Sources/App/Cells/Purpose/PurposeReviewCell.swift` (nylig, med Explore-skjema og intercepts).
- **Registrering:** `Sources/App/configure.swift`, `addCellResolveIfNeeded(name:cellScope:persistency:type:)`, som linje 1283 for `ProjectPortfolio`.
- **Ruter:** `Sources/App/routes.swift` rundt linje 274 (`app.register(collection:)`). Mal for en offentlig rute: `Sources/App/Controllers/VaporPublication.swift`.

## Regler (fra `AGENTS.md`)

- **Bygg og test:**
  - Bygg og test bare med `scripts/run_swift_bounded.sh build|test …` eller `scripts/run_tests_isolated.sh …`.
  - Ingen `swift build` direkte. Ingen egen `--scratch-path`.
- **Før push:**
  - Kjør `ci/check-value-literals.sh` før push.
  - Høyst 20 oppføringer per `.object([...])`/`.list([...])`. Større objekter bygges med `Object.build { $0["k"] = … }`.
- **Package.resolved:** Commit aldri drift i `Package.resolved` fra lokale pakkeoverstyringer.
- **ValueType i tester:** Tester som sammenligner `ValueType` `.object`/`.list`, sammenligner JSON med sorterte nøkler, ikke med `XCTAssertEqual` på verdiene.
- **Formålsref:** Hver endring nevner formålsrefen sin i commit-meldingen.

## Oppdrag

Rekkefølgen er avhengighetsrekkefølgen. Hvert oppdrag er ferdig når testen er grønn og utdata ligger i `../TESTRESULT.md` under ankeret.

### WP-E2: `GameProjectCell`, versjoner

**Formål:** `purpose://candidate.game-workshop.project.versioned-changes`

- **Celle:** `cell:///GameProject`, `identityUnique`, persistent.
- **Tilstand:** Et prosjekt har `id`, `title`, `engine` (`kaplay`), `versions` (liste av `{ n, title, code, createdAt, lib: [entryId] }`), `current` (n) og `pending` (forslag som ikke er lagret, eller null).
- **Handlinger (set-intercepts):**
  - `project.create { title, templateId? }`
  - `project.propose { title, changes, why, usedLibrary, code }` setter `pending`.
  - `project.applyProposal` gjør `pending` til en ny versjon.
  - `project.discardProposal`
  - `project.revert { n }` lager en ny versjon med koden fra n, så historikken bevares.
- **Lesing (get-keypaths):** `project.preview` → `{ url, label }` for `gamePreview`. Den viser `pending` hvis det finnes, ellers `current`.
- **Grenser:** Koden lagres som tekst, og cellen kjører den aldri. Høyst 200 kB per versjon.
- **Test (T-E2):** ti endringer, `revert { n: 3 }`, koden i siste versjon er lik versjon 3, og antall versjoner er 11.
- **Bevis:** `TESTRESULT.md#versjoner`

### WP-D2: sandkasseruten

**Formål:** `purpose://candidate.game-workshop.engine.sandbox-isolation`

- **Rute:** `GET /spill/sandbox/:project/:version` (`:version` er et tall eller `pending`). Den returnerer et HTML-dokument med:
  - `<script src="/vendor/kaplay/3001.0.19/kaplay.js">`
  - en liten feilrapportør
  - spillets kode inline
- Feilrapportøren poster `{type:"error", message, line}` ved `window.onerror`, `unhandledrejection` og `console.error`, og `{type:"ok"}` etter 1,2 sekunder uten feil. Linjenummer regnes relativt til spillkoden. Se `buildFrame`/`HEAD` i prototypen: `../prototype/spillverksted-prototype.html`.
- **Hoder:**
  - `Content-Security-Policy: sandbox allow-scripts; default-src 'none'; script-src 'self' 'unsafe-inline'; img-src data: blob:; style-src 'unsafe-inline'; connect-src 'none'; media-src data: blob:`
  - `X-Content-Type-Options: nosniff`
  - `Referrer-Policy: no-referrer`
  - Ingen `Set-Cookie`.
- **Tilgang:** Ruten leser koden fra `GameProjectCell` som eieren av prosjektet. I fase 2 er bare eieren av scaffoldet og identiteter eieren har gitt tilgang til prosjektet, med. Ukjent prosjekt eller versjon gir 404 uten detaljer.
- **Test (T-D2):** en Playwright-spec med et «ondsinnet» spill som prøver `parent.document.cookie`, `document.cookie`, `localStorage`, `fetch('/api/…')` og `top.location`. Alt skal feile, og `self.origin` skal være `"null"`. Mønster: `playwright/game-preview-visualization.spec.js`, testen «the game cannot read the session…». Pluss en Swift-test av hodene.
- **Bevis:** `TESTRESULT.md#sandkasse`

### WP-E1: prosjektet i Workbench

**Formål:** `purpose://candidate.game-workshop.project.uses-haven-workbench`

- Et spillprosjekt er et prosjekt i `ProjectPortfolio`. Oppgavene er `WorkItem`-poster (`Sources/App/Cells/WorkItems/`), og `GameProjectCell` lenker til prosjekt-id-en.
- Ingen ny prosjektmodell.
- **Test (T-E1):** inspeksjon. Opprett et spillprosjekt og vis at det står i porteføljen med to oppgaver.
- **Bevis:** `ACCEPT.md#prosjekt`

### WP-C2: `GameToolLibraryCell`, oppslag

**Formål:** `purpose://candidate.tool-library.purpose-first-lookup`

- **Celle:** `cell:///GameToolLibrary`. Den leser `Tools/GameToolLibrary/game-tool-library.v1.json` fra ressursene ved oppstart, og filen kopieres inn i bundle som andre JSON-ressurser.
- **`library.lookup { purposeRef?, text? }`** returnerer oppføringer:
  1. først de med nøyaktig `purposeRef`
  2. så de med en `purposeRef` under samme forelder
  3. til slutt ordtreff i `title`, `childSummary` og `summary`
- Hver oppføring har `matchedBy`: `purpose`, `sibling` eller `text`.
- **`library.purposes`** returnerer formålene gruppert som på verktøyflaten. Gruppene står i `../images/verktoy-fylt.html`.
- **Test (T-C2):** et sett på tjue ønsker (lages av Claude i `fixtures/`) gir treffrate med og uten tekstsøk.
- **Bevis:** `TESTRESULT.md#oppslag`

### Neste runde (ikke start før første runde er grønn)

- WP-B4 (forslag som `GroundedActionPlan`, negative tester)
- WP-B5 (profilregister ved siden av `switch helperRoute.keypath`, `Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift:5080`)
- WP-A3 (Kjetils oversikt)
- WP-F1, WP-F2 (publisering)

## Når du er ferdig

1. Push grenen `codex/spillverksted-runde1` og åpne en utkast-PR mot `main` med `gh pr create --draft`. Ikke merg.
1. Skriv kort i `codex-runde1-status.md` i denne mappa (handoff/) hva som er gjort, hvilke tester som er grønne, PR-lenken, og hva som er blokkert, med grunn. Skriv fila underveis også, etter hvert oppdrag, så Claude kan følge med.
2. Legg utdata fra testene i `../TESTRESULT.md`.
