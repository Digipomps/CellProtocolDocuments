#!/bin/bash
set -uo pipefail
WT="${CELLPROTOCOL_WORKTREE:-$HOME/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata}"
HERE="$(cd "$(dirname "$0")" && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOG="$HERE/verify-$STAMP.log"
FULL="$HERE/verify-$STAMP.full.log"
cd "$WT"
echo "logg: $LOG (sammendrag), $FULL (alt)"
summarize() {
  sed 's/\x1b\[[0-9;]*m//g' | grep -E "Test Suite '[A-Za-z]+Tests' (passed|failed)|Executed [0-9]+ tests|error:|Test Case .* failed" | grep -v "warning:"
}
{
  echo "== git =="
  git branch --show-current
  git rev-parse HEAD
  echo "== build =="
  swift build > "$FULL" 2>&1 && echo "Build: OK" || { echo "Build: FEILET"; grep -E "error:" "$FULL" | head -20; }
  echo "== runde 1-tester =="
  swift test --filter 'EntityGenesisTests|EntityAnchorGenesisTests|IdentityLinkRegistryBindingTests' >> "$FULL" 2>&1
  sed -n '/runde 1/,$p' "$FULL" | summarize
  echo "== regresjon: autorisasjon og identitet =="
  swift test --filter 'IdentityLinkRegistryTests|IdentityLinkingModelsTests|VaporCellRuntimeReadinessContractTests|CellRuntimeReadinessContractTests|TrustedIssuerCellTests|EntityAuthorityCommitTests|EntityAnchorEncryptionTests' > "$FULL.regresjon" 2>&1
  summarize < "$FULL.regresjon"
  echo "== hele CellBaseTests (for a se at ingenting annet knakk) =="
  swift test --filter 'CellBaseTests' > "$FULL.alle" 2>&1
  grep -E "Executed [0-9]+ tests" "$FULL.alle" | tail -2
  grep -E "Test Case .* failed" "$FULL.alle" | sed 's/\x1b\[[0-9;]*m//g' | head -30
} 2>&1 | tee "$LOG"
echo
echo "Les 'Executed N tests, with M failures'. Exitkoden er ikke sannheten."
