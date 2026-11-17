#!/usr/bin/env bash
set -euo pipefail
TASK_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HAVEN_TASK_ROOT="$(cd "$TASK_ROOT/../.." && pwd)"
export CLANG_MODULE_CACHE_PATH="$TASK_ROOT/module-cache"
export SWIFTPM_MODULECACHE_OVERRIDE="$CLANG_MODULE_CACHE_PATH"
export TMPDIR="$TASK_ROOT/tmp"
export SWIFTPM_MAX_CONCURRENT_OPERATIONS=1
export GIT_CONFIG_COUNT=2
export GIT_CONFIG_KEY_0=credential.https://github.com.helper
export GIT_CONFIG_VALUE_0=''
export GIT_CONFIG_KEY_1=credential.https://github.com.helper
export GIT_CONFIG_VALUE_1='!/opt/homebrew/bin/gh auth git-credential'
export HD0148_SWIFT_CONFIG="$TASK_ROOT/configuration"
export HD0148_SWIFT_SECURITY="$TASK_ROOT/security"
