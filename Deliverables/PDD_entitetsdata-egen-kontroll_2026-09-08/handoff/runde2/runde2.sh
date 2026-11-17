#!/bin/bash
# Entitetsdata runde 2 (WP3–WP5): applies runde2.patch on a fresh worktree from
# origin/main, builds, runs the new suite + full CellBaseTests, and commits+pushes
# only when everything is green. Never touches Kjetil's checkout. No force.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
BASE="$HOME/Build/Digipomps/HAVEN"
REPO="$BASE/CellProtocol"
WT="$BASE/CellProtocol-pdd-entitetsdata-r2"
BRANCH="pdd/entitetsdata-runde2"
STAMP="$(date +%Y%m%d-%H%M%S)"
FULL="$HERE/runde2-$STAMP.full.log"
MODE="${1:-}"

echo "== fetch =="
git -C "$REPO" fetch -q origin || { echo "FEIL: fetch"; exit 1; }
MAIN="$(git -C "$REPO" rev-parse --short origin/main)"
echo "origin/main: $MAIN"
git -C "$REPO" show origin/main:Sources/CellBase/Identity/EntityGenesis.swift >/dev/null 2>&1 || { echo "FEIL: genesis (#47) er ikke på origin/main"; exit 1; }

echo "== worktree $WT @ $BRANCH =="
if [ -d "$WT" ]; then
  if [ -n "$(git -C "$WT" status --porcelain)" ] || [ "$(git -C "$WT" rev-parse HEAD)" != "$(git -C "$REPO" rev-parse origin/main)" ]; then
    if git -C "$WT" log --oneline origin/main..HEAD | grep -q .; then
      echo "worktreet har egne commits — rører det ikke:"; git -C "$WT" log --oneline origin/main..HEAD; exit 1
    fi
    git -C "$WT" reset -q --hard origin/main
    git -C "$WT" clean -qfd
  fi
else
  git -C "$REPO" worktree add -q -B "$BRANCH" "$WT" origin/main || { echo "FEIL: worktree add"; exit 1; }
fi
git -C "$WT" checkout -q -B "$BRANCH" origin/main
echo "HEAD: $(git -C "$WT" rev-parse --short HEAD)"

echo "== patch (dry-run) =="
git -C "$WT" apply --check -p1 "$HERE/runde2.patch" || { echo "PATCHEN PASSER IKKE mot origin/main $MAIN — stopper"; exit 1; }
[ "$MODE" = "--go" ] || { echo "Tørrkjøring OK. Kjør med --go for å legge på, bygge, teste og pushe."; exit 0; }
git -C "$WT" apply -p1 "$HERE/runde2.patch" && echo "patch lagt på"
git -C "$WT" status --short

cd "$WT"
echo "== swift build =="
swift build > "$FULL" 2>&1 && echo "Build: OK" || { echo "Build: FEILET"; grep -E "error:" "$FULL" | head -30; exit 1; }
echo "== nye tester =="
swift test --filter 'EntityAnchorAccessBoundaryTests' > "$FULL.new" 2>&1
grep -E "Executed [0-9]+ tests" "$FULL.new" | tail -1
grep -E "error:|Test Case .* failed|XCTAssert" "$FULL.new" | head -40
echo "== runde 1-tester =="
swift test --filter 'EntityGenesisTests|EntityAnchorGenesisTests|IdentityLinkRegistryBindingTests' > "$FULL.r1" 2>&1
grep -E "Executed [0-9]+ tests" "$FULL.r1" | tail -1
echo "== hele CellBaseTests =="
swift test --filter 'CellBaseTests' > "$FULL.alle" 2>&1
grep -E "Executed [0-9]+ tests" "$FULL.alle" | tail -1
# Only the LAST "Executed" line counts: every suite prints its own, and a green
# suite early in the log must not vouch for a red one later (26.09: it did).
NEW_LAST="$(grep -E "Executed [0-9]+ tests" "$FULL.new" | tail -1)"
ALL_LAST="$(grep -E "Executed [0-9]+ tests" "$FULL.alle" | tail -1)"
# No pipe here: under pipefail, `echo | grep -q` can fail on SIGPIPE even when the text matches (26.09 02:32).
GREEN=0
case "$NEW_LAST" in *" 0 failures (0 unexpected)"*) case "$ALL_LAST" in *" 0 failures (0 unexpected)"*) GREEN=1;; esac;; esac
echo "gate: NEW_LAST=[$NEW_LAST] ALL_LAST=[$ALL_LAST] GREEN=$GREEN"
if [ "$GREEN" = "1" ]; then
  echo "== grønt — committer og pusher =="
  git add -A
  git commit -q -F - <<'MSG'
Entity data: reads and writes need entity proof, and every change leaves a trace

purpose://candidate.entitetsdata.read-requires-entity-proof
purpose://candidate.entitetsdata.no-write-without-owner-proof
purpose://candidate.entitetsdata.change-leaves-a-trace

- EntityChangeTrace: one chronicle entry per accepted batchPersist (signer,
  keypaths, purposeRef, modelRef, receipt), written in the same snapshot as the
  change; an idempotent replay adds nothing. purpose://prompt.unknown fails closed.
- Direct keypath writes through the anchor's feed require owner proof and are traced.
- EntityAnchorCell (Vapor + Apple) gains a read intercept for "agreements"; the
  stub key typo "agremments" is corrected for new anchors, old ones read as empty.
- SimulatedEntity: one vault, random UUIDs, per test entity.
- EntityAnchorAccessBoundaryTests: read-without-proof, wrong identity, scaffold
  admin (read, write, actions — on both the app and the cloud anchor), agreement
  grants exactly what it says, unsigned proposal, unknown purpose, direct write
  outside the batch path, first-persist genesis (unblocked from round 1), trace.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0166zoWBapoQ3R6iiJrhd2xx
MSG
  echo "commit: $(git rev-parse --short HEAD)"
  git push -u origin "$BRANCH" 2>&1 | tail -2
  echo "origin/$BRANCH: $(git ls-remote --heads origin "$BRANCH" | cut -c1-7)"
  if command -v gh >/dev/null; then
    gh pr create --draft --base main --head "$BRANCH" \
      --title "Entitetsdata runde 2: lesing og skriving krever entitetsbevis, hver endring etterlater spor" \
      --body "PDD_entitetsdata-egen-kontroll runde 2 (WP3–WP5). Se CellProtocolDocuments: Deliverables/PDD_entitetsdata-egen-kontroll_2026-09-08/TESTRESULT.md#runde2. Utkast for CI.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_0166zoWBapoQ3R6iiJrhd2xx" 2>&1 | tail -1
  fi
else
  echo "RØDT — committer IKKE. Se $FULL.new og $FULL.alle"
  grep -E "Test Case .* failed" "$FULL.alle" | head -20
  exit 1
fi
