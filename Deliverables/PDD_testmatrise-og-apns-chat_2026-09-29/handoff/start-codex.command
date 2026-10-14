#!/bin/bash
# Starter Codex mot handoff-filen. Skriv-tilgang kun til pdd-check, PDD-mappen og byggebuffere; nettverk på (localhost-probe, pakkehenting).
PDD="/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_testmatrise-og-apns-chat_2026-09-29"
cd /Users/kjetil/Build/pdd-check || exit 1
/Users/kjetil/.local/bin/codex exec --help > "$PDD/handoff/codex/exec-help.txt" 2>&1
/Users/kjetil/.local/bin/codex exec -C /Users/kjetil/Build/pdd-check \
  --sandbox workspace-write \
  -c sandbox_workspace_write.network_access=true \
  --add-dir "$PDD/handoff" \
  --add-dir "$HOME/Library/Caches" --add-dir "$HOME/.swiftpm" --add-dir "$HOME/Library/org.swift.swiftpm" --add-dir "$HOME/Library/Developer" \
  "Les $PDD/handoff/codex/HANDOFF_CODEX_fase1b.md og utfør slicene som er merket GODKJENT, med reglene der. Skriv resultatet til $PDD/handoff/codex/RESULT_fase1b.md."
RC=$?
echo; echo "Codex ferdig (exit $RC). Resultat: $PDD/handoff/codex/RESULT_fase1b.md"
read -p "Trykk Enter for å lukke…" _
