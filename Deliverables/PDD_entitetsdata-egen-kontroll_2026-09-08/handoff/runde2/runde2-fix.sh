#!/bin/bash
# Fix-commit on top of pdd/entitetsdata-runde2 (399f6d2 was pushed red because the
# green gate matched the wrong "Executed" line). Applies runde2-fix1.patch, builds,
# tests, and pushes a fast-forward commit only when the LAST result lines are green.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
WT="$HOME/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata-r2"
BRANCH="pdd/entitetsdata-runde2"
STAMP="$(date +%Y%m%d-%H%M%S)"
FULL="$HERE/fix1-$STAMP.full.log"
PATCH="${1:-$HERE/runde2-fix1.patch}"
cd "$WT" || { echo "FEIL: worktree mangler"; exit 1; }
[ "$(git branch --show-current)" = "$BRANCH" ] || { echo "FEIL: feil branch $(git branch --show-current)"; exit 1; }
echo "HEAD: $(git rev-parse --short HEAD) · patch: $(basename "$PATCH")"
if git apply --check -p1 "$PATCH" 2>/dev/null; then
  git apply -p1 "$PATCH" && echo "patch lagt på"
elif git apply --check -R -p1 "$PATCH" 2>/dev/null; then
  echo "patchen ligger allerede på (forrige kjøring stoppet før commit) — går videre"
else
  echo "PATCHEN PASSER IKKE, og ligger heller ikke allerede på"; git status --short; exit 1
fi
git status --short
echo "== swift build =="
swift build > "$FULL" 2>&1 && echo "Build: OK" || { echo "Build: FEILET"; grep -E "error:" "$FULL" | head -30; exit 1; }
echo "== nye tester =="
swift test --filter 'EntityAnchorAccessBoundaryTests' > "$FULL.new" 2>&1
NEW_LAST="$(grep -E "Executed [0-9]+ tests" "$FULL.new" | tail -1)"; echo "$NEW_LAST"
grep -E "error: -\[" "$FULL.new" | sed 's/\x1b\[[0-9;]*m//g' | cut -c1-300 | head -20
echo "== parity + runde 1 =="
swift test --filter 'EntityRelationHostParityTests|EntityGenesisTests|EntityAnchorGenesisTests|IdentityLinkRegistryBindingTests' > "$FULL.r1" 2>&1
grep -E "Executed [0-9]+ tests" "$FULL.r1" | tail -1
echo "== hele CellBaseTests =="
swift test --filter 'CellBaseTests' > "$FULL.alle" 2>&1
ALL_LAST="$(grep -E "Executed [0-9]+ tests" "$FULL.alle" | tail -1)"; echo "$ALL_LAST"
grep -E "Test Case .* failed" "$FULL.alle" | sed 's/\x1b\[[0-9;]*m//g' | head -20
# No pipe here: under pipefail, `echo | grep -q` can fail on SIGPIPE even when the text matches (26.09 02:32).
GREEN=0
case "$NEW_LAST" in *" 0 failures (0 unexpected)"*) case "$ALL_LAST" in *" 0 failures (0 unexpected)"*) GREEN=1;; esac;; esac
echo "gate: NEW_LAST=[$NEW_LAST] ALL_LAST=[$ALL_LAST] GREEN=$GREEN"
if [ "$GREEN" = "1" ]; then
  echo "== grønt — committer og pusher =="
  git add -A
  git commit -q -m "Entity data trace lives at its own keypath, not inside the chronicle list

The chronicle list is a wire-level contract hosts compare entry for entry
(EntityRelationHostParityTests); the trace must never change what a batch
wrote. It now lives at \`trace\` with its own grant, read intercept and
explore contract. Also: unknown-purpose assertion reads the error name, and
keypath lists are compared as strings (ValueType == is unreliable on
composites).

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0166zoWBapoQ3R6iiJrhd2xx"
  echo "commit: $(git rev-parse --short HEAD)"
  git push origin "$BRANCH" 2>&1 | tail -2
  echo "origin/$BRANCH: $(git ls-remote --heads origin "$BRANCH" | cut -c1-7)"
else
  echo "RØDT — committer IKKE (patchen ligger uncommitted i worktreet)."
  exit 1
fi
