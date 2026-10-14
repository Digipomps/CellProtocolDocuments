#!/bin/bash
cd "$(dirname "$0")"
LOG="merge-$(date +%Y%m%d-%H%M%S).log"
bash ./merge.sh 2>&1 | tee "$LOG"
echo; echo "Ferdig. Logg: $LOG"
