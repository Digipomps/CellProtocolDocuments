#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/environment.sh"
cd "$TASK_ROOT/HavenAgentD"
exec bash "$HAVEN_TASK_ROOT/CellProtocol/Scripts/haven-swiftpm.sh" --cache-root "$TASK_ROOT/swift-cache" --cache-key hd0148-agentd -- build --disable-sandbox --config-path "$HD0148_SWIFT_CONFIG" --security-path "$HD0148_SWIFT_SECURITY" --jobs 4
