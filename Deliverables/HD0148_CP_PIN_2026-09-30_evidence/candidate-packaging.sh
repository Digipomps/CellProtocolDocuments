#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/environment.sh"
export HD0148_SWIFT_CACHE="$TASK_ROOT/swift-cache/caches/8a14945cc5a24ce94059905cb43409534f00319f0c1fb3cf0be99ffe44285c9d/swiftpm-cache"
swift() {
  local subcommand="$1"
  shift
  /usr/bin/swift "$subcommand" --disable-sandbox --cache-path "$HD0148_SWIFT_CACHE" --config-path "$HD0148_SWIFT_CONFIG" --security-path "$HD0148_SWIFT_SECURITY" --jobs 4 "$@"
}
export -f swift
export ARCHS="arm64 x86_64"
export VERSION="0.3.1-hd0148-verification-20260930"
export BUILD_ROOT="$TASK_ROOT/pilot-build"
export DIST_DIR="$TASK_ROOT/pilot-dist"
export MACOS_DEPLOYMENT_TARGET=13.0
cd "$HAVEN_TASK_ROOT"
exec bash "$TASK_ROOT/HavenAgentD/Packaging/build_correspondence_pilot.sh"
