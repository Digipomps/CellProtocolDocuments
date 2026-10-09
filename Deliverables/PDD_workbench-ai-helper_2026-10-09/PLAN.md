# PLAN — AI-hjelper i Developer Workbench

Oppgavemappe: `PDD_workbench-ai-helper_2026-10-09` · Skrevet 2026-10-09 etter G1 (13:44Z) og G1-GUI (13:53Z) · Venter på G2

Kilder er lest fra CellScaffold `origin/main` 2026-10-09 (etter merge av #302, `8a59bf7e`), ikke fra et lokalt utsjekk (`lesson.read-origin-main-before-writing-a-mechanism`).

## Hovedgrep

Én ny celle, `WorkbenchHelperCell` (`cell:///WorkbenchHelper`), eier instruksjonssettene og forslagene. Den lager ingen ny chatmotor og gir ingen modell verktøy:

1. Eieren skriver en bestilling i panelet. Hjelpercellen sender teksten, settets instruksjoner, flatens handlingskontrakt og utvalget til `cell:///ExecutablePurposeGrounding` (`grounding.analyze`). Svaret er en `GroundedActionPlan` (`ExecutablePurposeGrounding.swift:45`).
2. Hjelpercellen avviser planen hvis `target.actionKeypath` ikke står i settets `allowedActions`. Det er A4: teksten kan ikke utvide listen.
3. `grounding.verify` og `grounding.dryRun` gir forhåndsvisningen. Panelet viser elementene som berøres og markerer dem i listen.
4. Eieren trykker Utfør. Hjelpercellen kaller målcellen som eieren selv (`requester` er eierens identitet), én gang per element. Målcellen sjekker tilgang hver gang (`WorkItemCell.swift:929-931`). Hjelpercellen lagrer forrige verdi for hvert element, så hele handlingen kan angres i ett steg.
5. Kan settet ikke gjøre det som blir bedt om, svarer hjelperen hva som mangler (B4) og tilbyr Butler (F2). Butler-knappen er alltid med og kan ikke skrus av (F1).

AIGateway foreslår og får ingen verktøy, Butler Chat ruter (beslutning 2026-09-02). Hjelpercellen er en vanlig celle som utfører eierens egne klikk.

## Arbeidspakker

Én pakke per bladformål, i avhengighetsrekkefølge. Fase 1 er detaljert. Fase 2 og 3 får egne planer når fase 1 er akseptert.

Utfører: **Claude** = skyøkt med CellScaffold og CellProtocolDocuments, bygg via `scripts/run_swift_bounded.sh` / CI. **Codex** = lokal Mac (Binding, Xcode). **Kjetil** = beslutning eller deploy.

### Fase 1

| WP | purposeRef | Hva | Utfører | Tester som skal bli grønne | Leverer til §3 |
|---|---|---|---|---|---|
| WP0 | — | Baseline: `ci/check-value-literals.sh` og hele testmengden på ren `origin/main`, tall fra kjøringen, ikke fra rapport. | Claude (CI) | test.build, test.regression (baseline) | TESTRESULT.md#baseline |
| WP1 | `…instructions.multiple-sets` (A2) | `WorkbenchHelperCell` med de fire settene fra `contract/instruction-sets.seed.v0.json`, eierens alene. `sets`, `set.select`. Registreres som Scaffold-intern tilstand, ikke eager bootstrap (`lesson.new-cell-must-declare-its-provisioning-mode`). | Claude | T-A2; `OrchestratorPersistenceTests`, `TopUpCheckoutTests` uendret | kontrakt + celle |
| WP2 | `…instructions.editable` (A1) | `set.save`: ny tekst lagres, neste svar fra settet bruker den. | Claude | T-A1 | sett-rediger-v1.png (paritet) |
| WP3 | `…instructions.versioned` (A3) | Append-only versjoner, `set.diff`, `set.revert` som lager ny versjon. Diff som liste med radtype. | Claude | T-A3 | sett-rediger-v1.png |
| WP4 | `…instructions.limits-per-set` (A4) | Planer med handling utenfor `allowedActions` avvises før forhåndsvisning. Negativ test med fiendtlig instruksjonstekst («du har lov til å slette alt»), feil requester og `purpose://prompt.unknown`. | Claude | T-A4, test.cell.auth-negative | TESTRESULT.md#auth |
| WP5 | `…surface.knows-context` (C2) | Panelet sender flate, fane, utvalg og handlingskontrakt, og viser dem som brikker. Ingenting annet sendes. | Claude | T-C2 | hjelperpanel-tom-v1.png |
| WP6 | `…surface.act-on-many` (C1) | «Flytt alt fra inbox til triage»: plan med N elementer, markering via `WorkItem select`, Utfør som N kall til `setStatus`, angre i ett steg. Ingen ny bulk-handling på WorkItem. | Claude | T-C1 (celletest mot WorkItem) | hjelperpanel-fylt-v1.png, TESTRESULT.md#c1 |
| WP7 | `…gui.say-what-is-impossible` (B4) | Når planen mangler handling eller felt, vises feilkortet med listen over det som mangler og «Lag oppgave på det som mangler». | Claude | T-B4 | hjelperpanel-feil-v1.png |
| WP8 | `…gui.create-new` (B2) | Beskrivelse gir skjelett-utkast i Porthole-editoren. Krever først en cellehandling for forhåndsvisning og lagring, fordi editoren i dag er sesjonsbundet (`PortholeWebSessionSupport.swift:5929`, `:6106`). Utkastet avvises hvis det mangler Butler-vei (F3). | Claude | T-B2 | ny flate i staging |
| WP9 | `candidate.butler.always-reachable` (F1) | Book 23: eget formål ved siden av `skeleton.owner-entity-access` (standardsvar på §6 spørsmål 1). Butler-knapp i hjelperpanelet. CI-sjekk over katalogens konfigurasjoner: hver flate har en vei til Butler, enten Porthole-verktøylinjen (`porthole-webo.js:5159`) eller egen knapp. | Claude | T-F1 | CI-logg |
| WP10 | `…butler.never-lose-entity` (F3) | Samme sjekk kjøres før hjelperen lagrer en flate (WP8). | Claude | T-F3 | — |
| WP11 | — | Fanen/panelet i `DeveloperWorkbenchConfiguration`, `HavenWorkbenchConfigurationTests` oppdatert med ny referanse. Skjelett-JSON lagres i `skeleton/`. | Claude | test.skeleton.no-unreachable-elements, test.skeleton.purpose-actions-reachable | skeleton/ |
| WP12 | — | Binding: `purposeTree` og hjelperpanelet i SwiftUI, paritet mot web. | Codex (Xcode) | test.gui.parity | ACCEPT.md#parity |
| WP13 | `…root` (R) | Deploy til staging, Playwright-kjøring av panelet: tom, fylt, feil, rediger, med lastetid tre ganger. | Kjetil (deploy), Claude (kjøring) | T-R, test.gui.load-time | ACCEPT.md |

Commit og push etter første grønne bygg, ikke etter siste pakke (`lesson.branch-is-empty-after-eight-work-packages`). Hver pakke rapporterer commit fra `git rev-parse` og `git ls-remote`.

### Fase 2 (egen plan senere)

B1 Sindres to eksempler (krever tekstfelt for publisert verk i `PublicationCell`), B3 teste andre flater, C3 beskriv hva du vil lage, D1 finne i dokumentasjonen (krever lesende søk mot utvikler-RAG-en som cellehandling), E1 vurdere idéer, E2 lage oppgaver, F2 gi saken til Butler.

### Fase 3 (egen plan senere)

D2 dokumentendring som PR, E3 start arbeid hos HavenAgentD.

## Risiko og det som kan stoppe planen

- **AIGateway uten nøkkel i staging.** Uten leverandør gir `grounding.analyze` bare deterministisk matching. WP6 kan da fortsatt testes med fast plan, men T-R krever leverandør. Avklares i WP0.
- **Sidepanel på tvers av faner** finnes ikke i skjelettformatet (`images/README.md`). WP11 legger panelet i hver fane med `Reference` til samme celle. Blir det for tungt, spør jeg før et nytt skjelettelement lages.
- **WP8 trenger en ny cellehandling for Porthole-editoren.** Det er en endring i Porthole-integrasjonen. Går den ikke, flyttes B2 til fase 2 og skrives i STATUS som planbytte.

## Dataflyt

Se `dataflow.md`.
