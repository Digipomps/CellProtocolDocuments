#!/bin/bash
# Fase 1 (WP1): InviteApnsPush + tester, i en engangs-worktree på egen gren. Rører ikke Kjetils checkout.
#   ./apply-phase1.sh        tørrkjøring: viser hva som ville skje
#   ./apply-phase1.sh --go   lag worktree/gren, legg inn filene, bygg og kjør testene
set -uo pipefail
MODE="${1:-}"
BASE="$HOME/Build/Digipomps/HAVEN"
CHECK="$HOME/Build/pdd-check"
HERE="$(cd "$(dirname "$0")" && pwd)"
FILES="$HERE/files"
BRANCH="pdd/testmatrise-apns"
WT="$CHECK/impl-CellScaffold"
OUT="$HERE/run-$(date +%Y%m%d-%H%M%S)"; mkdir -p "$OUT"
exec > >(tee "$OUT/apply.log") 2>&1

echo "gren $BRANCH fra origin/main i $WT"
echo "legger inn: InviteApnsPush.swift, InviteApnsPushTests.swift, sendInvite i PushProviderAdapter.swift"
[ "$MODE" = "--go" ] || { echo "Tørrkjøring OK. Kjør med --go."; exit 0; }

git -C "$BASE/CellScaffold" fetch -q origin || { echo "FEIL: fetch"; exit 1; }
if [ -e "$WT/.git" ] && ! git -C "$WT" rev-parse --git-dir >/dev/null 2>&1; then mv "$WT" "$WT.defekt-$$"; git -C "$BASE/CellScaffold" worktree prune; fi
if [ -e "$WT/.git" ]; then
  git -C "$WT" reset -q --hard; git -C "$WT" clean -qfd
  git -C "$WT" checkout -q -B "$BRANCH" origin/main
else
  git -C "$BASE/CellScaffold" worktree add -q -B "$BRANCH" "$WT" origin/main || { echo "FEIL: worktree"; exit 1; }
fi
echo "står på $(git -C "$WT" rev-parse --short HEAD) ($BRANCH)"

N="$WT/Sources/App/Cells/ConferenceMVP/Notifications"
cp "$FILES/InviteApnsPush.swift" "$N/InviteApnsPush.swift"
cp "$FILES/InviteApnsPushTests.swift" "$WT/Tests/AppTests/InviteApnsPushTests.swift"

PY=""; for c in /usr/bin/python3 /opt/homebrew/bin/python3 python3; do "$c" -c 'import sys' >/dev/null 2>&1 && { PY="$c"; break; }; done
[ -n "$PY" ] || { echo "FEIL: ingen fungerende python"; exit 1; }
"$PY" - "$N/PushProviderAdapter.swift" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p).read()
if "func sendInvite(" in s:
    print("sendInvite finnes allerede — hopper over"); sys.exit(0)
anchor = "    private func providerToken(now: Date = Date()) async throws -> String {"
assert s.count(anchor) == 1, "fant ikke anker for providerToken"
add = '''    /// Invitasjonsvarsel (kontrakt apns_invite_v1). Vert, topic og utløp følger registreringen
    /// (InviteApnsPush), ikke denne scaffoldens APNS_USE_SANDBOX / APNS_BUNDLE_ID.
    func sendInvite(_ push: InviteApnsPush) async throws -> PushSendResult {
        let authToken = try await providerToken()
        let response = try await transport.send(try push.urlRequest(authToken: authToken))
        let providerMessageID = stringHeader("apns-id", in: response.headers)
        if (200..<300).contains(response.statusCode) {
            return PushSendResult(providerMessageID: providerMessageID, accepted: true, diagnosticMessage: "APNS accepted invitation push.")
        }
        let diagnostic = parseAPNSFailure(body: response.body) ?? "APNS rejected invitation push with HTTP \\(response.statusCode)."
        return PushSendResult(providerMessageID: providerMessageID, accepted: false, diagnosticMessage: diagnostic)
    }

'''
s = s.replace(anchor, add + anchor, 1)
open(p, "w").write(s)
print("sendInvite lagt inn")
PYEOF

export CELLPROTOCOL_LOCAL_PACKAGE_PATH="$CHECK/pinned/CellProtocol" DIMYMINT_LOCAL_PACKAGE_PATH="$CHECK/pinned/DiMyMint" DIMYMICROPAYMENTS_LOCAL_PACKAGE_PATH="$CHECK/pinned/DiMyMicropayments"
echo "== build =="
( cd "$WT" && swift build > "$OUT/build.log" 2>&1 && echo "build: OK" || echo "build: FEILET (se build.log)" )
bundle_line() { sed 's/\x1b\[[0-9;]*m//g' "$1" | grep -A1 -E "^Test Suite '$2\.xctest' (passed|failed)" | grep -E "Executed [0-9]+ tests" | tail -1; }
verdict() { case "$1" in *" 0 failures (0 unexpected)"*) echo GRØNN;; "") echo INGEN-LINJE;; *) echo RØD;; esac; }
echo "== test: InviteApnsPushTests (kun de nye) =="
( cd "$WT" && swift test --filter InviteApnsPushTests > "$OUT/test.log" 2>&1 )
L="$(bundle_line "$OUT/test.log" AppTests)"; echo "AppTests-linje: [$L] → $(verdict "$L")"
grep -E "error:|failed" "$OUT/test.log" | sed 's/\x1b\[[0-9;]*m//g' | sort -u | head -20
echo "== regresjon: hele CellScaffold-suiten, sammenlignet med baseline-failures-pinned.txt =="
( cd "$WT" && swift test > "$OUT/test-all.log" 2>&1 )
L="$(bundle_line "$OUT/test-all.log" AppTests)"; echo "AppTests-linje: [$L]"
sed 's/\x1b\[[0-9;]*m//g' "$OUT/test-all.log" | grep -E "Test Case .* failed" | sed -E "s/^Test Case '-\[([^ ]+) ([^]]+)\]' failed.*/\1.\2/" | sort -u > "$OUT/failures.txt"
echo "røde tester nå: $(wc -l < "$OUT/failures.txt") · baseline: $(wc -l < "$HERE/../baseline-failures-pinned.txt")"
NEW="$(comm -13 "$HERE/../baseline-failures-pinned.txt" "$OUT/failures.txt")"
if [ -z "$NEW" ]; then echo "NYE RØDE: ingen (regresjon OK mot baseline)"; else echo "NYE RØDE (ikke i baseline):"; echo "$NEW"; fi
FIXED="$(comm -23 "$HERE/../baseline-failures-pinned.txt" "$OUT/failures.txt")"
[ -z "$FIXED" ] || { echo "i baseline men ikke rød nå (ustabil eller rettet):"; echo "$FIXED"; }
echo "== ferdig. Endringer (ikke committet): =="
git -C "$WT" status --short
echo "logger: $OUT"
