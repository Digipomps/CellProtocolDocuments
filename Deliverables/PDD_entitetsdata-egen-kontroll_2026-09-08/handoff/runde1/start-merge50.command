#!/bin/bash
cd "$(dirname "$0")/../runde2"
LOG="merge50-$(date +%Y%m%d-%H%M%S).log"
bash ./merge50.sh 2>&1 | tee "$LOG"
echo; echo "Ferdig. Logg: $LOG"
