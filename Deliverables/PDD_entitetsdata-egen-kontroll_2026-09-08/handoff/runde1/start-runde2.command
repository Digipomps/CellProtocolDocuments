#!/bin/bash
cd "$(dirname "$0")/../runde2"
LOG="runde2-$(date +%Y%m%d-%H%M%S).log"
bash ./runde2.sh --go 2>&1 | tee "$LOG"
echo; echo "Ferdig. Logg: $LOG"
