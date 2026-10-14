#!/bin/bash
# Dobbeltklikk: snapshot av ucommittet CellProtocol-arbeid til wip-gren + checkout main. Logger.
H="$HOME/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_invitasjon-tillit_2026-09-15/handoff/rundeA"
chmod +x "$H/snapshot-og-main.sh"
"$H/snapshot-og-main.sh" 2>&1 | tee "$H/snapshot-og-main-$(date +%Y%m%d-%H%M%S).log"
echo; echo "=== ferdig (exit ${PIPESTATUS[0]}) — vinduet kan lukkes ==="
