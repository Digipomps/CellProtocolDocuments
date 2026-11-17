#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/environment.sh"
phase="$1"
shift
case "$phase" in
  baseline-agentd) package="$TASK_ROOT/HavenAgentD"; cachekey=hd0148-agentd ;;
  baseline-cp) package="$TASK_ROOT/CellProtocol-baseline"; cachekey=hd0148-agentd ;;
  *) exit 64 ;;
esac
cd "$package"
exec bash "$HAVEN_TASK_ROOT/CellProtocol/Scripts/haven-swiftpm.sh" --cache-root "$TASK_ROOT/swift-cache" --cache-key "$cachekey" -- test --disable-sandbox --config-path "$HD0148_SWIFT_CONFIG" --security-path "$HD0148_SWIFT_SECURITY" --jobs 4 --no-parallel "$@"
