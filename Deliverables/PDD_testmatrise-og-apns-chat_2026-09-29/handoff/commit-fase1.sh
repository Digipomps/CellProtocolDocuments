#!/bin/bash
# Committer fase 1 i engangs-worktrees (aldri Kjetils checkout). Pusher bare med --push.
#   ./commit-fase1.sh            tørrkjøring: viser hva som ville committes
#   ./commit-fase1.sh --commit   lokale commits på grenene (ingenting forlater Macen)
#   ./commit-fase1.sh --push     commit + push grenene til origin (nye grener; ingen eksisterende røres)
set -uo pipefail
MODE="${1:-dry}"
BASE="$HOME/Build/Digipomps/HAVEN"; CHECK="$HOME/Build/pdd-check"
HERE="$(cd "$(dirname "$0")" && pwd)"
PDD="$(cd "$HERE/.." && pwd)"
SLUG="$(basename "$PDD")"
OUT="$HERE/commit-fase1-$(date +%Y%m%d-%H%M%S).log"
exec > >(tee "$OUT") 2>&1
TRAILER=$'Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_0166zowbapoq3r6iijrhd2xx'

commit_wt() { # navn worktree gren melding
  local name="$1" wt="$2" branch="$3" msg="$4"
  [ -e "$wt/.git" ] || { echo "$name: worktree $wt mangler — hopper over"; return; }
  [ "$(git -C "$wt" rev-parse --abbrev-ref HEAD)" = "$branch" ] || { echo "$name: $wt står ikke på $branch — hopper over"; return; }
  git -C "$wt" checkout -q -- Package.resolved 2>/dev/null   # SPM-støy, skal ikke med
  echo "== $name ($branch): $(git -C "$wt" status --short | wc -l | tr -d ' ') endringer"; git -C "$wt" status --short
  [ "$MODE" = "dry" ] && return
  git -C "$wt" add -A
  if git -C "$wt" diff --cached --quiet; then echo "$name: ingenting nytt å committe"; else
    git -C "$wt" commit -q -m "$msg" -m "$TRAILER" && echo "$name: committet $(git -C "$wt" rev-parse --short HEAD)"
  fi
  [ "$MODE" = "--push" ] && git -C "$wt" push -q origin "$branch" && echo "$name: pushet $branch → origin $(git -C "$wt" rev-parse --short HEAD)"
}

commit_wt CellProtocol "$CHECK/impl/CellProtocol" pdd/testmatrise-apns "APNs-invitasjon: signert tokenregistrering, planlegger og audienceEntity (PDD testmatrise WP2/WP3)

HavenPushRegistration/Revocation/Registry (nøkkelpinning, ingen navn lagret), HavenInvitePushPlanner (kun navngitt og registrert entitet), valgfritt signert audienceEntity i HavenInvitePublication. 31 nye tester; CellBaseTests 1559/0."
commit_wt "CellScaffold (fase 1, pinnet)" "$CHECK/impl-CellScaffold" pdd/testmatrise-apns "APNs-payload for invitasjoner uten innhold (PDD testmatrise WP1)

InviteApnsPush (gylden payload, headers, utløp) og APNSPushProviderAdapter.sendInvite. 9 nye tester, ingen nye røde mot pinnet CellProtocol 2026.9.4."
commit_wt "CellScaffold (dev)" "$CHECK/impl/CellScaffold" pdd/testmatrise-apns-dev "APNs-invitasjon: payload, tokenregister og dispatcher (PDD testmatrise WP1–WP3)

InviteApnsPush, PushRegistryService/FilePushRegistryStore, InvitePushDispatcher (utfall bare i scaffoldets logg). Bygger mot CellProtocol-grenen pdd/testmatrise-apns; to try-rettelser for CellProtocol #53. 20 nye tester, røde sett identisk med kontroll (42)."

# dokumentasjon: egen worktree av CellProtocolDocuments, bare lette filer (ikke test-logger)
DOC="$CHECK/impl/CellProtocolDocuments"
if [ "$MODE" != "dry" ]; then
  git -C "$BASE/CellProtocolDocuments" fetch -q origin
  if [ -e "$DOC/.git" ]; then git -C "$DOC" reset -q --hard; git -C "$DOC" clean -qfd; git -C "$DOC" checkout -q -B pdd/testmatrise-og-apns-chat origin/main
  else git -C "$BASE/CellProtocolDocuments" worktree add -q -B pdd/testmatrise-og-apns-chat "$DOC" origin/main || { echo "FEIL: dokument-worktree"; exit 1; }; fi
  DEST="$DOC/Deliverables/$SLUG"; mkdir -p "$DEST"
  /usr/bin/rsync -a --delete \
    --exclude '_dry/' --exclude 'snapshot-alle-2*/' --exclude 'build.log' --exclude '*-test.log' --exclude '*test-all.log' --exclude 'test*.log' \
    --exclude 'binding-build.log' --exclude 'cellscaffold-*-build.log' --exclude 'cellprotocol-build.log' --exclude 'matrix-*/' --exclude '_spec_*' \
    "$PDD/" "$DEST/"
  git -C "$DOC" add -A
  if git -C "$DOC" diff --cached --quiet; then echo "Dokumentasjon: ingenting nytt"; else
    git -C "$DOC" commit -q -m "PDD testmatrise og APNs-chat: spesifikasjon, plan, kontrakt, testresultat, handoff" -m "$TRAILER" && echo "Dokumentasjon: committet $(git -C "$DOC" rev-parse --short HEAD) ($(git -C "$DOC" show --stat --format= HEAD | tail -1))"
  fi
  [ "$MODE" = "--push" ] && git -C "$DOC" push -q origin pdd/testmatrise-og-apns-chat && echo "Dokumentasjon: pushet"
else
  echo "== dokumentasjon: ville kopiert $SLUG (uten test-logger) til gren pdd/testmatrise-og-apns-chat i en CellProtocolDocuments-worktree"
fi
echo "ferdig ($MODE). Logg: $OUT"
