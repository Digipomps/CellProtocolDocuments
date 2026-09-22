#!/bin/bash
set -euo pipefail
REPO="${CELLPROTOCOL_REPO:-$HOME/Build/Digipomps/HAVEN/CellProtocol}"
WT="${CELLPROTOCOL_WORKTREE:-$HOME/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata}"
BRANCH="pdd/entitetsdata-egen-kontroll"
HERE="$(cd "$(dirname "$0")" && pwd)"
GO="${1:-}"
cd "$REPO"
if [ "$GO" != "--go" ]; then
  echo "TORRKJORING. Ville gjort:"
  echo "  git worktree add $WT -b $BRANCH origin/main   (eller gjenbrukt worktreet)"
  echo "  git -C $WT apply --index $HERE/runde1.patch"
  echo "Hovedutsjekket rores ikke. Kjor med --go for a gjore det."
  exit 0
fi
if [ ! -d "$WT" ]; then
  if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
    git worktree add "$WT" "$BRANCH"
  else
    git worktree add "$WT" -b "$BRANCH" origin/main
  fi
fi
cd "$WT"
if git apply --check --reverse "$HERE/runde1.patch" >/dev/null 2>&1; then
  echo "patch: allerede pa plass i worktreet, hopper over apply"
elif [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ]; then
  echo "patch: ny versjon. Ingenting er committet pa grenen, sa worktreet nullstilles til origin/main og patchen legges pa nytt."
  git reset --hard origin/main >/dev/null
  git clean -fd Sources Tests >/dev/null
  git apply --index "$HERE/runde1.patch"
else
  echo "STOPP: grenen har commits utover origin/main og patchen passer ikke. Gjor dette for hand."
  git log --oneline origin/main..HEAD
  exit 1
fi
git status --short
echo "apply: OK i $WT. Ingenting er committet."
