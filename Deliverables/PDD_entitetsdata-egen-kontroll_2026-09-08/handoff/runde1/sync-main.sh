#!/bin/bash
# Fletter origin/main inn i pdd/entitetsdata-egen-kontroll i worktreet (ingen rebase, ingen force),
# bygger, kjører runde 1-testene + hele CellBaseTests, og pusher bare hvis alt er grønt.
set -uo pipefail
WT="${CELLPROTOCOL_WORKTREE:-$HOME/Build/Digipomps/HAVEN/CellProtocol-pdd-entitetsdata}"
BRANCH="pdd/entitetsdata-egen-kontroll"
HERE="$(cd "$(dirname "$0")" && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
FULL="$HERE/sync-$STAMP.full.log"
cd "$WT" || { echo "FEIL: worktree mangler"; exit 1; }
[ "$(git branch --show-current)" = "$BRANCH" ] || { echo "FEIL: feil branch"; exit 1; }
[ -z "$(git status --porcelain)" ] || { echo "FEIL: worktreet er skittent"; git status --short; exit 1; }
git fetch -q origin
echo "før:  HEAD $(git rev-parse --short HEAD) · origin/main $(git rev-parse --short origin/main) · bak $(git rev-list --count HEAD..origin/main)"
if [ "$(git rev-list --count HEAD..origin/main)" = "0" ]; then echo "allerede à jour"; else
  git merge --no-edit origin/main -m "Merge origin/main into $BRANCH (#45 database custody, matchfn)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0166zoWBapoQ3R6iiJrhd2xx" || { echo "MERGE FEILET"; git merge --abort; exit 1; }
fi
echo "etter: HEAD $(git rev-parse --short HEAD)"
echo "== swift build =="
swift build > "$FULL" 2>&1 && echo "Build: OK" || { echo "Build: FEILET"; grep -E "error:" "$FULL" | head -20; exit 1; }
echo "== runde 1-tester =="
swift test --filter 'EntityGenesisTests|EntityAnchorGenesisTests|IdentityLinkRegistryBindingTests' >> "$FULL" 2>&1
grep -E "Executed [0-9]+ tests" "$FULL" | tail -1
echo "== hele CellBaseTests =="
swift test --filter 'CellBaseTests' > "$FULL.alle" 2>&1
grep -E "Executed [0-9]+ tests" "$FULL.alle" | tail -1
FAILS=$(grep -cE "error: .*(failed|XCTAssert)|Test Case .* failed" "$FULL.alle" || true)
if grep -qE "Executed [0-9]+ tests, with 0 failures" "$FULL.alle"; then
  echo "== grønt — pusher =="
  git push origin "$BRANCH" 2>&1 | tail -3
  echo "origin/$BRANCH: $(git ls-remote --heads origin "$BRANCH" | cut -c1-7)"
else
  echo "RØDT ($FAILS) — pusher IKKE. Se $FULL.alle"; grep -E "Test Case .* failed" "$FULL.alle" | head -10
fi
