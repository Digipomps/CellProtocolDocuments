#!/bin/bash
set -uo pipefail
BASE="$HOME/Build/Digipomps/HAVEN"
WT="${CELLPROTOCOL_WORKTREE:-$BASE/CellProtocol-pdd-entitetsdata}"
CHECK="$HOME/Build/pdd-check"
HERE="$(cd "$(dirname "$0")" && pwd)"
LOG="$HERE/downstream-$(date +%Y%m%d-%H%M%S).log"
REV="$(git -C "$WT" rev-parse HEAD)"
BASEREV="$(git -C "$WT" rev-parse origin/main)"
MINT_REV="1718fda4ee8185cf3f848edc0b0b966543d834cf"
MICRO_REV="bc6f359c83f1af73f2509478981d919d5ee9292b"
echo "logg: $LOG"

ensure_worktree() {
  local repo="$1" target="$2" rev="$3" url="$4"
  if [ -d "$target/.git" ] || [ -f "$target/.git" ]; then
    git -C "$target" checkout -q --detach "$rev" 2>/dev/null || { git -C "$target" fetch -q origin && git -C "$target" checkout -q --detach "$rev"; }
  elif [ -d "$BASE/$repo/.git" ]; then
    git -C "$BASE/$repo" fetch -q origin
    git -C "$BASE/$repo" worktree add --detach "$target" "$rev"
  else
    git clone -q "$url" "$target" && git -C "$target" checkout -q --detach "$rev"
  fi
  echo "$repo @ $(git -C "$target" rev-parse --short HEAD)"
}

point_binding_at_local_cellprotocol() {
  local f="$CHECK/Binding/Binding.xcodeproj/project.pbxproj"
  if grep -q 'relativePath = ../CellProtocol;' "$f"; then
    echo "pbxproj: peker allerede paa ../CellProtocol"
    return
  fi
  /usr/bin/perl -0pi -e 's|\t\t24FEA0022F4203AB000334E1 /\* XCRemoteSwiftPackageReference "CellProtocol" \*/ = \{\n\t\t\tisa = XCRemoteSwiftPackageReference;\n\t\t\trepositoryURL = "https://github.com/Digipomps/CellProtocol.git";\n\t\t\trequirement = \{\n\t\t\t\tkind = revision;\n\t\t\t\trevision = [0-9a-f]+;\n\t\t\t\};\n\t\t\};\n|\t\t24FEA0022F4203AB000334E1 /* XCLocalSwiftPackageReference "../CellProtocol" */ = {\n\t\t\tisa = XCLocalSwiftPackageReference;\n\t\t\trelativePath = ../CellProtocol;\n\t\t};\n|' "$f"
  if grep -q 'relativePath = ../CellProtocol;' "$f"; then
    echo "pbxproj: CellProtocol -> ../CellProtocol (lokal worktree)"
  else
    echo "pbxproj: FEIL - fikk ikke byttet referansen. Binding-bygget vil bruke GitHub-pinnen, ikke endringen."
  fi
}

build_cellscaffold() {
  ( cd "$CHECK/CellScaffold" && \
    CELLPROTOCOL_LOCAL_PACKAGE_PATH="$CHECK/CellProtocol" \
    DIMYMINT_LOCAL_PACKAGE_PATH="$CHECK/DiMyMint" \
    DIMYMICROPAYMENTS_LOCAL_PACKAGE_PATH="$CHECK/DiMyMicropayments" \
    swift build 2>&1 | grep -E "error:|Build complete|Build failed" | sed 's/\x1b\[[0-9;]*m//g' | sort -u | tail -15 )
}

build_binding() {
  ( cd "$CHECK/Binding" && xcodebuild -project Binding.xcodeproj -scheme HAVEN -destination 'platform=macOS' \
      -derivedDataPath "$CHECK/DerivedData" CODE_SIGNING_ALLOWED=NO build 2>&1 \
    | grep -E "error:|\*\* BUILD" | sed 's/\x1b\[[0-9;]*m//g' | sort -u | tail -15 )
}

{
  echo "== worktrees i $CHECK =="
  mkdir -p "$CHECK"
  ensure_worktree CellProtocol "$CHECK/CellProtocol" "$BASEREV" "https://github.com/Digipomps/CellProtocol.git"
  ensure_worktree CellScaffold "$CHECK/CellScaffold" "origin/main" "https://github.com/Digipomps/CellScaffold.git"
  ensure_worktree Binding "$CHECK/Binding" "origin/main" "https://github.com/Digipomps/Binding.git"
  ensure_worktree DiMyMint "$CHECK/DiMyMint" "$MINT_REV" "git@github.com:DiMy-io/DiMyMint.git"
  ensure_worktree DiMyMicropayments "$CHECK/DiMyMicropayments" "$MICRO_REV" "git@github.com:DiMy-io/DiMyMicropayments.git"
  point_binding_at_local_cellprotocol
  echo "== pakkene som faktisk brukes =="
  ls -d "$CHECK"/* | sed "s#$CHECK/#  #"

  SKIP_SCAFFOLD="${1:-}"
  echo "== BASELINE: CellProtocol @ origin/main ($BASEREV) =="
  [ "$SKIP_SCAFFOLD" = "--binding-only" ] || { echo "-- CellScaffold --"; build_cellscaffold; }
  echo "-- Binding --"; build_binding

  echo "== ENDRINGEN: CellProtocol @ $REV =="
  git -C "$CHECK/CellProtocol" checkout -q --detach "$REV"
  [ "$SKIP_SCAFFOLD" = "--binding-only" ] || { echo "-- CellScaffold --"; build_cellscaffold; }
  echo "-- Binding --"; build_binding
} 2>&1 | tee "$LOG"
echo
echo "Sammenlign BASELINE mot ENDRINGEN. Er baseline rod, er det ikke denne patchen (lesson.a-red-baseline-is-a-question-not-an-answer)."
