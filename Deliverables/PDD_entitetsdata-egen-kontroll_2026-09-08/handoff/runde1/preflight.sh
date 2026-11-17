#!/bin/bash
set -euo pipefail
REPO="${CELLPROTOCOL_REPO:-$HOME/Build/Digipomps/HAVEN/CellProtocol}"
WT="${CELLPROTOCOL_WORKTREE:-$HOME/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata}"
BRANCH="pdd/entitetsdata-egen-kontroll"
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO"
echo "repo: $REPO"
echo "worktree: $WT"
echo "branch i hovedutsjekk: $(git branch --show-current) (rores ikke)"
git fetch origin main
if [ -n "$(git status --short --untracked-files=no)" ]; then
  echo "MERK: hovedutsjekket har ulagrede endringer. De rores ikke; arbeidet skjer i et eget worktree:"
  git status --short --untracked-files=no
fi
LOCAL_MAIN="$(git rev-parse main 2>/dev/null || echo none)"
ORIGIN_MAIN="$(git rev-parse origin/main)"
echo "main:        $LOCAL_MAIN"
echo "origin/main: $ORIGIN_MAIN"
if [ "$LOCAL_MAIN" != "$ORIGIN_MAIN" ]; then
  echo "MERK: lokal main og origin/main er ulike. Grenen lages fra origin/main."
fi
if [ -d "$WT" ]; then
  echo "MERK: worktree finnes allerede: $WT"
  echo "  gren der: $(git -C "$WT" branch --show-current)"
  echo "  tilstand: $(git -C "$WT" status --short | wc -l | tr -d ' ') endrede filer"
fi
echo "sjekker at patchen passer mot origin/main:"
git worktree add --detach /tmp/runde1-precheck origin/main >/dev/null 2>&1 || true
( cd /tmp/runde1-precheck && git apply --check "$HERE/runde1.patch" && echo "patch: passer" )
git worktree remove --force /tmp/runde1-precheck >/dev/null 2>&1 || true
echo "preflight: OK"
