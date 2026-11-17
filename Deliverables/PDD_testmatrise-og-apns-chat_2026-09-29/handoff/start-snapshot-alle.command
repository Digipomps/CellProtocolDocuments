#!/bin/bash
# Dobbeltklikk: wip-snapshot av ucommittet arbeid i CellProtocol, CellScaffold, Binding, CellProtocolDocuments (uten å røre checkouts).
# Første gang: tørrkjøring. Kjør med --go som argument i Terminal når listene er sett over.
H="$HOME/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_testmatrise-og-apns-chat_2026-09-29/handoff"
chmod +x "$H/snapshot-alle.sh"
cd "$H" && OUT="$H/snapshot-alle-$(date +%Y%m%d-%H%M%S)" ./snapshot-alle.sh "$@" 2>&1 | tee -a "$H/snapshot-alle-run-$(date +%Y%m%d).log"
echo; echo "=== ferdig — vinduet kan lukkes ==="
