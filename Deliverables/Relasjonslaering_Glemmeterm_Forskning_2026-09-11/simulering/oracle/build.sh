#!/bin/bash
set -euo pipefail
oracle_dir="$(cd "$(dirname "$0")" && pwd)"
cellprotocol_repo="${1:?CellProtocol checkout path required}"
xcode_developer="$(xcode-select -p)"
xcode_platform="$xcode_developer/Platforms/MacOSX.platform/Developer"
source_dir="$cellprotocol_repo/Sources/CellBase/PurposeAndInterest"
production_sources=("$source_dir/RelationalLearningEngine.swift" "$source_dir/RelationalLearningModels.swift" "$source_dir/RelationalDecayPolicy.swift")
swiftc -parse-as-library -module-cache-path "$oracle_dir/module-cache" "$oracle_dir/Support.swift" "$oracle_dir/Oracle.swift" "${production_sources[@]}" -o "$oracle_dir/oracle"
swiftc -emit-library -emit-module -enable-testing -module-name CellBase -module-cache-path "$oracle_dir/module-cache" "$oracle_dir/Support.swift" "${production_sources[@]}" -emit-module-path "$oracle_dir/CellBase.swiftmodule" -o "$oracle_dir/libCellBase.dylib"
swiftc -parse-as-library -module-cache-path "$oracle_dir/module-cache" -I "$oracle_dir" -L "$oracle_dir" -lCellBase -Xlinker -rpath -Xlinker "$oracle_dir" -F "$xcode_platform/Library/Frameworks" -I "$xcode_platform/usr/lib" -L "$xcode_platform/usr/lib" -framework XCTest -Xlinker -rpath -Xlinker "$xcode_platform/Library/Frameworks" -Xlinker -rpath -Xlinker "$xcode_platform/usr/lib" "$cellprotocol_repo/Tests/CellBaseTests/RelationalLearningEngineTests.swift" "$oracle_dir/TestMain.swift" -o "$oracle_dir/test-runner"
"$oracle_dir/test-runner" > "$oracle_dir/direct-tests-output.txt" 2>&1
shasum -a 256 "${production_sources[@]}" "$cellprotocol_repo/Tests/CellBaseTests/RelationalLearningEngineTests.swift" "$oracle_dir/Support.swift" "$oracle_dir/Oracle.swift" "$oracle_dir/TestMain.swift" > "$oracle_dir/source-hashes.txt"
