@testable import App
import CellBase
import Foundation
import XCTest

// Temporary provenance generator; remove before publishing the migration.
final class ButlerLegacyFixtureGenerationTests: XCTestCase {
    func testExportExactFormerMainFactory() throws {
        let configuration = try XCTUnwrap(LegacyButlerFactoryB4A2779A.configuration(for: PersonalChatHubContract.endpoint))
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.sortedKeys, .prettyPrinted, .withoutEscapingSlashes]
        let data = try encoder.encode(configuration)
        let target = URL(fileURLWithPath: #filePath).deletingLastPathComponent().appendingPathComponent("Fixtures/ButlerBuiltIn-b4a2779a.json")
        try data.write(to: target, options: .atomic)
        let skeleton = try XCTUnwrap(configuration.skeleton)
        let digest = try XCTUnwrap(ButlerBuiltInConfigurationUpgrade.fingerprint(skeleton))
        let independent = try XCTUnwrap(LegacyButlerFactoryB4A2779A.configuration(for: PersonalChatHubContract.endpoint)?.skeleton)
        XCTAssertEqual(ButlerBuiltInConfigurationUpgrade.fingerprint(independent), digest, "Only renderer UUIDs may differ between factory invocations")
        try digest.write(to: target.appendingPathExtension("sha256"), atomically: true, encoding: .utf8)
        print("VERIFIED_LEGACY_BUTLER_DIGEST=\(digest)")
    }
}
