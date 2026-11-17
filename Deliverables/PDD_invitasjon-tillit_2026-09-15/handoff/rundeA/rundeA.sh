#!/bin/bash
# Invitasjon runde A, del 1 (CellProtocol, WP1–WP5): applies rundeA.patch on a
# fresh worktree from origin/main, builds, runs the new suite + full
# CellBaseTests, and commits+pushes only when everything is green. Never touches
# Kjetil's checkout. No force.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
BASE="$HOME/Build/Digipomps/HAVEN"
REPO="$BASE/CellProtocol"
WT="$BASE/CellProtocol-pdd-invitasjon-a"
BRANCH="pdd/invitasjon-runde-a"
STAMP="$(date +%Y%m%d-%H%M%S)"
FULL="$HERE/rundeA-$STAMP.full.log"
MODE="${1:-}"

echo "== fetch =="
git -C "$REPO" fetch -q origin || { echo "FEIL: fetch"; exit 1; }
MAIN="$(git -C "$REPO" rev-parse --short origin/main)"
echo "origin/main: $MAIN"
git -C "$REPO" show origin/main:Sources/CellBase/PersistingCells/EntityChangeTrace.swift >/dev/null 2>&1 || { echo "FEIL: runde 2 (#50) er ikke på origin/main"; exit 1; }

echo "== worktree $WT @ $BRANCH =="
if [ -d "$WT" ]; then
  if [ -n "$(git -C "$WT" status --porcelain)" ] || [ "$(git -C "$WT" rev-parse HEAD)" != "$(git -C "$REPO" rev-parse origin/main)" ]; then
    if git -C "$WT" log --oneline origin/main..HEAD | grep -q .; then
      echo "worktreet har egne commits — rører det ikke:"; git -C "$WT" log --oneline origin/main..HEAD; exit 1
    fi
    git -C "$WT" reset -q --hard origin/main
    git -C "$WT" clean -qfd
  fi
else
  git -C "$REPO" worktree add -q -B "$BRANCH" "$WT" origin/main || { echo "FEIL: worktree add"; exit 1; }
fi
git -C "$WT" checkout -q -B "$BRANCH" origin/main
echo "HEAD: $(git -C "$WT" rev-parse --short HEAD)"

echo "== patch (dry-run) =="
git -C "$WT" apply --check -p1 "$HERE/rundeA.patch" || { echo "PATCHEN PASSER IKKE mot origin/main $MAIN — stopper"; exit 1; }
[ "$MODE" = "--go" ] || { echo "Tørrkjøring OK. Kjør med --go for å legge på, bygge, teste og pushe."; exit 0; }
git -C "$WT" apply -p1 "$HERE/rundeA.patch" && echo "patch lagt på"
git -C "$WT" status --short

cd "$WT"
echo "== swift build =="
swift build > "$FULL" 2>&1 && echo "Build: OK" || { echo "Build: FEILET"; grep -E "error:" "$FULL" | head -40; exit 1; }
echo "== nye tester =="
swift test --filter 'HavenInviteRoundATests' > "$FULL.new" 2>&1
grep -E "Executed [0-9]+ tests" "$FULL.new" | tail -1
grep -E "error:|Test Case .* failed|XCTAssert" "$FULL.new" | head -40
echo "== hele CellBaseTests =="
swift test --filter 'CellBaseTests' > "$FULL.alle" 2>&1
grep -E "Executed [0-9]+ tests" "$FULL.alle" | tail -1
# Only the LAST "Executed" line counts (lesson.green-gate-must-read-the-last-summary-line).
NEW_LAST="$(grep -E "Executed [0-9]+ tests" "$FULL.new" | tail -1)"
ALL_LAST="$(grep -E "Executed [0-9]+ tests" "$FULL.alle" | tail -1)"
GREEN=0
case "$NEW_LAST" in *" 0 failures (0 unexpected)"*) case "$ALL_LAST" in *" 0 failures (0 unexpected)"*) GREEN=1;; esac;; esac
echo "gate: NEW_LAST=[$NEW_LAST] ALL_LAST=[$ALL_LAST] GREEN=$GREEN"
if [ "$GREEN" = "1" ]; then
  echo "== grønt — committer og pusher =="
  git add -A
  git commit -q -F - <<'MSG'
Invitation round A (CellProtocol): domain, expiry, basis, reply, tombstone

purpose://candidate.invite.sender-is-the-domain-identity
purpose://candidate.invite.expires-by-itself
purpose://candidate.invite.claim-about-another
purpose://candidate.invite.minimum-for-the-send
purpose://candidate.invite.recipient-sees-what-is-held
purpose://candidate.invite.private-notes-never-leave
purpose://candidate.invite.no-automatic-reminders
purpose://candidate.invite.decline-without-account
purpose://candidate.invite.acceptance-carries-the-key-to-seal-to (first half)

- HavenInviteTicket: identityDomain ("id") and basis ("bs") under the
  signature; defaultTimeToLive 14 d, maximumTimeToLive 90 d; verifier code
  ttl_too_long. Older tickets without the keys still decode and verify.
- HavenInvitePublicationVerifier: refuses a publication of an expired ticket
  or one claiming too long a life; contact requests and replies on an
  expired ticket are refused; verifyReply.
- HavenInviteReply (yes / notNow / never), HavenInviteTombstone (a verified
  "never"; blocks a new ticket from the same issuer to the same audience,
  survives the ticket's expiry and a ledger round trip), HavenInviteTombstoneLedger.
- HavenInviteSenderView + HavenInviteSenderReport: the sender sees
  published / answered / expired / revoked — never "opened", and no
  difference between "not now" and "never".
- HavenContactBasisV1: basis fields (unconfirmed, with origin) and
  privateNotes as two parts; validation rejects free text and unknown keys;
  basisFields() is the only way out and does not read privateNotes.
- ChatInvitationAcceptance.inviteeKeyAgreementKey and
  HavenInviteContactRequest.senderKeyAgreementKey, both under the signature;
  ChatCell sets the key-agreement key on the invitee it resolves.
- EphemeralIdentityVault mints an X25519 key per identity and provides key
  roles, so SimulatedEntity can be sealed to.
- HavenInviteRoundATests: 14 tests, two simulated entities each.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0166zoWBapoQ3R6iiJrhd2xx
MSG
  echo "commit: $(git rev-parse --short HEAD)"
  git push -u origin "$BRANCH" 2>&1 | tail -2
  echo "origin/$BRANCH: $(git ls-remote --heads origin "$BRANCH" | cut -c1-7)"
  if command -v gh >/dev/null; then
    gh pr create --draft --base main --head "$BRANCH" \
      --title "Invitasjon runde A del 1: domene, utløp, grunnlag, svar og gravstein" \
      --body "PDD_invitasjon-tillit runde A, WP1–WP5, CellProtocol-delen. Se CellProtocolDocuments: Deliverables/PDD_invitasjon-tillit_2026-09-15/TESTRESULT.md#rundeA. Utkast for CI. Del 2 (CellScaffold + Binding) følger når denne er på main.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_0166zoWBapoQ3R6iiJrhd2xx" 2>&1 | tail -1
  fi
else
  echo "RØDT — committer IKKE. Se $FULL.new og $FULL.alle"
  grep -E "Test Case .* failed" "$FULL.alle" | head -20
  grep -E "error:" "$FULL.new" "$FULL.alle" | head -20
  exit 1
fi
