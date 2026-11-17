# STATUS — lister celle og komponent

- surfaces: binding, cell, gui, porthole, skeleton, web
- tags: cell, gui, lister, parity, skeleton

## Porter
- G1: godkjent 2026-10-02 (Kjetils ord, valgknapp i chatten: «G1 og G1-GUI godkjent»; FORMAALSSPEC revisjon 2)
- G1-GUI: godkjent 2026-10-02 (samme ord; referanse = de åtte `images/*-v1.png`, rendret med web-rendereren fra `skeleton/`)
- G2: godkjent 2026-10-08 (Kjetils ord, valgknapp: «G2 godkjent»; valg A for tekst i montering: `SkeletonComponentActionContext` i CellBase)
- G3: venter        (ACCEPT.md skrevet 2026-10-08; PR #64 åpen; venter på Kjetils ord — og på hans ja til app-bildene v2)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
-

## Logg
- 2026-10-08 10:02Z: **CI grønn på PR #64** (`m8`, `pr-status-4.md`): alle 5 sjekker pass (regression 20m20s, bounded synthetic runtime matrix 18m7s, Persisted Cell file bounds, Vapor identity vault strict storage, Dispatch PyCellProtocol), `mergeStateStatus: CLEAN`, head `29dbfa8`. Klar for Kjetils merge og G3.
- 2026-10-08 09:50Z: **P6 læringsfangst ført.** Fem lærdommer i `Book/haven_lessons_register_v0.json` (`lesson.render-candidate-skeleton-with-the-web-renderer-before-g1-gui`, `lesson.shared-swiftpm-cache-lost-its-ownership-marker`, `lesson.xctest-stdout-export-interleaves-with-its-own-log`, `lesson.textfield-cannot-carry-instance-identity-in-a-mount`, `lesson.capability-based-layout-variant-replaces-client-checks`); tre skills oppdatert (`haven-purpose-driven-dev`: P1-GUI med ekte web-renderer og app-kapabiliteter, P2 «Dette skal du gjøre» + lanes; `cellconfiguration-skeleton-authoring`: «Render the candidate first» + målte fakta; `haven-mac-shell-scripts`: byggjobber for PDD-arbeidstre); seks poster i `CellScaffold/Documentation/Learnings/ledger.jsonl` (`L-2026-10-08-render-candidate-skeleton-with-the-web-renderer`, `…-pdd-worktree-build-job-needs-its-own-swiftpm`, `…-xctest-stdout-export-must-go-through-a-file`, `…-textfield-in-a-mount-reads-the-instance-from-the`, `…-choose-affordances-by-capability-with`, `…-developer-workbench-must-show-lanes-like-plan-v1`), alle `applied` + `synced` av agent-runner-jobben `haven-learn-sync-20261008-094955` (09:49:58Z, alle 6 steg ok; ~/.claude, ~/.codex, Desktop-lagrene og ZIP-ene oppdatert, ingen drift). Kjetils lanes-innspill ført til `PDD_utviklerbenk-oppgavegraf_2026-09-10/INNSPILL-2026-10-08-lanes.md`. PR #64 (`m6`, 09:50Z): 3 sjekker grønne, `regression` og `bounded synthetic runtime matrix` fortsatt pending.
- 2026-10-08 09:36Z: **WP6 ferdig — PR #64 åpnet** (`m4`): `pdd/lister-celle` @ `29dbfa8` pushet (`origin == lokal HEAD`), `gh pr create` mot `main`. Full regresjon (`m1`): **1572 tester, 5 hoppet over, 0 feil** (1545 + 27). Formatsjekk (`m3`): tom diff mot SkeletonDescription/ReachabilityAudit/Porthole. ACCEPT.md skrevet; app-bildene fikk `-v2` (uten `drag`, pilene synlige); tre pikseldiffer referanse ↔ ekte state = 0.
- 2026-10-08 09:28Z: **WP5 ferdig**: cellens ekte `lists.state` eksportert (`l9`, via fil — stdout ble flettet med XCTests logg i `l5`, og `/usr/local/bin/python3` på Macen er en x86-binær, `l8`), rendret i skyen med CellScaffolds renderer: 3 monteringer ok, handlinger i montering bærer `mount.instanceID`, varianter drag/noDrag/narrow som ventet. Commits `4ecd1d5` (`l6`) og `29dbfa8` (`m2`).
- 2026-10-08 09:15Z: WP1–WP3 skrevet i skyen og lagt i arbeidstreet (4 kildefiler + `SkeletonComponentActionContext.swift` + 3 testfiler + fixture); byggejobb `l4` i køen (fokuserte tester). Ikke verifisert ennå («skrevet, ikke verifisert»).
- 2026-10-08 09:12Z: **WP0 GRØNN** (`l3`): arbeidstre `_worktrees/cellprotocol-lister` på `pdd/lister-celle` fra origin/main `afa8cbf` (låst mot prune), baseline `swift build` 6 min 9 s, `swift test` 2 min 21 s: **1545 tester, 5 hoppet over, 0 feil**. Underveis: `l0` blokkert av diskvakten (55 GiB; krav 57), `l1` ryddet /private/tmp til 68 GiB, `l2` stoppet i `haven-swiftpm.sh` fordi den delte cachen manglet eiermarkøren (exit 64) → eget cache-key `lister-celle` (lærdom, føres i P6).
- 2026-10-08 08:58Z: G2 godkjent av Kjetil, valg A (ComponentActionContext i CellBase). Innspill fra Kjetil samme minutt om lanes i utviklerbenken ført til `PDD_utviklerbenk-oppgavegraf_2026-09-10/INNSPILL-2026-10-08-lanes.md`. origin/main har gått til `afa8cbf` (#53, #60, #61, #62) siden auditen; skjelett-/Porthole-filene er uendret, FORMAALSSPEC holder.
- 2026-10-02: G1 og G1-GUI godkjent av Kjetil (valgknapp «G1 og G1-GUI godkjent»). PLAN.md (P2), dataflow.md, contract/ (kontrakt v0 + 18 fixtures + validator, GRØNN i skyen) og images/plan-v1.png skrevet. Venter på G2.
- 2026-10-02: opprettet
- 2026-10-02: §6 besvart av Kjetil i chatten (valgknapper): 1 piler + dra (pilene skjules der verten har `drag`), 2 CellProtocol `cell:///Lists`, 3 celle + konfig + tester i CellProtocol som én PR (meny i app/katalog som egen pakke etterpå), 4 idéer er vanlig liste i v1. FORMAALSSPEC iterasjon 2. Ingen port satt — venter på Kjetils ord for G1 og G1-GUI.
- 2026-10-02: FORMAALSSPEC iterasjon 1: §0 audit (21 rader, alle retrieved mot CellProtocol origin/main 253b4af og CellScaffold origin/main fdcfe7a5), §1 (15 noder + 3 antiformål), §2, §3 (15 rader), §5, §6 (4 spørsmål). Åtte referansebilder rendret i skyen med CellScaffolds skeleton-runtime.js (md5 i images/README.md) fra skeleton/*.json; oppførsel (5 handlinger) bekreftet i images/render-report.json. Funn underveis: webens produktvisning overstyrer `controlStyle: plain` (porthole-webo.css 4759); webens ikonkart mangler `circle`; Binding mangler både ComponentSurface-vertsadapter og drag-adapter (R6). Venter på G1, G1-GUI og svar på §6.

## Venter på Kjetil
- **Merge PR #64** (https://github.com/Digipomps/CellProtocol/pull/64) — CI er grønn (5/5, 10:02Z); Losen kan ikke merge.
- **G3**: les ACCEPT.md; si «G3 godkjent», og om app-referansen skal være `-v2` (pilene synlige), jf. ACCEPT «Avvik» 1–2.
- Neste pakke (egen PDD): integrasjon — meny i HAVEN-appen og CellScaffold-katalogen, pin-oppdatering, ScaffoldKit-typealias, native skjermbilde.
