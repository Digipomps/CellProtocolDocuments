# STATUS — haven visionos

- surfaces: binding, cell, codex, gui, porthole, skeleton, xcode
- tags: binding, diagnostics, flow, gui, inspect, multiwindow, porthole, skeleton, spatial, visionos

## Porter
- G1: godkjent 2026-09-16        (formålsspesifikasjon godkjent av Kjetil — grenene E og B; Kjetils svar på beslutningsspørsmålet 16.09)
- G1-GUI: venter        (rendret bilde godkjent — bare for GUI-oppgaver)
- G2: godkjent 2026-09-16        (PLAN.md steg 0–4; vei 1 = Losen styrer Terminal; første skive = baksiden parallelt med simulator-start)
- G3: venter        (akseptanse: forventning mot faktisk, alle avledede tester grønne)

Sett en port til `godkjent <dato>` kun når Kjetil har sagt det. `purpose_dev.py validate <mappe>` nekter porter uten artefakter.

## Planbytter (dato — hvorfor)
- 2026-09-16 — FORMAALSSPEC §6 foreslo B → C → E → A → D. G2 setter E og B parallelt, E først i tid, fordi Kjetils spørsmål 16.09 er «kjør det i simulatoren» og ingenting starter der uten E. C, A, D blir egne PDD-er.

## Logg
- 2026-09-10: opprettet
- 2026-09-10: læring fra Binding, CellProtocol, CellProtocolDocuments og Apple-dokumentasjon (visionOS 26/27); FORMAALSSPEC §0–§7 og ANALYSE.md skrevet; fire mockups i images/; H1-byggeprobe klargjort i handoff/queue-ready (ikke kjørt — venter på Kjetils ja). device_bash var nede hele økten; filer lest via staging. Klar for G1.
- 2026-09-10 (senere): Kjetil svarte på §6-1 — simulator inntil videre — og ba om opprydding i OS-/kapabilitetssjekker. Levert `OS_KAPABILITETSAUDIT.md` og `contract/` (referanse, ikke i repoet). Tre kompileringsfeil for visionOS funnet ved lesing (ContentView 1687/1695, RootView 185, ScannerService 266). Ingen kode endret i repoene. H1 fortsatt ikke kjørt (venter på ja).
- 2026-09-16: Kjetil spurte «Kan du implementere denne mocken og kjøre det i simulatoren med VisionOS?». Levert `PLAN.md` (utkast, G2 venter) med steg 0–4, hva hvert punkt innebærer og hva Kjetil selv må gjøre, `images/plan-simulator-v1.png`, og motlesning fra egen tråd («Fabel», PLAN.md §7) som endret ni punkter. `handoff/h1_compile_probe.sh` rettet etter motlesningen (simulator-kjøretid, disk, `--again`-vakt, `-project`, `CODE_SIGNING_ALLOWED=NO`). Kompileringsfeilene sjekket på nytt mot Macen: ContentView 1691/1699, RootView 188, ScannerService **288** (flyttet fra 266). Ingen kode endret i repoene. H1 fortsatt ikke kjørt. Venter på portord (G1/G2) og valg av vei (§3).
- 2026-09-16 (senere): Kjetil svarte: «G1 godkjent og G2 godkjent», vei 1 (Losen styrer Terminal på Macen), første skive = baksiden parallelt med simulator-start. G1-GUI venter på `bakside-datastrommer-v2.png`. Steg 0 startes.
- 2026-09-16 (kveld): vei 1 måtte endres — skjermstyring gir bare klikk i Terminal/Xcode, og køen tillater ikke bygg (runner.sh: read-only|workspace-write). Levert `handoff/KJOR-SELV-visionos.command` (steg 0–3 i ett dobbeltklikk), `handoff/patches/apply_patches.py` (fase P/A/B, ankere verifisert mot Macens filer 16.09, idempotent) og `handoff/patches/PortholeBackside.swift`. Ikke kompilert ennå. Venter på at løpet kjøres på Macen (dobbeltklikk).
- 2026-09-16 (natt): Løpet kjørt fire ganger fra Finder via skjermstyring. visionOS **blocked**: plattformen «visionOS 26.2» er ikke installert i Xcode 26.3 (SDK-stubben lurte forhåndssjekken; skriptet sjekker nå kjøretiden). Rød baseline (NavigationBar-case) reparert i worktreet med Kjetils egne ucommittede rettelser (`handoff/patches/baseline/`). **Steg 3 på Mac: bygger og kjører** — baksiden viser Absorbert/Abonnert/Puls/Set-get fra `Personal Home` med ærlige tilstander (`TESTRESULT.md#steg3-obs`). Worktrees `_worktrees/visionos-20260916/{Binding,CellProtocol}` på `losen/visionos-sim-20260916`, ucommittet, 1,7 GB. Venter på: visionOS-plattform installert (Kjetil), Skjermopptak-tillatelse for Terminal (for skjermbildefiler), G1-GUI-ord og G3-vurdering av baksiden på Mac.
