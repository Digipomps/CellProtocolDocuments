#!/bin/bash
cd "$(dirname "$0")/../runde2"
LOG="fix1-$(date +%Y%m%d-%H%M%S).log"
bash ./runde2-fix.sh 2>&1 | tee "$LOG"
echo; echo "Ferdig. Logg: $LOG"
