#!/bin/bash
# Selvfjernende launchd-jobb: kjør Codex-handoff for «husk det jeg sa» og logg.
export HOME=/Users/kjetil
export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Users/kjetil/.local/bin:/Applications/Xcode.app/Contents/Developer/usr/bin
LABEL=haven-losen-husk
PDD=/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/PDD_palazzo-husk-det-jeg-sa_2026-09-05
LOG=$PDD/handoff/codex_run.log
{
  echo "=== start $(date -Iseconds)"
  cd /Users/kjetil/Build/Digipomps/HAVEN || exit 1
  /Users/kjetil/.local/bin/codex exec --full-auto -C /Users/kjetil/Build/Digipomps/HAVEN \
    "Les $PDD/handoff/README.md og utfør slicene som er merket GODKJENT, i rekkefølge. Svar kun med rapporten."
  echo "=== exit $? $(date -Iseconds)"
} >> "$LOG" 2>&1
launchctl remove $LABEL
