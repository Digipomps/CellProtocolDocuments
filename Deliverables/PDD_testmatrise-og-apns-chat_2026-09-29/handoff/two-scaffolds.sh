#!/bin/bash
# WP6: to (eller tre) lokale scaffold-instanser side om side, hver med egen port, egen arbeidsmappe, egen SQLite og egne hemmeligheter.
# Tørrkjøring er standard. Rører ikke Kjetils checkout: bruker bygget i impl/CellScaffold (WP1–WP3) eller den katalogen du oppgir.
#   ./two-scaffolds.sh                 tørrkjøring: viser hva som ville startet
#   ./two-scaffolds.sh start [N]       start N instanser (standard 2, maks 3) på 8181, 8182, 8183
#   ./two-scaffolds.sh probe           GET mot hver (helse), skriver svar og skiller instansene
#   ./two-scaffolds.sh stop            stopp via PID-filer (kun våre egne)
#   SCAFFOLD_DIR=/sti ./two-scaffolds.sh start     bruk annen CellScaffold-katalog (må være bygget med swift build)
set -uo pipefail
CMD="${1:-dry}"; N="${2:-2}"; [ "$N" -le 3 ] 2>/dev/null || N=3
CHECK="$HOME/Build/pdd-check"
SC="${SCAFFOLD_DIR:-$CHECK/impl/CellScaffold}"
RUN="$CHECK/instances"; mkdir -p "$RUN"
BASEPORT=8181
export CELLPROTOCOL_LOCAL_PACKAGE_PATH="${CELLPROTOCOL_LOCAL_PACKAGE_PATH:-$CHECK/impl/CellProtocol}" DIMYMINT_LOCAL_PACKAGE_PATH="${DIMYMINT_LOCAL_PACKAGE_PATH:-$CHECK/impl/DiMyMint}" DIMYMICROPAYMENTS_LOCAL_PACKAGE_PATH="${DIMYMICROPAYMENTS_LOCAL_PACKAGE_PATH:-$CHECK/impl/DiMyMicropayments}"
BIN="$SC/.build/debug/Run"

rand() { /usr/bin/openssl rand -hex 24; }

case "$CMD" in
  dry)
    echo "scaffold: $SC  (binær: $BIN — finnes: $([ -x "$BIN" ] && echo ja || echo nei))"
    for i in $(seq 1 "$N"); do p=$((BASEPORT+i-1)); echo "  instans $i: port $p, arbeidsmappe $RUN/s$i, db $RUN/s$i/db.sqlite"; done
    echo "Tørrkjøring OK. Kjør «start»."
    ;;
  start)
    [ -x "$BIN" ] || { echo "FEIL: $BIN mangler — kjør apply-phase2.sh først (eller swift build i $SC)"; exit 1; }
    for i in $(seq 1 "$N"); do
      p=$((BASEPORT+i-1)); d="$RUN/s$i"; mkdir -p "$d"
      if [ -f "$d/pid" ] && kill -0 "$(cat "$d/pid")" 2>/dev/null; then echo "instans $i kjører allerede (pid $(cat "$d/pid"))"; continue; fi
      [ -f "$d/env" ] || { printf 'JWT_AUTH_SECRET=%s\nCHAT_MVP_TOKEN_SECRET=%s\n' "$(rand)" "$(rand)" > "$d/env"; chmod 600 "$d/env"; }
      ( cd "$d" && set -a && . ./env && set +a && \
        SQLITE_DATABASE_PATH="$d/db.sqlite" RP_ID=localhost RP_ORIGIN="http://localhost:$p" RP_DISPLAY_NAME="PDD s$i" \
        nohup "$BIN" serve --hostname 127.0.0.1 --port "$p" > "$d/scaffold.log" 2>&1 & echo $! > "$d/pid" )
      echo "instans $i startet: port $p, pid $(cat "$d/pid"), logg $d/scaffold.log"
    done
    sleep 8
    "$0" probe "$N"
    ;;
  probe)
    for i in $(seq 1 "$N"); do
      p=$((BASEPORT+i-1)); d="$RUN/s$i"
      code="$(/usr/bin/curl -s -o "$d/probe.body" -w '%{http_code}' --max-time 5 "http://127.0.0.1:$p/" 2>/dev/null)"
      echo "instans $i  http://127.0.0.1:$p/  → HTTP ${code:-ingen}  pid $(cat "$d/pid" 2>/dev/null || echo -)  db $( [ -f "$d/db.sqlite" ] && echo finnes || echo mangler )"
    done
    echo "distinkte databaser: $(ls "$RUN"/s*/db.sqlite 2>/dev/null | wc -l | tr -d ' ') · distinkte hemmeligheter: $(cat "$RUN"/s*/env 2>/dev/null | grep JWT_AUTH_SECRET | sort -u | wc -l | tr -d ' ')"
    ;;
  stop)
    for d in "$RUN"/s*; do
      [ -f "$d/pid" ] || continue
      pid="$(cat "$d/pid")"
      if kill -0 "$pid" 2>/dev/null; then kill "$pid" && echo "stoppet $d (pid $pid)"; else echo "$d: ikke i gang"; fi
      mv "$d/pid" "$d/pid.stoppet"
    done
    ;;
  *) echo "ukjent kommando: $CMD"; exit 2 ;;
esac
