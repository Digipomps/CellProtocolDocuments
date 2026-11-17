#!/bin/bash
# WP0 for PDD_invitasjon-tillit runde A: CellScaffold og Binding mot CellProtocol origin/main (7577d74)
cd "$(dirname "$0")"
LOG="../../../PDD_invitasjon-tillit_2026-09-15/handoff/rundeA/wp0-$(date +%Y%m%d-%H%M%S).log"
mkdir -p "$(dirname "$LOG")"
CELLPROTOCOL_WORKTREE="$HOME/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata-r2" bash ./downstream.sh 2>&1 | tee "$LOG"
echo; echo "Ferdig. Logg: $LOG"
