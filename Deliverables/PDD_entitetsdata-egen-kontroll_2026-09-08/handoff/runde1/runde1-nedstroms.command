#!/bin/bash
cd "$(dirname "$0")"
LOG="nedstroms-$(date +%Y%m%d-%H%M%S).log"
bash ./downstream.sh --binding-only 2>&1 | tee "$LOG"
echo
echo "Ferdig. Logg: $LOG"
