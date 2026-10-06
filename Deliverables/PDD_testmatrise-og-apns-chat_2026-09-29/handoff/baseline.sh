#!/bin/bash
# WP0: baseline av origin/main i tre repoer, målt i rene engangs-worktrees (aldri det delte arbeidstreet).
# Leser pinner fra CellScaffold sin egen Package.swift. Skriver INGENTING i Kjetils checkouts.
#   ./baseline.sh            tørrkjøring: viser revisjoner og hva som ville kjøres
#   ./baseline.sh --go       bygg + test, logg per repo; grønn-port leser siste «Executed»-linje
set -uo pipefail
MODE="${1:-}"
BASE="$HOME/Build/Digipomps/HAVEN"
CHECK="$HOME/Build/pdd-check"
HERE="$(cd "$(dirname "$0")" && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="$HERE/baseline-$STAMP"; mkdir -p "$OUT"
LOG="$OUT/baseline.log"
exec > >(tee "$LOG") 2>&1

git -C "$BASE/CellScaffold" fetch -q origin || { echo "FEIL: fetch CellScaffold"; exit 1; }
git -C "$BASE/CellProtocol" fetch -q origin || { echo "FEIL: fetch CellProtocol"; exit 1; }
git -C "$BASE/Binding" fetch -q origin || { echo "FEIL: fetch Binding"; exit 1; }
# Pinnene er versjonstagger («exact: "2026.9.4"») siden 26.09 — tidligere revisjoner. Les det som står der nå.
pin_from_scaffold() { git -C "$BASE/CellScaffold" show origin/main:Package.swift | grep -A3 "$1" | grep -oE 'exact: "[^"]+"' | head -1 | grep -oE '"[^"]+"' | tr -d '"'; }
CP_TAG="$(pin_from_scaffold CellProtocol.git)"; MINT_REV="$(pin_from_scaffold DiMyMint.git)"; MICRO_REV="$(pin_from_scaffold DiMyMicropayments.git)"
echo "origin/main: CellProtocol $(git -C "$BASE/CellProtocol" rev-parse --short origin/main) · CellScaffold $(git -C "$BASE/CellScaffold" rev-parse --short origin/main) · Binding $(git -C "$BASE/Binding" rev-parse --short origin/main)"
echo "pinner (tagger) fra CellScaffold: CellProtocol ${CP_TAG:-?} · DiMyMint ${MINT_REV:-?} · DiMyMicropayments ${MICRO_REV:-?}"
[ -n "$CP_TAG" ] && [ -n "$MINT_REV" ] && [ -n "$MICRO_REV" ] || { echo "FEIL: fant ikke pinnene i CellScaffold/Package.swift — stopper"; exit 1; }
echo "worktrees i $CHECK, logger i $OUT"
[ "$MODE" = "--go" ] || { echo "Tørrkjøring OK. Kjør med --go."; exit 0; }

ensure_worktree() { # repo target rev url
  local repo="$1" target="$2" rev="$3" url="$4"
  if [ -e "$target/.git" ] && ! git -C "$target" rev-parse --git-dir >/dev/null 2>&1; then
    # ødelagt worktree (peker på manglende git-dir): flytt til side, bygg på nytt
    mv "$target" "$target.defekt-$STAMP" && git -C "$BASE/$repo" worktree prune 2>/dev/null
    echo "  $repo: ødelagt worktree flyttet til $target.defekt-$STAMP"
  fi
  if [ -e "$target/.git" ]; then
    git -C "$target" reset -q --hard; git -C "$target" clean -qfd
    git -C "$target" fetch -q --tags origin
    git -C "$target" checkout -q --detach "$rev"
  elif [ -d "$BASE/$repo/.git" ]; then
    git -C "$BASE/$repo" fetch -q --tags origin; git -C "$BASE/$repo" worktree add -q --detach "$target" "$rev"
  else
    git clone -q "$url" "$target" && git -C "$target" checkout -q --detach "$rev"
  fi
  local got; got="$(git -C "$target" rev-parse --short HEAD)"; echo "  $repo står på $got"
}
mkdir -p "$CHECK"
CP_REV="$(git -C "$BASE/CellProtocol" rev-parse origin/main)"
ensure_worktree CellProtocol "$CHECK/CellProtocol" "$CP_REV" "https://github.com/Digipomps/CellProtocol.git"
# CellScaffold leveres mot den pinnede CellProtocol-taggen, ikke main: det er sannheten for «bygger det?».
# Katalogen MÅ hete CellProtocol (pakke-identiteten avledes av katalognavnet i DiMyMicropayments), derfor pinned/CellProtocol.
PINNED="$CHECK/pinned/CellProtocol"; mkdir -p "$CHECK/pinned"
if [ -e "$CHECK/CellProtocol-pinned/.git" ]; then git -C "$BASE/CellProtocol" worktree remove --force "$CHECK/CellProtocol-pinned" 2>/dev/null || mv "$CHECK/CellProtocol-pinned" "$CHECK/CellProtocol-pinned.gammel-$STAMP"; git -C "$BASE/CellProtocol" worktree prune; fi
[ -e "$PINNED/.git" ] || git -C "$BASE/CellProtocol" worktree add -q --detach "$PINNED" "$CP_TAG"
git -C "$PINNED" reset -q --hard; git -C "$PINNED" clean -qfd
git -C "$PINNED" fetch -q --tags origin; git -C "$PINNED" checkout -q --detach "$CP_TAG"
echo "  CellProtocol pinnet står på $(git -C "$PINNED" rev-parse --short HEAD) ($CP_TAG)"
ensure_worktree CellScaffold "$CHECK/CellScaffold" "origin/main" "https://github.com/Digipomps/CellScaffold.git"
ensure_worktree Binding "$CHECK/Binding" "origin/main" "https://github.com/Digipomps/Binding.git"
ensure_worktree DiMyMint "$CHECK/DiMyMint" "$MINT_REV" "git@github.com:DiMy-io/DiMyMint.git"
ensure_worktree DiMyMicropayments "$CHECK/DiMyMicropayments" "$MICRO_REV" "git@github.com:DiMy-io/DiMyMicropayments.git"
# Søsken-pakkene må ligge ved siden av den pinnede CellProtocol (samme katalog), ellers peker de på main-utgaven.
ensure_worktree DiMyMint "$CHECK/pinned/DiMyMint" "$MINT_REV" "$CHECK/DiMyMint" 2>/dev/null || true
ensure_worktree DiMyMicropayments "$CHECK/pinned/DiMyMicropayments" "$MICRO_REV" "$CHECK/DiMyMicropayments" 2>/dev/null || true
# Avvikende revisjon stopper kjøringen (lesson.disposable-worktree-must-be-reset-before-checkout)
[ "$(git -C "$CHECK/CellProtocol" rev-parse HEAD)" = "$CP_REV" ] || { echo "FEIL: CellProtocol-worktree står ikke på origin/main — stopper"; exit 1; }

last_executed() { grep -E "Executed [0-9]+ tests" "$1" | tail -1; }   # siste linje teller
bundle_line() { sed 's/\x1b\[[0-9;]*m//g' "$1" | grep -A1 -E "^Test Suite '$2\.xctest' (passed|failed)" | grep -E "Executed [0-9]+ tests" | tail -1; }   # swift test kjører flere bundler; AppTests er den som teller for CellScaffold
green() { case "$1" in *" 0 failures (0 unexpected)"*) echo GRØNN;; "") echo INGEN-LINJE;; *) echo RØD;; esac; }

echo "== 1. CellProtocol: build + CellBaseTests =="
( cd "$CHECK/CellProtocol" && swift build > "$OUT/cellprotocol-build.log" 2>&1 && echo "build: OK" || echo "build: FEILET (se cellprotocol-build.log)" )
( cd "$CHECK/CellProtocol" && swift test --filter CellBaseTests > "$OUT/cellprotocol-test.log" 2>&1 )
L="$(last_executed "$OUT/cellprotocol-test.log")"; echo "siste linje: [$L] → $(green "$L")"

echo "== 2a. CellScaffold: build + full test mot pinnet CellProtocol $CP_TAG (release-sannheten) =="
export DIMYMINT_LOCAL_PACKAGE_PATH="$CHECK/pinned/DiMyMint" DIMYMICROPAYMENTS_LOCAL_PACKAGE_PATH="$CHECK/pinned/DiMyMicropayments"
export CELLPROTOCOL_LOCAL_PACKAGE_PATH="$PINNED"
( cd "$CHECK/CellScaffold" && swift build > "$OUT/cellscaffold-pinned-build.log" 2>&1 && echo "build: OK" || echo "build: FEILET (se cellscaffold-pinned-build.log)" )
( cd "$CHECK/CellScaffold" && swift test > "$OUT/cellscaffold-pinned-test.log" 2>&1 )
L="$(bundle_line "$OUT/cellscaffold-pinned-test.log" AppTests)"; echo "AppTests-linje: [$L] → $(green "$L")"
grep -E "Test Case .* failed" "$OUT/cellscaffold-pinned-test.log" | sed 's/\x1b\[[0-9;]*m//g' | sort -u | head -20
echo "== 2b. CellScaffold build mot CellProtocol main (kompatibilitet; avvik her er ikke et release-brudd) =="
export CELLPROTOCOL_LOCAL_PACKAGE_PATH="$CHECK/CellProtocol" DIMYMINT_LOCAL_PACKAGE_PATH="$CHECK/DiMyMint" DIMYMICROPAYMENTS_LOCAL_PACKAGE_PATH="$CHECK/DiMyMicropayments"
( cd "$CHECK/CellScaffold" && swift build > "$OUT/cellscaffold-main-build.log" 2>&1 && echo "build: OK" || { echo "build: FEILET (se cellscaffold-main-build.log)"; sed 's/\x1b\[[0-9;]*m//g' "$OUT/cellscaffold-main-build.log" | grep -E "error:" | grep -v "failed with a nonzero" | sort -u | head -10; } )

echo "== 3. Binding: build (macOS) =="
( cd "$CHECK/Binding" && xcodebuild -project Binding.xcodeproj -scheme HAVEN -destination 'platform=macOS' -derivedDataPath "$CHECK/DerivedData" CODE_SIGNING_ALLOWED=NO build > "$OUT/binding-build.log" 2>&1; grep -E "\*\* BUILD" "$OUT/binding-build.log" | tail -1 )
echo "== ferdig. Rødt kjøres tre ganger før noe konkluderes (lesson.a-new-red-test-needs-a-repeated-baseline). Logger: $OUT =="
