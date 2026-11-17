#!/bin/bash
cd "$(dirname "$0")"
LOG="sync-$(date +%Y%m%d-%H%M%S).log"
bash ./sync-main.sh 2>&1 | tee "$LOG"
echo; echo "Ferdig. Logg: $LOG"
