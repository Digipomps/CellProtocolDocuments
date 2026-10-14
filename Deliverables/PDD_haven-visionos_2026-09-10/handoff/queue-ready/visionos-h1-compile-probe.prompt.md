Du er Codex-utfører for PDD «HAVEN på Apple Vision». Oppgavemappe (P): `CellProtocolDocuments/Deliverables/PDD_haven-visionos_2026-09-10/` (relativt HAVEN-roten, som er cwd).

Les først `P/handoff/README.md`. Utfør **kun H1 — byggeproben**: kjør `P/handoff/h1_compile_probe.sh` som en detached prosess og avslutt. Skriptet gjør alt; du skal ikke skrive kode, ikke rette feil, ikke endre hovedtrærne.

**Forhåndssjekk (gjør denne først):**

    zsh P/handoff/h1_compile_probe.sh

Dette er en tørrkjøring. Den skal skrive «Tørrkjøring ferdig» eller «BLOCKED: ingen visionOS-simulator-SDK». Skriver den BLOCKED: kjør den én gang til med `--go` (da skrives blocked-raden til `P/TESTRESULT.md#h1`), skriv én linje i `P/STATUS.md` («H1 blocked — visionOS-SDK mangler i Xcode»), og stopp.

**Kjøring (bare hvis tørrkjøringen var ren):** start skriptet detached slik at kalleren kan time ut uten at bygget dør:

    python3 - <<'PY'
    import subprocess, os
    log = open("_h1-visionos-probe.out", "ab")
    subprocess.Popen(["zsh", "CellProtocolDocuments/Deliverables/PDD_haven-visionos_2026-09-10/handoff/h1_compile_probe.sh", "--go"],
                     stdout=log, stderr=subprocess.STDOUT, start_new_session=True, cwd=os.getcwd())
    PY

Skriv deretter én linje i `P/STATUS.md`: «H1 startet <tidspunkt> — resultat kommer i TESTRESULT.md#h1 og _h1-visionos-probe.out». Vent ikke på bygget. Ingen ny kjøring hvis en `_h1-visionos-probe-<dato>/probe.log` allerede finnes fra i dag (lesson.codex-mcp-60s: én timeout = én kjørende sesjon).

Ingen git-operasjoner utover de skriptet selv gjør (`rev-parse`, `branch --show-current`, `archive`). Ingen docker. Ingen deploy. Ingen `pkill`.
