#!/bin/bash
# Dobbeltklikk: kjører invitasjon runde A del 1 (CellProtocol) og logger.
H="$HOME/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_invitasjon-tillit_2026-09-15/handoff/rundeA"
chmod +x "$H/rundeA.sh"
"$H/rundeA.sh" --go 2>&1 | tee "$H/rundeA-run-$(date +%Y%m%d-%H%M%S).log"
echo; echo "=== ferdig (exit ${PIPESTATUS[0]}) — vinduet kan lukkes ==="
