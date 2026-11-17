#!/bin/bash
cd "$(dirname "$0")"
LOG="push-$(date +%Y%m%d-%H%M%S).log"
bash ./push.sh 2>&1 | tee "$LOG"
echo; echo "Ferdig. Logg: $LOG"
