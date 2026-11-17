# Handoff — felles regler for Codex-jobber i denne PDD-en

Oppgavemappe (P): `CellProtocolDocuments/Deliverables/PDD_haven-visionos_2026-09-10/`, relativt HAVEN-roten. Sett alltid cwd til HAVEN-roten.

1. **Én jobb, ett formål.** Før G1 finnes bare én jobb: H1-byggeproben. Den svarer til hypotese H1 i `P/ANALYSE.md` §3 og formålet `purpose://candidate.platform.visionos-native` i `P/FORMAALSSPEC.md` §1.
2. **Leveransestien står på linje 3 i `.job`.** Ligger den ikke under cwd, avviser runneren jobben.
3. **Lange bygg går aldri som `workspace-write`-køjobb** (`lesson.codex-workspace-write-cannot-build-cellscaffold`). H1 er `danger-full-access` og starter skriptet detached med `Popen(start_new_session=True)`; jobben returnerer før bygget er ferdig og resultatet leses fra disk.
4. **Ingen git-skriving.** Skriptet bruker bare `rev-parse`, `branch --show-current` og `archive`. Ingen commit, push, worktree, branchbytte. Hovedtrærne røres ikke; alt skjer i `_h1-visionos-probe-<dato>/`.
5. **Ingen docker, ingen deploy.**
6. **Ekte tall.** Feiltellinger limes inn fra faktisk kjøring (skriptet gjør det), aldri fra en tidligere rapport.
7. **Forhåndssjekk først.** Tørrkjøring uten `--go`. Mangler visionOS-SDK: `blocked` med årsak i `P/TESTRESULT.md#h1` og én linje i `P/STATUS.md`. Ikke bruk tid på en full kjøring.
8. **Blocked er et gyldig utfall.** Aldri stille droppet.
9. **Én kjøring per dag.** Finnes `_h1-visionos-probe-<dato>/probe.log` allerede, startes ingen ny (`lesson.codex-mcp-60s`).
10. **Stier er relative til repoet** i prompts, dokumentasjon og kode (`Binding/...`, `CellProtocol/Sources/...`). Rå logg- og feilutdata limes inn ordrett og er unntatt.
11. **Ingen retting i H1.** Proben måler; den retter ikke. Rettelser er implementering og hører til etter G2 i gren E.

## Etter G2 (16.09): løpet kjøres som `.command`, ikke som kø-jobb

Køen kan ikke bygge (`runner.sh` tillater bare `read-only`/`workspace-write`, og der feiler SwiftPM-sandkassen
og nettet er av). Skjermstyring fra Cowork gir bare klikk i Terminal/Xcode. Derfor:

- `KJOR-SELV-visionos.command` — dobbeltklikk i Finder (eller `zsh KJOR-SELV-visionos.command --dry-run` i Terminal).
  Gjør steg 0 → 1 → P (H1-måling) → A (steg 2) → B (steg 3) og skriver `TESTRESULT.md#h1/#steg2/#steg3`,
  `handoff/logs/KJOR-<tid>.log` og skjermbilder i `images/`. Kjøres når Macen er våken og på nett; 20–60 min.
- `patches/apply_patches.py <Binding> <CellProtocol> --phase P|A|B|AB [--dry-run]` — ankere med forventet
  treffantall; feiler ett anker, røres ikke filen. Idempotent (markør «PDD haven-visionos»).
- `patches/PortholeBackside.swift` — kopieres inn i CellApple av fase B.
- Alt skjer i `_worktrees/visionos-<dato>/{Binding,CellProtocol}` på gren `losen/visionos-sim-<dato>`.
  Hovedtrærne røres ikke. Ingen commit, push eller sletting i løpet.
- `h1_compile_probe.sh` beholdes som frittstående H1-probe (ren eksport), men løpet over dekker H1 (fase P).
