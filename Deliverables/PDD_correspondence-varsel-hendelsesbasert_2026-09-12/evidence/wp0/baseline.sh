#!/bin/bash
# WP0 — baseline på ren eksport av origin/main (HavenAgentD, CellScaffold).
# Kjøres på macOS. Standard er tørrkjøring; --run utfører. Idempotent: eksporten lages på nytt hver gang.
# HAVEN-roten utledes fra skriptets plassering (CellProtocolDocuments/Deliverables/<pdd>/evidence/wp0/).
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
find_root() { local d="$1"; while [ "$d" != "/" ]; do if [ -d "$d/CellScaffold" ] && [ -d "$d/_losen-queue" ]; then printf '%s' "$d"; return 0; fi; d="$(dirname "$d")"; done; return 1; }
ROOT="$(find_root "$HERE")" || { echo "fant ikke HAVEN-roten over $HERE (trenger CellScaffold/ og _losen-queue/)"; exit 2; }
STAMP="$(date +%Y%m%dT%H%M%S)"
SCRATCH="$ROOT/_worktrees/baseline-corr-varsel-$STAMP"
LOG="$HERE/baseline-$STAMP.log"
SUMMARY="$HERE/SUMMARY-$STAMP.md"
RUN=0; KEEP=0
for a in "$@"; do case "$a" in --run) RUN=1 ;; --keep) KEEP=1 ;; esac; done
say() { printf '%s %s\n' "$(date -u +%FT%TZ)" "$*" | tee -a "$LOG"; }
say "ROOT=$ROOT SCRATCH=$SCRATCH RUN=$RUN"
for r in HavenAgentD CellScaffold; do [ -d "$ROOT/$r/.git" ] || { say "mangler repo: $ROOT/$r"; exit 2; }; done
if [ "$RUN" -ne 1 ]; then
  say "TØRRKJØRING: ville hentet origin/main i HavenAgentD og CellScaffold, eksportert med git archive til $SCRATCH, kjørt swift build/test i HavenAgentD (fullt) og CellScaffold (--filter AssistantCorrespondenceCellTests), og skrevet $SUMMARY"
  exit 0
fi
mkdir -p "$SCRATCH"
{
  echo "# WP0 baseline $STAMP"
  echo
  echo "ROOT: $ROOT"
} > "$SUMMARY"
for r in HavenAgentD CellScaffold; do
  say "== $r: fetch + archive =="
  git -C "$ROOT/$r" fetch origin main >>"$LOG" 2>&1 || { say "$r: fetch feilet (nett?) — bruker lokal origin/main-ref"; }
  SHA="$(git -C "$ROOT/$r" rev-parse --short origin/main)"
  mkdir -p "$SCRATCH/$r"
  git -C "$ROOT/$r" archive origin/main | tar -x -C "$SCRATCH/$r"
  echo "- $r origin/main = $SHA (eksportert til $SCRATCH/$r)" >> "$SUMMARY"
done
say "== HavenAgentD: swift build =="
( cd "$SCRATCH/HavenAgentD" && swift build >>"$LOG" 2>&1 ); BUILD_A=$?
echo "- HavenAgentD swift build exit=$BUILD_A" >> "$SUMMARY"
say "== HavenAgentD: swift test (exitkoden lyver i dette repoet; les Test run-linjen) =="
( cd "$SCRATCH/HavenAgentD" && swift test >>"$LOG" 2>&1 ); TEST_A=$?
TESTLINE_A="$(grep -E 'Test run with [0-9]+ tests' "$LOG" | tail -1)"
echo "- HavenAgentD swift test exit=$TEST_A; ${TESTLINE_A:-ingen Test run-linje funnet}" >> "$SUMMARY"
say "== HavenAgentD: preflight_before_landing + assert_dependencies_are_on_their_main (fra eksporten av origin/main; den lokale utsjekken kan staa paa en annen gren) =="
( cd "$SCRATCH/HavenAgentD" && bash Scripts/preflight_before_landing.sh >>"$LOG" 2>&1 ); PRE_A=$?
( cd "$SCRATCH/HavenAgentD" && bash Scripts/assert_dependencies_are_on_their_main.sh >>"$LOG" 2>&1 ); DEP_A=$?
echo "- HavenAgentD preflight_before_landing exit=$PRE_A; assert_dependencies_are_on_their_main exit=$DEP_A" >> "$SUMMARY"
say "== CellScaffold: swift build =="
( cd "$SCRATCH/CellScaffold" && swift build >>"$LOG" 2>&1 ); BUILD_S=$?
echo "- CellScaffold swift build exit=$BUILD_S" >> "$SUMMARY"
say "== CellScaffold: swift test --filter AssistantCorrespondenceCellTests =="
( cd "$SCRATCH/CellScaffold" && swift test --filter AssistantCorrespondenceCellTests >>"$LOG" 2>&1 ); TEST_S=$?
TESTLINE_S="$(grep -E 'Executed [0-9]+ tests, with' "$LOG" | tail -1)"; [ -z "$TESTLINE_S" ] && TESTLINE_S="$(grep -E 'Test run with [0-9]+ tests' "$LOG" | tail -1)"
echo "- CellScaffold filtrert test exit=$TEST_S; ${TESTLINE_S:-ingen testlinje funnet}" >> "$SUMMARY"
echo >> "$SUMMARY"; echo "Logg: $LOG" >> "$SUMMARY"
if [ "$KEEP" -eq 1 ]; then
  echo "- Eksporten er beholdt (--keep): $SCRATCH — husk at .build-mappene tar ~11 GB" >> "$SUMMARY"
else
  rm -rf "$SCRATCH"
  echo "- Eksporten er slettet etter kjøring (bygg-mappene tok ~11 GB sist); loggen over er beviset" >> "$SUMMARY"
fi
say "FERDIG — se $SUMMARY"
