#!/bin/bash
# Pusher pdd/entitetsdata-egen-kontroll fra worktreet. Rører ikke Kjetils utsjekk. Ingen merge, ingen force.
set -uo pipefail
WT="${CELLPROTOCOL_WORKTREE:-$HOME/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata}"
BRANCH="pdd/entitetsdata-egen-kontroll"
EXPECT="e66b7f1"
echo "worktree: $WT"
[ -d "$WT" ] || { echo "FEIL: worktree finnes ikke"; exit 1; }
cd "$WT"
echo "branch:   $(git branch --show-current)"
echo "HEAD:     $(git rev-parse --short HEAD)  ($(git log -1 --format=%s))"
[ "$(git branch --show-current)" = "$BRANCH" ] || { echo "FEIL: feil branch"; exit 1; }
git rev-parse --short HEAD | grep -q "^$EXPECT" || { echo "FEIL: HEAD er ikke $EXPECT"; exit 1; }
[ -z "$(git status --porcelain)" ] || { echo "FEIL: worktreet er skittent:"; git status --short; exit 1; }
git fetch -q origin
echo "origin/main: $(git rev-parse --short origin/main)"
echo "bak main:    $(git rev-list --count HEAD..origin/main) commits · foran: $(git rev-list --count origin/main..HEAD)"
echo "== merge-test mot origin/main (skriver ingenting) =="
if git merge-tree --write-tree origin/main HEAD >/tmp/mt.out 2>&1; then echo "merger rent"; else echo "KONFLIKT ved merge:"; grep -E '^CONFLICT' /tmp/mt.out | head; fi
if git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1; then
  echo "branchen finnes allerede på origin @ $(git ls-remote --heads origin "$BRANCH" | cut -c1-7)"
fi
echo "== push =="
git push -u origin "$BRANCH" 2>&1 | tail -5
echo "origin/$BRANCH: $(git ls-remote --heads origin "$BRANCH" | cut -c1-7)"
if command -v gh >/dev/null 2>&1; then
  if gh pr view "$BRANCH" --json url -q .url 2>/dev/null; then echo "PR finnes allerede"; else
    gh pr create --draft --base main --head "$BRANCH" \
      --title "Entitetsdata runde 1: genesis forsegler ankeret til initiatoren" \
      --body "PDD_entitetsdata-egen-kontroll runde 1 (WP1–WP2). EntityGenesisService/EntityGenesisSeal, identityLinks.genesis på EntityAnchorCell (Vapor + Apple), sameEntityLink krever localEntityAnchor. 16 nye tester, 1244/1244 CellBaseTests grønne 22.09 (CellProtocolDocuments: Deliverables/PDD_entitetsdata-egen-kontroll_2026-09-08/TESTRESULT.md). Utkast: åpnet for CI, ikke for merge ennå.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_0166zoWBapoQ3R6iiJrhd2xx" 2>&1 | tail -3
  fi
else
  echo "gh finnes ikke — ingen PR opprettet"
fi
