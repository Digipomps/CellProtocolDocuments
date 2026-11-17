#!/bin/bash
# Dobbeltklikk: lager wip-commits (én gren per repo) av ucommittet arbeid i CellProtocol, CellScaffold,
# Binding og CellProtocolDocuments, og pusher dem. Rører ingen checkout (egen indeks + commit-tree).
# Kjørt fra Mac fordi VM-en ikke har git-identitet eller SSH-nøkler. Godkjent av Kjetil 29.09 ("Ja, kjør --go").
H="$HOME/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_testmatrise-og-apns-chat_2026-09-29/handoff"
chmod +x "$H/snapshot-alle.sh"
cd "$H" && OUT="$H/snapshot-alle-$(date +%Y%m%d-%H%M%S)" ./snapshot-alle.sh --go 2>&1 | tee -a "$H/snapshot-alle-go-$(date +%Y%m%d).log"
echo; echo "=== ferdig — vinduet kan lukkes ==="
