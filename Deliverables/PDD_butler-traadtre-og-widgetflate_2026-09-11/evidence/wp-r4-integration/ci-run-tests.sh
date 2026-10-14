#!/usr/bin/env bash
# Kjører ci/test-filter.txt i bolker, én swift test-prosess per bolk.
# XCTest på Linux kjører alt i én prosess; hele listen i ett jafs blir
# drept stille sent i kjøringen. Bolker gir hver del en fersk heap.
set -euo pipefail
cd "$(dirname "$0")/.."

TEST_FILTER="${CI_TEST_FILTER_PATH:-ci/test-filter.txt}"
SWIFT_BIN="${CI_SWIFT_BIN:-swift}"
JOBS="${CI_TEST_JOBS:-2}"

if grep -Eq '^[[:space:]]*AdminEntryRemoteBridgeLoopbackTests([[:space:]]*(#.*)?)?$' "$TEST_FILTER"; then
  echo "::group::bygger AdminScaffold for loopback-test"
  "$SWIFT_BIN" build --force-resolved-versions --jobs "$JOBS" --product AdminScaffold
  ADMIN_SCAFFOLD_BIN_PATH="$("$SWIFT_BIN" build --show-bin-path --force-resolved-versions)"
  ADMIN_SCAFFOLD_TEST_BINARY="$ADMIN_SCAFFOLD_BIN_PATH/AdminScaffold"
  if [ ! -x "$ADMIN_SCAFFOLD_TEST_BINARY" ]; then
    echo "::error::AdminScaffold-produktet finnes ikke som kjørbar fil på SwiftPMs rapporterte binærsti"
    exit 1
  fi
  export ADMIN_SCAFFOLD_TEST_BINARY
  echo "::endgroup::"
fi

# Enkelttester som hoppes over, se ci/test-skips.txt for grunnene.
SKIP_ARGS=()
if [ -f ci/test-skips.txt ]; then
  while IFS= read -r s; do
    s="${s%%#*}"; s="$(echo "$s" | xargs)"
    [ -n "$s" ] && SKIP_ARGS+=(--skip "$s")
  done < ci/test-skips.txt
  [ ${#SKIP_ARGS[@]} -gt 0 ] && echo "hopper over ${#SKIP_ARGS[@]} enkelttester (ci/test-skips.txt)"
fi

CHUNK="${CI_TEST_CHUNK_SIZE:-20}"
# En linje med bare --- tvinger et gruppeskille. Brukes når en suite må
# kjøre i sin egen prosess fordi den er ordensavhengig.
groups=(); cur=()
while IFS= read -r line; do
  case "$line" in
    '---') [ ${#cur[@]} -gt 0 ] && groups+=("$(IFS='|'; echo "${cur[*]}")") && cur=() ;;
    ''|'#'*) ;;
    *) cur+=("$line")
       if [ ${#cur[@]} -ge "$CHUNK" ]; then
         groups+=("$(IFS='|'; echo "${cur[*]}")"); cur=()
       fi ;;
  esac
done < "$TEST_FILTER"
[ ${#cur[@]} -gt 0 ] && groups+=("$(IFS='|'; echo "${cur[*]}")")
TOTAL=${#groups[@]}
echo "bolker: $TOTAL | maks bolkstørrelse: $CHUNK"
LOGDIR="${CI_TEST_LOGDIR:-$(mktemp -d)}"
mkdir -p "$LOGDIR"
failed=(); n=0
for expr in "${groups[@]}"; do
  n=$((n+1))
  log="$LOGDIR/bolk-$n.log"
  echo "::group::bolk $n av $TOTAL"
  echo "$expr" | tr '|' '\n' | sed 's/^/  /'
  if "$SWIFT_BIN" test --force-resolved-versions --jobs "$JOBS" "${SKIP_ARGS[@]+"${SKIP_ARGS[@]}"}" --filter "$expr" 2>&1 | tee "$log"; then
    echo "bolk $n OK"
    echo "::endgroup::"
  else
    echo "bolk $n FEILET"
    # Lukk gruppen FØR feildetaljene. Alt inne i ::group:: er kollapset i
    # GitHubs logg, og en feil ingen ser er en feil ingen retter.
    echo "::endgroup::"
    failed+=("$n")
    echo "::error title=bolk $n av $TOTAL feilet::se testene og feillinjene under"
    echo "── bolk $n av $TOTAL: testene i bolken ──"
    echo "$expr" | tr '|' '\n' | sed 's/^/    /'
    echo "── bolk $n av $TOTAL: feillinjer ──"
    if ! grep -E "(^error:|\.swift:[0-9]+(:[0-9]+)?: error:|Fatal error|XCTAssert|Test Case .* failed|Test Suite .* failed)" "$log" | tail -60; then
      echo "    (ingen gjenkjennelige feillinjer — siste 40 linjer av bolken:)"
      tail -40 "$log" | sed 's/^/    /'
    fi
  fi
done
if [ ${#failed[@]} -gt 0 ]; then
  # Tallene er BOLKNUMRE, ikke et antall. Skriv det slik at ingen leser
  # "FEILENDE BOLKER: 7" som "sju bolker feilet".
  echo "RESULTAT: ${#failed[@]} av $TOTAL bolker feilet (bolknummer: ${failed[*]})"
  for f in "${failed[@]}"; do
    echo "  bolk $f inneholdt:"
    echo "${groups[$((f-1))]}" | tr '|' '\n' | sed 's/^/    /'
  done
  echo "::error title=Focused Swift gates::${#failed[@]} av $TOTAL bolker feilet — bolknummer ${failed[*]}"
  exit 1
fi
echo "alle $n bolker grønne"
