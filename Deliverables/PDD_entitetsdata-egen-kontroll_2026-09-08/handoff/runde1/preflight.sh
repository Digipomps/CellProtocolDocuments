#!/bin/bash
set -euo pipefail
REPO="${CELLPROTOCOL_REPO:-$HOME/Build/Digipomps/HAVEN/CellProtocol}"
BRANCH="pdd/entitetsdata-egen-kontroll"
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO"
echo "repo: $REPO"
echo "branch now: $(git branch --show-current)"
git fetch origin main
if [ -n "$(git status --short --untracked-files=no)" ]; then
  echo "STOPP: arbeidstreet har ulagrede endringer i sporede filer"
  git status --short --untracked-files=no
  exit 1
fi
LOCAL_MAIN="$(git rev-parse main 2>/dev/null || echo none)"
ORIGIN_MAIN="$(git rev-parse origin/main)"
echo "main:        $LOCAL_MAIN"
echo "origin/main: $ORIGIN_MAIN"
if [ "$LOCAL_MAIN" != "$ORIGIN_MAIN" ]; then
  echo "MERK: lokal main og origin/main er ulike. Grenen lages fra origin/main, ikke fra lokal main."
fi
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  echo "MERK: $BRANCH finnes allerede. apply.sh sjekker den ut i stedet for a lage den."
fi
echo "sjekker at patchen passer mot origin/main:"
git worktree add --detach /tmp/runde1-precheck origin/main >/dev/null 2>&1 || true
( cd /tmp/runde1-precheck && git apply --check "$HERE/runde1.patch" && echo "patch: passer" )
git worktree remove --force /tmp/runde1-precheck >/dev/null 2>&1 || true
if git ls-files --error-unmatch Package.swift >/dev/null 2>&1; then
  if [ -d .build ] && grep -rq "\"path\"" .build/workspace-state.json 2>/dev/null && grep -q "editedDependencies\|\"edited\"" .build/workspace-state.json 2>/dev/null; then
    echo "MERK: .build/workspace-state.json kan ha redigerte avhengigheter. Sjekk: swift package show-dependencies"
  fi
fi
echo "preflight: OK"
