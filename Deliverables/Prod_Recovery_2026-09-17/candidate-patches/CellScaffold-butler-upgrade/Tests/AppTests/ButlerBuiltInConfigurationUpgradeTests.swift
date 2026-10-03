// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright (c) 2026 Stiftelsen Digipomps and HAVEN contributors

@testable import App
import CellBase
import Foundation
import Vapor
import XCTest

final class ButlerBuiltInConfigurationUpgradeTests: IsolatedCellTestCase {
    private func legacy() throws -> CellConfiguration {
        let url = try XCTUnwrap(Bundle.module.url(
            forResource: "ButlerBuiltIn-b4a2779a", withExtension: "json", subdirectory: "Fixtures"
        ))
        return try JSONDecoder().decode(CellConfiguration.self, from: Data(contentsOf: url))
    }

    private func current() throws -> CellConfiguration {
        try XCTUnwrap(PersonalCopilotConfigurationFactory.configuration(for: PersonalChatHubContract.endpoint))
    }

    private func bytes<T: Encodable>(_ value: T) throws -> Data {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.sortedKeys]
        return try encoder.encode(value)
    }

    func testExactFormerFactoryUpgradesOnlySkeletonAndIsIdempotent() throws {
        var old = try legacy()
        old.uuid = "preserved-workspace-id"
        old.description = "Keep my workspace description"
        old.addReference(CellReference(endpoint: "cell:///EntityAnchor", label: "myExtraReference"))
        let published = try current()
        let upgraded = try XCTUnwrap(ButlerBuiltInConfigurationUpgrade.upgraded(old, using: published))
        XCTAssertEqual(upgraded.uuid, old.uuid)
        XCTAssertEqual(upgraded.description, old.description)
        XCTAssertEqual(try bytes(upgraded.discovery), try bytes(old.discovery))
        XCTAssertEqual(try bytes(upgraded.cellReferences), try bytes(old.cellReferences))
        XCTAssertEqual(try bytes(upgraded.localization), try bytes(old.localization))
        XCTAssertTrue(String(decoding: try bytes(upgraded.skeleton), as: UTF8.self).contains("chatHub.ui.helperTree.open"))
        XCTAssertNil(ButlerBuiltInConfigurationUpgrade.upgraded(upgraded, using: published))
    }

    func testCustomSkeletonNamesEndpointsAndActionPayloadsArePreserved() throws {
        let published = try current()
        var custom = try legacy()
        custom.skeleton = .Text(SkeletonText(text: "My own workspace"))
        XCTAssertNil(ButlerBuiltInConfigurationUpgrade.upgraded(custom, using: published))
        var renamed = try legacy()
        renamed.name = "My own Butler"
        XCTAssertNil(ButlerBuiltInConfigurationUpgrade.upgraded(renamed, using: published))
        var otherSource = try legacy()
        otherSource.discovery?.sourceCellEndpoint = "cell:///OtherCell"
        XCTAssertNil(ButlerBuiltInConfigurationUpgrade.upgraded(otherSource, using: published))

        // A UUID inside an action payload is semantic, unlike a renderer UUID.
        var button = SkeletonButton(keypath: "example.action", label: "Action", payload: .object(["id": .string(UUID().uuidString)]))
        let first = ButlerBuiltInConfigurationUpgrade.fingerprint(.Button(button))
        button.payload = .object(["id": .string(UUID().uuidString)])
        XCTAssertNotEqual(ButlerBuiltInConfigurationUpgrade.fingerprint(.Button(button)), first)
    }

    func testAccountContinuityReferenceAndOmittedOptionalReferencesArePreserved() throws {
        var old = try legacy()
        old.cellReferences = old.cellReferences?.filter { $0.label != "agreementWorkbench" }
        let chatIndex = try XCTUnwrap(old.cellReferences?.firstIndex(where: { $0.label == "chatHub" }))
        old.cellReferences?[chatIndex].endpoint = PersonalChatHubAccountCompatibility.endpoint
        let result = try XCTUnwrap(ButlerBuiltInConfigurationUpgrade.upgraded(old, using: current()))
        XCTAssertEqual(try bytes(result.cellReferences), try bytes(old.cellReferences))
        XCTAssertFalse(result.cellReferences?.contains(where: { $0.label == "agreementWorkbench" }) == true)
    }

    func testNormalBootstrapAndSameSurfaceLoadPersistThreadControls() async throws {
        let previousDebug = CellBase.debugValidateAccessForEverything
        CellBase.debugValidateAccessForEverything = false
        defer { CellBase.debugValidateAccessForEverything = previousDebug }
        let app = try await Application.make(.testing)
        do {
            try await configure(app)
            let ownerCandidate = await CellBase.defaultIdentityVault?.identity(
                for: "butler-upgrade-owner-\(UUID().uuidString)", makeNewIfNotFound: true
            )
            let owner = try XCTUnwrap(ownerCandidate)
            let ordinary = await OrchestratorCell(owner: owner)
            let old = try legacy()
            try await ordinary.setCellConfiguration(cellConfig: old)
            let bootstrap = try await PortholeWebSessionSupport.bootstrapValue(
                controlCell: ordinary, requester: owner, sessionId: "legacy-butler-bootstrap"
            )
            guard case let .object(envelope) = bootstrap,
                  case let .cellConfiguration(rendered)? = envelope["configuration"] else {
                throw XCTUnwrapFailure.missingConfiguration
            }
            XCTAssertTrue(String(decoding: try bytes(rendered.skeleton), as: UTF8.self).contains("chatHub.ui.helperTree.open"))
            let stored = try XCTUnwrap(ordinary.getCellConfiguration())
            XCTAssertEqual(stored.uuid, old.uuid)
            XCTAssertTrue(String(decoding: try bytes(stored.skeleton), as: UTF8.self).contains("chatHub.ui.helperTree.open"))

            // Recreate the old active configuration and use the ordinary
            // catalogue action; matching the active UUID must not keep it stale.
            try await ordinary.setCellConfiguration(cellConfig: old)
            let loaded = try await PortholeWebSessionSupport.loadRequestedConfiguration(
                from: .object(["configurationLookup": .object([
                    "name": .string(old.name),
                    "sourceCellEndpoint": .string(PersonalChatHubContract.endpoint)
                ])]), controlCell: ordinary, requester: owner
            )
            XCTAssertEqual(loaded.uuid, old.uuid)
            XCTAssertTrue(String(decoding: try bytes(loaded.skeleton), as: UTF8.self).contains("chatHub.ui.helperTree.open"))
            let encodedControl = try bytes(ordinary)
            let reloaded = try JSONDecoder().decode(OrchestratorCell.self, from: encodedControl)
            XCTAssertTrue(String(decoding: try bytes(reloaded.getCellConfiguration()?.skeleton), as: UTF8.self).contains("chatHub.ui.helperTree.open"))

            var customized = old
            customized.skeleton = .Text(SkeletonText(text: "Preserved user layout"))
            try await ordinary.setCellConfiguration(cellConfig: customized)
            _ = try await PortholeWebSessionSupport.bootstrapValue(
                controlCell: ordinary, requester: owner, sessionId: "custom-butler-bootstrap"
            )
            XCTAssertEqual(try bytes(ordinary.getCellConfiguration()?.skeleton), try bytes(customized.skeleton))
            // Upgrading the UI cannot create an account-compatibility mapping.
            let compatible = await AccountContinuityPortholeCell(owner: owner)
            var compatibilityOld = old
            let chatIndex = try XCTUnwrap(compatibilityOld.cellReferences?.firstIndex(where: { $0.label == "chatHub" }))
            compatibilityOld.cellReferences?[chatIndex].endpoint = PersonalChatHubAccountCompatibility.endpoint
            try await compatible.setCellConfiguration(cellConfig: compatibilityOld)
            let resolver = try XCTUnwrap(CellBase.defaultCellResolver)
            let beforeMappings = await resolver.identityNamedCells(requester: owner)
            XCTAssertNil(beforeMappings[owner.uuid]?[PersonalChatHubAccountCompatibility.referenceName])
            _ = try await PortholeWebSessionSupport.bootstrapValue(
                controlCell: compatible, requester: owner, sessionId: "unprovisioned-compatible-butler"
            )
            let afterMappings = await resolver.identityNamedCells(requester: owner)
            XCTAssertEqual(afterMappings[owner.uuid]?[PersonalChatHubAccountCompatibility.referenceName], beforeMappings[owner.uuid]?[PersonalChatHubAccountCompatibility.referenceName])
            XCTAssertEqual(try bytes(compatible.getCellConfiguration()?.skeleton), try bytes(compatibilityOld.skeleton))

            try await app.asyncShutdown()
        } catch {
            try? await app.asyncShutdown()
            throw error
        }
    }

    private enum XCTUnwrapFailure: Error { case missingConfiguration }
}
