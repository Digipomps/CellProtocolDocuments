#!/bin/bash
set -uo pipefail
REPO="${CELLPROTOCOL_REPO:-$HOME/Build/Digipomps/HAVEN/CellProtocol}"
HERE="$(cd "$(dirname "$0")" && pwd)"
LOG="$HERE/verify-$(date +%Y%m%d-%H%M%S).log"
cd "$REPO"
echo "logg: $LOG"
{
  echo "== git =="
  git branch --show-current
  git rev-parse HEAD
  echo "== build =="
  swift build 2>&1 | tail -40
  echo "== runde 1-tester =="
  swift test --filter 'EntityGenesisTests|EntityLinkAuthorizationTests|EntityAnchorGenesisTests' 2>&1 | tail -80
  echo "== eksisterende autorisasjonstester (regresjon) =="
  swift test --filter 'IdentityLinkingModelsTests|VaporCellRuntimeReadinessContractTests|CellRuntimeReadinessContractTests|TrustedIssuerCellTests|EntityAuthorityCommitTests' 2>&1 | tail -40
} 2>&1 | tee "$LOG"
echo
echo "Les resultatlinjene 'Executed N tests, with M failures' i loggen. Exitkoden er ikke sannheten (lesson.swift-test-exit-code-lies-in-havenagentd)."
