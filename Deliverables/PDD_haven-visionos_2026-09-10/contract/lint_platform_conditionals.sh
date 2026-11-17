#!/bin/zsh
# Linter for plattformbetingelser (test.lint.platform-conditionals).
# Teller `#if os(` / `#elseif os(` per fil i Binding/Binding, Binding/Cells og CellProtocol/Sources/CellApple,
# og sammenligner mot platform_conditional_allowlist.txt. Feiler (exit 1) hvis en fil har flere enn tillatt,
# eller hvis en fil utenfor listen har noen. Formål: purpose://candidate.platform.capability-axis —
# nye UX-valg skal gå gjennom HavenHostCapabilities, ikke gjennom os(...).
#
#   lint_platform_conditionals.sh            kjør (cwd = HAVEN-roten)
#   lint_platform_conditionals.sh --update   skriv ny grunnlinje (bare i samme endring som en opprydding)
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ALLOW="$SCRIPT_DIR/platform_conditional_allowlist.txt"
HAVEN_ROOT="${HAVEN_ROOT:-$(pwd)}"
typeset -A allowed
while read -r line; do
  [[ -z "$line" || "$line" == \#* ]] && continue
  key="${line%%  *}"; n="${line##*  }"
  allowed[$key]=$n
done < "$ALLOW"
status=0
typeset -A seen
scan() {
  local repo="$1" dir="$2"
  [[ -d "$HAVEN_ROOT/$dir" ]] || { print "mangler: $HAVEN_ROOT/$dir"; status=2; return; }
  while IFS= read -r f; do
    local rel="${f#$HAVEN_ROOT/$repo/}"
    local key="$repo::$rel"
    local n
    n=$(grep -cE '^[[:space:]]*#(if|elseif)[[:space:]].*os\(' "$f" || true)
    [[ "$n" -eq 0 ]] && continue
    seen[$key]=1
    local lim="${allowed[$key]:-0}"
    if (( n > lim )); then
      print "FEIL  $key: $n os(-direktiver, tillatt $lim"
      status=1
    else
      print "ok    $key: $n/$lim"
    fi
  done < <(find "$HAVEN_ROOT/$dir" -name '*.swift' -type f | sort)
}
scan Binding Binding/Binding
scan Binding Binding/Cells
scan CellProtocol CellProtocol/Sources/CellApple
if [[ "${1:-}" == "--update" ]]; then
  print "(--update: skriv grunnlinjen manuelt fra utdataene over; automatisk skriving er med vilje ikke implementert)"
fi
exit $status
