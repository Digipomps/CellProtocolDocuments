#!/bin/bash
# Kontroll: CellScaffold origin/main + KUN try-rettelsene, bygget mot CellProtocol main (impl/CellProtocol minus våre filer er ikke nødvendig:
# vi bruker en ren CellProtocol main-worktree $CHECK/CellProtocol fra baseline). Svarer på: er de røde i fase 2 våre, eller kommer de av CellProtocol main?
set -uo pipefail
MODE="${1:-}"
BASE="$HOME/Build/Digipomps/HAVEN"; CHECK="$HOME/Build/pdd-check"
HERE="$(cd "$(dirname "$0")" && pwd)"
WT="$CHECK/control/CellScaffold"; mkdir -p "$CHECK/control"
OUT="$HERE/run-ctl-$(date +%Y%m%d-%H%M%S)"; mkdir -p "$OUT"
exec > >(tee "$OUT/apply.log") 2>&1
echo "kontroll i $WT: origin/main + try-rettelser, mot ren CellProtocol main ($CHECK/CellProtocol)"
[ "$MODE" = "--go" ] || { echo "Tørrkjøring OK. Kjør med --go."; exit 0; }
for r in DiMyMint DiMyMicropayments; do
  if [ ! -e "$CHECK/control/$r/.git" ]; then
    rev="$(git -C "$CHECK/pinned/$r" rev-parse HEAD)" || exit 1
    git clone -q "$CHECK/pinned/$r" "$CHECK/control/$r" && git -C "$CHECK/control/$r" checkout -q --detach "$rev"
  fi
done
if [ ! -e "$CHECK/control/CellProtocol/.git" ]; then
  git -C "$BASE/CellProtocol" fetch -q origin; git -C "$BASE/CellProtocol" worktree add -q --detach "$CHECK/control/CellProtocol" origin/main || exit 1
fi
git -C "$CHECK/control/CellProtocol" reset -q --hard; git -C "$CHECK/control/CellProtocol" clean -qfd; git -C "$CHECK/control/CellProtocol" checkout -q --detach origin/main
echo "  CellProtocol main: $(git -C "$CHECK/control/CellProtocol" rev-parse --short HEAD)"
git -C "$BASE/CellScaffold" fetch -q origin
if [ -e "$WT/.git" ]; then git -C "$WT" reset -q --hard; git -C "$WT" clean -qfd; git -C "$WT" checkout -q --detach origin/main
else git -C "$BASE/CellScaffold" worktree add -q --detach "$WT" origin/main || exit 1; fi
echo "  CellScaffold: $(git -C "$WT" rev-parse --short HEAD)"
sed -i '' 's/^        await underlying.sendData(data)$/        try await underlying.sendData(data)/' "$WT/Sources/App/Controllers/VaporPersonEntityReadRoute.swift"
sed -i '' 's/^        await transport.sendData(data)$/        try await transport.sendData(data)/' "$WT/Tests/AppTests/EntityPersonBridgeProcessTests.swift"
git -C "$WT" status --short
export CELLPROTOCOL_LOCAL_PACKAGE_PATH="$CHECK/control/CellProtocol" DIMYMINT_LOCAL_PACKAGE_PATH="$CHECK/control/DiMyMint" DIMYMICROPAYMENTS_LOCAL_PACKAGE_PATH="$CHECK/control/DiMyMicropayments"
bundle_line() { sed 's/\x1b\[[0-9;]*m//g' "$1" | grep -A1 -E "^Test Suite '$2\.xctest' (passed|failed)" | grep -E "Executed [0-9]+ tests" | tail -1; }
( cd "$WT" && swift build > "$OUT/build.log" 2>&1 && echo "build: OK" || echo "build: FEILET (se build.log)" )
( cd "$WT" && swift test > "$OUT/test-all.log" 2>&1 )
L="$(bundle_line "$OUT/test-all.log" AppTests)"; echo "AppTests-linje: [$L]"
[ -n "$L" ] || { echo "TESTENE KOMPILERTE/KJØRTE IKKE"; exit 1; }
sed 's/\x1b\[[0-9;]*m//g' "$OUT/test-all.log" | grep -E "Test Case .* failed" | sed -E "s/^Test Case '-\[([^ ]+) ([^]]+)\]' failed.*/\1.\2/" | sort -u > "$HERE/../baseline-failures-cpmain.txt"
echo "røde tester (kontroll, CellProtocol main): $(wc -l < "$HERE/../baseline-failures-cpmain.txt")"
echo "ikke i pinnet baseline (følger av CellProtocol main):"; comm -13 "$HERE/../baseline-failures-pinned.txt" "$HERE/../baseline-failures-cpmain.txt"
echo "logger: $OUT"
