#!/bin/zsh -l
# Starter Codex på spillverkstedets runde 1 (WP-E2, WP-D2, WP-E1, WP-C2).
# Laget av Claude 2026-10-09. Dobbeltklikk i Finder for å kjøre.
HAVEN=/Users/kjetil/Build/Digipomps/HAVEN
WT=$HAVEN/tmp/codex-spillverksted-r1
HO=$HAVEN/CellProtocolDocuments/Deliverables/PDD_spillverksted_2026-10-09/handoff
LOG=$HO/codex-runde1.log
CODEX=$(command -v codex)
for c in /Applications/Codex.app/Contents/Resources/codex /Applications/ChatGPT.app/Contents/Resources/codex /opt/homebrew/bin/codex "$HOME/.local/bin/codex"; do
  [ -z "$CODEX" ] && [ -x "$c" ] && CODEX=$c
done
if [ -z "$CODEX" ]; then echo "Fant ikke codex. Si fra til Claude i tråden." | tee "$LOG"; read; exit 1; fi
if [ ! -d "$WT" ]; then
  git -C "$HAVEN/CellScaffold" fetch origin main && git -C "$HAVEN/CellScaffold" worktree add "$WT" -b codex/spillverksted-runde1 origin/main || { echo "Kunne ikke lage worktree" | tee "$LOG"; read; exit 1; }
fi
echo "codex: $CODEX  worktree: $WT  start: $(date -u +%FT%TZ)" | tee "$LOG"
"$CODEX" exec -s danger-full-access -C "$WT" \
  "Les $HO/README.md og utfør første runde (WP-E2, WP-D2, WP-E1, WP-C2) i rekkefølgen der. Følg AGENTS.md i repoet. Jobb bare i $WT. Oppdater $HO/codex-runde1-status.md etter hvert oppdrag. Push grenen og åpne en utkast-PR til slutt; ikke merg." 2>&1 | tee -a "$LOG"
echo "Ferdig $(date -u +%FT%TZ). Du kan lukke vinduet." | tee -a "$LOG"
