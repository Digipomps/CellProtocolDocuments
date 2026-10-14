# PLAN — Butler Chat: trådtre med skop, og widgetflate

Oppgavemappe: `PDD_butler-traadtre-og-widgetflate_2026-09-11` · Skrevet 2026-09-12 etter G1 (godkjent 2026-09-12) og G1-GUI (godkjent 2026-09-12, referanse `images/*-v1.png`) · Port: **G2 godkjent 2026-09-13**

Én arbeidspakke per bladformål i FORMAALSSPEC.md §1, i avhengighetsrekkefølge. Hver pakke navngir purposeRef, utfører, testene den skal gjøre grønne (§5) og artefaktene den leverer til §3. Stier er `<repo>::<sti>`. Ingen git-mutasjon fra Cowork-VM-mount; commits, pushes og PR-er gjøres av Codex eller Kjetil på Mac. Lange bygg som detached skript (`lesson.codex-workspace-write-cannot-build-cellscaffold`), aldri som `workspace-write`-køjobb. Codex startes alltid som køjobb i `_losen-queue/inbox` (`lesson.paste-command-instead-of-queue`).

Kjetils regel 2026-09-12: **to uavhengige ting i to uavhengige PR-er.** Derfor tre grener: `pdd/skjelett-elementer` (format + renderere, felles forutsetning), `pdd/butler-hjelpertre` (A) og `pdd/butler-widgetflate` (B). A og B merges hver for seg; C1 (paritet) verifiseres per gren.

Grunnlag lest 2026-09-12: §3 rad 1–4 er levert og godkjent; §3 rad 9–11 (elementkart, kandidatskjelett, preview-scenario per del) er satt i kø som `skjelett-gap-tre|chat|flate-20260912` og kjører sekvensielt. §6 spm. 3 er ubesvart — planen legger Claudes forslag til grunn: **én fabrikk nå** (web og app fra samme skjelett-JSON), generisk dra-og-slipp i appen som egen PDD-oppgave. Sier Kjetil noe annet, endres WP-C1 og WP-B1 (planbytte i STATUS.md).

## Dette skal du gjøre, Kjetil — og ingenting annet

Alt annet i denne planen gjør Claude og Codex. Din del er tre ting, i denne rekkefølgen, og hver av dem er én handling.

| Når | Hva du gjør | Hvorfor bare du kan | Hva som skjer etterpå |
|---|---|---|---|
| I morgen tidlig | Kjør `HAVEN-Deploy/_handoff/NATT/KJOR-SELV-MORGEN.sh` i en vanlig terminal (`--torrkjor` først hvis du vil se hva den gjør) | Bare Mac-en din har GitHub-legitimasjon og hetzner-nøkkelen; og uprøvd kode skal ikke merges uten at et menneske har sett CI | Nattgrenene pushes, PR-er åpnes, CI kjører, grønne PR-er merges, image publiseres, staging deployes og verifiseres. Rapport i `HAVEN-Deploy/_handoff/NATT/natt-<tid>/nattrapport.md` |
| Når staging er verifisert | Si «prod» — eller kjør samme skript med `--prod` | R-D24: prod bare etter verifisert staging, og bare på ditt ord | Samme revisjon til prod, med samme verifisering |
| Når elementkartene er syntetisert (WP-K2) | Si ja eller nei til listen over nye skjelettelementer og -modifikatorer i `handoff/SKJELETT_ELEMENTER.md` | Regelen: ingen ny skjelettkapabilitet uten ditt ja | WP-R bygger dem; deretter justeres modifikatorer til flaten ser ut som mockupen (WP-K3) |

Det du **ser** etter hvert steg: etter steg 1 et hjelpertre til venstre i Butler Chat på staging (Butler som rot, klikk = skop, «Undertre / Bare denne»), og en «Flaten rundt» til høyre der et kort fra loggen kan dras over og festes — begge i dagens skjelettformat, altså **tilnærmet** mockupen, ikke pikselrett. Pikselrett kommer etter steg 3. Grafisk fremstilling av avhengighetene: `images/plan-v1.png`.

## 0. Rekkefølge og blokkeringer

```
WP0 baseline ─────────────────────────────────────────────────────────────────────────────┐
                                                                                           │
WP-K1 elementkart ×3 (Codex, kjører) ─► WP-K2 syntese + Kjetils ja til nye elementer ─► WP-R format+renderere (gren pdd/skjelett-elementer)
                                                                                           │             │
                                                                                           │             ├─► WP-K3 iterasjon mot staging (modifikatorer til likt)
                                                                                           │             │
   A-grenen (pdd/butler-hjelpertre):        WP-A5 datamodell ─► WP-A1 kontrakt ─► WP-A2 skop ─► WP-A3 ruting ─► WP-A4 forslag ◄─ PDD_formaalsregister (måling)
                                                                                           │             │
   B-grenen (pdd/butler-widgetflate):       WP-B0 restore/pinned ─► WP-B2b persistens ─► WP-B1 grep+slipp ─► WP-B2 levende ─► WP-B3 full flate ─► WP-B4 nåbarhet
                                                                                                                      └─► WP-B2c skopforslag ◄─ PDD_formaalsregister (måling)
                                                                                           │
   WP-C1 paritet (per gren, Binding) ◄── WP-R ─┘             WP-C2 mønsterdokumenter ◄── A og B levert
                                                                                           │
   WP-D1 staging (Kjetil) ─► ACCEPT ─► G3 ─► WP-D2 prod (Kjetil, bare etter verifisert staging, R-D24)
```

Blokkeringer som ikke er denne PDD-ens: **disk** — Mac-en har 7,5 % ledig, byggstarteren krever 10 % (målt av Codex 2026-09-12, `HAVEN-Deploy::_handoff/XCTVAPOR/RAPPORT.md`); ingen lokalt bygg før rydding. **HD-0040** (aksepttester på staging) og prod-promotering av `47912c28` er åpne. **Arbeidskopiene står på andre grener** (CellScaffold og CellProtocol: `pdd/tillitspakke-agentflaate`); alt arbeid her starter fra `origin/main` i egne worktrees (`lesson.les-origin-main-ikke-arbeidskopien`). **Formålsmatchingen** (A4, B2c) er målt til ikke bedre enn TF-IDF på n=4 (`PDD_formaalsregister-som-graf_2026-09-11/handoff/GRAF_OG_VEKTER.md`); A4 og B2c bygges med matcheren som *utskiftbar* komponent bak én funksjon, og godtas bare med måling.

Testtall er «forventet ≈ N (fra kilde, dato)», aldri fra hukommelsen: CellScaffold-fulltest **ukjent** til WP0 har målt (121 av 284 suiter kjører i CI, HAVEN-Deploy endringsstyring 2026-09-08); CellProtocol `SkeletonTests` ukjent.

## 1. Arbeidspakker

### WP0 — Baseline på ren eksport
- purposeRef: `purpose://quality.build-and-regression` (`pkg.std.everything-works`)
- Utfører: **Kjetil** rydder disk (RYDD-mac.sh i `HAVEN-Deploy::_handoff/OPPRYDDING/`), deretter **Codex** som detached skript (`CellScaffold::scripts/run_swift_bounded.sh build --build-tests` fra `origin/main` i ren worktree), logg til `evidence/wp0/`
- Gjør: `git fetch origin` (macOS, ikke mount); worktree fra `origin/main` for CellScaffold og CellProtocol; `swift build --build-tests`; `swift test --filter SkeletonTests` i CellProtocol; les resultatet fra «Test run with N tests», ikke exitkoden. Rød baseline = spørsmål, ikke tiltak.
- Tester: test.build, test.regression (baseline-tall)
- Leverer: `TESTRESULT.md#build`, `#regression` (baseline), `evidence/wp0/`

### WP-K1 — Elementkart per del av mockupen (kjører)
- purposeRef: `purpose://candidate.pattern.parity-and-reuse` (C1, forutsetning)
- Utfører: **Codex**, tre køjobber `skjelett-gap-tre-20260912`, `-chat-`, `-flate-` (i kø 2026-09-12 20:27Z, sekvensielt)
- Gjør: mockup-element → dagens element/modifikator eller gap (nytt element / ny modifikator / renderer-semantikk), web og app hver for seg; kandidatskjelett med dagens format; modifikator-starttabell fra mockupens CSS; handlingsliste; preview-scenario 2000×1250 og 780×1688
- Tester: — (analyse); kandidatene kontrolleres mot dekoderen om verktøy finnes, ellers merket ukontrollert
- Leverer: §3 rad 9–11: `handoff/SKJELETT_GAP_{tre,chat,flate}.md`, `skjelett/<del>.candidate.skeleton.json`, `<del>.modifikatorer.md`, `<del>.handlinger.md`, `<del>.keypaths.md`, `<del>.preview.json`

### WP-K2 — Syntese og Kjetils ja til nye elementer
- purposeRef: samme som K1
- Utfører: **Claude** syntetiserer; **Kjetil** godkjenner listen (regelen i `cellconfiguration-skeleton-authoring`: ingen ny kapabilitet uten hans ja)
- Gjør: slå de tre kartene sammen til én liste «nye elementer / nye modifikatorer / renderer-semantikk», hver med minste forslag, web- og app-kostnad, og hvilke bladformål som stopper uten den. Uavhengig validering av listen med Astra før den legges fram (Kjetils regel 2026-09-12).
- Tester: —
- Leverer: `handoff/SKJELETT_ELEMENTER.md` (godkjent liste = kontrakt for WP-R); planbytte i STATUS.md hvis listen endrer WP-R

### WP-R — Format og renderere: elementene mockupen trenger (gren `pdd/skjelett-elementer`, egen PR)
- purposeRef: `purpose://candidate.pattern.parity-and-reuse` (C1); forutsetning for A2, B1, B3
- Utfører: **Codex** (kode + tester i CellProtocol og CellScaffold, worktree fra `origin/main`); **Xcode-tråd/Kjetil** for Binding-rendereren; Claude gransker diffen før PR
- Gjør, avgrenset til den godkjente listen fra K2: `CellProtocol::Sources/CellBase/Skeleton/SkeletonDescription.swift` (nye cases/felter, Codable, `SkeletonReachabilityAudit` utvidet så nye elementer ikke blir usynlige), `CellScaffold::Public/js/skeleton-runtime.js` (web), `CellProtocol::Sources/CellApple/Cells/Porthole/Utility Views/Skeleton/SkeletonElementView.swift` + `SkeletonParityRenderer.swift` (app). Hver ny case får en `SkeletonTests`-dekodingstest og en audit-test. Ingen Butler-spesifikk logikk her.
- Tester: test.skeleton.no-unreachable-elements (for nye elementer), test.build, test.regression
- Leverer: kode + tester på gren, `contract/skeleton-elements.md` (feltene, semantikken, hva web og app garanterer), `TESTRESULT.md#reachability`, `#build`

### WP-K3 — Iterasjon: modifikatorer justeres til det ser likt ut
- purposeRef: C1 (`test.gui.parity`)
- Utfører: **Claude** via Chrome på Kjetils maskin, eller **Codex** hvis `workspace-write` får nettverk (Kjetils valg, se handoff/README.md); mot staging som kjører WP-R
- Gjør: `npm run skeleton:iterate -- --mode preview --scenario skjelett/<del>.preview.json` per del; skjermbilde legges over `images/deler/<del>-web-<tilstand>.png` og `-app-`; modifikatorer i kandidaten justeres til avviket er borte eller navngitt; hver runde er en ny `-v<n>` i `images/` med `skeleton/`-JSON ved siden av (kravet i `pkg.std.gui-surface`)
- Tester: test.gui.parity (per del, web og app), test.gui.load-time
- Leverer: `skeleton/<del>.skeleton.json` (endelig), `images/<del>-<flate>-<tilstand>-v<n>.png` fra Porthole (ikke mockup), `TESTRESULT.md#load-time`, avvik i `ACCEPT.md#parity`

### WP-A5 — Hjelpertre som datamodell i cellen (gren `pdd/butler-hjelpertre`)
- purposeRef: `purpose://candidate.butler.helper-tree-model`
- Utfører: **Codex**; Claude gransker diffen
- Gjør: i `CellScaffold::Sources/App/Cells/PersonalCopilot/PersonalCopilotCloudStore.swift` (dagens flate `helperRows`/`activeHelper`/`visibleKinds`, `origin/main` l. 969–1205 lest 2026-09-11): nodeobjekt med `id`, `parentID` (Butler = rot uten forelder), `kind`, `references` (verktøy/celle/chat), og `promptMessages` får `nodeID`. Migrering: hver eksisterende `helperRow` blir barn av Butler, alle meldinger uten node får Butler; kjøres idempotent ved første lasting. Kontrakten i `CellProtocol::Sources/CellBase/PersonalCopilot/PersonalCopilotContracts.swift` utvides med versjon.
- Tester: test.migration (ekte staging-eksport som fixture, antall meldinger og hjelpere før = etter), test.build
- Leverer: kode + tester, `contract/helper-tree.md`, `dataflow.md` (hvem skriver treet, hvem leser), `TESTRESULT.md#migration`

### WP-A1 — Node = hjelper med forelder og referanser
- purposeRef: `purpose://candidate.pattern.reference-tree.model`
- Utfører: **Codex**
- Gjør: kontraktstest som bygger et tre med tre nivåer, legger til en node uten å røre rot, lar to noder peke på samme verktøy, og avviser sykler. Skjelettet leser treet gjennom keypathene fra WP-K1 (`tre.keypaths.md`).
- Tester: test.tree-model
- Leverer: `TESTRESULT.md#tree-model`; skjelett-JSON for treet i `skeleton/tre.skeleton.json` (fra WP-K3)

### WP-A2 — Skop: undertre / bare denne
- purposeRef: `purpose://candidate.pattern.reference-tree.scope`
- Utfører: **Codex**; avhenger av WP-R hvis K2 sier at skop er renderer-semantikk (KAPASITET rad 2 sier det i dag)
- Gjør: skopet beregnes i cellen (`scope.mode` ∈ {subtree, node}, `scope.nodeID`), loggen leveres ferdig filtrert og kronologisk med `branchOrigin` per melding; telleren «N meldinger · M grener i skop» kommer fra cellen. Klikk på node = én action-keypath (fra `tre.handlinger.md`).
- Tester: test.scope.switch (bytte endrer meldingsmengde og teller; grenopphav synlig)
- Leverer: kode + tester, `TESTRESULT.md#scope`, `ACCEPT.md#ways-in` (skop-handlingene i `reachableActionKeypaths`)

### WP-A3 — Ruting oppover med Butler som fallback
- purposeRef: `purpose://candidate.pattern.reference-tree.routing`
- Utfører: **Codex**
- Gjør: `route(message, fromNode)`: nærmeste hjelper som kan svare; kan den ikke (avslår, mangler tilgang, feiler), går meldingen til forelder, til Butler. Ruten logges per melding (`route: [nodeID…]`, `refusedBy`, `reason`) og vises som feillinjen i bildet `web-feil-v1.png` med handlingene «Gi tilgang» / «Vis ruten» (keypaths fra `chat.handlinger.md`). Ingen melding ubesvart.
- Tester: test.routing.fallback (hjelper som avslår → forelder → Butler; ruten logget)
- Leverer: kode + tester, `TESTRESULT.md#routing`

### WP-A4 — Forslag om ny hjelper fra formålsmatching
- purposeRef: `purpose://candidate.pattern.reference-tree.suggest-helper`
- Utfører: **Codex**; matcher fra `PDD_formaalsregister-som-graf_2026-09-11` bak én funksjon `suggestHelper(purposeSignals) -> Suggestion?`
- Gjør: når rutingen ender hos Butler uten treff, kalles matcheren med brukerens formålssignaler; forslaget vises i loggen og i treet som ny node når brukeren sier ja; avslått forslag lagres og gjentas ikke uendret. Matcheren er utskiftbar (TF-IDF er dagens beste målte kandidat; «vis alle» er nullreferansen).
- Tester: test.helper.suggestion (simulerte brukere med formål utenfor dagens hjelpere; treff-andel mot nullreferanse — måles, ikke antas)
- Leverer: kode + tester, `TESTRESULT.md#suggest` med tall mot nullreferanse

### WP-B0 — Lukk restore/pinned-spenningen før noe festes (gren `pdd/butler-widgetflate`)
- purposeRef: §2-avhengighet (mistenkt feil), forutsetning for B1
- Utfører: **Codex**
- Gjør: reprodusér eller avkreft med sti:linje: `origin/main` `PersonalCopilotCloudStore.swift` l. 1188 (`pinnedComponentSurfaces = visibleComponentSurfaces.filter { $0.pinned }`) mot `activePanelSurfaces`-filteret; skriv testen som feiler først (restore av en festet post skal gjøre den synlig i aktivt panel eller beholde den festet — kontrakten avgjøres i `contract/widgets.md`).
- Tester: test.regression (ny test), test.build
- Leverer: `TESTRESULT.md#restore-pinned`, oppdatert `contract/widgets.md`

### WP-B2b — Widgets eies og persisteres i Portholens CellConfiguration
- purposeRef: `purpose://candidate.pattern.detachable-surface-element.owned-and-persisted`
- Utfører: **Codex**; kontrakten skrives av Claude først (`contract/widgets.md`)
- Gjør: widgetlisten lever i Portholens `CellConfiguration` (ikke UI-tilstand, ikke nettleser): `widgets: [{id, sourceEndpoint, sourceKeypath, title, template, attachedAt, scope}]`; lagring gjennom eksisterende editable-kontrakt for source-backed konfigurasjon (`Skeleton_Runtime_Iteration_Workflow.md` «commit-runtime» krever `EditableCellConfigurationContract` — verifiser at Butler-konfigurasjonen har det, ellers er det første steg). Kilde: Kjetils svar §6 spm. 2.
- Tester: test.widget.persisted (ny innlasting + ny enhet med samme identitet)
- Leverer: kode + tester, `contract/widgets.md`, `TESTRESULT.md#persist`

### WP-B1 — Grep og slipp
- purposeRef: `purpose://candidate.pattern.detachable-surface-element.grip-and-drop`
- Utfører: **Codex** (web via `draggableRole`/`dropTargetRole`-modifikatorene som finnes, KAPASITET rad 3); app-delen er egen PDD (§6 spm. 3 default)
- Gjør: kortet i loggen får `draggableRole: "widget-source"`, `dragPayloadKeypath` = kortets kilde; flaten er `dropTargetRole` med `acceptedDragRoles: ["widget-source"]` og `dropActionKeypath` → cellens `widgets.attach` (oppretter posten fra WP-B2b). Slippsone og spøkelse som i `web-dra-v1.png`. Avbrutt dra = ingen endring.
- Tester: test.dnd.attach (dra→slipp fester; avbrutt dra endrer ingenting), test.skeleton.no-unreachable-elements
- Leverer: kode + tester, `TESTRESULT.md#dnd`, `#reachability`

### WP-B2 — Levende binding
- purposeRef: `purpose://candidate.pattern.detachable-surface-element.live-binding`
- Utfører: **Codex**; avhenger av WP-R hvis K2 sier at «følger kilden» er renderer-semantikk (KAPASITET rad 5 sier at pin/restore bare muterer UI-posten)
- Gjør: widgetposten binder til `sourceEndpoint`+`sourceKeypath`; oppdatering går gjennom en eksisterende, bevist hendelsesvei (Flow-abonnement eller bootstrap-refresh — velg den som er påvist, oppgi sti:linje), «oppdatert HH:MM» og feiltilstand «kilden svarer ikke — viser siste kjente verdi» (`web-feil-v1.png`).
- Tester: test.widget.live (kildeendring slår gjennom uten ny henting fra brukeren)
- Leverer: kode + tester, `dataflow.md` (widget-delen), `TESTRESULT.md#live`

### WP-B2c — Propageringsskop med formålsutledet forslag
- purposeRef: `purpose://candidate.pattern.detachable-surface-element.propagation-scope`
- Utfører: **Codex**; samme matcher-funksjon som WP-A4
- Gjør: ved feste/endring: spørsmål «alle / bare denne / utvalg» med forhåndsvalgt forslag fra `suggestScope(purposeSignals, widget)`; valget lagres på posten (`scope`), er synlig og reverserbart.
- Tester: test.widget.scope-suggestion (simulerte brukere med ulike formål; treff-andel mot «alltid bare denne» som nullreferanse)
- Leverer: kode + tester, `TESTRESULT.md#scope-suggestion` med tall

### WP-B3 — Full flate
- purposeRef: `purpose://candidate.pattern.detachable-surface-element.full-surface`
- Utfører: **Codex**; avhenger av WP-R (kolonnebytte er ikke uttrykkbart i dag, KAPASITET)
- Gjør: `widgets.expand`/`widgets.collapse`-actions; full flate viser Innleder-kolonnen (`web-full-v1.png`), chatten dokkes (`chat-web-full-dokket.png`); retur gir samme tilstand.
- Tester: test.gui.parity mot `web-full-v1.png`
- Leverer: kode, `ACCEPT.md#parity` (full-raden)

### WP-B4 — Alt widgeten kan, kan bes om i chatten
- purposeRef: `purpose://candidate.pattern.detachable-surface-element.reachability`
- Utfører: **Codex**
- Gjør: hver widget-action (attach, detach, expand, collapse, scope) finnes som keypath nåbar fra samtalen; `SkeletonReachabilityAudit.reachableActionKeypaths` over ferdig skjelett sammenlignes med handlingslistene fra WP-K1.
- Tester: test.skeleton.purpose-actions-reachable
- Leverer: `ACCEPT.md#ways-in`

### WP-C1 — Paritet HAVEN app (per gren)
- purposeRef: `purpose://candidate.pattern.parity-and-reuse.parity.haven-app`
- Utfører: **Xcode-tråd/Kjetil** (Binding-bygg og -tester), **Codex** for fabrikk
- Gjør: Butler-konfigurasjonen leveres fra én fabrikk (samme skjelett-JSON til web og Binding — §6 spm. 3 default); Binding-rendereren kjører WP-R-elementene; app-DnD er utenfor (egen PDD) og avviket **navngis** i ACCEPT.md med begrunnelse. Skjermbilde av bygget flate med ekte data, app-bredde 780×1688, ved siden av `app-*-v1.png`.
- Tester: test.gui.parity (app), `BindingTests/CellConfigurationVerifierXCTest/testNoLocalSurfaceHidesItsOwnWaysIn`
- Leverer: `ACCEPT.md#parity` (app-radene), `images/app-*-v<n>.png` fra Binding

### WP-C2 — Mønsterdokumentene
- purposeRef: `purpose://candidate.pattern.parity-and-reuse.reuse.documented-pattern`
- Utfører: **Claude**; uavhengig lesning av Astra («kan en fremmed leser peke ut hva som må implementeres?»)
- Gjør: `CellProtocolDocuments::patterns/reference-tree.md` og `patterns/detachable-surface-element.md` (ny mappe): kontrakt, grenser, skjelett-elementene fra WP-R, minst én bruk som ikke er Butler Chat (f.eks. utviklerbenkens idétre, `PDD_utviklerbenk-oppgavegraf_2026-09-10`); krysspekere fra `Book/`.
- Tester: test.docs-updated
- Leverer: §3 rad 5–6, `ACCEPT.md#docs`

### WP-D1 — Staging kjører A og B
- purposeRef: §3 rad 7–8
- Utfører: **Kjetil** (kjeden main → staging via `haven-deploy`, `lesson.codex-sandbox-cannot-reach-docker`); Claude forbereder HAVEN-Deploy-posten per PR
- Tester: `/health/build` = commit med PR-en; HD-0040-aksepttester
- Leverer: `TESTRESULT.md#staging-build`; deretter ACCEPT.md rad for rad → G3

### WP-D2 — Prod
- Utfører: **Kjetil**, bare etter verifisert staging (R-D24), som egen HAVEN-Deploy-post
- Leverer: `/health/build` prod = samme commit

## 2. Hva §3 får fra hvilken pakke

| §3 rad | Leveranse | Pakke |
|---|---|---|
| 1–4 | kapasitet, paritet, referansebilder | levert, godkjent |
| 5–6 | mønsterdokumenter | WP-C2 |
| 7 | trådtre med skop på staging | WP-A5, A1, A2, A3, A4 → WP-D1 |
| 8 | widgetflate med dra-ut på staging | WP-B0, B2b, B1, B2, B2c, B3, B4 → WP-D1 |
| 9–11 | elementkart, kandidatskjelett, preview-scenario | WP-K1 (kjører) |

## 3. Det planen ikke gjør
Generisk dra-og-slipp i appen (egen PDD). Ny svarkvalitet i Butler (#230, i main). Endringer i deploy-kjeden. Ny matcher — A4 og B2c bruker det `PDD_formaalsregister-som-graf` måler, bak én funksjon, og godtas bare med tall mot nullreferanse.
