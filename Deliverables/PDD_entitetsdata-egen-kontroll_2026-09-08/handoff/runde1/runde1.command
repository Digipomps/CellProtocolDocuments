#!/bin/bash
cd "$(dirname "$0")"
LOG="runde1-$(date +%Y%m%d-%H%M%S).log"
{
  echo "=== preflight ==="
  bash ./preflight.sh || { echo "PREFLIGHT FEILET - stopper for apply"; exit 1; }
  echo
  echo "=== apply --go ==="
  bash ./apply.sh --go || { echo "APPLY FEILET"; exit 1; }
  echo
  echo "=== verify ==="
  bash ./verify.sh
} 2>&1 | tee "$LOG"
echo
echo "Ferdig. Logg: $LOG"
