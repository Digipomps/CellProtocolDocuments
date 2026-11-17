#!/bin/bash
# Fase 2 (WP1+WP2+WP3 på scaffold-siden): alt CellScaffold-arbeid mot CellProtocol-grenen (pdd/testmatrise-apns), ikke den pinnede taggen.
# Krever at apply-cellprotocol.sh har kjørt (impl/CellProtocol finnes). Egen gren pdd/testmatrise-apns-dev i impl/CellScaffold.
#   ./apply-phase2.sh        tørrkjøring
#   ./apply-phase2.sh --go   bygg + nye tester + full regresjon mot baseline-failures-pinned.txt
set -uo pipefail
MODE="${1:-}"
BASE="$HOME/Build/Digipomps/HAVEN"
CHECK="$HOME/Build/pdd-check"
IMPL="$CHECK/impl"
HERE="$(cd "$(dirname "$0")" && pwd)"
BRANCH="pdd/testmatrise-apns-dev"
WT="$IMPL/CellScaffold"
OUT="$HERE/run-p2-$(date +%Y%m%d-%H%M%S)"; mkdir -p "$OUT"
exec > >(tee "$OUT/apply.log") 2>&1

echo "gren $BRANCH fra origin/main i $WT, bygget mot $IMPL/CellProtocol (gren pdd/testmatrise-apns)"
echo "legger inn: InviteApnsPush, InvitePushDispatcher (+ tester), sendInvite i PushProviderAdapter, try-rettelse i VaporPersonEntityReadRoute (kompatibilitet med CellProtocol main)"
[ "$MODE" = "--go" ] || { echo "Tørrkjøring OK. Kjør med --go."; exit 0; }

[ -e "$IMPL/CellProtocol/.git" ] || { echo "FEIL: $IMPL/CellProtocol mangler — kjør apply-cellprotocol.sh først"; exit 1; }
git -C "$BASE/CellScaffold" fetch -q origin || { echo "FEIL: fetch"; exit 1; }
# søsken-pakkene ved siden av CellProtocol (identitet avledes av katalognavn)
for r in DiMyMint DiMyMicropayments; do
  if [ ! -e "$IMPL/$r/.git" ]; then
    rev="$(git -C "$CHECK/pinned/$r" rev-parse HEAD 2>/dev/null)" || { echo "FEIL: pinned/$r mangler — kjør baseline.sh først"; exit 1; }
    git clone -q "$CHECK/pinned/$r" "$IMPL/$r" && git -C "$IMPL/$r" checkout -q --detach "$rev"
  fi
  echo "  $r står på $(git -C "$IMPL/$r" rev-parse --short HEAD)"
done
if [ -e "$WT/.git" ] && ! git -C "$WT" rev-parse --git-dir >/dev/null 2>&1; then mv "$WT" "$WT.defekt-$$"; git -C "$BASE/CellScaffold" worktree prune; fi
if [ -e "$WT/.git" ]; then
  git -C "$WT" reset -q --hard; git -C "$WT" clean -qfd
  git -C "$WT" checkout -q -B "$BRANCH" origin/main
else
  git -C "$BASE/CellScaffold" worktree add -q -B "$BRANCH" "$WT" origin/main || { echo "FEIL: worktree"; exit 1; }
fi
echo "står på $(git -C "$WT" rev-parse --short HEAD) ($BRANCH)"

N="$WT/Sources/App/Cells/ConferenceMVP/Notifications"
cp "$HERE/files/InviteApnsPush.swift" "$N/InviteApnsPush.swift"
cp "$HERE/files/InviteApnsPushTests.swift" "$WT/Tests/AppTests/InviteApnsPushTests.swift"
cp "$HERE/files-scaffold/InvitePushDispatcher.swift" "$N/InvitePushDispatcher.swift"
cp "$HERE/files-scaffold/InvitePushDispatcherTests.swift" "$WT/Tests/AppTests/InvitePushDispatcherTests.swift"

PY=""; for c in /usr/bin/python3 /opt/homebrew/bin/python3 python3; do "$c" -c 'import sys' >/dev/null 2>&1 && { PY="$c"; break; }; done
[ -n "$PY" ] || { echo "FEIL: ingen fungerende python"; exit 1; }
"$PY" - "$N/PushProviderAdapter.swift" "$WT/Sources/App/Controllers/VaporPersonEntityReadRoute.swift" "$WT/Tests/AppTests/EntityPersonBridgeProcessTests.swift" <<'PYEOF'
import sys
adapter, route, bridge_test = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(adapter).read()
if "func sendInvite(" in s:
    print("sendInvite finnes allerede — hopper over")
else:
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
    open(adapter, "w").write(s.replace(anchor, add + anchor, 1))
    print("sendInvite lagt inn")
r = open(route).read()
old = "        await underlying.sendData(data)\n"
if "try await underlying.sendData(data)" in r:
    print("try-rettelse finnes allerede")
else:
    assert r.count(old) == 1, "fant ikke sendData-linjen"
    open(route, "w").write(r.replace(old, "        try await underlying.sendData(data)\n", 1))
    print("try-rettelse lagt inn (CellProtocol #53 gjorde BridgeTransport.sendData throwing)")
t = open(bridge_test).read()
oldt = "        await transport.sendData(data)\n"
if "try await transport.sendData(data)" in t:
    print("try-rettelse i test finnes allerede")
else:
    assert t.count(oldt) == 1, "fant ikke sendData-linjen i EntityPersonBridgeProcessTests"
    open(bridge_test, "w").write(t.replace(oldt, "        try await transport.sendData(data)\n", 1))
    print("try-rettelse lagt inn i EntityPersonBridgeProcessTests (samme årsak)")
PYEOF

export CELLPROTOCOL_LOCAL_PACKAGE_PATH="$IMPL/CellProtocol" DIMYMINT_LOCAL_PACKAGE_PATH="$IMPL/DiMyMint" DIMYMICROPAYMENTS_LOCAL_PACKAGE_PATH="$IMPL/DiMyMicropayments"
bundle_line() { sed 's/\x1b\[[0-9;]*m//g' "$1" | grep -A1 -E "^Test Suite '$2\.xctest' (passed|failed)" | grep -E "Executed [0-9]+ tests" | tail -1; }
verdict() { case "$1" in *" 0 failures (0 unexpected)"*) echo GRØNN;; "") echo INGEN-LINJE;; *) echo RØD;; esac; }
echo "== build =="
( cd "$WT" && swift build > "$OUT/build.log" 2>&1 && echo "build: OK" || { echo "build: FEILET (se build.log)"; sed 's/\x1b\[[0-9;]*m//g' "$OUT/build.log" | grep "error:" | grep -v "failed with a nonzero" | sort -u | head -10; } )
echo "== test: nye tester (InviteApnsPushTests|InvitePushDispatcherTests) =="
( cd "$WT" && swift test --filter "InviteApnsPushTests|InvitePushDispatcherTests" > "$OUT/test.log" 2>&1 )
L="$(bundle_line "$OUT/test.log" AppTests)"; echo "AppTests-linje: [$L] → $(verdict "$L")"
sed 's/\x1b\[[0-9;]*m//g' "$OUT/test.log" | grep -E "error:|Test Case .* failed" | sort -u | cut -c1-300 | head -20
echo "== regresjon: hele CellScaffold-suiten mot CellProtocol-grenen, sammenlignet med baseline-failures-pinned.txt =="
( cd "$WT" && swift test > "$OUT/test-all.log" 2>&1 )
L="$(bundle_line "$OUT/test-all.log" AppTests)"; echo "AppTests-linje: [$L]"
if [ -z "$L" ]; then echo "TESTENE KOMPILERTE/KJØRTE IKKE — ingen sammenligning mot baseline er gyldig (ikke «0 røde»)"; echo "logger: $OUT"; exit 1; fi
sed 's/\x1b\[[0-9;]*m//g' "$OUT/test-all.log" | grep -E "Test Case .* failed" | sed -E "s/^Test Case '-\[([^ ]+) ([^]]+)\]' failed.*/\1.\2/" | sort -u > "$OUT/failures.txt"
echo "røde tester nå: $(wc -l < "$OUT/failures.txt") · baseline: $(wc -l < "$HERE/../baseline-failures-pinned.txt")"
NEW="$(comm -13 "$HERE/../baseline-failures-pinned.txt" "$OUT/failures.txt")"
if [ -z "$NEW" ]; then echo "NYE RØDE: ingen"; else echo "NYE RØDE (ikke i baseline):"; echo "$NEW"; fi
FIXED="$(comm -23 "$HERE/../baseline-failures-pinned.txt" "$OUT/failures.txt")"
[ -z "$FIXED" ] || { echo "i baseline men ikke rød nå:"; echo "$FIXED"; }
echo "== endringer (ikke committet) =="; git -C "$WT" status --short
echo "logger: $OUT"
