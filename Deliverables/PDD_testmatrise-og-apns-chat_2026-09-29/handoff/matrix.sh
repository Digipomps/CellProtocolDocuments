#!/bin/bash
# WP10: kjører (eller viser) enhetsprofilene. Profil = data i profiles/*.json. Tørrkjøring er standard.
#   ./matrix.sh            viser profiler og om de kan kjøres her
#   ./matrix.sh --go       bygger hver profil som kan kjøres, logger per profil i matrix-<stamp>/
set -uo pipefail
MODE="${1:-}"
HERE="$(cd "$(dirname "$0")" && pwd)"
CHECK="$HOME/Build/pdd-check"
BINDING="$CHECK/Binding"
STAMP="$(date +%Y%m%d-%H%M%S)"; OUT="$HERE/matrix-$STAMP"; mkdir -p "$OUT"
exec > >(tee "$OUT/matrix.log") 2>&1
PY=""; for c in /usr/bin/python3 /opt/homebrew/bin/python3 python3; do "$c" -c 'import sys' >/dev/null 2>&1 && { PY="$c"; break; }; done
[ -n "$PY" ] || { echo "FEIL: ingen fungerende python"; exit 1; }
SIMS="$(xcrun simctl list devices available 2>/dev/null)"
for f in "$HERE"/profiles/*.json; do
  name="$("$PY" -c 'import json,sys;print(json.load(open(sys.argv[1]))["profile"])' "$f")"
  dest="$("$PY" -c 'import json,sys;print(json.load(open(sys.argv[1]))["destination"])' "$f")"
  case "$name" in
    ios-sim-iphone) have=$(echo "$SIMS" | grep -c "iPhone") ;;
    ios-sim-ipad)   have=$(echo "$SIMS" | grep -c "iPad") ;;
    *)              have=1 ;;
  esac
  [ "$have" -gt 0 ] && status="kan kjøres her" || status="IKKE tilgjengelig (ingen slik simulator)"
  echo "== $name · $dest · $status"
  [ "$MODE" = "--go" ] || continue
  [ "$have" -gt 0 ] || { echo "   hoppet over"; continue; }
  case "$name" in
    linux-client)
      ( cd "$CHECK/impl/CellProtocol" 2>/dev/null && swift test --filter "HavenInvite|HavenPush" > "$OUT/$name.log" 2>&1 ) || echo "   (impl/CellProtocol mangler eller testene feilet — se logg)"
      L="$(grep -E "Executed [0-9]+ tests" "$OUT/$name.log" 2>/dev/null | tail -1)"; echo "   siste linje: [$L]" ;;
    *)
      ( cd "$BINDING" && xcodebuild -project Binding.xcodeproj -scheme HAVEN -destination "$dest" -derivedDataPath "$CHECK/DerivedData-$name" CODE_SIGNING_ALLOWED=NO build > "$OUT/$name.log" 2>&1 )
      echo "   $(grep -E '\*\* BUILD' "$OUT/$name.log" | tail -1)" ;;
  esac
done
echo "== ferdig. Logger: $OUT. Ekte iPhone: se iphone-sjekkliste.md =="
