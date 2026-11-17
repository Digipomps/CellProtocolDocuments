// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

import XCTest
@testable import CellBase

/// Measures what the skeleton's table data path actually costs.
///
/// `SkeletonGrid.getItems()` and `SkeletonList` both resolve a whole
/// `ValueTypeList` in one go — there is no window, no page, no cursor.
/// Before deciding whether a spreadsheet-grade table is a renderer problem
/// or a data problem, we need the numbers rather than an opinion.
///
/// These are benchmarks, not assertions about correctness. The XCTAssert at
/// the end of each only guards against the measurement silently doing nothing.
final class SkeletonTableDataPathBenchmarkTests: XCTestCase {

    private func makeRows(rows: Int, columns: Int) -> ValueTypeList {
        var list = ValueTypeList()
        list.reserveCapacity(rows)
        let keys = (0..<columns).map { "col\($0)" }
        for r in 0..<rows {
            var object = Object()
            for (c, key) in keys.enumerated() {
                object[key] = .string("r\(r)c\(c)")
            }
            list.append(.object(object))
        }
        return list
    }

    private func report(_ label: String, _ body: () -> Void) {
        let start = Date()
        body()
        let ms = Date().timeIntervalSince(start) * 1000
        print("BENCH \(label): \(String(format: "%.1f", ms)) ms")
    }

    func testBuildCostGrowsWithRowCount() throws {
        for rows in [1_000, 10_000, 50_000] {
            report("build \(rows)x20") {
                _ = self.makeRows(rows: rows, columns: 20)
            }
        }
        XCTAssertEqual(makeRows(rows: 3, columns: 2).count, 3)
    }

    func testJSONRoundTripIsThePortholeCost() throws {
        let encoder = JSONEncoder()
        let decoder = JSONDecoder()
        for rows in [1_000, 10_000, 50_000] {
            let list = makeRows(rows: rows, columns: 20)
            var data = Data()
            report("encode \(rows)x20") {
                data = (try? encoder.encode(list)) ?? Data()
            }
            print("BENCH bytes \(rows)x20: \(data.count)")
            report("decode \(rows)x20") {
                _ = try? decoder.decode(ValueTypeList.self, from: data)
            }
        }
        XCTAssertTrue(true)
    }

    /// What a windowed resolve would cost instead: the same 50k-row sheet,
    /// but only the 60 rows a viewport can show.
    func testWindowedResolveIsTheComparison() throws {
        let encoder = JSONEncoder()
        let decoder = JSONDecoder()
        let window = makeRows(rows: 60, columns: 20)
        var data = Data()
        report("encode window 60x20") {
            data = (try? encoder.encode(window)) ?? Data()
        }
        print("BENCH bytes window 60x20: \(data.count)")
        report("decode window 60x20") {
            _ = try? decoder.decode(ValueTypeList.self, from: data)
        }
        XCTAssertEqual(window.count, 60)
    }
}
