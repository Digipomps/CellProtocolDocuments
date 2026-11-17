#!/bin/bash
# Forbereder WP0 og WP-S1 på macOS: worktree for WP-S1 + baseline detached. Tørrkjøring uten --run.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
find_root() { local d="$1"; while [ "$d" != "/" ]; do if [ -d "$d/CellScaffold" ] && [ -d "$d/_losen-queue" ]; then printf '%s' "$d"; return 0; fi; d="$(dirname "$d")"; done; return 1; }
ROOT="$(find_root "$HERE")" || { echo "fant ikke HAVEN-roten over $HERE (trenger CellScaffold/ og _losen-queue/)"; exit 2; }
PDD_DIR="$ROOT/CellProtocolDocuments/Deliverables/PDD_correspondence-varsel-hendelsesbasert_2026-09-12"
WT="$ROOT/_worktrees/cellscaffold-corr-varsel-s1"
RUN=0; [ "${1:-}" = "--run" ] && RUN=1
echo "ROOT=$ROOT"
echo "1) git -C $ROOT/CellScaffold fetch origin main && git -C $ROOT/CellScaffold worktree add $WT -b pdd/corr-varsel-recipient-feed origin/main"
echo "2) nohup bash $PDD_DIR/evidence/wp0/baseline.sh --run > /dev/null 2>&1 &"
echo "3) cp $PDD_DIR/handoff/wp-s1-recipient-feed.prompt.md $PDD_DIR/handoff/wp-s1-recipient-feed.job $ROOT/_losen-queue/inbox/"
[ "$RUN" -eq 1 ] || { echo "TØRRKJØRING — legg til --run"; exit 0; }
git -C "$ROOT/CellScaffold" fetch origin main
if [ ! -d "$WT" ]; then git -C "$ROOT/CellScaffold" worktree add "$WT" -b pdd/corr-varsel-recipient-feed origin/main; fi
nohup bash "$PDD_DIR/evidence/wp0/baseline.sh" --run > /dev/null 2>&1 &
cp "$PDD_DIR/handoff/wp-s1-recipient-feed.prompt.md" "$PDD_DIR/handoff/wp-s1-recipient-feed.job" "$ROOT/_losen-queue/inbox/"
echo "FERDIG: worktree $WT, baseline startet detached, WP-S1 lagt i køen"
