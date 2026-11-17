#!/bin/bash
# Merger PR #47 (squash, som repoets konvensjon) — bare når alle CI-sjekker er grønne.
set -uo pipefail
WT="${CELLPROTOCOL_WORKTREE:-$HOME/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata}"
PR=47
cd "$WT" || exit 1
command -v gh >/dev/null || { echo "FEIL: gh mangler"; exit 1; }
echo "== PR #$PR =="
gh pr view $PR --json state,isDraft,mergeable,headRefOid,baseRefName -q '"state=\(.state) draft=\(.isDraft) mergeable=\(.mergeable) head=\(.headRefOid[0:7]) base=\(.baseRefName)"'
echo "== CI-sjekker (venter inntil 25 min på at alle er ferdige) =="
for i in $(seq 1 50); do
  OUT="$(gh pr checks $PR 2>&1)"; PENDING=$(echo "$OUT" | grep -ciE '\b(pending|queued|in_progress)\b' || true)
  if [ "$PENDING" = "0" ]; then break; fi
  echo "  $(date +%H:%M:%S): $PENDING venter…"; sleep 30
done
echo "$OUT"
if echo "$OUT" | grep -qiE '\bfail'; then echo "RØD CI — merger IKKE. Se over."; exit 1; fi
if echo "$OUT" | grep -qiE '\b(pending|queued|in_progress)\b'; then echo "CI ikke ferdig etter 25 min — merger IKKE."; exit 1; fi
echo "== undraft + squash-merge =="
gh pr ready $PR 2>&1 | tail -1
gh pr merge $PR --squash --subject "Entitetsdata runde 1: genesis forsegler ankeret til initiatoren (#$PR)" \
  --body "EntityGenesisService/EntityGenesisSeal; identityLinks.genesis på EntityAnchorCell (Vapor + Apple); sameEntityLink krever localEntityAnchor. 16 nye tester; CellBaseTests 1248/1248 på 94a4bed. Nedstrøms (CellScaffold, Binding) grønne mot branchen 24.09 — CellProtocolDocuments: Deliverables/PDD_entitetsdata-egen-kontroll_2026-09-08/TESTRESULT.md#build.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0166zoWBapoQ3R6iiJrhd2xx" 2>&1 | tail -3
git fetch -q origin
echo "origin/main: $(git rev-parse --short origin/main)  $(git log -1 --format=%s origin/main | cut -c1-80)"
git show origin/main:Sources/CellBase/Identity/EntityGenesis.swift >/dev/null 2>&1 && echo "EntityGenesis.swift finnes på origin/main ✓" || echo "EntityGenesis.swift MANGLER på origin/main"
gh pr view $PR --json state,mergedAt -q '"state=\(.state) mergedAt=\(.mergedAt)"'
