#!/bin/bash
# Dobbeltklikk: WP0-baseline (bygg + test av origin/main i tre repoer). Tar lang tid; vinduet må stå åpent.
H="$HOME/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_testmatrise-og-apns-chat_2026-09-29/handoff"
chmod +x "$H/baseline.sh"
cd "$H" && ./baseline.sh --go
echo; echo "=== ferdig — vinduet kan lukkes ==="
