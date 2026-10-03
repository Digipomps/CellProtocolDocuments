#!/bin/bash
# Kjetils checkout av CellProtocol: ta vare på alt ucommittet som en wip-gren
# (snapshot, pushet), og sett checkouten til origin/main. Ingenting slettes,
# ingenting tvinges. Stopper ved første avvik fra det som ble målt 29.09.
set -uo pipefail
REPO="$HOME/Build/Digipomps/HAVEN/CellProtocol"
EXPECT_BRANCH="pdd/tillitspakke-agentflaate"
EXPECT_HEAD="561d34a"
WIP="wip/uuid-nokling-2026-09-23"
STAMP="$(date +%Y%m%d-%H%M%S)"
cd "$REPO" || { echo "FEIL: finner ikke $REPO"; exit 1; }

echo "== før =="
if [ -f .git/index.lock ]; then
  mkdir -p .git/_stale && mv .git/index.lock ".git/_stale/index.lock.$STAMP" && echo "flyttet gammel index.lock til .git/_stale/"
fi
BRANCH="$(git rev-parse --abbrev-ref HEAD)"; HEAD="$(git rev-parse --short HEAD)"
echo "gren: $BRANCH @ $HEAD"
[ "$BRANCH" = "$EXPECT_BRANCH" ] || { echo "FEIL: ventet $EXPECT_BRANCH — stopper"; exit 1; }
[ "$HEAD" = "$EXPECT_HEAD" ] || { echo "FEIL: ventet HEAD $EXPECT_HEAD — stopper"; exit 1; }
git fetch -q origin || { echo "FEIL: fetch"; exit 1; }
echo "origin/main: $(git rev-parse --short origin/main)"
git merge-base --is-ancestor main origin/main || { echo "FEIL: lokal main har egne commits — stopper"; exit 1; }
git show-ref --verify -q "refs/heads/$WIP" && { echo "FEIL: $WIP finnes allerede — stopper"; exit 1; }
git status --short | wc -l | sed 's/^/ucommitterte filer (M+??): /'

echo "== 1. snapshot på $WIP =="
git checkout -q -b "$WIP" || { echo "FEIL: checkout -b"; exit 1; }
git add -A -- . ':!**/__pycache__/**' ':!**/*.pyc'
git commit -q -F - <<'MSG'
wip(uuid-nøkling): snapshot av ucommittet arbeid i Kjetils checkout, 2026-09-29

Alt som lå ucommittet på pdd/tillitspakke-agentflaate (561d34a) 23.09–29.09:
CellIdentifier/UUIDText-refaktoreringen (Sources/CellBase/Utilities/CellIdentifier.swift,
@UUIDText på ChatCell/ChatInvitationProofUtility/…, identifier-nøkling i
EphemeralIdentityVault), Docs/EntityData-Review-2026-09-11 (beslutning 22.09 om
uuid-nøkling og grupper), og øvrige lokale endringer. Ikke bygget, ikke testet her —
tatt vare på som det lå, så det kan tas opp igjen som egen PDD/PR.

Checkouten settes deretter til origin/main (81601a6), som allerede har #47, #50 og
#51 (invitasjon runde A del 1), så chat-testing mellom inviterte kan starte på main.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0166zoWBapoQ3R6iiJrhd2xx
MSG
[ $? -eq 0 ] || { echo "FEIL: commit"; exit 1; }
SNAP="$(git rev-parse --short HEAD)"
echo "snapshot: $SNAP ($(git diff --stat HEAD~1 HEAD | tail -1))"
git push -q -u origin "$WIP" 2>&1 | tail -2
echo "origin/$WIP: $(git ls-remote --heads origin "$WIP" | cut -c1-7)"
[ -n "$(git ls-remote --heads origin "$WIP")" ] || { echo "FEIL: push av snapshot feilet — checkouten står på $WIP, urørt ellers"; exit 1; }

echo "== 2. checkout main = origin/main =="
git checkout -q main || { echo "FEIL: checkout main"; exit 1; }
git merge -q --ff-only origin/main || { echo "FEIL: ff-only"; exit 1; }
echo "main @ $(git rev-parse --short HEAD)"
LEFT="$(git status --short | grep -v '^?? _wt' | wc -l | tr -d ' ')"
echo "ucommittert etter bytte: $LEFT"
git status --short | grep -v '^?? _wt' | head -10
for f in Sources/CellBase/Invitation/HavenInviteReply.swift Sources/CellBase/Invitation/HavenContactBasisV1.swift Sources/CellBase/PersistingCells/EntityChangeTrace.swift; do
  [ -f "$f" ] && echo "ok  $f" || echo "MANGLER $f"
done
git show origin/main:Sources/CellBase/Cells/Chat/ChatInvitationProofUtility.swift | cmp -s - Sources/CellBase/Cells/Chat/ChatInvitationProofUtility.swift && echo "ok  ChatInvitationProofUtility == origin/main" || echo "AVVIK ChatInvitationProofUtility"

echo "== 3. swift build på main (bare bygg; testene gikk i #51/CI) =="
swift build > "$HOME/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_invitasjon-tillit_2026-09-15/handoff/rundeA/main-build-$STAMP.log" 2>&1 && echo "Build: OK" || { echo "Build: FEILET (se main-build-$STAMP.log)"; exit 1; }
echo "== ferdig: snapshot $SNAP på $WIP, checkout på main $(git rev-parse --short HEAD) =="
