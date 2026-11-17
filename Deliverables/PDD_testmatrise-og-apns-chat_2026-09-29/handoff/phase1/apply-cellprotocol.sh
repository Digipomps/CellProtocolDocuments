#!/bin/bash
# Fase 1 (WP2, CellProtocol-delen): HavenPushRegistration + tester på egen gren i engangs-worktree.
#   ./apply-cellprotocol.sh        tørrkjøring
#   ./apply-cellprotocol.sh --go   lag worktree/gren, legg inn filene, bygg, kjør de nye testene + hele CellBaseTests
set -uo pipefail
MODE="${1:-}"
BASE="$HOME/Build/Digipomps/HAVEN"
CHECK="$HOME/Build/pdd-check"
HERE="$(cd "$(dirname "$0")" && pwd)"
FILES="$HERE/files-cellprotocol"
BRANCH="pdd/testmatrise-apns"
WT="$CHECK/impl/CellProtocol"; mkdir -p "$CHECK/impl"
OUT="$HERE/run-cp-$(date +%Y%m%d-%H%M%S)"; mkdir -p "$OUT"
exec > >(tee "$OUT/apply.log") 2>&1

echo "gren $BRANCH fra origin/main i $WT"
echo "legger inn: HavenPushRegistration, HavenInvitePushPlanner (+ tester), og audienceEntity i HavenInvitePublication"
[ "$MODE" = "--go" ] || { echo "Tørrkjøring OK. Kjør med --go."; exit 0; }

git -C "$BASE/CellProtocol" fetch -q origin || { echo "FEIL: fetch"; exit 1; }
if [ -e "$WT/.git" ] && ! git -C "$WT" rev-parse --git-dir >/dev/null 2>&1; then mv "$WT" "$WT.defekt-$$"; git -C "$BASE/CellProtocol" worktree prune; fi
if [ -e "$WT/.git" ]; then
  git -C "$WT" reset -q --hard; git -C "$WT" clean -qfd
  git -C "$WT" checkout -q -B "$BRANCH" origin/main
else
  git -C "$BASE/CellProtocol" worktree add -q -B "$BRANCH" "$WT" origin/main || { echo "FEIL: worktree"; exit 1; }
fi
echo "står på $(git -C "$WT" rev-parse --short HEAD) ($BRANCH)"
cp "$FILES/HavenPushRegistration.swift" "$WT/Sources/CellBase/Invitation/HavenPushRegistration.swift"
cp "$FILES/HavenPushRegistrationTests.swift" "$WT/Tests/CellBaseTests/HavenPushRegistrationTests.swift"
cp "$FILES/HavenInvitePushPlanner.swift" "$WT/Sources/CellBase/Invitation/HavenInvitePushPlanner.swift"
cp "$FILES/HavenInvitePushPlannerTests.swift" "$WT/Tests/CellBaseTests/HavenInvitePushPlannerTests.swift"

PY=""; for c in /usr/bin/python3 /opt/homebrew/bin/python3 python3; do "$c" -c 'import sys' >/dev/null 2>&1 && { PY="$c"; break; }; done
[ -n "$PY" ] || { echo "FEIL: ingen fungerende python"; exit 1; }
# audienceEntity: valgfritt, signert felt i publiseringen. Kodes bare når det er satt (gamle publiseringer får samme kanoniske bytes).
"$PY" - "$WT/Sources/CellBase/Invitation/HavenInvitePublication.swift" <<'PYEOF'
import sys
p = sys.argv[1]; s = open(p).read()
if "audienceEntity" in s:
    print("audienceEntity finnes allerede — hopper over"); sys.exit(0)
def rep(old, new):
    global s
    assert s.count(old) == 1, "anker mangler: " + old[:60]
    s = s.replace(old, new, 1)
rep("    public var statusKey: String\n    public var proof: HavenSignatureProof?\n",
    "    public var statusKey: String\n    /// The entity the sender named for this invitation, resolved from the sender's own relations or a registry\n    /// (purpose://candidate.invite.resolve-recipient-to-an-entity). Signed, but NOT in the ticket or link. Only an\n    /// entity named here can be pushed (purpose://candidate.testmatrise.apns.only-who-was-invited-is-pushed).\n    public var audienceEntity: String?\n    public var proof: HavenSignatureProof?\n")
rep("        statusKey: String,\n        proof: HavenSignatureProof? = nil\n    ) {\n        self.schema = schema\n        self.ticketID = ticketID\n        self.humanCode = humanCode\n        self.ticketToken",
    "        statusKey: String,\n        audienceEntity: String? = nil,\n        proof: HavenSignatureProof? = nil\n    ) {\n        self.schema = schema\n        self.ticketID = ticketID\n        self.humanCode = humanCode\n        self.ticketToken")
rep("        self.statusKey = statusKey\n        self.proof = proof\n",
    "        self.statusKey = statusKey\n        self.audienceEntity = audienceEntity\n        self.proof = proof\n")
rep("        guard ticket.issuer.uuid == publication.issuerIdentityUUID else {\n            throw Failure.issuerMismatch\n        }\n\n        try verifyEnvelope(publication, signedBy: ticket.issuer)",
    "        guard ticket.issuer.uuid == publication.issuerIdentityUUID else {\n            throw Failure.issuerMismatch\n        }\n        if let entity = publication.audienceEntity, !HavenPushFormat.isValidEntity(entity) {\n            throw Failure.ticketMismatch(\"audienceEntity\")\n        }\n\n        try verifyEnvelope(publication, signedBy: ticket.issuer)")
open(p, "w").write(s)
print("audienceEntity lagt inn")
PYEOF

last() { grep -E "Executed [0-9]+ tests" "$1" | tail -1; }
verdict() { case "$1" in *" 0 failures (0 unexpected)"*) echo GRØNN;; "") echo INGEN-LINJE;; *) echo RØD;; esac; }
echo "== build =="
( cd "$WT" && swift build > "$OUT/build.log" 2>&1 && echo "build: OK" || echo "build: FEILET (se build.log)" )
echo "== test: HavenPushRegistrationTests + HavenInvitePushPlannerTests =="
( cd "$WT" && swift test --filter "HavenPushRegistrationTests|HavenInvitePushPlannerTests" > "$OUT/test-push.log" 2>&1 )
L="$(last "$OUT/test-push.log")"; echo "siste linje: [$L] → $(verdict "$L")"
grep -E "error:|failed" "$OUT/test-push.log" | sed 's/\x1b\[[0-9;]*m//g' | sort -u | head -20
echo "== regresjon: hele CellBaseTests =="
( cd "$WT" && swift test --filter CellBaseTests > "$OUT/test-all.log" 2>&1 )
L="$(last "$OUT/test-all.log")"; echo "siste linje: [$L] → $(verdict "$L")"
echo "== endringer (ikke committet) =="; git -C "$WT" status --short
echo "logger: $OUT"
