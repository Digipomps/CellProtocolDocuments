#!/bin/bash
# Bruk: run_l.sh <TAG>   (f.eks. L1_ANALYSE) — starter Codex-økten i bakgrunnen via launchctl.
# Valgfritt: CODEX_MODEL=<modell> ./run_l.sh L1_ANALYSE   (legger til -m)
# MERK: prompten skal be Codex skrive til <TAG>.md — aldri til <TAG>_svar.md, som er -o-fila (sluttmeldingen).
T="$1"; SB="${2:-workspace-write}"
D=/Users/kjetil/Build/Digipomps/HAVEN/CellProtocolDocuments/Deliverables/Lokalisering_Analyse_2026-09-07
LABEL="haven.codex.l10n.$T"
[ -f "$D/.$T.done" ] && { echo "$T allerede ferdig"; exit 0; }
[ -f "$D/${T}_prompt.md" ] || { echo "mangler $D/${T}_prompt.md"; exit 1; }
MODELARG=""; [ -n "${CODEX_MODEL:-}" ] && MODELARG="-m $CODEX_MODEL"
launchctl submit -l "$LABEL" -o "$D/${T}_stdout.log" -e "$D/${T}_stderr.log" -- /bin/bash -c "
cd /Users/kjetil/Build/Digipomps/HAVEN || exit 1
if [ ! -f '$D/.$T.done' ]; then
  /Users/kjetil/.local/bin/codex exec -C '$D' -s $SB --skip-git-repo-check $MODELARG \
    -c model_reasoning_effort=xhigh -o '$D/${T}_svar.md' - < '$D/${T}_prompt.md'
  echo \"exit=\$?\" > '$D/.$T.done'
fi
launchctl remove '$LABEL'
"
echo "submitted $LABEL${CODEX_MODEL:+ (model $CODEX_MODEL)}"
