#!/bin/bash
# Merger PR #47 (squash, som repoets konvensjon) — bare når alle CI-sjekker er grønne.
set -uo pipefail
WT="$HOME/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata-r2"
PR=50
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
gh pr merge $PR --squash --subject "Entitetsdata runde 2: lesing og skriving krever entitetsbevis, hver endring etterlater spor (#$PR)" \
  --body "EntityChangeTrace (ett spor per akseptert batchPersist, på eget keypath trace), lesing/skriving/handlinger krever entitetsbevis, purpose://prompt.unknown feiler lukket, agreements-intercept, SimulatedEntity + 9 tester × 2 scaffolds. 1262/1262 CellBaseTests på d9bd69f. CellProtocolDocuments: Deliverables/PDD_entitetsdata-egen-kontroll_2026-09-08/TESTRESULT.md#runde2.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0166zoWBapoQ3R6iiJrhd2xx" 2>&1 | tail -3
git fetch -q origin
echo "origin/main: $(git rev-parse --short origin/main)  $(git log -1 --format=%s origin/main | cut -c1-80)"
git show origin/main:Sources/CellBase/PersistingCells/EntityChangeTrace.swift >/dev/null 2>&1 && echo "EntityChangeTrace.swift finnes på origin/main ✓" || echo "EntityChangeTrace.swift MANGLER på origin/main"
gh pr view $PR --json state,mergedAt -q '"state=\(.state) mergedAt=\(.mergedAt)"'
