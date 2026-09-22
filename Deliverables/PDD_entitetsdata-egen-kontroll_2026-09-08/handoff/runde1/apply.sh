#!/bin/bash
set -euo pipefail
REPO="${CELLPROTOCOL_REPO:-$HOME/Build/Digipomps/HAVEN/CellProtocol}"
BRANCH="pdd/entitetsdata-egen-kontroll"
HERE="$(cd "$(dirname "$0")" && pwd)"
GO="${1:-}"
cd "$REPO"
if [ "$GO" != "--go" ]; then
  echo "TORRKJORING. Ville gjort:"
  echo "  git checkout -b $BRANCH origin/main   (eller checkout hvis den finnes)"
  echo "  git apply --index $HERE/runde1.patch"
  echo "  git status --short"
  echo "Kjor med --go for a gjore det."
  git apply --check "$HERE/runde1.patch" && echo "patch: passer mot naavaerende utsjekk" || echo "patch: passer IKKE mot naavaerende utsjekk (forventet hvis du star pa en annen gren; preflight sjekket mot origin/main)"
  exit 0
fi
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git checkout "$BRANCH"
else
  git checkout -b "$BRANCH" origin/main
fi
git apply --index "$HERE/runde1.patch"
git status --short
echo "apply: OK. Ingenting er committet. verify.sh bygger og tester; commit gjores av deg."
